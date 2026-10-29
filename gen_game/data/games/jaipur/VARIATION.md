# Variation: Jaipur Bazaar (Balanced Schedule)

A two-player, 16-round duel of taking goods from a shared market and selling sets on falling prices. Hands are hidden, and the restock schedule is public and paired so that both seats get equal first refusals.

Players: 2 to 2, best with 2

## Review of the original

Jaipur is a two-player card-trading game. Players take goods or camels from a shared five-card market and sell sets of one good for falling-price tokens, with bonuses for large sets and for owning the most camels; the best of three rounds wins. The previous XColos variation turned it into a 16-round, three-good, count-based duel with a public restock schedule and a private draw each round.

- **non_degenerate**: weak. No thoughtless policy wins. Always CAMELS scores at most 5 and loses to one Diamond pair sale (14). Always SELL mostly passes or dumps singletons. Always TAKE never scores. Always pass scores 0. Sell-early (locking a high price) versus hold (set bonuses) is a real tension. The previous variation still gave the seats unequal value. A had first refusal on both sellable market Diamonds (rounds 5 and 11), and B's only Diamond, in round 16, could never be sold. Cloth first refusals ran 3 to B and 2 to A. A also acted last in round 16 with full information. The net edge to A was about 8 to 12 points, comparable to the margin between equal players.
- **skill_sensitive**: good. Points come from timing sales against a falling price ladder (Diamond pairs 14, 10, 6), building 3+ sets for +3/+5/+8, choosing when to spend camels on multi-card takes, and denying the opponent market cards. A careful player reliably beats a random or greedy one. Private draws add variance, but every one of them is offset by public market play.
- **headroom**: good. A weak player can still make a few pair sales. A strong player can keep improving: tracking the opponent's likely hand from the public deck composition and their takes and sales, preempting their sale by selling first to crash the price, and managing the camel race near the end.
- **reasoning_dependent**: good. Hands and private draws are hidden. The deck composition and every take and sale are public, so a player can infer the opponent's hand. The restock schedule is public, so planning over several rounds pays.
- **verifiable**: good. Scores are price times count plus fixed bonuses plus a camel bonus. Everything is arithmetic on tracked counts.
- **fits_platform**: good. Turn-based, text-only, with no board. It uses count attributes and one deck draw per round, takes 16 rounds, and stays within the step limits.

## Problems

- P1: The Diamond restock schedule gave player A first refusal on both sellable market Diamonds, while B's only Diamond came in round 16, when it was unsellable. This was a swing of about 10 to 14 points.
- P2: Cloth first refusals were uneven: B 3, A 2.
- P3: A strict odd/even alternation made A act last in round 16 with full knowledge, and restocks were not paired by seat, so per-type first refusals could not be balanced.
- P4: Goods restocked in the last round can only be taken, never sold, so whoever gets first refusal on a last-round goods card gains nothing, while the other seat may have lost a real card earlier.

## Changes

- Turn order follows the ABBA pattern: A, B, B, A, A, B, B, A, A, B, B, A, A, B, B, A. Each player is first in 8 rounds. A makes the game's first action; B makes the game's last action. (fixes: P3): Pairs the rounds so that each consecutive pair (1-2, 3-4, ...) has one A-first round and one B-first round. It also splits the first-move and last-move advantages between the seats instead of giving A both opening tempo and final-information play.
- The restock schedule repeats the same type in both rounds of each pair. Cloth goes in rounds 1-2 and 9-10, Silver in 3-4 and 11-12, Camel in 5-6 and 15-16, and Diamond in 7-8 and 13-14. (fixes: P1): Each seat gets first refusal on exactly 2 Diamonds, 2 Silver, 2 Cloth and 2 Camels. The Diamonds arrive at comparable times for both players: B first in round 7 and A first in round 8; A first in round 13 and B first in round 14. All of them come early enough to be sold.
- The same pairing gives each seat exactly 2 Cloth first refusals. (fixes: P2): Removes B's extra Cloth.
- The final pair, rounds 15 and 16, restocks Camels instead of goods. (fixes: P4): A card taken in round 16 can still matter, through the camel majority. No unsellable goods card is ever restocked.

