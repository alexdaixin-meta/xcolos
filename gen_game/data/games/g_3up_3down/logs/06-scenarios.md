# 06 scenarios

- time: 2026-10-28T03:57:26+00:00 (129.5s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 89b502b5382a4f70, reply sha256 5ea36d2f459d0800

## Sent

````
SPEC:
{
  "name": "Three Up: Even Rounds",
  "summary": "A three-player shedding game: each round everyone talks at the same time, then First, Second and Third each play cards of one rank at or above the Pile's top rank, play a Clear, or pick up the Pile; the first to empty Hand and Up pile wins, and the lowest picked-up total breaks ties.",
  "players": {
    "min": 3,
    "max": 3,
    "suggested": 3
  },
  "parameters": {
    "total_cards": 30,
    "lowest_rank": 1,
    "highest_rank": 9,
    "copies_per_rank": 3,
    "clear_cards": 3,
    "stack_size": 9,
    "low_ranks_max": 3,
    "mid_ranks_max": 6,
    "high_ranks_max": 9,
    "deal_per_stack": 3,
    "clear_per_player": 1,
    "cards_per_player": 10,
    "up_pile_size": 3,
    "hand_after_up": 7,
    "run_to_clear": 3,
    "max_rounds": 40,
    "rank_out_weight": 1000000,
    "rank_cards_weight": 10000
  },
  "attributes": {
    "player": [
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "The player's Hand cards, each written as '1'..'9' or 'C' for a Clear. Only the owner sees them.",
        "observable": false
      },
      {
        "key": "up_choice",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "The cards picked for the Up pile during the simultaneous setup choice, held privately until every player has chosen.",
        "observable": false
      },
      {
        "key": "up_pile",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "The player's revealed Up pile of 3 cards.",
        "observable": true
      },
      {
        "key": "hand_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The number of cards in Hand.",
        "observable": true
      },
      {
        "key": "up_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The number of cards in the Up pile.",
        "observable": true
      },
      {
        "key": "cards_left",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "hand_count + up_count.",
        "observable": true
      },
      {
        "key": "picked_up",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The total number of cards this player has taken from the Pile during the game.",
        "observable": true
      },
      {
        "key": "out",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "True when cards_left is 0. An out player skips their turns.",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "low_stack",
        "type": "list",
        "visible": "none",
        "initial": [
          "1",
          "1",
          "1",
          "2",
          "2",
          "2",
          "3",
          "3",
          "3"
        ],
        "meaning": "The shuffled Low stack.",
        "observable": false
      },
      {
        "key": "mid_stack",
        "type": "list",
        "visible": "none",
        "initial": [
          "4",
          "4",
          "4",
          "5",
          "5",
          "5",
          "6",
          "6",
          "6"
        ],
        "meaning": "The shuffled Mid stack.",
        "observable": false
      },
      {
        "key": "high_stack",
        "type": "list",
        "visible": "none",
        "initial": [
          "7",
          "7",
          "7",
          "8",
          "8",
          "8",
          "9",
          "9",
          "9"
        ],
        "meaning": "The shuffled High stack.",
        "observable": false
      },
      {
        "key": "clear_stack",
        "type": "list",
        "visible": "none",
        "initial": [
          "C",
          "C",
          "C"
        ],
        "meaning": "The three Clear cards before the deal.",
        "observable": false
      },
      {
        "key": "pile",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "The discard Pile, bottom to top.",
        "observable": true
      },
      {
        "key": "top_rank",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The rank of the Pile's top card, or 0 when the Pile is empty.",
        "observable": true
      },
      {
        "key": "run_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "How many cards of the top rank lie in a row on top of the Pile.",
        "observable": true
      },
      {
        "key": "removed",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Cards removed from the game by run clears and Clears.",
        "observable": false
      },
      {
        "key": "history",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "The full public log of plays and pickups.",
        "observable": false
      },
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The current round number.",
        "observable": true
      },
      {
        "key": "players_out",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The number of players with out = true.",
        "observable": true
      }
    ]
  },
  "setup": [
    "Seats are assigned in random (seeded) order. Seat 1 is First, seat 2 is Second and seat 3 is Third, and turn order is seat 1, 2, 3 in every round.",
    "low_stack, mid_stack and high_stack are each shuffled separately. Drawing at random from a stack is the shuffle.",
    "Each player draws 3 cards at random from low_stack, 3 from mid_stack and 3 from high_stack, and takes 1 card from clear_stack. Each card is appended to that player's hand and removed from its stack. Every stack ends empty and each hand holds 10 cards.",
    "Each player privately sees their own hand.",
    "Up pile selection, done simultaneously by poll: three successive polls ask every player at once to choose one card from their own hand. Each chosen card moves from hand to up_choice (visible only to the owner), so nobody sees another player's choice until all three picks are made.",
    "When every player has 3 cards in up_choice, each up_choice is copied to up_pile (public) and emptied. All Up piles are announced to everyone.",
    "Every player gets hand_count = 7, up_count = 3, cards_left = 10, picked_up = 0 and out = false.",
    "The table starts with pile = [], top_rank = 0, run_count = 0, removed = [], round = 0 and players_out = 0."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round += 1; announce the round number, pile, top_rank, run_count, every up_pile, hand_count and picked_up."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "short text (one message)",
      "effect": "Every message is shown to everyone at once: broadcast {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"}. No state changes and nothing binds."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player receives their own hand, plus the public pile, top_rank, run_count, up_piles, hand_counts and picked_up counts."
    },
    {
      "action": "ask",
      "who": "seat 1 (First), when out = false",
      "answer": "one choice from the offered list: 'pick up', 'play Clear' (only if the source holds a C), or 'play K x rank R' for each rank R held in the source with R >= top_rank (any rank if the pile is empty) and each K from 1 to the number of R cards held. The source is hand if hand_count > 0, otherwise up_pile.",
      "effect": "Records the chosen action. An illegal or unreadable answer counts as 'pick up'."
    },
    {
      "action": "update",
      "who": "seat 1 (First), when out = false",
      "answer": null,
      "effect": "PICK UP: append every pile card to hand; picked_up += len(pile); pile = []; top_rank = 0; run_count = 0. PLAY K x R: remove K R cards from the source and append them to pile; if R == top_rank then run_count += K, else run_count = K; top_rank = R; if run_count >= 3, move all pile cards to removed, set pile = [], top_rank = 0, run_count = 0. PLAY Clear: move the C and all pile cards to removed; pile = []; top_rank = 0; run_count = 0. Then recompute hand_count, up_count and cards_left = hand_count + up_count; out = (cards_left == 0); append the action to history; announce it."
    },
    {
      "action": "ask",
      "who": "seat 2 (Second), when out = false",
      "answer": "as for seat 1, against the current pile",
      "effect": "Records the chosen action. An illegal or unreadable answer counts as 'pick up'."
    },
    {
      "action": "update",
      "who": "seat 2 (Second), when out = false",
      "answer": null,
      "effect": "Resolved exactly as for seat 1."
    },
    {
      "action": "ask",
      "who": "seat 3 (Third), when out = false",
      "answer": "as for seat 1, against the current pile",
      "effect": "Records the chosen action. An illegal or unreadable answer counts as 'pick up'."
    },
    {
      "action": "update",
      "who": "seat 3 (Third), when out = false",
      "answer": null,
      "effect": "Resolved exactly as for seat 1."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "players_out = the number of players with out = true."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if players_out >= 1 or round >= 40; otherwise continue to the next round."
    }
  ],
  "ending": {
    "condition": "players_out >= 1 or round >= 40 (checked only after seat 3's turn)",
    "rank_by": "you.out * 1000000 - you.cards_left * 10000 - you.picked_up",
    "decided_by": "If any player is out at the end of the round, only the out players can win, and among them the lowest picked_up wins; out players tied on picked_up share the result (a draw). If round 40 ends with nobody out, the fewest cards_left wins, then the lowest picked_up, and players still tied share the result (a draw)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game is set up, there are 30 cards: three each of ranks 1 to 9 and three Clears."
    },
    {
      "id": "R2",
      "text": "When cards are dealt, each player gets 3 cards from Low (ranks 1-3), 3 from Mid (4-6), 3 from High (7-9) and 1 Clear, 10 cards in all, and every stack ends empty."
    },
    {
      "id": "R3",
      "text": "When Up piles are chosen, every player chooses exactly 3 of their own cards simultaneously; all Up piles are then made public and each hand holds 7 cards."
    },
    {
      "id": "R4",
      "text": "When setup ends, pile is empty, top_rank = 0, run_count = 0 and every picked_up = 0."
    },
    {
      "id": "R5",
      "text": "When a round starts, every player writes one message at the same time, and all messages are shown to everyone only after all are in."
    },
    {
      "id": "R6",
      "text": "When it is a player's turn, seats act in order 1 (First), 2 (Second), 3 (Third), and a player with cards_left = 0 skips the turn."
    },
    {
      "id": "R7",
      "text": "When a player has hand_count > 0, they may play only from hand; when hand_count = 0, they play from up_pile."
    },
    {
      "id": "R8",
      "text": "When a player plays numbered cards, all cards are of one rank and from one source, and the play is legal only if the pile is empty or the rank >= top_rank (e.g., on top_rank 5, a 5 or 9 is legal and a 4 is not)."
    },
    {
      "id": "R9",
      "text": "When a player plays K cards of rank R equal to top_rank, run_count increases by K; when R differs from top_rank, run_count becomes K and top_rank becomes R."
    },
    {
      "id": "R10",
      "text": "When run_count reaches 3 or more, all pile cards go to removed, the pile empties, and top_rank and run_count become 0."
    },
    {
      "id": "R11",
      "text": "When a player plays a Clear, it is played alone and is always legal; the Clear and the whole pile go to removed, and top_rank and run_count become 0."
    },
    {
      "id": "R12",
      "text": "When a player picks up, every pile card moves to their hand, picked_up increases by the number of cards taken, and pile, top_rank and run_count reset to empty/0; picking up an empty pile changes nothing."
    },
    {
      "id": "R13",
      "text": "When a player may legally play, they may still choose to pick up."
    },
    {
      "id": "R14",
      "text": "When a player's answer is illegal or unreadable, it is resolved as a pick up."
    },
    {
      "id": "R15",
      "text": "When seat 3's turn ends and exactly one player has cards_left = 0, that player wins."
    },
    {
      "id": "R16",
      "text": "When seat 3's turn ends and two or three players have cards_left = 0, the one among them with the lowest picked_up wins, and a tie on picked_up is a draw between them."
    },
    {
      "id": "R17",
      "text": "When a player empties mid-round, the round still continues to seat 3 before any end check."
    },
    {
      "id": "R18",
      "text": "When round 40 ends with nobody out, the fewest cards_left wins, ties are broken by the lowest picked_up, and a remaining tie is a draw."
    }
  ],
  "offers": [
    {
      "question": "Talk message each round",
      "who": "all players (including out players)",
      "options": "One short free-text message."
    },
    {
      "question": "Up pile pick (setup, three simultaneous polls)",
      "who": "every seat",
      "options": "Any one card still in their own hand."
    },
    {
      "question": "Turn action",
      "who": "the seat whose turn it is, if out = false; an out seat is not asked",
      "options": "Always 'pick up'. 'play Clear' if the source (hand if non-empty, else up_pile) holds a C. 'play K x rank R' for each rank R in the source with R >= top_rank (any rank when the pile is empty), with K from 1 to the count of R cards in that source. Cards from the other source are never offered."
    }
  ],
  "choices": [
    {
      "what": "Exactly 3 players, suggested 3",
      "why": "The designer fixed the table at three: three ranked seats in a turn order, and an end check written for one, two or three emptied players."
    },
    {
      "what": "The talk round is a simultaneous poll with broadcast",
      "why": "The rules say messages are written at the same moment. Talk earns its place because players want opposite things (each wants the others to pick up) and can try to coax a rival into taking the Pile."
    },
    {
      "what": "Random seating maps to seat numbers 1, 2, 3 as First, Second, Third",
      "why": "The engine's seeded random seating gives the random order the rules ask for."
    },
    {
      "what": "Up pile chosen by three successive simultaneous polls into a private up_choice list, revealed afterwards",
      "why": "A single answer is one choice; three picks kept hidden until all are done keep the choice simultaneous."
    },
    {
      "what": "rank_by = out*1000000 - cards_left*10000 - picked_up",
      "why": "Out players rank above all others, then fewer cards, then fewer picked up. picked_up cannot reach 10000 in 40 rounds (at most 40 pickups of 27 cards), so the weights never overlap."
    },
    {
      "what": "Cards are written as text '1'..'9' and 'C'; top_rank is 0 for an empty pile",
      "why": "Gives the legality check a simple arithmetic comparison."
    }
  ],
  "simplifications": [
    {
      "what": "A draw is represented as all tied top players sharing the win",
      "why": "The engine has no separate draw; players level at the top share the result, and the other players still lose."
    },
    {
      "what": "Each seat's turn is written as its own ask plus update steps, in fixed seat order",
      "why": "Each play must resolve before the next seat chooses, against the current pile."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: up_pile, hand_count, up_count, cards_left, picked_up, out; table: pile, top_rank, run_count, round, players_out.
````

## Reply

````
[
{"name":"R1 setup holds 30 cards: 7 in hand and 3 up per seat, all stacks emptied","rule":"R1","players":3,"seed":1,"rounds":0,"default":"decline","rules":[],
 "expect":{"lens":{"game":{"low_stack":0,"mid_stack":0,"high_stack":0,"clear_stack":0,"pile":0},
   "players":{"1":{"hand":7,"up_pile":3},"2":{"hand":7,"up_pile":3},"3":{"hand":7,"up_pile":3}}},
   "players":{"1":{"cards_left":10},"2":{"cards_left":10},"3":{"cards_left":10}}}},
{"name":"R2 each player is dealt 10 cards and every stack ends empty","rule":"R2","players":3,"seed":2,"rounds":0,"default":"decline","rules":[],
 "expect":{"lens":{"game":{"low_stack":0,"mid_stack":0,"high_stack":0,"clear_stack":0}},
   "players":{"1":{"hand_count":7,"up_count":3,"cards_left":10},"2":{"hand_count":7,"up_count":3,"cards_left":10},"3":{"hand_count":7,"up_count":3,"cards_left":10}}}},
{"name":"R3 every seat has a public Up pile of 3 and a hand of 7 after selection","rule":"R3","players":3,"seed":3,"rounds":0,"default":"decline","rules":[],
 "expect":{"lens":{"players":{"1":{"up_pile":3,"up_choice":0,"hand":7},"2":{"up_pile":3,"up_choice":0,"hand":7},"3":{"up_pile":3,"up_choice":0,"hand":7}}},
   "players":{"1":{"hand_count":7,"up_count":3},"2":{"hand_count":7,"up_count":3},"3":{"hand_count":7,"up_count":3}}}},
{"name":"R4 table starts empty with zero counters","rule":"R4","players":3,"seed":4,"rounds":0,"default":"decline","rules":[],
 "expect":{"game":{"pile":[],"top_rank":0,"run_count":0,"round":0,"players_out":0},
   "players":{"1":{"picked_up":0,"out":false},"2":{"picked_up":0,"out":false},"3":{"picked_up":0,"out":false}}}},
{"name":"R5 a round with talk then three pickups of an empty pile changes nothing but the round","rule":"R5","players":3,"seed":5,"rounds":1,"default":"decline",
 "given":{"players":{"1":{"hand":["5"],"up_pile":["1","2","3"],"hand_count":1,"up_count":3,"cards_left":4,"picked_up":0},
   "2":{"hand":["6"],"up_pile":["1","2","3"],"hand_count":1,"up_count":3,"cards_left":4,"picked_up":0},
   "3":{"hand":["7"],"up_pile":["1","2","3"],"hand_count":1,"up_count":3,"cards_left":4,"picked_up":0}},
   "game":{"pile":[],"top_rank":0,"run_count":0,"round":0}},
 "rules":[{"seat":1,"options_include":"pick up"},{"seat":2,"options_include":"pick up"},{"seat":3,"options_include":"pick up"}],
 "expect":{"game":{"round":1,"pile":[],"top_rank":0,"players_out":0},
   "players":{"1":{"cards_left":4,"picked_up":0},"2":{"cards_left":4,"picked_up":0},"3":{"cards_left":4,"picked_up":0}}}},
{"name":"R6 seats play in order 1, 2, 3","rule":"R6","players":3,"seed":6,"rounds":1,"default":"decline",
 "given":{"players":{"1":{"hand":["5","8"],"up_pile":["1","2","3"],"hand_count":2,"up_count":3,"cards_left":5},
   "2":{"hand":["6","9"],"up_pile":["1","2","3"],"hand_count":2,"up_count":3,"cards_left":5},
   "3":{"hand":["7","4"],"up_pile":["1","2","3"],"hand_count":2,"up_count":3,"cards_left":5}},
   "game":{"pile":[],"top_rank":0,"run_count":0}},
 "rules":[{"seat":1,"options_include":"play 1 x rank 5"},{"seat":2,"options_include":"play 1 x rank 6"},{"seat":3,"options_include":"play 1 x rank 7"}],
 "expect":{"game":{"pile":["5","6","7"],"top_rank":7,"run_count":1},
   "players":{"1":{"hand_count":1,"cards_left":4},"2":{"hand_count":1,"cards_left":4},"3":{"hand_count":1,"cards_left":4}},
   "not_offered":[{"seat":3,"option":"play 1 x rank 4"}]}},
{"name":"R6 a seat with no cards left is skipped","rule":"R6","players":3,"seed":7,"rounds":1,"default":"decline",
 "given":{"players":{"1":{"hand":["5","8"],"up_pile":["1","2","3"],"hand_count":2,"up_count":3,"cards_left":5,"picked_up":0},
   "2":{"hand":[],"up_pile":[],"hand_count":0,"up_count":0,"cards_left":0,"out":true,"picked_up":0},
   "3":{"hand":["7","4"],"up_pile":["1","2","3"],"hand_count":2,"up_count":3,"cards_left":5,"picked_up":0}},
   "game":{"pile":[],"top_rank":0,"run_count":0}},
 "rules":[{"seat":1,"options_include":"play 1 x rank 5"},{"seat":3,"options_include":"play 1 x rank 7"}],
 "expect":{"winner":2,"game":{"pile":["5","7"],"top_rank":7,"players_out":1},
   "players":{"2":{"cards_left":0,"picked_up":0,"out":true}},
   "not_offered":[{"seat":2,"option":"pick up"}]}},
{"name":"R7 with cards in hand only hand cards are offered","rule":"R7","players":3,"seed":8,"rounds":1,"default":"decline",
 "given":{"players":{"1":{"hand":["4"],"up_pile":["9","9","2"],"hand_count":1,"up_count":3,"cards_left":4,"picked_up":0}},
   "game":{"pile":[],"top_rank":0,"run_count":0}},
 "rules":[{"seat":1,"options_include":"play 1 x rank 4"},{"seat":2,"options_include":"pick up"},{"seat":3,"options_include":"pick up"}],
 "expect":{"players":{"1":{"hand_count":0,"up_count":3,"cards_left":3,"up_pile":["9","9","2"]}},
   "not_offered":[{"seat":1,"option":"play 1 x rank 9"},{"seat":1,"option":"play 1 x rank 2"}]}},
{"name":"R7 with an empty hand the seat plays from its Up pile","rule":"R7","players":3,"seed":9,"rounds":1,"default":"decline",
 "given":{"players":{"1":{"hand":[],"up_pile":["9","9","2"],"hand_count":0,"up_count":3,"cards_left":3,"picked_up":0}},
   "game":{"pile":["5"],"top_rank":5,"run_count":1}},
 "rules":[{"seat":1,"options_include":"play 2 x rank 9"},{"seat":2,"options_include":"pick up"},{"seat":3,"options_include":"pick up"}],
 "expect":{"players":{"1":{"hand_count":0,"up_count":1,"cards_left":1,"up_pile":["2"]}},
   "not_offered":[{"seat":1,"option":"play 1 x rank 2"}]}},
{"name":"R8 on top rank 5 a 5 or 9 is offered and a 4 is not","rule":"R8","players":3,"seed":10,"rounds":1,"default":"decline",
 "given":{"players":{"1":{"hand":["4","5","9"],"up_pile":["1","2","3"],"hand_count":3,"up_count":3,"cards_left":6,"picked_up":0},
   "2":{"hand":["1"],"up_pile":["1","2","3"],"hand_count":1,"up_count":3,"cards_left":4,"picked_up":0},
   "3":{"hand":["1"],"up_pile":["1","2","3"],"hand_count":1,"up_count":3,"cards_left":4,"picked_up":0}},
   "game":{"pile":["5"],"top_rank":5,"run_count":1}},
 "rules":[{"seat":1,"options_include":"play 1 x rank 9"},{"seat":2,"options_include":"pick up"},{"seat":3,"options_include":"pick up"}],
 "expect":{"players":{"1":{"hand_count":2,"cards_left":5},"2":{"picked_up":2,"hand_count":3,"cards_left":6}},
   "game":{"pile":[],"top_rank":0,"run_count":0},
   "offered":[{"seat":1,"option":"play 1 x rank 5"},{"seat":1,"option":"play 1 x rank 9"}],
   "not_offered":[{"seat":1,"option":"play 1 x rank 4"}]}},
{"name":"R9 same rank raises run_count, a new rank resets it","rule":"R9","players":3,"seed":11,"rounds":1,"default":"decline",
 "given":{"players":{"1":{"hand":["6","1"],"up_pile":["1","2","3"],"hand_count":2,"up_count":3,"cards_left":5},
   "2":{"hand":["8","2"],"up_pile":["1","2","3"],"hand_count":2,"up_count":3,"cards_left":5},
   "3":{"hand":["8","1"],"up_pile":["1","2","3"],"hand_count":2,"up_count":3,"cards_left":5}},
   "game":{"pile":["6"],"top_rank":6,"run_count":1}},
 "rules":[{"seat":1,"options_include":"play 1 x rank 6"},{"seat":2,"options_include":"play 1 x rank 8"},{"seat":3,"options_include":"play 1 x rank 8"}],
 "expect":{"game":{"pile":["6","6","8","8"],"top_rank":8,"run_count":2}}},
{"name":"R10 a third card of the top rank clears the pile","rule":"R10","players":3,"seed":12,"rounds":1,"default":"decline",
 "given":{"players":{"1":{"hand":["7","9"],"up_pile":["1","2","3"],"hand_count":2,"up_count":3,"cards_left":5},
   "2":{"hand":["3","4"],"up_pile":["1","2","3"],"hand_count":2,"up_count":3,"cards_left":5},
   "3":{"hand":["5","1"],"up_pile":["1","2","3"],"hand_count":2,"up_count":3,"cards_left":5}},
   "game":{"pile":["7","7"],"top_rank":7,"run_count":2}},
 "rules":[{"seat":1,"options_include":"play 1 x rank 7"},{"seat":2,"options_include":"play 1 x rank 3"},{"seat":3,"options_include":"play 1 x rank 5"}],
 "expect":{"game":{"pile":["3","5"],"top_rank":5,"run_count":1},
   "players":{"1":{"hand_count":1,"cards_left":4}},
   "offered":[{"seat":2,"option":"play 1 x rank 3"}]}},
{"name":"R10 playing three of a new rank at once clears the pile","rule":"R10","players":3,"seed":13,"rounds":1,"default":"decline",
 "given":{"players":{"1":{"hand":["5","5","5"],"up_pile":["1","2","3"],"hand_count":3,"up_count":3,"cards_left":6,"picked_up":0},
   "2":{"hand":["1"],"up_pile":["1","2","3"],"hand_count":1,"up_count":3,"cards_left":4,"picked_up":0},
   "3":{"hand":["1"],"up_pile":["1","2","3"],"hand_count":1,"up_count":3,"cards_left":4,"picked_up":0}},
   "game":{"pile":["2"],"top_rank":2,"run_count":1}},
 "rules":[{"seat":1,"options_include":"play 3 x rank 5"},{"seat":2,"options_include":"pick up"},{"seat":3,"options_include":"pick up"}],
 "expect":{"game":{"pile":[],"top_rank":0,"run_count":0},
   "players":{"1":{"hand_count":0,"up_count":3,"cards_left":3},"2":{"picked_up":0,"hand_count":1},"3":{"picked_up":0,"hand_count":1}}}},
{"name":"R11 a Clear is always offered and removes the whole pile","rule":"R11","players":3,"seed":14,"rounds":1,"default":"decline",
 "given":{"players":{"1":{"hand":["C","2"],"up_pile":["1","2","3"],"hand_count":2,"up_count":3,"cards_left":5},
   "2":{"hand":["1","6"],"up_pile":["1","2","3"],"hand_count":2,"up_count":3,"cards_left":5},
   "3":{"hand":["4","1"],"up_pile":["1","2","3"],"hand_count":2,"up_count":3,"cards_left":5}},
   "game":{"pile":["8","9"],"top_rank":9,"run_count":1}},
 "rules":[{"seat":1,"options_include":"play Clear"},{"seat":2,"options_include":"play 1 x rank 1"},{"seat":3,"options_include":"play 1 x rank 4"}],
 "expect":{"game":{"pile":["1","4"],"top_rank":4,"run_count":1},
   "players":{"1":{"hand_count":1,"cards_left":4}},
   "not_offered":[{"seat":1,"option":"play 1 x rank 2"}]}},
{"name":"R12 picking up takes the pile; picking up an empty pile changes nothing","rule":"R12","players":3,"seed":15,"rounds":1,"default":"decline",
 "given":{"players":{"1":{"hand":["2"],"up_pile":["1","2","3"],"hand_count":1,"up_count":3,"cards_left":4,"picked_up":0},
   "2":{"hand":["6"],"up_pile":["1","2","3"],"hand_count":1,"up_count":3,"cards_left":4,"picked_up":2},
   "3":{"hand":["7"],"up_pile":["1","2","3"],"hand_count":1,"up_count":3,"cards_left":4,"picked_up":0}},
   "game":{"pile":["3","5","5"],"top_rank":5,"run_count":2}},
 "rules":[{"seat":1,"options_include":"pick up"},{"seat":2,"options_include":"pick up"},{"seat":3,"options_include":"pick up"}],
 "expect":{"game":{"pile":[],"top_rank":0,"run_count":0},
   "players":{"1":{"picked_up":3,"hand_count":4,"cards_left":7},"2":{"picked_up":2,"hand_count":1,"cards_left":4},"3":{"picked_up":0,"hand_count":1,"cards_left":4}}}},
{"name":"R13 a seat that could play may pick up instead","rule":"R13","players":3,"seed":16,"rounds":1,"default":"decline",
 "given":{"players":{"1":{"hand":["9"],"up_pile":["1","2","3"],"hand_count":1,"up_count":3,"cards_left":4,"picked_up":0},
   "2":{"hand":["6"],"up_pile":["1","2","3"],"hand_count":1,"up_count":3,"cards_left":4,"picked_up":0},
   "3":{"hand":["7"],"up_pile":["1","2","3"],"hand_count":1,"up_count":3,"cards_left":4,"picked_up":0}},
   "game":{"pile":["4"],"top_rank":4,"run_count":1}},
 "rules":[{"seat":1,"options_include":"pick up"},{"seat":2,"options_include":"pick up"},{"seat":3,"options_include":"pick up"}],
 "expect":{"game":{"pile":[],"top_rank":0},
   "players":{"1":{"picked_up":1,"hand_count":2,"cards_left":5}},
   "offered":[{"seat":1,"option":"play 1 x rank 9"}]}},
{"name":"R15 the only seat that empties wins","rule":"R15","players":3,"seed":17,"default":"decline",
 "given":{"players":{"1":{"hand":[],"up_pile":["9"],"hand_count":0,"up_count":1,"cards_left":1,"picked_up":5},
   "2":{"hand":["2","3"],"up_pile":["4","5","6"],"hand_count":2,"up_count":3,"cards_left":5,"picked_up":0},
   "3":{"hand":["1"],"up_pile":["7","8","8"],"hand_count":1,"up_count":3,"cards_left":4,"picked_up":0}},
   "game":{"pile":[],"top_rank":0,"run_count":0,"round":0}},
 "rules":[{"seat":1,"options_include":"play 1 x rank 9"},{"seat":2,"options_include":"pick up"},{"seat":3,"options_include":"pick up"}],
 "expect":{"winner":1,"standings":{"1":999995,"2":-60001,"3":-40000},
   "players":{"1":{"out":true,"cards_left":0},"2":{"picked_up":1,"cards_left":6}},
   "game":{"players_out":1,"round":1}}},
{"name":"R16 of two seats that empty, the lower picked_up wins","rule":"R16","players":3,"seed":18,"default":"decline",
 "given":{"players":{"1":{"hand":[],"up_pile":["9"],"hand_count":0,"up_count":1,"cards_left":1,"picked_up":4},
   "2":{"hand":[],"up_pile":["9"],"hand_count":0,"up_count":1,"cards_left":1,"picked_up":2},
   "3":{"hand":["1"],"up_pile":["2","3","4"],"hand_count":1,"up_count":3,"cards_left":4,"picked_up":0}},
   "game":{"pile":[],"top_rank":0,"run_count":0,"round":0}},
 "rules":[{"seat":1,"options_include":"play 1 x rank 9"},{"seat":2,"options_include":"play 1 x rank 9"},{"seat":3,"options_include":"pick up"}],
 "expect":{"winner":2,"standings":{"1":999996,"2":999998,"3":-60002},
   "players":{"1":{"out":true},"2":{"out":true},"3":{"picked_up":2,"cards_left":6}},
   "game":{"players_out":2}}},
{"name":"R16 two emptied seats tied on picked_up share the win","rule":"R16","players":3,"seed":19,"default":"decline",
 "given":{"players":{"1":{"hand":[],"up_pile":["9"],"hand_count":0,"up_count":1,"cards_left":1,"picked_up":3},
   "2":{"hand":[],"up_pile":["9"],"hand_count":0,"up_count":1,"cards_left":1,"picked_up":3},
   "3":{"hand":["1"],"up_pile":["2","3","4"],"hand_count":1,"up_count":3,"cards_left":4,"picked_up":0}},
   "game":{"pile":[],"top_rank":0,"run_count":0,"round":0}},
 "rules":[{"seat":1,"options_include":"play 1 x rank 9"},{"seat":2,"options_include":"play 1 x rank 9"},{"seat":3,"options_include":"pick up"}],
 "expect":{"winner":[1,2],"standings":{"1":999997,"2":999997,"3":-60002},"game":{"players_out":2}}},
{"name":"R17 after seat 1 empties, seats 2 and 3 still take their turns","rule":"R17","players":3,"seed":20,"default":"decline",
 "given":{"players":{"1":{"hand":[],"up_pile":["5"],"hand_count":0,"up_count":1,"cards_left":1,"picked_up":0},
   "2":{"hand":["6","2"],"up_pile":["1","2","3"],"hand_count":2,"up_count":3,"cards_left":5,"picked_up":0},
   "3":{"hand":["7","1"],"up_pile":["1","2","3"],"hand_count":2,"up_count":3,"cards_left":5,"picked_up":0}},
   "game":{"pile":[],"top_rank":0,"run_count":0,"round":0}},
 "rules":[{"seat":1,"options_include":"play 1 x rank 5"},{"seat":2,"options_include":"play 1 x rank 6"},{"seat":3,"options_include":"play 1 x rank 7"}],
 "expect":{"winner":1,"game":{"pile":["5","6","7"],"top_rank":7,"round":1,"players_out":1},
   "players":{"1":{"out":true,"cards_left":0},"2":{"cards_left":4},"3":{"cards_left":4}},
   "offered":[{"seat":2,"option":"play 1 x rank 6"},{"seat":3,"option":"play 1 x rank 7"}]}},
{"name":"R18 at round 40 with nobody out, fewest cards then lowest picked_up wins","rule":"R18","players":3,"seed":21,"default":"decline",
 "given":{"players":{"1":{"hand":["5"],"up_pile":["1","2"],"hand_count":1,"up_count":2,"cards_left":3,"picked_up":5},
   "2":{"hand":["6"],"up_pile":["1","2"],"hand_count":1,"up_count":2,"cards_left":3,"picked_up":2},
   "3":{"hand":["7"],"up_pile":["1","2","3"],"hand_count":1,"up_count":3,"cards_left":4,"picked_up":0}},
   "game":{"pile":[],"top_rank":0,"run_count":0,"round":39}},
 "rules":[{"seat":1,"options_include":"pick up"},{"seat":2,"options_include":"pick up"},{"seat":3,"options_include":"pick up"}],
 "expect":{"winner":2,"standings":{"1":-30005,"2":-30002,"3":-40000},"game":{"round":40,"players_out":0}}},
{"name":"R18 at round 40 a full tie on cards and picked_up is shared","rule":"R18","players":3,"seed":22,"default":"decline",
 "given":{"players":{"1":{"hand":["5"],"up_pile":["1","2"],"hand_count":1,"up_count":2,"cards_left":3,"picked_up":2},
   "2":{"hand":["6"],"up_pile":["1","2"],"hand_count":1,"up_count":2,"cards_left":3,"picked_up":2},
   "3":{"hand":["7"],"up_pile":["1","2","3"],"hand_count":1,"up_count":3,"cards_left":4,"picked_up":0}},
   "game":{"pile":[],"top_rank":0,"run_count":0,"round":39}},
 "rules":[{"seat":1,"options_include":"pick up"},{"seat":2,"options_include":"pick up"},{"seat":3,"options_include":"pick up"}],
 "expect":{"winner":[1,2],"standings":{"1":-30002,"2":-30002,"3":-40000},"game":{"round":40}}}
]
````
