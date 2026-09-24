# Milestone 2: Any Game

**Status:** Built and running. Sections 4, 8 and 9 have been
corrected against what the first matches actually did.
**Date:** 2026-09-23
**Supersedes:** the Milestone 2 draft of 2026-09-22, the flow executor note and
the generic game model note. Those went through three incompatible versions;
this is the one to build from.

---

## 1. What this milestone is

One game is hardcoded in Python. This removes it. A game becomes a file, and a
model drives it by filling slots in a flow the system owns.

The shape, settled:

- **The flow is fixed and system-run.** A game does not describe a flow; it
  declares which of the flow's steps it uses and skips the rest.
- **The system owns all state.** Nothing changes except by the system applying
  a validated update.
- **The model writes the words and proposes the updates.** It calls nothing.
  It returns JSON against a schema it has been taught, and the system applies
  it.

---

## 2. The flow

Four kinds of step. A round is a list of them, in whatever order a game says.

```
SETUP
  brief    tell each player the game, the table, and what only they know

ROUND, repeating
  ask      address some players
             with an answer      an action: the game waits for them
             without an answer   information: delivered, not waited on
  update   change state, and say what changed
  check    continue, or end
```

**This replaced a list of twelve named slots** (`secret_act`, `reveal`, `vote`,
`resolve_vote`, `nominate`, `power` and so on). The twelve were a taxonomy of
what a step is *for*, and a taxonomy is a guess about games nobody has written
yet: every new game would either bend to fit a slot that nearly matched or need
a thirteenth. These four are what the engine *does*, and there is nothing else
it can do. A game's own vocabulary lives in `phase` and `label`, so Mafia still
has a night and a vote; the engine has neither.

Mafia's round, which is the shape the flow was written from:

```
phase night   ask      nightfall             information, to everyone
              ask      the kill              action, the mafia, at once
              ask      the investigation     action, the detective
              update   the night resolves    apply the kill and the reading
phase day     update   dawn                  reveal the death
              check    after the night
              ask      the debate            action, everyone, in seat order
              ask      the vote              action, everyone, at once
              update   the verdict           eliminate and reveal
              check    after the vote
```

**Every ask that changes something is followed by an update.** A night kill has
to be applied before the day discusses it, or players talk about a death that
has not happened.

**Each step is gated.** Before running one the system asks whether this game,
in this round, uses it. The answer is arithmetic when the game file states one
and a judge's when the game states a sentence. A skipped step costs nothing.

### Who the game waits for

The distinction the whole loop turns on, and the only thing that can stop it.

An `ask` carrying an `answer` spec is an **action**: the addressed players owe
a reply and nothing moves until they give one. An `ask` without one is
**information**: delivered, acknowledged, and the round carries straight on.

A step may also set `compose: true`, which hands the wording to a model. The
model writes each addressed player their own message and marks each one `info`
or `action`; the engine then waits only on the ones marked `action`. This is
the one place a model changes control flow rather than only wording, so it
fails closed in every direction: no judge, no `compose`, or a reply that does
not validate, and every addressed player is asked with the step's own template
exactly as if the feature did not exist. A dispatch missing one recipient is
rejected whole rather than silently dropping that player out of the round.

Composition is off by default. A template is free, reproducible, and cannot
hallucinate, so a call has to be worth making.

---

## 3. The structures: version 1

Fixed now, expected to change. Both structures carry a schema version, in the
game file and on the first line of every log, so a change is visible rather
than silent and an old log stays readable.

```yaml
schema: 1
```

**What iterating means.** Three grades, and only the first is cheap:

| Change | Cost |
|---|---|
| Add an attribute type, a status field, a step to the flow | Additive. Old files keep working |
| Add a visibility value, or a new update operation | Needs a version bump; old files still load |
| Change what a visibility means, or how allies resolve | Breaking. Old files must be rewritten |

**What I expect to change first**, so it is not a surprise: whether `ally`
attributes may be written mid-match, how a step runs twice in one round, and
whether a fourth visibility is needed. Those are the open questions in section 12
and none of them is settled by writing one game.

The rule that keeps the iteration honest is the same one as for the flow: a
field is added when a real game file cannot be written without it, and the game
comes first.

---

## 4. The Player structure

```json
{
  "id": 3,
  "name": "Curie",
  "status": "active",
  "attributes": [
    {"key": "role",        "value": "detective", "visible": "ally"},
    {"key": "claimed_role","value": "villager",  "visible": "public"},
    {"key": "marked",      "value": true,        "visible": "others"}
  ],
  "owed": null
}
```

Four fields the system owns, and one list the game fills.

| Field | Written by | Notes |
|---|---|---|
| `id` | the system, once | 1..N, fixed for the match |
| `name` | the system, once | display only, never affects anything |
| `status` | a validated update | one of the game's declared statuses |
| `attributes` | `deal`, and validated updates | the game's own data |
| `owed` | the flow only | which ask this player owes, or null |

