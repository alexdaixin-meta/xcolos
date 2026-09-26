"""The flow executor: runs a game from its definition.

An orchestrator like any other, so the kernel, the tools, the transports and
the console cannot tell it apart from the hardcoded Mafia. That is what lets
the two be switched between and compared on the same seed.

It knows the twelve flow slots and the five operations. It knows no game.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field as dataclass_field
from typing import Any, Iterator

from xcolos.flow.judge import (
    NO_REPLY,
    Call,
    Judge,
    Output,
    Reply,
    Where,
    prompt as user_prompt,
    system_prompt,
)
from xcolos.flow.state import Answer, FlowError, FlowState, seat_of as _seat, tally
from xcolos.games.definition import (
    NOBODY,
    Condition,
    GameDefinition,
    Operation,
    OptionSource,
    Selector,
    StepDef,
)
from xcolos.game import Game
from xcolos.orchestrators.base import ActionRequest, GameBrief
from xcolos.protocol import Action, ActionSchema
from xcolos.state import Audience

#: Template keys the engine will look for when a game has not named one at
#: the step. It supplies no wording of its own: these are the names a game
#: declares its own text under, and the loader refuses a game that needs one
#: and has not written it.
#:
#: There used to be English defaults here. They read as a convenience and
#: behaved as a trap — a game that forgot to word its ending got the engine's
#: sentence and nothing said so, which is the same failure as a silently
#: ignored field, arriving in front of the players.
REQUIRED_TEXT = {
    "answer_public": "how an answer is reported to everyone",
    "answer_ally": "how an answer is reported to the answerer's side",
    "answer_own": "how an answer is reported back to the answerer",
    "disclosed": "how a privately disclosed attribute is worded",
    "game_over": "how the end of the game is announced",
}


#: What each action asks a model for, and what the engine does with the answer.
#:
#: This is the contract in one place. An action fixes three things: which view
#: the model is shown, what shape must come back, and which engine call that
#: shape is fed to. A game supplies the prompt and the constraints; it cannot
#: change any of these, which is what lets the engine validate a reply and act
#: on it without reading prose.
#:
#: The middle column is the load-bearing one. A model never performs an action;
#: it returns a typed value, and the engine performs the action by calling the
#: named method with it. A reply that fails validation reaches no method at all.
ACTIONS = {
    "initialize": {
        "sees": "the attribute schema and the bare player list; nothing secret "
                "exists yet",
        "returns": "records",
        "engine_calls": "set_attribute / set_status, after a seeded shuffle",
    },
    "sync": {
        "sees": "nothing — no model is called",
        "returns": "no reply",
        "engine_calls": "emit_fact of that seat's own view, to that seat",
    },
    "tell": {
        "sees": "one recipient's view, per call",
        "returns": "message",
        "engine_calls": "emit_fact, and carry on",
    },
    "ask": {
        "sees": "one recipient's view, per call",
        "returns": "message",
        "engine_calls": "emit_fact, then park a turn and wait",
    },
    "poll": {
        "sees": "one recipient's view, per call",
        "returns": "message",
        "engine_calls": "emit_fact for all, park together, commit in seat order",
    },
    "broadcast": {
        "sees": "one listener's view, plus the answer being published",
        "returns": "message",
        "engine_calls": "emit_fact to that listener",
    },
    "update": {
        "sees": "the whole table",
        "returns": "update",
        "engine_calls": "the declared operations: set, adjust, append, remove, "
                        "set_status, disclose",
    },
    "check": {
        "sees": "the whole table",
        "returns": "boolean or choice",
        "engine_calls": "end_game, or nothing",
    },
}


@dataclass
class _Ask:
    """One step's question, resolved against the table as it stands."""

    step: StepDef
    seats: list[int]
    schema: ActionSchema
    legal: dict[int, tuple[Any, ...]]
    #: Per-seat wording, when a model composed it. Empty means the step's own
    #: template is used for everyone, which is the default.
    prompts: dict[int, str] = dataclass_field(default_factory=dict)


