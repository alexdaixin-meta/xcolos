# Variation: Secret Slice

A 3-player cut-and-choose pizza draft. The Slicer splits a line of 6 slices into 3 portions, and each player chases topping majorities while hiding a secret favourite topping.

Players: 3 to 3, best with 3

## Review of the original

New York Slice is an 'I split, you choose' drafting game for 2 to 6 players. Each round a rotating Slicer cuts a circle of 11 face-up slices plus a Special into contiguous portions, one per player. The others pick a portion before the Slicer, who takes the last one. At the end, majorities in each pizza type score, eaten pepperoni scores 1 per pepperoni, and collected anchovies cost points.

- **non_degenerate**: good. Simple policies lose. A Slicer who always cuts equal-sized portions is exploited by pickers who take the portions they value most. A picker who always takes the biggest portion can be handed a pile of anchovies. A player who always eats pepperoni gives up the pepperoni majority. The Slicer role rotates, so no seat has a structural edge.
- **skill_sensitive**: good. Cutting so that every portion is roughly equal in value to you, while predicting what earlier pickers will grab, is a real skill. The deal adds variance, but every player faces the same face-up slices.
- **headroom**: good. Majority races, tie denial and the eat-or-collect choice give a strong player much to refine. A weak player still scores from eaten pepperoni and occasional majorities.
- **reasoning_dependent**: weak. All information is public. The only inference is predicting picks from visible collections, and with full information a careful player can compute what each opponent needs. There is no hidden type to read or bluff about.
- **verifiable**: good. Majorities, pepperoni counts and anchovy penalties are all arithmetic on recorded holdings.
- **fits_platform**: weak. It is turn-based and text-friendly, but the circular layout reads as spatial, there are many different Special cards, rounds have 11 slices, and the game supports up to 6 players. Each of these inflates the steps and attributes beyond what the engine builds reliably.

## Problems

- With perfect information there is nothing hidden to infer, so opponent modelling reduces to calculation.
- The circular layout and wrap-around cuts suggest a spatial arrangement and make the cut harder to state as numbers.
- Many unique Special cards with different effects create a long chain of rules and too many attributes to build.
- Eleven slices per round, up to 6 players and a variable number of stacks make rounds long and the step count high.
- The Slicer would need a separate eat-or-collect decision after the picks, which exceeds the limit on choice steps per round.

## Changes

- Each player is secretly dealt a distinct favourite topping. Every collected slice of that type is worth +1 at the end. (fixes: With perfect information there is nothing hidden to infer, so opponent modelling reduces to calculation.): This creates a hidden type. The Slicer must guess what each picker wants, and pickers can bluff or reveal through their picks.
- Each round, every player writes one short message at the same time, before the cut. All messages are then shown. (fixes: With perfect information there is nothing hidden to infer, so opponent modelling reduces to calculation.): Players can claim favourites, true or false, to steer the Slicer's cut. Since only one player can win, each player benefits from a cut that favours them, so believing a claim has a cost.
- Slices are laid out in a numbered line of 6. The Slicer gives two cut positions, which produce three contiguous portions. (fixes: The circular layout and wrap-around cuts suggest a spatial arrangement and make the cut harder to state as numbers.): The cut becomes two numbers, with no circle or adjacency.
- Special cards are removed. The game uses four topping types with fixed majority values and a fixed anchovy penalty. (fixes: Many unique Special cards with different effects create a long chain of rules and too many attributes to build.): This keeps the rules short and buildable.
- The game is fixed at 3 players, 6 rounds and a 36-slice deck shuffled once. Each player is Slicer twice. (fixes: Eleven slices per round, up to 6 players and a variable number of stacks make rounds long and the step count high.): The game becomes short and has a fixed size. Every player slices equally often and holds every pick position equally often.
- The Slicer declares eat or collect for their eventual leftover portion as part of the cut. (fixes: The Slicer would need a separate eat-or-collect decision after the picks, which exceeds the limit on choice steps per round.): This keeps choice steps at 4. It also adds a commitment tension, because the Slicer does not know which portion will be left.

## Kept from the original

- I-split-you-choose: the Slicer cuts into contiguous portions in a fixed order and picks last.
- A rotating Slicer.
- Majority scoring per pizza type, with ties scoring nothing.
- The option to eat pepperoni for points instead of collecting it.
- Collected anchovies are negative.

## The variation's rules

SETUP
- There are 3 players, seated P1, P2, P3.
- The deck has 36 slices: 9 Cheese, 9 Mushroom, 9 Pepperoni and 9 Anchovy. It is shuffled once and split into 6 rows of 6.
- Each player is privately dealt one favourite topping, drawn without replacement from {Cheese, Mushroom, Pepperoni, Anchovy}. The three favourites are therefore all different, and one topping is nobody's favourite.
- Favourites stay secret until final scoring.

ROUNDS
The game has 6 rounds. The Slicer is P1 in round 1, then P2, P3, P1, P2, P3.

In each round:
1. Reveal. The next row of 6 slices is revealed, with positions numbered 1 to 6.
2. Talk. Every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Messages are not binding.
3. Cut. The Slicer states two whole numbers c1 and c2 with 1 <= c1 < c2 <= 5.
   - Portion A is positions 1 to c1.
   - Portion B is positions c1+1 to c2.
   - Portion C is positions c2+1 to 6.
   - In the same answer, the Slicer declares 'eat' or 'collect'. This applies to the pepperoni in whichever portion the Slicer ends up with.
   - The three portions are announced.
4. First pick. The player after the Slicer (P1→P2→P3→P1) chooses one portion and declares 'eat' or 'collect'.
5. Second pick. The remaining non-Slicer player chooses one of the two remaining portions and declares 'eat' or 'collect'.
6. Slicer. The Slicer takes the last portion, with the 'eat' or 'collect' declared at the cut.

EAT OR COLLECT
When a player takes a portion:
- With 'eat', each Pepperoni slice in it is eaten for +1 point and does not count as collected.
- With 'collect', every slice in the portion is collected.
- Non-pepperoni slices are always collected.

FINAL SCORING (after round 6)
Scoring uses only collected slices, plus eaten pepperoni and anchovy penalties.
- Majority: the player with strictly the most collected slices of a type scores Cheese 7, Mushroom 7, Pepperoni 5, Anchovy 10. If there is a tie for most, nobody scores that type.
- Eaten pepperoni: +1 per eaten Pepperoni slice.
- Anchovy penalty: -1 per collected Anchovy slice.
- Favourite: +1 per collected slice of your own favourite type. Eaten slices do not count.

The totals are announced.

Objective: The player with the highest final total wins. If two or three players tie for the highest total, the game is a draw.

Expected effect: Slicers must cut so that every portion is acceptable to them while guessing each opponent's hidden favourite from their past picks and their messages. Pickers balance chasing a majority against revealing their favourite. Talk matters because players disagree about the cut: each wants a portion rich in their own favourite and wants rivals' portions poor. A player who claims a false favourite can steer the Slicer into building a portion they secretly do not need, or into leaving them the one they want. A Slicer who simply follows the claims can be stuck with the worst leftover. Simple policies lose: always taking the biggest portion gets loaded with anchovies, always cutting 2-2-2 is exploited, and always eating concedes the pepperoni majority. Each player slices twice and holds each pick position twice, so no seat has an edge. Favourites roughly balance: the anchovy favourite cancels the penalty while chasing the 10-point majority, and the other favourites add +1 per slice to a 5 or 7 majority.

## Complexity (the designer's count, against the limits)

- steps_per_round: 12 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 12 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 6 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
