# Verification of coup

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design |  | 137.3 | 859 chars | 16714 chars |  |
| 02 | spec |  | 94.1 | 5097 chars | 21696 chars |  |
| 03 | scenarios |  | 166.5 | 24999 chars | 26513 chars |  |
| 04 | triage |  | 23.3 | 13099 chars | 1651 chars |  |
| 05 | scenarios |  | 162.4 | 29700 chars | 27496 chars |  |
| 06 | scenarios |  | 118.7 | 54109 chars | 28248 chars |  |
| 07 | triage |  | 29.3 | 10692 chars | 1991 chars |  |
| 08 | scenarios |  | 237.6 | 31185 chars | 39943 chars |  |
| 09 | triage |  | 36.2 | 13384 chars | 2028 chars |  |
| 10 | scenarios |  | 190.6 | 31142 chars | 26308 chars |  |
| 11 | scenarios |  | 114.7 | 55551 chars | 26876 chars |  |
| 12 | triage |  | 24.5 | 10657 chars | 1713 chars |  |
| 13 | scenarios |  | 178.4 | 31327 chars | 28585 chars |  |
| 14 | scenarios |  | 117.8 | 55736 chars | 29016 chars |  |
| 15 | triage |  | 515.0 | 10470 chars | 1460 chars |  |
| 16 | scenarios |  | 171.7 | 32367 chars | 28352 chars |  |
| 17 | scenarios |  | 120.1 | 56776 chars | 29009 chars |  |
| 18 | triage |  | 20.4 | 12319 chars | 1015 chars |  |
| 19 | scenarios |  | 203.1 | 33623 chars | 31882 chars |  |
| 20 | scenarios |  | 141.8 | 58032 chars | 33082 chars |  |
| 21 | triage |  | 25.9 | 6804 chars | 1957 chars |  |
| 22 | triage |  | 54.1 | 10306 chars | 1846 chars |  |
| 23 | scenarios |  | 52994.4 | 35041 chars | 0 chars | ERROR: CompletionError: claude exited 1: Claude Code at Meta (https://fburl.com/claude.code.users)
Using AI Gateway (Vertex upstream)
SessionEnd hook [/Users/alexdaixin/.config/iterm2/cc-status] failed: Hook cancelled
SessionEnd hook [bash $ |
| 24 | scenarios |  | 176.0 | 34013 chars | 31997 chars |  |
| 25 | triage |  | 40.4 | 10444 chars | 1515 chars |  |
| 26 | scenarios |  | 169.7 | 35079 chars | 30208 chars |  |
| 27 | scenarios |  | 141.2 | 59557 chars | 31344 chars |  |
| 28 | other |  | 22.8 | 13634 chars | 1242 chars |  |
| 29 | triage |  | 11.0 | 7849 chars | 1336 chars |  |
| 30 | other |  | 20.5 | 14126 chars | 904 chars |  |
| 31 | triage |  | 8.5 | 7551 chars | 1079 chars |  |
| 32 | other |  | 16.8 | 13877 chars | 672 chars |  |
| 33 | triage |  | 10.8 | 7305 chars | 1131 chars |  |
| 34 | other |  | 21.0 | 14149 chars | 13 chars |  |

## The prompt the coder was given

- `AGENT_PROMPT.md`: sha256 493cc93ba8531e0c, 48114 chars. no coder call in the log carries this hash (an agent reads this file itself; see logs/agent_output.md)

## The game file

- `game.json`: sha256 bdb041c1313ca420
- the flow's own checks, run again now (loader, arithmetic outcome, random play, every attribute updated, the independent tests): **all pass**
- independent scenarios: 58 of 58 pass
- tier 0 (valid, ends, replays identically): passed; results over 40 random matches: {'seat 1': 7, 'seat 3': 13, 'seat 2': 10, 'seat 4': 5, 'seat 5': 5}
- reasoning and balance: not checked here (real models will play it later)

