# Verification of one_night_revolution

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 93.6 | 880 chars | 10058 chars |  |
| 02 | critic | claude-opus-5-5 | 103.5 | 3444 chars | 5743 chars |  |
| 03 | design | claude-opus-5-5 | 73.5 | 8059 chars | 11268 chars |  |
| 04 | critic | claude-opus-5-5 | 67.2 | 3980 chars | 5416 chars |  |
| 05 | critic | claude-opus-5-5 | 19.4 | 9669 chars | 5457 chars |  |
| 06 | spec | claude-opus-5-5 | 50.2 | 3080 chars | 13208 chars |  |
| 07 | spec | claude-opus-5-5 | 34.9 | 16593 chars | 13535 chars |  |
| 08 | scenarios | claude-opus-5-5 | 108.9 | 15830 chars | 17095 chars |  |
| 09 | scenarios | claude-opus-5-5 | 71.0 | 33462 chars | 18798 chars |  |
| 10 | coder | claude-opus-5-5 | 85.1 | 30533 chars | 22872 chars |  |
| 11 | coder | claude-opus-5-5 | 67.7 | 53892 chars | 26666 chars |  |
| 12 | coder | claude-opus-5-5 | 66.7 | 55570 chars | 24159 chars |  |
| 13 | triage | claude-opus-5-5 | 12.4 | 8970 chars | 1256 chars |  |
| 14 | scenarios | claude-opus-5-5 | 106.4 | 16703 chars | 12516 chars |  |
| 15 | scenarios | claude-opus-5-5 | 50.8 | 29550 chars | 13138 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 50062c7398df7994, 30533 chars. MATCHES call 10: this is exactly what was sent.
- the coder was called 3 time(s); the last was call 12

## The game file

- `game.json`: sha256 302fd663cf4a7179
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 23 of 23 pass
- tier 0 (valid, ends, replays identically): passed; results over 20 random matches: {'seat 2': 4, 'seat 5': 5, 'seat 1': 6, 'seat 3': 2, 'seat 4': 3}
- reasoning and balance: not checked here (real models will play it later)

