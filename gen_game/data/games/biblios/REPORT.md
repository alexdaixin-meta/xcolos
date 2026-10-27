# biblios: ready for review

Built from the variation **Biblios: Scriptorium Lots (revised)** (design round 3); see VARIATION.md.

## What was changed from the original, and why

- Each player takes at most one church action per round, however many Church cards they acquire. The engine records this as a yes/no church flag per player. Any extra Church card acquired the same round has no effect. Flags are cleared at the end of every round. (fixes: Multiple Church cards in one round are ambiguous.): This tells every player exactly what they are owed and keeps CHURCH as a single simultaneous choice step, inside the 4-choice limit. A second Church in one round becomes a known dead card, which players must price when bidding or splitting.
- Steps 4, 5 and 9 now say that a Church card 'sets that player's church flag'. Step 10 says that each player whose flag is set chooses one of 10 options. (fixes: Steps 4 and 10 are worded inconsistently.): One consistent wording across all steps.
- Public totals are no longer stored as numbers. Each player has a single text 'public record' that lists the face-up cards they received, appended as they arrive. The full attribute list is now explicit and totals 18. (fixes: The attribute count was not listed.): The announcement can show public cards without five extra numeric totals per player. Hidden true totals stay in the colour attributes and are never announced.
- Keep the previous variation's structure: 36-card public-composition deck, 3 players, 12 rounds, balanced active-seat order, simultaneous capped bids, simultaneous talk, strict-majority colour scoring, and gold as tiebreak. (fixes: The original's full deck, card-based Gold payment, steal-and-reauction rule and letter tiebreaks are too heavy for the platform.): Testing showed this structure is finite, arithmetic and balanced. Bids capped at current gold mean non-payment cannot happen.

Objective: The player with the most VP wins. If VP is tied at the top, the tied player with the most remaining gold wins. If that is also tied, the game is a draw among those players.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. STRUCTURE: 36 cards over 12 rounds × 3 = 36, so the deck runs out exactly. Each seat is active 4 times: seat 1 in rounds 1, 6, 8, 10; seat 2 in rounds 2, 4, 9, 11; seat 3 in rounds 3, 5, 7, 12. GIVE runs in a full cycle (1→2, 2→3, 3→1, four times each). Per player: 4 kept cards, 4 received gifts and
- playable: pass. COMPLETENESS:
- Deck composition, setup, rotation, card effects and the 6 split options are fully specified.
- Simultaneous sealed bids from 0 to current gold mean gold cannot go negative, so no 'cannot pay' case arises.
- Tie or all-zero bids discard the card.
- A Church card received through KEEP,
- reasoning_over_luck: pass. CHANCE: The only randomness is the single shuffle. It decides which triples each active player sees, where the three 4-value cards per colour fall in each colour, and where the 3 Church and 3 Gold cards land. Each player sees 4 triples (12 cards), and every triple must be split three ways, so a luck

## Complexity

- steps_per_round: designed 16, built 16, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 18, built 74, limit 20 (built: 80)
- hidden_elements: designed 3, built 20, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 12, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Start: gold 8, vp 0, every die 3 (checked after a quiet round 1 that changes none of them)
- pass: Start: the deck holds 36 cards, so 33 remain after round 1's deal
- pass: Round 1 makes seat 1 active
- pass: Round 6 makes seat 1 active
- pass: Round 9 makes seat 2 active
- pass: Three cards leave the deck and only the active seat splits them
- pass: The active seat is offered all 6 assignments
- pass: A kept Red 3 lifts seat 3's red total above seat 2's 2 and scores the Red die
- pass: Keeping Gold 4 raises gold by 4
- pass: A kept Church gives one church action
- pass: A second Church in the same round gives no second action
- pass: The kept card stays out of the public record
- pass: The given Gold 3 goes from seat 1 to seat 2
- pass: The given Gold 3 goes from seat 3 to seat 1
- pass: The auction card is shown publicly
- pass: Talk is not binding: the round goes on and gold is untouched
- pass: Each bid ranges from 0 to the seat's gold
- pass: The sole top bidder pays 5 and gains the Gold 4
- pass: A tied top bid discards the card and nobody pays
- pass: All bids 0 discards the card and nobody pays
- pass: Only the seats with church Yes move dice
- pass: Raising a die already at 6 does nothing
- pass: Seat order with clamping: purple at 1, seat 1 raises and seat 2 lowers, ends at 1
- pass: With no church flag nobody is asked and the dice stay at 3
- pass: The church flag resets after the round, so there is no church action in round 2
- pass: The game ends after round 12 with the deck empty
- pass: A sole leader scores the die value and a tied top scores nobody
- pass: A VP tie goes to the seat with the most gold
- pass: Level on VP and gold: all three share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [3], results {'seat 1': 5, 'seat 2': 7, 'seats 1 and 3': 2, 'seat 3': 6}, 85-87 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 87.0 decisions, prompts of 161 characters on average (longest 233)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 1': 20, 'seat 2': 15, 'seats 1 and 3': 3, 'seat 3': 21, 'seats 1 and 2': 1}
- always `first@seat1`: won 14, lost 46, drew 0
- always `first@seat2`: won 11, lost 49, drew 0
- always `last@seat1`: won 15, lost 39, drew 6
- always `last@seat2`: won 17, lost 41, drew 2

