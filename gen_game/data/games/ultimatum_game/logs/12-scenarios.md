# 12 scenarios

- time: 2026-10-27T21:44:28+00:00 (69.8s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 7775364d0e7e525c, reply sha256 98eee38b1d5bab15

## Sent

````
SPEC:
{
  "name": "Hidden Pie Ultimatum III",
  "summary": "Three players take turns as Proposer over 12 rounds. Each Proposer splits a pot that only they can see between two Responders, and the deal passes if at least one Responder accepts.",
  "players": {
    "min": 3,
    "max": 3,
    "suggested": 3
  },
  "parameters": {
    "rounds": 12,
    "player_count": 3,
    "pot_value_1": 70,
    "pot_value_2": 90,
    "pot_value_3": 110,
    "pot_value_4": 130,
    "max_offer_total": 130,
    "min_offer": 0,
    "proposals_per_player": 4,
    "initial_score": 0,
    "rounds_per_block": 3
  },
  "attributes": {
    "player": [
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Total points gained so far.",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Current round number, 1 to 12.",
        "observable": true
      },
      {
        "key": "proposer",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat of this round's Proposer.",
        "observable": true
      },
      {
        "key": "responder1",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "First Responder this round, the lower-numbered seat of the two non-Proposers.",
        "observable": false
      },
      {
        "key": "responder2",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Second Responder this round, the higher-numbered seat of the two non-Proposers.",
        "observable": false
      },
      {
        "key": "pots_p1",
        "type": "list",
        "visible": "none",
        "initial": [
          70,
          90,
          110,
          130
        ],
        "meaning": "Pot values P1 has not yet played as Proposer.",
        "observable": false
      },
      {
        "key": "pots_p2",
        "type": "list",
        "visible": "none",
        "initial": [
          70,
          90,
          110,
          130
        ],
        "meaning": "Pot values P2 has not yet played as Proposer.",
        "observable": false
      },
      {
        "key": "pots_p3",
        "type": "list",
        "visible": "none",
        "initial": [
          70,
          90,
          110,
          130
        ],
        "meaning": "Pot values P3 has not yet played as Proposer.",
        "observable": false
      },
      {
        "key": "pot",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "This round's pot. Only the Proposer is told it before the reveal.",
        "observable": false
      },
      {
        "key": "offer_a",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Amount offered to the first Responder.",
        "observable": true
      },
      {
        "key": "offer_b",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Amount offered to the second Responder.",
        "observable": true
      },
      {
        "key": "response1",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "First Responder's choice, Accept or Reject, shown at the reveal.",
        "observable": true
      },
      {
        "key": "response2",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Second Responder's choice, Accept or Reject, shown at the reveal.",
        "observable": true
      }
    ]
  },
  "setup": [
    "Seats 1, 2 and 3 are P1, P2 and P3, and each starts with score 0.",
    "The table lists pots_p1, pots_p2 and pots_p3 each hold the values 70, 90, 110 and 130.",
    "Everyone is told that each player's pot list starts as 70, 90, 110 and 130, and that each value is used exactly once when that player proposes.",
    "Everyone is told the Proposer order: rounds 1-3 are P1, P2, P3; rounds 4-6 are P3, P2, P1; rounds 7-9 are P1, P2, P3; rounds 10-12 are P3, P2, P1."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round += 1. Let k = (round-1) div 3 and j = (round-1) mod 3. proposer = j+1 if k is even, otherwise 3-j. responder1 = 2 if proposer == 1, else 1. responder2 = 2 if proposer == 3, else 3. Announce the round, the proposer, responder1 and responder2."
    },
    {
      "action": "update",
      "who": "seat proposer",
      "answer": null,
      "effect": "Draw: pick one value at random from pots_p{proposer}, set pot to it, and remove it from pots_p{proposer}."
    },
    {
      "action": "tell",
      "who": "seat proposer",
      "answer": null,
      "effect": "Privately tell the Proposer: 'This round's pot is {pot}.'"
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "short text message",
      "effect": "All messages are collected at the same time, then broadcast to all as 'Seat {seat} says: {value}'. Messages are not binding."
    },
    {
      "action": "ask",
      "who": "seat proposer",
      "answer": "whole number from 0 to 130",
      "effect": "offer_a = answer (the amount for responder1)."
    },
    {
      "action": "ask",
      "who": "seat proposer",
      "answer": "whole number from 0 to 130 - offer_a",
      "effect": "offer_b = answer (the amount for responder2), so that offer_a + offer_b <= 130."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce: 'Seat {proposer} offers {offer_a} to Seat {responder1} and {offer_b} to Seat {responder2}.' The pot is not shown."
    },
    {
      "action": "poll",
      "who": "seat responder1 and seat responder2",
      "answer": "Accept or Reject",
      "effect": "response1 = responder1's choice and response2 = responder2's choice. Neither Responder sees the other's choice before answering."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "If response1 == Accept or response2 == Accept: the Proposer's score += pot - offer_a - offer_b (this may be negative); if response1 == Accept, responder1's score += offer_a; if response2 == Accept, responder2's score += offer_b. If both are Reject, no score changes."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Reveal: 'The pot was {pot}. Seat {responder1}: {response1}. Seat {responder2}: {response2}. Scores: P1 {score of seat 1}, P2 {score of seat 2}, P3 {score of seat 3}.'"
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if round >= 12; otherwise continue to the next round."
    }
  ],
  "ending": {
    "condition": "round >= 12",
    "rank_by": "you.score",
    "decided_by": "Each player's standing is their total score after round 12. The highest total wins. Players tied at the top share the result, which stands in for the source's draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game starts, then every player's score is 0 and each of pots_p1, pots_p2 and pots_p3 holds 70, 90, 110 and 130."
    },
    {
      "id": "R2",
      "text": "When the round is 1, 2 or 3, then the proposer is seat 1, 2 or 3 respectively."
    },
    {
      "id": "R3",
      "text": "When the round is 4, 5 or 6, then the proposer is seat 3, 2 or 1 respectively."
    },
    {
      "id": "R4",
      "text": "When the round is 7, 8 or 9, then the proposer is seat 1, 2 or 3 respectively."
    },
    {
      "id": "R5",
      "text": "When the round is 10, 11 or 12, then the proposer is seat 3, 2 or 1 respectively."
    },
    {
      "id": "R6",
      "text": "When the proposer is seat 1, then responder1 is seat 2 and responder2 is seat 3; when the proposer is seat 2, then they are seats 1 and 3; when the proposer is seat 3, then they are seats 1 and 2."
    },
    {
      "id": "R7",
      "text": "When a round begins, then one value is drawn at random from the proposer's pot list, set as pot, and removed from that list, so the list shrinks by 1."
    },
    {
      "id": "R8",
      "text": "When the game ends after 12 rounds, then every player has proposed exactly 4 times, has used each of 70, 90, 110 and 130 once, and has an empty pot list."
    },
    {
      "id": "R9",
      "text": "When the pot is drawn, then only the proposer is told its value before the reveal."
    },
    {
      "id": "R10",
      "text": "When the talk step runs, then every player submits one message at the same time and all three messages are shown to everyone afterwards."
    },
    {
      "id": "R11",
      "text": "When the proposer makes an offer, then offer_a and offer_b are whole numbers with offer_a >= 0, offer_b >= 0 and offer_a + offer_b <= 130."
    },
    {
      "id": "R12",
      "text": "When the offer is made, then offer_a and offer_b are shown to everyone and the pot is not."
    },
    {
      "id": "R13",
      "text": "When the Responders respond, then each chooses Accept or Reject at the same time without seeing the other's choice."
    },
    {
      "id": "R14",
      "text": "When both Responders accept, then the proposer gains pot - offer_a - offer_b, responder1 gains offer_a and responder2 gains offer_b (pot 110, offers 30 and 40: proposer +40, responders +30 and +40)."
    },
    {
      "id": "R15",
      "text": "When exactly one Responder accepts, then the proposer gains pot - offer_a - offer_b, the accepting Responder gains their offer, and the rejecting Responder gains 0 (pot 90, offers 30 and 40, only responder1 accepts: proposer +20, responder1 +30, responder2 +0)."
    },
    {
      "id": "R16",
      "text": "When the deal passes and offer_a + offer_b exceeds the pot, then the proposer's score goes down by the difference (pot 70, offers 50 and 50: proposer -30)."
    },
    {
      "id": "R17",
      "text": "When both Responders reject, then all three players gain 0 this round."
    },
    {
      "id": "R18",
      "text": "When a round's scoring is done, then the pot, both responses and all three scores are announced to everyone."
    },
    {
      "id": "R19",
      "text": "When round 12's scoring is done, then the game ends."
    },
    {
      "id": "R20",
      "text": "When the game ends, then the player with the highest score wins, and players tied for the highest score share the result."
    }
  ],
  "offers": [
    {
      "question": "Talk message",
      "who": "all three seats",
      "options": "any short text message"
    },
    {
      "question": "Offer for the first Responder (offer_a)",
      "who": "the proposer only",
      "options": "a whole number from 0 to 130"
    },
    {
      "question": "Offer for the second Responder (offer_b)",
      "who": "the proposer only",
      "options": "a whole number from 0 to 130 - offer_a"
    },
    {
      "question": "Response to the offer",
      "who": "responder1 and responder2 only (the proposer is not asked)",
      "options": "Accept, Reject"
    }
  ],
  "choices": [
    {
      "what": "3 players (min 3, max 3, suggested 3)",
      "why": "The designer fixed the table at 3. The Proposer order, the two-Responder structure and the 4 proposals each over 12 rounds only work with exactly 3 seats. The strategy is to infer the hidden pot from the offer size and from which values the Proposer has already used, to bluff about the pot in talk, and to decide whether to undercut a fellow Responder, since one acceptance is enough for the deal to pass."
    },
    {
      "what": "Talk is a simultaneous poll broadcast to all",
      "why": "The source requires all three messages to be written at the same time, unseen, and then shown to everyone. The players also disagree about the split, so talk earns its place."
    },
    {
      "what": "The pot lists are hidden table attributes (visibility none)",
      "why": "If the remaining lists were public, they would show the drawn pot the moment it is removed. Their contents are announced at setup, and every used value is revealed at the end of each round, so players can still track what remains, as the source intends."
    },
    {
      "what": "The offer is asked as two sequential numbers, with b's range limited to 130 - a",
      "why": "A question takes one number, and limiting b's range enforces a + b <= 130 by arithmetic."
    }
  ],
  "simplifications": [
    {
      "what": "A tie for the highest score is a shared win rather than a draw",
      "why": "The engine ranks by one expression and has players level at the top share the win, with no separate draw outcome. A sole leader still wins outright, as in the source."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: score; table: round, proposer, offer_a, offer_b, response1, response2.

EARLIER TESTS FOR THIS SPEC WERE FOUND WRONG. What to do differently:
When a scenario depends on both Responders rejecting, script that explicitly. Add rules for each Responder seat that choose the 'Reject' option every time it is offered, instead of relying on the 'decline' default, which here picked Accept. Then expect all three scores to stay 0, matching the rule for a failed deal. For the full-game R8 check, also assert that pots_p1, pots_p2 and pots_p3 are empty (length 0) and that each seat proposed 4 times. For the round-12 ending test, with both Responders scripted to Reject, the given scores stay unchanged and the winner follows from them. Do not let any expected score depend on which pot value is drawn, because the draw is random. Asserting only the score delta of the Proposer is fine only when the offer is accepted and the pot is known; otherwise assert that the scores are unchanged. For R10, a talk-only test should script rejections, or should not assert scores at all. The point of R10 is that the round completes after the simultaneous talk, so assert round/proposer progression rather than a score.
````

## Reply

````
```json
[
{"name":"Setup: all scores 0 and every pot list holds 4 values","rule":"R1","players":3,"rounds":0,
 "expect":{"players":{"1":{"score":0},"2":{"score":0},"3":{"score":0}},"game":{"round":0},
  "lens":{"game":{"pots_p1":4,"pots_p2":4,"pots_p3":4}}}},

{"name":"Round 1 proposer is seat 1","rule":"R2","players":3,"rounds":1,"default":"first",
 "rules":[{"seat":1,"options_include":0,"times":"all"},{"seat":2,"options_include":"Reject","times":"all"},{"seat":3,"options_include":"Reject","times":"all"}],
 "expect":{"game":{"round":1,"proposer":1},"players":{"1":{"score":0},"2":{"score":0},"3":{"score":0}},
  "not_offered":[{"seat":1,"option":"Accept"}]}},
{"name":"Round 2 proposer is seat 2","rule":"R2","players":3,"rounds":1,"default":"first","given":{"game":{"round":1}},
 "rules":[{"seat":2,"options_include":0,"times":"all"},{"seat":1,"options_include":"Reject","times":"all"},{"seat":3,"options_include":"Reject","times":"all"}],
 "expect":{"game":{"round":2,"proposer":2},"not_offered":[{"seat":2,"option":"Accept"}]}},
{"name":"Round 3 proposer is seat 3","rule":"R2","players":3,"rounds":1,"default":"first","given":{"game":{"round":2}},
 "rules":[{"seat":3,"options_include":0,"times":"all"},{"seat":1,"options_include":"Reject","times":"all"},{"seat":2,"options_include":"Reject","times":"all"}],
 "expect":{"game":{"round":3,"proposer":3},"not_offered":[{"seat":3,"option":"Accept"}]}},

{"name":"Round 4 proposer is seat 3","rule":"R3","players":3,"rounds":1,"default":"first","given":{"game":{"round":3}},
 "rules":[{"seat":3,"options_include":0,"times":"all"},{"seat":1,"options_include":"Reject","times":"all"},{"seat":2,"options_include":"Reject","times":"all"}],
 "expect":{"game":{"round":4,"proposer":3},"not_offered":[{"seat":3,"option":"Accept"}]}},
{"name":"Round 5 proposer is seat 2","rule":"R3","players":3,"rounds":1,"default":"first","given":{"game":{"round":4}},
 "rules":[{"seat":2,"options_include":0,"times":"all"},{"seat":1,"options_include":"Reject","times":"all"},{"seat":3,"options_include":"Reject","times":"all"}],
 "expect":{"game":{"round":5,"proposer":2},"not_offered":[{"seat":2,"option":"Accept"}]}},
{"name":"Round 6 proposer is seat 1","rule":"R3","players":3,"rounds":1,"default":"first","given":{"game":{"round":5}},
 "rules":[{"seat":1,"options_include":0,"times":"all"},{"seat":2,"options_include":"Reject","times":"all"},{"seat":3,"options_include":"Reject","times":"all"}],
 "expect":{"game":{"round":6,"proposer":1},"not_offered":[{"seat":1,"option":"Accept"}]}},

{"name":"Round 7 proposer is seat 1","rule":"R4","players":3,"rounds":1,"default":"first","given":{"game":{"round":6}},
 "rules":[{"seat":1,"options_include":0,"times":"all"},{"seat":2,"options_include":"Reject","times":"all"},{"seat":3,"options_include":"Reject","times":"all"}],
 "expect":{"game":{"round":7,"proposer":1}}},
{"name":"Round 8 proposer is seat 2","rule":"R4","players":3,"rounds":1,"default":"first","given":{"game":{"round":7}},
 "rules":[{"seat":2,"options_include":0,"times":"all"},{"seat":1,"options_include":"Reject","times":"all"},{"seat":3,"options_include":"Reject","times":"all"}],
 "expect":{"game":{"round":8,"proposer":2}}},
{"name":"Round 9 proposer is seat 3","rule":"R4","players":3,"rounds":1,"default":"first","given":{"game":{"round":8}},
 "rules":[{"seat":3,"options_include":0,"times":"all"},{"seat":1,"options_include":"Reject","times":"all"},{"seat":2,"options_include":"Reject","times":"all"}],
 "expect":{"game":{"round":9,"proposer":3}}},

{"name":"Round 10 proposer is seat 3","rule":"R5","players":3,"rounds":1,"default":"first","given":{"game":{"round":9}},
 "rules":[{"seat":3,"options_include":0,"times":"all"},{"seat":1,"options_include":"Reject","times":"all"},{"seat":2,"options_include":"Reject","times":"all"}],
 "expect":{"game":{"round":10,"proposer":3}}},
{"name":"Round 11 proposer is seat 2","rule":"R5","players":3,"rounds":1,"default":"first","given":{"game":{"round":10}},
 "rules":[{"seat":2,"options_include":0,"times":"all"},{"seat":1,"options_include":"Reject","times":"all"},{"seat":3,"options_include":"Reject","times":"all"}],
 "expect":{"game":{"round":11,"proposer":2}}},
{"name":"Round 12 proposer is seat 1","rule":"R5","players":3,"rounds":1,"default":"first","given":{"game":{"round":11}},
 "rules":[{"seat":1,"options_include":0,"times":"all"},{"seat":2,"options_include":"Reject","times":"all"},{"seat":3,"options_include":"Reject","times":"all"}],
 "expect":{"game":{"round":12,"proposer":1}}},

{"name":"Proposer 2: responder1 is seat 1 (gets offer_a), responder2 is seat 3","rule":"R6","players":3,"rounds":1,"default":"first",
 "given":{"game":{"round":1,"pots_p2":[90]}},
 "rules":[{"seat":2,"options_include":10},{"seat":2,"options_include":20},{"seat":1,"options_include":"Accept"},{"seat":3,"options_include":"Reject"}],
 "expect":{"game":{"proposer":2,"offer_a":10,"offer_b":20,"response1":"Accept","response2":"Reject"},
  "players":{"1":{"score":10},"2":{"score":60},"3":{"score":0}},"not_offered":[{"seat":2,"option":"Accept"}]}},

{"name":"Draw removes one value from the proposer's pot list","rule":"R7","players":3,"rounds":1,"default":"first",
 "given":{"game":{"pots_p1":[90,130]}},
 "rules":[{"seat":1,"options_include":0,"times":"all"},{"seat":2,"options_include":"Reject","times":"all"},{"seat":3,"options_include":"Reject","times":"all"}],
 "expect":{"lens":{"game":{"pots_p1":1,"pots_p2":4,"pots_p3":4}},"players":{"1":{"score":0},"2":{"score":0},"3":{"score":0}}}},

{"name":"Full game of rejections empties every pot list; all tied at 0 share the win","rule":"R8","players":3,"default":"first",
 "rules":[{"seat":1,"options_include":0,"times":"all"},{"seat":2,"options_include":0,"times":"all"},{"seat":3,"options_include":0,"times":"all"},
  {"seat":1,"options_include":"Reject","times":"all"},{"seat":2,"options_include":"Reject","times":"all"},{"seat":3,"options_include":"Reject","times":"all"}],
 "expect":{"winner":[1,2,3],"standings":{"1":0,"2":0,"3":0},"game":{"round":12},
  "lens":{"game":{"pots_p1":0,"pots_p2":0,"pots_p3":0}}}},

{"name":"Only the proposer is asked for amounts; responders never see a number question","rule":"R9","players":3,"rounds":1,"default":"first",
 "given":{"game":{"round":2,"pots_p3":[70]}},
 "rules":[{"seat":3,"options_include":0,"times":"all"},{"seat":1,"options_include":"Reject","times":"all"},{"seat":2,"options_include":"Reject","times":"all"}],
 "expect":{"game":{"proposer":3},"players":{"1":{"score":0},"2":{"score":0},"3":{"score":0}},
  "not_offered":[{"seat":1,"option":0},{"seat":2,"option":0}]}},

{"name":"Round completes after simultaneous talk","rule":"R10","players":3,"rounds":2,"default":"first",
 "rules":[{"seat":1,"options_include":0,"times":"all"},{"seat":2,"options_include":0,"times":"all"},
  {"seat":1,"options_include":"Reject","times":"all"},{"seat":2,"options_include":"Reject","times":"all"},{"seat":3,"options_include":"Reject","times":"all"}],
 "expect":{"game":{"round":2,"proposer":2}}},

{"name":"Offer_b range is limited to 130 - offer_a","rule":"R11","players":3,"rounds":1,"default":"first",
 "rules":[{"seat":1,"options_include":60},{"seat":1,"options_include":70},{"seat":2,"options_include":"Reject","times":"all"},{"seat":3,"options_include":"Reject","times":"all"}],
 "expect":{"game":{"offer_a":60,"offer_b":70},"offered":[{"seat":1,"option":70}],"not_offered":[{"seat":1,"option":131}],
  "players":{"1":{"score":0},"2":{"score":0},"3":{"score":0}}}},

{"name":"Offers are recorded publicly","rule":"R12","players":3,"rounds":1,"default":"first",
 "rules":[{"seat":1,"options_include":25},{"seat":1,"options_include":35},{"seat":2,"options_include":"Reject","times":"all"},{"seat":3,"options_include":"Reject","times":"all"}],
 "expect":{"game":{"offer_a":25,"offer_b":35},"players":{"1":{"score":0},"2":{"score":0},"3":{"score":0}}}},

{"name":"Both responders answer; proposer is not asked to respond","rule":"R13","players":3,"rounds":1,"default":"first",
 "given":{"game":{"pots_p1":[110]}},
 "rules":[{"seat":1,"options_include":30},{"seat":1,"options_include":40},{"seat":2,"options_include":"Accept"},{"seat":3,"options_include":"Reject"}],
 "expect":{"game":{"response1":"Accept","response2":"Reject"},"offered":[{"seat":2,"option":"Reject"},{"seat":3,"option":"Accept"}],
  "not_offered":[{"seat":1,"option":"Accept"}],"players":{"1":{"score":40},"2":{"score":30},"3":{"score":0}}}},

{"name":"Both accept: pot 110, offers 30/40 gives +40/+30/+40","rule":"R14","players":3,"rounds":1,"default":"first",
 "given":{"game":{"pots_p1":[110]}},
 "rules":[{"seat":1,"options_include":30},{"seat":1,"options_include":40},{"seat":2,"options_include":"Accept"},{"seat":3,"options_include":"Accept"}],
 "expect":{"players":{"1":{"score":40},"2":{"score":30},"3":{"score":40}},"game":{"response1":"Accept","response2":"Accept"}}},

{"name":"Only responder1 accepts: pot 90, offers 30/40 gives +20/+30/0","rule":"R15","players":3,"rounds":1,"default":"first",
 "given":{"game":{"pots_p1":[90]}},
 "rules":[{"seat":1,"options_include":30},{"seat":1,"options_include":40},{"seat":2,"options_include":"Accept"},{"seat":3,"options_include":"Reject"}],
 "expect":{"players":{"1":{"score":20},"2":{"score":30},"3":{"score":0}}}},

{"name":"Overpaying: pot 70, offers 50/50 accepted gives proposer -30","rule":"R16","players":3,"rounds":1,"default":"first",
 "given":{"game":{"pots_p1":[70]}},
 "rules":[{"seat":1,"options_include":50,"times":2},{"seat":2,"options_include":"Accept"},{"seat":3,"options_include":"Accept"}],
 "expect":{"players":{"1":{"score":-30},"2":{"score":50},"3":{"score":50}}}},

{"name":"Both reject: no score changes","rule":"R17","players":3,"rounds":1,"default":"first",
 "given":{"players":{"1":{"score":10},"2":{"score":20},"3":{"score":30}}},
 "rules":[{"seat":1,"options_include":30},{"seat":1,"options_include":40},{"seat":2,"options_include":"Reject","times":"all"},{"seat":3,"options_include":"Reject","times":"all"}],
 "expect":{"players":{"1":{"score":10},"2":{"score":20},"3":{"score":30}},"game":{"response1":"Reject","response2":"Reject"}}},

{"name":"Reveal state: responses and scores after proposer 3 deal (pot 130, offers 20/30)","rule":"R18","players":3,"rounds":1,"default":"first",
 "given":{"game":{"round":2,"pots_p3":[130]}},
 "rules":[{"seat":3,"options_include":20},{"seat":3,"options_include":30},{"seat":1,"options_include":"Accept"},{"seat":2,"options_include":"Accept"}],
 "expect":{"game":{"proposer":3,"response1":"Accept","response2":"Accept"},"players":{"1":{"score":20},"2":{"score":30},"3":{"score":80}}}},

{"name":"Game ends after round 12; leader with given scores wins","rule":"R19","players":3,"default":"first",
 "given":{"game":{"round":11,"pots_p1":[70]},"players":{"1":{"score":50},"2":{"score":40},"3":{"score":30}}},
 "rules":[{"seat":1,"options_include":0,"times":"all"},{"seat":2,"options_include":"Reject","times":"all"},{"seat":3,"options_include":"Reject","times":"all"}],
 "expect":{"winner":1,"standings":{"1":50,"2":40,"3":30},"game":{"round":12}}},

{"name":"Tie at the top after round 12 is a shared win","rule":"R20","players":3,"default":"first",
 "given":{"game":{"round":11,"pots_p1":[130]},"players":{"1":{"score":0},"2":{"score":100},"3":{"score":10}}},
 "rules":[{"seat":1,"options_include":15},{"seat":1,"options_include":0},{"seat":2,"options_include":"Accept"},{"seat":3,"options_include":"Reject"}],
 "expect":{"winner":[1,2],"standings":{"1":115,"2":115,"3":10}}}
]
```
````
