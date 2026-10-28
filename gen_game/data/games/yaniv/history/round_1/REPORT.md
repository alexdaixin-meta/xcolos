# yaniv: needs review

Built from the variation **Simultaneous Yaniv: Claims** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- The first hands are dealt at setup, before round 1. Every later re-deal happens inside the showdown resolution of the round in which someone called. The blind card is drawn only in rounds with no call. Each round therefore has exactly one random draw (a blind card or a re-deal, never both), and round 1 has none. (fixes: P1): This keeps random_draws_per_round at 1.
- The face-up card is removed. After the simultaneous discards, each player's discard set is laid out publicly as that player's offer. In a single card or an equal-value set, one card is available. In a run, two cards are available: the lowest and the highest. Each non-caller then secretly claims one available card from another player's offer, or takes BLIND. If two or more players claim the same card, none of them gets it and all of them take BLIND. (fixes: P2): This restores Yaniv's core skill of taking the edge card of someone's discard, and adds contest and denial. You must predict who else wants a card. Your discard becomes a choice of what to offer rivals: a low single card helps them, while a high card or the middle of a run is safe.
- Runs are restored as 3 or more cards of consecutive values (suits ignored; Ace = 1 is low; Joker is not part of runs; a run cannot use two cards of value 10). (fixes: P2): Runs give a second way to shrink the hand and create two-ended offers, which makes claims richer. This keeps more of Yaniv's identity.
- The blind card is shown privately, and only to the players who took BLIND. Everyone sees who took BLIND and who claimed which card, but not the blind card's value. It is revealed only at a showdown. (fixes: P3): Each player's hand stays partly hidden throughout a deal, so estimating opponents' sums from their discards, claims and BLIND takes becomes real inference.
- The call threshold is lowered from 10 to 7, as in standard Yaniv. (fixes: P4): Reaching 7 or less needs several rounds of shedding and good pickups, so calls come later and depend on reading whether a rival is also low.
- The game ends when a total reaches 150 after a showdown, or after round 40 with a forced final showdown (no Asaf, lowest hand sum scores 0). (fixes: P5): This gives more deals to average out luck while still guaranteeing an end within 40 rounds.
- The rules are reworded so that the blind card is described only as drawn in the resolution step. (fixes: P6): This removes the ambiguity about when the blind card exists.

Objective: When the game ends, the player with the strictly lowest total wins. If two or more players tie for the lowest total, the game is a draw.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. SHOE ODDS. 0: 2/54 (3.7%). Each of 1-9: 4/54 (7.4%). 10: 16/54 (29.6%). Mean card value = (4*45 + 160)/54 = 340/54 = 6.30, so a fresh 5-card hand averages about 31.5. A hand can only shrink through sets or runs: discard one and draw one keeps the size, a pair is -1 net, a 3-run is -2 net. CALL needs
- playable: pass. RULES COMPLETE FOR EVERY CASE:
- A 1-card player must CALL if allowed. Otherwise they discard nothing but still make the second choice and draw.
- Illegal answers have defaults: highest single card, discard nothing, or BLIND.
- When someone calls, all discards are cancelled.
- A run offers its low a
- reasoning_over_luck: pass. WHAT CAN BE INFERRED:
- Opponents' hand sums, from hand size and their public discard history. A player who discarded a pair of 9s, then a single 10, is now holding 2 cards.
- What BLIND co-takers hold. BLIND takers all receive the same card, so each knows what the others got.
- Whether to call now 

## Complexity

