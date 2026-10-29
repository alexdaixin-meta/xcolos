# biblios: needs review

Built from the variation **Biblios: Scriptorium** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Merge draft and auction into every round. The active player privately sees 2 cards, secretly keeps one and auctions the other. (fixes: P1): This keeps the defining 'secret card for me, other card to market' decision inside a flat step list.
- The gift turn becomes a single choice: which of the 2 cards to keep. (fixes: P2): One choice step instead of many placements.
- The auction becomes one simultaneous sealed bid by the non-active players. The highest unique bid wins. A tie or all zeros discards the card. (fixes: P3, P5): This is one poll with no re-auction loops, and bids can never exceed what a player owns.
- The winning bid is paid to the active player, the seller. (fixes: P6): Gold circulates, so being the seller is a real income source. It also creates a sell-high-versus-keep-the-good-card tension.
- Use 3 colours, a 24-card known deck that is exactly used up, VP shares split on ties, and no letters. (fixes: P4): This fits the attribute and length limits. A fully known deck makes card counting and inference about hidden kept cards possible.
- Church cards stay. Whoever gains one picks one colour to raise or lower by 1, with values limited to 1-5. This is done in a single end-of-round poll. (fixes: P2): This keeps the dice manipulation within the choice-step budget.
- Every player starts with 4 Gold, so no one is locked out. (fixes: P6): Everyone can bid from round 1.

Objective: The player with the most VP wins. If VP totals tie for first, the tied player with the most leftover Gold wins. If that also ties, the game is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. Deck accounting: 18 colour cards (each colour 1+1+2+2+3+4 = 14), 4 Gold (total 10) and 2 Church make 24 cards. 12 rounds x 2 cards = 24, so the deck is used exactly. Active turns: with 3 players each seat is active 4 times; with 4 players each seat is active 3 times. Turn counts are therefore symmet
- playable: pass. Every situation is covered. Draw 2; keep 1 secretly; the other becomes the lot. If both cards are Church or both Gold, one is kept and the other offered under the same rules. The rules handle bids from 0 to current Gold, a single highest bid of at least 1 wins, and ties or all-zero bids discard the 
- reasoning_over_luck: pass. There is real inference. The deck is public, every lot is revealed, and the kept set equals the deck minus the lots. Each player can narrow down opponents' hidden colours from which card they offered as the lot (they kept the other) and from how hard they bid. Gold is private but partly trackable fr

## Complexity

