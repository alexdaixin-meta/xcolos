# Variation: Escalation Ledger III

Three players bid secretly for a prize in each of 12 rounds. Each player privately knows which 3 rounds the prize is worth 12 to them; in all other rounds it is worth 6. Losing bidders pay half their bid, and ties go to a RAISE/DROP showdown in which two raisers both lose.

Players: 3 to 3, best with 3

## Review of the original

The dollar auction: two players take turns raising a public bid for a $1 prize. Both the winner and the runner-up pay their bids, so bidding tends to escalate past the prize's value. The previous adaptation, Escalation Ledger II, made it a 3-player, 12-round sealed-bid all-pay auction with hidden high-value schedules and a RAISE/DROP tie-break.

- **non_degenerate**: bad. In the original, the first mover can open high and the whole game turns on one escalation trap. In Ledger II, a value-16 player's RAISE strictly dominated DROP (+12 or +4, against 0), and a bid of 6 (the top bid) was near-forced in your own rounds. 'Always bid 6 and RAISE' beat both random and non-punishing play (about +30 against about 0). Only the 3 rounds of the undealt type were genuinely contested.
- **skill_sensitive**: weak. No dice are rolled, but a mechanical policy won. Skill showed only in the 3 empty rounds and in the decision to spite, which costs the spiter as much as or more than its target and helps the bystander.
- **headroom**: weak. Most of Ledger II's rounds are solved: H bids 6 and raises, and L bids 0. The original two-player auction is solved by 'never bid' or 'open at 0.95'.
- **reasoning_dependent**: weak. The hidden schedule existed, but it hardly mattered: once H's action was forced, there was little to infer. The original has nothing hidden at all.
- **verifiable**: good. Every payment and prize is arithmetic on bids and choices.
- **fits_platform**: good. Ledger II is turn-based, text-only, uses simultaneous polls and runs 12 rounds, all within the limits. The original's open-ended alternating raises would need an unbounded loop.

## Problems

- P1: RAISE in escalation strictly dominated DROP for the high-value player, because two raisers each still received half the prize.
- P2: The top bid (6) could not be outbid, so H bidding 6 nearly guaranteed a profit in its own rounds.
- P3: 'Always bid the maximum and RAISE' beat random and non-punishing play. Beating it required opponents to sacrifice repeatedly.
- P4: Punishing a greedy bidder cost the punisher as much as or more than the target, so punishment was not credible and mainly helped the bystander.
- P5: Only the 3 undealt-type rounds were genuinely contested, so the hidden type rarely changed what to do.

## Changes

- If two or more tied players RAISE, nobody receives the prize. Each raiser pays the raise cost of 3 and half of their bid. (fixes: P1): Raising against another raiser is now worse than dropping, for H and L alike. Escalation becomes a real chicken game for every value.
- The bid menu is 0, 2, 4, 6 or 8, and the maximum (8) is above an ordinary player's value (6) but below the high value (12). (fixes: P2): No bid is unbeatable. Any player can block H with 8 at a modest cost (6-8 = -2), and H can outbid a lower bid. No bid guarantees anyone a profit.
- The high value drops from 16 to 12, and the ordinary value stays at 6. (fixes: P3): Bidding the maximum in a round where you are not high-value now loses 2 even when uncontested. The maniac bleeds without anyone needing to punish it.
- Players who bid and do not receive the prize pay only half their bid. The winner pays in full. (fixes: P4): Contesting or blocking becomes cheaper than the damage it does. An L who blocks with 8 loses 2 while H loses its gain plus half its bid, so a threat to block is credible.
- Every round is contestable. Ls can profit by winning cheap rounds (bid 2 or 4 against 6), and H must guess how hard to bid without knowing whether its rivals will challenge, and in a round it does not own whether anyone is high-value at all. (fixes: P5): Reading opponents' schedules from their bids and talk now changes the best bid in every round.

## Kept from the original

- All-pay bidding: losers still pay part of their bid, so overbidding is costly.
- Escalation past the point of profit (bids up to 8 for a prize worth 6), the dollar-auction trap.
- The RAISE/DROP showdown between tied top bidders.
- Hidden high-value schedules with one undealt type, 3 players, 12 rounds and simultaneous talk.

## The variation's rules

SETUP
There are four schedule types:
- North: high-value rounds 1, 5 and 9.
- East: high-value rounds 2, 6 and 10.
- South: high-value rounds 3, 7 and 11.
- West: high-value rounds 4, 8 and 12.
Three different types are dealt at random, one to each player, and each player is told only their own type. The fourth type goes to nobody, and nobody is told which it is. In that type's rounds, the prize is worth 6 to everyone.
Every total starts at 0. Totals may go below 0.
In each round the prize is worth 12 to a player if it is one of that player's high-value rounds, and 6 otherwise.

EACH ROUND (rounds 1 to 12)
1. Announce the round number.
2. Talk: every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Nothing is binding, and players may lie.
3. Bid: every player secretly and simultaneously chooses 0, 2, 4, 6 or 8.
4. Reveal all bids.
5. Resolve:
   (a) All bids 0: nobody pays and nobody wins.
   (b) One bid strictly highest: that player wins. The winner pays the full bid and receives their own value of the prize (12 or 6). Every other player pays half of their own bid.
   (c) Two or three players tie for the highest bid (above 0): go to step 6. Players not in the tie pay half of their own bid.
6. Escalation, tied players only: each tied player secretly and simultaneously chooses RAISE or DROP. Every player who chooses RAISE pays 3.
   - Exactly one raiser: that player wins. The winner pays the full bid (plus the 3) and receives their own value of the prize. The other tied players pay half their bid.
   - Two or more raisers, or no raisers: nobody receives the prize. Every tied player pays half their bid; raisers have also paid 3.
7. Update all totals, then announce every bid, every escalation choice and every total.

END
After round 12 the game ends.

Objective: After round 12, the player with the highest total wins. If two or three players share the highest total, they draw.

Expected effect: No action is dominant.
- H in a tie: raising earns +5 to +8 more than dropping if the other drops, and 3 less if the other raises.
- L in a tie: the same chicken applies at low bids. At a bid of 8, raising is purely spite.
- No bid guarantees H a profit, because anyone can block with 8 for a cost of 2.

Simple policies all lose to sensible play:
- Always 8 and RAISE: it scores 3x4 - 9x2 = -6 against opponents who simply bid 0 when it is present, while they score 0.
- Always 6: it is outbid by H bidding 8 in H's rounds (H +4, maniac -3) and ends near 0, against sensible players near +12.
- Always 0: it ends at 0, below anyone who takes a cheap round (+10 in an own round won with a bid of 2).
- Always 2 or 4: it is overbid in the opponents' high rounds and pays half each time.

The lottery trap is avoided: every player gets exactly 3 high-value rounds, so types matter for when to fight, not for who ends ahead.

Play centres on inference:
- Whose round is this, and is it the undealt type's?
- Will my rival contest, block or yield?
- How high must I bid?

Talk passes both tests. Everyone wants the prize, so players disagree each round. A player claims 'this is my round, stay out' (true or a bluff), threatens to block, or proposes taking turns. A player who just follows lets a rival bank +10 rounds and falls behind, and a player who believes a bluff yields a round they could have won for 2 or 4.

This is a competitive auction with highest-total-wins, not a cooperation game, so the endgame-unraveling concern does not apply. Blocking the leader late in the game is a legitimate, costed tactic.

## Complexity (the designer's count, against the limits)

- steps_per_round: 13 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 17 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 12 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
