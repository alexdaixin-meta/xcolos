# Variation: Point Salad: Secret Recipes

Three players draft vegetables and point cards for 12 rounds with simultaneous picks. Each player holds a hidden two-vegetable Recipe. Players must read rivals' recipes to avoid fighting over the same vegetables, and must decide when to contest the round's point card.

Players: 3 to 3, best with 3

## Review of the original

Point Salad is a 2-6 player card-drafting game. Each turn you take either one scoring-rule card or two vegetable cards from a shared market. At the end, every scoring card you hold is scored against your whole vegetable tableau, and the most points wins.

- **non_degenerate**: good. No simple policy wins. Always taking point cards leaves you with no vegetables to score them, and always taking vegetables leaves you with nothing to score with. Seat order matters slightly, and ties go to the later seat as compensation.
- **skill_sensitive**: weak. Matching cards to vegetables rewards skill. However, the draw order of 108 unique cards and the market refills add a lot of variance. With 4-6 players, what reaches you between turns is mostly out of your control.
- **headroom**: good. Beginners still score points. Experts improve through hate-drafting, timing when to flip cards to vegetables, and reading the market.
- **reasoning_dependent**: weak. All tableaus are face up and the market is public, so nothing about opponents is hidden except their intentions. The reasoning is mostly an optimisation over 108 different rule texts rather than inference.
- **verifiable**: good. Every card's score is arithmetic on vegetable counts.
- **fits_platform**: bad. 108 unique scoring rules far exceed the attribute and step limits. Three piles with refill and pile-splitting is a long chain of deck operations. Sequential turns over about 18 rounds per player at 6 players are too long.

## Problems

