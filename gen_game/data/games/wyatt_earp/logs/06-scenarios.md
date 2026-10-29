# 06 scenarios

- time: 2026-10-28T04:12:19+00:00 (48.3s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 5503aa327c319210, reply sha256 c8cbef73c799cd5a

## Sent

````
SPEC:
{
  "name": "Wanted: Dead or Alive (Majority Rule)",
  "summary": "Over 6 rounds, players secretly spread 12 deputies across five outlaws whose posters grow. The player with the most deputies on each outlaw collects its poster, and each player's secret informant outlaw is worth $3,000 more at the end.",
  "players": {
    "min": 3,
    "max": 4,
    "suggested": 3
  },
  "parameters": {
    "outlaw_count": 5,
    "starting_poster": 2000,
    "sighting_bonus": 1000,
    "starting_deputies": 12,
    "starting_money": 0,
    "informant_tip": 3000,
    "rounds": 6,
    "max_commit_per_round": 4,
    "min_commit_per_round": 0
  },
  "attributes": {
    "player": [
      {
        "key": "money",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Dollars won in the final payout. This is the score.",
        "observable": true
      },
      {
        "key": "deputies",
        "type": "number",
        "visible": "public",
        "initial": 12,
        "meaning": "Deputies the player has not yet committed.",
        "observable": true
      },
      {
        "key": "informant",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "The player's secret informant outlaw, dealt at random and unique to each player. It is revealed at the end of the game.",
        "observable": false
      },
      {
        "key": "d_red",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The player's deputy count on Red.",
        "observable": true
      },
      {
        "key": "d_blue",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The player's deputy count on Blue.",
        "observable": true
      },
      {
        "key": "d_green",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The player's deputy count on Green.",
        "observable": true
      },
      {
        "key": "d_yellow",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The player's deputy count on Yellow.",
        "observable": true
      },
      {
        "key": "d_black",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The player's deputy count on Black.",
        "observable": true
      },
      {
        "key": "choice_outlaw",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "The outlaw chosen this round. It stays secret until the reveal.",
        "observable": false
      },
      {
        "key": "choice_number",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "The deputies committed this round, after clamping to remaining deputies. It stays secret until the reveal.",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The current round, from 1 to 6.",
        "observable": true
      },
      {
        "key": "outlaws",
        "type": "list",
        "visible": "public",
        "initial": [
          "Red",
          "Blue",
          "Green",
          "Yellow",
          "Black"
        ],
        "meaning": "The five outlaws. Sightings draw from this list with replacement.",
        "observable": false
      },
      {
        "key": "informant_deck",
        "type": "list",
        "visible": "none",
        "initial": [
          "Red",
          "Blue",
          "Green",
          "Yellow",
          "Black"
        ],
        "meaning": "The hidden pool that informants are dealt from without replacement.",
        "observable": false
      },
      {
        "key": "sighted",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The outlaw sighted this round.",
        "observable": true
      },
      {
        "key": "poster_red",
        "type": "number",
        "visible": "public",
        "initial": 2000,
        "meaning": "Red's poster value.",
        "observable": true
      },
      {
        "key": "poster_blue",
        "type": "number",
        "visible": "public",
        "initial": 2000,
        "meaning": "Blue's poster value.",
        "observable": true
      },
      {
        "key": "poster_green",
        "type": "number",
        "visible": "public",
        "initial": 2000,
        "meaning": "Green's poster value.",
        "observable": true
      },
      {
        "key": "poster_yellow",
        "type": "number",
        "visible": "public",
        "initial": 2000,
        "meaning": "Yellow's poster value.",
        "observable": true
      },
      {
        "key": "poster_black",
        "type": "number",
        "visible": "public",
        "initial": 2000,
        "meaning": "Black's poster value.",
        "observable": true
      },
      {
        "key": "max_red",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Scratch value at the end: the highest deputy count on Red.",
        "observable": false
      },
      {
        "key": "max_blue",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Scratch value at the end: the highest deputy count on Blue.",
        "observable": false
      },
      {
        "key": "max_green",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Scratch value at the end: the highest deputy count on Green.",
        "observable": false
      },
      {
        "key": "max_yellow",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Scratch value at the end: the highest deputy count on Yellow.",
        "observable": false
      },
      {
        "key": "max_black",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Scratch value at the end: the highest deputy count on Black.",
        "observable": false
      },
      {
        "key": "tied_red",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Scratch value at the end: the number of players whose count on Red equals max_red.",
        "observable": false
      },
      {
        "key": "tied_blue",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Scratch value at the end: the number of players whose count on Blue equals max_blue.",
        "observable": false
      },
      {
        "key": "tied_green",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Scratch value at the end: the number of players whose count on Green equals max_green.",
        "observable": false
      },
      {
        "key": "tied_yellow",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Scratch value at the end: the number of players whose count on Yellow equals max_yellow.",
        "observable": false
      },
      {
        "key": "tied_black",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Scratch value at the end: the number of players whose count on Black equals max_black.",
        "observable": false
      }
    ]
  },
  "setup": [
    "Every poster is set to $2,000. Every player gets deputies = 12, money = 0 and all five deputy counts at 0.",
    "For each player, one outlaw is drawn at random from informant_deck, written into that player's informant and removed from informant_deck, so no two players share an informant.",
    "Each player is told privately which outlaw is their informant. Nobody else is told.",
    "round is set to 0."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round += 1. sighted is set to one outlaw picked uniformly at random from outlaws, which is not removed (with replacement). The poster of sighted rises by 1000, for example poster_red += 1000 if sighted is Red.",
      "judged": null
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "The table hears: 'Round {round}: {sighted} was sighted; its poster is now {poster of sighted}.'",
      "judged": null
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player is sent their own state: deputies, informant, their deputy counts, all posters and all public deputy counts.",
      "judged": null
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "one short text message",
      "effect": "All messages are collected at once, then broadcast to everyone as 'Seat {seat} says: {value}'. Talk is not binding.",
      "judged": null
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "one choice from 25 options of the form '<outlaw> <n>', where outlaw is Red, Blue, Green, Yellow or Black and n is 0 to 4",
      "effect": "choice_outlaw is set to the outlaw and choice_number to min(n, deputies). No answer is seen until all are in.",
      "judged": null
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Every player's choice is announced: 'Seat {seat} commits {choice_number} deputies to {choice_outlaw}.'",
      "judged": null
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "For each player, deputies -= choice_number, and the deputy count matching choice_outlaw (d_red, d_blue, d_green, d_yellow or d_black) += choice_number. Posters do not change.",
      "judged": null
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "This step runs only when round == 6. Every player's informant is revealed to all. For each player, the poster of their informant += 3000.",
      "judged": null
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "This step runs only when round == 6. For each outlaw X: max_X = the maximum over players of d_X, and tied_X = the number of players with d_X == max_X. For each player and each outlaw X, if max_X > 0 and d_X == max_X, then money += floor(poster_X / tied_X). An outlaw with max_X == 0 escapes and pays nobody. Unused deputies are worth nothing.",
      "judged": null
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "This step runs only when round == 6. The final posters, the informants and each player's money are announced.",
      "judged": null
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "If round >= 6 the game ends. Otherwise play continues with the next round.",
      "judged": null
    }
  ],
  "ending": {
    "condition": "round >= 6",
    "rank_by": "you.money",
    "decided_by": "Each player's standing is their money after the final payout. The player with the most money wins, and players tied for the most money share the result (the source calls this a draw)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game starts, then every poster is $2,000, and every player has 12 deputies, $0 and a deputy count of 0 on each of the five outlaws."
    },
    {
      "id": "R2",
      "text": "When the game starts, then each player is dealt a distinct informant outlaw at random that only they can see."
    },
    {
      "id": "R3",
      "text": "When a round begins, then one of the five outlaws is sighted uniformly at random with replacement, and its poster rises by $1,000."
    },
    {
      "id": "R4",
      "text": "When the same outlaw is sighted in two rounds, then its poster rises by $1,000 each time."
    },
    {
      "id": "R5",
      "text": "When the talk step runs, then every player submits one short message simultaneously, and all messages are shown to everyone only after all are in."
    },
    {
      "id": "R6",
      "text": "When the commitment step runs, then every player simultaneously chooses one outlaw and a number from 0 to 4, and no choice is seen before all are in."
    },
    {
      "id": "R7",
      "text": "When a player commits more deputies than they have remaining (for example 4 with 2 left), then the commitment is reduced to their remaining deputies (2)."
    },
    {
      "id": "R8",
      "text": "When choices are in, then every player's outlaw and committed number are announced to all."
    },
    {
      "id": "R9",
      "text": "When a player commits n deputies to outlaw X, then their remaining deputies fall by n and their deputy count on X rises by n."
    },
    {
      "id": "R10",
      "text": "When deputies are committed, then no poster changes."
    },
    {
      "id": "R11",
      "text": "When round 6 ends, then all informants are revealed and each informant outlaw's poster rises by $3,000."
    },
    {
      "id": "R12",
      "text": "When an outlaw is nobody's informant, then its poster gets no $3,000 tip."
    },
    {
      "id": "R13",
      "text": "When no player has any deputies on an outlaw at the end, then it escapes and pays nobody."
    },
    {
      "id": "R14",
      "text": "When one player has the strictly highest deputy count on an outlaw at the end, then that player receives the outlaw's whole poster."
    },
    {
      "id": "R15",
      "text": "When k players tie for the highest positive deputy count on an outlaw, then each receives floor(poster / k) dollars (for example 3 players on a $5,000 poster get $1,666 each)."
    },
    {
      "id": "R16",
      "text": "When the game ends, then unused deputies are worth $0, and each player's money is the sum of their payouts."
    },
    {
      "id": "R17",
      "text": "When round 6 has been resolved, then the game ends and the player with the most money wins. Players tied for the most money share the result."
    }
  ],
  "offers": [
    {
      "question": "Talk: one short message",
      "who": "every seat",
      "options": "Free short text, every round, for every seat."
    },
    {
      "question": "Commitment: outlaw and number of deputies",
      "who": "every seat",
      "options": "Any of the 25 combinations of outlaw (Red, Blue, Green, Yellow, Black) and n from 0 to 4, every round, even with fewer than 4 deputies left. A number above remaining deputies is reduced by the engine, as the rules say."
    }
  ],
  "choices": [
    {
      "what": "3 to 4 players, suggested 3",
      "why": "The designer suggests 3, and the source allows 3 to 4. Majority contests need rivals, and 3 is the smallest table where a player can be outbid or split. With 5 informants the table cannot exceed 5, and the source caps it at 4."
    },
    {
      "what": "Talk kept as a simultaneous poll broadcast to all",
      "why": "The rules require it. Players disagree about which outlaws to contest and can bluff about their informant, so talk gives them something to reason about."
    },
    {
      "what": "Commitment offered as one combined choice of outlaw and number",
      "why": "This keeps both parts of the commitment in a single simultaneous poll, so no part is seen early."
    },
    {
      "what": "Remaining deputies made public",
      "why": "They follow directly from the announced commitments, so hiding them would hide nothing."
    },
    {
      "what": "Strategy at the table",
      "why": "A thoughtful player pushes deputies onto their own informant without giving it away, saves deputies for late sightings, avoids costly ties, and reads others' talk and commitments for hints about their informants."
    }
  ],
  "simplifications": [
    {
      "what": "A tie for the most money is a shared win rather than a separate draw",
      "why": "The engine ranks by one expression, and players level at the top share the win."
    },
    {
      "what": "End-of-game payout steps sit in the round with a 'round == 6' condition",
      "why": "The step list is flat. Conditional single steps reproduce the end-of-game payout exactly."
    },
    {
      "what": "Per-outlaw maximum and tie counts kept as table scratch attributes",
      "why": "Comparing player attributes needs a table attribute beside them."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: money, deputies, d_red, d_blue, d_green, d_yellow, d_black; table: round, sighted, poster_red, poster_blue, poster_green, poster_yellow, poster_black.
````

## Reply

````
[
{"name":"Setup: posters $2,000, 12 deputies, $0, no deputies on any outlaw","rule":"R1","players":3,"rounds":0,
 "expect":{"players":{"1":{"money":0,"deputies":12,"d_red":0,"d_blue":0,"d_green":0,"d_yellow":0,"d_black":0},
 "2":{"money":0,"deputies":12,"d_red":0,"d_blue":0,"d_green":0,"d_yellow":0,"d_black":0},
 "3":{"money":0,"deputies":12,"d_red":0,"d_blue":0,"d_green":0,"d_yellow":0,"d_black":0}},
 "game":{"round":0,"poster_red":2000,"poster_blue":2000,"poster_green":2000,"poster_yellow":2000,"poster_black":2000}}},
{"name":"Setup: each of 3 players draws a distinct informant, leaving 2 in the deck (which outlaws is chance)","rule":"R2","players":3,"rounds":0,
 "expect":{"lens":{"game":{"informant_deck":2}}}},
{"name":"Setup with 4 players leaves 1 informant in the deck","rule":"R2","players":4,"rounds":0,
 "expect":{"lens":{"game":{"informant_deck":1}}}},
{"name":"Sighted outlaw's poster rises by 1000","rule":"R3","players":3,"rounds":1,
 "given":{"game":{"outlaws":["Green"]}},
 "rules":[{"seat":1,"options_include":"Red 0"},{"seat":2,"options_include":"Red 0"},{"seat":3,"options_include":"Red 0"}],
 "expect":{"game":{"round":1,"sighted":"Green","poster_green":3000,"poster_red":2000,"poster_blue":2000,"poster_yellow":2000,"poster_black":2000}}},
{"name":"Same outlaw sighted twice rises 1000 each time","rule":"R4","players":3,"rounds":2,
 "given":{"game":{"outlaws":["Blue"]}},
 "rules":[{"seat":1,"options_include":"Red 0","times":2},{"seat":2,"options_include":"Red 0","times":2},{"seat":3,"options_include":"Red 0","times":2}],
 "expect":{"game":{"round":2,"sighted":"Blue","poster_blue":4000,"poster_red":2000,"poster_green":2000,"poster_yellow":2000,"poster_black":2000}}},
{"name":"Talk step does not change any state; the round proceeds to commitments","rule":"R5","players":3,"rounds":1,
 "given":{"game":{"outlaws":["Red"]}},
 "rules":[{"seat":1,"options_include":"Red 0"},{"seat":2,"options_include":"Red 0"},{"seat":3,"options_include":"Red 0"}],
 "expect":{"game":{"round":1},"players":{"1":{"deputies":12,"money":0},"2":{"deputies":12,"money":0},"3":{"deputies":12,"money":0}},
 "offered":[{"seat":1,"option":"Red 0"},{"seat":2,"option":"Red 0"},{"seat":3,"option":"Red 0"}]}},
{"name":"Every seat is offered all outlaw/number combinations including 0 and 4","rule":"R6","players":3,"rounds":1,
 "given":{"game":{"outlaws":["Red"]}},
 "rules":[{"seat":1,"options_include":"Green 3"},{"seat":2,"options_include":"Black 4"},{"seat":3,"options_include":"Yellow 0"}],
 "expect":{"players":{"1":{"d_green":3,"deputies":9},"2":{"d_black":4,"deputies":8},"3":{"d_yellow":0,"deputies":12}},
 "offered":[{"seat":1,"option":"Black 4"},{"seat":2,"option":"Red 0"},{"seat":3,"option":"Blue 4"},{"seat":1,"option":"Yellow 2"}]}},
{"name":"Committing 4 with 2 left commits only 2","rule":"R7","players":3,"rounds":1,
 "given":{"players":{"1":{"deputies":2},"2":{"deputies":0}},"game":{"outlaws":["Black"]}},
 "rules":[{"seat":1,"options_include":"Red 4"},{"seat":2,"options_include":"Blue 4"},{"seat":3,"options_include":"Red 0"}],
 "expect":{"players":{"1":{"deputies":0,"d_red":2},"2":{"deputies":0,"d_blue":0},"3":{"deputies":12}}}},
{"name":"Each player's choice is applied to their public counts","rule":"R8","players":3,"rounds":1,
 "given":{"game":{"outlaws":["Red"]}},
 "rules":[{"seat":1,"options_include":"Blue 1"},{"seat":2,"options_include":"Green 2"},{"seat":3,"options_include":"Black 4"}],
 "expect":{"players":{"1":{"d_blue":1,"deputies":11},"2":{"d_green":2,"deputies":10},"3":{"d_black":4,"deputies":8}}}},
{"name":"Committing 3 to Blue: deputies 12->9, d_blue 0->3","rule":"R9","players":3,"rounds":1,
 "given":{"game":{"outlaws":["Red"]}},
 "rules":[{"seat":1,"options_include":"Blue 3"},{"seat":2,"options_include":"Red 0"},{"seat":3,"options_include":"Red 0"}],
 "expect":{"players":{"1":{"deputies":9,"d_blue":3,"d_red":0,"d_green":0,"d_yellow":0,"d_black":0},"2":{"deputies":12},"3":{"deputies":12}}}},
{"name":"Commitments do not change posters","rule":"R10","players":3,"rounds":1,
 "given":{"game":{"outlaws":["Red"]}},
 "rules":[{"seat":1,"options_include":"Blue 4"},{"seat":2,"options_include":"Yellow 4"},{"seat":3,"options_include":"Red 4"}],
 "expect":{"game":{"poster_red":3000,"poster_blue":2000,"poster_green":2000,"poster_yellow":2000,"poster_black":2000}}},
{"name":"After round 6 each informant's poster rises by 3000","rule":"R11","players":3,
 "given":{"players":{"1":{"informant":"Red"},"2":{"informant":"Blue"},"3":{"informant":"Green"}},"game":{"round":5,"outlaws":["Black"]}},
 "rules":[{"seat":1,"options_include":"Red 0"},{"seat":2,"options_include":"Red 0"},{"seat":3,"options_include":"Red 0"}],
 "expect":{"winner":[1,2,3],"game":{"round":6,"poster_red":5000,"poster_blue":5000,"poster_green":5000,"poster_black":3000,"poster_yellow":2000},
 "players":{"1":{"money":0},"2":{"money":0},"3":{"money":0}}}},
{"name":"Outlaw nobody holds as informant gets no tip","rule":"R12","players":3,
 "given":{"players":{"1":{"informant":"Red"},"2":{"informant":"Blue"},"3":{"informant":"Green"}},"game":{"round":5,"outlaws":["Black"]}},
 "rules":[{"seat":1,"options_include":"Red 0"},{"seat":2,"options_include":"Red 0"},{"seat":3,"options_include":"Red 0"}],
 "expect":{"winner":[1,2,3],"game":{"poster_yellow":2000,"poster_black":3000}}},
{"name":"Outlaws with no deputies escape and pay nobody","rule":"R13","players":3,
 "given":{"players":{"1":{"informant":"Red","d_red":1,"deputies":11},"2":{"informant":"Blue"},"3":{"informant":"Green"}},"game":{"round":5,"outlaws":["Black"]}},
 "rules":[{"seat":1,"options_include":"Red 0"},{"seat":2,"options_include":"Red 0"},{"seat":3,"options_include":"Red 0"}],
 "expect":{"winner":1,"standings":{"1":5000,"2":0,"3":0},"players":{"1":{"money":5000},"2":{"money":0},"3":{"money":0}}}},
{"name":"Strict majority on Blue takes the whole $5,000 poster","rule":"R14","players":3,
 "given":{"players":{"1":{"informant":"Red","d_blue":3,"deputies":9},"2":{"informant":"Blue","d_blue":2,"deputies":10},"3":{"informant":"Green"}},"game":{"round":5,"outlaws":["Black"]}},
 "rules":[{"seat":1,"options_include":"Red 0"},{"seat":2,"options_include":"Red 0"},{"seat":3,"options_include":"Red 0"}],
 "expect":{"winner":1,"standings":{"1":5000,"2":0,"3":0},"players":{"1":{"money":5000},"2":{"money":0},"3":{"money":0}}}},
{"name":"Three-way tie on a $5,000 poster pays $1,666 each","rule":"R15","players":3,
 "given":{"players":{"1":{"informant":"Yellow","d_yellow":2,"deputies":10},"2":{"informant":"Red","d_yellow":2,"deputies":10},"3":{"informant":"Blue","d_yellow":2,"deputies":10}},"game":{"round":5,"outlaws":["Black"]}},
 "rules":[{"seat":1,"options_include":"Red 0"},{"seat":2,"options_include":"Red 0"},{"seat":3,"options_include":"Red 0"}],
 "expect":{"winner":[1,2,3],"standings":{"1":1666,"2":1666,"3":1666},"game":{"poster_yellow":5000},"players":{"1":{"money":1666},"2":{"money":1666},"3":{"money":1666}}}},
{"name":"Money is the sum of payouts; unused deputies worth nothing","rule":"R16","players":3,
 "given":{"players":{"1":{"informant":"Red","d_green":1,"deputies":11},"2":{"informant":"Blue","d_red":2,"d_black":1,"deputies":9},"3":{"informant":"Green","deputies":12}},"game":{"round":5,"outlaws":["Black"]}},
 "rules":[{"seat":1,"options_include":"Red 0"},{"seat":2,"options_include":"Red 0"},{"seat":3,"options_include":"Red 0"}],
 "expect":{"winner":2,"standings":{"1":5000,"2":8000,"3":0},"players":{"1":{"money":5000},"2":{"money":8000},"3":{"money":0,"deputies":12}}}},
{"name":"Game ends after round 6; players tied for most money share the win","rule":"R17","players":3,
 "given":{"players":{"1":{"informant":"Red","d_red":1,"deputies":11},"2":{"informant":"Blue","d_blue":1,"deputies":11},"3":{"informant":"Green"}},"game":{"round":5,"outlaws":["Black"]}},
 "rules":[{"seat":1,"options_include":"Red 0"},{"seat":2,"options_include":"Red 0"},{"seat":3,"options_include":"Red 0"}],
 "expect":{"winner":[1,2],"standings":{"1":5000,"2":5000,"3":0},"game":{"round":6}}}
]
````