class FlowOrchestrator:
    """Plays whatever game a definition describes."""

    def __init__(
        self, definition: GameDefinition, judge: Judge | None = None
    ) -> None:
        self.definition = definition
        self.game_id = definition.id
        self.flow: FlowState | None = None
        #: Answers conditions written in prose. Optional: a game defined
        #: entirely in arithmetic never needs one, and that is the path the
        #: shipped Mafia takes so it can serve as the oracle for this one.
        self.judge = judge

    # ------------------------------------------------------------------
    # Orchestrator interface
    # ------------------------------------------------------------------

    def setup(self, game: Game) -> None:
        d = self.definition
        seats = sorted(game.seats)
        if not d.min_players <= len(seats) <= d.max_players:
            raise FlowError(
                f"{d.name} takes {d.min_players} to {d.max_players} players, "
                f"got {len(seats)}"
            )

        self.flow = FlowState(d, seats)
        for key, attribute in ((a.key, a) for a in d.game_attributes):
            self.flow.game_attributes[key] = attribute.initial

        # A declarative deal only runs when nothing else assigns. A game with
        # an `initialize` step keeps `deal` as that step's fallback, and
        # running both would deal the table twice.
        if d.deal and not any(s.use == "initialize" for s in d.setup):
            self._deal(game)
        self._run_setup(game)

    def brief(self, game: Game) -> GameBrief:
        d = self.definition
        return GameBrief(
            name=d.name,
            rules=d.rules,
            seat_count=len(game.seats),
            round_shape=[s.label for s in d.steps],
            actions=[self._schema(s) for s in d.steps if s.asks],
        )

    def play(self, game: Game) -> Iterator[Any]:
        """The loop: rounds of steps, until a declared end or the round cap.

        Four kinds of step and nothing else. `brief` happened at setup; the
        other three are the whole of what a round can contain.
        """
        d, flow = self.definition, self._state()
        while True:
            game.advance_round()
            # `rounds` is the cap a game expects to need; `rounds_max` is the
            # ceiling it may not raise itself past. Only the ceiling was being
            # checked, so a game that could not reach an ending ground through
            # two hundred rounds before saying so — slow enough to look like a
            # hang rather than a result.
            cap = min(d.limits.rounds, d.limits.rounds_max)
            if game.round > cap:
                game.abandon(f"round cap of {cap} reached")
                return
            flow.bindings.clear()

            for step in d.steps:
                if not self._gate(step, game):
                    continue

                game.set_phase(step.phase or step.label)

                if step.use in ("ask", "poll"):
                    # Nothing moves until the addressed players answer, and
                    # only then is the tally taken.
                    answers = yield from self._run_ask(game, step)
                    self._verify(game, step, answers)
                    self._settle(game, step)
                elif step.use == "sync":
                    self._sync(game, step)
                elif step.use == "tell":
                    # Delivered and acknowledged; the loop does not wait.
                    self._inform(game, step)

                elif step.use == "update":
                    self._apply(game, step.do)
                    self._announce(game, step)

                elif step.use == "check" and self._finish(game, step):
                    return

            if game.status.value != "running":
                return

    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------

    def _deal(self, game: Game) -> None:
        """Hand out hidden attributes from the seed. No model involved."""
        d, flow = self.definition, self._state()
        rows = list(d.deal.plan(len(flow.players)))
        offered = [dict(r) for r in rows]
        game.rng.shuffle(rows)
        self._assign(game, rows, label="deal", offered=offered, by="seed")

    def _run_setup(self, game: Game) -> None:
        """Run the game's declared setup steps, in order.

        These used to be two hardcoded emissions: a briefing to every seat and
        an allies notice to anyone with allies. Both are now just steps, which
        is what makes them optional, reorderable, renameable, addressable to
        whoever a game likes, and composable by a model.

        No step here may ask anything. Setup runs before the greeting goes out
        and before the game is running, so there is nobody to wait on.
        """
        for step in self.definition.setup:
            if not self._gate(step, game):
                continue
            game.set_phase(step.phase or step.label)
            if step.use == "initialize":
                self._initialize(game, step)
            elif step.use == "sync":
                self._sync(game, step)
            elif step.use == "update":
                self._apply(game, step.do)
                self._announce(game, step)
            else:
                self._inform(game, step)

    def _initialize(self, game: Game, step: StepDef) -> None:
        """Have a model write the state this step declared, then apply it.

        Both halves of the call come from `updates`: the schema shown to the
        model is the declared attributes' own types and values, and the
        validator is the same thing. A model cannot be told about a field the
        engine will not accept, or return one it was never told about.

        The target decides who gets what. `players` returns a set of records
        and the **seed** deals them, which is what keeps a match replayable
        and lets the arithmetic game grade this one. `each` returns a record
        per named player and the model decides the assignment, for the games
        where position is the answer rather than an accident.

        With no model, or a reply that fails validation or the roster
        requirement, the declarative `deal` block runs instead.
        """
        d, flow = self.definition, self._state()
        # The roster follows the table, not the file: two mafia at a table of
        # five is not a harder game, it is a finished one.
        roster = step.roster_for(len(flow.players))

        def schema(keys, lookup, kind):
            out: dict[str, dict[str, Any]] = {}
            for key in keys:
                attribute = lookup(key)
                if attribute is None:
                    raise FlowError(f"{key!r} is not a declared {kind} attribute")
                spec: dict[str, Any] = {"type": attribute.type}
                if attribute.values:
                    spec["values"] = list(attribute.values)
                out[key] = spec
            return out

        declared = step.updates.targets if step.updates else {}
        targets = {
            name: schema(
                keys,
                d.game_attribute if name == "table" else d.player_attribute,
                "table" if name == "table" else "player",
            )
            for name, keys in declared.items()
        }

        written = None
        if targets and self.judge is not None and step.llm:
            reply = self._ask(
                game,
                self._call(
                    game,
                    task="\n\n".join(part for part in (
                        step.llm,
                        # Who the players are is only told when the model is
                        # the one assigning. Handing it a roster of ids and
                        # names and then saying "order does not matter" are
                        # contradictory instructions: it will line the records
                        # up with the players it was just shown, and the
                        # seeded deal throws that correspondence away. With
                        # `players` the answer is a bag, so it is asked for as
                        # one.
                        (
                            f"There are {len(flow.players)} players: "
                            f"{[{'id': p, 'name': game.seats[p].name} for p in flow.players]}."
                            if "each" in targets
                            else f"There are {len(flow.players)} players."
                        ),
                        # The engine supplies the entropy; the game says what
                        # to do with it. A model has no randomness of its own —
                        # asked to assign at random it returns the same answer
                        # every match — but it can apply a rule to an order it
                        # is handed, and that order comes from the seed, so the
                        # match still replays.
                        (
                            f"Deal in this order: {self._dealing_order(game)}."
                            if "each" in targets
                            else ""
                        ),
                        # Stated as well as checked. A reply that fails the
                        # check is thrown away, so telling the model the
                        # requirement up front is the difference between one
                        # call and a fallback to the declarative deal.
                        _requirement_text(roster),
                    ) if part),
                    output=Output(
                        kind="state",
                        targets=targets,
                        players=tuple(flow.players),
                    ),
                    step=step,
                    tag=f"initialize:{step.label}",
                ),
            )
            written = reply.value
            if written is not None:
                # The roster is whichever target carried the players.
                rostered = written.get("players")
                if rostered is None and "each" in written:
                    rostered = list(written["each"].values())
                shortfall = _shortfall(roster, rostered)
                if shortfall:
                    # Every field was individually legal and the result is
                    # still unplayable. Declined whole rather than applied:
                    # half a roster is worse than the declarative fallback.
                    game.log.record(
                        "orchestrator", "roster_rejected",
                        step=step.label, reason=shortfall,
                    )
                    written = None

        if written is None:
            self._deal_declared(game, step)
            return

        # The table first, so a player record may depend on it.
        for key, value in (written.get("table") or {}).items():
            flow.set_attribute(None, key, value, dealing=True)
        if "players" in written:
            rows = list(written["players"])
            offered = [dict(r) for r in rows]
            game.rng.shuffle(rows)
            self._assign(game, rows, label=step.label, offered=offered, by="seed")
        if written.get("each"):
            for player, row in written["each"].items():
                self._assign_one(game, player, row)
            game.log.record(
                "orchestrator", "dealt",
                step=step.label,
                assigned={str(p): dict(r) for p, r in written["each"].items()},
                by="model",
            )

        # Counting the roster is not the same as checking it is playable. A
        # range wide enough to be useful at twelve players permits a roster at
        # four that is already won, and every field in it is legal.
        decided = self._already_decided(game)
        if decided:
            game.log.record(
                "orchestrator", "roster_rejected",
                step=step.label, reason=f"the game would begin already over: {decided}",
            )
            self._deal_declared(game, step)

    def _deal_declared(self, game: Game, step: StepDef) -> None:
        """Deal from the game's own `deal` block, using the seed."""
        d, flow = self.definition, self._state()
        if not d.deal:
            raise FlowError(
                f"{step.label}: no usable roster and the game declares no "
                f"`deal` block to fall back to"
            )
        rows = list(d.deal.plan(len(flow.players)))
        offered = [dict(r) for r in rows]
        game.rng.shuffle(rows)
        self._assign(game, rows, label=step.label, offered=offered, by="seed")

    def _already_decided(self, game: Game) -> str:
        """The name of an ending that holds before a move has been made.

        A game may not begin finished. That is true of every game, so the
        engine may check it without knowing which one it is running: it asks
        the game's own endings, in whichever language the game wrote them.
        """
        flow = self._state()
        spoken = self._which_ending(game, None)
        named = spoken[0].name if spoken else None
        for rule in self._endings_for(None):
            if rule.when.kind == "prose":
                if named == rule.name:
                    return rule.name
            elif flow.holds(rule.when):
                return rule.name
        return ""

    def _dealing_order(self, game: Game) -> list[int]:
        """A random ordering of the players, drawn from the seed.

        Handed to the model so a game can write its own dealing rule — "the
        first in this order is the mafia", "deal clockwise from the first" —
        without the engine knowing any of it, and without depending on a model
        to be random, which it cannot be.
        """
        order = list(self._state().players)
        game.rng.shuffle(order)
        return order

    def _assign(
        self, game: Game, rows: list[dict[str, Any]], *,
        label: str = "", offered: list[dict[str, Any]] | None = None,
        by: str = "seed",
    ) -> None:
        """Write one record onto each player, in seat order, and say so.

        The log line is not decoration. A model returns the same bag every
        match — it has no entropy and sits at the mode — so the only thing that
        differs between two matches is the placement, and until this existed
        nothing recorded where that placement came from. Reading the model's
        output alone, the deal looks ignored.
        """
        players = self._state().players
        for seat, row in zip(players, rows):
            self._assign_one(game, seat, row)
        game.log.record(
            "orchestrator", "dealt",
            step=label,
            offered=offered if offered is not None else [dict(r) for r in rows],
            assigned={str(seat): dict(row) for seat, row in zip(players, rows)},
            by=by,
        )

    def _assign_one(self, game: Game, seat: int, row: dict[str, Any]) -> None:
        """One record onto one player, mirrored to the kernel's own fields."""
        d, flow = self.definition, self._state()
        for key, value in row.items():
            flow.set_attribute(seat, key, value, dealing=True)
        game.seats[seat].attributes.update(row)
        # The kernel keeps two display fields from Milestone 1. The game says
        # which of its attributes fills them; the engine assumes no names.
        if d.display:
            game.set_role(
                seat,
                str(row.get(d.display.get("role", ""), "") or ""),
                str(row.get(d.display.get("faction", ""), "") or ""),
            )

    # ------------------------------------------------------------------
    # Steps
    # ------------------------------------------------------------------

    def _gate(self, step: StepDef, game: Game) -> bool:
        if step.when is None:
            return True
        if step.when.kind == "prose":
            # An unanswerable gate opens. A game that quietly skipped every
            # step would still look like a game; a game that runs a step it
            # should not is visible in the first transcript anybody reads.
            reply = self._judge(game, step.when, step, f"gate:{step.label or step.use}")
            return reply.value is not False
        return self._state().holds(step.when)

    #: The answer that means the game continues. Not an ending, so it can
    #: never collide with one a game declared.
    CONTINUE = "continue"

    def _endings_for(self, step: StepDef | None) -> list[Any]:
        """Which endings this check tests. All of them unless it says."""
        rules = list(self.definition.end)
        if step is None or not step.against:
            return rules
        wanted = set(step.against)
        return [rule for rule in rules if rule.name in wanted]

    def _which_ending(self, game: Game, step: StepDef | None) -> Any:
        """Ask once whether the game is over, and if so which way.

        The model is shown the whole table — every player's status and every
        attribute, hidden ones included — together with the winning conditions
        in the words the game wrote them in. It answers with the name of one
        ending or `continue`, and nothing else is accepted.

        One call however many endings are being tested. Returns the rule, or
        None for "no spoken ending applies", which covers a declined answer, an
        unreadable one, and no judge being wired in. All of those mean the
        match goes on.
        """
        spoken = [r for r in self._endings_for(step) if r.when.kind == "prose"]
        if not spoken or self.judge is None:
            return None

        listed = "\n".join(f"  {rule.name}: {rule.when.prose}" for rule in spoken)
        call = self._call(
            game,
            task="\n\n".join(
                part for part in (
                    step.llm if step and step.llm else "",
                    "Has this game finished? Below are its winning conditions, "
                    "each with a name. Answer with the name of the first one "
                    f"that is true of the table right now, or "
                    f"{self.CONTINUE!r} if none of them is.",
                    listed,
                ) if part
            ),
            output=Output(
                kind="choice",
                options=tuple(r.name for r in spoken) + (self.CONTINUE,),
            ),
            step=step,
            tag="check",
        )
        reply = self._ask(game, call)
        chosen = next((r for r in spoken if r.name == reply.value), None)
        return (chosen, reply.reason) if chosen else None

    def _judge(
        self, game: Game, condition: Condition, step: StepDef | None, tag: str
    ) -> Reply:
        """Put a prose condition to the judge, as a boolean call.

        Returns NO_REPLY when there is no judge or the answer did not parse.
        Both are the same thing to every caller: nobody answered.
        """
        if self.judge is None:
            return NO_REPLY
        call = self._call(
            game,
            task=(
                "Decide whether this statement about the table is true right "
                f"now:\n\n{condition.prose}"
            ),
            output=Output(kind="boolean"),
            step=step,
            tag=tag,
        )
        # Logged whether or not it changed anything, because the interesting
        # case is always the ruling that disagrees with what you expected.
        return self._ask(game, call)

    def _ask(self, game: Game, call: Call) -> Reply:
        """Put a call to the judge, and write the whole exchange to the log.

        Both halves of the prompt and the model's unparsed reply are recorded,
        not just the verdict. A ruling that looks wrong is either a model that
        said something odd or a parser that read it wrongly, and without the
        text in front of you there is no way to tell which.

        The prompt contains every hidden role, because the judge is shown the
        whole table. That is safe here and only here: this goes to the log,
        which is the operator's view, and never into a fact.
        """
        import time

        started = time.time()
        reply = self.judge.decide(call)
        game.log.record(
            "orchestrator",
            "judge_call",
            **call.to_json(),
            **reply.to_json(),
            model=getattr(self.judge, "name", ""),
            seconds=round(time.time() - started, 2),
            system=system_prompt(call),
            prompt=user_prompt(call),
        )
        return reply

    def _call(
        self,
        game: Game,
        *,
        task: str,
        output: Output,
        step: StepDef | None = None,
        tag: str = "",
        seat: int | None = None,
    ) -> Call:
        """Assemble one call. The only place a call is built.

        `seat` is the safety-critical argument. Pass it and the model is shown
        only what that seat may see; leave it out and the model is shown the
        whole table.

        The distinction is not about tidiness. A call whose answer is a verdict
        may have full sight, because a boolean carries nothing back to the
        players. A call whose answer is *text delivered to a player* may not:
        the reply is forwarded, so anything in the prompt can come out of it.
        Handing full sight to a call that writes a player's message makes the
        model the one thing between a hidden role and the table, which is
        exactly the arrangement the rest of this system exists to avoid.
        """
        flow = self._state()
        return Call(
            task=task,
            output=output,
            rules=self.definition.rules,
            table=flow.view(seat) if seat is not None else flow.full_view(),
            where=Where(
                round=game.round,
                phase=game.phase,
                slot=step.use if step else "",
                label=step.label if step else "",
                tag=tag,
            ),
        )

    def _announce(self, game: Game, step: StepDef) -> None:
        """What an `update` says about what it just changed."""
        self._say(
            game, list(self._state().players), step.text or "", step.llm or "",
            {}, step.label.replace(" ", "_"), step.max_words,
        )

    def _sync(self, game: Game, step: StepDef) -> None:
        """Send each addressed player their own state, as data.

        The one action that cannot leak by construction, because its payload
        *is* the entitlement filter: it sends `view(seat)` and nothing else, so
        there is no wording for a model to overreach in and no template for an
        author to get wrong.

        It also needs no authoring at all. A game with eight attributes does
        not write eight templates; the fields come from the schema and the
        filtering from the declared visibilities. `fields` may narrow it and
        can never widen it.

        Used after a deal or a resolution, when what a player needs is their
        standing rather than a sentence about it.
        """
        flow = self._state()
        if step.sync_mode == "others":
            self._sync_outward(game, step)
            return
        for seat in flow.select(step.to, acting_only=False):
            state = flow.view(seat)
            if step.fields:
                keep = set(step.fields)
                state = {
                    **state,
                    "you": {
                        **state["you"],
                        "attributes": {k: v for k, v in
                                       state["you"]["attributes"].items()
                                       if k in keep},
                    },
                    "players": [
                        {**p, "attributes": {k: v for k, v in
                                             p["attributes"].items() if k in keep}}
                        for p in state["players"]
                    ],
                }
            # The fact always carries the state as data. What a player
            # *reads* is prose when the step asks for it: a raw JSON dump is
            # accurate and close to unreadable, and an agent given one spends
            # its attention parsing rather than playing.
            written = self._word_state(game, step, seat, state)
            if written is None:
                # No model to word it. Pretty-printed JSON was going straight
                # to the player — thirty lines of braces for five facts. A
                # compact line says the same thing and can be read.
                header = (self._render(seat, step.text, {"you": seat})
                          if step.text else "")
                written = " ".join(
                    part for part in (header, _plain_state(state)) if part
                )
            game.emit_fact(
                step.label.replace(" ", "_"),
                {"state": state, "rendered": written},
                Audience.only(seat),
            )

    def _word_state(
        self, game: Game, step: StepDef, seat: int, state: dict[str, Any]
    ) -> str | None:
        """Have a model turn one player's state into something readable.

        None when the step asks for no wording or no model is reachable, and
        the caller falls back to the template plus the raw state.

        The call is given this seat's view and nothing else, so the prose can
        only ever describe what the player already holds. It is also told the
        shape of the table — how many are playing, who they are by seat — which
        is public and is the context a state dump lacks.
        """
        if not step.llm or self.judge is None:
            return None
        flow = self._state()
        reply = self._ask(
            game,
            self._call(
                game,
                task="\n\n".join((
                    step.llm,
                    f"There are {len(flow.players)} players, in seats "
                    f"{list(flow.players)}. You are writing to seat {seat}.",
                    "This is their own state, and everything they may see of "
                    "the others. Say only what is here.",
                )),
                output=Output(kind="message", max_words=step.max_words),
                step=step,
                tag=f"sync:{step.label}:seat{seat}",
                seat=seat,
            ),
        )
        return reply.value["text"] if reply.value else None

    def _sync_outward(self, game: Game, step: StepDef) -> None:
        """Send each addressed player's state to everyone but them.

        The mirror of the default. `self` answers "what do I know?"; this
        answers "what has just changed about them?" — the same facts arriving
        as news about somebody else rather than as your own standing.

        Each recipient is filtered separately through `can_see`, so a subject's
        hidden attributes reach only those entitled to them. Two players can be
        told about the same subject and be told different things, which is
        exactly what a hidden-role game needs.
        """
        flow, definition = self._state(), self.definition
        keep = set(step.fields)
        for subject in flow.select(step.to, acting_only=False):
            grouped: dict[str, list[int]] = {}
            for viewer in flow.players:
                if viewer == subject:
                    continue
                visible = {
                    a.key: flow.attribute(subject, a.key)
                    for a in definition.player_attributes
                    if (not keep or a.key in keep)
                    and flow.can_see(viewer, subject, a)
                }
                state = {
                    "player": subject,
                    "status": flow.status[subject],
                    "attributes": visible,
                }
                rendered = json.dumps(state, indent=2, sort_keys=True, default=str)
                grouped.setdefault(rendered, []).append(viewer)
            for rendered, audience in grouped.items():
                header = (self._render(None, step.text, {"seat": subject})
                          if step.text else "")
                game.emit_fact(
                    step.label.replace(" ", "_"),
                    {"player": subject,
                     "rendered": (header + "\n" if header else "") + rendered},
                    Audience.only(*audience),
                )

    def _inform(self, game: Game, step: StepDef) -> None:
        """Deliver an `ask` that wants no reply, to whoever it addresses.

        Rendered once per recipient, because a message may name its reader. A
        step marked `compose` has a model write each one instead, on that
        reader's own view; otherwise the game's template is filled.

        Recipients whose message comes out identical share one fact, so an
        announcement with no per-player wording stays a single announcement
        rather than N copies of the same sentence. That grouping is why a
        composed step produces one fact each and a templated one usually
        produces a single fact for the table.
        """
        flow = self._state()
        # Resolved before the audience is chosen, not after: `to` may be stated
        # relative to the subject — `author` to address the player this is
        # about, `others` to address everyone but them. Computing it afterwards
        # left those selectors naming nobody, silently.
        subject = self._subject_of(step)
        seats = flow.select(step.to, acting_only=False, subject=subject)
        if not seats:
            return

        written = self._compose_for(game, step, seats)
        if not step.text and not written:
            return

        grouped: dict[str, list[int]] = {}
        for seat in seats:
            said = written.get(seat)
            rendered = (
                said["text"] if said
                else self._render(
                    seat, step.text,
                    {"you": seat} | ({"subject": subject} if subject else {}),
                )
            )
            if rendered:
                grouped.setdefault(rendered, []).append(seat)

        for rendered, audience in grouped.items():
            everyone = len(audience) == len(flow.players)
            game.emit_fact(
                step.label.replace(" ", "_"),
                {"rendered": rendered},
                Audience.all() if everyone else Audience.only(*audience),
            )

    def _run_ask(self, game: Game, step: StepDef) -> Iterator[Any]:
        ask = self._resolve_ask(step)
        if not ask.seats:
            return {}

        # A composed step lets a model write each player's message and mark it
        # info or action. Those marked info are delivered and not waited for,
        # which is the only way the engine ever addresses a player without
        # stopping. Everyone else is asked exactly as the definition said.
        composed = self._compose(game, step, ask)
        if composed:
            told = [s for s, m in composed.items() if m["type"] == "info"]
            for seat in sorted(told):
                game.emit_fact(
                    step.label.replace(" ", "_"),
                    {"rendered": composed[seat]["text"], "composed": True},
                    Audience.only(seat),
                )
            ask = _Ask(
                step=ask.step,
                seats=[s for s in ask.seats if s not in told],
                schema=ask.schema,
                legal=ask.legal,
                prompts={s: m["text"] for s, m in composed.items()},
            )
            if not ask.seats:
                return {}

        if step.mode == "sequential":
            answers: dict[int, Action] = {}
            for seat in ask.seats:
                action = yield self._request(step, ask, seat)
                answers[seat] = action
                self._remember(game, step, seat, action)
                self._echo(game, step, seat, action)
            return answers

        actions = yield [self._request(step, ask, seat) for seat in ask.seats]
        for seat in sorted(actions):
            self._remember(game, step, seat, actions[seat])
        for seat in sorted(actions):
            self._echo(game, step, seat, actions[seat])
        return actions

    def _compose(
        self, game: Game, step: StepDef, ask: _Ask
    ) -> dict[int, dict[str, str]]:
        return self._compose_for(game, step, ask.seats, ask.legal)

    def _compose_for(
        self,
        game: Game,
        step: StepDef,
        seats: list[int],
        legal: dict[int, tuple[Any, ...]] | None = None,
    ) -> dict[int, dict[str, str]]:
        """Have a model write this step's messages, one reader at a time.

        One call per recipient, each shown only that recipient's view. That is
        more calls than writing them all at once, and it is the only version
        that is safe: a single call covering five players has to be shown five
        players' secrets, and its output goes to all five.

        Falls back per recipient rather than all-or-nothing. A player whose
        message did not come back usably gets the step's own template, which is
        the same message they would have had if nobody had composed anything.
        """
        # A prompt is the switch. No prompt, or no model, and the step falls
        # back to its template.
        if not step.llm or self.judge is None:
            return {}

        legal = legal or {}
        written: dict[int, dict[str, str]] = {}
        for seat in seats:
            reply = self._ask(
                game,
                self._call(
                    game,
                    task=self._compose_task(step, legal.get(seat, ()), seat),
                    output=Output(
                        kind="message",
                        # `max_words` on the step caps the message the model
                        # writes. The answer's own limit caps what the *player*
                        # replies, which is a different thing: a briefing has
                        # no answer at all and still wants a length.
                        max_words=step.max_words
                        or (step.answer.max_words if step.answer else 0),
                    ),
                    step=step,
                    tag=f"compose:{step.label}:seat{seat}",
                    seat=seat,
                ),
            )
            if reply.value:
                written[seat] = reply.value
        return written

    def _status_update(self, step: StepDef, subject: int, reader: int) -> str:
        """What the subject's named fields now hold, as this reader may see them.

        Assembled by the engine so a game never writes "player 3 is now
        eliminated" into a prompt by hand: it says which player and which
        fields, and the current values go in front of the model.

        Filtered per reader, not once for the step. Two players told about the
        same subject can be shown different things, which is the only way this
        is safe in a game where an attribute may be visible to one side alone.
        """
        flow, definition = self._state(), self.definition
        wanted = set(step.fields)
        shown = {
            a.key: flow.attribute(subject, a.key)
            for a in definition.player_attributes
            if (not wanted or a.key in wanted) and flow.can_see(reader, subject, a)
        }
        if not wanted or "status" in wanted:
            shown["status"] = flow.status[subject]
        return (
            f"Player {subject} now stands as: "
            + json.dumps(shown, sort_keys=True, default=str)
            + ". Report only these."
        )

    def _subject_of(self, step: StepDef) -> int | None:
        """The seat a step says it is about, if it names one."""
        if not step.about:
            return None
        return _seat(self._bind(step.about))

    def _compose_task(
        self, step: StepDef, legal: tuple[Any, ...], seat: int
    ) -> str:
        """What to tell the model it is writing, for one reader.

        Says plainly that it is writing *to* this player and may use only what
        it has been shown. The restricted view is the guarantee; this is the
        instruction that stops it inventing what it was not given.
        """
        # The game's own instruction, first and unconditionally. It used to be
        # squeezed into a "What this step is for:" line built from `prompt`,
        # which is a different field — so a step that declared only `llm` lost
        # its instruction entirely and the model wrote from the generic opener
        # below. The briefing was doing exactly that.
        lines = [
            f"Write the message that player {seat} receives now. Address them "
            f"directly. You have been shown only what this player may see, and "
            f"you must not write anything you were not shown.",
        ]
        if step.llm:
            lines.append(step.llm)
        subject = self._subject_of(step)
        if subject is not None:
            # Who the message is about. A template reaches this through the
            # binding; without saying it here, a prompt cannot.
            lines.append(
                f"This message is about player {subject}. What you have been "
                f"shown of them is in the state above; say nothing else."
            )
            if step.kind == "status_update":
                lines.append(self._status_update(step, subject, seat))
        elif step.text:
            lines.append(f"What this step is for: {self._prompt(step)}")
        if step.asks:
            lines.append(
                f"This player must answer. Mark the message `action`."
                + (f" They may only choose from: {list(legal)}." if legal else "")
            )
        else:
            lines.append("This player only needs to read it. Mark it `info`.")
        return "\n\n".join(lines)

    #: Answer types where an empty list of candidates makes the question
    #: unanswerable rather than merely open-ended.
    _NEEDS_A_TARGET = ("player", "players", "choice")

    def _resolve_ask(self, step: StepDef) -> _Ask:
        flow = self._state()
        legal: dict[int, tuple[Any, ...]] = {}
        seats: list[int] = []
        for seat in flow.select(step.to):
            candidates = self._legal_for(step, seat)
            if not candidates and step.answer.type in self._NEEDS_A_TARGET:
                # Nobody left to point at. Asking anyway gets an empty answer
                # that looks like a choice, and an empty choice is what ends up
                # in a binding and then in an operation.
                continue
            seats.append(seat)
            legal[seat] = candidates
        return _Ask(step=step, seats=seats, schema=self._schema(step), legal=legal)

    def _legal_for(self, step: StepDef, seat: int) -> tuple[Any, ...]:
        answer, flow = step.answer, self._state()
        if answer.type not in ("player", "players"):
            if answer.options_from:
                return self._options_from_state(answer.options_from, seat)
            return tuple(answer.options)

        candidates = flow.acting()
        if answer.exclude_self:
            candidates = [p for p in candidates if p != seat]
        if answer.exclude:
            excluded = set(flow.select(answer.exclude, acting_only=False))
            candidates = [p for p in candidates if p not in excluded]
        return tuple(candidates)

    def _options_from_state(self, source: OptionSource, seat: int) -> tuple[Any, ...]:
        """The choices this one player has, read from the table as it stands.

        A player holding nothing gets an empty tuple and is skipped by
        `_resolve_ask`, which is the same treatment as a vote with nobody left
        to point at: a question with no answer is not asked.
        """
        flow = self._state()
        held = (flow.game_attributes.get(source.key) if source.scope == "game"
                else flow.attribute(seat, source.key))
        return tuple(held) if isinstance(held, list) else ()

    def _request(self, step: StepDef, ask: _Ask, seat: int) -> ActionRequest:
        schema = ask.schema
        if schema.target == "enum":
            # The step's schema carries whatever the file listed, which is
            # nothing when the options come from state. Validation and the
            # rendered "answer with one of" both read `choices`, so a
            # per-player hand has to reach them per player.
            schema = self._schema(step, ask.legal[seat])
        return ActionRequest(
            seat=seat,
            schema=schema,
            prompt=ask.prompts.get(seat) or self._prompt(step),
            legal_targets=ask.legal[seat],
            deadline_ms=(step.deadline_s or self.definition.limits.deadline_s) * 1000,
            reason=f"{step.use}:{step.label}",
        )

    def _schema(
        self, step: StepDef, choices: tuple[Any, ...] | None = None
    ) -> ActionSchema:
        answer = step.answer
        target = {"player": "seat", "players": "seat", "choice": "enum"}.get(
            answer.type, answer.type
        )
        return ActionSchema(
            id=step.label.replace(" ", "_"),
            target=target,
            choices=tuple(answer.options) if choices is None else tuple(choices),
            default="random" if target == "seat" else "pass",
            max_words=answer.max_words,
        )

    def _prompt(self, step: StepDef) -> str:
        """What an addressed player is told, when no model writes it.

        The game's `prompt`, and the answer's word limit if it has one. This
        used to return the step's *label* — an identifier, shown to a player as
        their instruction. It read sensibly only because Mafia's labels happen
        to be noun phrases; a step called `s2` sent the word "s2." and nothing
        flagged it. The loader now requires a prompt on any step that asks.
        """
        words = step.answer.max_words if step.answer else 0
        limit = f" in {words} words or fewer" if words else ""
        return f"{self._render(None, step.text, {})}{limit}".strip()

    # ------------------------------------------------------------------
    # Answers
    # ------------------------------------------------------------------

    def _remember(self, game: Game, step: StepDef, seat: int, action: Action) -> None:
        flow = self._state()
        flow.remember(
            Answer(
                round=game.round,
                step=step.label,
                player=seat,
                value=action.target if action.target is not None else action.text,
                # The record notes who was told, which is now the broadcast's
                # audience rather than a separate visibility field.
                visible=step.broadcast.to if step.broadcast else "none",
                reason=action.reason,
            )
        )

    def _echo(self, game: Game, step: StepDef, seat: int, action: Action) -> None:
        """Tell whoever the step says may learn what this player answered.

        Absent a `broadcast` block, nobody is told. A step has to ask to be
        published, which is the right default when some steps are secret
        ballots and the cost of getting it backwards is the whole game.
        """
        if step.broadcast is None:
            return
        flow, spec = self._state(), step.broadcast
        value = action.target if action.target is not None else action.text

        heard = flow.select(spec.to, acting_only=False, subject=seat)
        if not heard:
            return

        written = self._write_broadcast(game, step, seat, value, heard)
        grouped: dict[str, list[int]] = {}
        for listener in heard:
            # Rendered with no owning seat, so a listener's own attributes
            # cannot shadow `seat` or `value` and put their hidden state into
            # somebody else's copy of the message.
            rendered = written.get(listener) or (
                self._render(None, spec.text,
                             {"seat": seat, "you": seat, "value": value})
                if spec.text
                # No template: the answer is the message. Delivered whole,
                # word for word — a broadcast that reworded what a player said
                # would be the referee putting words in their mouth.
                else str(value)
            )
            if rendered:
                grouped.setdefault(rendered, []).append(listener)

        for rendered, audience in grouped.items():
            everyone = len(audience) == len(flow.players)
            game.emit_fact(
                step.label.replace(" ", "_"),
                {"seat": seat, "value": value, "rendered": rendered},
                Audience.all() if everyone else Audience.only(*audience),
            )

    def _write_broadcast(
        self, game: Game, step: StepDef, author: int, value: Any, heard: list[int]
    ) -> dict[int, str]:
        """Have a model word the broadcast, one listener at a time.

        Each call sees only that listener's view, plus the answer being
        published. The answer is handed over as a quoted string with an
        instruction to reproduce it exactly: a broadcast that paraphrases what
        a player said is not a broadcast, it is the referee putting words in
        their mouth, and in a game about reading each other that is the whole
        substance being altered.
        """
        spec = step.broadcast
        if spec is None or not spec.llm or self.judge is None:
            return {}

        out: dict[int, str] = {}
        for listener in heard:
            reply = self._ask(
                game,
                self._call(
                    game,
                    task=(
                        f"{spec.llm}\n\n"
                        f"Player {author} answered, exactly: {value!r}\n\n"
                        f"Write what player {listener} is told about it. "
                        f"Reproduce their answer word for word; you may frame "
                        f"it, never reword it. You have been shown only what "
                        f"player {listener} may see."
                    ),
                    output=Output(kind="message"),
                    step=step,
                    tag=f"broadcast:{step.label}:seat{listener}",
                    seat=listener,
                ),
            )
            if reply.value:
                out[listener] = reply.value["text"]
        return out

    def _settle(self, game: Game, step: StepDef) -> None:
        """Act on what the answers came to, and say what happened.

        One step now covers asking, reducing, applying and announcing, because
        in a game they are one act. They used to be a `poll` that bound a name
        and an `update` that read it back, with every operation guarded for the
        case where the tally chose nobody — and that guard was the whole of the
        tie handling, so a tie announced nothing.

        `$result` is this step's own outcome, available to the branch without
        the game naming it. `verify.bind` still exists for a result a *later*
        step needs, which is a different thing.
        """
        if step.outcome is None:
            return
        flow = self._state()
        # `_verify` stores this step's outcome under `result`, and under the
        # game's own name too when `bind` asks for one. Reading it back as
        # "$result" — the form a game *writes* — found nothing, so every vote
        # took the tie branch and the table was told a decided vote was tied.
        result = flow.bindings.get("result")
        if result is None and step.verify and step.verify.bind:
            result = flow.bindings.get(step.verify.bind)
        chose = _seat(result) is not None
        branch = step.outcome.chosen if chose else step.outcome.none
        if branch is None:
            return

        flow.bindings["result"] = result
        self._say_outcome(game, step, branch, result)
        # After the announcement, because these elaborate on it: a role
        # disclosure reads as a non sequitur before anyone has been told who
        # it is about.
        self._apply(game, branch.do)

    def _say_outcome(
        self, game: Game, step: StepDef, branch: Any, result: Any
    ) -> None:
        flow = self._state()
        key = branch.text
        if branch.llm and self.judge is not None:
            key = ""
        if not key and not branch.llm:
            return
        heard = flow.select(branch.to, acting_only=False, subject=_seat(result))
        if not heard:
            return
        written = self._word_outcome(game, step, branch, result, heard)
        for seat in heard if written else [None]:
            rendered = written.get(seat) if written else self._render(
                None, key, {"result": result})
            if not rendered:
                continue
            game.emit_fact(
                step.label.replace(" ", "_") + "_result",
                {"result": result, "rendered": rendered},
                Audience.all() if len(heard) == len(flow.players) and not written
                else Audience.only(*(heard if not written else [seat])),
            )

    def _word_outcome(
        self, game: Game, step: StepDef, branch: Any, result: Any, heard: list[int]
    ) -> dict[int, str]:
        """Have a model announce the outcome, one listener at a time."""
        if not branch.llm or self.judge is None:
            return {}
        out: dict[int, str] = {}
        for listener in heard:
            reply = self._ask(
                game,
                self._call(
                    game,
                    task=(
                        f"{branch.llm}\n\n"
                        f"The step was {step.label!r} and it came to: {result!r}."
                    ),
                    output=Output(kind="message", max_words=step.max_words),
                    step=step,
                    tag=f"outcome:{step.label}:seat{listener}",
                    seat=listener,
                ),
            )
            if reply.value:
                out[listener] = reply.value["text"]
        return out

    def _verify(self, game: Game, step: StepDef, answers: dict[int, Action]) -> None:
        """The system's own arithmetic, binding a name for later steps."""
        if step.verify is None:
            return
        flow = self._state()

        if step.verify.tally:
            values = [
                a.target if a.target is not None else a.text
                for _, a in sorted(answers.items())
            ]
            result = tally(values, step.verify.tally, step.verify.on_tie, game.rng)
        elif answers:
            result = next(
                (a.target if a.target is not None else a.text)
                for _, a in sorted(answers.items())
            )
        else:
            result = NOBODY

        if step.verify.bind:
            flow.bindings[step.verify.bind] = result
        # This step's own outcome, for its `outcome` block. Named separately so
        # a step can act on its result without the game inventing a binding.
        flow.bindings["result"] = result

    # ------------------------------------------------------------------
    # Operations
    # ------------------------------------------------------------------

    def _apply(self, game: Game, operations: tuple[Operation, ...]) -> None:
        """Perform each declared change, and say so where the game asked.

        Announcing is handled here rather than inside each operation, so every
        one of the six gets it on the same terms. It used to be wired into
        `set_status` alone — added for the elimination message — which left a
        score change or a card entering a hand with no way to be told to
        anybody.
        """
        for operation in operations:
            args = self._bind(operation.args)
            if args.get("unless") is not None and args.get(
                _subject_key(operation)
            ) == args["unless"]:
                continue
            getattr(self, "_op_" + operation.op)(game, args)
            self._announce_change(game, operation, args)

    def _op_set_status(self, game: Game, args: dict[str, Any]) -> None:
        """Change a player's status, and say so if the game asked.

        `text` is what makes an elimination announceable without revealing
        anything about the player. Before it, the only way to tell the table
        that somebody was voted out was to `disclose` their role in the same
        breath — so a game that eliminates without revealing could not be
        written, and Mafia's own "who is out" message was a side effect of the
        reveal rather than a thing it asked for.
        """
        seat = _seat(args.get("player"))
        if seat is None:
            return
        self._state().set_status(seat, str(args["to"]))
        if not self._state().acts(seat) and game.seats[seat].alive:
            game.eliminate(seat)

    def _announce_change(
        self, game: Game, operation: Operation, args: dict[str, Any]
    ) -> None:
        """Tell whoever the operation names about the change it just made.

        Silent unless it declares `text` or `llm`. `announce_to` chooses the
        audience and defaults to everyone; a change nobody may hear about is
        better expressed as no announcement than as one sent nowhere.

        A `disclose` announces itself, because the message *is* the disclosure
        and it goes to exactly the players who learned it.
        """
        if operation.op == "disclose":
            return
        if not (args.get("text") or args.get("llm")):
            return
        flow = self._state()
        subject = _seat(args.get(_subject_key(operation)))
        heard = flow.select(
            Selector.parse(args.get("announce_to", "all"), "announce_to"),
            acting_only=False, subject=subject,
        )
        self._say(
            game, heard,
            str(args.get("text") or ""), str(args.get("llm") or ""),
            {k: v for k, v in args.items()
             if k not in ("text", "llm", "announce_to", "unless")}
            | {"player": subject, "subject": subject},
            str(args.get("text") or operation.op),
            int(args.get("max_words", 0)),
        )

    def _say(
        self,
        game: Game,
        heard: list[int],
        text: str,
        llm: str,
        extra: dict[str, Any],
        fact_type: str,
        max_words: int = 0,
    ) -> None:
        """Announce something, worded by the game or by a model.

        The one place an announcement is turned into words, so every site gets
        the same choice: a prompt if the game wrote one and a model is
        reachable, its template otherwise. Three announcements used to be
        template-only for no reason other than the order they were written in.

        A model-written announcement is composed per listener, on that
        listener's own view, like every other player-facing call.
        """
        flow = self._state()
        if not heard:
            return
        everyone = len(heard) == len(flow.players)

        if llm and self.judge is not None:
            for listener in heard:
                reply = self._ask(
                    game,
                    self._call(
                        game,
                        task=f"{llm}\n\nWhat happened: "
                             + json.dumps(extra, sort_keys=True, default=str),
                        output=Output(kind="message", max_words=max_words),
                        tag=f"announce:{fact_type}:seat{listener}",
                        seat=listener,
                    ),
                )
                if reply.value:
                    game.emit_fact(
                        fact_type,
                        {**extra, "rendered": reply.value["text"]},
                        Audience.only(listener),
                    )
            return

        rendered = self._render(None, text, extra) if text else ""
        if not rendered:
            return
        game.emit_fact(
            fact_type,
            {**extra, "rendered": rendered},
            Audience.all() if everyone else Audience.only(*heard),
        )

    def _op_set(self, game: Game, args: dict[str, Any]) -> None:
        self._state().set_attribute(args.get("player"), str(args["key"]), args.get("value"))

    def _op_adjust(self, game: Game, args: dict[str, Any]) -> None:
        flow, key = self._state(), str(args["key"])
        seat = args.get("player")
        current = (
            flow.attribute(int(seat), key) if seat is not None
            else flow.game_attributes.get(key)
        ) or 0
        flow.set_attribute(seat, key, current + args.get("value", 0))

    def _op_append(self, game: Game, args: dict[str, Any]) -> None:
        flow, key = self._state(), str(args["key"])
        seat = args.get("player")
        current = list(
            (flow.attribute(int(seat), key) if seat is not None
             else flow.game_attributes.get(key)) or []
        )
        current.append(args.get("value"))
        flow.set_attribute(seat, key, current)

    def _op_remove(self, game: Game, args: dict[str, Any]) -> None:
        flow, key = self._state(), str(args["key"])
        seat = args.get("player")
        current = list(
            (flow.attribute(int(seat), key) if seat is not None
             else flow.game_attributes.get(key)) or []
        )
        if args.get("value") in current:
            current.remove(args["value"])
        flow.set_attribute(seat, key, current)

    def _op_disclose(self, game: Game, args: dict[str, Any]) -> None:
        """Tell named players one attribute of one player.

        The system reads the value itself. No model is ever shown it, which is
        why a detective's result does not need a model with full sight.
        """
        flow = self._state()
        owner = _seat(args.get("of"))
        if owner is None:
            return
        key = str(args["attribute"])
        value = flow.attribute(owner, key)

        to = args.get("to", "all")
        audience = (
            flow.players if to == "all"
            else flow.select(Selector.parse(to, "disclose.to"), acting_only=False)
        )
        flow.disclose(audience, owner, key, value)
        game.emit_fact(
            "disclosed",
            self._payload(
                None,
                args.get("text") or "disclosed",
                {"player": owner, "subject": owner, "key": key, "value": value},
            ),
            Audience.only(*audience) if to != "all" else Audience.all(),
        )

    # ------------------------------------------------------------------
    # Ending
    # ------------------------------------------------------------------

    def _finish(self, game: Game, step: StepDef | None = None) -> bool:
        """Has the game ended? At most one model call, however many rules.

        The rules are still tried strictly in their declared order, so an
        earlier ending beats a later one. What changed is that the prose rules
        are asked about together rather than one call each: a check step with
        three spoken endings was three sequential round trips, and on a slow
        model that is the whole cost of a round.
        """
        flow = self._state()
        spoken = self._which_ending(game, step)

        for rule in self._endings_for(step):
            if rule.when.kind == "prose":
                # Unanswered endings are declined. A match that overruns hits
                # the round cap and says so; a match that ends on a question
                # nobody answered is indistinguishable from one that ended
                # correctly, and that is the failure you cannot debug.
                if spoken is None or spoken[0] is not rule:
                    continue
                reason = spoken[1] or rule.reason
            elif flow.holds(rule.when):
                reason = rule.reason
            else:
                continue

            # What becomes public is this ending's business, not the game's as
            # a whole: some games reveal different things depending on how they
            # finished.
            for key in rule.reveal or self.definition.reveal:
                for seat in flow.players:
                    game.seats[seat].attributes[key] = flow.attribute(seat, key)
            self._say(
                game, list(flow.players),
                rule.text or "game_over", rule.llm,
                {"winner": rule.result, "result": rule.result,
                 "ending": rule.name, "reason": reason},
                "game_over",
            )
            game.end_game(rule.result, reason)
            return True
        return False

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _state(self) -> FlowState:
        if self.flow is None:
            raise FlowError("setup has not run")
        return self.flow

    def _bind(self, args: Any) -> Any:
        """Replace `$name` with whatever a `verify` bound it to."""
        if isinstance(args, str) and args.startswith("$"):
            return self._state().bindings.get(args[1:])
        if isinstance(args, dict):
            return {k: self._bind(v) for k, v in args.items()}
        if isinstance(args, list):
            return [self._bind(v) for v in args]
        return args

    def _payload(self, seat: int | None, key: str, extra: dict[str, Any]) -> dict[str, Any]:
        return {**extra, "rendered": self._render(seat, key, extra)}

    def _render(self, seat: int | None, key: str, extra: dict[str, Any]) -> str:
        """Fill a template. `{name}` only, no expressions.

        The template is the game's if it declared one under this key, and the
        engine's default otherwise. A game that declares every key in
        every key it references shares no wording with the engine at all.

        Three kinds of name are in scope, and the rule for which is which is
        the same for every game:

        - `{you}` and any bare attribute name: the seat being written to.
        - `{some_binding}`: whatever a `verify` bound, usually a seat number.
        - `{some_binding_attribute}`: an attribute of the player that binding
          named. This is how a death notice reaches the dead player's role
          without the engine knowing that a binding called `target` exists.
        """
        # A name in the `text` block, or the words themselves. Every template
        # in Mafia was referenced exactly once, so the indirection cost a
        # lookup on every read and bought no reuse; a game may still name one
        # where it genuinely shares wording between steps.
        template = self.definition.text.get(key, key)
        flow = self._state()

        context: dict[str, Any] = dict(flow.bindings)
        for name, value in flow.bindings.items():
            subject = _seat(value)
            if subject is not None and subject in flow.player_attributes:
                for attribute, held in flow.player_attributes[subject].items():
                    context[f"{name}_{attribute}"] = held
        context.update(extra)
        if seat is not None:
            context.setdefault("you", seat)
            context.update(flow.player_attributes[seat])
            # Allegiance is a concept the engine owns, so a message may name
            # the reader's allies without the game computing them.
            allies = sorted(flow.allies_of(seat) - {seat})
            context.setdefault("allies", ", ".join(str(a) for a in allies))
            context.setdefault("ally_count", len(allies))

        def fill(match: re.Match[str]) -> str:
            name = match.group(1)
            return str(context.get(name, match.group(0)))

        return re.sub(r"\{(\w+)\}", fill, template)


