# Concealed Quadrille

Four-player trick-taking game over 8 hands of 5 tricks. Players bid for the contract, the Taker names trumps and secretly calls a partner (or plays solo), and the hand is scored to zero sum.

Players: 4 to 4, best with 4

## Parameters

- `deck_size` = 20
- `suits` = 4
- `ranks_per_suit` = 5
- `hand_size` = 5
- `hands` = 8
- `tricks_per_hand` = 5
- `rounds` = 40
- `bid_pass_value` = 0
- `bid_min` = 3
- `bid_max` = 5
- `all_pass_contract` = 3
- `declaration_options` = 16
- `spadille_code` = 11
- `baste_code` = 21
- `power_spadille` = 30
- `power_manille` = 29
- `power_baste` = 28
- `power_trump_base` = 20
- `power_off_suit` = 0
- `solo_multiplier` = 3
- `trumps_red` = 7
- `trumps_black` = 6
- `tiebreak_key_bid_multiplier` = 10
- `rank_score_multiplier` = 100

## Round

1. **update** (all players): round_no += 1; hand_no = ceil(round_no/5); trick_in_hand = round_no - 5*(hand_no-1); priority_seat = ((hand_no-1) mod 4)+1; every played_card = 0 and power = 0
2. **update** (all players): when trick_in_hand == 1: return all cards to deck (deck = all 20 codes, every hand = []), then deal 5 random cards from deck to each player's hand (remove from deck, append to hand); every hand_tricks = 0, bid = 0, is_partner = false
3. **sync** (all players): when trick_in_hand == 1: each player is sent their own hand by name and code
4. **poll** (all players): when trick_in_hand == 1: bid = 0 for Pass, else the number; all bids announced together
5. **update** (all players): when trick_in_hand == 1: key(seat) = bid*10 + (4 - ((seat - priority_seat) mod 4)); if every bid == 0 then taker = priority_seat and contract = 3, else taker = seat with max key and contract = that seat's bid; announce taker and contract
6. **ask** (seat taker): when trick_in_hand == 1: trump = chosen suit number; partner_seat = chosen seat; is_solo = (partner_seat == taker); announce trump only
7. **update** (seat partner_seat): when trick_in_hand == 1 and is_solo == false: is_partner of partner_seat = true; that player alone is privately told 'you are the Taker's partner'
8. **update** (all players): leader = taker if trick_in_hand == 1, else last_winner
9. **ask** (seat leader): leader's played_card = chosen code; remove it from hand; announce the card by name and code
10. **update** (all players): suit(c) = trump if c in {11,21}, else floor(c/10); led_suit = suit(leader's played_card)
11. **poll** (every seat except leader): each responder's played_card = chosen code; remove it from hand
12. **update** (all players): for each player with c = played_card, r = c mod 10: power = 30 if c == 11; 29 if c == 10*trump+2; 28 if c == 21; 20 + r if floor(c/10) == trump; r if suit(c) == led_suit; else 0
13. **update** (all players): last_winner = seat with the highest power (ties impossible); last_winner's tricks_won += 1 and hand_tricks += 1; announce all four cards and the winner
14. **update** (all players): when trick_in_hand == 5: hand_total = taker.hand_tricks + (is_solo ? 0 : partner_seat.hand_tricks); hand_delta = contract-1 if hand_total >= contract; -(contract-1) if hand_total == contract-1; -contract if hand_total <= contract-2
15. **update** (all players): when trick_in_hand == 5: if is_solo then taker.score += 3*hand_delta and each other seat score -= hand_delta; else taker and partner_seat score += hand_delta and the other two score -= hand_delta
16. **tell** (all players): when trick_in_hand == 5: announce partner_seat (or that it was a solo), hand_total, hand_delta and all scores
17. **check** (all players): end the game if round_no == 40, else continue

## Ending

- ends when: round_no == 40
- ranked by: `you.score * 100 + you.tricks_won` (the highest wins; players level at the top share the win)
- decided by: Highest score wins; among players tied on score, the one with the most tricks won over the game wins; players still level share the win (a draw).

## Choices the source did not make

- 4 players, fixed: The designer set 4. The deck (20 cards = 4 x 5), the partner call and the priority rotation are all built for exactly four seats.
- No talk phase: The rules forbid discussion; bids and cards are the only signals. A player's strategy lies in bidding to hand strength, choosing a partner who likely holds key trumps, and inferring the hidden partner from play.
- Ranking expression score*100 + tricks_won: tricks_won is at most 40 (under 100), so score dominates and tricks_won only breaks ties; players still level share the win, which serves as the draw.
- Card power stored as public player attributes: Power is computed only from public played cards, so showing it reveals nothing new.

## Simplifications

- The deck is rebuilt from all 20 codes at the start of each hand instead of physically gathering the cards: This is equivalent to gathering and shuffling, since all 20 cards are always played out over the 5 tricks.
- Hand-start and hand-end steps run in every round, gated by conditions on trick_in_hand: The engine's step list is flat; per-step conditions reproduce the source's 'first trick' and 'fifth trick' steps.

## Unsupported (needs engine work)

- none
