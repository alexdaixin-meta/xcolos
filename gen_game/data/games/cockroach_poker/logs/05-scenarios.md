# 05 scenarios

- time: 2026-10-28T06:04:14+00:00 (38.8s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 4fc16ad71711eb74, reply sha256 91d73e7e66589d97

## Sent

````
SPEC:
{
  "name": "Roach Bluff",
  "summary": "A bluffing game in which players pass face-down creature cards with true or false claims; whoever ends up with three face-up cards of one creature, or has no card to send, loses.",
  "players": {
    "min": 3,
    "max": 4,
    "suggested": 4
  },
  "parameters": {
    "deck_size": 24,
    "cards_per_creature": 6,
    "creature_kinds": 4,
    "hand_size_4_players": 6,
    "hand_size_3_players": 8,
    "lose_at_faceup_of_one_creature": 3,
    "max_rounds": 24,
    "first_sender_seat": 1,
    "loser_rank_penalty": 1000
  },
  "attributes": {
    "player": [
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "The cards held face-down in this player's private hand.",
        "observable": false
      },
      {
        "key": "hand_size",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The number of cards in this player's hand.",
        "observable": true
      },
      {
        "key": "roach_up",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The number of face-up Roach cards in this player's pile.",
        "observable": true
      },
      {
        "key": "rat_up",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The number of face-up Rat cards in this player's pile.",
        "observable": true
      },
      {
        "key": "fly_up",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The number of face-up Fly cards in this player's pile.",
        "observable": true
      },
      {
        "key": "toad_up",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The number of face-up Toad cards in this player's pile.",
        "observable": true
      },
      {
        "key": "faceup_total",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The total number of face-up cards in this player's pile. This is the score, and fewer is better.",
        "observable": true
      },
      {
        "key": "lost",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "True if this player triggered the end of the game and loses.",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [
          "Roach x6",
          "Rat x6",
          "Fly x6",
          "Toad x6"
        ],
        "meaning": "The 24-card deck before dealing: 6 each of Roach, Rat, Fly and Toad.",
        "observable": false
      },
      {
        "key": "card_in_play",
        "type": "text",
        "visible": "none",
        "initial": "",
        "meaning": "The identity of the card currently being sent. It is hidden until resolution.",
        "observable": false
      },
      {
        "key": "sender",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "The seat of the current sender.",
        "observable": false
      },
      {
        "key": "receiver",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The seat of the current receiver, who is the judge when the card resolves.",
        "observable": false
      },
      {
        "key": "passer",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The seat that passed this round, or 0 if nobody passed.",
        "observable": false
      },
      {
        "key": "claimer",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The seat that made the latest claim.",
        "observable": false
      },
      {
        "key": "claim",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The latest declared creature.",
        "observable": false
      },
      {
        "key": "response",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The latest receiver answer: TRUE, FALSE or PASS.",
        "observable": false
      },
      {
        "key": "passed",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "True if the first receiver passed this round.",
        "observable": false
      },
      {
        "key": "taker",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The seat that took the card face-up this round.",
        "observable": false
      },
      {
        "key": "last_revealed",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The identity of the card revealed at the last resolution.",
        "observable": true
      },
      {
        "key": "round_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The number of rounds completed.",
        "observable": false
      },
      {
        "key": "game_over",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "True once a player has lost.",
        "observable": false
      }
    ]
  },
  "setup": [
    "Build the deck list with 24 cards: 6 Roach, 6 Rat, 6 Fly and 6 Toad.",
    "Deal the whole deck at random into the players' hand lists: 6 cards each with 4 players, or 8 cards each with 3 players. Draw each card at random from deck and remove it from deck.",
    "Set each player's hand_size to the number of cards dealt to them.",
    "Set all face-up counts, faceup_total and lost to 0 or false.",
    "Set sender to seat 1.",
    "Sync each player so they see their own hand."
  ],
  "round": [
    {
      "action": "update",
      "who": "engine",
      "answer": null,
      "effect": "Set passer=0, passed=false, response='', claim='', card_in_play=''."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce every player's roach_up, rat_up, fly_up, toad_up, faceup_total and hand_size."
    },
    {
      "action": "ask",
      "who": "seat {sender}",
      "answer": "one card from your own hand list",
      "effect": "card_in_play = the chosen card; remove that card from the sender's hand; sender's hand_size -= 1. The answer is shown only to the sender."
    },
    {
      "action": "ask",
      "who": "seat {sender}",
      "answer": "one of Roach, Rat, Fly, Toad",
      "effect": "claim = the answer; claimer = sender."
    },
    {
      "action": "ask",
      "who": "seat {sender}",
      "answer": "any seat other than the sender",
      "effect": "receiver = the chosen seat."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce: 'Seat {sender} sends a card to seat {receiver}, claiming it is a {claim}.'"
    },
    {
      "action": "ask",
      "who": "seat {receiver}",
      "answer": "TRUE, FALSE or PASS",
      "effect": "response = the answer, announced to all. If the answer is PASS: passed = true, passer = receiver, claimer = receiver."
    },
    {
      "action": "tell",
      "who": "seat {passer} (when passed)",
      "answer": null,
      "effect": "Privately show card_in_play to the passer."
    },
    {
      "action": "ask",
      "who": "seat {passer} (when passed)",
      "answer": "one of Roach, Rat, Fly, Toad",
      "effect": "claim = the answer."
    },
    {
      "action": "ask",
      "who": "seat {passer} (when passed)",
      "answer": "any seat that is neither the sender nor the passer",
      "effect": "receiver = the chosen seat."
    },
    {
      "action": "tell",
      "who": "all players (when passed)",
      "answer": null,
      "effect": "Announce: 'Seat {passer} passes the card to seat {receiver}, claiming it is a {claim}.'"
    },
    {
      "action": "ask",
      "who": "seat {receiver} (when passed)",
      "answer": "TRUE or FALSE",
      "effect": "response = the answer, announced to all."
    },
    {
      "action": "update",
      "who": "engine",
      "answer": null,
      "effect": "correct = (response=='TRUE' and card_in_play==claim) or (response=='FALSE' and card_in_play!=claim). taker = claimer if correct, else receiver. Add 1 to the taker's count for the card_in_play creature (roach_up, rat_up, fly_up or toad_up). Add 1 to the taker's faceup_total. last_revealed = card_in_play. sender = taker. round_count += 1."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce: 'The card was a {last_revealed}. Seat {taker} takes it face-up and sends next.'"
    },
    {
      "action": "update",
      "who": "engine",
      "answer": null,
      "effect": "If the taker has roach_up>=3 or rat_up>=3 or fly_up>=3 or toad_up>=3: taker.lost = true and game_over = true. Otherwise, if the sender's hand_size == 0: that player's lost = true and game_over = true."
    },
    {
      "action": "check",
      "who": "engine",
      "answer": null,
      "effect": "End the game if game_over == true or round_count >= 24. Otherwise continue."
    }
  ],
  "ending": {
    "condition": "game_over == true or round_count >= 24",
    "rank_by": "0 - you.faceup_total - 1000 * you.lost",
    "decided_by": "The player who triggered the end (three face-up cards of one creature, or no card to send) loses. Among the others, the player with the fewest total face-up cards wins. Players tied for fewest share the win, which stands for the source's draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game starts with 4 players, then each player holds 6 cards; with 3 players, each holds 8 cards; the 24-card deck has 6 each of Roach, Rat, Fly and Toad, and all of it is dealt."
    },
    {
      "id": "R2",
      "text": "When the game starts, then seat 1 is the first sender and every face-up count is 0."
    },
    {
      "id": "R3",
      "text": "When the sender sends a card, then that card leaves their hand and their hand_size drops by 1."
    },
    {
      "id": "R4",
      "text": "When the sender sends, then they declare one of Roach, Rat, Fly or Toad, which may be false, and choose a receiver who is not themselves."
    },
    {
      "id": "R5",
      "text": "When a claim is made, then the claim and the receiver are announced to all, but the card's identity is not."
    },
    {
      "id": "R6",
      "text": "When the receiver answers TRUE or FALSE, then the card resolves against the sender's claim."
    },
    {
      "id": "R7",
      "text": "When the receiver answers PASS, then they privately see the card, make a new claim, and choose a new receiver who is neither the original sender nor themselves."
    },
    {
      "id": "R8",
      "text": "When a card has been passed once, then the final receiver may answer only TRUE or FALSE."
    },
    {
      "id": "R9",
      "text": "When the judge says TRUE and the card matches the latest claim, or says FALSE and it does not, then the claimer takes the card face-up."
    },
    {
      "id": "R10",
      "text": "When the judge's call is wrong, then the judge takes the card face-up."
    },
    {
      "id": "R11",
      "text": "When a card resolves, then its identity is revealed to all, the taker's count for that creature and faceup_total each rise by 1, and the taker becomes the next sender."
    },
    {
      "id": "R12",
      "text": "When a player reaches 3 face-up cards of one creature, then that player loses and the game ends."
    },
    {
      "id": "R13",
      "text": "When the next sender has 0 cards in hand and nobody has 3 of one creature, then the next sender loses and the game ends."
    },
    {
      "id": "R14",
      "text": "When the game ends, then among the players who did not lose, the one with the fewest face-up cards wins, and players tied for fewest share the result."
    },
    {
      "id": "R15",
      "text": "When 24 rounds have been played, then the game ends."
    }
  ],
  "offers": [
    {
      "question": "Send: which card",
      "who": "the sender",
      "options": "Any card in the sender's own hand list."
    },
    {
      "question": "Send or pass: the claimed creature",
      "who": "the sender, or the passer",
      "options": "Roach, Rat, Fly, Toad."
    },
    {
      "question": "Send: the receiver",
      "who": "the sender",
      "options": "Every seat except the sender."
    },
    {
      "question": "Respond",
      "who": "the first receiver",
      "options": "TRUE, FALSE, PASS."
    },
    {
      "question": "Pass: the new receiver",
      "who": "the passer",
      "options": "Every seat except the original sender and the passer. With 3 players there is exactly one such seat."
    },
    {
      "question": "Final respond",
      "who": "the receiver after a pass",
      "options": "TRUE, FALSE."
    }
  ],
  "choices": [
    {
      "what": "3 to 4 players, suggested 4",
      "why": "The designer set 4 as the suggested size. At least 3 players are needed so that a pass can reach someone who is neither the sender nor the passer. The deck of 24 only deals evenly to 3 or 4 players, so the maximum is 4."
    },
    {
      "what": "No talk step",
      "why": "The rules forbid table talk; the claims are the only communication. Players reason by reading the face-up piles and by bluffing with claims that target a near-loser."
    },
    {
      "what": "Rank expression 0 - faceup_total - 1000*lost",
      "why": "This makes the loser rank below everyone, and among the rest the fewest face-up cards ranks highest."
    },
    {
      "what": "Pass steps run as individual steps with a 'when passed' condition",
      "why": "Each pass step is a single step with an arithmetic condition, not a chosen block, so the engine supports it directly."
    }
  ],
  "simplifications": [
    {
      "what": "A tie for fewest face-up cards is a shared win rather than a draw",
      "why": "The engine has no separate draw outcome; players level at the top share the win."
    },
    {
      "what": "Sending is split into three questions: the card, then the claim, then the receiver",
      "why": "Each engine question takes a single answer. The card choice is kept private to the sender."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: hand_size, roach_up, rat_up, fly_up, toad_up, faceup_total, lost; table: last_revealed.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
```json
[
  {"name": "4 players: each seat is dealt 6 cards and the whole deck is dealt", "rule": "R1", "players": 4, "seed": 1, "rounds": 0,
   "expect": {"lens": {"game": {"deck": 0}, "players": {"1": {"hand": 6}, "2": {"hand": 6}, "3": {"hand": 6}, "4": {"hand": 6}}},
              "players": {"1": {"hand_size": 6}, "2": {"hand_size": 6}, "3": {"hand_size": 6}, "4": {"hand_size": 6}}}},
  {"name": "3 players: each seat is dealt 8 cards and the whole deck is dealt", "rule": "R1", "players": 3, "seed": 2, "rounds": 0,
   "expect": {"lens": {"game": {"deck": 0}, "players": {"1": {"hand": 8}, "2": {"hand": 8}, "3": {"hand": 8}}},
              "players": {"1": {"hand_size": 8}, "2": {"hand_size": 8}, "3": {"hand_size": 8}}}},
  {"name": "At start every face-up count is 0", "rule": "R2", "players": 4, "seed": 3, "rounds": 0,
   "expect": {"players": {
     "1": {"roach_up": 0, "rat_up": 0, "fly_up": 0, "toad_up": 0, "faceup_total": 0, "lost": false},
     "2": {"roach_up": 0, "rat_up": 0, "fly_up": 0, "toad_up": 0, "faceup_total": 0, "lost": false},
     "3": {"roach_up": 0, "rat_up": 0, "fly_up": 0, "toad_up": 0, "faceup_total": 0, "lost": false},
     "4": {"roach_up": 0, "rat_up": 0, "fly_up": 0, "toad_up": 0, "faceup_total": 0, "lost": false}}}},
  {"name": "Seat 1 sends first: only seat 1's hand shrinks in round 1 (random deal, only hand sizes asserted)", "rule": "R2", "players": 4, "seed": 4, "rounds": 1, "default": "decline",
   "expect": {"players": {"1": {"hand_size": 5}, "2": {"hand_size": 6}, "3": {"hand_size": 6}, "4": {"hand_size": 6}}}},
  {"name": "Sent card leaves the hand and hand_size drops by 1", "rule": "R3", "players": 4, "seed": 5, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Rat", "Toad"], "hand_size": 2}}},
   "rules": [{"seat": 1, "options_include": "Rat"}, {"seat": 1, "options_include": "Toad"},
             {"seat": 1, "options_include": 3}, {"seat": 3, "options_include": "FALSE"}],
   "expect": {"lens": {"players": {"1": {"hand": 1}}},
              "players": {"1": {"hand_size": 1, "rat_up": 1, "faceup_total": 1}},
              "game": {"last_revealed": "Rat"}}},
  {"name": "Sender may claim a creature it does not hold and cannot choose itself as receiver", "rule": "R4", "players": 4, "seed": 6, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Rat", "Toad"], "hand_size": 2}}},
   "rules": [{"seat": 1, "options_include": "Rat"}, {"seat": 1, "options_include": "Fly"},
             {"seat": 1, "options_include": 4}, {"seat": 4, "options_include": "TRUE"}],
   "expect": {"offered": [{"seat": 1, "option": "Fly"}],
              "not_offered": [{"seat": 1, "option": 1}],
              "players": {"4": {"rat_up": 1, "faceup_total": 1}, "1": {"faceup_total": 0, "hand_size": 1}}}},
  {"name": "Only the chosen receiver is asked to respond to the claim", "rule": "R5", "players": 4, "seed": 7, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Roach", "Rat"], "hand_size": 2}}},
   "rules": [{"seat": 1, "options_include": "Roach", "times": 2},
             {"seat": 1, "options_include": 3}, {"seat": 3, "options_include": "TRUE"}],
   "expect": {"offered": [{"seat": 3, "option": "PASS"}],
              "not_offered": [{"seat": 2, "option": "TRUE"}, {"seat": 4, "option": "TRUE"}],
              "players": {"1": {"roach_up": 1, "faceup_total": 1}},
              "game": {"last_revealed": "Roach"}}},
  {"name": "TRUE on a true claim resolves against the sender's claim: sender takes", "rule": "R6", "players": 4, "seed": 8, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Roach", "Rat"], "hand_size": 2}}},
   "rules": [{"seat": 1, "options_include": "Roach", "times": 2},
             {"seat": 1, "options_include": 2}, {"seat": 2, "options_include": "TRUE"}],
   "expect": {"players": {"1": {"roach_up": 1, "faceup_total": 1}, "2": {"faceup_total": 0}},
              "game": {"last_revealed": "Roach"}}},
  {"name": "Passer makes a new claim to a seat that is neither sender nor itself", "rule": "R7", "players": 4, "seed": 9, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Roach", "Rat"], "hand_size": 2}}},
   "rules": [{"seat": 1, "options_include": "Roach"}, {"seat": 1, "options_include": "Rat"},
             {"seat": 1, "options_include": 2}, {"seat": 2, "options_include": "PASS"},
             {"seat": 2, "options_include": "Roach"}, {"seat": 2, "options_include": 3},
             {"seat": 3, "options_include": "TRUE"}],
   "expect": {"not_offered": [{"seat": 2, "option": 1}, {"seat": 2, "option": 2}],
              "offered": [{"seat": 2, "option": 4}],
              "players": {"2": {"roach_up": 1, "faceup_total": 1}, "1": {"faceup_total": 0, "hand_size": 1}, "3": {"faceup_total": 0}},
              "game": {"last_revealed": "Roach"}}},
  {"name": "After a pass the final receiver may not pass again; a wrong FALSE makes it take", "rule": "R8", "players": 4, "seed": 10, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Roach", "Rat"], "hand_size": 2}}},
   "rules": [{"seat": 1, "options_include": "Roach"}, {"seat": 1, "options_include": "Rat"},
             {"seat": 1, "options_include": 2}, {"seat": 2, "options_include": "PASS"},
             {"seat": 2, "options_include": "Roach"}, {"seat": 2, "options_include": 3},
             {"seat": 3, "options_include": "FALSE"}],
   "expect": {"not_offered": [{"seat": 3, "option": "PASS"}],
              "offered": [{"seat": 3, "option": "TRUE"}],
              "players": {"3": {"roach_up": 1, "faceup_total": 1}, "2": {"faceup_total": 0}}}},
  {"name": "Correct FALSE on a bluff: claimer takes the card", "rule": "R9", "players": 4, "seed": 11, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Rat", "Toad"], "hand_size": 2}}},
   "rules": [{"seat": 1, "options_include": "Rat"}, {"seat": 1, "options_include": "Toad"},
             {"seat": 1, "options_include": 2}, {"seat": 2, "options_include": "FALSE"}],
   "expect": {"players": {"1": {"rat_up": 1, "toad_up": 0, "faceup_total": 1}, "2": {"faceup_total": 0}},
              "game": {"last_revealed": "Rat"}}},
  {"name": "Wrong FALSE on a true claim: judge takes the card", "rule": "R10", "players": 4, "seed": 12, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Roach", "Rat"], "hand_size": 2}}},
   "rules": [{"seat": 1, "options_include": "Roach", "times": 2},
             {"seat": 1, "options_include": 2}, {"seat": 2, "options_include": "FALSE"}],
   "expect": {"players": {"2": {"roach_up": 1, "faceup_total": 1}, "1": {"faceup_total": 0, "roach_up": 0}},
              "game": {"last_revealed": "Roach"}}},
  {"name": "Taker becomes the next sender and its counts rise", "rule": "R11", "players": 4, "seed": 13, "rounds": 2,
   "given": {"players": {"1": {"hand": ["Roach", "Rat"], "hand_size": 2}, "2": {"hand": ["Fly", "Toad"], "hand_size": 2}}},
   "rules": [{"seat": 1, "options_include": "Roach", "times": 2},
             {"seat": 1, "options_include": 2}, {"seat": 2, "options_include": "FALSE"},
             {"seat": 2, "options_include": "Fly", "times": 2},
             {"seat": 2, "options_include": 3}, {"seat": 3, "options_include": "TRUE"}],
   "expect": {"players": {"1": {"hand_size": 1, "faceup_total": 0},
                          "2": {"hand_size": 1, "roach_up": 1, "fly_up": 1, "faceup_total": 2},
                          "3": {"faceup_total": 0}},
              "game": {"last_revealed": "Fly"}}},
  {"name": "Third face-up Roach makes the taker lose and ends the game", "rule": "R12", "players": 4, "seed": 14,
   "given": {"players": {"1": {"hand": ["Roach", "Rat"], "hand_size": 2}, "2": {"roach_up": 2, "faceup_total": 2}}},
   "rules": [{"seat": 1, "options_include": "Roach", "times": 2},
             {"seat": 1, "options_include": 2}, {"seat": 2, "options_include": "FALSE"}],
   "expect": {"winner": [1, 3, 4],
              "standings": {"1": 0, "2": -1003, "3": 0, "4": 0},
              "players": {"2": {"roach_up": 3, "faceup_total": 3, "lost": true}, "1": {"lost": false}}}},
  {"name": "Next sender with an empty hand loses", "rule": "R13", "players": 4, "seed": 15,
   "given": {"players": {"1": {"hand": ["Rat"], "hand_size": 1}}},
   "rules": [{"seat": 1, "options_include": "Toad"},
             {"seat": 1, "options_include": 2}, {"seat": 2, "options_include": "FALSE"}],
   "expect": {"winner": [2, 3, 4],
              "standings": {"1": -1001, "2": 0, "3": 0, "4": 0},
              "players": {"1": {"hand_size": 0, "rat_up": 1, "faceup_total": 1, "lost": true}, "2": {"lost": false}}}},
  {"name": "Among non-losers the fewest face-up cards wins", "rule": "R14", "players": 4, "seed": 16,
   "given": {"players": {"1": {"hand": ["Roach", "Rat"], "hand_size": 2, "toad_up": 1, "faceup_total": 1},
                         "2": {"roach_up": 2, "faceup_total": 2},
                         "3": {"fly_up": 1, "faceup_total": 1}}},
   "rules": [{"seat": 1, "options_include": "Roach", "times": 2},
             {"seat": 1, "options_include": 2}, {"seat": 2, "options_include": "FALSE"}],
   "expect": {"winner": 4,
              "standings": {"1": -1, "2": -1003, "3": -1, "4": 0},
              "players": {"2": {"lost": true}}}},
  {"name": "The game ends after round 24", "rule": "R15", "players": 4, "seed": 17,
   "given": {"players": {"1": {"hand": ["Roach", "Rat"], "hand_size": 2}}, "game": {"round_count": 23}},
   "rules": [{"seat": 1, "options_include": "Roach", "times": 2},
             {"seat": 1, "options_include": 2}, {"seat": 2, "options_include": "TRUE"}],
   "expect": {"winner": [2, 3, 4],
              "standings": {"1": -1, "2": 0, "3": 0, "4": 0},
              "players": {"1": {"roach_up": 1, "faceup_total": 1, "lost": false, "hand_size": 1}}}}
]
```

Why it was refused: scenario 1: needs `rules` (what each seat answers, by option name); scenario 2: needs `rules` (what each seat answers, by option name); scenario 3: needs `rules` (what each seat answers, by option name); scenario 4: needs `rules` (what each seat answers, by option name)
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
[
  {"name": "4 players: each seat is dealt 6 cards and the whole deck is dealt", "rule": "R1", "players": 4, "seed": 1, "rounds": 0,
   "rules": [],
   "expect": {"lens": {"game": {"deck": 0}, "players": {"1": {"hand": 6}, "2": {"hand": 6}, "3": {"hand": 6}, "4": {"hand": 6}}},
              "players": {"1": {"hand_size": 6}, "2": {"hand_size": 6}, "3": {"hand_size": 6}, "4": {"hand_size": 6}}}},
  {"name": "3 players: each seat is dealt 8 cards and the whole deck is dealt", "rule": "R1", "players": 3, "seed": 2, "rounds": 0,
   "rules": [],
   "expect": {"lens": {"game": {"deck": 0}, "players": {"1": {"hand": 8}, "2": {"hand": 8}, "3": {"hand": 8}}},
              "players": {"1": {"hand_size": 8}, "2": {"hand_size": 8}, "3": {"hand_size": 8}}}},
  {"name": "At start every face-up count is 0", "rule": "R2", "players": 4, "seed": 3, "rounds": 0,
   "rules": [],
   "expect": {"players": {
     "1": {"roach_up": 0, "rat_up": 0, "fly_up": 0, "toad_up": 0, "faceup_total": 0, "lost": false},
     "2": {"roach_up": 0, "rat_up": 0, "fly_up": 0, "toad_up": 0, "faceup_total": 0, "lost": false},
     "3": {"roach_up": 0, "rat_up": 0, "fly_up": 0, "toad_up": 0, "faceup_total": 0, "lost": false},
     "4": {"roach_up": 0, "rat_up": 0, "fly_up": 0, "toad_up": 0, "faceup_total": 0, "lost": false}}}},
  {"name": "Seat 1 sends first: only seat 1's hand shrinks in round 1", "rule": "R2", "players": 4, "seed": 4, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Fly", "Toad"], "hand_size": 2}}},
   "rules": [{"seat": 1, "options_include": "Fly", "times": 2},
             {"seat": 1, "options_include": 3}, {"seat": 3, "options_include": "TRUE"}],
   "expect": {"players": {"1": {"hand_size": 1, "fly_up": 1, "faceup_total": 1}, "2": {"hand_size": 6}, "3": {"hand_size": 6, "faceup_total": 0}, "4": {"hand_size": 6}},
              "game": {"last_revealed": "Fly"}}},
  {"name": "Sent card leaves the hand and hand_size drops by 1", "rule": "R3", "players": 4, "seed": 5, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Rat", "Toad"], "hand_size": 2}}},
   "rules": [{"seat": 1, "options_include": "Rat"}, {"seat": 1, "options_include": "Toad"},
             {"seat": 1, "options_include": 3}, {"seat": 3, "options_include": "FALSE"}],
   "expect": {"lens": {"players": {"1": {"hand": 1}}},
              "players": {"1": {"hand_size": 1, "rat_up": 1, "faceup_total": 1}},
              "game": {"last_revealed": "Rat"}}},
  {"name": "Sender may claim a creature it does not hold and cannot choose itself as receiver", "rule": "R4", "players": 4, "seed": 6, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Rat", "Toad"], "hand_size": 2}}},
   "rules": [{"seat": 1, "options_include": "Rat"}, {"seat": 1, "options_include": "Fly"},
             {"seat": 1, "options_include": 4}, {"seat": 4, "options_include": "TRUE"}],
   "expect": {"offered": [{"seat": 1, "option": "Fly"}],
              "not_offered": [{"seat": 1, "option": 1}],
              "players": {"4": {"rat_up": 1, "faceup_total": 1}, "1": {"faceup_total": 0, "hand_size": 1}}}},
  {"name": "Only the chosen receiver is asked to respond to the claim", "rule": "R5", "players": 4, "seed": 7, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Roach", "Rat"], "hand_size": 2}}},
   "rules": [{"seat": 1, "options_include": "Roach", "times": 2},
             {"seat": 1, "options_include": 3}, {"seat": 3, "options_include": "TRUE"}],
   "expect": {"offered": [{"seat": 3, "option": "PASS"}],
              "not_offered": [{"seat": 2, "option": "TRUE"}, {"seat": 4, "option": "TRUE"}],
              "players": {"1": {"roach_up": 1, "faceup_total": 1}},
              "game": {"last_revealed": "Roach"}}},
  {"name": "TRUE on a true claim resolves against the sender's claim: sender takes", "rule": "R6", "players": 4, "seed": 8, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Roach", "Rat"], "hand_size": 2}}},
   "rules": [{"seat": 1, "options_include": "Roach", "times": 2},
             {"seat": 1, "options_include": 2}, {"seat": 2, "options_include": "TRUE"}],
   "expect": {"players": {"1": {"roach_up": 1, "faceup_total": 1}, "2": {"faceup_total": 0}},
              "game": {"last_revealed": "Roach"}}},
  {"name": "Passer makes a new claim to a seat that is neither sender nor itself", "rule": "R7", "players": 4, "seed": 9, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Roach", "Rat"], "hand_size": 2}}},
   "rules": [{"seat": 1, "options_include": "Roach"}, {"seat": 1, "options_include": "Rat"},
             {"seat": 1, "options_include": 2}, {"seat": 2, "options_include": "PASS"},
             {"seat": 2, "options_include": "Roach"}, {"seat": 2, "options_include": 3},
             {"seat": 3, "options_include": "TRUE"}],
   "expect": {"not_offered": [{"seat": 2, "option": 1}, {"seat": 2, "option": 2}],
              "offered": [{"seat": 2, "option": 4}],
              "players": {"2": {"roach_up": 1, "faceup_total": 1}, "1": {"faceup_total": 0, "hand_size": 1}, "3": {"faceup_total": 0}},
              "game": {"last_revealed": "Roach"}}},
  {"name": "After a pass the final receiver may not pass again; a wrong FALSE makes it take", "rule": "R8", "players": 4, "seed": 10, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Roach", "Rat"], "hand_size": 2}}},
   "rules": [{"seat": 1, "options_include": "Roach"}, {"seat": 1, "options_include": "Rat"},
             {"seat": 1, "options_include": 2}, {"seat": 2, "options_include": "PASS"},
             {"seat": 2, "options_include": "Roach"}, {"seat": 2, "options_include": 3},
             {"seat": 3, "options_include": "FALSE"}],
   "expect": {"not_offered": [{"seat": 3, "option": "PASS"}],
              "offered": [{"seat": 3, "option": "TRUE"}],
              "players": {"3": {"roach_up": 1, "faceup_total": 1}, "2": {"faceup_total": 0}}}},
  {"name": "Correct FALSE on a bluff: claimer takes the card", "rule": "R9", "players": 4, "seed": 11, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Rat", "Toad"], "hand_size": 2}}},
   "rules": [{"seat": 1, "options_include": "Rat"}, {"seat": 1, "options_include": "Toad"},
             {"seat": 1, "options_include": 2}, {"seat": 2, "options_include": "FALSE"}],
   "expect": {"players": {"1": {"rat_up": 1, "toad_up": 0, "faceup_total": 1}, "2": {"faceup_total": 0}},
              "game": {"last_revealed": "Rat"}}},
  {"name": "Wrong FALSE on a true claim: judge takes the card", "rule": "R10", "players": 4, "seed": 12, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Roach", "Rat"], "hand_size": 2}}},
   "rules": [{"seat": 1, "options_include": "Roach", "times": 2},
             {"seat": 1, "options_include": 2}, {"seat": 2, "options_include": "FALSE"}],
   "expect": {"players": {"2": {"roach_up": 1, "faceup_total": 1}, "1": {"faceup_total": 0, "roach_up": 0}},
              "game": {"last_revealed": "Roach"}}},
  {"name": "Taker becomes the next sender and its counts rise", "rule": "R11", "players": 4, "seed": 13, "rounds": 2,
   "given": {"players": {"1": {"hand": ["Roach", "Rat"], "hand_size": 2}, "2": {"hand": ["Fly", "Toad"], "hand_size": 2}}},
   "rules": [{"seat": 1, "options_include": "Roach", "times": 2},
             {"seat": 1, "options_include": 2}, {"seat": 2, "options_include": "FALSE"},
             {"seat": 2, "options_include": "Fly", "times": 2},
             {"seat": 2, "options_include": 3}, {"seat": 3, "options_include": "TRUE"}],
   "expect": {"players": {"1": {"hand_size": 1, "faceup_total": 0},
                          "2": {"hand_size": 1, "roach_up": 1, "fly_up": 1, "faceup_total": 2},
                          "3": {"faceup_total": 0}},
              "game": {"last_revealed": "Fly"}}},
  {"name": "Third face-up Roach makes the taker lose and ends the game", "rule": "R12", "players": 4, "seed": 14,
   "given": {"players": {"1": {"hand": ["Roach", "Rat"], "hand_size": 2}, "2": {"roach_up": 2, "faceup_total": 2}}},
   "rules": [{"seat": 1, "options_include": "Roach", "times": 2},
             {"seat": 1, "options_include": 2}, {"seat": 2, "options_include": "FALSE"}],
   "expect": {"winner": [1, 3, 4],
              "standings": {"1": 0, "2": -1003, "3": 0, "4": 0},
              "players": {"2": {"roach_up": 3, "faceup_total": 3, "lost": true}, "1": {"lost": false}}}},
  {"name": "Next sender with an empty hand loses", "rule": "R13", "players": 4, "seed": 15,
   "given": {"players": {"1": {"hand": ["Rat"], "hand_size": 1}}},
   "rules": [{"seat": 1, "options_include": "Toad"},
             {"seat": 1, "options_include": 2}, {"seat": 2, "options_include": "FALSE"}],
   "expect": {"winner": [2, 3, 4],
              "standings": {"1": -1001, "2": 0, "3": 0, "4": 0},
              "players": {"1": {"hand_size": 0, "rat_up": 1, "faceup_total": 1, "lost": true}, "2": {"lost": false}}}},
  {"name": "Among non-losers the fewest face-up cards wins", "rule": "R14", "players": 4, "seed": 16,
   "given": {"players": {"1": {"hand": ["Roach", "Rat"], "hand_size": 2, "toad_up": 1, "faceup_total": 1},
                         "2": {"roach_up": 2, "faceup_total": 2},
                         "3": {"fly_up": 1, "faceup_total": 1}}},
   "rules": [{"seat": 1, "options_include": "Roach", "times": 2},
             {"seat": 1, "options_include": 2}, {"seat": 2, "options_include": "FALSE"}],
   "expect": {"winner": 4,
              "standings": {"1": -1, "2": -1003, "3": -1, "4": 0},
              "players": {"2": {"lost": true}}}},
  {"name": "The game ends after round 24", "rule": "R15", "players": 4, "seed": 17,
   "given": {"players": {"1": {"hand": ["Roach", "Rat"], "hand_size": 2}}, "game": {"round_count": 23}},
   "rules": [{"seat": 1, "options_include": "Roach", "times": 2},
             {"seat": 1, "options_include": 2}, {"seat": 2, "options_include": "TRUE"}],
   "expect": {"winner": [2, 3, 4],
              "standings": {"1": -1, "2": 0, "3": 0, "4": 0},
              "players": {"1": {"roach_up": 1, "faceup_total": 1, "lost": false, "hand_size": 1}}}}
]
```
````
