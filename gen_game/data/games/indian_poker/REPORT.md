# indian_poker: ready for review

Built from the variation **Forehead Poker Match** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Play a match of 16 hands, with chips carried from hand to hand. The winner is the player with the most chips at the end. (fixes: A single hand makes the result almost pure card luck; skill cannot show.): Card luck evens out over 16 hands, while good reading, folding and bluffing accumulate. Chip management and reputation across hands add planning.
- Replace open betting with two fixed simultaneous decisions. First, everyone at the same moment chooses Fold or a bet of 1, 2 or 3 chips. Then the bets are revealed, and every remaining player at the same moment chooses Call (match the highest bet) or Fold. (fixes: Open-ended sequential betting (raise and re-raise until matched) is an unbounded loop the engine cannot build.): This keeps the bet, see and respond structure of poker in a fixed number of steps the engine can build.
- Make all betting decisions simultaneous. (fixes: Turn-order betting gives a fixed positional edge to whoever acts last.): No seat ever acts with more information than another, so position gives no edge.
- If every player folds, or nobody is left to contest the pot, the whole pot carries over to the next hand. (fixes: Folding costs only the ante, so very tight play is cheap and the game can stall into everyone folding.): Mass folding feeds a bigger future pot, which raises the stakes and punishes passive play relative to opponents who contest it.
- Before betting each hand, every player writes one short public message at the same moment, and all messages are then shown. Players may say anything, including true or false claims about other players' cards. (fixes: The table-talk and bluffing that make the game fun in person are informal, so a text platform has no defined channel for them.): This formalises Indian Poker's table talk. You can try to scare a strong player out or lure a weak one in, but the other players see that player's card and know whether you lied. That rewards bluffing, reading and tracking reputation.
- Use a fixed ante, a bet cap of 3 chips and 40 starting chips. A player who has fewer than 4 chips at the start of a hand is eliminated and keeps that total. (fixes: There is no multi-round planning: no chip management, no reputation, nothing carried between decisions.): Losses per hand are bounded, so chip management across the match matters and one hand cannot decide everything.

Objective: The player with the most chips at the end of the match wins. Eliminated players count with the chips they held when eliminated. If two or more players tie for the most chips, the game is a draw among them.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. STRUCTURE: Every choice is a simultaneous poll and every player sees exactly N-1 cards, all but their own. No seat has a move-order or information edge. The game is zero-sum in chips, apart from a carried pot that is discarded at the end.

MAIN DECISION (4 players, cards numbered 1-52 by strength): 
- playable: pass. COMPLETENESS:
- Every situation is defined:
  - All players fold in step 5: the pot carries over.
  - A lone bettor equals H, calls free and wins.
  - Several callers: the strongest card wins.
  - No callers: the pot carries.
- Card order is total because suits break ties.
- Elimination below 4 chip
- reasoning_over_luck: pass. WHAT TO INFER: Each player must estimate their own hidden card from three sources:
1. The N-1 visible cards (the probability table above).
2. The simultaneous talk claims, which are possibly lies, and their senders' incentives.
3. The revealed step-5 bets, because opponents bet on how your card comp

## Complexity

- steps_per_round: designed 16, built 14, limit 20
- choice_steps_per_round: designed 3, built 3, limit 4
- attributes: designed 10, built 28, limit 20 (built: 80)
- hidden_elements: designed 1, built 7, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 16, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Match starts with 40 chips each, pot 0, hand_number 0
- pass: Player starting a hand with 3 chips is eliminated and keeps 3 chips
- pass: Player starting a hand with exactly 4 chips stays active and plays
- pass: Deal removes one card per active player from a refilled deck
- pass: Eliminated player is not dealt a card; deck refilled and only active players draw
- pass: Two callers: pot is paid out to one of them (card chance decides which), folders lose only the ante
- pass: Ante takes 1 chip from each of 4 active players into the pot
- pass: Talk with 5 players then all fold: hand completes, pot holds 5 antes
- pass: Bet 3 then fold at call: chips 36 and pot 7 carries over
- pass: First-bet folder loses only the ante and is not asked to call
- pass: H is the highest bet: Bet 1 caller pays 2 more when the other bet 3 and folded
- pass: Caller who bet 2 against H=3 pays 1 more and wins pot of 10 alone
- pass: Bettor who folds at call step forfeits ante and bet
- pass: Two callers: pot goes to one caller and becomes 0 (winner by chance not asserted)
- pass: Single caller wins the whole pot without comparison
- pass: Everyone folds two hands running: pot carries over to 8
- pass: Only bettor folds at call step: pot carries over
- pass: Showdown reveal: a player dealt no card (eliminated) shows nothing; hand completes
- pass: Match ends after hand 16; most chips wins
- pass: Only one player left active at hand start: match ends at once
- pass: Second player eliminated after one hand ends the match early
- pass: Tied for most chips at the end share the win
- pass: Eliminated player counts with chips at elimination in final ranking

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [4, 6], results {'seat 3': 8, 'seat 2': 7, 'seat 4': 4, 'seat 1': 15, 'seat 5': 3, 'seat 6': 3}, 169-271 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 217.7 decisions, prompts of 169 characters on average (longest 216)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 3': 10, 'seat 2': 16, 'seat 4': 13, 'seat 1': 19, 'seats 1 and 3': 1, 'seats 2 and 4': 1}
- always `first@seat1`: won 0, lost 60, drew 0
- always `first@seat2`: won 0, lost 60, drew 0
- always `last@seat1`: won 0, lost 60, drew 0
- always `last@seat2`: won 0, lost 60, drew 0

## Triage (whose problem each failure was)

- round 1: fix_tests: In every failing scenario the game's chips and pot are correct for the moves it actually received. In the Bet 3 case seat 1 bet 3, everyone else folded and seat 1 called, so as sole caller it rightly won the 7-chip pot and ended on 43. The tests expected the state you would get if the bettor had folded at the call step (36 chips, pot 7 carried over), but they never scripted that fold; they relied on the 'decline' default and on the hand stopping halfway.

## Choices the rules did not make

- 4 to 6 players, suggested 4: Kept from the source and the designer. Four is the smallest table where several opponents' cards give real information about your own and where there are rivals to bluff. Above 6, each player's card information and message get lost in a long conversation.
- Talk kept as a simultaneous poll broadcast to all: The rules require simultaneous messages. Talk earns its place: each player knows facts the others need (their cards) and has reason to lie about them, so following a claim can cost chips.
- Card strength encoded as a number from 1 to 52 (rank_index*4 + suit_index): This lets the showdown winner be found by arithmetic (the highest card_value among callers) and exactly matches the rank-then-suit order in the rules.
- Eligibility check and early-end check placed at the start of each round, with a further end check after the showdown: Elimination happens at the start of a hand. Checking right after it stops a hand being played with a single active player.
- Strategy at the table: A thoughtful player infers their own card from the others' cards, their messages and their bets, and decides when to bluff, mislead others about their cards, or fold cheaply. A thoughtless player bets blindly.

## Simplifications

- Shuffling the full deck each hand is done by resetting the deck list to 52 cards and drawing at random: The engine has no shuffle; drawing at random from a full list is equivalent.
- The discarded leftover pot is simply ignored at the end: It does not affect anyone's chips or the ranking.
