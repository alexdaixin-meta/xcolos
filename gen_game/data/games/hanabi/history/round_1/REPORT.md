# hanabi: needs review

Built from the variation **Hanabi: Three Fireworks** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Use a 30-card deck in 3 colours (three 1s, two each of 2, 3 and 4, one 5 per colour), 2 to 4 players, hand size 5 with 2 players and 4 with 3 or 4 players, and a cap of 40 turns. (fixes: The full game (50 cards, 5 colours, hands of 4 to 5, up to 5 players) is too long and carries too much state for the 40-round, 20-attribute limits.): This keeps the structure of Hanabi (scarce 5s, duplicated low cards, the hint economy) while making a game fit in 40 turns and a handful of tracked numbers.
- Add a team target: the team wins if the final fireworks score is at least 10 (2 or 3 players) or 9 (4 players). Losing the last fuse sets the team score to 0. Every player's total equals the team score, and the engine's target rule declares everyone a winner or nobody. (fixes: The original produces only a score, and the engine can only declare winners or a draw. A cooperative game needs a win threshold.): The engine can only declare winners. A threshold turns the cooperative score into a shared win or loss, and it needs real coordination to reach.
- At the start of each turn, the engine sends the active player, through a private channel, the faces of every other player's hand plus only the IDs of their own hand. (fixes: Owner-blind hands are the inverse of supported hidden hands, and the mechanism for showing each player the other hands was not stated.): This states the supported mechanism for owner-blind hands. Only the active player needs the view, so one step per turn is enough.
- Remove the copies-outstanding table entirely. Players work it out themselves from the public discard pile and the three pile values, both shown every turn. (fixes: The previous variation tracked a copies-outstanding table of 15 numbers. That pushed the tracked numbers to at least 23, over the limit of 20.): This removes 15 attributes and all the lookup updates. The information is still fully available, and doing the counting is part of the reasoning.
- No colour-by-rank cell is ever updated. Cards are strings such as 'R3' in game lists (deck, hands, discard pile), and only the three pile values change. (fixes: Updating a 15-cell colour-by-rank table on every play or discard needs lookup logic the engine lacks, costing roughly 15 to 20 steps by itself.): Without a table there is nothing to look up, so plays and discards cost a few list operations.
- Keep only: piles R, G and B; hint tokens; fuses; deck count; turns played; final-round counter; team score; target; the action this turn; a play-success flag; the deck, discard and hint-log lists; and each player's hand list and score. That is 17 in all. (fixes: The copies table is redundant. It can be derived exactly from the public discard pile and pile values, so it spends budget without adding information.): This is an honest attribute budget under 20.
- Recount the turn as 18 explicit steps, each with a `when` condition. The 4 ordered end checks are merged into 2 steps that use `or`. The final round is handled by one counter, decremented before it is triggered. (fixes: The previous step count (12) was understated. Validation, hint resolution, the play test, the pile update, fuses, bonuses, the draw, the final round and the end checks were not all counted.): This gives an honest step count within the 20-step limit, with every rule accounted for.
- Resolve the validity check, hint matching and the play test each as a single referee rule check. Examples: 'list the IDs in the named hand whose card has the named colour or rank'; 'the revealed card's rank equals its colour's pile value plus 1'. The pile is then raised by one step with three `if` operations. (fixes: Hint matching done card by card, and the play test done as a 3-way colour lookup, would each cost several steps per turn.): Each of these replaces several per-card or per-colour comparison steps with one step.

Objective: When the game ends, every player's total equals the team score: the sum of the three pile tops, or 0 if the last fuse was lost. If that total is at least the target (10 with 2 or 3 players, 9 with 4 players), every player wins together. Otherwise no player reaches the target, the team has lost, and the engine records the result as no winner (a shared draw). No player can ever win alone.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. This is a fully cooperative game. Every player's total is set to the same team score, and all win or all draw together. Seat order therefore gives no player an edge over another. Information is symmetric: each player sees every hand except their own.

Card counts check out:
- 3 colours x (3+2+2+2+1)
- playable: pass. Rules are complete. Each of the three actions has explicit legality conditions, and every invalid case is enumerated with a defined default (DISCARD oldest). Token cap (8), fuse loss, pile-completion bonus, draw timing, and the ID system (stable public IDs, faces hidden from the owner) are all speci
- reasoning_over_luck: pass. Chance is the single initial shuffle. Everything after it is decided by inference and planning:
- **Hint economy:** 8 tokens shared by a team that must make 10+ successful plays.
- **Implicature:** inferring why a teammate gave a particular hint, or chose to discard rather than hint.
- **Card counti

## Complexity

