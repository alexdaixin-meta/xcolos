# Cat in the Sack: Sealed Stages (Revised)

Each round every player secretly adds one card to a shared sack and writes a message. The sack is then auctioned over up to three sealed-bid stages, with one more card revealed at each stage. After 9 rounds the highest cat points + mice wins.

Players: 3 to 5, best with 4

## Parameters

- `cat_value_1` = -8
- `cat_value_2` = -5
- `cat_value_3` = 3
- `cat_value_4` = 5
- `cat_value_5` = 8
- `cat_value_6` = 11
- `cat_value_7` = 15
- `cats_per_hand` = 7
- `rabbit_value` = 0
- `dogs_per_hand` = 2
- `hand_size_dealt` = 10
- `cards_set_aside_per_player` = 1
- `hand_size_kept` = 9
- `starting_mice` = 15
- `starting_cat_points` = 0
- `rounds` = 9
- `message_max_words` = 30
- `max_stages` = 3
- `pass_reward_stage_1` = 2
- `pass_reward_stage_2` = 3
- `pass_reward_stage_3` = 4
- `all_pass_stage_1_reward` = 2
- `stage_3_outbid_bonus` = 5
- `initial_standing_bid` = 0
- `rank_tiebreak_multiplier` = 1000

## Round

1. **poll** (all players): message := the text; nobody sees any message until the messages are shown in step 4
2. **poll** (all players): played_card := the chosen card; the card is removed from hand; nobody sees another player's choice
3. **update** (all players): round_number += 1; sack_owners := seats in seat order beginning with start_seat; sack_cards := each owner's played_card in that order; sack_revealed := []; standing_bid := 0; leader_seat := 0; stage := 1; sack_done := false; sack_winner := 0; sack_value := 0; every in_auction := true; every bid := 0. Announce whose card is in each position.
4. **tell** (all players): broadcast every message labelled by seat: 'Seat {seat} says: {message}'
5. **update** (all players): append sack_cards[1] to sack_revealed and announce it; stage := 1
6. **poll** (all players): bid := the number; if bid < standing_bid + 1 or bid > mice, then bid := 0 (pass)
7. **update** (all players): Announce every bid by seat. If every bid = 0: every player's mice += 2, sack_cards are appended to unopened_pile, sack_winner := 0, sack_done := true. Otherwise: every player with bid = 0 sets in_auction := false and mice += 2; standing_bid := highest bid; leader_seat := the first seat with that bid, in seat order from the seat after start_seat with start_seat last; announce standing_bid, leader_seat and everyone's mice; if exactly one player has in_auction = true, then sack_winner := leader_seat and sack_done := true.
8. **update** (all players): when sack_done = false and count(in_auction) >= 2: stage := 2; append sack_cards[2] to sack_revealed and announce it; bid := 0 for all
9. **poll** (players with in_auction = true, when sack_done = false and stage = 2): bid := the number; if bid < standing_bid + 1 or bid > mice, then bid := 0
10. **update** (all players): when sack_done = false and stage = 2: announce bids. If every in_auction player bid 0: sack_winner := leader_seat (the previous leader, at the current standing_bid, with no reward); every in_auction player other than leader_seat gains mice += 3; sack_done := true. Otherwise: each in_auction player with bid 0 sets in_auction := false and mice += 3; standing_bid := highest bid; leader_seat := the first seat with that bid in the tie order; announce standing_bid, leader_seat and mice; if exactly one in_auction remains, then sack_winner := leader_seat and sack_done := true.
11. **update** (all players): when sack_done = false and count(in_auction) >= 2: stage := 3; append sack_cards[3] to sack_revealed and announce it; bid := 0 for all
12. **poll** (players with in_auction = true, when sack_done = false and stage = 3): bid := the number; if bid < standing_bid + 1 or bid > mice, then bid := 0
13. **update** (all players): when sack_done = false and stage = 3: announce bids. If every in_auction player bid 0: sack_winner := leader_seat; every in_auction player other than leader_seat gains mice += 4; sack_done := true. Otherwise: each in_auction player with bid 0 sets in_auction := false and mice += 4; standing_bid := highest bid; leader_seat := the first seat with that bid in the tie order; announce standing_bid, leader_seat and mice; if exactly one in_auction remains, then sack_winner := leader_seat and sack_done := true.
14. **update** (all players): when sack_done = false: sack_winner := leader_seat; every player with bid >= 1 at stage 3 and seat != leader_seat gains mice += 5; sack_done := true
15. **update** (all players): when sack_winner != 0: reveal all sack_cards (sack_revealed := sack_cards). Dog rule: if large_dog is in the sack and small_dog is not, remove the highest-valued cat; if small_dog is in the sack and large_dog is not, remove the lowest-valued cat; if no cat is present, nothing is removed; if both dogs are present, neither has any effect. sack_value := sum of the values of the cats remaining (rabbit 0; dogs and removed cats count nothing). The sack_winner pays mice -= standing_bid and gains cat_points += sack_value. All sack cards are appended face up to discard_pile with their owners. Announce the result.
16. **update** (all players): if sack_winner != 0, then start_seat := sack_winner; otherwise start_seat := the next seat after start_seat (wrapping from N to 1)
17. **check** (all players): end the game if round_number >= 9; otherwise continue to the next round

## Ending

- ends when: round_number >= 9
- ranked by: `(you.cat_points + you.mice) * 1000 + you.cat_points` (the highest wins; players level at the top share the win)
- decided by: Each player's score is cat points + mice, and the highest score wins. Among tied players, the one with more cat points wins. Players still tied share the win (a draw among them).

## Choices the source did not make

- 3 to 5 players, suggested 4: The designer chose 4, so it is kept. 3 is the least number of players for a sack with three staged reveals and a real auction among rivals. 5 is the most: a sack of 5 cards fills every position, and more seats would leave too many hidden cards and messages to reason about.
- Talk kept as a simultaneous poll shown to everyone: The rules require one simultaneous message per round. Players disagree over who should take the sack, so claims about their own card are worth bluffing and worth doubting.
- Card codes such as cat_15, rabbit, large_dog, small_dog: The cards need text names so the engine can store and compare them in lists.
- Cat values listed as separate parameters cat_value_1 to cat_value_7: Each parameter must be a single number.
- Tie-break encoded as (cat_points + mice) * 1000 + cat_points: The ranking must be one expression. Cat points can never exceed 210 in absolute value, so a one-point score difference always outweighs the cat-points term.
- Unopened sacks go to a hidden unopened_pile: The rules say such a sack is discarded without being opened, so its unrevealed cards must stay unseen.

## Simplifications

- The message and the card choice are two consecutive polls instead of one combined answer: A poll gathers one answer. Neither answer is shown until both polls are complete, so they stay simultaneous in effect.
- Bids are offered as any number from 0 to the bidder's mice, with numbers at or below the standing bid treated as a pass: This matches the rule that an illegal number counts as a pass, while keeping the offered range simple.
- 'Go to step 7/9' is done with when-conditions on sack_done and sack_winner: The step list is flat. Skipping single steps by condition gives the same flow.

## Unsupported (needs engine work)

- none
