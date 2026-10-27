# 23 scenarios

- time: 2026-10-27T09:04:29+00:00 (35.1s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 6f653732b8656b9e, reply sha256 caabba78ed7011c3

## Sent

````
SPEC:
{
  "name": "Kobayakawa Duel Rounds with Table Talk",
  "summary": "Over 10 rounds, players hold one secret card, may swap it blind, talk, then fight for a pot. The lowest fighter's card adds the face-up Kobayakawa value, and the highest total takes the pot plus 1 kamon from the centre.",
  "players": {
    "min": 3,
    "max": 5,
    "suggested": 4
  },
  "parameters": {
    "starting_kamons": 5,
    "centre_starting_kamons": 10,
    "rounds": 10,
    "deck_size": 15,
    "card_min": 1,
    "card_max": 15,
    "fight_stake": 1,
    "centre_bonus": 1,
    "hand_cards_per_player": 1,
    "reserve_cards_per_player": 1,
    "minimum_fighters_for_showdown": 2
  },
  "attributes": {
    "player": [
      {
        "key": "kamons",
        "type": "number",
        "visible": "public",
        "initial": 5,
        "meaning": "the player's kamons; this is the score",
        "observable": true
      },
      {
        "key": "hand",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "the player's current face-down hand card (1-15), seen only by its owner",
        "observable": false
      },
      {
        "key": "draw_choice",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "KEEP or SWAP this round",
        "observable": false
      },
      {
        "key": "discarded",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "the card discarded face up by a SWAP this round (0 if the player kept)",
        "observable": true
      },
      {
        "key": "message",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "this round's public table-talk message",
        "observable": false
      },
      {
        "key": "fight_choice",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "FIGHT or PASS this round",
        "observable": false
      },
      {
        "key": "fought",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "whether the player fights this round",
        "observable": false
      },
      {
        "key": "revealed_card",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "the card revealed in a showdown of 2 or more fighters (0 if not revealed)",
        "observable": true
      },
      {
        "key": "total",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "the fight total in a showdown: the card, plus K for the lowest card (0 if not in a showdown)",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "the current round number",
        "observable": true
      },
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "this round's fresh shuffled deck of cards 1-15",
        "observable": false
      },
      {
        "key": "reserve_cards",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "each seat's face-down reserve card, in seat order; nobody sees it",
        "observable": false
      },
      {
        "key": "kobayakawa",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "K, the face-up Kobayakawa card this round",
        "observable": true
      },
      {
        "key": "centre",
        "type": "number",
        "visible": "public",
        "initial": 10,
        "meaning": "kamons left in the centre",
        "observable": true
      },
      {
        "key": "pot",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "kamons staked this round",
        "observable": false
      },
      {
        "key": "fighter_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "the number of FIGHT players this round",
        "observable": false
      },
      {
        "key": "lowest_card",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "the lowest card among the fighters in a showdown",
        "observable": false
      },
      {
        "key": "winner_seat",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "the seat that won this round's showdown (0 if there was none)",
        "observable": true
      }
    ]
  },
  "setup": [
    "Every player's kamons is set to 5.",
    "The centre is set to 10 kamons.",
    "The round is set to 0."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round += 1; deck = [1..15] (a fresh deck); reserve_cards = []; pot = 0; fighter_count = 0; lowest_card = 0; winner_seat = 0; for every player: draw_choice = '', discarded = 0, message = '', fight_choice = '', fought = false, revealed_card = 0, total = 0"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "For each player: draw one random card from deck into hand and remove it from deck. Then, for each seat in order: draw one random card from deck, append it to reserve_cards and remove it from deck. Then draw one random card from deck into kobayakawa and remove it from deck. Announce: 'Round {round}: the Kobayakawa card K is {kobayakawa}.'"
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player sees their own hand, every player's kamons, the centre and kobayakawa."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "choice: KEEP | SWAP",
      "effect": "draw_choice = the answer"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "For each player with draw_choice == 'SWAP': discarded = hand; hand = reserve_cards[seat-1]. Announce each discard: 'Seat {seat} swapped and discarded {discarded}.'"
    },
    {
      "action": "sync",
      "who": "each player with draw_choice SWAP",
      "answer": null,
      "effect": "Each swapping player sees their new hand."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "short text",
      "effect": "message = the answer; broadcast {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"} once all messages are in"
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "choice: FIGHT | PASS (only PASS when kamons == 0)",
      "effect": "fight_choice = the answer; fought = (fight_choice == 'FIGHT')"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "For each player with fought: kamons -= 1; pot += 1. fighter_count = the number of players with fought."
    },
    {
      "action": "update",
      "who": "the single fighter",
      "answer": null,
      "effect": "when fighter_count == 1: that player's kamons += pot; pot = 0. The card is not revealed and the centre is unchanged."
    },
    {
      "action": "update",
      "who": "all fighters",
      "answer": null,
      "effect": "when fighter_count >= 2: lowest_card = min(hand) over players with fought; for each player with fought: revealed_card = hand; total = hand + (hand == lowest_card ? kobayakawa : 0)"
    },
    {
      "action": "update",
      "who": "the showdown winner",
      "answer": null,
      "effect": "when fighter_count >= 2: winner_seat = the fighter with the largest (total * 100 - hand), so the highest total wins and a tie goes to the lower card; that player's kamons += pot + min(1, centre); centre -= min(1, centre); pot = 0"
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce the fighters, each revealed_card and total, winner_seat, and every player's kamons and the centre."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if round >= 10; otherwise continue."
    }
  ],
  "ending": {
    "condition": "round >= 10",
    "rank_by": "you.kamons",
    "decided_by": "After round 10, each player's standing is their kamons. The most kamons wins, and players tied for most share the result (the source calls this a draw)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game starts, then each player has 5 kamons, the centre has 10 kamons and the round is 0."
    },
    {
      "id": "R2",
      "text": "When a round starts, then the deck is a fresh set of the 15 cards 1 to 15, and each player gets 1 hand card and 1 reserve card from it, all distinct."
    },
    {
      "id": "R3",
      "text": "When the deal is done, then one more card from the deck is set as kobayakawa (K) and announced publicly."
    },
    {
      "id": "R4",
      "text": "When a player's hand is dealt, then only that player can see it, and no player can see any reserve card."
    },
    {
      "id": "R5",
      "text": "When a player chooses SWAP, then discarded becomes their old hand card (publicly announced with their seat) and hand becomes their reserve card."
    },
    {
      "id": "R6",
      "text": "When a player chooses KEEP, then hand is unchanged, discarded stays 0 and their reserve card is not used."
    },
    {
      "id": "R7",
      "text": "When the KEEP/SWAP choice is asked, then all players answer at once, without seeing the others' choices."
    },
    {
      "id": "R8",
      "text": "When the talk step runs, then every player submits one short message at once, and all messages are shown to everyone only after all are in."
    },
    {
      "id": "R9",
      "text": "When a player has 0 kamons at the fight choice, then their only option is PASS."
    },
    {
      "id": "R10",
      "text": "When a player chooses FIGHT, then their kamons drop by 1 and the pot rises by 1."
    },
    {
      "id": "R11",
      "text": "When no player fights, then no kamons change that round."
    },
    {
      "id": "R12",
      "text": "When exactly one player fights, then that player gets their 1 kamon back, their card is not revealed and the centre is unchanged."
    },
    {
      "id": "R13",
      "text": "When two or more players fight, then each fighter's revealed_card equals their hand and their total equals their hand, plus K for the fighter with the lowest card."
    },
    {
      "id": "R14",
      "text": "When two or more players fight, then the fighter with the highest total wins, and if totals tie the tied fighter with the lower card wins (e.g. K=5: cards 3 and 8 give totals 8 and 8, so card 3 wins)."
    },
    {
      "id": "R15",
      "text": "When a showdown winner is decided and the centre has at least 1 kamon, then the winner gains the whole pot plus 1 kamon and the centre loses 1."
    },
    {
      "id": "R16",
      "text": "When a showdown winner is decided and the centre has 0 kamons, then the winner gains only the pot."
    },
    {
      "id": "R17",
      "text": "When a showdown is decided, then each losing fighter loses the 1 kamon they staked."
    },
    {
      "id": "R18",
      "text": "When round 10 ends, then the game ends and the player with the most kamons wins, with players tied for most sharing the result."
    }
  ],
  "offers": [
    {
      "question": "Draw choice",
      "who": "every seat",
      "options": "KEEP, SWAP"
    },
    {
      "question": "Talk message",
      "who": "every seat",
      "options": "any short text"
    },
    {
      "question": "Fight choice",
      "who": "every seat",
      "options": "a seat with kamons >= 1: FIGHT, PASS; a seat with kamons == 0: PASS only"
    }
  ],
  "choices": [
    {
      "what": "3 to 5 players, suggested 4",
      "why": "The designer suggests 4, so it is kept. Below 3 a showdown is just a duel with no one to bluff off the table. Above 5 the 15-card deck cannot cover a hand and a reserve for every player plus K (6 players would need 13 of the 15 cards, leaving swaps and discards nearly fully informative), and one player's choice matters less."
    },
    {
      "what": "Table talk kept as a simultaneous poll broadcast to all",
      "why": "The source requires simultaneous messages. Talk earns its place because interests conflict: a player can claim a high card to scare others into passing, or a low card to bait fighters when K is large."
    },
    {
      "what": "Reserve cards stored as a hidden table list in seat order",
      "why": "Nobody may see a reserve card, and a player attribute cannot be hidden from its owner, so the reserves live on the table with visibility none."
    },
    {
      "what": "The tie-break is coded as the largest (total * 100 - card)",
      "why": "Totals are at most 30, so this ranks by total first and by the lower card second. Cards are distinct, so the result is unique."
    },
    {
      "what": "Strategy at the table",
      "why": "A thoughtful player weighs K against their card (a low card plus a big K can win), reads public discards and messages, bluffs about strength, and saves kamons near 0, because staying out also keeps them alive."
    }
  ],
  "simplifications": [
    {
      "what": "A tie for most kamons at the end is a shared win rather than a declared draw",
      "why": "The engine ranks by one expression and players level at the top share the win, which is how it expresses the source's draw."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: kamons, discarded, revealed_card, total; table: round, kobayakawa, centre, winner_seat.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
```json
[
  {"name": "Setup: 5 kamons each, centre 10, round 0", "rule": "R1", "players": 4, "seed": 1, "rounds": 0, "default": "decline",
   "expect": {"players": {"1": {"kamons": 5}, "2": {"kamons": 5}, "3": {"kamons": 5}, "4": {"kamons": 5}},
              "game": {"centre": 10, "round": 0}}},

  {"name": "Round start: fresh 15-card deck, 1 hand and 1 reserve each (deck size only, cards are random)", "rule": "R2", "players": 3, "seed": 2, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "KEEP", "times": "all"}, {"seat": 2, "options_include": "KEEP", "times": "all"}, {"seat": 3, "options_include": "KEEP", "times": "all"},
             {"seat": 1, "options_include": "PASS", "times": "all"}, {"seat": 2, "options_include": "PASS", "times": "all"}, {"seat": 3, "options_include": "PASS", "times": "all"}],
   "expect": {"game": {"round": 1}, "lens": {"game": {"deck": 8, "reserve_cards": 3}}}},

  {"name": "Kobayakawa takes one more card from the deck (4 players: 15-8-1=6 left; K value is random)", "rule": "R3", "players": 4, "seed": 3, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "PASS", "times": "all"}, {"seat": 2, "options_include": "PASS", "times": "all"}, {"seat": 3, "options_include": "PASS", "times": "all"}, {"seat": 4, "options_include": "PASS", "times": "all"}],
   "expect": {"game": {"round": 1}, "lens": {"game": {"deck": 6, "reserve_cards": 4}}}},

  {"name": "Reserve cards are kept on the table, one per seat; keepers discard nothing", "rule": "R4", "players": 5, "seed": 4, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "KEEP", "times": "all"}, {"seat": 2, "options_include": "KEEP", "times": "all"}, {"seat": 3, "options_include": "KEEP", "times": "all"}, {"seat": 4, "options_include": "KEEP", "times": "all"}, {"seat": 5, "options_include": "KEEP", "times": "all"}],
   "expect": {"lens": {"game": {"reserve_cards": 5, "deck": 4}},
              "players": {"1": {"discarded": 0}, "2": {"discarded": 0}, "3": {"discarded": 0}, "4": {"discarded": 0}, "5": {"discarded": 0}}}},

  {"name": "SWAP is offered and does not draw from the deck; a keeper's discard stays 0 (swapped card value is random)", "rule": "R5", "players": 3, "seed": 5, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "SWAP", "times": "all"}, {"seat": 2, "options_include": "KEEP", "times": "all"}, {"seat": 3, "options_include": "KEEP", "times": "all"},
             {"seat": 1, "options_include": "PASS", "times": "all"}, {"seat": 2, "options_include": "PASS", "times": "all"}, {"seat": 3, "options_include": "PASS", "times": "all"}],
   "expect": {"offered": [{"seat": 1, "option": "SWAP"}],
              "lens": {"game": {"deck": 8}},
              "players": {"2": {"discarded": 0, "kamons": 5}, "3": {"discarded": 0, "kamons": 5}}}},

  {"name": "KEEP leaves discarded at 0", "rule": "R6", "players": 3, "seed": 6, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "KEEP", "times": "all"}, {"seat": 2, "options_include": "KEEP", "times": "all"}, {"seat": 3, "options_include": "KEEP", "times": "all"},
             {"seat": 1, "options_include": "PASS", "times": "all"}, {"seat": 2, "options_include": "PASS", "times": "all"}, {"seat": 3, "options_include": "PASS", "times": "all"}],
   "expect": {"players": {"1": {"discarded": 0}, "2": {"discarded": 0}, "3": {"discarded": 0}}}},

  {"name": "Every seat is asked KEEP/SWAP", "rule": "R7", "players": 4, "seed": 7, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "PASS", "times": "all"}, {"seat": 2, "options_include": "PASS", "times": "all"}, {"seat": 3, "options_include": "PASS", "times": "all"}, {"seat": 4, "options_include": "PASS", "times": "all"}],
   "expect": {"offered": [{"seat": 1, "option": "KEEP"}, {"seat": 2, "option": "KEEP"}, {"seat": 3, "option": "KEEP"}, {"seat": 4, "option": "KEEP"},
                          {"seat": 1, "option": "SWAP"}, {"seat": 2, "option": "SWAP"}, {"seat": 3, "option": "SWAP"}, {"seat": 4, "option": "SWAP"}]}},

  {"name": "Talk step runs for everyone and the round continues to the fight choice", "rule": "R8", "players": 3, "seed": 8, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "PASS", "times": "all"}, {"seat": 2, "options_include": "PASS", "times": "all"}, {"seat": 3, "options_include": "PASS", "times": "all"}],
   "expect": {"game": {"round": 1, "centre": 10},
              "offered": [{"seat": 1, "option": "PASS"}, {"seat": 2, "option": "PASS"}, {"seat": 3, "option": "PASS"}]}},

  {"name": "A seat with 0 kamons can only PASS", "rule": "R9", "players": 3, "seed": 9, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"kamons": 0}}},
   "rules": [{"seat": 2, "options_include": "PASS", "times": "all"}, {"seat": 3, "options_include": "PASS", "times": "all"}],
   "expect": {"not_offered": [{"seat": 1, "option": "FIGHT"}],
              "offered": [{"seat": 1, "option": "PASS"}, {"seat": 2, "option": "FIGHT"}],
              "players": {"1": {"kamons": 0}, "2": {"kamons": 5}, "3": {"kamons": 5}}}},

  {"name": "Two fighters stake 1 each: kamons stay conserved; passer unchanged, centre pays 1 (winner is random)", "rule": "R10", "players": 3, "seed": 10, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "FIGHT", "times": "all"}, {"seat": 2, "options_include": "FIGHT", "times": "all"}, {"seat": 3, "options_include": "PASS", "times": "all"}],
   "expect": {"players": {"3": {"kamons": 5, "revealed_card": 0, "total": 0}}, "game": {"centre": 9}}},

  {"name": "Nobody fights: no kamons change, no showdown", "rule": "R11", "players": 4, "seed": 11, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "PASS", "times": "all"}, {"seat": 2, "options_include": "PASS", "times": "all"}, {"seat": 3, "options_include": "PASS", "times": "all"}, {"seat": 4, "options_include": "PASS", "times": "all"}],
   "expect": {"players": {"1": {"kamons": 5, "revealed_card": 0, "total": 0}, "2": {"kamons": 5}, "3": {"kamons": 5}, "4": {"kamons": 5}},
              "game": {"centre": 10, "winner_seat": 0}}},

  {"name": "Single fighter gets the stake back, card not revealed, centre unchanged", "rule": "R12", "players": 3, "seed": 12, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "FIGHT", "times": "all"}, {"seat": 2, "options_include": "PASS", "times": "all"}, {"seat": 3, "options_include": "PASS", "times": "all"}],
   "expect": {"players": {"1": {"kamons": 5, "revealed_card": 0, "total": 0}, "2": {"kamons": 5}, "3": {"kamons": 5}},
              "game": {"centre": 10, "winner_seat": 0}}},

  {"name": "Showdown reveals only fighters; non-fighters keep revealed_card and total 0 (card values random)", "rule": "R13", "players": 4, "seed": 13, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "FIGHT", "times": "all"}, {"seat": 2, "options_include": "FIGHT", "times": "all"}, {"seat": 3, "options_include": "PASS", "times": "all"}, {"seat": 4, "options_include": "PASS", "times": "all"}],
   "expect": {"players": {"3": {"revealed_card": 0, "total": 0, "kamons": 5}, "4": {"revealed_card": 0, "total": 0, "kamons": 5}}}},

  {"name": "Three-way showdown has one winner: centre pays exactly 1, passer unchanged (winner random)", "rule": "R14", "players": 4, "seed": 14, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "FIGHT", "times": "all"}, {"seat": 2, "options_include": "FIGHT", "times": "all"}, {"seat": 3, "options_include": "FIGHT", "times": "all"}, {"seat": 4, "options_include": "PASS", "times": "all"}],
   "expect": {"players": {"4": {"kamons": 5, "revealed_card": 0}}, "game": {"centre": 9}}},

  {"name": "Showdown with centre at 3: centre loses 1", "rule": "R15", "players": 3, "seed": 15, "rounds": 1, "default": "decline",
   "given": {"game": {"centre": 3}},
   "rules": [{"seat": 1, "options_include": "FIGHT", "times": "all"}, {"seat": 2, "options_include": "FIGHT", "times": "all"}, {"seat": 3, "options_include": "PASS", "times": "all"}],
   "expect": {"game": {"centre": 2}, "players": {"3": {"kamons": 5}}}},

  {"name": "Showdown with centre at 0: centre stays 0", "rule": "R16", "players": 3, "seed": 16, "rounds": 1, "default": "decline",
   "given": {"game": {"centre": 0}},
   "rules": [{"seat": 1, "options_include": "FIGHT", "times": "all"}, {"seat": 2, "options_include": "FIGHT", "times": "all"}, {"seat": 3, "options_include": "PASS", "times": "all"}],
   "expect": {"game": {"centre": 0}, "players": {"3": {"kamons": 5}}}},

  {"name": "Showdown among all three seats: centre pays 1 to the winner (which seat loses is random)", "rule": "R17", "players": 3, "seed": 17, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "FIGHT", "times": "all"}, {"seat": 2, "options_include": "FIGHT", "times": "all"}, {"seat": 3, "options_include": "FIGHT", "times": "all"}],
   "expect": {"game": {"centre": 9}}},

  {"name": "After round 10 the most kamons wins (all pass in the last round)", "rule": "R18", "players": 3, "seed": 18, "default": "decline",
   "given": {"game": {"round": 9}, "players": {"1": {"kamons": 8}, "2": {"kamons": 5}, "3": {"kamons": 2}}},
   "rules": [{"seat": 1, "options_include": "PASS", "times": "all"}, {"seat": 2, "options_include": "PASS", "times": "all"}, {"seat": 3, "options_include": "PASS", "times": "all"}],
   "expect": {"winner": 1, "standings": {"1": 8, "2": 5, "3": 2}, "game": {"round": 10}}},

  {"name": "After round 10 seats tied for most share the win", "rule": "R18", "players": 3, "seed": 19, "default": "decline",
   "given": {"game": {"round": 9}, "players": {"1": {"kamons": 7}, "2": {"kamons": 7}, "3": {"kamons": 1}}},
   "rules": [{"seat": 1, "options_include": "PASS", "times": "all"}, {"seat": 2, "options_include": "PASS", "times": "all"}, {"seat": 3, "options_include": "PASS", "times": "all"}],
   "expect": {"winner": [1, 2], "standings": {"1": 7, "2": 7, "3": 1}}}
]
```

Why it was refused: scenario 1: needs `rules` (what each seat answers, by option name)
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
[
  {"name": "Setup: 5 kamons each, centre 10, round 0", "rule": "R1", "players": 4, "seed": 1, "rounds": 0, "default": "decline",
   "rules": [{"seat": 1, "options_include": "KEEP", "times": "all"}, {"seat": 2, "options_include": "KEEP", "times": "all"}, {"seat": 3, "options_include": "KEEP", "times": "all"}, {"seat": 4, "options_include": "KEEP", "times": "all"}],
   "expect": {"players": {"1": {"kamons": 5}, "2": {"kamons": 5}, "3": {"kamons": 5}, "4": {"kamons": 5}},
              "game": {"centre": 10, "round": 0}}},

  {"name": "Round start: fresh 15-card deck, 1 hand and 1 reserve each (deck size only, cards are random)", "rule": "R2", "players": 3, "seed": 2, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "KEEP", "times": "all"}, {"seat": 2, "options_include": "KEEP", "times": "all"}, {"seat": 3, "options_include": "KEEP", "times": "all"},
             {"seat": 1, "options_include": "PASS", "times": "all"}, {"seat": 2, "options_include": "PASS", "times": "all"}, {"seat": 3, "options_include": "PASS", "times": "all"}],
   "expect": {"game": {"round": 1}, "lens": {"game": {"deck": 8, "reserve_cards": 3}}}},

  {"name": "Kobayakawa takes one more card from the deck (4 players: 15-8-1=6 left; K value is random)", "rule": "R3", "players": 4, "seed": 3, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "PASS", "times": "all"}, {"seat": 2, "options_include": "PASS", "times": "all"}, {"seat": 3, "options_include": "PASS", "times": "all"}, {"seat": 4, "options_include": "PASS", "times": "all"}],
   "expect": {"game": {"round": 1}, "lens": {"game": {"deck": 6, "reserve_cards": 4}}}},

  {"name": "Reserve cards are kept on the table, one per seat; keepers discard nothing", "rule": "R4", "players": 5, "seed": 4, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "KEEP", "times": "all"}, {"seat": 2, "options_include": "KEEP", "times": "all"}, {"seat": 3, "options_include": "KEEP", "times": "all"}, {"seat": 4, "options_include": "KEEP", "times": "all"}, {"seat": 5, "options_include": "KEEP", "times": "all"}],
   "expect": {"lens": {"game": {"reserve_cards": 5, "deck": 4}},
              "players": {"1": {"discarded": 0}, "2": {"discarded": 0}, "3": {"discarded": 0}, "4": {"discarded": 0}, "5": {"discarded": 0}}}},

  {"name": "SWAP is offered and does not draw from the deck; a keeper's discard stays 0 (swapped card value is random)", "rule": "R5", "players": 3, "seed": 5, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "SWAP", "times": "all"}, {"seat": 2, "options_include": "KEEP", "times": "all"}, {"seat": 3, "options_include": "KEEP", "times": "all"},
             {"seat": 1, "options_include": "PASS", "times": "all"}, {"seat": 2, "options_include": "PASS", "times": "all"}, {"seat": 3, "options_include": "PASS", "times": "all"}],
   "expect": {"offered": [{"seat": 1, "option": "SWAP"}],
              "lens": {"game": {"deck": 8}},
              "players": {"2": {"discarded": 0, "kamons": 5}, "3": {"discarded": 0, "kamons": 5}}}},

  {"name": "KEEP leaves discarded at 0", "rule": "R6", "players": 3, "seed": 6, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "KEEP", "times": "all"}, {"seat": 2, "options_include": "KEEP", "times": "all"}, {"seat": 3, "options_include": "KEEP", "times": "all"},
             {"seat": 1, "options_include": "PASS", "times": "all"}, {"seat": 2, "options_include": "PASS", "times": "all"}, {"seat": 3, "options_include": "PASS", "times": "all"}],
   "expect": {"players": {"1": {"discarded": 0}, "2": {"discarded": 0}, "3": {"discarded": 0}}}},

  {"name": "Every seat is asked KEEP/SWAP", "rule": "R7", "players": 4, "seed": 7, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "PASS", "times": "all"}, {"seat": 2, "options_include": "PASS", "times": "all"}, {"seat": 3, "options_include": "PASS", "times": "all"}, {"seat": 4, "options_include": "PASS", "times": "all"}],
   "expect": {"offered": [{"seat": 1, "option": "KEEP"}, {"seat": 2, "option": "KEEP"}, {"seat": 3, "option": "KEEP"}, {"seat": 4, "option": "KEEP"},
                          {"seat": 1, "option": "SWAP"}, {"seat": 2, "option": "SWAP"}, {"seat": 3, "option": "SWAP"}, {"seat": 4, "option": "SWAP"}]}},

  {"name": "Talk step runs for everyone and the round continues to the fight choice", "rule": "R8", "players": 3, "seed": 8, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "PASS", "times": "all"}, {"seat": 2, "options_include": "PASS", "times": "all"}, {"seat": 3, "options_include": "PASS", "times": "all"}],
   "expect": {"game": {"round": 1, "centre": 10},
              "offered": [{"seat": 1, "option": "PASS"}, {"seat": 2, "option": "PASS"}, {"seat": 3, "option": "PASS"}]}},

  {"name": "A seat with 0 kamons can only PASS", "rule": "R9", "players": 3, "seed": 9, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"kamons": 0}}},
   "rules": [{"seat": 2, "options_include": "PASS", "times": "all"}, {"seat": 3, "options_include": "PASS", "times": "all"}],
   "expect": {"not_offered": [{"seat": 1, "option": "FIGHT"}],
              "offered": [{"seat": 1, "option": "PASS"}, {"seat": 2, "option": "FIGHT"}],
              "players": {"1": {"kamons": 0}, "2": {"kamons": 5}, "3": {"kamons": 5}}}},

  {"name": "Two fighters stake 1 each: kamons stay conserved; passer unchanged, centre pays 1 (winner is random)", "rule": "R10", "players": 3, "seed": 10, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "FIGHT", "times": "all"}, {"seat": 2, "options_include": "FIGHT", "times": "all"}, {"seat": 3, "options_include": "PASS", "times": "all"}],
   "expect": {"players": {"3": {"kamons": 5, "revealed_card": 0, "total": 0}}, "game": {"centre": 9}}},

  {"name": "Nobody fights: no kamons change, no showdown", "rule": "R11", "players": 4, "seed": 11, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "PASS", "times": "all"}, {"seat": 2, "options_include": "PASS", "times": "all"}, {"seat": 3, "options_include": "PASS", "times": "all"}, {"seat": 4, "options_include": "PASS", "times": "all"}],
   "expect": {"players": {"1": {"kamons": 5, "revealed_card": 0, "total": 0}, "2": {"kamons": 5}, "3": {"kamons": 5}, "4": {"kamons": 5}},
              "game": {"centre": 10, "winner_seat": 0}}},

  {"name": "Single fighter gets the stake back, card not revealed, centre unchanged", "rule": "R12", "players": 3, "seed": 12, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "FIGHT", "times": "all"}, {"seat": 2, "options_include": "PASS", "times": "all"}, {"seat": 3, "options_include": "PASS", "times": "all"}],
   "expect": {"players": {"1": {"kamons": 5, "revealed_card": 0, "total": 0}, "2": {"kamons": 5}, "3": {"kamons": 5}},
              "game": {"centre": 10, "winner_seat": 0}}},

  {"name": "Showdown reveals only fighters; non-fighters keep revealed_card and total 0 (card values random)", "rule": "R13", "players": 4, "seed": 13, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "FIGHT", "times": "all"}, {"seat": 2, "options_include": "FIGHT", "times": "all"}, {"seat": 3, "options_include": "PASS", "times": "all"}, {"seat": 4, "options_include": "PASS", "times": "all"}],
   "expect": {"players": {"3": {"revealed_card": 0, "total": 0, "kamons": 5}, "4": {"revealed_card": 0, "total": 0, "kamons": 5}}}},

  {"name": "Three-way showdown has one winner: centre pays exactly 1, passer unchanged (winner random)", "rule": "R14", "players": 4, "seed": 14, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "FIGHT", "times": "all"}, {"seat": 2, "options_include": "FIGHT", "times": "all"}, {"seat": 3, "options_include": "FIGHT", "times": "all"}, {"seat": 4, "options_include": "PASS", "times": "all"}],
   "expect": {"players": {"4": {"kamons": 5, "revealed_card": 0}}, "game": {"centre": 9}}},

  {"name": "Showdown with centre at 3: centre loses 1", "rule": "R15", "players": 3, "seed": 15, "rounds": 1, "default": "decline",
   "given": {"game": {"centre": 3}},
   "rules": [{"seat": 1, "options_include": "FIGHT", "times": "all"}, {"seat": 2, "options_include": "FIGHT", "times": "all"}, {"seat": 3, "options_include": "PASS", "times": "all"}],
   "expect": {"game": {"centre": 2}, "players": {"3": {"kamons": 5}}}},

  {"name": "Showdown with centre at 0: centre stays 0", "rule": "R16", "players": 3, "seed": 16, "rounds": 1, "default": "decline",
   "given": {"game": {"centre": 0}},
   "rules": [{"seat": 1, "options_include": "FIGHT", "times": "all"}, {"seat": 2, "options_include": "FIGHT", "times": "all"}, {"seat": 3, "options_include": "PASS", "times": "all"}],
   "expect": {"game": {"centre": 0}, "players": {"3": {"kamons": 5}}}},

  {"name": "Showdown among all three seats: centre pays 1 to the winner (which seat loses is random)", "rule": "R17", "players": 3, "seed": 17, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "FIGHT", "times": "all"}, {"seat": 2, "options_include": "FIGHT", "times": "all"}, {"seat": 3, "options_include": "FIGHT", "times": "all"}],
   "expect": {"game": {"centre": 9}}},

  {"name": "After round 10 the most kamons wins (all pass in the last round)", "rule": "R18", "players": 3, "seed": 18, "default": "decline",
   "given": {"game": {"round": 9}, "players": {"1": {"kamons": 8}, "2": {"kamons": 5}, "3": {"kamons": 2}}},
   "rules": [{"seat": 1, "options_include": "PASS", "times": "all"}, {"seat": 2, "options_include": "PASS", "times": "all"}, {"seat": 3, "options_include": "PASS", "times": "all"}],
   "expect": {"winner": 1, "standings": {"1": 8, "2": 5, "3": 2}, "game": {"round": 10}}},

  {"name": "After round 10 seats tied for most share the win", "rule": "R18", "players": 3, "seed": 19, "default": "decline",
   "given": {"game": {"round": 9}, "players": {"1": {"kamons": 7}, "2": {"kamons": 7}, "3": {"kamons": 1}}},
   "rules": [{"seat": 1, "options_include": "PASS", "times": "all"}, {"seat": 2, "options_include": "PASS", "times": "all"}, {"seat": 3, "options_include": "PASS", "times": "all"}],
   "expect": {"winner": [1, 2], "standings": {"1": 7, "2": 7, "3": 1}}}
]
```
````
