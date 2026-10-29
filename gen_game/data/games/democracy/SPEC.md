# Democracy: Three Tribes

Three players play simultaneous trick-taking over 4 deals of 6 tricks. Each trick's prize card sets trump, and a player who captures 11 or more points in a suit during a deal wins that suit's tribe.

Players: 3 to 3, best with 3

## Parameters

- `players` = 3
- `deck_size` = 24
- `suits` = 3
- `cards_per_suit` = 8
- `suit_points_total` = 20
- `deals` = 4
- `tricks_per_deal` = 6
- `total_tricks` = 24
- `hand_size` = 6
- `pool_size` = 6
- `tribe_threshold` = 11
- `tribe_award` = 1
- `points_five` = 5
- `points_four` = 4
- `points_three` = 3
- `points_ace` = 3
- `points_king` = 2
- `points_queen` = 2
- `points_jack` = 1
- `points_six` = 0
- `rank_five` = 8
- `rank_four` = 7
- `rank_three` = 6
- `rank_ace` = 5
- `rank_king` = 4
- `rank_queen` = 3
- `rank_jack` = 2
- `rank_six` = 1
- `trump_bonus` = 100
- `six_beats_five_strength` = 200
- `rank_weight_tribes` = 1000

## Round

1. **update** (all players): When trick % 6 == 0 (start of a deal): deal += 1; deck = all 24 cards; draw 6 random cards from deck into each player's hand (removing them from deck); draw the remaining 6 at random into pool, in order; set tally_hearts, tally_spades and tally_diamonds to 0 for every player; revealed = [].
2. **sync** (all players): When trick % 6 == 0: each player is sent their own hand and the public state.
3. **update** (all players): trick += 1; prize = first card of pool, removed from pool; trump = suit of prize; append prize to revealed; trick_winner = 0.
4. **tell** (all players): Announce: 'Deal {deal}, trick {trick}: the voting card is {prize}; trump is {trump}.'
5. **poll** (all players): Every player writes one message at the same time. All are then broadcast: {"to": "all", "text": "Seat {seat} says: {value}"}. Nothing said is binding.
6. **poll** (all players): Simultaneously, each player's chosen card becomes played_card and is removed from hand.
7. **update** (all players): Append all three played_card values to revealed. Each player's strength = the card's rank number (5=8, 4=7, 3=6, A=5, K=4, Q=3, J=2, 6=1), plus 100 if its suit == trump; if the played card is the 6 of trump and some player played the 5 of trump, strength = 200. If exactly one player holds the maximum strength, trick_winner = that seat; otherwise trick_winner = 0.
8. **update** (all players): If trick_winner > 0: for each of the 3 played cards and the prize, add the card's points (5=5, 4=4, 3=3, A=3, K=2, Q=2, J=1, 6=0) to the winner's tally for that card's suit (tally_hearts, tally_spades or tally_diamonds). If trick_winner == 0: each player adds their own played_card's points to their own tally for its suit, and the prize scores for no one.
9. **tell** (all players): Announce the played cards, trick_winner (0 means nobody), and every player's tally_hearts, tally_spades and tally_diamonds.
10. **update** (all players): When trick % 6 == 0 (end of a deal): for each suit, the player with that suit's tally >= 11 adds 1 to tribes. A suit with no player at 11 or more awards nothing.
11. **tell** (all players): When trick % 6 == 0: announce every player's tribes.
12. **check** (all players): If trick == 24, end the game; otherwise run the round again.

## Ending

- ends when: game.trick == 24
- ranked by: `you.tribes * 1000 + you.tally_hearts + you.tally_spades + you.tally_diamonds` (the highest wins; players level at the top share the win)
- decided by: Most tribes after 4 deals wins. A tie on tribes is broken by the highest sum of the three suit tallies in the 4th deal. Players still tied share the win (a draw among them).

## Choices the source did not make

- 3 players, fixed: The designer set 3. The game needs exactly three tribes contested by three players, and the 24-card deck splits exactly into three hands of 6 plus a pool of 6. Fewer or more seats would break the deal.
- Talk kept as a simultaneous poll broadcast to all: The rules say messages are written at the same moment and then shown. Talk matters because players compete for suits and can propose non-binding splits ("you take Hearts, I take Spades") that may be betrayed.
- Card encoding as rank+suit text (e.g. '5H', 'AS'): This gives the hand, pool and revealed lists a concrete, checkable form.
- Trick resolution by a strength number (rank 1 to 8, +100 for trump, 200 for the 6 of trump when the 5 of trump is played) with a unique maximum required: This makes the winner arithmetic. Trump ties cannot occur within one suit, so a tie at the top only happens with no trump played, which is the no-winner case.
- Tie-break folded into rank_by as tribes*1000 + the three tallies: Tallies are reset each deal, so at the end they are the 4th-deal tallies. A sum of at most 60 never overtakes a tribe.
- Draw expressed as a shared win: The engine has no separate draw: players level at the top share the win.

## Simplifications

- Deal-start and deal-end steps run inside the round with a `when trick % 6 == 0` condition: The engine repeats a single flat round. These steps are single conditional steps, not a separate block.
- Each deal restores all 24 cards to the deck before dealing: This models 'shuffle all 24 cards'. Drawing at random is the shuffle.

## Unsupported (needs engine work)

- none
