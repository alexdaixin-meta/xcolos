# 21 spec

- time: 2026-10-27T21:38:24+00:00 (51.7s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 0e90bea580caf66c, reply sha256 b1b2168d4e2af14e

## Sent

````
Game: Duel Durak (seeded)
Players in the source: 2 to 2
Suggested table size, chosen by the designer of these rules (keep it): 2

Rules, as filed in the inventory:
CARDS. 36 cards: suits Clubs (index 0), Diamonds (1), Hearts (2), Spades (3); ranks 6, 7, 8, 9, 10, J=11, Q=12, K=13, A=14. Each card has an id = suit index × 9 + (rank − 6), from 0 to 35. Hands, the discard pile and the set-aside pile are always kept as lists sorted ascending by id, and are always shown and read in that order.

CARD STRENGTH. Card X beats card Y if: (a) X has the same suit as Y and a higher rank; or (b) X is a trump and Y is not.

ROUND 1 (setup, no bout).
Step 1. Build the deck as the ordered list of ids 0 to 35. Shuffle it once with the engine's seeded shuffle. This is the only random operation in the game; no clock or other random source is ever used. Positions 1–8 go to player 1's hand, positions 9–16 to player 2's hand, and positions 17–36 to the set-aside pile. The set-aside pile stays face down for the whole game and is never drawn from. Each player is told only their own hand. Both players are told that each holds 8 cards.
Step 2. Player 2 names two different suits as the offer. If the answer is missing or illegal, the offer is Hearts and Spades.
Step 3. Player 1 picks one of the two offered suits as trump. If the answer is missing or illegal, trump is the offered suit with the lower suit index.
Step 4. The trump suit is announced. The first attacker is the player holding the lowest-rank trump. If neither player holds a trump, player 2 attacks first. The other player is the defender.

ROUNDS 2 TO 40 (one bout each, played only while both players hold cards).
Step 5 (attack). The attacker plays one card from their hand face up. If the answer is missing or illegal, the attacker plays their lowest-rank card, with ties broken by lower suit index.
Step 6 (defence 1). The defender either plays one card from their hand that beats the attack card, or says TAKE. A missing or illegal answer counts as TAKE.
Step 7 (throw-in). The attacker may add one card from their hand whose rank equals the rank of any card now on the table, or say PASS. A throw-in is allowed even if the defender said TAKE; the defender then takes it too. The attacker may not throw in if the defender has not said TAKE and has no cards left in hand. A missing or illegal answer counts as PASS.
Step 8 (defence 2). This step happens only if a card was thrown in and the defender has not said TAKE. The defender either plays one card that beats the thrown-in card, or says TAKE. A missing or illegal answer counts as TAKE.
Step 9 (resolution). If the defender said TAKE at any point, all cards on the table go into the defender's hand, and the same attacker attacks again next bout. Otherwise, all cards on the table go to the discard pile, and the defender becomes the attacker for the next bout.
Step 10 (announcement). Announce all cards played this bout in order, the result, and both players' hand sizes.

END. After a bout's resolution, if exactly one player has 0 cards, that player wins. If both have 0 cards, the game is a draw. If both players still hold cards after round 40, the player with fewer cards wins; equal counts are a draw.

DETERMINISM. Given the same seed, the game must produce identical logs. Every fallback is the fixed rule stated above, computed from the sorted lists.

How the winner is decided: The first player whose hand reaches 0 cards after a bout wins. If both reach 0 at the same resolution, the game is a draw. If round 40 ends with both players holding cards, the player with fewer cards wins; equal counts are a draw.
````

## Reply

````
```json
{
  "name": "Duel Durak (seeded)",
  "summary": "Two-player Durak with a fixed 8-card hand each, no drawing, a trump picked by offer and choice, and up to 39 single-attack bouts. The first player to empty their hand wins.",
  "players": {"min": 2, "max": 2, "suggested": 2},
  "parameters": {
    "deck_size": 36,
    "suit_count": 4,
    "ranks_per_suit": 9,
    "lowest_rank": 6,
    "highest_rank": 14,
    "hand_size_start": 8,
    "set_aside_size": 20,
    "deal_p1_first_position": 1,
    "deal_p1_last_position": 8,
    "deal_p2_first_position": 9,
    "deal_p2_last_position": 16,
    "set_aside_first_position": 17,
    "set_aside_last_position": 36,
    "offer_suit_count": 2,
    "default_offer_suit_a": 2,
    "default_offer_suit_b": 3,
    "default_first_attacker_seat": 2,
    "first_bout_round": 2,
    "last_round": 40,
    "max_bouts": 39,
    "max_throw_ins_per_bout": 1
  },
  "attributes": {
    "player": [
      {"key": "hand", "type": "list", "visible": "ally", "initial": [], "meaning": "Card ids held by this player, always sorted ascending by id.", "observable": false},
      {"key": "hand_size", "type": "number", "visible": "public", "initial": 8, "meaning": "Number of cards in hand. This is the score: fewer is better.", "observable": true}
    ],
    "game": [
      {"key": "deck", "type": "list", "visible": "none", "initial": [], "meaning": "The ordered ids 0..35, shuffled once with the seeded shuffle and then dealt from by position.", "observable": false},
      {"key": "set_aside", "type": "list", "visible": "none", "initial": [], "meaning": "Shuffled positions 17-36 (20 cards), sorted ascending. Face down and never drawn from.", "observable": false},
      {"key": "discard", "type": "list", "visible": "public", "initial": [], "meaning": "Cards from successfully defended bouts, sorted ascending by id.", "observable": false},
      {"key": "offer", "type": "list", "visible": "public", "initial": [], "meaning": "The two different suit indices offered by player 2.", "observable": false},
      {"key": "trump", "type": "number", "visible": "public", "initial": -1, "meaning": "Suit index of trump (0 Clubs, 1 Diamonds, 2 Hearts, 3 Spades).", "observable": true},
      {"key": "attacker", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat (1 or 2) of the current attacker. The other seat is the defender.", "observable": true},
      {"key": "table_cards", "type": "list", "visible": "public", "initial": [], "meaning": "Cards played this bout, in the order they were played.", "observable": false},
      {"key": "attack_card", "type": "number", "visible": "public", "initial": -1, "meaning": "Id of this bout's attack card.", "observable": false},
      {"key": "throw_card", "type": "number", "visible": "public", "initial": -1, "meaning": "Id of this bout's thrown-in card, or -1 if none.", "observable": false},
      {"key": "defender_took", "type": "bool", "visible": "public", "initial": false, "meaning": "Whether the defender said TAKE this bout.", "observable": false},
      {"key": "bout", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of bouts completed (round number minus 1).", "observable": true}
    ]
  },
  "setup": [
    "Card id = suit*9 + (rank-6), so suit(id) = floor(id/9) and rank(id) = id mod 9 + 6. Suits are 0 Clubs, 1 Diamonds, 2 Hearts, 3 Spades.",
    "Set deck to the ordered list 0..35 and shuffle it once with the engine's seeded shuffle. This is the only random operation in the game.",
    "Shuffled positions 1-8 go to seat 1's hand and positions 9-16 go to seat 2's hand, each sorted ascending. Positions 17-36 go to set_aside, sorted ascending. hand_size is 8 for each seat.",
    "Sync: each seat is told only its own hand. Tell both seats that each player holds 8 cards.",
    "Ask seat 2 to name two different suits as the offer, as a choice among the 6 suit pairs. If the answer is missing or illegal, offer = [2, 3] (Hearts and Spades).",
    "Ask seat 1 to pick one suit from offer as trump. If the answer is missing or illegal, trump = the offered suit with the lower index.",
    "Announce the trump. attacker = the seat holding the lowest-rank trump, which is the smallest id between trump*9 and trump*9+8 found in either hand. If neither hand holds a trump, attacker = 2."
  ],
  "round": [
    {"action": "update", "who": "table", "answer": null, "effect": "Reset for the bout: table_cards = [], attack_card = -1, throw_card = -1, defender_took = false."},
    {"action": "ask", "who": "the attacker (seat = attacker)", "answer": "one card id from the attacker's hand", "effect": "attack_card = the chosen id. Remove it from the attacker's hand, append it to table_cards and decrease the attacker's hand_size by 1. If the answer is missing or illegal, play the card minimising (rank, suit), that is the lowest rank with ties broken by lower suit index."},
    {"action": "ask", "who": "the defender (seat = 3 - attacker)", "answer": "TAKE, or a card id from the defender's hand that beats attack_card", "effect": "If a card is chosen, remove it from the defender's hand, append it to table_cards and decrease the defender's hand_size by 1. If TAKE is chosen, or the answer is missing or illegal, defender_took = true. X beats Y when (suit(X) = suit(Y) and rank(X) > rank(Y)) or (suit(X) = trump and suit(Y) != trump)."},
    {"action": "ask", "who": "the attacker", "answer": "PASS, or a card id from the attacker's hand whose rank equals the rank of a card in table_cards", "effect": "If a card is chosen, throw_card = that id. Remove it from the attacker's hand, append it to table_cards and decrease the attacker's hand_size by 1. A missing or illegal answer counts as PASS. Only PASS is offered when defender_took = false and the defender's hand_size = 0."},
    {"action": "ask", "who": "the defender, when throw_card != -1 and defender_took = false", "answer": "TAKE, or a card id from the defender's hand that beats throw_card", "effect": "If a card is chosen, remove it from the defender's hand, append it to table_cards and decrease the defender's hand_size by 1. If TAKE is chosen, or the answer is missing or illegal, defender_took = true."},
    {"action": "update", "who": "table", "answer": null, "effect": "If defender_took: add every card in table_cards to the defender's hand (re-sorted ascending), add len(table_cards) to the defender's hand_size, and leave attacker unchanged. Otherwise: add table_cards to discard (re-sorted ascending) and set attacker = 3 - attacker. In both cases bout += 1."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce table_cards in play order, the result (taken or beaten off), and both hand_size values."},
    {"action": "check", "who": "table", "answer": null, "effect": "End the game if any seat has hand_size = 0, or if bout = 39 (round 40 done). Otherwise continue."}
  ],
  "ending": {
    "condition": "any player's hand_size = 0, or bout = 39",
    "rank_by": "0 - you.hand_size",
    "decided_by": "Fewer cards in hand ranks higher. If exactly one player has 0 cards after a bout, that player wins. If both reach 0 together, they tie and share the result (a draw). After round 40 the player with fewer cards wins, and equal counts are a draw (shared)."
  },
  "rules": [
    {"id": "R1", "text": "When a card has id n, then its suit is floor(n/9) and its rank is n mod 9 + 6, with ids 0 to 35."},
    {"id": "R2", "text": "When the game starts, then the deck 0..35 is shuffled once with the seeded shuffle, seat 1 gets positions 1-8, seat 2 gets positions 9-16, and positions 17-36 (20 cards) go to set_aside, all sorted ascending."},
    {"id": "R3", "text": "When the deal is done, then each seat sees only its own hand, both are told each holds 8 cards, and set_aside is never drawn from."},
    {"id": "R4", "text": "When seat 2 makes the offer, then it names two different suits; if the answer is missing or illegal, the offer is Hearts (2) and Spades (3)."},
    {"id": "R5", "text": "When seat 1 picks trump, then trump is one of the two offered suits; if the answer is missing or illegal, trump is the offered suit with the lower index."},
    {"id": "R6", "text": "When trump is set, then the first attacker is the seat holding the lowest-rank trump; if neither seat holds a trump, seat 2 attacks first."},
    {"id": "R7", "text": "When card X is compared with card Y, then X beats Y if they share a suit and X has the higher rank, or if X is a trump and Y is not."},
    {"id": "R8", "text": "When the attacker attacks, then they play one card from their hand; if the answer is missing or illegal, they play their lowest-rank card, with ties broken by lower suit index."},
    {"id": "R9", "text": "When the defender answers the attack, then they play a card that beats it or say TAKE; a missing or illegal answer is TAKE."},
    {"id": "R10", "text": "When the attacker may throw in, then they add one card whose rank matches the rank of a card on the table, or PASS; a missing or illegal answer is PASS; at most 1 card is thrown in per bout."},
    {"id": "R11", "text": "When the defender has not said TAKE and has 0 cards in hand, then the attacker may not throw in."},
    {"id": "R12", "text": "When a card is thrown in after the defender said TAKE, then the defender takes that card too."},
    {"id": "R13", "text": "When a card was thrown in and the defender has not said TAKE, then the defender beats it or says TAKE; a missing or illegal answer is TAKE."},
    {"id": "R14", "text": "When the defender said TAKE at any point in a bout, then all table cards go into the defender's hand and the same attacker attacks next bout."},
    {"id": "R15", "text": "When the defender beat every card in a bout, then all table cards go to discard and the defender becomes the attacker."},
    {"id": "R16", "text": "When a bout ends, then the played cards in order, the result and both hand sizes are announced."},
    {"id": "R17", "text": "When exactly one seat has 0 cards after a bout's resolution, then that seat wins."},
    {"id": "R18", "text": "When both seats have 0 cards after a bout's resolution, then the game is a draw."},
    {"id": "R19", "text": "When bout 39 (round 40) ends with both seats holding cards, then the seat with fewer cards wins, and equal counts are a draw."}
  ],
  "offers": [
    {"question": "Offer (setup)", "who": "seat 2", "options": "the 6 pairs of different suits: {0,1}, {0,2}, {0,3}, {1,2}, {1,3}, {2,3}"},
    {"question": "Trump choice (setup)", "who": "seat 1", "options": "the two suits in offer"},
    {"question": "Attack", "who": "the attacker", "options": "every card id in the attacker's hand"},
    {"question": "Defence 1", "who": "the defender", "options": "TAKE, plus every card in the defender's hand that beats attack_card"},
    {"question": "Throw-in", "who": "the attacker", "options": "PASS, plus every card in the attacker's hand whose rank equals the rank of a table card; only PASS when defender_took is false and the defender's hand_size is 0"},
    {"question": "Defence 2 (only if a card was thrown in and the defender has not taken)", "who": "the defender", "options": "TAKE, plus every card in the defender's hand that beats throw_card"}
  ],
  "choices": [
    {"what": "2 players, suggested 2", "why": "The designer fixed the table at 2. This is a head-to-head duel of card management, where a thoughtful player saves trumps, chooses the trump offer to fit their own hand, and throws in to unload cards."},
    {"what": "No talk step", "why": "The source has no talk, and in a two-player zero-sum duel talk adds nothing to reason about."},
    {"what": "Draw expressed as a shared top rank", "why": "rank_by = -hand_size makes both seats level when both have 0 cards or equal counts, and the engine treats a level top as shared, which is the draw."},
    {"what": "The bout counter ends the game at 39 bouts", "why": "Rounds 2 to 40 are 39 bouts."}
  ],
  "simplifications": [
    {"what": "The source's round 1 is modelled as setup steps", "why": "It runs once before the bouts."},
    {"what": "Dynamic attacker and defender are named by the attacker attribute", "why": "The engine addresses seats, so the roles are read from a table number."}
  ],
  "unsupported": []
}
```
````
