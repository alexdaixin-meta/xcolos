# 07 spec

- time: 2026-10-27T18:20:01+00:00 (37.6s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 c8106db994a5af39, reply sha256 3a835a1b9cd47bc2

## Sent

````
Game: Cat in the Sack: Paid Entry
Players in the source: 3 to 5
Suggested table size, chosen by the designer of these rules (keep it): 4

Rules, as filed in the inventory:
SETUP
- Every player receives the same 9 cards: cats worth -8, -5, 3, 5, 8, 11 and 15, one Rabbit worth 0, and one Dog worth 0.
- One card is removed at random from each hand. Its owner is told which card it is. No one else is told.
- Each player starts with 15 mice and 0 cat points. The bank of mice is unlimited.
- Seats are numbered. Seat 1 is the start player in round 1.
- The game lasts 8 rounds, so every remaining card is played.

EACH ROUND
1. Start player. In round 1 it is Seat 1. In each later round it is the next seat in order. The start player matters only for breaking ties.
2. Fill the sack. All players at the same time secretly choose one card from their hand and place it in the sack. Placed cards never return.
3. Shuffle. The engine shuffles the sack into a random order.
4. First reveal. Cards are shown from the front of the shuffled order. With 3 players, 1 card is shown. With 4 or 5 players, 2 cards are shown. Revealed cards do not say who placed them.
5. Talk. Every player writes one short message at the same time, without seeing the others' messages. All messages are then shown. Claims are not binding and may be lies.
6. Stay or drop. All players at the same time choose STAY or DROP. A player with fewer than 2 mice must DROP.
7. Entry and drop payment. Each player who chose STAY pays 1 mouse to the bank immediately. This fee is never refunded. Each player who chose DROP receives 2 mice from the bank and is out for this round.
8. Second reveal. The next card in the shuffled order is shown to everyone.
9. Sealed bid. Every player who chose STAY secretly bids a whole number of mice, from 1 up to their current mice (counted after paying the fee). All bids are revealed together.
10. Winner. The highest bidder wins the sack.
   - If two or more players tie for the highest bid, the tied player with fewer current mice wins.
   - If they are still tied, the tied player who comes first in seat order, counting from the start player, wins.
   - If nobody stayed, nobody wins and the sack is discarded.
   - If exactly one player stayed, that player wins and pays their bid.
11. Sack value. All remaining sack cards are revealed. The sack's value is the sum of the cats in it. The Rabbit and Dogs are worth 0.
   - If exactly one Dog is in the sack and the sack holds at least one cat, the cat with the highest value is removed before summing.
   - Two or more Dogs have no effect.
12. Payment. The winner pays their bid to the bank and adds the sack's value to their cat points. The value may be negative.
13. Losing stayers receive nothing. They have already paid their fee.
14. Discard. All sack cards are discarded face up, so everyone can count which cards have been used.
15. End check. After round 8 the game ends.

SCORING
Each player's total is their cat points plus their mice.

How the winner is decided: After round 8 the player with the highest total (cat points plus mice) wins. If totals are tied, the tied player with the most cat points wins. If that is also tied, the game is a draw among those players.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
```json
{
  "name": "Cat in the Sack: Paid Entry",
  "summary": "Each round every player secretly puts one card into a shared sack. Some sack cards are revealed, players talk, then pay to stay or get paid to drop. Stayers bid sealed mice for the sack, whose cat value may be negative.",
  "players": {"min": 3, "max": 5, "suggested": 4},
  "parameters": {
    "hand_cat_values": [-8, -5, 3, 5, 8, 11, 15],
    "rabbit_value": 0,
    "dog_value": 0,
    "cards_per_hand": 9,
    "cards_removed_per_hand": 1,
    "starting_mice": 15,
    "starting_cat_points": 0,
    "rounds": 8,
    "stay_fee": 1,
    "drop_payment": 2,
    "min_mice_to_stay": 2,
    "min_bid": 1,
    "first_reveal_with_3_players": 1,
    "first_reveal_with_4_or_5_players": 2,
    "second_reveal_count": 1,
    "dogs_that_cancel_top_cat": 1
  },
  "attributes": {
    "player": [
      {"key": "hand", "type": "list", "visible": "ally", "initial": ["cat_-8", "cat_-5", "cat_3", "cat_5", "cat_8", "cat_11", "cat_15", "rabbit", "dog"], "meaning": "Cards still held. Before round 1 it holds 8 cards, after one is removed at random.", "observable": false},
      {"key": "removed_card", "type": "text", "visible": "ally", "initial": "", "meaning": "The card removed at random from this player's hand at setup. Only its owner knows it.", "observable": false},
      {"key": "placed_card", "type": "text", "visible": "ally", "initial": "", "meaning": "The card this player put into the sack this round.", "observable": false},
      {"key": "mice", "type": "number", "visible": "public", "initial": 15, "meaning": "Current mice.", "observable": true},
      {"key": "cat_points", "type": "number", "visible": "public", "initial": 0, "meaning": "Accumulated sack values won.", "observable": true},
      {"key": "stayed", "type": "bool", "visible": "public", "initial": false, "meaning": "True if the player chose STAY this round.", "observable": true},
      {"key": "bid", "type": "number", "visible": "public", "initial": 0, "meaning": "Sealed bid this round, revealed with all other bids. 0 if the player dropped.", "observable": true},
      {"key": "message", "type": "text", "visible": "public", "initial": "", "meaning": "This round's talk message. Not binding.", "observable": false}
    ],
    "game": [
      {"key": "round", "type": "number", "visible": "public", "initial": 0, "meaning": "Current round number, 1 to 8.", "observable": true},
      {"key": "start_seat", "type": "number", "visible": "public", "initial": 1, "meaning": "Start player this round, used only for the final tie-break.", "observable": true},
      {"key": "sack", "type": "list", "visible": "none", "initial": [], "meaning": "This round's sack cards in shuffled order. It does not record who placed which card.", "observable": false},
      {"key": "revealed_cards", "type": "list", "visible": "public", "initial": [], "meaning": "Sack cards shown so far this round, without owners.", "observable": true},
      {"key": "discard", "type": "list", "visible": "public", "initial": [], "meaning": "All face-up discarded sack cards from earlier rounds.", "observable": true},
      {"key": "stayer_count", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of players who chose STAY this round.", "observable": false},
      {"key": "winner_seat", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat that won the sack this round, or 0 if nobody did.", "observable": true},
      {"key": "sack_value", "type": "number", "visible": "public", "initial": 0, "meaning": "Computed value of this round's sack.", "observable": true}
    ]
  },
  "setup": [
    "Every player's hand is set to the same 9 cards: cat_-8, cat_-5, cat_3, cat_5, cat_8, cat_11, cat_15, rabbit and dog.",
    "For each player, one card is picked at random from their hand, removed from the hand and stored in that player's removed_card, which only that player can see.",
    "Each player's mice is set to 15 and cat_points to 0. The bank is unlimited, so it is not tracked.",
    "round is set to 0, start_seat to 1, and sack, revealed_cards and discard to empty lists."
  ],
  "round": [
    {"action": "update", "who": "table", "answer": null, "effect": "round += 1. start_seat = ((round - 1) mod player_count) + 1. Every player: stayed = false, bid = 0, placed_card = ''. sack = [], revealed_cards = [], winner_seat = 0, sack_value = 0. Announce the round and the start seat."},
    {"action": "poll", "who": "all players", "answer": "one card from your own hand", "effect": "Each player's choice is removed from hand, stored in placed_card and appended to sack. Nobody sees the choices."},
    {"action": "update", "who": "table", "answer": null, "effect": "Shuffle the sack: rebuild it by repeatedly drawing a card at random from it, which gives a random order."},
    {"action": "update", "who": "table", "answer": null, "effect": "First reveal: append the first k cards of sack to revealed_cards, where k = 1 if player_count = 3, else 2. Tell everyone the revealed cards, without owners."},
    {"action": "poll", "who": "all players", "answer": "short text message", "effect": "message is set for each player. Broadcast {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"} once all messages are in."},
    {"action": "poll", "who": "all players", "answer": "STAY or DROP (DROP only, if mice < 2)", "effect": "stayed = true for STAY, false for DROP. stayer_count = number of players with stayed = true. All choices are shown together."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Each player with stayed = true: mice -= 1 (never refunded). Each player with stayed = false: mice += 2."},
    {"action": "update", "who": "table", "answer": null, "effect": "Second reveal: append sack card number k+1 to revealed_cards, where k is the first-reveal count. Tell everyone."},
    {"action": "poll", "who": "each player with stayed = true", "answer": "whole number from 1 to your current mice", "effect": "bid is set for each stayer. All bids are revealed together."},
    {"action": "update", "who": "table", "answer": null, "effect": "If stayer_count = 0: winner_seat = 0. Otherwise winner_seat is the stayer with the highest key = bid * 100000 - mice * 100 - ((seat - start_seat + player_count) mod player_count). The ordering is: highest bid, then fewer current mice, then first in seat order counting from start_seat. Announce it."},
    {"action": "update", "who": "table", "answer": null, "effect": "Reveal all sack cards to everyone. Let cats = the values of the cat_ cards in sack, and dogs = the count of 'dog' in sack. sack_value = sum(cats), minus max(cats) if dogs = 1 and at least one cat is present. Rabbit and dog are worth 0, and 2 or more dogs have no effect. Announce sack_value."},
    {"action": "update", "who": "the winner_seat player", "answer": null, "effect": "If winner_seat != 0: that player's mice -= bid and cat_points += sack_value (which may be negative). Losing stayers change nothing more."},
    {"action": "update", "who": "table", "answer": null, "effect": "Append every sack card to discard (face up, public). sack = []. Announce mice and cat_points."},
    {"action": "check", "who": "table", "answer": null, "effect": "If round >= 8, end the game. Otherwise continue to the next round."}
  ],
  "ending": {
    "condition": "round >= 8",
    "rank_by": "(you.mice + you.cat_points) * 1000 + you.cat_points",
    "decided_by": "Each player's total is cat_points plus mice, and the highest total wins. If totals tie, the tied player with more cat points wins. If that also ties, those players share the win (a draw)."
  },
  "rules": [
    {"id": "R1", "text": "At setup every player's hand holds cat_-8, cat_-5, cat_3, cat_5, cat_8, cat_11, cat_15, rabbit and dog (9 cards)."},
    {"id": "R2", "text": "At setup exactly one random card is removed from each hand and recorded in that player's removed_card, visible only to that player, leaving 8 cards in hand."},
    {"id": "R3", "text": "At setup each player has mice = 15 and cat_points = 0."},
    {"id": "R4", "text": "In round r, start_seat = ((r - 1) mod player_count) + 1, so it is seat 1 in round 1 and seat 2 in round 2."},
    {"id": "R5", "text": "Each round every player simultaneously places one card from their hand into the sack, and that card leaves their hand permanently."},
    {"id": "R6", "text": "After shuffling, the first reveal shows 1 sack card with 3 players and 2 sack cards with 4 or 5 players, without naming who placed them."},
    {"id": "R7", "text": "Each round every player sends one simultaneous short message, and all messages are shown only after all are in. Messages are not binding."},
    {"id": "R8", "text": "When a player has fewer than 2 mice at the stay-or-drop step, they may only choose DROP."},
    {"id": "R9", "text": "When a player chooses STAY, they immediately pay 1 mouse, which is never refunded."},
    {"id": "R10", "text": "When a player chooses DROP, they receive 2 mice and take no further part in that round."},
    {"id": "R11", "text": "After stay-or-drop, one more sack card is revealed to everyone."},
    {"id": "R12", "text": "Each stayer bids a whole number from 1 to their mice after paying the fee, and all bids are revealed together."},
    {"id": "R13", "text": "When bids differ, the highest bidder wins the sack."},
    {"id": "R14", "text": "When two or more stayers tie for the highest bid, the tied stayer with fewer current mice wins."},
    {"id": "R15", "text": "When the tied stayers also have equal mice, the one first in seat order counting from start_seat wins."},
    {"id": "R16", "text": "When nobody stays, nobody wins, no bid is paid and the sack is discarded."},
    {"id": "R17", "text": "When exactly one player stays, that player wins the sack and pays their bid."},
    {"id": "R18", "text": "The sack value is the sum of its cat card values. The rabbit and dogs are worth 0."},
    {"id": "R19", "text": "When the sack holds exactly 1 dog and at least one cat, the highest-valued cat is excluded from the sum (for example, cat_15 + cat_3 + dog + rabbit = 3)."},
    {"id": "R20", "text": "When the sack holds 2 or more dogs, they have no effect (for example, cat_15 + dog + dog = 15)."},
    {"id": "R21", "text": "The winner pays their bid in mice and adds the sack value, which may be negative, to cat_points."},
    {"id": "R22", "text": "Losing stayers receive nothing and keep the 1-mouse fee paid."},
    {"id": "R23", "text": "All sack cards are added to the public discard list at the end of each round."},
    {"id": "R24", "text": "The game ends after round 8."},
    {"id": "R25", "text": "The player with the highest cat_points + mice wins. On a tie the higher cat_points wins, and if that also ties those players share the win."}
  ],
  "offers": [
    {"question": "Fill the sack", "who": "all players", "options": "any card currently in that player's own hand"},
    {"question": "Talk", "who": "all players", "options": "one short free-text message"},
    {"question": "Stay or drop", "who": "all players", "options": "a player with mice >= 2: STAY, DROP. A player with mice < 2: DROP only."},
    {"question": "Sealed bid", "who": "each player with stayed = true", "options": "a whole number from 1 to that player's current mice (after the fee). Players who dropped are not asked."}
  ],
  "choices": [
    {"what": "3 to 5 players, suggested 4", "why": "The designer chose 4 and the source allows 3 to 5. 3 is the minimum because an auction needs rivals and the sack needs enough unknown cards to hide one's own. 5 is the maximum because the hand and reveal structure is built for 5, and more seats would make one's own card nearly irrelevant to the sack."},
    {"what": "Talk kept as a simultaneous poll with broadcast", "why": "The source specifies simultaneous non-binding messages. Players disagree about the sack, since each wants others to drop or to overbid, so bluffing about one's placed card gives the others something to reason about."},
    {"what": "Cards encoded as text labels cat_<value>, rabbit and dog", "why": "The rabbit and dog are both worth 0 but behave differently, so a label is needed to count dogs."},
    {"what": "Sack winner computed as one key: bid * 100000 - mice * 100 - seat offset from start_seat", "why": "This puts the source's three-level tie-break (bid, fewer mice, seat order from the start player) into a single arithmetic maximum."},
    {"what": "Ranking expression (mice + cat_points) * 1000 + cat_points", "why": "Cat points can never reach plus or minus 500, so the total is compared first and cat points break ties. Exact ties share the win, which is the source's draw."},
    {"what": "Stay/drop choices and bids are public once revealed", "why": "The source reveals bids together, and paying the fee or receiving the drop payment is visible. Who placed which card stays secret."},
    {"what": "Strategy at the table", "why": "A thoughtful player infers others' cards from the public discard, the reveals and their own removed card, bluffs in talk, and weighs the 1-mouse fee against the 2-mouse drop payment. They also use the fewer-mice tie-break and the dog rule when sizing a bid."}
  ],
  "simplifications": [
    {"what": "The shuffle is done by drawing the sack cards at random into a new order", "why": "The engine shuffles by random draws from a list."},
    {"what": "The bank of mice is not tracked", "why": "It is unlimited, so only player mice change."},
    {"what": "A draw is represented as a shared win among the players tied at the top", "why": "The engine has no separate draw outcome."}
  ],
  "unsupported": []
}
```

Why it was refused: parameters must map each name to a number
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "name": "Cat in the Sack: Paid Entry",
  "summary": "Each round every player secretly puts one card into a shared sack. Some sack cards are revealed, players talk, then pay to stay or get paid to drop. Stayers bid sealed mice for the sack, whose cat value may be negative.",
  "players": {"min": 3, "max": 5, "suggested": 4},
  "parameters": {
    "cat_value_1": -8,
    "cat_value_2": -5,
    "cat_value_3": 3,
    "cat_value_4": 5,
    "cat_value_5": 8,
    "cat_value_6": 11,
    "cat_value_7": 15,
    "rabbit_value": 0,
    "dog_value": 0,
    "cards_per_hand": 9,
    "cards_removed_per_hand": 1,
    "starting_mice": 15,
    "starting_cat_points": 0,
    "rounds": 8,
    "stay_fee": 1,
    "drop_payment": 2,
    "min_mice_to_stay": 2,
    "min_bid": 1,
    "first_reveal_with_3_players": 1,
    "first_reveal_with_4_or_5_players": 2,
    "second_reveal_count": 1,
    "dogs_that_cancel_top_cat": 1,
    "start_seat_round_1": 1
  },
  "attributes": {
    "player": [
      {"key": "hand", "type": "list", "visible": "ally", "initial": ["cat_-8", "cat_-5", "cat_3", "cat_5", "cat_8", "cat_11", "cat_15", "rabbit", "dog"], "meaning": "Cards still held. Before round 1 it holds 8 cards, after one is removed at random.", "observable": false},
      {"key": "removed_card", "type": "text", "visible": "ally", "initial": "", "meaning": "The card removed at random from this player's hand at setup. Only its owner knows it.", "observable": false},
      {"key": "placed_card", "type": "text", "visible": "ally", "initial": "", "meaning": "The card this player put into the sack this round.", "observable": false},
      {"key": "mice", "type": "number", "visible": "public", "initial": 15, "meaning": "Current mice.", "observable": true},
      {"key": "cat_points", "type": "number", "visible": "public", "initial": 0, "meaning": "Accumulated sack values won.", "observable": true},
      {"key": "stayed", "type": "bool", "visible": "public", "initial": false, "meaning": "True if the player chose STAY this round.", "observable": true},
      {"key": "bid", "type": "number", "visible": "public", "initial": 0, "meaning": "Sealed bid this round, revealed with all other bids. 0 if the player dropped.", "observable": true},
      {"key": "message", "type": "text", "visible": "public", "initial": "", "meaning": "This round's talk message. Not binding.", "observable": false}
    ],
    "game": [
      {"key": "round", "type": "number", "visible": "public", "initial": 0, "meaning": "Current round number, 1 to 8.", "observable": true},
      {"key": "start_seat", "type": "number", "visible": "public", "initial": 1, "meaning": "Start player this round, used only for the sack tie-break.", "observable": true},
      {"key": "sack", "type": "list", "visible": "none", "initial": [], "meaning": "This round's sack cards in shuffled order. It does not record who placed which card.", "observable": false},
      {"key": "revealed_cards", "type": "list", "visible": "public", "initial": [], "meaning": "Sack cards shown so far this round, without owners.", "observable": true},
      {"key": "discard", "type": "list", "visible": "public", "initial": [], "meaning": "All face-up discarded sack cards from earlier rounds.", "observable": true},
      {"key": "stayer_count", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of players who chose STAY this round.", "observable": false},
      {"key": "winner_seat", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat that won the sack this round, or 0 if nobody did.", "observable": true},
      {"key": "sack_value", "type": "number", "visible": "public", "initial": 0, "meaning": "Computed value of this round's sack.", "observable": true}
    ]
  },
  "setup": [
    "Every player's hand is set to the same 9 cards: cat_-8, cat_-5, cat_3, cat_5, cat_8, cat_11, cat_15, rabbit and dog.",
    "For each player, one card is picked at random from their hand, removed from the hand and stored in that player's removed_card, which only that player can see.",
    "Each player's mice is set to 15 and cat_points to 0. The bank is unlimited, so it is not tracked.",
    "round is set to 0, start_seat to 1, and sack, revealed_cards and discard to empty lists."
  ],
  "round": [
    {"action": "update", "who": "table", "answer": null, "effect": "round += 1. start_seat = ((round - 1) mod player_count) + 1. Every player: stayed = false, bid = 0, placed_card = ''. sack = [], revealed_cards = [], winner_seat = 0, sack_value = 0. Announce the round and the start seat."},
    {"action": "poll", "who": "all players", "answer": "one card from your own hand", "effect": "Each player's choice is removed from hand, stored in placed_card and appended to sack. Nobody sees the choices."},
    {"action": "update", "who": "table", "answer": null, "effect": "Shuffle the sack: rebuild it by repeatedly drawing a card at random from it, which gives a random order."},
    {"action": "update", "who": "table", "answer": null, "effect": "First reveal: append the first k cards of sack to revealed_cards, where k = 1 if player_count = 3, else 2. Tell everyone the revealed cards, without owners."},
    {"action": "poll", "who": "all players", "answer": "short text message", "effect": "message is set for each player. Broadcast {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"} once all messages are in."},
    {"action": "poll", "who": "all players", "answer": "STAY or DROP (DROP only, if mice < 2)", "effect": "stayed = true for STAY, false for DROP. stayer_count = number of players with stayed = true. All choices are shown together."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Each player with stayed = true: mice -= 1 (never refunded). Each player with stayed = false: mice += 2."},
    {"action": "update", "who": "table", "answer": null, "effect": "Second reveal: append sack card number k+1 to revealed_cards, where k is the first-reveal count. Tell everyone."},
    {"action": "poll", "who": "each player with stayed = true", "answer": "whole number from 1 to your current mice", "effect": "bid is set for each stayer. All bids are revealed together."},
    {"action": "update", "who": "table", "answer": null, "effect": "If stayer_count = 0: winner_seat = 0. Otherwise winner_seat is the stayer with the highest key = bid * 100000 - mice * 100 - ((seat - start_seat + player_count) mod player_count). The ordering is: highest bid, then fewer current mice, then first in seat order counting from start_seat. Announce it."},
    {"action": "update", "who": "table", "answer": null, "effect": "Reveal all sack cards to everyone. Let cats = the values of the cat_ cards in sack, and dogs = the count of 'dog' in sack. sack_value = sum(cats), minus max(cats) if dogs = 1 and at least one cat is present. Rabbit and dog are worth 0, and 2 or more dogs have no effect. Announce sack_value."},
    {"action": "update", "who": "the winner_seat player", "answer": null, "effect": "If winner_seat != 0: that player's mice -= bid and cat_points += sack_value (which may be negative). Losing stayers change nothing more."},
    {"action": "update", "who": "table", "answer": null, "effect": "Append every sack card to discard (face up, public). sack = []. Announce mice and cat_points."},
    {"action": "check", "who": "table", "answer": null, "effect": "If round >= 8, end the game. Otherwise continue to the next round."}
  ],
  "ending": {
    "condition": "round >= 8",
    "rank_by": "(you.mice + you.cat_points) * 1000 + you.cat_points",
    "decided_by": "Each player's total is cat_points plus mice, and the highest total wins. If totals tie, the tied player with more cat points wins. If that also ties, those players share the win (a draw)."
  },
  "rules": [
    {"id": "R1", "text": "At setup every player's hand holds cat_-8, cat_-5, cat_3, cat_5, cat_8, cat_11, cat_15, rabbit and dog (9 cards)."},
    {"id": "R2", "text": "At setup exactly one random card is removed from each hand and recorded in that player's removed_card, visible only to that player, leaving 8 cards in hand."},
    {"id": "R3", "text": "At setup each player has mice = 15 and cat_points = 0."},
    {"id": "R4", "text": "In round r, start_seat = ((r - 1) mod player_count) + 1, so it is seat 1 in round 1 and seat 2 in round 2."},
    {"id": "R5", "text": "Each round every player simultaneously places one card from their hand into the sack, and that card leaves their hand permanently."},
    {"id": "R6", "text": "After shuffling, the first reveal shows 1 sack card with 3 players and 2 sack cards with 4 or 5 players, without naming who placed them."},
    {"id": "R7", "text": "Each round every player sends one simultaneous short message, and all messages are shown only after all are in. Messages are not binding."},
    {"id": "R8", "text": "When a player has fewer than 2 mice at the stay-or-drop step, they may only choose DROP."},
    {"id": "R9", "text": "When a player chooses STAY, they immediately pay 1 mouse, which is never refunded."},
    {"id": "R10", "text": "When a player chooses DROP, they receive 2 mice and take no further part in that round."},
    {"id": "R11", "text": "After stay-or-drop, one more sack card is revealed to everyone."},
    {"id": "R12", "text": "Each stayer bids a whole number from 1 to their mice after paying the fee, and all bids are revealed together."},
    {"id": "R13", "text": "When bids differ, the highest bidder wins the sack."},
    {"id": "R14", "text": "When two or more stayers tie for the highest bid, the tied stayer with fewer current mice wins."},
    {"id": "R15", "text": "When the tied stayers also have equal mice, the one first in seat order counting from start_seat wins."},
    {"id": "R16", "text": "When nobody stays, nobody wins, no bid is paid and the sack is discarded."},
    {"id": "R17", "text": "When exactly one player stays, that player wins the sack and pays their bid."},
    {"id": "R18", "text": "The sack value is the sum of its cat card values. The rabbit and dogs are worth 0."},
    {"id": "R19", "text": "When the sack holds exactly 1 dog and at least one cat, the highest-valued cat is excluded from the sum (for example, cat_15 + cat_3 + dog + rabbit = 3)."},
    {"id": "R20", "text": "When the sack holds 2 or more dogs, they have no effect (for example, cat_15 + dog + dog = 15)."},
    {"id": "R21", "text": "The winner pays their bid in mice and adds the sack value, which may be negative, to cat_points."},
    {"id": "R22", "text": "Losing stayers receive nothing and do not get back the 1-mouse fee."},
    {"id": "R23", "text": "All sack cards are added to the public discard list at the end of each round."},
    {"id": "R24", "text": "The game ends after round 8."},
    {"id": "R25", "text": "The player with the highest cat_points + mice wins. On a tie the higher cat_points wins, and if that also ties those players share the win."}
  ],
  "offers": [
    {"question": "Fill the sack", "who": "all players", "options": "any card currently in that player's own hand"},
    {"question": "Talk", "who": "all players", "options": "one short free-text message"},
    {"question": "Stay or drop", "who": "all players", "options": "a player with mice >= 2: STAY, DROP. A player with mice < 2: DROP only."},
    {"question": "Sealed bid", "who": "each player with stayed = true", "options": "a whole number from 1 to that player's current mice (after the fee). Players who dropped are not asked."}
  ],
  "choices": [
    {"what": "3 to 5 players, suggested 4", "why": "The designer chose 4 and the source allows 3 to 5. 3 is the minimum because an auction needs rivals and the sack needs enough unknown cards to hide one's own. 5 is the maximum because the hand and reveal structure is built for 5, and with more seats one's own card would barely affect the sack."},
    {"what": "Talk kept as a simultaneous poll with broadcast", "why": "The source specifies simultaneous non-binding messages. Players disagree about the sack, since each wants others to drop or to overbid, so bluffing about one's placed card gives the others something to reason about."},
    {"what": "Cards encoded as text labels cat_<value>, rabbit and dog", "why": "The rabbit and dog are both worth 0 but behave differently, so a label is needed to count dogs."},
    {"what": "Cat card values listed as separate parameters cat_value_1 to cat_value_7", "why": "Each parameter must be a single number."},
    {"what": "Sack winner computed as one key: bid * 100000 - mice * 100 - seat offset from start_seat", "why": "This puts the source's three-level tie-break (bid, fewer mice, seat order from the start player) into a single arithmetic maximum."},
    {"what": "Ranking expression (mice + cat_points) * 1000 + cat_points", "why": "Cat points can never reach plus or minus 500, so the total is compared first and cat points break ties. Exact ties share the win, which is the source's draw."},
    {"what": "Stay/drop choices and bids are public once revealed", "why": "The source reveals bids together, and paying the fee or receiving the drop payment is visible. Who placed which card stays secret."},
    {"what": "Strategy at the table", "why": "A thoughtful player infers others' cards from the public discard, the reveals and their own removed card. They bluff in talk and weigh the 1-mouse fee against the 2-mouse drop payment. They also use the fewer-mice tie-break and the dog rule when sizing a bid."}
  ],
  "simplifications": [
    {"what": "The shuffle is done by drawing the sack cards at random into a new order", "why": "The engine shuffles by random draws from a list."},
    {"what": "The bank of mice is not tracked", "why": "It is unlimited, so only player mice change."},
    {"what": "A draw is represented as a shared win among the players tied at the top", "why": "The engine has no separate draw outcome."}
  ],
  "unsupported": []
}
```
````
