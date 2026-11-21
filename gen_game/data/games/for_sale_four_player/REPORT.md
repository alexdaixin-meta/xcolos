# for_sale: ready for review

Built from the variation **For Sale: Sealed Bids - Four Player** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- 4 players, 18 coins each, 28 properties and 28 cheques used: 7 buying rounds and 7 selling rounds of 4 cards, bottom 2 of each deck unseen; buying rank 1 takes HIGH, rank 2 SECOND, rank 3 THIRD, rank 4 LOW; priority rotates ((r-1) mod 4)+1. (fixes: Three-player field only gave two rivals to model and an easier win, against the owner's request for four players and harder winning.): More opponents to model and harder win using original 4-player numbers, keeping two phases and deck sizes.
- Buying payments: first-ranked pays full bid, second-, third- and fourth-ranked each pay half their bid rounded UP (ceil). Bid range stays 0 to current coins, one simultaneous sealed bid, totals private. (fixes: Free minimal bids: under pay-half-rounded-down, bids of 1 cost 0 unless first, so 39 of 72 sealed bids were 1 and in 10 of 24 rounds every bid was 0 or 1, so rotating priority not reading rivals decided who took the best card.): Every positive bid now has real cost win or lose (1 always costs 1, 2 costs 1-2, etc.) while 0 is free but risks LOW, so amounts carry information about valuation and remaining budget.
- Kept sealed simultaneous buying and simultaneous selling instead of open auction. (fixes: Original open clockwise raise-or-pass auction cannot run on the turn-based simultaneous-poll engine.): Platform cannot run open ascending auction; sealed bids fit simultaneous polls and preserve bluff and inference.

Objective: Player with most final money (cheques plus remaining coins) wins. If tied for most, tied player with more remaining coins wins. If still tied, game is a draw among them.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. Cost table: pay = bid if 1st, ceil(bid/2) otherwise. 0->0/0,1->1/1,2->2/1,3->3/2,4->4/2,10->10/5,18->18/9. No dominant bid: higher bid raises P(HIGH) but raises cost. Winner rule = max(cheques+coins), tie=more coins. Always-0: gets 7x LOW (~exp min ~6) keeps 18 coins. Cheques ~2-3 avg => total ~15-2
- playable: pass. Complete: 4 players, 18 coins, decks defined, 14 fixed rounds (7 buy+7 sell), 28/30 cards used, bid 0..coins, ranking+rotating tiebreak, pay full/half-up, announce taker of HIGH/SECOND/THIRD/LOW, sell: play 1 property simultaneous, distinct values=>no ties, map rank to rank, discard, announce plays/
- reasoning_over_luck: pass. Luck: shuffle of 30->28 properties and 30->28 cheques, plus tiebreaks. Skill: coin management over 7 buys, valuing HIGH vs SECOND/THIRD/LOW spread, matching property rank to cheque board in sells. Good play beats no-reason: random bidder overspends early / mismatches high property to low cheque boar
- open_play: pass. Fixed R1 deal e.g. properties 28,20,11,3, all start 18. Options: bid high ~10 to force HIGH, mid ~3-5 for SECOND/THIRD cheap, 0-1 for LOW free. Plan A Aggressive: bid 8-10 R1 take 28, pay 8-10, keep power for high cheques. Wins vs opponents who all bid low/mid (steals HIGH cheap) and vs opponents wh

## Complexity

- steps_per_round: designed 5, built 13, limit 20
- choice_steps_per_round: designed 1, built 2, limit 4
- attributes: designed 16, built 37, limit 20 (built: 80)
- hidden_elements: designed 3, built 17, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 14, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Initial holds 18 coins 0 total empty hand
- pass: Property deck deals 4 to start buying
- pass: Cheque deck reveals 4 cheques in selling
- pass: Round 7 buying then round 8 selling boundary
- pass: Seven buying rounds deal 28 properties
- pass: R6 reveal next 4 sorted HIGH to LOW
- pass: R7 bids from 0 up to coins are accepted
- pass: R8 tie bids break by priority starting seat 2 in round 2
- pass: R9 first takes HIGH others take lower after half payments
- pass: R10 payments leave public property allocation
- pass: R11 public HIGH SECOND THIRD LOW allocation
- pass: R12 after round 7 each holds 7 properties
- pass: R13 selling reveals 4 cheques sorted high to low
- pass: R14 secretly choose one property from hand
- pass: R15 distinct properties have no ties
- pass: R16 highest property adds highest cheque
- pass: R17 played properties are discarded
- pass: R18 public property and cheque allocation
- pass: R19 hands empty and final money revealed at end
- pass: R20 most final money wins
- pass: R21 tie final more coins wins
- pass: R21 still tied shares win
- pass: R22 sealed simultaneous choices

## Does the file follow the spec's shape? (flags for a person)

- the spec uses `initialize` but the game file does not

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [4], results {'seat 1': 3, 'seat 4': 4, 'seat 2': 5, 'seat 3': 8}, 52-52 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 56.0 decisions, prompts of 304 characters on average (longest 402)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 1': 11, 'seat 4': 15, 'seat 2': 13, 'seat 3': 20, 'seats 2 and 3': 1}
- always `first@seat1`: won 5, lost 55, drew 0
- always `first@seat2`: won 6, lost 54, drew 0
- always `last@seat1`: won 0, lost 59, drew 1
- always `last@seat2`: won 3, lost 57, drew 0

## Triage (whose problem each failure was)

- round 1: fix_tests: The game correctly did round-7 buying with bids 4,3,2,1 to award 30,25,15,5, correct half-up payments and priority 3, yet was failed for offering 5 which bid 5 requires, and was failed for shuffled order.

## Choices the rules did not make

- 4 to 4 players with suggested 4: designer fixed 4 seats with 4 cards per round and 28 usable cards for 7 each; smallest table where sealed simultaneous bidding and priority tie-break matter and larger table breaks 4-per-round reveal
- no talk poll, sealed poll for bids and for property choice: source says no talk phase and every choice sealed; simultaneous choice must use poll not ask so later seats do not hear earlier answers
- half rounded up as (bid+1)//2: matches example 0->0 1->1 2->1 3->2 4->2 with integer arithmetic
- rank_by you.final_money * 1000 + you.coins: encodes most final money wins with more remaining coins as tie-break within arithmetic ranking since coins never reach 1000
- priority_seat ((round_number-1) mod 4)+1: concrete arithmetic for stated tie-break rotation

## Simplifications

- shuffle represented as random draw from list and remove bottom 2 unseen first: engine shuffles by drawing at random from game list with remove/append operations
- current_offer holds sorted HIGH to LOW reveal and property_discard holds played properties: engine has no board so cards live in table lists and player lists
- final_money attribute set to cheque_total+coins after round 14: enables arithmetic ranking and observable score without model opinion
