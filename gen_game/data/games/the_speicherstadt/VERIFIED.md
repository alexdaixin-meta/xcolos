# Verification of the_speicherstadt

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 66.4 | 1015 chars | 10457 chars |  |
| 02 | critic | claude-opus-5-5 | 68.6 | 3881 chars | 5665 chars |  |
| 03 | design | claude-opus-5-5 | 53.2 | 6903 chars | 11551 chars |  |
| 04 | critic | claude-opus-5-5 | 55.9 | 4163 chars | 5431 chars |  |
| 05 | spec | claude-opus-5-5 | 58.5 | 3127 chars | 13908 chars |  |
| 06 | scenarios | claude-opus-5-5 | 91.7 | 16350 chars | 16246 chars |  |
| 07 | coder | claude-opus-5-5 | 163.6 | 30653 chars | 40104 chars |  |
| 08 | coder | claude-opus-5-5 | 138.8 | 55140 chars | 54711 chars |  |
| 09 | triage | claude-opus-5-5 | 11.6 | 7581 chars | 1199 chars |  |
| 10 | scenarios | claude-opus-5-5 | 95.3 | 17140 chars | 16652 chars |  |
| 11 | scenarios | claude-opus-5-5 | 61.1 | 34123 chars | 17239 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 342fdf20714d91a8, 30653 chars. MATCHES call 07: this is exactly what was sent.
- the coder was called 2 time(s); the last was call 08

## The game file

- `game.json`: sha256 3349ffe8c959867f
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 22 of 22 pass
- tier 0 (valid, ends, replays identically): passed; results over 40 random matches: {'seat 3': 12, 'seat 1': 7, 'seats 1 and 3': 2, 'seat 2': 13, 'seat 4': 6}
- reasoning and balance: not checked here (real models will play it later)

