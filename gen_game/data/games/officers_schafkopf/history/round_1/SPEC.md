# Officers' Schafkopf: Bidding Match

A two-player Schafkopf match of 4 hands with a 16-card deck, open and face-down stacks, sealed bids for the declarer's contract, an optional Stoß, and 8 tricks per hand. Match points decide the winner, total card points break ties.

Players: 2 to 2, best with 2

## Parameters

- `deck_size` = 16
- `points_ace` = 11
- `points_ten` = 10
- `points_ober` = 3
- `points_unter` = 2
- `deck_points` = 104
- `hands_in_match` = 4
- `tricks_per_hand` = 8
- `rounds_per_hand` = 9
- `total_rounds` = 36
- `private_cards_per_player` = 4
- `stacks_per_player` = 2
- `face_up_cards_on_table` = 4
- `bid_pass` = 0
- `bid_low` = 53
- `bid_mid` = 66
- `bid_high` = 79
- `default_bid_when_both_pass` = 53
- `base_for_53` = 2
- `base_for_66` = 3
- `base_for_79` = 4
- `all_tricks_bonus` = 1
- `multiplier_stoss` = 2
- `multiplier_no_stoss` = 1
- `trump_strength_ober_acorns` = 20
- `trump_strength_ober_leaves` = 19
- `trump_strength_ober_hearts` = 18
- `trump_strength_ober_bells` = 17
- `trump_strength_unter_acorns` = 16
- `trump_strength_unter_leaves` = 15
- `trump_strength_unter_hearts` = 14
- `trump_strength_unter_bells` = 13
- `trump_strength_solo_suit_ace` = 12
- `trump_strength_solo_suit_ten` = 11
- `plain_rank_ace` = 3
- `plain_rank_ten` = 2
- `plain_rank_ober` = 1
- `plain_rank_unter` = 0
- `rank_weight_match_points` = 1000

## Round

1. **update** (all players): When round_in_hand == 0 (the deal):
- Set dealer = 1 if hand_number is odd, else 2, and set forehand to the other seat.
- Refill deck with all 16 cards.
- For each seat, draw 4 random cards from deck into hand, then 1 into stack1_up, 1 into the seat's stack1_down table attribute, 1 into stack2_up, and 1 into the seat's stack2_down table attribute.
- Reset hand_points, tricks_won, bid and the pending_reveal flags.
- Reset contract, multiplier = 1, declarer = 0 and defender = 0.
2. **sync** (all players): Each player sees their own hand, all four face-up stack cards, and the public table state.
3. **poll** (all players): When round_in_hand == 0: each player's bid is set to their answer (Pass = 0). No one sees a bid until both are in.
4. **update** (all players): When round_in_hand == 0, set declarer and contract_bid as follows:
- If one bid is higher, that seat is declarer and contract_bid is that bid.
- If the bids are equal and above 0, forehand is declarer at that bid.
- If both bids are 0, forehand is declarer with contract_bid = 53.
Then defender = the other seat. Both bids, the declarer and contract_bid are announced.
5. **ask** (the seat in declarer): When round_in_hand == 0: contract is set to the answer and announced.
6. **ask** (the seat in defender): When round_in_hand == 0: multiplier = 2 if Stoß, else 1. The choice is announced. Then leader = forehand and follower = dealer.
7. **ask** (the seat in leader): When round_in_hand >= 1: led_card is set to the answer and announced. The card is removed from hand. If it was stack1_up or stack2_up, that attribute becomes empty and the matching pending_reveal flag is set to true.
8. **update** (all players): When round_in_hand >= 1, build follow_options:
- Take the follower's available cards (hand plus non-empty stack ups) whose effective suit under contract equals the effective suit of led_card.
- If there are none, take all of the follower's available cards.
Effective suit is 'Trump' if the card's trump_strength is above 0, otherwise its printed suit.
9. **ask** (the seat in follower): When round_in_hand >= 1: followed_card is set to the answer and announced. The card is removed from hand or from its stack up, and the matching pending_reveal flag is set to true when it came from a stack.
10. **update** (all players): When round_in_hand >= 1, decide the trick winner from trump_strength and plain_rank under contract:
- If either card has trump_strength > 0, the card with the higher trump_strength wins.
- Otherwise, if followed_card's printed suit equals led_card's suit, the higher plain_rank wins.
- Otherwise the leader wins.
The winner adds the card points of both cards to hand_points and adds 1 to tricks_won. Set leader = winner and follower = the other seat. For every stack whose pending_reveal is true, move the matching face-down table card into that stack's up attribute and clear the flag. Announce the trick result.
11. **update** (all players): When round_in_hand == 8 (hand scoring):
- Let base = 2 if contract_bid == 53, 3 if 66, 4 if 79.
- The scorer is the declarer if the declarer's hand_points >= contract_bid, otherwise the defender.
- The scorer's match_points increase by (base + (1 if the scorer's tricks_won == 8 else 0)) * multiplier.
- Each player's card_total increases by their hand_points.
Announce the result.
12. **update** (all players): rounds_played += 1. If round_in_hand == 8, then round_in_hand = 0 and hand_number += 1; otherwise round_in_hand += 1.
13. **check** (all players): End the game if rounds_played >= 36; otherwise continue.

## Ending

- ends when: game.rounds_played >= 36
- ranked by: `you.match_points * 1000 + you.card_total` (the highest wins; players level at the top share the win)
- decided by: After 4 hands, the player with more match points wins. If match points are equal, the higher total card points over all 4 hands wins. If both are equal, the two players share the result, which is a draw.

## Choices the source did not make

- 2 players (min, max and suggested): The designer set 2. The deal uses all 16 cards for exactly two players, so neither more nor fewer seats fit.
- Strategy check: A thoughtful player judges their hand plus the open stack cards before bidding high, picks the contract that fits their trumps, gives Stoß only when the declarer looks overstretched, and times the playing of stack cards to unlock the hidden cards beneath.
- No free-text talk step: Talk is not part of the rules, and with two opponents it only adds words.
- Pass is stored as bid 0: This makes 'higher bid' a numeric comparison.
- Trump ranks encoded as trump_strength 20 down to 11, and plain ranks as Ace 3, Ten 2, Ober 1: This lets the trick winner be decided by arithmetic while keeping exactly the source's order.
- rank_by = match_points * 1000 + card_total: Card totals can never reach 1000 (at most 416), so match points come first and card points only break ties. An exact tie is a shared result, which matches the source's draw.
- Trick card points and trick counts are public: Both players see every played card, so these totals are open information.

## Simplifications

- The bidding steps and the trick steps share one flat round list, each step gated by a 'when' condition on round_in_hand: The engine runs one round script. Per-step arithmetic conditions keep 36 rounds exactly as the source counts them.
- Hand scoring runs as an update at the end of trick round 8: This keeps the round count at 36 without adding a separate scoring round.
- Face-down stack cards are held as hidden table attributes rather than player attributes: Not even their owner may see them, and a player attribute cannot be hidden from its owner.

## Unsupported (needs engine work)

- none
