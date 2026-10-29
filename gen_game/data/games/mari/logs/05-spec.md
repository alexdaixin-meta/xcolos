# 05 spec

- time: 2026-10-28T02:27:56+00:00 (61.4s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 cdd15689551f8e41, reply sha256 e5959abc9e60ab06

## Sent

````
Game: Little Bidding Mariáš
Players in the source: 3 to 3
Suggested table size, chosen by the designer of these rules (keep it): 3

Rules, as filed in the inventory:
CARDS. There are 20 cards in four suits, Hearts, Bells, Leaves and Acorns, each with ranks A, 10, K, O (Ober) and U (Unter). Within a suit the ranks run from highest to lowest A, 10, K, O, U. Each Ace and each Ten is worth 10 card points; all other cards are worth 0. Winning the 6th (last) trick of a deal is worth 10 more points, so the deal has 90 card points in total. Internally each card has the code suit*5 + rank, with suits Hearts=0, Bells=1, Leaves=2, Acorns=3 and ranks U=0, O=1, K=2, 10=3, A=4. Players see and name cards by their names, for example 'Ten of Leaves'. Suit order for tie-breaks is Hearts, Bells, Leaves, Acorns.

MATCH. The match has 6 deals of 6 tricks each, 36 rounds in total. Each round is one trick. Players are seated P1, P2, P3, and seat order is cyclic (P1, P2, P3, P1, ...). The eldest is P1 in deals 1 and 4, P2 in deals 2 and 5, and P3 in deals 3 and 6. Every score starts at 0. Players may not exchange messages at any time; defenders cooperate only through their card play.

DEAL (first round of each deal). The engine shuffles all 20 cards and deals 6 to each player privately. The remaining 2 cards are the talon: face down, seen by no one, and out of play for the whole deal.

BIDDING (first round of each deal, one simultaneous poll). Every player privately submits one answer containing a bid and a suit. A bid is PASS or one of 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150. A suit is Hearts, Bells, Leaves or Acorns.
- Any bid not in this list counts as PASS.
- The eldest may not pass: an eldest PASS or invalid bid counts as 50.
- A missing or invalid suit becomes the suit in which that player holds the most cards, ties broken by the suit order.
All bids and suits are then revealed together. The highest bid wins. If bids are equal, the eldest wins the tie first, then the next player in seat order after the eldest. The winner is the declarer, their bid is the contract T, and their suit is trump. The other two players are the defenders and form a team for this deal.

MARRIAGES (announced right after bidding). Every player who holds both the K and the O of one suit has a marriage in that suit. A marriage is worth 40 in the trump suit and 20 in any other suit, and it belongs to its holder's side (declarer or defenders). The engine publicly announces every marriage, its holder and its value. At the end of the deal a side's marriages count only if that side won at least one trick.

PLAYING A TRICK. The declarer leads the first trick of the deal. After that, the winner of the previous trick leads. Starting with the leader, each player in seat order plays one card, and each card is announced to all. The leader may play any card. For the other players:
(a) If you hold a card of the led suit, you must play that suit. You must also play one that beats the highest card of the led suit already in the trick, if you can. This beating duty is lifted only when the led suit is not trump and a trump has already been played to this trick.
(b) If you hold no card of the led suit but hold a trump, you must play a trump. It must beat the highest trump already in the trick, if you can.
(c) Otherwise you may play any card.
If a player names a card that is illegal or not in their hand, the engine plays for them the legal card of lowest rank; among equal ranks, the first in the suit order.
The trick is won by the highest trump in it, or by the highest card of the led suit if it holds no trump. Equivalently, each card gets the key rank + 10 if it is trump + 5 if it is of the led suit, and the highest key wins. The card points of the trick, plus 10 if it is the 6th trick, go to the winner's side: the declarer alone, or the defenders together. The engine announces the trick winner and both sides' running points.

END OF DEAL (after the 6th trick).
1. The declarer's tally is the declarer's points (including any last-trick 10), plus the declarer's marriages if the declarer won at least 1 trick, minus the defenders' marriages if the defenders won at least 1 trick.
2. Let S = (T − 40) / 10, so a contract of 50 gives S = 1 and 150 gives S = 11.
3. If the tally is at least T, the contract is made and S is unchanged. Otherwise S becomes −(S + 1).
4. If trump is Hearts, S is doubled.
5. The declarer's score changes by 2×S, and each defender's score changes by −S.
6. The engine announces the tally, whether the contract was made, and all scores.

ENGINE STEP LIST (per round; steps marked [trick 1] run only in the first round of a deal, and steps marked [trick 6] only in the last).
1. [trick 1] Shuffle and deal 6 hidden cards to each player and 2 to the talon.
2. [trick 1] Reset the declarer's points, the defenders' points and the declarer's tricks to 0.
3. [trick 1] Simultaneous poll: bid and suit.
4. [trick 1] Calc: apply the invalid-input rules; set declarer, T, trump, and leader = declarer.
5. [trick 1] Calc: the marriage values of the declarer's side and of the defenders' side.
6. [trick 1] Announce the bids, declarer, contract, trump and marriages.
7. Clear the list of cards in the current trick.
8. The leader chooses a card.
9. Validate or apply the fallback; remove the card from the hand, add it to the trick list, announce it.
10. The next player chooses a card.
11. Validate, remove, add and announce as in step 9.
12. The third player chooses a card.
13. Validate, remove, add and announce as in step 9.
14. Calc the trick winner by maximum key. Add the trick points (+10 on trick 6) to the winner's side, add 1 to the declarer's tricks if the declarer won, set the leader to the winner, and announce.
15. [trick 6] Calc the tally, S, the fail transform, Hearts doubling and all score changes.
16. [trick 6] Announce the tally, the result and the scores.
17. Advance the round counter.
18. [round 36] End the match and decide the winner.

ATTRIBUTES (16). Per player (4): score, hand, bid, bid suit. Table (12): round number, talon, declarer, contract T, trump, leader, cards in the current trick, declarer's points, defenders' points, declarer's tricks, declarer-side marriage value, defender-side marriage value. The deal number, trick number and eldest are derived from the round number. The defenders' trick count is (tricks completed − declarer's tricks).

How the winner is decided: After round 36 (6 deals), the player with the highest total score wins. If two or three players tie for the highest total, the game is a draw. Every deal is zero-sum (the declarer gains 2×S, and each defender loses S), so the totals always sum to 0.
````

## Reply

````
```json
{
  "name": "Little Bidding Mariáš",
  "summary": "Three-player trick-taking game over 6 deals of 6 tricks: one simultaneous bid picks a declarer and trump, marriages are announced, and the declarer plays alone against two defenders to reach the contract.",
  "players": {"min": 3, "max": 3, "suggested": 3},
  "parameters": {
    "card_count": 20,
    "suit_count": 4,
    "ranks_per_suit": 5,
    "suit_code_multiplier": 5,
    "hand_size": 6,
    "talon_size": 2,
    "tricks_per_deal": 6,
    "deals": 6,
    "total_rounds": 36,
    "ace_points": 10,
    "ten_points": 10,
    "last_trick_bonus": 10,
    "deal_card_points_total": 90,
    "min_bid": 50,
    "max_bid": 150,
    "bid_step": 10,
    "eldest_forced_bid": 50,
    "trump_marriage_value": 40,
    "plain_marriage_value": 20,
    "contract_offset": 40,
    "contract_divisor": 10,
    "hearts_multiplier": 2,
    "declarer_score_multiplier": 2,
    "defender_score_multiplier": 1,
    "trump_key_bonus": 10,
    "led_suit_key_bonus": 5,
    "starting_score": 0,
    "min_tricks_for_marriages": 1
  },
  "attributes": {
    "player": [
      {"key": "score", "type": "number", "visible": "public", "initial": 0, "meaning": "Match score, the sum of the deal settlements so far.", "observable": true},
      {"key": "hand", "type": "list", "visible": "ally", "initial": [], "meaning": "Card codes (suit*5+rank) held privately. 6 are dealt each deal and one is removed per trick.", "observable": false},
      {"key": "bid", "type": "text", "visible": "public", "initial": "PASS", "meaning": "This deal's bid: PASS or 50..150 in steps of 10. Submitted in a simultaneous poll and revealed together.", "observable": false},
      {"key": "bid_suit", "type": "text", "visible": "public", "initial": "", "meaning": "Suit named with the bid: Hearts, Bells, Leaves or Acorns.", "observable": false}
    ],
    "game": [
      {"key": "round", "type": "number", "visible": "public", "initial": 1, "meaning": "Round (trick) counter, 1..36. deal = floor((round-1)/6)+1, trick = (round-1)%6+1, eldest seat = ((deal-1)%3)+1.", "observable": true},
      {"key": "deck", "type": "list", "visible": "none", "initial": "codes 0..19", "meaning": "The full 20-card pack that each deal is shuffled and dealt from.", "observable": false},
      {"key": "talon", "type": "list", "visible": "none", "initial": [], "meaning": "The 2 undealt cards, face down and out of play for the deal.", "observable": false},
      {"key": "declarer", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat of this deal's declarer.", "observable": true},
      {"key": "contract", "type": "number", "visible": "public", "initial": 0, "meaning": "Contract T, the declarer's winning bid.", "observable": true},
      {"key": "trump", "type": "text", "visible": "public", "initial": "", "meaning": "Trump suit, the declarer's bid suit.", "observable": true},
      {"key": "leader", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat that leads the current trick.", "observable": false},
      {"key": "trick_cards", "type": "list", "visible": "public", "initial": [], "meaning": "Cards played to the current trick, in play order starting with the leader.", "observable": false},
      {"key": "declarer_points", "type": "number", "visible": "public", "initial": 0, "meaning": "Card points won by the declarer this deal, including the last-trick 10.", "observable": true},
      {"key": "defender_points", "type": "number", "visible": "public", "initial": 0, "meaning": "Card points won by the defenders together this deal.", "observable": true},
      {"key": "declarer_tricks", "type": "number", "visible": "public", "initial": 0, "meaning": "Tricks won by the declarer this deal. Defender tricks = tricks completed - declarer_tricks.", "observable": false},
      {"key": "declarer_marriages", "type": "number", "visible": "public", "initial": 0, "meaning": "Total marriage value held by the declarer.", "observable": false},
      {"key": "defender_marriages", "type": "number", "visible": "public", "initial": 0, "meaning": "Total marriage value held by the two defenders.", "observable": false}
    ]
  },
  "setup": [
    "Seat the players as P1, P2 and P3. Seat order is cyclic.",
    "Set every score to 0 and round to 1.",
    "Fill the deck with the 20 card codes 0..19 (suit*5+rank; Hearts=0, Bells=1, Leaves=2, Acorns=3; U=0, O=1, K=2, 10=3, A=4).",
    "Players may not exchange messages at any time, so the game has no talk step."
  ],
  "round": [
    {"action": "update", "who": "table", "answer": null, "effect": "[when (round-1)%6==0] Return all cards to the deck. Draw 6 cards at random from the deck into each player's hand and the remaining 2 into talon (hidden). Set declarer_points=0, defender_points=0, declarer_tricks=0, trick_cards=[]."},
    {"action": "sync", "who": "all players", "answer": null, "effect": "[when (round-1)%6==0] Each player privately sees their own hand, named by card names (e.g. 'Ten of Leaves')."},
    {"action": "poll", "who": "all players", "answer": "One choice of 'BID SUIT', where BID is PASS or 50,60,...,150 and SUIT is Hearts, Bells, Leaves or Acorns. The eldest is not offered PASS.", "effect": "[when (round-1)%6==0] Sets bid and bid_suit for every player. No answer is seen until all are in."},
    {"action": "update", "who": "table", "answer": null, "effect": "[when (round-1)%6==0] A bid not in the list becomes PASS. An eldest PASS or invalid bid becomes 50. A missing or invalid suit becomes the suit with the most cards in that player's hand, ties broken by Hearts, Bells, Leaves, Acorns. declarer = the seat with the maximum of bidvalue*10 + (3 - ((seat - eldest) mod 3)), with PASS = 0. Set contract = declarer's bid, trump = declarer's bid_suit, leader = declarer."},
    {"action": "update", "who": "table", "answer": null, "effect": "[when (round-1)%6==0] For each player and each suit s where both codes s*5+2 (K) and s*5+1 (O) are in hand, the marriage is worth 40 if s is trump, else 20. declarer_marriages = the sum for the declarer. defender_marriages = the sum for the two other seats."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "[when (round-1)%6==0] Announce all bids and suits, the declarer, the contract, the trump, and every marriage with its holder and value."},
    {"action": "update", "who": "table", "answer": null, "effect": "Set trick_cards = []."},
    {"action": "ask", "who": "seat leader", "answer": "One card from own hand, chosen by name.", "effect": "The chosen card is the lead."},
    {"action": "update", "who": "seat leader", "answer": null, "effect": "If the card is not in hand, use the lowest-rank card in hand, ties broken by suit order. Remove it from hand, append it to trick_cards, and announce it to all."},
    {"action": "ask", "who": "seat leader%3+1", "answer": "One card from own hand, chosen by name (offered the legal cards).", "effect": "The chosen card is this seat's play."},
    {"action": "update", "who": "seat leader%3+1", "answer": null, "effect": "If the card is illegal or not in hand, play the legal card of lowest rank, ties broken by suit order. Remove it from hand, append it to trick_cards, and announce it.", "judged": "The named card is in the player's hand and obeys the rules: follow the led suit and beat the highest led-suit card if possible (the beating duty is lifted when the led suit is not trump and a trump is already in the trick); otherwise play a trump that beats the highest trump if possible; otherwise any card."},
    {"action": "ask", "who": "seat (leader+1)%3+1", "answer": "One card from own hand, chosen by name (offered the legal cards).", "effect": "The chosen card is this seat's play."},
    {"action": "update", "who": "seat (leader+1)%3+1", "answer": null, "effect": "Validate as in the second player's step, using the fallback if needed. Remove the card from hand, append it to trick_cards, and announce it.", "judged": "The named card is in the player's hand and obeys the rules: follow the led suit and beat the highest led-suit card if possible (the beating duty is lifted when the led suit is not trump and a trump is already in the trick); otherwise play a trump that beats the highest trump if possible; otherwise any card."},
    {"action": "update", "who": "table", "answer": null, "effect": "Each card's key = rank + 10*(suit==trump) + 5*(suit==led suit). The winner is the seat that played the maximum key, the i-th card belonging to seat ((leader-1+i)%3)+1. points = 10 per Ace or Ten in trick_cards, +10 if (round-1)%6==5. If winner==declarer, add points to declarer_points and 1 to declarer_tricks; otherwise add points to defender_points. Set leader = winner. Announce the winner, declarer_points and defender_points."},
    {"action": "update", "who": "all players", "answer": null, "effect": "[when (round-1)%6==5] tally = declarer_points + (declarer_tricks>=1 ? declarer_marriages : 0) - ((6-declarer_tricks)>=1 ? defender_marriages : 0). S = (contract-40)/10. If tally < contract, S = -(S+1). If trump == Hearts, S = 2*S. The declarer's score += 2*S; each defender's score -= S."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "[when (round-1)%6==5] Announce the tally, whether the contract was made, and all scores."},
    {"action": "update", "who": "table", "answer": null, "effect": "round += 1."},
    {"action": "check", "who": "table", "answer": null, "effect": "End the match if round > 36; otherwise continue."}
  ],
  "ending": {
    "condition": "round > 36",
    "rank_by": "you.score",
    "decided_by": "After 6 deals (36 tricks), the player with the highest total score wins. Players tied at the top share the result."
  },
  "rules": [
    {"id": "R1", "text": "When a deal starts (round 1, 7, 13, 19, 25, 31), then each player receives 6 hidden cards and 2 cards go to the talon, which is out of play."},
    {"id": "R2", "text": "When a deal starts, then declarer_points, defender_points and declarer_tricks are reset to 0."},
    {"id": "R3", "text": "When the deal is d, then the eldest is seat ((d-1)%3)+1: P1 in deals 1 and 4, P2 in deals 2 and 5, P3 in deals 3 and 6."},
    {"id": "R4", "text": "When bidding, then all players submit a bid and suit simultaneously and all are revealed together."},
    {"id": "R5", "text": "When a bid is not one of PASS, 50, 60, ..., 150, then it counts as PASS."},
    {"id": "R6", "text": "When the eldest passes or bids invalidly, then the eldest's bid counts as 50."},
    {"id": "R7", "text": "When a suit is missing or invalid, then it becomes the suit in which that player holds the most cards, ties broken by Hearts, Bells, Leaves, Acorns."},
    {"id": "R8", "text": "When bids are compared, then the highest bid wins; on a tie the eldest wins, then the next seat after the eldest."},
    {"id": "R9", "text": "When the declarer is set, then contract equals the declarer's bid, trump equals the declarer's suit, and the declarer leads trick 1."},
    {"id": "R10", "text": "When a player holds the K and O of one suit, then that is a marriage worth 40 in trump and 20 otherwise, credited to the holder's side and publicly announced."},
    {"id": "R11", "text": "When a later player holds a card of the led suit, then they must play that suit and beat the highest led-suit card in the trick if they can, unless the led suit is not trump and a trump is already in the trick."},
    {"id": "R12", "text": "When a later player has no card of the led suit but holds a trump, then they must play a trump that beats the highest trump in the trick if they can."},
    {"id": "R13", "text": "When a later player has neither the led suit nor a trump, then they may play any card."},
    {"id": "R14", "text": "When a player names an illegal card or one not in their hand, then the engine plays their legal card of lowest rank, ties broken by suit order."},
    {"id": "R15", "text": "When a trick is complete, then the card with the highest key (rank + 10 if trump + 5 if of the led suit) wins."},
    {"id": "R16", "text": "When a trick is won, then its Aces and Tens score 10 each to the winner's side, plus 10 if it is the 6th trick of the deal."},
    {"id": "R17", "text": "When a trick is won, then the winner leads the next trick."},
    {"id": "R18", "text": "When a deal ends, then tally = declarer_points + declarer_marriages (if the declarer won at least 1 trick) - defender_marriages (if the defenders won at least 1 trick)."},
    {"id": "R19", "text": "When a deal ends with tally >= contract, then S = (contract-40)/10. For example, a 50 contract that is made gives S = 1."},
    {"id": "R20", "text": "When a deal ends with tally < contract, then S = -((contract-40)/10 + 1). For example, a failed 50 contract gives S = -2."},
    {"id": "R21", "text": "When trump is Hearts, then S is doubled."},
    {"id": "R22", "text": "When a deal is settled, then the declarer's score changes by 2*S and each defender's score changes by -S."},
    {"id": "R23", "text": "When round 36 is complete, then the match ends and the highest score wins; a tie at the top is shared."}
  ],
  "offers": [
    {"question": "Bid and suit poll", "who": "all players", "options": "The eldest: each of 50,60,...,150 combined with each of Hearts, Bells, Leaves, Acorns (44 options). Any other seat: those 44 plus PASS with each suit (48 options)."},
    {"question": "Leader's card", "who": "seat leader", "options": "Every card in the leader's hand."},
    {"question": "Second and third player's card", "who": "the two non-leading seats", "options": "Only the cards in hand that are legal under the follow/beat/trump rules. With no led suit and no trump in hand, every card in hand."}
  ],
  "choices": [
    {"what": "3 players exactly", "why": "The designer fixed 3 seats: a lone declarer against a two-defender team, with 20 cards dealt 6-6-6 plus a 2-card talon. No other count works with this pack."},
    {"what": "No talk step", "why": "The rules forbid all messages; defenders cooperate only through their card play."},
    {"what": "Bid and suit as one combined choice", "why": "The rules ask for one answer holding both. A combined list keeps it to one simultaneous poll."},
    {"what": "Eldest not offered PASS", "why": "The eldest may not pass. The rule still maps an eldest PASS to 50 if one arrives."},
    {"what": "Card plays use ask, in seat order", "why": "Trick play is sequential and each player sees the earlier cards."},
    {"what": "Strategy", "why": "Bid to the hand's strength including marriages, choose trump (Hearts doubles the stakes), and as defenders signal through play and save Aces and Tens for each other."}
  ],
  "simplifications": [
    {"what": "Legality of a played card is judged by a referee sentence; the fallback card is then computed", "why": "The follow/beat/trump rule is long to express as plain arithmetic in one step."},
    {"what": "A tie for top score is a shared win rather than a named draw", "why": "The engine has no separate draw; players level at the top share the win, which matches no single winner."},
    {"what": "Deal-start and deal-end steps carry a when-condition on the round counter", "why": "The step list is flat; per-step conditions reproduce the [trick 1] and [trick 6] markers."},
    {"what": "Added a hidden deck list", "why": "Dealing needs a list to draw from."}
  ],
  "unsupported": []
}
```
````
