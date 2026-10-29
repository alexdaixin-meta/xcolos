# 58 design

- time: 2026-10-27T10:26:14+00:00 (95.3s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 36ff319737ac27f5, reply sha256 bcfcf364355e4748

## Sent

````
Original game: Lost Cities
Players in the original: 2 to 2

Original rules:
Place board with 5 color discard spaces between players. Shuffle 60 cards (9 numbers 2-10 and 3 wagers per color). Deal 8 cards to each player; remaining cards form face-down draw pile. Oldest player starts; turns alternate. On your turn you must first play one card from hand, then draw one. To play to your expeditions: start or extend a column of that color on your side; numbers must be strictly increasing within a column; wager cards can only be played before any number card in that column, multiple allowed. To discard: place a card face-up on its color discard pile, only top visible. Then draw: take top card of draw pile or top card of any discard pile, but not the card you just discarded. Game ends immediately when last card is drawn from draw pile. Score each color: sum numbers, subtract 20 if column exists, multiply result by 1 plus number of wagers (x2,x3,x4), add 20 bonus if column has 8+ cards. No column scores 0. Highest total after three rounds wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
Rebalance so that building columns is clearly better than doing nothing.
- Lower or remove the column offset (column_offset 8 makes most short columns negative), or score an empty column below a modest built one, for example a small penalty per empty column.
- Remove illegal plays as a choice: only offer legal PLAY options, so random or careless play is not drained by penalties and the illegal_play_penalty parameter can go.
- Make the Wager risk symmetric: if it doubles positive scores, it should also worsen negative ones, so committing is a real decision.
- Keep the per-turn option list short so a fixed policy cannot exploit a structural default.
- Then check that neither first@ nor last@ policies beat random seats by much more than 60%.
the game was built and behaves as specified, but evaluation found design flaws:
- always taking the first option as seat 2 wins 87% of decided matches against random seats
- against random seats the results were {'seat 2': 25, 'seat 1': 35}
- a thoughtless policy `first@seat1`: won 50, lost 9, drew 1
- a thoughtless policy `first@seat2`: won 52, lost 8, drew 0
- a thoughtless policy `last@seat1`: won 39, lost 21, drew 0
- a thoughtless policy `last@seat2`: won 29, lost 30, drew 1

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Lost Cities is a two-player card game. Players take turns playing cards from a hidden hand into strictly ascending colour columns, or discarding them, and then draw from a deck or from a discard pile. Each started column costs 20 points, wagers multiply a column's result whether it is positive or negative, and the higher total after three hands wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "weak",
      "evidence": "The original has no dominant trivial policy, but the previous adaptation did. It offered a short, ordered option list with a safe structural default, and 'always the first option' won 87% of decided games as seat 2 and 85% as seat 1 against random seats. Random seats were also lopsided (seat 1 won 35, seat 2 won 25). Starting a column cost so much that doing little beat building."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "In the original, timing column starts, holding cards, discard denial and wager commitment reliably separate players, though the draw adds a fair amount of variance. The previous version's skill signal was hidden behind its defaults."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "The original has no solved line. A novice still scores by building one or two columns, and an expert keeps improving through card counting and reading the opponent's columns."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands and the deck order are hidden. Players infer what the opponent holds from their discards and columns, and plan several turns ahead about whether a column will pay off its 20-point offset."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Scoring is pure arithmetic: sum, minus the offset, times the multiplier, plus the bonus."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The original needs 8-card hidden hands, five discard piles that can be drawn from, per-card legality checks, three hands and a long game. That is too much state and too many steps for the engine. The 5-colour discard board is incidental, not spatial play."
    }
  ],
  "problems": [
    "Previous version: one structural default option ('first') beat random play about 85% of the time from either seat, so a thoughtless policy dominated.",
    "Previous version: the column offset made short columns negative, so not building was better than building.",
    "Previous version: illegal plays were offered as choices and punished, which drained random and careless players for reasons unrelated to strategy.",
    "Previous version: the seats were unbalanced (35 to 25 wins for random play).",
    "Original: hidden 8-card hands, five drawable discard piles and three hands exceed the step, attribute and hidden-element limits.",
    "Original: the wager decision is several separate card plays per colour, which costs many steps and choices."
  ],
  "changes": [
    {
      "what": "Replace hands and discard piles with one shared face-up card per round. Both players choose TAKE or LEAVE at the same moment. Priority on a clash alternates: seat 1 in odd rounds, seat 2 in even rounds, over an even 20 rounds.",
      "why": "This keeps the Lost Cities tension of 'do I want this card, or do I want to deny it' in one choice step and one random draw per round. Alternating priority over an even number of rounds makes the seats symmetric.",
      "fixes": "Original: hidden 8-card hands, five drawable discard piles and three hands exceed the step, attribute and hidden-element limits."
    },
    {
      "what": "There are only two options, TAKE and LEAVE, and both are always legal. A taken card that does not ascend is buried at a cost of 4 points instead of being an illegal play.",
      "why": "No illegal options exist. Burying gives TAKE a real price, so 'always TAKE' wrecks its own score, while 'always LEAVE' never builds. A selective policy beats both.",
      "fixes": "Previous version: illegal plays were offered as choices and punished, which drained random and careless players for reasons unrelated to strategy."
    },
    {
      "what": "Lower the column offset to 6, against card values of 2 to 10. Add a +10 bonus for 4 or more cards in a column. An empty non-backed column scores 0, and an empty backed column scores -10.",
      "why": "A modest two-card column, such as 4 and 7 (11 - 6 = +5), now beats doing nothing. Passing everything scores -10, which random play usually beats.",
      "fixes": "Previous version: the column offset made short columns negative, so not building was better than building."
    },
    {
      "what": "Each player is secretly dealt one Backed colour, which works as the wager. That column's score is doubled whether positive or negative, and leaving it empty costs -10.",
      "why": "This turns the wager into one hidden type. The risk is symmetric, it gives each player something to infer about the other (which colour are they chasing, and so which cards should I deny), and the types are equal in expectation, so it is not a lottery.",
      "fixes": "Original: the wager decision is several separate card plays per colour, which costs many steps and choices."
    },
    {
      "what": "Check the simple policies against this winner rule. Always-LEAVE ends at exactly -10 and loses to any player who builds one positive column. Always-TAKE grabs about 15 cards, buries about 8 (-32), and roughly breaks even, so it loses to a selective player and is close to a coin flip against random play. Random play takes half the time, buries little and lands near small positive totals.",
      "why": "No option is safe and no constant policy dominates, so the first-option dominance goes away.",
      "fixes": "Previous version: one structural default option ('first') beat random play about 85% of the time from either seat, so a thoughtless policy dominated."
    },
    {
      "what": "Use 20 rounds from a 27-card deck, with priority alternating 10 rounds each.",
      "why": "Each seat holds priority equally often. The 7 cards never revealed keep the endgame uncertain, so card counting matters without making the end certain.",
      "fixes": "Previous version: the seats were unbalanced (35 to 25 wins for random play)."
    }
  ],
  "keeps": [
    "Colour columns that must strictly ascend, so taking a high card early blocks the middle values.",
    "A fixed cost to start each expedition, which makes starting a colour a commitment.",
    "A wager that multiplies the column both ways, kept as the secret Backed colour.",
    "Taking or discarding a card the opponent needs as denial, kept as burying.",
    "A bonus for long expeditions.",
    "Card counting against a known deck composition.",
    "Two players, higher total wins."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core tension of ascending columns, a costly start, a double-edged wager and denial fits in one face-up draw and one simultaneous take-or-leave choice per round, with a single hidden type."
  },
  "variation": {
    "name": "Lost Cities: Expedition Draft",
    "summary": "Two explorers draft face-up cards one at a time into three ascending colour expeditions. Each player secretly backs one colour, whose result counts double for good or ill. Clashing claims go to the player holding priority, and taking a card you cannot use buries it at a cost, which is how you deny a rival.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "SETUP\n1. The deck has 27 cards: three colours (Red, Blue, Green), each with one card of every value from 2 to 10. Shuffle it face down. Players may know this composition.\n2. Each player is secretly and independently dealt one Backed colour, Red, Blue or Green, each with probability 1/3. The two may be the same. Only its owner sees it.\n3. Each player has three expeditions, one per colour. Each starts empty and is tracked by its top value (0 when empty), the sum of its values, and its card count. Each player also has a Burial penalty that starts at 0. All expeditions and Burial penalties are public.\n\nEACH ROUND (20 rounds)\n4. Reveal the top card of the deck to both players: its colour and value.\n5. Priority belongs to seat 1 in odd rounds and to seat 2 in even rounds. This is announced.\n6. Both players choose at the same moment: TAKE or LEAVE.\n7. Resolution:\n   - If exactly one player chose TAKE, that player gets the card.\n   - If both chose TAKE, the player with priority gets it and the other gets nothing.\n   - If both chose LEAVE, the card is removed from the game.\n8. The player who gets the card does one of two things:\n   - If its value is higher than the top value of their expedition in that colour (any value beats an empty expedition), it is added there. Its value is added to the sum, the count rises by 1, and the top value becomes this card's value.\n   - Otherwise the card is buried: it is removed from the game and that player's Burial penalty rises by 4.\n9. Announce both choices, who got the card, where it went, and all public expedition states.\n\nThe 7 cards still in the deck after round 20 are never revealed.\n\nFINAL SCORING (after round 20), for each player and colour\n10. If the expedition is empty, it scores 0. If it is empty and is that player's Backed colour, it scores -10.\n11. Otherwise its base is sum minus 6.\n12. If the colour is the player's Backed colour, the base is doubled. This applies to negative bases as well.\n13. Add 10 if the expedition holds 4 or more cards.\n14. The player's total is the sum of their three colour scores minus their Burial penalty.\n15. Backed colours are then revealed.",
    "objective": "After round 20 the player with the higher total wins. Equal totals are a draw.",
    "expected_effect": "Constant policies stop working:\n- Always-LEAVE is locked at -10.\n- Always-TAKE pays for about 8 buried cards and jumps its columns to high values too early, so it roughly breaks even.\n- Random play lands in between.\n- A selective player who takes cards that fit low-to-high and starts only colours it can fill beats all of them. Such a player also spends a 4-point burial only to deny a high card the opponent's visible columns need.\n\nThe secret Backed colour makes the opponent's choices informative. A player who keeps contesting Green is probably backing it, so Green high cards are worth denying on your priority rounds. Mixed signals, such as taking a colour you are not backing, become a cheap bluff. Card counting over the unseen pool decides whether starting a third column or holding a top of 4 is worth it. Alternating priority over 20 rounds keeps the seats even. There is no talk phase because this is a two-player zero-sum game."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 10,
    "choice_steps_per_round": 1,
    "attributes": 16,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 20
  }
}
```
````
