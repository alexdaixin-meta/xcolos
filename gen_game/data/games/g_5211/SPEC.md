# 5211: Mirror Hands

Each player holds the same 14 cards. Over 7 rounds everyone plays two cards at once, and either the Kododos score (when exactly n-1 are played) or the single most-played colour that did not bust scores.

Players: 3 to 4, best with 4

## Parameters

- `rounds` = 7
- `hand_size` = 14
- `colours` = 4
- `min_card_value` = 1
- `max_card_value` = 3
- `kododos_per_hand` = 2
- `kododo_value` = 3
- `cards_per_round` = 2
- `bonus_extra_per_card` = 1
- `kododo_target_offset` = -1
- `bust_offset` = 1
- `score_weight_in_ranking` = 100

## Round

1. **poll** (all players): All messages are broadcast to everyone at once ({"to": "all", "text": "Seat {seat} says: {value}"}). Nothing is binding and no state changes.
2. **poll** (all players): Set first_card to the chosen card and remove one copy of it from hand. Nobody sees a choice until all are in.
3. **tell** (all players): Reveal every player's first_card to everyone.
4. **poll** (all players): Set second_card to the chosen card and remove one copy of it from hand. Nobody sees a choice until all are in.
5. **tell** (all players): Reveal every player's second_card to everyone.
6. **update** (all players): Set round_points = 0 for each player. Set kododo_count = the number of K among all first_card and second_card values. Set red_count, blue_count, green_count and yellow_count = the number of played cards starting with R, B, G and Y respectively.
7. **update** (all players): When kododo_count == n - 1: set scoring_colour = 'Kododo'; each player adds 3 x (their K cards this round) to round_points and score, and (their K cards this round) to scored_cards.
8. **update** (all players): When kododo_count != n - 1: a colour is eligible if 1 <= its count <= n. If exactly one eligible colour has the highest count among eligible colours, scoring_colour = that colour; otherwise scoring_colour = 'none'. If scoring_colour is a colour, each player sums the face values of their played cards of that colour, plus 1 per such card if bonus_colour == scoring_colour. They add that sum to round_points and score, and add the number of such cards to scored_cards. Kododos score nothing.
9. **tell** (all players): Announce scoring_colour, the colour counts, kododo_count, each player's round_points, score and scored_cards.
10. **update** (all players): round += 1.
11. **check** (all players): End the game if round >= 7, otherwise continue to the next round.

## Ending

- ends when: round >= 7
- ranked by: `you.score * 100 + you.scored_cards` (the highest wins; players level at the top share the win)
- decided by: Highest total score wins. Among players tied on score, the higher scored_cards count wins. Players still tied share the win, which is the draw.

## Choices the source did not make

- 3 to 4 players, suggested 4: The designer fixed 3-4 and suggested 4. Below 3 the n-1 Kododo threshold and the bust rule lose their tension, and there are only 4 bonus colours, so 4 is the maximum.
- Keep the simultaneous talk poll before the plays: The rules require it. Players disagree about which colour should score, because each has a secret bonus colour, and coordinating exactly n-1 Kododos invites bluffing. A simultaneous poll with broadcast matches 'at the same time, without seeing the others'.
- Card codes R1..Y3 and K: Each card needs a compact text form so hands can be lists and colour counts can be taken by first letter.
- Ranking expression score*100 + scored_cards: scored_cards can never exceed 14, so multiplying the score by 100 puts score first and scored cards second. Players still level share the win, which is the source's draw.

## Simplifications

- Hands are visible only to their owner, while played cards are public: This matches 'hands are private'. Tracking what others hold is left to the players, as the source intends.
- Reveal steps are tell steps over the public first_card and second_card: Cards placed in a poll stay unseen until all answers are in, which is the face-down placement; the tell then reveals them.

## Unsupported (needs engine work)

- none
