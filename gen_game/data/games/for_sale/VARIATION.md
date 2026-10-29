# Variation: For Sale: Sealed Bids

Three players buy properties in 8 sealed-bid rounds with secret coin totals, then sell them in 8 blind rounds for cheques. Most money wins.

Players: 3 to 3, best with 3

## Review of the original

For Sale is a two-phase money game for 3 to 6 players. In the first phase players buy property cards (1-30) through open ascending auctions, where passing early gets a cheap, low property at half your bid. In the second phase they sell those properties in simultaneous blind rounds for currency cards, and the most money (currency plus leftover coins) wins.

- **non_degenerate**: good. No simple policy dominates. Always passing first keeps all 18k coins but collects the worst properties, and those win the worst cheques. Always raising spends the coins on a few top properties. Always playing your highest property in phase 2 wastes it on weak cheque sets. One flaw: in the auction the starting player and the clockwise order give positional edges, because a later bidder sees more before committing.
- **skill_sensitive**: good. Card order is random but shared by everyone. Skill decides the outcome: valuing each property relative to the others on offer, knowing when to drop out, and timing which property to sell into which cheque set. Experienced players beat novices reliably.
- **headroom**: good. There is no solved line. Bidding depends on rivals' remaining coins and the spread of the offer, and selling depends on predicting rivals' plays. A weak player can still collect cheques by bidding cheaply.
- **reasoning_dependent**: weak. Little is hidden. Bids are public, so every coin total is known, and every property won is public. Phase 2 is therefore close to perfect information plus a simultaneous guess. Inference about how much rivals can still spend is trivial.
- **verifiable**: good. The final score is currency plus coins, compared arithmetically, with a coin tiebreak. No judging is needed.
- **fits_platform**: weak. The game is text-only and arithmetic. However, the open clockwise auction is an unbounded loop of raise-or-pass turns. The engine cannot express a loop of indefinite length inside one round, and the number of steps would exceed the limits. The variable player count also multiplies the ranking steps.

## Problems

- The open ascending auction is an indefinite loop of sequential raise/pass turns. The engine cannot express it inside one round within 20 steps.
- Seat order matters in the auction: the starting player and the clockwise position change what each bidder knows when deciding.
- Too little is hidden. All bids, and therefore all coin totals, are public, so there is almost nothing to infer about rivals' spending power.
- With 3 to 6 players, ranking bids and properties takes many steps, and the deck and coin rules change with player count. That pushes the game past the complexity limits.
- Two separate deck shuffles plus per-round reveals risk more than one random draw in a single round.

## Changes

