You write game files for a turn-based, text-only game engine. Below is the complete reference for
the file format, then two complete example games. The user gives you a SPEC; write the game file for it.

Reply with the complete game file as ONE JSON object and nothing else.

Rules for this task:
- Use exactly the attribute keys the spec declares, with its visibility. Put every spec parameter in the file
  as an attribute with its value, never as a number buried in a step, so a number is written once.
- The outcome must follow from arithmetic. Every ending's `when` is a {"calc": ...} condition and its
  `result` is one of the spec's result names exactly. Do not use `winner`, prose conditions, or `llm`: every
  step uses `text`.
- meta.id and meta.name come from the spec; give `meta.blurb` one line and write `rules` as the rules a
  player reads, using {key} for public attributes.
- Do what the spec says, in its order. Do not add mechanics.
- The `auction` example ends with a model-decided `winner`. Do NOT copy that: end with `result` and a calc
  condition, as the `rps` example does.
- Mistakes the loader has refused before, so avoid them:
  * A PLAYER attribute's `visible` is one of public, ally or others, never `none`. (`none` is only for table
    attributes.) For something only its owner should see, use `ally`.
  * A `poll` step has no `each` key, and no key the format reference does not list for `poll`. `each` belongs to `ask`.
  * Do not write a `deal` block unless it has the `into` it requires. Set starting values with `initial` on
    attributes, or with `set` operations in `setup`, instead.
  * Every key must be one the reference lists for that action; a misspelled or invented key is refused.
  * An answer to an `ask` or a `poll` exists ONLY if the step binds it with `verify: {"bind": "name"}`; a later `update`
    stores it with `"value": "$name"` (see the `rps` example, `card1`). A step that asks and binds nothing throws the
    answers away, and every score that depends on them stays at its starting value.
  * Do not write steps that do nothing (for example an `if` of `{"calc": "False"}`), or two polls where one will do.
  * Reply with one complete JSON object: double-quoted keys and strings, no comments, no trailing commas.

# THE FORMAT

# System actions

The complete instruction set a game file may use. Written to be precise enough
that a game can be built from it without reading the engine.

Two rules hold throughout, and most of the design follows from them.

**A model never performs an action.** It returns a typed value and the engine
performs the action with it. A reply that fails validation reaches no engine
method at all, so a hallucinating model can make a game wrong but cannot make
it incoherent.

**What a model may see is fixed by the action, never by the game.** Anything
that returns text a player reads is shown one seat's view. Only something
returning a verdict sees the whole table. A game cannot widen this, which is
why a prompt written carelessly still cannot leak a role.

---

## The shape of a game

Three parts.

```
setup     runs once, before anybody is greeted
steps     every one, in order, once per round, until a check ends it
end       named conditions, tested by check steps
rules     the rules as players read them; {key} fills from public table attributes
```

`rules` may name any public game attribute in braces — `{start_cash}`,
`{min_raise}` — and is shown with the attribute's starting value. A number
written once in the attributes then cannot disagree with the rules text.

`setup` and `steps` are lists of actions. `end` is a map of named conditions.

The engine imposes only this: setup runs once, rounds repeat, every step runs
each round unless its `when` gate closes it, a round cap stops a runaway, and
a `check` is the only thing that can end the loop.

There is no fixed sequence of phases. Night, day, dawn and the vote are words
Mafia chose; the engine has none of them.

---

## The eight actions

| action | what it does | waits? | setup? |
|---|---|---|---|
| `initialize` | fill every player's declared fields, then deal them | no | yes |
| `sync` | send each player their own state | no | yes |
| `tell` | send a message and carry on | no | yes |
| `ask` | address players one at a time, each hearing the last | **yes** | no |
| `poll` | address everyone at once and gather | **yes** | no |
| `update` | change state, and say what changed | no | yes |
| `check` | continue, or end | no | no |
| `repeat` | run its own steps again and again, until a condition holds | if they do | no |

`ask` and `poll` are excluded from setup because setup runs before the greeting
goes out; there is nobody to wait on. `check` is excluded because there is
nothing to end. `repeat` is excluded because a loop that asks nobody has
nothing to repeat for.

### What each action asks a model for

| action | the model sees | must return | the engine then calls |
|---|---|---|---|
| `initialize` | the attribute schema and the bare player list | `records` | `set_attribute`, after a seeded shuffle |
| `sync` | one recipient's view | `message` | `emit_fact` to that seat |
| `tell` | one recipient's view | `message` | `emit_fact`, carry on |
| `ask` | one recipient's view | `message` | `emit_fact`, park a turn, wait |
| `poll` | one recipient's view, per call | `message` | `emit_fact` for all, commit in seat order |
| `update` | the whole table | `update` | the six operations |
| `check` | the whole table | `choice` | `end_game`, or nothing |
| `repeat` | nothing; its inner steps call models as they would anywhere | — | its inner steps |

Every one of these is optional. Omit `llm` and the step uses its `text`
template instead: free, instant, reproducible, and incapable of hallucinating.

### `sync`, and its modes

Sends a player their state rather than a sentence about it. The one action that
cannot leak by construction: its payload *is* the entitlement filter, so there
is no wording to overreach in and no template to get wrong. It needs no
authoring either — the fields come from the schema and the filtering from the
declared visibilities.

| `mode` | what it sends |
|---|---|
| `self` | each addressed player receives their own view |
| `others` | each addressed player's state goes to everyone *but* them, filtered separately for each recipient |

