# 17 design

- time: 2026-10-28T04:27:47+00:00 (67.8s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 56cfe85d7da1e30e, reply sha256 1e8813bee957690c

## Sent

````
Original game: Go Nuts for Donuts
Players in the original: 2 to 6

Original rules:
Set up a row of N+1 face-up donut cards where N is player count, numbered 1 to N+1 left to right, from a shuffled deck filtered by player count. Each player holds selection cards 1 to N+1. Each round all players secretly choose a row position and reveal simultaneously. Resolve positions in ascending order: if two or more players chose the same number, that donut is discarded with no one getting it. If exactly one player chose it, that player takes it face-up to their score pile. Some donuts are action cards that trigger immediately when taken from the row in number order, letting you steal, draw, or manipulate cards; powers do not trigger when gained other ways. After resolving, refill empty row spots in order from the deck and return selection cards to hands. Continue until the deck cannot fully refill the row, then total points on collected donuts. Most points wins, tie-break most cards.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
Fix the secret-split resolution so that each player's answer G sets glazed_picks = G and jelly_picks = premium_picks_total - G exactly once, and nothing later in setup or round 1 resets them. Look for a second operation that is overwriting the values. It may be a default or fallback that treats the answer as 0, an unconditional 'glazed_picks = 0, jelly_picks = premium_picks_total' step, or a step that reads the wrong attribute or the wrong player instead of split_g. Store the answer in split_g, compute both picks from split_g after the poll, and keep them private. Then check the following: void is true only for Glazed with glazed_picks == 0 or Jelly with jelly_picks == 0. A void choice is left out of the per-donut counts. A lone non-void chooser gains the donut's value and donuts += donut_collected_increment. Every non-void Glazed or Jelly choice decrements its picks and increments glazed_used or jelly_used, whether the donut was won or discarded.
the game was built and works on the platform, but it does not behave as the independent tests say the rules require:
- scenario `Glazed with 0 Glazed picks and Jelly with 0 Jelly picks are void; Glazed with picks is not` failed: rule R7 is broken: When a player chooses Glazed with glazed_picks == 0, or Jelly with jelly_picks == 0, then void = true. Otherwise void = false.; seat 2 void: expected True, got False; seat 2 score: expected 0, got 6; seat 3 void: expected False, got True; seat 3 score: expected 9, got 0; seat 3 do
- scenario `A void Jelly gains 0, uses no pick and does not collide with a real Jelly` failed: rule R8 is broken: When a choice is void, that player gains 0, uses no pick, and is not counted as choosing that donut.; seat 1 void: expected True, got False; seat 1 jelly_used: expected 0, got 1; seat 2 score: expected 6, got 0; seat 2 donuts: expected 1, got 0
- scenario `A lone Glazed chooser gains 9 and one donut` failed: rule R10 is broken: When exactly one non-void player chooses Glazed, that player gains 9 points and donuts += 1.; seat 1 score: expected 9, got 0; seat 1 donuts: expected 1, got 0
- scenario `A discarded non-void Glazed still uses a pick` failed: rule R16 is broken: When a player makes a non-void Glazed choice, glazed_picks decreases by 1 and glazed_used increases by 1, whether the donut was won or discarded.; seat 1 glazed_used: expected 3, got 2; seat 1 void: expected False, got True; seat 2 glazed_used: expected 1, got 0; seat 2 void: exp
- what the game did on `Glazed with 0 Glazed picks and Jelly with 0 Jelly picks are void; Glazed with picks is not`: moves played: r1 seat 1: 0; r1 seat 2: 0; r1 seat 3: 0; r1 seat 4: 0; r1 seat 1: 'Glazed'; r1 seat 2: 'Jelly'; r1 seat 3: 'Glazed'; r1 seat 4: 'Plain'. First attribute changes: seat 1 choice: '' -> 'none yet'; seat 2 choice: '' -> 'none yet'; seat 3 choice: '' -> 'none yet'; seat 4 choice: '' -> 'none yet'; seat 1 jelly_picks: 0 -> 6; seat 2 glazed_picks: 0 -> 6; seat 3 glazed_picks: 0 -> 2; seat 3 jelly_picks: 0 -> 4; seat 2 glazed_picks: 6 -> 0; seat 3 glazed_picks: 2 -> 0; seat 2 jelly_picks: 0 -> 6; seat 3 jelly_picks: 4 -> 6; seat 4 jelly_picks: 0 -> 6; table round: 0 -> 1 .... Final: players {"seat 1": {"score": 0, "donuts": 0, "glazed_picks": 0, "jelly_picks": 6, "glazed_used": 0, "jelly_used": 0, "choice": "Glazed", "void": true, "gain": 0, "split_g": 0, "shown": "Glazed (VOID)"}, "seat 2": {"score": 6, "donuts": 1, "glazed_picks": 0, "jelly_picks": 5, "glazed_used": 0, "jelly_used": 1, "choice": "Jelly", "void": false, "gain": 6, "split_g": 0, "shown": "Jelly"}, "seat 3": {"score": 0, "donuts": 0, "gl; table {"round": 1, "player_count": 4, "rounds": 10, "glazed_value": 9, "jelly_value": 6, "cruller_value": 4, "sprinkle_value": 2, "plain_value": 1, "premium_picks_total": 6, "split_min": 0, "split_max": 6, "lone_chooser_count": 1, "donut_collected_increment": 1, "pick_use_per_choice": 1, "tiebreak_multiplier": 100}
THE TESTS (written from the rules alone; judge whether they are right):
[
 {
  "name": "Every seat starts at 0: after one round with no Glazed or Jelly, totals equal only that round's gains",
  "rule": "R1",
  "players": 4,
  "seed": 1,
  "rounds": 1,
  "default": "last",
  "rules": [
   {
    "seat": 1,
    "options_include": "Cruller"
   },
   {
    "seat": 2,
    "options_include": "Sprinkle"
   },
   {
    "seat": 3,
    "options_include": "Plain"
   },
   {
    "seat": 4,
    "options_include": "Plain"
   }
  ],
  "expect": {
   "players": {
    "1": {
     "score": 4,
     "donuts": 1,
     "glazed_used": 0,
     "jelly_used": 0
    },
    "2": {
     "score": 2,
     "donuts": 1,
     "glazed_used": 0,
     "jelly_used": 0
    },
    "3": {
     "score": 0,
     "donuts": 0,
     "glazed_used": 0,
     "jelly_used": 0
    },
    "4": {
     "score": 0,
     "donuts": 0,
     "glazed_used": 0,
     "jelly_used": 0
    }
   },
   "game": {
    "round": 1
   }
  },
  "rule_text": "When the game starts, every player has score 0, donuts 0, glazed_used 0 and jelly_used 0."
 },
 {
  "name": "A split of G=3 gives Glazed picks, so a lone Glazed choice is not void and scores 9",
  "rule": "R2",
  "players": 4,
  "seed": 1,
  "rounds": 1,
  "default": "last",
  "rules": [
   {
    "seat": 1,
    "options_include": 3
   },
   {
    "seat": 1,
    "options_include": "Glazed"
   },
   {
    "seat": 2,
    "options_include": "Cruller"
   },
   {
    "seat": 3,
    "options_include": "Sprinkle"
   },
   {
    "seat": 4,
    "options_include": "Plain"
   }
  ],
  "expect": {
   "players": {
    "1": {
     "void": false,
     "score": 9,
     "donuts": 1,
     "glazed_used": 1,
     "jelly_used": 0
    },
    "2": {
     "score": 4,
     "donuts": 1
    },
    "3": {
     "score": 2,
     "donuts": 1
    },
    "4": {
     "score": 1,
     "donuts": 1
    }
   }
  },
  "rule_text": "When a player answers G (a whole number from 0 to 6) before round 1, then glazed_picks = G and jelly_picks = 6 - G, visible only to that player."
 },
 {
  "name": "A split of G=0 leaves no Glazed picks, so a Glazed choice is void",
  "rule": "R2",
  "players": 4,
  "seed": 1,
  "rounds": 1,
  "default": "last",
  "rules": [
   {
    "seat": 1,
    "options_include": 0
   },
   {
    "seat": 1,
    "options_include": "Glazed"
   },
   {
    "seat": 2,
    "options_include": "Cruller"
   },
   {
    "seat": 3,
    "options_include": "Sprinkle"
   },
   {
    "seat": 4,
    "options_include": "Plain"
   }
  ],
  "expect": {
   "players": {
    "1": {
     "void": true,
     "score": 0,
     "donuts": 0,
     "glazed_used": 0
    },
    "2": {
     "score": 4


Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Go Nuts for Donuts is a 2-6 player simultaneous-selection game. Each round every player secretly picks one of N+1 face-up donuts. A donut chosen by exactly one player goes to that player, and a donut chosen by two or more is discarded. Some donuts carry action powers, and the most points when the deck runs out wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "Neither 'always the top donut' nor 'always the cheapest' is safe, because two players on the same card both get nothing. No seat moves first, since the reveal is simultaneous. Choices decide every allocation."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "The shuffled deck decides which donuts appear and when. Action cards (steal, draw) add swingy luck. Most rounds are an anti-coordination guess in which a good reader gains a modest edge over many rounds."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Reading which donut rivals will crowd onto and taking the uncontested one keeps rewarding improvement. A weak player still picks up leftovers."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "weak",
      "evidence": "The core is predicting rivals' simultaneous picks, which is genuine opponent modelling. However, everything on the table is face-up and scores are public, so there is no private state to infer. Card-specific powers and set scoring reward rules knowledge more than inference."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Allocation and scoring are pure counting: lone chooser takes the card, and points are summed."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "Simultaneous polls fit. A shuffled deck with refills, many distinct card powers (steal, draw, manipulate) and set-based values would blow past the step and attribute limits."
    }
  ],
  "problems": [
    "Too many distinct card powers and set rules to build within 20 steps and 20 attributes.",
    "A shuffled deck makes the offer each round random, adding luck without adding reasoning.",
    "No hidden information: the table and scores are fully public, so opponent modelling has little to work from beyond history.",
    "BUILD FAILURE in the previous variation: the secret split was overwritten after the poll. Every seat ended with glazed_picks 0 and jelly_picks 6, which broke the void test (R7), the void-collision rule (R8), the lone-Glazed payout (R10) and the pick accounting (R16). The cause was a second, unconditional step that reset the stored picks. Storing two mutable pick counters derived from the answer invited exactly this overwrite.",
    "The previous variation carried redundant table constants (lone_chooser_count, donut_collected_increment, pick_use_per_choice) that added attributes and places for the builder to go wrong."
  ],
  "changes": [
    {
      "what": "A fixed row of five donuts every round: Glazed 9, Jelly 6, Cruller 4, Sprinkle 2, Plain 1. There are no action cards and no deck.",
      "why": "Keeps the 'pick one of N+1, collisions discard' core while fitting the limits. Removing the random offer means skill, not the shuffle, decides the game.",
      "fixes": "Too many distinct card powers and set rules to build within 20 steps and 20 attributes."
    },
    {
      "what": "No random draws at all: the same five donuts are offered in all 10 rounds.",
      "why": "Luck no longer swamps reading opponents.",
      "fixes": "A shuffled deck makes the offer each round random, adding luck without adding reasoning."
    },
    {
      "what": "Each player has 6 premium picks for the whole game, the only way to choose Glazed or Jelly. Before round 1 each player secretly sets how many are Glazed (G). The rest (6 - G) are Jelly. Players see each other's choices each round but never each other's G.",
      "why": "Creates one strong hidden element. Players must infer from rivals' play how many Glazed or Jelly picks each still holds, and plan their own budget over 10 rounds.",
      "fixes": "No hidden information: the table and scores are fully public, so opponent modelling has little to work from beyond history."
    },
    {
      "what": "Store only the answer split_g plus the counters glazed_used and jelly_used. There are no glazed_picks or jelly_picks attributes. A Glazed choice is void exactly when glazed_used >= split_g, and a Jelly choice is void exactly when jelly_used >= 6 - split_g. split_g is written once by the setup poll, and no other step ever writes it. glazed_used and jelly_used start at 0 and only ever increase by 1 on a non-void choice of that donut. The setup poll offers exactly the options 0 to 6, so there is no default or fallback value.",
      "why": "The overwritten-picks bug came from a second operation resetting derived counters. With nothing derived stored, nothing remains to reset. Void is computed directly from the answer and the usage counters.",
      "fixes": "BUILD FAILURE in the previous variation: the secret split was overwritten after the poll. Every seat ended with glazed_picks 0 and jelly_picks 6, which broke the void test (R7), the void-collision rule (R8), the lone-Glazed payout (R10) and the pick accounting (R16). The cause was a second, unconditional step that reset the stored picks. Storing two mutable pick counters derived from the answer invited exactly this overwrite."
    },
    {
      "what": "Drop the table constants lone_chooser_count, donut_collected_increment and pick_use_per_choice. Write the literal numbers (1) into the rules.",
      "why": "Fewer attributes and fewer indirections for the builder to misread.",
      "fixes": "The previous variation carried redundant table constants (lone_chooser_count, donut_collected_increment, pick_use_per_choice) that added attributes and places for the builder to go wrong."
    },
    {
      "what": "Add one simultaneous message per player before each round's choice.",
      "why": "Lets players claim, bluff about remaining picks and try to steer rivals off a donut. Interests conflict because only one player can take each donut and only one player wins.",
      "fixes": "No hidden information: the table and scores are fully public, so opponent modelling has little to work from beyond history."
    }
  ],
  "keeps": [
    "Simultaneous secret selection of one donut from a row of N+1.",
    "A donut chosen by exactly one player is taken. A donut chosen by two or more is discarded and nobody gets it.",
    "Donuts of different point values, with the most points winning and more donuts as the tie-break.",
    "The bluffing and second-guessing of 'will they all go for the big one?'"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The collision-discard selection is a clean anti-coordination game that rewards opponent modelling. With a fixed row, a hidden premium-pick split and simplified bookkeeping, it fits the limits and removes the earlier build bug."
  },
  "variation": {
    "name": "Go Nuts for Donuts: Secret Budget",
    "summary": "Four players pick donuts simultaneously for 10 rounds from a fixed row of five, and any donut picked by two or more players is discarded. The two best donuts, Glazed and Jelly, need limited premium picks. Each player secretly divides those picks between Glazed and Jelly at the start, so reading rivals' hidden budgets is the key skill.",
    "players": {
      "min": 4,
      "max": 4,
      "suggested": 4
    },
    "rules": "PLAYERS AND DONUTS. Exactly 4 players. Every round the same five donuts are offered: Glazed (9 points), Jelly (6 points), Cruller (4 points), Sprinkle (2 points), Plain (1 point). There are no cards, deck or random events.\n\nSTARTING STATE. Every player starts with score 0, donuts 0, glazed_used 0, jelly_used 0. The game lasts exactly 10 rounds.\n\nSECRET SPLIT (once, before round 1). Each player has 6 premium picks for the whole game. All players are asked at the same time: 'How many of your 6 premium picks are Glazed picks?' The options are exactly the whole numbers 0, 1, 2, 3, 4, 5, 6. The answer is stored as that player's split_g and is visible only to that player. That player then has split_g Glazed picks and (6 - split_g) Jelly picks. split_g is set by this poll only and is never changed by any later step. No step resets glazed_used or jelly_used except as stated below.\n\nEACH ROUND:\n1. TALK. Every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Messages bind no one.\n2. CHOOSE. All players choose at the same time one of: Glazed, Jelly, Cruller, Sprinkle, Plain. Before choosing, each player is privately reminded of their own Glazed picks left (split_g - glazed_used) and Jelly picks left (6 - split_g - jelly_used).\n3. VOID CHECK. A player's choice is void if and only if (a) they chose Glazed and glazed_used >= split_g, or (b) they chose Jelly and jelly_used >= 6 - split_g. Every other choice is not void. Cruller, Sprinkle and Plain are never void.\n4. COUNT. For each donut, count how many players made a NON-VOID choice of it. Void choices are not counted for any donut.\n5. AWARD. For each donut, if exactly 1 player made a non-void choice of it, that player adds the donut's points to their score and adds 1 to donuts. If 2 or more players made a non-void choice of it, it is discarded and none of them gains anything for it. A void choice gains 0.\n6. USE PICKS. Every player who made a non-void Glazed choice adds 1 to glazed_used. Every player who made a non-void Jelly choice adds 1 to jelly_used. This happens whether the donut was won or discarded. A void choice uses nothing.\n7. REVEAL. Everyone is shown every player's choice (marked VOID if void), what each player gained this round, and all scores and donut counts. Nobody's split_g is ever shown.\n8. END CHECK. After round 10 the game ends.",
    "objective": "After round 10, the player with the highest score wins. If several are tied on score, the one among them with the most donuts wins (rank value = score x 100 + donuts). If players are still tied on both, the game is a draw among them.",
    "expected_effect": "Players must budget 6 premium picks across 10 rounds and guess when rivals will spend theirs. Each rival's Glazed/Jelly split is hidden but can be inferred from what they have chosen and when their choices turned VOID. Crowding the Glazed donut wastes picks, while slipping into an uncontested Jelly or Cruller pays.\n\nTalk passes both tests. Players disagree because each donut can go to only one player and only one player wins. A message like 'I'm taking Glazed, take Jelly' is self-serving, and a player who follows it may hand the speaker 9 points while burning a Jelly pick on a collision. Players can also bluff about their remaining Glazed picks to scare rivals off.\n\nSimple policies all lose to readers:\n- Always Glazed (split 6) collides with anyone else doing it and is void for the last 4 rounds.\n- Always Cruller earns 0 once anyone contests it.\n- Always Plain caps at 10 points.\n- Random play scatters picks into collisions.\n\nThe game has no luck and no seat order, so reading rivals decides it."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 14,
    "choice_steps_per_round": 2,
    "attributes": 17,
    "hidden_elements": 1,
    "random_draws_per_round": 0,
    "rounds": 10
  }
}
```
````
