# Variation: Offered-Trump Duel Durak

A two-player Durak over 4 deals. Each deal, the first attacker offers two suits as possible trumps and the defender picks one. Players then attack with 1 to 3 cards of one rank, which must be beaten or taken. Cards left in hand become penalty points, and the lower total wins.

Players: 2 to 2, best with 2

## Review of the original

Durak is a shedding card game with a 36-card deck. Players attack with cards that the defender must beat, using a higher card of the same suit or a trump; a defender who cannot beat an attack takes the cards, and the last player left holding cards is the loser. The reviewed version, Duel Durak, cut it to two players, 6-card hands with no draw pile, a randomly chosen trump, one attack card plus one rank-matching add per bout, and penalty points over 4 deals.

- **non_degenerate**: good. No simple policy is safe. Always TAKE keeps picking up cards and scores large penalties. Always leading the lowest or highest card can be exploited by a defender who keeps trumps back. Seats are balanced because the first attacker alternates by deal. Choices visibly change who empties their hand first.
- **skill_sensitive**: bad. With 6 cards, no draw pile and a random trump, the deal is often decided by the holding alone. A hand has no trump with probability C(27,6)/C(36,6), about 0.152. In roughly 40-50% of deals one hand must take whenever the right suit is led, whatever its owner does. Over only 4 deals, chance decides an estimated 60% or more of results.
- **headroom**: weak. There is real skill: reading voids from TAKEs, saving trumps and timing the add. When both sides play sensibly, though, the deal result is mostly fixed by trump count and suit shape, so improving one's play buys little.
- **reasoning_dependent**: weak. Hands are hidden and 24 cards are unseen, so inference exists. But there is no event before play that signals anything, and the trump is random. What a player infers rarely changes what they can do with a bad hand.
- **verifiable**: good. Penalties are pure arithmetic on hand sizes at the end of each deal. The lower total wins, and equal totals are a draw. No judge is needed.
- **fits_platform**: bad. It is text-only, turn-based and fits within 40 rounds, 13 steps, 4 choice steps, 15 attributes and 3 hidden elements. However, the first round of each deal needs two independent random draws, the shuffle and a separate random trump, against a limit of 1 per round.

## Problems

- P1 (platform): Each deal needs two random draws in one round, the shuffle and an independent random trump suit, against a limit of 1.
- P2 (luck): A random trump with 6-card hands means a trumpless or void hand often cannot avoid taking. The holding decides most deals.
- P3 (luck vs memory): The suggested duplicate fix, replaying deals with the hands swapped, does not work between the same two players. In the replay each player has already seen one hand and now holds the other, so both know both hands exactly. Hidden information vanishes, and the replay is played under different information than the original, so it is not a fair comparison.
- P4 (reasoning): Nothing before play gives a signal to read. Inference is limited to occasional voids shown by TAKEs.
- P5 (headroom): Only one attack card plus one add per bout, from small hands, leaves few meaningful decisions per deal, so strong players cannot pull far ahead of merely sensible ones.
- P6 (sample size): Six cards over 4 deals gives too few decisions for skill to show.

## Changes

- Trump is no longer random. It is chosen by cut-and-choose. At the start of each deal, the first attacker, after seeing their hand, offers two different suits. The defender, after seeing their hand, picks one of them as trump. The deal's only random draw is the shuffle. (fixes: P1 (platform): Each deal needs two random draws in one round, the shuffle and an independent random trump suit, against a limit of 1.): This leaves one random draw per round. It also stops the shuffle from deciding the trump: each player shapes the trump with their own hand, so a trumpless disaster becomes rare.
- Trump selection by offer and choice replaces random trump, and the offer and choice are announced publicly. (fixes: P2 (luck): A random trump with 6-card hands means a trumpless or void hand often cannot avoid taking. The holding decides most deals.): The offer reveals which suits the proposer is strong in, and the choice reveals which of the two the chooser preferred. Each player must weigh offering their own strong suits, which helps them but tells the opponent their shape, against offering a decoy. The chooser must read the offer. Hand strength now depends partly on a reasoned decision rather than on the shuffle.
- The duplicate replay is not adopted. Every deal is a fresh shuffle, and the attacker role alternates by deal. (fixes: P3 (luck vs memory): The suggested duplicate fix, replaying deals with the hands swapped, does not work between the same two players. In the replay each player has already seen one hand and now holds the other, so both know both hands exactly. Hidden information vanishes, and the replay is played under different information than the original, so it is not a fair comparison.): A replay between the same two players leaks both hands. Luck is reduced instead through the trump choice, bigger hands and multi-card attacks, while all hands stay genuinely hidden.
- The public offer and choice act as signals, combined with the public record of every attack, defence and TAKE. (fixes: P4 (reasoning): Nothing before play gives a signal to read. Inference is limited to occasional voids shown by TAKEs.): Players get a structured signal to reason from before play, and the record lets them count cards and infer the opponent's suit lengths.
- The attack may be 1, 2 or 3 cards of the same rank, which the defender must beat one by one or else take all. This replaces the separate ADD and second-defence steps, freeing two choice steps for the trump offer and choice. (fixes: P5 (headroom): Only one attack card plus one add per bout, from small hands, leaves few meaningful decisions per deal, so strong players cannot pull far ahead of merely sensible ones.): Durak's rank-matching pressure is kept, and attackers gain a richer decision: lead a pair to overload the defender, or hold it back. The choice-step budget stays at 4.
- Hands are 8 cards instead of 6, with 20 cards set aside, still with a 10-bout cap per deal and 4 deals. (fixes: P6 (sample size): Six cards over 4 deals gives too few decisions for skill to show.): Larger hands lower the chance of a hopeless holding and add more decisions per deal. Multi-card attacks keep deals inside 10 bouts.

