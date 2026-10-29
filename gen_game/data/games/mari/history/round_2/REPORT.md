# mari: needs review

Built from the variation **Malý Mariáš (Little Mariáš)** (design round 2); see VARIATION.md.

## What was changed from the original, and why

- Shrink the deck to 12 cards: four suits (Hearts, Bells, Leaves, Acorns) times three ranks (A, 10, K). Deal 4 cards each with no talon, for 4 tricks per deal. Drop marriages and the special contracts. Card values stay A=10 and 10=10, and the last trick stays 10, so the total is still 90. (fixes: P1): This keeps the 90-point economy, the trump choice and follow/trump play, while one trick fits in one round with at most 4 choice steps.
- At the start of each deal, build a fresh list of the 12 card codes 0 to 11 and shuffle it once. Seat 1 takes positions 1-4, seat 2 positions 5-8, seat 3 positions 9-12. There are no index draws from a shrinking deck. (fixes: P2): A fixed-size permutation sliced at fixed positions cannot run out, and it is the round's only random draw.
- Track the trick winner with a running best_key and best_seat. The leader's card sets them. Each later card replaces them only if its key is strictly greater. The key is rank (K=0, 10=1, A=2), plus 10 if trump, plus 5 if of the led suit. (fixes: P3): No list search is needed, so nothing can come back empty.
- Use plain follow-suit: follow the led suit if able, otherwise trump if able, otherwise any card. An illegal or unheld card is replaced by the lowest-code legal card. A hand always has a card when its owner plays. (fixes: P4): Each play is one validated step, and the played card always exists and always enters the trick.
- Prompts contain no placeholders except {seat} and {value}. Each player's own hand is shown through their private hand attribute in their state view. (fixes: P5): Players never see unfilled braces.
- Hide the bookkeeping attributes (best_key, led_suit, deck, the bid's raw fields). Show only hand, score, trump, declarer, contract, multiplier, cards in the current trick, trick number and the points taken so far. (fixes: P6): The state view holds only usable information.
- Play 9 deals, with the eldest hand rotating 1, 2, 3, 1, ... so each seat is eldest exactly 3 times. The eldest cannot pass: an invalid entry or PASS from the eldest counts as '50 A'. Bid ties go to the player nearest the eldest in seat order. (fixes: P7): This preserves Mariáš's forced forehand while spreading that burden and privilege evenly.
- Make flek and re one simultaneous poll after trick 1. Each defender says FLEK or NO, and the declarer says RE or NO at the same moment. Any flek doubles the stake. RE doubles it again only if at least one flek was given. (fixes: P8): One choice step replaces a sequential chain, and the declarer must predict whether the defenders will flek.

Objective: After 9 deals, the player with the highest score wins. If two or three players tie for highest, those players draw. Scores are the sum of the zero-sum deal settlements in step 13.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. Deal settlement table (s = base stake x multiplier x 2 if trump is Hearts): declarer makes the contract: declarer +2s, each defender -s. Declarer fails: declarer -2s, each defender +s. Every deal sums to zero. Base stake is 1/2/3/4/5 for bids 50/60/70/80/90, the multiplier is 1, 2 or 4, so s ranges 
- playable: pass. Rules coverage: every situation is defined.
- Invalid bids default: the eldest to '50 A', others to PASS.
- Bid ties break in seat order from the eldest.
- Illegal or unheld cards are replaced by a fixed rule: led suit first, then trump, then any card, lowest code.
- Follow-suit and must-trump are e
- reasoning_over_luck: pass. The deal is random and matters. My estimate is that roughly 40-50% of the per-deal outcome comes from hand quality. Over 9 deals, though, the result turns on decisions:
- whether and how high to bid, with a secret simultaneous bid against unknown hands;
- the trump choice, where Hearts doubles stake

## Complexity

- steps_per_round: designed 14, built 18, limit 20
- choice_steps_per_round: designed 4, built 5, limit 4
- attributes: designed 18, built 70, limit 20 (built: 80)
- hidden_elements: designed 2, built 20, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 36, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Rank order A > 10 > K within a suit: the Ace played third wins the trick
- pass: Ace and Ten count 10 each, King 0: declarer reaches exactly 80
- pass: Last trick bonus of 10 makes the declarer reach the contract exactly
- pass: After trick 4 the next deal starts and seat 2 is eldest (no PASS for seat 2)
- pass: A new deal resets the multiplier to 1
- pass: Bid options: non-eldest seats may PASS or bid any of the 20 bids
- pass: The eldest is not offered PASS
- pass: Highest bid wins: 70 L beats 60 B, the third seat passes
- pass: Tie between seats 2 and 3 goes to seat 2 (first after the eldest)
- pass: Tie involving the eldest goes to the eldest
- pass: With seat 2 eldest, a tie between seats 1 and 3 goes to seat 3
- pass: A 90 bid sets contract 90 with the declarer's trump
- pass: Bid resolution publishes the declarer, contract and trump
- pass: Flek poll: declarer offered RE/NO, defenders FLEK/NO
- pass: One defender FLEK doubles the multiplier to 2
- pass: FLEK plus RE makes the multiplier 4
- pass: Both defenders FLEK and declarer RE still give multiplier 4
- pass: RE without any FLEK leaves the multiplier at 1
- pass: Led King of Hearts beats off-suit Aces (led-suit bonus)
- pass: A follower void in the led suit must trump rather than discard
- pass: A follower holding the led suit must follow and may not trump
- pass: A trump King beats the led Ace
- pass: A trick won by a defender goes to the defenders, so the declarer falls short
- pass: Stake = base 3 x multiplier 4 x 2 for Hearts = 24
- pass: A made contract: declarer +2 x stake, each defender -stake
- pass: A failed contract (70 < 80): declarer -2 x stake, each defender +stake
- pass: Match ends after deal 9 and the highest score wins
- pass: Players tied at the top after deal 9 share the win

## Does the file follow the spec's shape? (flags for a person)

- rule R8 has no scenario: nothing checks it
- rule R16 has no scenario: nothing checks it
- rule R19 has no scenario: nothing checks it

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [3], results {'seat 2': 7, 'seat 3': 8, 'seat 1': 4, 'seats 1 and 3': 1}, 94-114 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 162.0 decisions, prompts of 195 characters on average (longest 331)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- always taking the first option as seat 1 wins 93% of decided matches against random seats
- always taking the first option as seat 2 wins 98% of decided matches against random seats
- random seats: {'seat 2': 19, 'seat 3': 20, 'seat 1': 19, 'seats 1 and 3': 1, 'seats 2 and 3': 1}
- always `first@seat1`: won 55, lost 4, drew 1
- always `first@seat2`: won 57, lost 1, drew 2
- always `last@seat1`: won 0, lost 60, drew 0
- always `last@seat2`: won 1, lost 58, drew 1

## Triage (whose problem each failure was)

- round 1: fix_game: The tests match the rules: a trump beats the Ace of the led suit, a player void in the led suit must trump and overtrump, and a player with neither may play any card. The game breaks all of these, which points to faulty trump handling in the file, not to a test or rule problem. The game also credits too many points to declarer_points in the trump-marriage scenario.
- round 1: fix_game: Several independent trick-play scenarios fail in the same way: the trick points go to the wrong side, a trump does not beat a led-suit Ace, the trick winner does not lead next, and a seat is offered a card the follow and overtrump rules forbid. The tests match the written rules, so the game file's legal-card filtering, trick-winner calculation and point crediting are wrong.
- round 1: revise_rules: Across five attempts the coder fixed each reported problem, yet the match kept crashing in the card-handling core. The trick-winner calculation failed twice (attempts 3 and 5) and the deck draw once, which points to legality, fallback and trick bookkeeping too intricate to build reliably on a flat step list. The repeated failures, rather than one fixable slip, suggest the design itself should be simplified.
- round 2: fix_game: The rules are sound and the tests read them correctly. The game never offered the flek poll options, so each player's `offer` list stayed empty, every answer defaulted to NO and the multiplier stayed at 1. Per-seat options in a simultaneous poll are within the platform's capabilities, so this is an implementation error.
- round 2: revise_rules: The game was built as specified, and evaluation shows two design flaws. Each round has five choice steps (bid, flek poll, three cards), over the limit of four. A thoughtless first-option policy, which most likely amounts to always passing and never fleking, wins about 95% of matches, while the last option (always bidding the highest contract) almost always loses. Bidding as designed punishes declaring far more than it rewards it.

## Choices the rules did not make

- 3 players (min = max = suggested = 3): The designer fixed 3. The game is built on one declarer against two defenders, and the 12-card deck deals exactly 4 to each of 3 seats.
- No talk step: The rules say there is no discussion phase. Strategy lies in bidding to hand strength, choosing trump, fleking against overbids and card play.
- Bid tie-break computed as bid_value*10 + (3 - ((seat - eldest) mod 3)): This is an arithmetic form of 'first in seat order starting from the eldest'.
- Bids, flek answers and the trick list are reset in the advance step: The source leaves the moment of resetting these working values unstated.

## Simplifications

- Players are offered only legal options (no PASS for the eldest, only legal cards to follow): A seat is never offered what it may not do. The source's fallback rules for invalid or illegal answers are kept in the effects anyway.
- Steps for trick 1, trick 2 and trick 4 are single steps with a 'when trick = k' condition: The step list is flat, and each conditional part is a single step, so no block branching is needed.

## Encoding attempts

- 1: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (bid, bids_shown, card_name, deal_outcome) in `your_hand`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 2: it plays, but part of it does nothing: game attribute `all_codes` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `card_names` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `suit_names` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `seat_labels` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 3: passed
