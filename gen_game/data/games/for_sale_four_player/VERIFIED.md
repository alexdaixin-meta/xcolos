# Verification of for_sale

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | rl-muse-spark-1-3-sglang-playground | 74.0 | 5594 chars | 8679 chars |  |
| 02 | critic | rl-muse-spark-1-3-sglang-playground | 118.6 | 3557 chars | 4149 chars |  |
| 03 | spec | rl-muse-spark-1-3-sglang-playground | 115.3 | 2597 chars | 11004 chars |  |
| 04 | scenarios | rl-muse-spark-1-3-sglang-playground | 182.6 | 13898 chars | 13712 chars |  |
| 05 | scenarios | rl-muse-spark-1-3-sglang-playground | 125.7 | 14587 chars | 18225 chars |  |
| 06 | scenarios | rl-muse-spark-1-3-sglang-playground | 117.1 | 32522 chars | 16513 chars |  |
| 07 | coder | rl-muse-spark-1-3-sglang-playground | 156.9 | 29250 chars | 27652 chars |  |
| 08 | coder | rl-muse-spark-1-3-sglang-playground | 62.0 | 60355 chars | 27652 chars |  |
| 09 | coder | rl-muse-spark-1-3-sglang-playground | 67.9 | 91460 chars | 27508 chars |  |
| 10 | coder | rl-muse-spark-1-3-sglang-playground | 57.8 | 122496 chars | 27220 chars |  |
| 11 | coder | rl-muse-spark-1-3-sglang-playground | 55.5 | 153181 chars | 28584 chars |  |
| 12 | triage | rl-muse-spark-1-3-sglang-playground | 88.6 | 8358 chars | 675 chars |  |
| 13 | scenarios | rl-muse-spark-1-3-sglang-playground | 178.0 | 14371 chars | 12614 chars |  |
| 14 | scenarios | rl-muse-spark-1-3-sglang-playground | 175.6 | 15003 chars | 22998 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 65d4476f06150258, 28284 chars. no coder call in the log carries this hash
- the coder was called 5 time(s); the last was call 11

## The game file

- `game.json`: sha256 63ca0d42e3a1b564
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 23 of 23 pass
- tier 0 (valid, ends, replays identically): passed; results over 20 random matches: {'seat 1': 3, 'seat 4': 4, 'seat 2': 5, 'seat 3': 8}
- open play (random players from 3 fixed deals at 4 players, 24 matches each and 12 per answer to the tested seat's first choice): open: neither the deal nor one first move decides. Random players cannot show what thinking players make of a deal; the task's run does
- reasoning and balance: not checked here (real models will play it later)

