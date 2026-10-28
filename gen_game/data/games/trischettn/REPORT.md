# trischettn: ready for review

Built from the variation **Trischettn Duel** (design round 2); see VARIATION.md.

## What was changed from the original, and why

- Remove declarations entirely. (fixes: Declarations are scored mostly from luck of the deal or draw and outweigh card-play decisions (3-4 of about 11 points per deal).): Declarations were mainly a reward for the deal. Removing them makes card play decide the score and deletes every attribute that failed to update.
- Delete the declaration bookkeeping (declared_this_deal, declared_cards_shown, decl_value, decl_cards, decl_answer). No scratch attribute is kept that some step does not change every trick. (fixes: The declaration mechanic (only after winning a trick, opt-in, once-per-deal marks, cards reusable) produced attributes that never changed in testing (declared_this_deal, declared_cards_shown, decl_value, decl_cards), so the game could not be built.): Every remaining attribute changes in normal play.
- Remove drawn_hidden_card from shown state. Every public field starts with a non-empty value: led_card and followed_card start as 'none', and talon_up shows 'none' once the talon is empty. (fixes: Scratch fields (decl_answer, drawn_hidden_card) and a talon_up field that went blank when the talon ran out appeared empty in the state shown to players.): The state shown to players never contains a blank field.
- Fixed match of exactly 2 deals of 16 tricks (32 rounds, one trick per round). Player A leads the first trick of deal 1 and Player B leads the first trick of deal 2. (fixes: Playing to 31 or 41 points takes about 48 or more tricks, beyond the 40-round limit, and an open-ended match length is hard to build.): This fits the round limit, balances the opening lead, and lets a second deal reduce the luck of a single deal.
- Score in whole pips: Ace 3, Ten/Nine/King/Ober/Unter 1, Eight/Seven 0, last trick of a deal 3. This gives 35 pips per deal, the original 11-and-a-bit points times three, with no rounding. (fixes: Card points in thirds with rounding down after summing are awkward to track and create artificial ties.): Integer arithmetic only. Each deal's total is odd, so a single deal cannot tie.
- The game is for 2 players only. (fixes: The 3- and 4-player variants add discards and partnership gestures that the engine cannot support cleanly.): The 2-player form is the base game and the one that fits the engine.
- The top card of the talon lies face up (talon_up). The trick winner takes that visible card and the loser takes the next, hidden card. A new top card is then turned face up. (fixes: A completely hidden talon makes the decision to win or lose a trick for its draw rather thin.): Players must decide whether winning a trick is worth it for the visible card, and the loser's hidden draw is an inference target for the winner.

Objective: After 2 deals (32 tricks), each player's match total is the sum of their pips from both deals, out of 70 pips available. The higher total wins. If both totals are 35, the match is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. PIP ARITHMETIC. Each suit holds Ace 3 + Ten, Nine, King, Ober, Unter at 1 each (5) + Eight, Seven at 0 = 8 pips. Four suits give 32, plus 3 for the last trick, so 35 per deal and 70 per match, as stated. Totals sum to 70, so a draw happens only at 35-35, which is consistent with the winner rule. TRI
- playable: pass. RULES. Card flow is complete: 8+8 dealt and 16 in the talon. Each of tricks 1-8 consumes 2 talon cards, so the talon empties after trick 8. Hands then fall from 8 to 0 over tricks 9-16, giving 16 tricks and 32 cards. The talon-up card, the follow-suit rule, the trick winner, pip scoring, the last-tr
- reasoning_over_luck: pass. WHAT TO INFER. (a) Which cards the opponent holds: from talon-up cards they took publicly, from cards played, and from failures to follow suit, which reveal voids. (b) Whether to win or lose a trick: the winner gets the known talon-up card and the loser a blind card. (c) After trick 8 every unseen c

## Complexity

