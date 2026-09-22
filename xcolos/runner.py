"""The turn loop.

One agent acts at a time. Sequence numbers are assigned by the kernel at
execution time, not by message arrival, so nothing depends on latency.

Delivery is eager: the moment a fact exists, every entitled seat is pushed a
SITUATION and told to wait. Only YOUR_TURN costs an inference call, which is
what keeps eager delivery affordable.

Every envelope out and every response back is logged, so the log alone explains
what each seat was told and what it said.
"""

from __future__ import annotations

import time
from dataclasses import dataclass

from xcolos.game import Game, RunStatus
from xcolos.host import HostUnavailable, Registry
from xcolos.log import MoveRecord
from xcolos.orchestrators.base import ActionRequest, Orchestrator
from xcolos.protocol import Action, ActionInvalid, Envelope, MsgType, validate
from xcolos.render import render_briefing, render_facts, render_turn

MAX_REPAIR_ATTEMPTS = 2


@dataclass
class ParkedTurn:
    """A turn waiting on a seat that pulls rather than being pushed to.

    The server still decides whose turn it is and when it expires. It simply
    holds no open call while it waits, because a connector seat answers at
    conversation pace and a blocked thread for minutes is waste.
    """

    request: ActionRequest
    envelope: Envelope
    record: MoveRecord
    expires_at: float
    opened_at: float

    @property
    def seconds_left(self) -> float:
        return max(0.0, self.expires_at - time.monotonic())


@dataclass
class MatchResult:
    match_id: str
    status: str
    winner: str | None
    reason: str | None
    turns: int
    rounds: int
    degraded_turns: int


