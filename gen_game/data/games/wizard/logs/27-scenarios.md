# 27 scenarios

- time: 2026-10-27T21:25:33+00:00 (65.0s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 c5dc8d6dc8dfac6e, reply sha256 dd9d87b472105644

## Sent

````
SPEC:
{
  "name": "Wizard Duel of Three",
  "summary": "A three-player trick-taking game of 6 hands of 5 tricks. Players bid how many tricks they will take and score for exact bids, using Wizards, Jesters and a turned trump suit.",
  "players": {
    "min": 3,
    "max": 3,
    "suggested": 3
  },
  "parameters": {
    "num_hands": 6,
    "tricks_per_hand": 5,
    "total_rounds": 30,
    "deck_size": 32,
    "num_suits": 4,
    "max_rank": 7,
    "numbered_cards": 28,
    "num_wizards": 2,
    "num_jesters": 2,
    "hand_size": 5,
    "unused_cards_per_hand": 16,
    "bid_min": 0,
    "bid_max": 5,
    "exact_bid_bonus": 20,
    "exact_bid_per_trick": 10,
    "miss_penalty_per_trick": 10,
    "first_dealer_seat": 1,
    "trick_win_increment": 1
  },
  "attributes": {
    "player": [
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "The cards the player holds this hand, coded as text (R1..R7, B1..B7, G1..G7, Y1..Y7, W1, W2, J1, J2).",
        "observable": false
      },
      {
        "key": "bid",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Tricks bid this hand, revealed after the simultaneous bid.",
        "observable": true
      },
      {
        "key": "tricks_taken",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Tricks won so far this hand.",
        "observable": true
      },
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Running score.",
        "observable": true
      },
      {
        "key": "played_card",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The card this player played to the current trick.",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "The 32-card deck, rebuilt and drawn from at the start of each hand. The cards left in it after the deal are the 16 unused cards.",
        "observable": false
      },
      {
        "key": "trump_card",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The card turned face up after the deal.",
        "observable": true
      },
      {
        "key": "trump_suit",
        "type": "text",
        "visible": "public",
        "initial": "none",
        "meaning": "The suit letter of trump_card if it is numbered, otherwise none.",
        "observable": false
      },
      {
        "key": "led_suit",
        "type": "text",
        "visible": "public",
        "initial": "none",
        "meaning": "The suit of the first numbered card played in the trick, or none.",
        "observable": false
      },
      {
        "key": "trick_cards",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "The cards played to the current trick, in order of play.",
        "observable": false
      },
      {
        "key": "played_history",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Every card played so far this hand.",
        "observable": false
      },
      {
        "key": "dealer",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "The dealer seat for the current hand.",
        "observable": false
      },
      {
        "key": "leader",
        "type": "number",
        "visible": "public",
        "initial": 2,
        "meaning": "The seat that leads the current trick.",
        "observable": false
      },
      {
        "key": "hand_number",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "The current hand, from 1 to 6.",
        "observable": false
      },
      {
        "key": "trick_in_hand",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "The current trick within the hand, from 1 to 5.",
        "observable": false
      },
      {
        "key": "round_number",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "The current trick overall, from 1 to 30.",
        "observable": false
      }
    ]
  },
  "setup": [
    "Seats are 1, 2 and 3.",
    "Every score is 0.",
    "dealer is set to 1, hand_number to 1, trick_in_hand to 1 and round_number to 1.",
    "leader is set to 2, the seat after the dealer."
  ],
  "round": [
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "When trick_in_hand == 1: deck is set to all 32 cards (R1-R7, B1-B7, G1-G7, Y1-Y7, W1, W2, J1, J2). Every hand is emptied and every played_history entry is cleared."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When trick_in_hand == 1: each player draws 5 cards at random from deck into their hand, each card removed from deck as it is drawn."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "When trick_in_hand == 1: one more card is drawn at random from deck into trump_card. trump_suit is set to its suit letter if it is numbered, or to none if it is W or J. The 16 cards left in deck stay hidden and unused this hand."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "When trick_in_hand == 1: announce 'Hand {hand_number}: dealer is seat {dealer}; turned card is {trump_card}; trump is {trump_suit}.'"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When trick_in_hand == 1: every bid and every tricks_taken is set to 0."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "When trick_in_hand == 1: each player is sent their own hand, trump_card and the scores."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "a whole number from 0 to 5",
      "effect": "When trick_in_hand == 1: each player's bid is set to their answer. Nobody sees any bid until all are in."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "When trick_in_hand == 1: one message per player: 'Seat {seat} bids {bid}.'"
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "led_suit is set to none, trick_cards is emptied and every played_card is set to empty."
    },
    {
      "action": "ask",
      "who": "seat leader",
      "answer": "one card from the player's own hand",
      "effect": "The card is removed from the leader's hand and appended to trick_cards and played_history. The leader's played_card is set to it. If the card is numbered, led_suit is set to its suit."
    },
    {
      "action": "ask",
      "who": "seat leader % 3 + 1",
      "answer": "one card from the player's own hand",
      "effect": "The card is removed from the player's hand and appended to trick_cards and played_history. The player's played_card is set to it. If led_suit == none and trick_cards[0] is not a Wizard and the card is numbered, led_suit is set to its suit."
    },
    {
      "action": "ask",
      "who": "seat (leader + 1) % 3 + 1",
      "answer": "one card from the player's own hand",
      "effect": "The card is removed from the player's hand and appended to trick_cards and played_history. The player's played_card is set to it. If led_suit == none and trick_cards[0] is not a Wizard and the card is numbered, led_suit is set to its suit."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "The trick winner is worked out by arithmetic. Each card in trick_cards gets a power by its play position p (0, 1, 2). A Wizard has power 1000 - p. A card of trump_suit has power 200 + rank. A card of led_suit that is not trump has power 100 + rank. Any other numbered card has power 0. A Jester has power 3 - p only if all three cards are Jesters, otherwise 0. The seat that played the card with the highest power wins. That seat's tricks_taken increases by 1, and leader is set to that seat."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce 'Seat {leader} wins trick {trick_in_hand} with cards {trick_cards}; tricks taken now {tricks_taken}.'"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When trick_in_hand == 5: for each player, if tricks_taken == bid then score += 20 + 10 * tricks_taken, otherwise score -= 10 * |bid - tricks_taken|."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "When trick_in_hand == 5: separate messages per player: 'Seat {seat} took {tricks_taken} tricks' and 'Seat {seat} score is now {score}'."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "round_number += 1. If trick_in_hand == 5: hand_number += 1, trick_in_hand is set to 1, dealer is set to dealer % 3 + 1, and leader is set to dealer % 3 + 1 using the new dealer. Otherwise trick_in_hand += 1."
    },
    {
      "action": "check",
      "who": "table",
      "answer": null,
      "effect": "End the game if round_number > 30. Otherwise continue with the next round."
    }
  ],
  "ending": {
    "condition": "round_number > 30",
    "rank_by": "you.score",
    "decided_by": "Each player's final score after 6 hands (30 tricks). The highest score wins, and players tied for the highest score share the win (a draw)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game begins, the deck has 32 cards: four suits (Red, Blue, Green, Yellow) numbered 1 to 7, plus 2 Wizards and 2 Jesters."
    },
    {
      "id": "R2",
      "text": "When the game begins, every score is 0, the dealer is seat 1 and seat 2 leads the first trick."
    },
    {
      "id": "R3",
      "text": "When a hand starts (trick_in_hand == 1), the deck is rebuilt from all 32 cards and each player receives exactly 5 cards in their private hand."
    },
    {
      "id": "R4",
      "text": "When a hand starts, one more card becomes trump_card. If it is numbered, its suit is trump_suit; if it is a Wizard or Jester, trump_suit is none."
    },
    {
      "id": "R5",
      "text": "When a hand starts, 16 cards remain in the deck unused and unseen."
    },
    {
      "id": "R6",
      "text": "When a hand starts, every bid and tricks_taken is reset to 0."
    },
    {
      "id": "R7",
      "text": "When a hand starts, all three players bid simultaneously a whole number from 0 to 5, and the bids need not total 5."
    },
    {
      "id": "R8",
      "text": "When all bids are in, each player's bid is announced in its own message."
    },
    {
      "id": "R9",
      "text": "When a hand starts, the seat after the dealer leads the first trick."
    },
    {
      "id": "R10",
      "text": "When a trick is played, the leader plays first, then the next seat in order (leader % 3 + 1), then the remaining seat."
    },
    {
      "id": "R11",
      "text": "When a player plays, they may play any card in their hand, with no obligation to follow suit, and the card leaves their hand."
    },
    {
      "id": "R12",
      "text": "When the first numbered card of a trick is played and no Wizard was played first, its suit becomes led_suit; a Jester played before it does not set the suit."
    },
    {
      "id": "R13",
      "text": "When a Wizard is the first card of a trick, the trick has no led suit and that Wizard wins."
    },
    {
      "id": "R14",
      "text": "When any Wizard is played in a trick, the first Wizard played wins the trick."
    },
    {
      "id": "R15",
      "text": "When no Wizard is played but a trump is, the highest trump wins the trick."
    },
    {
      "id": "R16",
      "text": "When no Wizard and no trump is played, the highest card of led_suit wins the trick."
    },
    {
      "id": "R17",
      "text": "When all three cards in a trick are Jesters, the first Jester played wins."
    },
    {
      "id": "R18",
      "text": "When a numbered card is neither of led_suit nor trump, it never wins the trick."
    },
    {
      "id": "R19",
      "text": "When a player wins a trick, their tricks_taken increases by 1, this is announced, and they lead the next trick."
    },
    {
      "id": "R20",
      "text": "When a hand ends with tricks_taken equal to bid, the player gains 20 + 10 x tricks_taken (for example, bid 2 and took 2 gives +40; bid 0 and took 0 gives +20)."
    },
    {
      "id": "R21",
      "text": "When a hand ends with tricks_taken not equal to bid, the player loses 10 x |bid - tricks_taken| (for example, bid 3 and took 1 gives -20)."
    },
    {
      "id": "R22",
      "text": "When a hand ends, each player's trick count and new score are announced in separate messages."
    },
    {
      "id": "R23",
      "text": "When a hand ends, the dealer moves to the next seat (1, then 2, then 3, then 1)."
    },
    {
      "id": "R24",
      "text": "When the 30th trick (the end of hand 6) is complete, the game ends."
    },
    {
      "id": "R25",
      "text": "When the game ends, the highest score wins and players tied at the top share the win."
    }
  ],
  "offers": [
    {
      "question": "Bid at the start of a hand",
      "who": "all three seats, simultaneously",
      "options": "any whole number from 0 to 5"
    },
    {
      "question": "Lead card",
      "who": "the seat in leader",
      "options": "every card currently in that seat's hand"
    },
    {
      "question": "Second card",
      "who": "seat leader % 3 + 1",
      "options": "every card currently in that seat's hand, whatever the led suit"
    },
    {
      "question": "Third card",
      "who": "the remaining seat",
      "options": "every card currently in that seat's hand, whatever the led suit"
    }
  ],
  "choices": [
    {
      "what": "3 players (min 3, max 3, suggested 3)",
      "why": "The designer fixed the game at three. The deck arithmetic (15 dealt, 1 turned, 16 unused) and the seat rotation depend on exactly three seats, and a fourth would change the card counts."
    },
    {
      "what": "No talk step",
      "why": "The rules state there is no discussion phase."
    },
    {
      "what": "Cards coded as short text (R5, W1, J2) and the trick winner computed as a power value per card",
      "why": "This turns the trick-winning rules into pure arithmetic: the first Wizard beats everything, then the highest trump, then the highest led-suit card, and an all-Jester trick goes to the first Jester."
    },
    {
      "what": "Strategy at this table",
      "why": "A thoughtful player bids from hand strength and the trump suit, then plays to hit the bid exactly. They dump high cards or Jesters when they have enough tricks, and track played cards and others' bids to judge which cards are still out."
    }
  ],
  "simplifications": [
    {
      "what": "Start-of-hand and end-of-hand steps are ordinary round steps, each carrying a when-condition on trick_in_hand",
      "why": "The step list is flat. Each step is individually conditional on a counter rather than being a separately chosen block, so the game stays faithful."
    },
    {
      "what": "The order of play is addressed by seat expressions relative to leader",
      "why": "The engine asks named seats; leader, leader % 3 + 1 and (leader + 1) % 3 + 1 reproduce seat order starting from the trick winner."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: bid, tricks_taken, score; table: trump_card.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
[
{"name": "Deck of 32: after the first deal and one trick, 16 stay in the deck and each hand holds 4 (cards are random, only counts asserted)", "rule": "R1", "players": 3, "seed": 1, "rounds": 1, "default": "first",
 "expect": {"lens": {"game": {"deck": 16}, "players": {"1": {"hand": 4}, "2": {"hand": 4}, "3": {"hand": 4}}}}},

{"name": "At the start every score is 0", "rule": "R2", "players": 3, "seed": 1, "rounds": 0,
 "expect": {"players": {"1": {"score": 0}, "2": {"score": 0}, "3": {"score": 0}}, "standings": {"1": 0, "2": 0, "3": 0}}},

{"name": "A new hand rebuilds the deck and deals exactly 5 cards to each player, replacing old hands (counts only)", "rule": "R3", "players": 3, "seed": 2, "rounds": 1, "default": "first",
 "given": {"players": {"1": {"hand": ["R1", "R2"]}, "2": {"hand": ["B1", "B2"]}, "3": {"hand": ["G1", "G2"]}}, "game": {"deck": ["Y1", "Y2", "Y3"], "trick_in_hand": 1}},
 "expect": {"lens": {"game": {"deck": 16}, "players": {"1": {"hand": 4}, "2": {"hand": 4}, "3": {"hand": 4}}}}},

{"name": "One more card is turned as trump after the deal, leaving 16 in the deck (the card itself is random)", "rule": "R4", "players": 3, "seed": 3, "rounds": 1, "default": "first",
 "expect": {"lens": {"game": {"deck": 16}}}},

{"name": "16 cards stay unused in the deck after the deal (counts only)", "rule": "R5", "players": 3, "seed": 4, "rounds": 1, "default": "first",
 "expect": {"lens": {"game": {"deck": 16}}}},

{"name": "Bids from a previous hand are reset and replaced by the new bids", "rule": "R6", "players": 3, "seed": 5, "rounds": 1, "default": "first",
 "given": {"players": {"1": {"bid": 4, "tricks_taken": 3}, "2": {"bid": 4, "tricks_taken": 3}, "3": {"bid": 4, "tricks_taken": 3}}, "game": {"trick_in_hand": 1}},
 "rules": [{"seat": 1, "options_include": 1}, {"seat": 2, "options_include": 2}, {"seat": 3, "options_include": 0}],
 "expect": {"players": {"1": {"bid": 1}, "2": {"bid": 2}, "3": {"bid": 0}}}},

{"name": "All three may bid 5 at once; bids need not total 5", "rule": "R7", "players": 3, "seed": 6, "rounds": 1, "default": "first",
 "rules": [{"seat": 1, "options_include": 5}, {"seat": 2, "options_include": 5}, {"seat": 3, "options_include": 5}],
 "expect": {"players": {"1": {"bid": 5}, "2": {"bid": 5}, "3": {"bid": 5}},
            "offered": [{"seat": 1, "option": 0}, {"seat": 2, "option": 5}, {"seat": 3, "option": 0}]}},

{"name": "Each player's bid is recorded and revealed", "rule": "R8", "players": 3, "seed": 7, "rounds": 1, "default": "first",
 "rules": [{"seat": 1, "options_include": 1}, {"seat": 2, "options_include": 2}, {"seat": 3, "options_include": 3}],
 "expect": {"players": {"1": {"bid": 1}, "2": {"bid": 2}, "3": {"bid": 3}}}},

{"name": "After a hand ends a new hand starts with fresh bids (next leader is seat after new dealer; cards random)", "rule": "R9", "players": 3, "seed": 8, "rounds": 2, "default": "first",
 "given": {"players": {"1": {"hand": ["W1"], "bid": 1, "tricks_taken": 0, "score": 0}, "2": {"hand": ["B3"], "bid": 2, "tricks_taken": 2, "score": 0}, "3": {"hand": ["G2"], "bid": 2, "tricks_taken": 2, "score": 0}},
           "game": {"trick_in_hand": 5, "round_number": 5, "hand_number": 1, "dealer": 1, "leader": 1, "trump_card": "R4", "trump_suit": "R"}},
 "rules": [{"seat": 1, "options_include": 3}, {"seat": 2, "options_include": 4}, {"seat": 3, "options_include": 5}],
 "expect": {"players": {"1": {"bid": 3, "score": 30}, "2": {"bid": 4, "score": 40}, "3": {"bid": 5, "score": 40}}}},

{"name": "Play order is leader, then leader%3+1, then the last seat: Jester lead, seat 3's Blue sets the led suit and wins", "rule": "R10", "players": 3, "seed": 1, "rounds": 1,
 "given": {"players": {"1": {"hand": ["Y6"], "tricks_taken": 0}, "2": {"hand": ["J1"], "tricks_taken": 0}, "3": {"hand": ["B7"], "tricks_taken": 0}},
           "game": {"trick_in_hand": 2, "round_number": 2, "hand_number": 1, "dealer": 1, "leader": 2, "trump_card": "R4", "trump_suit": "R"}},
 "expect": {"players": {"1": {"tricks_taken": 0}, "2": {"tricks_taken": 0}, "3": {"tricks_taken": 1}}}},

{"name": "No need to follow suit: seat 2 holding Green may play Blue, which leaves its hand", "rule": "R11", "players": 3, "seed": 1, "rounds": 1,
 "given": {"players": {"1": {"hand": ["G5"], "tricks_taken": 0}, "2": {"hand": ["G2", "B7"], "tricks_taken": 0}, "3": {"hand": ["G1"], "tricks_taken": 0}},
           "game": {"trick_in_hand": 2, "round_number": 2, "hand_number": 1, "dealer": 3, "leader": 1, "trump_card": "R4", "trump_suit": "R"}},
 "rules": [{"seat": 2, "options_include": "B7"}],
 "expect": {"players": {"1": {"tricks_taken": 1}, "2": {"tricks_taken": 0}, "3": {"tricks_taken": 0}},
            "lens": {"players": {"2": {"hand": 1}}},
            "offered": [{"seat": 2, "option": "G2"}]}},

{"name": "A Jester lead does not set the suit; the first numbered card (Yellow 3) does and wins", "rule": "R12", "players": 3, "seed": 1, "rounds": 1,
 "given": {"players": {"1": {"hand": ["J2"], "tricks_taken": 0}, "2": {"hand": ["Y3"], "tricks_taken": 0}, "3": {"hand": ["B7"], "tricks_taken": 0}},
           "game": {"trick_in_hand": 2, "round_number": 2, "hand_number": 1, "dealer": 3, "leader": 1, "trump_card": "R4", "trump_suit": "R"}},
 "expect": {"players": {"1": {"tricks_taken": 0}, "2": {"tricks_taken": 1}, "3": {"tricks_taken": 0}}}},

{"name": "A Wizard led wins over trump and a later Wizard", "rule": "R13", "players": 3, "seed": 1, "rounds": 1,
 "given": {"players": {"1": {"hand": ["W1"], "tricks_taken": 0}, "2": {"hand": ["R7"], "tricks_taken": 0}, "3": {"hand": ["W2"], "tricks_taken": 0}},
           "game": {"trick_in_hand": 2, "round_number": 2, "hand_number": 1, "dealer": 3, "leader": 1, "trump_card": "R4", "trump_suit": "R"}},
 "expect": {"players": {"1": {"tricks_taken": 1}, "2": {"tricks_taken": 0}, "3": {"tricks_taken": 0}}}},

{"name": "The first Wizard played wins even when not led", "rule": "R14", "players": 3, "seed": 1, "rounds": 1,
 "given": {"players": {"1": {"hand": ["B5"], "tricks_taken": 0}, "2": {"hand": ["W2"], "tricks_taken": 0}, "3": {"hand": ["W1"], "tricks_taken": 0}},
           "game": {"trick_in_hand": 2, "round_number": 2, "hand_number": 1, "dealer": 3, "leader": 1, "trump_card": "R4", "trump_suit": "R"}},
 "expect": {"players": {"1": {"tricks_taken": 0}, "2": {"tricks_taken": 1}, "3": {"tricks_taken": 0}}}},

{"name": "Without a Wizard the highest trump wins over a higher led card", "rule": "R15", "players": 3, "seed": 1, "rounds": 1,
 "given": {"players": {"1": {"hand": ["B7"], "tricks_taken": 0}, "2": {"hand": ["R1"], "tricks_taken": 0}, "3": {"hand": ["R3"], "tricks_taken": 0}},
           "game": {"trick_in_hand": 2, "round_number": 2, "hand_number": 1, "dealer": 3, "leader": 1, "trump_card": "R4", "trump_suit": "R"}},
 "expect": {"players": {"1": {"tricks_taken": 0}, "2": {"tricks_taken": 0}, "3": {"tricks_taken": 1}}}},

{"name": "Without Wizard or trump the highest led-suit card wins", "rule": "R16", "players": 3, "seed": 1, "rounds": 1,
 "given": {"players": {"1": {"hand": ["B3"], "tricks_taken": 0}, "2": {"hand": ["B6"], "tricks_taken": 0}, "3": {"hand": ["G7"], "tricks_taken": 0}},
           "game": {"trick_in_hand": 2, "round_number": 2, "hand_number": 1, "dealer": 3, "leader": 1, "trump_card": "R4", "trump_suit": "R"}},
 "expect": {"players": {"1": {"tricks_taken": 0}, "2": {"tricks_taken": 1}, "3": {"tricks_taken": 0}}}},

{"name": "Three Jesters in a trick: the first Jester played wins", "rule": "R17", "players": 3, "seed": 1, "rounds": 1,
 "given": {"players": {"1": {"hand": ["J1"], "tricks_taken": 0}, "2": {"hand": ["J1"], "tricks_taken": 0}, "3": {"hand": ["J2"], "tricks_taken": 0}},
           "game": {"trick_in_hand": 2, "round_number": 2, "hand_number": 1, "dealer": 1, "leader": 2, "trump_card": "R4", "trump_suit": "R"}},
 "expect": {"players": {"1": {"tricks_taken": 0}, "2": {"tricks_taken": 1}, "3": {"tricks_taken": 0}}}},

{"name": "Off-suit non-trump sevens never win; the led Green 1 wins", "rule": "R18", "players": 3, "seed": 1, "rounds": 1,
 "given": {"players": {"1": {"hand": ["G1"], "tricks_taken": 0}, "2": {"hand": ["Y7"], "tricks_taken": 0}, "3": {"hand": ["B7"], "tricks_taken": 0}},
           "game": {"trick_in_hand": 2, "round_number": 2, "hand_number": 1, "dealer": 3, "leader": 1, "trump_card": "R4", "trump_suit": "R"}},
 "expect": {"players": {"1": {"tricks_taken": 1}, "2": {"tricks_taken": 0}, "3": {"tricks_taken": 0}}}},

{"name": "Trick winner gains a trick and leads the next: seat 3 wins with a Wizard, then leads Blue and wins again", "rule": "R19", "players": 3, "seed": 1, "rounds": 2,
 "given": {"players": {"1": {"hand": ["G5", "Y2"], "tricks_taken": 0}, "2": {"hand": ["G2", "B4"], "tricks_taken": 0}, "3": {"hand": ["W1", "B6"], "tricks_taken": 0}},
           "game": {"trick_in_hand": 2, "round_number": 2, "hand_number": 1, "dealer": 3, "leader": 1, "trump_card": "R4", "trump_suit": "R"}},
 "rules": [{"seat": 1, "options_include": "G5"}, {"seat": 2, "options_include": "G2"}, {"seat": 3, "options_include": "W1"}],
 "expect": {"players": {"1": {"tricks_taken": 0}, "2": {"tricks_taken": 0}, "3": {"tricks_taken": 2}}}},

{"name": "Exact bids score 20 + 10 per trick (bid 2 took 2 = +40, bid 0 took 0 = +20)", "rule": "R20", "players": 3, "seed": 1, "rounds": 1,
 "given": {"players": {"1": {"hand": ["W1"], "bid": 2, "tricks_taken": 1, "score": 0}, "2": {"hand": ["B3"], "bid": 0, "tricks_taken": 0, "score": 0}, "3": {"hand": ["G2"], "bid": 2, "tricks_taken": 2, "score": 0}},
           "game": {"trick_in_hand": 5, "round_number": 5, "hand_number": 1, "dealer": 3, "leader": 1, "trump_card": "R4", "trump_suit": "R"}},
 "expect": {"players": {"1": {"score": 40, "tricks_taken": 2}, "2": {"score": 20, "tricks_taken": 0}, "3": {"score": 40, "tricks_taken": 2}}}},

{"name": "Missed bids lose 10 per trick of difference", "rule": "R21", "players": 3, "seed": 1, "rounds": 1,
 "given": {"players": {"1": {"hand": ["W1"], "bid": 3, "tricks_taken": 0, "score": 50}, "2": {"hand": ["B3"], "bid": 1, "tricks_taken": 3, "score": 0}, "3": {"hand": ["G2"], "bid": 0, "tricks_taken": 1, "score": 10}},
           "game": {"trick_in_hand": 5, "round_number": 5, "hand_number": 1, "dealer": 3, "leader": 1, "trump_card": "R4", "trump_suit": "R"}},
 "expect": {"players": {"1": {"score": 30, "tricks_taken": 1}, "2": {"score": -20, "tricks_taken": 3}, "3": {"score": 0, "tricks_taken": 1}}}},

{"name": "At hand end each trick count and new score is settled", "rule": "R22", "players": 3, "seed": 1, "rounds": 1,
 "given": {"players": {"1": {"hand": ["W1"], "bid": 1, "tricks_taken": 0, "score": 0}, "2": {"hand": ["B3"], "bid": 1, "tricks_taken": 1, "score": 5}, "3": {"hand": ["G2"], "bid": 1, "tricks_taken": 3, "score": 0}},
           "game": {"trick_in_hand": 5, "round_number": 5, "hand_number": 1, "dealer": 3, "leader": 1, "trump_card": "R4", "trump_suit": "R"}},
 "expect": {"players": {"1": {"score": 30, "tricks_taken": 1}, "2": {"score": 35, "tricks_taken": 1}, "3": {"score": -20, "tricks_taken": 3}}}},

{"name": "After a hand ends the next hand is dealt and bid (dealer rotation itself not observable)", "rule": "R23", "players": 3, "seed": 9, "rounds": 2, "default": "first",
 "given": {"players": {"1": {"hand": ["W1"], "bid": 0, "tricks_taken": 0, "score": 0}, "2": {"hand": ["B3"], "bid": 0, "tricks_taken": 0, "score": 0}, "3": {"hand": ["G2"], "bid": 4, "tricks_taken": 4, "score": 0}},
           "game": {"trick_in_hand": 5, "round_number": 5, "hand_number": 1, "dealer": 1, "leader": 1, "trump_card": "R4", "trump_suit": "R"}},
 "rules": [{"seat": 1, "options_include": 2}, {"seat": 2, "options_include": 1}, {"seat": 3, "options_include": 0}],
 "expect": {"players": {"1": {"bid": 2, "score": -10}, "2": {"bid": 1, "score": 20}, "3": {"bid": 0, "score": 60}},
            "lens": {"game": {"deck": 16}, "players": {"1": {"hand": 4}, "2": {"hand": 4}, "3": {"hand": 4}}}}},

{"name": "The game ends after the 30th trick and the highest score wins", "rule": "R24", "players": 3, "seed": 1,
 "given": {"players": {"1": {"hand": ["W1"], "bid": 1, "tricks_taken": 0, "score": 100}, "2": {"hand": ["B3"], "bid": 0, "tricks_taken": 4, "score": 90}, "3": {"hand": ["G2"], "bid": 0, "tricks_taken": 0, "score": 95}},
           "game": {"trick_in_hand": 5, "round_number": 30, "hand_number": 6, "dealer": 3, "leader": 1, "trump_card": "R4", "trump_suit": "R"}},
 "expect": {"winner": 1, "standings": {"1": 130, "2": 50, "3": 115},
            "players": {"1": {"score": 130}, "2": {"score": 50}, "3": {"score": 115}}}},

{"name": "Players tied at the top share the win", "rule": "R25", "players": 3, "seed": 1,
 "given": {"players": {"1": {"hand": ["W1"], "bid": 1, "tricks_taken": 0, "score": 110}, "2": {"hand": ["B3"], "bid": 2, "tricks_taken": 2, "score": 100}, "3": {"hand": ["G2"], "bid": 1, "tricks_taken": 2, "score": 130}},
           "game": {"trick_in_hand": 5, "round_number": 30, "hand_number": 6, "dealer": 3, "leader": 1, "trump_card": "R4", "trump_suit": "R"}},
 "expect": {"winner": [1, 2], "standings": {"1": 140, "2": 140, "3": 120},
            "players": {"1": {"score": 140}, "2": {"score": 140}, "3": {"score": 120}}}}
]

Why it was refused: scenario 1: needs `rules` (what each seat answers, by option name); scenario 2: needs `rules` (what each seat answers, by option name); scenario 3: needs `rules` (what each seat answers, by option name); scenario 4: needs `rules` (what each seat answers, by option name); scenario 5: needs `rules` (what each seat answers, by option name); scenario 10: needs `rules` (what each seat answers, by option name); scenario 12: needs `rules` (what each seat answers, by option name); scenario 13: needs `rules` (what each seat answers, by option name); scenario 14: needs `rules` (what each seat answers, by option name); scenario 15: needs `rules` (what each seat answers, by option name); scenario 16: needs `rules` (what each seat answers, by option name); scenario 17: needs `rules` (what each seat answers, by option name); scenario 18: needs `rules` (what each seat answers, by option name); scenario 20: needs `rules` (what each seat answers, by option name); scenario 21: needs `rules` (what each seat answers, by option name); scenario 22: needs `rules` (what each seat answers, by option name); scenario 24: needs `rules` (what each seat answers, by option name); scenario 25: needs `rules` (what each seat answers, by option name)
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
[
{"name": "Deck of 32: after the first deal and one trick, 16 stay in the deck and each hand holds 4 (cards are random, only counts asserted)", "rule": "R1", "players": 3, "seed": 1, "rounds": 1, "default": "first",
 "rules": [{"seat": 1, "options_include": 1}, {"seat": 2, "options_include": 1}, {"seat": 3, "options_include": 1}],
 "expect": {"lens": {"game": {"deck": 16}, "players": {"1": {"hand": 4}, "2": {"hand": 4}, "3": {"hand": 4}}}}},

{"name": "At the start every score is 0 and it stays 0 through the first trick", "rule": "R2", "players": 3, "seed": 1, "rounds": 1, "default": "first",
 "rules": [{"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
 "expect": {"players": {"1": {"score": 0}, "2": {"score": 0}, "3": {"score": 0}}, "standings": {"1": 0, "2": 0, "3": 0}}},

{"name": "A new hand rebuilds the deck and deals exactly 5 cards to each player, replacing old hands (counts only)", "rule": "R3", "players": 3, "seed": 2, "rounds": 1, "default": "first",
 "given": {"players": {"1": {"hand": ["R1", "R2"]}, "2": {"hand": ["B1", "B2"]}, "3": {"hand": ["G1", "G2"]}}, "game": {"deck": ["Y1", "Y2", "Y3"], "trick_in_hand": 1}},
 "rules": [{"seat": 1, "options_include": 2}, {"seat": 2, "options_include": 2}, {"seat": 3, "options_include": 2}],
 "expect": {"lens": {"game": {"deck": 16}, "players": {"1": {"hand": 4}, "2": {"hand": 4}, "3": {"hand": 4}}}}},

{"name": "One more card is turned as trump after the deal, leaving 16 in the deck (the card itself is random)", "rule": "R4", "players": 3, "seed": 3, "rounds": 1, "default": "first",
 "rules": [{"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 1}, {"seat": 3, "options_include": 2}],
 "expect": {"lens": {"game": {"deck": 16}}}},

{"name": "16 cards stay unused in the deck after the deal (counts only)", "rule": "R5", "players": 3, "seed": 4, "rounds": 1, "default": "first",
 "rules": [{"seat": 1, "options_include": 3}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 1}],
 "expect": {"lens": {"game": {"deck": 16}}}},

{"name": "Bids from a previous hand are reset and replaced by the new bids", "rule": "R6", "players": 3, "seed": 5, "rounds": 1, "default": "first",
 "given": {"players": {"1": {"bid": 4, "tricks_taken": 3}, "2": {"bid": 4, "tricks_taken": 3}, "3": {"bid": 4, "tricks_taken": 3}}, "game": {"trick_in_hand": 1}},
 "rules": [{"seat": 1, "options_include": 1}, {"seat": 2, "options_include": 2}, {"seat": 3, "options_include": 0}],
 "expect": {"players": {"1": {"bid": 1}, "2": {"bid": 2}, "3": {"bid": 0}}}},

{"name": "All three may bid 5 at once; bids need not total 5", "rule": "R7", "players": 3, "seed": 6, "rounds": 1, "default": "first",
 "rules": [{"seat": 1, "options_include": 5}, {"seat": 2, "options_include": 5}, {"seat": 3, "options_include": 5}],
 "expect": {"players": {"1": {"bid": 5}, "2": {"bid": 5}, "3": {"bid": 5}},
            "offered": [{"seat": 1, "option": 0}, {"seat": 2, "option": 5}, {"seat": 3, "option": 0}]}},

{"name": "Each player's bid is recorded and revealed", "rule": "R8", "players": 3, "seed": 7, "rounds": 1, "default": "first",
 "rules": [{"seat": 1, "options_include": 1}, {"seat": 2, "options_include": 2}, {"seat": 3, "options_include": 3}],
 "expect": {"players": {"1": {"bid": 1}, "2": {"bid": 2}, "3": {"bid": 3}}}},

{"name": "After a hand ends a new hand starts with fresh bids (next leader is seat after new dealer; cards random)", "rule": "R9", "players": 3, "seed": 8, "rounds": 2, "default": "first",
 "given": {"players": {"1": {"hand": ["W1"], "bid": 1, "tricks_taken": 0, "score": 0}, "2": {"hand": ["B3"], "bid": 2, "tricks_taken": 2, "score": 0}, "3": {"hand": ["G2"], "bid": 2, "tricks_taken": 2, "score": 0}},
           "game": {"trick_in_hand": 5, "round_number": 5, "hand_number": 1, "dealer": 1, "leader": 1, "trump_card": "R4", "trump_suit": "R"}},
 "rules": [{"seat": 1, "options_include": 3}, {"seat": 2, "options_include": 4}, {"seat": 3, "options_include": 5}],
 "expect": {"players": {"1": {"bid": 3, "score": 30}, "2": {"bid": 4, "score": 40}, "3": {"bid": 5, "score": 40}}}},

{"name": "Play order is leader, then leader%3+1, then the last seat: Jester lead, seat 3's Blue sets the led suit and wins", "rule": "R10", "players": 3, "seed": 1, "rounds": 1,
 "given": {"players": {"1": {"hand": ["Y6"], "tricks_taken": 0}, "2": {"hand": ["J1"], "tricks_taken": 0}, "3": {"hand": ["B7"], "tricks_taken": 0}},
           "game": {"trick_in_hand": 2, "round_number": 2, "hand_number": 1, "dealer": 1, "leader": 2, "trump_card": "R4", "trump_suit": "R"}},
 "rules": [{"seat": 2, "options_include": "J1"}, {"seat": 3, "options_include": "B7"}, {"seat": 1, "options_include": "Y6"}],
 "expect": {"players": {"1": {"tricks_taken": 0}, "2": {"tricks_taken": 0}, "3": {"tricks_taken": 1}}}},

{"name": "No need to follow suit: seat 2 holding Green may play Blue, which leaves its hand", "rule": "R11", "players": 3, "seed": 1, "rounds": 1,
 "given": {"players": {"1": {"hand": ["G5"], "tricks_taken": 0}, "2": {"hand": ["G2", "B7"], "tricks_taken": 0}, "3": {"hand": ["G1"], "tricks_taken": 0}},
           "game": {"trick_in_hand": 2, "round_number": 2, "hand_number": 1, "dealer": 3, "leader": 1, "trump_card": "R4", "trump_suit": "R"}},
 "rules": [{"seat": 2, "options_include": "B7"}],
 "expect": {"players": {"1": {"tricks_taken": 1}, "2": {"tricks_taken": 0}, "3": {"tricks_taken": 0}},
            "lens": {"players": {"2": {"hand": 1}}},
            "offered": [{"seat": 2, "option": "G2"}]}},

{"name": "A Jester lead does not set the suit; the first numbered card (Yellow 3) does and wins", "rule": "R12", "players": 3, "seed": 1, "rounds": 1,
 "given": {"players": {"1": {"hand": ["J2"], "tricks_taken": 0}, "2": {"hand": ["Y3"], "tricks_taken": 0}, "3": {"hand": ["B7"], "tricks_taken": 0}},
           "game": {"trick_in_hand": 2, "round_number": 2, "hand_number": 1, "dealer": 3, "leader": 1, "trump_card": "R4", "trump_suit": "R"}},
 "rules": [{"seat": 1, "options_include": "J2"}, {"seat": 2, "options_include": "Y3"}, {"seat": 3, "options_include": "B7"}],
 "expect": {"players": {"1": {"tricks_taken": 0}, "2": {"tricks_taken": 1}, "3": {"tricks_taken": 0}}}},

{"name": "A Wizard led wins over trump and a later Wizard", "rule": "R13", "players": 3, "seed": 1, "rounds": 1,
 "given": {"players": {"1": {"hand": ["W1"], "tricks_taken": 0}, "2": {"hand": ["R7"], "tricks_taken": 0}, "3": {"hand": ["W2"], "tricks_taken": 0}},
           "game": {"trick_in_hand": 2, "round_number": 2, "hand_number": 1, "dealer": 3, "leader": 1, "trump_card": "R4", "trump_suit": "R"}},
 "rules": [{"seat": 1, "options_include": "W1"}, {"seat": 2, "options_include": "R7"}, {"seat": 3, "options_include": "W2"}],
 "expect": {"players": {"1": {"tricks_taken": 1}, "2": {"tricks_taken": 0}, "3": {"tricks_taken": 0}}}},

{"name": "The first Wizard played wins even when not led", "rule": "R14", "players": 3, "seed": 1, "rounds": 1,
 "given": {"players": {"1": {"hand": ["B5"], "tricks_taken": 0}, "2": {"hand": ["W2"], "tricks_taken": 0}, "3": {"hand": ["W1"], "tricks_taken": 0}},
           "game": {"trick_in_hand": 2, "round_number": 2, "hand_number": 1, "dealer": 3, "leader": 1, "trump_card": "R4", "trump_suit": "R"}},
 "rules": [{"seat": 1, "options_include": "B5"}, {"seat": 2, "options_include": "W2"}, {"seat": 3, "options_include": "W1"}],
 "expect": {"players": {"1": {"tricks_taken": 0}, "2": {"tricks_taken": 1}, "3": {"tricks_taken": 0}}}},

{"name": "Without a Wizard the highest trump wins over a higher led card", "rule": "R15", "players": 3, "seed": 1, "rounds": 1,
 "given": {"players": {"1": {"hand": ["B7"], "tricks_taken": 0}, "2": {"hand": ["R1"], "tricks_taken": 0}, "3": {"hand": ["R3"], "tricks_taken": 0}},
           "game": {"trick_in_hand": 2, "round_number": 2, "hand_number": 1, "dealer": 3, "leader": 1, "trump_card": "R4", "trump_suit": "R"}},
 "rules": [{"seat": 1, "options_include": "B7"}, {"seat": 2, "options_include": "R1"}, {"seat": 3, "options_include": "R3"}],
 "expect": {"players": {"1": {"tricks_taken": 0}, "2": {"tricks_taken": 0}, "3": {"tricks_taken": 1}}}},

{"name": "Without Wizard or trump the highest led-suit card wins", "rule": "R16", "players": 3, "seed": 1, "rounds": 1,
 "given": {"players": {"1": {"hand": ["B3"], "tricks_taken": 0}, "2": {"hand": ["B6"], "tricks_taken": 0}, "3": {"hand": ["G7"], "tricks_taken": 0}},
           "game": {"trick_in_hand": 2, "round_number": 2, "hand_number": 1, "dealer": 3, "leader": 1, "trump_card": "R4", "trump_suit": "R"}},
 "rules": [{"seat": 1, "options_include": "B3"}, {"seat": 2, "options_include": "B6"}, {"seat": 3, "options_include": "G7"}],
 "expect": {"players": {"1": {"tricks_taken": 0}, "2": {"tricks_taken": 1}, "3": {"tricks_taken": 0}}}},

{"name": "Three Jesters in a trick: the first Jester played wins", "rule": "R17", "players": 3, "seed": 1, "rounds": 1,
 "given": {"players": {"1": {"hand": ["J1"], "tricks_taken": 0}, "2": {"hand": ["J1"], "tricks_taken": 0}, "3": {"hand": ["J2"], "tricks_taken": 0}},
           "game": {"trick_in_hand": 2, "round_number": 2, "hand_number": 1, "dealer": 1, "leader": 2, "trump_card": "R4", "trump_suit": "R"}},
 "rules": [{"seat": 2, "options_include": "J1"}, {"seat": 3, "options_include": "J2"}, {"seat": 1, "options_include": "J1"}],
 "expect": {"players": {"1": {"tricks_taken": 0}, "2": {"tricks_taken": 1}, "3": {"tricks_taken": 0}}}},

{"name": "Off-suit non-trump sevens never win; the led Green 1 wins", "rule": "R18", "players": 3, "seed": 1, "rounds": 1,
 "given": {"players": {"1": {"hand": ["G1"], "tricks_taken": 0}, "2": {"hand": ["Y7"], "tricks_taken": 0}, "3": {"hand": ["B7"], "tricks_taken": 0}},
           "game": {"trick_in_hand": 2, "round_number": 2, "hand_number": 1, "dealer": 3, "leader": 1, "trump_card": "R4", "trump_suit": "R"}},
 "rules": [{"seat": 1, "options_include": "G1"}, {"seat": 2, "options_include": "Y7"}, {"seat": 3, "options_include": "B7"}],
 "expect": {"players": {"1": {"tricks_taken": 1}, "2": {"tricks_taken": 0}, "3": {"tricks_taken": 0}}}},

{"name": "Trick winner gains a trick and leads the next: seat 3 wins with a Wizard, then leads Blue and wins again", "rule": "R19", "players": 3, "seed": 1, "rounds": 2,
 "given": {"players": {"1": {"hand": ["G5", "Y2"], "tricks_taken": 0}, "2": {"hand": ["G2", "B4"], "tricks_taken": 0}, "3": {"hand": ["W1", "B6"], "tricks_taken": 0}},
           "game": {"trick_in_hand": 2, "round_number": 2, "hand_number": 1, "dealer": 3, "leader": 1, "trump_card": "R4", "trump_suit": "R"}},
 "rules": [{"seat": 1, "options_include": "G5"}, {"seat": 2, "options_include": "G2"}, {"seat": 3, "options_include": "W1"}],
 "expect": {"players": {"1": {"tricks_taken": 0}, "2": {"tricks_taken": 0}, "3": {"tricks_taken": 2}}}},

{"name": "Exact bids score 20 + 10 per trick (bid 2 took 2 = +40, bid 0 took 0 = +20)", "rule": "R20", "players": 3, "seed": 1, "rounds": 1,
 "given": {"players": {"1": {"hand": ["W1"], "bid": 2, "tricks_taken": 1, "score": 0}, "2": {"hand": ["B3"], "bid": 0, "tricks_taken": 0, "score": 0}, "3": {"hand": ["G2"], "bid": 2, "tricks_taken": 2, "score": 0}},
           "game": {"trick_in_hand": 5, "round_number": 5, "hand_number": 1, "dealer": 3, "leader": 1, "trump_card": "R4", "trump_suit": "R"}},
 "rules": [{"seat": 1, "options_include": "W1"}, {"seat": 2, "options_include": "B3"}, {"seat": 3, "options_include": "G2"}],
 "expect": {"players": {"1": {"score": 40, "tricks_taken": 2}, "2": {"score": 20, "tricks_taken": 0}, "3": {"score": 40, "tricks_taken": 2}}}},

{"name": "Missed bids lose 10 per trick of difference", "rule": "R21", "players": 3, "seed": 1, "rounds": 1,
 "given": {"players": {"1": {"hand": ["W1"], "bid": 3, "tricks_taken": 0, "score": 50}, "2": {"hand": ["B3"], "bid": 1, "tricks_taken": 3, "score": 0}, "3": {"hand": ["G2"], "bid": 0, "tricks_taken": 1, "score": 10}},
           "game": {"trick_in_hand": 5, "round_number": 5, "hand_number": 1, "dealer": 3, "leader": 1, "trump_card": "R4", "trump_suit": "R"}},
 "rules": [{"seat": 1, "options_include": "W1"}, {"seat": 2, "options_include": "B3"}, {"seat": 3, "options_include": "G2"}],
 "expect": {"players": {"1": {"score": 30, "tricks_taken": 1}, "2": {"score": -20, "tricks_taken": 3}, "3": {"score": 0, "tricks_taken": 1}}}},

{"name": "At hand end each trick count and new score is settled", "rule": "R22", "players": 3, "seed": 1, "rounds": 1,
 "given": {"players": {"1": {"hand": ["W1"], "bid": 1, "tricks_taken": 0, "score": 0}, "2": {"hand": ["B3"], "bid": 1, "tricks_taken": 1, "score": 5}, "3": {"hand": ["G2"], "bid": 1, "tricks_taken": 3, "score": 0}},
           "game": {"trick_in_hand": 5, "round_number": 5, "hand_number": 1, "dealer": 3, "leader": 1, "trump_card": "R4", "trump_suit": "R"}},
 "rules": [{"seat": 1, "options_include": "W1"}, {"seat": 2, "options_include": "B3"}, {"seat": 3, "options_include": "G2"}],
 "expect": {"players": {"1": {"score": 30, "tricks_taken": 1}, "2": {"score": 35, "tricks_taken": 1}, "3": {"score": -20, "tricks_taken": 3}}}},

{"name": "After a hand ends the next hand is dealt and bid (dealer rotation itself not observable)", "rule": "R23", "players": 3, "seed": 9, "rounds": 2, "default": "first",
 "given": {"players": {"1": {"hand": ["W1"], "bid": 0, "tricks_taken": 0, "score": 0}, "2": {"hand": ["B3"], "bid": 0, "tricks_taken": 0, "score": 0}, "3": {"hand": ["G2"], "bid": 4, "tricks_taken": 4, "score": 0}},
           "game": {"trick_in_hand": 5, "round_number": 5, "hand_number": 1, "dealer": 1, "leader": 1, "trump_card": "R4", "trump_suit": "R"}},
 "rules": [{"seat": 1, "options_include": 2}, {"seat": 2, "options_include": 1}, {"seat": 3, "options_include": 0}],
 "expect": {"players": {"1": {"bid": 2, "score": -10}, "2": {"bid": 1, "score": 20}, "3": {"bid": 0, "score": 60}},
            "lens": {"game": {"deck": 16}, "players": {"1": {"hand": 4}, "2": {"hand": 4}, "3": {"hand": 4}}}}},

{"name": "The game ends after the 30th trick and the highest score wins", "rule": "R24", "players": 3, "seed": 1,
 "given": {"players": {"1": {"hand": ["W1"], "bid": 1, "tricks_taken": 0, "score": 100}, "2": {"hand": ["B3"], "bid": 0, "tricks_taken": 4, "score": 90}, "3": {"hand": ["G2"], "bid": 0, "tricks_taken": 0, "score": 95}},
           "game": {"trick_in_hand": 5, "round_number": 30, "hand_number": 6, "dealer": 3, "leader": 1, "trump_card": "R4", "trump_suit": "R"}},
 "rules": [{"seat": 1, "options_include": "W1"}, {"seat": 2, "options_include": "B3"}, {"seat": 3, "options_include": "G2"}],
 "expect": {"winner": 1, "standings": {"1": 130, "2": 50, "3": 115},
            "players": {"1": {"score": 130}, "2": {"score": 50}, "3": {"score": 115}}}},

{"name": "Players tied at the top share the win", "rule": "R25", "players": 3, "seed": 1,
 "given": {"players": {"1": {"hand": ["W1"], "bid": 1, "tricks_taken": 0, "score": 110}, "2": {"hand": ["B3"], "bid": 2, "tricks_taken": 2, "score": 100}, "3": {"hand": ["G2"], "bid": 1, "tricks_taken": 2, "score": 130}},
           "game": {"trick_in_hand": 5, "round_number": 30, "hand_number": 6, "dealer": 3, "leader": 1, "trump_card": "R4", "trump_suit": "R"}},
 "rules": [{"seat": 1, "options_include": "W1"}, {"seat": 2, "options_include": "B3"}, {"seat": 3, "options_include": "G2"}],
 "expect": {"winner": [1, 2], "standings": {"1": 140, "2": 140, "3": 120},
            "players": {"1": {"score": 140}, "2": {"score": 140}, "3": {"score": 120}}}}
]
````
