# libertalia: ready for review

Built from the variation **Libertalia: Shared Hand** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Reduce the character set to 7 cards, ranked 1-7, each with one simple arithmetic ability resolved in a single phase. (fixes: There are far too many character abilities with phase-chained effects (day, dusk, night) to build within 20 steps per round.): This keeps the mind-game of identical hands while fitting the step limit.
- Booty is assigned automatically: non-tied players take tokens from best to worst in descending rank order. (fixes: Sequential booty picking by up to 6 players needs more than 4 choice steps per round. The choice is also mostly obvious, since everyone takes the most valuable token.): Picking the highest token was nearly forced anyway. Automating it removes choice steps while rank still decides who gets what.
- Booty is plain numeric tokens (5, 3, 1, and -3 for a cursed relic) in a daily row drawn from a fixed list of 6 rows. (fixes: Side tokens (maps in sets, sabers, officers) add state and rule chains without adding much inference.): This is one random draw per round with no set collection. The cursed relic preserves the pressure not to end up last.
- Same-rank ties become a Clash: all tied characters get nothing and their abilities do not fire. (fixes: Ties are broken by fixed player influence numbers, which gives some seats a permanent edge in ties.): Removing seat-based tie-breaks deletes the seat edge. Clashes also punish predictable play, because copying the obvious card is risky.
- Use 2 campaigns of 5 days. Each player gets the same 7-card hand per campaign and plays 5, so 2 cards go unused. The hand is refreshed for campaign 2. (fixes: The game is too long: 3 campaigns of 6 days, card keeping and redraws.): 10 rounds stays within limits. Saving cards is still a multi-round plan, and the shrinking known hands drive inference.
- Fix the game at exactly 3 players, with a simultaneous one-message talk phase before cards are played. (fixes: The variable player count of 2-6 makes booty rows and balance hard to fix. With 2 players under a highest-total rule, the game is purely zero-sum.): With 3 players, one rival's loss is not automatically the other's gain, and booty rows can be balanced. Talk allows bluffing and feinting about which card you will play.

Objective: After 10 rounds, the player with the highest doubloon total wins. If two or more players share the highest total, they draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. TOKEN TABLE (best/second/worst): A 5/3/1, B 5/1/-3, C 3/3/1, D 5/3/-3, E 3/1/-3, F 5/5/-3. Averages: best 26/6=4.33, second 16/6=2.67, worst -10/6=-1.67. All values below assume the card is not clashed.

CARD VALUES:
- Cabin Boy (1) is a flat +3.
- Admiral (7) always takes the best token, minus 2. P
- playable: pass. RULES COVERAGE: The rules cover every case:
- Clashes are defined for two or three matching ranks.
- Non-clashed ranks are distinct, so the booty order has no ties.
- At most 3 takers face 3 tokens, and leftovers are discarded.
- The Cabin Boy is excluded from booty.
- The Gunner and Quartermaster c
- reasoning_over_luck: pass. THE RANDOM ROW: The only random element is the row. It is drawn before choices, announced, and shared by all, so it is information to act on rather than a hidden luck source. The spread between best and worst token varies from 2 (row C) to 8 (row F). This changes the relative value of the Bosun, Mer

## Complexity

- steps_per_round: designed 14, built 10, limit 20
- choice_steps_per_round: designed 2, built 2, limit 4
- attributes: designed 17, built 55, limit 20 (built: 80)
- hidden_elements: designed 1, built 2, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 10, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: every seat starts at score 0 with a full 7-card hand (checked after one all-clash day)
- pass: Each day a booty row of 3 tokens is drawn (chance: only its size is asserted)
- pass: Talk step happens, then all seats play their cards
- pass: Played rank is revealed and removed from the hand
- pass: A card no longer in hand is not offered
- pass: Two seats on the same rank both clash and get nothing
- pass: Three seats on the same rank all clash
- pass: Higher rank takes the best token, next takes the second
- pass: Cabin Boy takes no token and gains 3
- pass: Gunner makes the Captain and the Admiral lose 3
- pass: Quartermaster gains 1 per other non-clashed higher rank
- pass: Bosun's negative token counts as 0
- pass: Merchant taking a token of 3 or more gains 2 extra
- pass: Captain takes booty normally with no ability
- pass: Admiral loses 2
- pass: Score changes by token + ability and can go negative
- pass: Day 6 resets every hand to the full 7 cards
- pass: No hand reset on an ordinary day mid-campaign
- pass: Game ends after day 10 and the highest score wins
- pass: Tied leaders after day 10 share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [3], results {'seat 1': 8, 'seat 2': 8, 'seat 3': 3, 'seats 1 and 2': 1}, 60-60 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 60.0 decisions, prompts of 114 characters on average (longest 120)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 1': 21, 'seat 2': 18, 'seat 3': 16, 'seats 1 and 2': 2, 'seats 2 and 3': 2, 'seats 1 and 3': 1}
- always `first@seat1`: won 21, lost 36, drew 3
- always `first@seat2`: won 19, lost 38, drew 3
- always `last@seat1`: won 30, lost 29, drew 1
- always `last@seat2`: won 32, lost 26, drew 2

## Choices the rules did not make

- 3 players (min = max = suggested = 3): The designer fixed 3. With 3 seats, clashes are a real risk and the three tokens are enough for everyone. A different count would change the token count and how clashes play out.
- Keep the simultaneous talk poll before the card poll: The rules require it. Players disagree, since each wants the others to avoid their rank, so a bluff or proposal is worth weighing, and messages are not binding.
- Hands are public attributes: All hands start identical and played cards are revealed, so the remaining hand can be worked out by everyone. Only the day's choice is secret, and the simultaneous poll keeps it so.
- Gunner penalty is a flat 3: Only one non-clashed Gunner can exist on a day, because two Gunners clash each other.

## Simplifications

- Booty rows are stored as a list of token lists, and the row is picked at random without removal: Drawing with replacement needs no deck depletion.
- Leftover tokens and discarded cards are not tracked: The rules never refer to them again.

## Encoding attempts

- 1: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state a player is shown has empty fields (choice, message, message, message); hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 2: it plays, but part of it does nothing: game attribute `booty_rows` is never changed in 3 random matches, so nothing updates it. Steps that name it: set the day. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.; game attribute `full_hand` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 3: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state a player is shown has empty fields (message, message, message); hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 4: passed
