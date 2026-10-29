# felicity_the_cat_in_the_sack: needs review

Built from the variation **Cat in the Sack: Sealed Stages (Revised)** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- After every stage, each player's number (their bid, or 0 for a pass) is announced by name, together with the new standing bid, the leader and every player's mice. (fixes: P1): This makes observations exact, so a player can infer, for example, that the owner of hidden card 3 bidding high suggests it is a good cat.
- All-pass rules stated exactly. At stage 1, if all pass, every player gains 2 and the sack is discarded unopened. At stage 2 or 3, if all players still in pass, the previous leader takes the sack at the standing bid and gets no reward, while every other passer gains that stage's reward. (fixes: P2): This removes the ambiguity, so every build pays out the same mice.
- Simultaneous talk is folded into the placement poll. While placing their card face down, each player writes one short message. All messages are shown once the sack is laid out, before stage 1. Claims are not enforced. (fixes: P3, P5): This gives players claims to make, test and bluff about (for example 'mine is the 15' or 'mine is the small dog'). It passes both talk tests: players disagree because only one player wins the game and each sack, and it adds no extra choice step.
- Reworded: the immediate win happens 'at the standing bid just set'. The consolation reads 'each player who bid at stage 3 but is not the leader gains 5'. (fixes: P4): This states clearly who pays what and who is consoled.

