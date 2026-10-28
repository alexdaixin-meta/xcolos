# Verification of button_men

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 103.9 | 929 chars | 10643 chars |  |
| 02 | critic | claude-opus-5-5 | 70.3 | 3641 chars | 5604 chars |  |
| 03 | design | claude-opus-5-5 | 129.7 | 9127 chars | 13417 chars |  |
| 04 | critic | claude-opus-5-5 | 67.7 | 4820 chars | 4880 chars |  |
| 05 | spec | claude-opus-5-5 | 62.5 | 3870 chars | 16894 chars |  |
| 06 | spec | claude-opus-5-5 | 42.7 | 21002 chars | 17080 chars |  |
| 07 | scenarios | claude-opus-5-5 | 143.0 | 19895 chars | 18424 chars |  |
| 08 | coder | claude-opus-5-5 | 149.5 | 34388 chars | 30782 chars |  |
| 09 | coder | claude-opus-5-5 | 81.9 | 59275 chars | 29882 chars |  |
| 10 | triage | claude-opus-5-5 | 8.9 | 5780 chars | 1275 chars |  |
| 11 | design | claude-opus-5-5 | 97.7 | 2640 chars | 11868 chars |  |
| 12 | critic | claude-opus-5-5 | 76.1 | 3843 chars | 6015 chars |  |
| 13 | design | claude-opus-5-5 | 72.3 | 9731 chars | 11390 chars |  |
| 14 | critic | claude-opus-5-5 | 66.5 | 4676 chars | 5024 chars |  |
| 15 | critic | claude-opus-5-5 | 18.9 | 9973 chars | 5034 chars |  |
| 16 | design | claude-opus-5-5 | 44.9 | 7217 chars | 11749 chars |  |
| 17 | design | claude-opus-5-5 | 29.2 | 19313 chars | 11542 chars |  |
| 18 | critic | claude-opus-5-5 | 56.9 | 4786 chars | 5191 chars |  |
| 19 | spec | claude-opus-5-5 | 45.3 | 3836 chars | 12081 chars |  |
| 20 | scenarios | claude-opus-5-5 | 45.5 | 13681 chars | 8251 chars |  |
| 21 | scenarios | claude-opus-5-5 | 33.9 | 22812 chars | 9282 chars |  |
| 22 | coder | claude-opus-5-5 | 152.9 | 30741 chars | 26429 chars |  |
| 23 | coder | claude-opus-5-5 | 73.5 | 55212 chars | 27402 chars |  |
| 24 | coder | claude-opus-5-5 | 72.6 | 55607 chars | 27792 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 bce7cbb08bfdd45e, 30741 chars. MATCHES call 22: this is exactly what was sent.
- the coder was called 5 time(s); the last was call 24

## The game file

- `game.json`: sha256 4bc28407173f7e17
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 19 of 19 pass
- tier 0 (valid, ends, replays identically): passed; results over 20 random matches: {'seat 1': 9, 'seat 2': 11}
- reasoning and balance: not checked here (real models will play it later)

