# Verification of break_the_code

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 62.7 | 1009 chars | 9357 chars |  |
| 02 | critic | claude-opus-5-5 | 65.4 | 3049 chars | 5658 chars |  |
| 03 | design | claude-opus-5-5 | 84.4 | 6873 chars | 12701 chars |  |
| 04 | critic | claude-opus-5-5 | 46.6 | 4816 chars | 4044 chars |  |
| 05 | spec | claude-opus-5-5 | 46.0 | 3786 chars | 10820 chars |  |
| 06 | scenarios | claude-opus-5-5 | 82.9 | 12403 chars | 11673 chars |  |
| 07 | coder | claude-opus-5-5 | 107.2 | 28966 chars | 18590 chars |  |
| 08 | coder | claude-opus-5-5 | 50.5 | 48036 chars | 18738 chars |  |
| 09 | coder | claude-opus-5-5 | 123.3 | 49483 chars | 21624 chars |  |
| 10 | coder | claude-opus-5-5 | 68.1 | 51917 chars | 22427 chars |  |
| 11 | triage | claude-opus-5-5 | 15.1 | 10964 chars | 1666 chars |  |
| 12 | coder | claude-opus-5-5 | 137.9 | 30187 chars | 19303 chars |  |
| 13 | coder | claude-opus-5-5 | 59.5 | 49789 chars | 19305 chars |  |
| 14 | coder | claude-opus-5-5 | 93.4 | 49958 chars | 24030 chars |  |
| 15 | coder | claude-opus-5-5 | 100.5 | 55946 chars | 24626 chars |  |
| 16 | coder | claude-opus-5-5 | 127.3 | 55652 chars | 23575 chars |  |
| 17 | triage | claude-opus-5-5 | 14.9 | 7167 chars | 1507 chars |  |
| 18 | coder | claude-opus-5-5 | 116.0 | 30239 chars | 19468 chars |  |
| 19 | coder | claude-opus-5-5 | 51.8 | 50719 chars | 19515 chars |  |
| 20 | coder | claude-opus-5-5 | 53.8 | 50224 chars | 19810 chars |  |
| 21 | coder | claude-opus-5-5 | 442.6 | 51814 chars | 20686 chars |  |
| 22 | coder | claude-opus-5-5 | 72.9 | 52387 chars | 20768 chars |  |
| 23 | triage | claude-opus-5-5 | 10.3 | 7763 chars | 985 chars |  |
| 24 | scenarios | claude-opus-5-5 | 83.4 | 13074 chars | 16166 chars |  |
| 25 | scenarios | claude-opus-5-5 | 60.0 | 30052 chars | 16924 chars |  |
| 26 | triage | claude-opus-5-5 | 20.1 | 10363 chars | 1443 chars |  |
| 27 | design | claude-opus-5-5 | 66.1 | 7857 chars | 10851 chars |  |
| 28 | critic | claude-opus-5-5 | 70.1 | 4328 chars | 5181 chars |  |
| 29 | design | claude-opus-5-5 | 95.4 | 7830 chars | 12024 chars |  |
| 30 | critic | claude-opus-5-5 | 76.5 | 4781 chars | 5235 chars |  |
| 31 | spec | claude-opus-5-5 | 48.0 | 3751 chars | 12408 chars |  |
| 32 | spec | claude-opus-5-5 | 34.7 | 16397 chars | 12599 chars |  |
| 33 | scenarios | claude-opus-5-5 | 83.5 | 14331 chars | 11360 chars |  |
| 34 | scenarios | claude-opus-5-5 | 45.5 | 25954 chars | 11376 chars |  |
| 35 | coder | claude-opus-5-5 | 124.2 | 30545 chars | 23247 chars |  |
| 36 | coder | claude-opus-5-5 | 61.7 | 54138 chars | 23192 chars |  |
| 37 | triage | claude-opus-5-5 | 11.8 | 5716 chars | 1312 chars |  |
| 38 | design | claude-opus-5-5 | 90.8 | 2809 chars | 10448 chars |  |
| 39 | critic | claude-opus-5-5 | 64.0 | 3341 chars | 5585 chars |  |
| 40 | spec | claude-opus-5-5 | 59.2 | 2311 chars | 12299 chars |  |
| 41 | scenarios | claude-opus-5-5 | 59.6 | 14067 chars | 9618 chars |  |
| 42 | scenarios | claude-opus-5-5 | 39.8 | 24016 chars | 9929 chars |  |
| 43 | coder | claude-opus-5-5 | 112.9 | 29148 chars | 19146 chars |  |
| 44 | coder | claude-opus-5-5 | 53.1 | 48814 chars | 19253 chars |  |
| 45 | coder | claude-opus-5-5 | 55.1 | 49071 chars | 18814 chars |  |
| 46 | triage | claude-opus-5-5 | 8.9 | 9004 chars | 1490 chars |  |
| 47 | coder | claude-opus-5-5 | 89.0 | 30280 chars | 20045 chars |  |
| 48 | coder | claude-opus-5-5 | 53.4 | 50840 chars | 20218 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 307a09bc8e6ac12c, 30280 chars. MATCHES call 47: this is exactly what was sent.
- the coder was called 21 time(s); the last was call 48

## The game file

- `game.json`: sha256 6f3ea619736e4084
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 19 of 19 pass
- tier 0 (valid, ends, replays identically): passed; results over 20 random matches: {'seat 1': 12, 'seat 2': 5, 'seats 1 and 2': 3}
- reasoning and balance: not checked here (real models will play it later)

