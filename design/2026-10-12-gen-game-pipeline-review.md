# Review of the game generation pipeline, idea to real-model check and back

Written 2026-10-12 after generating Coup and reviewing four real plays of it. "Checked" means a test or a run showed it; "claimed" means only the code or the prompt says so.

## The stages, what each hands on, and what verifies it

| # | Stage | Input | Output | Verified by |
| - | ----- | ----- | ------ | ----------- |
| 1 | **Idea** | the inventory entry (`rules_text`, players, needs) | itself | the inventory gates (loader of the record) |
| 2 | **Design** (`adapt.py`, idea mode) | idea | `variation.json`: rules, `min/max/suggested`, what it kept and cut and why, complexity | `adapt.problems`; keep-the-idea rules are prompt text only (claimed) |
| 3 | **Spec / game prompt** (`spec.py`) | the design as a source record | `spec.json`: numbered rules, offers table, state, steps, ending, players incl. `suggested` | `spec.problems` (shape only); a model writes it |
| 4 | **Scenarios** (`scenarios.py`) | the spec only | `scenarios.json`: one per rule, by option name, `given`/`rounds`/`lens`/`offered`/`status` | `scenarios.problems`; run against the game in stage 6 |
| 5 | **Coder** (`prompt.py`, `encode.py`, `agent.py`) | script from the spec + patterns + known mistakes + format reference | `game.json` | `encode.check` hard gates: loader, arithmetic outcome, smoke play, replay, dead attributes, unfilled text, blank state, offered-then-refused |
| 6 | **Evaluation** (`flow.py`) | game + scenarios | report | scenarios, tier 0, trace lint, conformance, size (informational), optional rules-text check (`--check-brief`); a model triage sorts failures (fix game / fix tests / revise rules / platform limit), 2 repair rounds |
| 7 | **Real-model play** (`simulate.py`) | installed game, a model per seat, at the suggested size | the whole event log | the engine's own log checks |
| 8 | **Play review** (`playreview.py`) | log + idea + design + spec + the prompt seats saw | findings with severity and where the fix belongs | exact facts by code; a reviewer model for the rest; a second model call to confirm |
| 9 | **Loop** (`loop.py`) | confirmed critical/major findings (+ open minor) | a rewritten design, then a rebuilt spec, scenarios, game; installed | policy in `2026-10-12-evaluation-loop-policy.md`; tested with fakes, one real happy-path pass |

Ownership rules that hold: the id, the table size (`meta.players`) and the spec's parameters are written by the pipeline, never trusted to the coder. Scenarios are written before the build, from the spec alone, and are advisory while the coder builds.

## Where each kind of finding is fixed (iterate from the game prompt)

| Finding is about | Change this | Then rerun |
| --- | --- | --- |
| a rule the coder got wrong, a missing initial-state fact, what a seat is offered, the rules text players read, a departure from the idea, an ambiguity | **the design first** (the designer revises it from the idea, the design as it stands and the findings, writing the missing fact into the rules) | adapt, then spec, scenarios and encode follow from it |
| the platform, the harness, the tools, the models | **nothing automatic: escalate** | after a person decides |

## Gaps found in this review

| # | Gap | Severity | Status |
| - | --- | -------- | ------ |
| G1 | The designer's `suggested` table size was not given to the spec step, so the spec model chose it again, independently. | major (data lost between stages) | **fixed**, with a test: the spec prompt now carries it and says to keep it |
| G2 | The loop had no route for `design` findings; it only revised the spec, and the designer, given only findings, would have written a fresh design. | major | **fixed**: an iteration starts at the design. The designer is given the idea, the design as it stands and the findings, and revises it. Tested. |
| G3 | After a spec revision, `variation.json` was stale: the spec held rules the design did not, and a later `--redo adapt` or `--redo spec` would have dropped them. | major | **fixed**: the loop rewrites the design first, then rebuilds the spec, scenarios, coder prompt and game from it; the old artifacts go to `history/iteration-N/`. A flow test shows all four are written again. |
| G4 | Only fixes that become numbered rules leave a regression test; wording or display fixes leave none. | minor | accepted |
| G5 | The verifier that confirms a finding is the same model as the reviewer. | minor | accepted |
| G6 | One play exercises about half the numbered rules; the loop reports the rules no play touched but does nothing about them. The scenarios are what cover those rules. | informational | accepted |
| G7 | The loop leaves the game installed in the shared library even when it stops escalated. | informational | accepted, say if you want it restored |

## What was not exercised

Only the happy path of the loop ran for real (a clean pass on a small game with offline seats). The revise, regenerate, regression and escalation paths ran only against fakes. A new game is the first end-to-end test of them.
