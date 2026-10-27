# 47 scenarios

- time: 2026-10-27T11:05:26+00:00 (51.4s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 119011b09992cde0, reply sha256 ca7be22bb07e8137

## Sent

````
SPEC:
{
  "name": "Hanamikoji: Five Geisha",
  "summary": "Two players each take four one-shot actions per hand to place Item cards for five Geisha, aiming for 11 Charm or 3 Geisha at the end of each pair of hands.",
  "players": {
    "min": 2,
    "max": 2,
    "suggested": 2
  },
  "parameters": {
    "geisha_count_total": 5,
    "charm_geisha_1": 3,
    "charm_geisha_2": 3,
    "charm_geisha_3": 4,
    "charm_geisha_4": 5,
    "charm_geisha_5": 6,
    "items_total": 21,
    "items_geisha_1": 3,
    "items_geisha_2": 3,
    "items_geisha_3": 4,
    "items_geisha_4": 5,
    "items_geisha_5": 6,
    "removed_per_hand": 1,
    "deal_per_player": 6,
    "deck_after_deal": 8,
    "hands": 4,
    "rounds_per_hand": 8,
    "rounds_total": 32,
    "turns_per_player_per_hand": 4,
    "secret_cards": 1,
    "tradeoff_cards": 2,
    "gift_cards": 3,
    "gift_cards_to_opponent": 1,
    "competition_cards": 4,
    "competition_pair_size": 2,
    "win_charm": 11,
    "win_geisha": 3
  },
  "attributes": {
    "player": [
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "Item cards held privately, each a Geisha number 1-5",
        "observable": false
      },
      {
        "key": "secret",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "0 or 1 face-down card set aside by Secret this hand",
        "observable": false
      },
      {
        "key": "pending",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "cards picked from hand for the current action, in pick order (picks 1-2 are Pair A and picks 3-4 are Pair B in Competition)",
        "observable": false
      },
      {
        "key": "unused_actions",
        "type": "list",
        "visible": "public",
        "initial": [
          "Secret",
          "Trade-off",
          "Gift",
          "Competition"
        ],
        "meaning": "actions not yet taken this hand",
        "observable": false
      },
      {
        "key": "kept",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "cards placed on this player's side, visible to both",
        "observable": true
      },
      {
        "key": "charm",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "total Charm of Geisha whose markers are on this player's side",
        "observable": true
      },
      {
        "key": "geisha_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "number of markers on this player's side",
        "observable": true
      },
      {
        "key": "standing",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "equals charm; the score",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "undealt Item cards this hand",
        "observable": false
      },
      {
        "key": "removed_card",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "the 1 card set aside face-down each hand",
        "observable": false
      },
      {
        "key": "discard",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "Trade-off cards, out of play this hand",
        "observable": false
      },
      {
        "key": "hand_number",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "current hand, 1-4",
        "observable": false
      },
      {
        "key": "round_in_hand",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "current round within the hand, 1-8",
        "observable": false
      },
      {
        "key": "starting_seat",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "seat that acts in odd rounds: 1 in hands 1 and 3, 2 in hands 2 and 4",
        "observable": false
      },
      {
        "key": "active_seat",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "seat taking this round's turn",
        "observable": false
      },
      {
        "key": "last_action",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "action chosen this round",
        "observable": false
      },
      {
        "key": "marker_1",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Geisha 1 marker: 0 middle, 1 Player 1's side, 2 Player 2's side",
        "observable": true
      },
      {
        "key": "marker_2",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Geisha 2 marker: 0 middle, 1 Player 1's side, 2 Player 2's side",
        "observable": true
      },
      {
        "key": "marker_3",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Geisha 3 marker: 0 middle, 1 Player 1's side, 2 Player 2's side",
        "observable": true
      },
      {
        "key": "marker_4",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Geisha 4 marker: 0 middle, 1 Player 1's side, 2 Player 2's side",
        "observable": true
      },
      {
        "key": "marker_5",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Geisha 5 marker: 0 middle, 1 Player 1's side, 2 Player 2's side",
        "observable": true
      },
      {
        "key": "game_over",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "1 once a player has won at a pair end, or hand 4 is complete",
        "observable": false
      }
    ]
  },
  "setup": [
    "Seat 1 is Player 1 and seat 2 is Player 2.",
    "All five markers start in the middle (marker_1 to marker_5 = 0).",
    "hand_number = 1, round_in_hand = 1, starting_seat = 1, game_over = 0.",
    "Each player's kept list is empty, and charm, geisha_count and standing are 0."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When round_in_hand == 1: build deck as the 21 Items (three 1s, three 2s, four 3s, five 4s, six 5s). Draw 1 at random into removed_card. Draw 6 at random into each player's hand; the remaining 8 stay in deck. Set each secret, pending and discard to empty. Set each unused_actions to [Secret, Trade-off, Gift, Competition]. If hand_number is 1 or 3, set each kept to empty; in hands 2 and 4, kept carries over. Markers carry over."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "active_seat = starting_seat if round_in_hand is odd, otherwise the other seat (3 - starting_seat)."
    },
    {
      "action": "update",
      "who": "seat active_seat",
      "answer": null,
      "effect": "Draw 1 card at random from deck (the top of a shuffled deck), append it to the active player's hand and remove it from deck."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player sees their own hand and secret, and both players' kept, unused_actions, markers and counters."
    },
    {
      "action": "ask",
      "who": "seat active_seat",
      "answer": "one of the active player's unused_actions",
      "effect": "last_action = the choice; remove it from the active player's unused_actions."
    },
    {
      "action": "ask",
      "who": "seat active_seat",
      "answer": "one Geisha number present in the active player's hand",
      "effect": "Move that card from hand to pending (pick 1)."
    },
    {
      "action": "ask",
      "who": "seat active_seat",
      "answer": "one Geisha number present in the active player's hand",
      "effect": "When last_action is Trade-off, Gift or Competition: move that card from hand to pending (pick 2)."
    },
    {
      "action": "ask",
      "who": "seat active_seat",
      "answer": "one Geisha number present in the active player's hand",
      "effect": "When last_action is Gift or Competition: move that card from hand to pending (pick 3)."
    },
    {
      "action": "ask",
      "who": "seat active_seat",
      "answer": "one Geisha number present in the active player's hand",
      "effect": "When last_action is Competition: move that card from hand to pending (pick 4). Picks 1-2 form Pair A and picks 3-4 form Pair B."
    },
    {
      "action": "update",
      "who": "seat active_seat",
      "answer": null,
      "effect": "When last_action is Secret: move the 1 pending card to the active player's secret, face-down."
    },
    {
      "action": "update",
      "who": "seat active_seat",
      "answer": null,
      "effect": "When last_action is Trade-off: move the 2 pending cards to discard, face-down."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "When last_action is Gift: announce the 3 pending cards. When last_action is Competition: announce Pair A (picks 1-2) and Pair B (picks 3-4)."
    },
    {
      "action": "ask",
      "who": "the seat that is not active_seat",
      "answer": "one of the 3 revealed Gift cards, by Geisha number",
      "effect": "When last_action is Gift: append the chosen card to the opponent's kept, append the other 2 pending cards to the active player's kept, and empty pending."
    },
    {
      "action": "ask",
      "who": "the seat that is not active_seat",
      "answer": "Pair A or Pair B",
      "effect": "When last_action is Competition: append the chosen pair to the opponent's kept, append the other pair to the active player's kept, and empty pending."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When round_in_hand == 8: reveal each player's secret card, append it to their kept, and empty secret."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When round_in_hand == 8 and hand_number is 2 or 4: (a) for each g in 1-5, count the cards of number g in each player's kept; if Player 1's count is strictly higher, marker_g = 1; if Player 2's is strictly higher, marker_g = 2; on a tie marker_g is unchanged. (b) Each player's charm = sum of the Charm (3,3,4,5,6) of g whose marker_g equals their seat; geisha_count = number of markers equal to their seat; standing = charm. (c) game_over = 1 if either charm >= 11, or either geisha_count >= 3, or hand_number == 4."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "When round_in_hand == 8 and hand_number is 2 or 4: announce marker_1 to marker_5 and each player's charm and geisha_count."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if game_over == 1; otherwise continue."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "If round_in_hand < 8: round_in_hand += 1. Otherwise: round_in_hand = 1, hand_number += 1, starting_seat = 3 - starting_seat."
    }
  ],
  "ending": {
    "condition": "game_over == 1",
    "rank_by": "(you.charm >= 11) * 10000 + (you.geisha_count >= 3) * 1000 + you.charm * 10 + you.geisha_count",
    "decided_by": "A player with 11 or more Charm wins first. Otherwise a player with 3 or more Geisha wins. If nobody has won after hand 4, the higher Charm wins, then the higher Geisha count. Players level on all of these share the result, which is a draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game starts, all 5 markers are in the middle (value 0)."
    },
    {
      "id": "R2",
      "text": "When a hand starts, 1 of the 21 Items is set aside as removed_card, each player is dealt 6 cards, and 8 cards remain in deck."
    },
    {
      "id": "R3",
      "text": "When a hand starts, both secrets and the discard are emptied and both unused_actions are reset to [Secret, Trade-off, Gift, Competition]."
    },
    {
      "id": "R4",
      "text": "When hand 1 or hand 3 starts, both kept lists are emptied; when hand 2 or 4 starts, kept lists and markers are unchanged."
    },
    {
      "id": "R5",
      "text": "Player 1 is starting_seat in hands 1 and 3, and Player 2 in hands 2 and 4."
    },
    {
      "id": "R6",
      "text": "In rounds 1, 3, 5 and 7 the starting seat is active; in rounds 2, 4, 6 and 8 the other seat is active."
    },
    {
      "id": "R7",
      "text": "At the start of each turn the active player draws 1 card from deck into hand."
    },
    {
      "id": "R8",
      "text": "The active player is offered exactly the actions in their unused_actions, and the chosen action is removed from that list."
    },
    {
      "id": "R9",
      "text": "In a player's 4th turn of a hand, exactly one action remains and it must be taken."
    },
    {
      "id": "R10",
      "text": "When Secret is chosen, 1 hand card moves face-down to the player's secret."
    },
    {
      "id": "R11",
      "text": "When Trade-off is chosen, 2 hand cards move face-down to discard and do not score this hand."
    },
    {
      "id": "R12",
      "text": "When Gift is chosen, 3 hand cards are revealed, the opponent picks 1 for their kept, and the other 2 go to the active player's kept."
    },
    {
      "id": "R13",
      "text": "When Competition is chosen, 4 hand cards are revealed as Pair A and Pair B of 2 cards each, the opponent picks one pair for their kept, and the other pair goes to the active player's kept."
    },
    {
      "id": "R14",
      "text": "Cards named for an action must be cards the active player holds."
    },
    {
      "id": "R15",
      "text": "After round 8 of every hand, each player's secret card is appended to their kept."
    },
    {
      "id": "R16",
      "text": "After hands 2 and 4, for each Geisha g, marker_g moves to the side of the player with strictly more g cards in kept; on a tie it stays where it is."
    },
    {
      "id": "R17",
      "text": "After hands 2 and 4, charm = the summed Charm (3,3,4,5,6) of a player's markers, geisha_count = their number of markers, and standing = charm."
    },
    {
      "id": "R18",
      "text": "At a pair end, a player with charm >= 11 wins and the game ends."
    },
    {
      "id": "R19",
      "text": "At a pair end, if no one has charm >= 11, a player with geisha_count >= 3 wins and the game ends."
    },
    {
      "id": "R20",
      "text": "If one player has 11 charm and the other has 3 Geisha, the 11-charm player wins."
    },
    {
      "id": "R21",
      "text": "If no one has won after hand 4, the higher charm wins; if charm is tied, the higher geisha_count wins; otherwise the game is a draw."
    },
    {
      "id": "R22",
      "text": "After hand 2, if no one has won, play continues to hand 3."
    }
  ],
  "offers": [
    {
      "question": "Choose an action",
      "who": "the active seat only",
      "options": "exactly the entries of the active player's unused_actions (4 in the first turn of a hand, 1 in the last)"
    },
    {
      "question": "Pick a card for the action (picks 1-4)",
      "who": "the active seat only",
      "options": "each distinct Geisha number still in the active player's hand; pick 1 always, pick 2 for Trade-off, Gift or Competition, pick 3 for Gift or Competition, pick 4 for Competition only"
    },
    {
      "question": "Choose a Gift card",
      "who": "the non-active seat, only when last_action is Gift",
      "options": "the Geisha numbers of the 3 revealed cards"
    },
    {
      "question": "Choose a Competition pair",
      "who": "the non-active seat, only when last_action is Competition",
      "options": "Pair A, Pair B"
    }
  ],
  "choices": [
    {
      "what": "2 players, min = max = suggested",
      "why": "The designer fixed 2. The Gift and Competition splits are a duel between the active player and one opponent, and the 21-card budget fits exactly two players."
    },
    {
      "what": "Strategy at the table",
      "why": "A thoughtful player hides key Geisha with Secret, offers Gift and Competition splits where every option leaves them ahead, and tracks the visible kept lists to guess what the opponent is holding."
    },
    {
      "what": "No talk step",
      "why": "The source has no negotiation, so none is added."
    },
    {
      "what": "unused_actions is public",
      "why": "The source does not state its visibility; the physical game shows used action tokens face-down, so both players know which actions remain."
    },
    {
      "what": "last_action is public",
      "why": "Which action was taken is visible in the physical game, even when the cards are not."
    },
    {
      "what": "Marker encoded as 0/1/2",
      "why": "Middle / Player 1 side / Player 2 side, so the marker can be used in arithmetic."
    },
    {
      "what": "rank_by weights 10000 / 1000 / 10 / 1",
      "why": "These weights encode the win order: 11 Charm, then 3 Geisha, then Charm, then Geisha count. Charm totals at most 21, so the weights never overlap. Both players cannot reach the same goal, so ties only occur in the final fallback, where a tie is a draw."
    }
  ],
  "simplifications": [
    {
      "what": "Cards for an action are named one pick at a time from the hand list",
      "why": "Choosing from the hand list guarantees the player names only cards they hold, with no free-text parsing."
    },
    {
      "what": "Competition pairs are set by pick order: picks 1-2 are Pair A, picks 3-4 are Pair B",
      "why": "This lets the split be made with sequential single-card choices."
    },
    {
      "what": "Drawing 'the top card' is a random draw from deck",
      "why": "The deck is shuffled, so the two are equivalent."
    },
    {
      "what": "Player-versus-player card counts for markers are compared in one update",
      "why": "The engine has no player-attribute operand, so the comparison is computed at the table level."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: kept, charm, geisha_count, standing; table: marker_1, marker_2, marker_3, marker_4, marker_5.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
[
{"name":"All markers start in the middle","rule":"R1","players":2,"rounds":0,
 "expect":{"game":{"marker_1":0,"marker_2":0,"marker_3":0,"marker_4":0,"marker_5":0}}},

{"name":"Hand start: 1 removed, 6 dealt each, 8 left in deck (7 after the first draw); random deal, counts only","rule":"R2","players":2,"rounds":1,
 "rules":[{"seat":1,"options_include":"Secret"}],
 "expect":{"lens":{"game":{"removed_card":1,"deck":7},"players":{"1":{"hand":6,"secret":1},"2":{"hand":6}}}}},

{"name":"Hand start empties secrets and discard and resets unused_actions","rule":"R3","players":2,"rounds":1,
 "given":{"players":{"1":{"secret":[3],"unused_actions":["Gift"]},"2":{"secret":[4],"unused_actions":["Gift"]}},"game":{"discard":[1,2]}},
 "rules":[{"seat":1,"options_include":"Secret"}],
 "expect":{"offered":[{"seat":1,"option":"Secret"},{"seat":1,"option":"Trade-off"},{"seat":1,"option":"Gift"},{"seat":1,"option":"Competition"}],
           "lens":{"game":{"discard":0},"players":{"1":{"secret":1,"unused_actions":3},"2":{"secret":0,"unused_actions":4}}}}},

{"name":"Hand 1 start empties both kept lists","rule":"R4","players":2,"rounds":1,
 "given":{"players":{"1":{"kept":[1,2]},"2":{"kept":[5]}},"game":{"hand_number":1,"round_in_hand":1,"starting_seat":1}},
 "rules":[{"seat":1,"options_include":"Secret"}],
 "expect":{"players":{"1":{"kept":[]},"2":{"kept":[]}}}},

{"name":"Hand 2 start keeps kept lists and markers","rule":"R4","players":2,"rounds":1,
 "given":{"players":{"1":{"kept":[1,2]},"2":{"kept":[5]}},"game":{"hand_number":2,"round_in_hand":1,"starting_seat":2,"marker_3":1}},
 "rules":[{"seat":2,"options_include":"Secret"}],
 "expect":{"players":{"1":{"kept":[1,2]},"2":{"kept":[5]}},"game":{"marker_3":1},
           "not_offered":[{"seat":1,"option":"Secret"},{"seat":1,"option":"Gift"}]}},

{"name":"After hand 1 ends, Player 2 starts hand 2","rule":"R5","players":2,"rounds":2,
 "given":{"players":{"1":{"unused_actions":[],"secret":[2]},"2":{"unused_actions":["Trade-off"],"hand":[1],"secret":[4]}},
          "game":{"hand_number":1,"round_in_hand":8,"starting_seat":1,"deck":[1]}},
 "rules":[{"seat":2,"options_include":"Secret"}],
 "expect":{"players":{"1":{"kept":[2]},"2":{"kept":[4]}},
           "offered":[{"seat":2,"option":"Gift"}],
           "not_offered":[{"seat":1,"option":"Secret"},{"seat":1,"option":"Trade-off"},{"seat":1,"option":"Gift"},{"seat":1,"option":"Competition"}]}},

{"name":"Round 1 starting seat acts, round 2 the other seat acts","rule":"R6","players":2,"rounds":2,
 "rules":[{"seat":1,"options_include":"Secret"},{"seat":2,"options_include":"Secret"}],
 "expect":{"lens":{"players":{"1":{"secret":1,"unused_actions":3},"2":{"secret":1,"unused_actions":3}}}}},

{"name":"Active player draws 1 card from deck at turn start","rule":"R7","players":2,"rounds":1,
 "given":{"players":{"2":{"hand":[1,1,1]}},"game":{"hand_number":1,"round_in_hand":2,"starting_seat":1,"deck":[5,5,5]}},
 "rules":[{"seat":2,"options_include":"Secret"},{"seat":2,"options_include":5}],
 "expect":{"offered":[{"seat":2,"option":5}],"lens":{"game":{"deck":2},"players":{"2":{"hand":3,"secret":1}}}}},

{"name":"Only unused actions are offered and the chosen one is removed","rule":"R8","players":2,"rounds":1,
 "given":{"players":{"1":{"hand":[3,4],"unused_actions":["Trade-off","Competition"]}},"game":{"hand_number":1,"round_in_hand":3,"starting_seat":1,"deck":[5]}},
 "rules":[{"seat":1,"options_include":"Trade-off"}],
 "expect":{"offered":[{"seat":1,"option":"Trade-off"},{"seat":1,"option":"Competition"}],
           "not_offered":[{"seat":1,"option":"Secret"},{"seat":1,"option":"Gift"}],
           "lens":{"game":{"discard":2},"players":{"1":{"unused_actions":1,"hand":1}}}}},

{"name":"Fourth turn has exactly one action which is taken","rule":"R9","players":2,"rounds":1,
 "given":{"players":{"1":{"unused_actions":[]},"2":{"unused_actions":["Secret"],"hand":[2]}},"game":{"hand_number":1,"round_in_hand":8,"starting_seat":1,"deck":[2]}},
 "expect":{"offered":[{"seat":2,"option":"Secret"}],
           "not_offered":[{"seat":2,"option":"Gift"},{"seat":2,"option":"Trade-off"},{"seat":2,"option":"Competition"}],
           "players":{"1":{"kept":[]},"2":{"kept":[2]}}}},

{"name":"Secret moves 1 hand card face-down to secret","rule":"R10","players":2,"rounds":1,
 "given":{"players":{"2":{"hand":[1,4]}},"game":{"hand_number":1,"round_in_hand":2,"starting_seat":1,"deck":[4]}},
 "rules":[{"seat":2,"options_include":"Secret"},{"seat":2,"options_include":4}],
 "expect":{"players":{"2":{"kept":[]}},"lens":{"players":{"2":{"hand":2,"secret":1}}}}},

{"name":"Trade-off discards 2 cards that do not score at the pair end","rule":"R11","players":2,"rounds":1,
 "given":{"players":{"1":{"hand":[5],"unused_actions":["Trade-off"],"kept":[]},"2":{"unused_actions":[],"kept":[5]}},
          "game":{"hand_number":2,"round_in_hand":8,"starting_seat":2,"deck":[5]}},
 "expect":{"players":{"1":{"kept":[],"charm":0,"geisha_count":0},"2":{"charm":6,"geisha_count":1,"standing":6}},
           "game":{"marker_5":2,"marker_1":0},"lens":{"game":{"discard":2}}}},

{"name":"Gift: opponent takes 1 of 3 revealed cards, active keeps the other 2","rule":"R12","players":2,"rounds":1,
 "given":{"players":{"1":{"hand":[3,4,5]}},"game":{"hand_number":1,"round_in_hand":3,"starting_seat":1,"deck":[1]}},
 "rules":[{"seat":1,"options_include":"Gift"},{"seat":1,"options_include":3},{"seat":1,"options_include":4},{"seat":1,"options_include":5},
          {"seat":2,"options_include":5}],
 "expect":{"players":{"1":{"kept":[3,4]},"2":{"kept":[5]}},"lens":{"players":{"1":{"hand":1}}}}},

{"name":"Competition: opponent takes one pair, active keeps the other","rule":"R13","players":2,"rounds":1,
 "given":{"players":{"1":{"hand":[1,2,3,4]}},"game":{"hand_number":1,"round_in_hand":3,"starting_seat":1,"deck":[5]}},
 "rules":[{"seat":1,"options_include":"Competition"},{"seat":1,"options_include":1},{"seat":1,"options_include":2},{"seat":1,"options_include":3},{"seat":1,"options_include":4},
          {"seat":2,"options_include":"Pair B"}],
 "expect":{"players":{"1":{"kept":[1,2]},"2":{"kept":[3,4]}},"offered":[{"seat":2,"option":"Pair A"}]}},

{"name":"Only held Geisha numbers are offered as card picks","rule":"R14","players":2,"rounds":1,
 "given":{"players":{"2":{"hand":[1,4]}},"game":{"hand_number":1,"round_in_hand":2,"starting_seat":1,"deck":[4]}},
 "rules":[{"seat":2,"options_include":"Secret"},{"seat":2,"options_include":4}],
 "expect":{"offered":[{"seat":2,"option":1},{"seat":2,"option":4}],
           "not_offered":[{"seat":2,"option":2},{"seat":2,"option":3},{"seat":2,"option":5}]}},

{"name":"After round 8 secrets are appended to kept","rule":"R15","players":2,"rounds":1,
 "given":{"players":{"1":{"unused_actions":[],"secret":[3],"kept":[4]},"2":{"unused_actions":["Trade-off"],"hand":[1],"secret":[5],"kept":[]}},
          "game":{"hand_number":1,"round_in_hand":8,"starting_seat":1,"deck":[1]}},
 "expect":{"players":{"1":{"kept":[4,3]},"2":{"kept":[5]}}}},

{"name":"Markers move to strictly more cards, stay on ties","rule":"R16","players":2,"rounds":1,
 "given":{"players":{"1":{"hand":[1],"unused_actions":["Trade-off"],"kept":[1,1,2,3,3,4]},"2":{"unused_actions":[],"kept":[1,2,2,3,3]}},
          "game":{"hand_number":2,"round_in_hand":8,"starting_seat":2,"deck":[1],"marker_3":2,"marker_4":2}},
 "expect":{"game":{"marker_1":1,"marker_2":2,"marker_3":2,"marker_4":1,"marker_5":0}}},

{"name":"Charm, geisha_count and standing computed from markers","rule":"R17","players":2,"rounds":1,
 "given":{"players":{"1":{"hand":[1],"unused_actions":["Trade-off"],"kept":[1,1,2,3,3,4]},"2":{"unused_actions":[],"kept":[1,2,2,3,3]}},
          "game":{"hand_number":2,"round_in_hand":8,"starting_seat":2,"deck":[1],"marker_3":2,"marker_4":2}},
 "expect":{"players":{"1":{"charm":8,"geisha_count":2,"standing":8},"2":{"charm":7,"geisha_count":2,"standing":7}}}},

{"name":"11 charm at pair end wins","rule":"R18","players":2,
 "given":{"players":{"1":{"hand":[1],"unused_actions":["Trade-off"],"kept":[4,5]},"2":{"unused_actions":[],"kept":[1]}},
          "game":{"hand_number":2,"round_in_hand":8,"starting_seat":2,"deck":[1]}},
 "expect":{"winner":1,"standings":{"1":10112,"2":31},
           "players":{"1":{"charm":11,"geisha_count":2},"2":{"charm":3,"geisha_count":1}}}},

{"name":"3 Geisha without 11 charm wins at pair end","rule":"R19","players":2,
 "given":{"players":{"1":{"hand":[1],"unused_actions":["Trade-off"],"kept":[4]},"2":{"unused_actions":[],"kept":[1,2,3]}},
          "game":{"hand_number":2,"round_in_hand":8,"starting_seat":2,"deck":[2]}},
 "expect":{"winner":2,"standings":{"1":51,"2":1103},
           "players":{"1":{"charm":5,"geisha_count":1},"2":{"charm":10,"geisha_count":3}}}},

{"name":"11 charm beats 3 Geisha","rule":"R20","players":2,
 "given":{"players":{"1":{"hand":[1],"unused_actions":["Trade-off"],"kept":[4,5]},"2":{"unused_actions":[],"kept":[1,2,3]}},
          "game":{"hand_number":2,"round_in_hand":8,"starting_seat":2,"deck":[1]}},
 "expect":{"winner":1,"standings":{"1":10112,"2":1103},
           "players":{"1":{"charm":11,"geisha_count":2},"2":{"charm":10,"geisha_count":3}}}},

{"name":"After hand 4 higher charm wins","rule":"R21","players":2,
 "given":{"players":{"1":{"hand":[1],"unused_actions":["Trade-off"],"kept":[5]},"2":{"unused_actions":[],"kept":[4]}},
          "game":{"hand_number":4,"round_in_hand":8,"starting_seat":2,"deck":[1],"marker_1":0,"marker_2":0,"marker_3":0,"marker_4":0,"marker_5":0}},
 "expect":{"winner":1,"standings":{"1":61,"2":51},"players":{"1":{"charm":6},"2":{"charm":5}}}},

{"name":"After hand 4 tied charm, higher geisha_count wins","rule":"R21","players":2,
 "given":{"players":{"1":{"hand":[3],"unused_actions":["Trade-off"],"kept":[5]},"2":{"unused_actions":[],"kept":[1,2]}},
          "game":{"hand_number":4,"round_in_hand":8,"starting_seat":2,"deck":[3],"marker_1":0,"marker_2":0,"marker_3":0,"marker_4":0,"marker_5":0}},
 "expect":{"winner":2,"standings":{"1":61,"2":62},
           "players":{"1":{"charm":6,"geisha_count":1},"2":{"charm":6,"geisha_count":2}}}},

{"name":"After hand 4 fully level is a draw","rule":"R21","players":2,
 "given":{"players":{"1":{"hand":[1],"unused_actions":["Trade-off"],"kept":[4]},"2":{"unused_actions":[],"kept":[4]}},
          "game":{"hand_number":4,"round_in_hand":8,"starting_seat":2,"deck":[1],"marker_1":0,"marker_2":0,"marker_3":0,"marker_4":0,"marker_5":0}},
 "expect":{"winner":[1,2],"standings":{"1":0,"2":0},"game":{"marker_4":0}}},

{"name":"No winner after hand 2: hand 3 starts with Player 1, kept emptied, markers kept","rule":"R22","players":2,"rounds":2,
 "given":{"players":{"1":{"hand":[1],"unused_actions":["Trade-off"],"kept":[1,1,2,3,3,4]},"2":{"unused_actions":[],"kept":[1,2,2,3,3]}},
          "game":{"hand_number":2,"round_in_hand":8,"starting_seat":2,"deck":[1],"marker_3":2,"marker_4":2}},
 "rules":[{"seat":1,"options_include":"Secret"}],
 "expect":{"players":{"1":{"kept":[],"charm":8},"2":{"kept":[],"charm":7}},
           "game":{"marker_1":1,"marker_2":2,"marker_3":2,"marker_4":1,"marker_5":0},
           "offered":[{"seat":1,"option":"Gift"}],
           "not_offered":[{"seat":2,"option":"Secret"},{"seat":2,"option":"Gift"}]}}
]

Why it was refused: scenario 1: needs `rules` (what each seat answers, by option name); scenario 10: needs `rules` (what each seat answers, by option name); scenario 12: needs `rules` (what each seat answers, by option name); scenario 16: needs `rules` (what each seat answers, by option name); scenario 17: needs `rules` (what each seat answers, by option name); scenario 18: needs `rules` (what each seat answers, by option name); scenario 19: needs `rules` (what each seat answers, by option name); scenario 20: needs `rules` (what each seat answers, by option name); scenario 21: needs `rules` (what each seat answers, by option name); scenario 22: needs `rules` (what each seat answers, by option name); scenario 23: needs `rules` (what each seat answers, by option name); scenario 24: needs `rules` (what each seat answers, by option name)
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
[
{"name":"All markers are still in the middle after the first turn of the game","rule":"R1","players":2,"rounds":1,
 "rules":[{"seat":1,"options_include":"Secret"}],
 "expect":{"game":{"marker_1":0,"marker_2":0,"marker_3":0,"marker_4":0,"marker_5":0}}},

{"name":"Hand start: 1 removed, 6 dealt each, 8 left in deck (7 after the first draw); random deal, counts only","rule":"R2","players":2,"rounds":1,
 "rules":[{"seat":1,"options_include":"Secret"}],
 "expect":{"lens":{"game":{"removed_card":1,"deck":7},"players":{"1":{"hand":6,"secret":1},"2":{"hand":6}}}}},

{"name":"Hand start empties secrets and discard and resets unused_actions","rule":"R3","players":2,"rounds":1,
 "given":{"players":{"1":{"secret":[3],"unused_actions":["Gift"]},"2":{"secret":[4],"unused_actions":["Gift"]}},"game":{"discard":[1,2]}},
 "rules":[{"seat":1,"options_include":"Secret"}],
 "expect":{"offered":[{"seat":1,"option":"Secret"},{"seat":1,"option":"Trade-off"},{"seat":1,"option":"Gift"},{"seat":1,"option":"Competition"}],
           "lens":{"game":{"discard":0},"players":{"1":{"secret":1,"unused_actions":3},"2":{"secret":0,"unused_actions":4}}}}},

{"name":"Hand 1 start empties both kept lists","rule":"R4","players":2,"rounds":1,
 "given":{"players":{"1":{"kept":[1,2]},"2":{"kept":[5]}},"game":{"hand_number":1,"round_in_hand":1,"starting_seat":1}},
 "rules":[{"seat":1,"options_include":"Secret"}],
 "expect":{"players":{"1":{"kept":[]},"2":{"kept":[]}}}},

{"name":"Hand 2 start keeps kept lists and markers","rule":"R4","players":2,"rounds":1,
 "given":{"players":{"1":{"kept":[1,2]},"2":{"kept":[5]}},"game":{"hand_number":2,"round_in_hand":1,"starting_seat":2,"marker_3":1}},
 "rules":[{"seat":2,"options_include":"Secret"}],
 "expect":{"players":{"1":{"kept":[1,2]},"2":{"kept":[5]}},"game":{"marker_3":1},
           "not_offered":[{"seat":1,"option":"Secret"},{"seat":1,"option":"Gift"}]}},

{"name":"After hand 1 ends, Player 2 starts hand 2","rule":"R5","players":2,"rounds":2,
 "given":{"players":{"1":{"unused_actions":[],"secret":[2]},"2":{"unused_actions":["Trade-off"],"hand":[1],"secret":[4]}},
          "game":{"hand_number":1,"round_in_hand":8,"starting_seat":1,"deck":[1]}},
 "rules":[{"seat":2,"options_include":"Secret"}],
 "expect":{"players":{"1":{"kept":[2]},"2":{"kept":[4]}},
           "offered":[{"seat":2,"option":"Gift"}],
           "not_offered":[{"seat":1,"option":"Secret"},{"seat":1,"option":"Trade-off"},{"seat":1,"option":"Gift"},{"seat":1,"option":"Competition"}]}},

{"name":"Round 1 starting seat acts, round 2 the other seat acts","rule":"R6","players":2,"rounds":2,
 "rules":[{"seat":1,"options_include":"Secret"},{"seat":2,"options_include":"Secret"}],
 "expect":{"lens":{"players":{"1":{"secret":1,"unused_actions":3},"2":{"secret":1,"unused_actions":3}}}}},

{"name":"Active player draws 1 card from deck at turn start","rule":"R7","players":2,"rounds":1,
 "given":{"players":{"2":{"hand":[1,1,1]}},"game":{"hand_number":1,"round_in_hand":2,"starting_seat":1,"deck":[5,5,5]}},
 "rules":[{"seat":2,"options_include":"Secret"},{"seat":2,"options_include":5}],
 "expect":{"offered":[{"seat":2,"option":5}],"lens":{"game":{"deck":2},"players":{"2":{"hand":3,"secret":1}}}}},

{"name":"Only unused actions are offered and the chosen one is removed","rule":"R8","players":2,"rounds":1,
 "given":{"players":{"1":{"hand":[3,4],"unused_actions":["Trade-off","Competition"]}},"game":{"hand_number":1,"round_in_hand":3,"starting_seat":1,"deck":[5]}},
 "rules":[{"seat":1,"options_include":"Trade-off"}],
 "expect":{"offered":[{"seat":1,"option":"Trade-off"},{"seat":1,"option":"Competition"}],
           "not_offered":[{"seat":1,"option":"Secret"},{"seat":1,"option":"Gift"}],
           "lens":{"game":{"discard":2},"players":{"1":{"unused_actions":1,"hand":1}}}}},

{"name":"Fourth turn has exactly one action which is taken","rule":"R9","players":2,"rounds":1,
 "given":{"players":{"1":{"unused_actions":[]},"2":{"unused_actions":["Secret"],"hand":[2]}},"game":{"hand_number":1,"round_in_hand":8,"starting_seat":1,"deck":[2]}},
 "rules":[{"seat":2,"options_include":"Secret"}],
 "expect":{"offered":[{"seat":2,"option":"Secret"}],
           "not_offered":[{"seat":2,"option":"Gift"},{"seat":2,"option":"Trade-off"},{"seat":2,"option":"Competition"}],
           "players":{"1":{"kept":[]},"2":{"kept":[2]}}}},

{"name":"Secret moves 1 hand card face-down to secret","rule":"R10","players":2,"rounds":1,
 "given":{"players":{"2":{"hand":[1,4]}},"game":{"hand_number":1,"round_in_hand":2,"starting_seat":1,"deck":[4]}},
 "rules":[{"seat":2,"options_include":"Secret"},{"seat":2,"options_include":4}],
 "expect":{"players":{"2":{"kept":[]}},"lens":{"players":{"2":{"hand":2,"secret":1}}}}},

{"name":"Trade-off discards 2 cards that do not score at the pair end","rule":"R11","players":2,"rounds":1,
 "given":{"players":{"1":{"hand":[5],"unused_actions":["Trade-off"],"kept":[]},"2":{"unused_actions":[],"kept":[5]}},
          "game":{"hand_number":2,"round_in_hand":8,"starting_seat":2,"deck":[5]}},
 "rules":[{"seat":1,"options_include":"Trade-off"}],
 "expect":{"players":{"1":{"kept":[],"charm":0,"geisha_count":0},"2":{"charm":6,"geisha_count":1,"standing":6}},
           "game":{"marker_5":2,"marker_1":0},"lens":{"game":{"discard":2}}}},

{"name":"Gift: opponent takes 1 of 3 revealed cards, active keeps the other 2","rule":"R12","players":2,"rounds":1,
 "given":{"players":{"1":{"hand":[3,4,5]}},"game":{"hand_number":1,"round_in_hand":3,"starting_seat":1,"deck":[1]}},
 "rules":[{"seat":1,"options_include":"Gift"},{"seat":1,"options_include":3},{"seat":1,"options_include":4},{"seat":1,"options_include":5},
          {"seat":2,"options_include":5}],
 "expect":{"players":{"1":{"kept":[3,4]},"2":{"kept":[5]}},"lens":{"players":{"1":{"hand":1}}}}},

{"name":"Competition: opponent takes one pair, active keeps the other","rule":"R13","players":2,"rounds":1,
 "given":{"players":{"1":{"hand":[1,2,3,4]}},"game":{"hand_number":1,"round_in_hand":3,"starting_seat":1,"deck":[5]}},
 "rules":[{"seat":1,"options_include":"Competition"},{"seat":1,"options_include":1},{"seat":1,"options_include":2},{"seat":1,"options_include":3},{"seat":1,"options_include":4},
          {"seat":2,"options_include":"Pair B"}],
 "expect":{"players":{"1":{"kept":[1,2]},"2":{"kept":[3,4]}},"offered":[{"seat":2,"option":"Pair A"}]}},

{"name":"Only held Geisha numbers are offered as card picks","rule":"R14","players":2,"rounds":1,
 "given":{"players":{"2":{"hand":[1,4]}},"game":{"hand_number":1,"round_in_hand":2,"starting_seat":1,"deck":[4]}},
 "rules":[{"seat":2,"options_include":"Secret"},{"seat":2,"options_include":4}],
 "expect":{"offered":[{"seat":2,"option":1},{"seat":2,"option":4}],
           "not_offered":[{"seat":2,"option":2},{"seat":2,"option":3},{"seat":2,"option":5}]}},

{"name":"After round 8 secrets are appended to kept","rule":"R15","players":2,"rounds":1,
 "given":{"players":{"1":{"unused_actions":[],"secret":[3],"kept":[4]},"2":{"unused_actions":["Trade-off"],"hand":[1],"secret":[5],"kept":[]}},
          "game":{"hand_number":1,"round_in_hand":8,"starting_seat":1,"deck":[1]}},
 "rules":[{"seat":2,"options_include":"Trade-off"}],
 "expect":{"players":{"1":{"kept":[4,3]},"2":{"kept":[5]}}}},

{"name":"Markers move to strictly more cards, stay on ties","rule":"R16","players":2,"rounds":1,
 "given":{"players":{"1":{"hand":[1],"unused_actions":["Trade-off"],"kept":[1,1,2,3,3,4]},"2":{"unused_actions":[],"kept":[1,2,2,3,3]}},
          "game":{"hand_number":2,"round_in_hand":8,"starting_seat":2,"deck":[1],"marker_3":2,"marker_4":2}},
 "rules":[{"seat":1,"options_include":"Trade-off"}],
 "expect":{"game":{"marker_1":1,"marker_2":2,"marker_3":2,"marker_4":1,"marker_5":0}}},

{"name":"Charm, geisha_count and standing computed from markers","rule":"R17","players":2,"rounds":1,
 "given":{"players":{"1":{"hand":[1],"unused_actions":["Trade-off"],"kept":[1,1,2,3,3,4]},"2":{"unused_actions":[],"kept":[1,2,2,3,3]}},
          "game":{"hand_number":2,"round_in_hand":8,"starting_seat":2,"deck":[1],"marker_3":2,"marker_4":2}},
 "rules":[{"seat":1,"options_include":"Trade-off"}],
 "expect":{"players":{"1":{"charm":8,"geisha_count":2,"standing":8},"2":{"charm":7,"geisha_count":2,"standing":7}}}},

{"name":"11 charm at pair end wins","rule":"R18","players":2,
 "given":{"players":{"1":{"hand":[1],"unused_actions":["Trade-off"],"kept":[4,5]},"2":{"unused_actions":[],"kept":[1]}},
          "game":{"hand_number":2,"round_in_hand":8,"starting_seat":2,"deck":[1]}},
 "rules":[{"seat":1,"options_include":"Trade-off"}],
 "expect":{"winner":1,"standings":{"1":10112,"2":31},
           "players":{"1":{"charm":11,"geisha_count":2},"2":{"charm":3,"geisha_count":1}}}},

{"name":"3 Geisha without 11 charm wins at pair end","rule":"R19","players":2,
 "given":{"players":{"1":{"hand":[1],"unused_actions":["Trade-off"],"kept":[4]},"2":{"unused_actions":[],"kept":[1,2,3]}},
          "game":{"hand_number":2,"round_in_hand":8,"starting_seat":2,"deck":[2]}},
 "rules":[{"seat":1,"options_include":"Trade-off"}],
 "expect":{"winner":2,"standings":{"1":51,"2":1103},
           "players":{"1":{"charm":5,"geisha_count":1},"2":{"charm":10,"geisha_count":3}}}},

{"name":"11 charm beats 3 Geisha","rule":"R20","players":2,
 "given":{"players":{"1":{"hand":[1],"unused_actions":["Trade-off"],"kept":[4,5]},"2":{"unused_actions":[],"kept":[1,2,3]}},
          "game":{"hand_number":2,"round_in_hand":8,"starting_seat":2,"deck":[1]}},
 "rules":[{"seat":1,"options_include":"Trade-off"}],
 "expect":{"winner":1,"standings":{"1":10112,"2":1103},
           "players":{"1":{"charm":11,"geisha_count":2},"2":{"charm":10,"geisha_count":3}}}},

{"name":"After hand 4 higher charm wins","rule":"R21","players":2,
 "given":{"players":{"1":{"hand":[1],"unused_actions":["Trade-off"],"kept":[5]},"2":{"unused_actions":[],"kept":[4]}},
          "game":{"hand_number":4,"round_in_hand":8,"starting_seat":2,"deck":[1],"marker_1":0,"marker_2":0,"marker_3":0,"marker_4":0,"marker_5":0}},
 "rules":[{"seat":1,"options_include":"Trade-off"}],
 "expect":{"winner":1,"standings":{"1":61,"2":51},"players":{"1":{"charm":6},"2":{"charm":5}}}},

{"name":"After hand 4 tied charm, higher geisha_count wins","rule":"R21","players":2,
 "given":{"players":{"1":{"hand":[3],"unused_actions":["Trade-off"],"kept":[5]},"2":{"unused_actions":[],"kept":[1,2]}},
          "game":{"hand_number":4,"round_in_hand":8,"starting_seat":2,"deck":[3],"marker_1":0,"marker_2":0,"marker_3":0,"marker_4":0,"marker_5":0}},
 "rules":[{"seat":1,"options_include":"Trade-off"}],
 "expect":{"winner":2,"standings":{"1":61,"2":62},
           "players":{"1":{"charm":6,"geisha_count":1},"2":{"charm":6,"geisha_count":2}}}},

{"name":"After hand 4 fully level is a draw","rule":"R21","players":2,
 "given":{"players":{"1":{"hand":[1],"unused_actions":["Trade-off"],"kept":[4]},"2":{"unused_actions":[],"kept":[4]}},
          "game":{"hand_number":4,"round_in_hand":8,"starting_seat":2,"deck":[1],"marker_1":0,"marker_2":0,"marker_3":0,"marker_4":0,"marker_5":0}},
 "rules":[{"seat":1,"options_include":"Trade-off"}],
 "expect":{"winner":[1,2],"standings":{"1":0,"2":0},"game":{"marker_4":0}}},

{"name":"No winner after hand 2: hand 3 starts with Player 1, kept emptied, markers kept","rule":"R22","players":2,"rounds":2,
 "given":{"players":{"1":{"hand":[1],"unused_actions":["Trade-off"],"kept":[1,1,2,3,3,4]},"2":{"unused_actions":[],"kept":[1,2,2,3,3]}},
          "game":{"hand_number":2,"round_in_hand":8,"starting_seat":2,"deck":[1],"marker_3":2,"marker_4":2}},
 "rules":[{"seat":1,"options_include":"Trade-off"},{"seat":1,"options_include":"Secret"}],
 "expect":{"players":{"1":{"kept":[],"charm":8},"2":{"kept":[],"charm":7}},
           "game":{"marker_1":1,"marker_2":2,"marker_3":2,"marker_4":1,"marker_5":0},
           "offered":[{"seat":1,"option":"Gift"}],
           "not_offered":[{"seat":2,"option":"Secret"},{"seat":2,"option":"Gift"}]}}
]
````
