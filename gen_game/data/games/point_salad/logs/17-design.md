# 17 design

- time: 2026-10-27T17:33:14+00:00 (68.4s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 966d3d920851407e, reply sha256 cf14f6a2afc0824a

## Sent

````
Original game: Point Salad
Players in the original: 2 to 6

Original rules:
108 cards are double-sided: veggie on one side, unique scoring rule on the other. Remove cards by player count: 2p use 36, 3p 54, 4p 72, 5p 90, 6p 108. Shuffle remaining and make 3 piles point-side up. Flip 2 cards per pile into a column below as a veggie market, veggie-side up. On your turn draft either 1 point card from top of any pile OR 2 veggie cards from the market. Add to your face-up tableau. Once per turn as a free action you may flip any of your point cards to its veggie side, never the reverse. Refill empty market slots from their piles, flipping point to veggie. If a pile empties, split the largest pile to replace it. Game ends when all piles and market are empty. Score each point card using your whole veggie tableau; same veggie can count for many cards. Most points wins, later turn order breaks ties.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
Recompute recipe scores from the rule: 2×T + 2×L + 2×min(T,L) for TL, and the same pattern for LC and CT. A CT player with c=2, t=2 scores recipe_score=12 and final_total=12 when points=0. Fix R23 and R24 to expect 12, or pick baskets that give the intended value, e.g. c=3, t=2 gives 6 + 4 + 4 = 14. For R24, set points so the points-versus-recipe comparison still holds with correct recipe values. Assert on recipe_score, final_total and the winner only.
the game was built and works on the platform, but it does not behave as the independent tests say the rules require:
- scenario `R23 CT player ending with c=2,t=2 scores recipe 16` failed: rule R23 is broken: When a CT player ends with c=2, t=2, then recipe_score=16.; seat 3 standing: expected 16, got 12; seat 3 recipe_score: expected 16, got 12; seat 3 final_total: expected 16, got 12
- scenario `R24 points can decide the winner over a higher recipe score` failed: rule R24 is broken: Final total = points + recipe_score, and the highest final total wins, with players tied at the top sharing the win.; seat 3 standing: expected 16, got 12; seat 3 recipe_score: expected 16, got 12; seat 3 final_total: expected 16, got 12
- what the game did on `R23 CT player ending with c=2,t=2 scores recipe 16`: moves played: r1 seat 1: 'Card'; r1 seat 2: 'Card'; r1 seat 3: 'Card'. First attribute changes: table deal_pick: '' -> 'CT'; seat 1 recipe: '' -> 'CT'; table recipe_deck: ['TL', 'LC', 'CT'] -> ['TL', 'LC']; table deal_pick: 'CT' -> 'TL'; seat 2 recipe: '' -> 'TL'; table recipe_deck: ['TL', 'LC'] -> ['LC']; table deal_pick: 'TL' -> 'LC'; seat 3 recipe: '' -> 'LC'; table recipe_deck: ['LC'] -> []; table card_pool: [] -> ['Tomato Fan', 'Lettuce Fan', 'Carrot Fan', 'Rainbow', 'Big Bowl', 'Balance']; seat 1 recipe: 'CT' -> 'TL'; seat 2 recipe: 'TL' -> 'LC'; seat 3 recipe: 'LC' -> 'CT'; seat 3 c: 0 -> 2 .... Final: players {"seat 1": {"recipe": "TL", "t": 0, "l": 0, "c": 0, "points": 0, "pick": "Card", "received": "nothing", "recipe_score": 0, "final_total": 0}, "seat 2": {"recipe": "LC", "t": 0, "l": 0, "c": 0, "points": 0, "pick": "Card", "received": "nothing", "recipe_score": 0, "final_total": 0}, "seat 3": {"recipe": "CT", "t": 2, "l": 0, "c": 2, "points": 0, "pick": "Card", "received": "nothing", "recipe_score": 12, "final_total":; table {"round": 12, "recipe_deck": [], "deal_pick": "LC", "card_pool": ["Tomato Fan", "Lettuce Fan", "Carrot Fan", "Rainbow", "Big Bowl", "Balance"], "current_card": "Big Bowl", "players": 3, "rounds": 12, "recipe_per_vegetable": 2, "recipe_pair_bonus": 2, "card_types": 6, "fan_per_vegetable": 2, "rainbow_per_set": 3, "big_bowl_per_vegetable": 1, "balance_bonus": 6, "balance_max_spread": 1, "balance_min_each": 1, "market_v
THE TESTS (written from the rules alone; judge whether they are right):
[
 {
  "name": "R1 setup: no turn played yet, every seat starts empty (recipes are hidden, so only the clean start is checked)",
  "rule": "R1",
  "players": 3,
  "rounds": 0,
  "rules": [
   {
    "seat": 1,
    "options_include": "Card",
    "times": "all"
   },
   {
    "seat": 2,
    "options_include": "Card",
    "times": "all"
   },
   {
    "seat": 3,
    "options_include": "Card",
    "times": "all"
   }
  ],
  "expect": {
   "game": {
    "round": 0
   },
   "players": {
    "1": {
     "t": 0,
     "l": 0,
     "c": 0,
     "points": 0
    },
    "2": {
     "t": 0,
     "l": 0,
     "c": 0,
     "points": 0
    },
    "3": {
     "t": 0,
     "l": 0,
     "c": 0,
     "points": 0
    }
   }
  },
  "rule_text": "At setup, each of the 3 players is dealt a different Recipe from TL, LC, CT, visible only to that player."
 },
 {
  "name": "R2 setup: every player has t=l=c=0 and points=0",
  "rule": "R2",
  "players": 3,
  "rounds": 0,
  "rules": [
   {
    "seat": 1,
    "options_include": "Card",
    "times": "all"
   },
   {
    "seat": 2,
    "options_include": "Card",
    "times": "all"
   },
   {
    "seat": 3,
    "options_include": "Card",
    "times": "all"
   }
  ],
  "expect": {
   "game": {
    "round": 0
   },
   "players": {
    "1": {
     "t": 0,
     "l": 0,
     "c": 0,
     "points": 0
    },
    "2": {
     "t": 0,
     "l": 0,
     "c": 0,
     "points": 0
    },
    "3": {
     "t": 0,
     "l": 0,
     "c": 0,
     "points": 0
    }
   }
  },
  "rule_text": "At setup, every player has t=0, l=0, c=0 and points=0."
 },
 {
  "name": "R3 a round draws a card and advances the round; all pick Card so the draw cannot change any score",
  "rule": "R3",
  "players": 3,
  "rounds": 1,
  "rules": [
   {
    "seat": 1,
    "options_include": "Card",
    "times": "all"
   },
   {
    "seat": 2,
    "options_include": "Card",
    "times": "all"
   },
   {
    "seat": 3,
    "options_include": "Card",
    "times": "all"
   }
  ],
  "expect": {
   "game": {
    "round": 1
   },
   "players": {
    "1": {
     "points": 0
    },
    "2": {
     "points": 0
    },
    "3": {
     "points": 0
    }
   }
  },
  "rule_text": "Each round, current_card is drawn at random with replacement from the 6 types Tomato Fan, Lettuce Fan, Carrot Fan, Rainbow, Big Bowl, Balance."
 },
 {
  "name": "R4 baskets and points carry through a round where everybody collides on Card",
  "rule": "R4",
  "players": 3,
  "rounds": 1,
  "given": {
   "players": {
    "1": {
     "t": 2,
     "l": 1,
     "c": 0,
     "points": 5
    },
    "2": {
     "t": 0,
     "l": 3,
  

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Point Salad is a 2-6 player card-drafting game. Each turn you take either one scoring-rule card or two vegetable cards from a shared market. At the end, every scoring card you hold is scored against your whole vegetable tableau, and the most points wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No simple policy wins. Always taking point cards leaves you with no vegetables to score them, and always taking vegetables leaves you with nothing to score with. Seat order matters slightly, and ties go to the later seat as compensation."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Matching cards to vegetables rewards skill. However, the draw order of 108 unique cards and the market refills add a lot of variance. With 4-6 players, what reaches you between turns is mostly out of your control."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Beginners still score points. Experts improve through hate-drafting, timing when to flip cards to vegetables, and reading the market."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "weak",
      "evidence": "All tableaus are face up and the market is public, so nothing about opponents is hidden except their intentions. The reasoning is mostly an optimisation over 108 different rule texts rather than inference."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Every card's score is arithmetic on vegetable counts."
    },
    {
      "criterion": "fits_platform",
      "verdict": "bad",
      "evidence": "108 unique scoring rules far exceed the attribute and step limits. Three piles with refill and pile-splitting is a long chain of deck operations. Sequential turns over about 18 rounds per player at 6 players are too long."
    }
  ],
  "problems": [
    "P1: 108 unique scoring rules and a three-pile market with refills and pile-splitting are far beyond the build limits.",
    "P2: There is nothing hidden. Every tableau is public, so there is no opponent type to infer.",
    "P3: Sequential drafting with random refills makes the luck of the flow large compared with skill, especially at higher player counts.",
    "P4 (previous variation): the recipe rule was ambiguous to the test writers. A CT basket with c=2, t=2 was expected to score 16, but the stated formula gives 2×2 + 2×2 + 2×min(2,2) = 12. The rules need an explicit formula with correct worked examples.",
    "P5 (previous variation): the build log showed recipes changing after the deal (each seat's recipe shifted to another). The rules did not state clearly that recipes are fixed once dealt, so the build invented a rotation.",
    "P6 (previous variation): the timing of card scoring (before or after this round's vegetables) and the collision outcomes were not pinned down tightly enough for exact tests."
  ],
  "changes": [
    {
      "what": "Replace the 108 cards with 6 public scoring-card types, one drawn at random each round with replacement: Tomato Fan, Lettuce Fan, Carrot Fan, Rainbow, Big Bowl, Balance. Each has a fixed arithmetic value.",
      "why": "This keeps the 'point card scored against your vegetables' idea within build limits.",
      "fixes": "P1"
    },
    {
      "what": "Give each player a hidden Recipe, a pair of two vegetables (TL, LC or CT), scored at game end as 2×first + 2×second + 2×min(first, second).",
      "why": "This creates one strong hidden element. Each recipe shares one vegetable with each rival, so inferring rivals' recipes from their picks decides where collisions happen.",
      "fixes": "P2"
    },
    {
      "what": "Replace sequential drafting with a simultaneous pick each round: Tomato, Lettuce, Carrot or Card. A vegetable gives 2 if you pick it alone, 1 each if two players pick it, and 0 if all three do. The Card goes only to a sole claimant, and colliding claimants get nothing.",
      "why": "The scarcity and contest of the market now come from reading opponents rather than from refill luck. The per-round random card is public and contestable by everyone.",
      "fixes": "P3"
    },
    {
      "what": "Write the recipe formula once, exactly, with checked worked examples: CT with c=2, t=2 scores 12; CT with c=3, t=2 scores 14; TL with t=4, l=1 scores 12.",
      "why": "Tests and the build must agree on the arithmetic.",
      "fixes": "P4"
    },
    {
      "what": "State that recipes are dealt once at setup, one from each of TL, LC and CT, and never change, pass or rotate.",
      "why": "This removes the build's invented recipe rotation.",
      "fixes": "P5"
    },
    {
      "what": "Fix the timing and collisions exactly. The Card's value is computed from the claimant's basket as it stood at the start of the round, before this round's vegetables are added. Card collisions give nothing. All picks and baskets are announced after resolution.",
      "why": "This makes every outcome a deterministic function of picks, the drawn card and prior state.",
      "fixes": "P6"
    },
    {
      "what": "Add one simultaneous message per player before each pick.",
      "why": "Players can bluff their recipe, propose a vegetable split or warn off a Card. Only one player can win, so following a proposal can cost you. This is genuine reasoning about trust.",
      "fixes": "P2"
    }
  ],
  "keeps": [
    "The central choice each turn: take a point card OR take vegetables.",
    "Point cards are scored by arithmetic on your own vegetable tableau, and the same vegetable counts for many cards.",
    "Card types modelled on originals: per-vegetable fans, a set-collection Rainbow, a count-everything Big Bowl and an even-spread Balance.",
    "Public vegetable tableaus.",
    "Hate-drafting a card a rival wants.",
    "Most points wins."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The draft-card-or-vegetables tension survives compression into six card types plus a hidden recipe. Simultaneous picks turn it into an opponent-modelling game within the limits."
  },
  "variation": {
    "name": "Point Salad: Secret Recipes",
    "summary": "Three players draft vegetables and point cards for 12 rounds with simultaneous picks. Each player holds a hidden two-vegetable Recipe. Players must read rivals' recipes to avoid fighting over the same vegetables, and must decide when to contest the round's point card.",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "rules": "VEGETABLES: Tomato (t), Lettuce (l), Carrot (c).\n\nSETUP\n1. There are exactly 3 players.\n2. Recipes:\n- There are 3 Recipe tiles: TL (tomato and lettuce), LC (lettuce and carrot) and CT (carrot and tomato).\n- Shuffle them and deal one to each player, so all three are used.\n- Each player sees only their own Recipe.\n- A Recipe never changes, moves or rotates for the rest of the game.\n3. Every player starts with t=0, l=0, c=0 and points=0. Baskets (t, l, c) and points are public at all times. Recipes are secret until game end.\n\nEACH ROUND (12 rounds)\n1. Draw the card: one scoring card type is drawn at random, with replacement, equally likely from these 6. It is announced to everyone.\n- Tomato Fan: worth 2 × t.\n- Lettuce Fan: worth 2 × l.\n- Carrot Fan: worth 2 × c.\n- Rainbow: worth 3 × min(t, l, c).\n- Big Bowl: worth 1 × (t + l + c).\n- Balance: worth 6 if t ≥ 1, l ≥ 1, c ≥ 1 and max(t,l,c) − min(t,l,c) ≤ 1; otherwise 0.\n2. Talk:\n- Every player writes one short message at the same time, without seeing the others.\n- All messages are then shown to everyone.\n- Messages bind no one.\n3. Pick: every player at the same moment chooses exactly one of Tomato, Lettuce, Carrot, Card.\n4. Resolve the Card:\n- If exactly one player chose Card, that player gains points equal to the drawn card's value, computed from their basket as it stood at the start of this round.\n- If zero players, or two or more players, chose Card, nobody gains anything from it. The card is discarded and colliding players receive nothing this round.\n5. Resolve vegetables, separately for each vegetable:\n- If exactly 1 player chose it, that player adds 2 of it to their basket.\n- If exactly 2 players chose it, each adds 1.\n- If all 3 chose it, nobody gets any.\n6. Announce: everyone's pick, what each received, and all baskets and points.\n7. If 12 rounds have been played, go to END. Otherwise start the next round.\n\nEND\n1. Each player's Recipe is revealed and scored. With first and second as that player's counts of the Recipe's two vegetables:\nrecipe_score = 2 × first + 2 × second + 2 × min(first, second).\nThe third vegetable scores nothing in the Recipe.\n- TL uses t and l.\n- LC uses l and c.\n- CT uses c and t.\n2. Worked examples (exact):\n- CT with c=2, t=2: 4 + 4 + 4 = 12.\n- CT with c=3, t=2: 6 + 4 + 4 = 14.\n- TL with t=4, l=1: 8 + 2 + 2 = 12.\n- LC with l=0, c=6: 0 + 12 + 0 = 12.\n3. final_total = points + recipe_score.\n4. Example of points deciding the game: a player with points=10 and recipe 12 (final 22) beats a player with points=0 and recipe 14 (final 14).\n\nCARD EXAMPLE: A player starting a round with t=3, l=1, c=2 who is the sole Card claimant scores:\n- Tomato Fan: 6\n- Lettuce Fan: 2\n- Carrot Fan: 4\n- Rainbow: 3\n- Big Bowl: 6\n- Balance: 0 (spread 2 > 1)",
    "objective": "After round 12, the player with the highest final_total (points + recipe_score) wins. If two or three players tie for the highest final_total, the game is a draw among them.",
    "expected_effect": "Simple policies all lose.\n- Always Card scores 0, because the card values come from an empty basket.\n- Always one vegetable caps the recipe at 2 × first, with min = 0. Even uncontested, that is 48 against about 72 for an uncontested balanced pair.\n- Random play wastes picks on the useless third vegetable and on Card collisions.\n\nWhat the players disagree about:\n- Every recipe shares one vegetable with each rival, so players fight over who gets the shared vegetables.\n- Players also fight over who claims a valuable late card. A Big Bowl or Fan worth 15-25 points in rounds 9-12 creates a chicken game.\n\nWhat talk is for:\n- Bluffing a recipe, offering a split ('I'll stay off carrots') or threatening to contest a card.\n- A player who trusts a split while the speaker defects ends up colliding for 1 instead of 2, or loses the card.\n\nWhat good play needs: inferring recipes from early picks, planning basket growth so cards claimed later are worth more, and predicting who will contest the card. The random card is public and open to all, and the recipes are symmetric, so neither is a lottery."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 12,
    "choice_steps_per_round": 2,
    "attributes": 17,
    "hidden_elements": 1,
    "random_draws_per_round": 1,
    "rounds": 12
  }
}
```
````
