# Gracias: The Counted Gift

Four players draft face-up/face-down card triplets over 3 sessions of 4 rounds. In each pick a player keeps one face-up card, gifts the other to an opponent and secretly takes the hidden card. Sets of 4 in a colour score 3 points, and the largest leftover pile in each colour is discarded.

Players: 4 to 4, best with 4

## Parameters

- `players` = 4
- `colours` = 4
- `cards_per_colour` = 12
- `deck_size` = 48
- `sessions` = 3
- `rounds_per_session` = 4
- `total_rounds` = 12
- `triplets_per_round` = 4
- `cards_per_triplet` = 3
- `cards_laid_out_per_round` = 12
- `shuffle_rounds_first` = 1
- `shuffle_rounds_second` = 5
- `shuffle_rounds_third` = 9
- `stack_size` = 4
- `points_per_stack` = 3
- `points_per_loose_card` = 1
- `min_loose_for_discard` = 1
- `count_increment` = 1
- `rank_tiebreak_multiplier` = 1000

## Round

1. **update** (table): When round mod 4 == 1 (rounds 1, 5, 9): set deck to 48 cards, 12 each of Red, Blue, Green and Yellow (shuffle). No other round refills or shuffles the deck.
2. **update** (table): Lay out: draw 12 cards at random from deck, removing each one from deck, into t1_a, t1_b, t1_h, t2_a, t2_b, t2_h, t3_a, t3_b, t3_h, t4_a, t4_b, t4_h. Set open_triplets = [T1, T2, T3, T4].
3. **tell** (all players): Announce the A and B colours of T1-T4 (t1_a, t1_b, ..., t4_a, t4_b). The H cards stay secret.
4. **ask** (each player in turn, starting at seat ((round-1) mod 4)+1 and going up in seat order, wrapping from 4 to 1): The picker's pub_<kept colour> += 1. The chosen receiver's pub_<gifted colour> += 1. The triplet's H colour is told privately to the picker only, and the picker's hid_<H colour> += 1. The triplet is removed from open_triplets. The keep and the gift (not H) are announced to all at once.
5. **tell** (all players): Announce every player's pub_red, pub_blue, pub_green and pub_yellow.
6. **tell** (all players): When round mod 4 == 0: reveal every player's hid_red, hid_blue, hid_green and hid_yellow to everyone.
7. **update** (all players): When round mod 4 == 0: for each player and colour c, totals[c] = pub_c + hid_c, stacks[c] = floor(totals[c] / 4), loose[c] = totals[c] - 4*stacks[c].
8. **update** (table): When round mod 4 == 0: for each colour c, max_loose[c] = the maximum of loose[c] over the 4 players.
9. **update** (all players): When round mod 4 == 0: session_score = sum over the 4 colours of (3*stacks[c] + (loose[c] if NOT (max_loose[c] >= 1 and loose[c] == max_loose[c]) else 0)). Then game_total += session_score, and if session_score > best_session_score, best_session_score = session_score. Announce session_score, game_total and best_session_score.
10. **update** (all players): When round mod 4 == 0: set every pub_* and hid_* to 0, and session += 1.
11. **update** (table): round += 1.
12. **check** (table): End the game if round > 12; otherwise start the next round.

## Ending

- ends when: round > 12
- ranked by: `you.game_total * 1000 + you.best_session_score` (the highest wins; players level at the top share the win)
- decided by: Highest game_total wins. Among players tied on it, the highest best_session_score wins. Players still tied share the win, which is the source's draw.

## Choices the source did not make

- Exactly 4 players (min = max = suggested = 4): The designer fixed 4. The 4 triplets per round, 12 cards per colour and the rotating first pick are all sized to 4 seats. The game is about counting cards and gifting tactically against several rivals, and it needs 3 opponents to choose among as gift targets.
- No talk step: The source has no communication phase. Adding one would add a mechanic.
- The whole pick (triplet, which card to keep, receiver) is asked as one choice from a generated list: The source resolves the pick as a single action. One question keeps it atomic and offers only legal combinations.
- rank_by multiplier 1000: best_session_score is far below 1000, so game_total always dominates and the best session only breaks ties.
- totals, stacks, loose and max_loose kept as 4-element lists in the order Red, Blue, Green, Yellow: The rules name these values, so they are declared, and lists keep the attribute count manageable.
- Strategy at the table: A thoughtful player counts the unseen cards to estimate opponents' hidden colours, completes stacks of 4, and gifts cards that push a rival into a majority-loose discard or past a stack boundary that breaks their leftovers.

## Simplifications

- Shuffling and dealing from the top is modelled as drawing 12 cards at random without replacement from the deck list each round, with the deck refilled only at rounds 1, 5 and 9: This has the same distribution as one shuffle per session followed by top-card dealing, and it is the engine's way to draw.
- The session-end reveal is a broadcast of hidden counts rather than a change in visibility: Attribute visibility is fixed. Announcing the values gives everyone the same information.

## Unsupported (needs engine work)

- none
