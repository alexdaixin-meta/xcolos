# Variation: Break the Code: Coarse Clues

Two players each hide three different digits and, over four rounds per leg, ask coarse yes-ish questions about the opponent's digits. They decide when to risk a guess. Cracking early scores well, guessing wrong feeds the opponent, and a code that survives the leg scores for its owner.

Players: 2 to 2, best with 2

## Review of the original

Break the Code is a deduction game. Players hide sorted number tiles behind screens and take turns asking public question cards (sums, positions of numbers, colour adjacencies and the like) that opponents must answer truthfully. The first to name a hidden code exactly wins.

- **non_degenerate**: good. No simple policy wins. Always guessing immediately is almost always wrong. Never guessing cannot win in 2-player. Turn order gives the first asker a small tempo edge, but the 2-player rule that gives the opponent one final guess after a correct guess mostly removes it.
- **skill_sensitive**: good. Choosing which face-up card extracts the most information, and combining answers into a consistent tile set, is a real skill. Better deducers solve in fewer questions. Luck enters through which six cards are face up and the deal.
- **headroom**: good. Card selection can always be sharpened toward the expected-information optimum, and guess timing under residual uncertainty is open-ended. A weak player still extracts some information and can eventually guess.
- **reasoning_dependent**: good. The whole game is inference from limited answers about a hidden arrangement. With 3-4 players, answers given to others are also clues.
- **verifiable**: good. Answers and guess checks are mechanical comparisons against the hidden tiles. No judgement is needed.
- **fits_platform**: weak. It is text-friendly and turn-based, but 21 distinct card types, a 20-tile shuffled deal, colour-tie sorting, a central pool and once-per-game secret peeks far exceed the step, attribute and draw limits. It must be cut down. The previous cut-down variation also failed: its 'solved' flag was ambiguous, and three of its cards (sum, middle digit, range) always identified a code, so competent play became a fixed 2-2 per leg.

## Problems

- P1 (previous variation): 'solved' had no owner, so it could be read as one shared flag that locks the second player out. It was also unstated whether both players score when both guess right in the same round.
- P2 (previous variation): cards 1, 4 and 5 (sum, middle digit, range) identified any code with certainty by leg-round 3. Every competent leg ended 2-2, and decisive results came only from expected-value-neutral 50/50 gambles. This is the lottery trap.
- P3 (previous variation): there was almost no interaction. A player's code choice did not affect their own score, and the attack was a fixed three-card recipe, so opponent modelling and code choice barely mattered.
- P4 (previous variation): the per-leg once-only card restriction cost an attribute or bitmask per player and added parsing for no strategic gain.
- P5 (original): the full game's 21 card types, tile deal, colours and central pool exceed the platform's limits, so a compact numeric version is required.

## Changes