- steps_per_round: designed 18, built 14, limit 20
- choice_steps_per_round: designed 1, built 1, limit 4
- attributes: designed 17, built 67, limit 20
- hidden_elements: designed 2, built 22, limit 3
- random_draws_per_round: designed 0, built -, limit 1
- rounds: designed 40, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: R1: setup builds 30 cards, 4 per hand with 3 players and 18 in the deck (chance-free counts only)
- pass: R2: every card gets an ID, so the deck and hands hold 30 IDs in total (chance-free counts only)
- pass: R3: 2 players get 5 cards each and deck_count starts at 20
- pass: R4: 3 players get 4 cards each and deck_count starts at 18
- pass: R4: 4 players get 4 cards each and deck_count starts at 14
- pass: R5: starting tokens, fuses, piles, turns and final-round counter
- pass: R6: with 4 players the target is 9, so ending on a score of 9 is a win
- pass: R7: after a turn the public state reflects the move (hint spent, turn counted, nothing discarded)
- pass: R8: the active seat acts only on its own IDs, never on another seat's IDs
- FAIL: R9: seat 1 then seat 2 act; seat 3 is not yet asked after two turns | rule R9 is broken: When turns pass, seats act in order 1, 2, ..., num_players, then seat 1 again, starting with seat 1.; game discard_pile: expected ['#11=R1', '#21=G2'], got ['#11=R4', '#21=R3']; Cleo: the rule for 'DISCARD #25' was never matched (the game never put that option to this seat)
- pass: R10: a legal colour hint costs 1 token and is logged
- pass: R11: with 0 hint tokens no hint is offered
- pass: R12: no hint to oneself and no hint matching no card is offered; a legal hint is logged
- FAIL: R13: a discard reveals the card to discard_pile, gains a token and draws a replacement | rule R13 is broken: When a seat discards an ID from its own hand, the card's face is revealed, it goes to discard_pile, and hint_tokens rises by 1, to at most 8.; game discard_pile: expected ['#12=G1'], got ['#12=B2']
- FAIL: R14: discarding at 8 hint tokens keeps 8 | rule R14 is broken: When a seat discards with hint_tokens = 8, hint_tokens stays at 8.; game discard_pile: expected ['#12=G1'], got ['#12=R4']
- FAIL: R15: playing R1 on an empty red pile raises it to 1 | rule R15 is broken: When a seat plays a card whose rank is exactly 1 more than its colour's pile, that pile becomes the card's rank.; seat 1 total: expected 1, got 0; seat 2 total: expected 1, got 0; seat 3 total: expected 1, got 0; game pile_red: expected 1, got 0; game fuses: expected 3, got 2; game discard_pile: expected [], got ['#11=G3']; game team_score: expected 1, got 0
- FAIL: R16: completing a pile with a 5 gains a hint token | rule R16 is broken: When a successful play brings a pile to 5, hint_tokens rises by 1, to at most 8.; game pile_blue: expected 5, got 4; game hint_tokens: expected 7, got 6; game fuses: expected 3, got 2; game discard_pile: expected [], got ['#13=R2']; game team_score: expected 5, got 4
- FAIL: R17: playing R2 on an empty red pile fails, burns a fuse and goes to discard_pile | rule R17 is broken: When a seat plays a card whose rank is not exactly 1 more than its colour's pile, the card goes face up to discard_pile and fuses drops by 1.; game discard_pile: expected ['#14=R2'], got ['#14=G4']
- FAIL: R18: invalid moves (hint at 0 tokens, self-hint, foreign or deck IDs) are never offered | rule R18 is broken: When an answer is unreadable, a hint at 0 tokens, a hint to oneself, a hint matching no card, or names an ID not in one's own hand, it is replaced by DISCARD of the oldest ID in the active seat's hand.; game discard_pile: expected ['#11=R1'], got ['#11=G1']
- FAIL: R19: each discard draws the top deck card into the hand, and the drawn ID becomes playable | rule R19 is broken: When a seat discards or plays and deck_count > 0, the top deck card is added to the end of its hand, its ID is announced, and deck_count drops by 1.; game discard_pile: expected ['#11=R1', '#21=G2', '#12=G1'], got ['#11=B4', '#21=G2', '#12=B1']
- pass: R20: giving a hint draws no card
- pass: R21: drawing the last deck card sets final_round_counter to 3 with 3 players
- FAIL: R22: the turn after the last draw lowers final_round_counter from 3 to 2 | rule R22 is broken: When final_round_counter > 0 at the end of a turn after the one that drew the last card, final_round_counter drops by 1.; game discard_pile: expected ['#11=R1', '#21=G2'], got ['#11=B3', '#21=B5']
- FAIL: R23: with the deck empty a discard draws nothing | rule R23 is broken: When final_round_counter has been set, no further cards are drawn because deck_count = 0.; game discard_pile: expected ['#11=R1'], got ['#11=G1']
- FAIL: R24: team_score is the sum of the piles and every total equals it | rule R24 is broken: When a turn ends, team_score = pile_red + pile_green + pile_blue, or 0 if fuses = 0, and every player's total = team_score.; seat 1 total: expected 4, got 3; seat 2 total: expected 4, got 3; seat 3 total: expected 4, got 3; game pile_green: expected 2, got 1; game team_score: expected 4, got 3; game fuses: expected 3, got 2
- pass: R25: losing the last fuse ends the game with score 0 and no winner
- FAIL: R26: reaching 15 ends the game and all players win | rule R26 is broken: When team_score reaches 15 at the end of a turn, the game ends.; result: expected 'all players win', got 'no winner'; seat 1 total: expected 15, got 0; seat 2 total: expected 15, got 0; seat 3 total: expected 15, got 0; game pile_blue: expected 5, got 4; game team_score: expected 15, got 0; game hint_tokens: expected 7, got 6; game turns_played: expected 1, got 3
- pass: R27: final_round_counter reaching 0 ends the game (score 3 is below target, so no winner)
- pass: R28: the 40th turn ends the game (score 6 is below target, so no winner)
- FAIL: R29: with 3 players the game ends at score 10, which meets the target, so all players win | rule R29 is broken: When the game ends with team_score >= target, every player wins together.; game pile_red: expected 5, got 4; game hint_tokens: expected 6, got 5
- pass: R30: with 3 players the game ends at score 9, below the target of 10, so no winner

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [2, 4], results {'no winner': 40}, 5-34 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 13.7 decisions, prompts of 178 characters on average (longest 178)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- every random match ended 'no winner': choices do not change the result
- result names are not 'seat N', so dominance was not checked
- random seats: {'no winner': 60}

