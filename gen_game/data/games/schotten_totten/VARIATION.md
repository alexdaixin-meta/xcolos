# Variation: Schotten Totten: Five Stones

A compact two-player Schotten Totten. Players alternate placing one card from a hidden 6-card hand onto their side of one of 5 Stones. Each Stone is resolved arithmetically when both sides hold 3 cards, and the first to claim 3 Stones wins.

Players: 2 to 2, best with 2

## Review of the original

Schotten Totten is a two-player card game. Players lay cards from a hidden six-card hand onto their side of nine Stones in a line. Each side of a Stone is completed with three cards forming poker-like formations, the stronger formation claims the Stone, and the first player to 5 Stones or to 3 adjacent Stones wins.

- **non_degenerate**: good. A thoughtless policy, such as always playing the lowest card to the leftmost open Stone, breaks up its own formations and loses most Stones to a player who builds flushes and straights. Neither seat has a clear edge: the first player has tempo, and the second sees one more card before committing. Every placement is permanent, so choices decide the outcome.
- **skill_sensitive**: good. Card counting, managing the hand, and timing commitments to win the 'who completed first' tie-break all give experienced players a reliable edge. Draw luck matters within a single game, but six-card hands and nine Stones give many decisions that smooth it out.
- **headroom**: good. A weak player still wins Stones with naturally strong hands. A strong player keeps gaining from tracking which cards are gone, from sacrificing Stones deliberately, and from forcing the opponent to spoil formations when they run out of safe plays.
- **reasoning_dependent**: good. Hands and the deck order are hidden. Players must infer what the opponent is holding back from the cards visible on the table, and plan which Stones to contest over many turns.
- **verifiable**: weak. Comparing formations at the end is arithmetic. The early-claim rule, which requires 'proving' the opponent cannot beat you, is an open-ended search over unseen cards, and the engine cannot check it simply.
- **fits_platform**: weak. The game is turn-based and text-only, but it breaks the platform limits in several ways. The '3 adjacent Stones' win depends on adjacency. Nine Stones with two sides each need 18 side attributes plus hands and deck, which exceeds the 20-attribute limit. Each round has two random draws, but only one is allowed. A full game takes about 50 or more turns, and the limit is 40 rounds.

## Problems

- The '3 adjacent Stones' victory depends on adjacency in a line, which is a spatial element the platform excludes.
- Nine Stones need 18 side attributes plus hands, deck and scores, which is more than 20 attributes.
- A round in which both players play and draw has two random draws, but the limit is one.
- A full game runs past 40 rounds.
- The early-claim 'proof' rule cannot be checked by simple arithmetic.
- Recognising formations is described in words and needs an exact arithmetic definition for the engine.

## Changes

- Remove the adjacency win. The game is won by claiming 3 of the 5 Stones, which is a strict majority. (fixes: The '3 adjacent Stones' victory depends on adjacency in a line, which is a spatial element the platform excludes.): This keeps a 'first to a majority' race without any spatial relation.
- Use 5 Stones instead of 9, and a 36-card deck (4 colours x values 1-9) instead of 54 cards. (fixes: Nine Stones need 18 side attributes plus hands, deck and scores, which is more than 20 attributes.): Ten Stone-side lists plus hands, deck and claim tracking fit within 20 attributes. The smaller deck keeps formations about as frequent relative to the number of Stones.
- Make one round equal one player's turn. Players alternate, and each round has at most one draw. (fixes: A round in which both players play and draw has two random draws, but the limit is one.): This gives exactly one chance event per round.
- Fix the length at 30 rounds: 5 Stones x 3 cards x 2 players. The game can end earlier when someone reaches 3 Stones. (fixes: A full game runs past 40 rounds.): This keeps the game within 40 rounds.
- Remove early claims. A Stone is resolved automatically as soon as both sides hold 3 cards. The tie-break 'player who completed their side first' is kept and tracked with one attribute per Stone. (fixes: The early-claim 'proof' rule cannot be checked by simple arithmetic.): Every resolution becomes pure arithmetic, while the tempo element of the tie-break survives.
- Define formation strength numerically: strength = sum of values + a tier bonus. The bonus is 120 for a Straight Flush, 90 for Three of a Kind, 60 for a Flush, 30 for a Straight, and 0 otherwise. (fixes: Recognising formations is described in words and needs an exact arithmetic definition for the engine.): The highest possible sum is 27, which is less than the 30-point gap between tiers. So the formula reproduces the original order exactly, and a single calculation compares two sides.

