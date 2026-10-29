# 16 scenarios

- time: 2026-10-27T17:51:14+00:00 (125.6s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 23cf1bece7c7ac6e, reply sha256 ef1acecc4489d302

## Sent

````
SPEC:
{
  "name": "Red3 Duel",
  "summary": "A Red7-style shedding duel: on your turn play a card to your palette and/or change the Canvas rule so that you lead under it, or you are out; the last player alive wins the hand, and points across hands win the match.",
  "players": {
    "min": 2,
    "max": 3,
    "suggested": 2
  },
  "parameters": {
    "card_numbers_min": 1,
    "card_numbers_max": 7,
    "colours": 3,
    "deck_size": 21,
    "rank_red": 3,
    "rank_green": 2,
    "rank_violet": 1,
    "strength_number_multiplier": 10,
    "key_count_multiplier": 100,
    "hand_size": 5,
    "palette_start_size": 1,
    "set_aside_2p": 9,
    "set_aside_3p": 3,
    "winner_points_2p": 1,
    "loser_points_2p": 0,
    "winner_points_3p": 2,
    "second_points_3p": 1,
    "first_out_points_3p": 0,
    "target_points_2p": 3,
    "target_points_3p": 6,
    "round_cap": 40,
    "even_number_1": 2,
    "even_number_2": 4,
    "even_number_3": 6,
    "low_number_max": 3
  },
  "attributes": {
    "player": [
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "Cards in the player's hidden hand. Each card is stored as its strength (number*10 + colour rank, e.g. 73 = 7 Red).",
        "observable": false
      },
      {
        "key": "palette",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Face-up cards in the player's palette, stored as strengths.",
        "observable": true
      },
      {
        "key": "alive",
        "type": "bool",
        "visible": "public",
        "initial": true,
        "meaning": "Whether the player is still in the current hand.",
        "observable": true
      },
      {
        "key": "key_value",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The player's KEY under the current Canvas rule, recomputed after every turn.",
        "observable": false
      },
      {
        "key": "elim_order",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "0 while alive this hand. Otherwise, the order in which the player was eliminated this hand (1 = first out).",
        "observable": false
      },
      {
        "key": "acted_this_round",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "Whether the player has taken their turn in the current round.",
        "observable": false
      },
      {
        "key": "points",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Match points (the score).",
        "observable": true
      },
      {
        "key": "is_recent_winner",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "1 if this player won the most recently completed hand, else 0.",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [
          11,
          12,
          13,
          21,
          22,
          23,
          31,
          32,
          33,
          41,
          42,
          43,
          51,
          52,
          53,
          61,
          62,
          63,
          71,
          72,
          73
        ],
        "meaning": "The undealt cards during dealing. It is rebuilt to all 21 cards at each new hand.",
        "observable": false
      },
      {
        "key": "set_aside",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "Cards set aside unseen for the current hand (9 with 2 players, 3 with 3 players).",
        "observable": false
      },
      {
        "key": "canvas",
        "type": "number",
        "visible": "public",
        "initial": 3,
        "meaning": "Current rule colour: 3 = Red, 2 = Green, 1 = Violet.",
        "observable": true
      },
      {
        "key": "turn_seat",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat whose turn it is.",
        "observable": false
      },
      {
        "key": "eliminated_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "How many players have been eliminated in the current hand.",
        "observable": false
      },
      {
        "key": "alive_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of living players in the current hand.",
        "observable": false
      },
      {
        "key": "hand_over",
        "type": "bool",
        "visible": "public",
        "initial": true,
        "meaning": "True when no hand is in progress, so that a new hand is set up at the start of the next round.",
        "observable": false
      },
      {
        "key": "most_recent_winner",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat of the most recent hand winner (0 = none yet).",
        "observable": true
      },
      {
        "key": "round_no",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of completed rounds.",
        "observable": true
      }
    ]
  },
  "setup": [
    "Every player starts with 0 points and is_recent_winner 0. most_recent_winner is 0 and round_no is 0.",
    "hand_over is set to true, so the first round begins by setting up a hand."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "when": "hand_over",
      "effect": "New hand: deck = all 21 strengths [11..73]. For every player: hand = [], palette = [], alive = true, elim_order = 0. Set eliminated_count = 0, alive_count = number of players, canvas = 3 (Red)."
    },
    {
      "action": "update",
      "who": "each player in turn",
      "answer": null,
      "when": "hand_over",
      "effect": "Deal: for each player, 5 times move a random card from deck to that player's hand, then move 1 random card from deck to that player's palette."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "when": "hand_over",
      "effect": "Move all remaining deck cards to set_aside (9 with 2 players, 3 with 3 players). Compute key_value under Red (max of palette) for everyone. Set turn_seat = the next seat in seat order after the player with the highest palette strength. Set hand_over = false. Announce palettes and the Canvas."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Start of round: acted_this_round = false for every player."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player sees their own hand plus all palettes, the canvas, alive flags, points and most_recent_winner."
    },
    {
      "action": "repeat",
      "who": "each living player in turn, starting at turn_seat",
      "answer": null,
      "effect": "Repeat the next four steps (turn, resolve, hand end, pass) until hand_over is true or every living player has acted_this_round = true."
    },
    {
      "action": "ask",
      "who": "the player at turn_seat",
      "answer": "one option: 'play X', 'discard X', 'play X then discard Y' (X != Y, both in hand), or 'fold'; only 'fold' if the hand is empty",
      "effect": "Play X: move X from hand to palette. Discard X: remove X from hand (it leaves play) and set canvas = X mod 10. Play X then discard Y: do both, in that order. Fold: nothing moves. In every case set acted_this_round = true."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Recompute key_value for every living player under canvas. Red (3): max strength in palette. Green (2): 100 * count of palette cards with floor(s/10) in {2,4,6} + max such strength, or 0 if none. Violet (1): 100 * count of palette cards with floor(s/10) <= 3 + max such strength, or 0 if none. If the acting player folded, or their key_value is not strictly greater than every other living player's key_value: alive = false, eliminated_count += 1, elim_order = eliminated_count, alive_count -= 1. Announce the action, the canvas and any elimination."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "when": "alive_count == 1",
      "effect": "Hand ends and the survivor is the hand winner. With 2 players: winner points += 1 (the other gets 0). With 3 players: winner points += 2, the player with elim_order 2 points += 1, the player with elim_order 1 points += 0. Set is_recent_winner = 1 for the winner and 0 for everyone else, most_recent_winner = winner's seat, hand_over = true. Announce the points."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "when": "not hand_over",
      "effect": "turn_seat = the next living seat in seat order after the seat that just acted."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round_no += 1."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the match if (number of players == 2 and any player's points >= 3) or (number of players == 3 and hand_over and any player's points >= 6) or round_no >= 40. Otherwise continue to the next round."
    }
  ],
  "ending": {
    "condition": "(player_count == 2 and max(points) >= 3) or (player_count == 3 and hand_over and max(points) >= 6) or round_no >= 40",
    "rank_by": "you.points * 10 + you.is_recent_winner",
    "min_to_win": 1,
    "decided_by": "Most points wins. Among players tied on points, the one who won the most recently completed hand wins. If no hand was ever completed, nobody reaches the bar of 1 and the match is a draw with no winner."
  },
  "rules": [
    {
      "id": "R1",
      "text": "The deck has 21 cards, numbers 1 to 7 in Red (rank 3), Green (rank 2) and Violet (rank 1), and each card's strength is number*10 + rank (7 Red = 73, 4 Violet = 41)."
    },
    {
      "id": "R2",
      "text": "When a hand is set up, each player gets 5 hidden hand cards and 1 face-up palette card, and the rest (9 with 2 players, 3 with 3 players) go to set_aside unseen."
    },
    {
      "id": "R3",
      "text": "When a hand is set up, canvas is Red (3), every player is alive, and the first turn goes to the next seat after the player whose palette card has the highest strength."
    },
    {
      "id": "R4",
      "text": "When the canvas is Red, a player's key is the highest strength in their palette."
    },
    {
      "id": "R5",
      "text": "When the canvas is Green, a player's key is 100 * (number of palette cards numbered 2, 4 or 6) + the strength of the highest such card, or 0 if they have none."
    },
    {
      "id": "R6",
      "text": "When the canvas is Violet, a player's key is 100 * (number of palette cards numbered 1, 2 or 3) + the strength of the highest such card, or 0 if they have none."
    },
    {
      "id": "R7",
      "text": "A player is leading only if their key is strictly higher than every other living player's key; tied players, including ties at 0, are not leading."
    },
    {
      "id": "R8",
      "text": "When a player plays a card, it moves from their hand to their palette."
    },
    {
      "id": "R9",
      "text": "When a player discards a card, it leaves their hand and play entirely, and the canvas becomes that card's colour."
    },
    {
      "id": "R10",
      "text": "When a player plays then discards, the two cards must be different, and the play happens before the discard."
    },
    {
      "id": "R11",
      "text": "When, after their action, the acting player is not leading under the current canvas, they are eliminated (alive = false)."
    },
    {
      "id": "R12",
      "text": "When a player folds, they are eliminated."
    },
    {
      "id": "R13",
      "text": "When a player has no cards in hand on their turn, their only option is to fold."
    },
    {
      "id": "R14",
      "text": "When a player is eliminated, their palette stays visible but their key no longer counts against others."
    },
    {
      "id": "R15",
      "text": "After a turn, play passes to the next living player in seat order."
    },
    {
      "id": "R16",
      "text": "A round is one pass of turns through all living players in seat order, starting with the player whose turn it is."
    },
    {
      "id": "R17",
      "text": "When only one player is alive, the hand ends immediately and that player is the hand winner and the most recent hand winner."
    },
    {
      "id": "R18",
      "text": "With 2 players, the hand winner scores 1 point and the other scores 0."
    },
    {
      "id": "R19",
      "text": "With 3 players, the hand winner scores 2 points, the second player eliminated scores 1, and the first player eliminated scores 0."
    },
    {
      "id": "R20",
      "text": "When a hand ends and the match is not over, a new hand is set up at the start of the next round."
    },
    {
      "id": "R21",
      "text": "With 2 players, the match ends when a player reaches 3 points."
    },
    {
      "id": "R22",
      "text": "With 3 players, the match ends after a hand in which a player reaches 6 or more points."
    },
    {
      "id": "R23",
      "text": "When round 40 is complete, the match ends and an unfinished hand scores nothing."
    },
    {
      "id": "R24",
      "text": "The player with the most points wins; a tie on points goes to the tied player who won the most recently completed hand; if no hand was completed, the match is a draw."
    }
  ],
  "offers": [
    {
      "question": "Your turn: choose an action",
      "who": "the player at turn_seat (living)",
      "options": "With an empty hand: fold only. With exactly 1 card X in hand: play X, discard X, fold. With 2 or more cards: play X for each X in hand; discard X for each X in hand; play X then discard Y for each ordered pair of different cards X, Y in hand; fold."
    }
  ],
  "choices": [
    {
      "what": "2 to 3 players, suggested 2",
      "why": "The designer's suggested size is 2, which keeps it a pure duel of reading the rival's palette and timing rule changes. The minimum is 2 because a duel needs a rival. The maximum is 3 because the deck and the scoring are only defined for 2 or 3 players."
    },
    {
      "what": "Cards are stored as their strength numbers (11 to 73)",
      "why": "Number = floor(s/10) and colour = s mod 10, so every key is plain arithmetic on the list."
    },
    {
      "what": "Even numbers listed as three separate parameters (even_number_1..3 = 2, 4, 6)",
      "why": "Parameters must be single numbers."
    },
    {
      "what": "No talk step",
      "why": "The rules say there is no table talk."
    },
    {
      "what": "Turns use sequential ask",
      "why": "Turns are taken one at a time in seat order, and each player sees the result of the turns before."
    },
    {
      "what": "The draw when no hand was completed is made with min_to_win 1",
      "why": "With no completed hand everyone ranks at 0 and nobody qualifies, giving no winner. Any completed hand gives someone at least 1 point."
    },
    {
      "what": "A player's strategy",
      "why": "Hold back strong cards. Switch the rule only when a discard both keeps you leading and leaves the rival needing cards they may not have. Read what a rival's palette implies about their hand."
    }
  ],
  "simplifications": [
    {
      "what": "Naming a card not held is never offered",
      "why": "Options are built from the player's hand, so the 'named a card you do not hold' elimination cannot arise."
    },
    {
      "what": "The turns within a round are a repeat loop over living players who have not yet acted",
      "why": "Turn order starts at turn_seat and must skip eliminated seats, and the loop must stop the moment a hand ends."
    },
    {
      "what": "The new-hand setup is a set of update steps each guarded by 'when hand_over'",
      "why": "The step list is flat, so the setup steps run only when a new hand is needed."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: palette, alive, points, is_recent_winner; table: canvas, most_recent_winner, round_no.

EARLIER TESTS FOR THIS SPEC WERE FOUND WRONG. What to do differently:
Rewrite the move-matching rules to use the game's actual option labels: '<number> <Colour>' for a card, for example 'play 7 Red', 'play 1 Violet', 'discard 4 Violet', plus 'fold'. Alternatively, match loosely on the action word plus the card's number and colour name. Do not assume options are named by strength values. Keep checking results through public attributes: palette (stored as strengths), alive, points, is_recent_winner, canvas, most_recent_winner. For R4–R7, set up the palettes so the expected leader and eliminated player follow from the rules, and assert on alive and points, not on internal fields like key_value. In R9, make sure the scripted move is the discard ('discard 4 Violet'), not the play, then assert canvas == 1 and that the card is not in any palette.
````

## Reply

````
[
{"name":"R1: card 7 Red is stored as strength 73 when played to the palette","rule":"R1","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"hand_over":false,"turn_seat":1,"alive_count":2,"eliminated_count":0,"canvas":3,"deck":[],"round_no":0},
  "players":{"1":{"hand":[73,12],"palette":[41],"alive":true,"elim_order":0,"points":0},
             "2":{"hand":[],"palette":[52],"alive":true,"elim_order":0,"points":0}}},
 "rules":[{"seat":1,"options_include":"play 7 Red"},{"seat":2,"options_include":"fold","times":"all"}],
 "expect":{"players":{"1":{"palette":[41,73],"alive":true,"points":1},"2":{"alive":false,"points":0}}}},

{"name":"R2: 2-player deal gives 5 hand cards, 1 palette card, 9 set aside (counts only, deal is random)","rule":"R2","players":2,"rounds":1,"default":"decline",
 "rules":[{"seat":1,"options_include":"fold","times":"all"},{"seat":2,"options_include":"fold","times":"all"}],
 "expect":{"lens":{"game":{"set_aside":9,"deck":0},"players":{"1":{"hand":5,"palette":1},"2":{"hand":5,"palette":1}}}}},

{"name":"R2: 3-player deal gives 5 hand cards, 1 palette card, 3 set aside (counts only, deal is random)","rule":"R2","players":3,"rounds":1,"default":"decline",
 "rules":[{"seat":1,"options_include":"fold","times":"all"},{"seat":2,"options_include":"fold","times":"all"},{"seat":3,"options_include":"fold","times":"all"}],
 "expect":{"lens":{"game":{"set_aside":3,"deck":0},"players":{"1":{"hand":5,"palette":1},"2":{"hand":5,"palette":1},"3":{"hand":5,"palette":1}}}}},

{"name":"R3: a new hand resets the canvas to Red and deals fresh palettes (deal is random)","rule":"R3","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"canvas":1,"hand_over":true},"players":{"1":{"palette":[11,22,33],"alive":false},"2":{"palette":[41,52],"alive":false}}},
 "rules":[{"seat":1,"options_include":"fold","times":"all"},{"seat":2,"options_include":"fold","times":"all"}],
 "expect":{"game":{"canvas":3},"lens":{"players":{"1":{"palette":1},"2":{"palette":1}}}}},

{"name":"R4: under Red the key is the highest palette strength; 41+33 does not beat 52","rule":"R4","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"hand_over":false,"turn_seat":1,"alive_count":2,"eliminated_count":0,"canvas":3,"deck":[],"round_no":0},
  "players":{"1":{"hand":[33,12],"palette":[41],"alive":true,"elim_order":0,"points":0},
             "2":{"hand":[],"palette":[52],"alive":true,"elim_order":0,"points":0}}},
 "rules":[{"seat":1,"options_include":"play 3 Red"}],
 "expect":{"players":{"1":{"palette":[41,33],"alive":false,"points":0},"2":{"alive":true,"points":1,"is_recent_winner":1}},"game":{"most_recent_winner":2}}},

{"name":"R5: under Green two even cards (241) beat one even card (163)","rule":"R5","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"hand_over":false,"turn_seat":1,"alive_count":2,"eliminated_count":0,"canvas":2,"deck":[],"round_no":0},
  "players":{"1":{"hand":[41,13],"palette":[21],"alive":true,"elim_order":0,"points":0},
             "2":{"hand":[],"palette":[63,73],"alive":true,"elim_order":0,"points":0}}},
 "rules":[{"seat":1,"options_include":"play 4 Violet"},{"seat":2,"options_include":"fold","times":"all"}],
 "expect":{"players":{"1":{"palette":[21,41],"alive":true,"points":1},"2":{"alive":false,"points":0}},"game":{"canvas":2}}},

