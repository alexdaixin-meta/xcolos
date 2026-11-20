# one_night_revolution: ready for review

Built from the variation **One Night Revolution: Ten Nights, Hidden Ledger** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Hide all scores until the end: announce no points during the game; announce votes and terminated roles each round only; announce every final total, Rebel points and Informant points after round 10. (fixes: Running announcements of total, Rebel points and Informant points let anyone read off every earlier Informant pair in all 20 matches; with each pair used once round 9 had one candidate pair left and round 10 Informants were terminated in 19 of 20.): Removes the deterministic schedule leak while keeping vote and termination information for deduction; round 9 keeps ~5 candidate pairs so deception and planning stay relevant.
- Individual survival bonus: each Informant who was not terminated this round gains 2 points, regardless of partner fate. (fixes: Team survival bonus gave both Informants 2 points only if no Informant was terminated, so an Informant lost the bonus because its partner was terminated in 14 of 80 Informant rounds, punishing play it could not control.): Rewards own survival and deceptive play instead of punishing a player for a partner error; keeps Informant scoring skill-sensitive.

Objective: After 10 rounds the player with the highest total points wins. Tie-break: among tied, most Rebel points wins; if still tied, most Informant points wins; if still tied, draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. Payoff table per round (R=Rebel, I=Informant): R votes I: +2 individual + team +1 if any I terminated (shared to all 3 R) => 2 or 3. R votes R: +0 + team 0/1 => 0 or 1. So voting believed-I dominates voting believed-R by +2 whatever termination does. I: +1 per R voting R (0-3 shared to both I) +2 if
- playable: pass. Complete/unambiguous: setup pair-list shuffle, r=1..10 pair=I rest=R, ROLES private + partner to I, NIGHT simultaneous target other, RESULTS rule for R only, CLAIMS simultaneous short message then show, RESPONSES simultaneous then show, VOTE simultaneous for other then publish who-for-whom, TERMINAT
- reasoning_over_luck: pass. Chance ~0-5%: only random event is secret shuffle of 10 pairs pre-game; per-round investigation/framing/votes/talk have no dice. Role counts equalized by design (each player I 4x with each partner once, R 6x), so shuffle changes order only, not totals. If all follow intended good strategy (R investi

## Complexity

- steps_per_round: designed 9, built 13, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 6, built 26, limit 20 (built: 80)
- hidden_elements: designed 3, built 8, limit 3
- random_draws_per_round: designed 0, built -, limit 1
- rounds: designed 10, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Round 1 Informants are first pair in order
- pass: Roles assigned so terminated reveal Informant and Rebel
- pass: Every player names another player as night target
- pass: Informant framing partner has no extra scoring effect
- pass: Rebel true Informant on Informant and true Rebel when unframed
- pass: Starting from zero one round gains as computed
- pass: Round 1 pair is the Informants
- pass: Last pair covers remaining seats as Informants
- pass: Private roles distinguish Rebel and Informant reveal
- pass: Every player names another night target
- pass: Informant may frame partner with no extra scoring effect
- pass: Rebel true Informant target votes correctly
- pass: Framed Rebel looks Informant yet scoring follows votes
- pass: Informants get no result but still score survival
- pass: Claims broadcast then voting proceeds
- pass: Responses broadcast then voting proceeds
- pass: Every player names another to Terminate
- pass: No two votes nobody terminated
- pass: Tie for most votes all tied terminated
- pass: Only terminated roles revealed
- pass: Rebel correct vote gains two
- pass: Rebel team bonus for terminated Informant
- pass: Informant gains per misdirected Rebel
- pass: Informant survival gains two
- pass: Points split into Rebel and Informant pools
- pass: Only votes and terminated roles announced
- pass: Terminated still play next round all five vote again
- pass: Final round announces totals and ends

## Does the file follow the spec's shape? (flags for a person)

- rule R24 has no scenario: nothing checks it

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [5], results {'seat 1': 6, 'seat 5': 5, 'seats 1 and 5': 1, 'seat 2': 4, 'seat 4': 2, 'seat 3': 1, 'seats 1 and 2': 1}, 200-200 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 200.0 decisions, prompts of 75 characters on average (longest 104)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 1': 18, 'seat 5': 14, 'seats 1 and 5': 1, 'seat 2': 10, 'seat 4': 10, 'seat 3': 5, 'seats 1 and 2': 1, 'seats 4 and 5': 1}
- always `first@seat1`: won 7, lost 53, drew 0
- always `first@seat2`: won 9, lost 51, drew 0
- always `last@seat1`: won 5, lost 52, drew 3
- always `last@seat2`: won 6, lost 54, drew 0

## Triage (whose problem each failure was)

- round 1: fix_tests: With votes 3,3,4,1,1 seats 1 and 3 have 2 votes each for the most, so per R14 they must be terminated, not seat 4; the tests expect the opposite 0-indexed mapping and a 0 informant count.

## Choices the rules did not make

- 5 to 5 players, suggested 5: designer set 5; minimum 5 because 2 Informants versus 3 Rebels plus framing and 2-vote termination needs a minority that can hide; maximum not larger because 10-pair schedule and vote math are built for 5
- simultaneous poll for night, claims, responses and votes: source says simultaneous, so poll with nobody seeing answers until all are in; ask not used because order must not leak
- rank_by you.total_points * 1000000 + you.rebel_points * 1000 + you.informant_points: encodes total first then Rebel points then Informant points as tie-breaks within one arithmetic expression; scaling exceeds max attainable points
- talk kept as two simultaneous polls with broadcast to all: claims and responses give material to reason about and players disagree because Informants want misdirected votes and Rebels want true votes, so following a proposal could cost them

## Simplifications

- pair schedule stored as secret game list pair_order drawn by position each round: to fit shared_deck_draw workaround with remove/append operations and no extra randomness
