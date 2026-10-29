# put: ready for review

Built from the variation **Put: Sixteen Hands** (design round 3); see VARIATION.md.

## What was changed from the original, and why

- Trick 1 is played in sequence and in the open. The leader leads one card face up. The responder sees it and then chooses which card to answer with. (fixes: P1): Responding to a seen card rewards real reasoning. The responder can beat cheaply, duck with the lowest card, or spend a high card, and each choice changes what is left. For example, the responder holds 11, 9 and 6, and the leader leads a 4 while holding 12 and 8. Answering with the 6 wins tricks 1 and 3, and so the hand. Answering with the 9 or the 11 loses tricks 2 and 3, and so the hand. A random answer wins only 1 time in 3; correct play wins every time.
- Tricks 2 and 3 are played automatically by a fixed rule. Each player plays their higher remaining card to trick 2 and their lower remaining card to trick 3. (fixes: P1): This removes the blind matching that made the previous variation a lottery. Once trick 1 is played, the rest of the hand is decided by the cards, but each player knows only their own cards. The Put decision then becomes a matter of reading a hidden but fixed outcome. Choosing which card to lead and which to answer with becomes a planning decision, because it decides which two cards are left to meet high-against-high and low-against-low.
- The Put window moves to after trick 1. Both players choose Put or Check at the same moment. If exactly one player Puts, the other chooses See or Fold. If both Put, the Put counts as seen automatically. If both Check, the hand is played for 1 point. (fixes: P2, P3): Betting now uses what has been seen: the trick-1 cards, how the opponent chose to lead or answer, and one's own remaining two cards. Merging the Put and reply decisions keeps the game at exactly 4 choice steps.
- The stakes are raised. A plain hand pays 1 point, a seen Put pays 4, and a fold concedes 1 to the putter. (fixes: P4): Bluffing with a losing hand turns a 1-point loss into a 1-point gain if the opponent folds. Calling a bluff is worth 4. The betting layer now matters as much as the cards, without one hand settling the match the way 'whole game' did.
- The original scoring condition is restored: a player must win at least 2 of the 3 tricks to win the hand. Tied tricks belong to no one, so a trick plus two ties, or a trick each plus a tie, scores nothing. (fixes: P5): This matches the original's trick-and-tie rule. It also makes ducking and tying with an equal card real tactical options.
- The match lasts 16 hands, with the lead alternating so that each seat leads 8 times. (fixes: P6): More hands average out the deal. Exact alternation cancels the responder's information advantage across the match.

Objective: After 16 hands, the player with the higher total score wins. If the totals are equal, the match is a draw.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. PAYOFFS. Facing a lone Put, Fold costs exactly 1 point. See risks the stake of 4. If q is the chance of winning 2 tricks (ignoring ties), See is worth about 4q - 4(1-q) = 8q - 4. See beats Fold when 8q - 4 > -1, that is when q > 3/8. A Put that is folded to earns +1, the same as winning a both-Check
- playable: pass. DECK. Four copies of 13 values gives 52 cards, with value names given for every number. Ties are defined for every trick.

ORDER. Every step is specified, including the both-Put case (counts as seen, stake 4) and the both-Check case (stake 1). Step 9 runs only when exactly one player Puts. Scoring i
- reasoning_over_luck: pass. WHAT THERE IS TO INFER. After trick 1, each player knows:
- their own two remaining cards;
- the opponent's trick-1 card, which is itself a strategic choice that signals strength or a deliberate dump;
- the trick-1 result;
- the deck composition (four of each value).

Tricks 2-3 are deterministic on

## Complexity

