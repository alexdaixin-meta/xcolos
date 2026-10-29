# Verification of cat_lady

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 59.0 | 1062 chars | 9275 chars |  |
| 02 | critic | claude-opus-5-5 | 59.1 | 3625 chars | 5630 chars |  |
| 03 | design | claude-opus-5-5 | 45.6 | 6540 chars | 9903 chars |  |
| 04 | critic | claude-opus-5-5 | 44.5 | 3861 chars | 4581 chars |  |
| 05 | spec | claude-opus-5-5 | 65.9 | 2778 chars | 14869 chars |  |
| 06 | scenarios | claude-opus-5-5 | 105.7 | 17420 chars | 14250 chars |  |
| 07 | coder | claude-opus-5-5 | 158.1 | 31343 chars | 36714 chars |  |
| 08 | coder | claude-opus-5-5 | 118.6 | 55866 chars | 35689 chars |  |
| 09 | coder | claude-opus-5-5 | 120.6 | 56159 chars | 32200 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 c8a820a1760daf76, 31343 chars. MATCHES call 07: this is exactly what was sent.
- the coder was called 3 time(s); the last was call 09

## The game file

- `game.json`: sha256 3b1fd6f96b96b01a
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 33 of 33 pass
- tier 0 (valid, ends, replays identically): passed; results over 40 random matches: {'seat 2': 11, 'seat 3': 10, 'seat 1': 12, 'seat 4': 7}
- reasoning and balance: not checked here (real models will play it later)

