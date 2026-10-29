# Little Two

A three-player climbing card game over up to 3 deals: shed your 9 cards by beating the pile with singles, pairs, triples or runs. Triples bomb singles and pairs. The lowest total penalty wins.

Players: 3 to 3, best with 3

## Parameters

- `deck_size` = 30
- `ranks` = 10
- `suits` = 3
- `hand_size` = 9
- `aside_size` = 3
- `max_deals` = 3
- `max_orbits` = 40
- `double_penalty_threshold` = 7
- `double_penalty_factor` = 2
- `top_rank_card_low` = 28
- `top_rank_card_high` = 30
- `top_card_penalty` = 1
- `min_play_cards` = 1
- `max_play_cards` = 3
- `run_length` = 3
- `initial_penalty` = 0
- `initial_deals_won` = 0
- `deals_won_tiebreak_multiplier` = 10

## Round

1. **update** (all players): orbit += 1
2. **update** (all players): Start a deal: deal_number += 1; set deck to cards 1..30, every hand to [] and aside to []; draw 9 random cards from deck into each player's hand (remove from deck, append to hand); move the remaining 3 deck cards into aside; every card_count = 9; leader_seat = deal_number; deal_active = true; first_orbit = true; pile_kind = 'empty'; pile_value = 0; last_player = leader_seat. Announce that deal {deal_number} has started and seat {leader_seat} leads.
3. **sync** (all players): each player privately sees their own hand and the public state
4. **update** (seat 1): Clearance: pile_kind = 'empty', pile_value = 0
5. **ask** (seat 1): the chosen option is recorded for the next step
6. **update** (seat 1): If 'pass': seat1.last_action = 'pass'. Otherwise split the option on spaces into cards; remove each card from seat1.hand; seat1.card_count -= number of cards; pile_kind = 'single' if 1 card, 'pair' if 2, 'triple' if 3 of one rank, 'run' if 3 of consecutive ranks; pile_value = highest card; last_player = 1; seat1.last_action = option.
7. **update** (all players): seat1.deals_won += 1; for each other seat with n = card_count: penalty += n * (2 if n >= 7 else 1) + (number of cards in hand numbered 28, 29 or 30); deal_active = false
8. **update** (seat 2): Clearance: pile_kind = 'empty', pile_value = 0
9. **ask** (seat 2): the chosen option is recorded for the next step
10. **update** (seat 2): If 'pass': seat2.last_action = 'pass'. Otherwise split the option on spaces into cards; remove each card from seat2.hand; seat2.card_count -= number of cards; set pile_kind by the cards (single, pair, triple or run); pile_value = highest card; last_player = 2; seat2.last_action = option.
11. **update** (all players): seat2.deals_won += 1; for each other seat with n = card_count: penalty += n * (2 if n >= 7 else 1) + (number of cards in hand numbered 28, 29 or 30); deal_active = false
12. **update** (seat 3): Clearance: pile_kind = 'empty', pile_value = 0
13. **ask** (seat 3): the chosen option is recorded for the next step
14. **update** (seat 3): If 'pass': seat3.last_action = 'pass'. Otherwise split the option on spaces into cards; remove each card from seat3.hand; seat3.card_count -= number of cards; set pile_kind by the cards (single, pair, triple or run); pile_value = highest card; last_player = 3; seat3.last_action = option.
15. **update** (all players): seat3.deals_won += 1; for each other seat with n = card_count: penalty += n * (2 if n >= 7 else 1) + (number of cards in hand numbered 28, 29 or 30); deal_active = false
16. **update** (all players): first_orbit = false
17. **update** (all players): For every seat with n = card_count: penalty += n * (2 if n >= 7 else 1) + (number of cards in hand numbered 28, 29 or 30); deal_active = false
18. **check** (all players): end the game if (deal_number == 3 and deal_active == false) or orbit >= 40; otherwise continue

## Ending

- ends when: (deal_number == 3 and deal_active == false) or orbit >= 40
- ranked by: `you.deals_won - 10 * you.penalty` (the highest wins; players level at the top share the win)
- decided by: The lowest total penalty wins. Among players tied for lowest penalty, the one with the most deals_won wins. Players still tied share the win, which is the draw.

## Choices the source did not make

- Exactly 3 players, suggested 3: The designer fixed the game at 3 seats. The clearance rule ('the other two have passed') and the leader rotation over 3 deals assume exactly three seats.
- No talk phase: The rules say there is no talk phase. All information comes from public plays, passes and card counts.
- Turns use ask, one seat at a time: The order of play matters, and each seat must see the earlier plays it has to beat.
- rank_by = deals_won - 10 * penalty: deals_won is at most 3, so a factor of 10 makes a lower penalty dominate and uses deals_won only as the tie-break. Players still tied share the win, which matches the source's draw.
- Strategy at the table: A thoughtful player keeps triples as bombs, holds high cards (28-30) to regain the lead, tracks which high cards are gone, and dumps cards before falling to 7 or more, where the penalty doubles.

## Simplifications

- The legal-play option list is computed by the engine from the seat's hand list and the pile each turn: The engine offers choices from a list. The rules define the options exactly, so they are generated by arithmetic on card numbers rather than typed freely.
- Each deal resets the deck to cards 1..30 and empties hands and aside before dealing: This is the 'shuffle all 30 cards' step expressed as list operations followed by random draws.
- The three seat turns are written out as three fixed blocks of steps, each with a when-condition: The step list is flat. Per-step conditions reproduce the skip rules and the end-of-deal cutoff.

## Unsupported (needs engine work)

- none
