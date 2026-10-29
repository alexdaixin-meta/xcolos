# cuttle: needs review

Built from the variation **Blind Scuttle** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- A 10 may scuttle a King: both go to scrap and the owner's King count drops by 1. Kings also lower the threshold less (by 8/6/4/3 instead of 7/4/3/2). (fixes: P2 Kings cannot be answered, so 'play a King at once' is dominant and the King deal decides games.): Playing a King becomes a timing decision: wait until the opponent's 10s are spent or scrapped. Holding a 10 in reserve becomes a plan.
- A Jack may steal any point card, of any rank. (fixes: P3 Jacks only steal rank 7 or less, so leading with the highest card is automatically safe and card order is not a decision.): High cards become the best targets, so leading greedily with 10s feeds the opponent's Jacks. Card order becomes a real trade-off.
- Base threshold raised to 30 (32 for the First player). Both players are dealt 6 cards, and the cap becomes 40 turns. (fixes: P4 The race is too short (3-6 rounds), so the deal swamps skill.): About 5+ net plays are needed, and scuttles and steals undo progress. Typical games should last 8+ rounds, so draws and decisions accumulate and the opening deal matters less.
- Point cards are laid face down showing only a band: Low 1-4, Mid 5-7, High 8-10. A scuttle names a target and succeeds only if the attacking rank is at least the hidden rank. A failed scuttle scraps the attacker's card and turns the target face up. (fixes: P5 Perfect information about laid points: nothing to infer, no bluff, scuttling is automatic.): Scuttling becomes a risky read that uses band information and public scrap counting. A player can weigh a safer Mid against a Jack-bait High. A player can also stack Mids, whose exact total the opponent must estimate.
- You win only if you are at or above your threshold at the START of your own turn, so the opponent always gets one turn to answer. The First player's base threshold is 32 against the Second's 30. (fixes: P1 Seat edge: the first mover's tempo advantage gives about 60-65% wins between equal greedy players.): Each crossing gets exactly one reply, whichever seat makes it. The 2-point handicap offsets the First player's half-turn of tempo, worth about half a typical 5-6 point play. The split should be checked by greedy-vs-greedy simulation and the handicap tuned to between 1 and 3 if needed.
- Each single turn is one engine round (40 turns = 20 per player). (fixes: P6 Two random draws per round would exceed the platform limit of one.): At most one card is drawn per engine round.

Objective: You win at the start of any of your own turns if your point total is at or above your threshold. If no one has won after turn 40, the smaller shortfall (threshold minus points, minimum 0) wins, and equal shortfalls are a draw.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. Deck: 40 point cards (ranks 1-10 x4, total 220 points, mean 5.5), 4 Jacks, 4 Kings. Hands are 6 each and the hand limit is 8.

VALUE OF ONE TURN, as a change in (my points minus opponent's points), where a King counts as points of threshold removed:
| Action | My change | Opponent's change | Net swi
- playable: pass. Rules completeness:
- Every action states its legality conditions: DRAW is barred at 8 cards or an empty pile; PASS is allowed only if you cannot draw; illegal choices become PASS.
- Scuttle resolution is a single comparison (equal or higher wins). The fail case reveals the target face up.
- King-sc
- reasoning_over_luck: pass. Things to infer and act on:
- Bands of face-down cards narrow a rank to 3-4 values.
- The scrap pile, face-up cards and your own hand are public or known. Card counting therefore gives exact probabilities, e.g. a 9 scuttling a High card succeeds only if the target is 8 or 9 among the unseen ranks.
-

## Complexity

- steps_per_round: designed 14, built 16, limit 20
- choice_steps_per_round: designed 1, built 3, limit 4
- attributes: designed 14, built 60, limit 20 (built: 80)
- hidden_elements: designed 3, built 20, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 40, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup deals 6 cards to each seat and leaves 36 in the draw pile
- pass: The First player acts on turn 1
- FAIL: The game stops after turn 40 and the smaller shortfall wins | rule R3 is broken: When the players alternate single turns, the game has at most 40 turns, numbered 1 to 40.; seat 2 standing: expected -30, got 970; seat 2 won: expected 0, got 1
- pass: First player with 1 King has threshold 24
- pass: First player with 3 Kings has threshold 14
- pass: First player with 4 Kings has threshold 11
- pass: Second player with 2 Kings has threshold 16
- pass: Second player with 4 Kings has threshold 9
- pass: Acting player at threshold at the start of the turn wins at once
- pass: Draw moves one card from draw pile to hand
- pass: Draw is not offered with 8 cards in hand
- pass: Points card goes face down showing only its band
- pass: Scuttle with a higher card removes the target and both go to scrap
- pass: Scuttle with a lower card scraps the attacker and the target stays
- pass: A 10 scuttles an opponent King and raises their threshold
- pass: A Jack steals an opponent point card
- pass: Placing a King lowers the threshold to the next table value
- pass: With an empty draw pile pass is offered and draw is not
- FAIL: An unparseable reply counts as pass and nothing changes | rule R15 is broken: When a reply is illegal or unparseable, then it counts as PASS and nothing changes.; seat 1 hand: expected 1 items, got 2; game draw_pile: expected 36 items, got 35
- FAIL: After turn 40 the smaller shortfall wins | rule R16 is broken: When turn 40 ends with no winner, then the player with the smaller max(threshold - points, 0) wins, and equal shortfalls are a draw.; seat 2 standing: expected -5, got 995; seat 2 won: expected 0, got 1
- FAIL: After turn 40 equal shortfalls share the result | rule R16 is broken: When turn 40 ends with no winner, then the player with the smaller max(threshold - points, 0) wins, and equal shortfalls are a draw.; seat 1 standing: expected -5, got 995; seat 2 standing: expected -5, got 995

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [2], results {'seat 1': 11, 'seat 2': 9}, 17-62 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 63.0 decisions, prompts of 313 characters on average (longest 431)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 1': 28, 'seat 2': 31, 'seats 1 and 2': 1}
- always `first@seat1`: won 0, lost 60, drew 0
- always `first@seat2`: won 0, lost 60, drew 0
- always `last@seat1`: won 34, lost 25, drew 1
- always `last@seat2`: won 47, lost 12, drew 1

## Triage (whose problem each failure was)

- round 1: fix_game: The scuttle and Jack scenarios crash inside the game's own bookkeeping: it reads `pile_ranks[target_index - 1]` from a list that does not hold the targeted card, so the lookup is out of range. The unparseable-reply scenario shows the game turning a bad reply into a DRAW (hand grew, draw pile shrank) when the rules say it counts as PASS and nothing changes. Both are faults in the file; the rules are clear and the platform can express them.
- round 1: fix_game: The rules say an illegal or unparseable reply counts as PASS, so nothing should change. When the test sent an unusable reply, the game resolved it to 'draw' and seat 1 drew a card (hand 1 to 2, draw pile 36 to 35). The likely cause is that the offer list is ['draw','points'] with no pass option, so the engine's fallback picked the first legal option.
- round 1: fix_game: In three end-of-game scenarios the file sets `won` = 1 for a player whose points (0) are below their threshold (30). So the start-of-turn win check, or an end-of-game step, writes `won` without the arithmetic condition. Separately, an unparseable reply was handled as DRAW (a card moved from the draw pile to the hand) instead of PASS.

## Choices the rules did not make

- Exactly 2 players, suggested 2: The designer fixed the game at two, and the asymmetric thresholds for First and second only make sense head to head.
- Card codes '1'..'10', 'J', 'K' and point-pile entries 'D<rank>' / 'U<rank>': Lists of text codes are needed to track face-down versus face-up cards and their ranks.
- A separate public point_pile_view beside the private point_pile: The opponent may see bands and face-up ranks but not face-down ranks, while the owner sees the exact ranks.
- One turn per round, with acting_seat alternating: Players take single alternating turns and the turn count is capped at 40.
- rank_by = won*1000 - shortfall: An immediate win outranks everything. Otherwise the smaller shortfall ranks higher, and equal values share the win, which models the draw.
- No talk step: The source has no communication. Players reason only from bands, the scrap pile and King counts.
- The King-scuttle and Jack card choices are not asked: The card used is fixed (a 10 or a J), and a King-scuttle target is just one of the opponent's Kings, which are interchangeable.

## Simplifications

- The top card of the draw pile is a random card from draw_pile: The engine draws at random from a list, which is equivalent to a shuffled pile.
- Placed Kings are tracked only by king_count, not as a list of cards: Kings have no identity beyond their count. When one is scuttled, a 'K' is appended to scrap.
- Only legal actions are offered, and any invalid reply becomes PASS: This follows the rule that an illegal choice counts as PASS and keeps the offers clean.

## Encoding attempts

- 1: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state a player is shown has empty fields (action, chosen_card); hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 2: it plays, but part of it does nothing: player attribute `won` is never changed in 3 random matches, so nothing updates it. Steps that name it: start of turn. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 3: passed
