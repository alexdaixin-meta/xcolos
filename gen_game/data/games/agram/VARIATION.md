# Variation: Agram Match

3-4 player trimmed-deck trick game; each of 6 hands plays 6 must-follow tricks and the winner of trick 6 scores the hand; most hands wins the match.

Players: 3 to 4, best with 4

## Review of the original

Agram is a trick-taking game on a trimmed 35-card deck where each player gets 6 cards, must follow the led suit if able, highest of the led suit wins the trick and leads next, and whoever wins the sixth trick wins outright.

- **non_degenerate**: good. No simple policy is unbeatable: always play highest legal empties aces/spade-10 early and loses the trick-5 lead fight; always play lowest never seizes trick-5 lead to force its boss on trick 6; leader and dealer rotate each hand so no seat keeps the trick-1 lead edge.
- **skill_sensitive**: good. Over 6 hands (36 tricks) counting played highs, conserving a boss in a forceable suit, voiding cheaply, and fighting for trick-5 lead beats random and thoughtless opposites reliably; single-hand luck is averaged out while stub (17 cards at 3p, 11 at 4p) keeps hidden variance.
- **headroom**: good. 36 sequential decisions per match with shrinking hands, lead control, and void reading; not solved, weak players can still steal a hand with a dealt boss, strong players improve via counting and lead planning.
- **reasoning_dependent**: good. Hands are hidden except as revealed by plays; must infer who is void in what suit, where remaining aces/spade-10 live, and plan a multi-trick sequence to arrive leading on trick 6 with a winner.
- **verifiable**: good. Trick winner is highest rank of led suit by fixed order, hand point is 1 if you won trick 6 else 0, match winner is most points; all arithmetic from tracked plays with no judge.
- **fits_platform**: good. Turn-based text-only sequential_choice with hidden_hands, no board, 36 trick-rounds within 40, at most 4 sequential choices per trick, one shuffle per hand; 3-4 players avoids 5-way turn overflow.

## Problems

- Single-hand lottery: one 6-trick deal decides everything; when everyone saves bosses and fights for lead, dealt aces and leadable suits largely decide trick 6.
- Low headroom and no recovery: six plays only with no comeback from a bad deal.
- Variable 2-5 table: stub size 23/17/11/5 changes hidden information unevenly and 5 sequential choices per trick exceed build limits.
- Under-specified loop: follow-suit enforcement, who leads trick 1, who leads next, dealer rotation, redeal, and tie rule were missing so coder/players had to guess.
- Missing standings and faulty final tally: ending summary dropped the last seat and no per-hand standings were announced despite being promised.
- Noisy private state: hand message showed build constants, deck size as remaining_cards, empty lead_suit and stale trick_winner before any trick, hid match_points, and added meaningless living-seats lines.

## Changes

- Play a match of 6 hands; each hand is a fresh 6-trick Agram deal, winner of trick 6 scores 1 match point, most points after 6 hands wins, tie for most is a draw. (fixes: Single-hand lottery: one 6-trick deal decides everything; when everyone saves bosses and fights for lead, dealt aces and leadable suits largely decide trick 6.): Spreads the single-deal lottery over 6 independent deals and gives recovery and headroom while keeping every hand recognisably Agram.
- Same 6-hand repetition with rotating random-start dealer. (fixes: Low headroom and no recovery: six plays only with no comeback from a bad deal.): 36 tricks instead of 6 gives learning, counting and lead planning room and balances any lead-order edge.
- Fix table to 3-4 players, suggested 4; deal 6 each in two batches of 3; stub 17 cards at 3p and 11 at 4p left face-down untouched for the hand. (fixes: Variable 2-5 table: stub size 23/17/11/5 changes hidden information unevenly and 5 sequential choices per trick exceed build limits.): Keeps hidden information consistent, keeps each trick to at most 4 sequential choices, and removes the uneven 2p duel and 5p overload.
- Write full engine-ready loop in numbers and order: 35-card composition and rank orders, deal order, trick-1 leader left of dealer, must-follow-if-able with off-suit never winning, winner leads next, redeal next hand with next dealer, legal-only offers, and both branches of every decision. (fixes: Under-specified loop: follow-suit enforcement, who leads trick 1, who leads next, dealer rotation, redeal, and tie rule were missing so coder/players had to guess.): Removes all guessing about setup, offers, resolution order, information timing, and success/failure outcomes.
- Require a standings announcement after every hand and a final announcement that loops over all seats 1..num_players listing every seat's match_points; same loop for any mid-match standings line. (fixes: Missing standings and faulty final tally: ending summary dropped the last seat and no per-hand standings were announced despite being promised.): Prevents the dropped-last-seat tally bug and makes running score public as promised.
- Fix message templates: private hand message shows only hand, dealer seat, hand k of 6, and points so far; hide build constants, hide lead_suit and trick_winner until set, drop living-seats lines; public log shows each play, trick winner plus next leader, hand winner, and standings. (fixes: Noisy private state: hand message showed build constants, deck size as remaining_cards, empty lead_suit and stale trick_winner before any trick, hid match_points, and added meaningless living-seats lines.): Removes misleading raw-state dumps and stale defaults and surfaces decision-relevant public state.

