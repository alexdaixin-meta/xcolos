# Variation: Put: Show One, Keep Three

A two-player bluffing card duel over 40 hands. Each player holds 4 cards, one of them face up. Players bet in sequence (PUT, SEE, FOLD, RE-PUT) on a best-of-3-tricks showdown played with 3 of their 4 cards in a secretly chosen order.

Players: 2 to 2, best with 2

## Review of the original

Put is an old two-to-four-player trick game with 3 cards each and the odd rank order 3-2-A-K-...-4. Players do not have to follow suit, and winning 2 of 3 tricks scores a point. At any moment a player may call 'Put' to stake the whole game, and the opponent must fold (conceding 1) or 'see it'. The previously tested two-player variation, 'Put: Trick by Trick', used a simultaneous PUT / HOLD-AND-SEE / HOLD-AND-FOLD call before trick 1 and again before trick 2, a raised stake of 3, and 24 hands.

- **non_degenerate**: weak. Always-PUT forces every hand to stake 3 at the first call, so the second call never happens. The thoughtful player's only levers are a blind fold-or-see and a near-random 3-card allocation. Correct play gains only about +0.25 per hand, about +6 over 24 hands, against a match spread of about 10. Always-PUT therefore still wins roughly 25-30% of matches. No seat has an edge, but a thoughtless policy is far too competitive.
- **skill_sensitive**: bad. When both players play sensibly, the decisive points come from stake-3 showdowns between two hands both players liked. These are settled by which 3 random cards are stronger. The test estimates that chance decides 40-50% of matches.
- **headroom**: weak. There is little to improve on beyond a fold threshold of about the bottom 30% of hands. Allocation of 3 cards in simultaneous play adds about +0.05 per hand. A weak player can score, but a strong one has almost no further levers.
- **reasoning_dependent**: weak. Cards are hidden, but the first call is simultaneous, so there is no betting sequence to read. The trick-1 card that could inform the second call is seen only when nobody put at call 1, which a PUT-heavy opponent prevents. Bluffing and opponent reading barely move the score.
- **verifiable**: good. Tricks, stakes, points and hands won are all arithmetic. No judge is needed.
- **fits_platform**: good. It is two-player, turn-based and text-only, with one deal per hand. It uses 4 choice steps at most and stays within the step limits.

## Problems

- P1: Always-PUT is too strong. Because the first call is simultaneous, putting blind cannot be punished by a re-raise, and it wins about 25-30% of matches against correct play.
- P2: The deal dominates. Stake-3 showdowns between two strong hands decide most matches, and about 40-50% of results are chance.
- P3: Inference is thin. A simultaneous first call gives no betting sequence to read, no information is public before betting, and the second call is usually skipped.
- P4: Card play is nearly skill-free. With 3 cards and nothing to choose except the order, the stronger hand wins its tricks almost regardless.
- P5: The match is too short. 24 hands cannot let a per-hand skill edge outweigh the variance.

## Changes

- The betting becomes a sequence with a re-raise. The caller, who alternates each hand, says PUT or PASS. The responder answers a PUT with SEE, FOLD or RE-PUT, and answers a PASS with PUT or PASS. The caller then answers a RE-PUT, or a PUT made after their PASS, with SEE or FOLD. (fixes: P1): A blind putter can now be re-put by a strong hand and must then fold, costing 2, or see at stake 4. Calls are made in order, so they can be read and bluffed.
- The stakes are rescaled: 1 if nobody puts, 2 if a PUT is seen, 4 if a RE-PUT is seen. A fold to a PUT pays the putter 1, and a fold to a RE-PUT pays the re-putter 2. (fixes: P1): The ladder rewards value-raising strong hands against a player who never folds, and makes well-timed bluffs and folds worth real points. Against always-PUT, folding the bottom ~37% of hands and re-putting the rest yields about +0.56 per hand.
- Each player is dealt 4 cards. The 4th is face up, visible to both, and the other 3 are private. A player plays only 3 of the 4 cards and chooses which to leave out. (fixes: P3, P4, P2): The public card gives each player something to infer the opponent's strength and calls from. Choosing which card to drop, and in what order to play the others, against a known opponent card adds decisions to the card play. Every bet is judged against visible information.
- Card play becomes a single simultaneous secret submission of an ordered list of 3 cards. Trick 1 is the first card of each list, and so on. (fixes: P4): This keeps the original's free play of any card while fitting the 4-choice limit next to three betting steps. Ordering against a known face-up card is a guessing game in which reading the opponent pays.
- The match lasts 40 hands instead of 24, with the caller alternating so each player calls 20 times. (fixes: P5, P2): Estimated edge against always-PUT is about +22 points against a spread of about 20 over 40 hands, which puts the thoughtless policy near or below a 13% win rate. The reasoner-vs-reasoner edges from reading and bluffing also accumulate.
- The original rule is restored that a hand is scored only by a player who wins at least 2 of the 3 tricks. Trick-and-tie, or one trick each with a tie, scores nothing. (fixes: P2, P4): This is faithful to the original and makes the choice of order matter. A weaker hand that forces ties can neutralise a big stake.

