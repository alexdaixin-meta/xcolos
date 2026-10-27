# 29 spec

- time: 2026-10-27T10:34:11+00:00 (69.9s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 a64e521dfde0de44, reply sha256 08a1e0726a20cabf

## Sent

````
Game: Hanamikoji: Paired Hands
Players in the source: 2 to 2
Suggested table size, chosen by the designer of these rules (keep it): 2

Rules, as filed in the inventory:
COMPONENTS
- 5 Geisha, G1 to G5, with Charm G1=3, G2=3, G3=4, G4=5, G5=6 (total 21).
- 21 Item cards: three of G1, three of G2, four of G3, five of G4 and six of G5. A card is written as its Geisha number, 1 to 5.
- 5 Victory Markers, one per Geisha. Each is on Player 1's side, on Player 2's side, or neutral. All start neutral.
- Each player has four action markers: Secret, Trade-off, Gift and Competition.
- Each player has pair totals: five counts, one per Geisha, of the cards they have kept during the current pair of hands.

STRUCTURE
- There are at most 4 hands of 8 rounds each (32 rounds).
- Hands 1 and 2 form pair 1. Hands 3 and 4 form pair 2.
- Player 1 starts hands 1 and 3. Player 2 starts hands 2 and 4.
- In each hand, the starting player is active in rounds 1, 3, 5 and 7, and the other player is active in rounds 2, 4, 6 and 8. The player who is not active is the opponent.

START OF EACH HAND (before its round 1)
- Shuffle all 21 Items.
- Remove the top card face down. Nobody sees it, and it plays no part this hand.
- Deal 6 cards to each player as a private hand. Each player sees only their own hand, as a sorted list of numbers.
- The other 8 cards form the face-down deck.
- Both players' four actions become unused, and both Secrets are emptied.
- At the start of hands 1 and 3 only, both players' pair totals are reset to 0 0 0 0 0.
- Victory Markers always stay where they are.

EACH ROUND
1. The game announces the hand, the round, the active player, each player's unused actions, both players' pair totals and the marker positions.
2. The active player draws the top deck card and is privately shown their hand.
3. Choice 1: the active player names one unused action: Secret, Trade-off, Gift or Competition.
4. Choice 2: the active player writes the cards the action uses, as space-separated numbers with repeats written out (for example '5 5 2'). The cards are legal if, for each Geisha number, the number of times it is written is at most the number of that card in the player's hand.
   - Secret: exactly 1 number. That card is set face down as their Secret.
   - Trade-off: exactly 2 numbers. Those cards are discarded face down and do not count.
   - Gift: exactly 3 numbers, revealed in the order written as offer 1, 2 and 3.
   - Competition: exactly 4 numbers, all revealed. The first two form pair A and the last two form pair B.
   The named cards leave the active player's hand.
5. Choice 3, only for Gift or Competition: the opponent writes one digit.
   - Gift: 1, 2 or 3. The opponent adds that card to their pair totals, and the active player adds the other two to theirs.
   - Competition: 1 for pair A or 2 for pair B. The opponent adds the chosen pair to their pair totals, and the active player adds the other pair to theirs.
6. The action becomes spent. The game publicly announces the action, and for Gift or Competition the revealed cards and the split. For Secret and Trade-off it announces only that the action was used.

DEFAULTS
- Illegal or missing action: the first unused action in the order Secret, Trade-off, Gift, Competition is used.
- Illegal card answer (wrong count, unreadable or not in hand): the required number of lowest-numbered cards in hand are used, in ascending order. For Competition, the first two of them form pair A.
- Illegal or missing pick: counts as 1.
- Cards always work out: each player holds 6 + 4 = 10 cards and spends 1 + 2 + 3 + 4 = 10.

END OF EACH HAND (after round 8)
- Each player's Secret is revealed and added to their pair totals.
- The game announces both Secrets and both players' pair totals.

END OF EACH PAIR (after hands 2 and 4, following the end-of-hand step)
- For each Geisha, compare the two players' pair totals. A strictly higher total moves that Geisha's marker to that player's side. A tie leaves the marker where it is (neutral, or on a side from pair 1).
- Charm is the sum of the Charm values of the Geisha on a player's side. Geisha count is the number of markers on a player's side.
- The game announces all markers, Charm and Geisha counts.
- Win check:
  - If a player has 11 or more Charm, they win.
  - Otherwise, if a player has 3 or more Geisha, they win.
  - Otherwise, after pair 1 the game continues with hand 3.
  - After pair 2 with no winner, the higher Charm wins. If Charm is equal, the higher Geisha count wins. If both are equal, the game is a draw.

How the winner is decided: After hand 2 and after hand 4: a player with 11 or more Charm from markers on their side wins. Otherwise a player with 3 or more markers on their side wins. Total Charm is 21 and there are 5 Geisha, so at most one player can meet each condition, and Charm is checked first. If nobody has won after hand 4, the higher Charm wins, then the higher Geisha count, and otherwise the game is a draw.
````

## Reply

````
```json
{
  "name": "Hanamikoji: Paired Hands",
  "summary": "Two players win the favour of five Geisha over up to four hands, played as two pairs, by keeping, discarding, gifting and splitting Item cards with four one-use actions; Victory Markers move after each pair.",
  "players": {"min": 2, "max": 2, "suggested": 2},
  "parameters": {
    "geisha_count_total": 5,
    "charm_g1": 3, "charm_g2": 3, "charm_g3": 4, "charm_g4": 5, "charm_g5": 6,
    "charm_total": 21,
    "cards_g1": 3, "cards_g2": 3, "cards_g3": 4, "cards_g4": 5, "cards_g5": 6,
    "cards_total": 21,
    "cards_removed_per_hand": 1,
    "hand_size_dealt": 6,
    "deck_size_after_deal": 8,
    "max_hands": 4,
    "rounds_per_hand": 8,
    "max_rounds": 32,
    "hands_per_pair": 2,
    "secret_cards": 1,
    "tradeoff_cards": 2,
    "gift_cards": 3,
    "competition_cards": 4,
    "charm_to_win": 11,
    "geisha_to_win": 3,
    "default_pick": 1
  },
  "attributes": {
    "player": [
      {"key": "hand", "type": "list", "visible": "ally", "initial": [], "meaning": "Item cards (numbers 1-5) the player privately holds, shown sorted", "observable": false},
      {"key": "secret", "type": "list", "visible": "ally", "initial": [], "meaning": "The 0 or 1 card set face down by the Secret action this hand", "observable": false},
      {"key": "unused_actions", "type": "list", "visible": "public", "initial": ["Secret", "Trade-off", "Gift", "Competition"], "meaning": "Action markers not yet spent this hand", "observable": false},
      {"key": "kept", "type": "list", "visible": "public", "initial": [], "meaning": "Cards kept during the current pair of hands; the pair total for Geisha g is the count of g in this list (Secrets join it only at the end of a hand)", "observable": true},
      {"key": "charm", "type": "number", "visible": "public", "initial": 0, "meaning": "Sum of Charm of the Geisha whose marker is on this player's side", "observable": true},
      {"key": "geisha_count", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of Victory Markers on this player's side", "observable": true},
      {"key": "standing", "type": "number", "visible": "public", "initial": 0, "meaning": "Ranking value: (charm>=11)*1000 + (geisha_count>=3)*100 + charm*10 + geisha_count", "observable": true}
    ],
    "game": [
      {"key": "deck", "type": "list", "visible": "none", "initial": [], "meaning": "Face-down draw deck for the current hand", "observable": false},
      {"key": "removed_card", "type": "list", "visible": "none", "initial": [], "meaning": "The one card set aside unseen at the start of each hand", "observable": false},
      {"key": "discard", "type": "list", "visible": "none", "initial": [], "meaning": "Face-down cards discarded by Trade-off this hand", "observable": false},
      {"key": "hand_number", "type": "number", "visible": "public", "initial": 1, "meaning": "Current hand, 1 to 4", "observable": false},
      {"key": "round_in_hand", "type": "number", "visible": "public", "initial": 1, "meaning": "Current round within the hand, 1 to 8", "observable": false},
      {"key": "starting_seat", "type": "number", "visible": "public", "initial": 1, "meaning": "Seat that starts the current hand: 1 in hands 1 and 3, 2 in hands 2 and 4", "observable": false},
      {"key": "active_seat", "type": "number", "visible": "public", "initial": 1, "meaning": "Seat acting this round; the other seat is the opponent", "observable": false},
      {"key": "chosen_action", "type": "text", "visible": "public", "initial": "", "meaning": "Action named this round after defaults", "observable": false},
      {"key": "chosen_cards", "type": "list", "visible": "none", "initial": [], "meaning": "Cards used this round after defaults; revealed publicly only for Gift and Competition", "observable": false},
      {"key": "pick", "type": "number", "visible": "public", "initial": 1, "meaning": "Opponent's pick: 1-3 for Gift offers, 1 or 2 for Competition pairs A/B", "observable": false},
      {"key": "marker_1", "type": "number", "visible": "public", "initial": 0, "meaning": "Victory Marker of Geisha 1: 0 neutral, 1 Player 1's side, 2 Player 2's side", "observable": true},
      {"key": "marker_2", "type": "number", "visible": "public", "initial": 0, "meaning": "Victory Marker of Geisha 2", "observable": true},
      {"key": "marker_3", "type": "number", "visible": "public", "initial": 0, "meaning": "Victory Marker of Geisha 3", "observable": true},
      {"key": "marker_4", "type": "number", "visible": "public", "initial": 0, "meaning": "Victory Marker of Geisha 4", "observable": true},
      {"key": "marker_5", "type": "number", "visible": "public", "initial": 0, "meaning": "Victory Marker of Geisha 5", "observable": true},
      {"key": "game_over", "type": "bool", "visible": "public", "initial": false, "meaning": "Set when a win check ends the game", "observable": false}
    ]
  },
  "setup": [
    "Seat 1 is Player 1 and seat 2 is Player 2.",
    "All five Victory Markers start neutral (marker_1..marker_5 = 0).",
    "Charm, geisha_count and standing start at 0 for both players.",
    "hand_number = 1, round_in_hand = 1, starting_seat = 1."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null,
     "effect": "When round_in_hand == 1 (start of a hand): build deck as the 21 Items [1,1,1,2,2,2,3,3,3,3,4,4,4,4,4,5,5,5,5,5,5]; move one random card from deck to removed_card (replacing its previous content); move 6 random deck cards into each player's hand (hand emptied first); deck now holds 8; discard emptied; each player's unused_actions = [Secret, Trade-off, Gift, Competition]; each secret emptied; if hand_number is 1 or 3, each kept = []; starting_seat = 1 if hand_number is 1 or 3, else 2."},
    {"action": "update", "who": "all players", "answer": null,
     "effect": "active_seat = starting_seat if round_in_hand is odd, else the other seat."},
    {"action": "tell", "who": "all players", "answer": null,
     "effect": "Announce hand_number, round_in_hand, active_seat, each player's unused_actions, each player's pair totals (count of 1..5 in kept), and marker_1..marker_5."},
    {"action": "update", "who": "the active seat", "answer": null,
     "effect": "Move one random card from deck to the active player's hand (the draw)."},
    {"action": "sync", "who": "all players", "answer": null,
     "effect": "Each player privately sees their own sorted hand and secret."},
    {"action": "ask", "who": "the active seat", "answer": "one of the active player's unused_actions: Secret, Trade-off, Gift, Competition",
     "effect": "chosen_action = the answer; if illegal or missing, chosen_action = the first of Secret, Trade-off, Gift, Competition still in unused_actions."},
    {"action": "ask", "who": "the active seat", "answer": "short text: space-separated card numbers, 1 for Secret, 2 for Trade-off, 3 for Gift, 4 for Competition, repeats written out",
     "effect": "If legal, chosen_cards = the written numbers in order; otherwise chosen_cards = the required number of lowest cards in hand in ascending order. Remove chosen_cards from the active player's hand.",
     "judged": "The answer is exactly the required number of card numbers for chosen_action (Secret 1, Trade-off 2, Gift 3, Competition 4), and no number appears more often than that card appears in the active player's hand."},
    {"action": "update", "who": "the active seat", "answer": null,
     "effect": "If chosen_action is Secret, append chosen_cards to the active player's secret; if Trade-off, append chosen_cards to discard. Remove chosen_action from the active player's unused_actions."},
    {"action": "ask", "who": "the opponent (the seat that is not active_seat)", "answer": "Gift: a choice of 1, 2 or 3; Competition: 1 (pair A = first two cards) or 2 (pair B = last two cards)",
     "effect": "When chosen_action is Gift or Competition: the opponent is shown the revealed chosen_cards (Gift as offers 1,2,3; Competition as pair A, pair B); pick = the answer, or 1 if illegal or missing."},
    {"action": "update", "who": "both players", "answer": null,
     "effect": "When chosen_action is Gift: append offer number pick to the opponent's kept and the other two offers to the active player's kept. When chosen_action is Competition: append the picked pair to the opponent's kept and the other pair to the active player's kept."},
    {"action": "tell", "who": "all players", "answer": null,
     "effect": "Publicly announce the active seat and chosen_action; for Gift or Competition also the revealed chosen_cards and who kept which; for Secret or Trade-off only that the action was used."},
    {"action": "update", "who": "all players", "answer": null,
     "effect": "When round_in_hand == 8 (end of hand): reveal each player's secret, append it to that player's kept, and announce both secrets and both players' pair totals."},
    {"action": "update", "who": "all players", "answer": null,
     "effect": "When round_in_hand == 8 and hand_number is 2 or 4 (end of pair): for each Geisha g, if count of g in Player 1's kept > count in Player 2's kept then marker_g = 1, if lower then marker_g = 2, if equal marker_g unchanged; for each player charm = sum of Charm (3,3,4,5,6) of Geisha with marker on their side, geisha_count = number of markers on their side, standing = (charm>=11)*1000 + (geisha_count>=3)*100 + charm*10 + geisha_count; game_over = true if any player has charm >= 11 or geisha_count >= 3, or if hand_number == 4. Announce all markers, charm and geisha counts."},
    {"action": "check", "who": "all players", "answer": null,
     "effect": "End the game if game_over is true; otherwise continue."},
    {"action": "update", "who": "all players", "answer": null,
     "effect": "If round_in_hand == 8 then hand_number += 1 and round_in_hand = 1; otherwise round_in_hand += 1."}
  ],
  "ending": {
    "condition": "game_over == true, set after a pair (round_in_hand == 8 and hand_number in {2,4}) when any player has charm >= 11 or geisha_count >= 3, or when hand_number == 4",
    "rank_by": "you.standing",
    "decided_by": "A player with 11 or more Charm wins. Otherwise a player with 3 or more Geisha wins. If neither holds after hand 4, the higher Charm wins, then the higher Geisha count. Equal standing is a shared result, which is the draw."
  },
  "rules": [
    {"id": "R1", "text": "When a hand starts, then the 21 Items are shuffled, 1 card is set aside unseen, each player is dealt 6 cards privately, and 8 cards remain in the deck."},
    {"id": "R2", "text": "When a hand starts, then both players' unused_actions become Secret, Trade-off, Gift, Competition and both secrets are emptied."},
    {"id": "R3", "text": "When hand 1 or hand 3 starts, then both players' kept lists are emptied; when hand 2 or 4 starts, kept is unchanged."},
    {"id": "R4", "text": "When a new hand starts, then the Victory Markers stay where they are."},
    {"id": "R5", "text": "When the hand is 1 or 3, then seat 1 is active in rounds 1, 3, 5, 7 and seat 2 in rounds 2, 4, 6, 8; in hands 2 and 4 it is the reverse."},
    {"id": "R6", "text": "When a round starts, then the active player draws 1 card from the deck into their hand."},
    {"id": "R7", "text": "When the active player names an action that is spent or invalid, then the first unused action in the order Secret, Trade-off, Gift, Competition is used."},
    {"id": "R8", "text": "When the active player uses Secret with 1 legal card, then that card leaves their hand and becomes their secret."},
    {"id": "R9", "text": "When the active player uses Trade-off with 2 legal cards, then both cards leave their hand into the discard and count for nobody."},
    {"id": "R10", "text": "When the active player uses Gift with cards a b c, then the opponent picks 1, 2 or 3, the opponent adds that card to kept and the active player adds the other two to kept."},
    {"id": "R11", "text": "When the active player uses Competition with cards a b c d, then the opponent picks 1 (a b) or 2 (c d), the opponent adds that pair to kept and the active player adds the other pair."},
    {"id": "R12", "text": "When the card answer has the wrong count or names cards not in hand, then the required number of lowest cards in hand, in ascending order, is used, and for Competition the first two form pair A."},
    {"id": "R13", "text": "When the opponent's pick is illegal or missing, then it counts as 1."},
    {"id": "R14", "text": "When an action is used, then it is removed from the active player's unused_actions for the rest of the hand."},
    {"id": "R15", "text": "When Secret or Trade-off is used, then only the action's use is announced, not the cards."},
    {"id": "R16", "text": "When round 8 of a hand ends, then each player's secret is revealed and added to their kept."},
    {"id": "R17", "text": "When a pair ends (after hand 2 or 4) and a player's count of Geisha g in kept is strictly higher than the other's, then marker_g moves to that player's side; on a tie it stays."},
    {"id": "R18", "text": "When a pair ends, then charm is the sum of 3,3,4,5,6 over Geisha 1..5 on the player's side and geisha_count is the number of markers on their side."},
    {"id": "R19", "text": "When a pair ends and a player has charm >= 11, then that player wins."},
    {"id": "R20", "text": "When a pair ends, no player has charm >= 11 and a player has geisha_count >= 3, then that player wins."},
    {"id": "R21", "text": "When pair 1 ends with no winner, then the game continues with hand 3."},
    {"id": "R22", "text": "When pair 2 ends with no winner by threshold, then the higher charm wins, then the higher geisha_count, and if both are equal it is a draw."}
  ],
  "offers": [
    {"question": "Choice 1: which action", "who": "the active seat", "options": "exactly the actions still in that player's unused_actions (4 options in the first turn of a hand, 1 in the last)"},
    {"question": "Choice 2: which cards", "who": "the active seat", "options": "free text of space-separated numbers 1-5: 1 number for Secret, 2 for Trade-off, 3 for Gift, 4 for Competition, drawn from their hand"},
    {"question": "Choice 3: the pick", "who": "the opponent (the non-active seat), only after Gift or Competition", "options": "after Gift: 1, 2, 3; after Competition: 1 (pair A), 2 (pair B)"}
  ],
  "choices": [
    {"what": "Exactly 2 players", "why": "The designer fixed the game at 2, and Gift and Competition are built as a split between the active player and one opponent."},
    {"what": "No talk step", "why": "The rules have no talk. In a two-player zero-sum game talk adds nothing to reason about."},
    {"what": "A standing attribute used as rank_by", "why": "It encodes the ordered win checks (Charm >= 11, then Geisha >= 3, then Charm, then Geisha) as one number. Equal standing gives the draw."},
    {"what": "Pair totals kept as a list `kept`", "why": "The total for Geisha g is the count of g in the list. This keeps the five per-Geisha counts in one attribute."},
    {"what": "Ask, not poll, for each choice", "why": "Each choice is made by one player in sequence, and the opponent picks after seeing the revealed cards."}
  ],
  "simplifications": [
    {"what": "'Top card' draws and removals are random picks from the deck list", "why": "The engine draws at random from a list, which is equivalent to drawing from a shuffled deck."},
    {"what": "Hand-start, end-of-hand and end-of-pair steps run inside the round list, gated by when-conditions on round_in_hand and hand_number", "why": "The step list is flat, and single conditional steps express these phases without choosing between blocks."},
    {"what": "Legality of the written cards is ruled by a judged sentence", "why": "Parsing free text and checking it as a sub-multiset of the hand is beyond plain arithmetic. The default and all scoring stay arithmetic."}
  ],
  "unsupported": []
}
```
````
