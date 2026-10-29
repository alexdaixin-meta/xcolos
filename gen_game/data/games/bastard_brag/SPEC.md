# Knock Brag (3-player)

Three players swap cards with a shared three-card table hand to build the best Brag hand; the leader may knock to force a showdown, the lowest hand at each showdown loses lives, and the last player with lives wins.

Players: 3 to 3, best with 3

## Parameters

- `player_count` = 3
- `starting_lives` = 3
- `deck_size` = 36
- `copies_per_value` = 4
- `lowest_card_value` = 1
- `highest_card_value` = 9
- `hand_size` = 3
- `table_cards` = 3
- `max_rounds` = 40
- `prial_base` = 300
- `prial_333_score` = 310
- `run_base` = 200
- `run_123_score` = 210
- `pair_base` = 100
- `pair_multiplier` = 10
- `knock_min_deal_round` = 2
- `life_loss_lowest` = 1
- `life_loss_knocker_lowest` = 2
- `forced_showdown_offset` = 1
- `rank_lives_weight` = 1000

## Round

1. **update** (all players): When deal_round == 1 (a new deal): rebuild deck as the 36 cards (four each of 1 to 9). Empty every hand. For each active player, draw 3 cards at random from deck into their hand. Then draw 1 card each into table_up, table_d1 and table_d2. Set knocker_seat = 0. The rest of deck is unused this deal.
2. **tell** (all players): When deal_round == 1: announce 'New deal. The face-up card U is {table_up}.'
3. **sync** (all players): Each player sees their own hand, table_up, lives, deal_round, leader_seat and knocker_seat.
4. **ask** (each active player in turn, clockwise starting at leader_seat and skipping eliminated seats): take_up_give_k: swap hand[k] with table_up, then announce 'Seat X took the face-up [old U] and left a face-up [new U]'. blind_Dj_give_k: swap hand[k] with table_dj; the player now sees the received card in their hand; announce 'Seat X made a blind swap with Dj'. whole_hand_expose_k: the old hand [h1,h2,h3] becomes the table and the hand becomes [table_up, table_d1, table_d2]; table_up = old hk, and the other two old cards go to table_d1 and table_d2 in order; announce 'Seat X swapped the whole hand and exposed a [table_up]'. knock: no exchange, set knocker_seat = the leader's seat, announce 'Seat X knocks'. Each effect applies before the next player is asked.
5. **update** (all players): showdown_now = (knocker_seat > 0) or (deal_round == active_count + 1).
6. **update** (all players): When showdown_now: for each active player, let a = min(hand), c = max(hand), b = sum(hand) - a - c. Then hand_score = 310 if a == 3 and c == 3; else 300 + a if a == c; else 210 if a == 1 and b == 2 and c == 3; else 200 + c if b == a + 1 and c == b + 1; else 100 + 10*b + (a + c - b) if a == b or b == c; else a + b + c. Set last_showdown_score = hand_score. Set lowest_score = min and highest_score = max of hand_score over active players.
7. **tell** (all players): When showdown_now: reveal every active player's hand and announce 'Seat X shows [hand] scoring {hand_score}' for each.
8. **update** (all players): When showdown_now and lowest_score < highest_score: each active player with hand_score == lowest_score loses 2 lives if their seat == knocker_seat, otherwise 1 life. Lives are floored at 0. Any player with lives == 0 gets eliminated = true. Recompute active_count as the number of players not eliminated. Announce each life lost and each elimination.
9. **update** (all players): If showdown_now, deal_round = 1; otherwise deal_round = deal_round + 1. Then round_number = round_number + 1, and leader_seat = the next seat clockwise after leader_seat that is not eliminated.
10. **check** (all players): End the game if active_count <= 1 or round_number > 40; otherwise continue.

## Ending

- ends when: active_count <= 1 or round_number > 40
- ranked by: `you.lives * 1000 + you.last_showdown_score` (the highest wins; players level at the top share the win)
- decided by: Most lives wins. A lone survivor is the only player with lives above 0. A tie on lives is broken by the higher last showdown score, and players still level share the win (a draw).

## Choices the source did not make

- Exactly 3 players, suggested 3: The designer fixed the game at 3, and the forced-showdown timing and leader rotation are written for it. A 3-seat table already gives rivals whose swaps and exposed cards can be read. The player's strategy is to infer opponents' hands from what they take and leave face up, to decide when to knock, and to avoid feeding a strong card into U.
- No free-talk step before actions: The source has no talk, and adding it would add a mechanic.
- Cards are named by hand position 1 to 3 in the choice options: Each action must be a single choice carrying every detail. The player sees their hand list, so a position identifies the card.
- Lives are floored at 0 when a loss would make them negative: The player is eliminated either way, and flooring keeps the ranking expression clean without changing who wins.
- Whole-hand swap puts the two unexposed old cards into D1 then D2 in their hand order: The source does not say which goes where. Nobody sees D1 or D2, so the order does not matter.
- rank_by = lives*1000 + last_showdown_score: Scores are at most 310, so lives always dominate and the showdown score breaks ties. Eliminated players have 0 lives and cannot tie with a survivor. A showdown happens at least every 4 rounds, so by round 40 one has always occurred.

## Simplifications

- The turn order is one ask step running clockwise from leader_seat and skipping eliminated seats, rather than fixed seat order: The engine asks in a flat sequence; the starting seat is taken from the table attribute leader_seat.
- Hand reveal at showdown is an announcement listing each active hand and score, not a change of the hand's visibility: The engine reveals through messages; hand_score is public.

## Unsupported (needs engine work)

- none
