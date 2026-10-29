# king_up: needs review

Built from the variation **King Up: Fair Throne** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Use 3 characters per player (9 for 3 players, 12 for 4, 15 for 5) and deal each player a disjoint triple from one shuffle. Every character is favoured by exactly one player. (fixes: P1): Every seat gets the same goal structure. No seat has built-in allies or can be dealt a duplicate goal, and the sound 3-player logic (owner gains +5 if crowned, loses 5 if eliminated, non-owners only care about game length) carries over to every player count.
- Set the round limit by player count: 15 rounds for 3 players, 16 for 4 and 15 for 5. (fixes: P2): Each limit is a multiple of the player count, so every seat is first raiser equally often (5, 4 and 3 times). Raises still outnumber what heights 0-4 can absorb (45>36, 64>48, 75>60), so pushes to the throne are eventually forced.
- Define seat order once: ascending seat number, wrapping from the highest seat to seat 1. Both the raise sequence and the first-raiser rotation follow it. (fixes: P3): Removes the ambiguity between 'left' and seat order.
- Store status inside each character's height: -1 means eliminated, 6 means king, 0 to 5 means active. (fixes: P4): One attribute per character. That gives 15 heights plus goal, No cards, round number and first raiser = 19 attributes at 5 players.
- Give every player 2 secret No cards at every player count. (fixes: P5): With 3n characters and 2n No cards, vetoes stay scarce and strategic but meaningful at 5 players. The game still ends by a king or the round limit.

Objective: The player with the highest score wins. If two or more players tie for the highest score, the game is a draw among them.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. PAYOFF STRUCTURE. Each player owns 3 of 3N characters, and no two players share one. The deal is symmetric: all characters start at 0 and none has a built-in value. Values: at height h (0 to 5) the owner scores h; eliminated (-1) scores 0; king scores 10. A safe character stops at 4, because reachin
- playable: pass. RULES ARE COMPLETE.
- Height encodes status (-1, 0-5, 6).
- Only one character can be at 5 at a time, and the 4->5 rule makes the candidate unique.
- Election happens once per round after all raises.
- Pass is defined (no legal raise).
- A player out of No cards must vote Yes.
- Only the number of N
- reasoning_over_luck: pass. CHANCE. The only random element is the setup shuffle, and it is payoff-symmetric because all characters are equivalent. Chance's share of the result is roughly 0%. With all players following good play (fill own characters to 4, veto others, attack the leader), the result is decided by the attack and

## Complexity

- steps_per_round: designed 11, built 14, limit 20
- choice_steps_per_round: designed 3, built 3, limit 4
- attributes: designed 19, built 44, limit 20 (built: 80)
- hidden_elements: designed 3, built 8, limit 3
- random_draws_per_round: designed 0, built -, limit 1
- rounds: designed 16, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup with 3 players: A-I in play from 0, J-O not in play (one round of raises on A, B, C)
- pass: Setup with 4 players: A-L in play from 0, M-O not in play
- pass: Setup with 5 players: A-O all in play from 0
- pass: Setup deals 3 goal labels to each seat and empties the deck
- pass: Every seat starts with No cards, so every seat is offered No in the first election
- pass: 3 players: game ends after round 15
- pass: 4 players: game continues past round 15 and ends after round 16
- pass: 5 players: game ends after round 15
- pass: Seat 1 raises first in round 1: it alone sees both 4s, then A at 5 blocks B for the others
- pass: A round begins with the round number advanced and the raises applied
- pass: Talk step runs and the round completes normally
- pass: Each of 4 seats raises one character by exactly 1
- pass: Eliminated (-1) and king (6) characters are never offered
- pass: A character at 5 may not be raised further by later seats
- pass: With A at 5, B at 4 may not be raised
- pass: A character at 4 with none at 5 is offered and can be raised to 5
- FAIL: With every character eliminated, each seat can only pass and nothing changes | rule R12 is broken: When a player has no legal raise, then that player passes and no height changes.; seat 1 was never offered 'pass', but should have been; seat 2 was never offered 'pass', but should have been; seat 3 was never offered 'pass', but should have been; Ada: the rule for 'pass' was never matched (the game never put that option to this seat); Blaise: the rule for 'pass' was never matched (the game never put that option to this seat); Cleo: the rule for 'pass' was never matched (the game never put that option to this seat)
- pass: No character at 5: no election is held
- pass: A character at 5 triggers an election with Yes and No offered to every seat
- FAIL: A seat with no No cards is offered only Yes | rule R15 is broken: When a player has no_cards = 0, then that player may vote only Yes.; seat 2 was never offered 'Yes', but should have been
- pass: All Yes crowns the candidate and the game ends that round
- FAIL: A No vote eliminates A and spends the voter's last No card, so D is crowned next round | rule R17 is broken: When at least one vote is No, then each No voter loses 1 No card and the candidate's height becomes -1 for the rest of the game.; Ada: the rule for 'Yes' was never matched enough (the game never put that option to this seat)
- pass: Election announces the number of No votes
- pass: First raiser wraps from seat 3 to seat 1: seat 1 takes A to 5 in round 2 before seat 3 can take B
- pass: Reaching the round limit without a king ends the game
- pass: Scoring: 10 for king, 0 for eliminated, height otherwise
- pass: Two seats tied on the highest score share the win
- pass: All seats level share the win

