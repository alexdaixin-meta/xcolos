# Verification of hogwash

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 51.2 | 733 chars | 9894 chars |  |
| 02 | critic | claude-opus-5-5 | 68.1 | 3626 chars | 5555 chars |  |
| 03 | design | claude-opus-5-5 | 81.4 | 8177 chars | 12863 chars |  |
| 04 | critic | claude-opus-5-5 | 62.7 | 4925 chars | 6496 chars |  |
| 05 | spec | claude-opus-5-5 | 56.9 | 4171 chars | 14681 chars |  |
| 06 | scenarios | claude-opus-5-5 | 97.8 | 16776 chars | 13754 chars |  |
| 07 | scenarios | claude-opus-5-5 | 57.9 | 31542 chars | 14060 chars |  |
| 08 | coder | claude-opus-5-5 | 164.2 | 33747 chars | 38137 chars |  |
| 09 | coder | claude-opus-5-5 | 106.1 | 58724 chars | 29950 chars |  |
| 10 | triage | claude-opus-5-5 | 10.8 | 6232 chars | 1575 chars |  |
| 11 | design | claude-opus-5-5 | 156.0 | 2572 chars | 12163 chars |  |
| 12 | critic | claude-opus-5-5 | 96.0 | 4135 chars | 5669 chars |  |
| 13 | critic | claude-opus-5-5 | 33.9 | 10106 chars | 5725 chars |  |
| 14 | design | claude-opus-5-5 | 94.1 | 8527 chars | 9761 chars |  |
| 15 | critic | claude-opus-5-5 | 119.3 | 3587 chars | 6454 chars |  |
| 16 | spec | claude-opus-5-5 | 51.9 | 2833 chars | 13027 chars |  |
| 17 | scenarios | claude-opus-5-5 | 81.0 | 15137 chars | 14205 chars |  |
| 18 | scenarios | claude-opus-5-5 | 55.1 | 29741 chars | 14755 chars |  |
| 19 | coder | claude-opus-5-5 | 183.6 | 29833 chars | 25472 chars |  |
| 20 | coder | claude-opus-5-5 | 85.4 | 54331 chars | 25556 chars |  |
| 21 | triage | claude-opus-5-5 | 7.4 | 8875 chars | 837 chars |  |
| 22 | scenarios | claude-opus-5-5 | 86.9 | 15735 chars | 16762 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 e01293ef1d4774a5, 29833 chars. MATCHES call 19: this is exactly what was sent.
- the coder was called 4 time(s); the last was call 20

## The game file

- `game.json`: sha256 c45fa028cd4dee1a
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 23 of 23 pass
- tier 0 (valid, ends, replays identically): passed; results over 20 random matches: {'seat 2': 7, 'seat 1': 5, 'seat 3': 8}
- reasoning and balance: not checked here (real models will play it later)

