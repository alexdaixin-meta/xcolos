# da_bai_fen: needs review

Built from the variation **Da Bai Fen Lite** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- The deck shrinks to 30 cards: four suits of 5, 8, 10, J, Q, K, A plus two jokers. Each player gets 7 cards and 2 go to a face-down kitty. Point cards stay K=10, 10=10, 5=5, still 100 in total. (fixes: 54 cards, 12 tricks per deal and a level race from 2 to Ace make the game far too long for the 40-round cap.): Keeps the 100-point fight while making each deal 7 tricks long.
- There is no level system or trump rank. Trumps are the two jokers plus a trump suit that the hand's declarer names after seeing their own 7 cards. (fixes: Trump declaration during a one-by-one deal, where any holder may interrupt, is a real-time-like race that the engine cannot run in a few steps.): One single choice step replaces the interruptible exposure race. The declarer still reads their hand to choose trumps, as in the original.
- Only single-card leads are allowed. A player must follow suit if able, and trumps count as their own suit. (fixes: Multi-card leads require checking that no card in any hidden hand beats them; this is a long, error-prone rule chain.): Removes the multi-card legality check while keeping follow-suit inference and the value of being void in a suit.
- The kitty is never exchanged. Its points go to whichever team wins the last trick, and its cards are revealed only then. There are no redeals. (fixes: The kitty exchange (take 6, discard 6) and void-hand redeals add choice steps and conditional blocks the flat step list cannot support.): Keeps a hidden element and a reason to fight for the last trick, without extra choice steps.
- The match has 4 hands. The declarer rotates through all four seats, so each team declares twice. Each hand pays match points from a threshold table on the defenders' points. The higher match total wins, with card points as the tie-break. (fixes: A short session is dominated by deal luck (jokers, trump length), and the declaring role does not rotate evenly, so one team can gain a structural edge.): Balances the seats and spreads deal luck over four deals. The threshold table keeps the original's stay-or-flip character on the 40-point line.
- The winning card in each trick is decided by a numeric strength: rank, plus 10 if the card is in the led suit, plus 20 if it is a trump. The jokers have fixed top values. (fixes: 54 cards, 12 tricks per deal and a level race from 2 to Ace make the game far too long for the 40-round cap.): Lets the engine find the trick winner in one calculation step with no lookup table.

Objective: After hand 4, the team with more match points wins, and both its players win. If match points are equal, the team with the higher card-point total over all four hands wins. If that is also equal, the match is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. DECK ARITHMETIC. 4 suits x 7 = 28 cards, plus 2 jokers = 30. Points per suit are K 10 + 10 10 + 5 5 = 25, so 4 x 25 = 100. Deal: 4 x 7 = 28 cards in hands plus a 2-card kitty = 30. Seven tricks use 7 x 4 = 28 cards. All consistent.

STRENGTH TABLE (c). Jokers are 40 and 39. Trump-suit cards are 21 t
- playable: pass. COMPLETENESS. All of the following are fully specified:
- seats, teams and anticlockwise order
- deck, ranks and point values
- deal (7 each, 2 in the kitty, kitty unseen)
- trump naming by the fixed declarer of each hand
- the 'Trump suit' rule for following, with jokers belonging to it
- the follo
- reasoning_over_luck: pass. SKILLS THAT MATTER:
- choosing the trump suit from a 7-card hand
- counting the 9 trumps and the 100 points as they fall
- inferring voids from discards
- inferring the partner's holding from their plays, since no talk is allowed
- deciding when to lead trumps to draw them
- feeding K, 10 and 5 into

## Complexity

