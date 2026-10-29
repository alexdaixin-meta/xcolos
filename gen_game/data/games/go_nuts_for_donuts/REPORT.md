# go_nuts_for_donuts: ready for review

Built from the variation **Go Nuts for Donuts: Secret Budget** (design round 2); see VARIATION.md.

## What was changed from the original, and why

- A fixed row of five donuts every round: Glazed 9, Jelly 6, Cruller 4, Sprinkle 2, Plain 1. There are no action cards and no deck. (fixes: Too many distinct card powers and set rules to build within 20 steps and 20 attributes.): Keeps the 'pick one of N+1, collisions discard' core while fitting the limits. Removing the random offer means skill, not the shuffle, decides the game.
- No random draws at all: the same five donuts are offered in all 10 rounds. (fixes: A shuffled deck makes the offer each round random, adding luck without adding reasoning.): Luck no longer swamps reading opponents.
- Each player has 6 premium picks for the whole game, the only way to choose Glazed or Jelly. Before round 1 each player secretly sets how many are Glazed (G). The rest (6 - G) are Jelly. Players see each other's choices each round but never each other's G. (fixes: No hidden information: the table and scores are fully public, so opponent modelling has little to work from beyond history.): Creates one strong hidden element. Players must infer from rivals' play how many Glazed or Jelly picks each still holds, and plan their own budget over 10 rounds.
- Store only the answer split_g plus the counters glazed_used and jelly_used. There are no glazed_picks or jelly_picks attributes. A Glazed choice is void exactly when glazed_used >= split_g, and a Jelly choice is void exactly when jelly_used >= 6 - split_g. split_g is written once by the setup poll, and no other step ever writes it. glazed_used and jelly_used start at 0 and only ever increase by 1 on a non-void choice of that donut. The setup poll offers exactly the options 0 to 6, so there is no default or fallback value. (fixes: BUILD FAILURE in the previous variation: the secret split was overwritten after the poll. Every seat ended with glazed_picks 0 and jelly_picks 6, which broke the void test (R7), the void-collision rule (R8), the lone-Glazed payout (R10) and the pick accounting (R16). The cause was a second, unconditional step that reset the stored picks. Storing two mutable pick counters derived from the answer invited exactly this overwrite.): The overwritten-picks bug came from a second operation resetting derived counters. With nothing derived stored, nothing remains to reset. Void is computed directly from the answer and the usage counters.
- Drop the table constants lone_chooser_count, donut_collected_increment and pick_use_per_choice. Write the literal numbers (1) into the rules. (fixes: The previous variation carried redundant table constants (lone_chooser_count, donut_collected_increment, pick_use_per_choice) that added attributes and places for the builder to go wrong.): Fewer attributes and fewer indirections for the builder to misread.
- Add one simultaneous message per player before each round's choice. (fixes: No hidden information: the table and scores are fully public, so opponent modelling has little to work from beyond history.): Lets players claim, bluff about remaining picks and try to steer rivals off a donut. Interests conflict because only one player can take each donut and only one player wins.

Objective: After round 10, the player with the highest score wins. If several are tied on score, the one among them with the most donuts wins (rank value = score x 100 + donuts). If players are still tied on both, the game is a draw among them.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. Donut values are G=9, J=6, C=4, S=2, P=1. A donut pays only to a player who picks it alone. Each player has 6 premium picks (G or J) over 10 rounds, so at least 4 rounds per player must go to C/S/P or be wasted as voids. The 4 players hold 24 premium picks for 20 premium slots (2 per round x 10). Th
- playable: pass. The rules cover every situation:
- Void conditions are exact and use >=.
- Void choices neither count for collisions nor use picks.
- Picks are used on non-void choices whether the donut was won or discarded.
- The split is fixed after setup and never reset.
- Reveal contents and the winner and tie 
- reasoning_over_luck: pass. There are no random draws (0 per round). Chance enters only through opponents' mixed strategies, which are what the game asks players to model. There is real hidden information to infer. Each split_g is secret, but every non-void choice is revealed, so used counts are public. A VOID mark reveals exh

## Complexity

- steps_per_round: designed 14, built 13, limit 20
- choice_steps_per_round: designed 2, built 3, limit 4
- attributes: designed 17, built 27, limit 20 (built: 80)
- hidden_elements: designed 1, built 4, limit 3
- random_draws_per_round: designed 0, built -, limit 1
- rounds: designed 10, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: R1: split poll answers are stored and used (seat 1 splits 6 Glazed, seat 2 splits 0 Glazed)
- pass: R2: split 2 gives exactly 2 Glazed picks, so the third Glazed is void
- pass: R3: a round with talk still resolves the donut picks normally
- pass: R4: with 1 Glazed pick, it is spent after one use and the next Glazed is void
- pass: R5: Glazed with split 0 is void and gains nothing
- pass: R6: Jelly with split 6 is void and gains nothing
- pass: R7: Cruller, Sprinkle and Plain are never void, whatever the split
- pass: R8: a lone non-void pick scores the donut's points and 1 donut
- pass: R9: two non-void picks of the same donut both score nothing
- pass: R10: a discarded Glazed still uses the pick, so the next Glazed is void
- pass: R11: a discarded Jelly still uses the pick, so the next Jelly is void
- pass: R12: a void Glazed uses no pick, and a later Jelly still scores
- pass: R13: a void Glazed does not block a lone non-void Glazed
- pass: R14: scores and donuts after a round with a collision
- pass: R15: the game ends after round 10 (10 lone Crullers give 40)
- pass: R16: seats level on score and donuts share the win
- pass: R16: on equal scores, more donuts wins

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [4], results {'seat 4': 8, 'seat 1': 4, 'seat 3': 5, 'seat 2': 3}, 84-84 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 84.0 decisions, prompts of 195 characters on average (longest 228)

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
- round 2: fix_tests: The failing tests set split_g with `given`, but the rules require the split poll to run before round 1, and that poll sets split_g. In the trace the game ran the poll and overwrote the given split_g (2 -> 0), then voided and scored exactly as the rules say for split 0. The R1 test, which sets the split through the poll answers, raised no failure.
- round 2: fix_tests: The game does offer the split options 0–6. R1 and R2 match option 0 for seats 2–4 and did not fail. The two R16 scenarios fail only because their rule for answer 0 was never matched, so those scenarios expect 0 to be offered somewhere the rules never offer it. That means the rule is either expected more than once, or set up in a run that starts after the one-time split poll.

## Choices the rules did not make

- Exactly 4 players, suggested 4: The rules fix the table at 4 and the designer chose it. Five donuts for four players makes collisions frequent but avoidable, which is what the game is about.
- Keep simultaneous talk each round, built as a poll and then a broadcast: The rules require it. Players disagree about who should take the high donuts, so talk can be used to bluff about one's remaining budget or to stake claims.
- glazed_used and jelly_used are public: The reveal shows every choice and whether it was void, so these counts can be deduced by anyone. Only split_g stays secret.
- Per-donut counters and the per-player choice, void and gained fields as attributes: The void check, the count and the award need state to work on. These are reset at the start of each round.
- Rank value score * 100 + donuts: This is given by the rules. Donuts can never exceed 10, so the score always dominates the tie-break.

## Simplifications

- The private reminder of picks left is delivered as a sync of each player's own state, with the computed values: The engine sends private state through sync. This has the same effect as the rule's reminder.
