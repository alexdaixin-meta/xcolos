"""The game tools an agent calls.

The server keeps each player's state. When it becomes a seat's turn, the server
writes the message into that seat's state and waits. The agent reads its own
state from its own end, and posts an action when one is owed.

Four tools, and only two of them are used during play:

    tables()                  where can I sit
    take_seat(code)           bind this session to a seat
    read_state(token, ack)    what do I know, and is it my turn
    post_action(token, ans)   here is my answer

`read_state` never blocks. A tool call that hangs for minutes inside someone's
chat session is a bad citizen, so it returns immediately with either "not yet"
and a suggested interval, or the turn.
"""

from __future__ import annotations

import secrets
from dataclasses import dataclass, field
from typing import Any, Callable

from xcolos.game import Game, RunStatus
from xcolos.host import Registry
from xcolos.identity import AccessDenied, Player
from xcolos.protocol import Action
from xcolos.render import render_facts
from xcolos.runner import Runner

#: How often an agent should come back when nothing is owed. Deliberately a
#: range rather than a number: a session should not hammer, and the exact
#: cadence is the operator's to tune.
DEFAULT_POLL_SECONDS = 8
MIN_POLL_SECONDS = 2
MAX_POLL_SECONDS = 120


@dataclass
class SeatToken:
    """What an agent holds. One opaque string, easy to paste by hand."""

    token: str
    seat: int
    player_id: str

    @staticmethod
    def issue(seat: int, player_id: str) -> "SeatToken":
        return SeatToken(f"xcs_{secrets.token_hex(10)}", seat, player_id)


@dataclass
class OpenSeat:
    """One seat, and the private address that is it.

    The key is the whole credential. An agent that has the URL is the seat, and
    an agent that does not cannot reach it. That collapses taking a seat and
    playing it into the same two calls, which matters when the instructions
    have to fit in something a person pastes into a chat.
    """

    seat: int
    name: str
    #: The player id. Unique, unguessable, and the whole credential. One
    #: endpoint serves any number of these, so players are unlimited without
    #: anything being registered in advance.
    key: str = field(default_factory=lambda: "pl_" + secrets.token_urlsafe(12))
    taken: bool = False
    player_id: str = ""


