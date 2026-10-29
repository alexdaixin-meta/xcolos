# big_two: needs review

Built from the variation **Little Two** (design round 2); see VARIATION.md.

## What was changed from the original, and why

- Use a 30-card deck: cards numbered 1 to 30, 10 ranks by 3 suits. Rank = floor((c+2)/3) and suit = c - 3*(rank-1). Rank 10 plays the role of the 2. Deal 9 cards to each of 3 players and set 3 cards aside face down. (fixes: A 52-card deck with five-card poker hands generates too many options, and classifying the hands needs too many steps for the engine.): This keeps hidden hands and card counting. The 3 unseen aside cards mean no one can deduce the remaining hands with certainty, and option lists stay small.
- Allow only four play kinds: single, pair (2 cards of the same rank), triple (3 cards of the same rank) and run (3 cards of three consecutive ranks). The play's value is its highest card number. A triple played on a single or a pair is a bomb. (fixes: A 52-card deck with five-card poker hands generates too many options, and classifying the hands needs too many steps for the engine.): This keeps Big Two's climbing-with-combinations feel, including dilemmas about breaking a pair to make a run, while staying cheap to enumerate.
- Add an explicit play-application procedure. Split the chosen option on spaces into all its card numbers, remove every one of them from the hand, lower card_count by that number of cards, and set pile_kind from the count and ranks. Set pile_value to the highest number, last_player to the seat, and last_action to the whole option string. (fixes: Earlier build defect: a multi-card answer such as '13 14' was applied as its first card only. The play then removed one card, set the wrong pile kind and value, and stored only the first token as last_action.): This removes the first-token bug, so a two- or three-card play removes all its cards.
- Add an explicit legality table and offer format. Options are written as card numbers in ascending order separated by single spaces. Pairs and triples are checked by equal rank under the formula. Each pile kind admits only the listed responses, and nothing else is ever offered or accepted. (fixes: Earlier build defect: the rules did not pin down legality per pile kind precisely enough. Lower or mismatched plays were offered, and pairs and triples were not checked with the rank formula.): This makes the offered list exactly the legal moves, which is what tests R1, R5, R6 and R7 check.
- Play 3 deals and add up penalties. The penalty is the number of cards left, doubled when 7 or more are left, plus 1 for each rank-10 card still held. The lowest total wins. (fixes: A single deal is luck-heavy, and the gambling-style penalty doublings are loosely specified.): Several deals average out the luck of one hand. The 2s penalty preserves the original's 'don't sit on your twos' tension, and the scoring is precise arithmetic.
- Rotate the leader: seat 1 leads deal 1, seat 2 leads deal 2 and seat 3 leads deal 3. (fixes: The leader is set by who holds a fixed low card. Over few deals this gives a random seat edge.): Every seat leads exactly once, so no seat has a built-in edge.
- Define the sequencing exactly. Each orbit, seats act in the order 1, 2, 3. In a deal's first orbit, seats before the leader skip their turn. When it is the turn of the seat that made the last play, the pile is first cleared and that seat leads. (fixes: The turn order around a pile clearance was not spelled out step by step, so the engine could mis-sequence who leads.): Cycling in seat order makes the last player lead naturally after the others pass. This matches test R3.

Objective: The player with the lowest total penalty wins. If two or three players tie for lowest, the one among them with the most deals_won wins. If they are still tied, the game is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. PENALTY TABLE for a loser holding n cards: n=1→1, 2→2, 3→3, 4→4, 5→5, 6→6, 7→14, 8→16, 9→18, plus 1 for each of cards 28, 29 and 30 still held. The winner of the deal scores 0. The step from 6 to 14 is intended: it punishes a hand that barely moved.

SEAT ORDER: leader_seat = deal_number, so each se
- playable: pass. RULES ARE COMPLETE:
- Card rank and suit come from a formula with worked examples.
- The four play kinds are exactly defined, and play value is the highest card number.
- The option list for every pile_kind is spelled out, including bombs and the bans on passing when leading.

CLEARANCE IS SOUND: wi
- reasoning_over_luck: pass. THE DEAL MATTERS: the 9-card deal (pairs, runs, 28-30, triples) is the main chance factor. With only 3 deals I estimate roughly 40-50% of the outcome variance is the cards.

SKILL IS SUBSTANTIAL:
- Card counting is unusually strong. At deal start each player knows its own 9 cards and that 21 are spl

## Complexity

