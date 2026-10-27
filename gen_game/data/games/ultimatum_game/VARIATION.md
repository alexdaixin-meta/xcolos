# Variation: Hidden-Pot Ultimatum (Three Players)

Three players take turns as Proposer, twice each. The Proposer secretly knows whether the pot is 12 or 24 and offers each of the two Responders 0–6 points. Both Responders must accept or the deal fails. A failed deal costs the Proposer a third of their intended keep and costs each rejecter 1 point. The highest total after 6 rounds wins.

Players: 3 to 3, best with 3

## Review of the original

The Ultimatum Game: a Proposer offers a Responder part of 100 units. If the Responder accepts, the split stands; if the Responder rejects, both get 0. It is one-shot, with complete information about the pot.

- **non_degenerate**: bad. In the one-shot original the offer-minimum/accept-anything pair is the subgame-perfect answer. Under 'higher total wins' with two players, only the difference counts, so the Responder rejects anything under 50 and the game collapses to a forced 50/50 draw. The previous 3-player variation still degenerated. Always taking the first option (offer 0, accept) won 60 of 60 games as seat 1 and as seat 2. Always taking the last option lost 60 of 60. Seat 3 won only 7 times against random seats, a structural seat bias.
- **skill_sensitive**: bad. A fixed one-line policy beat random players every time. Rejection was cheap for everyone except the proposer's rivals, and nothing hidden needed reading, so skill had little to work on beyond 'be stingy'.
- **headroom**: weak. With the pot public, the only question is how fairness norms hold up. Once the answer is known (lowball in the original, 50/50 under relative scoring), nothing is left to improve.
- **reasoning_dependent**: bad. Complete information: the Responder knows exactly what the Proposer keeps. There is no hidden state, no type to infer, and in the one-shot form no multi-round plan.
- **verifiable**: good. Payoffs follow by arithmetic from the offer and the accept or reject decision.
- **fits_platform**: good. The game is turn-based, text-only, short and numeric: a sequential choice followed by a response.

## Problems

- Offering the minimum and always accepting is near-dominant. In the previous variation the 'first option' policy won 100% of games against random seats.
- Rejection is not a credible threat: a stingy offer costs the Proposer nothing extra when it fails, and against non-punishing responders it pays the most.
- Rejection must not become free either. If only the Proposer pays for a failed deal, 'always reject' quietly drags rivals down and becomes a thoughtless winning policy.
- The pot is public, so there is nothing to infer. The Responder can compute the Proposer's keep exactly.
- Seat imbalance: a 1-2-3 proposer rotation, with the lower seat always first Responder, left seat 3 winning far less often even against random play.
- With two players and 'higher total wins', only the difference matters, so the game is a forced 50/50 draw. The one-shot form has no repeated-play reasoning at all.
- A random pot size per round would be a lottery: whoever is dealt bigger pots as Proposer gets ahead for no reason.

## Changes

