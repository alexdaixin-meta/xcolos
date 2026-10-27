# Reasoning and planning: 11 Nimmt: Two Hot Piles

**Verdict: adequate.** Winning clearly rewarded card counting, odds on the next player's follow, and multi-turn pile-filling traps, and the consistent winner (seat 1) played exactly that way. More hidden structure would reward deeper reasoning, for example more set-aside cards or variable pile capacity, so that simple counting leaves real uncertainty.

From 3 play(s): 66 choices, 65 with a reason given (about 77.4 words each); results {'seat 2': 1, 'seat 1': 2}.

## Reasoning: 3 of 3

Early moves mostly use a generic 'keep my hand flexible' heuristic. From mid-game on, most decisions rest on correct counting of unseen cards, how those cards split between hands, and rough odds that the next player can follow, as the designer intended. The counts checked (e.g. match 1 turn 15, match 2 turn 19) are accurate, and pile-take arithmetic including bulls is consistently right.

- match 1, turn 15, seat 1: "Unseen cards:** 3, 4, 9, 10, 15, 17, 23, 27 and 30. Seats 2 and 3 hold four of these each, and one was set aside." (Correct reconstruction of the unseen cards, used to compare how many follow each candidate top (3 of 9 vs 4 of 9).)
- match 2, turn 19, seat 2: "With 9 on top, a card fits only if it is 10 to 19, and none of the six unknown cards is in that range. Even 7 doesn't fit. So seat 3 must take" (Exact inference that the next player cannot follow, which deliberately forces a take.)
- match 3, turn 16, seat 1: "The chance seat 2 holds 17 or 26 is about 79%." (Weighs which pile to fill by the probability that the next opponent can fill the other one and force a take back.)

## Planning: 3 of 3

Seat 1 repeatedly set up two-turn traps: fill one pile, count on the intermediate player's move, then fill the other so the target seat is forced to take. These plans were carried out in all three matches. Players also chose restart cards and kept cards in hand to chain onto future tops.

- match 1, turn 6, seat 1: "Next turn I can probably fill A with 7, 13, 16, 20 or 21. That would leave seat 2 with no room and force them to take." (Multi-turn plan relying on seat 3's intervening play. It was executed at turn 8, and seat 2 was forced at turn 9.)
- match 2, turn 6, seat 1: "Whichever pile seat 3 fills next, I can still fill the other one... Then both piles are full, and seat 2 is forced to take a 5-card pile." (Contingent plan covering either choice by seat 3. It was carried out at turn 8.)
- match 3, turn 6, seat 1: "If seat 3 has a card that fits A, they play it there. I can then likely fill A with my 1" (Kept a reserve fitter for later, as the designer advises. Seat 1 then played 1 on A and seat 2 had to take.)

## Luck: 2 of 3

The deal decided how many fitters a player had at key moments. Whether an opponent happened to hold a follow card determined some takes, and two matches were close (6/7/7). Still, the deliberate forcing plays steered most of the big penalties.

- match 3, turn 19, seat 3: "if seat 2 plays 8 or 10 on A, neither of my next cards will fit. I will have to take either way." (Some takes were dictated by the hand held, not by choice.)
- match 1, turn 16, seat 1: "So the risk is about the same either way." (Outcome hinged on whether the next seat happened to hold a filler.)

## Weak spots

- match 1, turn 2, seat 2: Called 5 'a low ox card', but 5 carries 2 ox-heads. Playing 8 or 9 on A would have kept the same flexibility at lower ox.
- match 3, turn 12, seat 2: Played the lowest fitter purely for hand flexibility, the 'always lowest fitter' reflex the designer warns against. It did not consider which pile would fill on whose turn, and seat 2 was later forced into two more takes.
- match 3, turn 4, seat 2: Built A with 18 without considering the fill sequence. This let seat 1 fill B and then A around seat 3, trapping seat 2 at turn 8. Keeping pile counts uneven relative to seat order was the better-reasoned option.
