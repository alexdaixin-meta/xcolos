# For Sale: Sealed Bids - Four Player

Bid secretly for properties then sell them secretly for cheques; richest total wins.

Players: 4 to 4, best with 4

## Parameters

- `starting_coins` = 18
- `property_low` = 1
- `property_high` = 30
- `property_deck_size` = 30
- `property_deck_used` = 28
- `cheque_low` = 0
- `cheque_high` = 15
- `cheque_copies` = 2
- `cheque_deck_size` = 30
- `cheque_deck_used` = 28
- `total_rounds` = 14
- `buying_rounds` = 7
- `selling_rounds` = 7
- `cards_per_round` = 4

## Round

1. **initialize** (all players): set coins to 18 cheque_total to 0 properties to [] bid to 0 selected_property to 0 final_money to 0 property_deck to 1 to 30 cheque_deck to 0,0,2,2 to 15,15 round_number to 1 current_offer to []
2. **sync** (all players): send each player their coins cheque_total and properties
3. **update** (all players): when round_number is 1 remove 2 unseen cards from property_deck then move next 4 cards from property_deck to current_offer sorted HIGH SECOND THIRD LOW and set priority_seat to ((round_number-1) mod 4)+1
4. **poll** (all players): set you.bid to sealed bid 0 up to you.coins
5. **update** (all players): rank bids high to low breaking ties by priority_seat order wrapping 4 to 1 then first-ranked takes HIGH and pays full bid from coins second takes SECOND and pays (bid+1)//2 third takes THIRD and pays (bid+1)//2 fourth takes LOW and pays (bid+1)//2 and append taken property to you.properties
6. **tell** (all players): broadcast which player took HIGH SECOND THIRD LOW without revealing bid amounts or coin totals
7. **update** (all players): when round_number is 8 remove 2 unseen cheques from cheque_deck then move next 4 cheques from cheque_deck to current_offer sorted highest to lowest
8. **poll** (all players): set you.selected_property to one property from you.properties
9. **update** (all players): rank selected_property high to low with no ties then highest adds highest cheque in current_offer to cheque_total second-highest adds second-highest third adds third lowest adds lowest and remove selected_property from you.properties to property_discard
10. **tell** (all players): broadcast who played which property and who took which cheque without revealing running cheque totals
11. **update** (all players): set round_number to round_number+1 and if round_number>14 set you.final_money to you.cheque_total+you.coins
12. **check** (all players): end the game when round_number>14 else continue

## Ending

- ends when: round_number > 14
- ranked by: `you.final_money * 1000 + you.coins` (the highest wins; players level at the top share the win)
- decided by: Standing is final_money equal to cheque_total plus remaining coins with remaining coins as tie-break; highest value wins and players level at the top share the win

## Choices the source did not make

- 4 to 4 players with suggested 4: designer fixed 4 seats with 4 cards per round and 28 usable cards for 7 each; smallest table where sealed simultaneous bidding and priority tie-break matter and larger table breaks 4-per-round reveal
- no talk poll, sealed poll for bids and for property choice: source says no talk phase and every choice sealed; simultaneous choice must use poll not ask so later seats do not hear earlier answers
- half rounded up as (bid+1)//2: matches example 0->0 1->1 2->1 3->2 4->2 with integer arithmetic
- rank_by you.final_money * 1000 + you.coins: encodes most final money wins with more remaining coins as tie-break within arithmetic ranking since coins never reach 1000
- priority_seat ((round_number-1) mod 4)+1: concrete arithmetic for stated tie-break rotation

## Simplifications

- shuffle represented as random draw from list and remove bottom 2 unseen first: engine shuffles by drawing at random from game list with remove/append operations
- current_offer holds sorted HIGH to LOW reveal and property_discard holds played properties: engine has no board so cards live in table lists and player lists
- final_money attribute set to cheque_total+coins after round 14: enables arithmetic ranking and observable score without model opinion

## Unsupported (needs engine work)

- none
