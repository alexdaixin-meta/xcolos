# Verification of sushi_go

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 73.8 | 973 chars | 11816 chars |  |
| 02 | critic | claude-opus-5-5 | 40.0 | 4476 chars | 5234 chars |  |
| 03 | spec | claude-opus-5-5 | 50.5 | 3482 chars | 12935 chars |  |
| 04 | scenarios | claude-opus-5-5 | 106.9 | 14891 chars | 13619 chars |  |
| 05 | scenarios | claude-opus-5-5 | 64.4 | 30423 chars | 17329 chars |  |
| 06 | coder | claude-opus-5-5 | 131.7 | 30744 chars | 26641 chars |  |
| 07 | coder | claude-opus-5-5 | 104.4 | 55605 chars | 29984 chars |  |
| 08 | triage | claude-opus-5-5 | 9.7 | 9018 chars | 1437 chars |  |
| 09 | scenarios | claude-opus-5-5 | 113.5 | 15991 chars | 14674 chars |  |
| 10 | scenarios | claude-opus-5-5 | 77.4 | 32716 chars | 16600 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 d528e78fbd214525, 30744 chars. MATCHES call 06: this is exactly what was sent.
- the coder was called 2 time(s); the last was call 07

## The game file

- `game.json`: sha256 374c4a1a4b740337
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 31 of 31 pass
- tier 0 (valid, ends, replays identically): passed; results over 40 random matches: {'seat 1': 15, 'seat 2': 9, 'seat 3': 10, 'seat 4': 6}
- reasoning and balance: not checked here (real models will play it later)