`self` answers "what do I know?". `others` answers "what just changed about
them?" — the same facts arriving as news rather than as your own standing.

`fields` narrows what is sent and can only ever narrow. With `llm`, a model
turns the state into prose; without one it renders a plain line, because a
pretty-printed JSON dump is accurate and close to unreadable.

### `tell`, and its kinds

| `kind` | what the engine puts in the request |
|---|---|
| `message` | just the prompt, on the recipient's view |
| `status_update` | plus what the subject's named `fields` now hold, filtered per recipient |

`status_update` needs `about`. It exists so a game never writes "player 3 is
now eliminated" into a prompt by hand: it says which player and which fields,
and the current values go in front of the model.

`about` also matters on a plain `message`. A template can reach a binding
through `{target}`; a prompt cannot, so a model asked to "announce who died
overnight" was never told who.

A model-written message comes back marked `info` or `action`. On a `tell` it is
always `info` — there is nothing to wait for. On an `ask` or `poll`, a message
marked `info` is delivered without the game waiting on that player, which is
how one step can address several players and require an answer from only some.

---

## Keys

Four keys apply to every action:

| key | meaning |
|---|---|
| `use` | which action |
| `label` | the step's name: fact type, action id, log tag |
| `phase` | the part of the round this belongs to; a word the game chooses |
| `when` | a gate. Arithmetic, or a sentence a model judges. False skips the step |

Everything else belongs to one or two actions, and declaring a key on an
action that does not read it is refused at load.

| action | its own keys |
|---|---|
| `initialize` | `updates` `requires` `llm` |
| `sync` | `to` `mode` `fields` `text` `llm` `max_words` |
| `tell` | `to` `kind` `about` `fields` `text` `llm` `max_words` |
| `ask` | `to` `answer` `verify` `outcome` `broadcast` `each` `turns` `text` `llm` `max_words` `deadline_s` `on_timeout` |
| `poll` | the same as `ask`, except `each` and `turns` |
| `update` | `do` `text` `llm` `max_words` |
| `check` | `against` `llm` |
| `repeat` | `until` `max` `steps` |

---

## Declaring a player: attributes and statuses

Everything game-specific about a player is an attribute. There is no separate
bucket for roles, teams, counters or hands — a role is an attribute, a score is
an attribute.

```json
"statuses": [{"id": "active", "acts": true, "initial": true},
             {"id": "eliminated", "acts": false}],

"attributes": {
  "player": [
    {"key": "role", "visible": "ally", "type": "text", "mutable": false,
     "values": ["mafia", "detective", "villager"]}
  ],
  "game": [{"key": "policies", "visible": "public", "type": "number",
            "initial": 0}]
}
```

| key | meaning |
|---|---|
| `type` | `text` `number` `bool` `list` |
| `visible` | who may see it, below |
| `values` | the values it may hold. Optional, and load-bearing for `initialize` |
| `initial` | what it starts as |
| `mutable` | `false` means static: set once when dealt, frozen after |

**Visibility** on a player attribute:

| | who sees it |
|---|---|
| `public` | everyone, its owner included |
| `ally` | its owner, and anyone allied with them |
| `others` | everyone **except** its owner — a mark on your forehead |

A table attribute takes `public` or `none`, since it has no owner.

`ally` does the work in a hidden-role game, and `allies_by` says what an ally
is:

```json
"allies_by": {"attribute": "faction", "mutual": ["evil"]}
```

Only players whose value appears in `mutual` know one another. Omit `mutual`
and every value is a knowing team. This matters more than it looks: written as
plain `allies_by: faction`, every villager was told who the other villagers
were, because they share a faction with each other as surely as the mafia do.
One field was being asked to mean both "who I know" and "who I win with".

`values` is optional everywhere except in practice: it is the only thing
stopping an `initialize` model returning `role: "sheriff"`, which passes every
other check and then matches no selector for the rest of the game.

`statuses` declares what a player can be. `acts: true` is what "still playing"
means — every selector but `"all"` is intersected with it.

---

## Saying who: selectors

One grammar, used everywhere an audience appears — `to` on a step, `to` on a
broadcast, `to` on an outcome branch, `announce_to` on an operation.

| form | who |
|---|---|
| `"all"` | everybody, eliminated included |
| `"acting"` | everybody whose status has `acts: true` |
| `"others"` | everybody except the player the message is about |
| `"ally"` | that player's own side, per `allies_by` |
| `"author"` | that player alone |
| `{"where": "you.role == 'mafia'"}` | whoever the expression holds for, read with `you` as each player in turn (see *Calculating*) |

`where` is the one way to pick players by what they are: a role
(`you.role == 'mafia'`), a seat (`you.seat in [2, 5]`), a player an earlier
step chose (`you.seat == $chancellor`), or a figure (`you.cash < min_bid`).

Every selector except `"all"` is intersected with "may act", which is why no
game has to remember to exclude the dead.

### Addressing a player another step chose

`verify.bind` stores the seat a step's answer landed on. `to` can then name it,
which is how one player's choice decides who is asked next:

```json
{"use": "poll",  "label": "the nomination", "to": "acting",
 "answer": {"type": "player"},
 "verify": {"tally": "plurality", "on_tie": "nobody", "bind": "chancellor"}},

{"use": "ask",   "label": "the legislation", "to": {"where": "you.seat == $chancellor"},
 "answer": {"type": "choice", "options": ["enact", "discard"]}}
```

