# Verification of psychological_jujitsu

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 66.1 | 663 chars | 9681 chars |  |
| 02 | critic | claude-opus-5-5 | 46.3 | 2799 chars | 4830 chars |  |
| 03 | spec | claude-opus-5-5 | 40.6 | 2115 chars | 9439 chars |  |
| 04 | scenarios | claude-opus-5-5 | 38.2 | 11308 chars | 6163 chars |  |
| 05 | scenarios | claude-opus-5-5 | 34.9 | 18213 chars | 7499 chars |  |
| 06 | coder | claude-opus-5-5 | 68.1 | 26142 chars | 16295 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 6da451c10a47548c, 26142 chars. MATCHES call 06: this is exactly what was sent.
- the coder was called 1 time(s); the last was call 06

## The game file

- `game.json`: sha256 0918ec6b4c6a773a
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 16 of 16 pass
- tier 0 (valid, ends, replays identically): passed; results over 40 random matches: {'seat 1': 12, 'seat 3': 14, 'seat 2': 10, 'seat 4': 4}
- reasoning and balance: not checked here (real models will play it later)

