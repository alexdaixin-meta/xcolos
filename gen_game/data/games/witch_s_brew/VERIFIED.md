# Verification of witch_s_brew

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 94.1 | 834 chars | 11102 chars |  |
| 02 | critic | claude-opus-5-5 | 68.8 | 3723 chars | 4822 chars |  |
| 03 | spec | claude-opus-5-5 | 49.8 | 2869 chars | 11179 chars |  |
| 04 | scenarios | claude-opus-5-5 | 90.0 | 12858 chars | 11009 chars |  |
| 05 | scenarios | claude-opus-5-5 | 46.6 | 24130 chars | 11634 chars |  |
| 06 | coder | claude-opus-5-5 | 79.4 | 28779 chars | 19828 chars |  |
| 07 | coder | claude-opus-5-5 | 55.2 | 49082 chars | 19996 chars |  |
| 08 | coder | claude-opus-5-5 | 49.2 | 49440 chars | 19872 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 f0a89058c3cbfd2e, 28779 chars. MATCHES call 06: this is exactly what was sent.
- the coder was called 3 time(s); the last was call 08

## The game file

- `game.json`: sha256 eb4ee2c65c99639c
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 19 of 19 pass
- tier 0 (valid, ends, replays identically): passed; results over 40 random matches: {'seat 2': 9, 'seat 1': 6, 'seats 2 and 3': 2, 'seat 3': 9, 'seats 1 and 3': 2, 'seats 2 and 5': 1, 'seat 4': 7, 'seat 5': 4}
- reasoning and balance: not checked here (real models will play it later)

