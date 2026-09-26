# Milestone 3: where the design actually landed

**Status:** Built and running. 887 tests, offline.
**Reference:** [actions.md](actions.md) — the instruction set, in full.

Milestone 2 was designed on paper and then built. The built thing is not the
designed thing, and the differences are the interesting part. This records
what exists, why it differs, and what it still cannot do.

---

## 1. What changed from the design

**Twelve named slots became seven actions.** The design fixed a flow of
`secret_act`, `reveal`, `vote`, `resolve_vote`, `nominate`, `power` and so on,
which a game opted into. That is a taxonomy of what a step is *for*, and a
taxonomy is a guess about games nobody has written: every new game would bend
to fit a slot that nearly matched, or need a thirteenth. The seven that
replaced them are what the engine *does*, and there is nothing else it can do.

**The flow stopped being predefined.** There is no sequence at all now. A round
is `for step in game.steps` — the file's list, in the file's order. That Mafia
has a night before a day is in `mafia.json` and nowhere else.

**The model went from writing prose to filling declared shapes.** The design
had `gate`, `write` and `update` calls. What exists is a call whose *output
type* names the engine method that will consume it — `records` to
`set_attribute`, `message` to `emit_fact`, `choice` to `end_game`. A model
never performs an action; it returns a typed value and the engine acts.

**Visibility became structural rather than instructed.** The design said a
`write` call is handed one audience's view. The first implementation handed the
composing call the whole table, which is a leak channel, and the fix was to
make the *action* decide the view: anything returning player-facing text sees
one seat. A test asserts it against the action table.

---

## 2. The three parts

```
setup     a list of actions, run once
steps     a list of actions, run in order once per round
end       named conditions, tested by check steps
```

Two of the three are symmetric. The third is not: `end` declares *conditions*,
but what happens once one is true — reveal the declared attributes, announce to
everyone, stop — is in `_finish`, not in the file. A game can choose which
attributes and what words, but not the shape: it cannot sync final state,
cannot tell the losers something different, cannot run an epilogue.

A `finish` list would make all three read the same way. Not built.

---

## 3. What the engine owns, and why

Three things stayed out of the model's hands, and each is load-bearing.

**Legality.** `answer.type` and the permitted-target list are enforced without
a model, because every reply from every agent passes through them, including
broken and adversarial ones.

**Arithmetic.** Tallies and counts. A model that miscounts one time in fifty
gives a game that is both wrong and unreproducible.

**Entropy.** The seeded shuffle. This was tested rather than assumed: asked to
assign roles at random, the model returned the identical assignment on four
consecutive seeds; told explicitly to randomise and avoid seat one, it produced
two distinct placements in five matches and never used seats 1, 2 or 5. It has
no randomness to draw on. The engine now hands it a seeded ordering and the
game says what to do with it.

Everything else is the model's: which roster exists, what each player is told,
whether an English win condition has been met, how an outcome is announced.

---

## 4. What a match costs

Five-player Mafia, measured against `rl-muse-spark-1-1-playground`.

| | |
|---|---|
| calls per match | ~8-13 |
| latency per call | 2-4s |
| wall clock | 40-50s for two rounds |

Two findings worth keeping. The newest model was twenty times slower on the
same prompt — `1-1` answers in 2-3s where `1-3` takes 40-60s and drops the
connection — so the *older* model is the right default for a referee answering
yes-or-no questions about a table already described in the prompt. And the
system prompt is byte-identical across a match, which makes it cacheable; at
Mafia's rules length it is below the minimum block size and the cache never
engages, but a longer rules text would hit it.

---

## 5. The grading arrangement

Two definitions ship. `mafia` states its rules in English; `mafia-oracle`
states the same rules as arithmetic and needs no model at all.

This is not redundancy. The arithmetic game is the oracle: run both on a seed
and they must produce an identical fact-by-fact trace, which turns "did the
model get it right" from an opinion into a test. It is also what lets the suite
run offline, and `run_tests.py` sets `XCOLOS_NO_MODEL` so a key on a
developer's machine cannot make the suite mean something different than it does
in review.

The hardcoded Python Mafia survives in `xcolos/legacy/` for the same reason: it
is the only independent implementation of the same game.

---

## 6. What it cannot do

Three gaps, in the order a second game would hit them. A fourth — the largest —
is now closed, and is recorded below it.

**Choices cannot come from state.** `answer.options` is a literal list. "Discard
one of the three policies you drew" cannot be said. Any card game needs it.

**No conditional sub-sequences.** Steps run in declared order, gated
individually. Secret Hitler's powers — investigate at three policies, special
election at four — can be faked as gated steps, but "run this block instead of
that one" cannot be said.

**No variable repetition.** Avalon allows up to five team proposals per
mission until one passes. You would write the steps five times.

Two of the three are the same shape: **a place that takes only literals should
take a reference to state.** That suggests one fix rather than two, and it is
the fix that closed the fourth gap.

### Closed: a step can now address a player an earlier step chose

The pattern is one player naming another, who is then asked to act — a mafia
choosing a victim who gets a last word, a leader picking the team that votes.
Every selector until now described a *property* (all living players, whoever
has this role, seat 3); none could describe *a choice just made*.

The odd part was that the engine already knew the seat. After a tally,
`bindings["chancellor"] = 4` exists, and a game could act on seat 4 through an
operation and name them in wording — but `{"ids": ["$chancellor"]}` died on a
bare `int()` cast. Act on them, talk about them, but not talk to them.

`to` now resolves a bound name when the step runs. What the work cost beyond
that is the interesting part, because none of it was the feature:

- A binding that named nobody had to address nobody. The dangerous reading of
  an unresolved name is a falsy one that quietly aims at seat zero.
- A name no step binds is a load error, reusing the check operations already
  had. A step naming its own not-yet-made binding is too — `to` is resolved
  before the question is asked.
- `author` on a step was already broken and silent. The subject was computed
  nine lines *after* the recipients were chosen, so `to: "author"` loaded, ran,
  and reached an empty audience. Third instance of that failure class after
  `answers_visable` and the tied vote. A subject-relative selector on a step
  with no `about` is now refused.

Six tests, one of which is the feature.

---

## 7. What the engine still writes

Almost nothing, and the remainder is listed rather than defended.

`render_turn` appends `Living seats: [2, 3, 4, 5].` and `Answer with one of:
[...]` to every turn. That is the legal-move context, which the kernel owns,
but it is English the engine chose and it is inconsistent with everything else
being declared.

`role` and `faction` appear in the engine as the kernel's two legacy display
fields from Milestone 1. A game says which of its attributes fills them; a test
asserts the names appear nowhere else.

---

## 8. What was learned by running it

Recorded because the reasoning does not survive in anyone's head.

**A visibility rule that reads correctly can still be wrong.** `allies_by:
faction` looked right and told every villager who the other villagers were,
because villagers share a faction. One field was carrying two meanings —
mutual knowledge, and which side you win with — and in Mafia those differ.

**A silently ignored field is the same bug as a wrong one.** `answers_visable`
loaded cleanly and a step meant to keep its answers private published them. The
loader now refuses unknown keys everywhere, per action, and lists what it
accepts. Nine classes of previously-silent mistake are now load errors.

**The failure you cannot debug is the one that looks like success.** A tied
vote applied nothing and announced nothing, so the table watched a vote and
heard silence. An unanswered ending used to be indistinguishable from a
correct one. Both now fail towards the game visibly continuing.

**Tests that pass are not tests that cover.** Three consecutive fixes to the
seed defaulting passed 877 tests while the bug sat in an HTML attribute the
Python suite cannot see. Two tests now read the page itself.