{"name":"R6: under Violet two low cards (221) beat one low card (133)","rule":"R6","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"hand_over":false,"turn_seat":1,"alive_count":2,"eliminated_count":0,"canvas":1,"deck":[],"round_no":0},
  "players":{"1":{"hand":[21,73],"palette":[13],"alive":true,"elim_order":0,"points":0},
             "2":{"hand":[],"palette":[33,73],"alive":true,"elim_order":0,"points":0}}},
 "rules":[{"seat":1,"options_include":"play 2 Violet"},{"seat":2,"options_include":"fold","times":"all"}],
 "expect":{"players":{"1":{"palette":[13,21],"alive":true,"points":1},"2":{"alive":false,"points":0}},"game":{"canvas":1}}},

{"name":"R7: a tie at 0 under Green is not leading, so the actor is eliminated","rule":"R7","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"hand_over":false,"turn_seat":1,"alive_count":2,"eliminated_count":0,"canvas":2,"deck":[],"round_no":0},
  "players":{"1":{"hand":[53,11],"palette":[71],"alive":true,"elim_order":0,"points":0},
             "2":{"hand":[],"palette":[51],"alive":true,"elim_order":0,"points":0}}},
 "rules":[{"seat":1,"options_include":"play 5 Red"}],
 "expect":{"players":{"1":{"alive":false,"points":0},"2":{"alive":true,"points":1}}}},

