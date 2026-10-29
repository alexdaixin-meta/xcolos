# 25 spec

- time: 2026-10-27T21:22:52+00:00 (49.1s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 aed132ce32fa059a, reply sha256 51b76ae9aef1b1b9

## Sent

````
Game: Wizard Duel of Three
Players in the source: 3 to 3
Suggested table size, chosen by the designer of these rules (keep it): 3

Rules, as filed in the inventory:
DECK (32 cards). Four suits, Red, Blue, Green and Yellow, each numbered 1 to 7 (28 cards), plus 2 Wizards and 2 Jesters.

STRUCTURE. The game has 6 hands. Each hand has 5 tricks, and each trick is one game round, so the game lasts exactly 30 rounds. Seats are 1, 2 and 3. The dealer of hand 1 is seat 1, and the dealer moves to the next seat (1, then 2, then 3, then 1) each hand.

START OF A HAND (first trick of each hand only).
(a) The deck is rebuilt from all 32 cards and shuffled. This is the round's single random event.
(b) Each player receives 5 cards, kept privately.
(c) The next card is turned face up and announced. If it is a numbered card, its suit is trump for this hand. If it is a Wizard or a Jester, there is no trump this hand.
(d) The 16 remaining cards are not used this hand and nobody sees them.
(e) Each player's bid and tricks taken are reset to 0.
(f) All three players, at the same moment and without seeing each other's choice, bid how many of the 5 tricks they will take: 0, 1, 2, 3, 4 or 5. The bids need not add up to 5.
(g) All bids are then announced, one message per player.
The player after the dealer leads the first trick.

EACH TRICK.
(1) The led suit is reset to none and the trick is empty.
(2) The leader plays any one card from their hand, face up.
(3) The next player in seat order plays any one card from their hand.
(4) The third player plays any one card from their hand.
There is no obligation to follow suit: any card in hand may always be played.
The led suit is the suit of the first numbered card played in the trick. A Jester played before it does not set the suit. If a Wizard is the first card played, the trick has no led suit, and that Wizard wins.

WHO WINS THE TRICK.
- If any Wizard was played, the first Wizard played wins.
- Otherwise, if any trump was played, the highest trump wins.
- Otherwise, the highest card of the led suit wins.
- If all three cards are Jesters, the first Jester played wins.
Numbered cards not of the led suit and not trump can never win. Every card is unique, so there are no ties.
The winner's tricks taken increases by 1 and is announced, and the winner leads the next trick.

END OF A HAND (after the fifth trick).
Each player's score changes:
- If tricks taken equals the bid exactly, the player gains 20 + 10 x tricks taken.
- Otherwise, the player loses 10 x |bid - tricks taken|.
Each player's trick count and new score are announced in separate messages, then the dealer moves to the next seat.

INFORMATION. You see your own hand, the turned trump card, all revealed bids, every card played so far, and all scores. You never see other players' hands or the unused cards.

No discussion phase.

END. After the 30th trick (the end of hand 6), the game ends.

How the winner is decided: After 6 hands (30 tricks), the player with the highest score wins. If two or three players tie for the highest score, those players share the win and the game is a draw.
````

## Reply

````
```json
{
  "name": "Wizard Duel of Three",
  "summary": "A three-player trick-taking game of 6 hands of 5 tricks. Players bid how many tricks they will take and score for exact bids, using Wizards, Jesters and a turned trump suit.",
  "players": {"min": 3, "max": 3, "suggested": 3},
  "parameters": {
    "num_hands": 6,
    "tricks_per_hand": 5,
    "total_rounds": 30,
    "deck_size": 32,
    "num_suits": 4,
    "max_rank": 7,
    "numbered_cards": 28,
    "num_wizards": 2,
    "num_jesters": 2,
    "hand_size": 5,
    "unused_cards_per_hand": 16,
    "bid_min": 0,
    "bid_max": 5,
    "exact_bid_bonus": 20,
    "exact_bid_per_trick": 10,
    "miss_penalty_per_trick": 10,
    "first_dealer_seat": 1,
    "trick_win_increment": 1
  },
  "attributes": {
    "player": [
      {"key": "hand", "type": "list", "visible": "ally", "initial": [], "meaning": "The cards the player holds this hand, coded as text (R1..R7, B1..B7, G1..G7, Y1..Y7, W1, W2, J1, J2).", "observable": false},
      {"key": "bid", "type": "number", "visible": "public", "initial": 0, "meaning": "Tricks bid this hand, revealed after the simultaneous bid.", "observable": true},
      {"key": "tricks_taken", "type": "number", "visible": "public", "initial": 0, "meaning": "Tricks won so far this hand.", "observable": true},
      {"key": "score", "type": "number", "visible": "public", "initial": 0, "meaning": "Running score.", "observable": true},
      {"key": "played_card", "type": "text", "visible": "public", "initial": "", "meaning": "The card this player played to the current trick.", "observable": false}
    ],
    "game": [
      {"key": "deck", "type": "list", "visible": "none", "initial": [], "meaning": "The 32-card deck, rebuilt and drawn from at the start of each hand. The cards left in it after the deal are the 16 unused cards.", "observable": false},
      {"key": "trump_card", "type": "text", "visible": "public", "initial": "", "meaning": "The card turned face up after the deal.", "observable": true},
      {"key": "trump_suit", "type": "text", "visible": "public", "initial": "none", "meaning": "The suit letter of trump_card if it is numbered, otherwise none.", "observable": false},
      {"key": "led_suit", "type": "text", "visible": "public", "initial": "none", "meaning": "The suit of the first numbered card played in the trick, or none.", "observable": false},
      {"key": "trick_cards", "type": "list", "visible": "public", "initial": [], "meaning": "The cards played to the current trick, in order of play.", "observable": false},
      {"key": "played_history", "type": "list", "visible": "public", "initial": [], "meaning": "Every card played so far this hand.", "observable": false},
      {"key": "dealer", "type": "number", "visible": "public", "initial": 1, "meaning": "The dealer seat for the current hand.", "observable": false},
      {"key": "leader", "type": "number", "visible": "public", "initial": 2, "meaning": "The seat that leads the current trick.", "observable": false},
      {"key": "hand_number", "type": "number", "visible": "public", "initial": 1, "meaning": "The current hand, from 1 to 6.", "observable": false},
      {"key": "trick_in_hand", "type": "number", "visible": "public", "initial": 1, "meaning": "The current trick within the hand, from 1 to 5.", "observable": false},
      {"key": "round_number", "type": "number", "visible": "public", "initial": 1, "meaning": "The current trick overall, from 1 to 30.", "observable": false}
    ]
  },
  "setup": [
    "Seats are 1, 2 and 3.",
    "Every score is 0.",
    "dealer is set to 1, hand_number to 1, trick_in_hand to 1 and round_number to 1.",
    "leader is set to 2, the seat after the dealer."
  ],
  "round": [
    {"action": "update", "who": "table", "answer": null, "effect": "When trick_in_hand == 1: deck is set to all 32 cards (R1-R7, B1-B7, G1-G7, Y1-Y7, W1, W2, J1, J2). Every hand is emptied and every played_history entry is cleared."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When trick_in_hand == 1: each player draws 5 cards at random from deck into their hand, each card removed from deck as it is drawn."},
    {"action": "update", "who": "table", "answer": null, "effect": "When trick_in_hand == 1: one more card is drawn at random from deck into trump_card. trump_suit is set to its suit letter if it is numbered, or to none if it is W or J. The 16 cards left in deck stay hidden and unused this hand."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "When trick_in_hand == 1: announce 'Hand {hand_number}: dealer is seat {dealer}; turned card is {trump_card}; trump is {trump_suit}.'"},
    {"action": "update", "who": "all players", "answer": null, "effect": "When trick_in_hand == 1: every bid and every tricks_taken is set to 0."},
    {"action": "sync", "who": "all players", "answer": null, "effect": "When trick_in_hand == 1: each player is sent their own hand, trump_card and the scores."},
    {"action": "poll", "who": "all players", "answer": "a whole number from 0 to 5", "effect": "When trick_in_hand == 1: each player's bid is set to their answer. Nobody sees any bid until all are in."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "When trick_in_hand == 1: one message per player: 'Seat {seat} bids {bid}.'"},
    {"action": "update", "who": "table", "answer": null, "effect": "led_suit is set to none, trick_cards is emptied and every played_card is set to empty."},
    {"action": "ask", "who": "seat leader", "answer": "one card from the player's own hand", "effect": "The card is removed from the leader's hand and appended to trick_cards and played_history. The leader's played_card is set to it. If the card is numbered, led_suit is set to its suit."},
    {"action": "ask", "who": "seat leader % 3 + 1", "answer": "one card from the player's own hand", "effect": "The card is removed from the player's hand and appended to trick_cards and played_history. The player's played_card is set to it. If led_suit == none and trick_cards[0] is not a Wizard and the card is numbered, led_suit is set to its suit."},
    {"action": "ask", "who": "seat (leader + 1) % 3 + 1", "answer": "one card from the player's own hand", "effect": "The card is removed from the player's hand and appended to trick_cards and played_history. The player's played_card is set to it. If led_suit == none and trick_cards[0] is not a Wizard and the card is numbered, led_suit is set to its suit."},
    {"action": "update", "who": "table", "answer": null, "effect": "The trick winner is worked out by arithmetic. Each card in trick_cards gets a power by its play position p (0, 1, 2). A Wizard has power 1000 - p. A card of trump_suit has power 200 + rank. A card of led_suit that is not trump has power 100 + rank. Any other numbered card has power 0. A Jester has power 3 - p only if all three cards are Jesters, otherwise 0. The seat that played the card with the highest power wins. That seat's tricks_taken increases by 1, and leader is set to that seat."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce 'Seat {leader} wins trick {trick_in_hand} with cards {trick_cards}; tricks taken now {tricks_taken}.'"},
    {"action": "update", "who": "all players", "answer": null, "effect": "When trick_in_hand == 5: for each player, if tricks_taken == bid then score += 20 + 10 * tricks_taken, otherwise score -= 10 * |bid - tricks_taken|."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "When trick_in_hand == 5: separate messages per player: 'Seat {seat} took {tricks_taken} tricks' and 'Seat {seat} score is now {score}'."},
    {"action": "update", "who": "table", "answer": null, "effect": "round_number += 1. If trick_in_hand == 5: hand_number += 1, trick_in_hand is set to 1, dealer is set to dealer % 3 + 1, and leader is set to dealer % 3 + 1 using the new dealer. Otherwise trick_in_hand += 1."},
    {"action": "check", "who": "table", "answer": null, "effect": "End the game if round_number > 30. Otherwise continue with the next round."}
  ],
  "ending": {
    "condition": "round_number > 30",
    "rank_by": "you.score",
    "decided_by": "Each player's final score after 6 hands (30 tricks). The highest score wins, and players tied for the highest score share the win (a draw)."
  },
  "rules": [
    {"id": "R1", "text": "When the game begins, the deck has 32 cards: four suits (Red, Blue, Green, Yellow) numbered 1 to 7, plus 2 Wizards and 2 Jesters."},
    {"id": "R2", "text": "When the game begins, every score is 0, the dealer is seat 1 and seat 2 leads the first trick."},
    {"id": "R3", "text": "When a hand starts (trick_in_hand == 1), the deck is rebuilt from all 32 cards and each player receives exactly 5 cards in their private hand."},
    {"id": "R4", "text": "When a hand starts, one more card becomes trump_card. If it is numbered, its suit is trump_suit; if it is a Wizard or Jester, trump_suit is none."},
    {"id": "R5", "text": "When a hand starts, 16 cards remain in the deck unused and unseen."},
    {"id": "R6", "text": "When a hand starts, every bid and tricks_taken is reset to 0."},
    {"id": "R7", "text": "When a hand starts, all three players bid simultaneously a whole number from 0 to 5, and the bids need not total 5."},
    {"id": "R8", "text": "When all bids are in, each player's bid is announced in its own message."},
    {"id": "R9", "text": "When a hand starts, the seat after the dealer leads the first trick."},
    {"id": "R10", "text": "When a trick is played, the leader plays first, then the next seat in order (leader % 3 + 1), then the remaining seat."},
    {"id": "R11", "text": "When a player plays, they may play any card in their hand, with no obligation to follow suit, and the card leaves their hand."},
    {"id": "R12", "text": "When the first numbered card of a trick is played and no Wizard was played first, its suit becomes led_suit; a Jester played before it does not set the suit."},
    {"id": "R13", "text": "When a Wizard is the first card of a trick, the trick has no led suit and that Wizard wins."},
    {"id": "R14", "text": "When any Wizard is played in a trick, the first Wizard played wins the trick."},
    {"id": "R15", "text": "When no Wizard is played but a trump is, the highest trump wins the trick."},
    {"id": "R16", "text": "When no Wizard and no trump is played, the highest card of led_suit wins the trick."},
    {"id": "R17", "text": "When all three cards in a trick are Jesters, the first Jester played wins."},
    {"id": "R18", "text": "When a numbered card is neither of led_suit nor trump, it never wins the trick."},
    {"id": "R19", "text": "When a player wins a trick, their tricks_taken increases by 1, this is announced, and they lead the next trick."},
    {"id": "R20", "text": "When a hand ends with tricks_taken equal to bid, the player gains 20 + 10 x tricks_taken (for example, bid 2 and took 2 gives +40; bid 0 and took 0 gives +20)."},
    {"id": "R21", "text": "When a hand ends with tricks_taken not equal to bid, the player loses 10 x |bid - tricks_taken| (for example, bid 3 and took 1 gives -20)."},
    {"id": "R22", "text": "When a hand ends, each player's trick count and new score are announced in separate messages."},
    {"id": "R23", "text": "When a hand ends, the dealer moves to the next seat (1, then 2, then 3, then 1)."},
    {"id": "R24", "text": "When the 30th trick (the end of hand 6) is complete, the game ends."},
    {"id": "R25", "text": "When the game ends, the highest score wins and players tied at the top share the win."}
  ],
  "offers": [
    {"question": "Bid at the start of a hand", "who": "all three seats, simultaneously", "options": "any whole number from 0 to 5"},
    {"question": "Lead card", "who": "the seat in leader", "options": "every card currently in that seat's hand"},
    {"question": "Second card", "who": "seat leader % 3 + 1", "options": "every card currently in that seat's hand, whatever the led suit"},
    {"question": "Third card", "who": "the remaining seat", "options": "every card currently in that seat's hand, whatever the led suit"}
  ],
  "choices": [
    {"what": "3 players (min 3, max 3, suggested 3)", "why": "The designer fixed the game at three. The deck arithmetic (15 dealt, 1 turned, 16 unused) and the seat rotation depend on exactly three seats, and a fourth would change the card counts."},
    {"what": "No talk step", "why": "The rules state there is no discussion phase."},
    {"what": "Cards coded as short text (R5, W1, J2) and the trick winner computed as a power value per card", "why": "This turns the trick-winning rules into pure arithmetic: the first Wizard beats everything, then the highest trump, then the highest led-suit card, and an all-Jester trick goes to the first Jester."},
    {"what": "Strategy at this table", "why": "A thoughtful player bids from hand strength and the trump suit, then plays to hit the bid exactly. They dump high cards or Jesters when they have enough tricks, and track played cards and others' bids to judge which cards are still out."}
  ],
  "simplifications": [
    {"what": "Start-of-hand and end-of-hand steps are ordinary round steps, each carrying a when-condition on trick_in_hand", "why": "The step list is flat. Each step is individually conditional on a counter rather than being a separately chosen block, so the game stays faithful."},
    {"what": "The order of play is addressed by seat expressions relative to leader", "why": "The engine asks named seats; leader, leader % 3 + 1 and (leader + 1) % 3 + 1 reproduce seat order starting from the trick winner."}
  ],
  "unsupported": []
}
```
````
