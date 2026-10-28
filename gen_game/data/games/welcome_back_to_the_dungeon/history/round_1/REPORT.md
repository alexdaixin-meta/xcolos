# welcome_back_to_the_dungeon: needs review

Built from the variation **Back to the Dungeon: Single Delve** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Use one fixed adventurer: base HP 3 and five equipment items (Armor +5 HP, Shield +3 HP, Torch defeats strength 3 or less, Holy Water defeats Vampires and the Lich, Dragon Spear defeats the Dragon). Use a fixed 13-card monster deck with strengths 1-9. (fixes: Four adventurers with six unique, partly special-ability equipment tiles is too much state and too many rule exceptions for the complexity limits.): Keeps the identity of equipment that adds HP or defeats monster types, while cutting rule exceptions to a single damage calculation.
- One round is one player's turn. Cap the game at 40 rounds, with a tiebreak at the cap: most successes among surviving players, then fewest failures, otherwise a draw. (fixes: Game length is unbounded: dungeons repeat until someone has two successes or is the last one standing, with no round cap.): Gives a bounded, buildable loop and a result decided by arithmetic even if no one reaches two successes.
- No adventurer choice. The first player of each new dungeon is the next surviving player clockwise from the previous runner. (fixes: The winner of a run picks the next adventurer, a rich-get-richer seat advantage that also fixes who leads the next bidding.): Removes the snowball and spreads the leading position evenly.
- Each round, before the active player acts, every surviving player writes one short message at the same time. All messages are then shown. (fixes: Bluffing about what you drew is the heart of the game, but there is no structured way to communicate, so the platform would lose the claim-and-read element.): Gives bluffing a structured channel: claims about what was added or removed, which others must test against public facts.
- Announce each round the dungeon size, the remaining equipment, the deck size and who has passed. Monster identities stay private to whoever drew them. (fixes: Which information is public (dungeon size, remaining equipment, deck size) is implicit in the physical game and must be stated for a text engine.): Makes clear exactly what can be inferred and from what.
- Use several dungeons per game within 40 turns, with a reshuffle each dungeon. Two successes still win, two failures still eliminate, and the tiebreak at the cap counts every run. (fixes: Deck luck can decide a short game when no fallback or tiebreak exists.): More dungeons per game let skill average out over deck order.

Objective: The first player to reach 2 successes wins. A player is also the winner if every other player has been eliminated by 2 failures. If neither happens by the end of round 40: among non-eliminated players, the highest successes wins, then the fewest failures; any remaining tie is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. Deck strengths total 2+4+6+8+10+6+7+9 = 52. Damage defeated by each item: Torch 1+1+2+2+3+3 = 12; Holy Water 4+4+6 = 14; Spear 9. HP with both HP items is 11, with Armor only 8, with Shield only 6, with neither 3. With all five items, only the two Golems and the Demon get through, worth up to 17. A 
- playable: pass. The rules cover every situation. PASS or DRAW is forced to PASS when the deck is empty. ADD or SACRIFICE is allowed only while an item remains. Turns advance past passed and eliminated players. The run is triggered by exactly one non-passed survivor, with explicit HP and damage formulas. There are r
- reasoning_over_luck: pass. Chance enters through the deck order, which decides which cards each player sees. Everything else is inference. Each player knows the deck composition, the cards they drew themselves, the remaining items (public), the dungeon count, and every ADD or SACRIFICE choice, which shows through the item lis

## Complexity

