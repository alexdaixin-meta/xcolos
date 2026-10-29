# 04 scenarios

- time: 2026-10-28T02:26:50+00:00 (184.6s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 e942dec74da69dc3, reply sha256 29fd82db1372f99b

## Sent

````
SPEC:
{
  "name": "Trischettn Duel",
  "summary": "A two-player, no-trump trick-taking duel with a 24-card deck. It runs three deals of 12 tricks, with talon draws, declarations of sets, and scoring in thirds of a point.",
  "players": {
    "min": 2,
    "max": 2,
    "suggested": 2
  },
  "parameters": {
    "deck_size": 24,
    "suits": 4,
    "ranks_per_suit": 6,
    "hand_size": 6,
    "talon_size": 12,
    "tricks_per_deal": 12,
    "deals": 3,
    "total_tricks": 36,
    "talon_draw_tricks": 6,
    "ace_value": 3,
    "ten_value": 1,
    "nine_value": 1,
    "king_value": 1,
    "ober_value": 1,
    "unter_value": 1,
    "last_trick_bonus": 3,
    "thirds_per_deal": 35,
    "three_of_rank_points": 9,
    "four_of_rank_points": 12,
    "napoli_points": 9,
    "napoli_cards": 3,
    "rank_strength_ten": 6,
    "rank_strength_nine": 5,
    "rank_strength_ace": 4,
    "rank_strength_king": 3,
    "rank_strength_ober": 2,
    "rank_strength_unter": 1,
    "deal1_first_leader_seat": 1,
    "deal2_first_leader_seat": 2,
    "deal3_tie_first_leader_seat": 2
  },
  "attributes": {
    "player": [
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "Cards held, each written as text such as 'Ten of Hearts'.",
        "observable": false
      },
      {
        "key": "deal_points",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Thirds scored this deal from cards, the last trick and any declaration.",
        "observable": true
      },
      {
        "key": "match_total",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Thirds scored over all finished deals. This is the score.",
        "observable": true
      },
      {
        "key": "declared_this_deal",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "Whether this player has already declared in the current deal.",
        "observable": false
      },
      {
        "key": "drawn_hidden_card",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "The face-down talon card the trick loser just drew, which only that player sees.",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "Cards not yet dealt during dealing. It holds all 24 cards at the start of each deal.",
        "observable": false
      },
      {
        "key": "talon",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "Face-down talon cards in shuffled order. Drawing picks one at random.",
        "observable": false
      },
      {
        "key": "talon_up",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The face-up top card of the talon, or empty if there is none.",
        "observable": true
      },
      {
        "key": "talon_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Talon cards left, counting the face-up one.",
        "observable": false
      },
      {
        "key": "played_this_deal",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Every card played so far this deal.",
        "observable": true
      },
      {
        "key": "declared_cards_shown",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Cards shown by declarations this deal.",
        "observable": true
      },
      {
        "key": "deal_no",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The current deal, from 1 to 3.",
        "observable": false
      },
      {
        "key": "trick_in_deal",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Tricks completed in the current deal, from 0 to 12.",
        "observable": false
      },
      {
        "key": "tricks_played",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Tricks completed in the match, from 0 to 36.",
        "observable": false
      },
      {
        "key": "leader",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "The seat that leads the current trick.",
        "observable": false
      },
      {
        "key": "last_trick_winner",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The seat that won the previous trick of this deal, or 0 at the start of a deal.",
        "observable": false
      },
      {
        "key": "led_card",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The card the leader played this trick.",
        "observable": false
      },
      {
        "key": "follow_card",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The card the follower played this trick.",
        "observable": false
      },
      {
        "key": "trick_winner",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The seat that won the current trick.",
        "observable": false
      }
    ]
  },
  "setup": [
    "Seat 1 and seat 2 start with match_total 0.",
    "deal_no is 0, trick_in_deal is 0 and tricks_played is 0, so the first round begins by starting deal 1."
  ],
  "round": [
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "Only when trick_in_deal == 0 (start of a deal):\n- deal_no += 1.\n- deck = all 24 cards (Ten, Nine, Ace, King, Ober and Unter of Hearts, Bells, Leaves and Acorns).\n- Each hand = []. Then 6 times for each seat, move a random card from deck to that seat's hand.\n- talon = the remaining 12 cards. Move one random talon card to talon_up. talon_count = 12.\n- Each deal_points = 0 and each declared_this_deal = false.\n- played_this_deal = [], declared_cards_shown = [], last_trick_winner = 0.\n- leader = 1 if deal_no == 1. leader = 2 if deal_no == 2. If deal_no == 3: leader = 1 if seat 1 match_total < seat 2 match_total, otherwise 2.\n- Announce: 'Deal {deal_no} begins; the face-up talon card is {talon_up}; seat {leader} leads.'"
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player sees their own hand, talon_up, talon_count, every deal_points and match_total, played_this_deal and declared_cards_shown."
    },
    {
      "action": "ask",
      "who": "the leader (seat given by leader)",
      "answer": "declare or pass",
      "effect": "Asked only when all of these hold: trick_in_deal >= 1, last_trick_winner == leader, the leader's declared_this_deal is false, and the leader's declaration value is > 0.\n\nThe declaration value is the sum of these, over the hand:\n- For each rank of Ten, Nine and Ace: 12 if the hand holds 4 of that rank, 9 if it holds exactly 3, otherwise 0.\n- 9 for each suit whose Ten, Nine and Ace are all in hand."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "When the leader answered declare:\n- The leader's deal_points += declaration value.\n- The leader's declared_this_deal = true.\n- Append every card forming a qualifying set to declared_cards_shown.\n- Announce: 'Seat {leader} declares {value} thirds, showing {cards}.'"
    },
    {
      "action": "ask",
      "who": "the leader (seat given by leader)",
      "answer": "one card from the leader's hand",
      "effect": "led_card = chosen card. Remove it from the leader's hand and append it to played_this_deal. Announce: 'Seat {leader} leads {led_card}.'"
    },
    {
      "action": "ask",
      "who": "the follower (the seat that is not leader)",
      "answer": "one legal card from the follower's hand: a card of led_card's suit if any is held, otherwise any card",
      "effect": "follow_card = chosen card. Remove it from the follower's hand and append it to played_this_deal. Announce: 'Seat {follower} plays {follow_card}.'"
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "Decide and score the trick:\n- trick_winner = follower if follow_card has led_card's suit and a higher rank strength (Ten 6, Nine 5, Ace 4, King 3, Ober 2, Unter 1). Otherwise trick_winner = leader.\n- trick_in_deal += 1 and tricks_played += 1.\n- trick_winner's deal_points += value(led_card) + value(follow_card), where Ace = 3 and every other card = 1.\n- If trick_in_deal == 12, trick_winner's deal_points += 3.\n- last_trick_winner = trick_winner.\n- Announce: 'Seat {trick_winner} wins the trick.'"
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "Only when talon_count > 0:\n- Append talon_up to trick_winner's hand. talon_count -= 1.\n- Move one random talon card to the loser's hand and set the loser's drawn_hidden_card to it, seen only by the loser. talon_count -= 1.\n- If talon is not empty, move one random talon card to talon_up. Otherwise talon_up = ''.\n- Announce: 'Seat {trick_winner} takes the face-up card; the new face-up card is {talon_up}.'"
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "leader = trick_winner."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "Only when trick_in_deal == 12:\n- Each player's match_total += deal_points.\n- trick_in_deal = 0.\n- Announce: 'Deal {deal_no} over. Seat 1 has {match_total}, seat 2 has {match_total}.'"
    },
    {
      "action": "check",
      "who": "table",
      "answer": null,
      "effect": "End the game if tricks_played == 36, otherwise continue to the next round."
    }
  ],
  "ending": {
    "condition": "tricks_played == 36",
    "rank_by": "you.match_total",
    "decided_by": "After three deals, the player with the higher match total in thirds wins; equal totals share the win, which is a draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When a deal starts, then the 24 cards are shuffled, each player receives 6 cards in hand, the other 12 form the talon, and one talon card is turned face up as talon_up."
    },
    {
      "id": "R2",
      "text": "When a deal starts, then each player's deal_points is 0, declared_this_deal is false, and played_this_deal is empty."
    },
    {
      "id": "R3",
      "text": "When deal 1 starts, then seat 1 leads; when deal 2 starts, then seat 2 leads."
    },
    {
      "id": "R4",
      "text": "When deal 3 starts, then the seat with the lower match_total leads, and if the totals are equal, seat 2 leads."
    },
    {
      "id": "R5",
      "text": "When it is the first trick of a deal, then the leader is not offered a declaration."
    },
    {
      "id": "R6",
      "text": "When the leader won the previous trick of this deal, has not declared this deal, and holds a qualifying set, then the leader is offered declare or pass; otherwise the leader is not offered a declaration."
    },
    {
      "id": "R7",
      "text": "When a leader declares holding exactly three Tens, three Nines or three Aces, then 9 thirds per such rank are added to the leader's deal_points."
    },
    {
      "id": "R8",
      "text": "When a leader declares holding all four Tens, Nines or Aces, then 12 thirds per such rank are added instead of 9."
    },
    {
      "id": "R9",
      "text": "When a leader declares holding the Ten, Nine and Ace of one suit (a Napoli), then 9 thirds per such suit are added, and a card may count in several sets."
    },
    {
      "id": "R10",
      "text": "When a leader declares, then every qualifying set in hand is scored at once, its cards are added to declared_cards_shown, declared_this_deal becomes true, and no further declaration is offered that deal."
    },
    {
      "id": "R11",
      "text": "When the leader plays, then any card in hand may be played and it is added to played_this_deal."
    },
    {
      "id": "R12",
      "text": "When the follower holds a card of the led suit, then only cards of the led suit are offered; otherwise every card in hand is offered."
    },
    {
      "id": "R13",
      "text": "When the follower plays a higher card of the led suit (Ten > Nine > Ace > King > Ober > Unter), then the follower wins the trick; otherwise the leader wins, as there are no trumps."
    },
    {
      "id": "R14",
      "text": "When a trick is won, then the winner adds the values of both cards to deal_points, with Ace = 3 thirds and Ten, Nine, King, Ober, Unter = 1 third each."
    },
    {
      "id": "R15",
      "text": "When the 12th trick of a deal is won, then the winner adds a further 3 thirds."
    },
    {
      "id": "R16",
      "text": "When a trick ends and the talon is not empty, then the winner takes talon_up into hand, the loser takes a hidden talon card that only the loser sees, and a new card is turned face up if any remain."
    },
    {
      "id": "R17",
      "text": "When 6 tricks of a deal are done, then the talon is empty and no more draws happen that deal."
    },
    {
      "id": "R18",
      "text": "When a trick ends, then its winner leads the next trick."
    },
    {
      "id": "R19",
      "text": "When the 12th trick of a deal ends, then each player's deal_points is added to match_total and both totals are announced."
    },
    {
      "id": "R20",
      "text": "When 36 tricks (3 deals) have been played, then the game ends and the higher match_total wins; equal totals are a draw."
    }
  ],
  "offers": [
    {
      "question": "Declaration",
      "who": "the leader",
      "options": "When eligible (won the previous trick this deal, not yet declared this deal, holds a qualifying set): declare, pass. Otherwise the question is not asked."
    },
    {
      "question": "Lead a card",
      "who": "the leader",
      "options": "Every card in the leader's hand."
    },
    {
      "question": "Follow a card",
      "who": "the follower",
      "options": "If holding any card of the led suit: only those cards. Otherwise: every card in hand."
    }
  ],
  "choices": [
    {
      "what": "Exactly 2 players",
      "why": "The designer fixed the game as a duel. The trick and draw rules (winner takes the face-up card, loser the hidden one) only work with two."
    },
    {
      "what": "No talk step",
      "why": "This is a zero-sum duel with no source rule for talk, so messages would add words without anything to disagree about or agree on."
    },
    {
      "what": "Talon draws pick a random remaining talon card",
      "why": "Drawing at random from a hidden shuffled list is equivalent to taking the next card of a fixed shuffled order."
    },
    {
      "what": "Declaring is optional when eligible",
      "why": "The source says the leader 'may' declare, so pass is offered."
    },
    {
      "what": "Rank strengths Ten 6 down to Unter 1",
      "why": "These are numeric codes so the trick winner can be computed by comparison."
    }
  ],
  "simplifications": [
    {
      "what": "Deal-start actions run as conditional single steps at the top of the round (when trick_in_deal == 0)",
      "why": "The step list is flat. Each deal-start operation carries its own arithmetic condition, so no block of steps has to be chosen instead of another."
    },
    {
      "what": "The declaration value is computed arithmetically by counting ranks and suits in the hand",
      "why": "Outcomes must be calculated, and the set rules reduce to counts."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: deal_points, match_total; table: talon_up, played_this_deal, declared_cards_shown.
````

## Reply

````
```json
[
  {"name": "Deal start: 6 cards each, talon of 12 with one face up (after first trick: hands back to 6, 9 hidden talon cards left)", "rule": "R1", "players": 2, "seed": 1, "rounds": 1, "default": "first",
   "rules": [],
   "expect": {"lens": {"players": {"1": {"hand": 6}, "2": {"hand": 6}}, "game": {"talon": 9, "played_this_deal": 2}},
              "players": {"1": {"match_total": 0}, "2": {"match_total": 0}}}},

  {"name": "New deal resets declarations shown and played cards, match totals kept", "rule": "R2", "players": 2, "seed": 2, "rounds": 1, "default": "first",
   "given": {"players": {"1": {"match_total": 30, "deal_points": 30, "declared_this_deal": true}, "2": {"match_total": 40, "deal_points": 40, "declared_this_deal": true}},
             "game": {"deal_no": 1, "trick_in_deal": 0, "tricks_played": 12,
                      "played_this_deal": ["Ten of Hearts", "Nine of Hearts", "Ace of Hearts", "King of Hearts"],
                      "declared_cards_shown": ["Ten of Hearts", "Ten of Bells", "Ten of Leaves"]}},
   "rules": [],
   "expect": {"lens": {"game": {"played_this_deal": 2, "declared_cards_shown": 0}, "players": {"1": {"hand": 6}, "2": {"hand": 6}}},
              "players": {"1": {"match_total": 30}, "2": {"match_total": 40}},
              "not_offered": [{"seat": 1, "option": "declare"}, {"seat": 2, "option": "declare"}]}},

  {"name": "Deal 1 opens with a lead and a follow (random deal, only counts asserted)", "rule": "R3", "players": 2, "seed": 3, "rounds": 1, "default": "first",
   "rules": [],
   "expect": {"lens": {"game": {"played_this_deal": 2}},
              "players": {"1": {"match_total": 0}, "2": {"match_total": 0}}}},

  {"name": "Deal 3 starts with lower total leading (random deal, only counts and totals asserted)", "rule": "R4", "players": 2, "seed": 4, "rounds": 1, "default": "first",
   "given": {"players": {"1": {"match_total": 30, "deal_points": 10}, "2": {"match_total": 40, "deal_points": 20}},
             "game": {"deal_no": 2, "trick_in_deal": 0, "tricks_played": 24}},
   "rules": [],
   "expect": {"lens": {"game": {"played_this_deal": 2}, "players": {"1": {"hand": 6}, "2": {"hand": 6}}},
              "players": {"1": {"match_total": 30}, "2": {"match_total": 40}}}},

  {"name": "No declaration offered on the first trick of a deal", "rule": "R5", "players": 2, "seed": 5, "rounds": 1, "default": "first",
   "rules": [],
   "expect": {"not_offered": [{"seat": 1, "option": "declare"}, {"seat": 2, "option": "declare"}],
              "lens": {"game": {"declared_cards_shown": 0}}}},

  {"name": "Eligible leader with three Tens is offered declare and may pass", "rule": "R6", "players": 2, "seed": 6, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Ten of Hearts", "Ten of Bells", "Ten of Leaves", "Unter of Acorns", "King of Hearts", "Ober of Hearts"], "deal_points": 0, "declared_this_deal": false},
                         "2": {"hand": ["King of Acorns", "Ober of Bells", "Unter of Bells", "Ober of Leaves", "Unter of Leaves", "Nine of Hearts"], "deal_points": 0}},
             "game": {"deal_no": 1, "trick_in_deal": 6, "tricks_played": 6, "leader": 1, "last_trick_winner": 1, "talon": [], "talon_count": 0, "talon_up": "", "played_this_deal": [], "declared_cards_shown": []}},
   "rules": [{"seat": 1, "options_include": "pass"}, {"seat": 1, "options_include": "Unter of Acorns"}],
   "expect": {"offered": [{"seat": 1, "option": "declare"}],
              "players": {"1": {"deal_points": 0}, "2": {"deal_points": 2}},
              "lens": {"game": {"declared_cards_shown": 0}}}},

  {"name": "Leader who already declared this deal is not offered a declaration", "rule": "R6", "players": 2, "seed": 7, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Ten of Hearts", "Ten of Bells", "Ten of Leaves", "Unter of Acorns", "King of Hearts", "Ober of Hearts"], "deal_points": 9, "declared_this_deal": true},
                         "2": {"hand": ["King of Acorns", "Ober of Bells", "Unter of Bells", "Ober of Leaves", "Unter of Leaves", "Nine of Hearts"], "deal_points": 0}},
             "game": {"deal_no": 1, "trick_in_deal": 6, "tricks_played": 6, "leader": 1, "last_trick_winner": 1, "talon": [], "talon_count": 0, "talon_up": "", "played_this_deal": [], "declared_cards_shown": []}},
   "rules": [{"seat": 1, "options_include": "Unter of Acorns"}],
   "expect": {"not_offered": [{"seat": 1, "option": "declare"}],
              "players": {"1": {"deal_points": 9}, "2": {"deal_points": 2}}}},

  {"name": "Leader without a qualifying set is not offered a declaration", "rule": "R6", "players": 2, "seed": 8, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Ober of Hearts", "Ten of Bells", "King of Bells", "Unter of Leaves", "King of Acorns", "Unter of Acorns"], "deal_points": 0, "declared_this_deal": false},
                         "2": {"hand": ["Nine of Bells", "Ober of Bells", "Ten of Leaves", "Nine of Leaves", "Ace of Acorns", "Ober of Acorns"], "deal_points": 0}},
             "game": {"deal_no": 1, "trick_in_deal": 6, "tricks_played": 6, "leader": 1, "last_trick_winner": 1, "talon": [], "talon_count": 0, "talon_up": "", "played_this_deal": [], "declared_cards_shown": []}},
   "rules": [{"seat": 1, "options_include": "Ober of Hearts"}, {"seat": 2, "options_include": "Ober of Bells"}],
   "expect": {"not_offered": [{"seat": 1, "option": "declare"}],
              "players": {"1": {"deal_points": 2}, "2": {"deal_points": 0}}}},

  {"name": "Declaring three Tens scores 9 thirds", "rule": "R7", "players": 2, "seed": 9, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Ten of Hearts", "Ten of Bells", "Ten of Leaves", "Unter of Acorns", "King of Hearts", "Ober of Hearts"], "deal_points": 0, "declared_this_deal": false},
                         "2": {"hand": ["King of Acorns", "Ober of Bells", "Unter of Bells", "Ober of Leaves", "Unter of Leaves", "Nine of Hearts"], "deal_points": 0}},
             "game": {"deal_no": 1, "trick_in_deal": 6, "tricks_played": 6, "leader": 1, "last_trick_winner": 1, "talon": [], "talon_count": 0, "talon_up": "", "played_this_deal": [], "declared_cards_shown": []}},
   "rules": [{"seat": 1, "options_include": "declare"}, {"seat": 1, "options_include": "Unter of Acorns"}],
   "expect": {"players": {"1": {"deal_points": 9}, "2": {"deal_points": 2}},
              "lens": {"game": {"declared_cards_shown": 3}}}},

  {"name": "Declaring all four Aces scores 12 thirds", "rule": "R8", "players": 2, "seed": 10, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Ace of Hearts", "Ace of Bells", "Ace of Leaves", "Ace of Acorns", "Unter of Hearts", "Ober of Hearts"], "deal_points": 0, "declared_this_deal": false},
                         "2": {"hand": ["King of Hearts", "Ten of Bells", "Nine of Bells", "King of Bells", "Ten of Leaves", "Nine of Leaves"], "deal_points": 0}},
             "game": {"deal_no": 1, "trick_in_deal": 6, "tricks_played": 6, "leader": 1, "last_trick_winner": 1, "talon": [], "talon_count": 0, "talon_up": "", "played_this_deal": [], "declared_cards_shown": []}},
   "rules": [{"seat": 1, "options_include": "declare"}, {"seat": 1, "options_include": "Unter of Hearts"}],
   "expect": {"players": {"1": {"deal_points": 12}, "2": {"deal_points": 2}},
              "lens": {"game": {"declared_cards_shown": 4}}}},

  {"name": "Napoli plus three Tens sharing the Ten of Hearts scores 18 thirds", "rule": "R9", "players": 2, "seed": 11, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Ten of Hearts", "Nine of Hearts", "Ace of Hearts", "Ten of Bells", "Ten of Leaves", "Unter of Acorns"], "deal_points": 0, "declared_this_deal": false},
                         "2": {"hand": ["King of Acorns", "Ober of Bells", "Unter of Bells", "Ober of Leaves", "Unter of Leaves", "King of Leaves"], "deal_points": 0}},
             "game": {"deal_no": 1, "trick_in_deal": 6, "tricks_played": 6, "leader": 1, "last_trick_winner": 1, "talon": [], "talon_count": 0, "talon_up": "", "played_this_deal": [], "declared_cards_shown": []}},
   "rules": [{"seat": 1, "options_include": "declare"}, {"seat": 1, "options_include": "Unter of Acorns"}],
   "expect": {"players": {"1": {"deal_points": 18}, "2": {"deal_points": 2}}}},

  {"name": "After declaring, no second declaration is offered that deal", "rule": "R10", "players": 2, "seed": 12, "rounds": 2,
   "given": {"players": {"1": {"hand": ["Ten of Hearts", "Ten of Bells", "Ten of Leaves", "Nine of Acorns", "King of Hearts", "Ober of Hearts"], "deal_points": 0, "declared_this_deal": false},
                         "2": {"hand": ["Unter of Acorns", "Ober of Bells", "Unter of Bells", "Ober of Leaves", "Unter of Leaves", "King of Leaves"], "deal_points": 0}},
             "game": {"deal_no": 1, "trick_in_deal": 6, "tricks_played": 6, "leader": 1, "last_trick_winner": 1, "talon": [], "talon_count": 0, "talon_up": "", "played_this_deal": [], "declared_cards_shown": []}},
   "rules": [{"seat": 1, "options_include": "declare", "times": "all"},
             {"seat": 1, "options_include": "Nine of Acorns"},
             {"seat": 1, "options_include": "King of Hearts"},
             {"seat": 2, "options_include": "Ober of Bells"}],
   "expect": {"players": {"1": {"deal_points": 13}, "2": {"deal_points": 0}},
              "lens": {"game": {"declared_cards_shown": 3}}}},

  {"name": "Leader may lead any card and it is added to played cards", "rule": "R11", "players": 2, "seed": 13, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Ober of Hearts", "Ten of Bells", "King of Bells", "Unter of Leaves", "King of Acorns", "Unter of Acorns"], "deal_points": 0},
                         "2": {"hand": ["Nine of Bells", "Ober of Bells", "Ten of Leaves", "Nine of Leaves", "Ace of Acorns", "Ober of Acorns"], "deal_points": 0}},
             "game": {"deal_no": 1, "trick_in_deal": 6, "tricks_played": 6, "leader": 1, "last_trick_winner": 1, "talon": [], "talon_count": 0, "talon_up": "", "played_this_deal": [], "declared_cards_shown": []}},
   "rules": [{"seat": 1, "options_include": "Ober of Hearts"}, {"seat": 2, "options_include": "Ober of Bells"}],
   "expect": {"game": {"played_this_deal": ["Ober of Hearts", "Ober of Bells"]},
              "offered": [{"seat": 1, "option": "Unter of Leaves"}, {"seat": 1, "option": "King of Acorns"}, {"seat": 1, "option": "Ten of Bells"}],
              "players": {"1": {"deal_points": 2}, "2": {"deal_points": 0}}}},

  {"name": "Follower holding the led suit is offered only that suit", "rule": "R12", "players": 2, "seed": 14, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Ten of Hearts", "Nine of Bells", "King of Bells", "Ober of Leaves", "King of Acorns", "Ober of Acorns"], "deal_points": 0},
                         "2": {"hand": ["Unter of Hearts", "King of Hearts", "Ober of Bells", "Unter of Bells", "Ten of Leaves", "Unter of Leaves"], "deal_points": 0}},
             "game": {"deal_no": 1, "trick_in_deal": 6, "tricks_played": 6, "leader": 1, "last_trick_winner": 1, "talon": [], "talon_count": 0, "talon_up": "", "played_this_deal": [], "declared_cards_shown": []}},
   "rules": [{"seat": 1, "options_include": "Ten of Hearts"}, {"seat": 2, "options_include": "King of Hearts"}],
   "expect": {"offered": [{"seat": 2, "option": "Unter of Hearts"}, {"seat": 2, "option": "King of Hearts"}],
              "not_offered": [{"seat": 2, "option": "Ober of Bells"}, {"seat": 2, "option": "Ten of Leaves"}, {"seat": 2, "option": "Unter of Leaves"}],
              "players": {"1": {"deal_points": 2}, "2": {"deal_points": 0}}}},

  {"name": "Follower void in the led suit is offered every card", "rule": "R12", "players": 2, "seed": 15, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Ten of Hearts", "Nine of Bells", "King of Bells", "Ober of Leaves", "King of Acorns", "Ober of Acorns"], "deal_points": 0},
                         "2": {"hand": ["Ace of Bells", "Ober of Bells", "Unter of Bells", "Ten of Leaves", "Unter of Leaves", "Nine of Acorns"], "deal_points": 0}},
             "game": {"deal_no": 1, "trick_in_deal": 6, "tricks_played": 6, "leader": 1, "last_trick_winner": 1, "talon": [], "talon_count": 0, "talon_up": "", "played_this_deal": [], "declared_cards_shown": []}},
   "rules": [{"seat": 1, "options_include": "Ten of Hearts"}, {"seat": 2, "options_include": "Ace of Bells"}],
   "expect": {"offered": [{"seat": 2, "option": "Ober of Bells"}, {"seat": 2, "option": "Ten of Leaves"}, {"seat": 2, "option": "Nine of Acorns"}],
              "players": {"1": {"deal_points": 4}, "2": {"deal_points": 0}}}},

  {"name": "Higher card of the led suit wins for the follower", "rule": "R13", "players": 2, "seed": 16, "rounds": 1,
   "given": {"players": {"1": {"hand": ["King of Bells", "Ten of Hearts", "Ober of Hearts", "Unter of Leaves", "King of Acorns", "Ober of Acorns"], "deal_points": 0},
                         "2": {"hand": ["Ten of Bells", "Nine of Leaves", "Ace of Leaves", "Unter of Acorns", "Nine of Acorns", "Ace of Hearts"], "deal_points": 0}},
             "game": {"deal_no": 1, "trick_in_deal": 6, "tricks_played": 6, "leader": 1, "last_trick_winner": 1, "talon": [], "talon_count": 0, "talon_up": "", "played_this_deal": [], "declared_cards_shown": []}},
   "rules": [{"seat": 1, "options_include": "King of Bells"}],
   "expect": {"players": {"1": {"deal_points": 0}, "2": {"deal_points": 2}}}},

  {"name": "Off-suit Ace does not win: no trumps, leader takes the trick", "rule": "R13", "players": 2, "seed": 17, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Unter of Leaves", "Ten of Hearts", "Ober of Hearts", "King of Bells", "King of Acorns", "Ober of Acorns"], "deal_points": 0},
                         "2": {"hand": ["Ace of Acorns", "Ten of Bells", "Nine of Bells", "King of Hearts", "Unter of Hearts", "Nine of Acorns"], "deal_points": 0}},
             "game": {"deal_no": 1, "trick_in_deal": 6, "tricks_played": 6, "leader": 1, "last_trick_winner": 1, "talon": [], "talon_count": 0, "talon_up": "", "played_this_deal": [], "declared_cards_shown": []}},
   "rules": [{"seat": 1, "options_include": "Unter of Leaves"}, {"seat": 2, "options_include": "Ace of Acorns"}],
   "expect": {"players": {"1": {"deal_points": 4}, "2": {"deal_points": 0}}}},

  {"name": "Lower card of the led suit loses to the leader (Ace below Nine)", "rule": "R13", "players": 2, "seed": 18, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Nine of Bells", "Ten of Hearts", "Ober of Hearts", "Unter of Leaves", "King of Acorns", "Ober of Acorns"], "deal_points": 0},
                         "2": {"hand": ["Ace of Bells", "King of Hearts", "Unter of Hearts", "Ten of Leaves", "Nine of Leaves", "Unter of Acorns"], "deal_points": 0}},
             "game": {"deal_no": 1, "trick_in_deal": 6, "tricks_played": 6, "leader": 1, "last_trick_winner": 1, "talon": [], "talon_count": 0, "talon_up": "", "played_this_deal": [], "declared_cards_shown": []}},
   "rules": [{"seat": 1, "options_include": "Nine of Bells"}],
   "expect": {"players": {"1": {"deal_points": 4}, "2": {"deal_points": 0}}}},

  {"name": "Trick winner adds card values: Ace 3 plus Ten 1", "rule": "R14", "players": 2, "seed": 19, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Ace of Hearts", "Nine of Bells", "King of Bells", "Ober of Leaves", "King of Acorns", "Ober of Acorns"], "deal_points": 3},
                         "2": {"hand": ["Ten of Hearts", "Ober of Bells", "Unter of Bells", "Ten of Leaves", "Unter of Leaves", "Nine of Acorns"], "deal_points": 5}},
             "game": {"deal_no": 1, "trick_in_deal": 6, "tricks_played": 6, "leader": 1, "last_trick_winner": 1, "talon": [], "talon_count": 0, "talon_up": "", "played_this_deal": [], "declared_cards_shown": []}},
   "rules": [{"seat": 1, "options_include": "Ace of Hearts"}],
   "expect": {"players": {"1": {"deal_points": 3}, "2": {"deal_points": 9}}}},

  {"name": "Winner of the 12th trick gets 3 extra thirds", "rule": "R15", "players": 2, "seed": 20, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Ace of Hearts"], "deal_points": 20, "match_total": 0},
                         "2": {"hand": ["Unter of Hearts"], "deal_points": 15, "match_total": 0}},
             "game": {"deal_no": 1, "trick_in_deal": 11, "tricks_played": 11, "leader": 1, "last_trick_winner": 1, "talon": [], "talon_count": 0, "talon_up": "", "played_this_deal": []}},
   "rules": [],
   "expect": {"players": {"1": {"deal_points": 27}, "2": {"deal_points": 15}}}},

  {"name": "Trick winner takes the face-up talon card, loser draws a hidden one", "rule": "R16", "players": 2, "seed": 21, "rounds": 2, "default": "first",
   "given": {"players": {"1": {"hand": ["Ten of Hearts", "Nine of Hearts", "King of Bells", "Ober of Bells", "Unter of Bells", "King of Leaves"], "deal_points": 0},
                         "2": {"hand": ["Unter of Hearts", "Ten of Bells", "Nine of Bells", "Ace of Bells", "Ober of Leaves", "Unter of Leaves"], "deal_points": 0}},
             "game": {"deal_no": 1, "trick_in_deal": 3, "tricks_played": 3, "leader": 1, "last_trick_winner": 1,
                      "talon_up": "Ace of Acorns", "talon": ["Ten of Acorns", "Nine of Acorns", "King of Acorns", "Ober of Acorns", "Unter of Acorns"], "talon_count": 6,
                      "played_this_deal": ["Ace of Hearts", "King of Hearts", "Ober of Hearts", "Ten of Leaves", "Nine of Leaves", "Ace of Leaves"], "declared_cards_shown": []}},
   "rules": [{"seat": 1, "options_include": "Ten of Hearts"}, {"seat": 1, "options_include": "Ace of Acorns"}],
   "expect": {"lens": {"players": {"1": {"hand": 6}, "2": {"hand": 6}}, "game": {"talon": 1, "played_this_deal": 10}}}},

  {"name": "After the 6th trick the talon is empty and no more draws happen", "rule": "R17", "players": 2, "seed": 22, "rounds": 2,
   "given": {"players": {"1": {"hand": ["Ten of Hearts", "King of Hearts", "Nine of Bells", "King of Bells", "Ace of Leaves", "King of Leaves"], "deal_points": 10},
                         "2": {"hand": ["Unter of Hearts", "Ober of Hearts", "Unter of Bells", "Ober of Bells", "Unter of Leaves", "Ober of Leaves"], "deal_points": 4}},
             "game": {"deal_no": 1, "trick_in_deal": 5, "tricks_played": 5, "leader": 1, "last_trick_winner": 1,
                      "talon_up": "Ober of Acorns", "talon": ["Unter of Acorns"], "talon_count": 2,
                      "played_this_deal": ["Nine of Hearts", "Ace of Hearts", "Ten of Bells", "Ace of Bells", "Ten of Leaves", "Nine of Leaves", "Ten of Acorns", "Nine of Acorns", "Ace of Acorns", "King of Acorns"], "declared_cards_shown": []}},
   "rules": [{"seat": 1, "options_include": "Ten of Hearts"}, {"seat": 1, "options_include": "King of Hearts"},
             {"seat": 2, "options_include": "Unter of Hearts"}],
   "expect": {"game": {"talon_up": ""},
              "lens": {"players": {"1": {"hand": 5}, "2": {"hand": 5}}, "game": {"talon": 0, "played_this_deal": 14}},
              "players": {"1": {"deal_points": 14}, "2": {"deal_points": 4}}}},

  {"name": "The trick winner leads the next trick", "rule": "R18", "players": 2, "seed": 23, "rounds": 2,
   "given": {"players": {"1": {"hand": ["King of Hearts", "Unter of Bells", "Ober of Leaves", "Unter of Leaves", "Ober of Acorns", "Unter of Acorns"], "deal_points": 0},
                         "2": {"hand": ["Ten of Hearts", "Nine of Bells", "King of Acorns", "Ace of Bells", "King of Leaves", "Ace of Leaves"], "deal_points": 0}},
             "game": {"deal_no": 1, "trick_in_deal": 6, "tricks_played": 6, "leader": 1, "last_trick_winner": 1, "talon": [], "talon_count": 0, "talon_up": "", "played_this_deal": [], "declared_cards_shown": []}},
   "rules": [{"seat": 1, "options_include": "King of Hearts"}, {"seat": 2, "options_include": "Nine of Bells"}],
   "expect": {"game": {"played_this_deal": ["King of Hearts", "Ten of Hearts", "Nine of Bells", "Unter of Bells"]},
              "players": {"1": {"deal_points": 0}, "2": {"deal_points": 4}}}},

  {"name": "End of deal adds deal points to match totals", "rule": "R19", "players": 2, "seed": 24, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Ace of Hearts"], "deal_points": 20, "match_total": 40},
                         "2": {"hand": ["Unter of Hearts"], "deal_points": 15, "match_total": 30}},
             "game": {"deal_no": 1, "trick_in_deal": 11, "tricks_played": 11, "leader": 1, "last_trick_winner": 1, "talon": [], "talon_count": 0, "talon_up": "", "played_this_deal": []}},
   "rules": [],
   "expect": {"players": {"1": {"match_total": 67}, "2": {"match_total": 45}}}},

  {"name": "After 36 tricks the higher match total wins", "rule": "R20", "players": 2, "seed": 25,
   "given": {"players": {"1": {"hand": ["Unter of Hearts"], "deal_points": 10, "match_total": 60},
                         "2": {"hand": ["Ace of Hearts"], "deal_points": 20, "match_total": 50}},
             "game": {"deal_no": 3, "trick_in_deal": 11, "tricks_played": 35, "leader": 1, "last_trick_winner": 1, "talon": [], "talon_count": 0, "talon_up": "", "played_this_deal": []}},
   "rules": [],
   "expect": {"winner": 2, "standings": {"1": 70, "2": 77},
              "players": {"1": {"match_total": 70}, "2": {"match_total": 77}}}},

  {"name": "After 36 tricks equal match totals share the win", "rule": "R20", "players": 2, "seed": 26,
   "given": {"players": {"1": {"hand": ["Unter of Hearts"], "deal_points": 10, "match_total": 60},
                         "2": {"hand": ["Ace of Hearts"], "deal_points": 0, "match_total": 63}},
             "game": {"deal_no": 3, "trick_in_deal": 11, "tricks_played": 35, "leader": 1, "last_trick_winner": 1, "talon": [], "talon_count": 0, "talon_up": "", "played_this_deal": []}},
   "rules": [],
   "expect": {"winner": [1, 2], "standings": {"1": 70, "2": 70}}}
]
```
````