{"name":"R8: playing 6 Green moves it from the hand to the palette","rule":"R8","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"hand_over":false,"turn_seat":1,"alive_count":2,"eliminated_count":0,"canvas":3,"deck":[],"round_no":0},
  "players":{"1":{"hand":[62,31],"palette":[11],"alive":true,"elim_order":0,"points":0},
             "2":{"hand":[],"palette":[52],"alive":true,"elim_order":0,"points":0}}},
 "rules":[{"seat":1,"options_include":"play 6 Green"},{"seat":2,"options_include":"fold","times":"all"}],
 "expect":{"players":{"1":{"palette":[11,62],"alive":true}},"lens":{"players":{"1":{"hand":1,"palette":2}}}}},

{"name":"R9: discarding 4 Violet sets the canvas to Violet and the card goes to no palette","rule":"R9","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"hand_over":false,"turn_seat":1,"alive_count":2,"eliminated_count":0,"canvas":3,"deck":[],"round_no":0},
  "players":{"1":{"hand":[41,72],"palette":[13],"alive":true,"elim_order":0,"points":0},
             "2":{"hand":[],"palette":[52],"alive":true,"elim_order":0,"points":0}}},
 "rules":[{"seat":1,"options_include":"discard 4 Violet"},{"seat":2,"options_include":"fold","times":"all"}],
 "expect":{"game":{"canvas":1},"players":{"1":{"palette":[13],"alive":true,"points":1},"2":{"palette":[52],"alive":false}},
  "lens":{"players":{"1":{"hand":1,"palette":1},"2":{"palette":1}}}}},

