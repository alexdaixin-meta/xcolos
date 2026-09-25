"""The definition-driven engine: allegiance, visibility, and a whole match.

The visibility tests here are the ones worth keeping. A hidden-role game is
only a game because some players cannot see some things, so "who may see this"
deserves a test that fails loudly rather than a comment.
"""

from __future__ import annotations

import json

from xcolos.agents import ScriptedAgent
from xcolos.flow import FlowOrchestrator, ScriptedJudge
from xcolos.flow.state import FlowState
from xcolos.game import Game
from xcolos.games import available
from xcolos.games.definition import parse
from xcolos.games.loader import LIBRARY, load
from xcolos.host import LocalAgentHost, Registry
from xcolos.identity import Player
from xcolos.log import MatchLog
from xcolos.runner import Runner

NAMES = ["Ada", "Blaise", "Curie", "Dirac", "Euler", "Fermi", "Gauss"]


def play(seed: int = 1, seats: int = 5, game_id: str = "mafia-oracle"):
    """Run one whole match through the flow engine. Returns (result, game)."""
    log = MatchLog(f"flow_{seed}")
    game = Game(f"flow_{seed}", game_id, seed, log)
    registry = Registry(game.match_id)
    host = LocalAgentHost(
        [ScriptedAgent(name=NAMES[i]) for i in range(seats)],
        player=Player.new("operator"),
    )
    for bound in host.register():
        index = game.register_seat(bound.name, host.host_id, bound.profile)
        registry.attach(index, host, bound)
    orchestrator = FlowOrchestrator(available()[game_id])
    return Runner(game, orchestrator, registry).run(), game


# ----------------------------------------------------------------------
# Allegiance
# ----------------------------------------------------------------------


def _state(rows, **overrides):
    """A FlowState over a one-attribute definition, with roles assigned."""
    definition = parse(
        {
            "schema": 1,
            "meta": {"id": "t", "name": "T"},
            "statuses": [{"id": "active", "acts": True, "initial": True}],
            "attributes": {
                "player": [{"key": "faction", "visible": "ally", "type": "text"}]
            },
            "deal": {"into": ["faction"], "by_players": {"1": [{"faction": "x"}]}},
            "steps": [{"use": "check"}],
            "end": {
                "good_wins": {
                    "when": {
                        "count": {"attribute": "faction", "is": "evil"},
                        "op": "==",
                        "value": 0,
                    },
                    "result": "good",
                }
            },
            "text": {"game_over": "Over: {result}, {reason}."},
            **overrides,
        }
    )
    state = FlowState(definition, list(range(1, len(rows) + 1)))
    for player, faction in enumerate(rows, start=1):
        state.set_attribute(player, "faction", faction, dealing=True)
    return state


def test_no_allegiance_makes_everyone_their_own_only_ally():
    state = _state(["evil", "evil", "good"])
    assert state.allies_of(1) == {1}
    assert state.allies_of(2) == {2}


def test_declared_mutual_value_shares_sight_within_that_value_only():
    # The whole point: both sides have a faction, but only one side is a team
    # that knows itself.
    state = _state(
        ["evil", "evil", "good", "good"],
        allies_by={"attribute": "faction", "mutual": ["evil"]},
    )
    assert state.allies_of(1) == {1, 2}
    assert state.allies_of(2) == {1, 2}
    assert state.allies_of(3) == {3}, "the town must not know the town"
    assert state.allies_of(4) == {4}


def test_omitting_mutual_makes_every_value_a_knowing_team():
    state = _state(["red", "red", "blue"], allies_by="faction")
    assert state.allies_of(1) == {1, 2}
    assert state.allies_of(3) == {3}


def test_a_null_attribute_is_never_an_allegiance():
    state = _state([None, None, "evil"], allies_by="faction")
    assert state.allies_of(1) == {1}, "sharing 'unknown' is not sharing a side"


# ----------------------------------------------------------------------
# Visibility, from the game definition Mafia actually ships
# ----------------------------------------------------------------------


def test_only_the_town_is_blind_to_the_town():
    definition = available()["mafia-oracle"]
    state = FlowState(definition, [1, 2, 3, 4, 5])
    for player, (role, faction) in enumerate(
        [
            ("mafia", "evil"),
            ("detective", "good"),
            ("villager", "good"),
            ("villager", "good"),
            ("villager", "good"),
        ],
        start=1,
    ):
        state.set_attribute(player, "role", role, dealing=True)
        state.set_attribute(player, "faction", faction, dealing=True)

    role = definition.player_attribute("role")
    for viewer in state.players:
        for owner in state.players:
            expected = viewer == owner
            assert state.can_see(viewer, owner, role) is expected, (
                f"seat {viewer} seeing seat {owner}"
            )