- P1: 108 unique scoring rules and a three-pile market with refills and pile-splitting are far beyond the build limits.
- P2: There is nothing hidden. Every tableau is public, so there is no opponent type to infer.
- P3: Sequential drafting with random refills makes the luck of the flow large compared with skill, especially at higher player counts.
- P4 (previous variation): the recipe rule was ambiguous to the test writers. A CT basket with c=2, t=2 was expected to score 16, but the stated formula gives 2×2 + 2×2 + 2×min(2,2) = 12. The rules need an explicit formula with correct worked examples.
- P5 (previous variation): the build log showed recipes changing after the deal (each seat's recipe shifted to another). The rules did not state clearly that recipes are fixed once dealt, so the build invented a rotation.
- P6 (previous variation): the timing of card scoring (before or after this round's vegetables) and the collision outcomes were not pinned down tightly enough for exact tests.

## Changes

- Replace the 108 cards with 6 public scoring-card types, one drawn at random each round with replacement: Tomato Fan, Lettuce Fan, Carrot Fan, Rainbow, Big Bowl, Balance. Each has a fixed arithmetic value. (fixes: P1): This keeps the 'point card scored against your vegetables' idea within build limits.
- Give each player a hidden Recipe, a pair of two vegetables (TL, LC or CT), scored at game end as 2×first + 2×second + 2×min(first, second). (fixes: P2): This creates one strong hidden element. Each recipe shares one vegetable with each rival, so inferring rivals' recipes from their picks decides where collisions happen.
- Replace sequential drafting with a simultaneous pick each round: Tomato, Lettuce, Carrot or Card. A vegetable gives 2 if you pick it alone, 1 each if two players pick it, and 0 if all three do. The Card goes only to a sole claimant, and colliding claimants get nothing. (fixes: P3): The scarcity and contest of the market now come from reading opponents rather than from refill luck. The per-round random card is public and contestable by everyone.
- Write the recipe formula once, exactly, with checked worked examples: CT with c=2, t=2 scores 12; CT with c=3, t=2 scores 14; TL with t=4, l=1 scores 12. (fixes: P4): Tests and the build must agree on the arithmetic.
- State that recipes are dealt once at setup, one from each of TL, LC and CT, and never change, pass or rotate. (fixes: P5): This removes the build's invented recipe rotation.
- Fix the timing and collisions exactly. The Card's value is computed from the claimant's basket as it stood at the start of the round, before this round's vegetables are added. Card collisions give nothing. All picks and baskets are announced after resolution. (fixes: P6): This makes every outcome a deterministic function of picks, the drawn card and prior state.
- Add one simultaneous message per player before each pick. (fixes: P2): Players can bluff their recipe, propose a vegetable split or warn off a Card. Only one player can win, so following a proposal can cost you. This is genuine reasoning about trust.

## Kept from the original

- The central choice each turn: take a point card OR take vegetables.
- Point cards are scored by arithmetic on your own vegetable tableau, and the same vegetable counts for many cards.
- Card types modelled on originals: per-vegetable fans, a set-collection Rainbow, a count-everything Big Bowl and an even-spread Balance.
- Public vegetable tableaus.
- Hate-drafting a card a rival wants.
- Most points wins.

## The variation's rules

VEGETABLES: Tomato (t), Lettuce (l), Carrot (c).

SETUP
1. There are exactly 3 players.
2. Recipes:
- There are 3 Recipe tiles: TL (tomato and lettuce), LC (lettuce and carrot) and CT (carrot and tomato).
- Shuffle them and deal one to each player, so all three are used.
- Each player sees only their own Recipe.
- A Recipe never changes, moves or rotates for the rest of the game.
3. Every player starts with t=0, l=0, c=0 and points=0. Baskets (t, l, c) and points are public at all times. Recipes are secret until game end.

EACH ROUND (12 rounds)
1. Draw the card: one scoring card type is drawn at random, with replacement, equally likely from these 6. It is announced to everyone.
- Tomato Fan: worth 2 × t.
- Lettuce Fan: worth 2 × l.
- Carrot Fan: worth 2 × c.
- Rainbow: worth 3 × min(t, l, c).
- Big Bowl: worth 1 × (t + l + c).
- Balance: worth 6 if t ≥ 1, l ≥ 1, c ≥ 1 and max(t,l,c) − min(t,l,c) ≤ 1; otherwise 0.
2. Talk:
- Every player writes one short message at the same time, without seeing the others.
- All messages are then shown to everyone.
- Messages bind no one.
3. Pick: every player at the same moment chooses exactly one of Tomato, Lettuce, Carrot, Card.
4. Resolve the Card:
- If exactly one player chose Card, that player gains points equal to the drawn card's value, computed from their basket as it stood at the start of this round.
- If zero players, or two or more players, chose Card, nobody gains anything from it. The card is discarded and colliding players receive nothing this round.
5. Resolve vegetables, separately for each vegetable:
- If exactly 1 player chose it, that player adds 2 of it to their basket.
- If exactly 2 players chose it, each adds 1.
- If all 3 chose it, nobody gets any.
6. Announce: everyone's pick, what each received, and all baskets and points.
7. If 12 rounds have been played, go to END. Otherwise start the next round.

END
1. Each player's Recipe is revealed and scored. With first and second as that player's counts of the Recipe's two vegetables:
recipe_score = 2 × first + 2 × second + 2 × min(first, second).
The third vegetable scores nothing in the Recipe.
- TL uses t and l.
- LC uses l and c.
- CT uses c and t.
2. Worked examples (exact):
- CT with c=2, t=2: 4 + 4 + 4 = 12.
- CT with c=3, t=2: 6 + 4 + 4 = 14.
- TL with t=4, l=1: 8 + 2 + 2 = 12.
- LC with l=0, c=6: 0 + 12 + 0 = 12.
3. final_total = points + recipe_score.
4. Example of points deciding the game: a player with points=10 and recipe 12 (final 22) beats a player with points=0 and recipe 14 (final 14).

CARD EXAMPLE: A player starting a round with t=3, l=1, c=2 who is the sole Card claimant scores:
- Tomato Fan: 6
- Lettuce Fan: 2
- Carrot Fan: 4
- Rainbow: 3
- Big Bowl: 6
- Balance: 0 (spread 2 > 1)

Objective: After round 12, the player with the highest final_total (points + recipe_score) wins. If two or three players tie for the highest final_total, the game is a draw among them.

Expected effect: Simple policies all lose.
- Always Card scores 0, because the card values come from an empty basket.
- Always one vegetable caps the recipe at 2 × first, with min = 0. Even uncontested, that is 48 against about 72 for an uncontested balanced pair.
- Random play wastes picks on the useless third vegetable and on Card collisions.

What the players disagree about:
- Every recipe shares one vegetable with each rival, so players fight over who gets the shared vegetables.
- Players also fight over who claims a valuable late card. A Big Bowl or Fan worth 15-25 points in rounds 9-12 creates a chicken game.

What talk is for:
- Bluffing a recipe, offering a split ('I'll stay off carrots') or threatening to contest a card.
- A player who trusts a split while the speaker defects ends up colliding for 1 instead of 2, or loses the card.

What good play needs: inferring recipes from early picks, planning basket growth so cards claimed later are worth more, and predicting who will contest the card. The random card is public and open to all, and the recipes are symmetric, so neither is a lottery.

## Complexity (the designer's count, against the limits)

- steps_per_round: 12 (limit 20)
- choice_steps_per_round: 2 (limit 4)
- attributes: 17 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 12 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
