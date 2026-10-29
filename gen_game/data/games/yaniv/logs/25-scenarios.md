# 25 scenarios

- time: 2026-10-28T06:16:27+00:00 (81.2s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 ba9a2ebc7213ca21, reply sha256 37e209312a55f15d

## Sent

````
SPEC:
{
  "name": "Simultaneous Yaniv",
  "summary": "Each round, every player secretly chooses at the same time to discard a set of equal cards or to call. Claims on cards others discarded collide, and showdowns score hand sums. The lowest total after a showdown that pushes anyone to 100, or after round 30, wins.",
  "players": {
    "min": 3,
    "max": 5,
    "suggested": 4
  },
  "parameters": {
    "call_limit": 7,
    "asaf_penalty": 30,
    "end_total": 100,
    "max_rounds": 30,
    "hand_cards": 5,
    "shoe_size": 54,
    "shoe_zeros": 2,
    "shoe_each_1_to_9": 4,
    "shoe_tens": 16,
    "joker_value": 0,
    "ace_value": 1,
    "face_value": 10,
    "caller_safe_score": 0,
    "lowest_noncaller_score": 0
  },
  "attributes": {
    "player": [
      {
        "key": "total",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "running penalty total; lowest wins",
        "observable": true
      },
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "card values held, seen only by the owner",
        "observable": false
      },
      {
        "key": "hand_sum",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "sum of hand, recomputed at setup, at a redeal, and at step 10 (announce); this is what decides whether CALL is offered",
        "observable": false
      },
      {
        "key": "hand_size",
        "type": "number",
        "visible": "public",
        "initial": 5,
        "meaning": "number of cards in hand",
        "observable": true
      },
      {
        "key": "revealed_hand",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "copy of the hand shown to all at a showdown; empty otherwise",
        "observable": true
      },
      {
        "key": "first_choice",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "this round's first choice: CALL or 'discard V', revealed after the simultaneous answer",
        "observable": false
      },
      {
        "key": "called",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "player chose CALL this round",
        "observable": true
      },
      {
        "key": "discard_value",
        "type": "number",
        "visible": "public",
        "initial": -1,
        "meaning": "value V discarded this round (-1 if none); also the value of the one card this player offers",
        "observable": true
      },
      {
        "key": "shed_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "number of cards removed this round",
        "observable": true
      },
      {
        "key": "claim",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "claim choice: BLIND or 'value V'",
        "observable": true
      },
      {
        "key": "claim_success",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "claim on an offered value succeeded",
        "observable": true
      },
      {
        "key": "took_blind",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "player received the blind card this round",
        "observable": true
      },
      {
        "key": "blind_seen",
        "type": "number",
        "visible": "ally",
        "initial": -1,
        "meaning": "the blind value B, told privately to those who took it",
        "observable": false
      },
      {
        "key": "round_score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "score added at the last showdown",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "shoe",
        "type": "list",
        "visible": "none",
        "initial": "[0,0, 1x4, 2x4, 3x4, 4x4, 5x4, 6x4, 7x4, 8x4, 9x4, 10x16] (54 values)",
        "meaning": "the shoe; draws pick a random element and never remove it, so it is always full",
        "observable": false
      },
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "current round number, 1 to 30",
        "observable": true
      },
      {
        "key": "any_call",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "at least one player chose CALL this round",
        "observable": true
      },
      {
        "key": "lowest_sum",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "L, the lowest hand_sum at a showdown",
        "observable": true
      },
      {
        "key": "lowest_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "number of players whose hand_sum equals L",
        "observable": false
      },
      {
        "key": "blind_value",
        "type": "number",
        "visible": "none",
        "initial": -1,
        "meaning": "B, this round's blind card value",
        "observable": false
      },
      {
        "key": "game_over",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "set true when a showdown happens in round 30",
        "observable": true
      }
    ]
  },
  "setup": [
    "Every player's total is set to 0 and game.round to 0.",
    "game.shoe is filled with the 54 values: two 0s, four each of 1 to 9, and sixteen 10s.",
    "In one deal operation, each player's hand receives 5 values drawn at random from game.shoe, without removing them from the shoe; each hand is visible only to its owner.",
    "Each player's hand_sum is computed as the sum of their hand, and hand_size is set to 5 publicly."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "game.round += 1; game.any_call = false; for each player: called = false, first_choice = '', discard_value = -1, shed_count = 0, claim = '', claim_success = false, took_blind = false, blind_seen = -1, revealed_hand = []"
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "short text message",
      "effect": "messages are gathered simultaneously and then broadcast to all as 'Seat {seat} says: {value}'"
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "one of: 'CALL' (only if hand_sum <= 7), then 'discard V' for each distinct V in hand, V ascending",
      "effect": "set first_choice. An invalid answer becomes CALL if hand is empty, otherwise 'discard H' with H = max(hand). called = (first_choice == 'CALL'); game.any_call = (count of players with called) >= 1; all first choices revealed publicly"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "when game.any_call: revealed_hand = hand for every player (public); game.lowest_sum = min over players of hand_sum; game.lowest_count = count of players with hand_sum == game.lowest_sum"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "when game.any_call: for each player, round_score = if called then (if hand_sum == game.lowest_sum and game.lowest_count == 1 then 0 else hand_sum + 30) else (if hand_sum == game.lowest_sum then 0 else hand_sum); total += round_score; if game.round == 30 then game.game_over = true; announce each round_score and total publicly; discards chosen this round are ignored"
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "end the game if game.any_call and (max over players of total >= 100 or game.game_over)"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "when game.any_call: in one deal operation, each hand is replaced by 5 random values from game.shoe (shoe not depleted), visible only to the owner; hand_sum = sum(hand); hand_size = 5 (public); revealed_hand = []. Steps 8 to 13 are skipped because each carries the condition not game.any_call"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "when not game.any_call: V = value in first_choice; discard_value = V; shed_count = count of V in hand; remove every V from hand (the cards leave play); announce publicly each player's discard_value and shed_count. Each player offers one card of value discard_value"
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "one of: 'BLIND', then 'value V' for each distinct V offered as discard_value by at least one OTHER player, V ascending",
      "effect": "when not game.any_call: set claim; an invalid answer becomes 'BLIND'"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "when not game.any_call: for each player with claim 'value V': claim_success = (count of players with claim == 'value V') == 1; if claim_success, append V to hand"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "when not game.any_call: game.blind_value = one random value from game.shoe (not removed); for each player with claim == 'BLIND' or not claim_success: append game.blind_value to hand, took_blind = true, blind_seen = game.blind_value (told privately)"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "when not game.any_call: hand_sum = sum(hand); hand_size = length(hand); announce publicly for each player: discard_value, shed_count, claim, claim_success, took_blind, hand_size. B and hand contents stay private"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "when not game.any_call and game.round == 30: revealed_hand = hand for all; game.lowest_sum = min hand_sum; round_score = if hand_sum == game.lowest_sum then 0 else hand_sum; total += round_score; game.game_over = true; announce publicly"
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "end the game if game.game_over or max over players of total >= 100"
    }
  ],
  "ending": {
    "condition": "game.game_over == true or max over players of total >= 100",
    "rank_by": "0 - you.total",
    "decided_by": "Each player's standing is their total, and lower is better. The player with the lowest total wins, and players tied at the lowest total share the win (a draw among them)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "Card values are Joker = 0, Ace = 1, 2 to 10 at face value, and J/Q/K = 10. The shoe holds two 0s, four each of 1 to 9, and sixteen 10s (54 cards)."
    },
    {
      "id": "R2",
      "text": "Every random draw picks a value from the full 54-card shoe; the shoe never shrinks or runs out."
    },
    {
      "id": "R3",
      "text": "At setup, every total is 0, each player is dealt 5 private cards, hand_sum is their sum, and hand_size 5 is public."
    },
    {
      "id": "R4",
      "text": "When a player's current hand_sum is 7 or less, 'CALL' is offered first; otherwise it is not offered."
    },
    {
      "id": "R5",
      "text": "A player is offered 'discard V' for each distinct value V in their hand, in ascending order."
    },
    {
      "id": "R6",
      "text": "Before the first choice, every player writes one message simultaneously, and all messages are then shown to everyone."
    },
    {
      "id": "R7",
      "text": "First choices are made simultaneously. An invalid answer becomes CALL if the hand is empty, otherwise 'discard H' where H is the highest value in the hand."
    },
    {
      "id": "R8",
      "text": "When at least one player calls, all hands are revealed and L is the lowest hand_sum."
    },
    {
      "id": "R9",
      "text": "When a caller's hand_sum is strictly lower than every other player's, the caller scores 0."
    },
    {
      "id": "R10",
      "text": "When a caller's hand_sum is tied with or above another player's, the caller scores hand_sum + 30 (Asaf); for example, a caller with 5 tied by another 5 scores 35."
    },
    {
      "id": "R11",
      "text": "When a non-caller's hand_sum equals L, they score 0; otherwise they score their hand_sum."
    },
    {
      "id": "R12",
      "text": "When anyone calls, discards chosen that round are ignored."
    },
    {
      "id": "R13",
      "text": "When a showdown leaves any total at 100 or more, the game ends."
    },
    {
      "id": "R14",
      "text": "When a call happens in round 30, the game ends after that showdown."
    },
    {
      "id": "R15",
      "text": "When a showdown does not end the game, every hand is replaced by 5 new random cards, hand_size is reset to 5, and the round ends with no discard, claim or blind draw."
    },
    {
      "id": "R16",
      "text": "When no one calls, each player removes every card of their chosen value V; the hand may become empty."
    },
    {
      "id": "R17",
      "text": "When no one calls, each player's V and the number of cards shed are announced publicly."
    },
    {
      "id": "R18",
      "text": "Claim options are 'BLIND' followed by 'value V' for each distinct V offered by at least one other player, in ascending order; a player is never offered only their own offered value."
    },
    {
      "id": "R19",
      "text": "Claims are made simultaneously, and an invalid claim counts as BLIND."
    },
    {
      "id": "R20",
      "text": "When exactly one player claims value V, that player adds one card of value V to their hand."
    },
    {
      "id": "R21",
      "text": "When two or more players claim the same V, all of their claims fail."
    },
    {
      "id": "R22",
      "text": "One blind value B is drawn per no-call round; every player who chose BLIND or whose claim failed adds one card of value B and is told B privately."
    },
    {
      "id": "R23",
      "text": "After claims, hand_sum and hand_size are recomputed, and each player's discarded value, number shed, claim, success, whether they took the blind card, and hand_size are announced; B and hands stay private."
    },
    {
      "id": "R24",
      "text": "When round 30 ends with no call, all hands are revealed, each player scores 0 if their hand_sum equals the lowest hand_sum and otherwise their hand_sum, and the game ends."
    },
    {
      "id": "R25",
      "text": "When the game ends, the lowest total wins, and players tied at the lowest total share the win."
    }
  ],
  "offers": [
    {
      "question": "Talk message",
      "who": "all players",
      "options": "any short text"
    },
    {
      "question": "First choice",
      "who": "all players",
      "options": "a seat with hand_sum <= 7: 'CALL', then 'discard V' for each distinct value in its hand, ascending; a seat with hand_sum > 7: only the 'discard V' options; a seat with an empty hand: only 'CALL'"
    },
    {
      "question": "Claim choice",
      "who": "all players (only in rounds with no call)",
      "options": "'BLIND', then 'value V' for each distinct discard_value offered by at least one other seat, ascending; a value offered only by this seat is not listed"
    }
  ],
  "choices": [
    {
      "what": "3 to 5 players, suggested 4",
      "why": "The designer suggested 4, which is kept. Claim collisions and Asaf ties need at least 3 rivals' worth of interaction, and above 5 the claim list and the announcements grow long while one player's choice matters little."
    },
    {
      "what": "Talk is a simultaneous poll broadcast to all",
      "why": "The rules say messages are written at the same time. Talk earns its place: players disagree over who claims which offered value, so announcing a claim can deter rivals or bait a collision."
    },
    {
      "what": "Ranking is 0 - total",
      "why": "The engine ranks highest first, and the lowest total wins."
    },
    {
      "what": "Asaf is tested as hand_sum == L and lowest_count == 1",
      "why": "This is an arithmetic form of 'every other hand_sum is strictly greater', using table attributes because players cannot be compared directly."
    },
    {
      "what": "game_over flag",
      "why": "This records the end that comes from a showdown in round 30, so a single check covers both endings."
    },
    {
      "what": "Strategy",
      "why": "A thoughtful player times a call against the public hand_sizes and the claims seen, avoids claiming values that others likely want, and uses talk to steer or bluff about claims."
    }
  ],
  "simplifications": [
    {
      "what": "Cards are stored as values only, with no suits or ranks",
      "why": "Only values matter in these rules; J, Q and K are all 10 and the Joker is 0."
    },
    {
      "what": "The skip of steps 5 to 11 after a call is done by putting the condition 'not game.any_call' on each later step",
      "why": "The step list is flat, but per-step conditions express the same skip exactly."
    },
    {
      "what": "Draws pick from game.shoe without removing the value",
      "why": "The source states the shoe is full for every draw."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: total, hand_size, revealed_hand, called, discard_value, shed_count, claim, claim_success, took_blind, round_score; table: round, any_call, lowest_sum, game_over.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
```json
[
  {
    "name": "Setup: the shoe holds 54 values",
    "rule": "R1",
    "players": 4,
    "seed": 1,
    "rounds": 0,
    "expect": {
      "lens": {"game": {"shoe": 54}}
    }
  },
  {
    "name": "The shoe never shrinks after a no-call round with draws",
    "rule": "R2",
    "players": 3,
    "seed": 2,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [3, 8, 8, 9, 9], "hand_sum": 37, "hand_size": 5},
        "2": {"hand": [7, 8, 9, 10, 10], "hand_sum": 44, "hand_size": 5},
        "3": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5}
      }
    },
    "expect": {
      "lens": {"game": {"shoe": 54}},
      "game": {"any_call": false}
    }
  },
  {
    "name": "Setup: totals 0, five cards each, public hand_size 5",
    "rule": "R3",
    "players": 4,
    "seed": 3,
    "rounds": 0,
    "expect": {
      "players": {
        "1": {"total": 0, "hand_size": 5},
        "2": {"total": 0, "hand_size": 5},
        "3": {"total": 0, "hand_size": 5},
        "4": {"total": 0, "hand_size": 5}
      },
      "lens": {"players": {"1": {"hand": 5}, "2": {"hand": 5}, "3": {"hand": 5}, "4": {"hand": 5}}}
    }
  },
  {
    "name": "CALL is offered at hand_sum 7 and not at hand_sum 8",
    "rule": "R4",
    "players": 3,
    "seed": 4,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [1, 1, 2, 3, 0], "hand_sum": 7, "hand_size": 5},
        "2": {"hand": [1, 1, 2, 2, 2], "hand_sum": 8, "hand_size": 5},
        "3": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "discard 1"}
    ],
    "expect": {
      "offered": [{"seat": 1, "option": "CALL"}],
      "not_offered": [{"seat": 2, "option": "CALL"}, {"seat": 3, "option": "CALL"}],
      "players": {"1": {"called": false, "discard_value": 1, "shed_count": 2}},
      "game": {"any_call": false}
    }
  },
  {
    "name": "Discard options list each distinct value in hand",
    "rule": "R5",
    "players": 3,
    "seed": 5,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [3, 3, 5, 9, 10], "hand_sum": 30, "hand_size": 5},
        "2": {"hand": [7, 8, 9, 10, 10], "hand_sum": 44, "hand_size": 5},
        "3": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "discard 9"}
    ],
    "expect": {
      "offered": [
        {"seat": 1, "option": "discard 3"},
        {"seat": 1, "option": "discard 5"},
        {"seat": 1, "option": "discard 9"},
        {"seat": 1, "option": "discard 10"}
      ],
      "not_offered": [
        {"seat": 1, "option": "discard 4"},
        {"seat": 1, "option": "CALL"}
      ],
      "players": {"1": {"discard_value": 9, "shed_count": 1}}
    }
  },
  {
    "name": "A round with talk then discards proceeds to round 1 with no call",
    "rule": "R6",
    "players": 3,
    "seed": 6,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [3, 8, 8, 9, 9], "hand_sum": 37, "hand_size": 5},
        "2": {"hand": [7, 8, 9, 10, 10], "hand_sum": 44, "hand_size": 5},
        "3": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5}
      }
    },
    "expect": {
      "game": {"round": 1, "any_call": false}
    }
  },
  {
    "name": "A seat with an empty hand is only offered CALL, calls and scores 0 as strictly lowest",
    "rule": "R7",
    "players": 3,
    "seed": 7,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [], "hand_sum": 0, "hand_size": 0},
        "2": {"hand": [5, 5, 5, 5, 5], "hand_sum": 25, "hand_size": 5},
        "3": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5}
      }
    },
    "expect": {
      "offered": [{"seat": 1, "option": "CALL"}],
      "not_offered": [{"seat": 1, "option": "discard 0"}],
      "game": {"any_call": true, "lowest_sum": 0},
      "players": {
        "1": {"called": true, "round_score": 0, "total": 0, "hand_size": 5},
        "2": {"round_score": 25, "total": 25},
        "3": {"round_score": 50, "total": 50}
      }
    }
  },
  {
    "name": "A call causes a showdown with lowest_sum L",
    "rule": "R8",
    "players": 3,
    "seed": 8,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [1, 2, 0, 1, 3], "hand_sum": 7, "hand_size": 5},
        "2": {"hand": [5, 5, 5, 5, 5], "hand_sum": 25, "hand_size": 5},
        "3": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "CALL"}
    ],
    "expect": {
      "game": {"any_call": true, "lowest_sum": 7},
      "players": {
        "1": {"called": true, "round_score": 0, "total": 0},
        "2": {"called": false, "round_score": 25, "total": 25},
        "3": {"called": false, "round_score": 50, "total": 50}
      }
    }
  },
  {
    "name": "A strictly lowest caller scores 0",
    "rule": "R9",
    "players": 4,
    "seed": 9,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [0, 1, 1, 1, 1], "hand_sum": 4, "hand_size": 5},
        "2": {"hand": [1, 1, 2, 2, 2], "hand_sum": 8, "hand_size": 5},
        "3": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5},
        "4": {"hand": [5, 5, 5, 5, 5], "hand_sum": 25, "hand_size": 5}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "CALL"}
    ],
    "expect": {
      "game": {"lowest_sum": 4},
      "players": {
        "1": {"round_score": 0, "total": 0},
        "2": {"round_score": 8, "total": 8},
        "3": {"round_score": 50, "total": 50},
        "4": {"round_score": 25, "total": 25}
      }
    }
  },
  {
    "name": "Asaf: a caller tied at 5 scores 35, the tying non-caller scores 0",
    "rule": "R10",
    "players": 3,
    "seed": 10,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [1, 1, 1, 1, 1], "hand_sum": 5, "hand_size": 5},
        "2": {"hand": [5, 0, 0, 0, 0], "hand_sum": 5, "hand_size": 5},
        "3": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "CALL"},
      {"seat": 2, "options_include": "discard 5"}
    ],
    "expect": {
      "game": {"lowest_sum": 5},
      "players": {
        "1": {"called": true, "round_score": 35, "total": 35},
        "2": {"called": false, "round_score": 0, "total": 0},
        "3": {"round_score": 50, "total": 50}
      }
    }
  },
  {
    "name": "Asaf: a caller above a non-caller scores hand_sum + 30",
    "rule": "R10",
    "players": 3,
    "seed": 11,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [2, 1, 1, 1, 1], "hand_sum": 6, "hand_size": 5},
        "2": {"hand": [3, 0, 0, 0, 0], "hand_sum": 3, "hand_size": 5},
        "3": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "CALL"},
      {"seat": 2, "options_include": "discard 3"}
    ],
    "expect": {
      "game": {"lowest_sum": 3},
      "players": {
        "1": {"round_score": 36, "total": 36},
        "2": {"round_score": 0, "total": 0},
        "3": {"round_score": 50, "total": 50}
      }
    }
  },
  {
    "name": "A non-caller at L scores 0, another non-caller scores its hand_sum",
    "rule": "R11",
    "players": 3,
    "seed": 12,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [2, 1, 1, 1, 1], "hand_sum": 6, "hand_size": 5},
        "2": {"hand": [4, 0, 0, 0, 0], "hand_sum": 4, "hand_size": 5},
        "3": {"hand": [4, 4, 4, 4, 4], "hand_sum": 20, "hand_size": 5}
      },
      "game": {}
    },
    "rules": [
      {"seat": 1, "options_include": "CALL"},
      {"seat": 2, "options_include": "discard 4"}
    ],
    "expect": {
      "game": {"lowest_sum": 4},
      "players": {
        "1": {"round_score": 36, "total": 36},
        "2": {"round_score": 0, "total": 0},
        "3": {"round_score": 20, "total": 20}
      }
    }
  },
  {
    "name": "Discards chosen in a call round are ignored",
    "rule": "R12",
    "players": 3,
    "seed": 13,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [1, 2, 0, 1, 3], "hand_sum": 7, "hand_size": 5},
        "2": {"hand": [5, 5, 5, 5, 5], "hand_sum": 25, "hand_size": 5},
        "3": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "CALL"},
      {"seat": 2, "options_include": "discard 5"},
      {"seat": 3, "options_include": "discard 10"}
    ],
    "expect": {
      "players": {
        "2": {"discard_value": -1, "shed_count": 0, "hand_size": 5, "took_blind": false},
        "3": {"discard_value": -1, "shed_count": 0, "hand_size": 5, "took_blind": false}
      },
      "not_offered": [{"seat": 2, "option": "BLIND"}, {"seat": 3, "option": "BLIND"}]
    }
  },
  {
    "name": "A showdown pushing a total to 100+ ends the game and hands stay revealed",
    "rule": "R13",
    "players": 3,
    "seed": 14,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [1, 2, 0, 1, 3], "hand_sum": 7, "hand_size": 5},
        "2": {"hand": [5, 5, 5, 5, 5], "hand_sum": 25, "hand_size": 5},
        "3": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5, "total": 60}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "CALL"}
    ],
    "expect": {
      "winner": 1,
      "standings": {"1": 0, "2": -25, "3": -110},
      "players": {
        "1": {"total": 0, "revealed_hand": [1, 2, 0, 1, 3]},
        "2": {"total": 25, "revealed_hand": [5, 5, 5, 5, 5]},
        "3": {"total": 110, "revealed_hand": [10, 10, 10, 10, 10]}
      }
    }
  },
  {
    "name": "A call in round 30 ends the game after the showdown",
    "rule": "R14",
    "players": 3,
    "seed": 15,
    "default": "first",
    "given": {
      "game": {"round": 29},
      "players": {
        "1": {"hand": [1, 2, 0, 1, 3], "hand_sum": 7, "hand_size": 5, "total": 10},
        "2": {"hand": [5, 5, 5, 5, 5], "hand_sum": 25, "hand_size": 5, "total": 20},
        "3": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5, "total": 5}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "CALL"}
    ],
    "expect": {
      "winner": 1,
      "standings": {"1": -10, "2": -45, "3": -55},
      "game": {"round": 30, "game_over": true},
      "players": {
        "1": {"total": 10},
        "2": {"total": 45},
        "3": {"total": 55}
      }
    }
  },
  {
    "name": "After a non-ending showdown every hand is redealt to 5 and no claim or blind happens",
    "rule": "R15",
    "players": 3,
    "seed": 16,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [1, 2, 3], "hand_sum": 6, "hand_size": 3},
        "2": {"hand": [5, 5, 5, 5, 5], "hand_sum": 25, "hand_size": 5},
        "3": {"hand": [10, 10, 10], "hand_sum": 30, "hand_size": 3}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "CALL"}
    ],
    "expect": {
      "players": {
        "1": {"hand_size": 5, "revealed_hand": [], "took_blind": false, "claim": ""},
        "2": {"hand_size": 5, "revealed_hand": [], "took_blind": false, "claim": ""},
        "3": {"hand_size": 5, "revealed_hand": [], "took_blind": false, "claim": ""}
      },
      "lens": {"players": {"1": {"hand": 5}, "2": {"hand": 5}, "3": {"hand": 5}}},
      "game": {"any_call": true}
    }
  },
  {
    "name": "With no call each seat removes every card of its value, then all take the blind",
    "rule": "R16",
    "players": 3,
    "seed": 17,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [4, 4, 4, 9, 10], "hand_sum": 31, "hand_size": 5},
        "2": {"hand": [5, 6, 7, 8, 9], "hand_sum": 35, "hand_size": 5},
        "3": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "discard 4"}
    ],
    "expect": {
      "players": {
        "1": {"shed_count": 3, "hand_size": 3},
        "2": {"shed_count": 1, "hand_size": 5},
        "3": {"shed_count": 5, "hand_size": 1}
      },
      "lens": {"players": {"1": {"hand": 3}, "2": {"hand": 5}, "3": {"hand": 1}}}
    }
  },
  {
    "name": "Each seat's discarded value and number shed are public",
    "rule": "R17",
    "players": 3,
    "seed": 18,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [4, 4, 4, 9, 10], "hand_sum": 31, "hand_size": 5},
        "2": {"hand": [5, 6, 7, 8, 9], "hand_sum": 35, "hand_size": 5},
        "3": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "discard 9"},
      {"seat": 2, "options_include": "discard 7"}
    ],
    "expect": {
      "players": {
        "1": {"discard_value": 9, "shed_count": 1, "called": false},
        "2": {"discard_value": 7, "shed_count": 1, "called": false},
        "3": {"discard_value": 10, "shed_count": 5, "called": false}
      },
      "game": {"any_call": false}
    }
  },
  {
    "name": "Claim options list values offered by others, never a seat's own only value",
    "rule": "R18",
    "players": 3,
    "seed": 19,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [3, 8, 8, 9, 9], "hand_sum": 37, "hand_size": 5},
        "2": {"hand": [7, 8, 9, 10, 10], "hand_sum": 44, "hand_size": 5},
        "3": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5}
      }
    },
    "expect": {
      "offered": [
        {"seat": 1, "option": "BLIND"},
        {"seat": 1, "option": "value 7"},
        {"seat": 1, "option": "value 10"},
        {"seat": 2, "option": "value 3"},
        {"seat": 2, "option": "value 10"},
        {"seat": 3, "option": "value 3"},
        {"seat": 3, "option": "value 7"}
      ],
      "not_offered": [
        {"seat": 1, "option": "value 3"},
        {"seat": 2, "option": "value 7"},
        {"seat": 3, "option": "value 10"}
      ]
    }
  },
  {
    "name": "A BLIND claim is recorded and takes the blind card",
    "rule": "R19",
    "players": 3,
    "seed": 20,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [3, 8, 8, 9, 9], "hand_sum": 37, "hand_size": 5},
        "2": {"hand": [7, 8, 9, 10, 10], "hand_sum": 44, "hand_size": 5},
        "3": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "BLIND"}
    ],
    "expect": {
      "players": {
        "1": {"claim": "BLIND", "claim_success": false, "took_blind": true, "hand_size": 5}
      }
    }
  },
  {
    "name": "A lone claim on value 7 succeeds and skips the blind",
    "rule": "R20",
    "players": 3,
    "seed": 21,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [3, 8, 8, 9, 9], "hand_sum": 37, "hand_size": 5},
        "2": {"hand": [7, 8, 9, 10, 10], "hand_sum": 44, "hand_size": 5},
        "3": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "value 7"}
    ],
    "expect": {
      "players": {
        "1": {"claim": "value 7", "claim_success": true, "took_blind": false, "hand_size": 5},
        "2": {"claim": "BLIND", "took_blind": true, "hand_size": 5},
        "3": {"claim": "BLIND", "took_blind": true, "hand_size": 1}
      }
    }
  },
  {
    "name": "Two claims on the same value both fail and take the blind",
    "rule": "R21",
    "players": 3,
    "seed": 22,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [3, 8, 8, 9, 9], "hand_sum": 37, "hand_size": 5},
        "2": {"hand": [7, 8, 9, 10, 10], "hand_sum": 44, "hand_size": 5},
        "3": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "value 7"},
      {"seat": 3, "options_include": "value 7"}
    ],
    "expect": {
      "players": {
        "1": {"claim": "value 7", "claim_success": false, "took_blind": true, "hand_size": 5},
        "3": {"claim": "value 7", "claim_success": false, "took_blind": true, "hand_size": 1},
        "2": {"claim": "BLIND", "took_blind": true, "hand_size": 5}
      }
    }
  },
  {
    "name": "Blind and failed claimers take the blind card, a successful claimer does not",
    "rule": "R22",
    "players": 4,
    "seed": 23,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [3, 8, 8, 9, 9], "hand_sum": 37, "hand_size": 5},
        "2": {"hand": [7, 8, 9, 10, 10], "hand_sum": 44, "hand_size": 5},
        "3": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5},
        "4": {"hand": [6, 9, 9, 9, 9], "hand_sum": 42, "hand_size": 5}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "value 7"},
      {"seat": 2, "options_include": "value 6"},
      {"seat": 3, "options_include": "value 6"}
    ],
    "expect": {
      "players": {
        "1": {"claim_success": true, "took_blind": false},
        "2": {"claim_success": false, "took_blind": true},
        "3": {"claim_success": false, "took_blind": true},
        "4": {"claim": "BLIND", "took_blind": true}
      }
    }
  },
  {
    "name": "After claims, hand_size and the round's public facts are announced",
    "rule": "R23",
    "players": 3,
    "seed": 24,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [4, 4, 4, 9, 10], "hand_sum": 31, "hand_size": 5},
        "2": {"hand": [5, 6, 7, 8, 9], "hand_sum": 35, "hand_size": 5},
        "3": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "discard 4"},
      {"seat": 1, "options_include": "value 10"}
    ],
    "expect": {
      "players": {
        "1": {"discard_value": 4, "shed_count": 3, "claim": "value 10", "claim_success": true, "took_blind": false, "hand_size": 3},
        "2": {"discard_value": 5, "shed_count": 1, "claim": "BLIND", "claim_success": false, "took_blind": true, "hand_size": 5},
        "3": {"discard_value": 10, "shed_count": 5, "claim": "BLIND", "claim_success": false, "took_blind": true, "hand_size": 1}
      }
    }
  },
  {
    "name": "Round 30 with no call: hands revealed, all equal at the blind value score 0, game ends",
    "rule": "R24",
    "players": 3,
    "seed": 25,
    "default": "first",
    "given": {
      "game": {"round": 29},
      "players": {
        "1": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5, "total": 10},
        "2": {"hand": [8, 8, 8, 8, 8], "hand_sum": 40, "hand_size": 5, "total": 20},
        "3": {"hand": [9, 9, 9, 9, 9], "hand_sum": 45, "hand_size": 5, "total": 30}
      }
    },
    "expect": {
      "winner": 1,
      "standings": {"1": -10, "2": -20, "3": -30},
      "game": {"round": 30, "game_over": true, "any_call": false},
      "players": {
        "1": {"round_score": 0, "total": 10, "hand_size": 1},
        "2": {"round_score": 0, "total": 20, "hand_size": 1},
        "3": {"round_score": 0, "total": 30, "hand_size": 1}
      },
      "lens": {"players": {"1": {"revealed_hand": 1}, "2": {"revealed_hand": 1}, "3": {"revealed_hand": 1}}}
    }
  },
  {
    "name": "Seats tied at the lowest final total share the win",
    "rule": "R25",
    "players": 3,
    "seed": 26,
    "default": "first",
    "given": {
      "game": {"round": 29},
      "players": {
        "1": {"hand": [1, 2, 0, 1, 3], "hand_sum": 7, "hand_size": 5, "total": 20},
        "2": {"hand": [4, 4, 4, 4, 4], "hand_sum": 20, "hand_size": 5, "total": 0},
        "3": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5, "total": 0}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "CALL"}
    ],
    "expect": {
      "winner": [1, 2],
      "standings": {"1": -20, "2": -20, "3": -50},
      "game": {"game_over": true},
      "players": {
        "1": {"round_score": 0, "total": 20},
        "2": {"round_score": 20, "total": 20},
        "3": {"round_score": 50, "total": 50}
      }
    }
  }
]
```

Why it was refused: scenario 1: needs `rules` (what each seat answers, by option name); scenario 2: needs `rules` (what each seat answers, by option name); scenario 3: needs `rules` (what each seat answers, by option name); scenario 6: needs `rules` (what each seat answers, by option name); scenario 7: needs `rules` (what each seat answers, by option name); scenario 19: needs `rules` (what each seat answers, by option name); scenario 25: needs `rules` (what each seat answers, by option name)
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
[
  {
    "name": "The shoe holds 54 values after a round (it never shrinks)",
    "rule": "R1",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "default": "last",
    "rules": [
      {"seat": 1, "options_include": "BLIND"}
    ],
    "expect": {
      "lens": {"game": {"shoe": 54}}
    }
  },
  {
    "name": "The shoe never shrinks after a no-call round with draws",
    "rule": "R2",
    "players": 3,
    "seed": 2,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [3, 8, 8, 9, 9], "hand_sum": 37, "hand_size": 5},
        "2": {"hand": [7, 8, 9, 10, 10], "hand_sum": 44, "hand_size": 5},
        "3": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "BLIND"}
    ],
    "expect": {
      "lens": {"game": {"shoe": 54}},
      "game": {"any_call": false}
    }
  },
  {
    "name": "Setup totals are 0 and stay 0 through a first no-call round (random deal, only totals asserted)",
    "rule": "R3",
    "players": 4,
    "seed": 3,
    "rounds": 1,
    "default": "last",
    "rules": [
      {"seat": 1, "options_include": "BLIND"}
    ],
    "expect": {
      "game": {"round": 1, "any_call": false},
      "players": {
        "1": {"total": 0, "claim": "BLIND", "took_blind": true},
        "2": {"total": 0},
        "3": {"total": 0},
        "4": {"total": 0}
      }
    }
  },
  {
    "name": "CALL is offered at hand_sum 7 and not at hand_sum 8",
    "rule": "R4",
    "players": 3,
    "seed": 4,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [1, 1, 2, 3, 0], "hand_sum": 7, "hand_size": 5},
        "2": {"hand": [1, 1, 2, 2, 2], "hand_sum": 8, "hand_size": 5},
        "3": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "discard 1"}
    ],
    "expect": {
      "offered": [{"seat": 1, "option": "CALL"}],
      "not_offered": [{"seat": 2, "option": "CALL"}, {"seat": 3, "option": "CALL"}],
      "players": {"1": {"called": false, "discard_value": 1, "shed_count": 2}},
      "game": {"any_call": false}
    }
  },
  {
    "name": "Discard options list each distinct value in hand",
    "rule": "R5",
    "players": 3,
    "seed": 5,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [3, 3, 5, 9, 10], "hand_sum": 30, "hand_size": 5},
        "2": {"hand": [7, 8, 9, 10, 10], "hand_sum": 44, "hand_size": 5},
        "3": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "discard 9"}
    ],
    "expect": {
      "offered": [
        {"seat": 1, "option": "discard 3"},
        {"seat": 1, "option": "discard 5"},
        {"seat": 1, "option": "discard 9"},
        {"seat": 1, "option": "discard 10"}
      ],
      "not_offered": [
        {"seat": 1, "option": "discard 4"},
        {"seat": 1, "option": "CALL"}
      ],
      "players": {"1": {"discard_value": 9, "shed_count": 1}}
    }
  },
  {
    "name": "A round with talk then discards proceeds to round 1 with no call",
    "rule": "R6",
    "players": 3,
    "seed": 6,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [3, 8, 8, 9, 9], "hand_sum": 37, "hand_size": 5},
        "2": {"hand": [7, 8, 9, 10, 10], "hand_sum": 44, "hand_size": 5},
        "3": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "BLIND"}
    ],
    "expect": {
      "game": {"round": 1, "any_call": false}
    }
  },
  {
    "name": "A seat with an empty hand is only offered CALL, calls and scores 0 as strictly lowest",
    "rule": "R7",
    "players": 3,
    "seed": 7,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [], "hand_sum": 0, "hand_size": 0},
        "2": {"hand": [5, 5, 5, 5, 5], "hand_sum": 25, "hand_size": 5},
        "3": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "CALL"}
    ],
    "expect": {
      "offered": [{"seat": 1, "option": "CALL"}],
      "not_offered": [{"seat": 1, "option": "discard 0"}],
      "game": {"any_call": true, "lowest_sum": 0},
      "players": {
        "1": {"called": true, "round_score": 0, "total": 0, "hand_size": 5},
        "2": {"round_score": 25, "total": 25},
        "3": {"round_score": 50, "total": 50}
      }
    }
  },
  {
    "name": "A call causes a showdown with lowest_sum L",
    "rule": "R8",
    "players": 3,
    "seed": 8,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [1, 2, 0, 1, 3], "hand_sum": 7, "hand_size": 5},
        "2": {"hand": [5, 5, 5, 5, 5], "hand_sum": 25, "hand_size": 5},
        "3": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "CALL"}
    ],
    "expect": {
      "game": {"any_call": true, "lowest_sum": 7},
      "players": {
        "1": {"called": true, "round_score": 0, "total": 0},
        "2": {"called": false, "round_score": 25, "total": 25},
        "3": {"called": false, "round_score": 50, "total": 50}
      }
    }
  },
  {
    "name": "A strictly lowest caller scores 0",
    "rule": "R9",
    "players": 4,
    "seed": 9,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [0, 1, 1, 1, 1], "hand_sum": 4, "hand_size": 5},
        "2": {"hand": [1, 1, 2, 2, 2], "hand_sum": 8, "hand_size": 5},
        "3": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5},
        "4": {"hand": [5, 5, 5, 5, 5], "hand_sum": 25, "hand_size": 5}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "CALL"}
    ],
    "expect": {
      "game": {"lowest_sum": 4},
      "players": {
        "1": {"round_score": 0, "total": 0},
        "2": {"round_score": 8, "total": 8},
        "3": {"round_score": 50, "total": 50},
        "4": {"round_score": 25, "total": 25}
      }
    }
  },
  {
    "name": "Asaf: a caller tied at 5 scores 35, the tying non-caller scores 0",
    "rule": "R10",
    "players": 3,
    "seed": 10,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [1, 1, 1, 1, 1], "hand_sum": 5, "hand_size": 5},
        "2": {"hand": [5, 0, 0, 0, 0], "hand_sum": 5, "hand_size": 5},
        "3": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "CALL"},
      {"seat": 2, "options_include": "discard 5"}
    ],
    "expect": {
      "game": {"lowest_sum": 5},
      "players": {
        "1": {"called": true, "round_score": 35, "total": 35},
        "2": {"called": false, "round_score": 0, "total": 0},
        "3": {"round_score": 50, "total": 50}
      }
    }
  },
  {
    "name": "Asaf: a caller above a non-caller scores hand_sum + 30",
    "rule": "R10",
    "players": 3,
    "seed": 11,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [2, 1, 1, 1, 1], "hand_sum": 6, "hand_size": 5},
        "2": {"hand": [3, 0, 0, 0, 0], "hand_sum": 3, "hand_size": 5},
        "3": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "CALL"},
      {"seat": 2, "options_include": "discard 3"}
    ],
    "expect": {
      "game": {"lowest_sum": 3},
      "players": {
        "1": {"round_score": 36, "total": 36},
        "2": {"round_score": 0, "total": 0},
        "3": {"round_score": 50, "total": 50}
      }
    }
  },
  {
    "name": "A non-caller at L scores 0, another non-caller scores its hand_sum",
    "rule": "R11",
    "players": 3,
    "seed": 12,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [2, 1, 1, 1, 1], "hand_sum": 6, "hand_size": 5},
        "2": {"hand": [4, 0, 0, 0, 0], "hand_sum": 4, "hand_size": 5},
        "3": {"hand": [4, 4, 4, 4, 4], "hand_sum": 20, "hand_size": 5}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "CALL"},
      {"seat": 2, "options_include": "discard 4"}
    ],
    "expect": {
      "game": {"lowest_sum": 4},
      "players": {
        "1": {"round_score": 36, "total": 36},
        "2": {"round_score": 0, "total": 0},
        "3": {"round_score": 20, "total": 20}
      }
    }
  },
  {
    "name": "Discards chosen in a call round are ignored",
    "rule": "R12",
    "players": 3,
    "seed": 13,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [1, 2, 0, 1, 3], "hand_sum": 7, "hand_size": 5},
        "2": {"hand": [5, 5, 5, 5, 5], "hand_sum": 25, "hand_size": 5},
        "3": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "CALL"},
      {"seat": 2, "options_include": "discard 5"},
      {"seat": 3, "options_include": "discard 10"}
    ],
    "expect": {
      "players": {
        "2": {"discard_value": -1, "shed_count": 0, "hand_size": 5, "took_blind": false},
        "3": {"discard_value": -1, "shed_count": 0, "hand_size": 5, "took_blind": false}
      },
      "not_offered": [{"seat": 2, "option": "BLIND"}, {"seat": 3, "option": "BLIND"}]
    }
  },
  {
    "name": "A showdown pushing a total to 100+ ends the game and hands stay revealed",
    "rule": "R13",
    "players": 3,
    "seed": 14,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [1, 2, 0, 1, 3], "hand_sum": 7, "hand_size": 5},
        "2": {"hand": [5, 5, 5, 5, 5], "hand_sum": 25, "hand_size": 5},
        "3": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5, "total": 60}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "CALL"}
    ],
    "expect": {
      "winner": 1,
      "standings": {"1": 0, "2": -25, "3": -110},
      "players": {
        "1": {"total": 0, "revealed_hand": [1, 2, 0, 1, 3]},
        "2": {"total": 25, "revealed_hand": [5, 5, 5, 5, 5]},
        "3": {"total": 110, "revealed_hand": [10, 10, 10, 10, 10]}
      }
    }
  },
  {
    "name": "A call in round 30 ends the game after the showdown",
    "rule": "R14",
    "players": 3,
    "seed": 15,
    "default": "first",
    "given": {
      "game": {"round": 29},
      "players": {
        "1": {"hand": [1, 2, 0, 1, 3], "hand_sum": 7, "hand_size": 5, "total": 10},
        "2": {"hand": [5, 5, 5, 5, 5], "hand_sum": 25, "hand_size": 5, "total": 20},
        "3": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5, "total": 5}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "CALL"}
    ],
    "expect": {
      "winner": 1,
      "standings": {"1": -10, "2": -45, "3": -55},
      "game": {"round": 30, "game_over": true},
      "players": {
        "1": {"total": 10},
        "2": {"total": 45},
        "3": {"total": 55}
      }
    }
  },
  {
    "name": "After a non-ending showdown every hand is redealt to 5 and no claim or blind happens",
    "rule": "R15",
    "players": 3,
    "seed": 16,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [1, 2, 3], "hand_sum": 6, "hand_size": 3},
        "2": {"hand": [5, 5, 5, 5, 5], "hand_sum": 25, "hand_size": 5},
        "3": {"hand": [10, 10, 10], "hand_sum": 30, "hand_size": 3}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "CALL"}
    ],
    "expect": {
      "players": {
        "1": {"hand_size": 5, "revealed_hand": [], "took_blind": false, "claim": ""},
        "2": {"hand_size": 5, "revealed_hand": [], "took_blind": false, "claim": ""},
        "3": {"hand_size": 5, "revealed_hand": [], "took_blind": false, "claim": ""}
      },
      "lens": {"players": {"1": {"hand": 5}, "2": {"hand": 5}, "3": {"hand": 5}}},
      "game": {"any_call": true}
    }
  },
  {
    "name": "With no call each seat removes every card of its value, then all take the blind",
    "rule": "R16",
    "players": 3,
    "seed": 17,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [4, 4, 4, 9, 10], "hand_sum": 31, "hand_size": 5},
        "2": {"hand": [5, 6, 7, 8, 9], "hand_sum": 35, "hand_size": 5},
        "3": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "discard 4"}
    ],
    "expect": {
      "players": {
        "1": {"shed_count": 3, "hand_size": 3},
        "2": {"shed_count": 1, "hand_size": 5},
        "3": {"shed_count": 5, "hand_size": 1}
      },
      "lens": {"players": {"1": {"hand": 3}, "2": {"hand": 5}, "3": {"hand": 1}}}
    }
  },
  {
    "name": "Each seat's discarded value and number shed are public",
    "rule": "R17",
    "players": 3,
    "seed": 18,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [4, 4, 4, 9, 10], "hand_sum": 31, "hand_size": 5},
        "2": {"hand": [5, 6, 7, 8, 9], "hand_sum": 35, "hand_size": 5},
        "3": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "discard 9"},
      {"seat": 2, "options_include": "discard 7"}
    ],
    "expect": {
      "players": {
        "1": {"discard_value": 9, "shed_count": 1, "called": false},
        "2": {"discard_value": 7, "shed_count": 1, "called": false},
        "3": {"discard_value": 10, "shed_count": 5, "called": false}
      },
      "game": {"any_call": false}
    }
  },
  {
    "name": "Claim options list values offered by others, never a seat's own only value",
    "rule": "R18",
    "players": 3,
    "seed": 19,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [3, 8, 8, 9, 9], "hand_sum": 37, "hand_size": 5},
        "2": {"hand": [7, 8, 9, 10, 10], "hand_sum": 44, "hand_size": 5},
        "3": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "BLIND"}
    ],
    "expect": {
      "offered": [
        {"seat": 1, "option": "BLIND"},
        {"seat": 1, "option": "value 7"},
        {"seat": 1, "option": "value 10"},
        {"seat": 2, "option": "value 3"},
        {"seat": 2, "option": "value 10"},
        {"seat": 3, "option": "value 3"},
        {"seat": 3, "option": "value 7"}
      ],
      "not_offered": [
        {"seat": 1, "option": "value 3"},
        {"seat": 2, "option": "value 7"},
        {"seat": 3, "option": "value 10"}
      ]
    }
  },
  {
    "name": "A BLIND claim is recorded and takes the blind card",
    "rule": "R19",
    "players": 3,
    "seed": 20,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [3, 8, 8, 9, 9], "hand_sum": 37, "hand_size": 5},
        "2": {"hand": [7, 8, 9, 10, 10], "hand_sum": 44, "hand_size": 5},
        "3": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "BLIND"}
    ],
    "expect": {
      "players": {
        "1": {"claim": "BLIND", "claim_success": false, "took_blind": true, "hand_size": 5}
      }
    }
  },
  {
    "name": "A lone claim on value 7 succeeds and skips the blind",
    "rule": "R20",
    "players": 3,
    "seed": 21,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [3, 8, 8, 9, 9], "hand_sum": 37, "hand_size": 5},
        "2": {"hand": [7, 8, 9, 10, 10], "hand_sum": 44, "hand_size": 5},
        "3": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "value 7"}
    ],
    "expect": {
      "players": {
        "1": {"claim": "value 7", "claim_success": true, "took_blind": false, "hand_size": 5},
        "2": {"claim": "BLIND", "took_blind": true, "hand_size": 5},
        "3": {"claim": "BLIND", "took_blind": true, "hand_size": 1}
      }
    }
  },
  {
    "name": "Two claims on the same value both fail and take the blind",
    "rule": "R21",
    "players": 3,
    "seed": 22,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [3, 8, 8, 9, 9], "hand_sum": 37, "hand_size": 5},
        "2": {"hand": [7, 8, 9, 10, 10], "hand_sum": 44, "hand_size": 5},
        "3": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "value 7"},
      {"seat": 3, "options_include": "value 7"}
    ],
    "expect": {
      "players": {
        "1": {"claim": "value 7", "claim_success": false, "took_blind": true, "hand_size": 5},
        "3": {"claim": "value 7", "claim_success": false, "took_blind": true, "hand_size": 1},
        "2": {"claim": "BLIND", "took_blind": true, "hand_size": 5}
      }
    }
  },
  {
    "name": "Blind and failed claimers take the blind card, a successful claimer does not",
    "rule": "R22",
    "players": 4,
    "seed": 23,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [3, 8, 8, 9, 9], "hand_sum": 37, "hand_size": 5},
        "2": {"hand": [7, 8, 9, 10, 10], "hand_sum": 44, "hand_size": 5},
        "3": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5},
        "4": {"hand": [6, 9, 9, 9, 9], "hand_sum": 42, "hand_size": 5}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "value 7"},
      {"seat": 2, "options_include": "value 6"},
      {"seat": 3, "options_include": "value 6"}
    ],
    "expect": {
      "players": {
        "1": {"claim_success": true, "took_blind": false},
        "2": {"claim_success": false, "took_blind": true},
        "3": {"claim_success": false, "took_blind": true},
        "4": {"claim": "BLIND", "took_blind": true}
      }
    }
  },
  {
    "name": "After claims, hand_size and the round's public facts are announced",
    "rule": "R23",
    "players": 3,
    "seed": 24,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [4, 4, 4, 9, 10], "hand_sum": 31, "hand_size": 5},
        "2": {"hand": [5, 6, 7, 8, 9], "hand_sum": 35, "hand_size": 5},
        "3": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "discard 4"},
      {"seat": 1, "options_include": "value 10"}
    ],
    "expect": {
      "players": {
        "1": {"discard_value": 4, "shed_count": 3, "claim": "value 10", "claim_success": true, "took_blind": false, "hand_size": 3},
        "2": {"discard_value": 5, "shed_count": 1, "claim": "BLIND", "claim_success": false, "took_blind": true, "hand_size": 5},
        "3": {"discard_value": 10, "shed_count": 5, "claim": "BLIND", "claim_success": false, "took_blind": true, "hand_size": 1}
      }
    }
  },
  {
    "name": "Round 30 with no call: hands revealed, all equal at the blind value score 0, game ends",
    "rule": "R24",
    "players": 3,
    "seed": 25,
    "default": "first",
    "given": {
      "game": {"round": 29},
      "players": {
        "1": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5, "total": 10},
        "2": {"hand": [8, 8, 8, 8, 8], "hand_sum": 40, "hand_size": 5, "total": 20},
        "3": {"hand": [9, 9, 9, 9, 9], "hand_sum": 45, "hand_size": 5, "total": 30}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "BLIND"}
    ],
    "expect": {
      "winner": 1,
      "standings": {"1": -10, "2": -20, "3": -30},
      "game": {"round": 30, "game_over": true, "any_call": false},
      "players": {
        "1": {"round_score": 0, "total": 10, "hand_size": 1},
        "2": {"round_score": 0, "total": 20, "hand_size": 1},
        "3": {"round_score": 0, "total": 30, "hand_size": 1}
      },
      "lens": {"players": {"1": {"revealed_hand": 1}, "2": {"revealed_hand": 1}, "3": {"revealed_hand": 1}}}
    }
  },
  {
    "name": "Seats tied at the lowest final total share the win",
    "rule": "R25",
    "players": 3,
    "seed": 26,
    "default": "first",
    "given": {
      "game": {"round": 29},
      "players": {
        "1": {"hand": [1, 2, 0, 1, 3], "hand_sum": 7, "hand_size": 5, "total": 20},
        "2": {"hand": [4, 4, 4, 4, 4], "hand_sum": 20, "hand_size": 5, "total": 0},
        "3": {"hand": [10, 10, 10, 10, 10], "hand_sum": 50, "hand_size": 5, "total": 0}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "CALL"}
    ],
    "expect": {
      "winner": [1, 2],
      "standings": {"1": -20, "2": -20, "3": -50},
      "game": {"game_over": true},
      "players": {
        "1": {"round_score": 0, "total": 20},
        "2": {"round_score": 20, "total": 20},
        "3": {"round_score": 50, "total": 50}
      }
    }
  }
]
```
````
