# Roach Bluff

A bluffing game in which players pass face-down creature cards with true or false claims; whoever ends up with three face-up cards of one creature, or has no card to send, loses.

Players: 3 to 4, best with 4

## Parameters

- `deck_size` = 24
- `cards_per_creature` = 6
- `creature_kinds` = 4
- `hand_size_4_players` = 6
- `hand_size_3_players` = 8
- `lose_at_faceup_of_one_creature` = 3
- `max_rounds` = 24
- `first_sender_seat` = 1
- `loser_rank_penalty` = 1000

## Round

1. **update** (engine): Set passer=0, passed=false, response='', claim='', card_in_play=''.
2. **tell** (all players): Announce every player's roach_up, rat_up, fly_up, toad_up, faceup_total and hand_size.
3. **ask** (seat {sender}): card_in_play = the chosen card; remove that card from the sender's hand; sender's hand_size -= 1. The answer is shown only to the sender.
4. **ask** (seat {sender}): claim = the answer; claimer = sender.
5. **ask** (seat {sender}): receiver = the chosen seat.
6. **tell** (all players): Announce: 'Seat {sender} sends a card to seat {receiver}, claiming it is a {claim}.'
7. **ask** (seat {receiver}): response = the answer, announced to all. If the answer is PASS: passed = true, passer = receiver, claimer = receiver.
8. **tell** (seat {passer} (when passed)): Privately show card_in_play to the passer.
9. **ask** (seat {passer} (when passed)): claim = the answer.
10. **ask** (seat {passer} (when passed)): receiver = the chosen seat.
11. **tell** (all players (when passed)): Announce: 'Seat {passer} passes the card to seat {receiver}, claiming it is a {claim}.'
12. **ask** (seat {receiver} (when passed)): response = the answer, announced to all.
13. **update** (engine): correct = (response=='TRUE' and card_in_play==claim) or (response=='FALSE' and card_in_play!=claim). taker = claimer if correct, else receiver. Add 1 to the taker's count for the card_in_play creature (roach_up, rat_up, fly_up or toad_up). Add 1 to the taker's faceup_total. last_revealed = card_in_play. sender = taker. round_count += 1.
14. **tell** (all players): Announce: 'The card was a {last_revealed}. Seat {taker} takes it face-up and sends next.'
15. **update** (engine): If the taker has roach_up>=3 or rat_up>=3 or fly_up>=3 or toad_up>=3: taker.lost = true and game_over = true. Otherwise, if the sender's hand_size == 0: that player's lost = true and game_over = true.
16. **check** (engine): End the game if game_over == true or round_count >= 24. Otherwise continue.

## Ending

- ends when: game_over == true or round_count >= 24
- ranked by: `0 - you.faceup_total - 1000 * you.lost` (the highest wins; players level at the top share the win)
- decided by: The player who triggered the end (three face-up cards of one creature, or no card to send) loses. Among the others, the player with the fewest total face-up cards wins. Players tied for fewest share the win, which stands for the source's draw.

## Choices the source did not make

- 3 to 4 players, suggested 4: The designer set 4 as the suggested size. At least 3 players are needed so that a pass can reach someone who is neither the sender nor the passer. The deck of 24 only deals evenly to 3 or 4 players, so the maximum is 4.
- No talk step: The rules forbid table talk; the claims are the only communication. Players reason by reading the face-up piles and by bluffing with claims that target a near-loser.
- Rank expression 0 - faceup_total - 1000*lost: This makes the loser rank below everyone, and among the rest the fewest face-up cards ranks highest.
- Pass steps run as individual steps with a 'when passed' condition: Each pass step is a single step with an arithmetic condition, not a chosen block, so the engine supports it directly.

## Simplifications

- A tie for fewest face-up cards is a shared win rather than a draw: The engine has no separate draw outcome; players level at the top share the win.
- Sending is split into three questions: the card, then the claim, then the receiver: Each engine question takes a single answer. The card choice is kept private to the sender.

## Unsupported (needs engine work)

- none
