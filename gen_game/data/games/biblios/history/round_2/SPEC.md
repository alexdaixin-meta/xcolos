# Biblios: Sealed Scriptorium (revised)

Three scribes each round secretly keep one of two cards, then sealed-bid for the other, while public Church cards and secret marks shift the worth of five colours that score by majority.

Players: 3 to 3, best with 3

## Parameters

- `deck_size` = 36
- `colour_cards` = 30
- `church_cards` = 6
- `colours` = 5
- `cards_per_colour` = 6
- `value_1_cards_per_colour` = 2
- `value_2_cards_per_colour` = 2
- `value_3_cards_per_colour` = 1
- `value_4_cards_per_colour` = 1
- `starting_gold` = 8
- `starting_worth` = 4
- `worth_min` = 2
- `worth_max` = 8
- `rounds` = 12
- `cards_revealed_to_active` = 2
- `bid_min` = 0
- `min_winning_bid` = 1
- `gold_income_per_round` = 1
- `mark_step` = 1
- `church_step` = 1
- `tie_share_divisor` = 2
- `gold_per_vp` = 5
- `min_majority_total` = 1

## Round

1. **update** (all players): round += 1. If round <= 6, active_seat = ((round - 1) mod 3) + 1; otherwise active_seat = 3 - ((round - 7) mod 3). This gives seats 1,2,3,1,2,3,3,2,1,3,2,1. Reset winner_seat = 0, high_bid = 0, high_count = 0 and every bid = 0.
2. **tell** (all players): Announce round, active_seat, worth_red, worth_blue, worth_green, worth_yellow, worth_purple, every player's gold and every player's public_cards.
3. **update** (seat {active_seat}): Set the active player's offer_a = deck[0] and offer_b = deck[1]. Remove both from deck. Nothing is announced.
4. **sync** (seat {active_seat}): The active player privately sees offer_a as Card A and offer_b as Card B.
5. **ask** (seat {active_seat}): The answer is private. If Keep A, kept_card = offer_a and lot = offer_b; if Keep B, kept_card = offer_b and lot = offer_a. Append kept_card to the active player's hidden_cards.
6. **tell** (all players): Announce publicly: 'This round's lot is {lot}.' Nothing about the kept card is announced.
7. **poll** (all players): message = the answer. Once all are in, broadcast {"to": "all", "text": "Seat {seat} says: {value}"}. Messages are not binding.
8. **poll** (all players): bid = the answer. No bid is seen until all three are in.
9. **update** (all players): Reveal every bid publicly. high_bid = max of bid over players; high_count = number of players with bid == high_bid. If high_bid >= 1 and high_count == 1, then winner_seat = the seat with that bid, and that player's gold -= high_bid (paid to the bank and removed from the game). Otherwise winner_seat = 0, nobody pays, and lot is appended to discard (face-up).
10. **update** (seat {winner_seat}): when winner_seat != 0 and lot != 'Church': append lot to the winner's public_cards.
11. **poll** (seat {active_seat}; also seat {winner_seat} when winner_seat != 0 and lot == 'Church'): (a) Append 'round:colour:direction:counts' to the active player's marks, where counts = yes if kept_card == 'Church', otherwise no. This changes no worth now. (b) The answer is recorded for the next step and announced publicly.
12. **update** (all players): when winner_seat != 0 and lot == 'Church': for the named colour, if worth + direction is between 2 and 8 inclusive, then worth_<colour> += direction; otherwise no change. Append the Church card to discard (face-up). Announce the new worth.
13. **update** (all players): Every player's gold += 1.
14. **update** (all players): when round == 12: reveal every player's hidden_cards and marks to all. Set each final_worth_<colour> = worth_<colour>. Then take every mark with counts = yes, from all players, sorted by round ascending, and apply them one at a time: if final_worth_<colour> + direction is between 2 and 8 inclusive, final_worth_<colour> += direction; otherwise the mark has no effect. Each mark is checked against the worth as already changed by earlier marks.
15. **update** (all players): when round == 12: for each player and each colour, total_<colour> = sum of the numeric values of that colour's cards in hidden_cards and public_cards together. Church cards count 0.
16. **update** (all players): when round == 12: for each colour, M = max of total_<colour> over players and K = number of players with total_<colour> == M. If M >= 1 and K == 1, that player's vp += final_worth_<colour>. If M >= 1 and K >= 2, each tied player's vp += floor(final_worth_<colour> / 2). If M == 0, nobody scores the colour. Then every player's vp += floor(gold / 5). Announce every player's final worths, totals and vp.
17. **check** (all players): If round == 12, end the game; otherwise begin the next round.

## Ending

- ends when: round == 12
- ranked by: `you.vp` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their VP after scoring: colour majorities at final worths plus 1 VP per full 5 gold. The highest VP wins; players tied at the top share the result (the source calls this a draw).

## Choices the source did not make

- Exactly 3 players (min 3, max 3, suggested 3): The designer fixed the table at 3, and the active-seat schedule (1,2,3,1,2,3,3,2,1,3,2,1) is written for three seats. Three is also the smallest table where a sealed-bid tie can void a lot and a majority can be split. A thoughtful player bluffs about the kept card, reads the others' bids and Church choices, and spends gold only where a majority can still be won.
- Keep the simultaneous talk step as a poll broadcast to all: The source requires it. It earns its place because players disagree about which colours should rise, and they can bluff about kept cards or try to steer bids.
- Cards are named as text '<Colour> <value>' and 'Church'; the top of the deck is index 0 after the single setup shuffle: The source gives no card labels, and it needs a fixed hidden order with a top card.
- Card values per colour are given as counts per value in parameters (two 1s, two 2s, one 3, one 4): Every parameter must be a number.
- Marks are stored as 'round:colour:direction:counts', with counts fixed when the mark is made: This lets scoring apply only the counting marks, in round order, by arithmetic, without working out again which card was kept each round.
- Per-colour totals and final worths are explicit attributes computed at scoring: The majority rule needs these numbers stored as state so they can be compared across players.
- The active player's choice of A or B is an ask to that seat alone: Only one player answers, and the answer is private.

## Simplifications

- Scoring runs as conditional steps (when round == 12) at the end of round 12 rather than as a separate phase: The step list is flat, so final scoring is gated by an arithmetic condition.
- A tie for most VP is shown as a shared win rather than a 'draw': The engine has no separate draw; players level at the top share the win, which is the same outcome in effect.
- Parts (a) and (b) of step 9 are one poll addressed to the active seat and, when it applies, the Church winner: The source says they are answered at the same time; a seat that is both gets both questions in the same poll.

## Unsupported (needs engine work)

- none
