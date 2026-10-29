# medici: needs review

Built from the variation **Medici: Sealed Ledgers** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Shuffle the deck once at the start of each day. Each round, reveal the top 3 cards, and the active player chooses to auction the first 1, 2 or all 3. (fixes: P1): This keeps the drawer's lot-size decision while using one shuffle per day and no random draw in other rounds.
- Replace the once-around auction with a single sealed simultaneous bid from every player. Ties go to the active player, then to the tied player next in seating order after the active player. (fixes: P2): This takes one choice step regardless of player count. Bluffing and valuation stay central, and the drawer keeps a tie edge in place of the last-bid edge.
- Each day has exactly 2 lots per player (8 rounds with 4 players). Ships hold 5 cards, and a player whose ship lacks room cannot win the lot. (fixes: P3): A fixed length gives each seat equal active turns and needs no variable day ending. Capacity still bites.
- Each player is secretly dealt a different favoured good, worth 3 extra florins per card of it collected over the game. (fixes: P4): This adds a hidden private goal. Bids leak information about it, so players must infer rivals' goals and can disguise their own by bidding on decoys. All goods have identical card distributions, so the deal is worth the same to everyone.
- Replace the commodity track with per-player running counts per good and an end-game majority bonus. Replace the full ship ranking with a top-two bonus each day. (fixes: P5): This keeps majority races and ship-value competition using simple counts and max calculations.
- Limit the game to 3-4 players, with a 48-card deck reshuffled each day. (fixes: P6): The deck always covers a day's reveals, and the round counts give every seat equal turns.

Objective: After the end-of-game scoring, the player with the most florins wins. If several tie for most, the tied player with more total cards collected over the game wins. If still tied, the game is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. CARD VALUES: each good runs 0,1,1,2,2,3,3,3,4,4,5,5, so the sum is 33 and the mean is 2.75. A full 5-card ship averages about 13.75. A 3-card lot ranges from 0 to 15.

REWARD POOL: The day prizes are 15 + 7 = 22 per day, so 66 over the game. Majorities pay 4 x 10 = 40. The favoured good pays 3 per c
- playable: pass. COMPLETENESS:
- Deck: fully specified at 48 cards. Each day uses at most 3 x 8 = 24 cards, so the deck never runs out.
- Active seat: given by formula.
- Lot: fixed as a prefix of A,B,C.
- Bids: simultaneous, from 0 to current florins.
- Overfill rule: invalidates the bid.
- Ties: the active player 
- reasoning_over_luck: pass. CHANCE ELEMENTS: the daily shuffle, which all players see equally, and the favoured-good deal, which is symmetric (each good equally likely, 12 cards each).

WHAT DECIDES THE WINNER:
- Bid shading in a first-price sealed auction.
- Valuing a lot against your remaining capacity, the day race for 15/7

## Complexity

