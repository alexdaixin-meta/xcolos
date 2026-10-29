# 30 scenarios

- time: 2026-10-27T09:18:40+00:00 (48.9s)  model: claude-opus-5-5
- system prompt: [system/2ddacf4d-scenarios.md](system/2ddacf4d-scenarios.md) (sha256 2ddacf4d74fa3789)
- sent sha256 a0ce16465befd4df, reply sha256 d0a67356d166f190

## Sent

````
SPEC:
{
  "name": "Coyote: Around the Fire",
  "summary": "Each player sees every card but their own. Players raise a claim about the table's total until someone calls Coyote, and whoever is wrong takes a token; three tokens and you are out.",
  "players": {
    "min": 3,
    "max": 4,
    "suggested": 4
  },
  "parameters": {
    "deck_size": 20,
    "count_minus2": 1,
    "count_minus1": 2,
    "count_0": 3,
    "count_1": 3,
    "count_2": 3,
    "count_3": 3,
    "count_4": 2,
    "count_5": 2,
    "count_max0": 1,
    "max0_code": 100,
    "cards_per_player": 1,
    "first_declaration_min": -3,
    "declaration_max": 20,
    "raise_min_step": 1,
    "tokens_to_eliminate": 3,
    "token_per_loss": 1,
    "max_rounds": 40,
    "first_opener_seat": 1
  },
  "attributes": {
    "player": [
      {
        "key": "seat",
        "type": "number",
        "visible": "public",
        "initial": "1..N clockwise",
        "meaning": "seat number",
        "observable": true
      },
      {
        "key": "tokens",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "hands lost; at 3 the player is eliminated (the score, lower is better)",
        "observable": true
      },
      {
        "key": "alive",
        "type": "bool",
        "visible": "public",
        "initial": true,
        "meaning": "false once the player has 3 tokens",
        "observable": true
      },
      {
        "key": "card",
        "type": "number",
        "visible": "others",
        "initial": null,
        "meaning": "this hand's face-down card: -2..5, or 100 for Max\u21920; null if not dealt. Every other player sees it, the owner never does",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [
          -2,
          -1,
          -1,
          0,
          0,
          0,
          1,
          1,
          1,
          2,
          2,
          2,
          3,
          3,
          3,
          4,
          4,
          5,
          5,
          100
        ],
        "meaning": "undealt cards of the current hand",
        "observable": false
      },
      {
        "key": "opener_seat",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "seat that takes the first turn of every round of the current hand",
        "observable": true
      },
      {
        "key": "hand_active",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "whether a hand is in progress",
        "observable": false
      },
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "round counter, up to 40",
        "observable": true
      },
      {
        "key": "has_declaration",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "false while current_declaration is none",
        "observable": false
      },
      {
        "key": "current_declaration",
        "type": "number",
        "visible": "public",
        "initial": null,
        "meaning": "the highest declaration this hand (none at hand start)",
        "observable": false
      },
      {
        "key": "current_declarer",
        "type": "number",
        "visible": "public",
        "initial": null,
        "meaning": "seat that made current_declaration",
        "observable": false
      },
      {
        "key": "declarations",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "every (seat, number) declared this hand, in order",
        "observable": false
      },
      {
        "key": "coyote_called",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "set when a player calls Coyote this hand",
        "observable": false
      },
      {
        "key": "caller",
        "type": "number",
        "visible": "public",
        "initial": null,
        "meaning": "seat that called Coyote",
        "observable": false
      },
      {
        "key": "true_total",
        "type": "number",
        "visible": "public",
        "initial": null,
        "meaning": "true total of the resolved hand",
        "observable": false
      },
      {
        "key": "last_loser",
        "type": "number",
        "visible": "public",
        "initial": null,
        "meaning": "seat that lost the last hand",
        "observable": false
      },
      {
        "key": "alive_count",
        "type": "number",
        "visible": "public",
        "initial": "N",
        "meaning": "number of alive players",
        "observable": false
      }
    ]
  },
  "setup": [
    "Seats are numbered 1 to N clockwise (N is 3 or 4).",
    "Every player gets tokens = 0 and alive = true, and alive_count = N.",
    "Set opener_seat = 1, hand_active = false and round = 1."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "when": "hand_active == false",
      "effect": "New hand. Reset deck to the 20 cards. Set every player's card to null. For each alive player, draw 1 card at random from deck into that player's card and remove it from deck. Set has_declaration = false, current_declaration = none, current_declarer = none, declarations = [], coyote_called = false, caller = none, hand_active = true."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player is sent the cards of every other alive player (card is visible to others) and never their own."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "when": "a new hand began this round",
      "effect": "Announce: 'A new hand begins; seat {opener_seat} opens.'"
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "when": "hand_active and not coyote_called and alive_count >= 1",
      "effect": "Show current_declaration, current_declarer and declarations."
    },
    {
      "action": "ask",
      "who": "the 1st alive seat clockwise starting at opener_seat",
      "when": "hand_active and not coyote_called and alive_count >= 1",
      "answer": "if has_declaration is false: a whole number from -3 to 20; otherwise one of 'coyote' or a whole number from current_declaration+1 to 20 (only 'coyote' if current_declaration == 20)",
      "effect": "On a number: current_declaration = number, current_declarer = this seat, has_declaration = true, append (seat, number) to declarations. On 'coyote': coyote_called = true, caller = this seat."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "when": "hand_active and not coyote_called and alive_count >= 2",
      "effect": "Show current_declaration, current_declarer and declarations."
    },
    {
      "action": "ask",
      "who": "the 2nd alive seat clockwise starting at opener_seat",
      "when": "hand_active and not coyote_called and alive_count >= 2",
      "answer": "as in the 1st turn",
      "effect": "as in the 1st turn"
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "when": "hand_active and not coyote_called and alive_count >= 3",
      "effect": "Show current_declaration, current_declarer and declarations."
    },
    {
      "action": "ask",
      "who": "the 3rd alive seat clockwise starting at opener_seat",
      "when": "hand_active and not coyote_called and alive_count >= 3",
      "answer": "as in the 1st turn",
      "effect": "as in the 1st turn"
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "when": "hand_active and not coyote_called and alive_count >= 4",
      "effect": "Show current_declaration, current_declarer and declarations."
    },
    {
      "action": "ask",
      "who": "the 4th alive seat clockwise starting at opener_seat",
      "when": "hand_active and not coyote_called and alive_count >= 4",
      "answer": "as in the 1st turn",
      "effect": "as in the 1st turn"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "when": "coyote_called",
      "effect": "Work out the true total. Let S = the sum of all dealt cards that are not 100, and M = the highest dealt card that is not 100. true_total = S - (M if some dealt card == 100 and M > 0, else 0); only one copy of a tied highest card is cancelled. If true_total < current_declaration, then last_loser = current_declarer, else last_loser = caller. last_loser.tokens += 1. If last_loser.tokens >= 3, then last_loser.alive = false and alive_count -= 1. opener_seat = the next alive seat clockwise from the current opener_seat (if that opener was just eliminated, the next alive seat clockwise from their seat). hand_active = false."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "when": "coyote_called",
      "effect": "Announce every alive player's card, true_total, last_loser and the tokens, and any elimination."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if alive_count == 1."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round += 1"
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if round > 40. Any unfinished hand is discarded and no token is given."
    }
  ],
  "ending": {
    "condition": "alive_count == 1 or round > 40",
    "rank_by": "you.alive * 10 - you.tokens",
    "decided_by": "Eliminated players rank below every alive player. If only one player is alive, that player wins. If 40 rounds pass, the alive player with the fewest tokens wins, and alive players tied for fewest share the result (a draw)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game starts, then every player has tokens 0 and alive true, opener_seat is 1, hand_active is false and round is 1."
    },
    {
      "id": "R2",
      "text": "When a new hand begins, then deck is reset to exactly 20 cards: one -2, two -1, three 0, three 1, three 2, three 3, two 4, two 5 and one Max\u21920 (code 100)."
    },
    {
      "id": "R3",
      "text": "When a round starts with hand_active false, then each alive player gets exactly 1 card drawn from deck, those cards leave deck, and eliminated players get no card."
    },
    {
      "id": "R4",
      "text": "When cards are dealt, then each player sees the card of every other alive player and never their own."
    },
    {
      "id": "R5",
      "text": "When a new hand begins, then current_declaration is none, declarations is empty, hand_active becomes true and everyone is told who opens."
    },
    {
      "id": "R6",
      "text": "When a round starts with hand_active true, then no cards are dealt and the hand continues with the same cards and declarations."
    },
    {
      "id": "R7",
      "text": "When a round is played, then each alive player takes at most one turn, starting at opener_seat and going clockwise through alive seats only."
    },
    {
      "id": "R8",
      "text": "When Coyote is called, then the remaining turns of that round are skipped."
    },
    {
      "id": "R9",
      "text": "When no declaration has been made this hand, then the player to act must declare a whole number from -3 to 20 and may not call Coyote."
    },
    {
      "id": "R10",
      "text": "When a declaration exists, then the player to act may declare a whole number from current_declaration+1 to 20 or call Coyote."
    },
    {
      "id": "R11",
      "text": "When current_declaration is 20, then the player to act must call Coyote."
    },
    {
      "id": "R12",
      "text": "When a player declares a number, then current_declaration becomes that number, current_declarer becomes that seat, and the pair is appended to declarations."
    },
    {
      "id": "R13",
      "text": "When Coyote is called and Max\u21920 is not dealt, then true_total is the sum of the dealt cards (for example 3, 5 and -1 give 7)."
    },
    {
      "id": "R14",
      "text": "When Coyote is called and Max\u21920 is dealt with highest other card 5, then that 5 counts as 0 (for example Max\u21920, 5 and 2 give 2)."
    },
    {
      "id": "R15",
      "text": "When Max\u21920 is dealt with two 3s as the highest other cards, then only one 3 is cancelled (for example Max\u21920, 3, 3 and 1 give 4)."
    },
    {
      "id": "R16",
      "text": "When Max\u21920 is dealt and the highest other card is 0 or less, then nothing is cancelled (for example Max\u21920, -1 and 0 give -1)."
    },
    {
      "id": "R17",
      "text": "When Coyote is called and true_total < current_declaration, then the current declarer gains 1 token."
    },
    {
      "id": "R18",
      "text": "When Coyote is called and true_total >= current_declaration, then the caller gains 1 token."
    },
    {
      "id": "R19",
      "text": "When a hand is resolved, then all cards, true_total and the loser are announced to everyone, and hand_active becomes false."
    },
    {
      "id": "R20",
      "text": "When a player reaches 3 tokens, then alive becomes false, they get no more cards and they are skipped in turn order."
    },
    {
      "id": "R21",
      "text": "When a hand ends, then opener_seat moves to the next alive seat clockwise from the current opener, whoever lost; if the opener was eliminated, it moves to the next alive seat clockwise from their seat."
    },
    {
      "id": "R22",
      "text": "When only one player is alive, then the game ends immediately and that player wins."
    },
    {
      "id": "R23",
      "text": "When round 40 ends with two or more players alive, then any unfinished hand is discarded with no token, and the alive player with the fewest tokens wins."
    },
    {
      "id": "R24",
      "text": "When round 40 ends and two or more alive players tie for fewest tokens, then the game is a draw between them."
    }
  ],
  "offers": [
    {
      "question": "A turn in a hand with no declaration yet",
      "who": "the alive seat whose turn it is",
      "options": "a whole number from -3 to 20; no Coyote"
    },
    {
      "question": "A turn with current_declaration D < 20",
      "who": "the alive seat whose turn it is",
      "options": "coyote, or a whole number from D+1 to 20"
    },
    {
      "question": "A turn with current_declaration 20",
      "who": "the alive seat whose turn it is",
      "options": "coyote only"
    },
    {
      "question": "Any turn",
      "who": "eliminated seats",
      "options": "never asked"
    }
  ],
  "choices": [
    {
      "what": "3 to 4 players, suggested 4",
      "why": "The designer chose 4. Three is the smallest table where each player reads two other cards and must guess their own while rivals push the bid. More than 4 would exceed the source's range and the 20-card deck design."
    },
    {
      "what": "No table talk step",
      "why": "The rules say declarations and calls are the only communication."
    },
    {
      "what": "Max\u21920 is stored as card code 100",
      "why": "Keeps every card a number, so the true total is pure arithmetic: code 100 counts as 0 and triggers cancelling the highest positive other card."
    },
    {
      "what": "Rank by alive*10 - tokens",
      "why": "Puts every alive player above every eliminated one and orders alive players by fewest tokens."
    },
    {
      "what": "Strategy noted",
      "why": "A good player infers their own card from the visible cards and from how others raise, and calls Coyote or raises depending on how plausible the claim is. A careless one declares at random."
    }
  ],
  "simplifications": [
    {
      "what": "A round is written as four conditional turn steps (1st to 4th alive seat clockwise from opener_seat), each skipped once Coyote is called or when fewer seats are alive",
      "why": "The step list is flat; per-step when-conditions reproduce variable turn counts and skipped turns."
    },
    {
      "what": "A tie for fewest tokens at round 40 is represented as a shared win among the tied players",
      "why": "The engine has no separate draw; tied top ranks share the result, which stands for the draw."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: seat, tokens, alive; table: opener_seat, round.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
[
  {"name": "Start: every player has 0 tokens and is alive, opener 1, round 1", "rule": "R1", "players": 4, "rounds": 0,
   "expect": {"players": {"1": {"tokens": 0, "alive": true}, "2": {"tokens": 0, "alive": true}, "3": {"tokens": 0, "alive": true}, "4": {"tokens": 0, "alive": true}},
              "game": {"opener_seat": 1, "round": 1}}},

  {"name": "New hand resets deck to 20 cards before dealing 4 (16 left)", "rule": "R2", "players": 4, "rounds": 1,
   "given": {"game": {"deck": [1, 2]}},
   "rules": [{"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 1}, {"seat": 3, "options_include": 2}, {"seat": 4, "options_include": 3}],
   "expect": {"lens": {"game": {"deck": 16}}, "game": {"round": 2}}},

  {"name": "Only alive players are dealt a card: 3 alive of 4 leaves 17 in deck", "rule": "R3", "players": 4, "rounds": 1,
   "given": {"players": {"4": {"tokens": 3, "alive": false}}, "game": {"alive_count": 3}, "status": {"4": "out"}},
   "rules": [{"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 1}, {"seat": 3, "options_include": 2}],
   "expect": {"lens": {"game": {"deck": 17}}, "players": {"4": {"tokens": 3, "alive": false}},
              "not_offered": [{"seat": 4, "option": 5}, {"seat": 4, "option": "coyote"}]}},

  {"name": "Deal gives one card per player (visibility itself is not observable)", "rule": "R4", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 1}, {"seat": 3, "options_include": 2}],
   "expect": {"lens": {"game": {"deck": 17}}}},

  {"name": "New hand clears old declarations: opener may declare -3 again", "rule": "R5", "players": 3, "rounds": 1,
   "given": {"game": {"hand_active": false, "has_declaration": true, "current_declaration": 15, "current_declarer": 2}},
   "rules": [{"seat": 1, "options_include": -3}, {"seat": 2, "options_include": -2}, {"seat": 3, "options_include": -1}],
   "expect": {"offered": [{"seat": 1, "option": -3}], "lens": {"game": {"declarations": 3}},
              "players": {"1": {"tokens": 0}, "2": {"tokens": 0}, "3": {"tokens": 0}}}},

  {"name": "Hand in progress: no new deal and the declaration carries on", "rule": "R6", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"card": 1}, "2": {"card": 2}, "3": {"card": 3}},
             "game": {"hand_active": true, "has_declaration": true, "current_declaration": 4, "current_declarer": 1, "opener_seat": 1,
                      "deck": [-2, -1, -1, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 100]}},
   "rules": [{"seat": 1, "options_include": 5}, {"seat": 2, "options_include": 6}, {"seat": 3, "options_include": 7}],
   "expect": {"lens": {"game": {"deck": 17}}, "offered": [{"seat": 1, "option": 5}], "not_offered": [{"seat": 1, "option": 4}, {"seat": 1, "option": -3}]}},

  {"name": "Turns start at opener 3 and skip eliminated seat 2", "rule": "R7", "players": 4, "rounds": 1,
   "given": {"players": {"2": {"tokens": 3, "alive": false}}, "game": {"opener_seat": 3, "alive_count": 3}, "status": {"2": "out"}},
   "rules": [{"seat": 3, "options_include": 18}, {"seat": 4, "options_include": 19}, {"seat": 1, "options_include": 20}],
   "expect": {"lens": {"game": {"declarations": 3}},
              "players": {"1": {"tokens": 0}, "3": {"tokens": 0}, "4": {"tokens": 0}},
              "offered": [{"seat": 3, "option": -3}, {"seat": 1, "option": 20}],
              "not_offered": [{"seat": 2, "option": 18}, {"seat": 2, "option": "coyote"}, {"seat": 1, "option": -3}]}},

  {"name": "Coyote by the first player skips the rest of the round", "rule": "R8", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"card": 1}, "2": {"card": 2}, "3": {"card": 0}},
             "game": {"hand_active": true, "has_declaration": true, "current_declaration": 5, "current_declarer": 3, "opener_seat": 1}},
   "rules": [{"seat": 1, "options_include": "coyote"}],
   "expect": {"players": {"1": {"tokens": 0}, "2": {"tokens": 0}, "3": {"tokens": 1}}, "game": {"opener_seat": 2},
              "not_offered": [{"seat": 2, "option": "coyote"}, {"seat": 3, "option": "coyote"}]}},

  {"name": "First declaration: -3 to 20 offered, Coyote not offered", "rule": "R9", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 1}, {"seat": 3, "options_include": 2}],
   "expect": {"offered": [{"seat": 1, "option": -3}, {"seat": 1, "option": 20}],
              "not_offered": [{"seat": 1, "option": "coyote"}, {"seat": 1, "option": -4}, {"seat": 1, "option": 21}]}},

  {"name": "With declaration 7: Coyote or 8..20 offered, not 7", "rule": "R10", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"card": 1}, "2": {"card": 2}, "3": {"card": 3}},
             "game": {"hand_active": true, "has_declaration": true, "current_declaration": 7, "current_declarer": 3, "opener_seat": 1}},
   "rules": [{"seat": 1, "options_include": 8}, {"seat": 2, "options_include": 9}, {"seat": 3, "options_include": 10}],
   "expect": {"offered": [{"seat": 1, "option": "coyote"}, {"seat": 1, "option": 8}, {"seat": 1, "option": 20}],
              "not_offered": [{"seat": 1, "option": 7}, {"seat": 1, "option": 21}],
              "players": {"1": {"tokens": 0}, "2": {"tokens": 0}, "3": {"tokens": 0}}}},

  {"name": "Declaration 20 forces Coyote (cards 1,2,3 total 6 < 20, declarer loses)", "rule": "R11", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"card": 1}, "2": {"card": 2}, "3": {"card": 3}},
             "game": {"hand_active": true, "has_declaration": true, "current_declaration": 20, "current_declarer": 3, "opener_seat": 1}},
   "rules": [{"seat": 1, "options_include": "coyote"}],
   "expect": {"offered": [{"seat": 1, "option": "coyote"}], "not_offered": [{"seat": 1, "option": 20}],
              "players": {"1": {"tokens": 0}, "2": {"tokens": 0}, "3": {"tokens": 1}}}},

  {"name": "A declaration of 6 becomes the bar: next seat offered 7, not 6", "rule": "R12", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 6}, {"seat": 2, "options_include": 7}, {"seat": 3, "options_include": 8}],
   "expect": {"lens": {"game": {"declarations": 3}},
              "offered": [{"seat": 2, "option": 7}, {"seat": 3, "option": 9}],
              "not_offered": [{"seat": 2, "option": 6}, {"seat": 3, "option": 8}]}},

  {"name": "Cards 3,5,-1 total 7; declaration 7 holds so the caller loses", "rule": "R13", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"card": 3}, "2": {"card": 5}, "3": {"card": -1}},
             "game": {"hand_active": true, "has_declaration": true, "current_declaration": 7, "current_declarer": 3, "opener_seat": 1}},
   "rules": [{"seat": 1, "options_include": "coyote"}],
   "expect": {"players": {"1": {"tokens": 1}, "2": {"tokens": 0}, "3": {"tokens": 0}}}},

  {"name": "Cards 3,5,-1 total 7; declaration 8 is too high so the declarer loses", "rule": "R13", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"card": 3}, "2": {"card": 5}, "3": {"card": -1}},
             "game": {"hand_active": true, "has_declaration": true, "current_declaration": 8, "current_declarer": 3, "opener_seat": 1}},
   "rules": [{"seat": 1, "options_include": "coyote"}],
   "expect": {"players": {"1": {"tokens": 0}, "2": {"tokens": 0}, "3": {"tokens": 1}}}},

  {"name": "Max->0, 5, 2 total 2; declaration 3 loses", "rule": "R14", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"card": 100}, "2": {"card": 5}, "3": {"card": 2}},
             "game": {"hand_active": true, "has_declaration": true, "current_declaration": 3, "current_declarer": 3, "opener_seat": 1}},
   "rules": [{"seat": 1, "options_include": "coyote"}],
   "expect": {"players": {"1": {"tokens": 0}, "2": {"tokens": 0}, "3": {"tokens": 1}}}},

  {"name": "Max->0, 3, 3, 1 total 4; declaration 4 holds, caller loses", "rule": "R15", "players": 4, "rounds": 1,
   "given": {"players": {"1": {"card": 100}, "2": {"card": 3}, "3": {"card": 3}, "4": {"card": 1}},
             "game": {"hand_active": true, "has_declaration": true, "current_declaration": 4, "current_declarer": 4, "opener_seat": 1}},
   "rules": [{"seat": 1, "options_include": "coyote"}],
   "expect": {"players": {"1": {"tokens": 1}, "2": {"tokens": 0}, "3": {"tokens": 0}, "4": {"tokens": 0}}}},

  {"name": "Max->0, 3, 3, 1 total 4; declaration 5 loses", "rule": "R15", "players": 4, "rounds": 1,
   "given": {"players": {"1": {"card": 100}, "2": {"card": 3}, "3": {"card": 3}, "4": {"card": 1}},
             "game": {"hand_active": true, "has_declaration": true, "current_declaration": 5, "current_declarer": 4, "opener_seat": 1}},
   "rules": [{"seat": 1, "options_include": "coyote"}],
   "expect": {"players": {"1": {"tokens": 0}, "2": {"tokens": 0}, "3": {"tokens": 0}, "4": {"tokens": 1}}}},

  {"name": "Max->0, -1, -2: nothing cancelled, total -3 < declaration -2, declarer loses", "rule": "R16", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"card": 100}, "2": {"card": -1}, "3": {"card": -2}},
             "game": {"hand_active": true, "has_declaration": true, "current_declaration": -2, "current_declarer": 3, "opener_seat": 1}},
   "rules": [{"seat": 1, "options_include": "coyote"}],
   "expect": {"players": {"1": {"tokens": 0}, "2": {"tokens": 0}, "3": {"tokens": 1}}}},

  {"name": "Max->0, -1, 0 total -1; declaration -1 holds, caller loses", "rule": "R16", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"card": 100}, "2": {"card": -1}, "3": {"card": 0}},
             "game": {"hand_active": true, "has_declaration": true, "current_declaration": -1, "current_declarer": 3, "opener_seat": 1}},
   "rules": [{"seat": 1, "options_include": "coyote"}],
   "expect": {"players": {"1": {"tokens": 1}, "2": {"tokens": 0}, "3": {"tokens": 0}}}},

  {"name": "Total 3 < declaration 4: declarer seat 2 gains a token", "rule": "R17", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"card": 0}, "2": {"card": 1}, "3": {"card": 2}},
             "game": {"hand_active": true, "has_declaration": true, "current_declaration": 4, "current_declarer": 2, "opener_seat": 1}},
   "rules": [{"seat": 1, "options_include": "coyote"}],
   "expect": {"players": {"1": {"tokens": 0}, "2": {"tokens": 1}, "3": {"tokens": 0}}}},

  {"name": "Total 3 >= declaration 2: caller seat 1 gains a token", "rule": "R18", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"card": 0}, "2": {"card": 1}, "3": {"card": 2}},
             "game": {"hand_active": true, "has_declaration": true, "current_declaration": 2, "current_declarer": 3, "opener_seat": 1}},
   "rules": [{"seat": 1, "options_include": "coyote"}],
   "expect": {"players": {"1": {"tokens": 1}, "2": {"tokens": 0}, "3": {"tokens": 0}}}},

  {"name": "Resolved hand ends: next round deals a fresh hand from a full deck", "rule": "R19", "players": 3, "rounds": 2,
   "given": {"players": {"1": {"card": 1}, "2": {"card": 2}, "3": {"card": 3}},
             "game": {"hand_active": true, "has_declaration": true, "current_declaration": 10, "current_declarer": 3, "opener_seat": 1, "deck": [0, 0, 4, 4, 5]}},
   "rules": [{"seat": 1, "options_include": "coyote"}, {"seat": 1, "options_include": 2},
             {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 1}],
   "expect": {"players": {"1": {"tokens": 0}, "2": {"tokens": 0}, "3": {"tokens": 1}},
              "game": {"round": 3, "opener_seat": 2}, "lens": {"game": {"deck": 17}},
              "offered": [{"seat": 2, "option": -3}]}},

  {"name": "Third token eliminates: seat 3 out, no card, skipped next round", "rule": "R20", "players": 3, "rounds": 2,
   "given": {"players": {"1": {"card": 1}, "2": {"card": 2}, "3": {"card": 3, "tokens": 2}},
             "game": {"hand_active": true, "has_declaration": true, "current_declaration": 10, "current_declarer": 3, "opener_seat": 1}},
   "rules": [{"seat": 1, "options_include": "coyote"}, {"seat": 1, "options_include": 1}, {"seat": 2, "options_include": 0}],
   "expect": {"players": {"1": {"tokens": 0, "alive": true}, "2": {"tokens": 0, "alive": true}, "3": {"tokens": 3, "alive": false}},
              "status": {"3": "out"}, "game": {"opener_seat": 2, "round": 3}, "lens": {"game": {"deck": 18}},
              "not_offered": [{"seat": 3, "option": "coyote"}, {"seat": 3, "option": 0}]}},

  {"name": "Opener moves clockwise from 3 to 4 even though another seat lost", "rule": "R21", "players": 4, "rounds": 1,
   "given": {"players": {"1": {"card": 1}, "2": {"card": 2}, "3": {"card": 3}, "4": {"card": 0}},
             "game": {"hand_active": true, "has_declaration": true, "current_declaration": 10, "current_declarer": 1, "opener_seat": 3}},
   "rules": [{"seat": 3, "options_include": "coyote"}],
   "expect": {"players": {"1": {"tokens": 1}, "2": {"tokens": 0}, "3": {"tokens": 0}, "4": {"tokens": 0}}, "game": {"opener_seat": 4}}},

  {"name": "Eliminated opener 2: opener moves to seat 3", "rule": "R21", "players": 4, "rounds": 1,
   "given": {"players": {"1": {"card": 1}, "2": {"card": 2, "tokens": 2}, "3": {"card": 3}, "4": {"card": 0}},
             "game": {"hand_active": true, "has_declaration": true, "current_declaration": 3, "current_declarer": 1, "opener_seat": 2}},
   "rules": [{"seat": 2, "options_include": "coyote"}],
   "expect": {"players": {"1": {"tokens": 0}, "2": {"tokens": 3, "alive": false}}, "status": {"2": "out"}, "game": {"opener_seat": 3}}},

  {"name": "Last rival eliminated: game ends and the sole survivor wins", "rule": "R22", "players": 3,
   "given": {"players": {"1": {"card": 1, "tokens": 1}, "2": {"card": 2, "tokens": 2}, "3": {"card": null, "tokens": 3, "alive": false}},
             "game": {"hand_active": true, "has_declaration": true, "current_declaration": 10, "current_declarer": 2, "opener_seat": 1, "alive_count": 2},
             "status": {"3": "out"}},
   "rules": [{"seat": 1, "options_include": "coyote"}],
   "expect": {"winner": 1, "standings": {"1": 9, "2": -3, "3": -3},
              "players": {"1": {"tokens": 1, "alive": true}, "2": {"tokens": 3, "alive": false}}, "status": {"2": "out"}}},

  {"name": "Round 40 ends with an unfinished hand: no token, fewest tokens wins", "rule": "R23", "players": 3,
   "given": {"players": {"1": {"tokens": 0}, "2": {"tokens": 1}, "3": {"tokens": 2}}, "game": {"round": 40}},
   "rules": [{"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 1}, {"seat": 3, "options_include": 2}],
   "expect": {"winner": 1, "standings": {"1": 10, "2": 9, "3": 8},
              "players": {"1": {"tokens": 0}, "2": {"tokens": 1}, "3": {"tokens": 2}}}},

  {"name": "Round 40 ends with seats 1 and 2 tied on fewest tokens: shared result", "rule": "R24", "players": 3,
   "given": {"players": {"1": {"tokens": 1}, "2": {"tokens": 1}, "3": {"tokens": 2}}, "game": {"round": 40}},
   "rules": [{"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 1}, {"seat": 3, "options_include": 2}],
   "expect": {"winner": [1, 2], "standings": {"1": 9, "2": 9, "3": 8}}}
]

Why it was refused: scenario 1: needs `rules` (what each seat answers, by option name)
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
[
  {"name": "Start: every player has 0 tokens and is alive, opener 1, round 1", "rule": "R1", "players": 4, "rounds": 0,
   "rules": [{"seat": 1, "options_include": 0}],
   "expect": {"players": {"1": {"tokens": 0, "alive": true}, "2": {"tokens": 0, "alive": true}, "3": {"tokens": 0, "alive": true}, "4": {"tokens": 0, "alive": true}},
              "game": {"opener_seat": 1, "round": 1}}},

  {"name": "New hand resets deck to 20 cards before dealing 4 (16 left)", "rule": "R2", "players": 4, "rounds": 1,
   "given": {"game": {"deck": [1, 2]}},
   "rules": [{"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 1}, {"seat": 3, "options_include": 2}, {"seat": 4, "options_include": 3}],
   "expect": {"lens": {"game": {"deck": 16}}, "game": {"round": 2}}},

  {"name": "Only alive players are dealt a card: 3 alive of 4 leaves 17 in deck", "rule": "R3", "players": 4, "rounds": 1,
   "given": {"players": {"4": {"tokens": 3, "alive": false}}, "game": {"alive_count": 3}, "status": {"4": "out"}},
   "rules": [{"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 1}, {"seat": 3, "options_include": 2}],
   "expect": {"lens": {"game": {"deck": 17}}, "players": {"4": {"tokens": 3, "alive": false}},
              "not_offered": [{"seat": 4, "option": 5}, {"seat": 4, "option": "coyote"}]}},

  {"name": "Deal gives one card per player (visibility itself is not observable)", "rule": "R4", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 1}, {"seat": 3, "options_include": 2}],
   "expect": {"lens": {"game": {"deck": 17}}}},

  {"name": "New hand clears old declarations: opener may declare -3 again", "rule": "R5", "players": 3, "rounds": 1,
   "given": {"game": {"hand_active": false, "has_declaration": true, "current_declaration": 15, "current_declarer": 2}},
   "rules": [{"seat": 1, "options_include": -3}, {"seat": 2, "options_include": -2}, {"seat": 3, "options_include": -1}],
   "expect": {"offered": [{"seat": 1, "option": -3}], "lens": {"game": {"declarations": 3}},
              "players": {"1": {"tokens": 0}, "2": {"tokens": 0}, "3": {"tokens": 0}}}},

  {"name": "Hand in progress: no new deal and the declaration carries on", "rule": "R6", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"card": 1}, "2": {"card": 2}, "3": {"card": 3}},
             "game": {"hand_active": true, "has_declaration": true, "current_declaration": 4, "current_declarer": 1, "opener_seat": 1,
                      "deck": [-2, -1, -1, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 100]}},
   "rules": [{"seat": 1, "options_include": 5}, {"seat": 2, "options_include": 6}, {"seat": 3, "options_include": 7}],
   "expect": {"lens": {"game": {"deck": 17}}, "offered": [{"seat": 1, "option": 5}], "not_offered": [{"seat": 1, "option": 4}, {"seat": 1, "option": -3}]}},

  {"name": "Turns start at opener 3 and skip eliminated seat 2", "rule": "R7", "players": 4, "rounds": 1,
   "given": {"players": {"2": {"tokens": 3, "alive": false}}, "game": {"opener_seat": 3, "alive_count": 3}, "status": {"2": "out"}},
   "rules": [{"seat": 3, "options_include": 18}, {"seat": 4, "options_include": 19}, {"seat": 1, "options_include": 20}],
   "expect": {"lens": {"game": {"declarations": 3}},
              "players": {"1": {"tokens": 0}, "3": {"tokens": 0}, "4": {"tokens": 0}},
              "offered": [{"seat": 3, "option": -3}, {"seat": 1, "option": 20}],
              "not_offered": [{"seat": 2, "option": 18}, {"seat": 2, "option": "coyote"}, {"seat": 1, "option": -3}]}},

  {"name": "Coyote by the first player skips the rest of the round", "rule": "R8", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"card": 1}, "2": {"card": 2}, "3": {"card": 0}},
             "game": {"hand_active": true, "has_declaration": true, "current_declaration": 5, "current_declarer": 3, "opener_seat": 1}},
   "rules": [{"seat": 1, "options_include": "coyote"}],
   "expect": {"players": {"1": {"tokens": 0}, "2": {"tokens": 0}, "3": {"tokens": 1}}, "game": {"opener_seat": 2},
              "not_offered": [{"seat": 2, "option": "coyote"}, {"seat": 3, "option": "coyote"}]}},

  {"name": "First declaration: -3 to 20 offered, Coyote not offered", "rule": "R9", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 1}, {"seat": 3, "options_include": 2}],
   "expect": {"offered": [{"seat": 1, "option": -3}, {"seat": 1, "option": 20}],
              "not_offered": [{"seat": 1, "option": "coyote"}, {"seat": 1, "option": -4}, {"seat": 1, "option": 21}]}},

  {"name": "With declaration 7: Coyote or 8..20 offered, not 7", "rule": "R10", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"card": 1}, "2": {"card": 2}, "3": {"card": 3}},
             "game": {"hand_active": true, "has_declaration": true, "current_declaration": 7, "current_declarer": 3, "opener_seat": 1}},
   "rules": [{"seat": 1, "options_include": 8}, {"seat": 2, "options_include": 9}, {"seat": 3, "options_include": 10}],
   "expect": {"offered": [{"seat": 1, "option": "coyote"}, {"seat": 1, "option": 8}, {"seat": 1, "option": 20}],
              "not_offered": [{"seat": 1, "option": 7}, {"seat": 1, "option": 21}],
              "players": {"1": {"tokens": 0}, "2": {"tokens": 0}, "3": {"tokens": 0}}}},

  {"name": "Declaration 20 forces Coyote (cards 1,2,3 total 6 < 20, declarer loses)", "rule": "R11", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"card": 1}, "2": {"card": 2}, "3": {"card": 3}},
             "game": {"hand_active": true, "has_declaration": true, "current_declaration": 20, "current_declarer": 3, "opener_seat": 1}},
   "rules": [{"seat": 1, "options_include": "coyote"}],
   "expect": {"offered": [{"seat": 1, "option": "coyote"}], "not_offered": [{"seat": 1, "option": 20}],
              "players": {"1": {"tokens": 0}, "2": {"tokens": 0}, "3": {"tokens": 1}}}},

  {"name": "A declaration of 6 becomes the bar: next seat offered 7, not 6", "rule": "R12", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 6}, {"seat": 2, "options_include": 7}, {"seat": 3, "options_include": 8}],
   "expect": {"lens": {"game": {"declarations": 3}},
              "offered": [{"seat": 2, "option": 7}, {"seat": 3, "option": 9}],
              "not_offered": [{"seat": 2, "option": 6}, {"seat": 3, "option": 8}]}},

  {"name": "Cards 3,5,-1 total 7; declaration 7 holds so the caller loses", "rule": "R13", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"card": 3}, "2": {"card": 5}, "3": {"card": -1}},
             "game": {"hand_active": true, "has_declaration": true, "current_declaration": 7, "current_declarer": 3, "opener_seat": 1}},
   "rules": [{"seat": 1, "options_include": "coyote"}],
   "expect": {"players": {"1": {"tokens": 1}, "2": {"tokens": 0}, "3": {"tokens": 0}}}},

  {"name": "Cards 3,5,-1 total 7; declaration 8 is too high so the declarer loses", "rule": "R13", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"card": 3}, "2": {"card": 5}, "3": {"card": -1}},
             "game": {"hand_active": true, "has_declaration": true, "current_declaration": 8, "current_declarer": 3, "opener_seat": 1}},
   "rules": [{"seat": 1, "options_include": "coyote"}],
   "expect": {"players": {"1": {"tokens": 0}, "2": {"tokens": 0}, "3": {"tokens": 1}}}},

  {"name": "Max->0, 5, 2 total 2; declaration 3 loses", "rule": "R14", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"card": 100}, "2": {"card": 5}, "3": {"card": 2}},
             "game": {"hand_active": true, "has_declaration": true, "current_declaration": 3, "current_declarer": 3, "opener_seat": 1}},
   "rules": [{"seat": 1, "options_include": "coyote"}],
   "expect": {"players": {"1": {"tokens": 0}, "2": {"tokens": 0}, "3": {"tokens": 1}}}},

  {"name": "Max->0, 3, 3, 1 total 4; declaration 4 holds, caller loses", "rule": "R15", "players": 4, "rounds": 1,
   "given": {"players": {"1": {"card": 100}, "2": {"card": 3}, "3": {"card": 3}, "4": {"card": 1}},
             "game": {"hand_active": true, "has_declaration": true, "current_declaration": 4, "current_declarer": 4, "opener_seat": 1}},
   "rules": [{"seat": 1, "options_include": "coyote"}],
   "expect": {"players": {"1": {"tokens": 1}, "2": {"tokens": 0}, "3": {"tokens": 0}, "4": {"tokens": 0}}}},

  {"name": "Max->0, 3, 3, 1 total 4; declaration 5 loses", "rule": "R15", "players": 4, "rounds": 1,
   "given": {"players": {"1": {"card": 100}, "2": {"card": 3}, "3": {"card": 3}, "4": {"card": 1}},
             "game": {"hand_active": true, "has_declaration": true, "current_declaration": 5, "current_declarer": 4, "opener_seat": 1}},
   "rules": [{"seat": 1, "options_include": "coyote"}],
   "expect": {"players": {"1": {"tokens": 0}, "2": {"tokens": 0}, "3": {"tokens": 0}, "4": {"tokens": 1}}}},

  {"name": "Max->0, -1, -2: nothing cancelled, total -3 < declaration -2, declarer loses", "rule": "R16", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"card": 100}, "2": {"card": -1}, "3": {"card": -2}},
             "game": {"hand_active": true, "has_declaration": true, "current_declaration": -2, "current_declarer": 3, "opener_seat": 1}},
   "rules": [{"seat": 1, "options_include": "coyote"}],
   "expect": {"players": {"1": {"tokens": 0}, "2": {"tokens": 0}, "3": {"tokens": 1}}}},

  {"name": "Max->0, -1, 0 total -1; declaration -1 holds, caller loses", "rule": "R16", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"card": 100}, "2": {"card": -1}, "3": {"card": 0}},
             "game": {"hand_active": true, "has_declaration": true, "current_declaration": -1, "current_declarer": 3, "opener_seat": 1}},
   "rules": [{"seat": 1, "options_include": "coyote"}],
   "expect": {"players": {"1": {"tokens": 1}, "2": {"tokens": 0}, "3": {"tokens": 0}}}},

  {"name": "Total 3 < declaration 4: declarer seat 2 gains a token", "rule": "R17", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"card": 0}, "2": {"card": 1}, "3": {"card": 2}},
             "game": {"hand_active": true, "has_declaration": true, "current_declaration": 4, "current_declarer": 2, "opener_seat": 1}},
   "rules": [{"seat": 1, "options_include": "coyote"}],
   "expect": {"players": {"1": {"tokens": 0}, "2": {"tokens": 1}, "3": {"tokens": 0}}}},

  {"name": "Total 3 >= declaration 2: caller seat 1 gains a token", "rule": "R18", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"card": 0}, "2": {"card": 1}, "3": {"card": 2}},
             "game": {"hand_active": true, "has_declaration": true, "current_declaration": 2, "current_declarer": 3, "opener_seat": 1}},
   "rules": [{"seat": 1, "options_include": "coyote"}],
   "expect": {"players": {"1": {"tokens": 1}, "2": {"tokens": 0}, "3": {"tokens": 0}}}},

  {"name": "Resolved hand ends: next round deals a fresh hand from a full deck", "rule": "R19", "players": 3, "rounds": 2,
   "given": {"players": {"1": {"card": 1}, "2": {"card": 2}, "3": {"card": 3}},
             "game": {"hand_active": true, "has_declaration": true, "current_declaration": 10, "current_declarer": 3, "opener_seat": 1, "deck": [0, 0, 4, 4, 5]}},
   "rules": [{"seat": 1, "options_include": "coyote"}, {"seat": 1, "options_include": 2},
             {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 1}],
   "expect": {"players": {"1": {"tokens": 0}, "2": {"tokens": 0}, "3": {"tokens": 1}},
              "game": {"round": 3, "opener_seat": 2}, "lens": {"game": {"deck": 17}},
              "offered": [{"seat": 2, "option": -3}]}},

  {"name": "Third token eliminates: seat 3 out, no card, skipped next round", "rule": "R20", "players": 3, "rounds": 2,
   "given": {"players": {"1": {"card": 1}, "2": {"card": 2}, "3": {"card": 3, "tokens": 2}},
             "game": {"hand_active": true, "has_declaration": true, "current_declaration": 10, "current_declarer": 3, "opener_seat": 1}},
   "rules": [{"seat": 1, "options_include": "coyote"}, {"seat": 1, "options_include": 1}, {"seat": 2, "options_include": 0}],
   "expect": {"players": {"1": {"tokens": 0, "alive": true}, "2": {"tokens": 0, "alive": true}, "3": {"tokens": 3, "alive": false}},
              "status": {"3": "out"}, "game": {"opener_seat": 2, "round": 3}, "lens": {"game": {"deck": 18}},
              "not_offered": [{"seat": 3, "option": "coyote"}, {"seat": 3, "option": 0}]}},

  {"name": "Opener moves clockwise from 3 to 4 even though another seat lost", "rule": "R21", "players": 4, "rounds": 1,
   "given": {"players": {"1": {"card": 1}, "2": {"card": 2}, "3": {"card": 3}, "4": {"card": 0}},
             "game": {"hand_active": true, "has_declaration": true, "current_declaration": 10, "current_declarer": 1, "opener_seat": 3}},
   "rules": [{"seat": 3, "options_include": "coyote"}],
   "expect": {"players": {"1": {"tokens": 1}, "2": {"tokens": 0}, "3": {"tokens": 0}, "4": {"tokens": 0}}, "game": {"opener_seat": 4}}},

  {"name": "Eliminated opener 2: opener moves to seat 3", "rule": "R21", "players": 4, "rounds": 1,
   "given": {"players": {"1": {"card": 1}, "2": {"card": 2, "tokens": 2}, "3": {"card": 3}, "4": {"card": 0}},
             "game": {"hand_active": true, "has_declaration": true, "current_declaration": 3, "current_declarer": 1, "opener_seat": 2}},
   "rules": [{"seat": 2, "options_include": "coyote"}],
   "expect": {"players": {"1": {"tokens": 0}, "2": {"tokens": 3, "alive": false}}, "status": {"2": "out"}, "game": {"opener_seat": 3}}},

  {"name": "Last rival eliminated: game ends and the sole survivor wins", "rule": "R22", "players": 3,
   "given": {"players": {"1": {"card": 1, "tokens": 1}, "2": {"card": 2, "tokens": 2}, "3": {"card": null, "tokens": 3, "alive": false}},
             "game": {"hand_active": true, "has_declaration": true, "current_declaration": 10, "current_declarer": 2, "opener_seat": 1, "alive_count": 2},
             "status": {"3": "out"}},
   "rules": [{"seat": 1, "options_include": "coyote"}],
   "expect": {"winner": 1, "standings": {"1": 9, "2": -3, "3": -3},
              "players": {"1": {"tokens": 1, "alive": true}, "2": {"tokens": 3, "alive": false}}, "status": {"2": "out"}}},

  {"name": "Round 40 ends with an unfinished hand: no token, fewest tokens wins", "rule": "R23", "players": 3,
   "given": {"players": {"1": {"tokens": 0}, "2": {"tokens": 1}, "3": {"tokens": 2}}, "game": {"round": 40}},
   "rules": [{"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 1}, {"seat": 3, "options_include": 2}],
   "expect": {"winner": 1, "standings": {"1": 10, "2": 9, "3": 8},
              "players": {"1": {"tokens": 0}, "2": {"tokens": 1}, "3": {"tokens": 2}}}},

  {"name": "Round 40 ends with seats 1 and 2 tied on fewest tokens: shared result", "rule": "R24", "players": 3,
   "given": {"players": {"1": {"tokens": 1}, "2": {"tokens": 1}, "3": {"tokens": 2}}, "game": {"round": 40}},
   "rules": [{"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 1}, {"seat": 3, "options_include": 2}],
   "expect": {"winner": [1, 2], "standings": {"1": 9, "2": 9, "3": 8}}}
]
````
