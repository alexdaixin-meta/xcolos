# g_11_nimmt: needs review

Built from the variation **Eleven Takes: Three Piles** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Use exactly 3 piles throughout. A taken pile is immediately restarted, so there are always 3. (fixes: The number of piles grows each time one is taken, giving unbounded state that the engine cannot track within 20 attributes.): This bounds the state to 3 pile lists and keeps the take-or-play pile choice.
- When a player takes a pile, they restart it with a card of their own choosing from their hand (which now includes the taken cards). Nothing is drawn from a deck during play. (fixes: Each pile take draws two random cards from the deck, which breaks the limit of one random draw per round and adds luck to every take.): This removes all in-play randomness and turns the restart into a strategic choice: block opponents or set up your own run.
- Bulls are capped. Each bull held lets a player add one extra card to the same pile in the same turn, with a maximum of 2 extra cards. (fixes: Bull runs allow an unbounded number of cards in one turn, which exceeds the choice-step limit.): This keeps the bull-run idea while fitting within 4 choice steps.
- Use a deck of 1 to 40, circular distance at most 6, 6-card hands, 3 or 4 players, and a single deal of at most 36 or 40 turns. Each engine round is one player's turn. (fixes: The 104-card deck, 10-card hands and multi-round match (as many rounds as players) are too long and too large to build and play inside 40 rounds.): This scales the game to the round and attribute limits while keeping the density of legal plays similar to the original.
- Use 3 or 4 players only. When someone empties their hand, the current cycle is completed so that every player has had the same number of turns. The lowest penalty wins. (fixes: The two-player game is a pure difference game, and seat order gives the first player a tempo edge (they may empty their hand before others have had as many turns).): With 3 or more players the game is not a difference game. Finishing the cycle removes the first seat's tempo edge.
- Make the full contents of every pile public, so that every taken card is known to everyone. The initial deal is the only random event. (fixes: Random pile seeding and a large random deal let luck swamp skill in a single deal.): Hidden information shrinks to the original deal plus the undealt cards. A careful tracker can deduce more and more about opponents' hands, so skill beats luck over a game.

Objective: The player with the lowest penalty wins. If two or more players tie for lowest, the game is a draw among them (an engine draw).

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. Arithmetic checks. Ox-heads: 10/20/30/40 give 4x3=12; 5/15/25/35 give 4x2=8; the other 32 cards give 32. Total 52, as stated. Cards: 4 players use 24+3=27 and set aside 13; 3 players use 18+3=21 and set aside 19. Both correct. Turn caps are 40 (4p) and 36 (3p).

What each action does to hand size:
|
- playable: pass. Rules are complete for every situation:
- Legality: (c-t) mod 40 in 1..6, with worked examples.
- Illegal or impossible PLAY: falls back to taking the smallest pile, with ties A<B<C.
- Illegal extra card: ignored and ends the run.
- Bull supply empty: steal from the opponent with the most bulls; tie
- reasoning_over_luck: pass. The single shuffle decides each hand of 6, the 3 starting tops, and which 13-19 cards are missing. A clustered hand (several cards within 6 of each other) is a real advantage, and a missing link card can break a chain. I estimate chance decides roughly 30-40% of outcomes.

Good play can overcome a w

## Complexity

- steps_per_round: designed 15, built 17, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 16, built 53, limit 20 (built: 80)
- hidden_elements: designed 1, built 17, limit 3
- random_draws_per_round: designed 0, built -, limit 1
- rounds: designed 40, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup with 4 players: 6 cards per hand, 1 card per pile, 13 set aside (checked after seat 1 takes a 1-card pile and restarts it)
- pass: Setup with 3 players: 6 cards per hand, 1 card per pile, 19 set aside (checked after seat 1 takes a 1-card pile and restarts it)
- pass: Bull supply starts at 3 with 4 players, nobody holds bulls (a 1-card take moves no bull)
- pass: Bull supply starts at 2 with 3 players (a 1-card take moves no bull)
- pass: Ox-heads at the end: multiples of 10 count 3, other multiples of 5 count 2, the rest 1
- pass: Legal plays on 37 wrap around: 38, 40 and 3 offered, 36, 4 and 10 not
- pass: Legal plays on 12 are 13 to 18: 18 offered, 19 and 11 not
- pass: Playing a card moves it to the top of the pile and hand_size drops by 1
- pass: With 1 bull a player may add one extra legal card on the same pile
- pass: With 2 bulls a player may add two extra legal cards on the same pile
- pass: Using bulls for extra cards does not spend them or return them to the supply
- pass: Taking a 2-card pile adds both cards to the hand
- pass: After a take the player restarts the pile with one card from hand
- pass: Taking a 3-card pile gives the taker a bull from the supply
- pass: Empty supply: the taker steals from the tied opponent first after it in seat order
- pass: Empty supply: the taker steals from the opponent holding the most bulls
- pass: Empty supply and no opponent holds a bull: nothing changes
- pass: Taking a 2-card pile moves no bull
- pass: A player with a legal play may still take a pile
- pass: Seat 1 empties its hand; seats 2 and 3 still play before the game ends
- pass: With 3 players the game ends after 12 full cycles
- pass: A player who empties its hand on the last turn has penalty 0 and wins
- pass: Players tied for the lowest penalty share the win
- pass: After a take, the public piles, hand_size and bulls show the result

