# greek_hold_em: ready for review

Built from the variation **Greek Hold 'em Mini II** (design round 2); see VARIATION.md.

## What was changed from the original, and why

- Play 36 hands instead of 12. (fixes: P1): Per-game edge/σ grows with the square root of the number of hands, about 1.7× from length alone. Combined with the larger per-hand edge from the other changes, a skilled player should be clearly favoured. Duplicate dealing was rejected because replaying a shuffle with rotated hole hands tells players the other hands they held earlier, which leaks hidden information.
- Only board cards 1-3 are face up when betting; board card 4 stays face down until showdown. (fixes: P2): A hand can still gain 4 points if card 4 matches, so draws, card-removal reasoning and bluffing against possible improvement all matter. Hand strength is no longer certain.
- Replace the simultaneous opening bet and FOLD/CALL/RAISE decision with one sequential betting round. Each player, in an order that rotates each hand, chooses CHECK, BET 2 or BET 4 until someone bets. Later players then CALL or FOLD, and players who checked earlier respond with CALL or FOLD. (fixes: P3): A bet of 2 or 4 into a pot of 3 gives real fold equity. A bluff of 4 needs both others to fold only about 57% of the time, and a bluff of 2 about 40%. Players act on others' visible actions. Bet sizing becomes a signal that can be honest or deceptive. Check-then-call traps and stealing from the last seat become real options.
- The first actor rotates every hand, so each seat acts first 12 times, second 12 times and last 12 times. (fixes: P4): Sequential order creates positional information to exploit, and the rotation keeps seats balanced.
- Remove the table-talk step. (fixes: P5): In this zero-sum poker game talk is cheap and unverifiable. Bets already serve as costly, credible communication. Dropping talk shortens a 36-hand game and saves steps.
- Remove the carry and the separate raise stage. Because a bettor can never fold, the pot always goes to someone. (fixes: P6): This simplifies the build. The step count per hand falls to 15 and choice steps to at most 4 while keeping every meaningful decision.

Objective: After 36 hands, the player with the highest chip total wins. If two or three players share the highest total, the game is a draw among them.

## The critic (3 review(s) before the rules went to a coder)

- balanced: pass. SEAT BALANCE. The first actor in hand h is ((h-1) mod 3)+1. 36 is divisible by 3, so each player is first, second and third actor exactly 12 times. Information is symmetric: everyone sees the same 3 board cards and only their own hole cards. Within a hand, acting last is an advantage, but the rotati
- playable: pass. COMPLETENESS. Every branch of the betting is defined.
- Unbet: CHECK, BET 2 or BET 4.
- Facing a bet: CALL or FOLD.
- A bet after one or more checks: the earlier checkers answer in a simultaneous poll (correct for a same-moment choice).
- One bet per hand, no raises, and the bettor never acts again.
- reasoning_over_luck: pass. WHAT THERE IS TO INFER.
- By the time you bet you know 5 of the 18 cards and your score except for board card 4.
- A needed rank with k unseen copies arrives as card 4 with probability k/13, worth +4.
- Opponents' hole cards are hidden. They must be inferred from card removal and from their action: 

## Complexity

- steps_per_round: designed 15, built 13, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 18, built 39, limit 20 (built: 80)
- hidden_elements: designed 2, built 6, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 36, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: R1: a hand is dealt; chance only decides ranks, so assert the 4-card board and the 2-card reveals after an all-check showdown
- pass: R2: ante of 1 each makes pot 3; bet 4 and two folds give +2/-1/-1
- pass: R3: betting happens over 3 visible board cards, and the board shows 4 after the hand (card values are random)
- pass: R4: in hand 2 seat 2 acts first, then seat 3, then seat 1
- pass: R4: in hand 3 seat 3 acts first
- pass: R5: a BET 2 adds 2 to the pot
- pass: R6: after a bet, later actors may only CALL or FOLD (showdown result is random)
- pass: R7: earlier checkers answer CALL or FOLD to a later bet
- pass: R8: only one bet; the bettor never acts again (showdown is random)
- pass: R9: a folder loses the ante and its hole cards stay hidden
- pass: R10: board card 4 is face up after betting
- pass: R11: scores come from random cards; only assert that showdown hands are published
- pass: R12: an uncontested winner takes the pot unrevealed
- pass: R13: a two-player showdown reveals both hands (winner is random)
- pass: R14: ties are random; only the folder's loss is fixed in a contested pot
- pass: R15: three checks go to showdown with pot 3 and no response step
- pass: R16: totals change by won minus paid from prior fractional totals
- pass: R17: after hand 36 the highest total wins
- pass: R17: tied leaders after hand 36 share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [3], results {'seat 1': 10, 'seat 3': 4, 'seat 2': 6}, 114-123 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 120.7 decisions, prompts of 232 characters on average (longest 259)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 1': 24, 'seat 3': 16, 'seat 2': 20}
- always `first@seat1`: won 28, lost 32, drew 0
- always `first@seat2`: won 29, lost 31, drew 0
- always `last@seat1`: won 18, lost 42, drew 0
- always `last@seat2`: won 11, lost 49, drew 0

## Triage (whose problem each failure was)

- round 1: revise_rules: The file works as specified, but the betting structure lets a mindless policy dominate: always taking the last option (bet the maximum 4, never back down) wins 56 of 60 games from seat 1. Opponents who are uncertain fold often and hand over the pot, so raw aggression beats any judgment of card strength.

## Choices the rules did not make

- 3 players (min = max = suggested = 3): The designer fixes the game at three seats. The actor rotation, the response step and the split pots all assume exactly three players. With three, bluffing works because a bet must get past two opponents, one of whom may hold the third copy of a rank.
- No pre-choice talk step: The source has no table talk. The information in play is the actions themselves (check, bet size, call or fold), so adding talk would add a mechanic.
- Responders are identified by action = CHECK while bet_amount > 0: Anyone still showing CHECK once a bet exists must have checked before the bet. Since only one bet is possible, this matches 'each player who checked before the bet'.
- Score computed for everyone, but published only at a showdown with 2 or more players: This keeps the arithmetic uniform while honoring the rule that folded hands and uncontested winners' hands are never revealed.
- Strategy at this table: A thoughtful player weighs the visible board against their hole cards, bets 4 with strong pairs or matches, uses bet size and position to bluff, and reads opponents' checks and calls over 36 hands. A thoughtless player calls or bets blindly.

## Simplifications

- Ante, bets and calls are tracked in `paid`, and the net change is applied to `total` at the end of the hand: This is arithmetically the same as paying at once, and it keeps fractional split pots exact.

## Encoding attempts

- 1: players are sent text with a `{name}` that was never filled in: placeholder: players are shown the literal {hole} (in `prompt`: 'Hand 1. You act first. Board: [2, 4, 1]. Your hole cards: {hole}. Pot 3. CHECK, BET 2 or B'); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {hole} (in `prompt`: 'Hand 1. You act second. Board: [2, 4, 1]. Your hole cards: {hole}. Pot 7, current bet 4. I'); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {hole} (in `prompt`: 'Hand 1. You act third. Board: [2, 4, 1]. Your hole cards: {hole}. Pot 11, current bet 4. I'); use only names the step can fill in (see the broadcast rule: {value} and {seat})
- 2: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (action, resp, action, action) in `your_cards`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 3: it plays, but part of it does nothing: game attribute `full_deck` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 4: passed
