# 12 design

- time: 2026-10-27T18:24:42+00:00 (89.5s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 889000ef761870f0, reply sha256 3c6709b53f021b87

## Sent

````
Original game: Dollar auction
Players in the original: 2 to 2

Original rules:
An auctioneer offers a $1 bill. Players alternately raise the current high bid by at least a fixed minimum increment, e.g. $0.05, starting at $0.05. The current high bidder and the amount are public. On your turn you may drop out or raise above the current high bid. If you drop out you are out of the auction. When no player is willing to raise, the auction ends. The final high bidder receives $1 and pays their bid for a net payoff of 1 - bid. The second-highest bidder pays their last bid and receives nothing, payoff -bid. All other bidders who dropped earlier pay their last bids as well.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- balanced FAILED: Net result of one round for a bidder (prize value minus bid if they win, minus bid if they lose). Low-value round (value 5): bid 1 gives +4 / -1, bid 3 gives +2 / -3, bid 6 gives -1 / -6. High-value round (value 15): bid 1 gives +14 / -1, bid 3 gives +12 / -3, bid 6 gives +9 / -6. In escalation, a RAISE costs 4 more. In every round exactly one type is high-value. In 3 of the 12 rounds that type is undealt, so nobody holds it.

Thoughtless policies under the WINNER RULE (reach 20 or more):
(a) Always 0: total stays 0 and never reaches 20. Against sensible play it loses. It does not survive.
(b) Always 6, always RAISE (the spoiler). Its own ceiling is 3 x (15-6) + 9 x (5-6) = 27 - 9 = 18, which is below 20, so it can never win. But no other player can ever win a prize against it. A bid below 6 loses to it outright. A bid of 6 forces escalation. There the spoiler always raises, so the opponent either drops and the spoiler takes the prize, or raises too and nobody wins. Every other total therefore only falls and stays at or below 0. Nobody reaches 20, so the game is a draw with no winner.
- Against sensible play: draw.
- Against random play: draw (a random player who ties at 6 either drops or double-raises, and gets no prize either way).
- Against another spoiler: draw.
Always-6/RAISE NEVER LOSES. This fails by rule, even though no single option is strictly better in one round.

The threshold rule also makes the 'escalation' largely cooperative. If all three truthfully claim their types and each bids 1 in their own high rounds, each scores 3 x 14 = 42 and all draw. Denying a rival costs 6 to remove their 15. So any player who prefers a sole win to a draw is pushed toward spoiling, which collapses the game to the no-winner draw.

Seat and schedule edge: North collects its high rounds earliest, while West sees more of the history before its high rounds. This is a minor asymmetry, but it is untested.
- reasoning_over_luck FAILED: Chance is small. The deal is symmetric (3 high rounds each), and the only luck is schedule timing and which type is undealt. Perhaps 10% of the outcome is chance.

There is something to infer: rivals' types from their claims and bids, and the undealt type from the rounds where nobody bids high.

However, the result does not reward reasoning:
- If everyone plays the cooperative good strategy, all three reach 42 and draw.
- If anyone plays the thoughtless always-6/RAISE policy, everyone draws with no winner, however well the others reason.
- Because denial is cheap (6 to cancel a rival's 15), a strong player who tries for a sole win invites spoiling and ends in a draw.

A strong reasoner is therefore not clearly favoured over a thoughtless one. The modal outcome is a draw regardless of skill.
- change: Replace the 20-point threshold with a relative winner rule: the highest total after round 12 wins and equal totals draw. Then re-verify that always-6/RAISE loses to sensible play (its ceiling of 18 must be beaten by players who bid 0 against it and contest its high rounds).
- change: Break the escalation blocker so that always RAISE cannot cancel every prize. For example: if more than one tied player raises, the prize goes to the raiser with the lowest current total (ties broken by lowest seat number). Alternatively, every raiser beyond the first refunds nothing and the prize still goes to someone. A constant spoiler must then concede prizes.
- change: Add a worked check to the design showing, under the new winner rule, who wins or draws for always-0, always-1, always-6/RAISE and always-6/DROP against sensible and random opponents. Each must lose most games.
- change: State explicitly that totals may go negative.
The variation that was reviewed: Escalation Ledger: SETUP
There are four schedule types:
- North: high-value rounds 1, 5 and 9.
- East: high-value rounds 2, 6 and 10.
- South: high-value rounds 3, 7 and 11.
- West: high-value rounds 4, 8 and 12.
At the start, three different types are dealt at random, one to each player, and each player is told only their own. The fourth type goes to nobody, and nobody is told which one it is. Every player's total starts at 0.
In each round a prize is offered. Its value to a player is 15 if the round is one of that player's high-value rounds, and 5 otherwise.

EACH ROUND (12 rounds)
1. The round number is announced.
2. Talk: every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Nothing said is binding.
3. Bid: every player secretly and simultaneously chooses one bid from 0, 1, 3 or 6.
4. All three bids are revealed.
5. Every player pays their bid: it is subtracted from their total, win or lose.
6. Resolve the bids:
   - If one player's bid is strictly higher than both others and is above 0, that player wins the prize.
   - If all bids are 0, nobody wins.
   - If two or more players tie for the highest bid (above 0), they go to escalation.
7. Escalation (only the players tied for the highest bid take part): each tied player secretly and simultaneously chooses RAISE or DROP.
   - Each player who chooses RAISE pays 4 more points.
   - If exactly one tied player raises, that player wins the prize.
   - If none or more than one raise, nobody wins the prize.
8. The prize winner, if any, adds their own value of the prize (15 or 5) to their total.
9. All totals are announced.

END
After round 12 the game ends. Winner: After round 12, every player whose total is 20 or more wins. If exactly one player reaches 20, that player wins. If two or three reach 20, those players draw. If nobody reaches 20, the game is a draw with no winner.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "The Dollar Auction: two players take turns raising bids for a $1 bill. Both the winner and the runner-up pay their bids, so players get trapped escalating past the prize's value to avoid a sure loss. A previous adaptation, 'Escalation Ledger', made it a 3-player, 12-round sealed-bid all-pay auction with hidden value schedules and a 20-point target. It failed because an always-bid-6/always-RAISE spoiler could cancel every prize and force a no-winner draw.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "bad",
      "evidence": "In the original, a player who never bids scores 0. Under 'higher total wins' with two players, never bidding loses only when the opponent wins cheaply at 0.05, and any escalation war hands the non-escalator the win, so the game reduces to a war of attrition with a known answer: drop out at once, or bid once and stop. In the previous variation, always-6/RAISE can never lose: nobody can win a prize against it, so every game is a draw or a no-winner draw."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "The original has one decision, how far to escalate, and no information to use. In the previous variation the modal result was a draw whatever the skill: cooperative play draws at 42 each, and spoiling draws with no winner."
    },
    {
      "criterion": "headroom",
      "verdict": "weak",
      "evidence": "The original is a single war of attrition with one known lesson: don't escalate. It cannot be improved on over time. The previous variation had something to infer, but the threshold rule capped what a good player could gain."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "bad",
      "evidence": "The original has perfect information: the bids are public and the value of $1 is common knowledge. Nothing is hidden and there is no rival type to read. The previous variation added hidden schedules and an undealt type, but the winner rule made that reasoning irrelevant."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Payoffs are value minus bid for the winner and minus bid for the others: pure arithmetic."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The original is turn-based and text-only, but the open-ended alternating raises have no fixed length and need an unbounded sequential loop. Its currency is continuous. Two players under 'higher total wins' fall into the difference trap."
    }
  ],
  "problems": [
    "P1: The original is a single perfect-information war of attrition with nothing to infer.",
    "P2: The original's alternating, unbounded raises do not fit a flat step list with a fixed round count.",
    "P3: With two players and 'higher total wins', the original collapses into a difference game where not bidding is safe.",
    "P4: In the previous variation, an escalation in which two or more raisers cancel the prize lets an always-6/RAISE spoiler block every prize, so it never loses.",
    "P5: In the previous variation, the 20-point target made truthful cooperation (42 each) an all-draw, and spoiling a no-winner draw, so the modal outcome was a draw regardless of skill.",
    "P6: In the previous variation, totals going negative was implied but not stated.",
    "P7: Minor seat/schedule timing asymmetry (North collects earliest, West sees the most history)."
  ],
  "changes": [
    {
      "what": "Keep three players, 12 rounds and the sealed simultaneous bid menu 0/1/3/6, with an all-pay rule: every bid is paid, win or lose.",
      "why": "This gives a fixed-length structure that a flat step list can build, while keeping the dollar auction's defining all-pay sting.",
      "fixes": "P2"
    },
    {
      "what": "Keep the hidden value schedules: four types, three dealt and one undealt. Each type has 3 high-value rounds out of 12. Raise the prize values to 16 (high) and 6 (low).",
      "why": "Players must infer rivals' high rounds and the undealt type from talk and bids. The even values allow the half-value split below, and every dealt type is worth the same in total, so the deal is not a lottery.",
      "fixes": "P1"
    },
    {
      "what": "Escalation now always resolves. Each raiser pays 4. If exactly one tied player raises, that player takes the full prize. If two or more raise, each raiser receives half of their own value (8 or 3). If nobody raises, nobody gets the prize.",
      "why": "A permanent raiser can no longer cancel prizes. Contesting it costs it more than it costs the contester: in a round worth 16 to the contester, the contester nets 8-10 = -2 and the spoiler nets 3-10 = -7.",
      "fixes": "P4"
    },
    {
      "what": "Replace the 20-point target with 'highest total after round 12 wins; players tied for the highest total draw'.",
      "why": "With three players, one rival's gain is not the other's loss. Truthful turn-taking is no longer a stable draw, because outbidding a rival in their high round wins 6 for a cost of 3 and denies them about 15. Players must now judge when to contest and when to concede. This is a competitive auction, not a trust game, so the ending is meant to stay contested to the last round.",
      "fixes": "P5"
    },
    {
      "what": "Add a worked check of the simple policies under the new rule (see expected_effect).",
      "why": "This verifies that every thoughtless policy can lose.",
      "fixes": "P3"
    },
    {
      "what": "State explicitly that totals may go below 0.",
      "why": "Makes the rules and arithmetic unambiguous.",
      "fixes": "P6"
    },
    {
      "what": "Assign seats at random, independent of the schedule types. Each player knows only their own type, so nobody knows who collects earliest.",
      "why": "Removes any fixed seat edge. Timing becomes part of the hidden information.",
      "fixes": "P7"
    }
  ],
  "keeps": [
    "All-pay bidding: losers pay their bids too.",
    "An escalation stage where tied bidders must pay more to stay in, the dollar auction's sunk-cost trap.",
    "A prize that can be worth less than the total cost of fighting for it.",
    "The tension between conceding a cheap loss and escalating into a costly fight."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "With escalation that always resolves and a relative winner rule among three players, the hidden-schedule all-pay auction rewards inferring rivals' values and choosing when to fight, within the platform limits."
  },
  "variation": {
    "name": "Escalation Ledger II",
    "summary": "A 12-round, 3-player sealed all-pay auction with a short escalation stage. Each player secretly holds a schedule of three rounds in which the prize is worth 16 to them instead of 6. Players talk, bid, sometimes escalate, and the highest final total wins.",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "rules": "SETUP\nThere are four schedule types:\n- North: high-value rounds 1, 5 and 9.\n- East: high-value rounds 2, 6 and 10.\n- South: high-value rounds 3, 7 and 11.\n- West: high-value rounds 4, 8 and 12.\nSeat order is random. Three different types are dealt at random, one to each player, and each player is told only their own type. The fourth type goes to nobody, and nobody is told which it is.\nEvery player's total starts at 0. Totals may go below 0.\nEach round a prize is offered. Its value to a player is 16 if the round is one of that player's high-value rounds, and 6 otherwise.\n\nEACH ROUND (rounds 1 to 12)\n1. The round number is announced.\n2. Talk: every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Nothing said is binding, and players may lie.\n3. Bid: every player secretly and simultaneously chooses a bid of 0, 1, 3 or 6.\n4. All three bids are revealed.\n5. Every player subtracts their bid from their total, whether they win or lose.\n6. Resolve:\n   - If one bid is strictly higher than both others, that player wins the full prize.\n   - If all bids are 0, nobody wins.\n   - If two or three players tie for the highest bid (above 0), those players go to escalation.\n7. Escalation (only the tied players take part): each tied player secretly and simultaneously chooses RAISE or DROP. Each player who chooses RAISE subtracts 4 more from their total.\n   - If exactly one tied player raises, that player wins the full prize.\n   - If two or more raise, each raising player receives half of their own value of the prize (8 if it is their high-value round, otherwise 3).\n   - If nobody raises, nobody receives the prize.\n8. Each player who receives a prize, or a half-prize, adds that amount to their total. The full prize is 16 or 6, the receiver's own value.\n9. All bids, escalation choices and totals are announced.\n\nEND\nAfter round 12 the game ends.",
    "objective": "After round 12, the player with the highest total wins. If two or three players share the highest total, they draw. Totals may be negative.",
    "expected_effect": "Players must infer rivals' high rounds and the undealt type from claims and bidding patterns, decide which rounds to contest, and avoid escalation wars that cost more than half a prize.\n\nTalk passes both tests. Players disagree because only one can win: a player who agrees to a proposed 'everyone bids 1 in their own round' turn-taking plan can be undercut by a rival bidding 3 (+3 to them, -15 to the follower). Talk lets players claim types, bluff about their schedule, propose turn-taking, threaten escalation, and coordinate against the leader.\n\nWorked check (S = sensible: bids 0 in rounds that are not its own high rounds and contests its own high rounds at the level needed, raising at 6):\n(a) Always 0 scores exactly 0. Sensible players net positive from uncontested rounds (16-1 = +15), so always-0 loses. Against two random players it can sometimes win, but it can lose.\n(b) Always 6/RAISE against two S players. Each S bids 6 and raises in its own 3 high rounds: S nets 8-10 = -2 each time (-6 total); the spoiler nets 3-10 = -7 each time. Spoiler total: 3x(16-6) + 3x(6-6) + 6x(-7) = 30 + 0 - 42 = -12. The two S players finish at -6 each and share the win, so the spoiler loses. If the others never contest, the spoiler wins with 30, so it is beaten only by players who recognise it and fight back. Two spoilers, or three, tie.\n(c) Always 6/DROP: any rival who ties at 6 and raises takes the full prize, while it has paid 6. It loses to S.\n(d) Always 1 or always 3: outbid at the next level in the rounds that matter, it pays every round. It loses to S.\n\nWhen everyone plays well, nobody can safely bid low in their high round, because it invites an undercut. The outcome then depends on reading who values which round and on picking which fights to take. Hidden types are worth the same in total (3 high rounds each), so the deal changes what to do, not who is ahead."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 12,
    "choice_steps_per_round": 3,
    "attributes": 15,
    "hidden_elements": 1,
    "random_draws_per_round": 0,
    "rounds": 12
  }
}
```
````
