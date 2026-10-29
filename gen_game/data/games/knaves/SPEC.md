# Knaves Short Deck with Bids

Three players play 36 tricks with a 20-card deck, in six hands of six tricks. Each player bids how many tricks they will take each hand, Jacks in a won trick cost points, and an exact bid earns a bonus.

Players: 3 to 3, best with 3

## Parameters

- `num_players` = 3
- `deck_size` = 20
- `total_rounds` = 36
- `tricks_per_hand` = 6
- `num_hands` = 6
- `cards_per_player` = 6
- `turned_card_position` = 19
- `hidden_card_position` = 20
- `bid_min` = 0
- `bid_max` = 6
- `trick_base_points` = 2
- `penalty_JS` = 1
- `penalty_JC` = 2
- `penalty_JD` = 3
- `penalty_JH` = 4
- `exact_bid_bonus` = 5
- `rank_value_A` = 5
- `rank_value_K` = 4
- `rank_value_Q` = 3
- `rank_value_J` = 2
- `rank_value_10` = 1
- `trump_bonus` = 10

## Round

1. **update** (all players): When trick_in_hand == 1: set dealer = ((hand_number-1) mod 3)+1 and leader = (dealer mod 3)+1. Set deck to the full 20-card list, empty every hand and discard, and set every bid, tricks_taken and hand_score to 0. Shuffle the deck once. Deal cards 1-6 to seat 1's hand, 7-12 to seat 2's hand and 13-18 to seat 3's hand. Put card 19 in turned_card and set trump_suit to its suit. Put card 20 in hidden_card. The deck is now empty. Announce turned_card, trump_suit, dealer and leader.
2. **sync** (all players): When trick_in_hand == 1: each player is sent their own hand, plus the public turned_card and trump_suit.
3. **poll** (all players): When trick_in_hand == 1: set each player's bid to their answer. After all answers are in, broadcast every bid to all.
4. **ask** (the seat equal to leader): Remove the card from the leader's hand, set the leader's played_card to it, append it to discard, and set led_suit to its suit. Show the card to all.
5. **ask** (seat (leader mod 3)+1): Remove the card from the hand, set played_card to it, append it to discard, and show it to all.
6. **ask** (seat ((leader+1) mod 3)+1): Remove the card from the hand, set played_card to it, append it to discard, and show it to all.
7. **update** (all players): Score each played_card as rank value (A 5, K 4, Q 3, J 2, 10 1), plus 10 if its suit is trump_suit, or 0 if its suit is neither trump_suit nor led_suit. Set trick_winner to the seat with the highest score. That seat adds 1 to tricks_taken and adds 2 - (1 if JS played) - (2 if JC played) - (3 if JD played) - (4 if JH played) to hand_score. Set leader = trick_winner. Announce the winner.
8. **update** (all players): When trick_in_hand == 6: each player with tricks_taken == bid adds 5 to hand_score. Every player then adds hand_score to total. Announce all totals.
9. **update** (all players): Add 1 to round. Set trick_in_hand = ((round-1) mod 6)+1 and hand_number = floor((round-1)/6)+1.
10. **check** (all players): End the game if round > 36; otherwise continue to the next round.

## Ending

- ends when: round > 36
- ranked by: `you.total` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their total after the end-of-hand scoring of hand 6. The highest total wins. Players tied for the highest total share the result, which the source calls a draw.

## Choices the source did not make

- 3 players, min = max = suggested = 3: The designer fixed the game at 3. The deal uses exactly 18 of 20 cards, the dealer rotation is mod 3, and the 6-card hand fits only three seats.
- No talk step before bids or plays: The rules include no table talk, and adding it would add a mechanic.
- Trick winner computed by an arithmetic card score (rank 1-5, +10 for trump, 0 for an off-suit non-trump): This reproduces R13 exactly by calculation, with no referee needed.
- hand_score, played_card and discard are public: The source leaves their visibility open; all are derivable from cards played face up.
- Strategy at the table: Players read their hand against the trump suit to bid accurately, dodge winning tricks loaded with costly Jacks (especially JH and JD), and dump Jacks onto opponents' tricks while steering toward their exact bid.

## Simplifications

- A tie for the highest total is a shared win for the tied players rather than a separate draw result: The engine ranks by one expression and lets players level at the top share the win. This is equivalent to the source's draw.
- Per-hand reset, deal and bid run as single steps carrying the condition trick_in_hand == 1, and end-of-hand scoring carries trick_in_hand == 6: The step list is flat; each conditional step is a single step, not an alternative block.

## Unsupported (needs engine work)

- none
