# kobayakawa: ready for review

Built from the variation **Kobayakawa Duel Rounds with Table Talk** (design round 2); see VARIATION.md.

## What was changed from the original, and why

- Add one simultaneous, non-binding public talk step after the discards are announced and before the fight poll. Every player writes one short message at the same moment, then all messages are shown. (fixes: The fight decision depends strongly on how many others fight, but the simultaneous silent poll gives no way to learn or influence that, so the poll is largely blind guessing.): Players can now claim strength, threaten to fight, or bluff to deter others. Listeners must judge those claims against K, the discards and past behaviour, which replaces the sequential information of the original with something to reason about.
- State explicitly that messages may be false and bind nobody, and that the fight poll stays simultaneous so no seat speaks or acts last. (fixes: The game has 3-5 players with directly opposed (zero-sum) interests, which is exactly where bluff talk adds reasoning, yet the design was silent on talk and failed the playable check.): Bluffing stays costly to believe, and no fixed seat gains a positional edge.

Objective: After round 10, the player with the most kamons wins. If two or more players tie for most, the game is a draw.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. Payoff of one contest: each fighter stakes 1 and the winner takes the pot plus 1 from the centre. In a 2-way fight the winner nets +2 and the loser -1, so fighting breaks even at a win chance of 1/3. A lone fighter gets the stake back and nets 0. The centre holds 10 and pays at most 1 per round over
- playable: pass. Cards needed per round: with 5 players, 5 hands + 5 reserves + K = 11, within 15, so the fresh-deck deal always works. Every situation is covered: no fighters, a lone fighter, 2+ fighters, ties, a player at 0 (must PASS but still swaps and talks), an empty centre (impossible by count, but handled an
- reasoning_over_luck: pass. Chance is substantial. The deal decides card strength each round, and I estimate about 50-60% of a single round's outcome is chance. Over 10 rounds, decisions accumulate. There is real material to infer from: K is public, every discard and who made it is announced, and a KEEP choice signals a card w

## Complexity

- steps_per_round: designed 18, built 14, limit 20
- choice_steps_per_round: designed 3, built 3, limit 4
- attributes: designed 13, built 30, limit 20 (built: 80)
- hidden_elements: designed 2, built 4, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 10, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Game starts with 5 kamons each, centre 10, round 0
- pass: A round starts and deals; with everyone passing the round advances to 1 and nothing else changes (cards are random, only chance-free facts asserted)
- pass: Kobayakawa card is set after the deal; round completes with no fight and no showdown (K value is random, not asserted)
- pass: Hidden hands: with no showdown no card is revealed
- pass: SWAP is offered; seats that do not swap keep discarded 0 (the swapped card value is random)
- pass: All KEEP: every discarded stays 0
- pass: Every seat is asked KEEP or SWAP
- pass: Talk step runs for everyone and the round completes
- pass: A seat with 0 kamons cannot fight: seats 2 and 3 fight, seat 1 stays out of the showdown
- pass: A lone fighter stakes 1 and gets it back: kamons stay 5
- pass: Nobody fights: no kamons change
- pass: Exactly one fighter: kamon back, card not revealed, centre unchanged, no showdown winner
- pass: Showdown of two: non-fighters stay unrevealed with total 0 (fighters' cards are random)
- pass: Showdown of three resolves to one winner taking the centre bonus (who wins is random)
- pass: Showdown with centre at least 1: centre loses exactly 1
- pass: Showdown with centre 0: centre stays 0
- pass: Showdown: non-fighters are untouched and the centre pays 1 (which fighter loses is random)
- pass: Game ends after round 10; most kamons wins
- pass: Game ends after round 10; tied for most share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 5], results {'seat 3': 8, 'seat 1': 12, 'seat 2': 7, 'seat 4': 3, 'seats 2 and 4': 1, 'seats 3 and 4': 2, 'seat 5': 5, 'seats 3 and 5': 1, 'seats 1 and 4': 1}, 90-150 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 120.0 decisions, prompts of 142 characters on average (longest 164)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 3': 19, 'seat 1': 21, 'seat 2': 17, 'seats 1 and 2': 2, 'seats 1 and 3': 1}
- always `first@seat1`: won 25, lost 34, drew 1
- always `first@seat2`: won 17, lost 37, drew 6
- always `last@seat1`: won 0, lost 56, drew 4
- always `last@seat2`: won 0, lost 58, drew 2

## Triage (whose problem each failure was)

- round 1: fix_tests: The game applied the rule correctly. Seat 2 had 1 kamon after seat 1 fought HIGH (stake 2), so the game recorded PASS for it without asking: fight_choice = PASS, stake 0, kamons still 1, held_rounds now 1, and seat 1 took the pot as the sole fighter. The test failed only because it required a menu offering PASS. A forced pass with no menu has the same result under the rules.
- round 1: revise_rules: The game was built and behaves as specified, but the design needs 22 steps per round, over the engine's limit of 20. The excess comes from the rules, not a coding mistake. A thoughtless 'always last option' policy also wins about half its games from seat 1, which hints that blind aggression pays too well.
- round 2: fix_tests: The rule only says a player with 0 kamons must PASS. The game does this by setting seat 1's fight choice to PASS automatically instead of polling a one-option menu, and seat 1 never fought or staked. The test fails because it insists the forced PASS be shown as an offered option, which is a detail of how the move is presented, not of the rules' outcome.

## Choices the rules did not make

- 3 to 5 players, suggested 4: The designer suggests 4, so it is kept. Below 3 a showdown is just a duel with no one to bluff off the table. Above 5 the 15-card deck cannot cover a hand and a reserve for every player plus K (6 players would need 13 of the 15 cards, leaving swaps and discards nearly fully informative), and one player's choice matters less.
- Table talk kept as a simultaneous poll broadcast to all: The source requires simultaneous messages. Talk earns its place because interests conflict: a player can claim a high card to scare others into passing, or a low card to bait fighters when K is large.
- Reserve cards stored as a hidden table list in seat order: Nobody may see a reserve card, and a player attribute cannot be hidden from its owner, so the reserves live on the table with visibility none.
- The tie-break is coded as the largest (total * 100 - card): Totals are at most 30, so this ranks by total first and by the lower card second. Cards are distinct, so the result is unique.
- Strategy at the table: A thoughtful player weighs K against their card (a low card plus a big K can win), reads public discards and messages, bluffs about strength, and saves kamons near 0, because staying out also keeps them alive.

## Simplifications

- A tie for most kamons at the end is a shared win rather than a declared draw: The engine ranks by one expression and players level at the top share the win, which is how it expresses the source's draw.
