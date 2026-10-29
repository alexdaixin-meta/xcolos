# Little Two

A three-player climbing card game. Over 3 deals, players shed singles, pairs, triples and runs onto a pile, and each deal's losers take penalties for the cards left in hand. The lowest total penalty wins.

Players: 3 to 3, best with 3

## Parameters

- `card_count_total` = 30
- `rank_count` = 10
- `suit_count` = 3
- `deals` = 3
- `max_orbits` = 40
- `hand_size` = 9
- `cards_aside` = 3
- `two_rank` = 10
- `two_lowest_card` = 28
- `two_extra_penalty` = 1
- `double_threshold` = 7
- `double_factor` = 2
- `winner_penalty` = 0
- `run_length` = 3
- `pair_size` = 2
- `triple_size` = 3

## Round

1. **update** (table): WHEN deal_active is false AND deal_number < 3: deal_number += 1; deck = [1..30]; aside = []; each player's hand = []; pile_kind = 'empty'; pile_value = 0; last_player = 0; leader_seat = deal_number; first_orbit = true; deal_active = true. Announce 'Deal {deal_number} begins; seat {leader_seat} leads.'
2. **update** (table): WHEN first_orbit is true AND orbit has not advanced since the deal started (the deal-start condition above): for each player, 9 times move a random card from deck to hand; card_count = 9; then move the remaining 3 deck cards to aside. Hands stay private (ally).
3. **sync** (all players): Each player sees their own hand, all card_counts, all penalties, pile_kind, pile_value and last_player.
4. **update** (seat 1): WHEN deal_active AND NOT (first_orbit AND leader_seat > 1): if last_player == 1, then pile_kind = 'empty' and pile_value = 0 (the pile clears because both others passed).
5. **ask** (seat 1): WHEN deal_active AND NOT (first_orbit AND leader_seat > 1). Records the answer for the next step.
6. **update** (seat 1): WHEN the same condition as seat 1's ask. If judged true: remove the cards from hand; card_count -= number of cards; pile_kind = that kind; pile_value = highest card played; last_player = 1; last_action announces the cards to everyone. If judged false and pile_kind != 'empty': treat as a pass (last_action = 'pass'). If judged false and pile_kind == 'empty': play min(hand) as a single (remove it, card_count -= 1, pile_kind = 'single', pile_value = that card, last_player = 1, announce). (judged: "The answer is not 'pass', every named card is in seat 1's hand, the cards form a single, a pair (2 cards, same rank floor((c+2)/3)), a triple (3 same rank) or a run (3 cards of three consecutive ranks without wrap), and either pile_kind is empty, or the kind equals pile_kind with highest card > pile_value, or it is a triple played on a single or pair.")
7. **update** (table): WHEN deal_active AND seat 1 card_count == 0: seat 1 deals_won += 1; each other player's penalty += (card_count + number of hand cards >= 28) * (2 if card_count >= 7 else 1); deal_active = false. Announce the deal result. The remaining seats' steps this orbit are skipped because deal_active is false.
8. **update** (seat 2): WHEN deal_active AND NOT (first_orbit AND leader_seat > 2): if last_player == 2, then pile_kind = 'empty' and pile_value = 0.
9. **ask** (seat 2): WHEN deal_active AND NOT (first_orbit AND leader_seat > 2).
10. **update** (seat 2): Same as seat 1's resolution with seat 2: a legal play removes the cards, lowers card_count, sets pile_kind and pile_value, sets last_player = 2 and is announced. An illegal answer is a pass, or, if the pile is empty, min(hand) is played as a single. (judged: "The answer is not 'pass', every named card is in seat 2's hand, the cards form a single, pair, triple or run (ranks floor((c+2)/3), runs without wrap), and either pile_kind is empty, or the kind equals pile_kind with highest card > pile_value, or it is a triple played on a single or pair.")
11. **update** (table): WHEN deal_active AND seat 2 card_count == 0: seat 2 deals_won += 1; each other player's penalty += (card_count + twos in hand) * (2 if card_count >= 7 else 1); deal_active = false.
12. **update** (seat 3): WHEN deal_active: if last_player == 3, then pile_kind = 'empty' and pile_value = 0.
13. **ask** (seat 3): WHEN deal_active.
14. **update** (seat 3): Same as seat 1's resolution with seat 3 (last_player = 3). (judged: "The answer is not 'pass', every named card is in seat 3's hand, the cards form a single, pair, triple or run (ranks floor((c+2)/3), runs without wrap), and either pile_kind is empty, or the kind equals pile_kind with highest card > pile_value, or it is a triple played on a single or pair.")
15. **update** (table): WHEN deal_active AND seat 3 card_count == 0: seat 3 deals_won += 1; each other player's penalty += (card_count + twos in hand) * (2 if card_count >= 7 else 1); deal_active = false.
16. **update** (table): orbit += 1; first_orbit = false. If orbit == 40 AND deal_active: every player's penalty += (card_count + twos in hand) * (2 if card_count >= 7 else 1); deal_active = false. Announce penalty totals.
17. **check** (table): End the game if (deal_number == 3 AND deal_active == false) OR orbit >= 40; otherwise continue.

## Ending

- ends when: (deal_number == 3 AND deal_active == false) OR orbit >= 40
- ranked by: `0 - you.penalty` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their total penalty, and lower is better. The player with the lowest total wins. Players tied for the lowest total share the result, which the source calls a draw.

## Choices the source did not make

- 3 players (min = max = suggested = 3): The designer fixed 3 seats. The deal arithmetic (3 x 9 + 3 aside = 30) and the A-B-C rotation only work at 3.
- Strategy at the table: A thoughtful player tracks played cards and opponents' public card counts, saves triples as bombs, and passes to keep control, while sheding high-penalty cards (twos, a big hand) before someone goes out.
- No talk step: The source has no talk. It is a competitive individual game, so messages would add words without anything to agree on.
- Turns use ask, one seat at a time: The rules give a fixed turn order, and each player must see the current pile.
- Answer as free text listing card numbers: The set of legal combinations changes every turn. Free text plus the illegal-play-as-pass rule covers it faithfully.
- Seats numbered A=1, B=2, C=3: This lets the leader and last_player be compared arithmetically.

## Simplifications

- Play legality is checked by a judged referee step: Validating combination membership, rank equality, runs and kind/value comparison against the pile is too complex for single arithmetic operations. The resulting state changes are still arithmetic.
- Deal-start steps (shuffle, deal, reset) are separate flat steps each carrying the same 'when' condition: The engine has no conditional blocks. Each step is individually guarded instead.
- Lowest penalty wins is expressed as rank_by = 0 - penalty, and a tie at the top is a shared win: The engine ranks highest-wins and treats a tie at the top as shared. The source's 'draw' becomes a shared result.

## Unsupported (needs engine work)

- none
