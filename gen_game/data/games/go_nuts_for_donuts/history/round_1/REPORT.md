# go_nuts_for_donuts: needs review

Built from the variation **Go Nuts for Donuts: Premium Picks** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Premium picks: each player has exactly 6 premium picks for the whole game. A premium pick is needed to choose the Glazed (9) or the Jelly (6). The three lower donuts can be chosen without limit. A premium choice uses up its pick whether it scores or collides. A premium choice with no matching pick left is void: it scores 0 and blocks nobody. (fixes: P1: Chicken over the top donut.): Always-best can now only chase the Glazed 6 times. If it does so early, rivals can spend a few of their oversupplied picks contesting it, which cheaply drains it. There are 24 premium picks against only 20 premium donuts, so burning one to block is no longer pure self-harm.
- The budget is spent over 10 fixed rounds, and every player's premium uses so far are announced each round. (fixes: P2: No state links the rounds.): Timing now matters: when to spend premium picks, when to let a rival burn theirs, and whether to save picks for the final rounds.
- Secret split: at setup each player privately writes how many of their 6 premium picks are Glazed picks (0 to 6). The rest are Jelly picks. The split is never announced; only uses are visible. (fixes: P3: Nothing hidden to infer.): This is one strong hidden element, chosen by the player rather than dealt, so it is not a lottery. Rivals must infer from play and from talk who can still take the Glazed late, and bluffing about remaining picks becomes possible. It is also a Blotto-like guess: if everyone loads up on Glazed, the Jelly goes cheap.
- Remove the deck, the action cards and the rotation. The row is the same five donuts every round: 9, 6, 4, 2, 1. (fixes: P4: Luck from the deck and action cards; P5: Exceeds the platform's limits.): This removes draw luck and power-card swings and fits the step limits. What varies between rounds is each player's budget, not the row.
- The values 9, 6, 4, 2 and 1 are chosen so that a stable collision-free round yields 21 points. Over 10 rounds that is 210, which cannot be split equally among 4 players. (fixes: P6: Cooperative-draw risk.): Leaving any donut but the Plain untaken is unstable: whoever took a lower donut gains by switching to the untaken one. A stable perfect schedule therefore leaves only the Plain untaken each round, totalling 210, which is not divisible by 4. Someone must end ahead, so trailing players always have a reason to contest.
- Report the complexity consistently: 2 hidden elements (the secret split, and the sealed simultaneous choice), and 0 random draws. (fixes: P7: Inconsistent complexity report.): This corrects the earlier inconsistency.

Objective: The player with the highest point total after round 10 wins. If several players tie for the highest total, the one among them with the most donuts collected wins. If they are still tied, the game is a draw among those players.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. SETUP ARITHMETIC: Values are G=9, J=6, C=4, S=2, P=1. Each player has 6 premium picks (G+J=6) over 10 rounds, so every player has at least 4 rounds that must be C, S or P. Supply is 10 Glazed and 10 Jelly slots, and demand is 24 premium picks. Premium is oversupplied by 4 picks, so collisions are st
- playable: pass. COMPLETENESS: The rules are complete for every situation.
- A void choice is defined: it scores nothing, uses no pick, does not count toward collisions, and is shown as VOID.
- Pick use on a collision is defined: the pick is used.
- Unchosen donuts are defined: they have no effect.
- The announced i
- reasoning_over_luck: pass. CHANCE: There are no random draws at all (random_draws_per_round 0), so the platform contributes no luck. The only uncertainty is opponents' simultaneous choices, which is strategic, not random.

INFERENCE: Each player's remaining premium total is public (6 minus announced uses), but the Glazed/Jell

## Complexity

- steps_per_round: designed 10, built 12, limit 20
- choice_steps_per_round: designed 2, built 3, limit 4
- attributes: designed 9, built 26, limit 20 (built: 80)
- hidden_elements: designed 2, built 5, limit 3
- random_draws_per_round: designed 0, built -, limit 1
- rounds: designed 10, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Every seat starts at 0: after one round with no Glazed or Jelly, totals equal only that round's gains
- pass: A split of G=3 gives Glazed picks, so a lone Glazed choice is not void and scores 9
- pass: A split of G=0 leaves no Glazed picks, so a Glazed choice is void
- pass: The public counters reveal nothing of a secret split of G=4
- pass: Each round begins by adding 1 to the round number
- pass: Talk and choose run for all seats and the first round is round 1
- pass: All five donuts are offered, even Glazed and Jelly with no picks left
- FAIL: Glazed with 0 Glazed picks and Jelly with 0 Jelly picks are void; Glazed with picks is not | rule R7 is broken: When a player chooses Glazed with glazed_picks == 0, or Jelly with jelly_picks == 0, then void = true. Otherwise void = false.; seat 2 void: expected True, got False; seat 2 score: expected 0, got 6; seat 3 void: expected False, got True; seat 3 score: expected 9, got 0; seat 3 donuts: expected 1, got 0
- FAIL: A void Jelly gains 0, uses no pick and does not collide with a real Jelly | rule R8 is broken: When a choice is void, that player gains 0, uses no pick, and is not counted as choosing that donut.; seat 1 void: expected True, got False; seat 1 jelly_used: expected 0, got 1; seat 2 score: expected 6, got 0; seat 2 donuts: expected 1, got 0
- pass: At the reveal only the void choice is marked void
- FAIL: A lone Glazed chooser gains 9 and one donut | rule R10 is broken: When exactly one non-void player chooses Glazed, that player gains 9 points and donuts += 1.; seat 1 score: expected 9, got 0; seat 1 donuts: expected 1, got 0
- pass: A lone Jelly chooser gains 6 and one donut
- pass: A lone Cruller chooser gains 4 and one donut
- pass: A lone Sprinkle chooser gains 2 and one donut
- pass: A lone Plain chooser gains 1 and one donut
- pass: Two non-void players on the same donut both gain nothing
- FAIL: A discarded non-void Glazed still uses a pick | rule R16 is broken: When a player makes a non-void Glazed choice, glazed_picks decreases by 1 and glazed_used increases by 1, whether the donut was won or discarded.; seat 1 glazed_used: expected 3, got 2; seat 1 void: expected False, got True; seat 2 glazed_used: expected 1, got 0; seat 2 void: expected False, got True
- pass: A discarded non-void Jelly still uses a pick
- pass: Round gains add to the existing score and donut totals
- pass: The game ends after round 10 and unused picks are worth nothing
- pass: A tie on score is broken by more donuts
- pass: Players level on score and donuts share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [4], results {'seat 4': 8, 'seat 1': 4, 'seat 3': 5, 'seat 2': 3}, 84-84 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 84.0 decisions, prompts of 211 characters on average (longest 263)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 4': 18, 'seat 1': 16, 'seat 3': 13, 'seat 2': 13}
- always `first@seat1`: won 0, lost 60, drew 0
- always `first@seat2`: won 0, lost 60, drew 0
- always `last@seat1`: won 0, lost 60, drew 0
- always `last@seat2`: won 0, lost 60, drew 0

## Triage (whose problem each failure was)

- round 1: fix_game: The rules are clear and the platform can express them. The trace shows the game setting the secret-split picks (seat 2 glazed_picks 0→6, seat 3 glazed_picks 0→2 and jelly_picks 0→4) and then overwriting them with glazed_picks = 0 and jelly_picks = 6 for every seat. Every legitimate Glazed choice therefore comes out VOID, every Jelly is wrongly allowed, and the void, scoring and pick-use tests all fail as a result.
- round 1: fix_game: The trace shows each seat's picks first set correctly from its answer (seat 2 to 6 Glazed, seat 3 to 2 Glazed and 4 Jelly). A second update then resets every seat to 0 Glazed and 6 Jelly, using `split_g` = 0. Every legitimate Glazed choice therefore becomes VOID, and every Jelly pick is wrongly available. The four failures all follow from this bug in the file, not from the tests.
- round 1: fix_game: The trace shows the split being applied correctly and then overwritten: seat 2's glazed_picks went 0->6 and then 6->0, with jelly_picks set to 6, and seat 3 went 2/4 and then 0/6. Every player ends up as if G=0, so Glazed is wrongly void and Jelly wrongly allowed, which breaks the void, scoring and pick-use scenarios. The tests match the rules.

## Choices the rules did not make

- Exactly 4 players (min 4, max 4, suggested 4): The designer fixed the table at 4. The five-donut row against four choosers is what creates the collision tension, so another count would change the game.
- Talk kept as a simultaneous poll broadcast to all: The rules specify simultaneous, non-binding messages. Players want different donuts, so claims and bluffs about plans (and hidden pick splits) give real material to reason about.
- Strategy at the table: A thoughtful player infers others' remaining premium picks from the public glazed_used and jelly_used, times Glazed for rounds when others are likely out, and uses talk to bluff or deter. A thoughtless player always grabs Glazed and collides.
- Tie-break encoded as score * 100 + donuts: Donuts can never exceed 10, so multiplying the score by 100 keeps points primary and donuts as the tie-break.
- Glazed and Jelly are always offered, even with no picks left: The rules define void choices as possible outcomes, so the option must exist.

## Simplifications

- A final draw among tied players is represented as a shared win: The engine has no separate draw: players level at the top share the win, which matches the source's draw among those players.

## Encoding attempts

- 1: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state a player is shown has empty fields (choice, shown, shown, shown); hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 2: passed
