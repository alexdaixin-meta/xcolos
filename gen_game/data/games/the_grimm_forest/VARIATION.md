# Variation: Three Pigs: Secret Materials

3-4 pigs secretly pick where to gather each round. They split piles when they share, can send the Wolf to spoil a location, and race to build three houses. Each pig's cheap material is secret, and nobody can win with one material alone.

Players: 3 to 4, best with 3

## Review of the original

The Grimm Forest is a 2-4 player race in which the three little pigs secretly choose where to gather straw, wood or brick. A pig alone at a location takes all of its resources, while pigs who share a location split them. Players then spend materials to build houses floor, then walls, then roof, using Fable and Friend cards to interfere, and the first to finish three houses wins.

- **non_degenerate**: good. Simultaneous location choice with a split when players share punishes any fixed policy. A player who always picks the same location is easy to read, gets shared or blocked by Monsters, and the others can avoid them or crowd them. Turn order gives the first player a small edge in Fables and building, but the core choice is a fair simultaneous one.
- **skill_sensitive**: weak. Guessing where others will go and timing builds is real skill. However, the Fable and Friend draws are large swings that come from the deck, and a lucky Fable can wipe out a well-read gather round.
- **headroom**: good. Reading opponents' needs from their half-built houses, exploiting piles of leftover resources and timing the finish all reward deeper play. A weak player still gathers and builds something.
- **reasoning_dependent**: good. Gather cards are secret and simultaneous, so you must predict who goes where. Fables are hidden, and what a player needs can be inferred from their houses.
- **verifiable**: good. Splitting, building costs and the three-house finish are all arithmetic, so no judge is needed.
- **fits_platform**: bad. The Fable deck has dozens of unique effects and Monster miniatures. Friend cards carry once-per-turn special powers, players build in turn order, and a player can force a card onto another. Far more cards and rules exist than the step and attribute limits allow, even though the core loop is text-friendly.

## Problems

- The Fable deck (many unique effects) and the Friend cards (individual powers, forced gifting) far exceed the platform's step, attribute and hidden-element limits.
- Fable and Friend draws add large luck swings that can override good gather-reading.
- Building in turn order and resolving Fables in turn order give seat-dependent advantages.
- With any combination of houses allowed and all materials worth the same to everyone, players have no private agenda to hide or infer. The only inference is from public board state.
- There is no turn cap or tiebreak for simultaneous finishes, which a fixed-length engine needs.

## Changes

