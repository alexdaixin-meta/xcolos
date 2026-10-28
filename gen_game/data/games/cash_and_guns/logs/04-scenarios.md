# 04 scenarios

- time: 2026-10-28T06:15:50+00:00 (87.5s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 4a00e34f8082bb11, reply sha256 cb5557dd29d5226c

## Sent

````
SPEC:
{
  "name": "Cash and Guns: Standoff",
  "summary": "Over 8 rounds, gangsters bluff with a private hand of 3 Bang and 5 Click bullets, aim at each other, then Stand or Duck; the unwounded players who Stand split the pot, and three wounds eliminate a player.",
  "players": {
    "min": 3,
    "max": 5,
    "suggested": 4
  },
  "parameters": {
    "rounds": 8,
    "starting_cash": 0,
    "starting_wounds": 0,
    "bang_cards": 3,
    "click_cards": 5,
    "hand_size": 8,
    "pot_min": 6,
    "pot_max": 14,
    "pot_unit_dollars": 1000,
    "wounds_per_bang": 1,
    "wounds_to_eliminate": 3,
    "talk_messages_per_round": 1,
    "rank_alive_weight": 1000000,
    "rank_cash_weight": 1000,
    "rank_wound_weight": 1
  },
  "attributes": {
    "player": [
      {
        "key": "cash",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Cash collected, in thousands of dollars. It may be fractional.",
        "observable": true
      },
      {
        "key": "wounds",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Wounds taken so far. A player with 3 or more is eliminated.",
        "observable": true
      },
      {
        "key": "alive",
        "type": "bool",
        "visible": "public",
        "initial": true,
        "meaning": "False once the player has been eliminated.",
        "observable": true
      },
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [
          "Bang",
          "Bang",
          "Bang",
          "Click",
          "Click",
          "Click",
          "Click",
          "Click"
        ],
        "meaning": "The bullet cards the player still holds. Only the owner sees it.",
        "observable": false
      },
      {
        "key": "aim_target",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "The target chosen secretly in AIM, before it is shown.",
        "observable": false
      },
      {
        "key": "target",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "This round's target, shown publicly in GUNS SHOWN.",
        "observable": true
      },
      {
        "key": "bullet",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "The bullet card loaded this round, Bang or Click. It stays hidden unless it is fired.",
        "observable": false
      },
      {
        "key": "stance",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "This round's Stand or Duck, announced after everyone has chosen.",
        "observable": true
      },
      {
        "key": "fired",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "True if this round's bullet was fired, meaning both the shooter and the target Stood.",
        "observable": true
      },
      {
        "key": "revealed_bullets",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "The player's bullets that have been fired and revealed so far.",
        "observable": true
      },
      {
        "key": "hit_this_round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Wounds taken this round.",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The current round, from 1 to 8.",
        "observable": true
      },
      {
        "key": "pot",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "This round's loot, in thousands of dollars, from 6 to 14.",
        "observable": true
      },
      {
        "key": "sharers",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The number of players who split this round's pot.",
        "observable": false
      },
      {
        "key": "living",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The number of players still alive. This is a table copy kept for the end check.",
        "observable": true
      }
    ]
  },
  "setup": [
    "Every player starts with cash 0, wounds 0 and alive true.",
    "Every player's hand is set to 3 Bang and 5 Click cards, visible only to its owner.",
    "Table living is set to the number of seats, and round is set to 0.",
    "Each player is sent their own state."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round += 1. pot = a random whole number from 6 to 14. Each living player's target, aim_target, bullet and stance are set to empty, fired to false and hit_this_round to 0. Announce: 'Round {round}: the pot is {pot} thousand dollars.'"
    },
    {
      "action": "poll",
      "who": "all living players",
      "answer": "one short free-text message",
      "effect": "Nothing changes. Every message is broadcast to all players as 'Seat {seat} says: {value}'. Nothing said is binding."
    },
    {
      "action": "poll",
      "who": "all living players",
      "answer": "a choice of one other living seat",
      "effect": "The chosen seat is stored in aim_target, which stays hidden from the others for now."
    },
    {
      "action": "poll",
      "who": "all living players",
      "answer": "a choice of Bang or Click, offered only for a card type still present in the player's hand",
      "effect": "The chosen card is stored in bullet, which stays hidden."
    },
    {
      "action": "update",
      "who": "all living players",
      "answer": null,
      "effect": "GUNS SHOWN: target = aim_target for every living player. Announce every seat's target. Bullets stay hidden."
    },
    {
      "action": "poll",
      "who": "all living players",
      "answer": "a choice of Stand or Duck",
      "effect": "The choice is stored in stance. Announce every seat's stance once all are in."
    },
    {
      "action": "update",
      "who": "all living players",
      "answer": null,
      "effect": "FIRE: For each living player, one card equal to bullet is removed from hand. fired = (stance == Stand and the target's stance == Stand). If fired, bullet is appended to revealed_bullets and announced publicly. Then each living player's hit_this_round = the number of players with target == this seat, fired == true and bullet == Bang, and wounds += hit_this_round. All shots resolve at once."
    },
    {
      "action": "update",
      "who": "all living players",
      "answer": null,
      "effect": "ELIMINATION: if wounds >= 3, then alive = false and the elimination is announced. Afterwards, living = the count of players with alive == true."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "SPLIT: sharers = the count of players with alive == true, stance == Stand and hit_this_round == 0. If sharers > 0, then each of those players gets cash += pot / sharers. Otherwise the pot is lost. Announce the gains."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "The game ends if living <= 1 or round >= 8. Otherwise the next round starts."
    }
  ],
  "ending": {
    "condition": "living <= 1 or round >= 8",
    "rank_by": "you.alive * 1000000 + you.cash * 1000 + you.wounds",
    "min_to_win": 1000000,
    "decided_by": "Only living players can win. Among them, the highest cash wins, and if cash is tied, the most wounds wins. Players still tied share the win, which is the source's draw. A lone survivor wins. If nobody is alive, no one reaches the bar, so the game has no winner and is a draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game starts, then every player has cash 0, wounds 0, alive true, and a hand of exactly 3 Bang and 5 Click cards."
    },
    {
      "id": "R2",
      "text": "When a round starts, then pot is set to a whole number from 6 to 14 and announced, and round increases by 1."
    },
    {
      "id": "R3",
      "text": "When the talk step runs, then every living player submits one message simultaneously, and all messages are shown to everyone only after all are in."
    },
    {
      "id": "R4",
      "text": "When a player aims, then the target offered is any living seat except their own, and the bullet offered is only a card type still in their hand."
    },
    {
      "id": "R5",
      "text": "When all players have aimed, then every target is announced publicly and no bullet type is revealed."
    },
    {
      "id": "R6",
      "text": "When a player chooses Stand or Duck, then the choice is simultaneous and all stances are announced after all are in."
    },
    {
      "id": "R7",
      "text": "When FIRE resolves, then each living player's chosen bullet is removed from their hand, whether or not it is fired."
    },
    {
      "id": "R8",
      "text": "When both a shooter and their target Stood, then the shooter's bullet is fired and appended to their public revealed_bullets."
    },
    {
      "id": "R9",
      "text": "When a shooter Ducked or their target Ducked, then the bullet is discarded without its type being revealed, and it causes no wound."
    },
    {
      "id": "R10",
      "text": "When a fired bullet is a Bang, then its target gains 1 wound, and a target hit by k fired Bangs gains k wounds."
    },
    {
      "id": "R11",
      "text": "When shots are resolved, then all shots happen at once, so a player wounded this round still fires their own bullet."
    },
    {
      "id": "R12",
      "text": "When a player reaches 3 or more wounds, then alive becomes false, they keep their cash, and they take no further part in the game."
    },
    {
      "id": "R13",
      "text": "When the pot is split, then the sharers are the living players who Stood and took 0 wounds this round, and each gains pot / sharers in cash, which may be fractional."
    },
    {
      "id": "R14",
      "text": "When no player qualifies as a sharer, then the pot is lost and nobody gains cash."
    },
    {
      "id": "R15",
      "text": "When a player Ducked or was wounded this round, then they gain no cash that round."
    },
    {
      "id": "R16",
      "text": "When only one player is alive after a round, then the game ends and that player wins."
    },
    {
      "id": "R17",
      "text": "When no player is alive, then the game ends with no winner, which is a draw."
    },
    {
      "id": "R18",
      "text": "When round 8 ends with 2 or more players alive, then the game ends and the living player with the highest cash wins."
    },
    {
      "id": "R19",
      "text": "When living players are tied on cash, then the one with the most wounds wins, and players still tied share the win."
    },
    {
      "id": "R20",
      "text": "When an eliminated player has more cash than every living player, then the eliminated player still cannot win."
    }
  ],
  "offers": [
    {
      "question": "TALK: your message",
      "who": "every living seat",
      "options": "Free text, one short message."
    },
    {
      "question": "AIM: your target",
      "who": "every living seat",
      "options": "Every living seat except the one choosing."
    },
    {
      "question": "AIM: your bullet",
      "who": "every living seat",
      "options": "Bang and Click if the hand holds both. Only Bang if the hand holds no Click. Only Click if the hand holds no Bang."
    },
    {
      "question": "STAND OR DUCK",
      "who": "every living seat",
      "options": "Stand, Duck."
    }
  ],
  "choices": [
    {
      "what": "3 to 5 players, suggested 4",
      "why": "The designer chose 4, so it is kept. The minimum is 3, because with 2 players aiming has no choice and splitting the pot is trivial. The maximum is 5, because beyond that a single gun matters little and the talk is long."
    },
    {
      "what": "Keep a simultaneous talk poll each round, broadcast to all",
      "why": "The source requires it. Players disagree about who should duck and who gets shot, so non-binding threats and bluffs about bullets give them something to reason about."
    },
    {
      "what": "Target and bullet are taken in two consecutive polls, with the target held in a hidden aim_target until GUNS SHOWN",
      "why": "A step takes one answer. Holding the target hidden keeps both choices simultaneous and secret, as the source requires."
    },
    {
      "what": "rank_by = alive*1000000 + cash*1000 + wounds, with min_to_win 1000000",
      "why": "Only living players can win, cash comes first and wounds break ties. Cash differences are multiples of 1/60, so the weight 1000 keeps them above the maximum wound gap of 2. The bar makes an all-eliminated game end with no winner."
    }
  ],
  "simplifications": [
    {
      "what": "A tie on both cash and wounds is a shared win",
      "why": "The engine has no separate draw: players level at the top share the win, which stands for the source's draw."
    },
    {
      "what": "Comparing a player's stance with their target's stance, and counting the Bangs aimed at a seat, uses the player-attribute-compare workaround",
      "why": "The engine has no direct operand for another player's attribute, so this costs extra steps."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: cash, wounds, alive, target, stance, fired, revealed_bullets; table: round, pot, living.
````

## Reply

````
[
{"name":"Setup: cash 0, wounds 0, alive, hand of 8 cards","rule":"R1","players":3,"rounds":0,
 "expect":{"players":{"1":{"cash":0,"wounds":0,"alive":true},"2":{"cash":0,"wounds":0,"alive":true},"3":{"cash":0,"wounds":0,"alive":true}},
           "game":{"round":0,"living":3},
           "lens":{"players":{"1":{"hand":8,"revealed_bullets":0},"2":{"hand":8},"3":{"hand":8}}}}},

{"name":"Round counter increases by 1 (pot is random, not asserted)","rule":"R2","players":3,"rounds":1,
 "rules":[{"seat":1,"options_include":2},{"seat":1,"options_include":"Click"},{"seat":1,"options_include":"Duck"},
          {"seat":2,"options_include":3},{"seat":2,"options_include":"Click"},{"seat":2,"options_include":"Duck"},
          {"seat":3,"options_include":1},{"seat":3,"options_include":"Click"},{"seat":3,"options_include":"Duck"}],
 "expect":{"game":{"round":1,"living":3}}},

{"name":"Talk step changes nothing; the round still plays","rule":"R3","players":3,"rounds":1,
 "given":{"players":{"1":{"cash":2},"2":{"cash":3},"3":{"cash":4}}},
 "rules":[{"seat":1,"options_include":2},{"seat":1,"options_include":"Click"},{"seat":1,"options_include":"Duck"},
          {"seat":2,"options_include":3},{"seat":2,"options_include":"Click"},{"seat":2,"options_include":"Duck"},
          {"seat":3,"options_include":1},{"seat":3,"options_include":"Click"},{"seat":3,"options_include":"Duck"}],
 "expect":{"game":{"round":1,"living":3},
           "players":{"1":{"wounds":0,"alive":true,"cash":2},"2":{"wounds":0,"alive":true,"cash":3},"3":{"wounds":0,"alive":true,"cash":4}}}},

{"name":"Aim offers only other living seats and only bullet types in hand","rule":"R4","players":3,"rounds":1,
 "given":{"players":{"1":{"hand":["Click","Click"]},"3":{"alive":false,"wounds":3}},"game":{"living":2}},
 "rules":[{"seat":1,"options_include":2},{"seat":1,"options_include":"Click"},{"seat":1,"options_include":"Duck"},
          {"seat":2,"options_include":1},{"seat":2,"options_include":"Click"},{"seat":2,"options_include":"Duck"}],
 "expect":{"offered":[{"seat":1,"option":2},{"seat":1,"option":"Click"}],
           "not_offered":[{"seat":1,"option":"Bang"},{"seat":1,"option":1},{"seat":1,"option":3},{"seat":2,"option":2},{"seat":2,"option":3},{"seat":3,"option":"Stand"},{"seat":3,"option":"Duck"}],
           "lens":{"players":{"1":{"hand":1},"2":{"hand":7}}},
           "players":{"3":{"wounds":3,"alive":false}}}},

{"name":"Targets are shown publicly; bullets are not revealed","rule":"R5","players":3,"rounds":1,
 "rules":[{"seat":1,"options_include":2},{"seat":1,"options_include":"Bang"},{"seat":1,"options_include":"Duck"},
          {"seat":2,"options_include":3},{"seat":2,"options_include":"Click"},{"seat":2,"options_include":"Duck"},
          {"seat":3,"options_include":1},{"seat":3,"options_include":"Bang"},{"seat":3,"options_include":"Duck"}],
 "expect":{"players":{"1":{"target":"2","revealed_bullets":[]},"2":{"target":"3","revealed_bullets":[]},"3":{"target":"1","revealed_bullets":[]}}}},

{"name":"Stances are recorded and announced","rule":"R6","players":3,"rounds":1,
 "rules":[{"seat":1,"options_include":2},{"seat":1,"options_include":"Click"},{"seat":1,"options_include":"Stand"},
          {"seat":2,"options_include":3},{"seat":2,"options_include":"Click"},{"seat":2,"options_include":"Duck"},
          {"seat":3,"options_include":1},{"seat":3,"options_include":"Click"},{"seat":3,"options_include":"Duck"}],
 "expect":{"players":{"1":{"stance":"Stand"},"2":{"stance":"Duck"},"3":{"stance":"Duck"}},
           "offered":[{"seat":2,"option":"Stand"},{"seat":3,"option":"Stand"}]}},

{"name":"Chosen bullet leaves the hand even when not fired","rule":"R7","players":3,"rounds":1,
 "rules":[{"seat":1,"options_include":2},{"seat":1,"options_include":"Bang"},{"seat":1,"options_include":"Duck"},
          {"seat":2,"options_include":3},{"seat":2,"options_include":"Click"},{"seat":2,"options_include":"Duck"},
          {"seat":3,"options_include":1},{"seat":3,"options_include":"Bang"},{"seat":3,"options_include":"Duck"}],
 "expect":{"lens":{"players":{"1":{"hand":7,"revealed_bullets":0},"2":{"hand":7,"revealed_bullets":0},"3":{"hand":7,"revealed_bullets":0}}},
           "players":{"1":{"fired":false,"wounds":0},"2":{"fired":false,"wounds":0},"3":{"fired":false,"wounds":0}}}},

{"name":"Shooter and target both Stand: bullet fired and revealed","rule":"R8","players":3,"rounds":1,
 "rules":[{"seat":1,"options_include":2},{"seat":1,"options_include":"Click"},{"seat":1,"options_include":"Stand"},
          {"seat":2,"options_include":1},{"seat":2,"options_include":"Click"},{"seat":2,"options_include":"Stand"},
          {"seat":3,"options_include":1},{"seat":3,"options_include":"Click"},{"seat":3,"options_include":"Stand"}],
 "expect":{"players":{"1":{"fired":true,"revealed_bullets":["Click"],"wounds":0},
                      "2":{"fired":true,"revealed_bullets":["Click"],"wounds":0},
                      "3":{"fired":true,"revealed_bullets":["Click"],"wounds":0}}}},

{"name":"A Duck by shooter or target discards the bullet unrevealed and harmless","rule":"R9","players":3,"rounds":1,
 "rules":[{"seat":1,"options_include":2},{"seat":1,"options_include":"Bang"},{"seat":1,"options_include":"Stand"},
          {"seat":2,"options_include":1},{"seat":2,"options_include":"Click"},{"seat":2,"options_include":"Duck"},
          {"seat":3,"options_include":1},{"seat":3,"options_include":"Bang"},{"seat":3,"options_include":"Duck"}],
 "expect":{"players":{"1":{"fired":false,"revealed_bullets":[],"wounds":0},
                      "2":{"fired":false,"revealed_bullets":[],"wounds":0},
                      "3":{"fired":false,"revealed_bullets":[],"wounds":0}},
           "lens":{"players":{"1":{"hand":7},"3":{"hand":7}}}}},

{"name":"Two fired Bangs on one target give 2 wounds","rule":"R10","players":3,"rounds":1,
 "rules":[{"seat":1,"options_include":2},{"seat":1,"options_include":"Click"},{"seat":1,"options_include":"Stand"},
          {"seat":2,"options_include":1},{"seat":2,"options_include":"Bang"},{"seat":2,"options_include":"Stand"},
          {"seat":3,"options_include":1},{"seat":3,"options_include":"Bang"},{"seat":3,"options_include":"Stand"}],
 "expect":{"players":{"1":{"wounds":2,"alive":true,"cash":0},"2":{"wounds":0,"revealed_bullets":["Bang"]},"3":{"wounds":0,"revealed_bullets":["Bang"]}}}},

{"name":"Simultaneous shots: a player eliminated this round still fires","rule":"R11","players":3,"rounds":1,
 "given":{"players":{"1":{"wounds":2}}},
 "rules":[{"seat":1,"options_include":2},{"seat":1,"options_include":"Bang"},{"seat":1,"options_include":"Stand"},
          {"seat":2,"options_include":1},{"seat":2,"options_include":"Bang"},{"seat":2,"options_include":"Stand"},
          {"seat":3,"options_include":1},{"seat":3,"options_include":"Click"},{"seat":3,"options_include":"Duck"}],
 "expect":{"players":{"1":{"wounds":3,"alive":false,"fired":true,"revealed_bullets":["Bang"]},"2":{"wounds":1,"alive":true,"fired":true}},
           "game":{"living":2}}},

{"name":"Third wound eliminates; cash is kept and the player sits out later rounds","rule":"R12","players":3,"rounds":2,
 "given":{"players":{"1":{"wounds":2,"cash":5}}},
 "rules":[{"seat":1,"options_include":2},{"seat":1,"options_include":"Click"},{"seat":1,"options_include":"Stand"},
          {"seat":2,"options_include":1},{"seat":2,"options_include":3},{"seat":2,"options_include":"Bang"},{"seat":2,"options_include":"Click"},
          {"seat":2,"options_include":"Stand"},{"seat":2,"options_include":"Duck"},
          {"seat":3,"options_include":2,"times":2},{"seat":3,"options_include":"Click","times":2},{"seat":3,"options_include":"Duck","times":2}],
 "expect":{"players":{"1":{"wounds":3,"alive":false,"cash":5}},
           "lens":{"players":{"1":{"hand":7}}},
           "game":{"living":2,"round":2}}},

{"name":"Two unwounded Standers split the pot equally; the Ducker gets nothing (wounds decide the equal cash)","rule":"R13","players":3,
 "given":{"players":{"2":{"wounds":1}},"game":{"round":7}},
 "rules":[{"seat":1,"options_include":2},{"seat":1,"options_include":"Click"},{"seat":1,"options_include":"Stand"},
          {"seat":2,"options_include":1},{"seat":2,"options_include":"Click"},{"seat":2,"options_include":"Stand"},
          {"seat":3,"options_include":1},{"seat":3,"options_include":"Click"},{"seat":3,"options_include":"Duck"}],
 "expect":{"winner":2,"standings":{"3":1000000},"players":{"3":{"cash":0}},"game":{"round":8}}},

{"name":"Everyone Ducks: the pot is lost","rule":"R14","players":3,"rounds":1,
 "given":{"players":{"1":{"cash":2},"2":{"cash":3},"3":{"cash":4}}},
 "rules":[{"seat":1,"options_include":2},{"seat":1,"options_include":"Click"},{"seat":1,"options_include":"Duck"},
          {"seat":2,"options_include":3},{"seat":2,"options_include":"Click"},{"seat":2,"options_include":"Duck"},
          {"seat":3,"options_include":1},{"seat":3,"options_include":"Click"},{"seat":3,"options_include":"Duck"}],
 "expect":{"players":{"1":{"cash":2},"2":{"cash":3},"3":{"cash":4}}}},

{"name":"A Ducker and a wounded Stander gain no cash","rule":"R15","players":3,"rounds":1,
 "given":{"players":{"1":{"cash":2},"2":{"cash":3}}},
 "rules":[{"seat":1,"options_include":2},{"seat":1,"options_include":"Click"},{"seat":1,"options_include":"Duck"},
          {"seat":2,"options_include":3},{"seat":2,"options_include":"Click"},{"seat":2,"options_include":"Stand"},
          {"seat":3,"options_include":2},{"seat":3,"options_include":"Bang"},{"seat":3,"options_include":"Stand"}],
 "expect":{"players":{"1":{"cash":2,"wounds":0},"2":{"cash":3,"wounds":1},"3":{"wounds":0}}}},

{"name":"Last survivor wins","rule":"R16","players":3,
 "given":{"players":{"1":{"wounds":2},"3":{"alive":false,"wounds":3}},"game":{"living":2}},
 "rules":[{"seat":1,"options_include":2},{"seat":1,"options_include":"Click"},{"seat":1,"options_include":"Stand"},
          {"seat":2,"options_include":1},{"seat":2,"options_include":"Bang"},{"seat":2,"options_include":"Stand"}],
 "expect":{"winner":2,"players":{"1":{"alive":false,"wounds":3},"2":{"alive":true}},"game":{"living":1}}},

{"name":"Both last players eliminate each other: no winner","rule":"R17","players":3,
 "given":{"players":{"1":{"wounds":2,"cash":4},"2":{"wounds":2,"cash":1},"3":{"alive":false,"wounds":3}},"game":{"living":2}},
 "rules":[{"seat":1,"options_include":2},{"seat":1,"options_include":"Bang"},{"seat":1,"options_include":"Stand"},
          {"seat":2,"options_include":1},{"seat":2,"options_include":"Bang"},{"seat":2,"options_include":"Stand"}],
 "expect":{"winner":null,"players":{"1":{"alive":false,"wounds":3,"cash":4},"2":{"alive":false,"wounds":3,"cash":1}},"game":{"living":0}}},

{"name":"After round 8 the richest living player wins","rule":"R18","players":3,
 "given":{"players":{"1":{"cash":10},"2":{"cash":3},"3":{"cash":1}},"game":{"round":7}},
 "rules":[{"seat":1,"options_include":2},{"seat":1,"options_include":"Click"},{"seat":1,"options_include":"Duck"},
          {"seat":2,"options_include":3},{"seat":2,"options_include":"Click"},{"seat":2,"options_include":"Duck"},
          {"seat":3,"options_include":1},{"seat":3,"options_include":"Click"},{"seat":3,"options_include":"Duck"}],
 "expect":{"winner":1,"standings":{"1":1010000,"2":1003000,"3":1001000},"game":{"round":8}}},

{"name":"Cash tie broken by most wounds","rule":"R19","players":3,
 "given":{"players":{"1":{"cash":4,"wounds":2},"2":{"cash":4,"wounds":1},"3":{"cash":1}},"game":{"round":7}},
 "rules":[{"seat":1,"options_include":2},{"seat":1,"options_include":"Click"},{"seat":1,"options_include":"Duck"},
          {"seat":2,"options_include":3},{"seat":2,"options_include":"Click"},{"seat":2,"options_include":"Duck"},
          {"seat":3,"options_include":1},{"seat":3,"options_include":"Click"},{"seat":3,"options_include":"Duck"}],
 "expect":{"winner":1,"standings":{"1":1004002,"2":1004001,"3":1001000}}},

{"name":"Tied on cash and wounds: shared win","rule":"R19","players":3,
 "given":{"players":{"1":{"cash":4,"wounds":1},"2":{"cash":4,"wounds":1},"3":{"cash":1}},"game":{"round":7}},
 "rules":[{"seat":1,"options_include":2},{"seat":1,"options_include":"Click"},{"seat":1,"options_include":"Duck"},
          {"seat":2,"options_include":3},{"seat":2,"options_include":"Click"},{"seat":2,"options_include":"Duck"},
          {"seat":3,"options_include":1},{"seat":3,"options_include":"Click"},{"seat":3,"options_include":"Duck"}],
 "expect":{"winner":[1,2],"standings":{"1":1004001,"2":1004001,"3":1001000}}},

{"name":"Eliminated rich player cannot win","rule":"R20","players":3,
 "given":{"players":{"1":{"cash":5},"2":{"cash":2},"3":{"alive":false,"wounds":3,"cash":100}},"game":{"round":7,"living":2}},
 "rules":[{"seat":1,"options_include":2},{"seat":1,"options_include":"Click"},{"seat":1,"options_include":"Duck"},
          {"seat":2,"options_include":1},{"seat":2,"options_include":"Click"},{"seat":2,"options_include":"Duck"}],
 "expect":{"winner":1,"standings":{"1":1005000,"2":1002000,"3":100003},"players":{"3":{"cash":100,"alive":false}}}}
]
````
