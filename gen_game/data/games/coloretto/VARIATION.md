# Variation: Coloretto: Secret Favourites

Three players build colour sets by drawing cards into three shared rows or taking a row and sitting out. Each player has a secret Favourite colour that always scores positive, plus the best other colour; the other three colours score negative. There are three cycles, and the highest score wins.

Players: 3 to 3, best with 3

## Review of the original

Coloretto is a card-drafting game for 2 to 5 players. On each turn a player either draws a coloured card and adds it to a shared row, or takes a whole row and sits out the rest of the round. At the end each player's three best colours score positive on a triangular table and all other colours score negative.

- **non_degenerate**: good. Simple policies all lose. 'Always take the first non-empty row' collects about one card per cycle, around 3 to 4 cards in total, and loses to anyone who builds a colour. 'Always place while legal' gets pushed into taking full rows of colours other players chose for it, and scores negative. Seats are symmetric except that the last taker starts the next cycle, and that seat is earned in play, not built in. Every placement changes what the next player is offered.
- **skill_sensitive**: good. The core skill is deciding when to stop placing and take, and which card to dump into a row you hope an opponent must take. That skill compounds across 3 cycles. The card order is random, but with 3 rows and a choice every turn, a stronger player's tableau beats a passive one's reliably.
- **headroom**: good. A weak player who simply collects one colour still scores positive. A strong player can go further: track the cards left (7 of each colour), infer rivals' Favourites, poison rows aimed at a specific rival, and time takes against the shrinking number of open rows. These are not solved.
- **reasoning_dependent**: good. Each player's Favourite colour is secret, and 2 colours are undealt, so nobody knows which colours are 'free'. A player must infer rivals' Favourites from what they take and where they place. A player may also hide their own Favourite by delaying it or bluffing with an off-colour take. The deck order is also hidden.
- **verifiable**: good. The score is T(Favourite) + 2×max(T of others) − sum(T of others) + 2×plus2, which is pure arithmetic on counts the engine tracks. The highest score wins, and a tie is a draw.
- **fits_platform**: weak. The previous variation was turn-based, text-only and at most 36 turns, but it declared 18 attributes when it really needed about 22 to 23. That is over the limit of 20. The causes were redundant takers, turn, three row_k_open flags, favourite_pool and favourite_revealed. Everything else fit: 1 choice step, 1 draw per round, 2 hidden elements.

## Problems

- The attribute count was understated (18 declared, about 22 to 23 actual), which is over the limit of 20.
- 'takers' duplicates the number of players whose taken flag is true.
- 'turn' is redundant: the cycle structure already limits the game to 36 turns.
- Three row_k_open flags store what one closed-rows list can hold.
- 'favourite_pool' and 'favourite_revealed' have no gameplay use; the reveal can be a plain announcement.
- A running 'score' attribute is unnecessary until game end.

## Changes

- Delete 'takers'. The cycle ends when all three players' taken flags are true. (fixes: 'takers' duplicates the number of players whose taken flag is true.): It removes a duplicated attribute.
- Delete 'turn'. The game ends only when cycle reaches 4. (fixes: 'turn' is redundant: the cycle structure already limits the game to 36 turns.): Each cycle has at most 9 placements and 3 takes, so the game is bounded at 36 turns without a counter.
- Replace row_1_open, row_2_open and row_3_open with one table list 'closed_rows'. A row is closed if its number is in the list, and the list is emptied at cycle end. (fixes: Three row_k_open flags store what one closed-rows list can hold.): It saves two attributes and keeps the legality rules identical.
- Delete favourite_pool and favourite_revealed. At game end, Favourites are revealed by an announcement. (fixes: 'favourite_pool' and 'favourite_revealed' have no gameplay use; the reveal can be a plain announcement.): Neither attribute affects play.
- Keep 'score' as a per-player attribute that is written once, at game end, by a single calculation step. (fixes: The attribute count was understated (18 declared, about 22 to 23 actual), which is over the limit of 20.): The winner needs a number to compare, but no running total is kept. The count is then stated honestly as 17.

## Kept from the original

