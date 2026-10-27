# Variation: Break the Code: Three-Leg Duel

Two players each hide a 3-digit code and race to deduce the other's using 4 of 6 question cards per leg. Earlier correct guesses score more and wrong guesses cost a point, over 3 legs with fresh codes.

Players: 2 to 2, best with 2

## Review of the original

Break the Code is a deduction game. Players hide sorted number tiles and take turns asking face-up question cards that opponents must answer truthfully, then try to guess the hidden tiles exactly. The previously tested 2-player 'Duel' version reduced it to two secret 3-digit codes, six fixed question cards asked simultaneously, and a first-to-guess-correctly race over 6 rounds.

- **non_degenerate**: weak. In the tested Duel, no simple policy wins outright. Always-pass only draws, and blind early guessing (1/120) loses. But 'must use every card exactly once' makes question order nearly irrelevant by round 6. If both players pick codes from large ambiguity classes and wait for the full profile, the game draws. A simple wait-and-guess policy cannot lose against a strong player, so the interesting choices do not move the result.
- **skill_sensitive**: weak. Between competent players most games draw (same-round correct guesses, or nobody correct). Most decisive games turn on a blind 1/2 or 1/3 pick between indistinguishable candidates. Luck therefore decides more than half of decisive outcomes, and the better reasoner is not reliably favoured.
- **headroom**: weak. With all six cards forced and a binary race, the decisions are thin. A weak player still draws often, and a strong player has little way to convert better deduction or code choice into a win.
- **reasoning_dependent**: good. The hidden code is real hidden state: 120 candidates narrowed by known functions. Choosing a code that resists identification is opponent modelling, and choosing which card to ask next is planning.
- **verifiable**: good. Every answer and every guess check is arithmetic on stored codes. No judge is needed.
- **fits_platform**: weak. The game is text-only, turn-based and short. It failed playability on three counts. There were no defaults for an invalid or reused card, an illegal guess, or an illegal code. The attribute encoding was unstated: separate digit and card flags exceed 20 attributes. The step count for answer arithmetic was unclear.

## Problems

- P1: Most games between competent players are draws (both correct in the same round, or neither correct), so the result rarely reflects skill.
- P2: Decisive games are mostly settled by blind 1/2 or 1/3 guesses between indistinguishable candidates: luck among equals.
- P3: 'Use every card exactly once' removes card selection as a decision, and both players end with the same information at the same time.
- P4: A single code per match gives one luck-heavy sample, no chance to learn an opponent's code-choice habits, and no reward for efficient deduction beyond tying.
- P5: No rule for naming an invalid or already-used card.
- P6: No rule for an illegal guess (repeated digits, out of range, unsorted) or for guessing with no guesses left.
- P7: No rule for an illegal secret code at setup.
- P8: Attribute and step encoding was unstated and, done naively (separate digits, six card flags per player), exceeds the 20-attribute limit.

## Changes

- Replace the first-correct-wins race with points. In each leg, a correct guess scores 4, 3, 2 or 1 points in leg-round 1, 2, 3 or 4. A wrong guess costs 1 point. The leg does not stop when one player is correct; the other can still score less by guessing later. The higher match total wins. (fixes: P1): Same-round ties now depend on how early each player committed. A player who solves in leg-round 2 beats one who solves in leg-round 3. When to guess among k candidates becomes an expected-value decision, not a coin toss with nothing at stake.
- Play 3 legs of 4 rounds each (12 rounds). Each leg uses fresh secret codes, and both codes are revealed at the end of each leg. (fixes: P2): Three independent legs average out the luck of a final 1/2 pick. Revealing codes lets players learn and exploit each other's code-choice habits in later legs.
- Each leg has only 4 ask rounds, so each player uses 4 of the 6 cards. A card cannot be repeated within a leg; all cards become available again next leg. (fixes: P3): Which 4 cards to ask, and in which order given earlier answers, becomes a real adaptive planning decision. The two players reach different information at different speeds.
- Same leg structure as above, with code choice repeated at the start of every leg. (fixes: P4): Gives multiple deduction samples and repeated code-choice duels, where opponent modelling can pay off.
- Card default: a missing, invalid or already-used card number is replaced by the lowest-numbered card that player has not used this leg. (fixes: P5): Every ask resolves deterministically.
- Guess defaults:
- Three different digits 0-9 written in any order are sorted ascending and accepted.
- Anything else (repeats, wrong length, non-digits, blank) counts as a pass and costs nothing.
- A guess written with no guesses left, or after already guessing correctly this leg, counts as a pass and costs nothing. (fixes: P6): Every guess resolves deterministically.
- Code default: three different digits in any order are sorted. Any other entry becomes 0-1-2. This code is identifiable from the SUM card alone, which is a natural penalty. (fixes: P7): Setup always produces a legal code.
- Store each code as one number 100A+10B+C and each guess the same way. Store used cards as one bitmask per player (card n adds 2^(n-1)). Compute each answer in a single calculation step per player. (fixes: P8): Keeps the game at 17 attributes and 13 steps.
- Tie-break: if totals are equal, the player with fewer wrong guesses over the match wins. Otherwise it is a draw. (fixes: P1): Turns remaining ties into results that reward careful play.

