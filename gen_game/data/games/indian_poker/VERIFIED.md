# Verification of indian_poker

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 67.1 | 664 chars | 11156 chars |  |
| 02 | critic | claude-opus-5-5 | 56.1 | 3281 chars | 5765 chars |  |
| 03 | spec | claude-opus-5-5 | 52.2 | 2597 chars | 12540 chars |  |
| 04 | scenarios | claude-opus-5-5 | 70.0 | 14425 chars | 9502 chars |  |
| 05 | coder | claude-opus-5-5 | 103.9 | 29473 chars | 26496 chars |  |
| 06 | coder | claude-opus-5-5 | 65.0 | 54011 chars | 26722 chars |  |
| 07 | coder | claude-opus-5-5 | 88.0 | 54153 chars | 27199 chars |  |
| 08 | triage | claude-opus-5-5 | 18.4 | 14542 chars | 1437 chars |  |
| 09 | scenarios | claude-opus-5-5 | 61.5 | 15403 chars | 10582 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 b4aa2c0608e6a6ba, 29473 chars. MATCHES call 05: this is exactly what was sent.
- the coder was called 3 time(s); the last was call 07

## The game file

- `game.json`: sha256 a0be60532abfd1aa
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 23 of 23 pass
- tier 0 (valid, ends, replays identically): passed; results over 40 random matches: {'seat 3': 8, 'seat 2': 7, 'seat 4': 4, 'seat 1': 15, 'seat 5': 3, 'seat 6': 3}
- reasoning and balance: not checked here (real models will play it later)

