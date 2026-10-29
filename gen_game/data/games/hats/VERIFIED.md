# Verification of hats

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 71.3 | 1195 chars | 8532 chars |  |
| 02 | critic | claude-opus-5-5 | 56.8 | 3509 chars | 5633 chars |  |
| 03 | design | claude-opus-5-5 | 117.1 | 9055 chars | 11810 chars |  |
| 04 | critic | claude-opus-5-5 | 43.1 | 3006 chars | 5241 chars |  |
| 05 | critic | claude-opus-5-5 | 19.6 | 8523 chars | 5324 chars |  |
| 06 | spec | claude-opus-5-5 | 40.2 | 1790 chars | 11980 chars |  |
| 07 | scenarios | claude-opus-5-5 | 38.4 | 14302 chars | 8025 chars |  |
| 08 | scenarios | claude-opus-5-5 | 28.7 | 22726 chars | 8029 chars |  |
| 09 | coder | claude-opus-5-5 | 60.7 | 28222 chars | 18666 chars |  |
| 10 | coder | claude-opus-5-5 | 52.4 | 47414 chars | 19613 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 7dee5367fdc02e69, 28222 chars. MATCHES call 09: this is exactly what was sent.
- the coder was called 2 time(s); the last was call 10

## The game file

- `game.json`: sha256 f0ea775af95fac16
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 16 of 16 pass
- tier 0 (valid, ends, replays identically): passed; results over 40 random matches: {'seat 1': 9, 'seat 3': 15, 'seat 2': 9, 'seat 4': 6, 'seats 1 and 2': 1}
- reasoning and balance: not checked here (real models will play it later)

