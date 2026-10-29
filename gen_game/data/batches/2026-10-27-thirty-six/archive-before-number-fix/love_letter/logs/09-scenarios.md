# 09 scenarios

- time: 2026-10-27T18:20:13+00:00 (68.3s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 f120abd309d69adc, reply sha256 2faa88c6399da089

## Sent

````
SPEC:
{
  "name": "Love Letter: One Raise",
  "summary": "Two-player Love Letter with a 16-card deck in which, once per hand, the player about to draw may raise the stake from 1 to 2 and the opponent must accept or concede 1 point; first to 5 points wins, capped at 40 turns.",
  "players": {
    "min": 2,
    "max": 2,
    "suggested": 2
  },
  "parameters": {
    "deck_size": 16,
    "guard_rank": 1,
    "guard_copies": 5,
    "priest_rank": 2,
    "priest_copies": 2,
    "baron_rank": 3,
    "baron_copies": 2,
    "handmaid_rank": 4,
    "handmaid_copies": 2,
    "prince_rank": 5,
    "prince_copies": 2,
    "king_rank": 6,
    "king_copies": 1,
    "countess_rank": 7,
    "countess_copies": 1,
    "princess_rank": 8,
    "princess_copies": 1,
    "removed_face_up": 3,
    "cards_dealt_per_player": 1,
    "deck_after_deal": 11,
    "burned_cards": 1,
    "starting_points": 0,
    "starting_hands_won": 0,
    "starting_stake": 1,
    "raised_stake": 2,
    "concede_gain": 1,
    "max_raises_per_hand": 1,
    "guard_guess_min": 2,
    "guard_guess_max": 8,
    "hand_end_deck_threshold": 1,
    "points_to_win": 5,
    "max_turns": 40,
    "first_starter_seat": 1
  },
  "attributes": {
    "player": [
      {
        "key": "points",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "match points; the score",
        "observable": true
      },
      {
        "key": "hands_won",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "hands won, the tie-break at turn 40",
        "observable": true
      },
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "card ranks held: 1 between turns, 2 after drawing",
        "observable": false
      },
      {
        "key": "discard_sum",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "sum of the ranks this player discarded this hand",
        "observable": false
      },
      {
        "key": "protected",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "has Handmaid protection",
        "observable": false
      },
      {
        "key": "eliminated",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "knocked out of the current hand",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "turn",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "turns played so far",
        "observable": true
      },
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "drawable cards, in random order (excludes the burned card)",
        "observable": false
      },
      {
        "key": "burned",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "the bottom card of the deck, drawn only by a Prince when the deck is otherwise empty",
        "observable": false
      },
      {
        "key": "removed",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "the 3 cards removed face up this hand",
        "observable": false
      },
      {
        "key": "new_hand_due",
        "type": "bool",
        "visible": "none",
        "initial": true,
        "meaning": "a new hand starts this turn",
        "observable": false
      },
      {
        "key": "starter_seat",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "the seat that starts the current or next hand",
        "observable": false
      },
      {
        "key": "active_seat",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "the active player this turn",
        "observable": false
      },
      {
        "key": "stake",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "points the winner of this hand gains",
        "observable": false
      },
      {
        "key": "raised",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "a raise has been accepted this hand",
        "observable": false
      },
      {
        "key": "raise_choice",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "the active player's raise or no raise this turn",
        "observable": false
      },
      {
        "key": "response",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "the opponent's accept or concede",
        "observable": false
      },
      {
        "key": "last_discard",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "rank of the card the active player discarded this turn",
        "observable": false
      },
      {
        "key": "guard_guess",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "the number named with a Guard",
        "observable": false
      },
      {
        "key": "prince_target",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "seat targeted by a Prince",
        "observable": false
      },
      {
        "key": "prince_discard",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "card discarded by the Prince's target",
        "observable": false
      },
      {
        "key": "hand_over",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "the current hand ended this turn",
        "observable": false
      },
      {
        "key": "hand_winner",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "seat that won the hand that just ended (0 if nobody)",
        "observable": false
      }
    ]
  },
  "setup": [
    "Seat 1 and Seat 2 each start with 0 points and 0 hands won.",
    "turn = 0, starter_seat = 1 and new_hand_due = true, so turn 1 starts hand 1 with Seat 1 active."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When new_hand_due: deck = [1,1,1,1,1,2,2,3,3,4,4,5,5,6,7,8]. Move 3 random cards from deck to removed. Move 1 random card to the starter_seat player's hand, then 1 to the other player's hand. Move 1 random card from deck to burned, leaving 10 in deck. stake = 1, raised = false, hand_over = false, hand_winner = 0. Every player: protected = false, eliminated = false, discard_sum = 0. active_seat = starter_seat, new_hand_due = false."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "When a new hand was just started: announce the 3 cards in removed and which seat starts."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player sees their own hand."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "turn += 1; raise_choice = '', response = '', last_discard = 0, guard_guess = 0, prince_target = 0, prince_discard = 0."
    },
    {
      "action": "ask",
      "who": "the active player",
      "answer": "raise | no raise",
      "effect": "When raised == false: set raise_choice."
    },
    {
      "action": "ask",
      "who": "the opponent of the active player",
      "answer": "accept | concede",
      "effect": "When raise_choice == 'raise': set response."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "If response == 'concede': the active player's points += 1 and hands_won += 1; hand_winner = active_seat; hand_over = true. If response == 'accept': stake = 2 and raised = true."
    },
    {
      "action": "update",
      "who": "the active player",
      "answer": null,
      "effect": "When hand_over == false: the active player's protected = false; move 1 random card from deck to their hand."
    },
    {
      "action": "sync",
      "who": "the active player",
      "answer": null,
      "effect": "When hand_over == false: the active player sees both of their cards."
    },
    {
      "action": "ask",
      "who": "the active player",
      "answer": "one of the two ranks in their hand (only 7 if the hand holds 7 together with 5 or 6)",
      "effect": "When hand_over == false: set last_discard to the chosen rank."
    },
    {
      "action": "update",
      "who": "the active player",
      "answer": null,
      "effect": "When hand_over == false: remove last_discard from the active player's hand; their discard_sum += last_discard. If last_discard == 4, they become protected = true. If last_discard == 8, they become eliminated = true."
    },
    {
      "action": "ask",
      "who": "the active player",
      "answer": "a whole number from 2 to 8",
      "effect": "When hand_over == false and last_discard == 1: set guard_guess."
    },
    {
      "action": "ask",
      "who": "the active player",
      "answer": "self | opponent (only self if the opponent is protected)",
      "effect": "When hand_over == false and last_discard == 5: prince_target = the chosen seat."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Guard: when hand_over == false, last_discard == 1, the opponent is not protected and the opponent's hand card == guard_guess, the opponent's eliminated = true."
    },
    {
      "action": "tell",
      "who": "the active player",
      "answer": null,
      "effect": "Priest: when hand_over == false, last_discard == 2 and the opponent is not protected, privately show the opponent's hand card to the active player."
    },
    {
      "action": "tell",
      "who": "both players, each privately",
      "answer": null,
      "effect": "Baron: when hand_over == false, last_discard == 3 and the opponent is not protected, show each player the other's hand card privately."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Baron: when hand_over == false, last_discard == 3 and the opponent is not protected, the player whose hand card is lower gets eliminated = true; if the cards are equal, nothing happens."
    },
    {
      "action": "update",
      "who": "the Prince target",
      "answer": null,
      "effect": "Prince: when hand_over == false and last_discard == 5: prince_discard = the target's hand card; empty the target's hand; the target's discard_sum += prince_discard. If prince_discard == 8, the target's eliminated = true. Otherwise move 1 random card from deck to the target's hand, or the burned card if deck is empty."
    },
    {
      "action": "update",
      "who": "both players",
      "answer": null,
      "effect": "King: when hand_over == false, last_discard == 6 and the opponent is not protected, swap the two players' hand lists."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "When hand_over == false: each player sees their own current hand."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce last_discard, guard_guess or prince_target if any, prince_discard if any, any elimination with the eliminated player's revealed hand card, stake, both players' points, and the deck count (len(deck) + len(burned))."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When hand_over == false: if a player is eliminated, the other player's points += stake and hands_won += 1, hand_winner = that seat, hand_over = true. Otherwise, if len(deck) + len(burned) <= 1: the higher hand card wins, and on equal cards the higher discard_sum wins. The winner's points += stake and hands_won += 1, hand_winner = that seat; if both are equal, hand_winner = 0. hand_over = true."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "When a showdown happened: reveal both hand cards, both discard_sum values and the hand winner (or that nobody scored)."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "If hand_over: starter_seat = the seat that is not hand_winner if hand_winner != 0, else the seat that is not starter_seat; new_hand_due = true. If not hand_over: active_seat = the other seat."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if any player's points >= 5 or turn >= 40; otherwise continue."
    }
  ],
  "ending": {
    "condition": "any player's points >= 5 or turn >= 40",
    "rank_by": "you.points * 1000 + you.hands_won",
    "decided_by": "The player with the most points wins; the first to reach 5 ends the match at once, since only one player scores per hand. At the 40-turn limit, more points wins, then more hands won. Players level on both share the win, which is a draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "The deck has 16 cards: five 1s (Guard), two 2s (Priest), two 3s (Baron), two 4s (Handmaid), two 5s (Prince), one 6 (King), one 7 (Countess) and one 8 (Princess)."
    },
    {
      "id": "R2",
      "text": "When a hand starts, 3 random cards go face up to removed and are announced, each player gets 1 card, 1 card is set aside as burned, and 10 drawable cards remain."
    },
    {
      "id": "R3",
      "text": "When a hand starts, stake = 1, raised = false, and every player's protected = false, eliminated = false and discard_sum = 0."
    },
    {
      "id": "R4",
      "text": "Seat 1 starts hand 1."
    },
    {
      "id": "R5",
      "text": "When a hand had a winner, the other seat starts the next hand; when nobody scored, the seat that did not start it starts the next."
    },
    {
      "id": "R6",
      "text": "When no raise has been accepted this hand, the active player is asked 'raise' or 'no raise' before drawing; when raised == true, they are not asked."
    },
    {
      "id": "R7",
      "text": "When the active player raises and the opponent concedes, the active player gains 1 point and 1 hand won, and the hand ends with no draw or play."
    },
    {
      "id": "R8",
      "text": "When the active player raises and the opponent accepts, stake becomes 2 and no further raise is possible this hand."
    },
    {
      "id": "R9",
      "text": "When a turn goes on, the active player loses protection and draws 1 card from deck, then discards one of their two cards."
    },
    {
      "id": "R10",
      "text": "When the active player holds 7 together with 5 or 6, they must discard the 7."
    },
    {
      "id": "R11",
      "text": "When a card is discarded, its rank is added to its owner's discard_sum."
    },
    {
      "id": "R12",
      "text": "When a 4 (Handmaid) is discarded, its owner is protected until the start of their next turn."
    },
    {
      "id": "R13",
      "text": "When a player discards an 8 (Princess), by choice or through a Prince, they are eliminated."
    },
    {
      "id": "R14",
      "text": "When a 1 (Guard) is discarded, the active player names 2 to 8, and the unprotected opponent is eliminated if their card equals that number."
    },
    {
      "id": "R15",
      "text": "When a 2 (Priest) is discarded and the opponent is not protected, the active player privately sees the opponent's card."
    },
    {
      "id": "R16",
      "text": "When a 3 (Baron) is discarded and the opponent is not protected, the players privately see each other's cards and the lower card is eliminated; on equal cards nothing happens."
    },
    {
      "id": "R17",
      "text": "When a 5 (Prince) is discarded, the target (self or opponent, only self if the opponent is protected) discards their card without effect, adds it to their discard_sum, and draws 1 card, the burned card if the deck is empty."
    },
    {
      "id": "R18",
      "text": "When a 6 (King) is discarded and the opponent is not protected, the two players swap their cards."
    },
    {
      "id": "R19",
      "text": "When a 1, 2, 3 or 6 is discarded while the opponent is protected, it has no effect."
    },
    {
      "id": "R20",
      "text": "When a player is eliminated, the other player gains points equal to stake (1 or 2) and 1 hand won."
    },
    {
      "id": "R21",
      "text": "When no one is eliminated and 1 card or fewer remains in the deck (burned included), the higher card gains the stake; on equal cards the higher discard_sum gains it; if both are equal, nobody scores."
    },
    {
      "id": "R22",
      "text": "When a player reaches 5 points, the match ends and they win."
    },
    {
      "id": "R23",
      "text": "When turn 40 ends with nobody at 5, more points wins, then more hands won, and otherwise the match is a draw."
    },
    {
      "id": "R24",
      "text": "When a hand has not ended, the other player becomes active next turn; when it has ended, the next turn starts a new hand."
    }
  ],
  "offers": [
    {
      "question": "raise",
      "who": "the active player, only when raised == false",
      "options": "raise, no raise"
    },
    {
      "question": "response to a raise",
      "who": "the opponent of the active player, only after a raise",
      "options": "accept, concede"
    },
    {
      "question": "card to discard",
      "who": "the active player",
      "options": "holding 7 with 5 or 6: only 7; otherwise either of the two cards in hand"
    },
    {
      "question": "Guard number",
      "who": "the active player, after discarding a 1",
      "options": "whole number from 2 to 8"
    },
    {
      "question": "Prince target",
      "who": "the active player, after discarding a 5",
      "options": "opponent protected: self only; otherwise self or opponent"
    }
  ],
  "choices": [
    {
      "what": "2 players, suggested 2",
      "why": "The designer fixed the game at Seat 1 and Seat 2; the raise and concede duel is head to head and every rule addresses 'the opponent'. Strategy lies in raising on strong cards, bluffing raises on weak ones, and reading the removed and discarded cards."
    },
    {
      "what": "No free talk step",
      "why": "The source rules have no talk, and with two players the raise is itself the signal."
    },
    {
      "what": "The Countess is enforced by offering only the 7",
      "why": "The result is the same as 'discarded instead, whatever they chose', and the seat is never offered a move it may not make."
    },
    {
      "what": "rank_by = points * 1000 + hands_won",
      "why": "Points first, hands won as the tie-break; hands won never reaches 1000, and a full tie is a shared win, which is the draw."
    },
    {
      "what": "A 'no raise' does not use up the raise",
      "why": "The rules allow a raise whenever no raise has been made; only an accepted raise (or a concession, which ends the hand) closes it."
    }
  ],
  "simplifications": [
    {
      "what": "The burned bottom card is drawn at random at the start of the hand into a separate hidden 'burned' list, and draws take random cards from 'deck'.",
      "why": "The engine draws at random from a list rather than from an ordered pile; the outcome has the same distribution. The deck count is len(deck) + len(burned)."
    },
    {
      "what": "Effect steps are flat steps each guarded by a condition on last_discard, hand_over and protection",
      "why": "The step list is flat; the per-step conditions reproduce skipping the rest of the turn after a concession."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: points, hands_won; table: turn.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
```json
[
  {"name": "R1: the 16-card deck splits into 3 removed, 2 dealt, 1 burned and 10 drawable when a hand starts (a raise is conceded, so nothing is drawn)",
   "rule": "R1", "players": 2, "seed": 1, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "raise"}, {"seat": 2, "options_include": "concede"}],
   "expect": {"lens": {"game": {"deck": 10, "burned": 1, "removed": 3}, "players": {"1": {"hand": 1}, "2": {"hand": 1}}}}},

  {"name": "R2: hand start deals 1 card each, removes 3, burns 1 and leaves 10 drawable",
   "rule": "R2", "players": 2, "seed": 2, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "raise"}, {"seat": 2, "options_include": "concede"}],
   "expect": {"lens": {"game": {"deck": 10, "burned": 1, "removed": 3}, "players": {"1": {"hand": 1}, "2": {"hand": 1}}},
              "players": {"1": {"points": 1}, "2": {"points": 0}}}},

  {"name": "R3: a new hand resets raised, so seat 1 is offered the raise again",
   "rule": "R3", "players": 2, "seed": 3, "rounds": 1, "default": "decline",
   "given": {"game": {"raised": true, "stake": 2}},
   "rules": [{"seat": 1, "options_include": "raise"}, {"seat": 2, "options_include": "concede"}],
   "expect": {"offered": [{"seat": 1, "option": "raise"}],
              "players": {"1": {"points": 1, "hands_won": 1}, "2": {"points": 0, "hands_won": 0}}}},

  {"name": "R4: seat 1 is active on turn 1 of hand 1",
   "rule": "R4", "players": 2, "seed": 4, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "raise"}, {"seat": 2, "options_include": "concede"}],
   "expect": {"offered": [{"seat": 1, "option": "raise"}, {"seat": 2, "option": "concede"}],
              "not_offered": [{"seat": 2, "option": "no raise"}],
              "players": {"1": {"points": 1}, "2": {"points": 0}},
              "game": {"turn": 1}}},

  {"name": "R5: after seat 1 wins a hand, seat 2 starts the next hand",
   "rule": "R5", "players": 2, "seed": 5, "rounds": 2, "default": "decline",
   "rules": [{"seat": 1, "options_include": "raise", "times": 1}, {"seat": 1, "options_include": "concede"},
             {"seat": 2, "options_include": "concede", "times": 1}, {"seat": 2, "options_include": "raise"}],
   "expect": {"players": {"1": {"points": 1, "hands_won": 1}, "2": {"points": 1, "hands_won": 1}},
              "game": {"turn": 2}}},

  {"name": "R5: after a hand where nobody scored, the seat that did not start it starts the next",
   "rule": "R5", "players": 2, "seed": 6, "rounds": 2, "default": "decline",
   "given": {"players": {"1": {"hand": [1], "discard_sum": 0}, "2": {"hand": [1], "discard_sum": 1}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 1, "raised": true, "deck": [1], "burned": [5]}},
   "rules": [{"seat": 2, "options_include": "raise"}, {"seat": 1, "options_include": "concede"}],
   "expect": {"not_offered": [{"seat": 1, "option": "raise"}],
              "players": {"1": {"points": 0, "hands_won": 0}, "2": {"points": 1, "hands_won": 1}},
              "game": {"turn": 2}}},

  {"name": "R6: when raised is true the active player is not asked to raise",
   "rule": "R6", "players": 2, "seed": 7, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [1]}, "2": {"hand": [3]}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 2, "raised": true, "deck": [1, 1, 1], "burned": [2]}},
   "expect": {"not_offered": [{"seat": 1, "option": "raise"}, {"seat": 1, "option": "no raise"}],
              "players": {"1": {"points": 0}, "2": {"points": 0}},
              "game": {"turn": 1}}},

  {"name": "R6: when no raise has been accepted the active player is offered raise and no raise",
   "rule": "R6", "players": 2, "seed": 8, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [1]}, "2": {"hand": [3]}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 1, "raised": false, "deck": [1, 1, 1], "burned": [2]}},
   "expect": {"offered": [{"seat": 1, "option": "raise"}, {"seat": 1, "option": "no raise"}],
              "players": {"1": {"points": 0}, "2": {"points": 0}}}},

  {"name": "R7: a conceded raise gives the raiser 1 point and 1 hand won, with no draw",
   "rule": "R7", "players": 2, "seed": 9, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "raise"}, {"seat": 2, "options_include": "concede"}],
   "expect": {"players": {"1": {"points": 1, "hands_won": 1}, "2": {"points": 0, "hands_won": 0}},
              "lens": {"game": {"deck": 10}, "players": {"1": {"hand": 1}}},
              "game": {"turn": 1}}},

  {"name": "R8: an accepted raise makes the stake 2, so a Guard elimination pays 2",
   "rule": "R8", "players": 2, "seed": 10, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [1]}, "2": {"hand": [3]}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 1, "raised": false, "deck": [1, 1, 1], "burned": [2]}},
   "rules": [{"seat": 1, "options_include": "raise"}, {"seat": 2, "options_include": "accept"},
             {"seat": 1, "options_include": 3, "answer": 3}],
   "expect": {"players": {"1": {"points": 2, "hands_won": 1}, "2": {"points": 0, "hands_won": 0}}}},

  {"name": "R8: after an accepted raise the opponent is not offered a raise on the next turn",
   "rule": "R8", "players": 2, "seed": 11, "rounds": 2, "default": "decline",
   "given": {"players": {"1": {"hand": [1]}, "2": {"hand": [3]}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 1, "raised": false, "deck": [1, 1, 1], "burned": [2]}},
   "rules": [{"seat": 1, "options_include": "raise"}, {"seat": 2, "options_include": "accept"}],
   "expect": {"not_offered": [{"seat": 2, "option": "raise"}, {"seat": 2, "option": "no raise"}],
              "players": {"1": {"points": 0}, "2": {"points": 0}},
              "game": {"turn": 2}}},

  {"name": "R9: the active player draws 1 card and discards 1, ending with 1 card",
   "rule": "R9", "players": 2, "seed": 12, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [1], "protected": true}, "2": {"hand": [3]}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 1, "raised": true, "deck": [1, 1, 1], "burned": [2]}},
   "expect": {"lens": {"game": {"deck": 2}, "players": {"1": {"hand": 1}, "2": {"hand": 1}}},
              "players": {"1": {"points": 0}, "2": {"points": 0}}}},

  {"name": "R10: holding 7 with 5, only the 7 may be discarded",
   "rule": "R10", "players": 2, "seed": 13, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [7]}, "2": {"hand": [3]}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 1, "raised": true, "deck": [5, 5, 5], "burned": [2]}},
   "rules": [{"seat": 1, "options_include": 5, "answer": 5}],
   "expect": {"offered": [{"seat": 1, "option": 7}],
              "not_offered": [{"seat": 1, "option": 5}],
              "players": {"1": {"points": 0}, "2": {"points": 0}}}},

  {"name": "R11: discarded ranks count in discard_sum, which breaks an equal-card showdown",
   "rule": "R11", "players": 2, "seed": 14, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [1], "discard_sum": 0}, "2": {"hand": [1], "discard_sum": 0}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 1, "raised": false, "deck": [1], "burned": [5]}},
   "expect": {"players": {"1": {"points": 1, "hands_won": 1}, "2": {"points": 0, "hands_won": 0}}}},

  {"name": "R12: a Handmaid protects its owner from the opponent's correct Guard guess",
   "rule": "R12", "players": 2, "seed": 15, "rounds": 2, "default": "decline",
   "given": {"players": {"1": {"hand": [4]}, "2": {"hand": [1]}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 1, "raised": false, "deck": [2, 2, 2], "burned": [5]}},
   "rules": [{"seat": 1, "options_include": 4, "answer": 4},
             {"seat": 2, "options_include": 1, "answer": 1, "times": 1},
             {"seat": 2, "options_include": 2, "answer": 2}],
   "expect": {"players": {"1": {"points": 0, "hands_won": 0}, "2": {"points": 0, "hands_won": 0}},
              "game": {"turn": 2}}},

  {"name": "R13: discarding the Princess by choice eliminates you and the opponent scores",
   "rule": "R13", "players": 2, "seed": 16, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [8]}, "2": {"hand": [3]}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 1, "raised": true, "deck": [1, 1, 1], "burned": [2]}},
   "rules": [{"seat": 1, "options_include": 8, "answer": 8}],
   "expect": {"players": {"1": {"points": 0, "hands_won": 0}, "2": {"points": 1, "hands_won": 1}}}},

  {"name": "R13: a Prince forcing the Princess discard eliminates its holder",
   "rule": "R13", "players": 2, "seed": 17, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [5]}, "2": {"hand": [8]}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 1, "raised": true, "deck": [5, 5, 5], "burned": [2]}},
   "rules": [{"seat": 1, "options_include": "opponent"}],
   "expect": {"players": {"1": {"points": 1, "hands_won": 1}, "2": {"points": 0, "hands_won": 0}}}},

  {"name": "R14: a correct Guard guess eliminates the unprotected opponent",
   "rule": "R14", "players": 2, "seed": 18, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [1]}, "2": {"hand": [6]}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 1, "raised": true, "deck": [1, 1, 1], "burned": [2]}},
   "rules": [{"seat": 1, "options_include": 6, "answer": 6}],
   "expect": {"players": {"1": {"points": 1, "hands_won": 1}, "2": {"points": 0, "hands_won": 0}}}},

  {"name": "R15: a Priest only shows a card and changes no score",
   "rule": "R15", "players": 2, "seed": 19, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [2]}, "2": {"hand": [3]}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 1, "raised": true, "deck": [2, 2, 2], "burned": [1]}},
   "expect": {"players": {"1": {"points": 0, "hands_won": 0}, "2": {"points": 0, "hands_won": 0}},
              "game": {"turn": 1}}},

  {"name": "R16: a Baron eliminates the lower card",
   "rule": "R16", "players": 2, "seed": 20, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [3]}, "2": {"hand": [2]}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 1, "raised": true, "deck": [7, 7, 7], "burned": [1]}},
   "rules": [{"seat": 1, "options_include": 3, "answer": 3}],
   "expect": {"players": {"1": {"points": 1, "hands_won": 1}, "2": {"points": 0, "hands_won": 0}}}},

  {"name": "R16: a Baron with equal cards does nothing",
   "rule": "R16", "players": 2, "seed": 21, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [3]}, "2": {"hand": [4]}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 1, "raised": true, "deck": [4, 4, 4], "burned": [1]}},
   "rules": [{"seat": 1, "options_include": 3, "answer": 3}],
   "expect": {"players": {"1": {"points": 0}, "2": {"points": 0}}}},

  {"name": "R17: a Prince on self with an empty deck draws the burned card, which then wins the showdown",
   "rule": "R17", "players": 2, "seed": 22, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [5]}, "2": {"hand": [7]}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 1, "raised": true, "deck": [1], "burned": [8]}},
   "rules": [{"seat": 1, "options_include": 5, "answer": 5}, {"seat": 1, "options_include": "self"}],
   "expect": {"players": {"1": {"points": 1, "hands_won": 1}, "2": {"points": 0, "hands_won": 0}}}},

  {"name": "R17: a Prince cannot target a protected opponent",
   "rule": "R17", "players": 2, "seed": 23, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [5]}, "2": {"hand": [3], "protected": true}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 1, "raised": true, "deck": [1, 1, 1], "burned": [2]}},
   "rules": [{"seat": 1, "options_include": 5, "answer": 5}],
   "expect": {"offered": [{"seat": 1, "option": "self"}],
              "not_offered": [{"seat": 1, "option": "opponent"}],
              "players": {"1": {"points": 0}, "2": {"points": 0}}}},

  {"name": "R18: a King swaps the cards, so the swapped 7 wins the showdown",
   "rule": "R18", "players": 2, "seed": 24, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [6]}, "2": {"hand": [7]}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 1, "raised": true, "deck": [1], "burned": [2]}},
   "rules": [{"seat": 1, "options_include": 6, "answer": 6}],
   "expect": {"players": {"1": {"points": 1, "hands_won": 1}, "2": {"points": 0, "hands_won": 0}}}},

  {"name": "R19: a King against a protected opponent has no effect",
   "rule": "R19", "players": 2, "seed": 25, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [6]}, "2": {"hand": [7], "protected": true}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 1, "raised": true, "deck": [1], "burned": [2]}},
   "rules": [{"seat": 1, "options_include": 6, "answer": 6}],
   "expect": {"players": {"1": {"points": 0, "hands_won": 0}, "2": {"points": 1, "hands_won": 1}}}},

  {"name": "R20: an elimination at stake 2 gives the other player 2 points and 1 hand won",
   "rule": "R20", "players": 2, "seed": 26, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [1], "points": 1, "hands_won": 1}, "2": {"hand": [6]}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 2, "raised": true, "deck": [1, 1, 1], "burned": [2]}},
   "rules": [{"seat": 1, "options_include": 6, "answer": 6}],
   "expect": {"players": {"1": {"points": 3, "hands_won": 2}, "2": {"points": 0, "hands_won": 0}}}},

  {"name": "R21: at the showdown the higher card gains the stake",
   "rule": "R21", "players": 2, "seed": 27, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [2]}, "2": {"hand": [6]}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 2, "raised": true, "deck": [2], "burned": [3]}},
   "expect": {"players": {"1": {"points": 0, "hands_won": 0}, "2": {"points": 2, "hands_won": 1}}}},

  {"name": "R22: reaching 5 points ends the match with that player winning",
   "rule": "R22", "players": 2, "seed": 28, "default": "decline",
   "given": {"players": {"1": {"points": 4, "hands_won": 4}, "2": {"points": 3, "hands_won": 3}}},
   "rules": [{"seat": 1, "options_include": "raise"}, {"seat": 2, "options_include": "concede"}],
   "expect": {"winner": 1, "standings": {"1": 5005, "2": 3003},
              "players": {"1": {"points": 5, "hands_won": 5}, "2": {"points": 3, "hands_won": 3}},
              "game": {"turn": 1}}},

  {"name": "R23: at turn 40 with level points, more hands won wins",
   "rule": "R23", "players": 2, "seed": 29, "default": "decline",
   "given": {"players": {"1": {"hand": [1], "points": 2, "hands_won": 3}, "2": {"hand": [3], "points": 2, "hands_won": 2}},
             "game": {"turn": 39, "new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 1, "raised": true, "deck": [1, 1, 1], "burned": [2]}},
   "expect": {"winner": 1, "standings": {"1": 2003, "2": 2002}, "game": {"turn": 40}}},

  {"name": "R23: at turn 40 with level points and hands won, both share the win",
   "rule": "R23", "players": 2, "seed": 30, "default": "decline",
   "given": {"players": {"1": {"hand": [1], "points": 2, "hands_won": 2}, "2": {"hand": [3], "points": 2, "hands_won": 2}},
             "game": {"turn": 39, "new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 1, "raised": true, "deck": [1, 1, 1], "burned": [2]}},
   "expect": {"winner": [1, 2], "standings": {"1": 2002, "2": 2002}, "game": {"turn": 40}}},

  {"name": "R24: when the hand goes on, the other seat is active next turn",
   "rule": "R24", "players": 2, "seed": 31, "rounds": 2, "default": "decline",
   "given": {"players": {"1": {"hand": [1]}, "2": {"hand": [3]}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 1, "raised": false, "deck": [1, 1, 1, 1], "burned": [2]}},
   "rules": [{"seat": 2, "options_include": "raise"}, {"seat": 1, "options_include": "concede"}],
   "expect": {"offered": [{"seat": 2, "option": "raise"}],
              "players": {"1": {"points": 0, "hands_won": 0}, "2": {"points": 1, "hands_won": 1}},
              "game": {"turn": 2}}}
]
```

Why it was refused: scenario 7: needs `rules` (what each seat answers, by option name); scenario 8: needs `rules` (what each seat answers, by option name); scenario 12: needs `rules` (what each seat answers, by option name); scenario 14: needs `rules` (what each seat answers, by option name); scenario 19: needs `rules` (what each seat answers, by option name); scenario 27: needs `rules` (what each seat answers, by option name); scenario 29: needs `rules` (what each seat answers, by option name); scenario 30: needs `rules` (what each seat answers, by option name)
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
[
  {"name": "R1: the 16-card deck splits into 3 removed, 2 dealt, 1 burned and 10 drawable when a hand starts (a raise is conceded, so nothing is drawn)",
   "rule": "R1", "players": 2, "seed": 1, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "raise"}, {"seat": 2, "options_include": "concede"}],
   "expect": {"lens": {"game": {"deck": 10, "burned": 1, "removed": 3}, "players": {"1": {"hand": 1}, "2": {"hand": 1}}}}},

  {"name": "R2: hand start deals 1 card each, removes 3, burns 1 and leaves 10 drawable",
   "rule": "R2", "players": 2, "seed": 2, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "raise"}, {"seat": 2, "options_include": "concede"}],
   "expect": {"lens": {"game": {"deck": 10, "burned": 1, "removed": 3}, "players": {"1": {"hand": 1}, "2": {"hand": 1}}},
              "players": {"1": {"points": 1}, "2": {"points": 0}}}},

  {"name": "R3: a new hand resets raised, so seat 1 is offered the raise again",
   "rule": "R3", "players": 2, "seed": 3, "rounds": 1, "default": "decline",
   "given": {"game": {"raised": true, "stake": 2}},
   "rules": [{"seat": 1, "options_include": "raise"}, {"seat": 2, "options_include": "concede"}],
   "expect": {"offered": [{"seat": 1, "option": "raise"}],
              "players": {"1": {"points": 1, "hands_won": 1}, "2": {"points": 0, "hands_won": 0}}}},

  {"name": "R4: seat 1 is active on turn 1 of hand 1",
   "rule": "R4", "players": 2, "seed": 4, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "raise"}, {"seat": 2, "options_include": "concede"}],
   "expect": {"offered": [{"seat": 1, "option": "raise"}, {"seat": 2, "option": "concede"}],
              "not_offered": [{"seat": 2, "option": "no raise"}],
              "players": {"1": {"points": 1}, "2": {"points": 0}},
              "game": {"turn": 1}}},

  {"name": "R5: after seat 1 wins a hand, seat 2 starts the next hand",
   "rule": "R5", "players": 2, "seed": 5, "rounds": 2, "default": "decline",
   "rules": [{"seat": 1, "options_include": "raise", "times": 1}, {"seat": 1, "options_include": "concede"},
             {"seat": 2, "options_include": "concede", "times": 1}, {"seat": 2, "options_include": "raise"}],
   "expect": {"players": {"1": {"points": 1, "hands_won": 1}, "2": {"points": 1, "hands_won": 1}},
              "game": {"turn": 2}}},

  {"name": "R5: after a hand where nobody scored, the seat that did not start it starts the next",
   "rule": "R5", "players": 2, "seed": 6, "rounds": 2, "default": "decline",
   "given": {"players": {"1": {"hand": [1], "discard_sum": 0}, "2": {"hand": [1], "discard_sum": 1}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 1, "raised": true, "deck": [1], "burned": [5]}},
   "rules": [{"seat": 2, "options_include": "raise"}, {"seat": 1, "options_include": "concede"}],
   "expect": {"not_offered": [{"seat": 1, "option": "raise"}],
              "players": {"1": {"points": 0, "hands_won": 0}, "2": {"points": 1, "hands_won": 1}},
              "game": {"turn": 2}}},

  {"name": "R6: when raised is true the active player is not asked to raise",
   "rule": "R6", "players": 2, "seed": 7, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [1]}, "2": {"hand": [3]}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 2, "raised": true, "deck": [1, 1, 1], "burned": [2]}},
   "rules": [{"seat": 1, "options_include": 1, "answer": 1}, {"seat": 1, "options_include": 2, "answer": 2}],
   "expect": {"not_offered": [{"seat": 1, "option": "raise"}, {"seat": 1, "option": "no raise"}],
              "players": {"1": {"points": 0}, "2": {"points": 0}},
              "game": {"turn": 1}}},

  {"name": "R6: when no raise has been accepted the active player is offered raise and no raise",
   "rule": "R6", "players": 2, "seed": 8, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [1]}, "2": {"hand": [3]}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 1, "raised": false, "deck": [1, 1, 1], "burned": [2]}},
   "rules": [{"seat": 1, "options_include": "no raise"}, {"seat": 1, "options_include": 1, "answer": 1}, {"seat": 1, "options_include": 2, "answer": 2}],
   "expect": {"offered": [{"seat": 1, "option": "raise"}, {"seat": 1, "option": "no raise"}],
              "players": {"1": {"points": 0}, "2": {"points": 0}}}},

  {"name": "R7: a conceded raise gives the raiser 1 point and 1 hand won, with no draw",
   "rule": "R7", "players": 2, "seed": 9, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "raise"}, {"seat": 2, "options_include": "concede"}],
   "expect": {"players": {"1": {"points": 1, "hands_won": 1}, "2": {"points": 0, "hands_won": 0}},
              "lens": {"game": {"deck": 10}, "players": {"1": {"hand": 1}}},
              "game": {"turn": 1}}},

  {"name": "R8: an accepted raise makes the stake 2, so a Guard elimination pays 2",
   "rule": "R8", "players": 2, "seed": 10, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [1]}, "2": {"hand": [3]}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 1, "raised": false, "deck": [1, 1, 1], "burned": [2]}},
   "rules": [{"seat": 1, "options_include": "raise"}, {"seat": 2, "options_include": "accept"},
             {"seat": 1, "options_include": 3, "answer": 3}],
   "expect": {"players": {"1": {"points": 2, "hands_won": 1}, "2": {"points": 0, "hands_won": 0}}}},

  {"name": "R8: after an accepted raise the opponent is not offered a raise on the next turn",
   "rule": "R8", "players": 2, "seed": 11, "rounds": 2, "default": "decline",
   "given": {"players": {"1": {"hand": [1]}, "2": {"hand": [3]}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 1, "raised": false, "deck": [1, 1, 1], "burned": [2]}},
   "rules": [{"seat": 1, "options_include": "raise"}, {"seat": 2, "options_include": "accept"}],
   "expect": {"not_offered": [{"seat": 2, "option": "raise"}, {"seat": 2, "option": "no raise"}],
              "players": {"1": {"points": 0}, "2": {"points": 0}},
              "game": {"turn": 2}}},

  {"name": "R9: the active player draws 1 card and discards 1, ending with 1 card",
   "rule": "R9", "players": 2, "seed": 12, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [1], "protected": true}, "2": {"hand": [3]}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 1, "raised": true, "deck": [1, 1, 1], "burned": [2]}},
   "rules": [{"seat": 1, "options_include": 1, "answer": 1}, {"seat": 1, "options_include": 2, "answer": 2}],
   "expect": {"lens": {"game": {"deck": 2}, "players": {"1": {"hand": 1}, "2": {"hand": 1}}},
              "players": {"1": {"points": 0}, "2": {"points": 0}}}},

  {"name": "R10: holding 7 with 5, only the 7 may be discarded",
   "rule": "R10", "players": 2, "seed": 13, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [7]}, "2": {"hand": [3]}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 1, "raised": true, "deck": [5, 5, 5], "burned": [2]}},
   "rules": [{"seat": 1, "options_include": 5, "answer": 5}],
   "expect": {"offered": [{"seat": 1, "option": 7}],
              "not_offered": [{"seat": 1, "option": 5}],
              "players": {"1": {"points": 0}, "2": {"points": 0}}}},

  {"name": "R11: discarded ranks count in discard_sum, which breaks an equal-card showdown",
   "rule": "R11", "players": 2, "seed": 14, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [1], "discard_sum": 0}, "2": {"hand": [1], "discard_sum": 0}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 1, "raised": false, "deck": [1], "burned": [5]}},
   "rules": [{"seat": 1, "options_include": "no raise"}, {"seat": 1, "options_include": 1, "answer": 1}, {"seat": 1, "options_include": 2, "answer": 2}],
   "expect": {"players": {"1": {"points": 1, "hands_won": 1}, "2": {"points": 0, "hands_won": 0}}}},

  {"name": "R12: a Handmaid protects its owner from the opponent's correct Guard guess",
   "rule": "R12", "players": 2, "seed": 15, "rounds": 2, "default": "decline",
   "given": {"players": {"1": {"hand": [4]}, "2": {"hand": [1]}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 1, "raised": false, "deck": [2, 2, 2], "burned": [5]}},
   "rules": [{"seat": 1, "options_include": 4, "answer": 4},
             {"seat": 2, "options_include": 1, "answer": 1, "times": 1},
             {"seat": 2, "options_include": 2, "answer": 2}],
   "expect": {"players": {"1": {"points": 0, "hands_won": 0}, "2": {"points": 0, "hands_won": 0}},
              "game": {"turn": 2}}},

  {"name": "R13: discarding the Princess by choice eliminates you and the opponent scores",
   "rule": "R13", "players": 2, "seed": 16, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [8]}, "2": {"hand": [3]}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 1, "raised": true, "deck": [1, 1, 1], "burned": [2]}},
   "rules": [{"seat": 1, "options_include": 8, "answer": 8}],
   "expect": {"players": {"1": {"points": 0, "hands_won": 0}, "2": {"points": 1, "hands_won": 1}}}},

  {"name": "R13: a Prince forcing the Princess discard eliminates its holder",
   "rule": "R13", "players": 2, "seed": 17, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [5]}, "2": {"hand": [8]}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 1, "raised": true, "deck": [5, 5, 5], "burned": [2]}},
   "rules": [{"seat": 1, "options_include": "opponent"}],
   "expect": {"players": {"1": {"points": 1, "hands_won": 1}, "2": {"points": 0, "hands_won": 0}}}},

  {"name": "R14: a correct Guard guess eliminates the unprotected opponent",
   "rule": "R14", "players": 2, "seed": 18, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [1]}, "2": {"hand": [6]}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 1, "raised": true, "deck": [1, 1, 1], "burned": [2]}},
   "rules": [{"seat": 1, "options_include": 6, "answer": 6}],
   "expect": {"players": {"1": {"points": 1, "hands_won": 1}, "2": {"points": 0, "hands_won": 0}}}},

  {"name": "R15: a Priest only shows a card and changes no score",
   "rule": "R15", "players": 2, "seed": 19, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [2]}, "2": {"hand": [3]}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 1, "raised": true, "deck": [2, 2, 2], "burned": [1]}},
   "rules": [{"seat": 1, "options_include": 2, "answer": 2}],
   "expect": {"players": {"1": {"points": 0, "hands_won": 0}, "2": {"points": 0, "hands_won": 0}},
              "game": {"turn": 1}}},

  {"name": "R16: a Baron eliminates the lower card",
   "rule": "R16", "players": 2, "seed": 20, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [3]}, "2": {"hand": [2]}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 1, "raised": true, "deck": [7, 7, 7], "burned": [1]}},
   "rules": [{"seat": 1, "options_include": 3, "answer": 3}],
   "expect": {"players": {"1": {"points": 1, "hands_won": 1}, "2": {"points": 0, "hands_won": 0}}}},

  {"name": "R16: a Baron with equal cards does nothing",
   "rule": "R16", "players": 2, "seed": 21, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [3]}, "2": {"hand": [4]}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 1, "raised": true, "deck": [4, 4, 4], "burned": [1]}},
   "rules": [{"seat": 1, "options_include": 3, "answer": 3}],
   "expect": {"players": {"1": {"points": 0}, "2": {"points": 0}}}},

  {"name": "R17: a Prince on self with an empty deck draws the burned card, which then wins the showdown",
   "rule": "R17", "players": 2, "seed": 22, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [5]}, "2": {"hand": [7]}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 1, "raised": true, "deck": [1], "burned": [8]}},
   "rules": [{"seat": 1, "options_include": 5, "answer": 5}, {"seat": 1, "options_include": "self"}],
   "expect": {"players": {"1": {"points": 1, "hands_won": 1}, "2": {"points": 0, "hands_won": 0}}}},

  {"name": "R17: a Prince cannot target a protected opponent",
   "rule": "R17", "players": 2, "seed": 23, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [5]}, "2": {"hand": [3], "protected": true}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 1, "raised": true, "deck": [1, 1, 1], "burned": [2]}},
   "rules": [{"seat": 1, "options_include": 5, "answer": 5}],
   "expect": {"offered": [{"seat": 1, "option": "self"}],
              "not_offered": [{"seat": 1, "option": "opponent"}],
              "players": {"1": {"points": 0}, "2": {"points": 0}}}},

  {"name": "R18: a King swaps the cards, so the swapped 7 wins the showdown",
   "rule": "R18", "players": 2, "seed": 24, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [6]}, "2": {"hand": [7]}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 1, "raised": true, "deck": [1], "burned": [2]}},
   "rules": [{"seat": 1, "options_include": 6, "answer": 6}],
   "expect": {"players": {"1": {"points": 1, "hands_won": 1}, "2": {"points": 0, "hands_won": 0}}}},

  {"name": "R19: a King against a protected opponent has no effect",
   "rule": "R19", "players": 2, "seed": 25, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [6]}, "2": {"hand": [7], "protected": true}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 1, "raised": true, "deck": [1], "burned": [2]}},
   "rules": [{"seat": 1, "options_include": 6, "answer": 6}],
   "expect": {"players": {"1": {"points": 0, "hands_won": 0}, "2": {"points": 1, "hands_won": 1}}}},

  {"name": "R20: an elimination at stake 2 gives the other player 2 points and 1 hand won",
   "rule": "R20", "players": 2, "seed": 26, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [1], "points": 1, "hands_won": 1}, "2": {"hand": [6]}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 2, "raised": true, "deck": [1, 1, 1], "burned": [2]}},
   "rules": [{"seat": 1, "options_include": 6, "answer": 6}],
   "expect": {"players": {"1": {"points": 3, "hands_won": 2}, "2": {"points": 0, "hands_won": 0}}}},

  {"name": "R21: at the showdown the higher card gains the stake",
   "rule": "R21", "players": 2, "seed": 27, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [2]}, "2": {"hand": [6]}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 2, "raised": true, "deck": [2], "burned": [3]}},
   "rules": [{"seat": 1, "options_include": 2, "answer": 2}],
   "expect": {"players": {"1": {"points": 0, "hands_won": 0}, "2": {"points": 2, "hands_won": 1}}}},

  {"name": "R22: reaching 5 points ends the match with that player winning",
   "rule": "R22", "players": 2, "seed": 28, "default": "decline",
   "given": {"players": {"1": {"points": 4, "hands_won": 4}, "2": {"points": 3, "hands_won": 3}}},
   "rules": [{"seat": 1, "options_include": "raise"}, {"seat": 2, "options_include": "concede"}],
   "expect": {"winner": 1, "standings": {"1": 5005, "2": 3003},
              "players": {"1": {"points": 5, "hands_won": 5}, "2": {"points": 3, "hands_won": 3}},
              "game": {"turn": 1}}},

  {"name": "R23: at turn 40 with level points, more hands won wins",
   "rule": "R23", "players": 2, "seed": 29, "default": "decline",
   "given": {"players": {"1": {"hand": [1], "points": 2, "hands_won": 3}, "2": {"hand": [3], "points": 2, "hands_won": 2}},
             "game": {"turn": 39, "new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 1, "raised": true, "deck": [1, 1, 1], "burned": [2]}},
   "rules": [{"seat": 1, "options_include": 1, "answer": 1}, {"seat": 1, "options_include": 2, "answer": 2}],
   "expect": {"winner": 1, "standings": {"1": 2003, "2": 2002}, "game": {"turn": 40}}},

  {"name": "R23: at turn 40 with level points and hands won, both share the win",
   "rule": "R23", "players": 2, "seed": 30, "default": "decline",
   "given": {"players": {"1": {"hand": [1], "points": 2, "hands_won": 2}, "2": {"hand": [3], "points": 2, "hands_won": 2}},
             "game": {"turn": 39, "new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 1, "raised": true, "deck": [1, 1, 1], "burned": [2]}},
   "rules": [{"seat": 1, "options_include": 1, "answer": 1}, {"seat": 1, "options_include": 2, "answer": 2}],
   "expect": {"winner": [1, 2], "standings": {"1": 2002, "2": 2002}, "game": {"turn": 40}}},

  {"name": "R24: when the hand goes on, the other seat is active next turn",
   "rule": "R24", "players": 2, "seed": 31, "rounds": 2, "default": "decline",
   "given": {"players": {"1": {"hand": [1]}, "2": {"hand": [3]}},
             "game": {"new_hand_due": false, "active_seat": 1, "starter_seat": 1, "stake": 1, "raised": false, "deck": [1, 1, 1, 1], "burned": [2]}},
   "rules": [{"seat": 2, "options_include": "raise"}, {"seat": 1, "options_include": "concede"}],
   "expect": {"offered": [{"seat": 2, "option": "raise"}],
              "players": {"1": {"points": 0, "hands_won": 0}, "2": {"points": 1, "hands_won": 1}},
              "game": {"turn": 2}}}
]
```
````
