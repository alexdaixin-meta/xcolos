# Nyet! Trio (Widow edition, compact)

Three players veto trump and choose who goes Lone, then play 5 tricks per deal over 6 deals. The Lone takes the face-up Widow and scores 2 per trick won; the other two, the Pair, each score 1 per trick their side wins.

Players: 3 to 3, best with 3

## Parameters

- `players` = 3
- `colours` = 4
- `ranks_per_colour` = 6
- `deck_size` = 24
- `hand_size` = 5
- `widow_cards` = 1
- `set_aside_cards` = 8
- `lone_hand_size` = 6
- `total_rounds` = 36
- `deals` = 6
- `rounds_per_deal` = 6
- `veto_rounds_per_deal` = 1
- `tricks_per_deal` = 5
- `trump_boxes` = 4
- `lone_boxes` = 3
- `tokens_per_deal` = 3
- `max_lone_tokens_per_deal` = 1
- `lone_trick_points` = 2
- `lone_trick_count_gain` = 1
- `pair_trick_points_each` = 1
- `lone_cards_kept_back` = 1
- `trump_strength_bonus` = 200
- `led_strength_bonus` = 100
- `rank_weight_score` = 10000
- `rank_weight_lone_tricks` = 100

## Round

1. **update** (all players): round += 1; deal = floor((round - 1) / 6) + 1; round_in_deal = ((round - 1) mod 6) + 1
2. **update** (all players): when round_in_deal == 1: empty every hand (cards are discarded unseen); deck = all 24 cards; draw 5 cards at random from deck into each player's hand; draw 1 card at random from deck into widow (the remaining 8 stay in deck, hidden, as the set-aside cards); clear trump_tokens and lone_tokens; set trump_order (deals 1 and 5: Red, Yellow, Green, Blue; deals 2 and 6: Yellow, Green, Blue, Red; deal 3: Green, Blue, Red, Yellow; deal 4: Blue, Red, Yellow, Green); set veto_order (deals 1 and 4: 1, 2, 3; deals 2 and 5: 2, 3, 1; deals 3 and 6: 3, 1, 2); clear trump, lone_seat and roles
3. **sync** (all players): when round_in_deal == 1: each player sees their own 5-card hand
4. **tell** (all players): when round_in_deal == 1: announce deal, widow, trump_order (the TRUMP line), the LONE line boxes First/Second/Third with their seats from veto_order, and that the board is empty
5. **poll** (all players): when round_in_deal == 1: all messages are collected at once and then broadcast {"to": "all", "text": "Seat {seat} says: {value}"}
6. **ask** (seat veto_order[1] (First)): when round_in_deal == 1: append the chosen colour to trump_tokens, or the chosen lone box to lone_tokens; announce the placement
7. **ask** (seat veto_order[2] (Second)): when round_in_deal == 1: append to trump_tokens or lone_tokens; announce the placement
8. **ask** (seat veto_order[3] (Third)): when round_in_deal == 1: append to trump_tokens or lone_tokens; announce the placement
9. **update** (all players): when round_in_deal == 1: trump = first colour in trump_order not in trump_tokens; lone_seat = the veto_order seat at the first of the First, Second, Third positions not in lone_tokens; role = 'lone' for lone_seat and 'pair' for the other two; append widow to the Lone's hand (6 cards); leader = lone_seat
10. **tell** (all players): when round_in_deal == 1: announce trump, the Lone (lone_seat) and the Pair seats, and that the Lone leads the first trick
11. **sync** (all players): when round_in_deal == 1: each player sees their own hand (the Lone now sees 6 cards)
12. **ask** (seat leader): when round_in_deal >= 2: remove the card from hand; set played_colour and played_rank; led_colour = played_colour; announce the card
13. **ask** (seat clockwise after leader): when round_in_deal >= 2: remove the card from hand; set played_colour and played_rank; announce the card
14. **ask** (seat two clockwise after leader): when round_in_deal >= 2: remove the card from hand; set played_colour and played_rank; announce the card
15. **update** (all players): when round_in_deal >= 2: for each player, strength = (played_colour == trump) * 200 + (played_colour == led_colour) * 100 + played_rank; trick_winner = the seat with the highest strength; if trick_winner == lone_seat then that player's score += 2 and lone_tricks += 1, otherwise each player with role 'pair' gets score += 1; trick_winner's last_win = round; leader = trick_winner
16. **tell** (all players): when round_in_deal >= 2: announce the three cards played, trick_winner, and every score, lone_tricks and last_win
17. **sync** (all players): when round_in_deal >= 2: each player sees their own remaining hand
18. **check** (all players): end the game if round >= 36, otherwise continue

## Ending

- ends when: round >= 36
- ranked by: `you.score * 10000 + you.lone_tricks * 100 + you.last_win` (the highest wins; players level at the top share the win)
- decided by: The highest score wins. A tie goes to the tied player with the most lone_tricks, then to the one with the highest last_win (who won a trick most recently). Players still level share the win, which is the draw.

## Choices the source did not make

- 3 players (min 3, max 3, suggested 3): The designer fixed 3 seats. The game is one Lone against a Pair of two, and both the veto order and the LONE line have exactly 3 positions, so no other count works. The strategy is to veto colours and Lone positions to steer trump toward your own hand, and to judge whether to go Lone or force someone else into it.
- Talk is kept as a simultaneous poll with broadcast: The rules say all three write at once without seeing each other. The players disagree about trump and about who should be Lone, so talk gives them something to bluff and bargain over.
- Cards are text such as 'Red 3', handled through played_colour and played_rank: This lets the trick winner be found by arithmetic: strength = trump bonus 200 + led bonus 100 + rank.
- strength is a public scratch attribute: It is computed only from cards already played face up, so making it public reveals nothing; a player attribute may not be hidden from all.
- The 8 set-aside cards stay in the hidden deck list: They are never revealed or used, so the hidden deck can hold them.
- Tie-break encoded as score*10000 + lone_tricks*100 + last_win: lone_tricks is at most 30 and last_win at most 36, both under 100, so the order is strictly lexicographic. A full tie shares the win, which is the source's draw.

## Simplifications

- Veto-round and trick-round steps are one flat list, each step gated by a 'when' condition on round_in_deal: The engine has no branching blocks. Per-step conditions reproduce the alternation exactly.
- The 'Lone leads first' and 'winner leads next' rules are kept as a leader table attribute, and play order is addressed relative to the leader: The engine addresses seats by attribute rather than by a fixed rotation.

## Unsupported (needs engine work)

- none
