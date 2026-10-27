# Task: write the XColos game file for "Hanabi Trio"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 4; set `meta.players` to {"min": 2, "max": 4, "suggested": 3} (the suggested size is the one the game plays best at).

R1 Cards. The deck has 30 cards. For each colour Red (R), Green (G) and Blue (B) there are three 1s, two 2s, two 3s, two 4s and one 5. A face is written as colour letter plus rank, e.g. R1, G4, B5.

R2 Shuffle and IDs. At setup the 30 faces are shuffled once into the list deck_faces. The list deck_ids is #1, #2, …, #30 in order, so deck_ids position k and deck_faces position k always belong to the same card. An ID never reveals a face. The front of both lists is the top of the deck. deck_faces is hidden from every player.

R3 Single source of truth. A card's face exists in exactly one place: the faces list paired with the IDs list that currently holds it. That is deck_ids/deck_faces, or a seat's hand_ids/hand_faces, or the discard_pile entry once revealed. Whenever a card moves, its ID and its face are removed from the same index of their two lists and moved together. There is no other record of faces.

R4 Hand sizes. With 2 players each hand has 5 cards and deck_count starts at 20. With 3 players each hand has 4 cards and deck_count starts at 18. With 4 players each hand has 4 cards and deck_count starts at 14.

R5 Dealing. Seat 1 takes the top hand-size cards (ID and face together, in order), then seat 2 takes the next hand-size cards, and so on up to the last seat. Example: with 3 players, seat 1 holds #1-#4, seat 2 #5-#8 and seat 3 #9-#12, and the deck holds #13-#30. deck_count always equals the number of entries in deck_ids.

R6 Visibility. Every player sees every seat's hand_ids. Every player sees every other seat's hand_faces, but never their own. The piles, hint_tokens, fuses, deck_count, discard_pile, action_log, team_score and turns_played are public.

R7 Starting state. pile_red, pile_green and pile_blue start at 0. hint_tokens starts at 8 (maximum 8). fuses starts at 3. team_score starts at 0. discard_pile and action_log start empty. turns_played starts at 0. final_turns_left starts at -1. active_seat starts at 1.

R8 Turn order. One round is one turn by the active seat. Seats act in order 1, 2, …, num_players, then seat 1 again, starting with seat 1. Only the active seat is asked to choose.

R9 Legal options. At the start of each turn, legal_options for the active seat is built from that seat's current hand_ids only. The options are:
- "PLAY #id" for each ID in its hand.
- "DISCARD #id" for each ID in its hand.
- If hint_tokens is at least 1, "HINT s v" for each other seat s and each value v in R, G, B, 1, 2, 3, 4, 5 that matches at least one card in seat s's hand.
Every other seat's legal_options is empty. The active seat chooses exactly one option.

R10 Hint. hint_tokens falls by 1. A line is added to action_log naming the giver, the receiver, the value and every ID in the receiver's hand that matches it, e.g. "turn 4: seat 1 hints seat 2 R = #5, #7". Hints are public and are not otherwise stored. No card moves.

R11 Finding the card. For PLAY or DISCARD of an ID, find that ID's index i in the active seat's hand_ids. The card's face is hand_faces[i]. Remove index i from both hand_ids and hand_faces.

R12 Play succeeds. The play succeeds if the card's rank is exactly 1 more than its colour's pile. That pile becomes the card's rank and team_score rises by 1. If the rank is 5 and hint_tokens is below 8, hint_tokens rises by 1. action_log records "turn t: seat a plays #id = face, success".

R13 Play fails. If the play does not succeed, fuses falls by exactly 1. "#id=face" is added to the end of discard_pile, and action_log records the failure with the face.

R14 Discard. The face is revealed and "#id=face" is added to the end of discard_pile. hint_tokens rises by 1, to at most 8: discarding with 8 tokens leaves 8. action_log records "turn t: seat a discards #id = face".

R15 Drawing. After a PLAY or DISCARD, if deck_ids is not empty, the front entry of deck_ids and the front entry of deck_faces are removed together and added to the end of the active seat's hand_ids and hand_faces. deck_count is set to the length of deck_ids. If this draw made deck_count 0 and final_turns_left is -1, set final_turns_left to num_players + 1. After a HINT, nobody draws.

