# quadrille: needs review

Built from the variation **Concealed Quadrille** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Encode every card as a number: code = 10 x suit + rank, with suits Spades 1, Clubs 2, Hearts 3, Diamonds 4 and ranks A 1, 2 2, J 3, Q 4, K 5. Spadille is 11 and Baste is 21. A card's power is then ONE formula applied to all four played cards in a single step: 30 if code 11; 28 if code 21; 29 if code = 10t+2 (Manille); 20+rank if its suit is trump t; rank if its suit is the led suit; else 0. The winner is one argmax step. (fixes: P1 Step budget): Replaces six-way category branching with a single arithmetic calc. The rank codes double as plain-card power, so no table is needed.
- Score a hand in two steps: one calc for d = B-1 if T>=B, -(B-1) if T=B-1, else -B. Then one update applying +3d (solo Taker) or +d (call side) or -d (others) through per-player if-conditions. (fixes: P2 Hand scoring): Collapses 6 scoring cases into 2 steps.
- Drop the hidden running count T. Each player instead has a public 'hand tricks' count, since who wins each trick is announced anyway. At the end of the hand, T = hand tricks of the Taker plus hand tricks of the partner, with the partner counted only if a different seat. (fixes: P4 Hidden T and P3 Misreported complexity): Removes a per-trick hidden conditional update and one hidden element. The information is unchanged, because defenders still do not know which count belongs to the Taker's side.
- Provide an explicit numbered step list, with each start-of-hand and end-of-hand step guarded by a 'when' condition on the trick number. The total is 18 steps, 4 choice steps, 16 attributes, 2 hidden elements (hands, partner identity) and 1 random draw (the deal, first trick of a hand only). (fixes: P3 Misreported complexity): Makes the budget verifiable and the report honest.

Objective: After round 40, the player with the highest score wins. If several tie for the highest score, the one among them with the most tricks won over the whole game wins. If that also ties, the game is a draw.

## The critic (3 review(s) before the rules went to a coder)

- balanced: pass. PAYOFF TABLE (side delta d per hand; call: Taker and partner +d each, the other two -d each; solo: Taker +3d, the others -d each). B=3: made (T>=3) +2, remise (T=2) -2, codille (T<=1) -3. B=4: +3, -3 (T=3), -4 (T<=2). B=5: +4, -4 (T=4), -5 (T<=3). Solo B=3 pays the Taker +6, -6 or -9. Each hand sums
- playable: pass. COMPLETENESS: the rules fully specify the following. The pack and codes: 20 cards, all dealt 5 each. The bid: a simultaneous poll with tie-break key bid*10+(4-((seat-priority) mod 4)); Pass=0 gives a key of at most 4, below 30, so an all-pass correctly falls to the priority seat with B=3. The declar
- reasoning_over_luck: pass. WHAT DECIDES IT: the deal sets hand strength. Skill then acts at five points. (1) Selective bidding: take contracts only with trump length or top trumps. Opting out is possible except in a forced all-pass, about 2 hands per seat at most. (2) Choosing trump and a partner from the public simultaneous 

## Complexity

