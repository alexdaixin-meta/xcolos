# Verification of brusquembille

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 74.9 | 988 chars | 9292 chars |  |
| 02 | critic | claude-opus-5-5 | 52.4 | 3455 chars | 5090 chars |  |
| 03 | design | claude-opus-5-5 | 45.9 | 5057 chars | 10558 chars |  |
| 04 | critic | claude-opus-5-5 | 47.6 | 4011 chars | 4719 chars |  |
| 05 | critic | claude-opus-5-5 | 15.9 | 9003 chars | 4725 chars |  |
| 06 | spec | claude-opus-5-5 | 45.6 | 3002 chars | 10892 chars |  |
| 07 | scenarios | claude-opus-5-5 | 67.2 | 12944 chars | 10334 chars |  |
| 08 | coder | claude-opus-5-5 | 63.7 | 28761 chars | 15207 chars |  |
| 09 | coder | claude-opus-5-5 | 49.1 | 44458 chars | 15377 chars |  |
| 10 | coder | claude-opus-5-5 | 54.8 | 44628 chars | 20670 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 ae53e64fa6a7ede9, 28761 chars. MATCHES call 08: this is exactly what was sent.
- the coder was called 3 time(s); the last was call 10

## The game file

- `game.json`: sha256 e40aa5b68c5e2de8
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 20 of 20 pass
- tier 0 (valid, ends, replays identically): passed; results over 20 random matches: {'seat 2': 12, 'seat 1': 8}
- reasoning and balance: not checked here (real models will play it later)