### Attributes

Every piece of game-specific data about a player is an attribute: a key, a
value, and who can see it. There is no separate bucket for roles, teams,
counters or hands. A role is an attribute. A score is an attribute.

```
Attribute { key: string, value: text|number|bool|list, visible: Visibility }
```

### Visibility

Three values. Every attribute is visible to somebody; nothing is invisible to
everyone.

| `visible` | Who sees it | Example |
|---|---|---|
| `public` | everyone, including its owner | a vote count, a claimed role, a score |
| `ally` | its owner, and anyone allied with them | the role itself |
| `others` | everyone **except** its owner | a mark on your forehead |

**`ally` is the one that does the work**, because it collapses two cases that
would otherwise need separate rules. A villager is their own only ally, so
`ally` resolves to just them: they know their role and nobody else does. A
mafioso's allies are the other mafia, so the same declaration gives them a
shared secret. One value, both behaviours, no special case for "solo" roles.

Getting that to be true took a correction, described next.

**`others` is rarer and real.** Games where you cannot see your own card while
everyone else can. It is here because it costs nothing and its absence would be
a hard stop for that whole family of games.

### Who counts as an ally

The game declares which attribute defines allegiance, **and which values of it
are a team that knows itself**:

```yaml
allies_by:
  attribute: faction
  mutual: [evil]
```

The first draft was just `allies_by: faction`, on the reasoning that a villager
has a unique value and so is their own only ally. That reasoning is wrong, and
the first match run through the engine said so: every villager was handed a
message naming the other villagers as allies. Villagers do not have unique
factions. They share `good`, which is the same attribute the win condition
counts. One field was being asked to mean two things at once, mutual knowledge
and which side you win with, and in Mafia those differ.

`mutual` separates them. Only players whose value appears in that list see one
another; everyone else is their own only ally, whatever they share. The
conspiracy gets shared sight and the town stays in the dark, from one line, and
`faction` still counts correctly for the ending.

Omit `mutual` and every value is a knowing team, which is right for a game of
declared, visible sides. Omit `allies_by` entirely and `ally` means owner-only
everywhere, which is right for a game with no teams. A null value is never an
allegiance: sharing "unknown" is not sharing a side.

The lesson generalises past this one field. A visibility rule that reads
correctly in a design document can still be wrong, and the cheapest way to find
out is to run a match and read what each seat was actually sent.

### Declaring attributes

```yaml
allies_by: {attribute: faction, mutual: [evil]}

attributes:
  player:
    - {key: role,         visible: ally,   type: text}
    - {key: faction,      visible: ally,   type: text}
    - {key: claimed_role, visible: public, type: text, initial: null}
```

**Where something lives is the game file's call, not the system's.** The one
rule the system enforces is that the record in section 5 is written by the flow
and never by an update, so what a player *did* always has a single source of
truth.

Beyond that a game decides. A useful default: things a player *is* are
attributes, and things a player *did* are read from the record rather than
copied onto them. A game that wants a running vote count displayed can declare
one as a public attribute; it just has to keep it in step with the record, and
nothing stops it.

Four types: `text`, `number`, `bool`, `list`. That is what the update
operations need, since `adjust` only means something on a number and `append`
only on a list.

An undeclared key cannot be written, which is what stops a model inventing
state the system cannot validate or display.

### What removing the hidden bucket costs

The earlier draft had a third bucket for values nobody is ever told, used for
the win check. It is gone, and that is the right call for every game in
section 2: in all of them a player knows their own alignment, so `ally` covers
it.

The system still reads every attribute regardless of visibility. Visibility
shapes **views**, not storage, so a win condition counting factions works
exactly as before.

What is genuinely lost is an attribute nobody may learn, including its owner:
an alignment assigned secretly and never revealed. A game needing that must
derive it rather than store it, or the vocabulary needs a fourth value. Worth
knowing before it surprises someone.

---

## 5. The Game structure

```json
{
  "id": "w0001-g2",
  "round": 2,
  "step": {"index": 7, "use": "vote", "label": "the vote"},
  "status": "running",
  "attributes": [
    {"key": "deck", "value": ["liberal", "fascist"], "visible": "none"}
  ],
  "record": [ ... ],
  "players": [ ... ],
  "clocks": {"rounds": 2, "rounds_max": 20, "actions": 31, "actions_max": 400},
  "result": null
}
```

| Field | Written by |
|---|---|
| `id`, `round`, `step`, `status`, `clocks`, `result` | the flow, never an update |
| `attributes` | `deal`, declared operations, and validated updates |
| `record` | the flow, when an answer arrives. **Never by an update** |

Table attributes take `public` or `none`, since `ally` and `others` are
relative to an owner and a table has none. `none` is the face-down deck: the
system shuffles and draws from it and no view contains it.

There is no separate zone concept. An ordered collection is a `list`
attribute, and shuffle, draw and discard are operations on lists.

### The record

Everything any player has done, held by the game rather than smeared across
players.

