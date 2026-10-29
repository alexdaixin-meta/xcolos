# Variation: Knock Rummy Duel: Open Stock

A 2-player, 6-hand knock rummy with a 30-card suitless deck. Each player keeps 5 of 7 dealt cards. Every draw is a choice between two face-up cards. After a knock, the defender gets one last turn to undercut.

Players: 2 to 2, best with 2

## Review of the original

Knock Rummy is a draw-and-discard card game. Players try to form sets and runs, and any player may knock to end the hand at once. The lowest unmatched-card count (deadwood) wins the difference. A knocker who is not lowest pays a penalty. The reviewed 2-player variation (Even Hands) cut it to a 30-card suitless deck, 5-card hands, 4 hands and a 10-turn cap per hand.

- **non_degenerate**: weak. No pure policy is unbeatable. 'Never knock' loses to anyone who knocks early with a meld. 'Knock whenever possible' loses whenever the defender is lower and gets the +10. But one simple heuristic captures most of the edge: draw stock unless the upcard makes a meld, discard the highest loose card, knock at 8 or less. So the choices barely separate good play from rote play. The starter imbalance cancels only because A and B each start 2 hands.
- **skill_sensitive**: bad. The deal alone swings about 16 points per hand: a meld appears in 35-40% of 5-card deals, with expected deadwood about 11 with one and about 27.5 without. About half of the at most 5 draws per player are blind stock draws. The per-hand standard deviation is about 12-15, and over 4 hands the total difference has a standard deviation of about 25-30. A clearly better player gains about 12-15 per match and wins only about 60-65%.
- **headroom**: weak. Weak players do score, because luck hands them wins. Strong play plateaus quickly. With one meld per hand and blind draws, there is little beyond the knock-threshold heuristic to improve on. The 20-point rummy bonus is mostly a lottery on drawing into a 5-card run.
- **reasoning_dependent**: weak. There is hidden state: the opponent's hand and the stock. But the levers for using inference are small. Upcard pickups are rare, and the defender never gets to react to a knock, so reading the opponent rarely changes a decision. When both play well, the deal and the stock order decide the result.
- **verifiable**: good. Deadwood for a 5-card hand with at most one meld is a fixed arithmetic computation. Scoring and the winner are pure arithmetic.
- **fits_platform**: good. Turn-based and text-only, with no board. It has one shuffle per hand, few hidden elements and at most 40 turns. The only gap is that the rules did not say whether a taken upcard could be discarded on the same turn.

## Problems

- P1: The deal decides too much. A random 5-card hand either has a meld or does not, a swing of about 16 points before any decision.
- P2: Blind stock draws make about half of all draws pure chance, so a draw choice rarely takes thought.
- P3: The match is short: 4 hands with a per-hand standard deviation of 12-15. A better player wins only about 60-65%.
- P4: The 20-point rummy bonus rewards drawing into a 5-card run, which is luck, not reasoning.
- P5: Nothing makes reading the opponent matter. The knocker ends the hand instantly, so a defender's inference is never acted on and a knocker's risk is small.
- P6: Huge hands (a 40-deadwood bust against a 2) produce single swings that swamp many hands of small skill edges.
- P7: The rules are ambiguous about discarding the card just taken from the upcard.

## Changes

- Each hand, every player is dealt 7 cards and secretly keeps 5. The other 2 go face down to a dead pile that only their owner knows. (fixes: P1: The deal decides too much.): Choosing the best 5 of 7 raises the meld rate a lot (roughly 2 in 3 hands) and lets both players shape a low hand. Deal quality becomes far more even and the deal turns into a planning decision. The secret dead cards add a hidden element the opponent must reason about, since those values are out of play.
- The top card of the stock is always face up. Each turn the player chooses between two visible cards: the upcard or the stock top. (fixes: P2: Blind stock draws make about half of all draws pure chance, so a draw choice rarely takes thought.): This removes blind draws. Every draw is now a real comparison of two known options. Taking a card also denies it to the opponent. Every pickup is public, which feeds opponent modelling.
- The match is 6 hands of at most 6 turns each, 3 per player, giving at most 36 turns. A starts hands 1, 3 and 5; B starts hands 2, 4 and 6. (fixes: P3: The match is short: 4 hands with a per-hand standard deviation of 12-15. A better player wins only about 60-65%.): More hands average out the remaining chance. Equal turns per player within a hand remove the starter's extra turn, and alternating starters 3-3 removes any seat edge. Everything stays inside the 40-round limit.
- The rummy bonus is cut from 20 to 5. (fixes: P4: The 20-point rummy bonus rewards drawing into a 5-card run, which is luck, not reasoning.): A lucky 5-card run should not swing a hand.
- Knocking requires deadwood of 10 or less. After a knock, the defender is told the knocker's deadwood and takes one final turn (take one visible card, discard one, no knock) before the showdown. The undercut reward of (k minus d) plus 10 stays. (fixes: P5: Nothing makes reading the opponent matter. The knocker ends the hand instantly, so a defender's inference is never acted on and a knocker's risk is small.): The knocker must now estimate whether the defender can get under k with one more pick. That depends on the defender's pickups, discards and the visible cards. The defender gets a real decision informed by k. Knock timing becomes a bluff-and-read problem.
- Points scored in one hand are capped at 20, including bonuses. (fixes: P6: Huge hands (a 40-deadwood bust against a 2) produce single swings that swamp many hands of small skill edges.): This limits the damage of an occasional catastrophic hand, so the match rewards consistent good decisions across hands.
- The rules now state that a card taken from the upcard may not be discarded on the same turn, while a card taken from the stock top may be. (fixes: P7: The rules are ambiguous about discarding the card just taken from the upcard.): This removes the ambiguity and makes an upcard pickup a committed, informative signal.