R16 End of turn. Every seat's total is set to team_score. turns_played rises by 1. If final_turns_left is above 0, it falls by 1. active_seat passes to the next seat (after the last seat, seat 1).

R17 Game end. The game ends at the end of a turn if any of these holds:
- fuses is 0;
- team_score is 15;
- final_turns_left is 0, meaning every player, including the one who drew the last card, has had one more turn after the deck emptied;
- turns_played is 40.

R18 No talk. There is no message phase. Players may communicate only through the moves above.

R19 Result. Every seat whose total is at least 10 wins. Since all totals equal team_score, the team either wins together (team_score 10 or more) or loses together (below 10). Pile progress counts even if the game ended on the third fuse.

How the winner is decided: Cooperative target. When the game ends, every seat's total equals team_score, which is pile_red + pile_green + pile_blue (maximum 15). Every seat whose total reaches 10 wins, so all seats win together if team_score ≥ 10. Otherwise no seat wins and the game counts as a loss for the whole team. Pile progress is counted even when the game ended because fuses reached 0.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Hanabi Trio (2 to 4 players, best with 3)

A cooperative card game. Each player sees everyone's cards but their own and plays coloured cards 1 to 5 in order onto three piles, using hints, discards and plays; the team wins together if it scores 10 or more of the 15 possible points.

