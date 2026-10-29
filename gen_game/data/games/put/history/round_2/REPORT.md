# put: needs review

Built from the variation **Put: Twelve Hands** (design round 2); see VARIATION.md.

## What was changed from the original, and why

- The putter must win strictly MORE tricks than the opponent to collect a seen Put. If tricks are equal or the opponent wins more, the opponent collects instead. The stake is 3 points, not the whole game. (fixes: Tied hands paid nobody, so a Put that ended level was free for the putter, which made aggression costless.): A seen Put with an average hand now loses slightly on average (equal-trick hands go against the putter), so putting must be backed by strength or by a credible bluff. The 3-point stake keeps a seen Put big without deciding the match.
- A fold gives the putter only 1 point, while a seen Put is worth 3 either way. (fixes: Seeing a Put with a weak hand cost little more than folding, so folding was rarely right and bluff-reading did not matter.): Folding becomes the cheap exit for genuinely weak hands, and seeing a strong Put costs 3. The choice between seeing and folding now depends on reading the opponent's hand.
- Options are listed with the cautious choice first (Check before Put) and See before Fold. A seat's 'always first' line is now 'never put, always see', and 'always last' is 'always put, always fold'. (fixes: Always-aggressive play dominates: the previous variation's 'first option' policy (raise or see) won about 90% of decided matches from either seat.): Each line is now exploitable. 'Never put, always see' loses 3 every time a thoughtful opponent puts with a strong hand. 'Always put, always fold' gets seen by strong hands and folds away 1 point every time the opponent puts. Neither can dominate.
- After betting, both players secretly and simultaneously commit the order in which they will play their three cards. Trick 1 compares the first cards, trick 2 the second, trick 3 the third. (fixes: Three tricks with alternating leads need too many choice steps per round for the engine.): This keeps 'play any card, no need to follow' and the tie rule while fitting into one choice step. Ordering becomes a guessing contest: whether to sacrifice a low card against the opponent's expected high card, or where to place a known strong card.
- The first card dealt to each player is shown face up to both. The other two stay hidden. (fixes: Little information beyond one's own three cards: nothing about the opponent's hand to reason from except the betting.): This gives real information to infer from in both betting and ordering, at no extra choice cost. Players can judge how credible a Put is and plan around a known card.
- The match is exactly 12 hands, with the leader alternating so each seat leads 6. The higher total wins, and equal totals are a draw. (fixes: Open-ended match length ('first to 5 or 7') does not fit a fixed, short game and lets one hand end it.): Fixed and short, seat-balanced, and no single hand decides the match. A trailing player must decide when to take risks in the late hands.
- Stakes are capped at 3 per hand instead of the whole game. (fixes: Whole-game stakes on one seen Put turn a match into a single coin flip on the deal.): Over 12 hands, the betting and ordering decisions accumulate. A single lucky deal can no longer end the match.

Objective: After hand 12, the player with the higher total score wins. If the totals are equal, the match is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. PUT DECISION. Let p be the putter's chance of winning strictly more tricks if seen. A tie goes to the opponent. Net result to the putter: Fold gives +1. See gives +3 with chance p and -3 with chance 1-p, so 6p-3. The responder should see when 6p-3 < 1, that is when p < 2/3, and fold when p > 2/3. A 
- playable: pass. Every branch is defined:
- Put then See or Fold.
- Check then Check or Put.
- Check, Put, then See or Fold by the leader.
The fold result is defined, card ordering happens only if nobody folded (one step with a `when` condition), and scoring is defined for both checks, for a seen put, and for tie tr
- reasoning_over_luck: pass. The deal matters a lot within a hand: 3-card strength sets p. However, the fold option caps the loss on a bad hand at 1 instead of 3. Value puts need p > 2/3 to be seen profitably. Bluffs exploit fold rates, and the opponent can infer hand strength from the face-up card and the betting line.

The si

## Complexity

