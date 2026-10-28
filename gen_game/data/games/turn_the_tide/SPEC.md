# Turn The Tide: Short Seas (revised)

Over P deals of 10 hands, players play Weather cards at the same time to dodge high Tide levels and keep their lifelines. Each deal the hands pass to the left, and the highest total score wins.

Players: 3 to 4, best with 4

## Parameters

- `weather_cards_per_player` = 12
- `hand_size` = 11
- `hands_per_deal` = 10
- `tide_deck_size` = 20
- `tide_start_level` = 15
- `lifelines_per_deal` = 4
- `sunk_penalty` = 1
- `lowest_tide_bonus` = 1
- `deals_per_player` = 1
- `set_aside_cards_per_player` = 1
- `tie_break_weight` = 100

## Round

1. **update** (all players): When hand_no == 1 and deal_no >= 2: each player's pass_buffer = played + hand; then each player's hand = pass_buffer of the player on their right (each player passes to the left); played = [] for everyone.
2. **update** (all players): When hand_no == 1: tide_deck = cards 1 to 20; every tide = 15; every lifelines = 4; every sunk = false.
3. **sync** (all players): When hand_no == 1, each player is sent their hand, along with deal_no and all public attributes.
4. **update** (all players): Draw 2 cards at random from tide_deck and remove them from it; low_tide = the smaller, high_tide = the larger.
5. **tell** (all players): Announce: 'Deal {deal_no}, hand {hand_no}: Low Tide {low_tide}, High Tide {high_tide}.'
6. **poll** (all players): Each player's card_played = the chosen card; it is removed from hand and appended to played. All are revealed together.
7. **update** (all players): The player with the highest card_played sets tide = low_tide. The player with the second-highest card_played sets tide = high_tide. Sunk players are included. Everyone else keeps their tide.
8. **update** (all players): max_tide = the highest tide among players with sunk == false. For each player with sunk == false and tide == max_tide: if lifelines == 0 then sunk = true, else lifelines -= 1. If every player is Sunk, nothing changes.
9. **tell** (all players): Announce every card_played, tide, lifelines and sunk.
10. **update** (all players): When hand_no == 10: each player with sunk == false adds lifelines to score; each player with sunk == true subtracts 1 from score; min_tide = the lowest tide among players with sunk == false; each player with sunk == false and tide == min_tide adds 1 to score.
11. **update** (table): hand_no += 1; if hand_no > 10 then hand_no = 1 and deal_no += 1.
12. **check** (table): End the game when deal_no > P; otherwise continue.

## Ending

- ends when: deal_no > P (number of players)
- ranked by: `you.score * 100 - you.tide` (the highest wins; players level at the top share the win)
- decided by: The highest game score wins. A tie is broken by the lowest Tide level at the end of the last deal. Players still level on both share the win, which stands in for the source's draw.

## Choices the source did not make

- 3 to 4 players, suggested 4: The designer suggests 4, and the deck size and deal count scale with P. With fewer than 3 players, the highest and second-highest cards decide everyone's Tide. More than 4 is outside the deck design.
- No talk phase: The rules state there is no talk phase.
- Tie-break encoded as score*100 - tide: Tide is between 1 and 20, so it never outweighs a point of score, and a lower tide ranks higher.
- Hand passing modelled with a pass_buffer list: All players pass at once, so each 11-card set is gathered first and then moved to the left-hand neighbour.
- Count-dependent numbers written per player (weather_cards_per_player 12, deals_per_player 1, set_aside_cards_per_player 1): Parameters must be plain numbers. The Weather deck is 12*P cards, there are 1*P deals and 1*P cards set aside, so each holds at 3 and at 4 players.

## Simplifications

- The source's draw becomes a shared win: The engine has no separate draw: players level at the top share the win.
- Start-of-deal and end-of-deal work is done by steps conditioned on hand_no: The step list is flat, so these steps run every round but act only on hand 1 or hand 10.

## Unsupported (needs engine work)

- none