- steps_per_round: designed 14, built 20, limit 20
- choice_steps_per_round: designed 2, built 2, limit 4
- attributes: designed 14, built 44, limit 20 (built: 80)
- hidden_elements: designed 2, built 13, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 40, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: R1: setup deals 5 cards to each seat (values random, only the counts are asserted)
- pass: R2: before round 1 every total is 0 and each seat holds 5 cards
- pass: R3: CALL is offered at sum 7 and not at sum 8
- pass: R4: a pair whose full discard would empty the hand discards exactly one card
- FAIL: R5: a 9-10-10 hand never discards an illegal run; the fallback discards one 10 | rule R5 is broken: When a run contains a 0 or more than one 10, then it is illegal; 8-9-10 is legal and 9-10-10 is not.; seat 1 standing: expected -26, got -23; seat 1 total: expected 26, got 23; Ada: the rule for 'seat 3: value 7' was never matched (the game never put that option to this seat); Blaise: the rule for 'seat 1: value 10' was never matched (the game never put that option to this seat); Cleo: the rule for 'seat 2: value 8' was never matched (the game never put that option to this seat)
- pass: R6: a discard may not empty the hand; pairs keep one card
- pass: R7: a 1-card player with sum 3 must CALL and wins the showdown
- pass: R7: a 1-card player with sum 9 discards nothing and still takes a card (hand sizes only, blind value is random)
- FAIL: R8: an illegal first choice becomes discarding the single highest card | rule R8 is broken: When a first choice is illegal, then it is replaced by discarding the single highest card, or by discarding nothing for a player with 1 card.; winner: expected 'seat 1', got 'seat 2'; seat 1 standing: expected 0, got -23; seat 2 standing: expected -14, got 0; seat 3 standing: expected -14, got -19; seat 1 total: expected 0, got 23; seat 2 total: expected 14, got 0; seat 3 total: expected 14, got 19; Ada: the rule for 'seat 2: value 6' was never matched (the game never put that option to this seat); Blaise: the rule for 'seat 3: value 9' was never matched (the game never put that option to this seat); Cleo: the rule for 'seat 1: value 10' was never matched (the game never put that option to this seat)
- pass: R9: a call cancels discards and the showdown scores the hands as they stood
- pass: R10: a caller strictly lowest scores 0
- pass: R11: two callers tied at 6 are both caught and score 36
- pass: R12: non-callers above the lowest sum score their hand_sum
- pass: R13: after a showdown below 150 everyone gets a fresh 5-card hand
- FAIL: R14: discarded cards leave play and do not count at the final showdown | rule R14 is broken: When no one calls, then every discard is announced publicly and leaves play.; winner: expected 'seat 1', got 'seats 1, 2 and 3'; seat 2 standing: expected -13, got 0; seat 3 standing: expected -14, got 0; seat 2 total: expected 13, got 0; seat 3 total: expected 14, got 0; Ada: the rule for 'seat 2: value 10' was never matched (the game never put that option to this seat); Blaise: the rule for 'seat 3: value 10' was never matched (the game never put that option to this seat); Cleo: the rule for 'seat 1: value 10' was never matched (the game never put that option to this seat)
- FAIL: R15: a single-card discard makes one offer that another seat can claim | rule R15 is broken: When a single card or an equal-value set is discarded, then it makes one offer of that value; when a run is discarded, then it makes two offers, its lowest and its highest value.; seat 2 was never offered 'seat 1: value 10', but should have been; seat 3 was never offered 'seat 2: value 9', but should have been; Ada: the rule for 'seat 2: value 9' was never matched (the game never put that option to this seat); Blaise: the rule for 'seat 1: value 10' was never matched (the game never put that option to this seat)
- FAIL: R16: a seat is not offered its own discard (hand sizes only, blind value is random) | rule R16 is broken: When no one calls, then each player chooses BLIND or a claim on one offered card of another player; claiming one's own offer is illegal and becomes BLIND.; seat 2 was never offered 'seat 1: value 10', but should have been
- FAIL: R17: two seats claiming the same card both go BLIND (only chance-proof values asserted) | rule R17 is broken: When two or more players claim the same offered card, then none of them receives it and each is treated as BLIND.; winner: expected 'seat 1', got 'seats 1 and 3'; Blaise: the rule for 'seat 1: value 10' was never matched (the game never put that option to this seat); Cleo: the rule for 'seat 1: value 10' was never matched (the game never put that option to this seat)
- FAIL: R18: a sole claimant adds the offered card to their hand | rule R18 is broken: When exactly one player claims an offered card, then that card is added to that player's hand.; winner: expected 'seat 1', got 'seats 1 and 2'; seat 2 standing: expected -14, got 0; seat 3 standing: expected -13, got -19; seat 2 total: expected 14, got 0; seat 3 total: expected 13, got 19; Blaise: the rule for 'seat 3: value 9' was never matched (the game never put that option to this seat); Cleo: the rule for 'seat 1: value 10' was never matched (the game never put that option to this seat)
- pass: R19: each BLIND seat adds one card (blind value is random, sizes only)
- FAIL: R20: a claim round completes with the round advanced and no score change | rule R20 is broken: When the public result is announced, then it names who claimed which card, which claims failed through contest, and who took BLIND, but not the blind card's value.; Ada: the rule for 'seat 3: value 8' was never matched (the game never put that option to this seat); Blaise: the rule for 'seat 1: value 10' was never matched (the game never put that option to this seat); Cleo: the rule for 'seat 2: value 9' was never matched (the game never put that option to this seat)
- FAIL: R21: round 40 without a call ends with a final showdown, lowest scores 0 | rule R21 is broken: When round 40 ends with no showdown that round, then all hands are revealed, each player at the lowest sum scores 0 and every other player scores their hand_sum.; winner: expected 'seat 1', got 'seat 2'; seat 1 standing: expected 0, got -19; seat 2 standing: expected -12, got 0; seat 3 standing: expected -25, got -23; seat 1 round_score: expected 0, got 19; seat 1 total: expected 0, got 19; seat 2 round_score: expected 12, got 0; seat 2 total: expected 12, got 0; seat 3 round_score: expected 25, got 23; seat 3 total: expected 25, got 23; Blaise: the rule for 'seat 1: value 10' was never matched (the game never put that option to this seat); Cleo: the rule for 'seat 2: value 9' was never matched (the game never put that option to this seat)
- pass: R22: a showdown pushing a total to 150 or more ends the game
- pass: R23: seats tied at the lowest total share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 5], results {'seat 2': 10, 'seat 3': 11, 'seat 1': 9, 'seat 5': 7, 'seat 4': 3}, 221-389 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 312.5 decisions, prompts of 260 characters on average (longest 262)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- always taking the last option as seat 2 wins 88% of decided matches against random seats
- random seats: {'seat 2': 18, 'seat 3': 21, 'seat 1': 20, 'seats 2 and 3': 1}
- always `first@seat1`: won 0, lost 60, drew 0
- always `first@seat2`: won 0, lost 60, drew 0
- always `last@seat1`: won 49, lost 11, drew 0
- always `last@seat2`: won 50, lost 7, drew 3

