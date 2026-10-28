# 16 spec

- time: 2026-10-28T02:01:05+00:00 (49.8s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 77c9a2b2441d57ac, reply sha256 1bf4dd91786ced05

## Sent

````
Game: Greek Hold 'em Mini II
Players in the source: 3 to 3
Suggested table size, chosen by the designer of these rules (keep it): 3

Rules, as filed in the inventory:
SETUP. Three players, numbered 1, 2 and 3. Each starts with a chip total of 0. Totals may go negative and may include fractions from split pots. The deck has 18 cards: ranks 1, 2, 3, 4, 5 and 6, three copies of each, with no suits. The game lasts exactly 36 hands. In hand h, the FIRST ACTOR is player ((h - 1) mod 3) + 1. The SECOND ACTOR is the next player after the first actor (wrapping from 3 to 1), and the THIRD ACTOR is the remaining player.

EACH HAND:
1. Deal. Shuffle all 18 cards; this is the only random event of the hand. Deal 2 hole cards face down to each player and 4 board cards face down to the table. Each player sees only their own hole cards.
2. Ante. Each player pays 1 chip into the pot. The pot starts at 3.
3. Board. Board cards 1, 2 and 3 are turned face up for everyone. Board card 4 stays face down.
4. First actor's choice: CHECK, BET 2 or BET 4. A bet is paid into the pot at once, and the choice is announced to all.
5. Second actor's choice, announced to all. If nobody has bet yet, the choices are CHECK, BET 2 or BET 4. If a bet has been made, the choices are CALL (pay the same amount as the bet into the pot) or FOLD (leave the hand, losing everything already paid).
6. Third actor's choice, with the same options as the second actor, announced to all.
7. Response. This step happens only if a bet was made after at least one player checked. Each player who checked before the bet chooses, at the same moment, CALL (pay the bet amount) or FOLD. The choices are then revealed. Only one bet is ever made in a hand: there are no raises, and the bettor never acts again.
8. Final board. Board card 4 is turned face up.
9. Hand scores. Each player's score is computed from their hole cards (ranks a and b) and the 4 board cards. Score = a + b, plus 6 if a equals b, plus 4 for each match. A match is a board card whose rank equals a or b. At most 3 matches count, because a hand may use only three board cards.
10. Showdown. The players still in the hand are those who did not fold. If exactly one player is still in, that player takes the whole pot and no hole cards are revealed. If two or three are still in, their hole cards and scores are revealed, and the pot goes to the highest score among them. Players tied for the highest score split the pot equally. If everyone checked, all three go to showdown.
11. Folded players' hole cards are never revealed.
12. Totals. Each player's total changes by the chips they won minus the chips they paid this hand. All three totals are announced.
13. All cards return to the deck for the next shuffle.

The sum of all totals is always 0.

END. After hand 36 the game ends.

How the winner is decided: After 36 hands, the player with the highest chip total wins. If two or three players share the highest total, the game is a draw among them.
````

## Reply

````
```json
{
  "name": "Greek Hold 'em Mini II",
  "summary": "Three players play 36 hands of a tiny one-bet poker with an 18-card suitless deck; the highest net chip total after hand 36 wins.",
  "players": {"min": 3, "max": 3, "suggested": 3},
  "parameters": {
    "num_players": 3,
    "ranks": 6,
    "copies_per_rank": 3,
    "deck_size": 18,
    "hands": 36,
    "hole_cards": 2,
    "board_cards": 4,
    "board_face_up_before_betting": 3,
    "ante": 1,
    "starting_pot": 3,
    "bet_small": 2,
    "bet_large": 4,
    "pair_bonus": 6,
    "match_bonus": 4,
    "max_matches": 3,
    "starting_total": 0
  },
  "attributes": {
    "player": [
      {"key": "total", "type": "number", "visible": "public", "initial": 0, "meaning": "Net chip total across all hands. It may be negative or fractional.", "observable": true},
      {"key": "hole", "type": "list", "visible": "ally", "initial": [], "meaning": "The player's 2 hole cards for this hand. Only the owner sees them.", "observable": false},
      {"key": "revealed_hole", "type": "list", "visible": "public", "initial": [], "meaning": "Hole cards shown at a showdown with 2 or more players. Empty otherwise.", "observable": true},
      {"key": "hand_score", "type": "number", "visible": "ally", "initial": 0, "meaning": "This hand's score: a+b, plus 6 if a pair, plus 4 per matching board card, with at most 3 matches.", "observable": false},
      {"key": "revealed_score", "type": "number", "visible": "public", "initial": 0, "meaning": "hand_score, published at a showdown for players still in. 0 otherwise.", "observable": true},
      {"key": "action", "type": "text", "visible": "public", "initial": "", "meaning": "The player's last announced action this hand: CHECK, BET, CALL or FOLD.", "observable": true},
      {"key": "folded", "type": "bool", "visible": "public", "initial": false, "meaning": "Whether the player has folded this hand.", "observable": true},
      {"key": "paid", "type": "number", "visible": "public", "initial": 0, "meaning": "Chips paid into the pot this hand.", "observable": false},
      {"key": "won", "type": "number", "visible": "public", "initial": 0, "meaning": "Chips won from the pot this hand.", "observable": false}
    ],
    "game": [
      {"key": "deck", "type": "list", "visible": "none", "initial": [1,1,1,2,2,2,3,3,3,4,4,4,5,5,5,6,6,6], "meaning": "The undealt cards.", "observable": false},
      {"key": "board_up", "type": "list", "visible": "public", "initial": [], "meaning": "Face-up board cards: 3 during betting, 4 after the final board.", "observable": true},
      {"key": "board_hidden", "type": "list", "visible": "none", "initial": [], "meaning": "Board card 4 while it is still face down.", "observable": false},
      {"key": "pot", "type": "number", "visible": "public", "initial": 0, "meaning": "Chips in the pot this hand.", "observable": true},
      {"key": "hand", "type": "number", "visible": "public", "initial": 0, "meaning": "The current hand number, from 1 to 36.", "observable": true},
      {"key": "first_actor", "type": "number", "visible": "public", "initial": 1, "meaning": "Seat ((hand-1) mod 3)+1.", "observable": false},
      {"key": "second_actor", "type": "number", "visible": "public", "initial": 2, "meaning": "The seat after the first actor, wrapping from 3 to 1.", "observable": false},
      {"key": "third_actor", "type": "number", "visible": "public", "initial": 3, "meaning": "The remaining seat.", "observable": false},
      {"key": "bet_amount", "type": "number", "visible": "public", "initial": 0, "meaning": "The size of this hand's single bet (2 or 4). 0 if nobody has bet.", "observable": true},
      {"key": "in_count", "type": "number", "visible": "public", "initial": 0, "meaning": "The number of players who have not folded.", "observable": false},
      {"key": "best_score", "type": "number", "visible": "public", "initial": 0, "meaning": "The highest hand_score among players still in.", "observable": false},
      {"key": "winner_count", "type": "number", "visible": "public", "initial": 0, "meaning": "The number of players still in who hold best_score.", "observable": false}
    ]
  },
  "setup": [
    "Seats 1, 2 and 3 each start with a total of 0.",
    "The table's deck holds 18 cards: ranks 1 to 6, three copies of each, with no suits.",
    "The hand counter starts at 0. The game lasts exactly 36 hands."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "Increment hand by 1. Set first_actor = ((hand-1) mod 3)+1, second_actor = (first_actor mod 3)+1, and third_actor = (second_actor mod 3)+1. Return all cards to deck, so it again holds the 18 cards. For every player: clear hole and revealed_hole, set hand_score and revealed_score to 0, set action to empty, set folded to false, and set paid and won to 0. Clear board_up and board_hidden. Set bet_amount to 0."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Deal: draw 2 random cards from deck into each player's hole. Draw 3 random cards from deck into board_up and 1 into board_hidden."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Ante: each player's paid += 1, so pot = 3."},
    {"action": "sync", "who": "all players", "answer": null, "effect": "Each player sees their own hole, the 3 cards of board_up, the pot, the hand number and who acts first, second and third."},
    {"action": "ask", "who": "the first actor (seat first_actor)", "answer": "one of CHECK, BET 2, BET 4", "effect": "On CHECK: action = CHECK. On BET x: action = BET, bet_amount = x, paid += x, pot += x. The choice is announced to all."},
    {"action": "ask", "who": "the second actor (seat second_actor)", "answer": "if bet_amount = 0: CHECK, BET 2 or BET 4; if bet_amount > 0: CALL or FOLD", "effect": "On CHECK: action = CHECK. On BET x: action = BET, bet_amount = x, paid += x, pot += x. On CALL: action = CALL, paid += bet_amount, pot += bet_amount. On FOLD: action = FOLD, folded = true. The choice is announced to all."},
    {"action": "ask", "who": "the third actor (seat third_actor)", "answer": "if bet_amount = 0: CHECK, BET 2 or BET 4; if bet_amount > 0: CALL or FOLD", "effect": "Same effects as the second actor's step. The choice is announced to all."},
    {"action": "poll", "who": "every player whose action = CHECK, only when bet_amount > 0 (these players checked before the bet)", "answer": "CALL or FOLD", "effect": "Answers are collected simultaneously, then revealed. On CALL: action = CALL, paid += bet_amount, pot += bet_amount. On FOLD: action = FOLD, folded = true."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Final board: move the card in board_hidden into board_up, so board_up holds 4 cards."},
    {"action": "update", "who": "all players", "answer": null, "effect": "For each player with hole ranks a and b: matches = the number of cards in board_up whose rank equals a or b. hand_score = a + b + (6 if a = b else 0) + 4 * min(3, matches)."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Set in_count = the number of players with folded = false. If in_count = 1, the unfolded player gets won = pot. If in_count >= 2: for each unfolded player, revealed_hole = hole and revealed_score = hand_score; best_score = the maximum hand_score among unfolded players; winner_count = the number of unfolded players with hand_score = best_score; each such player gets won = pot / winner_count. Folded players' hole cards are never revealed."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Totals: each player's total += won - paid. All three totals, the showdown result and the pot split are announced."},
    {"action": "check", "who": "all players", "answer": null, "effect": "If hand >= 36, end the game. Otherwise play the next hand."}
  ],
  "ending": {
    "condition": "hand >= 36",
    "rank_by": "you.total",
    "decided_by": "Each player's standing is their net chip total after 36 hands. The highest total wins, and players tied at the top share the win (the source calls this a draw)."
  },
  "rules": [
    {"id": "R1", "text": "When a hand begins, then the deck holds all 18 cards (ranks 1-6, three of each), each player receives 2 hole cards and the board receives 4 cards, all drawn at random."},
    {"id": "R2", "text": "When a hand begins, then each player pays an ante of 1 and the pot is 3."},
    {"id": "R3", "text": "When betting starts, then 3 board cards are face up and board card 4 is hidden from everyone."},
    {"id": "R4", "text": "When it is hand h, then the first actor is seat ((h-1) mod 3)+1, the second actor is the next seat (wrapping from 3 to 1), and the third actor is the remaining seat."},
    {"id": "R5", "text": "When no bet has been made and a player acts, then they may CHECK, BET 2 or BET 4, and a bet adds that amount to their paid and to the pot."},
    {"id": "R6", "text": "When a bet has been made and a later actor acts, then they may only CALL (pay the bet amount into the pot) or FOLD."},
    {"id": "R7", "text": "When a bet is made after one or more players checked, then those checkers choose CALL or FOLD simultaneously, and the choices are revealed afterwards."},
    {"id": "R8", "text": "When a hand has a bet, then there is exactly one bet: there are no raises and the bettor never acts again."},
    {"id": "R9", "text": "When a player folds, then they leave the hand, forfeit everything they paid, and their hole cards are never revealed."},
    {"id": "R10", "text": "When betting ends, then board card 4 is turned face up."},
    {"id": "R11", "text": "When hole cards are ranks a and b, then the hand score is a + b, plus 6 if a = b, plus 4 for each board card whose rank equals a or b, counting at most 3 matches."},
    {"id": "R12", "text": "When exactly one player has not folded, then that player takes the whole pot and no hole cards are revealed."},
    {"id": "R13", "text": "When two or three players have not folded, then their hole cards and scores are revealed and the highest score takes the pot."},
    {"id": "R14", "text": "When players at showdown tie for the highest score, then they split the pot equally, which may give fractional totals."},
    {"id": "R15", "text": "When all three players check, then all three go to showdown with a pot of 3."},
    {"id": "R16", "text": "When a hand ends, then each player's total changes by the chips won minus the chips paid, all three totals are announced, and the totals sum to 0."},
    {"id": "R17", "text": "When hand 36 ends, then the game ends and the highest total wins, with tied leaders sharing the win."}
  ],
  "offers": [
    {"question": "First actor's choice", "who": "seat first_actor", "options": "CHECK, BET 2, BET 4"},
    {"question": "Second actor's choice", "who": "seat second_actor", "options": "if bet_amount = 0: CHECK, BET 2, BET 4; if bet_amount > 0: CALL, FOLD"},
    {"question": "Third actor's choice", "who": "seat third_actor", "options": "if bet_amount = 0: CHECK, BET 2, BET 4; if bet_amount > 0: CALL, FOLD"},
    {"question": "Response to a bet made after a check", "who": "every seat whose action is CHECK while bet_amount > 0; other seats are not asked", "options": "CALL, FOLD"}
  ],
  "choices": [
    {"what": "3 players (min = max = suggested = 3)", "why": "The designer fixes the game at three seats. The actor rotation, the response step and the split pots all assume exactly three players. With three, bluffing works because a bet must get past two opponents, one of whom may hold the third copy of a rank."},
    {"what": "No pre-choice talk step", "why": "The source has no table talk. The information in play is the actions themselves (check, bet size, call or fold), so adding talk would add a mechanic."},
    {"what": "Responders are identified by action = CHECK while bet_amount > 0", "why": "Anyone still showing CHECK once a bet exists must have checked before the bet. Since only one bet is possible, this matches 'each player who checked before the bet'."},
    {"what": "Score computed for everyone, but published only at a showdown with 2 or more players", "why": "This keeps the arithmetic uniform while honoring the rule that folded hands and uncontested winners' hands are never revealed."},
    {"what": "Strategy at this table", "why": "A thoughtful player weighs the visible board against their hole cards, bets 4 with strong pairs or matches, uses bet size and position to bluff, and reads opponents' checks and calls over 36 hands. A thoughtless player calls or bets blindly."}
  ],
  "simplifications": [
    {"what": "Ante, bets and calls are tracked in `paid`, and the net change is applied to `total` at the end of the hand", "why": "This is arithmetically the same as paying at once, and it keeps fractional split pots exact."}
  ],
  "unsupported": []
}
```
````
