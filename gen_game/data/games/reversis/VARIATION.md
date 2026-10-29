# Variation: Quick Reversis

Four players play 4 hands of 6 tricks each with a 24-card deck. In each trick the leader plays first, then the other three play at the same moment. Players avoid penalty points, especially the 5-point Quinola, unless one player takes every trick of a hand (a reversis). The lowest total after 4 hands wins.

Players: 4 to 4, best with 4

## Review of the original

Reversis is an 18th-century 4-player trick-taking game without trumps, and the aim is to avoid winning points. Players must follow suit, and the highest card of the led suit takes the trick. Aces, Kings, Queens and Jacks carry penalty points, and the Jack of Hearts (Quinola) is special. The fewest points wins, unless one player takes every trick (the reversis), which reverses the aim and wins outright.

- **non_degenerate**: good. Neither 'always play the highest legal card' nor 'always the lowest' is safe. Leading high takes the point cards, and ducking every time leaves you holding high cards late in the hand. The reversis threat punishes others' blind dumping. In the tested variation, simple policies lost about 65-85% of games (first@seat1 lost 44 of 60, last@seat2 lost 50 of 60). The one real flaw was seat bias: seat 4 won 21 of 60 games against random seats, against 10 for seat 2.
- **skill_sensitive**: weak. A single 13-trick deal is strongly shaped by the cards you hold: a hand full of high cards in long suits cannot avoid points. Skill shows only over many deals. The original settles one deal with side payments and pools, so luck dominates any single game.
- **headroom**: good. Several skills keep paying off: counting cards, inferring voids from discards, timing when to shed the Quinola and the Aces, and deciding whether to try a reversis or block one. Beginners still score, because the points spread across everyone.
- **reasoning_dependent**: good. Hands are hidden. Players must infer who is void in a suit from failures to follow, and judge which opponent is trying for a reversis. They also plan which card to lead several tricks ahead.
- **verifiable**: good. Trick winners and point totals are pure arithmetic on the cards played.
- **fits_platform**: weak. The original is too long: 13 tricks with 4 sequential plays each is 52 choices per hand. It uses anticlockwise turn order, pools, side payments and later bonus variants. The previous adaptation still had 6 choice steps per round against a limit of 4, because of the passing round and per-player turns.

## Problems

- P1: The built game had 6 choice steps per round, over the limit of 4. Passing and individual follow turns were still separate choice steps.
- P2: Seat imbalance. Seat 4 won 21 of 60 games against random seats and seat 2 only 10. The cause is information from playing later in a trick and an uneven pattern of who leads the first trick.
- P3: Luck of the deal is large in a single long hand. The fix is several short hands with a rotating first leader.
- P4: The original's pools, side payments and bonus variants are not arithmetic the engine needs. They add rules without adding reasoning.
- P5: Too many attributes would be needed to track hand points and trick counts per player for the reversis check.

## Changes

- Each round is exactly one trick with two choice steps. First the leader plays one card. Then the other three players choose their cards at the same moment in a single simultaneous poll. There is no passing round and there are no individual follow turns. (fixes: P1: The built game had 6 choice steps per round, over the limit of 4.): This brings choice steps per round to 2, well under 4.
- Followers commit at the same moment, so no follower sees another follower's card before choosing. Each of the 4 hands begins with a different player leading (player h leads trick 1 of hand h), so every seat leads the opening trick exactly once. (fixes: P2: Seat imbalance.): This removes the last-to-play information edge and evens out opening leads across seats.
- The deck is 24 cards (A K Q J 9 8 in four suits) dealt 6 to each player. Each hand is 6 tricks, and there are 4 hands, so 24 rounds. There is one shuffle-and-deal per hand, in that hand's first round. (fixes: P3: Luck of the deal is large in a single long hand.): Four short hands average out the luck of the deal and keep the game short. There is at most one random draw per round.
- Pools, side payments and bonus variants are dropped. The only scoring is penalty points and the reversis adjustment. The Quinola is kept as the single heaviest card (5 points). (fixes: P4: Pools, side payments and bonus variants add rules without adding reasoning.): This keeps the game's identity while making the winner pure arithmetic.
- The reversis is tracked with one table attribute, the sweeper: the player who has won every trick so far this hand, or none. At the end of a hand, if a sweeper remains, that player subtracts the 44 points they took and each other player adds 15. (fixes: P5: Too many attributes would be needed for the reversis check.): This avoids per-player trick counters and per-hand point totals.

