# Lost Cities: Wager Draft

Two players draft face-up cards from a 27-card, three-colour deck over 12 rounds. They build rising expeditions, pay 3 for every burial, and score a secret colour Wager at double.

Players: 2 to 2, best with 2

## Parameters

- `deck_size` = 27
- `colours` = 3
- `min_card_value` = 2
- `max_card_value` = 10
- `rounds` = 12
- `row_size` = 2
- `wager_round` = 5
- `burial_penalty` = 3
- `empty_wager_score` = -15
- `empty_expedition_score` = 0
- `base_offset` = 10
- `wager_multiplier` = 2
- `bonus_threshold` = 25
- `bonus` = 10
- `cards_left_unrevealed` = 3

## Round

1. **update** (all players): round += 1; priority_seat = 1 if round is odd, else 2; taken = NONE; every player's choice = NONE. Announce: 'Round {round}: seat {priority_seat} has priority.'
2. **poll** (all players): when round == 5: each player's wager = their answer. Nobody sees another's wager. This runs before Card A and Card B are revealed.
3. **update** (all players): Draw one card at random from deck and remove it: card_a_colour and card_a_value are set from it. Draw another and remove it: card_b_colour and card_b_value are set from it. Announce both cards to both players.
4. **ask** (seat {priority_seat}): the priority player's choice = answer; taken = answer. Both players are told what was chosen.
5. **update** (seat {priority_seat}): If choice is A or B, place that card (colour C, value v) for the priority player. If v > C_top: C_top = v and C_sum += v. Otherwise burial += 3 and the card is removed from the game.
6. **ask** (the seat that is not priority_seat): choice = answer, except that choice = NONE if answer equals taken.
7. **update** (the seat that is not priority_seat): If choice is A or B, place that card (colour C, value v) for this player. If v > C_top: C_top = v and C_sum += v. Otherwise burial += 3 and the card is removed from the game.
8. **update** (all players): Any card in the row that nobody took is removed from the game. Announce both choices, where each card went (added or buried), every player's red/blue/green top and sum, and every player's burial.
9. **update** (all players): when round == 12: for each colour C, colour_score = (C_sum == 0 ? (wager == C ? -15 : 0) : (C_sum - 10) * (wager == C ? 2 : 1) + (C_sum >= 25 ? 10 : 0)); score = red score + blue score + green score - burial. Reveal each player's wager publicly and announce the totals. The 3 cards left in the deck are never revealed.
10. **check** (all players): end the game if round >= 12, otherwise continue

## Ending

- ends when: round >= 12
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their final total (the three colour scores minus the Burial penalty). The higher total wins, and equal totals share the win, which is a draw.

## Choices the source did not make

- Exactly 2 players, suggested 2: The designer fixed the table at 2. The draft is a head-to-head contest over a shared row, and the second pick depends on reading the one opponent.
- No talk step: The rules include no talk, and with two players in direct competition a message would add nothing the rules ask for.
- Cards stored as 'Colour-Value' strings in the deck, split into card_a/card_b colour and value attributes when drawn: This lets placement and scoring be done by plain arithmetic comparisons on numbers.
- The second player is still offered the taken card: The rules say that naming the taken card counts as NONE, so the option exists and is resolved to NONE.
- Strategy at the table: A thoughtful player times the Wager against the cards already seen in rounds 1 to 4. They also deny the opponent high cards, avoid burials that cost 3, and take NONE rather than bury a card.

## Simplifications

- The 'shuffle once, take the top two' draw is done as two random draws from the deck list each round: The engine draws at random from a list. This is equivalent to drawing from the top of a shuffled deck.
- Removed and buried cards are not kept in a discard list: The rules take them out of the game and never refer to them again. Only the burial counter matters.

## Unsupported (needs engine work)

- none
