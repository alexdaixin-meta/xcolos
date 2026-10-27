# Skull King: Three-Card Raids

Eight rounds of three simultaneous tricks: secretly bid how many tricks you will win, then play cards from a private 3-card hand. Exact bids score and pay capture bonuses.

Players: 3 to 5, best with 4

## Parameters

- `deck_size` = 18
- `hand_size` = 3
- `tricks_per_round` = 3
- `rounds` = 8
- `bid_min` = 0
- `bid_max` = 3
- `number_card_min` = 1
- `number_card_max` = 12
- `escape_count` = 2
- `escape_power` = 0
- `mermaid_count` = 1
- `mermaid_power` = 20
- `pirate_a_power` = 30
- `pirate_b_power` = 31
- `skull_king_count` = 1
- `skull_king_power` = 40
- `zero_bid_success_points` = 30
- `zero_bid_fail_points` = -30
- `exact_bid_points_per_trick` = 20
- `missed_bid_points_per_trick_off` = -10
- `pirate_capture_bonus` = 20
- `skull_king_capture_bonus` = 40
- `starting_score` = 0
- `tricks_won_per_trick` = 1

## Round

1. **update** (all players): round += 1; trick_number = 0; deck = [1,2,3,4,5,6,7,8,9,10,11,12,0,0,20,30,31,40]; every hand = []; every tricks_won = 0; every bonus = 0; every round_points = 0
2. **update** (all players): Deal: 3 times for each player, pick a random card from deck, append it to that player's hand and remove it from deck. This is the round's only random event.
3. **sync** (all players): each player privately sees their own hand
4. **poll** (all players): bid = answer; no bid is shown until all are in
5. **tell** (all players): announce every player's bid
6. **update** (all players): trick_number += 1; every played = -1; trick_winner = 0
7. **poll** (all players): played = answer; remove one copy of answer from hand; nobody sees a card until all are in
8. **tell** (all players): reveal every player's played card
9. **update** (all players): if some player played 20 and some player played 40: trick_winner = seat with played == 20; else if max(played) > 0: trick_winner = seat with played == max(played) (unique, since only the Escapes share a power); else trick_winner = 0. If trick_winner != 0: that player's tricks_won += 1. If the winner played 40: winner's bonus += 20 * (count of players with played == 30 or played == 31). If the winner played 20 and some player played 40: winner's bonus += 40.
10. **tell** (all players): announce trick_winner (or that nobody won) and any bonus recorded
11. **repeat** (all players): run the trick steps again (from 'trick_number += 1' through the trick announcement) until trick_number == 3
12. **update** (all players): for each player: if bid == 0 and tricks_won == 0: round_points = 30; if bid == 0 and tricks_won >= 1: round_points = -30; if bid >= 1 and tricks_won == bid: round_points = 20 * bid + bonus; if bid >= 1 and tricks_won != bid: round_points = -10 * abs(bid - tricks_won). Then score += round_points.
13. **tell** (all players): announce each player's tricks_won, round_points and score
14. **update** (all players): every tricks_won = 0; every bonus = 0
15. **check** (all players): end the game if round == 8, otherwise continue

## Ending

- ends when: round == 8 after the round's scoring
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their total score after 8 rounds. The highest total wins; players tied for the highest total share the result, which is the source's draw.

## Choices the source did not make

- 3 to 5 players, suggested 4: The designer chose 4. Three is the smallest table where tricks are contested enough for bidding to be hard. Five is the cap because 15 of the 18 cards are dealt, and more seats would exhaust the deck.
- Cards are stored as their power values: Every card except the two Escapes has a unique power, so the value identifies the card, and resolving a trick is plain arithmetic on played.
- Trick steps are written once and run again with repeat until trick_number == 3: The three tricks are identical in the source.
- No talk step: The source states there is no talk phase.
- Strategy at the table: A thoughtful player bids from hand strength and from what others' bids imply. During tricks they dump Escapes or low cards to hit a bid exactly, or hold the Mermaid back to catch the Skull King.

## Simplifications

- A tie for the highest total is a shared win rather than a separate 'draw' outcome: The engine has no separate draw; players level at the top share the win, which is equivalent.

## Unsupported (needs engine work)

- none