{"name":"R10: play 2 Green then discard 4 Violet does both, and a card cannot be paired with itself","rule":"R10","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"hand_over":false,"turn_seat":1,"alive_count":2,"eliminated_count":0,"canvas":3,"deck":[],"round_no":0},
  "players":{"1":{"hand":[22,41],"palette":[13],"alive":true,"elim_order":0,"points":0},
             "2":{"hand":[],"palette":[52],"alive":true,"elim_order":0,"points":0}}},
 "rules":[{"seat":1,"options_include":"play 2 Green then discard 4 Violet"},{"seat":2,"options_include":"fold","times":"all"}],
 "expect":{"game":{"canvas":1},"players":{"1":{"palette":[13,22],"alive":true,"points":1},"2":{"alive":false}},
  "lens":{"players":{"1":{"hand":0}}},
  "not_offered":[{"seat":1,"option":"play 2 Green then discard 2 Green"},{"seat":1,"option":"play 4 Violet then discard 4 Violet"}]}},

{"name":"R11: a play that leaves the actor behind under Red eliminates them; their palette stays","rule":"R11","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"hand_over":false,"turn_seat":1,"alive_count":2,"eliminated_count":0,"canvas":3,"deck":[],"round_no":0},
  "players":{"1":{"hand":[52,13],"palette":[41],"alive":true,"elim_order":0,"points":0},
             "2":{"hand":[],"palette":[63],"alive":true,"elim_order":0,"points":0}}},
 "rules":[{"seat":1,"options_include":"play 5 Green"}],
 "expect":{"players":{"1":{"palette":[41,52],"alive":false,"points":0},"2":{"alive":true,"points":1}}}},

