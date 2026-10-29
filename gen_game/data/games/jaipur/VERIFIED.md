# Verification of jaipur

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 89.5 | 1062 chars | 10965 chars |  |
| 02 | critic | claude-opus-5-5 | 64.6 | 3977 chars | 5366 chars |  |
| 03 | design | claude-opus-5-5 | 59.6 | 6983 chars | 9857 chars |  |
| 04 | critic | claude-opus-5-5 | 71.2 | 4055 chars | 4934 chars |  |
| 05 | spec | claude-opus-5-5 | 53.8 | 2972 chars | 13246 chars |  |
| 06 | scenarios | claude-opus-5-5 | 91.6 | 15397 chars | 12102 chars |  |
| 07 | scenarios | claude-opus-5-5 | 54.3 | 27898 chars | 12270 chars |  |
| 08 | coder | claude-opus-5-5 | 166.2 | 30704 chars | 39327 chars |  |
| 09 | coder | claude-opus-5-5 | 111.8 | 55191 chars | 39342 chars |  |
| 10 | coder | claude-opus-5-5 | 120.2 | 55381 chars | 40192 chars |  |
| 11 | coder | claude-opus-5-5 | 121.4 | 55191 chars | 39868 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 ae90024fe02464d6, 30704 chars. MATCHES call 08: this is exactly what was sent.
- the coder was called 4 time(s); the last was call 11

## The game file

- `game.json`: sha256 c4d551e5197ae0c2
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 30 of 30 pass
- tier 0 (valid, ends, replays identically): passed; results over 20 random matches: {'seat 2': 7, 'seat 1': 12, 'seats 1 and 2': 1}
- reasoning and balance: not checked here (real models will play it later)