- Three players. The Proposer seat rotates in snake order 1,2,3,3,2,1 over 6 rounds, so each player proposes exactly twice. The two Responders choose at the same moment, so neither is 'first'. (fixes: Seat imbalance: a 1-2-3 proposer rotation, with the lower seat always first Responder, left seat 3 winning far less often even against random play.): Three players break the zero-sum difference trap. The snake order gives every seat one early and one late proposal. Simultaneous responses remove the lower-seat ordering.
- The deal passes only if BOTH Responders accept. If it fails, the Proposer loses one third (rounded down) of the amount they tried to keep. (fixes: Offering the minimum and always accepting is near-dominant. In the previous variation the 'first option' policy won 100% of games against random seats.): A stingy offer that gets vetoed now costs the Proposer heavily. A generous offer risks little, but hands rivals points. Both ends of the offer range are risky. Against purely random responders (25% pass), the penalty makes the expected value of proposing about zero for any keep, so lowballing no longer beats random play.
- Every Responder who rejects pays 1 point. (fixes: Rejection must not become free either. If only the Proposer pays for a failed deal, 'always reject' quietly drags rivals down and becomes a thoughtless winning policy.): A veto must be worth its cost. Always-reject now loses about 4 points over the game and never earns as a Responder, so it falls behind.
- The pot is hidden. Each player proposes once with a pot of 12 and once with a pot of 24, in a secret random order. Only the Proposer knows the current pot. Offers are capped at 0–6 per Responder. Pots, keeps and running totals stay private until the game ends; only offers, votes and pass or fail are public. (fixes: The pot is public, so there is nothing to infer. The Responder can compute the Proposer's keep exactly.): Responders must infer from an offer (and any talk) whether the Proposer is splitting fairly or lowballing a big pot. Proposers with a big pot want to look like they have a small one. Because every player gets the same two pots, the draw changes what players know, not who is ahead.
- Every player gets the same pair of pots (12 and 24); only the order is random. (fixes: A random pot size per round would be a lottery: whoever is dealt bigger pots as Proposer gets ahead for no reason.): The random draw affects only information and timing, not total opportunity, so it is not a lottery.
- Six rounds, the highest final total wins outright, and a tie for highest is a draw. A simultaneous one-message talk phase is held before each offer. (fixes: With two players and 'higher total wins', only the difference matters, so the game is a forced 50/50 draw. The one-shot form has no repeated-play reasoning at all.): Repetition lets players build a reputation and retaliate. Talk lets Proposers claim a pot size (truthfully or not) and lets Responders threaten vetoes. Interests conflict because only one player can win.

## Kept from the original

- A Proposer divides a pot and the Responders can only accept or reject. Rejection destroys the round's value for everyone.
- The core tension between keeping more and offering enough to avoid rejection.
- Simple integer offers and arithmetic payoffs.

## The variation's rules

SETUP: Three players, seats 1, 2 and 3. Everyone starts with 0 points. Totals are private: each player is told only their own total until the game ends. Each player will propose in exactly two rounds. For each player, one of those two rounds has a pot of 12 and the other a pot of 24. The order is secret and random.

PROPOSER ORDER: Round 1: seat 1. Round 2: seat 2. Round 3: seat 3. Round 4: seat 3. Round 5: seat 2. Round 6: seat 1. In each round the other two players are the Responders.

EACH ROUND:
1. Announce the round number and who the Proposer is.
2. Pot. If this is the Proposer's first proposal, the engine flips a fair coin: heads means the pot is 12 this time (and 24 next time), tails means 24 this time (and 12 next time). If it is the Proposer's second proposal, the pot is whichever value was not used the first time.
3. Tell the pot privately to the Proposer only.
4. Talk: all three players each write one short message at the same time, without seeing the others' messages. The Proposer may state, hint at or lie about the pot. Nothing said is binding.
5. Show all three messages to everyone.
6. The Proposer chooses two whole numbers: an offer to each Responder, each from 0 to 6. The two offers may differ. The Proposer's keep is the pot minus both offers (always at least 0).
7. Announce both offers to everyone. The pot and the keep are not announced.
8. The two Responders each choose Accept or Reject at the same time.
9. Announce both votes.
10. If both accepted, the deal passes: each Responder adds their offer to their total, and the Proposer adds their keep.
11. If at least one rejected, the deal fails: nobody receives an offer or a keep. The Proposer instead loses one third of their keep, rounded down (keep 12 loses 4, keep 6 loses 2, keep 2 loses 0).
12. In either case, each Responder who chose Reject loses 1 point.
13. Tell each player privately their own new total.

END: After round 6, reveal every round's pot and keep and every player's total. Totals may be negative.

Objective: The player with the strictly highest final total wins. If two or three players tie for the highest total, the game is a draw.

Expected effect: Lowballing (offers 0/0) now loses heavily whenever either Responder vetoes. With a 24 pot that is 8 points per veto, so first-option play no longer beats random seats. A rough expectation against random players puts it behind them. Maximum generosity (6/6) hands rivals 12 points, and always-reject bleeds about 4 points, so last-option play loses too.

Good play means calibrating offers to the hidden pot and judging whether an offer of, say, 4/4 is a fair 12-pot split or a 24-pot grab. Uneven offers can buy one Responder while testing the other's willingness to veto at a cost of 1. A Proposer can manage their reputation across their two turns: the second pot is known to them but not to the others.

Talk earns its place. Proposers can bluff about the pot. Responders can threaten or promise vetoes. The players disagree because only one can win. A Responder who simply follows the Proposer's 'it's a small pot, accept 4' may be handing a rival a 16-point keep. A Proposer who believes a veto threat may give away more than needed.

The snake order and the identical pot pairs remove seat and draw advantages.

## Complexity (the designer's count, against the limits)

- steps_per_round: 13 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 13 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 6 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