def test_a_view_carries_only_what_that_seat_may_see():
    _, game = play(seed=1)
    definition = available()["mafia-oracle"]
    # Rebuild the deal the match produced and check every seat's view against it.
    state = FlowState(definition, sorted(game.seats))
    for index, seat in game.seats.items():
        state.set_attribute(index, "role", seat.role, dealing=True)
        state.set_attribute(index, "faction", seat.faction, dealing=True)

    for viewer in state.players:
        view = state.view(viewer)
        for entry in view["players"]:
            if entry["id"] == viewer:
                assert entry["attributes"]["role"] == state.attribute(viewer, "role")
            else:
                assert "role" not in entry["attributes"]
                assert "faction" not in entry["attributes"]


# ----------------------------------------------------------------------
# A whole match
# ----------------------------------------------------------------------


def test_the_shipped_definition_plays_a_match_to_a_declared_ending():
    result, game = play(seed=1)
    assert result.status == "ended"
    assert result.winner in {"town", "mafia"}
    assert result.reason, "an ending must say why it ended"
    assert result.rounds >= 1 and result.turns > 0
    assert len(game.seats) == 5


def test_the_roster_is_one_mafia_and_one_detective_at_every_size():
    for seats in (4, 5, 6, 7):
        _, game = play(seed=3, seats=seats)
        roles = [s.role for s in game.seats.values()]
        assert roles.count("mafia") == 1, f"{seats} seats dealt {roles}"
        assert roles.count("detective") == 1, f"{seats} seats dealt {roles}"
        assert roles.count("villager") == seats - 2


def test_the_same_seed_plays_the_same_match():
    first, _ = play(seed=7)
    second, _ = play(seed=7)
    assert (first.winner, first.reason, first.rounds) == (
        second.winner,
        second.reason,
        second.rounds,
    )


def test_nobody_is_ever_told_another_seats_role_before_it_is_revealed():
    """Delivery equals entitlement, checked against what was actually sent."""
    _, game = play(seed=2)
    secret = {i: s.role for i, s in game.seats.items()}
    revealed: set[int] = set()

    for fact in game.facts:
        text = str(fact.payload.get("rendered", ""))
        for owner, role in secret.items():
            if owner in revealed or role == "villager":
                continue
            # A role naming a seat may only reach that seat.
            if f"seat {owner}" in text and role in text:
                recipients = sorted(fact.entitled)
                assert recipients == [owner], (
                    f"seat {owner} is {role}; {text!r} went to {recipients}"
                )
        if fact.type in {"reveal", "resolve_vote"}:
            revealed |= {s for s in game.seats}


# ----------------------------------------------------------------------
# Composed steps: the model writes the message and says whether to wait
# ----------------------------------------------------------------------


def composed_mafia(label: str = "the debate") -> dict:
    """The shipped Mafia, with one step's messages written by a model."""
    raw = json.loads((LIBRARY / "mafia_oracle.json").read_text(encoding="utf-8"))
    for step in raw["steps"]:
        if step.get("label") == label:
            step["llm"] = "Tell this player the floor is theirs."
    return raw


def play_with(raw: dict, judge, seed: int = 1, seats: int = 5):
    definition = load(json.dumps(raw), source="composed")
    log = MatchLog(f"c{seed}")
    game = Game(f"c{seed}", definition.id, seed, log)
    registry = Registry(game.match_id)
    host = LocalAgentHost(
        [ScriptedAgent(name=NAMES[i]) for i in range(seats)],
        player=Player.new("operator"),
    )
    for bound in host.register():
        index = game.register_seat(bound.name, host.host_id, bound.profile)
        registry.attach(index, host, bound)
    return Runner(game, FlowOrchestrator(definition, judge=judge), registry).run(), game


def composer(mark="action", text=None):
    """A stub that writes one message per call, and records the calls."""
    seen = []

    def compose(call):
        if call.output.kind != "message":
            return None
        seen.append(call)
        return {"type": mark, "text": text or f"Your turn, player {call.where.tag}."}

    return ScriptedJudge(compose), seen