- steps_per_round: designed 16, built 14, limit 20
- choice_steps_per_round: designed 4, built 5, limit 4
- attributes: designed 18, built 71, limit 20 (built: 80)
- hidden_elements: designed 2, built 9, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 32, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Teams are NS for seats 1 and 3 and EW for seats 2 and 4
- pass: Deal gives 7 cards to each seat and 2 to the kitty (random deal, counts only)
- pass: In hand 2 seat 2 declares and names trumps
- pass: In hand 3 seat 3 declares and names trumps
- pass: In hand 4 seat 4 declares and names trumps
- pass: Declarer seat 1 names Diamonds as trumps in hand 1, and only the declarer is asked
- pass: Jokers and trump-suit cards form one Trump suit for following
- pass: A non-trump lead sets led suit to that suit; trump-suit cards do not follow it
- pass: Leading a trump-suit card sets led suit to Trump, so jokers must follow
- pass: A follower with no led-suit card is offered every card; a follower with one is offered only led-suit cards
- pass: Play goes anticlockwise from leader seat 3 and later seats follow the led suit
- pass: A low trump beats the led suit's ace and king; an off-suit card is weakest
- pass: Big Joker beats Small Joker, which beats the trump ace
- pass: The trick winner's team takes the points and the winner leads the next trick
- pass: The kitty's points go to the winner of the last trick (EW 5 + kitty 15 = 20)
- pass: Defenders on 15 points: the declaring team NS gains 3 match points
- pass: Defenders NS on 30 points: the declaring team EW gains 2 match points
- pass: Defenders EW on 50 points: the defending team gains 1 match point
- pass: Defenders NS on 60 points: the defending team gains 2 match points
- pass: Defenders EW on 85 points: the defending team gains 3 match points
- pass: Hand points add to the running card-point totals and reset to 0 when the next hand starts
- pass: After hand 4 the team with more match points (NS) wins
- pass: Match points level after hand 4: the team with more card points (EW) wins
- pass: Match points and card points both level after hand 4: all four seats share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [4], results {'seats 1 and 3': 20}, 4-4 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 4.0 decisions, prompts of 164 characters on average (longest 164)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- every random match ended 'seats 1 and 3': choices do not change the result
- random seats: {'seats 1 and 3': 60}
- always `first@seat1`: won 0, lost 0, drew 60
- always `first@seat2`: won 0, lost 60, drew 0
- always `last@seat1`: won 0, lost 0, drew 60
- always `last@seat2`: won 0, lost 60, drew 0

## Triage (whose problem each failure was)

- round 1: revise_rules: The game was built as specified, and evaluation found design flaws. Because the step list is flat, the declarer's trump-naming choice sits beside the four card plays and gives 5 choice steps per round, over the limit of 4. Every random match also ended as a win for seats 1 and 3, so the players' choices do not change the result.

## Choices the rules did not make

- 4 players (min = max = suggested = 4): The designer fixed two partnerships of two. Fewer seats break the teams, and more seats do not fit the 30-card deal of 7 each plus a 2-card kitty.
- No talk step: The rules forbid talk; signalling through card play is the skill. A thoughtful player tracks played trumps and points, smears points onto a partner's winning trick, and holds trumps back to capture kings and tens.
- Team scores are mirrored onto each player's match_points and card_points: The ranking expression works per player, so both partners carry the team's totals.
- Ranking expression match_points * 1000 + card_points: Card points can total at most 400, so match points always come first and card points break ties. A full tie makes all four seats share the win, which is the draw.
- Card codes such as 'S-K', 'H-10', 'BJ', 'SJ': The rules do not say how cards are labelled; codes let suit, rank and points be read arithmetically.

## Simplifications

- The 32 rounds run as one repeated step list, with `when` conditions on round_in_hand choosing the deal steps (round 1) or the trick steps (rounds 2 to 8): The step list is flat; a condition on each single step gives the same order.
- Legality of following suit is enforced by offering only legal cards, with a judged check as a backstop: The source rejects illegal plays and asks again; offering only legal cards has the same effect.
- A draw is shown as all four seats sharing the win: The engine has no separate draw outcome.

## Encoding attempts

- 1: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (led_suit, trump_suit) in `your_hand`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 2: it plays, but part of it does nothing: game attribute `full_deck` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 3: passed
