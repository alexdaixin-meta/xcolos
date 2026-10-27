# Psychological Jujitsu: Hidden Favourites

Players secretly bid cards from identical 1-13 hands for 13 prizes. A bid value matched by anyone is cancelled, the highest unique bid wins, and each player has a secret favourite prize value worth +5.

Players: 3 to 4, best with 3

## Parameters

- `hand_size` = 13
- `card_min` = 1
- `card_max` = 13
- `prize_pile_size` = 13
- `rounds` = 13
- `bonus_value_min` = 5
- `bonus_value_max` = 9
- `bonus_points` = 5
- `message_max_words` = 40
- `starting_score` = 0

## Round

1. **update** (all players): round_no += 1. One value is drawn at random from prize_pile into prize and removed from prize_pile. Every player's bid_unique, won_round and bonus_scored are set to false, and winning_bid is set to 0.
2. **tell** (all players): Announce: 'Round {round_no}: the prize is {prize}.' Also announce every player's hand, every score and the prize_pile values still remaining.
3. **poll** (all players): Each player's message is set to their text. Then broadcast {"to": "all", "text": "Seat {seat} says: {value}"}. Messages are not binding.
4. **poll** (all players): Each player's bid is set to the chosen card. If a player gives an invalid answer or none, bid = the minimum of their hand.
5. **update** (all players): Each player's bid is removed from their hand. For each player, bid_unique = (number of other players whose bid equals this bid) == 0. winning_bid = the maximum bid among players with bid_unique true, or 0 if no player has bid_unique true. For each player, won_round = bid_unique and bid == winning_bid.
6. **update** (all players): For the player with won_round true: score += prize, and if prize == bonus, then score += 5 and bonus_scored = true.
7. **tell** (all players): Announce every player's bid, the winner of the prize (or 'cancelled: nobody scores' if winning_bid == 0) and the new scores. If bonus_scored is true for the winner, announce only '+5 bonus' together with the winner's new total, not the bonus value.
8. **check** (all players): If round_no == 13, reveal every player's bonus to everyone and end the game. Otherwise continue with the next round.

## Ending

- ends when: round_no == 13
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their final score. The highest score wins, and players tied at the top share the win (a draw among them).

## Choices the source did not make

- 3 to 4 players, suggested 3: The designer chose 3, so it is kept. Cancellation of matching bids needs at least 3 bidders to create the outbidding-by-colliding tension; with 2, any tie simply voids the round. The maximum stays at the source's 4, since more bidders make most rounds collapse into cancellations and drown out the hidden-favourite signal.
- Talk kept as a simultaneous poll with broadcast: The source specifies simultaneous talk. Players genuinely disagree, since everyone wants the prize, so bluffing about intended bids or hinting at a favourite gives others something to reason about.
- Strategy check: A thoughtful player avoids bids others are likely to duplicate, saves high cards for high prizes, uses talk to provoke collisions between rivals, and infers rivals' bonus values from how eagerly they chase mid prizes.
- Hands made public: The rules announce every remaining hand each round, and hands are deducible from the revealed bids anyway.

## Simplifications

- The shuffled face-down prize pile is modelled as a public list of remaining values with a random draw each round: The rules announce the remaining prize values each round; only the order is hidden, and a random draw reproduces that.
- The '+5 bonus' announcement and the end-of-game bonus reveal are done with tell steps: The bonus attribute stays visible only to its owner until the game ends.

## Unsupported (needs engine work)

- none