- steps_per_round: designed 15, built 9, limit 20
- choice_steps_per_round: designed 2, built 2, limit 4
- attributes: designed 12, built 65, limit 20 (built: 80)
- hidden_elements: designed 2, built 25, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 32, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Match starts in deal 1 at trick 1 (observable setup only)
- pass: First deal forms a 16-card talon; after trick 1 two cards have been drawn (chance-independent counts only)
- pass: Deal start sets talon_count 16, whatever it was before; after one trick it is 14
- pass: Deal 2 starts after trick 16 of deal 1 with a fresh talon and match totals kept (chance-independent)
- pass: Leader may play any card; a 0-pip trick changes no pips
- pass: Follower holding the led suit is offered only that suit
- pass: Follower void in the led suit is offered every card
- pass: Ten (strength 8) beats Ace (strength 6) of the led suit
- pass: Nine (7) led beats a lower King (5) following suit
- pass: Off-suit Ten does not win: no trumps, leader takes the trick
- pass: Winner adds Ace 3 + Unter 1 to deal_pips
- pass: Trick 16 adds 3 bonus pips (Ace 3 + Seven 0 + 3 = 6) and closes deal 1
- pass: Winner takes talon_up, loser takes the next talon card; both then appear in their hands
- pass: New top card becomes talon_up after a draw that leaves cards
- pass: Last draw empties the talon (talon_up none); trick 9 has no drawing
- pass: Follower who wins the trick leads the next one
- pass: End of deal 1 adds deal_pips to match_total
- pass: Scored deal totals 35 pips (14 + 21)
- pass: After round 32 the game ends and the higher match_total wins
- pass: 35 each is a draw shared by both seats
- pass: Public trick state is visible after a trick

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [2], results {'seat 1': 12, 'seat 2': 7, 'seats 1 and 2': 1}, 48-56 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 64.0 decisions, prompts of 139 characters on average (longest 147)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 1': 35, 'seat 2': 23, 'seats 1 and 2': 2}
- always `first@seat1`: won 33, lost 25, drew 2
- always `first@seat2`: won 25, lost 33, drew 2
- always `last@seat1`: won 25, lost 32, drew 3
- always `last@seat2`: won 27, lost 31, drew 2

## Triage (whose problem each failure was)

- round 1: fix_game: Every failure is a presentation slip in the file, not a problem with the rules or the platform. Prompts use placeholders the step cannot fill ({decl_value}, {decl_cards}), and internal scratch attributes (decl_answer, drawn_hidden_card, follow_card, led_card) are left visible. The coder has been fixing one of these and reintroducing the other, so both must be fixed together.
- round 1: revise_rules: Over four attempts the coder has swung between the same two failures: empty internal fields in the shown state, and the declaration bookkeeping (declared_this_deal, declared_cards_shown, decl_value, decl_cards) never firing in random matches. The declaration is gated by several conditions at once (won the previous trick, not yet declared, holds a qualifying three-of-rank or Napoli, chooses to declare), so it is both rarely reached and hard to detect with flat arithmetic steps over a hand. The interface also requires a public `talon_up` that is legitimately empty for half of every deal.

## Choices the rules did not make

- 2 players (min 2, max 2, suggested 2): The designer set 2. The game is a duel: one leader and one follower per trick, with a talon split between winner and loser. A third player would break the follow-and-draw structure.
- Card names written as text like 'Ace of Bells', with strength and pips taken from the parameter table: The engine has no card type. Strength and pip values are listed as parameters so the trick and scoring arithmetic is explicit.
- talon_count counts the talon-up card: The rules ask for 'the number of cards left in the talon' to be public. Counting the face-up card makes it 16 at the start and 0 after 8 tricks.
- No talk step: The rules have no table talk. In a two-player zero-sum duel, talk would add words without a real decision about whether to trust a proposal.
- Strategy at the table: A thoughtful player tracks played cards and openly drawn talon cards, decides when to win a trick for talon_up versus duck to save strong cards, keeps Aces (3 pips) safe, and plans the endgame for the 3-pip last trick.

## Simplifications

- The deal is run as conditional updates inside the round steps (when trick_number = 1) instead of as separate deal phases: The step list is flat. A single step with an arithmetic 'when' condition reproduces the start of deal 1 and deal 2.
- The talon-up card taken by the winner goes into their ally-visible hand, and is only announced publicly at the moment it is taken: The engine has no per-card visibility inside a list. The card was already public as talon_up, so players keep the same knowledge the rules give them.

## Encoding attempts

- 1: it plays, but part of it does nothing: game attribute `hearts` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `bells` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `leaves` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `acorns` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 2: passed
