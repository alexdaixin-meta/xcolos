# Variation: Cat in the Sack: Two Peeks

3-5 players each secretly add a card to a sack every round. After the first card is shown, everyone bids at once, and passers take 2 mice. If two or more bid, a second card is shown and those still in bid again, with stage-2 passers taking 3 mice. The winner pays and takes the cats, and dogs may remove one cat. After 9 rounds, cats plus mice decide the winner.

Players: 3 to 5, best with 4

## Review of the original

Felicity the Cat in the Sack is a 3-5 player bluffing auction. Each player secretly adds one card to a face-down 'sack' each round. The sack is revealed card by card while players bid open-outcry, and passing earns escalating mice. Dogs remove one cat if exactly one dog is in the sack. After 9 rounds, cat points plus remaining mice decide the winner.

- **non_degenerate**: good. Always-pass collects only small mouse cards and gives its own good cats to others. Always-bid-high goes broke and buys negative sacks. Seat order rotates to the sack winner. No simple policy dominates.
- **skill_sensitive**: good. All hands are dealt from the same 10-card set and only one card per hand is set aside, so luck is small. Reading which cards opponents still hold, choosing which card to sacrifice, and pricing a partly revealed sack decide the result.
- **headroom**: good. Novices can still score by passing for mice and buying cheap positive sacks. Experts can count cards, bluff with their own contribution and time when to bid.
- **reasoning_dependent**: good. The hidden sack contents, the hidden hands and the unseen set-aside cards all force inference. Card counting over 9 rounds is a multi-round plan.
- **verifiable**: good. Score is the sum of cat values plus mice. The dog rule is deterministic.
- **fits_platform**: weak. Open-outcry clockwise bidding with a card revealed after each pass is a long, variable chain of turns. The escalating mouse cards depend on pass order. The previous build also failed on poll ranges, pass bonuses, sole-bidder awards and setup overwriting scenario hands.

## Problems

- Open-ended clockwise raising with a reveal after each pass creates an unbounded, order-dependent loop of steps that the flat step list cannot express.
- Escalating mouse cards (2,3,4,6) depend on the order of passing, which disappears once bidding is simultaneous.
- Previous build: the stage-1 poll did not offer every whole number from 0 to the player's own mice.
- Previous build: stage-1 passers did not gain their bonus or leave the auction.
- Previous build: a sole stage-1 bidder was not awarded the sack, so payment, the dog rule, cat points and start seat were never applied.
- Previous build: setup re-dealt full hands over hands supplied by a test scenario, and the sack order from start_seat was not respected.
- If passers are paid even when nobody bids, an all-pass table guarantees everyone free mice and a draw.
- Too many state attributes once every number is kept as a parameter (the limit is 20).
- The original dog rule wording ('lowest negative if no positive') is ambiguous.

## Changes

