# The Generic Game Model

> **SUPERSEDED.** This draft is kept only for the reasoning it records.
> The design to build from is `2026-09-23-milestone-2-any-game.md`.
> Parts of this file contradict it.


**Status:** Design, nothing built
**Date:** 2026-09-23
**Companion to:** the Milestone 2 design, which covers the architecture. This
covers the data model: what a player is, what a game is, and what an event is.

---

## 1. What has to be generic

A turn-based multiplayer game, stripped of its theme, is four things:

- **Players**, each with a state and some values, some of which are secret.
- **Shared state**, some of which is hidden.
- **Events**: something happened, and some subset of players may know it.
- **Asks**: somebody must choose, from a declared set, within a deadline.

Everything else — roles, factions, decks, boards, phases, win conditions — is a
game arranging those four. The runtime should know the four and nothing else.

The test of this claim is section 9, which works six quite different games
through the model and says where it holds and where it does not.

---

## 2. The flow, as types

Every turn-based game has the same skeleton. Rounds repeat; a round is made of
phases; a phase is made of asks and declared consequences. The runtime tracks
that skeleton and knows nothing about what fills it.

```
Match
  └─ Round          numbered by the runtime
      └─ Phase      named by the game: "night", "betting", "mission"
          ├─ Ask        who is asked, what answer is legal
          ├─ Resolve    declared operations over the answers
          └─ Announce   events, whose wording a model supplies
```

**State moves only through declared operations.** Nothing a model returns is
ever applied directly. The five operations are the entire vocabulary:

```
deal        assign values from a distribution, from the seed
tally       reduce answers to a winner, by a declared rule
set_status  move a player to a declared status
adjust      change a numeric value
move        shift items between zones and list values
```

A model is consulted for exactly two things, and neither can change state:

```
choose(question, options) -> one of the options     # only where rules cannot decide
write(event, audience, view) -> text                # the sentence a player reads
```

### The runtime types

```
Player  {n: int, name: string, status: StatusId, values: {key: any}}
Table   {round: int, phase: string, players: [Player], shared: {...},
         clocks: {...}, status: setup|running|ended|abandoned}
Ask     {to: [int], mode: simultaneous|sequential, answer: AnswerSpec,
         deadline_s?: int, on_timeout?: Default}
Answer  {player: int, value: any, reason?: string, timed_out?: bool}
Event   {to: Audience, type: string, text: string, data?: object}
View    what one audience may see of the Table, derived from visibility
```

`View` is the type that carries the safety property. A model writing a message
is handed a `View`, never a `Table`, so it cannot disclose what it was not
given.

### The three flow shapes this covers

**Phase-cycling.** A round is a sequence of phases that repeats. Mafia, Secret
Hitler, Avalon. Declared as `cycle`.

**Rotating.** One player acts, then the next. Most board and card games. A
phase whose ask names one player, repeated.

**Simultaneous.** Everyone acts, then it resolves. Voting, bidding, secret
orders. One ask in `simultaneous` mode.

A game mixes them freely, because nothing says a round must have the same
phases twice.

---

## 3. Why the structures have to be exact

The flow updates state without knowing what game it is running. It can only do
that if every piece of state it touches is declared in a shape it understands.

So the structures below are not documentation of a convention. They are the
contract that makes a generic flow possible, and each field exists because one
of the flow's five operations needs it:

| Operation | Needs |
|---|---|
| `deal` | A distribution, and a player value to write into |
| `tally` | Answers, a rule, a tie rule, and somewhere to put the winner |
| `set_status` | A declared status set, and which of them permit acting |
| `adjust` | A numeric value, and whether it is per player or shared |
| `move` | Zones or list values, with counts and visibility |

Anything not declared cannot be operated on, which is the point. A game with an
undeclared concept has to reach for the model, and that is where correctness
stops being guaranteed.

---

## 4. The player structure

```
Player {
  n       int          1..N, assigned by the runtime, fixed for the match
  name    string       display only; never affects anything
  status  StatusId     one of the game's declared statuses
  values  {key: any}   typed and visibility-scoped by the game's declaration
}
```

That is the whole thing. No role, no faction, no team, no alive flag: those are
all `values` or `status` in some game and absent in others.