def test_a_composed_step_asks_once_per_recipient():
    judge, seen = composer()
    play_with(composed_mafia(), judge)
    assert seen, "a composed step must reach the judge"
    first = seen[0]
    assert first.output.kind == "message", "one reader per call"
    assert first.where.slot == "ask"
    assert first.where.tag.startswith("compose:the debate:seat")
    assert first.output.max_words == 100, "the step's own limit is passed through"
    # One call per addressed seat, not one call for the table.
    seats = {c.where.tag.rsplit("seat", 1)[1] for c in seen}
    assert len(seats) > 1, "every addressed player is written to individually"


def test_a_composed_call_is_shown_only_its_own_reader():
    """The safety property. A composed reply is delivered, so its prompt is a
    channel: anything the model is shown, it can write out."""
    judge, seen = composer()
    _, game = play_with(composed_mafia(), judge)
    secret = {i: s.role for i, s in game.seats.items()}

    for call in seen:
        reader = int(call.where.tag.rsplit("seat", 1)[1])
        shown = {p["id"]: p["attributes"] for p in call.table["players"]}
        assert "role" in shown[reader], "a player may be told their own role"
        for other, attributes in shown.items():
            if other == reader:
                continue
            assert "role" not in attributes, (
                f"writing to {reader} was shown seat {other}'s role"
            )
            assert "faction" not in attributes
        # Belt and braces: the rendered prompt must not contain the words.
        from xcolos.flow.judge import prompt as user_prompt

        text = user_prompt(call)
        for other, role in secret.items():
            if other == reader or role == "villager":
                continue
            assert role not in text, (
                f"the prompt for {reader} named seat {other}'s role {role!r}"
            )


def test_a_composed_call_never_carries_the_whole_table():
    judge, seen = composer()
    play_with(composed_mafia(), judge)
    for call in seen:
        assert "record" not in call.table or call.table.get("learned") is not None, (
            "a composing call gets a seat view, not the referee's full sight"
        )


def test_a_message_marked_info_is_delivered_and_never_waited_for():
    """The point of typing a message: an `info` seat owes the game nothing."""
    silent = 2

    def compose(call):
        if call.output.kind != "message":
            return None
        seat = int(call.where.tag.rsplit("seat", 1)[1])
        if seat == silent:
            return {"type": "info", "text": f"Nothing is asked of you, seat {seat}."}
        return {"type": "action", "text": f"Seat {seat}, say your piece."}

    _, game = play_with(composed_mafia(), ScriptedJudge(compose))

    told = [
        f for f in game.facts
        if f.payload.get("composed") and sorted(f.entitled) == [silent]
    ]
    assert told, "the info seat must still receive its message"
    assert all("Nothing is asked of you" in f.payload["rendered"] for f in told)

    # The day still has a vote after the debate, so filter to the composed
    # step rather than to the phase.
    debated = [
        r for r in game.log.records
        if r.get("category") == "turn" and r.get("reason") == "ask:the debate"
    ]
    assert debated, "the other seats did debate"
    assert silent not in {r["seat"] for r in debated}, (
        f"seat {silent} was marked info and must not owe the game a turn"
    )


def test_an_unusable_dispatch_falls_back_to_asking_everyone():
    """A broken composer must not silently drop players out of the round."""
    expected, _ = play(seed=1)
    actual, _ = play_with(composed_mafia(), ScriptedJudge(lambda c: "nonsense"))
    assert (actual.winner, actual.rounds, actual.turns) == (
        expected.winner,
        expected.rounds,
        expected.turns,
    )


def test_composition_is_off_unless_the_step_asks_for_it():
    judge = ScriptedJudge(lambda c: None)
    play_with(json.loads((LIBRARY / "mafia_oracle.json").read_text(encoding="utf-8")), judge)
    assert not any(c.output.kind == "dispatch" for c in judge.asked), (
        "a template is free; a call has to be asked for"
    )


# ----------------------------------------------------------------------
# The roster requirement
# ----------------------------------------------------------------------


def test_a_roster_that_is_legal_field_by_field_can_still_be_unplayable():
    """The check the schema cannot do.

    Every field passing its own type and value test says nothing about the set.
    Four villagers and no mafia is a valid answer to every question the schema
    asks, and a game nobody can win.
    """
    from xcolos.flow.executor import _shortfall

    need = {"role": {"mafia": 1, "detective": 1}}
    fine = [{"role": "mafia"}, {"role": "detective"},
            {"role": "villager"}, {"role": "villager"}]
    assert _shortfall(need, fine) == ""
    assert _shortfall(need, {"table": {}, "players": fine}) == ""
    assert _shortfall({}, fine) == "", "no requirement, nothing to fail"

    for bad, expect in (
        ([{"role": "villager"}] * 4, "got 0"),
        ([{"role": "mafia"}] * 2 + [{"role": "detective"}, {"role": "villager"}], "got 2"),
        ("not a list", "no player records"),
    ):
        why = _shortfall(need, bad)
        assert why and expect in why, f"{bad!r} -> {why!r}"


