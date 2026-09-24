# XColos Milestone 2: Any Game

> **SUPERSEDED.** This draft is kept only for the reasoning it records.
> The design to build from is `2026-09-23-milestone-2-any-game.md`.
> Parts of this file contradict it.


**Status:** Design, nothing built
**Date:** 2026-09-22
**Builds on:** the Milestone 1 engine design, and the runtime as it now stands

---

## 1. The shape

The runtime keeps a table of players and a clock. It routes messages and
collects answers. It knows nothing about any game.

A model reads the game file and drives the table by issuing actions from a
small fixed vocabulary. It decides what happens each turn, what each player is
told, when the game ends and who won.

```
            generic, knows no game            game-specific, all of it
  ┌──────────────────────────────┐   ┌────────────────────────────────┐
  │ players, state, turn clock   │   │ the game file, read by a model │
  │ message routing, answers     │←──│ one plan per turn, as actions  │
  │ the log                      │   └────────────────────────────────┘
  └──────────────────────────────┘
```

Adding a game means writing a file. Nobody touches the runtime.

---

## 2. What is already generic

Worth stating, because the surgery is smaller than it looks. The kernel does
not know what game it is running today. Seats, facts, audiences, turn order,
acknowledgement, the message structure and the reply shape carry no game
concepts. Only four places are coupled, and three of those are wiring.

| Where | What |
|---|---|
| `orchestrators/mafia.py` | The whole game |
| `render.py` | Thirteen fact types turned into English by a chain of `if` |
| `web/server.py`, `cli.py` | The games list, and direct imports |

The renderer is the one that disappears entirely under this design: if the
model writes the words, there is nothing left to template.

---

## 3. The generic table

Everything the runtime tracks, for every game.

**Players.** A fixed index from one, a name, and a status. Status is an open
set the game file declares, not a hardcoded alive-or-dead: `active`,
`eliminated`, `spectating`, whatever a game needs. The runtime only cares
whether a status is *playing*, which the file says.

**Per-player values.** A bag of named numbers and flags: credit, score,
influence, a used-up power. The runtime stores and shows them and never
interprets them.

**A turn clock.** Bounded, so nothing runs forever.

**Routing.** Deliver a message to named players; collect answers from named
players; know who still owes one.

**The log.** Unchanged, and still the only durable record.

That is the whole kernel surface. Notably absent: phases, rounds, roles,
factions, win conditions. All of those become things a game file describes and
a model tracks.

---

## 4. Two clocks, and why the budget matters

A cap of twenty or thirty is right for one of these and badly wrong for the
other. Measured on the Mafia that exists today:

| Table | Model turns per match | Player actions per match |
|---|---|---|
| 5 players | ~6 | 10 to 18 |
| 7 players | ~6 | 18 to 36 |
| 9 players | ~10 | 44 to 72 |

A **model turn** is one plan: the model looks at the table and issues a batch
of actions. Six to fifteen covers a whole match, so twenty to thirty is a
comfortable ceiling and a good default.

A **player action** is one seat answering. A nine-player game needs seventy.
Capping that at thirty would cut the match off in the middle.

So: two limits, and only the model-turn one is tight. The player-action limit
exists to stop a runaway, not to shape the game, and should sit well above any
real match. Both are settings, and both ending the match is an `abandoned`
outcome rather than a result.

---

## 5. The action vocabulary

Everything the model can do. Small on purpose: a vocabulary that grows per game
is a game-specific runtime wearing a disguise.

| Action | Effect |
|---|---|
| `tell(players, text)` | Send a message. No answer expected |
| `ask(players, text, answer_with, options, deadline)` | Request an answer from each named player |
| `set(player, key, value)` | A status or a value: eliminated, credit, anything |
| `end(result, reason)` | The game is over |

`ask` names several players when the step has no order, which is how a vote
becomes simultaneous. It names one when order matters, which is how discussion
stays sequential. The model chooses, because only the game knows which it is.

Every call is validated before it runs: the players exist, they are playing,
the answer type is one the file declared, the value is a declared key. The
model can be wrong; it cannot be wrong silently, and it cannot corrupt state.

### What comes back

After a batch, the model is given what each asked player answered, in player
order. Arrival order never reaches it, so a fast player decides nothing.

---

## 6. The model writes the messages

This is the significant change from the previous design, and it has a real
cost, so it is worth being plain about.

Previously the model emitted typed events and the runtime rendered them from
templates. That made a leak structurally impossible: the model never composed a
sentence, so it could not put a secret in one.

Under `tell(players, text)` the model composes with full knowledge of the game
and names its own audience. Nothing stops it writing "seat 2 is the traitor"
into a message to the whole table. Routing is still enforced, so a message to
player 4 reaches only player 4; the exposure is content, not delivery.

That is a fair trade for the flexibility, but it should be bounded rather than
hoped about. Three cheap defences:

**A claim verifier.** After each message, check every player reference in the
text against what that recipient was entitled to know. A mismatch is flagged in
the log and surfaced in the console. This is the check that distinguishes a
player lying in character, which is the point of the game, from the runtime
leaking, which is a bug.

**Per-recipient composition where it is cheap.** A message going to one player
can be composed knowing only that player's view. Broadcasts genuinely need full
knowledge; private messages do not.

