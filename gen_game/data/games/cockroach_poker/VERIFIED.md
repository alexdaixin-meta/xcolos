# Verification of cockroach_poker

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 59.1 | 857 chars | 9090 chars |  |
| 02 | critic | claude-opus-5-5 | 70.5 | 3287 chars | 6048 chars |  |
| 03 | spec | claude-opus-5-5 | 49.2 | 2409 chars | 12290 chars |  |
| 04 | scenarios | claude-opus-5-5 | 69.4 | 14677 chars | 9686 chars |  |
| 05 | scenarios | claude-opus-5-5 | 38.8 | 24830 chars | 9999 chars |  |
| 06 | coder | claude-opus-5-5 | 102.8 | 29485 chars | 24532 chars |  |
| 07 | coder | claude-opus-5-5 | 87.2 | 53994 chars | 35561 chars |  |
| 08 | coder | claude-opus-5-5 | 93.9 | 53984 chars | 28463 chars |  |
| 09 | triage | claude-opus-5-5 | 8.4 | 4434 chars | 1291 chars |  |
| 10 | design | claude-opus-5-5 | 53.4 | 2476 chars | 9727 chars |  |
| 11 | critic | claude-opus-5-5 | 82.2 | 3425 chars | 6809 chars |  |
| 12 | spec | claude-opus-5-5 | 43.2 | 2547 chars | 10582 chars |  |
| 13 | scenarios | claude-opus-5-5 | 68.5 | 12796 chars | 8871 chars |  |
| 14 | scenarios | claude-opus-5-5 | 39.9 | 21998 chars | 9137 chars |  |
| 15 | coder | claude-opus-5-5 | 93.3 | 28673 chars | 23124 chars |  |
| 16 | coder | claude-opus-5-5 | 65.4 | 52292 chars | 23163 chars |  |
| 17 | coder | claude-opus-5-5 | 66.8 | 52331 chars | 23156 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 be5c7c65af574618, 28673 chars. MATCHES call 15: this is exactly what was sent.
- the coder was called 6 time(s); the last was call 17

## The game file

- `game.json`: sha256 0879c49023972308
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 18 of 18 pass
- tier 0 (valid, ends, replays identically): passed; results over 20 random matches: {'seat 2': 9, 'seat 3': 2, 'seat 1': 9}
- reasoning and balance: not checked here (real models will play it later)

