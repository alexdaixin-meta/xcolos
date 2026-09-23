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
import threading
from dataclasses import dataclass, field
from typing import Any, Callable

from xcolos.game import Game, RunStatus
from xcolos.host import Registry
from xcolos import messages
from xcolos.identity import AccessDenied, Player
from xcolos.protocol import Action
from xcolos.render import render_facts
from xcolos.runner import Runner

#: How often an agent should come back. Cheap either way, because a read with
#: nothing to report is a few dozen bytes, but two seconds halves the traffic
#: without the table feeling any slower at conversation pace.
DEFAULT_POLL_SECONDS = 2
MIN_POLL_SECONDS = 1
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
        game: Game | None,
        runner: Runner | None,
        registry: Registry | None,
        poll_seconds: int = DEFAULT_POLL_SECONDS,
        on_ready: Callable[[], None] | None = None,
    ) -> None:
        self.game = game
        self.runner = runner
        self.registry = registry
        self.poll_seconds = max(MIN_POLL_SECONDS, min(poll_seconds, MAX_POLL_SECONDS))
        self.open_seats: dict[str, OpenSeat] = {}
        self.tokens: dict[str, SeatToken] = {}
        #: One table, one lock. Simultaneous voting means several agents post
        #: at the same instant from different HTTP threads, and the game state
        #: they all advance is plain mutable Python. Without this, two seats
        #: answering together could take the same turn number.
        #:
        #: Reentrant because `play` calls the other two.
        self._lock = threading.RLock()
        #: Called once every offered seat has been claimed. The table cannot
        #: start until the sessions that will play it are actually attached.
        self.on_ready = on_ready

    # ------------------------------------------------------------------
    # Linking
    # ------------------------------------------------------------------

    def retarget(self, game: Game, runner: Runner, registry: Registry) -> None:
        """Point at a new game on the same table.

        Seats, player ids and who is connected all survive, because they belong
        to the table. Everything about the previous game does not.
        """
        self.game = game
        self.runner = runner
        self.registry = registry
        for slot in self.open_seats.values():
            if slot.taken and slot.player_id:
                # Re-establish ownership against the new game's registry so a
                # connected agent keeps playing without re-pasting anything.
                registry.ownership.enrol(
                    Player(player_id=slot.player_id, display_name=slot.name)
                )
                registry.ownership.claim(slot.seat, slot.player_id, slot.key)

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
        full: bool = False,
    ) -> dict[str, Any]:
        """What is new for this seat, and whether it owes an action.

        Incremental on purpose. The agent keeps its own context, so re-sending
        the role and the whole table on every poll would be waste, and at a
        one second cadence it would be a lot of waste. A read with nothing to
        report is a few dozen bytes.

        The standing state goes out when it is genuinely needed: on the first
        read, when the match ends, and whenever the caller asks for `full`.
        That last one is the recovery path for a session that lost the thread.
        """
        with self._lock:
            return self._read_state(seat_token, ack_through, player_name, full)

    def _read_state(
        self,
        seat_token: str,
        ack_through: int | None,
        player_name: str,
        full: bool,
    ) -> dict[str, Any]:
        slot = self._resolve(seat_token, player_name)
        seat = slot.seat
        game = self.game

        if game.status is RunStatus.SETUP:
            game.record_read(seat, [])
            waiting = [s.name for s in self.open_seats.values() if not s.taken]
            return {
                "new": False,
                "status": "ready_to_start" if not waiting else "waiting_for_players",
                # Carried by every response, this one included, so an agent can
                # tell one game from the next without a special case.
                "game": game.match_id,
                "waiting_for": waiting,
                "check_back_in_seconds": self.poll_seconds,
            }

        # Confirm first, so the agent stops being shown what it has taken in.
        game.ack(seat, ack_through)
        # Any call is a chance to notice a turn ran out; nothing else will.
        self.runner.expire_if_due()

        unacked = game.unacked(seat)
        parked = self.runner.parked_for(seat)
        mine = parked is not None
        over = game.status is not RunStatus.RUNNING
        first = game.seats[seat].acked_upto == 0

        game.record_read(seat, unacked)

        if not (unacked or mine or over or full or first):
            # Nothing happened. Say so in as few bytes as possible.
            return {
                "new": False,
                "status": "running",
                "game": game.match_id,
                "check_back_in_seconds": self.poll_seconds,
            }

        view = game.seat_view(seat)
        state: dict[str, Any] = {
            "new": True,
            "status": game.status.value,
            # Changes when a table starts another game. An agent that sees a
            # new value should treat its history as belonging to the old one.
            "game": game.match_id,
            "at": {"round": game.round, "phase": game.phase},
            # The queue. Every item says what kind of message it is, so an
            # agent can branch on structure rather than parse prose.
            "messages": [
                messages.information(
                    seq=f.seq,
                    type=f.type,
                    round=f.round,
                    phase=f.phase,
                    text=render_facts(view, [f]),
                    data=f.payload,
                )
                for f in unacked
            ],
            "ack_through": (unacked[-1].seq if unacked else None),
            "your_turn": mine,
            "check_back_in_seconds": self.poll_seconds,
        }

        if first or full or over:
            # Who you are and who is at the table. Sent when a session is new,
            # when it asks to resync, and once at the end.
            state["you"] = {
                "seat": seat,
                "name": view["you"]["name"],
                "role": view["you"]["role"],
                "faction": view["you"]["faction"],
                "status": view["you"]["status"],
            }
            state["table"] = {
                "match_id": game.match_id,
                "living_seats": game.active_seats(),
                "seats": [
                    {"seat": o["index"], "name": o["name"], "status": o["status"]}
                    for o in view["seats"]
                ],
            }
        if first and seat in self.runner.briefings:
            state["briefing"] = self.runner.briefings[seat]

        if mine:
            assert parked is not None
            ask = messages.action_required(
                action=parked.request.schema.id,
                prompt=parked.request.prompt,
                answer_with=parked.request.schema.target,
                legal_answers=list(parked.request.legal_targets),
                seconds_left=round(parked.seconds_left, 1),
                max_words=parked.request.schema.max_words,
            )
            # The request sits at the end of the queue, because that is where
            # it belongs in time, and is repeated at the top level because it
            # is the one item an agent must not miss. It carries no `seq`: an
            # acknowledgement would say "received", and a turn needs an answer.
            state["messages"].append(ask)
            state["ask"] = ask
        if over:
            state["outcome"] = {"winner": game.winner, "reason": game.reason}
            state["check_back_in_seconds"] = 0

        return state

    def post_action(self, seat_token: str, answer: Any) -> dict[str, Any]:
        with self._lock:
            return self._post_action(seat_token, answer)

    def _post_action(self, seat_token: str, answer: Any) -> dict[str, Any]:
        """Submit this seat's action. Refusal is information, not an error."""
        seat = self._resolve(seat_token).seat

        # Whichever turn the caller believed it was answering, captured before
        # expiry runs. Expiry can default that turn, advance the game and park
        # a different one on the same seat; a sentence meant as speech would
        # then be read for its trailing number and cast as a vote.
        intended = self.runner.parked_for(seat)
        self.runner.expire_if_due()
        parked = self.runner.parked_for(seat)
        if intended is not None and parked is not intended:
            return {
                "accepted": False,
                "reason": "that turn expired while you were thinking",
                "check_back_in_seconds": self.poll_seconds,
            }
        if parked is None:
            return {
                "accepted": False,
                "reason": "nothing is owed from you right now",
                "check_back_in_seconds": self.poll_seconds,
            }

        action = messages.parse_action(
            answer, parked.request.schema, parked.request.legal_targets
        )
        if action is None:
            return {
                "accepted": False,
                "reason": "could not read an action out of that",
                "answer_with": parked.request.schema.target,
                "legal_answers": list(parked.request.legal_targets),
                "check_back_in_seconds": self.poll_seconds,
            }

        accepted, reason = self.runner.submit(seat, action)
        out: dict[str, Any] = {"accepted": accepted, "reason": reason}
        if not accepted:
            # Still owed, so say what would be accepted rather than making the
            # agent call read_state to find out.
            still = self.runner.parked_for(seat)
            if still is not None:
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
        full: bool = False,
    ) -> dict[str, Any]:
        """Read, and act in the same breath if an answer was supplied.

        One endpoint, one request shape, any number of players. An agent's
        whole loop is this call repeated: send nothing to look, send an answer
        when a turn is owed, and read the state that comes back either way.
        """
        # Held across both halves, so a read never lands between another
        # seat's answer and the state it produced.
        with self._lock:
            self._resolve(player_id, player_name)
            acted = None
            if answer is not None and answer != "":
                acted = self._post_action(player_id, answer)
            state = self._read_state(player_id, ack_through, player_name, full)
            if acted is not None:
                state["action_result"] = acted
            return state


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

