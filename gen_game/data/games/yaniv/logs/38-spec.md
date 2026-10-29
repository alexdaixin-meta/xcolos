# 38 spec

- time: 2026-10-28T06:36:25+00:00 (61.2s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 0c8dadd42b4b809f, reply sha256 cf047f3108ffd485

## Sent

````
Game: Row Yaniv
Players in the source: 2 to 4
Suggested table size, chosen by the designer of these rules (keep it): 3

Rules, as filed in the inventory:
DECK: 54 cards, used only for their values: two Jokers worth 0; four each of values 1 to 9 (Ace = 1); sixteen cards worth 10 (the 10s, Jacks, Queens and Kings). Only values matter; suits are ignored.

STATE: Each player has three private slots c1, c2 and c3. Each slot holds one card value or is empty. A player's hand total H is the sum of their non-empty slots. Each player has a public penalty total, starting at 0.
Public table state:
- the round number (1 to 24);
- the priority seat (seat 1 in round 1);
- a 'new hand' flag (on at the start);
- the draw pile, whose order is hidden and whose size is public;
- the OFFER ROW, an ordered public list of cards;
- the DEAD PILE, a public list of every card that has left play this hand.

EACH ROUND:
1. NEW HAND. If the 'new hand' flag is on: shuffle all 54 cards to form the draw pile. This is the only random event in any round. Empty all slots, empty the dead pile, and deal 3 cards from the top of the draw pile to each player in seat order, into c1, c2 and c3, told privately. Then turn the next card face up as the offer row (one card at position 1). Switch the flag off.
2. ANNOUNCE the offer row with its positions and values, the dead pile, the draw pile size, the priority seat, and each player's number of cards.
3. CHOICES. All players answer at the same moment, privately, three things:
   (a) action: YANIV, DRAW, or TAKE;
   (b) take position: a number from 1 to the length of the offer row (used only for TAKE);
   (c) shed slot: 1, 2 or 3. It must be a non-empty slot; if it is not, the lowest-numbered non-empty slot is used.
4. YANIV CHECK. A YANIV is valid only if the player's H is 10 or less. An invalid YANIV is announced as invalid, and that player is treated as DRAW for the rest of the round.
5. If at least one valid YANIV was made, no cards move this round. Go to step 10.
6. SHED. Each player removes the card in their shed slot. Every other slot of theirs holding the same value is also removed, so a pair sheds two cards and a triple sheds three. Those extra slots stay empty for the rest of the hand. Announce every player's shed card values.
7. TAKE. Go through the TAKE players in seat order, starting at the priority seat and wrapping around. Each one receives the offer-row card at their take position if no earlier player has claimed it, and places it in their shed slot. Announce who took which card. A TAKE player whose card was already claimed becomes DRAW.
8. DRAW. In the same order (from the priority seat), each DRAW player takes the top card of the draw pile into their shed slot, told privately. The drawn value is never announced.
9. ROW UPDATE. All offer-row cards not taken go to the dead pile. The new offer row is every card shed in step 6, listed in seat order from seat 1, and within a player in the order of their slots. Announce each player's card count and the draw pile size.
10. SHOWDOWN. A showdown happens in any of three cases:
   - a valid YANIV was made this round;
   - after step 9 the draw pile holds fewer cards than there are players;
   - this is round 24.
   All hands are revealed.
   If there were valid callers: let M be the lowest H among the callers, and N the lowest H among the non-callers (N = 99 if everyone called).
   - A caller scores 0 if their H equals M and M is less than N. Otherwise they score H + 20 (Asaf).
   - A non-caller scores 0 if their H is less than or equal to M. Otherwise they score H.
   With no valid caller: every player with the lowest H scores 0, and the others score their H.
   Add the scores to the penalty totals and announce all totals. Then switch the 'new hand' flag on, so the next round begins a fresh hand and a fresh shuffle.
11. The priority seat passes to the next seat in order.
12. END CHECK. The match ends after any showdown that leaves some player's penalty total at 50 or more, or after round 24.

There is no discussion phase.

How the winner is decided: When the match ends, the player with the lowest penalty total wins. If two or more players share the lowest total, the match is a draw among them.
````

## Reply

````
```json
{
  "name": "Row Yaniv",
  "summary": "A simultaneous-choice take on Yaniv: each round every player secretly chooses to call YANIV, draw blind or take from a public offer row, and sheds a card (with any matches). The lowest hand at showdown avoids penalty, and the lowest penalty total wins.",
  "players": {"min": 2, "max": 4, "suggested": 3},
  "parameters": {
    "deck_size": 54,
    "joker_count": 2,
    "joker_value": 0,
    "copies_per_value_1_to_9": 4,
    "ten_value_cards": 16,
    "ten_value": 10,
    "slots_per_player": 3,
    "cards_dealt_per_player": 3,
    "initial_offer_row_length": 1,
    "max_rounds": 24,
    "yaniv_threshold": 10,
    "asaf_penalty": 20,
    "no_noncaller_n": 99,
    "end_penalty": 50,
    "initial_penalty": 0,
    "empty_slot_code": -1
  },
  "attributes": {
    "player": [
      {"key": "c1", "type": "number", "visible": "ally", "initial": -1, "meaning": "Card value in slot 1 (0-10), or -1 if empty", "observable": false},
      {"key": "c2", "type": "number", "visible": "ally", "initial": -1, "meaning": "Card value in slot 2 (0-10), or -1 if empty", "observable": false},
      {"key": "c3", "type": "number", "visible": "ally", "initial": -1, "meaning": "Card value in slot 3 (0-10), or -1 if empty", "observable": false},
      {"key": "hand_total", "type": "number", "visible": "ally", "initial": 0, "meaning": "H: the sum of the non-empty slots", "observable": false},
      {"key": "card_count", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of non-empty slots", "observable": true},
      {"key": "penalty", "type": "number", "visible": "public", "initial": 0, "meaning": "Penalty total (the score; lower is better)", "observable": true},
      {"key": "action", "type": "text", "visible": "ally", "initial": "", "meaning": "This round's action (YANIV, DRAW or TAKE) after invalid-YANIV and lost-TAKE conversions", "observable": false},
      {"key": "take_pos", "type": "number", "visible": "ally", "initial": 1, "meaning": "Chosen offer-row position, used only for TAKE", "observable": false},
      {"key": "shed_slot", "type": "number", "visible": "ally", "initial": 1, "meaning": "Effective shed slot (1-3), corrected to the lowest non-empty slot if the chosen one is empty", "observable": false},
      {"key": "is_caller", "type": "bool", "visible": "public", "initial": false, "meaning": "Made a valid YANIV this round", "observable": false},
      {"key": "shed_values", "type": "list", "visible": "public", "initial": [], "meaning": "Card values shed this round, in slot order", "observable": false},
      {"key": "last_hand_total", "type": "number", "visible": "public", "initial": 0, "meaning": "H revealed at the most recent showdown", "observable": true}
    ],
    "game": [
      {"key": "round", "type": "number", "visible": "public", "initial": 1, "meaning": "Round number, 1 to 24", "observable": true},
      {"key": "priority_seat", "type": "number", "visible": "public", "initial": 1, "meaning": "Seat that resolves first in TAKE and DRAW", "observable": false},
      {"key": "new_hand", "type": "bool", "visible": "public", "initial": true, "meaning": "When true, a fresh hand is shuffled and dealt at the start of the round", "observable": false},
      {"key": "draw_pile", "type": "list", "visible": "none", "initial": [], "meaning": "Card values in the draw pile; its order is hidden", "observable": false},
      {"key": "draw_pile_size", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of cards in the draw pile", "observable": true},
      {"key": "offer_row", "type": "list", "visible": "public", "initial": [], "meaning": "Ordered public offer row of card values", "observable": true},
      {"key": "dead_pile", "type": "list", "visible": "public", "initial": [], "meaning": "Every card that has left play this hand", "observable": true},
      {"key": "claimed", "type": "list", "visible": "public", "initial": [], "meaning": "Offer-row positions already taken this round", "observable": false},
      {"key": "any_valid_yaniv", "type": "bool", "visible": "public", "initial": false, "meaning": "At least one valid YANIV was made this round", "observable": false},
      {"key": "showdown", "type": "bool", "visible": "public", "initial": false, "meaning": "A showdown happens this round", "observable": false},
      {"key": "min_caller_h", "type": "number", "visible": "public", "initial": 99, "meaning": "M: the lowest H among valid callers", "observable": false},
      {"key": "min_noncaller_h", "type": "number", "visible": "public", "initial": 99, "meaning": "N: the lowest H among non-callers (99 if everyone called)", "observable": false},
      {"key": "min_h", "type": "number", "visible": "public", "initial": 99, "meaning": "The lowest H overall, used when there is no valid caller", "observable": false},
      {"key": "max_penalty", "type": "number", "visible": "public", "initial": 0, "meaning": "The highest penalty total, kept beside the scores for the end check", "observable": false}
    ]
  },
  "setup": [
    "Every player's penalty is set to 0 and all slots c1, c2 and c3 are set to -1 (empty).",
    "round = 1, priority_seat = 1, new_hand = true, and offer_row and dead_pile are empty."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "When new_hand is true: draw_pile is set to the full 54-card list [0,0, four each of 1-9, sixteen 10s]; all slots are set to -1; dead_pile is emptied; in seat order, each player draws 3 cards at random from draw_pile into c1, c2 and c3 (removed from draw_pile); one more random card from draw_pile becomes offer_row = [that card]; new_hand = false. Then hand_total, card_count and draw_pile_size are recomputed."},
    {"action": "sync", "who": "all players", "answer": null, "effect": "Each player privately sees their own c1, c2, c3 and hand_total."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce offer_row with positions and values, dead_pile, draw_pile_size, priority_seat and every player's card_count."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Reset for the round: is_caller = false, shed_values = [], claimed = [], any_valid_yaniv = false, showdown = false."},
    {"action": "poll", "who": "all players", "answer": "one of YANIV, DRAW, TAKE", "effect": "Stored privately in action; no answer is shown until all are in."},
    {"action": "poll", "who": "all players", "answer": "a whole number from 1 to the length of offer_row", "effect": "Stored privately in take_pos (used only for TAKE)."},
    {"action": "poll", "who": "all players", "answer": "one of 1, 2, 3", "effect": "Stored in shed_slot; if that slot is -1, shed_slot is set to the lowest-numbered non-empty slot."},
    {"action": "update", "who": "all players", "answer": null, "effect": "YANIV check: for each player with action = YANIV, if hand_total <= 10 then is_caller = true, otherwise action = DRAW and the YANIV is announced as invalid. any_valid_yaniv = (count of is_caller > 0)."},
    {"action": "update", "who": "all players", "answer": null, "effect": "SHED, when any_valid_yaniv is false: each player appends the value in their shed slot to shed_values, then for each of their other slots, in slot order, holding that same value, appends it and sets that slot to -1. The shed slot is set to -1. Every player's shed_values is announced."},
    {"action": "update", "who": "each player in turn, starting at priority_seat and wrapping", "answer": null, "effect": "TAKE, when any_valid_yaniv is false: for each player with action = TAKE in that order, if take_pos is not in claimed, the shed slot is set to offer_row[take_pos], take_pos is appended to claimed, and the take is announced; otherwise action = DRAW."},
    {"action": "update", "who": "each player in turn, starting at priority_seat and wrapping", "answer": null, "effect": "DRAW, when any_valid_yaniv is false: for each player with action = DRAW in that order, one random card is removed from draw_pile and placed in the shed slot, told only to that player; draw_pile_size decreases by 1."},
    {"action": "update", "who": "all players", "answer": null, "effect": "ROW UPDATE, when any_valid_yaniv is false: offer_row cards at positions not in claimed are appended to dead_pile; offer_row = the concatenation of shed_values from seat 1 upward. hand_total and card_count are recomputed, and every card_count and draw_pile_size is announced."},
    {"action": "sync", "who": "all players", "answer": null, "effect": "Each player privately sees their updated slots and hand_total."},
    {"action": "update", "who": "all players", "answer": null, "effect": "showdown = any_valid_yaniv OR draw_pile_size < number of players OR round = 24. When showdown is true: last_hand_total = hand_total for every player (all hands revealed); min_caller_h = the lowest hand_total among is_caller players (99 if none); min_noncaller_h = the lowest among the others (99 if none); min_h = the lowest hand_total overall."},
    {"action": "update", "who": "all players", "answer": null, "effect": "SCORING, when showdown is true. With any_valid_yaniv: a caller adds 0 if hand_total = min_caller_h and min_caller_h < min_noncaller_h, otherwise adds hand_total + 20; a non-caller adds 0 if hand_total <= min_caller_h, otherwise adds hand_total. Without any_valid_yaniv: a player adds 0 if hand_total = min_h, otherwise adds hand_total. Then max_penalty = the highest penalty, new_hand = true, and all hands and penalty totals are announced."},
    {"action": "update", "who": "all players", "answer": null, "effect": "priority_seat = (priority_seat mod number of players) + 1; round increases by 1."},
    {"action": "check", "who": "all players", "answer": null, "effect": "End the game if (showdown is true and max_penalty >= 50) or round > 24; otherwise continue."}
  ],
  "ending": {
    "condition": "(showdown == true and max_penalty >= 50) or round > 24",
    "rank_by": "0 - you.penalty",
    "decided_by": "Each player's standing is their penalty total; the lowest penalty wins, and players tied for the lowest share the win (a draw among them)."
  },
  "rules": [
    {"id": "R1", "text": "When a new hand starts, the draw pile is the 54 values (two 0s, four each of 1-9, sixteen 10s), each player receives 3 random cards into c1, c2 and c3, and 1 more card becomes the offer row, leaving 54 - 3*players - 1 cards in the draw pile."},
    {"id": "R2", "text": "When a new hand starts, the dead pile is emptied and the new-hand flag is switched off."},
    {"id": "R3", "text": "A player's hand total H is the sum of their non-empty slots (an empty slot counts as nothing)."},
    {"id": "R4", "text": "When a player calls YANIV with H <= 10, the call is valid; with H = 11 or more it is announced as invalid and the player is treated as DRAW."},
    {"id": "R5", "text": "When at least one valid YANIV is made, no card moves that round and a showdown follows."},
    {"id": "R6", "text": "When a player sheds, the card in their shed slot and every other slot of theirs with the same value are removed, so a pair sheds 2 cards and a triple sheds 3."},
    {"id": "R7", "text": "When the chosen shed slot is empty, the lowest-numbered non-empty slot is shed instead."},
    {"id": "R8", "text": "When two TAKE players choose the same position, the one earlier in seat order from the priority seat gets the card, and the other becomes DRAW."},
    {"id": "R9", "text": "A taken or drawn card is placed in the player's shed slot; extra slots emptied by a pair or triple stay empty for the rest of the hand."},
    {"id": "R10", "text": "A drawn card's value is told only to the drawing player, and the draw pile size drops by 1 per draw."},
    {"id": "R11", "text": "After the take step, untaken offer-row cards go to the dead pile, and the new offer row is all shed cards in seat order from seat 1, in slot order within each player."},
    {"id": "R12", "text": "A showdown happens when a valid YANIV was made, when the draw pile holds fewer cards than there are players after the row update, or in round 24."},
    {"id": "R13", "text": "With valid callers, a caller whose H equals M (the lowest caller H) scores 0 when M < N (the lowest non-caller H, or 99 if all called); otherwise the caller scores H + 20."},
    {"id": "R14", "text": "With valid callers, a non-caller scores 0 when their H <= M; otherwise they score H."},
    {"id": "R15", "text": "In a showdown with no valid caller, every player with the lowest H scores 0 and the others score their H."},
    {"id": "R16", "text": "After every showdown, scores are added to penalty totals, all hands are revealed, and the next round starts a fresh hand."},
    {"id": "R17", "text": "Every round the priority seat moves to the next seat, wrapping from the last seat to seat 1."},
    {"id": "R18", "text": "The match ends after a showdown that leaves some penalty total at 50 or more, or after round 24."},
    {"id": "R19", "text": "The player with the lowest penalty total wins, and players tied for the lowest share the win."}
  ],
  "offers": [
    {"question": "action", "who": "all players", "options": "YANIV, DRAW, TAKE (the offer row always holds at least one card)"},
    {"question": "take position", "who": "all players", "options": "a whole number from 1 to the current length of offer_row"},
    {"question": "shed slot", "who": "all players", "options": "1, 2, 3 (an empty slot is replaced by the lowest non-empty slot, as the rules allow)"}
  ],
  "choices": [
    {"what": "2 to 4 players, suggested 3", "why": "The designer suggested 3, which is kept. The minimum is 2 because two players still race to a low hand, contest the row and time YANIV against Asaf. The maximum is 4 because each hand uses 3 cards per player plus the row, and more seats make take collisions and draws so frequent that one player's choice matters little."},
    {"what": "Empty slots are coded as -1", "why": "A Joker is worth 0, so 0 cannot also mean empty."},
    {"what": "No talk phase", "why": "The rules say there is no discussion phase."},
    {"what": "Strategy exists", "why": "Thoughtful players track the dead pile and offer row to count cards, set up pairs to shed several cards at once, avoid contested row positions, and time YANIV to avoid being undercut (Asaf)."},
    {"what": "The end check uses max_penalty after a showdown", "why": "This keeps the 50-point condition arithmetic on a table attribute."}
  ],
  "simplifications": [
    {"what": "The three simultaneous answers are three consecutive polls", "why": "A question takes one answer. Answers are stored privately and never shown between polls, so the choices stay simultaneous."},
    {"what": "Shuffling and drawing from the top are modelled as random draws from the draw_pile list", "why": "Drawing at random from an unordered hidden list is equivalent to drawing the top card of a shuffled pile."},
    {"what": "Skipping steps 6-9 after a valid YANIV is done with a per-step condition (any_valid_yaniv is false)", "why": "The step list is flat, but single steps can carry arithmetic conditions."}
  ],
  "unsupported": []
}
```
````