- steps_per_round: designed 19, built 18, limit 20
- choice_steps_per_round: designed 3, built 3, limit 4
- attributes: designed 16, built 39, limit 20 (built: 80)
- hidden_elements: designed 2, built 9, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 40, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: R1 ranks: 13,14,15 make a triple and 13,16,19 make a run
- pass: R2 a higher card number beats a single of the same rank
- pass: R3 runs and triples are offered when leading, other sets are not
- pass: R4 13 14 is a pair, 14 16 is not
- pass: R5 orbit increases by 1 each round
- pass: R6 first deal gives 9 cards each and 3 aside (chance: only counts asserted)
- pass: R7 seat 2 leads deal 2 and seat 1 is skipped in its first orbit (chance: counts only)
- pass: R8 in deal 3's first orbit seats 1 and 2 are skipped and seat 3 leads
- pass: R9 the pile clears when play comes back to the last player
- pass: R10 leading on an empty pile: pass is not offered
- pass: R11 on a single: pass, higher singles and any triple are offered
- pass: R12 on a pair: pass, higher pairs and any triple are offered
- pass: R13 on a triple: only pass and higher triples
- pass: R14 on a run: only pass and higher runs
- pass: R15 passing only sets last_action
- pass: R16 playing a pair removes 2 cards and records the play
- pass: R17 a triple bombs a single and the pile becomes a triple
- pass: R18 emptying a hand wins the deal and skips the rest of the orbit
- pass: R19 penalty: 7 cards with card 30 adds 15, 6 cards with card 28 adds 7
- pass: R20 after the first orbit of deal 2, seat 1 gets its turn (chance: counts only)
- pass: R21 orbit 40 ends an active deal and every seat is penalised
- pass: R22 the game ends when deal 3 is won
- pass: R23 tied lowest penalty and tied deals_won share the win
- pass: R23 tied lowest penalty is broken by more deals_won
- pass: R24 a play is public: card_count, last_action and the pile change for all to see

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [3], results {'seat 3': 7, 'seats 2 and 3': 1, 'seat 2': 8, 'seats 1 and 3': 1, 'seat 1': 3}, 50-81 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 92.0 decisions, prompts of 149 characters on average (longest 150)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- always taking the last option as seat 1 wins 90% of decided matches against random seats
- random seats: {'seat 3': 22, 'seats 2 and 3': 2, 'seat 2': 19, 'seats 1 and 3': 1, 'seat 1': 15, 'seats 1 and 2': 1}
- always `first@seat1`: won 0, lost 60, drew 0
- always `first@seat2`: won 0, lost 60, drew 0
- always `last@seat1`: won 54, lost 6, drew 0
- always `last@seat2`: won 46, lost 14, drew 0

## Triage (whose problem each failure was)

- round 1: fix_game: The game encodes multi-card combinations as concatenated numbers (the pair 13+14 is offered as 1314). That form is ambiguous (123 could be 1+23 or 12+3) and unreadable to the model players, and it is why every test's option for a pair, triple or run ('13 14', '4 5 6', '13 14 15', '10 13 16') was never matched. The rules and tests are consistent: 13 and 14 do form a pair, 4-5-6 is a rank-2 triple, and 10-13-16 is a run of ranks 4-5-6.
- round 1: fix_tests: After seat 2 played 22, seats 3 and 1 both passed, so by the clearing rule the pile was cleared and seat 2 had to lead. Its lead of 3 was legal and emptied its hand, so the game correctly gave card_count 0 and ended the deal. The test wrongly assumed the pile still held 22, making '3' illegal and treating it as a pass.
- round 1: fix_game: In R1 seat 1 sent the move '13 14', which the game itself offered as a pair. The game recorded 'played 13', removed only one card and set the pile to single 13. Multi-card combinations are being parsed or applied wrongly, and the same fault shows in the pair, triple and bomb scenarios (R5, R6, R7).
- round 1: fix_game: In R1 the game offered '13 14' and seat 1 chose it, yet only card 13 left the hand and the pile became a single of 13. The file is resolving a multi-card answer to its first card. The same miscount (seat 1 keeps too many cards, so the pile and the later seats' plays are wrong) explains the R5, R6 and R7 failures, and the tests match the rules.
- round 2: revise_rules: The game is built correctly, but a thoughtless policy (always take the last offered option, which is the biggest multi-card play or bomb) wins 77-90% of games. The rules make dumping the largest play dominant: a triple or run lead is almost never answerable, so shedding three cards at a time beats any real decision.

## Choices the rules did not make

- Exactly 3 players, suggested 3: The designer fixed the game at 3 seats. The clearance rule ('the other two have passed') and the leader rotation over 3 deals assume exactly three seats.
- No talk phase: The rules say there is no talk phase. All information comes from public plays, passes and card counts.
- Turns use ask, one seat at a time: The order of play matters, and each seat must see the earlier plays it has to beat.
- rank_by = deals_won - 10 * penalty: deals_won is at most 3, so a factor of 10 makes a lower penalty dominate and uses deals_won only as the tie-break. Players still tied share the win, which matches the source's draw.
- Strategy at the table: A thoughtful player keeps triples as bombs, holds high cards (28-30) to regain the lead, tracks which high cards are gone, and dumps cards before falling to 7 or more, where the penalty doubles.

## Simplifications

- The legal-play option list is computed by the engine from the seat's hand list and the pile each turn: The engine offers choices from a list. The rules define the options exactly, so they are generated by arithmetic on card numbers rather than typed freely.
- Each deal resets the deck to cards 1..30 and empties hands and aside before dealing: This is the 'shuffle all 30 cards' step expressed as list operations followed by random draws.
- The three seat turns are written out as three fixed blocks of steps, each with a when-condition: The step list is flat. Per-step conditions reproduce the skip rules and the end-of-deal cutoff.

## Encoding attempts

- 1: it plays, but part of it does nothing: game attribute `all_cards` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `card_names` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 2: passed
