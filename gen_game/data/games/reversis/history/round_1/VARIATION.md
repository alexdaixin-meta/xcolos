# Variation: Short Reversis

A four-player no-trump trick-avoidance game over 4 hands of 6 tricks each, with secret card passing, a Quinola worth 5, and a reversis (taking all 6 tricks) that hands 15 points to each opponent. The lowest total wins.

Players: 4 to 4, best with 4

## Review of the original

Reversis is a four-player trick-taking game with no trumps in which players try to avoid winning tricks that contain counting cards (A=4, K=3, Q=2, J=1), and the Jack of Hearts (Quinola) is especially dangerous. The player with the fewest points wins, unless someone takes every trick (the reversis), which reverses the aim and wins outright.

- **non_degenerate**: good. Always playing the lowest legal card loses to a player who dumps high counters when void of the led suit. Always playing high takes most of the points. The reversis threat stops 'just dodge everything' from being safe, because if all three others duck, one strong hand can sweep. The anticlockwise lead gives no lasting edge over a full deal. A single deal can favour whoever holds low cards.
- **skill_sensitive**: weak. Card counting, reading voids and timing discards are real skills. But one deal of 13 cards is heavily luck-driven: a hand full of high cards in long suits can hardly avoid points. The original gives no mechanism, such as passing or several hands, to average this out.
- **headroom**: good. Weak players still score, since points are spread around. Strong players improve through inference about voids, by holding back or forcing out the Quinola, and by spotting or blocking a reversis attempt. It is not solved.
- **reasoning_dependent**: good. Hands are hidden. Players must infer holdings from what others follow and discard, keep track of which counters are out, and plan several tricks ahead, both for safe exits and for or against a slam.
- **verifiable**: good. Trick winners follow from suit and rank. Points are card sums. Lowest total wins. Pools, side payments and the various Quinola bonus variants are messy, but they are still arithmetic.
- **fits_platform**: weak. The game is turn-based, text-only and has hidden hands, which all fit. However, 13 tricks with 52 cards, stakes, pools and several regional variants are too long and loosely specified. A deck that small per round and fixed rules are needed to stay within the step and round limits.

## Problems

- A single long deal makes the result depend heavily on the cards dealt (luck swamps skill).
- 52 cards and 13 tricks per deal is too long for the round limit once several deals are played to reduce luck.
- Pools, talon payments, side payments and the variant Quinola bonuses are underspecified and not a winner rule the engine can use.
- There is no decision before play that lets a player fix a bad deal, so the deal often decides the game before any reasoning happens.
- The reversis reward ('wins outright, sweeps pools') is not stated as numbers, so its risk and reward cannot be weighed.

## Changes

- Use a 24-card deck (A K Q J 9 8 in four suits) and deal 6 cards each, so a hand is 6 tricks. (fixes: 52 cards and 13 tricks per deal is too long for the round limit once several deals are played to reduce luck.): This keeps the full rank and counting structure, including the Quinola, while making a hand short enough to play several.
- Play 4 hands. The first lead rotates so that each seat leads first exactly once. Penalty points carry over between hands. (fixes: A single long deal makes the result depend heavily on the cards dealt (luck swamps skill).): Averaging over 4 deals and equal lead order reduces deal luck and seat advantage. It also creates multi-hand planning, such as pushing points onto the current leader.
- Before each hand except the 4th, every player at the same moment secretly passes 2 cards: to the left in hand 1, to the right in hand 2, across in hand 3, and no pass in hand 4. (fixes: There is no decision before play that lets a player fix a bad deal, so the deal often decides the game before any reasoning happens.): Passing lets good players repair a bad deal. It also creates hidden knowledge to exploit, since you know two cards an opponent holds and they know two of yours, and it opens the option to build toward a reversis.
- Fix the scoring: A=4, K=3, Q=2, J=1 per card taken, with the Quinola (J of hearts) worth 5 instead of 1. The total is 44 per hand. The winner is the player with the lowest total after 4 hands. (fixes: Pools, talon payments, side payments and the variant Quinola bonuses are underspecified and not a winner rule the engine can use.): This gives one exact, arithmetic objective with no pools or payments.
- Reversis: a player who takes all 6 tricks of a hand scores 0 for that hand, and each other player scores 15 instead of their card points. (fixes: The reversis reward ('wins outright, sweeps pools') is not stated as numbers, so its risk and reward cannot be weighed.): This keeps the reversal with a stated payoff that is large but not game-ending. The three others must sometimes take a counter on purpose to break a sweep, which creates conflict among them.

