# ultimatum_game: ready for review

Built from the variation **Hidden-Pot Ultimatum (Three Players)** (design round 2); see VARIATION.md.

## What was changed from the original, and why

- Three players. The Proposer seat rotates in snake order 1,2,3,3,2,1 over 6 rounds, so each player proposes exactly twice. The two Responders choose at the same moment, so neither is 'first'. (fixes: Seat imbalance: a 1-2-3 proposer rotation, with the lower seat always first Responder, left seat 3 winning far less often even against random play.): Three players break the zero-sum difference trap. The snake order gives every seat one early and one late proposal. Simultaneous responses remove the lower-seat ordering.
- The deal passes only if BOTH Responders accept. If it fails, the Proposer loses one third (rounded down) of the amount they tried to keep. (fixes: Offering the minimum and always accepting is near-dominant. In the previous variation the 'first option' policy won 100% of games against random seats.): A stingy offer that gets vetoed now costs the Proposer heavily. A generous offer risks little, but hands rivals points. Both ends of the offer range are risky. Against purely random responders (25% pass), the penalty makes the expected value of proposing about zero for any keep, so lowballing no longer beats random play.
- Every Responder who rejects pays 1 point. (fixes: Rejection must not become free either. If only the Proposer pays for a failed deal, 'always reject' quietly drags rivals down and becomes a thoughtless winning policy.): A veto must be worth its cost. Always-reject now loses about 4 points over the game and never earns as a Responder, so it falls behind.
- The pot is hidden. Each player proposes once with a pot of 12 and once with a pot of 24, in a secret random order. Only the Proposer knows the current pot. Offers are capped at 0–6 per Responder. Pots, keeps and running totals stay private until the game ends; only offers, votes and pass or fail are public. (fixes: The pot is public, so there is nothing to infer. The Responder can compute the Proposer's keep exactly.): Responders must infer from an offer (and any talk) whether the Proposer is splitting fairly or lowballing a big pot. Proposers with a big pot want to look like they have a small one. Because every player gets the same two pots, the draw changes what players know, not who is ahead.
- Every player gets the same pair of pots (12 and 24); only the order is random. (fixes: A random pot size per round would be a lottery: whoever is dealt bigger pots as Proposer gets ahead for no reason.): The random draw affects only information and timing, not total opportunity, so it is not a lottery.
- Six rounds, the highest final total wins outright, and a tie for highest is a draw. A simultaneous one-message talk phase is held before each offer. (fixes: With two players and 'higher total wins', only the difference matters, so the game is a forced 50/50 draw. The one-shot form has no repeated-play reasoning at all.): Repetition lets players build a reputation and retaliate. Talk lets Proposers claim a pot size (truthfully or not) and lets Responders threaten vetoes. Interests conflict because only one player can win.

Objective: The player with the strictly highest final total wins. If two or three players tie for the highest total, the game is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. PAYOFFS PER ROUND. Pot P is 12 or 24. Offers are a and b, each from 0 to 6. Keep k = P - a - b, which is always at least 0 because a + b <= 12 <= P.
- Deal passes: Proposer +k, Responder A +a, Responder B +b.
- Deal fails: Proposer -floor(k/3), and each rejecter -1.

SWING CAUSED BY ONE REJECTION (o
- playable: pass. Rules are complete:
- Offer ranges 0-6 guarantee keep >= 0.
- The fail case is fully specified, including rounding (keep 0 loses 0) and both responders rejecting (each -1).
- The second pot is deterministic.
- The winner is the strict highest total, otherwise a draw.

The game is finite at 6 rounds 
- reasoning_over_luck: pass. The only random element is the coin deciding whether each player's 12 or 24 comes first. Every player receives exactly 12 + 24 = 36 in pots, so chance changes only ordering and information, not endowment. Its share of the outcome is small, roughly under 10%.

Under intended good play, results are de

## Complexity

- steps_per_round: designed 13, built 16, limit 20
- choice_steps_per_round: designed 3, built 4, limit 4
- attributes: designed 13, built 34, limit 20 (built: 80)
- hidden_elements: designed 2, built 10, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 6, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Start: every total is 0
- pass: Round 1 is proposed by seat 1 and only seats 2 and 3 vote (proposer keep is random, so not asserted)
- pass: Round 4 is proposed by seat 3 again
- pass: Round 6 is proposed by seat 1
- pass: First proposal uses a coin-flipped pot (only the chance-free responder payouts are asserted)
- pass: Second proposal uses the stored other pot (12): keep 12-2-3 = 7
- pass: Whole game with zero offers all accepted: each seat's two pots sum to 36 whatever the coins, three-way tie
- pass: Pot is private: responders are never asked for offers
- pass: Talk step does not change the round's outcome
- pass: Offers range 0 to 6 and may differ (2 to seat 2, 5 to seat 3)
- pass: Pot 24, offers 3 and 5: keep 16
- pass: Pot 12, offers 6 and 6: keep 0, so a rejection costs the proposer nothing
- pass: Both offers are announced as public offer values
- pass: Votes are recorded: seat 2 accept, seat 3 reject
- pass: Both accept: responders get their offers, proposer gets keep 24-4-6 = 14
- pass: One reject with keep 18: proposer loses 6, nothing is paid
- pass: Reject with keep 12 (pot 24, offers 6 and 6): proposer loses 4
- pass: Both reject with keep 2: proposer loses 0, each rejecter loses 1
- pass: After a round each total reflects only that round's payout
- pass: Game ends after round 6 and totals may be negative
- pass: Single highest total wins
- pass: Two seats tied for the top: nobody wins

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [3], results {'seat 2': 10, 'seat 3': 6, 'seat 1': 3, 'no winner decided (no seat reached the minimum to win)': 1}, 42-42 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 42.0 decisions, prompts of 231 characters on average (longest 329)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 2': 23, 'seat 3': 18, 'seat 1': 17, 'no winner decided (no seat reached the minimum to win)': 2}
- always `first@seat1`: won 16, lost 41, drew 3
- always `first@seat2`: won 19, lost 38, drew 3
- always `last@seat1`: won 34, lost 16, drew 10
- always `last@seat2`: won 38, lost 13, drew 9

## Triage (whose problem each failure was)

- round 1: fix_tests: In every failing scenario the move log shows both Responders answering 'Accept', not 'Reject'. The game then correctly paid the Proposer pot - a - b, which gives 70+90+110+130 = 400 each over a full game, 130 in round 1 and +70 in the round-12 case. The game follows the rules; the tests assumed rejections they never actually scripted, since the 'decline' default resolved to Accept.
- round 1: revise_rules: The game file is correct; the design is degenerate. A single Accept passes the deal and rejecting never costs a Responder anything, so offering 0/0 keeps nearly the whole pot and accepting is never worse than rejecting, which is why the 'first option' policy wins every decided match and the 'last option' policy loses every one.

## Choices the rules did not make

- Exactly 3 players, suggested 3: The designer fixed the table at 3. The proposer schedule (1,2,3,3,2,1) and the two-Responder unanimity rule are built for exactly three seats, so no other size is defined. The minimum is 3 because the schedule needs three seats, and the maximum is not larger because the schedule names only three.
- Keep the simultaneous talk step as a poll with a broadcast: The rules require it. It earns its place because the Proposer's interest (claiming a small pot to justify low offers) conflicts with the Responders' interest (believing the pot is large and demanding more), and Responders can coordinate threats to reject.
- The coin flip is made at each seat's first proposal, and the second pot is stored in hidden table attributes second_pot_s1, second_pot_s2 and second_pot_s3: This matches the source exactly: no seat learns its pot order before its first proposal, so the order stays secret until then.
- The two offers are asked as two consecutive number questions to the Proposer, lower-numbered Responder first: A question takes one whole number. The Proposer answers both before anyone sees them, because the offers are only announced afterwards.
- Strategy at the table: A thoughtful Proposer weighs bluffing about the pot against the risk of a rejection that costs a third of the keep. A thoughtful Responder judges whether an offer is fair given the hidden pot, remembers that rejecting costs 1 point, and uses the reversed schedule (rounds 4 to 6) to reward or punish earlier Proposers.

## Simplifications

- A draw (a tie for the top total) is expressed as 'nobody wins' through min_to_win = top_total + 1000 * (top_count - 1): The engine shares the win among tied leaders by default. Raising the bar out of reach when more than one player holds the top total reproduces the source's 'tie is a draw' with no winner.
- Totals are switched from owner-only to public at the end of round 6: The source reveals every total at the end, so the end-of-game reveal is done by changing visibility as well as by announcement.

## Encoding attempts

- 1: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state a player is shown has empty fields (vote, vote); hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 2: passed
