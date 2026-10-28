# Verification of mari

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 121.5 | 866 chars | 11383 chars |  |
| 02 | critic | claude-opus-5-5 | 76.2 | 4821 chars | 5775 chars |  |
| 03 | design | claude-opus-5-5 | 92.7 | 7688 chars | 14429 chars |  |
| 04 | critic | claude-opus-5-5 | 68.6 | 7584 chars | 5898 chars |  |
| 05 | spec | claude-opus-5-5 | 61.4 | 6697 chars | 15426 chars |  |
| 06 | scenarios | claude-opus-5-5 | 214.1 | 17759 chars | 16470 chars |  |
| 07 | coder | claude-opus-5-5 | 267.6 | 36809 chars | 52200 chars |  |
| 08 | coder | claude-opus-5-5 | 204.9 | 61310 chars | 48940 chars |  |
| 09 | coder | claude-opus-5-5 | 244.4 | 62036 chars | 56661 chars |  |
| 10 | triage | claude-opus-5-5 | 16.3 | 14564 chars | 1842 chars |  |
| 11 | coder | claude-opus-5-5 | 253.6 | 38270 chars | 42629 chars |  |
| 12 | coder | claude-opus-5-5 | 189.2 | 62778 chars | 46665 chars |  |
| 13 | coder | claude-opus-5-5 | 211.3 | 63489 chars | 38324 chars |  |
| 14 | triage | claude-opus-5-5 | 16.9 | 14431 chars | 2056 chars |  |
| 15 | coder | claude-opus-5-5 | 249.7 | 38475 chars | 36908 chars |  |
| 16 | coder | claude-opus-5-5 | 186.5 | 62851 chars | 39368 chars |  |
| 17 | coder | claude-opus-5-5 | 148.6 | 62983 chars | 41111 chars |  |
| 18 | coder | claude-opus-5-5 | 198.0 | 63071 chars | 40946 chars |  |
| 19 | coder | claude-opus-5-5 | 195.5 | 63473 chars | 41761 chars |  |
| 20 | triage | claude-opus-5-5 | 15.9 | 10353 chars | 1640 chars |  |
| 21 | design | claude-opus-5-5 | 102.5 | 4156 chars | 13608 chars |  |
| 22 | critic | claude-opus-5-5 | 85.7 | 5574 chars | 4973 chars |  |
| 23 | spec | claude-opus-5-5 | 59.2 | 4687 chars | 15034 chars |  |
| 24 | scenarios | claude-opus-5-5 | 147.6 | 17726 chars | 15459 chars |  |
| 25 | coder | claude-opus-5-5 | 208.2 | 34116 chars | 44602 chars |  |
| 26 | coder | claude-opus-5-5 | 147.1 | 58638 chars | 43083 chars |  |
| 27 | coder | claude-opus-5-5 | 148.5 | 58665 chars | 44708 chars |  |
| 28 | coder | claude-opus-5-5 | 142.9 | 58644 chars | 43881 chars |  |
| 29 | coder | claude-opus-5-5 | 147.6 | 59342 chars | 44415 chars |  |
| 30 | triage | claude-opus-5-5 | 7.7 | 12015 chars | 1222 chars |  |
| 31 | coder | claude-opus-5-5 | 203.1 | 35018 chars | 34338 chars |  |
| 32 | coder | claude-opus-5-5 | 129.8 | 59537 chars | 33357 chars |  |
| 33 | coder | claude-opus-5-5 | 116.9 | 60244 chars | 30758 chars |  |
| 34 | triage | claude-opus-5-5 | 12.0 | 6738 chars | 1588 chars |  |
| 35 | design | claude-opus-5-5 | 106.0 | 2800 chars | 11454 chars |  |
| 36 | critic | claude-opus-5-5 | 62.5 | 4197 chars | 5849 chars |  |
| 37 | design | claude-opus-5-5 | 165.1 | 6369 chars | 12735 chars |  |
| 38 | critic | claude-opus-5-5 | 100.6 | 5144 chars | 7287 chars |  |
| 39 | design | claude-opus-5-5 | 90.0 | 8888 chars | 13623 chars |  |
| 40 | critic | claude-opus-5-5 | 68.2 | 5133 chars | 5242 chars |  |
| 41 | critic | claude-opus-5-5 | 19.8 | 10648 chars | 5322 chars |  |
| 42 | spec | claude-opus-5-5 | 69.4 | 4246 chars | 17173 chars |  |
| 43 | scenarios | claude-opus-5-5 | 108.8 | 19767 chars | 15854 chars |  |
| 44 | scenarios | claude-opus-5-5 | 65.4 | 36708 chars | 17498 chars |  |
| 45 | coder | claude-opus-5-5 | 194.9 | 35153 chars | 38184 chars |  |
| 46 | coder | claude-opus-5-5 | 124.2 | 59647 chars | 37179 chars |  |
| 47 | coder | claude-opus-5-5 | 128.0 | 60198 chars | 37686 chars |  |
| 48 | coder | claude-opus-5-5 | 133.6 | 59647 chars | 37947 chars |  |
| 49 | triage | claude-opus-5-5 | 11.5 | 6033 chars | 1514 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 f80f16269efeac61, 35153 chars. MATCHES call 45: this is exactly what was sent.
- the coder was called 23 time(s); the last was call 48

## The game file

- `game.json`: sha256 3ad52a7c156b2520
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 30 of 30 pass
- tier 0 (valid, ends, replays identically): passed; results over 20 random matches: {'seat 3': 6, 'seat 2': 6, 'seat 1': 7, 'seats 2 and 3': 1}
- reasoning and balance: not checked here (real models will play it later)

