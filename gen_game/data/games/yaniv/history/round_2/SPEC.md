# Simultaneous Yaniv

Each round, every player secretly chooses at the same time to discard a set of equal cards or to call. Claims on cards others discarded collide, and showdowns score hand sums. The lowest total after a showdown that pushes anyone to 100, or after round 30, wins.

Players: 3 to 5, best with 4

## Parameters

- `call_limit` = 7
- `asaf_penalty` = 30
- `end_total` = 100
- `max_rounds` = 30
- `hand_cards` = 5
- `shoe_size` = 54
- `shoe_zeros` = 2
- `shoe_each_1_to_9` = 4
- `shoe_tens` = 16
- `joker_value` = 0
- `ace_value` = 1
- `face_value` = 10
- `caller_safe_score` = 0
- `lowest_noncaller_score` = 0

## Round

1. **update** (all players): game.round += 1; game.any_call = false; for each player: called = false, first_choice = '', discard_value = -1, shed_count = 0, claim = '', claim_success = false, took_blind = false, blind_seen = -1, revealed_hand = []
2. **poll** (all players): messages are gathered simultaneously and then broadcast to all as 'Seat {seat} says: {value}'
3. **poll** (all players): set first_choice. An invalid answer becomes CALL if hand is empty, otherwise 'discard H' with H = max(hand). called = (first_choice == 'CALL'); game.any_call = (count of players with called) >= 1; all first choices revealed publicly
4. **update** (all players): when game.any_call: revealed_hand = hand for every player (public); game.lowest_sum = min over players of hand_sum; game.lowest_count = count of players with hand_sum == game.lowest_sum
5. **update** (all players): when game.any_call: for each player, round_score = if called then (if hand_sum == game.lowest_sum and game.lowest_count == 1 then 0 else hand_sum + 30) else (if hand_sum == game.lowest_sum then 0 else hand_sum); total += round_score; if game.round == 30 then game.game_over = true; announce each round_score and total publicly; discards chosen this round are ignored
6. **check** (all players): end the game if game.any_call and (max over players of total >= 100 or game.game_over)
7. **update** (all players): when game.any_call: in one deal operation, each hand is replaced by 5 random values from game.shoe (shoe not depleted), visible only to the owner; hand_sum = sum(hand); hand_size = 5 (public); revealed_hand = []. Steps 8 to 13 are skipped because each carries the condition not game.any_call
8. **update** (all players): when not game.any_call: V = value in first_choice; discard_value = V; shed_count = count of V in hand; remove every V from hand (the cards leave play); announce publicly each player's discard_value and shed_count. Each player offers one card of value discard_value
9. **poll** (all players): when not game.any_call: set claim; an invalid answer becomes 'BLIND'
10. **update** (all players): when not game.any_call: for each player with claim 'value V': claim_success = (count of players with claim == 'value V') == 1; if claim_success, append V to hand
11. **update** (all players): when not game.any_call: game.blind_value = one random value from game.shoe (not removed); for each player with claim == 'BLIND' or not claim_success: append game.blind_value to hand, took_blind = true, blind_seen = game.blind_value (told privately)
12. **update** (all players): when not game.any_call: hand_sum = sum(hand); hand_size = length(hand); announce publicly for each player: discard_value, shed_count, claim, claim_success, took_blind, hand_size. B and hand contents stay private
13. **update** (all players): when not game.any_call and game.round == 30: revealed_hand = hand for all; game.lowest_sum = min hand_sum; round_score = if hand_sum == game.lowest_sum then 0 else hand_sum; total += round_score; game.game_over = true; announce publicly
14. **check** (all players): end the game if game.game_over or max over players of total >= 100

## Ending

- ends when: game.game_over == true or max over players of total >= 100
- ranked by: `0 - you.total` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their total, and lower is better. The player with the lowest total wins, and players tied at the lowest total share the win (a draw among them).

## Choices the source did not make

- 3 to 5 players, suggested 4: The designer suggested 4, which is kept. Claim collisions and Asaf ties need at least 3 rivals' worth of interaction, and above 5 the claim list and the announcements grow long while one player's choice matters little.
- Talk is a simultaneous poll broadcast to all: The rules say messages are written at the same time. Talk earns its place: players disagree over who claims which offered value, so announcing a claim can deter rivals or bait a collision.
- Ranking is 0 - total: The engine ranks highest first, and the lowest total wins.
- Asaf is tested as hand_sum == L and lowest_count == 1: This is an arithmetic form of 'every other hand_sum is strictly greater', using table attributes because players cannot be compared directly.
- game_over flag: This records the end that comes from a showdown in round 30, so a single check covers both endings.
- Strategy: A thoughtful player times a call against the public hand_sizes and the claims seen, avoids claiming values that others likely want, and uses talk to steer or bluff about claims.

## Simplifications

- Cards are stored as values only, with no suits or ranks: Only values matter in these rules; J, Q and K are all 10 and the Joker is 0.
- The skip of steps 5 to 11 after a call is done by putting the condition 'not game.any_call' on each later step: The step list is flat, but per-step conditions express the same skip exactly.
- Draws pick from game.shoe without removing the value: The source states the shoe is full for every draw.

## Unsupported (needs engine work)

- none
