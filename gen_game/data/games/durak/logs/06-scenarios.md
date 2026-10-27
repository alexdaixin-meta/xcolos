# 06 scenarios

- time: 2026-10-27T21:13:52+00:00 (75.2s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 a406170a098c0e32, reply sha256 834e82451439fb3e

## Sent

````
SPEC:
{
  "name": "Offered-Trump Duel Durak",
  "summary": "Two-player Durak over 4 deals of up to 10 bouts each. The first attacker offers two suits and the defender picks one as trump. The player left holding cards takes penalty points, and the lower total penalty wins.",
  "players": {
    "min": 2,
    "max": 2,
    "suggested": 2
  },
  "parameters": {
    "deck_size": 36,
    "suits": 4,
    "ranks_per_suit": 9,
    "lowest_rank": 6,
    "highest_rank": 14,
    "hand_size_dealt": 8,
    "cards_set_aside": 20,
    "deals": 4,
    "max_bouts_per_deal": 10,
    "max_rounds_total": 40,
    "min_attack_cards": 1,
    "max_attack_cards": 3,
    "suits_offered": 2,
    "suit_code_clubs": 1,
    "suit_code_diamonds": 2,
    "suit_code_hearts": 3,
    "suit_code_spades": 4
  },
  "attributes": {
    "player": [
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "Card codes in the player's hand. A code is rank*10+suit code, e.g. 61 = 6 of Clubs, 144 = Ace of Spades.",
        "observable": false
      },
      {
        "key": "hand_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of cards in hand, announced after each bout",
        "observable": true
      },
      {
        "key": "penalty",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Total penalty points (lower is better)",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "The 36 card codes, refilled and shuffled at the start of each deal; the 20 cards left after dealing stay here, set aside and unused",
        "observable": false
      },
      {
        "key": "deal_number",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Current deal, 1 to 4; becomes 5 when deal 4 has ended",
        "observable": true
      },
      {
        "key": "bout_counter",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Bouts played in the current deal",
        "observable": true
      },
      {
        "key": "round_number",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Total bouts played in the game",
        "observable": false
      },
      {
        "key": "attacker_seat",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Seat that attacks this bout; the other seat defends",
        "observable": false
      },
      {
        "key": "offer",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "The two suits offered as trump this deal",
        "observable": false
      },
      {
        "key": "trump",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Trump suit for the current deal",
        "observable": true
      },
      {
        "key": "attack_cards",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Cards placed in the current attack",
        "observable": false
      },
      {
        "key": "defence_cards",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Cards played in defence, each paired with an attack card",
        "observable": false
      },
      {
        "key": "defence_ok",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "Whether this bout's defence succeeded",
        "observable": false
      },
      {
        "key": "discard",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Face-up discarded cards, out of play for the deal",
        "observable": false
      }
    ]
  },
  "setup": [
    "Each seat's penalty is set to 0.",
    "deal_number is set to 1, bout_counter to 0, round_number to 0 and attacker_seat to 1."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "when": "bout_counter == 0",
      "effect": "Start of a deal (S1). Set deck to all 36 card codes, empty both hands and clear discard, offer and trump. Draw 8 cards at random from deck into each seat's hand, removing each from deck. The 20 cards left in deck are set aside, unused. Set hand_count = 8 for each seat. Set attacker_seat = 1 if deal_number is 1 or 3, and 2 if deal_number is 2 or 4."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "when": "bout_counter == 0",
      "effect": "Each seat privately sees its own hand."
    },
    {
      "action": "ask",
      "who": "the seat in attacker_seat (first attacker)",
      "answer": "one pair of two different suits: Clubs+Diamonds, Clubs+Hearts, Clubs+Spades, Diamonds+Hearts, Diamonds+Spades, Hearts+Spades",
      "when": "bout_counter == 0",
      "effect": "Set offer to the two named suits (S2). If the answer is not two different suits, set offer = [Hearts, Spades]. Announce the offer to both seats."
    },
    {
      "action": "ask",
      "who": "the seat not in attacker_seat (first defender)",
      "answer": "one of the two suits in offer",
      "when": "bout_counter == 0",
      "effect": "Set trump to the chosen suit (S3). If the answer is not in offer, set trump to the first suit in offer. Announce trump."
    },
    {
      "action": "ask",
      "who": "the seat in attacker_seat",
      "answer": "short text: 1 to 3 card codes from your hand, all of the same rank",
      "effect": "Set attack_cards to the named cards and remove them from the attacker's hand. If any card is not in hand, the ranks differ, or there are more cards than 3 or than the defender's hand_count, use instead the single card with the minimum code in the attacker's hand. Announce attack_cards.",
      "judged": "Every card the attacker named is in the attacker's hand, all named cards share one rank, and there are between 1 and 3 of them, no more than the defender's hand_count."
    },
    {
      "action": "ask",
      "who": "the seat not in attacker_seat (defender)",
      "answer": "short text: TAKE, or one pairing per attack card in the form 'defence card beats attack card'",
      "effect": "If judged true, set defence_ok = true, set defence_cards to the named defence cards and remove them from the defender's hand. Otherwise set defence_ok = false and defence_cards = [] (counts as TAKE).",
      "judged": "The defender named exactly one different card from the defender's own hand for each card in attack_cards, and each named card beats its paired attack card: it is the same suit and of higher rank, or it is of the trump suit while the attack card is not."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "RESOLVE. If defence_ok: append attack_cards and defence_cards to discard, and switch attacker_seat to the other seat. If not defence_ok: append attack_cards to the defender's hand, and attacker_seat stays the same. Recompute hand_count for both seats. Clear attack_cards and defence_cards. Add 1 to bout_counter and 1 to round_number. Announce the cards played, the result, and both hand_count values."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "when": "any seat has hand_count == 0 or bout_counter >= 10 or round_number >= 40",
      "effect": "END OF DEAL. If exactly one seat has hand_count 0, the other seat adds its hand_count to penalty. If both have 0, nobody scores. If both hold cards, the seat with the larger hand_count adds (larger hand_count - smaller hand_count) to penalty; equal hands score nothing. Then add 1 to deal_number and set bout_counter = 0. Announce both penalty totals."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if deal_number > 4 or round_number >= 40; otherwise continue."
    }
  ],
  "ending": {
    "condition": "deal_number > 4 or round_number >= 40",
    "rank_by": "0 - you.penalty",
    "decided_by": "Each player's standing is their total penalty, and the lower total wins. If the two totals are equal, both share the top spot, which is the draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "The deck has 36 cards: suits Clubs, Diamonds, Hearts, Spades, each with ranks 6, 7, 8, 9, 10, 11 (J), 12 (Q), 13 (K) and 14 (A)."
    },
    {
      "id": "R2",
      "text": "When a deal starts (bout_counter is 0), all 36 cards are shuffled, each player receives 8 cards in hand, and the remaining 20 stay set aside, unused."
    },
    {
      "id": "R3",
      "text": "When deal 1 or 3 starts, seat 1 is the first attacker; when deal 2 or 4 starts, seat 2 is the first attacker."
    },
    {
      "id": "R4",
      "text": "When a deal starts, the first attacker names two different suits as the offer; if the answer is not two different suits, the offer is Hearts and Spades."
    },
    {
      "id": "R5",
      "text": "When the offer is made, the first defender picks one offered suit as trump for the whole deal; if the answer is not an offered suit, the first offered suit becomes trump."
    },
    {
      "id": "R6",
      "text": "Card X beats card Y only when X is the same suit as Y and of higher rank, or when X is trump and Y is not."
    },
    {
      "id": "R7",
      "text": "When attacking, the attacker places 1 to 3 cards of the same rank from hand, and never more cards than the defender holds."
    },
    {
      "id": "R8",
      "text": "When an attack is illegal (a card not in hand, mixed ranks, or too many cards), it is replaced by the attacker's single lowest-ranked card, with ties going to the earliest suit in the order Clubs, Diamonds, Hearts, Spades."
    },
    {
      "id": "R9",
      "text": "When defending, the defender says TAKE or names one different card from hand for each attack card that legally beats it; any illegal or incomplete defence counts as TAKE."
    },
    {
      "id": "R10",
      "text": "When the defence succeeds, all attack and defence cards are discarded, and the defender becomes the attacker for the next bout."
    },
    {
      "id": "R11",
      "text": "When the defender takes, the attack cards go into the defender's hand, and the same player attacks again next bout."
    },
    {
      "id": "R12",
      "text": "When a bout resolves, the cards played, the result and both hand sizes are announced, and bout_counter rises by 1."
    },
    {
      "id": "R13",
      "text": "When a bout resolves with either player at 0 cards or bout_counter at 10, the deal ends."
    },
    {
      "id": "R14",
      "text": "When a deal ends with exactly one player at 0 cards, the other player adds their hand size to their penalty (e.g. holding 5 cards adds 5)."
    },
    {
      "id": "R15",
      "text": "When a deal ends with both players at 0 cards, nobody's penalty changes."
    },
    {
      "id": "R16",
      "text": "When a deal ends at 10 bouts with both holding cards, the player with more cards adds the difference to their penalty (e.g. 7 vs 3 adds 4); equal hands add nothing."
    },
    {
      "id": "R17",
      "text": "When round 40 finishes during a deal, that deal is scored as if it had reached its 10-bout cap."
    },
    {
      "id": "R18",
      "text": "When deal 4 has ended, the game ends: the player with the lower total penalty wins, and equal totals are a draw."
    }
  ],
  "offers": [
    {
      "question": "OFFER (first bout of a deal)",
      "who": "the first attacker",
      "options": "one of the six pairs of two different suits: Clubs+Diamonds, Clubs+Hearts, Clubs+Spades, Diamonds+Hearts, Diamonds+Spades, Hearts+Spades"
    },
    {
      "question": "CHOICE (first bout of a deal)",
      "who": "the first defender",
      "options": "either of the two suits in the offer, and no other"
    },
    {
      "question": "ATTACK",
      "who": "the attacker",
      "options": "free text naming 1 to 3 cards of one rank from their own hand, no more than the defender's hand_count"
    },
    {
      "question": "DEFENCE",
      "who": "the defender",
      "options": "TAKE, or free text pairing one different card from their own hand with each attack card"
    }
  ],
  "choices": [
    {
      "what": "Exactly 2 players (min 2, max 2, suggested 2)",
      "why": "The designer fixed the game as a duel: the offer-and-choose trump mechanic and the attacker/defender alternation are defined only between two seats."
    },
    {
      "what": "No talk step before choices",
      "why": "The rules have no talk, and in a zero-sum duel talk would only add words."
    },
    {
      "what": "Cards encoded as rank*10 + suit code (Clubs 1, Diamonds 2, Hearts 3, Spades 4)",
      "why": "The minimum code in a hand is then exactly the lowest-ranked card with ties broken by suit order, so the illegal-attack fallback is pure arithmetic."
    },
    {
      "what": "The offer is asked as a choice among the six suit pairs",
      "why": "Every reply is then two different suits; the Hearts and Spades fallback is kept in the effect for completeness."
    },
    {
      "what": "The 20 set-aside cards stay in the hidden deck list",
      "why": "They are unused for the deal; keeping them in the deck is equivalent to setting them aside face down."
    },
    {
      "what": "Strategy at the table",
      "why": "The first attacker offers two suits they hold strength in, or that the opponent likely lacks. The chooser picks the one that helps their own hand. Attackers lead ranks the defender probably cannot beat, and defenders weigh taking against spending their trumps."
    }
  ],
  "simplifications": [
    {
      "what": "Attack legality and defence legality are judged by a referee from one sentence each",
      "why": "Parsing free-text card lists and matching each defence card to an attack card is too complex for plain arithmetic. The effects of each ruling (moving cards, scoring) are still calculated."
    },
    {
      "what": "Deal-start steps run inside the round, each carrying the condition bout_counter == 0",
      "why": "The engine repeats one flat round. Per-step conditions reproduce 'only in the first bout of a deal' without choosing between blocks of steps."
    },
    {
      "what": "A draw is shown as both players sharing the win",
      "why": "The engine ranks by one expression, and players level at the top share the win; this is equivalent to the source's draw."
    },
    {
      "what": "The 40-round cap and the 4-deal end are both checked",
      "why": "With at most 10 bouts per deal over 4 deals, round 40 can only fall at the end of deal 4, so the cap is kept as a safeguard."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: hand_count, penalty; table: deal_number, bout_counter, trump.
````

## Reply

````
```json
[
  {
    "name": "First round of a fresh game: 8 cards each, 20 set aside, defaults give Clubs trump and a take",
    "rule": "R2",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "rules": [],
    "expect": {
      "lens": {"game": {"deck": 20}},
      "players": {"1": {"hand_count": 7, "penalty": 0}, "2": {"hand_count": 9, "penalty": 0}},
      "game": {"deal_number": 1, "bout_counter": 1, "trump": "Clubs"}
    }
  },
  {
    "name": "Fresh deal deals all 36 codes: 8 in each hand, 20 left in the deck",
    "rule": "R1",
    "players": 2,
    "seed": 2,
    "rounds": 1,
    "default": "first",
    "rules": [],
    "expect": {
      "lens": {"game": {"deck": 20}},
      "game": {"deal_number": 1, "bout_counter": 1}
    }
  },
  {
    "name": "Deal 2 starts with seat 2 as first attacker making the offer",
    "rule": "R3",
    "players": 2,
    "seed": 3,
    "rounds": 1,
    "given": {
      "game": {"deal_number": 2, "bout_counter": 0, "round_number": 10, "attacker_seat": 1}
    },
    "rules": [
      {"seat": 2, "options_include": "Hearts+Spades"},
      {"seat": 1, "options_include": "Spades"}
    ],
    "expect": {
      "players": {"1": {"hand_count": 9}, "2": {"hand_count": 7}},
      "game": {"deal_number": 2, "bout_counter": 1, "trump": "Spades"},
      "offered": [{"seat": 2, "option": "Hearts+Spades"}, {"seat": 1, "option": "Spades"}],
      "not_offered": [{"seat": 1, "option": "Hearts+Spades"}, {"seat": 2, "option": "Spades"}]
    }
  },
  {
    "name": "First attacker offers Diamonds+Spades and the defender may only pick one of those",
    "rule": "R4",
    "players": 2,
    "seed": 4,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": "Diamonds+Spades"},
      {"seat": 2, "options_include": "Diamonds"}
    ],
    "expect": {
      "game": {"trump": "Diamonds", "deal_number": 1, "bout_counter": 1},
      "offered": [{"seat": 1, "option": "Diamonds+Spades"}, {"seat": 2, "option": "Spades"}],
      "not_offered": [{"seat": 2, "option": "Clubs"}, {"seat": 2, "option": "Hearts"}, {"seat": 2, "option": "Diamonds+Spades"}]
    }
  },
  {
    "name": "First defender picks the second offered suit as trump",
    "rule": "R5",
    "players": 2,
    "seed": 5,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": "Clubs+Hearts"},
      {"seat": 2, "options_include": "Hearts"}
    ],
    "expect": {
      "game": {"trump": "Hearts"},
      "offered": [{"seat": 2, "option": "Clubs"}],
      "not_offered": [{"seat": 2, "option": "Spades"}, {"seat": 2, "option": "Diamonds"}]
    }
  },
  {
    "name": "A defence card that beats the attack card discards both cards",
    "rule": "R6",
    "players": 2,
    "seed": 6,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [61, 72, 83], "hand_count": 3}, "2": {"hand": [94, 104, 114], "hand_count": 3}},
      "game": {"deal_number": 1, "bout_counter": 3, "round_number": 3, "attacker_seat": 1, "offer": ["Hearts", "Spades"], "trump": "Spades"}
    },
    "judge": {"The defender named exactly one different card": true},
    "rules": [],
    "expect": {
      "players": {"1": {"hand_count": 2, "penalty": 0}, "2": {"hand_count": 2, "penalty": 0}},
      "game": {"bout_counter": 4, "trump": "Spades"}
    }
  },
  {
    "name": "An attack with too many cards for the defender becomes a single card",
    "rule": "R7",
    "players": 2,
    "seed": 7,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [61, 62, 63], "hand_count": 3}, "2": {"hand": [94], "hand_count": 1}},
      "game": {"deal_number": 1, "bout_counter": 3, "round_number": 3, "attacker_seat": 1, "offer": ["Hearts", "Spades"], "trump": "Spades"}
    },
    "rules": [],
    "expect": {
      "players": {"1": {"hand_count": 2}, "2": {"hand_count": 2}},
      "game": {"bout_counter": 4}
    }
  },
  {
    "name": "An illegal attack is replaced by one card, which the defender takes",
    "rule": "R8",
    "players": 2,
    "seed": 8,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [61, 72, 83, 131], "hand_count": 4}, "2": {"hand": [94, 104, 114], "hand_count": 3}},
      "game": {"deal_number": 1, "bout_counter": 2, "round_number": 2, "attacker_seat": 1, "offer": ["Hearts", "Spades"], "trump": "Hearts"}
    },
    "judge": {"Every card the attacker named is in the attacker's hand": false},
    "rules": [],
    "expect": {
      "players": {"1": {"hand_count": 3}, "2": {"hand_count": 4}},
      "game": {"bout_counter": 3}
    }
  },
  {
    "name": "An illegal defence counts as TAKE",
    "rule": "R9",
    "players": 2,
    "seed": 9,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [61, 72, 83], "hand_count": 3}, "2": {"hand": [94, 104, 114], "hand_count": 3}},
      "game": {"deal_number": 1, "bout_counter": 3, "round_number": 3, "attacker_seat": 1, "offer": ["Hearts", "Spades"], "trump": "Spades"}
    },
    "judge": {"The defender named exactly one different card": false},
    "rules": [],
    "expect": {
      "players": {"1": {"hand_count": 2}, "2": {"hand_count": 4}},
      "game": {"bout_counter": 4}
    }
  },
  {
    "name": "A successful defence discards the attack and defence cards",
    "rule": "R10",
    "players": 2,
    "seed": 10,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [61, 72, 83, 92], "hand_count": 4}, "2": {"hand": [94, 104, 114], "hand_count": 3}},
      "game": {"deal_number": 1, "bout_counter": 4, "round_number": 4, "attacker_seat": 1, "offer": ["Hearts", "Spades"], "trump": "Spades"}
    },
    "judge": {"The defender named exactly one different card": true},
    "rules": [],
    "expect": {
      "players": {"1": {"hand_count": 3, "penalty": 0}, "2": {"hand_count": 2, "penalty": 0}},
      "game": {"bout_counter": 5}
    }
  },
  {
    "name": "When the defender takes, the attack card goes into the defender's hand",
    "rule": "R11",
    "players": 2,
    "seed": 11,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [61, 72, 83], "hand_count": 3}, "2": {"hand": [94, 104, 114], "hand_count": 3}},
      "game": {"deal_number": 1, "bout_counter": 3, "round_number": 3, "attacker_seat": 1, "offer": ["Hearts", "Spades"], "trump": "Spades"}
    },
    "rules": [],
    "expect": {
      "players": {"1": {"hand_count": 2, "penalty": 0}, "2": {"hand_count": 4, "penalty": 0}},
      "game": {"bout_counter": 4, "deal_number": 1}
    }
  },
  {
    "name": "Resolving a bout raises bout_counter by 1 and updates both hand counts",
    "rule": "R12",
    "players": 2,
    "seed": 12,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [61, 72, 83, 93, 101], "hand_count": 5}, "2": {"hand": [94, 104], "hand_count": 2}},
      "game": {"deal_number": 2, "bout_counter": 6, "round_number": 16, "attacker_seat": 1, "offer": ["Clubs", "Spades"], "trump": "Clubs"}
    },
    "rules": [],
    "expect": {
      "players": {"1": {"hand_count": 4}, "2": {"hand_count": 3}},
      "game": {"bout_counter": 7, "deal_number": 2, "trump": "Clubs"}
    }
  },
  {
    "name": "The deal ends when a player reaches 0 cards",
    "rule": "R13",
    "players": 2,
    "seed": 13,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [61], "hand_count": 1}, "2": {"hand": [94, 104, 114], "hand_count": 3}},
      "game": {"deal_number": 1, "bout_counter": 5, "round_number": 5, "attacker_seat": 1, "offer": ["Hearts", "Spades"], "trump": "Spades"}
    },
    "judge": {"The defender named exactly one different card": true},
    "rules": [],
    "expect": {
      "players": {"1": {"penalty": 0}, "2": {"penalty": 2}},
      "game": {"deal_number": 2, "bout_counter": 0}
    }
  },
  {
    "name": "Only one player at 0 cards: the other adds the hand size they hold",
    "rule": "R14",
    "players": 2,
    "seed": 14,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [61], "hand_count": 1, "penalty": 2}, "2": {"hand": [94, 104, 114, 124], "hand_count": 4, "penalty": 1}},
      "game": {"deal_number": 1, "bout_counter": 5, "round_number": 5, "attacker_seat": 1, "offer": ["Hearts", "Spades"], "trump": "Spades"}
    },
    "rules": [],
    "expect": {
      "players": {"1": {"penalty": 2}, "2": {"penalty": 6}},
      "game": {"deal_number": 2, "bout_counter": 0}
    }
  },
  {
    "name": "Both players at 0 cards: no penalty",
    "rule": "R15",
    "players": 2,
    "seed": 15,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [61], "hand_count": 1, "penalty": 3}, "2": {"hand": [74], "hand_count": 1, "penalty": 5}},
      "game": {"deal_number": 2, "bout_counter": 7, "round_number": 17, "attacker_seat": 1, "offer": ["Hearts", "Spades"], "trump": "Spades"}
    },
    "judge": {"The defender named exactly one different card": true},
    "rules": [],
    "expect": {
      "players": {"1": {"penalty": 3}, "2": {"penalty": 5}},
      "game": {"deal_number": 3, "bout_counter": 0}
    }
  },
  {
    "name": "10-bout cap with 4 vs 1 cards: the larger hand adds 3",
    "rule": "R16",
    "players": 2,
    "seed": 16,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [61, 62, 63, 64, 71], "hand_count": 5}, "2": {"hand": [74, 84], "hand_count": 2}},
      "game": {"deal_number": 1, "bout_counter": 9, "round_number": 9, "attacker_seat": 1, "offer": ["Hearts", "Spades"], "trump": "Spades"}
    },
    "judge": {"The defender named exactly one different card": true},
    "rules": [],
    "expect": {
      "players": {"1": {"penalty": 3}, "2": {"penalty": 0}},
      "game": {"deal_number": 2, "bout_counter": 0}
    }
  },
  {
    "name": "10-bout cap with equal hands (3 vs 3): nobody scores",
    "rule": "R16",
    "players": 2,
    "seed": 17,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [61, 62, 63, 64], "hand_count": 4, "penalty": 1}, "2": {"hand": [74, 84], "hand_count": 2, "penalty": 2}},
      "game": {"deal_number": 1, "bout_counter": 9, "round_number": 9, "attacker_seat": 1, "offer": ["Hearts", "Spades"], "trump": "Spades"}
    },
    "rules": [],
    "expect": {
      "players": {"1": {"penalty": 1}, "2": {"penalty": 2}},
      "game": {"deal_number": 2, "bout_counter": 0}
    }
  },
  {
    "name": "Round 40 ends the deal as if capped and ends the game",
    "rule": "R17",
    "players": 2,
    "seed": 18,
    "given": {
      "players": {"1": {"hand": [61, 62, 63, 64], "hand_count": 4, "penalty": 0}, "2": {"hand": [74, 84, 94, 104], "hand_count": 4, "penalty": 0}},
      "game": {"deal_number": 3, "bout_counter": 5, "round_number": 39, "attacker_seat": 1, "offer": ["Hearts", "Spades"], "trump": "Spades"}
    },
    "rules": [],
    "expect": {
      "winner": 1,
      "standings": {"1": 0, "2": -2},
      "players": {"1": {"penalty": 0}, "2": {"penalty": 2}}
    }
  },
  {
    "name": "After deal 4 the lower total penalty wins",
    "rule": "R18",
    "players": 2,
    "seed": 19,
    "given": {
      "players": {"1": {"hand": [61, 62, 63], "hand_count": 3, "penalty": 10}, "2": {"hand": [74, 84, 94], "hand_count": 3, "penalty": 7}},
      "game": {"deal_number": 4, "bout_counter": 9, "round_number": 35, "attacker_seat": 2, "offer": ["Hearts", "Spades"], "trump": "Hearts"}
    },
    "rules": [],
    "expect": {
      "winner": 2,
      "standings": {"1": -12, "2": -7},
      "players": {"1": {"penalty": 12}, "2": {"penalty": 7}},
      "game": {"deal_number": 5}
    }
  },
  {
    "name": "Equal totals after deal 4 are a draw shared by both seats",
    "rule": "R18",
    "players": 2,
    "seed": 20,
    "given": {
      "players": {"1": {"hand": [61, 62, 63], "hand_count": 3, "penalty": 5}, "2": {"hand": [74, 84, 94], "hand_count": 3, "penalty": 5}},
      "game": {"deal_number": 4, "bout_counter": 9, "round_number": 35, "attacker_seat": 2, "offer": ["Hearts", "Spades"], "trump": "Hearts"}
    },
    "judge": {"The defender named exactly one different card": true},
    "rules": [],
    "expect": {
      "winner": [1, 2],
      "standings": {"1": -5, "2": -5},
      "players": {"1": {"penalty": 5}, "2": {"penalty": 5}},
      "game": {"deal_number": 5}
    }
  }
]
```
````
