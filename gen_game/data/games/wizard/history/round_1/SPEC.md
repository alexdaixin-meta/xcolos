# Three-Card Wizard

Over 12 rounds, players are dealt 3 cards, publicly bid how many of the 3 tricks they will take, then play the tricks with trump, Wizards and Jesters; an exact bid scores 20 + 10 per trick and a missed bid loses 10 per trick off.

Players: 3 to 4, best with 3

## Parameters

- `deck_size` = 25
- `suit_count` = 3
- `rank_min` = 1
- `rank_max` = 7
- `numbered_cards` = 21
- `wizard_count` = 2
- `jester_count` = 2
- `hand_size` = 3
- `tricks_per_round` = 3
- `rounds` = 12
- `bid_min` = 0
- `bid_max` = 3
- `forbidden_bid_total` = 3
- `exact_bid_bonus` = 20
- `points_per_trick_on_exact_bid` = 10
- `penalty_per_trick_off` = 10
- `first_dealer_seat` = 1
- `wizard_power_base` = 100
- `trump_power_base` = 50
- `led_suit_power_base` = 20
- `jester_power_base` = 5
- `offsuit_power` = 0

## Round

1. **update** (all players): Shuffle: deck = all 25 cards. Each hand = [], bid = -1, tricks = 0, played_card = ''. bid_total = 0, trick_no = 0, led_suit = ''. leader = (dealer mod N) + 1.
2. **update** (all players): Deal 3 cards to each player: 3 times per player, pick a random card from deck, append it to that player's hand and remove it from deck. Then pick one more random card from deck, set trump_card to it and remove it from deck. trump_suit = the suit of trump_card if it is a numbered card; otherwise (Wizard or Jester) trump_suit = 'none'. Announce trump_card and trump_suit.
3. **sync** (all players): Each player sees their own hand, the trump_card, the trump_suit and the dealer.
4. **ask** (each player in turn, starting with seat (dealer mod N)+1 and ending with the dealer): The player's bid = answer; bid_total += answer. Each bid is announced publicly.
5. **update** (all players): Start a trick: played_card = '', play_pos = 0 and power = 0 for every player; led_suit = ''.
6. **ask** (each player in turn, starting with seat leader and going round the table): Remove the card from hand; played_card = card; play_pos = 1 + the number of players who have already played to this trick. If led_suit = '' and the card is a Wizard and play_pos = 1, then led_suit = 'none'. If led_suit = '' and the card is numbered, then led_suit = the card's suit. The card is shown to everyone.
7. **update** (all players): For each player, power = 100 - play_pos if played_card is a Wizard; 50 + rank if it is numbered and its suit = trump_suit; 20 + rank if it is numbered and its suit = led_suit (and it is not trump); 5 - play_pos if it is a Jester; 0 otherwise. The player with the highest power wins the trick: their tricks += 1, leader = that seat, trick_no += 1. Announce the trick winner.
8. **repeat** (all players): Repeat the three trick steps above (start a trick, play cards, find the winner) until trick_no = 3.
9. **update** (all players): For each player: if tricks = bid, then score += 20 + 10 * tricks; otherwise score -= 10 * |bid - tricks|. Announce each bid, tricks and score.
10. **update** (all players): round_no += 1; dealer = (dealer mod N) + 1.
11. **check** (all players): If round_no = 12, end the game; otherwise start the next round.

## Ending

- ends when: round_no >= 12
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their total score after 12 rounds. The highest total wins. If players tie at the top, they share the result, which stands for the source's draw.

## Choices the source did not make

- 3 to 4 players, suggested 3: The designer's size is kept. With 3 players the dealer's restriction (the bids may not total exactly 3) forces at least one player to miss, so reading the earlier bids and your seat matters. At 4 players, 13 of the 25 cards are used, so the deck still fits. The minimum is 3 because with 2 players bidding and the dealer's restriction lose most of their tension. The maximum is not larger because the source stops at 4.
- No free talk step: The source has no table talk. The public bids are the only signal, so adding talk would add a mechanic.
- Card power values for finding the trick winner: The order of the trick-winner rules is encoded arithmetically: first Wizard = 100 - play_pos, trump = 50 + rank, led suit = 20 + rank, Jester = 5 - play_pos, any other card = 0. The highest power reproduces the source's order. Whenever a numbered card is present, it is either trump or of the led suit, so it beats Jesters.
- The 2 Wizards and 2 Jesters are named A and B: They are identical in play. The names only keep the hand and deck list entries distinct.
- The card played to a trick is chosen with ask in seat order from the leader: The source says each player sees the cards already played to that trick.

## Simplifications

- A tie at the top is shared by the tied players instead of being called a draw: The engine has no separate draw outcome. Players level at the top share the win, which is the same result.
- The three tricks are written as a repeat of the trick steps until trick_no = 3: The engine's step list is flat. A repeat expresses the fixed loop of 3 tricks.

## Unsupported (needs engine work)

- none
