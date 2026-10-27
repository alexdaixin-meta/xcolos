# Variation: No Thanks! Two Laps

Players take or pay on face-up cards one lap at a time. A card keeps circling with its growing pot until someone takes it. If it survives two full laps it is burned, and its pot carries over to the next card. Lowest score wins.

Players: 3 to 4, best with 4

## Review of the original

No Thanks! is a 3-5 player push-your-luck card game. A face-up card (3-35) circles the table, and each player either pays a chip onto it or takes it with all the chips on it. Runs of consecutive cards score only their lowest card, chips subtract one point each, and the lowest score wins.

- **non_degenerate**: bad. In the reviewed One Lap variation, a card that every player passed fell to the starter together with N chips. That made PAY strictly better than TAKE for the starter on every card that does not extend one of their runs. Middle and last seats PAY unless the card connects a run. 'Always PAY' was practically indistinguishable from good play. The original game itself is fine: the card stays in the middle and the pot keeps growing.
- **skill_sensitive**: bad. Under mutual good play in the One Lap variation, nearly every card went to whoever was starter when it was flipped. A 6-card random sum has a standard deviation of about 23 points, which swamps the few points earned by grabbing run-connecting cards. About 80% or more of the result was decided by the deal.
- **headroom**: weak. Chips stayed near 11 for everyone, so there was nothing to plan about chip scarcity, pot growth or forcing an opponent. A weak player could still score, but a strong player had almost no edge to develop.
- **reasoning_dependent**: weak. Chip counts were private but never mattered, because nobody ran low. The 9 removed cards were hidden, but there was little to infer from that. The original's inference (who is short of chips, who wants this card for a run, how long will the card keep circling) was lost.
- **verifiable**: good. The score is the sum of the lowest card of each run minus chips, and the winner is the lowest score. This is pure arithmetic on tracked numbers.
- **fits_platform**: good. It is turn-based, text-only, has no board, uses at most 4 sequential choices per round and runs for 24 rounds. The problems are in balance, not in fit.

## Problems