Objective: The player with the highest score (cat points + mice) wins. If several players tie, the tied player with the most cat points wins. If they are still tied, the game is a draw among them.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. SACK VALUE. One hand's cats sum to -8-5+3+5+8+11+15 = 29 over 10 cards, so a card averages 2.9. One random card is removed, so a player expects to play 26.1 cat points over the game. An unchosen sack card is worth about +2.9. A full sack averages about 8.7 (3 players), 11.6 (4) or 14.5 (5), before d
- playable: pass. COMPLETENESS. Every branch is specified:
- all pass at stage 1 (sack discarded, +2 each);
- all still in pass at stage 2 or 3 (the previous leader takes the sack at the standing bid);
- exactly one player left (immediate win);
- two or more left after stage 3 (the leader wins, stage-3 bidders who lo
- reasoning_over_luck: pass. CHANCE. Chance comes from two sources:
- One removed card per hand. Expected removed value is 2.9, ranging from -8 to 15. A player's own cards score only if he wins his own sack, so the removal mostly changes what opponents can win, not his own total.
- A random first start player, a one-round effec

## Complexity

- steps_per_round: designed 18, built 17, limit 20
- choice_steps_per_round: designed 4, built 5, limit 4
- attributes: designed 15, built 49, limit 20 (built: 80)
- hidden_elements: designed 2, built 10, limit 3
- random_draws_per_round: designed 0, built -, limit 1
- rounds: designed 9, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: each hand keeps 9 cards and 3 cards are set aside (3 players)
- pass: Setup: 15 mice and 0 cat points each
- pass: Playing a card removes it from the hand (9 -> 8)
- pass: Message round is played and the round continues normally (all pass, +2 each)
- FAIL: Sack holds one card per seat, one owner per position | rule R5 is broken: The sack is ordered in seat order beginning with the start player, so sack position 1 is the start player's card; everyone knows the owner of each position.; game sack_cards: expected 3 items, got 0
- FAIL: Standing bid starts at 0, so a bid of 1 is legal and wins when alone | rule R6 is broken: At stage 1, sack card 1 is revealed to all, the standing bid is 0 and there is no leader.; seat 1 mice: expected 14, got 17; seat 1 cat_points: expected 18, got 0; game start_seat: expected 1, got 2
- FAIL: A stage 2 bid at or below the standing bid counts as a pass | rule R7 is broken: At each stage, the players still in simultaneously write a number; 0 is a pass, and a bid must be at least standing_bid + 1 and at most the bidder's mice, or it counts as a pass.; seat 1 mice: expected 10, got 17; seat 1 cat_points: expected 18, got 0; seat 2 mice: expected 18, got 17; Blaise: the rule for 4 was never matched (the game never put that option to this seat)
- FAIL: Bids are announced and the auction resolves from them (single bidder wins) | rule R8 is broken: After each stage, every player's bid (0 for a pass) is announced by name.; seat 2 mice: expected 12, got 17; seat 2 cat_points: expected 8, got 0; Blaise: the rule for 3 was never matched (the game never put that option to this seat)
- FAIL: All pass at stage 1: +2 each, sack unopened, start moves to next seat (wraps 3 -> 1) | rule R9 is broken: When every player passes at stage 1, then every player gains 2 mice, nobody takes the sack, it is discarded unopened, and play goes to choosing the next start player.; game unopened_pile: expected 3 items, got None
- FAIL: All in pass at stage 2: previous leader takes sack, other passer +3 | rule R10 is broken: When every player still in passes at stage 2, then the previous leader takes the sack at the standing bid with no reward, and every other passer gains 3 mice.; seat 1 mice: expected 10, got 17; seat 1 cat_points: expected 18, got 0; seat 2 mice: expected 18, got 17
- FAIL: All in pass at stage 3: previous leader takes sack, other passer +4 | rule R11 is broken: When every player still in passes at stage 3, then the previous leader takes the sack at the standing bid with no reward, and every other passer gains 4 mice.; seat 1 mice: expected 10, got 17; seat 1 cat_points: expected 18, got 0; seat 2 mice: expected 19, got 17; Ada: the rule for 2 was never matched (the game never put that option to this seat); Blaise: the rule for 2 was never matched (the game never put that option to this seat); Blaise: the rule for 4 was never matched (the game never put that option to this seat)
- FAIL: Passers leave with +3 at stage 2 and +4 at stage 3 | rule R12 is broken: When not everyone passed, then each passer leaves the auction for the round and gains 2 mice at stage 1, 3 at stage 2 or 4 at stage 3.; seat 1 mice: expected 18, got 17; seat 2 mice: expected 9, got 17; seat 2 cat_points: expected 18, got 0; seat 3 mice: expected 19, got 17; game start_seat: expected 2, got 1; Blaise: the rule for 2 was never matched (the game never put that option to this seat); Blaise: the rule for 4 was never matched (the game never put that option to this seat); Blaise: the rule for 6 was never matched (the game never put that option to this seat); Cleo: the rule for 3 was never matched (the game never put that option to this seat); Cleo: the rule for 5 was never matched (the game never put that option to this seat)
- FAIL: Highest bid sets the standing bid and its bidder leads (seat 1 pays 7) | rule R13 is broken: When not everyone passed, then the standing bid becomes the highest bid at that stage, and its bidder becomes the leader.; seat 1 mice: expected 8, got 17; seat 1 cat_points: expected 18, got 0; seat 2 mice: expected 18, got 17; Ada: the rule for 7 was never matched (the game never put that option to this seat)
- FAIL: Tied top bid: leader is first after the start player (start 1 -> seat 2 leads) | rule R14 is broken: When several players make the highest bid, then the leader is the first of them in seat order, counting from the player after the start player, with the start player last.; seat 1 mice: expected 18, got 17; seat 2 mice: expected 11, got 17; seat 2 cat_points: expected 18, got 0; seat 3 mice: expected 18, got 17; Ada: the rule for 4 was never matched (the game never put that option to this seat); Blaise: the rule for 4 was never matched (the game never put that option to this seat); Cleo: the rule for 4 was never matched (the game never put that option to this seat)
- FAIL: After a stage the new mice totals are correct (passers +2, winner pays) | rule R15 is broken: After a stage is resolved, the new standing bid, the leader and every player's mice are announced.; seat 4 mice: expected 9, got 17; seat 4 cat_points: expected 16, got 0; game start_seat: expected 4, got 2; Dara: the rule for 6 was never matched (the game never put that option to this seat)
- FAIL: One player left after stage 1 wins at once at the bid just set | rule R16 is broken: When exactly one player remains in after a stage, then that player wins the sack at the standing bid just set and the remaining stages are skipped.; seat 3 mice: expected 6, got 17; seat 3 cat_points: expected 18, got 0; game start_seat: expected 3, got 2; Cleo: the rule for 9 was never matched (the game never put that option to this seat)
- FAIL: Stages 2 and 3 are played while two or more remain | rule R17 is broken: Stage 2 reveals sack card 2 and stage 3 reveals sack card 3, and each is played only if two or more players are still in.; seat 1 mice: expected 18, got 17; seat 2 mice: expected 9, got 17; seat 2 cat_points: expected 18, got 0; seat 3 mice: expected 19, got 17; Blaise: the rule for 2 was never matched (the game never put that option to this seat); Blaise: the rule for 4 was never matched (the game never put that option to this seat); Blaise: the rule for 6 was never matched (the game never put that option to this seat); Cleo: the rule for 3 was never matched (the game never put that option to this seat); Cleo: the rule for 5 was never matched (the game never put that option to this seat)
- FAIL: Two still in after stage 3: tied leader wins, other stage-3 bidder +5 | rule R18 is broken: When two or more players are still in after stage 3 is resolved, then the leader wins the sack at the standing bid, and each other player who bid at stage 3 gains 5 mice.; seat 1 mice: expected 10, got 17; seat 1 cat_points: expected 18, got 0; seat 2 mice: expected 20, got 17; Ada: the rule for 2 was never matched (the game never put that option to this seat); Ada: the rule for 5 was never matched (the game never put that option to this seat); Blaise: the rule for 1 was never matched (the game never put that option to this seat); Blaise: the rule for 5 was never matched (the game never put that option to this seat)
- FAIL: Opened sack: all cards counted (cat_5 + cat_8 + cat_11 = 24) | rule R19 is broken: When the sack is opened, all its cards are revealed.; seat 1 mice: expected 13, got 17; seat 1 cat_points: expected 24, got 0; Ada: the rule for 2 was never matched (the game never put that option to this seat)
- FAIL: Large dog alone removes the highest cat (15 removed, 3 left) | rule R20 is broken: When exactly one dog is in the sack, then the large dog removes the highest-valued cat or the small dog removes the lowest-valued cat; when no cat is present nothing is removed, and when both dogs are present neither has any effect.; seat 1 mice: expected 14, got 17; seat 1 cat_points: expected 3, got 0; Ada: the rule for 1 was never matched (the game never put that option to this seat)
- FAIL: Small dog alone removes the lowest cat (-8 removed, 11 left) | rule R20 is broken: When exactly one dog is in the sack, then the large dog removes the highest-valued cat or the small dog removes the lowest-valued cat; when no cat is present nothing is removed, and when both dogs are present neither has any effect.; seat 1 mice: expected 14, got 17; seat 1 cat_points: expected 11, got 0; Ada: the rule for 1 was never matched (the game never put that option to this seat)
- FAIL: Both dogs present: no effect (-8 stays) | rule R20 is broken: When exactly one dog is in the sack, then the large dog removes the highest-valued cat or the small dog removes the lowest-valued cat; when no cat is present nothing is removed, and when both dogs are present neither has any effect.; seat 2 mice: expected 14, got 17; seat 2 cat_points: expected -8, got 0; Blaise: the rule for 1 was never matched (the game never put that option to this seat)
- FAIL: Dog with no cat present removes nothing (value 0) | rule R20 is broken: When exactly one dog is in the sack, then the large dog removes the highest-valued cat or the small dog removes the lowest-valued cat; when no cat is present nothing is removed, and when both dogs are present neither has any effect.; seat 1 mice: expected 14, got 17; Ada: the rule for 1 was never matched (the game never put that option to this seat)
- FAIL: Winner pays the bid and cat points may go negative (-8 -5 + rabbit = -13) | rule R21 is broken: The sack winner pays their winning bid in mice and adds the total value of the remaining cats to cat_points, which may go negative; the rabbit is worth 0.; seat 3 mice: expected 13, got 17; seat 3 cat_points: expected -13, got 0; Cleo: the rule for 2 was never matched (the game never put that option to this seat)
- FAIL: Opened sack cards go to the discard pile (3 cards) | rule R22 is broken: Opened sack cards are discarded face up, so everyone can see which cards each player has used.; game discard_pile: expected 3 items, got 0
- FAIL: Sack winner becomes start player (start 1, seat 3 wins -> 3) | rule R23 is broken: When someone took the sack, then the sack winner becomes the start player; otherwise the start player passes to the next seat.; game start_seat: expected 3, got 2; Cleo: the rule for 1 was never matched (the game never put that option to this seat)
- pass: No sack winner: start passes to the next seat (1 -> 2)
- pass: Game ends after round 9 with hands empty
- pass: Tied score broken by cat points
- pass: Fully tied players share the win

## Does the file follow the spec's shape? (flags for a person)

- the spec declares player attribute `seat` but the game file does not: a piece of state the rules need is missing
- the spec declares game attribute `unopened_pile` but the game file does not: a piece of state the rules need is missing

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 5], results {'seat 1': 13, 'seat 3': 9, 'seat 2': 9, 'seat 5': 6, 'seat 4': 3}, 79-164 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 124.5 decisions, prompts of 182 characters on average (longest 276)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 1': 23, 'seat 3': 22, 'seat 2': 15}
- always `first@seat1`: won 15, lost 45, drew 0
- always `first@seat2`: won 13, lost 47, drew 0
- always `last@seat1`: won 19, lost 41, drew 0
- always `last@seat2`: won 23, lost 37, drew 0

