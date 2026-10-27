# Variation: Break the Code: Duel of Two Tiles

Two players each set a secret two-tile code. Over four legs of six simultaneous turns, each player either asks one of five truthful questions about the opponent's code or guesses it. A correct guess earlier in the leg scores more.

Players: 2 to 2, best with 2

## Review of the original

Break the Code is a deduction game. Each player hides a sorted row of numbered, coloured tiles. On a turn a player either asks one of six face-up question cards, which opponents must answer truthfully, or tries to name a hidden code exactly; the first correct full guess wins.

- **non_degenerate**: weak. The original has no dominant simple policy: never guessing cannot win, and guessing blind almost never succeeds. Seat order matters, though. The first player to guess correctly wins, and the 2-player rule that gives the opponent one last guess only partly offsets that. The previous scored variation degenerated completely. Always-first and always-last won 60 of 60 matches from either seat, because random play lost points on wrong guesses while the passive policies never risked anything.
- **skill_sensitive**: good. In the original, choosing questions that split the remaining possibilities well, and knowing when to commit to a guess, beats asking at random. The shuffled question cards add some luck: one player may be offered sharper cards than the other.
- **headroom**: good. Adaptive question choice and judging how risky a guess is leave plenty of room to improve. A weak player still eventually narrows the code down.
- **reasoning_dependent**: good. The core of the game is inference about a hidden code from partial, truthful answers. In the original there is no opponent modelling, because codes are dealt at random.
- **verifiable**: good. Every answer to a question card is a mechanical fact about the hidden tiles, and a guess is either exactly right or not.
- **fits_platform**: weak. The game is text and turn-based, but it has some awkward features. There are 21 different question cards with varied answer formats such as positions and adjacency. A 20-tile deal and a 21-card deck need many draws. The code space of 5 tiles from 20 is large, so games run long. The 3-4 player central-pool and elimination rules add a second hidden structure.

## Problems

- P1: In the previous variation, wrong guesses cost points or handed points to the code's owner, so random play lost by self-destruction and any never-guessing policy (first or last option) won every match.
- P2: There was a reward for an unsolved leg (or no price on passing), so not guessing was a safe way to bank the result.
- P3: The code space was too large to deduce within a leg, so careful play rarely reached a guess and the result came from the opponent's mistakes, not one's own deduction.
- P4: Codes were dealt at random, so nothing could be learned about the opponent. There was no opponent modelling, and the deal could favour a player.
- P5: Turn order gives the first guesser an edge, and the original's many card types, deck draws and position-based answers exceed what the engine builds reliably.
- P6: Under highest-total-wins, a wrong guess that gave no information was pure loss, so the guess-or-ask tension disappeared.

## Changes

- A wrong guess costs no points and gives the guessed code's owner nothing. Its only cost is the turn, and it still returns a little information (whether the guess shares a tile with the code). (fixes: P1): Guessing must never be self-destructive. Random play then no longer feeds points to passive players, and an informed early guess becomes a real option.
- Points come only from correct guesses: 7 minus the turn number within the leg (6 down to 1). Nothing is scored for an unsolved leg. (fixes: P2): Passivity scores zero, so an always-ask policy loses to anyone who ever guesses right. Guessing earlier pays more, so committing under uncertainty is rewarded.
- The code shrinks to two tiles valued 0-5, sorted low-high (21 possible codes). There are five fixed coarse questions with three possible answers each, and a leg lasts 6 turns. (fixes: P3): A code can now be pinned down in about three good questions, so deduction decides the leg. Each answer has only three values, so one cannot solve a code in two questions and guessing at turn 3 versus turn 4 is a real gamble.
- Each player chooses their own secret code at the start of every leg instead of having it dealt. (fixes: P4): This adds opponent modelling. Setters try to pick codes that stay ambiguous under the questions, and guessers can exploit an opponent's habits over four legs. It also removes deal luck and the need for random draws.
- Both players act simultaneously each turn, using the same fixed menu of questions. Answers are announced publicly. Draws and discards are removed. (fixes: P5): Simultaneous play removes the seat advantage. A fixed menu keeps the step count and attributes within the platform's limits.
- A wrong guess reveals whether 0 or 1 of the guessed tiles appear in the code. (fixes: P6): A guess becomes a weak question as well as a gamble. Choosing between a sharp question and a rewarding but risky guess is then a real decision.
- The winner is the higher total after 4 legs. If totals are tied, the player who solved more legs wins; if that is also tied, the match is a draw. (fixes: P1): The winner rule is simple arithmetic. The only way to gain on the opponent is to solve faster, so risk-free passivity cannot win.

