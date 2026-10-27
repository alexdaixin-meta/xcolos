# 06 scenarios

- time: 2026-10-27T04:12:26+00:00 (163.8s)  model: claude-opus-5-5
- system prompt: [system/5914d71d-scenarios.md](system/5914d71d-scenarios.md) (sha256 5914d71de58bb622)
- sent sha256 dfaa1ca44cb1e6ce, reply sha256 a0b5a0f437f3a339

## Sent

````
SPEC:
{
  "name": "Hanabi: Three Fireworks",
  "summary": "A cooperative card game for 2 to 4 players. Each player sees everyone's cards except their own, and the team uses hints, discards and plays to build three colour piles from 1 to 5 and reach a target score before the fuses run out.",
  "players": {
    "min": 2,
    "max": 4,
    "suggested": 3
  },
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
      {
        "key": "hand_ids",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "IDs of the cards in this player's hand, oldest first. IDs never reveal faces.",
        "observable": false
      },
      {
        "key": "hand_faces",
        "type": "list",
        "visible": "others",
        "initial": [],
        "meaning": "Faces of the cards in this player's hand (e.g. R3), kept parallel to hand_ids. Every player except the owner sees them.",
        "observable": false
      },
      {
        "key": "legal_options",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "The moves this player may choose on the current turn. Built only for the active player and seen only by them.",
        "observable": false
      },
      {
        "key": "total",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The player's total. It always equals team_score.",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "num_players",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of seats at the table.",
        "observable": false
      },
      {
        "key": "deck_ids",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "IDs of the face-down deck, in order from the top.",
        "observable": false
      },
      {
        "key": "deck_faces",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "Faces of the face-down deck, kept parallel to deck_ids.",
        "observable": false
      },
      {
        "key": "deck_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of cards left in the deck.",
        "observable": true
      },
      {
        "key": "pile_red",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Value of the Red pile, 0 to 5.",
        "observable": true
      },
      {
        "key": "pile_green",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Value of the Green pile, 0 to 5.",
        "observable": true
      },
      {
        "key": "pile_blue",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Value of the Blue pile, 0 to 5.",
        "observable": true
      },
      {
        "key": "hint_tokens",
        "type": "number",
        "visible": "public",
        "initial": 8,
        "meaning": "Hint tokens remaining, 0 to 8.",
        "observable": true
      },
      {
        "key": "fuses",
        "type": "number",
        "visible": "public",
        "initial": 3,
        "meaning": "Fuses remaining.",
        "observable": true
      },
      {
        "key": "discard_pile",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Face-up discarded and failed cards, written as ID and face (e.g. #12=G2).",
        "observable": true
      },
      {
        "key": "hint_log",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Every hint given: who gave it, to whom, the colour or rank, the matching IDs and the non-matching IDs.",
        "observable": true
      },
      {
        "key": "turns_played",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Turns completed so far.",
        "observable": true
      },
      {
        "key": "final_round_counter",
        "type": "number",
        "visible": "public",
        "initial": -1,
        "meaning": "-1 until the last card is drawn. It is then set to num_players and drops by 1 at the end of each later turn.",
        "observable": true
      },
      {
        "key": "counter_set_this_turn",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "True on the turn the last card of the deck is drawn, so the counter is not decremented on that turn.",
        "observable": false
      },
      {
        "key": "target",
        "type": "number",
        "visible": "public",
        "initial": 10,
        "meaning": "Score the team must reach: 10 with 2 or 3 players, 9 with 4.",
        "observable": false
      },
      {
        "key": "team_score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "pile_red + pile_green + pile_blue, or 0 if fuses = 0.",
        "observable": true
      },
      {
        "key": "active_seat",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Seat whose turn it is.",
        "observable": false
      },
      {
        "key": "last_move",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The move resolved this turn (HINT, DISCARD or PLAY with its arguments), after any invalid answer has been replaced.",
        "observable": false
      }
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
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce pile_red, pile_green, pile_blue, hint_tokens, fuses, deck_count, turns_played, the full discard_pile with faces, and the full hint_log."
    },
    {
      "action": "update",
      "who": "the seat equal to active_seat",
      "answer": null,
      "effect": "Build legal_options for the active seat. Add PLAY <ID> and DISCARD <ID> for every ID in their own hand_ids. If hint_tokens >= 1, also add HINT <seat> <X> for every other seat and every X in {R, G, B, 1, 2, 3, 4, 5} that matches at least one face in that seat's hand_faces."
    },
    {
      "action": "sync",
      "who": "the seat equal to active_seat",
      "answer": null,
      "effect": "Privately send the active seat the hand_faces and hand_ids of every other seat, their own hand_ids (never their own faces), and their legal_options."
    },
    {
      "action": "ask",
      "who": "the seat equal to active_seat",
      "answer": "one option from legal_options: PLAY <ID>, DISCARD <ID>, or HINT <seat> <colour or rank>",
      "effect": "Set last_move to the answer. If the answer is unreadable or not a legal move (a hint with 0 tokens, a hint to yourself, a hint matching no card, an ID not in your own hand), set last_move to DISCARD <first ID in own hand_ids>."
    },
    {
      "action": "update",
      "who": "the seat equal to active_seat",
      "answer": null,
      "effect": "When last_move is HINT <seat s> <X>: hint_tokens -= 1. Append to hint_log the giver, s, X, the IDs in s's hand_ids whose face matches X, and every other ID currently in s's hand_ids as not matching. Announce this to everyone."
    },
    {
      "action": "update",
      "who": "the seat equal to active_seat",
      "answer": null,
      "effect": "When last_move is DISCARD <ID>: remove the ID from hand_ids and its face from hand_faces. Append ID=face to discard_pile. hint_tokens = min(8, hint_tokens + 1). Announce the face to everyone."
    },
    {
      "action": "update",
      "who": "the seat equal to active_seat",
      "answer": null,
      "effect": "When last_move is PLAY <ID>: remove the ID and its face from the hand and announce the face. If the rank equals the matching pile (pile_red, pile_green or pile_blue) + 1, set that pile to the rank, and if the rank is 5, hint_tokens = min(8, hint_tokens + 1). Otherwise append ID=face to discard_pile and fuses -= 1."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Set counter_set_this_turn to false. If final_round_counter > 0, final_round_counter -= 1. This only happens on turns after the last-card turn, because the counter is still -1 until the draw step below sets it."
    },
    {
      "action": "update",
      "who": "the seat equal to active_seat",
      "answer": null,
      "effect": "When last_move is DISCARD or PLAY and deck_count > 0: move the first entry of deck_ids and deck_faces to the end of the active seat's hand_ids and hand_faces, deck_count -= 1, and announce the new ID to everyone. If deck_count is now 0, set final_round_counter to num_players and counter_set_this_turn to true."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "turns_played += 1. team_score = 0 if fuses = 0, otherwise pile_red + pile_green + pile_blue. Set every player's total to team_score."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if fuses = 0, or team_score = 15, or final_round_counter = 0, or turns_played = 40. Otherwise continue."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "active_seat = (active_seat mod num_players) + 1."
    }
  ],
  "ending": {
    "condition": "fuses == 0 OR team_score == 15 OR final_round_counter == 0 OR turns_played == 40",
    "results": [
      "all players win",
      "no winner"
    ],
    "decided_by": "If team_score >= target (10 with 2 or 3 players, 9 with 4), the result is 'all players win'. Otherwise it is 'no winner' (a shared draw). No player can win alone."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game is set up, the deck has 30 cards: for each of Red, Green and Blue, three 1s, two 2s, two 3s, two 4s and one 5."
    },
    {
      "id": "R2",
      "text": "When the deck is shuffled at setup, the cards get the IDs #1 to #30 in shuffled order, and an ID never reveals a face."
    },
    {
      "id": "R3",
      "text": "When there are 2 players, each hand starts with 5 cards and deck_count starts at 20."
    },
    {
      "id": "R4",
      "text": "When there are 3 players, each hand starts with 4 cards and deck_count starts at 18; when there are 4 players, each hand starts with 4 cards and deck_count starts at 14."
    },
    {
      "id": "R5",
      "text": "When the game starts, hint_tokens = 8, fuses = 3, pile_red = pile_green = pile_blue = 0, turns_played = 0 and final_round_counter = -1."
    },
    {
      "id": "R6",
      "text": "When there are 2 or 3 players, target = 10; when there are 4 players, target = 9."
    },
    {
      "id": "R7",
      "text": "When a turn starts, everyone is told the three piles, hint_tokens, fuses, deck_count, turns_played, the full discard_pile with faces, and the full hint_log."
    },
    {
      "id": "R8",
      "text": "When a seat is active, it privately sees the faces and IDs of every other hand, and only the IDs of its own hand."
    },
    {
      "id": "R9",
      "text": "When turns pass, seats act in order 1, 2, ..., num_players, then seat 1 again, starting with seat 1."
    },
    {
      "id": "R10",
      "text": "When a seat gives HINT s X with hint_tokens >= 1, s is another seat and at least one card in s's hand matches X, then hint_tokens drops by 1 and the matching and non-matching IDs of s's hand are announced and added to hint_log."
    },
    {
      "id": "R11",
      "text": "When hint_tokens = 0, a seat cannot give a hint."
    },
    {
      "id": "R12",
      "text": "When a seat names itself in a hint, or names a colour or rank that matches no card in the named hand, the hint is invalid."
    },
    {
      "id": "R13",
      "text": "When a seat discards an ID from its own hand, the card's face is revealed, it goes to discard_pile, and hint_tokens rises by 1, to at most 8."
    },
    {
      "id": "R14",
      "text": "When a seat discards with hint_tokens = 8, hint_tokens stays at 8."
    },
    {
      "id": "R15",
      "text": "When a seat plays a card whose rank is exactly 1 more than its colour's pile, that pile becomes the card's rank."
    },
    {
      "id": "R16",
      "text": "When a successful play brings a pile to 5, hint_tokens rises by 1, to at most 8."
    },
    {
      "id": "R17",
      "text": "When a seat plays a card whose rank is not exactly 1 more than its colour's pile, the card goes face up to discard_pile and fuses drops by 1."
    },
    {
      "id": "R18",
      "text": "When an answer is unreadable, a hint at 0 tokens, a hint to oneself, a hint matching no card, or names an ID not in one's own hand, it is replaced by DISCARD of the oldest ID in the active seat's hand."
    },
    {
      "id": "R19",
      "text": "When a seat discards or plays and deck_count > 0, the top deck card is added to the end of its hand, its ID is announced, and deck_count drops by 1."
    },
    {
      "id": "R20",
      "text": "When a seat gives a hint, no card is drawn."
    },
    {
      "id": "R21",
      "text": "When the last deck card is drawn, final_round_counter is set to num_players."
    },
    {
      "id": "R22",
      "text": "When final_round_counter > 0 at the end of a turn after the one that drew the last card, final_round_counter drops by 1."
    },
    {
      "id": "R23",
      "text": "When final_round_counter has been set, no further cards are drawn because deck_count = 0."
    },
    {
      "id": "R24",
      "text": "When a turn ends, team_score = pile_red + pile_green + pile_blue, or 0 if fuses = 0, and every player's total = team_score."
    },
    {
      "id": "R25",
      "text": "When fuses reach 0 at the end of a turn, the game ends."
    },
    {
      "id": "R26",
      "text": "When team_score reaches 15 at the end of a turn, the game ends."
    },
    {
      "id": "R27",
      "text": "When final_round_counter reaches 0 at the end of a turn, the game ends."
    },
    {
      "id": "R28",
      "text": "When turns_played reaches 40, the game ends."
    },
    {
      "id": "R29",
      "text": "When the game ends with team_score >= target, every player wins together."
    },
    {
      "id": "R30",
      "text": "When the game ends with team_score < target, the result is no winner."
    }
  ],
  "offers": [
    {
      "question": "The active seat's move each turn",
      "who": "the seat equal to active_seat",
      "options": "With hint_tokens >= 1: PLAY <ID> and DISCARD <ID> for each ID in own hand_ids, plus HINT <seat> <X> for every other seat and every X in {R, G, B, 1, 2, 3, 4, 5} that matches at least one card in that seat's hand. With hint_tokens = 0: only PLAY <ID> and DISCARD <ID> for each ID in own hand_ids. The active seat is never offered a hint to itself, a hint matching no card, or an ID outside its own hand."
    },
    {
      "question": "Any other question",
      "who": "seats that are not active",
      "options": "None. Seats that are not active are not asked anything; there is no talk phase."
    }
  ],
  "choices": [
    {
      "what": "2 to 4 players, suggested 3",
      "why": "The designer suggested 3, so it is kept. The minimum is 2 because hidden-hand cooperation needs at least one teammate who can see your cards. The maximum is 4 because larger tables shrink hands and the deck, and each player's turns grow rare. The key skill is giving hints whose meaning a teammate can read from the timing and from which IDs they mark, while saving tokens and avoiding risky plays."
    },
    {
      "what": "No talk phase",
      "why": "The rules forbid all communication except hints, so no talk poll is added."
    },
    {
      "what": "Moves offered as a choice list (legal_options) instead of free text",
      "why": "This keeps answers readable and ensures a seat is never offered an illegal move. The invalid-answer fallback, DISCARD of the oldest ID, is kept for unreadable replies."
    },
    {
      "what": "Dealing goes one card at a time around the table in seat order",
      "why": "The source says 'deal from the top in seat order' without saying whether cards go one at a time or a full hand at once. Since the deck is shuffled, the outcome is the same in distribution."
    },
    {
      "what": "A hand is stored as two parallel lists, hand_ids (public) and hand_faces (others)",
      "why": "IDs are announced to everyone, while faces must be hidden from the owner only."
    },
    {
      "what": "Final-round timing uses the flag counter_set_this_turn and a decrement step placed before the draw step",
      "why": "This gives each player, from the next seat through the player who drew the last card, exactly one more turn."
    },
    {
      "what": "Game results are named 'all players win' and 'no winner'",
      "why": "The source describes a shared win or a shared loss recorded as no winner."
    }
  ],
  "simplifications": [
    {
      "what": "hand_faces is visible to every non-owner at all times, not only to the active player during their private view",
      "why": "The engine's 'others' visibility is per attribute. Teammates seeing the faces off-turn changes no decision, because only the active player acts and there is no talk."
    },
    {
      "what": "The deck is an ordered hidden list and drawing takes its first entry",
      "why": "This matches 'take the top card'. Drawing at random from a shuffled deck would be equivalent."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: total; table: deck_count, pile_red, pile_green, pile_blue, hint_tokens, fuses, discard_pile, hint_log, turns_played, final_round_counter, team_score.
````

## Reply

````
```json
[
  {"name": "R1: 2 players, the 30 cards are split into 20 in the deck and 5 in each hand (counts only, the shuffle is random)", "rule": "R1", "players": 2, "seed": 1, "rounds": 0,
   "expect": {"game": {"deck_count": 20},
              "lens": {"game": {"deck_ids": 20, "deck_faces": 20}, "players": {"1": {"hand_ids": 5, "hand_faces": 5}, "2": {"hand_ids": 5, "hand_faces": 5}}}}},

  {"name": "R1: 4 players, the 30 cards are split into 14 in the deck and 4 in each hand (counts only)", "rule": "R1", "players": 4, "seed": 2, "rounds": 0,
   "expect": {"game": {"deck_count": 14},
              "lens": {"game": {"deck_ids": 14, "deck_faces": 14}, "players": {"1": {"hand_ids": 4}, "2": {"hand_ids": 4}, "3": {"hand_ids": 4}, "4": {"hand_ids": 4}}}}},

  {"name": "R2: 3 players, deck IDs and face lists are parallel after the deal (counts only)", "rule": "R2", "players": 3, "seed": 3, "rounds": 0,
   "expect": {"game": {"deck_count": 18},
              "lens": {"game": {"deck_ids": 18, "deck_faces": 18}, "players": {"1": {"hand_ids": 4, "hand_faces": 4}, "2": {"hand_ids": 4, "hand_faces": 4}, "3": {"hand_ids": 4, "hand_faces": 4}}}}},

  {"name": "R3: 2 players start with 5 cards each and deck_count 20", "rule": "R3", "players": 2, "seed": 4, "rounds": 0,
   "expect": {"game": {"deck_count": 20}, "lens": {"players": {"1": {"hand_ids": 5}, "2": {"hand_ids": 5}}}}},

  {"name": "R4: 3 players start with 4 cards each and deck_count 18", "rule": "R4", "players": 3, "seed": 5, "rounds": 0,
   "expect": {"game": {"deck_count": 18}, "lens": {"players": {"1": {"hand_ids": 4}, "2": {"hand_ids": 4}, "3": {"hand_ids": 4}}}}},

  {"name": "R4: 4 players start with 4 cards each and deck_count 14", "rule": "R4", "players": 4, "seed": 6, "rounds": 0,
   "expect": {"game": {"deck_count": 14}, "lens": {"players": {"1": {"hand_ids": 4}, "2": {"hand_ids": 4}, "3": {"hand_ids": 4}, "4": {"hand_ids": 4}}}}},

  {"name": "R5: starting tokens, fuses, piles, turns and final-round counter", "rule": "R5", "players": 3, "seed": 7, "rounds": 0,
   "expect": {"game": {"hint_tokens": 8, "fuses": 3, "pile_red": 0, "pile_green": 0, "pile_blue": 0, "turns_played": 0, "final_round_counter": -1, "team_score": 0, "discard_pile": [], "hint_log": []},
              "players": {"1": {"total": 0}, "2": {"total": 0}, "3": {"total": 0}}}},

  {"name": "R6: with 4 players the target is 9, so the game ends on the final counter with score 9 and all players win", "rule": "R6", "players": 4, "seed": 8, "default": "decline",
   "given": {"players": {"1": {"hand_ids": ["#1", "#2", "#3", "#4"], "hand_faces": ["R1", "G1", "B1", "R2"]}},
             "game": {"deck_ids": [], "deck_faces": [], "deck_count": 0, "final_round_counter": 1, "pile_red": 3, "pile_green": 3, "pile_blue": 3}},
   "rules": [{"seat": 1, "options_include": "DISCARD #2"}],
   "expect": {"result": "all players win", "game": {"team_score": 9, "final_round_counter": 0},
              "players": {"1": {"total": 9}, "2": {"total": 9}, "3": {"total": 9}, "4": {"total": 9}}}},

  {"name": "R6: with 2 players the target is 10, so the game ends with score 10 and all players win", "rule": "R6", "players": 2, "seed": 9, "default": "decline",
   "given": {"players": {"1": {"hand_ids": ["#1", "#2", "#3", "#4", "#5"], "hand_faces": ["R1", "G1", "B1", "R2", "G2"]}},
             "game": {"deck_ids": [], "deck_faces": [], "deck_count": 0, "final_round_counter": 1, "pile_red": 4, "pile_green": 3, "pile_blue": 3}},
   "rules": [{"seat": 1, "options_include": "DISCARD #2"}],
   "expect": {"result": "all players win", "game": {"team_score": 10}, "players": {"1": {"total": 10}, "2": {"total": 10}}}},

  {"name": "R7: after one turn the announced public state shows the hint and the turn count", "rule": "R7", "players": 3, "seed": 10, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand_ids": ["#1", "#2", "#3", "#4"], "hand_faces": ["R1", "G1", "B1", "R2"]},
                         "2": {"hand_ids": ["#5", "#6", "#7", "#8"], "hand_faces": ["R3", "G2", "B4", "G1"]},
                         "3": {"hand_ids": ["#9", "#10", "#11", "#12"], "hand_faces": ["B1", "R4", "G3", "R1"]}},
             "game": {"deck_ids": ["#13", "#14", "#15", "#16", "#17"], "deck_faces": ["G4", "B2", "R5", "G5", "B3"], "deck_count": 5}},
   "rules": [{"seat": 1, "options_include": "HINT 2 G"}],
   "expect": {"game": {"turns_played": 1, "hint_tokens": 7, "deck_count": 5, "fuses": 3, "discard_pile": []}, "lens": {"game": {"hint_log": 1}}}},

  {"name": "R8: the active seat is offered hints built from the other seats' faces, never a hint to itself", "rule": "R8", "players": 3, "seed": 11, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand_ids": ["#1", "#2", "#3", "#4"], "hand_faces": ["R1", "G1", "B1", "R2"]},
                         "2": {"hand_ids": ["#5", "#6", "#7", "#8"], "hand_faces": ["R3", "G2", "B4", "G1"]},
                         "3": {"hand_ids": ["#9", "#10", "#11", "#12"], "hand_faces": ["B1", "R4", "G3", "R1"]}},
             "game": {"deck_ids": ["#13", "#14", "#15", "#16", "#17"], "deck_faces": ["G4", "B2", "R5", "G5", "B3"], "deck_count": 5}},
   "rules": [{"seat": 1, "options_include": "HINT 2 G"}],
   "expect": {"offered": [{"seat": 1, "option": "HINT 2 G"}, {"seat": 1, "option": "HINT 2 4"}, {"seat": 1, "option": "HINT 3 B"}, {"seat": 1, "option": "PLAY #1"}, {"seat": 1, "option": "DISCARD #4"}],
              "not_offered": [{"seat": 1, "option": "HINT 1 R"}, {"seat": 1, "option": "HINT 1 1"}, {"seat": 1, "option": "PLAY #5"}, {"seat": 2, "option": "DISCARD #5"}]}},

  {"name": "R9: seat 1 acts first and then seat 2, and seat 3 has not acted after two turns", "rule": "R9", "players": 3, "seed": 12, "rounds": 2, "default": "decline",
   "given": {"players": {"1": {"hand_ids": ["#1", "#2", "#3", "#4"], "hand_faces": ["R1", "G1", "B1", "R2"]},
                         "2": {"hand_ids": ["#5", "#6", "#7", "#8"], "hand_faces": ["R3", "G2", "B4", "G1"]},
                         "3": {"hand_ids": ["#9", "#10", "#11", "#12"], "hand_faces": ["B1", "R4", "G3", "R1"]}},
             "game": {"deck_ids": ["#13", "#14", "#15", "#16", "#17"], "deck_faces": ["G4", "B2", "R5", "G5", "B3"], "deck_count": 5, "hint_tokens": 4}},
   "rules": [{"seat": 1, "options_include": "DISCARD #1"}, {"seat": 2, "options_include": "DISCARD #5"}, {"seat": 3, "options_include": "DISCARD #9"}],
   "expect": {"game": {"discard_pile": ["#1=R1", "#5=R3"], "turns_played": 2, "hint_tokens": 6, "deck_count": 3},
              "offered": [{"seat": 2, "option": "DISCARD #5"}],
              "not_offered": [{"seat": 3, "option": "DISCARD #9"}]}},

  {"name": "R9: after seat 3, play returns to seat 1", "rule": "R9", "players": 3, "seed": 13, "rounds": 4, "default": "decline",
   "given": {"players": {"1": {"hand_ids": ["#1", "#2", "#3", "#4"], "hand_faces": ["R1", "G1", "B1", "R2"]},
                         "2": {"hand_ids": ["#5", "#6", "#7", "#8"], "hand_faces": ["R3", "G2", "B4", "G1"]},
                         "3": {"hand_ids": ["#9", "#10", "#11", "#12"], "hand_faces": ["B1", "R4", "G3", "R1"]}},
             "game": {"deck_ids": ["#13", "#14", "#15", "#16", "#17"], "deck_faces": ["G4", "B2", "R5", "G5", "B3"], "deck_count": 5, "hint_tokens": 2}},
   "rules": [{"seat": 1, "options_include": "DISCARD #1"}, {"seat": 1, "options_include": "DISCARD #2"},
             {"seat": 2, "options_include": "DISCARD #5"}, {"seat": 3, "options_include": "DISCARD #9"}],
   "expect": {"game": {"discard_pile": ["#1=R1", "#5=R3", "#9=B1", "#2=G1"], "turns_played": 4, "hint_tokens": 6, "deck_count": 1}}},

  {"name": "R10: a valid colour hint costs 1 token and is logged", "rule": "R10", "players": 3, "seed": 14, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand_ids": ["#1", "#2", "#3", "#4"], "hand_faces": ["R1", "G1", "B1", "R2"]},
                         "2": {"hand_ids": ["#5", "#6", "#7", "#8"], "hand_faces": ["R3", "G2", "B4", "G1"]},
                         "3": {"hand_ids": ["#9", "#10", "#11", "#12"], "hand_faces": ["B1", "R4", "G3", "R1"]}},
             "game": {"deck_ids": ["#13", "#14", "#15", "#16", "#17"], "deck_faces": ["G4", "B2", "R5", "G5", "B3"], "deck_count": 5, "hint_tokens": 5}},
   "rules": [{"seat": 1, "options_include": "HINT 2 G"}],
   "expect": {"game": {"hint_tokens": 4, "discard_pile": [], "fuses": 3, "pile_green": 0, "turns_played": 1}, "lens": {"game": {"hint_log": 1}}}},

  {"name": "R11: with 0 hint tokens no hint is offered and a discard regains a token", "rule": "R11", "players": 3, "seed": 15, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand_ids": ["#1", "#2", "#3", "#4"], "hand_faces": ["R1", "G1", "B1", "R2"]},
                         "2": {"hand_ids": ["#5", "#6", "#7", "#8"], "hand_faces": ["R3", "G2", "B4", "G1"]},
                         "3": {"hand_ids": ["#9", "#10", "#11", "#12"], "hand_faces": ["B1", "R4", "G3", "R1"]}},
             "game": {"deck_ids": ["#13", "#14", "#15", "#16", "#17"], "deck_faces": ["G4", "B2", "R5", "G5", "B3"], "deck_count": 5, "hint_tokens": 0}},
   "rules": [{"seat": 1, "options_include": "DISCARD #1"}],
   "expect": {"game": {"hint_tokens": 1, "discard_pile": ["#1=R1"], "hint_log": []},
              "offered": [{"seat": 1, "option": "DISCARD #1"}, {"seat": 1, "option": "PLAY #1"}],
              "not_offered": [{"seat": 1, "option": "HINT 2 G"}, {"seat": 1, "option": "HINT 3 B"}, {"seat": 1, "option": "HINT 2 R"}]}},

  {"name": "R12: hints to oneself and hints that match no card are not offered", "rule": "R12", "players": 3, "seed": 16, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand_ids": ["#1", "#2", "#3", "#4"], "hand_faces": ["R1", "G1", "B1", "R2"]},
                         "2": {"hand_ids": ["#5", "#6", "#7", "#8"], "hand_faces": ["R3", "G2", "B4", "G1"]},
                         "3": {"hand_ids": ["#9", "#10", "#11", "#12"], "hand_faces": ["B1", "R4", "G3", "R1"]}},
             "game": {"deck_ids": ["#13", "#14", "#15", "#16", "#17"], "deck_faces": ["G4", "B2", "R5", "G5", "B3"], "deck_count": 5}},
   "rules": [{"seat": 1, "options_include": "DISCARD #1"}],
   "expect": {"not_offered": [{"seat": 1, "option": "HINT 1 R"}, {"seat": 1, "option": "HINT 1 G"}, {"seat": 1, "option": "HINT 2 5"}, {"seat": 1, "option": "HINT 3 2"}, {"seat": 1, "option": "HINT 3 5"}],
              "offered": [{"seat": 1, "option": "HINT 2 1"}, {"seat": 1, "option": "HINT 3 G"}]}},

  {"name": "R12: an answered hint to oneself is invalid and becomes a discard of the oldest card", "rule": "R12", "players": 3, "seed": 17, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand_ids": ["#1", "#2", "#3", "#4"], "hand_faces": ["R1", "G1", "B1", "R2"]},
                         "2": {"hand_ids": ["#5", "#6", "#7", "#8"], "hand_faces": ["R3", "G2", "B4", "G1"]},
                         "3": {"hand_ids": ["#9", "#10", "#11", "#12"], "hand_faces": ["B1", "R4", "G3", "R1"]}},
             "game": {"deck_ids": ["#13", "#14", "#15", "#16", "#17"], "deck_faces": ["G4", "B2", "R5", "G5", "B3"], "deck_count": 5, "hint_tokens": 6}},
   "rules": [{"seat": 1, "options_include": "HINT 2 G", "answer": "HINT 1 R"}],
   "expect": {"game": {"hint_tokens": 7, "discard_pile": ["#1=R1"], "hint_log": [], "deck_count": 4}}},

  {"name": "R13: a discard reveals the card, adds it to the discard pile and gains 1 token", "rule": "R13", "players": 3, "seed": 18, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand_ids": ["#1", "#2", "#3", "#4"], "hand_faces": ["R1", "G1", "B1", "R2"]},
                         "2": {"hand_ids": ["#5", "#6", "#7", "#8"], "hand_faces": ["R3", "G2", "B4", "G1"]},
                         "3": {"hand_ids": ["#9", "#10", "#11", "#12"], "hand_faces": ["B1", "R4", "G3", "R1"]}},
             "game": {"deck_ids": ["#13", "#14", "#15", "#16", "#17"], "deck_faces": ["G4", "B2", "R5", "G5", "B3"], "deck_count": 5, "hint_tokens": 5}},
   "rules": [{"seat": 1, "options_include": "DISCARD #2"}],
   "expect": {"game": {"hint_tokens": 6, "discard_pile": ["#2=G1"], "pile_green": 0, "fuses": 3}}},

  {"name": "R14: a discard at 8 tokens leaves the tokens at 8", "rule": "R14", "players": 3, "seed": 19, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand_ids": ["#1", "#2", "#3", "#4"], "hand_faces": ["R1", "G1", "B1", "R2"]},
                         "2": {"hand_ids": ["#5", "#6", "#7", "#8"], "hand_faces": ["R3", "G2", "B4", "G1"]},
                         "3": {"hand_ids": ["#9", "#10", "#11", "#12"], "hand_faces": ["B1", "R4", "G3", "R1"]}},
             "game": {"deck_ids": ["#13", "#14", "#15", "#16", "#17"], "deck_faces": ["G4", "B2", "R5", "G5", "B3"], "deck_count": 5, "hint_tokens": 8}},
   "rules": [{"seat": 1, "options_include": "DISCARD #3"}],
   "expect": {"game": {"hint_tokens": 8, "discard_pile": ["#3=B1"]}}},

  {"name": "R15: playing R1 onto an empty red pile sets the red pile to 1", "rule": "R15", "players": 3, "seed": 20, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand_ids": ["#1", "#2", "#3", "#4"], "hand_faces": ["R1", "G1", "B1", "R2"]},
                         "2": {"hand_ids": ["#5", "#6", "#7", "#8"], "hand_faces": ["R3", "G2", "B4", "G1"]},
                         "3": {"hand_ids": ["#9", "#10", "#11", "#12"], "hand_faces": ["B1", "R4", "G3", "R1"]}},
             "game": {"deck_ids": ["#13", "#14", "#15", "#16", "#17"], "deck_faces": ["G4", "B2", "R5", "G5", "B3"], "deck_count": 5}},
   "rules": [{"seat": 1, "options_include": "PLAY #1"}],
   "expect": {"game": {"pile_red": 1, "fuses": 3, "discard_pile": [], "hint_tokens": 8, "team_score": 1},
              "players": {"1": {"total": 1}, "2": {"total": 1}, "3": {"total": 1}}}},

  {"name": "R16: completing the red pile with R5 gains 1 hint token", "rule": "R16", "players": 3, "seed": 21, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand_ids": ["#1", "#2", "#3", "#4"], "hand_faces": ["R5", "G1", "B1", "R2"]},
                         "2": {"hand_ids": ["#5", "#6", "#7", "#8"], "hand_faces": ["R3", "G2", "B4", "G1"]},
                         "3": {"hand_ids": ["#9", "#10", "#11", "#12"], "hand_faces": ["B1", "R4", "G3", "R1"]}},
             "game": {"deck_ids": ["#13", "#14", "#15", "#16", "#17"], "deck_faces": ["G4", "B2", "R1", "G5", "B3"], "deck_count": 5, "pile_red": 4, "hint_tokens": 6}},
   "rules": [{"seat": 1, "options_include": "PLAY #1"}],
   "expect": {"game": {"pile_red": 5, "hint_tokens": 7, "fuses": 3, "team_score": 5}, "players": {"1": {"total": 5}}}},

  {"name": "R17: playing R2 onto an empty red pile fails, goes to the discard pile and costs a fuse", "rule": "R17", "players": 3, "seed": 22, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand_ids": ["#1", "#2", "#3", "#4"], "hand_faces": ["R1", "G1", "B1", "R2"]},
                         "2": {"hand_ids": ["#5", "#6", "#7", "#8"], "hand_faces": ["R3", "G2", "B4", "G1"]},
                         "3": {"hand_ids": ["#9", "#10", "#11", "#12"], "hand_faces": ["B1", "R4", "G3", "R1"]}},
             "game": {"deck_ids": ["#13", "#14", "#15", "#16", "#17"], "deck_faces": ["G4", "B2", "R5", "G5", "B3"], "deck_count": 5, "hint_tokens": 5}},
   "rules": [{"seat": 1, "options_include": "PLAY #4"}],
   "expect": {"game": {"pile_red": 0, "fuses": 2, "discard_pile": ["#4=R2"], "hint_tokens": 5, "team_score": 0, "deck_count": 4}}},

  {"name": "R18: an unreadable answer becomes a discard of the oldest card", "rule": "R18", "players": 3, "seed": 23, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand_ids": ["#1", "#2", "#3", "#4"], "hand_faces": ["R1", "G1", "B1", "R2"]},
                         "2": {"hand_ids": ["#5", "#6", "#7", "#8"], "hand_faces": ["R3", "G2", "B4", "G1"]},
                         "3": {"hand_ids": ["#9", "#10", "#11", "#12"], "hand_faces": ["B1", "R4", "G3", "R1"]}},
             "game": {"deck_ids": ["#13", "#14", "#15", "#16", "#17"], "deck_faces": ["G4", "B2", "R5", "G5", "B3"], "deck_count": 5, "hint_tokens": 6}},
   "rules": [{"seat": 1, "options_include": "PLAY #3", "answer": "xyzzy blah"}],
   "expect": {"game": {"discard_pile": ["#1=R1"], "pile_red": 0, "pile_blue": 0, "hint_tokens": 7, "fuses": 3, "deck_count": 4}}},

  {"name": "R18: naming an ID not in one's own hand becomes a discard of the oldest card", "rule": "R18", "players": 3, "seed": 24, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand_ids": ["#1", "#2", "#3", "#4"], "hand_faces": ["R1", "G1", "B1", "R2"]},
                         "2": {"hand_ids": ["#5", "#6", "#7", "#8"], "hand_faces": ["R3", "G2", "B4", "G1"]},
                         "3": {"hand_ids": ["#9", "#10", "#11", "#12"], "hand_faces": ["B1", "R4", "G3", "R1"]}},
             "game": {"deck_ids": ["#13", "#14", "#15", "#16", "#17"], "deck_faces": ["G4", "B2", "R5", "G5", "B3"], "deck_count": 5, "hint_tokens": 6}},
   "rules": [{"seat": 1, "options_include": "PLAY #2", "answer": "PLAY #8"}],
   "expect": {"game": {"discard_pile": ["#1=R1"], "pile_green": 0, "pile_red": 0, "hint_tokens": 7, "fuses": 3}}},

  {"name": "R18: a hint answered at 0 tokens becomes a discard of the oldest card", "rule": "R18", "players": 3, "seed": 25, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand_ids": ["#1", "#2", "#3", "#4"], "hand_faces": ["R1", "G1", "B1", "R2"]},
                         "2": {"hand_ids": ["#5", "#6", "#7", "#8"], "hand_faces": ["R3", "G2", "B4", "G1"]},
                         "3": {"hand_ids": ["#9", "#10", "#11", "#12"], "hand_faces": ["B1", "R4", "G3", "R1"]}},
             "game": {"deck_ids": ["#13", "#14", "#15", "#16", "#17"], "deck_faces": ["G4", "B2", "R5", "G5", "B3"], "deck_count": 5, "hint_tokens": 0}},
   "rules": [{"seat": 1, "options_include": "DISCARD #3", "answer": "HINT 2 G"}],
   "expect": {"game": {"discard_pile": ["#1=R1"], "hint_tokens": 1, "hint_log": []}}},

  {"name": "R19: a play draws the top deck card, so the hand stays at 4 and deck_count drops by 1", "rule": "R19", "players": 3, "seed": 26, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand_ids": ["#1", "#2", "#3", "#4"], "hand_faces": ["R1", "G1", "B1", "R2"]},
                         "2": {"hand_ids": ["#5", "#6", "#7", "#8"], "hand_faces": ["R3", "G2", "B4", "G1"]},
                         "3": {"hand_ids": ["#9", "#10", "#11", "#12"], "hand_faces": ["B1", "R4", "G3", "R1"]}},
             "game": {"deck_ids": ["#13", "#14", "#15", "#16", "#17"], "deck_faces": ["G4", "B2", "R5", "G5", "B3"], "deck_count": 5}},
   "rules": [{"seat": 1, "options_include": "PLAY #1"}],
   "expect": {"game": {"deck_count": 4, "pile_red": 1, "final_round_counter": -1},
              "lens": {"players": {"1": {"hand_ids": 4, "hand_faces": 4}}, "game": {"deck_ids": 4}}}},

  {"name": "R20: a hint draws no card", "rule": "R20", "players": 3, "seed": 27, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand_ids": ["#1", "#2", "#3", "#4"], "hand_faces": ["R1", "G1", "B1", "R2"]},
                         "2": {"hand_ids": ["#5", "#6", "#7", "#8"], "hand_faces": ["R3", "G2", "B4", "G1"]},
                         "3": {"hand_ids": ["#9", "#10", "#11", "#12"], "hand_faces": ["B1", "R4", "G3", "R1"]}},
             "game": {"deck_ids": ["#13", "#14", "#15", "#16", "#17"], "deck_faces": ["G4", "B2", "R5", "G5", "B3"], "deck_count": 5}},
   "rules": [{"seat": 1, "options_include": "HINT 3 R"}],
   "expect": {"game": {"deck_count": 5, "hint_tokens": 7},
              "lens": {"players": {"1": {"hand_ids": 4}, "3": {"hand_ids": 4}}, "game": {"deck_ids": 5}}}},

  {"name": "R21: drawing the last deck card with 3 players sets final_round_counter to 3", "rule": "R21", "players": 3, "seed": 28, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand_ids": ["#1", "#2", "#3", "#4"], "hand_faces": ["R1", "G1", "B1", "R2"]},
                         "2": {"hand_ids": ["#5", "#6", "#7", "#8"], "hand_faces": ["R3", "G2", "B4", "G1"]},
                         "3": {"hand_ids": ["#9", "#10", "#11", "#12"], "hand_faces": ["B1", "R4", "G3", "R1"]}},
             "game": {"deck_ids": ["#13"], "deck_faces": ["G4"], "deck_count": 1}},
   "rules": [{"seat": 1, "options_include": "DISCARD #2"}],
   "expect": {"game": {"deck_count": 0, "final_round_counter": 3, "turns_played": 1}, "lens": {"players": {"1": {"hand_ids": 4}}}}},

  {"name": "R21: drawing the last deck card with 2 players sets final_round_counter to 2", "rule": "R21", "players": 2, "seed": 29, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand_ids": ["#1", "#2", "#3", "#4", "#5"], "hand_faces": ["R1", "G1", "B1", "R2", "G2"]}},
             "game": {"deck_ids": ["#13"], "deck_faces": ["G4"], "deck_count": 1}},
   "rules": [{"seat": 1, "options_include": "DISCARD #2"}],
   "expect": {"game": {"deck_count": 0, "final_round_counter": 2}}},

  {"name": "R22: a turn after the last draw lowers final_round_counter from 3 to 2", "rule": "R22", "players": 3, "seed": 30, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand_ids": ["#1", "#2", "#3", "#4"], "hand_faces": ["R1", "G1", "B1", "R2"]},
                         "2": {"hand_ids": ["#5", "#6", "#7", "#8"], "hand_faces": ["R3", "G2", "B4", "G1"]},
                         "3": {"hand_ids": ["#9", "#10", "#11", "#12"], "hand_faces": ["B1", "R4", "G3", "R1"]}},
             "game": {"deck_ids": [], "deck_faces": [], "deck_count": 0, "final_round_counter": 3}},
   "rules": [{"seat": 1, "options_include": "DISCARD #2"}],
   "expect": {"game": {"final_round_counter": 2, "deck_count": 0}}},

  {"name": "R23: with the deck empty a play draws nothing, so the hand shrinks to 3", "rule": "R23", "players": 3, "seed": 31, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand_ids": ["#1", "#2", "#3", "#4"], "hand_faces": ["R1", "G1", "B1", "R2"]},
                         "2": {"hand_ids": ["#5", "#6", "#7", "#8"], "hand_faces": ["R3", "G2", "B4", "G1"]},
                         "3": {"hand_ids": ["#9", "#10", "#11", "#12"], "hand_faces": ["B1", "R4", "G3", "R1"]}},
             "game": {"deck_ids": [], "deck_faces": [], "deck_count": 0, "final_round_counter": 2}},
   "rules": [{"seat": 1, "options_include": "PLAY #1"}],
   "expect": {"game": {"deck_count": 0, "pile_red": 1, "final_round_counter": 1}, "lens": {"players": {"1": {"hand_ids": 3, "hand_faces": 3}}}}},

  {"name": "R24: team_score and every total equal the sum of the piles after a turn", "rule": "R24", "players": 3, "seed": 32, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand_ids": ["#1", "#2", "#3", "#4"], "hand_faces": ["R1", "G1", "B1", "R2"]},
                         "2": {"hand_ids": ["#5", "#6", "#7", "#8"], "hand_faces": ["R3", "G2", "B4", "G1"]},
                         "3": {"hand_ids": ["#9", "#10", "#11", "#12"], "hand_faces": ["B1", "R4", "G3", "R1"]}},
             "game": {"deck_ids": ["#13", "#14", "#15", "#16", "#17"], "deck_faces": ["G4", "B2", "R5", "G5", "B3"], "deck_count": 5, "pile_green": 2, "pile_blue": 1}},
   "rules": [{"seat": 1, "options_include": "PLAY #1"}],
   "expect": {"game": {"pile_red": 1, "pile_green": 2, "pile_blue": 1, "team_score": 4},
              "players": {"1": {"total": 4}, "2": {"total": 4}, "3": {"total": 4}}}},

  {"name": "R25: a failed play on the last fuse ends the game with score 0 and no winner", "rule": "R25", "players": 3, "seed": 33, "default": "decline",
   "given": {"players": {"1": {"hand_ids": ["#1", "#2", "#3", "#4"], "hand_faces": ["R1", "G1", "B1", "R2"]},
                         "2": {"hand_ids": ["#5", "#6", "#7", "#8"], "hand_faces": ["R3", "G2", "B4", "G1"]},
                         "3": {"hand_ids": ["#9", "#10", "#11", "#12"], "hand_faces": ["B1", "R4", "G3", "R1"]}},
             "game": {"deck_ids": ["#13", "#14", "#15", "#16", "#17"], "deck_faces": ["G4", "B2", "R5", "G5", "B3"], "deck_count": 5, "fuses": 1, "pile_red": 3, "pile_green": 4, "pile_blue": 4}},
   "rules": [{"seat": 1, "options_include": "PLAY #4"}],
   "expect": {"result": "no winner", "game": {"fuses": 0, "team_score": 0, "discard_pile": ["#4=R2"], "pile_red": 3},
              "players": {"1": {"total": 0}, "2": {"total": 0}, "3": {"total": 0}}}},

  {"name": "R26: completing the last pile reaches 15 and ends the game with all players winning", "rule": "R26", "players": 3, "seed": 34, "default": "decline",
   "given": {"players": {"1": {"hand_ids": ["#1", "#2", "#3", "#4"], "hand_faces": ["R5", "G1", "B1", "R2"]},
                         "2": {"hand_ids": ["#5", "#6", "#7", "#8"], "hand_faces": ["R3", "G2", "B4", "G1"]},
                         "3": {"hand_ids": ["#9", "#10", "#11", "#12"], "hand_faces": ["B1", "R4", "G3", "R1"]}},
             "game": {"deck_ids": ["#13", "#14", "#15", "#16", "#17"], "deck_faces": ["G4", "B2", "R1", "G1", "B3"], "deck_count": 5, "pile_red": 4, "pile_green": 5, "pile_blue": 5, "hint_tokens": 8}},
   "rules": [{"seat": 1, "options_include": "PLAY #1"}],
   "expect": {"result": "all players win", "game": {"pile_red": 5, "team_score": 15, "hint_tokens": 8, "turns_played": 1},
              "players": {"1": {"total": 15}, "2": {"total": 15}, "3": {"total": 15}}}},

  {"name": "R27: final_round_counter reaching 0 ends the game (score 12 with 3 players, so all players win)", "rule": "R27", "players": 3, "seed": 35, "default": "decline",
   "given": {"players": {"1": {"hand_ids": ["#1", "#2", "#3", "#4"], "hand_faces": ["R1", "G1", "B1", "R2"]},
                         "2": {"hand_ids": ["#5", "#6", "#7", "#8"], "hand_faces": ["R3", "G2", "B4", "G1"]},
                         "3": {"hand_ids": ["#9", "#10", "#11", "#12"], "hand_faces": ["B1", "R4", "G3", "R1"]}},
             "game": {"deck_ids": [], "deck_faces": [], "deck_count": 0, "final_round_counter": 1, "pile_red": 4, "pile_green": 4, "pile_blue": 4}},
   "rules": [{"seat": 1, "options_include": "DISCARD #2"}],
   "expect": {"result": "all players win", "game": {"final_round_counter": 0, "team_score": 12, "turns_played": 1},
              "players": {"1": {"total": 12}}, "lens": {"players": {"1": {"hand_ids": 3}}}}},

  {"name": "R28: the 40th turn ends the game (score 0, so no winner)", "rule": "R28", "players": 3, "seed": 36, "default": "decline",
   "given": {"players": {"1": {"hand_ids": ["#1", "#2", "#3", "#4"], "hand_faces": ["R1", "G1", "B1", "R2"]},
                         "2": {"hand_ids": ["#5", "#6", "#7", "#8"], "hand_faces": ["R3", "G2", "B4", "G1"]},
                         "3": {"hand_ids": ["#9", "#10", "#11", "#12"], "hand_faces": ["B1", "R4", "G3", "R1"]}},
             "game": {"deck_ids": ["#13", "#14", "#15", "#16", "#17"], "deck_faces": ["G4", "B2", "R5", "G5", "B3"], "deck_count": 5, "turns_played": 39}},
   "rules": [{"seat": 1, "options_include": "DISCARD #2"}],
   "expect": {"result": "no winner", "game": {"turns_played": 40, "team_score": 0, "deck_count": 4}}},

  {"name": "R29: the game ends with score exactly 10 with 3 players, so all players win", "rule": "R29", "players": 3, "seed": 37, "default": "decline",
   "given": {"players": {"1": {"hand_ids": ["#1", "#2", "#3", "#4"], "hand_faces": ["R1", "G1", "B1", "R2"]},
                         "2": {"hand_ids": ["#5", "#6", "#7", "#8"], "hand_faces": ["R3", "G2", "B4", "G1"]},
                         "3": {"hand_ids": ["#9", "#10", "#11", "#12"], "hand_faces": ["B1", "R4", "G3", "R1"]}},
             "game": {"deck_ids": [], "deck_faces": [], "deck_count": 0, "final_round_counter": 1, "pile_red": 4, "pile_green": 3, "pile_blue": 3}},
   "rules": [{"seat": 1, "options_include": "DISCARD #2"}],
   "expect": {"result": "all players win", "game": {"team_score": 10},
              "players": {"1": {"total": 10}, "2": {"total": 10}, "3": {"total": 10}}}},

  {"name": "R30: the game ends with score 9 with 3 players (target 10), so there is no winner", "rule": "R30", "players": 3, "seed": 38, "default": "decline",
   "given": {"players": {"1": {"hand_ids": ["#1", "#2", "#3", "#4"], "hand_faces": ["R1", "G1", "B1", "R2"]},
                         "2": {"hand_ids": ["#5", "#6", "#7", "#8"], "hand_faces": ["R3", "G2", "B4", "G1"]},
                         "3": {"hand_ids": ["#9", "#10", "#11", "#12"], "hand_faces": ["B1", "R4", "G3", "R1"]}},
             "game": {"deck_ids": [], "deck_faces": [], "deck_count": 0, "final_round_counter": 1, "pile_red": 4, "pile_green": 3, "pile_blue": 2}},
   "rules": [{"seat": 1, "options_include": "DISCARD #2"}],
   "expect": {"result": "no winner", "game": {"team_score": 9},
              "players": {"1": {"total": 9}, "2": {"total": 9}, "3": {"total": 9}}}}
]
```
````
