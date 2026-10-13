# Variation: Agram Match

A 3-4 player last-trick trick-taker played as a 6-hand match; each hand is six tricks of must-follow trick play and the winner of trick 6 banks the hand.

Players: 3 to 4, best with 4

## Review of the original

Agram is a last-trick-wins trick-taker: from a 35-card trimmed deck each player gets six cards, must follow suit, highest of led suit wins the trick and leads next, and whoever wins the sixth trick wins outright.

- **non_degenerate**: good. No simple policy dominates: always playing the highest legal card wins early tricks but empties the hand for trick 6; always playing the lowest legal card saves winners but cedes control of who leads tricks 5-6. Seat has only a small lead edge and choices change who leads the final trick.
- **skill_sensitive**: bad. One hand of six tricks is decided largely by the deal: e.g. a hand with two aces plus lead control wins trick 6 against random play far more often, while a 6-low hand loses almost always. A better player cannot reliably beat a worse one in one hand; variance swamps decisions.
- **headroom**: weak. One hand gives a weak player about 1/n win chance by luck and gives a strong player no room to recover from a bad deal. There is inference and lead planning, but only six plays before the game ends, so improvement across play is truncated.
- **reasoning_dependent**: good. Hands are hidden, the stub is unseen, and discards reveal voids and remaining highs. Winning requires inferring who holds the bosses in each suit, planning which suits to void early, and planning lead control into tricks 5-6 over several rounds.
- **verifiable**: good. Winner follows by arithmetic: highest card of led suit wins each trick, lead passes to that winner, winner of trick 6 wins. No judge is needed.
- **fits_platform**: weak. Turn-based and text-only in principle with hidden hands and sequential choice, but as filed it is incomplete for the engine: 2-5 players changes steps per trick, undealt stub size changes, follow-suit enforcement, dealer/lead rotation and tie/match end are unstated, and a single 6-trick game is too short to score reliably.

## Problems

- Lottery trap in one hand: when everyone plays the intended save-bosses and control-lead strategy, who was dealt aces and a leadable suit largely decides who wins trick 6.
- Single-hand scoring gives high luck-to-skill ratio and little headroom: six plays only, no recovery from a bad deal.
- Variable 2-5 table: 5-player tricks need 5 sequential choices, exceeding build limits, and stub size 23/17/11/5 changes hidden information unevenly.
- Under-specified for build: follow-suit enforcement, lead and dealer rotation, redeal, and match winner rule are missing.

## Changes

- Play a match of 6 hands of 6 tricks each from a fresh trimmed deck each hand; each hand win is 1 point for winning trick 6; most points after 6 hands wins, tie is a draw. (fixes: Lottery trap in one hand: when everyone plays the intended save-bosses and control-lead strategy, who was dealt aces and a leadable suit largely decides who wins trick 6.): Aggregating over different deals lets good conservation, voiding and lead-counting overcome any single bad deal while keeping last-trick-wins as the objective.
- Same match scoring over 6 hands instead of one hand. (fixes: Single-hand scoring gives high luck-to-skill ratio and little headroom: six plays only, no recovery from a bad deal.): Weak players still score hands by luck but strong players reliably finish ahead on totals, and there is room to adapt across hands.
- Fix table to 3-4 players, suggested 4; deal 6 each, stub unseen for the hand. (fixes: Variable 2-5 table: 5-player tricks need 5 sequential choices, exceeding build limits, and stub size 23/17/11/5 changes hidden information unevenly.): 3 is the minimum for real lead-rotation and void-versus-follow contention; 4 is the largest that keeps at most 4 choice steps per trick-round. Fixed stub rules stabilize hidden information.
- State full engine-ready loop: 35-card composition and ranks, deal 3-at-a-time, left-of-dealer leads trick 1, must-follow-if-able with off-suit never winning, winner leads next, dealer rotates each hand. (fixes: Under-specified for build: follow-suit enforcement, lead and dealer rotation, redeal, and match winner rule are missing.): Makes the game complete, clear, and buildable with sequential hidden-hand choices and arithmetic trick resolution.

## Kept from the original

- Trimmed 35-card deck and ranks: A-10-9-8-7-6-5-4-3 in hearts/diamonds/clubs, 10-9-8-7-6-5-4-3 in spades with 10 high, no kings/queens/jacks/deuces and no ace of spades.
- Six cards per player dealt three at a time.
- Must follow led suit if able; otherwise any discard, and an off-suit card cannot win the trick.
- Highest card of led suit wins the trick and leads the next trick.
- Six tricks per deal with winner of the sixth trick winning that deal outright.
- Clockwise sequential turn order with no board, map or movement.

## The variation's rules

Deck: standard 52-card deck minus all kings, queens, jacks (12 cards), all deuces (4 cards), and the ace of spades (1 card), leaving 35 cards. Ranks high to low: hearts, diamonds, clubs: A-10-9-8-7-6-5-4-3; spades: 10-9-8-7-6-5-4-3 with 10 highest. Suits are not ranked; only the led suit matters. Match: 6 hands. Each hand: shuffle the 35 cards, choose a starting dealer at random for hand 1 then rotate dealer clockwise each hand. Dealer deals 6 cards to each player in two rounds of 3 cards each, clockwise from left of dealer. Remaining cards form a face-down stub that is never viewed and takes no part. Tricks: 6 tricks per hand. Player left of dealer leads trick 1 by playing any card face up. Clockwise, each other player in turn must play a card of the led suit if they hold any; if they hold none they may play any card, but an off-suit card cannot win the trick. Highest rank of the led suit wins the trick. The trick winner leads any card to the next trick. Cards are removed after each trick; hands shrink 6 to 0. Hand scoring: the winner of trick 6 wins the hand outright and scores 1 final point; all other players score 0 for the hand. Tricks 1-5 score nothing except determining who leads next. Then redeal for the next hand with the next dealer. All card plays are shown to all players as played; hands are otherwise hidden. No discussion messages are used: hands stay hidden so discards and follow/void signals must be read, and with one winner per hand cheap talk would only add noise or give hands away. Illegal play (not following when able) is not allowed; the choice offered is restricted to legal cards.

Objective: After 6 hands, the player with the most final points (hand wins, 0-6) wins the match. If two or more players tie for most, the result is a draw among all players (engine reports a draw). There is no other scoring.

Expected effect: Min 3 is the minimum because with 2 there is no multi-opponent lead race or cross-void reading; tricks become a simple two-way high-card duel. Suggested 4 is best because there are enough followers to force real follow-or-void decisions, enough hidden cards to require counting, and each lead still matters, while keeping turns short and within 4 choices per trick. Thoughtful play conserves a boss (ace or spade 10) in a suit it can force, voids a side suit early while losing cheaply, counts remaining highs from what was played, and fights for the lead on trick 5 to lead its boss into trick 6; thoughtless always-high empties winners early and always-low never seizes the trick-5 lead, so each can lose to the other and to random play. Repeating 6 hands removes the single-deal lottery while keeping every hand recognisably Agram.

## Complexity (the designer's count, against the limits)

- steps_per_round: 7 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 12 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 36 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