def test_a_range_is_accepted_where_a_count_would_be_too_strict():
    from xcolos.flow.executor import _shortfall

    need = {"role": {"mafia": [1, 2]}}
    assert _shortfall(need, [{"role": "mafia"}]) == ""
    assert _shortfall(need, [{"role": "mafia"}] * 2) == ""
    assert "got 3" in _shortfall(need, [{"role": "mafia"}] * 3)


def test_a_rejected_roster_falls_back_rather_than_dealing_half_a_game():
    """A model that ignores the requirement must not produce a broken match."""
    definition = load(
        json.dumps(json.loads((LIBRARY / "mafia.json").read_text(encoding="utf-8"))),
        source="mafia",
    )
    # Always answers with a roster of villagers: every field legal, no mafia.
    # A reply that is legal field by field and still unplayable: every player
    # a villager, so nobody can ever win.
    judge = ScriptedJudge(
        lambda call: (
            {"each": {str(p): {"role": "villager", "faction": "good"}
                      for p in call.output.players}}
            if call.output.kind == "state" else None
        )
    )
    result, game = play_with(
        json.loads((LIBRARY / "mafia.json").read_text(encoding="utf-8")), judge
    )
    roles = [s.role for s in game.seats.values()]
    assert roles.count("mafia") == 1, (
        f"the declarative deal should have run instead; got {roles}"
    )
    rejected = [r for r in game.log.records if r.get("type") == "roster_rejected"]
    assert rejected, "and it should say why it fell back"
    assert "mafia" in rejected[0]["reason"]


def test_the_model_is_told_the_requirement_not_only_checked_against_it():
    from xcolos.flow.executor import _requirement_text

    text = _requirement_text({"role": {"mafia": 1, "detective": [1, 2]}})
    assert "exactly 1 player(s) with role = mafia" in text
    assert "between 1 and 2 player(s) with role = detective" in text
    assert _requirement_text({}) == ""


def test_a_spoken_answer_is_its_own_broadcast():
    """`broadcast: "others"` and nothing else, for a step that asks for text.

    A speech needs no template: the player's words are the message, and the
    engine has nothing to add. Anything else — a seat number, a choice — is not
    a sentence, so the game still has to say how it is announced.
    """
    from xcolos.games.definition import DefinitionError

    base = json.loads((LIBRARY / "mafia.json").read_text(encoding="utf-8"))
    debate = next(s for s in base["steps"] if s["label"] == "the debate")
    assert debate["broadcast"] == "others"
    # `text` now carries the step's own instruction to the speaker, which is a
    # different thing from how their answer is broadcast. The broadcast still
    # declares no wording, which is what makes it verbatim.
    assert "llm" not in debate

    _, game = play_with(base, None)
    spoken = [
        f for f in game.facts
        if f.type == "the_debate" and f.payload.get("value")
    ]
    assert spoken, "the debate was heard"
    for fact in spoken:
        assert fact.payload["rendered"] == str(fact.payload["value"]), (
            "a broadcast that rewords a player is the referee speaking for them"
        )
        assert fact.payload["seat"] not in fact.entitled, "not echoed to its author"

    # The same shortcut on an answer that is not a sentence is refused.
    broken = json.loads(json.dumps(base))
    next(s for s in broken["steps"] if s["label"] == "the vote")["broadcast"] = "others"
    try:
        load(json.dumps(broken), source="vote-verbatim")
    except DefinitionError as error:
        assert "not a message on its own" in str(error)
    else:
        raise AssertionError("a bare seat number is not a broadcast")


