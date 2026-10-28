# Reasoning and planning: Duplicate Open-Face Pairs

**Verdict: strong.** Winning takes real reasoning and planning: foul-bounded placement, card counting, and in mirrored hands exact modelling of the opponent's options, with matches decided by one or two points of better row contests. It would take more if the second hand of each shuffle were less fully determined, for example by dealing the mirrored hand with some cards hidden or reordered, so that opponent modelling stays inference rather than lookup.

From 3 play(s): 236 choices, 236 with a reason given (about 64.0 words each); results {'seat 2': 2, 'seat 1': 1}.

## Reasoning: 3 of 3

Most decisions rest on specific, correct inference: exact foul bounds, counts of which copies of a value are already accounted for, and in mirrored hands the exact options the opponent holds and how far their rows can reach. There are a few arithmetic slips on pair strengths (107, 108, 106), but they never changed a choice.

- match 1, turn 12, seat 1: "A 6–6 pair is the one danger, and it cannot happen: all four 6s have already passed through my hands. Keeping the 7 instead would foul if my last card were a 7 or an 8." (Card counting used to rule out the only foul risk and compare it with the alternative.)
- match 2, turn 38, seat 2: "They are being dealt [1, 1, 8], the cards I had in hand 1, round 5. Their Middle is 13, so a Front 8 (strength 16) would foul them. They will almost certainly keep a 1" (Predicts the opponent's forced choice from their known options, and takes Front 7 at exactly the tie limit.)
- match 3, turn 74, seat 2: "counting the cards seen in hand 3 and this hand, all four 6s, 5s and 2s are already accounted for. Next round I'll get the 4 the opponent kept in hand 3 round 5, plus two of {3, 4, 7, 8}." (Detailed deduction of the next deal's contents from both hands.)
- match 2, turn 13, seat 1: "All the 5s are already seen, so their best Middle is 6 + 4 = 10... the chance that all three of my next cards are above 5 is only about 3%." (In an unseen hand, combines counting with an explicit foul probability.)

## Planning: 3 of 3

In the mirrored hands, players lay out five-round builds from known future offers and carry them out, including targeted plans against the opponent's known ceiling, such as a scoop plan and an aim to out-pair the opponent's Back. In the first hand of each shuffle, planning is shorter: players keep flexibility and fill Front late.

- match 2, turn 67, seat 2: "Their later options are the cards I had in hand 3... Their Middle can reach at most 11 without fouling... We should win all three rows... 7 points. That is more than our 6-point deficit." (A multi-turn scoop plan built on the opponent's limits, carried out through turn 78 to win the match.)
- match 1, turn 21, seat 1: "I can keep 8 now, then 4, 7, 7 and 8. That gives Back 8+8... Opponent's best hand... Back 6+6 (112), Middle 3+3 (106) and Front 8." (A full-hand plan made in round 1 against a modelled opponent line, executed exactly.)
- match 3, turn 66, seat 2: "Keeping the 7 now and adding that 7 later makes a Back pair of 7s, worth 114. That beats the 6-6 Back pair (112) Seat 1 can build from my hand 3 cards." (Plans two rounds ahead specifically to beat the opponent's predicted row; carried out at turn 72.)
- match 2, turn 34, seat 2: "My last card goes to Front and only has to be 7 or lower... My round-5 cards include the 3 the opponent kept from that slot" (Keeps the Front open for a known later card, which later became the Front 7 royalty.)

## Luck: 1 of 3

The mirrored deals cancel most card luck, and hands 2 and 4 were played with near-full information. Chance mattered only at the margin in the unseen hands 1 and 3, where who saw a late 8 or a pair card first set the target the other seat had to beat. All three matches were decided by one or two points.

- match 2, turn 50, seat 1: "only one 8 remains for a pair" (In unseen hand 3, seat 1 had to commit Back before learning an 8 would come in round 4. That later became the opponent's 8-8 scoop in hand 4.)

## Weak spots

- match 2, turn 8, seat 2: Put the 6 in Back beside the 5, capping Back at 11 when the opponent's Back 7+8=15 was already visible. This led to being scooped. Placing the 6 in Middle and keeping Back open for a 7 or 8 (both offered later) would have contested more rows.
- match 1, turn 21, seat 1: Valued the planned Middle 7-7 at 107 instead of 114. The error was corrected later and was harmless, but it is a miscalculation.
- match 2, turn 67, seat 2: Stated Back 8+8 as 108 instead of 116. It did not change the plan.
- match 3, turn 71, seat 1: Called a 6-6 Back pair 106 instead of 112. The foul check still held only because the 100 pair bonus dwarfs a Middle of 15.
