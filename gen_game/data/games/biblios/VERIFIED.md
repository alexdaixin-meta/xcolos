# Verification of biblios

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 80.4 | 1060 chars | 11936 chars |  |
| 02 | critic | claude-opus-5-5 | 61.8 | 4036 chars | 6174 chars |  |
| 03 | design | claude-opus-5-5 | 80.3 | 8180 chars | 11649 chars |  |
| 04 | critic | claude-opus-5-5 | 51.7 | 4383 chars | 4851 chars |  |
| 05 | spec | claude-opus-5-5 | 52.0 | 3302 chars | 13141 chars |  |
| 06 | scenarios | claude-opus-5-5 | 79.7 | 15556 chars | 13763 chars |  |
| 07 | scenarios | claude-opus-5-5 | 57.2 | 29718 chars | 14756 chars |  |
| 08 | coder | claude-opus-5-5 | 124.7 | 30743 chars | 33796 chars |  |
| 09 | coder | claude-opus-5-5 | 88.0 | 55249 chars | 32319 chars |  |
| 10 | coder | claude-opus-5-5 | 88.3 | 55421 chars | 32289 chars |  |
| 11 | coder | claude-opus-5-5 | 87.2 | 55249 chars | 31883 chars |  |
| 12 | coder | claude-opus-5-5 | 87.6 | 55545 chars | 32289 chars |  |
| 13 | triage | claude-opus-5-5 | 10.1 | 6650 chars | 1479 chars |  |
| 14 | coder | claude-opus-5-5 | 142.6 | 31946 chars | 29824 chars |  |
| 15 | triage | claude-opus-5-5 | 7.2 | 9907 chars | 1062 chars |  |
| 16 | scenarios | claude-opus-5-5 | 115.5 | 16180 chars | 19019 chars |  |
| 17 | scenarios | claude-opus-5-5 | 69.3 | 35462 chars | 19189 chars |  |
| 18 | triage | claude-opus-5-5 | 13.3 | 5062 chars | 1454 chars |  |
| 19 | design | claude-opus-5-5 | 99.0 | 2702 chars | 12460 chars |  |
| 20 | critic | claude-opus-5-5 | 54.6 | 4139 chars | 5433 chars |  |
| 21 | design | claude-opus-5-5 | 57.6 | 6267 chars | 11990 chars |  |
| 22 | critic | claude-opus-5-5 | 57.7 | 5218 chars | 6197 chars |  |
| 23 | spec | claude-opus-5-5 | 79.7 | 4137 chars | 19186 chars |  |
| 24 | spec | claude-opus-5-5 | 52.2 | 23561 chars | 19772 chars |  |
| 25 | scenarios | claude-opus-5-5 | 115.1 | 23508 chars | 16781 chars |  |
| 26 | scenarios | claude-opus-5-5 | 63.3 | 40620 chars | 16813 chars |  |
| 27 | coder | claude-opus-5-5 | 380.0 | 37127 chars | 39533 chars |  |
| 28 | coder | claude-opus-5-5 | 118.9 | 62134 chars | 39408 chars |  |
| 29 | coder | claude-opus-5-5 | 128.6 | 61643 chars | 41578 chars |  |
| 30 | coder | claude-opus-5-5 | 140.4 | 62566 chars | 40590 chars |  |
| 31 | triage | claude-opus-5-5 | 13.7 | 6743 chars | 1582 chars |  |
| 32 | design | claude-opus-5-5 | 69.7 | 3038 chars | 10104 chars |  |
| 33 | critic | claude-opus-5-5 | 58.1 | 4216 chars | 5324 chars |  |
| 34 | design | claude-opus-5-5 | 46.5 | 6325 chars | 11201 chars |  |
| 35 | critic | claude-opus-5-5 | 49.8 | 4996 chars | 5496 chars |  |
| 36 | spec | claude-opus-5-5 | 60.5 | 3915 chars | 15185 chars |  |
| 37 | spec | claude-opus-5-5 | 42.3 | 19338 chars | 15975 chars |  |
| 38 | scenarios | claude-opus-5-5 | 99.7 | 19008 chars | 14779 chars |  |
| 39 | scenarios | claude-opus-5-5 | 60.4 | 34322 chars | 15598 chars |  |
| 40 | coder | claude-opus-5-5 | 194.4 | 33614 chars | 42816 chars |  |
| 41 | coder | claude-opus-5-5 | 128.7 | 58137 chars | 42185 chars |  |
| 42 | coder | claude-opus-5-5 | 126.3 | 57992 chars | 41533 chars |  |
| 43 | coder | claude-opus-5-5 | 137.7 | 58965 chars | 43546 chars |  |
| 44 | coder | claude-opus-5-5 | 140.6 | 57992 chars | 42876 chars |  |
| 45 | triage | claude-opus-5-5 | 13.7 | 8506 chars | 1818 chars |  |
| 46 | coder | claude-opus-5-5 | 184.2 | 35087 chars | 44926 chars |  |
| 47 | coder | claude-opus-5-5 | 135.0 | 59610 chars | 44279 chars |  |
| 48 | coder | claude-opus-5-5 | 151.0 | 60211 chars | 44559 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 5fe741e3ba2c30fc, 35087 chars. MATCHES call 46: this is exactly what was sent.
- the coder was called 18 time(s); the last was call 48

## The game file

- `game.json`: sha256 9df4662daa6de54e
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 29 of 29 pass
- tier 0 (valid, ends, replays identically): passed; results over 20 random matches: {'seat 1': 5, 'seat 2': 7, 'seats 1 and 3': 2, 'seat 3': 6}
- reasoning and balance: not checked here (real models will play it later)

