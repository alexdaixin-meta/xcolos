# Verification of code_777

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 91.1 | 930 chars | 10667 chars |  |
| 02 | critic | claude-opus-5-5 | 63.8 | 3952 chars | 6161 chars |  |
| 03 | spec | claude-opus-5-5 | 47.3 | 3001 chars | 11431 chars |  |
| 04 | scenarios | claude-opus-5-5 | 72.5 | 13173 chars | 11333 chars |  |
| 05 | scenarios | claude-opus-5-5 | 45.4 | 25180 chars | 11566 chars |  |
| 06 | coder | claude-opus-5-5 | 187.6 | 28727 chars | 26820 chars |  |
| 07 | coder | claude-opus-5-5 | 85.0 | 53410 chars | 27056 chars |  |
| 08 | triage | claude-opus-5-5 | 9.6 | 10220 chars | 1207 chars |  |
| 09 | scenarios | claude-opus-5-5 | 70.7 | 13994 chars | 11827 chars |  |
| 10 | scenarios | claude-opus-5-5 | 42.7 | 26492 chars | 12530 chars |  |
| 11 | triage | claude-opus-5-5 | 10.2 | 10327 chars | 1450 chars |  |
| 12 | scenarios | claude-opus-5-5 | 70.7 | 14168 chars | 10662 chars |  |
| 13 | scenarios | claude-opus-5-5 | 46.9 | 25709 chars | 11539 chars |  |
| 14 | triage | claude-opus-5-5 | 13.0 | 10498 chars | 1095 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 e253d3452cb54935, 28727 chars. MATCHES call 06: this is exactly what was sent.
- the coder was called 2 time(s); the last was call 07

## The game file

- `game.json`: sha256 1bc2562a16e7d611
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **FAIL: tests written independently from the rules disagree with the game: Setup: 3 tiles per rack, deck holds 28 - 9 = 19 (unchanged after a round where everyone passes): rule R1 is broken: When the game is set up, the deck holds 28 tiles (one 1, two 2s, three 3s, four 4s, five 5s, six 6s, seven 7s), each player is dealt 3 tiles into rack, and the deck then holds 28 - 3N.; Ada: the rule for 'EVEN' was ne**

