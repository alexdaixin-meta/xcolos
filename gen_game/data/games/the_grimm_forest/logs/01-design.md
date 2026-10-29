# 01 design

- time: 2026-10-28T04:34:19+00:00 (96.3s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 5e698b4226075452, reply sha256 ead13a63d7f5bee7

## Sent

````
Original game: The Grimm Forest
Players in the original: 2 to 4

Original rules:
Each round has Gather then Build. In Gather, each player secretly chooses one Gather location card (Fields=Straw, Forest=Wood, Brickyard=Brick, Market in 4p) and may play a Fable card face down. Reveal and resolve Fable When Revealed effects in turn order, placing any Monster miniatures. Reveal Gather cards and move pigs. If alone at a location, take all Single and Mega resources there; if multiple pigs share, divide equally rounding down, leftover stays. Resolve End of Gather Fables, discard them and return Monsters. In Build, in turn order each player takes two actions: draw a Fable, gain 1 resource of choice, or Build a house section paying its specific resource type. Houses must be built Floor then Walls then Roof. You cannot have two unfinished houses of same type, and you have 5 build sites. Building Walls lets you draw a Friend card; you may keep it or force it on another player, max one Friend each with a once-per-turn special action. First player to complete any three houses in any combination wins immediately.
````

## Reply

````
```json
{
  "original_summary": "The Grimm Forest is a 2-4 player race in which the three little pigs secretly choose where to gather straw, wood or brick. A pig alone at a location takes all of its resources, while pigs who share a location split them. Players then spend materials to build houses floor, then walls, then roof, using Fable and Friend cards to interfere, and the first to finish three houses wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "Simultaneous location choice with a split when players share punishes any fixed policy. A player who always picks the same location is easy to read, gets shared or blocked by Monsters, and the others can avoid them or crowd them. Turn order gives the first player a small edge in Fables and building, but the core choice is a fair simultaneous one."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Guessing where others will go and timing builds is real skill. However, the Fable and Friend draws are large swings that come from the deck, and a lucky Fable can wipe out a well-read gather round."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Reading opponents' needs from their half-built houses, exploiting piles of leftover resources and timing the finish all reward deeper play. A weak player still gathers and builds something."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Gather cards are secret and simultaneous, so you must predict who goes where. Fables are hidden, and what a player needs can be inferred from their houses."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Splitting, building costs and the three-house finish are all arithmetic, so no judge is needed."
    },
    {
      "criterion": "fits_platform",
      "verdict": "bad",
      "evidence": "The Fable deck has dozens of unique effects and Monster miniatures. Friend cards carry once-per-turn special powers, players build in turn order, and a player can force a card onto another. Far more cards and rules exist than the step and attribute limits allow, even though the core loop is text-friendly."
    }
  ],
  "problems": [
    "The Fable deck (many unique effects) and the Friend cards (individual powers, forced gifting) far exceed the platform's step, attribute and hidden-element limits.",
    "Fable and Friend draws add large luck swings that can override good gather-reading.",
    "Building in turn order and resolving Fables in turn order give seat-dependent advantages.",
    "With any combination of houses allowed and all materials worth the same to everyone, players have no private agenda to hide or infer. The only inference is from public board state.",
    "There is no turn cap or tiebreak for simultaneous finishes, which a fixed-length engine needs."
  ],
  "changes": [
    {
      "what": "Replace the whole Fable deck with one Wolf gather option: instead of gathering, a player sends the Wolf to a location. Nobody gathers there this round, and the pile stays and grows.",
      "why": "This keeps the Monster idea of scaring pigs off a location as a single arithmetic rule. It also gives a way to block a leader or punish a predictable opponent, at the cost of your own gathering.",
      "fixes": "The Fable deck (many unique effects) and the Friend cards (individual powers, forced gifting) far exceed the platform's step, attribute and hidden-element limits."
    },
    {
      "what": "Remove Friend cards and the draw-a-Fable build action.",
      "why": "This cuts complexity and removes card luck, so outcomes come from gather choices and build timing.",
      "fixes": "Fable and Friend draws add large luck swings that can override good gather-reading."
    },
    {
      "what": "All choices (gather, and both build actions) are simultaneous polls. Ties for the win are broken by leftover resources, not seat.",
      "why": "This leaves no seat edge.",
      "fixes": "Building in turn order and resolving Fables in turn order give seat-dependent advantages."
    },
    {
      "what": "Deal each player a secret Favoured Material, for which each section costs 1 instead of 2. Keep each player's stockpile private. Allow at most 2 completed houses of any one material, so every winner needs at least one house in a non-favoured material.",
      "why": "This gives every player a hidden agenda. Others must infer your type from where you gather and what you build, and stockpiles cannot be reconstructed without knowing your costs. The two-per-material cap forces everyone into a contested second material, so collisions and Wolf blocks are real decisions.",
      "fixes": "With any combination of houses allowed and all materials worth the same to everyone, players have no private agenda to hide or infer. The only inference is from public board state."
    },
    {
      "what": "Set a 15-round cap. If several players finish on the same round, the one with most leftover resources wins. At the cap, compare most houses, then most sections, else draw.",
      "why": "This guarantees an arithmetic end.",
      "fixes": "There is no turn cap or tiebreak for simultaneous finishes, which a fixed-length engine needs."
    },
    {
      "what": "Add one random bonus each round (+2 to one announced location) and a non-shared Market giving 1 of your favoured material.",
      "why": "The bonus plays the role of the original's Mega resources, a public lure that creates collisions. The Market preserves the 4-player location as a safe but slow option. Both are publicly known before players choose, so they shape decisions rather than decide outcomes.",
      "fixes": "Fable and Friend draws add large luck swings that can override good gather-reading."
    }
  ],
  "keeps": [
    "A secret, simultaneous gather location choice among Fields (straw), Forest (wood) and Brickyard (brick), plus a Market.",
    "Alone you take the whole pile, shared you split it rounding down, and leftovers stay and accumulate.",
    "Houses built section by section: floor, then walls, then roof, paid in that house's material, with only one unfinished house per material.",
    "Two build actions per round.",
    "Monsters scaring pigs away from a location (the Wolf).",
    "A race: the first to complete three houses wins."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core gather-collision and build-race loop is simultaneous, arithmetic and inference-rich. Only the card decks are too heavy, and they can be replaced by one Wolf rule and a hidden favoured material."
  },
  "variation": {
    "name": "Three Pigs: Secret Materials",
    "summary": "3-4 pigs secretly pick where to gather each round. They split piles when they share, can send the Wolf to spoil a location, and race to build three houses. Each pig's cheap material is secret, and nobody can win with one material alone.",
    "players": {"min": 3, "max": 4, "suggested": 3},
    "rules": "SETUP\n- Materials: Straw, Wood, Brick.\n- Locations: Fields (Straw), Forest (Wood), Brickyard (Brick). Each starts with a pile of 0.\n- Each player is secretly dealt a Favoured Material:\n  - 3 players: shuffle one Straw, one Wood and one Brick card and deal one each, so all three differ.\n  - 4 players: shuffle two each of Straw, Wood and Brick and deal one each.\n- A player's Favoured Material is known only to them.\n- Each player starts with 0 Straw, 0 Wood and 0 Brick. A player's stockpile is private, known only to them.\n\nHOUSES\n- A house is one material and has three sections, built in order: Floor, Walls, Roof.\n- Each section costs 2 of that house's material, or 1 if it is the builder's Favoured Material.\n- A player may have at most one unfinished house of each material.\n- A player may complete at most 2 houses of any one material.\n- Which sections each player has built, and of what material, is public. The cost paid is not shown.\n\nEACH ROUND (up to 15 rounds)\n1. Bonus: one location is drawn at random (each 1/3) and announced.\n2. Refill: every location's pile gains 3, and the announced location gains 2 more.\n3. Talk: everyone writes one short message at the same time, then all messages are shown to everyone. Messages bind no one.\n4. Gather choice: everyone simultaneously chooses one of seven options:\n   - Fields, Forest, Brickyard, Market;\n   - Wolf-Fields, Wolf-Forest, Wolf-Brickyard.\n5. Reveal: all choices are shown.\n6. Resolve each of the three locations:\n   - If any player chose Wolf at that location, nobody gathers there and its pile is unchanged.\n   - Otherwise, the pile is divided equally among the players who chose it, rounding down. Each takes their share of that material, and the remainder stays in the pile.\n   - If nobody chose the location, the pile stays.\n   - Each player is told only their own gain, but the piles and the number of gatherers are public, so gains can be computed by anyone.\n7. Market: every player who chose Market gains 1 of their Favoured Material. Any number of players can use the Market without sharing.\n8. Players who chose a Wolf gain nothing.\n9. Build action 1: everyone simultaneously chooses Build Straw, Build Wood, Build Brick or Pass.\n   - A build adds the next section to that player's house of that material, starting a new house at the Floor if none is unfinished, and pays the cost from their stockpile.\n   - If the player cannot pay, or the build would start a third house of that material, it counts as Pass.\n   - The resulting public build state is shown.\n10. Build action 2: exactly as build action 1.\n11. Win check: any player with 3 completed houses has finished.\n    - If exactly one player has finished, they win.\n    - If several have, the finisher with the most total leftover resources wins. If that is tied, it is a draw among them.\n    - The game then ends.\n12. If round 15 ends with no finisher, the game ends. The winner is the player with the most completed houses, then the most built sections. If still tied, it is a draw.",
    "objective": "The first player to complete 3 houses (at most 2 of any one material) wins. If several do so in the same round, the one with the most leftover resources wins, and a further tie is a draw. If nobody finishes in 15 rounds, the winner is the player with the most completed houses, then the most sections. Any remaining tie is a draw.",
    "expected_effect": "Every simple policy loses.\n- Always Market gains only the Favoured Material, so it can never build the required non-favoured house.\n- Always one location gains one material only, so it caps at 2 houses.\n- Always Wolf never gathers.\n- Random play wastes rounds on collisions and Wolves.\n\nGood play means:\n- inferring each rival's Favoured Material from where they gather and which houses they build;\n- predicting which piles they will avoid or crowd, and timing a raid on a big accumulated pile;\n- using the Wolf to stall whoever is closest to finishing.\n\nWith 3 players the types are a permutation, so identifying one rival's type narrows the others. Because the materials are symmetric and the types are worth the same, the deal changes what to do rather than who wins.\n\nTalk earns its place because only one player can win:\n- Players may propose splitting locations ('I'll take Forest, you take Fields'), claim false types, or call for a Wolf on the leader.\n- A player who simply follows a proposal can walk into a collision, leave a big pile to a rival who lied, or Wolf a location in a way that hands the race to the proposer.\n- They disagree about who gathers which contested material and whom to block."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 15,
    "choice_steps_per_round": 4,
    "attributes": 15,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 15
  }
}
```
````
