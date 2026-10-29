# Verification of ys

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 56.0 | 991 chars | 8946 chars |  |
| 02 | critic | claude-opus-5-5 | 64.7 | 3480 chars | 4840 chars |  |
| 03 | spec | claude-opus-5-5 | 53.6 | 2469 chars | 13104 chars |  |
| 04 | scenarios | claude-opus-5-5 | 73.5 | 15407 chars | 13113 chars |  |
| 05 | scenarios | claude-opus-5-5 | 52.6 | 28851 chars | 13724 chars |  |
| 06 | coder | claude-opus-5-5 | 87.4 | 29909 chars | 23816 chars |  |
| 07 | coder | claude-opus-5-5 | 60.9 | 54398 chars | 23651 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 ed0e3a10d50019f7, 29909 chars. MATCHES call 06: this is exactly what was sent.
- the coder was called 2 time(s); the last was call 07

## The game file

- `game.json`: sha256 c13488b08f616684
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 20 of 20 pass
- tier 0 (valid, ends, replays identically): passed; results over 20 random matches: {'seat 1': 6, 'seat 2': 7, 'seat 3': 7}
- reasoning and balance: not checked here (real models will play it later)

