# felicity_the_cat_in_the_sack: needs review

Built from the variation **Cat in the Sack: Two-Stage Auction** (design round 2); see VARIATION.md.

## What was changed from the original, and why

- The auction becomes exactly two simultaneous sealed-bid stages. Stage 1 reveals sack card 1 and lets anyone bid or pass. Stage 2 reveals sack card 2, and the remaining players may raise. The stage-1 leader may also hold, writing 0, to keep their stage-1 bid. The highest effective bid wins. (fixes: P1): This keeps the escalating, information-revealing auction in a fixed number of steps.
- start_seat is drawn once at setup and changes only at the end of a round: to the sack winner, or to the next seat if nobody bought the sack. sack_owners lists the seats in seat order starting from start_seat. sack_cards is filled with each owner's played_card in the same order, immediately after cards are played, and is kept until the round ends. (fixes: P2): The sack must exist, with known owners per position, before revealing and valuing it.
- Each stage writes every submitted number into that player's bid attribute. Legality is checked against the standing_bid in force before the stage, which is 0 at stage 1. Bids are cleared only at the start of the next round. (fixes: P3): Resolution must read the real bids.
- Choices are limited to card, message, stage-1 bid and stage-2 bid, which is 4 choice steps. Every legal value is listed as an option at both stages: stage 1 offers 0 to the player's mice; stage 2 offers 0 and standing_bid+1 to the player's mice. (fixes: P4): This stays inside the choice limit and makes every legal bid choosable.
- Rewards are simplified. Every stage-1 passer gains 2 mice and leaves. Every player still in at stage 2 who does not win gains 3 mice. If everyone passes at stage 1, nobody takes the sack and its cards are discarded. (fixes: P5): Each player is in one of three clear outcomes. This keeps the original's rising consolation payments (2, then 3).
- The dog rule is restated precisely. It applies only if exactly one dog is in the whole sack. The large dog removes the highest positive cat, or the most negative cat if there is no positive one. The small dog removes the most negative cat, or the lowest positive cat if there is no negative one. (fixes: P6): The rule is unambiguous arithmetic.

Objective: The highest score (cat_points + mice) wins. If players tie, the one with more cat_points among them wins. If still tied, it is a draw between them.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. BASE NUMBERS. Each player's cat cards sum to -8-5+3+5+8+11+15 = 29. The average card is worth 29/10 = 2.9. A sack therefore averages about 8.7 with 3 players and about 14.5 with 5. A lone large dog cuts this by about 10, and a lone small dog adds about 6, so the dog effects roughly cancel. Over the 
- playable: pass. COMPLETENESS. Every case is specified:
- no bids;
- exactly one bid;
- several bids, with leader tie-break by seat order;
- stage 2 for the leader (hold or raise) and for others (raise above the standing bid or drop);
- a stage-2 tie, which the leader wins. A holding leader can never tie, because ot
- reasoning_over_luck: pass. CHANCE. The only randomness is the setup: one set-aside card per player and the start seat.
- Set-aside cards go into sacks that anyone may win, so a player is not directly harmed by losing a strong card.
- The swing in total cats available is at most 23 points across all players. It does not land o

## Complexity

