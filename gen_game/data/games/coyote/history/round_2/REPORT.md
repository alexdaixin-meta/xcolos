# coyote: needs review

Built from the variation **Coyote: Around the Fire** (design round 2); see VARIATION.md.

## What was changed from the original, and why

- Remove the hand turn cap. A hand passes around the table lap after lap, one lap per engine round, until someone calls Coyote. A new hand can begin only at the start of a round, and once Coyote is called the remaining turns of that round are skipped. (fixes: P3): This restores real Coyote. Nobody is forced to end the hand by seat. The loss lands on whoever misjudges the total, or is caught when the declaration reaches it. It also keeps choice steps at no more than 4 per round and one deal per round.
- Abolish the R9 showdown. Every hand ends with a Coyote call: the declarer loses if the true total is below the declaration, otherwise the caller loses. (fixes: P3): A true claim is never punished, so the only ways to lose are overclaiming or calling a true claim.
- The opener may declare any whole number from −3 to 20. (fixes: P1): The floor of −3 is below almost every possible total, so the opener is no longer forced into a false claim. The opener chooses how aggressive to be.
- The opener rotates one surviving seat clockwise every hand, whoever lost. (fixes: P2): Every player opens equally often and there is no snowball.
- The minimum raise is +1. (fixes: P4): The 'stuck' situation shrinks to the single case where the declaration equals the true total exactly. Aiming at that exact value, and avoiding it, becomes the skill.
- Use a new 20-card deck: values −2 to 5 plus one Max→0. The card SD is about 2.0 and the 4-player total has mean ≈ 5.7. (fixes: P5): Your own-card uncertainty (about ±4) becomes comparable to what others' declarations reveal. Inference can narrow it, and totals are small, so hands last 1–3 laps.
- Each hand has many +1-sized decisions near the true total, made over several laps, with the full declaration history visible. (fixes: P6): Players can read jumps and hesitations, which carry information about their own card. They can jump to pin the next player or creep safely. This gives many reasoned decisions per hand.

Objective: Be the last player not eliminated (3 tokens eliminate). If 40 rounds pass with more than one player alive, the alive player with the fewest tokens wins, and a tie for fewest is a draw.

## The critic (3 review(s) before the rules went to a coder)

- balanced: pass. Deck check: the numbered cards sum to -2-1-1+0+3+6+9+8+10 = 32 over 19 cards, a mean of about 1.68 and an SD of about 1.8. Max->0 cancels the highest positive card. Extremes: the 3-player minimum total is -2-1-1 = -4. The 4-player maximum is 5+5+4+4 = 18, so a declaration of 20 is never true. Each p
- playable: pass. The rules cover: setup; the deck; the deal; private views; legal declarations (opening -3 to 20, a raise of at least 1, a forced call at 20); the true total, including Max->0 ties and non-positive cases; resolution; elimination; opener rotation, including an eliminated opener; hands that span rounds
- reasoning_over_luck: pass. There is something to infer: your own card, from others' declarations. Worked example (3 players, cards A=1, B=3, C=5, true total 9). A sees 8 and expects about 9.7. B sees 6 and expects about 7.7. C sees 4 and expects about 5.7. A opens 8, which is safe unless A holds a negative card or a cancellin

## Complexity

