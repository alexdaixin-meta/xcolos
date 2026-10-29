# 21 spec

- time: 2026-10-27T18:19:09+00:00 (57.7s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 a4d64769d6a8c2ec, reply sha256 b06714d0ba6b678b

## Sent

````
Game: Three-Card Wizard
Players in the source: 3 to 3
Suggested table size, chosen by the designer of these rules (keep it): 3

Rules, as filed in the inventory:
CARDS. The deck has 28 cards:
- Red R1-R8, Blue B1-B8 and Green G1-G8 (the suit is the letter, the rank is the number);
- two Wizards, W1 and W2;
- two Jesters, J1 and J2.

SEATS. Players sit in seats 1, 2 and 3. Everyone starts with a score of 0.

STRUCTURE. The game has 12 hands of 3 tricks each. Each round is one trick, so there are 36 rounds.
- The table tracks hand_number (starting at 0) and trick_in_hand (starting at 1).
- Each player has: hand (a list, private to them), bid, tricks_taken, played_card, offer (a list) and score.

RULE 1 (new hand: deal). Only when trick_in_hand = 1:
- add 1 to hand_number;
- shuffle all 28 cards into the deck (this is the round's only random event);
- empty every hand and set every tricks_taken to 0;
- deal the top 3 cards of the deck to seat 1, the next 3 to seat 2 and the next 3 to seat 3, each seen only by its owner;
- remove the 10th card from the deck and place it face up as trump_card, announced to all. After this, 18 cards remain in the deck.

RULE 2 (trump). If trump_card is suited, trump_suit is its suit letter. If it is a Wizard or a Jester, trump_suit is 'none' for the whole hand.

RULE 3 (first leader). Only when trick_in_hand = 1, leader = ((hand_number - 1) mod 3) + 1:
- seat 1 leads in hands 1, 4, 7 and 10;
- seat 2 leads in hands 2, 5, 8 and 11;
- seat 3 leads in hands 3, 6, 9 and 12.

RULE 4 (bidding). Only when trick_in_hand = 1, all three players answer one simultaneous poll.
- The options are exactly the fixed list 0, 1, 2, 3, offered to every seat.
- Each player's answer is stored in their bid exactly as given, and a 0 stays 0.
- Only if an answer is missing or not one of 0, 1, 2, 3 does that bid become 1.
- All bids are then announced. They need not sum to 3.
- Bids are not changed again until Rule 10.

RULE 5 (trick setup). Every round, set:
- led_suit = 'none';
- wizard_played = false;
- best_value = -1;
- best_seat = 0;
- played_cards empty.

RULE 6 (play order). Three players play one card each, one after another:
- first the seat in leader;
- then the seat (leader mod 3) + 1;
- then the seat ((leader + 1) mod 3) + 1.
Each player sees the cards already played to the trick.

RULE 7 (legal cards). Before a player chooses, build their offer list, keeping the order the cards sit in their hand:
- if led_suit is not 'none' and they hold at least one card of led_suit, the offer is their cards of led_suit plus any Wizards and Jesters they hold;
- otherwise, the offer is every card in their hand.
The player picks one card from the offer.

RULE 8 (fallback). If the answer is missing or not in the offer, the engine plays the first card of the offer list.

RULE 9 (resolving each played card). As each card is played, remove it from the hand, record it as played_card and append it to played_cards. Then work out the led suit and the card's strength.

Led suit:
- If the card is suited, led_suit is 'none' and wizard_played is false, then led_suit becomes that card's suit.
- If the card is a Wizard, set wizard_played = true.
- A Wizard or Jester never sets led_suit. Once any Wizard is played, later cards do not set led_suit.

Strength:
- Wizard: 100.
- Suited card whose suit equals trump_suit: 20 + rank.
- Other suited card whose suit equals led_suit: its rank.
- Anything else: 0. This includes Jesters and off-suit non-trump cards.

If strength > best_value (strictly), set best_value = strength and best_seat = this seat. As a result:
- the first Wizard wins the trick;
- otherwise the highest trump wins;
- otherwise the highest card of the led suit wins;
- if all three cards are Jesters, the first Jester wins.

RULE 10 (end of trick). Add 1 to tricks_taken of best_seat, announce the winner, and set leader = best_seat.
- If trick_in_hand = 3, score the hand. A player whose tricks_taken equals their bid gains 20 + 10 × tricks_taken. Otherwise they lose 10 × |tricks_taken - bid|. Announce all scores, then set every bid to 0 and trick_in_hand = 1.
- Otherwise add 1 to trick_in_hand.

RULE 11 (end). The game ends after round 36, which is the end of hand 12.

How the winner is decided: After hand 12, the player with the highest score wins. If two or three players tie for the highest score, the game is a draw.
````

## Reply

````
```json
{
  "name": "Three-Card Wizard",
  "summary": "A three-player trick-taking game of 12 hands with 3 tricks each: players bid exactly how many tricks they will take, then play Wizards, Jesters and suited cards to hit that number.",
  "players": {"min": 3, "max": 3, "suggested": 3},
  "parameters": {
    "deck_size": 28,
    "suits": 3,
    "ranks_per_suit": 8,
    "wizards": 2,
    "jesters": 2,
    "hands": 12,
    "tricks_per_hand": 3,
    "rounds": 36,
    "cards_dealt_per_player": 3,
    "trump_card_position": 10,
    "cards_left_in_deck_after_deal": 18,
    "bid_min": 0,
    "bid_max": 3,
    "default_bid": 1,
    "wizard_strength": 100,
    "trump_strength_bonus": 20,
    "jester_or_offsuit_strength": 0,
    "initial_best_value": -1,
    "exact_bid_bonus": 20,
    "points_per_trick_when_exact": 10,
    "penalty_per_trick_off": 10,
    "starting_score": 0,
    "starting_hand_number": 0,
    "starting_trick_in_hand": 1
  },
  "attributes": {
    "player": [
      {"key": "hand", "type": "list", "visible": "ally", "initial": [], "meaning": "The cards this player holds in the current hand. Only the owner sees them.", "observable": false},
      {"key": "bid", "type": "number", "visible": "public", "initial": 0, "meaning": "The number of tricks bid this hand. It is collected by a simultaneous poll and then announced, and it is reset to 0 after scoring.", "observable": true},
      {"key": "tricks_taken", "type": "number", "visible": "public", "initial": 0, "meaning": "Tricks won so far in the current hand.", "observable": true},
      {"key": "played_card", "type": "text", "visible": "public", "initial": "", "meaning": "The card this player played to the current trick.", "observable": false},
      {"key": "offer", "type": "list", "visible": "ally", "initial": [], "meaning": "The legal cards this player may play now, in hand order.", "observable": false},
      {"key": "score", "type": "number", "visible": "public", "initial": 0, "meaning": "Cumulative score.", "observable": true}
    ],
    "game": [
      {"key": "deck", "type": "list", "visible": "none", "initial": ["R1","R2","R3","R4","R5","R6","R7","R8","B1","B2","B3","B4","B5","B6","B7","B8","G1","G2","G3","G4","G5","G6","G7","G8","W1","W2","J1","J2"], "meaning": "The undealt cards, refilled with all 28 cards and shuffled at the start of each hand.", "observable": false},
      {"key": "trump_card", "type": "text", "visible": "public", "initial": "", "meaning": "The face-up 10th card of the shuffled deck.", "observable": true},
      {"key": "trump_suit", "type": "text", "visible": "public", "initial": "none", "meaning": "The suit letter of trump_card, or 'none' if it is a Wizard or a Jester.", "observable": false},
      {"key": "hand_number", "type": "number", "visible": "public", "initial": 0, "meaning": "The current hand, 1 to 12.", "observable": true},
      {"key": "trick_in_hand", "type": "number", "visible": "public", "initial": 1, "meaning": "The current trick within the hand, 1 to 3.", "observable": false},
      {"key": "leader", "type": "number", "visible": "public", "initial": 1, "meaning": "The seat that leads the current trick.", "observable": false},
      {"key": "led_suit", "type": "text", "visible": "public", "initial": "none", "meaning": "The suit led in this trick, or 'none'.", "observable": false},
      {"key": "wizard_played", "type": "bool", "visible": "public", "initial": false, "meaning": "Whether a Wizard has been played in this trick.", "observable": false},
      {"key": "best_value", "type": "number", "visible": "public", "initial": -1, "meaning": "The strength of the currently winning card in the trick.", "observable": false},
      {"key": "best_seat", "type": "number", "visible": "public", "initial": 0, "meaning": "The seat currently winning the trick.", "observable": false},
      {"key": "played_cards", "type": "list", "visible": "public", "initial": [], "meaning": "The cards played to the current trick, in order.", "observable": false}
    ]
  },
  "setup": [
    "Seats 1, 2 and 3 are filled, and every score is set to 0.",
    "hand_number is set to 0, trick_in_hand to 1 and every bid to 0.",
    "The deck list holds the 28 cards R1-R8, B1-B8, G1-G8, W1, W2, J1 and J2."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "When trick_in_hand = 1: add 1 to hand_number; refill deck with all 28 cards and shuffle it; empty every hand and set every tricks_taken to 0; draw 3 cards at random from deck into seat 1's hand, then 3 into seat 2's, then 3 into seat 3's (each removed from deck); remove the next random card from deck and set it as trump_card (18 cards stay in deck); set trump_suit to the suit letter of trump_card if it is suited, otherwise 'none'; set leader = ((hand_number - 1) mod 3) + 1."},
    {"action": "sync", "who": "all players", "answer": null, "effect": "When trick_in_hand = 1: each player sees their own hand; trump_card, trump_suit, hand_number and leader are announced to all."},
    {"action": "poll", "who": "all players", "answer": "one of 0, 1, 2, 3", "effect": "When trick_in_hand = 1: each player's bid is set to their answer exactly (a 0 stays 0); a missing or invalid answer sets that bid to 1. All bids are then announced."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Every round: led_suit = 'none', wizard_played = false, best_value = -1, best_seat = 0, played_cards = []."},
    {"action": "update", "who": "seat leader", "answer": null, "effect": "Build the leader's offer from their hand, in hand order: if led_suit != 'none' and they hold a card of led_suit, the offer is those cards plus any W or J cards they hold; otherwise it is the whole hand."},
    {"action": "ask", "who": "seat leader", "answer": "one card from their offer", "effect": "The chosen card is removed from hand, set as played_card and appended to played_cards; a missing or invalid answer plays offer[0]."},
    {"action": "update", "who": "seat leader", "answer": null, "effect": "Resolve the card. If it is suited and led_suit = 'none' and wizard_played = false, set led_suit to its suit. If it is a Wizard, set wizard_played = true. Strength is 100 for a Wizard, 20 + rank for a suit equal to trump_suit, rank for a suit equal to led_suit, and 0 otherwise. If strength > best_value, set best_value = strength and best_seat = this seat. The played card is announced."},
    {"action": "update", "who": "seat (leader mod 3) + 1", "answer": null, "effect": "Build this player's offer with the same rule as above."},
    {"action": "ask", "who": "seat (leader mod 3) + 1", "answer": "one card from their offer", "effect": "The player sees played_cards. The chosen card is removed from hand, set as played_card and appended to played_cards; a missing or invalid answer plays offer[0]."},
    {"action": "update", "who": "seat (leader mod 3) + 1", "answer": null, "effect": "Resolve the card with the same led-suit and strength rule as above, then announce it."},
    {"action": "update", "who": "seat ((leader + 1) mod 3) + 1", "answer": null, "effect": "Build this player's offer with the same rule as above."},
    {"action": "ask", "who": "seat ((leader + 1) mod 3) + 1", "answer": "one card from their offer", "effect": "The player sees played_cards. The chosen card is removed from hand, set as played_card and appended to played_cards; a missing or invalid answer plays offer[0]."},
    {"action": "update", "who": "seat ((leader + 1) mod 3) + 1", "answer": null, "effect": "Resolve the card with the same led-suit and strength rule as above, then announce it."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Add 1 to tricks_taken of best_seat; announce best_seat as the trick winner; set leader = best_seat."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When trick_in_hand = 3: for each player, if tricks_taken = bid, add 20 + 10 * tricks_taken to score; otherwise subtract 10 * |tricks_taken - bid|. Announce all scores, set every bid to 0 and set trick_in_hand = 1. Otherwise (trick_in_hand < 3) add 1 to trick_in_hand."},
    {"action": "check", "who": "all players", "answer": null, "effect": "End the game if hand_number >= 12 and trick_in_hand = 1 (hand 12 has just been scored); otherwise continue to the next round."}
  ],
  "ending": {
    "condition": "game.hand_number >= 12 and game.trick_in_hand = 1",
    "rank_by": "you.score",
    "decided_by": "Each player's standing is their final score after hand 12. The highest score wins, and players tied at the top share the win (the source calls this a draw)."
  },
  "rules": [
    {"id": "R1", "text": "When trick_in_hand = 1 at the start of a round, then hand_number increases by 1, the deck is refilled to 28 cards and shuffled, every tricks_taken becomes 0, and each seat receives exactly 3 cards in its hand."},
    {"id": "R2", "text": "When a hand is dealt, then one further card is removed from the deck and becomes trump_card, leaving exactly 18 cards in the deck."},
    {"id": "R3", "text": "When trump_card is suited (for example G5), then trump_suit is its letter (G); when trump_card is W1, W2, J1 or J2, then trump_suit is 'none'."},
    {"id": "R4", "text": "When a hand begins, then leader = ((hand_number - 1) mod 3) + 1: seat 1 leads in hands 1, 4, 7 and 10, seat 2 in hands 2, 5, 8 and 11, and seat 3 in hands 3, 6, 9 and 12."},
    {"id": "R5", "text": "When trick_in_hand = 1, then all three players bid at once from {0, 1, 2, 3}, and each bid is stored exactly as given (a 0 stays 0)."},
    {"id": "R6", "text": "When a bid answer is missing or not in {0, 1, 2, 3}, then that bid is 1."},
    {"id": "R7", "text": "When bidding is done, then all bids are announced, and they need not sum to 3."},
    {"id": "R8", "text": "When a trick starts, then led_suit = 'none', wizard_played = false, best_value = -1, best_seat = 0 and played_cards is empty."},
    {"id": "R9", "text": "When a trick is played, then the order is leader, then (leader mod 3) + 1, then ((leader + 1) mod 3) + 1."},
    {"id": "R10", "text": "When led_suit is not 'none' and the player holds a card of led_suit, then the offer is their led-suit cards plus any Wizards and Jesters they hold, in hand order; otherwise the offer is the whole hand."},
    {"id": "R11", "text": "When a play answer is missing or not in the offer, then the first card of the offer is played."},
    {"id": "R12", "text": "When a card is played, then it is removed from the hand, recorded as played_card and appended to played_cards."},
    {"id": "R13", "text": "When a suited card is played while led_suit = 'none' and wizard_played = false, then led_suit becomes its suit."},
    {"id": "R14", "text": "When a Wizard is played, then wizard_played = true and led_suit does not change; when a Jester is played, then led_suit does not change."},
    {"id": "R15", "text": "When a card is played, then its strength is 100 for a Wizard, 20 + rank for a trump-suit card, its rank for a led-suit card, and 0 for a Jester or an off-suit non-trump card."},
    {"id": "R16", "text": "When a card's strength is strictly greater than best_value, then best_value becomes that strength and best_seat becomes that seat; equal strength does not take the lead, so the first Wizard wins and three Jesters are won by the first Jester."},
    {"id": "R17", "text": "When a trick ends, then best_seat's tricks_taken increases by 1 and leader becomes best_seat."},
    {"id": "R18", "text": "When trick_in_hand = 3 at the end of a trick and a player's tricks_taken equals their bid, then they gain 20 + 10 * tricks_taken (for example bid 0 and 0 tricks gains 20, bid 2 and 2 tricks gains 40)."},
    {"id": "R19", "text": "When trick_in_hand = 3 at the end of a trick and a player's tricks_taken differs from their bid, then they lose 10 * |tricks_taken - bid| (for example bid 3 and 1 trick loses 20)."},
    {"id": "R20", "text": "When a hand is scored, then all scores are announced, every bid is set to 0 and trick_in_hand becomes 1; after tricks 1 and 2 of a hand, trick_in_hand increases by 1 instead."},
    {"id": "R21", "text": "When hand 12 has been scored (after round 36), then the game ends and the highest score wins, with players tied at the top sharing the win."}
  ],
  "offers": [
    {"question": "Bid for this hand (poll, only when trick_in_hand = 1)", "who": "seats 1, 2 and 3", "options": "every seat: 0, 1, 2, 3"},
    {"question": "Card to play to the trick", "who": "the leader, then (leader mod 3) + 1, then ((leader + 1) mod 3) + 1", "options": "the leader, or any later player when led_suit is 'none' (a Wizard was led, or only Wizards and Jesters have been played so far): every card in their hand; a later player when led_suit is set and they hold a card of led_suit: their led-suit cards plus any W1, W2, J1, J2 they hold; a later player when led_suit is set and they hold none of it: every card in their hand"}
  ],
  "choices": [
    {"what": "Exactly 3 players, suggested 3", "why": "The designer fixed 3 seats. The deal (9 cards plus the 10th as trump), the leader rotation mod 3 and the play order all assume three players. The game is about predicting tricks and managing the trick count against two rivals whose bids are public."},
    {"what": "Strategy at the table", "why": "A thoughtful player bids from card strength and the trump suit, then plays to hit the bid exactly: dumping Jesters or low cards to avoid tricks, spending Wizards or trumps to take them, and reading the opponents' public bids to disrupt them. A thoughtless player bids blindly and plays cards in any order."},
    {"what": "No talk step", "why": "The source has no table talk, and adding it would add a mechanic."},
    {"what": "Shuffle and deal written as random draws from the deck list", "why": "The engine shuffles by drawing at random; drawing 9 cards and then one more for trump matches 'top 3 to each seat, the 10th is trump'."},
    {"what": "The bid and tricks_taken are public attributes", "why": "The rules announce bids after the simultaneous poll and announce each trick winner, so both are open information. The poll keeps bids secret until all are in."}
  ],
  "simplifications": [
    {"what": "The source's 'draw' when two or three players tie for the top score becomes a shared win", "why": "The engine ranks by one expression and players level at the top share the win; there is no separate draw outcome."},
    {"what": "Each of the three plays is written as three steps (build offer, ask, resolve) addressed to the computed seat", "why": "The engine runs a flat list of steps; play order is expressed by naming the seat from leader."},
    {"what": "Hand-start steps carry a 'when trick_in_hand = 1' condition, and scoring carries 'when trick_in_hand = 3'", "why": "Single steps may be conditional, so no block substitution is needed."}
  ],
  "unsupported": []
}
```
````