## Kept from the original

- Secret sorted number codes that each player hides from the other
- Question cards that must be answered truthfully with a computed fact about the opponent's code
- Exact full-code guesses, with a limited number of attempts and wrong guesses penalised
- The race to deduce faster than your opponent while choosing a code that is hard to deduce

## The variation's rules

OVERVIEW. Two players. The match has 3 legs of 4 rounds each (12 rounds in total). Leg 1 is rounds 1-4, leg 2 is rounds 5-8, leg 3 is rounds 9-12. The leg-round is 1, 2, 3 or 4 within each leg. Scores start at 0 and carry across legs.

CODES. A code is three different digits from 0 to 9, kept smallest first as A < B < C. Example: 2-5-8.

THE SIX QUESTION CARDS. Each answer is one number computed from the opponent's current code A < B < C.
1 SUM: A + B + C.
2 EVENS: how many of the three digits are even (0 counts as even).
3 RANGE: C - A.
4 HIGH: how many of the three digits are 5 or more.
5 STEPS: how many of the pairs (A,B) and (B,C) differ by exactly 1 (0, 1 or 2).
6 THREES: how many of the three digits are in {0, 3, 6, 9}.

EACH ROUND:

Step 1. Code choice (leg-round 1 only, i.e. rounds 1, 5, 9).
- Both players simultaneously and secretly write a code.
- Three different digits written in any order are sorted ascending and become that player's code for this leg.
- Any other entry (repeated digits, wrong count, non-digits, blank) becomes the code 0-1-2.
- Only the engine knows the codes.
- Each player's guesses for the leg are set to 2, their solved flag to no, and their used cards to none.

Step 2. Ask. Both players simultaneously and secretly name one card number (1-6) they have not used in this leg.
- If a player names nothing, an invalid number, or a card already used this leg, they are given the lowest-numbered card they have not used this leg.
- The card becomes used for that player until the leg ends.
- Each player uses exactly 4 different cards per leg; all six are available again at the start of the next leg.

Step 3. Answer. The engine computes each player's card from the opponent's code. It announces to both players which card each player asked and the answer.

Step 4. Guess. Both players simultaneously either pass or write a code guess.
- A guess of three different digits in any order is sorted ascending.
- Any other entry counts as a pass.
- A guess written by a player with 0 guesses left, or who has already guessed correctly this leg, counts as a pass.
- A pass costs nothing.
- A valid guess uses up 1 of that player's guesses for the leg.

Step 5. Check. Each valid guess is compared with the opponent's code.
- Correct (all three digits match): the guesser scores 5 minus the leg-round, so 4 points in leg-round 1, 3 in leg-round 2, 2 in leg-round 3, 1 in leg-round 4. The guesser is marked solved for the rest of the leg and makes no further guesses that leg.
- Wrong: the guesser loses 1 point and also gains 1 to their wrong-guess count.
- Every guess and its result (correct or wrong) is announced to both players.
- One player guessing correctly does not end the leg for the other player, who may keep asking and guessing.

Step 6. Leg end (leg-round 4 only, i.e. rounds 4, 8, 12). Both codes are revealed to both players, and the current scores are announced.

Step 7. End check. After round 12 the match ends.

ENGINE ENCODING (for builders):
- Per player: score, wrong_count, guesses_left, solved (0/1), used_mask, code (100A+10B+C), ask, answer, guess (100A+10B+C, or 0 for a pass).
- Plus one table attribute: round.
- Total: 17 attributes.
- Leg-round is ((round - 1) mod 4) + 1.
- Digits of a code are A = floor(code/100), B = floor(code/10) mod 10, C = code mod 10.
- Card n is used if floor(used_mask / 2^(n-1)) mod 2 = 1.

Objective: After round 12, the player with the higher total score wins. If the totals are equal, the player with fewer wrong guesses over the whole match wins. If that is also equal, the match is a draw.

Expected effect: Speed of deduction now separates players even when both eventually solve. Solving in leg-round 2 instead of 3 is worth a point, so ties are rarer.

Choosing 4 of 6 cards adaptively rewards picking the most informative next question given earlier answers. Codes with extreme sums (such as 0-1-2 or 7-8-9) become easy targets, so code choice becomes a reasoned bet on which cards the opponent will ask.

Guessing becomes an expected-value decision. With 2 candidates left in leg-round 3, guessing now (2 points, 50%, -1 if wrong) competes with waiting for a 4th card that may settle it for 1 point. Remaining 1/2 picks are spread over 3 legs, so luck averages down.

Revealed codes let players model each other's code-choice habits across legs.

Simple policies all lose to good play:
- Always pass scores 0 and loses to any positive score.
- Blind early guessing averages about -2 per leg.
- Always asking cards in fixed order loses speed to adaptive asking.
- Always waiting until leg-round 4 caps at 1 point per leg and loses to a player who solves earlier.

Talk is omitted: two players with directly opposed interests and nothing to coordinate.

## Complexity (the designer's count, against the limits)

- steps_per_round: 13 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 17 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 12 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
