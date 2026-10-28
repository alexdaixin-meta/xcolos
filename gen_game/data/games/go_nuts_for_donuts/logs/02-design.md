# 02 design

- time: 2026-10-28T04:10:40+00:00 (152.8s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 27c2149a0d130400, reply sha256 7154510989c928a8

## Sent

````
Original game: Go Nuts for Donuts
Players in the original: 2 to 6

Original rules:
Set up a row of N+1 face-up donut cards where N is player count, numbered 1 to N+1 left to right, from a shuffled deck filtered by player count. Each player holds selection cards 1 to N+1. Each round all players secretly choose a row position and reveal simultaneously. Resolve positions in ascending order: if two or more players chose the same number, that donut is discarded with no one getting it. If exactly one player chose it, that player takes it face-up to their score pile. Some donuts are action cards that trigger immediately when taken from the row in number order, letting you steal, draw, or manipulate cards; powers do not trigger when gained other ways. After resolving, refill empty row spots in order from the deck and return selection cards to hands. Continue until the deck cannot fully refill the row, then total points on collected donuts. Most points wins, tie-break most cards.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
Playing the rules with numbers (every simple policy, 1200 games each) found:
- the policy 'if Choc->P3, Jelly->P4' wins 73% of games against random opponents and loses 25%: the simple policy is too good
- when everyone plays the best joint policy ('if Choc->P3, Jelly->P5'), 50% of games are decided by the random draw (someone finishes ahead only because of a hidden type or deal): reasoning does not decide the winner
- numbers (seat 1's policy, outcome against random opponents): random: win 25% draw 2% loss 72%; always P1: win 13% draw 1% loss 86%; if Choc->P1, Jelly->P2: win 25% draw 4% loss 71%; if Choc->P1, Jelly->P3: win 19% draw 3% loss 78%; if Choc->P1, Jelly->P4: win 50% draw 3% loss 48%; if Choc->P1, Jelly->P5: win 27% draw 4% loss 69%; if Choc->P2, Jelly->P1: win 0% draw 0% loss 100%; always P2: win 13% draw 2% loss 85%; if Choc->P2, Jelly->P3: win 7% draw 1% loss 92%; if Choc->P2, Jelly->P4: win 38% draw 1% loss 60%; if Choc->P2, Jelly->P5: win 17% draw 3% loss 81%; if Choc->P3, Jelly->P1: win 37% draw 1% loss 62%; if Choc->P3, Jelly->P2: win 48% draw 3% loss 49%; always P3: win 42% draw 2% loss 55%; if Choc->P3, Jelly->P4: win 73% draw 2% loss 25%; if Choc->P3, Jelly->P5: win 52% draw 2% loss 46%; if Choc->P4, Jelly->P1: win 8% draw 1% loss 91%; if Choc->P4, Jelly->P2: win 20% draw 3% loss 78%; if Choc->P4, Jelly->P3: win 16% draw 3% loss 81%; always P4: win 42% draw 3% loss 55%; if Choc->P4, Jelly->P5: win 24% draw 3% loss 74%; if Choc->P5, Jelly->P1: win 17% draw 2% loss 81%; if Choc->P5, Jelly->P2: win 30% draw 3% loss 66%; if Choc->P5, Jelly->P3: win 22% draw 3% loss 74%; if Choc->P5, Jelly->P4: win 52% draw 4% loss 44%; always P5: win 32% draw 4% loss 63%
- everyone playing 'if Choc->P3, Jelly->P5' (best joint play): mean total 10.5; every player tied in 50% of games, so 50% are decided by the draw
The variation that was played: Go Nuts for Donuts: Secret Cravings: SETUP: There are 4 players. Each player is privately and independently assigned a craving, Chocolate or Jelly, with a 50% chance each. Only that player knows their craving. Every player starts with 0 points and 0 donuts.

THE ROW: The same 5 donuts are offered every round, and everyone can see them:
- Position 1: Chocolate, base value 2
- Position 2: Jelly, base value 2
- Position 3: Chocolate, base value 4
- Position 4: Jelly, base value 4
- Position 5: Plain, base value 5

A donut of a player's craved flavour is worth its base value + 3 to that player. All other donuts are worth their base value. This gives the following values:
- For a Chocolate craver, positions 1 to 5 are worth 5, 2, 7, 4, 5.
- For a Jelly craver, positions 1 to 5 are worth 2, 5, 4, 7, 5.

EACH ROUND (12 rounds):
1. TALK: Every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Promises and claims (including claims about your craving) are not binding.
2. CHOOSE: Every player secretly and simultaneously chooses one position from 1 to 5.
3. REVEAL: All choices are revealed together.
4. RESOLVE: For each position, if exactly one player chose it, that player gains points equal to that donut's value to them and adds 1 to their donut count. If two or more players chose it, it is discarded and none of them gains anything. Positions nobody chose have no effect.
5. ANNOUNCE: Each player's points gained this round and the new totals are announced. Cravings remain secret.

The row is the same again next round.

END: The game ends after round 12, and cravings are revealed. Winner: The player with the highest point total wins. If two or more players tie for the highest total, the tied player with the most donuts taken wins. If they are still tied, the game is a draw among them.
Do not tweak it: change the payoffs or the objective until every one of these problems is gone.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Go Nuts for Donuts is a 2-6 player simultaneous-selection game. Each round every player secretly picks one position in a row of N+1 donuts. A donut picked by exactly one player goes to that player, and a donut picked by two or more is discarded. Some donuts have action powers. Most points at the end wins. The previous variation fixed the row at 5 donuts, added a hidden 50/50 Chocolate/Jelly craving worth +3 on matching donuts, and ran 12 rounds with talk and a highest-total winner.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "bad",
      "evidence": "The row never changed, so the craving-conditional fixed policy 'Choc->P3, Jelly->P4' (always grab your best donut) won 73% and lost 25% against random opponents. Other fixed policies won only 0-52%. One thoughtless rule dominates, and repeating it every round cost nothing because the same row came back each round."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Under the best joint policy, 50% of games were all-player ties and the other 50% were decided by the craving deal. A player whose craving was the minority type simply never collided. Collisions were driven by who shared your type, not by how well you predicted opponents."
    },
    {
      "criterion": "headroom",
      "verdict": "weak",
      "evidence": "With a static row there is one obvious target per type. After round 1 there is little left to improve except guessing whether a same-type rival exists. The 12 rounds repeat the same decision."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "weak",
      "evidence": "There is something to infer: rivals' cravings and their next pick. But the payoff from that inference was swamped by type luck. Talk mostly served to announce a craving, which the static row made easy to verify from the announced gains."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Scores follow by arithmetic from the choices: uncontested position gives its value, contested gives 0."
    },
    {
      "criterion": "fits_platform",
      "verdict": "good",
      "evidence": "Simultaneous polls, a public row, simple arithmetic and fixed rounds, with no board. The original's deck refills and action cards (steal, draw) were already removed sensibly."
    }
  ],
  "problems": [
    "P1: The row is identical every round, so a fixed 'take my best donut' policy that never looks at the round wins 73% against random play.",
    "P2: The hidden craving decides the winner under good play. A player with the minority craving never collides, so 50% of best-joint-play games are won by the deal and the rest are all-tied.",
    "P3: There is only one meaningful decision, repeated 12 times. The repetition gives no reason to plan across rounds or to vary play, so headroom is small.",
    "P4: Talk mostly leaks or claims a craving rather than creating a real contest over who takes the most valuable donut."
  ],
  "changes": [
    {
      "what": "The row rotates on a public schedule. Five donuts worth 9, 7, 5, 3 and 1 shift one position left each round, wrapping around, over a 5-round cycle played twice (10 rounds). Every position holds every value exactly twice over the game.",
      "why": "This restores the original's changing row. A policy that always picks the same position earns the same expected points as random play, so no round-blind rule has an edge. Doing well means tracking where the 9 and 7 are this round and predicting who goes for them.",
      "fixes": "P1"
    },
    {
      "what": "The hidden cravings are removed. All donuts are worth the same to everyone.",
      "why": "Any private random type in a collision game gives the minority type a free uncontested lane. With identical values, symmetric good play produces equal outcomes, and the winner is whoever out-predicts the others rather than whoever was dealt the lucky type.",
      "fixes": "P2"
    },
    {
      "what": "Values are spread wide (9/7/5/3/1) instead of nearly flat.",
      "why": "This creates a real chicken/minority dilemma every round. The 9 is worth fighting for but is the most likely to be contested. The 1 and 3 are low but often uncontested. The best pick depends on the round's layout, the scoreboard and opponents' revealed habits, which gives the game something to plan and adapt over 10 rounds.",
      "fixes": "P3"
    },
    {
      "what": "Talk is kept as one simultaneous message per round, now about claims and threats over the top donuts.",
      "why": "Everyone wants the same high donuts and only one player can win. Messages like 'I'm taking the 9, take the 7 or we both get nothing' are bluffs and threats that must be read against each player's history. Following someone else's proposal can hand them the round.",
      "fixes": "P4"
    },
    {
      "what": "The tie-break on donut count is dropped. Players tied for the highest total share a draw.",
      "why": "This keeps the winner rule exactly expressible in arithmetic and in the model. Donut count rewarded taking 1-point scraps in a way that distorted the main choice.",
      "fixes": "P2"
    }
  ],
  "keeps": [
    "A face-up row of N+1 donuts (5 for 4 players) and the secret simultaneous choice of one position.",
    "The signature rule: a donut chosen by exactly one player is taken, and a donut chosen by two or more is discarded.",
    "A row that changes between rounds, like the original's refills, in a public and deterministic form.",
    "Most points at the end wins."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core collision-avoidance guessing game is a strong opponent-modelling test once the static row and the luck-driven hidden cravings are removed, and it fits easily inside the limits."
  },
  "variation": {
    "name": "Go Nuts for Donuts: Rotating Row",
    "summary": "Four players spend 10 rounds secretly picking one of five donuts from a public row whose values rotate each round. A donut picked by exactly one player is taken, and a donut picked by two or more is discarded. A simultaneous message phase each round allows claims, threats and bluffs. The highest total wins.",
    "players": {
      "min": 4,
      "max": 4,
      "suggested": 4
    },
    "rules": "SETUP: There are exactly 4 players. Each starts with 0 points. There are no hidden cards or types.\n\nTHE DONUTS: Five donuts are worth 9, 7, 5, 3 and 1 points, the same to every player. They sit in a face-up row of positions 1 to 5. Their arrangement changes each round on a fixed public schedule, shown to everyone at the start of the game:\n- Rounds 1 and 6: positions 1-5 are worth 9, 7, 5, 3, 1\n- Rounds 2 and 7: positions 1-5 are worth 7, 5, 3, 1, 9\n- Rounds 3 and 8: positions 1-5 are worth 5, 3, 1, 9, 7\n- Rounds 4 and 9: positions 1-5 are worth 3, 1, 9, 7, 5\n- Rounds 5 and 10: positions 1-5 are worth 1, 9, 7, 5, 3\nEach round, every value moves one position to the left, and the value in position 1 wraps to position 5.\n\nEACH ROUND (10 rounds):\n1. ANNOUNCE ROW: The round number and the values of positions 1 to 5 for this round are announced.\n2. TALK: Every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Messages are not binding.\n3. CHOOSE: Every player secretly and simultaneously chooses one position from 1 to 5.\n4. REVEAL: All four choices are revealed together.\n5. RESOLVE: For each position, if exactly one player chose it, that player gains its value this round. If two or more players chose it, the donut is discarded and none of them gains anything. A position nobody chose has no effect.\n6. SCORE: Each player's gain this round and everyone's new total are announced.\n\nEND: After round 10 the game ends.",
    "objective": "The player with the highest point total after round 10 wins. If two or more players tie for the highest total, the game is a draw among those tied players.",
    "expected_effect": "No fixed position or other round-blind rule beats random play on average, because every position holds each value exactly twice. The edge comes from reading the round's layout and predicting rivals. Each round poses a chicken/minority dilemma: the 9 and 7 tempt everyone, so they are often discarded, while the 3 and 1 are safe but small. Players must model who has been greedy, who backs off after collisions, and who is behind and must gamble late. Talk passes both tests. On REASONING, players claim donuts, threaten to collide if challenged, offer splits ('you take 9 this round, I take it in round 7'), and bluff, and every claim can be checked against later choices. On CONFLICT, everyone wants the same top donuts and only one player can win. A player who obeys 'you take the 7, I'll take the 9' hands the proposer 2 points a round, and a player who trusts a split promise can be betrayed in the next rotation. When everyone plays the same symmetric strategy, totals come out equal in expectation, so there is no type luck. Outcomes are decided by who reads the others best, especially in rounds 9-10, when leaders and trailers want different risks."
  },
  "model": {
    "players": 4,
    "rounds": 10,
    "actions": ["P1", "P2", "P3", "P4", "P5"],
    "types": null,
    "payoff": "(9 - 2 * (((0 if action == 'P1' else 1 if action == 'P2' else 2 if action == 'P3' else 3 if action == 'P4' else 4) + (round - 1 if round <= 5 else round - 6)) if ((0 if action == 'P1' else 1 if action == 'P2' else 2 if action == 'P3' else 3 if action == 'P4' else 4) + (round - 1 if round <= 5 else round - 6)) < 5 else ((0 if action == 'P1' else 1 if action == 'P2' else 2 if action == 'P3' else 3 if action == 'P4' else 4) + (round - 1 if round <= 5 else round - 6)) - 5)) if ((action == 'P1' and n_P1 == 1) or (action == 'P2' and n_P2 == 1) or (action == 'P3' and n_P3 == 1) or (action == 'P4' and n_P4 == 1) or (action == 'P5' and n_P5 == 1)) else 0",
    "winner": {
      "kind": "highest_total"
    }
  },
  "complexity": {
    "steps_per_round": 8,
    "choice_steps_per_round": 2,
    "attributes": 8,
    "hidden_elements": 1,
    "random_draws_per_round": 0,
    "rounds": 10
  }
}
```
````