class TableTools:
    """The tool surface for one match."""

    def __init__(
        self,
        game: Game,
        runner: Runner,
        registry: Registry,
        poll_seconds: int = DEFAULT_POLL_SECONDS,
        on_ready: Callable[[], None] | None = None,
    ) -> None:
        self.game = game
        self.runner = runner
        self.registry = registry
        self.poll_seconds = max(MIN_POLL_SECONDS, min(poll_seconds, MAX_POLL_SECONDS))
        self.open_seats: dict[str, OpenSeat] = {}
        self.tokens: dict[str, SeatToken] = {}
        #: Called once every offered seat has been claimed. The table cannot
        #: start until the sessions that will play it are actually attached.
        self.on_ready = on_ready

    # ------------------------------------------------------------------
    # Linking
    # ------------------------------------------------------------------

    def offer(self, seat: int, name: str) -> OpenSeat:
        """Give a seat its own address. Whoever holds it plays that seat."""
        slot = OpenSeat(seat=seat, name=name)
        self.open_seats[slot.key] = slot
        return slot

    def slot_of(self, seat: int) -> OpenSeat | None:
        return next((s for s in self.open_seats.values() if s.seat == seat), None)

    def summary(self) -> dict[str, Any]:
        return {
            "match_id": self.game.match_id,
            "game": self.game.game_id,
            "seats": len(self.game.seats),
            "status": self.game.status.value,
            "open_seats": [
                {
                    "seat": s.seat,
                    "name": s.name,
                    "player_id": s.key,
                    "taken": s.taken,
                }
                for s in self.open_seats.values()
            ],
            "connected": [self.presence(s.seat) for s in self.open_seats.values()],
        }

    def presence(self, seat: int) -> dict[str, Any]:
        """Whether a session is attached to this seat and still working.

        Four states, because they mean different things to whoever is watching:

        ``open``        nobody has called this seat's address
        ``connecting``  something called once; not yet proof of a loop
        ``connected``   it acknowledged, or it is calling repeatedly
        ``stalled``     it was here and has stopped calling

        Acknowledging is the strong signal. Anything can fetch a URL once; a
        session that confirms what it read has actually taken it in. Repeated
        calls are the weaker signal that covers the stretch before the game
        starts, when there is nothing yet to acknowledge.
        """
        from datetime import datetime, timezone

        slot = self.slot_of(seat)
        st = self.game.seats.get(seat)
        reads = st.reads if st else 0
        acked = bool(st and st.acked_upto > 0)

        last, since = (st.last_read_at if st else ""), None
        if last:
            try:
                delta = datetime.now(timezone.utc) - datetime.fromisoformat(last)
                since = round(delta.total_seconds(), 1)
            except ValueError:
                since = None

        # Still polling, judged against the cadence we asked it to keep.
        live = since is not None and since < self.poll_seconds * 3

        if reads == 0:
            state = "open"
        elif not live:
            state = "stalled"
        elif acked or reads >= 2:
            state = "connected"
        else:
            state = "connecting"

        return {
            "seat": seat,
            "name": slot.name if slot else (st.name if st else ""),
            "player_id": slot.key if slot else "",
            "state": state,
            "claimed": bool(slot and slot.taken),
            "acked": acked,
            "polling": live and reads >= 2,
            "live": live,
            "reads": reads,
            "last_read_at": last,
            "seconds_since_read": since,
        }

    def _claim(self, slot: OpenSeat, player_name: str) -> None:
        """First touch takes the seat. There is no separate joining step."""
        if slot.taken:
            return
        player = Player.new(player_name or slot.name)
        slot.taken = True
        slot.player_id = player.player_id

        token = SeatToken(slot.key, slot.seat, player.player_id)
        self.tokens[slot.key] = token
        self.registry.ownership.enrol(player)
        self.registry.ownership.claim(slot.seat, player.player_id, slot.key)
        self.game.log.record(
            "setup",
            "seat_claimed",
            seat=slot.seat,
            player=player.player_id,
            display_name=player_name or slot.name,
        )

        if not [s for s in self.open_seats.values() if not s.taken]:
            if self.on_ready is not None:
                self.on_ready()

    # ------------------------------------------------------------------
    # Play
    # ------------------------------------------------------------------

    def _resolve(self, key: str, player_name: str = "") -> OpenSeat:
        slot = self.open_seats.get((key or "").strip())
        if slot is None:
            raise AccessDenied("no seat lives at that address")
        self._claim(slot, player_name)
        return slot

    def read_state(
        self,
        seat_token: str,
        ack_through: int | None = None,
        player_name: str = "",
    ) -> dict[str, Any]:
        """This seat's whole world, and whether it owes an action.

        Self-contained on purpose. The standing state is sent every time, not
        just what is new, because an assistant's context is shared with
        everything else its owner is doing and it will lose the thread. A few
        hundred extra tokens removes a whole class of failure.
        """
        slot = self._resolve(seat_token, player_name)
        seat = slot.seat
        game = self.game

        if game.status is RunStatus.SETUP:
            # Seated, but the table is not full yet. Keep pulling: the game
            # begins the moment the last seat is claimed, and an agent that
            # stopped checking would miss its own first turn.
            game.record_read(seat, [])
            waiting = [s.name for s in self.open_seats.values() if not s.taken]
            full = not waiting
            return {
                "you": {"seat": seat, "status": "seated"},
                "table": {
                    "match_id": game.match_id,
                    "status": "ready_to_start" if full else "waiting_for_players",
                    "waiting_for": waiting,
                },
                "new_for_you": [],
                "ack_through": None,
                "your_turn": False,
                "check_back_in_seconds": self.poll_seconds,
                "note": (
                    "Everyone is seated. Waiting for the table to be started."
                    if full
                    else "The table is not full yet."
                ) + " Keep calling on this cadence so you do not miss your first turn.",
            }

        # Confirm first, so the agent stops seeing what it has already taken in.
        game.ack(seat, ack_through)
        # Any call is a chance to notice a turn ran out; nothing else will.
        self.runner.expire_if_due()

        unacked = game.unacked(seat)
        game.record_read(seat, unacked)
        view = game.seat_view(seat)

        parked = self.runner.parked
        mine = parked is not None and parked.request.seat == seat

        state: dict[str, Any] = {
            "you": {
                "seat": seat,
                "name": view["you"]["name"],
                "role": view["you"]["role"],
                "faction": view["you"]["faction"],
                "status": view["you"]["status"],
            },
            "table": {
                "match_id": game.match_id,
                "status": game.status.value,
                "round": game.round,
                "phase": game.phase,
                "living_seats": game.active_seats(),
                "seats": [
                    {"seat": s["index"], "name": s["name"], "status": s["status"]}
                    for s in view["seats"]
                ],
            },
            "new_for_you": [
                {
                    "fact_seq": f.seq,
                    "round": f.round,
                    "text": render_facts(view, [f]),
                }
                for f in unacked
            ],
            "ack_through": (unacked[-1].seq if unacked else None),
            "your_turn": mine,
            "check_back_in_seconds": self.poll_seconds,
        }

        # Until this seat confirms anything, it has not read its briefing.
        # Repeating it costs little and covers a session that dropped it.
        if game.seats[seat].acked_upto == 0 and seat in self.runner.briefings:
            state["briefing"] = self.runner.briefings[seat]

        if mine:
            assert parked is not None
            state["ask"] = {
                "action": parked.request.schema.id,
                "prompt": parked.request.prompt,
                "answer_with": parked.request.schema.target,
                "legal_answers": list(parked.request.legal_targets),
                "seconds_left": round(parked.seconds_left, 1),
            }
            # A turn is owed, so come back promptly rather than on the idle
            # cadence. The deadline is the thing that matters now.
            state["check_back_in_seconds"] = MIN_POLL_SECONDS
        elif game.status is not RunStatus.RUNNING:
            state["outcome"] = {"winner": game.winner, "reason": game.reason}
            state["check_back_in_seconds"] = 0

        return state

    def post_action(self, seat_token: str, answer: Any) -> dict[str, Any]:
        """Submit this seat's action. Refusal is information, not an error."""
        seat = self._resolve(seat_token).seat

        self.runner.expire_if_due()
        parked = self.runner.parked
        if parked is None or parked.request.seat != seat:
            return {
                "accepted": False,
                "reason": "nothing is owed from you right now",
                "check_back_in_seconds": self.poll_seconds,
            }

        schema = parked.request.schema
        action = (
            Action(type=schema.id, text=str(answer))
            if schema.target == "text"
            else Action(type=schema.id, target=_coerce(answer, parked.request.legal_targets))
        )

        accepted, reason = self.runner.submit(seat, action)
        out: dict[str, Any] = {"accepted": accepted, "reason": reason}
        if not accepted:
            # Still owed, so say what would be accepted rather than making the
            # agent call read_state to find out.
            still = self.runner.parked
            if still is not None and still.request.seat == seat:
                out["legal_answers"] = list(still.request.legal_targets)
                out["answer_with"] = still.request.schema.target
                out["seconds_left"] = round(still.seconds_left, 1)
        out["check_back_in_seconds"] = self.poll_seconds
        return out


    # ------------------------------------------------------------------
    # The one call
    # ------------------------------------------------------------------

    def play(
        self,
        player_id: str,
        ack_through: int | None = None,
        answer: Any = None,
        player_name: str = "",
    ) -> dict[str, Any]:
        """Read, and act in the same breath if an answer was supplied.

        One endpoint, one request shape, any number of players. An agent's
        whole loop is this call repeated: send nothing to look, send an answer
        when a turn is owed, and read the state that comes back either way.
        """
        self._resolve(player_id, player_name)
        acted = None
        if answer is not None and answer != "":
            acted = self.post_action(player_id, answer)
        state = self.read_state(player_id, ack_through, player_name)
        if acted is not None:
            state["action_result"] = acted
        return state


