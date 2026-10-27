# 32 scenarios

- time: 2026-10-27T19:08:37+00:00 (129.0s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 802509bc7de94308, reply sha256 6813bfff329ef4f7

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
````

## Reply

````
[
{"name":"New hand: 5 cards set aside face up, 1 card each, reserve of 1 (chance: only counts asserted)","rule":"R1","players":2,"rounds":1,"seed":1,"default":"decline",
 "expect":{"lens":{"game":{"out_of_play":5,"reserve":1},"players":{"1":{"discards":1}}},"game":{"round_number":2}}},

{"name":"Turn-start draw takes the top deck card and lowers deck_count by 1","rule":"R1","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"new_hand":0,"active_seat":1,"starter_seat":1,"stake":1,"round_number":5,"deck":[1,2,3,5,6,7,8,4],"reserve":[4],"deck_count":9},
          "players":{"1":{"hand":[1],"discards":[]},"2":{"hand":[1],"discards":[]}}},
 "rules":[{"seat":1,"options_include":3}],
 "expect":{"game":{"deck_count":8,"round_number":6},"players":{"1":{"discards":[1]},"2":{"eliminated":0}}}},

{"name":"New hand resets discards, protection, elimination and stake, and the starter seat plays first","rule":"R2","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"new_hand":1,"starter_seat":2,"active_seat":1,"stake":2,"full_deck":[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]},
          "players":{"1":{"discards":[3,4],"protected":1,"eliminated":1},"2":{"discards":[5],"protected":1,"eliminated":0}}},
 "expect":{"players":{"1":{"discards":[],"protected":0,"eliminated":0},"2":{"discards":[1],"eliminated":0}},
           "game":{"stake":1,"deck_count":8,"round_number":2}}},

{"name":"Turn start clears own protection and draws one card","rule":"R3","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"new_hand":0,"active_seat":1,"starter_seat":1,"stake":1,"round_number":3,"deck":[1,2,3,5,6],"reserve":[4],"deck_count":6},
          "players":{"1":{"hand":[1],"discards":[4],"protected":1},"2":{"hand":[3],"discards":[]}}},
 "rules":[{"seat":1,"options_include":5}],
 "expect":{"players":{"1":{"protected":0,"discards":[4,1]},"2":{"eliminated":0}},"game":{"deck_count":5,"round_number":4},
           "lens":{"players":{"1":{"hand":1}}}}},

{"name":"Reserve card is not drawn at turn start; showdown at deck_count 1","rule":"R4","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"new_hand":0,"active_seat":1,"starter_seat":1,"stake":1,"round_number":5,"deck":[2],"reserve":[8],"deck_count":2},
          "players":{"1":{"hand":[1],"discards":[]},"2":{"hand":[3],"discards":[]}}},
 "rules":[{"seat":1,"options_include":2}],
 "expect":{"lens":{"game":{"reserve":1,"deck":0}},"game":{"deck_count":1},"players":{"1":{"discards":[2],"points":0},"2":{"points":1}}}},

{"name":"Chosen discard moves from hand to the end of discards","rule":"R5","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"new_hand":0,"active_seat":1,"starter_seat":1,"stake":1,"round_number":5,"deck":[2,5,5,6,7],"reserve":[4],"deck_count":6},
          "players":{"1":{"hand":[1],"discards":[1]},"2":{"hand":[3],"discards":[]}}},
 "rules":[{"seat":1,"options_include":2}],
 "expect":{"players":{"1":{"discards":[1,2]},"2":{"eliminated":0}},"lens":{"players":{"1":{"hand":1}}},"game":{"deck_count":5}}},

{"name":"Countess with Prince must be discarded; Prince not offered","rule":"R6","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"new_hand":0,"active_seat":1,"starter_seat":1,"stake":1,"round_number":5,"deck":[5,1,2,3,6],"reserve":[4],"deck_count":6},
          "players":{"1":{"hand":[7],"discards":[]},"2":{"hand":[3],"discards":[]}}},
 "rules":[{"seat":1,"options_include":5}],
 "expect":{"players":{"1":{"discards":[7]},"2":{"discards":[]}},"not_offered":[{"seat":1,"option":5}],"game":{"deck_count":5}}},

