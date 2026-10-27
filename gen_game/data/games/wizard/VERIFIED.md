# Verification of wizard

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 57.2 | 821 chars | 9452 chars |  |
| 02 | critic | claude-opus-5-5 | 42.0 | 3379 chars | 5148 chars |  |
| 03 | spec | claude-opus-5-5 | 55.6 | 2537 chars | 12985 chars |  |
| 04 | scenarios | claude-opus-5-5 | 54.9 | 15024 chars | 6575 chars |  |
| 05 | coder | claude-opus-5-5 | 129.5 | 29929 chars | 27332 chars |  |
| 06 | coder | claude-opus-5-5 | 80.5 | 54455 chars | 27557 chars |  |
| 07 | coder | claude-opus-5-5 | 93.4 | 54726 chars | 29324 chars |  |
| 08 | coder | claude-opus-5-5 | 100.2 | 54726 chars | 32672 chars |  |
| 09 | coder | claude-opus-5-5 | 110.0 | 54858 chars | 31453 chars |  |
| 10 | triage | claude-opus-5-5 | 11.0 | 6488 chars | 1497 chars |  |
| 11 | coder | claude-opus-5-5 | 165.2 | 31060 chars | 39786 chars |  |
| 12 | coder | claude-opus-5-5 | 124.6 | 55416 chars | 38249 chars |  |
| 13 | coder | claude-opus-5-5 | 114.7 | 55586 chars | 32151 chars |  |
| 14 | coder | claude-opus-5-5 | 119.2 | 55854 chars | 38354 chars |  |
| 15 | coder | claude-opus-5-5 | 148.8 | 55854 chars | 37971 chars |  |
| 16 | triage | claude-opus-5-5 | 13.4 | 6366 chars | 1845 chars |  |
| 17 | coder | claude-opus-5-5 | 168.4 | 31393 chars | 39780 chars |  |
| 18 | coder | claude-opus-5-5 | 119.7 | 55909 chars | 38830 chars |  |
| 19 | coder | claude-opus-5-5 | 188.9 | 56188 chars | 40366 chars |  |
| 20 | coder | claude-opus-5-5 | 116.0 | 56255 chars | 31346 chars |  |
| 21 | coder | claude-opus-5-5 | 284.6 | 56322 chars | 31122 chars |  |
| 22 | triage | claude-opus-5-5 | 11.6 | 6488 chars | 1950 chars |  |
| 23 | design | claude-opus-5-5 | 74.4 | 4962 chars | 12830 chars |  |
| 24 | critic | claude-opus-5-5 | 62.5 | 3958 chars | 6095 chars |  |
| 25 | spec | claude-opus-5-5 | 49.1 | 3116 chars | 13724 chars |  |
| 26 | scenarios | claude-opus-5-5 | 111.4 | 15930 chars | 13192 chars |  |
| 27 | scenarios | claude-opus-5-5 | 65.0 | 30554 chars | 15474 chars |  |
| 28 | coder | claude-opus-5-5 | 125.7 | 30833 chars | 26463 chars |  |
| 29 | coder | claude-opus-5-5 | 73.5 | 55359 chars | 26707 chars |  |
| 30 | coder | claude-opus-5-5 | 72.1 | 55512 chars | 26649 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 c9ee01f0891bc2b7, 30833 chars. MATCHES call 28: this is exactly what was sent.
- the coder was called 18 time(s); the last was call 30

## The game file

- `game.json`: sha256 23a8d79c499e361c
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 25 of 25 pass
- tier 0 (valid, ends, replays identically): passed; results over 20 random matches: {'seat 3': 3, 'seat 1': 7, 'seat 2': 10}
- reasoning and balance: not checked here (real models will play it later)

