# officers_schafkopf: ready for review

Built from the variation **Blind Officers' Schafkopf** (design round 2); see VARIATION.md.

## What was changed from the original, and why

- Replace the stacks with 8-card concealed hands. The remaining 8 cards become an unseen Blind that is never played. (fixes: The face-up/face-down stack layout needs positional tracking of 16 stacks, which exceeds the attribute and step limits and behaves like a small board.): This removes positional state and creates genuine hidden information. No one knows which 8 cards are out of play, so players must infer the opponent's hand from bids and play.
- Use a 24-card deck (Ace, Ten, King, Ober, Unter, Nine in four suits; 120 card points) with concealed hands and a Blind. (fixes: With many face-up cards there is little hidden information to reason about once play is under way.): This keeps the deck clean and makes the unknown cards the core of the reasoning.
- Play a match of four hands of 8 tricks each (32 rounds), scored in match points with stakes set by contract level and the double. (fixes: A single hand is largely decided by the deal, so luck dominates one game.): Several deals average out card luck. The match score creates planning across hands, such as a trailing player taking on Strong contracts.
- Use a simultaneous sealed bid with Strong above Simple above Pass. Priority breaks same-level ties and alternates by hand. The defender keeps the option to double. (fixes: The ordered announce-then-double sequence gives the non-dealer a fixed seat edge within a hand.): This removes the fixed announcer edge and makes each player predict the other's hand strength.
- State the bid poll as exactly eleven options and list all eleven explicitly. (fixes: The previous variation's bid step said 'one of nine options' but listed eleven, so the legal option list for the simultaneous poll was ambiguous.): The count and the list now agree, so the legal option set is exact.

Objective: After the fourth hand, the player with more match points wins. Equal match points is a draw.

## The critic (3 review(s) before the rules went to a coder)

- balanced: pass. Deck check: each suit has 11+10+4+3+2+0 = 30 points, and 4 x 30 = 120, as stated. Only 16 of the 24 cards are played, so the points in play average 80 and vary from deal to deal. Both thresholds are relative to those points: Simple needs D >= F+10, about 45 of 80. Strong needs D >= 2F and D >= 30, a
- playable: pass. Rules are complete and unambiguous:
- Card ranks and points are specified for Wenz, Solo and Ramsch.
- Obers and Unters are removed from the plain suits in a Solo; Unters only in Wenz and Ramsch. The plain orders (A>10>K>O>9 in Wenz, A>10>K>9 in Solo) are given.
- The 12 trumps are listed in order: 
- reasoning_over_luck: pass. The deal is a large source of variance: hand quality and the unseen Blind. Over only 4 hands with stakes of 2, 4 or 8, I estimate chance at roughly 40-50% of match outcomes between equally skilled players. That is typical of trick-taking games, and skill still clearly matters:
- Bidding: choosing th

## Complexity

- steps_per_round: designed 15, built 14, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 18, built 66, limit 20 (built: 80)
- hidden_elements: designed 3, built 11, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 32, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Deal: each seat gets 8 cards, 8 go to the blind, the deck is left empty (one trick played, so 7 cards remain in each hand)
- pass: Hand 2: seat 2 has priority, so equal Simple bids go to seat 2
- pass: Both seats are offered all bid options
- pass: Both pass: Ramsch with no declarer and no double question
- pass: Strong beats Simple even against the priority seat
- pass: Simple against Pass: the Simple bidder declares
- pass: Hand 1: equal Strong bids go to priority seat 1
- pass: Resolved contract and declarer are set after the bids
- pass: Only the defender is asked Double or No double
- pass: Wenz: an Ober is a plain card and beats a Nine of its suit
- pass: Wenz: an Unter is a trump and beats a led Ace
- pass: Ramsch: Acorns Unter outranks Leaves Unter
- pass: Hearts solo: Bells Ober is a trump above Hearts Ace
- pass: Hearts solo: Bells Unter beats Hearts Nine (both trumps)
- pass: First trick: the declarer (seat 2) is set up to lead (only the declarer is observable; chance hides the cards)
- pass: The winner of a trick leads the next one
- pass: Trump led: a follower holding a trump must play one
- pass: Plain suit led: must follow with a non-trump of that suit (the trump Ober of the suit does not count)
- pass: Cannot follow: any card may be played, a discard loses
- pass: A trump played on a plain lead wins the trick
- pass: Trick winner adds both cards' points to its total
- pass: After a trick both card_points totals reflect the result
- pass: Simple made at exactly D = F + 10: declarer gains 2, hand advances
- pass: Simple missed by one point (D = F + 9): defender gains 2
- pass: Strong made at D = 2F = 40: declarer seat 2 gains 4
- pass: Strong fails below 30 points even with F = 0: defender gains 4
- pass: Failed Simple contract: the defender's match points rise by 2
- pass: Doubled Strong contract made: declarer gains 8
- pass: Ramsch: the seat with fewer card points gains 1
- pass: Ramsch tied on card points: nobody scores
- pass: End of hand resets both card_points to 0
- pass: Match ends after hand 4: more match points wins
- pass: Match ends level on match points: both share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [2], results {'seat 1': 9, 'seat 2': 8, 'seats 1 and 2': 3}, 56-64 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 76.0 decisions, prompts of 307 characters on average (longest 429)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 1': 24, 'seat 2': 27, 'seats 1 and 2': 9}
- always `first@seat1`: won 44, lost 12, drew 4
- always `first@seat2`: won 42, lost 13, drew 5
- always `last@seat1`: won 13, lost 39, drew 8
- always `last@seat2`: won 14, lost 39, drew 7

## Triage (whose problem each failure was)

- round 1: fix_game: The R1 test is correct. In Acorns Solo, Ober of Bells (trump strength 17) beats Unter of Hearts (14), so seat 2 should take the 5 points (49+5=54) and seat 1 stays at 50, below the 53 bid. The game gave the trick to seat 1, and the R12 failures show the same fault: trick resolution ignores the trump strengths.
- round 1: fix_tests: The full-play tests (R2, R3) start from a real deal and ran without error, so trick play itself works. Only the four scenarios that inject a mid-hand state crashed. Those scenarios use internal names the test writer guessed (round_in_hand, leader, follower, hand, stack1_up, hand_points, a 'led card'), so the game's own bookkeeping, such as its led_card, did not match a card in its card table.
- round 1: revise_rules: The game was built faithfully, but the design exceeds the platform's budgets: 5 choice steps per round against a limit of 4, and 87 attributes against a limit of 80. It also has a degenerate strategy: always picking the first option wins about 70% of games for either seat, and always picking the last option loses over 80%.

## Choices the rules did not make

- 2 players, as the designer set: The source is written for exactly 2 players (priority, declarer against defender). Its core is reading the opponent's sealed bid and hand strength, which works at 2. More seats would break the declarer/defender structure.
- No table talk step: The rules have none, and with 2 opposed players talk would only add words.
- Card naming as '<Suit> <Rank>': Lets the suit and rank be read from the card's name for the follow rule, strength and points.
- Trick winner decided by a numeric strength: Trump strength is 100 plus a position score from the ordered trump_list, plain led-suit cards score their rank, and others score 0. This is an arithmetic version of the stated ranking rules.
- Hand bookkeeping driven by trick_number and hand_number with per-step 'when' conditions: The start-of-hand and end-of-hand steps run only on the first and eighth trick of each hand, without needing alternative blocks.

## Simplifications

- Follow-suit legality is enforced by restricting the offered options rather than by a penalty: The engine offers a seat only what it may do, so illegal plays cannot occur.
- Card point values and plain ranks are applied by rank name instead of a lookup table: The engine has no lookup operation; a small conditional on the rank word is equivalent.

## Encoding attempts

- 1: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (contract, follow_card, last_result, led_card) in `your_cards`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 2: it plays, but part of it does nothing: game attribute `all_cards` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `suit_names` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `index_list` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 3: passed