## Kept from the original

- Draw-then-discard turns with a public upcard pile
- Melds as sets of three or runs of three or more, with the rest scored as deadwood
- Knocking to end the hand, scoring the deadwood difference
- Undercut punishment (+10) when the knocker is not lower
- A small bonus for going out with zero deadwood
- The scoring of a hand that ends with no knock
- Scores carried across hands, with the higher total winning

## The variation's rules

DECK: 30 cards, values 1 to 10, three copies of each value, no suits. A card is worth its value.

MATCH: The match is exactly 6 hands. Player A starts hands 1, 3 and 5. Player B starts hands 2, 4 and 6. Both scores start at 0 and carry across hands.

DEALING A HAND:
1. Shuffle all 30 cards.
2. Deal 7 cards face down to each player.
3. KEEP: Both players secretly and at the same time choose 5 of their 7 cards to keep. Each player's 2 other cards go face down into that player's own dead pile. Only the owner knows them. They are out of play for the hand.
4. Turn the next card face up to start the discard pile. Its top card is the 'upcard'.
5. The remaining 15 cards form the stock. The top card of the stock is always turned face up and visible to both players (the 'stock top'). Whenever it is taken, the next stock card is turned face up.

TURNS: Players alternate turns, beginning with the starter. A hand has at most 6 turns, 3 per player. On a turn the active player makes one decision with three parts:
(a) TAKE either the upcard or the stock top. Both players see which card was taken.
(b) DISCARD one of their 6 cards face up onto the discard pile, where it becomes the new upcard. A card taken from the upcard this turn may not be discarded this turn. A card taken from the stock top may be.
(c) Optionally KNOCK. A knock is allowed only if the player's deadwood after the discard is 10 or less.
If the active player knocked, the defender's final turn follows. If the 6th turn ends with no knock, a showdown with no knocker follows. Otherwise play passes to the other player.

DEFENDER'S FINAL TURN: After a knock, the defender is told the knocker's deadwood k. The defender then takes the upcard or the stock top and discards one card, under the same no-same-turn-discard rule for a taken upcard. The defender may not knock. Then a showdown happens.

MELDS AND DEADWOOD:
- A meld is 3 cards of equal value, or 3 or more cards of consecutive values (such as 4-5-6 or 6-7-8-9). 10 is not next to 1.
- A 5-card hand contains at most one meld.
- A hand's deadwood is computed automatically as the lowest possible: the sum of its 5 cards minus the sum of the meld that leaves the smallest remainder. With no meld, it is the sum of all 5 cards.

SHOWDOWN: Both hands are revealed. The dead piles are revealed too. Let k be the knocker's deadwood and d the defender's, both measured after the defender's final turn.
- If k < d, the knocker scores d - k. If k = 0, the knocker scores 5 more.
- If k >= d, the defender scores (k - d) + 10.
- With no knocker (6-turn cap reached), the player with the lower deadwood scores the difference. On a tie, nobody scores.
- No player can score more than 20 points in a single hand. Any excess is lost.

AFTER A SHOWDOWN: If fewer than 6 hands have been played, deal the next hand. After the 6th showdown, the match ends.

INFORMATION: Each player knows their own hand and their own dead pile. Both players see the whole discard pile, the current stock top, every card taken and from where, every discard, any knock and its k value, the hand and turn number, and both scores. The opponent's hand and dead pile and the stock below its top card stay hidden until the showdown.

Objective: After the 6th hand, the player with the higher total score wins. Equal totals are a draw.

Expected effect: Deal luck shrinks because both players build their hand from 7 cards, and draw luck largely disappears because both draw options are visible. The skill share therefore rises sharply. Over 6 hands with a 20-point cap, a better player's edge should outweigh the remaining noise far more often than the 60-65% of the previous version. The key decisions are:
- which 5 to keep, and what the opponent's two hidden dead cards might be;
- whether to take a card for yourself or to deny the opponent;
- when to knock, given that the defender gets one more pick and can be read from their pickups and discards.
A defender who sees k chooses between going for an undercut and limiting losses. Simple policies all lose to some opponent: always knock at the first legal moment, always take the stock top, and never knock.

## Complexity (the designer's count, against the limits)

- steps_per_round: 16 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 16 (limit 20)
- hidden_elements: 3 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 36 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