## Triage (whose problem each failure was)

- round 1: fix_game: Each attempt failed on a different file-level problem: visible scratch fields, attributes that never change, an unused attribute. The coder has fixed the earlier issues each time, so this is not one failure repeating. The rules are a standard cooperative card game that the engine can express with hidden hands, private views and per-step conditions.
- round 1: fix_tests: The game deals from a random shuffle, as the rules require, yet the failing tests assert specific card faces (#1=R1, #5=R3, #2=G1) that chance decides. The game played seat 1 and then seat 2 correctly, as its discard pile and active_seat show. The self-hint test also assumes the game will offer an invalid self-hint, when the game only offers legal options (no HINT to one's own seat), so the scripted move was never matched.
- round 1: fix_game: The scenarios set each seat's hand through the game's own parallel lists hand_ids and hand_faces. The game instead looks up a revealed card's face in a separate id_faces table built from its own shuffle, so DISCARD and PLAY reveal the wrong face: #11 came out as R4 instead of R1, and the R1 play failed, losing a fuse. Faces and IDs have two inconsistent sources in the file, which is a game-file bug, not a rules or test problem.

## Choices the rules did not make

- 2 to 4 players, suggested 3: The designer suggested 3, so it is kept. The minimum is 2 because hidden-hand cooperation needs at least one teammate who can see your cards. The maximum is 4 because larger tables shrink hands and the deck, and each player's turns grow rare. The key skill is giving hints whose meaning a teammate can read from the timing and from which IDs they mark, while saving tokens and avoiding risky plays.
- No talk phase: The rules forbid all communication except hints, so no talk poll is added.
- Moves offered as a choice list (legal_options) instead of free text: This keeps answers readable and ensures a seat is never offered an illegal move. The invalid-answer fallback, DISCARD of the oldest ID, is kept for unreadable replies.
- Dealing goes one card at a time around the table in seat order: The source says 'deal from the top in seat order' without saying whether cards go one at a time or a full hand at once. Since the deck is shuffled, the outcome is the same in distribution.
- A hand is stored as two parallel lists, hand_ids (public) and hand_faces (others): IDs are announced to everyone, while faces must be hidden from the owner only.
- Final-round timing uses the flag counter_set_this_turn and a decrement step placed before the draw step: This gives each player, from the next seat through the player who drew the last card, exactly one more turn.
- Game results are named 'all players win' and 'no winner': The source describes a shared win or a shared loss recorded as no winner.

## Simplifications

- hand_faces is visible to every non-owner at all times, not only to the active player during their private view: The engine's 'others' visibility is per attribute. Teammates seeing the faces off-turn changes no decision, because only the active player acts and there is no talk.
- The deck is an ordered hidden list and drawing takes its first entry: This matches 'take the top card'. Drawing at random from a shuffled deck would be equivalent.