- Replace the open auction with one simultaneous sealed bid per round. The highest bidder takes the highest property and pays the full bid. The second and third bidders take the middle and lowest properties and each pay half their bid, rounded down. (fixes: The open ascending auction is an indefinite loop of sequential raise/pass turns. The engine cannot express it inside one round within 20 steps.): This keeps the original's tension: a winner pays full, a loser pays half and takes a worse card. It fits in a single poll step.
- Break bid ties by a priority order that rotates each round (player 1 first in round 1, player 2 in round 2, player 3 in round 3, and so on). (fixes: Seat order matters in the auction: the starting player and the clockwise position change what each bidder knows when deciding.): Simultaneous bids plus a rotating tiebreak remove any fixed positional advantage.
- Keep bid amounts and coin totals private. Only who took which property is announced. (fixes: Too little is hidden. All bids, and therefore all coin totals, are public, so there is almost nothing to infer about rivals' spending power.): Players must infer rivals' remaining coins from the order in which properties were won. Bidding high against a rival who is secretly broke wastes money, so reading spending power becomes the core inference.
- Fix the player count at 3, using the original 3-player setup: 18 coins each, 24 properties and 24 cheques in play, 8 auction rounds and 8 selling rounds. (fixes: With 3 to 6 players, ranking bids and properties takes many steps, and the deck and coin rules change with player count. That pushes the game past the complexity limits.): Three ranks keep the ranking and award steps within limits. Three players also avoid the two-player difference trap, because one rival's loss is not automatically your gain.
- Shuffle the property deck only at the start of round 1 and the cheque deck only at the start of round 9. Every other reveal takes the top cards in order. (fixes: Two separate deck shuffles plus per-round reveals risk more than one random draw in a single round.): This keeps every round at no more than one random draw.

## Kept from the original

- The two-phase structure: buy properties with coins, then sell properties for cheques.
- The original 3-player numbers: property cards 1-30, cheques 0 and 2-15 (two of each), 18 coins each, 6 cards of each deck left out.
- The auction pricing: the top buyer pays full and takes the best card, while the others pay half rounded down and take worse cards.
- The simultaneous blind selling phase, where the highest property takes the highest cheque.
- Final score is cheques plus leftover coins, with the coin tiebreak.

## The variation's rules

SETUP. There are exactly 3 players, numbered 1, 2 and 3.
- Each player starts with 18 coins. A player's coin total is private: only that player sees it.
- The property deck holds the cards 1 to 30, one of each.
- The cheque deck holds the values 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14 and 15, two of each, for 30 cheques.
- Each player has a cheque total starting at 0. It is private.
- Each player has a property hand starting empty. Hands are public.

The game lasts 16 rounds. Rounds 1-8 are BUYING rounds and rounds 9-16 are SELLING rounds.

BUYING ROUND (rounds 1-8):
1. In round 1 only, shuffle the property deck. Only the top 24 cards will ever be used; the bottom 6 stay unseen.
2. Reveal the next 3 cards from the top of the property deck. Call them LOW, MIDDLE and HIGH by value.
3. All players at the same moment secretly submit a bid: a whole number from 0 up to their current coins.
4. Rank the bids from highest to lowest. Break ties by this round's priority order. In round r, priority goes first to player ((r-1) mod 3)+1, then to the next player number, wrapping 3 to 1.
5. The first-ranked player takes HIGH and pays their full bid.
6. The second-ranked player takes MIDDLE and pays half their bid, rounded down.
7. The third-ranked player takes LOW and pays half their bid, rounded down.
8. Payments go to the bank and come out of each player's private coins.
9. Announce publicly which player took LOW, MIDDLE and HIGH. Bid amounts and coin totals are NOT announced.
After round 8 each player holds exactly 8 properties.

SELLING ROUND (rounds 9-16):
1. In round 9 only, shuffle the cheque deck. Only the top 24 cheques will ever be used.
2. Reveal the next 3 cheques from the top of the cheque deck.
3. All players at the same moment secretly choose one property from their own hand.
4. Reveal the chosen properties. Properties are all different, so there are no ties.
5. The player who played the highest property adds the highest cheque to their cheque total. The middle property gets the middle cheque, and the lowest property gets the lowest cheque.
6. Played properties are discarded from hands.
7. Announce publicly who played which property and who took which cheque. Running cheque totals stay private.

END. After round 16, each player's final money is their cheque total plus their remaining coins. These are revealed.

Objective: The player with the most final money (cheques plus remaining coins) wins. If two or more tie for most, the tied player with more remaining coins wins. If they are still tied, the game is a draw among them.

Expected effect: Sealed bids with private coin totals turn the buy phase into inference. Players read how much a rival has left from the properties they won: taking HIGH several times probably drained them, while taking LOW repeatedly suggests a hoard. They then bid just above what the rivals can afford. Overbidding is punished twice, because second place still pays half. Simple policies all lose to reasoned play. Always bidding 0 keeps 18 coins but takes the worst properties and therefore the worst cheques. Bidding everything spends the coins on one card. Always selling your highest property wastes it on weak cheque sets. The selling phase stays a mind-game of timing your big properties against rivals' known hands. Talk is left out. Bids are never revealed, so promises about bidding can never be checked, and the messages would add steps without giving players anything to verify or reason about.

## Complexity (the designer's count, against the limits)

- steps_per_round: 18 (limit 20)
- choice_steps_per_round: 2 (limit 4)
- attributes: 12 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 16 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
