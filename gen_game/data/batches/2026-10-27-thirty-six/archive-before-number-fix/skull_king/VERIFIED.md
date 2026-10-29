# Verification of skull_king

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 59.3 | 1088 chars | 9703 chars |  |
| 02 | critic | claude-opus-5-5 | 54.5 | 3636 chars | 4816 chars |  |
| 03 | spec | claude-opus-5-5 | 42.0 | 2528 chars | 10548 chars |  |
| 04 | scenarios | claude-opus-5-5 | 56.9 | 12494 chars | 7897 chars |  |
| 05 | scenarios | claude-opus-5-5 | 38.9 | 21203 chars | 9588 chars |  |
| 06 | coder | claude-opus-5-5 | 93.4 | 28080 chars | 22253 chars |  |
| 07 | coder | claude-opus-5-5 | 81.2 | 51104 chars | 23792 chars |  |
| 08 | coder | claude-opus-5-5 | 70.9 | 52541 chars | 23725 chars |  |
| 09 | triage | claude-opus-5-5 | 18.8 | 10185 chars | 1571 chars |  |
| 10 | scenarios | claude-opus-5-5 | 50.1 | 13561 chars | 6480 chars |  |
| 11 | scenarios | claude-opus-5-5 | 27.9 | 20852 chars | 7196 chars |  |
| 12 | triage | claude-opus-5-5 | 12.3 | 10295 chars | 1104 chars |  |
| 13 | coder | claude-opus-5-5 | 92.5 | 28893 chars | 22769 chars |  |
| 14 | coder | claude-opus-5-5 | 84.8 | 52433 chars | 24158 chars |  |
| 15 | coder | claude-opus-5-5 | 74.1 | 53572 chars | 24088 chars |  |
| 16 | triage | claude-opus-5-5 | 10.8 | 10322 chars | 997 chars |  |
| 17 | design | claude-opus-5-5 | 57.9 | 8152 chars | 9977 chars |  |
| 18 | critic | claude-opus-5-5 | 63.4 | 3879 chars | 4487 chars |  |
| 19 | spec | claude-opus-5-5 | 48.1 | 2771 chars | 11867 chars |  |
| 20 | scenarios | claude-opus-5-5 | 82.5 | 13835 chars | 11137 chars |  |
| 21 | scenarios | claude-opus-5-5 | 44.1 | 25851 chars | 13122 chars |  |
| 22 | coder | claude-opus-5-5 | 76.9 | 28678 chars | 19580 chars |  |
| 23 | coder | claude-opus-5-5 | 69.0 | 49029 chars | 22315 chars |  |
| 24 | triage | claude-opus-5-5 | 23.1 | 9971 chars | 1385 chars |  |
| 25 | scenarios | claude-opus-5-5 | 95.1 | 14699 chars | 8852 chars |  |
| 26 | scenarios | claude-opus-5-5 | 56.3 | 24774 chars | 13435 chars |  |
| 27 | triage | claude-opus-5-5 | 10.6 | 10013 chars | 864 chars |  |
| 28 | coder | claude-opus-5-5 | 87.0 | 29220 chars | 20778 chars |  |
| 29 | coder | claude-opus-5-5 | 79.0 | 50769 chars | 23242 chars |  |
| 30 | coder | claude-opus-5-5 | 67.9 | 53131 chars | 23089 chars |  |
| 31 | triage | claude-opus-5-5 | 8.4 | 10055 chars | 895 chars |  |
| 32 | design | claude-opus-5-5 | 55.1 | 7879 chars | 10051 chars |  |
| 33 | critic | claude-opus-5-5 | 69.2 | 4130 chars | 5851 chars |  |
| 34 | design | claude-opus-5-5 | 68.7 | 7790 chars | 11128 chars |  |
| 35 | critic | claude-opus-5-5 | 51.7 | 3667 chars | 4421 chars |  |
| 36 | spec | claude-opus-5-5 | 47.5 | 2558 chars | 10825 chars |  |
| 37 | scenarios | claude-opus-5-5 | 40.4 | 12663 chars | 5309 chars |  |
| 38 | scenarios | claude-opus-5-5 | 25.2 | 19264 chars | 6318 chars |  |
| 39 | coder | claude-opus-5-5 | 77.8 | 27457 chars | 18516 chars |  |
| 40 | coder | claude-opus-5-5 | 71.2 | 46744 chars | 26801 chars |  |
| 41 | coder | claude-opus-5-5 | 75.7 | 52311 chars | 27523 chars |  |
| 42 | coder | claude-opus-5-5 | 93.0 | 52650 chars | 26680 chars |  |
| 43 | coder | claude-opus-5-5 | 94.1 | 52311 chars | 27445 chars |  |
| 44 | triage | claude-opus-5-5 | 14.8 | 6203 chars | 1192 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 869d39e37a33c315, 27457 chars. MATCHES call 39: this is exactly what was sent.
- the coder was called 16 time(s); the last was call 43

