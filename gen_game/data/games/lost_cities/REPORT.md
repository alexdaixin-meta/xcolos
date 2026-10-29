# lost_cities: ready for review

Built from the variation **Lost Cities: Wager Draft** (design round 2); see VARIATION.md.

## What was changed from the original, and why

- Track only top value and sum per player and colour, and drop the card count. Replace the 4-card bonus with a bonus for a column sum of 25 or more. Store each revealed card as a single attribute such as 'Red 7'. (fixes: P1: The previous variation's attribute count (24) exceeded the limit of 20, and its step count was unverified.): This brings the attribute count to 19, and the steps per round are written out at 16.
- Each round, reveal a public row of 2 cards. The priority player picks one card or none, then the other player picks from what is left. There are 12 rounds and 24 of the 27 cards are shown. (fixes: P2: Order luck dominated. Each player passively accepted one card at a time in the order it arrived, so the arrival order of their own colour decided their score.): A shared draft makes order luck hit both players alike. The question becomes which card to take and which to leave the opponent, not whether one's own colour arrives kindly.
- Replace the dealt Backed colour with a secret Wager. At the start of round 5, after 8 cards have been seen and drafted, both players choose one colour to double, at the same moment and in secret. (fixes: P4: The dealt hidden type acted as a lottery. Who got the colour that happened to arrive in the friendlier order decided the winner when both played well.): The hidden element becomes a decision made with information, like playing a wager card in Lost Cities. It is no longer a random gift. Each player must also read and hide which colour is doubled.
- All colours are open to both players, and denying a card means taking it into your own column or burying it at -3. (fixes: P3: Independently dealt Backed colours usually differed. This made the two players' games nearly separate, so interaction and denial were thin.): Every pick both builds your columns and denies the opponent's. Players compete for the same colours, so guessing the opponent's Wager matters.
- Show 2 cards per round and leave only 3 cards unseen. The deck composition is public. (fixes: P5: The 7 deck cards that were never revealed, plus seeing only one card at a time, left planning with little to work on.): Players can count what remains in each colour and plan their rising sequences.

Objective: After round 12, the player with the higher total wins. Equal totals are a draw.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. SCORING TABLE (one colour): empty = 0, or -15 if it is the Wager colour. Otherwise base = sum - 10, doubled if it is the Wager colour (negatives too), +10 if sum >= 25. Examples: sum 8 non-wager = -2; sum 8 wager = -4; sum 22 non-wager = +12; sum 24 wager = 28; sum 27 wager = 34+10 = 44. A buried ca
- playable: pass. RULES:
- Order is fully specified: priority picks and places, then the other picks.
- 'Naming the taken card = NONE' covers collisions. Unique values per colour mean 'higher than top' is never tied.
- Placement and burial are mandatory and defined. Untaken cards are removed.
- The wager is clearly a
- reasoning_over_luck: pass. CHANCE: the deal order decides which cards land in whose priority rounds and whether long ascending runs are possible. I estimate roughly 30-40% of the result is chance.

SKILL DECISIONS:
- Card counting: the full composition is public, and the only unknowns at the end are 3 cards.
- When to open a 

## Complexity

- steps_per_round: designed 16, built 10, limit 20
- choice_steps_per_round: designed 3, built 3, limit 4
- attributes: designed 19, built 41, limit 20 (built: 80)
- hidden_elements: designed 1, built 10, limit 3
- random_draws_per_round: designed 0, built -, limit 1
- rounds: designed 12, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: 27-card deck, all expeditions and burials at 0
- pass: Odd round 1 gives priority to seat 1
- pass: Even round 2 gives priority to seat 2
- pass: One round draws two cards, so the deck shrinks from 27 to 25
- pass: Both seats are offered a Wager colour in round 5
- pass: No Wager is asked outside round 5
- pass: Priority seat picks, then the other seat picks the other card
- pass: Second seat naming the taken card gets nothing
- pass: Red 7 on red_top 3 raises the top to 7 and the sum by 7
- pass: Red 7 on an empty Red gives top 7 and sum 7
- pass: Red 5 on red_top 7 is buried for +3 burial
- pass: A card equal to the top is buried too
- pass: Choosing NONE changes nothing for the player
- pass: Untaken cards leave the game and do not return to the deck
- pass: After the round both players' public tops, sums and burials show the placements
- pass: Empty Wager colour scores -15, other empty colours score 0
- pass: Non-empty expedition base is sum minus 10
- pass: Wager colour doubles the base, negative or positive
- pass: Sum of 25 or more adds 10 after doubling
- pass: Score is the three colour scores minus burial
- pass: Equal final scores share the win
- pass: Full 12-round game with no picks ends after round 12 with 3 cards left and empty Wagers at -15 each

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [2], results {'seat 1': 15, 'seat 2': 5}, 26-26 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 26.0 decisions, prompts of 285 characters on average (longest 336)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 1': 33, 'seat 2': 27}
- always `first@seat1`: won 38, lost 22, drew 0
- always `first@seat2`: won 41, lost 19, drew 0
- always `last@seat1`: won 9, lost 51, drew 0
- always `last@seat2`: won 8, lost 50, drew 2

## Triage (whose problem each failure was)

- round 1: revise_rules: The game is built to the rules, but a thoughtless 'always take the first option' policy wins about 85% of matches from either seat. That means a near-mindless line, probably playing or discarding the oldest card and always drawing from the draw pile while avoiding penalties and negative columns, beats varied play. The scoring rewards passivity and punishes any attempt to build columns.

## Choices the rules did not make

- Exactly 2 players, suggested 2: The designer fixed the table at 2. The draft is a head-to-head contest over a shared row, and the second pick depends on reading the one opponent.
- No talk step: The rules include no talk, and with two players in direct competition a message would add nothing the rules ask for.
- Cards stored as 'Colour-Value' strings in the deck, split into card_a/card_b colour and value attributes when drawn: This lets placement and scoring be done by plain arithmetic comparisons on numbers.
- The second player is still offered the taken card: The rules say that naming the taken card counts as NONE, so the option exists and is resolved to NONE.
- Strategy at the table: A thoughtful player times the Wager against the cards already seen in rounds 1 to 4. They also deny the opponent high cards, avoid burials that cost 3, and take NONE rather than bury a card.

## Simplifications

- The 'shuffle once, take the top two' draw is done as two random draws from the deck list each round: The engine draws at random from a list. This is equivalent to drawing from the top of a shuffled deck.
- Removed and buried cards are not kept in a discard list: The rules take them out of the game and never refer to them again. Only the burial counter matters.

## Encoding attempts

- 1: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state a player is shown has empty fields (wager, card_a_colour, card_b_colour, fate_first); hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 2: it plays, but part of it does nothing: game attribute `card_table` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 3: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state a player is shown has empty fields (wager, card_a_colour, card_b_colour); hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 4: passed
