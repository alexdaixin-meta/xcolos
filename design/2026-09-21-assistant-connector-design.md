# Linking a Player's Assistant Session to a Seat

**Status:** Design, nothing built
**Date:** 2026-09-21
**Depends on:** the Milestone 1 engine design, particularly the client and server split

---

## 1. What this replaces

Earlier attempts at "link a real model" all failed on the same point. Calling a
provider API from XColos, or from the player's browser, creates a *new*
conversation. The player's own assistant session, with everything it has
accumulated, is not in it.

So the model does not come to XColos. XColos goes to the model.

**XColos exposes a connector. The player's existing assistant session attaches
to it and plays from inside itself.** Nothing is billed to the operator, no
credential exists anywhere, and the session context is not merely preserved, it
is the whole point: it is the player's own session, unchanged.

This is also the shape the player described early on. The agent pulls its
current status and pushes its action, rather than being called.

---

## 2. The two halves of "who drives"

These sound contradictory and are not.

**The server drives the game.** Whose turn it is, what is legal, what each seat
is entitled to know, when a turn expires. None of that moves.

**The assistant drives its own participation.** It asks when it wants, answers
when it is due, and is refused when it is not. The server never calls out to it.

The practical consequence is that the server can no longer hold an open call
waiting for a seat. It parks the turn as state and returns. The orchestrator is
already a generator that suspends where it wants an action, so parking it is
natural; a submission resumes it.

That deletes the blocked thread per pending seat, which matters once seats take
minutes rather than milliseconds.

---

## 3. Slowness is the design constraint

A conversational session answers in tens of seconds, sometimes minutes. It also
only acts when the player prompts it. Four things follow.

**Deadlines become per seat, not per game.** A scripted bot gets seconds. A
person typing gets minutes. A connector session gets longer still. The turn
deadline already exists as an operator setting; it becomes a property of the
seat.

**A table runs at the pace of its slowest seat.** That is unavoidable and
should be stated rather than engineered around. Mixing bots and connector
players is fine, but the match will feel like the connector player's match.

**Every read must be self-sufficient.** This is the important one. The
assistant's context is shared with everything else the player is doing, and the
game is not its main concern. It will lose the thread. So a situation read
returns the standing state as well as what is new: your seat, your role, who is
alive, what phase it is, and what you are being asked. Re-briefing on every read
costs a few hundred tokens and removes an entire category of failure.

**The web app has to show whose turn it is.** A chat session acts when
prompted, so the player needs to know when to nudge it. Whose turn it is, and
how long is left, belong on screen.

---

## 4. The tool surface

Four tools. Small on purpose: an assistant reading these for the first time
should need no explanation.

### `xcolos_tables()`

Open tables and how many seats each has free. No credential. Used once, to find
somewhere to sit.

### `xcolos_take_seat(join_code)`

Binds this session to one seat. The code is short, single use, and shown by the
web app next to an open seat.

Returns the seat number, the full briefing (rules, table size, your role, the
round shape), and a **seat token** for later calls. The assistant keeps the
token in its own context; the server stores nothing about the session.

The join code is what links the person sitting in front of XColos to the
session answering for them.

### `xcolos_situation(seat_token)`

The pull. Returns, every time:

| Field | Why it is always sent |
|---|---|
| `you` | Seat number, role, alive or dead. The session may have forgotten |
| `table` | Who is alive, what phase, what round |
| `new_since_last_call` | What happened that this seat is entitled to know |
| `your_turn` | Whether an action is owed right now |
| `ask` | What to answer, if it is your turn |
| `legal_answers` | The only answers that will be accepted |
| `seconds_left` | So the assistant knows whether to think or answer |

Safe to call at any time and as often as it likes. Returns quickly, always. It
never blocks, because a tool call that hangs for two minutes is a bad citizen
inside someone's chat.

### `xcolos_act(seat_token, answer)`

The push. Submits one action.

Returns accepted, or refused with a plain reason: not your turn, that seat is
dead, the turn already expired, you already answered. A refusal is not an error;
the assistant should read it and call `situation` again.

Answering twice is refused rather than applied twice.

---

## 5. What stays exactly as it is

The kernel, the entitlement model, the orchestrator, the message types, the
logging, the ownership model, and the failure ladder. A connector seat is a
client like any other. It receives only what it is entitled to, it can answer
badly or not at all, and the declared default covers it.

Specifically, `situation` is built from the same per-seat view every other
client gets. There is no second path to state, so there is no second place for a
leak to hide.

---

## 6. Open questions

1. Does a connector seat get a deadline at all, or does its turn simply wait
   until the player nudges their session? Waiting is friendlier and risks a
   table stalling forever. A long deadline with a visible countdown is probably
   the right middle.
2. Should `situation` be callable by a seat that is dead? Probably yes, since
   eliminated players still watch, and refusing would be confusing.
3. Does one session take more than one seat? Technically fine, but a single
   session holding two seats sees both sets of secrets, which is exactly the
   case the ownership rule exists to prevent. Likely one seat per session.
