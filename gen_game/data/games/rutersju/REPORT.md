# rutersju: ready for review

Built from the variation **Rutersju Hook** (design round 2); see VARIATION.md.

## What was changed from the original, and why

- An exact hit now scores 3 + bid (0→3, 1→4, 2→5, 3→6), and EVERY player who misses loses 2 points per trick of error, not only the declarer. Missing no longer feeds the other players. (fixes: P1): Bidding 0 while holding a card that will win a trick now costs 2 instead of being free. Higher bids are worth a little more, so a player should bid what the hand will take rather than hiding at 0. The slope is kept mild (3 to 6) so that a weak hand bid correctly still scores most of what a strong hand scores.
- The declarer (highest bid) gains +1 extra on an exact hit and loses 1 extra on a miss. Nobody else gains from the declarer's miss. (fixes: P2): This keeps Rutersju's declarer as a real, two-sided risk instead of a gift to the table.
- Bids are now made one at a time, each player hearing the earlier bids. Bidding starts with the player to the left of the priority seat and ends with the priority seat, which rotates every deal. The last bidder may not make the bids add up to exactly 3 (the 'hook'). (fixes: P3, P5): Since exactly 3 tricks are played and the bids cannot total 3, at least one player must miss every deal. This rules out a universal all-zero table. Each bidder must also infer hand strength from the earlier bids. Rotating the last seat spreads the hook's burden and its information advantage evenly across seats.
- Bids are public before the tricks are played, and someone must miss. Trick play therefore becomes deliberate: you can play a high card to give a trick to a 0-bidder, or under-play to deny a bidder their count. (fixes: P4): This turns the luck of the deal into a contest of steering tricks. A weak hand can still score by hitting 0 and by breaking a rival's exact count. A strong hand can be broken by opponents who read its bid.
- The player count is kept at 3–5, with 3 deals per player (9/12/15 deals), the rotating priority seat and the numeric card strengths resolved by highest strength. (fixes: P4): Repeated deals average out the luck of the deal. Rotation removes any seat edge. Simultaneous highest-strength tricks stay within the engine and within 20 steps.

Objective: After 3N deals, the single player with the highest total points wins. A tie for the highest total is a draw.

## The critic (3 review(s) before the rules went to a coder)

- balanced: pass. SETTLEMENT TABLE (d = |bid - tricks|): exact bid 0/1/2/3 scores +3/+4/+5/+6, plus 1 if declarer. A miss by d=1/2/3 scores -2/-4/-6, minus 1 more if declarer. Swing between hitting and missing by 1: bid0 5, bid1 6, bid2 7, bid3 8 points.

LABEL CHECK: 'at least one player misses every deal' is true. 
- playable: pass. RULES: complete. There are 36 unique strengths, so trick ties are impossible. Bidding order, the hook, the declarer tie-break, the no-declarer case, settlement, rotation, end and draw are all specified. Step 3 contains a garbled clause ('can only exceed 3 in this case if… it never matters') but ends
- reasoning_over_luck: pass. CHANCE COMPONENT: hand strength caps the achievable bid, so payoff (3+bid) is partly deal-driven. A trivially weak hand bids 0 for +3; a ♦7♦A♦K hand bids 3 for +7. Per-deal trick potential has SD of about 0.8. Over 9 deals the average differs by about 0.27 tricks per deal, or about 2-3 points of cei

## Complexity

