# 14 spec

- time: 2026-10-27T08:53:16+00:00 (42.7s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 e23ca43cc63675bc, reply sha256 186a7ce28e57a545

## Sent

````
Game: Lost Cities: Three Expeditions
Players in the source: 2 to 2
Suggested table size, chosen by the designer of these rules (keep it): 2

Rules, as filed in the inventory:
CARDS. There are 33 cards in 3 colours: Red (R), Blue (B) and Green (G). Each colour has number cards 2, 3, 4, 5, 6, 7, 8, 9 and 10, written like R7 or B10, plus 2 wager cards, written RW, BW and GW (two of each).

SETUP. Shuffle all 33 cards into a face-down deck. This is the only random event in the game. Deal 6 cards to each player. Each player's hand is a hidden list that only its owner can see; the engine shows it to its owner as part of that player's state.

Table state:
- deck: hidden list, 21 cards remaining after the deal.
- discard_tops: public list of face-up cards, at most one per colour. It starts as an empty list.
- last_discard: hidden bookkeeping value, never shown to players. It starts as 'none'.

Player state, for each player and each colour c in R, B, G:
- sum_c: total of the numbers played in that colour. Starts at 0.
- top_c: highest number played in that colour, 0 meaning no number yet. Starts at 0.
- wag_c: number of wagers played in that colour. Starts at 0.
- cnt_c: number of cards in that colour's expedition, wagers included. Starts at 0.
- score: the player's current score. Starts at 0.
All player state is public except hand.

ROUND. Seat 1 is chosen at random. Each round, seat 1 takes a turn and then seat 2 takes a turn.

A TURN has two choices.

(1) PLAY OR DISCARD. The active player answers with one of:
- 'PLAY X', where X is a card in their hand.
- 'DISCARD X', where X is a card in their hand.

A PLAY is legal if:
- X is a number greater than top_c of its colour; or
- X is a wager and top_c of its colour is still 0.

When a play is legal, remove X from the hand, add 1 to cnt_c, then:
- for a number: add X to sum_c and set top_c to X;
- for a wager: add 1 to wag_c.

An illegal PLAY, or a card not in the hand, is treated as DISCARD of the first card in the hand.

A DISCARD removes X from the hand. If discard_tops already contains a card of X's colour, that old card is removed from the game permanently. Then X is appended to discard_tops, and last_discard is set to X.

(2) DRAW. The active player answers one of:
- 'DECK': take the top card of the deck into the hand.
- The name of a card in discard_tops other than last_discard: move that card from discard_tops into the hand.

An invalid answer, or naming last_discard, means DECK. If the deck is empty, the player must take a card from discard_tops other than last_discard. If none is available, the player draws nothing.

After the draw, last_discard is reset to 'none'. Both players always see discard_tops, both players' expedition numbers, and how many cards remain in the deck.

END OF ROUND. Recompute both scores. For each colour:
- if cnt_c = 0, the colour scores 0;
- otherwise it scores (sum_c - 15) x (1 + wag_c), plus 10 if cnt_c is 5 or more.
A player's score is the total of their three colours.

The game ends at the end of the round in which the deck became empty, or at the end of round 20, whichever comes first. Seat 2 always finishes the round, so both players take the same number of turns.

How the winner is decided: When the game ends, the player with the higher score wins. If the scores are equal, the game is a draw.
````

## Reply

````
```json
{
  "name": "Lost Cities: Three Expeditions",
  "summary": "Two explorers build rising number runs in three colours, betting with wager cards and fighting over a shared discard row, while a 21-card deck runs out.",
  "players": {"min": 2, "max": 2, "suggested": 2},
  "parameters": {
    "colours": 3,
    "total_cards": 33,
    "lowest_number": 2,
    "highest_number": 10,
    "wagers_per_colour": 2,
    "hand_size": 6,
    "deck_after_deal": 21,
    "expedition_cost": 15,
    "wager_multiplier_base": 1,
    "bonus_card_count": 5,
    "bonus_points": 10,
    "max_rounds": 20,
    "max_discard_tops_per_colour": 1
  },
  "attributes": {
    "player": [
      {"key": "hand", "type": "list", "visible": "ally", "initial": "6 cards dealt from deck", "meaning": "The cards the player holds. Only the owner sees them.", "observable": false},
      {"key": "sum_r", "type": "number", "visible": "public", "initial": 0, "meaning": "Total of the Red numbers played", "observable": false},
      {"key": "top_r", "type": "number", "visible": "public", "initial": 0, "meaning": "Highest Red number played. 0 means none yet.", "observable": false},
      {"key": "wag_r", "type": "number", "visible": "public", "initial": 0, "meaning": "Red wagers played", "observable": false},
      {"key": "cnt_r", "type": "number", "visible": "public", "initial": 0, "meaning": "Cards in the Red expedition, wagers included", "observable": false},
      {"key": "sum_b", "type": "number", "visible": "public", "initial": 0, "meaning": "Total of the Blue numbers played", "observable": false},
      {"key": "top_b", "type": "number", "visible": "public", "initial": 0, "meaning": "Highest Blue number played. 0 means none yet.", "observable": false},
      {"key": "wag_b", "type": "number", "visible": "public", "initial": 0, "meaning": "Blue wagers played", "observable": false},
      {"key": "cnt_b", "type": "number", "visible": "public", "initial": 0, "meaning": "Cards in the Blue expedition, wagers included", "observable": false},
      {"key": "sum_g", "type": "number", "visible": "public", "initial": 0, "meaning": "Total of the Green numbers played", "observable": false},
      {"key": "top_g", "type": "number", "visible": "public", "initial": 0, "meaning": "Highest Green number played. 0 means none yet.", "observable": false},
      {"key": "wag_g", "type": "number", "visible": "public", "initial": 0, "meaning": "Green wagers played", "observable": false},
      {"key": "cnt_g", "type": "number", "visible": "public", "initial": 0, "meaning": "Cards in the Green expedition, wagers included", "observable": false},
      {"key": "score", "type": "number", "visible": "public", "initial": 0, "meaning": "Current total score over the three colours", "observable": true}
    ],
    "game": [
      {"key": "deck", "type": "list", "visible": "none", "initial": "all 33 cards shuffled, 21 left after the deal", "meaning": "The face-down draw deck", "observable": false},
      {"key": "deck_size", "type": "number", "visible": "public", "initial": 21, "meaning": "Cards remaining in the deck. The rules show this to both players.", "observable": true},
      {"key": "discard_tops", "type": "list", "visible": "public", "initial": [], "meaning": "Face-up discards, at most one per colour", "observable": true},
      {"key": "last_discard", "type": "text", "visible": "none", "initial": "none", "meaning": "The card discarded this turn. It cannot be drawn back on the same turn.", "observable": false},
      {"key": "round", "type": "number", "visible": "public", "initial": 0, "meaning": "Rounds completed", "observable": true}
    ]
  },
  "setup": [
    "Build the 33-card deck: R2-R10, B2-B10, G2-G10, and two each of RW, BW and GW.",
    "Shuffle the deck. This is the only random event in the game.",
    "Choose seat 1 at random.",
    "Deal 6 cards to each player's hand by drawing at random from deck, leaving 21 cards in deck. Set deck_size to 21.",
    "Set discard_tops to an empty list and last_discard to 'none'.",
    "Sync each player their own state."
  ],
  "round": [
    {"action": "sync", "who": "all players", "answer": null, "effect": "Each player sees their own hand and all public state: the expedition numbers, discard_tops and deck_size."},
    {"action": "ask", "who": "seat 1", "answer": "one of 'PLAY X' (X a card in hand that is legal to play) or 'DISCARD X' (X any card in hand)", "effect": "On a legal PLAY of X in colour c: remove X from hand and add 1 to cnt_c. For a number, add X to sum_c and set top_c to X. For a wager, add 1 to wag_c. On DISCARD X: remove X from hand, remove any card of X's colour from discard_tops (it leaves the game), append X to discard_tops and set last_discard to X. An illegal PLAY, or a card not in hand, is treated as DISCARD of the first card in hand."},
    {"action": "ask", "who": "seat 1", "answer": "'DECK' (if deck is not empty) or the name of a card in discard_tops other than last_discard", "effect": "DECK: draw a random card from deck into hand and subtract 1 from deck_size. A named card: move it from discard_tops to hand. An invalid answer, or naming last_discard, means DECK. If deck is empty and no eligible discard exists, nothing is drawn. Then set last_discard to 'none'."},
    {"action": "update", "who": "seat 1", "answer": null, "effect": "Announce the card played or discarded, what was drawn (deck or the named discard), and the new deck_size and discard_tops."},
    {"action": "sync", "who": "seat 2", "answer": null, "effect": "Seat 2 sees their updated state."},
    {"action": "ask", "who": "seat 2", "answer": "one of 'PLAY X' (X a card in hand that is legal to play) or 'DISCARD X' (X any card in hand)", "effect": "Same as seat 1's play or discard step."},
    {"action": "ask", "who": "seat 2", "answer": "'DECK' (if deck is not empty) or the name of a card in discard_tops other than last_discard", "effect": "Same as seat 1's draw step. Then set last_discard to 'none'."},
    {"action": "update", "who": "all players", "answer": null, "effect": "For each player and each colour c: if cnt_c = 0 the colour scores 0, otherwise it scores (sum_c - 15) * (1 + wag_c), plus 10 if cnt_c >= 5. Set score to the total of the three colours. Add 1 to round. Announce both scores."},
    {"action": "check", "who": "all players", "answer": null, "effect": "End the game if deck_size = 0 or round >= 20. Otherwise continue."}
  ],
  "ending": {
    "condition": "deck_size == 0 or round >= 20 (checked at the end of a round, after seat 2's turn)",
    "rank_by": "you.score",
    "decided_by": "The player with the higher score wins. If the scores are equal, both share the result, which is a draw."
  },
  "rules": [
    {"id": "R1", "text": "When the game starts, the deck has 33 cards (numbers 2-10 in R, B and G, plus two wagers per colour), each player is dealt 6 cards, and 21 remain in deck."},
    {"id": "R2", "text": "When the game starts, seat 1 is chosen at random, and each round seat 1 takes a full turn and then seat 2 does."},
    {"id": "R3", "text": "When a player PLAYs a number X of colour c with X > top_c, then X leaves the hand, cnt_c rises by 1, sum_c rises by X and top_c becomes X."},
    {"id": "R4", "text": "When a player PLAYs a wager of colour c while top_c = 0, then it leaves the hand, cnt_c rises by 1 and wag_c rises by 1."},
    {"id": "R5", "text": "When a player attempts a PLAY of a number X <= top_c, or of a wager while top_c > 0, or of a card not in hand, then it is treated as DISCARD of the first card in hand."},
    {"id": "R6", "text": "When a player DISCARDs X, then X leaves the hand, any card of X's colour already in discard_tops is removed from the game, X is appended to discard_tops, and last_discard becomes X."},
    {"id": "R7", "text": "When a player draws DECK and the deck is not empty, then one card moves from deck to hand and deck_size falls by 1."},
    {"id": "R8", "text": "When a player names a card in discard_tops other than last_discard, then that card moves from discard_tops to hand."},
    {"id": "R9", "text": "When a player gives an invalid draw answer or names last_discard, then they draw from DECK."},
    {"id": "R10", "text": "When the deck is empty, then the player must take a card from discard_tops other than last_discard, and if none exists they draw nothing."},
    {"id": "R11", "text": "When a draw step ends, then last_discard is reset to 'none'."},
    {"id": "R12", "text": "When a round ends and a colour has cnt_c = 0, then it scores 0."},
    {"id": "R13", "text": "When a round ends and a colour has cnt_c >= 1, then it scores (sum_c - 15) * (1 + wag_c), so one wager with numbers totalling 20 scores 10."},
    {"id": "R14", "text": "When a round ends and a colour has cnt_c >= 5, then it scores an extra 10 points."},
    {"id": "R15", "text": "When a round ends, then each player's score is the sum of their three colour scores."},
    {"id": "R16", "text": "When a round ends with deck_size = 0, then the game ends, and seat 2 always completes the round first."},
    {"id": "R17", "text": "When round 20 ends, then the game ends."},
    {"id": "R18", "text": "When the game ends, then the higher score wins, and equal scores are a draw."}
  ],
  "offers": [
    {"question": "Play or discard", "who": "the active seat (seat 1, then seat 2)", "options": "'DISCARD X' for every card X in hand. 'PLAY X' for every number X in hand greater than top_c of its colour, and for every wager in hand whose colour has top_c = 0."},
    {"question": "Draw", "who": "the active seat", "options": "If deck is not empty: 'DECK' plus every card in discard_tops except last_discard. If deck is empty: every card in discard_tops except last_discard. If deck is empty and none exist: 'NOTHING' only."}
  ],
  "choices": [
    {"what": "Exactly 2 players", "why": "The designer fixed 2 players. The game is a duel over a shared discard row: what you discard feeds your one opponent."},
    {"what": "No talk step", "why": "The rules have no communication, and the game is a pure two-player contest of hand management and denial."},
    {"what": "Only legal plays are offered", "why": "A seat is never offered what it may not do. The fallback rule (an illegal play becomes a discard of the first card in hand) is kept for malformed answers."},
    {"what": "Public deck_size counter", "why": "The rules say both players see how many cards remain, while the deck itself stays hidden."},
    {"what": "Public round counter", "why": "Needed to apply the 20-round limit arithmetically."},
    {"what": "Strategy at the table", "why": "A thoughtful player commits only to colours they can reach 15+ in, times wagers before the numbers, avoids discarding cards the opponent needs, and watches the deck count to judge how much longer the game runs."}
  ],
  "simplifications": [
    {"what": "Taking the top card of the deck is a random pick from the deck list", "why": "The deck is shuffled, so a random draw is equivalent and keeps the match seed-reproducible."},
    {"what": "Each seat's turn is written as explicit seat 1 and seat 2 steps", "why": "The step list is flat. This keeps both players' turns equal within a round."}
  ],
  "unsupported": []
}
```
````