### Statuses

```yaml
statuses:
  - {id: active,     acts: true,  initial: true}
  - {id: eliminated, acts: false}
  - {id: silenced,   acts: false}
```

`acts` is the only field the runtime reads. It answers one question: may this
player be included in an ask? `initial` says where everyone starts.

Three statuses rather than a boolean matters because `silenced` exists: a
player still in the game, still receiving events, who may not be asked this
round. A hardcoded alive-or-dead flag gets that case wrong.

### Values

```yaml
values:
  player:
    - {id: role,    type: text,   visible: owner}
    - {id: faction, type: text,   visible: private}
    - {id: credit,  type: number, visible: public, initial: 0}
    - {id: hand,    type: list,   visible: owner}
  shared:
    - {id: fascist_track, type: number, visible: public, initial: 0}
```

**Types** are `text`, `number`, `bool`, `list`. Four is enough; the runtime
only needs to know what it may do to a value, and `adjust` only means anything
on a number.

**Visibility** is the field that carries the whole information model:

| `visible` | Who may read it |
|---|---|
| `private` | Nobody. Used by the flow, never rendered to anyone |
| `owner` | The player it belongs to |
| `public` | Everyone |

A role is `owner`. A faction used only for the win check is `private`, because
the runtime counts it without anyone being told. A score is `public`.

Note what changed from the earlier draft: `private` no longer means "the model
can see it". The model does not read state at all now. It is handed a view
composed for one audience, and a `private` value is in nobody's view.

---

## 5. Shared structure

```yaml
zones:
  - {id: deck,    ordered: true,  visible: none, initial: {liberal: 6, fascist: 11}, shuffle: true}
  - {id: discard, ordered: true,  visible: none}
  - {id: board,   ordered: false, visible: public}
```

A zone holds opaque items. The runtime moves them, shuffles from the seeded
generator, and enforces visibility. It never knows what an item means.

A hand belongs to a player and is a `list` value with `visible: owner`. A deck
belongs to the table and is a zone. The distinction is ownership, not shape.

---

## 6. Deals

How hidden state gets created, without the runtime knowing what a role is.

```yaml
deals:
  - id: roles
    into: [role, faction]          # player values to write
    distribution:
      4:  [{role: mafia, faction: evil}, {role: detective, faction: good},
           {role: villager, faction: good, fill: true}]
      7:  [{role: mafia, faction: evil, count: 2}, ...]
```

The runtime shuffles from the seed and assigns. `fill: true` means "everyone
left over". Counts are given per table size, filling forward from the largest
declared size at or below the actual one.

This is `deal`, and it is why roles never pass through a model. The same seed
produces the same assignment, every time, whether a model is involved or not.

---

## 7. Phases

```yaml
phases:
  voting:
    ask:
      to: playing                   # or an explicit list, or a value filter
      mode: simultaneous
      prompt_event: ask_vote        # the model writes the prompt
      answer: {type: player, from: playing, exclude_self: true}
      deadline_s: 120
      on_timeout: random
    resolve:
      - tally: {of: answers, rule: plurality, on_tie: nobody, into: $target}
      - set_status: {player: $target, to: eliminated, unless: nobody}
    announce:
      - {to: all, event: vote_result, fallback: "Seat {target} was voted out."}

cycle: [night, day, discussion, voting]
```

`cycle` is the default answer to "what next". A game whose order branches omits
it and delegates `next` to the model instead.

`$target` is a phase-local binding written by one operation and read by the
next. Not a variable in a language: a named slot, declared by `into`, valid for
the length of the phase.

---

## 8. Ending

Declared, so a match never ends at the wrong moment because a model miscounted.

```yaml
end:
  - when: {count: {faction: evil, acts: true}, op: "==", value: 0}
    result: town
    reason: "every mafia is eliminated"
  - when: {count: {faction: evil, acts: true}, op: ">=",
           other: {count: {faction: good, acts: true}}}
    result: mafia
    reason: "the mafia equal or outnumber the town"
  - when: {shared: fascist_track, op: ">=", value: 6}
    result: fascists
```

