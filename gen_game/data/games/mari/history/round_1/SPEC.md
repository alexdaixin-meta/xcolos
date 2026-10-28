# Little Bidding Mariáš

Three-player trick-taking game over 6 deals of 6 tricks: one simultaneous bid picks a declarer and trump, marriages are announced, and the declarer plays alone against two defenders to reach the contract.

Players: 3 to 3, best with 3

## Parameters

- `card_count` = 20
- `suit_count` = 4
- `ranks_per_suit` = 5
- `suit_code_multiplier` = 5
- `hand_size` = 6
- `talon_size` = 2
- `tricks_per_deal` = 6
- `deals` = 6
- `total_rounds` = 36
- `ace_points` = 10
- `ten_points` = 10
- `last_trick_bonus` = 10
- `deal_card_points_total` = 90
- `min_bid` = 50
- `max_bid` = 150
- `bid_step` = 10
- `eldest_forced_bid` = 50
- `trump_marriage_value` = 40
- `plain_marriage_value` = 20
- `contract_offset` = 40
- `contract_divisor` = 10
- `hearts_multiplier` = 2
- `declarer_score_multiplier` = 2
- `defender_score_multiplier` = 1
- `trump_key_bonus` = 10
- `led_suit_key_bonus` = 5
- `starting_score` = 0
- `min_tricks_for_marriages` = 1

## Round

1. **update** (table): [when (round-1)%6==0] Return all cards to the deck. Draw 6 cards at random from the deck into each player's hand and the remaining 2 into talon (hidden). Set declarer_points=0, defender_points=0, declarer_tricks=0, trick_cards=[].
2. **sync** (all players): [when (round-1)%6==0] Each player privately sees their own hand, named by card names (e.g. 'Ten of Leaves').
3. **poll** (all players): [when (round-1)%6==0] Sets bid and bid_suit for every player. No answer is seen until all are in.
4. **update** (table): [when (round-1)%6==0] A bid not in the list becomes PASS. An eldest PASS or invalid bid becomes 50. A missing or invalid suit becomes the suit with the most cards in that player's hand, ties broken by Hearts, Bells, Leaves, Acorns. declarer = the seat with the maximum of bidvalue*10 + (3 - ((seat - eldest) mod 3)), with PASS = 0. Set contract = declarer's bid, trump = declarer's bid_suit, leader = declarer.
5. **update** (table): [when (round-1)%6==0] For each player and each suit s where both codes s*5+2 (K) and s*5+1 (O) are in hand, the marriage is worth 40 if s is trump, else 20. declarer_marriages = the sum for the declarer. defender_marriages = the sum for the two other seats.
6. **tell** (all players): [when (round-1)%6==0] Announce all bids and suits, the declarer, the contract, the trump, and every marriage with its holder and value.
7. **update** (table): Set trick_cards = [].
8. **ask** (seat leader): The chosen card is the lead.
9. **update** (seat leader): If the card is not in hand, use the lowest-rank card in hand, ties broken by suit order. Remove it from hand, append it to trick_cards, and announce it to all.
10. **ask** (seat leader%3+1): The chosen card is this seat's play.
11. **update** (seat leader%3+1): If the card is illegal or not in hand, play the legal card of lowest rank, ties broken by suit order. Remove it from hand, append it to trick_cards, and announce it. (judged: "The named card is in the player's hand and obeys the rules: follow the led suit and beat the highest led-suit card if possible (the beating duty is lifted when the led suit is not trump and a trump is already in the trick); otherwise play a trump that beats the highest trump if possible; otherwise any card.")
12. **ask** (seat (leader+1)%3+1): The chosen card is this seat's play.
13. **update** (seat (leader+1)%3+1): Validate as in the second player's step, using the fallback if needed. Remove the card from hand, append it to trick_cards, and announce it. (judged: "The named card is in the player's hand and obeys the rules: follow the led suit and beat the highest led-suit card if possible (the beating duty is lifted when the led suit is not trump and a trump is already in the trick); otherwise play a trump that beats the highest trump if possible; otherwise any card.")
14. **update** (table): Each card's key = rank + 10*(suit==trump) + 5*(suit==led suit). The winner is the seat that played the maximum key, the i-th card belonging to seat ((leader-1+i)%3)+1. points = 10 per Ace or Ten in trick_cards, +10 if (round-1)%6==5. If winner==declarer, add points to declarer_points and 1 to declarer_tricks; otherwise add points to defender_points. Set leader = winner. Announce the winner, declarer_points and defender_points.
15. **update** (all players): [when (round-1)%6==5] tally = declarer_points + (declarer_tricks>=1 ? declarer_marriages : 0) - ((6-declarer_tricks)>=1 ? defender_marriages : 0). S = (contract-40)/10. If tally < contract, S = -(S+1). If trump == Hearts, S = 2*S. The declarer's score += 2*S; each defender's score -= S.
16. **tell** (all players): [when (round-1)%6==5] Announce the tally, whether the contract was made, and all scores.
17. **update** (table): round += 1.
18. **check** (table): End the match if round > 36; otherwise continue.

## Ending

- ends when: round > 36
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: After 6 deals (36 tricks), the player with the highest total score wins. Players tied at the top share the result.

## Choices the source did not make

- 3 players exactly: The designer fixed 3 seats: a lone declarer against a two-defender team, with 20 cards dealt 6-6-6 plus a 2-card talon. No other count works with this pack.
- No talk step: The rules forbid all messages; defenders cooperate only through their card play.
- Bid and suit as one combined choice: The rules ask for one answer holding both. A combined list keeps it to one simultaneous poll.
- Eldest not offered PASS: The eldest may not pass. The rule still maps an eldest PASS to 50 if one arrives.
- Card plays use ask, in seat order: Trick play is sequential and each player sees the earlier cards.
- Strategy: Bid to the hand's strength including marriages, choose trump (Hearts doubles the stakes), and as defenders signal through play and save Aces and Tens for each other.

## Simplifications

- Legality of a played card is judged by a referee sentence; the fallback card is then computed: The follow/beat/trump rule is long to express as plain arithmetic in one step.
- A tie for top score is a shared win rather than a named draw: The engine has no separate draw; players level at the top share the win, which matches no single winner.
- Deal-start and deal-end steps carry a when-condition on the round counter: The step list is flat; per-step conditions reproduce the [trick 1] and [trick 6] markers.
- Added a hidden deck list: Dealing needs a list to draw from.

## Unsupported (needs engine work)

- none