## Does the file follow the spec's shape? (flags for a person)

- rule R14 has no scenario: nothing checks it

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 4], results {'seat 1': 12, 'seat 2': 12, 'seat 3': 7, 'seats 1, 2 and 3': 1, 'seats 1 and 3': 2, 'seats 1 and 2': 1, 'seats 1 and 4': 1, 'seat 4': 4}, 55-70 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 64.3 decisions, prompts of 121 characters on average (longest 164)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- always taking the first option as seat 1 wins 93% of decided matches against random seats
- always taking the first option as seat 2 wins 89% of decided matches against random seats
- random seats: {'seat 1': 15, 'seat 2': 22, 'seat 3': 17, 'seats 1, 2 and 3': 1, 'seats 1 and 3': 3, 'seats 1 and 2': 1, 'seats 2 and 3': 1}
- always `first@seat1`: won 53, lost 4, drew 3
- always `first@seat2`: won 50, lost 6, drew 4
- always `last@seat1`: won 0, lost 60, drew 0
- always `last@seat2`: won 0, lost 59, drew 1

## Triage (whose problem each failure was)

- round 1: fix_game: The interface defines `ending_triggered` as true only once some player has emptied their hand. In the 3-player cycle-limit scenario no hand was empty (sizes 3, 2, 2), yet the game set it to True when `cycle` reached `max_cycles` = 12. The game is reusing that flag for the cycle-limit ending, so the test's expectation of False is correct.
- round 1: revise_rules: The game is built and behaves as specified, yet one fixed, thoughtless policy wins about 90% of decided matches and the opposite fixed policy loses nearly every game. The real decisions are degenerate: playing a card off your hand is almost always right, and taking a pile is almost always wrong, so little strategy remains.

## Choices the rules did not make

- 3 to 4 players, suggested 4: The designer gives 3-4 and suggests 4. With fewer than 3 there are too few rivals to steal bulls from or to dump piles on. With more than 4 the 40-card deck cannot deal 6 cards each plus 3 piles with cards left to set aside as the rules intend, and the bull supply and cycle limits are defined only for 3 and 4.
- One engine round is one player's turn, with active_seat cycling 1..N: The rules say a turn is one engine round. The end check runs only after seat N's turn, so every player gets the same number of turns.
- max_cycles = 18 - 2*N and bull_supply = N - 1: These write the source's per-count numbers (10 cycles with 4 and 12 with 3; supply 3 with 4 and 2 with 3) as rules over the count.
- Penalty is computed only at the end of the game: A running public penalty would leak hidden hand contents. The rules make only hand size and bulls public.
- No pre-move talk step: The source has no talk, and adding it would add a mechanic. Play is purely sequential and every action is public.
- Ranking is 0 - penalty: Lowest penalty wins. Negating it lets the highest rank_by win, and ties at the top share the win, which matches the source's draw.
- The steal tie-break uses the smallest (seat - active_seat) mod N: This is 'the first such player in seat order after the taker' written as arithmetic.

## Simplifications

- Only legal plays are offered, so an illegal PLAY choice cannot be made. The fallback 'take the smallest pile' applies when a seat gives no valid answer.: The engine never offers a seat an action it may not take. The fallback still covers the same failure case.
- Only legal extra cards are offered, plus 'stop': This has the same effect as the rule that an illegal extra card is ignored and ends the run.
- The branches after the main action (extra cards for a play, restart card and bulls for a take) are separate steps, each with its own arithmetic 'when' condition: The step list is flat. A per-step condition on action_kind reproduces both branches without choosing between blocks of steps.

## Encoding attempts

- 1: players are sent text with a `{name}` that was never filled in: placeholder: players are shown the literal {hand} (in `prompt`: 'Your turn. Piles: A [20], B [16], C [27] (last card is the top). Your hand: {hand}. Play a'); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {hand} (in `prompt`: 'Your turn. Piles: A [20], B [16], C [27, 33] (last card is the top). Your hand: {hand}. Pl'); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {hand} (in `prompt`: 'You took pile B. Your hand: {hand}. Choose one card from your hand to place face up as the'); use only names the step can fill in (see the broadcast rule: {value} and {seat})
- 2: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (action_kind, chosen_pile, last_action) in `the_state`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 3: it plays, but part of it does nothing: game attribute `cards` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `card_labels` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `bull_from` is never changed in 3 random matches, so nothing updates it. Steps that name it: build the action offer, the bull. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 4: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (action_kind, chosen_pile, last_action) in `the_state`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 5: passed
