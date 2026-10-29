# 18 design

- time: 2026-10-28T03:43:56+00:00 (69.4s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 2efdb3d3f8ae446c, reply sha256 684a81e8ac9e1d1e

## Sent

````
Original game: Rutersju
Players in the original: 3 to 12

Original rules:
Use a 36 card French pack. The ♦7 is the highest trump that wins any trick it is in. Deal three cards to each player. Going clockwise players bid 0 to 3 for the exact number of tricks they intend to take. Highest bidder becomes declarer; ties go to the last tied bidder. Declarer leads first trick alone against all others. Players must follow suit if able. Highest card of led suit wins unless ♦7 is played. Play three tricks. If declarer makes exactly the bid, declarer scores that many points. Otherwise each opponent scores one point per trick of difference between bid and tricks taken.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- reasoning_over_luck FAILED: WHAT DECIDES A DEAL. A deal is decided mainly by who is dealt the ♦7 and the top trumps.
- The ♦7 holder can always make bid 1: they play ♦7 once and their lowest cards otherwise. The holder exists in 25% of deals at N=3, 33% at N=4 and 42% at N=5.
- Without ♦7 or other top trumps, any positive bid is a gamble that the opponents can usually defeat, because any one of them can overtrump.

WHERE SKILL APPEARS. Skill appears in two places, and both are small:
- choosing the bid from your hand and from what the others' bids imply;
- guessing when to spend a high card in simultaneous play.

HOW THE POT AMPLIFIES THE DEAL. When no one holds a sure hand, every sensible player bids 0 and the pot carries over. The pot then accumulates N per idle deal. The next player dealt the ♦7 collects it all.

OUTCOME WITH ALL PLAYERS PLAYING WELL. They bid only on sure hands. The game becomes: whoever is dealt ♦7 while the pot is large wins. That is about 2 to 4 sure hands per game, assigned by the shuffle.

ESTIMATE. About 70% or more of the result is decided by the deal. A careful reasoner is not clearly favoured over a lucky moderate player. With all players playing the intended good strategy, the deal alone decides the winner.
- change: Cancel card luck with a duplicate format. Store each shuffled deal and replay it N times, with the hands rotated so every seat plays every hand once (N×k deals, k≥2, still ≤40 rounds). This uses the game-list workaround and does not need a second random draw. Winning then depends on bidding and play from the same cards.
- change: Bound the pot swing. Pay the declarer a fixed 2×bid plus at most a capped pot share (e.g. min(pot, 2×bid)), or discard the pot each deal. The game should then stop rewarding whoever happens to hold ♦7 after idle deals.
- change: Give opponents a stake and a reason for real decisions. For example, when a contract fails, each opponent who won a trick gains 1. Opponents then have to choose between spending trumps and conserving them, rather than all blocking the same way.
- change: Set the stated rounds to 3N, not 9, and confirm the attribute count at N=5 stays at or below 20.
The variation that was reviewed: Rutersju Pot: SETUP. Use a 36-card French pack (6, 7, 8, 9, 10, J, Q, K, A in ♣ ♥ ♠ ♦). Each player starts with 0 points, and the pot starts at 0. The game lasts 3 deals per player (9 deals with 3 players, 12 with 4, 15 with 5). Seats are numbered 1 to N. The 'priority seat' is seat 1 in deal 1 and moves one seat to the left each deal.

CARD STRENGTH. Every card has a unique strength from 1 to 36.
- The ♦7 is strength 36, the highest card.
- The other diamonds are trumps: ♦A=35, ♦K=34, ♦Q=33, ♦J=32, ♦10=31, ♦9=30, ♦8=29, ♦6=28.
- The plain suits (♣, ♥, ♠) are ranked by rank first, then by suit, with ♣ lowest and ♠ highest: ♠A=27, ♥A=26, ♣A=25, ♠K=24, ♥K=23, ♣K=22, and so on down to ♠6=3, ♥6=2, ♣6=1.

EACH DEAL.
1. Shuffle the pack and deal 3 cards face down to each player. Hands are private.
2. Ante: every player loses 1 point, and the pot grows by the number of players.
3. Bid: all players secretly and simultaneously choose a bid of 0, 1, 2 or 3 (the exact number of tricks they would undertake to win). The bids are then revealed.
4. Declarer: if every bid is 0, there is no declarer. Skip steps 5 to 7 and go to step 8; the pot carries over. Otherwise the highest bidder becomes declarer. If several players tie for highest, list the players in seat order starting with the priority seat and going left; the tied player who comes LAST in that list becomes declarer. Announce the declarer and the contract (their bid).
5. Tricks: play 3 tricks. In each trick, every player (declarer included) secretly and simultaneously chooses one card from their hand. All played cards are then revealed, and the card with the highest strength wins the trick. There is no need to follow suit.
6. After each trick, if the declarer played the winning card, add 1 to the declarer's trick count. Played cards are discarded face up and remain public.
7. Settlement:
   - If the declarer's trick count equals the bid exactly, the declarer gains the whole pot plus a bonus of 2 × bid, and the pot becomes 0.
   - Otherwise the declarer loses points equal to |bid − tricks won|, and that amount is added to the pot.
   - Opponents gain or lose nothing at settlement.
8. Announce all scores and the pot. Move the priority seat one place to the left.

END. After the last deal, any points still in the pot are discarded. Winner: After the final deal, the player with the highest point total wins. If two or more players tie for the highest total, the game is a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Rutersju is a three-card trick-taking game. Players bid for the exact number of tricks they will take, the highest bidder plays alone against everyone else, and the ♦7 beats every other card. The reviewed variation, 'Rutersju Pot', uses simultaneous bids and simultaneous card play. Only the declarer can score, by taking a growing pot when they make their contract exactly.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "weak",
      "evidence": "Opponents gain nothing at settlement, so 'always bid 0 unless holding ♦7' is close to optimal. Most deals become idle ante-and-carry-over. Once someone declares, the other players have no stake of their own and all block the same way. Seats are fair through the rotating priority, but much of a player's game is not a choice at all."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "bad",
      "evidence": "About 70% or more of the result follows from who is dealt the ♦7 or top trumps while the pot is large. A careful player and a lucky average player finish close together. The only skill left is the bid on a borderline hand and when to spend a high card."
    },
    {
      "criterion": "headroom",
      "verdict": "weak",
      "evidence": "Good play quickly reduces to 'bid only on sure hands, otherwise 0', which is easy to learn and leaves little to improve. A weak player who copies that rule does nearly as well."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "weak",
      "evidence": "Hands are hidden and bids are public signals, so there is something to infer. But the inference rarely changes the decision, because the opponents have no payoff to plan for and the declarer's best play with ♦7 is mechanical."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Unique card strengths, an exact-bid test and pot arithmetic decide everything. No judge is needed."
    },
    {
      "criterion": "fits_platform",
      "verdict": "good",
      "evidence": "Simultaneous bids and card polls, one shuffle per deal and no board. It fits the step limits, but the round count should be stated as 3 deals per player."
    }
  ],
  "problems": [
    "P1 Deal luck dominates: holding ♦7 (or top trumps) is nearly the only way to score, so the shuffle decides the game when everyone plays well (lottery trap).",
    "P2 The carry-over pot amplifies that luck: idle deals pile up points that the next lucky ♦7 holder collects.",
    "P3 Opponents have no stake. They score nothing, so they have no real decisions and no conflict among themselves, and 'bid 0' costs nothing.",
    "P4 Only the declarer's bid matters, so most players' bids carry no risk, no reward and no information worth reasoning about.",
    "P5 The previously suggested duplicate (replay) fix would leak information: every card is revealed during the tricks, so a replayed deal is perfect information to anyone who played it before.",
    "P6 The round count needs to be stated as 3 deals per player, and the attribute count must stay within limits at 5 players."
  ],
  "changes": [
    {
      "what": "Every player's bid is a contract. Each player who takes exactly the number of tricks they bid scores 3 points, whatever the bid (0, 1, 2 or 3). A miss scores 0.",
      "why": "Weak and strong hands become worth the same in principle: a weak hand aims for an exact 0, a strong hand for its exact count. Hand strength changes what to bid and how to play, not who can score. Middling hands are the hardest to read, so skill matters most there.",
      "fixes": "P1"
    },
    {
      "what": "Remove the ante and the pot entirely.",
      "why": "Idle deals no longer pile up a windfall for whoever next holds ♦7.",
      "fixes": "P2"
    },
    {
      "what": "Keep the declarer as the highest bidder with the original tie rule. A declarer who makes the contract exactly gains 1 bonus point. If the declarer misses, every other player gains 1 point per trick of difference (the original opponent scoring).",
      "why": "Opponents now have a stake. Each must weigh making their own exact bid against breaking the declarer. A declarer can be broken by being forced to win extra tricks as well as by being overtrumped. Different opponents want different things, so they do not all block the same way.",
      "fixes": "P3"
    },
    {
      "what": "Bids remain secret and simultaneous, then are revealed. Because there are exactly 3 tricks, a sum of bids other than 3 guarantees that someone will miss.",
      "why": "Every bid is now a public signal about a hidden hand and a target the others can attack or accommodate. This creates inference and opponent modelling during the trick play.",
      "fixes": "P4"
    },
    {
      "what": "Do not use a duplicate or replay format. Rely on equal-value exact scoring to neutralise the deal instead.",
      "why": "Replaying a deal whose cards were all revealed would turn it into a perfect-information puzzle.",
      "fixes": "P5"
    },
    {
      "what": "State the length as 3 deals per player (9, 12 or 15 deals) for 3 to 5 players. Keep only these tracked numbers: score, bid and tricks per player, plus priority seat, declarer and trick number.",
      "why": "This keeps the game within 40 rounds and within 20 attributes at 5 players.",
      "fixes": "P6"
    }
  ],
  "keeps": [
    "The 36-card French pack with ♦7 as the unbeatable top card and diamonds as trumps",
    "Three-card hands, three tricks per deal",
    "Bidding 0 to 3 for an exact number of tricks",
    "The highest bidder becomes the declarer, ties going to the last tied bidder",
    "Opponents scoring one point per trick of difference when the declarer misses",
    "Simultaneous bids and simultaneous card play with the unique strength ranking"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core (an exact bid on three hidden cards, with the declarer against the field) supports real inference once every bid is a contract worth the same and the opponents have a stake."
  },
  "variation": {
    "name": "Rutersju Exact",
    "summary": "Three-card exact-bidding trick game with simultaneous play. Every player who takes exactly their bid scores 3, so a weak hand is as playable as a strong one. The highest bidder is the declarer: making the contract earns a small bonus, and missing it pays every opponent 1 point per trick of difference.",
    "players": {
      "min": 3,
      "max": 5,
      "suggested": 4
    },
    "rules": "SETUP. Use a 36-card French pack (6, 7, 8, 9, 10, J, Q, K, A in ♣ ♥ ♠ ♦). Each player starts with 0 points. Seats are numbered 1 to N. The game lasts 3 deals per player: 9 deals with 3 players, 12 with 4, 15 with 5. The 'priority seat' is seat 1 in deal 1 and moves one seat to the left after each deal.\n\nCARD STRENGTH. Every card has a unique strength from 1 to 36.\n- ♦7 = 36, the highest card.\n- The other diamonds are trumps: ♦A=35, ♦K=34, ♦Q=33, ♦J=32, ♦10=31, ♦9=30, ♦8=29, ♦6=28.\n- The plain suits are ranked by rank first, then by suit, with ♣ low, ♥ middle and ♠ high: ♠A=27, ♥A=26, ♣A=25, ♠K=24, ♥K=23, ♣K=22, ♠Q=21, ♥Q=20, ♣Q=19, ♠J=18, ♥J=17, ♣J=16, ♠10=15, ♥10=14, ♣10=13, ♠9=12, ♥9=11, ♣9=10, ♠8=9, ♥8=8, ♣8=7, ♠7=6, ♥7=5, ♣7=4, ♠6=3, ♥6=2, ♣6=1.\n\nEACH DEAL.\n1. Shuffle the full pack and deal 3 cards face down to each player. Hands are private. Undealt cards stay hidden.\n2. Bid: all players secretly and simultaneously choose a bid of 0, 1, 2 or 3. This is the exact number of tricks they aim to win this deal. All bids are then revealed.\n3. Declarer: if every bid is 0, there is no declarer this deal. Otherwise the highest bidder is the declarer. If several players tie for the highest bid, list the players in seat order starting with the priority seat and going left; the tied player who comes LAST in that list is the declarer. Announce the declarer, if any.\n4. Tricks: play 3 tricks. In each trick, every player secretly and simultaneously chooses one card from their hand. All chosen cards are revealed together, and the card with the highest strength wins the trick. There is no need to follow suit. Add 1 to the trick count of the player who played the winning card. Played cards are discarded face up and stay public.\n5. Settlement, applied to every player:\n   a. Every player whose trick count equals their bid exactly gains 3 points. A player who misses gains 0.\n   b. If there is a declarer and the declarer's trick count equals their bid exactly, the declarer gains 1 more point.\n   c. If there is a declarer and the declarer's trick count does not equal their bid, every other player gains points equal to |declarer's bid − declarer's trick count|.\n6. Announce all bids, trick counts and scores. Move the priority seat one place to the left.\n\nThere is no discussion phase. Players communicate only through their public bids and the cards they play.\n\nEND. After the last deal, the player with the highest point total wins. If two or more players tie for the highest total, the game is a draw.",
    "objective": "After 3N deals, the single player with the highest total points wins. A tie for the highest total is a draw.",
    "expected_effect": "Every hand now has a winnable exact contract, so the shuffle sets the puzzle rather than the winner. Bidding becomes reading your own hand against unknown hands. Simultaneous play becomes managing your trick count against everyone's revealed bids: dumping low cards when bids overshoot, or forcing an unwanted trick onto a rival. Opponents disagree about whether to break the declarer, since doing so can cost them their own exact 3. The declarer bonus is small, so holding ♦7 helps only modestly. Simple policies lose to a careful player. 'Always bid 0' misses whenever it holds ♦7 or is forced to take a trick. 'Always bid high' misses often and pays every opponent. 'Always play the lowest card' cannot hit a positive bid. Talk was left out because the bids already serve as simultaneous public signals, and a talk step would exceed the 4 choice steps per round."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 14,
    "choice_steps_per_round": 4,
    "attributes": 18,
    "hidden_elements": 1,
    "random_draws_per_round": 1,
    "rounds": 15
  }
}
```
````
