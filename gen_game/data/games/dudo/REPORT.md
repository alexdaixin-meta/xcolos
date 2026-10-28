# dudo: needs review

Built from the variation **Short Dudo** (design round 2); see VARIATION.md.

## What was changed from the original, and why

- Each round has at most 4 choice steps: an opening bid, up to two responses that can raise by +1 or +2, and a final forced Dudo or Calza. (fixes: Unbounded bidding chains exceed the limit of 4 choice steps per round.): Keeps the round within 4 choice steps while keeping the escalation of bids and the bluff-or-call tension.
- Ones are always wild, and bids may only name faces 2 to 6. There is no switching to aces. (fixes: The ace conversion rules (halve or more than double) add complexity without adding much reasoning at small scale.): Removes a special-case rule chain, while the wild ones still make counting interesting.
- 2 to 4 players with 5 dice each, and a cap of 30 rounds after which the player with the most dice wins. (fixes: Up to 10 players with 5 dice each exceeds the attribute and step budgets, and games can run very long.): Keeps the hidden state within 20 dice and the game short enough to play.
- The separate first-opener draw is removed. Seat 1 opens round 1, and afterwards the loser opens as in the original. (fixes: Previous variation: a separate random draw to pick the first opener put hand 1 at two random draws, over the limit of 1.): Every round, including round 1, then has exactly one random event: the roll. A one-time opening advantage is negligible over many rounds.
- The rules state that each round's roll is one deal operation that produces every player's hidden dice at once, and that N is computed by one count operation over all revealed dice. (fixes: Previous variation: it did not say that the dice roll is a single deal operation, so the roll looked like many independent draws, and it did not say that N is a single count.): Makes random_draws_per_round = 1 true by construction and keeps the step count fixed.
- The opening quantity bound becomes max(1, floor(T/3)) <= Q <= ceil(T/2). (fixes: Previous variation: with T=2 the opening bound floor(T/3)=0 allowed a Q=0 bid. Such a bid is always true, so it is not a claim, and Dudo against it always loses.): Every legal bid is now a real claim of at least one die. At T=2 the only opening quantity is Q=1.

Objective: If only one player has dice left, that player wins. If 30 rounds are completed with two or more players still in, the player holding the most dice wins. If two or more players tie for the most dice, the game is a draw.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. Main decision, 2 players, T=10, both players at 5 dice. Each die matches a named face (that face or a 1) with p=1/3. Each player sees only their own 5 dice, so all that is unknown is the opponent's 5 dice. An opponent's 5 dice yield X matches, with X ~ Bin(5,1/3): P0=.132, P1=.329, P2=.329, P3=.165,
- playable: pass. Rules are complete:
- The opening range max(1,floor(T/3)) to ceil(T/2) is non-empty for every T of 2 or more (T=2 gives [1,1]; T=3 gives [1,2]).
- Raise legality (new Q at most T) and the fallback to Dudo or Calza are specified.
- The final response forbids raising, so each round has at most 4 choic
- reasoning_over_luck: pass. There is real inference at every choice:
- the binomial over the opponents' unseen dice, conditioned on your own hand;
- reading the opener's face choice as evidence of what it holds;
- weighing Dudo against Calza against raising onto your own face to pass the risk on;
- planning the forced final ca

## Complexity

