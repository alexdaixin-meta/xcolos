# Variation: 3Up Clear Race

Three players each hold a balanced private hand of 10 cards, lock 3 of them face-up, and race to shed everything. Each play must be equal to or higher than the top of the pile. Clear cards and runs of three equal ranks wipe the pile, and a player who cannot play takes it.

Players: 3 to 3, best with 3

## Review of the original

3Up 3Down is a shedding race for 2 to 6 players. Each player plays cards equal to or higher than the top of a shared discard pile, uses Clear cards and runs of three equal ranks to wipe the pile, takes the whole pile when unable to play, and finally sheds a face-up pile and then a blind face-down pile. The first player to run out of cards wins. This revision fixes the previously tested 3-player adaptation, '3Up Clear Race'.

- **non_degenerate**: good. In the tested variation, a seat that always plays its lowest legal single never builds a run, rarely forces a pickup and is beaten by players who hold back. A seat that always plays C first has no defence left when a high pile builds, and takes the pile. A seat that always plays its highest card jams opponents briefly, but is then left with low cards it cannot play on high piles. Each of these policies can lose. The lead rotates every round, so no seat always moves first.
- **skill_sensitive**: good. The deal is stratified: every hand holds 3 Low, 3 Mid, 3 High and 1 C. Starting hands are therefore close in quality. Outcomes then turn on decisions: when to spend the C, when to play a pair or triple to finish a run of three, which 3 cards to lock face-up, and when to dump a high card to force a pickup.
- **headroom**: good. A weak player who plays legal cards still sheds most of the hand. A strong player keeps improving by tracking which ranks are gone, inferring opponents' holdings from their plays and pickups, and timing clears. There is no fixed solution.
- **reasoning_dependent**: good. Hands are private. Each player knows its own 9 numbered cards, so the other 18 are split between the two opponents in an unknown way, and every play or pickup refines the estimate. Face-up piles are public commitments that opponents can plan against. Play is a sequence of turns, so a player must anticipate the next two seats.
- **verifiable**: good. The winner is the first seat whose cards_left reaches 0, or else the fewest cards_left after 30 rounds. Both are arithmetic on tracked counts.
- **fits_platform**: bad. The previous build FAILED playability. It used 33 attributes against a limit of 20, counting a 15-entry PARAMETERS block. Hidden elements were understated (it claimed 1; there were 2). The position of C in the option list was ambiguous, so a default answer could waste C. The face-up selection was one poll of up to 120 three-card sets.

## Problems

- Attribute count was 33, over the limit of 20, mainly because of a 15-entry read-only PARAMETERS block and four separate deal stacks.
- The hidden-element count was misreported. The private up_offer list existed only to support a huge poll.
- The position of C in the turn option list and in the face-up set ordering was unspecified, so the 'first option' default could burn C on an empty pile.
- The face-up choice was a single poll over up to 120 three-card sets, which is too heavy for a text choice.
- The 'out' and 'picked_up' attributes were redundant: game_over already ends play, and picked_up is never used in scoring.

## Changes

- Removed the PARAMETERS block entirely. All constants (ranks 1-9, 3 copies, 3 C, 10-card hands, run of 3, 30 rounds) are written directly in the rule text. (fixes: Attribute count was 33, over the limit of 20, mainly because of a 15-entry read-only PARAMETERS block and four separate deal stacks.): Constants do not need to be attributes.
- Dropped clear_stack. Each seat simply receives one C during the deal. Kept only three number stacks (low, mid, high) for the stratified deal. (fixes: Attribute count was 33, over the limit of 20, mainly because of a 15-entry read-only PARAMETERS block and four separate deal stacks.): This saves an attribute and keeps hands balanced.
- Deleted the out, picked_up and up_offer attributes. (fixes: The 'out' and 'picked_up' attributes were redundant: game_over already ends play, and picked_up is never used in scoring.): Reaching 0 cards sets game_over directly. Pickups are not scored. up_offer is no longer needed with sequential picks.
- The face-up selection is now three simultaneous setup polls. Each poll lists the seat's own hand cards, numbers ascending with C last, and each pick moves one card to the face-up pile. A missing answer takes the first (lowest) card. (fixes: The face-up choice was a single poll over up to 120 three-card sets, which is too heavy for a text choice.): Each poll has at most 10 options, and the default is unambiguous.
- Fixed the option order. Rank options come first, ascending by rank and then by count. 'C' is always listed last. 'take' appears only when nothing else is legal. (fixes: The position of C in the turn option list and in the face-up set ordering was unspecified, so the 'first option' default could burn C on an empty pile.): A default answer now plays the lowest single and never wastes C.
- Restated complexity honestly: 14 attributes in total, 1 hidden element (private hands). (fixes: The hidden-element count was misreported. The private up_offer list existed only to support a huge poll.): The report must match the build.

