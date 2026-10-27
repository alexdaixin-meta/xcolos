# sushi_go: ready for review

Built from the variation **Sushi Draft** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Remove chopsticks from the deck (104 cards remain, with the original proportions of everything else). (fixes: P1: Chopsticks needs a conditional second pick within a turn and returns the card into the hand being passed, which the flat step list cannot express cleanly. It also adds swingy extra picks.): Every turn becomes exactly one simultaneous pick, so no conditional block of steps is needed. A swingy luck source disappears.
- Restrict the game to 3 or 4 players (4 suggested): 9-card hands for 3 players and 8-card hands for 4. (fixes: P2: The 2-player game needs a special no-penalty pudding rule, and in 2 players the highest-total rule makes play pure hate-drafting. The 5-player game adds noise from passing chains and almost uses up the deck.): This avoids the special 2-player pudding rule and the degenerate head-to-head denial game. It keeps the deck sufficient and the number of rounds at 27 or fewer. With 4 players every hand passes each player twice, which rewards memory and inference.
- Spell out every scoring edge case: maki ties, unused wasabi, pudding ties including the case where all are tied, players with zero cards, and a final tie-break chain ending in a shared draw. (fixes: P3: The rules are vague in places: maki tie-breaking beyond the split, what happens when a wasabi never gets a nigiri, how ties for fewest pudding work, and how a final tie is resolved after the pudding tie-break.): The winner must follow by arithmetic with no interpretation left to a referee.
- Make each engine round one pick turn with a fixed sequence of steps. Hands are dealt only on the first pick of each hand (the single random draw that round). Set scoring happens only on the last pick of each hand, and pudding scoring only on the last pick of the game. (fixes: P4: Pick order and hand-size bookkeeping vary with player count, which raises build complexity and the number of steps.): This keeps the game to one choice, one random draw and about 17 steps per round, with conditions only on single steps.
- Each turn, publicly announce every player's face-up cards and the number of cards in each hand. Privately show each player their current hand. (fixes: P5: Moderate luck from the shuffle and from passing chains weakens how reliably skill decides the winner.): Players have everything needed to reason about neighbours' needs. Skill then shows in inference and denial rather than in tracking bookkeeping, which reduces noise from misreading the state.

Objective: After pudding scoring, the player with the highest score wins. If two or more players tie for the highest score, the one among them with the most puddings wins. If they are still tied, the game is a draw among those players.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. DECK CHECK: 14+14+14+6+12+8+10+5+5+10+6 = 104. Cards needed: 3 players x 9 x 3 hands = 81; 4 players x 8 x 3 hands = 96. Both fit in 104, so the deck never runs out.

PER-CARD VALUE TABLE (value if the set completes):
- Tempura: 2.5 per card, but 0 if it ends unpaired.
- Sashimi: 3.33 per card, but 
- playable: pass. RULES COVERAGE: every card has an explicit record rule.
- Wasabi: placement is automatic when unused wasabi is at least 1, which removes the original's choice ambiguity.
- Chopsticks: removed, which avoids a two-card pick.
- The last card is taken automatically.
- Maki: ties for first and second are
- reasoning_over_luck: pass. WHAT THERE IS TO INFER: with 3 players a 9-card hand returns to you after 3 picks. You see the hand's contents again and can deduce what each neighbour took, since all chosen cards are revealed. From that you can track:
- which sets each opponent is building (two sashimi means they want the third);


## Complexity

