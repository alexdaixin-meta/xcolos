# 45 spec

- time: 2026-10-27T11:02:22+00:00 (69.7s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 7a9634d846e05cdc, reply sha256 652dfcce12fc9c8f

## Sent

````
Game: Hanamikoji: Five Geisha
Players in the source: 2 to 2
Suggested table size, chosen by the designer of these rules (keep it): 2

Rules, as filed in the inventory:
COMPONENTS.
- There are 5 Geisha, numbered 1 to 5, with Charm 3, 3, 4, 5, 6.
- There are 21 Item cards. Each card shows a Geisha number: three 1s, three 2s, four 3s, five 4s and six 5s.
- Each Geisha has a marker. Each marker is on Player 1's side, Player 2's side, or in the middle. All markers start in the middle.

PLAYER STATE.
- hand: private cards.
- secret: 0 or 1 face-down card.
- unused_actions: a list.
- kept: the cards placed on the player's side, visible to both.
- charm.
- geisha_count.
- standing.

GAME STATE.
- deck, removed_card, discard (hidden).
- hand_number (1–4), round_in_hand (1–8), starting_seat.
- marker_1 to marker_5.

ACTION NAMES.
The four actions are spelled exactly: Secret, Trade-off, Gift, Competition.

STRUCTURE.
The game is 4 hands of 8 rounds, 32 rounds in total. Hands 1 and 2 form Pair 1; hands 3 and 4 form Pair 2. Player 1 is the starting seat in hands 1 and 3; Player 2 is the starting seat in hands 2 and 4.

START OF A HAND (round_in_hand = 1, before anything else).
1. Shuffle all 21 Items and set 1 aside face-down as removed_card. Nobody sees it.
2. Deal 6 cards privately to each player. The remaining 8 cards form the deck.
3. Empty both secrets. Empty the discard.
4. Set both players' unused_actions to [Secret, Trade-off, Gift, Competition].
5. If this is hand 1 or hand 3, empty both players' kept lists. In hands 2 and 4, kept lists carry over unchanged. Markers always carry over.

EACH ROUND (one turn).
1. The active player is the starting seat in odd rounds (1, 3, 5, 7) and the other player in even rounds (2, 4, 6, 8). Each player therefore takes 4 turns per hand.
2. The active player draws the top card of the deck into their hand.
3. The active player chooses one action. The options offered are exactly the actions currently in their unused_actions list. The list is never rebuilt from the round number.
4. That action is removed from their unused_actions list.
5. The active player names the hand cards the action uses, by Geisha number, from cards they actually hold.
6. The action is resolved:
   - Secret: move 1 hand card face-down to the player's secret.
   - Trade-off: move 2 hand cards face-down to the discard. They are out of play for this hand.
   - Gift: reveal 3 hand cards. The opponent chooses 1 of them, and it goes to the opponent's kept. The other 2 go to the active player's kept.
   - Competition: reveal 4 hand cards split into Pair A (2 cards) and Pair B (2 cards). The opponent chooses Pair A or Pair B, and it goes to the opponent's kept. The other pair goes to the active player's kept.

CARD BUDGET.
Each player holds 6 cards and draws 4 per hand, 10 in total. The actions use exactly 1+2+3+4 = 10 cards, so the chosen action is always affordable. In round 8 the active player has exactly one action left, which may be Trade-off, and must take it.

END OF A HAND (after round 8).
Each player's secret card is revealed and appended to their kept list.

END OF A PAIR (after hands 2 and 4 only, after the step above). Run these steps in this order:
(a) For each Geisha g, count the cards of number g in each player's kept. If one player's count is strictly higher, marker_g moves to that player's side. On a tie the marker stays where it is.
(b) For each player, charm is the total Charm of the Geisha whose markers are on their side, and geisha_count is the number of markers on their side. standing = charm.
(c) Win check:
   - A player with charm 11 or more wins.
   - Otherwise, a player with geisha_count 3 or more wins.
   - Both players cannot reach the same goal. If one reaches 11 charm and the other reaches 3 Geisha, the 11-charm player wins.
   - If someone wins, the game ends.

AFTER HAND 4.
If no one has won, the player with the higher charm wins. If charm is tied, the player with the higher geisha_count wins. Otherwise the game is a draw.

How the winner is decided: The win check runs at the end of each pair, after hand 2 and after hand 4. A player whose markers total 11 or more Charm wins. Otherwise, a player holding 3 or more markers wins; if one player has 11 Charm and the other has 3 markers, the 11-Charm player wins. If no one has won after hand 4, the higher Charm wins, then the higher Geisha count; otherwise the game is a draw.
````

## Reply

````
```json
{
  "name": "Hanamikoji: Five Geisha",
  "summary": "Two players each take four one-shot actions per hand to place Item cards for five Geisha, aiming for 11 Charm or 3 Geisha at the end of each pair of hands.",
  "players": {"min": 2, "max": 2, "suggested": 2},
  "parameters": {
    "geisha_count_total": 5,
    "charm_geisha_1": 3,
    "charm_geisha_2": 3,
    "charm_geisha_3": 4,
    "charm_geisha_4": 5,
    "charm_geisha_5": 6,
    "items_total": 21,
    "items_geisha_1": 3,
    "items_geisha_2": 3,
    "items_geisha_3": 4,
    "items_geisha_4": 5,
    "items_geisha_5": 6,
    "removed_per_hand": 1,
    "deal_per_player": 6,
    "deck_after_deal": 8,
    "hands": 4,
    "rounds_per_hand": 8,
    "rounds_total": 32,
    "turns_per_player_per_hand": 4,
    "secret_cards": 1,
    "tradeoff_cards": 2,
    "gift_cards": 3,
    "gift_cards_to_opponent": 1,
    "competition_cards": 4,
    "competition_pair_size": 2,
    "win_charm": 11,
    "win_geisha": 3
  },
  "attributes": {
    "player": [
      {"key": "hand", "type": "list", "visible": "ally", "initial": [], "meaning": "Item cards held privately, each a Geisha number 1-5", "observable": false},
      {"key": "secret", "type": "list", "visible": "ally", "initial": [], "meaning": "0 or 1 face-down card set aside by Secret this hand", "observable": false},
      {"key": "pending", "type": "list", "visible": "ally", "initial": [], "meaning": "cards picked from hand for the current action, in pick order (picks 1-2 are Pair A and picks 3-4 are Pair B in Competition)", "observable": false},
      {"key": "unused_actions", "type": "list", "visible": "public", "initial": ["Secret", "Trade-off", "Gift", "Competition"], "meaning": "actions not yet taken this hand", "observable": false},
      {"key": "kept", "type": "list", "visible": "public", "initial": [], "meaning": "cards placed on this player's side, visible to both", "observable": true},
      {"key": "charm", "type": "number", "visible": "public", "initial": 0, "meaning": "total Charm of Geisha whose markers are on this player's side", "observable": true},
      {"key": "geisha_count", "type": "number", "visible": "public", "initial": 0, "meaning": "number of markers on this player's side", "observable": true},
      {"key": "standing", "type": "number", "visible": "public", "initial": 0, "meaning": "equals charm; the score", "observable": true}
    ],
    "game": [
      {"key": "deck", "type": "list", "visible": "none", "initial": [], "meaning": "undealt Item cards this hand", "observable": false},
      {"key": "removed_card", "type": "list", "visible": "none", "initial": [], "meaning": "the 1 card set aside face-down each hand", "observable": false},
      {"key": "discard", "type": "list", "visible": "none", "initial": [], "meaning": "Trade-off cards, out of play this hand", "observable": false},
      {"key": "hand_number", "type": "number", "visible": "public", "initial": 1, "meaning": "current hand, 1-4", "observable": false},
      {"key": "round_in_hand", "type": "number", "visible": "public", "initial": 1, "meaning": "current round within the hand, 1-8", "observable": false},
      {"key": "starting_seat", "type": "number", "visible": "public", "initial": 1, "meaning": "seat that acts in odd rounds: 1 in hands 1 and 3, 2 in hands 2 and 4", "observable": false},
      {"key": "active_seat", "type": "number", "visible": "public", "initial": 1, "meaning": "seat taking this round's turn", "observable": false},
      {"key": "last_action", "type": "text", "visible": "public", "initial": "", "meaning": "action chosen this round", "observable": false},
      {"key": "marker_1", "type": "number", "visible": "public", "initial": 0, "meaning": "Geisha 1 marker: 0 middle, 1 Player 1's side, 2 Player 2's side", "observable": true},
      {"key": "marker_2", "type": "number", "visible": "public", "initial": 0, "meaning": "Geisha 2 marker: 0 middle, 1 Player 1's side, 2 Player 2's side", "observable": true},
      {"key": "marker_3", "type": "number", "visible": "public", "initial": 0, "meaning": "Geisha 3 marker: 0 middle, 1 Player 1's side, 2 Player 2's side", "observable": true},
      {"key": "marker_4", "type": "number", "visible": "public", "initial": 0, "meaning": "Geisha 4 marker: 0 middle, 1 Player 1's side, 2 Player 2's side", "observable": true},
      {"key": "marker_5", "type": "number", "visible": "public", "initial": 0, "meaning": "Geisha 5 marker: 0 middle, 1 Player 1's side, 2 Player 2's side", "observable": true},
      {"key": "game_over", "type": "number", "visible": "public", "initial": 0, "meaning": "1 once a player has won at a pair end, or hand 4 is complete", "observable": false}
    ]
  },
  "setup": [
    "Seat 1 is Player 1 and seat 2 is Player 2.",
    "All five markers start in the middle (marker_1 to marker_5 = 0).",
    "hand_number = 1, round_in_hand = 1, starting_seat = 1, game_over = 0.",
    "Each player's kept list is empty, and charm, geisha_count and standing are 0."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "When round_in_hand == 1: build deck as the 21 Items (three 1s, three 2s, four 3s, five 4s, six 5s). Draw 1 at random into removed_card. Draw 6 at random into each player's hand; the remaining 8 stay in deck. Set each secret, pending and discard to empty. Set each unused_actions to [Secret, Trade-off, Gift, Competition]. If hand_number is 1 or 3, set each kept to empty; in hands 2 and 4, kept carries over. Markers carry over."},
    {"action": "update", "who": "all players", "answer": null, "effect": "active_seat = starting_seat if round_in_hand is odd, otherwise the other seat (3 - starting_seat)."},
    {"action": "update", "who": "seat active_seat", "answer": null, "effect": "Draw 1 card at random from deck (the top of a shuffled deck), append it to the active player's hand and remove it from deck."},
    {"action": "sync", "who": "all players", "answer": null, "effect": "Each player sees their own hand and secret, and both players' kept, unused_actions, markers and counters."},
    {"action": "ask", "who": "seat active_seat", "answer": "one of the active player's unused_actions", "effect": "last_action = the choice; remove it from the active player's unused_actions."},
    {"action": "ask", "who": "seat active_seat", "answer": "one Geisha number present in the active player's hand", "effect": "Move that card from hand to pending (pick 1)."},
    {"action": "ask", "who": "seat active_seat", "answer": "one Geisha number present in the active player's hand", "effect": "When last_action is Trade-off, Gift or Competition: move that card from hand to pending (pick 2)."},
    {"action": "ask", "who": "seat active_seat", "answer": "one Geisha number present in the active player's hand", "effect": "When last_action is Gift or Competition: move that card from hand to pending (pick 3)."},
    {"action": "ask", "who": "seat active_seat", "answer": "one Geisha number present in the active player's hand", "effect": "When last_action is Competition: move that card from hand to pending (pick 4). Picks 1-2 form Pair A and picks 3-4 form Pair B."},
    {"action": "update", "who": "seat active_seat", "answer": null, "effect": "When last_action is Secret: move the 1 pending card to the active player's secret, face-down."},
    {"action": "update", "who": "seat active_seat", "answer": null, "effect": "When last_action is Trade-off: move the 2 pending cards to discard, face-down."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "When last_action is Gift: announce the 3 pending cards. When last_action is Competition: announce Pair A (picks 1-2) and Pair B (picks 3-4)."},
    {"action": "ask", "who": "the seat that is not active_seat", "answer": "one of the 3 revealed Gift cards, by Geisha number", "effect": "When last_action is Gift: append the chosen card to the opponent's kept, append the other 2 pending cards to the active player's kept, and empty pending."},
    {"action": "ask", "who": "the seat that is not active_seat", "answer": "Pair A or Pair B", "effect": "When last_action is Competition: append the chosen pair to the opponent's kept, append the other pair to the active player's kept, and empty pending."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When round_in_hand == 8: reveal each player's secret card, append it to their kept, and empty secret."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When round_in_hand == 8 and hand_number is 2 or 4: (a) for each g in 1-5, count the cards of number g in each player's kept; if Player 1's count is strictly higher, marker_g = 1; if Player 2's is strictly higher, marker_g = 2; on a tie marker_g is unchanged. (b) Each player's charm = sum of the Charm (3,3,4,5,6) of g whose marker_g equals their seat; geisha_count = number of markers equal to their seat; standing = charm. (c) game_over = 1 if either charm >= 11, or either geisha_count >= 3, or hand_number == 4."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "When round_in_hand == 8 and hand_number is 2 or 4: announce marker_1 to marker_5 and each player's charm and geisha_count."},
    {"action": "check", "who": "all players", "answer": null, "effect": "End the game if game_over == 1; otherwise continue."},
    {"action": "update", "who": "all players", "answer": null, "effect": "If round_in_hand < 8: round_in_hand += 1. Otherwise: round_in_hand = 1, hand_number += 1, starting_seat = 3 - starting_seat."}
  ],
  "ending": {
    "condition": "game_over == 1",
    "rank_by": "(you.charm >= 11) * 10000 + (you.geisha_count >= 3) * 1000 + you.charm * 10 + you.geisha_count",
    "decided_by": "A player with 11 or more Charm wins first. Otherwise a player with 3 or more Geisha wins. If nobody has won after hand 4, the higher Charm wins, then the higher Geisha count. Players level on all of these share the result, which is a draw."
  },
  "rules": [
    {"id": "R1", "text": "When the game starts, all 5 markers are in the middle (value 0)."},
    {"id": "R2", "text": "When a hand starts, 1 of the 21 Items is set aside as removed_card, each player is dealt 6 cards, and 8 cards remain in deck."},
    {"id": "R3", "text": "When a hand starts, both secrets and the discard are emptied and both unused_actions are reset to [Secret, Trade-off, Gift, Competition]."},
    {"id": "R4", "text": "When hand 1 or hand 3 starts, both kept lists are emptied; when hand 2 or 4 starts, kept lists and markers are unchanged."},
    {"id": "R5", "text": "Player 1 is starting_seat in hands 1 and 3, and Player 2 in hands 2 and 4."},
    {"id": "R6", "text": "In rounds 1, 3, 5 and 7 the starting seat is active; in rounds 2, 4, 6 and 8 the other seat is active."},
    {"id": "R7", "text": "At the start of each turn the active player draws 1 card from deck into hand."},
    {"id": "R8", "text": "The active player is offered exactly the actions in their unused_actions, and the chosen action is removed from that list."},
    {"id": "R9", "text": "In a player's 4th turn of a hand, exactly one action remains and it must be taken."},
    {"id": "R10", "text": "When Secret is chosen, 1 hand card moves face-down to the player's secret."},
    {"id": "R11", "text": "When Trade-off is chosen, 2 hand cards move face-down to discard and do not score this hand."},
    {"id": "R12", "text": "When Gift is chosen, 3 hand cards are revealed, the opponent picks 1 for their kept, and the other 2 go to the active player's kept."},
    {"id": "R13", "text": "When Competition is chosen, 4 hand cards are revealed as Pair A and Pair B of 2 cards each, the opponent picks one pair for their kept, and the other pair goes to the active player's kept."},
    {"id": "R14", "text": "Cards named for an action must be cards the active player holds."},
    {"id": "R15", "text": "After round 8 of every hand, each player's secret card is appended to their kept."},
    {"id": "R16", "text": "After hands 2 and 4, for each Geisha g, marker_g moves to the side of the player with strictly more g cards in kept; on a tie it stays where it is."},
    {"id": "R17", "text": "After hands 2 and 4, charm = the summed Charm (3,3,4,5,6) of a player's markers, geisha_count = their number of markers, and standing = charm."},
    {"id": "R18", "text": "At a pair end, a player with charm >= 11 wins and the game ends."},
    {"id": "R19", "text": "At a pair end, if no one has charm >= 11, a player with geisha_count >= 3 wins and the game ends."},
    {"id": "R20", "text": "If one player has 11 charm and the other has 3 Geisha, the 11-charm player wins."},
    {"id": "R21", "text": "If no one has won after hand 4, the higher charm wins; if charm is tied, the higher geisha_count wins; otherwise the game is a draw."},
    {"id": "R22", "text": "After hand 2, if no one has won, play continues to hand 3."}
  ],
  "offers": [
    {"question": "Choose an action", "who": "the active seat only", "options": "exactly the entries of the active player's unused_actions (4 in the first turn of a hand, 1 in the last)"},
    {"question": "Pick a card for the action (picks 1-4)", "who": "the active seat only", "options": "each distinct Geisha number still in the active player's hand; pick 1 always, pick 2 for Trade-off, Gift or Competition, pick 3 for Gift or Competition, pick 4 for Competition only"},
    {"question": "Choose a Gift card", "who": "the non-active seat, only when last_action is Gift", "options": "the Geisha numbers of the 3 revealed cards"},
    {"question": "Choose a Competition pair", "who": "the non-active seat, only when last_action is Competition", "options": "Pair A, Pair B"}
  ],
  "choices": [
    {"what": "2 players, min = max = suggested", "why": "The designer fixed 2. The Gift and Competition splits are a duel between the active player and one opponent, and the 21-card budget fits exactly two players."},
    {"what": "Strategy at the table", "why": "A thoughtful player hides key Geisha with Secret, offers Gift and Competition splits where every option leaves them ahead, and tracks the visible kept lists to guess what the opponent is holding."},
    {"what": "No talk step", "why": "The source has no negotiation, so none is added."},
    {"what": "unused_actions is public", "why": "The source does not state its visibility; the physical game shows used action tokens face-down, so both players know which actions remain."},
    {"what": "last_action is public", "why": "Which action was taken is visible in the physical game, even when the cards are not."},
    {"what": "Marker encoded as 0/1/2", "why": "Middle / Player 1 side / Player 2 side, so the marker can be used in arithmetic."},
    {"what": "rank_by weights 10000 / 1000 / 10 / 1", "why": "These weights encode the win order: 11 Charm, then 3 Geisha, then Charm, then Geisha count. Charm totals at most 21, so the weights never overlap. Both players cannot reach the same goal, so ties only occur in the final fallback, where a tie is a draw."}
  ],
  "simplifications": [
    {"what": "Cards for an action are named one pick at a time from the hand list", "why": "Choosing from the hand list guarantees the player names only cards they hold, with no free-text parsing."},
    {"what": "Competition pairs are set by pick order: picks 1-2 are Pair A, picks 3-4 are Pair B", "why": "This lets the split be made with sequential single-card choices."},
    {"what": "Drawing 'the top card' is a random draw from deck", "why": "The deck is shuffled, so the two are equivalent."},
    {"what": "Player-versus-player card counts for markers are compared in one update", "why": "The engine has no player-attribute operand, so the comparison is computed at the table level."}
  ],
  "unsupported": []
}
```
````
