# 03 spec

- time: 2026-10-27T20:43:50+00:00 (51.6s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 124c88f6d0e633d4, reply sha256 68291598350304a9

## Sent

````
Game: Skull King: Three-Card Raids
Players in the source: 3 to 3
Suggested table size, chosen by the designer of these rules (keep it): 3

Rules, as filed in the inventory:
PLAYERS AND DECK. 3 players, seats 1, 2 and 3. The deck has 25 cards: Green 1-7 (7 cards), Yellow 1-7 (7 cards), Black 1-5 (5 cards), 2 Pirates, 2 Escapes, 1 Mermaid and 1 Skull King. Green, Yellow and Black are the suited cards. Pirates, Escapes, the Mermaid and the Skull King are special cards.

STRUCTURE. The game has 9 hands of 3 tricks each, so 27 rounds; each round is one trick. Each player's score starts at 0.

START OF EACH HAND (first trick of the hand only). Shuffle all 25 cards and deal 3 to each player, face down. Each player sees only their own cards. The other 16 cards are set aside unseen. All players then bid at the same moment, each secretly choosing a whole number from 0 to 3: the number of tricks they will win this hand. All bids are then revealed to everyone. The first leader of hand h is seat ((h-1) mod 3) + 1, so hands 1, 4 and 7 are led by seat 1, hands 2, 5 and 8 by seat 2, and hands 3, 6 and 9 by seat 3.

PLAYING A TRICK. The leader plays one card face up, then the next seat clockwise (1 to 2, 2 to 3, 3 to 1), then the third player.
- Lead suit: the suit of the first suited card played in the trick. If special cards are played before any suited card, the lead suit is set by the first suited card that follows. If no suited card is played, there is no lead suit.
- Following: once a lead suit exists, a player who holds a card of that suit must play either a card of that suit or a special card. A player with no card of that suit may play any card. Special cards may always be played.
- The engine offers each player only the cards they may legally play.

WINNING A TRICK. Check these in order:
(1) If the trick contains both the Skull King and the Mermaid, the Mermaid wins.
(2) Otherwise, if it contains the Skull King, the Skull King wins.
(3) Otherwise, if it contains a Pirate, the first Pirate played wins.
(4) Otherwise, if it contains the Mermaid, the Mermaid wins.
(5) Otherwise, if it contains any Black card, the highest Black card wins.
(6) Otherwise, if there is a lead suit, the highest card of the lead suit wins.
(7) Otherwise (all Escapes), the first card played wins.

The player who played the winning card wins the trick, adds 1 to their trick count for this hand and leads the next trick of the hand. Capture bonuses are recorded for the trick winner: +30 for each Pirate in a trick won by the Skull King, and +40 if the Mermaid wins a trick containing the Skull King. The winner, the cards played and any bonus are announced to everyone.

END OF EACH HAND (after the third trick). Each player scores:
- Exact bid of 1, 2 or 3: +20 per trick bid, plus all capture bonuses they recorded this hand.
- Exact bid of 0: +20, plus any capture bonuses they recorded this hand (normally none).
- Missed bid of 0: -20, and bonuses are lost.
- Missed bid of 1, 2 or 3: -10 per trick of difference between bid and tricks won, and bonuses are lost.

Scores are announced. Trick counts and bonuses reset to 0 for the next hand.

END OF GAME. After hand 9 (round 27), the game ends.

How the winner is decided: After 9 hands the player with the highest total score wins. If two or three players tie for the highest total, the game is a draw among the tied players.
````

## Reply

````
```json
{
  "name": "Skull King: Three-Card Raids",
  "summary": "Three players play 9 hands of 3 tricks each. Before each hand every player secretly bids how many tricks they will win, then scores for hitting the bid exactly and loses points for missing it, with bonuses for capturing Pirates or the Skull King.",
  "players": {"min": 3, "max": 3, "suggested": 3},
  "parameters": {
    "player_count": 3,
    "deck_size": 25,
    "green_cards": 7,
    "green_max_rank": 7,
    "yellow_cards": 7,
    "yellow_max_rank": 7,
    "black_cards": 5,
    "black_max_rank": 5,
    "pirates": 2,
    "escapes": 2,
    "mermaids": 1,
    "skull_kings": 1,
    "hands": 9,
    "tricks_per_hand": 3,
    "total_rounds": 27,
    "cards_dealt_per_player": 3,
    "cards_set_aside": 16,
    "bid_min": 0,
    "bid_max": 3,
    "exact_bid_points_per_trick": 20,
    "exact_zero_bid_points": 20,
    "missed_zero_bid_points": -20,
    "missed_bid_points_per_trick_difference": -10,
    "pirate_captured_by_skull_king_bonus": 30,
    "skull_king_captured_by_mermaid_bonus": 40,
    "trick_win_increment": 1,
    "starting_score": 0
  },
  "attributes": {
    "player": [
      {"key": "score", "type": "number", "visible": "public", "initial": 0, "meaning": "Total score across all hands.", "observable": true},
      {"key": "hand", "type": "list", "visible": "ally", "initial": [], "meaning": "Cards the player holds this hand; only the owner sees them.", "observable": false},
      {"key": "bid", "type": "number", "visible": "public", "initial": 0, "meaning": "Tricks the player bid for the current hand (0-3). Chosen secretly, then revealed.", "observable": true},
      {"key": "tricks_won", "type": "number", "visible": "public", "initial": 0, "meaning": "Tricks won so far this hand.", "observable": true},
      {"key": "bonus", "type": "number", "visible": "public", "initial": 0, "meaning": "Capture bonuses recorded this hand. Paid only if the bid is exact.", "observable": false},
      {"key": "played_card", "type": "text", "visible": "public", "initial": "", "meaning": "The card this player played in the current trick.", "observable": false}
    ],
    "game": [
      {"key": "deck", "type": "list", "visible": "none", "initial": ["G1","G2","G3","G4","G5","G6","G7","Y1","Y2","Y3","Y4","Y5","Y6","Y7","B1","B2","B3","B4","B5","Pirate","Pirate","Escape","Escape","Mermaid","SkullKing"], "meaning": "The 25-card deck. After dealing, the 16 undealt cards stay here, set aside unseen.", "observable": false},
      {"key": "round", "type": "number", "visible": "public", "initial": 1, "meaning": "Current trick number in the game (1-27).", "observable": false},
      {"key": "hand_number", "type": "number", "visible": "public", "initial": 1, "meaning": "Current hand (1-9).", "observable": false},
      {"key": "trick_in_hand", "type": "number", "visible": "public", "initial": 1, "meaning": "Which trick of the hand is being played (1-3).", "observable": false},
      {"key": "leader", "type": "number", "visible": "public", "initial": 1, "meaning": "Seat that leads the current trick.", "observable": false},
      {"key": "lead_suit", "type": "text", "visible": "public", "initial": "", "meaning": "Suit of the first suited card in the trick (Green, Yellow or Black). Empty if no suited card has been played yet.", "observable": false},
      {"key": "trick_cards", "type": "list", "visible": "public", "initial": [], "meaning": "Cards played to the current trick, in play order, each tagged with the seat that played it.", "observable": false},
      {"key": "trick_winner", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat that won the most recent trick.", "observable": false}
    ]
  },
  "setup": [
    "Seats 1, 2 and 3 are seated clockwise (1 to 2, 2 to 3, 3 to 1).",
    "Every player's score is set to 0.",
    "The deck list holds all 25 cards: G1-G7, Y1-Y7, B1-B5, 2 Pirate, 2 Escape, 1 Mermaid, 1 SkullKing.",
    "round = 1, hand_number = 1, trick_in_hand = 1, leader = 1."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "When trick_in_hand == 1: return every card in each player's hand and in trick_cards to deck. Then, for each player, draw 3 cards at random from deck into their hand (remove from deck, append to hand); the 16 cards left in deck are set aside unseen. Set each player's bid = 0, tricks_won = 0, bonus = 0. Set leader = ((hand_number - 1) mod 3) + 1."},
    {"action": "sync", "who": "all players", "answer": null, "effect": "When trick_in_hand == 1: each player is sent their own hand. Nobody sees another player's hand."},
    {"action": "poll", "who": "all players", "answer": "a whole number from 0 to 3", "effect": "When trick_in_hand == 1: each player's bid is set to their answer. No bid is shown until all are in."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "When trick_in_hand == 1: announce every seat's bid for hand {hand_number} and the first leader, seat {leader}."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Set trick_cards = [], lead_suit = '', and each player's played_card = ''."},
    {"action": "ask", "who": "each player in turn, starting with seat leader and going clockwise", "answer": "one card from the player's hand that is legal to play (see offers)", "effect": "Remove the chosen card from the player's hand, append it (with the seat) to trick_cards, and set played_card. If lead_suit == '' and the card is Green, Yellow or Black, set lead_suit to that suit. Each player hears the cards played before them."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Set trick_winner to the seat holding the first applicable card: (1) if trick_cards holds both SkullKing and Mermaid, the Mermaid; (2) else the SkullKing; (3) else the first Pirate played; (4) else the Mermaid; (5) else the highest Black card; (6) else, if lead_suit is not empty, the highest card of lead_suit; (7) else (all Escapes) the first card played. Add 1 to the winner's tricks_won. If the winning card is the SkullKing, add 30 to the winner's bonus for each Pirate in trick_cards. If the winning card is the Mermaid and trick_cards holds the SkullKing, add 40 to the winner's bonus. Set leader = trick_winner."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce the cards played (trick_cards), the trick_winner seat and any bonus just recorded."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When trick_in_hand == 3, for each player: if bid >= 1 and tricks_won == bid, score += 20 * bid + bonus; if bid == 0 and tricks_won == 0, score += 20 + bonus; if bid == 0 and tricks_won > 0, score -= 20; if bid >= 1 and tricks_won != bid, score -= 10 * |bid - tricks_won|. Then set tricks_won = 0 and bonus = 0."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "When trick_in_hand == 3: announce every seat's score after hand {hand_number}."},
    {"action": "update", "who": "all players", "answer": null, "effect": "round += 1. If trick_in_hand == 3, then hand_number += 1 and trick_in_hand = 1; otherwise trick_in_hand += 1."},
    {"action": "check", "who": "all players", "answer": null, "effect": "End the game if round > 27; otherwise continue with the next round."}
  ],
  "ending": {
    "condition": "round > 27",
    "rank_by": "you.score",
    "decided_by": "Each player's standing is their total score after 9 hands. The highest score wins, and players tied for the highest share the win (a draw among them)."
  },
  "rules": [
    {"id": "R1", "text": "When a hand starts (trick_in_hand == 1), then each of the 3 players is dealt 3 cards at random from the 25-card deck into their hand, and the 16 undealt cards stay in deck unseen."},
    {"id": "R2", "text": "When cards are dealt, then each player sees only their own hand."},
    {"id": "R3", "text": "When a hand starts, then all players bid at the same time, each a whole number from 0 to 3, and all bids are revealed only after everyone has bid."},
    {"id": "R4", "text": "When hand h starts, then its first leader is seat ((h-1) mod 3) + 1: seat 1 for hands 1, 4 and 7, seat 2 for hands 2, 5 and 8, and seat 3 for hands 3, 6 and 9."},
    {"id": "R5", "text": "When a trick is played, then the leader plays first, then the next seat clockwise, then the third seat, each playing one card face up from their hand."},
    {"id": "R6", "text": "When the first suited card (Green, Yellow or Black) is played in a trick, then its suit becomes the lead suit, even if special cards were played before it."},
    {"id": "R7", "text": "When no suited card is played in a trick, then the trick has no lead suit."},
    {"id": "R8", "text": "When a lead suit exists and a player holds a card of that suit, then they are offered only cards of that suit and special cards."},
    {"id": "R9", "text": "When a player holds no card of the lead suit, or there is no lead suit yet, then they are offered every card in their hand."},
    {"id": "R10", "text": "When a trick contains both the Skull King and the Mermaid, then the Mermaid wins it."},
    {"id": "R11", "text": "When a trick contains the Skull King and no Mermaid, then the Skull King wins it."},
    {"id": "R12", "text": "When a trick contains no Skull King and at least one Pirate, then the first Pirate played wins it."},
    {"id": "R13", "text": "When a trick contains the Mermaid but no Skull King and no Pirate, then the Mermaid wins it."},
    {"id": "R14", "text": "When a trick contains no Skull King, Pirate or Mermaid but at least one Black card, then the highest Black card wins it."},
    {"id": "R15", "text": "When a trick contains no special card that wins and no Black card, then the highest card of the lead suit wins it."},
    {"id": "R16", "text": "When a trick contains only Escapes, then the first card played wins it."},
    {"id": "R17", "text": "When a player wins a trick, then their tricks_won rises by 1 and they lead the next trick of the hand."},
    {"id": "R18", "text": "When the Skull King wins a trick, then its player's bonus rises by 30 for each Pirate in that trick."},
    {"id": "R19", "text": "When the Mermaid wins a trick containing the Skull King, then its player's bonus rises by 40."},
    {"id": "R20", "text": "When a trick ends, then its cards, its winner and any bonus are announced to everyone."},
    {"id": "R21", "text": "When a hand ends and a player bid 1, 2 or 3 and won exactly that many tricks, then they score +20 per trick bid plus their bonus (for example, bid 2 and won 2 scores +40 plus bonus)."},
    {"id": "R22", "text": "When a hand ends and a player bid 0 and won 0 tricks, then they score +20 plus their bonus."},
    {"id": "R23", "text": "When a hand ends and a player bid 0 but won at least 1 trick, then they score -20 and lose their bonus."},
    {"id": "R24", "text": "When a hand ends and a player bid 1, 2 or 3 but missed, then they score -10 per trick of difference and lose their bonus (for example, bid 3 and won 1 scores -20)."},
    {"id": "R25", "text": "When a hand ends, then scores are announced and every player's tricks_won and bonus reset to 0."},
    {"id": "R26", "text": "When round 27 (the third trick of hand 9) has been scored, then the game ends."},
    {"id": "R27", "text": "When the game ends, then the player with the highest score wins, and players tied for the highest share the win."}
  ],
  "offers": [
    {"question": "Bid at the start of a hand", "who": "all seats, at once", "options": "0, 1, 2 or 3"},
    {"question": "Card to play in a trick", "who": "each seat in turn, starting with the leader", "options": "If lead_suit is empty (the player leads, or only special cards have been played so far): every card in their hand. If lead_suit is set and the player holds at least one card of that suit: only their cards of the lead suit plus any Pirate, Escape, Mermaid or SkullKing they hold. If lead_suit is set and the player holds no card of that suit: every card in their hand."}
  ],
  "choices": [
    {"what": "Exactly 3 players, suggested 3", "why": "The designer fixed the game at 3 seats, and the 25-card deck, the 3-card deal and the clockwise leader rotation are all built for 3. Minimum and maximum are both 3."},
    {"what": "No free-talk step before bids or plays", "why": "The source has no talk. Strategy comes from reading the revealed bids and the cards played (whether to win or duck a trick to land your own bid, or to spoil a rival's), so added talk would only add words."},
    {"what": "One trick per round, with the deal, bid and scoring steps run only when trick_in_hand is 1 or 3", "why": "The source sets each round to one trick (27 rounds). Single-step 'when' conditions keep the step list flat."},
    {"what": "Ties at the top share the win", "why": "The source calls a top tie a draw among the tied players, which is exactly a shared win."}
  ],
  "simplifications": [
    {"what": "The 16 undealt cards stay in the deck list rather than a separate set-aside pile", "why": "They are unseen and unused until the next hand's reshuffle, so a separate list adds nothing."},
    {"what": "Card play uses ask in seat order starting from the leader", "why": "Tricks are sequential in the source; each later player must see the earlier cards to follow suit."}
  ],
  "unsupported": []
}
```
````
