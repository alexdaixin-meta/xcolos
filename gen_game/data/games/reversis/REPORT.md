# reversis: ready for review

Built from the variation **Quick Reversis** (design round 2); see VARIATION.md.

## What was changed from the original, and why

- Each round is exactly one trick with two choice steps. First the leader plays one card. Then the other three players choose their cards at the same moment in a single simultaneous poll. There is no passing round and there are no individual follow turns. (fixes: P1: The built game had 6 choice steps per round, over the limit of 4.): This brings choice steps per round to 2, well under 4.
- Followers commit at the same moment, so no follower sees another follower's card before choosing. Each of the 4 hands begins with a different player leading (player h leads trick 1 of hand h), so every seat leads the opening trick exactly once. (fixes: P2: Seat imbalance.): This removes the last-to-play information edge and evens out opening leads across seats.
- The deck is 24 cards (A K Q J 9 8 in four suits) dealt 6 to each player. Each hand is 6 tricks, and there are 4 hands, so 24 rounds. There is one shuffle-and-deal per hand, in that hand's first round. (fixes: P3: Luck of the deal is large in a single long hand.): Four short hands average out the luck of the deal and keep the game short. There is at most one random draw per round.
- Pools, side payments and bonus variants are dropped. The only scoring is penalty points and the reversis adjustment. The Quinola is kept as the single heaviest card (5 points). (fixes: P4: Pools, side payments and bonus variants add rules without adding reasoning.): This keeps the game's identity while making the winner pure arithmetic.
- The reversis is tracked with one table attribute, the sweeper: the player who has won every trick so far this hand, or none. At the end of a hand, if a sweeper remains, that player subtracts the 44 points they took and each other player adds 15. (fixes: P5: Too many attributes would be needed for the reversis check.): This avoids per-player trick counters and per-hand point totals.

Objective: After 4 hands, the player with the lowest total wins. If two or more players tie for the lowest total, the game is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. Point check: Aces 4x4=16, Kings 4x3=12, Queens 4x2=8, three non-heart Jacks 3x1=3, Quinola 5. Total 16+12+8+3+5=44, which matches the stated 44. So each hand distributes 44 points and a player's fair share is 11. Seat fairness: the first leader of hand h is seat h, so each of the 4 seats opens exact
- playable: pass. The rules are complete. The deck is 24 cards, all dealt (6x4), and there are 6 tricks per hand. The rules cover the leader's free lead, the must-follow constraint, free discard when void, the trick winner (highest card of the led suit is always unique), scoring, the sweeper tracking (set on trick 1,
- reasoning_over_luck: pass. There is something to infer, and a way to act on it. The full deck is in play, so each player knows the 18 unseen cards exactly and can track them as they fall. Players can infer voids when an opponent discards off-suit. They can also judge whether the leader can be undercut: a follower sees the led

## Complexity

- steps_per_round: designed 14, built 16, limit 20
- choice_steps_per_round: designed 2, built 2, limit 4
- attributes: designed 14, built 41, limit 20 (built: 80)
- hidden_elements: designed 1, built 7, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 24, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Every total starts at 0
- pass: First hand deals 6 cards each and empties the deck (5 left after trick 1, deal is random)
- pass: Hand 4 starts at round 19 with a fresh deal (who wins the trick depends on the random deal)
- pass: A new hand starts at round 7 after a sweep in hand 1 (random deal)
- pass: Each player holds their own dealt hand (random deal)
- pass: Leader may lead any card; KD sets led suit D
- pass: A follower holding the led suit must follow it
- pass: A follower void in the led suit may play any card
- pass: All three followers' cards are revealed after the poll
- pass: An off-suit ace does not win; the highest card of the led suit does
- pass: The Quinola (JH) counts 5: AH+JH+8H+KC = 12 to seat 3
- pass: Played cards leave the hand: each hand drops from 5 to 4
- pass: First trick of a new hand is played after a broken hand (winner depends on the random deal)
- pass: A later trick won by a non-sweeper sets sweeper to 0
- pass: The trick winner leads next
- pass: Totals after a trick are as announced
- pass: Reversis: seat 2 takes all 6 tricks, loses 44 and others gain 15
- pass: No sweeper at hand end: no adjustment
- pass: Game ends after round 24; lowest total wins
- pass: Tied lowest totals share the win
- pass: A trick plays through with only card choices (no talk)

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [4], results {'seat 1': 9, 'seat 2': 5, 'seat 4': 6}, 52-63 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 96.0 decisions, prompts of 206 characters on average (longest 232)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 1': 18, 'seat 2': 15, 'seat 4': 20, 'seat 3': 5, 'seats 1 and 3': 1, 'seats 2 and 4': 1}
- always `first@seat1`: won 17, lost 42, drew 1
- always `first@seat2`: won 12, lost 44, drew 4
- always `last@seat1`: won 17, lost 43, drew 0
- always `last@seat2`: won 13, lost 45, drew 2

## Triage (whose problem each failure was)

- round 1: fix_tests: The rules make the first round of each hand the passing round, with the 6 trick rounds coming after it. After `rounds: 1` each player should therefore still hold 6 cards (dealt, then 2 passed and 2 received), which is exactly what the game showed: deck empty, every hand 6 cards, trick_number 0. The tests wrongly expect every hand to be empty after only one round.
- round 1: revise_rules: The game was built correctly, but the design needs 6 choice steps per round, over the limit of 4. The extra steps come from the passing choice plus four trick plays in seat order starting from a leader who changes. Against random seats the results are also lopsided, with seat 4 winning 21 games and seat 2 only 10.

## Choices the rules did not make

- 4 players: min 4, max 4, suggested 4: The designer fixed 4. The 24-card deck deals exactly 6 cards to each of 4 players, and the 44-point and 15-point values assume this size. Fewer seats would leave cards undealt and change the avoidance tension; more would not fit the deck.
- The sweeper's 'none' is encoded as 0: Seats are 1 to 4, so 0 marks no sweeper unambiguously as a number.
- Card ranks are encoded as numbers (A=6, K=5, Q=4, J=3, 9=2, 8=1): This lets the trick winner be found by arithmetic comparison within the led suit.
- Card names are written as rank followed by suit letter (for example JH is the Quinola): Hands, the deck and played cards need a compact text form.
- No talk step: The source says there is no table talk.
- The leader is asked with ask; the followers answer with poll: The source plays the lead face up first, then has the other three choose at the same moment.
- Ranking expression 0 - total: The engine picks the highest value, and the source's winner is the lowest total. A tie at the top is shared, which matches the source's draw.
- Strategy at the table: A thoughtful player sheds high-point cards (especially the Quinola) when void in the led suit, ducks under the current high card, tracks which cards have left the hand, and judges when to try a reversis or deliberately break an opponent's sweep.

## Simplifications

- The reveal of the three simultaneous cards is a tell after the poll: The engine reveals the polled answers together once all are in, which matches 'all cards are revealed together'.
- The trick winner's tricks_this_hand counter is added: It is a scratch counter that makes 'took all 6 tricks' checkable. The sweeper alone already decides the reversis.

## Encoding attempts

- 1: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (follow, played_card, played_card, played_card) in `your_hand`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 2: it plays, but part of it does nothing: game attribute `full_deck` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 3: passed