## Kept from the original

- The rank order 3-2-A-K-Q-J-10-9-8-7-6-5-4, with suits irrelevant.
- Any card may be played, with no need to follow suit.
- Equal ranks tie a trick, which belongs to no one.
- Winning 2 of 3 tricks scores the hand, and trick-and-tie scores nothing.
- The 'Put' call that raises the stake, answered by 'I see it' or by folding and conceding.
- Three-card hands in play and an alternating first player.

## The variation's rules

CARDS. Use a standard 52-card deck; suits do not matter. Strengths: 3 = 13, 2 = 12, A = 11, K = 10, Q = 9, J = 8, 10 = 7, 9 = 6, 8 = 5, 7 = 4, 6 = 3, 5 = 2, 4 = 1. Higher strength is better.

SETUP. There are two players, A and B. Each starts with 0 points and 0 hands won. The match lasts exactly 40 hands. In odd-numbered hands A is the Caller and B the Responder. In even-numbered hands B is the Caller and A the Responder.

EACH HAND:
1. Deal. Shuffle all 52 cards and deal 4 cards to each player. Each player's 4th card is face up and announced to both players. The other 3 are private to their holder.

2. Caller's call. The Caller says PUT or PASS.

3. Responder's answer.
- If the Caller said PUT, the Responder says SEE, FOLD or RE-PUT. On SEE, the stake is 2; go to step 5. On FOLD, the Caller scores 1 point and wins the hand; go to step 8. On RE-PUT, go to step 4.
- If the Caller said PASS, the Responder says PUT or PASS. On PASS, the stake is 1; go to step 5. On PUT, go to step 4.

4. Caller's answer. This step happens only if the Responder said RE-PUT or PUT in step 3. The Caller says SEE or FOLD.
- After a RE-PUT: SEE makes the stake 4. FOLD gives the Responder 2 points and the hand.
- After a PUT that followed the Caller's PASS: SEE makes the stake 2. FOLD gives the Responder 1 point and the hand.
- A FOLD ends the hand; go to step 8.

5. Play (simultaneous). Each player secretly writes an ordered list of 3 different cards chosen from their own 4 cards. The face-up card may be used or left out. The lists are then revealed.

6. Tricks. Compare the 1st cards of the two lists, then the 2nd cards, then the 3rd cards. In each pair the higher strength wins that trick. Equal strength ties the trick, and it belongs to no one.

7. Score. A player who won at least 2 of the 3 tricks scores the stake (1, 2 or 4) and wins the hand. Otherwise, for example one trick each with a tie, or one win and two ties, or three ties, nobody scores.

8. Announce. Announce all calls, all 8 cards (including any card that was left out or never played), the hand result, and both players' points and hands won.

END. After hand 40 the match ends.

Objective: After 40 hands, the player with more points wins. If points are equal, the player with more hands won wins. A hand is won by scoring it on tricks or by the opponent folding. If both are equal, the match is a draw.

Expected effect: Always-PUT is now punished. A reader re-puts the top ~60% of hands and folds the rest cheaply, for an estimated edge of about +0.56 per hand, about +22 over 40 hands against a spread of about 20. That leaves the blind policy winning roughly 10-13% of matches. Always-SEE loses to value raises, and always-PASS or always-FOLD lose outright. Between two reasoners, the visible card and the order of calls give something to read. A PASS from a Caller showing a 3 is suspicious, and a RE-PUT against a high face-up card signals strength or a bluff. Folds at 1 or 2 points and value raises to 4 now shift the score as much as raw card strength does. Choosing which card to leave out, and how to order the rest against a known enemy card, rewards anticipating the opponent's order. Equal-rank ties let a weaker hand void a big stake. This is a two-player zero-sum duel, so talk is omitted: it would add nothing beyond what the calls already signal.

## Complexity (the designer's count, against the limits)

- steps_per_round: 17 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 17 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 40 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
