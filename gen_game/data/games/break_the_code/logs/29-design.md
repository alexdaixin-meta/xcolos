# 29 design

- time: 2026-10-27T18:59:10+00:00 (95.4s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 6603ed0c123d06d1, reply sha256 2cc28592d5013a73

## Sent

````
Original game: Break the Code
Players in the original: 2 to 4

Original rules:
Each player hides 5 tiles (4 in 4-player) behind a screen, sorted ascending, red before blue for same number. 20 tiles containing numbers 0-9 in two colors are shuffled and dealt. 21 question cards are shuffled; six are face up. On your turn you must either ask one face-up question card or attempt to guess. If you ask, your opponent(s) must answer truthfully according to the card (e.g., where is a number, where are same colors adjacent, where are sequential numbers). Asked cards are discarded and replaced from the deck. In 2-player you guess opponent's 5 tiles in order; if wrong you continue, if right you win but opponent gets one final guess chance, otherwise tie if deck runs out. In 3-4 players there is a central pool of 4-5 hidden tiles; players ask and all opponents answer (all shared in 4-player), and any player may once per game secretly check and claim the central tiles; wrong guess eliminates you from asking.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- playable FAILED: Limits: 12 rounds (max 40), 3 choice steps (max 4), 1 hidden element (max 3), 0 random draws, 18 attributes (max 20). Parsing uses floor and mod. Sorting works as min, max and sum minus min minus max. Card answers are arithmetic with `if`. No board, clock, judge or trade is needed. Talk is correctly absent: it is a 2-player game with nothing to negotiate.

The game is finite and decided by arithmetic.

A real ambiguity remains in 'solved'. R3 resets 'guesses left' per player ('each player's guesses left = 2') but writes 'solved = 0' with no owner. R7 says 'solved becomes 1 for the rest of the leg' and gates the guess prompt on 'solved = 0'. If 'solved' is one shared flag, the first player to solve locks the other out of guessing. That changes the whole leg: it becomes a race in which a +2 at round 3 can deny the opponent anything. If it is per-player, both can solve. A model with only these words cannot tell which applies. It is also unstated whether both players score when both guess right in the same round.

Minor: 13 steps per round looks tight for 2 parses, 2 sorts, 12 conditional card answers and 2 guess resolutions. It is feasible only if several operations share a step.

This fails on the 'solved' ambiguity.
- reasoning_over_luck FAILED: There are no random draws, so luck comes from guessing among candidates. The key fact is that cards 1, 4 and 5 identify ANY code with certainty: b from card 4, a + c = sum - b, c - a from card 5. Any competent player is therefore guaranteed +2 per leg by round 3, a 6-6 baseline over 12 rounds.

The only way to beat it is an early guess. A round-2 guess with k candidates left is worth 3/k + ((k-1)/k)(-1+2), which equals 3/k + (k-1)/k. Against the safe 2 points:
| k | 1 | 2 | 3 | 4 |
| EV | 3 | 2 | 1.67 | 1.5 |
So a gamble pays only when k = 1. Otherwise it is break-even (k = 2, a pure 50/50 between +3 and +1) or worse.

When every player follows the intended good strategy, both pick codes that stay ambiguous after any first card and adaptive second card, and both run the certain line. Every leg ends 2-2 and the match is a draw. Any decisive result comes from EV-neutral coin-flip gambles at k = 2, so chance, not reasoning, separates good players.

Opponent modelling is minimal. There is no interaction except code choice, and the attack is a fixed formula. Inference exists, but it is solved by a three-card recipe, so a strong reasoner is not clearly favoured over one who has learned the recipe.
- change: Make 'solved' explicitly per player ('each player's solved = 0'; 'that player's solved becomes 1'). State that both players score if both guess correctly in the same round.
- change: Remove the guaranteed solve. For example, drop card 4 (or card 5) so that no fixed set of three cards always identifies a code. Or use 4-digit codes (210 possibilities) with at most 3 asks per leg, so that leg-round-4 guesses still face several candidates.
- change: Add interaction so code choice and opponent modelling matter. For example: the defender scores +1 whenever the attacker guesses wrong on their code, and the first player to solve in a leg (strictly earlier round) gets a +1 bonus. This makes the timing of guesses depend on predicting the opponent's progress, which is visible through the public card and guess results.
- change: Re-check that under the revised rules, play by two competent players does not reduce to a fixed 2-2 per leg with outcomes decided only by 50/50 guesses.
The variation that was reviewed: Break the Code: Three Digits: R1. Structure. The match has 12 rounds in 3 legs of 4 rounds each (legs start at rounds 1, 5 and 9). Leg-round = ((round - 1) mod 4) + 1. The round counter starts at 0 and is increased by exactly 1 at the very start of each round; nothing else changes it.

R2. Scores. Scores and wrong-guess counts start at 0 and carry across legs. They change only as described in R7.

R3. Writing codes. When leg-round is 1 (rounds 1, 5, 9), first reset for the new leg:
- each player's guesses left = 2;
- solved = 0;
- used cards = none.
Then both players secretly and at the same time enter a code as a number, such as 147, 852 or 12 (meaning 0-1-2). In any other round there is no code prompt and codes stay as they are.

R4. Parsing a code. Read the entry x as digits A = floor(x/100), B = floor(x/10) mod 10, C = x mod 10. If 0 <= x <= 999 and A, B and C are all different, sort them ascending and store 100*first + 10*second + third. For example, 852 is stored as 258.

R5. Invalid code. Any other entry becomes code 12 (digits 0, 1, 2). This covers repeated digits (552, 7 = 007), out of range, non-numeric, missing or declined.

R6. Asking. Each round, after any code step, both players at the same time may pick one question card number 1-6 to ask about the opponent's code. Declining, an invalid number, or a card that player has already asked this leg means no question this round. Each player may ask each card at most once per leg. With the opponent's sorted digits a < b < c, the answers are:
- Card 1: a + b + c.
- Card 2: how many of the digits are 5 or higher.
- Card 3: how many of the digits are odd.
- Card 4: the middle digit b.
- Card 5: c - a.
- Card 6: how many neighbouring pairs are consecutive numbers, (1 if b - a = 1 else 0) + (1 if c - b = 1 else 0).
The answer is shown privately to the asker only. Both players are then told which card number (or none) each player asked.

R7. Guessing. Then both players at the same time may enter a guess of the opponent's code. The guess prompt is given only to a player who has guesses left above 0 and solved = 0 this leg. The guess is parsed like a code (R4): three different digits, sorted.
- Pass: declining, entering 0, or an entry without three different digits counts as a pass and costs nothing.
- Correct: a valid guess equal to the opponent's stored code. The player scores 5 - leg-round (4, 3, 2 or 1) and solved becomes 1 for the rest of the leg. For example, guessing 12 or 012 matches code 12.
- Wrong: any other valid guess. The player scores -1, and their wrong count and guesses left change by +1 and -1 respectively.

R8. Results. After guessing, both players are told whether each player passed, guessed right or guessed wrong; codes are not revealed. Codes are revealed at the end of each leg (after rounds 4, 8 and 12).

R9. End. After round 12 the game ends. Winner: After round 12, the player with the higher total score wins. If the totals are equal, the player with fewer wrong guesses wins. If both are still equal, it is a draw (shared win). For example, if nobody ever guesses it is 0-0 with 0 wrong guesses each: a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Break the Code is a deduction game. Players hide sorted number tiles behind screens and take turns asking public question cards (sums, positions of numbers, colour adjacencies and the like) that opponents must answer truthfully. The first to name a hidden code exactly wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No simple policy wins. Always guessing immediately is almost always wrong. Never guessing cannot win in 2-player. Turn order gives the first asker a small tempo edge, but the 2-player rule that gives the opponent one final guess after a correct guess mostly removes it."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "Choosing which face-up card extracts the most information, and combining answers into a consistent tile set, is a real skill. Better deducers solve in fewer questions. Luck enters through which six cards are face up and the deal."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Card selection can always be sharpened toward the expected-information optimum, and guess timing under residual uncertainty is open-ended. A weak player still extracts some information and can eventually guess."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "The whole game is inference from limited answers about a hidden arrangement. With 3-4 players, answers given to others are also clues."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Answers and guess checks are mechanical comparisons against the hidden tiles. No judgement is needed."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "It is text-friendly and turn-based, but 21 distinct card types, a 20-tile shuffled deal, colour-tie sorting, a central pool and once-per-game secret peeks far exceed the step, attribute and draw limits. It must be cut down. The previous cut-down variation also failed: its 'solved' flag was ambiguous, and three of its cards (sum, middle digit, range) always identified a code, so competent play became a fixed 2-2 per leg."
    }
  ],
  "problems": [
    "P1 (previous variation): 'solved' had no owner, so it could be read as one shared flag that locks the second player out. It was also unstated whether both players score when both guess right in the same round.",
    "P2 (previous variation): cards 1, 4 and 5 (sum, middle digit, range) identified any code with certainty by leg-round 3. Every competent leg ended 2-2, and decisive results came only from expected-value-neutral 50/50 gambles. This is the lottery trap.",
    "P3 (previous variation): there was almost no interaction. A player's code choice did not affect their own score, and the attack was a fixed three-card recipe, so opponent modelling and code choice barely mattered.",
    "P4 (previous variation): the per-leg once-only card restriction cost an attribute or bitmask per player and added parsing for no strategic gain.",
    "P5 (original): the full game's 21 card types, tile deal, colours and central pool exceed the platform's limits, so a compact numeric version is required."
  ],
  "changes": [
    {
      "what": "Every per-player state value is written with an owner: 'that player's solved', 'that player's guesses left'. A rule states that both players are scored independently, so both can solve in the same leg, even in the same round.",
      "why": "Removes the shared-flag reading and the same-round ambiguity.",
      "fixes": "P1 (previous variation): 'solved' had no owner"
    },
    {
      "what": "The card set is replaced with six coarse cards, each with at most 4 possible answers: count of digits 5 or higher, count of odd digits, count of primes (2, 3, 5, 7), count of multiples of 3 (0, 3, 6, 9), count of consecutive neighbouring pairs, and sum mod 4. There are 120 possible codes. Any plan of 3 asks, even an adaptive one, has at most 4×4×4 = 64 answer paths, so at least 56 codes cannot be pinned down by leg-round 3 under any asking plan. Even after 4 asks a code may remain ambiguous.",
      "why": "No recipe guarantees a solve. Players must choose cards adaptively for information, judge how many candidates remain, and decide when a guess is worth its risk.",
      "fixes": "P2 (previous variation): cards 1, 4 and 5 identified any code with certainty"
    },
    {
      "what": "A wrong guess now gives -1 to the guesser and +1 to the code's owner, a swing of 2. An owner whose code is not cracked by the end of the leg scores +1. A correct guess scores 5 - leg-round as before.",
      "why": "Code choice now pays directly: an ambiguous code earns points by luring wrong guesses and surviving. Guess timing becomes a real expected-value calculation that depends on the remaining candidates and on the opponent's visible progress. For example, with 2 candidates at leg-round 3 a guess is worth +0.5 over waiting, while at leg-round 4 it is worth -0.5. Players also model which codes the opponent is likely to hide.",
      "fixes": "P3 (previous variation): almost no interaction"
    },
    {
      "what": "Repeat asks are allowed and simply return the same answer.",
      "why": "Saves the used-card attribute and parsing. A repeat is just a wasted ask, which is its own penalty.",
      "fixes": "P4 (previous variation): the once-only card restriction cost state for no gain"
    },
    {
      "what": "The game is kept as 2 players, 3 legs of 4 rounds, a 3-digit sorted numeric code, simultaneous asks and guesses, and arithmetic card answers.",
      "why": "Fits within 16 steps, 3 choice steps, 18 attributes, 1 hidden element and 0 random draws.",
      "fixes": "P5 (original): the full game exceeds the platform's limits"
    }
  ],
  "keeps": [
    "A hidden sorted code made of distinct digits, like the sorted tiles behind the screen",
    "Asking question cards that must be answered truthfully by arithmetic on the hidden code",
    "Guessing the exact code, with a cost for wrong guesses and a reward for early correct ones",
    "The race to deduce the opponent's code before they deduce yours"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The deduction core fits the platform once cut to a numeric code. The coarse-card pigeonhole fix removes the guaranteed solve, and the defender scoring rules make code choice and guess timing strategic."
  },
  "variation": {
    "name": "Break the Code: Coarse Clues",
    "summary": "Two players each hide three different digits and, over four rounds per leg, ask coarse yes-ish questions about the opponent's digits. They decide when to risk a guess. Cracking early scores well, guessing wrong feeds the opponent, and a code that survives the leg scores for its owner.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "R1. Structure. Two players play a match of 12 rounds, split into 3 legs of 4 rounds each. Legs start at rounds 1, 5 and 9. The round counter starts at 0 and increases by exactly 1 at the very start of each round; nothing else changes it. Leg-round = ((round - 1) mod 4) + 1, so it runs 1, 2, 3, 4 within each leg.\n\nR2. Player state. Each player has their own: score, wrong count, code, guesses left, solved, card asked, answer and guess. Score and wrong count start at 0 and carry over between legs. Both players are always handled separately: one player's result never blocks or changes the other's, except where a rule says the code's owner scores.\n\nR3. New leg. When leg-round is 1, first reset each player's own guesses left to 2 and each player's own solved to 0. Then both players secretly and at the same time enter a code as a number, for example 147, 852, or 12 (meaning 0-1-2). In other rounds there is no code prompt and codes stay unchanged.\n\nR4. Parsing a code. Read the entry x as digits A = floor(x / 100), B = floor(x / 10) mod 10 and C = x mod 10. If x is a whole number from 0 to 999 and A, B and C are all different, sort them ascending as a < b < c and store 100*a + 10*b + c. For example, 852 is stored as 258.\n\nR5. Invalid code. Any other entry is stored as code 12 (digits 0, 1, 2). This covers repeated digits, out-of-range or non-numeric entries, and missing or declined entries.\n\nR6. Asking. Every round, both players at the same time may pick one card number from 1 to 6 to ask about the opponent's code. Declining or giving an invalid number means no question this round. A card may be asked again; it gives the same answer. With the opponent's sorted digits a < b < c, the answers are:\n- Card 1, High: how many of the three digits are 5 or higher (0-3).\n- Card 2, Odd: how many of the digits are odd (0-3).\n- Card 3, Prime: how many of the digits are 2, 3, 5 or 7 (0-3).\n- Card 4, Threes: how many of the digits are 0, 3, 6 or 9 (0-3).\n- Card 5, Chain: (1 if b - a = 1 else 0) + (1 if c - b = 1 else 0) (0-2).\n- Card 6, Sum mod 4: (a + b + c) mod 4 (0-3).\nEach answer is shown privately to the player who asked. Then both players are told which card number (or none) each player asked.\n\nR7. Guessing. Then both players at the same time may enter a guess of the opponent's code. A player is prompted only if that player's own guesses left is above 0 and that player's own solved is 0. The guess is parsed as in R4.\n- Pass: declining, or an entry that does not give three different digits from 0 to 999. A pass costs nothing.\n- Correct: a valid guess equal to the opponent's stored code. The guesser scores 5 - leg-round, that is 4, 3, 2 or 1. That player's own solved becomes 1 for the rest of the leg.\n- Wrong: any other valid guess. The guesser scores -1, their wrong count increases by 1, and their guesses left decreases by 1. The opponent, the code's owner, scores +1.\nIf both players guess correctly in the same round, both score.\n\nR8. Results. After guessing, both players are told whether each player passed, guessed right or guessed wrong. Codes are not shown.\n\nR9. End of leg. When leg-round is 4, after R8, each player whose own code was not guessed correctly during this leg scores +1. That is, a player scores +1 if the opponent's solved is still 0. Then both codes are revealed to both players.\n\nR10. End. The game ends after round 12.",
    "objective": "After round 12, the player with the higher total score wins. If the totals are equal, the player with fewer wrong guesses wins. If those are also equal, the game is a draw.",
    "expected_effect": "No asking plan can guarantee a solve before leg-round 4: three asks give at most 64 answer patterns for 120 codes. Players must therefore pick cards adaptively, count the remaining candidates, and weigh guessing now (more points, but each miss is a swing of 2 to the opponent) against waiting, which risks scoring little and conceding the +1 for an uncracked code. Code choice becomes a hide-and-seek against the opponent's likely asking plan: pick codes that share answer patterns with many others, and avoid ones a strong asker isolates quickly. Seeing which cards the opponent asked and whether they guessed lets a player estimate the opponent's progress. Every simple policy can lose. Always passing earns at most +1 per leg and loses to any player who cracks at least once without reckless misses. Always guessing bleeds swings of 2. Both always passing is a 3-3 draw. Some residual chance remains when a guess must be made among 2-3 candidates. Better card choice shrinks the candidate count, and expected-value-aware timing uses it, so the stronger reasoner should win most matches. There is no talk phase: it is a 2-player zero-sum contest with nothing to negotiate."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 16,
    "choice_steps_per_round": 3,
    "attributes": 18,
    "hidden_elements": 1,
    "random_draws_per_round": 0,
    "rounds": 12
  }
}
```
````