- P1: The forced starter-take rule makes PAY dominant for the starter and near-dominant for everyone, so 'always PAY' is about as good as good play.
- P2: Chips never become scarce (each player's net chip flow is about 0 per cycle), so the original game's central tension of a draining hand and a growing pot is gone.
- P3: Under good play each player's cards are just the cards flipped on their start rounds, so the shuffle decides about 80% of results (lottery trap).
- P4: Private chip counts and public history give nothing worth inferring, because nobody is ever forced to take.
- P5: Restoring the original 'card stays until taken' rule could run past the 40-round limit unless the game length is bounded.

## Changes

- If every player pays during a round, nobody is forced to take. The card stays in the middle with its pot, and the next round offers it again starting from the same player. This is the original game's continuous circling, cut into laps of at most N offers. (fixes: P1: The forced starter-take rule makes PAY dominant for the starter and near-dominant for everyone, so 'always PAY' is about as good as good play.): Removes the starter's guaranteed profit, so passing a card along is no longer free. The pot grows lap after lap, and every player must judge when the pot is worth the card.
- After a take, the next card is first offered to the taker, as in the original game. (fixes: P3: Under good play each player's cards are just the cards flipped on their start rounds, so the shuffle decides about 80% of results (lottery trap).): Taking now costs tempo: the taker faces a fresh card with an empty pot. Who sees which card first then depends on players' own timing, not on a fixed rotation.
- Burn rule: a card that every player passes in two consecutive rounds is removed from the game. Its pot stays in the middle and becomes the starting pot of the next card. The next card is first offered to the player clockwise of the player who started the burned card's rounds. (fixes: P5: Restoring the original 'card stays until taken' rule could run past the 40-round limit unless the game length is bounded.): Bounds every card to at most 2 rounds. Keeping the pot means chips leave players' hands at N per lap and pile up into jackpots, so passing costs real chips and players can run dry.
- The deck shrinks to 20 cards (13 removed unseen). Every player starts with 11 chips. The game ends when the 20th card has been taken or burned, which takes at most 40 rounds. (fixes: P2: Chips never become scarce (each player's net chip flow is about 0 per cycle), so the original game's central tension of a draining hand and a growing pot is gone.): Keeps the game inside the round limit. With 11 chips and up to 8 chips drained per burned card in a 4-player game, chips become genuinely scarce.
- A player with 0 chips must take. Chip counts stay private, but every action is announced, so others can reconstruct a player's chips from the public history. (fixes: P4: Private chip counts and public history give nothing worth inferring, because nobody is ever forced to take.): Tracking who is nearly broke now matters. Players can pass a high card along to force it onto a player at 0, or avoid feeding a jackpot to someone who needs it.
- The game is limited to 3-4 players. (fixes: P5: Restoring the original 'card stays until taken' rule could run past the 40-round limit unless the game length is bounded.): One lap of offers must fit within 4 choice steps per round.

## Kept from the original

- Take the card and its pot, or pay one chip and pass it on.
- Cards 3-35 with some removed unseen, so the deck has gaps.
- Runs score only their lowest card.
- Chips subtract from the score at one point each.
- The lowest score wins.
- Hidden chip counts.
- The taker starts the next card.
- The pot keeps growing while a card circles.

## The variation's rules

SETUP:
- Take cards numbered 3 to 35 (33 cards), shuffle them, and remove 13 face-down without anyone seeing them. The removed cards are out of the game. The remaining 20 cards form the deck.
- Players are numbered 1 to N clockwise (N = 3 or 4).
- Each player receives 11 chips. A player's chip count is private: only that player is told it.
- Every action (pay, take, chips gained, burn) is announced publicly.
- Each player has a face-up tableau, which starts empty, and a card-points total, which starts at 0.
- The game keeps three public values: the current card (none at start), the pot (0 at start) and the lap count of the current card (0).
- The lead player for the first card is player 1.

EACH ROUND:
1. If there is no current card, reveal the top deck card. It becomes the current card, its lap count is set to 0, and the pot is unchanged: it may hold chips carried over from a burned card.
2. The current card is offered once around the table. Offers start with the lead player and go clockwise, and stop when someone takes it or every player has been offered it once this round.
3. When offered the card, a player chooses PAY or TAKE. A player with 0 chips must choose TAKE.
   - PAY: the player puts 1 chip from their hand into the pot, and the card is offered to the next player.
   - TAKE: the player adds all chips in the pot to their hand, places the card in their tableau, and the pot becomes 0. The card is no longer current. The taker becomes the lead player for the next card, and the round ends at once.
4. Card-point update when a player takes card c: their card-points total changes by (c if they do not hold c-1, else 0) minus (c+1 if they hold c+1, else 0). Card points therefore always equal the sum of the lowest card of each run of consecutive numbers in the tableau.
5. If every player chose PAY this round, the card's lap count increases by 1.
   - If the lap count is now 1, the card stays current with its pot, and the next round offers it again starting from the same lead player.
   - If the lap count is now 2, the card is burned (removed from the game). The pot stays in the middle for the next card, and the lead player for the next card becomes the player clockwise of the current lead player.
6. Announce what happened: who paid, who took what with how many chips, or that the card was burned, plus the pot size and every tableau.
7. If the deck is empty and there is no current card, the game ends. Any chips left in the pot are out of the game.

There is no discussion phase.

END: Each player's final score is card points minus chips in hand.

Objective: The player with the lowest final score (card points minus remaining chips) wins. If several players tie for lowest, the one among them with more remaining chips wins. If they are still tied, the game is a draw among them.

Expected effect: Passing a card now costs a chip per lap with no guaranteed refund, so pots grow and chips drain. Players must price each card against its pot, their runs and their remaining chips.

Simple policies lose:
- Always PAY runs out of chips within about 11 offers. From then on it must take whatever reaches it first, often a high card on a fresh, empty pot.
- Always TAKE collects many high cards for 0-3 chips.
- Random play overpays and takes high cards cheaply priced.
- A fixed pot-threshold rule loses to players who track opponents' chips, leave high cards for broke players, and time takes of run-connecting cards.

Who gets which card now depends on take timing, so the shuffle sets the problem but does not decide the winner.

Talk was left out. The choices are sequential and individual, and promises like 'let's dump this on player 3' cannot bind. A discussion step would mostly let players gang up on whoever is leading, rather than adding reasoning.

## Complexity (the designer's count, against the limits)

- steps_per_round: 14 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 11 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 40 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
