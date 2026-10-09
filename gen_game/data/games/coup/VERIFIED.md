# Verification of coup

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design |  | 137.3 | 859 chars | 16714 chars |  |
| 02 | spec |  | 94.1 | 5097 chars | 21696 chars |  |
| 03 | scenarios |  | 166.5 | 24999 chars | 26513 chars |  |
| 04 | triage |  | 23.3 | 13099 chars | 1651 chars |  |

## The prompt the coder was given

- `AGENT_PROMPT.md`: sha256 3a295712e3e46484, 37138 chars. no coder call in the log carries this hash (an agent reads this file itself; see logs/agent_output.md)

## The game file

- `game.json`: sha256 fa79e0ae8498bdc8
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 43 of 43 pass
- tier 0 (valid, ends, replays identically): passed; results over 40 random matches: {'seat 3': 11, 'seat 2': 9, 'seat 1': 12, 'seat 4': 3, 'seat 5': 5}
- reasoning and balance: not checked here (real models will play it later)

