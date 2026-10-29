# 05 design

- time: 2026-10-27T20:47:15+00:00 (54.0s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 6e0498caabec92f3, reply sha256 a7b6bab564c9ff73

## Sent

````
Original game: Love Letter
Players in the original: 2 to 4

Original rules:
Love Letter uses 16 cards ranked 1 Guard to 8 Princess with special effects. Shuffle the deck and burn one card face down unseen. In 2 players also reveal 3 cards face up as out of play. Each player gets one hidden card. On your turn draw one card then choose and discard one of your two cards face up in front of you, applying its effect even if harmful. Guard guesses an opponent's hand, Priest looks at a hand, Baron compares hands to eliminate loser, Handmaid protects you, Prince makes a player discard, King trades hands, Countess must be discarded if you also hold King or Prince, Princess eliminates you if discarded. If eliminated, reveal hand without effect. Round ends when one player remains or deck empties; then remaining players compare hands, highest wins tie by sum of discards. Winner gains a token of affection, and first player next round is previous winner. First game player is who was most recently on a date. First to 7 tokens in 2p, 5 in 3p, 4 in 4p wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- playable FAILED: RULES. The card count checks: 16 - 1 burned - 5 revealed - 2 dealt = 8 deck cards. The deck can never be empty at the start of a turn. If a Prince on turn 7 takes the last deck card, the end-of-turn check triggers a showdown. A Prince on turn 8 takes the burned card. So 'at most 8 turns per hand' holds, and the match ends by turn 39.
All effects are specified, including the protected cases (Prince must self-target if the opponent is protected), the Countess rule, Princess discard, showdown, tie-break by discard sum, and no-winner ties. Public and private information is spelled out. The game is finite and decided by token arithmetic. There is no board, clock or judge. The stake is correctly a simultaneous secret choice. Two players means no talk phase is needed. The game is zero-sum, so the repeated-cooperation test is not relevant.
LIMITS.
- Steps: 18 of 20.
- Choice steps: stake, discard, and Guard guess / Prince target, giving 3 or 4 of 4.
- Attributes: 14 of 20.
- Hidden elements: 2 hands plus deck order with the burned card as its tail, giving 3 of 3.
- Rounds: 39-40 of 40.
VIOLATION. random_draws_per_round is limited to 1. The first round of hand 1 needs two random operations: the shuffle in step 1, and step 6, 'in hand 1 it is chosen at random'. That breaks the stated limit. The stated complexity (random_draws_per_round: 1) does not match the rules as written.
- change: Playable: remove the second random operation in the first round. Derive the hand-1 starter from the shuffle already performed, for example: 'the player who starts hand 1 is player A if the burned card's rank is odd, otherwise player B', resolved at match end or kept hidden until needed. Or give the hand-1 start to a fixed seat. Then random_draws_per_round truly stays at 1 and matches the stated complexity.
- change: Optional, for balance: to remove the small odd-hand-count starter edge, end the match only after a hand that leaves both players with an equal number of starts, for example 'the match ends at the end of the first even-numbered hand that ends with 32 or more turns played'. Then raise the turn bound and rounds accordingly, keeping them at or under 40, or lower 32 to 28.
The variation that was reviewed: Love Letter: Sealed Stakes: CARDS (16):
- 5 Guard (rank 1)
- 2 Priest (rank 2)
- 2 Baron (rank 3)
- 2 Handmaid (rank 4)
- 2 Prince (rank 5)
- 1 King (rank 6)
- 1 Countess (rank 7)
- 1 Princess (rank 8)

Both players start the match with 0 tokens. Token totals are always public. The match counts turns played.

STARTING A HAND (happens whenever a new hand begins):
1. Shuffle all 16 cards.
2. Burn the top card: set it aside face down, unseen by anyone.
3. Reveal the next 5 cards face up as out of play. Both players see them.
4. Deal 1 card face down to each player as their hand. 8 cards remain in the draw deck.
5. Clear both players' protection, elimination flag, discard pile and discard sum.
6. Starting player: in hand 1 it is chosen at random. In each later hand it is the player who did not start the previous hand.
7. STAKE: each player looks at their own card. Both then choose, at the same moment and in secret, a stake of 1, 2 or 3. The two stakes are revealed to both players. The pot for this hand is stake A plus stake B, so it is between 2 and 6.

A TURN (players alternate, beginning with the starting player; every turn adds 1 to the turn count):
1. If the active player is protected, their protection ends now.
2. The active player draws the top card of the deck and now holds 2 cards. Only they see them.
3. The active player chooses one of their 2 cards to discard face up. The card's rank is added to their discard sum.
   - If one of the 2 cards is the Countess and the other is the King or a Prince, they must discard the Countess.
   - They may discard the Princess, but that eliminates them.
4. The discarded card's effect applies:
   - Guard: if the opponent is not protected, name one rank from 2 to 8. If the opponent's card has that rank, the opponent is eliminated.
   - Priest: if the opponent is not protected, the active player privately sees the opponent's card.
   - Baron: if the opponent is not protected, both players privately see each other's card. The lower rank is eliminated. Equal ranks: nothing happens.
   - Handmaid: the active player is protected until the start of their own next turn. While a player is protected, the opponent's discards have no effect on them.
   - Prince: choose a player, either yourself or the opponent. You may choose the opponent only if they are not protected. The chosen player discards their hand card face up without its effect, and its rank is added to their discard sum. If that card is the Princess, they are eliminated. Otherwise they draw the top card of the deck, or take the burned card if the deck is empty.
   - King: if the opponent is not protected, the two players swap hand cards.
   - Countess: no effect.
   - Princess: the active player is eliminated.
5. Announce publicly: the card discarded, any rank named, any Prince target and the card it discarded, any elimination together with the eliminated player's card, and whether a swap happened. Cards seen privately through a Priest or Baron are not announced.

END OF A HAND (checked at the end of every turn):
- If a player is eliminated, the other player wins the hand.
- Otherwise, if the deck is empty, both players reveal their cards. The higher rank wins. If the ranks are equal, the higher discard sum wins. If the sums are also equal, nobody wins the hand.
- The winner of the hand gains tokens equal to the pot. If nobody wins, no tokens are given.

END OF THE MATCH:
- When a hand ends, if fewer than 32 turns have been played in total, a new hand starts.
- If 32 or more turns have been played, the match ends.
- A hand lasts at most 8 turns, so the match always ends by turn 39. Winner: When the match ends, the player with more tokens wins. Equal token totals are a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Love Letter is a 2-4 player card game played with 16 cards. Each player holds one hidden card, draws a second each turn and discards one, applying its effect: guessing, peeking, comparing, protecting, forcing a discard or swapping hands. A hand ends when one player is left or the deck runs out, and the winner of the hand gains a token. The match is played to a token target.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "weak",
      "evidence": "In the original, no simple policy wins. 'Always discard the lower card' loses to Guard guesses and Baron comparisons. 'Always guess Guard-rank 2' is easily exploited. However, the starting player keeps going first after each win, so a winner snowballs. In the previous variation, alternating starts fixed that, but the hand-1 starter was random. With a hand count that could be odd, one player could get one more start than the other: a small built-in edge."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "The original awards one token per hand, so a single lucky Guard guess on turn 1 is worth the same as a hand won through careful deduction. Hands are short and swingy. The stake mechanic in the previous variation (a secret stake of 1-3 set after seeing your card) lets a skilled player bet big on strong hands and small on weak ones. That moves the weight toward judgement. It is kept."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Weak players still win hands through the draw. Strong players improve through card counting with 5 cards revealed, posterior Guard guesses, reading what a stake says about an opponent's card, Handmaid timing and King/Prince tactics. It is not solved."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "The core of the game is inference about one hidden card. You combine the public discards, the 5 revealed cards, Priest and Baron information and the opponent's stake to estimate their hand, then guess, compare or protect."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Eliminations, showdown ranks, discard-sum tie-breaks and token totals are all arithmetic. The original's 'most recently on a date' starter rule is the only non-arithmetic element. It was removed."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The game is turn-based, text-only and has no board. The previous variation fit every limit except one. In the first round of hand 1 it used two random operations: the shuffle and a random choice of starter. That exceeds random_draws_per_round = 1 and contradicts its stated complexity. Its match length, up to 39 turns, is within 40 rounds."
    }
  ],
  "problems": [
    "The previous variation used two random operations in the first round (the shuffle and a random choice of the hand-1 starter), breaking the limit of 1 random draw per round.",
    "Ending the match at the first hand that reaches 32 turns could leave an odd number of hands, so one seat (decided at random) started one more hand than the other: a small seat edge.",
    "Original only: the 'most recently on a date' starter rule is not arithmetic, and winner-starts-next-hand snowballs the leader.",
    "Original only: a flat one token per hand lets a single lucky early Guard guess count as much as a deduced win, which weakens skill sensitivity."
  ],
  "changes": [
    {
      "what": "Hand 1 is always started by Player A, a fixed seat. The starter then alternates every hand. No random choice of starter remains.",
      "why": "The shuffle is then the only random operation in any round, so random_draws_per_round truly equals 1.",
      "fixes": "The previous variation used two random operations in the first round (the shuffle and a random choice of the hand-1 starter), breaking the limit of 1 random draw per round."
    },
    {
      "what": "The match ends only at the end of an even-numbered hand, specifically the first even-numbered hand after which 24 or more turns have been played in total. The threshold drops from 32 to 24 so the worst case still fits in 40 rounds: at most 23 turns, plus an odd hand of up to 8, plus an even hand of up to 8, gives 39.",
      "why": "Because starts alternate and the hand count is always even, each player starts exactly half the hands. Giving hand 1 to a fixed seat then creates no edge.",
      "fixes": "Ending the match at the first hand that reaches 32 turns could leave an odd number of hands, so one seat (decided at random) started one more hand than the other: a small seat edge."
    },
    {
      "what": "Keep alternating starters instead of winner-starts, and give hand 1 to a fixed seat instead of using the dating rule.",
      "why": "This removes the non-arithmetic rule and the snowball.",
      "fixes": "Original only: the 'most recently on a date' starter rule is not arithmetic, and winner-starts-next-hand snowballs the leader."
    },
    {
      "what": "Keep the secret simultaneous stake of 1-3 per player, set after each player sees their own card. The hand's pot is the sum of the two stakes.",
      "why": "Hands won on a strong read with a high stake are worth more than lucky low-stake hands. Each stake also leaks information the opponent can reason about.",
      "fixes": "Original only: a flat one token per hand lets a single lucky early Guard guess count as much as a deduced win, which weakens skill sensitivity."
    }
  ],
  "keeps": [
    "The 16-card deck with its ranks and effects: Guard, Priest, Baron, Handmaid, Prince, King, Countess, Princess.",
    "The two-player setup: burn 1 card unseen and reveal 5 cards as out of play (5 rather than the original's 3), so each player holds 1 hidden card and draws to 2 each turn.",
    "The forced Countess discard and Princess self-elimination.",
    "Showdown by rank with the discard-sum tie-break.",
    "Winning hands to gain tokens of affection, with most tokens winning the match."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The previous variation was sound except for the extra random draw and a small parity edge. Both are fixed with a fixed hand-1 seat and an even-hand ending, and everything stays within limits."
  },
  "variation": {
    "name": "Love Letter: Sealed Stakes",
    "summary": "This is two-player Love Letter. Before each hand's play, both players secretly stake 1-3 tokens' worth on their card, and the winner of the hand takes the pot. Starters alternate, the match always has an even number of hands, and it ends after the first even-numbered hand at which 24 or more turns have been played.",
    "players": {"min": 2, "max": 2, "suggested": 2},
    "rules": "PLAYERS: Player A and Player B.\n\nCARDS (16):\n- 5 Guard (rank 1)\n- 2 Priest (rank 2)\n- 2 Baron (rank 3)\n- 2 Handmaid (rank 4)\n- 2 Prince (rank 5)\n- 1 King (rank 6)\n- 1 Countess (rank 7)\n- 1 Princess (rank 8)\n\nMATCH STATE: Both players start the match with 0 tokens. Token totals are always public. The match publicly counts turns played (starting at 0) and hands played (starting at 0).\n\nSTARTING A HAND (happens at the start of the first turn of each new hand):\n1. Add 1 to the hand count. Shuffle all 16 cards. This is the only random event; it happens at most once per turn.\n2. Burn the top card: set it aside face down, unseen by anyone.\n3. Reveal the next 5 cards face up as out of play. Both players see them.\n4. Deal 1 card face down to each player as their hand. Each player sees only their own card. 8 cards remain in the draw deck.\n5. Clear both players' protection, elimination flag, discard pile and discard sum (each discard sum becomes 0).\n6. Starting player: Player A starts odd-numbered hands (1, 3, 5, ...). Player B starts even-numbered hands (2, 4, 6, ...).\n7. STAKE: each player looks at their own card. Both then choose, at the same moment and in secret, a stake of 1, 2 or 3. Both stakes are then revealed to both players. The pot for this hand is stake A plus stake B, so it is between 2 and 6.\n\nA TURN (players alternate within a hand, beginning with that hand's starting player; every turn adds 1 to the turn count):\n1. If the active player is protected, their protection ends now.\n2. The active player draws the top card of the deck and now holds 2 cards. Only they see them.\n3. The active player chooses one of their 2 cards to discard face up. The card's rank is added to their discard sum.\n   - If one of the 2 cards is the Countess and the other is the King or a Prince, they must discard the Countess.\n   - They may discard the Princess, but that eliminates them.\n4. The discarded card's effect applies:\n   - Guard: if the opponent is not protected, the active player names one rank from 2 to 8. If the opponent's card has that rank, the opponent is eliminated. If the opponent is protected, no rank is named and nothing happens.\n   - Priest: if the opponent is not protected, the active player privately sees the opponent's card.\n   - Baron: if the opponent is not protected, both players privately see each other's card. The player with the lower rank is eliminated. If the ranks are equal, nothing happens.\n   - Handmaid: the active player is protected until the start of their own next turn. While a player is protected, the opponent's discards have no effect on them.\n   - Prince: the active player chooses a player, either themself or the opponent. They may choose the opponent only if the opponent is not protected; otherwise they must choose themself. The chosen player discards their hand card face up without applying its effect, and its rank is added to their discard sum. If that card is the Princess, the chosen player is eliminated. Otherwise the chosen player draws the top card of the deck, or takes the burned card if the deck is empty.\n   - King: if the opponent is not protected, the two players swap hand cards.\n   - Countess: no effect.\n   - Princess: the active player is eliminated.\n5. Announce publicly:\n   - the card discarded;\n   - any rank named;\n   - any Prince target and the card it discarded;\n   - any elimination, together with the eliminated player's hand card;\n   - whether a swap happened.\n   Cards seen privately through a Priest or Baron are not announced.\n\nEND OF A HAND (checked at the end of every turn):\n- If a player is eliminated, the other player wins the hand.\n- Otherwise, if the draw deck is empty, both players reveal their cards. The higher rank wins. If the ranks are equal, the higher discard sum wins. If the sums are also equal, nobody wins the hand.\n- Otherwise the hand continues with the other player's turn.\n- When a hand ends, its winner gains tokens equal to the pot. If nobody wins, no tokens are given.\n- A hand lasts at most 8 turns.\n\nEND OF THE MATCH (checked whenever a hand ends):\n- If the hand count is even and 24 or more turns have been played in total, the match ends.\n- Otherwise a new hand starts on the next turn.\n- The match therefore always has an even number of hands, each player starts exactly half of them, and it ends by turn 39 at the latest.",
    "objective": "When the match ends, the player with more tokens wins. Equal token totals are a draw.",
    "expected_effect": "The starter edge is now exactly balanced, because the hand count is always even and starts alternate. Hand 1 needs no random choice, so every round has at most one random event, the shuffle. A match typically runs 4-6 hands. Play centres on inference about the opponent's single hidden card from discards, revealed cards, Priest and Baron peeks, and the opponent's stake. Stake sizing rewards accurate self-assessment and punishes predictable staking: always staking 3 risks big losses on weak cards, while always staking 1 forfeits value on strong ones, and either can lose. The game is zero-sum with two players, so no talk phase is needed and endgame unravelling does not apply."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 18,
    "choice_steps_per_round": 4,
    "attributes": 15,
    "hidden_elements": 3,
    "random_draws_per_round": 1,
    "rounds": 39
  }
}
```
````
