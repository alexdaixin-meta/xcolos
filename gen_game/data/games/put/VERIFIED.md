# Verification of put

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 58.1 | 739 chars | 9107 chars |  |
| 02 | critic | claude-opus-5-5 | 45.1 | 2709 chars | 4722 chars |  |
| 03 | critic | claude-opus-5-5 | 19.4 | 7704 chars | 5092 chars |  |
| 04 | design | claude-opus-5-5 | 78.0 | 5003 chars | 10083 chars |  |
| 05 | critic | claude-opus-5-5 | 54.5 | 3585 chars | 5954 chars |  |
| 06 | design | claude-opus-5-5 | 98.1 | 6454 chars | 10655 chars |  |
| 07 | critic | claude-opus-5-5 | 44.9 | 3326 chars | 4986 chars |  |
| 08 | spec | claude-opus-5-5 | 59.2 | 2566 chars | 12874 chars |  |
| 09 | scenarios | claude-opus-5-5 | 61.5 | 14794 chars | 11134 chars |  |
| 10 | scenarios | claude-opus-5-5 | 39.0 | 26191 chars | 11330 chars |  |
| 11 | coder | claude-opus-5-5 | 131.4 | 29867 chars | 27969 chars |  |
| 12 | coder | claude-opus-5-5 | 84.1 | 54391 chars | 28030 chars |  |
| 13 | coder | claude-opus-5-5 | 83.0 | 54391 chars | 30343 chars |  |
| 14 | coder | claude-opus-5-5 | 86.3 | 54546 chars | 30069 chars |  |
| 15 | coder | claude-opus-5-5 | 95.0 | 54391 chars | 30479 chars |  |
| 16 | triage | claude-opus-5-5 | 12.4 | 4611 chars | 1218 chars |  |
| 17 | design | claude-opus-5-5 | 118.1 | 2279 chars | 11310 chars |  |
| 18 | critic | claude-opus-5-5 | 46.8 | 3033 chars | 4286 chars |  |
| 19 | spec | claude-opus-5-5 | 36.5 | 2273 chars | 9370 chars |  |
| 20 | scenarios | claude-opus-5-5 | 63.7 | 11152 chars | 11750 chars |  |
| 21 | coder | claude-opus-5-5 | 74.9 | 27462 chars | 20578 chars |  |
| 22 | coder | claude-opus-5-5 | 53.7 | 48567 chars | 20711 chars |  |
| 23 | coder | claude-opus-5-5 | 69.6 | 48686 chars | 21003 chars |  |
| 24 | coder | claude-opus-5-5 | 56.8 | 48963 chars | 21485 chars |  |
| 25 | coder | claude-opus-5-5 | 55.7 | 49616 chars | 21178 chars |  |
| 26 | triage | claude-opus-5-5 | 5.9 | 9407 chars | 896 chars |  |
| 27 | coder | claude-opus-5-5 | 97.7 | 28112 chars | 22646 chars |  |
| 28 | coder | claude-opus-5-5 | 58.8 | 51283 chars | 22724 chars |  |
| 29 | coder | claude-opus-5-5 | 63.2 | 51349 chars | 22869 chars |  |
| 30 | coder | claude-opus-5-5 | 58.5 | 51969 chars | 22853 chars |  |
| 31 | coder | claude-opus-5-5 | 60.6 | 51478 chars | 22817 chars |  |
| 32 | triage | claude-opus-5-5 | 10.6 | 6163 chars | 1536 chars |  |
| 33 | coder | claude-opus-5-5 | 112.4 | 28687 chars | 24075 chars |  |
| 34 | coder | claude-opus-5-5 | 62.5 | 53209 chars | 24496 chars |  |
| 35 | triage | claude-opus-5-5 | 5.1 | 9387 chars | 730 chars |  |
| 36 | design | claude-opus-5-5 | 60.0 | 6898 chars | 11029 chars |  |
| 37 | design | claude-opus-5-5 | 29.8 | 18274 chars | 11061 chars |  |
| 38 | critic | claude-opus-5-5 | 62.9 | 3758 chars | 4880 chars |  |
| 39 | design | claude-opus-5-5 | 92.7 | 6076 chars | 11449 chars |  |
| 40 | critic | claude-opus-5-5 | 56.6 | 3350 chars | 5246 chars |  |
| 41 | critic | claude-opus-5-5 | 21.0 | 8869 chars | 5263 chars |  |
| 42 | spec | claude-opus-5-5 | 42.4 | 2590 chars | 11360 chars |  |
| 43 | scenarios | claude-opus-5-5 | 49.0 | 13214 chars | 9197 chars |  |
| 44 | coder | claude-opus-5-5 | 73.0 | 28270 chars | 19281 chars |  |
| 45 | coder | claude-opus-5-5 | 53.9 | 48403 chars | 20471 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 1c624bb9d9418ec6, 28270 chars. MATCHES call 44: this is exactly what was sent.
- the coder was called 19 time(s); the last was call 45

## The game file

- `game.json`: sha256 04661d44986f34aa
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 18 of 18 pass
- tier 0 (valid, ends, replays identically): passed; results over 20 random matches: {'seat 1': 10, 'seat 2': 10}
- reasoning and balance: not checked here (real models will play it later)