class Runner:
    def __init__(
        self,
        game: Game,
        orchestrator: Orchestrator,
        registry: Registry,
        max_turns: int = 400,
        max_degraded_streak: int = 8,
        deadline_ms: int | None = None,
    ) -> None:
        self.game = game
        self.orchestrator = orchestrator
        #: Which client speaks for which seat. The server never holds an agent.
        self.registry = registry
        self.max_turns = max_turns
        self.max_degraded_streak = max_degraded_streak
        #: Overrides what the orchestrator asked for. How long a seat may take
        #: is an operator's concern, not a game rule.
        self.deadline_ms = deadline_ms
        self.degraded_turns = 0

        # Turn driving. A pull seat parks here instead of blocking a thread.
        self.parked: ParkedTurn | None = None
        self.result: MatchResult | None = None
        self._play = None
        self._request: ActionRequest | None = None
        self._concluded = False
        #: Briefings for pull seats, which are read rather than pushed.
        self.briefings: dict[int, str] = {}

    # ------------------------------------------------------------------

    def run(self) -> MatchResult:
        """Play to the end. Only valid when every seat is a push seat."""
        self.start()
        if self.result is None:
            raise RuntimeError(
                "the match parked on a pull seat; drive it with submit() instead"
            )
        return self.result

    # ------------------------------------------------------------------
    # Driving
    # ------------------------------------------------------------------

    def start(self) -> None:
        game = self.game
        self.orchestrator.setup(game)
        game.status = RunStatus.RUNNING
        game.log.record(
            "process", "start", game_id=self.orchestrator.game_id, seed=game.seed
        )
        self._greet()
        self._flush()

        self._play = self.orchestrator.play(game)
        try:
            self._request = next(self._play)
        except StopIteration:
            self._request = None
        self._pump()

    def _pump(self) -> None:
        """Advance until a pull seat is due, or the match is over."""
        game = self.game
        while self._request is not None and game.status is RunStatus.RUNNING:
            if game.turn_seq >= self.max_turns:
                game.abandon(f"turn cap of {self.max_turns} reached")
                break
            if self._is_pull(self._request.seat):
                self._park(self._request)
                return
            self._resume(self._take_turn(self._request))
            if game.status is not RunStatus.RUNNING:
                break
        self._conclude()

    def _resume(self, action: Action) -> None:
        self._flush()
        if self.game.status is not RunStatus.RUNNING:
            self._request = None
            return
        try:
            self._request = self._play.send(action)
        except StopIteration:
            self._request = None

    def _conclude(self) -> None:
        if self._concluded:
            return
        self._concluded = True
        self._farewell()
        self.result = self._result()

    def _is_pull(self, seat: int) -> bool:
        return getattr(self.registry.host_of.get(seat), "pull", False)

    def _park(self, request: ActionRequest) -> None:
        envelope, record = self._open_turn(request)
        ms = self.deadline_ms or request.deadline_ms or 30_000
        now = time.monotonic()
        self.parked = ParkedTurn(
            request=request,
            envelope=envelope,
            record=record,
            expires_at=now + ms / 1000,
            opened_at=now,
        )
        # Offered, not delivered: nobody has fetched it yet. The distinction is
        # the whole point of a pull transport.
        self.game.log.record(
            "message",
            "offered",
            seat=request.seat,
            msg_type=envelope.type.value,
            body=envelope.body,
            action_schema=request.schema.id,
            legal_targets=list(request.legal_targets),
            deadline_ms=ms,
        )

    def submit(self, seat: int, action: Action | None) -> tuple[bool, str]:
        """Take one action from a pull seat. Returns accepted, and why not."""
        parked = self.parked
        if parked is None:
            return False, "nothing is owed right now"
        if parked.request.seat != seat:
            return False, f"it is seat {parked.request.seat}'s turn, not yours"
        if self.expire_if_due():
            return False, "that turn had already expired"

        if action is None:
            return False, "no action was supplied"
        try:
            checked = validate(action, parked.request.schema, parked.request.legal_targets)
        except ActionInvalid as exc:
            # The turn stays parked. A refusal is information, not a failure,
            # and the caller can simply answer again.
            parked.record.attempts.append(
                {"n": len(parked.record.attempts) + 1, "outcome": "invalid",
                 "error": str(exc)}
            )
            self.game.log.record(
                "message", "from_agent", seat=seat,
                response=action.to_json(), rejected=str(exc),
            )
            return False, str(exc)

        parked.record.attempts.append(
            {"n": len(parked.record.attempts) + 1, "outcome": "ok"}
        )
        parked.record.final_outcome = (
            "ok" if len(parked.record.attempts) == 1 else "repaired"
        )
        self.game.seats[seat].degraded_streak = 0
        self.game.log.record(
            "message", "from_agent", seat=seat, response=checked.to_json()
        )

        self.parked = None
        self._close_turn(parked.record, checked)
        self._resume(checked)
        self._pump()
        return True, "accepted"

    def expire_if_due(self) -> bool:
        """Apply the default if a parked turn has run out of time.

        Checked lazily, on any call that touches the match. A server that never
        calls out has no other moment to notice.
        """
        parked = self.parked
        if parked is None or parked.seconds_left > 0:
            return False

        self.game.log.record(
            "message", "expired", seat=parked.request.seat,
            after_s=round(time.monotonic() - parked.opened_at, 1),
        )
        action = self._default_action(parked.request, parked.record)
        self.parked = None
        self._close_turn(parked.record, action)
        self._resume(action)
        self._pump()
        return True

    # ------------------------------------------------------------------
    # Messaging
    # ------------------------------------------------------------------

    def _send(self, envelope: Envelope) -> Action | None:
        """Hand one envelope to the client that owns the seat, and record both
        directions.

        A client that is unreachable is not a special case. It looks like a seat
        that did not answer, which the failure ladder already handles.
        """
        self.game.log.record(
            "message",
            "to_agent",
            seat=envelope.seat,
            msg_type=envelope.type.value,
            body=envelope.body,
            action_schema=envelope.schema.id if envelope.schema else None,
            legal_targets=list(envelope.legal_targets),
        )
        try:
            response = self.registry.deliver(envelope)
        except HostUnavailable as exc:
            self.game.log.record(
                "message", "host_unavailable", seat=envelope.seat, error=str(exc)
            )
            raise

        if envelope.type is MsgType.YOUR_TURN:
            self.game.log.record(
                "message",
                "from_agent",
                seat=envelope.seat,
                response=response.to_json() if response else None,
            )
        return response

    def _tell(self, envelope: Envelope) -> None:
        """Send something that needs no answer. An unreachable client is fine."""
        try:
            self._send(envelope)
        except HostUnavailable:
            pass

    def _greet(self) -> None:
        """Brief every seat, once, before the first round.

        The briefing absorbs each seat's pending setup facts rather than letting
        them arrive separately afterwards. A seat learns its role as part of
        being told the rules, which is one message doing one job.
        """
        game = self.game
        brief = self.orchestrator.brief(game)
        for seat in self.registry.seats():
            pending = game.undelivered(seat)
            body = render_briefing(game.seat_view(seat), pending, brief)
            if self._is_pull(seat):
                # Held for the agent to read. Marking it delivered here would
                # acknowledge on its behalf, which is exactly what the ack
                # cursor exists to prevent.
                self.briefings[seat] = body
                continue
            game.mark_delivered(seat, pending)
            self._tell(
                Envelope(
                    type=MsgType.GAME_START,
                    match_id=game.match_id,
                    seat=seat,
                    body=body,
                )
            )

    def _farewell(self) -> None:
        game = self.game
        self._flush()
        for seat in self.registry.seats():
            if self._is_pull(seat):
                continue
            self._tell(
                Envelope(
                    type=MsgType.GAME_END,
                    match_id=game.match_id,
                    seat=seat,
                    body=f"Game over. Winner: {game.winner}. {game.reason or ''}".strip(),
                )
            )

    def _flush(self) -> None:
        """Push every undelivered entitled fact to its audience.

        A SITUATION requires no inference, so telling everyone what happened the
        moment it happens costs nothing.
        """
        game = self.game
        for seat in sorted(game.seats):
            if self._is_pull(seat):
                continue  # it reads its own state, on its own cadence
            pending = game.undelivered(seat)
            game.mark_delivered(seat, pending)
            if not pending:
                continue
            self._tell(
                Envelope(
                    type=MsgType.SITUATION,
                    match_id=game.match_id,
                    seat=seat,
                    body=render_facts(game.seat_view(seat), pending),
                )
            )

    # ------------------------------------------------------------------
    # Turns
    # ------------------------------------------------------------------

    def _open_turn(self, request: ActionRequest):
        """Everything up to asking. Shared by both transports."""
        game = self.game
        game.turn_seq += 1
        seat = game.seats[request.seat]

        game.log.record(
            "orchestrator",
            "action_request",
            seat=request.seat,
            action_schema=request.schema.id,
            legal_targets=list(request.legal_targets),
            reason=request.reason,
            prompt=request.prompt,
        )

        pending = game.undelivered(request.seat)
        record = MoveRecord(
            turn_seq=game.turn_seq,
            seat=request.seat,
            role=seat.role,
            delta_fact_seqs=[f.seq for f in pending],
            action_schema=request.schema.id,
            legal_targets=list(request.legal_targets),
            reason=request.reason,
        )
        if not self._is_pull(request.seat):
            game.mark_delivered(request.seat, pending)

        envelope = Envelope(
            type=MsgType.YOUR_TURN,
            match_id=game.match_id,
            seat=request.seat,
            body=render_turn(
                game.seat_view(request.seat),
                pending,
                request.schema,
                request.legal_targets,
                request.prompt,
            ),
            turn_seq=game.turn_seq,
            schema=request.schema,
            legal_targets=request.legal_targets,
            deadline_ms=self.deadline_ms or request.deadline_ms,
        )

        return envelope, record

    def _close_turn(self, record: MoveRecord, action: Action) -> Action:
        record.action = action.to_json()
        record.rng_state_after = self.game.rng.digest()
        self.game.log.record("turn", "move", **record.to_fields())
        return action

    def _take_turn(self, request: ActionRequest) -> Action:
        """Ask a push seat and wait. Used for in-process clients only."""
        envelope, record = self._open_turn(request)
        return self._close_turn(record, self._ladder(envelope, request, record))

    def _ladder(
        self, envelope: Envelope, request: ActionRequest, record: MoveRecord
    ) -> Action:
        """Validate, repair, retry, then fall back to the declared default.

        A match never stalls on a bad response. Every attempt is recorded, so a
        seat that played badly is distinguishable from one that could not
        produce valid output at all.
        """
        env = envelope

        for attempt in range(1, MAX_REPAIR_ATTEMPTS + 2):
            try:
                raw = self._send(env)
                if raw is None:
                    raise ActionInvalid("no response")
                action = validate(raw, request.schema, request.legal_targets)
            except HostUnavailable as exc:
                # Not a wrong answer, so repeating the question is pointless and
                # costs another full deadline. Fall through to the default.
                record.attempts.append(
                    {"n": attempt, "outcome": "unreachable", "error": str(exc)}
                )
                break
            except ActionInvalid as exc:
                record.attempts.append(
                    {"n": attempt, "outcome": "invalid", "error": str(exc)}
                )
                if attempt > MAX_REPAIR_ATTEMPTS:
                    break
                # A distinct type, not another YOUR_TURN, so neither the agent
                # nor the log can mistake a retry for a fresh turn. The body
                # carries the validation error and nothing else, so it can
                # never echo state this seat is not entitled to.
                env = Envelope(
                    type=MsgType.ACTION_REJECTED,
                    match_id=env.match_id,
                    seat=env.seat,
                    body=f"That answer was not legal: {exc}. Answer again.",
                    turn_seq=env.turn_seq,
                    schema=env.schema,
                    legal_targets=env.legal_targets,
                    deadline_ms=env.deadline_ms,
                )
                continue

            record.attempts.append({"n": attempt, "outcome": "ok"})
            record.final_outcome = "ok" if attempt == 1 else "repaired"
            self.game.seats[request.seat].degraded_streak = 0
            return action

        return self._default_action(request, record)

    def _default_action(self, request: ActionRequest, record: MoveRecord) -> Action:
        game = self.game
        schema = request.schema
        record.final_outcome = "defaulted"
        record.degraded = True
        self.degraded_turns += 1

        seat = game.seats[request.seat]
        seat.degraded_streak += 1
        if seat.degraded_streak >= self.max_degraded_streak:
            game.abandon(
                f"seat {seat.index} failed {seat.degraded_streak} turns in a row"
            )

        if schema.target == "text":
            return Action(type=schema.id, text="(no answer)")
        if schema.default == "random" and request.legal_targets:
            # Drawn from the seeded PRNG at a point fixed by turn order, so the
            # fallback is reproducible rather than latency-ordered.
            return Action(
                type=schema.id, target=game.rng.choice(list(request.legal_targets))
            )
        if request.legal_targets:
            return Action(type=schema.id, target=request.legal_targets[0])
        return Action(type=schema.id)

    # ------------------------------------------------------------------

    def _result(self) -> MatchResult:
        game = self.game
        game.log.record(
            "result",
            "summary",
            status=game.status.value,
            winner=game.winner,
            reason=game.reason,
            turns=game.turn_seq,
            rounds=game.round,
            degraded_turns=self.degraded_turns,
            facts=len(game.facts),
            identity=game.identity,
            # String keys: JSON has no integer keys, and a log that does not
            # survive a round trip through its own file is not a record.
            roles={str(i): s.role for i, s in sorted(game.seats.items())},
        )
        game.log.close()
        return MatchResult(
            match_id=game.match_id,
            status=game.status.value,
            winner=game.winner,
            reason=game.reason,
            turns=game.turn_seq,
            rounds=game.round,
            degraded_turns=self.degraded_turns,
        )
