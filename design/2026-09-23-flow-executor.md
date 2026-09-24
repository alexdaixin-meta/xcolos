# The Flow Executor

> **SUPERSEDED.** This draft is kept only for the reasoning it records.
> The design to build from is `2026-09-23-milestone-2-any-game.md`.
> Parts of this file contradict it.


**Status:** Design, nothing built
**Date:** 2026-09-23
**Read before:** the generic game model, which defines players, events and
asks. This defines the machine that runs them, and the contract a game fills in.

---

## 1. The idea

There is one flow. It is fixed, it is generic, and it knows nothing about any
game. A game does not describe a flow; it answers questions the flow asks.

That inversion is the whole design. If a game could define its own flow, the
runtime would need a language for expressing flows, and that language would
grow until it was a bad programming language. Instead the flow is a small state
machine with three places where it turns to the game and says: what now?

---

## 2. The machine

```
                  ┌─────────────────────────────────┐
                  │                                 │
   START ──► SETUP ──► PHASE ──► GATHER ──► RESOLVE ─┤
                         ▲                           │
                         │                           ▼
                         └──────── continue ──── CHECK ──► END
```

| State | What the runtime does | Game consulted? |
|---|---|---|
| `SETUP` | Create players, apply opening state, deliver what each is told | yes |
| `PHASE` | Label the phase, announce it | yes |
| `GATHER` | Ask the named players, wait, apply deadlines and defaults | no |
| `RESOLVE` | Apply consequences, tell players the outcome | yes |
| `CHECK` | Continue, or end | part of resolve |
| `END` | Record the result, reveal what the game says to reveal | no |

**`GATHER` is the important row.** It is the only state where the runtime waits
on people rather than on a game, and it is entirely generic: it knows how to
ask, how to collect, how long to wait and what to do when nobody answers. No
game has ever needed to change how waiting works.

---

## 3. Two jobs, and they are not the same job

The single most useful split in this design. Running a game is two kinds of
work, with opposite requirements, and conflating them is what made the earlier
drafts fragile.

| | Deciding | Wording |
|---|---|---|
| What it does | Changes state: who is out, whose turn, what a counter reads | Produces the sentence a player reads |
| Must be | **Correct.** A wrong elimination breaks the game | **Good.** A flat sentence is a worse game, not a broken one |
| Who does it | The flow, from declared rules | A model |
| Failure mode | Silent corruption | An awkward message |

**The flow updates state. The model writes the words.** A model that only
produces text cannot corrupt a game, however badly it hallucinates: the worst
case is a confusing sentence, not a player eliminated who should not be.

---

## 4. The flow owns every state change

State moves only through declared, mechanical operations. The vocabulary is
small and generic, and it is the runtime's, not any game's.

| Operation | What it does |
|---|---|
| `deal` | Assign values from a declared distribution, randomly, from the seed |
| `tally` | Reduce answers to a winner: majority, plurality, unanimity, with a declared tie rule |
| `set_status` | Move a player to a declared status |
| `adjust` | Add to or set a numeric value |
| `move` | Shift items between zones, or between a zone and a player value |

A phase declares which of these run on its answers:

```yaml
voting:
  ask: {to: playing, mode: simultaneous, answer: {type: player, exclude_self: true}}
  resolve:
    - tally: {of: answers, rule: plurality, on_tie: nobody, into: $target}
    - set_status: {player: $target, to: eliminated, unless: nobody}
```

A tally is arithmetic. It should never have been a judgement call, and under
this design it is not: the same votes always produce the same elimination,
model or no model.

### Where a model still decides

Some choices genuinely cannot be declared. Which presidential power fires,
whether a special election is warranted, what an ambiguous rule means in an
edge case.

Even there, **the model returns a choice, never a state change**:

```
runtime ──► model :  "Three fascist policies are on the board with 8 players.
                      Which power applies?"  options: [investigate, peek,
                      execution, special_election, none]
model   ──► runtime:  {"choice": "investigate", "reason": "..."}
runtime           :  applies the declared consequence of `investigate`
```

The model picks from a closed set the game file declared. The runtime applies
the consequence. There is no path from a model's output to arbitrary state.

---

## 5. Wording, and why this restores the leak guarantee

The model's other job is to write what players read, and the way it is asked
gives back the safety the previous draft spent.

**It is asked once per audience, and told only what that audience knows.**

```
runtime ──► model :  event: {player 5 eliminated by vote, tally 3-1-1,
                             revealed role: villager}
                     writing for: everyone
                     they already know: <the public record>
model   ──► runtime: "The table turns on seat 5. They were a villager."
```

For a private message the model is handed only that recipient's view:

```
runtime ──► model :  event: {investigation of player 2 returned "evil"}
                     writing for: player 7
                     they already know: <player 7's own record>
model   ──► runtime: "Your investigation of seat 2 comes back evil."
```

It cannot disclose the role of player 3 in that message, because it was never
told it. The guarantee is structural again, not a matter of the model behaving.

This is the piece the earlier draft gave up when it let one model compose
messages with full knowledge of the game. Splitting deciding from wording
brings it back, because a writer does not need to know the secrets to describe
an event that has already happened.

**Cost.** One short generation per audience per event, on a small prompt.
Cheaper than one large call that has to reason about the whole game, and it
parallelises, since the messages are independent of each other.

**The fallback is a template.** If the model is slow, expensive or unavailable,
the game file can carry a template per event type and the runtime renders it
with no model at all. Wording degrades; the game does not stop.

---

## 6. The contract

Three hooks, narrower than before.

