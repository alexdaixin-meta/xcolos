# modern_art: needs review

Built from the variation **Modern Art: Sealed Season** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Every auction uses one format. The auctioneer secretly picks a card and announces a public reserve price. Then all other players submit sealed bids at the same moment. The highest bid at or above the reserve buys the card and pays the auctioneer. If nobody meets the reserve, the auctioneer must buy the card at the reserve, paying the bank. (fixes: The open ascending auction is effectively real-time or an unbounded loop of turns, which the engine cannot run.): Sealed simultaneous bids are a single poll. The public reserve with forced purchase keeps the fixed-price risk and tension of the original, all inside one flat step list.
- Drop the per-card auction icons and the double auction. (fixes: Five auction types each need their own block of steps, chosen per card. The engine has a flat step list with no conditional subsequences.): This removes the branching blocks and long chains. The bluffing and valuation that made those formats interesting survive through the reserve and the sealed bids.
- Use a fixed-price idea only as the auctioneer's reserve. There is no first-to-accept sequence. (fixes: The double auction and first-to-accept fixed price add long sequential chains for little extra reasoning.): This keeps the auctioneer's pricing decision without a turn-by-turn accept loop.
- Use 4 artists (46 cards), 3 to 4 players and 3 seasons. A season ends at an artist's 4th card. The top two artists earn 30 and 20. Cards are dealt once, at the start. The game lasts at most 32 auctions. (fixes: Four seasons, five artists and up to 5 players make the game long and push past the attribute and step limits.): This keeps seasons, cumulative values and the uncertain season end, while staying inside the limits on rounds, attributes and draws.
- After each auction, all bids are revealed. Money and hands stay private. Each round also has a simultaneous one-message talk phase before bidding. (fixes: The rules leave money hidden but do not say what bid information becomes public. Inference needs a clear information rule.): Revealed bids give evidence about rivals' valuations and holdings. Talk allows bluffing about which artists will rise, and players disagree about which artists should win.

Objective: When the game ends, each player's money is revealed. The player with the most money wins. If two or more players tie for the most, the game is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. PAINTING VALUES. The artist that ends a season always has count 4, because the 4th card is counted and then discarded. Every other artist has at most 3. So the ending artist always ranks first and gets +30, and the second-ranked artist gets +20. A painting therefore pays 30, 20 or 0 in season 1. In 
- playable: pass. COMPLETENESS. The rules cover these edge cases. Reserve 0 with all bids 0: a bid of 0 meets the reserve, the tie-break picks the winner, and the price is 0. A forced buy happens only when the reserve exceeds 0 and no bid reaches it, and it is paid to the bank. Reserves and bids are capped at current
- reasoning_over_luck: pass. CHANCE. The only random element is the setup deal: 30 or 32 of 46 cards are dealt, and the rest are unused and unknown. This gives each player private knowledge of which artists they can push and which 4th cards they can play to end a season. The estimated chance share of the result is about 20 to 3

## Complexity

