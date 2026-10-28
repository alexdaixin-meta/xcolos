# Verification of loot

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 62.8 | 1092 chars | 9430 chars |  |
| 02 | critic | claude-opus-5-5 | 94.9 | 3687 chars | 5658 chars |  |
| 03 | spec | claude-opus-5-5 | 47.1 | 2574 chars | 12205 chars |  |
| 04 | scenarios | claude-opus-5-5 | 69.3 | 14245 chars | 8996 chars |  |
| 05 | scenarios | claude-opus-5-5 | 41.8 | 23777 chars | 9793 chars |  |
| 06 | coder | claude-opus-5-5 | 68.5 | 29487 chars | 16884 chars |  |
| 07 | coder | claude-opus-5-5 | 43.6 | 46722 chars | 16814 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 39c28ded91a9ddaf, 29487 chars. MATCHES call 06: this is exactly what was sent.
- the coder was called 2 time(s); the last was call 07

## The game file

- `game.json`: sha256 509a90222017d795
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 20 of 20 pass
- tier 0 (valid, ends, replays identically): passed; results over 40 random matches: {'seat 3': 13, 'seat 1': 8, 'seat 2': 6, 'seats 1, 2 and 3': 2, 'seat 5': 6, 'seat 4': 5}
- reasoning and balance: not checked here (real models will play it later)