- steps_per_round: designed 14, built 15, limit 20
- choice_steps_per_round: designed 4, built 2, limit 4
- attributes: designed 13, built 45, limit 20 (built: 80)
- hidden_elements: designed 1, built 9, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 40, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Start: every player has 0 tokens and is alive, opener 1, round 1
- pass: New hand resets deck to 20 cards before dealing 4 (16 left)
- pass: Only alive players are dealt a card: 3 alive of 4 leaves 17 in deck
- pass: Deal gives one card per player (visibility itself is not observable)
- pass: New hand clears old declarations: opener may declare -3 again
- FAIL: Hand in progress: no new deal and the declaration carries on | rule R6 is broken: When a round starts with hand_active true, then no cards are dealt and the hand continues with the same cards and declarations.; seat 1 was never offered 5, but should have been; Ada: the rule for 5 was never matched (the game never put that option to this seat); Blaise: the rule for 6 was never matched (the game never put that option to this seat); Cleo: the rule for 7 was never matched (the game never put that option to this seat)
- pass: Turns start at opener 3 and skip eliminated seat 2
- FAIL: Coyote by the first player skips the rest of the round | rule R8 is broken: When Coyote is called, then the remaining turns of that round are skipped.; seat 3 tokens: expected 1, got 0; game opener_seat: expected 2, got 1; Ada: the rule for 'coyote' was never matched (the game never put that option to this seat)
- pass: First declaration: -3 to 20 offered, Coyote not offered
- FAIL: With declaration 7: Coyote or 8..20 offered, not 7 | rule R10 is broken: When a declaration exists, then the player to act may declare a whole number from current_declaration+1 to 20 or call Coyote.; seat 1 was never offered 'coyote', but should have been; seat 1 was never offered 8, but should have been; seat 1 was never offered 20, but should have been; Ada: the rule for 8 was never matched (the game never put that option to this seat); Blaise: the rule for 9 was never matched (the game never put that option to this seat); Cleo: the rule for 10 was never matched (the game never put that option to this seat)
- FAIL: Declaration 20 forces Coyote (cards 1,2,3 total 6 < 20, declarer loses) | rule R11 is broken: When current_declaration is 20, then the player to act must call Coyote.; seat 3 tokens: expected 1, got 0; seat 1 was never offered 'coyote', but should have been; Ada: the rule for 'coyote' was never matched (the game never put that option to this seat)
- FAIL: A declaration of 6 becomes the bar: next seat offered 7, not 6 | rule R12 is broken: When a player declares a number, then current_declaration becomes that number, current_declarer becomes that seat, and the pair is appended to declarations.; seat 3 was offered 8, but must not be
- FAIL: Cards 3,5,-1 total 7; declaration 7 holds so the caller loses | rule R13 is broken: When Coyote is called and Max→0 is not dealt, then true_total is the sum of the dealt cards (for example 3, 5 and -1 give 7).; seat 1 tokens: expected 1, got 0; Ada: the rule for 'coyote' was never matched (the game never put that option to this seat)
- FAIL: Cards 3,5,-1 total 7; declaration 8 is too high so the declarer loses | rule R13 is broken: When Coyote is called and Max→0 is not dealt, then true_total is the sum of the dealt cards (for example 3, 5 and -1 give 7).; seat 3 tokens: expected 1, got 0; Ada: the rule for 'coyote' was never matched (the game never put that option to this seat)
- FAIL: Max->0, 5, 2 total 2; declaration 3 loses | rule R14 is broken: When Coyote is called and Max→0 is dealt with highest other card 5, then that 5 counts as 0 (for example Max→0, 5 and 2 give 2).; seat 3 tokens: expected 1, got 0; Ada: the rule for 'coyote' was never matched (the game never put that option to this seat)
- FAIL: Max->0, 3, 3, 1 total 4; declaration 4 holds, caller loses | rule R15 is broken: When Max→0 is dealt with two 3s as the highest other cards, then only one 3 is cancelled (for example Max→0, 3, 3 and 1 give 4).; seat 1 tokens: expected 1, got 0; Ada: the rule for 'coyote' was never matched (the game never put that option to this seat)
- FAIL: Max->0, 3, 3, 1 total 4; declaration 5 loses | rule R15 is broken: When Max→0 is dealt with two 3s as the highest other cards, then only one 3 is cancelled (for example Max→0, 3, 3 and 1 give 4).; seat 4 tokens: expected 1, got 0; Ada: the rule for 'coyote' was never matched (the game never put that option to this seat)
- FAIL: Max->0, -1, -2: nothing cancelled, total -3 < declaration -2, declarer loses | rule R16 is broken: When Max→0 is dealt and the highest other card is 0 or less, then nothing is cancelled (for example Max→0, -1 and 0 give -1).; seat 3 tokens: expected 1, got 0; Ada: the rule for 'coyote' was never matched (the game never put that option to this seat)
- FAIL: Max->0, -1, 0 total -1; declaration -1 holds, caller loses | rule R16 is broken: When Max→0 is dealt and the highest other card is 0 or less, then nothing is cancelled (for example Max→0, -1 and 0 give -1).; seat 1 tokens: expected 1, got 0; Ada: the rule for 'coyote' was never matched (the game never put that option to this seat)
- FAIL: Total 3 < declaration 4: declarer seat 2 gains a token | rule R17 is broken: When Coyote is called and true_total < current_declaration, then the current declarer gains 1 token.; seat 2 tokens: expected 1, got 0; Ada: the rule for 'coyote' was never matched (the game never put that option to this seat)
- FAIL: Total 3 >= declaration 2: caller seat 1 gains a token | rule R18 is broken: When Coyote is called and true_total >= current_declaration, then the caller gains 1 token.; seat 1 tokens: expected 1, got 0; Ada: the rule for 'coyote' was never matched (the game never put that option to this seat)
- FAIL: Resolved hand ends: next round deals a fresh hand from a full deck | rule R19 is broken: When a hand is resolved, then all cards, true_total and the loser are announced to everyone, and hand_active becomes false.; seat 3 tokens: expected 1, got 0; game opener_seat: expected 2, got 1; game deck: expected 17 items, got 5; seat 2 was never offered -3, but should have been; Ada: the rule for 'coyote' was never matched (the game never put that option to this seat); Ada: the rule for 2 was never matched (the game never put that option to this seat); Blaise: the rule for 0 was never matched (the game never put that option to this seat); Cleo: the rule for 1 was never matched (the game never put that option to this seat)
- FAIL: Third token eliminates: seat 3 out, no card, skipped next round | rule R20 is broken: When a player reaches 3 tokens, then alive becomes false, they get no more cards and they are skipped in turn order.; seat 3 tokens: expected 3, got 2; seat 3 alive: expected False, got True; game opener_seat: expected 2, got 1; game deck: expected 18 items, got 20; seat 3 platform status: expected 'out', got 'playing'; Ada: the rule for 'coyote' was never matched (the game never put that option to this seat); Ada: the rule for 1 was never matched (the game never put that option to this seat); Blaise: the rule for 0 was never matched (the game never put that option to this seat)
- FAIL: Opener moves clockwise from 3 to 4 even though another seat lost | rule R21 is broken: When a hand ends, then opener_seat moves to the next alive seat clockwise from the current opener, whoever lost; if the opener was eliminated, it moves to the next alive seat clockwise from their seat.; seat 1 tokens: expected 1, got 0; game opener_seat: expected 4, got 3; Cleo: the rule for 'coyote' was never matched (the game never put that option to this seat)
- FAIL: Eliminated opener 2: opener moves to seat 3 | rule R21 is broken: When a hand ends, then opener_seat moves to the next alive seat clockwise from the current opener, whoever lost; if the opener was eliminated, it moves to the next alive seat clockwise from their seat.; seat 2 tokens: expected 3, got 2; seat 2 alive: expected False, got True; game opener_seat: expected 3, got 2; seat 2 platform status: expected 'out', got 'playing'; Blaise: the rule for 'coyote' was never matched (the game never put that option to this seat)
- FAIL: Last rival eliminated: game ends and the sole survivor wins | rule R22 is broken: When only one player is alive, then the game ends immediately and that player wins.; seat 2 standing: expected -3, got 8; seat 2 tokens: expected 3, got 2; seat 2 alive: expected False, got True; seat 2 platform status: expected 'out', got 'playing'; Ada: the rule for 'coyote' was never matched (the game never put that option to this seat)
- FAIL: Round 40 ends with an unfinished hand: no token, fewest tokens wins | rule R23 is broken: When round 40 ends with two or more players alive, then any unfinished hand is discarded with no token, and the alive player with the fewest tokens wins.; seat 1 standing: expected 10, got 9; seat 2 standing: expected 9, got 8; seat 3 standing: expected 8, got -3; seat 1 tokens: expected 0, got 1; seat 2 tokens: expected 1, got 2; seat 3 tokens: expected 2, got 3
- FAIL: Round 40 ends with seats 1 and 2 tied on fewest tokens: shared result | rule R24 is broken: When round 40 ends and two or more alive players tie for fewest tokens, then the game is a draw between them.; seat 1 standing: expected 9, got 8; seat 2 standing: expected 9, got 8; seat 3 standing: expected 8, got -3

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 4], results {'seat 2': 16, 'seat 1': 13, 'seat 3': 9, 'seat 4': 2}, 13-35 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- empty: an announcement says nothing (in `the_cards_you_can_see`: '"card": null'); skip the announcement when there is nothing to say, or give it an `if` (in 30 of 6 matches)
- cost of a match: 24.3 decisions, prompts of 229 characters on average (longest 242)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 2': 21, 'seat 1': 22, 'seat 3': 17}
- always `first@seat1`: won 19, lost 41, drew 0
- always `first@seat2`: won 23, lost 37, drew 0
- always `last@seat1`: won 0, lost 60, drew 0
- always `last@seat2`: won 0, lost 60, drew 0