## Triage (whose problem each failure was)

- round 1: fix_game: The rules are buildable on this platform. The attempts fail on two file-level bookkeeping problems, and the coder keeps fixing one while bringing back the other: talk/auction_colour fields shown blank, and a static `lot_list` attribute that no step ever changes.
- round 1: fix_tests: The failing test checks the length of `lot_list`. That attribute is not in the interface: it is the coder's own scratch value, emptied while shuffling the lots into `lots`, which holds the 11 lots not yet used after round 1 was dealt. Everything the interface does define came out as the rules say: seat 1 kept B1, G4 went to auction, both bids were 0, the auction card went back to seat 1, all gold stayed at 12 and the worths stayed at 3.
- round 1: revise_rules: The game behaves as specified, yet a thoughtless policy dominates. Always taking the first option (keep the first card, bid 0) wins about 80-85% of matches, and always taking the last option (bid all your gold) almost always loses. Bidding is a losing proposition: the winner's gold goes straight to a rival, gold converts directly to VP, and tied or zero bids hand the card to the seller for free.
- round 2: revise_rules: The game was built correctly and behaves as specified, but the design itself breaks the evaluation limits: 21 steps and 5 choice steps per round, against limits of 20 and 4. It is also unbalanced, with seat 2 winning about twice as often as seat 1 or seat 3 against random play.
- round 3: fix_game: Every failure is a coding error in the file, not a problem with the rules. The file reads `you` in a step with no player, keeps attributes that no step sets (active_order, card_table, perms), and has church steps that never actually move die_blue. The design uses only supported features (hidden hands, simultaneous polls, numeric bids, a deck as list operations).

## Choices the rules did not make

- Exactly 3 players, suggested 3: The designer fixed the table at 3, and the 12-round active order and next-seat cycle are written for seats 1-3, so the minimum and maximum are both 3. At 3 an auction has two rivals, and a colour majority can be contested or shared.
- Strategy at the table: A thoughtful player keeps cards that build hidden majorities and gives away cards that cannot tip a colour. They bid according to what an auction card is worth in the colours they can win, and use Church to raise colours they lead and lower colours rivals lead. They also read public records and gold changes to infer the others' hidden kept cards.
- Talk kept, as a simultaneous poll broadcast to all: The source says all three write at the same time and messages are shown together. Players disagree about who should win each auction, so talk (bluffing about majorities, proposing who drops out of bidding) has strategic weight.
- Church flag visibility is ally (owner only): A kept Church card is face-down, so a public flag would reveal it. The rules publish only dice, gold and records.
- Rank expression vp*1000 + gold: Gold can never exceed 17 (8 at the start plus 9 from Gold cards), so the factor 1000 makes VP decide first and gold break ties. A remaining tie is a shared win, which matches the source's draw.
- Card representation as text like 'Red 3', 'Gold 4', 'Church': The source does not name a format; text labels let the effect be read off the card.
- Unwon auction cards go to a public discard list: The source says 'discarded' without naming a pile; a list keeps the card stated somewhere.
- List-valued numbers (card values, active order) split into separate numeric parameters: Parameters must each be a single number, so each count, value and per-round active seat is listed on its own.

## Simplifications

- Colour majority scoring uses comparisons kept beside the scores (for each colour, the top total and how many players hold it): The engine has no direct player-to-player attribute operand, so the workaround compares each player's total with maxima kept on the table.
- Dealt cards are held in a hidden table list and revealed privately to the active seat: A table attribute cannot be visible to one changing seat, so a private reveal provides 'shown only to the active player'.
- Final scoring is a round step gated by round == 12 before the ending check: The step list is flat; a single conditional update computes VP once, at the end.

## Encoding attempts

- 1: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state a player is shown has empty fields (church_choice, public_record, public_record, public_record); hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 2: it plays, but part of it does nothing: game attribute `die_blue` is never changed in 3 random matches, so nothing updates it. Steps that name it: the dice, the dice move. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.; game attribute `active_order` is never changed in 3 random matches, so nothing updates it. Steps that name it: shuffle the deck and fix the turn order. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 3: passed
