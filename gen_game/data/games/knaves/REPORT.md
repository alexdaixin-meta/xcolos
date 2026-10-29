# knaves: ready for review

Built from the variation **Knaves Short Deck with Bids** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Use a 20-card deck (A K Q J 10 in four suits), 6 cards each, 6 hands of 6 tricks: 36 rounds, one trick per round. (fixes: P1): Fits the round limit while keeping trumps, follow-suit and all four Jacks.
- Add a simultaneous bid of 0 to 6 tricks at the start of each hand, with a +5 bonus for taking exactly the bid. Bids are revealed together. (fixes: P2): A weak hand can score by bidding low and ducking. Bids reveal information that opponents can reason about and try to spoil.
- At the first round of every hand, explicitly reset the deck to the full 20-card list, clear every hand and the discard pile, and reset the per-hand counters. This happens before shuffling. (fixes: P3): Every hand starts from a full deck, so the deal can never draw from an empty list.
- Played cards move from the hand to a separate discard list and are never returned to the deck. After the deal the deck is empty. (fixes: P4): Keeps the card count consistent: 18 dealt, 1 turned, 1 hidden, 0 in the deck.
- The bid poll is one simultaneous choice put to all three seats, each offered exactly the options 0, 1, 2, 3, 4, 5, 6. It runs only in the first round of each hand. (fixes: P5): Removes the ambiguity about who is asked and which options are offered.
- All fixed numbers are written into the rules as constants, not stored as attributes. (fixes: P6): Saves attributes and removes the mismatch risk.
- Deal with one shuffle of the full deck (the single random event), then hand out cards in fixed order: cards 1-6 to seat 1, 7-12 to seat 2, 13-18 to seat 3, card 19 turned, card 20 hidden. (fixes: P7): One random draw per round, and a deterministic deal after it.

Objective: After the 36th trick and the final end-of-hand scoring, the single player with the highest total wins. A tie for the highest total is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. Per-hand arithmetic: there are 6 tricks at +2 each, so 12 trick points. 18 of the 20 cards are in play, so the expected Jack penalty in play is 10 × 18/20 = 9. Expected trick points across all three seats are therefore about 12 − 9 = 3 per hand, roughly 1 per seat. The exact-bid bonus of +5 dominate
- playable: pass. Rules completeness:
- R1 lists all 20 cards. R2 gives the rank order. R3/R4 fix 36 rounds as 6 hands of 6 tricks.
- R5/R6 give closed-form formulas for dealer and eldest.
- R7 is the deal. Each of its steps carries a per-step 'when trick_in_hand==1' condition, which is allowed; it is not a condition
- reasoning_over_luck: pass. Chance enters through 6 deals, which set hand strength, trump and the hidden card. Skill levers:
(a) Bidding from a hand evaluation that accounts for trump and for 2 unknown cards out of play.
(b) Card counting. Only 20 cards exist and 18 are played, so by mid-hand a counting player can nearly recon

## Complexity

- steps_per_round: designed 15, built 11, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 19, built 45, limit 20 (built: 80)
- hidden_elements: designed 2, built 8, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 36, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Game starts with totals 0, hand 1 and the full 20-card deck
- pass: Within the led suit the Ace beats the King and the Queen
- pass: Game ends after round 36's scoring with no 37th trick
- pass: After round 30 the round becomes 31, which is hand 6
- pass: Hand 4 begins with a fresh deal (random deal: only the hand number, the card counts and the bids are asserted)
- pass: First trick of hand 1 is played by all seats (random deal: only the card counts and the bids are asserted)
- pass: The start of a hand resets bids and re-deals 6 cards each without touching totals (random deal: only the counts are asserted)
- pass: The deal uses 18 cards for the hands and none stays in the deck (random deal: only the counts are asserted)
- pass: After the deal the deck holds 0 cards (random deal: only the counts are asserted)
- pass: All three seats are offered bids 0 to 6 and each bid is recorded
- pass: Leader seat 3 plays, then seat 1, then seat 2; the cards leave the hands and go to discard
- pass: A seat holding the led suit must follow it; a seat without the led suit may play any card
- pass: A low trump beats the led Ace, and the trick winner leads the next trick
- pass: A trick holding JD and JH scores 2-3-4 = -5 for its winner, shown in the end-of-hand total
- pass: At the end of the hand an exact bid earns 5 and every hand_score is added to the total
- pass: Seats level on the highest final total share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [3], results {'seat 1': 8, 'seat 3': 5, 'seat 2': 7}, 78-90 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 126.0 decisions, prompts of 123 characters on average (longest 150)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 1': 21, 'seat 3': 19, 'seat 2': 15, 'seats 1 and 2': 3, 'seats 1, 2 and 3': 1, 'seats 1 and 3': 1}
- always `first@seat1`: won 18, lost 37, drew 5
- always `first@seat2`: won 17, lost 42, drew 1
- always `last@seat1`: won 8, lost 51, drew 1
- always `last@seat2`: won 14, lost 41, drew 5

## Choices the rules did not make

- 3 players, min = max = suggested = 3: The designer fixed the game at 3. The deal uses exactly 18 of 20 cards, the dealer rotation is mod 3, and the 6-card hand fits only three seats.
- No talk step before bids or plays: The rules include no table talk, and adding it would add a mechanic.
- Trick winner computed by an arithmetic card score (rank 1-5, +10 for trump, 0 for an off-suit non-trump): This reproduces R13 exactly by calculation, with no referee needed.
- hand_score, played_card and discard are public: The source leaves their visibility open; all are derivable from cards played face up.
- Strategy at the table: Players read their hand against the trump suit to bid accurately, dodge winning tricks loaded with costly Jacks (especially JH and JD), and dump Jacks onto opponents' tricks while steering toward their exact bid.

## Simplifications

- A tie for the highest total is a shared win for the tied players rather than a separate draw result: The engine ranks by one expression and lets players level at the top share the win. This is equivalent to the source's draw.
- Per-hand reset, deal and bid run as single steps carrying the condition trick_in_hand == 1, and end-of-hand scoring carries trick_in_hand == 6: The step list is flat; each conditional step is a single step, not an alternative block.
