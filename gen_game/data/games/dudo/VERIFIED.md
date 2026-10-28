# Verification of dudo

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 59.1 | 852 chars | 9027 chars |  |
| 02 | critic | claude-opus-5-5 | 97.2 | 3407 chars | 5994 chars |  |
| 03 | design | claude-opus-5-5 | 193.5 | 8021 chars | 12864 chars |  |
| 04 | critic | claude-opus-5-5 | 46.4 | 4034 chars | 5741 chars |  |
| 05 | critic | claude-opus-5-5 | 22.3 | 10048 chars | 5904 chars |  |
| 06 | spec | claude-opus-5-5 | 48.5 | 3162 chars | 12325 chars |  |
| 07 | scenarios | claude-opus-5-5 | 76.5 | 14306 chars | 11832 chars |  |
| 08 | scenarios | claude-opus-5-5 | 49.1 | 26673 chars | 12378 chars |  |
| 09 | coder | claude-opus-5-5 | 81.4 | 29488 chars | 18909 chars |  |
| 10 | triage | claude-opus-5-5 | 9.0 | 8534 chars | 968 chars |  |
| 11 | scenarios | claude-opus-5-5 | 69.7 | 15016 chars | 10354 chars |  |
| 12 | scenarios | claude-opus-5-5 | 40.6 | 25905 chars | 10984 chars |  |
| 13 | triage | claude-opus-5-5 | 12.4 | 4755 chars | 1346 chars |  |
| 14 | design | claude-opus-5-5 | 85.0 | 2498 chars | 10533 chars |  |
| 15 | critic | claude-opus-5-5 | 100.7 | 3499 chars | 5153 chars |  |
| 16 | design | claude-opus-5-5 | 40.7 | 5626 chars | 10286 chars |  |
| 17 | critic | claude-opus-5-5 | 101.1 | 4063 chars | 6015 chars |  |
| 18 | spec | claude-opus-5-5 | 47.0 | 3191 chars | 11789 chars |  |
| 19 | scenarios | claude-opus-5-5 | 132.1 | 13615 chars | 10309 chars |  |
| 20 | scenarios | claude-opus-5-5 | 36.9 | 24187 chars | 10087 chars |  |
| 21 | coder | claude-opus-5-5 | 99.8 | 29542 chars | 23694 chars |  |
| 22 | coder | claude-opus-5-5 | 67.1 | 54271 chars | 24168 chars |  |
| 23 | triage | claude-opus-5-5 | 13.5 | 9613 chars | 1059 chars |  |
| 24 | scenarios | claude-opus-5-5 | 112.9 | 14334 chars | 13459 chars |  |
| 25 | scenarios | claude-opus-5-5 | 63.8 | 28056 chars | 13721 chars |  |
| 26 | triage | claude-opus-5-5 | 12.0 | 4753 chars | 1224 chars |  |
| 27 | design | claude-opus-5-5 | 148.7 | 2534 chars | 9945 chars |  |
| 28 | critic | claude-opus-5-5 | 68.3 | 3501 chars | 4782 chars |  |
| 29 | design | claude-opus-5-5 | 61.5 | 6652 chars | 10178 chars |  |
| 30 | critic | claude-opus-5-5 | 79.1 | 3606 chars | 5777 chars |  |
| 31 | design | claude-opus-5-5 | 46.4 | 5364 chars | 11647 chars |  |
| 32 | critic | claude-opus-5-5 | 80.2 | 4159 chars | 4969 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 a25d80722ca7cf58, 29542 chars. MATCHES call 21: this is exactly what was sent.
- the coder was called 3 time(s); the last was call 22

## The game file

- `game.json`: sha256 af95d74bf02d2d9c
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 22 of 22 pass
- tier 0 (valid, ends, replays identically): passed; results over 40 random matches: {'seat 1': 12, 'seat 2': 15, 'seat 4': 9, 'seat 3': 4}
- reasoning and balance: not checked here (real models will play it later)

