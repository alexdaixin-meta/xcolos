# Verification of smear

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 92.7 | 742 chars | 11067 chars |  |
| 02 | critic | claude-opus-5-5 | 72.3 | 4126 chars | 5420 chars |  |
| 03 | design | claude-opus-5-5 | 52.8 | 6202 chars | 12470 chars |  |
| 04 | critic | claude-opus-5-5 | 54.6 | 4825 chars | 5571 chars |  |
| 05 | spec | claude-opus-5-5 | 66.6 | 4062 chars | 15575 chars |  |
| 06 | scenarios | claude-opus-5-5 | 139.8 | 18367 chars | 13204 chars |  |
| 07 | coder | claude-opus-5-5 | 185.1 | 33872 chars | 35378 chars |  |
| 08 | coder | claude-opus-5-5 | 111.8 | 58383 chars | 38490 chars |  |
| 09 | coder | claude-opus-5-5 | 131.1 | 58915 chars | 39655 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 9947ad3f274e4195, 33872 chars. MATCHES call 07: this is exactly what was sent.
- the coder was called 3 time(s); the last was call 09

## The game file

- `game.json`: sha256 cea02e443fcbf481
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 25 of 25 pass
- tier 0 (valid, ends, replays identically): passed; results over 20 random matches: {'seat 1': 8, 'seat 3': 7, 'seat 2': 5}
- reasoning and balance: not checked here (real models will play it later)

