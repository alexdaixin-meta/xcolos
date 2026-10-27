# 46 scenarios

- time: 2026-10-27T18:05:51+00:00 (58.8s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 ddf5695da68f51fe, reply sha256 67d89f7c33f7094f

## Sent

````
SPEC:
{
  "name": "Biblios: The Scriptorium (revised)",
  "summary": "Three scribes take turns splitting a three-card deal into a kept card, a lot that everyone bids on and a gift for a rival. They collect colour cards to win colours and play Church cards to move each colour's VP die.",
  "players": {
    "min": 3,
    "max": 3,
    "suggested": 3
  },
  "parameters": {
    "deck_size": 36,
    "colours": 3,
    "colour_cards_per_colour": 7,
    "colour_value_1_copies": 2,
    "colour_value_2_copies": 2,
    "colour_value_3_copies": 2,
    "colour_value_4_copies": 1,
    "colour_total_per_colour": 16,
    "gold_cards": 9,
    "gold_value_1_copies": 3,
    "gold_value_2_copies": 3,
    "gold_value_3_copies": 3,
    "gold_cards_total": 18,
    "church_cards": 6,
    "starting_gold": 4,
    "die_start": 3,
    "die_min": 1,
    "die_max": 5,
    "rounds": 12,
    "cards_per_round": 3,
    "bid_min": 0,
    "bid_max": 22,
    "max_church_per_player_per_round": 2,
    "rank_vp_weight": 100
  },
  "attributes": {
    "player": [
      {
        "key": "gold",
        "type": "number",
        "visible": "ally",
        "initial": 4,
        "meaning": "Gold coins held. Only the owner sees it.",
        "observable": false
      },
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "Colour cards held face-down, such as 'Red 3'",
        "observable": false
      },
      {
        "key": "offer",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "The 3 dealt cards in positions 1, 2 and 3. Filled only for the active player during the deal.",
        "observable": false
      },
      {
        "key": "new_cards",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "Cards that entered this player's hand this round (keep, lot or gift)",
        "observable": false
      },
      {
        "key": "bid",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "This round's sealed bid. Revealed to all after the sale.",
        "observable": false
      },
      {
        "key": "effective_bid",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "min(bid, gold): the bid as it counts",
        "observable": false
      },
      {
        "key": "church_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Church cards that entered this player's hand this round (0, 1 or 2)",
        "observable": true
      },
      {
        "key": "church_choice",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "This round's Church choice. Announced after the dice move.",
        "observable": false
      },
      {
        "key": "red_sum",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "Total value of Red cards in hand, computed at scoring",
        "observable": false
      },
      {
        "key": "green_sum",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "Total value of Green cards in hand, computed at scoring",
        "observable": false
      },
      {
        "key": "blue_sum",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "Total value of Blue cards in hand, computed at scoring",
        "observable": false
      },
      {
        "key": "vp",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Victory points scored at the end",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": "the 36 cards: Red/Green/Blue 1,1,2,2,3,3,4; Gold 1,1,1,2,2,2,3,3,3; Church x6",
        "meaning": "Face-down shuffled deck",
        "observable": false
      },
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Current round, 1 to 12",
        "observable": true
      },
      {
        "key": "active_seat",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat of the active player this round",
        "observable": true
      },
      {
        "key": "lot",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The card being auctioned this round",
        "observable": true
      },
      {
        "key": "gift",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The card given away this round",
        "observable": true
      },
      {
        "key": "lot_winner",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat that won the lot this round",
        "observable": false
      },
      {
        "key": "gift_receiver",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat that received the gift this round",
        "observable": false
      },
      {
        "key": "vp_red",
        "type": "number",
        "visible": "public",
        "initial": 3,
        "meaning": "Red VP die, from 1 to 5",
        "observable": true
      },
      {
        "key": "vp_green",
        "type": "number",
        "visible": "public",
        "initial": 3,
        "meaning": "Green VP die, from 1 to 5",
        "observable": true
      },
      {
        "key": "vp_blue",
        "type": "number",
        "visible": "public",
        "initial": 3,
        "meaning": "Blue VP die, from 1 to 5",
        "observable": true
      }
    ]
  },
  "setup": [
    "The deck list is filled with the 36 cards: 'Red 1', 'Red 1', 'Red 2', 'Red 2', 'Red 3', 'Red 3', 'Red 4' and the same for Green and Blue; 'Gold 1' x3, 'Gold 2' x3, 'Gold 3' x3; and 'Church' x6. Everyone is told the composition, but the order is hidden.",
    "Each player gets gold 4, an empty hand and church_count 0.",
    "vp_red, vp_green and vp_blue are set to 3.",
    "Seats are P1, P2 and P3. Clockwise order is P1 -> P2 -> P3 -> P1."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round += 1; active_seat = ((round - 1) mod 3) + 1. Announce 'Round {round}: seat {active_seat} is active.'"
    },
    {
      "action": "update",
      "who": "seat active_seat",
      "answer": null,
      "effect": "Draw 3 cards at random from deck into the active player's offer, as positions 1, 2 and 3, and remove them from deck. Only the active player sees offer."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "short text",
      "effect": "Each message is broadcast to all as 'Seat {seat} says: {value}'. Talk is not binding."
    },
    {
      "action": "ask",
      "who": "seat active_seat",
      "answer": "one of: 'keep 1 sell 2', 'keep 1 sell 3', 'keep 2 sell 1', 'keep 2 sell 3', 'keep 3 sell 1', 'keep 3 sell 2'",
      "effect": "The keep card is appended to the active player's hand and new_cards. lot = the sell card. gift = the remaining card. offer = []."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce 'Lot: {lot}. Gift: {gift}.' The kept card stays secret."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "whole number 0 to 22",
      "effect": "bid = answer; effective_bid = min(bid, gold)."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "lot_winner = the seat with the highest effective_bid. On a tie, the active seat wins if it is among the tied; otherwise the tied seat that comes first clockwise after the active seat wins. If all bid 0, the active seat wins. The winner's gold -= the winner's effective_bid. lot is appended to the winner's hand and new_cards. All three bids are announced."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "If lot_winner != active_seat: gift_receiver = the non-active seat that is not lot_winner. Otherwise gift_receiver = the non-active seat with the lower effective_bid; on a tie, the seat next clockwise after active_seat. gift is appended to gift_receiver's hand and new_cards. Announce the receiver."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "For each player, each 'Gold N' card in new_cards is removed from hand, and gold += N."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "For each player, church_count = the number of 'Church' cards in new_cards, and those cards are removed from hand. Announce each church_count."
    },
    {
      "action": "poll",
      "who": "each player with church_count >= 1",
      "answer": "one of: 'red up', 'red down', 'green up', 'green down', 'blue up', 'blue down'",
      "effect": "church_choice = answer."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "net = the sum of church_count over players with church_choice 'red up' minus the sum over players with 'red down'; vp_red = min(5, max(1, vp_red + net))."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "net = the sum of church_count over 'green up' minus the sum over 'green down'; vp_green = min(5, max(1, vp_green + net))."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "net = the sum of church_count over 'blue up' minus the sum over 'blue down'; vp_blue = min(5, max(1, vp_blue + net)). Announce vp_red, vp_green, vp_blue and each player's church_choice."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "For every player: church_count = 0, bid = 0, effective_bid = 0, church_choice = '', new_cards = []. Set lot = '', gift = '', lot_winner = 0 and gift_receiver = 0."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Runs only when round == 12. For each player: red_sum, green_sum and blue_sum = the totals of that colour's card values in hand. For each colour, the player with the strictly highest sum gets vp += that colour's die value (vp_red, vp_green or vp_blue). If the highest is tied, nobody scores that colour. Announce each vp and gold."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "If round == 12, end the game; otherwise start the next round."
    }
  ],
  "ending": {
    "condition": "round == 12",
    "rank_by": "you.vp * 100 + you.gold",
    "decided_by": "The most VP wins. A VP tie is broken by the most remaining Gold. Players still tied share the win, which is a draw among them."
  },
  "rules": [
    {
      "id": "R1",
      "text": "At setup, the deck holds 36 cards: Red, Green and Blue each 1,1,2,2,3,3,4; Gold 1,1,1,2,2,2,3,3,3; and 6 Church cards."
    },
    {
      "id": "R2",
      "text": "At setup, each player has 4 gold, an empty hand and church_count 0, and vp_red, vp_green and vp_blue are each 3."
    },
    {
      "id": "R3",
      "text": "When the round is 1, 4, 7 or 10, then P1 is active; when it is 2, 5, 8 or 11, then P2 is active; when it is 3, 6, 9 or 12, then P3 is active."
    },
    {
      "id": "R4",
      "text": "At the start of each round, 3 cards are removed from the deck and shown only to the active player, so after round r the deck holds 36 - 3r cards."
    },
    {
      "id": "R5",
      "text": "When the active player chooses 'keep X sell Y', then card X goes into their hand, card Y becomes the lot, and the third card becomes the gift."
    },
    {
      "id": "R6",
      "text": "Each round, every player sends one talk message at the same time, and all messages are shown to everyone with their authors."
    },
    {
      "id": "R7",
      "text": "When a player bids more than their gold, then the bid counts as exactly their gold."
    },
    {
      "id": "R8",
      "text": "The highest effective bid wins the lot, and the winner's gold drops by that bid."
    },
    {
      "id": "R9",
      "text": "When the highest bid is tied and the active player is among the tied, then the active player wins the lot; otherwise the tied player first clockwise after the active player wins."
    },
    {
      "id": "R10",
      "text": "When all three players bid 0, then the active player wins the lot and pays 0."
    },
    {
      "id": "R11",
      "text": "When a non-active player wins the lot, then the gift goes to the other non-active player."
    },
    {
      "id": "R12",
      "text": "When the active player wins the lot, then the gift goes to the non-active player with the lower bid, or on a tie to the player next clockwise after the active player."
    },
    {
      "id": "R13",
      "text": "When a Gold N card enters a hand, then it is removed from that hand and the player's gold rises by N."
    },
    {
      "id": "R14",
      "text": "When Church cards enter a player's hand in a round, then church_count equals their number (0 to 2) and they are removed from the hand."
    },
    {
      "id": "R15",
      "text": "Each player with church_count >= 1 makes exactly one choice among red, green or blue, up or down; players with church_count 0 do not choose."
    },
    {
      "id": "R16",
      "text": "Each die moves by the summed church_count of its 'up' choosers minus that of its 'down' choosers, clamped to between 1 and 5 (for example 4 + 2 -> 5, and 2 - 2 -> 1)."
    },
    {
      "id": "R17",
      "text": "At the end of each round, every church_count, bid and church_choice is reset."
    },
    {
      "id": "R18",
      "text": "When round 12 ends, then the game ends and scoring happens."
    },
    {
      "id": "R19",
      "text": "At scoring, the player with the strictly highest sum in a colour gains VP equal to that colour's die value; when the highest is tied, nobody scores that colour."
    },
    {
      "id": "R20",
      "text": "The most VP wins, ties are broken by the most gold, and players still tied share a draw."
    }
  ],
  "offers": [
    {
      "question": "Talk message",
      "who": "all players",
      "options": "any short text"
    },
    {
      "question": "Split",
      "who": "the active seat only",
      "options": "'keep 1 sell 2', 'keep 1 sell 3', 'keep 2 sell 1', 'keep 2 sell 3', 'keep 3 sell 1', 'keep 3 sell 2'"
    },
    {
      "question": "Bid",
      "who": "all players, including the active seat",
      "options": "a whole number from 0 to 22"
    },
    {
      "question": "Church choice",
      "who": "only seats with church_count >= 1; seats with church_count 0 are not asked",
      "options": "'red up', 'red down', 'green up', 'green down', 'blue up', 'blue down'"
    }
  ],
  "choices": [
    {
      "what": "3 players (min 3, max 3, suggested 3)",
      "why": "The designer fixed 3 seats. The active rotation, the gift rules (lot to one non-active player, gift to the other) and the 36-card deck (12 rounds x 3 cards) only work at exactly 3."
    },
    {
      "what": "Bid upper limit of 22",
      "why": "The rules say bids run from 0 upward. 22 is the most gold a player can ever hold (4 + 18), and any higher bid would count as the player's whole gold anyway."
    },
    {
      "what": "Talk is a simultaneous poll broadcast to all",
      "why": "The rules say messages are written at the same time without seeing the others. Talk earns its place because players disagree about colours and dice, and bluffing about the kept card matters."
    },
    {
      "what": "Ranking expression vp * 100 + gold",
      "why": "Gold never exceeds 22, so this ranks by VP first and gold second, and a full tie shares the win as the rules' draw."
    },
    {
      "what": "The gift tie-break and lot comparisons use effective bids",
      "why": "The rules say a bid above a player's gold counts as exactly their gold."
    },
    {
      "what": "Dealt cards are stored in a per-player offer list",
      "why": "The cards must be visible only to the active player, which a public or hidden table attribute cannot express."
    },
    {
      "what": "Card values are listed as numeric copy counts in parameters",
      "why": "Parameters must be numbers, so the value lists 1,1,2,2,3,3,4 and 1,1,1,2,2,2,3,3,3 are given as the number of copies of each value."
    }
  ],
  "simplifications": [
    {
      "what": "Scoring runs as a conditional update in round 12, before the end check",
      "why": "The engine's round is a flat list, so a step with a 'round == 12' condition does the scoring before the game ends."
    },
    {
      "what": "Cards entering a hand are tracked in a scratch new_cards list",
      "why": "The Gold and Church steps act on cards that entered a hand this round, so this needs explicit state."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: church_count, vp; table: round, active_seat, lot, gift, vp_red, vp_green, vp_blue.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
[
  {"name": "R1: the deck holds 36 cards right after setup", "rule": "R1", "players": 3, "rounds": 0,
   "expect": {"lens": {"game": {"deck": 36}, "players": {"1": {"hand": 0}, "2": {"hand": 0}, "3": {"hand": 0}}}}},

  {"name": "R2: setup gives each player 4 gold, an empty hand, church_count 0, and every die is at 3", "rule": "R2", "players": 3, "rounds": 0,
   "expect": {"standings": {"1": 4, "2": 4, "3": 4},
              "players": {"1": {"church_count": 0, "vp": 0}, "2": {"church_count": 0, "vp": 0}, "3": {"church_count": 0, "vp": 0}},
              "game": {"vp_red": 3, "vp_green": 3, "vp_blue": 3},
              "lens": {"players": {"1": {"hand": 0}, "2": {"hand": 0}, "3": {"hand": 0}}}}},

  {"name": "R3: round 4 makes P1 active", "rule": "R3", "players": 3, "rounds": 1, "default": "decline",
   "given": {"game": {"round": 3}},
   "expect": {"game": {"round": 4, "active_seat": 1}}},

  {"name": "R3: round 5 makes P2 active", "rule": "R3", "players": 3, "rounds": 1, "default": "decline",
   "given": {"game": {"round": 4}},
   "expect": {"game": {"round": 5, "active_seat": 2}}},

  {"name": "R3: round 6 makes P3 active", "rule": "R3", "players": 3, "rounds": 1, "default": "decline",
   "given": {"game": {"round": 5}},
   "expect": {"game": {"round": 6, "active_seat": 3}}},

  {"name": "R4: the deck holds 33 cards after round 1 (chance cannot change this count)", "rule": "R4", "players": 3, "rounds": 1, "default": "decline",
   "expect": {"lens": {"game": {"deck": 33}}, "game": {"round": 1}}},

  {"name": "R4: the deck holds 30 cards after round 2 (chance cannot change this count)", "rule": "R4", "players": 3, "rounds": 2, "default": "decline",
   "expect": {"lens": {"game": {"deck": 30}}, "game": {"round": 2}}},

  {"name": "R5: the keep, lot and gift cards each go to a different seat", "rule": "R5", "players": 3, "rounds": 1, "default": "decline",
   "given": {"game": {"deck": ["Red 1", "Red 1", "Red 1"]}},
   "rules": [{"seat": 1, "options_include": "keep 1 sell 2"},
             {"seat": 2, "options_include": 2, "answer": 2},
             {"seat": 1, "options_include": 0, "answer": 0},
             {"seat": 3, "options_include": 0, "answer": 0}],
   "expect": {"lens": {"game": {"deck": 0}, "players": {"1": {"hand": 1}, "2": {"hand": 1}, "3": {"hand": 1}}},
              "standings": {"1": 4, "2": 2, "3": 4}}},

  {"name": "R6: a round with talk plays through normally", "rule": "R6", "players": 3, "rounds": 1, "default": "decline",
   "expect": {"game": {"round": 1, "active_seat": 1}, "lens": {"game": {"deck": 33}}}},

  {"name": "R7: a bid of 22 with 4 gold counts as 4 and costs 4", "rule": "R7", "players": 3, "rounds": 1, "default": "decline",
   "given": {"game": {"deck": ["Red 1", "Red 1", "Red 1"]}},
   "rules": [{"seat": 1, "options_include": "keep 1 sell 2"},
             {"seat": 1, "options_include": 0, "answer": 0},
             {"seat": 2, "options_include": 22, "answer": 22},
             {"seat": 3, "options_include": 3, "answer": 3}],
   "expect": {"standings": {"1": 4, "2": 0, "3": 4},
              "lens": {"players": {"1": {"hand": 1}, "2": {"hand": 1}, "3": {"hand": 1}}}}},

  {"name": "R8: the highest bid wins the lot and the winner pays it", "rule": "R8", "players": 3, "rounds": 1, "default": "decline",
   "given": {"game": {"deck": ["Red 1", "Red 1", "Red 1"]}},
   "rules": [{"seat": 1, "options_include": "keep 2 sell 3"},
             {"seat": 1, "options_include": 0, "answer": 0},
             {"seat": 2, "options_include": 2, "answer": 2},
             {"seat": 3, "options_include": 3, "answer": 3}],
   "expect": {"standings": {"1": 4, "2": 4, "3": 1},
              "lens": {"players": {"1": {"hand": 1}, "2": {"hand": 1}, "3": {"hand": 1}}}}},

  {"name": "R9: a tie between non-active seats goes to the first seat clockwise after the active seat (P2 active, P3 beats P1)", "rule": "R9", "players": 3, "rounds": 1, "default": "decline",
   "given": {"game": {"round": 1, "deck": ["Red 1", "Red 1", "Red 1"]}},
   "rules": [{"seat": 2, "options_include": "keep 1 sell 2"},
             {"seat": 2, "options_include": 0, "answer": 0},
             {"seat": 1, "options_include": 3, "answer": 3},
             {"seat": 3, "options_include": 3, "answer": 3}],
   "expect": {"game": {"active_seat": 2},
              "standings": {"1": 4, "2": 4, "3": 1},
              "lens": {"players": {"1": {"hand": 1}, "2": {"hand": 1}, "3": {"hand": 1}}}}},

  {"name": "R9: a tie that includes the active seat goes to the active seat", "rule": "R9", "players": 3, "rounds": 1, "default": "decline",
   "given": {"game": {"deck": ["Red 1", "Red 1", "Red 1"]}},
   "rules": [{"seat": 1, "options_include": "keep 1 sell 2"},
             {"seat": 1, "options_include": 2, "answer": 2},
             {"seat": 2, "options_include": 1, "answer": 1},
             {"seat": 3, "options_include": 2, "answer": 2}],
   "expect": {"standings": {"1": 2, "2": 4, "3": 4},
              "lens": {"players": {"1": {"hand": 2}, "2": {"hand": 1}, "3": {"hand": 0}}}}},

  {"name": "R10: when all three bid 0, the active seat wins the lot and pays nothing", "rule": "R10", "players": 3, "rounds": 1, "default": "decline",
   "given": {"game": {"deck": ["Red 1", "Red 1", "Red 1"]}},
   "rules": [{"seat": 1, "options_include": "keep 1 sell 2"},
             {"seat": 1, "options_include": 0, "answer": 0},
             {"seat": 2, "options_include": 0, "answer": 0},
             {"seat": 3, "options_include": 0, "answer": 0}],
   "expect": {"standings": {"1": 4, "2": 4, "3": 4},
              "lens": {"players": {"1": {"hand": 2}, "2": {"hand": 1}, "3": {"hand": 0}}}}},

  {"name": "R11: when a non-active seat wins the lot, the other non-active seat gets the gift (P3 active, P1 wins)", "rule": "R11", "players": 3, "rounds": 1, "default": "decline",
   "given": {"game": {"round": 2, "deck": ["Red 1", "Red 1", "Red 1"]}},
   "rules": [{"seat": 3, "options_include": "keep 3 sell 1"},
             {"seat": 1, "options_include": 1, "answer": 1},
             {"seat": 2, "options_include": 0, "answer": 0},
             {"seat": 3, "options_include": 0, "answer": 0}],
   "expect": {"game": {"active_seat": 3},
              "standings": {"1": 3, "2": 4, "3": 4},
              "lens": {"players": {"1": {"hand": 1}, "2": {"hand": 1}, "3": {"hand": 1}}}}},

  {"name": "R12: when the active seat wins the lot, the gift goes to the non-active seat with the lower bid", "rule": "R12", "players": 3, "rounds": 1, "default": "decline",
   "given": {"game": {"deck": ["Red 1", "Red 1", "Red 1"]}},
   "rules": [{"seat": 1, "options_include": "keep 1 sell 2"},
             {"seat": 1, "options_include": 3, "answer": 3},
             {"seat": 2, "options_include": 2, "answer": 2},
             {"seat": 3, "options_include": 1, "answer": 1}],
   "expect": {"standings": {"1": 1, "2": 4, "3": 4},
              "lens": {"players": {"1": {"hand": 2}, "2": {"hand": 0}, "3": {"hand": 1}}}}},

  {"name": "R13: Gold cards leave the hand and add their value to gold", "rule": "R13", "players": 3, "rounds": 1, "default": "decline",
   "given": {"game": {"deck": ["Gold 2", "Gold 2", "Gold 2"]}},
   "rules": [{"seat": 1, "options_include": "keep 1 sell 2"},
             {"seat": 1, "options_include": 0, "answer": 0},
             {"seat": 2, "options_include": 0, "answer": 0},
             {"seat": 3, "options_include": 0, "answer": 0}],
   "expect": {"standings": {"1": 8, "2": 6, "3": 4},
              "lens": {"players": {"1": {"hand": 0}, "2": {"hand": 0}, "3": {"hand": 0}}}}},

  {"name": "R14: two Church cards give a church_count of 2 (the die moves by 2) and Church cards leave the hand", "rule": "R14", "players": 3, "rounds": 1, "default": "decline",
   "given": {"game": {"deck": ["Church", "Church", "Church"]}},
   "rules": [{"seat": 1, "options_include": "keep 1 sell 2"},
             {"seat": 1, "options_include": 0, "answer": 0},
             {"seat": 2, "options_include": 0, "answer": 0},
             {"seat": 3, "options_include": 0, "answer": 0},
             {"seat": 1, "options_include": "green down"},
             {"seat": 2, "options_include": "blue up"}],
   "expect": {"game": {"vp_red": 3, "vp_green": 1, "vp_blue": 4},
              "lens": {"players": {"1": {"hand": 0}, "2": {"hand": 0}, "3": {"hand": 0}}}}},

  {"name": "R15: only seats with Church cards choose; a seat with church_count 0 is not asked", "rule": "R15", "players": 3, "rounds": 1, "default": "decline",
   "given": {"game": {"deck": ["Church", "Church", "Church"]}},
   "rules": [{"seat": 1, "options_include": "keep 1 sell 2"},
             {"seat": 1, "options_include": 0, "answer": 0},
             {"seat": 2, "options_include": 0, "answer": 0},
             {"seat": 3, "options_include": 0, "answer": 0},
             {"seat": 1, "options_include": "red up"},
             {"seat": 2, "options_include": "red up"}],
   "expect": {"offered": [{"seat": 1, "option": "red up"}, {"seat": 2, "option": "red up"}],
              "not_offered": [{"seat": 3, "option": "red up"}, {"seat": 3, "option": "blue down"}],
              "game": {"vp_red": 5, "vp_green": 3, "vp_blue": 3}}},

  {"name": "R16: 4 + 2 + 1 is clamped to 5", "rule": "R16", "players": 3, "rounds": 1, "default": "decline",
   "given": {"game": {"deck": ["Church", "Church", "Church"], "vp_red": 4}},
   "rules": [{"seat": 1, "options_include": "keep 1 sell 2"},
             {"seat": 1, "options_include": 0, "answer": 0},
             {"seat": 2, "options_include": 0, "answer": 0},
             {"seat": 3, "options_include": 0, "answer": 0},
             {"seat": 1, "options_include": "red up"},
             {"seat": 2, "options_include": "red up"}],
   "expect": {"game": {"vp_red": 5, "vp_green": 3, "vp_blue": 3}}},

  {"name": "R16: 2 - 2 - 1 is clamped to 1", "rule": "R16", "players": 3, "rounds": 1, "default": "decline",
   "given": {"game": {"deck": ["Church", "Church", "Church"], "vp_green": 2}},
   "rules": [{"seat": 1, "options_include": "keep 1 sell 2"},
             {"seat": 1, "options_include": 0, "answer": 0},
             {"seat": 2, "options_include": 0, "answer": 0},
             {"seat": 3, "options_include": 0, "answer": 0},
             {"seat": 1, "options_include": "green down"},
             {"seat": 2, "options_include": "green down"}],
   "expect": {"game": {"vp_red": 3, "vp_green": 1, "vp_blue": 3}}},

  {"name": "R16: up 2 and down 1 on the same die nets +1", "rule": "R16", "players": 3, "rounds": 1, "default": "decline",
   "given": {"game": {"deck": ["Church", "Church", "Church"]}},
   "rules": [{"seat": 1, "options_include": "keep 1 sell 2"},
             {"seat": 1, "options_include": 0, "answer": 0},
             {"seat": 2, "options_include": 0, "answer": 0},
             {"seat": 3, "options_include": 0, "answer": 0},
             {"seat": 1, "options_include": "red up"},
             {"seat": 2, "options_include": "red down"}],
   "expect": {"game": {"vp_red": 4, "vp_green": 3, "vp_blue": 3}}},

  {"name": "R17: church_count, lot and gift are reset at the end of the round", "rule": "R17", "players": 3, "rounds": 1, "default": "decline",
   "given": {"game": {"deck": ["Church", "Church", "Church"]}},
   "rules": [{"seat": 1, "options_include": "keep 1 sell 2"},
             {"seat": 1, "options_include": 0, "answer": 0},
             {"seat": 2, "options_include": 0, "answer": 0},
             {"seat": 3, "options_include": 0, "answer": 0},
             {"seat": 1, "options_include": "blue up"},
             {"seat": 2, "options_include": "blue up"}],
   "expect": {"players": {"1": {"church_count": 0}, "2": {"church_count": 0}, "3": {"church_count": 0}},
              "game": {"lot": "", "gift": "", "vp_blue": 5}}},

  {"name": "R18: after round 12 the game ends and is scored", "rule": "R18", "players": 3, "default": "decline",
   "given": {"game": {"round": 11, "deck": ["Red 1", "Red 1", "Red 1"]},
             "players": {"1": {"hand": ["Red 4", "Red 3"], "gold": 5}, "2": {"hand": ["Green 4"]}, "3": {"hand": []}}},
   "rules": [{"seat": 3, "options_include": "keep 1 sell 2"},
             {"seat": 1, "options_include": 0, "answer": 0},
             {"seat": 2, "options_include": 0, "answer": 0},
             {"seat": 3, "options_include": 0, "answer": 0}],
   "expect": {"winner": 1,
              "standings": {"1": 305, "2": 304, "3": 4},
              "players": {"1": {"vp": 3}, "2": {"vp": 3}, "3": {"vp": 0}},
              "game": {"round": 12}}},

  {"name": "R19: a tied colour scores for nobody; a strictly highest colour scores its die", "rule": "R19", "players": 3, "default": "decline",
   "given": {"game": {"round": 11, "deck": ["Gold 1", "Gold 1", "Gold 1"], "vp_blue": 5},
             "players": {"1": {"hand": ["Red 4"]}, "2": {"hand": ["Red 3", "Red 1"]}, "3": {"hand": ["Blue 2"]}}},
   "rules": [{"seat": 3, "options_include": "keep 1 sell 2"},
             {"seat": 1, "options_include": 0, "answer": 0},
             {"seat": 2, "options_include": 0, "answer": 0},
             {"seat": 3, "options_include": 0, "answer": 0}],
   "expect": {"winner": 3,
              "standings": {"1": 5, "2": 4, "3": 506},
              "players": {"1": {"vp": 0}, "2": {"vp": 0}, "3": {"vp": 5}}}},

  {"name": "R20: a VP tie is broken by gold", "rule": "R20", "players": 3, "default": "decline",
   "given": {"game": {"round": 11, "deck": ["Gold 1", "Gold 1", "Gold 1"]},
             "players": {"1": {"hand": ["Red 4"]}, "2": {"hand": ["Green 4"]}, "3": {"hand": []}}},
   "rules": [{"seat": 3, "options_include": "keep 1 sell 2"},
             {"seat": 1, "options_include": 0, "answer": 0},
             {"seat": 2, "options_include": 0, "answer": 0},
             {"seat": 3, "options_include": 0, "answer": 0}],
   "expect": {"winner": 1,
              "standings": {"1": 305, "2": 304, "3": 6},
              "players": {"1": {"vp": 3}, "2": {"vp": 3}, "3": {"vp": 0}}}},

  {"name": "R20: equal VP and equal gold share the win", "rule": "R20", "players": 3, "default": "decline",
   "given": {"game": {"round": 11, "deck": ["Church", "Church", "Church"]},
             "players": {"1": {"hand": ["Red 4"]}, "2": {"hand": ["Green 4"]}, "3": {"hand": []}}},
   "rules": [{"seat": 3, "options_include": "keep 1 sell 2"},
             {"seat": 1, "options_include": 0, "answer": 0},
             {"seat": 2, "options_include": 0, "answer": 0},
             {"seat": 3, "options_include": 0, "answer": 0},
             {"seat": 3, "options_include": "blue up"},
             {"seat": 1, "options_include": "blue up"}],
   "expect": {"winner": [1, 2],
              "standings": {"1": 304, "2": 304, "3": 4},
              "players": {"1": {"vp": 3}, "2": {"vp": 3}, "3": {"vp": 0}},
              "game": {"vp_blue": 5}}}
]

Why it was refused: scenario 1: needs `rules` (what each seat answers, by option name); scenario 2: needs `rules` (what each seat answers, by option name); scenario 3: needs `rules` (what each seat answers, by option name); scenario 4: needs `rules` (what each seat answers, by option name); scenario 5: needs `rules` (what each seat answers, by option name); scenario 6: needs `rules` (what each seat answers, by option name); scenario 7: needs `rules` (what each seat answers, by option name); scenario 9: needs `rules` (what each seat answers, by option name)
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
[
  {"name": "R1: the deck holds 36 cards right after setup", "rule": "R1", "players": 3, "rounds": 0,
   "rules": [{"seat": 1, "options_include": "keep 1 sell 2"}],
   "expect": {"lens": {"game": {"deck": 36}, "players": {"1": {"hand": 0}, "2": {"hand": 0}, "3": {"hand": 0}}}}},

  {"name": "R2: setup gives each player 4 gold, an empty hand, church_count 0, and every die is at 3", "rule": "R2", "players": 3, "rounds": 0,
   "rules": [{"seat": 1, "options_include": "keep 1 sell 2"}],
   "expect": {"standings": {"1": 4, "2": 4, "3": 4},
              "players": {"1": {"church_count": 0, "vp": 0}, "2": {"church_count": 0, "vp": 0}, "3": {"church_count": 0, "vp": 0}},
              "game": {"vp_red": 3, "vp_green": 3, "vp_blue": 3},
              "lens": {"players": {"1": {"hand": 0}, "2": {"hand": 0}, "3": {"hand": 0}}}}},

  {"name": "R3: round 4 makes P1 active", "rule": "R3", "players": 3, "rounds": 1, "default": "decline",
   "given": {"game": {"round": 3}},
   "rules": [{"seat": 1, "options_include": "keep 1 sell 2"}],
   "expect": {"game": {"round": 4, "active_seat": 1}}},

  {"name": "R3: round 5 makes P2 active", "rule": "R3", "players": 3, "rounds": 1, "default": "decline",
   "given": {"game": {"round": 4}},
   "rules": [{"seat": 2, "options_include": "keep 1 sell 2"}],
   "expect": {"game": {"round": 5, "active_seat": 2}}},

  {"name": "R3: round 6 makes P3 active", "rule": "R3", "players": 3, "rounds": 1, "default": "decline",
   "given": {"game": {"round": 5}},
   "rules": [{"seat": 3, "options_include": "keep 1 sell 2"}],
   "expect": {"game": {"round": 6, "active_seat": 3}}},

  {"name": "R4: the deck holds 33 cards after round 1 (chance cannot change this count)", "rule": "R4", "players": 3, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "keep 1 sell 2"}],
   "expect": {"lens": {"game": {"deck": 33}}, "game": {"round": 1}}},

  {"name": "R4: the deck holds 30 cards after round 2 (chance cannot change this count)", "rule": "R4", "players": 3, "rounds": 2, "default": "decline",
   "rules": [{"seat": 1, "options_include": "keep 1 sell 2"},
             {"seat": 2, "options_include": "keep 1 sell 2"}],
   "expect": {"lens": {"game": {"deck": 30}}, "game": {"round": 2}}},

  {"name": "R5: the keep, lot and gift cards each go to a different seat", "rule": "R5", "players": 3, "rounds": 1, "default": "decline",
   "given": {"game": {"deck": ["Red 1", "Red 1", "Red 1"]}},
   "rules": [{"seat": 1, "options_include": "keep 1 sell 2"},
             {"seat": 2, "options_include": 2, "answer": 2},
             {"seat": 1, "options_include": 0, "answer": 0},
             {"seat": 3, "options_include": 0, "answer": 0}],
   "expect": {"lens": {"game": {"deck": 0}, "players": {"1": {"hand": 1}, "2": {"hand": 1}, "3": {"hand": 1}}},
              "standings": {"1": 4, "2": 2, "3": 4}}},

  {"name": "R6: a round with talk plays through normally", "rule": "R6", "players": 3, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "keep 1 sell 2"}],
   "expect": {"game": {"round": 1, "active_seat": 1}, "lens": {"game": {"deck": 33}}}},

  {"name": "R7: a bid of 22 with 4 gold counts as 4 and costs 4", "rule": "R7", "players": 3, "rounds": 1, "default": "decline",
   "given": {"game": {"deck": ["Red 1", "Red 1", "Red 1"]}},
   "rules": [{"seat": 1, "options_include": "keep 1 sell 2"},
             {"seat": 1, "options_include": 0, "answer": 0},
             {"seat": 2, "options_include": 22, "answer": 22},
             {"seat": 3, "options_include": 3, "answer": 3}],
   "expect": {"standings": {"1": 4, "2": 0, "3": 4},
              "lens": {"players": {"1": {"hand": 1}, "2": {"hand": 1}, "3": {"hand": 1}}}}},

  {"name": "R8: the highest bid wins the lot and the winner pays it", "rule": "R8", "players": 3, "rounds": 1, "default": "decline",
   "given": {"game": {"deck": ["Red 1", "Red 1", "Red 1"]}},
   "rules": [{"seat": 1, "options_include": "keep 2 sell 3"},
             {"seat": 1, "options_include": 0, "answer": 0},
             {"seat": 2, "options_include": 2, "answer": 2},
             {"seat": 3, "options_include": 3, "answer": 3}],
   "expect": {"standings": {"1": 4, "2": 4, "3": 1},
              "lens": {"players": {"1": {"hand": 1}, "2": {"hand": 1}, "3": {"hand": 1}}}}},

  {"name": "R9: a tie between non-active seats goes to the first seat clockwise after the active seat (P2 active, P3 beats P1)", "rule": "R9", "players": 3, "rounds": 1, "default": "decline",
   "given": {"game": {"round": 1, "deck": ["Red 1", "Red 1", "Red 1"]}},
   "rules": [{"seat": 2, "options_include": "keep 1 sell 2"},
             {"seat": 2, "options_include": 0, "answer": 0},
             {"seat": 1, "options_include": 3, "answer": 3},
             {"seat": 3, "options_include": 3, "answer": 3}],
   "expect": {"game": {"active_seat": 2},
              "standings": {"1": 4, "2": 4, "3": 1},
              "lens": {"players": {"1": {"hand": 1}, "2": {"hand": 1}, "3": {"hand": 1}}}}},

  {"name": "R9: a tie that includes the active seat goes to the active seat", "rule": "R9", "players": 3, "rounds": 1, "default": "decline",
   "given": {"game": {"deck": ["Red 1", "Red 1", "Red 1"]}},
   "rules": [{"seat": 1, "options_include": "keep 1 sell 2"},
             {"seat": 1, "options_include": 2, "answer": 2},
             {"seat": 2, "options_include": 1, "answer": 1},
             {"seat": 3, "options_include": 2, "answer": 2}],
   "expect": {"standings": {"1": 2, "2": 4, "3": 4},
              "lens": {"players": {"1": {"hand": 2}, "2": {"hand": 1}, "3": {"hand": 0}}}}},

  {"name": "R10: when all three bid 0, the active seat wins the lot and pays nothing", "rule": "R10", "players": 3, "rounds": 1, "default": "decline",
   "given": {"game": {"deck": ["Red 1", "Red 1", "Red 1"]}},
   "rules": [{"seat": 1, "options_include": "keep 1 sell 2"},
             {"seat": 1, "options_include": 0, "answer": 0},
             {"seat": 2, "options_include": 0, "answer": 0},
             {"seat": 3, "options_include": 0, "answer": 0}],
   "expect": {"standings": {"1": 4, "2": 4, "3": 4},
              "lens": {"players": {"1": {"hand": 2}, "2": {"hand": 1}, "3": {"hand": 0}}}}},

  {"name": "R11: when a non-active seat wins the lot, the other non-active seat gets the gift (P3 active, P1 wins)", "rule": "R11", "players": 3, "rounds": 1, "default": "decline",
   "given": {"game": {"round": 2, "deck": ["Red 1", "Red 1", "Red 1"]}},
   "rules": [{"seat": 3, "options_include": "keep 3 sell 1"},
             {"seat": 1, "options_include": 1, "answer": 1},
             {"seat": 2, "options_include": 0, "answer": 0},
             {"seat": 3, "options_include": 0, "answer": 0}],
   "expect": {"game": {"active_seat": 3},
              "standings": {"1": 3, "2": 4, "3": 4},
              "lens": {"players": {"1": {"hand": 1}, "2": {"hand": 1}, "3": {"hand": 1}}}}},

  {"name": "R12: when the active seat wins the lot, the gift goes to the non-active seat with the lower bid", "rule": "R12", "players": 3, "rounds": 1, "default": "decline",
   "given": {"game": {"deck": ["Red 1", "Red 1", "Red 1"]}},
   "rules": [{"seat": 1, "options_include": "keep 1 sell 2"},
             {"seat": 1, "options_include": 3, "answer": 3},
             {"seat": 2, "options_include": 2, "answer": 2},
             {"seat": 3, "options_include": 1, "answer": 1}],
   "expect": {"standings": {"1": 1, "2": 4, "3": 4},
              "lens": {"players": {"1": {"hand": 2}, "2": {"hand": 0}, "3": {"hand": 1}}}}},

  {"name": "R13: Gold cards leave the hand and add their value to gold", "rule": "R13", "players": 3, "rounds": 1, "default": "decline",
   "given": {"game": {"deck": ["Gold 2", "Gold 2", "Gold 2"]}},
   "rules": [{"seat": 1, "options_include": "keep 1 sell 2"},
             {"seat": 1, "options_include": 0, "answer": 0},
             {"seat": 2, "options_include": 0, "answer": 0},
             {"seat": 3, "options_include": 0, "answer": 0}],
   "expect": {"standings": {"1": 8, "2": 6, "3": 4},
              "lens": {"players": {"1": {"hand": 0}, "2": {"hand": 0}, "3": {"hand": 0}}}}},

  {"name": "R14: two Church cards give a church_count of 2 (the die moves by 2) and Church cards leave the hand", "rule": "R14", "players": 3, "rounds": 1, "default": "decline",
   "given": {"game": {"deck": ["Church", "Church", "Church"]}},
   "rules": [{"seat": 1, "options_include": "keep 1 sell 2"},
             {"seat": 1, "options_include": 0, "answer": 0},
             {"seat": 2, "options_include": 0, "answer": 0},
             {"seat": 3, "options_include": 0, "answer": 0},
             {"seat": 1, "options_include": "green down"},
             {"seat": 2, "options_include": "blue up"}],
   "expect": {"game": {"vp_red": 3, "vp_green": 1, "vp_blue": 4},
              "lens": {"players": {"1": {"hand": 0}, "2": {"hand": 0}, "3": {"hand": 0}}}}},

  {"name": "R15: only seats with Church cards choose; a seat with church_count 0 is not asked", "rule": "R15", "players": 3, "rounds": 1, "default": "decline",
   "given": {"game": {"deck": ["Church", "Church", "Church"]}},
   "rules": [{"seat": 1, "options_include": "keep 1 sell 2"},
             {"seat": 1, "options_include": 0, "answer": 0},
             {"seat": 2, "options_include": 0, "answer": 0},
             {"seat": 3, "options_include": 0, "answer": 0},
             {"seat": 1, "options_include": "red up"},
             {"seat": 2, "options_include": "red up"}],
   "expect": {"offered": [{"seat": 1, "option": "red up"}, {"seat": 2, "option": "red up"}],
              "not_offered": [{"seat": 3, "option": "red up"}, {"seat": 3, "option": "blue down"}],
              "game": {"vp_red": 5, "vp_green": 3, "vp_blue": 3}}},

  {"name": "R16: 4 + 2 + 1 is clamped to 5", "rule": "R16", "players": 3, "rounds": 1, "default": "decline",
   "given": {"game": {"deck": ["Church", "Church", "Church"], "vp_red": 4}},
   "rules": [{"seat": 1, "options_include": "keep 1 sell 2"},
             {"seat": 1, "options_include": 0, "answer": 0},
             {"seat": 2, "options_include": 0, "answer": 0},
             {"seat": 3, "options_include": 0, "answer": 0},
             {"seat": 1, "options_include": "red up"},
             {"seat": 2, "options_include": "red up"}],
   "expect": {"game": {"vp_red": 5, "vp_green": 3, "vp_blue": 3}}},

  {"name": "R16: 2 - 2 - 1 is clamped to 1", "rule": "R16", "players": 3, "rounds": 1, "default": "decline",
   "given": {"game": {"deck": ["Church", "Church", "Church"], "vp_green": 2}},
   "rules": [{"seat": 1, "options_include": "keep 1 sell 2"},
             {"seat": 1, "options_include": 0, "answer": 0},
             {"seat": 2, "options_include": 0, "answer": 0},
             {"seat": 3, "options_include": 0, "answer": 0},
             {"seat": 1, "options_include": "green down"},
             {"seat": 2, "options_include": "green down"}],
   "expect": {"game": {"vp_red": 3, "vp_green": 1, "vp_blue": 3}}},

  {"name": "R16: up 2 and down 1 on the same die nets +1", "rule": "R16", "players": 3, "rounds": 1, "default": "decline",
   "given": {"game": {"deck": ["Church", "Church", "Church"]}},
   "rules": [{"seat": 1, "options_include": "keep 1 sell 2"},
             {"seat": 1, "options_include": 0, "answer": 0},
             {"seat": 2, "options_include": 0, "answer": 0},
             {"seat": 3, "options_include": 0, "answer": 0},
             {"seat": 1, "options_include": "red up"},
             {"seat": 2, "options_include": "red down"}],
   "expect": {"game": {"vp_red": 4, "vp_green": 3, "vp_blue": 3}}},

  {"name": "R17: church_count, lot and gift are reset at the end of the round", "rule": "R17", "players": 3, "rounds": 1, "default": "decline",
   "given": {"game": {"deck": ["Church", "Church", "Church"]}},
   "rules": [{"seat": 1, "options_include": "keep 1 sell 2"},
             {"seat": 1, "options_include": 0, "answer": 0},
             {"seat": 2, "options_include": 0, "answer": 0},
             {"seat": 3, "options_include": 0, "answer": 0},
             {"seat": 1, "options_include": "blue up"},
             {"seat": 2, "options_include": "blue up"}],
   "expect": {"players": {"1": {"church_count": 0}, "2": {"church_count": 0}, "3": {"church_count": 0}},
              "game": {"lot": "", "gift": "", "vp_blue": 5}}},

  {"name": "R18: after round 12 the game ends and is scored", "rule": "R18", "players": 3, "default": "decline",
   "given": {"game": {"round": 11, "deck": ["Red 1", "Red 1", "Red 1"]},
             "players": {"1": {"hand": ["Red 4", "Red 3"], "gold": 5}, "2": {"hand": ["Green 4"]}, "3": {"hand": []}}},
   "rules": [{"seat": 3, "options_include": "keep 1 sell 2"},
             {"seat": 1, "options_include": 0, "answer": 0},
             {"seat": 2, "options_include": 0, "answer": 0},
             {"seat": 3, "options_include": 0, "answer": 0}],
   "expect": {"winner": 1,
              "standings": {"1": 305, "2": 304, "3": 4},
              "players": {"1": {"vp": 3}, "2": {"vp": 3}, "3": {"vp": 0}},
              "game": {"round": 12}}},

  {"name": "R19: a tied colour scores for nobody; a strictly highest colour scores its die", "rule": "R19", "players": 3, "default": "decline",
   "given": {"game": {"round": 11, "deck": ["Gold 1", "Gold 1", "Gold 1"], "vp_blue": 5},
             "players": {"1": {"hand": ["Red 4"]}, "2": {"hand": ["Red 3", "Red 1"]}, "3": {"hand": ["Blue 2"]}}},
   "rules": [{"seat": 3, "options_include": "keep 1 sell 2"},
             {"seat": 1, "options_include": 0, "answer": 0},
             {"seat": 2, "options_include": 0, "answer": 0},
             {"seat": 3, "options_include": 0, "answer": 0}],
   "expect": {"winner": 3,
              "standings": {"1": 5, "2": 4, "3": 506},
              "players": {"1": {"vp": 0}, "2": {"vp": 0}, "3": {"vp": 5}}}},

  {"name": "R20: a VP tie is broken by gold", "rule": "R20", "players": 3, "default": "decline",
   "given": {"game": {"round": 11, "deck": ["Gold 1", "Gold 1", "Gold 1"]},
             "players": {"1": {"hand": ["Red 4"]}, "2": {"hand": ["Green 4"]}, "3": {"hand": []}}},
   "rules": [{"seat": 3, "options_include": "keep 1 sell 2"},
             {"seat": 1, "options_include": 0, "answer": 0},
             {"seat": 2, "options_include": 0, "answer": 0},
             {"seat": 3, "options_include": 0, "answer": 0}],
   "expect": {"winner": 1,
              "standings": {"1": 305, "2": 304, "3": 6},
              "players": {"1": {"vp": 3}, "2": {"vp": 3}, "3": {"vp": 0}}}},

  {"name": "R20: equal VP and equal gold share the win", "rule": "R20", "players": 3, "default": "decline",
   "given": {"game": {"round": 11, "deck": ["Church", "Church", "Church"]},
             "players": {"1": {"hand": ["Red 4"]}, "2": {"hand": ["Green 4"]}, "3": {"hand": []}}},
   "rules": [{"seat": 3, "options_include": "keep 1 sell 2"},
             {"seat": 1, "options_include": 0, "answer": 0},
             {"seat": 2, "options_include": 0, "answer": 0},
             {"seat": 3, "options_include": 0, "answer": 0},
             {"seat": 3, "options_include": "blue up"},
             {"seat": 1, "options_include": "blue up"}],
   "expect": {"winner": [1, 2],
              "standings": {"1": 304, "2": 304, "3": 4},
              "players": {"1": {"vp": 3}, "2": {"vp": 3}, "3": {"vp": 0}},
              "game": {"vp_blue": 5}}}
]
````
