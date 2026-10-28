# greek_hold_em: needs review

Built from the variation **Greek Hold 'em Lite** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Two betting stages per hand instead of four: one after the 3-card flop and one after the last 2 board cards. Each stage is a simultaneous sealed bet of 0–4 chips, followed by a simultaneous call-or-fold for everyone who bet less than the highest bet. (fixes: P1: Open-ended sequential raise/re-raise loops cannot be built in a flat step list, and four betting streets exceed the 4-choice-step limit.): This gives a fixed 4 choice steps per hand while keeping betting, raising (bidding high), calling and folding.
- The 52-card deck is replaced by 32 numbered cards (values 1–8, four copies each). Hand strength becomes a single formula: Strength = 20 × min(matches, 3) + 30 × (hole pair ? 1 : 0) + hole1 + hole2, where 'matches' counts board cards equal in value to either hole card. (fixes: P2: Standard poker hand ranking (suits, straights, flushes, kickers, best 5 of 7 with the Greek constraint) is far too long a rule chain to compute arithmetically. It would need a referee to decide the winner.): This keeps the Greek rule that both hole cards always play and at most three board cards count. Pairing the board with your hole cards is what makes a hand strong. It is computable in one calculation.
- Bets are capped at 4 chips per stage and the ante is 1. Stacks start at 40. The session is 15 hands, and the winner is the highest stack. (fixes: P3: Unlimited bet sizes let one all-in pot decide a short session, so luck swamps skill in the number of hands the platform can play.): Each hand can move at most 9 chips per player. Many hands decide the game, so consistent reading and betting beats one lucky deal.
- All betting decisions are simultaneous polls, so there is no button or acting order. (fixes: P4: Acting position within a betting round gives a seat-based edge in any single hand.): No seat ever acts with more information than another.
- There are no side pots. A player who cannot cover a call puts in their whole stack and stays in for the whole pot. A player with 0 chips is eliminated. (fixes: P5: Side pots and all-in handling add state and steps without adding much reasoning.): This removes side-pot bookkeeping. With a 4-chip cap and 40-chip stacks the case is rare and late.

Objective: When the game ends, the player with the most chips wins. If two or more players tie for the most chips, those players draw. If only one player has chips left before hand 15, that player wins.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. Hand values. A pair in the hole has probability 3/31 ≈ 9.7%. For a non-pair hand, 6 copies of its two values remain among 30 unseen cards. The expected number of matches on a 5-card board is 5×6/30 = 1. Strength is about 20×matches + sum, ranging from 3 (1+2 with no matches) up to 75 (8+7 with 3 mat
- playable: pass. Edge cases resolve from the text:
- If H = 0, nobody is below H and nobody acts.
- A player who bet H always remains, so a hand can never end with everyone folded.
- A player who went all-in on the ante (stack 0) bets 0. If they face H > 0, they 'call' by paying their whole stack of 0 and stay in.
-
- reasoning_over_luck: pass. Inference and its use:
- A player infers opponents' hole values from the flop, from the 3 board values already seen, and from opponents' simultaneous bet sizes.
- They act on it through bet sizing and the call/fold decision at stated pot odds (about 33% equity needed to call a 4-bet into a pot of 4)

## Complexity

- steps_per_round: designed 16, built 15, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 16, built 37, limit 20 (built: 80)
- hidden_elements: designed 2, built 7, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 15, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Start: everyone has 40 chips and the pot is 0 (seen through hand 1: antes to 39, seat 1 wins pot of 4)
- pass: Ante: seat with 5 goes to 4; others fold to seat 2's bet
- pass: Player with 1 chip antes to 0 and stays in to showdown (pot 4 splits evenly, chance-independent)
- pass: Deal: 2 hole cards each, 5 board, deck left with 21 (chance-independent counts)
- pass: Flop reveals exactly 3 board cards (hand ends at flop)
- pass: Bet capped by chips and moves from chips to pot
- pass: Only players below H are asked to call or fold
- pass: Bet 1 against H=4: call pays 3 more
- pass: Short call pays all chips and stays in to showdown (chance-independent)
- pass: Fold leaves the hand, bet chips are lost
- pass: Last player after flop takes the pot; no turn or river
- pass: Two remain after flop: all 5 board cards shown
- pass: River betting: fresh bets, chips to pot, fold loses river bet
- pass: Last player after river takes the pot without showdown
- pass: Showdown reveals every remaining hole (chance-independent counts)
- pass: Two-way showdown with even pot 8 empties the pot (chance-independent)
- pass: Three-way showdown with pot 12 empties the pot (chance-independent)
- pass: Showdown pays out the pot; folded seat unchanged (chance-independent)
- pass: Pot of 6 split among any number of 1-3 tied winners leaves 0 (chance-independent)
- pass: Player at 0 chips after the hand is eliminated
- pass: Game ends after hand 15
- pass: Game ends at once when only one player is left
- pass: Tied for most chips at the end share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 5], results {'seat 1': 17, 'seat 3': 8, 'seat 2': 2, 'seats 1 and 2': 1, 'seat 4': 7, 'seat 5': 5}, 91-206 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 148.2 decisions, prompts of 258 characters on average (longest 286)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- always taking the last option as seat 1 wins 95% of decided matches against random seats
- random seats: {'seat 1': 23, 'seat 3': 20, 'seat 2': 15, 'seats 1 and 2': 1, 'seats 1 and 3': 1}
- always `first@seat1`: won 32, lost 27, drew 1
- always `first@seat2`: won 39, lost 20, drew 1
- always `last@seat1`: won 56, lost 3, drew 1
- always `last@seat2`: won 50, lost 9, drew 1

