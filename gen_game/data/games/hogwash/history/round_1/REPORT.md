# hogwash: needs review

Built from the variation **Hogwash: Even Rounds** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- When any player empties their hand, the current cycle of seats is finished, so every seat has had exactly the same number of turns before the game ends. Every player then at zero cards is a finisher. Ties among finishers are broken by fewest total cards taken from the pile over the game, otherwise a draw. (fixes: P1): Equal turns remove the tempo edge. The uncontested race now ends with all seats out together, a draw, so seat order alone wins nothing. The tiebreak rewards accurate challenging and well-judged bluffing over the whole game.
- Use a 25-card deck: ranks 1 to 5, five copies of each. Deal 8 each with 3 players or 6 each with 4. The one leftover card goes face down as the first pile card, seen by nobody. There is no player-placed starter card. (fixes: P2): The shuffle and deal is the only random event, everyone is dealt the same hand size, and nobody has special knowledge of the starter card.
- Use 5 ranks instead of 6. (fixes: P3): 5 shares no factor with 3 or 4, so over five cycles every seat must claim every rank. A hand rich in one rank helps every seat equally often, and no seat is locked to fixed ranks.
- Because the game no longer ends on the spot, a challenger who calls a true final play takes the whole pile. (fixes: P4): Calling a last play now has a real cost, so it becomes a judgement rather than an automatic call.
- Add a simultaneous talk step after the claim and before the challenge poll. Every player still holding cards, including the active player, writes one short message. All messages are shown, then the poll happens. (fixes: P5): The first challenger clockwise carries all the risk and later challengers carry none, so non-active players disagree about who should call. The active player can bluster or bait. Talk gives players promises to test and bluffs to read.
- State the zero-card rules explicitly. A player with zero cards is finished. They take no further turns (their turn slot passes with no play), do not talk, are always counted as PASS in polls, and can never receive the pile. (fixes: P6): Removes ambiguity so the engine can build the game correctly.

Objective: When the game ends, every seat has had the same number of turns. Find the smallest hand size held by any player; this is 0 if anyone is finished. Among the players holding that many cards, the one with the lowest taken counter wins. If two or more of them tie on the lowest taken counter, the game is a draw.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. SETUP ARITHMETIC: 3 players: 3x8 = 24 dealt plus 1 pile card = 25. 4 players: 4x6 = 24 plus 1 = 25. Turn 36 is 12 cycles with 3 players and 9 cycles with 4. Ranks cycle through all seats because gcd(5,3) = gcd(5,4) = 1. Check for 3 players: Player 1 plays turns 1, 4, 7, 10, 13, which require ranks 1
- playable: pass. COMPLETENESS: Every situation is covered.
- Deal sizes for 3 and 4 players.
- The leftover card goes face down on the pile.
- Rank advance wraps 5 to 1.
- Claim size is 1-3, never more than held.
- The resolving challenger is the first challenger clockwise after the active player.
- Only the just-pl
- reasoning_over_luck: pass. The deal is the only randomness. It sets how many truthful plays a hand allows across its required ranks, which is a moderate effect. Rough estimate: chance accounts for about 25-35% of outcomes. The rest comes from three things:
- Bluff sizing: 1-card bluffs are believable at about 86% base rate; 3

## Complexity

