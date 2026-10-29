# Variation: Biblios: Sealed Scriptorium (revised)

Three scribes take turns drawing two cards, secretly keeping one and auctioning the other by sealed bid. Colour majorities score their die worth, which Church cards move in public when won at auction or in secret when kept.

Players: 3 to 3, best with 3

## Review of the original

Biblios is a 2-4 player card game in two phases. In the Gift phase the active player splits drawn cards between a secret keep, a face-down auction pile and face-up cards for opponents. In the Auction phase players bid Gold cards for the auction pile. Church cards shift the VP dice on five colours, and the player with the highest total value in a colour wins that colour's die.

- **non_degenerate**: good. No simple policy dominates. Never bidding leaves a player with only gifted cards and loses majorities. Always overbidding drains Gold and leaves a player unable to compete later. Majority scoring means choices directly move VP.
- **skill_sensitive**: weak. Skill matters in splitting gifts and timing bids. But an 87-card shuffle, random theft when a player cannot pay, and a re-shuffled auction pile give luck a large share.
- **headroom**: good. Card counting, reading opponents' secret keeps and steering dice give long-term room to improve. Weak players still win some colours.
- **reasoning_dependent**: good. Secret keeps and face-down auction cards hide state. Players infer rivals' colour totals and plan Gold across many rounds.
- **verifiable**: good. Scoring is sums and comparisons, with ties broken by card letters.
- **fits_platform**: weak. It is text-friendly with no board. But the 87-card deck, Gold-as-cards payment, overpaying, random theft, open-outcry auction re-runs, two-phase structure and letter tie-breaks exceed the step limits.

## Problems

- The original's deck, payment-by-cards, theft and open-outcry auctions exceed platform complexity, and its many random steps let luck swamp skill.
- The previous variation contradicted itself. Step 4 hid whether the kept card was a Church card, but step 9 announced 'a hidden Church card was used', which reveals both the card type and the user, since only the active player keeps a card.
- The previous variation never said where a won Church card goes after it is used.
- The previous variation called two Church adjustments simultaneous yet ordered, without saying whether the 2-8 limit is checked before or after the first adjustment.
- A hidden Church choice that only some players are asked to make would itself leak information: being asked reveals that the kept card is a Church card.

## Changes

- The original is reduced to a 36-card deck, abstract gold, one sealed bid per round, and the active player's keep-one-of-two choice standing in for the gift split. This is retained from the previous variation. (fixes: The original's deck, payment-by-cards, theft and open-outcry auctions exceed platform complexity, and its many random steps let luck swamp skill.): It keeps the gift-and-auction identity within the step limits, with one shuffle at setup.
- A kept Church card no longer changes worths during play. Its owner records a secret colour and direction in their hidden collection, applied only at scoring. Worths shown during play exclude these secret adjustments. Nothing is announced when a kept Church card is used. (fixes: The previous variation contradicted itself. Step 4 hid whether the kept card was a Church card, but step 9 announced 'a hidden Church card was used', which reveals both the card type and the user, since only the active player keeps a card.): This keeps secrecy without contradiction, and makes reading which colour a rival secretly boosted part of the inference.
- Every round the active player always gives a secret mark (a colour and +1 or -1), whatever they kept. The mark counts only if the kept card was a Church card. (fixes: A hidden Church choice that only some players are asked to make would itself leak information: being asked reveals that the kept card is a Church card.): Being asked never reveals anything, because everyone sees the active player asked every round.
- A won Church card is used at once in public (the winner names a colour and a direction, applied immediately) and is then discarded face-up. It never enters any collection. (fixes: The previous variation never said where a won Church card goes after it is used.): It gives the card a stated destination.
- During play only the public adjustment from a won Church card changes a worth, so at most one public adjustment happens per round. At scoring, the secret marks that count are applied one at a time in round order, starting from the final public worths. Each mark is checked against the limit using the worth as already changed by earlier marks; a mark that would take a worth below 2 or above 8 has no effect. (fixes: The previous variation called two Church adjustments simultaneous yet ordered, without saying whether the 2-8 limit is checked before or after the first adjustment.): This gives an exact, ordered clamping rule. For example, worth 7 with two +1 marks becomes 8, then the second mark has no effect.

## Kept from the original

- The active player splits drawn cards between a secret keep and a card offered to everyone.
- Gold-based auctions for the offered cards, with gold also worth points at the end.
- Five colours whose majority holder scores that colour's die worth.
- Church cards that move die worths up or down, now with a secret version.
- Hidden collections that opponents must infer from what was offered and how players bid.

