# Skull King: Three-Card Raids

Three players play 9 hands of 3 tricks each. Before each hand every player secretly bids how many tricks they will win, then scores for hitting the bid exactly and loses points for missing it, with bonuses for capturing Pirates or the Skull King.

Players: 3 to 3, best with 3

## Parameters

- `player_count` = 3
- `deck_size` = 25
- `green_cards` = 7
- `green_max_rank` = 7
- `yellow_cards` = 7
- `yellow_max_rank` = 7
- `black_cards` = 5
- `black_max_rank` = 5
- `pirates` = 2
- `escapes` = 2
- `mermaids` = 1
- `skull_kings` = 1
- `hands` = 9
- `tricks_per_hand` = 3
- `total_rounds` = 27
- `cards_dealt_per_player` = 3
- `cards_set_aside` = 16
- `bid_min` = 0
- `bid_max` = 3
- `exact_bid_points_per_trick` = 20
- `exact_zero_bid_points` = 20
- `missed_zero_bid_points` = -20
- `missed_bid_points_per_trick_difference` = -10
- `pirate_captured_by_skull_king_bonus` = 30
- `skull_king_captured_by_mermaid_bonus` = 40
- `trick_win_increment` = 1
- `starting_score` = 0

## Round

1. **update** (all players): When trick_in_hand == 1: return every card in each player's hand and in trick_cards to deck. Then, for each player, draw 3 cards at random from deck into their hand (remove from deck, append to hand); the 16 cards left in deck are set aside unseen. Set each player's bid = 0, tricks_won = 0, bonus = 0. Set leader = ((hand_number - 1) mod 3) + 1.
2. **sync** (all players): When trick_in_hand == 1: each player is sent their own hand. Nobody sees another player's hand.
3. **poll** (all players): When trick_in_hand == 1: each player's bid is set to their answer. No bid is shown until all are in.
4. **tell** (all players): When trick_in_hand == 1: announce every seat's bid for hand {hand_number} and the first leader, seat {leader}.
5. **update** (all players): Set trick_cards = [], lead_suit = '', and each player's played_card = ''.
6. **ask** (each player in turn, starting with seat leader and going clockwise): Remove the chosen card from the player's hand, append it (with the seat) to trick_cards, and set played_card. If lead_suit == '' and the card is Green, Yellow or Black, set lead_suit to that suit. Each player hears the cards played before them.
7. **update** (all players): Set trick_winner to the seat holding the first applicable card: (1) if trick_cards holds both SkullKing and Mermaid, the Mermaid; (2) else the SkullKing; (3) else the first Pirate played; (4) else the Mermaid; (5) else the highest Black card; (6) else, if lead_suit is not empty, the highest card of lead_suit; (7) else (all Escapes) the first card played. Add 1 to the winner's tricks_won. If the winning card is the SkullKing, add 30 to the winner's bonus for each Pirate in trick_cards. If the winning card is the Mermaid and trick_cards holds the SkullKing, add 40 to the winner's bonus. Set leader = trick_winner.
8. **tell** (all players): Announce the cards played (trick_cards), the trick_winner seat and any bonus just recorded.
9. **update** (all players): When trick_in_hand == 3, for each player: if bid >= 1 and tricks_won == bid, score += 20 * bid + bonus; if bid == 0 and tricks_won == 0, score += 20 + bonus; if bid == 0 and tricks_won > 0, score -= 20; if bid >= 1 and tricks_won != bid, score -= 10 * |bid - tricks_won|. Then set tricks_won = 0 and bonus = 0.
10. **tell** (all players): When trick_in_hand == 3: announce every seat's score after hand {hand_number}.
11. **update** (all players): round += 1. If trick_in_hand == 3, then hand_number += 1 and trick_in_hand = 1; otherwise trick_in_hand += 1.
12. **check** (all players): End the game if round > 27; otherwise continue with the next round.

## Ending

- ends when: round > 27
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their total score after 9 hands. The highest score wins, and players tied for the highest share the win (a draw among them).

## Choices the source did not make

- Exactly 3 players, suggested 3: The designer fixed the game at 3 seats, and the 25-card deck, the 3-card deal and the clockwise leader rotation are all built for 3. Minimum and maximum are both 3.
- No free-talk step before bids or plays: The source has no talk. Strategy comes from reading the revealed bids and the cards played (whether to win or duck a trick to land your own bid, or to spoil a rival's), so added talk would only add words.
- One trick per round, with the deal, bid and scoring steps run only when trick_in_hand is 1 or 3: The source sets each round to one trick (27 rounds). Single-step 'when' conditions keep the step list flat.
- Ties at the top share the win: The source calls a top tie a draw among the tied players, which is exactly a shared win.

## Simplifications

- The 16 undealt cards stay in the deck list rather than a separate set-aside pile: They are unseen and unused until the next hand's reshuffle, so a separate list adds nothing.
- Card play uses ask in seat order starting from the leader: Tricks are sequential in the source; each later player must see the earlier cards to follow suit.

## Unsupported (needs engine work)

- none
