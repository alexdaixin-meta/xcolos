# Nyet! Contract Veto

Three players play 6 deals of 5 tricks: in each deal the Pair veto trump colours, the Lone names trump, the first leader and an exact trick bid, and every trick scores 1 point for whoever wins it.

Players: 3 to 3, best with 3

## Parameters

- `player_count` = 3
- `deck_size` = 20
- `colour_count` = 4
- `rank_min` = 1
- `rank_max` = 5
- `hand_size` = 5
- `widow_size` = 5
- `deals` = 6
- `rounds_per_deal` = 6
- `tricks_per_deal` = 5
- `total_rounds` = 36
- `bans_per_pair_member` = 1
- `unbanned_if_same_ban` = 3
- `unbanned_if_different_bans` = 2
- `bid_min` = 0
- `bid_max` = 5
- `trick_point` = 1
- `exact_bid_lone_gain` = 6
- `off_by_one_lone_gain` = 2
- `off_by_one_pair_gain` = 1
- `off_by_two_or_more_pair_gain` = 3
- `off_by_one_difference` = 1
- `off_by_two_threshold` = 2
- `trump_strength_offset` = 10

## Round

1. **update** (all players): When round_in_deal == 1 (setup round): every card in widow and in any hand is returned to deck. lone_seat = ((deal - 1) mod 3) + 1. is_lone is set true for the seat equal to lone_seat and false for the others. Each player's ban is set to empty, unbanned is reset to all four colours, trump to empty, bid to 0 and lone_tricks to 0. The Lone and the Pair are announced to everyone.
2. **update** (all players): When round_in_deal == 1: shuffle by drawing at random. Each player gets 5 random cards, each moved from deck into that player's hand. The remaining 5 cards of deck are moved into widow, which stays hidden from everyone.
3. **sync** (all players): When round_in_deal == 1: each player is sent their own hand, plus lone_seat and the scores.
4. **poll** (all players): When round_in_deal == 1: all three write at the same time, and the messages are then broadcast {"to": "all", "text": "Seat {seat} says: {value}"}. No state changes and nothing is binding.
5. **poll** (each player with is_lone == false): When round_in_deal == 1: each Pair member's ban is set to the chosen colour, chosen at the same time. Both banned colours are removed from unbanned, leaving 3 colours if the two bans match and 2 if they differ. Both bans and unbanned are announced.
6. **ask** (the seat with is_lone == true): When round_in_deal == 1: trump, leader and bid are set from the choice and announced.
7. **update** (all players): When round_in_deal >= 2 (trick round): each played_card is set to empty, each card_strength to 0, and led_colour to empty.
8. **ask** (each player in turn, clockwise starting at leader): When round_in_deal >= 2: the card is removed from that player's hand and set as their played_card, shown face up. For the leader, led_colour is set to the card's colour. Each player hears the earlier plays.
9. **update** (all players): When round_in_deal >= 2: card_strength = 10 + number if the card's colour == trump; = number if its colour == led_colour and is not trump; otherwise 0. trick_winner is the seat with the highest card_strength. That seat's score += 1. If trick_winner == lone_seat, lone_tricks += 1. leader = trick_winner. The winner, all scores and lone_tricks are announced.
10. **update** (all players): When round_in_deal == 6 (after the 5th trick), with T = lone_tricks and B = bid: if |T - B| == 0, the Lone's score += 6; if |T - B| == 1, the Lone's score += 2 and each Pair member's score += 1; if |T - B| >= 2, each Pair member's score += 3. The result is announced.
11. **update** (all players): round_number += 1. If round_in_deal == 6, then deal += 1 and round_in_deal = 1; otherwise round_in_deal += 1.
12. **check** (all players): The game ends if deal > 6 (all 36 rounds played); otherwise it continues.

## Ending

- ends when: deal > 6
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their total score after 6 deals (36 rounds). The highest total wins, and players level at the top share the result.

## Choices the source did not make

- Exactly 3 players (min 3, max 3, suggested 3): The designer fixed 3. The rules depend on 3 seats: a 1-versus-2 Lone/Pair split, 5 cards each plus a 5-card widow from 20 cards, and a fixed clockwise order. Any other count breaks the deal and the rotation. Strategy: the Lone bids a count they can hit exactly, using trump and the first leader to steer. The Pair try to push the Lone 2 or more tricks off the bid, either by taking tricks or by feeding the Lone extra ones, while still collecting 1 point per trick.
- Talk kept as one simultaneous poll broadcast to all: The source requires it. It earns its place because the Pair benefit from coordinating vetoes (matching bans leave 3 colours, different bans leave 2), while the Lone can mislead and each Pair member is also a rival for the overall win.
- The contract is offered as one combined choice list: The rules call it one decision of three parts. Listing every valid trump, leader and bid combination keeps it to one choice and enforces that trump is unbanned.
- Cards are written as colour letter plus number (R1..Y5), and trick strength is computed as 10 plus number for trump, number for the led colour, 0 otherwise: This lets the trick winner be found by arithmetic. Every card is distinct, so no ties are possible, matching the rules.
- Each widow is never revealed, not even at the end: The widow is redealt every deal and plays no role in scoring. The rules only say it is unseen during play, so it stays hidden.

## Simplifications

- A tie for the highest total is shared as a win rather than declared a draw: The engine ranks by one expression and players level at the top share the win. This is the engine's form of the source's draw.
- Setup-round and trick-round steps live in one flat round, each gated by a when-condition on round_in_deal: The engine repeats one step list. Per-step arithmetic conditions select the setup or trick steps without choosing whole blocks.

## Unsupported (needs engine work)

- none
