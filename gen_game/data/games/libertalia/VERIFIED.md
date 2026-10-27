# Verification of libertalia

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 68.0 | 1201 chars | 10277 chars |  |
| 02 | critic | claude-opus-5-5 | 71.3 | 3862 chars | 5257 chars |  |
| 03 | critic | claude-opus-5-5 | 19.4 | 9392 chars | 5263 chars |  |
| 04 | spec | claude-opus-5-5 | 40.8 | 2640 chars | 9372 chars |  |
| 05 | scenarios | claude-opus-5-5 | 66.8 | 11278 chars | 11560 chars |  |
| 06 | scenarios | claude-opus-5-5 | 43.9 | 23101 chars | 12020 chars |  |
| 07 | coder | claude-opus-5-5 | 60.8 | 27558 chars | 16404 chars |  |
| 08 | coder | claude-opus-5-5 | 50.9 | 44450 chars | 16288 chars |  |
| 09 | coder | claude-opus-5-5 | 46.2 | 44808 chars | 16311 chars |  |
| 10 | coder | claude-opus-5-5 | 55.5 | 44349 chars | 16309 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 ea9cf5cf209902b3, 27558 chars. MATCHES call 07: this is exactly what was sent.
- the coder was called 4 time(s); the last was call 10

## The game file

- `game.json`: sha256 d3417d8c16bc707a
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 20 of 20 pass
- tier 0 (valid, ends, replays identically): passed; results over 20 random matches: {'seat 1': 8, 'seat 2': 8, 'seat 3': 3, 'seats 1 and 2': 1}
- reasoning and balance: not checked here (real models will play it later)