## Kept from the original

- The 36-card deck from 6 to Ace and the Durak beating rule: a higher card of the same suit, or any trump over a non-trump.
- Attacker and defender roles. The defender beats every attack card or takes them. A successful defence discards the cards and the defender becomes the attacker. After a take, the same player attacks again.
- Attacking with cards of matching rank to overload the defender.
- Being left holding cards is what loses (the durak), scored as penalty points.
- Two players, 4 deals, alternating first attacker, and a 10-bout cap per deal.

## The variation's rules

CARDS. There are 36 cards: four suits (Clubs, Diamonds, Hearts, Spades), each with ranks 6, 7, 8, 9, 10, J (11), Q (12), K (13), A (14). Suit order, used only to break ties, is Clubs, Diamonds, Hearts, Spades.

BEATING. Once a trump suit is set, card X beats card Y if (a) X is the same suit as Y and of higher rank, or (b) X is a trump and Y is not. Nothing else beats.

STRUCTURE. The game has 4 deals. Each round is one bout. There are at most 10 bouts per deal and at most 40 rounds in total. Player 1 is the first attacker (the proposer) in deals 1 and 3. Player 2 is the first attacker in deals 2 and 4. The other player is the first defender (the chooser).

STARTING A DEAL (these steps happen only in the first bout of a deal, when the deal's bout counter is 0):
S1. DEAL. Shuffle all 36 cards once. Deal 8 cards face down to each player; only the owner sees their hand. The remaining 20 cards are set aside face down, unseen by both and unused this deal. This shuffle is the only random event.
S2. OFFER. The first attacker names two different suits. If the answer is not two different suits, the offer is Hearts and Spades. The offer is announced to both players.
S3. CHOICE. The first defender picks one of the two offered suits. That suit is the trump for the whole deal and is announced. If the answer is not one of the offered suits, the first suit offered becomes trump.

A BOUT (every round), in order:
1. ATTACK. The attacker places 1, 2 or 3 cards from their hand face up. All of them must be the same rank, and their number may not exceed the number of cards in the defender's hand. An illegal attack (a card not in hand, mixed ranks, or too many cards) is replaced by the attacker's single lowest-ranked card; ties go to the earliest suit in suit order. The attack is announced.
2. DEFENCE. The defender either says TAKE, or names one different card from their hand for each attack card, saying which attack card each one beats. Every pairing must be a legal beat. Any illegal or incomplete defence counts as TAKE.
3. RESOLVE. If the defence succeeded, all attack and defence cards are discarded face up, out of play, and the defender becomes the attacker for the next bout. If the defender took, the attack cards go into the defender's hand and the same player attacks again next bout. All cards played, the result, and both hand sizes are announced. Add 1 to the bout counter.

ENDING A DEAL. After RESOLVE, the deal ends if either player has no cards or the bout counter has reached 10. Penalties:
- If exactly one player has no cards, the other player (the durak) adds the number of cards in their hand to their penalty total.
- If both have no cards, nobody scores.
- If the deal ended at 10 bouts with both holding cards, the player with more cards adds the difference in hand sizes to their penalty total. Equal hands score nothing.

The next deal then starts with its bout counter at 0 and the first attacker set by the schedule above.

ENDING THE GAME. The game ends when deal 4 has ended. If round 40 finishes during a deal, that deal is scored as if it had reached its 10-bout cap.

Objective: When the game ends, the player with the lower total penalty wins. If the two totals are equal, the game is a draw.

Expected effect: Luck of the deal shrinks because the trump is shaped by both players' choices rather than a coin. The proposer cannot simply offer their two strongest suits, because the chooser will pick whichever of those suits suits the chooser better. The chooser must also infer the proposer's shape from the offer, since every offered suit is a suit the proposer may well hold. In play, multi-card same-rank attacks create real tension: whether to spend a pair now, whether to beat cheaply or with a trump, and whether to take rather than burn trumps. The public record of the offer, choice, plays and takes supports card counting and void inference. Thoughtless policies can all lose: always-TAKE accumulates penalties; always-lowest-lead and always-first-suit choices are exploitable; a defender who burns trumps early is overloaded later. There is no talk, because the game is two-player and zero-sum.

## Complexity (the designer's count, against the limits)

- steps_per_round: 16 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 16 (limit 20)
- hidden_elements: 3 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 40 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
