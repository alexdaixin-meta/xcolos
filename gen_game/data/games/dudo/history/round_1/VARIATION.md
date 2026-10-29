# Variation: Open-Table Dudo

This is Liar's Dice played one turn per round. Players raise a shared claim about the hidden dice, with ones wild, until someone calls Dudo. The wrong side loses a die, and the last player with dice wins. There is no turn cap, so no seat is a built-in hot seat.

Players: 2 to 4, best with 3

## Review of the original

Dudo (Liar's Dice) is a bluffing game for 2 to 10 players. Each player hides their own dice, and players in turn raise a public claim about how many dice on the table show a face, with ones wild. Anyone may challenge with 'Dudo' instead of raising, the wrong side loses a die, and the last player with dice wins. The previous adaptation, Four-Call Dudo, capped each hand at four bidding turns and auto-challenged a raise made on turn 4.

- **non_degenerate**: bad. This verdict is for the reviewed Four-Call variation. The fixed four-turn horizon creates a hot seat. The opener can always bid their own count and is never wrong. Turn 2 can creep by changing only the face, for example two 4s to two 5s, which is true about 98% of the time with 15 dice. Turn 3 is then squeezed, and turn 4 wins with probability at least max(p, 1-p). The thoughtless policy 'on turn 4 always raise by the smallest step' wins about 90% against naive play and never drops below about 50%. Turn 3 loses at least about 50% whatever it does. I also checked the suggested patch, in which turn 4 must call and raises need +1 quantity. By backward induction, turn 2 then has a nearly risk-free bid near the expected count minus one, and the loss lands on turns 3 and 4 (about 42% and 58%). Any fixed horizon puts the risk on fixed positions. The original Dudo, with unlimited wrap-around bidding, has no such seat.
- **skill_sensitive**: weak. In Four-Call, about half of each result came from seat position, which is fixed by who lost the previous hand. A strong player sitting at turn 3 still loses at least half the time. The original Dudo is strongly skill-sensitive: reading bids, using your own dice and timing a challenge all matter, and research on Liar's Dice shows large gaps between good and naive strategies.
- **headroom**: good. Estimating the count from your own dice plus what other players' bids reveal about their dice, choosing which face to bid, bluffing a face to mislead, and judging when a rival is stretching are all open-ended skills. A weak player who bids around the expected count still wins hands, so weak play is not hopeless.
- **reasoning_dependent**: good. Every player's dice are hidden. Each bid is a noisy and possibly deceptive signal about the bidder's dice. The decision to call or raise is a probabilistic inference that combines your own dice with what you can read into the bid history.
- **verifiable**: good. A challenge is settled by counting the dice showing the bid face plus ones and comparing with the bid quantity. Losing dice, elimination and the last survivor are all arithmetic.
- **fits_platform**: weak. Dudo is text-only and turn-based. The four-turn cap was introduced only to fit at most 4 choice steps into a round, and that cap is what broke balance. The original's unlimited bidding fits if one round is one turn instead of one hand. That keeps one choice step per round, but the game must then finish within 40 turns, so starting dice must be fewer.

## Problems

- P1: The fixed four-turn horizon makes the turn-3 or turn-4 position a structural hot seat. By backward induction, any fixed cap concentrates the loss on fixed positions, so seat order, not judgement, decides most hands.
- P2: Same-quantity, higher-face raises let early bidders creep with almost certainly true bids, so they carry no risk and make no real decision.
- P3: The auto-challenge after a turn-4 raise gives turn 4 the better of two options (at least max(p, 1-p)). This yields a thoughtless policy that wins about 90%: always raise minimally on turn 4.
- P4: Because the previous loser opens and positions are fixed relative to the opener, losses rotate nearly cyclically by seat. The winner is then largely set by the initial seating and the dice (the lottery trap).
- P5: If bidding is uncapped and starting dice are not reduced, a full game cannot reliably fit within 40 rounds.

## Changes

- Make one round equal one bidding turn, not one hand. A hand continues around the table, wrapping as often as needed, until someone calls Dudo. There is no turn cap and no auto-challenge. New dice are rolled only in a round where a hand ends, using a step with a 'when' condition, so there is at most one random draw per round. (fixes: P1): This restores the original's open horizon. Nobody knows in advance who will face the decisive bid, so risk falls on whoever misjudges the dice, not on a fixed position. Each round has a single choice step, well inside the limits.
- Remove the auto-challenge entirely. A raise is only ever settled if the next player calls it. (fixes: P3): No position gets the 'best of call or raise' privilege, so the 'always raise minimally on the last turn' policy no longer exists.
- Every raise must increase the quantity by at least 1, with any face 2 to 6. A same-quantity raise with a higher face is not allowed. The opening bid must have quantity at least max(1, floor(total dice / 4)). (fixes: P2): Bids reach contested territory within two or three turns, so creeping is impossible and every bidder after the opener carries real risk. It also bounds a hand at most total-dice + 1 turns, which keeps the game within the round limit.
- Keep 'the loser opens the next hand' from the original. Because there is no fixed horizon, opening no longer maps to a fixed hot seat. (fixes: P4): Under an open horizon, the opener's safe first bid is only a mild catch-up help for the player who just lost. It does not decide who loses next, so losses stop rotating mechanically by seat.
- Scale starting dice to the player count: 2 players get 4 dice each, 3 players get 3 each, 4 players get 2 each. Cap players at 4. If 40 rounds pass, the player with the most dice wins and a tie for most dice is a draw. (fixes: P5): A full game needs at most 7 or 8 die losses. At about 3 to 4 turns per hand, that is about 20 to 30 rounds, so the 40-round cap rarely binds.

## Kept from the original

- Hidden dice that only their owner sees, rolled fresh every hand
- Bids of 'at least N dice show face F' across the whole table, with ones wild
- Each turn is a choice between raising the bid and calling Dudo
- The wrong side of a challenge loses one die, and the loser opens the next hand
- Elimination at zero dice, and the last player with dice wins
- Bidding continues around the table until someone challenges, as in the original

## The variation's rules

SETUP: Seat the players in a random order, numbered seat 1 upward, with clockwise meaning increasing seat number and wrapping from the last seat to seat 1. Starting dice depend on the number of players: 2 players start with 4 dice each, 3 players with 3 each, 4 players with 2 each. Every player rolls their dice (six-sided, faces 1 to 6). Each player is privately shown their own faces and no one else's. Seat 1 is the opener of the first hand.

PUBLIC INFORMATION: At every turn all players are told how many dice each player holds, the total number of dice in play (T), the current bid and who made it (if any), and the list of bids made so far in this hand.

BIDS: A bid is a quantity and a face from 2 to 6, for example 'three 5s'. It claims that at least that many dice on the whole table show that face. Ones are wild and count toward every face. Ones cannot be named as a bid face.

EACH ROUND IS ONE TURN by the player to act.
(a) If there is no current bid, the player to act is the opener and must make an opening bid. The quantity must be at least max(1, floor(T / 4)) and at most T. If the opener calls Dudo instead, or makes an invalid bid, the opener loses one die and the hand ends with no count.
(b) If there is a current bid, the player to act either raises or calls 'Dudo'. A raise is a new bid whose quantity is at least the current quantity plus 1 and at most T, with any face from 2 to 6. An invalid raise counts as a Dudo call. If the current quantity already equals T, the player must call Dudo.
(c) After a valid bid or raise, it becomes the current bid, and the next surviving player clockwise is the player to act in the next round. Bidding wraps around the table as many times as needed.
(d) DUDO: When a player calls Dudo on the current bid, all dice are revealed to everyone. Count the dice showing the bid face plus all ones. If the count is at least the bid quantity, the bid was true and the caller loses one die. Otherwise the bid was false and the bidder loses one die. The hand ends.

AFTER A HAND ENDS (this happens in the same round as the Dudo call or failed opening): A player with 0 dice is eliminated, and this is announced. The player who lost the die becomes the opener of the next hand. If that player was eliminated, the next surviving player clockwise from them is the opener. The current bid is cleared. Every surviving player rolls all their remaining dice and is privately shown their own faces. T is recomputed. The opener acts in the next round.

END: The game ends immediately when only one player has dice left. The game also ends after round 40. In that case any hand still in progress is not resolved and its bids are ignored.

Objective: The last player with at least one die wins, and every other player loses. If the game ends after round 40 with more than one player holding dice, the player holding the most dice wins. If several players are tied for the most dice, it is a draw among those tied and every other player loses.

Expected effect: Without a fixed horizon there is no backward-induction squeeze. With +1-quantity raises and an opening floor, bids reach the expected count (about T/3 plus the bidder's own excess) within two or three turns. Whoever faces a bid that exceeds their own estimate must decide, and who that is depends on the dice and on earlier bids, not on seat. The simple policies all lose. 'Always call Dudo' loses to openers who bid their own count. 'Always raise minimally' is called once its bid passes the true count. 'Always bid your own count' is impossible after the opening because raises must go up. The open horizon prevents the hot seat, and the loser opening (now only a small catch-up advantage) no longer makes losses rotate by seat.

Worked example with 3 players and 9 dice. A holds 5,5,1. B holds 3,3,6. C holds 1,4,4. C opens 'two 4s', which is true from C's own dice. A raises to 'three 5s', also true from A's own dice. B holds no 5 and no 1, and reasons that A's switch to 5s signals at least two. If B calls, B loses for certain. B instead raises to 'four 3s', a stretch needing two more 3s or ones among the 6 unknown dice, about 65% true from B's view. C holds one wild and reads B as strong in 3s, so C raises to 'five 4s'. C's own 1,4,4 plus a likely 1 elsewhere gives about 4, so this is a bluff. A holds no 4s and one wild, counts at most 4, and calls Dudo. The true count of 4s is 4 (C's 1, 4 and 4, plus A's 1), so C loses a die. Under a fixed cap B, at turn 3, would have been the forced loser. Here the loser was the player who misjudged the dice.

Talk is left out. The bids are the communication channel and carry the bluffing. A free message phase each turn would cost extra steps, and since only one player can win there is little to bargain over. Unenforceable claims would mostly repeat what the bids already signal.

## Complexity (the designer's count, against the limits)

- steps_per_round: 16 (limit 20)
- choice_steps_per_round: 1 (limit 4)
- attributes: 13 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 40 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