def _subject_key(operation: Operation) -> str:
    return "of" if operation.op == "disclose" else "player"


def _plain_state(state: dict[str, Any]) -> str:
    """One seat's state on one line, for when no model is there to word it.

    Not prose and not trying to be: it is the offline fallback, and its job is
    to be complete and legible rather than good. Skips players it can say
    nothing about, because "seat 3: nothing" repeated four times is noise.
    """
    you = state.get("you") or {}
    bits = [f"You are seat {you.get('id')}"]
    own = ", ".join(f"{k} {v}" for k, v in sorted((you.get("attributes") or {}).items())
                    if v is not None)
    if own:
        bits.append(own)
    known = [
        f"seat {p['id']} " + ", ".join(f"{k} {v}" for k, v in sorted(p["attributes"].items()))
        for p in state.get("players") or []
        if p["id"] != you.get("id") and p.get("attributes")
    ]
    if known:
        bits.append("you know " + "; ".join(known))
    table = ", ".join(f"{k} {v}" for k, v in sorted((state.get("table") or {}).items()))
    if table:
        bits.append(table)
    acting = state.get("acting") or []
    bits.append(f"still playing: {', '.join(str(a) for a in acting)}")
    return ". ".join(bits) + "."


def _requirement_text(requires: dict[str, Any]) -> str:
    """The roster requirement, spelled out for the model."""
    if not requires:
        return ""
    lines = ["The roster must satisfy exactly this, or it will be rejected:"]
    for key, counts in requires.items():
        for value, wanted in counts.items():
            want = (f"exactly {wanted}" if isinstance(wanted, int)
                    else f"between {wanted[0]} and {wanted[1]}")
            lines.append(f"  {want} player(s) with {key} = {value}")
    return "\n".join(lines)


def _shortfall(requires: dict[str, Any], records: Any) -> str:
    """Why this roster is unplayable, or "" if it is fine.

    The schema checks each field on its own. This checks the set: a reply of
    four villagers and no mafia passes every type and value test and produces a
    game nobody can win.
    """
    if not requires:
        return ""
    rows = records.get("players") if isinstance(records, dict) else records
    if not isinstance(rows, list):
        return "the reply carried no player records"

    for key, counts in requires.items():
        for value, wanted in counts.items():
            got = sum(1 for row in rows if row.get(key) == value)
            low, high = (wanted, wanted) if isinstance(wanted, int) else wanted
            if not low <= got <= high:
                want = f"{low}" if low == high else f"{low} to {high}"
                return (
                    f"{key}={value!r}: wanted {want}, got {got} "
                    f"in {len(rows)} players"
                )
    return ""
