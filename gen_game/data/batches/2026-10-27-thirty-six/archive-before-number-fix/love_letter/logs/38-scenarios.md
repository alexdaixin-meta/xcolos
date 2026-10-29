# 38 scenarios

- time: 2026-10-27T19:19:55+00:00 (134.7s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 fe0d36b981d72e2f, reply sha256 f26ee5feb3e998a7

## Sent

````
SPEC:
{
  "name": "Love Letter: Short Hands",
  "summary": "Two-player Love Letter over exactly 40 turns: draw, discard a card to use its effect, knock out the rival or win the showdown, and optionally raise a hand's stake to 2.",
  "players": {
    "min": 2,
    "max": 2,
    "suggested": 2
  },
  "parameters": {
    "deck_size": 16,
    "guard_count": 5,
    "guard_rank": 1,
    "priest_count": 2,
    "priest_rank": 2,
    "baron_count": 2,
    "baron_rank": 3,
    "handmaid_count": 2,
    "handmaid_rank": 4,
    "prince_count": 2,
    "prince_rank": 5,
    "king_count": 1,
    "king_rank": 6,
    "countess_count": 1,
    "countess_rank": 7,
    "princess_count": 1,
    "princess_rank": 8,
    "total_rounds": 40,
    "cards_out_of_play": 5,
    "cards_dealt_each": 1,
    "deck_after_deal": 9,
    "base_stake": 1,
    "raised_stake": 2,
    "fold_points": 1,
    "guard_guess_min": 2,
    "guard_guess_max": 8,
    "showdown_deck_threshold": 1,
    "raise_min_deck": 2,
    "starting_points": 0,
    "starting_starter_seat": 1
  },
  "attributes": {
    "player": [
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "Ranks of the cards held: 1 card between turns, 2 during own turn.",
        "observable": false
      },
      {
        "key": "discards",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Ranks this player discarded this hand, in order.",
        "observable": true
      },
      {
        "key": "points",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Score.",
        "observable": true
      },
      {
        "key": "protected",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "1 if protected by a Handmaid until this player's next turn starts.",
        "observable": true
      },
      {
        "key": "eliminated",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "1 if knocked out of the current hand.",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "full_deck",
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
        "meaning": "The 16 card ranks, copied into the deck each new hand.",
        "observable": false
      },
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "Drawable cards in shuffled order, top first, not counting the reserve.",
        "observable": false
      },
      {
        "key": "reserve",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "The bottom card of the deck. It is never drawn at the start of a turn. A Prince redraw takes it only when the deck list is empty.",
        "observable": false
      },
      {
        "key": "deck_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Cards left in the deck: length of deck plus length of reserve.",
        "observable": true
      },
      {
        "key": "out_of_play",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "The 5 cards set aside face up at the start of each hand.",
        "observable": true
      },
      {
        "key": "stake",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Points the current hand is worth.",
        "observable": true
      },
      {
        "key": "active_seat",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Seat taking this turn.",
        "observable": false
      },
      {
        "key": "starter_seat",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Seat that starts the next or current hand.",
        "observable": false
      },
      {
        "key": "round_number",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Current round (turn), 1 to 40.",
        "observable": true
      },
      {
        "key": "new_hand",
        "type": "number",
        "visible": "none",
        "initial": 1,
        "meaning": "1 if a new hand must be dealt at the start of this round.",
        "observable": false
      },
      {
        "key": "folded",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "1 if the opponent folded to a raise this turn.",
        "observable": false
      },
      {
        "key": "current_discard",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "Rank discarded this turn.",
        "observable": false
      },
      {
        "key": "guard_guess",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "Rank named with a Guard this turn (0 if none).",
        "observable": false
      },
      {
        "key": "raised",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "Scratch: 1 if the active player raised this turn.",
        "observable": false
      },
      {
        "key": "prince_target",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "Scratch: seat targeted by a Prince this turn (0 if none).",
        "observable": false
      }
    ]
  },
  "setup": [
    "Every player starts with points 0, empty hand and discards, protected 0 and eliminated 0.",
    "Set starter_seat = 1, active_seat = 1, round_number = 1, new_hand = 1 and stake = 1.",
    "No cards are dealt in setup. The first hand is dealt by the NEW HAND step of round 1."
  ],
  "round": [
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "When new_hand = 1: empty both players' hand and discards. Clear out_of_play. Copy full_deck into deck and shuffle it. Move the top 5 cards of deck into out_of_play (public). Deal 1 card from the top of deck to each player's hand. Move the bottom card of deck into reserve, leaving deck with 8 cards and reserve with 1. Set deck_count = 9, protected = 0 and eliminated = 0 for both players, stake = 1, folded = 0, active_seat = starter_seat and new_hand = 0. Announce out_of_play to everyone."
    },
    {
      "action": "update",
      "who": "active seat",
      "answer": null,
      "effect": "Reset guard_guess = 0, raised = 0, prince_target = 0. Set the active player's protected = 0. Move the top card of deck into the active player's hand (never the reserve). Set deck_count = len(deck) + len(reserve)."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player sees their own hand and all public attributes."
    },
    {
      "action": "ask",
      "who": "active seat",
      "answer": "one rank from the active player's hand (see offers)",
      "effect": "The chosen rank is held for the next step. Prompt: 'Choose one of your two cards to discard.'"
    },
    {
      "action": "update",
      "who": "active seat",
      "answer": null,
      "effect": "If the active hand contains 7 together with 5 or 6, the discarded card is 7 whatever was chosen. Remove that card from the active hand, append it to the active player's discards and set current_discard to it. Announce 'Seat {active_seat} discards {card name}'."
    },
    {
      "action": "ask",
      "who": "active seat",
      "answer": "a whole number from 2 to 8",
      "effect": "When current_discard = 1 and the opponent's protected = 0: set guard_guess to the named rank and announce the named rank to both players."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "When guard_guess >= 2: if the opponent's hand card equals guard_guess, set the opponent's eliminated = 1 and announce 'Hit: {card name}'. Otherwise announce 'Miss'."
    },
    {
      "action": "tell",
      "who": "active seat only",
      "answer": null,
      "effect": "When current_discard = 2 and the opponent's protected = 0: privately tell the active player the opponent's hand card."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "When current_discard = 3 and the opponent's protected = 0: compare the active hand card with the opponent's hand card. The holder of the lower rank gets eliminated = 1 and their card is announced. On equal ranks nothing happens and nothing is revealed."
    },
    {
      "action": "update",
      "who": "active seat",
      "answer": null,
      "effect": "When current_discard = 4: set the active player's protected = 1."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "When current_discard = 5: prince_target = the opponent if the opponent's protected = 0, otherwise the active seat. Move the target's hand card to the target's discards and announce it. If that card is 8, set the target's eliminated = 1."
    },
    {
      "action": "update",
      "who": "prince target",
      "answer": null,
      "effect": "When prince_target > 0 and the target's eliminated = 0: move the top card of deck into the target's hand, or the reserve card if deck is empty. Set deck_count = len(deck) + len(reserve)."
    },
    {
      "action": "update",
      "who": "both players",
      "answer": null,
      "effect": "When current_discard = 6 and the opponent's protected = 0: swap the active player's hand with the opponent's hand."
    },
    {
      "action": "update",
      "who": "active seat",
      "answer": null,
      "effect": "When current_discard = 8: set the active player's eliminated = 1."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player sees their own (possibly swapped or redrawn) hand and all public attributes."
    },
    {
      "action": "ask",
      "who": "active seat",
      "answer": "raise | pass",
      "effect": "When stake = 1, both players' eliminated = 0, deck_count >= 2 and the opponent's discards has at least 1 card: prompt 'Raise this hand's stake to 2, or pass?' On raise, set raised = 1 and announce the raise."
    },
    {
      "action": "ask",
      "who": "opponent of the active seat",
      "answer": "accept | fold",
      "effect": "When raised = 1: prompt 'Accept (the stake becomes 2) or fold?' On accept, set stake = 2. On fold, set folded = 1. Announce the answer."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "HAND END, first that holds: (a) if folded = 1, the active player's points += 1; (b) else if a player has eliminated = 1, the other player's points += stake; (c) else if deck_count <= 1 or round_number = 40, reveal both hand cards and the higher rank's points += stake, with no score on equal ranks. If (a), (b) or (c) applied, set new_hand = 1 and starter_seat = 3 - starter_seat, and announce the result."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "If new_hand = 1, set active_seat = starter_seat. Otherwise set active_seat = 3 - active_seat. Then round_number += 1."
    },
    {
      "action": "check",
      "who": "table",
      "answer": null,
      "effect": "End the game if round_number > 40, otherwise continue."
    }
  ],
  "ending": {
    "condition": "round_number > 40",
    "rank_by": "you.points",
    "decided_by": "After exactly 40 rounds, the player with more points wins. Equal points share the win, which is the draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When a new hand starts, the 16-card deck (5 Guard, 2 Priest, 2 Baron, 2 Handmaid, 2 Prince, 1 King, 1 Countess, 1 Princess) is shuffled, 5 cards go face up to out_of_play, each player gets 1 card, and deck_count = 9."
    },
    {
      "id": "R2",
      "text": "When a new hand starts, both players' discards are emptied, protected = 0, eliminated = 0, stake = 1, and the active seat becomes the starter seat."
    },
    {
      "id": "R3",
      "text": "When a turn starts, the active player's protected becomes 0 and they draw the top card, holding 2 cards, and deck_count falls by 1."
    },
    {
      "id": "R4",
      "text": "The bottom (reserve) card is never drawn at the start of a turn."
    },
    {
      "id": "R5",
      "text": "When the active player chooses a discard, that card moves from their hand to their discards and is announced as 'Seat X discards CARD'."
    },
    {
      "id": "R6",
      "text": "When the active player holds the Countess (7) with a King (6) or Prince (5), the Countess is discarded whatever was chosen."
    },
    {
      "id": "R7",
      "text": "When a Guard (1) is discarded and the opponent is not protected, the active player names a rank from 2 to 8, which is announced."
    },
    {
      "id": "R8",
      "text": "When the named Guard rank equals the opponent's card, the opponent is eliminated and 'Hit: CARD' is announced; otherwise 'Miss' is announced."
    },
    {
      "id": "R9",
      "text": "When a Priest (2) is discarded and the opponent is not protected, only the active player is told the opponent's card."
    },
    {
      "id": "R10",
      "text": "When a Baron (3) is discarded and the opponent is not protected, the lower hand card's holder is eliminated and their card announced; on equal ranks nothing happens and nothing is revealed."
    },
    {
      "id": "R11",
      "text": "When a Handmaid (4) is discarded, the active player's protected becomes 1 until their next turn starts."
    },
    {
      "id": "R12",
      "text": "When a Prince (5) is discarded, the opponent (or the active player if the opponent is protected) discards their hand card face up with no effect, and it is announced."
    },
    {
      "id": "R13",
      "text": "When a Prince makes a player discard the Princess (8), that player is eliminated."
    },
    {
      "id": "R14",
      "text": "When a Prince target is not eliminated, they draw the top card, taking the reserve only if it is the last card."
    },
    {
      "id": "R15",
      "text": "When a King (6) is discarded and the opponent is not protected, the two players swap hand cards."
    },
    {
      "id": "R16",
      "text": "When the Princess (8) is discarded, the active player is eliminated."
    },
    {
      "id": "R17",
      "text": "Cards targeting the opponent (Guard, Priest, Baron, King) have no effect when the opponent's protected = 1."
    },
    {
      "id": "R18",
      "text": "When stake = 1, nobody is eliminated, deck_count >= 2 and the opponent has at least 1 discard, the active player may raise or pass."
    },
    {
      "id": "R19",
      "text": "When the active player raises, the opponent accepts (stake = 2) or folds (folded = 1)."
    },
    {
      "id": "R20",
      "text": "When the opponent folds, the active player gains 1 point and the hand ends."
    },
    {
      "id": "R21",
      "text": "When a player is eliminated and nobody folded, the other player gains points equal to the stake and the hand ends."
    },
    {
      "id": "R22",
      "text": "When nobody folded or was eliminated and deck_count <= 1 or it is round 40, both cards are revealed and the higher rank gains the stake; equal ranks score nothing."
    },
    {
      "id": "R23",
      "text": "When a hand ends, the starter seat switches and the new starter takes the next turn; otherwise the turn passes to the opponent."
    },
    {
      "id": "R24",
      "text": "After round 40 the game ends and the player with more points wins; equal points is a draw."
    }
  ],
  "offers": [
    {
      "question": "Choose one of your two cards to discard",
      "who": "active seat",
      "options": "Holding 7 together with 5 or 6: only 7. Otherwise: either of the two ranks in hand (one option if both are equal)."
    },
    {
      "question": "Guard guess",
      "who": "active seat, only when a Guard was discarded and the opponent is not protected",
      "options": "a whole number 2 to 8"
    },
    {
      "question": "Raise this hand's stake to 2, or pass?",
      "who": "active seat, only when stake = 1, nobody is eliminated, deck_count >= 2 and the opponent has at least 1 discard",
      "options": "raise, pass"
    },
    {
      "question": "Accept (the stake becomes 2) or fold?",
      "who": "the opponent, only right after a raise",
      "options": "accept, fold"
    }
  ],
  "choices": [
    {
      "what": "2 players (min 2, max 2)",
      "why": "The designer fixed the table at 2. Every effect (Guard, Baron, King, the raise and fold) targets 'the opponent', so more seats would break the rules."
    },
    {
      "what": "No free talk step",
      "why": "The source has none. The raise and fold already carry the bluffing signal."
    },
    {
      "what": "Countess forcing is shown in the offer as well as enforced in the resolve step",
      "why": "A seat is never offered what it may not do. The outcome is the same as the source's override."
    },
    {
      "what": "Strategy at the table",
      "why": "Players track the out_of_play cards and both discard piles to make good Guard guesses, time Baron and King plays, and raise as a bluff or with a strong card."
    }
  ],
  "simplifications": [
    {
      "what": "Cards are stored as their ranks (1 to 8) and named in announcements",
      "why": "The Guard check, Baron comparison and showdown are then plain arithmetic."
    },
    {
      "what": "The reserve is kept in its own hidden list instead of at the bottom of the deck",
      "why": "The engine draws from a list, so separating it guarantees the turn-start draw never takes it. deck_count adds both lists."
    },
    {
      "what": "The Guard guess and Guard check are tracked with guard_guess > 0 instead of 'step 5 ran'; the Prince redraw uses prince_target",
      "why": "A step's 'when' must be an arithmetic condition on state."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: discards, points, protected, eliminated; table: deck_count, out_of_play, stake, round_number.

EARLIER TESTS FOR THIS SPEC WERE FOUND WRONG. What to do differently:
Only require an option when the rules force it to be offered given the stated hand and deck top. In the turn-start test, either make the top card a 3 or drop the `options_include` 3 rule. In the Countess test, assert that 5 is NOT offered, or that the discard is 7 whatever the choice, instead of requiring 5. For the R2 and R3 tests, work out the exact hand after the draw from the given deck top, and assert only options that hand can produce (for example a Guard guess of 2 only after a Guard is discarded and the opponent is unprotected). Keep given state consistent: `deck_count` must equal len(deck)+len(reserve), and the reserve must not also be listed inside the deck. Assert on public results (discards, deck_count, eliminated, points, stake) rather than on internal lists like `reserve` or `offer`. For shuffled setups, assert only counts.
````

## Reply

````
```json
[
  {"name": "New hand from setup: 5 cards out of play, seat 1 holds 1 card after its turn (shuffled, counts only)", "rule": "R1", "players": 2, "seed": 1, "rounds": 1, "default": "decline",
   "rules": [],
   "expect": {"lens": {"game": {"out_of_play": 5}, "players": {"1": {"hand": 1, "discards": 1}}},
              "game": {"round_number": 2}}},

  {"name": "New hand with an all-Handmaid deck: 5 out of play, deck_count 9 minus seat 1's draw = 8", "rule": "R1", "players": 2, "seed": 1, "rounds": 1, "default": "decline",
   "given": {"game": {"full_deck": [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4]}},
   "rules": [{"seat": 1, "options_include": 4, "times": "all"}],
   "expect": {"lens": {"game": {"out_of_play": 5}, "players": {"1": {"hand": 1}, "2": {"hand": 1}}},
              "game": {"deck_count": 8, "out_of_play": [4,4,4,4,4], "stake": 1},
              "players": {"1": {"discards": [4], "protected": 1}, "2": {"discards": []}}}},

  {"name": "New hand resets discards, protection, elimination and stake; the starter seat 2 acts", "rule": "R2", "players": 2, "seed": 1, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"discards": [1, 3], "protected": 1, "eliminated": 1, "points": 2, "hand": [5]},
                         "2": {"discards": [2], "protected": 1, "eliminated": 0, "points": 1, "hand": [6]}},
             "game": {"full_deck": [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4], "new_hand": 1, "starter_seat": 2, "active_seat": 1, "stake": 2, "round_number": 5}},
   "rules": [{"seat": 2, "options_include": 4, "times": "all"}],
   "expect": {"players": {"1": {"discards": [], "protected": 0, "eliminated": 0, "points": 2},
                          "2": {"discards": [4], "protected": 1, "eliminated": 0, "points": 1}},
              "game": {"stake": 1, "deck_count": 8, "round_number": 6},
              "not_offered": [{"seat": 1, "option": 4}]}},

  {"name": "Turn start clears own protection, draws the top card (4) and deck_count falls by 1", "rule": "R3", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [2], "protected": 1, "discards": [4]}, "2": {"hand": [1], "discards": []}},
             "game": {"new_hand": 0, "active_seat": 1, "starter_seat": 1, "round_number": 5, "stake": 1,
                      "deck": [4, 1, 1], "reserve": [3], "deck_count": 4}},
   "rules": [{"seat": 1, "options_include": 2}],
   "expect": {"players": {"1": {"protected": 0, "discards": [4, 2]}, "2": {"eliminated": 0}},
              "game": {"deck_count": 3, "round_number": 6},
              "lens": {"players": {"1": {"hand": 1}}},
              "offered": [{"seat": 1, "option": 4}, {"seat": 1, "option": 2}]}},

  {"name": "The reserve card (8) is not drawn at turn start; the deck top (2) is", "rule": "R4", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [3]}, "2": {"hand": [1]}},
             "game": {"new_hand": 0, "active_seat": 1, "starter_seat": 1, "round_number": 5, "stake": 1,
                      "deck": [2], "reserve": [8], "deck_count": 2}},
   "rules": [{"seat": 1, "options_include": 2}],
   "expect": {"players": {"1": {"discards": [2]}},
              "game": {"deck_count": 1},
              "offered": [{"seat": 1, "option": 2}, {"seat": 1, "option": 3}],
              "not_offered": [{"seat": 1, "option": 8}]}},

  {"name": "The chosen discard moves from hand to discards", "rule": "R5", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [4]}, "2": {"hand": [1]}},
             "game": {"new_hand": 0, "active_seat": 1, "starter_seat": 1, "round_number": 5, "stake": 1,
                      "deck": [2, 1, 1], "reserve": [1], "deck_count": 4}},
   "rules": [{"seat": 1, "options_include": 2}],
   "expect": {"players": {"1": {"discards": [2], "protected": 0}, "2": {"discards": []}},
              "lens": {"players": {"1": {"hand": 1}}},
              "game": {"deck_count": 3}}},

  {"name": "Countess with Prince: the Countess is discarded and the Prince is not offered", "rule": "R6", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [7]}, "2": {"hand": [1]}},
             "game": {"new_hand": 0, "active_seat": 1, "starter_seat": 1, "round_number": 5, "stake": 1,
                      "deck": [5, 1, 1], "reserve": [1], "deck_count": 4}},
   "rules": [{"seat": 1, "options_include": 5}],
   "expect": {"players": {"1": {"discards": [7]}, "2": {"discards": []}},
              "game": {"deck_count": 3},
              "not_offered": [{"seat": 1, "option": 5}]}},

  {"name": "Countess with King: the Countess is discarded and the King is not offered", "rule": "R6", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [6]}, "2": {"hand": [1]}},
             "game": {"new_hand": 0, "active_seat": 1, "starter_seat": 1, "round_number": 5, "stake": 1,
                      "deck": [7, 1, 1], "reserve": [1], "deck_count": 4}},
   "rules": [{"seat": 1, "options_include": 6}],
   "expect": {"players": {"1": {"discards": [7]}},
              "not_offered": [{"seat": 1, "option": 6}]}},

  {"name": "A Guard against an unprotected opponent asks for a guess from 2 to 8 (a wrong guess of 3 misses)", "rule": "R7", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [1]}, "2": {"hand": [5]}},
             "game": {"new_hand": 0, "active_seat": 1, "starter_seat": 1, "round_number": 5, "stake": 1,
                      "deck": [4, 2, 3], "reserve": [2], "deck_count": 4}},
   "rules": [{"seat": 1, "options_include": 1}, {"seat": 1, "options_include": 3}],
   "expect": {"players": {"1": {"discards": [1], "points": 0}, "2": {"eliminated": 0, "points": 0}},
              "offered": [{"seat": 1, "option": 8}, {"seat": 1, "option": 2}]}},

  {"name": "A Guard guess equal to the opponent's card (5) eliminates them", "rule": "R8", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [1]}, "2": {"hand": [5]}},
             "game": {"new_hand": 0, "active_seat": 1, "starter_seat": 1, "round_number": 5, "stake": 1,
                      "deck": [4, 2, 3], "reserve": [2], "deck_count": 4}},
   "rules": [{"seat": 1, "options_include": 1}, {"seat": 1, "options_include": 5}],
   "expect": {"players": {"1": {"discards": [1], "points": 1}, "2": {"eliminated": 1, "points": 0}}}},

  {"name": "A wrong Guard guess (6 against a 5) misses", "rule": "R8", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [1]}, "2": {"hand": [5]}},
             "game": {"new_hand": 0, "active_seat": 1, "starter_seat": 1, "round_number": 5, "stake": 1,
                      "deck": [4, 2, 3], "reserve": [2], "deck_count": 4}},
   "rules": [{"seat": 1, "options_include": 1}, {"seat": 1, "options_include": 6}],
   "expect": {"players": {"1": {"points": 0}, "2": {"eliminated": 0, "points": 0}}}},

  {"name": "A Priest only reveals privately: nobody is eliminated and nothing else changes", "rule": "R9", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [4]}, "2": {"hand": [8]}},
             "game": {"new_hand": 0, "active_seat": 1, "starter_seat": 1, "round_number": 5, "stake": 1,
                      "deck": [2, 1, 1], "reserve": [1], "deck_count": 4}},
   "rules": [{"seat": 1, "options_include": 2}],
   "expect": {"players": {"1": {"discards": [2], "eliminated": 0}, "2": {"discards": [], "eliminated": 0}},
              "game": {"deck_count": 3}}},

  {"name": "Baron: the opponent's lower card (2 against 6) is eliminated", "rule": "R10", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [3]}, "2": {"hand": [2]}},
             "game": {"new_hand": 0, "active_seat": 1, "starter_seat": 1, "round_number": 5, "stake": 1,
                      "deck": [6, 1, 1], "reserve": [1], "deck_count": 4}},
   "rules": [{"seat": 1, "options_include": 3}],
   "expect": {"players": {"1": {"discards": [3], "eliminated": 0, "points": 1}, "2": {"eliminated": 1, "points": 0}}}},

  {"name": "Baron: the active player's own lower card (1 against 4) is eliminated", "rule": "R10", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [3]}, "2": {"hand": [4]}},
             "game": {"new_hand": 0, "active_seat": 1, "starter_seat": 1, "round_number": 5, "stake": 1,
                      "deck": [1, 2, 1], "reserve": [1], "deck_count": 4}},
   "rules": [{"seat": 1, "options_include": 3}],
   "expect": {"players": {"1": {"eliminated": 1, "points": 0}, "2": {"eliminated": 0, "points": 1}}}},

  {"name": "Baron: equal ranks (4 and 4) eliminate nobody", "rule": "R10", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [3]}, "2": {"hand": [4]}},
             "game": {"new_hand": 0, "active_seat": 1, "starter_seat": 1, "round_number": 5, "stake": 1,
                      "deck": [4, 2, 1], "reserve": [1], "deck_count": 4}},
   "rules": [{"seat": 1, "options_include": 3}],
   "expect": {"players": {"1": {"eliminated": 0, "points": 0, "discards": [3]}, "2": {"eliminated": 0, "points": 0}}}},

  {"name": "A Handmaid sets protected = 1", "rule": "R11", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [4]}, "2": {"hand": [1]}},
             "game": {"new_hand": 0, "active_seat": 1, "starter_seat": 1, "round_number": 5, "stake": 1,
                      "deck": [2, 1, 1], "reserve": [1], "deck_count": 4}},
   "rules": [{"seat": 1, "options_include": 4}],
   "expect": {"players": {"1": {"discards": [4], "protected": 1}, "2": {"protected": 0}}}},

  {"name": "A Prince makes the unprotected opponent discard its card (4) and redraw", "rule": "R12", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [5]}, "2": {"hand": [4]}},
             "game": {"new_hand": 0, "active_seat": 1, "starter_seat": 1, "round_number": 5, "stake": 1,
                      "deck": [1, 3, 2], "reserve": [2], "deck_count": 4}},
   "rules": [{"seat": 1, "options_include": 5}],
   "expect": {"players": {"1": {"discards": [5]}, "2": {"discards": [4], "eliminated": 0}},
              "lens": {"players": {"2": {"hand": 1}}},
              "game": {"deck_count": 2, "stake": 1}}},

  {"name": "A Prince with the opponent protected targets the active player itself", "rule": "R12", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [5]}, "2": {"hand": [1], "protected": 1, "discards": [4]}},
             "game": {"new_hand": 0, "active_seat": 1, "starter_seat": 1, "round_number": 5, "stake": 1,
                      "deck": [2, 6, 1], "reserve": [1], "deck_count": 4}},
   "rules": [{"seat": 1, "options_include": 5}],
   "expect": {"players": {"1": {"discards": [5, 2], "eliminated": 0}, "2": {"discards": [4], "protected": 1}},
              "game": {"deck_count": 2}}},

  {"name": "A Prince forcing the Princess out eliminates its holder, with no redraw", "rule": "R13", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [5]}, "2": {"hand": [8]}},
             "game": {"new_hand": 0, "active_seat": 1, "starter_seat": 1, "round_number": 5, "stake": 1,
                      "deck": [1, 2, 3], "reserve": [4], "deck_count": 4}},
   "rules": [{"seat": 1, "options_include": 5}],
   "expect": {"players": {"1": {"points": 1}, "2": {"discards": [8], "eliminated": 1, "points": 0}},
              "game": {"deck_count": 3}}},

  {"name": "A Prince redraw with an empty deck takes the reserve (3), then the showdown 3 beats 1", "rule": "R14", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [5]}, "2": {"hand": [6]}},
             "game": {"new_hand": 0, "active_seat": 1, "starter_seat": 1, "round_number": 5, "stake": 1,
                      "deck": [1], "reserve": [3], "deck_count": 2}},
   "rules": [{"seat": 1, "options_include": 5}],
   "expect": {"players": {"1": {"discards": [5], "points": 0}, "2": {"discards": [6], "eliminated": 0, "points": 1}},
              "game": {"deck_count": 0}}},

  {"name": "A King swaps the hands: seat 1 gets the 8 and wins the showdown", "rule": "R15", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [6]}, "2": {"hand": [8]}},
             "game": {"new_hand": 0, "active_seat": 1, "starter_seat": 1, "round_number": 5, "stake": 1,
                      "deck": [1], "reserve": [2], "deck_count": 2}},
   "rules": [{"seat": 1, "options_include": 6}],
   "expect": {"players": {"1": {"discards": [6], "points": 1}, "2": {"points": 0}},
              "game": {"deck_count": 1}}},

  {"name": "Discarding the Princess eliminates the active player", "rule": "R16", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [8]}, "2": {"hand": [1]}},
             "game": {"new_hand": 0, "active_seat": 1, "starter_seat": 1, "round_number": 5, "stake": 1,
                      "deck": [2, 1, 1], "reserve": [1], "deck_count": 4}},
   "rules": [{"seat": 1, "options_include": 8}],
   "expect": {"players": {"1": {"discards": [8], "eliminated": 1, "points": 0}, "2": {"points": 1}}}},

  {"name": "A Guard against a protected opponent asks no guess", "rule": "R17", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [1]}, "2": {"hand": [5], "protected": 1, "discards": [4]}},
             "game": {"new_hand": 0, "active_seat": 1, "starter_seat": 1, "round_number": 5, "stake": 1,
                      "deck": [2, 1, 1], "reserve": [1], "deck_count": 4}},
   "rules": [{"seat": 1, "options_include": 1}],
   "expect": {"players": {"1": {"discards": [1]}, "2": {"eliminated": 0}},
              "not_offered": [{"seat": 1, "option": 8}, {"seat": 1, "option": 5}]}},

  {"name": "A Baron against a protected opponent does nothing (1 against 8)", "rule": "R17", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [3]}, "2": {"hand": [8], "protected": 1, "discards": [4]}},
             "game": {"new_hand": 0, "active_seat": 1, "starter_seat": 1, "round_number": 5, "stake": 1,
                      "deck": [1, 2, 1], "reserve": [1], "deck_count": 4}},
   "rules": [{"seat": 1, "options_include": 3}],
   "expect": {"players": {"1": {"eliminated": 0, "points": 0}, "2": {"eliminated": 0, "points": 0}}}},

  {"name": "A King against a protected opponent does not swap: seat 2 keeps the 8 and wins the showdown", "rule": "R17", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [6]}, "2": {"hand": [8], "protected": 1, "discards": [4]}},
             "game": {"new_hand": 0, "active_seat": 1, "starter_seat": 1, "round_number": 5, "stake": 1,
                      "deck": [1], "reserve": [2], "deck_count": 2}},
   "rules": [{"seat": 1, "options_include": 6}],
   "expect": {"players": {"1": {"points": 0}, "2": {"points": 1}}}},

  {"name": "A raise is offered when stake is 1, deck_count is 3 and the opponent has a discard; pass keeps stake 1", "rule": "R18", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [4]}, "2": {"hand": [3], "discards": [1]}},
             "game": {"new_hand": 0, "active_seat": 1, "starter_seat": 1, "round_number": 5, "stake": 1,
                      "deck": [2, 1, 1], "reserve": [1], "deck_count": 4}},
   "rules": [{"seat": 1, "options_include": 2}, {"seat": 1, "options_include": "pass"}],
   "expect": {"game": {"stake": 1},
              "offered": [{"seat": 1, "option": "raise"}, {"seat": 1, "option": "pass"}],
              "not_offered": [{"seat": 2, "option": "accept"}, {"seat": 2, "option": "fold"}]}},

  {"name": "No raise is offered when the opponent has no discards", "rule": "R18", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [4]}, "2": {"hand": [3], "discards": []}},
             "game": {"new_hand": 0, "active_seat": 1, "starter_seat": 1, "round_number": 5, "stake": 1,
                      "deck": [2, 1, 1], "reserve": [1], "deck_count": 4}},
   "rules": [{"seat": 1, "options_include": 2}],
   "expect": {"game": {"stake": 1},
              "not_offered": [{"seat": 1, "option": "raise"}]}},

  {"name": "No raise is offered when the stake is already 2", "rule": "R18", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [4]}, "2": {"hand": [3], "discards": [1]}},
             "game": {"new_hand": 0, "active_seat": 1, "starter_seat": 1, "round_number": 5, "stake": 2,
                      "deck": [2, 1, 1], "reserve": [1], "deck_count": 4}},
   "rules": [{"seat": 1, "options_include": 2}],
   "expect": {"game": {"stake": 2},
              "not_offered": [{"seat": 1, "option": "raise"}]}},

  {"name": "A raise accepted sets the stake to 2", "rule": "R19", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [4]}, "2": {"hand": [3], "discards": [1]}},
             "game": {"new_hand": 0, "active_seat": 1, "starter_seat": 1, "round_number": 5, "stake": 1,
                      "deck": [2, 1, 1], "reserve": [1], "deck_count": 4}},
   "rules": [{"seat": 1, "options_include": 2}, {"seat": 1, "options_include": "raise"}, {"seat": 2, "options_include": "accept"}],
   "expect": {"game": {"stake": 2},
              "players": {"1": {"points": 0}, "2": {"points": 0}},
              "offered": [{"seat": 2, "option": "accept"}, {"seat": 2, "option": "fold"}]}},

  {"name": "Folding to a raise gives the raiser 1 point and ends the hand", "rule": "R20", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [4]}, "2": {"hand": [3], "discards": [1]}},
             "game": {"new_hand": 0, "active_seat": 1, "starter_seat": 1, "round_number": 5, "stake": 1,
                      "deck": [2, 1, 1], "reserve": [1], "deck_count": 4}},
   "rules": [{"seat": 1, "options_include": 2}, {"seat": 1, "options_include": "raise"}, {"seat": 2, "options_include": "fold"}],
   "expect": {"players": {"1": {"points": 1}, "2": {"points": 0}},
              "game": {"round_number": 6}}},

  {"name": "An elimination at stake 2 gives the other player 2 points", "rule": "R21", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [1], "points": 1}, "2": {"hand": [5], "discards": [2]}},
             "game": {"new_hand": 0, "active_seat": 1, "starter_seat": 1, "round_number": 5, "stake": 2,
                      "deck": [4, 2, 3], "reserve": [1], "deck_count": 4}},
   "rules": [{"seat": 1, "options_include": 1}, {"seat": 1, "options_include": 5}],
   "expect": {"players": {"1": {"points": 3}, "2": {"eliminated": 1, "points": 0}}}},

  {"name": "Showdown at deck_count 1: the higher card (7 over 5) gains the stake of 2", "rule": "R22", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [7]}, "2": {"hand": [5]}},
             "game": {"new_hand": 0, "active_seat": 1, "starter_seat": 1, "round_number": 5, "stake": 2,
                      "deck": [2], "reserve": [1], "deck_count": 2}},
   "rules": [{"seat": 1, "options_include": 2}],
   "expect": {"players": {"1": {"points": 2}, "2": {"points": 0}},
              "game": {"deck_count": 1}}},

  {"name": "Showdown with equal cards (4 and 4) scores nothing", "rule": "R22", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [4]}, "2": {"hand": [4]}},
             "game": {"new_hand": 0, "active_seat": 1, "starter_seat": 1, "round_number": 5, "stake": 1,
                      "deck": [2], "reserve": [1], "deck_count": 2}},
   "rules": [{"seat": 1, "options_include": 2}],
   "expect": {"players": {"1": {"points": 0}, "2": {"points": 0}}}},

  {"name": "Without a hand end the turn passes to the opponent", "rule": "R23", "players": 2, "rounds": 2, "default": "decline",
   "given": {"players": {"1": {"hand": [4]}, "2": {"hand": [2]}},
             "game": {"new_hand": 0, "active_seat": 1, "starter_seat": 1, "round_number": 5, "stake": 1,
                      "deck": [4, 2, 1, 1], "reserve": [1], "deck_count": 5}},
   "rules": [{"seat": 1, "options_include": 4}, {"seat": 2, "options_include": 2}],
   "expect": {"players": {"1": {"discards": [4], "protected": 1}, "2": {"discards": [2]}},
              "game": {"deck_count": 3, "round_number": 7, "stake": 1}}},

  {"name": "After a hand ends the starter switches and seat 2 starts the new hand", "rule": "R23", "players": 2, "rounds": 2, "default": "decline",
   "given": {"players": {"1": {"hand": [8]}, "2": {"hand": [1]}},
             "game": {"full_deck": [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4], "new_hand": 0, "active_seat": 1, "starter_seat": 1, "round_number": 5, "stake": 1,
                      "deck": [2, 1, 1], "reserve": [1], "deck_count": 4}},
   "rules": [{"seat": 1, "options_include": 8}, {"seat": 2, "options_include": 4}],
   "expect": {"players": {"1": {"discards": [], "eliminated": 0, "points": 0}, "2": {"discards": [4], "protected": 1, "points": 1}},
              "game": {"deck_count": 8, "round_number": 7}}},

  {"name": "Round 40 showdown (6 over 1) decides the game: seat 1 wins 4 to 3", "rule": "R24", "players": 2, "default": "decline",
   "given": {"players": {"1": {"hand": [6], "points": 3}, "2": {"hand": [1], "points": 3}},
             "game": {"new_hand": 0, "active_seat": 1, "starter_seat": 1, "round_number": 40, "stake": 1,
                      "deck": [2, 3, 4, 1], "reserve": [1], "deck_count": 5}},
   "rules": [{"seat": 1, "options_include": 2}],
   "expect": {"winner": 1, "standings": {"1": 4, "2": 3},
              "players": {"1": {"points": 4}, "2": {"points": 3}}}},

  {"name": "Round 40 showdown with equal cards leaves the points equal: shared win", "rule": "R24", "players": 2, "default": "decline",
   "given": {"players": {"1": {"hand": [4], "points": 2}, "2": {"hand": [4], "points": 2}},
             "game": {"new_hand": 0, "active_seat": 1, "starter_seat": 1, "round_number": 40, "stake": 1,
                      "deck": [2, 3, 1, 1], "reserve": [1], "deck_count": 5}},
   "rules": [{"seat": 1, "options_include": 2}],
   "expect": {"winner": [1, 2], "standings": {"1": 2, "2": 2}}}
]
```
````