- steps_per_round: designed 17, built 14, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 18, built 46, limit 20 (built: 80)
- hidden_elements: designed 2, built 9, limit 3
- random_draws_per_round: designed 0, built -, limit 1
- rounds: designed 9, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: each hand holds 9 cards and set_aside holds one card per player
- pass: Setup: mice 15, cat_points 0, no rounds completed
- pass: Each round every hand shrinks by one played card
- FAIL: Sack holds every seat's card with start_seat 3 of 4; sole bidder seat 4 takes all four cats | rule R4 is broken: sack_owners lists every seat starting at start_seat, ascending and wrapping, and sack_cards holds each owner's played_card in that order. With start_seat=3 of 4, sack_owners=[3,4,1,2].; seat 4 mice: expected 13, got 17; seat 4 cat_points: expected 27, got 0; Dara: the rule for 2 was never matched (the game never put that option to this seat)
- pass: Talk changes no state; all pass
- FAIL: Stage 1 offers bids from 0 up to the player's mice only | rule R6 is broken: In stage 1, sack_cards[1] is appended to sack_revealed, and each player simultaneously picks a bid from 0 to their mice. A bid of 0 is a pass.; seat 1 was never offered 5, but should have been; seat 1 was never offered 0, but should have been
- FAIL: Passers in stage 1 gain 2 mice | rule R7 is broken: When a player passes in stage 1 (bid 0, or bid above their mice), that player gains 2 mice and gets in_auction=false.; seat 1 mice: expected 11, got 17; seat 1 cat_points: expected 3, got 0; Ada: the rule for 4 was never matched (the game never put that option to this seat)
- pass: Nobody bids: start_seat 4 of 4 wraps to 1, everyone gains 2
- FAIL: Single stage-1 bidder wins the sack at their bid | rule R9 is broken: When exactly one player bids in stage 1, that player wins the sack at their bid, and stage 2 does not happen.; seat 2 mice: expected 9, got 17; seat 2 cat_points: expected 13, got 0; Blaise: the rule for 6 was never matched (the game never put that option to this seat)
- FAIL: Highest stage-1 bid leads; leader holding at 0 wins at standing bid | rule R10 is broken: When two or more players bid in stage 1, standing_bid is the highest bid and leader_seat is its bidder. A tie goes to the first tied seat counting from the seat after start_seat.; seat 2 mice: expected 9, got 17; seat 2 cat_points: expected 8, got 0; seat 1 mice: expected 18, got 17; Ada: the rule for 4 was never matched (the game never put that option to this seat); Blaise: the rule for 6 was never matched (the game never put that option to this seat)
- FAIL: Stage-1 tie: leader is first tied seat after start_seat (seat 3 over seat 1) | rule R10 is broken: When two or more players bid in stage 1, standing_bid is the highest bid and leader_seat is its bidder. A tie goes to the first tied seat counting from the seat after start_seat.; seat 3 mice: expected 10, got 17; seat 3 cat_points: expected 8, got 0; seat 1 mice: expected 18, got 17; game start_seat: expected 3, got 2; Cleo: the rule for 5 was never matched (the game never put that option to this seat)
- FAIL: Stage 2 offers raises up to mice only; non-leader raise wins | rule R11 is broken: In stage 2, sack_cards[2] is revealed, and each player with in_auction=true is offered 0 or any whole number from standing_bid+1 to their mice.; seat 1 mice: expected 0, got 12; seat 1 cat_points: expected 3, got 0; seat 2 mice: expected 18, got 17; game start_seat: expected 1, got 2; seat 1 was never offered 10, but should have been; Ada: the rule for 3 was never matched (the game never put that option to this seat); Ada: the rule for 10 was never matched (the game never put that option to this seat)
- FAIL: Leader's raise above standing bid is their effective bid and beats a lower raise | rule R12 is broken: When the leader answers 0 in stage 2, their effective bid equals standing_bid. When the leader answers a number above standing_bid, that number is their effective bid.; seat 2 mice: expected 6, got 17; seat 2 cat_points: expected 8, got 0; seat 1 mice: expected 18, got 17; Ada: the rule for 4 was never matched (the game never put that option to this seat); Ada: the rule for 8 was never matched (the game never put that option to this seat); Blaise: the rule for 6 was never matched (the game never put that option to this seat); Blaise: the rule for 9 was never matched (the game never put that option to this seat)
- FAIL: Non-leader answering 0 in stage 2 has no effective bid; leader wins at standing bid | rule R13 is broken: When a non-leader answers 0, or a number not above standing_bid or above their mice, in stage 2, that player has no effective bid.; seat 1 mice: expected 9, got 17; seat 1 cat_points: expected 11, got 0; seat 2 mice: expected 18, got 17; game start_seat: expected 1, got 2; Ada: the rule for 6 was never matched (the game never put that option to this seat); Blaise: the rule for 4 was never matched (the game never put that option to this seat)
- FAIL: Stage-2 tie among non-leaders goes to first seat after start_seat | rule R14 is broken: In stage 2 the highest effective bid wins. On a tie the leader wins if among the tied players; otherwise the first tied seat counting from the seat after start_seat wins.; seat 2 mice: expected 7, got 17; seat 2 cat_points: expected 8, got 0; seat 1 mice: expected 18, got 17; seat 3 mice: expected 18, got 17; Blaise: the rule for 8 was never matched (the game never put that option to this seat); Cleo: the rule for 3 was never matched (the game never put that option to this seat); Cleo: the rule for 8 was never matched (the game never put that option to this seat)
- FAIL: Stage-2 tie including the leader goes to the leader | rule R14 is broken: In stage 2 the highest effective bid wins. On a tie the leader wins if among the tied players; otherwise the first tied seat counting from the seat after start_seat wins.; seat 2 mice: expected 6, got 17; seat 2 cat_points: expected 8, got 0; seat 1 mice: expected 18, got 17; game start_seat: expected 2, got 1; Ada: the rule for 9 was never matched (the game never put that option to this seat); Blaise: the rule for 7 was never matched (the game never put that option to this seat); Blaise: the rule for 9 was never matched (the game never put that option to this seat)
- FAIL: Every in-auction stage-2 loser gains 3 mice | rule R15 is broken: When stage 2 resolves, every in_auction player other than the winner gains 3 mice.; seat 2 mice: expected 9, got 17; seat 2 cat_points: expected 11, got 0; seat 1 mice: expected 18, got 17; seat 3 mice: expected 18, got 17; Ada: the rule for 4 was never matched (the game never put that option to this seat); Blaise: the rule for 6 was never matched (the game never put that option to this seat); Cleo: the rule for 2 was never matched (the game never put that option to this seat)
- FAIL: Sack winner pays and becomes start_seat | rule R16 is broken: The sack winner pays winning_bid mice, all sack cards are revealed, and the winner becomes start_seat.; seat 1 mice: expected 10, got 17; Ada: the rule for 5 was never matched (the game never put that option to this seat)
- FAIL: Large dog removes highest positive cat: 15,3,large_dog = 3 | rule R17 is broken: When exactly one dog is in the sack and it is large_dog, it removes the highest positive cat, or the most negative cat if there is no positive cat. Example: a sack of cat_15, cat_3, large_dog has value 3.; seat 1 mice: expected 14, got 17; seat 1 cat_points: expected 3, got 0
- FAIL: Large dog with no positive cat removes most negative: -8,-5,large_dog = -5 | rule R17 is broken: When exactly one dog is in the sack and it is large_dog, it removes the highest positive cat, or the most negative cat if there is no positive cat. Example: a sack of cat_15, cat_3, large_dog has value 3.; seat 1 mice: expected 14, got 17; seat 1 cat_points: expected -5, got 0; Ada: the rule for 1 was never matched (the game never put that option to this seat)
- FAIL: Small dog removes most negative cat: -8,5,small_dog = 5 | rule R18 is broken: When exactly one dog is in the sack and it is small_dog, it removes the most negative cat, or the lowest positive cat if there is no negative cat. Example: a sack of cat_-8, cat_5, small_dog has value 5.; seat 1 mice: expected 14, got 17; seat 1 cat_points: expected 5, got 0; Ada: the rule for 1 was never matched (the game never put that option to this seat)
- FAIL: Small dog with no negative cat removes lowest positive: 3,8,small_dog = 8 | rule R18 is broken: When exactly one dog is in the sack and it is small_dog, it removes the most negative cat, or the lowest positive cat if there is no negative cat. Example: a sack of cat_-8, cat_5, small_dog has value 5.; seat 1 mice: expected 14, got 17; seat 1 cat_points: expected 8, got 0; Ada: the rule for 1 was never matched (the game never put that option to this seat)
- FAIL: Two dogs remove nothing: 15,large_dog,small_dog = 15 | rule R19 is broken: When the sack holds zero or two dogs, no cat is removed. Example: a sack of cat_15, large_dog, small_dog has value 15.; seat 1 mice: expected 14, got 17; seat 1 cat_points: expected 15, got 0
- FAIL: Negative sack value is added: -8,rabbit,-5 = -13 | rule R20 is broken: sack_value is the sum of the remaining cat values, with rabbit and dogs worth 0, and it is added to the winner's cat_points even if negative. Example: cat_-8, rabbit, cat_-5 gives -13.; seat 1 mice: expected 14, got 17; seat 1 cat_points: expected -13, got 0; Ada: the rule for 1 was never matched (the game never put that option to this seat)
- pass: Game ends after round 9; equal score broken by more cat_points
- pass: Fully tied score and cat_points share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 5], results {'seat 3': 11, 'seat 1': 14, 'seat 2': 10, 'seat 5': 2, 'seat 4': 3}, 84-155 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 122.2 decisions, prompts of 206 characters on average (longest 421)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 3': 22, 'seat 1': 21, 'seat 2': 17}
- always `first@seat1`: won 10, lost 50, drew 0
- always `first@seat2`: won 12, lost 48, drew 0
- always `last@seat1`: won 15, lost 44, drew 1
- always `last@seat2`: won 24, lost 36, drew 0