def test_a_worded_sync_says_only_what_the_seat_may_see():
    """`sync` sends state; with `llm` a model turns it into something readable.

    A raw JSON dump is accurate and close to unreadable, and an agent given one
    spends its attention parsing rather than playing. The prose is written per
    recipient from that recipient's view, so it cannot describe anything they
    do not already hold, and the structured state stays on the fact for
    anything that wants to read it as data.
    """
    judge = ScriptedJudge(
        lambda call: ({"type": "info", "text": f"Briefing for {call.where.tag}."}
                      if call.output.kind == "message" else None)
    )
    raw = json.loads((LIBRARY / "mafia.json").read_text(encoding="utf-8"))
    _, game = play_with(raw, judge)

    synced = [f for f in game.facts if f.type == "your_state"]
    assert len(synced) == len(game.seats), "one per player"
    secret = {i: s.role for i, s in game.seats.items()}
    for fact in synced:
        seat = sorted(fact.entitled)[0]
        assert len(fact.entitled) == 1, "a sync is private by construction"
        assert "state" in fact.payload, "the data survives alongside the prose"
        shown = {p["id"]: p["attributes"] for p in fact.payload["state"]["players"]}
        assert shown[seat], "a player sees their own attributes"
        for other, attributes in shown.items():
            if other != seat and secret[other] != "villager":
                assert not attributes, (
                    f"seat {seat}'s sync carried seat {other}'s state"
                )


def test_a_vote_names_both_outcomes_so_a_tie_cannot_be_forgotten():
    """Asking, reducing, applying and announcing are one act.

    They used to be a `poll` that bound a name and an `update` that read it
    back, with every operation guarded for the case where the tally chose
    nobody — and that guard *was* the tie handling, so a tied vote applied
    nothing and announced nothing. The table watched a vote happen and was
    told absolutely nothing. Naming both branches makes that unwriteable.
    """
    raw = json.loads((LIBRARY / "mafia_oracle.json").read_text(encoding="utf-8"))
    vote = next(s for s in raw["steps"] if s["label"] == "the vote")
    assert set(vote["outcome"]) == {"chosen", "none"}, "both outcomes named"
    assert not any(s["label"] == "the verdict" for s in raw["steps"]), (
        "the separate resolution step is gone"
    )

    # Two players, each the other's only legal target, so the vote is 1-1 and
    # the tally settles on nobody. Nothing else in the game can eliminate
    # anyone, so what the table hears is the tie and nothing else.
    tie = json.loads(json.dumps(raw))
    tie["steps"] = [s for s in tie["steps"]
                    if s["label"] in ("the vote", "after the vote")]
    tie["meta"]["players"]["min"] = 2
    tie["deal"]["by_players"]["2"] = [
        {"role": "mafia", "faction": "evil"},
        {"role": "villager", "faction": "good", "fill": True},
    ]
    _, game = play_with(tie, None, seats=2)
    announced = [f.payload["rendered"] for f in game.facts
                 if f.type.endswith("_result")]
    assert announced, "a tie must still tell the table something"
    assert all("tied" in line for line in announced)
    assert all(s.alive for s in game.seats.values()), "and eliminate nobody"


def test_a_decided_vote_eliminates_and_announces_in_one_step():
    result, game = play(seed=1)
    outcomes = [f for f in game.facts if f.type == "the_vote_result"]
    assert outcomes, "the vote announced its own outcome"
    for fact in outcomes:
        assert fact.entitled == frozenset(game.seats), "to the whole table"
        assert "voted out" in fact.payload["rendered"]
        # And the elimination happened, without a separate step to do it.
        assert not game.seats[fact.payload["result"]].alive


def test_who_is_out_is_announced_before_what_they_were():
    """An elimination is news; the reveal elaborates on it.

    `_settle` applied the branch's operations and announced afterwards, so a
    vote read "They were a villager." and only then "Seat 2 was voted out." —
    a reveal about nobody in particular, followed by the news it referred to.
    """
    _, game = play(seed=1)
    public = [f for f in game.facts
              if f.entitled == frozenset(game.seats) and f.payload.get("rendered")]
    order = [f.type for f in public]

    assert "the_vote_result" in order, "the vote announced its outcome"
    told = order.index("the_vote_result")
    reveal = next(i for i, t in enumerate(order) if t == "disclosed" and i > told)
    assert told < reveal, (
        f"the reveal came first: {order[max(0, told - 1):reveal + 1]}"
    )

    # Every elimination is announced to the whole table, by whichever step
    # made it: the night kill by `set_status`, the vote by its outcome.
    dead = {r["seat"] for r in game.log.records
            if r.get("category") == "state" and r.get("type") == "eliminate"}
    named = set()
    for fact in public:
        for seat in dead:
            if f"Seat {seat} " in fact.payload["rendered"]:
                named.add(seat)
    assert named == dead, f"eliminated {sorted(dead)}, announced {sorted(named)}"
