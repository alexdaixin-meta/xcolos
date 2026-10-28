# Simultaneous Yaniv: Claims

Low-hand card game played in simultaneous turns: each round players secretly call or discard, then secretly claim another player's discarded card or take a shared blind draw. A caller who is not strictly lowest is caught (Asaf) for +30, and the lowest total when someone reaches 150 or after 40 rounds wins.

Players: 3 to 5, best with 4

## Parameters

- `hand_size_start` = 5
- `call_limit` = 7
- `asaf_penalty` = 30
- `end_total` = 150
- `max_rounds` = 40
- `min_set_size` = 2
- `min_run_length` = 3
- `max_tens_in_run` = 1
- `min_cards_kept` = 1
- `shoe_size` = 54
- `copies_per_value_1_to_9` = 4
- `copies_value_10` = 16
- `copies_value_0` = 2
- `run_offer_cards` = 2
- `set_or_single_offer_cards` = 1
- `contest_threshold` = 2
- `blind_draws_per_round` = 1

## Round

1. **tell** (all players): Announce round, every player's hand_size and total, and last_results.
2. **sync** (all players): Each player privately sees their own hand and hand_sum.
3. **poll** (all players): first_choice := the answer.
4. **update** (all players): Any illegal first_choice is replaced: a player with hand_size >= 2 discards their single highest card; a player with hand_size 1 discards nothing (NONE). Then called := (first_choice == CALL), and called_count := the number of players with called true. (judged: "This player's first choice is legal: CALL with hand_sum at most 7; or values all held in their hand that form a single card, two or more cards of equal value, or a run of three or more consecutive values with no 0 and at most one 10; and at least one card is left in hand.")
5. **update** (all players): When called_count >= 1 (showdown): all discards are cancelled and lowest_sum := the minimum hand_sum. For each player: if called and hand_sum == lowest_sum and the count of players with hand_sum == lowest_sum is 1, round_score := 0; else if called, round_score := hand_sum + 30; else if hand_sum == lowest_sum, round_score := 0; else round_score := hand_sum. total += round_score. last_results records the revealed hands, the callers and the scores.
6. **tell** (all players): When called_count >= 1: reveal every hand, hand_sum, called, round_score and total.
7. **check** (all players): When called_count >= 1: end the game if any total >= 150 or round == 40.
8. **update** (all players): When called_count >= 1 and round < 40: each hand is cleared and gets 5 random draws from the shoe (without removal). hand_sum and hand_size are recomputed.
9. **update** (all players): When called_count == 0: discard := the discarded values, which are removed from hand; hand_sum and hand_size are recomputed. offers := for each player who discarded one card or an equal-value set, one entry 'seat S: value V'; for each player who discarded a run, two entries, its lowest and its highest value. A player who discarded nothing makes no offer.
10. **tell** (all players): When called_count == 0: announce every player's discard and the offers list.
11. **poll** (all players): When called_count == 0: claim := the answer. An illegal answer becomes BLIND.
12. **update** (all players): When called_count == 0 (contests): for each offer entry claimed by 2 or more players, each of those players gets claim_failed := true and claim := BLIND. took_blind := (claim == BLIND).
13. **update** (all players): When called_count == 0: blind_card := one value drawn at random from the shoe (without removal). Each player whose claim is an offer appends that offer's value to hand. Each player with took_blind appends blind_card to hand. hand_sum and hand_size are recomputed.
14. **tell** (each player with took_blind true): When called_count == 0: privately tell the player the value of blind_card.
15. **update** (all players): When called_count == 0: last_results := who claimed which card, which claims failed through contest, and who took BLIND. The blind_card value is not included.
16. **tell** (all players): When called_count == 0: announce last_results.
17. **update** (all players): When round == 40 and called_count == 0 (final showdown): lowest_sum := the minimum hand_sum. Each player gets round_score := 0 if hand_sum == lowest_sum, else round_score := hand_sum. total += round_score.
18. **tell** (all players): When round == 40 and called_count == 0: reveal every hand, hand_sum, round_score and total.
19. **update** (all players): Reset called, discard, claim, claim_failed, took_blind and offers. round += 1.
20. **check** (all players): End the game if any total >= 150 or round > 40.

## Ending

- ends when: any player's total >= 150 after a showdown, or round > 40 (after round 40 is played)
- ranked by: `-you.total` (the highest wins; players level at the top share the win)
- decided by: The player with the lowest total wins. Players level at the lowest total share the result (the source calls this a draw).

## Choices the source did not make

- 3 to 5 players, suggested 4: 4 is the designer's size and is kept. Three is the minimum for contests over offered cards and for a caller to face more than one rival. More than five makes contests near-certain and the showdown arithmetic too long to follow.
- No talk step: The source has no talk. Strategy lies in reading discards and claims (claiming a card reveals what you hold), timing the call, and avoiding contested claims.
- A 1-card player is offered only the forced option: The rules force CALL (if allowed) or discarding nothing, so no other option is offered.
- Draws are with replacement from a 54-value list: The source reshuffles the shoe before every draw, so the shoe's frequencies never change.
- Each card of a run's two offers is claimable separately: The rules call each one an offered card that a player may claim.

## Simplifications

- The legality of a discard (set or run) is judged by a referee sentence: Checking that values are held and form a set or a valid run is list logic, beyond simple arithmetic. Scoring stays arithmetic.
- A tie for the lowest total is a shared win rather than a declared draw: The engine shares the win among players level at the top. This is the same outcome as the source's draw.
- The lowest total wins via rank_by = -total: The engine ranks the highest value first.

## Unsupported (needs engine work)

- none
