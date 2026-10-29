# Verification of truc

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 77.6 | 938 chars | 10024 chars |  |
| 02 | critic | claude-opus-5-5 | 49.3 | 3633 chars | 5283 chars |  |
| 03 | spec | claude-opus-5-5 | 60.6 | 2674 chars | 13205 chars |  |
| 04 | scenarios | claude-opus-5-5 | 56.8 | 15797 chars | 7313 chars |  |
| 05 | coder | claude-opus-5-5 | 110.0 | 30579 chars | 28010 chars |  |
| 06 | coder | claude-opus-5-5 | 76.4 | 55440 chars | 28357 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 e2290fc8bc72302f, 30579 chars. MATCHES call 05: this is exactly what was sent.
- the coder was called 2 time(s); the last was call 06

## The game file

- `game.json`: sha256 25683b47cfd38024
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 12 of 12 pass
- tier 0 (valid, ends, replays identically): passed; results over 20 random matches: {'seat 2': 9, 'seat 1': 11}
- reasoning and balance: not checked here (real models will play it later)