```json
"record": [
  {"round": 1, "step": "vote",       "player": 3, "value": 5, "visible": "public"},
  {"round": 1, "step": "vote",       "player": 4, "value": 5, "visible": "public"},
  {"round": 2, "step": "secret_act", "player": 2, "value": 4, "visible": "ally"},
  {"round": 2, "step": "discuss",    "player": 6,
   "value": "Seat 5 has said nothing useful.", "visible": "public"}
]
```

Each entry is one answer, addressed by round, step and player. The flow writes
it when the answer arrives, and nothing else may write it.

**This is where a vote count comes from.** "Seat 5 received three votes" is a
query over the record, not a number stored on seat 5. One source of truth, so
the tally and the count cannot drift apart, and a model that miscounts is
contradicted by the data rather than believed.

It is also what makes `verify` possible. When a step declares
`verify: {tally: plurality}` the system runs that tally over the record itself
and rejects an update that eliminates anyone else. The model writes the
announcement; the arithmetic is not its job.

And it is what a game reads to reason about the past: who voted with whom, who
has been quiet, who investigated whom. Without it, every such question would
need its own player attribute, maintained by hand, and one of them would
eventually be wrong.

### Who sees an answer

The answering player always sees their own answer. `visible` says who *else*
does, and the step declares it:

```yaml
- use: vote
  answers_visible: none        # a secret ballot
- use: discuss
  answers_visible: public      # said out loud
- use: secret_act
  answers_visible: ally        # the mafia agree a target together
```

`none` is the default. For Mafia this is exactly right: an individual vote is
nobody else's business, and the public tally is an announcement derived from
the record rather than a disclosure of it.

Note that `none` here is not the visibility removed in section 4. That would
have been an attribute nobody could see, including its owner. This is an answer
its own author obviously knows.

The private `reason` a player attaches to an answer is stored alongside it and
appears in **no** view at any visibility. It is for the operator and the log.

### Views

A **view** is what one audience may see, derived mechanically from visibility.

```
view(for: player 3) =
  round, step, status, clocks
  game attributes where visible == public
  for every player p:
    id, name, status
    attributes of p where:
        visible == public
     or visible == ally   and p is 3, or p is allied with 3
     or visible == others and p is not 3
  record entries where:
        visible == public
     or player is 3
     or visible == ally and that player is allied with 3
  never any `reason`
```

Views are the type a model is handed when it writes a message. It is never
given the game object, which is what keeps a leak structurally impossible
rather than a matter of the model behaving. One function, one test.

---

## 6. How state is updated

**The model returns JSON. The system applies it.** The model calls nothing,
which is what makes this safe to build.

An update is a list of explicit changes, not a new copy of the state:

```json
{
  "updates": [
    {"player": 5, "op": "set",    "key": "status",         "value": "eliminated"},
    {"player": 3, "op": "set",    "key": "claimed_role",   "value": null},
    {"game": true, "op": "adjust", "key": "deaths_this_round", "value": 1},
    {"game": true, "op": "append", "key": "discard",       "value": "fascist"}
  ],
  "reason": "Seat 5 took 3 of 5 votes; seat 2 and seat 4 took one each."
}
```

One change per record: who, what operation, which key, what value. `status` is
the one key that is not an attribute; everything else names a declared
attribute of that player or of the table.

### Why a diff rather than the whole state

A full replacement is simpler to generate and worse in every other way. It
costs the whole table in tokens on every step. A player omitted from it is
ambiguous: deleted, or unchanged? And a model that regenerates the table can
silently drop a value nobody notices until the win check is wrong.

A diff is also exactly what belongs in the log. Every line above is one audit
record.

### Operations

Four, and they cover every game in section 2.

| Operation | Meaning |
|---|---|
| `set` | Assign an attribute, or a status |
| `adjust` | Add to a number |
| `append` | Push onto a list |
| `remove` | Take a named item out of a list |
| `disclose` | Tell named players one attribute of one player |

`disclose` is the one that is not obvious, and writing the Mafia file is what
found it. A detective learns whether a suspect is evil. That is not a state
change and not a message a model can write, because writing it would mean
showing a model the suspect's faction, which is exactly what must not happen.

So the system does it: it reads the attribute itself and puts the fact in that
recipient's view. The model then writes the sentence from a view that now
legitimately contains it. Revealing a dead player's role to the table is the
same operation with a wider audience.

Without `disclose`, every game with private information would need either a
model with full sight or a special case in the runtime.

No paths and no nesting. A `key` is a declared attribute name or the literal
`status`, and that is the whole address space. Nesting would be a game
modelling something the system cannot validate.

Visibility is never part of an update. An attribute's visibility is fixed when
the game declares it, and only a declared reveal at `end` changes it. A model
cannot make a role public by writing to it.

### Where the system checks the model's arithmetic

This is the part worth building even though it is extra work.

An update is validated for **legality** everywhere, and for **correctness**
wherever the game file says the answer is mechanical:

```yaml
vote:
  answer: {type: player, exclude_self: true}
  verify: {tally: plurality, on_tie: nobody, must_eliminate: true}
```

With `verify`, the system computes the tally itself from the answers it
collected and rejects an update that eliminates anyone else. The model still
writes the announcement; it no longer gets to decide who died.

Not every step can be verified. Most of the ones that matter can, because the
steps where a wrong decision breaks a game are usually the arithmetic ones:
tallies, counters, thresholds, win conditions.

---

## 7. What the system validates

On every update, before anything is applied:

- The player exists, and `id` was not invented.
- The status is one the game declared.
- The key was declared, and the value matches its type.
- Visibility is not widened. A model cannot move an attribute from `ally` to
  `public`; only a declared reveal at `end` does that.
- A table attribute marked `none` is not written by a model at all.
- Where `verify` is declared, the model's update matches what the system
  computed.
- Clocks have not run out.

A rejected update goes back with the reason attached, bounded retries, then the
step's declared fallback. The same ladder a player's answer already goes
through, for the same reason: the game must not stall.

**What this cannot catch.** A legal, unverified update that is simply wrong.
"Eliminate player 3" when the rules say player 5, on a step with no `verify`.
Three things narrow it: declare `verify` wherever the answer is mechanical,
conformance suites per game, and the `reason` field, which does not prove
anything but puts a wrong decision and its justification in the log together.

---

## 8. What the model is asked, and when

Three kinds of call. None of them changes state.

```
gate(step, view)              -> run | skip
write(step, event, audience)  -> the text for that audience
update(step, answers, view)   -> the JSON diff above
```

`write` is handed one audience's view, never the whole table, so it cannot
disclose what it was not given. That is what keeps leaks structural rather than
a matter of the model behaving.

`update` needs more than one view, because a resolution spans players. It is
the one call with broad sight, and it is also the one whose output is a diff
the system validates rather than text it forwards.

### Batch by step, not by player

The first sketch looped players and called the model for each. Measured at
seven players over three rounds:

| | Calls per round | Per match |
|---|---|---|
| One call per player per step | 24 | 79 |
| One call per step | 4 | 13 |

Six times the cost for the same messages. One `write` call returns a message
per recipient, each composed against that recipient's view, and they can differ.

### Conditions in plain language: the judge

The comparison language in section 6 is deliberately small and always will be.
Anything past counting and comparing has to be said in words. So a `when` on a
step and a `when` on an ending both accept a sentence as well as a comparison:

```yaml
end:
  - when: Every player whose faction is evil has been eliminated.
    result: town
```

A sentence is answered by a **judge**: a fourth kind of call, separate from the
three above, and a different model from the ones playing.

```
rule(question) -> {answer: true | false, reason: "one sentence"}
```

Four properties make this safe to add.

**The judge never joins the table.** It receives full sight, including every
role, and returns a boolean plus a reason. It writes nothing an agent reads
except the reason attached to an ending, which is public by the time anyone
sees it. A judge that hallucinates can end a match early. It cannot leak a
role, because leaking requires a channel and it has none.

**The judge is never asked what the system can compute.** Tallies, counts and
comparisons stay declarative. Asking a model to count is how you get a result
that is wrong one time in fifty and unreproducible every time.

**Silence is not a yes.** With no judge wired in, a prose ending is declined
and a prose gate opens. Both defaults keep the match running, because a match
that overruns hits the round cap and says so, while a match that ended on a
question nobody answered is indistinguishable from one that ended correctly.

**Every ruling is logged** with the question, the answer, the reason and the
source, so an ending anybody disputes can be read back.

The judge is stateless. Each question carries the whole table and the rules
text; there is no conversation and no history. A referee should answer from the
state in front of it, not from something it half-remembers four rounds ago.
That also makes the call reproducible and cheap to retry.

#### What it costs, measured

Run against Muse Spark on the internal Model API, five-player Mafia with both
endings written in English:

| | |
|---|---|
| Judge calls per match | 3 |
| Latency per call | 2-3s |
| Added wall-clock per match | ~9s |

Three things got it there, and the first two were not optimisations so much as
corrections.

**All the endings are one call, not one call each.** The rules are still tried
in declared order; they are simply asked about together, as a choice between
labels plus "none". A check step with three spoken endings was three sequential
round trips.

**The newest model was the wrong default.** On the same prompt,
`rl-muse-spark-1-1` answers in 2-3s and `rl-muse-spark-1-3` takes 40-60s and
sometimes drops the connection. Twenty times the latency for a yes-or-no
question about a table that is already fully described in the prompt. A judge
is called several times a round, so latency dominates and the older model wins.

**Model ids are granted per team and are not the ids in the docs.** A key
issued through the playground carries `rl-muse-spark-*-playground`, not
`muse-spark-*-eval`. A 404 now lists what the key actually holds rather than
sending anyone to a wiki.