- steps_per_round: designed 14, built 17, limit 20
- choice_steps_per_round: designed 4, built 5, limit 4
- attributes: designed 14, built 35, limit 20 (built: 80)
- hidden_elements: designed 1, built 5, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 30, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: R1 setup: every seat starts with 5 dice and not out; after seat 1 opens and seat 2 calls Dudo, uninvolved seat 3 still holds 5 and nobody is out
- pass: R1 seat 1 opens round 1: only seat 1 is asked the opening quantity (T=15, range 5..8)
- pass: R2 each seat not out gets exactly dice_count dice and an out seat gets none (faces are random, only the counts are checked)
- pass: R3 total_dice counts only seats not out: dice 1,2 and seat 3 out give T=3, so after an opening bid of 2 only Raise +1 is legal
- pass: R4 with T=15 the opening quantity offers 7 and 8 but not 9
- pass: R5 Raise +1 makes the raiser the bidder: seat 3 responds next and seat 1 is not involved in the call
- pass: R6 Raise +2 adds 2: with T=4 a bid of 1 raised by 2 is 3, so the next responder gets Raise +1 but not Raise +2
- pass: R7 with T=3 and the bid raised to 3, the next responder is offered only Dudo and Calza
- pass: R8 with 2 players, response 2 is answered by the opener
- pass: R8 the responder skips an out seat: seat 2 is out, so seat 3 responds to seat 1
- pass: R9 a Dudo on response 1 ends the bidding, so seat 3 is never asked
- pass: R10 the final responder is offered only Dudo and Calza even though raises would fit
- pass: R11 the reveal settles only between bidder and caller (the dice are random): the uninvolved seat keeps its dice
- pass: R12 a Dudo costs a die only to the caller or the bidder (random which): the uninvolved seat keeps 5 and nobody is out
- pass: R13 a Dudo after a raise never touches the original opener (random outcome)
- pass: R14 a Calza changes only the caller's dice (random outcome): the bidder and the other seat keep 5
- pass: R15 a Calza from a 2-die caller leaves it with 1 or 3 dice, never out (random outcome); the others are unchanged
- pass: R16 an out seat is skipped and gets no hand: seat 2 is out and is never asked
- pass: R17 the next opener is the loser of the Dudo between seats 1 and 2, so seat 3 never opens round 2 (random which of 1 or 2)
- pass: R18 when one of two 1-die survivors loses a Dudo the game ends after that round (winner is random)
- pass: R19 after round 30 the game ends and the seat with the most dice wins
- pass: R19 after round 30 the seats tied for the most dice share the win

## Does the file follow the spec's shape? (flags for a person)

- the spec uses `initialize` but the game file does not

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [2, 4], results {'seat 1': 12, 'seat 2': 15, 'seat 4': 9, 'seat 3': 4}, 25-98 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 58.8 decisions, prompts of 166 characters on average (longest 198)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- always taking the first option as seat 1 wins 92% of decided matches against random seats
- always taking the first option as seat 2 wins 97% of decided matches against random seats
- random seats: {'seat 1': 30, 'seat 2': 30}
- always `first@seat1`: won 55, lost 5, drew 0
- always `first@seat2`: won 58, lost 2, drew 0
- always `last@seat1`: won 0, lost 60, drew 0
- always `last@seat2`: won 0, lost 60, drew 0

## Triage (whose problem each failure was)

- round 1: fix_tests: With T = 9 the opening quantity may be anything from 2 to 9, so offering 7 on the quantity prompt is correct. The test treats 7 as forbidden, apparently meaning 'face 7 is out of range', but its exclusion is not tied to a particular prompt, and the legal quantity 7 trips it.
- round 1: revise_rules: The game file works as specified, but one fixed choice dominates. Always taking the first option wins about 90% of decided matches from either seat. Always taking the last option (bidding the maximum T) almost always loses. Because raises may jump straight to any quantity up to T, most bids are wildly false, so calling Dudo or making the smallest bid wins without any thought.
- round 2: fix_tests: The game asks the opener for the face (options 2 to 6) and then the quantity as two separate prompts. Every 'offered but must not be' failure (2 and 6 at T=9, 5 at T=8, 4 at T=15, 2 at T=2) is a legitimate face option, not a quantity. The quantity range itself looks right: at T=9 seat 1 bid quantity 3 and the game recorded current_qty 3.
- round 2: revise_rules: The game was built as specified, so the failures come from the design. Mindless policies decide the outcome: always taking the first option wins 92–97% of decided matches, and always taking the last option (Calza) never wins. The round also needs 5 choice steps, which is over the limit of 4.

## Choices the rules did not make

- 2 to 4 players, suggested 3: The designer suggests 3. Two is the smallest table where a bid can be doubted. Above 4 the 3-response limit means most seats never act in a round.
- No talk phase: The source says bids and calls are the only communication. Bluffing happens through the bids themselves.
- Strategy at the table: A thoughtful player estimates the expected count from their own hand plus T/3 for the unseen dice, bluffs bids toward faces they hold, reads the raises of others, and saves Calza for when they hold the bid face, since a correct Calza gains a die.

## Simplifications

- The opening bid is asked as two questions to the same seat, face then quantity: One answer is either a choice or a number, never both.
- A raise and its face are offered as one combined choice, such as raise2_face4: This lets one choice question carry the raise size and the face, with illegal raises left out.
- A tie for most dice after 30 rounds is a shared top result rather than a separate 'draw' outcome: The engine has no separate draw. Players level at the top share the win, which records the draw.