- steps_per_round: designed 14, built 14, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 15, built 32, limit 20 (built: 80)
- hidden_elements: designed 1, built 9, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 12, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: both scores start at 0 and no hand has been played
- pass: Match lasts exactly 12 hands: every hand the leader puts and the responder folds, 6-6 draw
- pass: Hand 1 is odd so seat 1 leads
- pass: Hand 2 is even so seat 2 leads
- pass: After the deal each player holds 3 cards and the deck holds 46
- pass: Each player is dealt three cards, the first of which is the face-up card (values are chance, only counts asserted)
- pass: Leader is offered Check and Put and checks
- FAIL: Leader puts, responder is offered See and Fold and sees | rule R7 is broken: When the leader puts, the responder chooses See or Fold.; game leader_reply: expected '', got 'none'
- pass: Leader checks, responder is offered Check and Put and puts
- pass: Leader checked, responder put: leader is offered See or Fold and folds, putter scores 1
- pass: Responder facing the leader's Put is not offered Put
- pass: A fold gives the putter 1 point, the folder 0, and no cards are played
- pass: With no fold both seats are offered the six card orders
- pass: Card ranks decide tricks (dealt cards are chance: only that cards are played is asserted)
- pass: Three tricks are played when nobody folds (trick winners are chance, not asserted)
- FAIL: Both check: an unput hand with no fold (point winner is chance, not asserted) | rule R14 is broken: When both players checked, the player with more tricks scores 1 point, and equal tricks score nothing.; game leader_reply: expected '', got 'none'
- pass: Leader's Put is seen and the hand is played out (who gets the 3 points is chance, not asserted)
- pass: Responder's Put is seen by the leader and the hand is played out (scoring is chance, not asserted)
- pass: End of hand reveal: public results stay visible after a fold
- pass: After hand 12 the higher score wins
- pass: After hand 12 equal totals are a shared win
- pass: Full match: seat 1 always puts and seat 2 always checks then folds, so seat 1 wins 12-0

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [2], results {'seat 2': 9, 'seat 1': 9, 'seats 1 and 2': 2}, 38-46 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 42.7 decisions, prompts of 142 characters on average (longest 178)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 2': 28, 'seat 1': 25, 'seats 1 and 2': 7}
- always `first@seat1`: won 35, lost 23, drew 2
- always `first@seat2`: won 29, lost 27, drew 4
- always `last@seat1`: won 27, lost 27, drew 6
- always `last@seat2`: won 31, lost 20, drew 9

## Triage (whose problem each failure was)

- round 1: revise_rules: The game file is built correctly and behaves as specified. The flaw is in the design: a mindless 'always pick the first option' policy, presumably always putting and seeing and never folding, wins about 90% of decided matches from either seat against random play. So the betting structure rewards blind aggression and calling, not judgement about the cards.
- round 2: fix_game: The interface says `leader_reply` is empty ('') when there was no leader reply. The game instead writes the placeholder 'none', and earlier 'not chosen yet', into it. The tests correctly expect '' in hands where the leader put, or where both checked.
- round 2: fix_game: The failures differ from attempt to attempt (blank fields, an unfilled placeholder, an attribute nothing updates), and attempt 5 got past the blank-field problem, so these are fixable file mistakes, not a flaw in the rules or the platform. The latest failure is a `full_deck` attribute that no step ever changes.
- round 2: fix_game: The interface defines `leader_reply` as empty ('') when there was no leader reply, but at the start of each hand the game resets it to the text 'none'. The tests correctly expect '' after a hand where the leader put, or where both checked.

## Choices the rules did not make

- Exactly 2 players: The designer fixed the game at 2. It is a heads-up bluffing duel, and the leader/responder structure is built for two seats.
- Ranks stored as numbers 1 (for 4) to 13 (for 3): Tricks are then decided by a plain numeric comparison.
- Card order answered as a permutation of dealt positions: This gives a fixed choice list that names the player's own cards unambiguously.
- No talk step: The rules say talk is not part of the game.
- Strategy at the table: A good player reads the opponent's face-up card, bluffs or value-puts with their hidden cards, and chooses a card order that anticipates the opponent's ordering.

## Simplifications

- none

## Encoding attempts

- 1: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state a player is shown has empty fields (order_choice, leader_call, leader_reply, responder_action); hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 2: passed
