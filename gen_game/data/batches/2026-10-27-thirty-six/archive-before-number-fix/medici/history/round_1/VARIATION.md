# Variation: Medici: Sealed Ledgers

Players bid sealed florins for lots of commodity cards over 3 days. They fill 5-card ships for daily value bonuses, race for commodity majorities, and chase a secret favoured good that rivals try to read from their bids.

Players: 3 to 4, best with 4

## Review of the original

Medici is a 2-6 player auction game over 3 days. Each turn the active player turns up 1-3 commodity cards as a lot, which is then auctioned once around the table. Players load the lots onto ships of limited size and score florins for ship value rankings and commodity majorities; the most florins wins.

- **non_degenerate**: good. Always passing earns no ship or commodity income. Always bidding high bankrupts a player early. Lot size, overfill limits and turn order create real choices. The fixed once-around order does give the drawer a last-bid edge, but it rotates.
- **skill_sensitive**: good. Valuing a lot against ship space, money left and majority races is a skill. Experienced players beat novices fairly reliably, though the order of the deck adds noticeable swing.
- **headroom**: good. Pricing, timing lot sizes to starve rivals, and reading who can still bid give deep play. A weak player still picks up some cheap lots and scores.
- **reasoning_dependent**: weak. Cards are face-up and the state is almost fully public. The inference lies in reading opponents' valuations and budgets. No player holds a private goal, so there is little hidden information to infer.
- **verifiable**: good. All scoring is arithmetic on card values, counts and florins.
- **fits_platform**: weak. The commodity track is a small board. The draw-1-to-3 loop needs several random draws per turn. The day length depends on ships filling. The clockwise auction needs one choice step per player, which can exceed 4 choice steps. Ranking ships over 6 players needs costly arithmetic.

## Problems

- P1: Drawing cards one at a time with a stop decision needs up to 3 random draws and nested choices per turn, which exceeds the limit of 1 random draw per round.
- P2: The clockwise once-around auction needs one sequential choice step per player, which exceeds 4 choice steps with 5-6 players.
- P3: The day ends when ships fill, which is a variable, conditional length that is hard to build and to balance.
- P4: The game is nearly perfect-information, with no private goal, so there is little to infer beyond rivals' money.
- P5: The commodity track is a board, and full ship rankings over many players need expensive ranking arithmetic.
- P6: A wide player range (2-6) makes the deck size, the number of rounds and seat parity hard to keep fair.

## Changes

- Shuffle the deck once at the start of each day. Each round, reveal the top 3 cards, and the active player chooses to auction the first 1, 2 or all 3. (fixes: P1): This keeps the drawer's lot-size decision while using one shuffle per day and no random draw in other rounds.
- Replace the once-around auction with a single sealed simultaneous bid from every player. Ties go to the active player, then to the tied player next in seating order after the active player. (fixes: P2): This takes one choice step regardless of player count. Bluffing and valuation stay central, and the drawer keeps a tie edge in place of the last-bid edge.
- Each day has exactly 2 lots per player (8 rounds with 4 players). Ships hold 5 cards, and a player whose ship lacks room cannot win the lot. (fixes: P3): A fixed length gives each seat equal active turns and needs no variable day ending. Capacity still bites.
- Each player is secretly dealt a different favoured good, worth 3 extra florins per card of it collected over the game. (fixes: P4): This adds a hidden private goal. Bids leak information about it, so players must infer rivals' goals and can disguise their own by bidding on decoys. All goods have identical card distributions, so the deal is worth the same to everyone.
- Replace the commodity track with per-player running counts per good and an end-game majority bonus. Replace the full ship ranking with a top-two bonus each day. (fixes: P5): This keeps majority races and ship-value competition using simple counts and max calculations.
- Limit the game to 3-4 players, with a 48-card deck reshuffled each day. (fixes: P6): The deck always covers a day's reveals, and the round counts give every seat equal turns.

## Kept from the original

