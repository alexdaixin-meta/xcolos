# Verification of bastard_brag

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 98.0 | 902 chars | 11986 chars |  |
| 02 | critic | claude-opus-5-5 | 72.1 | 4168 chars | 6609 chars |  |
| 03 | design | claude-opus-5-5 | 79.3 | 7131 chars | 14577 chars |  |
| 04 | critic | claude-opus-5-5 | 85.4 | 5305 chars | 6923 chars |  |
| 05 | spec | claude-opus-5-5 | 64.8 | 4383 chars | 14041 chars |  |
| 06 | scenarios | claude-opus-5-5 | 131.0 | 16451 chars | 18444 chars |  |
| 07 | coder | claude-opus-5-5 | 166.4 | 33135 chars | 45869 chars |  |
| 08 | coder | claude-opus-5-5 | 130.0 | 58133 chars | 45957 chars |  |
| 09 | coder | claude-opus-5-5 | 132.2 | 57998 chars | 46008 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 cdfe9b7b3c2eafc6, 33135 chars. MATCHES call 07: this is exactly what was sent.
- the coder was called 3 time(s); the last was call 09

## The game file

- `game.json`: sha256 e51f3a77dc8a4710
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 24 of 24 pass
- tier 0 (valid, ends, replays identically): passed; results over 20 random matches: {'seat 3': 5, 'seat 1': 8, 'seat 2': 7}
- reasoning and balance: not checked here (real models will play it later)

