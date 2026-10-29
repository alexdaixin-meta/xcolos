# Variation: Cat in the Sack: Paid Entry

Players secretly feed cards into a shuffled sack, see part of it, talk, then decide whether to pay a mouse to enter a sealed-bid auction for it or take a safe 2 mice. They must infer the hidden cards and their rivals' intentions.

Players: 3 to 5, best with 4

## Review of the original

Felicity the Cat in the Sack is a 3-5 player bluffing auction. Each round every player secretly adds a card (cats of positive or negative value, a rabbit, dogs) to a 'sack', and players bid mice in a rising auction while the sack is revealed bit by bit. Players who pass take a mouse card as consolation, and final score is cat points plus leftover mice.

- **non_degenerate**: weak. The original has no dominant policy, but its rising auction with escalating mouse-card consolations (2,3,4,6) is complex. The previous sealed-bid variation failed because STAY weakly dominated DROP. A losing stayer got 3 mice and a dropper got 2. Winning at price 1 beats DROP whenever the sack is worth 3 or more, and the average sack is worth about 12.9. So the stay/drop poll and the first reveal decided nothing.
- **skill_sensitive**: good. Every hand holds the same cards, so the deal matters little. What decides the game is reading which cards rivals dumped, valuing a partly revealed sack, and pacing mice over the rounds. Shuffling the sack adds noise, but it falls on everyone.
- **headroom**: good. A weak player can still score by dropping or buying cheap sacks. A strong player can keep improving by counting used cards from the face-up discards, timing the Dog, choosing when to dump the -8 and -5, and bidding with rivals' mice in mind.
- **reasoning_dependent**: good. Sack contents are partly hidden, and each player knows only their own contribution. Rivals' contributions must be inferred from what has been revealed, from cards already used, and from table talk. The value of a lone Dog depends on the hidden cats.
- **verifiable**: good. Sack value, the Dog removal, bids, payments and totals are all arithmetic.
- **fits_platform**: weak. The original's clockwise rising auction, with refunds, ordered consolation cards and a reveal on every pass, is a long chain of conditional steps. The previous sealed-bid variation fits the platform but left the 4-player reveal count ambiguous.

## Problems

- P1: STAY weakly dominates DROP. A losing stayer earns 3 mice and a dropper earns 2, so staying never costs anything and the stay/drop poll is an empty step.
- P2: Because everyone always stays, the first reveal and the talk before the stay/drop choice inform nothing.
- P3: The reveal counts per player count were unclear, especially for 4 players.
- P4: Without any cost to staying, bidding 1 every round is a cheap fallback that collects consolation income with no risk.

## Changes

- Staying costs a non-refundable entry fee of 1 mouse, paid when STAY is chosen. Losing stayers receive no consolation. Droppers receive 2 mice. (fixes: P1): A losing stayer now ends the round 3 mice behind a dropper (-1 against +2). Staying only pays when the chance of winning a good sack at a good price justifies it. DROP is not dominant either: if everyone else drops, a lone stayer wins at price 1 and nets V-2 against 2, which is better whenever V > 4.
- The stay/drop decision comes after the first reveal and the talk, and the entry fee makes it a real gamble. (fixes: P2): The revealed cards and the rivals' claims now decide whether paying to enter is worth it.
- Exact reveal counts are stated for every player count. With 3 players: 1 card in the first reveal, 1 in the second, 1 hidden. With 4 players: 2, then 1, with 1 hidden. With 5 players: 2, then 1, with 2 hidden. (fixes: P3): Removes the ambiguity, and every player count keeps at least one hidden card at bidding time.
- A player needs at least 2 mice to stay (1 for the fee and at least 1 to bid). Otherwise they must drop. (fixes: P4): Keeps the fee-plus-bid rule consistent. Always-STAY-bid-1 now bleeds 1 mouse per lost round and ends far behind.

## Kept from the original

- Every player feeds one card per round into a shared sack, so you build the sack your rivals may buy
- Cats with positive and negative values, a worthless Rabbit, and a Dog that cancels the top cat only when it is alone
- Gradual revealing of the sack before and during bidding
- A choice between bidding for the sack and taking a safe mouse income
- Final score of cat points plus remaining mice, so mice are both bidding power and points