- Every per-player state value is written with an owner: 'that player's solved', 'that player's guesses left'. A rule states that both players are scored independently, so both can solve in the same leg, even in the same round. (fixes: P1 (previous variation): 'solved' had no owner): Removes the shared-flag reading and the same-round ambiguity.
- The card set is replaced with six coarse cards, each with at most 4 possible answers: count of digits 5 or higher, count of odd digits, count of primes (2, 3, 5, 7), count of multiples of 3 (0, 3, 6, 9), count of consecutive neighbouring pairs, and sum mod 4. There are 120 possible codes. Any plan of 3 asks, even an adaptive one, has at most 4×4×4 = 64 answer paths, so at least 56 codes cannot be pinned down by leg-round 3 under any asking plan. Even after 4 asks a code may remain ambiguous. (fixes: P2 (previous variation): cards 1, 4 and 5 identified any code with certainty): No recipe guarantees a solve. Players must choose cards adaptively for information, judge how many candidates remain, and decide when a guess is worth its risk.
- A wrong guess now gives -1 to the guesser and +1 to the code's owner, a swing of 2. An owner whose code is not cracked by the end of the leg scores +1. A correct guess scores 5 - leg-round as before. (fixes: P3 (previous variation): almost no interaction): Code choice now pays directly: an ambiguous code earns points by luring wrong guesses and surviving. Guess timing becomes a real expected-value calculation that depends on the remaining candidates and on the opponent's visible progress. For example, with 2 candidates at leg-round 3 a guess is worth +0.5 over waiting, while at leg-round 4 it is worth -0.5. Players also model which codes the opponent is likely to hide.
- Repeat asks are allowed and simply return the same answer. (fixes: P4 (previous variation): the once-only card restriction cost state for no gain): Saves the used-card attribute and parsing. A repeat is just a wasted ask, which is its own penalty.
- The game is kept as 2 players, 3 legs of 4 rounds, a 3-digit sorted numeric code, simultaneous asks and guesses, and arithmetic card answers. (fixes: P5 (original): the full game exceeds the platform's limits): Fits within 16 steps, 3 choice steps, 18 attributes, 1 hidden element and 0 random draws.

## Kept from the original

- A hidden sorted code made of distinct digits, like the sorted tiles behind the screen
- Asking question cards that must be answered truthfully by arithmetic on the hidden code
- Guessing the exact code, with a cost for wrong guesses and a reward for early correct ones
- The race to deduce the opponent's code before they deduce yours

## The variation's rules

R1. Structure. Two players play a match of 12 rounds, split into 3 legs of 4 rounds each. Legs start at rounds 1, 5 and 9. The round counter starts at 0 and increases by exactly 1 at the very start of each round; nothing else changes it. Leg-round = ((round - 1) mod 4) + 1, so it runs 1, 2, 3, 4 within each leg.

R2. Player state. Each player has their own: score, wrong count, code, guesses left, solved, card asked, answer and guess. Score and wrong count start at 0 and carry over between legs. Both players are always handled separately: one player's result never blocks or changes the other's, except where a rule says the code's owner scores.

R3. New leg. When leg-round is 1, first reset each player's own guesses left to 2 and each player's own solved to 0. Then both players secretly and at the same time enter a code as a number, for example 147, 852, or 12 (meaning 0-1-2). In other rounds there is no code prompt and codes stay unchanged.

R4. Parsing a code. Read the entry x as digits A = floor(x / 100), B = floor(x / 10) mod 10 and C = x mod 10. If x is a whole number from 0 to 999 and A, B and C are all different, sort them ascending as a < b < c and store 100*a + 10*b + c. For example, 852 is stored as 258.

R5. Invalid code. Any other entry is stored as code 12 (digits 0, 1, 2). This covers repeated digits, out-of-range or non-numeric entries, and missing or declined entries.

R6. Asking. Every round, both players at the same time may pick one card number from 1 to 6 to ask about the opponent's code. Declining or giving an invalid number means no question this round. A card may be asked again; it gives the same answer. With the opponent's sorted digits a < b < c, the answers are:
- Card 1, High: how many of the three digits are 5 or higher (0-3).
- Card 2, Odd: how many of the digits are odd (0-3).
- Card 3, Prime: how many of the digits are 2, 3, 5 or 7 (0-3).
- Card 4, Threes: how many of the digits are 0, 3, 6 or 9 (0-3).
- Card 5, Chain: (1 if b - a = 1 else 0) + (1 if c - b = 1 else 0) (0-2).
- Card 6, Sum mod 4: (a + b + c) mod 4 (0-3).
Each answer is shown privately to the player who asked. Then both players are told which card number (or none) each player asked.

R7. Guessing. Then both players at the same time may enter a guess of the opponent's code. A player is prompted only if that player's own guesses left is above 0 and that player's own solved is 0. The guess is parsed as in R4.
- Pass: declining, or an entry that does not give three different digits from 0 to 999. A pass costs nothing.
- Correct: a valid guess equal to the opponent's stored code. The guesser scores 5 - leg-round, that is 4, 3, 2 or 1. That player's own solved becomes 1 for the rest of the leg.
- Wrong: any other valid guess. The guesser scores -1, their wrong count increases by 1, and their guesses left decreases by 1. The opponent, the code's owner, scores +1.
If both players guess correctly in the same round, both score.

R8. Results. After guessing, both players are told whether each player passed, guessed right or guessed wrong. Codes are not shown.

R9. End of leg. When leg-round is 4, after R8, each player whose own code was not guessed correctly during this leg scores +1. That is, a player scores +1 if the opponent's solved is still 0. Then both codes are revealed to both players.

R10. End. The game ends after round 12.

Objective: After round 12, the player with the higher total score wins. If the totals are equal, the player with fewer wrong guesses wins. If those are also equal, the game is a draw.

Expected effect: No asking plan can guarantee a solve before leg-round 4: three asks give at most 64 answer patterns for 120 codes. Players must therefore pick cards adaptively, count the remaining candidates, and weigh guessing now (more points, but each miss is a swing of 2 to the opponent) against waiting, which risks scoring little and conceding the +1 for an uncracked code. Code choice becomes a hide-and-seek against the opponent's likely asking plan: pick codes that share answer patterns with many others, and avoid ones a strong asker isolates quickly. Seeing which cards the opponent asked and whether they guessed lets a player estimate the opponent's progress. Every simple policy can lose. Always passing earns at most +1 per leg and loses to any player who cracks at least once without reckless misses. Always guessing bleeds swings of 2. Both always passing is a 3-3 draw. Some residual chance remains when a guess must be made among 2-3 candidates. Better card choice shrinks the candidate count, and expected-value-aware timing uses it, so the stronger reasoner should win most matches. There is no talk phase: it is a 2-player zero-sum contest with nothing to negotiate.

## Complexity (the designer's count, against the limits)

- steps_per_round: 16 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 18 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 12 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
