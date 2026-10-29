# masterpiece: ready for review

Built from the variation **Masterpiece: Secret Collectors** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- There are 4 public styles. Each player gets a secret collector theme, one distinct style per player. Every painting of your theme style is worth +400 extra to you at scoring. (fixes: P1, P4): A matching collector values a lot at v+400 while a non-matching seller values it at v. Mutually profitable trades now exist, and buyers who are not the matching collector still face a lemons market and should stay out. Inferring who collects what becomes the core skill.
- A seller who keeps the painting pays only a flat fee of 50 to the bank, and only if the highest bid was at least 50. (fixes: P2): The seller's honest reservation price becomes about v-50 instead of v/2. A matching buyer then has positive expected bids: against an unknown value, bidding 50 gives +87.5 in expectation and bidding 350 gives +100. Sellers in turn shade reserves upward to capture the collector's surplus. The small fee keeps stonewalling from being free.
- The reserve is never published. Only the bids, sold-or-kept, the money moved and cash totals are announced. (fixes: P3): Values stay private to past owners. A 'kept despite a high bid' outcome is only a hint, open to interpretation.
- Each player holds one painting of each style. Values are dealt by a Latin square: each player holds one each of 0, 300, 600 and 1200, and each style has exactly one painting of each value. (fixes: P6, P4): Every player starts at exactly 1500 + 2100 + 400 = 4000, with one theme painting each, so the deal is no lottery. Owning your own painting of a style tells you which values the other three paintings of that style have, which gives a deduction to plan with.
- The tie-break is most cash, then a draw. The game is fixed at 4 players. (fixes: P5, P1): This removes most draws. Four players also means a trade benefits both parties relative to the two bystanders, so trading beats passivity.
- Paintings are stored as hidden-hand items with three fields: style, value and owner. Seats 1 to 4 are defined at setup. (fixes: P7): This states exactly how the 16 paintings fit within the attribute limits.

Objective: The highest score wins. If several players tie for the highest score, the one among them with the most cash wins. If they are still tied, the game is a draw.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. STARTING POSITION. Every player holds one painting each worth 0, 300, 600 and 1200, which is 2100 in painting value. Every player holds one painting of each style, so exactly one painting matches their own theme and earns +400. Every player therefore starts at 1500 + 2100 + 400 = 4000. The deal shuf
- playable: pass. RULES COMPLETE. The rules specify all of the following:
- seller order;
- the lot chooser, who is always a non-seller;
- talk;
- the sealed bid range and the reserve range;
- the tie rule and resolution;
- the fee, including the case where the seller has less than 50 cash;
- the case where all bids 
- reasoning_over_luck: pass. CHANCE IS LOW. Starting scores are identical (4000). Randomness only sets which painting holds which value and which style is whose theme.

WHAT CAN BE INFERRED.
- Values follow a Latin-square structure: each style has exactly one painting of each value. Knowing your own four values rules out values

## Complexity

- steps_per_round: designed 13, built 12, limit 20
- choice_steps_per_round: designed 4, built 3, limit 4
- attributes: designed 14, built 50, limit 20 (built: 80)
- hidden_elements: designed 2, built 18, limit 3
- random_draws_per_round: designed 0, built -, limit 1
- rounds: designed 12, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Start: every seat has 1500 cash and its four paintings, one of each style
- pass: Dealt themes are real styles: with fixed values, each seat owning its own four paintings scores exactly one 400 bonus (themes random)
- pass: Values dealt: 16 painting values exist
- pass: Each seat starts knowing exactly its own 4 values
- pass: Round 1 seller is seat 1
- pass: Round 6 seller is seat 2
- pass: Seller with no paintings: no lot, no bids, nothing changes
- pass: Seat to the seller's left chooses the lot from the seller's paintings
- pass: A round with talk proceeds to the auction normally
- pass: Bids range to own cash, reserve to 2000, rounded down to 50
- pass: Tie between seats 4 and 1 with seat 2 selling: seat 4 is nearer clockwise and wins
- pass: Bid above reserve: buyer pays seller, gets the painting and learns its value
- pass: Bid equal to reserve: lot kept, seller pays 50 fee
- pass: Unsold with seller holding only 30: fee takes all 30
- pass: All bids 0: lot kept, no fee
- pass: Resolved auction publishes high bid, winner and new cash totals
- pass: A bought painting can be the lot when its new owner sells
- pass: Game ends after round 12; untraded seats all score 1500+2100+400 (values and themes random)
- pass: Scoring: cash + painting values + 400 per theme painting
- pass: Tied top score: more cash wins
- pass: Tied on score and cash: shared win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [4], results {'seat 4': 12, 'seat 2': 1, 'seat 3': 6, 'seats 3 and 4': 1}, 108-108 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 108.0 decisions, prompts of 222 characters on average (longest 289)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 4': 26, 'seat 2': 8, 'seat 3': 19, 'seats 3 and 4': 1, 'seat 1': 6}
- always `first@seat1`: won 43, lost 17, drew 0
- always `first@seat2`: won 42, lost 18, drew 0
- always `last@seat1`: won 1, lost 59, drew 0
- always `last@seat2`: won 0, lost 60, drew 0

## Triage (whose problem each failure was)

- round 1: fix_game: The scoring tests follow rule R17 exactly. Take seat 1: cash 1000, plus owned values 0+300+1200+300 = 1800, plus 3 Red theme paintings × 400 = 1200, gives 4000. The game instead produced 5500, and wrong scores for other seats too. Those scores do not match the values in the game's own table `painting_values`, so the end-of-game score computation is wrong.

## Choices the rules did not make

- Exactly 4 players (min 4, max 4, suggested 4): The designer chose 4. The structure needs it: 4 styles, 4 distinct themes, a 4x4 Latin square of values and 3 sales per seat over 12 rounds. Fewer seats break the value deal, and more have no theme or values to receive.
- Talk kept as a simultaneous poll broadcast to all: The source requires simultaneous unbinding talk. It earns its place because interests conflict: sellers want to talk up lots, and bidders want to bluff their themes and known values.
- Tie-break encoded as bid*10 + tie_priority: Bids are multiples of 50, so adding a priority from 0 to 3 never changes the order of different bids. It ranks the seller's left first, as the rules say.
- Ranking expression score*100000 + cash: Scores stay well under 100000, so cash only breaks ties in score. Players tied on both share the win, which stands for the source's draw.
- Strategy at the table: A thoughtful player infers others' themes from their bids and talk, uses known values to bid on undervalued lots, sets reserves to protect theme paintings, and bluffs in talk. A thoughtless one bids on face value.

## Simplifications

- Bids and reserves are entered as whole numbers and rounded down to a multiple of 50: The engine takes a whole number in a range; rounding enforces the multiple-of-50 rule.
- The skip when the seller has no paintings is done with a 'when' condition on each step: The step list is flat; per-step conditions give the same effect without choosing a block of steps.
- Painting values are stored as 'name=value' text entries in lists: The engine has lists, not maps; each player's known_values plays the role of 'values known to past owners'.
- Bids and the reserve are gathered in one simultaneous poll with different ranges per seat: The source makes them simultaneous; one poll keeps every answer hidden until all are in.

## Encoding attempts

- 1: playing it with random seats failed: seed 1, 4 players: the match crashed: FlowError: 'sold and lot_entry not in you.known_values' reads `you` where there is no player
- 2: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (lot, lot_style) in `your_collection`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 3: it plays, but part of it does nothing: game attribute `styles` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `seat_tags` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `value_labels` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 4: passed