- steps_per_round: designed 18, built 16, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 16, built 57, limit 20 (built: 80)
- hidden_elements: designed 2, built 27, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 40, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: R1 deck holds the 20 cards before any deal
- pass: R2 game ends after round 40 and highest score wins
- pass: R3 priority seat of hand 2 is seat 2 (all pass)
- pass: R3 priority seat of hand 4 is seat 4 (all pass)
- pass: R4 each seat is dealt 5 cards, deck emptied (one card played after)
- pass: R5 every seat is offered Pass, 3, 4 and 5
- pass: R6 highest bid takes the contract
- pass: R6 tie with priority 1 goes to seat 2 over seat 3
- pass: R6 tie with priority 3 goes to seat 4 over seat 1
- pass: R7 all pass in hand 1: seat 1 takes contract 3
- FAIL: R8 Taker's chosen trump suit is set | rule R8 is broken: The Taker privately chooses a trump suit and a partner seat from 16 options, and the trump suit is announced to all.; game trump: expected 3, got 1
- pass: R9 named seat is the partner and shares the made contract
- pass: R10 solo: other seats' tricks do not help the Taker
- pass: R11 mid-hand trick changes no scores
- pass: R12 Manille (2 of trump) beats Baste and trump King
- FAIL: R12 Baste is not a club: seat without clubs may play any card | rule R12 is broken: The trumps are every card of the trump suit plus 11 and 21; 11 and 21 count only as the trump suit, and Manille is code 10*trump+2.; seat 2 was never offered 'Jack of Hearts', but should have been
- pass: R13 previous trick winner leads a later trick
- pass: R14 leading Spadille makes trump the led suit
- pass: R15 Baste counts as trump and must follow a trump lead
- pass: R15 a seat holding the led suit must follow it
- FAIL: R16 a seat void in the led suit may trump | rule R16 is broken: A player holding no card of the led suit may play any card, and illegal cards are never accepted.; seat 2 was never offered 'Queen of Diamonds', but should have been
- pass: R17 Spadille beats Manille and Baste
- pass: R17 a trump beats a higher card of the led suit
- pass: R17 highest card of the led suit wins without trumps
- pass: R18 trick winner gains 1 tricks_won and 1 hand_tricks
- pass: R19 partner's tricks count toward T in a call
- pass: R20 made: T=4 of contract 4 gives d=3
- pass: R20 remise: T=3 of contract 4 gives d=-3
- pass: R20 codille: T=3 of contract 5 gives d=-5
- pass: R21 call: Taker and partner gain d, others lose d, added to running scores
- pass: R22 solo made: Taker gains 3d, others lose d
- pass: R22 solo codille: Taker loses 12, others gain 4
- pass: R23 scores are updated at hand end
- pass: R24 no talk option is ever offered
- pass: R25 tie on score broken by tricks_won
- pass: R25 level on score and tricks_won share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [4], results {'seat 4': 4, 'seat 3': 6, 'seat 2': 4, 'seat 1': 6}, 122-139 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 200.0 decisions, prompts of 208 characters on average (longest 338)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 4': 13, 'seat 3': 15, 'seat 2': 12, 'seat 1': 20}
- always `first@seat1`: won 41, lost 19, drew 0
- always `first@seat2`: won 38, lost 22, drew 0
- always `last@seat1`: won 0, lost 60, drew 0
- always `last@seat2`: won 1, lost 59, drew 0

## Triage (whose problem each failure was)

- round 1: fix_game: Two independent tests show the follow poll offering too few cards. In one a seat with no club is denied the Jack of Hearts when Baste is led; in the other a seat void in the led suit is denied a trump. That is a bug in the legality filter, not in the rules. The trump test also got Spades (1) stored where Hearts (3) was expected, which points to the declaration options or how the chosen option is turned into `trump`.
- round 1: fix_game: Each attempt failed on a different coder mistake: bookkeeping fields shown to players, a list comprehension using range (not an allowed function), reading `you` outside a per-player context, and extra constant attributes that no step ever changes. None of these comes from the rules, which the engine can express with flat steps, `when` conditions and simultaneous polls.
- round 1: fix_game: All three failures point at what the game offers and records during the declaration and the follow. The Taker's trump choice did not end up as the intended suit: the move actually played was the first option, 'Spades, partner seat 1', which suggests the scripted Hearts declaration was not among the options as offered. A seat that should be free to play any card (void in the led suit, with Spadille and Baste counted only as trump) was never offered that card. The rules are clear and expressible, so the file's option building and legality filter are at fault.

## Choices the rules did not make

- 4 players, fixed: The designer set 4. The deck (20 cards = 4 x 5), the partner call and the priority rotation are all built for exactly four seats.
- No talk phase: The rules forbid discussion; bids and cards are the only signals. A player's strategy lies in bidding to hand strength, choosing a partner who likely holds key trumps, and inferring the hidden partner from play.
- Ranking expression score*100 + tricks_won: tricks_won is at most 40 (under 100), so score dominates and tricks_won only breaks ties; players still level share the win, which serves as the draw.
- Card power stored as public player attributes: Power is computed only from public played cards, so showing it reveals nothing new.

## Simplifications

- The deck is rebuilt from all 20 codes at the start of each hand instead of physically gathering the cards: This is equivalent to gathering and shuffling, since all 20 cards are always played out over the 5 tricks.
- Hand-start and hand-end steps run in every round, gated by conditions on trick_in_hand: The engine's step list is flat; per-step conditions reproduce the source's 'first trick' and 'fifth trick' steps.

## Encoding attempts

- 1: players are sent text with a `{name}` that was never filled in: placeholder: players are shown the literal {hand_view} (in `prompt`: 'You lead trick 1 of hand 1. Trump is Diamonds. Play any card from your hand by its code (y'); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {hand_view} (in `prompt`: 'You lead trick 2 of hand 1. Trump is Diamonds. Play any card from your hand by its code (y'); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {hand_view} (in `prompt`: 'You lead trick 3 of hand 1. Trump is Diamonds. Play any card from your hand by its code (y'); use only names the step can fill in (see the broadcast rule: {value} and {seat})
- 2: passed
