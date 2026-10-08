# Verification of assurance_game

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | rl-muse-spark-1-2-playground | 157.4 | 625 chars | 7708 chars |  |
| 02 | spec | rl-muse-spark-1-2-playground | 49.8 | 1220 chars | 5252 chars |  |
| 03 | coder | rl-muse-spark-1-2-playground | 140.3 | 10174 chars | 10958 chars |  |
| 04 | scenarios | rl-muse-spark-1-2-playground | 98.3 | 6502 chars | 2710 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 2df2188ec1fde95a, 9512 chars. no coder call in the log carries this hash
- the coder was called 1 time(s); the last was call 03

## The game file

- `game.json`: sha256 e90625b83f2237a1
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 5 of 5 pass
- tier 0 (valid, ends, replays identically): passed; results over 20 random matches: {'draw': 20}
- tier 1 (thoughtless policies, luck): every random match ended 'draw': choices do not change the result
  - always `first@seat1`: won 0, lost 10, drew 50
  - always `first@seat2`: won 0, lost 8, drew 52
  - always `last@seat1`: won 0, lost 0, drew 60
  - always `last@seat2`: won 0, lost 0, drew 60

