# Play review: Coup (XColos)

Verdict: **GAPS**

I recomputed every coin, card and deck change across all 21 turns, and each one follows the DESIGN and the SPEC. That covers costs, challenge swaps, first-challenger priority, eliminations, skipping eliminated seats and the last-alive win. Every seat was offered only legal options and targets, and no hidden information leaked. The gaps are in what players see and in the platform's final status: no rules brief appears in the offered prompt, the state line is full of blank and unlabeled bookkeeping, and all four seats are still shown as 'active' after the game ended.

## The play

- players ['connector', 'connector', 'connector', 'connector'], seed 263796; ended, winner seat 2, 21 rounds, 61 decisions
- model calls 1 (errors 0, average 16.7s); degraded turns 0; answered by the engine 3
- trace check: blank: the state shown to players has empty fields (action, block_role, claimed_role, winner) in `your_hidden_cards`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed (x84)
- trace check: blank: the state shown to players has empty fields (action, block_role, claimed_role, winner) in `your_cards`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed (x4)

## Alignment with the idea

This is still the Coup in the IDEA: hidden roles, bluffed claims (seat 4's Duke block and Duke taxes), challenges that cost the loser a card, and last player standing wins. The changes the play exercised (simultaneous single-poll reactions, first-challenger priority, draw-1/return-1 Exchange, first player starting with 1 coin) are all listed in the DESIGN with reasons.

## Gaps

### F1 [game_file, medium] end of game (after round 21), all seats

- observed: FINAL SEAT STATUS shows 'seat 1 Ada: active, seat 2 Blaise: active, seat 3 Curie: active, seat 4 Dirac: active'. Seat 1 was eliminated in turn 8, seat 3 in turn 9 and seat 4 in turn 21, and seat 2 won.
- expected: Seats 1, 3 and 4 should show as eliminated or lost, and seat 2 as the winner. SPEC R29 sets alive=false and R34 names the winner, and the platform status should reflect both.
- fix: When the game file sets alive=false, also mark the seat eliminated to the platform, and declare seat 2 the winner at R34. If the game file already does this, then the engine is failing to map it to seat status.

### F2 [prompt, medium] FIRST QUESTION, seat 1 (and every action question)

- observed: Apart from state dumps, the whole question was: 'Choose your action. Tax claims Duke, assassinate claims Assassin, steal claims Captain, exchange claims Ambassador; claims can be challenged.' Nothing says what each action gains or costs (Income 1, Foreign Aid 2, Coup 7, Tax 3, Assassinate 3, Steal 2, Exchange draw 1 / return 1). Nothing says who may block what, what a challenge costs either side, that 10+ coins forces Coup, or how the game is won, including the 40-turn cap.
- expected: PROMPT: the players need the rules brief from the DESIGN, covering actions, costs, blocks, challenge outcomes and the ending.
- fix: Include a rules brief in the system prompt or the first question. Give a one-line effect next to each option, for example 'tax: +3 coins, claims Duke'.

### F3 [prompt, low] every round, the private 'Your hidden cards' line to each seat

- observed: The line prints raw bookkeeping with empty values, such as 'action , ... block_role , ... claimed_role , ... winner .'. trace_lint counts 84 of these lines plus 4 more. It also prints 'standings [[1, 5], [2, 4], [1, 3], [2, 3]]' with no labels; these appear to be [hidden_count, coins] in seat order. The action announcement for Income/Coup reads 'Claimed role: . Target seat: 0 (0 means none).'
- expected: PROMPT: show only what a player can use, with labels, and never print empty fields.
- fix: Hide the game-level bookkeeping attributes (action, claimed_role, block_role, winner, challenger, etc.) from the private line, or skip any that are empty. Label standings or drop them, since the public per-seat blocks already carry the same data. Leave out 'Claimed role'/'Target' when they don't apply.

### F4 [prompt, low] rounds 0-1 and every STATE step

- observed: Players get their hand twice before the first decision: 'Your two hidden role cards' in round 0, then 'Your hidden cards' in round 1, with the same content. Each seat's public block repeats the header 'Seat X is the active player and the deck holds 7 cards. Coins, revealed cards and hidden card count of the other players:', which is already in the turn announcement.
- expected: PROMPT: avoid repeated text, and print one state summary per turn.
- fix: Merge the per-seat blocks into a single table under one header, and drop either the round-0 deal message or the round-1 repeat.

### F5 [game_file, low] round 2, seat 1; round 12, seat 4

- observed: Seat 1 was asked `choose_the_card_to_reveal` with options ['Duke', 'Duke']. Seat 4 was asked `choose_the_card_to_return` with options ['Ambassador', 'Ambassador']. Both options are identical cards, so there was nothing to decide.
- expected: INTERFACE: ask only what needs deciding. The engine already auto-answers single-option target choices (rounds 11, 20, 21).
- fix: Remove duplicate card names from the options before asking, and auto-resolve when only one distinct card remains.

## Where the fixes belong

- prompt: 3
- game_file: 2

## Rules

- seen at work: R1, R2, R3, R5, R6, R7, R8, R10, R11, R12, R13, R15, R17, R18, R19, R20, R21, R23, R28, R29, R30, R32, R33, R34, R36, R37, R38, R39, R40, R41, R42
- not exercised by this play: R4, R9, R14, R16, R22, R24, R25, R26, R27, R31, R35
