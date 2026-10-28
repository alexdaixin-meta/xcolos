# Variation: Petite Quadrille III

A four-player, 8-hand miniature of Quadrille played with a 20-card pack. Each hand begins with an auction round, followed by 4 tricks. Four cards lie unseen in a talon. The Taker names trump and calls a King whose holder is a secret partner, or goes solo. Spadille, Manille and Baste are the top trumps.

Players: 4 to 4, best with 4

## Review of the original

Quadrille is an 18th-century four-player trick-taking game with a 40-card pack and three permanent top trumps: Spadille, Manille and Baste. An auction decides the Taker, who names trump and either calls a King, whose holder becomes a concealed partner, or plays solo against three; the side must take the majority of the ten tricks.

- **non_degenerate**: good. In the reviewed variation, Petite Quadrille II, no simple policy is safe. Always-pass makes a player a perpetual defender who only scores when others fail. Always-bid-5 fails most contracts at the highest stake (v=3). Always-Assist never takes the high solo payoffs. Priority rotates evenly, two hands per seat. With four players and the highest total winning, one rival's loss is not automatically your gain, so the two-player difference trap does not apply.
- **skill_sensitive**: good. Bidding to the strength of a 5-card hand, choosing trump and partner, following suit, and counting the 20 cards all reward skill. Over 8 hands, deal luck is diluted but not removed.
- **headroom**: good. Inferring the partner from play, managing the top trumps, and judging when solo pays leave room to improve. A weak player still scores as a defender when Takers overreach.
- **reasoning_dependent**: good. Hands and partner identity are hidden. Players must infer holdings from bids and the cards played, and plan five tricks ahead. With all 20 cards dealt, perfect counting is possible late in a hand, so the hidden information thins out quickly.
- **verifiable**: good. Trick winners, contracts and scores are arithmetic on card codes and counters. No judge is needed.
- **fits_platform**: bad. Position-1 rounds had six choice steps (bid, declare, lead and three follows) against a limit of 4. Rule 12 said the trump suit was both unrevealed and announced, which makes the follow-suit offers unusable.

## Problems

- Choice steps exceed the limit: the auction and declaration share a round with a full trick, giving 6 choice steps where at most 4 are allowed.
- Rule 12 contradicts itself: trump is said to be both hidden and announced, so defenders cannot know which cards are trumps and following suit becomes unplayable.
- Moving the auction into its own round with 5 tricks per hand would allow only 4 hands in 40 rounds (6 rounds each). That gives one priority per seat and much more deal luck.
- With all 20 cards dealt, the hidden state collapses fast: by trick 3 a careful counter knows every hand, so late-hand inference is thin.
- The partner is chosen by seat number, which loses the original's characteristic called King. It also lets the Taker pick a partner without any uncertainty about whether that partner is strong.

## Changes