{"name":"R12: folding eliminates even a leading player","rule":"R12","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"hand_over":false,"turn_seat":1,"alive_count":2,"eliminated_count":0,"canvas":3,"deck":[],"round_no":0},
  "players":{"1":{"hand":[11],"palette":[73],"alive":true,"elim_order":0,"points":0},
             "2":{"hand":[12],"palette":[52],"alive":true,"elim_order":0,"points":0}}},
 "rules":[{"seat":1,"options_include":"fold"}],
 "expect":{"players":{"1":{"palette":[73],"alive":false,"points":0},"2":{"alive":true,"points":1,"is_recent_winner":1}},"game":{"most_recent_winner":2}}},

{"name":"R13: with an empty hand the only option is fold, so the player is eliminated","rule":"R13","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"hand_over":false,"turn_seat":1,"alive_count":2,"eliminated_count":0,"canvas":3,"deck":[],"round_no":0},
  "players":{"1":{"hand":[],"palette":[73],"alive":true,"elim_order":0,"points":0},
             "2":{"hand":[12],"palette":[52],"alive":true,"elim_order":0,"points":0}}},
 "rules":[],
 "expect":{"players":{"1":{"alive":false,"points":0},"2":{"points":1}},
  "offered":[{"seat":1,"option":"fold"}],"not_offered":[{"seat":1,"option":"play 1 Green"},{"seat":1,"option":"discard 1 Green"}]}},

