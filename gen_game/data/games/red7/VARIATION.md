# Variation: Red3 Duel

A 21-card, 3-colour Red7 for 2 or 3 players. You must lead under the current rule after your own turn, and you may change the rule by discarding. The match is first to 3 hands in a duel, or first to 6 points with a recent-winner tiebreak in 3 players, so every match has a winner.

Players: 2 to 3, best with 2

## Review of the original

Red7 is a card-shedding survival game. Each turn a player adds a card to their face-up palette and/or changes the rule card that decides who is 'winning', and must be winning after their turn or be eliminated. The last player standing wins the hand. The reviewed variation, Red3, cut it to 21 cards, 3 colours, 3 rules and a points match to 6.

- **non_degenerate**: weak. The card play in Red3 holds up against simple policies. Always-fold loses every hand. Always-play-strongest-and-never-switch loses to a rule switch: P has 7V (Red key 71) against Q's 2G, Q discards a Green card and leads 122 to 0. Always option (c) burns two cards a turn and runs out first. The leader is fixed by the dealt card, not the seat. The flaw is the 2-player scoring. Survivor 2 and last-eliminated 1 means the gap is just hands won minus hands lost, so every 2-2 split ends 6-6. That draws about 37% of matches between equals and about 35% at p=0.6.
- **skill_sensitive**: weak. Within a hand, card conservation and timing of rule switches decide survival, so skill shows. Over a 2-player match, though, a third of results are draws whatever the skill gap. At p=0.6 the stronger player wins only about 45% of matches outright. Each individual hand also carries real deal luck: the dealt palette fixes the first leader and the 5-card hand matters.
- **headroom**: good. Strong play involves several things: holding high cards back, inferring opponents' hands from the unseen cards (21 cards, at most 18 dealt), switching to a rule the opponent cannot answer, and keeping enough cards to outlast them. A weak player still wins some hands through the deal.
- **reasoning_dependent**: good. Hands and the set-aside cards are hidden. Whether a switch to Green is safe depends on whether the opponent likely holds an even card that beats your key. That must be inferred from the cards visible in palettes and on the canvas, and from how the opponent has chosen to spend cards so far.
- **verifiable**: good. Keys are arithmetic on public palette cards, eliminations are mechanical and points are counted. No judgement is needed.
- **fits_platform**: good. The game is turn-based text with hidden hands, one shuffle per hand and a 40-round cap. Each turn costs at least one card, so a hand lasts at most 6 rounds. The 21-card deck supports 2 or 3 players: 4 players would need 24 dealt cards, which the original's '2 to 4' cannot cover.

## Problems

- In 2 players the 2/1 hand scoring makes the score gap equal hands won minus hands lost, so any 2-2 split reaches 6-6 and the match is a draw (about 35-37% of matches).
- The 1-point consolation is meaningless in 2 players, because the loser of a hand is always the last eliminated.
- In 3 players a tie for most points at or above 6 (for example a hand winner going 4 to 6 while the runner-up goes 5 to 6) ends in a draw, and a tie at the round-40 cap also gives no winner.
- The stated player range must match the deck: 4 players cannot be dealt from 21 cards.

## Changes

- In 2-player matches, a hand winner scores 1 point and the loser 0. The first player to 3 points wins (best of five hands). (fixes: In 2 players the 2/1 hand scoring makes the score gap equal hands won minus hands lost, so any 2-2 split reaches 6-6 and the match is a draw (about 35-37% of matches).): An odd number of hands is needed to decide, so 2-2 can never end the match. A fifth hand always settles it, and the useless consolation point disappears.
- The 1-point consolation for the last-eliminated player applies only in 3-player matches. (fixes: The 1-point consolation is meaningless in 2 players, because the loser of a hand is always the last eliminated.): Finishing order genuinely varies in 3 players and is worth fighting for there. In 2 players it adds nothing.
- In 3 players, a tie for most points is broken in favour of the tied player who won the most recently completed hand. This applies both at the 6-point end and at the round-40 cap. (fixes: In 3 players a tie for most points at or above 6 (for example a hand winner going 4 to 6 while the runner-up goes 5 to 6) ends in a draw, and a tie at the round-40 cap also gives no winner.): Each hand has exactly one survivor, so 'most recent hand winner' always picks out one player. It also rewards closing out the deciding hand.
- The player count is fixed at 2 or 3. (fixes: The stated player range must match the deck: 4 players cannot be dealt from 21 cards.): The deal of 5 hidden cards plus 1 palette card per player needs 12 or 18 of the 21 cards. That always leaves some cards unseen, which keeps inference alive.