- steps_per_round: designed 16, built 15, limit 20
- choice_steps_per_round: designed 3, built 6, limit 4
- attributes: designed 18, built 33, limit 20 (built: 80)
- hidden_elements: designed 2, built 6, limit 3
- random_draws_per_round: designed 0, built -, limit 1
- rounds: designed 36, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: 3 hands of 8 plus 1 pile card make up the 25-card deck
- pass: Setup with 4 players deals 6 cards each
- pass: Setup with 3 players deals 8 cards each
- pass: Leftover card goes to the pile and the deck is empty (4 players)
- pass: Initial taken, turn, rank and active seat
- pass: With 2 cards in hand the active player may play 1 or 2 but not 3
- pass: With 5 cards in hand at most 3 may be played
- pass: The claim is of the required rank 3: two real 3s beat a challenge
- pass: Playing 3 cards lowers hand_count by 3 and raises pile_count by 3
- pass: Talk changes no state; a finished seat is left out
- pass: Only non-active unfinished seats are polled for a challenge
- pass: An unchallenged bluff stays in the pile
- pass: 4 players, active seat 3, challengers 1 and 2: seat 1 resolves and takes the pile on a true claim
- pass: True claim challenged: the challenger takes the whole pile
- pass: Bluff challenged: the active player takes the whole pile
- pass: Two challengers on a true claim: seat 2 resolves, seat 3 loses nothing, pile empties
- pass: Only the cards just played decide the challenge: older off-rank pile cards do not make it a bluff
- pass: A caught bluffer playing their last card is not finished
- pass: Playing the last card unchallenged makes the player finished
- pass: A finished seat's turn plays nothing and rank and seat advance; next seat then plays
- pass: The first finished player sets end_marked; the game continues until the last seat
- pass: Last seat finishes on its turn: the game ends and that seat wins
- pass: Turn 36 on the last seat ends the game; fewest cards wins
- pass: After the last seat's turn the rank wraps 5 to 1, the seat wraps to 1 and turn increases
- pass: Level on fewest cards, the lower taken wins
- pass: Level on cards and taken: the win is shared
- pass: A finished seat never receives the pile when a challenge resolves

## Does the file follow the spec's shape? (flags for a person)

- the spec declares player attribute `seat` but the game file does not: a piece of state the rules need is missing

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 4], results {'seat 1': 10, 'seat 3': 11, 'seat 2': 13, 'seat 4': 6}, 113-366 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 285.7 decisions, prompts of 142 characters on average (longest 198)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 1': 20, 'seat 3': 17, 'seat 2': 23}
- always `first@seat1`: won 46, lost 14, drew 0
- always `first@seat2`: won 48, lost 12, drew 0
- always `last@seat1`: won 14, lost 45, drew 1
- always `last@seat2`: won 12, lost 48, drew 0

## Triage (whose problem each failure was)

- round 1: revise_rules: The game was built correctly, but the design fails evaluation on two counts. A round has 6 choice steps against a limit of 4, and a thoughtless 'always take the first option' policy wins about 77–80% of its games from either seat while 'always take the last option' loses about 75–80%, so a trivial strategy dominates.

## Choices the rules did not make

- 3 to 4 players, suggested 3: The designer suggested 3. Bluff-calling needs at least two potential challengers, so at least 3 seats are needed for the clockwise resolver rule to matter. The deal (8 or 6 cards each from 25) only supports 3 or 4 seats.
- Keep the simultaneous talk poll before the challenge poll: The source requires it. It earns its place because players disagree: each wants someone else to be the one to challenge and risk the pile. Threats and bluffs about challenging give something to reason about.
- One engine round equals one turn: This makes the end check after the last seat's turn and the rank/seat advance straightforward arithmetic.
- Ranking expression -(hand_count*1000 + taken): This puts hand size first and taken second in one arithmetic value. taken cannot exceed about 109 (at most 108 cards played in 36 turns plus the first pile card), so the 1000 weight keeps the two levels separate.

## Simplifications

- Choosing 1-3 cards is asked as a count followed by up to three single-card picks gated by when-conditions: An engine answer is a single choice, number or text, not a multi-select.
- A tie on fewest cards and lowest taken is a shared win rather than a declared draw: The engine has no separate draw: players level at the top share the win, which is equivalent.

## Encoding attempts

- 1: players are sent text with a `{name}` that was never filled in: placeholder: players are shown the literal {hand} (in `prompt`: 'Turn 1: you must claim rank 1. How many cards will you play face down (from 1 to 3, never '); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {hand} (in `prompt`: 'Choose the first card to put face down. Any rank is allowed; a card that is not rank 1 is '); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {hand} (in `prompt`: 'Choose the second card to put face down. Your remaining hand: {hand}.'); use only names the step can fill in (see the broadcast rule: {value} and {seat})
- 2: passed
