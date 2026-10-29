# medici: needs review

Built from the variation **Medici: Secret Patrons** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Each player is secretly dealt a different Patron commodity. Commodity-majority awards in your Patron commodity are paid to you twice. Patrons are revealed only at the end. (fixes: P1): This creates one strong hidden element. Bids now signal which commodity a rival is chasing, and players must infer the two unknown patrons from bidding behaviour, and can bluff by bidding on a commodity that is not theirs. Patrons are a permutation of three equal commodities, so no one is dealt a better type: the type changes what to buy, not who is ahead.
- Replace card-by-card drawing with an open Dock: the next 3 cards of the deck are always face up. The active player chooses to auction the first 1, 2 or 3 Dock cards as the lot. The Dock is then refilled from the deck. (fixes: P2): This keeps the drawer's key decision, sizing the lot to tempt or starve rivals, in a single choice with no loop. It also removes blind-flip luck, because everyone sees what is coming next.
- Fix the game at exactly 3 players. (fixes: P3): An auction then needs 2 rival bids plus the drawer's bid. With the lot-size choice that is 4 choice steps. Three players also fit the patron permutation exactly.
- Use 3 commodities (Spice, Silk, Grain), each with 10 cards valued 0,1,1,2,2,3,3,4,4,5, a 30-card deck reshuffled each day, and ship capacity 5. (fixes: P4): This keeps the attribute count low and the arithmetic easy while preserving the ship-value and track-majority trade-off.
- Each day is exactly 9 auction rounds: each player is active 3 times. A full ship simply cannot bid. The fill-free rule is dropped. (fixes: P5): This gives fixed length and a flat step list. With about 2 cards per lot against 15 total ship space, ships still fill and space stays scarce.
- The Dock shows the next 3 cards openly. (fixes: P6): Players plan around known upcoming lots, so outcomes depend on valuation rather than on flips.
- Rotate the first active player each day (day 1 player A, day 2 player B, day 3 player C). (fixes: P7): Every seat gets the same number of drawer turns and each seat leads one day.

Objective: After the end-of-day scoring of day 3, the player with the most florins wins. If two or more players tie for the most, the game is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. AWARD ECONOMY PER DAY: ship prizes 20+10 = 30; three commodity majorities at 10+5 = 45; Patron bonus up to 10 per player, so up to 30. That is 75 to 105 florins created per day, 225 to 315 over the game. At most 15 cards are loaded per day (3 ships of 5), 45 over the game. So a card is worth very ro
- playable: pass. COMPLETENESS: the deck (30 cards, defined values), the Dock (3 face-up, ordered), lot = first N Dock cards, bid order, legal bids (at least 1, above the high bid, at most florins, room on ship), loading and track +1 capped at 10, discard if all pass, refill, and all end-of-day tie rules are specifie
- reasoning_over_luck: pass. CHANCE SOURCES:
- The Patron deal is symmetric: everyone gets exactly one, from the same card distribution of 0,1,1,2,2,3,3,4,4,5 per commodity.
- The deck order decides which commodities and values appear in the Dock when you are active.
The Dock is public before every auction, so all players price

## Complexity

