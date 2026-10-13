# From game generation to real-model evaluation: the loop and its rules

Status: proposal, agreed in outline in conversation on 2026-10-12. Nothing here is built yet except where marked.

## The loop

1. Generate the game (design, spec with numbered rules, rule scenarios, game file) and install it.
2. Play it with real models on the core, at the **suggested table size** (not the minimum): `gen_game simulate <id> --players muse` fills the table to
   the size the game was designed to play best at. Two plays at different seeds. Keep every log.
3. Review each play against the idea, the design, the spec's numbered rules and the prompt players saw (`gen_game review`). Report which rules no play
   exercised.
4. Sort every finding by severity and by where its fix belongs (below), confirm it, then act.
5. Loop back to generation only for confirmed critical and major findings. **An iteration starts at the design, never at the spec**: the designer is given the idea, the design as it stands and the
   findings (the minor ones too), and rewrites the design so that the missing fact is in the rules themselves. The spec, the scenarios, the coder's prompt and the game file are then all rebuilt from that
   design; nothing below it is patched, so no artifact is left from the old version. The old artifacts are kept in `history/iteration-N/`. (`gen_game revise` edits the spec alone and is for manual use;
   the loop does not use it.)

## Table size is designed first (built)

The designer gives `min`, `max` and `suggested` and says why `min` is the minimum and why `suggested` is the best size. The spec and the game file
carry `meta.players.suggested`; the console fills a table to it and shows "best with N"; the real-model run plays at it. Without one, the minimum is used.

## Severity

| Severity | Meaning | Action |
| --- | --- | --- |
| Critical | The game cannot be played correctly: crash, hang, no ending, wrong winner, corrupted state, hidden information leaked. | Fix and loop. |
| Major | A rule or an offer differs from the design, or the prompt hides or misstates something a player decides on. Test: would a typical player's choice change if they read it? | Fix and loop. |
| Minor | Display, wording, noise, efficiency; does not change play. | Logged. **Never starts an iteration by itself.** When an iteration is started for a critical or major finding, the open minor findings are handed to the generator in the same pass. |
| Infra | The fix is in the engine, the harness, the pipeline, the models or the evaluation tools, whatever its severity. | **Stop, document in `ESCALATIONS.md`, ask.** |

Balance is not evaluated: the design step is trusted to have considered it.

## Confirmation

A finding drives a fix only if a program confirms it (a scenario, a probe or a lint check). A reviewer's finding that nothing confirms goes into an
"unconfirmed" list for a person. (A reviewer once reported a wrong elimination that was in fact two legitimate losses.)

## Control

- At most 3 iterations; stop earlier when a full round has no critical or major finding.
- A finding that comes back after being fixed stops the loop and is escalated.
- A confirmed fix returns as a numbered rule in the rewritten design, and so as a scenario. Wording or display fixes leave no regression test (accepted).
- A cap on model calls and time per iteration.
- Each iteration appends to `LOOP_LOG.md`: finding, severity, confirmed or not, fixed, carried (minor) or escalated.

## The judge (added 2026-10-12, built)

Severity rules alone let a game through that a person would not call good: the Agram loop ended "clean" while the end screen left a seat out of the
final tally in every play (a minor display finding). So after the plays, the reviews and the verifier, a model makes the overall call
(`playreview.judge`, `Hooks.judge`, saved as `sim/judge-N.json` and written to `LOOP_LOG.md`). It is shown the idea, the design, each play's result and end
announcement, the measured facts, the reviewer's verdicts and the merged findings (with severity, plays seen in, confirmed or not), and answers:

1. Is each result reasonable, and does the end state make sense: the announcement says the true, complete result (winner or draw, the deciding figures, every seat) and only the result, no retelling of the game? (Not balance, not how well models played.)
2. Is the game played the game designed, and the game of the idea?
3. `iterate` or `good_enough`, with the finding ids that must be fixed.

How its call is used: a confirmed critical or major finding always iterates, whatever the judge says. The judge may add minor findings to the pass (a minor that
misleads players about the result, or that shows in every play); only finding ids that exist count. Infra findings still stop the loop and the judge is not asked.
If the judge cannot answer, the severity rules decide as before. "Good enough" ends the loop with the remaining minors carried.
