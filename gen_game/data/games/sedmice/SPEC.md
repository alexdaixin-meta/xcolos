# Sedmice Duel

A two-player trick-taking duel over 4 deals of 8-card hands. Sevens are wild, Aces and Tens score 10 each, and the leader may extend a trick once to win it back.

Players: 2 to 2, best with 2

## Parameters

- `deck_size` = 32
- `copies_per_rank` = 4
- `point_card_value` = 10
- `deals` = 4
- `max_rounds_per_deal` = 8
- `total_rounds` = 32
- `guaranteed_cards_per_player` = 3
- `extra_cards_dealt_per_player` = 5
- `hand_size` = 8
- `set_aside_cards` = 16
- `last_trick_bonus` = 10
- `max_extensions_per_trick` = 1
- `min_tricks_per_deal` = 4

## Round

1. **update** (all players): Set deck to the full 32 cards (four each of 7,8,9,10,J,Q,K,A). Set each hand to empty. For each player, move one '7', one 'A' and one '10' from deck to hand. Then draw 5 cards at random from deck into each hand, so each hand has 8 cards. Move the 16 remaining deck cards to set_aside. Set leader = 1 if deal_number is 1 or 3, else 2. Set new_deal = false.
2. **sync** (all players): Each player sees their own hand, both scores, deal_number and who leads.
3. **ask** (the leader (seat game.leader)): Remove the card from the leader's hand, append it to trick_cards and set led_rank to its rank.
4. **ask** (the follower (the seat that is not game.leader)): Remove the card from the follower's hand and append it to trick_cards. Set follower_winning = (card == led_rank or card == '7').
5. **ask** (the leader (seat game.leader)): If a card is chosen: remove it from the leader's hand, append it to trick_cards and set extended = true. If declined: nothing changes.
6. **ask** (the follower (the seat that is not game.leader)): Remove the card from the follower's hand and append it to trick_cards. Set follower_winning = (card == led_rank or card == '7').
7. **update** (all players): Set trick_winner = the follower if follower_winning is true, else leader. The trick winner's score += 10 × (count of 'A' in trick_cards + count of '10' in trick_cards). Announce trick_cards, the winner and the points scored.
8. **update** (all players): If both hands are empty: the trick winner's score += last_trick_bonus (10), clear set_aside, deal_number += 1 and new_deal = true. Otherwise leader = trick_winner. Announce the result.
9. **update** (all players): Reset for the next trick: trick_cards = [], led_rank = '', follower_winning = false, extended = false.
10. **check** (all players): End the game if deal_number > 4; otherwise continue.

## Ending

- ends when: game.deal_number > 4
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their total points across the 4 deals. The higher total wins, and equal totals share the win (a draw).

## Choices the source did not make

- Exactly 2 players, suggested 2: The designer fixed it as a duel. Its trick mechanics (one leader, one follower, an extension answered by the follower) only work with two players.
- No talk step: With two directly opposed players, talk gives nothing to coordinate and only adds words.
- Seat 1 is Player A and seat 2 is Player B: This maps the source's named players to seats so the first-lead rule can be applied.
- Cards are stored as rank strings in lists: Suits do not matter, so a rank fully identifies a card.
- The match loop runs trick by trick instead of in 32 fixed round slots: Skipped rounds in a deal do nothing, so ending each deal when the hands empty and counting deals gives the same game.

## Simplifications

- The 8-round deal slot is not counted explicitly; a deal ends when both hands are empty: The rules say the remaining rounds of a deal are skipped, so counting slots adds steps without changing play.
- Dealing is a single conditional update at the start of a round when new_deal is true: The engine's step list is flat, and a step with a when condition expresses dealing on the first round of each deal.

## Unsupported (needs engine work)

- none