- steps_per_round: designed 13, built 15, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 16, built 50, limit 20 (built: 80)
- hidden_elements: designed 3, built 14, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 12, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: 24-card deck, empty bought lists, VP values all 3
- pass: Round 5 with 3 players makes seat 2 active
- FAIL: Round start removes 2 cards from the deck, only the active seat is offered them | rule R3 is broken: When a round begins, 2 cards are removed from the deck, and only the active player sees them.; Ada: the rule for 'red-2' was never matched (the game never put that option to this seat)
- pass: A kept red-3 goes to the hand and scores Red at the end
- pass: A kept gold-3 adds 3 gold at once
- pass: A kept Church is played the same round
- pass: The card not kept becomes the lot
- pass: The talk step runs and the round continues normally
- FAIL: Only non-active seats bid, from 0 up to their gold | rule R9 is broken: When bidding, every non-active player at once bids a whole number from 0 to their current gold, and the active player does not bid.; seat 2 was never offered 4, but should have been; seat 2 was never offered 0, but should have been; seat 3 was never offered 2, but should have been
- FAIL: The sole highest bidder pays and takes the lot | rule R10 is broken: When exactly one player has the highest bid and it is at least 1, that player pays the bid from their gold to the active player's gold and takes the lot.; seat 2 bought: expected ['blue-2'], got []; seat 2 bought_blue: expected 2, got 0; game sale_price: expected 3, got 0; Blaise: the rule for 3 was never matched (the game never put that option to this seat); Cleo: the rule for 1 was never matched (the game never put that option to this seat)
- FAIL: Tied top bids: lot discarded, nobody pays | rule R11 is broken: When the highest bid is tied or all bids are 0, nobody pays and the lot is discarded.; Blaise: the rule for 2 was never matched (the game never put that option to this seat); Cleo: the rule for 2 was never matched (the game never put that option to this seat)
- FAIL: All bids 0: lot discarded | rule R11 is broken: When the highest bid is tied or all bids are 0, nobody pays and the lot is discarded.; Blaise: the rule for 0 was never matched (the game never put that option to this seat); Cleo: the rule for 0 was never matched (the game never put that option to this seat)
- FAIL: A won green-3 is public and adds 3 to bought_green | rule R12 is broken: When a colour lot of value v is won, it is public in the winner's bought cards and adds v to their bought sum for that colour.; seat 3 bought: expected ['green-3'], got []; seat 3 bought_green: expected 3, got 0; game sale_price: expected 1, got 0; Blaise: the rule for 0 was never matched (the game never put that option to this seat); Cleo: the rule for 1 was never matched (the game never put that option to this seat)
- FAIL: A won gold-2 adds 2 gold to the winner (seen in the final standings) | rule R13 is broken: When a Gold lot of value v is won, the winner's gold increases by v.; seat 1 standing: expected 5, got 4; seat 3 standing: expected 3005, got 3004.0; seat 1 bought: expected ['gold-2'], got []; Ada: the rule for 1 was never matched (the game never put that option to this seat); Blaise: the rule for 0 was never matched (the game never put that option to this seat)
- FAIL: A won Church is played by the buyer that round | rule R14 is broken: When a Church lot is won, the winner plays it at step 9 that round.; seat 2 bought: expected ['church'], got []; seat 2 church_choice: expected 'green-1', got 'none'; game vp_green: expected 2, got 3; game sale_price: expected 1, got 0; seat 2 was never offered 'green-1', but should have been; Blaise: the rule for 1 was never matched (the game never put that option to this seat); Blaise: the rule for 'green-1' was never matched (the game never put that option to this seat); Cleo: the rule for 0 was never matched (the game never put that option to this seat)
- FAIL: The sale price is made public | rule R15 is broken: When the auction resolves, the sale price, or that the lot was discarded, is announced.; seat 2 bought: expected ['blue-4'], got []; game sale_price: expected 2, got 0; Blaise: the rule for 2 was never matched (the game never put that option to this seat); Cleo: the rule for 0 was never matched (the game never put that option to this seat)
- FAIL: Two Church plays on the same colour both apply, capped at 5 | rule R16 is broken: When players gained a Church card this round, each chooses at once one colour and +1 or -1. All changes apply, each VP value is limited to 1-5, and a colour may receive two changes.; seat 2 church_choice: expected 'red+1', got 'none'; Blaise: the rule for 1 was never matched (the game never put that option to this seat); Blaise: the rule for 'red+1' was never matched (the game never put that option to this seat); Cleo: the rule for 0 was never matched (the game never put that option to this seat)
- FAIL: Two Church plays lower a colour by 2 | rule R16 is broken: When players gained a Church card this round, each chooses at once one colour and +1 or -1. All changes apply, each VP value is limited to 1-5, and a colour may receive two changes.; game vp_red: expected 1, got 2; Blaise: the rule for 1 was never matched (the game never put that option to this seat); Blaise: the rule for 'red-1' was never matched (the game never put that option to this seat); Cleo: the rule for 0 was never matched (the game never put that option to this seat)
- FAIL: A played Church choice is revealed publicly with the new value | rule R17 is broken: When a Church card is played, it and the chosen change are revealed, and the new VP values are announced.; seat 2 church_choice: expected '', got 'none'
- pass: The game ends after round 12 with the deck empty
- pass: Kept plus bought: total 5 beats total 4 and takes Red
- pass: A tie for most Blue splits its 3 VP as 1.5 each
- pass: Colours nobody holds score for no one
- pass: Gold scores no VP
- pass: A VP tie is won by the seat with more leftover gold
- pass: A tie on both VP and gold shares the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 4], results {'seats 1 and 2': 1, 'seat 2': 19, 'seat 3': 11, 'seat 1': 7, 'seat 4': 2}, 70-98 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 84.3 decisions, prompts of 178 characters on average (longest 285)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seats 1 and 2': 1, 'seat 2': 27, 'seat 3': 19, 'seat 1': 12, 'seats 1 and 3': 1}
- always `first@seat1`: won 4, lost 56, drew 0
- always `first@seat2`: won 9, lost 51, drew 0
- always `last@seat1`: won 14, lost 46, drew 0
- always `last@seat2`: won 17, lost 43, drew 0

