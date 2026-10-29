# point_salad: ready for review

Built from the variation **Point Salad: Secret Recipes** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Replace the 108 cards with 6 public scoring-card types, one drawn at random each round with replacement: Tomato Fan, Lettuce Fan, Carrot Fan, Rainbow, Big Bowl, Balance. Each has a fixed arithmetic value. (fixes: P1): This keeps the 'point card scored against your vegetables' idea within build limits.
- Give each player a hidden Recipe, a pair of two vegetables (TL, LC or CT), scored at game end as 2×first + 2×second + 2×min(first, second). (fixes: P2): This creates one strong hidden element. Each recipe shares one vegetable with each rival, so inferring rivals' recipes from their picks decides where collisions happen.
- Replace sequential drafting with a simultaneous pick each round: Tomato, Lettuce, Carrot or Card. A vegetable gives 2 if you pick it alone, 1 each if two players pick it, and 0 if all three do. The Card goes only to a sole claimant, and colliding claimants get nothing. (fixes: P3): The scarcity and contest of the market now come from reading opponents rather than from refill luck. The per-round random card is public and contestable by everyone.
- Write the recipe formula once, exactly, with checked worked examples: CT with c=2, t=2 scores 12; CT with c=3, t=2 scores 14; TL with t=4, l=1 scores 12. (fixes: P4): Tests and the build must agree on the arithmetic.
- State that recipes are dealt once at setup, one from each of TL, LC and CT, and never change, pass or rotate. (fixes: P5): This removes the build's invented recipe rotation.
- Fix the timing and collisions exactly. The Card's value is computed from the claimant's basket as it stood at the start of the round, before this round's vegetables are added. Card collisions give nothing. All picks and baskets are announced after resolution. (fixes: P6): This makes every outcome a deterministic function of picks, the drawn card and prior state.
- Add one simultaneous message per player before each pick. (fixes: P2): Players can bluff their recipe, propose a vegetable split or warn off a Card. Only one player can win, so following a proposal can cost you. This is genuine reasoning about trust.

Objective: After round 12, the player with the highest final_total (points + recipe_score) wins. If two or three players tie for the highest final_total, the game is a draw among them.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. Labelled arithmetic checks out. Recipe examples: CT(2,2)=4+4+4=12; CT(3,2)=6+4+4=14; TL(4,1)=8+2+2=12; LC(0,6)=0+12+0=12. Card example (3,1,2): Tomato Fan 6, Lettuce Fan 2, Carrot Fan 4, Rainbow 3x1=3, Big Bowl 6, Balance 0 (spread 2). Final-total example: 22 beats 14.

Vegetable payoffs per pick: a
- playable: pass. The rules are complete.
- Setup deals all 3 recipes.
- Each round has one public random draw (6 types, with replacement), simultaneous talk and a simultaneous 4-way pick.
- Card resolution is explicit: only a sole claimant scores, using the start-of-round basket.
- Vegetable resolution is explicit f
- reasoning_over_luck: pass. Chance enters in two places.
(a) The recipe deal is a symmetric cycle and confers no advantage.
(b) The 12 card draws are public before the pick. A draw favours whoever's basket suits it, but players shape their baskets knowing the six types: they diversify for Rainbow and Balance and build volume f

## Complexity

- steps_per_round: designed 12, built 11, limit 20
- choice_steps_per_round: designed 2, built 2, limit 4
- attributes: designed 17, built 36, limit 20 (built: 80)
- hidden_elements: designed 1, built 6, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 12, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: every basket and points start at 0 and all three Recipe tiles are dealt
- pass: One card is drawn and announced each round (draw rigged: all 6 entries Big Bowl)
- pass: Tomato Fan is worth 2*t: t=3 gives 6 (draw rigged: all 6 entries Tomato Fan)
- pass: Carrot Fan is worth 2*c: c=2 gives 4 (draw rigged: all 6 entries Carrot Fan)
- pass: Lettuce Fan is worth 2*l: l=4 gives 8 (draw rigged: all 6 entries Lettuce Fan)
- pass: Rainbow is worth 3*min(t,l,c): t=3, l=1, c=2 gives 3 (draw rigged: all 6 entries Rainbow)
- pass: Big Bowl is worth t+l+c: t=3, l=1, c=2 gives 6 (draw rigged: all 6 entries Big Bowl)
- pass: Balance is worth 0 when the spread is too big: t=3, l=1, c=2 gives 0 (draw rigged: all 6 entries Balance)
- pass: Balance is worth 6 when each is at least 1 and the spread is at most 1: t=1, l=2, c=2 (draw rigged: all 6 entries Balance)
- pass: Card value uses the basket at the start of the round: 2 tomatoes from round 1 make Tomato Fan worth 4 in round 2 (draw rigged: all 6 entries Tomato Fan)
- pass: Talk happens each round and binds no one; the round still resolves
- pass: Every seat is offered Tomato, Lettuce, Carrot and Card, and its pick is recorded
- pass: The sole Card picker gains the card value (Tomato Fan rigged, t=2 gives 4)
- pass: Two Card pickers cancel: nobody gains points
- pass: No Card picker: nobody's points change
- pass: A sole vegetable picker adds 2 of it
- pass: Two players picking the same vegetable each add 1
- pass: All three picking the same vegetable get nothing
- pass: After the round every pick, basket and points total is public
- pass: The game ends after round 12 and the best recipe total wins
- pass: Recipe score: CT with c=3, t=2 is 14; LC with l=0, c=6 is 12
- pass: Points 10 plus recipe 12 (22) beats points 0 plus recipe 14 (14)
- pass: Two players tied at the top share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [3], results {'seat 3': 7, 'seat 2': 10, 'seat 1': 3}, 72-72 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 72.0 decisions, prompts of 143 characters on average (longest 150)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 3': 15, 'seat 2': 24, 'seat 1': 18, 'seats 1 and 2': 1, 'seats 1 and 3': 2}
- always `first@seat1`: won 19, lost 38, drew 3
- always `first@seat2`: won 16, lost 41, drew 3
- always `last@seat1`: won 0, lost 60, drew 0
- always `last@seat2`: won 0, lost 60, drew 0

## Choices the rules did not make

- 3 players, fixed: The designer fixed exactly 3: the three Recipes are all dealt and the collision rules (1, 2 or 3 pickers) are written for three seats.
- Keep simultaneous talk before the pick, as a poll with broadcast: The rules ask for simultaneous messages. Players clash over the Card and over shared vegetables, so a proposal can cost the one who follows it, and the talk gives players something to bluff and coordinate with.
- recipe_score is recomputed every round as owner-only state and revealed in the final round: The ranking needs it as an attribute, and computing it as the baskets change gives the same value at the end.
- Strategy at the table: A thoughtful player reads the public baskets to guess the others' secret Recipes and Card values, avoids colliding on the Card when another player has a big payoff, and uses talk to bluff or steer the others away from shared picks.

## Simplifications

- The Recipe reveal is an announcement step that runs when round == 12, before the end check: The engine has no separate end phase. The reveal is equivalent and does not change scoring.
