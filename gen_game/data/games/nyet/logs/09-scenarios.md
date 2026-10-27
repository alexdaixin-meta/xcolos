# 09 scenarios

- time: 2026-10-27T18:06:30+00:00 (99.1s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 f767166b051c0cbe, reply sha256 53caeebcd4928965

## Sent

````
SPEC:
{
  "name": "Nyet! Trio (Widow edition, compact)",
  "summary": "Three players veto trump and choose who goes Lone, then play 5 tricks per deal over 6 deals. The Lone takes the face-up Widow and scores 2 per trick won; the other two, the Pair, each score 1 per trick their side wins.",
  "players": {
    "min": 3,
    "max": 3,
    "suggested": 3
  },
  "parameters": {
    "players": 3,
    "colours": 4,
    "ranks_per_colour": 6,
    "deck_size": 24,
    "hand_size": 5,
    "widow_cards": 1,
    "set_aside_cards": 8,
    "lone_hand_size": 6,
    "total_rounds": 36,
    "deals": 6,
    "rounds_per_deal": 6,
    "veto_rounds_per_deal": 1,
    "tricks_per_deal": 5,
    "trump_boxes": 4,
    "lone_boxes": 3,
    "tokens_per_deal": 3,
    "max_lone_tokens_per_deal": 1,
    "lone_trick_points": 2,
    "lone_trick_count_gain": 1,
    "pair_trick_points_each": 1,
    "lone_cards_kept_back": 1,
    "trump_strength_bonus": 200,
    "led_strength_bonus": 100,
    "rank_weight_score": 10000,
    "rank_weight_lone_tricks": 100
  },
  "attributes": {
    "player": [
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "points scored",
        "observable": true
      },
      {
        "key": "lone_tricks",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "tricks won while Lone (first tie-break)",
        "observable": true
      },
      {
        "key": "last_win",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "round number of this player's most recent trick win, 0 if none (second tie-break)",
        "observable": true
      },
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "private hand of cards such as 'Red 3'",
        "observable": false
      },
      {
        "key": "role",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "'lone' or 'pair' for the current deal",
        "observable": false
      },
      {
        "key": "played_colour",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "colour of the card played to the current trick",
        "observable": false
      },
      {
        "key": "played_rank",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "rank (1 to 6) of the card played to the current trick",
        "observable": false
      },
      {
        "key": "strength",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "scratch value: strength of the card this player played to the current trick, worked out from the face-up card, so it reveals nothing hidden",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "current round, 1 to 36",
        "observable": true
      },
      {
        "key": "deal",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "current deal, 1 to 6",
        "observable": false
      },
      {
        "key": "round_in_deal",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "1 is the veto round; 2 to 6 are trick rounds",
        "observable": false
      },
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "undealt cards; after a deal it holds the 8 set-aside cards, which are never revealed",
        "observable": false
      },
      {
        "key": "widow",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "the face-up Widow card for this deal",
        "observable": true
      },
      {
        "key": "trump_order",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "this deal's trump line, in order",
        "observable": false
      },
      {
        "key": "veto_order",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "this deal's First, Second and Third seats",
        "observable": false
      },
      {
        "key": "trump_tokens",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "trump boxes holding a Nyet token",
        "observable": false
      },
      {
        "key": "lone_tokens",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "lone boxes (First, Second, Third) holding a Nyet token",
        "observable": false
      },
      {
        "key": "trump",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "this deal's trump colour",
        "observable": true
      },
      {
        "key": "lone_seat",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "seat of this deal's Lone",
        "observable": true
      },
      {
        "key": "leader",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "seat that leads the current trick",
        "observable": false
      },
      {
        "key": "led_colour",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "colour of the leader's card in the current trick",
        "observable": false
      },
      {
        "key": "trick_winner",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "seat that won the last trick",
        "observable": true
      }
    ]
  },
  "setup": [
    "Seats 1, 2 and 3 are P1, P2 and P3; clockwise order is 1 -> 2 -> 3 -> 1.",
    "Every player's score, lone_tricks and last_win are set to 0.",
    "The full card set is 24 unique cards: Red, Yellow, Green and Blue, each numbered 1 to 6."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round += 1; deal = floor((round - 1) / 6) + 1; round_in_deal = ((round - 1) mod 6) + 1"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "when round_in_deal == 1: empty every hand (cards are discarded unseen); deck = all 24 cards; draw 5 cards at random from deck into each player's hand; draw 1 card at random from deck into widow (the remaining 8 stay in deck, hidden, as the set-aside cards); clear trump_tokens and lone_tokens; set trump_order (deals 1 and 5: Red, Yellow, Green, Blue; deals 2 and 6: Yellow, Green, Blue, Red; deal 3: Green, Blue, Red, Yellow; deal 4: Blue, Red, Yellow, Green); set veto_order (deals 1 and 4: 1, 2, 3; deals 2 and 5: 2, 3, 1; deals 3 and 6: 3, 1, 2); clear trump, lone_seat and roles"
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "when round_in_deal == 1: each player sees their own 5-card hand"
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "when round_in_deal == 1: announce deal, widow, trump_order (the TRUMP line), the LONE line boxes First/Second/Third with their seats from veto_order, and that the board is empty"
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "short text (non-binding talk)",
      "effect": "when round_in_deal == 1: all messages are collected at once and then broadcast {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"}"
    },
    {
      "action": "ask",
      "who": "seat veto_order[1] (First)",
      "answer": "one empty box: a TRUMP colour not in trump_tokens, or a LONE box (First/Second/Third) if lone_tokens is empty; never the last empty box of a line",
      "effect": "when round_in_deal == 1: append the chosen colour to trump_tokens, or the chosen lone box to lone_tokens; announce the placement"
    },
    {
      "action": "ask",
      "who": "seat veto_order[2] (Second)",
      "answer": "one empty box, under the same restrictions, seeing the tokens already placed",
      "effect": "when round_in_deal == 1: append to trump_tokens or lone_tokens; announce the placement"
    },
    {
      "action": "ask",
      "who": "seat veto_order[3] (Third)",
      "answer": "one empty box, under the same restrictions, seeing the tokens already placed",
      "effect": "when round_in_deal == 1: append to trump_tokens or lone_tokens; announce the placement"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "when round_in_deal == 1: trump = first colour in trump_order not in trump_tokens; lone_seat = the veto_order seat at the first of the First, Second, Third positions not in lone_tokens; role = 'lone' for lone_seat and 'pair' for the other two; append widow to the Lone's hand (6 cards); leader = lone_seat"
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "when round_in_deal == 1: announce trump, the Lone (lone_seat) and the Pair seats, and that the Lone leads the first trick"
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "when round_in_deal == 1: each player sees their own hand (the Lone now sees 6 cards)"
    },
    {
      "action": "ask",
      "who": "seat leader",
      "answer": "one card from own hand",
      "effect": "when round_in_deal >= 2: remove the card from hand; set played_colour and played_rank; led_colour = played_colour; announce the card"
    },
    {
      "action": "ask",
      "who": "seat clockwise after leader",
      "answer": "one card from own hand of colour led_colour if holding any, otherwise any card in hand",
      "effect": "when round_in_deal >= 2: remove the card from hand; set played_colour and played_rank; announce the card"
    },
    {
      "action": "ask",
      "who": "seat two clockwise after leader",
      "answer": "one card from own hand of colour led_colour if holding any, otherwise any card in hand",
      "effect": "when round_in_deal >= 2: remove the card from hand; set played_colour and played_rank; announce the card"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "when round_in_deal >= 2: for each player, strength = (played_colour == trump) * 200 + (played_colour == led_colour) * 100 + played_rank; trick_winner = the seat with the highest strength; if trick_winner == lone_seat then that player's score += 2 and lone_tricks += 1, otherwise each player with role 'pair' gets score += 1; trick_winner's last_win = round; leader = trick_winner"
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "when round_in_deal >= 2: announce the three cards played, trick_winner, and every score, lone_tricks and last_win"
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "when round_in_deal >= 2: each player sees their own remaining hand"
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "end the game if round >= 36, otherwise continue"
    }
  ],
  "ending": {
    "condition": "round >= 36",
    "rank_by": "you.score * 10000 + you.lone_tricks * 100 + you.last_win",
    "decided_by": "The highest score wins. A tie goes to the tied player with the most lone_tricks, then to the one with the highest last_win (who won a trick most recently). Players still level share the win, which is the draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game starts, then each of the 3 players has score 0, lone_tricks 0 and last_win 0."
    },
    {
      "id": "R2",
      "text": "When round is 1, 7, 13, 19, 25 or 31, then it is a veto round; every other round is a trick round."
    },
    {
      "id": "R3",
      "text": "When a veto round starts, then all hands are emptied, the 24-card deck is rebuilt, each player receives 5 private cards, 1 card becomes the public widow, and 8 cards remain hidden in deck."
    },
    {
      "id": "R4",
      "text": "When a veto round starts, then trump_tokens and lone_tokens are empty."
    },
    {
      "id": "R5",
      "text": "When deal is 1 or 4, then the veto order is seats 1, 2, 3; when deal is 2 or 5, it is 2, 3, 1; when deal is 3 or 6, it is 3, 1, 2."
    },
    {
      "id": "R6",
      "text": "When deal is 1 or 5, then trump_order is Red, Yellow, Green, Blue; when deal is 2 or 6, it is Yellow, Green, Blue, Red; when deal is 3, it is Green, Blue, Red, Yellow; when deal is 4, it is Blue, Red, Yellow, Green."
    },
    {
      "id": "R7",
      "text": "When the veto round talk happens, then all 3 players submit one short message at once, and all messages are shown to everyone only after all are in."
    },
    {
      "id": "R8",
      "text": "When a player places a Nyet token, then it goes on exactly one empty box, and the player sees all tokens already placed."
    },
    {
      "id": "R9",
      "text": "When lone_tokens already holds a token, then no further token may be placed on the LONE line this deal."
    },
    {
      "id": "R10",
      "text": "When a box is the last empty box of its line, then no token may be placed on it."
    },
    {
      "id": "R11",
      "text": "When all 3 tokens are placed, then trump is the first colour in trump_order without a token."
    },
    {
      "id": "R12",
      "text": "When all 3 tokens are placed, then the Lone is the seat of the first of First, Second, Third without a token, and the other two seats are the Pair."
    },
    {
      "id": "R13",
      "text": "When the Lone is chosen, then the widow is added to the Lone's hand, giving 6 cards, and the Lone leads the first trick."
    },
    {
      "id": "R14",
      "text": "When a trick is played, then the leader plays first, then the next seat clockwise, then the third seat, each seeing the cards already played."
    },
    {
      "id": "R15",
      "text": "When a player holds a card of led_colour, then they must play a card of led_colour; otherwise they may play any card in hand."
    },
    {
      "id": "R16",
      "text": "When any trump is played in a trick, then the highest trump wins; otherwise the highest card of led_colour wins."
    },
    {
      "id": "R17",
      "text": "When the Lone wins a trick, then the Lone's score rises by 2 and lone_tricks by 1."
    },
    {
      "id": "R18",
      "text": "When a Pair member wins a trick, then the score of each of the two Pair members rises by 1."
    },
    {
      "id": "R19",
      "text": "When a player wins a trick, then their last_win is set to the current round number and they lead the next trick of the deal."
    },
    {
      "id": "R20",
      "text": "When the 5th trick of a deal ends, then the Lone's 1 remaining card is never played or revealed and is discarded at the next shuffle."
    },
    {
      "id": "R21",
      "text": "When round 36 ends, then the game ends."
    },
    {
      "id": "R22",
      "text": "When the game ends, then the highest score wins; ties go to most lone_tricks, then highest last_win; players still tied share the win as a draw."
    }
  ],
  "offers": [
    {
      "question": "Veto talk",
      "who": "all three seats at once",
      "options": "a short free-text message"
    },
    {
      "question": "Nyet token placement (First, Second, Third in turn)",
      "who": "the seat at that position of veto_order",
      "options": "if lone_tokens is empty: each TRUMP colour not in trump_tokens plus each LONE box (First, Second, Third) not in lone_tokens, excluding any box that is the last empty one of its line; if lone_tokens has a token: only the TRUMP colours not in trump_tokens, excluding the last empty one"
    },
    {
      "question": "Lead a card",
      "who": "the leader",
      "options": "every card in the leader's hand"
    },
    {
      "question": "Follow to the trick",
      "who": "the second and third seats clockwise from the leader",
      "options": "if the seat holds a card of led_colour: only its cards of led_colour; otherwise every card in its hand"
    }
  ],
  "choices": [
    {
      "what": "3 players (min 3, max 3, suggested 3)",
      "why": "The designer fixed 3 seats. The game is one Lone against a Pair of two, and both the veto order and the LONE line have exactly 3 positions, so no other count works. The strategy is to veto colours and Lone positions to steer trump toward your own hand, and to judge whether to go Lone or force someone else into it."
    },
    {
      "what": "Talk is kept as a simultaneous poll with broadcast",
      "why": "The rules say all three write at once without seeing each other. The players disagree about trump and about who should be Lone, so talk gives them something to bluff and bargain over."
    },
    {
      "what": "Cards are text such as 'Red 3', handled through played_colour and played_rank",
      "why": "This lets the trick winner be found by arithmetic: strength = trump bonus 200 + led bonus 100 + rank."
    },
    {
      "what": "strength is a public scratch attribute",
      "why": "It is computed only from cards already played face up, so making it public reveals nothing; a player attribute may not be hidden from all."
    },
    {
      "what": "The 8 set-aside cards stay in the hidden deck list",
      "why": "They are never revealed or used, so the hidden deck can hold them."
    },
    {
      "what": "Tie-break encoded as score*10000 + lone_tricks*100 + last_win",
      "why": "lone_tricks is at most 30 and last_win at most 36, both under 100, so the order is strictly lexicographic. A full tie shares the win, which is the source's draw."
    }
  ],
  "simplifications": [
    {
      "what": "Veto-round and trick-round steps are one flat list, each step gated by a 'when' condition on round_in_deal",
      "why": "The engine has no branching blocks. Per-step conditions reproduce the alternation exactly."
    },
    {
      "what": "The 'Lone leads first' and 'winner leads next' rules are kept as a leader table attribute, and play order is addressed relative to the leader",
      "why": "The engine addresses seats by attribute rather than by a fixed rotation."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: score, lone_tricks, last_win; table: round, widow, trump, lone_seat, trick_winner.
````

## Reply

````
```json
[
  {
    "name": "At game start every seat has score 0, lone_tricks 0 and last_win 0",
    "rule": "R1",
    "players": 3,
    "rounds": 0,
    "expect": {
      "players": {
        "1": {"score": 0, "lone_tricks": 0, "last_win": 0},
        "2": {"score": 0, "lone_tricks": 0, "last_win": 0},
        "3": {"score": 0, "lone_tricks": 0, "last_win": 0}
      },
      "game": {"round": 0}
    }
  },
  {
    "name": "Round 1 is a veto round: tokens choose trump and Lone, no trick and no score",
    "rule": "R2",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": "Red"},
      {"seat": 2, "options_include": "Yellow"},
      {"seat": 3, "options_include": "First"}
    ],
    "expect": {
      "game": {"round": 1, "trump": "Green", "lone_seat": 2},
      "players": {
        "1": {"score": 0, "lone_tricks": 0, "last_win": 0},
        "2": {"score": 0, "lone_tricks": 0, "last_win": 0},
        "3": {"score": 0, "lone_tricks": 0, "last_win": 0}
      }
    }
  },
  {
    "name": "Round 7 is a veto round: old hands are emptied, 5 cards are dealt to each seat, the Lone gets 6 and the deck keeps 8",
    "rule": "R3",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round": 6},
      "players": {
        "1": {"hand": ["Red 1"], "score": 3},
        "2": {"hand": ["Red 2"], "score": 4},
        "3": {"hand": ["Red 3"], "score": 3}
      }
    },
    "rules": [
      {"seat": 2, "options_include": "Yellow"},
      {"seat": 3, "options_include": "Green"},
      {"seat": 1, "options_include": "First"}
    ],
    "expect": {
      "game": {"round": 7, "trump": "Blue", "lone_seat": 3},
      "lens": {"game": {"deck": 8}, "players": {"1": {"hand": 5}, "2": {"hand": 5}, "3": {"hand": 6}}},
      "players": {"1": {"score": 3}, "2": {"score": 4}, "3": {"score": 3}}
    }
  },
  {
    "name": "Tokens left over from a previous deal are cleared at the start of a veto round",
    "rule": "R4",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round": 30, "trump_tokens": ["Yellow", "Green"], "lone_tokens": ["First"]}
    },
    "rules": [
      {"seat": 3, "options_include": "First"},
      {"seat": 1, "options_include": "Yellow"},
      {"seat": 2, "options_include": "Green"}
    ],
    "expect": {
      "game": {"round": 31, "trump": "Blue", "lone_seat": 1},
      "offered": [{"seat": 3, "option": "Yellow"}, {"seat": 3, "option": "First"}, {"seat": 1, "option": "Yellow"}]
    }
  },
  {
    "name": "Deal 3 veto order is 3, 1, 2 (seat 3 places first and is the First Lone box)",
    "rule": "R5",
    "players": 3,
    "rounds": 1,
    "given": {"game": {"round": 12}},
    "rules": [
      {"seat": 3, "options_include": "Green"},
      {"seat": 1, "options_include": "Blue"},
      {"seat": 2, "options_include": "Second"}
    ],
    "expect": {"game": {"round": 13, "trump": "Red", "lone_seat": 3}}
  },
  {
    "name": "Deal 5 veto order is 2, 3, 1: a token on First makes seat 3 (Second) the Lone",
    "rule": "R5",
    "players": 3,
    "rounds": 1,
    "given": {"game": {"round": 24}},
    "rules": [
      {"seat": 2, "options_include": "Red"},
      {"seat": 3, "options_include": "Green"},
      {"seat": 1, "options_include": "First"}
    ],
    "expect": {"game": {"round": 25, "trump": "Yellow", "lone_seat": 3}}
  },
  {
    "name": "Deal 4 trump order is Blue, Red, Yellow, Green: vetoing Blue and Red gives Yellow",
    "rule": "R6",
    "players": 3,
    "rounds": 1,
    "given": {"game": {"round": 18}},
    "rules": [
      {"seat": 1, "options_include": "Third"},
      {"seat": 2, "options_include": "Blue"},
      {"seat": 3, "options_include": "Red"}
    ],
    "expect": {"game": {"round": 19, "trump": "Yellow", "lone_seat": 1}}
  },
  {
    "name": "Veto talk is collected and the veto round still completes",
    "rule": "R7",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": "Yellow"},
      {"seat": 2, "options_include": "Green"},
      {"seat": 3, "options_include": "Third"}
    ],
    "expect": {"game": {"round": 1, "trump": "Red", "lone_seat": 1}}
  },
  {
    "name": "A box that already holds a token is not offered again",
    "rule": "R8",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": "Red"},
      {"seat": 2, "options_include": "Yellow"},
      {"seat": 3, "options_include": "Second"}
    ],
    "expect": {
      "game": {"trump": "Green", "lone_seat": 1},
      "not_offered": [{"seat": 2, "option": "Red"}, {"seat": 3, "option": "Red"}, {"seat": 3, "option": "Yellow"}]
    }
  },
  {
    "name": "Once the LONE line holds a token, no other LONE box is offered",
    "rule": "R9",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": "First"},
      {"seat": 2, "options_include": "Red"},
      {"seat": 3, "options_include": "Yellow"}
    ],
    "expect": {
      "game": {"trump": "Green", "lone_seat": 2},
      "not_offered": [
        {"seat": 2, "option": "Second"}, {"seat": 2, "option": "Third"},
        {"seat": 3, "option": "Second"}, {"seat": 3, "option": "Third"}
      ]
    }
  },
  {
    "name": "With two trump boxes still empty, neither is withheld as a last box",
    "rule": "R10",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": "Red"},
      {"seat": 2, "options_include": "Yellow"},
      {"seat": 3, "options_include": "Green"}
    ],
    "expect": {
      "game": {"trump": "Blue", "lone_seat": 1},
      "offered": [{"seat": 3, "option": "Green"}, {"seat": 3, "option": "Blue"}]
    }
  },
  {
    "name": "Trump is the first colour of the line without a token (Yellow and Blue vetoed in deal 1 gives Red)",
    "rule": "R11",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": "Yellow"},
      {"seat": 2, "options_include": "Blue"},
      {"seat": 3, "options_include": "Second"}
    ],
    "expect": {"game": {"trump": "Red", "lone_seat": 1}}
  },
  {
    "name": "The Lone is the seat at the first LONE box without a token (Third vetoed gives seat 1)",
    "rule": "R12",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": "Red"},
      {"seat": 2, "options_include": "Third"},
      {"seat": 3, "options_include": "Yellow"}
    ],
    "expect": {"game": {"trump": "Green", "lone_seat": 1}}
  },
  {
    "name": "The Lone takes the widow and holds 6 cards; the Pair hold 5",
    "rule": "R13",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": "First"},
      {"seat": 2, "options_include": "Red"},
      {"seat": 3, "options_include": "Yellow"}
    ],
    "expect": {
      "game": {"lone_seat": 2, "trump": "Green"},
      "lens": {"players": {"1": {"hand": 5}, "2": {"hand": 6}, "3": {"hand": 5}}, "game": {"deck": 8}}
    }
  },
  {
    "name": "The leader plays first and sets the led colour; seat 3 leads Blue and seat 1's Blue 5 wins",
    "rule": "R14",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round": 1, "trump": "Green", "lone_seat": 2, "leader": 3},
      "players": {
        "1": {"role": "pair", "hand": ["Red 1", "Blue 5"]},
        "2": {"role": "lone", "hand": ["Yellow 6", "Yellow 2"]},
        "3": {"role": "pair", "hand": ["Blue 3", "Red 4"]}
      }
    },
    "rules": [
      {"seat": 3, "options_include": "Blue 3"},
      {"seat": 1, "options_include": "Blue 5"},
      {"seat": 2, "options_include": "Yellow 6"}
    ],
    "expect": {
      "game": {"round": 2, "trick_winner": 1},
      "players": {"1": {"score": 1, "last_win": 2}, "2": {"score": 0}, "3": {"score": 1}}
    }
  },
  {
    "name": "A seat holding the led colour must follow it",
    "rule": "R15",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round": 1, "trump": "Green", "lone_seat": 2, "leader": 2},
      "players": {
        "1": {"role": "pair", "hand": ["Red 6", "Yellow 1"]},
        "2": {"role": "lone", "hand": ["Red 5", "Green 1"]},
        "3": {"role": "pair", "hand": ["Red 2", "Blue 6"]}
      }
    },
    "rules": [
      {"seat": 2, "options_include": "Red 5"},
      {"seat": 3, "options_include": "Red 2"},
      {"seat": 1, "options_include": "Red 6"}
    ],
    "expect": {
      "offered": [{"seat": 3, "option": "Red 2"}],
      "not_offered": [{"seat": 3, "option": "Blue 6"}, {"seat": 1, "option": "Yellow 1"}],
      "game": {"trick_winner": 1}
    }
  },
  {
    "name": "A low trump beats the highest card of the led colour",
    "rule": "R16",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round": 1, "trump": "Green", "lone_seat": 2, "leader": 2},
      "players": {
        "1": {"role": "pair", "hand": ["Red 1"]},
        "2": {"role": "lone", "hand": ["Red 6"]},
        "3": {"role": "pair", "hand": ["Green 1", "Blue 6"]}
      }
    },
    "rules": [
      {"seat": 2, "options_include": "Red 6"},
      {"seat": 3, "options_include": "Green 1"},
      {"seat": 1, "options_include": "Red 1"}
    ],
    "expect": {
      "game": {"trick_winner": 3},
      "players": {"1": {"score": 1}, "2": {"score": 0, "lone_tricks": 0}, "3": {"score": 1, "last_win": 2}}
    }
  },
  {
    "name": "An off-colour non-trump card cannot win; the highest card of the led colour wins",
    "rule": "R16",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round": 1, "trump": "Green", "lone_seat": 2, "leader": 2},
      "players": {
        "1": {"role": "pair", "hand": ["Red 1"]},
        "2": {"role": "lone", "hand": ["Red 3"]},
        "3": {"role": "pair", "hand": ["Blue 6"]}
      }
    },
    "rules": [
      {"seat": 2, "options_include": "Red 3"},
      {"seat": 3, "options_include": "Blue 6"},
      {"seat": 1, "options_include": "Red 1"}
    ],
    "expect": {
      "game": {"trick_winner": 2},
      "players": {"2": {"score": 2, "lone_tricks": 1, "last_win": 2}, "1": {"score": 0}, "3": {"score": 0}}
    }
  },
  {
    "name": "The Lone wins a trick: +2 score and +1 lone_tricks",
    "rule": "R17",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round": 1, "trump": "Green", "lone_seat": 2, "leader": 2},
      "players": {
        "1": {"role": "pair", "hand": ["Red 1", "Yellow 1"]},
        "2": {"role": "lone", "hand": ["Red 5", "Green 1"]},
        "3": {"role": "pair", "hand": ["Red 2", "Blue 6"]}
      }
    },
    "rules": [
      {"seat": 2, "options_include": "Red 5"},
      {"seat": 3, "options_include": "Red 2"},
      {"seat": 1, "options_include": "Red 1"}
    ],
    "expect": {
      "game": {"trick_winner": 2},
      "players": {
        "1": {"score": 0, "lone_tricks": 0},
        "2": {"score": 2, "lone_tricks": 1, "last_win": 2},
        "3": {"score": 0, "lone_tricks": 0}
      }
    }
  },
  {
    "name": "A Pair member wins a trick: both Pair members gain 1, the Lone gains nothing",
    "rule": "R18",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round": 1, "trump": "Green", "lone_seat": 2, "leader": 2},
      "players": {
        "1": {"role": "pair", "hand": ["Red 6", "Yellow 1"]},
        "2": {"role": "lone", "hand": ["Red 5", "Green 1"]},
        "3": {"role": "pair", "hand": ["Red 2", "Blue 6"]}
      }
    },
    "rules": [
      {"seat": 2, "options_include": "Red 5"},
      {"seat": 3, "options_include": "Red 2"},
      {"seat": 1, "options_include": "Red 6"}
    ],
    "expect": {
      "game": {"trick_winner": 1},
      "players": {
        "1": {"score": 1, "lone_tricks": 0, "last_win": 2},
        "2": {"score": 0, "lone_tricks": 0, "last_win": 0},
        "3": {"score": 1, "lone_tricks": 0, "last_win": 0}
      }
    }
  },
  {
    "name": "The trick winner's last_win is the round and that seat leads the next trick",
    "rule": "R19",
    "players": 3,
    "rounds": 2,
    "given": {
      "game": {"round": 1, "trump": "Green", "lone_seat": 2, "leader": 2},
      "players": {
        "1": {"role": "pair", "hand": ["Red 6", "Blue 1"]},
        "2": {"role": "lone", "hand": ["Red 5", "Yellow 6"]},
        "3": {"role": "pair", "hand": ["Red 2", "Yellow 2"]}
      }
    },
    "rules": [
      {"seat": 2, "options_include": "Red 5"},
      {"seat": 3, "options_include": "Red 2"},
      {"seat": 1, "options_include": "Red 6"},
      {"seat": 1, "options_include": "Blue 1"},
      {"seat": 2, "options_include": "Yellow 6"},
      {"seat": 3, "options_include": "Yellow 2"}
    ],
    "expect": {
      "game": {"round": 3, "trick_winner": 1},
      "players": {
        "1": {"score": 2, "last_win": 3},
        "2": {"score": 0, "lone_tricks": 0, "last_win": 0},
        "3": {"score": 2, "last_win": 0}
      }
    }
  },
  {
    "name": "After the 5th trick the Lone still holds 1 unplayed card",
    "rule": "R20",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"round": 5, "trump": "Green", "lone_seat": 2, "leader": 2},
      "players": {
        "1": {"role": "pair", "hand": ["Red 1"]},
        "2": {"role": "lone", "hand": ["Red 5", "Blue 1"]},
        "3": {"role": "pair", "hand": ["Red 2"]}
      }
    },
    "rules": [
      {"seat": 2, "options_include": "Red 5"},
      {"seat": 3, "options_include": "Red 2"},
      {"seat": 1, "options_include": "Red 1"}
    ],
    "expect": {
      "game": {"round": 6, "trick_winner": 2},
      "lens": {"players": {"1": {"hand": 0}, "2": {"hand": 1}, "3": {"hand": 0}}},
      "players": {"2": {"score": 2, "lone_tricks": 1, "last_win": 6}}
    }
  },
  {
    "name": "The game ends after round 36 and the highest score wins",
    "rule": "R21",
    "players": 3,
    "given": {
      "game": {"round": 35, "trump": "Green", "lone_seat": 2, "leader": 2},
      "players": {
        "1": {"role": "pair", "hand": ["Red 1"], "score": 10, "lone_tricks": 0, "last_win": 20},
        "2": {"role": "lone", "hand": ["Red 5", "Blue 1"], "score": 10, "lone_tricks": 2, "last_win": 25},
        "3": {"role": "pair", "hand": ["Red 2"], "score": 5, "lone_tricks": 0, "last_win": 10}
      }
    },
    "rules": [
      {"seat": 2, "options_include": "Red 5"},
      {"seat": 3, "options_include": "Red 2"},
      {"seat": 1, "options_include": "Red 1"}
    ],
    "expect": {
      "winner": 2,
      "standings": {"1": 100020, "2": 120336, "3": 50010},
      "game": {"round": 36, "trick_winner": 2},
      "players": {"2": {"score": 12, "lone_tricks": 3, "last_win": 36}}
    }
  },
  {
    "name": "Tie on score and lone_tricks is broken by the most recent trick win",
    "rule": "R22",
    "players": 3,
    "given": {
      "game": {"round": 35, "trump": "Green", "lone_seat": 2, "leader": 2},
      "players": {
        "1": {"role": "pair", "hand": ["Red 1"], "score": 12, "lone_tricks": 3, "last_win": 30},
        "2": {"role": "lone", "hand": ["Red 5", "Blue 1"], "score": 10, "lone_tricks": 2, "last_win": 25},
        "3": {"role": "pair", "hand": ["Red 2"], "score": 11, "lone_tricks": 0, "last_win": 0}
      }
    },
    "rules": [
      {"seat": 2, "options_include": "Red 5"},
      {"seat": 3, "options_include": "Red 2"},
      {"seat": 1, "options_include": "Red 1"}
    ],
    "expect": {
      "winner": 2,
      "standings": {"1": 120330, "2": 120336, "3": 110000},
      "players": {
        "1": {"score": 12, "lone_tricks": 3, "last_win": 30},
        "2": {"score": 12, "lone_tricks": 3, "last_win": 36}
      }
    }
  },
  {
    "name": "Tie on score is broken by lone_tricks",
    "rule": "R22",
    "players": 3,
    "given": {
      "game": {"round": 35, "trump": "Green", "lone_seat": 2, "leader": 2},
      "players": {
        "1": {"role": "pair", "hand": ["Red 6"], "score": 9, "lone_tricks": 0, "last_win": 20},
        "2": {"role": "lone", "hand": ["Red 5", "Blue 1"], "score": 10, "lone_tricks": 4, "last_win": 25},
        "3": {"role": "pair", "hand": ["Red 2"], "score": 8, "lone_tricks": 0, "last_win": 10}
      }
    },
    "rules": [
      {"seat": 2, "options_include": "Red 5"},
      {"seat": 3, "options_include": "Red 2"},
      {"seat": 1, "options_include": "Red 6"}
    ],
    "expect": {
      "winner": 2,
      "standings": {"1": 100036, "2": 100425, "3": 90010},
      "players": {
        "1": {"score": 10, "last_win": 36},
        "2": {"score": 10, "lone_tricks": 4},
        "3": {"score": 9}
      }
    }
  }
]
```
````
