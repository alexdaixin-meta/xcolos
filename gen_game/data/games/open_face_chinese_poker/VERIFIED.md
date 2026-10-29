# Verification of open_face_chinese_poker

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 59.9 | 977 chars | 9143 chars |  |
| 02 | design | claude-opus-5-5 | 30.1 | 10336 chars | 10007 chars |  |
| 03 | critic | claude-opus-5-5 | 75.5 | 3597 chars | 5920 chars |  |
| 04 | design | claude-opus-5-5 | 123.6 | 6337 chars | 13268 chars |  |
| 05 | critic | claude-opus-5-5 | 58.7 | 4759 chars | 5156 chars |  |
| 06 | critic | claude-opus-5-5 | 20.1 | 10188 chars | 5176 chars |  |
| 07 | spec | claude-opus-5-5 | 57.6 | 3761 chars | 12751 chars |  |
| 08 | scenarios | claude-opus-5-5 | 175.6 | 15261 chars | 18687 chars |  |
| 09 | scenarios | claude-opus-5-5 | 66.3 | 34211 chars | 18807 chars |  |
| 10 | coder | claude-opus-5-5 | 116.1 | 31360 chars | 27565 chars |  |
| 11 | coder | claude-opus-5-5 | 72.1 | 55721 chars | 27408 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 d9e2d35d885955d8, 31360 chars. MATCHES call 10: this is exactly what was sent.
- the coder was called 2 time(s); the last was call 11

## The game file

- `game.json`: sha256 703fdfe3a5d497d0
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 25 of 25 pass
- tier 0 (valid, ends, replays identically): passed; results over 20 random matches: {'seat 1': 9, 'seats 1 and 2': 4, 'seat 2': 7}
- reasoning and balance: not checked here (real models will play it later)