- steps_per_round: designed 16, built 15, limit 20
- choice_steps_per_round: designed 3, built 3, limit 4
- attributes: designed 12, built 55, limit 20 (built: 80)
- hidden_elements: designed 3, built 16, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 40, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: All five items give the runner HP 11
- pass: Without Armor the HP is 3 + 3 = 6
- pass: With no items, damage is the sum of strengths (Golem 5 + Orc 3 = 8) against HP 3
- pass: Torch removes the cards of strength 3 or less: Goblin+Orc+Golem gives damage 5
- pass: Holy Water removes Vampire and Lich: Vampire+Lich+Goblin gives damage 1
- pass: Dragon Spear removes the Dragon: Dragon+Skeleton gives damage 2
- pass: Damage equal to HP (3 vs 3) is a failure
- pass: Damage below HP (2 vs 3) is a success
- pass: A second failure eliminates the runner
- pass: PASS marks the active player as passed and no run happens yet
- pass: With an empty deck only PASS is offered
- pass: DRAW takes one card from the deck (which card is chance, only counts asserted)
- pass: ADD puts the drawn card into the dungeon and the player's added cards
- pass: SACRIFICE Armor removes Armor and discards the card
- pass: SACRIFICE is offered only for items still present
- pass: The turn skips eliminated and passed seats
- pass: The last seat that has not passed runs the dungeon
- pass: A run publishes its damage and HP
- pass: After a run the dungeon is reset and the seat after the runner starts
- pass: A second success wins the game
- pass: The sole survivor wins when the other runner is eliminated
- pass: At round 40 the most successes wins
- pass: At round 40 a tie on successes and failures is shared
- pass: Talk does not change the state; the round goes on

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 4], results {'seat 3': 15, 'seat 2': 13, 'seat 1': 8, 'seat 4': 4}, 16-199 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 70.3 decisions, prompts of 98 characters on average (longest 218)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- always taking the last option as seat 1 wins 88% of decided matches against random seats
- always taking the last option as seat 2 wins 92% of decided matches against random seats
- random seats: {'seat 3': 24, 'seat 2': 24, 'seat 1': 12}
- always `first@seat1`: won 0, lost 60, drew 0
- always `first@seat2`: won 0, lost 60, drew 0
- always `last@seat1`: won 53, lost 7, drew 0
- always `last@seat2`: won 55, lost 5, drew 0

## Triage (whose problem each failure was)

- round 1: revise_rules: The file works as specified, but a mindless fixed policy (always the last option, likely DRAW and then SACRIFICE or ADD) wins about 90% of decided games, and always taking the first option (PASS) never wins. Never passing makes you the runner, and the run is too easy to survive, so the pass-or-draw decision has no real tension.

## Choices the rules did not make

- 3 to 4 players, suggested 3: The designer's suggested size is 3. Three is the smallest table where the bluff about what was secretly added and the pressure of who ends up running both work. Four is the maximum because the 13-card deck gets thin and turns grow long.
- Talk is kept as a simultaneous poll with a broadcast: The source says messages are written at the same time without seeing the others. Players disagree, since nobody wants to be the runner, so claims about added cards are worth reasoning about.
- The dungeon is tracked with hidden counters (total, low, undead, dragon) alongside the card list: These let damage be computed by plain arithmetic, while the card list is what gets revealed.
- The rank expression gives non-eliminated players +1000: This keeps eliminated players from winning the round-40 tiebreak.

## Simplifications

- Drawing the top card of a shuffled deck is a random pick from the deck list: The engine shuffles by drawing at random, and the two are equivalent.
- A draw after round 40 is a shared win among the tied leaders: The engine has no separate draw outcome.
- The run and the new-dungeon steps are single steps with a 'when' condition: The step list is flat, and these are conditional updates rather than alternative blocks.

## Encoding attempts

- 1: players are sent text with a `{name}` that was never filled in: placeholder: players are shown the literal {drawn_card} (in `prompt`: 'You drew: {drawn_card}. Only you know it. ADD it face-down to the dungeon, or SACRIFICE on'); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {drawn_card} (in `prompt`: 'You drew: {drawn_card}. Only you know it. ADD it face-down to the dungeon, or SACRIFICE on'); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {drawn_card} (in `prompt`: 'You drew: {drawn_card}. Only you know it. ADD it face-down to the dungeon, or SACRIFICE on'); use only names the step can fill in (see the broadcast rule: {value} and {seat})
- 2: it plays, but part of it does nothing: player attribute `successes` is never changed in 3 random matches, so nothing updates it. Steps that name it: prepare the first dungeon, the run's result. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.; player attribute `failures` is never changed in 3 random matches, so nothing updates it. Steps that name it: prepare the first dungeon, the run's result. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.; player attribute `eliminated` is never changed in 3 random matches, so nothing updates it. Steps that name it: prepare the first dungeon, the run's result. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.; game attribute `all_monsters` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 3: it plays, but part of it does nothing: player attribute `eliminated` is never changed in 3 random matches, so nothing updates it. Steps that name it: prepare the first dungeon, the run's result. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.; game attribute `dungeon_dragon` is never changed in 3 random matches, so nothing updates it. Steps that name it: prepare the first dungeon, resolve the card, new dungeon. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 4: passed