- Each hand is 5 rounds. Round 1 is the auction only: Bid, then Declare, so 2 choice steps. Rounds 2–5 are one trick each: Lead plus 3 Follows, so 4 choice steps. (fixes: Choice steps exceed the limit: the auction and declaration share a round with a full trick, giving 6 choice steps where at most 4 are allowed.): This keeps every round at 4 choice steps or fewer.
- Deal 4 cards to each player and leave 4 cards face down as a hidden talon that nobody sees. A hand therefore has 4 tricks, and 8 hands fill exactly 40 rounds. (fixes: Moving the auction into its own round with 5 tricks per hand would allow only 4 hands in 40 rounds (6 rounds each). That gives one priority per seat and much more deal luck.): This keeps 8 hands, so each seat has priority twice and luck is diluted. The talon keeps uncertainty alive to the last trick.
- The talon of 4 unseen cards also means no player can ever fully count the hands. (fixes: With all 20 cards dealt, the hidden state collapses fast: by trick 3 a careful counter knows every hand, so late-hand inference is thin.): Players must keep reasoning about where the top trumps and the called King are.
- There is a single unambiguous announcement rule. The trump suit and the call (a named King, or 'Solo') are announced to everyone. Only who holds the called King stays secret until the end of the hand. (fixes: Rule 12 contradicts itself: trump is said to be both hidden and announced, so defenders cannot know which cards are trumps and following suit becomes unplayable.): This removes the contradiction. Every player knows which cards are trumps.
- The Taker calls a King instead of a seat. Its holder becomes the concealed partner. If the Taker holds that King, or it lies in the talon, the Taker plays alone at partnership stakes. (fixes: The partner is chosen by seat number, which loses the original's characteristic called King. It also lets the Taker pick a partner without any uncertainty about whether that partner is strong.): This restores the original's call mechanic. The Taker gets real uncertainty about the partner and the defenders get a real inference task.
- Trick power is computed by a stated formula on the card code and the trump suit, not a per-card table. (fixes: Choice steps exceed the limit: the auction and declaration share a round with a full trick, giving 6 choice steps where at most 4 are allowed.): The engine has no lookup operation. A single calculation per card keeps the step count low.

## Kept from the original

- Four players, an auction for the role of Taker, and the Taker naming trump.
- The three permanent top trumps: Spadille (Ace of Spades) highest, Manille (the Two of trump), and Baste (Ace of Clubs).
- Calling a King whose holder becomes a concealed partner, or playing solo against three.
- Must follow suit, with trumping optional when you cannot follow.
- Contracts are a majority of tricks for the Taker's side, solo pays double, and codille rewards the defender who beats a failed Taker.
- Settlement by counters, a fresh deal every hand, and sides that change every hand.

## The variation's rules

CARDS
1. The pack has 20 cards. Each card's code is 10 × suit + rank.
   - Suits: Spades 1, Clubs 2, Hearts 3, Diamonds 4.
   - Ranks: Ace 1, Two 2, Jack 3, Queen 4, King 5.
   - Cards are shown as '<code> <Rank> of <Suit>', for example '35 King of Hearts'.
   - Code 11 (Ace of Spades) is Spadille. Code 21 (Ace of Clubs) is Baste. Both are always trumps.
2. Plain power (used only when a card is not a trump): King 5, Queen 4, Jack 3, Ace of Hearts or Diamonds 2, any Two 1. Codes 11 and 21 have plain power 0.

STRUCTURE
3. The game has 40 rounds, in 8 hands of 5 rounds. Hand h covers rounds 5h−4 to 5h. A round's position p (1 to 5) is its place in its hand.
4. Position 1 is the auction round, with no trick. Positions 2, 3, 4 and 5 each contain exactly one trick.
5. The priority seat of hand h is ((h − 1) mod 4) + 1. That is seats 1, 2, 3, 4, 1, 2, 3, 4, so each seat has priority twice.
6. Turn order always runs 1→2→3→4→1.
7. Whenever a player is asked to choose, they are first shown their current hand, the trump suit (once declared) and the call (once declared).

AUCTION ROUND (position 1)
8. Reset. Every player's hand_tricks becomes 0 and is_partner becomes false. The leader becomes the priority seat.
9. Deal. Shuffle the 20 cards. Deal 4 to each player privately and put the remaining 4 face down in the talon.
   - This is the round's only random draw.
   - Each player sees only their own 4 cards. Nobody ever sees the talon.
10. Bid. All four choose at the same moment, each picking one of: Pass, Assist, 3, 4.
   - Pass means no interest.
   - Assist signals willingness to be called. It does not compete for Taker.
   - 3 or 4 is an offer to be Taker with a contract of that many of the hand's 4 tricks for the Taker's side.
11. Resolve. Every bid is announced.
   - The highest numeric bid wins.
   - Between equal numeric bids, the winner is the first such seat in turn order starting from the priority seat.
   - If nobody bid a number, the priority seat becomes Taker with contract 3.
   - The Taker and the contract are announced.
12. Declare. The Taker alone chooses one of exactly 20 options:
   - a trump suit (Spades, Clubs, Hearts or Diamonds), combined with
   - either a called King (15 King of Spades, 25 King of Clubs, 35 King of Hearts, 45 King of Diamonds) or 'Solo'.
   - Options are labelled like 'Hearts, call 15 King of Spades' or 'Diamonds, Solo'.
13. Announcement. The trump suit t and the call (the named King, or 'Solo') are announced publicly to everyone. If a King was called:
   - If another player holds it, that player gets is_partner = true and is told privately 'You hold the called King: you are the Taker's partner.'
   - If the Taker holds it, or it is in the talon, the Taker plays alone but is NOT solo, and nobody is told this.
   - No one except the partner (and the Taker, if they hold the King) learns who the partner is until the end of the hand.

CARD STRENGTH (computed from code c and trump t, no table)
14. Effective suit: t if c is 11 or 21; otherwise floor(c / 10).
15. Trump power, for cards whose effective suit is t:
   - c = 11 (Spadille): 20.
   - c = 10t + 2 (Manille, the Two of trump): 19.
   - c = 21 (Baste): 18.
   - c = 10t + 1 when t is 3 or 4 (Ace of a red trump): 17.
   - Otherwise 11 + plain power, so King 16, Queen 15, Jack 14.
   - Every card whose effective suit is not t has trump power 0.

TRICK ROUNDS (positions 2 to 5)
16. Lead. The leader plays any card from their hand. It is removed at once. The led suit L is its effective suit.
17. Follow. The other three play one card each, in turn order after the leader. Each follower's offer is built from their current hand:
   - If they hold any card of effective suit L, the offer is exactly those cards.
   - Otherwise the offer is their whole hand, so they may trump or discard.
   - The played card is removed at once.
18. Winner. A card's trick power is:
   - its trump power, if above 0;
   - otherwise its plain power, if its effective suit is L;
   - otherwise 0.
   The highest trick power wins. Ties cannot occur among cards that can win.
19. The winner gains 1 hand_tricks and 1 tricks_won and leads the next trick. The four cards, who played each, and the winner are announced.

END OF HAND (after the trick at position 5)
20. Count.
   - The side's tricks are the Taker's hand_tricks, plus the partner's if a partner exists.
   - The contract is made if the side's tricks are at least the contract.
   - v = contract − 2, so 1 or 2.
21. Score.
   - With a partner, made: Taker +v, partner +v, each of the two defenders −v.
   - With a partner, failed: Taker −v, partner −v, each of the two defenders +v.
   - Alone by call (the called King was in the Taker's hand or the talon), made: Taker +v, each of the three defenders −v.
   - Alone by call, failed: Taker −v, each of the three defenders +v.
   - Solo, made: Taker +2v, each of the three defenders −v.
   - Solo, failed: Taker −2v, each of the three defenders +v.
22. Codille. If the contract failed and exactly one defender has more hand_tricks than the side's tricks, that defender scores an extra +1.
23. Reveal. The partner's seat (or 'alone' or 'solo'), the talon, each player's hand_tricks, the side's tricks and every score change are announced.

END OF GAME
24. After round 40 the game ends. Each player's standing is 100 × score + tricks_won.

There is no talk phase. The bid (including Assist) and the card play are the only signals.

Objective: After 40 rounds, the player with the highest score wins. If scores tie, the tied player with the most tricks_won wins (equivalently, the highest 100 × score + tricks_won). If that also ties, those players draw.

Expected effect: Every round now fits the 4-choice limit. Public trump removes the contradiction and makes following suit well defined. The hidden talon and the concealed King-holder create sustained inference:
- Defenders must read who the partner is, or whether the King sits in the talon.
- The Taker must judge whether the call will find a strong partner, or go solo for double stakes.
- Over 8 hands, bidding discipline beats overbidding and passivity.
- Codille punishes reckless Takers.
Talk stays out because sides are hidden and adversarial: open messages would be unverifiable partnership claims, and the bid already carries the Assist signal.

## Complexity (the designer's count, against the limits)

- steps_per_round: 12 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 18 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 40 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