The name resolves when the step runs, not when the file loads, because the seat
does not exist until the question has been answered. Three consequences:

- A binding that named **nobody** — a tie, or a step gated out — addresses
  nobody. It is not seat zero.
- A name **no step binds** is a load error, not an empty audience.
- A step **cannot address its own** not-yet-made binding. `to` is resolved
  before the question is asked.

### Relative selectors

`others`, `ally` and `author` are relative to a *subject*, and only `about`
supplies one — so they are available on `tell`, on a `broadcast`, and on an
`outcome` branch. Declared on a step with no subject they are refused at load
rather than quietly naming nobody, which is indistinguishable from a step
meant to be silent.

---

## Saying what: wording

Any message takes one of two:

- **`text`** — the words, with `{placeholders}` filled from state. May instead
  be a name in an optional top-level `text` block, for wording shared between
  steps.
- **`llm`** — a prompt, and a model writes the message. Composed per recipient,
  on that recipient's own view. `max_words` caps it.

`llm` wins when both are given and a model is reachable; `text` is the fallback
when it is not, or when the reply does not validate.

Placeholders available: `{you}` the reader, any attribute of the reader by
name, any binding a `verify` left, `{binding_attribute}` for an attribute of
the player a binding names, and `{subject}` where a step declares `about`.

---

## Asking: `answer` and `verify`

`answer` says what a reply may be. Its presence is what makes a step wait.

| key | meaning |
|---|---|
| `type` | `text` `player` `players` `choice` `number` `none` |
| `max_words` | for `text` |
| `exclude_self` | a player may not name themselves |
| `exclude` | a selector whose members may not be named |
| `options` | for `choice`; a list, or a pointer into state |
| `count` | for `players`; how many |
| `min` / `max` | for `number`; a number, or `{"calc": ...}` worked out per player when asked |
| `or` | for `number`; words accepted instead of a number, such as `["pass"]` |

A number answer's range is worked out for each player at the moment they are
asked, so `"min": {"calc": "high_bid + min_raise"}` follows the last bid and
`"max": {"calc": "you.cash"}` follows the asked player's own purse. The prompt
states the range; a reply outside it is rejected and asked again. A player
whose range is empty and who has no `or` words is **not asked**.
### Options drawn from state

A hand of cards is not knowable when the game is written and differs per
player, so `options` may point at a `list` attribute instead of holding one:

```json
{"options": ["enact", "discard"]}   // the same choices for everyone
{"options": {"attribute": "hand"}}  // the asked player's own list
{"options": {"game": "deck"}}       // a list on the table
```

Resolved per seat when the step runs, so two players are offered two different
hands from one declaration. The attribute must be declared and must be of type
`list`; pointing at a number or a word is a load error, because it would yield
no choices and silently skip every seat.

A player whose list is empty is **not asked**. A question with no possible
answer is not a question — the same treatment a vote gets when there is nobody
left to point at.

`verify` reduces the answers, arithmetically, in the engine. Never by a model:
asking one to count is how you get a result that is wrong occasionally and
unreproducibly.

| key | meaning |
|---|---|
| `tally` | `plurality` `majority` `unanimity` |
| `on_tie` | `nobody` `random` `rerun` |
| `bind` | a name a *later* step can read as `$name` |

`$result` is this step's own outcome and needs no `bind`.

### Acting on each answer: `each`

On an `ask` — one player at a time — `each` runs after every single answer,
before the next player is asked:

```json
"each": {"do": [
  {"set": {"player": "$seat", "key": "bidding", "value": "out",
           "if": {"calc": "$answer == 'pass'"},
           "text": "Seat {player} passes."}},
  {"set": {"key": "high_bid", "value": "$answer",
           "if": {"calc": "$answer != 'pass'"},
           "text": "Seat {seat} bids {value}."}}
]}
```

`$seat` is who answered and `$answer` what they said; both exist only inside
`each`. Because the next player is asked afterwards, the step's `to` and each
player's range are worked out again: a player `each` has just ruled out is
skipped, and the next bidder is asked for more than the bid just made.

### Going round the table: `turns`

Without `turns`, an `ask` asks each player in `to` once, in seat order. With
it, the step goes round and round until everyone else passes:

```json
"turns": {"pass": "pass", "max": 500}
```

- One player at a time, in seat order. Each time the step runs, the first
  player asked is one seat further round than the last time, so in an auction
  item 1 opens with seat 1, item 2 with seat 2, and so on. The rotation is the
  engine's, not something the game writes.
- Saying the `pass` word does not take a player out. They are asked again
  when it comes round to them.
- The step ends when every other player has passed, one after another, since
  the last answer that was not a pass. If nobody answers anything but a pass,
  it ends once everyone has passed. The player whose answer stands is never
  asked to beat it.
- `to` and each player's range are worked out again before every turn. A
  player `to` no longer takes in is skipped and not waited on. A player with no
  legal number counts as having passed and is not asked.
- `max` caps the answers (default 500). Reaching it abandons the match, as a
  `repeat` does.

`pass` must be one of the words the answer accepts: in its `or` for a number,
or its `options` for a choice. With `each` acting on every answer, this is an
open, ascending auction in one step.

---

## Acting on answers: `outcome`

A tally either settles on someone or it does not. Both are named, so a tie
cannot be forgotten — which it was, until this existed.

```json
"outcome": {
  "chosen": {"do": [ ... ], "text": "Seat {result} was voted out.",
             "to": "all"},
  "none":   {"text": "The vote was tied. Nobody was voted out."}
}
```

