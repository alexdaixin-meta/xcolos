# nyet: needs review

Built from the variation **Nyet! Contract Veto** (design round 2); see VARIATION.md.

## What was changed from the original, and why

- The Lone makes a contract. After trump is set, the Lone publicly bids how many tricks (0 to 5) it will take. Exactly the bid scores 6 for the Lone. Missing by one scores 2 for the Lone and 1 for each Pair member. Missing by two or more scores 3 for each Pair member. Every trick won also scores 1 to its winner. (fixes: P1): A weak hand can bid low and succeed, and a strong hand can bid high. Success depends on judging the hand, controlling the play and reading the Pair, not on holding high cards. The main prize, 6, is the same for every hand. A Pair member's goal changes from 'win tricks' to 'make the Lone miss', which can mean pushing tricks onto a Lone that bid low.
- Each trick scores 1 point to the individual player who won it, including Pair members. (fixes: P2): Pair members are now rivals as well as allies. Each wants the Lone to miss, but each would rather take the tricks personally, so tricks separate them.
- Veto in the Nyet style. The two Pair members each secretly ban one colour. The Lone then chooses trump from the unbanned colours (2 or 3 remain), chooses who leads the first trick, and states the bid, all as one choice. (fixes: P3): The Lone can shape the deal to fit the hand: choose a void colour as trump to bid 0, or a long colour to bid high. Pair members must infer the Lone's likely strength from their own holdings before banning. The two choices restore two of Nyet's board lines, trump and first player.
- Drop duplicate dealing. Use fresh random deals, with the contract scoring and Lone control above absorbing hand luck instead. (fixes: P4): Replaying known hands between the same players removes the hidden information that the game depends on.
- Deal 5 cards to each player and leave 5 face down in the Widow (previously 6 cards each and a 2-card Widow). Each deal is one setup round plus 5 trick rounds, 6 deals in total, 36 rounds. (fixes: P5): A quarter of the deck stays unknown, so card counting becomes probabilistic and the Lone's bid is a real estimate. Separate setup rounds keep every round within 4 choice steps.
- Add one simultaneous public message per player in the setup round, before the bans. (fixes: P6): The Lone can bluff about its strong colour to steer the bans. Pair members can propose a split of bans, but they compete for tricks and for the win, so a proposal can be self-serving.

Objective: After 36 rounds (6 deals), the player with the highest total score wins. If two or three players tie for the highest total, the game is a draw.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. Each deal gives out 5 trick points (1 per trick, to whoever wins it) plus a contract payout:

| Contract result | Lone | each Pair member | contract points |
|---|---|---|---|
| T = B | +6 | 0 | 6 |
| abs(T-B) = 1 | +2 | +1 | 4 |
| abs(T-B) >= 2 | 0 | +3 | 6 |

Roles are symmetric over the game. Eve
- playable: pass. Rules are complete:
- Deck 20 = 3x5 + 5 widow.
- Lone schedule is fixed.
- Ban outcomes: same colour leaves 3 unbanned, different colours leave 2. Trump is always available.
- Leader, follow-suit and winner rules are given. Cards are unique, so there are no ties.
- Five tricks use exactly the five c
- reasoning_over_luck: pass. Chance is the 5-card deal and the 5-card widow. The decisive choices are inference and planning.

- The Lone fits trump, leader and bid to its hand, so a weak hand can still make 0 or 1. This converts deal luck into a bidding problem.
- The Pair infer the Lone's suit from talk to ban it. They read t

## Complexity