- steps_per_round: designed 16, built 16, limit 20
- choice_steps_per_round: designed 2, built 2, limit 4
- attributes: designed 14, built 50, limit 20 (built: 80)
- hidden_elements: designed 2, built 8, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 24, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Every seat starts with 40 florins and no cards
- FAIL: Favoured goods (random) pay 3 per card whichever good is dealt: equal holdings give equal end scores | rule R2 is broken: When the game starts, then each player holds a different favoured good drawn at random from Grain, Cloth, Spice and Dye, known only to that player.; Cleo: the rule for 1 was never matched (the game never put that option to this seat)
- FAIL: A new day rebuilds the 48-card deck and empties ships | rule R3 is broken: When a day starts (round mod 2N == 1), then the deck is rebuilt as 48 cards: 12 per good, with values 0,1,1,2,2,3,3,3,4,4,5,5.; Ada: the rule for 1 was never matched (the game never put that option to this seat)
- FAIL: In round 5 of a 3-player game only seat 2 chooses the lot size | rule R4 is broken: When it is round r, then the active seat is ((r-1) mod N)+1.; seat 2 was never offered 3, but should have been; Blaise: the rule for 3 was never matched (the game never put that option to this seat)
- FAIL: With 4 players a day lasts 8 rounds: round 16 ends day 2 | rule R5 is broken: When the game has N players, then each day has 2N rounds and the game has 6N rounds: 18 with 3 players, 24 with 4.; Dara: the rule for 1 was never matched (the game never put that option to this seat)
- FAIL: With 4 players the game ends after round 24 | rule R5 is broken: When the game has N players, then each day has 2N rounds and the game has 6N rounds: 18 with 3 players, 24 with 4.; Dara: the rule for 1 was never matched (the game never put that option to this seat)
- FAIL: Each round draws 3 cards from the deck | rule R6 is broken: When a round starts, then 3 cards are drawn from the deck and revealed in order as A, B and C.; Blaise: the rule for 1 was never matched (the game never put that option to this seat)
- FAIL: Lot size 2 offers A+B and discards C | rule R7 is broken: When the active player chooses lot size 1, 2 or 3, then the lot is A, A+B or A+B+C, and the unchosen revealed cards are discarded.; seat 1 florins: expected 35, got 40; seat 1 ship_count: expected 2, got 0; seat 1 total_cards: expected 2, got 0; game discard: expected 1 items, got 3; Ada: the rule for 0 was never matched (the game never put that option to this seat); Blaise: the rule for 2 was never matched (the game never put that option to this seat)
- FAIL: Bids range from 0 to own florins and the active seat bids too | rule R8 is broken: When bidding happens, then all players, including the active player, bid at the same time a whole number from 0 to their own current florins, and 0 is a pass.; seat 2 florins: expected 33, got 40; seat 2 ship_count: expected 1, got 0; seat 2 total_cards: expected 1, got 0; seat 1 was never offered 12, but should have been; seat 1 was never offered 0, but should have been; seat 2 was never offered 0, but should have been; Blaise: the rule for 0 was never matched (the game never put that option to this seat); Blaise: the rule for 1 was never matched (the game never put that option to this seat)
- FAIL: A bid from a seat whose ship cannot hold the lot counts as 0 | rule R9 is broken: When a player's ship_count + lot_size > 5, then that player's bid is treated as 0.; seat 3 florins: expected 35, got 40; seat 3 ship_count: expected 2, got 0; seat 3 total_cards: expected 2, got 0; Ada: the rule for 0 was never matched (the game never put that option to this seat); Blaise: the rule for 2 was never matched (the game never put that option to this seat); Cleo: the rule for 0 was never matched (the game never put that option to this seat)
- FAIL: The strictly highest bid wins the lot | rule R10 is broken: When one valid bid above 0 is strictly highest, then that bidder wins the lot.; seat 3 florins: expected 31, got 40; seat 3 ship_count: expected 1, got 0; seat 3 total_cards: expected 1, got 0; Ada: the rule for 0 was never matched (the game never put that option to this seat); Blaise: the rule for 1 was never matched (the game never put that option to this seat); Cleo: the rule for 0 was never matched (the game never put that option to this seat)
- FAIL: A tie including the active seat goes to the active seat | rule R11 is broken: When the highest valid bids tie and the active player is among them, then the active player wins.; seat 2 florins: expected 34, got 40; seat 2 ship_count: expected 1, got 0; Ada: the rule for 0 was never matched (the game never put that option to this seat); Blaise: the rule for 0 was never matched (the game never put that option to this seat); Blaise: the rule for 1 was never matched (the game never put that option to this seat); Cleo: the rule for 0 was never matched (the game never put that option to this seat)
- FAIL: A tie without the active seat goes to the first seat after it (seat 3 before seat 1 when seat 2 is active) | rule R12 is broken: When the highest valid bids tie without the active player, then the tied player who comes first in seat order after the active seat wins.; seat 3 florins: expected 34, got 40; seat 3 ship_count: expected 1, got 0; seat 3 total_cards: expected 1, got 0; Ada: the rule for 0 was never matched (the game never put that option to this seat); Blaise: the rule for 1 was never matched (the game never put that option to this seat); Cleo: the rule for 0 was never matched (the game never put that option to this seat)
- FAIL: When every bid is 0 the lot is discarded and nobody pays | rule R13 is broken: When every bid is 0, then the lot is discarded and nobody pays.; Blaise: the rule for 3 was never matched (the game never put that option to this seat)
- FAIL: Winning a 3-card lot with bid 11 costs 11 and adds 3 cards | rule R14 is broken: When a player wins a lot with bid b, then their florins fall by b, ship_value rises by the sum of the lot's card values, ship_count and total_cards rise by the lot size, and each good count rises by that good's cards in the lot.; seat 1 florins: expected 19, got 30; seat 1 ship_count: expected 4, got 1; seat 1 total_cards: expected 7, got 4; Ada: the rule for 0 was never matched (the game never put that option to this seat); Blaise: the rule for 3 was never matched (the game never put that option to this seat)
- FAIL: After a round every seat's ship count reflects the sale | rule R15 is broken: When a round ends, then the winner, the price paid and every player's ship_count are announced, and florins are not announced.; seat 3 ship_count: expected 2, got 0; seat 3 florins: expected 32, got 40; Blaise: the rule for 2 was never matched (the game never put that option to this seat); Cleo: the rule for 0 was never matched (the game never put that option to this seat)
- FAIL: A lone top ship at day end gains 15 | rule R16 is broken: When a day ends and one player alone has the highest ship value (above 0), then that player gains 15 florins.; Cleo: the rule for 1 was never matched (the game never put that option to this seat)
- FAIL: Two ships tied for top each gain 11 and no second place is paid | rule R17 is broken: When a day ends and k>1 players tie for the highest ship value (above 0), then each gains floor(22/k) florins and no second place is paid.; Cleo: the rule for 1 was never matched (the game never put that option to this seat)
- FAIL: Two ships tied for second each gain 3 | rule R18 is broken: When a day ends with a single leader, then the m players with the second-highest ship value (above 0) each gain floor(7/m) florins.; Cleo: the rule for 1 was never matched (the game never put that option to this seat)
- FAIL: A ship of value 0 earns nothing at day end | rule R19 is broken: When a player's ship value is 0 at day end, then that player earns nothing from day scoring.; Cleo: the rule for 1 was never matched (the game never put that option to this seat)
- FAIL: Day scoring empties ships but keeps total cards | rule R20 is broken: When day scoring is done, then all ships are emptied (value 0, count 0), and the game-long good counts are kept.; Cleo: the rule for 1 was never matched (the game never put that option to this seat)
- FAIL: End majorities: sole grain leader gains 10, cloth tie gains 5 each, uncollected goods pay nothing | rule R21 is broken: When the game ends, then for each good the j players with the most cards of it (more than 0) each gain floor(10/j) florins, and a good nobody collected pays nothing.; Cleo: the rule for 1 was never matched (the game never put that option to this seat)
- FAIL: Favoured goods pay 3 per card at game end | rule R22 is broken: When the game ends, then each player gains 3 florins per card of their favoured good collected, and favoured goods are revealed.; Cleo: the rule for 1 was never matched (the game never put that option to this seat)
- FAIL: A 3-player game ends after round 18 | rule R23 is broken: When round 6N has been completed, then the game ends.; Cleo: the rule for 1 was never matched (the game never put that option to this seat)
- FAIL: Florins tie broken by total cards, remaining tie shares the win | rule R24 is broken: When the game ends, then the player with the most florins wins, a tie goes to more total_cards, and players still tied share the win.; Cleo: the rule for 1 was never matched (the game never put that option to this seat)

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 4], results {'seat 3': 11, 'seat 2': 14, 'seat 1': 12, 'seat 4': 3}, 72-120 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 96.0 decisions, prompts of 270 characters on average (longest 295)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 3': 22, 'seat 2': 21, 'seat 1': 17}
- always `first@seat1`: won 10, lost 50, drew 0
- always `first@seat2`: won 3, lost 57, drew 0
- always `last@seat1`: won 1, lost 59, drew 0
- always `last@seat2`: won 0, lost 60, drew 0

