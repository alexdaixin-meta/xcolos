# Verification of masterpiece

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 94.1 | 907 chars | 10902 chars |  |
| 02 | critic | claude-opus-5-5 | 95.7 | 3714 chars | 5321 chars |  |
| 03 | critic | claude-opus-5-5 | 21.8 | 9308 chars | 5298 chars |  |
| 04 | design | claude-opus-5-5 | 107.1 | 7905 chars | 11579 chars |  |
| 05 | critic | claude-opus-5-5 | 52.7 | 4257 chars | 5662 chars |  |
| 06 | critic | claude-opus-5-5 | 24.8 | 10192 chars | 5918 chars |  |
| 07 | spec | claude-opus-5-5 | 57.5 | 3329 chars | 14163 chars |  |
| 08 | scenarios | claude-opus-5-5 | 107.2 | 16118 chars | 14397 chars |  |
| 09 | coder | claude-opus-5-5 | 135.9 | 32056 chars | 26647 chars |  |
| 10 | coder | claude-opus-5-5 | 65.9 | 56431 chars | 26832 chars |  |
| 11 | coder | claude-opus-5-5 | 68.0 | 56582 chars | 27047 chars |  |
| 12 | coder | claude-opus-5-5 | 72.1 | 56562 chars | 26927 chars |  |
| 13 | coder | claude-opus-5-5 | 73.0 | 57277 chars | 27428 chars |  |
| 14 | triage | claude-opus-5-5 | 14.9 | 10730 chars | 1407 chars |  |
| 15 | coder | claude-opus-5-5 | 155.6 | 33098 chars | 25596 chars |  |
| 16 | coder | claude-opus-5-5 | 68.9 | 57476 chars | 25797 chars |  |
| 17 | coder | claude-opus-5-5 | 74.2 | 57597 chars | 25641 chars |  |
| 18 | coder | claude-opus-5-5 | 76.9 | 58139 chars | 25985 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 b09d23c042d090a3, 33098 chars. MATCHES call 15: this is exactly what was sent.
- the coder was called 9 time(s); the last was call 18

## The game file

- `game.json`: sha256 08bec9052ab0e81d
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 21 of 21 pass
- tier 0 (valid, ends, replays identically): passed; results over 20 random matches: {'seat 4': 12, 'seat 2': 1, 'seat 3': 6, 'seats 3 and 4': 1}
- reasoning and balance: not checked here (real models will play it later)

