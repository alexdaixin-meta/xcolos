# Verification of schotten_totten

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 64.0 | 847 chars | 10637 chars |  |
| 02 | critic | claude-opus-5-5 | 51.0 | 3881 chars | 4608 chars |  |
| 03 | spec | claude-opus-5-5 | 53.7 | 3013 chars | 12102 chars |  |
| 04 | scenarios | claude-opus-5-5 | 94.5 | 14220 chars | 11547 chars |  |
| 05 | scenarios | claude-opus-5-5 | 43.2 | 26030 chars | 11604 chars |  |
| 06 | coder | claude-opus-5-5 | 110.1 | 28291 chars | 22655 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 ff6ccb9d02b1ea5f, 28291 chars. MATCHES call 06: this is exactly what was sent.
- the coder was called 1 time(s); the last was call 06

## The game file

- `game.json`: sha256 3009aa23b8a4511b
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 20 of 20 pass
- tier 0 (valid, ends, replays identically): passed; results over 20 random matches: {'seat 2': 13, 'seat 1': 7}
- reasoning and balance: not checked here (real models will play it later)

