# 32 spec

- time: 2026-10-27T05:02:45+00:00 (61.7s)  model: claude-opus-5-5
- system prompt: [system/54cfed18-spec.md](system/54cfed18-spec.md) (sha256 54cfed18f9e94a06)
- sent sha256 97170225c080b4ce, reply sha256 b560bc98cde43ea6

## Sent

````
Game: Hanabi Duo
Players in the source: 2 to 2
Suggested table size, chosen by the designer of these rules (keep it): 2

Rules, as filed in the inventory:
CARDS. The deck has 12 cards in 2 colours, Red and Blue. Each colour has three 1s, two 2s and one 3. (Engine codes: Red 1/2/3 = 11/12/13, Blue 1/2/3 = 21/22/23, empty slot = 0. Colour is code divided by 10 rounded down; rank is code mod 10.)

SETUP. Shuffle the deck once. Deal 2 cards to each player into slots A and B, taking them from the front of the deck: player 1 gets A then B, then player 2 gets A then B. The 8 remaining cards stay in order face down. Set the Red pile and the Blue pile to 0. Set hint tokens to 3 (the maximum is 3) and fuses to 3. The discard pile starts empty. Every card note starts blank. Both players' scores start at 0.

WHAT EACH PLAYER SEES. On your turn you are shown:
- your partner's two cards;
- the notes on all four cards (yours and your partner's);
- both pile values, the hint tokens and the fuses;
- the full discard pile and the number of cards left in the deck;
- your partner's last action and its result.
You are never shown your own cards. There is no other communication: no messages, only the actions below.

ROUND. Each round player 1 takes a turn, then player 2 takes a turn. There are at most 12 rounds.

TURN. The active player chooses exactly one of these 8 options:
- Play A or Play B: reveal your card in that slot. If its rank is exactly 1 more than its colour's pile, that pile goes up by 1. Otherwise the play fails: the card goes to the discard pile and fuses go down by 1. If the slot is empty, nothing happens.
- Discard A or Discard B: put your card in that slot on the discard pile and gain 1 hint token, up to the maximum of 3. If the slot is empty, nothing happens.
- Hint colour of partner's A, Hint colour of partner's B, Hint rank of partner's A, or Hint rank of partner's B: if you have at least 1 hint token and the named partner slot holds a card, spend 1 token. Then name that card's colour (or rank) to your partner. Each of the partner's non-empty cards gets a note added: 'is Red' (or 'is 2', and so on) if it matches, or 'not Red' (or 'not 2') if it does not. If you have no token or the named slot is empty, nothing happens and the turn is wasted.

DRAWING. After a card leaves a slot (played, successfully or not, or discarded), the player takes the front card of the deck into that slot, and that slot's note is cleared. If the deck is empty, the slot stays empty and its note stays blank.

ANNOUNCEMENT. After every turn, the action and its result are shown to both players: which option was chosen, any card revealed, whether a play succeeded, and the hint named.

SCORE. After every turn, both players' scores are set to the Red pile plus the Blue pile. The two scores are always equal.

END. The game ends immediately when either of these happens after a turn:
- fuses reach 0;
- both piles reach 3.
Otherwise it ends after round 12. In every case the team keeps its current score.

How the winner is decided: Cooperative. When the game ends, if the team score (Red pile + Blue pile, shown identically as each player's score) is 4 or more, both seats win. Otherwise no seat wins. This holds whether the game ended on fuses, on a full score of 6, or after round 12.
````

## Reply

````
```json
{
  "name": "Hanabi Duo",
  "summary": "A cooperative two-player card game: each player sees only the partner's two cards, and the pair use hints, plays and discards to build Red and Blue piles from 1 to 3, scoring 4 or more to win together.",
  "players": {"min": 2, "max": 2, "suggested": 2},
  "parameters": {
    "deck_size": 12,
    "colours": 2,
    "red_colour_code": 1,
    "blue_colour_code": 2,
    "copies_of_rank_1_per_colour": 3,
    "copies_of_rank_2_per_colour": 2,
    "copies_of_rank_3_per_colour": 1,
    "hand_size": 2,
    "cards_left_after_deal": 8,
    "starting_hint_tokens": 3,
    "max_hint_tokens": 3,
    "starting_fuses": 3,
    "hint_cost": 1,
    "discard_gain": 1,
    "failed_play_fuse_loss": 1,
    "pile_start": 0,
    "pile_max": 3,
    "max_rounds": 12,
    "max_score": 6,
    "win_threshold": 4,
    "empty_slot_code": 0
  },
  "attributes": {
    "player": [
      {"key": "card_a", "type": "number", "visible": "others", "initial": 0, "meaning": "Code of the card in slot A (11/12/13 Red 1-3, 21/22/23 Blue 1-3, 0 empty). The partner sees it and the owner never does.", "observable": false},
      {"key": "card_b", "type": "number", "visible": "others", "initial": 0, "meaning": "Code of the card in slot B, same coding as card_a. The partner sees it and the owner never does.", "observable": false},
      {"key": "note_a", "type": "list", "visible": "public", "initial": [], "meaning": "Hint notes on the card in slot A, e.g. 'is Red', 'not 2'. Cleared when a new card is drawn into the slot.", "observable": false},
      {"key": "note_b", "type": "list", "visible": "public", "initial": [], "meaning": "Hint notes on the card in slot B. Cleared when a new card is drawn into the slot.", "observable": false},
      {"key": "score", "type": "number", "visible": "public", "initial": 0, "meaning": "Team score, equal to red_pile + blue_pile and identical for both seats.", "observable": true}
    ],
    "game": [
      {"key": "deck", "type": "list", "visible": "none", "initial": [11, 11, 11, 12, 12, 13, 21, 21, 21, 22, 22, 23], "meaning": "Face-down draw deck, shuffled once at setup. Cards are taken from the front, index 0.", "observable": false},
      {"key": "deck_left", "type": "number", "visible": "public", "initial": 12, "meaning": "Number of cards left in the deck. It is 8 after the deal.", "observable": false},
      {"key": "red_pile", "type": "number", "visible": "public", "initial": 0, "meaning": "Highest Red rank played successfully (0 to 3).", "observable": true},
      {"key": "blue_pile", "type": "number", "visible": "public", "initial": 0, "meaning": "Highest Blue rank played successfully (0 to 3).", "observable": true},
      {"key": "hints", "type": "number", "visible": "public", "initial": 3, "meaning": "Hint tokens available (0 to 3).", "observable": true},
      {"key": "fuses", "type": "number", "visible": "public", "initial": 3, "meaning": "Fuses remaining. The game ends when this reaches 0.", "observable": true},
      {"key": "discard", "type": "list", "visible": "public", "initial": [], "meaning": "Codes of discarded cards and of cards from failed plays.", "observable": true},
      {"key": "round_number", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of completed rounds.", "observable": false},
      {"key": "last_action", "type": "text", "visible": "public", "initial": "", "meaning": "The most recent action and its result: option chosen, card revealed, success or failure, hint named.", "observable": false},
      {"key": "action", "type": "text", "visible": "none", "initial": "", "meaning": "Scratch: the option chosen this turn by the active seat.", "observable": false}
    ]
  },
  "setup": [
    "Shuffle the deck list of 12 codes [11,11,11,12,12,13,21,21,21,22,22,23] into a random (seeded) order.",
    "Deal from the front of the deck: seat 1 card_a, then seat 1 card_b, then seat 2 card_a, then seat 2 card_b. Each dealt code is removed from deck.",
    "Set deck_left to 8.",
    "Set red_pile = 0, blue_pile = 0, hints = 3, fuses = 3, discard = [], round_number = 0, and last_action = ''.",
    "Set every note_a and note_b to [] and both scores to 0."
  ],
  "round": [
    {"action": "sync", "who": "seat 1", "answer": null, "effect": "Seat 1 is shown: seat 2's card_a and card_b; note_a and note_b of both seats; red_pile, blue_pile, hints, fuses; discard and deck_left; last_action. Seat 1's own card_a and card_b are not shown."},
    {"action": "ask", "who": "seat 1", "answer": "one of: Play A, Play B, Discard A, Discard B, Hint colour of partner's A, Hint colour of partner's B, Hint rank of partner's A, Hint rank of partner's B", "effect": "game.action = the chosen option"},
    {"action": "update", "who": "seat 1", "answer": null, "effect": "PLAY X (X = A or B), with c = seat 1 card_X: if c == 0, nothing changes. Otherwise colour = floor(c/10) and rank = c mod 10. If (colour == 1 and rank == red_pile + 1), then red_pile += 1. Else if (colour == 2 and rank == blue_pile + 1), then blue_pile += 1. Otherwise append c to discard and fuses -= 1. In every non-empty case, card_X is vacated (marked for drawing). DISCARD X: if c != 0, append c to discard, hints = min(3, hints + 1), and vacate card_X; if c == 0, nothing changes. HINT (colour or rank) of partner's X, with p = seat 2 card_X: if hints >= 1 and p != 0, then hints -= 1 and v = floor(p/10) (colour) or p mod 10 (rank). For each of seat 2's slots Y with card_Y != 0, append 'is V' to note_Y if the matching value equals v, else append 'not V'. V is the colour name (Red for 1, Blue for 2) or the rank number. Otherwise nothing changes and the turn is wasted. Set last_action to the option, any revealed code, success or failure, and any hint named."},
    {"action": "update", "who": "seat 1", "answer": null, "effect": "If seat 1's slot X was vacated this turn: if deck_left > 0, then card_X = deck[0], remove deck[0], deck_left -= 1, note_X = []. If deck_left == 0, then card_X = 0 and note_X = []."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Each seat's score = red_pile + blue_pile."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce last_action: the option seat 1 chose, any card code revealed, whether a play succeeded, and the hint named. Also announce red_pile, blue_pile, hints and fuses."},
    {"action": "check", "who": "all players", "answer": null, "effect": "End the game if fuses == 0 or (red_pile == 3 and blue_pile == 3); otherwise continue."},
    {"action": "sync", "who": "seat 2", "answer": null, "effect": "Seat 2 is shown: seat 1's card_a and card_b; note_a and note_b of both seats; red_pile, blue_pile, hints, fuses; discard and deck_left; last_action. Seat 2's own cards are not shown."},
    {"action": "ask", "who": "seat 2", "answer": "one of: Play A, Play B, Discard A, Discard B, Hint colour of partner's A, Hint colour of partner's B, Hint rank of partner's A, Hint rank of partner's B", "effect": "game.action = the chosen option"},
    {"action": "update", "who": "seat 2", "answer": null, "effect": "Same resolution as seat 1's resolution step, with seat 2 as the active seat and seat 1 as the partner: plays and discards act on seat 2's card_X, and hints act on seat 1's cards and notes. Set last_action accordingly."},
    {"action": "update", "who": "seat 2", "answer": null, "effect": "If seat 2's slot X was vacated this turn: if deck_left > 0, then card_X = deck[0], remove deck[0], deck_left -= 1, note_X = []. If deck_left == 0, then card_X = 0 and note_X = []."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Each seat's score = red_pile + blue_pile. round_number += 1."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce last_action for seat 2's turn (option, revealed card, success or failure, hint named), plus red_pile, blue_pile, hints and fuses."},
    {"action": "check", "who": "all players", "answer": null, "effect": "End the game if fuses == 0 or (red_pile == 3 and blue_pile == 3) or round_number >= 12; otherwise continue."}
  ],
  "ending": {
    "condition": "fuses == 0 OR (red_pile == 3 AND blue_pile == 3) OR round_number >= 12",
    "results": ["both seats win", "no seat wins"],
    "decided_by": "If red_pile + blue_pile (each seat's score) >= 4, the result is 'both seats win'; otherwise it is 'no seat wins'. This applies whichever ending condition triggered."
  },
  "rules": [
    {"id": "R1", "text": "When the game is set up, the deck contains exactly 12 cards: three each of 11 and 21, two each of 12 and 22, and one each of 13 and 23."},
    {"id": "R2", "text": "When the deal is done, each seat holds 2 cards (card_a and card_b), deck_left is 8, red_pile and blue_pile are 0, hints is 3, fuses is 3, discard is empty, all notes are empty and both scores are 0."},
    {"id": "R3", "text": "When a seat is shown its state, it sees its partner's card_a and card_b but never its own card_a or card_b."},
    {"id": "R4", "text": "When a seat plays a card whose rank equals its colour's pile + 1 (e.g. Red 1 on red_pile 0), then that pile increases by 1 and fuses are unchanged."},
    {"id": "R5", "text": "When a seat plays a card whose rank is not its colour's pile + 1 (e.g. Blue 2 on blue_pile 0), then the card's code is appended to discard and fuses decrease by 1."},
    {"id": "R6", "text": "When a seat plays or discards an empty slot (code 0), then nothing changes: no pile, fuse, hint or discard change, and no draw."},
    {"id": "R7", "text": "When a seat discards a non-empty slot, then the card's code is appended to discard and hints become min(3, hints + 1); with hints at 3, hints stay 3."},
    {"id": "R8", "text": "When a seat gives a hint with hints >= 1 and the named partner slot is non-empty, then hints decrease by 1."},
    {"id": "R9", "text": "When a colour hint names Red (or Blue), then each non-empty partner card gets the note 'is Red' if its colour is Red, and 'not Red' otherwise (likewise for Blue)."},
    {"id": "R10", "text": "When a rank hint names rank r, then each non-empty partner card gets the note 'is r' if its rank is r, and 'not r' otherwise."},
    {"id": "R11", "text": "When a seat gives a hint with hints == 0 or names an empty partner slot, then nothing changes and the turn is wasted."},
    {"id": "R12", "text": "When a card leaves a slot by play (successful or failed) or by discard and deck_left > 0, then the front card of the deck goes into that slot, deck_left decreases by 1 and that slot's note becomes empty."},
    {"id": "R13", "text": "When a card leaves a slot and deck_left == 0, then the slot becomes 0 and its note stays empty."},
    {"id": "R14", "text": "When any turn ends, then both seats' scores equal red_pile + blue_pile."},
    {"id": "R15", "text": "When any turn ends, then the chosen option, any revealed card, whether a play succeeded, and any hint named are announced to both seats."},
    {"id": "R16", "text": "When fuses reach 0 after any turn, then the game ends immediately."},
    {"id": "R17", "text": "When red_pile == 3 and blue_pile == 3 after any turn, then the game ends immediately with score 6."},
    {"id": "R18", "text": "When round 12 is completed (seat 2's 12th turn), then the game ends."},
    {"id": "R19", "text": "When the game ends with red_pile + blue_pile >= 4, then both seats win."},
    {"id": "R20", "text": "When the game ends with red_pile + blue_pile <= 3, then no seat wins."},
    {"id": "R21", "text": "When a round is played, then seat 1 takes its turn before seat 2."}
  ],
  "offers": [
    {"question": "Your turn: choose one action", "who": "the active seat (seat 1, then seat 2, each round)", "options": "In every situation, all 8 options: Play A, Play B, Discard A, Discard B, Hint colour of partner's A, Hint colour of partner's B, Hint rank of partner's A, Hint rank of partner's B. The rules define the outcome of each option even when a slot is empty or no hint token remains (nothing happens), so all 8 are always legal."}
  ],
  "choices": [
    {"what": "Exactly 2 players (min 2, max 2, suggested 2)", "why": "The designer fixed the game at 2 and the card counts, hand size and hint structure are built for a pair. The minimum is 2 because each player needs a partner to see their cards. The maximum stays 2 because the rules define 'partner' as a single other player. Strategy lies in choosing hints that convey the most, inferring meaning from a partner's hint choice, and deciding when to risk a play versus discard to regain tokens."},
    {"what": "No talk step", "why": "The rules forbid all communication besides the 8 actions; information must flow only through hints."},
    {"what": "All 8 options are always offered", "why": "The source specifies a result (nothing happens) for empty-slot plays and discards and for hints without tokens, so those choices are legal moves, just wasted ones."},
    {"what": "Results named 'both seats win' and 'no seat wins'", "why": "The game is cooperative with one shared outcome; the source gives no names for the results."},
    {"what": "Notes stored as one public list per slot", "why": "Both players see all four cards' notes, so each slot's notes are a public list that is cleared on draw."},
    {"what": "Discarding an empty slot gains no hint token", "why": "The source says 'If the slot is empty, nothing happens', which includes the token gain."}
  ],
  "simplifications": [
    {"what": "A turn is split into one resolution update and one draw update", "why": "The engine applies state changes as separate update steps; the order (resolve, then draw, then score) matches the source."},
    {"what": "The two turns of a round are written as two mirrored step blocks", "why": "The step list is flat, so seat 1's and seat 2's turns are each written out in order, with a check after each turn so the game ends immediately."}
  ],
  "unsupported": []
}
```
````
