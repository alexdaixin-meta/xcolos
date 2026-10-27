# 05 spec

- time: 2026-10-27T04:11:01+00:00 (85.2s)  model: claude-opus-5-5
- system prompt: [system/54cfed18-spec.md](system/54cfed18-spec.md) (sha256 54cfed18f9e94a06)
- sent sha256 1a4a743396289a49, reply sha256 3bb75ffdf15be33c

## Sent

````
Game: Hanabi: Three Fireworks
Players in the source: 2 to 4
Suggested table size, chosen by the designer of these rules (keep it): 3

Rules, as filed in the inventory:
CARDS. The deck has 30 cards in three colours: Red, Green and Blue. Each colour has three 1s, two 2s, two 3s, two 4s and one 5. A card is written as colour letter plus rank, for example R1 or B5. At the start, the deck is shuffled once and each card gets a permanent ID from #1 to #30 in shuffled order. An ID never reveals a card's face.

SETUP. With 2 players each hand has 5 cards; with 3 or 4 players each hand has 4 cards. Deal from the top of the deck in seat order. Each hand is an ordered list of card IDs, oldest first. The rest form the face-down deck: 20 cards with 2 players, 18 with 3, 14 with 4. The team starts with 8 hint tokens (never more than 8) and 3 fuses. There are three piles, Red, Green and Blue, each starting at 0. The target is 10 with 2 or 3 players and 9 with 4 players. Turns played starts at 0. The final-round counter starts at -1, meaning not started.

WHAT PLAYERS SEE. At the start of every turn the engine announces to everyone:
- the three pile values;
- the hint tokens and fuses remaining;
- the number of cards left in the deck;
- the turns played so far;
- the full discard pile, with faces;
- the full hint log.
The engine then sends the active player, privately, the colour and rank of every card in every other player's hand, together with the IDs only (never the faces) of the active player's own hand. A player never sees the faces of their own cards until those cards are played or discarded. How many copies of a card remain unseen can be worked out from the discard pile and the piles; the engine does not track it. There is no talk phase and no other communication.

TURN ORDER. Players take turns in seat order, starting with seat 1. On a turn, the active player gives exactly one answer, in one of these three forms.

(a) HINT <player> <colour or rank>. This needs at least 1 hint token. The named player must be someone else, and at least one card in their hand must match. The team spends 1 token. The engine announces to everyone which IDs in that hand match, and that every other ID currently in that hand does not match. The hint is added to the public log.

(b) DISCARD <ID>. The ID must be in your own hand. Remove it, reveal its face to everyone and put it face up in the discard pile. The team gains 1 hint token, up to a maximum of 8.

(c) PLAY <ID>. The ID must be in your own hand. Remove it and reveal its face to everyone.
- If its rank is exactly 1 more than the current value of its colour's pile, the play succeeds and that pile rises to the card's rank. If the pile has just reached 5, the team gains 1 hint token, up to a maximum of 8.
- Otherwise the play fails: the card goes face up to the discard pile and the team loses 1 fuse.

INVALID ANSWERS. An answer is invalid if it:
- has an unreadable form;
- is a hint given with 0 tokens;
- is a hint to yourself;
- is a hint that matches no card;
- names an ID not in your own hand.
An invalid answer is replaced by DISCARD of the oldest ID in the active player's hand.

DRAW. After a discard or a play, if the deck is not empty, the active player takes the top card into the end of their hand. Its ID is announced to everyone. Its face is visible only to the other players, through their private views.

FINAL ROUND. When the last card of the deck is drawn, the final-round counter is set to the number of players. On each later turn it drops by 1 at the end of that turn. So every player, starting with the next seat and ending with the player who drew the last card, gets exactly one more turn. No draws happen during these turns.

SCORE. After every turn, the team score is the sum of the three pile values (0 to 15). If the fuses are at 0, the team score is 0 instead. Every player's total is set to the team score.

END OF GAME. After every turn, the game ends if any of these is true:
- fuses are 0;
- the team score is 15;
- the final-round counter has reached 0;
- 40 turns have been played.

