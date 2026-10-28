# put: needs review

Built from the variation **Put: Show One, Keep Three** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- The betting becomes a sequence with a re-raise. The caller, who alternates each hand, says PUT or PASS. The responder answers a PUT with SEE, FOLD or RE-PUT, and answers a PASS with PUT or PASS. The caller then answers a RE-PUT, or a PUT made after their PASS, with SEE or FOLD. (fixes: P1): A blind putter can now be re-put by a strong hand and must then fold, costing 2, or see at stake 4. Calls are made in order, so they can be read and bluffed.
- The stakes are rescaled: 1 if nobody puts, 2 if a PUT is seen, 4 if a RE-PUT is seen. A fold to a PUT pays the putter 1, and a fold to a RE-PUT pays the re-putter 2. (fixes: P1): The ladder rewards value-raising strong hands against a player who never folds, and makes well-timed bluffs and folds worth real points. Against always-PUT, folding the bottom ~37% of hands and re-putting the rest yields about +0.56 per hand.
- Each player is dealt 4 cards. The 4th is face up, visible to both, and the other 3 are private. A player plays only 3 of the 4 cards and chooses which to leave out. (fixes: P3, P4, P2): The public card gives each player something to infer the opponent's strength and calls from. Choosing which card to drop, and in what order to play the others, against a known opponent card adds decisions to the card play. Every bet is judged against visible information.
- Card play becomes a single simultaneous secret submission of an ordered list of 3 cards. Trick 1 is the first card of each list, and so on. (fixes: P4): This keeps the original's free play of any card while fitting the 4-choice limit next to three betting steps. Ordering against a known face-up card is a guessing game in which reading the opponent pays.
- The match lasts 40 hands instead of 24, with the caller alternating so each player calls 20 times. (fixes: P5, P2): Estimated edge against always-PUT is about +22 points against a spread of about 20 over 40 hands, which puts the thoughtless policy near or below a 13% win rate. The reasoner-vs-reasoner edges from reading and bluffing also accumulate.
- The original rule is restored that a hand is scored only by a player who wins at least 2 of the 3 tricks. Trick-and-tie, or one trick each with a tie, scores nothing. (fixes: P2, P4): This is faithful to the original and makes the choice of order matter. A weaker hand that forces ties can neutralise a big stake.

Objective: After 40 hands, the player with more points wins. If points are equal, the player with more hands won wins. A hand is won by scoring it on tricks or by the opponent folding. If both are equal, the match is a draw.

## The critic (3 review(s) before the rules went to a coder)

- balanced: pass. Seats: there are 40 hands, with A calling in the 20 odd hands and B calling in the 20 even hands. The Responder acts after seeing the Caller's call, but each seat holds that position 20 times. Deals are symmetric, so neither seat has a structural edge.

Decision table. Let w and l be a player's esti
- playable: pass. Rules completeness:
- Every call sequence leads to a defined stake or fold result: PUT-SEE gives 2, PUT-FOLD gives +1 to the Caller, PUT-REPUT-SEE gives 4, PUT-REPUT-FOLD gives +2 to the Responder, PASS-PASS gives 1, PASS-PUT-SEE gives 2, PASS-PUT-FOLD gives +1 to the Responder.
- Trick comparison, 
- reasoning_over_luck: pass. The deal decides a large share of any single hand. Over 40 hands, skill controls the size of results:
- folding bad hands limits a loss to 1 instead of 2 to 4;
- a re-put with a strong hand extracts 4;
- bluffed PUTs and RE-PUTs win 1 to 2 points without a showdown.
A rough estimate is that chance d

## Complexity

