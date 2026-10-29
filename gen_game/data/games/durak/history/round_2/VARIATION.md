# Variation: Duel Durak (seeded)

Two-player Durak with 8-card hands, no drawing, and a hidden 20-card set-aside pile. The trump suit is chosen by cut-and-choose. Each bout has one attack, one optional throw-in and up to two defences. The first player to empty their hand wins. The only randomness is a single seeded shuffle in round 1.

Players: 2 to 2, best with 2

## Review of the original

Durak is a 2–6 player shedding game played with a 36-card deck and a trump suit. An attacker plays cards, and the defender must beat each one with a higher card of the same suit or with a trump, or else pick up the whole table. Players draw back up to six, and the last player still holding cards is the loser (the 'durak').

- **non_degenerate**: good. Every simple policy loses to sensible play. A player who always takes swells their hand and ends as durak. A player who always attacks with their highest card throws away trumps they need later. A player who never adds cards gives up tempo. The first attacker is set by the deal (lowest trump), so no fixed seat has an edge. With 3–6 players, the seat to the left of a strong attacker is slightly worse off, but the effect is minor.
- **skill_sensitive**: weak. Card counting, saving trumps and choosing when to take all reward skill. But drawing from the talon after every bout adds a lot of luck, so a single deal is noisy. With many players, who ends as durak also depends partly on who happens to gang up on whom.
- **headroom**: good. Play has many levels: tracking seen cards, timing trump spends, taking on purpose to collect a rank, and adding cards to strand the defender. A weak player still sheds cards and can survive a hand.
- **reasoning_dependent**: good. Hands and the talon are hidden. Good play means inferring the opponent's holding from what they beat, failed to beat or added, and planning the endgame once the talon is empty.
- **verifiable**: good. Whether a card beats another, which ranks may be added, and who runs out of cards are all mechanical facts that arithmetic can check.
- **fits_platform**: bad. The game is turn-based and text-only. But open-ended multi-player adding with clockwise priority, drawing order across up to 6 players, and up to 6 attacks per bout go far beyond 4 choice steps per round. Repeated talon draws exceed one random draw per round. The previous variation also failed the determinism test: the same seed gave different logs. That points to an unseeded or clock-based pick, randomness outside the single setup shuffle, fallbacks not computed from ordered data, or output produced by iterating over an unordered collection.

## Problems

- P1: Non-determinism. Replaying the same seed gave different logs. Likely causes are an unseeded or time-based random pick, randomness used outside the single setup shuffle, fallbacks not computed from ordered data, or hands, discards or announcements listed by iterating over a set or map.
- P2: Drawing from the talon every bout needs many random draws and makes a single deal luck-heavy.
- P3: Multi-player adding with clockwise priority and up to 6 attacks per bout needs far more than 4 choice steps per round.
- P4: With 3 or more players, whether you end as durak depends partly on seat position and on others' choices, not only on your own reasoning.
- P5: If a random card fixes the trump suit, the deal alone could decide the game.
- P6: The game needs a guaranteed end within 40 rounds, and every illegal or missing answer needs a deterministic resolution.

## Changes

- Randomness happens exactly once, at step 1 of round 1. The 36-card deck is built as an ordered list: Clubs, Diamonds, Hearts, Spades, and ranks 6 to 14 within each suit, with card id = suit index × 9 + rank − 6. The engine's seeded shuffle is applied to this list. Cards are dealt by fixed positions: positions 1–8 to player 1, then 9–16 to player 2, and 17–36 to the set-aside list in that order. No other random operation, clock value or external source is used anywhere. (fixes: P1: Non-determinism): The game has a single seeded source of randomness, so the same seed always gives the same deal.
- All hands, the discard pile and the set-aside pile are stored as ordered lists sorted ascending by card id. Every announcement and every fallback reads them in that order. Nothing iterates over a set or map. (fixes: P1: Non-determinism): This removes output and fallbacks that depend on iteration order.
- Every fallback is a fixed rule on ordered data. An illegal or missing offer becomes Hearts and Spades. An illegal or missing trump pick becomes the first offered suit in suit order. An illegal or missing attack becomes the attacker's lowest-rank card, with ties broken by lower suit index. An illegal or missing defence counts as TAKE. An illegal or missing throw-in counts as PASS. (fixes: P1: Non-determinism; P6: guaranteed end and deterministic resolution): Every fallback is deterministic and reproducible.
- Two players, 8 cards each, no drawing. The other 20 cards stay set aside face down and are never used. (fixes: P2: talon luck and repeated draws; P4: seat and coalition effects): This removes talon luck and repeated draws. It keeps a real inference problem: 28 unseen cards, of which 8 are in the opponent's hand.
- Each bout has one attack, one optional throw-in matching a rank on the table, and up to two defences. (fixes: P3: too many choice steps): This keeps choice steps at 4 per round while keeping attack, defend, take and add.
- The trump suit is chosen by cut-and-choose. Player 2 offers two different suits, and player 1 picks one of them as trump. The holder of the lowest trump attacks first. If neither player holds a trump, player 2 attacks first. (fixes: P5: deal deciding the game): Player 2 must offer two suits it can live with, and player 1 chooses after reading its own hand. Reasoning can offset a lopsided deal, and the two seat roles balance each other.
- The game ends when a hand empties, with a cap at round 40. At the cap, the player with fewer cards wins, and equal counts are a draw. (fixes: P6: guaranteed end and deterministic resolution): This guarantees an end with an arithmetic result.

