# Verification of turn_the_tide

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 81.5 | 961 chars | 8856 chars |  |
| 02 | critic | claude-opus-5-5 | 51.7 | 3321 chars | 5355 chars |  |
| 03 | design | claude-opus-5-5 | 79.3 | 5278 chars | 12139 chars |  |
| 04 | critic | claude-opus-5-5 | 47.8 | 4281 chars | 4778 chars |  |
| 05 | spec | claude-opus-5-5 | 41.4 | 3299 chars | 10212 chars |  |
| 06 | spec | claude-opus-5-5 | 29.9 | 13749 chars | 10491 chars |  |
| 07 | scenarios | claude-opus-5-5 | 94.7 | 12394 chars | 16341 chars |  |
| 08 | scenarios | claude-opus-5-5 | 71.4 | 29134 chars | 17857 chars |  |
| 09 | coder | claude-opus-5-5 | 94.8 | 28236 chars | 19528 chars |  |
| 10 | coder | claude-opus-5-5 | 46.6 | 48752 chars | 19521 chars |  |
| 11 | coder | claude-opus-5-5 | 52.0 | 48429 chars | 19439 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 3b4e959d12e702cc, 28236 chars. MATCHES call 09: this is exactly what was sent.
- the coder was called 3 time(s); the last was call 11

## The game file

- `game.json`: sha256 90d29ccffc0d098e
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 18 of 18 pass
- tier 0 (valid, ends, replays identically): passed; results over 40 random matches: {'seat 3': 11, 'seat 1': 12, 'seat 2': 12, 'seat 4': 5}
- reasoning and balance: not checked here (real models will play it later)

