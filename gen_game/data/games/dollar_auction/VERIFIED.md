# Verification of dollar_auction

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 77.6 | 673 chars | 10125 chars |  |
| 02 | critic | claude-opus-5-5 | 65.8 | 3528 chars | 5459 chars |  |
| 03 | spec | claude-opus-5-5 | 46.9 | 2835 chars | 12624 chars |  |
| 04 | scenarios | claude-opus-5-5 | 60.8 | 14781 chars | 8758 chars |  |
| 05 | scenarios | claude-opus-5-5 | 35.2 | 24212 chars | 9624 chars |  |
| 06 | coder | claude-opus-5-5 | 69.2 | 29386 chars | 20152 chars |  |
| 07 | coder | claude-opus-5-5 | 51.0 | 49890 chars | 20082 chars |  |
| 08 | triage | claude-opus-5-5 | 8.8 | 4523 chars | 1280 chars |  |
| 09 | design | claude-opus-5-5 | 125.5 | 2375 chars | 10256 chars |  |
| 10 | critic | claude-opus-5-5 | 66.1 | 2781 chars | 4686 chars |  |
| 11 | critic | claude-opus-5-5 | 19.7 | 7743 chars | 4703 chars |  |
| 12 | design | claude-opus-5-5 | 89.5 | 6511 chars | 11260 chars |  |
| 13 | critic | claude-opus-5-5 | 105.4 | 2949 chars | 6017 chars |  |
| 14 | critic | claude-opus-5-5 | 27.9 | 9239 chars | 6331 chars |  |
| 15 | design | claude-opus-5-5 | 103.6 | 6712 chars | 9408 chars |  |
| 16 | critic | claude-opus-5-5 | 84.6 | 2850 chars | 4965 chars |  |
| 17 | spec | claude-opus-5-5 | 39.2 | 2156 chars | 9984 chars |  |
| 18 | scenarios | claude-opus-5-5 | 53.5 | 11585 chars | 11867 chars |  |
| 19 | scenarios | claude-opus-5-5 | 41.0 | 23715 chars | 11884 chars |  |
| 20 | coder | claude-opus-5-5 | 59.4 | 27030 chars | 17281 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 7118e677cd76a9a3, 27030 chars. MATCHES call 20: this is exactly what was sent.
- the coder was called 3 time(s); the last was call 20

## The game file

- `game.json`: sha256 563033fb706cbe20
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 15 of 15 pass
- tier 0 (valid, ends, replays identically): passed; results over 20 random matches: {'seat 1': 8, 'seat 3': 5, 'seat 2': 6, 'seats 1 and 2': 1}
- reasoning and balance: not checked here (real models will play it later)

