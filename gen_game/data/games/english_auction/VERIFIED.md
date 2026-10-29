# Verification of english_auction

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 61.9 | 653 chars | 8919 chars |  |
| 02 | critic | claude-opus-5-5 | 38.1 | 3118 chars | 4940 chars |  |
| 03 | spec | claude-opus-5-5 | 58.9 | 2445 chars | 13225 chars |  |
| 04 | spec | claude-opus-5-5 | 35.3 | 15908 chars | 13475 chars |  |
| 05 | scenarios | claude-opus-5-5 | 93.8 | 15512 chars | 10302 chars |  |
| 06 | scenarios | claude-opus-5-5 | 48.4 | 26692 chars | 12477 chars |  |
| 07 | coder | claude-opus-5-5 | 71.3 | 29805 chars | 18002 chars |  |
| 08 | coder | claude-opus-5-5 | 44.5 | 48148 chars | 18170 chars |  |
| 09 | triage | claude-opus-5-5 | 20.3 | 9575 chars | 1333 chars |  |
| 10 | scenarios | claude-opus-5-5 | 102.3 | 16268 chars | 10970 chars |  |
| 11 | scenarios | claude-opus-5-5 | 59.9 | 28117 chars | 12335 chars |  |
| 12 | triage | claude-opus-5-5 | 20.3 | 9559 chars | 1579 chars |  |
| 13 | scenarios | claude-opus-5-5 | 106.0 | 16575 chars | 12975 chars |  |
| 14 | scenarios | claude-opus-5-5 | 61.3 | 29881 chars | 13366 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 9abf1d021e7853f2, 29805 chars. MATCHES call 07: this is exactly what was sent.
- the coder was called 2 time(s); the last was call 08

## The game file

- `game.json`: sha256 48f662cc9effac5c
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 26 of 26 pass
- tier 0 (valid, ends, replays identically): passed; results over 40 random matches: {'seat 2': 14, 'seat 3': 11, 'seat 1': 8, 'seat 5': 4, 'seat 4': 3}
- reasoning and balance: not checked here (real models will play it later)

