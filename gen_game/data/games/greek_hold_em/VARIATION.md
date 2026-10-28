# Variation: Greek Hold 'em Mini II

This is a three-player, 36-hand numeric poker game. Each hand has one sequential betting round, played with three board cards visible and a fourth board card still hidden. Bets of 2 or 4 into a pot of 3, a rotating action order and an unseen last card make bluffing, hand-reading and position matter. The longer game lets skill outweigh the shuffle.

Players: 3 to 3, best with 3

## Review of the original

Greek hold 'em is a poker variant. Each player holds two private hole cards and must use both of them with exactly three of five community cards, with Texas hold 'em style betting rounds between the board stages. The previous XColos adaptation, Greek Hold 'em Mini, cut it to three players, an 18-card numeric deck, 12 hands, a simultaneous 0/1/2 opening bet, a simultaneous FOLD/CALL/RAISE decision after the whole board was visible, and a raise response.

- **non_degenerate**: good. No simple policy dominates. Always-raise gets called by strong hands, and never-fold pays off value bets. Seats were symmetric because all decisions were simultaneous, and choices do change pots.
- **skill_sensitive**: bad. Over 12 hands, σ ≈ 14 chips against a realistic skill edge of 4-6 chips gives edge/σ ≈ 0.3-0.4. A skilled player wins about 40-45% against two weaker players, versus 33% by chance. Card luck decides most games.
- **headroom**: weak. With every board card visible before the main decision, each player knew their exact final score. Good play collapses to fixed strength thresholds that a competent model finds quickly, leaving little to improve beyond that.
- **reasoning_dependent**: weak. Opponents' hole cards were hidden, but the simultaneous decision made bluff raises almost never win a fold, so reads hardly changed outcomes. The payoff to inference was small next to the shuffle.
- **verifiable**: good. Hand scores follow from a stated formula, and pots and totals are plain arithmetic. No judge is needed.
- **fits_platform**: good. It is text-only and turn-based, with one shuffle per hand, a small numeric deck and no board geometry. It fits within the step and attribute limits.

## Problems

- P1: Luck swamps skill. 12 hands is too few, and edge/σ ≈ 0.35 means the deal decides most games.
- P2: No uncertainty at the decision. All four board cards were visible before the main bet, so each player knew their exact score and the only open question was opponents' hole cards. Play reduced to fixed thresholds.
- P3: Bets had no fold equity. The decision was simultaneous and the raise of 2 was small against the pot, so bluffs almost never won a fold and raising was value-only.
- P4: No positional or sequential information. Nobody acted after seeing what others did within a betting round, so opponent modelling had little to work with.
- P5: The talk step cost time and steps but added little. Claims are free and unverifiable, and the bets themselves already carry the signal.
- P6: The carry rule (all three fold) and the multi-stage opening-bet-then-raise structure added steps and edge cases without adding decisions worth making.

## Changes

- Play 36 hands instead of 12. (fixes: P1): Per-game edge/σ grows with the square root of the number of hands, about 1.7× from length alone. Combined with the larger per-hand edge from the other changes, a skilled player should be clearly favoured. Duplicate dealing was rejected because replaying a shuffle with rotated hole hands tells players the other hands they held earlier, which leaks hidden information.
- Only board cards 1-3 are face up when betting; board card 4 stays face down until showdown. (fixes: P2): A hand can still gain 4 points if card 4 matches, so draws, card-removal reasoning and bluffing against possible improvement all matter. Hand strength is no longer certain.
- Replace the simultaneous opening bet and FOLD/CALL/RAISE decision with one sequential betting round. Each player, in an order that rotates each hand, chooses CHECK, BET 2 or BET 4 until someone bets. Later players then CALL or FOLD, and players who checked earlier respond with CALL or FOLD. (fixes: P3): A bet of 2 or 4 into a pot of 3 gives real fold equity. A bluff of 4 needs both others to fold only about 57% of the time, and a bluff of 2 about 40%. Players act on others' visible actions. Bet sizing becomes a signal that can be honest or deceptive. Check-then-call traps and stealing from the last seat become real options.
- The first actor rotates every hand, so each seat acts first 12 times, second 12 times and last 12 times. (fixes: P4): Sequential order creates positional information to exploit, and the rotation keeps seats balanced.
- Remove the table-talk step. (fixes: P5): In this zero-sum poker game talk is cheap and unverifiable. Bets already serve as costly, credible communication. Dropping talk shortens a 36-hand game and saves steps.
- Remove the carry and the separate raise stage. Because a bettor can never fold, the pot always goes to someone. (fixes: P6): This simplifies the build. The step count per hand falls to 15 and choice steps to at most 4 while keeping every meaningful decision.

## Kept from the original

- Two private hole cards per player, both of which must be used.
- Exactly three board cards count, so a hand scores at most three matches.
- Community cards revealed in stages, with betting while some cards are still unknown.
- Betting, calling and folding, with the last player in winning without a showdown.
- The compact 18-card numeric deck and the established scoring formula, which keep it a game of hand strength, reads and bluffs.

## The variation's rules

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

Objective: After 36 hands, the player with the highest chip total wins. If two or three players share the highest total, the game is a draw among them.

Expected effect: Players can no longer know their exact score when they bet. Card 4 can add 4 points, so paired-with-board hands and hands needing a match play differently. Bets now carry real fold equity: a 4-chip bluff into 3 needs folds only about 57% of the time. This rewards bluffing, check-calling traps, stealing from the third seat after two checks, and reading bet size as a strength signal. Position rotates, so no seat is favoured.

Simple policies all lose. Always-check/always-call gets value-bet without ever winning folds. Always-bet-4/always-call bleeds chips when strong hands call. Always-fold-to-bets is stolen from every hand. Random play loses to all of these.

So the outcome is not decided by the deal when everyone plays well. Even when all three play sensible threshold strategies, sequential bets with a hidden last card mean a player who reads opponents' bet sizes and frequencies, and adjusts bluffing to who still has to act, should gain more than a pure threshold player. A rough estimate is a skill edge of 0.5-0.8 chips per hand, about 18-29 over the game, against σ ≈ 20, for about a 55-65% win rate against two weaker players. This should be confirmed by 3-player simulation.

The chip lead also creates multi-hand planning. A leader late in the game can tighten up, but the ante makes passivity costly. Trailing players must take calculated risks.

Talk is left out. Bets are the costly, credible signals here. Free messages in a zero-sum poker game would only add words, so they fail the reasoning test even though interests conflict.

## Complexity (the designer's count, against the limits)

- steps_per_round: 15 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 18 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 36 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