```
setup(table)                    -> [DeclaredOperation]
next(table)                     -> phase name | End
choose(table, question, options) -> one option        # only when declared rules
                                                      # cannot decide
write(event, audience, view)    -> text
```

`setup` and the phase definitions are declarations, not model output. `next`
is a declared cycle for most games and a model choice for branching ones.
`choose` is the narrow judgement channel. `write` is the wording.

Nothing here returns a state change. The runtime reads declarations, applies
operations, and asks a model only for a choice from a list or a sentence.

---

## 7. Gathering

A phase's asks are gathered in one of two modes, and this is a property of the
ask, not of the game.

**`simultaneous`.** Everyone named is asked at once, and the phase waits for all
of them. Answers come back in player order, so speed decides nothing. This is a
vote, a bid, a set of secret orders.

**`sequential`.** Players are asked one at a time, in the order given, and each
sees the answers before it. This is a discussion, a betting round, a turn
rotation. It costs no extra model calls: the whole sequence is one phase and
one `resolve`.

```yaml
asks:
  - mode: sequential
    to: [1, 2, 4, 5]
    prompt: "Say something to the table."
    answer: {type: text, max_words: 100}
```

Two modes is enough for every game in the model document. A third would need a
game that cannot be written without it.

---

## 8. What the runtime guarantees

Everything in this list is true of every game, which is why it belongs to the
runtime rather than to any game.

- **One phase at a time.** A game cannot have two phases in flight.
- **Player order, never arrival order.** Answers are presented sorted, so who
  was quickest is invisible.
- **Deadlines and defaults.** An unanswered ask is defaulted and marked, and
  the phase proceeds.
- **Validation.** Every step and every answer is checked before it counts.
- **Entitlement.** A player is only ever sent what its audience includes.
- **Stamping.** Round and phase are recorded on every event, message and move.
- **Clocks.** Phase count and player-action count are bounded; hitting either
  ends the match as abandoned rather than as a result.
- **Recording.** Every hook call, every step, every answer, in the log.

A game that tries to violate one of these is refused with a reason, and the
refusal is logged.

---

## 9. Who does what, per phase

A phase is declared or delegated, and most are declared.

```yaml
phases:
  voting:
    ask: {to: playing, mode: simultaneous, answer: {type: player, exclude_self: true}}
    resolve:
      - tally: {of: answers, rule: plurality, on_tie: nobody, into: $target}
      - set_status: {player: $target, to: eliminated, unless: nobody}
    announce:
      to: all
      event: eliminated              # the model writes this one sentence
      fallback: "Seat {target} was voted out. They were {role}."

  presidential_power:
    decide: model                    # which power fires is a judgement call
    options: [investigate, peek, execution, special_election, none]
```

Even a fully declared phase uses the model, for one sentence. Even a delegated
phase only asks it to pick from a list. Those are the only two shapes.

**The fallback line is not decoration.** It is what runs when the model is
unavailable, too slow, or being skipped for a cheap batch run. A game with
fallbacks everywhere is playable with no model at all, which is what makes the
test suite free and the conformance runs deterministic.

---

## 10. Mafia through the machine

One round, showing who does what.

| # | Phase | Flow does | Model does |
|---|---|---|---|
| 1 | setup | Deal roles from the declared distribution | Write each player's "you are…" and the mafia's "your allies are…" |
| 2 | night | Ask mafia and detective; resolve the target and the investigation result | Write the night announcement, the mafia's confirmation, the detective's result |
| 3 | day | Set the victim eliminated | Write the death announcement |
| 4 | discussion | Ask each living player in sequence | Nothing. The players supply the words |
| 5 | voting | Tally, eliminate, check the win condition | Write the tally and the elimination |

Every decision in that round is arithmetic or a declared rule. The model writes
seven or eight short sentences and decides nothing.

The win condition is a declared comparison of counts by faction, not a
judgement, so a match cannot end at the wrong moment because a model
miscounted.

---

## 11. What a game file provides

Against this machine, a game file is:

- The **player model**: counts, statuses, values and their visibility.
- The **shared model**: values and zones, if any.
- The **answer types** it uses, with constraints.
- The **phases**: declared ones in full, delegated ones by name.
- The **rules prose**, for the delegated hooks and for the model's briefing.
- The **limits**: phase and action clocks.

Nothing about flow control. No conditions, no loops, no transitions. The
machine owns those, and a game that wants different control flow expresses it by
what `phase` returns next, which is a decision, not a language.

---

## 12. Build order

1. **The machine, with declarative hooks only.** Run Mafia entirely from a
   file, with no model. The existing test suite is the proof: if it passes with
   the hardcoded orchestrator deleted, the flow is genuinely generic.
2. **A second declarative game.** This is what validates the file format, and I
   expect it to change it.
3. **Model-answered hooks**, graded against the declarative Mafia on the same
   seed.
4. **A game that cannot be declared.** Secret Hitler, mixing declared phases
   with delegated ones.

Steps one and two need no model and no network.

---

## 13. Open questions

1. Should `resolve` be able to add another phase rather than returning to
   `PHASE`? A presidential power is arguably a sub-phase of resolution, not a
   phase of its own, and forcing it through `phase` means the game must
   remember it owes one.
2. Is `CHECK` really part of `resolve`, or its own hook? Folding it in is fewer
   calls; separating it means a game cannot forget to check.
3. Does `setup` need to be a hook at all, or is it just the first `phase`? It
   differs only in that no answers precede it.
4. What happens when a declared phase and the model disagree during oracle
   comparison? Treating the declaration as correct is the obvious answer and is
   probably wrong: the prose is what a human wrote deliberately.
