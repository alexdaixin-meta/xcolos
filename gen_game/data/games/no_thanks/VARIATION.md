# Variation: No Thanks! (Two-Lap)

No Thanks! for 3 to 4 players with a 20-card deck. A card that goes twice around the table untaken is burned, and its chips roll onto the next card. Offer order and take effects are stated exactly.

Players: 3 to 4, best with 4

## Review of the original

No Thanks! is a push-your-luck card game for 3 to 5 players. A numbered card is offered around the table, and each player either takes it with the chips piled on it or pays one chip to pass it on. Runs of consecutive cards score only their lowest number, chips left in hand subtract from the score, and the lowest score wins.

- **non_degenerate**: good. Every simple policy can lose. 'Always pay' runs out of chips within about 11 offers and is then forced to take every card it is offered, often with high card values. 'Always take' grabs every card it is offered with small pots and ends with a high sum and no chips. 'Take only when the pot is at least the card value' almost never takes early and is forced into the same high cards once its chips are gone. There are three or more players and the lowest score wins, so the two-player 'difference only' trap does not apply. The first seat decides first on card 1 only; after that, leading moves to whoever took.
- **skill_sensitive**: good. The card order is random, but the decisions repeat about 20 times. These decisions are when to stop paying, how far to let a pot grow on a card that fits your run, and whether to deny a card that fits a rival's run. Their effects add up, so a careful player beats a careless one reliably over a game.
- **headroom**: good. Weak play still scores: you can simply take low cards. Strong play keeps improving through several skills. These are: counting rivals' chips from the public pays; estimating which cards were removed; and timing a take so a rival who must pay is drained.
- **reasoning_dependent**: good. Three things are hidden: the removed cards, the deck order, and opponents' chips (shown only to their owner, but they can be inferred from the public pays). Players must infer whether a rival can afford to keep passing, and whether a card that would bridge a run still exists.
- **verifiable**: good. Score = sum of the lowest card in each run, minus chips left. This is pure arithmetic on tracked numbers.
- **fits_platform**: weak. The game is text-only and turn-based, but the original has two problems. First, a single card can circle the table without limit, which breaks a 40-round cap. Second, with 5 players a lap is 5 choice steps, above the limit of 4. The previous build also failed two tests because TAKE was never offered to the right seat. The tests are correct as written. The rules did not state the offer order and gating precisely enough, so the builder produced the wrong sequence.

## Problems

- P1: The previous rules did not pin down exactly which seat receives offer k. They also did not say that TAKE is offered unconditionally. The build never put TAKE to some seats, and the 'lead 3 gives 3, 4, 1' scenario failed.
- P2: After a TAKE, the rules did not say clearly that the remaining offers that round are skipped (gated on current_card != 0), or that the taker becomes lead_seat.
- P3: In the original, a card can circle indefinitely, so the game has no bounded length within the 40-round cap.
- P4: Five players means five sequential choices per lap, above the limit of 4 choice steps per round.
- P5: The original's score needs run detection at the end, which costs many steps. It must be kept as an incremental card_points total instead.

## Changes

