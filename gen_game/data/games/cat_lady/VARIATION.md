# Variation: Cat Lady: Secret Favourites (Balanced)

Players draft 2-card lots from a public market, feeding cats, building toy sets, chasing catnip and collecting strays. Each player holds a secret Favourite that adds bonus points in one category. Seat order is fully symmetric, and the Favourites are tuned to be worth about the same.

Players: 3 to 4, best with 4

## Review of the original

Cat Lady is a 2-4 player card-drafting game. Players take rows or columns from a 3x3 market of cards and collect cats that must be fed with food, plus toys (scored in sets), catnip (scored on an increasing scale), stray cats and other cards. Highest victory points wins. The previously reviewed variation replaced the grid with a market of 2-card lots drafted in rotating seat order, and added one secret Favourite per player.

- **non_degenerate**: weak. No simple policy wins. 'Always earliest letter' and 'always latest letter' take effectively random lots, collect unfed cats at -1 and attract the food penalty, so they lose to a greedy drafter. 'Always most catnip' splits 16 cards with any other chaser and ignores Strays. 'Always most points now' ignores feeding dependencies. However, the 4-player game ran 9 rounds, so seat 1 picked first 3 times and last 2 times while seat 4 did the reverse. Picking first from 5 lots instead of last from 2 is worth about 2-4 points, which gave seat 1 an edge of about 4-8 points in totals of 40-60. That is a built-in seat edge.
- **skill_sensitive**: good. Lot contents are public before anyone picks. Values depend on what a player already holds (food against cats, toy colours, the catnip curve) and on what rivals need. The skilled drafter plans feeding, completes sets and hate-drafts. Randomness lies only in which lots appear, and every player faces the same market.
- **headroom**: good. A weak player still scores through Strays (3 flat) and loose toys. A strong player can keep improving through timing, denial and reading Favourites from rivals' picks. Food scarcity (38 food for 20 cats) makes feeding a real planning problem.
- **reasoning_dependent**: good. Each player's secret Favourite changes what they value, so players must infer rivals' Favourites from their picks to predict and deny. Planning across rounds matters for feeding, the catnip curve and toy sets. The Favourite gap was a minor lottery element: Cats was worth about +10-12 and Catnip about +6-7.
- **verifiable**: good. Every score is arithmetic on public counts plus a revealed Favourite. The winner and tie-break are numeric.
- **fits_platform**: good. The game is text-only, sequential picks are turn-based, and there is no board. It uses one hidden element, one market deal per round, at most 4 choice steps per round and at most 12 rounds.

## Problems

- P1: In the 4-player game, 9 rounds cannot be split evenly over 4 seats. Seat 1 picks first 3 times and last 2 times while seat 4 does the reverse, a structural edge of about 4-8 points.
- P2: Favourite bonuses are uneven (Cats about +10-12, Toys about +8-10, Catnip about +6-7, Strays about +6-8), so the secret deal tilts the result before skill acts.
- P3: Because the deck is used differently at 4 players, the Favourite values need re-checking against how many Catnip and Stray cards actually appear.

## Changes

- The 4-player game becomes 8 rounds of 5 lots of 2 cards (80 of the 96 cards are dealt; the bottom 16 are never used). The first picker still rotates by seat each round. (fixes: P1): Every seat now picks first twice, second twice, third twice and last twice, so the move-order edge disappears. The 3-player game stays at 12 rounds of 4 lots, already symmetric at 4 of each position.
- The Cats Favourite becomes +2 per fed cat, capped at +10. (fixes: P2): This removes the top end of the strongest Favourite: realistic value about +8-10.
- The Catnip Favourite becomes +2 per Catnip card owned (including any beyond 6), capped at +12. (fixes: P2): This raises the weakest Favourite. Catnip is heavily contested, and a holder typically gets 4-5 cards, so it is worth about +8-10.
- The Strays Favourite (4 players only) becomes +3 per Stray Cat. The Toys Favourite stays at +1 per Toy card. (fixes: P2, P3): With about 6-7 Strays dealt across 8 rounds, a holder gets about 3, worth about +9. Toys is already about +8-10. All four Favourites now sit near +8-10, so the deal changes what to draft, not who leads.
- No discussion phase is added. (fixes: P2): Picks are sequential and public, so Favourites are already inferred from behaviour. Talk would add only cheap claims that cannot be checked, and no plan players could share, because every player competes for one win. It also costs steps.

