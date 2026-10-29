# 04 scenarios

- time: 2026-10-28T01:34:42+00:00 (70.0s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 cf3053bff2613f60, reply sha256 e4eee422f7ccdc29

## Sent

````
SPEC:
{
  "name": "Forehead Poker Match",
  "summary": "Over 16 hands, each player sees every other player's card but never their own, talks, bets and calls; the player with the most chips at the end wins.",
  "players": {
    "min": 4,
    "max": 6,
    "suggested": 4
  },
  "parameters": {
    "starting_chips": 40,
    "starting_pot": 0,
    "hands": 16,
    "elimination_below": 4,
    "ante": 1,
    "bet_min": 1,
    "bet_max": 3,
    "message_max_words": 40,
    "deck_size": 52,
    "cards_per_player": 1,
    "suits_per_rank": 4
  },
  "attributes": {
    "player": [
      {
        "key": "chips",
        "type": "number",
        "visible": "public",
        "initial": 40,
        "meaning": "The player's chip stack. This is the score. It freezes when the player is eliminated.",
        "observable": true
      },
      {
        "key": "active",
        "type": "bool",
        "visible": "public",
        "initial": true,
        "meaning": "Whether the player is still in the match. It becomes false when the player starts a hand with fewer than 4 chips.",
        "observable": true
      },
      {
        "key": "card",
        "type": "text",
        "visible": "others",
        "initial": "",
        "meaning": "The card dealt this hand, such as 'Q of Hearts'. Every other player sees it; the owner does not.",
        "observable": false
      },
      {
        "key": "card_value",
        "type": "number",
        "visible": "others",
        "initial": 0,
        "meaning": "The card's strength from 1 (2 of Clubs) to 52 (A of Spades), worked out as rank_index*4 + suit_index. rank_index runs 0 for 2 up to 12 for A. suit_index is Clubs 1, Diamonds 2, Hearts 3, Spades 4. It is 0 when no card is held.",
        "observable": false
      },
      {
        "key": "bet",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The step-5 bet this hand: 0 for a fold, otherwise 1 to 3.",
        "observable": false
      },
      {
        "key": "folded",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "Whether the player folded in step 5 or step 7 of this hand.",
        "observable": false
      },
      {
        "key": "called",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "Whether the player called in step 7 of this hand.",
        "observable": false
      },
      {
        "key": "shown_card",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The player's card, revealed to everyone after the showdown. It is empty before then.",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": "the 52 standard cards",
        "meaning": "The shuffled deck that cards are dealt from. It is refilled to all 52 cards every hand.",
        "observable": false
      },
      {
        "key": "pot",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The chips in the pot. It carries over when nobody calls.",
        "observable": true
      },
      {
        "key": "hand_number",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The number of hands completed so far.",
        "observable": true
      },
      {
        "key": "high_bet",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "H, the highest step-5 bet this hand. It is 0 if everyone folded.",
        "observable": false
      },
      {
        "key": "caller_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "How many players called in step 7.",
        "observable": false
      },
      {
        "key": "best_value",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "The highest card_value among this hand's callers. It is 0 if there are no callers.",
        "observable": false
      }
    ]
  },
  "setup": [
    "Each player gets 40 chips and is marked active.",
    "The pot is set to 0 and hand_number to 0.",
    "The deck list is filled with the 52 standard cards."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "ELIGIBILITY: every active player with chips < 4 gets active = false, and their chips stay as their final total. Then every player is reset for the hand: bet = 0, folded = false, called = false, card = '', card_value = 0, shown_card = ''. On the table, high_bet, caller_count and best_value are set to 0."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "The game ends if the number of players with active = true is 1 or fewer. Any pot is discarded."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "DEAL: deck is reset to all 52 cards. Each active player draws one card at random: it is removed from deck and its name is set as card, with its strength as card_value."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player is sent their state. They see the card and card_value of every other active player, but not their own."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "ANTE: each active player pays 1: chips -= 1 and pot += 1."
    },
    {
      "action": "poll",
      "who": "every active player",
      "answer": "short text, at most 40 words",
      "effect": "TALK: once every message is in, each one is broadcast to all as 'Seat {seat} says: {value}'. No message binds anyone."
    },
    {
      "action": "poll",
      "who": "every active player",
      "answer": "one of: Fold, Bet 1, Bet 2, Bet 3",
      "effect": "FIRST BET: answers are collected simultaneously and stored. Nothing is shown until all are in."
    },
    {
      "action": "update",
      "who": "every active player",
      "answer": null,
      "effect": "On Fold: bet = 0 and folded = true. On Bet k: bet = k, chips -= k and pot += k. Then high_bet = the largest bet among active players."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "REVEAL BETS: every player's step-5 choice (bet or fold) and H = high_bet are announced to everyone."
    },
    {
      "action": "poll",
      "who": "every active player with bet >= 1",
      "answer": "one of: Call, Fold",
      "effect": "CALL OR FOLD: answers are collected simultaneously. This step is skipped if nobody bet."
    },
    {
      "action": "update",
      "who": "every player asked in the previous step",
      "answer": null,
      "effect": "On Call: called = true, chips -= (high_bet - bet) and pot += (high_bet - bet); the cost is 0 if bet = high_bet. On Fold: folded = true, and nothing put in this hand is returned. Then caller_count = the number of players with called = true, and best_value = the highest card_value among players with called = true (0 if there are none)."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "SHOWDOWN: if caller_count >= 1, the player with called = true and card_value = best_value gets chips += pot, and then pot = 0. If caller_count = 0, pot is unchanged and carries over. Every player who was dealt a card gets shown_card = card. Then hand_number += 1."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "All cards (shown_card), the callers, the winner of the pot (or that it carried over), the pot and everyone's chips are announced."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "The game ends if hand_number >= 16 or the number of players with active = true is 1 or fewer. Any remaining pot is discarded."
    }
  ],
  "ending": {
    "condition": "hand_number >= 16 or (count of players with active = true) <= 1",
    "rank_by": "you.chips",
    "decided_by": "Each player's standing is their chips at the end. Eliminated players count with the chips they held when eliminated. The most chips wins, and players tied for the most share a draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the match starts, then each player has 40 chips, the pot is 0 and hand_number is 0."
    },
    {
      "id": "R2",
      "text": "When a hand begins and an active player has fewer than 4 chips, then that player becomes inactive, takes no further part, and keeps those chips as their final total."
    },
    {
      "id": "R3",
      "text": "When a hand begins and an active player has 4 or more chips, then that player stays active."
    },
    {
      "id": "R4",
      "text": "When a hand is dealt, then the deck is refilled to 52 cards and each active player receives exactly one card, removed from the deck."
    },
    {
      "id": "R5",
      "text": "When cards are dealt, then each player can see the card of every other active player but never their own."
    },
    {
      "id": "R6",
      "text": "When cards are compared, then rank decides first (A high, 2 low) and suit breaks ties (Spades > Hearts > Diamonds > Clubs), so the A of Spades is strongest and the 2 of Clubs weakest."
    },
    {
      "id": "R7",
      "text": "When the ante is taken, then each active player loses 1 chip and the pot grows by 1 per active player."
    },
    {
      "id": "R8",
      "text": "When talk happens, then every active player submits one message of at most 40 words simultaneously, and all messages are then shown to everyone."
    },
    {
      "id": "R9",
      "text": "When a player chooses Bet k (k = 1, 2 or 3) in the first bet, then their chips fall by k and the pot rises by k immediately."
    },
    {
      "id": "R10",
      "text": "When a player folds in the first bet, then they are out of the hand, have lost only the 1-chip ante, and are not asked to call."
    },
    {
      "id": "R11",
      "text": "When all first bets are in, then every choice is revealed to everyone and H is the highest bet made."
    },
    {
      "id": "R12",
      "text": "When a player who bet b calls, then they pay H - b chips into the pot, which is 0 if b = H."
    },
    {
      "id": "R13",
      "text": "When a player who bet folds at the call step, then they forfeit everything they put in this hand and nothing is returned."
    },
    {
      "id": "R14",
      "text": "When two or more players call, then the caller with the highest card strength wins the whole pot and the pot becomes 0."
    },
    {
      "id": "R15",
      "text": "When exactly one player calls, then that player wins the whole pot without comparison and the pot becomes 0."
    },
    {
      "id": "R16",
      "text": "When no player calls (including when everyone folded in the first bet), then the pot stays and carries over to the next hand."
    },
    {
      "id": "R17",
      "text": "When the showdown ends, then every dealt card is revealed to everyone."
    },
    {
      "id": "R18",
      "text": "When 16 hands have been completed, then the match ends and any remaining pot is discarded."
    },
    {
      "id": "R19",
      "text": "When only one or no player is active, then the match ends early and any remaining pot is discarded."
    },
    {
      "id": "R20",
      "text": "When the match ends, then the player with the most chips wins, eliminated players count with their chips at elimination, and players tied for the most share a draw."
    }
  ],
  "offers": [
    {
      "question": "TALK message",
      "who": "every active player",
      "options": "free text of at most 40 words. Eliminated players are not asked."
    },
    {
      "question": "FIRST BET",
      "who": "every active player",
      "options": "Fold, Bet 1, Bet 2, Bet 3 (every active player has at least 3 chips after the ante, so all four are always affordable). Eliminated players are not asked."
    },
    {
      "question": "CALL OR FOLD",
      "who": "every active player whose step-5 bet was 1, 2 or 3",
      "options": "Call, Fold. Players who folded in step 5 and eliminated players are not asked."
    }
  ],
  "choices": [
    {
      "what": "4 to 6 players, suggested 4",
      "why": "Kept from the source and the designer. Four is the smallest table where several opponents' cards give real information about your own and where there are rivals to bluff. Above 6, each player's card information and message get lost in a long conversation."
    },
    {
      "what": "Talk kept as a simultaneous poll broadcast to all",
      "why": "The rules require simultaneous messages. Talk earns its place: each player knows facts the others need (their cards) and has reason to lie about them, so following a claim can cost chips."
    },
    {
      "what": "Card strength encoded as a number from 1 to 52 (rank_index*4 + suit_index)",
      "why": "This lets the showdown winner be found by arithmetic (the highest card_value among callers) and exactly matches the rank-then-suit order in the rules."
    },
    {
      "what": "Eligibility check and early-end check placed at the start of each round, with a further end check after the showdown",
      "why": "Elimination happens at the start of a hand. Checking right after it stops a hand being played with a single active player."
    },
    {
      "what": "Strategy at the table",
      "why": "A thoughtful player infers their own card from the others' cards, their messages and their bets, and decides when to bluff, mislead others about their cards, or fold cheaply. A thoughtless player bets blindly."
    }
  ],
  "simplifications": [
    {
      "what": "Shuffling the full deck each hand is done by resetting the deck list to 52 cards and drawing at random",
      "why": "The engine has no shuffle; drawing at random from a full list is equivalent."
    },
    {
      "what": "The discarded leftover pot is simply ignored at the end",
      "why": "It does not affect anyone's chips or the ranking."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: chips, active, shown_card; table: pot, hand_number.
````

## Reply

````
```json
[
  {"name": "Match starts with 40 chips each, pot 0, hand_number 0", "rule": "R1", "players": 4, "rounds": 0, "seed": 1, "default": "decline",
   "rules": [],
   "expect": {"players": {"1": {"chips": 40, "active": true}, "2": {"chips": 40, "active": true}, "3": {"chips": 40, "active": true}, "4": {"chips": 40, "active": true}},
              "game": {"pot": 0, "hand_number": 0}}},

  {"name": "Player starting a hand with 3 chips is eliminated and keeps 3", "rule": "R2", "players": 4, "rounds": 1, "seed": 1, "default": "decline",
   "given": {"players": {"4": {"chips": 3}}},
   "rules": [],
   "expect": {"players": {"4": {"chips": 3, "active": false, "shown_card": ""}, "1": {"chips": 39, "active": true}, "2": {"chips": 39}, "3": {"chips": 39}},
              "game": {"pot": 3, "hand_number": 1},
              "not_offered": [{"seat": 4, "option": "Bet 1"}, {"seat": 4, "option": "Fold"}]}},

  {"name": "Player with exactly 4 chips stays active and plays the hand", "rule": "R3", "players": 4, "rounds": 1, "seed": 1, "default": "decline",
   "given": {"players": {"1": {"chips": 4}}},
   "rules": [],
   "expect": {"players": {"1": {"chips": 3, "active": true}, "2": {"chips": 39}},
              "game": {"pot": 4, "hand_number": 1},
              "offered": [{"seat": 1, "option": "Bet 1"}]}},

  {"name": "Deal removes one card per active player from a 52-card deck", "rule": "R4", "players": 4, "rounds": 1, "seed": 2, "default": "decline",
   "rules": [],
   "expect": {"lens": {"game": {"deck": 48}}, "game": {"hand_number": 1}}},

  {"name": "Deal with one eliminated seat removes only 3 cards (chance: card identities not asserted)", "rule": "R4", "players": 4, "rounds": 1, "seed": 3, "default": "decline",
   "given": {"players": {"2": {"chips": 2}}},
   "rules": [],
   "expect": {"lens": {"game": {"deck": 49}}, "players": {"2": {"active": false, "chips": 2, "shown_card": ""}}}},

  {"name": "No card is shown to anyone before any deal and showdown", "rule": "R5", "players": 4, "rounds": 0, "seed": 1, "default": "decline",
   "rules": [],
   "expect": {"players": {"1": {"shown_card": ""}, "2": {"shown_card": ""}, "3": {"shown_card": ""}, "4": {"shown_card": ""}},
              "lens": {"game": {"deck": 52}}}},

  {"name": "Three callers: one of them takes the pot of 7, pot becomes 0 (chance decides who)", "rule": "R6", "players": 4, "rounds": 1, "seed": 4, "default": "decline",
   "rules": [{"seat": 1, "options_include": "Bet 1"}, {"seat": 2, "options_include": "Bet 1"}, {"seat": 3, "options_include": "Bet 1"},
             {"seat": 1, "options_include": "Call"}, {"seat": 2, "options_include": "Call"}, {"seat": 3, "options_include": "Call"}],
   "expect": {"players": {"4": {"chips": 39}}, "game": {"pot": 0, "hand_number": 1}}},

  {"name": "Ante takes 1 from each active player and adds 4 to the pot", "rule": "R7", "players": 4, "rounds": 1, "seed": 1, "default": "decline",
   "given": {"game": {"pot": 5}},
   "rules": [],
   "expect": {"players": {"1": {"chips": 39}, "2": {"chips": 39}, "3": {"chips": 39}, "4": {"chips": 39}}, "game": {"pot": 9}}},

  {"name": "Talk round passes without changing chips; eliminated seat is not asked to act", "rule": "R8", "players": 4, "rounds": 1, "seed": 1, "default": "decline",
   "given": {"players": {"3": {"chips": 1}}},
   "rules": [],
   "expect": {"players": {"1": {"chips": 39}, "2": {"chips": 39}, "3": {"chips": 1, "active": false}, "4": {"chips": 39}},
              "game": {"pot": 3, "hand_number": 1},
              "not_offered": [{"seat": 3, "option": "Bet 1"}]}},

  {"name": "Bet 3 costs 3 chips and adds 3 to the pot", "rule": "R9", "players": 4, "rounds": 1, "seed": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "Bet 3"}],
   "expect": {"players": {"1": {"chips": 36}, "2": {"chips": 39}, "3": {"chips": 39}, "4": {"chips": 39}}, "game": {"pot": 7},
              "offered": [{"seat": 1, "option": "Call"}]}},

  {"name": "Folding in the first bet loses only the ante and gives no call question", "rule": "R10", "players": 4, "rounds": 1, "seed": 1, "default": "decline",
   "rules": [{"seat": 2, "options_include": "Bet 1"}, {"seat": 2, "options_include": "Call"}],
   "expect": {"players": {"1": {"chips": 39}, "2": {"chips": 43}, "3": {"chips": 39}, "4": {"chips": 39}}, "game": {"pot": 0},
              "not_offered": [{"seat": 1, "option": "Call"}, {"seat": 3, "option": "Call"}, {"seat": 4, "option": "Call"}]}},

  {"name": "H is the highest bet: bettor of 1 calls against a bet of 2 and pays 1 more", "rule": "R11", "players": 4, "rounds": 1, "seed": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "Bet 1"}, {"seat": 2, "options_include": "Bet 2"}, {"seat": 1, "options_include": "Call"}],
   "expect": {"players": {"1": {"chips": 45}, "2": {"chips": 37}, "3": {"chips": 39}, "4": {"chips": 39}}, "game": {"pot": 0},
              "offered": [{"seat": 2, "option": "Call"}]}},

  {"name": "Caller who bet H pays nothing more to call", "rule": "R12", "players": 4, "rounds": 1, "seed": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "Bet 3"}, {"seat": 2, "options_include": "Bet 1"}, {"seat": 1, "options_include": "Call"}],
   "expect": {"players": {"1": {"chips": 44}, "2": {"chips": 38}, "3": {"chips": 39}, "4": {"chips": 39}}, "game": {"pot": 0}}},

  {"name": "Caller who bet 1 against H=3 pays 2 more and wins the pot alone", "rule": "R12", "players": 4, "rounds": 1, "seed": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "Bet 1"}, {"seat": 2, "options_include": "Bet 3"}, {"seat": 1, "options_include": "Call"}],
   "expect": {"players": {"1": {"chips": 46}, "2": {"chips": 36}, "3": {"chips": 39}, "4": {"chips": 39}}, "game": {"pot": 0}}},

  {"name": "Bettor folding at the call step forfeits ante and bet", "rule": "R13", "players": 4, "rounds": 1, "seed": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "Bet 1"}, {"seat": 2, "options_include": "Bet 3"}, {"seat": 2, "options_include": "Call"}],
   "expect": {"players": {"1": {"chips": 38}, "2": {"chips": 44}, "3": {"chips": 39}, "4": {"chips": 39}}, "game": {"pot": 0}}},

  {"name": "Two callers: the pot of 8 goes to one of them and becomes 0 (chance decides who)", "rule": "R14", "players": 4, "rounds": 1, "seed": 5, "default": "decline",
   "rules": [{"seat": 1, "options_include": "Bet 2"}, {"seat": 2, "options_include": "Bet 2"},
             {"seat": 1, "options_include": "Call"}, {"seat": 2, "options_include": "Call"}],
   "expect": {"players": {"3": {"chips": 39}, "4": {"chips": 39}}, "game": {"pot": 0}}},

  {"name": "Sole caller wins the whole pot", "rule": "R15", "players": 4, "rounds": 1, "seed": 1, "default": "decline",
   "given": {"game": {"pot": 2}},
   "rules": [{"seat": 1, "options_include": "Bet 3"}, {"seat": 1, "options_include": "Call"}],
   "expect": {"players": {"1": {"chips": 45}, "2": {"chips": 39}, "3": {"chips": 39}, "4": {"chips": 39}}, "game": {"pot": 0}}},

  {"name": "Everyone folds: pot carries over", "rule": "R16", "players": 4, "rounds": 1, "seed": 1, "default": "decline",
   "given": {"game": {"pot": 6}},
   "rules": [],
   "expect": {"players": {"1": {"chips": 39}, "2": {"chips": 39}, "3": {"chips": 39}, "4": {"chips": 39}}, "game": {"pot": 10, "hand_number": 1},
              "not_offered": [{"seat": 1, "option": "Call"}]}},

  {"name": "Only bettor folds at call step: pot carries over", "rule": "R16", "players": 4, "rounds": 1, "seed": 1, "default": "decline",
   "rules": [{"seat": 3, "options_include": "Bet 2"}],
   "expect": {"players": {"3": {"chips": 37}}, "game": {"pot": 6, "hand_number": 1}}},

  {"name": "Showdown reveals only dealt cards: eliminated seat shows none", "rule": "R17", "players": 4, "rounds": 1, "seed": 1, "default": "decline",
   "given": {"players": {"4": {"chips": 2}}},
   "rules": [],
   "expect": {"players": {"4": {"shown_card": "", "active": false}}, "game": {"hand_number": 1}}},

  {"name": "Match ends after hand 16; most chips wins", "rule": "R18", "players": 4, "seed": 1, "default": "decline",
   "given": {"players": {"2": {"chips": 45}}, "game": {"hand_number": 15}},
   "rules": [{"seat": 1, "options_include": "Bet 1"}, {"seat": 1, "options_include": "Call"}],
   "expect": {"winner": 2, "standings": {"1": 43, "2": 44, "3": 39, "4": 39},
              "game": {"hand_number": 16}}},

  {"name": "Only one active player after eligibility: match ends at once", "rule": "R19", "players": 4, "seed": 1, "default": "decline",
   "given": {"players": {"2": {"chips": 3}, "3": {"chips": 3}, "4": {"chips": 2}}},
   "rules": [],
   "expect": {"winner": 1, "standings": {"1": 40, "2": 3, "3": 3, "4": 2},
              "players": {"2": {"active": false}, "3": {"active": false}, "4": {"active": false}},
              "game": {"hand_number": 0},
              "not_offered": [{"seat": 1, "option": "Bet 1"}]}},

  {"name": "Eliminated player counts with frozen chips and can win", "rule": "R20", "players": 4, "seed": 1, "default": "decline",
   "given": {"players": {"4": {"chips": 50, "active": false}}, "game": {"hand_number": 15}},
   "rules": [],
   "expect": {"winner": 4, "standings": {"1": 39, "2": 39, "3": 39, "4": 50}}},

  {"name": "Players tied for most chips share the win", "rule": "R20", "players": 4, "seed": 1, "default": "decline",
   "given": {"game": {"hand_number": 15}},
   "rules": [],
   "expect": {"winner": [1, 2, 3, 4], "standings": {"1": 39, "2": 39, "3": 39, "4": 39}}}
]
```
````