## Triage (whose problem each failure was)

- round 1: fix_game: In the bidding scenarios the scripted bids were never offered to the players. Seat 1's bid of 1 and Blaise's bid of 3 were never put to them, so every stage-1 poll fell back to a pass (0), and the all-pass branch ran where a sale should have happened. The rules are clear and the platform supports numeric simultaneous bids, so the bid poll in the game file is wrong.
- round 1: fix_game: Each failure is a fixable coding slip, not a flaw in the rules or a missing capability. The attempts hit an unfilled {mice} placeholder, private bookkeeping fields shown blank to players, and an `unopened_pile` attribute that a rare all-pass branch only would ever change. The rules are expressible: simultaneous bids, hidden hands, and `when`/`if` conditional updates are all supported.
- round 1: fix_game: In several scenarios a lone legal bid of 1 (or another legal bid) is treated as a pass. Seat 1 ends with 17 mice (15 + the 2-mouse pass reward) and 0 cat points instead of winning the sack, which points to a bug in how the game file reads, validates or resolves bids, not to a problem with the rules.
- round 2: fix_game: Every failing scenario has the same cause: the stage-1 bid poll never offers the numbers the rules require. Seats were never offered 0, 2, 4, 5 or 6, so everyone ended up passing (mice 17, no sack taken). Numeric bids are supported, and the pass bonus and start_seat advance worked correctly, so the fault is in how the game file builds the bid options, not in the rules or the tests.
- round 2: fix_game: The sack held cat_3, cat_8 and small_dog. Under R10 a lone small dog with no negative cat removes the lowest positive cat, so the sack is worth 8, but the game left dog_removed at 0 and scored 11. The test reads the rules correctly, and the file is missing the small dog's fallback branch.
- round 2: fix_game: In every failing scenario the stage-1 bid poll never offered the numbers 0 to the player's mice: seat 1 was never offered 0 or 5, and the rules for 4 and 6 were never matched. So every player was recorded as passing, gained 2 mice (17 each), and no sack was taken. The rules are clear and the engine supports numeric bids in a simultaneous poll, so this is an error in the game file.