## Kept from the original

- Drafting groups of cards from a shared face-up market, with the cut-down market of 2-card lots from the previous variation
- Cats must be fed: each needs 2 food, fed cats score 5, unfed cats score -1
- Toy sets of Red, Blue and Green; the increasing catnip scale capped at 6 cards; Strays at 3 flat
- The penalty for hoarding the most leftover food
- Secret Favourites revealed at the end, inferred from picks
- Highest total wins, tie-break most fed cats

## The variation's rules

SETUP.
The deck has 96 cards:
- 18 Food-1 (1 food each)
- 10 Food-2 (2 food each)
- 20 Cat
- 8 Stray Cat
- 24 Toy (8 Red, 8 Blue, 8 Green)
- 16 Catnip
Shuffle the deck once.
Each player is secretly dealt one Favourite, and every player gets a different one. With 3 players the Favourites are drawn from {Cats, Toys, Catnip}; with 4 players they are drawn from {Cats, Toys, Catnip, Strays}. Only the owner knows their Favourite.
Seat the players in a fixed order, seat 1 to seat N.

ROUNDS.
With 3 players there are 12 rounds; with 4 players there are 8.
In round r, the first picker is seat ((r-1) mod N) + 1, and the others follow in seat order. Over the game, every seat holds each picking position equally often: 4 times each with 3 players, 2 times each with 4 players.

EACH ROUND.
1. Deal the market from the top of the deck. With 3 players deal 4 lots (Lot A to Lot D) of 2 cards each; with 4 players deal 5 lots (Lot A to Lot E) of 2 cards each. Announce every lot's contents to all players.
2. Starting with the first picker, each player in turn chooses one remaining lot by its letter. Each player sees all earlier picks.
3. A chosen lot goes to that player at once. Food cards add their food value to the player's food total. Cats, Strays, Toys (by colour) and Catnip are added to the player's counts. Everything a player owns is public, except their Favourite.
4. When every player has picked, the one leftover lot is discarded.
5. After the last round, go to final scoring. With 4 players, the 16 cards still in the deck are never used.

FINAL SCORING. For each player:
- Feeding: each Cat needs 2 food. Fed cats = the smaller of (Cats) and (food ÷ 2, rounded down). Each fed cat scores 5 and each unfed Cat scores -1. Leftover food = food total - 2 × fed cats.
- Strays: each Stray Cat scores 3.
- Toys: each Toy scores 1, plus 4 for each complete set of one Red, one Blue and one Green. Number of sets = the smallest of the three colour counts.
- Catnip: with n Catnip cards, counting at most 6, the player scores n(n+1)/2 (maximum 21). Catnip beyond 6 scores nothing here.
- Food penalty: the player or players with the most leftover food lose 2 points, provided that amount is at least 1.
- Favourite bonus, revealed now:
  - Cats: +2 per fed cat, maximum +10.
  - Toys: +1 per Toy card.
  - Catnip: +2 per Catnip card owned (including any beyond 6), maximum +12.
  - Strays (4 players only): +3 per Stray Cat.

Objective: The highest final total wins. If players are tied, the tied player with the most fed cats wins. If they are still tied, those players draw.

Expected effect: With 8 rounds at 4 players, every seat picks first, second, third and last twice, so seat order no longer decides close games. Favourites now cluster around +8-10, so the secret deal mainly changes what each player should draft rather than who is ahead. Skill shows in planning food against cats, timing toy sets and the catnip curve, inferring rivals' Favourites from their picks, and denying key lots. No simple policy is safe. Fixed-letter picking accumulates unfed cats and the food penalty. Catnip-only play splits a contested suit and ignores Strays. Greedy points-now play misses feeding dependencies and denial. Talk is left out: every player competes for one win, picks already reveal intent, and claims about Favourites cannot be checked, so a discussion would add words, not reasoning.

## Complexity (the designer's count, against the limits)

- steps_per_round: 12 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 15 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 12 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
