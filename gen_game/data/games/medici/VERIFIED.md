# Verification of medici

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 85.6 | 1013 chars | 10622 chars |  |
| 02 | critic | claude-opus-5-5 | 72.5 | 4002 chars | 6140 chars |  |
| 03 | spec | claude-opus-5-5 | 62.1 | 2968 chars | 13938 chars |  |
| 04 | spec | claude-opus-5-5 | 40.1 | 17144 chars | 14424 chars |  |
| 05 | scenarios | claude-opus-5-5 | 141.6 | 16504 chars | 18788 chars |  |
| 06 | scenarios | claude-opus-5-5 | 67.8 | 35555 chars | 18805 chars |  |
| 07 | coder | claude-opus-5-5 | 148.1 | 31605 chars | 34260 chars |  |
| 08 | coder | claude-opus-5-5 | 98.4 | 56284 chars | 33914 chars |  |
| 09 | triage | claude-opus-5-5 | 11.1 | 4933 chars | 1435 chars |  |
| 10 | design | claude-opus-5-5 | 113.5 | 2721 chars | 12441 chars |  |
| 11 | critic | claude-opus-5-5 | 76.1 | 4048 chars | 5921 chars |  |
| 12 | spec | claude-opus-5-5 | 58.1 | 3014 chars | 14276 chars |  |
| 13 | scenarios | claude-opus-5-5 | 108.3 | 16465 chars | 14406 chars |  |
| 14 | scenarios | claude-opus-5-5 | 57.2 | 31270 chars | 14765 chars |  |
| 15 | coder | claude-opus-5-5 | 108.9 | 30769 chars | 23850 chars |  |
| 16 | coder | claude-opus-5-5 | 71.1 | 55108 chars | 24090 chars |  |
| 17 | coder | claude-opus-5-5 | 59.8 | 55448 chars | 24032 chars |  |
| 18 | triage | claude-opus-5-5 | 11.9 | 8502 chars | 981 chars |  |
| 19 | scenarios | claude-opus-5-5 | 124.4 | 17046 chars | 18873 chars |  |
| 20 | scenarios | claude-opus-5-5 | 71.9 | 36318 chars | 19318 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 cf6340140c13578b, 30769 chars. MATCHES call 15: this is exactly what was sent.
- the coder was called 5 time(s); the last was call 17

## The game file

- `game.json`: sha256 4e06f079f40b3f09
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 29 of 29 pass
- tier 0 (valid, ends, replays identically): passed; results over 20 random matches: {'seat 2': 4, 'seat 1': 9, 'seat 3': 6, 'seats 2 and 3': 1}
- reasoning and balance: not checked here (real models will play it later)

