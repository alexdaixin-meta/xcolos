# Kobayakawa Duel Rounds with Table Talk

Over 10 rounds, players hold one secret card, may swap it blind, talk, then fight for a pot. The lowest fighter's card adds the face-up Kobayakawa value, and the highest total takes the pot plus 1 kamon from the centre.

Players: 3 to 5, best with 4

## Parameters

- `starting_kamons` = 5
- `centre_starting_kamons` = 10
- `rounds` = 10
- `deck_size` = 15
- `card_min` = 1
- `card_max` = 15
- `fight_stake` = 1
- `centre_bonus` = 1
- `hand_cards_per_player` = 1
- `reserve_cards_per_player` = 1
- `minimum_fighters_for_showdown` = 2

## Round

1. **update** (all players): round += 1; deck = [1..15] (a fresh deck); reserve_cards = []; pot = 0; fighter_count = 0; lowest_card = 0; winner_seat = 0; for every player: draw_choice = '', discarded = 0, message = '', fight_choice = '', fought = false, revealed_card = 0, total = 0
2. **update** (all players): For each player: draw one random card from deck into hand and remove it from deck. Then, for each seat in order: draw one random card from deck, append it to reserve_cards and remove it from deck. Then draw one random card from deck into kobayakawa and remove it from deck. Announce: 'Round {round}: the Kobayakawa card K is {kobayakawa}.'
3. **sync** (all players): Each player sees their own hand, every player's kamons, the centre and kobayakawa.
4. **poll** (all players): draw_choice = the answer
5. **update** (all players): For each player with draw_choice == 'SWAP': discarded = hand; hand = reserve_cards[seat-1]. Announce each discard: 'Seat {seat} swapped and discarded {discarded}.'
6. **sync** (each player with draw_choice SWAP): Each swapping player sees their new hand.
7. **poll** (all players): message = the answer; broadcast {"to": "all", "text": "Seat {seat} says: {value}"} once all messages are in
8. **poll** (all players): fight_choice = the answer; fought = (fight_choice == 'FIGHT')
9. **update** (all players): For each player with fought: kamons -= 1; pot += 1. fighter_count = the number of players with fought.
10. **update** (the single fighter): when fighter_count == 1: that player's kamons += pot; pot = 0. The card is not revealed and the centre is unchanged.
11. **update** (all fighters): when fighter_count >= 2: lowest_card = min(hand) over players with fought; for each player with fought: revealed_card = hand; total = hand + (hand == lowest_card ? kobayakawa : 0)
12. **update** (the showdown winner): when fighter_count >= 2: winner_seat = the fighter with the largest (total * 100 - hand), so the highest total wins and a tie goes to the lower card; that player's kamons += pot + min(1, centre); centre -= min(1, centre); pot = 0
13. **tell** (all players): Announce the fighters, each revealed_card and total, winner_seat, and every player's kamons and the centre.
14. **check** (all players): End the game if round >= 10; otherwise continue.

## Ending

- ends when: round >= 10
- ranked by: `you.kamons` (the highest wins; players level at the top share the win)
- decided by: After round 10, each player's standing is their kamons. The most kamons wins, and players tied for most share the result (the source calls this a draw).

## Choices the source did not make

- 3 to 5 players, suggested 4: The designer suggests 4, so it is kept. Below 3 a showdown is just a duel with no one to bluff off the table. Above 5 the 15-card deck cannot cover a hand and a reserve for every player plus K (6 players would need 13 of the 15 cards, leaving swaps and discards nearly fully informative), and one player's choice matters less.
- Table talk kept as a simultaneous poll broadcast to all: The source requires simultaneous messages. Talk earns its place because interests conflict: a player can claim a high card to scare others into passing, or a low card to bait fighters when K is large.
- Reserve cards stored as a hidden table list in seat order: Nobody may see a reserve card, and a player attribute cannot be hidden from its owner, so the reserves live on the table with visibility none.
- The tie-break is coded as the largest (total * 100 - card): Totals are at most 30, so this ranks by total first and by the lower card second. Cards are distinct, so the result is unique.
- Strategy at the table: A thoughtful player weighs K against their card (a low card plus a big K can win), reads public discards and messages, bluffs about strength, and saves kamons near 0, because staying out also keeps them alive.

## Simplifications

- A tie for most kamons at the end is a shared win rather than a declared draw: The engine ranks by one expression and players level at the top share the win, which is how it expresses the source's draw.

## Unsupported (needs engine work)

- none