{"name":"Countess with King must be discarded; no swap happens","rule":"R6","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"new_hand":0,"active_seat":1,"starter_seat":1,"stake":1,"round_number":5,"deck":[6,1,2,3,5],"reserve":[4],"deck_count":6},
          "players":{"1":{"hand":[7],"discards":[]},"2":{"hand":[3],"discards":[]}}},
 "rules":[{"seat":1,"options_include":6}],
 "expect":{"players":{"1":{"discards":[7]}},"not_offered":[{"seat":1,"option":6}]}},

{"name":"Guard on unprotected opponent asks for a guess 2..8; wrong guess misses","rule":"R7","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"new_hand":0,"active_seat":1,"starter_seat":1,"stake":1,"round_number":5,"deck":[1,2,3,5,6],"reserve":[4],"deck_count":6},
          "players":{"1":{"hand":[1],"discards":[]},"2":{"hand":[5],"discards":[]}}},
 "rules":[{"seat":1,"options_include":3}],
 "expect":{"offered":[{"seat":1,"option":2},{"seat":1,"option":8}],"players":{"2":{"eliminated":0},"1":{"points":0,"discards":[1]}}}},

{"name":"Correct Guard guess eliminates the opponent and the guesser scores the stake","rule":"R8","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"new_hand":0,"active_seat":1,"starter_seat":1,"stake":1,"round_number":5,"deck":[1,2,3,5,6],"reserve":[4],"deck_count":6},
          "players":{"1":{"hand":[1],"discards":[]},"2":{"hand":[5],"discards":[]}}},
 "rules":[{"seat":1,"options_include":5}],
 "expect":{"players":{"2":{"eliminated":1,"points":0},"1":{"points":1}}}},

{"name":"Priest changes nothing visible: nobody eliminated","rule":"R9","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"new_hand":0,"active_seat":1,"starter_seat":1,"stake":1,"round_number":5,"deck":[2,1,3,5,6],"reserve":[4],"deck_count":6},
          "players":{"1":{"hand":[1],"discards":[]},"2":{"hand":[5],"discards":[]}}},
 "rules":[{"seat":1,"options_include":2}],
 "expect":{"players":{"1":{"discards":[2],"eliminated":0,"points":0},"2":{"discards":[],"eliminated":0,"points":0}},"game":{"deck_count":5}}},

{"name":"Baron: opponent's lower card is eliminated","rule":"R10","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"new_hand":0,"active_seat":1,"starter_seat":1,"stake":1,"round_number":5,"deck":[5,1,2,3,6],"reserve":[4],"deck_count":6},
          "players":{"1":{"hand":[3],"discards":[]},"2":{"hand":[2],"discards":[]}}},
 "rules":[{"seat":1,"options_include":3}],
 "expect":{"players":{"2":{"eliminated":1},"1":{"eliminated":0,"points":1}}}},

{"name":"Baron: active player's lower card is eliminated","rule":"R10","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"new_hand":0,"active_seat":1,"starter_seat":1,"stake":1,"round_number":5,"deck":[1,2,3,5,7],"reserve":[4],"deck_count":6},
          "players":{"1":{"hand":[3],"discards":[]},"2":{"hand":[6],"discards":[]}}},
 "rules":[{"seat":1,"options_include":3}],
 "expect":{"players":{"1":{"eliminated":1,"points":0},"2":{"eliminated":0,"points":1}}}},

{"name":"Baron: equal ranks, nothing happens","rule":"R10","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"new_hand":0,"active_seat":1,"starter_seat":1,"stake":1,"round_number":5,"deck":[4,1,2,5,7],"reserve":[1],"deck_count":6},
          "players":{"1":{"hand":[3],"discards":[]},"2":{"hand":[4],"discards":[]}}},
 "rules":[{"seat":1,"options_include":3}],
 "expect":{"players":{"1":{"eliminated":0,"points":0},"2":{"eliminated":0,"points":0}}}},

