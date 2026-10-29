# 06 scenarios

- time: 2026-10-27T09:49:00+00:00 (125.7s)  model: claude-opus-5-5
- system prompt: [system/2ddacf4d-scenarios.md](system/2ddacf4d-scenarios.md) (sha256 2ddacf4d74fa3789)
- sent sha256 a9f462928f0e49e2, reply sha256 68d3e2a05ff31dd3

## Sent

````
SPEC:
{
  "name": "Hanamikoji: Compact Build",
  "summary": "Two players spend four one-use actions each hand to place Item cards for seven Geisha. They win a Geisha's favour by placing more of her Items, and the first to 11 Charm or 4 Geisha at a hand's end wins.",
  "players": {
    "min": 2,
    "max": 2,
    "suggested": 2
  },
  "parameters": {
    "charm_g1": 2,
    "charm_g2": 2,
    "charm_g3": 2,
    "charm_g4": 3,
    "charm_g5": 3,
    "charm_g6": 4,
    "charm_g7": 5,
    "total_charm": 21,
    "total_items": 21,
    "items_per_geisha_equals_charm": 1,
    "geisha_count": 7,
    "max_hands": 4,
    "turns_per_hand": 8,
    "cards_removed_per_hand": 1,
    "starting_hand_size": 6,
    "deck_size_after_deal": 8,
    "cards_drawn_per_turn": 1,
    "secret_cards": 1,
    "tradeoff_cards": 2,
    "gift_cards": 3,
    "competition_cards": 4,
    "gift_cards_to_opponent": 1,
    "competition_cards_per_pair": 2,
    "charm_to_win": 11,
    "geisha_to_win": 4
  },
  "attributes": {
    "player": [
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "This player's ordered hand of Item cards (hand_A for seat 1, hand_B for seat 2). Cards dealt keep their dealt order, a drawn card goes to the end, and the cards left behind keep their order.",
        "observable": false
      },
      {
        "key": "secret",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "The card held by Secret this hand, at most 1 (secret_A, secret_B). It is revealed and scored after turn 8.",
        "observable": false
      },
      {
        "key": "counts",
        "type": "list",
        "visible": "public",
        "initial": [
          0,
          0,
          0,
          0,
          0,
          0,
          0
        ],
        "meaning": "Cards this player has placed per Geisha, G1..G7, this hand (counts_A, counts_B).",
        "observable": true
      },
      {
        "key": "actions",
        "type": "list",
        "visible": "public",
        "initial": [
          "Secret",
          "Trade-off",
          "Gift",
          "Competition"
        ],
        "meaning": "This player's unused actions this hand (actions_A, actions_B).",
        "observable": false
      },
      {
        "key": "charm",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Sum of the Charm of the Geisha whose marker is on this player's side (standing[0] for A, standing[1] for B).",
        "observable": true
      },
      {
        "key": "geisha",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of Geisha markers on this player's side (standing[2] for A, standing[3] for B).",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "The ordered draw deck. Each hand it is refilled from the 21 Items: G1 x2, G2 x2, G3 x2, G4 x3, G5 x3, G6 x4, G7 x5.",
        "observable": false
      },
      {
        "key": "pile",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "Out-of-play cards: the 1 removed card and all Trade-off cards. Never revealed.",
        "observable": false
      },
      {
        "key": "markers",
        "type": "list",
        "visible": "public",
        "initial": [
          "N",
          "N",
          "N",
          "N",
          "N",
          "N",
          "N"
        ],
        "meaning": "For each Geisha G1..G7: 'A' (seat 1), 'B' (seat 2) or 'N'. Never reset between hands.",
        "observable": true
      },
      {
        "key": "charm_values",
        "type": "list",
        "visible": "public",
        "initial": [
          2,
          2,
          2,
          3,
          3,
          4,
          5
        ],
        "meaning": "Charm of G1..G7.",
        "observable": false
      },
      {
        "key": "hand_number",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Current hand, 1 to 4.",
        "observable": true
      },
      {
        "key": "turn_number",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Turn within the hand, 1 to 8. It is 9 briefly during end-of-hand scoring.",
        "observable": false
      },
      {
        "key": "active_seat",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Seat acting this turn: 1 + ((hand_number + turn_number) mod 2).",
        "observable": false
      },
      {
        "key": "chosen_action",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The action the active player chose this turn.",
        "observable": false
      },
      {
        "key": "offer",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "Cards the active player selected this turn, in order. For Competition, entries 1-2 are Pair 1 and entries 3-4 are Pair 2. Revealed to both players for Gift and Competition only.",
        "observable": false
      },
      {
        "key": "pick",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The opponent's pick: 'card 1', 'card 2' or 'card 3' for Gift, or 'Pair 1' or 'Pair 2' for Competition.",
        "observable": false
      }
    ]
  },
  "setup": [
    "Seat 1 is Player A and seat 2 is Player B.",
    "Markers start as seven 'N', and each player's charm and geisha start at 0.",
    "hand_number is 1 and turn_number is 1; the shuffle and deal happen in the first step of round one."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When turn_number = 1: deck is set to the 21 Items (G1 x2, G2 x2, G3 x2, G4 x3, G5 x3, G6 x4, G7 x5) and pile to []. Every hand, secret and offer is emptied, every counts becomes [0,0,0,0,0,0,0], and every actions becomes [Secret, Trade-off, Gift, Competition]. Then, drawing at random from deck (the shuffle): 1 card is appended to pile; 6 cards, one at a time, to the hand of the first player (seat 1 + ((hand_number + 1) mod 2)); 6 cards to the other seat's hand. The remaining 8 stay in deck in the order drawn. markers, charm and geisha are not reset."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "active_seat = 1 + ((hand_number + turn_number) mod 2)."
    },
    {
      "action": "update",
      "who": "the active seat",
      "answer": null,
      "effect": "The first card of deck is removed from deck and appended to the end of the active seat's hand."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player sees markers, both counts, both actions, both charm and geisha, hand_number and turn_number, plus their own hand and own secret."
    },
    {
      "action": "ask",
      "who": "the active seat",
      "answer": "one of the active seat's actions list (unused actions only)",
      "effect": "chosen_action = the answer. An invalid answer becomes the first unused action in the order Secret, Trade-off, Gift, Competition."
    },
    {
      "action": "ask",
      "who": "the active seat",
      "answer": "one card from the active seat's hand (first selected card)",
      "effect": "That card is removed from hand (one copy) and appended to offer. An invalid answer becomes the first card of hand."
    },
    {
      "action": "ask",
      "who": "the active seat",
      "answer": "one card from the active seat's remaining hand (second selected card)",
      "effect": "When chosen_action is not Secret: that card is removed from hand and appended to offer. An invalid answer becomes the first card of hand."
    },
    {
      "action": "ask",
      "who": "the active seat",
      "answer": "one card from the active seat's remaining hand (third selected card)",
      "effect": "When chosen_action is Gift or Competition: that card is removed from hand and appended to offer. An invalid answer becomes the first card of hand."
    },
    {
      "action": "ask",
      "who": "the active seat",
      "answer": "one card from the active seat's remaining hand (fourth selected card)",
      "effect": "When chosen_action is Competition: that card is removed from hand and appended to offer. An invalid answer becomes the first card of hand."
    },
    {
      "action": "update",
      "who": "the active seat",
      "answer": null,
      "effect": "When chosen_action is Secret: the offer card moves to the active seat's secret. When chosen_action is Trade-off: both offer cards are appended to pile. In both cases offer is emptied."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "When chosen_action is Gift or Competition: the offer is revealed to both players, in order. For Competition it is shown as Pair 1 = cards 1-2 and Pair 2 = cards 3-4."
    },
    {
      "action": "ask",
      "who": "the seat that is not active (3 - active_seat)",
      "answer": "card 1, card 2 or card 3",
      "effect": "When chosen_action is Gift: pick = the answer. An invalid answer becomes card 1."
    },
    {
      "action": "ask",
      "who": "the seat that is not active (3 - active_seat)",
      "answer": "Pair 1 or Pair 2",
      "effect": "When chosen_action is Competition: pick = the answer. An invalid answer becomes Pair 1."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When chosen_action is Gift: the picked offer card adds 1 to the opponent's counts at its Geisha, and each of the other two offer cards adds 1 to the active seat's counts at its Geisha. Announce the placement publicly."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When chosen_action is Competition: each card of the picked pair adds 1 to the opponent's counts at its Geisha, and each card of the other pair adds 1 to the active seat's counts at its Geisha. Announce the placement publicly."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "chosen_action is removed from the active seat's actions. offer, chosen_action and pick are cleared. turn_number goes up by 1."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When turn_number = 9: each player's secret is revealed to all and adds 1 to that player's counts at its Geisha, then every secret is emptied."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When turn_number = 9: for each Geisha i from 1 to 7, markers[i] = 'A' if seat 1 counts[i] > seat 2 counts[i]; 'B' if seat 2 counts[i] > seat 1 counts[i]; otherwise unchanged. Then seat 1 charm = sum of charm_values[i] over markers 'A' and seat 1 geisha = number of 'A'; seat 2 charm = sum over markers 'B' and seat 2 geisha = number of 'B'."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "When turn_number = 9: announce markers and both players' charm and geisha."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "When turn_number = 9: end the game if any player's charm >= 11, or any player's geisha >= 4, or hand_number = 4. Otherwise continue."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When turn_number = 9: hand_number goes up by 1 and turn_number = 1. The next hand's first player is then the other seat, by the active_seat formula."
    }
  ],
  "ending": {
    "condition": "turn_number = 9 and (max over players of charm >= 11 or max over players of geisha >= 4 or hand_number = 4)",
    "rank_by": "you.charm * 10 + you.geisha",
    "decided_by": "Charm held, then Geisha held. A player with 11+ Charm always has the higher Charm (the total is 21). A player with 4+ Geisha always has at least equal Charm and more Geisha whenever neither player has 11 Charm. So this one ranking reproduces the 11-Charm win, the 4-Geisha win and the hand-4 tie-break. Equal Charm and equal Geisha is a draw, a shared win."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When a hand begins (turn_number = 1), then all 21 Items are shuffled: 1 card goes to pile, 6 to the first player's hand, 6 to the second player's hand, and 8 form the deck."
    },
    {
      "id": "R2",
      "text": "When a hand begins, then both actions lists become [Secret, Trade-off, Gift, Competition], both counts become seven zeros and both secrets are emptied, while markers, charm and geisha are kept."
    },
    {
      "id": "R3",
      "text": "When hand_number is 1 or 3, then seat 1 (A) acts on odd turns and seat 2 (B) on even turns; when hand_number is 2 or 4, then seat 2 acts on odd turns and seat 1 on even turns."
    },
    {
      "id": "R4",
      "text": "When a turn starts, then the active player moves the first card of deck to the end of their hand, so their hand grows by 1 and the deck shrinks by 1."
    },
    {
      "id": "R5",
      "text": "When the active player chooses Secret, then 1 card leaves their hand and becomes their secret, hidden from the opponent until after turn 8."
    },
    {
      "id": "R6",
      "text": "When the active player chooses Trade-off, then 2 cards leave their hand and go to the pile, which is never revealed."
    },
    {
      "id": "R7",
      "text": "When the active player chooses Gift, then 3 cards leave their hand and are revealed, and the opponent picks 1 of them."
    },
    {
      "id": "R8",
      "text": "When the opponent picks a Gift card, then that card adds 1 to the opponent's counts for its Geisha and the other 2 cards add 1 each to the active player's counts."
    },
    {
      "id": "R9",
      "text": "When the active player chooses Competition, then 4 cards leave their hand and are revealed as Pair 1 (cards 1-2) and Pair 2 (cards 3-4), and the opponent picks one pair."
    },
    {
      "id": "R10",
      "text": "When the opponent picks a Competition pair, then its 2 cards add to the opponent's counts and the other 2 cards add to the active player's counts."
    },
    {
      "id": "R11",
      "text": "When a Gift or Competition pick is invalid, then it becomes option 1 (card 1 or Pair 1)."
    },
    {
      "id": "R12",
      "text": "When an action choice or card choice is invalid, then the engine uses the first unused action in the order Secret, Trade-off, Gift, Competition, and the first cards of the hand in hand order."
    },
    {
      "id": "R13",
      "text": "When an action is used, then it is removed from that player's actions and cannot be chosen again this hand, so each player uses each of the 4 actions exactly once per hand."
    },
    {
      "id": "R14",
      "text": "When turn 8 ends, then both secrets are revealed and each adds 1 to its owner's counts for its Geisha."
    },
    {
      "id": "R15",
      "text": "When turn 8 ends, then for each Geisha the player with strictly more placed cards takes her marker, and on a tie the marker stays where it was."
    },
    {
      "id": "R16",
      "text": "When markers are updated, then each player's charm is the sum of Charm (G1=2, G2=2, G3=2, G4=3, G5=3, G6=4, G7=5) of their markers, and their geisha is the number of their markers."
    },
    {
      "id": "R17",
      "text": "When a hand ends and a player has 11 or more charm, then the game ends and that player wins."
    },
    {
      "id": "R18",
      "text": "When a hand ends, no player has 11 charm and a player has 4 or more geisha, then the game ends and that player wins."
    },
    {
      "id": "R19",
      "text": "When hand 4 ends with no earlier win, then the player with higher charm wins; on equal charm the player with more geisha wins; if both are equal, the game is a draw."
    },
    {
      "id": "R20",
      "text": "When a hand ends without the game ending, then hand_number goes up by 1, turn_number returns to 1, and the other player acts first in the new hand."
    }
  ],
  "offers": [
    {
      "question": "Choose an action",
      "who": "the active seat",
      "options": "exactly the entries still in that seat's actions list (of Secret, Trade-off, Gift, Competition)"
    },
    {
      "question": "Select the 1st card",
      "who": "the active seat",
      "options": "any card in that seat's current hand"
    },
    {
      "question": "Select the 2nd card (Trade-off, Gift or Competition only)",
      "who": "the active seat",
      "options": "any card still in that seat's hand after earlier selections this turn"
    },
    {
      "question": "Select the 3rd card (Gift or Competition only)",
      "who": "the active seat",
      "options": "any card still in that seat's hand after earlier selections this turn"
    },
    {
      "question": "Select the 4th card (Competition only)",
      "who": "the active seat",
      "options": "any card still in that seat's hand after earlier selections this turn"
    },
    {
      "question": "Pick from a Gift",
      "who": "the non-active seat",
      "options": "card 1, card 2, card 3"
    },
    {
      "question": "Pick from a Competition",
      "who": "the non-active seat",
      "options": "Pair 1, Pair 2"
    }
  ],
  "choices": [
    {
      "what": "Exactly 2 players, suggested 2",
      "why": "The designer's size is kept. The game is a two-sided split-and-choose duel: every Gift and Competition is offered by one player to the single opponent, and each marker is won by comparing two counts."
    },
    {
      "what": "Seat 1 is Player A and seat 2 is Player B",
      "why": "The source names the players A and B; markers 'A' and 'B' refer to seats 1 and 2."
    },
    {
      "what": "No talk step",
      "why": "The source has no talk. In a two-player zero-sum duel, talk would only add words, and bluffing already lives in the offers."
    },
    {
      "what": "Strategy at the table",
      "why": "A thoughtful player builds Gift and Competition offers so that either answer suits them, saves Secret and Trade-off to hide or deny key Geisha, and tracks the 21-card composition and the spent actions to infer the opponent's hand."
    },
    {
      "what": "rank_by = charm * 10 + geisha",
      "why": "Geisha never exceeds 7, so charm decides first and geisha breaks ties. The 11-Charm and 4-Geisha wins always coincide with the top of this ranking, as explained under decided_by."
    }
  ],
  "simplifications": [
    {
      "what": "The single choice 'name an action and its cards' is split into one action question plus 1 to 4 card questions, each chosen from the current hand list",
      "why": "Choices from a game list make a held card automatic and count duplicates correctly. The source fallback is kept for invalid answers, though it is rarely reached."
    },
    {
      "what": "standing is stored as each player's charm and geisha attributes instead of one 4-number table list",
      "why": "Ranking is an expression over you.<attribute>; the values are identical to standing [A charm, B charm, A geisha, B geisha]."
    },
    {
      "what": "hand_A/hand_B, secret_A/secret_B, counts_A/counts_B and actions_A/actions_B become per-player attributes hand, secret, counts and actions",
      "why": "Per-player attributes with ally or public visibility give each player the same view as the source."
    },
    {
      "what": "Turn-1-only and after-turn-8-only steps are ordinary steps carrying a 'when' condition, and the after-turn-8 steps test turn_number = 9 after the increment",
      "why": "The step list is flat; single conditioned steps express it without block branching."
    },
    {
      "what": "The multi-step winner check is folded into one end condition plus the ranking",
      "why": "The engine ends on an arithmetic condition and ranks by one expression; the outcomes are unchanged."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: counts, charm, geisha; table: markers, hand_number.
````

## Reply

````
```json
[
  {
    "name": "Hand start deals 1 card to the pile, 6 to each hand and 8 to the deck (after seat 1 draws and keeps a Secret)",
    "rule": "R1",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "rules": [{"seat": 1, "options_include": "Secret"}],
    "expect": {
      "lens": {"game": {"deck": 7, "pile": 1},
               "players": {"1": {"hand": 6, "secret": 1}, "2": {"hand": 6, "secret": 0}}},
      "players": {"1": {"counts": [0,0,0,0,0,0,0]}, "2": {"counts": [0,0,0,0,0,0,0]}}
    }
  },
  {
    "name": "New hand resets counts, actions and secrets but keeps markers, charm and geisha",
    "rule": "R2",
    "players": 2,
    "seed": 2,
    "rounds": 1,
    "default": "first",
    "given": {
      "game": {"hand_number": 2, "turn_number": 1, "markers": ["A","B","N","N","N","N","N"]},
      "players": {"1": {"counts": [3,0,1,0,0,2,0], "actions": [], "secret": ["G7"], "charm": 2, "geisha": 1},
                  "2": {"counts": [0,2,0,1,0,0,1], "actions": [], "secret": ["G6"], "charm": 2, "geisha": 1}}
    },
    "rules": [{"seat": 2, "options_include": "Secret"}],
    "expect": {
      "game": {"markers": ["A","B","N","N","N","N","N"], "hand_number": 2},
      "players": {"1": {"counts": [0,0,0,0,0,0,0], "charm": 2, "geisha": 1},
                  "2": {"counts": [0,0,0,0,0,0,0], "charm": 2, "geisha": 1}},
      "lens": {"players": {"1": {"actions": 4, "secret": 0}, "2": {"actions": 3, "secret": 1}}}
    }
  },
  {
    "name": "Hand 1: seat 1 acts on turn 1 and seat 2 on turn 2",
    "rule": "R3",
    "players": 2,
    "seed": 3,
    "rounds": 2,
    "default": "first",
    "rules": [{"seat": 1, "options_include": "Secret"},
              {"seat": 2, "options_include": "Trade-off"}],
    "expect": {
      "lens": {"game": {"deck": 6},
               "players": {"1": {"actions": 3, "hand": 6}, "2": {"actions": 3, "hand": 5}}},
      "offered": [{"seat": 2, "option": "Trade-off"}]
    }
  },
  {
    "name": "Hand 2: seat 2 acts on turn 1",
    "rule": "R3",
    "players": 2,
    "seed": 4,
    "rounds": 1,
    "default": "first",
    "given": {"game": {"hand_number": 2, "turn_number": 1}},
    "rules": [{"seat": 2, "options_include": "Secret"}],
    "expect": {
      "lens": {"players": {"1": {"actions": 4, "hand": 6}, "2": {"actions": 3, "hand": 6}}},
      "offered": [{"seat": 2, "option": "Secret"}],
      "not_offered": [{"seat": 1, "option": "Secret"}, {"seat": 1, "option": "Gift"}]
    }
  },
  {
    "name": "Active player draws the first deck card into their hand",
    "rule": "R4",
    "players": 2,
    "seed": 5,
    "rounds": 1,
    "default": "first",
    "given": {
      "game": {"hand_number": 1, "turn_number": 3, "deck": ["G7","G1","G2"]},
      "players": {"1": {"hand": ["G3","G4"], "actions": ["Secret","Gift"]}}
    },
    "rules": [{"seat": 1, "options_include": "Secret"},
              {"seat": 1, "options_include": "G7"}],
    "expect": {
      "lens": {"game": {"deck": 2}, "players": {"1": {"hand": 2, "secret": 1}}},
      "offered": [{"seat": 1, "option": "G7"}]
    }
  },
  {
    "name": "Secret moves one card from hand to secret and places nothing yet",
    "rule": "R5",
    "players": 2,
    "seed": 6,
    "rounds": 1,
    "default": "first",
    "given": {
      "game": {"hand_number": 1, "turn_number": 3, "deck": ["G1","G2"]},
      "players": {"1": {"hand": ["G6","G7"], "actions": ["Secret","Gift"]}}
    },
    "rules": [{"seat": 1, "options_include": "Secret"},
              {"seat": 1, "options_include": "G6"}],
    "expect": {
      "lens": {"players": {"1": {"hand": 2, "secret": 1}}},
      "players": {"1": {"counts": [0,0,0,0,0,0,0]}, "2": {"counts": [0,0,0,0,0,0,0]}},
      "not_offered": [{"seat": 2, "option": "card 1"}, {"seat": 2, "option": "Pair 1"}]
    }
  },
  {
    "name": "Trade-off sends two cards from hand to the pile",
    "rule": "R6",
    "players": 2,
    "seed": 7,
    "rounds": 1,
    "default": "first",
    "given": {
      "game": {"hand_number": 1, "turn_number": 3, "deck": ["G1","G2"], "pile": ["G3"]},
      "players": {"1": {"hand": ["G6","G7"], "actions": ["Trade-off","Gift"]}}
    },
    "rules": [{"seat": 1, "options_include": "Trade-off"},
              {"seat": 1, "options_include": "G6"},
              {"seat": 1, "options_include": "G7"}],
    "expect": {
      "lens": {"game": {"pile": 3, "deck": 1}, "players": {"1": {"hand": 1}}},
      "players": {"1": {"counts": [0,0,0,0,0,0,0]}, "2": {"counts": [0,0,0,0,0,0,0]}},
      "not_offered": [{"seat": 2, "option": "card 1"}]
    }
  },
  {
    "name": "Gift takes three cards from hand and the opponent picks one of them",
    "rule": "R7",
    "players": 2,
    "seed": 8,
    "rounds": 1,
    "default": "first",
    "given": {
      "game": {"hand_number": 1, "turn_number": 3, "deck": ["G4","G5"]},
      "players": {"1": {"hand": ["G1","G2","G3"], "actions": ["Secret","Gift"]}}
    },
    "rules": [{"seat": 1, "options_include": "Gift"},
              {"seat": 1, "options_include": "G1"},
              {"seat": 1, "options_include": "G2"},
              {"seat": 1, "options_include": "G3"},
              {"seat": 2, "options_include": "card 1"}],
    "expect": {
      "lens": {"game": {"deck": 1}, "players": {"1": {"hand": 1}}},
      "offered": [{"seat": 2, "option": "card 1"}, {"seat": 2, "option": "card 2"}, {"seat": 2, "option": "card 3"}],
      "players": {"1": {"counts": [0,1,1,0,0,0,0]}, "2": {"counts": [1,0,0,0,0,0,0]}}
    }
  },
  {
    "name": "Gift: the picked card scores for the opponent, the other two for the giver",
    "rule": "R8",
    "players": 2,
    "seed": 9,
    "rounds": 1,
    "default": "first",
    "given": {
      "game": {"hand_number": 1, "turn_number": 3, "deck": ["G1","G2"]},
      "players": {"1": {"hand": ["G5","G6","G7"], "actions": ["Gift","Competition"]}}
    },
    "rules": [{"seat": 1, "options_include": "Gift"},
              {"seat": 1, "options_include": "G5"},
              {"seat": 1, "options_include": "G6"},
              {"seat": 1, "options_include": "G7"},
              {"seat": 2, "options_include": "card 3"}],
    "expect": {
      "players": {"1": {"counts": [0,0,0,0,1,1,0]}, "2": {"counts": [0,0,0,0,0,0,1]}}
    }
  },
  {
    "name": "Competition takes four cards from hand and the opponent picks a pair",
    "rule": "R9",
    "players": 2,
    "seed": 10,
    "rounds": 1,
    "default": "first",
    "given": {
      "game": {"hand_number": 1, "turn_number": 3, "deck": ["G5","G6"]},
      "players": {"1": {"hand": ["G1","G2","G3","G4"], "actions": ["Gift","Competition"]}}
    },
    "rules": [{"seat": 1, "options_include": "Competition"},
              {"seat": 1, "options_include": "G1"},
              {"seat": 1, "options_include": "G2"},
              {"seat": 1, "options_include": "G3"},
              {"seat": 1, "options_include": "G4"},
              {"seat": 2, "options_include": "Pair 1"}],
    "expect": {
      "lens": {"game": {"deck": 1}, "players": {"1": {"hand": 1}}},
      "offered": [{"seat": 2, "option": "Pair 1"}, {"seat": 2, "option": "Pair 2"}],
      "not_offered": [{"seat": 2, "option": "card 1"}],
      "players": {"1": {"counts": [0,0,1,1,0,0,0]}, "2": {"counts": [1,1,0,0,0,0,0]}}
    }
  },
  {
    "name": "Competition: the picked pair scores for the opponent, the other pair for the active player",
    "rule": "R10",
    "players": 2,
    "seed": 11,
    "rounds": 1,
    "default": "first",
    "given": {
      "game": {"hand_number": 1, "turn_number": 3, "deck": ["G3","G4"]},
      "players": {"1": {"hand": ["G1","G2","G6","G7"], "actions": ["Gift","Competition"]}}
    },
    "rules": [{"seat": 1, "options_include": "Competition"},
              {"seat": 1, "options_include": "G1"},
              {"seat": 1, "options_include": "G2"},
              {"seat": 1, "options_include": "G6"},
              {"seat": 1, "options_include": "G7"},
              {"seat": 2, "options_include": "Pair 2"}],
    "expect": {
      "players": {"1": {"counts": [1,1,0,0,0,0,0]}, "2": {"counts": [0,0,0,0,0,1,1]}}
    }
  },
  {
    "name": "Invalid Gift pick becomes card 1",
    "rule": "R11",
    "players": 2,
    "seed": 12,
    "rounds": 1,
    "default": "first",
    "given": {
      "game": {"hand_number": 1, "turn_number": 3, "deck": ["G1","G2"]},
      "players": {"1": {"hand": ["G5","G6","G7"], "actions": ["Gift","Competition"]}}
    },
    "rules": [{"seat": 1, "options_include": "Gift"},
              {"seat": 1, "options_include": "G5"},
              {"seat": 1, "options_include": "G6"},
              {"seat": 1, "options_include": "G7"},
              {"seat": 2, "options_include": "card 2", "answer": "card 7"}],
    "expect": {
      "players": {"1": {"counts": [0,0,0,0,0,1,1]}, "2": {"counts": [0,0,0,0,1,0,0]}}
    }
  },
  {
    "name": "Invalid Competition pick becomes Pair 1",
    "rule": "R11",
    "players": 2,
    "seed": 13,
    "rounds": 1,
    "default": "first",
    "given": {
      "game": {"hand_number": 1, "turn_number": 3, "deck": ["G3","G4"]},
      "players": {"1": {"hand": ["G1","G2","G6","G7"], "actions": ["Competition"]}}
    },
    "rules": [{"seat": 1, "options_include": "Competition"},
              {"seat": 1, "options_include": "G1"},
              {"seat": 1, "options_include": "G2"},
              {"seat": 1, "options_include": "G6"},
              {"seat": 1, "options_include": "G7"},
              {"seat": 2, "options_include": "Pair 2", "answer": "Pair 9"}],
    "expect": {
      "players": {"1": {"counts": [0,0,0,0,0,1,1]}, "2": {"counts": [1,1,0,0,0,0,0]}}
    }
  },
  {
    "name": "Invalid action becomes the first unused action and invalid cards become the first cards of hand",
    "rule": "R12",
    "players": 2,
    "seed": 14,
    "rounds": 1,
    "default": "first",
    "given": {
      "game": {"hand_number": 1, "turn_number": 3, "deck": ["G1","G2"]},
      "players": {"1": {"hand": ["G5","G6","G7"], "actions": ["Gift","Competition"]}}
    },
    "rules": [{"seat": 1, "options_include": "Gift", "answer": "Dance"},
              {"seat": 1, "options_include": "G1", "answer": "Z9", "times": "all"},
              {"seat": 2, "options_include": "card 1"}],
    "expect": {
      "players": {"1": {"counts": [0,0,0,0,0,1,1]}, "2": {"counts": [0,0,0,0,1,0,0]}}
    }
  },
  {
    "name": "Used actions are not offered again and the used action is removed",
    "rule": "R13",
    "players": 2,
    "seed": 15,
    "rounds": 1,
    "default": "first",
    "given": {
      "game": {"hand_number": 1, "turn_number": 3, "deck": ["G4","G5"]},
      "players": {"1": {"hand": ["G1","G2","G3"], "actions": ["Gift","Competition"]}}
    },
    "rules": [{"seat": 1, "options_include": "Gift"}],
    "expect": {
      "lens": {"players": {"1": {"actions": 1}}},
      "offered": [{"seat": 1, "option": "Gift"}, {"seat": 1, "option": "Competition"}],
      "not_offered": [{"seat": 1, "option": "Secret"}, {"seat": 1, "option": "Trade-off"}]
    }
  },
  {
    "name": "Each turn removes one action from the active player (three turns from the start)",
    "rule": "R13",
    "players": 2,
    "seed": 16,
    "rounds": 3,
    "default": "first",
    "rules": [],
    "expect": {
      "lens": {"players": {"1": {"actions": 2}, "2": {"actions": 3}}}
    }
  },
  {
    "name": "After turn 8 both secrets are revealed and scored",
    "rule": "R14",
    "players": 2,
    "seed": 17,
    "rounds": 1,
    "default": "first",
    "given": {
      "game": {"hand_number": 1, "turn_number": 8, "deck": ["G3"], "markers": ["N","N","N","N","N","N","N"]},
      "players": {"1": {"counts": [0,0,0,0,0,0,2], "secret": ["G7"], "actions": [], "hand": ["G4"]},
                  "2": {"counts": [0,0,0,0,0,1,0], "secret": ["G6"], "actions": ["Trade-off"], "hand": ["G1","G2"]}}
    },
    "rules": [{"seat": 2, "options_include": "Trade-off"}],
    "expect": {
      "players": {"1": {"counts": [0,0,0,0,0,0,3], "charm": 5, "geisha": 1},
                  "2": {"counts": [0,0,0,0,0,2,0], "charm": 4, "geisha": 1}},
      "game": {"markers": ["N","N","N","N","N","B","A"], "hand_number": 2}
    }
  },
  {
    "name": "Strictly more cards takes a marker; a tie leaves it where it was",
    "rule": "R15",
    "players": 2,
    "seed": 18,
    "rounds": 1,
    "default": "first",
    "given": {
      "game": {"hand_number": 1, "turn_number": 8, "deck": ["G3"], "markers": ["A","B","N","N","N","N","N"]},
      "players": {"1": {"counts": [1,1,2,0,0,0,0], "secret": [], "actions": [], "hand": ["G4"], "charm": 2, "geisha": 1},
                  "2": {"counts": [1,1,0,1,0,0,0], "secret": [], "actions": ["Trade-off"], "hand": ["G1","G2"], "charm": 2, "geisha": 1}}
    },
    "rules": [{"seat": 2, "options_include": "Trade-off"}],
    "expect": {
      "game": {"markers": ["A","B","A","B","N","N","N"], "hand_number": 2},
      "players": {"1": {"charm": 4, "geisha": 2}, "2": {"charm": 5, "geisha": 2}}
    }
  },
  {
    "name": "Charm is the sum of held Geisha's charm and geisha is the marker count",
    "rule": "R16",
    "players": 2,
    "seed": 19,
    "rounds": 1,
    "default": "first",
    "given": {
      "game": {"hand_number": 1, "turn_number": 8, "deck": ["G3"], "markers": ["B","N","N","N","N","N","N"]},
      "players": {"1": {"counts": [0,0,0,1,0,2,0], "secret": [], "actions": [], "hand": ["G5"], "charm": 0, "geisha": 0},
                  "2": {"counts": [0,0,0,0,0,0,1], "secret": [], "actions": ["Trade-off"], "hand": ["G1","G2"], "charm": 2, "geisha": 1}}
    },
    "rules": [{"seat": 2, "options_include": "Trade-off"}],
    "expect": {
      "game": {"markers": ["B","N","N","A","N","A","B"], "hand_number": 2},
      "players": {"1": {"charm": 7, "geisha": 2}, "2": {"charm": 7, "geisha": 2}}
    }
  },
  {
    "name": "11 or more charm at a hand's end wins the game",
    "rule": "R17",
    "players": 2,
    "seed": 20,
    "default": "first",
    "given": {
      "game": {"hand_number": 1, "turn_number": 8, "deck": ["G3"], "markers": ["N","N","N","N","N","N","N"]},
      "players": {"1": {"counts": [0,0,0,0,1,2,3], "secret": [], "actions": [], "hand": ["G4"]},
                  "2": {"counts": [0,0,0,0,0,0,0], "secret": [], "actions": ["Trade-off"], "hand": ["G1","G2"]}}
    },
    "rules": [{"seat": 2, "options_include": "Trade-off"}],
    "expect": {
      "winner": 1,
      "standings": {"1": 123, "2": 0},
      "game": {"markers": ["N","N","N","N","A","A","A"], "hand_number": 1},
      "players": {"1": {"charm": 12, "geisha": 3}, "2": {"charm": 0, "geisha": 0}}
    }
  },
  {
    "name": "4 geisha at a hand's end wins when nobody has 11 charm",
    "rule": "R18",
    "players": 2,
    "seed": 21,
    "default": "first",
    "given": {
      "game": {"hand_number": 1, "turn_number": 8, "deck": ["G3"], "markers": ["N","N","N","N","N","N","N"]},
      "players": {"1": {"counts": [0,0,0,0,0,0,3], "secret": [], "actions": [], "hand": ["G6"]},
                  "2": {"counts": [1,1,1,1,0,0,0], "secret": [], "actions": ["Trade-off"], "hand": ["G5","G5"]}}
    },
    "rules": [{"seat": 2, "options_include": "Trade-off"}],
    "expect": {
      "winner": 2,
      "standings": {"1": 51, "2": 94},
      "game": {"markers": ["B","B","B","B","N","N","A"], "hand_number": 1},
      "players": {"1": {"charm": 5, "geisha": 1}, "2": {"charm": 9, "geisha": 4}}
    }
  },
  {
    "name": "Hand 4 ends: equal charm, more geisha wins",
    "rule": "R19",
    "players": 2,
    "seed": 22,
    "default": "first",
    "given": {
      "game": {"hand_number": 4, "turn_number": 8, "deck": ["G3"], "markers": ["B","N","N","B","N","N","A"]},
      "players": {"1": {"counts": [0,0,0,0,0,0,0], "secret": [], "actions": ["Trade-off"], "hand": ["G5","G6"], "charm": 5, "geisha": 1},
                  "2": {"counts": [0,0,0,0,0,0,0], "secret": [], "actions": [], "hand": ["G2"], "charm": 5, "geisha": 2}}
    },
    "rules": [{"seat": 1, "options_include": "Trade-off"}],
    "expect": {
      "winner": 2,
      "standings": {"1": 51, "2": 52},
      "game": {"markers": ["B","N","N","B","N","N","A"], "hand_number": 4},
      "players": {"1": {"charm": 5, "geisha": 1}, "2": {"charm": 5, "geisha": 2}}
    }
  },
  {
    "name": "Hand 4 ends: equal charm and geisha is a shared win",
    "rule": "R19",
    "players": 2,
    "seed": 23,
    "default": "first",
    "given": {
      "game": {"hand_number": 4, "turn_number": 8, "deck": ["G3"], "markers": ["N","N","N","A","B","N","N"]},
      "players": {"1": {"counts": [0,0,0,0,0,0,0], "secret": [], "actions": ["Trade-off"], "hand": ["G6","G7"], "charm": 3, "geisha": 1},
                  "2": {"counts": [0,0,0,0,0,0,0], "secret": [], "actions": [], "hand": ["G2"], "charm": 3, "geisha": 1}}
    },
    "rules": [{"seat": 1, "options_include": "Trade-off"}],
    "expect": {
      "winner": [1, 2],
      "standings": {"1": 31, "2": 31},
      "game": {"markers": ["N","N","N","A","B","N","N"]}
    }
  },
  {
    "name": "Hand ends without a winner: next hand starts, the other seat acts first, markers kept",
    "rule": "R20",
    "players": 2,
    "seed": 24,
    "rounds": 2,
    "default": "first",
    "given": {
      "game": {"hand_number": 1, "turn_number": 8, "deck": ["G3"], "markers": ["N","N","N","N","N","N","N"]},
      "players": {"1": {"counts": [0,0,0,0,0,0,1], "secret": [], "actions": [], "hand": ["G4"]},
                  "2": {"counts": [0,0,0,0,0,0,0], "secret": [], "actions": ["Trade-off"], "hand": ["G1","G2"]}}
    },
    "rules": [{"seat": 2, "options_include": "Trade-off"},
              {"seat": 2, "options_include": "Secret"}],
    "expect": {
      "game": {"hand_number": 2, "markers": ["N","N","N","N","N","N","A"]},
      "players": {"1": {"counts": [0,0,0,0,0,0,0], "charm": 5, "geisha": 1},
                  "2": {"counts": [0,0,0,0,0,0,0], "charm": 0, "geisha": 0}},
      "lens": {"players": {"1": {"actions": 4}, "2": {"actions": 3}}},
      "not_offered": [{"seat": 1, "option": "Secret"}]
    }
  }
]
```
````
