# biblios: needs review

Built from the variation **Scriptorium Lots (Seller's Edition)** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- The current lot is shown privately to the active player only. Everyone else sees just the auction card. The public lot list lets opponents work out that the kept card's value is 5 minus the auction value and that its colour is one of exactly two. They narrow it by tracking which lots are used up. (fixes: P1 Hidden-information contradiction: the lot was revealed publicly, so kept cards could be deduced and the claimed inference did not exist.): This creates real, bounded hidden state that rewards bookkeeping and inference.
- The 'next lot' peek is removed entirely. Each round's own lot is the only thing shown, and only to its active player. (fixes: P2 The 'next lot' peek was undefined in round 12 and confusing in every round.): Nothing is left unspecified in round 12, and there is one clear private view per round.
- There is a single hidden holding per player per colour (9 attributes). Cards gained in auctions are announced in the public log rather than stored separately. The total is 19 attributes. (fixes: P3 Separate hidden and public holdings needed 24 attributes, more than the limit of 20.): This stays under 20, and the public cards remain knowable from the log.
- Announcing bids is merged into resolve, and the active player is excluded from bidding. The round is 15 steps. (fixes: P4 The step budget sat exactly at 20, with no slack for the multi-operation resolve and the bounded worth shift.): This leaves 5 steps of slack.
- The active player is the seller: the winning bid is paid to the active player, not removed. Remaining gold counts at the end, at 1 VP per full 4 gold. (fixes: P5 Deal luck: which lots a player was active on decided their high kept cards. Nothing let a player convert a bad lot into value.): A lot in an unwanted colour can be sold dear for gold that becomes VP. Choosing whether to keep the 4 or sell it becomes a real decision, and bad deals can be overcome by play.
- Equal bids, including 0-0, give the auction card to the seller for free. (fixes: P6 Thin trade-offs: gold paid simply vanished, so selling a valuable card never paid. Ties discarded the card, so passive zero bidding carried no risk.): Passive bidding now hands the seller a full lot, so 'always bid 0' can lose. Bidders must actually contest.
- Only the two non-active players bid, and they bid simultaneously. (fixes: P6 Thin trade-offs: gold paid simply vanished, so selling a valuable card never paid. Ties discarded the card, so passive zero bidding carried no risk.): This creates a direct duel between two rivals, with the seller profiting from their competition.

Objective: The player with the most VP wins. If players tie on VP, the tied player with more remaining gold wins. If still tied, the game is a draw.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. TOTALS. Each card appears in exactly two lots, so every colour carries 2x(1+2+3+4) = 20 card points. All 60 points enter play.

GOLD. The 36 gold is conserved. Gold VP is floor(g/4), so the starting 12 gold is worth 3 VP and a full 36 would be worth 9. Colour VP is the sum of three worths, each betw
- playable: pass. RULES COMPLETE.
- Bids are capped at gold held, so payment is always possible.
- Ties, including 0-0, are resolved.
- Shift limits of 1-5 are clamped.
- The all-zero colour case is explicitly excluded from the half-worth split.
- The VP tie-break uses gold, and draws are allowed.
- The game is finit
- reasoning_over_luck: pass. CHANCE. The only randomness is the setup order of the lots, which decides which seat sees which lots.

VARIANCE. The values a seat can keep range from four (2,3) lots, keeping 12, to four (1,4) lots, keeping 16. That is a 4-point swing out of about 60. Colour concentration and auction outcomes matte

## Complexity

- steps_per_round: designed 15, built 13, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 19, built 40, limit 20 (built: 80)
- hidden_elements: designed 2, built 14, limit 3
- random_draws_per_round: designed 0, built -, limit 1
- rounds: designed 12, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: R1: start state is 12 gold each and all worths 3; a 0-0 first round keeps that (lot depends on chance)
- pass: R2: gold changes from a sale are public (seat 3 buys B3 for 6)
- pass: R3: shuffled lots, round 1 with a 0-0 tie leaves gold at 12 and gives the card to seat 1 (lot itself depends on chance)
- pass: R4: in round 2 seat 2 is the seller; seats 1 and 3 bid and seat 2 is not asked to bid
- pass: R4: three tied rounds rotate the seller 1,2,3, so the last recipient is seat 3
- pass: R5: only the active seat is offered the lot's cards
- pass: R6: kept R2 gives the seller the red majority at the end
- pass: R7: keeping B3 puts R2 up for auction, and seat 2 buys it
- pass: R8: a round with the talk poll completes normally (0-0 tie)
- pass: R9: bids range from 0 to the bidder's own gold; the seller is not asked to bid
- pass: R10: bids 5 and 3 for B4 move 5 gold from the winner to the seller
- pass: R11: equal bids of 3 move no gold and the seller takes the auction card
- pass: R12: auction_recipient records the buyer of the latest round (seat 3 in round 2)
- pass: R13: the winning bidder raises Red by 1
- pass: R14: Red +1 with Red already at 5 leaves it at 5
- pass: R14: Green -1 with Green already at 1 leaves it at 1
- pass: R15: after a 2-2 tie nobody is asked to shift a worth
- pass: R16: worths after the round reflect a Blue -1 shift
- pass: R17: the game ends after round 12 (tie, seat 3 keeps both cards)
- pass: R18: the sole Red leader with Red worth 4 gains 4 VP
- pass: R19: two players tied on Red at worth 5 score 2 VP each
- pass: R20: nobody holds Green, so its worth of 4 scores nothing
- pass: R21: gold scores 1 VP per full 4 (15 gives 3, 7 gives 1)
- pass: R22: a VP tie is broken by more gold
- pass: R22: level on VP and gold, two seats share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [3], results {'seat 3': 9, 'seat 2': 6, 'seat 1': 5}, 81-84 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 83.7 decisions, prompts of 246 characters on average (longest 360)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- always taking the first option as seat 2 wins 85% of decided matches against random seats
- random seats: {'seat 3': 34, 'seat 2': 16, 'seat 1': 10}
- always `first@seat1`: won 47, lost 13, drew 0
- always `first@seat2`: won 51, lost 9, drew 0
- always `last@seat1`: won 5, lost 55, drew 0
- always `last@seat2`: won 6, lost 54, drew 0

## Triage (whose problem each failure was)

- round 1: fix_game: The rules are buildable on this platform. The attempts fail on two file-level bookkeeping problems, and the coder keeps fixing one while bringing back the other: talk/auction_colour fields shown blank, and a static `lot_list` attribute that no step ever changes.
- round 1: fix_tests: The failing test checks the length of `lot_list`. That attribute is not in the interface: it is the coder's own scratch value, emptied while shuffling the lots into `lots`, which holds the 11 lots not yet used after round 1 was dealt. Everything the interface does define came out as the rules say: seat 1 kept B1, G4 went to auction, both bids were 0, the auction card went back to seat 1, all gold stayed at 12 and the worths stayed at 3.
- round 1: revise_rules: The game behaves as specified, yet a thoughtless policy dominates. Always taking the first option (keep the first card, bid 0) wins about 80-85% of matches, and always taking the last option (bid all your gold) almost always loses. Bidding is a losing proposition: the winner's gold goes straight to a rival, gold converts directly to VP, and tied or zero bids hand the card to the seller for free.

## Choices the rules did not make

- Exactly 3 players, suggested 3: The designer fixed 3: one seller and two rival bidders each round. The lot deduction and rotation (4 turns each) are built for 3 seats, so the minimum and maximum are both 3.
- Keep the simultaneous talk poll before bidding: The rules require it. Players disagree (the seller wants high bids, and bidders want cheap cards and to hide their colours), so bluffing about the kept card or about worth plans gives the others something to reason about.
- Ranking expression vp*1000 + gold: Total gold never exceeds 36, so a factor of 1000 puts VP first and gold as the tie-break. Remaining exact ties share the win, which is the engine's form of a draw.
- The shift question is always offered as all 7 options: The rules say a change past the limits simply has no effect, so the options do not need to depend on the current worths.
- A strategy exists: Thoughtful players track used lots to infer the seller's kept colour, bid by how much a card swings a majority, use worth shifts to raise colours they lead and sink rivals', and bluff in talk.

## Simplifications

- Bids are stored as a private attribute and announced in the resolve update: The engine's poll keeps answers hidden until all are in; the announcement then reveals both bids as the rules require.
- End scoring is a single update step that runs when round > 12, before the ending check: The engine's ending ranks by one expression, so the colour majorities are computed into vp first.