- steps_per_round: designed 14, built 14, limit 20
- choice_steps_per_round: designed 3, built 4, limit 4
- attributes: designed 18, built 56, limit 20 (built: 80)
- hidden_elements: designed 2, built 19, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 32, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Every player starts with 100 money
- FAIL: 3 players are dealt 10 cards each from the 46-card deck | rule R2 is broken: When there are 3 players, then each is dealt 10 cards; when there are 4 players, then each is dealt 8 cards, from a 46-card deck of 10 red, 11 blue, 12 green and 13 yellow.; seat 1 hand: expected 10 items, got 9; seat 2 hand: expected 10 items, got 9; seat 3 hand: expected 10 items, got 9; game deck: expected 16 items, got 19
- pass: 4 players are dealt 8 cards each from the 46-card deck
- FAIL: Auctioneer picks a card from own hand and a reserve up to own money | rule R3 is broken: When a round begins, then the auctioneer secretly picks one card from their hand and a reserve from 0 to their current money.; seat 1 was never offered 100, but should have been; Ada: the rule for 0 was never matched (the game never put that option to this seat)
- FAIL: Revealed card leaves the hand and raises its artist's count | rule R4 is broken: When the card is revealed, then it leaves the auctioneer's hand, its artist is announced, and that artist's season count rises by 1.; Ada: the rule for 0 was never matched (the game never put that option to this seat)
- FAIL: Fourth card of an artist is discarded unsold, no bidding, season is scored | rule R5 is broken: When the revealed card brings its artist's season count to 4, then the card is discarded unsold, the reserve is ignored, there is no talk or bidding, and season scoring happens.; Ada: the rule for 0 was never matched (the game never put that option to this seat)
- FAIL: Reserve is announced when the season does not end | rule R6 is broken: When the season does not end on the reveal, then the reserve is announced to everyone.; game reserve: expected 25, got 0; Ada: the rule for 25 was never matched (the game never put that option to this seat)
- FAIL: When the season continues, talk happens and the auction goes on to bidding | rule R7 is broken: When the season does not end on the reveal, then every player including the auctioneer submits one short message simultaneously, and all messages are shown to everyone.; game price: expected 10, got 0; seat 2 was never offered 10, but should have been; seat 3 was never offered 0, but should have been; Ada: the rule for 0 was never matched (the game never put that option to this seat); Blaise: the rule for 10 was never matched (the game never put that option to this seat)
- FAIL: Non-auctioneers bid from 0 to their own money | rule R8 is broken: When bidding happens, then every player except the auctioneer submits a sealed bid from 0 to their own current money, simultaneously.; seat 2 was never offered 40, but should have been; seat 3 was never offered 100, but should have been; Ada: the rule for 0 was never matched (the game never put that option to this seat)
- FAIL: Highest bid at or above reserve pays the auctioneer and takes the painting | rule R9 is broken: When at least one bid is >= the reserve, then the highest such bidder pays their bid to the auctioneer and appends the painting to their paintings.; seat 1 money: expected 130, got 100; seat 2 money: expected 70, got 100; game price: expected 30, got 0; Ada: the rule for 25 was never matched (the game never put that option to this seat); Blaise: the rule for 30 was never matched (the game never put that option to this seat); Cleo: the rule for 20 was never matched (the game never put that option to this seat)
- FAIL: Tied top bids go to the first seat after the auctioneer | rule R10 is broken: When the highest eligible bids tie, then the tied bidder first in seat order after the auctioneer wins.; seat 2 money: expected 120, got 100; seat 4 money: expected 80, got 100; seat 4 paintings: expected ['blue'], got []; game buyer: expected 4, got 3; game price: expected 20, got 0; Ada: the rule for 20 was never matched (the game never put that option to this seat); Blaise: the rule for 0 was never matched (the game never put that option to this seat); Cleo: the rule for 10 was never matched (the game never put that option to this seat); Dara: the rule for 20 was never matched (the game never put that option to this seat)
- FAIL: No bid reaches the reserve: auctioneer pays the reserve to the bank and keeps the painting | rule R11 is broken: When no bid reaches the reserve, then the auctioneer pays the reserve to the bank (money leaves the game) and takes the painting.; seat 1 money: expected 50, got 100; seat 1 paintings: expected ['blue'], got []; seat 2 paintings: expected [], got ['blue']; game buyer: expected 1, got 2; game price: expected 50, got 0; Ada: the rule for 50 was never matched (the game never put that option to this seat); Blaise: the rule for 10 was never matched (the game never put that option to this seat); Cleo: the rule for 0 was never matched (the game never put that option to this seat)
- FAIL: Buyer and price are made public after the auction | rule R12 is broken: When an auction resolves, then all bids, the buyer and the price are announced publicly.; seat 1 money: expected 115, got 100; seat 3 money: expected 85, got 100; game buyer: expected 3, got 2; game price: expected 15, got 0; Ada: the rule for 10 was never matched (the game never put that option to this seat); Blaise: the rule for 12 was never matched (the game never put that option to this seat); Cleo: the rule for 15 was never matched (the game never put that option to this seat)
- FAIL: Season ranking: first gains 30, count tie for second goes to the earlier artist | rule R13 is broken: When season scoring happens, then artists are ranked by season count with ties to the earlier of red, blue, green, yellow; the first gains 30 cumulative value and the second gains 20 unless its count is 0.; Ada: the rule for 0 was never matched (the game never put that option to this seat)
- FAIL: Second artist with count 0 gains nothing | rule R13 is broken: When season scoring happens, then artists are ranked by season count with ties to the earlier of red, blue, green, yellow; the first gains 30 cumulative value and the second gains 20 unless its count is 0.; Ada: the rule for 0 was never matched (the game never put that option to this seat)
- FAIL: Paintings of ranked artists pay their cumulative value, unranked pay 0 | rule R14 is broken: When season scoring happens, then each player gains, for each painting they own of a ranked artist, that artist's cumulative value after the increase; paintings of unranked artists pay 0.; Ada: the rule for 0 was never matched (the game never put that option to this seat)
- FAIL: After scoring, paintings are discarded, counts reset and the season advances | rule R15 is broken: When season scoring finishes, then all paintings are discarded, all season counts reset to 0, and the season number rises by 1.; Ada: the rule for 0 was never matched (the game never put that option to this seat)
- FAIL: When all hands are empty after an auction the season is scored and the game ends | rule R16 is broken: When every hand is empty after an auction, then the current season is scored and the game ends.; seat 1 standing: expected 105, got 100; seat 2 standing: expected 125, got 130; Ada: the rule for 0 was never matched (the game never put that option to this seat); Blaise: the rule for 5 was never matched (the game never put that option to this seat); Cleo: the rule for 0 was never matched (the game never put that option to this seat)
- FAIL: The third season scoring ends the game | rule R17 is broken: When the third season scoring is done, then the game ends.; Ada: the rule for 0 was never matched (the game never put that option to this seat)
- FAIL: The game ends after round 32 | rule R18 is broken: When the game would pass 32 rounds, then it ends.; winner: expected 'seat 1', got 'seats 1, 2 and 3'; seat 1 standing: expected 110, got 100; seat 2 standing: expected 90, got 100; Ada: the rule for 0 was never matched (the game never put that option to this seat); Blaise: the rule for 10 was never matched (the game never put that option to this seat); Cleo: the rule for 0 was never matched (the game never put that option to this seat)
- FAIL: Auctioneer passes over an empty-handed seat, which still bids | rule R19 is broken: When the auctioneer rotates, then it passes to the next seat in order holding at least one card; empty-handed players still bid.; game price: expected 10, got 0; seat 2 was never offered 10, but should have been; Ada: the rule for 0 was never matched (the game never put that option to this seat); Blaise: the rule for 10 was never matched (the game never put that option to this seat); Cleo: the rule for 0 was never matched (the game never put that option to this seat)
- FAIL: Players tied for most money share the win | rule R20 is broken: When the game ends, then the player with the most money wins, and players tied for most share the result.; Ada: the rule for 0 was never matched (the game never put that option to this seat); Blaise: the rule for 0 was never matched (the game never put that option to this seat); Cleo: the rule for 0 was never matched (the game never put that option to this seat)
- FAIL: Bids and reserves are capped at current money, so money never goes below 0 | rule R21 is broken: Money never goes below 0, because bids and reserves are capped at the player's current money.; seat 1 money: expected 35, got 20; seat 2 money: expected 0, got 15; game price: expected 15, got 0; Ada: the rule for 10 was never matched (the game never put that option to this seat); Blaise: the rule for 15 was never matched (the game never put that option to this seat); Cleo: the rule for 0 was never matched (the game never put that option to this seat)

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 4], results {'seat 3': 11, 'seat 1': 12, 'seat 2': 10, 'seat 4': 7}, 118-260 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 189.8 decisions, prompts of 176 characters on average (longest 230)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- always taking the first option as seat 1 wins 100% of decided matches against random seats
- always taking the first option as seat 2 wins 98% of decided matches against random seats
- random seats: {'seat 3': 27, 'seat 1': 14, 'seat 2': 18, 'seats 2 and 3': 1}
- always `first@seat1`: won 60, lost 0, drew 0
- always `first@seat2`: won 59, lost 1, drew 0
- always `last@seat1`: won 5, lost 55, drew 0
- always `last@seat2`: won 5, lost 55, drew 0