## Triage (whose problem each failure was)

- round 1: fix_game: The tests follow the rules. In all four failing scenarios the active seat was never offered the lot-size choice that rule R4 gives it, or was offered only part of it. The trace also shows other defects in the file: only seat 2 was polled for a bid, the deck held repeated 'Grain-2' cards, and the game stopped at round 6 instead of running 6N rounds.
- round 1: fix_game: The trace shows the game moves `round` from 1 to 2 and `active_seat` from 1 to 2 before round 1 is played, so seat 2 chooses the lot size in round 1. The rules make seat ((r-1) mod N)+1 active, which is seat 1 in round 1. Because of this off-by-one, the scripted lot sizes and bids never reach the right seats, every bid comes out 0, nobody wins, and all three revealed cards are discarded instead of only the unchosen one.
- round 1: fix_game: The tests follow the rules. In R2 the 58-florin result checks out: 40, plus 3 from each of the 4 split majorities, plus 6 for favoured cards, gives 58008. The traces show the game file does not give the active seat a correct lot-size choice: in round 5 seat 2 was never offered 3, and in rounds 18 (N=3), 7 (N=3) and 16 (N=4) the active seat was never asked for a lot size at all.

## Choices the rules did not make

- 3 to 4 players, suggested 4: The designer chose 4. 3 is the least where a sealed auction has real rivals and both day prizes are contested. More than 4 is impossible because only 4 favoured goods can be dealt, and majorities would get too thin.
- No talk phase: The source says there is no talk. Bidding is sealed and simultaneous, so it is a poll.
- Tie-break order computed as priority = N - ((seat - active_seat + N) mod N): This turns 'active player first, then seats after the active player' into arithmetic.
- Cards encoded as text like 'Spice-3': The good and the value are both needed for the counts and the ship value.
- Card values given as the number of copies of each value per good, and round counts given per player (2 per day, 6 per game): Parameters must be plain numbers. 1,2,2,3,2,2 copies of values 0 to 5 give the 12-card distribution, and rounds = 2N per day and 6N in total.
- ship_value is public: Lots and winners are announced, so ship contents are public knowledge. Only florins, bids and favoured goods are secret.
- Second place is computed only among ship values above 0 and strictly below the top: The source says a value of 0 earns nothing and a tied first place cancels second place.
- Rank expression florins*1000 + total_cards: total_cards cannot reach 1000, so florins decide first and cards break ties. Any remaining tie shares the win, which is the draw.

## Simplifications

- The deck rebuild and ship emptying at a day boundary are done by conditional updates on round, at the start of a day and at its end: The step list is flat, so day transitions use if-conditions on round.
- Favoured goods are revealed by a public tell at the end of the game: The attribute stays private to its owner, so the reveal is an announcement.

## Encoding attempts

- 1: players are sent text with a `{name}` that was never filled in: placeholder: players are shown the literal {florins} (in `prompt`: "Sealed bid for the lot ['Spice-4', 'Dye-2', 'Dye-4'] (3 cards, total value 10). Bid a whol"); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {florins} (in `prompt`: "Sealed bid for the lot ['Spice-4', 'Dye-2', 'Dye-4'] (3 cards, total value 10). Bid a whol"); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {florins} (in `prompt`: "Sealed bid for the lot ['Spice-4', 'Dye-2', 'Dye-4'] (3 cards, total value 10). Bid a whol"); use only names the step can fill in (see the broadcast rule: {value} and {seat})
- 2: it plays, but part of it does nothing: game attribute `full_deck` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 3: passed
