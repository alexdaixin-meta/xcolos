# Verification of gracias

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 63.5 | 1057 chars | 10132 chars |  |
| 02 | critic | claude-opus-5-5 | 69.3 | 3485 chars | 5200 chars |  |
| 03 | design | claude-opus-5-5 | 68.8 | 6835 chars | 11122 chars |  |
| 04 | critic | claude-opus-5-5 | 79.8 | 4182 chars | 6132 chars |  |
| 05 | spec | claude-opus-5-5 | 69.9 | 3104 chars | 14627 chars |  |
| 06 | scenarios | claude-opus-5-5 | 134.6 | 17574 chars | 13921 chars |  |
| 07 | coder | claude-opus-5-5 | 121.4 | 31174 chars | 23528 chars |  |
| 08 | coder | claude-opus-5-5 | 71.9 | 55071 chars | 23547 chars |  |
| 09 | triage | claude-opus-5-5 | 12.2 | 15729 chars | 1687 chars |  |
| 10 | scenarios | claude-opus-5-5 | 147.4 | 18754 chars | 16622 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 895509ccedbab0a4, 31174 chars. MATCHES call 07: this is exactly what was sent.
- the coder was called 2 time(s); the last was call 08

## The game file

- `game.json`: sha256 0948447ac9e28733
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 21 of 21 pass
- tier 0 (valid, ends, replays identically): passed; results over 20 random matches: {'seat 1': 7, 'seat 3': 4, 'seat 4': 6, 'seat 2': 3}
- reasoning and balance: not checked here (real models will play it later)

