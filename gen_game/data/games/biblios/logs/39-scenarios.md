# 39 scenarios

- time: 2026-10-27T21:33:45+00:00 (60.4s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 6eed5c8f7bdddea2, reply sha256 6b13b4fd0fd8edb9

## Sent

````
SPEC:
{
  "name": "Biblios: Scriptorium Lots (revised)",
  "summary": "Three scribes take turns splitting three cards among keep, give and auction. They bid gold for the auction cards and use Church cards to push colour dice, then score each colour they alone lead at its final die value.",
  "players": {
    "min": 3,
    "max": 3,
    "suggested": 3
  },
  "parameters": {
    "player_count": 3,
    "deck_size": 36,
    "colours": 5,
    "colour_cards_per_colour": 6,
    "colour_value_1_copies": 2,
    "colour_value_2_copies": 2,
    "colour_value_3_copies": 1,
    "colour_value_4_copies": 1,
    "colour_cards_total": 30,
    "gold_card_small": 2,
    "gold_card_mid": 3,
    "gold_card_large": 4,
    "gold_cards": 3,
    "church_cards": 3,
    "starting_gold": 8,
    "starting_colour_total": 0,
    "die_start": 3,
    "die_min": 1,
    "die_max": 6,
    "die_step": 1,
    "rounds": 12,
    "cards_per_round": 3,
    "split_options": 6,
    "church_options": 10,
    "max_church_actions_per_round": 1,
    "min_bid": 0,
    "winning_bid_must_exceed": 0,
    "active_seat_round_1": 1,
    "active_seat_round_2": 2,
    "active_seat_round_3": 3,
    "active_seat_round_4": 2,
    "active_seat_round_5": 3,
    "active_seat_round_6": 1,
    "active_seat_round_7": 3,
    "active_seat_round_8": 1,
    "active_seat_round_9": 2,
    "active_seat_round_10": 1,
    "active_seat_round_11": 2,
    "active_seat_round_12": 3,
    "rank_gold_weight": 1,
    "rank_vp_weight": 1000
  },
  "attributes": {
    "player": [
      {
        "key": "red",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "true Red total, kept cards included",
        "observable": false
      },
      {
        "key": "blue",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "true Blue total, kept cards included",
        "observable": false
      },
      {
        "key": "green",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "true Green total, kept cards included",
        "observable": false
      },
      {
        "key": "yellow",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "true Yellow total, kept cards included",
        "observable": false
      },
      {
        "key": "purple",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "true Purple total, kept cards included",
        "observable": false
      },
      {
        "key": "gold",
        "type": "number",
        "visible": "public",
        "initial": 8,
        "meaning": "purse; the public tie-break",
        "observable": true
      },
      {
        "key": "church",
        "type": "bool",
        "visible": "ally",
        "initial": false,
        "meaning": "church flag; Yes gives one church action this round",
        "observable": false
      },
      {
        "key": "kept",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "cards this player kept face-down",
        "observable": false
      },
      {
        "key": "public_record",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "cards received openly (given or won at auction)",
        "observable": true
      },
      {
        "key": "vp",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "victory points, computed after round 12",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "die_red",
        "type": "number",
        "visible": "public",
        "initial": 3,
        "meaning": "Red die, 1-6",
        "observable": true
      },
      {
        "key": "die_blue",
        "type": "number",
        "visible": "public",
        "initial": 3,
        "meaning": "Blue die, 1-6",
        "observable": true
      },
      {
        "key": "die_green",
        "type": "number",
        "visible": "public",
        "initial": 3,
        "meaning": "Green die, 1-6",
        "observable": true
      },
      {
        "key": "die_yellow",
        "type": "number",
        "visible": "public",
        "initial": 3,
        "meaning": "Yellow die, 1-6",
        "observable": true
      },
      {
        "key": "die_purple",
        "type": "number",
        "visible": "public",
        "initial": 3,
        "meaning": "Purple die, 1-6",
        "observable": true
      },
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "current round number",
        "observable": true
      },
      {
        "key": "active_seat",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "seat of the active player this round",
        "observable": true
      },
      {
        "key": "active_order",
        "type": "list",
        "visible": "public",
        "initial": [
          1,
          2,
          3,
          2,
          3,
          1,
          3,
          1,
          2,
          1,
          2,
          3
        ],
        "meaning": "active seat for rounds 1-12",
        "observable": false
      },
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [
          "Red 1",
          "Red 1",
          "Red 2",
          "Red 2",
          "Red 3",
          "Red 4",
          "Blue 1",
          "Blue 1",
          "Blue 2",
          "Blue 2",
          "Blue 3",
          "Blue 4",
          "Green 1",
          "Green 1",
          "Green 2",
          "Green 2",
          "Green 3",
          "Green 4",
          "Yellow 1",
          "Yellow 1",
          "Yellow 2",
          "Yellow 2",
          "Yellow 3",
          "Yellow 4",
          "Purple 1",
          "Purple 1",
          "Purple 2",
          "Purple 2",
          "Purple 3",
          "Purple 4",
          "Gold 2",
          "Gold 3",
          "Gold 4",
          "Church",
          "Church",
          "Church"
        ],
        "meaning": "shuffled draw pile; its makeup is public, its order hidden",
        "observable": false
      },
      {
        "key": "dealt",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "the 3 cards dealt this round, shown privately to the active player only",
        "observable": false
      },
      {
        "key": "auction_card",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "the card up for auction this round",
        "observable": true
      },
      {
        "key": "discard",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "auction cards nobody won",
        "observable": false
      }
    ]
  },
  "setup": [
    "Seats 1, 2 and 3 are filled.",
    "The 36-card deck is placed in `deck` and shuffled once by the seeded random draw. It holds 30 colour cards (Red, Blue, Green, Yellow and Purple, each with values 1, 1, 2, 2, 3, 4), Gold 2, Gold 3, Gold 4 and three Church cards.",
    "Each player starts with gold 8, all five colour totals 0, an empty kept list, an empty public_record, church No and vp 0.",
    "All five dice start at 3.",
    "The deck makeup is announced to everyone."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round += 1; active_seat = active_order[round-1]; announce 'Round {round}: seat {active_seat} is active.'"
    },
    {
      "action": "update",
      "who": "seat active_seat",
      "answer": null,
      "effect": "Draw 3 cards at random from deck into dealt, removing them from deck. Reveal dealt privately to the active seat only."
    },
    {
      "action": "ask",
      "who": "seat active_seat",
      "answer": "one of the 6 assignments of the three dealt cards to KEEP / AUCTION / GIVE, each listed as an option naming the cards (e.g. 'KEEP Red 3, AUCTION Gold 2, GIVE Church')",
      "effect": "records which dealt card is keep_card, auction_card and give_card"
    },
    {
      "action": "update",
      "who": "seat active_seat",
      "answer": null,
      "effect": "keep_card is appended to the active player's kept list and takes effect for them. A colour card adds its value to that colour total, a Gold card adds to gold, and a Church card sets church = true (no extra effect if already true). Nothing is announced except the public change in gold."
    },
    {
      "action": "update",
      "who": "next seat of active_seat (1->2, 2->3, 3->1)",
      "answer": null,
      "effect": "give_card is revealed to everyone, takes effect for the next seat (colour total, gold or church = true), and is appended to that player's public_record."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "auction_card = the AUCTION card; announce it to everyone. dealt is emptied."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "short text message",
      "effect": "broadcast {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"} once all are in; non-binding"
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "whole number from 0 to that player's gold",
      "effect": "records each player's secret bid"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "All bids are revealed and top = max bid. If top > 0 and exactly one player bid top, that player's gold -= top (the gold leaves the game), auction_card takes effect for them (colour total, gold or church = true) and is appended to their public_record. Otherwise auction_card is appended to discard and nobody pays."
    },
    {
      "action": "poll",
      "who": "every player whose church is true (step skipped if none)",
      "answer": "one of: raise Red, lower Red, raise Blue, lower Blue, raise Green, lower Green, raise Yellow, lower Yellow, raise Purple, lower Purple",
      "effect": "Choices are applied in seat order 1, 2, 3: the named die is changed by +1 or -1 and clamped to 1..6."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "church = false for every player."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce the five die values, each player's gold and each player's public_record. Kept cards and true colour totals are not shown."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "when round == 12: for each colour, a player whose total in that colour is strictly greater than both other players' totals gets vp += that colour's die value; a tied top scores nobody."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "end the game if round == 12, otherwise continue"
    }
  ],
  "ending": {
    "condition": "round == 12",
    "rank_by": "you.vp * 1000 + you.gold",
    "decided_by": "Most VP wins. A tie on VP goes to the tied player with the most gold. Players still level share the win (a draw)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game starts, then each player has gold 8, all colour totals 0, church No and an empty public_record, and every die is 3."
    },
    {
      "id": "R2",
      "text": "When the game starts, then the deck holds 36 cards: values 1, 1, 2, 2, 3, 4 in each of five colours, Gold 2, Gold 3, Gold 4 and 3 Church cards."
    },
    {
      "id": "R3",
      "text": "When round r (1-12) begins, then the active seat is entry r of the order 1, 2, 3, 2, 3, 1, 3, 1, 2, 1, 2, 3."
    },
    {
      "id": "R4",
      "text": "When a round begins, then 3 cards are removed from the deck and shown only to the active seat."
    },
    {
      "id": "R5",
      "text": "When the active seat splits the cards, then they choose one of exactly 6 assignments of the 3 cards to KEEP, AUCTION and GIVE."
    },
    {
      "id": "R6",
      "text": "When a player receives a colour card of value v, then their total in that colour rises by v."
    },
    {
      "id": "R7",
      "text": "When a player receives a Gold card worth g, then their gold rises by g."
    },
    {
      "id": "R8",
      "text": "When a player receives a Church card, then their church flag becomes Yes, and a second Church card in the same round has no further effect."
    },
    {
      "id": "R9",
      "text": "When the KEEP card is applied, then it goes to the active seat's kept list, is not revealed, and is not added to the public record."
    },
    {
      "id": "R10",
      "text": "When the GIVE card is applied, then it is revealed, goes to the next seat (1->2, 2->3, 3->1), takes effect and is added to that seat's public_record."
    },
    {
      "id": "R11",
      "text": "When the AUCTION card is chosen, then it is revealed to everyone before talk and bidding."
    },
    {
      "id": "R12",
      "text": "When talk happens, then all three players submit one short message at the same time and all are shown together; talk is not binding."
    },
    {
      "id": "R13",
      "text": "When bidding happens, then each player secretly bids a whole number from 0 to their current gold, all at the same time."
    },
    {
      "id": "R14",
      "text": "When exactly one player has the highest bid and it is above 0, then that player loses that much gold (the gold leaves the game), gets the auction card's effect, and the card is added to their public_record."
    },
    {
      "id": "R15",
      "text": "When the top bid is tied or all bids are 0, then the auction card is discarded and nobody pays."
    },
    {
      "id": "R16",
      "text": "When at least one church flag is Yes, then each such player picks one of 10 options (raise or lower one of the five dice by 1), all at the same time."
    },
    {
      "id": "R17",
      "text": "When church choices are applied, then they are applied in seat order 1, 2, 3, and each die is clamped to between 1 and 6 (raising a 6 or lowering a 1 does nothing)."
    },
    {
      "id": "R18",
      "text": "When no church flag is Yes, then the church step is skipped."
    },
    {
      "id": "R19",
      "text": "When a round ends, then every church flag is reset to No and the dice, every player's gold and every public_record are announced."
    },
    {
      "id": "R20",
      "text": "When round 12 ends, then the game ends and all 36 cards have been dealt."
    },
    {
      "id": "R21",
      "text": "When the game ends, then for each colour the single player with the strictly highest true total gains VP equal to that colour's die, and a tied top scores nobody."
    },
    {
      "id": "R22",
      "text": "When the game ends, then the player with the most VP wins; a VP tie goes to the most gold; players still level share the win as a draw."
    }
  ],
  "offers": [
    {
      "question": "SPLIT",
      "who": "the active seat only",
      "options": "the 6 permutations assigning this round's 3 dealt cards to KEEP, AUCTION and GIVE, each naming the cards"
    },
    {
      "question": "TALK",
      "who": "all three seats",
      "options": "one short free-text message"
    },
    {
      "question": "BID",
      "who": "all three seats",
      "options": "a whole number from 0 to that seat's current gold"
    },
    {
      "question": "CHURCH",
      "who": "only seats whose church flag is Yes; seats with No are not asked",
      "options": "raise Red, lower Red, raise Blue, lower Blue, raise Green, lower Green, raise Yellow, lower Yellow, raise Purple, lower Purple"
    }
  ],
  "choices": [
    {
      "what": "Exactly 3 players, suggested 3",
      "why": "The designer fixed the table at 3, and the 12-round active order and next-seat cycle are written for seats 1-3, so the minimum and maximum are both 3. At 3 an auction has two rivals, and a colour majority can be contested or shared."
    },
    {
      "what": "Strategy at the table",
      "why": "A thoughtful player keeps cards that build hidden majorities and gives away cards that cannot tip a colour. They bid according to what an auction card is worth in the colours they can win, and use Church to raise colours they lead and lower colours rivals lead. They also read public records and gold changes to infer the others' hidden kept cards."
    },
    {
      "what": "Talk kept, as a simultaneous poll broadcast to all",
      "why": "The source says all three write at the same time and messages are shown together. Players disagree about who should win each auction, so talk (bluffing about majorities, proposing who drops out of bidding) has strategic weight."
    },
    {
      "what": "Church flag visibility is ally (owner only)",
      "why": "A kept Church card is face-down, so a public flag would reveal it. The rules publish only dice, gold and records."
    },
    {
      "what": "Rank expression vp*1000 + gold",
      "why": "Gold can never exceed 17 (8 at the start plus 9 from Gold cards), so the factor 1000 makes VP decide first and gold break ties. A remaining tie is a shared win, which matches the source's draw."
    },
    {
      "what": "Card representation as text like 'Red 3', 'Gold 4', 'Church'",
      "why": "The source does not name a format; text labels let the effect be read off the card."
    },
    {
      "what": "Unwon auction cards go to a public discard list",
      "why": "The source says 'discarded' without naming a pile; a list keeps the card stated somewhere."
    },
    {
      "what": "List-valued numbers (card values, active order) split into separate numeric parameters",
      "why": "Parameters must each be a single number, so each count, value and per-round active seat is listed on its own."
    }
  ],
  "simplifications": [
    {
      "what": "Colour majority scoring uses comparisons kept beside the scores (for each colour, the top total and how many players hold it)",
      "why": "The engine has no direct player-to-player attribute operand, so the workaround compares each player's total with maxima kept on the table."
    },
    {
      "what": "Dealt cards are held in a hidden table list and revealed privately to the active seat",
      "why": "A table attribute cannot be visible to one changing seat, so a private reveal provides 'shown only to the active player'."
    },
    {
      "what": "Final scoring is a round step gated by round == 12 before the ending check",
      "why": "The step list is flat; a single conditional update computes VP once, at the end."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: gold, public_record, vp; table: die_red, die_blue, die_green, die_yellow, die_purple, round, active_seat, auction_card.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
[
  {"name": "Start: gold 8, empty records, vp 0, every die 3", "rule": "R1", "players": 3, "seed": 1, "rounds": 0,
   "expect": {"players": {"1": {"gold": 8, "public_record": "", "vp": 0}, "2": {"gold": 8, "public_record": "", "vp": 0}, "3": {"gold": 8, "public_record": "", "vp": 0}},
              "game": {"die_red": 3, "die_blue": 3, "die_green": 3, "die_yellow": 3, "die_purple": 3}}},

  {"name": "Start: the deck holds 36 cards", "rule": "R2", "players": 3, "seed": 1, "rounds": 0,
   "expect": {"lens": {"game": {"deck": 36}}}},

  {"name": "Round 1 makes seat 1 active", "rule": "R3", "players": 3, "seed": 1, "rounds": 1, "default": "decline",
   "expect": {"game": {"round": 1, "active_seat": 1}}},

  {"name": "Round 6 makes seat 1 active", "rule": "R3", "players": 3, "seed": 2, "rounds": 1, "default": "decline",
   "given": {"game": {"round": 5}},
   "expect": {"game": {"round": 6, "active_seat": 1}}},

  {"name": "Round 9 makes seat 2 active", "rule": "R3", "players": 3, "seed": 3, "rounds": 1, "default": "decline",
   "given": {"game": {"round": 8}},
   "expect": {"game": {"round": 9, "active_seat": 2}}},

  {"name": "Three cards leave the deck and only the active seat splits them", "rule": "R4", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"deck": ["Red 1", "Blue 1", "Green 1"]}},
   "rules": [{"seat": 1, "options_include": "KEEP Red 1, AUCTION Blue 1, GIVE Green 1"},
             {"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"lens": {"game": {"deck": 0}},
              "not_offered": [{"seat": 2, "option": "KEEP Red 1, AUCTION Blue 1, GIVE Green 1"},
                              {"seat": 3, "option": "KEEP Red 1, AUCTION Blue 1, GIVE Green 1"}]}},

  {"name": "The active seat is offered all 6 assignments", "rule": "R5", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"deck": ["Red 1", "Blue 1", "Green 1"]}},
   "rules": [{"seat": 1, "options_include": "KEEP Green 1, AUCTION Blue 1, GIVE Red 1"},
             {"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"offered": [{"seat": 1, "option": "KEEP Red 1, AUCTION Blue 1, GIVE Green 1"},
                          {"seat": 1, "option": "KEEP Red 1, AUCTION Green 1, GIVE Blue 1"},
                          {"seat": 1, "option": "KEEP Blue 1, AUCTION Red 1, GIVE Green 1"},
                          {"seat": 1, "option": "KEEP Blue 1, AUCTION Green 1, GIVE Red 1"},
                          {"seat": 1, "option": "KEEP Green 1, AUCTION Red 1, GIVE Blue 1"},
                          {"seat": 1, "option": "KEEP Green 1, AUCTION Blue 1, GIVE Red 1"}]}},

  {"name": "A kept Red 3 lifts seat 3's red total above seat 2's 2 and scores the Red die", "rule": "R6", "players": 3, "seed": 1,
   "given": {"game": {"round": 11, "deck": ["Red 3", "Blue 1", "Green 2"], "die_red": 5},
             "players": {"2": {"red": 2}}},
   "rules": [{"seat": 3, "options_include": "KEEP Red 3, AUCTION Blue 1, GIVE Green 2"},
             {"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"winner": 3, "standings": {"1": 3008, "2": 8, "3": 5008},
              "players": {"1": {"vp": 3}, "2": {"vp": 0}, "3": {"vp": 5}}}},

  {"name": "Keeping Gold 4 raises gold by 4", "rule": "R7", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"deck": ["Gold 4", "Red 1", "Blue 1"]}},
   "rules": [{"seat": 1, "options_include": "KEEP Gold 4, AUCTION Red 1, GIVE Blue 1"},
             {"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"players": {"1": {"gold": 12}, "2": {"gold": 8}, "3": {"gold": 8}}}},

  {"name": "A kept Church gives one church action", "rule": "R8", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"deck": ["Church", "Red 1", "Blue 1"]}},
   "rules": [{"seat": 1, "options_include": "KEEP Church, AUCTION Red 1, GIVE Blue 1"},
             {"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0},
             {"seat": 1, "options_include": "raise Red"}],
   "expect": {"game": {"die_red": 4},
              "not_offered": [{"seat": 2, "option": "raise Red"}, {"seat": 3, "option": "raise Red"}]}},

  {"name": "A second Church in the same round gives no second action", "rule": "R8", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"deck": ["Church", "Church", "Red 1"]}},
   "rules": [{"seat": 1, "options_include": "KEEP Church, AUCTION Church, GIVE Red 1"},
             {"seat": 1, "options_include": 1}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0},
             {"seat": 1, "options_include": "raise Red"}],
   "expect": {"players": {"1": {"gold": 7}},
              "game": {"die_red": 4}}},

  {"name": "The kept card stays out of the public record", "rule": "R9", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"deck": ["Gold 2", "Red 1", "Blue 1"]}},
   "rules": [{"seat": 1, "options_include": "KEEP Gold 2, AUCTION Red 1, GIVE Blue 1"},
             {"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"players": {"1": {"gold": 10, "public_record": ""}}}},

  {"name": "The given Gold 3 goes from seat 1 to seat 2", "rule": "R10", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"deck": ["Gold 3", "Red 1", "Blue 1"]}},
   "rules": [{"seat": 1, "options_include": "KEEP Red 1, AUCTION Blue 1, GIVE Gold 3"},
             {"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"players": {"1": {"gold": 8, "public_record": ""}, "2": {"gold": 11}, "3": {"gold": 8, "public_record": ""}}}},

  {"name": "The given Gold 3 goes from seat 3 to seat 1", "rule": "R10", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"round": 2, "deck": ["Gold 3", "Red 1", "Blue 1"]}},
   "rules": [{"seat": 3, "options_include": "KEEP Red 1, AUCTION Blue 1, GIVE Gold 3"},
             {"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"players": {"1": {"gold": 11}, "2": {"gold": 8}, "3": {"gold": 8, "public_record": ""}}}},

  {"name": "The auction card is shown publicly", "rule": "R11", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"deck": ["Red 1", "Blue 1", "Green 1"]}},
   "rules": [{"seat": 1, "options_include": "KEEP Red 1, AUCTION Blue 1, GIVE Green 1"},
             {"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"game": {"auction_card": "Blue 1"}}},

  {"name": "Talk is not binding: the round goes on and gold is untouched", "rule": "R12", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"deck": ["Red 1", "Blue 1", "Green 1"]}},
   "rules": [{"seat": 1, "options_include": "KEEP Red 1, AUCTION Blue 1, GIVE Green 1"},
             {"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"players": {"1": {"gold": 8}, "2": {"gold": 8}, "3": {"gold": 8}}, "game": {"round": 1}}},

  {"name": "Each bid ranges from 0 to the seat's gold", "rule": "R13", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"deck": ["Red 1", "Blue 1", "Green 1"]}, "players": {"2": {"gold": 3}}},
   "rules": [{"seat": 1, "options_include": "KEEP Red 1, AUCTION Blue 1, GIVE Green 1"},
             {"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"offered": [{"seat": 1, "option": 8}, {"seat": 2, "option": 3}, {"seat": 3, "option": 8}],
              "not_offered": [{"seat": 1, "option": 9}, {"seat": 2, "option": 4}]}},

  {"name": "The sole top bidder pays 5 and gains the Gold 4", "rule": "R14", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"deck": ["Gold 4", "Red 1", "Blue 1"]}},
   "rules": [{"seat": 1, "options_include": "KEEP Red 1, AUCTION Gold 4, GIVE Blue 1"},
             {"seat": 1, "options_include": 2}, {"seat": 2, "options_include": 5}, {"seat": 3, "options_include": 0}],
   "expect": {"players": {"1": {"gold": 8}, "2": {"gold": 7}, "3": {"gold": 8}}}},

  {"name": "A tied top bid discards the card and nobody pays", "rule": "R15", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"deck": ["Gold 4", "Red 1", "Blue 1"]}},
   "rules": [{"seat": 1, "options_include": "KEEP Red 1, AUCTION Gold 4, GIVE Blue 1"},
             {"seat": 1, "options_include": 3}, {"seat": 2, "options_include": 3}, {"seat": 3, "options_include": 0}],
   "expect": {"players": {"1": {"gold": 8}, "2": {"gold": 8}, "3": {"gold": 8}}}},

  {"name": "All bids 0 discards the card and nobody pays", "rule": "R15", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"deck": ["Gold 4", "Red 1", "Blue 1"]}},
   "rules": [{"seat": 1, "options_include": "KEEP Red 1, AUCTION Gold 4, GIVE Blue 1"},
             {"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"players": {"1": {"gold": 8}, "2": {"gold": 8}, "3": {"gold": 8}}}},

  {"name": "Only the seats with church Yes move dice", "rule": "R16", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"deck": ["Red 1", "Blue 1", "Green 1"]}, "players": {"2": {"church": true}, "3": {"church": true}}},
   "rules": [{"seat": 1, "options_include": "KEEP Red 1, AUCTION Blue 1, GIVE Green 1"},
             {"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0},
             {"seat": 2, "options_include": "raise Blue"}, {"seat": 3, "options_include": "lower Green"}],
   "expect": {"game": {"die_red": 3, "die_blue": 4, "die_green": 2, "die_yellow": 3, "die_purple": 3},
              "not_offered": [{"seat": 1, "option": "raise Red"}]}},

  {"name": "Raising a die already at 6 does nothing", "rule": "R17", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"deck": ["Red 1", "Blue 1", "Green 1"], "die_red": 6}, "players": {"1": {"church": true}}},
   "rules": [{"seat": 1, "options_include": "KEEP Red 1, AUCTION Blue 1, GIVE Green 1"},
             {"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0},
             {"seat": 1, "options_include": "raise Red"}],
   "expect": {"game": {"die_red": 6}}},

  {"name": "Seat order with clamping: purple at 1, seat 1 raises and seat 2 lowers, ends at 1", "rule": "R17", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"deck": ["Red 1", "Blue 1", "Green 1"], "die_purple": 1}, "players": {"1": {"church": true}, "2": {"church": true}}},
   "rules": [{"seat": 1, "options_include": "KEEP Red 1, AUCTION Blue 1, GIVE Green 1"},
             {"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0},
             {"seat": 1, "options_include": "raise Purple"}, {"seat": 2, "options_include": "lower Purple"}],
   "expect": {"game": {"die_purple": 1}}},

  {"name": "With no church flag nobody is asked and the dice stay at 3", "rule": "R18", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"deck": ["Red 1", "Blue 1", "Green 1"]}},
   "rules": [{"seat": 1, "options_include": "KEEP Red 1, AUCTION Blue 1, GIVE Green 1"},
             {"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"game": {"die_red": 3, "die_blue": 3, "die_green": 3, "die_yellow": 3, "die_purple": 3},
              "not_offered": [{"seat": 1, "option": "raise Red"}, {"seat": 2, "option": "raise Red"}, {"seat": 3, "option": "raise Red"}]}},

  {"name": "The church flag resets after the round, so there is no church action in round 2", "rule": "R19", "players": 3, "seed": 1, "rounds": 2, "default": "decline",
   "given": {"game": {"deck": ["Red 1", "Blue 1", "Green 1", "Yellow 1", "Purple 1", "Red 2"]}, "players": {"1": {"church": true}}},
   "rules": [{"seat": 1, "options_include": "lower Red"}],
   "expect": {"game": {"round": 2, "die_red": 2, "die_blue": 3, "die_green": 3, "die_yellow": 3, "die_purple": 3}}},

  {"name": "The game ends after round 12 with the deck empty", "rule": "R20", "players": 3, "seed": 1,
   "given": {"game": {"round": 11, "deck": ["Red 1", "Blue 1", "Green 1"]}},
   "rules": [{"seat": 3, "options_include": "KEEP Red 1, AUCTION Blue 1, GIVE Green 1"},
             {"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"winner": [1, 3], "standings": {"1": 3008, "2": 8, "3": 3008},
              "game": {"round": 12}, "lens": {"game": {"deck": 0}},
              "players": {"1": {"vp": 3}, "2": {"vp": 0}, "3": {"vp": 3}}}},

  {"name": "A sole leader scores the die value and a tied top scores nobody", "rule": "R21", "players": 3, "seed": 1,
   "given": {"game": {"round": 11, "deck": ["Blue 1", "Green 1", "Yellow 1"], "die_blue": 6, "die_yellow": 2},
             "players": {"1": {"red": 2}, "2": {"red": 2}}},
   "rules": [{"seat": 3, "options_include": "KEEP Blue 1, AUCTION Green 1, GIVE Yellow 1"},
             {"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"winner": 3, "standings": {"1": 2008, "2": 8, "3": 6008},
              "players": {"1": {"vp": 2}, "2": {"vp": 0}, "3": {"vp": 6}}}},

  {"name": "A VP tie goes to the seat with the most gold", "rule": "R22", "players": 3, "seed": 1,
   "given": {"game": {"round": 11, "deck": ["Red 1", "Blue 1", "Green 1"]},
             "players": {"1": {"red": 5, "gold": 10}, "2": {"blue": 5}, "3": {"green": 5}}},
   "rules": [{"seat": 3, "options_include": "KEEP Green 1, AUCTION Red 1, GIVE Blue 1"},
             {"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"winner": 1, "standings": {"1": 3010, "2": 3008, "3": 3008},
              "players": {"1": {"vp": 3, "gold": 10}, "2": {"vp": 3}, "3": {"vp": 3}}}},

  {"name": "Level on VP and gold: all three share the win", "rule": "R22", "players": 3, "seed": 1,
   "given": {"game": {"round": 11, "deck": ["Red 1", "Blue 1", "Green 1"]},
             "players": {"1": {"red": 5}, "2": {"blue": 5}, "3": {"green": 5}}},
   "rules": [{"seat": 3, "options_include": "KEEP Green 1, AUCTION Red 1, GIVE Blue 1"},
             {"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"winner": [1, 2, 3], "standings": {"1": 3008, "2": 3008, "3": 3008}}}
]

Why it was refused: scenario 1: needs `rules` (what each seat answers, by option name); scenario 2: needs `rules` (what each seat answers, by option name); scenario 3: needs `rules` (what each seat answers, by option name); scenario 4: needs `rules` (what each seat answers, by option name); scenario 5: needs `rules` (what each seat answers, by option name)
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
[
  {"name": "Start: gold 8, vp 0, every die 3 (checked after a quiet round 1 that changes none of them)", "rule": "R1", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"deck": ["Red 1", "Blue 1", "Green 1"]}},
   "rules": [{"seat": 1, "options_include": "KEEP Red 1, AUCTION Blue 1, GIVE Green 1"},
             {"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"players": {"1": {"gold": 8, "public_record": "", "vp": 0}, "2": {"gold": 8, "vp": 0}, "3": {"gold": 8, "public_record": "", "vp": 0}},
              "game": {"die_red": 3, "die_blue": 3, "die_green": 3, "die_yellow": 3, "die_purple": 3}}},

  {"name": "Start: the deck holds 36 cards, so 33 remain after round 1's deal", "rule": "R2", "players": 3, "seed": 1, "rounds": 1, "default": "first",
   "rules": [{"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"lens": {"game": {"deck": 33}}}},

  {"name": "Round 1 makes seat 1 active", "rule": "R3", "players": 3, "seed": 1, "rounds": 1, "default": "first",
   "rules": [{"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"game": {"round": 1, "active_seat": 1}}},

  {"name": "Round 6 makes seat 1 active", "rule": "R3", "players": 3, "seed": 2, "rounds": 1, "default": "first",
   "given": {"game": {"round": 5}},
   "rules": [{"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"game": {"round": 6, "active_seat": 1}}},

  {"name": "Round 9 makes seat 2 active", "rule": "R3", "players": 3, "seed": 3, "rounds": 1, "default": "first",
   "given": {"game": {"round": 8}},
   "rules": [{"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"game": {"round": 9, "active_seat": 2}}},

  {"name": "Three cards leave the deck and only the active seat splits them", "rule": "R4", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"deck": ["Red 1", "Blue 1", "Green 1"]}},
   "rules": [{"seat": 1, "options_include": "KEEP Red 1, AUCTION Blue 1, GIVE Green 1"},
             {"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"lens": {"game": {"deck": 0}},
              "not_offered": [{"seat": 2, "option": "KEEP Red 1, AUCTION Blue 1, GIVE Green 1"},
                              {"seat": 3, "option": "KEEP Red 1, AUCTION Blue 1, GIVE Green 1"}]}},

  {"name": "The active seat is offered all 6 assignments", "rule": "R5", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"deck": ["Red 1", "Blue 1", "Green 1"]}},
   "rules": [{"seat": 1, "options_include": "KEEP Green 1, AUCTION Blue 1, GIVE Red 1"},
             {"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"offered": [{"seat": 1, "option": "KEEP Red 1, AUCTION Blue 1, GIVE Green 1"},
                          {"seat": 1, "option": "KEEP Red 1, AUCTION Green 1, GIVE Blue 1"},
                          {"seat": 1, "option": "KEEP Blue 1, AUCTION Red 1, GIVE Green 1"},
                          {"seat": 1, "option": "KEEP Blue 1, AUCTION Green 1, GIVE Red 1"},
                          {"seat": 1, "option": "KEEP Green 1, AUCTION Red 1, GIVE Blue 1"},
                          {"seat": 1, "option": "KEEP Green 1, AUCTION Blue 1, GIVE Red 1"}]}},

  {"name": "A kept Red 3 lifts seat 3's red total above seat 2's 2 and scores the Red die", "rule": "R6", "players": 3, "seed": 1,
   "given": {"game": {"round": 11, "deck": ["Red 3", "Blue 1", "Green 2"], "die_red": 5},
             "players": {"2": {"red": 2}}},
   "rules": [{"seat": 3, "options_include": "KEEP Red 3, AUCTION Blue 1, GIVE Green 2"},
             {"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"winner": 3, "standings": {"1": 3008, "2": 8, "3": 5008},
              "players": {"1": {"vp": 3}, "2": {"vp": 0}, "3": {"vp": 5}}}},

  {"name": "Keeping Gold 4 raises gold by 4", "rule": "R7", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"deck": ["Gold 4", "Red 1", "Blue 1"]}},
   "rules": [{"seat": 1, "options_include": "KEEP Gold 4, AUCTION Red 1, GIVE Blue 1"},
             {"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"players": {"1": {"gold": 12}, "2": {"gold": 8}, "3": {"gold": 8}}}},

  {"name": "A kept Church gives one church action", "rule": "R8", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"deck": ["Church", "Red 1", "Blue 1"]}},
   "rules": [{"seat": 1, "options_include": "KEEP Church, AUCTION Red 1, GIVE Blue 1"},
             {"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0},
             {"seat": 1, "options_include": "raise Red"}],
   "expect": {"game": {"die_red": 4},
              "not_offered": [{"seat": 2, "option": "raise Red"}, {"seat": 3, "option": "raise Red"}]}},

  {"name": "A second Church in the same round gives no second action", "rule": "R8", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"deck": ["Church", "Church", "Red 1"]}},
   "rules": [{"seat": 1, "options_include": "KEEP Church, AUCTION Church, GIVE Red 1"},
             {"seat": 1, "options_include": 1}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0},
             {"seat": 1, "options_include": "raise Red"}],
   "expect": {"players": {"1": {"gold": 7}},
              "game": {"die_red": 4}}},

  {"name": "The kept card stays out of the public record", "rule": "R9", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"deck": ["Gold 2", "Red 1", "Blue 1"]}},
   "rules": [{"seat": 1, "options_include": "KEEP Gold 2, AUCTION Red 1, GIVE Blue 1"},
             {"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"players": {"1": {"gold": 10, "public_record": ""}}}},

  {"name": "The given Gold 3 goes from seat 1 to seat 2", "rule": "R10", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"deck": ["Gold 3", "Red 1", "Blue 1"]}},
   "rules": [{"seat": 1, "options_include": "KEEP Red 1, AUCTION Blue 1, GIVE Gold 3"},
             {"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"players": {"1": {"gold": 8, "public_record": ""}, "2": {"gold": 11}, "3": {"gold": 8, "public_record": ""}}}},

  {"name": "The given Gold 3 goes from seat 3 to seat 1", "rule": "R10", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"round": 2, "deck": ["Gold 3", "Red 1", "Blue 1"]}},
   "rules": [{"seat": 3, "options_include": "KEEP Red 1, AUCTION Blue 1, GIVE Gold 3"},
             {"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"players": {"1": {"gold": 11}, "2": {"gold": 8}, "3": {"gold": 8, "public_record": ""}}}},

  {"name": "The auction card is shown publicly", "rule": "R11", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"deck": ["Red 1", "Blue 1", "Green 1"]}},
   "rules": [{"seat": 1, "options_include": "KEEP Red 1, AUCTION Blue 1, GIVE Green 1"},
             {"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"game": {"auction_card": "Blue 1"}}},

  {"name": "Talk is not binding: the round goes on and gold is untouched", "rule": "R12", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"deck": ["Red 1", "Blue 1", "Green 1"]}},
   "rules": [{"seat": 1, "options_include": "KEEP Red 1, AUCTION Blue 1, GIVE Green 1"},
             {"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"players": {"1": {"gold": 8}, "2": {"gold": 8}, "3": {"gold": 8}}, "game": {"round": 1}}},

  {"name": "Each bid ranges from 0 to the seat's gold", "rule": "R13", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"deck": ["Red 1", "Blue 1", "Green 1"]}, "players": {"2": {"gold": 3}}},
   "rules": [{"seat": 1, "options_include": "KEEP Red 1, AUCTION Blue 1, GIVE Green 1"},
             {"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"offered": [{"seat": 1, "option": 8}, {"seat": 2, "option": 3}, {"seat": 3, "option": 8}],
              "not_offered": [{"seat": 1, "option": 9}, {"seat": 2, "option": 4}]}},

  {"name": "The sole top bidder pays 5 and gains the Gold 4", "rule": "R14", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"deck": ["Gold 4", "Red 1", "Blue 1"]}},
   "rules": [{"seat": 1, "options_include": "KEEP Red 1, AUCTION Gold 4, GIVE Blue 1"},
             {"seat": 1, "options_include": 2}, {"seat": 2, "options_include": 5}, {"seat": 3, "options_include": 0}],
   "expect": {"players": {"1": {"gold": 8}, "2": {"gold": 7}, "3": {"gold": 8}}}},

  {"name": "A tied top bid discards the card and nobody pays", "rule": "R15", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"deck": ["Gold 4", "Red 1", "Blue 1"]}},
   "rules": [{"seat": 1, "options_include": "KEEP Red 1, AUCTION Gold 4, GIVE Blue 1"},
             {"seat": 1, "options_include": 3}, {"seat": 2, "options_include": 3}, {"seat": 3, "options_include": 0}],
   "expect": {"players": {"1": {"gold": 8}, "2": {"gold": 8}, "3": {"gold": 8}}}},

  {"name": "All bids 0 discards the card and nobody pays", "rule": "R15", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"deck": ["Gold 4", "Red 1", "Blue 1"]}},
   "rules": [{"seat": 1, "options_include": "KEEP Red 1, AUCTION Gold 4, GIVE Blue 1"},
             {"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"players": {"1": {"gold": 8}, "2": {"gold": 8}, "3": {"gold": 8}}}},

  {"name": "Only the seats with church Yes move dice", "rule": "R16", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"deck": ["Red 1", "Blue 1", "Green 1"]}, "players": {"2": {"church": true}, "3": {"church": true}}},
   "rules": [{"seat": 1, "options_include": "KEEP Red 1, AUCTION Blue 1, GIVE Green 1"},
             {"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0},
             {"seat": 2, "options_include": "raise Blue"}, {"seat": 3, "options_include": "lower Green"}],
   "expect": {"game": {"die_red": 3, "die_blue": 4, "die_green": 2, "die_yellow": 3, "die_purple": 3},
              "not_offered": [{"seat": 1, "option": "raise Red"}]}},

  {"name": "Raising a die already at 6 does nothing", "rule": "R17", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"deck": ["Red 1", "Blue 1", "Green 1"], "die_red": 6}, "players": {"1": {"church": true}}},
   "rules": [{"seat": 1, "options_include": "KEEP Red 1, AUCTION Blue 1, GIVE Green 1"},
             {"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0},
             {"seat": 1, "options_include": "raise Red"}],
   "expect": {"game": {"die_red": 6}}},

  {"name": "Seat order with clamping: purple at 1, seat 1 raises and seat 2 lowers, ends at 1", "rule": "R17", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"deck": ["Red 1", "Blue 1", "Green 1"], "die_purple": 1}, "players": {"1": {"church": true}, "2": {"church": true}}},
   "rules": [{"seat": 1, "options_include": "KEEP Red 1, AUCTION Blue 1, GIVE Green 1"},
             {"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0},
             {"seat": 1, "options_include": "raise Purple"}, {"seat": 2, "options_include": "lower Purple"}],
   "expect": {"game": {"die_purple": 1}}},

  {"name": "With no church flag nobody is asked and the dice stay at 3", "rule": "R18", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"deck": ["Red 1", "Blue 1", "Green 1"]}},
   "rules": [{"seat": 1, "options_include": "KEEP Red 1, AUCTION Blue 1, GIVE Green 1"},
             {"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"game": {"die_red": 3, "die_blue": 3, "die_green": 3, "die_yellow": 3, "die_purple": 3},
              "not_offered": [{"seat": 1, "option": "raise Red"}, {"seat": 2, "option": "raise Red"}, {"seat": 3, "option": "raise Red"}]}},

  {"name": "The church flag resets after the round, so there is no church action in round 2", "rule": "R19", "players": 3, "seed": 1, "rounds": 2, "default": "decline",
   "given": {"game": {"deck": ["Red 1", "Blue 1", "Green 1", "Yellow 1", "Purple 1", "Red 2"]}, "players": {"1": {"church": true}}},
   "rules": [{"seat": 1, "options_include": "lower Red"}],
   "expect": {"game": {"round": 2, "die_red": 2, "die_blue": 3, "die_green": 3, "die_yellow": 3, "die_purple": 3}}},

  {"name": "The game ends after round 12 with the deck empty", "rule": "R20", "players": 3, "seed": 1,
   "given": {"game": {"round": 11, "deck": ["Red 1", "Blue 1", "Green 1"]}},
   "rules": [{"seat": 3, "options_include": "KEEP Red 1, AUCTION Blue 1, GIVE Green 1"},
             {"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"winner": [1, 3], "standings": {"1": 3008, "2": 8, "3": 3008},
              "game": {"round": 12}, "lens": {"game": {"deck": 0}},
              "players": {"1": {"vp": 3}, "2": {"vp": 0}, "3": {"vp": 3}}}},

  {"name": "A sole leader scores the die value and a tied top scores nobody", "rule": "R21", "players": 3, "seed": 1,
   "given": {"game": {"round": 11, "deck": ["Blue 1", "Green 1", "Yellow 1"], "die_blue": 6, "die_yellow": 2},
             "players": {"1": {"red": 2}, "2": {"red": 2}}},
   "rules": [{"seat": 3, "options_include": "KEEP Blue 1, AUCTION Green 1, GIVE Yellow 1"},
             {"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"winner": 3, "standings": {"1": 2008, "2": 8, "3": 6008},
              "players": {"1": {"vp": 2}, "2": {"vp": 0}, "3": {"vp": 6}}}},

  {"name": "A VP tie goes to the seat with the most gold", "rule": "R22", "players": 3, "seed": 1,
   "given": {"game": {"round": 11, "deck": ["Red 1", "Blue 1", "Green 1"]},
             "players": {"1": {"red": 5, "gold": 10}, "2": {"blue": 5}, "3": {"green": 5}}},
   "rules": [{"seat": 3, "options_include": "KEEP Green 1, AUCTION Red 1, GIVE Blue 1"},
             {"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"winner": 1, "standings": {"1": 3010, "2": 3008, "3": 3008},
              "players": {"1": {"vp": 3, "gold": 10}, "2": {"vp": 3}, "3": {"vp": 3}}}},

  {"name": "Level on VP and gold: all three share the win", "rule": "R22", "players": 3, "seed": 1,
   "given": {"game": {"round": 11, "deck": ["Red 1", "Blue 1", "Green 1"]},
             "players": {"1": {"red": 5}, "2": {"blue": 5}, "3": {"green": 5}}},
   "rules": [{"seat": 3, "options_include": "KEEP Green 1, AUCTION Red 1, GIVE Blue 1"},
             {"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"winner": [1, 2, 3], "standings": {"1": 3008, "2": 3008, "3": 3008}}}
]
````
