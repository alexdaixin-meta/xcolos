# Variation: No Thanks! (Bounded Laps)

No Thanks! for 3-4 players. A card that goes twice round the table unclaimed is burned, its chips carry to the next card, and run scoring is computed incrementally.

Players: 3 to 4, best with 4

## Review of the original

No Thanks! is a 3-5 player push-your-luck card game. A face-up card collects chips as players pay one chip each to refuse it, until someone takes the card and its chips. Runs of consecutive cards score only their lowest number, unspent chips subtract from your score, and the lowest score wins.

- **non_degenerate**: good. Always TAKE collects nearly every card, scores well over 150 points and loses. Always PAY runs out of chips around card 11 and is then forced to take every later card, including the high ones, with no chips left to offset them. Seat order matters only a little, because the lead passes to whoever takes. With 3 or more players and a lowest-score-wins rule, one rival's loss is not automatically another's gain.
- **skill_sensitive**: good. Good play beats weak play reliably. It means milking a card you plan to take anyway, taking a card that extends your run, and forcing chip-poor opponents to eat high cards. The order of the cards is random, but every player faces the same card, so the draw rarely decides the game on its own.
- **headroom**: good. Novices can still finish with moderate scores. Experts keep improving at reading opponents' chip counts, judging how long a card can be milked, and judging when a run can still be completed given the removed cards.
- **reasoning_dependent**: good. Chip counts are hidden and must be inferred from paying history. The removed cards are unknown, so a gap in a run may never be fillable. Each card needs an opponent model: will they pass this back to me with more chips on it, or take it?
- **verifiable**: good. The score is pure arithmetic: the sum of the lowest card of each run, minus chips. The lowest score wins. No judgement is needed.
- **fits_platform**: weak. It is turn-based and text-only, but the original has unbounded passing laps and up to 5 sequential offers per card (the limit is 4 choice steps per round). In the previous build, a card stayed current over several rounds and the offer and draw steps were conditioned wrongly. After an all-PAY lap the game stopped offering TAKE, so test R11 failed.

## Problems

- P1: In the original, a card can circle forever while everyone pays, so the number of rounds is unbounded and the 40-round limit can be broken.
- P2: With 5 players, one lap needs 5 sequential choices, more than the 4 choice steps allowed per round.
- P3: In the previous build, after a full all-PAY lap the next round's offers were not made. Seats were never shown TAKE, so test R11 failed. The cause was that the offer steps and the draw step were gated on lap or draw state instead of only on whether a card is current.
- P4: The previous variation had two lap parameters (laps_to_stay = 1 and laps_to_burn = 2) that describe the same event. This invited contradictory conditions in the end-of-round step.
- P5: Run scoring ('lowest number of each run') needs a calculation over the whole tableau, which is fragile to build. It needs an incremental arithmetic form.
- P6: 'The taker flips the next card and decides first' must happen in the next round, with a clear lead-seat rule. Otherwise the engine skips or reorders seats.

## Changes

- Each round is at most one lap of offers on the current card. If everyone pays, lap_count goes up by 1. After laps_to_burn = 2 full all-PAY laps, the card is burned (removed from play unscored), its pot stays in the middle for the next card, and the lead seat moves one place clockwise. The deck has 20 cards, so the game lasts at most 20 x 2 = 40 rounds. (fixes: P1): This bounds the game length while keeping 'pay to refuse' tension. The pot carried over from a burned card makes the next card more tempting.
- The player count is set to 3-4. (fixes: P2): A lap is then at most 4 sequential choice steps.
- The rules now state the order of operations exactly. Offer step k goes to the k-th seat clockwise from lead_seat, and its only condition is that a card is current (current_card is not 0). TAKE is always offered. PAY is offered only if the seat has at least pay_cost chips. The draw step runs only when current_card is 0. The end-of-lap step runs only if the card is still current after all offers. When lap_count becomes 1, nothing else changes: same card, same pot, same lead seat. (fixes: P3): This removes the conditions that suppressed the offers after the first all-PAY lap. The tests written from the rules (R1-R4, R11) are correct and match these rules.
- The rules use one lap parameter, laps_to_burn = 2, plus pay_cost = 1. Both are stored as game attributes. (fixes: P4): Removing the redundant parameter leaves a single, unambiguous burn condition.
- Card points are updated incrementally when a card c is taken: add c, subtract (c+1) if c+1 is already in the tableau, and subtract c if c-1 is already in the tableau. (fixes: P5): This always equals 'sum of the lowest card of each run' and needs only membership checks and one arithmetic update. Example: holding 10 and 12, then taking 11, gives 11 - 12 - 11 = -12, so the points go from 22 to 10, which is correct.
- Whoever takes a card becomes lead_seat. The rest of that round's offers are skipped. The next round draws a new card and offers it to the taker first. (fixes: P6): This keeps the original 'taker decides first on the next card' as a clean between-round rule.