STATE (every item below must exist in the file):
  - each player: hand_ids (list, starts []); everyone sees it. IDs (#k) of the cards this seat holds, in order; seen by everyone (R6)
  - each player: hand_faces (list, starts []); everyone but its owner sees it. Faces (e.g. R1) of the held cards, index-paired with hand_ids; every seat except the owner sees them (R6)
  - each player: legal_options (list, starts []); only its owner sees it. Options offered this turn; filled only for the active seat, empty for all others (R9)
  - each player: total (number, starts 0); everyone sees it. This seat's score; set to team_score at the end of every turn (R16)
  - the table: deck_ids (list, starts []); hidden from all players. IDs of the cards still in the deck, front = top; index-paired with deck_faces
  - the table: deck_faces (list, starts []); hidden from all players. Faces of the cards still in the deck, shuffled once at setup, front = top; hidden from every player (R2)
  - the table: deck_count (number, starts 0); everyone sees it. Always the number of entries in deck_ids
  - the table: pile_red (number, starts 0); everyone sees it. Highest red rank played successfully
  - the table: pile_green (number, starts 0); everyone sees it. Highest green rank played successfully
  - the table: pile_blue (number, starts 0); everyone sees it. Highest blue rank played successfully
  - the table: hint_tokens (number, starts 8); everyone sees it. Hint tokens available, 0 to 8
  - the table: fuses (number, starts 3); everyone sees it. Fuses left; the game ends when this reaches 0
  - the table: discard_pile (list, starts []); everyone sees it. Revealed discarded or failed cards as '#id=face', in order
  - the table: action_log (list, starts []); everyone sees it. One public line per turn: hints with matched IDs, plays and discards with faces
  - the table: team_score (number, starts 0); everyone sees it. pile_red + pile_green + pile_blue (0 to 15)
  - the table: turns_played (number, starts 0); everyone sees it. Turns completed so far
  - the table: final_turns_left (number, starts -1); everyone sees it. -1 until the deck empties; then counts down the remaining turns
  - the table: active_seat (number, starts 1); everyone sees it. Seat whose turn it is
  - parameters, each kept as a table attribute: deck_size = 30, num_colours = 3, copies_of_rank_1 = 3, copies_of_rank_2 = 2, copies_of_rank_3 = 2, copies_of_rank_4 = 2, copies_of_rank_5 = 1, max_rank = 5, hand_size_2_players = 5, hand_size_3_players = 4, hand_size_4_players = 4, deck_count_start_2_players = 20, deck_count_start_3_players = 18, deck_count_start_4_players = 14, pile_start = 0, hint_tokens_start = 8, hint_tokens_max = 8, hint_cost = 1, discard_hint_gain = 1, five_played_hint_gain = 1, fuses_start = 3, fuse_loss_per_failed_play = 1, score_per_successful_play = 1, max_team_score = 15, win_threshold = 10, max_turns = 40, final_turns_left_start = -1, final_turns_extra = 1, team_score_start = 0, turns_played_start = 0, first_active_seat = 1

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Build the 30 faces: for each of R, G, B, three 1s, two 2s, two 3s, two 4s and one 5. Shuffle them once into deck_faces.
  2. Set deck_ids to #1, #2, ..., #30 in order, so deck_ids[k] and deck_faces[k] are the same card.
  3. Hand size is 5 with 2 players and 4 with 3 or 4 players.
  4. Seat 1 takes the front hand-size entries of deck_ids and deck_faces together, in order, into hand_ids and hand_faces. Then seat 2 takes the next hand-size entries, and so on to the last seat. With 3 players, seat 1 holds #1-#4, seat 2 #5-#8, seat 3 #9-#12, and the deck holds #13-#30.
  5. Set deck_count to the length of deck_ids: 20 with 2 players, 18 with 3, 14 with 4.
  6. Set pile_red, pile_green, pile_blue = 0, hint_tokens = 8, fuses = 3, team_score = 0, discard_pile = [], action_log = [], turns_played = 0, final_turns_left = -1, active_seat = 1, and every seat's total = 0.
  7. Sync: each seat receives every seat's hand_ids, every other seat's hand_faces (never its own) and all public table attributes.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] seat {active_seat}. What happens: Set legal_options of the active seat to: 'PLAY #id' for each id in its hand_ids; 'DISCARD #id' for each id in its hand_ids; and, if hint_tokens >= 1, 'HINT s v' for each other seat s and each v in {R,G,B,1,2,3,4,5} where at least one face in seat s's hand_faces has colour letter v or rank v. Set every other seat's legal_options to [].
  2. [sync] all players. What happens: Each seat receives its permitted view: all hand_ids, other seats' hand_faces, the piles, hint_tokens, fuses, deck_count, discard_pile, action_log, team_score, turns_played, active_seat, and its own legal_options.
  3. [ask] seat {active_seat} answers: exactly one option from the active seat's legal_options. What happens: Store the chosen option as this turn's choice.
  4. [update] seat {active_seat}. What happens: When the choice is 'HINT s v': hint_tokens -= 1. Append to action_log 'turn {turns_played+1}: seat {active_seat} hints seat s v = ' followed by every id in seat s's hand_ids whose paired face matches v. No card moves.
  5. [update] seat {active_seat}. What happens: When the choice is 'PLAY #id': find index i of #id in the active seat's hand_ids, take face = hand_faces[i], and remove index i from both hand_ids and hand_faces. If face rank == (pile of face colour) + 1: set that pile to the rank, team_score += 1, if rank == 5 and hint_tokens < 8 then hint_tokens += 1, and append 'turn t: seat a plays #id = face, success' to action_log. Otherwise: fuses -= 1, append '#id=face' to discard_pile, and append 'turn t: seat a plays #id = face, failure' to action_log.
  6. [update] seat {active_seat}. What happens: When the choice is 'DISCARD #id': find index i of #id in the active seat's hand_ids, take face = hand_faces[i], and remove index i from both lists. Append '#id=face' to discard_pile, set hint_tokens = min(8, hint_tokens + 1), and append 'turn t: seat a discards #id = face' to action_log.
  7. [update] seat {active_seat}. What happens: When the choice was PLAY or DISCARD and deck_ids is not empty: remove the front entry of deck_ids and of deck_faces together and append them to the end of the active seat's hand_ids and hand_faces. Set deck_count = length of deck_ids. If deck_count is now 0 and final_turns_left == -1, set final_turns_left = num_players + 1. After a HINT nobody draws.
  8. [update] all players. What happens: Set every seat's total = team_score. turns_played += 1. If final_turns_left > 0, final_turns_left -= 1. active_seat = active_seat + 1, or 1 after the last seat.
  9. [tell] all players. What happens: Announce the last action_log line with the current pile_red, pile_green, pile_blue, hint_tokens, fuses, deck_count and team_score.
  10. [check] all players. What happens: End the game if fuses == 0 or team_score == 15 or final_turns_left == 0 or turns_played == 40; otherwise continue with the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the deck is built, then it has 30 cards: for each of R, G, B, three 1s, two 2s, two 3s, two 4s and one 5.
  R2. When setup runs, then deck_faces is a shuffle of the 30 faces and deck_ids is #1..#30 in order, with deck_ids[k] paired to deck_faces[k].
  R3. When any card moves, then its ID and face are removed from the same index of their paired lists and moved together, and no other record of the face exists.
  R4. When there are 2 players, then each hand has 5 cards and deck_count starts at 20.
  R5. When there are 3 players, then each hand has 4 cards and deck_count starts at 18.
  R6. When there are 4 players, then each hand has 4 cards and deck_count starts at 14.
  R7. When dealing with 3 players, then seat 1 holds #1-#4, seat 2 #5-#8, seat 3 #9-#12, and deck_ids holds #13-#30.
  R8. When any step ends, then deck_count equals the number of entries in deck_ids.
  R9. When a seat views the table, then it sees every seat's hand_ids and every other seat's hand_faces, but never its own hand_faces.
  R10. When the game starts, then the piles are 0, hint_tokens is 8, fuses is 3, team_score is 0, discard_pile and action_log are empty, turns_played is 0, final_turns_left is -1 and active_seat is 1.
  R11. When a turn begins, then only the active seat is asked; seats act in order 1..num_players and then seat 1 again.
  R12. When a turn begins, then the active seat's options are 'PLAY #id' and 'DISCARD #id' for each id in its hand, and every other seat's legal_options is empty.
  R13. When hint_tokens >= 1, then the active seat is also offered 'HINT s v' for each other seat s and each v in R,G,B,1-5 that matches at least one card in seat s's hand; when hint_tokens is 0, no HINT is offered.
  R14. When a seat hints, then hint_tokens falls by 1, action_log gains a line naming giver, receiver, value and every matching ID in the receiver's hand, and no card moves or is drawn.
  R15. When a seat plays or discards #id, then the card at #id's index in its hand_ids is removed from both hand_ids and hand_faces.
  R16. When a played card's rank is exactly 1 more than its colour's pile, then that pile becomes the rank, team_score rises by 1, and action_log records the success with the face.
  R17. When a 5 is played successfully and hint_tokens is below 8, then hint_tokens rises by 1; at 8 it stays 8.
  R18. When a play fails, then fuses falls by exactly 1, '#id=face' is appended to discard_pile, the piles and team_score are unchanged, and action_log records the failure with the face.
  R19. When a seat discards, then '#id=face' is appended to discard_pile, hint_tokens rises by 1 to at most 8 (8 stays 8), and action_log records the discard with the face.
  R20. When a seat plays or discards and deck_ids is not empty, then the front entries of deck_ids and deck_faces move together to the end of that seat's hand_ids and hand_faces.
  R21. When a draw makes deck_count 0 and final_turns_left is -1, then final_turns_left is set to num_players + 1.
  R22. When a turn ends, then every seat's total is set to team_score, turns_played rises by 1, final_turns_left falls by 1 if it is above 0, and active_seat passes to the next seat (after the last seat, seat 1).
  R23. When fuses reaches 0 at the end of a turn, then the game ends.
  R24. When team_score reaches 15 at the end of a turn, then the game ends.
  R25. When final_turns_left reaches 0 at the end of a turn, then the game ends, so every player, including the one who drew the last card, has had one more turn after the deck emptied.
  R26. When turns_played reaches 40, then the game ends.
  R27. When the game is played, then there is no message phase and players communicate only through PLAY, DISCARD and HINT.
  R28. When the game ends with team_score >= 10, then every seat wins; with team_score below 10, no seat wins, even if the game ended on the third fuse.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - The active seat's turn action | asked: seat {active_seat} only | options: If hint_tokens >= 1: 'PLAY #id' for each id in its hand_ids, 'DISCARD #id' for each id in its hand_ids, and 'HINT s v' for each other seat s and each v in R,G,B,1,2,3,4,5 that matches at least one card in seat s's hand_faces. If hint_tokens == 0: only the PLAY and DISCARD options. Seats that are not active are not asked and are offered nothing.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: fuses == 0 OR team_score == 15 OR final_turns_left == 0 OR turns_played == 40, checked at the end of each turn
  - the result is one of: all seats win, no seat wins
  - how the result is decided: Every seat's total equals team_score = pile_red + pile_green + pile_blue. If team_score >= 10, every seat's total is at least 10 and all seats win together. Otherwise no seat wins. Pile progress counts even when the game ended because fuses reached 0.
  - the end screen states the final scores or deciding figures, and a short model-written summary of how the game went

