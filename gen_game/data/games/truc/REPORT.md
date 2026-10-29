# truc: ready for review

Built from the variation **Truc Duel** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Replace free raising with one fixed betting window after the first trick. Both players secretly and simultaneously choose Stay or "Two more". If exactly one raises, the other answers Accept, Fold or Four (a final re-raise the raiser cannot refuse). If both raise, the round is worth 4. (fixes: P1): This keeps raise, bluff, fold and re-raise in a fixed number of steps: one poll plus one conditional answer.
- Play the first trick with simultaneous card choice. After the betting window, each player secretly submits the order of their two remaining cards, which are compared in pairs as tricks 2 and 3. (fixes: P2): Two choice steps replace six or more. Simultaneous play removes the leader advantage and turns card order into a guessing duel. Revealing trick 1 before betting gives each raise real information to read.
- Place betting after trick 1 is revealed. (fixes: P4): Players bet knowing one card of the opponent's hand, and the trick-1 result matters for tie-breaks. A raise becomes a readable, bluffable signal rather than a coin flip.
- Remove the redeal. (fixes: P3): This keeps one random draw (the deal) per round and avoids a conditional block.
- Use an exact round-winner rule: most tricks won. If tied, the winner of the earliest non-spoilt trick takes the round. If all three are spoilt, the round is void. (fixes: P5): This makes every outcome arithmetic and keeps the original's 'spoilt tricks follow the first winner' spirit.
- Keep first to 12 points, but cap the game at 30 rounds. At the cap, the higher score wins and equal scores are a draw. (fixes: P6): This guarantees an end without changing the race in normal play, which lasts about 5 to 12 rounds.

Objective: The first player whose score reaches 12 or more wins. Only one player scores in any round, so two players cannot reach 12 at once. If the game ends at the 30-round cap, the player with the higher score wins, and equal scores are a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. SEATS. Every choice except the response is a simultaneous poll. The responder role comes from the raise poll, not from seat order, and there is no dealer and no redeal option. Neither seat has an edge from move order or information.

RESPONSE TABLE. Let p be the responder's chance of winning the rou
- playable: pass. COMPLEXITY. Choice steps per round: trick-1 card, raise poll, conditional response, order of last two cards = 4 (at the limit, allowed). Steps 15 <= 20; attributes 18 <= 20; hidden elements 1 (hands) <= 3; random draws 1 (one shuffle and deal) <= 1; rounds 30 <= 40.

CONDITIONAL STEPS. 'Skip steps 4
- reasoning_over_luck: pass. WHAT CAN BE INFERRED.
- The opponent's two unseen cards, from the 29 unseen cards minus the opponent's revealed trick-1 card.
- Whether the opponent led high (strong remaining hand less likely) or low (sandbagging).
- What their raise or stay signals, and whether it is a bluff.

HOW TO ACT ON IT.
- 

## Complexity

- steps_per_round: designed 15, built 14, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 18, built 45, limit 20 (built: 80)
- hidden_elements: designed 1, built 8, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 30, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Before any round the deck holds the full 32-card pack and scores are 0
- pass: After a round's deal the deck holds 26 cards; with a fold each hand keeps 2 cards (chance-independent)
- pass: Both STAY makes the round worth 1 and no response is asked
- pass: Both TWO MORE makes the round worth 4 and nobody may fold
- pass: A lone raise by seat 1 makes seat 2 choose ACCEPT, FOLD or FOUR; the raiser is offered nothing
- pass: ACCEPT makes the round worth 2
- pass: FOUR makes the round worth 4 and the raiser gets no further choice
- pass: FOLD gives the raiser 1 point, leaves the responder unchanged and stops play after trick 1
- pass: Without a fold all three cards are played (chance-independent)
- pass: Seat 1 on 11 wins a fold and reaches 12, ending the game
- pass: At the 30-round cap the higher score wins
- pass: At the 30-round cap equal scores share the win

## Does the file follow the spec's shape? (flags for a person)

- rule R2 has no scenario: nothing checks it
- rule R3 has no scenario: nothing checks it
- rule R4 has no scenario: nothing checks it
- rule R11 has no scenario: nothing checks it
- rule R13 has no scenario: nothing checks it
- rule R14 has no scenario: nothing checks it
- rule R15 has no scenario: nothing checks it
- rule R16 has no scenario: nothing checks it

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [2], results {'seat 2': 9, 'seat 1': 11}, 29-68 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 53.0 decisions, prompts of 178 characters on average (longest 275)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 2': 26, 'seat 1': 34}
- always `first@seat1`: won 31, lost 29, drew 0
- always `first@seat2`: won 25, lost 35, drew 0
- always `last@seat1`: won 28, lost 32, drew 0
- always `last@seat2`: won 33, lost 27, drew 0

## Choices the rules did not make

- Exactly 2 players, suggested 2: The designer set 2. The game is a heads-up duel of stakes, folds and trick order, and a third player would break the one-raiser/one-responder structure.
- Cards are stored as their strength numbers 1 to 8, with rank names used in what players are shown: Trick comparison is then plain arithmetic, and suits do not matter.
- No talk phase: The rules say there is none; all information comes from revealed cards and choices.
- The order poll is a choice between the two orderings, not free text: It still offers exactly the two legal orders. The dealt-order fallback is kept for any invalid answer.
- The garbled tie clause ('0-0 with three... see below') is read as: equal trick counts go to the earliest non-spoilt trick's winner, and all three spoilt is void: This is the only consistent reading, and the next bullet of the rules covers the all-spoilt case.
- 'The raiser may not fold' after FOUR, and 'no one may fold' after both raise, are built as no further question being asked: The rules give no later folding opportunity, so these lines mean the stakes are fixed.
- A draw at the round cap is equal scores sharing the win: The ranking treats players level at the top as sharing the win.

## Simplifications

- Trick comparison uses table scratch attributes seat1_card and seat2_card: The engine has no direct player-to-player attribute comparison; a table copy is the stated workaround.
- Reshuffling the full pack is a reset of the deck list followed by random draws: The engine draws by picking at random from a list, which is the same as shuffling.

## Encoding attempts

- 1: it plays, but part of it does nothing: game attribute `full_pack` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `rank_names` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 2: passed
