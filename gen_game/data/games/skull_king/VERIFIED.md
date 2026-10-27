# Verification of skull_king

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 71.0 | 1088 chars | 11579 chars |  |
| 02 | critic | claude-opus-5-5 | 46.2 | 4497 chars | 4776 chars |  |
| 03 | spec | claude-opus-5-5 | 51.6 | 3388 chars | 13409 chars |  |
| 04 | scenarios | claude-opus-5-5 | 110.5 | 15587 chars | 13174 chars |  |
| 05 | scenarios | claude-opus-5-5 | 67.5 | 30537 chars | 16016 chars |  |
| 06 | coder | claude-opus-5-5 | 149.5 | 31441 chars | 32201 chars |  |
| 07 | coder | claude-opus-5-5 | 97.3 | 56439 chars | 31677 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 001651bad2b1dc34, 31441 chars. MATCHES call 06: this is exactly what was sent.
- the coder was called 2 time(s); the last was call 07

## The game file

- `game.json`: sha256 04ee601936342e4a
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 27 of 27 pass
- tier 0 (valid, ends, replays identically): passed; results over 20 random matches: {'seat 3': 4, 'seat 1': 9, 'seat 2': 6, 'seats 1 and 2': 1}
- reasoning and balance: not checked here (real models will play it later)

