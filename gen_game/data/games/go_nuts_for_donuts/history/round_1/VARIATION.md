# Variation: Go Nuts for Donuts: Premium Picks

Four players pick donuts from the same row of five each round, and a donut picked by two or more is lost. The two best donuts can only be chosen with premium picks: 6 per player, split secretly between Glazed and Jelly at the start. Players talk, bluff about what they have left, and time their premium picks over 10 rounds.

Players: 4 to 4, best with 4

## Review of the original

Go Nuts for Donuts is a 2-6 player game. A face-up row of N+1 donut cards is dealt from a shuffled deck, and every round each player secretly picks a row position. A donut picked by exactly one player goes to that player; a donut picked by two or more is discarded. Some donuts carry action powers (steal, draw, manipulate). The game ends when the deck cannot refill the row, and the most points wins.

- **non_degenerate**: weak. Seats are symmetric and the sealed picks are simultaneous, so no seat has an edge. The core is a chicken game over the most valuable donut, and nothing limits how often a player can go for it. A stubborn 'always pick the best donut' player wins whenever rivals give way, because blocking costs the blocker as much as the target and hands the gain to the bystanders. The previous variation showed exactly this: always-9 scored about 46 against random play and about 90 against rivals who gave way.
- **skill_sensitive**: weak. The shuffled deck decides which values appear each round, and the action cards (steal, draw) swing totals by luck of timing. Among equally careful players, mixed picks over a random row largely decide who ends up uncontested.
- **headroom**: good. Predicting which donut each rival will chase, and using action cards well, gives a strong player something to improve on. A weak player still collects uncontested donuts.
- **reasoning_dependent**: weak. The row is face-up and nothing links rounds except the deck running down. The only thing to infer is the rivals' simultaneous pick, so there is no hidden state to deduce and no resource to plan with. The previous variation's rotating row was a public relabelling: round 7 was strategically identical to round 1.
- **verifiable**: good. Points on collected donuts are summed and the tie-break is a card count, all plain arithmetic.
- **fits_platform**: weak. It is turn-based and text-only. However, a deck filtered by player count, refills and many distinct action-card powers need far more steps and rules than the limits allow, and the action-card powers are mostly luck.

## Problems

- P1: Chicken over the top donut. Nothing limits how often a player can chase the best donut, so a stubborn always-best policy wins or draws against sensible rivals, because blocking it is self-harm that helps the bystanders.
- P2: No state links the rounds. There is no budget or resource to plan with, so every round is the same one-shot game and multi-round planning is impossible.
- P3: Nothing hidden to infer. Apart from the sealed pick everything is public, and the previous rotating row was a pure relabelling.
- P4: Luck from the shuffled deck and from action-card powers decides much of the outcome among careful players.
- P5: Action cards, deck filtering and refills exceed the platform's step and complexity limits.
- P6: Cooperative-draw risk. If players can agree a schedule in which everyone scores the same, talk produces a stable four-way draw and the interesting choice disappears.
- P7: The previous variation's complexity report was inconsistent about hidden elements.

## Changes