A condition is a **count over a filter**, or a **value**, compared to a number
or to another count. That is the whole vocabulary: no expressions, no
arithmetic, no parser.

It covers elimination games, track games and score games, which is most of
them. A game whose win condition does not fit declares none and asks the model
at `resolve`, accepting that the check is then a judgement.

---

## 9. Does it actually cover anything?

The claim is only worth what it survives. Six games, worked through.

**Mafia / Werewolf.** Roles as `owner` values. Night kill is `ask` to the mafia
with `type: player`. Discussion is a sequence of one-player `text` asks. Voting
is one `each` ask with `type: player`. Elimination is `set` status. ✅ Fully
covered by tier one.

**Spyfall / Who is the Spy.** One `owner` value for the location, one player
who does not get it. Questions and answers are `text` asks. A final vote. ✅
Tier one.

**Avalon.** Adds `players` with `count: 3` for a mission team, and `choice`
with `options: [success, fail]` for the mission itself, asked only of those on
it. ✅ Tier one plus `players`.

**Secret Hitler.** Needs zones: a policy deck, a discard, a drawn hand. The
president draws three (`item` ask over a zone), discards one, passes two. The
chancellor plays one. Tracks are shared `number` values. Presidential powers
are just more asks, chosen by the model from the prose. ✅ Needs tier two.

**Poker.** Hands are `owner` list values. Betting is `choice` plus `number`.
The pot is a shared value. Community cards are a `public` zone. ✅ Needs tier
two. The awkward part is not the model, it is that a betting round loops until
everyone has matched, which is many model turns.

**Codenames.** Teams are a `public` player value. The grid is a `public` zone
with a parallel `private` zone for the key. A clue is `text` plus `number`.
Guesses are `item` asks over the grid. ✅ Needs tier two.

**Where it does not reach.** Anything with real-time pressure, continuous
space, or a board whose geometry matters to legality. Chess would technically
fit as `text` moves with the model as arbiter, but the model would be doing
legality checking it is bad at, and the runtime could not help. Those want a
different kind of engine.

---

## 10. Tiers: start easy, grow deliberately

Each tier is a shippable runtime. Nothing in a later tier changes an earlier
one; it only adds.

**Tier one.** Players with statuses and values. Events. Asks of type `text`,
`player`, `players`, `choice`, `none`. Modes `each` and `first`.

Enough for Mafia, Werewolf, Spyfall, Avalon, and most social deduction. This is
what Milestone 2 ships.

**Tier two.** Shared values and zones, and the `number`, `item` and `items`
answer types.

Adds Secret Hitler, poker, Codenames, auctions, most card games.

**Tier three.** The `order` type, and whatever a real second-tier game turns out
to need. Deliberately unspecified: guessing now is how a schema gets features
nothing uses.

**The rule that keeps this honest.** A tier grows only when a real game file
cannot be written without it, and the game comes first. Adding a type because
it seems useful is how the vocabulary stops being generic and starts being a
list of everything anyone ever wanted.

---

## 11. What the runtime validates

The whole point of declaring any of this is that the runtime can refuse bad
calls. It checks, on every model action:

- Named players exist, and their status allows being asked.
- The answer type is one the file declared, with its constraints satisfied.
- A value key exists and the written type matches.
- A zone exists and holds enough items.
- Visibility is never widened except by `end.reveal`.
- The turn clocks have not run out.

A refused call is logged and returned to the model with a reason. It can be
wrong; it cannot be wrong silently, and it cannot corrupt state.

---

## 12. Open questions

1. Does `mode: first` earn its place in tier one? No social deduction game
   needs it, and it could wait for the game that does.
2. Should `text` asks carry structure, so a clue is `{word, number}` rather
   than a sentence to be parsed? Probably yes for Codenames, which argues for a
   `fields` answer type in tier two rather than making every game parse prose.
3. Does a hand belong as an `owner` list value or as a zone with an owner? The
   two overlap and one of them should go. Values feel right for things that
   belong to a player, zones for things on the table.
4. How does a game express "the same ask, repeated until a condition"? A
   betting round, or a discussion that continues until nobody objects. The
   model can loop, but each iteration is a model turn, and that is the main
   cost driver in section 4 of the milestone design.
