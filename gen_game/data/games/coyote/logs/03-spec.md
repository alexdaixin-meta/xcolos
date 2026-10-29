# 03 spec

- time: 2026-10-27T08:39:37+00:00 (51.7s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 3f8ff214adf0cecc, reply sha256 7f34210f025e10b9

## Sent

````
Game: Coyote Lap
Players in the source: 3 to 4
Suggested table size, chosen by the designer of these rules (keep it): 4

Rules, as filed in the inventory:
DECK (33 cards): one -10, two -5, three 0, four each of 1, 2, 3, 4 and 5, three 10, two 15, one 20, and one special card 'Max→0'.

SETUP: Seat players in a fixed clockwise order. Each player starts with 0 Coyote tokens. The player in seat 1 opens hand 1. The game lasts exactly 12 hands.

EACH HAND:
1. Deal: shuffle the full 33-card deck and deal one card face down to each player.
2. Bandana: each player is told privately the cards of all other players, but never their own card.
3. Opening declaration: the opener declares a whole number from -30 to 60, a claim about the TRUE TOTAL of all cards in play this hand.
4. Responses: each other player, one at a time in clockwise order from the opener, chooses one of two options:
   (a) RAISE: declare a whole number strictly higher than the current declaration, at most 60. It becomes the current declaration, and this player becomes the current declarer.
   (b) CALL COYOTE: challenge the current declaration. Bidding stops immediately, and later players do not act this hand.
   Every declaration is announced to all players as it is made.
5. Automatic call: if every responder raised, the opener is treated as having called Coyote on the final declaration.
6. True total: add up the numbers on all cards in play. If the 'Max→0' card is in play, it counts as 0 itself, and the highest-valued other card in play also counts as 0. If several cards tie for highest, only one of them counts as 0. If the highest other card is negative, it still becomes 0.
7. Resolution: if the true total is LESS than the current declaration, the current declarer takes 1 Coyote token. Otherwise the caller, or the opener in the case of an automatic call, takes 1 Coyote token.
8. Reveal: all cards, the true total and the token taken are announced to everyone.
9. Rotate: the next player clockwise opens the next hand.

END: After hand 12, the game ends.

How the winner is decided: After 12 hands, the player with the fewest Coyote tokens wins. If two or more players tie for the fewest, the game is a draw.
````

## Reply

````
```json
{
  "name": "Coyote Lap",
  "summary": "Each player sees every card but their own. Players bid upward on the true total of the cards in play until someone calls Coyote, and whoever is wrong takes a token. After 12 hands the fewest tokens wins.",
  "players": {"min": 3, "max": 4, "suggested": 4},
  "parameters": {
    "deck_size": 33,
    "count_minus_10": 1,
    "count_minus_5": 2,
    "count_0": 3,
    "count_each_1_to_5": 4,
    "count_10": 3,
    "count_15": 2,
    "count_20": 1,
    "count_max_to_zero": 1,
    "max_to_zero_code": 100,
    "hands": 12,
    "declaration_min": -30,
    "declaration_max": 60,
    "raise_min_step": 1,
    "tokens_per_loss": 1,
    "starting_tokens": 0,
    "cards_per_player": 1
  },
  "attributes": {
    "player": [
      {"key": "tokens", "type": "number", "visible": "public", "initial": 0, "meaning": "Coyote tokens taken so far (fewer is better)", "observable": true},
      {"key": "card", "type": "number", "visible": "others", "initial": 0, "meaning": "The card dealt this hand, as its face value, or 100 for the special 'Max→0' card. Every other player sees it; the owner does not (the bandana).", "observable": false}
    ],
    "game": [
      {"key": "deck", "type": "list", "visible": "none", "initial": [-10,-5,-5,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,10,10,10,15,15,20,100], "meaning": "The undealt cards of the 33-card deck (100 = 'Max→0')", "observable": false},
      {"key": "hand_number", "type": "number", "visible": "public", "initial": 1, "meaning": "The current hand, from 1 to 12", "observable": true},
      {"key": "opener_seat", "type": "number", "visible": "public", "initial": 1, "meaning": "Seat that opens this hand", "observable": true},
      {"key": "current_declaration", "type": "number", "visible": "public", "initial": 0, "meaning": "The highest declaration made so far this hand", "observable": true},
      {"key": "current_declarer", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat that made the current declaration", "observable": true},
      {"key": "bidding_open", "type": "bool", "visible": "public", "initial": false, "meaning": "True while nobody has called Coyote this hand", "observable": false},
      {"key": "caller", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat that called Coyote, or the opener on an automatic call", "observable": true},
      {"key": "true_total", "type": "number", "visible": "public", "initial": 0, "meaning": "The true total of the cards in play, computed after bidding", "observable": true},
      {"key": "hand_loser", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat that took the token this hand", "observable": true}
    ]
  },
  "setup": [
    "Seat the players in a fixed clockwise order, seats 1 to N.",
    "Every player's tokens is set to 0.",
    "hand_number is set to 1 and opener_seat to 1."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "Reset deck to the full 33-card list. For each player, draw one card at random from deck: set that player's card to its value and remove it from deck. Set caller = 0, current_declarer = 0, hand_loser = 0, true_total = 0, bidding_open = true."},
    {"action": "sync", "who": "all players", "answer": null, "effect": "Each player privately sees the card of every other player (card is visible to others) but never their own."},
    {"action": "ask", "who": "the opener (seat opener_seat)", "answer": "a whole number from -30 to 60", "effect": "Set current_declaration = answer and current_declarer = opener_seat. Announce to all: 'Seat {opener_seat} opens at {current_declaration}.'"},
    {"action": "ask", "who": "responder 1: seat ((opener_seat) mod N) + 1, when bidding_open", "answer": "a choice: raise or call_coyote (raise is offered only if current_declaration < 60)", "effect": "If call_coyote: set caller = this seat, set bidding_open = false, and announce the call. If raise: go on to the next step."},
    {"action": "ask", "who": "responder 1, when bidding_open and they chose raise", "answer": "a whole number from current_declaration + 1 to 60", "effect": "Set current_declaration = answer and current_declarer = this seat. Announce the declaration to all."},
    {"action": "ask", "who": "responder 2: seat ((opener_seat + 1) mod N) + 1, when bidding_open", "answer": "a choice: raise or call_coyote (raise is offered only if current_declaration < 60)", "effect": "If call_coyote: set caller = this seat, set bidding_open = false, and announce the call. If raise: go on to the next step."},
    {"action": "ask", "who": "responder 2, when bidding_open and they chose raise", "answer": "a whole number from current_declaration + 1 to 60", "effect": "Set current_declaration = answer and current_declarer = this seat. Announce the declaration to all."},
    {"action": "ask", "who": "responder 3: seat ((opener_seat + 2) mod N) + 1, only when N = 4 and bidding_open", "answer": "a choice: raise or call_coyote (raise is offered only if current_declaration < 60)", "effect": "If call_coyote: set caller = this seat, set bidding_open = false, and announce the call. If raise: go on to the next step."},
    {"action": "ask", "who": "responder 3, only when N = 4, bidding_open and they chose raise", "answer": "a whole number from current_declaration + 1 to 60", "effect": "Set current_declaration = answer and current_declarer = this seat. Announce the declaration to all."},
    {"action": "update", "who": "the opener, when bidding_open", "answer": null, "effect": "Automatic call: set caller = opener_seat and bidding_open = false. Announce: 'Everyone raised; Seat {opener_seat} calls Coyote automatically on {current_declaration}.'"},
    {"action": "update", "who": "table", "answer": null, "effect": "true_total = sum of every card that is not 100. If some player's card = 100, subtract the maximum of the other players' cards (exactly one copy of the highest, even if that value is negative)."},
    {"action": "update", "who": "table", "answer": null, "effect": "If true_total < current_declaration: the current_declarer's tokens += 1 and hand_loser = current_declarer. Otherwise: the caller's tokens += 1 and hand_loser = caller."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Reveal every player's card (100 shown as 'Max→0'), plus true_total, current_declaration and hand_loser: 'Cards: {cards}. True total {true_total} against a declaration of {current_declaration}. Seat {hand_loser} takes a Coyote token.'"},
    {"action": "update", "who": "table", "answer": null, "effect": "opener_seat = (opener_seat mod N) + 1; hand_number += 1."},
    {"action": "check", "who": "table", "answer": null, "effect": "If hand_number > 12, end the game; otherwise continue to the next hand."}
  ],
  "ending": {
    "condition": "hand_number > 12",
    "rank_by": "0 - you.tokens",
    "decided_by": "A player's standing is the negative of their Coyote tokens. The player with the fewest tokens wins, and players tied for the fewest share the result (the source calls this a draw)."
  },
  "rules": [
    {"id": "R1", "text": "When the game starts, every player has 0 tokens, hand_number is 1 and opener_seat is 1."},
    {"id": "R2", "text": "When a hand begins, the deck is reset to the 33 cards (one -10, two -5, three 0, four each of 1 to 5, three 10, two 15, one 20, one Max→0), and each player is dealt exactly 1 card that is removed from the deck."},
    {"id": "R3", "text": "When cards are dealt, each player can see every other player's card but not their own."},
    {"id": "R4", "text": "When the opener declares, the value must be a whole number from -30 to 60, and the opener becomes current_declarer."},
    {"id": "R5", "text": "When a responder raises, the new declaration must be a whole number strictly greater than current_declaration and at most 60, and that responder becomes current_declarer."},
    {"id": "R6", "text": "When current_declaration is 60, a responder is offered only call_coyote."},
    {"id": "R7", "text": "When a responder calls Coyote, bidding stops and no later responder acts this hand."},
    {"id": "R8", "text": "When every responder raises, the opener is the caller (an automatic call) on the final declaration."},
    {"id": "R9", "text": "When no Max→0 card is in play, true_total is the plain sum of all cards in play (for example, cards 5, 10 and -5 give 10)."},
    {"id": "R10", "text": "When the Max→0 card is in play, it counts 0 and exactly one copy of the highest other card counts 0 (for example, Max→0, 15, 15 and 3 give 18)."},
    {"id": "R11", "text": "When the Max→0 card is in play and the highest other card is negative, that card still counts 0 (for example, Max→0, -5 and -10 give -10)."},
    {"id": "R12", "text": "When true_total < current_declaration, the current_declarer's tokens rise by 1."},
    {"id": "R13", "text": "When true_total >= current_declaration, the caller's tokens rise by 1 (the opener's on an automatic call)."},
    {"id": "R14", "text": "When a hand ends, every card, true_total and the seat that took the token are announced to all players."},
    {"id": "R15", "text": "When a hand ends, opener_seat moves to the next seat clockwise, wrapping from seat N to seat 1."},
    {"id": "R16", "text": "When 12 hands have been played, the game ends."},
    {"id": "R17", "text": "When the game ends, the player with the fewest tokens wins, and players tied for the fewest share the result."}
  ],
  "offers": [
    {"question": "Opening declaration", "who": "the opener (seat opener_seat)", "options": "any whole number from -30 to 60"},
    {"question": "Raise or call", "who": "each responder in clockwise order from the opener, while bidding is open", "options": "raise or call_coyote when current_declaration < 60; only call_coyote when current_declaration = 60"},
    {"question": "Raise amount", "who": "a responder who chose raise", "options": "any whole number from current_declaration + 1 to 60"}
  ],
  "choices": [
    {"what": "3 to 4 players, suggested 4", "why": "The designer suggests 4, so it is kept. 3 is the minimum because with fewer players there is too little hidden information to reason about and no chain of raises. 4 is the maximum the source allows, and more responders would push declarations past what the deck can support."},
    {"what": "Max→0 is stored as the code 100 in card", "why": "Cards must be numbers so the total can be computed. 100 is never a face value, so the code is unambiguous, and the reveal shows it as 'Max→0'."},
    {"what": "No free-talk step before the bidding", "why": "The source has no table talk. Information is carried by the declarations themselves, and adding talk would add a mechanic."},
    {"what": "Strategy at the table", "why": "Each player sums the cards they can see and estimates their own unseen card from the deck odds, watching for a visible Max→0. They then read the other players' declarations as signals about their own card. A thoughtful player raises only when the expected total supports it, and calls when the current bid outruns what they see."}
  ],
  "simplifications": [
    {"what": "The clockwise response sequence is written as fixed responder slots (responder 1, 2 and 3 relative to the opener), each a raise-or-call choice followed by a number step for raises", "why": "The engine runs flat step lists. Per-slot steps with when-conditions interleave the choice and the amount for each responder in order."},
    {"what": "A tie for the fewest tokens is a shared win rather than a declared draw", "why": "The engine's ranking makes players level at the top share the win. This matches the source's draw outcome in effect."},
    {"what": "The deck is reset and redealt with random draws each hand", "why": "Shuffling is modelled as drawing at random from the deck list."}
  ],
  "unsupported": []
}
```
````
