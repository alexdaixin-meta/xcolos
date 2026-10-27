# 07 scenarios

- time: 2026-10-27T08:42:31+00:00 (98.7s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 534c93241dbf8dd6, reply sha256 e71903dd61089cd5

## Sent

````
SPEC:
{
  "name": "Kobayakawa: Held Cards",
  "summary": "A bluffing and betting game over 10 rounds. Each player holds one secret card and may keep, swap or shift the bonus card, then decides in seat order whether to fight for the kamon pot. A passer may carry their card into later rounds.",
  "players": {
    "min": 3,
    "max": 5,
    "suggested": 4
  },
  "parameters": {
    "starting_kamons": 4,
    "centre_kamons": 11,
    "starting_pot": 0,
    "card_min": 1,
    "card_max": 15,
    "total_rounds": 10,
    "min_stake_rounds_1_to_9": 1,
    "min_stake_round_10": 2,
    "high_stake_extra": 1,
    "centre_feed_rounds_1_to_9": 1,
    "first_start_seat": 1
  },
  "attributes": {
    "player": [
      {
        "key": "kamons",
        "type": "number",
        "visible": "public",
        "initial": 4,
        "meaning": "the player's kamons; this is the score",
        "observable": true
      },
      {
        "key": "active",
        "type": "bool",
        "visible": "public",
        "initial": true,
        "meaning": "false once the player is eliminated at 0 kamons",
        "observable": true
      },
      {
        "key": "hand",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "the player's secret hand card, 1-15, or 0 for no card",
        "observable": false
      },
      {
        "key": "held_rounds",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "how many earlier rounds the current hand card has been kept through by passing; 0 means a fresh card",
        "observable": true
      },
      {
        "key": "reserve_seen",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "the reserve card's value, shown only to a player who chose DRAW, otherwise 0",
        "observable": false
      },
      {
        "key": "draw_choice",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "this round's KEEP, DRAW or SHIFT; gathered by a simultaneous poll and revealed at step 6",
        "observable": true
      },
      {
        "key": "keep_choice",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "OLD or NEW, set for drawers only",
        "observable": false
      },
      {
        "key": "fight_choice",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "this round's PASS, LOW or HIGH",
        "observable": true
      },
      {
        "key": "stake",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "kamons staked this round",
        "observable": false
      },
      {
        "key": "shown_card",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "the fighter's card once revealed in a showdown, otherwise 0",
        "observable": false
      },
      {
        "key": "total",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "the fighter's showdown total: the card, plus the Kobayakawa if it is the lowest fighter's card",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "the current round, 1-10",
        "observable": true
      },
      {
        "key": "pot",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "kamons in the pot",
        "observable": true
      },
      {
        "key": "centre",
        "type": "number",
        "visible": "public",
        "initial": 11,
        "meaning": "kamons left in the centre",
        "observable": true
      },
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "the shuffled cards 1-15, less the hand cards held by players, rebuilt each round",
        "observable": false
      },
      {
        "key": "reserves",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "the face-down reserve cards, one per active seat in seat order, unseen by all",
        "observable": false
      },
      {
        "key": "kobayakawa",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "the face-up Kobayakawa value",
        "observable": true
      },
      {
        "key": "alternate",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "the face-down Alternate card",
        "observable": false
      },
      {
        "key": "face_up_discards",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "cards discarded face up this round",
        "observable": false
      },
      {
        "key": "start_seat",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "the seat that acts first in the fight",
        "observable": true
      },
      {
        "key": "min_stake",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "the minimum stake: 1 in rounds 1-9, 2 in round 10",
        "observable": false
      },
      {
        "key": "high_fought",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "true once anyone has fought HIGH this round",
        "observable": false
      },
      {
        "key": "winner_seat",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "the seat that took the pot this round, or 0 for none",
        "observable": false
      }
    ]
  },
  "setup": [
    "Seat players 1 to N.",
    "Set each player's kamons to 4, active to true, hand to 0 and held_rounds to 0.",
    "Set centre to 11, pot to 0, round to 1 and start_seat to 1."
  ],
  "round": [
    {
      "action": "update",
      "who": "engine",
      "answer": null,
      "effect": "Set min_stake = 1 if round <= 9, else 2. Set high_fought = false and winner_seat = 0. Clear face_up_discards, and clear each player's draw_choice, keep_choice, fight_choice, stake, shown_card, total and reserve_seen. Set deck = the cards 1..15 minus every active player's hand (where hand > 0), then shuffle it."
    },
    {
      "action": "update",
      "who": "each active player with hand = 0",
      "answer": null,
      "effect": "Draw one card at random from deck into hand (visible only to the owner) and remove it from deck."
    },
    {
      "action": "update",
      "who": "each active player",
      "answer": null,
      "effect": "Draw one card at random from deck and append it to reserves at that seat's position; remove it from deck. Nobody sees it."
    },
    {
      "action": "update",
      "who": "engine",
      "answer": null,
      "effect": "Draw one card from deck into kobayakawa (public) and one into alternate (hidden), removing each from deck."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce round, kobayakawa, pot, every player's kamons, every player with held_rounds > 0 and their held_rounds, start_seat, and min_stake."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player is sent their own state, including their hand."
    },
    {
      "action": "poll",
      "who": "all active players",
      "answer": "one of KEEP, DRAW, SHIFT",
      "effect": "Store the answer in draw_choice. It is not shown until step 6."
    },
    {
      "action": "update",
      "who": "each active player with draw_choice = DRAW",
      "answer": null,
      "effect": "Set reserve_seen = that seat's card in reserves; only the owner sees it."
    },
    {
      "action": "poll",
      "who": "active players with draw_choice = DRAW",
      "answer": "one of OLD, NEW",
      "effect": "Store the answer in keep_choice. If NEW: append hand to face_up_discards, then set hand = reserve_seen. If OLD: append reserve_seen to face_up_discards. Then clear reserves; undrawn reserves are discarded face down, unseen. If a player chose NEW, set held_rounds = 0."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce every active player's draw_choice and the contents of face_up_discards."
    },
    {
      "action": "update",
      "who": "engine",
      "answer": null,
      "effect": "If the count of players with draw_choice = SHIFT is >= 1, set kobayakawa = alternate and announce the new kobayakawa."
    },
    {
      "action": "poll",
      "who": "all active players",
      "answer": "short text",
      "effect": "Broadcast every message to all as {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"}. Talk is not binding."
    },
    {
      "action": "ask",
      "who": "each active player in turn, in seat order starting at start_seat and wrapping around",
      "answer": "one of the options allowed for this seat: PASS; LOW if high_fought = false and kamons >= min_stake; HIGH if kamons >= min_stake + 1",
      "effect": "Store the answer in fight_choice. If LOW, set stake = min_stake. If HIGH, set stake = min_stake + 1 and high_fought = true. If PASS, set stake = 0."
    },
    {
      "action": "update",
      "who": "engine",
      "answer": null,
      "effect": "For each player: kamons -= stake and pot += stake. Then the centre feeds the pot: if round <= 9, move min(1, centre) from centre to pot; if round = 10, move all of centre to pot."
    },
    {
      "action": "update",
      "who": "engine",
      "answer": null,
      "effect": "Let F = the number of players with fight_choice in {LOW, HIGH}. If F = 1, set winner_seat = that fighter and move the whole pot to their kamons; their card is not revealed. If F >= 2: for each fighter set shown_card = hand and total = hand, and add kobayakawa to the total of the fighter with the lowest hand. If exactly one fighter has the highest total, move the whole pot to them and set winner_seat to their seat. If F = 0, the pot carries."
    },
    {
      "action": "update",
      "who": "engine",
      "answer": null,
      "effect": "If F >= 2 and two or more fighters share the highest total: if round <= 9, the pot carries. If round = 10, each tied fighter gains floor(pot / number tied), and pot is set to 0 (the remainder leaves the game)."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce every fight_choice, every shown_card and total, the pot result, and every player's kamons."
    },
    {
      "action": "update",
      "who": "engine",
      "answer": null,
      "effect": "Each fighter sets hand = 0 and held_rounds = 0. Each active passer keeps hand and adds 1 to held_rounds. For each active player with kamons = 0, set active = false and hand = 0 (their card is discarded unseen). Then set start_seat = winner_seat if winner_seat > 0; otherwise the next active seat after the old start_seat, wrapping. Then add 1 to round."
    },
    {
      "action": "check",
      "who": "engine",
      "answer": null,
      "effect": "End the game if round > 10 or the count of active players <= 1. Otherwise continue."
    }
  ],
  "ending": {
    "condition": "round > 10 or count(active players) <= 1",
    "rank_by": "you.kamons",
    "decided_by": "The player with the most kamons wins. Eliminated players have 0. If only one player remains active, that player has the most kamons and wins. Players tied for the most share the result, which stands for the source's draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "At setup, then each player has 4 kamons, the centre has 11, the pot is 0, the start seat is 1, and nobody holds a card."
    },
    {
      "id": "R2",
      "text": "When a round begins, then the deck is the cards 1-15 minus the hand cards held by active players."
    },
    {
      "id": "R3",
      "text": "When a round begins, then each active player with no hand card is dealt one hand card, seen only by them."
    },
    {
      "id": "R4",
      "text": "When a round begins, then each active player is dealt one face-down reserve card that nobody sees, then a face-up Kobayakawa and a face-down Alternate are dealt."
    },
    {
      "id": "R5",
      "text": "When the round is 1-9, then the minimum stake is 1; when the round is 10, then it is 2."
    },
    {
      "id": "R6",
      "text": "When the round is announced, then the announcement gives the round, the Kobayakawa, the pot, every player's kamons, the players holding a kept card with its held_rounds, the start seat and the minimum stake."
    },
    {
      "id": "R7",
      "text": "When the draw choice is made, then every active player chooses KEEP, DRAW or SHIFT at the same time, and no choice is seen until all are in."
    },
    {
      "id": "R8",
      "text": "When a player chose DRAW, then they alone see their reserve card."
    },
    {
      "id": "R9",
      "text": "When a drawer chooses NEW, then the reserve card becomes their hand and the old hand card is discarded face up; when they choose OLD, then the reserve card is discarded face up."
    },
    {
      "id": "R10",
      "text": "When drawers have chosen, then every undrawn reserve card is discarded face down and stays unseen."
    },
    {
      "id": "R11",
      "text": "When the draw choices are revealed, then every player's draw choice and every face-up discard is announced."
    },
    {
      "id": "R12",
      "text": "When at least 1 player chose SHIFT, then the Alternate replaces the Kobayakawa and the new value is announced; when no player chose SHIFT, then the Kobayakawa is unchanged."
    },
    {
      "id": "R13",
      "text": "When the talk step runs, then every active player writes one short message at the same time, and all messages are shown to everyone."
    },
    {
      "id": "R14",
      "text": "When the fight runs, then each active player acts once, in seat order starting at the start seat and wrapping around, and sees all earlier choices."
    },
    {
      "id": "R15",
      "text": "When nobody earlier this round has fought HIGH and the player has at least the minimum stake in kamons, then FIGHT LOW is offered at a stake equal to the minimum."
    },
    {
      "id": "R16",
      "text": "When the player has at least the minimum stake + 1 in kamons, then FIGHT HIGH is offered at a stake of the minimum + 1."
    },
    {
      "id": "R17",
      "text": "When any earlier player this round fought HIGH, then FIGHT LOW is not offered."
    },
    {
      "id": "R18",
      "text": "When a player has fewer kamons than every stake they are allowed, then only PASS is offered."
    },
    {
      "id": "R19",
      "text": "When the fight ends, then each fighter pays their stake into the pot."
    },
    {
      "id": "R20",
      "text": "When the fight ends in rounds 1-9, then 1 kamon moves from the centre to the pot if the centre has any."
    },
    {
      "id": "R21",
      "text": "When the fight ends in round 10, then all remaining centre kamons move to the pot."
    },
    {
      "id": "R22",
      "text": "When nobody fights, then the pot carries to the next round."
    },
    {
      "id": "R23",
      "text": "When exactly one player fights, then they take the whole pot and their card is not revealed."
    },
    {
      "id": "R24",
      "text": "When two or more players fight, then all fighters' cards are revealed, the fighter with the lowest card adds the Kobayakawa value to it, and the unique highest total takes the whole pot."
    },
    {
      "id": "R25",
      "text": "When fighters tie for the highest total in rounds 1-9, then nobody takes the pot and it carries."
    },
    {
      "id": "R26",
      "text": "When fighters tie for the highest total in round 10, then each tied fighter gets floor(pot / number tied), and the remainder leaves the game."
    },
    {
      "id": "R27",
      "text": "When a round is cleaned up, then each fighter's hand card is discarded and their held_rounds is set to 0, and each passer keeps their card and adds 1 to held_rounds."
    },
    {
      "id": "R28",
      "text": "When a player wins the pot, then they are the next start player; when nobody wins it, then the next start player is the next active seat after this round's start seat."
    },
    {
      "id": "R29",
      "text": "When a player has 0 kamons at the end of a round, then they are eliminated and their card is discarded unseen."
    },
    {
      "id": "R30",
      "text": "When round 10 ends, or when only 1 active player remains, then the game ends, and the most kamons wins."
    }
  ],
  "offers": [
    {
      "question": "Draw choice",
      "who": "every active seat",
      "options": "KEEP, DRAW, SHIFT"
    },
    {
      "question": "Keep choice",
      "who": "every active seat that chose DRAW",
      "options": "OLD, NEW"
    },
    {
      "question": "Talk",
      "who": "every active seat",
      "options": "a short free-text message"
    },
    {
      "question": "Fight",
      "who": "each active seat in turn from the start seat",
      "options": "no HIGH fought yet and kamons >= min+1: PASS, LOW, HIGH. No HIGH fought yet and kamons = min: PASS, LOW. HIGH already fought and kamons >= min+1: PASS, HIGH. Any other case: PASS only."
    }
  ],
  "choices": [
    {
      "what": "3 to 5 players, suggested 4",
      "why": "The designer chose 4. Three is the smallest table where fight order, reads and pot competition work. Five fits the 15-card deck: up to 5 hands, 5 reserves and 2 table cards is 12 cards, and more players would stretch the fight sequence."
    },
    {
      "what": "Talk kept as one simultaneous poll",
      "why": "The source specifies it. Bluffing about hand strength gives players something to disagree about."
    },
    {
      "what": "A SHIFT voter keeps their hand card",
      "why": "SHIFT replaces neither the hand nor the reserve, so the hand stays."
    },
    {
      "what": "Next start seat chosen after eliminations, skipping eliminated seats",
      "why": "The source says 'next active seat'."
    },
    {
      "what": "Centre feed in rounds 1-9 is limited by what remains",
      "why": "The centre cannot go negative."
    },
    {
      "what": "A drawer who keeps NEW has held_rounds reset to 0",
      "why": "Their card is no longer one kept from an earlier round."
    }
  ],
  "simplifications": [
    {
      "what": "A tie for the most kamons is a shared win rather than a declared draw",
      "why": "The engine treats players level at the top as sharing the win, with no separate draw."
    },
    {
      "what": "Reserve cards are kept in a hidden table list, indexed by seat",
      "why": "A player attribute cannot be hidden from its own owner, and the rules say the reserve is unseen until drawn."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: kamons, active, held_rounds, draw_choice, fight_choice; table: round, pot, centre, kobayakawa, start_seat.
````

## Reply

````
```json
[
{"name":"Setup: 4 kamons each, centre 11, pot 0, start seat 1, no held cards","rule":"R1","players":3,"rounds":0,
 "expect":{"players":{"1":{"kamons":4,"active":true,"held_rounds":0},"2":{"kamons":4,"active":true,"held_rounds":0},"3":{"kamons":4,"active":true,"held_rounds":0}},
 "game":{"centre":11,"pot":0,"start_seat":1,"round":1}}},

{"name":"Deck excludes held hand cards: 4 players, two holding cards, deck ends at 5","rule":"R2","players":4,"rounds":1,"default":"decline",
 "given":{"players":{"1":{"hand":7,"held_rounds":1},"2":{"hand":9,"held_rounds":1}}},
 "expect":{"lens":{"game":{"deck":5}},"players":{"1":{"held_rounds":2},"2":{"held_rounds":2},"3":{"held_rounds":1},"4":{"held_rounds":1}}}},

{"name":"Each seat without a card is dealt one: 3 players, deck ends at 7","rule":"R3","players":3,"rounds":1,"default":"decline",
 "expect":{"lens":{"game":{"deck":7}},"players":{"1":{"held_rounds":1},"2":{"held_rounds":1},"3":{"held_rounds":1}}}},

{"name":"Reserves per seat plus Kobayakawa and Alternate: 5 players, deck ends at 3","rule":"R4","players":5,"rounds":1,"default":"decline",
 "expect":{"lens":{"game":{"deck":3,"reserves":0}}}},

{"name":"Round 9 min stake 1: seat with 2 kamons may fight HIGH at stake 2","rule":"R5","players":3,"rounds":1,"default":"decline",
 "given":{"players":{"1":{"kamons":2}},"game":{"round":9}},
 "rules":[{"seat":1,"options_include":"HIGH"}],
 "expect":{"offered":[{"seat":1,"option":"HIGH"}],"players":{"1":{"kamons":3},"2":{"kamons":4},"3":{"kamons":4}},"game":{"centre":10,"pot":0,"start_seat":1}}},

{"name":"Round 10 min stake 2: seat with 2 kamons gets LOW but not HIGH, then wins the pot and the game","rule":"R5","players":3,"default":"decline",
 "given":{"players":{"1":{"kamons":2}},"game":{"round":10,"centre":3,"pot":0}},
 "rules":[{"seat":1,"options_include":"LOW"}],
 "expect":{"winner":1,"standings":{"1":5,"2":4,"3":4},"offered":[{"seat":1,"option":"LOW"}],"not_offered":[{"seat":1,"option":"HIGH"}],
 "players":{"1":{"kamons":5}},"game":{"centre":0,"pot":0}}},

{"name":"Kept card with held_rounds carries on: everyone passes","rule":"R6","players":3,"rounds":1,"default":"decline",
 "given":{"players":{"2":{"hand":5,"held_rounds":2}}},
 "expect":{"players":{"1":{"held_rounds":1},"2":{"held_rounds":3},"3":{"held_rounds":1}},"game":{"pot":1,"centre":10,"round":2,"start_seat":2}}},

{"name":"Every seat makes a draw choice and each is recorded","rule":"R7","players":3,"rounds":1,"default":"decline",
 "rules":[{"seat":1,"options_include":"DRAW"},{"seat":1,"options_include":"OLD"},{"seat":2,"options_include":"SHIFT"},{"seat":3,"options_include":"KEEP"}],
 "expect":{"players":{"1":{"draw_choice":"DRAW"},"2":{"draw_choice":"SHIFT"},"3":{"draw_choice":"KEEP"}}}},

{"name":"Only the drawer is asked OLD/NEW","rule":"R8","players":3,"rounds":1,"default":"decline",
 "rules":[{"seat":1,"options_include":"DRAW"},{"seat":1,"options_include":"OLD"}],
 "expect":{"offered":[{"seat":1,"option":"OLD"}],"not_offered":[{"seat":2,"option":"OLD"},{"seat":2,"option":"NEW"},{"seat":3,"option":"OLD"},{"seat":3,"option":"NEW"}],
 "lens":{"game":{"face_up_discards":1}}}},

{"name":"DRAW then NEW resets held_rounds and discards the old card face up","rule":"R9","players":3,"rounds":1,"default":"decline",
 "given":{"players":{"1":{"hand":6,"held_rounds":3}}},
 "rules":[{"seat":1,"options_include":"DRAW"},{"seat":1,"options_include":"NEW"}],
 "expect":{"players":{"1":{"held_rounds":1,"draw_choice":"DRAW"}},"lens":{"game":{"face_up_discards":1}}}},

{"name":"DRAW then OLD keeps the card and discards the reserve face up","rule":"R9","players":3,"rounds":1,"default":"decline",
 "given":{"players":{"1":{"hand":6,"held_rounds":3}}},
 "rules":[{"seat":1,"options_include":"DRAW"},{"seat":1,"options_include":"OLD"}],
 "expect":{"players":{"1":{"held_rounds":4}},"lens":{"game":{"face_up_discards":1}}}},

{"name":"Undrawn reserves go face down: nobody draws, no face-up discards, reserves cleared","rule":"R10","players":3,"rounds":1,"default":"decline",
 "expect":{"lens":{"game":{"reserves":0,"face_up_discards":0}},"players":{"1":{"draw_choice":"KEEP"},"2":{"draw_choice":"KEEP"},"3":{"draw_choice":"KEEP"}}}},

{"name":"All draw and keep OLD: three face-up discards and all choices revealed","rule":"R11","players":3,"rounds":1,"default":"decline",
 "rules":[{"seat":1,"options_include":"DRAW"},{"seat":2,"options_include":"DRAW"},{"seat":3,"options_include":"DRAW"},
          {"seat":1,"options_include":"OLD"},{"seat":2,"options_include":"OLD"},{"seat":3,"options_include":"OLD"}],
 "expect":{"lens":{"game":{"face_up_discards":3}},"players":{"1":{"draw_choice":"DRAW"},"2":{"draw_choice":"DRAW"},"3":{"draw_choice":"DRAW"}}}},

{"name":"SHIFT is recorded and the round plays on (new Kobayakawa value is random, not asserted)","rule":"R12","players":3,"rounds":1,"default":"decline",
 "rules":[{"seat":2,"options_include":"SHIFT"}],
 "expect":{"players":{"2":{"draw_choice":"SHIFT","held_rounds":1}},"game":{"pot":1,"centre":10}}},

{"name":"Talk step does not change kamons; all pass","rule":"R13","players":3,"rounds":1,"default":"decline",
 "expect":{"players":{"1":{"kamons":4},"2":{"kamons":4},"3":{"kamons":4}},"game":{"pot":1,"centre":10}}},

{"name":"Fight order starts at start seat 2 and wraps: HIGH by seat 2 blocks LOW for seats 3 and 1","rule":"R14","players":3,"rounds":1,"default":"decline",
 "given":{"game":{"start_seat":2}},
 "rules":[{"seat":2,"options_include":"HIGH"}],
 "expect":{"not_offered":[{"seat":3,"option":"LOW"},{"seat":1,"option":"LOW"}],
 "players":{"1":{"kamons":4},"2":{"kamons":5,"fight_choice":"HIGH"},"3":{"kamons":4}},"game":{"start_seat":2,"pot":0,"centre":10}}},

{"name":"Seat with exactly min stake gets LOW (not HIGH) and fights at stake 1","rule":"R15","players":3,"rounds":1,"default":"decline",
 "given":{"players":{"1":{"kamons":1}}},
 "rules":[{"seat":1,"options_include":"LOW"}],
 "expect":{"offered":[{"seat":1,"option":"LOW"}],"not_offered":[{"seat":1,"option":"HIGH"}],"players":{"1":{"kamons":2,"active":true,"fight_choice":"LOW"}},"game":{"pot":0,"centre":10}}},

{"name":"HIGH costs min+1 = 2","rule":"R16","players":3,"rounds":1,"default":"decline",
 "rules":[{"seat":1,"options_include":"HIGH"}],
 "expect":{"offered":[{"seat":1,"option":"HIGH"}],"players":{"1":{"kamons":5,"held_rounds":0},"2":{"kamons":4},"3":{"kamons":4}},"game":{"pot":0,"centre":10,"start_seat":1}}},

{"name":"After a HIGH, later seats are not offered LOW but may still go HIGH","rule":"R17","players":3,"rounds":1,"default":"decline",
 "rules":[{"seat":1,"options_include":"HIGH"}],
 "expect":{"not_offered":[{"seat":2,"option":"LOW"},{"seat":3,"option":"LOW"}],"offered":[{"seat":2,"option":"HIGH"},{"seat":3,"option":"HIGH"}],
 "players":{"1":{"kamons":5}}}},

{"name":"Seat with 1 kamon after a HIGH is offered only PASS","rule":"R18","players":3,"rounds":1,"default":"decline",
 "given":{"players":{"2":{"kamons":1}}},
 "rules":[{"seat":1,"options_include":"HIGH"}],
 "expect":{"not_offered":[{"seat":2,"option":"LOW"},{"seat":2,"option":"HIGH"}],"offered":[{"seat":2,"option":"PASS"}],
 "players":{"1":{"kamons":5},"2":{"kamons":1,"fight_choice":"PASS","held_rounds":1}}}},

{"name":"Both fighters pay stakes: LOW 1 and HIGH 2; card 1 always beats card 2","rule":"R19","players":3,"rounds":1,"default":"decline",
 "given":{"players":{"1":{"hand":1},"2":{"hand":2}}},
 "rules":[{"seat":1,"options_include":"LOW"},{"seat":2,"options_include":"HIGH"}],
 "expect":{"players":{"1":{"kamons":7},"2":{"kamons":2},"3":{"kamons":4}},"game":{"pot":0,"centre":10,"start_seat":1}}},

{"name":"Empty centre feeds nothing in rounds 1-9","rule":"R20","players":3,"rounds":1,"default":"decline",
 "given":{"game":{"round":3,"centre":0,"pot":5}},
 "expect":{"game":{"centre":0,"pot":5,"round":4}}},

{"name":"Round 10: whole centre goes to the pot, sole fighter takes it and wins","rule":"R21","players":3,"default":"decline",
 "given":{"game":{"round":10,"centre":6,"pot":2}},
 "rules":[{"seat":1,"options_include":"LOW"}],
 "expect":{"winner":1,"standings":{"1":12,"2":4,"3":4},"players":{"1":{"kamons":12}},"game":{"centre":0,"pot":0}}},

{"name":"Nobody fights: pot carries and gains 1 from centre","rule":"R22","players":3,"rounds":1,"default":"decline",
 "given":{"game":{"pot":3}},
 "expect":{"game":{"pot":4,"centre":10,"start_seat":2},"players":{"1":{"kamons":4},"2":{"kamons":4},"3":{"kamons":4}}}},

{"name":"Sole fighter takes the whole pot","rule":"R23","players":3,"rounds":1,"default":"decline",
 "given":{"game":{"pot":3}},
 "rules":[{"seat":1,"options_include":"LOW"}],
 "expect":{"players":{"1":{"kamons":8,"held_rounds":0},"2":{"kamons":4},"3":{"kamons":4}},"game":{"pot":0,"centre":10,"start_seat":1}}},

{"name":"Showdown: card 1 plus Kobayakawa always beats card 2","rule":"R24","players":3,"rounds":1,"default":"decline",
 "given":{"players":{"1":{"hand":2},"2":{"hand":1}}},
 "rules":[{"seat":1,"options_include":"LOW"},{"seat":2,"options_include":"LOW"}],
 "expect":{"players":{"1":{"kamons":3,"held_rounds":0},"2":{"kamons":6,"held_rounds":0},"3":{"kamons":4,"held_rounds":1}},"game":{"pot":0,"centre":10,"start_seat":2}}},

{"name":"Possible tie in round 1-9 (chance: only what cannot change is asserted; card 3 never wins vs card 1)","rule":"R25","players":3,"rounds":1,"default":"decline",
 "given":{"players":{"1":{"hand":3},"2":{"hand":1}}},
 "rules":[{"seat":1,"options_include":"LOW"},{"seat":2,"options_include":"LOW"}],
 "expect":{"players":{"1":{"kamons":3,"held_rounds":0},"3":{"kamons":4}},"game":{"centre":10}}},

{"name":"Round 10 showdown, tie or not (chance): pot and centre end at 0","rule":"R26","players":3,"rounds":1,"default":"decline",
 "given":{"players":{"1":{"hand":5},"2":{"hand":1}},"game":{"round":10,"centre":2,"pot":0}},
 "rules":[{"seat":1,"options_include":"LOW"},{"seat":2,"options_include":"LOW"}],
 "expect":{"players":{"3":{"kamons":4}},"game":{"pot":0,"centre":0}}},

{"name":"Cleanup: fighter's held_rounds resets, passers add 1","rule":"R27","players":3,"rounds":1,"default":"decline",
 "given":{"players":{"1":{"hand":4,"held_rounds":2},"2":{"hand":9,"held_rounds":3}}},
 "rules":[{"seat":1,"options_include":"LOW"}],
 "expect":{"players":{"1":{"held_rounds":0},"2":{"held_rounds":4},"3":{"held_rounds":1}}}},

{"name":"Pot winner becomes next start seat","rule":"R28","players":3,"rounds":1,"default":"decline",
 "rules":[{"seat":3,"options_include":"LOW"}],
 "expect":{"game":{"start_seat":3},"players":{"3":{"kamons":5}}}},

{"name":"No pot winner: start seat moves to next seat, wrapping from 3 to 1","rule":"R28","players":3,"rounds":1,"default":"decline",
 "given":{"game":{"start_seat":3}},
 "expect":{"game":{"start_seat":1,"pot":1}}},

{"name":"Seat dropping to 0 kamons is eliminated","rule":"R29","players":3,"rounds":1,"default":"decline",
 "given":{"players":{"1":{"hand":1},"2":{"hand":2,"kamons":1}}},
 "rules":[{"seat":1,"options_include":"LOW"},{"seat":2,"options_include":"LOW"}],
 "expect":{"players":{"1":{"kamons":6,"active":true},"2":{"kamons":0,"active":false},"3":{"kamons":4,"active":true}},"game":{"start_seat":1}}},

{"name":"Game ends when only one active seat remains; it wins","rule":"R30","players":3,"default":"decline",
 "given":{"players":{"1":{"hand":1},"2":{"hand":2,"kamons":1},"3":{"hand":3,"kamons":1}}},
 "rules":[{"seat":1,"options_include":"LOW"},{"seat":2,"options_include":"LOW"},{"seat":3,"options_include":"LOW"}],
 "expect":{"winner":1,"standings":{"1":7,"2":0,"3":0},"players":{"1":{"kamons":7},"2":{"active":false},"3":{"active":false}}}}
]
```
````
