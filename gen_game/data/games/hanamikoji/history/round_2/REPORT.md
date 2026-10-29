# hanamikoji: needs review

Built from the variation **Hanamikoji: Paired Hands** (design round 2); see VARIATION.md.

## What was changed from the original, and why

- Hands are played in pairs: hands 1 and 2 form pair 1, and hands 3 and 4 form pair 2. Within a pair, Player 1 starts the first hand and Player 2 starts the second. Kept counts add up across both hands of the pair, and Geisha markers move only after the second hand of a pair, by comparing these combined counts. (fixes: P1): Each player gets the last-mover position exactly once in every scored contest, and both hands of a pair weigh the same. Both players play the second hand knowing the full first-hand result, so the extra information is shared.
- There are at most 2 pairs (4 hands, 32 rounds). Each player starts exactly 2 hands. (fixes: P2): The number of starts is equal, and the game is shorter and well inside the limit.
- Markers are updated only from combined pair totals, never from a single hand. At the start of hand 3 the pair totals reset to zero, and markers already placed stay where they are when a later pair ties on that Geisha. (fixes: P3): Neither hand of a pair can overwrite the other, so both last-mover hands count equally.
- At the end of the first hand of a pair, the Secrets are revealed and both players' running pair totals are announced. (fixes: P4): Both players play the second hand with the same full knowledge of where they stand, and the deal's swing is averaged over 32 counted cards instead of 16.
- The win is checked after hands 2 and 4 only. After hand 4 the tiebreak is higher Charm, then more Geisha, otherwise a draw. (fixes: P1): This gives a clean end, and the game always stops at a point where the seats are balanced.
- Legality is stated as 'for each Geisha number, how many times you name it must be at most how many of that number are in your hand'. (fixes: P6): The check becomes pure arithmetic.
- The maximum length is 32 rounds instead of 40. (fixes: P5): This gives margin under the 40-round limit.

Objective: After hand 2 and after hand 4: a player with 11 or more Charm from markers on their side wins. Otherwise a player with 3 or more markers on their side wins. Total Charm is 21 and there are 5 Geisha, so at most one player can meet each condition, and Charm is checked first. If nobody has won after hand 4, the higher Charm wins, then the higher Geisha count, and otherwise the game is a draw.

## The critic (3 review(s) before the rules went to a coder)

- balanced: pass. Seats: P1 starts hands 1 and 3 and P2 starts hands 2 and 4, so each player starts exactly one hand in each pair. Within a hand the second player acts last and sees more, but this edge alternates and cancels over every pair. No seat has a net edge.

Cards kept per hand: Secret 1 + own Gift 2 + oppone
- playable: pass. Rules cover every situation:
- Action legality, card-multiset legality, Gift and Competition reveal order, and the opponent's pick are all specified.
- Defaults exist for an illegal action (first unused), illegal cards (lowest cards ascending, first two as pair A) and an illegal pick (counts as 1).

- reasoning_over_luck: pass. Chance enters through the deal, the 1 removed card and the draw order, in 4 independent hands.

Pairing hands smooths the luck. Pair totals sum about 16 kept cards per player across two deals, and markers carry over between pairs, so one bad deal rarely decides a Geisha. I estimate chance decides ab

## Complexity

- steps_per_round: designed 19, built 18, limit 20
- choice_steps_per_round: designed 3, built 3, limit 4
- attributes: designed 15, built 54, limit 20 (built: 80)
- hidden_elements: designed 3, built 9, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 32, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: R1: hand 1 deal gives 6 cards each, sets 1 aside and leaves 8 in the deck; seat 1 then draws and plays Secret
- pass: R2: start of hand 2 resets both players' actions and empties both secrets
- pass: R3: kept lists are unchanged when hand 2 starts
- pass: R3: kept lists are emptied when hand 3 starts
- pass: R4: Victory Markers stay where they are when hand 3 starts
- pass: R5: in hand 2, seat 2 acts in round 1 and seat 1 is not offered an action
- pass: R5: in hand 1, seat 2 acts in round 2
- pass: R6: the active player draws 1 card from the deck before acting
- pass: R8: Secret moves 1 card from the hand to the secret and nothing to kept
- pass: R9: Trade-off moves 2 cards to the discard and they count for nobody
- pass: R10: Gift of the lowest cards 1 2 3; opponent picks offer 2 and keeps the 2, active keeps 1 and 3
- pass: R11: Competition of 1 2 3 4; opponent picks pair B (3 4), active keeps pair A (1 2)
- pass: R12: a card answer not judged legal uses the 4 lowest cards in ascending order; the first two form pair A
- pass: R14: a used action leaves unused_actions
- pass: R15: after Secret the opponent is not asked for a pick and no cards are added to any kept list
- FAIL: R16: at the end of round 8 both secrets are revealed and appended to kept | rule R16 is broken: When round 8 of a hand ends, then each player's secret is revealed and added to their kept.; Blaise: the rule for 'Trade-off' was never matched (the game never put that option to this seat)
- FAIL: R17: at the end of pair 1 markers move to the strictly higher count and stay on a tie | rule R17 is broken: When a pair ends (after hand 2 or 4) and a player's count of Geisha g in kept is strictly higher than the other's, then marker_g moves to that player's side; on a tie it stays.; Ada: the rule for 'Trade-off' was never matched (the game never put that option to this seat)
- FAIL: R18: after pair 1, charm and geisha_count follow the markers (P1 has G5 = 6; P2 has G1 + G2 = 6) | rule R18 is broken: When a pair ends, then charm is the sum of 3,3,4,5,6 over Geisha 1..5 on the player's side and geisha_count is the number of markers on their side.; Ada: the rule for 'Trade-off' was never matched (the game never put that option to this seat)
- FAIL: R19: P1 reaches 11 charm (G4 + G5) at the end of pair 1 and wins over P2 with 3 Geisha | rule R19 is broken: When a pair ends and a player has charm >= 11, then that player wins.; Ada: the rule for 'Trade-off' was never matched (the game never put that option to this seat)
- FAIL: R20: P1 wins 3 Geisha (charm 10) at the end of pair 1 with nobody at 11 charm and wins | rule R20 is broken: When a pair ends, no player has charm >= 11 and a player has geisha_count >= 3, then that player wins.; Ada: the rule for 'Trade-off' was never matched (the game never put that option to this seat)
- pass: R21: pair 1 ends with no winner, so hand 3 is dealt (kept emptied, markers and charm kept)
- FAIL: R22: after hand 4 with no threshold reached, the higher charm wins (9 against 8) | rule R22 is broken: When pair 2 ends with no winner by threshold, then the higher charm wins, then the higher geisha_count, and if both are equal it is a draw.; Ada: the rule for 'Trade-off' was never matched (the game never put that option to this seat)
- FAIL: R22: after hand 4, equal charm (6) is broken by the higher Geisha count | rule R22 is broken: When pair 2 ends with no winner by threshold, then the higher charm wins, then the higher geisha_count, and if both are equal it is a draw.; Ada: the rule for 'Trade-off' was never matched (the game never put that option to this seat)
- FAIL: R22: after hand 4, equal charm and equal Geisha count is a shared result | rule R22 is broken: When pair 2 ends with no winner by threshold, then the higher charm wins, then the higher geisha_count, and if both are equal it is a draw.; Ada: the rule for 'Trade-off' was never matched (the game never put that option to this seat)

