# 03 spec

- time: 2026-10-28T06:11:43+00:00 (58.1s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 6d65582442c37d7d, reply sha256 2c6f194fa7ce6fdd

## Sent

````
Game: Scopa Duel
Players in the source: 2 to 2
Suggested table size, chosen by the designer of these rules (keep it): 2

Rules, as filed in the inventory:
DECK: 40 cards in four suits: Coins, Cups, Swords, Clubs. Each suit has ranks 1 to 10: Ace=1, 2 to 7 at face value, Jack=8, Knight=9, King=10.

STRUCTURE: The match is 2 hands of 18 rounds each, 36 rounds in total. In each round both players play one card: first the Leader, then the Dealer. In hand 1 (rounds 1 to 18), Player A is Leader and Player B is Dealer. In hand 2 (rounds 19 to 36), the roles swap.

DEALING: At the start of round 1 and round 19, the full 40-card deck is shuffled (the only random event that round). Four cards are dealt face up to the table, and three cards are dealt privately to each player. At the start of rounds 4, 7, 10, 13 and 16 (hand 1) and rounds 22, 25, 28, 31 and 34 (hand 2), both hands are empty and three more cards are dealt to each player from the deck. Each hand uses exactly 4 + 6x3 = 40 cards.

INFORMATION: The table, all played cards and all captures are public. Each player sees only their own hand. The deck order is hidden.

A PLAY: On your turn, choose one card from your hand and declare which table cards you capture: a list, possibly empty. The declaration is legal if:
(a) some table card has the same rank as your card, and you declare exactly one such card; or
(b) no table card has the same rank, and you declare either nothing or a set of table cards whose ranks add up exactly to your card's rank.

If legal, you take your card and the declared cards into your capture pile. If you declared nothing, your card goes face up onto the table. If the declaration is illegal, your card goes face up onto the table and you capture nothing.

SCOPA: If your legal capture leaves the table empty, you score 1 Scopa point. The exception is the final play of a hand (the Dealer's play in round 18 or round 36), which never scores a Scopa.

LAST CAPTURE: The engine records who made the most recent capture. After the Dealer's play in round 18 (and in round 36), every card left on the table goes to that player's capture pile. If nobody captured in that hand, the leftover cards are discarded.

HAND SCORING (after rounds 18 and 36), using only that hand's capture piles:
- 1 point to the player with more captured cards (none if 20-20).
- 1 point to the player with more Coins (none if 5-5).
- 1 point to the holder of the Seven of Coins.
- 1 point to the player with more sevens. If tied, the player with more sixes gets it. If still tied, no point.
- Plus each player's Scopa points.

Capture piles are then cleared for hand 2, but each player's running totals of points, captured cards and captured Coins are kept.

How the winner is decided: After round 36, the player with more total points across both hands wins. If tied, the player who captured more cards in total across both hands wins. If still tied, the player who captured more Coins in total wins. If still tied, the match is a draw.
````

## Reply

````
```json
{
  "name": "Scopa Duel",
  "summary": "Two-player Scopa over 2 hands of 18 rounds. Players capture table cards by matching rank or summing to it, score Scopas for sweeping the table, then score cards, Coins, the Seven of Coins and sevens.",
  "players": {"min": 2, "max": 2, "suggested": 2},
  "parameters": {
    "deck_size": 40,
    "suits": 4,
    "ranks_per_suit": 10,
    "jack_rank": 8,
    "knight_rank": 9,
    "king_rank": 10,
    "hands": 2,
    "rounds_per_hand": 18,
    "total_rounds": 36,
    "table_deal": 4,
    "cards_per_deal": 3,
    "deals_per_hand": 6,
    "shuffle_rounds": [1, 19],
    "redeal_rounds_hand1": [4, 7, 10, 13, 16],
    "redeal_rounds_hand2": [22, 25, 28, 31, 34],
    "final_play_rounds": [18, 36],
    "scopa_points": 1,
    "most_cards_points": 1,
    "cards_tie_count": 20,
    "most_coins_points": 1,
    "coins_tie_count": 5,
    "seven_of_coins_points": 1,
    "most_sevens_points": 1,
    "no_capturer": 0
  },
  "attributes": {
    "player": [
      {"key": "hand", "type": "list", "visible": "ally", "initial": [], "meaning": "Cards held privately, as codes such as '7Co' (rank 1-10 plus suit Co=Coins, Cu=Cups, Sw=Swords, Cl=Clubs).", "observable": false},
      {"key": "captures", "type": "list", "visible": "public", "initial": [], "meaning": "This hand's capture pile. Captures are public.", "observable": false},
      {"key": "scopa_points", "type": "number", "visible": "public", "initial": 0, "meaning": "Scopas scored in the current hand.", "observable": false},
      {"key": "played_card", "type": "text", "visible": "public", "initial": "", "meaning": "Card chosen this turn.", "observable": false},
      {"key": "declared", "type": "list", "visible": "public", "initial": [], "meaning": "Table cards declared as captured this turn; may be empty.", "observable": false},
      {"key": "score", "type": "number", "visible": "public", "initial": 0, "meaning": "Total points across both hands.", "observable": true},
      {"key": "total_cards", "type": "number", "visible": "public", "initial": 0, "meaning": "Running total of cards captured across both hands.", "observable": true},
      {"key": "total_coins", "type": "number", "visible": "public", "initial": 0, "meaning": "Running total of Coins captured across both hands.", "observable": true}
    ],
    "game": [
      {"key": "deck", "type": "list", "visible": "none", "initial": [], "meaning": "Undealt cards. The order is hidden.", "observable": false},
      {"key": "table_cards", "type": "list", "visible": "public", "initial": [], "meaning": "Face-up cards on the table.", "observable": true},
      {"key": "round", "type": "number", "visible": "public", "initial": 1, "meaning": "Current round, 1 to 36.", "observable": true},
      {"key": "last_capturer", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat of the most recent capture in this hand; 0 if none.", "observable": false},
      {"key": "full_deck", "type": "list", "visible": "none", "initial": ["1Co","2Co","3Co","4Co","5Co","6Co","7Co","8Co","9Co","10Co","1Cu","2Cu","3Cu","4Cu","5Cu","6Cu","7Cu","8Cu","9Cu","10Cu","1Sw","2Sw","3Sw","4Sw","5Sw","6Sw","7Sw","8Sw","9Sw","10Sw","1Cl","2Cl","3Cl","4Cl","5Cl","6Cl","7Cl","8Cl","9Cl","10Cl"], "meaning": "The 40 card codes, used to refill the deck at the start of each hand.", "observable": false}
    ]
  },
  "setup": [
    "Seat 1 is Player A and seat 2 is Player B.",
    "Every player's score, total_cards and total_coins are set to 0, and round is set to 1.",
    "Dealing happens inside the round steps at rounds 1 and 19."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "When round is 1 or 19: deck = full_deck; table_cards, every hand, every captures and every declared are emptied; scopa_points = 0 for each player; last_capturer = 0. Then 4 cards are drawn at random from deck into table_cards, and 3 cards are drawn at random from deck into each player's hand (each draw is removed from deck and appended to its destination)."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When round is in {4,7,10,13,16,22,25,28,31,34}: 3 cards are drawn at random from deck into each player's hand."},
    {"action": "sync", "who": "all players", "answer": null, "effect": "Each player sees their own hand plus the public table_cards, captures, scopa_points, score, total_cards, total_coins and round."},
    {"action": "ask", "who": "the Leader: seat 1 when round <= 18, seat 2 when round >= 19", "answer": "one card from the Leader's own hand", "effect": "Leader.played_card = the chosen card; it is removed from Leader.hand."},
    {"action": "ask", "who": "the Leader", "answer": "short text listing the table card codes captured, separated by spaces, or 'none'", "effect": "Leader.declared = the listed table cards (empty if 'none')."},
    {"action": "update", "who": "the Leader", "answer": null, "judged": "The declaration is legal: if some table card has the same rank as the played card, the declaration names exactly one such table card; otherwise it names either no cards or a set of distinct cards currently on the table whose ranks add up exactly to the played card's rank.", "effect": "If legal and declared is non-empty: the played_card and the declared cards are appended to Leader.captures, the declared cards are removed from table_cards, and last_capturer = Leader's seat; then, if table_cards is empty, Leader.scopa_points += 1. Otherwise (declared is empty, or the declaration is illegal): played_card is appended to table_cards and nothing is captured. The table is told what was played and captured."},
    {"action": "ask", "who": "the Dealer: seat 2 when round <= 18, seat 1 when round >= 19", "answer": "one card from the Dealer's own hand", "effect": "Dealer.played_card = the chosen card; it is removed from Dealer.hand."},
    {"action": "ask", "who": "the Dealer", "answer": "short text listing the table card codes captured, separated by spaces, or 'none'", "effect": "Dealer.declared = the listed table cards (empty if 'none')."},
    {"action": "update", "who": "the Dealer", "answer": null, "judged": "The declaration is legal: if some table card has the same rank as the played card, the declaration names exactly one such table card; otherwise it names either no cards or a set of distinct cards currently on the table whose ranks add up exactly to the played card's rank.", "effect": "If legal and declared is non-empty: the played_card and the declared cards are appended to Dealer.captures, the declared cards are removed from table_cards, and last_capturer = Dealer's seat; then, if table_cards is empty and round is not 18 or 36, Dealer.scopa_points += 1. Otherwise: played_card is appended to table_cards and nothing is captured. The table is told what was played and captured."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When round is 18 or 36: if last_capturer > 0, all table_cards are appended to that seat's captures; otherwise they are discarded. table_cards is emptied. Hand scoring, using this hand's captures: +1 score to the player with strictly more cards; +1 to the player with strictly more cards whose suit is Co; +1 to the holder of '7Co'; +1 to the player with more rank-7 cards, or, if those are tied, more rank-6 cards, and no point if both are tied; each player's score += scopa_points. Each player's total_cards += count(captures) and total_coins += count of Co cards in captures. The hand's results are announced."},
    {"action": "update", "who": "all players", "answer": null, "effect": "round += 1."},
    {"action": "check", "who": "all players", "answer": null, "effect": "End the game if round > 36; otherwise continue to the next round."}
  ],
  "ending": {
    "condition": "round > 36",
    "rank_by": "you.score * 10000 + you.total_cards * 100 + you.total_coins",
    "decided_by": "Most total points across both hands wins. A tie goes to more total captured cards, then to more total captured Coins. If still tied, both players share the result (a draw)."
  },
  "rules": [
    {"id": "R1", "text": "When round is 1 or 19, then the deck is refilled to all 40 cards, 4 random cards go to table_cards, and each player's hand receives 3 random cards from the deck."},
    {"id": "R2", "text": "When round is 4, 7, 10, 13, 16, 22, 25, 28, 31 or 34, then each player receives 3 cards from the deck into their hand."},
    {"id": "R3", "text": "When round <= 18, then seat 1 plays first (Leader) and seat 2 plays second (Dealer); when round >= 19, then seat 2 leads and seat 1 deals."},
    {"id": "R4", "text": "When a player plays a card and a table card has the same rank, then the declaration is legal only if it names exactly one such card, and that card plus the played card go to the player's captures."},
    {"id": "R5", "text": "When no table card has the same rank and the declared table cards' ranks sum exactly to the played card's rank, then those cards plus the played card go to the player's captures."},
    {"id": "R6", "text": "When a player declares nothing, then the played card is added to table_cards."},
    {"id": "R7", "text": "When a declaration is illegal (for example, a sum is declared while a same-rank card is on the table, or the ranks do not add up), then the played card is added to table_cards and nothing is captured."},
    {"id": "R8", "text": "When a legal non-empty capture leaves table_cards empty, then the capturer's scopa_points increase by 1, unless it is the Dealer's play in round 18 or 36."},
    {"id": "R9", "text": "When a player makes a legal non-empty capture, then last_capturer is set to that player's seat."},
    {"id": "R10", "text": "When round 18 or 36 ends, then the remaining table_cards go to last_capturer's captures, or are discarded if last_capturer is 0."},
    {"id": "R11", "text": "When a hand is scored, then the player with more captured cards gets 1 point, and nobody gets it at 20-20."},
    {"id": "R12", "text": "When a hand is scored, then the player with more captured Coins gets 1 point, and nobody gets it at 5-5."},
    {"id": "R13", "text": "When a hand is scored, then the player whose captures contain 7Co gets 1 point."},
    {"id": "R14", "text": "When a hand is scored, then the player with more sevens gets 1 point; if sevens are tied, the player with more sixes gets it; if both are tied, nobody does."},
    {"id": "R15", "text": "When a hand is scored, then each player's scopa_points are added to their score, and their captured card count and Coins count are added to total_cards and total_coins."},
    {"id": "R16", "text": "When hand 2 begins at round 19, then captures, scopa_points and last_capturer are reset, while score, total_cards and total_coins are kept."},
    {"id": "R17", "text": "When round 36 is complete, then the game ends and the higher score wins, tie-broken by total_cards and then total_coins; if all three are equal, it is a draw."}
  ],
  "offers": [
    {"question": "Choose a card to play", "who": "the Leader, then the Dealer", "options": "Every card currently in that seat's own hand, and nothing else."},
    {"question": "Declare the table cards you capture", "who": "the Leader, then the Dealer", "options": "Free text: a space-separated list of card codes currently in table_cards, or 'none'. Any declaration may be sent; an illegal one sends the played card to the table and captures nothing."}
  ],
  "choices": [
    {"what": "Exactly 2 players (suggested 2)", "why": "The designer's rules are a duel: fixed Leader/Dealer roles and a 40-card count that assumes exactly two hands of play."},
    {"what": "No pre-play talk step", "why": "This is a zero-sum duel with no coordination; talk would only add words."},
    {"what": "Card codes such as '7Co', '10Sw'", "why": "A compact text form of rank and suit, so suit and rank counts are simple arithmetic."},
    {"what": "Play is split into a card choice and a text declaration", "why": "Choosing from the hand list guarantees a real card; the capture set has too many possible subsets to list as options."},
    {"what": "Seat 1 is Player A, seat 2 is Player B", "why": "The source names players A and B but not seats."},
    {"what": "Leftover cards with no last capturer are not counted for either player", "why": "The source says they are discarded."}
  ],
  "simplifications": [
    {"what": "Capture legality is decided by a judged referee sentence", "why": "Checking for a same-rank card and an exact subset sum over parsed text is too complex for a single arithmetic check. The effects of the ruling are still arithmetic."},
    {"what": "The three-step tie-break is folded into one rank expression: score*10000 + total_cards*100 + total_coins", "why": "rank_by must be a single expression. total_cards and total_coins never reach 100, so the order of the tie-breaks is preserved."},
    {"what": "A complete tie is a shared win", "why": "The engine treats players level at the top as sharing the win, which is equivalent to a draw."}
  ],
  "unsupported": []
}
```
````