- Draw-and-place versus take-a-row-and-sit-out, with row capacity 3 and one row per player.
- The last taker starts the next cycle.
- Triangular colour scoring with a few positive colours and the rest negative.
- +2 cards.
- The secret Favourite colour as the single strong hidden element, plus the hidden deck order.
- The complete turn and legality rules that the previous review confirmed (next-seat search, last player placing alone, cycle reset).
- 3 cycles, at most 36 turns, no talk.

## The variation's rules

COMPONENTS
- Deck of 38 cards: 7 each of Red, Blue, Green, Yellow and Purple, plus 3 '+2' cards.
- 3 rows (row_1, row_2, row_3), each holding at most 3 cards.
- A table list closed_rows records which rows have been taken this cycle.

ATTRIBUTES (17 in total)
- Per player: red, blue, green, yellow, purple, plus2, taken, favourite, score.
- Table: row_1, row_2, row_3, closed_rows, top_card, deck, cycle, active_seat.

SETUP
1. Shuffle the deck and turn the top card face up as top_card.
2. All rows start empty, and closed_rows is empty.
3. Every player's taken = false and colour and plus2 counts = 0. Set cycle = 1 and active_seat = 1.
4. Deal each player a different Favourite colour at random from the 5 colours. Each player sees only their own. The 2 undealt colours are never shown.
5. Tableaux (colour counts and plus2) are public.

EACH TURN (one engine round)
1. Announce to all: the contents of the three rows, closed_rows, top_card, every player's tableau, which players have taken this cycle, and the cycle number.
2. The active player chooses one legal option.
   - place_k (k = 1, 2, 3) is legal only if k is not in closed_rows and row_k holds fewer than 3 cards.
   - take_k is legal only if k is not in closed_rows and row_k holds at least 1 card.
   - If every open row is full, only take options exist. The number of open rows always equals the number of players who have not taken, so at least one option is always legal.
3. If place_k: append top_card to row_k, then turn the next deck card face up as top_card.
4. If take_k: add each card in row_k to the active player's matching colour count (or plus2), empty row_k, add k to closed_rows, and set the player's taken = true.
5. If all three players now have taken = true (the cycle ends): set every taken = false, empty all rows, empty closed_rows, and add 1 to cycle. active_seat stays the player who just took, so the last taker starts the next cycle.
6. Otherwise: the next active_seat is the first seat, checking s+1, then s+2, then s itself (wrapping 1, 2, 3, 1), whose taken is false. This can be the same player. For example, a lone remaining player keeps placing while their open row has room, and must take once it is full.
7. If cycle is now 4, the game ends. A cycle has at most 12 turns, so the game lasts at most 36 turns and uses at most 27 cards plus the first top card.

SCORING (once, at game end)
- Announce every Favourite.
- T(c) = c(c+1)/2, so 0, 1, 3, 6, 10, 15, 21, 28 for 0 to 7 cards.
- Let F be the count of the player's Favourite colour and o1 to o4 the counts of the other four colours.
- score = T(F) + 2×max(T(o1), T(o2), T(o3), T(o4)) − (T(o1)+T(o2)+T(o3)+T(o4)) + 2×plus2.
- In words: the Favourite and the single largest other colour score positive, and the remaining three other colours score negative. If other colours tie for largest, only one of them counts positive.

There is no table talk.

Objective: After the third cycle, each player's score is computed by the formula. The single highest score wins. If two or more players tie for the highest score, the game is a draw.

Expected effect: Play is the same as the previously tested version, which played correctly. Players weigh taking early (a small safe row) against placing (a bigger row, at the risk of poisoning it for themselves). They infer rivals' Favourites from their takes so they can dump those colours on others or deny them. They may disguise their own Favourite. With only the state needed, the game now builds within the limit at 17 attributes. Talk is left out: Favourites are inferable from public actions, and cheap talk would add little beyond what placements already signal.

## Complexity (the designer's count, against the limits)

- steps_per_round: 11 (limit 20)
- choice_steps_per_round: 1 (limit 4)
- attributes: 17 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 36 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
