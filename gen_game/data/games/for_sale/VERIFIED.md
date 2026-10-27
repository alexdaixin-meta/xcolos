# Verification of for_sale

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 74.1 | 940 chars | 10589 chars |  |
| 02 | critic | claude-opus-5-5 | 40.0 | 3717 chars | 4695 chars |  |
| 03 | spec | claude-opus-5-5 | 45.8 | 2756 chars | 12238 chars |  |
| 04 | spec | claude-opus-5-5 | 35.6 | 15304 chars | 12696 chars |  |
| 05 | scenarios | claude-opus-5-5 | 66.7 | 14529 chars | 10891 chars |  |
| 06 | scenarios | claude-opus-5-5 | 53.2 | 26370 chars | 12479 chars |  |
| 07 | coder | claude-opus-5-5 | 77.1 | 29387 chars | 22366 chars |  |
| 08 | coder | claude-opus-5-5 | 55.6 | 52126 chars | 22081 chars |  |
| 09 | coder | claude-opus-5-5 | 70.0 | 52252 chars | 22361 chars |  |
| 10 | triage | claude-opus-5-5 | 15.1 | 10190 chars | 1540 chars |  |
| 11 | coder | claude-opus-5-5 | 95.4 | 30530 chars | 26468 chars |  |
| 12 | coder | claude-opus-5-5 | 69.6 | 54918 chars | 26583 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 a76f3d5f302c4540, 30530 chars. MATCHES call 11: this is exactly what was sent.
- the coder was called 5 time(s); the last was call 12

## The game file

- `game.json`: sha256 b614cc9b7d2fdf4b
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 19 of 19 pass
- tier 0 (valid, ends, replays identically): passed; results over 20 random matches: {'seat 2': 11, 'seat 3': 4, 'seat 1': 5}
- reasoning and balance: not checked here (real models will play it later)

