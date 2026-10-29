# Verification of durak

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 109.2 | 1003 chars | 11184 chars |  |
| 02 | critic | claude-opus-5-5 | 57.0 | 4384 chars | 5188 chars |  |
| 03 | design | claude-opus-5-5 | 181.7 | 7422 chars | 12949 chars |  |
| 04 | critic | claude-opus-5-5 | 43.3 | 4448 chars | 5267 chars |  |
| 05 | spec | claude-opus-5-5 | 56.9 | 3424 chars | 13297 chars |  |
| 06 | scenarios | claude-opus-5-5 | 75.2 | 15126 chars | 12101 chars |  |
| 07 | coder | claude-opus-5-5 | 158.4 | 30627 chars | 29937 chars |  |
| 08 | coder | claude-opus-5-5 | 104.5 | 55984 chars | 29588 chars |  |
| 09 | coder | claude-opus-5-5 | 127.8 | 56063 chars | 31250 chars |  |
| 10 | triage | claude-opus-5-5 | 14.0 | 9905 chars | 1673 chars |  |
| 11 | coder | claude-opus-5-5 | 255.7 | 31891 chars | 29826 chars |  |
| 12 | coder | claude-opus-5-5 | 97.1 | 56752 chars | 28597 chars |  |
| 13 | triage | claude-opus-5-5 | 9.1 | 9475 chars | 1462 chars |  |
| 14 | coder | claude-opus-5-5 | 256.9 | 31636 chars | 30428 chars |  |
| 15 | coder | claude-opus-5-5 | 113.8 | 56861 chars | 29144 chars |  |
| 16 | triage | claude-opus-5-5 | 6.8 | 4658 chars | 1202 chars |  |
| 17 | design | claude-opus-5-5 | 72.6 | 2134 chars | 12537 chars |  |
| 18 | design | claude-opus-5-5 | 36.7 | 15018 chars | 12317 chars |  |
| 19 | critic | claude-opus-5-5 | 67.2 | 4663 chars | 5392 chars |  |
| 20 | critic | claude-opus-5-5 | 21.0 | 10328 chars | 5443 chars |  |
| 21 | spec | claude-opus-5-5 | 51.7 | 3639 chars | 12303 chars |  |
| 22 | scenarios | claude-opus-5-5 | 87.2 | 13977 chars | 11615 chars |  |
| 23 | coder | claude-opus-5-5 | 158.4 | 31261 chars | 26711 chars |  |
| 24 | coder | claude-opus-5-5 | 68.9 | 56304 chars | 27182 chars |  |
| 25 | triage | claude-opus-5-5 | 13.1 | 10940 chars | 1394 chars |  |
| 26 | scenarios | claude-opus-5-5 | 105.7 | 15038 chars | 12515 chars |  |
| 27 | triage | claude-opus-5-5 | 14.4 | 11436 chars | 1329 chars |  |
| 28 | coder | claude-opus-5-5 | 174.8 | 32254 chars | 26335 chars |  |
| 29 | coder | claude-opus-5-5 | 72.9 | 57246 chars | 26661 chars |  |
| 30 | coder | claude-opus-5-5 | 72.4 | 56933 chars | 26785 chars |  |
| 31 | triage | claude-opus-5-5 | 12.2 | 10416 chars | 1129 chars |  |
| 32 | coder | claude-opus-5-5 | 157.4 | 32009 chars | 27071 chars |  |
| 33 | coder | claude-opus-5-5 | 75.5 | 56870 chars | 28079 chars |  |
| 34 | triage | claude-opus-5-5 | 8.5 | 10287 chars | 1031 chars |  |
| 35 | design | claude-opus-5-5 | 70.7 | 7212 chars | 10700 chars |  |
| 36 | critic | claude-opus-5-5 | 72.8 | 5158 chars | 5227 chars |  |
| 37 | spec | claude-opus-5-5 | 53.8 | 4134 chars | 13988 chars |  |
| 38 | scenarios | claude-opus-5-5 | 107.6 | 15966 chars | 14775 chars |  |
| 39 | coder | claude-opus-5-5 | 124.7 | 32757 chars | 29409 chars |  |
| 40 | triage | claude-opus-5-5 | 14.2 | 10535 chars | 1001 chars |  |
| 41 | scenarios | claude-opus-5-5 | 102.3 | 16590 chars | 13890 chars |  |
| 42 | scenarios | claude-opus-5-5 | 53.6 | 30880 chars | 14400 chars |  |
| 43 | triage | claude-opus-5-5 | 13.0 | 11363 chars | 1365 chars |  |
| 44 | scenarios | claude-opus-5-5 | 93.2 | 17000 chars | 14485 chars |  |
| 45 | triage | claude-opus-5-5 | 11.0 | 5804 chars | 1237 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 9cb287dd5140a3fe, 32757 chars. MATCHES call 39: this is exactly what was sent.
- the coder was called 15 time(s); the last was call 39

## The game file

- `game.json`: sha256 d4c71efa89bf7a2d
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 24 of 24 pass
- tier 0 (valid, ends, replays identically): passed; results over 20 random matches: {'seat 2': 13, 'seat 1': 7}
- reasoning and balance: not checked here (real models will play it later)

