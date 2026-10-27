# Verification of big_two

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 72.0 | 863 chars | 10314 chars |  |
| 02 | critic | claude-opus-5-5 | 58.9 | 4162 chars | 6242 chars |  |
| 03 | critic | claude-opus-5-5 | 23.4 | 10677 chars | 6247 chars |  |
| 04 | spec | claude-opus-5-5 | 64.9 | 3278 chars | 15470 chars |  |
| 05 | scenarios | claude-opus-5-5 | 120.8 | 17610 chars | 14722 chars |  |
| 06 | scenarios | claude-opus-5-5 | 56.9 | 32732 chars | 15015 chars |  |
| 07 | coder | claude-opus-5-5 | 244.5 | 33058 chars | 47784 chars |  |
| 08 | coder | claude-opus-5-5 | 151.8 | 57580 chars | 48090 chars |  |
| 09 | coder | claude-opus-5-5 | 263.0 | 57737 chars | 47245 chars |  |
| 10 | coder | claude-opus-5-5 | 149.5 | 57580 chars | 47687 chars |  |
| 11 | triage | claude-opus-5-5 | 13.6 | 10163 chars | 1258 chars |  |
| 12 | coder | claude-opus-5-5 | 211.6 | 33880 chars | 43709 chars |  |
| 13 | coder | claude-opus-5-5 | 126.9 | 58396 chars | 44363 chars |  |
| 14 | coder | claude-opus-5-5 | 120.0 | 58741 chars | 44746 chars |  |
| 15 | triage | claude-opus-5-5 | 9.1 | 9198 chars | 1076 chars |  |
| 16 | scenarios | claude-opus-5-5 | 109.7 | 18383 chars | 13189 chars |  |
| 17 | scenarios | claude-opus-5-5 | 54.5 | 31971 chars | 13450 chars |  |
| 18 | triage | claude-opus-5-5 | 10.6 | 10073 chars | 1513 chars |  |
| 19 | coder | claude-opus-5-5 | 233.2 | 34268 chars | 42287 chars |  |
| 20 | coder | claude-opus-5-5 | 119.3 | 58770 chars | 44127 chars |  |
| 21 | coder | claude-opus-5-5 | 143.4 | 59125 chars | 44161 chars |  |
| 22 | triage | claude-opus-5-5 | 10.1 | 9980 chars | 1503 chars |  |
| 23 | design | claude-opus-5-5 | 77.8 | 7662 chars | 13452 chars |  |
| 24 | critic | claude-opus-5-5 | 62.1 | 5698 chars | 5657 chars |  |
| 25 | spec | claude-opus-5-5 | 56.4 | 4814 chars | 15786 chars |  |
| 26 | scenarios | claude-opus-5-5 | 147.4 | 18471 chars | 19786 chars |  |
| 27 | scenarios | claude-opus-5-5 | 76.2 | 38794 chars | 20766 chars |  |
| 28 | coder | claude-opus-5-5 | 205.2 | 33977 chars | 43372 chars |  |
| 29 | coder | claude-opus-5-5 | 125.5 | 58838 chars | 43340 chars |  |
| 30 | triage | claude-opus-5-5 | 10.9 | 6852 chars | 1188 chars |  |
| 31 | design | claude-opus-5-5 | 129.2 | 2385 chars | 11747 chars |  |
| 32 | critic | claude-opus-5-5 | 75.9 | 4193 chars | 7762 chars |  |
| 33 | design | claude-opus-5-5 | 72.1 | 7526 chars | 14045 chars |  |
| 34 | critic | claude-opus-5-5 | 77.9 | 5955 chars | 5926 chars |  |
| 35 | design | claude-opus-5-5 | 93.1 | 8823 chars | 11591 chars |  |
| 36 | critic | claude-opus-5-5 | 120.8 | 4884 chars | 6323 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 80ae5ccdd6a4c55e, 33977 chars. MATCHES call 28: this is exactly what was sent.
- the coder was called 12 time(s); the last was call 29

## The game file

- `game.json`: sha256 b91c9bf65418df27
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 25 of 25 pass
- tier 0 (valid, ends, replays identically): passed; results over 20 random matches: {'seat 3': 7, 'seats 2 and 3': 1, 'seat 2': 8, 'seats 1 and 3': 1, 'seat 1': 3}
- reasoning and balance: not checked here (real models will play it later)

