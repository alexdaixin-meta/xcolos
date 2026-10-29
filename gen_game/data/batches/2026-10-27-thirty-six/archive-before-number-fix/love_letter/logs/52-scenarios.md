# 52 scenarios

- time: 2026-10-27T19:40:16+00:00 (110.6s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 24abd308047681a5, reply sha256 7782ea38a68d9589

## Sent

````
SPEC:
{
  "name": "Love Letter Duel: Long Courtship",
  "summary": "A two-player Love Letter duel over exactly 40 turns. Each turn one player draws, discards one of two cards and resolves its effect. Winning a hand earns a token; most tokens wins, with total discarded ranks as the tie-break.",
  "players": {
    "min": 2,
    "max": 2,
    "suggested": 2
  },
  "parameters": {
    "total_rounds": 40,
    "deck_size": 16,
    "guard_count": 5,
    "priest_count": 2,
    "baron_count": 2,
    "handmaid_count": 2,
    "prince_count": 2,
    "king_count": 1,
    "countess_count": 1,
    "princess_count": 1,
    "guard_rank": 1,
    "priest_rank": 2,
    "baron_rank": 3,
    "handmaid_rank": 4,
    "prince_rank": 5,
    "king_rank": 6,
    "countess_rank": 7,
    "princess_rank": 8,
    "out_of_play_size": 6,
    "face_up_out_of_play": 5,
    "burned_cards": 1,
    "cards_dealt_per_player": 1,
    "deck_count_after_deal": 8,
    "guard_guess_min": 2,
    "guard_guess_max": 8,
    "tokens_per_hand_won": 1,
    "starting_tokens": 0,
    "starting_career_sum": 0,
    "starting_active_seat": 1,
    "rank_tiebreak_multiplier": 1000
  },
  "attributes": {
    "player": [
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "Ranks of the cards in this player's hand: 1 card between turns, 2 during their own turn.",
        "observable": false
      },
      {
        "key": "discards",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Ranks this player has discarded this hand, in order.",
        "observable": true
      },
      {
        "key": "discard_sum",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Sum of ranks discarded this hand; reset at each new hand.",
        "observable": false
      },
      {
        "key": "career_sum",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Sum of all ranks discarded over the whole game, including cards a Prince forced out.",
        "observable": true
      },
      {
        "key": "tokens",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Hands won.",
        "observable": true
      },
      {
        "key": "protected",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "1 if protected by a Handmaid until this player's next turn starts.",
        "observable": false
      },
      {
        "key": "eliminated",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "1 if knocked out of the current hand.",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [
          1,
          1,
          1,
          1,
          1,
          2,
          2,
          3,
          3,
          4,
          4,
          5,
          5,
          6,
          7,
          8
        ],
        "meaning": "Ranks of the undrawn cards; order is hidden.",
        "observable": false
      },
      {
        "key": "burned_card",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "Out-of-play position 1: the face-down burned card (0 or 1 rank).",
        "observable": false
      },
      {
        "key": "face_up",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Out-of-play positions 2-6: five face-up ranks.",
        "observable": true
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
        "key": "active_seat",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Seat taking this round's turn.",
        "observable": false
      },
      {
        "key": "hand_over",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "1 if a new hand must be dealt at the start of the next round.",
        "observable": false
      },
      {
        "key": "discard_choice",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Rank the active player discards this turn.",
        "observable": false
      },
      {
        "key": "guess",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Rank named with a Guard.",
        "observable": false
      },
      {
        "key": "round_number",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Current round, from 1 to 40.",
        "observable": true
      },
      {
        "key": "new_hand",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "Scratch flag: 1 if a hand was dealt this round.",
        "observable": false
      },
      {
        "key": "token_awarded",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "Scratch flag: 1 if a token was awarded this round.",
        "observable": false
      }
    ]
  },
  "setup": [
    "Two seats are filled. Each player starts with tokens 0 and career_sum 0, an empty hand and empty discards.",
    "The table starts with active_seat 1, hand_over 1 and round_number 0. The deck holds all 16 ranks: 1 x5, 2 x2, 3 x2, 4 x2, 5 x2, 6, 7, 8."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round_number += 1; new_hand = 0; token_awarded = 0."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When hand_over = 1: empty every hand, every player's discards, burned_card and face_up, and set deck to all 16 ranks. Draw 1 random rank from deck into burned_card, then 5 random ranks from deck into face_up. Draw 1 random rank from deck into each player's hand. Set deck_count = 8. For both players set protected = 0, eliminated = 0 and discard_sum = 0. Set hand_over = 0 and new_hand = 1."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "When new_hand = 1, announce: 'The face-up out-of-play cards are ranks {face_up}.'"
    },
    {
      "action": "update",
      "who": "seat active_seat",
      "answer": null,
      "effect": "Set the active player's protected = 0. Move 1 random rank from deck to the active player's hand; deck_count -= 1. Privately tell the active player: 'You kept rank X and just drew rank Y.'"
    },
    {
      "action": "ask",
      "who": "seat active_seat",
      "answer": "one of the ranks in their hand",
      "effect": "Store the chosen rank in discard_choice."
    },
    {
      "action": "update",
      "who": "seat active_seat",
      "answer": null,
      "effect": "Countess: if the active player's hand contains 7 and also contains 5 or 6, set discard_choice = 7."
    },
    {
      "action": "update",
      "who": "seat active_seat",
      "answer": null,
      "effect": "Move one card of rank discard_choice from the active player's hand to their discards. Add discard_choice to their discard_sum and career_sum. Announce 'Seat s discards rank r (name).'"
    },
    {
      "action": "ask",
      "who": "seat active_seat",
      "answer": "a whole number from 2 to 8",
      "effect": "When discard_choice = 1: store the number in guess."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When discard_choice = 1: if the opponent's protected = 1, announce no effect. Otherwise, if the opponent's hand card = guess, set the opponent's eliminated = 1 and announce a hit; if not, announce a miss."
    },
    {
      "action": "update",
      "who": "seat active_seat",
      "answer": null,
      "effect": "When discard_choice = 2: if the opponent's protected = 1, announce no effect. Otherwise privately tell the active player the opponent's hand rank, and announce 'Seat s looked at Seat o's card.'"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When discard_choice = 3: if the opponent's protected = 1, announce no effect. Otherwise compare the two hand cards. The owner of the lower one gets eliminated = 1, and the loser and the losing rank are announced. If the cards are equal, announce a tie and nobody is out."
    },
    {
      "action": "update",
      "who": "seat active_seat",
      "answer": null,
      "effect": "When discard_choice = 4: set the active player's protected = 1 and announce it."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When discard_choice = 5: the target is the opponent, or the active player if the opponent's protected = 1. Move the target's hand card to their discards, add its rank to their discard_sum and career_sum, and announce the rank. If the rank was 8, set the target's eliminated = 1. Otherwise, if deck_count > 0, move 1 random rank from deck to the target's hand and deck_count -= 1; if deck_count = 0, move the burned_card rank to the target's hand."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When discard_choice = 6: if the opponent's protected = 1, announce no effect. Otherwise swap the two players' hand lists and announce the swap."
    },
    {
      "action": "update",
      "who": "seat active_seat",
      "answer": null,
      "effect": "When discard_choice = 8: set the active player's eliminated = 1 and announce it."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Showdown, when the sum of eliminated = 0 and (deck_count = 0 or round_number = 40): announce both hand ranks. The owner of the lower hand card gets eliminated = 1. If the cards are equal, the owner of the lower discard_sum gets eliminated = 1. If those are also equal, announce that the hand is tied and set hand_over = 1."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Award, when the sum of eliminated = 1: the player with eliminated = 0 gains tokens += 1, and the new total is announced. Set hand_over = 1, token_awarded = 1, and active_seat = the seat of the eliminated player."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Pass, when token_awarded = 0: active_seat = 3 - active_seat."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if round_number = 40; otherwise continue."
    }
  ],
  "ending": {
    "condition": "round_number = 40",
    "rank_by": "you.tokens * 1000 + you.career_sum",
    "decided_by": "The player with more tokens wins. If tokens are equal, the higher career_sum wins. If both are equal, the players share the result as a draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "The deck has 16 cards: rank 1 x5, rank 2 x2, rank 3 x2, rank 4 x2, rank 5 x2, rank 6 x1, rank 7 x1, rank 8 x1."
    },
    {
      "id": "R2",
      "text": "When hand_over = 1 at the start of a round, then all 16 cards are gathered, 1 goes to burned_card, 5 go face up to face_up, each player gets 1 card, deck_count = 8, protected, eliminated and discard_sum are 0 for both players, and hand_over = 0."
    },
    {
      "id": "R3",
      "text": "When a new hand is dealt, then the 5 face_up ranks are announced and the burned card stays hidden."
    },
    {
      "id": "R4",
      "text": "When a turn starts, then the active player's protected = 0, they draw 1 card from the deck, deck_count drops by 1, and they are privately told the rank they kept and the rank they drew."
    },
    {
      "id": "R5",
      "text": "When the active player chooses a rank, then it is stored in discard_choice."
    },
    {
      "id": "R6",
      "text": "When the active player holds rank 7 together with rank 5 or rank 6, then discard_choice = 7."
    },
    {
      "id": "R7",
      "text": "When a card is discarded, then it moves to the player's discards, its rank is added to discard_sum and career_sum, and 'Seat s discards rank r (name)' is announced."
    },
    {
      "id": "R8",
      "text": "When discard_choice = 1, then the active player names a rank from 2 to 8 as guess."
    },
    {
      "id": "R9",
      "text": "When a Guard is played against a protected opponent, then it has no effect."
    },
    {
      "id": "R10",
      "text": "When a Guard's guess equals an unprotected opponent's card, then the opponent's eliminated = 1 and a hit is announced; otherwise a miss is announced."
    },
    {
      "id": "R11",
      "text": "When a Priest is played against an unprotected opponent, then the active player is privately told the opponent's rank and the look is announced publicly; against a protected opponent it has no effect."
    },
    {
      "id": "R12",
      "text": "When a Baron is played against an unprotected opponent, then the holder of the lower hand card gets eliminated = 1 and the losing rank is announced; on equal cards a tie is announced and nobody is out."
    },
    {
      "id": "R13",
      "text": "When a Handmaid is played, then the active player's protected = 1 until their next turn starts."
    },
    {
      "id": "R14",
      "text": "When a Prince is played, then its target is the opponent, or the active player if the opponent is protected."
    },
    {
      "id": "R15",
      "text": "When a Prince target discards, then the rank is added to the target's discard_sum and career_sum and announced; if it was rank 8, the target's eliminated = 1."
    },
    {
      "id": "R16",
      "text": "When a Prince target did not discard rank 8, then the target draws from the deck if deck_count > 0 (deck_count drops by 1); otherwise the target takes the burned card."
    },
    {
      "id": "R17",
      "text": "When a King is played against an unprotected opponent, then the two hand cards are swapped and the swap is announced; against a protected opponent it has no effect."
    },
    {
      "id": "R18",
      "text": "When a Princess is discarded by the active player, then their eliminated = 1."
    },
    {
      "id": "R19",
      "text": "When nobody is eliminated and (deck_count = 0 or it is round 40), then both hands are revealed and the lower card's owner gets eliminated = 1."
    },
    {
      "id": "R20",
      "text": "When showdown cards are equal, then the lower discard_sum is eliminated; if discard_sum is also equal, then the hand is tied, no token is awarded, and hand_over = 1."
    },
    {
      "id": "R21",
      "text": "When exactly one player is eliminated, then the other gains 1 token, hand_over = 1, and the eliminated player is active_seat for the next hand."
    },
    {
      "id": "R22",
      "text": "When no token was awarded in a round, then active_seat switches to the other seat."
    },
    {
      "id": "R23",
      "text": "When round 40 ends, then the game ends; more tokens wins, then higher career_sum, and if both are equal it is a draw."
    }
  ],
  "offers": [
    {
      "question": "Which rank to discard",
      "who": "the active seat",
      "options": "If the hand contains 7 together with 5 or 6: only 7. Otherwise: each distinct rank in their two-card hand (one option if both cards are the same rank)."
    },
    {
      "question": "Guard guess",
      "who": "the active seat, only when discard_choice = 1",
      "options": "any whole number from 2 to 8"
    }
  ],
  "choices": [
    {
      "what": "Exactly 2 players",
      "why": "The designer fixed the duel at 2. All card effects target 'the opponent', and the game is two-person deduction and bluffing about one hidden card."
    },
    {
      "what": "No talk step",
      "why": "The source has no table talk. Adding it would be a new mechanic."
    },
    {
      "what": "Out-of-play split into burned_card (hidden) and face_up (public)",
      "why": "Position 1 is face down while positions 2-6 are face up, so they need different visibility."
    },
    {
      "what": "Ranking expression tokens*1000 + career_sum",
      "why": "career_sum can never reach 1000 in 40 rounds (at most about 16 per round), so tokens come first and career_sum breaks ties. Equal values share the win, which is the draw."
    },
    {
      "what": "When the hand holds 7 with 5 or 6, only 7 is offered",
      "why": "A seat is never offered what it may not do. The Countess step still enforces it."
    },
    {
      "what": "Scratch flags new_hand, token_awarded and round_number added",
      "why": "Needed to condition the face-up announcement, the pass step and the round-40 showdown with arithmetic."
    }
  ],
  "simplifications": [
    {
      "what": "Deck draws are random picks from the deck list instead of taking the top card of one shuffle per hand",
      "why": "The engine draws at random. The deck order is hidden and unseen, so each draw has the same distribution as a single shuffle."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: discards, career_sum, tokens; table: face_up, deck_count, round_number.
````

## Reply

````
```json
[
  {"name": "Before any deal the deck holds all 16 cards and hands are empty", "rule": "R1", "players": 2, "rounds": 0,
   "expect": {"lens": {"game": {"deck": 16}, "players": {"1": {"hand": 0}, "2": {"hand": 0}}}}},

  {"name": "First round deals 1 burned, 5 face up and resets old discards (random deal: only counts asserted)", "rule": "R2", "players": 2, "rounds": 1, "default": "first",
   "given": {"players": {"1": {"discards": [5, 5, 5], "discard_sum": 15}}, "game": {"hand_over": 1}},
   "expect": {"game": {"round_number": 1},
              "lens": {"game": {"face_up": 5, "burned_card": 1}, "players": {"1": {"discards": 1}}}}},

  {"name": "New hand shows 5 face-up ranks while the burned card stays apart (random deal: only counts asserted)", "rule": "R3", "players": 2, "rounds": 1, "default": "first",
   "expect": {"lens": {"game": {"face_up": 5, "burned_card": 1}}}},

  {"name": "Turn start draws one card and deck_count drops by 1", "rule": "R4", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": [2]}, "2": {"hand": [3]}},
             "game": {"hand_over": 0, "active_seat": 1, "deck": [4, 4, 4], "deck_count": 3}},
   "rules": [{"seat": 1, "options_include": 4}],
   "expect": {"game": {"deck_count": 2}, "lens": {"game": {"deck": 2}, "players": {"1": {"hand": 1}}},
              "players": {"1": {"discards": [4], "career_sum": 4}}}},

  {"name": "The chosen rank is the one discarded", "rule": "R5", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": [2]}, "2": {"hand": [3]}},
             "game": {"hand_over": 0, "active_seat": 1, "deck": [4, 4, 4], "deck_count": 3}},
   "rules": [{"seat": 1, "options_include": 2}],
   "expect": {"players": {"1": {"discards": [2], "career_sum": 2}, "2": {"discards": [], "tokens": 0}},
              "offered": [{"seat": 1, "option": 2}, {"seat": 1, "option": 4}]}},

  {"name": "Countess with Prince must be discarded", "rule": "R6", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": [7]}, "2": {"hand": [3]}},
             "game": {"hand_over": 0, "active_seat": 1, "deck": [5, 5, 5], "deck_count": 3}},
   "rules": [{"seat": 1, "options_include": 5}],
   "expect": {"players": {"1": {"discards": [7], "career_sum": 7}, "2": {"discards": []}},
              "not_offered": [{"seat": 1, "option": 5}]}},

  {"name": "Discard appends to discards and adds to career_sum", "rule": "R7", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": [4], "discards": [4], "discard_sum": 4, "career_sum": 10}, "2": {"hand": [3]}},
             "game": {"hand_over": 0, "active_seat": 1, "deck": [4, 4], "deck_count": 2}},
   "rules": [{"seat": 1, "options_include": 4}],
   "expect": {"players": {"1": {"discards": [4, 4], "career_sum": 14}}, "game": {"deck_count": 1}}},

  {"name": "Guard asks for a guess from 2 to 8", "rule": "R8", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": [1]}, "2": {"hand": [3]}},
             "game": {"hand_over": 0, "active_seat": 1, "deck": [4, 4, 4], "deck_count": 3}},
   "rules": [{"seat": 1, "options_include": 1}, {"seat": 1, "options_include": 2}],
   "expect": {"players": {"1": {"discards": [1], "career_sum": 1, "tokens": 0}, "2": {"tokens": 0}},
              "offered": [{"seat": 1, "option": 2}, {"seat": 1, "option": 8}]}},

  {"name": "Guard against a protected opponent does nothing even with the right guess", "rule": "R9", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": [1]}, "2": {"hand": [3], "protected": 1}},
             "game": {"hand_over": 0, "active_seat": 1, "deck": [4, 4, 4], "deck_count": 3}},
   "rules": [{"seat": 1, "options_include": 1}, {"seat": 1, "options_include": 3}],
   "expect": {"players": {"1": {"tokens": 0, "discards": [1]}, "2": {"tokens": 0}}}},

  {"name": "Guard correct guess eliminates the opponent and gives a token", "rule": "R10", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": [1]}, "2": {"hand": [3]}},
             "game": {"hand_over": 0, "active_seat": 1, "deck": [4, 4, 4], "deck_count": 3}},
   "rules": [{"seat": 1, "options_include": 1}, {"seat": 1, "options_include": 3}],
   "expect": {"players": {"1": {"tokens": 1}, "2": {"tokens": 0}}}},

  {"name": "Guard wrong guess is a miss", "rule": "R10", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": [1]}, "2": {"hand": [3]}},
             "game": {"hand_over": 0, "active_seat": 1, "deck": [4, 4, 4], "deck_count": 3}},
   "rules": [{"seat": 1, "options_include": 1}, {"seat": 1, "options_include": 5}],
   "expect": {"players": {"1": {"tokens": 0}, "2": {"tokens": 0}}}},

  {"name": "Priest only looks: nobody is out and the opponent keeps its card", "rule": "R11", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": [2]}, "2": {"hand": [3]}},
             "game": {"hand_over": 0, "active_seat": 1, "deck": [4, 4, 4], "deck_count": 3}},
   "rules": [{"seat": 1, "options_include": 2}],
   "expect": {"players": {"1": {"tokens": 0, "discards": [2]}, "2": {"tokens": 0, "discards": []}},
              "lens": {"players": {"2": {"hand": 1}}}}},

  {"name": "Baron: opponent's lower card is out", "rule": "R12", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": [3]}, "2": {"hand": [2]}},
             "game": {"hand_over": 0, "active_seat": 1, "deck": [5, 5, 5], "deck_count": 3}},
   "rules": [{"seat": 1, "options_include": 3}],
   "expect": {"players": {"1": {"tokens": 1, "discards": [3]}, "2": {"tokens": 0}}}},

  {"name": "Baron: active player's lower card is out", "rule": "R12", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": [3]}, "2": {"hand": [7]}},
             "game": {"hand_over": 0, "active_seat": 1, "deck": [5, 5, 5], "deck_count": 3}},
   "rules": [{"seat": 1, "options_include": 3}],
   "expect": {"players": {"1": {"tokens": 0}, "2": {"tokens": 1}}}},

  {"name": "Baron: equal cards tie, nobody out", "rule": "R12", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": [3]}, "2": {"hand": [5]}},
             "game": {"hand_over": 0, "active_seat": 1, "deck": [5, 5, 5], "deck_count": 3}},
   "rules": [{"seat": 1, "options_include": 3}],
   "expect": {"players": {"1": {"tokens": 0}, "2": {"tokens": 0}}}},

  {"name": "Handmaid protects against the opponent's next Guard", "rule": "R13", "players": 2, "rounds": 2,
   "given": {"players": {"1": {"hand": [4]}, "2": {"hand": [1]}},
             "game": {"hand_over": 0, "active_seat": 1, "deck": [6, 6, 6], "deck_count": 3}},
   "rules": [{"seat": 1, "options_include": 4}, {"seat": 2, "options_include": 1}, {"seat": 2, "options_include": 6}],
   "expect": {"players": {"1": {"tokens": 0, "discards": [4]}, "2": {"tokens": 0, "discards": [1]}},
              "game": {"deck_count": 1}}},

  {"name": "Prince targets the unprotected opponent, who discards and redraws", "rule": "R14", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": [5]}, "2": {"hand": [3]}},
             "game": {"hand_over": 0, "active_seat": 1, "deck": [4, 4, 4], "deck_count": 3}},
   "rules": [{"seat": 1, "options_include": 5}],
   "expect": {"players": {"1": {"discards": [5], "career_sum": 5}, "2": {"discards": [3], "career_sum": 3}},
              "game": {"deck_count": 1}, "lens": {"players": {"2": {"hand": 1}}}}},

  {"name": "Prince targets the active player when the opponent is protected", "rule": "R14", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": [5]}, "2": {"hand": [3], "protected": 1}},
             "game": {"hand_over": 0, "active_seat": 1, "deck": [4, 4, 4], "deck_count": 3}},
   "rules": [{"seat": 1, "options_include": 5}],
   "expect": {"players": {"1": {"discards": [5, 4], "career_sum": 9}, "2": {"discards": [], "career_sum": 0}},
              "game": {"deck_count": 1}}},

  {"name": "Prince forcing out the Princess eliminates the target", "rule": "R15", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": [5]}, "2": {"hand": [8]}},
             "game": {"hand_over": 0, "active_seat": 1, "deck": [4, 4, 4], "deck_count": 3}},
   "rules": [{"seat": 1, "options_include": 5}],
   "expect": {"players": {"1": {"tokens": 1}, "2": {"discards": [8], "career_sum": 8, "tokens": 0}},
              "game": {"deck_count": 2}}},

  {"name": "Prince with an empty deck gives the target the burned card", "rule": "R16", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": [5]}, "2": {"hand": [3]}},
             "game": {"hand_over": 0, "active_seat": 1, "deck": [4], "deck_count": 1, "burned_card": [2]}},
   "rules": [{"seat": 1, "options_include": 5}],
   "expect": {"players": {"1": {"tokens": 1}, "2": {"discards": [3], "career_sum": 3, "tokens": 0}},
              "game": {"deck_count": 0}, "lens": {"game": {"burned_card": 0}}}},

  {"name": "King swaps hands (seen through the showdown that follows)", "rule": "R17", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": [6]}, "2": {"hand": [7]}},
             "game": {"hand_over": 0, "active_seat": 1, "deck": [2], "deck_count": 1}},
   "rules": [{"seat": 1, "options_include": 6}],
   "expect": {"players": {"1": {"tokens": 1, "discards": [6]}, "2": {"tokens": 0}}}},

  {"name": "King against a protected opponent does not swap", "rule": "R17", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": [6]}, "2": {"hand": [7], "protected": 1}},
             "game": {"hand_over": 0, "active_seat": 1, "deck": [2], "deck_count": 1}},
   "rules": [{"seat": 1, "options_include": 6}],
   "expect": {"players": {"1": {"tokens": 0}, "2": {"tokens": 1}}}},

  {"name": "Discarding the Princess knocks yourself out", "rule": "R18", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": [8]}, "2": {"hand": [3]}},
             "game": {"hand_over": 0, "active_seat": 1, "deck": [4, 4, 4], "deck_count": 3}},
   "rules": [{"seat": 1, "options_include": 8}],
   "expect": {"players": {"1": {"discards": [8], "career_sum": 8, "tokens": 0}, "2": {"tokens": 1}}}},

  {"name": "Empty deck triggers showdown, lower card loses", "rule": "R19", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": [4]}, "2": {"hand": [6]}},
             "game": {"hand_over": 0, "active_seat": 1, "deck": [4], "deck_count": 1}},
   "rules": [{"seat": 1, "options_include": 4}],
   "expect": {"players": {"1": {"tokens": 0}, "2": {"tokens": 1}}, "game": {"deck_count": 0}}},

  {"name": "Equal showdown cards: lower discard_sum loses", "rule": "R20", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": [4]}, "2": {"hand": [4], "discard_sum": 2}},
             "game": {"hand_over": 0, "active_seat": 1, "deck": [4], "deck_count": 1}},
   "rules": [{"seat": 1, "options_include": 4}],
   "expect": {"players": {"1": {"tokens": 1}, "2": {"tokens": 0}}}},

  {"name": "Equal showdown cards and discard_sum: tied hand, no token", "rule": "R20", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": [4]}, "2": {"hand": [4], "discard_sum": 4}},
             "game": {"hand_over": 0, "active_seat": 1, "deck": [4], "deck_count": 1}},
   "rules": [{"seat": 1, "options_include": 4}],
   "expect": {"players": {"1": {"tokens": 0}, "2": {"tokens": 0}}}},

  {"name": "Elimination gives the other player exactly one token", "rule": "R21", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": [1], "tokens": 2}, "2": {"hand": [6], "tokens": 1}},
             "game": {"hand_over": 0, "active_seat": 1, "deck": [4, 4, 4], "deck_count": 3}},
   "rules": [{"seat": 1, "options_include": 1}, {"seat": 1, "options_include": 6}],
   "expect": {"players": {"1": {"tokens": 3}, "2": {"tokens": 1}}}},

  {"name": "Eliminated seat starts the next hand (random new deal: only counts asserted)", "rule": "R21", "players": 2, "rounds": 2, "default": "first",
   "given": {"players": {"1": {"hand": [1]}, "2": {"hand": [6]}},
             "game": {"hand_over": 0, "active_seat": 1, "deck": [4, 4, 4], "deck_count": 3}},
   "rules": [{"seat": 1, "options_include": 1, "times": 1}, {"seat": 1, "options_include": 6, "times": 1}],
   "expect": {"game": {"round_number": 2}, "lens": {"players": {"2": {"discards": 1}}}}},

  {"name": "Without a token the turn passes to the other seat", "rule": "R22", "players": 2, "rounds": 2,
   "given": {"players": {"1": {"hand": [4]}, "2": {"hand": [2]}},
             "game": {"hand_over": 0, "active_seat": 1, "deck": [4, 4, 4, 4], "deck_count": 4}},
   "rules": [{"seat": 1, "options_include": 4}, {"seat": 2, "options_include": 4}],
   "expect": {"players": {"1": {"discards": [4]}, "2": {"discards": [4]}}, "game": {"deck_count": 2}}},

  {"name": "Round 40 showdown decides the last token and the game ends", "rule": "R23", "players": 2,
   "given": {"players": {"1": {"hand": [2], "tokens": 3, "career_sum": 50}, "2": {"hand": [3], "tokens": 3, "career_sum": 60}},
             "game": {"hand_over": 0, "active_seat": 1, "round_number": 39, "deck": [4, 4, 4, 4, 4], "deck_count": 5}},
   "rules": [{"seat": 1, "options_include": 4}],
   "expect": {"winner": 2, "standings": {"1": 3054, "2": 4060},
              "players": {"1": {"tokens": 3, "career_sum": 54}, "2": {"tokens": 4}}, "game": {"round_number": 40}}},

  {"name": "Equal tokens at the end: higher career_sum wins", "rule": "R23", "players": 2,
   "given": {"players": {"1": {"hand": [4], "tokens": 2, "career_sum": 30}, "2": {"hand": [4], "tokens": 2, "career_sum": 40, "discard_sum": 4}},
             "game": {"hand_over": 0, "active_seat": 1, "round_number": 39, "deck": [4, 4, 4, 4, 4], "deck_count": 5}},
   "rules": [{"seat": 1, "options_include": 4}],
   "expect": {"winner": 2, "standings": {"1": 2034, "2": 2040},
              "players": {"1": {"tokens": 2, "career_sum": 34}, "2": {"tokens": 2, "career_sum": 40}}}},

  {"name": "Equal tokens and career_sum at the end: shared result", "rule": "R23", "players": 2,
   "given": {"players": {"1": {"hand": [4], "tokens": 2, "career_sum": 36}, "2": {"hand": [4], "tokens": 2, "career_sum": 40, "discard_sum": 4}},
             "game": {"hand_over": 0, "active_seat": 1, "round_number": 39, "deck": [4, 4, 4, 4, 4], "deck_count": 5}},
   "rules": [{"seat": 1, "options_include": 4}],
   "expect": {"winner": [1, 2], "standings": {"1": 2040, "2": 2040}}}
]
```
````
