# Verification of one_night_revolution

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | rl-muse-spark-1-3-sglang-playground | 81.5 | 6528 chars | 8394 chars |  |
| 02 | critic | rl-muse-spark-1-3-sglang-playground | 141.6 | 3820 chars | 4381 chars |  |
| 03 | spec | rl-muse-spark-1-3-sglang-playground | 141.0 | 2922 chars | 11462 chars |  |
| 04 | scenarios | rl-muse-spark-1-3-sglang-playground | 1328.8 | 14036 chars | 0 chars | ERROR: CompletionError: Model API returned no text (max_output_tokens); max_output_tokens=16384 may be spent on reasoning |
| 05 | scenarios | rl-muse-spark-1-3-sglang-playground | 1272.6 | 14036 chars | 0 chars | ERROR: CompletionError: Model API returned no text (max_output_tokens); max_output_tokens=16384 may be spent on reasoning |
| 06 | coder | rl-muse-spark-1-3-sglang-playground | 122.5 | 30728 chars | 20449 chars |  |
| 07 | coder | rl-muse-spark-1-3-sglang-playground | 62.2 | 53739 chars | 21254 chars |  |
| 08 | coder | rl-muse-spark-1-3-sglang-playground | 124.0 | 77730 chars | 21212 chars |  |
| 09 | scenarios | rl-muse-spark-1-3-sglang-playground | 151.6 | 14036 chars | 0 chars | ERROR: CompletionError: Model API returned 403: {"error":{"code":"network_access_required","message":"This API key belongs to an internal Meta team and requires the Meta corporate network. Connect to the corporate VPN and retry.","param":null,"type":"permission_error"}} |
| 10 | scenarios | rl-muse-spark-1-3-sglang-playground | 2814.0 | 14036 chars | 0 chars | ERROR: CompletionError: Model API returned 403: {"error":{"code":"network_access_required","message":"This API key belongs to an internal Meta team and requires the Meta corporate network. Connect to the corporate VPN and retry.","param":null,"type":"permission_error"}} |
| 11 | scenarios | rl-muse-spark-1-3-sglang-playground | 151.2 | 14036 chars | 0 chars | ERROR: CompletionError: Model API returned 403: {"error":{"code":"network_access_required","message":"This API key belongs to an internal Meta team and requires the Meta corporate network. Connect to the corporate VPN and retry.","param":null,"type":"permission_error"}} |
| 12 | scenarios | rl-muse-spark-1-3-sglang-playground | 150.9 | 14036 chars | 0 chars | ERROR: CompletionError: Model API returned 403: {"error":{"code":"network_access_required","message":"This API key belongs to an internal Meta team and requires the Meta corporate network. Connect to the corporate VPN and retry.","param":null,"type":"permission_error"}} |
| 13 | scenarios | rl-muse-spark-1-3-sglang-playground | 249.8 | 14036 chars | 27389 chars |  |
| 14 | scenarios | rl-muse-spark-1-3-sglang-playground | 115.1 | 38300 chars | 15209 chars |  |
| 15 | scenarios | rl-muse-spark-1-3-sglang-playground | 57.8 | 29499 chars | 15532 chars |  |
| 16 | scenarios | rl-muse-spark-1-3-sglang-playground | 258.1 | 14036 chars | 22777 chars |  |
| 17 | scenarios | rl-muse-spark-1-3-sglang-playground | 57.0 | 37144 chars | 24095 chars |  |
| 18 | scenarios | rl-muse-spark-1-3-sglang-playground | 147.3 | 38298 chars | 10159 chars |  |
| 19 | scenarios | rl-muse-spark-1-3-sglang-playground | 175.7 | 14036 chars | 23359 chars |  |
| 20 | scenarios | rl-muse-spark-1-3-sglang-playground | 119.1 | 15256 chars | 34932 chars |  |
| 21 | scenarios | rl-muse-spark-1-3-sglang-playground | 99.0 | 38377 chars | 16969 chars |  |
| 22 | triage | rl-muse-spark-1-3-sglang-playground | 61.7 | 9274 chars | 646 chars |  |
| 23 | coder | rl-muse-spark-1-3-sglang-playground | 128.7 | 31196 chars | 21060 chars |  |
| 24 | coder | rl-muse-spark-1-3-sglang-playground | 112.5 | 54912 chars | 39030 chars |  |
| 25 | coder | rl-muse-spark-1-3-sglang-playground | 57.8 | 97976 chars | 39277 chars |  |
| 26 | triage | rl-muse-spark-1-3-sglang-playground | 143.8 | 9325 chars | 726 chars |  |
| 27 | coder | rl-muse-spark-1-3-sglang-playground | 97.0 | 31185 chars | 18716 chars |  |
| 28 | coder | rl-muse-spark-1-3-sglang-playground | 51.3 | 52097 chars | 19388 chars |  |
| 29 | coder | rl-muse-spark-1-3-sglang-playground | 79.0 | 73792 chars | 20276 chars |  |
| 30 | coder | rl-muse-spark-1-3-sglang-playground | 59.1 | 96350 chars | 23771 chars |  |
| 31 | coder | rl-muse-spark-1-3-sglang-playground | 60.8 | 122662 chars | 23579 chars |  |
| 32 | triage | rl-muse-spark-1-3-sglang-playground | 47.1 | 5670 chars | 658 chars |  |
| 33 | design | rl-muse-spark-1-3-sglang-playground | 144.3 | 5784 chars | 12032 chars |  |
| 34 | critic | rl-muse-spark-1-3-sglang-playground | 441.5 | 4388 chars | 0 chars | ERROR: URLError: <urlopen error timed out> |
| 35 | triage | rl-muse-spark-1-3-sglang-playground | 143.7 | 9325 chars | 573 chars |  |
| 36 | scenarios | rl-muse-spark-1-3-sglang-playground | 267.7 | 14424 chars | 17115 chars |  |
| 37 | scenarios | rl-muse-spark-1-3-sglang-playground | 248.5 | 15117 chars | 34708 chars |  |
| 38 | scenarios | rl-muse-spark-1-3-sglang-playground | 148.8 | 38765 chars | 22795 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 6aff3768a63d9c28, 30202 chars. no coder call in the log carries this hash
- the coder was called 11 time(s); the last was call 31

## The game file

- `game.json`: sha256 59732fa9d83f7f79
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 28 of 28 pass
- tier 0 (valid, ends, replays identically): passed; results over 20 random matches: {'seat 1': 6, 'seat 5': 5, 'seats 1 and 5': 1, 'seat 2': 4, 'seat 4': 2, 'seat 3': 1, 'seats 1 and 2': 1}
- reasoning and balance: not checked here (real models will play it later)

