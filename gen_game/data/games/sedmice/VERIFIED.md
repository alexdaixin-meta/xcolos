# Verification of sedmice

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 62.4 | 898 chars | 9212 chars |  |
| 02 | critic | claude-opus-5-5 | 50.7 | 3187 chars | 5247 chars |  |
| 03 | critic | claude-opus-5-5 | 19.6 | 8707 chars | 5252 chars |  |
| 04 | spec | claude-opus-5-5 | 48.9 | 2268 chars | 10644 chars |  |
| 05 | scenarios | claude-opus-5-5 | 72.5 | 12247 chars | 8362 chars |  |
| 06 | scenarios | claude-opus-5-5 | 37.7 | 21147 chars | 8844 chars |  |
| 07 | coder | claude-opus-5-5 | 85.6 | 27418 chars | 23987 chars |  |
| 08 | coder | claude-opus-5-5 | 57.0 | 52074 chars | 23856 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 fd838efafb4a818b, 27418 chars. MATCHES call 07: this is exactly what was sent.
- the coder was called 2 time(s); the last was call 08

## The game file

- `game.json`: sha256 3e0749ae4630f9ec
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 20 of 20 pass
- tier 0 (valid, ends, replays identically): passed; results over 20 random matches: {'seat 2': 11, 'seat 1': 9}
- reasoning and balance: not checked here (real models will play it later)

