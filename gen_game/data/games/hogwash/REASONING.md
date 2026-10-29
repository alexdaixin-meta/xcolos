# Reasoning and planning: Hogwash: Six Ranks

**Verdict: weak.** Early on, winning takes real card-tracking and odds weighing, but the game quickly settles into a frozen state where every claim is a provable bluff on an empty pile, so the deal and a few early challenges decide it. Making a caught bluff cost something even on an empty pile (e.g., a penalty card), or capping repeated impossible claims, would keep claim sizing and multi-turn planning relevant all game.

From 3 play(s): 288 choices, 279 with a reason given (about 43.3 words each); results {'seat 2': 2, 'seat 3': 1}.

## Reasoning: 2 of 3

Responders track cards closely: they follow revealed bluffs back into hands, use the engine's fill order to rule out ranks, and compute hypergeometric odds, and most of these inferences are correct. Once the early rounds pass, though, nearly every decision is a certain-bluff detection ('I hold two, so they can't have four'), and active players keep making impossible k=4 claims, so the reasoning is thin across most of the game.

- match 3, turn 24, seat 2: "this is a bluff only if both sixes sit in seat 1's 2 unknown slots, which is about a 1 in 36 chance" (Infers the opponent's hand from revealed cards and computes an exact odds figure)
- match 2, turn 60, seat 2: "The engine takes cards in the order 6, 1, 2, 3, 4, 5. Seat 3 played [1, 4, 4, 5], so it had no 6s, no 2s and no 3s at that point." (Uses the engine's fill order to deduce which ranks are missing from a hidden hand)
- match 1, turn 28, seat 3: "The fourth went back into seat 1's hand when they took the pile after being caught in round 1. It hasn't left their hand since, so their one card must be that 1." (Follows a single card through pile pickups to prove a claim is true)
- match 3, turn 45, seat 3: "These opponents almost always challenge 4-card claims but often trust 1-card claims. A small, believable claim gives the best expected result." (Reads opponents' tendencies and adjusts claim size, the kind of weighing the designer asked for)

## Planning: 1 of 3

Look-ahead is rare and short: one player empties a hand to dodge later turns, another sets up a final-round tie win on catches, and a leader notes it can trust next round. Most turns are judged alone, and the mid-game is a repeated loop of empty-pile max bluffs with no multi-turn plan.

- match 1, turn 29, seat 2: "With an empty hand I skip my later turns and can only gain cards by challenging." (Considers how shedding now affects the turns that follow)
- match 1, turn 89, seat 2: "Playing the maximum gives the biggest gain for the same risk, and next round I can simply trust to avoid picking up the pile." (Plans one round ahead to protect a lead)
- match 3, turn 93, seat 3: "That would leave me at 6 cards, tied with seat 2, and I would win the tie on catches (13 to 12)." (End-game plan that relies on the tiebreak counters)

## Luck: 2 of 3

All three matches were decided in the first six rounds, largely by who was dealt multiple copies of their required ranks and got doubly challenged on true plays. After that, hand sizes froze as certain bluffs were always caught. The deal set who could make true plays at all, while challenge choices made on reasonable odds turned out badly by chance.

- match 1, turn 20, seat 3: "with about a 64% chance of a bluff, challenging should usually send 3 cards to Seat 2" (A favourable challenge lost to a strong deal; seat 2 dropped to 2 cards and won)
- match 2, turn 24, seat 2: "The chance seat 3 holds both is only about 13%." (A 13% outcome happened and decided the winner: seat 3 shed to 6 and later 5)

## Weak spots

- match 1, turn 35, seat 1: Challenged seat 3's single 3 without noticing that seat 3's round-3 card came back to it in the round-4 pile pickup, so seat 3 very likely held a real 3. Seat 2 tracked this correctly and trusted. Trusting was the better-reasoned option.
- match 1, turn 45, seat 3: From mid-game on, active players kept claiming four of a rank that responders could disprove from their own hands, guaranteeing a challenge. A plausible 1-card claim, which seat 3 itself later found works (match 3 turn 45), gave some chance of shedding.
- match 1, turn 73, seat 1: Played k=1 on a certain bluff onto an empty pile while saying the cost was the same for any k. k=4 was weakly better, since the downside was identical and the upside larger.
- match 2, turn 89, seat 2: Justified k=4 by saying a bigger pile makes it costlier for seat 3 if caught in round 24. That holds only if the claim is trusted, and nobody trusted impossible claims. Seat 3 had already locked the win at 5 cards, and the reasoning ignored that.
