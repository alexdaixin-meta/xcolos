# air_land_and_sea: needs review

Built from the variation **Three Fronts** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Remove all card abilities. Cards are just Air, Land or Sea with a strength from 1 to 6. Deploying face-up gives the printed strength in the matching theater; improvising face-down gives strength 2 in any theater. (fixes: Eighteen unique card abilities, including adjacency, move and flip interactions, far exceed the step and attribute limits and invite rule disputes.): This keeps the core tension (bluffing face-down versus committing face-up, and spreading strength across theaters) while fitting the step budget and leaving nothing to interpret.
- The three theaters are independent labelled piles with no adjacency. (fixes: Adjacency between theaters gives the game a spatial flavour the platform excludes.): This removes every spatial relation.
- The match is exactly 4 battles of 6 rounds each (24 rounds). The first player alternates each battle, and the higher VP total wins. (fixes: 'First to 12 VP' gives a variable match length. With ties going to the first player, an odd number of battles can leave one seat with an extra first-player battle.): Each player is first player exactly twice, so the tie-break edge balances out and the length is fixed. The game is zero-sum, so there is no cooperative option for 'higher total wins' to collapse.
- Use a single withdrawal table that depends only on how many cards the withdrawing player still holds: 4 or more gives the opponent 2 VP, 2 to 3 gives 3 VP, and 1 gives 4 VP. A battle fought to the end gives the winner 6 VP. (fixes: The withdrawal VP table depends on seat and has several cases, which adds bookkeeping without adding much reasoning.): The table stays simple but keeps the identity of the game: withdraw early to save points, at the cost of conceding the battle.

Objective: After 4 battles, the player with more VP wins. Equal VP is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. Per-battle decision for the trailing player. Fighting to the end is worth +6 if won and -6 if lost, so its relative value is 12p-6. Withdrawing costs -2 with 4+ cards, -3 with 2-3 cards and -4 with 1 card. Withdrawing early is right when p < 1/3, and withdrawing on the last action is right when p < 
- playable: pass. Rules are complete. Each action is precisely defined: which theater each card may go to, what strength it counts and what the opponent sees. The withdraw condition (at least 1 card held) and its VP table are given, as is skipping the remaining rounds after a withdrawal. Stacking is irrelevant to sco
- reasoning_over_luck: pass. Chance: hand-total sd is about 3.5, so the difference between two hands has sd of about 5. Suit spread varies as well. Improvise compresses low cards to 2, which reduces the variance, and the 6 set-aside cards hide exact totals. A large hand gap (for example 27 vs 14) decides a battle almost regardl

## Complexity

