# Skull King: Three-Card Bids

Over 8 rounds, players are dealt 3 cards from an 18-card deck, bid at the same time on how many of 3 simultaneous tricks they will win, and score for bidding exactly right, with bonuses when the Skull King captures Pirates or the Mermaid captures the Skull King.

Players: 3 to 5, best with 4

## Parameters

- `hand_size` = 3
- `tricks_per_round` = 3
- `rounds` = 8
- `bid_min` = 0
- `bid_max` = 3
- `deck_size` = 18
- `number_card_min` = 1
- `number_card_max` = 12
- `escape_count` = 2
- `escape_power` = 0
- `mermaid_power` = 20
- `pirate_a_power` = 30
- `pirate_b_power` = 31
- `skull_king_power` = 40
- `exact_bid_points_per_trick` = 20
- `missed_bid_penalty_per_trick` = 10
- `zero_bid_success_points` = 20
- `zero_bid_failure_penalty` = 20
- `skull_king_bonus_per_pirate` = 30
- `mermaid_captures_skull_king_bonus` = 50

## Round

1. **update** (all players): round += 1. For every player: tricks_won = 0, bonus = 0, hand = [], played = -1. Table: trick = 0.
2. **update** (all players): deck = [1,2,3,4,5,6,7,8,9,10,11,12,0,0,20,30,31,40]. All 18 cards are gathered; shuffling happens through the random draws.
3. **update** (each player in turn): Deal hand_size (3) cards to each player, one at a time in seat order. Each card is a random draw: it is removed from deck and appended to that player's hand. The remaining cards stay in deck, hidden.
4. **sync** (all players): Each player privately sees their own hand.
5. **poll** (all players): Each player's answer is stored as that player's bid. No player sees another's bid until all are in.
6. **tell** (all players): Announce every player's bid to everyone.
7. **poll** (all players): played = the chosen power. That card is removed from the player's hand.
8. **tell** (all players): Reveal every player's played card to everyone.
9. **update** (all players): Table: mermaid_played = (some player's played == 20); skull_king_played = (some player's played == 40); pirates_in_trick = count of players whose played is 30 or 31; max_power = the maximum of played over all players.
10. **update** (all players): The trick winner is: if mermaid_played and skull_king_played, the player whose played == 20; otherwise the player whose played == max_power. For the winner: tricks_won += 1. If the winner's played == 40: bonus += 30 * pirates_in_trick. If the winner's played == 20 and skull_king_played: bonus += 50. Then trick += 1.
11. **repeat** (all players): Run the play, reveal, resolve and award steps again until trick == tricks_per_round (3).
12. **update** (all players): For each player: if bid >= 1 and tricks_won == bid, score += 20 * bid + bonus; if bid >= 1 and tricks_won != bid, score -= 10 * |tricks_won - bid|; if bid == 0 and tricks_won == 0, score += 20; if bid == 0 and tricks_won >= 1, score -= 20. Announce the round's results.
13. **check** (all players): If round == rounds (8), end the game; otherwise start the next round.

## Ending

- ends when: round == 8
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: After round 8, each player's standing is their total score. The highest score wins, and players tied for the highest share the win (a draw among them).

## Choices the source did not make

- 3 to 5 players, 4 suggested: The designer's table size of 4 is kept. The minimum is 3 because, with fewer, one player could hold both Escapes and a trick could end in a tie, and bids would have no rivals to read. The maximum is 5 because 5 x 3 = 15 cards fit an 18-card deck with some cards left unseen, and more seats would leave no uncertainty about the undealt cards.
- Strategy at the table: A thoughtful player bids from the strength of their hand and from how many high cards are still unseen. After the announced bids, they time their strong cards against the tricks rivals need, and they spend Escapes to avoid unwanted wins. Simultaneous play rewards predicting when others will commit their Pirates and the Skull King.
- No talk step: The source states there is no discussion phase.
- Table attributes mermaid_played, skull_king_played, pirates_in_trick, max_power and trick: The engine cannot compare one player's attribute against another's directly, so the trick resolution is computed through table attributes. The three tricks are counted with trick.
- The played attribute resets to -1 each round: This is a sentinel meaning no card played yet, so it cannot be confused with an Escape (power 0).

## Simplifications

- Shuffling is modelled as random draws from the freshly refilled deck list: The engine draws at random from a list, which is equivalent to shuffling and dealing.
- The three tricks use a repeat over the play, reveal, resolve and award steps, counted by trick: The engine runs a flat step list, so repetition happens through repeat with a counter.

## Unsupported (needs engine work)

- none
