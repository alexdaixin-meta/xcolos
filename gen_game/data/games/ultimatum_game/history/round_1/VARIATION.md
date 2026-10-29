# Variation: Hidden Pie Ultimatum III

Three players take turns proposing how to split a pot whose size only the Proposer knows. Every player plays each of the pot values 70, 90, 110 and 130 exactly once, in random order. One acceptance passes a deal; a rejected share is burned. Highest total after 12 rounds wins.

Players: 3 to 3, best with 3

## Review of the original

A two-player, one-shot bargain. A Proposer offers the Responder a share S of 100 units. If the Responder accepts, the split stands; if the Responder rejects, both get nothing.

- **non_degenerate**: bad. The original game fails. Under 'higher total wins' with two players only the difference counts. A Responder should reject any S below 50, and a Proposer offering exactly 50 can at worst draw, so 'offer 50' never loses and 'reject below 50' never loses. The game collapses to a forced 50/50 draw, and the Proposer seat is decided by that one rule. The previous 3-player variation fixed the proposal rounds: 0/0 offers get rejected, over-offers lose, always-accept is exploited, and always-reject falls behind accepters. But its round-10 Split Demand let a leader demand 60 and never fall behind.
- **skill_sensitive**: bad. The original is one decision with a known pie, so there is no gap for skill to exploit. In the previous variation, players drew 3 of 4 pot values, which gave pot totals of 270 to 330. Under both sensible strategies (fixed offers, or offering a third of the pot each), the winner was whoever left out the lowest value, or the tie-break went to whoever drew small pots. Luck decided.
- **headroom**: weak. The original is solved instantly at 50/50. The 3-player hidden-pot version does have room to improve: reading the pot from the offer and the remaining list, playing one Responder off the other, and choosing when to reject to cut down a leader.
- **reasoning_dependent**: bad. In the original the pie, the offer and the rules are all public, so there is nothing to infer. The previous variation added a hidden pot, but the deal decided the result, so the inference did not decide the winner.
- **verifiable**: good. All payoffs are sums and differences of announced numbers. The winner is the highest total, by arithmetic.
- **fits_platform**: weak. The original is text-only and turn-based but is a single move. The previous variation fit the limits only if the pot lists were game lists, and it needed a special round 10 with its own per-step conditions.

## Problems

- P1: In the original 2-player 'higher total wins' setting, 'offer 50' and 'reject below 50' can never lose, so the game is a forced draw.
- P2: The original has no hidden information and only one move, so there is nothing to infer and nothing to plan.
- P3: In the previous variation, each player played only 3 of 4 pot values, so total pie differed by up to 60 points and decided the winner under good play (the lottery trap).
- P4: The previous tie-break, highest Responder-gains tally, rose as one's own drawn pots fell, so the draw also decided ties.
- P5: The previous Split Demand round 10 was a safe-option collapse. Demanding 60 was never behind, which locked in the leader and let anyone block at no cost.
- P6: Last-proposer edge: P3 alone made the final proposal with full knowledge of the scores, and P1 alone proposed first with the least information.
- P7: The attribute count was over 20 unless the pot lists were stated to be game lists.

## Changes

- Three players. A proposal passes if at least one of two Responders accepts, and a rejected share is burned. (fixes: P1): With three players one rival's gain is not the other's loss. Two Responders compete for the offer, and a lone holdout punishes the Proposer only partly, so offering the minimum, rejecting everything or offering a fair split can each lose.
- The pot is hidden from the Responders. Each player has the list 70/90/110/130 and is told the pot only when it is drawn; the pot is revealed after the round. (fixes: P2): Responders must infer the pot from the offer size and from the values the Proposer has not yet played.
- 12 proposal rounds. Each player proposes exactly 4 times and plays every pot value once; only the order is random. (fixes: P3): Every player's pie is exactly 400, so the deal changes only what is known, not who is ahead. Under symmetric fair play everyone ends on 400 and the game is a draw.
- The tie-break is removed. A tie for the highest total is a draw. (fixes: P4): No tie-break that depends on the draw.
- The Split Demand round is removed entirely. (fixes: P5): It was a never-behind safe option. The final proposal rounds still let Responders retaliate, and a leading Responder who rejects can be overtaken if the other accepts.
- Snake proposer order: P1, P2, P3, P3, P2, P1, P1, P2, P3, P3, P2, P1. (fixes: P6): P1 proposes both first (least information) and last (most information). P3 proposes twice in a row in the middle, and P2's turns are evenly spread, so first-mover and last-mover effects offset.
- The pot lists are kept as game lists, not player attributes. (fixes: P7): This keeps the attribute count at 9.