- steps_per_round: designed 14, built 16, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 15, built 46, limit 20 (built: 80)
- hidden_elements: designed 2, built 4, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 27, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Game start: 30 florins, all tracks at 0, empty ships
- pass: Day start resets the deck, empties ships, keeps tracks and deals a dock of 3 (all pass, lot of 1 discarded)
- pass: Day 2 round 1: seat 2 is active and chooses the lot, then bids last
- pass: Day 3 round 1: seat 3 is active and chooses the lot, then bids last
- pass: Lot size is capped by the dock length (2 cards) and takes the first dock cards
- pass: Lot of 1 is only the first dock card
- pass: Auction order with seat 1 active: seat 2, then seat 3, then seat 1
- pass: Auction order with seat 3 active: seat 1, then seat 2, then seat 3
- pass: Bids must exceed the high bid and not exceed own florins; a seat whose florins do not exceed the high bid may only pass
- pass: A seat whose ship lacks room for the lot may only pass
- pass: The winning bidder pays exactly the high bid and loads every lot card
- pass: Tracks rise by 1 per loaded card but are capped at 10
- pass: When everyone passes, the lot is discarded and nothing else changes
- pass: Resolved lot cards leave the dock, the rest keep their order, and an empty deck refills nothing
- pass: End of day ship scoring: highest ship value +20, second +10
- pass: Ship scoring tie for first: two tied first get 15 each, third gets 0
- pass: Ship scoring tie for second: two tied second get 5 each
- pass: Ship scoring three-way tie for first: 10 each
- pass: An empty ship earns no ship prize and takes no place; a ship worth 0 still places second
- pass: Majority scoring with ties and no patron bonus earned
- pass: Majority scoring: two tied second get 2 each, three tied first get 5 each (patron bonuses included)
- pass: A track at 0 earns no majority award and takes no place
- pass: Patron bonus doubles the majority award in the patron commodity (first and second place)
- pass: After the day 3 scoring the game ends with day 4; all level, all share the win
- pass: The most florins after the final scoring wins
- pass: Players tied for the most florins share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [3], results {'seats 1 and 3': 2, 'seat 2': 5, 'seat 1': 7, 'seat 3': 5, 'seats 1 and 2': 1}, 59-77 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 65.7 decisions, prompts of 261 characters on average (longest 276)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- always taking the first option as seat 2 wins 86% of decided matches against random seats
- random seats: {'seats 1 and 3': 3, 'seat 2': 23, 'seat 1': 16, 'seat 3': 15, 'seats 1 and 2': 1, 'seats 2 and 3': 2}
- always `first@seat1`: won 48, lost 12, drew 0
- always `first@seat2`: won 51, lost 8, drew 1
- always `last@seat1`: won 0, lost 60, drew 0
- always `last@seat2`: won 0, lost 60, drew 0

## Triage (whose problem each failure was)

- round 1: revise_rules: The game is built correctly, but a mindless policy (always the first option, which amounts to small lots and minimum bids) wins about 80-86% of decided games, and always taking the last option (bidding all your florins) always loses. Prizes are large and bids are cheap, so grabbing cards for 1 florin beats any thinking. Seat 2 also wins far more often than the other seats.

## Choices the rules did not make

- Exactly 3 players, suggested 3: The designer fixed 3 seats. The game needs exactly three different Patrons for the three commodities, so the count cannot change. The strategy lies in reading rivals' Patrons from their bidding and hiding your own while still building your Patron track.
- No free-text talk step: The source rules have no negotiation phase. Adding talk would be a new mechanic.
- A pass is answered as bid 0: This keeps the bid as one whole-number answer. 0 can never be a legal bid because the minimum is 1.
- Players with an empty ship, or a track at 0, are left out of the ranking and occupy no place: The source says they earn nothing but does not say whether they occupy a place. Leaving them out lets the other players take the prizes in order.
- Third place earns 0 in the tie-split arithmetic: Only first and second prizes exist, so a place beyond second contributes 0 to a tied group's sum.
- Cards are written as 'Commodity-value' text in lists: This lets one card carry both its commodity, for tracks, and its value, for ship_value.
- The card value list is given as separate copy-count parameters: Parameters must each be a single number. The values 0,1,1,2,2,3,3,4,4,5 are written as how many copies of each value every commodity has.

## Simplifications

- A tie for the most florins is a shared win at the top, not a separate draw: The engine has no draw outcome. Tied leaders sharing the win expresses the same result.
- Start-of-day and end-of-day work are single updates with a round_in_day condition: The engine runs one flat round list. Each conditional step is a single arithmetic update, not a separate block.

## Encoding attempts

- 1: it plays, but part of it does nothing: game attribute `full_deck` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 2: passed
