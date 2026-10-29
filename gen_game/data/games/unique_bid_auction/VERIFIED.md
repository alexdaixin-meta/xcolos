# Verification of unique_bid_auction

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 58.1 | 576 chars | 9587 chars |  |
| 02 | design | claude-opus-5-5 | 24.9 | 10468 chars | 9565 chars |  |
| 03 | critic | claude-opus-5-5 | 39.5 | 2039 chars | 4051 chars |  |
| 04 | spec | claude-opus-5-5 | 27.3 | 1445 chars | 7938 chars |  |
| 05 | scenarios | claude-opus-5-5 | 27.1 | 9337 chars | 5895 chars |  |
| 06 | scenarios | claude-opus-5-5 | 25.6 | 15495 chars | 6130 chars |  |
| 07 | coder | claude-opus-5-5 | 33.9 | 24009 chars | 9731 chars |  |
| 08 | coder | claude-opus-5-5 | 27.4 | 34220 chars | 9593 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 7895ece89eb84e34, 24009 chars. MATCHES call 07: this is exactly what was sent.
- the coder was called 2 time(s); the last was call 08

## The game file

- `game.json`: sha256 204af7f1c60e97b5
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 14 of 14 pass
- tier 0 (valid, ends, replays identically): passed; results over 40 random matches: {'seat 2': 10, 'seat 1': 13, 'seat 3': 6, 'seat 4': 6, 'seats 2 and 5': 1, 'seat 5': 3, 'seats 2 and 3': 1}
- reasoning and balance: not checked here (real models will play it later)