## The variation's rules

SETUP
- Every player receives the same 9 cards: cats worth -8, -5, 3, 5, 8, 11 and 15, one Rabbit worth 0, and one Dog worth 0.
- One card is removed at random from each hand. Its owner is told which card it is. No one else is told.
- Each player starts with 15 mice and 0 cat points. The bank of mice is unlimited.
- Seats are numbered. Seat 1 is the start player in round 1.
- The game lasts 8 rounds, so every remaining card is played.

EACH ROUND
1. Start player. In round 1 it is Seat 1. In each later round it is the next seat in order. The start player matters only for breaking ties.
2. Fill the sack. All players at the same time secretly choose one card from their hand and place it in the sack. Placed cards never return.
3. Shuffle. The engine shuffles the sack into a random order.
4. First reveal. Cards are shown from the front of the shuffled order. With 3 players, 1 card is shown. With 4 or 5 players, 2 cards are shown. Revealed cards do not say who placed them.
5. Talk. Every player writes one short message at the same time, without seeing the others' messages. All messages are then shown. Claims are not binding and may be lies.
6. Stay or drop. All players at the same time choose STAY or DROP. A player with fewer than 2 mice must DROP.
7. Entry and drop payment. Each player who chose STAY pays 1 mouse to the bank immediately. This fee is never refunded. Each player who chose DROP receives 2 mice from the bank and is out for this round.
8. Second reveal. The next card in the shuffled order is shown to everyone.
9. Sealed bid. Every player who chose STAY secretly bids a whole number of mice, from 1 up to their current mice (counted after paying the fee). All bids are revealed together.
10. Winner. The highest bidder wins the sack.
   - If two or more players tie for the highest bid, the tied player with fewer current mice wins.
   - If they are still tied, the tied player who comes first in seat order, counting from the start player, wins.
   - If nobody stayed, nobody wins and the sack is discarded.
   - If exactly one player stayed, that player wins and pays their bid.
11. Sack value. All remaining sack cards are revealed. The sack's value is the sum of the cats in it. The Rabbit and Dogs are worth 0.
   - If exactly one Dog is in the sack and the sack holds at least one cat, the cat with the highest value is removed before summing.
   - Two or more Dogs have no effect.
12. Payment. The winner pays their bid to the bank and adds the sack's value to their cat points. The value may be negative.
13. Losing stayers receive nothing. They have already paid their fee.
14. Discard. All sack cards are discarded face up, so everyone can count which cards have been used.
15. End check. After round 8 the game ends.

SCORING
Each player's total is their cat points plus their mice.

Objective: After round 8 the player with the highest total (cat points plus mice) wins. If totals are tied, the tied player with the most cat points wins. If that is also tied, the game is a draw among those players.

Expected effect: Staying is now a priced risk. A losing stayer falls 3 mice behind a dropper, so players stay only when the revealed cards, the counted discards and the talk suggest a sack worth more than about bid + 3. DROP is not dominant either: when the table drops, a lone stayer buys the sack for 1 mouse.

Simple-policy checks:
- Always DROP ends with 31 points and 0 cat points. It loses to any player who buys two decent sacks at a margin, since a sack of value 12 bought for 4 nets 7 against DROP's 2.
- Always STAY bidding 1 loses about 1 mouse per lost round and ends near 7 plus a few cheap sacks, so it loses to sensible play.
- Always STAY bidding everything wins round 1 at a loss of about 15 mice, then is stuck dropping, so it loses.
- Random play overpays and enters bad sacks, so it loses.

Talk earns its place because interests conflict. Each player wants rivals to enter bad sacks (where they themselves dumped the -8 or the Dog) and to drop out of good sacks. A player who believes 'I put in the 15, stay!' may pay a fee and a bid for a sack holding the speaker's -8, or a lone Dog that wipes out the 15. A follower can therefore lose, and talk tests reading and bluffing. Endgame: the face-up discards make the last rounds a counting puzzle rather than an unravelling, because there is no cooperation to betray. Seat order only breaks ties and rotates, and all hands are identical apart from one removed card, which shapes what you can dump rather than who wins.

## Complexity (the designer's count, against the limits)

- steps_per_round: 15 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 13 (limit 20)
- hidden_elements: 3 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 8 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