#### Grading it against the arithmetic

The declarative path is not legacy. It is the oracle. The shipped Mafia states
its endings as comparisons; the test suite takes that same file, rewrites only
the endings as English, and runs both on the same seed with a judge that
computes what the comparison would have said. The two must produce an identical
fact-by-fact trace. A prose rule can therefore be graded against a rule that
cannot be wrong, which turns "did the judge get it right" from an opinion into
a test.

Every definition that ships in the library must run with no judge at all. There
is a test that asserts it.

Live, on two seeds, the spoken endings reached the same winner in the same
number of rounds as the arithmetic ones, and the reasons the judge gave were
its own: *"One evil and one good remain alive, so evil count equals good
count."*

### The round cap

Two hundred is a fine hard ceiling and a poor default. Mafia takes two to five
rounds. At thirteen calls a round, a runaway to two hundred is twenty-six
hundred calls. Default to twenty; keep two hundred as the limit that abandons
the match.

---

## 9. The game definition

Everything needed to run a game, and nothing that belongs to the runtime. Ten
sections; six of them are optional.

| Section | Required | What it declares |
|---|---|---|
| `schema` | yes | The definition version, so a change is visible |
| `meta` | yes | Identity and how many can play |
| `statuses` | yes | The states a player can be in, and which permit acting |
| `attributes` | yes | Per-player and per-table data, with visibility |
| `allies_by` | no | Which attribute makes two players allies |
| `deal` | no | How hidden attributes are handed out at setup |
| `steps` | yes | Which flow slots this game uses, in order |
| `end` | yes | When the game is over and who won |
| `limits` | no | Clocks, with defaults if omitted |
| `rules` | yes | The prose a model reads |
| `text` | no | Fallback wording, so the game is playable with no model |

A complete example is `examples/mafia.yaml`, which expresses everything the
hardcoded Python Mafia does today. Writing it is what found `disclose`.

### `statuses`

```yaml
statuses:
  - {id: active,     acts: true, initial: true}
  - {id: eliminated, acts: false}
```

| Field | Meaning |
|---|---|
| `id` | The name, used in updates |
| `acts` | May a player in this state be included in a step? The only field the system reads |
| `initial` | Where everyone starts. Exactly one status must set it |

### `attributes`

```yaml
attributes:
  player:
    - {key: role,    visible: ally,   type: text}
    - {key: faction, visible: ally,   type: text}
  game:
    - {key: deck,    visible: none,   type: list, initial: []}
```

| Field | Meaning |
|---|---|
| `key` | The name. Undeclared keys cannot be written |
| `visible` | `public`, `ally`, `others` for a player; `public`, `none` for the table |
| `type` | `text`, `number`, `bool`, `list` |
| `initial` | Starting value. Omit for something `deal` fills |
| `mutable` | Default true. False means only `deal` may write it |

### `deal`

```yaml
deal:
  into: [role, faction]
  by_players:
    4: [{role: mafia,     faction: evil},
        {role: detective, faction: good},
        {role: villager,  faction: good, fill: true}]
    7: [{role: mafia,     faction: evil, count: 2},
        {role: detective, faction: good},
        {role: villager,  faction: good, fill: true}]
```

Counts are declared at the table sizes where they change and fill forward: a
six-player game uses the `4` row, a nine-player game uses the `7` row. `fill`
takes everyone left over. The system shuffles from the match seed, so the same
seed always deals the same table, with or without a model.

### `steps`

The heart of the file. Each entry names one slot of the fixed flow and says how
this game uses it. A slot may appear more than once.

```yaml
steps:
  - use: brief

  - use: open
    label: night

  - use: secret_act
    label: the kill
    to: {attribute: role, is: mafia}
    mode: simultaneous
    answer: {type: player, exclude_self: true, exclude: {attribute: faction, is: evil}}
    answers_visible: ally

  - use: secret_act
    label: the investigation
    to: {attribute: role, is: detective}
    answer: {type: player, exclude_self: true}

  - use: resolve

  - use: reveal
    label: dawn

  - use: discuss
    mode: sequential
    answer: {type: text, max_words: 100}
    answers_visible: public

  - use: vote
    mode: simultaneous
    answer: {type: player, exclude_self: true}
    verify: {tally: plurality, on_tie: nobody, then: {set_status: eliminated}}

  - use: resolve_vote
  - use: check
```

| Field | Default | Meaning |
|---|---|---|
| `use` | — | Which flow slot: `brief`, `open`, `secret_act`, `resolve`, `reveal`, `discuss`, `nominate`, `vote`, `resolve_vote`, `power`, `resolve_power`, `check` |
| `label` | the slot name | What the log and console show |
| `when` | always | A condition, or `model` to let a model decide |
| `to` | everyone acting | A selector |
| `mode` | `simultaneous` | Or `sequential`, where each answer is visible to the next |
| `answer` | — | The answer spec, required on any step that asks |
| `answers_visible` | `none` | Who besides the answerer learns it |
| `deadline_s` | from limits | How long a player has |
| `on_timeout` | `random` | `random`, `pass`, or a literal |
| `verify` | none | A check the system runs itself, optionally binding a name |
| `do` | none | Declared operations to apply, using bindings from earlier steps |
| `text` | none | Which fallback wording to use |