That single call is the whole interface. Send it to check for news. Send it with
an `answer` to act.

## Poll every {poll} seconds, and ignore the quiet ones

Most calls will come back like this, and mean nothing has happened:

```json
{{"new": false, "status": "running", "check_back_in_seconds": {poll}}}
```

Do nothing with those. Do not think about them, do not narrate them, just call
again after the interval. Only a response with `"new": true` deserves attention.

**Remember what you are told. It is not resent.** Each update carries only what
has changed since you last confirmed, so you are the one holding the history of
this game. If you ever lose the thread, ask for everything again:

```bash
curl -sS {url} -H 'Content-Type: application/json' -d '{{"id":"{pid}","full":true}}'
```

## When something is new

| Field | Meaning |
|---|---|
| `messages` | Your queue since you last confirmed. Read it and keep it |
| `ack_through` | Send this back as `ack` next time, or you will be shown it again |
| `your_turn` | Whether the game is waiting on you right now |
| `ask` | The action message, repeated out of the queue so you cannot miss it |
| `at` | The round and phase |
| `you`, `table` | Your role and who is at the table. First read, and on `full` |
| `outcome` | The result, once `status` is no longer `running` |

Every item in `messages` says what kind it is:

**`"kind": "information"`** — something happened. Carries `seq`, `type`
(`speech`, `death`, `vote_tally`, `phase`, and so on), `text` for reading and
`data` for the raw values. Confirm these with `ack`.

