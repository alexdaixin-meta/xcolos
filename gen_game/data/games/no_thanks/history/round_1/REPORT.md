# no_thanks: needs review

Built from the variation **No Thanks! Two Laps** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- If every player pays during a round, nobody is forced to take. The card stays in the middle with its pot, and the next round offers it again starting from the same player. This is the original game's continuous circling, cut into laps of at most N offers. (fixes: P1: The forced starter-take rule makes PAY dominant for the starter and near-dominant for everyone, so 'always PAY' is about as good as good play.): Removes the starter's guaranteed profit, so passing a card along is no longer free. The pot grows lap after lap, and every player must judge when the pot is worth the card.
- After a take, the next card is first offered to the taker, as in the original game. (fixes: P3: Under good play each player's cards are just the cards flipped on their start rounds, so the shuffle decides about 80% of results (lottery trap).): Taking now costs tempo: the taker faces a fresh card with an empty pot. Who sees which card first then depends on players' own timing, not on a fixed rotation.
- Burn rule: a card that every player passes in two consecutive rounds is removed from the game. Its pot stays in the middle and becomes the starting pot of the next card. The next card is first offered to the player clockwise of the player who started the burned card's rounds. (fixes: P5: Restoring the original 'card stays until taken' rule could run past the 40-round limit unless the game length is bounded.): Bounds every card to at most 2 rounds. Keeping the pot means chips leave players' hands at N per lap and pile up into jackpots, so passing costs real chips and players can run dry.
- The deck shrinks to 20 cards (13 removed unseen). Every player starts with 11 chips. The game ends when the 20th card has been taken or burned, which takes at most 40 rounds. (fixes: P2: Chips never become scarce (each player's net chip flow is about 0 per cycle), so the original game's central tension of a draining hand and a growing pot is gone.): Keeps the game inside the round limit. With 11 chips and up to 8 chips drained per burned card in a 4-player game, chips become genuinely scarce.
- A player with 0 chips must take. Chip counts stay private, but every action is announced, so others can reconstruct a player's chips from the public history. (fixes: P4: Private chip counts and public history give nothing worth inferring, because nobody is ever forced to take.): Tracking who is nearly broke now matters. Players can pass a high card along to force it onto a player at 0, or avoid feeding a jackpot to someone who needs it.
- The game is limited to 3-4 players. (fixes: P5: Restoring the original 'card stays until taken' rule could run past the 40-round limit unless the game length is bounded.): One lap of offers must fit within 4 choice steps per round.

Objective: The player with the lowest final score (card points minus remaining chips) wins. If several players tie for lowest, the one among them with more remaining chips wins. If they are still tied, the game is a draw among them.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. Main decision: PAY costs exactly 1 point now (one chip lost). TAKE on card c with pot p changes score by Δ = (card-point change) − p. For an isolated card Δ = c − p. For c−1 already held, Δ = −p. For a card that joins two runs, Δ = −(c+1) − p. Example table for N=3, card 20, isolated: lap 1 offer 1 
- playable: pass. The rules cover every situation:
- reveal when there is no current card;
- sequential offers from the lead, stopping at a take;
- forced TAKE at 0 chips (so a burn is impossible while anyone holds 0);
- lap increment, re-offer on lap 1, burn on lap 2 with the pot carried over and the lead moved cloc
- reasoning_over_luck: pass. Chance comes from the 13 removed cards (39% of 33) and the deal order. Estimate: chance decides about 25–35% of results among equally skilled players. With everyone playing well (taking adjacent cards cheaply, letting pots grow on high cards, and timing burns), the winner depends on reading opponent

## Complexity

- steps_per_round: designed 14, built 12, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 11, built 29, limit 20 (built: 80)
- hidden_elements: designed 2, built 9, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 40, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: deck holds 20 cards and 13 are removed
- pass: Setup: every tableau is empty and card points are 0
- pass: Setup: no current card, empty pot, lap 0, lead seat 1
- pass: Drawing a card shrinks the deck, resets lap_count and leaves the pot alone
- pass: Offers start at lead_seat; after the lead seat takes, nobody else is offered the card
- pass: Each PAY adds 1 to the pot and passes the offer to the next seat
- pass: PAY costs the payer 1 chip, seen in the final scores
- pass: A seat with 0 chips is offered only TAKE
- pass: TAKE gives the taker the pot and the card and ends the offers
- pass: The taker becomes lead_seat
- pass: Taking 20 while holding 21 changes card points by 20 - 21
- pass: Taking 20 while holding 19 and 21 changes card points by 0 - 21
- pass: After one full lap the card stays with its pot and the lead seat is unchanged
- FAIL: The next round's offers start again at the same lead seat after one lap | rule R11 is broken: When every player chooses PAY in a round and lap_count becomes 1, then the card stays current with its pot and the next round starts its offers at the same lead_seat.; Ada: the rule for 'TAKE' was never matched (the game never put that option to this seat); Cleo: the rule for 'TAKE' was never matched (the game never put that option to this seat)
- pass: After the second full lap the card is burned, the pot carries over and the lead seat moves on
- pass: After a take, the public state shows the new tableau, the card points and an empty pot
- pass: The last card burns with an empty deck: game ends, pot chips leave the game, all level so all share the win
- pass: Final score is card points minus chips
- pass: Lowest final score wins; a tie goes to the seat with more chips

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 4], results {'seat 1': 12, 'seat 2': 7, 'seat 3': 19, 'seat 4': 2}, 30-56 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 39.8 decisions, prompts of 166 characters on average (longest 166)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- always taking the first option as seat 1 wins 100% of decided matches against random seats
- always taking the first option as seat 2 wins 97% of decided matches against random seats
- random seats: {'seat 1': 12, 'seat 2': 18, 'seat 3': 30}
- always `first@seat1`: won 60, lost 0, drew 0
- always `first@seat2`: won 58, lost 2, drew 0
- always `last@seat1`: won 0, lost 60, drew 0
- always `last@seat2`: won 0, lost 60, drew 0

## Triage (whose problem each failure was)

- round 1: fix_game: In three scenarios the game never actually put a PAY/TAKE choice to the seats: 'moves played' is empty, yet seat 1 ended up holding card 20 with offer ['TAKE']. So the offer step is being resolved inside the file instead of being presented as a real choice. The rules are clear and the engine supports sequential choices, so this is an implementation error.
- round 1: fix_game: The test follows rule 5: after a lap where everyone pays, the card stays current and the next round offers it again from the same lead seat. The game never offered TAKE to the scripted seats in that next round, so the second lap is not being run correctly.
- round 1: fix_game: The test matches the rules: after a full lap of PAYs with lap_count becoming 1, the card stays current and is offered again starting at lead_seat. The game never offered TAKE to Ada or Cleo, so it does not run that second offering round correctly.

## Choices the rules did not make

- 3 to 4 players, suggested 4: This is the designer's count. With 3 or more players, the pot grows enough to make chicken-style refusal tense. More than 4 is not in the source and would stretch a 20-card deck thin.
- current_card = 0 stands for 'no current card': Real cards run from 3 to 35, so 0 is never a real card.
- Revealing the top deck card is a random draw from the hidden deck list: The deck is shuffled, so a random draw is equivalent to taking the top card.
- Offers use sequential ask, not poll: The rules make offers in clockwise order, and each player sees earlier payments and stops once someone takes.
- No talk step: The rules say there is no discussion phase.
- Strategy at the table: A thoughtful player tracks opponents' chips from the public pays and takes. They let the pot grow on cards that extend their own runs, and take a card early when a rival would want it or when their own chips run low.

## Simplifications

- The ranking is one expression: (chips - card_points) * 100 + chips: The engine ranks highest-wins. Negating the score makes lowest-score-wins, and since total chips (at most 44) are under 100, the trailing chips term breaks ties on more chips without disturbing the score order.
- A final_score attribute is computed at game end: It gives an observable score without revealing private chips during play.
- A scratch taken flag tracks whether the card was taken this round: It lets the round skip the remaining offers and decide between a lap and a take with arithmetic.

## Encoding attempts

- 1: it plays, but part of it does nothing: game attribute `burned` is never changed in 3 random matches, so nothing updates it. Steps that name it: everyone paid. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.; game attribute `burn_now` is never changed in 3 random matches, so nothing updates it. Steps that name it: start the round, everyone paid. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 2: passed