## Kept from the original

- Shedding race: play equal or higher than the top of the pile, or take the whole pile.
- Multiple copies of one rank may be played together.
- Clear cards wipe the pile; three of the same rank in a row (by any players) also clear it.
- A face-up pile chosen at the start, played only once the hand is empty.
- The first player to empty all cards wins.

## The variation's rules

CARDS: Ranks 1 to 9, three copies of each (27 cards), plus three Clear cards written 'C'. Low = 1-3, Mid = 4-6, High = 7-9.

ATTRIBUTES. Table: low_stack, mid_stack, high_stack (setup lists), pile (list), top_rank (number, 0 means empty), run_count (number), round (number, starts 0), lead (number), game_over (true/false, starts false). Each seat: hand (PRIVATE list), up_pile (public list), hand_count, up_count, cards_left (public numbers).

SETUP (before round 1):
S1. low_stack = the nine cards 1,1,1,2,2,2,3,3,3; mid_stack = the nine cards 4-6; high_stack = the nine cards 7-9. Shuffle each stack.
S2. Deal to seats 1, 2, 3 in turn: 3 cards from low_stack, 3 from mid_stack, 3 from high_stack, then add one 'C'. Every hand has 10 cards and all stacks end empty.
S3. Face-up pick, done three times (picks 1, 2, 3). Each pick is a simultaneous poll: every seat chooses one card from its own hand. Options are listed numbers ascending, then C last. The chosen card moves from hand to up_pile, which is visible to all. A missing or invalid answer takes the first listed card.
S4. For every seat: hand_count = 7, up_count = 3, cards_left = 10. Set pile = empty, top_rank = 0, run_count = 0.

ROUND (repeat while game_over is false and round < 30):
R1. round = round + 1. lead = ((round - 1) mod 3) + 1.
R2. Seats take one turn each in the order lead, lead+1, lead+2 (seat 3 wraps to seat 1). A turn is skipped if game_over is true.

A TURN (steps T1 to T5):
T1. Options. The source is the hand if hand_count > 0, otherwise the up_pile. For each rank r in the source with r >= top_rank, and for each k from 1 up to the number of copies of r in the source, add the option 'r xk' (for example '5 x2'). List these by rank ascending, then by k ascending. If the source holds a C, add the option 'C', which is ALWAYS listed last and is always legal. If there are no options, the only option is 'take'.
T2. The seat chooses one option (seen only by that seat; the result is announced to all). A missing or invalid answer takes the first option.
T3. Apply the option:
- 'r xk': move k cards of rank r from the source to the pile. If top_rank == r, run_count = run_count + k; otherwise run_count = k. Then top_rank = r.
- 'C': remove that C from the game and clear the pile (T4).
- 'take': move every pile card into the seat's hand, then set top_rank = 0 and run_count = 0.
T4. Clear: if C was played or run_count >= 3, remove all pile cards from the game, and set top_rank = 0 and run_count = 0. The turn then ends; the next seat plays onto the empty pile.
T5. Update hand_count and up_count. Set cards_left = hand_count + up_count. If cards_left == 0, set game_over = true.

END OF ROUND:
E1. If round == 30, set game_over = true.

There is no talk phase. All plays and pickups are announced publicly; hands stay private.

Objective: The first seat whose cards_left reaches 0 wins immediately. If 30 rounds pass with no seat at 0, the seat with the fewest cards_left wins. If two or more seats tie for fewest, the game is a draw.

Expected effect: The game plays like the previous variation, but it can now be built. Players reason about which 3 cards to lock face-up (strong public cards versus flexible private ones) and when to spend their single C. They choose between playing a pair or triple to finish a run of three and holding back, and they infer opponents' remaining ranks from the public plays and from the known 3 Low / 3 Mid / 3 High / 1 C structure of each hand. Talk is left out. All three players want the same thing, to be first out, so any proposal amounts to 'gang up on the leader'. Every play is already public, so non-binding talk would add words without information or a real bargain, while the hidden hands and turn order already supply the conflict.

## Complexity (the designer's count, against the limits)

- steps_per_round: 17 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 14 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 30 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
