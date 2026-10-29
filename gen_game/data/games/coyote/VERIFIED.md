# Verification of coyote

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 115.8 | 954 chars | 9665 chars |  |
| 02 | critic | claude-opus-5-5 | 81.0 | 3172 chars | 6227 chars |  |
| 03 | spec | claude-opus-5-5 | 51.7 | 2197 chars | 11921 chars |  |
| 04 | scenarios | claude-opus-5-5 | 62.0 | 14106 chars | 9123 chars |  |
| 05 | scenarios | claude-opus-5-5 | 35.2 | 23492 chars | 9187 chars |  |
| 06 | coder | claude-opus-5-5 | 82.6 | 28495 chars | 22948 chars |  |
| 07 | coder | claude-opus-5-5 | 56.7 | 52112 chars | 23306 chars |  |
| 08 | triage | claude-opus-5-5 | 10.2 | 9731 chars | 1477 chars |  |
| 09 | scenarios | claude-opus-5-5 | 61.0 | 15088 chars | 9200 chars |  |
| 10 | scenarios | claude-opus-5-5 | 33.8 | 24551 chars | 9290 chars |  |
| 11 | triage | claude-opus-5-5 | 14.2 | 10143 chars | 1418 chars |  |
| 12 | coder | claude-opus-5-5 | 70.2 | 29603 chars | 20185 chars |  |
| 13 | coder | claude-opus-5-5 | 54.3 | 50457 chars | 20543 chars |  |
| 14 | triage | claude-opus-5-5 | 12.0 | 7996 chars | 1403 chars |  |
| 15 | coder | claude-opus-5-5 | 96.6 | 29577 chars | 25758 chars |  |
| 16 | coder | claude-opus-5-5 | 70.7 | 54256 chars | 26107 chars |  |
| 17 | triage | claude-opus-5-5 | 9.3 | 8427 chars | 960 chars |  |
| 18 | scenarios | claude-opus-5-5 | 59.9 | 14643 chars | 9146 chars |  |
| 19 | scenarios | claude-opus-5-5 | 37.2 | 24052 chars | 9219 chars |  |
| 20 | triage | claude-opus-5-5 | 11.4 | 9241 chars | 1277 chars |  |
| 21 | design | claude-opus-5-5 | 73.2 | 7438 chars | 11803 chars |  |
| 22 | critic | claude-opus-5-5 | 52.2 | 4493 chars | 4957 chars |  |
| 23 | design | claude-opus-5-5 | 86.8 | 8209 chars | 11641 chars |  |
| 24 | critic | claude-opus-5-5 | 125.3 | 4505 chars | 6466 chars |  |
| 25 | design | claude-opus-5-5 | 301.9 | 9316 chars | 12249 chars |  |
| 26 | critic | claude-opus-5-5 | 57.4 | 4304 chars | 4630 chars |  |
| 27 | critic | claude-opus-5-5 | 31.7 | 9207 chars | 4998 chars |  |
| 28 | spec | claude-opus-5-5 | 55.4 | 3329 chars | 14204 chars |  |
| 29 | scenarios | claude-opus-5-5 | 102.7 | 16641 chars | 14978 chars |  |
| 30 | scenarios | claude-opus-5-5 | 48.9 | 31882 chars | 15027 chars |  |
| 31 | coder | claude-opus-5-5 | 140.1 | 30519 chars | 32945 chars |  |
| 32 | coder | claude-opus-5-5 | 112.9 | 54902 chars | 32932 chars |  |
| 33 | triage | claude-opus-5-5 | 22.8 | 9731 chars | 1682 chars |  |
| 34 | coder | claude-opus-5-5 | 171.4 | 31742 chars | 32632 chars |  |
| 35 | coder | claude-opus-5-5 | 111.2 | 56600 chars | 33035 chars |  |
| 36 | triage | claude-opus-5-5 | 17.2 | 9945 chars | 1460 chars |  |
| 37 | coder | claude-opus-5-5 | 157.8 | 31608 chars | 26331 chars |  |
| 38 | triage | claude-opus-5-5 | 12.1 | 9972 chars | 1403 chars |  |
| 39 | design | claude-opus-5-5 | 66.0 | 7627 chars | 11964 chars |  |
| 40 | critic | claude-opus-5-5 | 62.2 | 4304 chars | 5525 chars |  |
| 41 | critic | claude-opus-5-5 | 23.5 | 10102 chars | 5717 chars |  |
| 42 | design | claude-opus-5-5 | 88.6 | 9922 chars | 11955 chars |  |
| 43 | critic | claude-opus-5-5 | 49.5 | 4251 chars | 5789 chars |  |
| 44 | design | claude-opus-5-5 | 46.2 | 6437 chars | 11811 chars |  |
| 45 | critic | claude-opus-5-5 | 77.4 | 5005 chars | 6103 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 fab48c4db43668c6, 31608 chars. MATCHES call 37: this is exactly what was sent.
- the coder was called 11 time(s); the last was call 37

## The game file

- `game.json`: sha256 2cad5285ec2c81d1
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **FAIL: tests written independently from the rules disagree with the game: Hand in progress: no new deal and the declaration carries on: rule R6 is broken: When a round starts with hand_active true, then no cards are dealt and the hand continues with the same cards and declarations.; seat 1 was never offered 5, but should have been; Ada: the rule for 5 was never matched (the | Coyote by the first player s**

