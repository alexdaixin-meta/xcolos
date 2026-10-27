# hanabi: ready for review

Built from the variation **Hanabi Trio** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Use 3 colours (Red, Green, Blue) with the original rank mix: three 1s, two each of 2/3/4 and one 5, giving 30 cards. Allow 2 to 4 players with fixed hand sizes. Cap the game at 40 turns. (fixes: P1 Length): Keeps every game within 40 turns while preserving the rank scarcity that makes discards dangerous.
- Every seat's total always equals team_score. Every seat whose total reaches 13 (of a maximum 15) wins, so the whole team wins together or all lose together. (fixes: P2 No winner): Turns the cooperative score into an arithmetic win condition. 10 is out of reach of thoughtless play but reachable by careful inference.
- Use a single source of truth for card faces. deck_ids and deck_faces are parallel lists, and each seat's hand_ids and hand_faces are parallel lists. Every move takes entries from the same index of both lists and moves them together. There is no separate lookup table. (fixes: P3 Card-face bookkeeping in the previous build): A face can then never disagree with its card. Discard reveals and play judgements always use the true face.
- At the start of every turn, rebuild legal_options for the active seat only, from that seat's current hand_ids. Clear every other seat's options. (fixes: P4 Legal options in the previous build): A seat can only play or discard cards it actually holds.
- Fix turn order explicitly: seat 1 first, then 2, …, num_players, then seat 1 again. Use a single final_turns_left counter, set to num_players + 1 on the turn the last card is drawn and reduced by 1 at the end of every turn, including that one. (fixes: P5 Turn order and the end-of-deck final round): Gives an unambiguous, testable turn order and end of game with no extra flag.
- Remove id_faces, shuffle_keys, id_labels, rank_pool, hint_values, seat_labels, hand_size and last_move. Merge hint and move logging into one action_log. Hand size follows from num_players. The target 13 is a constant in the rules. (fixes: P6 Attribute budget): Brings the state to 19 attributes and removes the stale copies that caused the bugs.
- Target raised from 10 to 13 of 15 (a person's decision, 2026-10-27). (fixes: play-test: target too easy for strong players): In play-tests Claude teams scored 14, 13 and 13 against a target of 10, so strong play cleared it with room to spare; at 13 a team must lose at most 2 points. Random teams never reached 10.

Objective: Cooperative target. When the game ends, every seat's total equals team_score, which is pile_red + pile_green + pile_blue (maximum 15). Every seat whose total reaches 13 wins, so all seats win together if team_score ≥ 13. Otherwise no seat wins and the game counts as a loss for the whole team. Pile progress is counted even when the game ended because fuses reached 0.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. This is a cooperative game. All totals equal team_score, so the winner rule is: everyone wins if team_score >= 10, otherwise everyone loses. No seat can win or lose alone, so neither seat order nor information gives one seat an edge. Every seat sees all other seats' faces and none of its own, which 
- playable: pass. Rules completeness:
- Every situation is covered: legal options are listed each turn, empty hints are excluded, discarding at 8 tokens is allowed and leaves 8, and drawing stops when the deck is empty.
- Final turns are correct. The last draw sets final_turns_left to N+1, and R16 cuts it to N on tha
- reasoning_over_luck: pass. Chance enters only through the setup shuffle; there are no draws during play.

There is a great deal to infer:
- what your own cards are, from hints received, from which hints were given and which were not, and from discards;
- which cards are critical. Single 5s and the last copies of 2s, 3s and 4s

## Complexity

- steps_per_round: designed 13, built 11, limit 20
- choice_steps_per_round: designed 1, built 1, limit 4
- attributes: designed 19, built 64, limit 20 (built: 80)
- hidden_elements: designed 2, built 18, limit 3
- random_draws_per_round: designed 0, built -, limit 1
- rounds: designed 40, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: 3 players hold 4+4+4 cards and the deck holds 18, 30 cards in all (faces random, only counts asserted)
- pass: Setup: deck_ids and deck_faces are paired lists of equal length (2 players, 20 left)
- pass: A discarded card moves with its id and face together; the paired lists keep equal lengths
- pass: 2 players: hands of 5, deck_count 20
- pass: 3 players: hands of 4, deck_count 18
- pass: 4 players: hands of 4, deck_count 14
- pass: 3-player deal: each seat holds 4 ids, the deck holds the remaining 18 ids
- pass: deck_count tracks deck_ids after two draws
- pass: Hints are offered from other seats' faces, never about one's own hand
- pass: Start state: piles 0, 8 hints, 3 fuses, score 0, empty discard pile, no turns played
- pass: First turn: only seat 1 is asked
- pass: Seats act in order 1, 2, 3
- pass: The active seat may play or discard only its own cards
- pass: With 1 hint token, only hints matching the target's cards are offered
- pass: With 0 hint tokens no hint is offered; the seat discards and regains one
- pass: A hint costs 1 token and moves or draws no card
- pass: Discarding with an empty deck removes the card from both hand lists and draws nothing
- pass: Playing R1 onto an empty red pile succeeds: pile_red 1, team_score 1, every total 1
- pass: A successful 5 with 5 hint tokens raises them to 6
- pass: A successful 5 with 8 hint tokens leaves them at 8
- pass: Playing G2 onto an empty green pile fails: fuses 2, card to discard pile, piles and score unchanged
- pass: Discarding with 5 hint tokens: card to discard pile, tokens 6
- pass: Discarding with 8 hint tokens leaves them at 8
- pass: After a play the player draws the top deck card: hand back to 4, deck down by 1
- pass: 2 players, last card drawn on turn 1: the game ends after 3 turns
- pass: End of turn: every total becomes team_score and turns_played rises by 1
- pass: After seat 3 the turn passes back to seat 1
- pass: A failed play on the last fuse ends the game with score 0: no seat wins
- pass: Playing the last 5 reaches 15 and ends the game: all seats win, a hint token is regained
- pass: 3 players, last card drawn on turn 1: everyone gets one more turn, the game ends after 4 turns
- pass: The 40th turn ends the game
- pass: A turn is a single action by the active seat; other seats are offered nothing
- pass: Game ends on the third fuse with team_score 13: all seats win
- pass: Game ends on turn 40 with team_score 12: no seat wins

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [2, 4], results {'no seat wins': 40}, 4-35 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 14.3 decisions, prompts of 309 characters on average (longest 310)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- result names are not 'seat N', so dominance was not checked
- note: random teams end 'no seat wins' in 100% of matches, as a shared target should; whether thinking play reaches it is for a model play-test
- random seats: {'no seat wins': 60}

## Choices the rules did not make

- 2 to 4 players, suggested 3: The designer chose 3, so it is kept. 2 is the smallest table where hints between players happen. 4 is the source maximum: the 30-card deck leaves only 14 cards to draw, and with more seats each player waits longer between turns and each hint matters less.
- Strategy at the table: A thoughtful player reads the action_log to infer what a hint implies, spends scarce hint tokens on playable or critical cards, discards cards already played or with remaining duplicates, and avoids blind plays that burn fuses. A thoughtless player wastes hints or plays unknown cards.
- No talk phase: R18 forbids any message phase. Limited communication is the core of the game, so no talk poll is added even though there are 3 or more players.
- Turn choice is an ask to the active seat only: The rules give one seat one action per turn, so it is a sequential ask, not a poll.
- final_turns_left and active_seat are public: R6 does not list them. Both can be worked out from public information (deck_count, turn order), and players need to know whose turn it is.
- deck_ids is hidden (none): R6 does not list it as public. Its contents follow from the public hand_ids and discard_pile anyway, and it reveals no faces.
- Results are named 'all seats win' and 'no seat wins': The rules say the team wins or loses together, decided by team_score >= 13.
- The failure log text is 'turn t: seat a plays #id = face, failure': R13 says only that the failure and face are recorded; the wording mirrors the success line in R12.

## Simplifications

- A face's colour and rank are read from its two-character text (colour letter, rank digit): The engine compares numbers and text; this lets rank == pile + 1 and the hint matching be computed arithmetically, with no change to the rules.
- PLAY, DISCARD and HINT are three separate update steps, each guarded by a 'when' on the choice: The step list is flat. Each branch is a single conditional update, which the engine supports.
