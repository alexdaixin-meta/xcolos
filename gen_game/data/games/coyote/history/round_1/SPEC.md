# Coyote Lap

Each player sees every card but their own. Players bid upward on the true total of the cards in play until someone calls Coyote, and whoever is wrong takes a token. After 12 hands the fewest tokens wins.

Players: 3 to 4, best with 4

## Parameters

- `deck_size` = 33
- `count_minus_10` = 1
- `count_minus_5` = 2
- `count_0` = 3
- `count_each_1_to_5` = 4
- `count_10` = 3
- `count_15` = 2
- `count_20` = 1
- `count_max_to_zero` = 1
- `max_to_zero_code` = 100
- `hands` = 12
- `declaration_min` = -30
- `declaration_max` = 60
- `raise_min_step` = 1
- `tokens_per_loss` = 1
- `starting_tokens` = 0
- `cards_per_player` = 1

## Round

1. **update** (all players): Reset deck to the full 33-card list. For each player, draw one card at random from deck: set that player's card to its value and remove it from deck. Set caller = 0, current_declarer = 0, hand_loser = 0, true_total = 0, bidding_open = true.
2. **sync** (all players): Each player privately sees the card of every other player (card is visible to others) but never their own.
3. **ask** (the opener (seat opener_seat)): Set current_declaration = answer and current_declarer = opener_seat. Announce to all: 'Seat {opener_seat} opens at {current_declaration}.'
4. **ask** (responder 1: seat ((opener_seat) mod N) + 1, when bidding_open): If call_coyote: set caller = this seat, set bidding_open = false, and announce the call. If raise: go on to the next step.
5. **ask** (responder 1, when bidding_open and they chose raise): Set current_declaration = answer and current_declarer = this seat. Announce the declaration to all.
6. **ask** (responder 2: seat ((opener_seat + 1) mod N) + 1, when bidding_open): If call_coyote: set caller = this seat, set bidding_open = false, and announce the call. If raise: go on to the next step.
7. **ask** (responder 2, when bidding_open and they chose raise): Set current_declaration = answer and current_declarer = this seat. Announce the declaration to all.
8. **ask** (responder 3: seat ((opener_seat + 2) mod N) + 1, only when N = 4 and bidding_open): If call_coyote: set caller = this seat, set bidding_open = false, and announce the call. If raise: go on to the next step.
9. **ask** (responder 3, only when N = 4, bidding_open and they chose raise): Set current_declaration = answer and current_declarer = this seat. Announce the declaration to all.
10. **update** (the opener, when bidding_open): Automatic call: set caller = opener_seat and bidding_open = false. Announce: 'Everyone raised; Seat {opener_seat} calls Coyote automatically on {current_declaration}.'
11. **update** (table): true_total = sum of every card that is not 100. If some player's card = 100, subtract the maximum of the other players' cards (exactly one copy of the highest, even if that value is negative).
12. **update** (table): If true_total < current_declaration: the current_declarer's tokens += 1 and hand_loser = current_declarer. Otherwise: the caller's tokens += 1 and hand_loser = caller.
13. **tell** (all players): Reveal every player's card (100 shown as 'Max→0'), plus true_total, current_declaration and hand_loser: 'Cards: {cards}. True total {true_total} against a declaration of {current_declaration}. Seat {hand_loser} takes a Coyote token.'
14. **update** (table): opener_seat = (opener_seat mod N) + 1; hand_number += 1.
15. **check** (table): If hand_number > 12, end the game; otherwise continue to the next hand.

## Ending

- ends when: hand_number > 12
- ranked by: `0 - you.tokens` (the highest wins; players level at the top share the win)
- decided by: A player's standing is the negative of their Coyote tokens. The player with the fewest tokens wins, and players tied for the fewest share the result (the source calls this a draw).

## Choices the source did not make

- 3 to 4 players, suggested 4: The designer suggests 4, so it is kept. 3 is the minimum because with fewer players there is too little hidden information to reason about and no chain of raises. 4 is the maximum the source allows, and more responders would push declarations past what the deck can support.
- Max→0 is stored as the code 100 in card: Cards must be numbers so the total can be computed. 100 is never a face value, so the code is unambiguous, and the reveal shows it as 'Max→0'.
- No free-talk step before the bidding: The source has no table talk. Information is carried by the declarations themselves, and adding talk would add a mechanic.
- Strategy at the table: Each player sums the cards they can see and estimates their own unseen card from the deck odds, watching for a visible Max→0. They then read the other players' declarations as signals about their own card. A thoughtful player raises only when the expected total supports it, and calls when the current bid outruns what they see.

## Simplifications

- The clockwise response sequence is written as fixed responder slots (responder 1, 2 and 3 relative to the opener), each a raise-or-call choice followed by a number step for raises: The engine runs flat step lists. Per-slot steps with when-conditions interleave the choice and the amount for each responder in order.
- A tie for the fewest tokens is a shared win rather than a declared draw: The engine's ranking makes players level at the top share the win. This matches the source's draw outcome in effect.
- The deck is reset and redealt with random draws each hand: Shuffling is modelled as drawing at random from the deck list.

## Unsupported (needs engine work)

- none