## Triage (whose problem each failure was)

- round 1: revise_rules: The file works as specified, but the betting structure lets a mindless policy dominate: always taking the last option (bet the maximum 4, never back down) wins 56 of 60 games from seat 1. Opponents who are uncertain fold often and hand over the pot, so raw aggression beats any judgment of card strength.

## Choices the rules did not make

- 3 to 5 players, suggested 4: The designer suggests 4, so it is kept. The minimum is 3 because with 2 players simultaneous betting is a pure guess against one rival, and 3 or more make folding and calling a reading of several opponents. The maximum is 5 because 10 hole cards and 5 board cards already use half the 32-card deck, and more seats dilute each bet's effect on the pot.
- No pre-bet talk step: The rules contain no table talk. Adding it would add a mechanic, and the bluffing already lives in the simultaneous bet sizes.
- Strategy at the table: A thoughtful player bets according to their likely matches against the 3 shown board cards and pair potential. They read big bets as strength, fold weak hands when H is high, and use the carried-over pot and opponents' short stacks (who are forced all-in) to decide when calling is worth it.
- The call cost is computed against the player's current-round bet: The rules say a caller pays 'the difference so their bet equals H'. Bets reset between the flop and river rounds, since each is a separate betting round.
- A player at 0 chips bets 0 and calls for 0: The rules cap bets at the stack and let an all-in caller stay in, so a 0-chip player stays in at no cost.
- No side pots: The rules give the whole pot to the highest strength, including an all-in player, so no side pots are created.

## Simplifications

- 'Skip to step 10' is done with a 'when in_hand_count >= 2' condition on each turn, river and showdown step instead of a jump: The step list is flat. Per-step arithmetic conditions give the same result.
- Revealing hole cards at showdown is done by copying hole into a public shown_hole list: Hole cards are owner-only, so a public copy is how the engine reveals them to everyone.

## Encoding attempts

- 1: playing it with random seats failed: seed 1, 3 players: the match crashed: KeyError: 0
- 2: players are sent text with a `{name}` that was never filled in: placeholder: players are shown the literal {chips} (in `prompt`: 'Flop bet. Board so far: [2, 6, 1]. Pot: 3. You have {chips} chips. Secretly bet a whole nu'); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {chips} (in `prompt`: 'Flop bet. Board so far: [2, 6, 1]. Pot: 3. You have {chips} chips. Secretly bet a whole nu'); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {chips} (in `prompt`: 'Flop bet. Board so far: [2, 6, 1]. Pot: 3. You have {chips} chips. Secretly bet a whole nu'); use only names the step can fill in (see the broadcast rule: {value} and {seat})
- 3: passed
