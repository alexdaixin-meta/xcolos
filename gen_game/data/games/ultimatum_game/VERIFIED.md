# Verification of ultimatum_game

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 57.3 | 528 chars | 8772 chars |  |
| 02 | critic | claude-opus-5-5 | 74.5 | 2445 chars | 4477 chars |  |
| 03 | design | claude-opus-5-5 | 84.3 | 5318 chars | 9938 chars |  |
| 04 | critic | claude-opus-5-5 | 62.3 | 3079 chars | 5069 chars |  |
| 05 | design | claude-opus-5-5 | 65.5 | 8061 chars | 10129 chars |  |
| 06 | critic | claude-opus-5-5 | 58.3 | 2679 chars | 4741 chars |  |
| 07 | spec | claude-opus-5-5 | 44.9 | 2131 chars | 11163 chars |  |
| 08 | scenarios | claude-opus-5-5 | 60.5 | 13059 chars | 10523 chars |  |
| 09 | scenarios | claude-opus-5-5 | 37.5 | 23845 chars | 10566 chars |  |
| 10 | coder | claude-opus-5-5 | 50.2 | 27989 chars | 14920 chars |  |
| 11 | triage | claude-opus-5-5 | 12.0 | 8475 chars | 1514 chars |  |
| 12 | scenarios | claude-opus-5-5 | 69.8 | 14188 chars | 11468 chars |  |
| 13 | scenarios | claude-opus-5-5 | 43.4 | 25919 chars | 11499 chars |  |
| 14 | triage | claude-opus-5-5 | 12.5 | 3901 chars | 1334 chars |  |
| 15 | design | claude-opus-5-5 | 134.5 | 2226 chars | 11116 chars |  |
| 16 | critic | claude-opus-5-5 | 74.8 | 2896 chars | 4649 chars |  |
| 17 | spec | claude-opus-5-5 | 56.0 | 2348 chars | 12690 chars |  |
| 18 | scenarios | claude-opus-5-5 | 68.1 | 14619 chars | 11905 chars |  |
| 19 | scenarios | claude-opus-5-5 | 48.0 | 26787 chars | 11921 chars |  |
| 20 | coder | claude-opus-5-5 | 74.0 | 29475 chars | 17981 chars |  |
| 21 | coder | claude-opus-5-5 | 48.6 | 47921 chars | 18024 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 c3f16b1d8acfb307, 29475 chars. MATCHES call 20: this is exactly what was sent.
- the coder was called 3 time(s); the last was call 21

## The game file

- `game.json`: sha256 f31104d610e2fec8
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 22 of 22 pass
- tier 0 (valid, ends, replays identically): passed; results over 20 random matches: {'seat 2': 10, 'seat 3': 6, 'seat 1': 3, 'no winner decided (no seat reached the minimum to win)': 1}
- reasoning and balance: not checked here (real models will play it later)

