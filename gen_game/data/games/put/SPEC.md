# Put: Sixteen Hands

A two-player trick-taking bluffing duel over 16 hands. After the first trick, each player may secretly call Put to raise the stake from 1 to 4, and a lone Put can be seen or folded to.

Players: 2 to 2, best with 2

## Parameters

- `deck_size` = 52
- `copies_per_value` = 4
- `lowest_value` = 1
- `highest_value` = 13
- `hands` = 16
- `cards_dealt_per_player` = 3
- `tricks_per_hand` = 3
- `tricks_needed_to_win_hand` = 2
- `stake_put_seen` = 4
- `stake_both_checked` = 1
- `fold_points` = 1
- `starting_score` = 0

## Round

1. **update** (all players): Reset step. hand_number += 1. leader = 1 if hand_number is odd, else 2. deck = four copies of each value 1..13 (52 cards). Each player's hand, card1, card2 and card3 are cleared to empty or 0, call and response to empty text, and tricks to 0. stake = 0 and folded = false.
2. **update** (all players): Deal step. Each player draws 3 cards at random: each card is removed from deck and appended to that player's hand.
3. **sync** (all players): Each player privately sees their own hand.
4. **ask** (the leader (seat given by leader)): Lead step. leader.card1 = the chosen value; one copy of that value is removed from leader.hand.
5. **tell** (all players): Announce: 'Hand {hand_number}: Seat {leader} leads {card1}.'
6. **ask** (the responder (the seat that is not leader)): Answer step. responder.card1 = the chosen value; one copy of that value is removed from responder.hand.
7. **update** (all players): Trick 1. If seat1.card1 > seat2.card1, seat1.tricks += 1. If seat2.card1 > seat1.card1, seat2.tricks += 1. If the cards are equal, the trick is a tie and no one's tricks change. The result is announced.
8. **poll** (all players): Put window. Each player's call is set to their answer. Neither player sees the other's call until both have answered.
9. **tell** (all players): Announce: 'Seat 1 calls {seat1.call}; Seat 2 calls {seat2.call}.'
10. **ask** (the player whose call is Check, only when exactly one player's call is Put): Reply step. That player's response is set to the answer. When both called Put or both called Check, this step is skipped.
11. **update** (all players): Stake step. If both calls are Put, or one call is Put and the Checker's response is See, then stake = 4. If both calls are Check, then stake = 1. If the Checker's response is Fold, then folded = true.
12. **update** (all players): Fold scoring, only when folded is true. The player whose call is Put gets score += 1. The remaining cards are not shown.
13. **update** (all players): Trick 2, only when folded is false. Each player's card2 = the maximum value in their hand, and that card is removed from hand. Compare card2: the higher card gives its owner tricks += 1; equal cards are a tie.
14. **update** (all players): Trick 3, only when folded is false. Each player's card3 = their last card in hand, and hand becomes empty. Compare card3: the higher card gives its owner tricks += 1; equal cards are a tie.
15. **tell** (all players): Reveal, only when folded is false. Announce each seat's card1, card2 and card3 and each seat's tricks.
16. **update** (all players): Hand scoring, only when folded is false. A player with tricks >= 2 gets score += stake. If neither player has tricks >= 2, no one scores.
17. **check** (all players): End check. If hand_number >= 16, end the match; otherwise the next hand begins.

## Ending

- ends when: hand_number >= 16
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: After 16 hands, the player with the higher total score wins. Equal totals share the win, which is a draw.

## Choices the source did not make

- Exactly 2 players, suggested 2: The designer fixed the table at 2. The game is a heads-up duel: three tricks between two hands and a Put that one opponent sees or folds to. It has no meaning at another size. The strategy is reading the opponent's lead and answer from trick 1, putting to bluff or value-bet, and folding a weak hand for a 1-point loss rather than risking 4.
- No talk phase: The source says there is no talk phase.
- Cards are stored as numbers 1-13 rather than named ranks: Arithmetic comparison needs numbers; the rank names map one to one (13 = Three, highest, down to 1 = Four, lowest), so nothing is lost.
- Played cards and calls are public attributes: The rules play them face up or announce them.
- The fold scores the fixed 1 point (fold_points), not the stake: The source says the Putter scores 1 point when the other folds.

## Simplifications

- Steps that apply only in some situations (reply, fold scoring, tricks 2 and 3, reveal, hand scoring) are single steps, each carrying its own arithmetic condition: The step list is flat. Each skipped step depends on one simple condition (folded, or exactly one Put), so no block of steps has to be chosen instead of another.

## Unsupported (needs engine work)

- none
