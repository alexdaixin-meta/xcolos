# Variation: 3Up Shed (Equal Turns)

A three-player counted-deck shedding game. Each player has a hidden hand and a public 3-card up pile. Players must beat or match the pile or pick it up, Clears and triples wipe the pile, the lead rotates each round, and everyone who empties within the same round shares the win.

Players: 3 to 3, best with 3

## Review of the original

3Up 3Down is a shedding game for 2 to 6 players. Each turn you must play a card at least as high as the top of the discard pile or pick the whole pile up. Clear cards and three-of-a-kind runs wipe the pile. You play from your hand, then from your face-up cards, then blindly from your face-down cards, and the first to run out of cards wins.

- **non_degenerate**: weak. In the original, playing is forced whenever a legal play exists, so many turns have only one choice. The blind 3DOWN flips are pure chance. In the previous variation no simple policy dominated. 'Lowest single' loses the race to players who shed pairs, and 'always last' wastes its Clear on turn 1. But the instant win on reaching zero cards, with seat 1 always moving first, gave seat 1 about 52% of wins against about 19% for seat 3.
- **skill_sensitive**: weak. In the original, the shuffled draw pile and the blind flips decide a lot, so luck is large. The counted, band-symmetric deal of the previous variation removed most of that. However, seat order then outweighed skill.
- **headroom**: good. There is room to improve in several places: when to spend the Clear, whether to split or keep pairs, whether to complete a run of three (which wipes the pile and hands a free empty pile to the next player), which three cards to expose as the up pile, and card counting. A weak player still sheds cards every turn and finishes with some score.
- **reasoning_dependent**: good. Hands are hidden, but the deck composition is known, every deal is band-symmetric, up piles are public and every play is visible. So opponents' remaining ranks can be inferred by counting. Deciding what to leave on top for the next player requires modelling that player's likely holdings.
- **verifiable**: good. The winner follows from cards_left counts, which are pure arithmetic.
- **fits_platform**: weak. The original has a shared draw pile, extra plays after Clear+1 and Clear+2, and blind flips. These are costly or impossible as a flat step list. The previous variation fit the platform, but it ended mid-round and carried an unused attribute (players_out).

## Problems

- P1 Seat edge: the game ends the instant a seat empties, and seat 1 always acts first in a round. Seat 1 wins about 52% of races against about 19% for seat 3.
- P2 Seat 1 alone opens round 1 on an empty pile and leads every round, so it always gets the earliest free plays.
- P3 The unused players_out attribute inflates the state.
- P4 Original only: blind face-down flips, the shuffled draw pile and multi-play Clears add luck and step complexity. These were already removed in the previous variation, and that removal is kept.

## Changes

- Equal turns: reaching 0 cards no longer ends the game mid-round. Every remaining seat finishes the round. At round end, all seats with 0 cards share the win, and two or more such seats make a draw. (fixes: P1 Seat edge): Turning the race into 'fewest turns needed' gives every seat the same number of turns, so move order no longer decides ties in turn count.
- Rotate the lead: in round r, the order is seat L, L+1, L+2 (wrapping), with L = ((r-1) mod 3)+1. (fixes: P2 Seat 1 opening advantage): This spreads the lead, and the free plays onto a fresh pile that come with it, across all seats.
- Remove players_out. The end check uses each seat's out flag directly. (fixes: P3 Unused attribute): The state should hold only what the game uses.
- Keep the counted 30-card deck, the band-symmetric deal and the single-play Clear, with no blind cards and no draw pile. (fixes: P4 Original luck and complexity): This keeps luck low and the step count small.

## Kept from the original

- Play a card at least equal to the top of the pile, or pick the whole pile up
- Multiple copies of one rank may be played together
- Clear cards wipe the pile
- Three consecutive cards of the same rank wipe the pile
- Hand first, then the public face-up 3UP pile
- Choosing which 3 cards to place face-up
- Shedding all cards wins

