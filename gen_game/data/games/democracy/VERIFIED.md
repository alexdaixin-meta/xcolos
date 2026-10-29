# Verification of democracy

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 78.2 | 954 chars | 10733 chars |  |
| 02 | critic | claude-opus-5-5 | 53.9 | 3538 chars | 5675 chars |  |
| 03 | spec | claude-opus-5-5 | 52.4 | 2563 chars | 11907 chars |  |
| 04 | scenarios | claude-opus-5-5 | 87.8 | 14049 chars | 11258 chars |  |
| 05 | scenarios | claude-opus-5-5 | 61.5 | 26667 chars | 13499 chars |  |
| 06 | coder | claude-opus-5-5 | 107.6 | 29391 chars | 25388 chars |  |
| 07 | coder | claude-opus-5-5 | 75.6 | 53918 chars | 25460 chars |  |
| 08 | coder | claude-opus-5-5 | 77.1 | 53886 chars | 25219 chars |  |
| 09 | coder | claude-opus-5-5 | 75.0 | 54070 chars | 25291 chars |  |
| 10 | coder | claude-opus-5-5 | 75.5 | 53918 chars | 26674 chars |  |
| 11 | triage | claude-opus-5-5 | 14.2 | 6144 chars | 1669 chars |  |
| 12 | coder | claude-opus-5-5 | 119.1 | 30799 chars | 25563 chars |  |
| 13 | coder | claude-opus-5-5 | 72.4 | 55797 chars | 25570 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 5d667ae75648ea48, 30799 chars. MATCHES call 12: this is exactly what was sent.
- the coder was called 7 time(s); the last was call 13

## The game file

- `game.json`: sha256 020d6d5763e417af
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 18 of 18 pass
- tier 0 (valid, ends, replays identically): passed; results over 20 random matches: {'seat 2': 7, 'seat 3': 6, 'seat 1': 7}
- reasoning and balance: not checked here (real models will play it later)

