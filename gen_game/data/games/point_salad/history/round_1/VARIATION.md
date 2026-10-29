# Variation: Secret Salad

Three players draft vegetables and scoring cards over 12 rounds with simultaneous picks. Each holds a secret Recipe that prizes two of the three vegetables. Contested items go to no one, so reading and bluffing about rivals' Recipes decides who eats well.

Players: 3 to 3, best with 3

## Review of the original

Point Salad is a 2-6 player card-drafting game. Each turn a player takes either one scoring-rule card or two vegetable cards from an open market, and at the end every scoring card is applied to that player's whole vegetable collection; the most points wins.

- **non_degenerate**: good. No fixed policy wins. Always taking veggies leaves you with no scoring cards and near 0 points. Always taking point cards leaves nothing for them to score, and many cards carry penalties. Seat order matters only slightly: later turn order wins ties and the first player gets first pick.
- **skill_sensitive**: weak. Good drafting does beat random drafting. But what is offered depends heavily on which of 108 unique cards turn up, and with 36-108 cards the swing from a lucky pile top is large for so short a game.
- **headroom**: good. Beginners score through obvious combos. Experts gain by hate-drafting, reading what opponents' cards need, and flipping cards at the right moment.
- **reasoning_dependent**: weak. Everything is face up: every tableau, the market and the pile tops. The only unknown is the deck order. There is planning, but almost nothing about opponents to infer; it is close to a perfect-information optimisation.
- **verifiable**: good. The final score is pure arithmetic on cards held.
- **fits_platform**: bad. It has 108 unique scoring rules, three refilling piles with pile-splitting, a market and per-player tableaux. That is far beyond 20 attributes and 1 random draw per round, and end scoring would need a step for each distinct rule.

## Problems

- Far too many unique cards and moving parts (three piles, pile splitting, refilling market) to build within the step, attribute and draw limits.
- Nearly perfect information: there is little hidden to infer about opponents, so it tests optimisation more than opponent modelling.
- Luck of which scoring cards appear is large relative to skill.
- Sequential turns give a seat edge (first pick, tie-break by turn order).
- End-of-game scoring of many cards against the whole tableau needs per-player storage of every drafted card, which exceeds the attribute limit.

## Changes

- Reduce to 3 veggies (Tomato, Lettuce, Carrot), a fixed market of one of each per round, and one public point card per round drawn from 6 types. (fixes: Far too many unique cards and moving parts (three piles, pile splitting, refilling market) to build within the step, attribute and draw limits.): This keeps the drafting choice (take a veggie or take a scoring card) inside 1 random draw per round and a handful of steps.
- Deal each player a secret Recipe. The three Recipes are rotations of one another, each prizing a different pair of veggies, and they score at game end on the player's whole basket. (fixes: Nearly perfect information: there is little hidden to infer about opponents, so it tests optimisation more than opponent modelling.): This creates hidden types to infer from picks and talk. Every veggie is wanted by exactly two Recipes, so interests clash. Because the Recipes are rotationally symmetric, no Recipe is better than another.
- Point cards score immediately on your basket at the moment you take them. (fixes: End-of-game scoring of many cards against the whole tableau needs per-player storage of every drafted card, which exceeds the attribute limit.): This keeps 'the same veggie counts for many cards' while needing no storage of drafted cards. It also adds a timing decision: take the card early for a little or late for a lot.
- Picks are simultaneous. If two or more players pick the same item, nobody gets it. (fixes: Sequential turns give a seat edge (first pick, tie-break by turn order).): This removes the seat edge, makes predicting opponents central, and lets a player deny a rival at a cost to themselves.
- Use only 6 point-card types of similar value, drawn with replacement, with every card open to all players. (fixes: Luck of which scoring cards appear is large relative to skill.): A card's luck is shared by everyone. What it is worth depends on each player's basket and timing, not on who saw it first.

## Kept from the original

- The core draft decision: take vegetables or take a scoring card.
- Scoring cards that value your vegetable collection, with the same vegetable counting toward many cards.
- Set-collection tension between specialising and balancing (pair bonus, Rainbow, Balance).
- Hate-drafting: taking or contesting what a rival needs.
- Most points wins.

## The variation's rules

SETUP: There are three vegetables: Tomato (T), Lettuce (L), Carrot (C). There are three secret Recipes:
- Recipe TL is worth 2 per T + 2 per L + 2 per complete T-L pair (that is, 2 x the smaller of T and L).
- Recipe LC is worth 2 per L + 2 per C + 2 x the smaller of L and C.
- Recipe CT is worth 2 per C + 2 per T + 2 x the smaller of C and T.
Shuffle the three Recipes and deal one face down to each player. Each player sees only their own Recipe and knows the other two players hold the other two. Every player starts with T=0, L=0, C=0 and 0 points.

EACH ROUND (12 rounds):
1. Draw one point card at random, with replacement, from these 6 equally likely types:
- Tomato Fan: 2 points per T you hold.
- Lettuce Fan: 2 points per L you hold.
- Carrot Fan: 2 points per C you hold.
- Rainbow: 3 points per complete set of one T, one L and one C (3 x the smallest of your three counts).
- Big Bowl: 1 point per vegetable you hold (T+L+C).
- Balance: 6 points if you hold at least one of each vegetable and your largest count minus your smallest count is at most 1; otherwise 0.
2. Announce the round number, the point card, and every player's current T, L, C counts and points. Baskets and points are public; Recipes are not.
3. Talk: every player writes one short message at the same time without seeing the others. All messages are then shown to everyone. Talk is not binding and may be false.
4. Pick: every player simultaneously chooses exactly one of: Tomato, Lettuce, Carrot, or Card. The market each round holds exactly one Tomato, one Lettuce, one Carrot and the drawn point card.
5. Resolve: for each of the four options, count how many players chose it.
- If exactly one player chose a vegetable, that player adds 1 of it to their basket.
- If exactly one player chose Card, that player immediately scores the point card against their basket as it stands now, before this round's vegetables are added. Add those points to their total.
- If two or more players chose the same option, nobody receives it.
Unclaimed items are discarded.
6. Announce what every player picked and what they received.

END: After round 12, reveal all Recipes. Each player adds their Recipe score, computed on their final basket, to the points they earned from point cards. That sum is their final total.

Objective: The player with the highest final total wins. If two or three players tie for the highest total, the game is a draw.

Expected effect: Each vegetable is prized by two of the three Recipes, so each player's two key vegetables are both contested. Players must guess who holds which Recipe from basket contents and talk, and must decide when to dodge a collision, when to force one to deny a rival, and when to grab a point card. Point cards reward timing: Big Bowl or Rainbow is weak early and strong late. Off-Recipe vegetables are worth taking for Carrot Fan, Rainbow or Balance, which also helps disguise your Recipe. Talk passes both tests. Interests conflict because only one player can win and every vegetable is wanted by two Recipes. Players can propose divisions ('I'll take Lettuce, you take Tomato'), claim a false Recipe, or promise to leave the card alone. A player who just follows proposals can be steered into taking vegetables worthless to their Recipe, or can be ambushed on the item they were promised. Simple policies lose. Always Card scores 0 in round 1, and with a single card scored before each round's vegetables are added, its basket stays empty and it scores 0 overall. Always the same vegetable earns 2 per round at best, and it is collidable or ignorable by rivals. A balanced Recipe collector earns 3 per round plus point cards. Recipes are rotations of one another, so the deal does not decide the winner.

## Complexity (the designer's count, against the limits)

- steps_per_round: 13 (limit 20)
- choice_steps_per_round: 2 (limit 4)
- attributes: 17 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 12 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
