# Skull King: Blind Broadsides

A simultaneous trick-taking game over 10 rounds: players bid how many of 3 tricks they will win, then all play a card at once in each trick, scoring for exact bids and a bonus when the Mermaid captures the Skull King.

Players: 3 to 4, best with 4

## Parameters

- `rounds` = 10
- `hand_size` = 3
- `tricks_per_round` = 3
- `revealed_cards` = 3
- `bid_min` = 0
- `bid_max` = 3
- `deck_size` = 18
- `number_card_min` = 1
- `number_card_max` = 12
- `escape_count` = 2
- `escape_power` = 0
- `mermaid_power` = 20
- `pirate_a_power` = 30
- `pirate_b_power` = 31
- `skull_king_power` = 40
- `made_bid_points` = 30
- `mermaid_capture_bonus` = 10
- `miss_penalty_per_trick` = 10
- `initial_score` = 0
- `initial_round` = 0

## Round

1. **update** (all players): round += 1; for every player: tricks_won = 0, bonus = 0, hand = [], played = -1; revealed = []; trick = 0; deck = [1,2,3,4,5,6,7,8,9,10,11,12,0,0,20,30,31,40]. Announce the new round number.
2. **update** (all players): Deal: for each player, 3 times, pick a random card from deck, append it to that player's hand and remove it from deck (random picks are the shuffle).
3. **update** (all players): Reveal: 3 times, pick a random card from deck, append it to revealed and remove it from deck. The rest of deck stays hidden (3 cards with 4 players, 6 with 3).
4. **sync** (all players): Each player is sent their own hand, the revealed list, the scores and the round number.
5. **poll** (all players): Each player's bid = their answer. No one sees a bid until all are in.
6. **tell** (all players): Announce every player's bid to everyone.
7. **poll** (all players): Each player's played = the chosen card, which is removed from their hand. No one sees a choice until all are in.
8. **tell** (all players): Show every player's played card to everyone at once.
9. **update** (all players): winning_power = 20 if some player's played == 20 and some player's played == 40, otherwise the maximum of played over all players. The player whose played == winning_power gets tricks_won += 1. If that player's played == 20 and some played == 40, that player also gets bonus += 10. trick += 1. Announce the trick winner.
10. **repeat** (all players): Run the play, show and resolve steps again until trick == 3.
11. **update** (all players): Scoring for each player: if tricks_won == bid then score += 30 + bonus; otherwise score -= 10 * |bid - tricks_won| and the bonus is lost. Announce all scores.
12. **check** (all players): If round == 10 the game ends; otherwise go back to the first round step.

## Ending

- ends when: round == 10 (checked after the round's scoring)
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their final score after round 10. The highest score wins, and players tied for the highest score share the result (the source calls this a draw).

## Choices the source did not make

- 3 to 4 players, suggested 4: The designer suggests 4 and the source allows 3 to 4. The minimum is 3 because the rules need at least 3 players to guarantee a unique trick winner, given that only the two Escapes share a power. The maximum stays at 4 because 4 × 3 dealt cards plus 3 revealed cards leaves 3 hidden cards; larger tables would remove the hidden cards and break the source deck.
- Cards represented by their power numbers: Power is all the rules use. The two Escapes are both 0, and the labels are 0 Escape, 20 Mermaid, 30 Pirate A, 31 Pirate B, 40 Skull King.
- No talk step: The source states there is no discussion phase.
- Strategy at the table: A thoughtful player counts the revealed cards and their own hand to judge which high cards are still out, bids accordingly, then reads the public bids and tricks so far to decide when to dump a winner or duck with a low card. They also hold the Mermaid back for a trick where the Skull King is likely to appear.
- Shuffling as random draws from the deck list: Drawing a random card from a freshly reset deck is equivalent to dealing from a shuffled deck.
- A table attribute winning_power and a trick counter: Used to resolve each trick by arithmetic and to repeat the trick steps exactly 3 times.
- played initial value -1: Marks 'no card played yet'. -1 is below every real power.

## Simplifications

- A tie for the highest score is a shared win rather than a draw: The engine ranks by one expression and players level at the top share the win, which corresponds to the source's draw.
- The three tricks use a repeat over the play, show and resolve steps: The engine runs a flat step list and repeats steps until a condition holds.

## Unsupported (needs engine work)

- none