- steps_per_round: designed 17, built 12, limit 20
- choice_steps_per_round: designed 1, built 1, limit 4
- attributes: designed 13, built 57, limit 20 (built: 80)
- hidden_elements: designed 2, built 5, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 27, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: every seat starts at score 0 and puddings 0, hand 1, full 104-card deck
- pass: Deal with 4 players: 8 cards each leave the deck (72 left), one picked so 7 remain in hand (any cards)
- pass: Deal with 3 players: 9 cards each leave the deck (77 left), one picked so 8 remain in hand (any cards)
- pass: Deck is not reshuffled: after a full hand and the next deal, 104-32-32=40 cards remain
- pass: Every seat is asked to pick from its own hand only
- pass: A single card in hand is taken automatically with no question and the hand empties
- pass: A revealed pick leaves the hand and goes to the tableau
- pass: Tempura, Sashimi and Dumpling picks count toward their sets (2nd tempura 5, 3rd sashimi 10, 3rd dumpling 6)
- pass: Maki-3/1/1 add icons: totals 3,2,1,0 give 6 and 3
- pass: Pudding adds 1 and puddings survive the end of a hand
- pass: Wasabi picked earlier triples the next nigiri; passing decides who gets what
- pass: Nigiri without wasabi: Egg 1, Salmon 2, Squid 3
- pass: Nigiri on wasabi: Egg 3, Salmon 6, Squid 9
- pass: Remaining hand passes left: seat 1's leftover Pudding reaches seat 2
- pass: Tempura: 3 gives 5, 4 gives 10, 1 gives 0
- pass: Sashimi: 5 gives 10, 6 gives 20, 2 gives 0
- pass: Dumplings: 1,4,5,6 score 1,10,15,15
- pass: Nigiri points are scored; unused wasabi scores nothing
- pass: Three-way tie for most maki splits 6 as 2 each; no second place
- pass: Single maki leader gets 6; two tied seconds get floor(3/2)=1 each
- pass: Two tied for most maki get 3 each and the next player gets nothing
- pass: Players with 0 maki score no maki points even when only one other has maki
- pass: Hand counts reset after a hand (all-Wasabi second hand scores nothing) while puddings stay
- pass: End of game: sole pudding leader gets +6, two tied fewest get -3 each
- pass: End of game: two tied for most puddings get +3 each and share the win
- pass: End of game: 0 puddings counts as fewest; two seats at 0 get -3 each
- pass: End of game: equal puddings score nothing
- pass: Game ends after the last pick of hand 3 with 3 players (pick 27)
- pass: Game ends after the last pick of hand 3 with 4 players (pick 24)
- pass: Score tie broken by most puddings
- pass: Players tied on score and puddings share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 4], results {'seat 1': 15, 'seat 2': 9, 'seat 3': 10, 'seat 4': 6}, 61-82 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 78.0 decisions, prompts of 181 characters on average (longest 181)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 1': 21, 'seat 2': 22, 'seat 3': 16, 'seats 1 and 3': 1}
- always `first@seat1`: won 24, lost 36, drew 0
- always `first@seat2`: won 19, lost 41, drew 0
- always `last@seat1`: won 43, lost 17, drew 0
- always `last@seat2`: won 43, lost 17, drew 0

## Choices the rules did not make

- 3 to 4 players, suggested 4: The designer suggests 4, and hand sizes are defined only for 3 and 4. At 3, passing still creates drafting tension. Above 4 the rules give no hand size.
- No talk phase: The source says there is no talk phase. Drafting is decided by reading the visible tableaus and passed hands.
- Strategy at the table: A thoughtful player tracks what others are collecting and what will come back around, denies key cards to rivals, times wasabi before high nigiri, and weighs the pudding race against points in each hand.
- Tie-break encoded as score*100 + puddings: There are at most 10 puddings, so puddings can never outweigh one point of score. Players still tied share the win, matching the source's draw.
- Dumpling table written as m*(m+1)/2 with m = min(dumplings,5): This gives exactly 0, 1, 3, 6, 10, 15 and is pure arithmetic.

## Simplifications

- The left neighbour is the next seat number, wrapping to seat 1: The engine has no physical seating.
- Passing is done by rotating the hand lists between players in one update: The engine moves cards only through list operations.
- The automatic last pick is done as an update instead of a question: The rules take the single card without a choice.
