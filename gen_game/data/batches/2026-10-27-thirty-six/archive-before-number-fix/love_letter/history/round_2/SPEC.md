# Love Letter: Short Hands

Two-player Love Letter over exactly 40 turns: draw, discard a card to use its effect, knock out the rival or win the showdown, and optionally raise a hand's stake to 2.

Players: 2 to 2, best with 2

## Parameters

- `deck_size` = 16
- `guard_count` = 5
- `guard_rank` = 1
- `priest_count` = 2
- `priest_rank` = 2
- `baron_count` = 2
- `baron_rank` = 3
- `handmaid_count` = 2
- `handmaid_rank` = 4
- `prince_count` = 2
- `prince_rank` = 5
- `king_count` = 1
- `king_rank` = 6
- `countess_count` = 1
- `countess_rank` = 7
- `princess_count` = 1
- `princess_rank` = 8
- `total_rounds` = 40
- `cards_out_of_play` = 5
- `cards_dealt_each` = 1
- `deck_after_deal` = 9
- `base_stake` = 1
- `raised_stake` = 2
- `fold_points` = 1
- `guard_guess_min` = 2
- `guard_guess_max` = 8
- `showdown_deck_threshold` = 1
- `raise_min_deck` = 2
- `starting_points` = 0
- `starting_starter_seat` = 1

## Round

1. **update** (table): When new_hand = 1: empty both players' hand and discards. Clear out_of_play. Copy full_deck into deck and shuffle it. Move the top 5 cards of deck into out_of_play (public). Deal 1 card from the top of deck to each player's hand. Move the bottom card of deck into reserve, leaving deck with 8 cards and reserve with 1. Set deck_count = 9, protected = 0 and eliminated = 0 for both players, stake = 1, folded = 0, active_seat = starter_seat and new_hand = 0. Announce out_of_play to everyone.
2. **update** (active seat): Reset guard_guess = 0, raised = 0, prince_target = 0. Set the active player's protected = 0. Move the top card of deck into the active player's hand (never the reserve). Set deck_count = len(deck) + len(reserve).
3. **sync** (all players): Each player sees their own hand and all public attributes.
4. **ask** (active seat): The chosen rank is held for the next step. Prompt: 'Choose one of your two cards to discard.'
5. **update** (active seat): If the active hand contains 7 together with 5 or 6, the discarded card is 7 whatever was chosen. Remove that card from the active hand, append it to the active player's discards and set current_discard to it. Announce 'Seat {active_seat} discards {card name}'.
6. **ask** (active seat): When current_discard = 1 and the opponent's protected = 0: set guard_guess to the named rank and announce the named rank to both players.
7. **update** (table): When guard_guess >= 2: if the opponent's hand card equals guard_guess, set the opponent's eliminated = 1 and announce 'Hit: {card name}'. Otherwise announce 'Miss'.
8. **tell** (active seat only): When current_discard = 2 and the opponent's protected = 0: privately tell the active player the opponent's hand card.
9. **update** (table): When current_discard = 3 and the opponent's protected = 0: compare the active hand card with the opponent's hand card. The holder of the lower rank gets eliminated = 1 and their card is announced. On equal ranks nothing happens and nothing is revealed.
10. **update** (active seat): When current_discard = 4: set the active player's protected = 1.
11. **update** (table): When current_discard = 5: prince_target = the opponent if the opponent's protected = 0, otherwise the active seat. Move the target's hand card to the target's discards and announce it. If that card is 8, set the target's eliminated = 1.
12. **update** (prince target): When prince_target > 0 and the target's eliminated = 0: move the top card of deck into the target's hand, or the reserve card if deck is empty. Set deck_count = len(deck) + len(reserve).
13. **update** (both players): When current_discard = 6 and the opponent's protected = 0: swap the active player's hand with the opponent's hand.
14. **update** (active seat): When current_discard = 8: set the active player's eliminated = 1.
15. **sync** (all players): Each player sees their own (possibly swapped or redrawn) hand and all public attributes.
16. **ask** (active seat): When stake = 1, both players' eliminated = 0, deck_count >= 2 and the opponent's discards has at least 1 card: prompt 'Raise this hand's stake to 2, or pass?' On raise, set raised = 1 and announce the raise.
17. **ask** (opponent of the active seat): When raised = 1: prompt 'Accept (the stake becomes 2) or fold?' On accept, set stake = 2. On fold, set folded = 1. Announce the answer.
18. **update** (table): HAND END, first that holds: (a) if folded = 1, the active player's points += 1; (b) else if a player has eliminated = 1, the other player's points += stake; (c) else if deck_count <= 1 or round_number = 40, reveal both hand cards and the higher rank's points += stake, with no score on equal ranks. If (a), (b) or (c) applied, set new_hand = 1 and starter_seat = 3 - starter_seat, and announce the result.
19. **update** (table): If new_hand = 1, set active_seat = starter_seat. Otherwise set active_seat = 3 - active_seat. Then round_number += 1.
20. **check** (table): End the game if round_number > 40, otherwise continue.

## Ending

- ends when: round_number > 40
- ranked by: `you.points` (the highest wins; players level at the top share the win)
- decided by: After exactly 40 rounds, the player with more points wins. Equal points share the win, which is the draw.

## Choices the source did not make

- 2 players (min 2, max 2): The designer fixed the table at 2. Every effect (Guard, Baron, King, the raise and fold) targets 'the opponent', so more seats would break the rules.
- No free talk step: The source has none. The raise and fold already carry the bluffing signal.
- Countess forcing is shown in the offer as well as enforced in the resolve step: A seat is never offered what it may not do. The outcome is the same as the source's override.
- Strategy at the table: Players track the out_of_play cards and both discard piles to make good Guard guesses, time Baron and King plays, and raise as a bluff or with a strong card.

## Simplifications

- Cards are stored as their ranks (1 to 8) and named in announcements: The Guard check, Baron comparison and showdown are then plain arithmetic.
- The reserve is kept in its own hidden list instead of at the bottom of the deck: The engine draws from a list, so separating it guarantees the turn-start draw never takes it. deck_count adds both lists.
- The Guard guess and Guard check are tracked with guard_guess > 0 instead of 'step 5 ran'; the Prince redraw uses prince_target: A step's 'when' must be an arithmetic condition on state.

## Unsupported (needs engine work)

- none