- steps_per_round: designed 17, built 15, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 17, built 54, limit 20 (built: 80)
- hidden_elements: designed 1, built 13, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 40, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: both players start at 0 points and 0 hands won on hand 1, so one PUT/FOLD hand leaves the Caller at exactly 1 and 1
- pass: Hand 1 (odd): seat 1 is Caller, seat 2 Responder; PUT then FOLD scores for seat 1
- pass: Hand 2 (even): seat 2 is Caller, seat 1 Responder; PUT then FOLD scores for seat 2
- pass: Each player is dealt 3 private cards; 8 cards leave the 52-card deck (counts only, the deal is random)
- pass: Caller is offered PUT and PASS first; after PUT the Responder is not offered PUT or PASS
- pass: PUT then SEE goes straight to play: the Caller gets no second question (trick result is random, not asserted)
- pass: PUT then FOLD: the Caller scores 1 point and 1 hand won, with no play
- pass: PUT then RE-PUT: the Caller is offered SEE and FOLD
- pass: PASS then PASS goes straight to play: no SEE/FOLD question for the Caller (result random, not asserted)
- pass: PASS then PUT: the Caller is offered SEE and FOLD
- pass: PUT, RE-PUT, SEE leads to play and the hand completes (stake 4 result is random, not asserted)
- pass: FOLD after RE-PUT: the Responder scores 2 points and 1 hand won
- pass: PASS, PUT, SEE leads to play and the hand completes (result random, not asserted)
- pass: FOLD after PASS then PUT: the Responder scores 1 point and 1 hand won
- pass: Hand 2 with seat 2 as Caller: FOLD after PASS then PUT gives seat 1 (the Responder) 1 point
- pass: When play happens, the hand is played out and the match moves on (cards random; only the hand number is asserted)
- pass: After hand 40 the match ends: equal points, more hands won wins
- pass: After hand 40 the match ends: more points wins despite fewer hands won
- pass: After hand 40 the match ends: equal points and hands won is a shared draw
- pass: Hand 40 is the last: the match ends after it with the scores from that hand

## Does the file follow the spec's shape? (flags for a person)

- rule R1 has no scenario: nothing checks it
- rule R16 has no scenario: nothing checks it
- rule R17 has no scenario: nothing checks it
- rule R18 has no scenario: nothing checks it
- rule R19 has no scenario: nothing checks it

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [2], results {'seat 2': 8, 'seat 1': 12}, 137-157 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 143.3 decisions, prompts of 353 characters on average (longest 425)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- always taking the first option as seat 1 wins 90% of decided matches against random seats
- always taking the first option as seat 2 wins 88% of decided matches against random seats
- random seats: {'seat 2': 33, 'seat 1': 27}
- always `first@seat1`: won 54, lost 6, drew 0
- always `first@seat2`: won 53, lost 7, drew 0
- always `last@seat1`: won 25, lost 35, drew 0
- always `last@seat2`: won 34, lost 26, drew 0

## Triage (whose problem each failure was)

- round 1: revise_rules: The game file is built correctly and behaves as specified. The flaw is in the design: a mindless 'always pick the first option' policy, presumably always putting and seeing and never folding, wins about 90% of decided matches from either seat against random play. So the betting structure rewards blind aggression and calling, not judgement about the cards.

## Choices the rules did not make

- Exactly 2 players (suggested 2): The designer fixed the game at 2. The call structure (Caller/Responder alternating by hand) and the head-to-head tricks only work with two seats.
- Card coding as strength*10+suit: Strength is then floor(card/10), which makes trick comparison pure arithmetic while keeping 52 distinct cards.
- Play offered as one choice among 24 ordered triples: This makes the simultaneous secret ordered list a single poll with only legal options (3 different cards from own 4).
- No free-text talk step: The rules contain no talk. With two players the calls themselves are the signalling and bluffing channel.
- Strategy check: A thoughtful player weighs the opponent's visible face-up card against their own, bluffs PUT or RE-PUT with weak hands, folds cheaply when outmatched, and orders cards to dodge the opponent's likely ordering (e.g. sacrificing a weak card against a strong one).
- rank_by weight 1000: Hands won is at most 40, so points*1000 + hands_won ranks by points first, then by hands won.

## Simplifications

- The Caller and Responder are worked out from hand_number parity in each step's 'who': The engine has no role-swap action; parity gives the same alternation.
- Conditional steps 4 and 5–7 are written as individual steps with when-conditions on caller_call, responder_answer and folded: The step list is flat, and per-step conditions reproduce the branching of the hand faithfully.
- Trick comparison between the two players' play lists uses a table-side comparison: Comparing one player's attribute with another's needs the documented workaround of copying values to the table.

## Encoding attempts

- 1: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (caller_answer, caller_call, responder_answer) in `your_cards`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 2: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (caller_answer, caller_call, responder_answer) in `your_cards`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 3: it plays, but part of it does nothing: game attribute `full_deck` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 4: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (caller_answer, caller_call, responder_answer) in `your_cards`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 5: passed