{"name":"R14: an eliminated player's high palette stays visible but does not count against others","rule":"R14","players":3,"rounds":1,"default":"decline",
 "given":{"game":{"hand_over":false,"turn_seat":1,"alive_count":2,"eliminated_count":1,"canvas":3,"deck":[],"round_no":0},
  "players":{"1":{"hand":[52],"palette":[41],"alive":true,"elim_order":0,"points":0},
             "2":{"hand":[],"palette":[73],"alive":false,"elim_order":1,"points":0},
             "3":{"hand":[],"palette":[43],"alive":true,"elim_order":0,"points":0}}},
 "rules":[{"seat":1,"options_include":"play 5 Green"},{"seat":3,"options_include":"fold","times":"all"}],
 "expect":{"players":{"1":{"palette":[41,52],"alive":true,"points":2},"2":{"palette":[73],"alive":false,"points":0},"3":{"alive":false,"points":1}}}},

{"name":"R15: play passes to the next living seat, skipping an eliminated one","rule":"R15","players":3,"rounds":1,"default":"decline",
 "given":{"game":{"hand_over":false,"turn_seat":1,"alive_count":2,"eliminated_count":1,"canvas":3,"deck":[],"round_no":0},
  "players":{"1":{"hand":[62],"palette":[51],"alive":true,"elim_order":0,"points":0},
             "2":{"hand":[],"palette":[12],"alive":false,"elim_order":1,"points":0},
             "3":{"hand":[11],"palette":[43],"alive":true,"elim_order":0,"points":0}}},
 "rules":[{"seat":1,"options_include":"play 6 Green"},{"seat":3,"options_include":"play 1 Violet"}],
 "expect":{"players":{"1":{"palette":[51,62],"alive":true,"points":2},"3":{"palette":[43,11],"alive":false,"points":1},"2":{"points":0}},
  "not_offered":[{"seat":2,"option":"fold"}]}},