- steps_per_round: designed 13, built 14, limit 20
- choice_steps_per_round: designed 2, built 2, limit 4
- attributes: designed 16, built 44, limit 20 (built: 80)
- hidden_elements: designed 2, built 13, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 24, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Battle start deals 6 cards to each hand and sets 6 aside, leaving the deck empty (deal is random, only counts asserted)
- pass: Battle start resets all strengths to 0 (seat 1 then withdraws)
- FAIL: After battle 1 ends, battle 2 has seat 2 as first player | rule R3 is broken: When it is battle 1 or 3, then seat 1 (A) is first player; when it is battle 2 or 4, then seat 2 (B) is first player.; Ada: the rule for 'withdraw' was never matched (the game never put that option to this seat); Blaise: the rule for 'withdraw' was never matched (the game never put that option to this seat)
- FAIL: After battle 2 ends, battle 3 has seat 1 as first player | rule R3 is broken: When it is battle 1 or 3, then seat 1 (A) is first player; when it is battle 2 or 4, then seat 2 (B) is first player.; Ada: the rule for 'withdraw' was never matched (the game never put that option to this seat); Blaise: the rule for 'withdraw' was never matched (the game never put that option to this seat)
- pass: Each player takes one action in a round
- pass: Deploying Land 6 adds 6 to land strength and leaves the hand
- pass: Improvising Land 5 to Sea adds 2 to sea only
- pass: Withdrawing with 4 cards gives the opponent 2 VP
- pass: Second player withdrawing with 3 cards gives the opponent 3 VP
- pass: Withdrawing with 1 card gives the opponent 4 VP
- pass: A player holding 0 cards is not offered withdraw
- FAIL: After a withdrawal the rest of the battle passes with no actions and no scoring | rule R11 is broken: When a player withdraws, then no further actions are taken in that battle and its remaining rounds pass with no actions.; seat 1 was offered 'deploy Air 1', but must not be
- pass: A card placed on an occupied theater adds to what is already there
- pass: Higher strength controls each theater; seat 1 wins Air and Sea and gains 6
- pass: Ties, including 0-0, go to the first player (seat 2 in battle 2)
- pass: Controlling all 3 theaters still gains exactly 6 VP
- pass: A face-down card counts 2 when the battle is fought to the end (reveal itself not observable)
- pass: Game ends after round 24; the last battle's 6 VP decides the winner
- FAIL: Equal VP after round 24 is a shared win | rule R17 is broken: When round 24 is over, then the game ends and the player with more VP wins; equal VP is a draw.; Ada: the rule for 'withdraw' was never matched (the game never put that option to this seat); Blaise: the rule for 'withdraw' was never matched (the game never put that option to this seat)

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [2], results {'seat 2': 11, 'seat 1': 9}, 19-47 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 40.0 decisions, prompts of 331 characters on average (longest 332)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- always taking the first option as seat 1 wins 95% of decided matches against random seats
- always taking the first option as seat 2 wins 93% of decided matches against random seats
- random seats: {'seat 2': 27, 'seat 1': 32, 'seats 1 and 2': 1}
- always `first@seat1`: won 56, lost 3, drew 1
- always `first@seat2`: won 56, lost 4, drew 0
- always `last@seat1`: won 0, lost 60, drew 0
- always `last@seat2`: won 0, lost 60, drew 0

## Triage (whose problem each failure was)

- round 1: fix_game: After a withdrawal the game keeps offering deploy and improvise to the players. It also never clears `battle_over` when the next battle starts: the final state shows battle 2 with `battle_over` still true. As a result, no seat is ever offered 'withdraw' in later battles, which is what makes the R3 and R17 scenarios fail; these are implementation errors, and the rules are sound.
- round 1: fix_game: The rules are sound and expressible, but the game file mishandles the end of a battle and the withdrawal. After a withdrawal it still offered seat 1 'deploy Air 1' in that battle. When it moved on to battle 2 it left battle_over true and never dealt: the deck still holds 18 cards, set_aside is empty and the old hands remain. So no seat was offered actions, including withdraw, in later scenarios.
- round 1: fix_tests: The failing scenarios demand moves the rules forbid. Three tests start with battle_over true (or in a round where no action can occur) and still script 'withdraw' for both seats, which the game rightly never offers. The withdrawal test also forbids 'deploy' in the very round where seat 1 must be offered its normal options before it withdraws. As far as the trace shows, the game's withdrawal handling is correct: 2 VP to the opponent for 4 cards held, battle_over set, offers cleared.

## Choices the rules did not make

- Exactly 2 players (min 2, max 2, suggested 2): The designer fixed the game at 2. It is a head-to-head duel over who controls each theater, and the first-player alternation and the withdrawal payoffs are built for two sides.
- No talk step before actions: The source has no negotiation. In a two-player zero-sum duel, talk would only add words, and bluffing already happens through face-down cards and withdrawal timing.
- Seat 1 is Player A and seat 2 is Player B: The source names A and B but does not say who is who.
- Strength totals are public: Face-down cards always count 2, so each side's strength sum is known to both players. Only the identity of face-down cards is hidden.
- Strategy at the table: A thoughtful player decides which theaters to contest and which to concede, uses improvise to bluff or to shore up a theater, and withdraws early (giving up 2 VP) when the battle is lost rather than giving up 6.

## Simplifications

- The three possible actions are offered as one choice list combining action, card and theater: The engine takes one choice per question. A single list keeps each action to one step.
- The stacking order of cards is not tracked: Every card counts whether or not it is covered, so the order has no effect on play.
- Theater control is compared through the table scratch values seat1_theaters and seat2_theaters: This is the engine's workaround for comparing two players' attributes.

## Encoding attempts

- 1: it plays, but part of it does nothing: game attribute `full_deck` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 2: passed