- Replace the whole Fable deck with one Wolf gather option: instead of gathering, a player sends the Wolf to a location. Nobody gathers there this round, and the pile stays and grows. (fixes: The Fable deck (many unique effects) and the Friend cards (individual powers, forced gifting) far exceed the platform's step, attribute and hidden-element limits.): This keeps the Monster idea of scaring pigs off a location as a single arithmetic rule. It also gives a way to block a leader or punish a predictable opponent, at the cost of your own gathering.
- Remove Friend cards and the draw-a-Fable build action. (fixes: Fable and Friend draws add large luck swings that can override good gather-reading.): This cuts complexity and removes card luck, so outcomes come from gather choices and build timing.
- All choices (gather, and both build actions) are simultaneous polls. Ties for the win are broken by leftover resources, not seat. (fixes: Building in turn order and resolving Fables in turn order give seat-dependent advantages.): This leaves no seat edge.
- Deal each player a secret Favoured Material, for which each section costs 1 instead of 2. Keep each player's stockpile private. Allow at most 2 completed houses of any one material, so every winner needs at least one house in a non-favoured material. (fixes: With any combination of houses allowed and all materials worth the same to everyone, players have no private agenda to hide or infer. The only inference is from public board state.): This gives every player a hidden agenda. Others must infer your type from where you gather and what you build, and stockpiles cannot be reconstructed without knowing your costs. The two-per-material cap forces everyone into a contested second material, so collisions and Wolf blocks are real decisions.
- Set a 15-round cap. If several players finish on the same round, the one with most leftover resources wins. At the cap, compare most houses, then most sections, else draw. (fixes: There is no turn cap or tiebreak for simultaneous finishes, which a fixed-length engine needs.): This guarantees an arithmetic end.
- Add one random bonus each round (+2 to one announced location) and a non-shared Market giving 1 of your favoured material. (fixes: Fable and Friend draws add large luck swings that can override good gather-reading.): The bonus plays the role of the original's Mega resources, a public lure that creates collisions. The Market preserves the 4-player location as a safe but slow option. Both are publicly known before players choose, so they shape decisions rather than decide outcomes.

## Kept from the original

- A secret, simultaneous gather location choice among Fields (straw), Forest (wood) and Brickyard (brick), plus a Market.
- Alone you take the whole pile, shared you split it rounding down, and leftovers stay and accumulate.
- Houses built section by section: floor, then walls, then roof, paid in that house's material, with only one unfinished house per material.
- Two build actions per round.
- Monsters scaring pigs away from a location (the Wolf).
- A race: the first to complete three houses wins.

## The variation's rules

SETUP
- Materials: Straw, Wood, Brick.
- Locations: Fields (Straw), Forest (Wood), Brickyard (Brick). Each starts with a pile of 0.
- Each player is secretly dealt a Favoured Material:
  - 3 players: shuffle one Straw, one Wood and one Brick card and deal one each, so all three differ.
  - 4 players: shuffle two each of Straw, Wood and Brick and deal one each.
- A player's Favoured Material is known only to them.
- Each player starts with 0 Straw, 0 Wood and 0 Brick. A player's stockpile is private, known only to them.

HOUSES
- A house is one material and has three sections, built in order: Floor, Walls, Roof.
- Each section costs 2 of that house's material, or 1 if it is the builder's Favoured Material.
- A player may have at most one unfinished house of each material.
- A player may complete at most 2 houses of any one material.
- Which sections each player has built, and of what material, is public. The cost paid is not shown.

EACH ROUND (up to 15 rounds)
1. Bonus: one location is drawn at random (each 1/3) and announced.
2. Refill: every location's pile gains 3, and the announced location gains 2 more.
3. Talk: everyone writes one short message at the same time, then all messages are shown to everyone. Messages bind no one.
4. Gather choice: everyone simultaneously chooses one of seven options:
   - Fields, Forest, Brickyard, Market;
   - Wolf-Fields, Wolf-Forest, Wolf-Brickyard.
5. Reveal: all choices are shown.
6. Resolve each of the three locations:
   - If any player chose Wolf at that location, nobody gathers there and its pile is unchanged.
   - Otherwise, the pile is divided equally among the players who chose it, rounding down. Each takes their share of that material, and the remainder stays in the pile.
   - If nobody chose the location, the pile stays.
   - Each player is told only their own gain, but the piles and the number of gatherers are public, so gains can be computed by anyone.
7. Market: every player who chose Market gains 1 of their Favoured Material. Any number of players can use the Market without sharing.
8. Players who chose a Wolf gain nothing.
9. Build action 1: everyone simultaneously chooses Build Straw, Build Wood, Build Brick or Pass.
   - A build adds the next section to that player's house of that material, starting a new house at the Floor if none is unfinished, and pays the cost from their stockpile.
   - If the player cannot pay, or the build would start a third house of that material, it counts as Pass.
   - The resulting public build state is shown.
10. Build action 2: exactly as build action 1.
11. Win check: any player with 3 completed houses has finished.
    - If exactly one player has finished, they win.
    - If several have, the finisher with the most total leftover resources wins. If that is tied, it is a draw among them.
    - The game then ends.
12. If round 15 ends with no finisher, the game ends. The winner is the player with the most completed houses, then the most built sections. If still tied, it is a draw.

Objective: The first player to complete 3 houses (at most 2 of any one material) wins. If several do so in the same round, the one with the most leftover resources wins, and a further tie is a draw. If nobody finishes in 15 rounds, the winner is the player with the most completed houses, then the most sections. Any remaining tie is a draw.

Expected effect: Every simple policy loses.
- Always Market gains only the Favoured Material, so it can never build the required non-favoured house.
- Always one location gains one material only, so it caps at 2 houses.
- Always Wolf never gathers.
- Random play wastes rounds on collisions and Wolves.

Good play means:
- inferring each rival's Favoured Material from where they gather and which houses they build;
- predicting which piles they will avoid or crowd, and timing a raid on a big accumulated pile;
- using the Wolf to stall whoever is closest to finishing.

With 3 players the types are a permutation, so identifying one rival's type narrows the others. Because the materials are symmetric and the types are worth the same, the deal changes what to do rather than who wins.

Talk earns its place because only one player can win:
- Players may propose splitting locations ('I'll take Forest, you take Fields'), claim false types, or call for a Wolf on the leader.
- A player who simply follows a proposal can walk into a collision, leave a big pile to a rival who lied, or Wolf a location in a way that hands the race to the proposer.
- They disagree about who gathers which contested material and whom to block.

## Complexity (the designer's count, against the limits)

- steps_per_round: 15 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 15 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 15 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
