# Reasoning and planning: Put: Sixteen Hands

**Verdict: adequate.** Winning rewards reasoning: reading the lead and answer, counting the opponent's possible holdings, and exploiting their Put and fold habits all paid off. However, short hands and large swings from dealt high pairs leave deal luck heavily involved. More decisions per hand, such as a choice over trick 2's card or a second betting round, would demand more planning and dilute the swings that come from the deal.

From 3 play(s): 216 choices, 216 with a reason given (about 58.5 words each); results {'seat 1': 2, 'seat 2': 1}.

## Reasoning: 3 of 3

Most decisions rest on specific inference: what the lead card reveals about the opponent's remaining cards, explicit card-count odds, and reads on the opponent's Put and fold habits built across hands. There are a few slips, such as calling for 'variance' with hands that are -EV and leading a 13, which hands trick 1's cheap dump to the opponent. Most odds and reads, though, are specific and roughly correct.

- match 1, turn 10, seat 2: "Their lead of 3 is probably their lowest card, since in hand 1 they led 3 while holding 12 and 6." (Uses an earlier reveal to infer the opponent's lead habit and narrow their hidden cards.)
- match 1, turn 41, seat 2: "Seeing is worth about 4 × (0.52 − 0.38) ≈ +0.57. Folding costs −1." (Weighs See against Fold by expected value, and discounts the Put signal using the opponent's earlier bluff.)
- match 3, turn 4, seat 2: "Winning pairs for me: 861 − 21 = 840 out of C(48,2) = 1128, about 74%." (Exact combinatorial count of the opponent's possible holdings before raising.)
- match 1, turn 21, seat 1: "But a Put would likely make them fold their weak hands and play on with their strong ones, which costs me 4 when I lose." (Sees that a 61% favourite still should not Put, because of how a sensible opponent responds selectively.)

## Planning: 2 of 3

Players often shape trick 1 for the Put window that follows. They hide strength to get a Put seen, win trick 1 cheaply to set up a credible bluff, and exploit an opponent's observed fold habit. They also manage the score across hands, for example locking a win by committing to Check/Fold for the remaining hands. Each hand is short, so true multi-turn plans are limited to this end-of-match score management.

- match 1, turn 53, seat 1: "Losing trick 1 also hides my strength, so a Put is more likely to be seen for a stake of 4." (Chooses the answer card to induce a seen Put later in the hand.)
- match 1, turn 28, seat 1: "A trick-1 win would make a later Put more believable, and this opponent has folded to every lone Put so far." (Sets up a bluff that relies on the opponent's observed tendency.)
- match 1, turn 66, seat 1: "If I always Check and Fold to any Put, the opponent can gain at most 1 point per hand. That caps them at 11, so the win is locked." (Multi-hand plan to secure the match, carried out over the last two hands.)
- match 2, turn 57, seat 2: "seat 1 has folded to my lone Put both times after I won trick 1." (Lead chosen to exploit an opponent pattern tracked across hands.)

## Luck: 2 of 3

The big 4-point swings mostly came when one player was dealt very high pairs (13/12) and both Put, which decided several hands outright. Match 3's 24-4 result was driven largely by deals. Fold and check choices still shaped the margins in the closer matches.

- match 3, turn 44, seat 2: "I hold 13 and 12 for tricks 2 and 3, so I almost surely win both." (The dealt cards alone settle the hand.)
- match 2, turn 64, seat 2: "I've already won trick 1, and I still hold 12 and 4. I win the hand if the opponent's higher card is below 12, or if their lower card is below 4. That is a strong position, so I'll Put." (A reasonable Put lost 4 because the opponent happened to hold 13 and 12.)

## Weak spots

- match 3, turn 1, seat 1: Led the 13. That lets the responder dump their lowest card and keep 12 and 10 against 10 and 6, and the hand was lost for 4. Leading the 6 would have kept 13 and 10 together, the reasoning this same model used in other hands.
- match 3, turn 22, seat 1: Saw a Put needing to win both tricks with 10 and 7 after the opponent won trick 1 with an 8, while admitting the Put signals strength. Being down only 1-5 in hand 5 does not justify a -EV call for variance; folding was better.
- match 3, turn 40, seat 1: Saw with 12 and 4 despite noting the opponent 'probably hold nothing below 4'. Calling being 7 behind with 8 hands left 'nearly hopeless' is wrong, and the call cost 4 more; folding was clearly better.