## The variation's rules

DECK. There are 30 cards: three copies each of ranks 1 to 9, plus three Clears (C). They are split into four stacks: Low (ranks 1-3, nine cards), Mid (ranks 4-6, nine cards), High (ranks 7-9, nine cards) and Clear (three cards). Everyone knows the deck's composition.

SETUP (once, before round 1).
S1. Shuffle the Low, Mid and High stacks separately.
S2. In seat order 1, 2, 3, each seat's hand receives the top 3 Low, the top 3 Mid and the top 3 High cards, plus 1 Clear. Each hand now holds 10 cards and every stack is empty.
S3. For each seat, the engine lists as up_offer every distinct set of 3 cards from that hand. Each set is written in ascending order, with C counting above 9, and the list is sorted ascending.
S4. All seats answer at the same moment, each picking one set. A missing or invalid answer takes the first set listed.
S5. The chosen 3 cards move from the hand to that seat's up_pile. Up piles are public; hands are secret.
S6. For each seat, set hand_count = 7, up_count = 3, cards_left = 10, out = false and picked_up = 0.
S7. The table starts with an empty pile: top_rank = 0, run_count = 0, round = 0, game_over = false.

ROUND (at most 20 rounds).
R1. Increase round by 1. Set lead = ((round - 1) mod 3) + 1.
R2. Three turns are taken, in this order: seat lead, then the next seat, then the next (after seat 3 comes seat 1). A seat with out = true skips its turn: it makes no choice and nothing about it changes.
R3. After the three turns: if at least one seat has out = true, set game_over = true.
R4. If game_over is true, or round = 20, the game ends.

TURN.
T1. Source: if the seat's hand is not empty, it plays from its hand. Otherwise it plays from its up_pile.
T2. Legal plays come from the source only:
- a rank r with r >= top_rank, played as 1, 2 or 3 copies, up to the number held;
- a single C, which is always legal.
When top_rank = 0, every card is legal. The engine lists the legal plays by ascending rank, then by number of copies, with C last. If no play is legal, the only option is PICK UP.
T3. The seat chooses one option. A missing or invalid answer takes the first option listed.
T4. Apply the choice:
- Rank play: the cards go onto the pile. If the previous top was also rank r, add the number of cards played to run_count; otherwise set run_count to that number. Set top_rank = r. If run_count >= 3, wipe the pile: remove it from the game and set top_rank = 0 and run_count = 0.
- C: remove the pile and the C from the game, and set top_rank = 0 and run_count = 0.
- PICK UP: the whole pile goes into the seat's hand, picked_up increases by 1, and top_rank = 0 and run_count = 0.
Every choice ends the turn; there are no extra plays.
T5. Recompute hand_count and up_count, and set cards_left = hand_count + up_count. If cards_left = 0, set out = true.

There are no draw pile and no face-down cards.

Objective: If the game ends because game_over is true, every seat with cards_left = 0 wins. If exactly one seat has 0 cards, it wins alone; if two or three do, the game is a draw. If round 20 ends with nobody out, the seat with the fewest cards_left wins, and a tie for fewest is a draw.

Expected effect: Every seat gets the same number of turns, so the race is decided by how few turns a player needs. Shedding pairs, timing the Clear and choosing the up pile then decide the game, not seating. Rotating the lead spreads out who plays onto a fresh pile. Two decisions now carry the opponent modelling: whether to complete a run of three (which hands the next player an empty pile), and what top card to leave for the next seat given its counted holdings. Ties for the fewest turns become draws, which is honest given the symmetric deals. Talk is left out. The conflict is real, since only the fastest wins, but nearly every play is forced by what the player holds. Any agreement such as 'don't feed the leader' cannot be enforced and changes few actual options. Talk would add words without reasoning.

## Complexity (the designer's count, against the limits)

- steps_per_round: 15 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 15 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 20 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