## Does the file follow the spec's shape? (flags for a person)

- the spec has players being eliminated but the game file has no status for a player who is out (one with `acts: false`, set with `set_status`): the platform and the console keep showing eliminated players as still playing

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 5], results {'seat 1': 11, 'seats 2 and 3': 1, 'seat 3': 6, 'seat 2': 10, 'seats 3 and 5': 1, 'seat 4': 6, 'seat 5': 5}, 39-156 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 94.0 decisions, prompts of 152 characters on average (longest 188)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 1': 23, 'seats 2 and 3': 1, 'seat 3': 21, 'seat 2': 15}
- always `first@seat1`: won 23, lost 37, drew 0
- always `first@seat2`: won 16, lost 44, drew 0
- always `last@seat1`: won 22, lost 37, drew 1
- always `last@seat2`: won 16, lost 44, drew 0

## Triage (whose problem each failure was)

- round 1: fix_tests: The rules say a player with no legal raise simply passes, and a player with no No cards must vote Yes. Neither is a real choice, so a correct game may skip that seat or record the forced action without polling it. The R12 run shows the game playing correctly: seat 1 raised I to 5, seats 2 and 3 had no legal raise and were skipped, everyone voted Yes, and I was crowned with the right scores. The tests fail because they demand that 'pass' and 'Yes' be offered as options to seats that do not act.
- round 1: fix_tests: The game handled R17 correctly: the No voter (seat 2) lost its last card, A became -1, seat 2 was not polled in round 2 because it had to vote Yes, and D was crowned. The h_b/h_e mismatch comes from the test's own scripted raise: in round 2 seat 1 raised B, which the game offered and played legally. The test assumed seat 1 would raise E.
- round 1: fix_tests: In every failing scenario the seat had no real choice: it had no legal raise, or no No cards left so it must vote Yes. The game resolved these forced moves automatically and the heights stayed correct (all -1, unchanged in the all-eliminated case). The tests fail only because they demand that a 'pass' or 'Yes' option be put to a seat that, by the rule under test, does not actually choose.

## Choices the rules did not make

- 3 to 5 players, suggested 4: The designer's suggested size is 4 and is kept. 3 is the minimum because with fewer players secret goals are easy to deduce and there is no group to veto against. 5 is the maximum because the label set only goes up to O, and with more players each player's raise and veto would matter little.
- Talk as a simultaneous poll broadcast to all: The rules say messages are written at the same time without seeing the others. Talk earns its place because players' goals conflict: players bluff about which characters they favour and try to steer others into spending No cards.
- Score computed only at game end: The rules reveal goals only at scoring, so a running public score would leak the secret goals.
- Unused letters set to height -2: This keeps a fixed set of 15 height attributes for every table size while marking the unused letters as never raisable and never in any goal.
- Strategy at the table: A thoughtful player hides their goal, raises characters that help them without revealing them, saves No cards for candidates that help rivals more, and reads the No counts and others' raises to infer goals. A thoughtless player rushes one favourite to 5 and gets it vetoed.

## Simplifications

- Characters stored as 15 fixed height attributes h_a..h_o rather than a variable-length list: Arithmetic and per-character options are simpler on named numbers. Letters not in play are fixed at -2 and never offered.
- Election and resolve steps carry a 'when candidate is not empty' condition instead of being skipped as a block: The step list is flat. Each step is gated individually by the same arithmetic condition, which matches the rule exactly.
- The secret vote is stored in a per-player vote attribute visible only to its owner: This is needed to deduct No cards from the No voters while announcing only the count.
