# Variation: Love Letter: Sealed Stakes

This is two-player Love Letter. Before each hand's play, both players secretly stake 1-3 tokens' worth on their card, and the winner of the hand takes the pot. Starters alternate, the match always has an even number of hands, and it ends after the first even-numbered hand at which 24 or more turns have been played.

Players: 2 to 2, best with 2

## Review of the original

Love Letter is a 2-4 player card game played with 16 cards. Each player holds one hidden card, draws a second each turn and discards one, applying its effect: guessing, peeking, comparing, protecting, forcing a discard or swapping hands. A hand ends when one player is left or the deck runs out, and the winner of the hand gains a token. The match is played to a token target.

- **non_degenerate**: weak. In the original, no simple policy wins. 'Always discard the lower card' loses to Guard guesses and Baron comparisons. 'Always guess Guard-rank 2' is easily exploited. However, the starting player keeps going first after each win, so a winner snowballs. In the previous variation, alternating starts fixed that, but the hand-1 starter was random. With a hand count that could be odd, one player could get one more start than the other: a small built-in edge.
- **skill_sensitive**: weak. The original awards one token per hand, so a single lucky Guard guess on turn 1 is worth the same as a hand won through careful deduction. Hands are short and swingy. The stake mechanic in the previous variation (a secret stake of 1-3 set after seeing your card) lets a skilled player bet big on strong hands and small on weak ones. That moves the weight toward judgement. It is kept.
- **headroom**: good. Weak players still win hands through the draw. Strong players improve through card counting with 5 cards revealed, posterior Guard guesses, reading what a stake says about an opponent's card, Handmaid timing and King/Prince tactics. It is not solved.
- **reasoning_dependent**: good. The core of the game is inference about one hidden card. You combine the public discards, the 5 revealed cards, Priest and Baron information and the opponent's stake to estimate their hand, then guess, compare or protect.
- **verifiable**: good. Eliminations, showdown ranks, discard-sum tie-breaks and token totals are all arithmetic. The original's 'most recently on a date' starter rule is the only non-arithmetic element. It was removed.
- **fits_platform**: weak. The game is turn-based, text-only and has no board. The previous variation fit every limit except one. In the first round of hand 1 it used two random operations: the shuffle and a random choice of starter. That exceeds random_draws_per_round = 1 and contradicts its stated complexity. Its match length, up to 39 turns, is within 40 rounds.

## Problems

- The previous variation used two random operations in the first round (the shuffle and a random choice of the hand-1 starter), breaking the limit of 1 random draw per round.
- Ending the match at the first hand that reaches 32 turns could leave an odd number of hands, so one seat (decided at random) started one more hand than the other: a small seat edge.
- Original only: the 'most recently on a date' starter rule is not arithmetic, and winner-starts-next-hand snowballs the leader.
- Original only: a flat one token per hand lets a single lucky early Guard guess count as much as a deduced win, which weakens skill sensitivity.

## Changes

- Hand 1 is always started by Player A, a fixed seat. The starter then alternates every hand. No random choice of starter remains. (fixes: The previous variation used two random operations in the first round (the shuffle and a random choice of the hand-1 starter), breaking the limit of 1 random draw per round.): The shuffle is then the only random operation in any round, so random_draws_per_round truly equals 1.
- The match ends only at the end of an even-numbered hand, specifically the first even-numbered hand after which 24 or more turns have been played in total. The threshold drops from 32 to 24 so the worst case still fits in 40 rounds: at most 23 turns, plus an odd hand of up to 8, plus an even hand of up to 8, gives 39. (fixes: Ending the match at the first hand that reaches 32 turns could leave an odd number of hands, so one seat (decided at random) started one more hand than the other: a small seat edge.): Because starts alternate and the hand count is always even, each player starts exactly half the hands. Giving hand 1 to a fixed seat then creates no edge.
- Keep alternating starters instead of winner-starts, and give hand 1 to a fixed seat instead of using the dating rule. (fixes: Original only: the 'most recently on a date' starter rule is not arithmetic, and winner-starts-next-hand snowballs the leader.): This removes the non-arithmetic rule and the snowball.
- Keep the secret simultaneous stake of 1-3 per player, set after each player sees their own card. The hand's pot is the sum of the two stakes. (fixes: Original only: a flat one token per hand lets a single lucky early Guard guess count as much as a deduced win, which weakens skill sensitivity.): Hands won on a strong read with a high stake are worth more than lucky low-stake hands. Each stake also leaks information the opponent can reason about.

## Kept from the original