{"name":"Handmaid sets protected to 1","rule":"R11","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"new_hand":0,"active_seat":1,"starter_seat":1,"stake":1,"round_number":5,"deck":[4,1,2,3,5],"reserve":[6],"deck_count":6},
          "players":{"1":{"hand":[1],"discards":[]},"2":{"hand":[3],"discards":[]}}},
 "rules":[{"seat":1,"options_include":4}],
 "expect":{"players":{"1":{"protected":1,"discards":[4]},"2":{"protected":0}}}},

{"name":"Prince makes the opponent discard and redraw from the deck","rule":"R12","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"new_hand":0,"active_seat":1,"starter_seat":1,"stake":1,"round_number":5,"deck":[2,6,3,1],"reserve":[1],"deck_count":5},
          "players":{"1":{"hand":[5],"discards":[]},"2":{"hand":[4],"discards":[]}}},
 "rules":[{"seat":1,"options_include":5}],
 "expect":{"players":{"1":{"discards":[5]},"2":{"discards":[4],"eliminated":0}},"game":{"deck_count":3,"stake":1},"lens":{"players":{"2":{"hand":1}}}}},

{"name":"Prince with protected opponent targets the active player","rule":"R12","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"new_hand":0,"active_seat":1,"starter_seat":1,"stake":1,"round_number":5,"deck":[2,6,3,1],"reserve":[1],"deck_count":5},
          "players":{"1":{"hand":[5],"discards":[]},"2":{"hand":[4],"discards":[],"protected":1}}},
 "rules":[{"seat":1,"options_include":5}],
 "expect":{"players":{"1":{"discards":[5,2],"eliminated":0},"2":{"discards":[],"protected":1}},"game":{"deck_count":3}}},

{"name":"Prince forcing the Princess eliminates the target with no redraw","rule":"R13","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"new_hand":0,"active_seat":1,"starter_seat":1,"stake":1,"round_number":5,"deck":[2,6,3,1],"reserve":[1],"deck_count":5},
          "players":{"1":{"hand":[5],"discards":[]},"2":{"hand":[8],"discards":[]}}},
 "rules":[{"seat":1,"options_include":5}],
 "expect":{"players":{"2":{"discards":[8],"eliminated":1},"1":{"points":1}},"game":{"deck_count":4}}},

{"name":"Prince redraw takes the reserve when the deck is empty, then showdown","rule":"R14","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"new_hand":0,"active_seat":1,"starter_seat":1,"stake":1,"round_number":5,"deck":[5],"reserve":[3],"deck_count":2},
          "players":{"1":{"hand":[1],"discards":[]},"2":{"hand":[2],"discards":[]}}},
 "rules":[{"seat":1,"options_include":5}],
 "expect":{"players":{"2":{"discards":[2],"eliminated":0,"points":1},"1":{"discards":[5],"points":0}},"game":{"deck_count":0},"lens":{"game":{"reserve":0}}}},

{"name":"King swaps hands: the swapped Countess wins the showdown","rule":"R15","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"new_hand":0,"active_seat":1,"starter_seat":1,"stake":1,"round_number":5,"deck":[2],"reserve":[1],"deck_count":2},
          "players":{"1":{"hand":[6],"discards":[]},"2":{"hand":[7],"discards":[]}}},
 "rules":[{"seat":1,"options_include":6}],
 "expect":{"players":{"1":{"discards":[6],"points":1},"2":{"points":0}},"game":{"deck_count":1}}},

{"name":"Discarding the Princess eliminates the active player","rule":"R16","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"new_hand":0,"active_seat":1,"starter_seat":1,"stake":1,"round_number":5,"deck":[1,2,3,5,6],"reserve":[4],"deck_count":6},
          "players":{"1":{"hand":[8],"discards":[]},"2":{"hand":[3],"discards":[]}}},
 "rules":[{"seat":1,"options_include":8}],
 "expect":{"players":{"1":{"eliminated":1,"discards":[8],"points":0},"2":{"points":1}}}},