## Triage (whose problem each failure was)

- round 1: fix_game: The tests match the rules: the auctioneer must pick a reserve from 0 up to their current money. The game never put 0, 25 or 100 to seat 1 as a reserve option, so the reserve fell back to a default and the table `reserve` stayed 0 when it should have been 25. The reserve choice step is missing or wrongly built in the game file; the rules themselves are fine.
- round 1: fix_game: The reserve choice is not built correctly. Seat 1 was never offered a reserve of 0 or 100, and an auctioneer choosing 25 still left the table `reserve` at 0. The card choice worked, so the fault is in the reserve step, not in the rules or the tests.
- round 1: fix_game: The rules are clear and within the platform's capabilities, but the file deals 9 cards each instead of 10. Its trace shows some 'pick' draws (e.g. green) that never reach a hand, so the deal loop loses picks. The R3 to R5 scenarios also show the reserve choice is never put to the auctioneer as options from 0 to their current money.

## Choices the rules did not make

- 3 to 4 players, suggested 4: Kept from the designer. The minimum is 3 because a sealed auction needs at least two rival bidders against the auctioneer. The maximum is 4 because the 46-card deck and the 32-round limit are sized for it (4 x 8 = 32 cards).
- Talk kept as a simultaneous poll before the bids: The rules say messages are written at the same time. Players disagree about which artists should rise, since each holds different hands and paintings, so talk gives material for bluffing and persuasion.
- Artist ranking computed as count*4 + tiebreak (red 3, blue 2, green 1, yellow 0): Turns 'rank by count, ties by artist order' into arithmetic. Counts never exceed 4, so the tiebreak never outweighs a count difference.
- The auctioneer picks an artist name instead of a specific card: Cards of the same artist are identical, so naming the artist is equivalent.
- Cards the auctioneer chooses that end the season are revealed before the reserve is announced: Follows the step order: the reserve is chosen secretly, then announced only if the season did not end.

## Simplifications

- A tie for most money is a shared win rather than a declared draw: The engine ranks by one expression and players level at the top share the win; there is no separate draw outcome.
- The card choice and the reserve choice are two consecutive questions to the auctioneer: A question takes one answer; both stay secret until the reveal, so nothing changes.

## Encoding attempts

- 1: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (first_artist, second_artist) in `your_standing`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 2: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state a player is shown has empty fields (chosen_card, current_artist); hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 3: passed