## Kept from the original

- Must be leading at the end of your own turn or be eliminated.
- Value beats colour: strength = number x 10 + colour rank.
- Discarding to the Canvas changes the rule, and play-then-discard is allowed.
- Three of Red7's rules: highest card, most evens, most cards below 4.
- Hidden hands, public palettes, last player standing wins the hand.
- A multi-hand match scored by hands survived.

## The variation's rules

CARDS. There are 21 cards: numbers 1 to 7 in each of three colours, Red, Green and Violet. Colour rank is Red 3, Green 2, Violet 1. A card's strength is number x 10 + colour rank (7 Red = 73, 4 Violet = 41). Higher strength beats lower. A card is EVEN if its number is 2, 4 or 6. A card is LOW if its number is 1, 2 or 3.

THE RULE. The Canvas shows one colour, which is the current rule. Each living player has a KEY under the current rule:
- Red: key = strength of the highest card in your palette.
- Green: key = 100 x (number of even cards in your palette) + strength of your highest even card, or 0 if you have no even card.
- Violet: key = 100 x (number of low cards in your palette) + strength of your highest low card, or 0 if you have no low card.
You are LEADING if your key is strictly higher than every other living player's key. If keys tie, including at 0, no tied player is leading.

SETUP OF A HAND. Shuffle all 21 cards. Deal each player 5 cards as a hidden hand, then 1 card face up as their palette. The remaining cards (9 with 2 players, 3 with 3 players) are set aside unseen for this hand. The Canvas starts as Red. Everyone is alive. The initial leader is the player whose palette card has the highest strength. The first turn of the hand goes to the next player in seat order after that leader.

A TURN. On your turn choose exactly one:
(a) play one card from your hand face up to your palette;
(b) discard one card from your hand to the Canvas, so the rule becomes that card's colour and the card leaves play;
(c) do (a), then (b), with two different cards;
(d) fold.
Then recompute keys under the current rule. If you are not leading, or you folded, or you named a card you do not hold, you are eliminated. Your palette stays visible but no longer counts. If you have no cards left in hand when your turn comes, you can only fold. Play passes to the next living player in seat order.

A ROUND is one pass of turns through all living players in seat order, starting with the player whose turn it is.

END OF A HAND. A hand ends the moment only one player is alive. That player is the hand winner.
- With 2 players: the hand winner scores 1 point; the other scores 0.
- With 3 players: the hand winner scores 2 points; the player whose elimination left one survivor scores 1; the first player eliminated scores 0.
The engine records the hand winner as the MOST RECENT HAND WINNER. If the match is not over, a new hand is set up at the start of the next round.

END OF THE MATCH.
- With 2 players, the match ends when a player reaches 3 points.
- With 3 players, the match ends after any hand in which a player reaches 6 or more points.
- In either case, it also ends when round 40 is complete; an unfinished hand then scores nothing.

INFORMATION. Palettes, the Canvas, eliminations, points and the most recent hand winner are public. Hands and set-aside cards are hidden. There is no table talk.

Objective: The player with the most points when the match ends wins. With 2 players this is the first to 3 points, and a tie cannot occur at that end. If two or more players share the most points, which can happen in 3 players or at the round-40 cap, the tied player who won the most recently completed hand wins. If no hand was completed at all, the match is a draw.

Expected effect: Draws in 2-player matches go from about 35% to essentially 0. With p=0.6 per hand, the stronger player now wins the best of five about 68% of the time instead of about 45% outright. Every hand matters to the end, and hand 5 is a true decider. In 3 players the recent-winner tiebreak removes draws and makes winning the deciding hand worth more than limping into second. Talk is left out: play is sequential and hidden-hand inference is the core skill, so cheap, unenforceable claims would add steps without adding a real decision. Within a hand, play is unchanged: players weigh when to spend high cards, infer from visible and discarded cards what opponents can answer, and switch rules to strand them.

## Complexity (the designer's count, against the limits)

- steps_per_round: 15 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 13 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 40 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
