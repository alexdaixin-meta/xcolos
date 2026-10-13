# Verification of agram

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | rl-muse-spark-1-3-sglang-playground | 83.2 | 694 chars | 8446 chars |  |
| 02 | spec | rl-muse-spark-1-3-sglang-playground | 77.2 | 2026 chars | 9298 chars |  |
| 03 | scenarios | rl-muse-spark-1-3-sglang-playground | 1123.0 | 11562 chars | 5704 chars |  |
| 04 | scenarios | rl-muse-spark-1-3-sglang-playground | 58.8 | 18556 chars | 8303 chars |  |
| 05 | other | rl-muse-spark-1-3-sglang-playground | 16.4 | 3887 chars | 12 chars |  |

## The prompt the coder was given

- `AGENT_PROMPT.md`: sha256 1c94277787d404a9, 26508 chars. no coder call in the log carries this hash (an agent reads this file itself; see logs/agent_output.md)

## The game file

- `game.json`: sha256 b33a0292db73b36b
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 16 of 16 pass
- tier 0 (valid, ends, replays identically): passed; results over 40 random matches: {'seat 1': 8, 'draw': 16, 'seat 3': 9, 'seat 2': 5, 'seat 4': 2}
- reasoning and balance: not checked here (real models will play it later)