{"name":"R16: one round is one turn for each living player, then it stops","rule":"R16","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"hand_over":false,"turn_seat":1,"alive_count":2,"eliminated_count":0,"canvas":3,"deck":[],"round_no":0},
  "players":{"1":{"hand":[52,13],"palette":[41],"alive":true,"elim_order":0,"points":0},
             "2":{"hand":[63,12],"palette":[43],"alive":true,"elim_order":0,"points":0}}},
 "rules":[{"seat":1,"options_include":"play 5 Green"},{"seat":2,"options_include":"play 6 Red"}],
 "expect":{"players":{"1":{"palette":[41,52],"alive":true,"points":0},"2":{"palette":[43,63],"alive":true,"points":0}},
  "game":{"round_no":1},"lens":{"players":{"1":{"hand":1},"2":{"hand":1}}}}},

{"name":"R17: when only one player is left the hand ends at once and the survivor is the recent winner","rule":"R17","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"hand_over":false,"turn_seat":1,"alive_count":2,"eliminated_count":0,"canvas":3,"deck":[],"round_no":0},
  "players":{"1":{"hand":[11],"palette":[41],"alive":true,"elim_order":0,"points":0},
             "2":{"hand":[12],"palette":[43],"alive":true,"elim_order":0,"points":0}}},
 "rules":[{"seat":1,"options_include":"fold"}],
 "expect":{"players":{"1":{"alive":false,"is_recent_winner":0},"2":{"palette":[43],"alive":true,"points":1,"is_recent_winner":1}},
  "game":{"most_recent_winner":2},"not_offered":[{"seat":2,"option":"play 1 Green"}]}},

{"name":"R18: with 2 players the hand winner scores 1 and the loser 0","rule":"R18","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"hand_over":false,"turn_seat":1,"alive_count":2,"eliminated_count":0,"canvas":3,"deck":[],"round_no":0},
  "players":{"1":{"hand":[73],"palette":[11],"alive":true,"elim_order":0,"points":1,"is_recent_winner":0},
             "2":{"hand":[],"palette":[52],"alive":true,"elim_order":0,"points":1,"is_recent_winner":1}}},
 "rules":[{"seat":1,"options_include":"play 7 Red"},{"seat":2,"options_include":"fold","times":"all"}],
 "expect":{"players":{"1":{"points":2,"is_recent_winner":1},"2":{"points":1,"is_recent_winner":0}},"game":{"most_recent_winner":1}}},

{"name":"R19: with 3 players the winner scores 2, second out 1, first out 0","rule":"R19","players":3,"rounds":1,"default":"decline",
 "given":{"game":{"hand_over":false,"turn_seat":1,"alive_count":3,"eliminated_count":0,"canvas":3,"deck":[],"round_no":0},
  "players":{"1":{"hand":[],"palette":[73],"alive":true,"elim_order":0,"points":0},
             "2":{"hand":[],"palette":[52],"alive":true,"elim_order":0,"points":0},
             "3":{"hand":[],"palette":[11],"alive":true,"elim_order":0,"points":0}}},
 "rules":[],
 "expect":{"players":{"1":{"alive":false,"points":0},"2":{"alive":false,"points":1},"3":{"alive":true,"points":2,"is_recent_winner":1}},"game":{"most_recent_winner":3}}},

{"name":"R20: after a finished hand the next round sets up a new hand (counts only, deal is random)","rule":"R20","players":2,"rounds":1,"default":"decline",
 "given":{"game":{"hand_over":true,"canvas":2,"most_recent_winner":1,"round_no":3},
  "players":{"1":{"hand":[],"palette":[11,22,33],"alive":true,"points":1,"is_recent_winner":1},
             "2":{"hand":[],"palette":[41,52],"alive":false,"points":0,"is_recent_winner":0}}},
 "rules":[{"seat":1,"options_include":"fold","times":"all"},{"seat":2,"options_include":"fold","times":"all"}],
 "expect":{"game":{"canvas":3,"round_no":4},"lens":{"game":{"set_aside":9},"players":{"1":{"hand":5,"palette":1},"2":{"hand":5,"palette":1}}}}},