- steps_per_round: designed 18, built 15, limit 20
- choice_steps_per_round: designed 3, built 6, limit 4
- attributes: designed 19, built 48, limit 20 (built: 80)
- hidden_elements: designed 2, built 8, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 36, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Game starts with all scores 0 and a 20-card deck
- pass: Deal gives 5 cards to each seat and 5 to the widow (random cards, only counts asserted)
- pass: Leftover hand and widow cards return to the deck before the deal
- pass: Deal 4 makes seat 1 the Lone
- pass: Deal 5 makes seat 2 the Lone
- pass: Deal 3 makes seat 3 the Lone
- pass: Talk step changes no scores
- pass: Only the Pair seats ban a colour
- pass: Matching bans leave 3 colours unbanned
- pass: Different bans leave 2 colours unbanned
- pass: Lone sets trump, leader and bid; a banned trump is not offered
- pass: Named leader leads the first trick; the winner leads the next
- pass: All three seats play once to a trick led by seat 3
- pass: Must follow the led colour if able; a void seat may play anything
- pass: A played card leaves the hand and is shown face up
- pass: A low trump beats a higher card of the led colour
- pass: A Pair member who wins a trick scores 1
- pass: A trick won by the Lone raises lone_tricks
- pass: Exact bid: the Lone gains 6 plus the trick point
- pass: Off by one: the Lone gains 2 and each Pair member gains 1
- pass: Off by two or more: each Pair member gains 3
- pass: Game ends after deal 6 and seats level at the top share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [3], results {'seat 1': 8, 'seat 3': 3, 'seat 2': 7, 'seats 1 and 3': 1, 'seats 2 and 3': 1}, 82-93 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 126.0 decisions, prompts of 169 characters on average (longest 229)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 1': 23, 'seat 3': 12, 'seat 2': 22, 'seats 1 and 3': 2, 'seats 2 and 3': 1}
- always `first@seat1`: won 18, lost 39, drew 3
- always `first@seat2`: won 16, lost 40, drew 4
- always `last@seat1`: won 11, lost 49, drew 0
- always `last@seat2`: won 5, lost 53, drew 2

## Triage (whose problem each failure was)

- round 1: fix_game: The rules are sound and the platform can express them. Every failure is a file mistake: calc expressions where `players` resolves to the engine's player list instead of the numeric parameter, and internal or not-yet-set text fields shown blank in announcements.
- round 1: revise_rules: The game was built faithfully, but the design needs 7 choice steps per round against a limit of 4. Because the step list is flat, the veto round (one talk poll plus three sequential token placements) and the trick round (three sequential card plays) all count toward the same per-round total, so the coder cannot fix this; the rules must change.
- round 2: revise_rules: The game was built and behaves as specified, but the design breaks the platform's per-round choice limit. A round holds 6 choice steps against a limit of 4: talk, veto and contract plus three card plays all sit in the same flat step list. Results against random seats are also lopsided (seat 3 wins 12 against 22–23 for seats 1 and 2), so the rules themselves need changing.

## Choices the rules did not make

- Exactly 3 players (min 3, max 3, suggested 3): The designer fixed 3. The rules depend on 3 seats: a 1-versus-2 Lone/Pair split, 5 cards each plus a 5-card widow from 20 cards, and a fixed clockwise order. Any other count breaks the deal and the rotation. Strategy: the Lone bids a count they can hit exactly, using trump and the first leader to steer. The Pair try to push the Lone 2 or more tricks off the bid, either by taking tricks or by feeding the Lone extra ones, while still collecting 1 point per trick.
- Talk kept as one simultaneous poll broadcast to all: The source requires it. It earns its place because the Pair benefit from coordinating vetoes (matching bans leave 3 colours, different bans leave 2), while the Lone can mislead and each Pair member is also a rival for the overall win.
- The contract is offered as one combined choice list: The rules call it one decision of three parts. Listing every valid trump, leader and bid combination keeps it to one choice and enforces that trump is unbanned.
- Cards are written as colour letter plus number (R1..Y5), and trick strength is computed as 10 plus number for trump, number for the led colour, 0 otherwise: This lets the trick winner be found by arithmetic. Every card is distinct, so no ties are possible, matching the rules.
- Each widow is never revealed, not even at the end: The widow is redealt every deal and plays no role in scoring. The rules only say it is unseen during play, so it stays hidden.

## Simplifications

- A tie for the highest total is shared as a win rather than declared a draw: The engine ranks by one expression and players level at the top share the win. This is the engine's form of the source's draw.
- Setup-round and trick-round steps live in one flat round, each gated by a when-condition on round_in_deal: The engine repeats one step list. Per-step arithmetic conditions select the setup or trick steps without choosing whole blocks.

## Encoding attempts

- 1: playing it with random seats failed: seed 1, 3 players: the match crashed: CalcError: 'deck[int(uniform(0, len(deck)))]': list index out of range
- 2: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (ban, played_card, veto_answer, ban) in `your_hand`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 3: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (led_colour, trump) in `your_hand`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 4: it plays, but part of it does nothing: game attribute `all_cards` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `colour_names` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `seat_labels` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `bid_labels` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 5: passed