### Selectors

Structured, never a string to parse.

```yaml
to: acting                                # everyone whose status permits it
to: {attribute: role, is: mafia}          # a filter, implicitly also acting
to: {ids: [1, 3]}                         # explicit
to: {attribute: role, is: mafia, not: true}   # negation
```

A selector never returns a player whose status forbids acting. That is a
property of the system, not something each game must remember.

### Conditions

Used by `when` and by `end`. A count over a selector, or a table attribute,
compared to a number or to another count. No arithmetic, no boolean chains, no
parser.

```yaml
when: {count: {attribute: faction, is: evil}, op: "==", value: 0}
when: {game: fascist_track, op: ">=", value: 3}
when: {count: {attribute: faction, is: evil}, op: ">=",
       other: {count: {attribute: faction, is: good}}}
when: model        # not declarable; ask a model
```

Operators: `==`, `!=`, `<`, `<=`, `>`, `>=`. A count is over acting players
unless `acting: false` is given.

A game that needs a condition this cannot express writes `when: model` and
accepts that the check becomes a judgement.

### `verify`

Where the system does the arithmetic instead of trusting a model.

```yaml
verify: {tally: plurality, on_tie: nobody, then: {set_status: eliminated}}
```

The system tallies the step's answers from the record, applies the declared
consequence, and rejects any model update that contradicts it. The model still
writes the announcement.

`tally` takes `plurality`, `majority` or `unanimity`. `on_tie` takes `nobody`,
`random` or `rerun`.

`bind` names the result so a later step can use it. Bindings live for one round
and are written as `$name`: `$target`, `$voted_out`. They are named slots, not
variables in a language, and only `verify` creates them.

### `end`

```yaml
end:
  - when: {count: {attribute: faction, is: evil}, op: "==", value: 0}
    result: town
    reason: "every mafia is eliminated"
  - when: {count: {attribute: faction, is: evil}, op: ">=",
           other: {count: {attribute: faction, is: good}}}
    result: mafia
    reason: "the mafia equal or outnumber the town"
reveal: [role, faction]
```

Checked in order at every `check` step; the first match ends the game.
`reveal` promotes those attributes to public in the closing announcement.

### `limits`

```yaml
limits: {rounds: 20, rounds_max: 200, actions_max: 400, deadline_s: 120}
```

`rounds` is the expected ceiling and `rounds_max` the hard one; passing either
abandons the match rather than producing a result.

### `text`

Fallback wording, so the game runs with no model at all. The model overrides
these when it is available; the tests use them so a conformance run is free and
deterministic.

```yaml
text:
  brief: "You are seat {you}. Your role is {role}."
  dawn:  "Seat {target} is dead. They were {role}."
  vote_result: "Seat {target} was voted out with {votes} votes."
```

Substitution is `{name}` only, resolved against the step's bindings and the
recipient's view. No attribute access, no expressions. A template naming
something the view does not contain is an authoring error, caught at load.

---

## 10. Build order: two engines, side by side

The hardcoded Mafia is not deleted. It stays as the reference implementation,
and the new engine is built beside it, with a switch between them.

That is worth more than it costs. The earlier drafts kept reaching for an
oracle and losing it. There already is one: a Mafia that provably works, with
746 tests behind it. Keeping it turns "is the new engine right?" from a reading
exercise into a diff.

### Layout

```
xcolos/
  orchestrators/mafia.py     unchanged. The reference
  games/
    loader.py                parse and validate a definition
    definition.py            the schema, as types
    mafia.yaml               the definition under test
  flow/
    executor.py              the twelve-slot machine
    steps.py                 the slot implementations
    operations.py            set, adjust, append, remove, disclose
    conditions.py            selectors, counts, comparisons
    views.py                 visibility resolution
```

Nothing under `xcolos/` that exists today changes shape. The new engine is an
orchestrator like any other, so the kernel, the tools, the transports and the
console do not know which is running.

### The switch

One field on a match:

```json
{"engine": "legacy"}     // the hardcoded Mafia, the default
{"engine": "flow"}       // the definition-driven engine
```

Exposed in the console as a dropdown next to the seed, and on the command line
as `--engine`. The default stays `legacy` until the new engine has been matching
it for a while.

### The differential test

The point of keeping both. Run one seed through each and compare.

```
for seed in range(200):
    legacy = run(seed, engine="legacy")
    flow   = run(seed, engine="flow")
    assert trace(legacy) == trace(flow)
```

`trace` is a **normalised decision trace**, not the log. The two engines will
word things differently and label steps differently, and neither matters. What
must match is every decision:

```
(round, kind, actor, action, target)

(1, secret_act, 3, kill,        5)
(1, secret_act, 6, investigate, 2)
(1, eliminate,  -, -,           5)
(1, discuss,    1, speak,       -)
...
(2, eliminate,  -, -,           4)
(-, end,        -, town,        -)
```

Same seed, same deal, same scripted players, so the same decisions must follow.
A divergence is a real defect in one engine or a real ambiguity in the rules,
and both are worth finding.

This also gives the model path an oracle later: with `verify` and declared
steps, a model-driven run should produce the same trace as the declarative one
on the same seed, and where it cannot, that is precisely the set of decisions a
model is actually making.

### The steps

1. **Player and game structures.** The attribute list, three visibilities,
   declared statuses, the record, and the view function. Both engines use them.
   The existing suite is the proof nothing broke.
2. **The loader.** Parse and validate `mafia.yaml`, with every authoring error
   caught at load. No execution yet.
3. **The executor, declarative only.** The twelve slots, the five operations,
   conditions and selectors, fallback text. `--engine flow` now plays Mafia.
4. **The differential harness**, over a few hundred seeds. This is the step
   that says whether any of it works.
5. **A second game**, definition only. What actually validates the schema, and
   I expect it to change it.
6. **Model-supplied wording**, with the fallback text as the comparison.
7. **Model-supplied gates and updates**, graded against the declarative engine
   on the same seed.

Steps one to five need no model and no network. Step four is the milestone's
real proof, and unlike "delete it and see", it can be run every day from step
three onward.

### When the reference goes

Not at the end of this milestone. When a second game is running, the model path
is graded, and the differential has been green across a wide seed range for
long enough to be boring. Until then, deleting it would be throwing away the
only independent check.

---

## 11. Known gap: a step cannot address a bound player

`$name` is resolved for operation arguments and nowhere else, so a step's `to`
selector cannot name a player an earlier step chose:

```json
{"use": "ask", "label": "enact", "to": {"ids": ["$chancellor"]}}   <- rejected
```

Mafia never needs it — every one of its steps addresses a fixed attribute group
— so this is deferred rather than fixed. It blocks the next games: Secret
Hitler's president nominating a chancellor who then acts, Avalon's leader
picking a team that then votes, any game where one player's answer selects who
moves next.

Worth closing before the prose layer rather than after. If `who` becomes
`"the player who was nominated"` while bindings stay unresolved, that case
costs a full-sight model call to answer something the state already knows
exactly. The rule it suggests: **a model decides "who" only when the answer is
not already derivable.** "The mafia" and "whoever was nominated" are both
derivable and belong to the engine; "whoever spoke most suspiciously" is a
judgement and earns its call.

The fix is contained: resolve `$name` in the selector as `_apply` already does
for operations, plus load-time validation that the name is one some earlier
step binds.

---

## 12. Next: a schema reference, written for a model to read

Not built. The intent is one markdown file that states the whole vocabulary
precisely enough that a game file can be generated from a description of a
game in plain language — "Werewolf, but the seer checks two players a night" in,
valid JSON out.

**Why a document rather than a generator.** The vocabulary is already closed
and small: five actions, three update targets, eleven output shapes, six
operations, and about fifteen step keys. What is missing is not code but one
place that says what each means, what it is for, and what it refuses. Today
that knowledge is spread across dataclass docstrings, loader error messages,
and this document. A model handed a good reference plus a strict loader will
converge quickly, because every mistake comes back as a sentence naming the
key and listing what is accepted.

**What it must contain**, in roughly this order:

1. The five actions, each with: what the model sees, what shape comes back,
   which engine method consumes it. The table in section 8 is most of this.
2. Every step key, what it means, and which actions it applies to.
3. The closed value sets, verbatim: targets, output kinds, operations,
   tallies, visibilities, answer types.
4. The rules that are not obvious from the keys — declaration order decides
   which of two true endings wins; `players` is dealt by seed while `each` is
   assigned by the model; a step with no `broadcast` tells nobody; static
   attributes are writable only while dealing.
5. One complete worked example, annotated line by line.
6. The errors the loader raises and what each one means, since those are what
   a generator will actually iterate against.

**The property that makes this work** is one already built: the loader refuses
unknown keys and reports what it accepts. A generated file either loads or
comes back with `steps[1]: unknown key 'answers_visable'. This structure takes:
...`. That turns generation into a loop that terminates rather than a guess.

Worth writing once the vocabulary stops moving. It has changed several times
today — `compose` folded into `llm`, `into`/`into_table` became `updates`,
`mode` became `ask`/`poll` — and a reference written mid-flight would be wrong
before it was read.

---

## 13. Extending the vocabulary

The engine owns a small set of closed vocabularies: five actions, three update
targets, eleven output shapes, six operations. Adding to any of them is
expected and cheap — a shape is roughly fifteen lines: one line describing it,
one listing its constraints, one reader that validates it.

