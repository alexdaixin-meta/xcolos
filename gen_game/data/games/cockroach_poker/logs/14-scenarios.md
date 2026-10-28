# 14 scenarios

- time: 2026-10-28T06:14:00+00:00 (39.9s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 ad16713cc1058ff1, reply sha256 903aae70ab5d7d10

## Sent

````
SPEC:
{
  "name": "Cockroach Poker: Straight Calls",
  "summary": "Three players pass cards face-down with a creature claim. The receiver calls the claim true or false, and whoever is wrong about the card takes it face-up. Three face-up cards of one creature, or having to send from an empty hand, loses.",
  "players": {
    "min": 3,
    "max": 3,
    "suggested": 3
  },
  "parameters": {
    "deck_size": 24,
    "creature_kinds": 4,
    "copies_per_creature": 6,
    "hand_size_start": 7,
    "aside_cards": 3,
    "max_rounds": 24,
    "loss_same_creature": 3,
    "receiver_options": 2
  },
  "attributes": {
    "player": [
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "The player's private hand of creature cards, one entry per card, such as 'Rat'.",
        "observable": false
      },
      {
        "key": "hand_size",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of cards in the hand.",
        "observable": true
      },
      {
        "key": "face_cockroach",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Face-up Cockroach cards.",
        "observable": true
      },
      {
        "key": "face_rat",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Face-up Rat cards.",
        "observable": true
      },
      {
        "key": "face_stinkbug",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Face-up Stinkbug cards.",
        "observable": true
      },
      {
        "key": "face_toad",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Face-up Toad cards.",
        "observable": true
      },
      {
        "key": "face_total",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Total face-up cards, the sum of the four face counts.",
        "observable": true
      },
      {
        "key": "max_face",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Largest of the four face counts.",
        "observable": true
      },
      {
        "key": "lost",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "1 if this player has lost, otherwise 0.",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [
          "Cockroach x6",
          "Rat x6",
          "Stinkbug x6",
          "Toad x6"
        ],
        "meaning": "The 24-card deck before dealing: 6 entries of each creature.",
        "observable": false
      },
      {
        "key": "aside",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "The 3 cards set aside face-down, unseen by anyone, for the whole game.",
        "observable": false
      },
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Current round number.",
        "observable": true
      },
      {
        "key": "sender",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat of the current sender.",
        "observable": true
      },
      {
        "key": "receiver",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat chosen as receiver this round.",
        "observable": true
      },
      {
        "key": "card_in_play",
        "type": "text",
        "visible": "none",
        "initial": "",
        "meaning": "The creature on the card being passed. It stays hidden until the reveal.",
        "observable": false
      },
      {
        "key": "revealed_card",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The passed card's creature, made public at the reveal.",
        "observable": true
      },
      {
        "key": "claim",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The sender's claimed creature.",
        "observable": true
      },
      {
        "key": "call",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The receiver's call, TRUE or FALSE.",
        "observable": true
      },
      {
        "key": "taker",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat that took the card face-up this round.",
        "observable": true
      },
      {
        "key": "game_over",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "1 once the game has ended.",
        "observable": true
      }
    ]
  },
  "setup": [
    "Fill deck with 24 cards: 6 each of Cockroach, Rat, Stinkbug and Toad.",
    "Deal 7 cards to each of the 3 players. Each card is a random draw removed from deck and appended to that player's hand. Set each hand_size to 7.",
    "Move the remaining 3 cards from deck to aside, unseen by anyone, for the whole game.",
    "Every player starts with all face counts, face_total, max_face and lost at 0.",
    "Set sender to a seat chosen uniformly at random, and set round to 1."
  ],
  "round": [
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce round, sender, and each player's face_cockroach, face_rat, face_stinkbug, face_toad and hand_size."
    },
    {
      "action": "ask",
      "who": "the sender (seat = sender)",
      "answer": "one creature present in the sender's hand",
      "effect": "Set card_in_play to the chosen creature. Remove one card of that creature from the sender's hand and decrease the sender's hand_size by 1."
    },
    {
      "action": "ask",
      "who": "the sender (seat = sender)",
      "answer": "one of Cockroach, Rat, Stinkbug, Toad",
      "effect": "Set claim to the answer, visible to all."
    },
    {
      "action": "ask",
      "who": "the sender (seat = sender)",
      "answer": "one of the two other seats",
      "effect": "Set receiver to the chosen seat."
    },
    {
      "action": "ask",
      "who": "the receiver (seat = receiver)",
      "answer": "TRUE or FALSE",
      "effect": "Set call to the answer."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Set revealed_card = card_in_play and announce it. Let correct = (call == TRUE and card_in_play == claim) or (call == FALSE and card_in_play != claim). If correct, taker = sender, otherwise taker = receiver. Add 1 to the taker's face_<card_in_play> and to their face_total, and recompute the taker's max_face."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Set sender = taker for the next round."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "If the taker's face count for revealed_card >= 3, set the taker's lost = 1 and game_over = 1, and end the game."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "If the new sender's hand_size == 0, set that player's lost = 1 and game_over = 1, and end the game."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "If round >= 24, set game_over = 1 and end the game with no loser. Otherwise add 1 to round."
    }
  ],
  "ending": {
    "condition": "game_over == 1, which happens when some player's lost == 1 or when round 24 has finished",
    "rank_by": "(1 - you.lost) * 1000000 - you.face_total * 10000 - you.max_face * 100 + you.hand_size",
    "decided_by": "A player who lost can never rank above a player who did not. Among the others, fewest face-up cards ranks first, then the smaller most-common face-up creature count, then more cards left in hand. The highest value wins, and players level on all three tests share the win (a draw)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "At setup, each of the 3 players holds 7 cards, 3 cards are set aside unseen, and the deck of 24 (6 of each of 4 creatures) is fully used."
    },
    {
      "id": "R2",
      "text": "At setup, every player has 0 face-up cards and lost = 0, and the first sender is a random seat."
    },
    {
      "id": "R3",
      "text": "Each round, the sender passes one card from their own hand, and the sender's hand_size falls by 1."
    },
    {
      "id": "R4",
      "text": "The sender's claim is one of Cockroach, Rat, Stinkbug or Toad, and it may differ from the card."
    },
    {
      "id": "R5",
      "text": "The receiver must be one of the two seats other than the sender."
    },
    {
      "id": "R6",
      "text": "When the receiver calls TRUE and the card matches the claim, the sender takes the card face-up."
    },
    {
      "id": "R7",
      "text": "When the receiver calls FALSE and the card does not match the claim, the sender takes the card face-up."
    },
    {
      "id": "R8",
      "text": "When the receiver calls TRUE and the card does not match, or calls FALSE and it matches, the receiver takes the card face-up."
    },
    {
      "id": "R9",
      "text": "The card is revealed to everyone after the call, and the taker's count for that creature and face_total rise by 1."
    },
    {
      "id": "R10",
      "text": "The player who took the card face-up is the sender of the next round."
    },
    {
      "id": "R11",
      "text": "When the taker reaches 3 face-up cards of one creature, the taker's lost becomes 1 and the game ends."
    },
    {
      "id": "R12",
      "text": "When the next sender has 0 cards in hand, that player's lost becomes 1 and the game ends."
    },
    {
      "id": "R13",
      "text": "When round 24 finishes without a loser, the game ends with no loser."
    },
    {
      "id": "R14",
      "text": "A player with lost = 1 cannot win."
    },
    {
      "id": "R15",
      "text": "Among the players who did not lose, the one with the fewest face_total wins."
    },
    {
      "id": "R16",
      "text": "If face_total is tied, the smaller max_face wins. If that is still tied, the larger hand_size wins. If all three are tied, the tied players draw."
    }
  ],
  "offers": [
    {
      "question": "Which card to pass",
      "who": "the sender only",
      "options": "each distinct creature currently in the sender's hand"
    },
    {
      "question": "Which creature to claim",
      "who": "the sender only",
      "options": "Cockroach, Rat, Stinkbug, Toad"
    },
    {
      "question": "Who receives the card",
      "who": "the sender only",
      "options": "the two seats other than the sender"
    },
    {
      "question": "Call the claim",
      "who": "the receiver only",
      "options": "TRUE, FALSE"
    }
  ],
  "choices": [
    {
      "what": "Exactly 3 players, suggested 3",
      "why": "The designer fixed the game at 3. The deal of 7 + 7 + 7 + 3 aside uses the 24-card deck exactly, so another count would break the deal. Three seats also give the sender a real choice of whom to target."
    },
    {
      "what": "No talk phase",
      "why": "The rules say the claim is the only message."
    },
    {
      "what": "Single rank_by expression with weights 1000000 / 10000 / 100",
      "why": "This encodes not-lost first, then fewest face_total, then smaller max_face, then more hand_size. Each weight exceeds the largest possible value of the next term (face_total <= 24, max_face <= 6, hand_size <= 7)."
    },
    {
      "what": "Strategy at the table",
      "why": "The sender reads which creatures each player already shows and steers cards toward the player closest to 3 of a kind, bluffing or telling the truth unpredictably. The receiver weighs the sender's hand and the creatures already exposed when calling."
    }
  ],
  "simplifications": [
    {
      "what": "A card is chosen by naming its creature",
      "why": "Copies of a creature are identical, so naming the creature is equivalent to picking the card."
    },
    {
      "what": "The sender's three decisions are three sequential asks",
      "why": "Only the sender answers them and the receiver does not see the card, so splitting them changes nothing."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: hand_size, face_cockroach, face_rat, face_stinkbug, face_toad, face_total, max_face, lost; table: round, sender, receiver, revealed_card, claim, call, taker, game_over.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
[
{"name":"Setup deals 7 cards to each seat and sets 3 aside","rule":"R1","players":3,"seed":1,"rounds":0,
 "expect":{"lens":{"game":{"aside":3,"deck":0},"players":{"1":{"hand":7},"2":{"hand":7},"3":{"hand":7}}},
  "players":{"1":{"hand_size":7},"2":{"hand_size":7},"3":{"hand_size":7}}}},
{"name":"Setup starts everyone with no face-up cards and not lost","rule":"R2","players":3,"seed":2,"rounds":0,
 "expect":{"players":{"1":{"face_total":0,"max_face":0,"lost":0,"face_rat":0,"face_toad":0,"face_cockroach":0,"face_stinkbug":0},
  "2":{"face_total":0,"max_face":0,"lost":0},"3":{"face_total":0,"max_face":0,"lost":0}},"game":{"round":1,"game_over":0}}},
{"name":"Sender passes one card and hand_size falls by 1","rule":"R3","players":3,"seed":1,"rounds":1,
 "given":{"players":{"1":{"hand":["Rat","Stinkbug","Toad"],"hand_size":3}},"game":{"sender":1}},
 "rules":[{"seat":1,"options_include":"Rat","times":2},{"seat":1,"options_include":2},{"seat":2,"options_include":"TRUE"}],
 "expect":{"players":{"1":{"hand_size":2,"face_rat":1}},"lens":{"players":{"1":{"hand":2}}}}},
{"name":"Claim may differ from the card and any creature can be claimed","rule":"R4","players":3,"seed":1,"rounds":1,
 "given":{"players":{"1":{"hand":["Rat","Stinkbug"],"hand_size":2}},"game":{"sender":1}},
 "rules":[{"seat":1,"options_include":"Rat"},{"seat":1,"options_include":"Toad"},{"seat":1,"options_include":2},{"seat":2,"options_include":"FALSE"}],
 "expect":{"game":{"claim":"Toad","revealed_card":"Rat"},"offered":[{"seat":1,"option":"Cockroach"}]}},
{"name":"Receiver is one of the other two seats, never the sender","rule":"R5","players":3,"seed":1,"rounds":1,
 "given":{"players":{"1":{"hand":["Rat","Stinkbug"],"hand_size":2}},"game":{"sender":1}},
 "rules":[{"seat":1,"options_include":"Rat","times":2},{"seat":1,"options_include":3},{"seat":3,"options_include":"TRUE"}],
 "expect":{"game":{"receiver":3},"offered":[{"seat":1,"option":2},{"seat":1,"option":3}],
  "not_offered":[{"seat":1,"option":1},{"seat":2,"option":"TRUE"},{"seat":2,"option":"FALSE"}]}},
{"name":"TRUE call on a true claim: sender takes the card","rule":"R6","players":3,"seed":1,"rounds":1,
 "given":{"players":{"1":{"hand":["Rat","Stinkbug"],"hand_size":2}},"game":{"sender":1}},
 "rules":[{"seat":1,"options_include":"Rat","times":2},{"seat":1,"options_include":2},{"seat":2,"options_include":"TRUE"}],
 "expect":{"game":{"taker":1,"call":"TRUE"},"players":{"1":{"face_rat":1,"face_total":1},"2":{"face_total":0}}}},
{"name":"FALSE call on a bluff: sender takes the card","rule":"R7","players":3,"seed":1,"rounds":1,
 "given":{"players":{"1":{"hand":["Rat","Stinkbug"],"hand_size":2}},"game":{"sender":1}},
 "rules":[{"seat":1,"options_include":"Rat"},{"seat":1,"options_include":"Toad"},{"seat":1,"options_include":2},{"seat":2,"options_include":"FALSE"}],
 "expect":{"game":{"taker":1,"call":"FALSE"},"players":{"1":{"face_rat":1,"face_total":1},"2":{"face_total":0}}}},
{"name":"TRUE call on a bluff: receiver takes the card","rule":"R8","players":3,"seed":1,"rounds":1,
 "given":{"players":{"1":{"hand":["Rat","Stinkbug"],"hand_size":2}},"game":{"sender":1}},
 "rules":[{"seat":1,"options_include":"Rat"},{"seat":1,"options_include":"Toad"},{"seat":1,"options_include":2},{"seat":2,"options_include":"TRUE"}],
 "expect":{"game":{"taker":2},"players":{"2":{"face_rat":1,"face_total":1},"1":{"face_total":0,"hand_size":1}}}},
{"name":"FALSE call on a true claim: receiver takes the card","rule":"R8","players":3,"seed":1,"rounds":1,
 "given":{"players":{"1":{"hand":["Rat","Stinkbug"],"hand_size":2}},"game":{"sender":1}},
 "rules":[{"seat":1,"options_include":"Rat","times":2},{"seat":1,"options_include":3},{"seat":3,"options_include":"FALSE"}],
 "expect":{"game":{"taker":3},"players":{"3":{"face_rat":1,"face_total":1},"1":{"face_total":0}}}},
{"name":"Card is revealed and taker's creature count and total rise by 1","rule":"R9","players":3,"seed":1,"rounds":1,
 "given":{"players":{"1":{"hand":["Toad","Stinkbug"],"hand_size":2},"2":{"face_toad":1,"face_total":1,"max_face":1}},"game":{"sender":1}},
 "rules":[{"seat":1,"options_include":"Toad"},{"seat":1,"options_include":"Rat"},{"seat":1,"options_include":2},{"seat":2,"options_include":"TRUE"}],
 "expect":{"game":{"revealed_card":"Toad","claim":"Rat"},"players":{"2":{"face_toad":2,"face_total":2,"max_face":2}}}},
{"name":"The taker becomes the next sender","rule":"R10","players":3,"seed":1,"rounds":1,
 "given":{"players":{"1":{"hand":["Rat","Stinkbug"],"hand_size":2}},"game":{"sender":1}},
 "rules":[{"seat":1,"options_include":"Rat"},{"seat":1,"options_include":"Toad"},{"seat":1,"options_include":2},{"seat":2,"options_include":"TRUE"}],
 "expect":{"game":{"taker":2,"sender":2}}},
{"name":"Third face-up Rat makes the taker lose and ends the game","rule":"R11","players":3,"seed":1,
 "given":{"players":{"1":{"hand":["Rat","Stinkbug"],"hand_size":2},"2":{"face_rat":2,"face_total":2,"max_face":2,"hand":["Toad"],"hand_size":1},"3":{"hand":["Toad","Toad"],"hand_size":2}},"game":{"sender":1}},
 "rules":[{"seat":1,"options_include":"Rat"},{"seat":1,"options_include":"Cockroach"},{"seat":1,"options_include":2},{"seat":2,"options_include":"TRUE"}],
 "expect":{"winner":3,"standings":{"1":1000001,"2":-30299,"3":1000002},
  "players":{"2":{"lost":1,"face_rat":3},"1":{"lost":0},"3":{"lost":0}},"game":{"game_over":1}}},
{"name":"Next sender with an empty hand loses","rule":"R12","players":3,"seed":1,
 "given":{"players":{"1":{"hand":["Rat"],"hand_size":1},"2":{"hand":["Toad","Toad"],"hand_size":2},"3":{"hand":["Toad"],"hand_size":1}},"game":{"sender":1}},
 "rules":[{"seat":1,"options_include":"Rat","times":2},{"seat":1,"options_include":2},{"seat":2,"options_include":"TRUE"}],
 "expect":{"winner":2,"standings":{"1":-10100,"2":1000002,"3":1000001},
  "players":{"1":{"lost":1,"hand_size":0,"face_rat":1},"2":{"lost":0},"3":{"lost":0}},"game":{"game_over":1}}},
{"name":"Round 24 finishing ends the game with no loser","rule":"R13","players":3,"seed":1,
 "given":{"players":{"1":{"hand":["Rat","Stinkbug"],"hand_size":2},"2":{"hand":["Toad","Toad","Toad"],"hand_size":3},"3":{"hand":["Toad","Toad"],"hand_size":2}},"game":{"sender":1,"round":24}},
 "rules":[{"seat":1,"options_include":"Rat","times":2},{"seat":1,"options_include":2},{"seat":2,"options_include":"TRUE"}],
 "expect":{"winner":2,"standings":{"1":989901,"2":1000003,"3":1000002},
  "players":{"1":{"lost":0},"2":{"lost":0},"3":{"lost":0}},"game":{"game_over":1}}},
{"name":"A seat that lost cannot win despite the fewest face-up cards","rule":"R14","players":3,"seed":1,
 "given":{"players":{"2":{"hand":["Rat"],"hand_size":1},
  "1":{"hand":["Stinkbug"],"hand_size":1,"face_cockroach":2,"face_toad":2,"face_total":4,"max_face":2},
  "3":{"hand":["Toad"],"hand_size":1,"face_cockroach":2,"face_stinkbug":2,"face_toad":1,"face_total":5,"max_face":2}},"game":{"sender":2}},
 "rules":[{"seat":2,"options_include":"Rat","times":2},{"seat":2,"options_include":1},{"seat":1,"options_include":"TRUE"}],
 "expect":{"winner":1,"standings":{"1":959801,"2":-10100,"3":949801},"players":{"2":{"lost":1}}}},
{"name":"Fewest face-up cards wins over a bigger hand","rule":"R15","players":3,"seed":1,
 "given":{"players":{"1":{"hand":["Rat","Stinkbug"],"hand_size":2},
  "2":{"hand":["Toad","Toad","Toad","Toad","Toad"],"hand_size":5,"face_toad":2,"face_total":2,"max_face":2},
  "3":{"hand":["Toad"],"hand_size":1}},"game":{"sender":1,"round":24}},
 "rules":[{"seat":1,"options_include":"Rat","times":2},{"seat":1,"options_include":2},{"seat":2,"options_include":"TRUE"}],
 "expect":{"winner":3,"standings":{"1":989901,"2":979805,"3":1000001}}},
{"name":"Tied face_total: smaller max_face wins over larger hand","rule":"R16","players":3,"seed":1,
 "given":{"players":{"1":{"hand":["Rat","Stinkbug"],"hand_size":2,"face_rat":1,"face_total":1,"max_face":1},
  "2":{"hand":["Toad","Toad","Toad"],"hand_size":3,"face_toad":2,"face_total":2,"max_face":2},
  "3":{"hand":["Toad"],"hand_size":1,"face_cockroach":1,"face_toad":1,"face_total":2,"max_face":1}},"game":{"sender":1,"round":24}},
 "rules":[{"seat":1,"options_include":"Rat","times":2},{"seat":1,"options_include":2},{"seat":2,"options_include":"TRUE"}],
 "expect":{"winner":3,"standings":{"1":979801,"2":979803,"3":979901}}},
{"name":"Tied face_total and max_face: larger hand wins, full tie shares the win","rule":"R16","players":3,"seed":1,
 "given":{"players":{"1":{"hand":["Rat","Stinkbug"],"hand_size":2},
  "2":{"hand":["Toad","Toad"],"hand_size":2,"face_toad":1,"face_total":1,"max_face":1},
  "3":{"hand":["Toad","Toad"],"hand_size":2,"face_cockroach":1,"face_total":1,"max_face":1}},"game":{"sender":1,"round":24}},
 "rules":[{"seat":1,"options_include":"Rat","times":2},{"seat":1,"options_include":2},{"seat":2,"options_include":"TRUE"}],
 "expect":{"winner":[2,3],"standings":{"1":989901,"2":989902,"3":989902}}}
]

Why it was refused: scenario 1: needs `rules` (what each seat answers, by option name); scenario 2: needs `rules` (what each seat answers, by option name)
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
[
{"name":"Setup deals 7 cards to each seat and sets 3 aside (seat 1's hand after it sends one)","rule":"R1","players":3,"seed":1,"rounds":1,"default":"first",
 "given":{"game":{"sender":1}},
 "rules":[{"seat":1,"options_include":2},{"seat":2,"options_include":"TRUE"}],
 "expect":{"lens":{"game":{"aside":3,"deck":0},"players":{"1":{"hand":6},"2":{"hand":7},"3":{"hand":7}}},
  "players":{"1":{"hand_size":6},"2":{"hand_size":7},"3":{"hand_size":7}}}},
{"name":"Setup starts everyone with no face-up cards and not lost (uninvolved seat stays at 0)","rule":"R2","players":3,"seed":2,"rounds":1,"default":"first",
 "given":{"game":{"sender":1}},
 "rules":[{"seat":1,"options_include":2},{"seat":2,"options_include":"TRUE"}],
 "expect":{"players":{"3":{"face_total":0,"max_face":0,"lost":0,"face_rat":0,"face_toad":0,"face_cockroach":0,"face_stinkbug":0},
  "1":{"lost":0},"2":{"lost":0}},"game":{"round":2,"game_over":0}}},
{"name":"Sender passes one card and hand_size falls by 1","rule":"R3","players":3,"seed":1,"rounds":1,
 "given":{"players":{"1":{"hand":["Rat","Stinkbug","Toad"],"hand_size":3}},"game":{"sender":1}},
 "rules":[{"seat":1,"options_include":"Rat","times":2},{"seat":1,"options_include":2},{"seat":2,"options_include":"TRUE"}],
 "expect":{"players":{"1":{"hand_size":2,"face_rat":1}},"lens":{"players":{"1":{"hand":2}}}}},
{"name":"Claim may differ from the card and any creature can be claimed","rule":"R4","players":3,"seed":1,"rounds":1,
 "given":{"players":{"1":{"hand":["Rat","Stinkbug"],"hand_size":2}},"game":{"sender":1}},
 "rules":[{"seat":1,"options_include":"Rat"},{"seat":1,"options_include":"Toad"},{"seat":1,"options_include":2},{"seat":2,"options_include":"FALSE"}],
 "expect":{"game":{"claim":"Toad","revealed_card":"Rat"},"offered":[{"seat":1,"option":"Cockroach"}]}},
{"name":"Receiver is one of the other two seats, never the sender","rule":"R5","players":3,"seed":1,"rounds":1,
 "given":{"players":{"1":{"hand":["Rat","Stinkbug"],"hand_size":2}},"game":{"sender":1}},
 "rules":[{"seat":1,"options_include":"Rat","times":2},{"seat":1,"options_include":3},{"seat":3,"options_include":"TRUE"}],
 "expect":{"game":{"receiver":3},"offered":[{"seat":1,"option":2},{"seat":1,"option":3}],
  "not_offered":[{"seat":1,"option":1},{"seat":2,"option":"TRUE"},{"seat":2,"option":"FALSE"}]}},
{"name":"TRUE call on a true claim: sender takes the card","rule":"R6","players":3,"seed":1,"rounds":1,
 "given":{"players":{"1":{"hand":["Rat","Stinkbug"],"hand_size":2}},"game":{"sender":1}},
 "rules":[{"seat":1,"options_include":"Rat","times":2},{"seat":1,"options_include":2},{"seat":2,"options_include":"TRUE"}],
 "expect":{"game":{"taker":1,"call":"TRUE"},"players":{"1":{"face_rat":1,"face_total":1},"2":{"face_total":0}}}},
{"name":"FALSE call on a bluff: sender takes the card","rule":"R7","players":3,"seed":1,"rounds":1,
 "given":{"players":{"1":{"hand":["Rat","Stinkbug"],"hand_size":2}},"game":{"sender":1}},
 "rules":[{"seat":1,"options_include":"Rat"},{"seat":1,"options_include":"Toad"},{"seat":1,"options_include":2},{"seat":2,"options_include":"FALSE"}],
 "expect":{"game":{"taker":1,"call":"FALSE"},"players":{"1":{"face_rat":1,"face_total":1},"2":{"face_total":0}}}},
{"name":"TRUE call on a bluff: receiver takes the card","rule":"R8","players":3,"seed":1,"rounds":1,
 "given":{"players":{"1":{"hand":["Rat","Stinkbug"],"hand_size":2}},"game":{"sender":1}},
 "rules":[{"seat":1,"options_include":"Rat"},{"seat":1,"options_include":"Toad"},{"seat":1,"options_include":2},{"seat":2,"options_include":"TRUE"}],
 "expect":{"game":{"taker":2},"players":{"2":{"face_rat":1,"face_total":1},"1":{"face_total":0,"hand_size":1}}}},
{"name":"FALSE call on a true claim: receiver takes the card","rule":"R8","players":3,"seed":1,"rounds":1,
 "given":{"players":{"1":{"hand":["Rat","Stinkbug"],"hand_size":2}},"game":{"sender":1}},
 "rules":[{"seat":1,"options_include":"Rat","times":2},{"seat":1,"options_include":3},{"seat":3,"options_include":"FALSE"}],
 "expect":{"game":{"taker":3},"players":{"3":{"face_rat":1,"face_total":1},"1":{"face_total":0}}}},
{"name":"Card is revealed and taker's creature count and total rise by 1","rule":"R9","players":3,"seed":1,"rounds":1,
 "given":{"players":{"1":{"hand":["Toad","Stinkbug"],"hand_size":2},"2":{"face_toad":1,"face_total":1,"max_face":1}},"game":{"sender":1}},
 "rules":[{"seat":1,"options_include":"Toad"},{"seat":1,"options_include":"Rat"},{"seat":1,"options_include":2},{"seat":2,"options_include":"TRUE"}],
 "expect":{"game":{"revealed_card":"Toad","claim":"Rat"},"players":{"2":{"face_toad":2,"face_total":2,"max_face":2}}}},
{"name":"The taker becomes the next sender","rule":"R10","players":3,"seed":1,"rounds":1,
 "given":{"players":{"1":{"hand":["Rat","Stinkbug"],"hand_size":2}},"game":{"sender":1}},
 "rules":[{"seat":1,"options_include":"Rat"},{"seat":1,"options_include":"Toad"},{"seat":1,"options_include":2},{"seat":2,"options_include":"TRUE"}],
 "expect":{"game":{"taker":2,"sender":2}}},
{"name":"Third face-up Rat makes the taker lose and ends the game","rule":"R11","players":3,"seed":1,
 "given":{"players":{"1":{"hand":["Rat","Stinkbug"],"hand_size":2},"2":{"face_rat":2,"face_total":2,"max_face":2,"hand":["Toad"],"hand_size":1},"3":{"hand":["Toad","Toad"],"hand_size":2}},"game":{"sender":1}},
 "rules":[{"seat":1,"options_include":"Rat"},{"seat":1,"options_include":"Cockroach"},{"seat":1,"options_include":2},{"seat":2,"options_include":"TRUE"}],
 "expect":{"winner":3,"standings":{"1":1000001,"2":-30299,"3":1000002},
  "players":{"2":{"lost":1,"face_rat":3},"1":{"lost":0},"3":{"lost":0}},"game":{"game_over":1}}},
{"name":"Next sender with an empty hand loses","rule":"R12","players":3,"seed":1,
 "given":{"players":{"1":{"hand":["Rat"],"hand_size":1},"2":{"hand":["Toad","Toad"],"hand_size":2},"3":{"hand":["Toad"],"hand_size":1}},"game":{"sender":1}},
 "rules":[{"seat":1,"options_include":"Rat","times":2},{"seat":1,"options_include":2},{"seat":2,"options_include":"TRUE"}],
 "expect":{"winner":2,"standings":{"1":-10100,"2":1000002,"3":1000001},
  "players":{"1":{"lost":1,"hand_size":0,"face_rat":1},"2":{"lost":0},"3":{"lost":0}},"game":{"game_over":1}}},
{"name":"Round 24 finishing ends the game with no loser","rule":"R13","players":3,"seed":1,
 "given":{"players":{"1":{"hand":["Rat","Stinkbug"],"hand_size":2},"2":{"hand":["Toad","Toad","Toad"],"hand_size":3},"3":{"hand":["Toad","Toad"],"hand_size":2}},"game":{"sender":1,"round":24}},
 "rules":[{"seat":1,"options_include":"Rat","times":2},{"seat":1,"options_include":2},{"seat":2,"options_include":"TRUE"}],
 "expect":{"winner":2,"standings":{"1":989901,"2":1000003,"3":1000002},
  "players":{"1":{"lost":0},"2":{"lost":0},"3":{"lost":0}},"game":{"game_over":1}}},
{"name":"A seat that lost cannot win despite the fewest face-up cards","rule":"R14","players":3,"seed":1,
 "given":{"players":{"2":{"hand":["Rat"],"hand_size":1},
  "1":{"hand":["Stinkbug"],"hand_size":1,"face_cockroach":2,"face_toad":2,"face_total":4,"max_face":2},
  "3":{"hand":["Toad"],"hand_size":1,"face_cockroach":2,"face_stinkbug":2,"face_toad":1,"face_total":5,"max_face":2}},"game":{"sender":2}},
 "rules":[{"seat":2,"options_include":"Rat","times":2},{"seat":2,"options_include":1},{"seat":1,"options_include":"TRUE"}],
 "expect":{"winner":1,"standings":{"1":959801,"2":-10100,"3":949801},"players":{"2":{"lost":1}}}},
{"name":"Fewest face-up cards wins over a bigger hand","rule":"R15","players":3,"seed":1,
 "given":{"players":{"1":{"hand":["Rat","Stinkbug"],"hand_size":2},
  "2":{"hand":["Toad","Toad","Toad","Toad","Toad"],"hand_size":5,"face_toad":2,"face_total":2,"max_face":2},
  "3":{"hand":["Toad"],"hand_size":1}},"game":{"sender":1,"round":24}},
 "rules":[{"seat":1,"options_include":"Rat","times":2},{"seat":1,"options_include":2},{"seat":2,"options_include":"TRUE"}],
 "expect":{"winner":3,"standings":{"1":989901,"2":979805,"3":1000001}}},
{"name":"Tied face_total: smaller max_face wins over larger hand","rule":"R16","players":3,"seed":1,
 "given":{"players":{"1":{"hand":["Rat","Stinkbug"],"hand_size":2,"face_rat":1,"face_total":1,"max_face":1},
  "2":{"hand":["Toad","Toad","Toad"],"hand_size":3,"face_toad":2,"face_total":2,"max_face":2},
  "3":{"hand":["Toad"],"hand_size":1,"face_cockroach":1,"face_toad":1,"face_total":2,"max_face":1}},"game":{"sender":1,"round":24}},
 "rules":[{"seat":1,"options_include":"Rat","times":2},{"seat":1,"options_include":2},{"seat":2,"options_include":"TRUE"}],
 "expect":{"winner":3,"standings":{"1":979801,"2":979803,"3":979901}}},
{"name":"Tied face_total and max_face: larger hand wins, full tie shares the win","rule":"R16","players":3,"seed":1,
 "given":{"players":{"1":{"hand":["Rat","Stinkbug"],"hand_size":2},
  "2":{"hand":["Toad","Toad"],"hand_size":2,"face_toad":1,"face_total":1,"max_face":1},
  "3":{"hand":["Toad","Toad"],"hand_size":2,"face_cockroach":1,"face_total":1,"max_face":1}},"game":{"sender":1,"round":24}},
 "rules":[{"seat":1,"options_include":"Rat","times":2},{"seat":1,"options_include":2},{"seat":2,"options_include":"TRUE"}],
 "expect":{"winner":[2,3],"standings":{"1":989901,"2":989902,"3":989902}}}
]
````