- Premium picks: each player has exactly 6 premium picks for the whole game. A premium pick is needed to choose the Glazed (9) or the Jelly (6). The three lower donuts can be chosen without limit. A premium choice uses up its pick whether it scores or collides. A premium choice with no matching pick left is void: it scores 0 and blocks nobody. (fixes: P1: Chicken over the top donut.): Always-best can now only chase the Glazed 6 times. If it does so early, rivals can spend a few of their oversupplied picks contesting it, which cheaply drains it. There are 24 premium picks against only 20 premium donuts, so burning one to block is no longer pure self-harm.
- The budget is spent over 10 fixed rounds, and every player's premium uses so far are announced each round. (fixes: P2: No state links the rounds.): Timing now matters: when to spend premium picks, when to let a rival burn theirs, and whether to save picks for the final rounds.
- Secret split: at setup each player privately writes how many of their 6 premium picks are Glazed picks (0 to 6). The rest are Jelly picks. The split is never announced; only uses are visible. (fixes: P3: Nothing hidden to infer.): This is one strong hidden element, chosen by the player rather than dealt, so it is not a lottery. Rivals must infer from play and from talk who can still take the Glazed late, and bluffing about remaining picks becomes possible. It is also a Blotto-like guess: if everyone loads up on Glazed, the Jelly goes cheap.
- Remove the deck, the action cards and the rotation. The row is the same five donuts every round: 9, 6, 4, 2, 1. (fixes: P4: Luck from the deck and action cards; P5: Exceeds the platform's limits.): This removes draw luck and power-card swings and fits the step limits. What varies between rounds is each player's budget, not the row.
- The values 9, 6, 4, 2 and 1 are chosen so that a stable collision-free round yields 21 points. Over 10 rounds that is 210, which cannot be split equally among 4 players. (fixes: P6: Cooperative-draw risk.): Leaving any donut but the Plain untaken is unstable: whoever took a lower donut gains by switching to the untaken one. A stable perfect schedule therefore leaves only the Plain untaken each round, totalling 210, which is not divisible by 4. Someone must end ahead, so trailing players always have a reason to contest.
- Report the complexity consistently: 2 hidden elements (the secret split, and the sealed simultaneous choice), and 0 random draws. (fixes: P7: Inconsistent complexity report.): This corrects the earlier inconsistency.

## Kept from the original

- Everyone secretly picks a donut from a face-up row at the same moment.
- A donut picked by exactly one player scores for them; a donut picked by two or more is discarded and nobody scores it.
- The row has N+1 donuts for N players (5 donuts for 4 players), so one donut always goes untaken.
- Most points wins, with the original tie-break of most donuts collected.

## The variation's rules

SETUP: There are exactly 4 players, each starting with 0 points and 0 donuts collected.

THE ROW: Every round the same five donuts are offered:
- Glazed, worth 9 points
- Jelly, worth 6 points
- Cruller, worth 4 points
- Sprinkle, worth 2 points
- Plain, worth 1 point

SECRET SPLIT: Before round 1, each player privately and simultaneously writes a whole number G from 0 to 6. That player has G Glazed picks and 6 minus G Jelly picks. Nobody else is told this number, at any time during the game.

EACH ROUND (10 rounds):
1. ANNOUNCE: The round number is announced, along with, for every player, their points, how many donuts they have collected, and how many Glazed choices and how many Jelly choices they have made so far that used a pick. Remaining picks are not announced.
2. TALK: Every player writes one short message at the same time, without seeing the others. All four messages are then shown to everyone. Messages are not binding.
3. CHOOSE: Every player secretly and simultaneously chooses exactly one donut: Glazed, Jelly, Cruller, Sprinkle or Plain.
4. CHECK PICKS: A player who chose Glazed with no Glazed picks left, or Jelly with no Jelly picks left, has made a VOID choice. A void choice scores nothing, uses no pick, and does not count as choosing that donut for anyone else.
5. REVEAL: All four choices are revealed together, with any void choice marked VOID.
6. RESOLVE: For each donut, count the non-void players who chose it. If exactly one did, that player gains the donut's value and adds 1 to their donuts collected. If two or more did, the donut is discarded and none of them gains anything. A donut nobody chose has no effect.
7. USE PICKS: Every non-void Glazed choice uses up one of that player's Glazed picks, and every non-void Jelly choice uses up one of that player's Jelly picks. This happens whether the donut was won or discarded.
8. SCORE: Each player's gain this round and everyone's new totals are announced.

END: The game ends after round 10. Unused picks are worth nothing.

Objective: The player with the highest point total after round 10 wins. If several players tie for the highest total, the one among them with the most donuts collected wins. If they are still tied, the game is a draw among those players.

Expected effect: Always-best can lose. It spends its Glazed picks in a visible run, and rivals with spare picks (24 picks for 20 premium donuts) can take turns contesting it cheaply, then share the later Glazeds among themselves. Always-Cruller, always-Plain and random play score well below a player who takes premium donuts uncontested, so each can lose. No random draw exists, so the winner is decided by the secret split, by timing and by reading rivals.

Talk passes both tests. Only one player can win, and no equal schedule exists, because the stable 210 points per game cannot split four ways. Players therefore disagree about who takes each round's Glazed and Jelly. A player who follows a proposal such as 'you take Cruller, I take Glazed' hands the proposer the lead. A player who trusts a rival's claim to be out of Glazed picks can be ambushed by a hidden one. Talk is used to propose rotations, to bluff about remaining picks, and to test promises against revealed choices.

Cooperation stays worth trying after a betrayal, because each round's collision costs both parties, so mutual avoidance remains individually valuable until the end. The final rounds turn on inferred remaining picks rather than collapsing to one safe option.

## Complexity (the designer's count, against the limits)

- steps_per_round: 10 (limit 20)
- choice_steps_per_round: 2 (limit 4)
- attributes: 9 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 10 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