- steps_per_round: designed 15, built 17, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 12, built 27, limit 20 (built: 80)
- hidden_elements: designed 1, built 4, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 16, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: R1: a new hand restores the deck, clears the old hands and advances hand_number (fold keeps the count deterministic)
- pass: R2: each player is dealt 3 cards from the deck (after one card each is played and the hand folds, 2 remain each and the deck holds 46)
- pass: R3: an even hand is played with seat 2 leading and hand_number advances to 2 (who leads is not observable)
- pass: R4: the leader plays one card from their own hand (2 left after a fold)
- pass: R5: the responder plays one card from their own hand (2 left after a fold)
- pass: R6: with a fold only trick 1 is compared, so the scores move only by the fold point (the trick-1 result depends on the deal)
- pass: R7: both seats are offered Put and Check in the put window
- pass: R8: a lone Put makes only the Checker choose See or Fold
- pass: R9: when both Put no reply is asked and all tricks are played (the scoring depends on the deal)
- pass: R10: when both Check no reply is asked
- pass: R11: a fold gives the Putter exactly 1 point and stops play, so each player keeps 2 cards
- pass: R12: with no fold trick 2 is played automatically, leaving no cards in hand after trick 3
- pass: R13: with no fold (a seen Put) trick 3 plays each player's last card, leaving empty hands
- pass: R14: with no fold all three tricks are played out (the trick counts depend on the deal)
- pass: R15: a seen Put plays out the hand (who scores the stake depends on the deal; only the hand count is asserted)
- pass: R16: a checked hand is played out (whether ties leave no one scoring depends on the deal; only structure is asserted)
- pass: R17: the match ends after hand 16 and the higher score wins
- pass: R17: equal totals after hand 16 share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [2], results {'seat 1': 10, 'seat 2': 10}, 69-77 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 72.0 decisions, prompts of 137 characters on average (longest 159)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 1': 30, 'seat 2': 29, 'seats 1 and 2': 1}
- always `first@seat1`: won 47, lost 12, drew 1
- always `first@seat2`: won 46, lost 13, drew 1
- always `last@seat1`: won 0, lost 60, drew 0
- always `last@seat2`: won 0, lost 60, drew 0

## Triage (whose problem each failure was)

- round 1: revise_rules: The game file is built correctly and behaves as specified. The flaw is in the design: a mindless 'always pick the first option' policy, presumably always putting and seeing and never folding, wins about 90% of decided matches from either seat against random play. So the betting structure rewards blind aggression and calling, not judgement about the cards.
- round 2: fix_game: The interface says `leader_reply` is empty ('') when there was no leader reply. The game instead writes the placeholder 'none', and earlier 'not chosen yet', into it. The tests correctly expect '' in hands where the leader put, or where both checked.
- round 2: fix_game: The failures differ from attempt to attempt (blank fields, an unfilled placeholder, an attribute nothing updates), and attempt 5 got past the blank-field problem, so these are fixable file mistakes, not a flaw in the rules or the platform. The latest failure is a `full_deck` attribute that no step ever changes.
- round 2: fix_game: The interface defines `leader_reply` as empty ('') when there was no leader reply, but at the start of each hand the game resets it to the text 'none'. The tests correctly expect '' after a hand where the leader put, or where both checked.

## Choices the rules did not make

- Exactly 2 players, suggested 2: The designer fixed the table at 2. The game is a heads-up duel: three tricks between two hands and a Put that one opponent sees or folds to. It has no meaning at another size. The strategy is reading the opponent's lead and answer from trick 1, putting to bluff or value-bet, and folding a weak hand for a 1-point loss rather than risking 4.
- No talk phase: The source says there is no talk phase.
- Cards are stored as numbers 1-13 rather than named ranks: Arithmetic comparison needs numbers; the rank names map one to one (13 = Three, highest, down to 1 = Four, lowest), so nothing is lost.
- Played cards and calls are public attributes: The rules play them face up or announce them.
- The fold scores the fixed 1 point (fold_points), not the stake: The source says the Putter scores 1 point when the other folds.

## Simplifications

- Steps that apply only in some situations (reply, fold scoring, tricks 2 and 3, reveal, hand scoring) are single steps, each carrying its own arithmetic condition: The step list is flat. Each skipped step depends on one simple condition (folded, or exactly one Put), so no block of steps has to be chosen instead of another.

## Encoding attempts

- 1: it plays, but part of it does nothing: game attribute `full_deck` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `card_values` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 2: passed
