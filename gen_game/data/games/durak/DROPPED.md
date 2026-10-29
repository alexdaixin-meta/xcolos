# Dropped: too complex

it is too large for the platform: the built game has 6 choice steps per round, over the limit of 4 (after 3 variation(s))

## The last variation tried

Duel Durak: Two-player Durak with fixed 8-card hands, 20 unseen set-aside cards, a trump chosen by offer-and-pick, and at most one throw-in per bout. The first player to shed all their cards wins.

## What was tried

- design 1: the critic found it not sound (playable, reasoning_over_luck)
- round 1: behavior problem; triage said fix_game: In the failing scenario the attack was 61 (6 of Clubs) with Spades as trump, and the defender held 94, 104 and 114, all Spades trumps, so a one-card defence is 
- round 1: behavior problem; triage said fix_game: In the failing scenario the trump was Spades and the defender held 94 (9 of Spades, a trump) against an attack of 61 (6 of Clubs), yet the game offered the defe
- round 1: build problem; triage said fix_game: The rules have only one random event, the S1 shuffle at the start of each deal, and the platform supports seeded deck handling. Different logs from the same see
- round 2: behavior problem; triage said fix_tests: The offer, trump-pick and first-attacker scenarios run with "rounds": 0, so no moves are played (the log shows 'moves played: .'). Round 1, where seat 2 offers 
- round 2: behavior problem; triage said fix_game: The rules make round 1 setup only, with no bout, and bouts run in rounds 2 to 40. The game plays a full bout inside round 1 as well: in R1 seat 1 attacked 9, se
- round 2: behavior problem; triage said fix_game: The R10 and R11 failures show the game offering the attacker throw-in cards it may not play. In R10 it offered card 20 (the 8 of Hearts), whose rank matches not
- round 2: behavior problem; triage said fix_game: The throw-in options are wrong in the game file. In R10 the table holds 9 (6 of Diamonds) and 1 (7 of Clubs), so only rank-6 and rank-7 cards may be thrown in, 
- round 3: behavior problem; triage said fix_tests: In the trace seat 2 takes once in each bout: card 10, then card 0. It ends holding [0, 1, 2, 3, 10], and hand_size 5 equals the cards actually held, so the game
- round 3: behavior problem; triage said fix_tests: In the first two failures the game's throw-in offer was correct: the final offer was [PASS, 9, 18, 27] after attack 0. The tests flagged 1 and 14 because their 
- round 3: design problem; triage said revise_rules: The game was built and behaves as specified, but the design has six choice steps per round where the limit is four. A thoughtless 'always pick the last option' 

To bring the game back, clear `dropped` in its inventory record.
