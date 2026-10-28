# 05 spec

- time: 2026-10-28T03:35:51+00:00 (66.6s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 dbd5f427cfb251cd, reply sha256 a5b1362964192bbf

## Sent

````
Game: Pocket Smear
Players in the source: 3 to 3
Suggested table size, chosen by the designer of these rules (keep it): 3

Rules, as filed in the inventory:
PLAYERS: exactly 3, seated as Player 1, Player 2 and Player 3. Seat order is 1, 2, 3, then back to 1.

DECK: 24 cards in three suits (Red, Blue, Green). Each suit has ranks 1 to 8. Card points, used only for Game: rank 8 = 4, rank 7 = 3, rank 6 = 2, rank 5 = 1, all other ranks = 0.

STRUCTURE: The game is 9 deals. Each deal is 4 rounds with one trick per round, so the game is 36 rounds. The dealer rotates: Player 1 deals deals 1, 4 and 7; Player 2 deals deals 2, 5 and 8; Player 3 deals deals 3, 6 and 9. For each deal, PRIORITY ORDER is: the player after the dealer in seat order, then the next player, then the dealer. All scores start at 0.

DEAL (first round of each deal): Shuffle all 24 cards and deal 4 cards privately to each player. The other 12 cards are set aside face down, unseen by anyone, for the whole deal. Each player sees only their own hand.

BID (first round of each deal, one simultaneous poll): Every player at the same moment submits ONE answer made of two parts: (a) either PASS or a whole number from 2 to 6, and (b) one suit that appears in their own hand. A suit must be named even when passing. Examples: '4 Blue', 'PASS Red'. When all answers are in, the engine reveals every player's bid amount (or PASS).
- The highest number wins. A tie goes to the tied player who comes first in priority order.
- The winner becomes the PITCHER, their number becomes the CONTRACT, and their named suit becomes TRUMP.
- If all three pass, the dealer becomes the pitcher with a contract of 2, and trump is the suit the dealer named.
- The engine announces the pitcher, the contract and trump. The suits named by the other two players are NEVER revealed.

TRICKS (each round of a deal): Three cards are played one at a time, starting with the LEADER and continuing in seat order.
- Leader: in the first trick of a deal, the leader is the pitcher, who must lead a trump card. The pitcher always holds one, because they named a suit from their hand. In later tricks of the deal, the leader is the winner of the previous trick, who may lead any card.
- Following: each later player must play a card of the led suit if they hold one, but may instead play a trump even if they hold the led suit. A player holding no card of the led suit may play any card.
- Winning: the trick goes to the highest-ranked trump played. If no trump was played, it goes to the highest-ranked card of the led suit.
- All played cards are visible to everyone. The three cards go into the trick winner's captured pile.

DEAL SCORING (after the 4th trick of each deal; only cards played this deal count; every dealt card is played):
- HIGH, 1 point: to the player who captured the highest-ranked trump played.
- LOW, 1 point: to the player who captured the lowest-ranked trump played. This may be the same card as High. At least one trump is always played, because the first lead is trump.
- GAME, 1 point: to the player whose captured pile has the most card points. If two or more players tie for most, nobody scores Game.
- THREE, 3 points: to the player who captured the trump of rank 3, if it was dealt. If it was not dealt, nobody scores it.
- Each player's deal points are the sum of the categories they won, from 0 to 6.
- Each of the two non-pitchers adds their deal points to their score.
- If the pitcher's deal points are at least the contract, the pitcher adds their deal points to their score.
- Otherwise the pitcher is SET: the pitcher subtracts the contract from their score and does not add their deal points.
- Scores may go negative. Captured piles are then cleared and the next deal begins.

COMMUNICATION: There is no table talk. Players communicate only through bids and played cards.

END: After the 9th deal is scored, the game ends.

How the winner is decided: After 9 deals, the player with the highest total score wins. If two or more players tie for the highest total, the game is a draw.
````

## Reply

````
```json
{
  "name": "Pocket Smear",
  "summary": "A three-player trick-taking game of 9 four-trick deals: bid blind, the highest bidder names trump, then everyone fights for High, Low, Game and Three while the pitcher tries to make the contract.",
  "players": {"min": 3, "max": 3, "suggested": 3},
  "parameters": {
    "players": 3,
    "deals": 9,
    "tricks_per_deal": 4,
    "total_rounds": 36,
    "suits": 3,
    "ranks_per_suit": 8,
    "deck_size": 24,
    "hand_size": 4,
    "set_aside_cards": 12,
    "bid_min": 2,
    "bid_max": 6,
    "pass_value": 0,
    "all_pass_contract": 2,
    "card_points_rank_8": 4,
    "card_points_rank_7": 3,
    "card_points_rank_6": 2,
    "card_points_rank_5": 1,
    "card_points_other_ranks": 0,
    "high_points": 1,
    "low_points": 1,
    "game_points": 1,
    "three_points": 3,
    "three_rank": 3,
    "max_deal_points": 6,
    "starting_score": 0
  },
  "attributes": {
    "player": [
      {"key": "score", "type": "number", "visible": "public", "initial": 0, "meaning": "Running total score. It may go negative.", "observable": true},
      {"key": "hand", "type": "list", "visible": "ally", "initial": [], "meaning": "Cards held this deal, as codes suit*10+rank (Red=1, Blue=2, Green=3), so 18 is Red 8 and 23 is Blue 3.", "observable": false},
      {"key": "bid", "type": "number", "visible": "public", "initial": 0, "meaning": "Bid amount this deal: 2 to 6, or 0 for PASS. It is revealed after the bid poll.", "observable": true},
      {"key": "bid_suit", "type": "text", "visible": "ally", "initial": "", "meaning": "Suit named with the bid. It must be in the player's hand and is never revealed, except that the pitcher's suit becomes trump.", "observable": false},
      {"key": "played_card", "type": "number", "visible": "public", "initial": 0, "meaning": "Card code played in the current trick, or 0 if none yet.", "observable": false},
      {"key": "captured", "type": "list", "visible": "public", "initial": [], "meaning": "Cards captured in tricks this deal.", "observable": false},
      {"key": "captured_points", "type": "number", "visible": "public", "initial": 0, "meaning": "Sum of card points in the captured pile this deal: rank 8 = 4, 7 = 3, 6 = 2, 5 = 1, others 0.", "observable": false},
      {"key": "deal_points", "type": "number", "visible": "public", "initial": 0, "meaning": "Category points won in this deal, from 0 to 6.", "observable": false}
    ],
    "game": [
      {"key": "deck", "type": "list", "visible": "none", "initial": [11,12,13,14,15,16,17,18,21,22,23,24,25,26,27,28,31,32,33,34,35,36,37,38], "meaning": "Undealt cards. It is rebuilt to all 24 cards at the start of each deal.", "observable": false},
      {"key": "set_aside", "type": "list", "visible": "none", "initial": [], "meaning": "The 12 cards set aside face down and unseen for the deal.", "observable": false},
      {"key": "rounds_played", "type": "number", "visible": "public", "initial": 0, "meaning": "Tricks completed so far, from 0 to 36.", "observable": false},
      {"key": "deal_number", "type": "number", "visible": "public", "initial": 1, "meaning": "Current deal, from 1 to 9.", "observable": true},
      {"key": "trick_in_deal", "type": "number", "visible": "public", "initial": 1, "meaning": "Current trick within the deal, from 1 to 4.", "observable": false},
      {"key": "dealer", "type": "number", "visible": "public", "initial": 1, "meaning": "Dealer seat: ((deal_number - 1) mod 3) + 1.", "observable": false},
      {"key": "pitcher", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat of the bid winner this deal.", "observable": true},
      {"key": "contract", "type": "number", "visible": "public", "initial": 0, "meaning": "The pitcher's winning bid, or 2 if all passed.", "observable": true},
      {"key": "trump", "type": "number", "visible": "public", "initial": 0, "meaning": "Trump suit code (1 Red, 2 Blue, 3 Green): the pitcher's named suit.", "observable": true},
      {"key": "leader", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat that leads the current trick.", "observable": false},
      {"key": "led_suit", "type": "number", "visible": "public", "initial": 0, "meaning": "Suit code of the card led in the current trick.", "observable": false},
      {"key": "trick_winner", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat that won the last trick.", "observable": false},
      {"key": "high_trump_rank", "type": "number", "visible": "none", "initial": 0, "meaning": "Highest trump rank played this deal (0 = none yet).", "observable": false},
      {"key": "high_trump_seat", "type": "number", "visible": "none", "initial": 0, "meaning": "Seat that captured the highest trump played.", "observable": false},
      {"key": "low_trump_rank", "type": "number", "visible": "none", "initial": 9, "meaning": "Lowest trump rank played this deal (9 = none yet).", "observable": false},
      {"key": "low_trump_seat", "type": "number", "visible": "none", "initial": 0, "meaning": "Seat that captured the lowest trump played.", "observable": false},
      {"key": "three_seat", "type": "number", "visible": "none", "initial": 0, "meaning": "Seat that captured the trump 3 this deal (0 = not played or not dealt).", "observable": false}
    ]
  },
  "setup": [
    "Seat the 3 players as Player 1, Player 2 and Player 3; seat order is 1, 2, 3, then back to 1.",
    "Set every score to 0, deal_number to 1, trick_in_deal to 1 and rounds_played to 0.",
    "Encode the 24 cards as suit*10+rank, with Red=1, Blue=2, Green=3 and ranks 1 to 8; they are shown to players as names such as 'Red 8'."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "When trick_in_deal == 1: dealer = ((deal_number - 1) mod 3) + 1; deck = all 24 card codes; for each player, clear hand, captured and played_card, and set captured_points = 0, deal_points = 0, bid = 0, bid_suit = ''; draw 4 cards at random from deck into each player's hand; move the remaining 12 deck cards into set_aside; reset high_trump_rank = 0, high_trump_seat = 0, low_trump_rank = 9, low_trump_seat = 0, three_seat = 0."},
    {"action": "sync", "who": "all players", "answer": null, "effect": "When trick_in_deal == 1: each player sees their own hand, the dealer and every score."},
    {"action": "poll", "who": "all players", "answer": "One choice from: 'PASS <suit>' or '<n> <suit>' for n in 2..6, where <suit> is any suit present in the player's own hand", "effect": "When trick_in_deal == 1: bid = n (0 for PASS); bid_suit = the named suit. The bid amounts are broadcast: 'Seat {seat} bids {bid or PASS}'. The suits are not shown."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When trick_in_deal == 1: if max(bid) > 0, pitcher = the seat with the highest bid, ties going to the earliest seat in priority order (dealer+1, dealer+2, dealer, mod 3), and contract = that bid; otherwise pitcher = dealer and contract = 2. trump = pitcher's bid_suit; leader = pitcher."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "When trick_in_deal == 1: announce 'Pitcher: Seat {pitcher}, contract {contract}, trump {trump}'."},
    {"action": "ask", "who": "seat leader", "answer": "A card from own hand; on trick_in_deal == 1 only trump cards are offered", "effect": "played_card = chosen card; remove it from hand; led_suit = floor(card/10); broadcast the card to all."},
    {"action": "ask", "who": "seat (leader mod 3) + 1", "answer": "A legal card from own hand: if the hand holds the led suit, cards of the led suit plus any trumps; otherwise any card", "effect": "played_card = chosen card; remove it from hand; broadcast the card to all."},
    {"action": "ask", "who": "seat ((leader + 1) mod 3) + 1", "answer": "A legal card from own hand, by the same following rule", "effect": "played_card = chosen card; remove it from hand; broadcast the card to all."},
    {"action": "update", "who": "all players", "answer": null, "effect": "trick_winner = the seat whose played_card has suit == trump and the highest rank, or if no trump was played, the seat with the highest rank of led_suit. Append all three played cards to trick_winner's captured; add their card points to trick_winner's captured_points. For each played trump of rank r: if r > high_trump_rank, set high_trump_rank = r and high_trump_seat = trick_winner; if r < low_trump_rank, set low_trump_rank = r and low_trump_seat = trick_winner; if r == 3, set three_seat = trick_winner. Then leader = trick_winner, clear every played_card and announce the winner."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When trick_in_deal == 4: deal_points = (seat == high_trump_seat ? 1 : 0) + (seat == low_trump_seat ? 1 : 0) + (captured_points strictly greater than both other players' captured_points ? 1 : 0) + (seat == three_seat ? 3 : 0). For each non-pitcher, score += deal_points. For the pitcher: if deal_points >= contract, score += deal_points; else score -= contract. Announce every deal_points value and score. Clear every captured pile."},
    {"action": "update", "who": "all players", "answer": null, "effect": "rounds_played += 1; if trick_in_deal == 4, then trick_in_deal = 1 and deal_number += 1; otherwise trick_in_deal += 1."},
    {"action": "check", "who": "all players", "answer": null, "effect": "End the game if rounds_played == 36 (9 deals scored); otherwise continue."}
  ],
  "ending": {
    "condition": "rounds_played == 36",
    "rank_by": "you.score",
    "decided_by": "Each player's standing is their total score after 9 deals; the highest score wins, and players tied for highest share the result (the source calls this a draw)."
  },
  "rules": [
    {"id": "R1", "text": "When deal d begins, then the dealer is seat ((d-1) mod 3)+1: seat 1 deals deals 1, 4 and 7, seat 2 deals 2, 5 and 8, and seat 3 deals 3, 6 and 9."},
    {"id": "R2", "text": "When a deal begins, then all 24 cards are shuffled, each player receives exactly 4 private cards, and the other 12 are set aside unseen for the whole deal."},
    {"id": "R3", "text": "When bidding, then every player answers at once with PASS or a number from 2 to 6, plus one suit present in their own hand; a suit is named even when passing."},
    {"id": "R4", "text": "When the bids are in, then every player's amount or PASS is revealed, and the suits of the two non-pitchers are never revealed."},
    {"id": "R5", "text": "When bids differ, then the highest number wins: that player becomes pitcher, the number becomes the contract and the named suit becomes trump."},
    {"id": "R6", "text": "When the highest bid is tied, then the tied player earliest in priority order (dealer+1, then dealer+2, then dealer) wins the bid."},
    {"id": "R7", "text": "When all three players pass, then the dealer becomes pitcher with contract 2, and trump is the dealer's named suit."},
    {"id": "R8", "text": "When the first trick of a deal is played, then the pitcher leads and must lead a trump card."},
    {"id": "R9", "text": "When a later trick of a deal is played, then the winner of the previous trick leads any card."},
    {"id": "R10", "text": "When a trick is played, then the cards go one at a time from the leader in seat order."},
    {"id": "R11", "text": "When a following player holds the led suit, then they must play the led suit or a trump."},
    {"id": "R12", "text": "When a following player holds no card of the led suit, then they may play any card."},
    {"id": "R13", "text": "When at least one trump is in a trick, then the highest-ranked trump wins it; otherwise the highest-ranked card of the led suit wins it."},
    {"id": "R14", "text": "When a trick is won, then all three cards are visible to everyone and go into the winner's captured pile."},
    {"id": "R15", "text": "When a deal is scored, then 1 point (High) goes to the player who captured the highest-ranked trump played."},
    {"id": "R16", "text": "When a deal is scored, then 1 point (Low) goes to the player who captured the lowest-ranked trump played, which may be the same card as High."},
    {"id": "R17", "text": "When a deal is scored, then 1 point (Game) goes to the player with the most captured card points (rank 8 = 4, 7 = 3, 6 = 2, 5 = 1, others 0), and nobody scores Game if two or more players tie for most."},
    {"id": "R18", "text": "When the trump 3 was dealt and played, then 3 points (Three) go to the player who captured it; if it was not dealt, nobody scores Three."},
    {"id": "R19", "text": "When a deal is scored, then each non-pitcher adds their deal points (0 to 6) to their score."},
    {"id": "R20", "text": "When the pitcher's deal points are at least the contract, then the pitcher adds their deal points to their score."},
    {"id": "R21", "text": "When the pitcher's deal points are below the contract, then the pitcher is set: they subtract the contract from their score and add nothing; scores may go negative."},
    {"id": "R22", "text": "When the 9th deal (36th trick) has been scored, then the game ends and the highest total score wins; players tied for highest share it, which the source calls a draw."},
    {"id": "R23", "text": "When playing, then there is no table talk: players communicate only through bids and played cards."}
  ],
  "offers": [
    {"question": "Bid poll", "who": "all seats", "options": "For each suit S present in the seat's own hand: 'PASS S', '2 S', '3 S', '4 S', '5 S', '6 S'. Suits not in the hand are never offered."},
    {"question": "Lead card", "who": "the leader", "options": "First trick of a deal (the pitcher leading): only the trump cards in their hand. Later tricks: every card in their hand."},
    {"question": "Follow card (second and third player)", "who": "the two seats after the leader, in seat order", "options": "If the hand holds the led suit: every card of the led suit plus every trump in the hand. If the hand holds no card of the led suit: every card in the hand."}
  ],
  "choices": [
    {"what": "3 players, fixed", "why": "The designer set exactly 3; the priority order, dealer rotation and 12 set-aside cards are all built for 3 seats."},
    {"what": "Card encoding suit*10+rank (Red 1, Blue 2, Green 3)", "why": "Lets trick winners, trump checks and card points be worked out by arithmetic; players see card names."},
    {"what": "Bid offered as one combined choice such as '4 Blue' or 'PASS Red'", "why": "The engine takes one answer per question; listing only suits from the seat's own hand enforces that rule."},
    {"what": "PASS stored as bid 0", "why": "Allows a numeric comparison for the highest bid and an all-pass test with max(bid) == 0."},
    {"what": "No talk step", "why": "The rules forbid table talk; players communicate only through bids and cards."},
    {"what": "Strategy at the table", "why": "Players judge their hand's trump strength, bid against two rivals, and decide when to trump in, cash High or protect the 3, reading what is left from the cards played."}
  ],
  "simplifications": [
    {"what": "A tie for the highest final score is a shared win rather than a separate draw", "why": "The engine ranks by one expression and players level at the top share the win; this is the same outcome as a draw."},
    {"what": "Deal-start actions (deal, bid, pitcher resolution) are single steps carrying a 'when trick_in_deal == 1' condition", "why": "The step list is flat; per-step conditions reproduce the first round of each deal."}
  ],
  "unsupported": []
}
```
````
