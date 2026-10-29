# Reasoning and planning: Break the Code: Duel of Two Tiles

**Verdict: adequate.** Winning rewards correct deduction, choosing guesses whose feedback separates the remaining codes, and modelling the opponent's code and question habits, so reasoning matters a lot. Because many legs end in coin flips among two or three equally likely codes and margins are tiny, chance weighs heavily; larger code spaces, or questions that leave fewer exact ties, would make planning and inference count for more.

From 3 play(s): 115 choices, 115 with a reason given (about 67.1 words each); results {'seats 1 and 2': 1, 'seat 1': 1, 'seat 2': 1}.

## Reasoning: 3 of 3

Nearly every guess rests on correct deduction of the candidate set, including the parity trick (one odd tile forces sum 5) and reading tile-match feedback to eliminate codes. Players also compute expected values and model the opponent: mirroring, the gap-3 code pattern, and question habits that guide code choice.

- match 1, turn 7, seat 1: "If it is wrong, the feedback still tells the other two apart: 2-2 would answer 0 and 2-4 would answer 1. That makes next turn's guess certain, worth 3 points." (Picks the one guess whose wrong-answer feedback separates the other two candidates.)
- match 1, turn 26, seat 2: "One odd tile means the sum is odd, so the sum must be 5. That leaves three codes: **0-5, 1-4 or 2-3**." (Correct parity inference narrows the set, then weighs guessing now against asking first.)
- match 3, turn 40, seat 1: "So the code is 0-4. The only other code with a 0 is 0-0, and that would have given 0 matching for 3-4." (Chains several tile-match results into a unique solution and checks the one alternative.)
- match 2, turn 20, seat 1: "The opponent's codes have kept a gap of 3: 1-4 in leg 1, then 2-5 in leg 2. If they shift up again with wrap-around, the next code is 0-3." (Reads the opponent's revealed codes to make a turn-1 guess, which paid 6 points.)

## Planning: 2 of 3

Players routinely plan two turns ahead: they choose turn-3 guesses that guarantee a turn-4 solve, and they set codes to survive the opponent's known sum-then-odd routine. Endgame timing is worked out against the opponent's likely solve, though the 6-turn legs keep the horizon short.

- match 1, turn 10, seat 1: "My opponent's habit is to ask sum, then odd, then guess. No code leaves more than 3 candidates after those two questions. 3-4 gives a HIGH sum and one odd tile, which is shared with 2-5 and 4-5." (Code choice is planned against the opponent's expected question sequence.)
- match 3, turn 41, seat 2: "If I guess correctly now, I reach 12 and win. If I wait a turn, the best I can do is 11, which is a draw. So I take the 50/50 now." (Times the guess by projecting the opponent's next-turn solve and the final standings.)
- match 3, turn 32, seat 1: "In leg 1 they tried 2-3 and then 1-4 from this same group, so 0-5 is likely to be their last try." (Sets a code expecting the opponent's guess order within the final candidate group.)

## Luck: 2 of 3

After two questions, legs routinely come down to a 1-in-2 or 1-in-3 guess. Matches were decided by 1 to 4 points, and match 2 was largely decided by speculative early guesses that happened to hit.

- match 1, turn 17, seat 2: "Guessing now is better, and either code is an equal pick." (The decisive point gain was a pure coin flip between equally likely candidates.)
- match 2, turn 15, seat 1: "favour 2-5. They copied my code in leg 1, and on turn 1 here they guessed 2-5, maybe their own code. That makes 2-5 more likely than 1 in 10." (A 5-point swing came from a read with low odds that happened to land.)

## Weak spots

- match 3, turn 35, seat 2: Claimed 'Every question splits the 21 possible codes about equally (6 / 9 / 6)', which is false for gap and edge. Sum was still a fine choice, but the stated reasoning was wrong.
- match 3, turn 19, seat 2: Guessed 1-3 on a mirroring hunch instead of 3-3, whose wrong-answer feedback would have guaranteed a turn-4 solve. The ~60% likelihood given to 1-3 was speculative, so the guess that separates the other codes was the better-reasoned option.
- match 3, turn 26, seat 1: Asserted that 'Guessing a code right now also averages about 3.5' with six candidates left, which overstates the value of a 1-in-6 guess. Asking gap was still correct.
- match 2, turn 32, seat 2: Took a 1-in-8 blind guess on the claim that only a turn-3 solve could still win. Asking a question first kept a larger chance of solving, and a later solve might still have helped if seat 1 stalled.