## The variation's rules

SETUP.
The deck has 36 cards.
- There are 30 colour cards: for each of the five colours (Red, Blue, Green, Yellow, Purple), one card each of values 1, 1, 2, 2, 3 and 4.
- There are 6 Church cards.
Shuffle the deck once. Its order is hidden from everyone.

Each player starts with 8 gold. Each colour has a public die worth, starting at 4. A public worth can never go below 2 or above 8.

Every player has two collections:
- A hidden collection, seen only by its owner. It holds the colour cards and Church cards they kept, and their secret marks.
- A public collection, seen by all. It holds the colour cards they won.
Gold totals and public die worths are public. The worths shown during play never include secret marks.

ROUNDS.
There are 12 rounds. The active player is seat 1, 2, 3, 1, 2, 3 in rounds 1-6, and seat 3, 2, 1, 3, 2, 1 in rounds 7-12. Each round has these steps:

1. Announce the round number, the active player, all public die worths, all gold totals and all public collections.
2. Remove the top two cards of the deck. Show them privately to the active player only, as Card A (the top card) and Card B (the next card).
3. The active player privately chooses Keep A or Keep B.
4. The kept card goes into the active player's hidden collection. Nothing about it is announced. The other card is announced publicly as this round's lot.
5. Talk: every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Messages are not binding.
6. Sealed bid: all three players, including the active player, at the same time bid a whole number of gold from 0 up to the gold they hold.
7. Reveal all bids. If the highest bid is at least 1 and no other player bid the same amount, that player wins the lot and pays their bid to the bank (the gold leaves the game). Otherwise nobody pays and the lot is discarded face-up.
8. A won colour card goes into the winner's public collection.
9. Church and secret mark, answered at the same time:
   (a) The active player always privately names one colour and a direction (+1 or -1). This is recorded secretly in their hidden collection as this round's mark. It counts at scoring only if the card they kept this round is a Church card. Otherwise it is void. This question is asked every round, so being asked reveals nothing.
   (b) If the lot was a Church card and someone won it, the winner publicly names one colour and a direction (+1 or -1).
   If the active player is also the winner, they answer both parts.
10. If part (b) was answered, change that colour's public worth by the named direction. If this would take it below 2 or above 8, it has no effect. The won Church card is then discarded face-up. Secret marks change nothing now.
11. Every player gains 1 gold.
12. If this was round 12, go to scoring. Otherwise begin the next round.

SCORING.
1. Final worths. Start from each colour's public worth. Reveal all hidden collections. Take every mark that counts (made in a round where that player kept a Church card) and apply them one at a time in round order, earliest round first. Each mark changes its colour's worth by 1 in its direction, checked against the worth as already changed by earlier marks. A mark that would take a worth below 2 or above 8 has no effect.
2. Majorities. For each colour, add up the values of each player's cards of that colour, hidden and public together.
   - If one player has the strictly highest total and it is at least 1, they score VP equal to that colour's final worth.
   - If two or more players tie for the highest total (at least 1), each of them scores half the final worth, rounded down.
   - If no one has a card of that colour, nobody scores it.
   Church cards have no value at scoring.
3. Gold. Each player scores 1 VP for every full 5 gold they hold.

Objective: The player with the most VP after scoring wins. If two or more players tie for the most VP, the game is a draw.

Expected effect: The fixes make the rules consistent without losing the hidden layer. Since nobody knows whether a kept card was a Church card, and the mark is asked every round, players must infer secret worth shifts from behaviour: an unusually high bid for a colour, or talk pushing a colour. Public Church cards become contested lots because they move worths at once. Each player is active four times and sees two cards then; 12 cards are never seen, so colour totals must be estimated. Talk earns its place because all three compete for the same majorities and only one can win. A player might claim to be dropping a colour so rivals underbid, or urge two players to gang up on the leader. A player who simply believes such claims overpays or concedes a colour the speaker secretly holds, and loses. Simple policies all lose. Always bidding 0 leaves a player with four kept cards against rivals winning lots for 1 gold. Always bidding everything burns gold and gold VP early and leaves the player unable to contest the late lots. Always keeping Card A ignores the information the choice offers.

## Complexity (the designer's count, against the limits)

- steps_per_round: 12 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 18 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 12 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