{"name":"Guard against a protected opponent: no guess asked, no effect","rule":"R17","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"new_hand":0,"active_seat":1,"starter_seat":1,"stake":1,"round_number":5,"deck":[1,2,3,5,6],"reserve":[4],"deck_count":6},
          "players":{"1":{"hand":[1],"discards":[]},"2":{"hand":[5],"discards":[],"protected":1}}},
 "rules":[{"seat":1,"options_include":5}],
 "expect":{"not_offered":[{"seat":1,"option":5},{"seat":1,"option":8}],"players":{"2":{"eliminated":0,"protected":1},"1":{"discards":[1],"points":0}}}},

{"name":"Baron against a protected opponent has no effect","rule":"R17","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"new_hand":0,"active_seat":1,"starter_seat":1,"stake":1,"round_number":5,"deck":[1,2,3,5,7],"reserve":[4],"deck_count":6},
          "players":{"1":{"hand":[3],"discards":[]},"2":{"hand":[6],"discards":[],"protected":1}}},
 "rules":[{"seat":1,"options_include":3}],
 "expect":{"players":{"1":{"eliminated":0,"points":0},"2":{"eliminated":0,"points":0,"protected":1}}}},

{"name":"Raise is offered when the opponent has a discard; passing keeps stake 1","rule":"R18","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"new_hand":0,"active_seat":1,"starter_seat":1,"stake":1,"round_number":5,"deck":[4,1,2,3,5],"reserve":[6],"deck_count":6},
          "players":{"1":{"hand":[4],"discards":[]},"2":{"hand":[3],"discards":[1]}}},
 "rules":[{"seat":1,"options_include":"pass"}],
 "expect":{"offered":[{"seat":1,"option":"raise"}],"game":{"stake":1}}},

{"name":"No raise offered when the opponent has no discard","rule":"R18","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"new_hand":0,"active_seat":1,"starter_seat":1,"stake":1,"round_number":5,"deck":[4,1,2,3,5],"reserve":[6],"deck_count":6},
          "players":{"1":{"hand":[4],"discards":[]},"2":{"hand":[3],"discards":[]}}},
 "rules":[{"seat":1,"options_include":"raise"}],
 "expect":{"not_offered":[{"seat":1,"option":"raise"}],"game":{"stake":1}}},

{"name":"No raise offered when stake is already 2","rule":"R18","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"new_hand":0,"active_seat":1,"starter_seat":1,"stake":2,"round_number":5,"deck":[4,1,2,3,5],"reserve":[6],"deck_count":6},
          "players":{"1":{"hand":[4],"discards":[]},"2":{"hand":[3],"discards":[1]}}},
 "rules":[{"seat":1,"options_include":"raise"}],
 "expect":{"not_offered":[{"seat":1,"option":"raise"}],"game":{"stake":2}}},

{"name":"Raise accepted sets stake to 2","rule":"R19","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"new_hand":0,"active_seat":1,"starter_seat":1,"stake":1,"round_number":5,"deck":[4,1,2,3,5],"reserve":[6],"deck_count":6},
          "players":{"1":{"hand":[4],"discards":[]},"2":{"hand":[3],"discards":[1]}}},
 "rules":[{"seat":1,"options_include":"raise"},{"seat":2,"options_include":"accept"}],
 "expect":{"offered":[{"seat":2,"option":"fold"}],"game":{"stake":2,"deck_count":5},"players":{"1":{"points":0},"2":{"points":0}}}},

{"name":"Fold gives the raiser 1 point and ends the hand","rule":"R20","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"new_hand":0,"active_seat":1,"starter_seat":1,"stake":1,"round_number":5,"deck":[4,1,2,3,5],"reserve":[6],"deck_count":6},
          "players":{"1":{"hand":[4],"discards":[],"points":2},"2":{"hand":[3],"discards":[1],"points":1}}},
 "rules":[{"seat":1,"options_include":"raise"},{"seat":2,"options_include":"fold"}],
 "expect":{"players":{"1":{"points":3},"2":{"points":1}},"game":{"stake":1}}},

