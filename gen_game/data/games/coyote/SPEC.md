# Coyote: Around the Fire

Each player sees every card but their own. Players raise a claim about the table's total until someone calls Coyote, and whoever is wrong takes a token; three tokens and you are out.

Players: 3 to 4, best with 4

## Parameters

- `deck_size` = 20
- `count_minus2` = 1
- `count_minus1` = 2
- `count_0` = 3
- `count_1` = 3
- `count_2` = 3
- `count_3` = 3
- `count_4` = 2
- `count_5` = 2
- `count_max0` = 1
- `max0_code` = 100
- `cards_per_player` = 1
- `first_declaration_min` = -3
- `declaration_max` = 20
- `raise_min_step` = 1
- `tokens_to_eliminate` = 3
- `token_per_loss` = 1
- `max_rounds` = 40
- `first_opener_seat` = 1

## Round

1. **update** (all players): New hand. Reset deck to the 20 cards. Set every player's card to null. For each alive player, draw 1 card at random from deck into that player's card and remove it from deck. Set has_declaration = false, current_declaration = none, current_declarer = none, declarations = [], coyote_called = false, caller = none, hand_active = true.
2. **sync** (all players): Each player is sent the cards of every other alive player (card is visible to others) and never their own.
3. **tell** (all players): Announce: 'A new hand begins; seat {opener_seat} opens.'
4. **tell** (all players): Show current_declaration, current_declarer and declarations.
5. **ask** (the 1st alive seat clockwise starting at opener_seat): On a number: current_declaration = number, current_declarer = this seat, has_declaration = true, append (seat, number) to declarations. On 'coyote': coyote_called = true, caller = this seat.
6. **tell** (all players): Show current_declaration, current_declarer and declarations.
7. **ask** (the 2nd alive seat clockwise starting at opener_seat): as in the 1st turn
8. **tell** (all players): Show current_declaration, current_declarer and declarations.
9. **ask** (the 3rd alive seat clockwise starting at opener_seat): as in the 1st turn
10. **tell** (all players): Show current_declaration, current_declarer and declarations.
11. **ask** (the 4th alive seat clockwise starting at opener_seat): as in the 1st turn
12. **update** (all players): Work out the true total. Let S = the sum of all dealt cards that are not 100, and M = the highest dealt card that is not 100. true_total = S - (M if some dealt card == 100 and M > 0, else 0); only one copy of a tied highest card is cancelled. If true_total < current_declaration, then last_loser = current_declarer, else last_loser = caller. last_loser.tokens += 1. If last_loser.tokens >= 3, then last_loser.alive = false and alive_count -= 1. opener_seat = the next alive seat clockwise from the current opener_seat (if that opener was just eliminated, the next alive seat clockwise from their seat). hand_active = false.
13. **tell** (all players): Announce every alive player's card, true_total, last_loser and the tokens, and any elimination.
14. **check** (all players): End the game if alive_count == 1.
15. **update** (all players): round += 1
16. **check** (all players): End the game if round > 40. Any unfinished hand is discarded and no token is given.

## Ending

- ends when: alive_count == 1 or round > 40
- ranked by: `you.alive * 10 - you.tokens` (the highest wins; players level at the top share the win)
- decided by: Eliminated players rank below every alive player. If only one player is alive, that player wins. If 40 rounds pass, the alive player with the fewest tokens wins, and alive players tied for fewest share the result (a draw).

## Choices the source did not make

- 3 to 4 players, suggested 4: The designer chose 4. Three is the smallest table where each player reads two other cards and must guess their own while rivals push the bid. More than 4 would exceed the source's range and the 20-card deck design.
- No table talk step: The rules say declarations and calls are the only communication.
- Max→0 is stored as card code 100: Keeps every card a number, so the true total is pure arithmetic: code 100 counts as 0 and triggers cancelling the highest positive other card.
- Rank by alive*10 - tokens: Puts every alive player above every eliminated one and orders alive players by fewest tokens.
- Strategy noted: A good player infers their own card from the visible cards and from how others raise, and calls Coyote or raises depending on how plausible the claim is. A careless one declares at random.

## Simplifications

- A round is written as four conditional turn steps (1st to 4th alive seat clockwise from opener_seat), each skipped once Coyote is called or when fewer seats are alive: The step list is flat; per-step when-conditions reproduce variable turn counts and skipped turns.
- A tie for fewest tokens at round 40 is represented as a shared win among the tied players: The engine has no separate draw; tied top ranks share the result, which stands for the draw.

## Unsupported (needs engine work)

- none
