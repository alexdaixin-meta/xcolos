# Hanamikoji: Compact Build

Two players spend four one-use actions each hand to place Item cards for seven Geisha. They win a Geisha's favour by placing more of her Items, and the first to 11 Charm or 4 Geisha at a hand's end wins.

Players: 2 to 2, best with 2

## Parameters

- `charm_g1` = 2
- `charm_g2` = 2
- `charm_g3` = 2
- `charm_g4` = 3
- `charm_g5` = 3
- `charm_g6` = 4
- `charm_g7` = 5
- `total_charm` = 21
- `total_items` = 21
- `items_per_geisha_equals_charm` = 1
- `geisha_count` = 7
- `max_hands` = 4
- `turns_per_hand` = 8
- `cards_removed_per_hand` = 1
- `starting_hand_size` = 6
- `deck_size_after_deal` = 8
- `cards_drawn_per_turn` = 1
- `secret_cards` = 1
- `tradeoff_cards` = 2
- `gift_cards` = 3
- `competition_cards` = 4
- `gift_cards_to_opponent` = 1
- `competition_cards_per_pair` = 2
- `charm_to_win` = 11
- `geisha_to_win` = 4

## Round

1. **update** (all players): When turn_number = 1: deck is set to the 21 Items (G1 x2, G2 x2, G3 x2, G4 x3, G5 x3, G6 x4, G7 x5) and pile to []. Every hand, secret and offer is emptied, every counts becomes [0,0,0,0,0,0,0], and every actions becomes [Secret, Trade-off, Gift, Competition]. Then, drawing at random from deck (the shuffle): 1 card is appended to pile; 6 cards, one at a time, to the hand of the first player (seat 1 + ((hand_number + 1) mod 2)); 6 cards to the other seat's hand. The remaining 8 stay in deck in the order drawn. markers, charm and geisha are not reset.
2. **update** (all players): active_seat = 1 + ((hand_number + turn_number) mod 2).
3. **update** (the active seat): The first card of deck is removed from deck and appended to the end of the active seat's hand.
4. **sync** (all players): Each player sees markers, both counts, both actions, both charm and geisha, hand_number and turn_number, plus their own hand and own secret.
5. **ask** (the active seat): chosen_action = the answer. An invalid answer becomes the first unused action in the order Secret, Trade-off, Gift, Competition.
6. **ask** (the active seat): That card is removed from hand (one copy) and appended to offer. An invalid answer becomes the first card of hand.
7. **ask** (the active seat): When chosen_action is not Secret: that card is removed from hand and appended to offer. An invalid answer becomes the first card of hand.
8. **ask** (the active seat): When chosen_action is Gift or Competition: that card is removed from hand and appended to offer. An invalid answer becomes the first card of hand.
9. **ask** (the active seat): When chosen_action is Competition: that card is removed from hand and appended to offer. An invalid answer becomes the first card of hand.
10. **update** (the active seat): When chosen_action is Secret: the offer card moves to the active seat's secret. When chosen_action is Trade-off: both offer cards are appended to pile. In both cases offer is emptied.
11. **tell** (all players): When chosen_action is Gift or Competition: the offer is revealed to both players, in order. For Competition it is shown as Pair 1 = cards 1-2 and Pair 2 = cards 3-4.
12. **ask** (the seat that is not active (3 - active_seat)): When chosen_action is Gift: pick = the answer. An invalid answer becomes card 1.
13. **ask** (the seat that is not active (3 - active_seat)): When chosen_action is Competition: pick = the answer. An invalid answer becomes Pair 1.
14. **update** (all players): When chosen_action is Gift: the picked offer card adds 1 to the opponent's counts at its Geisha, and each of the other two offer cards adds 1 to the active seat's counts at its Geisha. Announce the placement publicly.
15. **update** (all players): When chosen_action is Competition: each card of the picked pair adds 1 to the opponent's counts at its Geisha, and each card of the other pair adds 1 to the active seat's counts at its Geisha. Announce the placement publicly.
16. **update** (all players): chosen_action is removed from the active seat's actions. offer, chosen_action and pick are cleared. turn_number goes up by 1.
17. **update** (all players): When turn_number = 9: each player's secret is revealed to all and adds 1 to that player's counts at its Geisha, then every secret is emptied.
18. **update** (all players): When turn_number = 9: for each Geisha i from 1 to 7, markers[i] = 'A' if seat 1 counts[i] > seat 2 counts[i]; 'B' if seat 2 counts[i] > seat 1 counts[i]; otherwise unchanged. Then seat 1 charm = sum of charm_values[i] over markers 'A' and seat 1 geisha = number of 'A'; seat 2 charm = sum over markers 'B' and seat 2 geisha = number of 'B'.
19. **tell** (all players): When turn_number = 9: announce markers and both players' charm and geisha.
20. **check** (all players): When turn_number = 9: end the game if any player's charm >= 11, or any player's geisha >= 4, or hand_number = 4. Otherwise continue.
21. **update** (all players): When turn_number = 9: hand_number goes up by 1 and turn_number = 1. The next hand's first player is then the other seat, by the active_seat formula.

## Ending

- ends when: turn_number = 9 and (max over players of charm >= 11 or max over players of geisha >= 4 or hand_number = 4)
- ranked by: `you.charm * 10 + you.geisha` (the highest wins; players level at the top share the win)
- decided by: Charm held, then Geisha held. A player with 11+ Charm always has the higher Charm (the total is 21). A player with 4+ Geisha always has at least equal Charm and more Geisha whenever neither player has 11 Charm. So this one ranking reproduces the 11-Charm win, the 4-Geisha win and the hand-4 tie-break. Equal Charm and equal Geisha is a draw, a shared win.

## Choices the source did not make

- Exactly 2 players, suggested 2: The designer's size is kept. The game is a two-sided split-and-choose duel: every Gift and Competition is offered by one player to the single opponent, and each marker is won by comparing two counts.
- Seat 1 is Player A and seat 2 is Player B: The source names the players A and B; markers 'A' and 'B' refer to seats 1 and 2.
- No talk step: The source has no talk. In a two-player zero-sum duel, talk would only add words, and bluffing already lives in the offers.
- Strategy at the table: A thoughtful player builds Gift and Competition offers so that either answer suits them, saves Secret and Trade-off to hide or deny key Geisha, and tracks the 21-card composition and the spent actions to infer the opponent's hand.
- rank_by = charm * 10 + geisha: Geisha never exceeds 7, so charm decides first and geisha breaks ties. The 11-Charm and 4-Geisha wins always coincide with the top of this ranking, as explained under decided_by.

## Simplifications

- The single choice 'name an action and its cards' is split into one action question plus 1 to 4 card questions, each chosen from the current hand list: Choices from a game list make a held card automatic and count duplicates correctly. The source fallback is kept for invalid answers, though it is rarely reached.
- standing is stored as each player's charm and geisha attributes instead of one 4-number table list: Ranking is an expression over you.<attribute>; the values are identical to standing [A charm, B charm, A geisha, B geisha].
- hand_A/hand_B, secret_A/secret_B, counts_A/counts_B and actions_A/actions_B become per-player attributes hand, secret, counts and actions: Per-player attributes with ally or public visibility give each player the same view as the source.
- Turn-1-only and after-turn-8-only steps are ordinary steps carrying a 'when' condition, and the after-turn-8 steps test turn_number = 9 after the increment: The step list is flat; single conditioned steps express it without block branching.
- The multi-step winner check is folded into one end condition plus the ranking: The engine ends on an arithmetic condition and ranks by one expression; the outcomes are unchanged.

## Unsupported (needs engine work)

- none
