# Da Bai Fen Duplicate

Four players in two fixed partnerships play 4 hands of 6 trick-taking rounds with a 26-card deck. Hands 3 and 4 replay the deals of hands 1 and 2, rotated one seat, and the team that captures more card points wins.

Players: 4 to 4, best with 4

## Parameters

- `deck_size` = 26
- `cards_per_seat` = 6
- `kitty_size` = 2
- `hands` = 4
- `tricks_per_hand` = 6
- `total_rounds` = 24
- `points_five` = 5
- `points_ten` = 10
- `points_king` = 10
- `points_other` = 0
- `points_per_suit` = 25
- `points_in_deck` = 100
- `kitty_multiplier` = 2
- `first_leader_hand_1` = 1
- `first_leader_hand_2` = 2
- `first_leader_hand_3` = 2
- `first_leader_hand_4` = 3
- `rank_big_joker` = 8
- `rank_small_joker` = 7
- `rank_ace` = 6
- `rank_king` = 5
- `rank_queen` = 4
- `rank_jack` = 3
- `rank_ten` = 2
- `rank_five` = 1
- `trump_strength_base` = 200
- `led_suit_strength_base` = 100

## Round

1. **update** (all players): Runs only when trick_number == 1. Clears played_this_hand and kitty_revealed. If hand_number is 1 or 2, the deck is refilled with all 26 cards; each seat then draws 6 cards at random from the deck into its hand, and the 2 cards left move to the kitty. When hand_number == 1, each hand is copied to hand1_cards and the kitty to kitty_hand1. When hand_number == 2, each hand is copied to hand2_cards and the kitty to kitty_hand2. If hand_number == 3, each seat s gets hand = hand1_cards of seat s-1 (seat 1 gets seat 4's), and kitty = kitty_hand1. If hand_number == 4, each seat s gets hand = hand2_cards of seat s-1, and kitty = kitty_hand2. trump_suit is S if hand_number is 1 or 3, otherwise H. leader is 1, 2, 2 or 3 for hands 1 to 4. is_replay = (hand_number >= 3).
2. **tell** (all players): Runs only when trick_number == 1. Announces 'Hand {hand_number} begins. Trump is {trump_suit}. Seat {leader} leads.' When is_replay is true, it adds 'This hand is a replay: each seat holds the cards the previous seat held in hand {hand_number - 2}.'
3. **sync** (all players): Each seat is sent its own hand, plus played_this_hand, team_a_total, team_b_total, trump_suit, trick_number and hand_number.
4. **ask** (each player in turn, starting with the seat in leader and going anticlockwise (leader, leader+1, ... wrapping 4 to 1)): The card is removed from the player's hand and appended to trick_cards and played_this_hand, and played_card is set. For the first player, led_card is set to the card. led_is_trump = (the card is a joker or of trump_suit). led_suit = TRUMP if led_is_trump, otherwise the card's suit.
5. **update** (all players): Each seat gets card_strength = 200 + rank if played_card is a joker or of trump_suit; otherwise 100 + rank if led_is_trump is false and played_card's suit == led_suit; otherwise 0. Ranks are Big Joker 8, Small Joker 7, A 6, K 5, Q 4, J 3, 10 2, 5 1. trick_winner = the seat with the highest card_strength. trick_points = the sum of the points of the 4 trick_cards, where 5 = 5, 10 = 10, K = 10 and all others = 0. If trick_winner is 1 or 3, team_a_total += trick_points; otherwise team_b_total += trick_points. Seats 1 and 3 get score = team_a_total, and seats 2 and 4 get score = team_b_total. leader = trick_winner.
6. **tell** (all players): Announces 'Trick {trick_number} of hand {hand_number}: cards {trick_cards}. Seat {trick_winner} wins {trick_points} points. Team A {team_a_total}, Team B {team_b_total}.'
7. **update** (all players): Runs only when trick_number == 6. kitty_revealed = kitty. If trick_winner is 1 or 3, team_a_total += 2 * (points of kitty); otherwise team_b_total += 2 * (points of kitty). Both teams' scores are mirrored to the seats again.
8. **tell** (all players): Runs only when trick_number == 6. Announces 'End of hand {hand_number}. Kitty: {kitty_revealed}, doubled for the team of seat {trick_winner}. Team A {team_a_total}, Team B {team_b_total}.'
9. **update** (all players): trick_cards is cleared, led_card is set to empty, and each played_card is set to empty. trick_number += 1. If trick_number > 6, then trick_number = 1 and hand_number += 1.
10. **check** (all players): The game ends if hand_number > 4. Otherwise it continues with the next round.

## Ending

- ends when: hand_number > 4 (after 24 tricks)
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: Each seat's standing is its team's match total: captured card points plus doubled kitty points. Both partners of the team with the higher total win. If the totals are equal, all four seats tie at the top, which is the draw.

## Choices the source did not make

- 4 players, suggested 4: The designer fixed two partnerships of two. The duplicate replay structure depends on exactly 4 seats rotating, so neither fewer nor more seats work.
- No talk step: The source forbids table talk. Partnership play here rests on inferring a partner's cards from what they play.
- Rank numbers 1 to 8 and strength bases of 100 (led suit) and 200 (trump): These let the trick winner be found by arithmetic as the seat with the highest card_strength.
- The play order starts at the leader: The source says the leader plays first and the others follow anticlockwise. The ask step runs from the seat in leader.
- Saved hand1_cards and hand2_cards are visible to their owner (ally): A player attribute cannot be hidden from its owner, and the owner already saw those cards when they were dealt.
- Strategy at the table: A thoughtful player counts the trumps and points already played, keeps high trumps to capture the 6th trick (worth the doubled kitty), and feeds point cards to tricks the partner is winning.

## Simplifications

- Each team's match total is mirrored onto both partners as score: The ranking is a per-player expression, so both partners carry their team's total.
- A draw is represented as all four seats sharing the top rank: The engine has no separate draw outcome. Tied totals give every seat the same rank_by value.

## Unsupported (needs engine work)

- none