## Kept from the original

- Cards 3-35 with some removed unseen, so a run gap may be unfillable.
- The core choice: pay one chip to refuse the card, or take the card and all the chips on it.
- Hidden chip counts.
- Runs score only their lowest card, and leftover chips subtract from the score.
- Lowest final score wins.
- The taker decides first on the next card.

## The variation's rules

SETUP. (R1) Take the 33 cards numbered 3 to 35. Remove 13 of them at random, unseen by anyone; they stay hidden all game. The other 20 cards, shuffled, form the deck. (R2) Each player starts with 11 chips, an empty tableau and 0 card points. A player's chip count is visible only to that player. Tableaus, the current card, the pot and the number of burned cards are public. (R3) Game state: current_card = 0 (meaning no card), pot = 0, lap_count = 0, lead_seat = 1, an empty burned list, pay_cost = 1, laps_to_burn = 2. Seats are numbered 1 to N clockwise.

EACH ROUND, in this exact order:

Step 1, DRAW (R4). Only if current_card = 0 and the deck is not empty: draw the top deck card at random, make it current_card, and set lap_count = 0. The pot is NOT changed, so it may hold chips left over from a burned card. If current_card is not 0, skip this step: the same card and pot continue.

Step 2, ANNOUNCE. Show everyone the current card, the pot, every tableau, the number of cards left in the deck and the number of burned cards.

Steps 3 to 6, OFFERS (R5). Offer k (k = 1 to N) goes to the seat k-1 places clockwise from lead_seat. Make an offer only while current_card is not 0. The options are TAKE (always offered) and PAY (offered only if that seat has at least pay_cost = 1 chip).
- PAY: the seat moves 1 chip from its hand into the pot.
- TAKE: the seat adds the current card c to its tableau. Its card points change by c, minus (c+1) if c+1 was already in its tableau, minus c if c-1 was already in its tableau. It gains all chips in the pot, and the pot becomes 0. Then current_card becomes 0 and lead_seat becomes the taker's seat. No further offers are made this round.

Step 7, END OF LAP (R11). Only if current_card is still not 0 (everyone paid): add 1 to lap_count.
- If lap_count is now less than laps_to_burn (that is, lap_count = 1): change nothing else. The same card and pot stay current, lead_seat stays the same, and next round's offers start again at lead_seat with TAKE offered to every seat.
- If lap_count = laps_to_burn = 2: put the card into the burned list (it scores for no one), set current_card = 0, keep the pot as it is, and move lead_seat one seat clockwise.

Step 8, ANNOUNCE RESULT. Tell everyone who paid and who took (or that the card was burned). Players' own chip counts are shown only to themselves.

Step 9, END CHECK. If the deck is empty and current_card = 0, the game ends. Otherwise start the next round. The game cannot last more than 40 rounds.

SCORING. Each player's final score = card points minus chips in hand. Card points equal the sum of the lowest card of each run of consecutive numbers in the tableau. Any chips left in the pot at the end belong to no one.

Objective: Each player's final score is card points minus remaining chips. The single player with the lowest final score wins. If two or more players tie for lowest, the game is a draw.

Expected effect: Play stays recognisably No Thanks!: milk cards you intend to take, punish opponents you believe are low on chips, and take cards that extend your runs. The burn rule adds a new decision. After one all-PAY lap, everyone knows a second lap burns the card, so paying again is a bet that nobody else wants it. A large pot carried from a burned card turns the next card into a contest. Simple policies lose: always TAKE collects nearly every card and scores far higher than anyone, and always PAY is bled dry and then forced to take everything. Talk is left out. Players disagree (only one can win), but chip-count claims are cheap and unverifiable, and the hidden chips are inferred better from the public paying history, so a talk phase would add steps without adding a decision.

## Complexity (the designer's count, against the limits)

- steps_per_round: 12 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 13 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 40 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