## Kept from the original

- Trick-avoidance with no trumps and strict follow-suit.
- The counting cards A=4, K=3, Q=2, J=1, with the lowest score winning.
- The Quinola (Jack of Hearts) as the special dangerous card.
- The reversis: taking every trick reverses the aim and punishes everyone else.
- Four players with hidden hands.

## The variation's rules

DECK: 24 cards, A K Q J 9 8 in each of the four suits (spades, hearts, diamonds, clubs). Rank within a suit, high to low: A, K, Q, J, 9, 8. There are no trumps.

SEATS: Players 1 to 4 sit in a circle. Play goes from player 1 to 2 to 3 to 4 and back to 1. 'Left' means the next player in that order, 'right' the previous, and 'across' the player two seats away.

GAME STRUCTURE: The game is 4 hands. Each hand is 7 rounds: one passing round followed by 6 trick rounds. That makes 28 rounds in total.

PASSING ROUND (first round of each hand):
(1) The deck is shuffled and each player is dealt 6 cards, seen only by that player.
(2) In hands 1, 2 and 3, all players at the same moment each secretly choose 2 cards from their hand to pass. The passes go left in hand 1, right in hand 2 and across in hand 3. Passed cards are added to the receiver's hand after everyone has chosen, and only the passer and receiver know which cards moved. In hand 4 there is no pass.
(3) The game announces that passing is complete.

TRICK ROUNDS (6 per hand):
- Lead: In the first trick of hand h, player h leads (player 1 in hand 1, player 2 in hand 2, and so on). In every later trick, the winner of the previous trick leads.
- Playing: Starting with the leader and going around in seat order, each of the 4 players plays one card face up. The leader may play any card. Each other player must play a card of the led suit if they hold one. If they hold none, they may play any card.
- Winning: The highest card of the led suit wins the trick. Cards of other suits never win.
- Recording: The trick winner adds the trick's points to their score for this hand. Points per card: A=4, K=3, Q=2, J=1, with the Jack of Hearts (Quinola) worth 5. Nines and Eights are worth 0. The winner's trick count for the hand goes up by 1. All played cards are public.

END OF HAND (after the 6th trick):
- If one player won all 6 tricks (a reversis), that player scores 0 for the hand and each other player scores 15 for the hand.
- Otherwise each player scores the points they took. These always total 44 across the four players.
- Hand scores are added to running totals, which are public. Hand scores and trick counts reset to 0.

END OF GAME: After the 4th hand, the game ends.

Objective: After 4 hands, the player with the lowest running total wins. If two or more players tie for the lowest total, the game is a draw.

Expected effect: Averaging over four hands, equal first leads and passing to repair bad deals should make card reading and planning matter more than the deal. Passing creates targeted inference: you know two of a neighbour's cards, can pass a dangerous Quinola or Ace into a likely void, or can keep strength to try a reversis. The reversis threat stops pure ducking: when one player is sweeping, someone among the other three must take a counting trick to stop it, and each would prefer that someone else pays. This is a real conflict among the opponents. Across hands, players should steer points toward whoever leads the running totals. Simple policies lose: always playing the lowest legal card lets voids be exploited and lets a sweeper go unchecked, always playing the highest card collects most of the 44 points, and random play is beaten by any counting player. Talk is left out. Its main use would be loose ganging-up deals among three players, which the engine cannot enforce. Play order, the card passes and the cards played already carry the signals that are worth reasoning about, and talk would add steps without adding a decision.

## Complexity (the designer's count, against the limits)

- steps_per_round: 13 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 12 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 28 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