## Triage (whose problem each failure was)

- round 1: fix_game: The rules are clear and within the platform's abilities, but the game file draws from the wrong end of the deck and does not put the right bid amounts to the bidders. In the trace, given deck ['green-2','blue-1'], the game picked 'blue-1' (the last card) first. The bid tests also report that seat 2 (4 Gold) was never offered 4 or 0 and seat 3 (2 Gold) was never offered 2. Because those bids never happen, the sole-winner and tie scenarios fail as a knock-on effect.
- round 1: fix_game: The tests follow the rules, but the game does not offer the moves the rules require. Bidding seats were never given the options 0 to their gold, so every bid fell to 0 and no lot was ever sold. The draw also did not offer the active seat the top 2 cards of the given deck.
- round 1: fix_game: In three bidding scenarios the scripted bids never reached the game. Seat 2 was never offered 4 or 0, seat 3 was never offered 2, and Blaise and Cleo were never offered 2. As a result no sale ever happened (bought [] and sale_price 0 where the rules require blue-2 and a price of 3). The bid step is not presenting the whole-number range 0..current gold to each non-active seat, which is a game-file error and not a rules or platform problem.

## Choices the rules did not make

- 3 to 4 players, suggested 3: The designer suggests 3, so it is kept. The minimum is 3 because with 2 players the auction has a single bidder and no rivalry. The maximum is 4 because that is the source's limit; the 24-card deck and 12 rounds are fixed, so more seats would leave each player too few turns as the active seller.
- Keep the simultaneous talk step as a poll broadcast to all: The source requires it, and it earns its place: players disagree about who should take each colour, and the seller can bluff about the hidden kept card to raise the price.
- Strategy at the table: A thoughtful player reads the others' bought cards and their bluffs to infer majorities. They price a lot by the gold it hands the seller, and use Church cards to raise colours they lead and lower colours they trail.
- Card encoding as text 'colour-value', 'gold-value', 'church': It gives the keep options and lots a readable, parseable form.
- Card distribution expressed as numeric counts per value in parameters: Parameters must be numbers, so the value lists are given as how many cards of each value exist.
- rank_by = vp*1000 + gold: It folds the Gold tie-break into one expression. Fractional VP differences are at least 1/12, and 1000/12 is about 83, which exceeds the maximum possible gold (26 with 4 players).
- Church changes applied one after another, with clamping at each step: The source says to apply all changes, limited to 1-5, but does not say whether clamping happens per change or at the end. Applying them in sequence is the natural reading.
- Separate kept (private) and bought (public) sums per colour: Kept cards are hidden and bought cards are face-up, so their visibility differs. Scoring adds the two.
- End scoring runs as an update conditioned on round == 12, placed before the end check: The check ends the game, so scoring must happen before it.

## Simplifications

- Shuffling is replaced by drawing random cards from the deck list: This is equivalent to a shuffled deck in the engine's draw model.
- The drawn cards are shown only to the active player as the options of the keep question, not through an 'active player only' visibility: The engine has no per-round visibility for the active player; private question options give the same effect.
- The Gold tie-break and the draw are folded into a single ranking where tied players share the win: The engine ranks by one arithmetic expression and has no separate draw.

## Encoding attempts

- 1: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state a player is shown has empty fields (church_choice, church_choice, church_choice, lot); hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 2: passed
