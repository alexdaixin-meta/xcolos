# dollar_auction: ready for review

Built from the variation **Escalation Ledger III** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- If two or more tied players RAISE, nobody receives the prize. Each raiser pays the raise cost of 3 and half of their bid. (fixes: P1): Raising against another raiser is now worse than dropping, for H and L alike. Escalation becomes a real chicken game for every value.
- The bid menu is 0, 2, 4, 6 or 8, and the maximum (8) is above an ordinary player's value (6) but below the high value (12). (fixes: P2): No bid is unbeatable. Any player can block H with 8 at a modest cost (6-8 = -2), and H can outbid a lower bid. No bid guarantees anyone a profit.
- The high value drops from 16 to 12, and the ordinary value stays at 6. (fixes: P3): Bidding the maximum in a round where you are not high-value now loses 2 even when uncontested. The maniac bleeds without anyone needing to punish it.
- Players who bid and do not receive the prize pay only half their bid. The winner pays in full. (fixes: P4): Contesting or blocking becomes cheaper than the damage it does. An L who blocks with 8 loses 2 while H loses its gain plus half its bid, so a threat to block is credible.
- Every round is contestable. Ls can profit by winning cheap rounds (bid 2 or 4 against 6), and H must guess how hard to bid without knowing whether its rivals will challenge, and in a round it does not own whether anyone is high-value at all. (fixes: P5): Reading opponents' schedules from their bids and talk now changes the best bid in every round.

Objective: After round 12, the player with the highest total wins. If two or three players share the highest total, they draw.

## The critic (3 review(s) before the rules went to a coder)

- balanced: pass. Payoffs. Value v is 12 in a player's own high round and 6 otherwise. A sole highest bidder nets v-b. Every other bidder pays b/2. Escalation for two tied players at bid b: raise alone gives v-b-3; drop gives -b/2; both raise gives -b/2-3 each.

Escalation tables (row player's payoff vs the other tie
- playable: pass. Rules completeness:
- Bids are even, so all halves are integers.
- Every tie case is covered: 2 or 3 tied players, with one raiser, several raisers, or none.
- Non-tied players pay half their bid.
- The winner pays the full bid, plus 3 if they raised.
- Values per player and round are fully specifie
- reasoning_over_luck: pass. Chance enters only at setup: the type deal and which type goes to nobody.

If everyone plays the intended strategy (owners bid 6 or 8 in their rounds, non-owners mostly stay out), each player banks a similar amount from their own 3 rounds. The winner is then decided by:
- the three value-6 chicken r

## Complexity

- steps_per_round: designed 13, built 10, limit 20
- choice_steps_per_round: designed 3, built 3, limit 4
- attributes: designed 17, built 28, limit 20 (built: 80)
- hidden_elements: designed 1, built 7, limit 3
- random_draws_per_round: designed 0, built -, limit 1
- rounds: designed 12, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: totals start at 0, round 0, schedule deck emptied into seats and unused type
- pass: Prize value is 12 in own high-value round: North sole bid 8 in round 1 gives +4
- pass: Prize value is 6 outside own high-value round: East sole bid 8 in round 1 goes negative to -2
- pass: A round with talk and all zero bids advances the round without changing totals
- pass: Bids 2, 4 and 6 are revealed; sole top bid with no tie means no escalation
- pass: All bids 0: no total changes
- pass: Strict highest bid 8 at prize 12 gives +4; a bid of 4 costs 2; a bid of 0 costs nothing
- pass: Tie at 6: non-tied seat bidding 4 loses 2 and is not asked; tied seats both DROP and lose 3
- pass: Three-way tie at 4, all RAISE: each pays 3 for raising plus half the bid, total -5
- pass: Tie at 6, lone raiser at prize 12 gets +3, dropper loses 3, outside bid 2 loses 1
- pass: Tie at 8 with zero raisers: nobody gets the prize, each tied seat loses 4
- pass: Tie at 6 with two raisers: each raiser loses 3 plus half the bid, total -6
- pass: After the round, bids, escalation choices and totals are visible
- pass: Game ends after round 12; highest total wins
- pass: Game ends after round 12; seats level at the top share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [3], results {'seat 1': 8, 'seat 3': 5, 'seat 2': 6, 'seats 1 and 2': 1}, 72-85 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 79.7 decisions, prompts of 122 characters on average (longest 283)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 1': 25, 'seat 3': 16, 'seat 2': 16, 'seats 1 and 2': 2, 'seats 1 and 3': 1}
- always `first@seat1`: won 32, lost 25, drew 3
- always `first@seat2`: won 20, lost 32, drew 8
- always `last@seat1`: won 36, lost 21, drew 3
- always `last@seat2`: won 29, lost 28, drew 3

## Choices the rules did not make

- 3 players (min, max and suggested 3): The designer fixed the table at 3. Three seats are dealt from four types, so one type stays hidden, which the deduction depends on. A fourth seat would leave no unused type, and fewer seats would remove the multi-way ties.
- Talk kept, as a simultaneous poll broadcast to all: The rules require simultaneous talk. Players disagree over who should win each prize, and claims about one's own schedule can be bluffs, so the talk gives players something to reason about.
- Type stored as schedule_slot = round % 4 value (North 1, East 2, South 3, West 0): This makes the 12-or-6 prize value a single arithmetic test.
- In a no-winner escalation, the tied players pay half the bid as well as the 3 for raising: This follows the rules exactly: every tied player pays half, and raisers have also paid 3.

## Simplifications

- The escalation poll and its resolution are steps that always appear in the round, with a when-condition, instead of a separate block: The engine's step list is flat. A conditional step reproduces step 6 exactly.
- The winner's payment and prize are applied as one net change (prize_value - bid): The arithmetic result is identical.
