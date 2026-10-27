# 03 spec

- time: 2026-10-27T20:43:32+00:00 (55.6s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 32f932a322d0455b, reply sha256 41160cbbc92a1c7d

## Sent

````
Game: Three-Card Wizard
Players in the source: 3 to 4
Suggested table size, chosen by the designer of these rules (keep it): 3

Rules, as filed in the inventory:
DECK: 25 cards: three suits (Red, Blue, Green), each numbered 1 to 7 (21 cards), plus 2 Wizards and 2 Jesters. Wizards and Jesters have no suit.

SETUP: Seat players in a fixed order. Player 1 is dealer in round 1. The dealer moves one seat along each round. All scores start at 0. The game lasts 12 rounds.

EACH ROUND:
1. Deal: shuffle all 25 cards, deal 3 cards face down to each player (seen only by their owner), then turn the next card face up as the trump card.
2. Trump: if the trump card is a numbered card, its suit is trump for this round. If it is a Wizard or a Jester, there is no trump this round.
3. Bidding: starting with the player after the dealer and ending with the dealer, each player in turn publicly bids a whole number from 0 to 3: the number of tricks they expect to take. Each bidder sees earlier bids. The dealer may not choose a bid that makes the total of all bids exactly 3.
4. Tricks: 3 tricks are played. The player after the dealer leads the first trick; the winner of each trick leads the next. In each trick, starting with the leader, each player in turn plays one card face up from their hand, seeing the cards already played to that trick.
5. Led suit: the led suit is the suit of the first numbered card played to the trick.
   - If a Jester is led, the next numbered card played sets the led suit.
   - If a Wizard is led, there is no led suit for that trick and anything may be played.
6. Following: a player holding a numbered card of the led suit must play either a card of that suit or a Wizard or Jester. Wizards and Jesters may always be played. A player with no card of the led suit may play any card. Only legal cards are offered.
7. Trick winner:
   - the first Wizard played wins;
   - if there is no Wizard, the highest trump card wins;
   - if there is no trump, the highest card of the led suit wins;
   - if every card is a Jester, the first Jester played wins.
   The winner adds 1 to their tricks taken this round.
8. Scoring: each player whose tricks taken equals their bid scores 20 + 10 x tricks taken. Each other player loses 10 x |bid - tricks taken|.
9. Reset bids and tricks taken, and pass the deal to the next seat.

END: after round 12 the game ends.

How the winner is decided: After 12 rounds the player with the highest total score wins. If two or more players tie for the highest total, the game is a draw.
````

## Reply

````
```json
{
  "name": "Three-Card Wizard",
  "summary": "Over 12 rounds, players are dealt 3 cards, publicly bid how many of the 3 tricks they will take, then play the tricks with trump, Wizards and Jesters; an exact bid scores 20 + 10 per trick and a missed bid loses 10 per trick off.",
  "players": {"min": 3, "max": 4, "suggested": 3},
  "parameters": {
    "deck_size": 25,
    "suit_count": 3,
    "rank_min": 1,
    "rank_max": 7,
    "numbered_cards": 21,
    "wizard_count": 2,
    "jester_count": 2,
    "hand_size": 3,
    "tricks_per_round": 3,
    "rounds": 12,
    "bid_min": 0,
    "bid_max": 3,
    "forbidden_bid_total": 3,
    "exact_bid_bonus": 20,
    "points_per_trick_on_exact_bid": 10,
    "penalty_per_trick_off": 10,
    "first_dealer_seat": 1,
    "wizard_power_base": 100,
    "trump_power_base": 50,
    "led_suit_power_base": 20,
    "jester_power_base": 5,
    "offsuit_power": 0
  },
  "attributes": {
    "player": [
      {"key": "score", "type": "number", "visible": "public", "initial": 0, "meaning": "Running total score.", "observable": true},
      {"key": "hand", "type": "list", "visible": "ally", "initial": [], "meaning": "Cards held this round, seen only by the owner.", "observable": false},
      {"key": "bid", "type": "number", "visible": "public", "initial": -1, "meaning": "Tricks bid this round. -1 means the player has not bid yet.", "observable": true},
      {"key": "tricks", "type": "number", "visible": "public", "initial": 0, "meaning": "Tricks taken this round.", "observable": true},
      {"key": "played_card", "type": "text", "visible": "public", "initial": "", "meaning": "Card played to the current trick, face up.", "observable": true},
      {"key": "play_pos", "type": "number", "visible": "public", "initial": 0, "meaning": "Order in which this player played to the current trick: 1 for the leader, then 2, 3, 4.", "observable": false},
      {"key": "power", "type": "number", "visible": "public", "initial": 0, "meaning": "Strength of played_card in the current trick, used to find the trick winner.", "observable": false}
    ],
    "game": [
      {"key": "deck", "type": "list", "visible": "none", "initial": "the 25 cards: Red 1..Red 7, Blue 1..Blue 7, Green 1..Green 7, Wizard A, Wizard B, Jester A, Jester B", "meaning": "Undealt cards, hidden from everyone.", "observable": false},
      {"key": "trump_card", "type": "text", "visible": "public", "initial": "", "meaning": "Card turned face up after the deal.", "observable": true},
      {"key": "trump_suit", "type": "text", "visible": "public", "initial": "none", "meaning": "Trump suit this round (Red, Blue or Green), or none.", "observable": true},
      {"key": "dealer", "type": "number", "visible": "public", "initial": 1, "meaning": "Seat of this round's dealer.", "observable": true},
      {"key": "leader", "type": "number", "visible": "public", "initial": 2, "meaning": "Seat that leads the current trick.", "observable": false},
      {"key": "led_suit", "type": "text", "visible": "public", "initial": "", "meaning": "Led suit of the current trick. Empty until it is set; 'none' if a Wizard was led.", "observable": false},
      {"key": "bid_total", "type": "number", "visible": "public", "initial": 0, "meaning": "Sum of the bids made so far this round.", "observable": false},
      {"key": "trick_no", "type": "number", "visible": "public", "initial": 0, "meaning": "Tricks completed this round.", "observable": false},
      {"key": "round_no", "type": "number", "visible": "public", "initial": 0, "meaning": "Rounds completed.", "observable": true}
    ]
  },
  "setup": [
    "Seat the players in a fixed order, seats 1 to N.",
    "Every score starts at 0.",
    "Seat 1 is the dealer for round 1 (dealer = 1).",
    "round_no = 0."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "Shuffle: deck = all 25 cards. Each hand = [], bid = -1, tricks = 0, played_card = ''. bid_total = 0, trick_no = 0, led_suit = ''. leader = (dealer mod N) + 1."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Deal 3 cards to each player: 3 times per player, pick a random card from deck, append it to that player's hand and remove it from deck. Then pick one more random card from deck, set trump_card to it and remove it from deck. trump_suit = the suit of trump_card if it is a numbered card; otherwise (Wizard or Jester) trump_suit = 'none'. Announce trump_card and trump_suit."},
    {"action": "sync", "who": "all players", "answer": null, "effect": "Each player sees their own hand, the trump_card, the trump_suit and the dealer."},
    {"action": "ask", "who": "each player in turn, starting with seat (dealer mod N)+1 and ending with the dealer", "answer": "a whole number from 0 to 3; for the dealer, the value 3 - bid_total is not offered", "effect": "The player's bid = answer; bid_total += answer. Each bid is announced publicly."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Start a trick: played_card = '', play_pos = 0 and power = 0 for every player; led_suit = ''."},
    {"action": "ask", "who": "each player in turn, starting with seat leader and going round the table", "answer": "one card from the player's own hand, chosen from the legal cards only: if led_suit is a suit and the hand holds a numbered card of that suit, the offer is the cards of that suit plus any Wizards and Jesters in hand; otherwise the whole hand", "effect": "Remove the card from hand; played_card = card; play_pos = 1 + the number of players who have already played to this trick. If led_suit = '' and the card is a Wizard and play_pos = 1, then led_suit = 'none'. If led_suit = '' and the card is numbered, then led_suit = the card's suit. The card is shown to everyone."},
    {"action": "update", "who": "all players", "answer": null, "effect": "For each player, power = 100 - play_pos if played_card is a Wizard; 50 + rank if it is numbered and its suit = trump_suit; 20 + rank if it is numbered and its suit = led_suit (and it is not trump); 5 - play_pos if it is a Jester; 0 otherwise. The player with the highest power wins the trick: their tricks += 1, leader = that seat, trick_no += 1. Announce the trick winner."},
    {"action": "repeat", "who": "all players", "answer": null, "effect": "Repeat the three trick steps above (start a trick, play cards, find the winner) until trick_no = 3."},
    {"action": "update", "who": "all players", "answer": null, "effect": "For each player: if tricks = bid, then score += 20 + 10 * tricks; otherwise score -= 10 * |bid - tricks|. Announce each bid, tricks and score."},
    {"action": "update", "who": "all players", "answer": null, "effect": "round_no += 1; dealer = (dealer mod N) + 1."},
    {"action": "check", "who": "all players", "answer": null, "effect": "If round_no = 12, end the game; otherwise start the next round."}
  ],
  "ending": {
    "condition": "round_no >= 12",
    "rank_by": "you.score",
    "decided_by": "Each player's standing is their total score after 12 rounds. The highest total wins. If players tie at the top, they share the result, which stands for the source's draw."
  },
  "rules": [
    {"id": "R1", "text": "When a round starts, then the deck holds all 25 cards: Red, Blue and Green 1 to 7, 2 Wizards and 2 Jesters."},
    {"id": "R2", "text": "When cards are dealt, then each player receives exactly 3 cards into their hand, seen only by the owner, and those cards leave the deck."},
    {"id": "R3", "text": "When the deal is done, then one more card from the deck becomes trump_card, face up."},
    {"id": "R4", "text": "When trump_card is a numbered card, then trump_suit is its suit; when it is a Wizard or a Jester, then trump_suit is none."},
    {"id": "R5", "text": "When bidding happens, then players bid in turn from the seat after the dealer through the dealer, each a whole number from 0 to 3, and each bid is public before the next player bids."},
    {"id": "R6", "text": "When the dealer bids, then the dealer may not choose the bid that makes the total of all bids exactly 3."},
    {"id": "R7", "text": "When the first trick of a round begins, then the seat after the dealer leads it."},
    {"id": "R8", "text": "When a trick is won, then its winner leads the next trick."},
    {"id": "R9", "text": "When the first numbered card is played to a trick, and no Wizard was led, then its suit becomes the led suit."},
    {"id": "R10", "text": "When a Jester is led, then the next numbered card played sets the led suit."},
    {"id": "R11", "text": "When a Wizard is led, then the trick has no led suit and any card may be played to it."},
    {"id": "R12", "text": "When a player holds a numbered card of the led suit, then they are offered only cards of that suit plus any Wizards and Jesters they hold."},
    {"id": "R13", "text": "When a player holds no numbered card of the led suit, or there is no led suit yet, then they are offered every card in their hand."},
    {"id": "R14", "text": "When a trick contains a Wizard, then the first Wizard played wins it."},
    {"id": "R15", "text": "When a trick has no Wizard and contains a trump card, then the highest trump card wins it."},
    {"id": "R16", "text": "When a trick has no Wizard and no trump card, then the highest card of the led suit wins it."},
    {"id": "R17", "text": "When every card in a trick is a Jester, then the first Jester played wins it."},
    {"id": "R18", "text": "When a player wins a trick, then their tricks increases by 1."},
    {"id": "R19", "text": "When 3 tricks have been played, then the round is scored."},
    {"id": "R20", "text": "When a player's tricks equals their bid, then they score 20 + 10 x tricks (bid 0 and took 0 gives +20; bid 2 and took 2 gives +40)."},
    {"id": "R21", "text": "When a player's tricks differs from their bid, then they lose 10 x |bid - tricks| (bid 3 and took 1 gives -20)."},
    {"id": "R22", "text": "When a round ends, then bids and tricks are reset and the deal passes one seat along (dealer = dealer mod N + 1)."},
    {"id": "R23", "text": "When 12 rounds have been completed, then the game ends and the highest total score wins, with players tied at the top sharing the win."}
  ],
  "offers": [
    {"question": "Bid", "who": "each non-dealer seat, in turn from the seat after the dealer", "options": "0, 1, 2, 3"},
    {"question": "Bid", "who": "the dealer (bids last)", "options": "0, 1, 2, 3 except the value 3 - bid_total, when that value lies between 0 and 3; if bid_total > 3, all of 0 to 3"},
    {"question": "Play a card", "who": "the trick leader", "options": "every card in their hand"},
    {"question": "Play a card", "who": "a later player in the trick, when led_suit is Red, Blue or Green and they hold a numbered card of that suit", "options": "their cards of the led suit, plus any Wizards and Jesters in their hand"},
    {"question": "Play a card", "who": "a later player in the trick, when led_suit is empty (only Jesters played so far), or led_suit is none (a Wizard was led), or they hold no card of the led suit", "options": "every card in their hand"}
  ],
  "choices": [
    {"what": "3 to 4 players, suggested 3", "why": "The designer's size is kept. With 3 players the dealer's restriction (the bids may not total exactly 3) forces at least one player to miss, so reading the earlier bids and your seat matters. At 4 players, 13 of the 25 cards are used, so the deck still fits. The minimum is 3 because with 2 players bidding and the dealer's restriction lose most of their tension. The maximum is not larger because the source stops at 4."},
    {"what": "No free talk step", "why": "The source has no table talk. The public bids are the only signal, so adding talk would add a mechanic."},
    {"what": "Card power values for finding the trick winner", "why": "The order of the trick-winner rules is encoded arithmetically: first Wizard = 100 - play_pos, trump = 50 + rank, led suit = 20 + rank, Jester = 5 - play_pos, any other card = 0. The highest power reproduces the source's order. Whenever a numbered card is present, it is either trump or of the led suit, so it beats Jesters."},
    {"what": "The 2 Wizards and 2 Jesters are named A and B", "why": "They are identical in play. The names only keep the hand and deck list entries distinct."},
    {"what": "The card played to a trick is chosen with ask in seat order from the leader", "why": "The source says each player sees the cards already played to that trick."}
  ],
  "simplifications": [
    {"what": "A tie at the top is shared by the tied players instead of being called a draw", "why": "The engine has no separate draw outcome. Players level at the top share the win, which is the same result."},
    {"what": "The three tricks are written as a repeat of the trick steps until trick_no = 3", "why": "The engine's step list is flat. A repeat expresses the fixed loop of 3 tricks."}
  ],
  "unsupported": []
}
```
````