## Kept from the original

- The 36-card deck, ranks 6 to Ace
- A trump suit that beats all other suits
- Beating a card with a higher card of the same suit or with any trump
- The attacker adding cards that match ranks already on the table
- A defender who fails takes the whole table
- A successful defender becomes the next attacker
- The lowest trump attacks first
- Shedding all your cards to escape being the durak

## The variation's rules

CARDS. 36 cards: suits Clubs (index 0), Diamonds (1), Hearts (2), Spades (3); ranks 6, 7, 8, 9, 10, J=11, Q=12, K=13, A=14. Each card has an id = suit index × 9 + (rank − 6), from 0 to 35. Hands, the discard pile and the set-aside pile are always kept as lists sorted ascending by id, and are always shown and read in that order.

CARD STRENGTH. Card X beats card Y if: (a) X has the same suit as Y and a higher rank; or (b) X is a trump and Y is not.

ROUND 1 (setup, no bout).
Step 1. Build the deck as the ordered list of ids 0 to 35. Shuffle it once with the engine's seeded shuffle. This is the only random operation in the game; no clock or other random source is ever used. Positions 1–8 go to player 1's hand, positions 9–16 to player 2's hand, and positions 17–36 to the set-aside pile. The set-aside pile stays face down for the whole game and is never drawn from. Each player is told only their own hand. Both players are told that each holds 8 cards.
Step 2. Player 2 names two different suits as the offer. If the answer is missing or illegal, the offer is Hearts and Spades.
Step 3. Player 1 picks one of the two offered suits as trump. If the answer is missing or illegal, trump is the offered suit with the lower suit index.
Step 4. The trump suit is announced. The first attacker is the player holding the lowest-rank trump. If neither player holds a trump, player 2 attacks first. The other player is the defender.

ROUNDS 2 TO 40 (one bout each, played only while both players hold cards).
Step 5 (attack). The attacker plays one card from their hand face up. If the answer is missing or illegal, the attacker plays their lowest-rank card, with ties broken by lower suit index.
Step 6 (defence 1). The defender either plays one card from their hand that beats the attack card, or says TAKE. A missing or illegal answer counts as TAKE.
Step 7 (throw-in). The attacker may add one card from their hand whose rank equals the rank of any card now on the table, or say PASS. A throw-in is allowed even if the defender said TAKE; the defender then takes it too. The attacker may not throw in if the defender has not said TAKE and has no cards left in hand. A missing or illegal answer counts as PASS.
Step 8 (defence 2). This step happens only if a card was thrown in and the defender has not said TAKE. The defender either plays one card that beats the thrown-in card, or says TAKE. A missing or illegal answer counts as TAKE.
Step 9 (resolution). If the defender said TAKE at any point, all cards on the table go into the defender's hand, and the same attacker attacks again next bout. Otherwise, all cards on the table go to the discard pile, and the defender becomes the attacker for the next bout.
Step 10 (announcement). Announce all cards played this bout in order, the result, and both players' hand sizes.

END. After a bout's resolution, if exactly one player has 0 cards, that player wins. If both have 0 cards, the game is a draw. If both players still hold cards after round 40, the player with fewer cards wins; equal counts are a draw.

DETERMINISM. Given the same seed, the game must produce identical logs. Every fallback is the fixed rule stated above, computed from the sorted lists.

Objective: The first player whose hand reaches 0 cards after a bout wins. If both reach 0 at the same resolution, the game is a draw. If round 40 ends with both players holding cards, the player with fewer cards wins; equal counts are a draw.

Expected effect: Without drawing, the game becomes a card-counting duel. Each player knows their own 8 cards, and play gradually reveals which of the 28 unseen cards are in the opponent's hand rather than set aside. A failed defence or a declined throw-in leaks information about the opponent's hand. Cut-and-choose makes player 2 offer two suits it can live with, while player 1 reads its own hand to pick between them. Taking on purpose to collect a rank, saving trumps for the last bouts, and throwing in to strand the defender are all rewarded. Simple policies lose: always TAKE builds a huge hand, always attacking with the lowest card is read and punished, and never throwing in gives up tempo. With one seeded shuffle and fallbacks computed from ordered lists, two runs with the same seed should replay identically.

## Complexity (the designer's count, against the limits)

- steps_per_round: 16 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 18 (limit 20)
- hidden_elements: 3 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 40 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
