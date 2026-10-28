# 03 design

- time: 2026-10-28T05:25:36+00:00 (193.5s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 46a2d22a1b2e24ef, reply sha256 cd23ee85886bf95b

## Sent

````
Original game: Dudo
Players in the original: 2 to 10

Original rules:
Each player starts with 5 dice and a cup. Each round all players shake and conceal their dice, then look at only their own. In clockwise order starting from the loser of last round, players bid: a number and a face, claiming at least that many dice among all players show that face. Ones are wild and count as any face. A bid must increase either the quantity, the face value, or both. Bidding aces is special: to switch to aces you may halve the current quantity rounded up; to switch from aces you must more than double the quantity. Instead of raising, a player may call Dudo. All cups are lifted. If the bid is true (at least as many dice as claimed), the caller loses one die; otherwise the bidder loses one die. Losing your last die eliminates you. Last player with dice wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- balanced FAILED: The four-turn cap, together with the automatic challenge after a turn-4 raise, turns the turn-3 seat into a structural hot seat. Raises can creep by tiny steps (same quantity, next face), so early bids stay almost certainly true. Take a 3-player hand with 15 dice, so each unknown die matches a named face with p = 1/3.

(1) The opener can always make a guaranteed-true bid: the count of their own dice showing some face, plus their ones. A turn-2 call on that bid loses 100% of the time.

(2) Turn 2 makes a minimal raise, e.g. two 4s to two 5s. P(at least 2 of 15) = 1 - (2/3)^15 - 15(1/3)(2/3)^14 = 1 - 0.0023 - 0.0171 = about 0.98 true. A turn-3 call loses about 98% of the time.

(3) Turn 3 must therefore raise. Its bid can be minimal (two 6s or three 2s, about 0.92 to 0.98 true) or stretched. Say turn 3's bid is true with probability p.

(4) Turn 4 picks the better of two options: call, winning with probability 1-p, or raise one face higher, winning with roughly p because the step is tiny. Turn 4 also knows its own dice. So it wins with probability at least max(p, 1-p), which is 0.5 or more.

Win/lose table for turn 3 against turn 4:
- Turn 3 bids minimal (p about 0.95): turn 4 raises minimally (P true for three-of-15 = 1 - 0.0023 - 0.0171 - 0.0599 = about 0.92). Turn 3 loses about 92%.
- Turn 3 bids medium (p about 0.5): turn 4 calls or raises using its own dice. Turn 3 loses about 60%.
- Turn 3 bids high (p about 0.2): turn 4 calls. Turn 3 loses about 80%.
Turn 3 cannot get below roughly a 50% loss rate in any line.

Thoughtless policy test: 'on turn 4 always raise by the smallest step' wins about 90% against naive or minimal bidding, and never does worse than about 50%. 'Always open with your own count' essentially never loses the hand for the opener.

Seat structure:
- 3 players: the opener holds turns 1 and 4, both protected; the seat before the opener holds turn 3.
- 4 players: turn 4 goes to the seat just counter-clockwise of the opener.
Roles are fixed by the previous loser, so with good play die losses rotate almost mechanically. The 3-player sketch runs: hand 1, seat 3 loses; then seat 2; then seat 1; repeat. Move order, not judgement, carries most of the edge in each hand. No single option is strictly dominant, but a position that loses at least about 50% whatever it does is a large move-order imbalance.
- reasoning_over_luck FAILED: Assume everyone plays the intended good line:
- the opener bids their own count (safe);
- turn 2 raises by a small step (about 98% safe);
- turn 3 is squeezed (loses about 50 to 92%);
- turn 4 takes whichever of call or raise is better.

Under that line the loser of each hand is mostly the turn-3 seat, and that seat is fixed by who lost the previous hand. Losses then rotate nearly cyclically: in 3 players, seats 3, 2, 1, 3, 2, 1 down to one die each. The final eliminations depend on where that cycle sits plus dice noise. The winner is therefore largely set by the random initial seating and the rolls, not by better inference.

Estimate of what decides the result:
- seat-driven position: about 50% of the result;
- dice variance at the decisive one-die end-game: about 25%;
- skill (reading bids, using one's own dice, bluffing on turn 4): about 25%.

There is genuine inference available on turn 4 and in calling stretched bids. But a strong player in the turn-3 seat still loses at least half the time, so good reasoning is not clearly favoured.
- change: Remove the squeeze from the four-turn cap by forcing bids into contested territory quickly:
- Make every raise increase the quantity by at least 1; drop the same-quantity, higher-face raise.
- Set the minimum opening quantity to floor(total dice / 4).
With 15 dice that means an open of 3 or more and a turn-3 bid of 5 or more. With p = 1/3 the turn-3 bid is then near or above the expected count of 5, so it is genuinely uncertain (P about 0.4 to 0.6), and a turn-3 call on turn 2's bid is a real option.
- change: Replace the turn-4 auto-challenge with: 'Turn 4 must call Dudo on the current bid; it cannot raise.' Turn 4 then gets one option, not the better of two, and turn 3 can choose a bid that balances its risk.
- change: Show a simulated or computed per-position loss-rate table (turn 1, 2, 3, 4) under sensible play after the change. Each position should lose between about 15% and 40% of hands, with no position at 50% or more.
- change: Demonstrate that the per-hand loser no longer rotates deterministically by seat. Give a short worked example of a 3-player game in which bid-reading changes the elimination order.
The variation that was reviewed: Four-Call Dudo: SETUP: Seat the players in a random order (seats 1 to 3 or 1 to 4). Each player starts with 5 dice.

EACH ROUND (one hand):
1. Every player still in the game rolls all their dice. Each player is privately shown their own faces and no one else's. Everyone is told how many dice each player holds and the total number of dice in play.
2. The opener is the player who lost a die in the previous hand. If that player was eliminated, the opener is the next surviving player clockwise. Seat 1 opens the first hand.
3. A bid is a quantity and a face from 2 to 6, for example 'four 5s'. It claims that at least that many dice on the whole table show that face. Ones are wild and count toward every face. Ones cannot be bid as a face.
4. A raise must name a higher quantity (with any face), or the same quantity with a higher face. The quantity must be at least 1 and at most the total dice in play.
5. BIDDING: up to four turns are taken in clockwise order starting with the opener, skipping eliminated players and wrapping around if needed. With 3 players the order is opener, next, next, opener. With 2 survivors the two alternate.
   Turn 1: the opener must make a bid. If it is invalid, the opener loses one die, the hand ends, and no dice are counted.
   Turns 2, 3 and 4: the player either raises or calls 'Dudo' on the current bid. An invalid raise counts as a Dudo call.
   As soon as anyone calls Dudo, bidding stops.
   If turn 4 is a valid raise, the player who made the bid before it is automatically deemed to call Dudo on that raise.
6. RESOLUTION: All dice are revealed. Count the dice showing the bid face plus all ones.
   If the count is at least the bid quantity, the bid is true and the challenger loses one die.
   Otherwise the bid is false and the bidder loses one die.
7. A player with 0 dice is eliminated.
8. The loser of the die opens the next hand (see step 2).

END: The game ends when only one player has dice left. It cannot last more than 19 hands. A limit of 40 rounds exists only as a technical safeguard; if it were ever reached, the player with the most dice would win, and players tied on most dice would share a draw. Winner: The last player with at least one die wins. Every other player loses. If the 40-round safeguard were reached, the player holding the most dice wins, and a tie for most dice is a draw among those tied.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Dudo (Liar's Dice) is a bluffing game for 2 to 10 players. Each player hides their own dice, and players in turn raise a public claim about how many dice on the table show a face, with ones wild. Anyone may challenge with 'Dudo' instead of raising, the wrong side loses a die, and the last player with dice wins. The previous adaptation, Four-Call Dudo, capped each hand at four bidding turns and auto-challenged a raise made on turn 4.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "bad",
      "evidence": "This verdict is for the reviewed Four-Call variation. The fixed four-turn horizon creates a hot seat. The opener can always bid their own count and is never wrong. Turn 2 can creep by changing only the face, for example two 4s to two 5s, which is true about 98% of the time with 15 dice. Turn 3 is then squeezed, and turn 4 wins with probability at least max(p, 1-p). The thoughtless policy 'on turn 4 always raise by the smallest step' wins about 90% against naive play and never drops below about 50%. Turn 3 loses at least about 50% whatever it does. I also checked the suggested patch, in which turn 4 must call and raises need +1 quantity. By backward induction, turn 2 then has a nearly risk-free bid near the expected count minus one, and the loss lands on turns 3 and 4 (about 42% and 58%). Any fixed horizon puts the risk on fixed positions. The original Dudo, with unlimited wrap-around bidding, has no such seat."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "In Four-Call, about half of each result came from seat position, which is fixed by who lost the previous hand. A strong player sitting at turn 3 still loses at least half the time. The original Dudo is strongly skill-sensitive: reading bids, using your own dice and timing a challenge all matter, and research on Liar's Dice shows large gaps between good and naive strategies."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Estimating the count from your own dice plus what other players' bids reveal about their dice, choosing which face to bid, bluffing a face to mislead, and judging when a rival is stretching are all open-ended skills. A weak player who bids around the expected count still wins hands, so weak play is not hopeless."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Every player's dice are hidden. Each bid is a noisy and possibly deceptive signal about the bidder's dice. The decision to call or raise is a probabilistic inference that combines your own dice with what you can read into the bid history."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "A challenge is settled by counting the dice showing the bid face plus ones and comparing with the bid quantity. Losing dice, elimination and the last survivor are all arithmetic."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "Dudo is text-only and turn-based. The four-turn cap was introduced only to fit at most 4 choice steps into a round, and that cap is what broke balance. The original's unlimited bidding fits if one round is one turn instead of one hand. That keeps one choice step per round, but the game must then finish within 40 turns, so starting dice must be fewer."
    }
  ],
  "problems": [
    "P1: The fixed four-turn horizon makes the turn-3 or turn-4 position a structural hot seat. By backward induction, any fixed cap concentrates the loss on fixed positions, so seat order, not judgement, decides most hands.",
    "P2: Same-quantity, higher-face raises let early bidders creep with almost certainly true bids, so they carry no risk and make no real decision.",
    "P3: The auto-challenge after a turn-4 raise gives turn 4 the better of two options (at least max(p, 1-p)). This yields a thoughtless policy that wins about 90%: always raise minimally on turn 4.",
    "P4: Because the previous loser opens and positions are fixed relative to the opener, losses rotate nearly cyclically by seat. The winner is then largely set by the initial seating and the dice (the lottery trap).",
    "P5: If bidding is uncapped and starting dice are not reduced, a full game cannot reliably fit within 40 rounds."
  ],
  "changes": [
    {
      "what": "Make one round equal one bidding turn, not one hand. A hand continues around the table, wrapping as often as needed, until someone calls Dudo. There is no turn cap and no auto-challenge. New dice are rolled only in a round where a hand ends, using a step with a 'when' condition, so there is at most one random draw per round.",
      "why": "This restores the original's open horizon. Nobody knows in advance who will face the decisive bid, so risk falls on whoever misjudges the dice, not on a fixed position. Each round has a single choice step, well inside the limits.",
      "fixes": "P1"
    },
    {
      "what": "Remove the auto-challenge entirely. A raise is only ever settled if the next player calls it.",
      "why": "No position gets the 'best of call or raise' privilege, so the 'always raise minimally on the last turn' policy no longer exists.",
      "fixes": "P3"
    },
    {
      "what": "Every raise must increase the quantity by at least 1, with any face 2 to 6. A same-quantity raise with a higher face is not allowed. The opening bid must have quantity at least max(1, floor(total dice / 4)).",
      "why": "Bids reach contested territory within two or three turns, so creeping is impossible and every bidder after the opener carries real risk. It also bounds a hand at most total-dice + 1 turns, which keeps the game within the round limit.",
      "fixes": "P2"
    },
    {
      "what": "Keep 'the loser opens the next hand' from the original. Because there is no fixed horizon, opening no longer maps to a fixed hot seat.",
      "why": "Under an open horizon, the opener's safe first bid is only a mild catch-up help for the player who just lost. It does not decide who loses next, so losses stop rotating mechanically by seat.",
      "fixes": "P4"
    },
    {
      "what": "Scale starting dice to the player count: 2 players get 4 dice each, 3 players get 3 each, 4 players get 2 each. Cap players at 4. If 40 rounds pass, the player with the most dice wins and a tie for most dice is a draw.",
      "why": "A full game needs at most 7 or 8 die losses. At about 3 to 4 turns per hand, that is about 20 to 30 rounds, so the 40-round cap rarely binds.",
      "fixes": "P5"
    }
  ],
  "keeps": [
    "Hidden dice that only their owner sees, rolled fresh every hand",
    "Bids of 'at least N dice show face F' across the whole table, with ones wild",
    "Each turn is a choice between raising the bid and calling Dudo",
    "The wrong side of a challenge loses one die, and the loser opens the next hand",
    "Elimination at zero dice, and the last player with dice wins",
    "Bidding continues around the table until someone challenges, as in the original"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The imbalance came entirely from the artificial turn cap. Making each round a single turn restores Dudo's open-ended bidding inside the engine limits."
  },
  "variation": {
    "name": "Open-Table Dudo",
    "summary": "This is Liar's Dice played one turn per round. Players raise a shared claim about the hidden dice, with ones wild, until someone calls Dudo. The wrong side loses a die, and the last player with dice wins. There is no turn cap, so no seat is a built-in hot seat.",
    "players": {
      "min": 2,
      "max": 4,
      "suggested": 3
    },
    "rules": "SETUP: Seat the players in a random order, numbered seat 1 upward, with clockwise meaning increasing seat number and wrapping from the last seat to seat 1. Starting dice depend on the number of players: 2 players start with 4 dice each, 3 players with 3 each, 4 players with 2 each. Every player rolls their dice (six-sided, faces 1 to 6). Each player is privately shown their own faces and no one else's. Seat 1 is the opener of the first hand.\n\nPUBLIC INFORMATION: At every turn all players are told how many dice each player holds, the total number of dice in play (T), the current bid and who made it (if any), and the list of bids made so far in this hand.\n\nBIDS: A bid is a quantity and a face from 2 to 6, for example 'three 5s'. It claims that at least that many dice on the whole table show that face. Ones are wild and count toward every face. Ones cannot be named as a bid face.\n\nEACH ROUND IS ONE TURN by the player to act.\n(a) If there is no current bid, the player to act is the opener and must make an opening bid. The quantity must be at least max(1, floor(T / 4)) and at most T. If the opener calls Dudo instead, or makes an invalid bid, the opener loses one die and the hand ends with no count.\n(b) If there is a current bid, the player to act either raises or calls 'Dudo'. A raise is a new bid whose quantity is at least the current quantity plus 1 and at most T, with any face from 2 to 6. An invalid raise counts as a Dudo call. If the current quantity already equals T, the player must call Dudo.\n(c) After a valid bid or raise, it becomes the current bid, and the next surviving player clockwise is the player to act in the next round. Bidding wraps around the table as many times as needed.\n(d) DUDO: When a player calls Dudo on the current bid, all dice are revealed to everyone. Count the dice showing the bid face plus all ones. If the count is at least the bid quantity, the bid was true and the caller loses one die. Otherwise the bid was false and the bidder loses one die. The hand ends.\n\nAFTER A HAND ENDS (this happens in the same round as the Dudo call or failed opening): A player with 0 dice is eliminated, and this is announced. The player who lost the die becomes the opener of the next hand. If that player was eliminated, the next surviving player clockwise from them is the opener. The current bid is cleared. Every surviving player rolls all their remaining dice and is privately shown their own faces. T is recomputed. The opener acts in the next round.\n\nEND: The game ends immediately when only one player has dice left. The game also ends after round 40. In that case any hand still in progress is not resolved and its bids are ignored.",
    "objective": "The last player with at least one die wins, and every other player loses. If the game ends after round 40 with more than one player holding dice, the player holding the most dice wins. If several players are tied for the most dice, it is a draw among those tied and every other player loses.",
    "expected_effect": "Without a fixed horizon there is no backward-induction squeeze. With +1-quantity raises and an opening floor, bids reach the expected count (about T/3 plus the bidder's own excess) within two or three turns. Whoever faces a bid that exceeds their own estimate must decide, and who that is depends on the dice and on earlier bids, not on seat. The simple policies all lose. 'Always call Dudo' loses to openers who bid their own count. 'Always raise minimally' is called once its bid passes the true count. 'Always bid your own count' is impossible after the opening because raises must go up. The open horizon prevents the hot seat, and the loser opening (now only a small catch-up advantage) no longer makes losses rotate by seat.\n\nWorked example with 3 players and 9 dice. A holds 5,5,1. B holds 3,3,6. C holds 1,4,4. C opens 'two 4s', which is true from C's own dice. A raises to 'three 5s', also true from A's own dice. B holds no 5 and no 1, and reasons that A's switch to 5s signals at least two. If B calls, B loses for certain. B instead raises to 'four 3s', a stretch needing two more 3s or ones among the 6 unknown dice, about 65% true from B's view. C holds one wild and reads B as strong in 3s, so C raises to 'five 4s'. C's own 1,4,4 plus a likely 1 elsewhere gives about 4, so this is a bluff. A holds no 4s and one wild, counts at most 4, and calls Dudo. The true count of 4s is 4 (C's 1, 4 and 4, plus A's 1), so C loses a die. Under a fixed cap B, at turn 3, would have been the forced loser. Here the loser was the player who misjudged the dice.\n\nTalk is left out. The bids are the communication channel and carry the bluffing. A free message phase each turn would cost extra steps, and since only one player can win there is little to bargain over. Unenforceable claims would mostly repeat what the bids already signal."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 16,
    "choice_steps_per_round": 1,
    "attributes": 13,
    "hidden_elements": 1,
    "random_draws_per_round": 1,
    "rounds": 40
  }
}
```
````
