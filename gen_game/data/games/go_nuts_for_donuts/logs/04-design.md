# 04 design

- time: 2026-10-28T04:13:53+00:00 (271.4s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 fbe79dd6cf0b1ec4, reply sha256 4c2bafd880e9eae3

## Sent

````
Original game: Go Nuts for Donuts
Players in the original: 2 to 6

Original rules:
Set up a row of N+1 face-up donut cards where N is player count, numbered 1 to N+1 left to right, from a shuffled deck filtered by player count. Each player holds selection cards 1 to N+1. Each round all players secretly choose a row position and reveal simultaneously. Resolve positions in ascending order: if two or more players chose the same number, that donut is discarded with no one getting it. If exactly one player chose it, that player takes it face-up to their score pile. Some donuts are action cards that trigger immediately when taken from the row in number order, letting you steal, draw, or manipulate cards; powers do not trigger when gained other ways. After resolving, refill empty row spots in order from the deck and return selection cards to hands. Continue until the deck cannot fully refill the row, then total points on collected donuts. Most points wins, tie-break most cards.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- balanced FAILED: The rotation does nothing. Every round's values are announced publicly before anyone chooses (step 1), so choosing 'position k' is just choosing a value from {9,7,5,3,1}. All 10 rounds are therefore the same one-shot game: 4 players pick from 5 values, and only a value picked by exactly one player scores. Seats are symmetric and move order gives no edge.

Thoughtless policy 'always take the 9' (whatever position it sits in):

(a) Against 3 uniformly random players.
- The 9 is uncontested with probability (4/5)^3 = 0.512, so the always-9 player expects about 0.512 x 9 = 4.6 per round, or 46 over the game.
- A random player scores 0 whenever it picks the 9. Otherwise its value must avoid the 2 other random players: P = 0.8^2 = 0.64.
- Its expectation is (7+5+3+1)/5 x 0.64 = 2.05 per round, or about 20 over the game.
- Always-9 wins almost every game.

(b) Against sensible players who see the commitment (stated in talk, or plain after round 1). Per-round payoff for an opponent who responds:

| Opponent's choice | Opponent's gain | Always-9's gain |
|---|---|---|
| Also takes 9 | 0 | 0 |
| Takes uncontested 7 | 7 | 9 |
| Takes uncontested 5 / 3 / 1 | 5 / 3 / 1 | 9 |

- The myopic best response is to leave the 9 alone, so the committer gets 90.
- The best any other player can do is 70, and only if both remaining players also avoid the 7.
- Blocking the committer costs the blocker 0 that round and hands the relative gain to the other two players. A lone spiteful blocker therefore falls behind them and does not win either.
- Always-9 loses only when someone repeatedly self-sacrifices, or draws when everyone plays always-9 (all on 0).

This is a commitment/chicken game in which the stubborn thoughtless policy wins or draws in nearly every realistic line. There is no budget, carry-over or cost that ever makes the 9 a bad long-run choice. Talk is non-binding and is used only to announce the commitment. There is no cooperative structure to reward: four players wanting the same top prize is pure conflict.
- reasoning_over_luck FAILED: No random draw exists, so chance is not formally a factor. However, there is almost nothing to reason about.
- The rotation is a fully public relabelling: it gives no inference and no planning. Round 7 is strategically identical to round 1.
- There is no state linking rounds (no budgets, no depletion, no hidden values). Planning over rounds is therefore impossible, and 'opponent modelling' reduces to guessing who will be stubborn about the 9.

When everyone plays the intended good strategy, there are two possible outcomes:
- Everyone plays the symmetric mixed equilibrium of the one-shot 4-player/5-value anti-coordination game. Collisions then fall out of the players' randomisation, totals are close, and the winner is effectively decided by which mixed picks happened to land uncontested. That is luck in all but name.
- One player commits loudly to the 9 and wins. That rewards bluster, not inference.

A well-reasoning player is not clearly favoured over one who simply always takes the 9.
- change: Add state that links the rounds so planning and inference matter. For example: each player may choose each value at most twice across the 10 rounds (exactly two uses of each of 9/7/5/3/1). Remaining uses are tracked as public attributes, so players must plan their timing and infer when opponents will spend their 9s. This removes the always-9 policy outright.
- change: Either drop the rotating-row schedule or make position meaningful. One option: some values are private per player (private_values), so a player's best target differs and must be inferred from talk and past picks. Another option: one hidden element, such as a secret bonus value per player revealed at the end.
- change: Recheck balance after the change. Show that no fixed spending order of the value budget (for example all 9s first, or all 9s last) wins or draws almost every game against random and sensible opponents.
- change: Resolve the hidden_elements inconsistency: either state that it counts the sealed simultaneous choice, or set it to 0.
The variation that was reviewed: Go Nuts for Donuts: Rotating Row: SETUP: There are exactly 4 players. Each starts with 0 points. There are no hidden cards or types.

THE DONUTS: Five donuts are worth 9, 7, 5, 3 and 1 points, the same to every player. They sit in a face-up row of positions 1 to 5. Their arrangement changes each round on a fixed public schedule, shown to everyone at the start of the game:
- Rounds 1 and 6: positions 1-5 are worth 9, 7, 5, 3, 1
- Rounds 2 and 7: positions 1-5 are worth 7, 5, 3, 1, 9
- Rounds 3 and 8: positions 1-5 are worth 5, 3, 1, 9, 7
- Rounds 4 and 9: positions 1-5 are worth 3, 1, 9, 7, 5
- Rounds 5 and 10: positions 1-5 are worth 1, 9, 7, 5, 3
Each round, every value moves one position to the left, and the value in position 1 wraps to position 5.

EACH ROUND (10 rounds):
1. ANNOUNCE ROW: The round number and the values of positions 1 to 5 for this round are announced.
2. TALK: Every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Messages are not binding.
3. CHOOSE: Every player secretly and simultaneously chooses one position from 1 to 5.
4. REVEAL: All four choices are revealed together.
5. RESOLVE: For each position, if exactly one player chose it, that player gains its value this round. If two or more players chose it, the donut is discarded and none of them gains anything. A position nobody chose has no effect.
6. SCORE: Each player's gain this round and everyone's new total are announced.

END: After round 10 the game ends. Winner: The player with the highest point total after round 10 wins. If two or more players tie for the highest total, the game is a draw among those tied players.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Go Nuts for Donuts is a 2-6 player game. A face-up row of N+1 donut cards is dealt from a shuffled deck, and every round each player secretly picks a row position. A donut picked by exactly one player goes to that player; a donut picked by two or more is discarded. Some donuts carry action powers (steal, draw, manipulate). The game ends when the deck cannot refill the row, and the most points wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "weak",
      "evidence": "Seats are symmetric and the sealed picks are simultaneous, so no seat has an edge. The core is a chicken game over the most valuable donut, and nothing limits how often a player can go for it. A stubborn 'always pick the best donut' player wins whenever rivals give way, because blocking costs the blocker as much as the target and hands the gain to the bystanders. The previous variation showed exactly this: always-9 scored about 46 against random play and about 90 against rivals who gave way."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "The shuffled deck decides which values appear each round, and the action cards (steal, draw) swing totals by luck of timing. Among equally careful players, mixed picks over a random row largely decide who ends up uncontested."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Predicting which donut each rival will chase, and using action cards well, gives a strong player something to improve on. A weak player still collects uncontested donuts."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "weak",
      "evidence": "The row is face-up and nothing links rounds except the deck running down. The only thing to infer is the rivals' simultaneous pick, so there is no hidden state to deduce and no resource to plan with. The previous variation's rotating row was a public relabelling: round 7 was strategically identical to round 1."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Points on collected donuts are summed and the tie-break is a card count, all plain arithmetic."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "It is turn-based and text-only. However, a deck filtered by player count, refills and many distinct action-card powers need far more steps and rules than the limits allow, and the action-card powers are mostly luck."
    }
  ],
  "problems": [
    "P1: Chicken over the top donut. Nothing limits how often a player can chase the best donut, so a stubborn always-best policy wins or draws against sensible rivals, because blocking it is self-harm that helps the bystanders.",
    "P2: No state links the rounds. There is no budget or resource to plan with, so every round is the same one-shot game and multi-round planning is impossible.",
    "P3: Nothing hidden to infer. Apart from the sealed pick everything is public, and the previous rotating row was a pure relabelling.",
    "P4: Luck from the shuffled deck and from action-card powers decides much of the outcome among careful players.",
    "P5: Action cards, deck filtering and refills exceed the platform's step and complexity limits.",
    "P6: Cooperative-draw risk. If players can agree a schedule in which everyone scores the same, talk produces a stable four-way draw and the interesting choice disappears.",
    "P7: The previous variation's complexity report was inconsistent about hidden elements."
  ],
  "changes": [
    {
      "what": "Premium picks: each player has exactly 6 premium picks for the whole game. A premium pick is needed to choose the Glazed (9) or the Jelly (6). The three lower donuts can be chosen without limit. A premium choice uses up its pick whether it scores or collides. A premium choice with no matching pick left is void: it scores 0 and blocks nobody.",
      "why": "Always-best can now only chase the Glazed 6 times. If it does so early, rivals can spend a few of their oversupplied picks contesting it, which cheaply drains it. There are 24 premium picks against only 20 premium donuts, so burning one to block is no longer pure self-harm.",
      "fixes": "P1: Chicken over the top donut."
    },
    {
      "what": "The budget is spent over 10 fixed rounds, and every player's premium uses so far are announced each round.",
      "why": "Timing now matters: when to spend premium picks, when to let a rival burn theirs, and whether to save picks for the final rounds.",
      "fixes": "P2: No state links the rounds."
    },
    {
      "what": "Secret split: at setup each player privately writes how many of their 6 premium picks are Glazed picks (0 to 6). The rest are Jelly picks. The split is never announced; only uses are visible.",
      "why": "This is one strong hidden element, chosen by the player rather than dealt, so it is not a lottery. Rivals must infer from play and from talk who can still take the Glazed late, and bluffing about remaining picks becomes possible. It is also a Blotto-like guess: if everyone loads up on Glazed, the Jelly goes cheap.",
      "fixes": "P3: Nothing hidden to infer."
    },
    {
      "what": "Remove the deck, the action cards and the rotation. The row is the same five donuts every round: 9, 6, 4, 2, 1.",
      "why": "This removes draw luck and power-card swings and fits the step limits. What varies between rounds is each player's budget, not the row.",
      "fixes": "P4: Luck from the deck and action cards; P5: Exceeds the platform's limits."
    },
    {
      "what": "The values 9, 6, 4, 2 and 1 are chosen so that a stable collision-free round yields 21 points. Over 10 rounds that is 210, which cannot be split equally among 4 players.",
      "why": "Leaving any donut but the Plain untaken is unstable: whoever took a lower donut gains by switching to the untaken one. A stable perfect schedule therefore leaves only the Plain untaken each round, totalling 210, which is not divisible by 4. Someone must end ahead, so trailing players always have a reason to contest.",
      "fixes": "P6: Cooperative-draw risk."
    },
    {
      "what": "Report the complexity consistently: 2 hidden elements (the secret split, and the sealed simultaneous choice), and 0 random draws.",
      "why": "This corrects the earlier inconsistency.",
      "fixes": "P7: Inconsistent complexity report."
    }
  ],
  "keeps": [
    "Everyone secretly picks a donut from a face-up row at the same moment.",
    "A donut picked by exactly one player scores for them; a donut picked by two or more is discarded and nobody scores it.",
    "The row has N+1 donuts for N players (5 donuts for 4 players), so one donut always goes untaken.",
    "Most points wins, with the original tie-break of most donuts collected."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The sealed anti-coordination pick is a good strategic core. A limited, secretly split premium budget and an unequal-splitting payoff fix the chicken problem and the lack of planning inside the platform's limits."
  },
  "variation": {
    "name": "Go Nuts for Donuts: Premium Picks",
    "summary": "Four players pick donuts from the same row of five each round, and a donut picked by two or more is lost. The two best donuts can only be chosen with premium picks: 6 per player, split secretly between Glazed and Jelly at the start. Players talk, bluff about what they have left, and time their premium picks over 10 rounds.",
    "players": {
      "min": 4,
      "max": 4,
      "suggested": 4
    },
    "rules": "SETUP: There are exactly 4 players, each starting with 0 points and 0 donuts collected.\n\nTHE ROW: Every round the same five donuts are offered:\n- Glazed, worth 9 points\n- Jelly, worth 6 points\n- Cruller, worth 4 points\n- Sprinkle, worth 2 points\n- Plain, worth 1 point\n\nSECRET SPLIT: Before round 1, each player privately and simultaneously writes a whole number G from 0 to 6. That player has G Glazed picks and 6 minus G Jelly picks. Nobody else is told this number, at any time during the game.\n\nEACH ROUND (10 rounds):\n1. ANNOUNCE: The round number is announced, along with, for every player, their points, how many donuts they have collected, and how many Glazed choices and how many Jelly choices they have made so far that used a pick. Remaining picks are not announced.\n2. TALK: Every player writes one short message at the same time, without seeing the others. All four messages are then shown to everyone. Messages are not binding.\n3. CHOOSE: Every player secretly and simultaneously chooses exactly one donut: Glazed, Jelly, Cruller, Sprinkle or Plain.\n4. CHECK PICKS: A player who chose Glazed with no Glazed picks left, or Jelly with no Jelly picks left, has made a VOID choice. A void choice scores nothing, uses no pick, and does not count as choosing that donut for anyone else.\n5. REVEAL: All four choices are revealed together, with any void choice marked VOID.\n6. RESOLVE: For each donut, count the non-void players who chose it. If exactly one did, that player gains the donut's value and adds 1 to their donuts collected. If two or more did, the donut is discarded and none of them gains anything. A donut nobody chose has no effect.\n7. USE PICKS: Every non-void Glazed choice uses up one of that player's Glazed picks, and every non-void Jelly choice uses up one of that player's Jelly picks. This happens whether the donut was won or discarded.\n8. SCORE: Each player's gain this round and everyone's new totals are announced.\n\nEND: The game ends after round 10. Unused picks are worth nothing.",
    "objective": "The player with the highest point total after round 10 wins. If several players tie for the highest total, the one among them with the most donuts collected wins. If they are still tied, the game is a draw among those players.",
    "expected_effect": "Always-best can lose. It spends its Glazed picks in a visible run, and rivals with spare picks (24 picks for 20 premium donuts) can take turns contesting it cheaply, then share the later Glazeds among themselves. Always-Cruller, always-Plain and random play score well below a player who takes premium donuts uncontested, so each can lose. No random draw exists, so the winner is decided by the secret split, by timing and by reading rivals.\n\nTalk passes both tests. Only one player can win, and no equal schedule exists, because the stable 210 points per game cannot split four ways. Players therefore disagree about who takes each round's Glazed and Jelly. A player who follows a proposal such as 'you take Cruller, I take Glazed' hands the proposer the lead. A player who trusts a rival's claim to be out of Glazed picks can be ambushed by a hidden one. Talk is used to propose rotations, to bluff about remaining picks, and to test promises against revealed choices.\n\nCooperation stays worth trying after a betrayal, because each round's collision costs both parties, so mutual avoidance remains individually valuable until the end. The final rounds turn on inferred remaining picks rather than collapsing to one safe option."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 10,
    "choice_steps_per_round": 2,
    "attributes": 9,
    "hidden_elements": 2,
    "random_draws_per_round": 0,
    "rounds": 10
  }
}
```
````
