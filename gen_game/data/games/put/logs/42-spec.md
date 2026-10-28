# 42 spec

- time: 2026-10-28T06:56:15+00:00 (42.4s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 3ef1f93860d34028, reply sha256 f2f290c4dcd8defa

## Sent

````
Game: Put: Sixteen Hands
Players in the source: 2 to 2
Suggested table size, chosen by the designer of these rules (keep it): 2

Rules, as filed in the inventory:
CARDS. Use a deck of 52 cards made of four copies of each value from 1 to 13. Value 13 is a Three (highest), 12 a Two, 11 an Ace, 10 a King, 9 a Queen, 8 a Jack, 7 a Ten, 6 a Nine, 5 an Eight, 4 a Seven, 3 a Six, 2 a Five and 1 a Four (lowest). There are no suits. In any trick the higher value wins, and equal values tie the trick, which then belongs to no one.

SETUP. Both players start with a score of 0. The match is exactly 16 hands. Seat 1 leads in odd-numbered hands and seat 2 leads in even-numbered hands. The other seat is the responder.

EACH HAND, in this order:
1. Reset. Restore and shuffle the full 52-card deck. Clear each player's hand, played card, call, response and trick count, and clear the stake and the folded marker.
2. Deal. Deal 3 cards to each player. Each player sees only their own cards.
3. Lead (leader's choice). The leader chooses one of their 3 cards and plays it face up.
4. Announce the lead to both players.
5. Answer (responder's choice). Having seen the lead, the responder chooses one of their 3 cards and plays it face up.
6. Trick 1. Compare the two cards; the higher wins trick 1 and an equal pair is a tie. Announce the result.
7. Put window (both players at the same moment). Each player privately chooses Put or Check, without seeing the other's choice.
8. Announce both calls.
9. Reply. This step happens only if exactly one player chose Put. The player who chose Check now chooses See or Fold. If both chose Put, the Put counts as seen. If both chose Check, there is no Put. The stake for the hand is 4 if a Put was seen (by See or by both Putting), 1 if both Checked.
10. Fold. If a player folded, the player who Put scores 1 point and the hand ends there; skip to step 15. The remaining cards are not shown.
11. Trick 2. Each player automatically plays the higher of their two remaining cards. Compare them as in trick 1.
12. Trick 3. Each player automatically plays their last card. Compare them as in trick 1.
13. Reveal. Show all cards and each player's number of tricks won.
14. Hand scoring. A player who won at least 2 of the 3 tricks scores the stake (1 or 4). If neither player won 2 tricks, because of tied tricks, no one scores.
15. End check. After hand 16 the match ends; otherwise the next hand begins.

There is no talk phase.

How the winner is decided: After 16 hands, the player with the higher total score wins. If the totals are equal, the match is a draw.
````

## Reply

````
```json
{
  "name": "Put: Sixteen Hands",
  "summary": "A two-player trick-taking bluffing duel over 16 hands. After the first trick, each player may secretly call Put to raise the stake from 1 to 4, and a lone Put can be seen or folded to.",
  "players": {"min": 2, "max": 2, "suggested": 2},
  "parameters": {
    "deck_size": 52,
    "copies_per_value": 4,
    "lowest_value": 1,
    "highest_value": 13,
    "hands": 16,
    "cards_dealt_per_player": 3,
    "tricks_per_hand": 3,
    "tricks_needed_to_win_hand": 2,
    "stake_put_seen": 4,
    "stake_both_checked": 1,
    "fold_points": 1,
    "starting_score": 0
  },
  "attributes": {
    "player": [
      {"key": "score", "type": "number", "visible": "public", "initial": 0, "meaning": "Total points over the match", "observable": true},
      {"key": "hand", "type": "list", "visible": "ally", "initial": [], "meaning": "The player's unplayed cards, as values 1-13", "observable": false},
      {"key": "card1", "type": "number", "visible": "public", "initial": 0, "meaning": "Card played face up to trick 1 (0 = none yet)", "observable": false},
      {"key": "card2", "type": "number", "visible": "public", "initial": 0, "meaning": "Card auto-played to trick 2, the higher of the two remaining", "observable": false},
      {"key": "card3", "type": "number", "visible": "public", "initial": 0, "meaning": "Card auto-played to trick 3, the last card", "observable": false},
      {"key": "call", "type": "text", "visible": "public", "initial": "", "meaning": "Put or Check, chosen secretly in the put window and announced after", "observable": false},
      {"key": "response", "type": "text", "visible": "public", "initial": "", "meaning": "See or Fold, given only by the lone Checker when exactly one player Put", "observable": false},
      {"key": "tricks", "type": "number", "visible": "public", "initial": 0, "meaning": "Tricks won this hand", "observable": true}
    ],
    "game": [
      {"key": "deck", "type": "list", "visible": "none", "initial": [], "meaning": "The undealt cards: four copies of each value 1-13", "observable": false},
      {"key": "hand_number", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of the current hand, 1 to 16", "observable": true},
      {"key": "leader", "type": "number", "visible": "public", "initial": 1, "meaning": "Seat that leads this hand: 1 in odd hands, 2 in even hands", "observable": false},
      {"key": "stake", "type": "number", "visible": "public", "initial": 0, "meaning": "Points the hand is worth: 4 if a Put was seen, 1 if both Checked", "observable": false},
      {"key": "folded", "type": "bool", "visible": "public", "initial": false, "meaning": "True if the lone Checker folded this hand", "observable": false}
    ]
  },
  "setup": [
    "Both players' score is set to 0.",
    "hand_number is set to 0.",
    "The match will last exactly 16 hands."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "Reset step. hand_number += 1. leader = 1 if hand_number is odd, else 2. deck = four copies of each value 1..13 (52 cards). Each player's hand, card1, card2 and card3 are cleared to empty or 0, call and response to empty text, and tricks to 0. stake = 0 and folded = false."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Deal step. Each player draws 3 cards at random: each card is removed from deck and appended to that player's hand."},
    {"action": "sync", "who": "all players", "answer": null, "effect": "Each player privately sees their own hand."},
    {"action": "ask", "who": "the leader (seat given by leader)", "answer": "one card value from their hand", "effect": "Lead step. leader.card1 = the chosen value; one copy of that value is removed from leader.hand."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce: 'Hand {hand_number}: Seat {leader} leads {card1}.'"},
    {"action": "ask", "who": "the responder (the seat that is not leader)", "answer": "one card value from their hand", "effect": "Answer step. responder.card1 = the chosen value; one copy of that value is removed from responder.hand."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Trick 1. If seat1.card1 > seat2.card1, seat1.tricks += 1. If seat2.card1 > seat1.card1, seat2.tricks += 1. If the cards are equal, the trick is a tie and no one's tricks change. The result is announced."},
    {"action": "poll", "who": "all players", "answer": "Put or Check", "effect": "Put window. Each player's call is set to their answer. Neither player sees the other's call until both have answered."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce: 'Seat 1 calls {seat1.call}; Seat 2 calls {seat2.call}.'"},
    {"action": "ask", "who": "the player whose call is Check, only when exactly one player's call is Put", "answer": "See or Fold", "effect": "Reply step. That player's response is set to the answer. When both called Put or both called Check, this step is skipped."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Stake step. If both calls are Put, or one call is Put and the Checker's response is See, then stake = 4. If both calls are Check, then stake = 1. If the Checker's response is Fold, then folded = true."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Fold scoring, only when folded is true. The player whose call is Put gets score += 1. The remaining cards are not shown."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Trick 2, only when folded is false. Each player's card2 = the maximum value in their hand, and that card is removed from hand. Compare card2: the higher card gives its owner tricks += 1; equal cards are a tie."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Trick 3, only when folded is false. Each player's card3 = their last card in hand, and hand becomes empty. Compare card3: the higher card gives its owner tricks += 1; equal cards are a tie."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Reveal, only when folded is false. Announce each seat's card1, card2 and card3 and each seat's tricks."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Hand scoring, only when folded is false. A player with tricks >= 2 gets score += stake. If neither player has tricks >= 2, no one scores."},
    {"action": "check", "who": "all players", "answer": null, "effect": "End check. If hand_number >= 16, end the match; otherwise the next hand begins."}
  ],
  "ending": {
    "condition": "hand_number >= 16",
    "rank_by": "you.score",
    "decided_by": "After 16 hands, the player with the higher total score wins. Equal totals share the win, which is a draw."
  },
  "rules": [
    {"id": "R1", "text": "When a hand begins, then the deck is restored to 52 cards, four copies of each value 1 to 13, and each player's hand, played cards, call, response and tricks are cleared, along with stake and folded."},
    {"id": "R2", "text": "When cards are dealt, then each player receives 3 cards drawn from the deck, and each player sees only their own cards."},
    {"id": "R3", "text": "When hand_number is odd, then seat 1 leads; when hand_number is even, then seat 2 leads."},
    {"id": "R4", "text": "When the leader leads, then they play one card from their own hand face up, and it is announced before the responder plays."},
    {"id": "R5", "text": "When the responder answers, then they play one card from their own hand face up, having seen the lead."},
    {"id": "R6", "text": "When a trick is compared, then the higher value wins the trick and adds 1 to its owner's tricks; when the values are equal, then the trick is a tie and no one's tricks change."},
    {"id": "R7", "text": "When the put window opens, then both players choose Put or Check simultaneously, without seeing the other's choice, and both calls are then announced."},
    {"id": "R8", "text": "When exactly one player calls Put, then the player who called Check chooses See or Fold."},
    {"id": "R9", "text": "When both players call Put, or one calls Put and the other Sees, then stake = 4."},
    {"id": "R10", "text": "When both players call Check, then there is no Put, no reply is asked, and stake = 1."},
    {"id": "R11", "text": "When the Checker folds, then the player who called Put scores 1 point, no further tricks are played, and the remaining cards are not shown."},
    {"id": "R12", "text": "When no one folded, then in trick 2 each player automatically plays the higher of their two remaining cards."},
    {"id": "R13", "text": "When no one folded, then in trick 3 each player automatically plays their last card."},
    {"id": "R14", "text": "When no one folded, then after trick 3 all cards and each player's tricks are revealed."},
    {"id": "R15", "text": "When no one folded and a player has won at least 2 of the 3 tricks, then that player's score increases by the stake, 1 or 4."},
    {"id": "R16", "text": "When no one folded and neither player has won 2 tricks because of tied tricks, then no one scores that hand."},
    {"id": "R17", "text": "When hand 16 has been scored, then the match ends, and the higher total score wins; equal totals are a draw."}
  ],
  "offers": [
    {"question": "Lead: which card to play", "who": "the leader (seat 1 in odd hands, seat 2 in even hands)", "options": "each distinct card value in the leader's 3-card hand"},
    {"question": "Answer: which card to play", "who": "the responder (the non-leader)", "options": "each distinct card value in the responder's 3-card hand"},
    {"question": "Put window", "who": "both seats, simultaneously", "options": "Put, Check"},
    {"question": "Reply to a lone Put", "who": "only the seat that called Check, and only when the other seat called Put", "options": "See, Fold"}
  ],
  "choices": [
    {"what": "Exactly 2 players, suggested 2", "why": "The designer fixed the table at 2. The game is a heads-up duel: three tricks between two hands and a Put that one opponent sees or folds to. It has no meaning at another size. The strategy is reading the opponent's lead and answer from trick 1, putting to bluff or value-bet, and folding a weak hand for a 1-point loss rather than risking 4."},
    {"what": "No talk phase", "why": "The source says there is no talk phase."},
    {"what": "Cards are stored as numbers 1-13 rather than named ranks", "why": "Arithmetic comparison needs numbers; the rank names map one to one (13 = Three, highest, down to 1 = Four, lowest), so nothing is lost."},
    {"what": "Played cards and calls are public attributes", "why": "The rules play them face up or announce them."},
    {"what": "The fold scores the fixed 1 point (fold_points), not the stake", "why": "The source says the Putter scores 1 point when the other folds."}
  ],
  "simplifications": [
    {"what": "Steps that apply only in some situations (reply, fold scoring, tricks 2 and 3, reveal, hand scoring) are single steps, each carrying its own arithmetic condition", "why": "The step list is flat. Each skipped step depends on one simple condition (folded, or exactly one Put), so no block of steps has to be chosen instead of another."}
  ],
  "unsupported": []
}
```
````
