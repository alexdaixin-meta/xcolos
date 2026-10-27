# Tides of Madness: Obsession

A two-player card draft over 3 tides of 5 rounds: pick a card, swap hands, score suit sets doubled for a secret Obsession suit, and avoid reaching 9 madness.

Players: 2 to 2, best with 2

## Parameters

- `deck_size` = 30
- `suits` = 5
- `cards_per_suit` = 6
- `plain_cards_per_suit` = 4
- `madness_cards_per_suit` = 2
- `total_rounds` = 15
- `tides` = 3
- `rounds_per_tide` = 5
- `hand_size` = 5
- `set_points_0` = 0
- `set_points_1` = 1
- `set_points_2` = 3
- `set_points_3` = 6
- `set_points_4_or_more` = 10
- `obsession_multiplier` = 2
- `points_per_madness_card` = 1
- `diversity_suits_needed` = 4
- `diversity_bonus` = 4
- `madness_bonus_points` = 4
- `madness_bonus_reduction` = 1
- `madness_loss_threshold` = 9
- `cards_retained_per_tide` = 1
- `retain_tides` = 2
- `starting_score` = 0
- `starting_madness` = 0

## Round

1. **update** (all players): round += 1; tide = ceil(round / 5); round_in_tide = (round - 1) mod 5 + 1. Announce the round and tide.
2. **update** (all players): When round_in_tide == 1: deck = full_deck minus every card in either player's retained list; each player's hand = [] and tableau = []; then deal 5 cards to each player's hand. Each card is a random draw removed from deck and appended to hand. The cards left in deck are unused this tide.
3. **sync** (all players): Each player privately sees their own hand, tableau, obsession and both retained lists.
4. **poll** (all players): When round_in_tide == 1: set you.obsession to the chosen suit. It stays hidden from the opponent (ally) until the tide's reveal.
5. **poll** (all players): Simultaneously, each player removes the chosen card from you.hand and appends it to you.tableau, face down. When round_in_tide == 5 the hand has 1 card, so the pick is forced.
6. **update** (all players): When round_in_tide < 5: swap hands, so seat 1's hand becomes seat 2's old hand and seat 2's hand becomes seat 1's old hand.
7. **tell** (all players): When round_in_tide == 5: reveal to everyone each player's tableau, retained cards and obsession.
8. **update** (all players): When round_in_tide == 5, for each player, with T = tableau + retained: tide_icons = number of cards in T with '*'; madness += tide_icons. For each suit, n = cards of that suit in T and set_pts = 0 if n=0, 1 if n=1, 3 if n=2, 6 if n=3, 10 if n>=4, doubled if the suit equals obsession. tide_points = sum of set_pts + tide_icons * 1 + (4 if the number of distinct suits in T >= 4 else 0). score += tide_points. Then bonus_seat = 1 if seat 1's tide_icons > seat 2's, 2 if seat 2's > seat 1's, else 0. Announce each player's tide_points, score and madness.
9. **ask** (the seat equal to bonus_seat (skipped if bonus_seat == 0)): When round_in_tide == 5 and bonus_seat > 0: the bonus seat chooses privately. gain_4_points: you.score += 4. reduce_madness_1: you.madness -= 1.
10. **update** (all players): When round_in_tide == 5, madness check. If exactly one player has madness >= 9, that player's lost = 1 and madness_end = 1. If both have madness >= 9: the one with the higher madness gets lost = 1; if equal, both keep lost = 0 (a draw); madness_end = 1 either way. Announce the result.
11. **check** (all players): End the game if madness_end == 1 or (round == 15 and round_in_tide == 5); otherwise continue.
12. **poll** (all players): When round_in_tide == 5 and tide < 3: simultaneously, each player picks one card to retain permanently.
13. **update** (all players): When round_in_tide == 5 and tide < 3: append each player's chosen card to you.retained, face up and public; set tableau = [] and obsession = ''. All other drafted cards go back to the pool used to rebuild the deck next tide. Announce the retained cards.

## Ending

- ends when: madness_end == 1 or (round == 15 and round_in_tide == 5)
- ranked by: `madness_end * (1 - you.lost) * 1000000 + (1 - madness_end) * (you.score * 100 + (99 - you.madness))` (the highest wins; players level at the top share the win)
- decided by: If the game ended at a madness check, the player who did not lose wins; if both reached 9 or more with equal madness totals, both rank level and the game is a draw. Otherwise, after tide 3 the higher score wins; on tied scores the lower madness total wins; if both are tied, the game is a draw (shared win).

## Choices the source did not make

- Exactly 2 players (min 2, max 2, suggested 2): The designer fixed 2. The hand-swap draft only works between two players: what you pass is exactly what your single opponent gets. The strategy lies in reading the opponent's Obsession from what they take, hate-drafting their suit, and managing madness against theirs for the bonus without nearing 9.
- No talk step: The source has no communication. Picks are secret and simultaneous, and with only two rivals in direct conflict, talk would add nothing faithful to the rules.
- Card names such as 'Deep-3' and 'Deep*-1': Each of the 30 cards needs a distinct name so it can be removed from and appended to lists; '*' marks the madness icon, as in the source.
- rank_by encodes the madness loss with madness_end and lost: A single arithmetic expression must cover both endings. After a madness end only not-losing counts, and equal totals tie (draw). Otherwise score comes first, then lower madness.
- Madness reduction needs no floor at 0: The bonus seat added at least 1 icon this tide, so its madness total is at least 1 before the -1.

## Simplifications

- The Obsession is asked in its own simultaneous poll just before the first pick of the tide, not in the same answer: The engine takes one answer per question. Nothing is revealed between the two polls, so the choice is still made blind, at the same moment as the first pick.
- The reveal of face-down tableaus and Obsessions is done by an announcement, while the attributes stay owner-only: Visibility is fixed per attribute. The tell step makes the contents public at the moment the rules reveal them.
- The madness-bonus comparison uses a table attribute, bonus_seat: The engine has no operand for another player's attribute (player_attribute_compare workaround).
- Steps for the start and end of a tide carry a 'when' condition on round_in_tide inside one flat round list: Single conditional steps are supported; no block of steps replaces another.

## Unsupported (needs engine work)

- none
