# psychological_jujitsu: ready for review

Built from the variation **Psychological Jujitsu: Hidden Favourites** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Each player is secretly dealt a different 'bonus card' value from 5 to 9. Winning that prize earns +5 extra points. (fixes: There is no private information. Hands are fully deducible, so the only inference is guessing an opponent's style, which limits hidden-state reasoning.): This gives each player a private stake that shapes what they should do. Rivals must infer it from unusually strong bids on middling prizes. Every bonus is the same flat +5 and drawn from a narrow mid range, so it changes what to fight for without deciding who ends ahead.
- The game is fixed at 3 to 4 players, and the original's 'next highest' variant is adopted. Tied highest bids are cancelled and the prize goes to the highest bid that is not tied. If every bid is tied, the prize is discarded. (fixes: The original gives two tie rules as alternatives. A rule set must pick one, and with 3 or more players the 'discard everything' rule throws away many prizes and blunts interaction.): This creates real multi-way tactics. Two rivals clashing at the top can hand the prize to a third player's modest bid. Because only one player can win, it also gives talk something to fight over.
- A short simultaneous message phase is added before each bid. (fixes: There is no private information. Hands are fully deducible, so the only inference is guessing an opponent's style, which limits hidden-state reasoning.): With one winner and hidden bonus cards, players can bluff about their bonus, threaten to contest a prize, or try to coordinate against the leader. The tie rule makes naive coordination dangerous: if two players agree to both bid 13, they cancel out and hand the prize to the next highest bidder.
- At the start of each round, the engine announces every player's remaining hand, every score and the remaining prize values. (fixes: Models may lose track of which cards remain, which turns bad play into bookkeeping errors rather than reasoning errors.): This removes bookkeeping failure so that results reflect strategy.
- An invalid or missing bid is replaced by that player's lowest remaining card. (fixes: The rules do not say what happens if a player names a card they no longer hold.): The rules become complete and build-able, and an invalid bid carries a mild penalty.
- Final ties are resolved as a draw among the tied leaders. (fixes: The original never says how a tie for the highest final total is resolved.): The winner rule becomes complete and purely arithmetic.

Objective: The player with the highest final score wins. If two or more players tie for the highest score, the game is a draw among them.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. The game is symmetric. Every player has the same 13-card hand, bids are simultaneous, prizes are public when revealed, and bonus values come from the same symmetric draw, so no seat has an edge from move order.

Thoughtless policies, judged by the winner rule:
(a) ALWAYS HIGHEST (13,12,...,1). Its b
- playable: pass. The rules are complete.
- Invalid bids default to the lowest remaining card.
- The cancellation rule is precise and comes with a worked example.
- The all-cancelled case is covered: the prize is discarded.
- The final tie is a draw among the tied players.
- The bonus announcement rule is explicit.
-
- reasoning_over_luck: pass. Chance enters in two places.
- Prize order: it is identical for all players and revealed one card at a time, so it is symmetric.
- Bonus assignment: it is worth +5 once, and only if that player wins that specific prize, which is contested and depends on strategy.
I estimate chance at roughly 15-25% 

## Complexity

- steps_per_round: designed 11, built 10, limit 20
- choice_steps_per_round: designed 2, built 2, limit 4
- attributes: designed 19, built 25, limit 20 (built: 80)
- hidden_elements: designed 2, built 4, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 13, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: every hand holds the 13 cards 1 to 13 and scores start at 0 (all bid 13, cancelled)
- pass: Setup: three distinct bonus values leave two in the pool of five
- pass: Setup with 4 players: four bonus values dealt, one left in the pool
- pass: Round start draws the prize from the pile and removes it
- pass: A round with the talk poll completes and the round counter advances
- pass: Bids are revealed after all are in; highest unique bid wins
- pass: The bid card leaves the hand and is not offered again
- pass: Matching bids are cancelled and the unique lower bid wins
- pass: Bids 10, 10 and 4: the 4 wins the prize
- pass: Bids 7, 7, 7: all cancelled, no score changes
- pass: Winning a prize of 11 adds 11
- pass: Winning prize 7 with bonus 7 adds 12
- pass: Bonus round: total includes the +5 (announcement content not observable)
- pass: Game ends after round 13
- pass: Tied highest final scores share the win
- pass: Single highest final score wins alone

## Does the file follow the spec's shape? (flags for a person)

- rule R6 has no scenario: nothing checks it

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 4], results {'seat 1': 12, 'seat 3': 14, 'seat 2': 10, 'seat 4': 4}, 75-100 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 91.0 decisions, prompts of 182 characters on average (longest 194)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 1': 22, 'seat 3': 17, 'seat 2': 21}
- always `first@seat1`: won 16, lost 42, drew 2
- always `first@seat2`: won 22, lost 37, drew 1
- always `last@seat1`: won 27, lost 30, drew 3
- always `last@seat2`: won 26, lost 34, drew 0

## Choices the rules did not make

- 3 to 4 players, suggested 3: The designer chose 3, so it is kept. Cancellation of matching bids needs at least 3 bidders to create the outbidding-by-colliding tension; with 2, any tie simply voids the round. The maximum stays at the source's 4, since more bidders make most rounds collapse into cancellations and drown out the hidden-favourite signal.
- Talk kept as a simultaneous poll with broadcast: The source specifies simultaneous talk. Players genuinely disagree, since everyone wants the prize, so bluffing about intended bids or hinting at a favourite gives others something to reason about.
- Strategy check: A thoughtful player avoids bids others are likely to duplicate, saves high cards for high prizes, uses talk to provoke collisions between rivals, and infers rivals' bonus values from how eagerly they chase mid prizes.
- Hands made public: The rules announce every remaining hand each round, and hands are deducible from the revealed bids anyway.

## Simplifications

- The shuffled face-down prize pile is modelled as a public list of remaining values with a random draw each round: The rules announce the remaining prize values each round; only the order is hidden, and a random draw reproduces that.
- The '+5 bonus' announcement and the end-of-game bonus reveal are done with tell steps: The bonus attribute stays visible only to its owner until the game ends.

## Encoding attempts

- 1: passed
