# Hidden Pie Ultimatum III

Three players take turns as Proposer over 12 rounds. Each Proposer splits a pot that only they can see between two Responders, and the deal passes if at least one Responder accepts.

Players: 3 to 3, best with 3

## Parameters

- `rounds` = 12
- `player_count` = 3
- `pot_value_1` = 70
- `pot_value_2` = 90
- `pot_value_3` = 110
- `pot_value_4` = 130
- `max_offer_total` = 130
- `min_offer` = 0
- `proposals_per_player` = 4
- `initial_score` = 0
- `rounds_per_block` = 3

## Round

1. **update** (all players): round += 1. Let k = (round-1) div 3 and j = (round-1) mod 3. proposer = j+1 if k is even, otherwise 3-j. responder1 = 2 if proposer == 1, else 1. responder2 = 2 if proposer == 3, else 3. Announce the round, the proposer, responder1 and responder2.
2. **update** (seat proposer): Draw: pick one value at random from pots_p{proposer}, set pot to it, and remove it from pots_p{proposer}.
3. **tell** (seat proposer): Privately tell the Proposer: 'This round's pot is {pot}.'
4. **poll** (all players): All messages are collected at the same time, then broadcast to all as 'Seat {seat} says: {value}'. Messages are not binding.
5. **ask** (seat proposer): offer_a = answer (the amount for responder1).
6. **ask** (seat proposer): offer_b = answer (the amount for responder2), so that offer_a + offer_b <= 130.
7. **tell** (all players): Announce: 'Seat {proposer} offers {offer_a} to Seat {responder1} and {offer_b} to Seat {responder2}.' The pot is not shown.
8. **poll** (seat responder1 and seat responder2): response1 = responder1's choice and response2 = responder2's choice. Neither Responder sees the other's choice before answering.
9. **update** (all players): If response1 == Accept or response2 == Accept: the Proposer's score += pot - offer_a - offer_b (this may be negative); if response1 == Accept, responder1's score += offer_a; if response2 == Accept, responder2's score += offer_b. If both are Reject, no score changes.
10. **tell** (all players): Reveal: 'The pot was {pot}. Seat {responder1}: {response1}. Seat {responder2}: {response2}. Scores: P1 {score of seat 1}, P2 {score of seat 2}, P3 {score of seat 3}.'
11. **check** (all players): End the game if round >= 12; otherwise continue to the next round.

## Ending

- ends when: round >= 12
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their total score after round 12. The highest total wins. Players tied at the top share the result, which stands in for the source's draw.

## Choices the source did not make

- 3 players (min 3, max 3, suggested 3): The designer fixed the table at 3. The Proposer order, the two-Responder structure and the 4 proposals each over 12 rounds only work with exactly 3 seats. The strategy is to infer the hidden pot from the offer size and from which values the Proposer has already used, to bluff about the pot in talk, and to decide whether to undercut a fellow Responder, since one acceptance is enough for the deal to pass.
- Talk is a simultaneous poll broadcast to all: The source requires all three messages to be written at the same time, unseen, and then shown to everyone. The players also disagree about the split, so talk earns its place.
- The pot lists are hidden table attributes (visibility none): If the remaining lists were public, they would show the drawn pot the moment it is removed. Their contents are announced at setup, and every used value is revealed at the end of each round, so players can still track what remains, as the source intends.
- The offer is asked as two sequential numbers, with b's range limited to 130 - a: A question takes one number, and limiting b's range enforces a + b <= 130 by arithmetic.

## Simplifications

- A tie for the highest score is a shared win rather than a draw: The engine ranks by one expression and has players level at the top share the win, with no separate draw outcome. A sole leader still wins outright, as in the source.

## Unsupported (needs engine work)

- none
