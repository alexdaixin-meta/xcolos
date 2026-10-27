# Budget English Auctions

Over 8 rounds, players with fixed coin budgets bid for items whose value only they can see, in short ascending auctions of up to 3 simultaneous bidding steps; the winner has the highest total of value minus price.

Players: 3 to 5, best with 4

## Parameters

- `starting_coins` = 40
- `starting_score` = 0
- `card_min_value` = 2
- `card_value_step` = 2
- `card_max_value` = 16
- `deck_size` = 8
- `rounds` = 8
- `bidding_steps_max` = 3
- `min_raise_increment` = 2
- `initial_standing_bid` = 0
- `no_leader_code` = 0
- `priority_raise_weight` = 10000
- `priority_score_offset` = 500
- `priority_score_weight` = 10
- `rank_score_weight` = 1000

## Round

1. **update** (all players): round += 1; start_seat = ((round-1) mod n)+1; standing_bid = 0; leader = 0; step = 0; bidding_open = true; revealed_value = 0; for every player: active = true, raise = 0, priority = 0; for every player: draw one card at random from their deck, set value to it and remove it from deck.
2. **sync** (all players): Each player privately sees their own value, coins and score, along with all public coins and scores.
3. **poll** (all players): All messages are collected at once and then broadcast {"to": "all", "text": "Seat {seat} says: {value}"}. Messages are not binding and change no state.
4. **update** (all players): BIDDING STEP START (when bidding_open): step += 1; every active player who is not the leader and has coins < standing_bid + 2 gets active = false (forced drop); raise = 0 and priority = 0 for all.
5. **poll** (every active player whose seat is not leader (when bidding_open)): Answers are gathered at once, and nobody sees another's answer until all are in. On DROP: active = false and raise = 0. On a number: raise = that number, and the player stays active.
6. **update** (all players): (when bidding_open) For every player with raise > 0: priority = raise*10000 + (500 - score)*10 - ((seat - start_seat + n) mod n). If any raise > 0: standing_bid = max raise, and leader = the seat with the highest priority (highest raise, then lowest score, then the first seat counting upward from start_seat). Outbid raisers remain active. If no player has raise > 0: bidding_open = false. If step = 3: bidding_open = false.
7. **tell** (all players): Announce step, standing_bid, leader (or 'no leader') and the seats that dropped this step.
8. **repeat** (all players): Repeat from BIDDING STEP START (the update, poll, update and tell steps) until bidding_open = false. This happens at the latest after step 3.
9. **update** (the leader): When leader > 0: the leader's coins -= standing_bid; the leader's score += (leader's value - standing_bid); revealed_value = the leader's value. When leader = 0, nothing changes and the item is unsold.
10. **tell** (all players): If leader > 0: 'Seat {leader} buys for {standing_bid}; their value was {revealed_value}.' Otherwise: 'The item goes unsold.' No other value is revealed.
11. **check** (all players): If round >= 8, end the game. Otherwise continue to the next round. Unspent coins carry over.

## Ending

- ends when: round >= 8
- ranked by: `you.score * 1000 + you.coins` (the highest wins; players level at the top share the win)
- decided by: The highest score (total of value minus price over items won) wins. A tie on score is broken by more coins remaining. Players still tied share the win, which is a draw among them.

## Choices the source did not make

- 3 to 5 players, suggested 4: The designer's suggested size of 4 is kept. The minimum is 3 because an auction needs at least two rivals for a bidder, so that the tie-breaks and the budget pressure matter. The maximum stays at 5 because with more seats one player's bids rarely decide an item and the talk becomes long.
- Talk kept as a simultaneous poll broadcast to all: The source requires simultaneous messages. Talk earns its place because players disagree about who should win each item and can bluff about their values or signal restraint, and none of it is binding.
- Strategy at the table: A thoughtful player bids below their value, saves coins for high-value rounds since the deck's remaining cards are known to them, reads rivals' coins and messages, and uses the 3-step limit to jump-bid. A thoughtless player overpays early or drops good items.
- Tie-break encoded as a priority number: The priority raise*10000 + (500 - score)*10 - ((seat - start_seat + n) mod n) orders by highest raise, then lowest score, then seat order from start_seat. Scores stay within about -40 to 128, so the terms never overlap.
- Ranking expression score*1000 + coins: Coins never exceed 40, so coins act only as a tie-break after score, as the source states.
- Forced drop applied at the start of each step: The source says such a player must drop. Applying it before the poll means they are never offered a choice they cannot make.
- Card values given as card_min_value 2, card_value_step 2 and card_max_value 16: Parameters must be single numbers. The deck 2, 4, ..., 16 is every value from the minimum to the maximum in steps of 2, which is 8 cards (deck_size).

## Simplifications

- The secretly shuffled deck is modelled as random draws without replacement from the player's deck list: This is equivalent to drawing in order from a separately shuffled deck, and the order stays secret even from its owner.
- The 3 bidding steps are a repeated block of four steps that stops when bidding_open becomes false: The engine runs steps in a flat list with repeat. A step where nobody raises, or step 3, closes the bidding.

## Unsupported (needs engine work)

- none