## Does the file follow the spec's shape? (flags for a person)

- rule R7 has no scenario: nothing checks it
- rule R13 has no scenario: nothing checks it

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [2], results {'seat 1': 15, 'seat 2': 5}, 31-67 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 66.0 decisions, prompts of 319 characters on average (longest 380)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 1': 42, 'seat 2': 18}
- always `first@seat1`: won 30, lost 30, drew 0
- always `first@seat2`: won 23, lost 37, drew 0
- always `last@seat1`: won 43, lost 17, drew 0
- always `last@seat2`: won 40, lost 20, drew 0

## Triage (whose problem each failure was)

- round 1: revise_rules: The game was built and behaves as specified, and its balance is acceptable (about 29-30 wins per seat against random play, no thoughtless policy dominates). The flaw is structural: each round needs 7 choice steps against a limit of 4. Four action types each take a different number of cards, the active seat alternates, and a second-player pick follows Gift and Competition, so the choices cannot be expressed in so few steps.
- round 2: fix_game: The game deals 7 cards to each player instead of 6. After seat 1's draw and Secret, seat 1 holds 7 cards plus a secret, seat 2 holds 7 without drawing, and the deck has 5 cards (21 - 1 - 7 - 7 - 1). That is an off-by-one in the deal loop, not a problem with the rules or the tests.
- round 2: fix_game: The deal is off by one. After seat 1 drew and played Secret in round 1, the trace shows 7 cards in each hand and 5 in the deck. That means the game dealt 7 cards to each player and left 6 in the deck, when the rules say 6 each and 8 left. The test's figures are correct: seat 1 holds 6 + 1 drawn − 1 Secret = 6, seat 2 holds 6, and the deck holds 8 − 1 = 7.
- round 2: fix_game: All four failing scenarios break the same way: the active seat in round 8 (Blaise in hand 1, Ada in hand 2) was scripted to play 'Trade-off', but the game never offered that option. Each named seat is the correct active player for that round, and the scenarios that only use Secret or Competition passed, so the most likely cause is that the game builds or names the Trade-off option wrongly, not that the tests are wrong.

## Choices the rules did not make

- Exactly 2 players: The designer fixed the game at 2, and Gift and Competition are built as a split between the active player and one opponent.
- No talk step: The rules have no talk. In a two-player zero-sum game talk adds nothing to reason about.
- A standing attribute used as rank_by: It encodes the ordered win checks (Charm >= 11, then Geisha >= 3, then Charm, then Geisha) as one number. Equal standing gives the draw.
- Pair totals kept as a list `kept`: The total for Geisha g is the count of g in the list. This keeps the five per-Geisha counts in one attribute.
- Ask, not poll, for each choice: Each choice is made by one player in sequence, and the opponent picks after seeing the revealed cards.

## Simplifications

- 'Top card' draws and removals are random picks from the deck list: The engine draws at random from a list, which is equivalent to drawing from a shuffled deck.
- Hand-start, end-of-hand and end-of-pair steps run inside the round list, gated by when-conditions on round_in_hand and hand_number: The step list is flat, and single conditional steps express these phases without choosing between blocks.
- Legality of the written cards is ruled by a judged sentence: Parsing free text and checking it as a sub-multiset of the hand is beyond plain arithmetic. The default and all scoring stay arithmetic.

## Encoding attempts

- 1: playing it with random seats failed: seed 1, 2 players: the match crashed: FlowError: 'len(you.secret) > 0' reads `you` where there is no player
- 2: it plays, but part of it does nothing: game attribute `all_items` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 3: passed
