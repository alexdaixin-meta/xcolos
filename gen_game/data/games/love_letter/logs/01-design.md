# 01 design

- time: 2026-10-27T20:41:52+00:00 (79.9s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 176201f2ca8b9f89, reply sha256 42d5f811ff2dc481

## Sent

````
Original game: Love Letter
Players in the original: 2 to 4

Original rules:
Love Letter uses 16 cards ranked 1 Guard to 8 Princess with special effects. Shuffle the deck and burn one card face down unseen. In 2 players also reveal 3 cards face up as out of play. Each player gets one hidden card. On your turn draw one card then choose and discard one of your two cards face up in front of you, applying its effect even if harmful. Guard guesses an opponent's hand, Priest looks at a hand, Baron compares hands to eliminate loser, Handmaid protects you, Prince makes a player discard, King trades hands, Countess must be discarded if you also hold King or Prince, Princess eliminates you if discarded. If eliminated, reveal hand without effect. Round ends when one player remains or deck empties; then remaining players compare hands, highest wins tie by sum of discards. Winner gains a token of affection, and first player next round is previous winner. First game player is who was most recently on a date. First to 7 tokens in 2p, 5 in 3p, 4 in 4p wins.
````

## Reply

````
```json
{
  "original_summary": "Love Letter is a 2-4 player card game of deduction and elimination. Each player holds one hidden card; on each turn they draw a second card and discard one of the two, applying its effect: guessing, peeking, comparing, protecting, swapping or forcing discards. Winning a hand earns a token, and the first player to reach a token target wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No simple policy is safe. 'Always discard the higher card' throws away the Princess and eliminates you. 'Always discard the lower card' is a decent heuristic, but it plays Guards blindly and walks into Barons. 'Always guess the same rank' loses to a player who counts cards. Every choice can change who is eliminated. The first-player rule (most recently on a date, then the previous winner starts) is not arithmetic, and it lets the winner of a hand keep the tempo."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "A single hand is very luck-heavy. A lucky Guard guess on turn one, or being dealt the Princess against a Baron, decides it. Skill only shows over many hands. The 2-player token target of 7 helps but is too long for the platform, while the 4-player target of 4 is short and noisy."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Strong play involves counting the publicly visible cards, reading what an opponent kept from what they discarded, timing the Handmaid, and bluffing through discards. A weak player still wins some hands. The game is not solved."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands are hidden, and the main skill is inferring the opponent's card from public discards, the face-up removed cards and their discard choices. A Guard guess is a probability judgement, and a Priest look gives private information you can exploit later."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Eliminations, the comparison of cards when the deck runs out, the tie-break on discard sums and the token count are all arithmetic. The only non-arithmetic rule is the 'last on a date' start, which is trivial to replace."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The game is turn-based and text-only, but it has 8 card types with separate effects. The Prince adds a second draw within a turn and can empty the deck mid-turn. Tokens are carried across hands with variable targets by player count. A 4-player multi-hand match can exceed 40 turns. Each step can be built, but the full card set plus the hand resets crowds the step and attribute limits."
    }
  ],
  "problems": [
    "P1: The full card set (8 types including the Prince, whose forced discard needs an extra draw and can empty the deck mid-turn) costs too many steps and edge cases for the engine.",
    "P2: Token targets of 4-7 across 2-4 players make the match too long, so it does not fit inside 40 turns.",
    "P3: The first-player rule is not arithmetic ('most recently on a date'), and 'the winner starts next hand' compounds the edge of whoever is already ahead.",
    "P4: Luck in a single hand is high; one blind Guard hit can decide it, so the match has to aggregate enough hands for deduction to show.",
    "P5: With 3-4 players there is extra chaos (being targeted is out of your control) and much more state to track, which weakens skill sensitivity and adds steps."
  ],
  "changes": [
    {
      "what": "Remove the Prince and use a 14-card deck: 5 Guard (1), 2 Priest (2), 2 Baron (3), 2 Handmaid (4), 1 King (6), 1 Countess (7), 1 Princess (8). The Countess must be discarded if held together with the King.",
      "why": "Exactly one card is drawn per turn and the deck can never run out mid-turn. All the other effects become single conditional steps, and the core of guessing, peeking, comparing, protecting, swapping and the Princess is kept.",
      "fixes": "P1: The full card set (8 types including the Prince, whose forced discard needs an extra draw and can empty the deck mid-turn) costs too many steps and edge cases for the engine."
    },
    {
      "what": "Fix the game at 2 players. Each hand: shuffle, set aside 1 card face down, reveal 3 face up out of play, and deal 1 to each player, leaving 8 cards to draw. The match goes to 3 tokens, with a hard cap of 40 turns.",
      "why": "A hand lasts at most 8 turns and a first-to-3 match lasts at most 5 hands, so 40 turns always suffice. The 3 face-up cards give public information to reason from.",
      "fixes": "P2: Token targets of 4-7 across 2-4 players make the match too long, so it does not fit inside 40 turns."
    },
    {
      "what": "The first hand's starting player is chosen at random. After that, the loser of the previous hand starts the next one. If no token was awarded, the player who did not start the previous hand starts.",
      "why": "This replaces the non-arithmetic date rule and gives the trailing player the tempo, offsetting the first-move edge instead of compounding it.",
      "fixes": "P3: The first-player rule is not arithmetic ('most recently on a date'), and 'the winner starts next hand' compounds the edge of whoever is already ahead."
    },
    {
      "what": "Use a best-of-five-hands structure (first to 3 tokens). All discards stay public and the 3 face-up cards are visible, so card counting is always possible. A Guard may not name Guard.",
      "why": "Aggregating several hands cuts the effect of one lucky draw, and the public information makes each Guard guess and Baron challenge a calculable judgement rather than a coin flip.",
      "fixes": "P4: Luck in a single hand is high; one blind Guard hit can decide it, so the match has to aggregate enough hands for deduction to show."
    },
    {
      "what": "Drop the 3-4 player modes and the talk phase.",
      "why": "Heads-up play makes every effect target the one opponent, keeps the state small, and turns the game into pure mutual deduction. With two players there is no coalition dynamic for talk to add.",
      "fixes": "P5: With 3-4 players there is extra chaos (being targeted is out of your control) and much more state to track, which weakens skill sensitivity and adds steps."
    }
  ],
  "keeps": [
    "One hidden card in hand; draw one, discard one, and apply its effect even when it hurts you.",
    "The Guard guess, Priest peek, Baron comparison, Handmaid protection, King swap, the Countess's forced discard and the Princess's self-elimination.",
    "The 2-player setup of one card set aside unseen and three revealed out of play.",
    "When the deck runs out, the higher card wins the hand, with ties broken by the sum of discards.",
    "Tokens of affection carried across hands, with the first to reach the target winning."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The deduction core fits the platform once the Prince is removed and the game is fixed at 2 players with a short token race that fits inside 40 turns."
  },
  "variation": {
    "name": "Love Letter: Heads-Up",
    "summary": "A two-player Love Letter with a 14-card deck and no Prince, played as a race to 3 tokens. The loser of each hand starts the next one.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "CARDS (14):\n- 5 Guard (rank 1)\n- 2 Priest (rank 2)\n- 2 Baron (rank 3)\n- 2 Handmaid (rank 4)\n- 1 King (rank 6)\n- 1 Countess (rank 7)\n- 1 Princess (rank 8)\n\nSTARTING A HAND:\n1. Gather all 14 cards and shuffle them.\n2. Set the top card aside face down. Nobody sees it, and it takes no part in the hand.\n3. Reveal the next 3 cards face up as out of play. Everyone sees them.\n4. Deal 1 card face down to each player as their hand. 8 cards remain in the draw deck.\n5. Clear both players' protection, elimination and discard piles.\n6. Starting player: in hand 1 it is chosen at random. In later hands it is the player who lost the previous hand. If the previous hand gave no token, it is the player who did not start the previous hand.\n\nA TURN (players alternate, starting with the starting player):\n1. If the active player is protected, their protection ends now.\n2. The active player draws the top card of the deck, so they hold 2 cards. Only they see their cards.\n3. The active player chooses one of their 2 cards to discard face up. Discards are public, and their ranks are added to that player's discard sum.\n   - If they hold the Countess together with the King, they must discard the Countess.\n   - They may discard the Princess, but then they are eliminated.\n4. The discarded card's effect applies:\n   - Guard: if the opponent is not protected, the active player names one rank other than 1 (2, 3, 4, 6, 7 or 8). If the opponent's card has that rank, the opponent is eliminated.\n   - Priest: if the opponent is not protected, the active player privately sees the opponent's card.\n   - Baron: if the opponent is not protected, both players privately see each other's card. The player with the lower rank is eliminated. On equal ranks nothing happens.\n   - Handmaid: the active player is protected until the start of their next turn. Cards discarded by the opponent have no effect on a protected player.\n   - King: if the opponent is not protected, the two players swap their hand cards.\n   - Countess: no effect.\n   - Princess: the active player is eliminated.\n5. The discard and its public outcome are announced: the guess named, whether someone was eliminated, whether a swap happened. The cards seen privately through a Priest or Baron are not announced, except that an eliminated player's card is revealed.\n\nEND OF A HAND:\n- If a player is eliminated, the other player wins the hand.\n- Otherwise, if the deck is empty at the end of a turn, both players reveal their cards and the higher rank wins the hand.\n- If the ranks are equal, the higher discard sum wins the hand.\n- If the discard sums are also equal, nobody wins the hand.\n- The hand's winner gains 1 token.\n- If the game has not ended, a new hand starts as described above.\n\nEND OF THE GAME:\n- The first player to reach 3 tokens wins at once.\n- There is a hard cap of 40 turns, which cannot be reached in normal play because a hand lasts at most 8 turns and the match at most 5 hands. If the cap is reached anyway, any hand in progress is resolved as if the deck were empty. Then the player with more tokens wins, and equal tokens is a draw.",
    "objective": "The first player to hold 3 tokens wins. If the 40-turn cap is reached first, the player with more tokens wins, and equal tokens is a draw.",
    "expected_effect": "Every turn is a small deduction problem. There are 14 cards in total, 3 are visible from the start, and every discard is public, so players can work out the probability of each rank for the opponent's card. They can pick Guard guesses accordingly, judge when a Baron challenge is favourable, and read what the opponent's discard choices reveal about the card they kept. A Priest peek creates an information edge that a King swap can erase, which rewards planning across turns. Removing the Prince keeps the rules within the engine. The race to 3 tokens with the loser starting next hand dilutes single-hand luck and removes the first-player snowball, so the more careful counter should win most matches. With two players and opposed interests, talk is left out."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 16,
    "choice_steps_per_round": 2,
    "attributes": 16,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 40
  }
}
```
````