## Kept from the original

- Trick-taking with no trumps: players must follow suit, and the highest card of the led suit wins.
- Avoiding points is the aim, and the lowest total wins.
- Point values A=4, K=3, Q=2, J=1.
- The Jack of Hearts, the Quinola, is the most dangerous card.
- The reversis: taking every trick of a hand turns your penalty into a win-swing against the others.
- The trick winner leads the next trick.

## The variation's rules

SETUP
- Players are seats 1, 2, 3 and 4. Every player's total starts at 0.
- The deck has 24 cards: A, K, Q, J, 9 and 8 in each of Spades, Hearts, Diamonds and Clubs.
- Within a suit the ranking is A (highest), K, Q, J, 9, 8. There are no trumps.

CARD POINTS
- Each Ace counts 4, each King 3, each Queen 2 and each Jack 1. Nines and eights count 0.
- The exception is the Jack of Hearts (the Quinola), which counts 5.
- Each hand contains 44 points in total.

STRUCTURE
- The game has 4 hands of 6 tricks each, so 24 rounds. Each round is one trick.

START OF A HAND (rounds 1, 7, 13 and 19)
- Shuffle the 24 cards and deal 6 face down to each player. Each player sees only their own hand.
- The leader of the first trick of hand h is seat h.
- Set the sweeper to 'none'.

EACH ROUND (ONE TRICK)
1. The leader plays any one card from their hand face up. Its suit is the led suit. Announce it.
2. The other three players each choose one card at the same moment, without seeing each other's choices.
   - A player who holds a card of the led suit must play one.
   - A player who holds none may play any card.
3. All cards are revealed together.
4. The highest card of the led suit wins the trick.
5. Add up the points of the 4 cards played. The trick winner adds them to their total.
6. Played cards leave the game for the rest of the hand.
7. Update the sweeper:
   - On the first trick of a hand, the sweeper becomes the trick winner.
   - On later tricks, if the trick winner is not the sweeper, the sweeper becomes 'none'.
8. The trick winner leads the next trick.
9. Announce every player's total.

END OF A HAND (after tricks 6, 12, 18 and 24)
- If the sweeper is a player (that player took all 6 tricks, a reversis):
  - that player subtracts 44 from their total, so the hand counts 0 for them;
  - each other player adds 15 to their total.

TALK
- There is no table talk.

END OF GAME
- After round 24 the game ends.

Objective: After 4 hands, the player with the lowest total wins. If two or more players tie for the lowest total, the game is a draw.

Expected effect: Simultaneous following removes the edge of playing last within a trick, and rotating the opening lead gives every seat one first lead. Both should flatten the seat-4 bias. Four short hands reduce the luck of one bad deal. Play rewards several kinds of reasoning:
- counting the 24 cards;
- inferring voids from players who fail to follow, which shows who can shed the Quinola or the Aces;
- deciding when to lead a low card to duck and when to cash a high card early;
- watching the sweeper to judge whether a player who has won several tricks is attempting a reversis, and spending a cheap winning card to break it.
Simple policies still lose:
- Always playing the highest legal card collects the points.
- Always playing the lowest legal card leaves you stuck with high cards in the last tricks. It can also hand a reversis-capable opponent the run, which costs you 15.
Talk is left out. With hidden hands, talk would mainly let three players gang up on the leader or trade claims about card holdings that cannot be checked. That adds words without real reasoning, and the original game has no table talk.

## Complexity (the designer's count, against the limits)

- steps_per_round: 14 (limit 20)
- choice_steps_per_round: 2 (limit 4)
- attributes: 14 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 24 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