- The 16-card deck with its ranks and effects: Guard, Priest, Baron, Handmaid, Prince, King, Countess, Princess.
- The two-player setup: burn 1 card unseen and reveal 5 cards as out of play (5 rather than the original's 3), so each player holds 1 hidden card and draws to 2 each turn.
- The forced Countess discard and Princess self-elimination.
- Showdown by rank with the discard-sum tie-break.
- Winning hands to gain tokens of affection, with most tokens winning the match.

## The variation's rules

PLAYERS: Player A and Player B.

CARDS (16):
- 5 Guard (rank 1)
- 2 Priest (rank 2)
- 2 Baron (rank 3)
- 2 Handmaid (rank 4)
- 2 Prince (rank 5)
- 1 King (rank 6)
- 1 Countess (rank 7)
- 1 Princess (rank 8)

MATCH STATE: Both players start the match with 0 tokens. Token totals are always public. The match publicly counts turns played (starting at 0) and hands played (starting at 0).

STARTING A HAND (happens at the start of the first turn of each new hand):
1. Add 1 to the hand count. Shuffle all 16 cards. This is the only random event; it happens at most once per turn.
2. Burn the top card: set it aside face down, unseen by anyone.
3. Reveal the next 5 cards face up as out of play. Both players see them.
4. Deal 1 card face down to each player as their hand. Each player sees only their own card. 8 cards remain in the draw deck.
5. Clear both players' protection, elimination flag, discard pile and discard sum (each discard sum becomes 0).
6. Starting player: Player A starts odd-numbered hands (1, 3, 5, ...). Player B starts even-numbered hands (2, 4, 6, ...).
7. STAKE: each player looks at their own card. Both then choose, at the same moment and in secret, a stake of 1, 2 or 3. Both stakes are then revealed to both players. The pot for this hand is stake A plus stake B, so it is between 2 and 6.

A TURN (players alternate within a hand, beginning with that hand's starting player; every turn adds 1 to the turn count):
1. If the active player is protected, their protection ends now.
2. The active player draws the top card of the deck and now holds 2 cards. Only they see them.
3. The active player chooses one of their 2 cards to discard face up. The card's rank is added to their discard sum.
   - If one of the 2 cards is the Countess and the other is the King or a Prince, they must discard the Countess.
   - They may discard the Princess, but that eliminates them.
4. The discarded card's effect applies:
   - Guard: if the opponent is not protected, the active player names one rank from 2 to 8. If the opponent's card has that rank, the opponent is eliminated. If the opponent is protected, no rank is named and nothing happens.
   - Priest: if the opponent is not protected, the active player privately sees the opponent's card.
   - Baron: if the opponent is not protected, both players privately see each other's card. The player with the lower rank is eliminated. If the ranks are equal, nothing happens.
   - Handmaid: the active player is protected until the start of their own next turn. While a player is protected, the opponent's discards have no effect on them.
   - Prince: the active player chooses a player, either themself or the opponent. They may choose the opponent only if the opponent is not protected; otherwise they must choose themself. The chosen player discards their hand card face up without applying its effect, and its rank is added to their discard sum. If that card is the Princess, the chosen player is eliminated. Otherwise the chosen player draws the top card of the deck, or takes the burned card if the deck is empty.
   - King: if the opponent is not protected, the two players swap hand cards.
   - Countess: no effect.
   - Princess: the active player is eliminated.
5. Announce publicly:
   - the card discarded;
   - any rank named;
   - any Prince target and the card it discarded;
   - any elimination, together with the eliminated player's hand card;
   - whether a swap happened.
   Cards seen privately through a Priest or Baron are not announced.

END OF A HAND (checked at the end of every turn):
- If a player is eliminated, the other player wins the hand.
- Otherwise, if the draw deck is empty, both players reveal their cards. The higher rank wins. If the ranks are equal, the higher discard sum wins. If the sums are also equal, nobody wins the hand.
- Otherwise the hand continues with the other player's turn.
- When a hand ends, its winner gains tokens equal to the pot. If nobody wins, no tokens are given.
- A hand lasts at most 8 turns.

END OF THE MATCH (checked whenever a hand ends):
- If the hand count is even and 24 or more turns have been played in total, the match ends.
- Otherwise a new hand starts on the next turn.
- The match therefore always has an even number of hands, each player starts exactly half of them, and it ends by turn 39 at the latest.

Objective: When the match ends, the player with more tokens wins. Equal token totals are a draw.

Expected effect: The starter edge is now exactly balanced, because the hand count is always even and starts alternate. Hand 1 needs no random choice, so every round has at most one random event, the shuffle. A match typically runs 4-6 hands. Play centres on inference about the opponent's single hidden card from discards, revealed cards, Priest and Baron peeks, and the opponent's stake. Stake sizing rewards accurate self-assessment and punishes predictable staking: always staking 3 risks big losses on weak cards, while always staking 1 forfeits value on strong ones, and either can lose. The game is zero-sum with two players, so no talk phase is needed and endgame unravelling does not apply.

## Complexity (the designer's count, against the limits)

- steps_per_round: 18 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 15 (limit 20)
- hidden_elements: 3 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 39 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