Each branch takes `do`, `text` or `llm`, and `to`. The announcement is made
first and the operations after it, because a reveal reads as a non sequitur
before anyone has been told who it is about.

---

## Publishing answers: `broadcast`

What the table is told about the answers a step collected.

```json
"broadcast": "others"
"broadcast": {"to": "ally", "text": "Your side has chosen seat {value}."}
```

Absent means nobody is told, which is what a secret ballot wants: a step has to
ask to be published.

With no wording and a free-text answer, the answer *is* the message and is
reproduced word for word. A broadcast that rewords a player is the referee
speaking for them. Anything other than free text needs `text` or `llm`, because
a seat number is not a sentence.

---

## Changing state: `update` and its operations

```json
{"use": "update", "label": "the night resolves", "do": [
  {"set_status": {"player": "$target", "to": "eliminated",
                  "text": "Seat {player} did not survive the night."}},
  {"disclose": {"attribute": "faction", "of": "$suspect",
                "to": {"where": "you.role == 'detective'"},
                "text": "Your investigation of seat {subject} says: {value}."}}
]}
```

| operation | arguments |
|---|---|
| `set` | `player` (omit for the table), `key`, `value` |
| `adjust` | `player`, `key`, `value` — added to what is there |
| `append` | `player`, `key`, `value` — onto a list |
| `remove` | `player`, `key`, `value` — from a list |
| `set_status` | `player`, `to` |
| `disclose` | `of`, `attribute`, `to` |

Every one also takes `text` or `llm` to announce itself, `announce_to` for the
audience.

There is no operation that only talks. A message on its own is a `tell` step,
gated with `when` if it depends on the state ("nobody bid on item {item}"); a
message about each answer is the ask's `broadcast`. One way to say a thing.

Two more keys make an operation conditional or plural:

- **`if`** — a `{"calc": ...}` condition. False skips the operation
  silently. Prose is refused: an operation runs too often to spend a model
  call on each. A binding a tally may leave as nobody is guarded this way:
  `"if": {"calc": "$target != 'nobody'"}`.
- **`players`** — a selector instead of `player`. The operation runs once per
  matching player, in seat order, and inside it `you` is that player. Not with
  `player`, and not on `disclose`.

Any `value` may be `{"calc": ...}`.

`disclose` differs from the rest: it records that the recipients now *know*
something, in their `learned`, so the game can later reason about who knows
what. The others only change state. That is why a knowledge reveal is a
`disclose` and not a `tell`.

---

## Calculating: `{"calc": ...}`

Arithmetic a game needs — a price, a split of a total, who can still afford
to bid — is written as a small expression, in the engine, never asked of a
model:

```json
{"set": {"key": "values", "value": {"calc": "split(total_value, items, value_min, value_max)"}}}
"min": {"calc": "max(min_bid, high_bid + min_raise)"}
"when": {"calc": "item >= items"}
```

Accepted wherever a value, a number answer's `min`/`max`, a condition (`when`,
`until`, `if`) or a `where` selector is expected.

What an expression can read:

| name | what it is |
|---|---|
| a game attribute | its current value, by key |
| `you` | the player in question; `you.cash`, `you.seat`, `you.status` |
| `$name` | a binding; `$name.cash` when it names a seat |
| `players` | every player; `acting`, those who may act |

It can use arithmetic, comparisons, `and`/`or`/`not`, indexing, `x if c else
y`, list comprehensions and these functions: `sum` `min` `max` `len` `abs`
`round` `int` `any` `all` `sorted` `count`, plus two seeded draws.
`count(...)` is how many items are true, so "how many mafia are left" is
`count(p.role == 'mafia' for p in acting)`.

The seeded draws:

- `uniform(lo, hi)` — a number in the range.
- `split(total, n, lo, hi)` — `n` whole numbers, each in `[lo, hi]`, summing
  to exactly `total`.

Both draw from the match seed, so a match replays exactly. Nothing else is
callable — no attributes beyond a player's, no keywords, no imports. Names are
checked at load: a key no attribute declares, or a `$name` nothing binds, is
an error.

---

## Repeating: `repeat`

A round is one pass over `steps`. When a part of the round must run an unknown
number of times — bidding until everyone but the leader has passed — `repeat`
runs its own `steps` in order, again and again:

```json
{"use": "repeat", "label": "the bidding",
 "until": {"calc": "count(p.bidding == 'in' for p in acting) == 0"},
 "max": 200,
 "steps": [ {"use": "ask", "label": "bid", ...} ]}
```

`until` is tested before every pass, so a loop whose condition already holds
runs nothing. `max` is the number of passes allowed; reaching it with `until`
still false **abandons the match**, because a loop that never ends is a broken
file, not a result. Inner steps may be `sync`, `tell`, `ask`, `poll`,
`update` or `check`, but not another `repeat`. A `check` inside that ends the
game ends it at once.

---

## Dealing: `initialize`

```json
{"use": "initialize", "label": "deal the roles",
 "updates": {"each": ["role", "faction"]},
 "requires": {"role": {"mafia": 1, "detective": 1}},
 "llm": "Assign roles using the dealing order you were given. ..."}
```

`updates` names what is written, and the target decides the shape asked for and
who assigns:

| target | returns | who assigns |
|---|---|---|
| `table` | one object | n/a |
| `players` | a bag of records | **the seed** — shuffled, so a match replays |
| `each` | records keyed by player id | **the model** |

