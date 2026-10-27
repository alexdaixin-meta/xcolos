# 05 scenarios

- time: 2026-10-27T21:20:23+00:00 (60.5s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 193170133d38efd2, reply sha256 62b3ea366a6dc3d6

## Sent

````
SPEC:
{
  "name": "Eleven Takes: Three Piles",
  "summary": "Players play cards from hidden hands onto three shared piles in a clockwise number range, or take a pile into their hand and earn bulls that allow extra plays; the lowest ox-head penalty in hand wins.",
  "players": {
    "min": 3,
    "max": 4,
    "suggested": 4
  },
  "parameters": {
    "deck_low": 1,
    "deck_high": 40,
    "deck_size": 40,
    "oxheads_multiple_of_10": 3,
    "oxheads_multiple_of_5_not_10": 2,
    "oxheads_other": 1,
    "deck_total_oxheads": 52,
    "hand_size_start": 6,
    "pile_count": 3,
    "start_cards_per_pile": 1,
    "set_aside_with_4": 13,
    "set_aside_with_3": 19,
    "bull_supply_offset": 1,
    "legal_step_min": 1,
    "legal_step_max": 6,
    "legal_modulus": 40,
    "take_bull_threshold": 3,
    "bulls_for_first_extra": 1,
    "bulls_for_second_extra": 2,
    "max_cycles_with_4": 10,
    "max_cycles_with_3": 12,
    "max_turns_with_4": 40,
    "max_turns_with_3": 36,
    "empty_hand_penalty": 0
  },
  "attributes": {
    "player": [
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "The cards (numbers 1-40) in this player's private hand.",
        "observable": false
      },
      {
        "key": "hand_size",
        "type": "number",
        "visible": "public",
        "initial": 6,
        "meaning": "The number of cards in hand. It is public by the rules and kept equal to the length of hand.",
        "observable": true
      },
      {
        "key": "bulls",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Bull tokens held. Each one allows one extra card after a play, up to 2 extras. Bulls are never spent.",
        "observable": true
      },
      {
        "key": "penalty",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Total ox-heads of the cards in hand. It is computed when the game ends, and 0 for an empty hand.",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "set_aside",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "The cards left over after the deal, set aside unseen for the whole game: 13 with 4 players, 19 with 3.",
        "observable": false
      },
      {
        "key": "pile_a",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Ordered contents of Pile A. The last element is the top card.",
        "observable": true
      },
      {
        "key": "pile_b",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Ordered contents of Pile B. The last element is the top card.",
        "observable": true
      },
      {
        "key": "pile_c",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Ordered contents of Pile C. The last element is the top card.",
        "observable": true
      },
      {
        "key": "bull_supply",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Bull tokens left in the supply. It starts at the number of players minus 1.",
        "observable": true
      },
      {
        "key": "active_seat",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "The seat whose turn it is.",
        "observable": false
      },
      {
        "key": "cycle",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The number of full cycles completed, where one cycle is a turn for every seat.",
        "observable": true
      },
      {
        "key": "max_cycles",
        "type": "number",
        "visible": "public",
        "initial": 10,
        "meaning": "The cycle limit, 18 - 2*N: 10 with 4 players, 12 with 3.",
        "observable": false
      },
      {
        "key": "ending_triggered",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "True once any player has emptied their hand. The game then ends after seat N's turn.",
        "observable": true
      },
      {
        "key": "last_action",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "A public record of the active player's action this turn: the card played and the pile, or the pile taken and the restart card.",
        "observable": false
      },
      {
        "key": "chosen_pile",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The pile (A, B or C) named in this turn's action.",
        "observable": false
      },
      {
        "key": "action_kind",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Either 'play' or 'take' for the current turn.",
        "observable": false
      },
      {
        "key": "taken_size",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "How many cards the taken pile held before it was taken.",
        "observable": false
      },
      {
        "key": "extra_stopped",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "True once the active player stops adding extra cards this turn, or an extra card ends the run.",
        "observable": false
      }
    ]
  },
  "setup": [
    "Build the deck as the numbers 1 to 40. A card's ox-heads are 3 if it is a multiple of 10, 2 if it is a multiple of 5 but not of 10, and 1 otherwise, for 52 ox-heads in total.",
    "Shuffle once, using the seeded random draw. This is the only random event in the game.",
    "Deal 6 cards to each player's hand by drawing at random from the deck. Set each hand_size to 6.",
    "Draw one card each to form pile_a, pile_b and pile_c, face up, so each pile is a public one-card list.",
    "Put the remaining cards in set_aside, hidden from everyone (13 with 4 players, 19 with 3). They are never used again.",
    "Set bull_supply to N - 1 and max_cycles to 18 - 2*N. Set active_seat to 1, cycle to 0 and ending_triggered to false.",
    "Seats are numbered 1 to N. Seat 1 moves first and play proceeds in seat order."
  ],
  "round": [
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player sees their own hand, and everyone sees the piles, every hand_size, bulls, bull_supply, cycle and last_action."
    },
    {
      "action": "ask",
      "who": "the seat equal to active_seat",
      "answer": "One choice from: 'play X on P' for every card X in hand that is legal on pile P (that is, (X - top(P)) mod 40 is between 1 and 6), plus 'take A', 'take B' and 'take C'.",
      "effect": "Sets action_kind to 'play' or 'take' and sets chosen_pile. A missing or invalid answer is replaced by taking the smallest pile, with ties broken A before B before C. Clears extra_stopped."
    },
    {
      "action": "update",
      "who": "the seat equal to active_seat",
      "answer": null,
      "effect": "When action_kind is 'play': remove X from hand, append X to the chosen pile, subtract 1 from hand_size, and set last_action to 'Seat s plays X on P'."
    },
    {
      "action": "ask",
      "who": "the seat equal to active_seat, when action_kind is 'play' and bulls >= 1",
      "answer": "Either 'stop', or one card in hand that is legal on the new top of the chosen pile.",
      "effect": "If 'stop', set extra_stopped to true. Otherwise remove the card from hand, append it to the chosen pile, subtract 1 from hand_size, and add it to last_action."
    },
    {
      "action": "ask",
      "who": "the seat equal to active_seat, when action_kind is 'play', bulls >= 2 and extra_stopped is false",
      "answer": "Either 'stop', or one card in hand that is legal on the new top of the chosen pile.",
      "effect": "If a card is given, remove it from hand, append it to the chosen pile, subtract 1 from hand_size, and add it to last_action."
    },
    {
      "action": "update",
      "who": "the seat equal to active_seat",
      "answer": null,
      "effect": "When action_kind is 'take': set taken_size to the length of the chosen pile, append all of its cards to hand, set the pile to empty, and add taken_size to hand_size."
    },
    {
      "action": "ask",
      "who": "the seat equal to active_seat, when action_kind is 'take'",
      "answer": "One card from the player's hand.",
      "effect": "Remove that card from hand, set the chosen pile to a list holding only that card, subtract 1 from hand_size, and set last_action to 'Seat s takes P (k cards) and restarts it with Y'."
    },
    {
      "action": "update",
      "who": "the seat equal to active_seat",
      "answer": null,
      "effect": "When action_kind is 'take' and taken_size >= 3: if bull_supply > 0, subtract 1 from bull_supply and add 1 to the taker's bulls. Otherwise, if any opponent has bulls > 0, take 1 bull from the opponent with the most bulls, breaking ties by the smallest (seat - active_seat) mod N, and add it to the taker's bulls. If no opponent has a bull, nothing happens."
    },
    {
      "action": "update",
      "who": "the seat equal to active_seat",
      "answer": null,
      "effect": "If the active player's hand_size = 0, set ending_triggered to true."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "If active_seat = N, add 1 to cycle and set active_seat to 1. Otherwise add 1 to active_seat."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When active_seat = 1 and (ending_triggered is true or cycle >= max_cycles): set every player's penalty to the sum, over the cards in their hand, of 3 for a multiple of 10, 2 for a multiple of 5 that is not a multiple of 10, and 1 otherwise. An empty hand gives 0."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if active_seat = 1 and (ending_triggered is true or cycle >= max_cycles). Otherwise continue with the next turn."
    }
  ],
  "ending": {
    "condition": "active_seat = 1 and (ending_triggered = true or cycle >= max_cycles)",
    "rank_by": "0 - you.penalty",
    "decided_by": "Each player's standing is minus their penalty, the total ox-heads in their hand at the end. The lowest penalty wins, and players tied for the lowest share the win as a draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game is set up, the deck is the numbers 1 to 40, each player's hand holds 6 cards, pile_a, pile_b and pile_c hold 1 card each, and set_aside holds the remaining 13 cards with 4 players or 19 with 3."
    },
    {
      "id": "R2",
      "text": "When ox-heads are counted, a multiple of 10 is worth 3, a multiple of 5 that is not a multiple of 10 is worth 2, and any other card is worth 1, so the deck totals 52."
    },
    {
      "id": "R3",
      "text": "When the game starts, bull_supply is N - 1: 3 with 4 players and 2 with 3."
    },
    {
      "id": "R4",
      "text": "When a card c is played on a pile with top card t, the play is legal only if (c - t) mod 40 is between 1 and 6. For example, on 12 the cards 13 to 18 are legal, and on 37 the cards 38, 39, 40, 1, 2 and 3 are legal."
    },
    {
      "id": "R5",
      "text": "When the active player chooses 'play X on P', X is removed from their hand, appended to the top of pile P, and their hand_size drops by 1."
    },
    {
      "id": "R6",
      "text": "When the active player has played and holds at least 1 bull, they may add one more card legal on the new top of the same pile, or stop."
    },
    {
      "id": "R7",
      "text": "When the active player has played, holds 2 or more bulls and did not stop after the first extra card, they may add a second extra card legal on the new top of the same pile, or stop."
    },
    {
      "id": "R8",
      "text": "When a player uses bulls to add extra cards, their bulls count is unchanged."
    },
    {
      "id": "R9",
      "text": "When the active player chooses 'take P', every card of pile P is added to their hand and hand_size rises by the pile's size."
    },
    {
      "id": "R10",
      "text": "When a player has taken pile P, they must choose one card from their hand to become the only card of pile P, and hand_size drops by 1."
    },
    {
      "id": "R11",
      "text": "When the taken pile held 3 or more cards and bull_supply > 0, bull_supply drops by 1 and the taker's bulls rise by 1."
    },
    {
      "id": "R12",
      "text": "When the taken pile held 3 or more cards and bull_supply = 0, the taker takes 1 bull from the opponent with the most bulls, ties going to the first such opponent in seat order after the taker. If no opponent has a bull, nothing changes."
    },
    {
      "id": "R13",
      "text": "When the taken pile held 2 or fewer cards, no bull changes hands."
    },
    {
      "id": "R14",
      "text": "When the active player gives no valid answer to the action question, they take the smallest pile, with ties broken A before B before C."
    },
    {
      "id": "R15",
      "text": "When a player may take, they may do so even if a legal play exists."
    },
    {
      "id": "R16",
      "text": "When a player's hand_size reaches 0 on their turn, ending_triggered becomes true and the game ends after seat N's turn in that cycle, so every player has the same number of turns."
    },
    {
      "id": "R17",
      "text": "When 10 full cycles have been played with 4 players (40 turns), or 12 with 3 players (36 turns), the game ends."
    },
    {
      "id": "R18",
      "text": "When the game ends, each player's penalty is the total ox-heads in their hand, and a player with an empty hand has penalty 0."
    },
    {
      "id": "R19",
      "text": "When the game ends, the player with the lowest penalty wins, and players tied for the lowest share a draw."
    },
    {
      "id": "R20",
      "text": "When any action is taken, last_action records it publicly, and pile contents, hand_size and bulls are always public, while hands and set_aside stay hidden."
    }
  ],
  "offers": [
    {
      "question": "Main action on your turn",
      "who": "the seat equal to active_seat",
      "options": "Every 'play X on P' where X is in that seat's hand and (X - top of P) mod 40 is between 1 and 6, for P in A, B and C, plus 'take A', 'take B' and 'take C' always. A seat with no legal play is offered only the three take options."
    },
    {
      "question": "First extra card after a play",
      "who": "the active seat, only if it played and holds 1 or more bulls",
      "options": "'stop', plus every card in hand that is legal on the new top of the pile just played on. If no card is legal, only 'stop' is offered."
    },
    {
      "question": "Second extra card after a play",
      "who": "the active seat, only if it played, holds 2 or more bulls and did not stop at the first extra",
      "options": "'stop', plus every card in hand that is legal on the new top of the same pile. If no card is legal, only 'stop' is offered."
    },
    {
      "question": "Restart card for the taken pile",
      "who": "the active seat, only after a take",
      "options": "Every card currently in that seat's hand, including the cards just taken."
    }
  ],
  "choices": [
    {
      "what": "3 to 4 players, suggested 4",
      "why": "The designer gives 3-4 and suggests 4. With fewer than 3 there are too few rivals to steal bulls from or to dump piles on. With more than 4 the 40-card deck cannot deal 6 cards each plus 3 piles with cards left to set aside as the rules intend, and the bull supply and cycle limits are defined only for 3 and 4."
    },
    {
      "what": "One engine round is one player's turn, with active_seat cycling 1..N",
      "why": "The rules say a turn is one engine round. The end check runs only after seat N's turn, so every player gets the same number of turns."
    },
    {
      "what": "max_cycles = 18 - 2*N and bull_supply = N - 1",
      "why": "These write the source's per-count numbers (10 cycles with 4 and 12 with 3; supply 3 with 4 and 2 with 3) as rules over the count."
    },
    {
      "what": "Penalty is computed only at the end of the game",
      "why": "A running public penalty would leak hidden hand contents. The rules make only hand size and bulls public."
    },
    {
      "what": "No pre-move talk step",
      "why": "The source has no talk, and adding it would add a mechanic. Play is purely sequential and every action is public."
    },
    {
      "what": "Ranking is 0 - penalty",
      "why": "Lowest penalty wins. Negating it lets the highest rank_by win, and ties at the top share the win, which matches the source's draw."
    },
    {
      "what": "The steal tie-break uses the smallest (seat - active_seat) mod N",
      "why": "This is 'the first such player in seat order after the taker' written as arithmetic."
    }
  ],
  "simplifications": [
    {
      "what": "Only legal plays are offered, so an illegal PLAY choice cannot be made. The fallback 'take the smallest pile' applies when a seat gives no valid answer.",
      "why": "The engine never offers a seat an action it may not take. The fallback still covers the same failure case."
    },
    {
      "what": "Only legal extra cards are offered, plus 'stop'",
      "why": "This has the same effect as the rule that an illegal extra card is ignored and ends the run."
    },
    {
      "what": "The branches after the main action (extra cards for a play, restart card and bulls for a take) are separate steps, each with its own arithmetic 'when' condition",
      "why": "The step list is flat. A per-step condition on action_kind reproduces both branches without choosing between blocks of steps."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: hand_size, bulls, penalty; table: pile_a, pile_b, pile_c, bull_supply, cycle, ending_triggered.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
```json
[
  {
    "name": "Setup with 4 players: 6 cards per hand, 1 card per pile, 13 set aside",
    "rule": "R1",
    "players": 4,
    "seed": 1,
    "rounds": 0,
    "expect": {
      "lens": {
        "game": {"pile_a": 1, "pile_b": 1, "pile_c": 1, "set_aside": 13},
        "players": {"1": {"hand": 6}, "2": {"hand": 6}, "3": {"hand": 6}, "4": {"hand": 6}}
      },
      "players": {"1": {"hand_size": 6}, "2": {"hand_size": 6}, "3": {"hand_size": 6}, "4": {"hand_size": 6}}
    }
  },
  {
    "name": "Setup with 3 players: 6 cards per hand, 1 card per pile, 19 set aside",
    "rule": "R1",
    "players": 3,
    "seed": 2,
    "rounds": 0,
    "expect": {
      "lens": {
        "game": {"pile_a": 1, "pile_b": 1, "pile_c": 1, "set_aside": 19},
        "players": {"1": {"hand": 6}, "2": {"hand": 6}, "3": {"hand": 6}}
      },
      "players": {"1": {"hand_size": 6}, "2": {"hand_size": 6}, "3": {"hand_size": 6}}
    }
  },
  {
    "name": "Bull supply starts at 3 with 4 players, nobody holds bulls",
    "rule": "R3",
    "players": 4,
    "seed": 3,
    "rounds": 0,
    "expect": {
      "game": {"bull_supply": 3, "cycle": 0, "ending_triggered": false},
      "players": {"1": {"bulls": 0}, "2": {"bulls": 0}, "3": {"bulls": 0}, "4": {"bulls": 0}}
    }
  },
  {
    "name": "Bull supply starts at 2 with 3 players",
    "rule": "R3",
    "players": 3,
    "seed": 4,
    "rounds": 0,
    "expect": {
      "game": {"bull_supply": 2, "cycle": 0, "ending_triggered": false},
      "players": {"1": {"bulls": 0}, "2": {"bulls": 0}, "3": {"bulls": 0}}
    }
  },
  {
    "name": "Ox-heads at the end: multiples of 10 count 3, other multiples of 5 count 2, the rest 1",
    "rule": "R2",
    "players": 4,
    "seed": 5,
    "given": {
      "players": {
        "1": {"hand": [10, 20], "hand_size": 2, "bulls": 0},
        "2": {"hand": [5, 15, 1], "hand_size": 3, "bulls": 0},
        "3": {"hand": [2, 3, 4], "hand_size": 3, "bulls": 0},
        "4": {"hand": [13, 7, 35], "hand_size": 3, "bulls": 0}
      },
      "game": {"pile_a": [12], "pile_b": [24], "pile_c": [26], "active_seat": 4, "cycle": 9, "max_cycles": 10, "bull_supply": 3}
    },
    "rules": [{"seat": 4, "options_include": "play 13 on A"}],
    "expect": {
      "winner": 3,
      "standings": {"1": -6, "2": -5, "3": -3, "4": -3},
      "players": {"1": {"penalty": 6}, "2": {"penalty": 5}, "3": {"penalty": 3}, "4": {"penalty": 3}},
      "game": {"cycle": 10, "pile_a": [12, 13]}
    }
  },
  {
    "name": "Legal plays on 37 wrap around: 38, 40 and 3 offered, 36, 4 and 10 not",
    "rule": "R4",
    "players": 3,
    "seed": 6,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [38, 3, 4, 36, 40, 10], "hand_size": 6, "bulls": 0}},
      "game": {"pile_a": [37], "pile_b": [12], "pile_c": [20], "active_seat": 1}
    },
    "rules": [{"seat": 1, "options_include": "play 3 on A"}],
    "expect": {
      "offered": [
        {"seat": 1, "option": "play 38 on A"},
        {"seat": 1, "option": "play 40 on A"},
        {"seat": 1, "option": "play 3 on A"}
      ],
      "not_offered": [
        {"seat": 1, "option": "play 4 on A"},
        {"seat": 1, "option": "play 36 on A"},
        {"seat": 1, "option": "play 10 on A"},
        {"seat": 1, "option": "play 10 on B"},
        {"seat": 1, "option": "play 38 on C"}
      ],
      "game": {"pile_a": [37, 3]},
      "players": {"1": {"hand_size": 5}}
    }
  },
  {
    "name": "Legal plays on 12 are 13 to 18: 18 offered, 19 and 11 not",
    "rule": "R4",
    "players": 3,
    "seed": 7,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [18, 19, 11], "hand_size": 3, "bulls": 0}},
      "game": {"pile_a": [12], "pile_b": [30], "pile_c": [32], "active_seat": 1}
    },
    "rules": [{"seat": 1, "options_include": "play 18 on A"}],
    "expect": {
      "offered": [{"seat": 1, "option": "play 18 on A"}],
      "not_offered": [{"seat": 1, "option": "play 19 on A"}, {"seat": 1, "option": "play 11 on A"}],
      "game": {"pile_a": [12, 18]},
      "players": {"1": {"hand_size": 2}}
    }
  },
  {
    "name": "Playing a card moves it to the top of the pile and hand_size drops by 1",
    "rule": "R5",
    "players": 3,
    "seed": 8,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [13, 25, 30], "hand_size": 3, "bulls": 0}},
      "game": {"pile_a": [12], "pile_b": [1], "pile_c": [5], "active_seat": 1}
    },
    "rules": [{"seat": 1, "options_include": "play 13 on A"}],
    "expect": {
      "game": {"pile_a": [12, 13], "pile_b": [1], "pile_c": [5]},
      "players": {"1": {"hand_size": 2, "bulls": 0}}
    }
  },
  {
    "name": "With 1 bull a player may add one extra legal card on the same pile",
    "rule": "R6",
    "players": 3,
    "seed": 9,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [13, 15, 30], "hand_size": 3, "bulls": 1}},
      "game": {"pile_a": [12], "pile_b": [2], "pile_c": [22], "active_seat": 1, "bull_supply": 1}
    },
    "rules": [
      {"seat": 1, "options_include": "play 13 on A"},
      {"seat": 1, "options_include": 15}
    ],
    "expect": {
      "offered": [{"seat": 1, "option": "stop"}],
      "game": {"pile_a": [12, 13, 15]},
      "players": {"1": {"hand_size": 1, "bulls": 1}}
    }
  },
  {
    "name": "With 2 bulls a player may add two extra legal cards on the same pile",
    "rule": "R7",
    "players": 3,
    "seed": 10,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [13, 15, 17, 30], "hand_size": 4, "bulls": 2}},
      "game": {"pile_a": [12], "pile_b": [2], "pile_c": [22], "active_seat": 1, "bull_supply": 0}
    },
    "rules": [
      {"seat": 1, "options_include": "play 13 on A"},
      {"seat": 1, "options_include": 15},
      {"seat": 1, "options_include": 17}
    ],
    "expect": {
      "game": {"pile_a": [12, 13, 15, 17]},
      "players": {"1": {"hand_size": 1, "bulls": 2}}
    }
  },
  {
    "name": "Using bulls for extra cards does not spend them or return them to the supply",
    "rule": "R8",
    "players": 3,
    "seed": 11,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [13, 15, 30], "hand_size": 3, "bulls": 1}},
      "game": {"pile_a": [12], "pile_b": [2], "pile_c": [22], "active_seat": 1, "bull_supply": 1}
    },
    "rules": [
      {"seat": 1, "options_include": "play 13 on A"},
      {"seat": 1, "options_include": 15}
    ],
    "expect": {
      "game": {"bull_supply": 1, "pile_a": [12, 13, 15]},
      "players": {"1": {"bulls": 1, "hand_size": 1}}
    }
  },
  {
    "name": "Taking a 2-card pile adds both cards to the hand",
    "rule": "R9",
    "players": 3,
    "seed": 12,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [1, 20, 30], "hand_size": 3, "bulls": 0}},
      "game": {"pile_a": [12, 13], "pile_b": [33], "pile_c": [35], "active_seat": 1, "bull_supply": 2}
    },
    "rules": [{"seat": 1, "options_include": "take A"}],
    "expect": {
      "lens": {"players": {"1": {"hand": 4}}},
      "players": {"1": {"hand_size": 4}}
    }
  },
  {
    "name": "After a take the player restarts the pile with one card from hand",
    "rule": "R10",
    "players": 3,
    "seed": 13,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [1, 20, 30], "hand_size": 3, "bulls": 0}},
      "game": {"pile_a": [12, 13], "pile_b": [33], "pile_c": [35], "active_seat": 1, "bull_supply": 2}
    },
    "rules": [{"seat": 1, "options_include": "take A"}],
    "expect": {
      "lens": {"game": {"pile_a": 1}},
      "game": {"pile_b": [33], "pile_c": [35]},
      "players": {"1": {"hand_size": 4}}
    }
  },
  {
    "name": "Taking a 3-card pile gives the taker a bull from the supply",
    "rule": "R11",
    "players": 3,
    "seed": 14,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [1, 20, 30], "hand_size": 3, "bulls": 0}},
      "game": {"pile_a": [12, 13, 14], "pile_b": [33], "pile_c": [35], "active_seat": 1, "bull_supply": 2}
    },
    "rules": [{"seat": 1, "options_include": "take A"}],
    "expect": {
      "lens": {"game": {"pile_a": 1}},
      "game": {"bull_supply": 1},
      "players": {"1": {"bulls": 1, "hand_size": 5}}
    }
  },
  {
    "name": "Empty supply: the taker steals from the tied opponent first after it in seat order",
    "rule": "R12",
    "players": 3,
    "seed": 15,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": [1, 20, 30], "hand_size": 3, "bulls": 0},
        "2": {"bulls": 1},
        "3": {"bulls": 1}
      },
      "game": {"pile_a": [12, 13, 14], "pile_b": [33], "pile_c": [35], "active_seat": 1, "bull_supply": 0}
    },
    "rules": [{"seat": 1, "options_include": "take A"}],
    "expect": {
      "game": {"bull_supply": 0},
      "players": {"1": {"bulls": 1, "hand_size": 5}, "2": {"bulls": 0}, "3": {"bulls": 1}}
    }
  },
  {
    "name": "Empty supply: the taker steals from the opponent holding the most bulls",
    "rule": "R12",
    "players": 3,
    "seed": 16,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": [1, 20, 30], "hand_size": 3, "bulls": 0},
        "2": {"bulls": 1},
        "3": {"bulls": 2}
      },
      "game": {"pile_a": [12, 13, 14], "pile_b": [33], "pile_c": [35], "active_seat": 1, "bull_supply": 0}
    },
    "rules": [{"seat": 1, "options_include": "take A"}],
    "expect": {
      "game": {"bull_supply": 0},
      "players": {"1": {"bulls": 1}, "2": {"bulls": 1}, "3": {"bulls": 1}}
    }
  },
  {
    "name": "Empty supply and no opponent holds a bull: nothing changes",
    "rule": "R12",
    "players": 3,
    "seed": 17,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": [1, 20, 30], "hand_size": 3, "bulls": 0},
        "2": {"bulls": 0},
        "3": {"bulls": 0}
      },
      "game": {"pile_a": [12, 13, 14], "pile_b": [33], "pile_c": [35], "active_seat": 1, "bull_supply": 0}
    },
    "rules": [{"seat": 1, "options_include": "take A"}],
    "expect": {
      "game": {"bull_supply": 0},
      "players": {"1": {"bulls": 0, "hand_size": 5}, "2": {"bulls": 0}, "3": {"bulls": 0}}
    }
  },
  {
    "name": "Taking a 2-card pile moves no bull",
    "rule": "R13",
    "players": 3,
    "seed": 18,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": [1, 20, 30], "hand_size": 3, "bulls": 0},
        "2": {"bulls": 0},
        "3": {"bulls": 0}
      },
      "game": {"pile_a": [12, 13], "pile_b": [33], "pile_c": [35], "active_seat": 1, "bull_supply": 2}
    },
    "rules": [{"seat": 1, "options_include": "take A"}],
    "expect": {
      "game": {"bull_supply": 2},
      "players": {"1": {"bulls": 0, "hand_size": 4}, "2": {"bulls": 0}, "3": {"bulls": 0}}
    }
  },
  {
    "name": "A player with a legal play may still take a pile",
    "rule": "R15",
    "players": 3,
    "seed": 19,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [1, 13, 20], "hand_size": 3, "bulls": 0}},
      "game": {"pile_a": [12], "pile_b": [30], "pile_c": [35], "active_seat": 1, "bull_supply": 2}
    },
    "rules": [{"seat": 1, "options_include": "take B"}],
    "expect": {
      "offered": [
        {"seat": 1, "option": "play 13 on A"},
        {"seat": 1, "option": "take A"},
        {"seat": 1, "option": "take B"},
        {"seat": 1, "option": "take C"}
      ],
      "lens": {"game": {"pile_b": 1}},
      "game": {"pile_a": [12], "pile_c": [35], "bull_supply": 2},
      "players": {"1": {"hand_size": 3, "bulls": 0}}
    }
  },
  {
    "name": "Seat 1 empties its hand; seats 2 and 3 still play before the game ends",
    "rule": "R16",
    "players": 3,
    "seed": 20,
    "given": {
      "players": {
        "1": {"hand": [13], "hand_size": 1, "bulls": 0},
        "2": {"hand": [14, 20], "hand_size": 2, "bulls": 0},
        "3": {"hand": [15, 30], "hand_size": 2, "bulls": 0}
      },
      "game": {"pile_a": [12], "pile_b": [33], "pile_c": [35], "active_seat": 1, "cycle": 0, "max_cycles": 12, "bull_supply": 2}
    },
    "rules": [
      {"seat": 1, "options_include": "play 13 on A"},
      {"seat": 2, "options_include": "play 14 on A"},
      {"seat": 3, "options_include": "play 15 on A"}
    ],
    "expect": {
      "winner": 1,
      "standings": {"1": 0, "2": -3, "3": -3},
      "players": {
        "1": {"hand_size": 0, "penalty": 0},
        "2": {"hand_size": 1, "penalty": 3},
        "3": {"hand_size": 1, "penalty": 3}
      },
      "game": {"ending_triggered": true, "pile_a": [12, 13, 14, 15], "cycle": 1}
    }
  },
  {
    "name": "With 3 players the game ends after 12 full cycles",
    "rule": "R17",
    "players": 3,
    "seed": 21,
    "given": {
      "players": {
        "1": {"hand": [10, 20, 30], "hand_size": 3, "bulls": 0},
        "2": {"hand": [5, 15], "hand_size": 2, "bulls": 0},
        "3": {"hand": [7, 11, 13], "hand_size": 3, "bulls": 0}
      },
      "game": {"pile_a": [12], "pile_b": [24], "pile_c": [26], "active_seat": 3, "cycle": 11, "max_cycles": 12, "bull_supply": 2}
    },
    "rules": [{"seat": 3, "options_include": "play 13 on A"}],
    "expect": {
      "winner": 3,
      "standings": {"1": -9, "2": -4, "3": -2},
      "players": {"1": {"penalty": 9}, "2": {"penalty": 4}, "3": {"penalty": 2, "hand_size": 2}},
      "game": {"cycle": 12, "ending_triggered": false}
    }
  },
  {
    "name": "A player who empties its hand on the last turn has penalty 0 and wins",
    "rule": "R18",
    "players": 3,
    "seed": 22,
    "given": {
      "players": {
        "1": {"hand": [10], "hand_size": 1, "bulls": 0},
        "2": {"hand": [5], "hand_size": 1, "bulls": 0},
        "3": {"hand": [13], "hand_size": 1, "bulls": 0}
      },
      "game": {"pile_a": [12], "pile_b": [24], "pile_c": [26], "active_seat": 3, "cycle": 3, "max_cycles": 12, "bull_supply": 2}
    },
    "rules": [{"seat": 3, "options_include": "play 13 on A"}],
    "expect": {
      "winner": 3,
      "standings": {"1": -3, "2": -2, "3": 0},
      "players": {"1": {"penalty": 3}, "2": {"penalty": 2}, "3": {"penalty": 0, "hand_size": 0}},
      "game": {"ending_triggered": true}
    }
  },
  {
    "name": "Players tied for the lowest penalty share the win",
    "rule": "R19",
    "players": 3,
    "seed": 23,
    "given": {
      "players": {
        "1": {"hand": [4, 7], "hand_size": 2, "bulls": 0},
        "2": {"hand": [10], "hand_size": 1, "bulls": 0},
        "3": {"hand": [13, 8, 9], "hand_size": 3, "bulls": 0}
      },
      "game": {"pile_a": [12], "pile_b": [24], "pile_c": [26], "active_seat": 3, "cycle": 11, "max_cycles": 12, "bull_supply": 2}
    },
    "rules": [{"seat": 3, "options_include": "play 13 on A"}],
    "expect": {
      "winner": [1, 3],
      "standings": {"1": -2, "2": -3, "3": -2},
      "players": {"1": {"penalty": 2}, "2": {"penalty": 3}, "3": {"penalty": 2}}
    }
  },
  {
    "name": "After a take, the public piles, hand_size and bulls show the result",
    "rule": "R20",
    "players": 3,
    "seed": 24,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [1, 20, 30], "hand_size": 3, "bulls": 0}},
      "game": {"pile_a": [33], "pile_b": [12, 13, 14], "pile_c": [35], "active_seat": 1, "bull_supply": 2}
    },
    "rules": [{"seat": 1, "options_include": "take B"}],
    "expect": {
      "lens": {"game": {"pile_b": 1}},
      "game": {"pile_a": [33], "pile_c": [35], "bull_supply": 1},
      "players": {"1": {"hand_size": 5, "bulls": 1}}
    }
  }
]
```

Why it was refused: scenario 1: needs `rules` (what each seat answers, by option name); scenario 2: needs `rules` (what each seat answers, by option name); scenario 3: needs `rules` (what each seat answers, by option name); scenario 4: needs `rules` (what each seat answers, by option name)
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
[
  {
    "name": "Setup with 4 players: 6 cards per hand, 1 card per pile, 13 set aside (checked after seat 1 takes a 1-card pile and restarts it)",
    "rule": "R1",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "rules": [{"seat": 1, "options_include": "take A"}],
    "expect": {
      "lens": {
        "game": {"pile_a": 1, "pile_b": 1, "pile_c": 1, "set_aside": 13},
        "players": {"1": {"hand": 6}, "2": {"hand": 6}, "3": {"hand": 6}, "4": {"hand": 6}}
      },
      "players": {"1": {"hand_size": 6}, "2": {"hand_size": 6}, "3": {"hand_size": 6}, "4": {"hand_size": 6}}
    }
  },
  {
    "name": "Setup with 3 players: 6 cards per hand, 1 card per pile, 19 set aside (checked after seat 1 takes a 1-card pile and restarts it)",
    "rule": "R1",
    "players": 3,
    "seed": 2,
    "rounds": 1,
    "rules": [{"seat": 1, "options_include": "take A"}],
    "expect": {
      "lens": {
        "game": {"pile_a": 1, "pile_b": 1, "pile_c": 1, "set_aside": 19},
        "players": {"1": {"hand": 6}, "2": {"hand": 6}, "3": {"hand": 6}}
      },
      "players": {"1": {"hand_size": 6}, "2": {"hand_size": 6}, "3": {"hand_size": 6}}
    }
  },
  {
    "name": "Bull supply starts at 3 with 4 players, nobody holds bulls (a 1-card take moves no bull)",
    "rule": "R3",
    "players": 4,
    "seed": 3,
    "rounds": 1,
    "rules": [{"seat": 1, "options_include": "take A"}],
    "expect": {
      "game": {"bull_supply": 3, "cycle": 0, "ending_triggered": false},
      "players": {"1": {"bulls": 0}, "2": {"bulls": 0}, "3": {"bulls": 0}, "4": {"bulls": 0}}
    }
  },
  {
    "name": "Bull supply starts at 2 with 3 players (a 1-card take moves no bull)",
    "rule": "R3",
    "players": 3,
    "seed": 4,
    "rounds": 1,
    "rules": [{"seat": 1, "options_include": "take A"}],
    "expect": {
      "game": {"bull_supply": 2, "cycle": 0, "ending_triggered": false},
      "players": {"1": {"bulls": 0}, "2": {"bulls": 0}, "3": {"bulls": 0}}
    }
  },
  {
    "name": "Ox-heads at the end: multiples of 10 count 3, other multiples of 5 count 2, the rest 1",
    "rule": "R2",
    "players": 4,
    "seed": 5,
    "given": {
      "players": {
        "1": {"hand": [10, 20], "hand_size": 2, "bulls": 0},
        "2": {"hand": [5, 15, 1], "hand_size": 3, "bulls": 0},
        "3": {"hand": [2, 3, 4], "hand_size": 3, "bulls": 0},
        "4": {"hand": [13, 7, 35], "hand_size": 3, "bulls": 0}
      },
      "game": {"pile_a": [12], "pile_b": [24], "pile_c": [26], "active_seat": 4, "cycle": 9, "max_cycles": 10, "bull_supply": 3}
    },
    "rules": [{"seat": 4, "options_include": "play 13 on A"}],
    "expect": {
      "winner": [3, 4],
      "standings": {"1": -6, "2": -5, "3": -3, "4": -3},
      "players": {"1": {"penalty": 6}, "2": {"penalty": 5}, "3": {"penalty": 3}, "4": {"penalty": 3}},
      "game": {"cycle": 10, "pile_a": [12, 13]}
    }
  },
  {
    "name": "Legal plays on 37 wrap around: 38, 40 and 3 offered, 36, 4 and 10 not",
    "rule": "R4",
    "players": 3,
    "seed": 6,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [38, 3, 4, 36, 40, 10], "hand_size": 6, "bulls": 0}},
      "game": {"pile_a": [37], "pile_b": [12], "pile_c": [20], "active_seat": 1}
    },
    "rules": [{"seat": 1, "options_include": "play 3 on A"}],
    "expect": {
      "offered": [
        {"seat": 1, "option": "play 38 on A"},
        {"seat": 1, "option": "play 40 on A"},
        {"seat": 1, "option": "play 3 on A"}
      ],
      "not_offered": [
        {"seat": 1, "option": "play 4 on A"},
        {"seat": 1, "option": "play 36 on A"},
        {"seat": 1, "option": "play 10 on A"},
        {"seat": 1, "option": "play 10 on B"},
        {"seat": 1, "option": "play 38 on C"}
      ],
      "game": {"pile_a": [37, 3]},
      "players": {"1": {"hand_size": 5}}
    }
  },
  {
    "name": "Legal plays on 12 are 13 to 18: 18 offered, 19 and 11 not",
    "rule": "R4",
    "players": 3,
    "seed": 7,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [18, 19, 11], "hand_size": 3, "bulls": 0}},
      "game": {"pile_a": [12], "pile_b": [30], "pile_c": [32], "active_seat": 1}
    },
    "rules": [{"seat": 1, "options_include": "play 18 on A"}],
    "expect": {
      "offered": [{"seat": 1, "option": "play 18 on A"}],
      "not_offered": [{"seat": 1, "option": "play 19 on A"}, {"seat": 1, "option": "play 11 on A"}],
      "game": {"pile_a": [12, 18]},
      "players": {"1": {"hand_size": 2}}
    }
  },
  {
    "name": "Playing a card moves it to the top of the pile and hand_size drops by 1",
    "rule": "R5",
    "players": 3,
    "seed": 8,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [13, 25, 30], "hand_size": 3, "bulls": 0}},
      "game": {"pile_a": [12], "pile_b": [1], "pile_c": [5], "active_seat": 1}
    },
    "rules": [{"seat": 1, "options_include": "play 13 on A"}],
    "expect": {
      "game": {"pile_a": [12, 13], "pile_b": [1], "pile_c": [5]},
      "players": {"1": {"hand_size": 2, "bulls": 0}}
    }
  },
  {
    "name": "With 1 bull a player may add one extra legal card on the same pile",
    "rule": "R6",
    "players": 3,
    "seed": 9,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [13, 15, 30], "hand_size": 3, "bulls": 1}},
      "game": {"pile_a": [12], "pile_b": [2], "pile_c": [22], "active_seat": 1, "bull_supply": 1}
    },
    "rules": [
      {"seat": 1, "options_include": "play 13 on A"},
      {"seat": 1, "options_include": 15}
    ],
    "expect": {
      "offered": [{"seat": 1, "option": "stop"}],
      "game": {"pile_a": [12, 13, 15]},
      "players": {"1": {"hand_size": 1, "bulls": 1}}
    }
  },
  {
    "name": "With 2 bulls a player may add two extra legal cards on the same pile",
    "rule": "R7",
    "players": 3,
    "seed": 10,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [13, 15, 17, 30], "hand_size": 4, "bulls": 2}},
      "game": {"pile_a": [12], "pile_b": [2], "pile_c": [22], "active_seat": 1, "bull_supply": 0}
    },
    "rules": [
      {"seat": 1, "options_include": "play 13 on A"},
      {"seat": 1, "options_include": 15},
      {"seat": 1, "options_include": 17}
    ],
    "expect": {
      "game": {"pile_a": [12, 13, 15, 17]},
      "players": {"1": {"hand_size": 1, "bulls": 2}}
    }
  },
  {
    "name": "Using bulls for extra cards does not spend them or return them to the supply",
    "rule": "R8",
    "players": 3,
    "seed": 11,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [13, 15, 30], "hand_size": 3, "bulls": 1}},
      "game": {"pile_a": [12], "pile_b": [2], "pile_c": [22], "active_seat": 1, "bull_supply": 1}
    },
    "rules": [
      {"seat": 1, "options_include": "play 13 on A"},
      {"seat": 1, "options_include": 15}
    ],
    "expect": {
      "game": {"bull_supply": 1, "pile_a": [12, 13, 15]},
      "players": {"1": {"bulls": 1, "hand_size": 1}}
    }
  },
  {
    "name": "Taking a 2-card pile adds both cards to the hand",
    "rule": "R9",
    "players": 3,
    "seed": 12,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [1, 20, 30], "hand_size": 3, "bulls": 0}},
      "game": {"pile_a": [12, 13], "pile_b": [33], "pile_c": [35], "active_seat": 1, "bull_supply": 2}
    },
    "rules": [{"seat": 1, "options_include": "take A"}],
    "expect": {
      "lens": {"players": {"1": {"hand": 4}}},
      "players": {"1": {"hand_size": 4}}
    }
  },
  {
    "name": "After a take the player restarts the pile with one card from hand",
    "rule": "R10",
    "players": 3,
    "seed": 13,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [1, 20, 30], "hand_size": 3, "bulls": 0}},
      "game": {"pile_a": [12, 13], "pile_b": [33], "pile_c": [35], "active_seat": 1, "bull_supply": 2}
    },
    "rules": [{"seat": 1, "options_include": "take A"}],
    "expect": {
      "lens": {"game": {"pile_a": 1}},
      "game": {"pile_b": [33], "pile_c": [35]},
      "players": {"1": {"hand_size": 4}}
    }
  },
  {
    "name": "Taking a 3-card pile gives the taker a bull from the supply",
    "rule": "R11",
    "players": 3,
    "seed": 14,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [1, 20, 30], "hand_size": 3, "bulls": 0}},
      "game": {"pile_a": [12, 13, 14], "pile_b": [33], "pile_c": [35], "active_seat": 1, "bull_supply": 2}
    },
    "rules": [{"seat": 1, "options_include": "take A"}],
    "expect": {
      "lens": {"game": {"pile_a": 1}},
      "game": {"bull_supply": 1},
      "players": {"1": {"bulls": 1, "hand_size": 5}}
    }
  },
  {
    "name": "Empty supply: the taker steals from the tied opponent first after it in seat order",
    "rule": "R12",
    "players": 3,
    "seed": 15,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": [1, 20, 30], "hand_size": 3, "bulls": 0},
        "2": {"bulls": 1},
        "3": {"bulls": 1}
      },
      "game": {"pile_a": [12, 13, 14], "pile_b": [33], "pile_c": [35], "active_seat": 1, "bull_supply": 0}
    },
    "rules": [{"seat": 1, "options_include": "take A"}],
    "expect": {
      "game": {"bull_supply": 0},
      "players": {"1": {"bulls": 1, "hand_size": 5}, "2": {"bulls": 0}, "3": {"bulls": 1}}
    }
  },
  {
    "name": "Empty supply: the taker steals from the opponent holding the most bulls",
    "rule": "R12",
    "players": 3,
    "seed": 16,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": [1, 20, 30], "hand_size": 3, "bulls": 0},
        "2": {"bulls": 1},
        "3": {"bulls": 2}
      },
      "game": {"pile_a": [12, 13, 14], "pile_b": [33], "pile_c": [35], "active_seat": 1, "bull_supply": 0}
    },
    "rules": [{"seat": 1, "options_include": "take A"}],
    "expect": {
      "game": {"bull_supply": 0},
      "players": {"1": {"bulls": 1}, "2": {"bulls": 1}, "3": {"bulls": 1}}
    }
  },
  {
    "name": "Empty supply and no opponent holds a bull: nothing changes",
    "rule": "R12",
    "players": 3,
    "seed": 17,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": [1, 20, 30], "hand_size": 3, "bulls": 0},
        "2": {"bulls": 0},
        "3": {"bulls": 0}
      },
      "game": {"pile_a": [12, 13, 14], "pile_b": [33], "pile_c": [35], "active_seat": 1, "bull_supply": 0}
    },
    "rules": [{"seat": 1, "options_include": "take A"}],
    "expect": {
      "game": {"bull_supply": 0},
      "players": {"1": {"bulls": 0, "hand_size": 5}, "2": {"bulls": 0}, "3": {"bulls": 0}}
    }
  },
  {
    "name": "Taking a 2-card pile moves no bull",
    "rule": "R13",
    "players": 3,
    "seed": 18,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": [1, 20, 30], "hand_size": 3, "bulls": 0},
        "2": {"bulls": 0},
        "3": {"bulls": 0}
      },
      "game": {"pile_a": [12, 13], "pile_b": [33], "pile_c": [35], "active_seat": 1, "bull_supply": 2}
    },
    "rules": [{"seat": 1, "options_include": "take A"}],
    "expect": {
      "game": {"bull_supply": 2},
      "players": {"1": {"bulls": 0, "hand_size": 4}, "2": {"bulls": 0}, "3": {"bulls": 0}}
    }
  },
  {
    "name": "A player with a legal play may still take a pile",
    "rule": "R15",
    "players": 3,
    "seed": 19,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [1, 13, 20], "hand_size": 3, "bulls": 0}},
      "game": {"pile_a": [12], "pile_b": [30], "pile_c": [35], "active_seat": 1, "bull_supply": 2}
    },
    "rules": [{"seat": 1, "options_include": "take B"}],
    "expect": {
      "offered": [
        {"seat": 1, "option": "play 13 on A"},
        {"seat": 1, "option": "take A"},
        {"seat": 1, "option": "take B"},
        {"seat": 1, "option": "take C"}
      ],
      "lens": {"game": {"pile_b": 1}},
      "game": {"pile_a": [12], "pile_c": [35], "bull_supply": 2},
      "players": {"1": {"hand_size": 3, "bulls": 0}}
    }
  },
  {
    "name": "Seat 1 empties its hand; seats 2 and 3 still play before the game ends",
    "rule": "R16",
    "players": 3,
    "seed": 20,
    "given": {
      "players": {
        "1": {"hand": [13], "hand_size": 1, "bulls": 0},
        "2": {"hand": [14, 20], "hand_size": 2, "bulls": 0},
        "3": {"hand": [15, 30], "hand_size": 2, "bulls": 0}
      },
      "game": {"pile_a": [12], "pile_b": [33], "pile_c": [35], "active_seat": 1, "cycle": 0, "max_cycles": 12, "bull_supply": 2}
    },
    "rules": [
      {"seat": 1, "options_include": "play 13 on A"},
      {"seat": 2, "options_include": "play 14 on A"},
      {"seat": 3, "options_include": "play 15 on A"}
    ],
    "expect": {
      "winner": 1,
      "standings": {"1": 0, "2": -3, "3": -3},
      "players": {
        "1": {"hand_size": 0, "penalty": 0},
        "2": {"hand_size": 1, "penalty": 3},
        "3": {"hand_size": 1, "penalty": 3}
      },
      "game": {"ending_triggered": true, "pile_a": [12, 13, 14, 15], "cycle": 1}
    }
  },
  {
    "name": "With 3 players the game ends after 12 full cycles",
    "rule": "R17",
    "players": 3,
    "seed": 21,
    "given": {
      "players": {
        "1": {"hand": [10, 20, 30], "hand_size": 3, "bulls": 0},
        "2": {"hand": [5, 15], "hand_size": 2, "bulls": 0},
        "3": {"hand": [7, 11, 13], "hand_size": 3, "bulls": 0}
      },
      "game": {"pile_a": [12], "pile_b": [24], "pile_c": [26], "active_seat": 3, "cycle": 11, "max_cycles": 12, "bull_supply": 2}
    },
    "rules": [{"seat": 3, "options_include": "play 13 on A"}],
    "expect": {
      "winner": 3,
      "standings": {"1": -9, "2": -4, "3": -2},
      "players": {"1": {"penalty": 9}, "2": {"penalty": 4}, "3": {"penalty": 2, "hand_size": 2}},
      "game": {"cycle": 12, "ending_triggered": false}
    }
  },
  {
    "name": "A player who empties its hand on the last turn has penalty 0 and wins",
    "rule": "R18",
    "players": 3,
    "seed": 22,
    "given": {
      "players": {
        "1": {"hand": [10], "hand_size": 1, "bulls": 0},
        "2": {"hand": [5], "hand_size": 1, "bulls": 0},
        "3": {"hand": [13], "hand_size": 1, "bulls": 0}
      },
      "game": {"pile_a": [12], "pile_b": [24], "pile_c": [26], "active_seat": 3, "cycle": 3, "max_cycles": 12, "bull_supply": 2}
    },
    "rules": [{"seat": 3, "options_include": "play 13 on A"}],
    "expect": {
      "winner": 3,
      "standings": {"1": -3, "2": -2, "3": 0},
      "players": {"1": {"penalty": 3}, "2": {"penalty": 2}, "3": {"penalty": 0, "hand_size": 0}},
      "game": {"ending_triggered": true}
    }
  },
  {
    "name": "Players tied for the lowest penalty share the win",
    "rule": "R19",
    "players": 3,
    "seed": 23,
    "given": {
      "players": {
        "1": {"hand": [4, 7], "hand_size": 2, "bulls": 0},
        "2": {"hand": [10], "hand_size": 1, "bulls": 0},
        "3": {"hand": [13, 8, 9], "hand_size": 3, "bulls": 0}
      },
      "game": {"pile_a": [12], "pile_b": [24], "pile_c": [26], "active_seat": 3, "cycle": 11, "max_cycles": 12, "bull_supply": 2}
    },
    "rules": [{"seat": 3, "options_include": "play 13 on A"}],
    "expect": {
      "winner": [1, 3],
      "standings": {"1": -2, "2": -3, "3": -2},
      "players": {"1": {"penalty": 2}, "2": {"penalty": 3}, "3": {"penalty": 2}}
    }
  },
  {
    "name": "After a take, the public piles, hand_size and bulls show the result",
    "rule": "R20",
    "players": 3,
    "seed": 24,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [1, 20, 30], "hand_size": 3, "bulls": 0}},
      "game": {"pile_a": [33], "pile_b": [12, 13, 14], "pile_c": [35], "active_seat": 1, "bull_supply": 2}
    },
    "rules": [{"seat": 1, "options_include": "take B"}],
    "expect": {
      "lens": {"game": {"pile_b": 1}},
      "game": {"pile_a": [33], "pile_c": [35], "bull_supply": 1},
      "players": {"1": {"hand_size": 5, "bulls": 1}}
    }
  }
]
```
````
