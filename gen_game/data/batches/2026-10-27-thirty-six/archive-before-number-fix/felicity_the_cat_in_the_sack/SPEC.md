# Cat in the Sack: Two Peeks

Each round every player secretly adds a card to a sack. Players bid mice in up to two sealed stages, seeing one card before each stage. The winner pays and scores the cats inside, and dogs may remove the best or worst cat. Most cat points plus mice after 9 rounds wins.

Players: 3 to 5, best with 4

## Parameters

- `starting_mice` = 15
- `stage1_pass_bonus` = 2
- `stage2_pass_bonus` = 3
- `rounds` = 9
- `hand_size_dealt` = 10
- `set_aside_per_player` = 1
- `hand_size_after_setup` = 9
- `cat_neg8_value` = -8
- `cat_neg5_value` = -5
- `cat_3_value` = 3
- `cat_5_value` = 5
- `cat_8_value` = 8
- `cat_11_value` = 11
- `cat_15_value` = 15
- `rabbit_value` = 0
- `large_dog_value` = 0
- `small_dog_value` = 0
- `first_peek_index` = 1
- `second_peek_index` = 2
- `min_bid_to_count` = 1
- `rank_score_multiplier` = 1000

## Round

1. **update** (all players): round_number += 1. For every player: bid = 0, in_auction = true, played_card = ''. For the table: standing_bid = 0, leader_seat = 0, bidder_count = 0, sack_winner = 0, sack_value = 0, sack_revealed = [], sack_owners = [], sack_cards = [].
2. **poll** (all players): The chosen card is removed from hand and stored in played_card.
3. **update** (all players): sack_owners = the seats in ascending order starting at start_seat and wrapping after the last seat to seat 1 (for example, start_seat 3 of 4 gives [3,4,1,2]). sack_cards = each owner's played_card in the same order.
4. **update** (all players): First peek: sack_cards[1] (the start seat's card) is appended to sack_revealed and broadcast to all.
5. **poll** (all players): Stored in bid, then made public.
6. **update** (all players): bidder_count = the number of players with bid > 0. standing_bid = the maximum bid. leader_seat = the seat with the maximum bid; ties go to the seat earliest in sack_owners. Every player with bid = 0 gets in_auction = false. If bidder_count >= 1, every player with bid = 0 also gets mice += stage1_pass_bonus (2).
7. **update** (all players): This step runs when bidder_count = 0. sack_cards = []. start_seat = (start_seat mod player_count) + 1. Nobody gains anything, and no later step that needs bidders runs.
8. **update** (all players): This step runs when bidder_count = 1. sack_winner = leader_seat, and the price stays at standing_bid. There is no stage 2.
9. **update** (all players): This step runs when bidder_count >= 2. Second peek: sack_cards[2] is appended to sack_revealed and broadcast to all.
10. **poll** (every player with in_auction = true, when bidder_count >= 2): The answer replaces bid, which is then made public.
11. **update** (all players): This step runs when bidder_count >= 2. If any in-auction player has bid > 0: sack_winner = the in-auction seat with the highest bid (ties go to the seat earliest in sack_owners) and standing_bid = that bid. Otherwise sack_winner = leader_seat and standing_bid is unchanged. Then every in-auction player with bid = 0 who is not sack_winner gets mice += stage2_pass_bonus (3).
12. **update** (all players): This step runs when sack_winner > 0. The sack_winner's mice -= standing_bid. Dog rule: if exactly one of large_dog or small_dog is in sack_cards and at least one cat is there, then large_dog removes one cat with the highest value, or small_dog removes one cat with the lowest value. With 0 or 2 dogs, or no cats, nothing is removed. sack_value = the sum of the values of the remaining cat cards (rabbit and dogs count 0). The sack_winner's cat_points += sack_value. All sack_cards are broadcast to everyone, then sack_cards = [].
13. **update** (all players): This step runs when sack_winner > 0. start_seat = sack_winner.
14. **update** (all players): For every player: score = cat_points + mice. Mice, cat_points and score are announced.
15. **check** (all players): End the game if round_number >= 9. Otherwise continue to the next round.

## Ending

- ends when: round_number >= 9
- ranked by: `(you.cat_points + you.mice) * 1000 + you.cat_points` (the highest wins; players level at the top share the win)
- decided by: The highest cat_points + mice wins. Ties are broken by higher cat_points. Players still tied share the win, which is a draw among them.

## Choices the source did not make

- 3 to 5 players, suggested 4: The designer suggested 4, and the source allows 3 to 5. 3 is the minimum because the auction needs rivals and the pass bonuses only matter with several bidders. Above 5 the sack has too many unseen cards, so the peeks tell too little.
- No talk step added: The source has no talk phase, and adding one would add a mechanic. The strategy lies in reading the peeks and others' public bids, and in choosing between passing for the bonus and paying.
- When a dog removes a cat and several cats share the highest or lowest value, only one of them is removed: The source says 'the cat', which means a single card.
- The tie-break is folded into rank_by as score*1000 + cat_points: cat_points stays within -65 to 210, so a 1-point score difference always outweighs it.
- score is kept as an attribute and updated every round: This makes the final score observable. It equals cat_points + mice after round 9, as the rules state.

## Simplifications

- The stage-2 range has a gap (0, or standing_bid+1 to mice). It is offered as a number with validation rejecting 1 to standing_bid. If the engine can only express a contiguous range, any value from 1 to standing_bid is treated as 0 (a pass).: Engine number questions take a single range.
- Stages and branches (no bidders, sole bidder, two or more bidders) are built as a flat step list with arithmetic 'when' conditions on single steps.: The engine runs a flat step list, and each branch here is one condition per step.

## Unsupported (needs engine work)

- none