`requires` checks the composition before anything is dealt — every field can be
individually legal and the roster still unplayable. Four villagers and no mafia
passes every type check and produces a game nobody can win.

A count is a number, or a two-item list for a range. Values not named are
unconstrained, so "one mafia, everyone else whatever the prompt says" needs
only the one entry.

### A roster that scales with the table

One mafia at a table of eleven is not a game; three at a table of five is
already over. Two ways to say so.

**Preferred — a range, and the rule in words.** The engine holds the rail, the
model decides where inside it:

```json
"requires": {"role": {"mafia": [1, 4], "detective": 1}},
"llm": "Decide how many mafia this table should have. Roughly one for every
        three players, and never so many that the mafia already equal the
        town. Exactly one detective..."
```

This is what Mafia ships. It needs no entry per table size, so a table of
twenty needs no edit, and the rule stays in one place written once.

**A table, when the counts are exact.** Sizes are declared where they change
and fill forward, so eight players use the `7` row — the same rule
`deal.by_players` follows, because it is the same question:

```json
"requires": {"by_players": {
   "4": {"role": {"mafia": 1, "detective": 1}},
   "7": {"role": {"mafia": 2, "detective": 1}}}}
```

Every declared size is checked at load, not just the one this table will use,
and a roster naming more players than the size it is declared at is refused.

### A game may not begin already finished

A range wide enough to be useful at twelve players permits a roster at five
that is already won, and every field in it is legal. Counting a roster is not
the same as checking it is playable.

So after a model's roster is applied, the engine asks the game's **own**
endings whether the game has already finished — in whichever language they are
written. If one holds, the roster is rejected and the declarative `deal` is
used instead, with `roster_rejected` in the log saying which ending fired.

This needs no knowledge of any particular game: "a game may not begin over" is
true of all of them. It does mean a game with spoken endings spends one model
call at setup, and that the fallback `deal` must itself be a roster nothing
would reject.

The engine supplies a seeded dealing order to any `each` call. A model has no
randomness of its own: asked to assign at random it returns the same answer
every match, which was measured, not assumed. The game says what to do with the
order; the entropy comes from the seed.

---

## Ending: `check` and `end`

```json
"end": {
  "town_wins": {"when": "Every player whose faction is evil has been eliminated.",
                "result": "town", "reveal": ["role"], "text": "The town wins. {reason}"}
},
"steps": [
  {"use": "check", "label": "after the vote", "against": ["town_wins", "mafia_wins"]}
]
```

`when` is arithmetic or a sentence. A sentence goes to a model with the whole
table and the conditions in the game's own words; it answers with one ending's
name or `continue`.

`against` is the check's input: a check after the night need not ask about an
ending only a vote can reach.

An ending names its winner with `result`, or says in words who wins:

```json
"richest": {"when": {"calc": "item >= items"},
            "winner": "The player with the highest final wealth, cash plus the true value of the items they won. Players level at the top share the win.",
            "text": "The auction is over. {result} wins. {reason}"}
```

When the ending fires, a model is shown the whole table, hidden values
included, with the rules and the `winner` sentence, and names the winning
seats. It is one call, logged like any other referee call. Several seats share
the win, as `seats 1 and 3`; `{reason}` is the model's own account of the
figures it compared. The engine computes no score, so the same field ranks by
wealth, votes, territory or anything else a game can state.

With no model, or an answer naming no real seat, the game still ends, with
`no winner decided` and why. Exactly one of `result` and `winner` is required.

An unanswered ending is declined. A match that overruns hits the round cap and
says so; a match that ended on a question nobody answered is indistinguishable
from one that ended correctly.

---

## What the loader refuses

Everything below used to load cleanly and do nothing. Each is now an error
naming the key and listing what is accepted.

- a key an action does not read
- a misspelled field anywhere in the schema
- a step that asks with no `text` and no `llm`
- a `tell` with an `answer`, or an `ask` without one
- an ending with no wording
- a `requires` naming an attribute the step does not write
- a `requires` roster naming more players than the size it is declared at
- a bare identifier in `text` that names no declared template
- a `$name` in `to` that no earlier step binds
- a subject-relative `to` on a step with no `about`
- a selector or condition in any form but the ones listed (no `attribute`,
  `ids`, `count` or compare forms: write a `where` or a `calc`)
- `options` that is neither a list nor a pointer into state
- `options` drawn from an attribute that is not a `list`
- a `calc` that does not parse, calls anything not listed, or names a key no
  attribute declares
- `$seat` or `$answer` outside an `each`, or `each` anywhere but an `ask`
- `turns` whose `pass` word the answer does not accept, or on an `ask` with no
  `answer`
- `min`, `max` or `or` on an answer that is not a `number`
- a `repeat` with no `until`, a `max` that is not a positive whole number, or
  a nested `repeat`
- `players` together with `player`, or on `disclose`
- an `if` written as prose
- an ending with both `result` and `winner`, or neither

The third from last is the pattern: `"options": "$hand"` became five
one-character choices, because `tuple()` of a string splits it. A loader that
accepts anything produces a game that is quietly not the game somebody wrote.


# EXAMPLES