def _coerce(answer: Any, legal: tuple[Any, ...]) -> Any:
    """Read a seat number out of whatever the agent sent."""
    if legal and isinstance(legal[0], int):
        import re

        found = re.findall(r"-?\d+", str(answer))
        if found:
            return int(found[-1])
    return answer


# ----------------------------------------------------------------------
# The invitation
# ----------------------------------------------------------------------


INVITE = """# You are playing XColos, seat {seat} at table {match_id}

You are a player in a hidden-role social deduction game. Play to win. You know
only what the game tells you, and the other players are told different things.

## Your one command

```bash
curl -sS {url} -H 'Content-Type: application/json' -d '{{"id":"{pid}"}}'
```

`{pid}` is you. Anyone who has it is you, so do not share it and do not paste it
anywhere public.

That single call is the whole interface. Send it with nothing else to look at
the table. Send it with an `answer` to act. You get the current state back
either way.

```bash
# confirm what you have read, and answer this turn, in one go
curl -sS {url} -H 'Content-Type: application/json' -d '{{"id":"{pid}","ack":17,"answer":3}}'
```

## What comes back

| Field | Meaning |
|---|---|
| `you`, `table` | Your role and the state of play. Sent every time |
| `new_for_you` | What has happened since you last confirmed |
| `ack_through` | Send this back as `ack` next time to confirm you read it |
| `your_turn` | Whether the game is waiting on you right now |
| `ask` | What to answer, and which answers are legal |
| `check_back_in_seconds` | How long to wait before calling again |
| `action_result` | Whether your answer was accepted, if you sent one |

## What to do now

1. Call it straight away. **The table may not be full yet, and that is fine.**
   Play begins the moment the last seat is taken, and a session that waited to
   be told would miss its own first turn.
2. Keep calling on the cadence the response asks for, roughly every {poll}
   seconds.
3. Whenever `your_turn` is true, decide and answer before `ask.seconds_left`
   runs out. If you are late the game answers for you, badly.
4. Stop when `table.status` is no longer `running`. The result is in `outcome`.

## Playing well

- Send `ack` every time, or you will keep re-reading the same news.
- Answer with a seat number when `ask.answer_with` is `seat`, or a sentence
  when it is `text`. Only values in `ask.legal_answers` are accepted.
- A refused answer leaves the turn open. Read the reason and answer again.
- You may deceive other players. It is that kind of game. But you can only
  reason from what you were actually told; there is no other source.
- When you speak, say something that does work. The others read it and remember.

Begin by making that call.
"""


#: The one endpoint every player uses.
PLAY_PATH = "/api/play"


def invite_text(
    base_url: str,
    match_id: str,
    seat: int,
    player_id: str,
    poll_seconds: int = DEFAULT_POLL_SECONDS,
) -> str:
    """The block a player pastes into their own assistant session."""
    return INVITE.format(
        url=f"{base_url.rstrip('/')}{PLAY_PATH}",
        pid=player_id,
        match_id=match_id,
        seat=seat,
        poll=poll_seconds,
    )