## Kept from the original

- Two players lay cards from a hidden hand onto their own side of contested Stones.
- Each side of a Stone holds three permanent cards, scored in the original formation order: Straight Flush > Three of a Kind > Flush > Straight > High sum.
- The tie-break by higher sum and then by who completed first.
- A forced play every turn, so a player who runs out of good moves must spoil a formation.
- Drawing one card after each play while the deck lasts.
- Racing to claim a majority of the Stones.

## The variation's rules

COMPONENTS: A deck of 36 cards, 4 colours (Red, Blue, Green, Yellow) x values 1-9, each card written like 'R7'. There are 5 Stones numbered 1-5. Each Stone has a side for Player A and a side for Player B, and each side holds at most 3 cards.

SETUP: Shuffle the deck. Deal 6 cards face down to each player. Each hand is private: only its owner sees it. The remaining 24 cards form a face-down draw pile. Randomly decide which player is A; A takes the first turn.

ROUNDS: The game has at most 30 rounds. In odd rounds Player A is active; in even rounds Player B is active. Each round:
(1) The engine announces to both players the cards on every side of every Stone, which Stones are claimed and by whom, each player's number of claimed Stones, and how many cards remain in the draw pile.
(2) The active player chooses one card from their hand.
(3) The active player chooses one Stone that is unclaimed and whose side for that player holds fewer than 3 cards. A player always has such a Stone and a card to play, and must play.
(4) The card moves from the hand to that player's side of the chosen Stone, face up. Cards never move again.
(5) If this card was the third card on that side and the other side has fewer than 3 cards, record this player as that Stone's 'first finisher'.
(6) If the draw pile is not empty, the active player draws its top card into their hand.
(7) For each unclaimed Stone where both sides now hold 3 cards, resolve it, as described below.
(8) If either player has claimed 3 Stones, the game ends immediately and that player wins.

STRENGTH OF A SIDE: Let the three values sum to S. The side has one formation:
- Straight Flush: all three cards share a colour, the values are all different, and highest minus lowest equals 2. Bonus 120.
- Three of a Kind: all three values are equal. Bonus 90.
- Flush: all three cards share a colour (and the side is not a Straight Flush). Bonus 60.
- Straight: the values are all different and highest minus lowest equals 2 (and the side is not a Straight Flush). Bonus 30.
- Otherwise: bonus 0.
Strength = S + bonus.

RESOLVING A STONE: The side with the higher strength claims the Stone. If the strengths are equal, the first finisher of that Stone claims it. A claimed Stone stays on the table with its cards visible, but it can no longer be played on.

END OF CARDS: After round 30 every Stone has been resolved. If no one has reached 3 Stones (possible only if the game has not yet ended), the player with more claimed Stones wins. Equal counts are a draw.

Objective: The first player to claim 3 of the 5 Stones wins immediately. If the game reaches the end of round 30 without this, the player with more claimed Stones wins, and equal counts are a draw. With the first-finisher tie-break every resolved Stone has an owner, so in practice someone reaches 3.

Expected effect: Play keeps the original's tension. Players should hold strong partial formations back, count which values and colours are gone in order to judge whether an opponent's two-card start can still become a Straight Flush or Three of a Kind, and race to complete a side first so they win ties. The forced play every turn creates late-game squeeze: a player whose safe moves run out must dump cards onto Stones they are willing to concede, and choosing which Stones to give up becomes a key decision. Five Stones with a 3-Stone majority makes each Stone weighty, so sacrificing one Stone to secure two others is a real plan. The 6-card hand and alternating turns give enough decisions per game that skill outweighs the draw. Talk is omitted, because in a two-player zero-sum race it adds no reasoning beyond bluffing that the hidden hand already supplies.

## Complexity (the designer's count, against the limits)

- steps_per_round: 12 (limit 20)
- choice_steps_per_round: 2 (limit 4)
- attributes: 20 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 30 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