- Auctioning lots of commodity cards for florins
- The active player choosing how big a lot to offer
- Limited ship capacity, where a lot that would overfill your ship cannot be won
- Three days with a ship-value bonus each day and ships emptied between days
- Commodity majority racing across the whole game
- Most florins at the end wins

## The variation's rules

SETUP. Each player starts with 40 florins. Florin totals are private to each player, and the engine tracks them. The deck has 48 cards: 4 goods (Grain, Cloth, Spice, Dye) with 12 cards each. Each good has the card values 0,1,1,2,2,3,3,3,4,4,5,5. Each player is secretly dealt a different favoured good, chosen at random from the 4, and only that player knows it. Seats are numbered 1 to N. The active player in round r is seat ((r-1) mod N)+1.

DAYS AND ROUNDS. The game lasts 3 days. Each day has 2N rounds: 6 rounds with 3 players, 8 with 4. The game therefore has 6N rounds in total (18 or 24). At the start of each day, all 48 cards are shuffled into a fresh deck, and every ship is empty. A ship holds at most 5 cards.

EACH ROUND:
1. Reveal. The top 3 cards of the deck are revealed to everyone, in order, as cards A, B and C.
2. Lot size. The active player chooses 1, 2 or 3. The lot is card A, cards A and B, or cards A, B and C. Unchosen revealed cards are discarded. The lot is announced.
3. Sealed bids. All players, including the active player, at the same moment secretly bid a whole number of florins from 0 up to their own current florins. A bid of 0 is a pass.
4. Validity. A bid is treated as 0 if loading the lot would put that player's ship over 5 cards.
5. Winner. The highest valid bid above 0 wins. Ties go to the active player if tied. Otherwise they go to the tied player who comes first in seating order starting after the active player. If every bid is 0, the lot is discarded.
6. Payment and loading. The winner pays the bid to the bank and loads the lot onto their ship. The winner's ship value rises by the sum of the lot's card values. Their ship card count rises by the lot size. Their game-long count of each good rises by the number of cards of that good in the lot.
7. Announcement. The engine announces the winner, the price paid, and every player's ship card count. It does not announce florin totals.

END OF DAY (after the last round of each day):
- The highest ship value earns 15 florins. The second-highest earns 7. If several players tie for highest, they split 22 florins equally, rounded down, and no second place is paid. If several tie for second, they split 7 equally, rounded down. A ship value of 0 earns nothing.
- Then all ships are emptied: value 0, card count 0. The game-long good counts are kept.

END OF GAME (after day 3 scoring):
- Majorities. For each good, the player with the most cards of it over the whole game earns 10 florins. Ties split 10 equally, rounded down. If nobody has any cards of a good, nothing is paid for it.
- Favoured good. Each player earns 3 florins per card of their own favoured good collected over the game. Favoured goods are then revealed.

There is no talk phase.

Objective: After the end-of-game scoring, the player with the most florins wins. If several tie for most, the tied player with more total cards collected over the game wins. If still tied, the game is a draw.

Expected effect: Sealed bids force players to price each lot against ship space, remaining money, the daily top-two race and majority races. The active player sizes lots to bundle junk with prizes or to fill a rival's ship. Every bid leaks information about a player's secret favoured good, so strong players infer rivals' goals and avoid bidding wars over them. They can also bid on a decoy good to mislead, which carries real cost because majorities pay. Simple policies lose. Always passing ends at 40 florins while active buyers net far more, since about 66 florins of daily bonuses plus 40 of majorities plus favoured-good income enter play. Always bidding everything goes broke on the first lot and buys nothing afterwards. Always offering 3 cards hands rivals large, efficient lots. Talk is left out. Interests do conflict, but in a sealed-bid auction the main use of talk is proposing that everyone bid low, a cartel that strips out the pricing decision. Bluffing about favoured goods is already carried by the bids themselves, which are costly signals rather than cheap talk.

## Complexity (the designer's count, against the limits)

- steps_per_round: 16 (limit 20)
- choice_steps_per_round: 2 (limit 4)
- attributes: 14 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 24 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