{"name":"Elimination at stake 2 gives the other player 2 points","rule":"R21","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"new_hand":0,"active_seat":1,"starter_seat":1,"stake":2,"round_number":5,"deck":[1,2,3,5,6],"reserve":[4],"deck_count":6},
          "players":{"1":{"hand":[1],"discards":[]},"2":{"hand":[6],"discards":[1]}}},
 "rules":[{"seat":1,"options_include":6}],
 "expect":{"players":{"1":{"points":2},"2":{"eliminated":1,"points":0}}}},

{"name":"Showdown with equal ranks scores nothing","rule":"R22","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"new_hand":0,"active_seat":1,"starter_seat":1,"stake":1,"round_number":5,"deck":[2],"reserve":[1],"deck_count":2},
          "players":{"1":{"hand":[4],"discards":[]},"2":{"hand":[4],"discards":[]}}},
 "rules":[{"seat":1,"options_include":2}],
 "expect":{"players":{"1":{"points":0},"2":{"points":0}},"game":{"deck_count":1}}},

{"name":"Round 40 forces a showdown; higher card wins the game","rule":"R22","players":2,"default":"decline",
 "given":{"game":{"new_hand":0,"active_seat":1,"starter_seat":1,"stake":1,"round_number":40,"deck":[4,1,2,3,5],"reserve":[1],"deck_count":6},
          "players":{"1":{"hand":[6],"discards":[]},"2":{"hand":[3],"discards":[]}}},
 "rules":[{"seat":1,"options_include":4}],
 "expect":{"winner":1,"standings":{"1":1,"2":0},"players":{"1":{"points":1},"2":{"points":0}}}},

{"name":"After a hand ends the starter switches: seat 2 opens the next hand","rule":"R23","players":2,"rounds":2,"default":"decline",
 "given":{"game":{"new_hand":0,"active_seat":1,"starter_seat":1,"stake":1,"round_number":5,"deck":[1,2,3,5,6],"reserve":[4],"deck_count":6,"full_deck":[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]},
          "players":{"1":{"hand":[8],"discards":[]},"2":{"hand":[3],"discards":[]}}},
 "rules":[{"seat":1,"options_include":8}],
 "expect":{"players":{"1":{"discards":[],"eliminated":0,"points":0},"2":{"discards":[1],"points":1}},"game":{"round_number":7,"deck_count":8}}},

{"name":"Without a hand end the turn passes to the opponent","rule":"R23","players":2,"rounds":2,"default":"decline",
 "given":{"game":{"new_hand":0,"active_seat":1,"starter_seat":1,"stake":1,"round_number":5,"deck":[4,1,2,3,5],"reserve":[6],"deck_count":6},
          "players":{"1":{"hand":[4],"discards":[]},"2":{"hand":[1],"discards":[]}}},
 "rules":[{"seat":1,"options_include":4}],
 "expect":{"players":{"1":{"discards":[4],"protected":1,"eliminated":0},"2":{"discards":[1]}},"game":{"deck_count":4,"round_number":7}}},

{"name":"Game ends after round 40; equal points share the win","rule":"R24","players":2,"default":"decline",
 "given":{"game":{"new_hand":0,"active_seat":1,"starter_seat":1,"stake":1,"round_number":40,"deck":[1,2,3,5,7],"reserve":[4],"deck_count":6},
          "players":{"1":{"hand":[1],"discards":[],"points":4},"2":{"hand":[6],"discards":[],"points":5}}},
 "rules":[{"seat":1,"options_include":6}],
 "expect":{"winner":[1,2],"standings":{"1":5,"2":5},"players":{"1":{"points":5},"2":{"points":5,"eliminated":1}}}}
]
````
