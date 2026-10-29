# Variation: Rutersju Hook

A three-card exact-bidding trick game. Players bid in turn, the last bidder may not make the bids total 3, so someone must miss every deal. Exact hits score 3 + bid, every miss loses 2 per trick of error, and the declarer carries an extra ±1.

Players: 3 to 5, best with 4

## Review of the original

Rutersju is a short Scandinavian trick-taking game for 3 to 12 players. Each player gets three cards, players bid how many of the three tricks they will take, and the highest bidder becomes declarer against the rest. ♦7 is the top trump. A declarer who makes the bid exactly scores it; a declarer who misses pays one point per trick of error to each opponent.

- **non_degenerate**: bad. In the reviewed variation a bid of 0 is never the declarer, so it never pays the miss penalty. It still scores the same +3 on a hit as a bid of 3, and it collects d from every declarer who misses. At 4–5 players 'always bid 0, dump high cards early' hits about 60–70% of the time and wins or draws most games against both random and sensible play. Any bid above 0 is a liability: +1 at best, and −d against every rival at worst. The bidding decision collapses.
- **skill_sensitive**: weak. With nearly everyone bidding 0, each deal is decided by who was dealt top cards that cannot be dumped (P = 1/N per deal). The only skill left is a simultaneous dumping guess. About 60–70% of the per-deal swing is the deal itself.
- **headroom**: weak. A bot that bids 0 and dumps low is close to optimal at 4–5 players. A strong player has little to improve on, because good bidding is not rewarded.
- **reasoning_dependent**: weak. Hands are hidden, and bids plus face-up discards could carry information. But when all bids are 0 the bids reveal nothing, and there is nothing to act on even if a player infers something.
- **verifiable**: good. Card strengths are fixed numbers. Trick winners, trick counts and scores all follow by arithmetic.
- **fits_platform**: good. Play is text-only with no board. Trick play is simultaneous with numeric strengths, and the step count was within limits (about 14–16).

## Problems

- P1: A bid of 0 pays the same as any other exact bid and is never the declarer, so it carries no risk. 'Always bid 0' dominates at 4–5 players.
- P2: A declarer's miss is a gift to every other player, so taking on the declarer bid is pure liability and nobody wants it.
- P3: Nothing stops everyone bidding 0 together, so the bids carry no information and no player is forced into a contested decision.
- P4: Under good play the deal decides each hand, because the holder of the top card simply misses. The skill left is a coin-flip dumping guess, so luck dominates.
- P5: Simultaneous blind bids mean no player reasons from others' bids when choosing their own, so there is little inference in the bidding.

## Changes

- An exact hit now scores 3 + bid (0→3, 1→4, 2→5, 3→6), and EVERY player who misses loses 2 points per trick of error, not only the declarer. Missing no longer feeds the other players. (fixes: P1): Bidding 0 while holding a card that will win a trick now costs 2 instead of being free. Higher bids are worth a little more, so a player should bid what the hand will take rather than hiding at 0. The slope is kept mild (3 to 6) so that a weak hand bid correctly still scores most of what a strong hand scores.
- The declarer (highest bid) gains +1 extra on an exact hit and loses 1 extra on a miss. Nobody else gains from the declarer's miss. (fixes: P2): This keeps Rutersju's declarer as a real, two-sided risk instead of a gift to the table.
- Bids are now made one at a time, each player hearing the earlier bids. Bidding starts with the player to the left of the priority seat and ends with the priority seat, which rotates every deal. The last bidder may not make the bids add up to exactly 3 (the 'hook'). (fixes: P3, P5): Since exactly 3 tricks are played and the bids cannot total 3, at least one player must miss every deal. This rules out a universal all-zero table. Each bidder must also infer hand strength from the earlier bids. Rotating the last seat spreads the hook's burden and its information advantage evenly across seats.
- Bids are public before the tricks are played, and someone must miss. Trick play therefore becomes deliberate: you can play a high card to give a trick to a 0-bidder, or under-play to deny a bidder their count. (fixes: P4): This turns the luck of the deal into a contest of steering tricks. A weak hand can still score by hitting 0 and by breaking a rival's exact count. A strong hand can be broken by opponents who read its bid.
- The player count is kept at 3–5, with 3 deals per player (9/12/15 deals), the rotating priority seat and the numeric card strengths resolved by highest strength. (fixes: P4): Repeated deals average out the luck of the deal. Rotation removes any seat edge. Simultaneous highest-strength tricks stay within the engine and within 20 steps.

## Kept from the original