## Kept from the original

- A hidden code of numbered tiles, kept in ascending order
- Truthful answers to question cards about properties of the code (sums, odd tiles, gaps, high tiles)
- Each turn, the choice between asking a question and attempting a full guess
- Winning by naming the opponent's exact code sooner than they name yours

## The variation's rules

SETUP. The match is 4 legs of 6 turns each (24 turns). Scores start at 0.

CODES. At the start of each leg, both players at the same moment secretly choose a code of two tiles. Each tile is a whole number from 0 to 5. A code is written low tile then high tile, with low no greater than high; equal tiles are allowed, for example 3-3. There are 21 possible codes. A code cannot be changed during the leg.

TURNS. On each turn of a leg, both players choose at the same moment. Each picks exactly one of the following actions, about the opponent's code:
- Question A (Sum): is the sum of the two tiles LOW (0-3), MIDDLE (4-6) or HIGH (7-10)?
- Question B (Odd): how many tiles are odd: 0, 1 or 2?
- Question C (Gap): is high minus low 0 (PAIR), 1 (ADJACENT) or 2 or more (APART)?
- Question D (Big): how many tiles are 3 or more: 0, 1 or 2?
- Question E (Edge): how many tiles are 0 or 5: 0, 1 or 2?
- Guess: name a full code (low, high).
Repeating a question is allowed, but it gives the same answer again.

ANSWERS. After both have chosen, the engine announces to both players each player's action and its truthful answer, computed from the opponent's code.
- If a guess equals the opponent's code exactly, it is CORRECT. The guesser scores 7 minus the turn number within the leg: 6 points on turn 1, 5 on turn 2, 4 on turn 3, 3 on turn 4, 2 on turn 5 and 1 on turn 6.
- If a guess is wrong, it scores 0 and costs nothing else. The engine announces how many of the guessed tiles appear in the code, which is 0 or 1. Each code tile can match at most one guessed tile.

SOLVED. A player who guesses correctly has solved the leg. For the rest of that leg their choices are ignored and they score nothing more. The other player keeps playing normally.

END OF LEG. After turn 6 of a leg, both codes are revealed to both players. Unsolved legs score nothing for anyone. The next leg starts with new codes.

END OF MATCH. After 4 legs the match ends.

Objective: After 4 legs, the player with the higher total score wins. If totals are equal, the player who solved more legs wins. If that is also equal, the match is a draw.

Expected effect: Never guessing scores zero and loses to any player who guesses right even once, including a random player who stumbles onto a code. Fixed guessing, such as always naming 0-0 or 5-5, scores only when the opponent happens to set that code, so it also loses. Strong play asks the question that best splits the remaining codes given earlier answers. It then decides whether to gamble a guess on turn 3 among two or three candidates for 4 points, or to ask once more and guess safely on turn 4 for 3 points. Setters choose codes that stay ambiguous under the five questions and vary them so the opponent cannot exploit a habit. Guessers break near-ties by reading the opponent's past code choices, revealed at the end of each leg. Play is simultaneous and the rules are symmetric, so no seat has an edge. There is no random deal, so the result reflects deduction, risk judgement and opponent modelling. Talk is omitted: there are only two players, and every statement would be cheap talk about a code.

## Complexity (the designer's count, against the limits)

- steps_per_round: 11 (limit 20)
- choice_steps_per_round: 2 (limit 4)
- attributes: 15 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 24 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
