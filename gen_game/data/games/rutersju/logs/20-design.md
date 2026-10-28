# 20 design

- time: 2026-10-28T03:46:22+00:00 (80.0s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 567498d464de53d0, reply sha256 1e0f7eb64d9eb93f

## Sent

````
Original game: Rutersju
Players in the original: 3 to 12

Original rules:
Use a 36 card French pack. The ♦7 is the highest trump that wins any trick it is in. Deal three cards to each player. Going clockwise players bid 0 to 3 for the exact number of tricks they intend to take. Highest bidder becomes declarer; ties go to the last tied bidder. Declarer leads first trick alone against all others. Players must follow suit if able. Highest card of led suit wins unless ♦7 is played. Play three tricks. If declarer makes exactly the bid, declarer scores that many points. Otherwise each opponent scores one point per trick of difference between bid and tricks taken.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- balanced FAILED: SCORING TABLE for one deal, from settlement steps a-c. Exact hit at any bid: +3. Declarer who hits: +1 more, so +4 in total. Declarer who misses by d: 0 for the declarer, and +d to EVERY other player. A bid of 0 is never the declarer (if all bid 0 there is no declarer), so it never pays this penalty, and it collects d from every missed declarer. A bid of 3 pays 3, the same as a bid of 0. It is almost always the declarer bid, it needs the top three strengths in play, and a miss feeds the whole table. Bidding high is pure liability: +1 at best and -d against N-1 rivals at worst.

HOW EASY ZERO IS. All 3N cards are played. A player's highest card wins a trick for sure only if it is the highest card dealt. P(holding the top dealt card) = 1/N: 33% at 3p, 25% at 4p, 20% at 5p. Otherwise a 0-bidder can usually dump its best card into a trick where a bidder fires high. At most 3 players can win tricks, so 2 or more players finish on 0 tricks at 5p, and 1 or more at 4p. Rough P(0 tricks | bid 0 with sensible dumping): about 45% at 3p, 60% at 4p, 65-70% at 5p. Bidding exactly 1 or 2 means hitting an exact count in simultaneous blind play. That is markedly harder (about 30-45%), and if it is the top bid it also carries the declarer penalty.

THOUGHTLESS POLICY 'always bid 0, play lowest card first' (4p):
- Against random play (bids uniform 0-3): the top bid is usually 2 or 3, and declarers miss often (a bid of 3 rarely makes). The policy collects about 1.5 per deal in penalties plus about 0.6×3 = 1.8 from hits, so about 3.3 per deal. A random bidder hits about 25% of the time, about 0.8 per deal plus some penalties. The policy wins almost every game.
- Against sensible play: sensible players also converge to bid 0, because the table shows bids above 0 are only worth it with ♦7 plus ♦A-class holdings. The policy therefore ties or edges sensible play deal after deal. Only at 3p, with its higher 1/3 'forced trick' rate, is it noticeably weaker.

The policy is not strictly dominant, since ♦7+♦A should bid 2. But it never pays the declarer penalty and is the near-best action at 4-5 players, so the bidding decision collapses.

SEATS: the priority seat rotates evenly (each seat holds it 3 times), and the tie-break only matters for who carries the declarer liability. There is no seat edge.

OVERALL: the game fails on degenerate bid-0 dominance at 4-5 players.
- reasoning_over_luck FAILED: GOOD-PLAY OUTCOME: when all players follow the intended good strategy, most players bid 0 most deals, because the scoring makes bidding above 0 a liability. Each deal then turns on whether a player was dealt the top card(s), which cannot be dumped:
- P(holding the top dealt card) = 1/N, and that holder always misses a 0 bid.
- The 3 tricks fall on whoever holds the high cards, so who scores +3 is set mostly by the deal.

WHAT SKILL REMAINS: deciding WHEN to dump your second-best card. That is a simultaneous guessing game, in effect a mixed-strategy coin flip against other dumpers.

CHANCE ESTIMATE: I estimate 60-70% of the per-deal swing is the deal itself. Over 12-15 deals, the winner among competent players is decided largely by who drew fewer unavoidable top cards.

INFERENCE: the information exists (bids reveal strength, discards are public), but with nearly everyone bidding 0 there is little to infer and little to act on. A reasoner is not clearly favoured over a 'bid 0, dump low' bot.
- change: Make the bid size matter: an exact hit should score 1 + 2×bid (0→1, 1→3, 2→5, 3→7) instead of a flat 3, so that 0 is the cheapest success, not an equal one.
- change: Make the declarer's miss a loss for the declarer rather than a gift to every opponent: a declarer who misses by d loses 2×d points (the optional +1 bonus for a made bid can stay). Only if the miss must reward others, split d to the single player with the most tricks.
- change: Add a penalty that stops universal zero bidding: if every bid is 0, every player who wins at least 1 trick loses 2 points per trick, and the players with 0 tricks gain only 1. Alternatively, require that the sum of revealed bids ≠ 3; if the sum equals 3, the player in the priority seat must raise or lower their bid by 1 (one sequential choice step).
- change: Re-check with a numeric table that 'always bid 0' no longer wins or draws most games against random and sensible play at 3, 4 and 5 players.
- change: Store each card's strength as a numeric attribute in the card list and resolve each trick with a calc for the max, rather than a lookup the engine lacks; recount the steps (expected about 16, ≤20).
The variation that was reviewed: Rutersju Exact: SETUP. Use a 36-card French pack (6, 7, 8, 9, 10, J, Q, K, A in ♣ ♥ ♠ ♦). Each player starts with 0 points. Seats are numbered 1 to N. The game lasts 3 deals per player: 9 deals with 3 players, 12 with 4, 15 with 5. The 'priority seat' is seat 1 in deal 1 and moves one seat to the left after each deal.

CARD STRENGTH. Every card has a unique strength from 1 to 36.
- ♦7 = 36, the highest card.
- The other diamonds are trumps: ♦A=35, ♦K=34, ♦Q=33, ♦J=32, ♦10=31, ♦9=30, ♦8=29, ♦6=28.
- The plain suits are ranked by rank first, then by suit, with ♣ low, ♥ middle and ♠ high: ♠A=27, ♥A=26, ♣A=25, ♠K=24, ♥K=23, ♣K=22, ♠Q=21, ♥Q=20, ♣Q=19, ♠J=18, ♥J=17, ♣J=16, ♠10=15, ♥10=14, ♣10=13, ♠9=12, ♥9=11, ♣9=10, ♠8=9, ♥8=8, ♣8=7, ♠7=6, ♥7=5, ♣7=4, ♠6=3, ♥6=2, ♣6=1.

EACH DEAL.
1. Shuffle the full pack and deal 3 cards face down to each player. Hands are private. Undealt cards stay hidden.
2. Bid: all players secretly and simultaneously choose a bid of 0, 1, 2 or 3. This is the exact number of tricks they aim to win this deal. All bids are then revealed.
3. Declarer: if every bid is 0, there is no declarer this deal. Otherwise the highest bidder is the declarer. If several players tie for the highest bid, list the players in seat order starting with the priority seat and going left; the tied player who comes LAST in that list is the declarer. Announce the declarer, if any.
4. Tricks: play 3 tricks. In each trick, every player secretly and simultaneously chooses one card from their hand. All chosen cards are revealed together, and the card with the highest strength wins the trick. There is no need to follow suit. Add 1 to the trick count of the player who played the winning card. Played cards are discarded face up and stay public.
5. Settlement, applied to every player:
   a. Every player whose trick count equals their bid exactly gains 3 points. A player who misses gains 0.
   b. If there is a declarer and the declarer's trick count equals their bid exactly, the declarer gains 1 more point.
   c. If there is a declarer and the declarer's trick count does not equal their bid, every other player gains points equal to |declarer's bid − declarer's trick count|.
6. Announce all bids, trick counts and scores. Move the priority seat one place to the left.

There is no discussion phase. Players communicate only through their public bids and the cards they play.

END. After the last deal, the player with the highest point total wins. If two or more players tie for the highest total, the game is a draw. Winner: After 3N deals, the single player with the highest total points wins. A tie for the highest total is a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Rutersju is a short Scandinavian trick-taking game for 3 to 12 players. Each player gets three cards, players bid how many of the three tricks they will take, and the highest bidder becomes declarer against the rest. ♦7 is the top trump. A declarer who makes the bid exactly scores it; a declarer who misses pays one point per trick of error to each opponent.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "bad",
      "evidence": "In the reviewed variation a bid of 0 is never the declarer, so it never pays the miss penalty. It still scores the same +3 on a hit as a bid of 3, and it collects d from every declarer who misses. At 4–5 players 'always bid 0, dump high cards early' hits about 60–70% of the time and wins or draws most games against both random and sensible play. Any bid above 0 is a liability: +1 at best, and −d against every rival at worst. The bidding decision collapses."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "With nearly everyone bidding 0, each deal is decided by who was dealt top cards that cannot be dumped (P = 1/N per deal). The only skill left is a simultaneous dumping guess. About 60–70% of the per-deal swing is the deal itself."
    },
    {
      "criterion": "headroom",
      "verdict": "weak",
      "evidence": "A bot that bids 0 and dumps low is close to optimal at 4–5 players. A strong player has little to improve on, because good bidding is not rewarded."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "weak",
      "evidence": "Hands are hidden, and bids plus face-up discards could carry information. But when all bids are 0 the bids reveal nothing, and there is nothing to act on even if a player infers something."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Card strengths are fixed numbers. Trick winners, trick counts and scores all follow by arithmetic."
    },
    {
      "criterion": "fits_platform",
      "verdict": "good",
      "evidence": "Play is text-only with no board. Trick play is simultaneous with numeric strengths, and the step count was within limits (about 14–16)."
    }
  ],
  "problems": [
    "P1: A bid of 0 pays the same as any other exact bid and is never the declarer, so it carries no risk. 'Always bid 0' dominates at 4–5 players.",
    "P2: A declarer's miss is a gift to every other player, so taking on the declarer bid is pure liability and nobody wants it.",
    "P3: Nothing stops everyone bidding 0 together, so the bids carry no information and no player is forced into a contested decision.",
    "P4: Under good play the deal decides each hand, because the holder of the top card simply misses. The skill left is a coin-flip dumping guess, so luck dominates.",
    "P5: Simultaneous blind bids mean no player reasons from others' bids when choosing their own, so there is little inference in the bidding."
  ],
  "changes": [
    {
      "what": "An exact hit now scores 3 + bid (0→3, 1→4, 2→5, 3→6), and EVERY player who misses loses 2 points per trick of error, not only the declarer. Missing no longer feeds the other players.",
      "why": "Bidding 0 while holding a card that will win a trick now costs 2 instead of being free. Higher bids are worth a little more, so a player should bid what the hand will take rather than hiding at 0. The slope is kept mild (3 to 6) so that a weak hand bid correctly still scores most of what a strong hand scores.",
      "fixes": "P1"
    },
    {
      "what": "The declarer (highest bid) gains +1 extra on an exact hit and loses 1 extra on a miss. Nobody else gains from the declarer's miss.",
      "why": "This keeps Rutersju's declarer as a real, two-sided risk instead of a gift to the table.",
      "fixes": "P2"
    },
    {
      "what": "Bids are now made one at a time, each player hearing the earlier bids. Bidding starts with the player to the left of the priority seat and ends with the priority seat, which rotates every deal. The last bidder may not make the bids add up to exactly 3 (the 'hook').",
      "why": "Since exactly 3 tricks are played and the bids cannot total 3, at least one player must miss every deal. This rules out a universal all-zero table. Each bidder must also infer hand strength from the earlier bids. Rotating the last seat spreads the hook's burden and its information advantage evenly across seats.",
      "fixes": "P3, P5"
    },
    {
      "what": "Bids are public before the tricks are played, and someone must miss. Trick play therefore becomes deliberate: you can play a high card to give a trick to a 0-bidder, or under-play to deny a bidder their count.",
      "why": "This turns the luck of the deal into a contest of steering tricks. A weak hand can still score by hitting 0 and by breaking a rival's exact count. A strong hand can be broken by opponents who read its bid.",
      "fixes": "P4"
    },
    {
      "what": "The player count is kept at 3–5, with 3 deals per player (9/12/15 deals), the rotating priority seat and the numeric card strengths resolved by highest strength.",
      "why": "Repeated deals average out the luck of the deal. Rotation removes any seat edge. Simultaneous highest-strength tricks stay within the engine and within 20 steps.",
      "fixes": "P4"
    }
  ],
  "keeps": [
    "The 36-card pack with ♦7 as the unbeatable top card and the other diamonds as trumps",
    "Three cards each and three tricks per deal",
    "Bidding the exact number of tricks, from 0 to 3",
    "A declarer, the highest bidder with ties going to the last tied bidder, who carries extra risk and reward",
    "Exactness as the core skill: too many tricks is as bad as too few"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The trick structure is sound; the scoring made bidding 0 riskless and dominant. The changes make misses cost, add a hook rule so someone must miss each deal, and switch to sequential bidding so bids carry information. Together these restore a real bidding decision and opponent-steering in play, within the limits."
  },
  "variation": {
    "name": "Rutersju Hook",
    "summary": "A three-card exact-bidding trick game. Players bid in turn, the last bidder may not make the bids total 3, so someone must miss every deal. Exact hits score 3 + bid, every miss loses 2 per trick of error, and the declarer carries an extra ±1.",
    "players": {
      "min": 3,
      "max": 5,
      "suggested": 4
    },
    "rules": "SETUP. Use a 36-card French pack (6, 7, 8, 9, 10, J, Q, K, A in ♣ ♥ ♠ ♦). Seats are numbered 1 to N (N = 3, 4 or 5). Every player starts with 0 points. The game lasts 3 deals per player: 9 deals with 3 players, 12 with 4, 15 with 5. The priority seat is seat 1 in deal 1 and moves one seat to the left after each deal.\n\nCARD STRENGTH. Every card has a unique strength from 1 to 36. The higher strength always wins.\n- ♦7 = 36.\n- The other diamonds: ♦A=35, ♦K=34, ♦Q=33, ♦J=32, ♦10=31, ♦9=30, ♦8=29, ♦6=28.\n- The plain suits: ♠A=27, ♥A=26, ♣A=25, ♠K=24, ♥K=23, ♣K=22, ♠Q=21, ♥Q=20, ♣Q=19, ♠J=18, ♥J=17, ♣J=16, ♠10=15, ♥10=14, ♣10=13, ♠9=12, ♥9=11, ♣9=10, ♠8=9, ♥8=8, ♣8=7, ♠7=6, ♥7=5, ♣7=4, ♠6=3, ♥6=2, ♣6=1.\n\nEACH DEAL.\n1. Deal. Shuffle the full pack and deal 3 cards face down to each player. Each hand is seen only by its owner. Undealt cards stay hidden for the whole deal.\n2. Bid (in turn). Starting with the player to the LEFT of the priority seat and going left, each player in turn announces a bid of 0, 1, 2 or 3, hearing all earlier bids. The priority seat bids last.\n3. The hook. The last bidder (the priority seat) may not choose a bid that makes the sum of all bids exactly 3. The sum of the others' bids can only exceed 3 in this case if… it never matters: when the others' sum is already above 3, every bid is allowed.\n4. Declarer. The player with the highest bid is the declarer. If several players tie for the highest bid, the one among them who bid LAST is the declarer. If every bid is 0, there is no declarer (the hook allows this only when the bids can total 0, which is permitted because 0 ≠ 3). Announce all bids and the declarer.\n5. Tricks. Play 3 tricks. In each trick, every player secretly and simultaneously chooses one card from their hand. All chosen cards are revealed together. The card with the highest strength wins the trick, and its player adds 1 to their trick count. There is no need to follow suit. Played cards stay face up and public.\n6. Settlement, for each player separately, where d = |bid − tricks won|:\n   a. If d = 0, the player gains 3 + bid points (bid 0 → 3, bid 1 → 4, bid 2 → 5, bid 3 → 6).\n   b. If d > 0, the player loses 2 × d points.\n   c. The declarer, if there is one, additionally gains 1 point if their d = 0, or loses 1 point if their d > 0.\n   Because exactly 3 tricks are won and the bids never total 3, at least one player misses every deal.\n7. Announce all bids, trick counts and point totals. Move the priority seat one place to the left.\n\nThere is no discussion phase. Players communicate only through their bids, which are public and made in turn, and through the cards they play. Scores may go negative.\n\nEND. After the last deal, the single player with the highest point total wins. If two or more players tie for the highest total, the game is a draw.",
    "objective": "After 3N deals, the single player with the highest total points wins. A tie for the highest total is a draw.",
    "expected_effect": "Bidding becomes a real reading problem. You estimate your sure tricks from your hand and from the bids before yours, and the last bidder must pick which way to break the total of 3 knowing someone will miss. 'Always bid 0' now loses 2 or more whenever it is forced to win a trick: a top card, or a high card no one else beats. It therefore loses to hand-reading players. 'Always bid 3' almost always loses 4–8 per deal. 'Always bid 1' scores roughly 0 on average. All three can lose. In play, the public bids let players hand unwanted tricks to 0-bidders or deny bidders their count, so a weak hand can still profit and a strong hand can be broken. The deal still matters, but a correct 0 earns 3 against 6 for a correct 3, and 9–15 deals plus deliberate spoiling let skill outweigh it. The rotating last-bidder seat gives no seat an edge over a full game. Talk is left out: the in-turn bids already carry the information that matters, and open talk would mainly let players gang up on whoever leads without adding any inference beyond what bids and play provide."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 15,
    "choice_steps_per_round": 4,
    "attributes": 10,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 15
  }
}
```
````