## Kept from the original

- The take-or-sell turn with a hand limit of 7
- Taking several cards costs camels
- Taking all camels from the market
- A falling price ladder per good, with bonuses for sets of 3, 4 and 5 or more
- A minimum sale of 2 for the precious goods
- +5 for camel majority
- Hidden hands and private draws from a deck of public composition

## The variation's rules

CARDS AND STATE
- There are three goods types (Diamond, Silver, Cloth) and camels.
- Each player has a hidden hand, recorded as counts of Diamond, Silver and Cloth. Each player also has a public camel herd (a count) and a public score.
- The market is public and holds counts of Diamond, Silver, Cloth and Camel.
- Each good has a public price. The starting prices are Diamond 7, Silver 5, Cloth 3.
- A private deck of 20 goods cards is shuffled once at the start: 5 Diamond, 7 Silver, 8 Cloth. The composition is public.

SETUP
- The market starts with 2 Camel, 1 Silver and 1 Cloth.
- Each player starts with 1 Silver and 1 Cloth in hand, 1 camel in herd, and score 0.

TURN ORDER
- The round's first player is:
  - A in rounds 1, 4, 5, 8, 9, 12, 13 and 16;
  - B in rounds 2, 3, 6, 7, 10, 11, 14 and 15.
- The other player is second in that round.

EACH ROUND (16 rounds)
1. Restock: add one card to the market according to this public schedule.
   - Rounds 1 and 2: Cloth. Rounds 3 and 4: Silver. Rounds 5 and 6: Camel. Rounds 7 and 8: Diamond.
   - Rounds 9 and 10: Cloth. Rounds 11 and 12: Silver. Rounds 13 and 14: Diamond. Rounds 15 and 16: Camel.
2. Private draw: the round's first player draws the top deck card into their hand.
   - Only they see its type. Both players are told that a draw happened.
   - If that hand already holds 7 goods, the drawn card is discarded instead, and only the drawer learns its type.
3. The first player takes one turn, which is announced publicly.
4. The second player takes one turn, which is announced publicly.

A TURN: choose exactly one action.
- TAKE <good> <n>: take n cards (n at least 1) of one goods type from the market into your hand. Three conditions apply:
  - the market must hold at least n of that type;
  - you must return n-1 camels from your herd to the market, so you must own at least n-1 camels;
  - your hand must hold at most 7 goods afterwards.
- CAMELS: move all camels in the market into your herd. The market must hold at least 1 camel.
- SELL <good> <n>: discard n cards of one good from your hand.
  - Diamond and Silver need n of at least 2. Cloth needs n of at least 1.
  - You score n times that good's current price.
  - You also score a bonus: +3 if n is 3, +5 if n is 4, +8 if n is 5 or more.
  - Then that good's price drops by n, to a minimum of 1.
- An illegal or missing choice counts as a pass: nothing happens.
- What is announced publicly: the action type, the good and n. The type of a privately drawn card is never announced.

END
- After round 16, the player with strictly more camels in their herd scores +5. If camels are tied, nobody gets the bonus.
- Cards left in hand score nothing.

Objective: After the camel bonus, the player with the higher score wins. Equal scores are a draw.

Expected effect: Each seat now has first refusal on 2 sellable Diamonds, 2 Silver, 2 Cloth and 2 Camels, and each draws privately 8 times. The first-move edge (A) and the last-move edge (B) offset each other, so seat results should be close to even. Simple policies still lose: always CAMELS scores at most 5, always pass scores 0, and always SELL dumps singletons at falling prices. Play centres on reading the opponent's hidden hand from the public deck composition and their takes, racing to sell before they crash a price, deciding when 3+ sets are worth the wait, and contesting the final camel restocks for the +5 bonus. The private draws add some variance, but contested market cards and price preemption let a better player overcome a worse deal. There is no talk phase, because with two players and a zero-sum winner rule talk would add nothing to reason about.

## Complexity (the designer's count, against the limits)

- steps_per_round: 14 (limit 20)
- choice_steps_per_round: 2 (limit 4)
- attributes: 19 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 16 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
