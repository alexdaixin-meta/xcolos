# Agram Match

6-hand trick game where only trick 6 of each 6-card hand scores 1 point; most hand wins after 6 hands wins.

Players: 3 to 4, best with 4

## Parameters

- `standard_cards` = 52
- `removed_face_cards` = 12
- `removed_deuces` = 4
- `removed_ace_of_spades` = 1
- `remaining_cards` = 35
- `num_hands` = 6
- `cards_per_player` = 6
- `deal_batches` = 2
- `deal_batch_size` = 3
- `tricks_per_hand` = 6
- `scoring_trick` = 6
- `hand_win_points` = 1

## Round

1. **initialize** (all players): reset deck to 35 cards, clear hand stub discard_pile trick_cards, deal 6 cards to each hand from deck in two batches of 3 clockwise from left of dealer_seat, remainder to stub, set trick_number to 1 and trick_winner to left of dealer_seat
2. **sync** (all players): send each player their own hand
3. **tell** (all players): announce hand_number dealer_seat and trick leader
4. **ask** (each player in turn): play one card from hand to trick_cards, set lead_suit from first card, remove card from hand
5. **update** (all players): rank trick_cards by rank of lead_suit only, highest wins, off-suit cannot win, set trick_winner, move trick_cards to discard_pile, clear trick_cards and lead_suit, increment trick_number unless it was 6
6. **repeat** (all players): repeat play-card and resolve-trick steps until trick_number equals 6 completed tricks
7. **update** (all players): add hand_win_points 1 to match_points of trick_winner of trick 6, others add 0
8. **update** (all players): rotate dealer_seat clockwise by 1 and increment hand_number by 1 and reset trick_number to 1 for next hand
9. **check** (all players): continue if hand_number <= num_hands 6, else end match

## Ending

- ends when: hand_number > 6
- results: seat 1, seat 2, seat 3, seat 4, draw
- decided by: seat with highest match_points wins; if two or more tie for most then draw

## Choices the source did not make

- 3 to 5? no: 3 to 4 players with suggested 4: source says 3 to 4 and designer fixes suggested 4; minimum 3 because with 2 there is no multi-way trick race or void signalling and trick-6 timing is trivial; maximum 4 because a larger table makes one trick-6 win too diluted and turns too long to read discards
- thoughtful play at 4: save a high card of a suit others are void in for trick 6, read follow/void signals, lead suits to exhaust rivals: only trick 6 scores so trick 1-5 are about gaining lead and gathering information while preserving a trick-6 winner
- no talk poll; card plays only: source bans discussion so hands stay hidden; simultaneous poll talk would add noise and leak hands, so only sequential play asks are used
- card codes like AH 10S and arithmetic rank values for trick compare: engine has no card type so text codes plus arithmetic on led-suit ranks decide trick_winner, never model opinion
- all numbers fixed as filed; no open payoff to choose: source gives every count so parameters copy them directly

## Simplifications

- shuffle and two rounds of 3 via random draws with remove from deck and append to hand, remainder to stub: engine has no physical shuffle; shared_deck_draw workaround uses list operations
- trick winner computed by arithmetic rank compare on trick_cards of lead_suit in an update step: engine decides outcomes by arithmetic, not by opinion
- trick loop and hand loop via repeat plus check on trick_number and hand_number with dealer rotation update: step list is flat so counted repetition replaces manual redeal flow
- stub enforced by none visibility and never referenced after deal; discard_pile holds removed cards: engine needs stated state for dealt and removed cards

## Unsupported (needs engine work)

- none
