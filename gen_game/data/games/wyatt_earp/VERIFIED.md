# Verification of wyatt_earp

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 67.4 | 1182 chars | 10643 chars |  |
| 02 | critic | claude-opus-5-5 | 59.7 | 3393 chars | 6420 chars |  |
| 03 | design | claude-opus-5-5 | 76.3 | 9687 chars | 11003 chars |  |
| 04 | critic | claude-opus-5-5 | 53.5 | 3357 chars | 5004 chars |  |
| 05 | spec | claude-opus-5-5 | 52.1 | 2155 chars | 13905 chars |  |
| 06 | scenarios | claude-opus-5-5 | 48.3 | 16765 chars | 7989 chars |  |
| 07 | scenarios | claude-opus-5-5 | 34.8 | 25153 chars | 8611 chars |  |
| 08 | coder | claude-opus-5-5 | 95.2 | 30327 chars | 25213 chars |  |
| 09 | coder | claude-opus-5-5 | 63.8 | 54689 chars | 25085 chars |  |
| 10 | coder | claude-opus-5-5 | 59.6 | 55337 chars | 25100 chars |  |
| 11 | coder | claude-opus-5-5 | 61.8 | 54835 chars | 25246 chars |  |
| 12 | coder | claude-opus-5-5 | 63.0 | 55004 chars | 25376 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 c2852a4a925914b5, 30327 chars. MATCHES call 08: this is exactly what was sent.
- the coder was called 5 time(s); the last was call 12

## The game file

- `game.json`: sha256 d4e2b9e971d3ad90
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 18 of 18 pass
- tier 0 (valid, ends, replays identically): passed; results over 40 random matches: {'seat 3': 7, 'seat 2': 15, 'seat 1': 9, 'seats 1 and 2': 1, 'seats 2 and 3': 1, 'seat 4': 5, 'seats 2 and 4': 2}
- reasoning and balance: not checked here (real models will play it later)