- The 36-card pack with ♦7 as the unbeatable top card and the other diamonds as trumps
- Three cards each and three tricks per deal
- Bidding the exact number of tricks, from 0 to 3
- A declarer, the highest bidder with ties going to the last tied bidder, who carries extra risk and reward
- Exactness as the core skill: too many tricks is as bad as too few

## The variation's rules

SETUP. Use a 36-card French pack (6, 7, 8, 9, 10, J, Q, K, A in ♣ ♥ ♠ ♦). Seats are numbered 1 to N (N = 3, 4 or 5). Every player starts with 0 points. The game lasts 3 deals per player: 9 deals with 3 players, 12 with 4, 15 with 5. The priority seat is seat 1 in deal 1 and moves one seat to the left after each deal.

CARD STRENGTH. Every card has a unique strength from 1 to 36. The higher strength always wins.
- ♦7 = 36.
- The other diamonds: ♦A=35, ♦K=34, ♦Q=33, ♦J=32, ♦10=31, ♦9=30, ♦8=29, ♦6=28.
- The plain suits: ♠A=27, ♥A=26, ♣A=25, ♠K=24, ♥K=23, ♣K=22, ♠Q=21, ♥Q=20, ♣Q=19, ♠J=18, ♥J=17, ♣J=16, ♠10=15, ♥10=14, ♣10=13, ♠9=12, ♥9=11, ♣9=10, ♠8=9, ♥8=8, ♣8=7, ♠7=6, ♥7=5, ♣7=4, ♠6=3, ♥6=2, ♣6=1.

EACH DEAL.
1. Deal. Shuffle the full pack and deal 3 cards face down to each player. Each hand is seen only by its owner. Undealt cards stay hidden for the whole deal.
2. Bid (in turn). Starting with the player to the LEFT of the priority seat and going left, each player in turn announces a bid of 0, 1, 2 or 3, hearing all earlier bids. The priority seat bids last.
3. The hook. The last bidder (the priority seat) may not choose a bid that makes the sum of all bids exactly 3. The sum of the others' bids can only exceed 3 in this case if… it never matters: when the others' sum is already above 3, every bid is allowed.
4. Declarer. The player with the highest bid is the declarer. If several players tie for the highest bid, the one among them who bid LAST is the declarer. If every bid is 0, there is no declarer (the hook allows this only when the bids can total 0, which is permitted because 0 ≠ 3). Announce all bids and the declarer.
5. Tricks. Play 3 tricks. In each trick, every player secretly and simultaneously chooses one card from their hand. All chosen cards are revealed together. The card with the highest strength wins the trick, and its player adds 1 to their trick count. There is no need to follow suit. Played cards stay face up and public.
6. Settlement, for each player separately, where d = |bid − tricks won|:
   a. If d = 0, the player gains 3 + bid points (bid 0 → 3, bid 1 → 4, bid 2 → 5, bid 3 → 6).
   b. If d > 0, the player loses 2 × d points.
   c. The declarer, if there is one, additionally gains 1 point if their d = 0, or loses 1 point if their d > 0.
   Because exactly 3 tricks are won and the bids never total 3, at least one player misses every deal.
7. Announce all bids, trick counts and point totals. Move the priority seat one place to the left.

There is no discussion phase. Players communicate only through their bids, which are public and made in turn, and through the cards they play. Scores may go negative.

END. After the last deal, the single player with the highest point total wins. If two or more players tie for the highest total, the game is a draw.

Objective: After 3N deals, the single player with the highest total points wins. A tie for the highest total is a draw.

Expected effect: Bidding becomes a real reading problem. You estimate your sure tricks from your hand and from the bids before yours, and the last bidder must pick which way to break the total of 3 knowing someone will miss. 'Always bid 0' now loses 2 or more whenever it is forced to win a trick: a top card, or a high card no one else beats. It therefore loses to hand-reading players. 'Always bid 3' almost always loses 4–8 per deal. 'Always bid 1' scores roughly 0 on average. All three can lose. In play, the public bids let players hand unwanted tricks to 0-bidders or deny bidders their count, so a weak hand can still profit and a strong hand can be broken. The deal still matters, but a correct 0 earns 3 against 6 for a correct 3, and 9–15 deals plus deliberate spoiling let skill outweigh it. The rotating last-bidder seat gives no seat an edge over a full game. Talk is left out: the in-turn bids already carry the information that matters, and open talk would mainly let players gang up on whoever leads without adding any inference beyond what bids and play provide.

## Complexity (the designer's count, against the limits)

- steps_per_round: 15 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 10 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 15 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