{"name":"R21: with 2 players the match ends when a player reaches 3 points","rule":"R21","players":2,"default":"decline",
 "given":{"game":{"hand_over":false,"turn_seat":1,"alive_count":2,"eliminated_count":0,"canvas":3,"deck":[],"round_no":5},
  "players":{"1":{"hand":[11],"palette":[41],"alive":true,"elim_order":0,"points":2,"is_recent_winner":0},
             "2":{"hand":[],"palette":[32],"alive":true,"elim_order":0,"points":2,"is_recent_winner":1}}},
 "rules":[{"seat":1,"options_include":"play 1 Violet"},{"seat":2,"options_include":"fold","times":"all"}],
 "expect":{"winner":1,"standings":{"1":31,"2":20},"players":{"1":{"points":3},"2":{"points":2}}}},

{"name":"R22: with 3 players the match ends after a hand in which a player reaches 6","rule":"R22","players":3,"default":"decline",
 "given":{"game":{"hand_over":false,"turn_seat":1,"alive_count":3,"eliminated_count":0,"canvas":3,"deck":[],"round_no":5},
  "players":{"1":{"hand":[11],"palette":[41],"alive":true,"elim_order":0,"points":4,"is_recent_winner":0},
             "2":{"hand":[],"palette":[32],"alive":true,"elim_order":0,"points":5,"is_recent_winner":1},
             "3":{"hand":[],"palette":[21],"alive":true,"elim_order":0,"points":0,"is_recent_winner":0}}},
 "rules":[{"seat":1,"options_include":"play 1 Violet"}],
 "expect":{"winner":1,"standings":{"1":61,"2":50,"3":10},"players":{"1":{"points":6},"2":{"points":5},"3":{"points":1}}}},

{"name":"R23: after round 40 the match ends and the unfinished hand scores nothing","rule":"R23","players":2,"default":"decline",
 "given":{"game":{"hand_over":false,"turn_seat":1,"alive_count":2,"eliminated_count":0,"canvas":3,"deck":[],"round_no":39,"most_recent_winner":1},
  "players":{"1":{"hand":[52,13],"palette":[41],"alive":true,"elim_order":0,"points":1,"is_recent_winner":1},
             "2":{"hand":[63,12],"palette":[43],"alive":true,"elim_order":0,"points":0,"is_recent_winner":0}}},
 "rules":[{"seat":1,"options_include":"play 5 Green"},{"seat":2,"options_include":"play 6 Red"}],
 "expect":{"winner":1,"standings":{"1":11,"2":0},"game":{"round_no":40},"players":{"1":{"points":1,"alive":true},"2":{"points":0,"alive":true}}}},

{"name":"R24: a tie on points goes to the most recent hand winner","rule":"R24","players":2,"default":"decline",
 "given":{"game":{"hand_over":false,"turn_seat":1,"alive_count":2,"eliminated_count":0,"canvas":3,"deck":[],"round_no":39,"most_recent_winner":2},
  "players":{"1":{"hand":[52,13],"palette":[41],"alive":true,"elim_order":0,"points":2,"is_recent_winner":0},
             "2":{"hand":[63,12],"palette":[43],"alive":true,"elim_order":0,"points":2,"is_recent_winner":1}}},
 "rules":[{"seat":1,"options_include":"play 5 Green"},{"seat":2,"options_include":"play 6 Red"}],
 "expect":{"winner":2,"standings":{"1":20,"2":21}}},

{"name":"R24: with no completed hand the match ends with no winner","rule":"R24","players":2,"default":"decline",
 "given":{"game":{"hand_over":false,"turn_seat":1,"alive_count":2,"eliminated_count":0,"canvas":3,"deck":[],"round_no":39,"most_recent_winner":0},
  "players":{"1":{"hand":[52,13],"palette":[41],"alive":true,"elim_order":0,"points":0,"is_recent_winner":0},
             "2":{"hand":[63,12],"palette":[43],"alive":true,"elim_order":0,"points":0,"is_recent_winner":0}}},
 "rules":[{"seat":1,"options_include":"play 5 Green"},{"seat":2,"options_include":"play 6 Red"}],
 "expect":{"winner":null,"standings":{"1":0,"2":0}}}
]
````
