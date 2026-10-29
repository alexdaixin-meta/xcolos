# Verification of go_nuts_for_donuts

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 66.9 | 985 chars | 8445 chars |  |
| 02 | design | claude-opus-5-5 | 152.8 | 4993 chars | 10277 chars |  |
| 03 | critic | claude-opus-5-5 | 38.9 | 2858 chars | 5287 chars |  |
| 04 | design | claude-opus-5-5 | 271.4 | 6986 chars | 11437 chars |  |
| 05 | critic | claude-opus-5-5 | 65.5 | 3454 chars | 5828 chars |  |
| 06 | spec | claude-opus-5-5 | 38.0 | 2449 chars | 9616 chars |  |
| 07 | scenarios | claude-opus-5-5 | 70.6 | 11147 chars | 12334 chars |  |
| 08 | scenarios | claude-opus-5-5 | 48.9 | 23812 chars | 12764 chars |  |
| 09 | coder | claude-opus-5-5 | 55.0 | 27146 chars | 15164 chars |  |
| 10 | coder | claude-opus-5-5 | 47.7 | 42792 chars | 15426 chars |  |
| 11 | triage | claude-opus-5-5 | 15.8 | 9285 chars | 1447 chars |  |
| 12 | coder | claude-opus-5-5 | 58.6 | 28171 chars | 14906 chars |  |
| 13 | triage | claude-opus-5-5 | 11.6 | 9275 chars | 1298 chars |  |
| 14 | coder | claude-opus-5-5 | 54.3 | 28066 chars | 14676 chars |  |
| 15 | coder | claude-opus-5-5 | 48.3 | 43224 chars | 14742 chars |  |
| 16 | triage | claude-opus-5-5 | 11.5 | 9285 chars | 1379 chars |  |
| 17 | design | claude-opus-5-5 | 67.8 | 7748 chars | 11581 chars |  |
| 18 | critic | claude-opus-5-5 | 51.7 | 3841 chars | 4923 chars |  |
| 19 | spec | claude-opus-5-5 | 34.7 | 2835 chars | 9863 chars |  |
| 20 | scenarios | claude-opus-5-5 | 57.9 | 11544 chars | 9268 chars |  |
| 21 | coder | claude-opus-5-5 | 56.4 | 27110 chars | 15668 chars |  |
| 22 | coder | claude-opus-5-5 | 43.3 | 43277 chars | 15832 chars |  |
| 23 | triage | claude-opus-5-5 | 12.0 | 8745 chars | 974 chars |  |
| 24 | scenarios | claude-opus-5-5 | 68.2 | 12187 chars | 13532 chars |  |
| 25 | triage | claude-opus-5-5 | 13.4 | 7000 chars | 1266 chars |  |
| 26 | scenarios | claude-opus-5-5 | 72.2 | 12426 chars | 10826 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 8e9136c9eb174f80, 27110 chars. MATCHES call 21: this is exactly what was sent.
- the coder was called 7 time(s); the last was call 22

## The game file

- `game.json`: sha256 9d8e097376f3d316
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 17 of 17 pass
- tier 0 (valid, ends, replays identically): passed; results over 20 random matches: {'seat 4': 8, 'seat 1': 4, 'seat 3': 5, 'seat 2': 3}
- reasoning and balance: not checked here (real models will play it later)