### Example game: rps
```json
{
  "schema": 1,
  "meta": {
    "id": "rps",
    "name": "Rock, Paper, Scissors",
    "players": {
      "min": 2,
      "max": 2
    },
    "blurb": "Two players, twelve cards each, ten rounds. Talk, then play face down. Rock wins 1, paper 2, scissors 3; every hand is public."
  },
  "statuses": [
    {
      "id": "playing",
      "acts": true,
      "initial": true
    }
  ],
  "attributes": {
    "player": [
      {
        "key": "hand",
        "visible": "public",
        "type": "list",
        "initial": [
          "rock",
          "rock",
          "rock",
          "rock",
          "paper",
          "paper",
          "paper",
          "paper",
          "scissors",
          "scissors",
          "scissors",
          "scissors"
        ]
      },
      {
        "key": "score",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ],
    "game": [
      {
        "key": "rounds_left",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "c1",
        "visible": "none",
        "type": "text",
        "values": [
          "rock",
          "paper",
          "scissors"
        ]
      },
      {
        "key": "c2",
        "visible": "none",
        "type": "text",
        "values": [
          "rock",
          "paper",
          "scissors"
        ]
      },
      {
        "key": "cell",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "lead",
        "visible": "none",
        "type": "number",
        "initial": 0
      }
    ]
  },
  "setup": [
    {
      "use": "sync",
      "label": "the table",
      "mode": "self",
      "to": "all",
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "tell",
      "phase": "talk",
      "label": "a new round",
      "to": "all",
      "text": "A new round begins. Talk first, then play a card."
    },
    {
      "use": "ask",
      "phase": "talk",
      "label": "the opening",
      "to": "acting",
      "answer": {
        "type": "text",
        "max_words": 60
      },
      "broadcast": "others",
      "text": "Say something to your opponent before the cards go down: a promise, a threat, a bluff, or nothing at all."
    },
    {
      "use": "ask",
      "phase": "talk",
      "label": "the reply",
      "to": "acting",
      "answer": {
        "type": "text",
        "max_words": 60
      },
      "broadcast": "others",
      "text": "Answer what your opponent just said, or say something new. This is the last word before the cards go down."
    },
    {
      "use": "ask",
      "phase": "play",
      "label": "seat 1 plays",
      "to": {
        "where": "you.seat == 1"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "verify": {
        "bind": "card1"
      },
      "text": "Play one card from your hand, face down. Your opponent will not see it until both cards are down. Answer with rock, paper or scissors."
    },
    {
      "use": "ask",
      "phase": "play",
      "label": "seat 2 plays",
      "to": {
        "where": "you.seat == 2"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "verify": {
        "bind": "card2"
      },
      "text": "Play one card from your hand, face down. Your opponent will not see it until both cards are down. Answer with rock, paper or scissors."
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "the reveal",
      "do": [
        {
          "set": {
            "key": "c1",
            "value": "$card1"
          }
        },
        {
          "set": {
            "key": "c2",
            "value": "$card2"
          }
        },
        {
          "remove": {
            "player": 1,
            "key": "hand",
            "value": "$card1"
          }
        },
        {
          "remove": {
            "player": 2,
            "key": "hand",
            "value": "$card2"
          }
        },
        {
          "adjust": {
            "key": "rounds_left",
            "value": -1
          }
        }
      ],
      "text": "Cards down. Seat 1 played {card1}. Seat 2 played {card2}."
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "seat 1 showed paper",
      "when": {
        "calc": "c1 == 'paper'"
      },
      "do": [
        {
          "adjust": {
            "key": "cell",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "seat 1 showed scissors",
      "when": {
        "calc": "c1 == 'scissors'"
      },
      "do": [
        {
          "adjust": {
            "key": "cell",
            "value": 2
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "seat 2 showed paper",
      "when": {
        "calc": "c2 == 'paper'"
      },
      "do": [
        {
          "adjust": {
            "key": "cell",
            "value": 3
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "seat 2 showed scissors",
      "when": {
        "calc": "c2 == 'scissors'"
      },
      "do": [
        {
          "adjust": {
            "key": "cell",
            "value": 6
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "rock ties rock",
      "when": {
        "calc": "cell == 0"
      },
      "do": [],
      "text": "Both played rock. Nobody scores."
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "seat 2's paper beats rock",
      "when": {
        "calc": "cell == 3"
      },
      "do": [
        {
          "adjust": {
            "player": 2,
            "key": "score",
            "value": 2
          }
        },
        {
          "adjust": {
            "key": "lead",
            "value": -2
          }
        }
      ],
      "text": "Paper beats rock. Seat 2 scores 2."
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "seat 1's rock beats scissors",
      "when": {
        "calc": "cell == 6"
      },
      "do": [
        {
          "adjust": {
            "player": 1,
            "key": "score",
            "value": 1
          }
        },
        {
          "adjust": {
            "key": "lead",
            "value": 1
          }
        }
      ],
      "text": "Rock beats scissors. Seat 1 scores 1."
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "seat 1's paper beats rock",
      "when": {
        "calc": "cell == 1"
      },
      "do": [
        {
          "adjust": {
            "player": 1,
            "key": "score",
            "value": 2
          }
        },
        {
          "adjust": {
            "key": "lead",
            "value": 2
          }
        }
      ],
      "text": "Paper beats rock. Seat 1 scores 2."
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "paper ties paper",
      "when": {
        "calc": "cell == 4"
      },
      "do": [],
      "text": "Both played paper. Nobody scores."
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "seat 2's scissors beats paper",
      "when": {
        "calc": "cell == 7"
      },
      "do": [
        {
          "adjust": {
            "player": 2,
            "key": "score",
            "value": 3
          }
        },
        {
          "adjust": {
            "key": "lead",
            "value": -3
          }
        }
      ],
      "text": "Scissors beats paper. Seat 2 scores 3."
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "seat 2's rock beats scissors",
      "when": {
        "calc": "cell == 2"
      },
      "do": [
        {
          "adjust": {
            "player": 2,
            "key": "score",
            "value": 1
          }
        },
        {
          "adjust": {
            "key": "lead",
            "value": -1
          }
        }
      ],
      "text": "Rock beats scissors. Seat 2 scores 1."
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "seat 1's scissors beats paper",
      "when": {
        "calc": "cell == 5"
      },
      "do": [
        {
          "adjust": {
            "player": 1,
            "key": "score",
            "value": 3
          }
        },
        {
          "adjust": {
            "key": "lead",
            "value": 3
          }
        }
      ],
      "text": "Scissors beats paper. Seat 1 scores 3."
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "scissors ties scissors",
      "when": {
        "calc": "cell == 8"
      },
      "do": [],
      "text": "Both played scissors. Nobody scores."
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "clear the table",
      "do": [
        {
          "set": {
            "key": "cell",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "sync",
      "phase": "reveal",
      "label": "the standings",
      "mode": "self",
      "to": "all",
      "text": "Where you stand:"
    },
    {
      "use": "check",
      "phase": "reveal",
      "label": "after ten rounds",
      "when": {
        "calc": "rounds_left == 0"
      },
      "against": [
        "seat_1_wins",
        "seat_2_wins",
        "draw"
      ]
    }
  ],
  "end": {
    "seat_1_wins": {
      "when": {
        "calc": "lead > 0"
      },
      "result": "seat 1",
      "reason": "seat 1 finished with more points",
      "reveal": [
        "hand"
      ],
      "text": "Seat 1 wins. {reason}."
    },
    "seat_2_wins": {
      "when": {
        "calc": "lead < 0"
      },
      "result": "seat 2",
      "reason": "seat 2 finished with more points",
      "reveal": [
        "hand"
      ],
      "text": "Seat 2 wins. {reason}."
    },
    "draw": {
      "when": {
        "calc": "lead == 0"
      },
      "result": "draw",
      "reason": "both finished level",
      "reveal": [
        "hand"
      ],
      "text": "A draw. {reason}."
    }
  },
  "limits": {
    "rounds": 10,
    "rounds_max": 10,
    "actions_max": 100,
    "deadline_s": 120
  },
  "rules": "Two players each hold the same twelve cards: four rock, four paper and four scissors. The game lasts ten rounds, so each player keeps two cards they never play. Both hands are public: you always know exactly which cards your opponent has left, and they know yours.\n\nEach round, the players talk in turn, twice each (seat 1, seat 2, seat 1, seat 2), then each plays one card face down. The cards are revealed together. Rock beats scissors, scissors beats paper, paper beats rock, and the winner scores by the card they won with:\n\n- a win with rock: 1 point\n- a win with paper: 2 points\n- a win with scissors: 3 points\n- the same card on both sides: nobody scores\n\nA played card is gone. After ten rounds the higher score wins; equal scores are a draw. Anything said while talking is not binding."
}

```