How the winner is decided: When the game ends, every player's total equals the team score: the sum of the three pile tops, or 0 if the last fuse was lost. If that total is at least the target (10 with 2 or 3 players, 9 with 4 players), every player wins together. Otherwise no player reaches the target, the team has lost, and the engine records the result as no winner (a shared draw). No player can ever win alone.
````

## Reply

````
```json
{
  "name": "Hanabi: Three Fireworks",
  "summary": "A cooperative card game for 2 to 4 players. Each player sees everyone's cards except their own, and the team uses hints, discards and plays to build three colour piles from 1 to 5 and reach a target score before the fuses run out.",
  "players": {"min": 2, "max": 4, "suggested": 3},
  "parameters": {
    "deck_size": 30,
    "colours": 3,
    "copies_rank_1": 3,
    "copies_rank_2": 2,
    "copies_rank_3": 2,
    "copies_rank_4": 2,
    "copies_rank_5": 1,
    "hand_size_2_players": 5,
    "hand_size_3_or_4_players": 4,
    "deck_after_deal_2_players": 20,
    "deck_after_deal_3_players": 18,
    "deck_after_deal_4_players": 14,
    "hint_tokens_start": 8,
    "hint_tokens_max": 8,
    "hint_cost": 1,
    "discard_token_gain": 1,
    "completed_pile_token_gain": 1,
    "fuses_start": 3,
    "failed_play_fuse_loss": 1,
    "pile_start": 0,
    "pile_max": 5,
    "target_2_or_3_players": 10,
    "target_4_players": 9,
    "max_team_score": 15,
    "max_turns": 40,
    "turns_played_start": 0,
    "final_round_counter_start": -1,
    "first_seat": 1
  },
  "attributes": {
    "player": [
      {"key": "hand_ids", "type": "list", "visible": "public", "initial": [], "meaning": "IDs of the cards in this player's hand, oldest first. IDs never reveal faces.", "observable": false},
      {"key": "hand_faces", "type": "list", "visible": "others", "initial": [], "meaning": "Faces of the cards in this player's hand (e.g. R3), kept parallel to hand_ids. Every player except the owner sees them.", "observable": false},
      {"key": "legal_options", "type": "list", "visible": "ally", "initial": [], "meaning": "The moves this player may choose on the current turn. Built only for the active player and seen only by them.", "observable": false},
      {"key": "total", "type": "number", "visible": "public", "initial": 0, "meaning": "The player's total. It always equals team_score.", "observable": true}
    ],
    "game": [
      {"key": "num_players", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of seats at the table.", "observable": false},
      {"key": "deck_ids", "type": "list", "visible": "none", "initial": [], "meaning": "IDs of the face-down deck, in order from the top.", "observable": false},
      {"key": "deck_faces", "type": "list", "visible": "none", "initial": [], "meaning": "Faces of the face-down deck, kept parallel to deck_ids.", "observable": false},
      {"key": "deck_count", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of cards left in the deck.", "observable": true},
      {"key": "pile_red", "type": "number", "visible": "public", "initial": 0, "meaning": "Value of the Red pile, 0 to 5.", "observable": true},
      {"key": "pile_green", "type": "number", "visible": "public", "initial": 0, "meaning": "Value of the Green pile, 0 to 5.", "observable": true},
      {"key": "pile_blue", "type": "number", "visible": "public", "initial": 0, "meaning": "Value of the Blue pile, 0 to 5.", "observable": true},
      {"key": "hint_tokens", "type": "number", "visible": "public", "initial": 8, "meaning": "Hint tokens remaining, 0 to 8.", "observable": true},
      {"key": "fuses", "type": "number", "visible": "public", "initial": 3, "meaning": "Fuses remaining.", "observable": true},
      {"key": "discard_pile", "type": "list", "visible": "public", "initial": [], "meaning": "Face-up discarded and failed cards, written as ID and face (e.g. #12=G2).", "observable": true},
      {"key": "hint_log", "type": "list", "visible": "public", "initial": [], "meaning": "Every hint given: who gave it, to whom, the colour or rank, the matching IDs and the non-matching IDs.", "observable": true},
      {"key": "turns_played", "type": "number", "visible": "public", "initial": 0, "meaning": "Turns completed so far.", "observable": true},
      {"key": "final_round_counter", "type": "number", "visible": "public", "initial": -1, "meaning": "-1 until the last card is drawn. It is then set to num_players and drops by 1 at the end of each later turn.", "observable": true},
      {"key": "counter_set_this_turn", "type": "bool", "visible": "public", "initial": false, "meaning": "True on the turn the last card of the deck is drawn, so the counter is not decremented on that turn.", "observable": false},
      {"key": "target", "type": "number", "visible": "public", "initial": 10, "meaning": "Score the team must reach: 10 with 2 or 3 players, 9 with 4.", "observable": false},
      {"key": "team_score", "type": "number", "visible": "public", "initial": 0, "meaning": "pile_red + pile_green + pile_blue, or 0 if fuses = 0.", "observable": true},
      {"key": "active_seat", "type": "number", "visible": "public", "initial": 1, "meaning": "Seat whose turn it is.", "observable": false},
      {"key": "last_move", "type": "text", "visible": "public", "initial": "", "meaning": "The move resolved this turn (HINT, DISCARD or PLAY with its arguments), after any invalid answer has been replaced.", "observable": false}
    ]
  },
  "setup": [
    "Set num_players to the number of seats.",
    "Set target to 10 if num_players is 2 or 3, and to 9 if num_players is 4.",
    "Build the 30 faces: for each of R, G and B, three 1s, two 2s, two 3s, two 4s and one 5.",
    "Shuffle the faces once. Give them the IDs #1 to #30 in shuffled order. Store the IDs in deck_ids and the faces in deck_faces, in the same order.",
    "Deal from the top of the deck, one card at a time in seat order starting with seat 1, until each hand has 5 cards (2 players) or 4 cards (3 or 4 players).",
    "Each dealt card is removed from the front of deck_ids and deck_faces and appended to the end of that seat's hand_ids and hand_faces, so hands are oldest first.",
    "Set deck_count to the number of cards left: 20 with 2 players, 18 with 3, 14 with 4.",
    "Set hint_tokens to 8, fuses to 3, and pile_red, pile_green and pile_blue to 0.",
    "Set turns_played to 0, final_round_counter to -1, team_score to 0, every total to 0, and active_seat to 1."
  ],
  "round": [
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce pile_red, pile_green, pile_blue, hint_tokens, fuses, deck_count, turns_played, the full discard_pile with faces, and the full hint_log."},
    {"action": "update", "who": "the seat equal to active_seat", "answer": null, "effect": "Build legal_options for the active seat. Add PLAY <ID> and DISCARD <ID> for every ID in their own hand_ids. If hint_tokens >= 1, also add HINT <seat> <X> for every other seat and every X in {R, G, B, 1, 2, 3, 4, 5} that matches at least one face in that seat's hand_faces."},
    {"action": "sync", "who": "the seat equal to active_seat", "answer": null, "effect": "Privately send the active seat the hand_faces and hand_ids of every other seat, their own hand_ids (never their own faces), and their legal_options."},
    {"action": "ask", "who": "the seat equal to active_seat", "answer": "one option from legal_options: PLAY <ID>, DISCARD <ID>, or HINT <seat> <colour or rank>", "effect": "Set last_move to the answer. If the answer is unreadable or not a legal move (a hint with 0 tokens, a hint to yourself, a hint matching no card, an ID not in your own hand), set last_move to DISCARD <first ID in own hand_ids>."},
    {"action": "update", "who": "the seat equal to active_seat", "answer": null, "effect": "When last_move is HINT <seat s> <X>: hint_tokens -= 1. Append to hint_log the giver, s, X, the IDs in s's hand_ids whose face matches X, and every other ID currently in s's hand_ids as not matching. Announce this to everyone."},
    {"action": "update", "who": "the seat equal to active_seat", "answer": null, "effect": "When last_move is DISCARD <ID>: remove the ID from hand_ids and its face from hand_faces. Append ID=face to discard_pile. hint_tokens = min(8, hint_tokens + 1). Announce the face to everyone."},
    {"action": "update", "who": "the seat equal to active_seat", "answer": null, "effect": "When last_move is PLAY <ID>: remove the ID and its face from the hand and announce the face. If the rank equals the matching pile (pile_red, pile_green or pile_blue) + 1, set that pile to the rank, and if the rank is 5, hint_tokens = min(8, hint_tokens + 1). Otherwise append ID=face to discard_pile and fuses -= 1."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Set counter_set_this_turn to false. If final_round_counter > 0, final_round_counter -= 1. This only happens on turns after the last-card turn, because the counter is still -1 until the draw step below sets it."},
    {"action": "update", "who": "the seat equal to active_seat", "answer": null, "effect": "When last_move is DISCARD or PLAY and deck_count > 0: move the first entry of deck_ids and deck_faces to the end of the active seat's hand_ids and hand_faces, deck_count -= 1, and announce the new ID to everyone. If deck_count is now 0, set final_round_counter to num_players and counter_set_this_turn to true."},
    {"action": "update", "who": "all players", "answer": null, "effect": "turns_played += 1. team_score = 0 if fuses = 0, otherwise pile_red + pile_green + pile_blue. Set every player's total to team_score."},
    {"action": "check", "who": "all players", "answer": null, "effect": "End the game if fuses = 0, or team_score = 15, or final_round_counter = 0, or turns_played = 40. Otherwise continue."},
    {"action": "update", "who": "all players", "answer": null, "effect": "active_seat = (active_seat mod num_players) + 1."}
  ],
  "ending": {
    "condition": "fuses == 0 OR team_score == 15 OR final_round_counter == 0 OR turns_played == 40",
    "results": ["all players win", "no winner"],
    "decided_by": "If team_score >= target (10 with 2 or 3 players, 9 with 4), the result is 'all players win'. Otherwise it is 'no winner' (a shared draw). No player can win alone."
  },
  "rules": [
    {"id": "R1", "text": "When the game is set up, the deck has 30 cards: for each of Red, Green and Blue, three 1s, two 2s, two 3s, two 4s and one 5."},
    {"id": "R2", "text": "When the deck is shuffled at setup, the cards get the IDs #1 to #30 in shuffled order, and an ID never reveals a face."},
    {"id": "R3", "text": "When there are 2 players, each hand starts with 5 cards and deck_count starts at 20."},
    {"id": "R4", "text": "When there are 3 players, each hand starts with 4 cards and deck_count starts at 18; when there are 4 players, each hand starts with 4 cards and deck_count starts at 14."},
    {"id": "R5", "text": "When the game starts, hint_tokens = 8, fuses = 3, pile_red = pile_green = pile_blue = 0, turns_played = 0 and final_round_counter = -1."},
    {"id": "R6", "text": "When there are 2 or 3 players, target = 10; when there are 4 players, target = 9."},
    {"id": "R7", "text": "When a turn starts, everyone is told the three piles, hint_tokens, fuses, deck_count, turns_played, the full discard_pile with faces, and the full hint_log."},
    {"id": "R8", "text": "When a seat is active, it privately sees the faces and IDs of every other hand, and only the IDs of its own hand."},
    {"id": "R9", "text": "When turns pass, seats act in order 1, 2, ..., num_players, then seat 1 again, starting with seat 1."},
    {"id": "R10", "text": "When a seat gives HINT s X with hint_tokens >= 1, s is another seat and at least one card in s's hand matches X, then hint_tokens drops by 1 and the matching and non-matching IDs of s's hand are announced and added to hint_log."},
    {"id": "R11", "text": "When hint_tokens = 0, a seat cannot give a hint."},
    {"id": "R12", "text": "When a seat names itself in a hint, or names a colour or rank that matches no card in the named hand, the hint is invalid."},
    {"id": "R13", "text": "When a seat discards an ID from its own hand, the card's face is revealed, it goes to discard_pile, and hint_tokens rises by 1, to at most 8."},
    {"id": "R14", "text": "When a seat discards with hint_tokens = 8, hint_tokens stays at 8."},
    {"id": "R15", "text": "When a seat plays a card whose rank is exactly 1 more than its colour's pile, that pile becomes the card's rank."},
    {"id": "R16", "text": "When a successful play brings a pile to 5, hint_tokens rises by 1, to at most 8."},
    {"id": "R17", "text": "When a seat plays a card whose rank is not exactly 1 more than its colour's pile, the card goes face up to discard_pile and fuses drops by 1."},
    {"id": "R18", "text": "When an answer is unreadable, a hint at 0 tokens, a hint to oneself, a hint matching no card, or names an ID not in one's own hand, it is replaced by DISCARD of the oldest ID in the active seat's hand."},
    {"id": "R19", "text": "When a seat discards or plays and deck_count > 0, the top deck card is added to the end of its hand, its ID is announced, and deck_count drops by 1."},
    {"id": "R20", "text": "When a seat gives a hint, no card is drawn."},
    {"id": "R21", "text": "When the last deck card is drawn, final_round_counter is set to num_players."},
    {"id": "R22", "text": "When final_round_counter > 0 at the end of a turn after the one that drew the last card, final_round_counter drops by 1."},
    {"id": "R23", "text": "When final_round_counter has been set, no further cards are drawn because deck_count = 0."},
    {"id": "R24", "text": "When a turn ends, team_score = pile_red + pile_green + pile_blue, or 0 if fuses = 0, and every player's total = team_score."},
    {"id": "R25", "text": "When fuses reach 0 at the end of a turn, the game ends."},
    {"id": "R26", "text": "When team_score reaches 15 at the end of a turn, the game ends."},
    {"id": "R27", "text": "When final_round_counter reaches 0 at the end of a turn, the game ends."},
    {"id": "R28", "text": "When turns_played reaches 40, the game ends."},
    {"id": "R29", "text": "When the game ends with team_score >= target, every player wins together."},
    {"id": "R30", "text": "When the game ends with team_score < target, the result is no winner."}
  ],
  "offers": [
    {"question": "The active seat's move each turn", "who": "the seat equal to active_seat", "options": "With hint_tokens >= 1: PLAY <ID> and DISCARD <ID> for each ID in own hand_ids, plus HINT <seat> <X> for every other seat and every X in {R, G, B, 1, 2, 3, 4, 5} that matches at least one card in that seat's hand. With hint_tokens = 0: only PLAY <ID> and DISCARD <ID> for each ID in own hand_ids. The active seat is never offered a hint to itself, a hint matching no card, or an ID outside its own hand."},
    {"question": "Any other question", "who": "seats that are not active", "options": "None. Seats that are not active are not asked anything; there is no talk phase."}
  ],
  "choices": [
    {"what": "2 to 4 players, suggested 3", "why": "The designer suggested 3, so it is kept. The minimum is 2 because hidden-hand cooperation needs at least one teammate who can see your cards. The maximum is 4 because larger tables shrink hands and the deck, and each player's turns grow rare. The key skill is giving hints whose meaning a teammate can read from the timing and from which IDs they mark, while saving tokens and avoiding risky plays."},
    {"what": "No talk phase", "why": "The rules forbid all communication except hints, so no talk poll is added."},
    {"what": "Moves offered as a choice list (legal_options) instead of free text", "why": "This keeps answers readable and ensures a seat is never offered an illegal move. The invalid-answer fallback, DISCARD of the oldest ID, is kept for unreadable replies."},
    {"what": "Dealing goes one card at a time around the table in seat order", "why": "The source says 'deal from the top in seat order' without saying whether cards go one at a time or a full hand at once. Since the deck is shuffled, the outcome is the same in distribution."},
    {"what": "A hand is stored as two parallel lists, hand_ids (public) and hand_faces (others)", "why": "IDs are announced to everyone, while faces must be hidden from the owner only."},
    {"what": "Final-round timing uses the flag counter_set_this_turn and a decrement step placed before the draw step", "why": "This gives each player, from the next seat through the player who drew the last card, exactly one more turn."},
    {"what": "Game results are named 'all players win' and 'no winner'", "why": "The source describes a shared win or a shared loss recorded as no winner."}
  ],
  "simplifications": [
    {"what": "hand_faces is visible to every non-owner at all times, not only to the active player during their private view", "why": "The engine's 'others' visibility is per attribute. Teammates seeing the faces off-turn changes no decision, because only the active player acts and there is no talk."},
    {"what": "The deck is an ordered hidden list and drawing takes its first entry", "why": "This matches 'take the top card'. Drawing at random from a shuffled deck would be equivalent."}
  ],
  "unsupported": []
}
```
````