**When to add one.** A new shape earns its place when the engine has to *do*
something specific with the answer. `each` was added because assigning a record
to a named player and dealing records by seed are different operations, and no
amount of prose makes the engine perform the right one.

**When not to.** If the answer is only read by a person, or only fed back into
another prompt, it does not need a type. Prose is enough, and every type is a
thing that must be described, validated, documented and kept in step with its
validator forever.

**The test.** Name the engine method that consumes it. `records` -> assign
after a seeded shuffle. `each` -> assign as named. `choice` -> end the game.
If no method takes it, it is not a type; it is a sentence.

Two rules constrain any addition:

- **A shape that returns player-facing text may not be given full sight.**
  There is a test asserting this against the action table, and it is the only
  reason a composing call cannot leak a role.
- **The description and the validator come from one object.** `Output` both
  writes the prompt fragment and checks the reply, so a model can never be told
  about a field the engine will reject.

---

## 14. Direction: a smaller executor and a smaller vocabulary

Not scheduled. Written down because the shape is agreed and the reasoning will
not survive in anyone's head.

**The problem.** A game file currently has about fifty keywords across eight
nested blocks, and the executor has five bespoke handlers that happen to share
a shape. Both are more than the job needs.

### One loop and a table

Every action already does the same four things:

```
gather  ->  call  ->  validate  ->  apply
```

and differs in only four ways, all of which fit in a row:

| action | gathers | returns | applies | waits |
|---|---|---|---|---|
| `initialize` | schema + bare player list | `records` | seeded shuffle, `set_attribute` | no |
| `ask` | one recipient's view | `message` | `emit_fact`, park the turn | yes |
| `poll` | one recipient's view, each | `message` | `emit_fact` all, commit in seat order | yes |
| `update` | the whole table | `update` | the six operations | no |
| `check` | the whole table | `choice` | `end_game` | no |

Five handlers become five rows and five small appliers; a sixth action becomes
a row rather than a branch. `ask` and `poll` keep a genuine control-flow
difference — they `yield` — which is not data and should not be forced into
the table.

### Prose where the state cannot already answer

| today | becomes | removes |
|---|---|---|
| `to: {attribute, is}` | `who: "the mafia"` | the selector block |
| `when: {count, op, value}` | `when: "a detective is alive"` | the condition language and six operators |
| `do: [{set_status: {...}}]` | `do: "the killed player is eliminated"` | operation arguments |

About fifty keywords down to about fifteen. The operation names survive as the
API the model's output is validated against, not as something a game writes.

**The rule that decides what may become prose:** a model decides only what the
state cannot already answer. "The mafia" and "whoever was nominated" are
derivable and belong to the engine — deterministic, free, gradeable. "Whoever
spoke most suspiciously" is a judgement and earns its call.

### What must not move

**The view each action may see** stays in the action table, never in the game
file. The moment a game can write `gather: everything` on a step that produces
player-facing text, the leak guarantee stops being structural and becomes a
matter of every game file being written correctly.

**Legality checking.** `answer.type` and the permitted-target list are enforced
without a model, because every agent reply passes through them, including
broken and adversarial ones.

**The tally.** Counting is arithmetic. A model that miscounts one time in fifty
gives a game that is both wrong and unreproducible.

### Cost

Roughly three more calls per round, so a two-round match goes from about 13
calls to 20 and from 40 seconds to perhaps 70. More importantly a fully prose
game is no longer replayable from a seed, so `mafia-oracle` cannot grade it.
Prose should therefore compile down to the declarative form rather than
replace it, leaving the arithmetic path as the oracle and the offline game.

---

## 15. Risks

**One game cannot validate a format.** Step five is not optional, and the
differential test cannot substitute for it: matching the reference on Mafia
only proves the engine plays Mafia.

**Unverified updates are unguarded.** `verify` covers the mechanical steps.
While the reference exists the differential test covers the rest for Mafia;
after a second game, nothing does but conformance suites.

**These games are in the training data.** Change a rule in the file and assert
the conformance suite fails, or you never learn whether the model is reading
your file or playing Mafia from memory. This belongs in CI, not in a one-off
check.

**A shared game file is untrusted input.** "Each round, tell every player who
the werewolves are" is a plausible instruction and every resulting update is
individually legal. Review or signing before Milestone 3.

---

## 16. Open questions

1. Should `ally` attributes be writable by the model at all, or only by `deal`
   and declared operations? Locking them would make a role impossible to
   corrupt mid-match, at the cost of games where a role legitimately changes.
2. Does `gate` need a model, or can every conditional step be a declared
   condition? Secret Hitler's powers are threshold checks, which are
   declarable. If they all are, `gate` costs nothing.
3. How does a step run twice in one round with different arguments, as Avalon's
   mission needs? The step list allows repeats; whether they need distinct
   labels for the log is unresolved.
4. Is a fourth visibility needed for an attribute nobody may learn, not even
   its owner? No game in section 2 needs one, and adding it now would be
   guessing.