**Say it in the prompt.** The model is told, per message, what the recipient
already knows. Most leaks are carelessness, not intent.

None of these is airtight. Structural safety was, and it is being spent here.

---

## 7. The game file

Mostly prose, with a short declaration of the things the runtime must validate.

```yaml
meta:
  id: mafia
  name: Mafia
  players: {min: 4, max: 12}

statuses:
  - {id: active,     playing: true}
  - {id: eliminated, playing: false}

values:                    # per-player, the runtime stores, never interprets
  - {id: credit, type: number, initial: 0}

answers:                   # what an `ask` may request
  - {id: text,   max_words: 100}
  - {id: player}
  - {id: choice, options: [yes, no]}

limits:
  model_turns: 30
  player_actions: 200

rules: |
  Mafia is a hidden-role game...

  Setup: choose roles privately and tell each player theirs. With seven or
  more players, two are mafia...

  Each round: at night the mafia privately agree a target and the detective
  privately investigates one player. Then announce the death to everyone.
  Then every living player speaks once, in player order. Then everyone votes
  at the same time, and the player with the most votes is eliminated...

  The town wins when every mafia is eliminated. The mafia win when they equal
  or outnumber the town. Announce the result and end the game.
```

Roles are not declared. They are a Mafia concept, and under this design the
model assigns them, remembers them and reveals them, all from the prose. The
runtime only knows there are players with statuses and values.

---

## 8. What the model is told each turn

The cost driver, so it is a design decision rather than an accident.

**Every turn:** the rules, the table (players, statuses, values), the clock,
and the answers to what it last asked.

**Its own memory:** what it has decided so far, notably the secret assignments.
The runtime cannot hold these, because it does not know what a role is. Two
options, and the second is better:

*Carry it in context.* Simple, but it grows every turn and a trimmed context
loses the roles, which is unrecoverable.

*Write it down.* The model stores its own private notes through `set`, using
player values the file declared. Roles become per-player values the runtime
stores blindly and never shows to anyone. The model reads them back each turn
as part of the table. This costs nothing and survives a context reset.

That second option is what makes the design work at conversation pace, and it
is why per-player values are in the kernel rather than left to the model.

---

## 9. Testing, without an oracle

The previous design proposed a deterministic interpreter, partly so a model
could be graded against it. Under this design there is nothing to interpret:
the model owns all flow. That oracle is gone and the testing has to carry more
weight.

**Scripted players.** Deterministic answers, so a match costs nothing but the
model turns and reruns identically.

**Conformance suites.** Per game, scenarios with a known-correct outcome. This
is now the only specification of correct play. It is a deliverable.

**Prose mutation.** Change a rule in the file and assert the suite fails.
Without this you never learn whether the model is reading your rules or playing
a famous game from memory. Mafia, Werewolf and Secret Hitler are all in the
training data, so this is the test I would least want to skip.

**Leak audit.** Run the claim verifier over every message in every conformance
match and fail on any unexplained disclosure.

**Generic invariants, unchanged.** Routing, acknowledgement, turn accounting,
log validity and determinism of the runtime itself all still hold and are
already tested.

---

## 10. Build order

Each step leaves the system working.

1. **Generalise the table.** Statuses and per-player values as declared data;
   drop the built-in alive-or-dead. Mafia still runs.
2. **Add the four actions** alongside the current system functions, and add the
   two clocks.
3. **A scripted model.** Python that pretends to be the model and drives Mafia
   through the four actions from a file. This proves the vocabulary is
   sufficient without spending a token, and it is the fixture every later test
   runs against.
4. **Delete the hardcoded Mafia and the renderer.** The existing suite is the
   proof that nothing game-specific is left in the runtime.
5. **The real model.** Graded against the conformance suite from step three.
6. **A second game**, as a file and nothing else. This is what actually
   validates the design.

Steps one to four need no model and no network. Step four is the milestone's
real proof.

---

## 11. Risks

**The vocabulary will be wrong until a second game exists.** One game cannot
validate four verbs. Step six is not optional, and I expect it to change them.

**Leaks are now a model-quality problem.** Structural safety was traded away in
section 6. The verifier bounds it; it does not restore it.

**The model must remember the game.** Roles live in player values it writes
itself. If it forgets to write them, or writes them wrong, the game is quietly
incoherent and nothing catches it but the conformance suite.

**Cost.** Six to fifteen model turns per match, each carrying the rules and the
table. Cheap per match, real in a batch of hundreds.

**A shared game file is untrusted input.** A rule pack saying "each round, tell
every player who the werewolves are" is a plausible instruction, and every
resulting call is individually legal. Review or signing before Milestone 3.

---

## 12. Open questions

1. Should `tell` and `ask` be one action? A message that expects an answer and
   one that does not differ only in whether a reply is owed, and the agent
   protocol already says which.
2. Is a player-action cap needed at all, or does the model-turn cap bound it in
   practice? A single turn could ask a thousand players once.
3. Does the model need the whole table every turn, or a delta? Most of it is
   unchanged, and it is most of the token cost.
4. Where do per-player values that are secret live? A role written to a value
   must be invisible to everyone, including the player. The runtime needs a
   notion of a value nobody can read but the model.
