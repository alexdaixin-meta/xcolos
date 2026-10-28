# one_night_revolution: ready for review

Built from the variation **One Night Revolution: Ten Nights** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Replace the chained cycle with all 10 possible Informant pairs among 5 players, each used exactly once, in an order shuffled secretly before round 1. The game lasts 10 rounds. (fixes: P1): Every player is an Informant exactly 4 times and a Rebel exactly 6 times, so role exposure is identical. Knowing a past partner only tells you that pair will not recur; it never tells you who is an Informant now.
- Random order of pairs instead of a fixed position chain, and only terminated players' roles are revealed each round. (fixes: P2): No position is structurally tied to the blind first round, and the hidden pair list cannot be reconstructed from public reveals.
- Fully individual scoring per round. A Rebel scores 2 for voting for an Informant, plus 1 if an Informant is terminated. An Informant scores 1 for each Rebel who voted for a Rebel, plus 2 if no Informant is terminated. (fixes: P3): Each player's points come mostly from their own vote or from deceiving specific Rebels. Skill is not shared with whoever happened to be on your team.
- The individual vote reward is now 2 per round as a Rebel (12 possible over the game). Deception points scale with how many Rebels you misled. (fixes: P5): Individual reasoning becomes the main source of points rather than a tiebreaker.
- Arithmetic tiebreak: most points earned as a Rebel, then most points earned as an Informant, then a draw. (fixes: P4): Uniform round outcomes no longer tie everyone, because individual vote accuracy differs.
- State that an Informant may frame any other player, including their partner (which has no extra effect). Any Rebel who investigates a framed player or an Informant sees 'Informant'. (fixes: P6): This removes ambiguity so the night can be built and reasoned about exactly.
- Publicly announce who voted for whom after each vote. (fixes: P1): Gives cross-round evidence for opponent modelling (who frames, who protects whom). Because pairs never repeat, this does not leak future roles.

Objective: After 10 rounds, the player with the highest total points wins. If several players tie, the one among them with the most Rebel points wins. If still tied, the one with the most Informant points wins. If still tied, the game is a draw.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. ROLE SYMMETRY: There are C(5,2)=10 pairs. Each player belongs to exactly 4 pairs, so each player is Informant in 4 rounds and Rebel in 6, with each partner once. The rule's arithmetic is correct. Over the game every player gets the same role exposure, so neither seat nor role count gives an edge. Se
- playable: pass. COMPLETENESS: Every step defines who acts, what is private, what is public, and the arithmetic.
- The investigation result is a single conditional: Informant if (target is Informant) OR (framed by at least one Informant).
- Termination: at least 2 votes required, all tied for most are terminated, on
- reasoning_over_luck: pass. CHANCE: The only random event is the order of the 10 pairs. Role counts are equalised (4 Informant / 6 Rebel each), so luck affects only timing and partner pairing. The night results are deterministic given the choices.

INFERENCE AVAILABLE:
(1) A 'Rebel' result is certain and clears one player.
(2)

## Complexity

- steps_per_round: designed 15, built 17, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 12, built 38, limit 20 (built: 80)
- hidden_elements: designed 2, built 10, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 10, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: R1: totals start at 0, so cyclic votes over 10 rounds give each seat exactly 20 (6 rebel + 14 informant), whichever pairs are scheduled
- pass: R2: pair_order holds the 10 pairs and a round plays from it
- pass: R3: cyclic votes for 10 rounds give everyone 20 points whichever pair is scheduled each round
- pass: R4: each seat is an Informant 4 times and a Rebel 6 times, so cyclic votes give 6 rebel and 14 informant points to each
- pass: R5: a round plays through with private roles; only public results are checked
- pass: R6: the night target is any other seat, never oneself
- pass: R7: a Rebel's night investigation leaves the public state unchanged (results are private)
- pass: R8: framing gives no public change and no points (results are private)
- pass: R9: an unframed Rebel target reveals nothing publicly
- pass: R10: Informants' night choice reveals nothing publicly
- pass: R11: both talk phases happen and the round completes
- pass: R12: every seat votes for another seat, never itself
- pass: R13: cyclic votes (1 each) terminate nobody
- pass: R14: a 2-2-1 split terminates both seats with 2 votes
- pass: R15: only the terminated seat 1 can have a revealed role; the others stay empty
- pass: R16: over all 10 pairs, cyclic Rebel votes on Informants earn 6 rebel points each
- pass: R17: seat 1 is terminated every round; Rebels earn the termination bonus in its 4 Informant rounds
- pass: R18: over all 10 pairs, cyclic misvotes earn each seat 14 informant points
- pass: R19: a terminated Informant gets no survival bonus, so seat 1 ends with 0 informant points
- pass: R20: score equals rebel_points plus informant_points for every seat
- pass: R21: seat 1, terminated every round, still plays all 10 rounds and scores
- pass: R22: the game ends after round 10 and the highest scores win
- pass: R23: seats fully level on score and both sub-totals share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [5], results {'seat 2': 4, 'seat 5': 5, 'seat 1': 6, 'seat 3': 2, 'seat 4': 3}, 200-200 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 200.0 decisions, prompts of 133 characters on average (longest 185)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 2': 9, 'seat 5': 15, 'seat 1': 16, 'seat 3': 9, 'seat 4': 10, 'seats 2 and 3': 1}
- always `first@seat1`: won 5, lost 54, drew 1
- always `first@seat2`: won 10, lost 48, drew 2
- always `last@seat1`: won 4, lost 56, drew 0
- always `last@seat2`: won 5, lost 54, drew 1

## Triage (whose problem each failure was)

- round 1: fix_tests: Every crash happens in scenarios that inject `pair_order` as a list of [a,b] lists. The game stores each pair as a two-digit number, which it is free to do because `pair_order` is internal and not part of the interface. R2, which injects nothing, ran fine, so the game works with its own schedule, and the scoring the tests expect (e.g. R1: 4,4,0,0,2) matches the rules.

## Choices the rules did not make

- Exactly 5 players (min = max = suggested = 5): The designer fixed 5. The schedule of 10 pairs over 10 rounds, with each player an Informant 4 times and partnered with everyone once, only works with 5 seats. Five also leaves 3 Rebels, enough for a 2-Informant minority to hide in.
- Keep both talk phases as simultaneous polls broadcast to all: The rules make both message phases simultaneous. Talk matters because Informants want Rebels to misvote while Rebels want to find the Informants, so following a claim can cost a player.
- rebel_points and informant_points are public: The rules announce everyone's totals and use these sub-totals as tie-breaks; making them public is the plainest reading.
- Rank expression score*10000 + rebel_points*100 + informant_points: Each sub-total stays well below 100 over 10 rounds, so the weights keep the order: score first, then Rebel points, then Informant points. Players still level share the win, which is the draw.
- Player strategy: Rebels compare results and claims, knowing a 'Rebel' result is always true while an 'Informant' result may be a frame. Informants frame Rebels and coordinate a story with their partner. Everyone tracks past pairings, since each pair is Informants only once.

## Simplifications

- The secret schedule is stored as a hidden table list pair_order, and roles are recomputed from it each round: The engine needs the schedule as stated state; this is the rule's own mechanism.
- Which players were framed is kept in a hidden table list framed_seats rather than on each player: A player attribute cannot be hidden from its owner, and a framed player must not learn of the frame; a table list with visibility none keeps it secret.
- Per-round scratch values (votes_received, max_votes, informant_terminated, rebel_misvotes) are held as attributes: The engine computes termination and scoring by arithmetic on stated attributes.
