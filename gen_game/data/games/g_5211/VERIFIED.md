# Verification of g_5211

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 70.2 | 945 chars | 10451 chars |  |
| 02 | critic | claude-opus-5-5 | 49.3 | 3585 chars | 4406 chars |  |
| 03 | critic | claude-opus-5-5 | 19.5 | 8264 chars | 4560 chars |  |
| 04 | spec | claude-opus-5-5 | 40.5 | 2620 chars | 10637 chars |  |
| 05 | scenarios | claude-opus-5-5 | 63.8 | 12595 chars | 12375 chars |  |
| 06 | scenarios | claude-opus-5-5 | 52.5 | 25437 chars | 13910 chars |  |
| 07 | coder | claude-opus-5-5 | 83.8 | 27850 chars | 19222 chars |  |
| 08 | coder | claude-opus-5-5 | 52.8 | 47574 chars | 19159 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 8b9c28698eb5727b, 27850 chars. MATCHES call 07: this is exactly what was sent.
- the coder was called 2 time(s); the last was call 08

## The game file

- `game.json`: sha256 0f720e407042f797
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 18 of 18 pass
- tier 0 (valid, ends, replays identically): passed; results over 40 random matches: {'seat 1': 14, 'seat 3': 11, 'seat 2': 12, 'seats 1 and 3': 1, 'seat 4': 2}
- reasoning and balance: not checked here (real models will play it later)

