# Verification of tides_of_madness

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 80.1 | 832 chars | 9575 chars |  |
| 02 | critic | claude-opus-5-5 | 52.7 | 3955 chars | 5300 chars |  |
| 03 | critic | claude-opus-5-5 | 20.5 | 9528 chars | 5325 chars |  |
| 04 | spec | claude-opus-5-5 | 71.7 | 3102 chars | 15083 chars |  |
| 05 | scenarios | claude-opus-5-5 | 113.5 | 17468 chars | 15740 chars |  |
| 06 | scenarios | claude-opus-5-5 | 74.4 | 34500 chars | 17317 chars |  |
| 07 | coder | claude-opus-5-5 | 130.6 | 31852 chars | 30010 chars |  |
| 08 | coder | claude-opus-5-5 | 81.4 | 56356 chars | 30089 chars |  |
| 09 | coder | claude-opus-5-5 | 80.9 | 56712 chars | 30349 chars |  |
| 10 | coder | claude-opus-5-5 | 88.7 | 56202 chars | 30565 chars |  |
| 11 | triage | claude-opus-5-5 | 9.6 | 8784 chars | 1090 chars |  |
| 12 | scenarios | claude-opus-5-5 | 107.2 | 18246 chars | 11870 chars |  |
| 13 | scenarios | claude-opus-5-5 | 86.7 | 31890 chars | 15238 chars |  |
| 14 | triage | claude-opus-5-5 | 9.8 | 8466 chars | 1564 chars |  |
| 15 | coder | claude-opus-5-5 | 133.1 | 33027 chars | 30930 chars |  |
| 16 | coder | claude-opus-5-5 | 110.0 | 57388 chars | 30481 chars |  |
| 17 | coder | claude-opus-5-5 | 95.5 | 57540 chars | 30671 chars |  |
| 18 | coder | claude-opus-5-5 | 93.0 | 58002 chars | 30352 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 29f86c3fc5863eec, 33027 chars. MATCHES call 15: this is exactly what was sent.
- the coder was called 8 time(s); the last was call 18

## The game file

- `game.json`: sha256 0468ccc64e359719
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 29 of 29 pass
- tier 0 (valid, ends, replays identically): passed; results over 20 random matches: {'seat 1': 11, 'seat 2': 9}
- reasoning and balance: not checked here (real models will play it later)