## Recipe: a shared deck and hidden hands (tested on the engine)

When the script has a deck and hands, both must exist as attributes, and setup must really deal. Declare the hand as a PLAYER attribute
`{"key": "hand", "visible": "ally", "type": "list", "initial": []}` (only its owner sees it; a player attribute is never `none`) and the
deck as a TABLE attribute `{"key": "deck", "visible": "none", "type": "list", "initial": [every card, one entry per copy]}`, plus a table text
attribute `pick` (visible `none`, initial `""`) to hold the card just drawn. Then ONE draw, of a random card into seat N's hand, is three operations
in an `update`'s `do` list, in this order:

  {"set":    {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
  {"append": {"player": N, "key": "hand", "value": {"calc": "pick"}}},
  {"remove": {"key": "deck", "value": {"calc": "pick"}}}

Dealing two cards to three seats is that block repeated twice for each seat (6 draws), never a fixed list written into `initial`: the deal
is random and different each match, and every player's hand must differ. A card coming back is `{"append": {"key": "deck", ...}}` and
`{"remove": {"player": N, "key": "hand", ...}}`. "Has a card of role R" is `"R" in you.hand`. Use `{"if": {"calc": ...}}` on an operation to make
it conditional. Never declare `hand` or `deck` and then leave them unchanged: the rules would then claim cards that do not exist.

## Pattern: offer each seat only what it may do (tested on the engine)

A question's options may come from state, and the state can differ for every player. So make who may do what part of the OFFER, never a check
afterwards. Declare a PLAYER list attribute (say `offer`, visible `ally`), and set it for everyone in one `update` just before the question,
from each player's own attributes and the table's:

  {"set": {"players": "all", "key": "offer",
           "value": {"calc": "['wait'] + (['buy'] if you.coins >= price else []) + (['block'] if you.seat == target else [])"}}}

then ask with `"answer": {"type": "choice", "options": {"attribute": "offer"}}` and `to` naming who is asked. `you` is each player in turn, and a
list can be built with `+` and `(... if ... else [])`. Whatever a seat may not do is not in its list: a seat that cannot pay is not offered the
paid action, only the target of an action is offered a block against it, a player already out is not asked. Do the same for a target: put the
legal seats in a list attribute.

When a player is eliminated, set the PLATFORM status as well as your own counters: declare a status for it (`{"id": "out", "acts": false}`) next to `playing` and
run `{"set_status": {"player": N, "to": "out", "text": "Seat {player} is out."}}`. Without it the platform and the console show the player as still in the game, and the
prompts list them as playing, whatever your own `alive` attribute says. Name the cards it reveals in the same announcement.

Do NOT offer a broad list and then refuse illegal answers and ask again (a `repeat` that asks, checks, and asks again, or an update that removes
an option the player just picked). It costs a model call, it lets a model choose something illegal, and the pipeline reports it as a failure:
"an option is offered and then refused". If you find yourself writing a step called "refuse...", "check the answer is legal" or "not allowed",
you are filling the wrong list: fix the offer.

## Rounds and the safety cap

If the script ends when someone wins (the last player standing, a target reached) and not after a set number of rounds, do not add a fixed
round count to the rules. The game file still has a `limits` block: set `limits.rounds` to the generous cap the script gives (the number of
rounds it says a match may run at most) and `limits.rounds_max` to at least that. The `end` rules fire the real endings from the state; add one more
ending that fires when the cap is reached and decides the winner as the script says, so a match that hits the cap still ends with a result.

## The interface the file must use

Independent tests were written against these names and you cannot see them, so use them exactly.

- each player: `total` (number, visible: public, starts 0): This seat's score; set to team_score at the end of every turn (R16)
- the table: `deck_count` (number, visible: public, starts 0): Always the number of entries in deck_ids
- the table: `pile_red` (number, visible: public, starts 0): Highest red rank played successfully
- the table: `pile_green` (number, visible: public, starts 0): Highest green rank played successfully
- the table: `pile_blue` (number, visible: public, starts 0): Highest blue rank played successfully
- the table: `hint_tokens` (number, visible: public, starts 8): Hint tokens available, 0 to 8
- the table: `fuses` (number, visible: public, starts 3): Fuses left; the game ends when this reaches 0
- the table: `discard_pile` (list, visible: public, starts []): Revealed discarded or failed cards as '#id=face', in order
- the table: `team_score` (number, visible: public, starts 0): pile_red + pile_green + pile_blue (0 to 15)
- the table: `turns_played` (number, visible: public, starts 0): Turns completed so far
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 30, num_colours = 3, copies_of_rank_1 = 3, copies_of_rank_2 = 2, copies_of_rank_3 = 2, copies_of_rank_4 = 2, copies_of_rank_5 = 1, max_rank = 5, hand_size_2_players = 5, hand_size_3_players = 4, hand_size_4_players = 4, deck_count_start_2_players = 20, deck_count_start_3_players = 18, deck_count_start_4_players = 14, pile_start = 0, hint_tokens_start = 8, hint_tokens_max = 8, hint_cost = 1, discard_hint_gain = 1, five_played_hint_gain = 1, fuses_start = 3, fuse_loss_per_failed_play = 1, score_per_successful_play = 1, max_team_score = 15, win_threshold = 10, max_turns = 40, final_turns_left_start = -1, final_turns_extra = 1, team_score_start = 0, turns_played_start = 0, first_active_seat = 1
- the game ends with exactly one of these results, named exactly: `all seats win`, `no seat wins`
- anything else the game needs to keep track of is yours to design: name it as you like.

## How the platform works

The complete file format reference and two example games are in your system prompt. Follow them exactly: every key an
action accepts is listed there, and the loader refuses any other. The outcome must be decided by arithmetic: every
ending's `when` is a calc condition with a `result`; no `winner`, no prose ending, no `llm` in an ending. Use calc for any rule that is
arithmetic. For a spec step marked `judged`, make that step's `when` `{"prose": "<the judged sentence, verbatim>"}`: a referee answers it
true or false at play time. You may add `llm` wording to a tell, sync or update (never an ask or poll, never an outcome branch), but always keep its `text`, which is used when no
model answers. Choices made at the same moment are a `poll`. The end screen announces only the result: every ending's `text` says who won and the final scores or deciding figures with
placeholders such as `{players[0].score}`, in a line or two, with no retelling of how the game went. End with a `result` and a calc condition as the `rps` example does (not the `auction`'s `winner`).

- Mistakes the loader has refused before, so avoid them:
  * A PLAYER attribute's `visible` is one of public, ally or others, never `none`. (`none` is only for table
    attributes.) For something only its owner should see, use `ally`.
  * A `poll` step has no `each` key, and no key the format reference does not list for `poll`. `each` belongs to `ask`.
  * Do not write a `deal` block unless it has the `into` it requires. Set starting values with `initial` on
    attributes, or with `set` operations in `setup`, instead.
  * Every key must be one the reference lists for that action; a misspelled or invented key is refused.
  * TALK that everyone hears is a `poll` with a free-text answer and `"broadcast": {"to": "all", "text": "Seat {seat} says: {value}"}`
    (or `"broadcast": "all"` with no `text`, which shows each message word for word). A broadcast may use ONLY `{value}` (what that
    player answered), `{seat}` (who) and table attributes: a name bound by `verify` is not set yet, so `{talk_msg}` reaches players as
    the literal braces, and the loader refuses it.
  * WHO answered what (who challenged, who blocked, who raised a hand) is `"store": "attr"` on the `poll` or `ask`, naming a PLAYER
    attribute declared under `attributes.player` (a `text` attribute for a choice). Each player's own answer is written to it and a calc reads
    them all: `count(p.said == 'Challenge' for p in players)`, `min([p.seat for p in players if p.said == 'Challenge'])`. A `verify`
    tally gives ONE winning value and loses who gave which: one "Challenge" against three "Pass" tallies to "Pass". Never write a seat
    number into a calc by guessing (`2 if active_seat == 1 else 1`); read it from a stored answer. Reset the stored attribute with a `set`
    to `""` (`players: "all"`) before each poll, so last round's answers do not count.
  * `meta.players` carries `min`, `max` and `suggested`, exactly as the task gives them: the console fills a table to the suggested size and the real-model tests play at it.
  * THE RULES TEXT SAYS BOTH OUTCOMES. For every decision point (a challenge, a block, a claim, a cost), say what happens when it is true AND when it is false,
    and whether the action still goes ahead; a player decides on this text and nothing else, and a check compares it with each numbered rule.
  * THE RULES TEXT PLAYERS READ IS THE DESIGN'S. `meta.rules` (the brief) says each mechanic in the design's own words and in its order: how a challenge is resolved,
    what a block costs, who counts when several answer. Do not paraphrase a mechanic: a reordered sentence is a different rule.
  * BOOKKEEPING IS HIDDEN. An attribute that only the game's own steps read (a scratch value, a counter, a copy of an option list, who is blocking) is declared
    hidden (`none` on the table, `ally` on a player), not `public`: every public attribute is printed into every player's prompt on every turn.
  * THE DEAL REMOVES WHAT IT DEALS. Every card put into a hand is taken out of the deck in the same step (see the deck recipe); after setup, deck plus hands holds
    exactly the cards the rules start with, and no card appears more often than the rules say.
  * OFFER ONLY WHAT A SEAT MAY DO. Build each seat's option list from its own state (see the offer pattern) and never refuse an answer afterwards
    and ask again: an option that is offered, taken and then taken back fails the pipeline's check.
  * A QUESTION WITH ONE POSSIBLE ANSWER IS NEVER WORTH ASKING ("pass" and nothing else): the engine answers it itself, but write the step so
    it is not asked at all, and never announce a seat's answer when the seat was not asked (eliminated players).
  * ASK ONLY WHAT IS NEEDED. Put a `when` on a question that applies only sometimes: a target is asked only for the actions that take one
    (`"when": {"calc": "chosen_action in ['Steal', 'Assassinate', 'Coup']"}`), a block only when something can be blocked.
  * A counter must not go below what the rules allow. Guard every payment and loss with an `if` (`"if": {"calc": "you.coins >= cost"}`,
    or check it before the action is allowed), and treat an action the player cannot afford as the cheapest legal one, as the rules say.
  * An answer to an `ask` or a `poll` exists ONLY if the step binds it with `verify: {"bind": "name"}`; a later `update`
    stores it with `"value": "$name"` (see the `rps` example, `card1`). A step that asks and binds nothing throws the
    answers away, and every score that depends on them stays at its starting value.
  * An attribute declared `"mutable": false` is set once, by an `initialize` step, and any other step that sets it crashes the game
    ("declared static and has already been dealt"). To set a hidden type or a starting value at setup, either use an `initialize`
    step or leave the attribute mutable.
  * Do not write steps that do nothing (for example an `if` of `{"calc": "False"}`), or two polls where one will do.
  * Reply with one complete JSON object: double-quoted keys and strings, no comments, no trailing commas. WRITE IT INDENTED,
    two spaces per level and one key per line, so you can see the nesting and count the brackets; do not put it on one line.
- Keep a round to at most 20 steps. Put several operations in one `update`'s `do` list, and use one `tell` for the
  reveal. A game with more steps than that is flagged as too large in the report, however well it plays, and `verify` tells you the count.

## A pattern that works (this complete game is tested: it loads, ends, and every attribute it declares is updated)

For "each player chooses in private, then the choices decide the score":
1. One `ask` per seat, addressed with `{"where": "you.seat == N"}`, with `"verify": {"bind": "aN"}`. The answer exists only because it is bound.
2. One `update` after both. It `set`s the bound answers into table attributes with `"$aN"`, and `adjust`s each player's score with a
   `calc` that may use `$aN` and `if ... else`.
3. A `check` with `when` and `against`, and the endings in `end`, comparing `players[0].score` and `players[1].score`.
Every attribute is set by a step that runs. Adapt this; do not invent another way to store answers.

```json
{
  "schema": 1,
  "meta": {
    "id": "match_or_miss",
    "name": "Match or Miss",
    "players": {
      "min": 2,
      "max": 2
    },
    "blurb": "Two players choose A or B in secret; seat 1 scores when they match, seat 2 when they differ."
  },
  "statuses": [
    {
      "id": "playing",
      "acts": true,
      "initial": true
    }
  ],
  "attributes": {
    "player": [
      {
        "key": "score",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ],
    "game": [
      {
        "key": "rounds_left",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "last_a1",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "last_a2",
        "visible": "public",
        "type": "text",
        "initial": ""
      }
    ]
  },
  "rules": "Three rounds. Each round both players secretly choose A or B. If the choices match, seat 1 scores a point; if they differ, seat 2 does. The higher score wins.",
  "setup": [
    {
      "use": "sync",
      "label": "the table",
      "mode": "self",
      "to": "all",
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "ask",
      "label": "seat 1 chooses",
      "to": {
        "where": "you.seat == 1"
      },
      "answer": {
        "type": "choice",
        "options": [
          "A",
          "B"
        ]
      },
      "verify": {
        "bind": "a1"
      },
      "text": "Choose A or B. Your opponent will not see it."
    },
    {
      "use": "ask",
      "label": "seat 2 chooses",
      "to": {
        "where": "you.seat == 2"
      },
      "answer": {
        "type": "choice",
        "options": [
          "A",
          "B"
        ]
      },
      "verify": {
        "bind": "a2"
      },
      "text": "Choose A or B. Your opponent will not see it."
    },
    {
      "use": "update",
      "label": "score the round",
      "do": [
        {
          "set": {
            "key": "last_a1",
            "value": "$a1"
          }
        },
        {
          "set": {
            "key": "last_a2",
            "value": "$a2"
          }
        },
        {
          "adjust": {
            "player": 1,
            "key": "score",
            "value": {
              "calc": "1 if $a1 == $a2 else 0"
            }
          }
        },
        {
          "adjust": {
            "player": 2,
            "key": "score",
            "value": {
              "calc": "0 if $a1 == $a2 else 1"
            }
          }
        },
        {
          "adjust": {
            "key": "rounds_left",
            "value": -1
          }
        }
      ],
      "text": "Seat 1 chose {last_a1}, seat 2 chose {last_a2}."
    },
    {
      "use": "check",
      "label": "is it over",
      "when": {
        "calc": "rounds_left <= 0"
      },
      "against": [
        "seat_1_wins",
        "seat_2_wins",
        "draw"
      ]
    }
  ],
  "end": {
    "seat_1_wins": {
      "when": {
        "calc": "players[0].score > players[1].score"
      },
      "result": "seat 1",
      "text": "Seat 1 wins."
    },
    "seat_2_wins": {
      "when": {
        "calc": "players[1].score > players[0].score"
      },
      "result": "seat 2",
      "text": "Seat 2 wins."
    },
    "draw": {
      "when": {
        "calc": "players[0].score == players[1].score"
      },
      "result": "draw",
      "text": "A draw."
    }
  }
}
```

Your file is checked by the platform's loader, a rule that the outcome is arithmetic, random play, a check that every
attribute is actually updated, and tests written independently from the rules. If it is refused you will be told why and
shown your file again; fix what is wrong and keep the rest.
