# Verification of reversis

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 56.0 | 866 chars | 10304 chars |  |
| 02 | critic | claude-opus-5-5 | 42.5 | 3449 chars | 4726 chars |  |
| 03 | spec | claude-opus-5-5 | 60.1 | 2562 chars | 13712 chars |  |
| 04 | scenarios | claude-opus-5-5 | 51.3 | 16028 chars | 7259 chars |  |
| 05 | scenarios | claude-opus-5-5 | 35.0 | 24991 chars | 7611 chars |  |
| 06 | coder | claude-opus-5-5 | 118.8 | 30423 chars | 30900 chars |  |
| 07 | coder | claude-opus-5-5 | 117.3 | 55205 chars | 31290 chars |  |
| 08 | coder | claude-opus-5-5 | 122.2 | 55205 chars | 31996 chars |  |
| 09 | coder | claude-opus-5-5 | 111.4 | 55417 chars | 31440 chars |  |
| 10 | coder | claude-opus-5-5 | 127.9 | 55205 chars | 32033 chars |  |
| 11 | triage | claude-opus-5-5 | 8.5 | 10700 chars | 1094 chars |  |
| 12 | scenarios | claude-opus-5-5 | 45.4 | 16770 chars | 8773 chars |  |
| 13 | scenarios | claude-opus-5-5 | 37.7 | 27247 chars | 9147 chars |  |
| 14 | triage | claude-opus-5-5 | 12.3 | 4268 chars | 1456 chars |  |
| 15 | design | claude-opus-5-5 | 55.9 | 2613 chars | 9463 chars |  |
| 16 | critic | claude-opus-5-5 | 40.6 | 3121 chars | 4704 chars |  |
| 17 | critic | claude-opus-5-5 | 18.3 | 8098 chars | 4706 chars |  |
| 18 | spec | claude-opus-5-5 | 43.5 | 2234 chars | 11709 chars |  |
| 19 | scenarios | claude-opus-5-5 | 93.2 | 13779 chars | 14789 chars |  |
| 20 | scenarios | claude-opus-5-5 | 61.6 | 29448 chars | 15679 chars |  |
| 21 | coder | claude-opus-5-5 | 107.4 | 28652 chars | 25562 chars |  |
| 22 | coder | claude-opus-5-5 | 74.7 | 53176 chars | 25633 chars |  |
| 23 | coder | claude-opus-5-5 | 71.9 | 53331 chars | 25625 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 2d9a983a93523f6f, 28652 chars. MATCHES call 21: this is exactly what was sent.
- the coder was called 8 time(s); the last was call 23

## The game file

- `game.json`: sha256 b9bbe466dab3d8ad
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 21 of 21 pass
- tier 0 (valid, ends, replays identically): passed; results over 20 random matches: {'seat 1': 9, 'seat 2': 5, 'seat 4': 6}
- reasoning and balance: not checked here (real models will play it later)