## Triage (whose problem each failure was)

- round 1: fix_game: The R3 test is consistent with the rules: seat 1 calls with the strictly lowest sum 7 and scores 0, while seats 2 and 3 score 8 and 20. The game ignored the preset hands: the trace shows it building the shoe and value tables and dealing fresh 5-card hands at the start of round 1, so seat 1 never held [3,4] and was never offered CALL. R4–R6 fail the same way, with totals coming from re-dealt random hands.
- round 1: fix_game: The R3 test agrees with the rules: seat 1 at sum 7 calls and is strictly lowest, so it scores 0, and seats 2 and 3 score 8 and 20. The game ignored the scenario's given hands and dealt fresh 5-card hands inside round 1 (seat 1 got [10,10,6,6,10], sum 42), so CALL was never offered. R4 to R6 fail the same way, because the dealt hands overwrite the given ones.
- round 1: fix_game: Several independent scenarios show the game file breaking clear, buildable rules. Discard offers are never put to other seats as claim options. The round-40 final showdown leaves every total at 0. The illegal-choice fallback does not discard the single highest card. Hands lose cards that were never chosen, for example [8,10,10,9,2] became [9,10,10]. These are implementation errors, not problems with the rules or limits of the platform.

## Choices the rules did not make

- 3 to 5 players, suggested 4: 4 is the designer's size and is kept. Three is the minimum for contests over offered cards and for a caller to face more than one rival. More than five makes contests near-certain and the showdown arithmetic too long to follow.
- No talk step: The source has no talk. Strategy lies in reading discards and claims (claiming a card reveals what you hold), timing the call, and avoiding contested claims.
- A 1-card player is offered only the forced option: The rules force CALL (if allowed) or discarding nothing, so no other option is offered.
- Draws are with replacement from a 54-value list: The source reshuffles the shoe before every draw, so the shoe's frequencies never change.
- Each card of a run's two offers is claimable separately: The rules call each one an offered card that a player may claim.

## Simplifications

- The legality of a discard (set or run) is judged by a referee sentence: Checking that values are held and form a set or a valid run is list logic, beyond simple arithmetic. Scoring stays arithmetic.
- A tie for the lowest total is a shared win rather than a declared draw: The engine shares the win among players level at the top. This is the same outcome as the source's draw.
- The lowest total wins via rank_by = -total: The engine ranks the highest value first.

## Encoding attempts

- 1: it plays, but part of it does nothing: game attribute `shoe` is never changed in 3 random matches, so nothing updates it. Steps that name it: fill the shoe. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.; game attribute `all_values` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `value_names` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `idx` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 2: passed
