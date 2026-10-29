# wyatt_earp: ready for review

Built from the variation **Wanted: Dead or Alive (Majority Rule)** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Commits no longer raise posters. Posters grow only from a fixed base ($2,000 each), public sightings (+$1,000) and a hidden informant tip (+$3,000, revealed at the end). (fixes: P1): Investing in a rival's outlaw now takes value from the rival instead of adding to it.
- Payout becomes majority-takes-all: the player with the most deputies on an outlaw takes its whole poster, tied leaders split it equally, and an outlaw with no deputies pays nobody. The 2x informant CP is dropped. (fixes: P1, P6): This turns the game into a contest of hidden-value allocation (Colonel Blotto). Piling everything on one outlaw wins at most one poster and leaves the rest to others. Contesting, defending, conceding and sniping all become real choices.
- Each informant secretly adds $3,000 to one outlaw's poster, known only to the player who holds that informant. Base posters are equal, so every informant is worth the same. (fixes: P3, P2): Private knowledge now matters. The holder knows an outlaw is worth more than it looks. Rivals must infer it from commitments and talk. The holder must choose between claiming openly (and inviting a contest) and hiding the claim. Because tips are equal and anyone can win any poster, this is information, not a lottery.
- Sightings stay random but are public, announced before players commit, and contestable by everyone. The rules now state the draw is uniform over the five outlaws, with replacement. (fixes: P2, P5): A sighting changes what is worth fighting for, not who gets it. Good play reacts to sightings, so they cannot decide the winner on their own.
- Deputies drop to 12 per player, at most 4 committed per round, over 6 rounds. All commitments are revealed each round. (fixes: P3, P6): The per-round cap makes timing a decision: commit early to stake a claim (which signals your informant) or hold deputies back for late snipes that rivals cannot fully answer. Public reveals give players the evidence to read informants from.
- The game is set at 3-4 players, keeping simultaneous talk before each commitment. (fixes: P4): Only one player can win. Players bargain over spheres ('you take Blue, I take Green'), bluff about informants, and gang up on a leader. Pacts are not binding, and a final-round snipe punishes anyone who trusts blindly.

Objective: The player with the most money after the final payout wins. If two or more players tie for the most money, the game is a draw.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. MONEY AT STAKE. Base posters are 5 × $2,000 = $10,000. Six sightings add $6,000. Tips add $9,000 with 3 players (3 informants) or $12,000 with 4. Total pot is $25,000 (3p) or $28,000 (4p). The expected value of one poster is $2,000 + 1.2 × $1,000 + (3/5 or 4/5) × $3,000, which is about $5,000 (3p) o
- playable: pass. RULES. They cover every case:
- Committing 0 is legal, and the chosen outlaw is then irrelevant.
- Over-commitment is capped at remaining deputies.
- An outlaw with no deputies escapes.
- Majority ties split the poster, rounded down.
- A tie for most money is a draw.
- Setup is defined: informants a
- reasoning_over_luck: pass. SOURCES OF CHANCE.
- Sightings: six random draws, but public, so any player can contest any sighted outlaw. They change what is valuable, not who gets it.
- Informant deal: random, but each tip is the same $3,000, and others can steal a tip by out-committing on that outlaw. Gaining the tip depends o

## Complexity

- steps_per_round: designed 11, built 12, limit 20
- choice_steps_per_round: designed 3, built 2, limit 4
- attributes: designed 13, built 41, limit 20 (built: 80)
- hidden_elements: designed 1, built 17, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 6, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: posters start at $2,000, players at 12 deputies, $0, no deputies on any outlaw (checked after one round of zero commitments with Green sighted)
- pass: Setup: each of 3 players draws a distinct informant, leaving 2 in the deck (which outlaws is chance)
- pass: Setup with 4 players leaves 1 informant in the deck
- pass: Sighted outlaw's poster rises by 1000
- pass: Same outlaw sighted twice rises 1000 each time
- pass: Talk step does not change any state; the round proceeds to commitments
- pass: Every seat is offered all outlaw/number combinations including 0 and 4
- pass: Committing 4 with 2 left commits only 2
- pass: Each player's choice is applied to their public counts
- pass: Committing 3 to Blue: deputies 12->9, d_blue 0->3
- pass: Commitments do not change posters
- pass: After round 6 each informant's poster rises by 3000
- pass: Outlaw nobody holds as informant gets no tip
- pass: Outlaws with no deputies escape and pay nobody
- pass: Strict majority on Blue takes the whole $5,000 poster
- pass: Three-way tie on a $5,000 poster pays $1,666 each
- pass: Money is the sum of payouts; unused deputies worth nothing
- pass: Game ends after round 6; players tied for most money share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 4], results {'seat 3': 7, 'seat 2': 15, 'seat 1': 9, 'seats 1 and 2': 1, 'seats 2 and 3': 1, 'seat 4': 5, 'seats 2 and 4': 2}, 36-48 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 42.0 decisions, prompts of 183 characters on average (longest 213)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 3': 16, 'seat 2': 22, 'seat 1': 20, 'seats 1 and 2': 1, 'seats 2 and 3': 1}
- always `first@seat1`: won 0, lost 60, drew 0
- always `first@seat2`: won 0, lost 60, drew 0
- always `last@seat1`: won 0, lost 58, drew 2
- always `last@seat2`: won 1, lost 58, drew 1

## Choices the rules did not make

- 3 to 4 players, suggested 3: The designer suggests 3, and the source allows 3 to 4. Majority contests need rivals, and 3 is the smallest table where a player can be outbid or split. With 5 informants the table cannot exceed 5, and the source caps it at 4.
- Talk kept as a simultaneous poll broadcast to all: The rules require it. Players disagree about which outlaws to contest and can bluff about their informant, so talk gives them something to reason about.
- Commitment offered as one combined choice of outlaw and number: This keeps both parts of the commitment in a single simultaneous poll, so no part is seen early.
- Remaining deputies made public: They follow directly from the announced commitments, so hiding them would hide nothing.
- Strategy at the table: A thoughtful player pushes deputies onto their own informant without giving it away, saves deputies for late sightings, avoids costly ties, and reads others' talk and commitments for hints about their informants.

## Simplifications

- A tie for the most money is a shared win rather than a separate draw: The engine ranks by one expression, and players level at the top share the win.
- End-of-game payout steps sit in the round with a 'round == 6' condition: The step list is flat. Conditional single steps reproduce the end-of-game payout exactly.
- Per-outlaw maximum and tie counts kept as table scratch attributes: Comparing player attributes needs a table attribute beside them.

## Encoding attempts

- 1: playing it with random seats failed: seed 1, 3 players: the match crashed: FlowError: "you.choice_outlaw == 'Red'" reads `you` where there is no player
- 2: players are sent text with a `{name}` that was never filled in: placeholder: players are shown the literal {deputies} (in `prompt`: "Secretly choose one outlaw and a number of deputies from 0 to 4, as '<outlaw> <n>'. You ha"); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {deputies} (in `prompt`: "Secretly choose one outlaw and a number of deputies from 0 to 4, as '<outlaw> <n>'. You ha"); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {deputies} (in `prompt`: "Secretly choose one outlaw and a number of deputies from 0 to 4, as '<outlaw> <n>'. You ha"); use only names the step can fill in (see the broadcast rule: {value} and {seat})
- 3: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (choice_outlaw, commit_raw) in `your_standing`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 4: it plays, but part of it does nothing: game attribute `outlaws` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 5: passed
