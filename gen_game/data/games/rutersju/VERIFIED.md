# Verification of rutersju

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 68.2 | 665 chars | 10278 chars |  |
| 02 | critic | claude-opus-5-5 | 48.9 | 3304 chars | 4634 chars |  |
| 03 | spec | claude-opus-5-5 | 48.0 | 2619 chars | 11507 chars |  |
| 04 | scenarios | claude-opus-5-5 | 61.5 | 13458 chars | 10830 chars |  |
| 05 | coder | claude-opus-5-5 | 119.4 | 28619 chars | 24022 chars |  |
| 06 | coder | claude-opus-5-5 | 73.5 | 53130 chars | 27697 chars |  |
| 07 | coder | claude-opus-5-5 | 74.3 | 53405 chars | 27999 chars |  |
| 08 | coder | claude-opus-5-5 | 88.3 | 53405 chars | 28327 chars |  |
| 09 | coder | claude-opus-5-5 | 79.7 | 53475 chars | 27868 chars |  |
| 10 | triage | claude-opus-5-5 | 12.8 | 11352 chars | 1316 chars |  |
| 11 | coder | claude-opus-5-5 | 111.8 | 29552 chars | 25462 chars |  |
| 12 | coder | claude-opus-5-5 | 68.0 | 54338 chars | 25839 chars |  |
| 13 | coder | claude-opus-5-5 | 108.1 | 54338 chars | 36082 chars |  |
| 14 | coder | claude-opus-5-5 | 90.2 | 54413 chars | 35624 chars |  |
| 15 | triage | claude-opus-5-5 | 11.0 | 4242 chars | 1390 chars |  |
| 16 | design | claude-opus-5-5 | 146.5 | 2426 chars | 10609 chars |  |
| 17 | critic | claude-opus-5-5 | 61.6 | 3305 chars | 5626 chars |  |
| 18 | design | claude-opus-5-5 | 69.4 | 5505 chars | 10367 chars |  |
| 19 | critic | claude-opus-5-5 | 76.4 | 3502 chars | 6297 chars |  |
| 20 | design | claude-opus-5-5 | 80.0 | 8122 chars | 10851 chars |  |
| 21 | critic | claude-opus-5-5 | 79.7 | 3800 chars | 4780 chars |  |
| 22 | spec | claude-opus-5-5 | 46.4 | 3115 chars | 11065 chars |  |
| 23 | scenarios | claude-opus-5-5 | 75.1 | 13082 chars | 8899 chars |  |
| 24 | coder | claude-opus-5-5 | 135.3 | 28937 chars | 29791 chars |  |
| 25 | coder | claude-opus-5-5 | 80.0 | 53438 chars | 28850 chars |  |
| 26 | coder | claude-opus-5-5 | 91.6 | 53728 chars | 33646 chars |  |
| 27 | coder | claude-opus-5-5 | 93.2 | 53799 chars | 29570 chars |  |
| 28 | coder | claude-opus-5-5 | 115.1 | 53728 chars | 33193 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 4a1c784e98f2adeb, 28937 chars. MATCHES call 24: this is exactly what was sent.
- the coder was called 14 time(s); the last was call 28

## The game file

- `game.json`: sha256 7cb896448f94c7e3
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 23 of 23 pass
- tier 0 (valid, ends, replays identically): passed; results over 40 random matches: {'seat 2': 12, 'seat 1': 10, 'seat 3': 9, 'seat 4': 7, 'seat 5': 2}
- reasoning and balance: not checked here (real models will play it later)