## Choices the rules did not make

- 3 to 5 players, suggested 4: The designer suggests 4, which is kept. 3 is the minimum for a sack built from several hidden cards with rivals bidding. Above 5 the sack and the bidding become too diluted for one card or bid to matter.
- Talk is a simultaneous poll broadcast to all: The rules say messages are written simultaneously without seeing the others. Players disagree about the sack's value, so bluffing about one's own card matters.
- The tie-break uses the order (seat - start_seat - 1 + N) mod N: This is the arithmetic form of 'first tied seat starting from the seat after start_seat'.
- rank_by = (cat_points + mice) * 1000 + cat_points: This encodes score first and cat_points as the tie-break. |cat_points| stays well below 500 given the finite cards.
- Card values are read from the card name (cat_X is worth X; rabbit and dogs are worth 0): The rules give cards as named tokens with these values.
- Players are offered only legal numbers, though the rules also say out-of-range numbers mean pass or drop out: The engine offers ranges. The out-of-range rule is still stated so the resolution stays faithful.

## Simplifications

- The branches 'round ends' and 'go to R10' are run as per-step `when` conditions on bidder_count and sack_winner in a flat step list: The engine has no block branching. Single steps with arithmetic conditions give the same result.
- The dog rule and sack_value are worked out in one update step with conditional arithmetic over sack_cards: The removal rules are deterministic arithmetic, so no referee is needed.

## Encoding attempts

- 1: it plays, but part of it does nothing: game attribute `starting_cards` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 2: passed