- Rules now give the exact formula for each offer step. For k = 1..N, offer k goes to seat ((lead_seat - 1 + k - 1) mod N) + 1, read from the lead_seat attribute. A worked example is included (lead 3 with 4 players gives 3, 4, 1, 2). TAKE is always offered, gated only on current_card != 0. PAY is offered only when the seat has chips >= 1. The option names are exactly 'TAKE' and 'PAY'. (fixes: P1: The previous rules did not pin down exactly which seat receives offer k.): This removes any room for hard-coding seat 1 first or for gating TAKE on the wrong condition.
- The TAKE effect is spelled out as an ordered list of updates: tableau, card_points, chips += pot, pot = 0, current_card = 0, lap_count = 0, lead_seat = taker. Every later offer in the round is gated on current_card != 0. (fixes: P2: After a TAKE, the rules did not say clearly that the remaining offers that round are skipped.): This makes the end of a trick on TAKE explicit and testable.
- One round is one lap around the table. If a card completes 2 laps with nobody taking it, it is burned: it moves to the public burned list, and its pot stays in the middle for the next card. (fixes: P3: In the original, a card can circle indefinitely.): This bounds the game at 20 cards × 2 laps = 40 rounds. Carrying the pot forward keeps the tension: refusing a card makes the next card richer.
- The player count is limited to 3 to 4. (fixes: P4: Five players means five sequential choices per lap.): This keeps a lap to at most 4 choice steps.
- card_points is updated when each card is taken. Add c, subtract c+1 if c+1 is already held, and subtract c if c-1 is already held. The running total then always equals the sum of the lowest card of each run. (fixes: P5: The original's score needs run detection at the end.): This gives correct run scoring with one update step and no end-game scan.
- The deck is 20 of the cards 3 to 35, with 13 cards removed face-down. (fixes: P3: In the original, a card can circle indefinitely.): More removed cards mean more uncertainty about runs. It also matches the 40-round bound in P3.

## Kept from the original

- The core take-or-pay-one-chip decision with a growing pot
- Runs score only their lowest card
- Chips left in hand reduce your score; the lowest score wins
- Hidden removed cards and privately held chips
- The taker flips the next card and decides first

## The variation's rules

SETUP. Seats are numbered 1 to N (N = 3 or 4), and clockwise means seat s is followed by seat s+1, with seat N followed by seat 1. Shuffle the 33 cards numbered 3 to 35. Put 20 of them face-down in the deck in random order. Put the other 13 in a hidden 'removed' list that no player ever sees. Each player starts with chips = 11 (visible only to that player), an empty tableau (public) and card_points = 0. The game state starts with current_card = 0 (meaning no card on offer), pot = 0, lap_count = 0, lead_seat = 1 and an empty public 'burned' list. The pay cost is always 1 chip.

EACH ROUND (one lap), in this order:

Step 1, DRAW. If current_card = 0 and the deck is not empty, move the top deck card to current_card and announce it. The pot is NOT reset; any chips already in the pot stay with the new card.

Step 2, OFFERS. Make up to N offer steps, for k = 1, 2, ..., N. Offer k goes to the seat k-1 places clockwise from lead_seat, that is seat ((lead_seat - 1 + k - 1) mod N) + 1. Always read the current lead_seat value; it need not be 1. For example, with lead_seat = 3 and N = 4 the order is 3, 4, 1, 2, and with lead_seat = 3 and N = 3 it is 3, 1, 2. An offer step happens only if current_card != 0; otherwise it is skipped. The offered seat sees current_card, the pot, every tableau, the burned list and its own chips. Its options are named exactly 'TAKE' and 'PAY'. TAKE is always offered. PAY is offered only if that seat has chips >= 1; a seat with 0 chips must TAKE.
- PAY: the seat's chips decrease by 1 and the pot increases by 1. Play passes to the next offer step.
- TAKE: apply these updates in order. (a) Let c = current_card. (b) Add c to card_points. If card c+1 is already in this seat's tableau, subtract c+1. If card c-1 is already in this seat's tableau, subtract c. (c) Append c to the seat's tableau. (d) Add the pot to the seat's chips and set pot = 0. (e) Set current_card = 0, lap_count = 0 and lead_seat = this seat. Because current_card is now 0, all remaining offer steps this round are skipped.

Step 3, LAP. If current_card != 0 (nobody took it this lap), increase lap_count by 1.

Step 4, BURN. If current_card != 0 and lap_count >= 2, append current_card to the burned list, then set current_card = 0 and lap_count = 0. The pot stays as it is and lead_seat is unchanged.

Step 5, END CHECK. If current_card = 0 and the deck is empty, the game ends. The game can last at most 40 rounds.

SCORING. Each player's final score = card_points - chips. card_points always equals the sum of the lowest card of each run of consecutive numbers in the tableau. All chips and tableaus are revealed at the end.

There is no talk phase.

Objective: The lowest final score (card_points minus chips) wins. If two or more players tie for lowest, the game is a draw among them.

Expected effect: Play matches classic No Thanks!. Players decide when a growing pot is worth a bad card, which cards extend their own runs, and when to deny a rival's bridge card. They also judge whether a low-chip rival is about to be forced to take. The two-lap burn rule adds a choice: let a card die so its pot boosts the next draw, or grab it now. Talk is left out for two reasons. A message phase would push the round above 4 choice steps. And with no trading or binding deals, talk would add little beyond cheap bluffing. The rival tension already comes from the private chips and the single-winner rule. The explicit offer formula and gating should make the build pass the 'taker collects the pot' and 'lead 3: 3, 4, 1' scenarios.

## Complexity (the designer's count, against the limits)

- steps_per_round: 8 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 10 (limit 20)
- hidden_elements: 3 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 40 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
