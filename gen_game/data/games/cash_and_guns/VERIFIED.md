# Verification of cash_and_guns

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 60.0 | 1096 chars | 10035 chars |  |
| 02 | critic | claude-opus-5-5 | 47.5 | 3792 chars | 4521 chars |  |
| 03 | spec | claude-opus-5-5 | 49.5 | 2676 chars | 11760 chars |  |
| 04 | scenarios | claude-opus-5-5 | 87.5 | 13714 chars | 13086 chars |  |
| 05 | scenarios | claude-opus-5-5 | 53.8 | 27063 chars | 13674 chars |  |
| 06 | coder | claude-opus-5-5 | 75.2 | 29851 chars | 16969 chars |  |
| 07 | coder | claude-opus-5-5 | 43.8 | 47324 chars | 17183 chars |  |
| 08 | coder | claude-opus-5-5 | 45.1 | 47829 chars | 17184 chars |  |
| 09 | triage | claude-opus-5-5 | 11.9 | 10046 chars | 1083 chars |  |
| 10 | coder | claude-opus-5-5 | 86.3 | 30627 chars | 18248 chars |  |
| 11 | coder | claude-opus-5-5 | 47.7 | 49217 chars | 18165 chars |  |
| 12 | coder | claude-opus-5-5 | 48.0 | 49305 chars | 18462 chars |  |
| 13 | coder | claude-opus-5-5 | 49.7 | 49887 chars | 18325 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 4657bed9f97ad7e4, 30627 chars. MATCHES call 10: this is exactly what was sent.
- the coder was called 7 time(s); the last was call 13

## The game file

- `game.json`: sha256 17772c65f48ac18a
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 21 of 21 pass
- tier 0 (valid, ends, replays identically): passed; results over 40 random matches: {'seat 1': 10, 'seat 3': 13, 'seat 2': 7, 'seats 1 and 3': 1, 'seat 4': 4, 'seat 5': 5}
- reasoning and balance: not checked here (real models will play it later)