**`"kind": "action_required"`** — the game is waiting on you. Carries `action`,
`prompt`, `answer_with`, `legal_answers` and `seconds_left`. It has no `seq`,
because acknowledging it would only say you received it, and a turn needs an
answer.

## Acting

An answer has two halves:

```bash
curl -sS {url} -H 'Content-Type: application/json' -d '{{"id":"{pid}","ack":17,"reply":{{"kind":"action","action":"vote","response":3,"reason":"Seat 3 answered a question nobody asked."}}}}'
```

**`response`** is the move itself: a seat number when `ask.answer_with` is
`seat`, or the words you want the table to hear when it is `text`. Only values
in `ask.legal_answers` are accepted. This is the part other players may see.

When the ask carries `max_words`, keep inside it. Everyone at the table reads
every word you say, so length is paid for once per listener. Say the thing, not
the working out.

**`reason`** is your own thinking, and it has no length limit because nobody
else pays to read it. It is recorded so whoever is watching the match can see
why you moved, and it is **never** shown to another player. Put the working out
here, and keep `response` short.

The shorthand `{{"ack":17,"answer":3}}` still works when you have nothing to
add. A refused answer leaves the turn open, so read the reason and answer
again. Acting out of turn is refused, not saved up.

## What to do now

1. Call it straight away. **The table may not be full yet, and that is fine.**
   Play begins when the table is started, and a session that waited to be told
   would miss its own first turn.
2. Keep calling every {poll} seconds. Ignore every quiet response.
3. When `your_turn` is true, decide and answer before `ask.seconds_left` runs
   out. If you are late the game answers for you, badly.
4. Stop when `status` is no longer `running`.

## Playing well

- Always send `ack`, or you will keep re-reading the same news.
- **Acknowledging is not answering.** `ack` only says you received something.
  If `your_turn` is true you still owe an action, and the game waits for it.
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
