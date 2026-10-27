# 03 design

- time: 2026-10-27T18:21:21+00:00 (84.4s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 0ab467f47ddd294e, reply sha256 f85b8ec8e94abefa

## Sent

````
Original game: Break the Code
Players in the original: 2 to 4

Original rules:
Each player hides 5 tiles (4 in 4-player) behind a screen, sorted ascending, red before blue for same number. 20 tiles containing numbers 0-9 in two colors are shuffled and dealt. 21 question cards are shuffled; six are face up. On your turn you must either ask one face-up question card or attempt to guess. If you ask, your opponent(s) must answer truthfully according to the card (e.g., where is a number, where are same colors adjacent, where are sequential numbers). Asked cards are discarded and replaced from the deck. In 2-player you guess opponent's 5 tiles in order; if wrong you continue, if right you win but opponent gets one final guess chance, otherwise tie if deck runs out. In 3-4 players there is a central pool of 4-5 hidden tiles; players ask and all opponents answer (all shared in 4-player), and any player may once per game secretly check and claim the central tiles; wrong guess eliminates you from asking.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- playable FAILED: The rules are finite (6 rounds) and decided by arithmetic on stored codes. No board, clock or judge is needed, and asking and guessing are correctly simultaneous polls. It is a 2-player game, so talk is not needed.

Gaps that leave situations unplayable from the words alone:
1. No rule covers naming a card already used, or an invalid card. 'Must use every card exactly once' gives no enforcement or default.
2. No rule covers an illegal guess (repeated digits, not ascending, out of range) or writing a code with 0 guesses left. Is it treated as a pass, as wrong, or does it still consume a guess?
3. No rule covers an illegal secret code at setup, for example 3-3-7.

Complexity limits:
- Tracking 6 used-card flags per player (12), 2 guess counters and 6 code digits already reaches 20 attributes. That is before guess digits, answer values and correctness flags, so the declared 13 attributes only works if the codes are hidden elements and the used cards are packed into one bitmask per player. This is not stated.
- Steps: Q5 and Q6 each need several conditional operations per player. 10 steps fits only if each answer is a single multi-operation step.

The rules need these defaults and this encoding spelled out.
- reasoning_over_luck FAILED: There is no random draw, and inference is real: you narrow 120 candidates with 6 known functions, choose the order of question cards, and choose a hard-to-identify code.

Under the intended good strategy, though, the result is not decided by reasoning:
- Both players pick codes in large equivalence classes, such as the 3-7-8 / 4-5-9 pair or classes that stay ambiguous until late cards.
- Both use the same six cards, so both reach comparable information at about the same round.
- The race is then settled in one of three ways:
  (i) Both identify the code in the same round and both guess correctly: a draw.
  (ii) Both still face k candidates: each player's early 1/k guess succeeds or fails essentially by coin flip.
  (iii) Both wait until the full profile and then use their 2 guesses on a class of size ≤2: both correct, a draw.

Rough estimate: among competent players, most games draw. Most decisive games turn on a blind 1/2 or 1/3 guess among indistinguishable candidates. Chance among equals is effectively above 50% of decisive outcomes. A better reasoner is not clearly favoured once both choose good codes, and the required use of every card removes most planning from question order by round 6.
- change: Reduce draws and coin-flip races. Add a margin of victory that turns draws into decisive results, scored over the cards not yet used. Example: a correct guess in round r scores 7−r points, a wrong guess costs 2 points, and higher total wins. Play several codes per match, such as 3 legs with roles carried over, so early efficient deduction and smart code choice are rewarded beyond same-round ties.
- change: Drop 'must use every card exactly once'. Let each player ask only 4 of the 6 cards, so card selection is a real planning decision and the two players reach different information.
- change: Add a tie-break for both players correct in the same round. For example, the player with more unused question cards or more remaining guesses wins, so better planning is rewarded instead of a draw.
- change: Specify the defaults. An already-used or invalid card is replaced by the lowest-numbered unused card. An illegal guess, or a guess with 0 guesses left, counts as a pass and consumes nothing. An illegal secret code is replaced by 0-1-2, or the player is re-polled.
- change: State the encoding. Store each code as a hidden element per player and each player's used cards as one bitmask attribute, so attributes stay at or below 20. List the arithmetic for Q5 and Q6 so steps_per_round stays at or below 20.
The variation that was reviewed: Break the Code: Duel: SETUP. Before round 1, each player secretly chooses a code: three different digits from 0 to 9, recorded smallest first as A < B < C. For example 2-5-8 is legal; 3-3-7 is not. Only the engine knows both codes. Each player starts with 2 guesses available and all six question cards unused.

THE SIX QUESTION CARDS. Each card is answered with one number computed from the opponent's code A < B < C.
Q1 SUM: A + B + C.
Q2 EVENS: how many of the three digits are even (0 counts as even).
Q3 RANGE: C − A.
Q4 HIGH: how many of the three digits are 5 or more.
Q5 STEPS: how many of the two neighbouring pairs (A,B) and (B,C) differ by exactly 1 (answer 0, 1 or 2).
Q6 THREES: how many of the three digits are in {0, 3, 6, 9}.

EACH ROUND (6 rounds):
1. Ask. Both players simultaneously and secretly name one question card they have not used yet. Each player must use every card exactly once over the six rounds.
2. Answer. The engine computes each answer from the opponent's code and announces to both players which card each player asked and its answer.
3. Guess. Both players simultaneously either pass or, if they have a guess left, write a full code (three digits, smallest first). Each guess uses up one of that player's 2 guesses.
4. Check. Each guess is compared with the opponent's code. A guess is correct only if all three digits match exactly. Every guess and its result (correct or wrong) is announced to both players.
5. End check. If at least one player guessed correctly this round, the game ends now. Otherwise play continues to the next round. After round 6 the game ends regardless. Winner: If exactly one player guesses the opponent's code correctly in the round the game ends, that player wins. If both guess correctly in the same round, it is a draw. If neither has guessed correctly by the end of round 6, it is a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Break the Code is a deduction game. Players hide sorted number tiles and take turns asking face-up question cards that opponents must answer truthfully, then try to guess the hidden tiles exactly. The previously tested 2-player 'Duel' version reduced it to two secret 3-digit codes, six fixed question cards asked simultaneously, and a first-to-guess-correctly race over 6 rounds.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "weak",
      "evidence": "In the tested Duel, no simple policy wins outright. Always-pass only draws, and blind early guessing (1/120) loses. But 'must use every card exactly once' makes question order nearly irrelevant by round 6. If both players pick codes from large ambiguity classes and wait for the full profile, the game draws. A simple wait-and-guess policy cannot lose against a strong player, so the interesting choices do not move the result."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Between competent players most games draw (same-round correct guesses, or nobody correct). Most decisive games turn on a blind 1/2 or 1/3 pick between indistinguishable candidates. Luck therefore decides more than half of decisive outcomes, and the better reasoner is not reliably favoured."
    },
    {
      "criterion": "headroom",
      "verdict": "weak",
      "evidence": "With all six cards forced and a binary race, the decisions are thin. A weak player still draws often, and a strong player has little way to convert better deduction or code choice into a win."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "The hidden code is real hidden state: 120 candidates narrowed by known functions. Choosing a code that resists identification is opponent modelling, and choosing which card to ask next is planning."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Every answer and every guess check is arithmetic on stored codes. No judge is needed."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The game is text-only, turn-based and short. It failed playability on three counts. There were no defaults for an invalid or reused card, an illegal guess, or an illegal code. The attribute encoding was unstated: separate digit and card flags exceed 20 attributes. The step count for answer arithmetic was unclear."
    }
  ],
  "problems": [
    "P1: Most games between competent players are draws (both correct in the same round, or neither correct), so the result rarely reflects skill.",
    "P2: Decisive games are mostly settled by blind 1/2 or 1/3 guesses between indistinguishable candidates: luck among equals.",
    "P3: 'Use every card exactly once' removes card selection as a decision, and both players end with the same information at the same time.",
    "P4: A single code per match gives one luck-heavy sample, no chance to learn an opponent's code-choice habits, and no reward for efficient deduction beyond tying.",
    "P5: No rule for naming an invalid or already-used card.",
    "P6: No rule for an illegal guess (repeated digits, out of range, unsorted) or for guessing with no guesses left.",
    "P7: No rule for an illegal secret code at setup.",
    "P8: Attribute and step encoding was unstated and, done naively (separate digits, six card flags per player), exceeds the 20-attribute limit."
  ],
  "changes": [
    {
      "what": "Replace the first-correct-wins race with points. In each leg, a correct guess scores 4, 3, 2 or 1 points in leg-round 1, 2, 3 or 4. A wrong guess costs 1 point. The leg does not stop when one player is correct; the other can still score less by guessing later. The higher match total wins.",
      "why": "Same-round ties now depend on how early each player committed. A player who solves in leg-round 2 beats one who solves in leg-round 3. When to guess among k candidates becomes an expected-value decision, not a coin toss with nothing at stake.",
      "fixes": "P1"
    },
    {
      "what": "Play 3 legs of 4 rounds each (12 rounds). Each leg uses fresh secret codes, and both codes are revealed at the end of each leg.",
      "why": "Three independent legs average out the luck of a final 1/2 pick. Revealing codes lets players learn and exploit each other's code-choice habits in later legs.",
      "fixes": "P2"
    },
    {
      "what": "Each leg has only 4 ask rounds, so each player uses 4 of the 6 cards. A card cannot be repeated within a leg; all cards become available again next leg.",
      "why": "Which 4 cards to ask, and in which order given earlier answers, becomes a real adaptive planning decision. The two players reach different information at different speeds.",
      "fixes": "P3"
    },
    {
      "what": "Same leg structure as above, with code choice repeated at the start of every leg.",
      "why": "Gives multiple deduction samples and repeated code-choice duels, where opponent modelling can pay off.",
      "fixes": "P4"
    },
    {
      "what": "Card default: a missing, invalid or already-used card number is replaced by the lowest-numbered card that player has not used this leg.",
      "why": "Every ask resolves deterministically.",
      "fixes": "P5"
    },
    {
      "what": "Guess defaults:\n- Three different digits 0-9 written in any order are sorted ascending and accepted.\n- Anything else (repeats, wrong length, non-digits, blank) counts as a pass and costs nothing.\n- A guess written with no guesses left, or after already guessing correctly this leg, counts as a pass and costs nothing.",
      "why": "Every guess resolves deterministically.",
      "fixes": "P6"
    },
    {
      "what": "Code default: three different digits in any order are sorted. Any other entry becomes 0-1-2. This code is identifiable from the SUM card alone, which is a natural penalty.",
      "why": "Setup always produces a legal code.",
      "fixes": "P7"
    },
    {
      "what": "Store each code as one number 100A+10B+C and each guess the same way. Store used cards as one bitmask per player (card n adds 2^(n-1)). Compute each answer in a single calculation step per player.",
      "why": "Keeps the game at 17 attributes and 13 steps.",
      "fixes": "P8"
    },
    {
      "what": "Tie-break: if totals are equal, the player with fewer wrong guesses over the match wins. Otherwise it is a draw.",
      "why": "Turns remaining ties into results that reward careful play.",
      "fixes": "P1"
    }
  ],
  "keeps": [
    "Secret sorted number codes that each player hides from the other",
    "Question cards that must be answered truthfully with a computed fact about the opponent's code",
    "Exact full-code guesses, with a limited number of attempts and wrong guesses penalised",
    "The race to deduce faster than your opponent while choosing a code that is hard to deduce"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core is genuine hidden-state deduction plus code-choice opponent modelling. It needed graded scoring, partial card use, several legs and explicit defaults, all of which fit within the limits."
  },
  "variation": {
    "name": "Break the Code: Three-Leg Duel",
    "summary": "Two players each hide a 3-digit code and race to deduce the other's using 4 of 6 question cards per leg. Earlier correct guesses score more and wrong guesses cost a point, over 3 legs with fresh codes.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "OVERVIEW. Two players. The match has 3 legs of 4 rounds each (12 rounds in total). Leg 1 is rounds 1-4, leg 2 is rounds 5-8, leg 3 is rounds 9-12. The leg-round is 1, 2, 3 or 4 within each leg. Scores start at 0 and carry across legs.\n\nCODES. A code is three different digits from 0 to 9, kept smallest first as A < B < C. Example: 2-5-8.\n\nTHE SIX QUESTION CARDS. Each answer is one number computed from the opponent's current code A < B < C.\n1 SUM: A + B + C.\n2 EVENS: how many of the three digits are even (0 counts as even).\n3 RANGE: C - A.\n4 HIGH: how many of the three digits are 5 or more.\n5 STEPS: how many of the pairs (A,B) and (B,C) differ by exactly 1 (0, 1 or 2).\n6 THREES: how many of the three digits are in {0, 3, 6, 9}.\n\nEACH ROUND:\n\nStep 1. Code choice (leg-round 1 only, i.e. rounds 1, 5, 9).\n- Both players simultaneously and secretly write a code.\n- Three different digits written in any order are sorted ascending and become that player's code for this leg.\n- Any other entry (repeated digits, wrong count, non-digits, blank) becomes the code 0-1-2.\n- Only the engine knows the codes.\n- Each player's guesses for the leg are set to 2, their solved flag to no, and their used cards to none.\n\nStep 2. Ask. Both players simultaneously and secretly name one card number (1-6) they have not used in this leg.\n- If a player names nothing, an invalid number, or a card already used this leg, they are given the lowest-numbered card they have not used this leg.\n- The card becomes used for that player until the leg ends.\n- Each player uses exactly 4 different cards per leg; all six are available again at the start of the next leg.\n\nStep 3. Answer. The engine computes each player's card from the opponent's code. It announces to both players which card each player asked and the answer.\n\nStep 4. Guess. Both players simultaneously either pass or write a code guess.\n- A guess of three different digits in any order is sorted ascending.\n- Any other entry counts as a pass.\n- A guess written by a player with 0 guesses left, or who has already guessed correctly this leg, counts as a pass.\n- A pass costs nothing.\n- A valid guess uses up 1 of that player's guesses for the leg.\n\nStep 5. Check. Each valid guess is compared with the opponent's code.\n- Correct (all three digits match): the guesser scores 5 minus the leg-round, so 4 points in leg-round 1, 3 in leg-round 2, 2 in leg-round 3, 1 in leg-round 4. The guesser is marked solved for the rest of the leg and makes no further guesses that leg.\n- Wrong: the guesser loses 1 point and also gains 1 to their wrong-guess count.\n- Every guess and its result (correct or wrong) is announced to both players.\n- One player guessing correctly does not end the leg for the other player, who may keep asking and guessing.\n\nStep 6. Leg end (leg-round 4 only, i.e. rounds 4, 8, 12). Both codes are revealed to both players, and the current scores are announced.\n\nStep 7. End check. After round 12 the match ends.\n\nENGINE ENCODING (for builders):\n- Per player: score, wrong_count, guesses_left, solved (0/1), used_mask, code (100A+10B+C), ask, answer, guess (100A+10B+C, or 0 for a pass).\n- Plus one table attribute: round.\n- Total: 17 attributes.\n- Leg-round is ((round - 1) mod 4) + 1.\n- Digits of a code are A = floor(code/100), B = floor(code/10) mod 10, C = code mod 10.\n- Card n is used if floor(used_mask / 2^(n-1)) mod 2 = 1.",
    "objective": "After round 12, the player with the higher total score wins. If the totals are equal, the player with fewer wrong guesses over the whole match wins. If that is also equal, the match is a draw.",
    "expected_effect": "Speed of deduction now separates players even when both eventually solve. Solving in leg-round 2 instead of 3 is worth a point, so ties are rarer.\n\nChoosing 4 of 6 cards adaptively rewards picking the most informative next question given earlier answers. Codes with extreme sums (such as 0-1-2 or 7-8-9) become easy targets, so code choice becomes a reasoned bet on which cards the opponent will ask.\n\nGuessing becomes an expected-value decision. With 2 candidates left in leg-round 3, guessing now (2 points, 50%, -1 if wrong) competes with waiting for a 4th card that may settle it for 1 point. Remaining 1/2 picks are spread over 3 legs, so luck averages down.\n\nRevealed codes let players model each other's code-choice habits across legs.\n\nSimple policies all lose to good play:\n- Always pass scores 0 and loses to any positive score.\n- Blind early guessing averages about -2 per leg.\n- Always asking cards in fixed order loses speed to adaptive asking.\n- Always waiting until leg-round 4 caps at 1 point per leg and loses to a player who solves earlier.\n\nTalk is omitted: two players with directly opposed interests and nothing to coordinate."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 13,
    "choice_steps_per_round": 3,
    "attributes": 17,
    "hidden_elements": 1,
    "random_draws_per_round": 0,
    "rounds": 12
  }
}
```
````
