# 01 design

- time: 2026-10-28T03:00:49+00:00 (56.0s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 6685887ada705211, reply sha256 de4c66e9310605fd

## Sent

````
Original game: Reversis
Players in the original: 4 to 5

Original rules:
Reversis is for 4 players (5 with fewer cards) with a 52-card French pack, later 48 cards without Tens, ranking A K Q J 9-2, no trumps, deal and play anticlockwise. Each of 13 tricks: follow suit if able, otherwise discard any card; highest card of led suit wins trick and leads next. Counting cards are A=4 K=3 Q=2 J=1 (earlier 5-4-3-2) total 40, plus the Jack of Hearts called Quinola is special. After all tricks points are totaled; normally the player with fewest points wins and is paid the talon by the player with most points. If a player makes the reversis by taking every trick, that slam reverses the aim and that player wins outright, sweeping pools and reclaiming side payments. Bonuses for discarding Quinola and penalties for being forced to play it were added in later variants.
````

## Reply

````
```json
{
  "original_summary": "Reversis is a four-player trick-taking game with no trumps in which players try to avoid winning tricks that contain counting cards (A=4, K=3, Q=2, J=1), and the Jack of Hearts (Quinola) is especially dangerous. The player with the fewest points wins, unless someone takes every trick (the reversis), which reverses the aim and wins outright.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "Always playing the lowest legal card loses to a player who dumps high counters when void of the led suit. Always playing high takes most of the points. The reversis threat stops 'just dodge everything' from being safe, because if all three others duck, one strong hand can sweep. The anticlockwise lead gives no lasting edge over a full deal. A single deal can favour whoever holds low cards."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Card counting, reading voids and timing discards are real skills. But one deal of 13 cards is heavily luck-driven: a hand full of high cards in long suits can hardly avoid points. The original gives no mechanism, such as passing or several hands, to average this out."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Weak players still score, since points are spread around. Strong players improve through inference about voids, by holding back or forcing out the Quinola, and by spotting or blocking a reversis attempt. It is not solved."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands are hidden. Players must infer holdings from what others follow and discard, keep track of which counters are out, and plan several tricks ahead, both for safe exits and for or against a slam."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Trick winners follow from suit and rank. Points are card sums. Lowest total wins. Pools, side payments and the various Quinola bonus variants are messy, but they are still arithmetic."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The game is turn-based, text-only and has hidden hands, which all fit. However, 13 tricks with 52 cards, stakes, pools and several regional variants are too long and loosely specified. A deck that small per round and fixed rules are needed to stay within the step and round limits."
    }
  ],
  "problems": [
    "A single long deal makes the result depend heavily on the cards dealt (luck swamps skill).",
    "52 cards and 13 tricks per deal is too long for the round limit once several deals are played to reduce luck.",
    "Pools, talon payments, side payments and the variant Quinola bonuses are underspecified and not a winner rule the engine can use.",
    "There is no decision before play that lets a player fix a bad deal, so the deal often decides the game before any reasoning happens.",
    "The reversis reward ('wins outright, sweeps pools') is not stated as numbers, so its risk and reward cannot be weighed."
  ],
  "changes": [
    {
      "what": "Use a 24-card deck (A K Q J 9 8 in four suits) and deal 6 cards each, so a hand is 6 tricks.",
      "why": "This keeps the full rank and counting structure, including the Quinola, while making a hand short enough to play several.",
      "fixes": "52 cards and 13 tricks per deal is too long for the round limit once several deals are played to reduce luck."
    },
    {
      "what": "Play 4 hands. The first lead rotates so that each seat leads first exactly once. Penalty points carry over between hands.",
      "why": "Averaging over 4 deals and equal lead order reduces deal luck and seat advantage. It also creates multi-hand planning, such as pushing points onto the current leader.",
      "fixes": "A single long deal makes the result depend heavily on the cards dealt (luck swamps skill)."
    },
    {
      "what": "Before each hand except the 4th, every player at the same moment secretly passes 2 cards: to the left in hand 1, to the right in hand 2, across in hand 3, and no pass in hand 4.",
      "why": "Passing lets good players repair a bad deal. It also creates hidden knowledge to exploit, since you know two cards an opponent holds and they know two of yours, and it opens the option to build toward a reversis.",
      "fixes": "There is no decision before play that lets a player fix a bad deal, so the deal often decides the game before any reasoning happens."
    },
    {
      "what": "Fix the scoring: A=4, K=3, Q=2, J=1 per card taken, with the Quinola (J of hearts) worth 5 instead of 1. The total is 44 per hand. The winner is the player with the lowest total after 4 hands.",
      "why": "This gives one exact, arithmetic objective with no pools or payments.",
      "fixes": "Pools, talon payments, side payments and the variant Quinola bonuses are underspecified and not a winner rule the engine can use."
    },
    {
      "what": "Reversis: a player who takes all 6 tricks of a hand scores 0 for that hand, and each other player scores 15 instead of their card points.",
      "why": "This keeps the reversal with a stated payoff that is large but not game-ending. The three others must sometimes take a counter on purpose to break a sweep, which creates conflict among them.",
      "fixes": "The reversis reward ('wins outright, sweeps pools') is not stated as numbers, so its risk and reward cannot be weighed."
    }
  ],
  "keeps": [
    "Trick-avoidance with no trumps and strict follow-suit.",
    "The counting cards A=4, K=3, Q=2, J=1, with the lowest score winning.",
    "The Quinola (Jack of Hearts) as the special dangerous card.",
    "The reversis: taking every trick reverses the aim and punishes everyone else.",
    "Four players with hidden hands."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core trick-avoidance game rewards inference and planning. It only needs a smaller deck, several hands, passing and fixed scoring to fit and to reduce luck."
  },
  "variation": {
    "name": "Short Reversis",
    "summary": "A four-player no-trump trick-avoidance game over 4 hands of 6 tricks each, with secret card passing, a Quinola worth 5, and a reversis (taking all 6 tricks) that hands 15 points to each opponent. The lowest total wins.",
    "players": {
      "min": 4,
      "max": 4,
      "suggested": 4
    },
    "rules": "DECK: 24 cards, A K Q J 9 8 in each of the four suits (spades, hearts, diamonds, clubs). Rank within a suit, high to low: A, K, Q, J, 9, 8. There are no trumps.\n\nSEATS: Players 1 to 4 sit in a circle. Play goes from player 1 to 2 to 3 to 4 and back to 1. 'Left' means the next player in that order, 'right' the previous, and 'across' the player two seats away.\n\nGAME STRUCTURE: The game is 4 hands. Each hand is 7 rounds: one passing round followed by 6 trick rounds. That makes 28 rounds in total.\n\nPASSING ROUND (first round of each hand):\n(1) The deck is shuffled and each player is dealt 6 cards, seen only by that player.\n(2) In hands 1, 2 and 3, all players at the same moment each secretly choose 2 cards from their hand to pass. The passes go left in hand 1, right in hand 2 and across in hand 3. Passed cards are added to the receiver's hand after everyone has chosen, and only the passer and receiver know which cards moved. In hand 4 there is no pass.\n(3) The game announces that passing is complete.\n\nTRICK ROUNDS (6 per hand):\n- Lead: In the first trick of hand h, player h leads (player 1 in hand 1, player 2 in hand 2, and so on). In every later trick, the winner of the previous trick leads.\n- Playing: Starting with the leader and going around in seat order, each of the 4 players plays one card face up. The leader may play any card. Each other player must play a card of the led suit if they hold one. If they hold none, they may play any card.\n- Winning: The highest card of the led suit wins the trick. Cards of other suits never win.\n- Recording: The trick winner adds the trick's points to their score for this hand. Points per card: A=4, K=3, Q=2, J=1, with the Jack of Hearts (Quinola) worth 5. Nines and Eights are worth 0. The winner's trick count for the hand goes up by 1. All played cards are public.\n\nEND OF HAND (after the 6th trick):\n- If one player won all 6 tricks (a reversis), that player scores 0 for the hand and each other player scores 15 for the hand.\n- Otherwise each player scores the points they took. These always total 44 across the four players.\n- Hand scores are added to running totals, which are public. Hand scores and trick counts reset to 0.\n\nEND OF GAME: After the 4th hand, the game ends.",
    "objective": "After 4 hands, the player with the lowest running total wins. If two or more players tie for the lowest total, the game is a draw.",
    "expected_effect": "Averaging over four hands, equal first leads and passing to repair bad deals should make card reading and planning matter more than the deal. Passing creates targeted inference: you know two of a neighbour's cards, can pass a dangerous Quinola or Ace into a likely void, or can keep strength to try a reversis. The reversis threat stops pure ducking: when one player is sweeping, someone among the other three must take a counting trick to stop it, and each would prefer that someone else pays. This is a real conflict among the opponents. Across hands, players should steer points toward whoever leads the running totals. Simple policies lose: always playing the lowest legal card lets voids be exploited and lets a sweeper go unchecked, always playing the highest card collects most of the 44 points, and random play is beaten by any counting player. Talk is left out. Its main use would be loose ganging-up deals among three players, which the engine cannot enforce. Play order, the card passes and the cards played already carry the signals that are worth reasoning about, and talk would add steps without adding a decision."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 13,
    "choice_steps_per_round": 4,
    "attributes": 12,
    "hidden_elements": 1,
    "random_draws_per_round": 1,
    "rounds": 28
  }
}
```
````
