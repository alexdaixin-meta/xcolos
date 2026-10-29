# 01 design

- time: 2026-10-27T18:19:12+00:00 (62.7s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 828b33b9d542c9da, reply sha256 b3e0021d65fdca9b

## Sent

````
Original game: Break the Code
Players in the original: 2 to 4

Original rules:
Each player hides 5 tiles (4 in 4-player) behind a screen, sorted ascending, red before blue for same number. 20 tiles containing numbers 0-9 in two colors are shuffled and dealt. 21 question cards are shuffled; six are face up. On your turn you must either ask one face-up question card or attempt to guess. If you ask, your opponent(s) must answer truthfully according to the card (e.g., where is a number, where are same colors adjacent, where are sequential numbers). Asked cards are discarded and replaced from the deck. In 2-player you guess opponent's 5 tiles in order; if wrong you continue, if right you win but opponent gets one final guess chance, otherwise tie if deck runs out. In 3-4 players there is a central pool of 4-5 hidden tiles; players ask and all opponents answer (all shared in 4-player), and any player may once per game secretly check and claim the central tiles; wrong guess eliminates you from asking.
````

## Reply

````
```json
{
  "original_summary": "Break the Code is a deduction game. Each player hides a sorted row of numbered, coloured tiles. On a turn a player asks a face-up question card, which opponents must answer truthfully (where are the 5s, how many reds, the sum of the left tiles), or tries to guess a code outright. In two-player games the first correct guess wins, though the opponent gets one last chance to guess and draw.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "weak",
      "evidence": "Simple policies lose. Guessing at random almost never cracks a code, and never guessing cannot win. Choices clearly matter. But the first player in turn order gets a built-in tempo edge, which the opponent's final-guess rule only patches into a draw. Codes are dealt, so some hands are much easier to crack than others."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "A careful deducer who picks informative questions and narrows the possible codes beats a sloppy one reliably. Luck enters through the dealt tiles and the face-up question cards: a lucky card that pins a number can decide a close race."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Choosing questions that split the remaining codes most evenly, and judging when to risk a guess, leave room to improve. A weak player still gathers answers and can eventually guess."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "The whole game is inference about a hidden code from partial answers. It has little opponent modelling, though, because codes are dealt rather than chosen."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Answers are factual and a guess is right or wrong, so the winner follows mechanically."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "It is text-friendly, but 20 coloured tiles, 21 card types with positional answers, a rotating face-up market and the 3–4 player central-pool variant together exceed the attribute and step limits. Positional answers about tile slots also need many computations per card."
    }
  ],
  "problems": [
    "Turn order gives the first player a tempo edge in the race to guess.",
    "Codes are dealt at random, so one player may get a far easier code to crack: luck that good play cannot fully correct.",
    "Random face-up question cards let a lucky draw decide the race.",
    "The full component set (20 coloured tiles, 21 question types, a central pool for 3–4 players) exceeds the platform's attribute and step limits.",
    "There is no opponent modelling: nothing about the hidden code is a choice, so players only solve logic and never outthink a person.",
    "Unlimited wrong guesses make blind guessing nearly free whenever the deck is long."
  ],
  "changes": [
    {
      "what": "Both players ask and guess simultaneously each round. A correct guess ends the game at the end of that round, and two correct guesses in the same round are a draw.",
      "why": "This removes turn order entirely, and the same-round draw replaces the final-guess patch.",
      "fixes": "Turn order gives the first player a tempo edge in the race to guess."
    },
    {
      "what": "Each player secretly chooses their own code: three different digits from 0–9, written smallest to largest.",
      "why": "No one is dealt an easy code. Choosing a code that the question answers leave ambiguous becomes a strategic act of anticipating the opponent's deductions.",
      "fixes": "Codes are dealt at random, so one player may get a far easier code to crack: luck that good play cannot fully correct."
    },
    {
      "what": "The random market is replaced by a fixed menu of six question cards. Each player uses each card exactly once, one per round, over six rounds.",
      "why": "Luck in the questions disappears, and ordering the questions becomes a planning problem: which answers to get early so you can guess sooner.",
      "fixes": "Random face-up question cards let a lucky draw decide the race."
    },
    {
      "what": "Codes are cut to three distinct digits with no colours. The six questions each have a single numeric answer computed by arithmetic, and there is one two-player format.",
      "why": "This keeps attributes at about 13 and the steps per round at about 10, within the limits.",
      "fixes": "The full component set (20 coloured tiles, 21 question types, a central pool for 3–4 players) exceeds the platform's attribute and step limits."
    },
    {
      "what": "Questions are chosen so that no three of them combine linearly to give the code. The answers overlap, so several codes stay consistent and players must reason about which codes the opponent is likely to pick.",
      "why": "Code choice and code cracking become a contest of minds, not just algebra.",
      "fixes": "There is no opponent modelling: nothing about the hidden code is a choice, so players only solve logic and never outthink a person."
    },
    {
      "what": "Each player may guess at most twice in the whole game, and a wrong guess is announced to both players.",
      "why": "Guessing becomes a costly, timed decision: guess early at risk, or wait and risk the opponent cracking first.",
      "fixes": "Unlimited wrong guesses make blind guessing nearly free whenever the deck is long."
    }
  ],
  "keeps": [
    "A hidden sorted code of digits that each player must deduce about the other.",
    "Question cards answered truthfully as the only source of information.",
    "The tension between asking for more information and committing to a guess.",
    "The first correct guess wins, with a tie when both crack at the same moment."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The deduction core fits a text engine well once the components are cut down. Letting players choose their codes adds the opponent modelling the original lacks."
  },
  "variation": {
    "name": "Break the Code: Duel",
    "summary": "Two players each secretly choose a three-digit code. Over six simultaneous rounds each asks the other one question from a fixed six-card menu and may risk one of two guesses. The first to crack the opposing code wins.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "SETUP. Before round 1, each player secretly chooses a code: three different digits from 0 to 9, recorded smallest first as A < B < C. For example 2-5-8 is legal; 3-3-7 is not. Only the engine knows both codes. Each player starts with 2 guesses available and all six question cards unused.\n\nTHE SIX QUESTION CARDS. Each card is answered with one number computed from the opponent's code A < B < C.\nQ1 SUM: A + B + C.\nQ2 EVENS: how many of the three digits are even (0 counts as even).\nQ3 RANGE: C − A.\nQ4 HIGH: how many of the three digits are 5 or more.\nQ5 STEPS: how many of the two neighbouring pairs (A,B) and (B,C) differ by exactly 1 (answer 0, 1 or 2).\nQ6 THREES: how many of the three digits are in {0, 3, 6, 9}.\n\nEACH ROUND (6 rounds):\n1. Ask. Both players simultaneously and secretly name one question card they have not used yet. Each player must use every card exactly once over the six rounds.\n2. Answer. The engine computes each answer from the opponent's code and announces to both players which card each player asked and its answer.\n3. Guess. Both players simultaneously either pass or, if they have a guess left, write a full code (three digits, smallest first). Each guess uses up one of that player's 2 guesses.\n4. Check. Each guess is compared with the opponent's code. A guess is correct only if all three digits match exactly. Every guess and its result (correct or wrong) is announced to both players.\n5. End check. If at least one player guessed correctly this round, the game ends now. Otherwise play continues to the next round. After round 6 the game ends regardless.",
    "objective": "If exactly one player guesses the opponent's code correctly in the round the game ends, that player wins. If both guess correctly in the same round, it is a draw. If neither has guessed correctly by the end of round 6, it is a draw.",
    "expected_effect": "With seats symmetric, no dealt luck and no random cards, results depend on three skills. First, choosing a code that stays ambiguous under the likely question orders, avoiding giveaways such as 0-1-2 or consecutive runs that Q5 exposes. Second, ordering questions to cut down the opponent's possible codes fastest. Third, timing the two scarce guesses: guessing among two or three remaining candidates can win a round early, but a miss burns a guess and shows the opponent you are close. Simple policies all lose to a deducing player. Blind guessing in round 1 hits about 1 time in 120 and otherwise wastes guesses. Never guessing can at best draw and loses whenever the opponent cracks the code. Asking in fixed order 1–6 without reasoning gives the same information but a slower, worse guess."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 10,
    "choice_steps_per_round": 3,
    "attributes": 13,
    "hidden_elements": 1,
    "random_draws_per_round": 0,
    "rounds": 6
  }
}
```
````