## Kept from the original

- Trimmed 35-card deck and ranks: hearts/diamonds/clubs A-10-9-8-7-6-5-4-3, spades 10-9-8-7-6-5-4-3 with 10 high, no K/Q/J/deuces and no ace of spades.
- Six cards per player dealt three at a time.
- Must follow led suit if able, otherwise any discard, and off-suit never wins the trick.
- Highest rank of led suit wins the trick and leads the next trick.
- Six tricks per deal with winner of sixth trick winning that deal outright.
- Clockwise sequential turns with no board, map or movement.

## The variation's rules

Deck: 35 cards. Hearts 9: A,10,9,8,7,6,5,4,3. Diamonds 9: same. Clubs 9: same. Spades 8: 10,9,8,7,6,5,4,3. No kings, queens, jacks, deuces, and no ace of spades. Rank high to low in hearts/diamonds/clubs is A then 10-9-8-7-6-5-4-3; in spades 10 then 9-8-7-6-5-4-3. Suits are unranked; only the led suit matters. Match: 6 hands. Initial state: every seat match_points 0, hand number 0, no cards dealt. Dealer for hand 1 is chosen uniformly at random; dealer rotates one seat clockwise each later hand. Each hand in order: 1) Shuffle the 35 cards. 2) Deal 6 cards to each player face-down, in two batches: clockwise from left of dealer, 3 cards to each, then 3 cards to each again. Remaining stub (17 cards at 3 players, 11 at 4 players) is left face-down, never viewed, and takes no part in the hand. 3) Play 6 tricks. Trick 1 leader is the player left of the dealer. For each trick in order: a) Leader is offered all cards remaining in their hand and must play exactly one face-up. That suit becomes the led suit for this trick. b) Clockwise, each follower in turn is offered a restricted choice: if they hold at least one card of the led suit they are offered only those led-suit cards and must play one of them (following is enforced, illegal off-suit play is never offered); if they hold none of the led suit they are offered all cards remaining in their hand and must play one (any discard). c) Resolution: the highest rank of the led suit among cards played wins the trick; off-suit cards cannot win even if higher in their own rank. There are no ties because all 35 cards are distinct. The trick cards are removed and hands shrink by one. Announce the trick winner and that they lead the next trick. The trick winner leads any one card to the next trick. Tricks 1-5 score nothing except determining who leads next. 4) Hand scoring: the winner of trick 6 wins the hand outright and gains 1 match_point; every other player gains 0 for the hand. Announce hand winner. 5) Standings: announce every seat's match_points by looping seats 1 to num_players, e.g. 'Points: seat 1 X, seat 2 Y, ...'. Then redeal for the next hand with the next dealer. Information: all card plays are shown to all players as played with seat and card; hands are otherwise hidden and never shown. Private message at the start of each hand uses only this template: 'Your hand: [cards]; dealer seat D; hand k of 6; points so far: seat 1 X, seat 2 Y, ...'. Do not show build constants, deck size, empty lead_suit, stale trick_winner, or living-seats lines; trick_winner and lead_suit are shown only after they are set for the current trick. No discussion messages are used: hands stay hidden so follow/void signals must be read, and with one winner per hand cheap talk would only add noise or give hands away.

Objective: After 6 hands, the player with the most match_points (hand wins, 0-6) wins the match. If two or more players tie for most, the result is a draw. The ending announcement must list every seat 1 to num_players with its points, e.g. 'Final points: seat 1 X, seat 2 Y, seat 3 Z, seat 4 W. Winner seat N' or 'Draw among ...'.

Expected effect: Players disagree because only the trick-6 winner scores the hand, so helping another take trick-5 lead can lose you the hand; no talk is used because hidden voids must be read and proposals would be unenforceable noise. Min 3 is the minimum because with 2 there is no multi-opponent lead race or cross-void reading. Suggested 4 is best because there are enough followers to force real follow-or-void decisions and enough hidden stub cards to require counting, while each lead still matters and turns stay short. Thoughtful play conserves a boss (an ace or spade 10) in a suit it can force, voids a side suit early while losing cheaply, counts remaining highs from revealed plays, and fights for the trick-5 lead to lead its boss into trick 6; thoughtless always-high empties winners early and always-low never seizes the trick-5 lead, so each can lose to the other and to random play. The 6-hand match plus per-hand standings and full-seat final tally remove the single-deal lottery and the dropped-seat bug while keeping every hand recognisably Agram.

## Complexity (the designer's count, against the limits)

- steps_per_round: 7 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 8 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 36 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
