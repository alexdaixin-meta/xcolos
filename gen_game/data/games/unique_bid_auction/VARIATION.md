# Variation: Lowest Unique Number

Over 12 rounds, 3 to 5 players each secretly pick a number from 1 to 5. The player with the lowest number picked by exactly one player wins the round and scores that number, so players weigh safe low numbers against valuable high ones while reading each other's habits.

Players: 3 to 5, best with 4

## Review of the original

Unique Bid Auction: players pay a fee per bid and secretly submit any number of penny-precise bids up to a cap. In the lowest-unique version the smallest amount bid by exactly one player wins the lot at that price; the highest-unique version is the mirror image.

- **non_degenerate**: bad. With two players and lowest-unique, bidding the minimum (1 cent) cannot lose. If the opponent also bids it, nobody wins (a draw); otherwise the minimum is unique and lowest. Under 'higher total wins' this is a dominant thoughtless policy. Buying many bids also lets the richest player cover a whole range, so money beats choice.
- **skill_sensitive**: weak. As a one-shot game with many anonymous players it is close to a lottery. The equilibrium is a mixed strategy, and an individual player's edge over random bidding is small next to the variance of who else picked which number.
- **headroom**: weak. A single auction gives no history to learn from, so a strong player cannot improve on the mixed equilibrium. With 100 players and penny precision, a weak player's outcome is noise.
- **reasoning_dependent**: good. Bids stay hidden until close, and the core question (what will others pick, and which number will be left unique) is genuine opponent modelling. The one-shot, large-field form simply makes poor use of it.
- **verifiable**: good. The winner follows from counting how often each amount was bid and taking the lowest amount bid exactly once. This is pure arithmetic.
- **fits_platform**: weak. The original allows unlimited bids per player, penny precision, up to 100 players and per-bid fees paid in money. That is too much state and too many choices per step. The core simultaneous number pick fits well.

## Problems

- With 2 players, always bidding the minimum cannot lose, so the game is degenerate under a highest-total winner rule.
- Unlimited multiple bids per player let a player buy coverage of a range instead of reasoning, and they explode the choice space.
- Penny-precise bids and up to 100 players make the choice space huge and the outcome a lottery.
- A single one-shot auction gives no history, so there is no opponent modelling or planning over rounds, and luck dominates skill.
- In the lowest-unique version the lowest number is always the most valuable to win with, so the only tension is the risk of collision, not value against safety.

## Changes

- Fix the player count at 3 to 5 (suggested 4), so that a collision on the minimum benefits third parties. (fixes: With 2 players, always bidding the minimum cannot lose, so the game is degenerate under a highest-total winner rule.): With three or more players, two players sitting on 1 cancel each other and hand the round to someone else, so always picking 1 can lose.
- Each player picks exactly one number per round, from 1 to 5. There are no fees and no multiple bids. (fixes: Unlimited multiple bids per player let a player buy coverage of a range instead of reasoning, and they explode the choice space.): This removes buying coverage and keeps the choice small, clear and buildable.
- Use a small whole-number range (1 to 5) instead of pennies, with a small field of players. (fixes: Penny-precise bids and up to 100 players make the choice space huge and the outcome a lottery.): Each pick then meaningfully changes who is unique, and choices change outcomes.
- Play 12 rounds, reveal all picks after each round, and decide the game by the highest total. (fixes: A single one-shot auction gives no history, so there is no opponent modelling or planning over rounds, and luck dominates skill.): Revealed history lets players model each opponent's habits, exploit them, and plan blocks against the leader over several rounds.
- The player with the lowest unique number wins the round and scores points equal to that number (1 to 5). (fixes: In the lowest-unique version the lowest number is always the most valuable to win with, so the only tension is the risk of collision, not value against safety.): Low numbers win more often but pay little, and high numbers pay a lot but rarely survive. This adds a real trade-off between safety and value on top of collision risk.
- Add a simultaneous one-message talk phase before each pick. (fixes: A single one-shot auction gives no history, so there is no opponent modelling or planning over rounds, and luck dominates skill.): Only one player can win each round and only one can win the game, so messages become bluffs, feints and calls to gang up on the leader by colliding with them. Talk gives players something to reason about; it is not a coordination device that removes the choice.

## Kept from the original

- Secret simultaneous submission of numbers, revealed only at close.
- The lowest-unique rule: the smallest number chosen by exactly one player wins.
- If no number is unique, nobody wins the round.
- The central tension of guessing which numbers others will crowd onto and which will be left alone.

## The variation's rules

Setup: 3 to 5 players (4 suggested). Every player starts with a score of 0. The game lasts exactly 12 rounds.

Each round has these phases:

1. Talk. Every player writes one short message (at most 30 words) at the same time, without seeing the others. All messages are then shown to everyone together. Messages are not binding: players may claim, threaten or lie freely.

2. Pick. Every player secretly and simultaneously picks one whole number from 1 to 5. No player sees any other pick before choosing.

3. Reveal. All picks are revealed together, showing who picked what.

4. Count. For each number from 1 to 5, count how many players picked it.

5. Winner of the round. A number is 'unique' if exactly one player picked it. The round winner is the player who picked the lowest unique number. If no number is unique, nobody wins the round.

6. Score. The round winner adds points equal to their number (1 to 5) to their score. Nobody else scores this round.

7. Announce. The round's picks, the winning number (or 'no winner') and all players' current scores are announced to everyone.

After round 12 the game ends.

Objective: After 12 rounds, the player with the highest total score wins. If two or more players tie for the highest total, the game is a draw.

Expected effect: Always picking 1 wins often against careless fields but scores only 1 point per win. It is also easy to punish: a rival who also sits on 1 cancels it and hands the round to whoever holds the lowest unique number elsewhere. Always picking 5 rarely wins. Good play means modelling each opponent from the revealed history (who crowds low, who drifts high), mixing unpredictably, and timing grabs at 3 to 5 when others are expected to collide lower. Talk passes both tests. Players disagree because only one can win each round and only one can win the game, so a player who follows another's announced plan ('I'll take 2, you take 3') simply hands that player the lower unique number. Players also negotiate blocks against the leader ('both of us take 1 so the leader's 1 dies'). These blocks cost the blockers too, so trusting such a call is a real bet. As the leader pulls ahead, trailing players have reasons to collide with them, which keeps the late rounds contested instead of settling into a single safe pick.

## Complexity (the designer's count, against the limits)

- steps_per_round: 10 (limit 20)
- choice_steps_per_round: 2 (limit 4)
- attributes: 9 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 12 (limit 40)

## The rules played with numbers (every simple policy, 1200 games each)

no problems found

- numbers (seat 1's policy, outcome against random opponents): random: win 20% draw 6% loss 74%; always b1: win 32% draw 10% loss 58%; always b2: win 37% draw 9% loss 54%; always b3: win 35% draw 6% loss 59%; always b4: win 21% draw 4% loss 74%; always b5: win 4% draw 1% loss 94%
- everyone playing 'always b1' (best joint play): mean total 0.0; every player tied in 100% of games, so 0% are decided by the draw