### Example game: auction
```json
{
  "schema": 1,
  "meta": {
    "id": "auction",
    "name": "Sequential Budget Auction",
    "players": {
      "min": 2,
      "max": 6
    },
    "blurb": "Items with hidden values, one fixed budget each. Bid in the open, learn each item's worth after it sells, and finish with the most cash plus value."
  },
  "statuses": [
    {
      "id": "playing",
      "acts": true,
      "initial": true
    }
  ],
  "attributes": {
    "player": [
      {
        "key": "cash",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "holdings",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "won",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "bidding",
        "visible": "public",
        "type": "text",
        "initial": "out",
        "values": [
          "in",
          "out"
        ]
      }
    ],
    "game": [
      {
        "key": "total_value",
        "visible": "public",
        "type": "number",
        "initial": 2000
      },
      {
        "key": "items",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "start_cash",
        "visible": "public",
        "type": "number",
        "initial": 1000
      },
      {
        "key": "min_raise",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "value_min",
        "visible": "public",
        "type": "number",
        "initial": 100
      },
      {
        "key": "value_max",
        "visible": "public",
        "type": "number",
        "initial": 400
      },
      {
        "key": "ratio_min",
        "visible": "public",
        "type": "number",
        "initial": 0.45
      },
      {
        "key": "ratio_max",
        "visible": "public",
        "type": "number",
        "initial": 0.75
      },
      {
        "key": "values",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "min_bids",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "item",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "min_bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "high_bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "high_bidder",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "last_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "revealed",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "remaining_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the lots",
      "do": [
        {
          "set": {
            "key": "values",
            "value": {
              "calc": "split(total_value, items, value_min, value_max)"
            }
          }
        },
        {
          "set": {
            "key": "min_bids",
            "value": {
              "calc": "[round(v * uniform(ratio_min, ratio_max) / min_raise) * min_raise for v in values]"
            }
          }
        },
        {
          "set": {
            "key": "remaining_value",
            "value": {
              "calc": "total_value"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "cash",
            "value": {
              "calc": "start_cash"
            }
          }
        }
      ]
    },
    {
      "use": "sync",
      "label": "the table",
      "mode": "self",
      "to": "all",
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "update",
      "label": "the next item",
      "do": [
        {
          "adjust": {
            "key": "item",
            "value": 1
          }
        },
        {
          "set": {
            "key": "min_bid",
            "value": {
              "calc": "min_bids[item - 1]"
            }
          }
        },
        {
          "set": {
            "key": "high_bid",
            "value": 0
          }
        },
        {
          "set": {
            "key": "high_bidder",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "tell",
      "label": "the item is up",
      "to": "all",
      "text": "Item {item} of {items} is up. The minimum bid is {min_bid}."
    },
    {
      "use": "update",
      "label": "who can bid",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.cash >= min_bid"
            },
            "key": "bidding",
            "value": "in"
          }
        },
        {
          "set": {
            "players": {
              "where": "you.cash < min_bid"
            },
            "key": "bidding",
            "value": "out",
            "text": "Seat {player} cannot afford the minimum bid and sits out item {item}."
          }
        }
      ]
    },
    {
      "use": "ask",
      "label": "bid",
      "to": {
        "where": "you.bidding == 'in'"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "max(min_bid, high_bid + min_raise)"
        },
        "max": {
          "calc": "you.cash"
        },
        "or": [
          "pass"
        ]
      },
      "turns": {
        "pass": "pass",
        "max": 500
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "high_bidder",
              "value": "$seat",
              "if": {
                "calc": "$answer != 'pass'"
              }
            }
          },
          {
            "set": {
              "key": "high_bid",
              "value": "$answer",
              "if": {
                "calc": "$answer != 'pass'"
              }
            }
          },
          {
            "set": {
              "players": {
                "where": "you.bidding == 'in' and you.seat != high_bidder and you.cash < high_bid + min_raise"
              },
              "key": "bidding",
              "value": "out",
              "if": {
                "calc": "$answer != 'pass'"
              },
              "text": "Seat {player} cannot afford to raise and drops out of item {item}."
            }
          }
        ]
      },
      "text": "Item {item} of {items}: minimum bid {min_bid}, high bid so far {high_bid}. Bid higher to take the lead, or pass. Passing does not take you out: you are asked again when it comes round to you, until everyone else passes after the last bid.",
      "broadcast": {
        "to": "all",
        "text": "Seat {seat}: {value} on item {item}."
      }
    },
    {
      "use": "tell",
      "label": "unsold",
      "when": {
        "calc": "high_bidder == 0"
      },
      "to": "all",
      "text": "Nobody bid on item {item}."
    },
    {
      "use": "update",
      "label": "the sale",
      "do": [
        {
          "set": {
            "key": "last_value",
            "value": {
              "calc": "values[item - 1]"
            }
          }
        },
        {
          "append": {
            "key": "revealed",
            "value": {
              "calc": "last_value"
            }
          }
        },
        {
          "adjust": {
            "key": "remaining_value",
            "value": {
              "calc": "-last_value"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "high_bidder"
            },
            "key": "cash",
            "value": {
              "calc": "-high_bid"
            },
            "if": {
              "calc": "high_bidder > 0"
            },
            "text": "Seat {player} wins item {item} for {high_bid}."
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "high_bidder"
            },
            "key": "holdings",
            "value": {
              "calc": "last_value"
            },
            "if": {
              "calc": "high_bidder > 0"
            }
          }
        },
        {
          "append": {
            "player": {
              "calc": "high_bidder"
            },
            "key": "won",
            "value": {
              "calc": "item"
            },
            "if": {
              "calc": "high_bidder > 0"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bidding",
            "value": "out"
          }
        }
      ],
      "text": "Item {item} was worth {last_value}. Value not yet revealed: {remaining_value}."
    },
    {
      "use": "check",
      "label": "after the last item"
    }
  ],
  "end": {
    "richest": {
      "when": {
        "calc": "item >= items"
      },
      "winner": "The winner is the player with the highest final wealth: their cash plus the true value of the items they won (holdings). Players level at the top share the win.",
      "reason": "the highest final wealth, cash plus the value of items won",
      "text": "The auction is over. {result} wins. {reason}"
    }
  },
  "limits": {
    "rounds": 20,
    "rounds_max": 20,
    "actions_max": 1000,
    "deadline_s": 120
  },
  "rules": "{items} items are auctioned one at a time. Every item has a true value that nobody knows until it has sold. The {items} values together always add up to {total_value}, and each is between {value_min} and {value_max}. Everyone starts with {start_cash} in cash.\n\nEvery item has a public minimum bid, set at between {ratio_min} and {ratio_max} times its true value, so a minimum bid is a clue to what the item is worth. All the minimum bids are shown from the start, in the order the items will be sold.\n\nEach item is sold in an open, ascending auction. Players are asked one at a time in seat order, round and round the table; the first player asked moves one seat round with each item, so item 1 opens with seat 1, item 2 with seat 2, and so on. When asked, either bid a whole number that is at least the minimum bid, at least {min_raise} above the current high bid, and no more than your cash; or pass. Passing does not take you out: you are asked again when it comes round to you. Bidding on an item ends when everyone else has passed, one after another, since the last bid; if nobody bids at all, it ends once everyone has passed. The high bidder is never asked to beat their own bid. A player who cannot afford the next legal bid is out of that item. Everyone sees every bid and every pass. Nobody talks: you only bid.\n\nWhen bidding stops, the leader pays their bid and takes the item. Its true value is then revealed to everyone. If nobody bids, the item goes unsold and its value is still revealed.\n\nAfter the last item, your final wealth is your remaining cash plus the true value of every item you won. The highest final wealth wins; players level at the top share the win. Cash you keep counts exactly as much as value you buy, so paying more than an item is worth loses you wealth."
}

```