- Replace open-outcry bidding with exactly two simultaneous sealed stages. Stage 1 bids after the first sack card is shown. Stage 2 bids after the second card is shown, and only players still in may take part. (fixes: Open-ended clockwise raising with a reveal after each pass creates an unbounded, order-dependent loop of steps that the flat step list cannot express.): Gives a bounded, flat step list while keeping 'bid on a partly revealed sack'.
- Fixed pass bonuses: 2 mice for passing in stage 1 and 3 mice for passing in stage 2, both stored as parameters. (fixes: Escalating mouse cards (2,3,4,6) depend on the order of passing, which disappears once bidding is simultaneous.): Keeps the 'passing pays, and later passing pays more' feel without needing a pass order.
- State the stage-1 poll explicitly: a simultaneous poll offering every whole number from 0 up to that player's own current mice, stored in bid. State the stage-2 poll the same way: 0 plus every number from standing_bid+1 up to the player's mice, offered only to players with in_auction=true. (fixes: Previous build: the stage-1 poll did not offer every whole number from 0 to the player's own mice.): Matches what the tests check.
- Bidders are the players with bid > 0. Each stage-1 passer gets in_auction=false and gains stage1_pass_bonus, but only if at least one player bid. (fixes: Previous build: stage-1 passers did not gain their bonus or leave the auction.): Makes passing an explicit, tested step, and stops an all-pass table from farming free mice.
- Add an explicit sole-bidder branch. When exactly one player bid, that player becomes sack_winner at their bid, stage 2 is skipped, and the shared award steps (pay, dog rule, add sack_value, set start_seat) run. (fixes: Previous build: a sole stage-1 bidder was not awarded the sack, so payment, the dog rule, cat points and start seat were never applied.): Ensures the award always happens.
- Deal hands only as normal initial setup, never over supplied state. Build sack_owners as every seat from start_seat upward, wrapping round, and fill sack_cards with each owner's played_card in that order. (fixes: Previous build: setup re-dealt full hands over hands supplied by a test scenario, and the sack order from start_seat was not respected.): Gives a deterministic, testable sack order and lets scenario tests supply hands.
- When nobody bids in stage 1, nobody gains mice, the sack is discarded and start_seat moves to the next seat. (fixes: If passers are paid even when nobody bids, an all-pass table guarantees everyone free mice and a draw.): All-pass now earns nothing, so it cannot coast to a draw. Someone who bids 1 takes the sack and beats it.
- Trim attributes to 20. Reuse bid for both stages. Store the price to pay in standing_bid. Drop the discard pile (clear sack_cards instead). Keep 3 number parameters. (fixes: Too many state attributes once every number is kept as a parameter (the limit is 20).): Fits the complexity limit while keeping every rule number as a parameter.
- Dog rule made exact: with exactly one dog in the sack, the large dog removes the cat with the highest value and the small dog removes the cat with the lowest value. With 0 or 2+ dogs nothing is removed. (fixes: The original dog rule wording ('lowest negative if no positive') is ambiguous.): Gives unambiguous arithmetic.

## Kept from the original

- Identical 10-card hands (cats -8,-5,3,5,8,11,15, rabbit, large dog, small dog) with one random card set aside unseen from each.
- 15 starting mice and 9 rounds, so every hand card is played.
- A face-down sack built from one card per player, revealed partly during bidding.
- Passing pays mice from the bank, and the winner pays the bank.
- The large/small dog removal rule when exactly one dog is present.
- The winner of a sack becomes the next start player.
- Score is cats plus mice, with ties broken by cat points.

## The variation's rules

PARAMETERS (table attributes): starting_mice=15, stage1_pass_bonus=2, stage2_pass_bonus=3. The game lasts 9 rounds.

CARDS: cat_-8, cat_-5, cat_3, cat_5, cat_8, cat_11, cat_15 (each worth its number), rabbit (worth 0), large_dog, small_dog (worth 0; see the dog rule).

ATTRIBUTES.
- Per player: hand (private list), played_card (private until revealed), mice (public), cat_points (public), bid (public after each poll), in_auction (public).
- Table: set_aside (hidden list), start_seat, round_number, sack_owners, sack_cards (hidden), sack_revealed (public), standing_bid, leader_seat, bidder_count, sack_winner, sack_value.

R1 SETUP (normal initial setup only; do not replace any hands, mice or other state a scenario supplies): Each player's hand is the 10 cards above. One card is chosen at random from each hand and moved to set_aside, unseen by everyone, leaving 9 cards per hand.

R2 SETUP: Each player has mice=starting_mice and cat_points=0. round_number=0. start_seat is chosen at random once.

EACH ROUND:

R3 RESET AND PLAY: round_number increases by 1. Every player gets bid=0 and in_auction=true. Set standing_bid=0, leader_seat=0, bidder_count=0, sack_winner=0, sack_value=0, sack_revealed=[]. Then all players simultaneously choose one card from their own hand; it moves to played_card and the hand shrinks by 1.

R4 BUILD THE SACK: sack_owners lists every seat starting at start_seat, ascending and wrapping round (for example, start_seat 3 of 4 gives [3,4,1,2]). sack_cards holds each owner's played_card in that same order.

R5 FIRST PEEK: sack_cards[1] (the start seat's card) is appended to sack_revealed and shown to all.

R6 STAGE 1 POLL: Simultaneously, each player chooses a whole number from 0 up to their own current mice, inclusive. The choice is stored in bid. A bid of 0 is a pass.

R7 COUNT: bidder_count = the number of players with bid > 0. standing_bid = the highest bid. leader_seat = the player with the highest bid; ties go to whichever comes first in sack_owners. Every player with bid=0 gets in_auction=false. If bidder_count is at least 1, every player with bid=0 also gains stage1_pass_bonus mice.

R8 NO BIDDERS (only when bidder_count=0): Nobody gains anything. sack_cards is cleared, and start_seat advances to the next seat (after the last seat comes seat 1). Steps R9 to R14 are skipped this round.

R9 SOLE BIDDER (only when bidder_count=1): sack_winner=leader_seat, and the price is standing_bid (that player's bid). Stage 2 (R10 to R12) does not happen. Go to R13.

R10 SECOND PEEK (only when bidder_count is at least 2): sack_cards[2] is appended to sack_revealed and shown to all.

R11 STAGE 2 POLL (only when bidder_count is at least 2): Simultaneously, each player with in_auction=true chooses 0 or any whole number from standing_bid+1 up to their own current mice. A player with mice at or below standing_bid may only choose 0. The choice replaces bid.

R12 STAGE 2 RESOLUTION (only when bidder_count is at least 2):
- If any in-auction player bid more than 0, sack_winner is the one with the highest bid (ties go to whichever comes first in sack_owners), and standing_bid becomes that bid.
- Otherwise sack_winner=leader_seat, and the price stays at the stage-1 standing_bid.
- Every in-auction player who chose 0 in stage 2 and is not sack_winner gains stage2_pass_bonus mice.

R13 AWARD (whenever there is a sack_winner):
- The sack_winner pays standing_bid mice to the bank.
- Dog rule: if exactly one dog is among sack_cards, the large dog removes the cat with the highest value, or the small dog removes the cat with the lowest value. If there are no cats, nothing is removed. With 0 or 2 dogs, nothing is removed.
- sack_value = the sum of the values of the remaining cats (rabbit and dogs count 0), and is added to the winner's cat_points.
- All sack_cards are then shown and cleared.

R14 NEXT START: start_seat becomes sack_winner.

R15 END: After round 9, each player's score = cat_points + mice.

Objective: The highest score (cat_points + mice) wins. If tied, the higher cat_points wins. If still tied, it is a draw among the tied players.

Expected effect: Every round, players must price a sack they see only one or two cards of. They do this by counting which cards each opponent has already played, guessing what the start player contributed, and deciding whether to sacrifice a negative cat or dog into a sack they expect to lose. Passing is a real alternative, but it only pays when someone else bids, and it gives away your own card. Always-pass ends near 33 and loses to anyone who buys a few good sacks cheaply. Always-bid-max goes broke in round 1 and can be stuck with negative cats. Talk is left out: every claim about your own card would be unverifiable, and the hidden-card bluff already happens through what you play and bid. That keeps the build small.

## Complexity (the designer's count, against the limits)

- steps_per_round: 18 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 20 (limit 20)
- hidden_elements: 3 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 9 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