## Kept from the original

- A Proposer splits a pie and Responders accept or reject, with rejection destroying value.
- The Proposer keeps the pie minus the offer, and a Responder gets the offer only by accepting.
- The tension between the fairness threat (rejection) and greed (a low offer).
- The hidden pie size from the previous variation, and inferring it from the offer and the remaining list.
- Simultaneous non-binding talk before each offer.

## The variation's rules

SETUP: Three players, P1, P2 and P3, each start with a score of 0. Each player has a pot list (a game list, not a player attribute) holding the four values 70, 90, 110 and 130. Everyone knows the contents of every list.

ROUNDS: There are 12 proposal rounds. The Proposer by round is:
- rounds 1-3: P1, P2, P3
- rounds 4-6: P3, P2, P1
- rounds 7-9: P1, P2, P3
- rounds 10-12: P3, P2, P1
Each player proposes exactly 4 times. The other two players are that round's Responders; the first Responder is the one with the lower seat number.

EACH ROUND:
1. Draw: one value is drawn at random from the Proposer's remaining pot list and removed from it. This is the pot. Only the Proposer is told it. Because each list loses one value per proposal, every player plays all four values exactly once.
2. Talk: every player writes one short message at the same time, without seeing the others. Then all three messages are shown to everyone. Messages are not binding and may be false.
3. Offer: the Proposer announces two whole numbers: a for the first Responder and b for the second. Each must be 0 or more, and a + b must be at most 130. The offer is shown to everyone; the pot is not.
4. Response: both Responders choose Accept or Reject at the same time, without seeing each other's choice.
5. Scoring:
   - If at least one Responder accepts, the deal passes. The Proposer gains pot - a - b; if a + b exceeds the pot, this is negative and the Proposer loses points. Each Responder who accepted gains their offered amount. A Responder who rejected gains 0, and their share is destroyed (the Proposer still pays it).
   - If both Responders reject, the deal fails and all three gain 0 this round.
6. Reveal: the pot, both responses and all three scores are announced.

END: The game ends after round 12.

Objective: After round 12, the player with the strictly highest total score wins. If two or three players tie for the highest total, the game is a draw.

Expected effect: Pie luck is gone: every player proposes pots totalling 400, so differences come only from bargaining. Responders must judge from the offer and the remaining list whether the hidden pot is large or small. A player's last-remaining value is public, so inference sharpens as the game goes on. Players disagree about who gets the Responder share and who gets squeezed, and only one player can win. In talk, two players may propose a pact (high offers to each other, low to the third). The excluded player tries to break it by bidding more to one partner. A player who simply follows a pact can lose: the partner may take high offers and then give low ones, or simply finish ahead. Late in the game a leading Responder must decide whether to reject. Rejecting alone does not stop the deal if the other Responder accepts, so the leader can be passed. No simple policy is safe. Offering 0/0 gets rejected and earns 0 on your own pots. Over-offering loses points. Always-accept is exploited with offers of 0 or 1. Always-reject earns only from your own proposals and falls behind. Symmetric fair play ends in a 400/400/400 draw, not a lottery.

## Complexity (the designer's count, against the limits)

- steps_per_round: 12 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 9 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 12 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