- steps_per_round: designed 15, built 17, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 10, built 39, limit 20 (built: 80)
- hidden_elements: designed 2, built 13, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 15, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Game starts with 0 points, priority seat 1 and no deals completed
- pass: With 5 players the game lasts 15 deals: a game at 14 deals ends after one more deal (leader too far ahead for chance to matter)
- pass: 3 players: each is dealt 3 cards, 27 cards stay in deck all deal
- pass: 4 players: 24 cards stay in deck
- pass: 5 players: hidden deck keeps 21 cards through the deal
- pass: Priority seat 2 bids last after seats 3 and 1 (wraparound), and is refused the hook bid
- pass: A bid is a whole number from 0 to 3
- pass: Others sum to 1: priority seat may bid 0, 1 or 3 but not 2
- pass: Others sum to 3: priority seat may not bid 0
- pass: Others sum to 4: priority seat may bid any of 0 to 3
- pass: Tie for highest bid: the latest bidder of the tied players is declarer
- pass: Unique highest bid makes that player declarer
- pass: All bids 0 means no declarer
- pass: Every player plays one card per trick: all hands empty after 3 tricks (cards random)
- pass: Three tricks are played and revealed (winners depend on the random deal)
- pass: Played cards leave hands and go to the public played_cards list
- pass: After 3 tricks the deal is settled: deal count and priority advance
- pass: Exact-bid scoring deal: tricks depend on chance, so only bids, declarer and deal count are asserted
- pass: Miss scoring deal: everyone bids 3 (at most one can hit); chance decides tricks, only bids and declarer asserted
- pass: Declarer bonus deal: declarer set by highest bid; chance decides tricks, only bids and declarer asserted
- pass: After settlement deal_number rises by 1 and priority wraps from seat 3 to seat 1
- pass: Game ends after 9 deals with 3 players; far-ahead seat 1 wins whatever the last deal brings
- pass: Game ends after 12 deals with 4 players; far-ahead seat 3 wins

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 5], results {'seat 2': 12, 'seat 1': 10, 'seat 3': 9, 'seat 4': 7, 'seat 5': 2}, 81-225 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 204.0 decisions, prompts of 161 characters on average (longest 163)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 2': 20, 'seat 1': 22, 'seat 3': 18}
- always `first@seat1`: won 30, lost 29, drew 1
- always `first@seat2`: won 26, lost 31, drew 3
- always `last@seat1`: won 0, lost 60, drew 0
- always `last@seat2`: won 0, lost 60, drew 0

## Triage (whose problem each failure was)

- round 1: fix_game: The game plays only one trick per round. After round 1 every hand still holds 2 cards and trick_number is 1, and after round 2 deal_number is still 1, so a 12-deal game cannot fit the 12 rounds the rules imply. The tests rightly treat one round as one complete deal (deal, bid, three tricks, score), and the platform's counted repetition can express all three tricks inside one round.
- round 1: revise_rules: The game is built correctly, but the design has two flaws. It needs 23 steps per round, over the limit of 20. And a thoughtless policy (always bid lowest and play the first legal card) wins well over half its games, while always bidding high loses badly.

## Choices the rules did not make

- 3 to 5 players, suggested 4: The designer suggests 4, so it is kept. 3 is the smallest table where the hook and declarer contests bite. Above 5, 3 tricks spread over too many players, so most bids are 0 and one choice matters little.
- 'Left' means the next higher seat number, wrapping from N to 1: The engine has no physical table, and seat order must be concrete.
- Cards are written as 'strength:card', for example '36:♦7': The engine has no lookup table, so putting the strength in the card text lets the trick winner be found by comparing numbers.
- No talk step: The rules forbid discussion; players communicate only through bids and cards.
- Bidding uses ask; card play uses poll: Bids are made in turn and each bidder hears earlier bids, while cards are chosen secretly and simultaneously.

## Simplifications

- A tie for the highest score is shown as a shared win among the tied players: The engine ranks by one expression and players level at the top share the win. This is equivalent to the source's draw.
- Scratch value d = |bid - tricks| is computed inside the settlement step rather than stored: The rules never refer to it outside settlement.

## Encoding attempts

- 1: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (played, played, played) in `your_hand`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 2: an option is offered and then refused (see the offer-only-what-is-allowed pattern): refused: seat 1 was offered '4:♣7' in `play_a_card`, picked it, and was asked again without it (round 1): the first offer held an option that was not allowed. Offer each seat only what it may do, from its own state, instead of refusing afterwards | refused: seat 2 was offered '11:♥9' in `play_a_card`, picked it, and was asked again without it (round 1): the first offer held an option that was not allowed. Offer each seat only what it may do, from its own state, instead of refusing afterwards
- 3: it plays, but part of it does nothing: game attribute `full_pack` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `bid_options` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 4: an option is offered and then refused (see the offer-only-what-is-allowed pattern): refused: seat 1 was offered '4:♣7' in `play_a_card`, picked it, and was asked again without it (round 1): the first offer held an option that was not allowed. Offer each seat only what it may do, from its own state, instead of refusing afterwards | refused: seat 2 was offered '11:♥9' in `play_a_card`, picked it, and was asked again without it (round 1): the first offer held an option that was not allowed. Offer each seat only what it may do, from its own state, instead of refusing afterwards
- 5: passed
