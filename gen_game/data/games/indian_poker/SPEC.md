# Forehead Poker Match

Over 16 hands, each player sees every other player's card but never their own, talks, bets and calls; the player with the most chips at the end wins.

Players: 4 to 6, best with 4

## Parameters

- `starting_chips` = 40
- `starting_pot` = 0
- `hands` = 16
- `elimination_below` = 4
- `ante` = 1
- `bet_min` = 1
- `bet_max` = 3
- `message_max_words` = 40
- `deck_size` = 52
- `cards_per_player` = 1
- `suits_per_rank` = 4

## Round

1. **update** (all players): ELIGIBILITY: every active player with chips < 4 gets active = false, and their chips stay as their final total. Then every player is reset for the hand: bet = 0, folded = false, called = false, card = '', card_value = 0, shown_card = ''. On the table, high_bet, caller_count and best_value are set to 0.
2. **check** (all players): The game ends if the number of players with active = true is 1 or fewer. Any pot is discarded.
3. **update** (all players): DEAL: deck is reset to all 52 cards. Each active player draws one card at random: it is removed from deck and its name is set as card, with its strength as card_value.
4. **sync** (all players): Each player is sent their state. They see the card and card_value of every other active player, but not their own.
5. **update** (all players): ANTE: each active player pays 1: chips -= 1 and pot += 1.
6. **poll** (every active player): TALK: once every message is in, each one is broadcast to all as 'Seat {seat} says: {value}'. No message binds anyone.
7. **poll** (every active player): FIRST BET: answers are collected simultaneously and stored. Nothing is shown until all are in.
8. **update** (every active player): On Fold: bet = 0 and folded = true. On Bet k: bet = k, chips -= k and pot += k. Then high_bet = the largest bet among active players.
9. **tell** (all players): REVEAL BETS: every player's step-5 choice (bet or fold) and H = high_bet are announced to everyone.
10. **poll** (every active player with bet >= 1): CALL OR FOLD: answers are collected simultaneously. This step is skipped if nobody bet.
11. **update** (every player asked in the previous step): On Call: called = true, chips -= (high_bet - bet) and pot += (high_bet - bet); the cost is 0 if bet = high_bet. On Fold: folded = true, and nothing put in this hand is returned. Then caller_count = the number of players with called = true, and best_value = the highest card_value among players with called = true (0 if there are none).
12. **update** (all players): SHOWDOWN: if caller_count >= 1, the player with called = true and card_value = best_value gets chips += pot, and then pot = 0. If caller_count = 0, pot is unchanged and carries over. Every player who was dealt a card gets shown_card = card. Then hand_number += 1.
13. **tell** (all players): All cards (shown_card), the callers, the winner of the pot (or that it carried over), the pot and everyone's chips are announced.
14. **check** (all players): The game ends if hand_number >= 16 or the number of players with active = true is 1 or fewer. Any remaining pot is discarded.

## Ending

- ends when: hand_number >= 16 or (count of players with active = true) <= 1
- ranked by: `you.chips` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their chips at the end. Eliminated players count with the chips they held when eliminated. The most chips wins, and players tied for the most share a draw.

## Choices the source did not make

- 4 to 6 players, suggested 4: Kept from the source and the designer. Four is the smallest table where several opponents' cards give real information about your own and where there are rivals to bluff. Above 6, each player's card information and message get lost in a long conversation.
- Talk kept as a simultaneous poll broadcast to all: The rules require simultaneous messages. Talk earns its place: each player knows facts the others need (their cards) and has reason to lie about them, so following a claim can cost chips.
- Card strength encoded as a number from 1 to 52 (rank_index*4 + suit_index): This lets the showdown winner be found by arithmetic (the highest card_value among callers) and exactly matches the rank-then-suit order in the rules.
- Eligibility check and early-end check placed at the start of each round, with a further end check after the showdown: Elimination happens at the start of a hand. Checking right after it stops a hand being played with a single active player.
- Strategy at the table: A thoughtful player infers their own card from the others' cards, their messages and their bets, and decides when to bluff, mislead others about their cards, or fold cheaply. A thoughtless player bets blindly.

## Simplifications

- Shuffling the full deck each hand is done by resetting the deck list to 52 cards and drawing at random: The engine has no shuffle; drawing at random from a full list is equivalent.
- The discarded leftover pot is simply ignored at the end: It does not affect anyone's chips or the ranking.

## Unsupported (needs engine work)

- none
