# Judged conditions in generated games

2026-10-26. A short design: a small change to `gen_game/`. No engine change.

## Intent

When a game has a complex rule, the generated game should hand the rule check to a model with a fixed answer format,
instead of making the coder write it as calc every time and instead of adding new engine operations or syntax
(Alex's direction). The engine already does this mid-game: a step's `when` can be a sentence that a model judges true
or false (`xcolos/flow/executor.py:540`), and Mafia uses prose conditions and `llm` wording. Only the pipeline forbids
it (`gen_game/prompt.py:124`, `gen_game/encode.py:283-297`).

## Goals

- The coder may write a step's `when` as `{"prose": "<sentence>"}` when the rule it checks is complex. The engine's
  judge answers true or false at play time.
- The coder may use `llm` for wording on `tell`, `sync` and `update`, always with a `text` fallback (the engine uses
  `text` when no model is reachable or the reply does not validate). Not on `ask` or `poll`: there a model's message can
  mark a seat as not asked, so it could skip a player's turn. Not on an outcome branch: the engine drops the branch's
  `text` when a model is wired, so nothing would be announced if the model fails.
- The pipeline's checks still run offline and still say something true about the game.

## Non-goals and anti-goals

- **The outcome stays arithmetic.** Endings stay `{"calc": ...}` with a `result`: no prose endings, no `winner`, no
  `llm` in an ending. Rewards must stay verifiable. A model deciding who won would make this a failure even if it
  works.
- **No model-written state.** No model-computed values in `update` and no `initialize` `llm` in generated games. That
  is the one engine gap, left until a game needs it.
- No engine change. Operation `if` stays arithmetic (the engine already refuses prose there, `definition.py:650`).
- Counts, sums and comparisons stay calc: the judge is for rules calc cannot say well (the engine's own rule,
  "never asked what the system can compute", `xcolos/flow/judge.py`).

## Approaches considered

1. **Prose only in step conditions; endings and scores stay arithmetic; tests script the judge.** Chosen.
2. A real model judge in every pipeline check: checks real behaviour, but means hundreds of calls per check, network,
   and caching for exact replay.
3. Prose endings too, as Mafia has: a model decides the winner, so the reward is not verifiable, and it needs (2).

## The design

**Spec** (`spec.py`). A round step may carry `"judged": "<one sentence a referee answers true or false>"`, for a rule
check too complex for a calc. The prompt keeps "outcomes are decided by arithmetic" for endings and scores, and says
a step may be judged.

**Designer and critic** (`adapt.py`, `critic.py`). One line in the engine overview: "a model can rule whether a
complex rule applies at a step (true or false); scores and the winner are still calculated". `verifiable` is
unchanged.

**Coder** (`prompt.py`, `encode.py`'s instructions). For each spec step with `judged`, the game step's `when` is
`{"prose": <that sentence, verbatim>}`. Use calc whenever the rule is arithmetic. `llm` is allowed for wording on the
five message steps, with `text` always present. The ending rules are unchanged.

**The file check** (`encode.py`). Still refused: a prose ending, `winner`, `llm` in an ending, `llm` on `initialize`
or `check`. Newly allowed: a prose step `when`, and `llm` on a tell, sync or update that also has `text`. Refused as
well (found in review): `llm` on `ask`, `poll` or an outcome branch, a broadcast `llm` with no `text`, a prose `when`
that is really arithmetic (it parses as a calc), and a prose `when` on a `check` (a referee must not choose when the
game ends). The unused-attribute check also plays judged steps as true, so an attribute only a judged step writes is
not reported as dead.

**Scenarios** (`scenarios.py`, `harness.py`). A scenario may give `"judge": {"<the judged sentence, or a distinctive
part of it>": true | false}`. The runner wires a scripted judge: a prose condition whose sentence contains a key
(case-insensitive) gets that answer, and any other gets **false**. `problems()` refuses a `judge` that is not a map
of strings to booleans. The scenario writer is told which spec steps are judged, and to script them.

**Tier 0, tier 1, smoke, lint.** They run with a judge that answers **false** to every prose condition, so judged
branches never fire there. The game still ends, because endings are calc. Judged branches are covered by the
scenarios, and by a real-model `simulate` (the server wires a model judge, `xcolos/web/server.py:120`).

## Tests

- File check: a prose step `when` passes; a prose ending, `winner` or `llm` without `text` is refused.
- Scenarios: a game with one prose-gated step (built in the test from `rps.json`) plays the step when the scenario's
  `judge` says true, skips it when false, and skips it when the sentence is not listed.
- Tier 0 on that game ends every match, and the judged step never fires.
- The full suite stays green.

## Left to the builder

The exact wording of each prompt line; where the scripted judge is built (one helper in `harness.py`); which existing
tests to extend rather than add.
