# Biblios: The Scriptorium (revised)

Three scribes take turns splitting a three-card deal into a kept card, a lot that everyone bids on and a gift for a rival. They collect colour cards to win colours and play Church cards to move each colour's VP die.

Players: 3 to 3, best with 3

## Parameters

- `deck_size` = 36
- `colours` = 3
- `colour_cards_per_colour` = 7
- `colour_value_1_copies` = 2
- `colour_value_2_copies` = 2
- `colour_value_3_copies` = 2
- `colour_value_4_copies` = 1
- `colour_total_per_colour` = 16
- `gold_cards` = 9
- `gold_value_1_copies` = 3
- `gold_value_2_copies` = 3
- `gold_value_3_copies` = 3
- `gold_cards_total` = 18
- `church_cards` = 6
- `starting_gold` = 4
- `die_start` = 3
- `die_min` = 1
- `die_max` = 5
- `rounds` = 12
- `cards_per_round` = 3
- `bid_min` = 0
- `bid_max` = 22
- `max_church_per_player_per_round` = 2
- `rank_vp_weight` = 100

## Round

1. **update** (all players): round += 1; active_seat = ((round - 1) mod 3) + 1. Announce 'Round {round}: seat {active_seat} is active.'
2. **update** (seat active_seat): Draw 3 cards at random from deck into the active player's offer, as positions 1, 2 and 3, and remove them from deck. Only the active player sees offer.
3. **poll** (all players): Each message is broadcast to all as 'Seat {seat} says: {value}'. Talk is not binding.
4. **ask** (seat active_seat): The keep card is appended to the active player's hand and new_cards. lot = the sell card. gift = the remaining card. offer = [].
5. **tell** (all players): Announce 'Lot: {lot}. Gift: {gift}.' The kept card stays secret.
6. **poll** (all players): bid = answer; effective_bid = min(bid, gold).
7. **update** (all players): lot_winner = the seat with the highest effective_bid. On a tie, the active seat wins if it is among the tied; otherwise the tied seat that comes first clockwise after the active seat wins. If all bid 0, the active seat wins. The winner's gold -= the winner's effective_bid. lot is appended to the winner's hand and new_cards. All three bids are announced.
8. **update** (all players): If lot_winner != active_seat: gift_receiver = the non-active seat that is not lot_winner. Otherwise gift_receiver = the non-active seat with the lower effective_bid; on a tie, the seat next clockwise after active_seat. gift is appended to gift_receiver's hand and new_cards. Announce the receiver.
9. **update** (all players): For each player, each 'Gold N' card in new_cards is removed from hand, and gold += N.
10. **update** (all players): For each player, church_count = the number of 'Church' cards in new_cards, and those cards are removed from hand. Announce each church_count.
11. **poll** (each player with church_count >= 1): church_choice = answer.
12. **update** (all players): net = the sum of church_count over players with church_choice 'red up' minus the sum over players with 'red down'; vp_red = min(5, max(1, vp_red + net)).
13. **update** (all players): net = the sum of church_count over 'green up' minus the sum over 'green down'; vp_green = min(5, max(1, vp_green + net)).
14. **update** (all players): net = the sum of church_count over 'blue up' minus the sum over 'blue down'; vp_blue = min(5, max(1, vp_blue + net)). Announce vp_red, vp_green, vp_blue and each player's church_choice.
15. **update** (all players): For every player: church_count = 0, bid = 0, effective_bid = 0, church_choice = '', new_cards = []. Set lot = '', gift = '', lot_winner = 0 and gift_receiver = 0.
16. **update** (all players): Runs only when round == 12. For each player: red_sum, green_sum and blue_sum = the totals of that colour's card values in hand. For each colour, the player with the strictly highest sum gets vp += that colour's die value (vp_red, vp_green or vp_blue). If the highest is tied, nobody scores that colour. Announce each vp and gold.
17. **check** (all players): If round == 12, end the game; otherwise start the next round.

## Ending

- ends when: round == 12
- ranked by: `you.vp * 100 + you.gold` (the highest wins; players level at the top share the win)
- decided by: The most VP wins. A VP tie is broken by the most remaining Gold. Players still tied share the win, which is a draw among them.

## Choices the source did not make

- 3 players (min 3, max 3, suggested 3): The designer fixed 3 seats. The active rotation, the gift rules (lot to one non-active player, gift to the other) and the 36-card deck (12 rounds x 3 cards) only work at exactly 3.
- Bid upper limit of 22: The rules say bids run from 0 upward. 22 is the most gold a player can ever hold (4 + 18), and any higher bid would count as the player's whole gold anyway.
- Talk is a simultaneous poll broadcast to all: The rules say messages are written at the same time without seeing the others. Talk earns its place because players disagree about colours and dice, and bluffing about the kept card matters.
- Ranking expression vp * 100 + gold: Gold never exceeds 22, so this ranks by VP first and gold second, and a full tie shares the win as the rules' draw.
- The gift tie-break and lot comparisons use effective bids: The rules say a bid above a player's gold counts as exactly their gold.
- Dealt cards are stored in a per-player offer list: The cards must be visible only to the active player, which a public or hidden table attribute cannot express.
- Card values are listed as numeric copy counts in parameters: Parameters must be numbers, so the value lists 1,1,2,2,3,3,4 and 1,1,1,2,2,2,3,3,3 are given as the number of copies of each value.

## Simplifications

- Scoring runs as a conditional update in round 12, before the end check: The engine's round is a flat list, so a step with a 'round == 12' condition does the scoring before the game ends.
- Cards entering a hand are tracked in a scratch new_cards list: The Gold and Church steps act on cards that entered a hand this round, so this needs explicit state.

## Unsupported (needs engine work)

- none
