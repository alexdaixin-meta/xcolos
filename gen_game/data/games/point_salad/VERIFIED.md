# Verification of point_salad

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 78.3 | 901 chars | 9891 chars |  |
| 02 | critic | claude-opus-5-5 | 78.1 | 3516 chars | 5668 chars |  |
| 03 | critic | claude-opus-5-5 | 20.7 | 9457 chars | 5710 chars |  |
| 04 | spec | claude-opus-5-5 | 46.8 | 2594 chars | 11065 chars |  |
| 05 | scenarios | claude-opus-5-5 | 81.1 | 12958 chars | 14393 chars |  |
| 06 | scenarios | claude-opus-5-5 | 50.8 | 27682 chars | 14821 chars |  |
| 07 | coder | claude-opus-5-5 | 69.4 | 28322 chars | 17394 chars |  |
| 08 | coder | claude-opus-5-5 | 44.9 | 46217 chars | 17507 chars |  |
| 09 | coder | claude-opus-5-5 | 46.7 | 46498 chars | 17658 chars |  |
| 10 | triage | claude-opus-5-5 | 5.3 | 8751 chars | 711 chars |  |
| 11 | scenarios | claude-opus-5-5 | 64.9 | 13443 chars | 10573 chars |  |
| 12 | scenarios | claude-opus-5-5 | 42.2 | 24347 chars | 10884 chars |  |
| 13 | triage | claude-opus-5-5 | 10.8 | 8350 chars | 1558 chars |  |
| 14 | scenarios | claude-opus-5-5 | 68.2 | 14194 chars | 12381 chars |  |
| 15 | scenarios | claude-opus-5-5 | 43.8 | 26906 chars | 12705 chars |  |
| 16 | triage | claude-opus-5-5 | 6.8 | 9090 chars | 724 chars |  |
| 17 | design | claude-opus-5-5 | 68.4 | 6475 chars | 10971 chars |  |
| 18 | critic | claude-opus-5-5 | 48.8 | 4047 chars | 4632 chars |  |
| 19 | critic | claude-opus-5-5 | 30.8 | 8952 chars | 4754 chars |  |
| 20 | spec | claude-opus-5-5 | 43.5 | 3125 chars | 10455 chars |  |
| 21 | scenarios | claude-opus-5-5 | 70.7 | 12455 chars | 12846 chars |  |
| 22 | scenarios | claude-opus-5-5 | 46.6 | 25564 chars | 13055 chars |  |
| 23 | coder | claude-opus-5-5 | 69.0 | 28251 chars | 20354 chars |  |
| 24 | coder | claude-opus-5-5 | 55.3 | 48969 chars | 20729 chars |  |
| 25 | coder | claude-opus-5-5 | 54.8 | 49479 chars | 20830 chars |  |
| 26 | coder | claude-opus-5-5 | 55.9 | 49751 chars | 21138 chars |  |
| 27 | triage | claude-opus-5-5 | 8.9 | 8540 chars | 1041 chars |  |
| 28 | scenarios | claude-opus-5-5 | 67.4 | 13132 chars | 14933 chars |  |
| 29 | scenarios | claude-opus-5-5 | 60.3 | 30072 chars | 15851 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 7c5eace3c0c8b4da, 28251 chars. MATCHES call 23: this is exactly what was sent.
- the coder was called 7 time(s); the last was call 26

## The game file

- `game.json`: sha256 0174deacf4c90631
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 23 of 23 pass
- tier 0 (valid, ends, replays identically): passed; results over 20 random matches: {'seat 3': 7, 'seat 2': 10, 'seat 1': 3}
- reasoning and balance: not checked here (real models will play it later)

