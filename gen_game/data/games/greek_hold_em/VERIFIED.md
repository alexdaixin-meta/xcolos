# Verification of greek_hold_em

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 87.0 | 583 chars | 10250 chars |  |
| 02 | critic | claude-opus-5-5 | 50.0 | 3340 chars | 4893 chars |  |
| 03 | spec | claude-opus-5-5 | 59.7 | 2737 chars | 14520 chars |  |
| 04 | scenarios | claude-opus-5-5 | 116.1 | 17006 chars | 13508 chars |  |
| 05 | scenarios | claude-opus-5-5 | 52.9 | 30777 chars | 13807 chars |  |
| 06 | coder | claude-opus-5-5 | 151.1 | 31279 chars | 31466 chars |  |
| 07 | coder | claude-opus-5-5 | 107.5 | 55576 chars | 30864 chars |  |
| 08 | coder | claude-opus-5-5 | 90.8 | 56280 chars | 30530 chars |  |
| 09 | triage | claude-opus-5-5 | 11.2 | 4541 chars | 1249 chars |  |
| 10 | design | claude-opus-5-5 | 129.8 | 2151 chars | 11637 chars |  |
| 11 | critic | claude-opus-5-5 | 59.9 | 2855 chars | 5486 chars |  |
| 12 | design | claude-opus-5-5 | 66.6 | 7062 chars | 11673 chars |  |
| 13 | critic | claude-opus-5-5 | 79.6 | 3945 chars | 6461 chars |  |
| 14 | design | claude-opus-5-5 | 87.3 | 6435 chars | 11457 chars |  |
| 15 | critic | claude-opus-5-5 | 84.5 | 3587 chars | 6293 chars |  |
| 16 | spec | claude-opus-5-5 | 49.8 | 2984 chars | 12895 chars |  |
| 17 | scenarios | claude-opus-5-5 | 65.6 | 15343 chars | 10769 chars |  |
| 18 | coder | claude-opus-5-5 | 111.5 | 30553 chars | 27743 chars |  |
| 19 | coder | claude-opus-5-5 | 74.1 | 55551 chars | 30369 chars |  |
| 20 | coder | claude-opus-5-5 | 90.7 | 55061 chars | 30606 chars |  |
| 21 | coder | claude-opus-5-5 | 86.3 | 55232 chars | 30383 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 b3193f3c322b4e90, 30553 chars. MATCHES call 18: this is exactly what was sent.
- the coder was called 7 time(s); the last was call 21

## The game file

- `game.json`: sha256 7e407515f88f2c8a
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 19 of 19 pass
- tier 0 (valid, ends, replays identically): passed; results over 20 random matches: {'seat 1': 10, 'seat 3': 4, 'seat 2': 6}
- reasoning and balance: not checked here (real models will play it later)

