# Cockroach Poker: Straight Calls

Three players pass cards face-down with a creature claim. The receiver calls the claim true or false, and whoever is wrong about the card takes it face-up. Three face-up cards of one creature, or having to send from an empty hand, loses.

Players: 3 to 3, best with 3

## Parameters

- `deck_size` = 24
- `creature_kinds` = 4
- `copies_per_creature` = 6
- `hand_size_start` = 7
- `aside_cards` = 3
- `max_rounds` = 24
- `loss_same_creature` = 3
- `receiver_options` = 2

## Round

1. **tell** (all players): Announce round, sender, and each player's face_cockroach, face_rat, face_stinkbug, face_toad and hand_size.
2. **ask** (the sender (seat = sender)): Set card_in_play to the chosen creature. Remove one card of that creature from the sender's hand and decrease the sender's hand_size by 1.
3. **ask** (the sender (seat = sender)): Set claim to the answer, visible to all.
4. **ask** (the sender (seat = sender)): Set receiver to the chosen seat.
5. **ask** (the receiver (seat = receiver)): Set call to the answer.
6. **update** (all players): Set revealed_card = card_in_play and announce it. Let correct = (call == TRUE and card_in_play == claim) or (call == FALSE and card_in_play != claim). If correct, taker = sender, otherwise taker = receiver. Add 1 to the taker's face_<card_in_play> and to their face_total, and recompute the taker's max_face.
7. **update** (all players): Set sender = taker for the next round.
8. **check** (all players): If the taker's face count for revealed_card >= 3, set the taker's lost = 1 and game_over = 1, and end the game.
9. **check** (all players): If the new sender's hand_size == 0, set that player's lost = 1 and game_over = 1, and end the game.
10. **check** (all players): If round >= 24, set game_over = 1 and end the game with no loser. Otherwise add 1 to round.

## Ending

- ends when: game_over == 1, which happens when some player's lost == 1 or when round 24 has finished
- ranked by: `(1 - you.lost) * 1000000 - you.face_total * 10000 - you.max_face * 100 + you.hand_size` (the highest wins; players level at the top share the win)
- decided by: A player who lost can never rank above a player who did not. Among the others, fewest face-up cards ranks first, then the smaller most-common face-up creature count, then more cards left in hand. The highest value wins, and players level on all three tests share the win (a draw).

## Choices the source did not make

- Exactly 3 players, suggested 3: The designer fixed the game at 3. The deal of 7 + 7 + 7 + 3 aside uses the 24-card deck exactly, so another count would break the deal. Three seats also give the sender a real choice of whom to target.
- No talk phase: The rules say the claim is the only message.
- Single rank_by expression with weights 1000000 / 10000 / 100: This encodes not-lost first, then fewest face_total, then smaller max_face, then more hand_size. Each weight exceeds the largest possible value of the next term (face_total <= 24, max_face <= 6, hand_size <= 7).
- Strategy at the table: The sender reads which creatures each player already shows and steers cards toward the player closest to 3 of a kind, bluffing or telling the truth unpredictably. The receiver weighs the sender's hand and the creatures already exposed when calling.

## Simplifications

- A card is chosen by naming its creature: Copies of a creature are identical, so naming the creature is equivalent to picking the card.
- The sender's three decisions are three sequential asks: Only the sender answers them and the receiver does not see the card, so splitting them changes nothing.

## Unsupported (needs engine work)

- none
