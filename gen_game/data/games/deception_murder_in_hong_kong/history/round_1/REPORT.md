# deception_murder_in_hong_kong: needs review

Built from the variation **Deception: Five Clues** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Replace timed in-turn presentations with one written message per round from every player except the Scientist, followed by an accusation poll. (fixes: Timed 30-second presentations and open-ended discussion are real-time; the engine is turn-based.): This is turn-based and text-only.
- The engine deals roles privately. The Murderer chooses the solution as a private choice. The engine privately tells the Accomplice and the Witness who is on the Murderer side. (fixes: The eyes-closed secret setup and the Scientist's role-revealing gestures are physical actions.): Reproduces the secret setup without physical gestures.
- Each non-Scientist holds 2 Clue words and 2 Means words dealt from fixed lists, instead of 4 and 4. (fixes: 4 Clue + 4 Means cards for up to 11 players creates far more state than the 20-attribute limit allows.): Keeps the state within limits while leaving 4 candidate pairs per player and 20 to 28 candidates in total.
- Fix the player range at 6 to 8. The role set is always Scientist, Murderer, Accomplice and Witness, with the rest Investigators. (fixes: Optional Accomplice/Witness and up to 12 players make the role set ambiguous and the step count large.): Gives one unambiguous role table and a bounded state.
- Use 5 rounds with one Scene tile per round. Rounds 1 and 2 use the fixed Cause of Death and Location tiles. Rounds 3 to 5 each draw one tile from a deck of 6. There is no replacement. (fixes: Optional tile replacement plus 6 tiles a round needs more choice steps and random draws per round than allowed.): One Scientist choice and at most one random draw per round, while still giving 5 constrained hints.
- Every accusation is announced with its result. Any correct accusation counts as solved, whoever made it. An accusation naming a Clue and a Means from different players is automatically wrong. (fixes: Rules for a wrong accusation's announcement, and for murderer-side accusations, are informal.): Makes resolution pure arithmetic and makes wrong guesses informative for later rounds.
- Talk is simultaneous: all messages are written without seeing the others, then shown together. (fixes: Turn-order presentations let later speakers copy or react to earlier ones, so the first speaker anchors everyone.): Every player commits to a reading independently.

Objective: Team win, decided purely by matching. If any accusation exactly matches the secret Clue and Means, and the Murderer then fails to name the Witness, the Scientist, the Witness and all Investigators win. If the Murderer names the Witness correctly after a solve, or if no correct accusation happens within 5 rounds, the Murderer and Accomplice win. There are no draws.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. SIZE OF THE PROBLEM. There are 5 to 7 card holders, each with 2 Clues x 2 Means = 4 pairs. That gives 20, 24 or 28 candidate pairs for 6, 7 or 8 players. Only 4 of them belong to the Murderer. The cross-player rule removes every other combination. Honest badges (Witness plus Investigators) number 3,
- playable: pass. Completeness: the roles, the deal (up to 7 x 2 = 14 Clues and 14 Means from lists of 16, no repeats), the solution choice, the tile order (rounds 1 and 2 fixed, 3 to 5 drawn without replacement from 6), the marker, talk, accusation, resolution, Witness Hunt and end are all specified. 'Currently on t
- reasoning_over_luck: pass. Sources of chance: role deal, card deal (how well the Murderer's words fit the scene tiles), the three tile draws, and the base rate in the Witness Hunt. Things to infer: reading the Scientist's 5 markers against 20 to 28 pairs, spotting the Witness's 8-pair knowledge in talk, unmasking Murderer-sid

## Complexity

- steps_per_round: designed 10, built 15, limit 20
- choice_steps_per_round: designed 4, built 7, limit 4
- attributes: designed 12, built 46, limit 20 (built: 80)
- hidden_elements: designed 2, built 19, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 5, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Seat 1 is the Scientist: no cards and no badge
- pass: 7 players: the 6 non-Scientist seats are each dealt cards, so 12 clue words leave the deck (roles hidden, only counts asserted)
- pass: 8 players: setup deals 7 seats (intel hidden, only observable state asserted)
- pass: With stated roles, a round of passes leaves the case unsolved and nobody has won
- pass: Seat 1 holds no cards and every other seat has a badge (Scientist intel is hidden)
- pass: 6 players: seats 2-6 hold 2 clues and 2 means each, decks hold the rest
- pass: Murderer's other own clue and means (Key + Poison) is not the solution: wrong
- pass: A round of passes leaves the case unsolved and no hunt (solution knowledge is hidden)
- pass: Starting badges: seat 1 has 0, all others 1 (kept after a round of passes)
- pass: Round 1 tile is Cause of Death
- pass: Round 2 tile is Location
- pass: Round 3 draws a tile from tile_deck and removes it (which tile is random)
- pass: Scientist marks in round 1 on the Cause of Death tile
- pass: Scientist is never asked to accuse
- pass: A full round of talk and passes keeps every badge
- FAIL: Only badge holders are asked to accuse, and only clues on the table are offered | rule R15 is broken: When accusations are made, then only players with badge 1 are asked, all at the same time, to choose PASS or one Clue on the table and one Means on the table.; seat 6 was offered 'Mask', but must not be
- FAIL: A wrong accuser's badge drops to 0, and the game goes on | rule R16 is broken: When a player accuses, then their badge drops from 1 to 0 and they are not asked to accuse again.; seat 5 badge: expected 0, got 1; Eli: the rule for 'Wallet' was never matched (the game never put that option to this seat); Eli: the rule for 'Insulin' was never matched (the game never put that option to this seat)
- FAIL: Correct accusation Glove + Rope solves the case | rule R17 is broken: When an accusation's Clue equals key_evidence and its Means equals means_of_murder, then it is announced as correct and solved becomes true; otherwise it is announced as wrong.; game solved: expected True, got False; game hunt_target: expected 6, got 0; Blaise: the rule for 6 was never matched (the game never put that option to this seat); Eli: the rule for 'Rope' was never matched (the game never put that option to this seat)
- FAIL: Right clue with the wrong means (Glove + Poison) is wrong | rule R17 is broken: When an accusation's Clue equals key_evidence and its Means equals means_of_murder, then it is announced as correct and solved becomes true; otherwise it is announced as wrong.; Eli: the rule for 'Poison' was never matched (the game never put that option to this seat)
- FAIL: Clue and means from different players (Glove + Knife) is wrong | rule R18 is broken: When an accusation pairs a Clue and a Means from two different players' cards, then it is always wrong.; seat 5 badge: expected 0, got 1; Eli: the rule for 'Glove' was never matched (the game never put that option to this seat); Eli: the rule for 'Knife' was never matched (the game never put that option to this seat)
- pass: Witness Hunt offers only seats other than 1, the Accomplice and the Murderer
- FAIL: Murderer finds the Witness: the Murderer side wins | rule R20 is broken: When the named seat is the Witness, then the Murderer and the Accomplice get won = 1; otherwise the Scientist, the Witness and all Investigators get won = 1.; game solved: expected True, got False; game hunt_target: expected 4, got 0; Blaise: the rule for 4 was never matched (the game never put that option to this seat); Eli: the rule for 'Glove' was never matched (the game never put that option to this seat); Eli: the rule for 'Rope' was never matched (the game never put that option to this seat)
- pass: Murderer misses the Witness: the Investigator side, including the Scientist, wins
- pass: Round 5 ends unsolved: the Murderer side wins
- FAIL: A wrong accusation in round 1 leads to round 2, nobody has won | rule R22 is broken: When no accusation is correct in rounds 1 to 4, then the next round begins.; seat 6 badge: expected 0, got 1; Fay: the rule for 'Watch' was never matched (the game never put that option to this seat); Fay: the rule for 'Drowning' was never matched (the game never put that option to this seat)

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [6, 8], results {'seats 3 and 6': 4, 'seats 5 and 6': 3, 'seats 4 and 5': 7, 'seats 3 and 4': 6, 'seats 2 and 5': 1, 'seats 3 and 5': 3, 'seats 4 and 6': 1, 'seats 2 and 4': 1, 'seats 2 and 3': 2, 'seats 3 and 8': 2, 'seats 5 and 8': 4, 'seats 6 and 7': 1, 'seats 4 and 8': 2, 'seats 2 and 6': 1, 'seats 3 and 7': 1, 'seats 2 and 8': 1}, 42-58 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 49.5 decisions, prompts of 128 characters on average (longest 193)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seats 3 and 6': 9, 'seats 5 and 6': 3, 'seats 4 and 5': 12, 'seats 3 and 4': 5, 'seats 2 and 5': 5, 'seats 3 and 5': 7, 'seats 4 and 6': 9, 'seats 2 and 4': 3, 'seats 2 and 3': 2, 'seats 2 and 6': 2, 'seats 1, 4, 5 and 6': 1, 'seats 1, 3, 4 and 5': 1, 'seats 1, 3, 5 and 6': 1}
- always `first@seat1`: won 0, lost 57, drew 3
- always `first@seat2`: won 0, lost 46, drew 14
- always `last@seat1`: won 0, lost 57, drew 3
- always `last@seat2`: won 0, lost 46, drew 14

## Triage (whose problem each failure was)

- round 1: fix_game: Every failure is a mistake in the game file: a prompt uses a `{acc_clue}` placeholder the step cannot fill, and internal or not-yet-set fields are printed empty. The attempts swing between these two slips, but each has a direct fix inside the rules and interface, so no rule or platform capability is at fault.
- round 1: fix_game: The tests follow the rules: an accuser may name any Clue and any Means word currently on the table. The game never offered seats valid table words such as Glove, Rope or Insulin, so the scripted correct accusations could not be made, and solved, badge and the hunt never progressed. The setup is also inconsistent: the dealt cards and roles disagree with the remaining decks and the intel, solved starts True and is then reset, and hunt_target starts at -1.
- round 1: fix_game: The tests follow the rules, and the game breaks the accusation step. It offered seat 6 'Mask', a word still in clue_deck and not on the table. It never put a Clue and Means choice to accusers, so a badge never dropped and Glove + Rope never solved the case.

## Choices the rules did not make

- 6 to 8 players, suggested 7: Kept the designer's 7. Six is the minimum because the four special roles plus 2 Investigators are needed for the Murderer side to hide. Above 8 the talk becomes too long and the Scientist's single marker per round is spread too thin.
- The accusation is split into two simultaneous polls (Clue or PASS, then Means): Offering every Clue-Means pair would mean up to about 200 options. Answers stay hidden until resolution, so the choice is still effectively simultaneous.
- Talk is kept as a simultaneous poll broadcast to all: The source requires it. Players disagree because the Murderer side wants to mislead, so reading each other's statements against the marker is the core of the game.
- The win is recorded as won = 1 for each player on the winning side, with min_to_win 1: This expresses a team win as an arithmetic ranking.
- The Witness Hunt is a single conditional step inside the round, followed by game_over: A flat step list cannot branch into a separate block, but a step with a 'when' condition works.
- Strategy at the table: The Scientist picks markers that point towards one player's cards. Investigators cross-reference the markers with the face-up cards and spend their single badge carefully. The Murderer and Accomplice steer talk towards innocent pairs. The Witness must hint without revealing themself.

## Simplifications

- The Scientist's ban on sending any other message is enforced by never asking seat 1 to talk: The engine only lets players speak when asked.

## Encoding attempts

- 1: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (current_tile, marker) in `tell_the_solution`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 2: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state a player is shown has empty fields (current_tile, marker); hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 3: it plays, but part of it does nothing: game attribute `tile_table` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `seat_names` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `solved` is never changed in 3 random matches, so nothing updates it. Steps that name it: resolution. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.; game attribute `hunt_target` is never changed in 3 random matches, so nothing updates it. Steps that name it: hunt result. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 4: passed