## Triage (whose problem each failure was)

- round 1: fix_game: In the bidding scenarios the scripted bids were never offered to the players. Seat 1's bid of 1 and Blaise's bid of 3 were never put to them, so every stage-1 poll fell back to a pass (0), and the all-pass branch ran where a sale should have happened. The rules are clear and the platform supports numeric simultaneous bids, so the bid poll in the game file is wrong.
- round 1: fix_game: Each failure is a fixable coding slip, not a flaw in the rules or a missing capability. The attempts hit an unfilled {mice} placeholder, private bookkeeping fields shown blank to players, and an `unopened_pile` attribute that a rare all-pass branch only would ever change. The rules are expressible: simultaneous bids, hidden hands, and `when`/`if` conditional updates are all supported.
- round 1: fix_game: In several scenarios a lone legal bid of 1 (or another legal bid) is treated as a pass. Seat 1 ends with 17 mice (15 + the 2-mouse pass reward) and 0 cat points instead of winning the sack, which points to a bug in how the game file reads, validates or resolves bids, not to a problem with the rules.

## Choices the rules did not make

- 3 to 5 players, suggested 4: The designer chose 4, so it is kept. 3 is the least number of players for a sack with three staged reveals and a real auction among rivals. 5 is the most: a sack of 5 cards fills every position, and more seats would leave too many hidden cards and messages to reason about.
- Talk kept as a simultaneous poll shown to everyone: The rules require one simultaneous message per round. Players disagree over who should take the sack, so claims about their own card are worth bluffing and worth doubting.
- Card codes such as cat_15, rabbit, large_dog, small_dog: The cards need text names so the engine can store and compare them in lists.
- Cat values listed as separate parameters cat_value_1 to cat_value_7: Each parameter must be a single number.
- Tie-break encoded as (cat_points + mice) * 1000 + cat_points: The ranking must be one expression. Cat points can never exceed 210 in absolute value, so a one-point score difference always outweighs the cat-points term.
- Unopened sacks go to a hidden unopened_pile: The rules say such a sack is discarded without being opened, so its unrevealed cards must stay unseen.

## Simplifications

- The message and the card choice are two consecutive polls instead of one combined answer: A poll gathers one answer. Neither answer is shown until both polls are complete, so they stay simultaneous in effect.
- Bids are offered as any number from 0 to the bidder's mice, with numbers at or below the standing bid treated as a pass: This matches the rule that an illegal number counts as a pass, while keeping the offered range simple.
- 'Go to step 7/9' is done with when-conditions on sack_done and sack_winner: The step list is flat. Skipping single steps by condition gives the same flow.

## Encoding attempts

- 1: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (message, played_card) in `your_starting_state`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 2: passed