## Triage (whose problem each failure was)

- round 1: fix_game: Every failing scenario fails the same way: a responder was never offered the option 'raise'. The tests that only use 'call_coyote' and the opener's numeric declaration pass, so the game's response step is missing the RAISE choice the rules require (or names it differently), and later seats never get to raise.
- round 1: fix_tests: The game handled a declaration of 60 correctly. No raise is possible, so seat 2 was recorded as caller, the true total of 19 was below 60, and seat 1 (the declarer) took the token, exactly as the rules require. The test failed only because it demands that seat 2 be shown a menu holding the single forced option. Skipping a choice that has only one possible answer is legitimate and changes no result or score.
- round 1: fix_tests: The game deals 1 card per player from the 33-card deck correctly: the trace shows the deck going from 33 to 30 during the hand. It then returns the cards after resolution, so after a full round the deck is back at 33, ready for the next hand's fresh shuffle. The deck-count tests read internal bookkeeping at a moment the rules don't pin down. The 60-declaration test relies on an option literally named 'raise', a name the interface never defines; the game takes raises as numeric bids.
- round 2: fix_game: The failures point to the game's own turn and hand bookkeeping, not to the tests or the rules. When a hand is already in progress, nobody acts, so Coyote and raises are never offered and no token moves. With opener 3 and seat 2 eliminated, the wrong seat takes the token. This suggests the turn order is a list built only when a new hand is dealt, and that a separate has_declaration flag is used instead of the rule variables hand_active and current_declaration.
- round 2: fix_game: The game file has two rule bugs. It draws from the deck it already holds instead of rebuilding the full 20-card deck when a new hand begins (R3), so it crashes on a short deck. It also resolves Coyote wrongly when the true total equals the declaration: the declarer loses where R7 says the caller does, which shows up in both the plain and the Max→0 scenarios.
- round 2: fix_game: In every scenario that starts with a hand already in progress (hand_active true, current_declaration set), the game played zero moves. It advanced the round without offering any seat a turn: order stays [] and turn_seat stays 0. The game builds its turn order only when a new hand is dealt, so a continuing hand has no turns, which breaks R4 and R5.

## Choices the rules did not make

- 3 to 4 players, suggested 4: The designer chose 4. Three is the smallest table where each player reads two other cards and must guess their own while rivals push the bid. More than 4 would exceed the source's range and the 20-card deck design.
- No table talk step: The rules say declarations and calls are the only communication.
- Max→0 is stored as card code 100: Keeps every card a number, so the true total is pure arithmetic: code 100 counts as 0 and triggers cancelling the highest positive other card.
- Rank by alive*10 - tokens: Puts every alive player above every eliminated one and orders alive players by fewest tokens.
- Strategy noted: A good player infers their own card from the visible cards and from how others raise, and calls Coyote or raises depending on how plausible the claim is. A careless one declares at random.

## Simplifications

- A round is written as four conditional turn steps (1st to 4th alive seat clockwise from opener_seat), each skipped once Coyote is called or when fewer seats are alive: The step list is flat; per-step when-conditions reproduce variable turn counts and skipped turns.
- A tie for fewest tokens at round 40 is represented as a shared win among the tied players: The engine has no separate draw; tied top ranks share the result, which stands for the draw.

## Encoding attempts

- 1: passed
