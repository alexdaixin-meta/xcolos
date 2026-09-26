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
```

`setup` and `steps` are lists of actions. `end` is a map of named conditions.

The engine imposes only this: setup runs once, rounds repeat, every step runs
each round unless its `when` gate closes it, a round cap stops a runaway, and
a `check` is the only thing that can end the loop.

There is no fixed sequence of phases. Night, day, dawn and the vote are words
Mafia chose; the engine has none of them.

---

## The seven actions

| action | what it does | waits? | setup? |
|---|---|---|---|
| `initialize` | fill every player's declared fields, then deal them | no | yes |
| `sync` | send each player their own state | no | yes |
| `tell` | send a message and carry on | no | yes |
| `ask` | address players one at a time, each hearing the last | **yes** | no |
| `poll` | address everyone at once and gather | **yes** | no |
| `update` | change state, and say what changed | no | yes |
| `check` | continue, or end | no | no |

`ask` and `poll` are excluded from setup because setup runs before the greeting
goes out; there is nobody to wait on. `check` is excluded because there is
nothing to end.

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
| `ask` | `to` `answer` `verify` `outcome` `broadcast` `text` `llm` `max_words` `deadline_s` `on_timeout` |
| `poll` | the same as `ask` |
| `update` | `do` `text` `llm` `max_words` |
| `check` | `against` `llm` |

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
| `{"attribute": "role", "is": "mafia"}` | whoever matches; add `"not": true` to invert |
| `{"ids": [2, 5]}` | named seats |
| `{"ids": ["$chancellor"]}` | whoever an earlier step bound to that name |

Every selector except `"all"` is intersected with "may act", which is why no
game has to remember to exclude the dead.

### Addressing a player another step chose

`verify.bind` stores the seat a step's answer landed on. `to` can then name it,
which is how one player's choice decides who is asked next:

```json
{"use": "poll",  "label": "the nomination", "to": "acting",
 "answer": {"type": "player"},
 "verify": {"tally": "plurality", "on_tie": "nobody", "bind": "chancellor"}},

{"use": "ask",   "label": "the legislation", "to": {"ids": ["$chancellor"]},
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
| `options` | for `choice`; a list of literals |
| `count` | for `players`; how many |
| `min` / `max` | for `number` |

`verify` reduces the answers, arithmetically, in the engine. Never by a model:
asking one to count is how you get a result that is wrong occasionally and
unreproducibly.

| key | meaning |
|---|---|
| `tally` | `plurality` `majority` `unanimity` |
| `on_tie` | `nobody` `random` `rerun` |
| `bind` | a name a *later* step can read as `$name` |

`$result` is this step's own outcome and needs no `bind`.

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
                "to": {"attribute": "role", "is": "detective"},
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
audience, and `unless` to skip when a binding named nobody.

`disclose` differs from the rest: it records that the recipients now *know*
something, in their `learned`, so the game can later reason about who knows
what. The others only change state. That is why a knowledge reveal is a
`disclose` and not a `tell`.

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
- an `unless` naming a value no tally can produce
- a `requires` naming an attribute the step does not write
- a bare identifier in `text` that names no declared template
- a `$name` in `to` that no earlier step binds
- a subject-relative `to` on a step with no `about`
- an `ids` entry that is neither a seat number nor a `$name`
- `options` that is not a list

The last one is the pattern: `"options": "$hand"` became five one-character
choices, because `tuple()` of a string splits it. A loader that accepts
anything produces a game that is quietly not the game somebody wrote.
