# 30 scenarios

- time: 2026-10-27T10:35:21+00:00 (124.6s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 5ff663a6940b9e5f, reply sha256 2c7334775310b358

## Sent

````
SPEC:
{
  "name": "Hanamikoji: Paired Hands",
  "summary": "Two players win the favour of five Geisha over up to four hands, played as two pairs, by keeping, discarding, gifting and splitting Item cards with four one-use actions; Victory Markers move after each pair.",
  "players": {
    "min": 2,
    "max": 2,
    "suggested": 2
  },
  "parameters": {
    "geisha_count_total": 5,
    "charm_g1": 3,
    "charm_g2": 3,
    "charm_g3": 4,
    "charm_g4": 5,
    "charm_g5": 6,
    "charm_total": 21,
    "cards_g1": 3,
    "cards_g2": 3,
    "cards_g3": 4,
    "cards_g4": 5,
    "cards_g5": 6,
    "cards_total": 21,
    "cards_removed_per_hand": 1,
    "hand_size_dealt": 6,
    "deck_size_after_deal": 8,
    "max_hands": 4,
    "rounds_per_hand": 8,
    "max_rounds": 32,
    "hands_per_pair": 2,
    "secret_cards": 1,
    "tradeoff_cards": 2,
    "gift_cards": 3,
    "competition_cards": 4,
    "charm_to_win": 11,
    "geisha_to_win": 3,
    "default_pick": 1
  },
  "attributes": {
    "player": [
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "Item cards (numbers 1-5) the player privately holds, shown sorted",
        "observable": false
      },
      {
        "key": "secret",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "The 0 or 1 card set face down by the Secret action this hand",
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
        "meaning": "Action markers not yet spent this hand",
        "observable": false
      },
      {
        "key": "kept",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Cards kept during the current pair of hands; the pair total for Geisha g is the count of g in this list (Secrets join it only at the end of a hand)",
        "observable": true
      },
      {
        "key": "charm",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Sum of Charm of the Geisha whose marker is on this player's side",
        "observable": true
      },
      {
        "key": "geisha_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of Victory Markers on this player's side",
        "observable": true
      },
      {
        "key": "standing",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Ranking value: (charm>=11)*1000 + (geisha_count>=3)*100 + charm*10 + geisha_count",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "Face-down draw deck for the current hand",
        "observable": false
      },
      {
        "key": "removed_card",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "The one card set aside unseen at the start of each hand",
        "observable": false
      },
      {
        "key": "discard",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "Face-down cards discarded by Trade-off this hand",
        "observable": false
      },
      {
        "key": "hand_number",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Current hand, 1 to 4",
        "observable": false
      },
      {
        "key": "round_in_hand",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Current round within the hand, 1 to 8",
        "observable": false
      },
      {
        "key": "starting_seat",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Seat that starts the current hand: 1 in hands 1 and 3, 2 in hands 2 and 4",
        "observable": false
      },
      {
        "key": "active_seat",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Seat acting this round; the other seat is the opponent",
        "observable": false
      },
      {
        "key": "chosen_action",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Action named this round after defaults",
        "observable": false
      },
      {
        "key": "chosen_cards",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "Cards used this round after defaults; revealed publicly only for Gift and Competition",
        "observable": false
      },
      {
        "key": "pick",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Opponent's pick: 1-3 for Gift offers, 1 or 2 for Competition pairs A/B",
        "observable": false
      },
      {
        "key": "marker_1",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Victory Marker of Geisha 1: 0 neutral, 1 Player 1's side, 2 Player 2's side",
        "observable": true
      },
      {
        "key": "marker_2",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Victory Marker of Geisha 2",
        "observable": true
      },
      {
        "key": "marker_3",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Victory Marker of Geisha 3",
        "observable": true
      },
      {
        "key": "marker_4",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Victory Marker of Geisha 4",
        "observable": true
      },
      {
        "key": "marker_5",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Victory Marker of Geisha 5",
        "observable": true
      },
      {
        "key": "game_over",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "Set when a win check ends the game",
        "observable": false
      }
    ]
  },
  "setup": [
    "Seat 1 is Player 1 and seat 2 is Player 2.",
    "All five Victory Markers start neutral (marker_1..marker_5 = 0).",
    "Charm, geisha_count and standing start at 0 for both players.",
    "hand_number = 1, round_in_hand = 1, starting_seat = 1."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When round_in_hand == 1 (start of a hand): build deck as the 21 Items [1,1,1,2,2,2,3,3,3,3,4,4,4,4,4,5,5,5,5,5,5]; move one random card from deck to removed_card (replacing its previous content); move 6 random deck cards into each player's hand (hand emptied first); deck now holds 8; discard emptied; each player's unused_actions = [Secret, Trade-off, Gift, Competition]; each secret emptied; if hand_number is 1 or 3, each kept = []; starting_seat = 1 if hand_number is 1 or 3, else 2."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "active_seat = starting_seat if round_in_hand is odd, else the other seat."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce hand_number, round_in_hand, active_seat, each player's unused_actions, each player's pair totals (count of 1..5 in kept), and marker_1..marker_5."
    },
    {
      "action": "update",
      "who": "the active seat",
      "answer": null,
      "effect": "Move one random card from deck to the active player's hand (the draw)."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player privately sees their own sorted hand and secret."
    },
    {
      "action": "ask",
      "who": "the active seat",
      "answer": "one of the active player's unused_actions: Secret, Trade-off, Gift, Competition",
      "effect": "chosen_action = the answer; if illegal or missing, chosen_action = the first of Secret, Trade-off, Gift, Competition still in unused_actions."
    },
    {
      "action": "ask",
      "who": "the active seat",
      "answer": "short text: space-separated card numbers, 1 for Secret, 2 for Trade-off, 3 for Gift, 4 for Competition, repeats written out",
      "effect": "If legal, chosen_cards = the written numbers in order; otherwise chosen_cards = the required number of lowest cards in hand in ascending order. Remove chosen_cards from the active player's hand.",
      "judged": "The answer is exactly the required number of card numbers for chosen_action (Secret 1, Trade-off 2, Gift 3, Competition 4), and no number appears more often than that card appears in the active player's hand."
    },
    {
      "action": "update",
      "who": "the active seat",
      "answer": null,
      "effect": "If chosen_action is Secret, append chosen_cards to the active player's secret; if Trade-off, append chosen_cards to discard. Remove chosen_action from the active player's unused_actions."
    },
    {
      "action": "ask",
      "who": "the opponent (the seat that is not active_seat)",
      "answer": "Gift: a choice of 1, 2 or 3; Competition: 1 (pair A = first two cards) or 2 (pair B = last two cards)",
      "effect": "When chosen_action is Gift or Competition: the opponent is shown the revealed chosen_cards (Gift as offers 1,2,3; Competition as pair A, pair B); pick = the answer, or 1 if illegal or missing."
    },
    {
      "action": "update",
      "who": "both players",
      "answer": null,
      "effect": "When chosen_action is Gift: append offer number pick to the opponent's kept and the other two offers to the active player's kept. When chosen_action is Competition: append the picked pair to the opponent's kept and the other pair to the active player's kept."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Publicly announce the active seat and chosen_action; for Gift or Competition also the revealed chosen_cards and who kept which; for Secret or Trade-off only that the action was used."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When round_in_hand == 8 (end of hand): reveal each player's secret, append it to that player's kept, and announce both secrets and both players' pair totals."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When round_in_hand == 8 and hand_number is 2 or 4 (end of pair): for each Geisha g, if count of g in Player 1's kept > count in Player 2's kept then marker_g = 1, if lower then marker_g = 2, if equal marker_g unchanged; for each player charm = sum of Charm (3,3,4,5,6) of Geisha with marker on their side, geisha_count = number of markers on their side, standing = (charm>=11)*1000 + (geisha_count>=3)*100 + charm*10 + geisha_count; game_over = true if any player has charm >= 11 or geisha_count >= 3, or if hand_number == 4. Announce all markers, charm and geisha counts."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if game_over is true; otherwise continue."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "If round_in_hand == 8 then hand_number += 1 and round_in_hand = 1; otherwise round_in_hand += 1."
    }
  ],
  "ending": {
    "condition": "game_over == true, set after a pair (round_in_hand == 8 and hand_number in {2,4}) when any player has charm >= 11 or geisha_count >= 3, or when hand_number == 4",
    "rank_by": "you.standing",
    "decided_by": "A player with 11 or more Charm wins. Otherwise a player with 3 or more Geisha wins. If neither holds after hand 4, the higher Charm wins, then the higher Geisha count. Equal standing is a shared result, which is the draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When a hand starts, then the 21 Items are shuffled, 1 card is set aside unseen, each player is dealt 6 cards privately, and 8 cards remain in the deck."
    },
    {
      "id": "R2",
      "text": "When a hand starts, then both players' unused_actions become Secret, Trade-off, Gift, Competition and both secrets are emptied."
    },
    {
      "id": "R3",
      "text": "When hand 1 or hand 3 starts, then both players' kept lists are emptied; when hand 2 or 4 starts, kept is unchanged."
    },
    {
      "id": "R4",
      "text": "When a new hand starts, then the Victory Markers stay where they are."
    },
    {
      "id": "R5",
      "text": "When the hand is 1 or 3, then seat 1 is active in rounds 1, 3, 5, 7 and seat 2 in rounds 2, 4, 6, 8; in hands 2 and 4 it is the reverse."
    },
    {
      "id": "R6",
      "text": "When a round starts, then the active player draws 1 card from the deck into their hand."
    },
    {
      "id": "R7",
      "text": "When the active player names an action that is spent or invalid, then the first unused action in the order Secret, Trade-off, Gift, Competition is used."
    },
    {
      "id": "R8",
      "text": "When the active player uses Secret with 1 legal card, then that card leaves their hand and becomes their secret."
    },
    {
      "id": "R9",
      "text": "When the active player uses Trade-off with 2 legal cards, then both cards leave their hand into the discard and count for nobody."
    },
    {
      "id": "R10",
      "text": "When the active player uses Gift with cards a b c, then the opponent picks 1, 2 or 3, the opponent adds that card to kept and the active player adds the other two to kept."
    },
    {
      "id": "R11",
      "text": "When the active player uses Competition with cards a b c d, then the opponent picks 1 (a b) or 2 (c d), the opponent adds that pair to kept and the active player adds the other pair."
    },
    {
      "id": "R12",
      "text": "When the card answer has the wrong count or names cards not in hand, then the required number of lowest cards in hand, in ascending order, is used, and for Competition the first two form pair A."
    },
    {
      "id": "R13",
      "text": "When the opponent's pick is illegal or missing, then it counts as 1."
    },
    {
      "id": "R14",
      "text": "When an action is used, then it is removed from the active player's unused_actions for the rest of the hand."
    },
    {
      "id": "R15",
      "text": "When Secret or Trade-off is used, then only the action's use is announced, not the cards."
    },
    {
      "id": "R16",
      "text": "When round 8 of a hand ends, then each player's secret is revealed and added to their kept."
    },
    {
      "id": "R17",
      "text": "When a pair ends (after hand 2 or 4) and a player's count of Geisha g in kept is strictly higher than the other's, then marker_g moves to that player's side; on a tie it stays."
    },
    {
      "id": "R18",
      "text": "When a pair ends, then charm is the sum of 3,3,4,5,6 over Geisha 1..5 on the player's side and geisha_count is the number of markers on their side."
    },
    {
      "id": "R19",
      "text": "When a pair ends and a player has charm >= 11, then that player wins."
    },
    {
      "id": "R20",
      "text": "When a pair ends, no player has charm >= 11 and a player has geisha_count >= 3, then that player wins."
    },
    {
      "id": "R21",
      "text": "When pair 1 ends with no winner, then the game continues with hand 3."
    },
    {
      "id": "R22",
      "text": "When pair 2 ends with no winner by threshold, then the higher charm wins, then the higher geisha_count, and if both are equal it is a draw."
    }
  ],
  "offers": [
    {
      "question": "Choice 1: which action",
      "who": "the active seat",
      "options": "exactly the actions still in that player's unused_actions (4 options in the first turn of a hand, 1 in the last)"
    },
    {
      "question": "Choice 2: which cards",
      "who": "the active seat",
      "options": "free text of space-separated numbers 1-5: 1 number for Secret, 2 for Trade-off, 3 for Gift, 4 for Competition, drawn from their hand"
    },
    {
      "question": "Choice 3: the pick",
      "who": "the opponent (the non-active seat), only after Gift or Competition",
      "options": "after Gift: 1, 2, 3; after Competition: 1 (pair A), 2 (pair B)"
    }
  ],
  "choices": [
    {
      "what": "Exactly 2 players",
      "why": "The designer fixed the game at 2, and Gift and Competition are built as a split between the active player and one opponent."
    },
    {
      "what": "No talk step",
      "why": "The rules have no talk. In a two-player zero-sum game talk adds nothing to reason about."
    },
    {
      "what": "A standing attribute used as rank_by",
      "why": "It encodes the ordered win checks (Charm >= 11, then Geisha >= 3, then Charm, then Geisha) as one number. Equal standing gives the draw."
    },
    {
      "what": "Pair totals kept as a list `kept`",
      "why": "The total for Geisha g is the count of g in the list. This keeps the five per-Geisha counts in one attribute."
    },
    {
      "what": "Ask, not poll, for each choice",
      "why": "Each choice is made by one player in sequence, and the opponent picks after seeing the revealed cards."
    }
  ],
  "simplifications": [
    {
      "what": "'Top card' draws and removals are random picks from the deck list",
      "why": "The engine draws at random from a list, which is equivalent to drawing from a shuffled deck."
    },
    {
      "what": "Hand-start, end-of-hand and end-of-pair steps run inside the round list, gated by when-conditions on round_in_hand and hand_number",
      "why": "The step list is flat, and single conditional steps express these phases without choosing between blocks."
    },
    {
      "what": "Legality of the written cards is ruled by a judged sentence",
      "why": "Parsing free text and checking it as a sub-multiset of the hand is beyond plain arithmetic. The default and all scoring stay arithmetic."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: kept, charm, geisha_count, standing; table: marker_1, marker_2, marker_3, marker_4, marker_5.
````

## Reply

````
```json
[
  {
    "name": "R1: hand 1 deal gives 6 cards each, sets 1 aside and leaves 8 in the deck; seat 1 then draws and plays Secret",
    "rule": "R1",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "rules": [{"seat": 1, "options_include": "Secret"}],
    "expect": {
      "lens": {
        "game": {"deck": 7, "removed_card": 1, "discard": 0},
        "players": {"1": {"hand": 6, "secret": 1}, "2": {"hand": 6, "secret": 0}}
      },
      "players": {"1": {"kept": []}, "2": {"kept": []}}
    }
  },
  {
    "name": "R2: start of hand 2 resets both players' actions and empties both secrets",
    "rule": "R2",
    "players": 2,
    "seed": 2,
    "rounds": 1,
    "default": "decline",
    "given": {
      "game": {"hand_number": 2, "round_in_hand": 1, "starting_seat": 2},
      "players": {
        "1": {"secret": [3], "unused_actions": ["Competition"], "kept": [1, 2]},
        "2": {"secret": [4], "unused_actions": ["Gift"], "kept": [3]}
      }
    },
    "rules": [{"seat": 2, "options_include": "Secret"}],
    "expect": {
      "lens": {"players": {"1": {"unused_actions": 4, "secret": 0}, "2": {"unused_actions": 3, "secret": 1}}},
      "offered": [{"seat": 2, "option": "Secret"}, {"seat": 2, "option": "Competition"}]
    }
  },
  {
    "name": "R3: kept lists are unchanged when hand 2 starts",
    "rule": "R3",
    "players": 2,
    "seed": 3,
    "rounds": 1,
    "default": "decline",
    "given": {
      "game": {"hand_number": 2, "round_in_hand": 1, "starting_seat": 2},
      "players": {"1": {"kept": [1, 2]}, "2": {"kept": [3]}}
    },
    "rules": [{"seat": 2, "options_include": "Secret"}],
    "expect": {"players": {"1": {"kept": [1, 2]}, "2": {"kept": [3]}}}
  },
  {
    "name": "R3: kept lists are emptied when hand 3 starts",
    "rule": "R3",
    "players": 2,
    "seed": 4,
    "rounds": 1,
    "default": "decline",
    "given": {
      "game": {"hand_number": 3, "round_in_hand": 1, "starting_seat": 2},
      "players": {"1": {"kept": [1, 2]}, "2": {"kept": [5]}}
    },
    "rules": [{"seat": 1, "options_include": "Secret"}],
    "expect": {"players": {"1": {"kept": []}, "2": {"kept": []}}}
  },
  {
    "name": "R4: Victory Markers stay where they are when hand 3 starts",
    "rule": "R4",
    "players": 2,
    "seed": 5,
    "rounds": 1,
    "default": "decline",
    "given": {
      "game": {"hand_number": 3, "round_in_hand": 1, "starting_seat": 2, "marker_1": 1, "marker_2": 2, "marker_3": 0, "marker_4": 1, "marker_5": 2}
    },
    "rules": [{"seat": 1, "options_include": "Secret"}],
    "expect": {"game": {"marker_1": 1, "marker_2": 2, "marker_3": 0, "marker_4": 1, "marker_5": 2}}
  },
  {
    "name": "R5: in hand 2, seat 2 acts in round 1 and seat 1 is not offered an action",
    "rule": "R5",
    "players": 2,
    "seed": 6,
    "rounds": 1,
    "default": "decline",
    "given": {"game": {"hand_number": 2, "round_in_hand": 1, "starting_seat": 2}},
    "rules": [{"seat": 2, "options_include": "Secret"}],
    "expect": {
      "lens": {"players": {"1": {"hand": 6, "secret": 0}, "2": {"hand": 6, "secret": 1}}},
      "offered": [{"seat": 2, "option": "Secret"}],
      "not_offered": [
        {"seat": 1, "option": "Secret"}, {"seat": 1, "option": "Trade-off"},
        {"seat": 1, "option": "Gift"}, {"seat": 1, "option": "Competition"}
      ]
    }
  },
  {
    "name": "R5: in hand 1, seat 2 acts in round 2",
    "rule": "R5",
    "players": 2,
    "seed": 7,
    "rounds": 1,
    "default": "decline",
    "given": {
      "game": {"hand_number": 1, "round_in_hand": 2, "starting_seat": 1, "deck": [1, 2, 3]},
      "players": {
        "1": {"hand": [1, 2, 3, 4, 5]},
        "2": {"hand": [1, 2, 3, 4, 5], "unused_actions": ["Secret", "Trade-off", "Gift", "Competition"], "secret": []}
      }
    },
    "rules": [{"seat": 2, "options_include": "Secret"}],
    "expect": {
      "lens": {"game": {"deck": 2}, "players": {"1": {"hand": 5}, "2": {"hand": 5, "secret": 1}}},
      "not_offered": [
        {"seat": 1, "option": "Secret"}, {"seat": 1, "option": "Trade-off"},
        {"seat": 1, "option": "Gift"}, {"seat": 1, "option": "Competition"}
      ]
    }
  },
  {
    "name": "R6: the active player draws 1 card from the deck before acting",
    "rule": "R6",
    "players": 2,
    "seed": 8,
    "rounds": 1,
    "default": "decline",
    "given": {
      "game": {"hand_number": 1, "round_in_hand": 3, "starting_seat": 1, "deck": [5, 5]},
      "players": {"1": {"hand": [2, 3, 4], "unused_actions": ["Secret", "Gift"], "secret": []}}
    },
    "rules": [{"seat": 1, "options_include": "Secret"}],
    "expect": {"lens": {"game": {"deck": 1}, "players": {"1": {"hand": 3, "secret": 1}}}}
  },
  {
    "name": "R8: Secret moves 1 card from the hand to the secret and nothing to kept",
    "rule": "R8",
    "players": 2,
    "seed": 9,
    "rounds": 1,
    "default": "decline",
    "given": {
      "game": {"hand_number": 1, "round_in_hand": 3, "starting_seat": 1, "deck": [5]},
      "players": {"1": {"hand": [2, 4], "unused_actions": ["Secret", "Gift"], "secret": [], "kept": []}, "2": {"kept": []}}
    },
    "rules": [{"seat": 1, "options_include": "Secret"}],
    "expect": {
      "lens": {"players": {"1": {"hand": 2, "secret": 1}}},
      "players": {"1": {"kept": []}, "2": {"kept": []}}
    }
  },
  {
    "name": "R9: Trade-off moves 2 cards to the discard and they count for nobody",
    "rule": "R9",
    "players": 2,
    "seed": 10,
    "rounds": 1,
    "default": "decline",
    "given": {
      "game": {"hand_number": 1, "round_in_hand": 3, "starting_seat": 1, "deck": [5], "discard": []},
      "players": {"1": {"hand": [1, 2, 3], "unused_actions": ["Trade-off", "Gift"], "secret": [], "kept": []}, "2": {"kept": []}}
    },
    "rules": [{"seat": 1, "options_include": "Trade-off"}],
    "expect": {
      "lens": {"game": {"discard": 2}, "players": {"1": {"hand": 2, "secret": 0}}},
      "players": {"1": {"kept": []}, "2": {"kept": []}}
    }
  },
  {
    "name": "R10: Gift of the lowest cards 1 2 3; opponent picks offer 2 and keeps the 2, active keeps 1 and 3",
    "rule": "R10",
    "players": 2,
    "seed": 11,
    "rounds": 1,
    "default": "decline",
    "given": {
      "game": {"hand_number": 1, "round_in_hand": 3, "starting_seat": 1, "deck": [5]},
      "players": {"1": {"hand": [1, 2, 3], "unused_actions": ["Gift", "Competition"], "secret": [], "kept": []}, "2": {"kept": []}}
    },
    "rules": [{"seat": 1, "options_include": "Gift"}, {"seat": 2, "options_include": 2}],
    "expect": {
      "players": {"1": {"kept": [1, 3]}, "2": {"kept": [2]}},
      "lens": {"players": {"1": {"hand": 1}}}
    }
  },
  {
    "name": "R11: Competition of 1 2 3 4; opponent picks pair B (3 4), active keeps pair A (1 2)",
    "rule": "R11",
    "players": 2,
    "seed": 12,
    "rounds": 1,
    "default": "decline",
    "given": {
      "game": {"hand_number": 1, "round_in_hand": 3, "starting_seat": 1, "deck": [4]},
      "players": {"1": {"hand": [1, 2, 3], "unused_actions": ["Competition"], "secret": [], "kept": []}, "2": {"kept": []}}
    },
    "rules": [{"seat": 2, "options_include": 2}],
    "expect": {
      "players": {"1": {"kept": [1, 2]}, "2": {"kept": [3, 4]}},
      "lens": {"players": {"1": {"hand": 0}}},
      "not_offered": [{"seat": 2, "option": 3}]
    }
  },
  {
    "name": "R12: a card answer not judged legal uses the 4 lowest cards in ascending order; the first two form pair A",
    "rule": "R12",
    "players": 2,
    "seed": 13,
    "rounds": 1,
    "default": "decline",
    "given": {
      "game": {"hand_number": 1, "round_in_hand": 3, "starting_seat": 1, "deck": [5]},
      "players": {"1": {"hand": [5, 4, 3, 1], "unused_actions": ["Competition"], "secret": [], "kept": []}, "2": {"kept": []}}
    },
    "rules": [{"seat": 2, "options_include": 1}],
    "expect": {
      "players": {"1": {"kept": [4, 5]}, "2": {"kept": [1, 3]}},
      "lens": {"players": {"1": {"hand": 1}}}
    }
  },
  {
    "name": "R14: a used action leaves unused_actions",
    "rule": "R14",
    "players": 2,
    "seed": 14,
    "rounds": 1,
    "default": "decline",
    "given": {
      "game": {"hand_number": 1, "round_in_hand": 3, "starting_seat": 1, "deck": [5]},
      "players": {"1": {"hand": [2, 3, 4], "unused_actions": ["Secret", "Gift"], "secret": []}}
    },
    "rules": [{"seat": 1, "options_include": "Secret"}],
    "expect": {"lens": {"players": {"1": {"unused_actions": 1}}}}
  },
  {
    "name": "R15: after Secret the opponent is not asked for a pick and no cards are added to any kept list",
    "rule": "R15",
    "players": 2,
    "seed": 15,
    "rounds": 1,
    "default": "decline",
    "given": {
      "game": {"hand_number": 1, "round_in_hand": 3, "starting_seat": 1, "deck": [5]},
      "players": {"1": {"hand": [2, 3, 4], "unused_actions": ["Secret", "Gift"], "secret": [], "kept": []}, "2": {"kept": []}}
    },
    "rules": [{"seat": 1, "options_include": "Secret"}],
    "expect": {
      "players": {"1": {"kept": []}, "2": {"kept": []}},
      "not_offered": [{"seat": 2, "option": 1}, {"seat": 2, "option": 2}]
    }
  },
  {
    "name": "R16: at the end of round 8 both secrets are revealed and appended to kept",
    "rule": "R16",
    "players": 2,
    "seed": 16,
    "rounds": 1,
    "default": "decline",
    "given": {
      "game": {"hand_number": 1, "round_in_hand": 8, "starting_seat": 1, "deck": [1]},
      "players": {
        "1": {"secret": [3], "kept": [2]},
        "2": {"hand": [1], "unused_actions": ["Trade-off"], "secret": [5], "kept": []}
      }
    },
    "expect": {
      "players": {"1": {"kept": [2, 3]}, "2": {"kept": [5]}},
      "game": {"marker_1": 0, "marker_2": 0, "marker_3": 0, "marker_4": 0, "marker_5": 0}
    }
  },
  {
    "name": "R17: at the end of pair 1 markers move to the strictly higher count and stay on a tie",
    "rule": "R17",
    "players": 2,
    "seed": 17,
    "rounds": 1,
    "default": "decline",
    "given": {
      "game": {"hand_number": 2, "round_in_hand": 8, "starting_seat": 2, "deck": [1], "marker_1": 0, "marker_2": 0, "marker_3": 2, "marker_4": 0, "marker_5": 1},
      "players": {
        "1": {"hand": [1], "unused_actions": ["Trade-off"], "secret": [], "kept": [1, 1, 3, 3, 4]},
        "2": {"secret": [], "kept": [1, 2, 3, 3, 4, 4]}
      }
    },
    "expect": {"game": {"marker_1": 1, "marker_2": 2, "marker_3": 2, "marker_4": 2, "marker_5": 1}}
  },
  {
    "name": "R18: after pair 1, charm and geisha_count follow the markers (P1 has G5 = 6; P2 has G1 + G2 = 6)",
    "rule": "R18",
    "players": 2,
    "seed": 18,
    "rounds": 1,
    "default": "decline",
    "given": {
      "game": {"hand_number": 2, "round_in_hand": 8, "starting_seat": 2, "deck": [1]},
      "players": {
        "1": {"hand": [1], "unused_actions": ["Trade-off"], "secret": [], "kept": [5]},
        "2": {"secret": [], "kept": [1, 2]}
      }
    },
    "expect": {
      "game": {"marker_1": 2, "marker_2": 2, "marker_3": 0, "marker_4": 0, "marker_5": 1},
      "players": {"1": {"charm": 6, "geisha_count": 1, "standing": 61}, "2": {"charm": 6, "geisha_count": 2, "standing": 62}},
      "standings": {"1": 61, "2": 62}
    }
  },
  {
    "name": "R19: P1 reaches 11 charm (G4 + G5) at the end of pair 1 and wins over P2 with 3 Geisha",
    "rule": "R19",
    "players": 2,
    "seed": 19,
    "default": "decline",
    "given": {
      "game": {"hand_number": 2, "round_in_hand": 8, "starting_seat": 2, "deck": [1]},
      "players": {
        "1": {"hand": [1], "unused_actions": ["Trade-off"], "secret": [], "kept": [4, 5]},
        "2": {"secret": [], "kept": [1, 2, 3]}
      }
    },
    "expect": {
      "winner": 1,
      "standings": {"1": 1112, "2": 203},
      "players": {"1": {"charm": 11, "geisha_count": 2}, "2": {"charm": 10, "geisha_count": 3}}
    }
  },
  {
    "name": "R20: P1 wins 3 Geisha (charm 10) at the end of pair 1 with nobody at 11 charm and wins",
    "rule": "R20",
    "players": 2,
    "seed": 20,
    "default": "decline",
    "given": {
      "game": {"hand_number": 2, "round_in_hand": 8, "starting_seat": 2, "deck": [1]},
      "players": {
        "1": {"hand": [1], "unused_actions": ["Trade-off"], "secret": [], "kept": [1, 2, 3]},
        "2": {"secret": [], "kept": [4]}
      }
    },
    "expect": {
      "winner": 1,
      "standings": {"1": 203, "2": 51},
      "players": {"1": {"charm": 10, "geisha_count": 3}, "2": {"charm": 5, "geisha_count": 1}}
    }
  },
  {
    "name": "R21: pair 1 ends with no winner, so hand 3 is dealt (kept emptied, markers and charm kept)",
    "rule": "R21",
    "players": 2,
    "seed": 21,
    "rounds": 2,
    "default": "decline",
    "given": {
      "game": {"hand_number": 2, "round_in_hand": 8, "starting_seat": 2, "deck": [1]},
      "players": {
        "1": {"hand": [1], "unused_actions": ["Trade-off"], "secret": [], "kept": [5]},
        "2": {"secret": [], "kept": [1, 2]}
      }
    },
    "rules": [{"seat": 1, "options_include": "Secret"}],
    "expect": {
      "game": {"marker_1": 2, "marker_2": 2, "marker_3": 0, "marker_4": 0, "marker_5": 1},
      "players": {"1": {"kept": [], "charm": 6, "geisha_count": 1}, "2": {"kept": [], "charm": 6, "geisha_count": 2}},
      "lens": {"game": {"deck": 7}, "players": {"1": {"hand": 6, "secret": 1}, "2": {"hand": 6}}}
    }
  },
  {
    "name": "R22: after hand 4 with no threshold reached, the higher charm wins (9 against 8)",
    "rule": "R22",
    "players": 2,
    "seed": 22,
    "default": "decline",
    "given": {
      "game": {"hand_number": 4, "round_in_hand": 8, "starting_seat": 2, "deck": [1]},
      "players": {
        "1": {"hand": [1], "unused_actions": ["Trade-off"], "secret": [], "kept": [5, 1]},
        "2": {"secret": [], "kept": [4, 2]}
      }
    },
    "expect": {
      "winner": 1,
      "standings": {"1": 92, "2": 82},
      "players": {"1": {"charm": 9, "geisha_count": 2}, "2": {"charm": 8, "geisha_count": 2}}
    }
  },
  {
    "name": "R22: after hand 4, equal charm (6) is broken by the higher Geisha count",
    "rule": "R22",
    "players": 2,
    "seed": 23,
    "default": "decline",
    "given": {
      "game": {"hand_number": 4, "round_in_hand": 8, "starting_seat": 2, "deck": [1]},
      "players": {
        "1": {"hand": [1], "unused_actions": ["Trade-off"], "secret": [], "kept": [5]},
        "2": {"secret": [], "kept": [1, 2]}
      }
    },
    "expect": {
      "winner": 2,
      "standings": {"1": 61, "2": 62}
    }
  },
  {
    "name": "R22: after hand 4, equal charm and equal Geisha count is a shared result",
    "rule": "R22",
    "players": 2,
    "seed": 24,
    "default": "decline",
    "given": {
      "game": {"hand_number": 4, "round_in_hand": 8, "starting_seat": 2, "deck": [1]},
      "players": {
        "1": {"hand": [1], "unused_actions": ["Trade-off"], "secret": [], "kept": [1, 4]},
        "2": {"secret": [], "kept": [2, 4]}
      }
    },
    "expect": {
      "winner": [1, 2],
      "standings": {"1": 31, "2": 31},
      "game": {"marker_1": 1, "marker_2": 2, "marker_3": 0, "marker_4": 0, "marker_5": 0}
    }
  }
]
```
````
