# 12 coder

- time: 2026-10-27T04:28:11+00:00 (122.9s)  model: claude-opus-5-5
- system prompt: [system/d8d0f7f5-coder.md](system/d8d0f7f5-coder.md) (sha256 d8d0f7f5fe01453f)
- sent sha256 a57d42dee8003668, reply sha256 f29486bc371c61ca

## Sent

````
# Task: write the XColos game file for "Hanabi: Three Fireworks"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 4; set `meta.players` to {"min": 2, "max": 4, "suggested": 3} (the suggested size is the one the game plays best at).

CARDS. The deck has 30 cards in three colours: Red, Green and Blue. Each colour has three 1s, two 2s, two 3s, two 4s and one 5. A card is written as colour letter plus rank, for example R1 or B5. At the start, the deck is shuffled once and each card gets a permanent ID from #1 to #30 in shuffled order. An ID never reveals a card's face.

SETUP. With 2 players each hand has 5 cards; with 3 or 4 players each hand has 4 cards. Deal from the top of the deck in seat order. Each hand is an ordered list of card IDs, oldest first. The rest form the face-down deck: 20 cards with 2 players, 18 with 3, 14 with 4. The team starts with 8 hint tokens (never more than 8) and 3 fuses. There are three piles, Red, Green and Blue, each starting at 0. The target is 10 with 2 or 3 players and 9 with 4 players. Turns played starts at 0. The final-round counter starts at -1, meaning not started.

WHAT PLAYERS SEE. At the start of every turn the engine announces to everyone:
- the three pile values;
- the hint tokens and fuses remaining;
- the number of cards left in the deck;
- the turns played so far;
- the full discard pile, with faces;
- the full hint log.
The engine then sends the active player, privately, the colour and rank of every card in every other player's hand, together with the IDs only (never the faces) of the active player's own hand. A player never sees the faces of their own cards until those cards are played or discarded. How many copies of a card remain unseen can be worked out from the discard pile and the piles; the engine does not track it. There is no talk phase and no other communication.

TURN ORDER. Players take turns in seat order, starting with seat 1. On a turn, the active player gives exactly one answer, in one of these three forms.

(a) HINT <player> <colour or rank>. This needs at least 1 hint token. The named player must be someone else, and at least one card in their hand must match. The team spends 1 token. The engine announces to everyone which IDs in that hand match, and that every other ID currently in that hand does not match. The hint is added to the public log.

(b) DISCARD <ID>. The ID must be in your own hand. Remove it, reveal its face to everyone and put it face up in the discard pile. The team gains 1 hint token, up to a maximum of 8.

(c) PLAY <ID>. The ID must be in your own hand. Remove it and reveal its face to everyone.
- If its rank is exactly 1 more than the current value of its colour's pile, the play succeeds and that pile rises to the card's rank. If the pile has just reached 5, the team gains 1 hint token, up to a maximum of 8.
- Otherwise the play fails: the card goes face up to the discard pile and the team loses 1 fuse.

INVALID ANSWERS. An answer is invalid if it:
- has an unreadable form;
- is a hint given with 0 tokens;
- is a hint to yourself;
- is a hint that matches no card;
- names an ID not in your own hand.
An invalid answer is replaced by DISCARD of the oldest ID in the active player's hand.

DRAW. After a discard or a play, if the deck is not empty, the active player takes the top card into the end of their hand. Its ID is announced to everyone. Its face is visible only to the other players, through their private views.

FINAL ROUND. When the last card of the deck is drawn, the final-round counter is set to the number of players. On each later turn it drops by 1 at the end of that turn. So every player, starting with the next seat and ending with the player who drew the last card, gets exactly one more turn. No draws happen during these turns.

SCORE. After every turn, the team score is the sum of the three pile values (0 to 15). If the fuses are at 0, the team score is 0 instead. Every player's total is set to the team score.

END OF GAME. After every turn, the game ends if any of these is true:
- fuses are 0;
- the team score is 15;
- the final-round counter has reached 0;
- 40 turns have been played.

How the winner is decided: When the game ends, every player's total equals the team score: the sum of the three pile tops, or 0 if the last fuse was lost. If that total is at least the target (10 with 2 or 3 players, 9 with 4 players), every player wins together. Otherwise no player reaches the target, the team has lost, and the engine records the result as no winner (a shared draw). No player can ever win alone.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Hanabi: Three Fireworks (2 to 4 players, best with 3)

A cooperative card game for 2 to 4 players. Each player sees everyone's cards except their own, and the team uses hints, discards and plays to build three colour piles from 1 to 5 and reach a target score before the fuses run out.

STATE (every item below must exist in the file):
  - each player: hand_ids (list, starts []); everyone sees it. IDs of the cards in this player's hand, oldest first. IDs never reveal faces.
  - each player: hand_faces (list, starts []); everyone but its owner sees it. Faces of the cards in this player's hand (e.g. R3), kept parallel to hand_ids. Every player except the owner sees them.
  - each player: legal_options (list, starts []); only its owner sees it. The moves this player may choose on the current turn. Built only for the active player and seen only by them.
  - each player: total (number, starts 0); everyone sees it. The player's total. It always equals team_score.
  - the table: num_players (number, starts 0); everyone sees it. Number of seats at the table.
  - the table: deck_ids (list, starts []); hidden from all players. IDs of the face-down deck, in order from the top.
  - the table: deck_faces (list, starts []); hidden from all players. Faces of the face-down deck, kept parallel to deck_ids.
  - the table: deck_count (number, starts 0); everyone sees it. Number of cards left in the deck.
  - the table: pile_red (number, starts 0); everyone sees it. Value of the Red pile, 0 to 5.
  - the table: pile_green (number, starts 0); everyone sees it. Value of the Green pile, 0 to 5.
  - the table: pile_blue (number, starts 0); everyone sees it. Value of the Blue pile, 0 to 5.
  - the table: hint_tokens (number, starts 8); everyone sees it. Hint tokens remaining, 0 to 8.
  - the table: fuses (number, starts 3); everyone sees it. Fuses remaining.
  - the table: discard_pile (list, starts []); everyone sees it. Face-up discarded and failed cards, written as ID and face (e.g. #12=G2).
  - the table: hint_log (list, starts []); everyone sees it. Every hint given: who gave it, to whom, the colour or rank, the matching IDs and the non-matching IDs.
  - the table: turns_played (number, starts 0); everyone sees it. Turns completed so far.
  - the table: final_round_counter (number, starts -1); everyone sees it. -1 until the last card is drawn. It is then set to num_players and drops by 1 at the end of each later turn.
  - the table: counter_set_this_turn (bool, starts False); everyone sees it. True on the turn the last card of the deck is drawn, so the counter is not decremented on that turn.
  - the table: target (number, starts 10); everyone sees it. Score the team must reach: 10 with 2 or 3 players, 9 with 4.
  - the table: team_score (number, starts 0); everyone sees it. pile_red + pile_green + pile_blue, or 0 if fuses = 0.
  - the table: active_seat (number, starts 1); everyone sees it. Seat whose turn it is.
  - the table: last_move (text, starts ''); everyone sees it. The move resolved this turn (HINT, DISCARD or PLAY with its arguments), after any invalid answer has been replaced.
  - parameters, each kept as a table attribute: deck_size = 30, colours = 3, copies_rank_1 = 3, copies_rank_2 = 2, copies_rank_3 = 2, copies_rank_4 = 2, copies_rank_5 = 1, hand_size_2_players = 5, hand_size_3_or_4_players = 4, deck_after_deal_2_players = 20, deck_after_deal_3_players = 18, deck_after_deal_4_players = 14, hint_tokens_start = 8, hint_tokens_max = 8, hint_cost = 1, discard_token_gain = 1, completed_pile_token_gain = 1, fuses_start = 3, failed_play_fuse_loss = 1, pile_start = 0, pile_max = 5, target_2_or_3_players = 10, target_4_players = 9, max_team_score = 15, max_turns = 40, turns_played_start = 0, final_round_counter_start = -1, first_seat = 1

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Set num_players to the number of seats.
  2. Set target to 10 if num_players is 2 or 3, and to 9 if num_players is 4.
  3. Build the 30 faces: for each of R, G and B, three 1s, two 2s, two 3s, two 4s and one 5.
  4. Shuffle the faces once. Give them the IDs #1 to #30 in shuffled order. Store the IDs in deck_ids and the faces in deck_faces, in the same order.
  5. Deal from the top of the deck, one card at a time in seat order starting with seat 1, until each hand has 5 cards (2 players) or 4 cards (3 or 4 players).
  6. Each dealt card is removed from the front of deck_ids and deck_faces and appended to the end of that seat's hand_ids and hand_faces, so hands are oldest first.
  7. Set deck_count to the number of cards left: 20 with 2 players, 18 with 3, 14 with 4.
  8. Set hint_tokens to 8, fuses to 3, and pile_red, pile_green and pile_blue to 0.
  9. Set turns_played to 0, final_round_counter to -1, team_score to 0, every total to 0, and active_seat to 1.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [tell] all players. What happens: Announce pile_red, pile_green, pile_blue, hint_tokens, fuses, deck_count, turns_played, the full discard_pile with faces, and the full hint_log.
  2. [update] the seat equal to active_seat. What happens: Build legal_options for the active seat. Add PLAY <ID> and DISCARD <ID> for every ID in their own hand_ids. If hint_tokens >= 1, also add HINT <seat> <X> for every other seat and every X in {R, G, B, 1, 2, 3, 4, 5} that matches at least one face in that seat's hand_faces.
  3. [sync] the seat equal to active_seat. What happens: Privately send the active seat the hand_faces and hand_ids of every other seat, their own hand_ids (never their own faces), and their legal_options.
  4. [ask] the seat equal to active_seat answers: one option from legal_options: PLAY <ID>, DISCARD <ID>, or HINT <seat> <colour or rank>. What happens: Set last_move to the answer. If the answer is unreadable or not a legal move (a hint with 0 tokens, a hint to yourself, a hint matching no card, an ID not in your own hand), set last_move to DISCARD <first ID in own hand_ids>.
  5. [update] the seat equal to active_seat. What happens: When last_move is HINT <seat s> <X>: hint_tokens -= 1. Append to hint_log the giver, s, X, the IDs in s's hand_ids whose face matches X, and every other ID currently in s's hand_ids as not matching. Announce this to everyone.
  6. [update] the seat equal to active_seat. What happens: When last_move is DISCARD <ID>: remove the ID from hand_ids and its face from hand_faces. Append ID=face to discard_pile. hint_tokens = min(8, hint_tokens + 1). Announce the face to everyone.
  7. [update] the seat equal to active_seat. What happens: When last_move is PLAY <ID>: remove the ID and its face from the hand and announce the face. If the rank equals the matching pile (pile_red, pile_green or pile_blue) + 1, set that pile to the rank, and if the rank is 5, hint_tokens = min(8, hint_tokens + 1). Otherwise append ID=face to discard_pile and fuses -= 1.
  8. [update] all players. What happens: Set counter_set_this_turn to false. If final_round_counter > 0, final_round_counter -= 1. This only happens on turns after the last-card turn, because the counter is still -1 until the draw step below sets it.
  9. [update] the seat equal to active_seat. What happens: When last_move is DISCARD or PLAY and deck_count > 0: move the first entry of deck_ids and deck_faces to the end of the active seat's hand_ids and hand_faces, deck_count -= 1, and announce the new ID to everyone. If deck_count is now 0, set final_round_counter to num_players and counter_set_this_turn to true.
  10. [update] all players. What happens: turns_played += 1. team_score = 0 if fuses = 0, otherwise pile_red + pile_green + pile_blue. Set every player's total to team_score.
  11. [check] all players. What happens: End the game if fuses = 0, or team_score = 15, or final_round_counter = 0, or turns_played = 40. Otherwise continue.
  12. [update] all players. What happens: active_seat = (active_seat mod num_players) + 1.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game is set up, the deck has 30 cards: for each of Red, Green and Blue, three 1s, two 2s, two 3s, two 4s and one 5.
  R2. When the deck is shuffled at setup, the cards get the IDs #1 to #30 in shuffled order, and an ID never reveals a face.
  R3. When there are 2 players, each hand starts with 5 cards and deck_count starts at 20.
  R4. When there are 3 players, each hand starts with 4 cards and deck_count starts at 18; when there are 4 players, each hand starts with 4 cards and deck_count starts at 14.
  R5. When the game starts, hint_tokens = 8, fuses = 3, pile_red = pile_green = pile_blue = 0, turns_played = 0 and final_round_counter = -1.
  R6. When there are 2 or 3 players, target = 10; when there are 4 players, target = 9.
  R7. When a turn starts, everyone is told the three piles, hint_tokens, fuses, deck_count, turns_played, the full discard_pile with faces, and the full hint_log.
  R8. When a seat is active, it privately sees the faces and IDs of every other hand, and only the IDs of its own hand.
  R9. When turns pass, seats act in order 1, 2, ..., num_players, then seat 1 again, starting with seat 1.
  R10. When a seat gives HINT s X with hint_tokens >= 1, s is another seat and at least one card in s's hand matches X, then hint_tokens drops by 1 and the matching and non-matching IDs of s's hand are announced and added to hint_log.
  R11. When hint_tokens = 0, a seat cannot give a hint.
  R12. When a seat names itself in a hint, or names a colour or rank that matches no card in the named hand, the hint is invalid.
  R13. When a seat discards an ID from its own hand, the card's face is revealed, it goes to discard_pile, and hint_tokens rises by 1, to at most 8.
  R14. When a seat discards with hint_tokens = 8, hint_tokens stays at 8.
  R15. When a seat plays a card whose rank is exactly 1 more than its colour's pile, that pile becomes the card's rank.
  R16. When a successful play brings a pile to 5, hint_tokens rises by 1, to at most 8.
  R17. When a seat plays a card whose rank is not exactly 1 more than its colour's pile, the card goes face up to discard_pile and fuses drops by 1.
  R18. When an answer is unreadable, a hint at 0 tokens, a hint to oneself, a hint matching no card, or names an ID not in one's own hand, it is replaced by DISCARD of the oldest ID in the active seat's hand.
  R19. When a seat discards or plays and deck_count > 0, the top deck card is added to the end of its hand, its ID is announced, and deck_count drops by 1.
  R20. When a seat gives a hint, no card is drawn.
  R21. When the last deck card is drawn, final_round_counter is set to num_players.
  R22. When final_round_counter > 0 at the end of a turn after the one that drew the last card, final_round_counter drops by 1.
  R23. When final_round_counter has been set, no further cards are drawn because deck_count = 0.
  R24. When a turn ends, team_score = pile_red + pile_green + pile_blue, or 0 if fuses = 0, and every player's total = team_score.
  R25. When fuses reach 0 at the end of a turn, the game ends.
  R26. When team_score reaches 15 at the end of a turn, the game ends.
  R27. When final_round_counter reaches 0 at the end of a turn, the game ends.
  R28. When turns_played reaches 40, the game ends.
  R29. When the game ends with team_score >= target, every player wins together.
  R30. When the game ends with team_score < target, the result is no winner.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - The active seat's move each turn | asked: the seat equal to active_seat | options: With hint_tokens >= 1: PLAY <ID> and DISCARD <ID> for each ID in own hand_ids, plus HINT <seat> <X> for every other seat and every X in {R, G, B, 1, 2, 3, 4, 5} that matches at least one card in that seat's hand. With hint_tokens = 0: only PLAY <ID> and DISCARD <ID> for each ID in own hand_ids. The active seat is never offered a hint to itself, a hint matching no card, or an ID outside its own hand.
  - Any other question | asked: seats that are not active | options: None. Seats that are not active are not asked anything; there is no talk phase.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: fuses == 0 OR team_score == 15 OR final_round_counter == 0 OR turns_played == 40
  - the result is one of: all players win, no winner
  - how the result is decided: If team_score >= target (10 with 2 or 3 players, 9 with 4), the result is 'all players win'. Otherwise it is 'no winner' (a shared draw). No player can win alone.
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

- each player: `total` (number, visible: public, starts 0): The player's total. It always equals team_score.
- the table: `deck_count` (number, visible: public, starts 0): Number of cards left in the deck.
- the table: `pile_red` (number, visible: public, starts 0): Value of the Red pile, 0 to 5.
- the table: `pile_green` (number, visible: public, starts 0): Value of the Green pile, 0 to 5.
- the table: `pile_blue` (number, visible: public, starts 0): Value of the Blue pile, 0 to 5.
- the table: `hint_tokens` (number, visible: public, starts 8): Hint tokens remaining, 0 to 8.
- the table: `fuses` (number, visible: public, starts 3): Fuses remaining.
- the table: `discard_pile` (list, visible: public, starts []): Face-up discarded and failed cards, written as ID and face (e.g. #12=G2).
- the table: `hint_log` (list, visible: public, starts []): Every hint given: who gave it, to whom, the colour or rank, the matching IDs and the non-matching IDs.
- the table: `turns_played` (number, visible: public, starts 0): Turns completed so far.
- the table: `final_round_counter` (number, visible: public, starts -1): -1 until the last card is drawn. It is then set to num_players and drops by 1 at the end of each later turn.
- the table: `team_score` (number, visible: public, starts 0): pile_red + pile_green + pile_blue, or 0 if fuses = 0.
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 30, colours = 3, copies_rank_1 = 3, copies_rank_2 = 2, copies_rank_3 = 2, copies_rank_4 = 2, copies_rank_5 = 1, hand_size_2_players = 5, hand_size_3_or_4_players = 4, deck_after_deal_2_players = 20, deck_after_deal_3_players = 18, deck_after_deal_4_players = 14, hint_tokens_start = 8, hint_tokens_max = 8, hint_cost = 1, discard_token_gain = 1, completed_pile_token_gain = 1, fuses_start = 3, failed_play_fuse_loss = 1, pile_start = 0, pile_max = 5, target_2_or_3_players = 10, target_4_players = 9, max_team_score = 15, max_turns = 40, turns_played_start = 0, final_round_counter_start = -1, first_seat = 1
- the game ends with exactly one of these results, named exactly: `all players win`, `no winner`
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


YOUR PREVIOUS GAME FILE WAS REFUSED. Here it is:
```json
{
  "schema": 1,
  "meta": {
    "id": "hanabi_three_fireworks",
    "name": "Hanabi: Three Fireworks",
    "players": {
      "min": 2,
      "max": 4,
      "suggested": 3
    },
    "blurb": "A cooperative card game: see every hand but your own, and use hints, discards and plays to build three colour piles to the target before the fuses run out."
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
        "key": "hand_ids",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "hand_faces",
        "visible": "others",
        "type": "list",
        "initial": []
      },
      {
        "key": "legal_options",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "total",
        "visible": "public",
        "type": "number"
      }
    ],
    "game": [
      {
        "key": "num_players",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "deck_ids",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "deck_faces",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "deck_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "pile_red",
        "visible": "public",
        "type": "number"
      },
      {
        "key": "pile_green",
        "visible": "public",
        "type": "number"
      },
      {
        "key": "pile_blue",
        "visible": "public",
        "type": "number"
      },
      {
        "key": "hint_tokens",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "fuses",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "discard_pile",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "hint_log",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "turns_played",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "final_round_counter",
        "visible": "public",
        "type": "number"
      },
      {
        "key": "counter_set_this_turn",
        "visible": "public",
        "type": "bool"
      },
      {
        "key": "target",
        "visible": "public",
        "type": "number"
      },
      {
        "key": "team_score",
        "visible": "public",
        "type": "number"
      },
      {
        "key": "active_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "last_move",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "last_event",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "last_draw",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "hand_size",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "id_labels",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "positions",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "digits",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "colour_letters",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "hint_values",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "hint_target",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hint_value",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "hint_yes",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "hint_no",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "move_id",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "move_face",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "move_rank",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "move_pile",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "play_ok",
        "visible": "none",
        "type": "bool"
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "colours",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "copies_rank_1",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "copies_rank_2",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "copies_rank_3",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "copies_rank_4",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "copies_rank_5",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "hand_size_2_players",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "hand_size_3_or_4_players",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "deck_after_deal_2_players",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "deck_after_deal_3_players",
        "visible": "public",
        "type": "number",
        "initial": 18
      },
      {
        "key": "deck_after_deal_4_players",
        "visible": "public",
        "type": "number",
        "initial": 14
      },
      {
        "key": "hint_tokens_start",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "hint_tokens_max",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "hint_cost",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "discard_token_gain",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "completed_pile_token_gain",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "fuses_start",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "failed_play_fuse_loss",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "pile_start",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "pile_max",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "target_2_or_3_players",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "target_4_players",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "max_team_score",
        "visible": "public",
        "type": "number",
        "initial": 15
      },
      {
        "key": "max_turns",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "turns_played_start",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "final_round_counter_start",
        "visible": "public",
        "type": "number",
        "initial": -1
      },
      {
        "key": "first_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "count the seats",
      "do": [
        {
          "set": {
            "key": "num_players",
            "value": {
              "calc": "len(players)"
            }
          }
        },
        {
          "set": {
            "key": "positions",
            "value": {
              "calc": "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]"
            }
          }
        },
        {
          "set": {
            "key": "digits",
            "value": {
              "calc": "['1', '2', '3', '4', '5', '6']"
            }
          }
        },
        {
          "set": {
            "key": "colour_letters",
            "value": {
              "calc": "['R', 'G', 'B']"
            }
          }
        },
        {
          "set": {
            "key": "hint_values",
            "value": {
              "calc": "['R', 'G', 'B', '1', '2', '3', '4', '5']"
            }
          }
        },
        {
          "set": {
            "key": "id_labels",
            "value": {
              "calc": "['#1', '#2', '#3', '#4', '#5', '#6', '#7', '#8', '#9', '#10', '#11', '#12', '#13', '#14', '#15', '#16', '#17', '#18', '#19', '#20', '#21', '#22', '#23', '#24', '#25', '#26', '#27', '#28', '#29', '#30']"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "set the target",
      "do": [
        {
          "set": {
            "key": "target",
            "value": {
              "calc": "target_4_players if num_players == 4 else target_2_or_3_players"
            }
          }
        },
        {
          "set": {
            "key": "hand_size",
            "value": {
              "calc": "hand_size_2_players if num_players == 2 else hand_size_3_or_4_players"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "build the faces",
      "do": [
        {
          "set": {
            "key": "deck_faces",
            "value": {
              "calc": "[colour_letters[ci] + digits[r] for ci in positions if ci < colours for r in positions if r < pile_max for k in positions if k < [copies_rank_1, copies_rank_2, copies_rank_3, copies_rank_4, copies_rank_5][r]]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "shuffle and number the cards",
      "do": [
        {
          "set": {
            "key": "deck_faces",
            "value": {
              "calc": "[q[1] for q in sorted([[uniform(0, 1000000), f] for f in deck_faces])]"
            }
          }
        },
        {
          "set": {
            "key": "deck_ids",
            "value": {
              "calc": "[id_labels[k] for k in positions if k < deck_size]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "deal the hands",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "hand_ids",
            "value": {
              "calc": "[deck_ids[r * num_players + you.seat - 1] for r in positions if r < hand_size]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_faces",
            "value": {
              "calc": "[deck_faces[r * num_players + you.seat - 1] for r in positions if r < hand_size]"
            }
          }
        },
        {
          "set": {
            "key": "deck_ids",
            "value": {
              "calc": "[deck_ids[k] for k in positions if k < len(deck_ids) if k >= hand_size * num_players]"
            }
          }
        },
        {
          "set": {
            "key": "deck_faces",
            "value": {
              "calc": "[deck_faces[k] for k in positions if k < len(deck_faces) if k >= hand_size * num_players]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "count the deck",
      "do": [
        {
          "set": {
            "key": "deck_count",
            "value": {
              "calc": "deck_after_deal_2_players if num_players == 2 else (deck_after_deal_3_players if num_players == 3 else deck_after_deal_4_players)"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "tokens, fuses and piles",
      "do": [
        {
          "set": {
            "key": "hint_tokens",
            "value": {
              "calc": "hint_tokens_start"
            }
          }
        },
        {
          "set": {
            "key": "fuses",
            "value": {
              "calc": "fuses_start"
            }
          }
        },
        {
          "set": {
            "key": "pile_red",
            "value": {
              "calc": "pile_start"
            }
          }
        },
        {
          "set": {
            "key": "pile_green",
            "value": {
              "calc": "pile_start"
            }
          }
        },
        {
          "set": {
            "key": "pile_blue",
            "value": {
              "calc": "pile_start"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "counters and first seat",
      "do": [
        {
          "set": {
            "key": "turns_played",
            "value": {
              "calc": "turns_played_start"
            }
          }
        },
        {
          "set": {
            "key": "final_round_counter",
            "value": {
              "calc": "final_round_counter_start"
            }
          }
        },
        {
          "set": {
            "key": "counter_set_this_turn",
            "value": false
          }
        },
        {
          "set": {
            "key": "play_ok",
            "value": false
          }
        },
        {
          "set": {
            "key": "team_score",
            "value": {
              "calc": "pile_start * colours"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "total",
            "value": {
              "calc": "team_score"
            }
          }
        },
        {
          "set": {
            "key": "active_seat",
            "value": {
              "calc": "first_seat"
            }
          }
        }
      ]
    },
    {
      "use": "sync",
      "label": "the table",
      "mode": "self",
      "to": "all",
      "text": "The cards are dealt. You see every hand but your own; of your own hand you see only the IDs."
    }
  ],
  "steps": [
    {
      "use": "tell",
      "phase": "turn",
      "label": "the table at the start of the turn",
      "to": "all",
      "text": "Seat {active_seat} is to move. Turns played: {turns_played}. Piles: Red {pile_red}, Green {pile_green}, Blue {pile_blue}. Hint tokens {hint_tokens}, fuses {fuses}, cards in the deck {deck_count}. Discard pile: {discard_pile}. Hint log: {hint_log}."
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "build the active seat's options",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "legal_options",
            "value": []
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == active_seat"
            },
            "key": "legal_options",
            "value": {
              "calc": "['PLAY ' + i for i in you.hand_ids] + ['DISCARD ' + i for i in you.hand_ids] + (['HINT ' + digits[p.seat - 1] + ' ' + x for p in players if p.seat != you.seat for x in hint_values if any(f[0] == x or f[1] == x for f in p.hand_faces)] if hint_tokens >= hint_cost else [])"
            }
          }
        },
        {
          "set": {
            "key": "last_move",
            "value": {
              "calc": "'DISCARD ' + players[active_seat - 1].hand_ids[0]"
            }
          }
        }
      ]
    },
    {
      "use": "sync",
      "phase": "turn",
      "label": "the active seat's private view",
      "to": {
        "where": "you.seat == active_seat"
      },
      "mode": "self",
      "text": "Your private view: the faces and IDs of every other hand, the IDs (not the faces) of your own hand, and your legal moves."
    },
    {
      "use": "ask",
      "phase": "turn",
      "label": "the move",
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "legal_options"
        }
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "last_move",
              "value": {
                "calc": "$answer if $answer in players[active_seat - 1].legal_options else 'DISCARD ' + players[active_seat - 1].hand_ids[0]"
              }
            }
          }
        ]
      },
      "text": "Your turn, Seat {active_seat}. Choose exactly one move from your options: PLAY <ID> or DISCARD <ID> for a card in your own hand, or HINT <seat> <colour or rank> to another player (costs 1 hint token). Piles: Red {pile_red}, Green {pile_green}, Blue {pile_blue}. Hint tokens {hint_tokens}, fuses {fuses}, deck {deck_count}."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "a hint",
      "when": {
        "calc": "last_move[0] == 'H'"
      },
      "do": [
        {
          "set": {
            "key": "hint_target",
            "value": {
              "calc": "[p.seat for p in players if digits[p.seat - 1] == last_move[5]][0]"
            }
          }
        },
        {
          "set": {
            "key": "hint_value",
            "value": {
              "calc": "last_move[7]"
            }
          }
        },
        {
          "set": {
            "key": "hint_yes",
            "value": {
              "calc": "[players[hint_target - 1].hand_ids[k] for k in positions if k < len(players[hint_target - 1].hand_ids) if players[hint_target - 1].hand_faces[k][0] == hint_value or players[hint_target - 1].hand_faces[k][1] == hint_value]"
            }
          }
        },
        {
          "set": {
            "key": "hint_no",
            "value": {
              "calc": "[players[hint_target - 1].hand_ids[k] for k in positions if k < len(players[hint_target - 1].hand_ids) if not (players[hint_target - 1].hand_faces[k][0] == hint_value or players[hint_target - 1].hand_faces[k][1] == hint_value)]"
            }
          }
        },
        {
          "adjust": {
            "key": "hint_tokens",
            "value": {
              "calc": "-hint_cost"
            },
            "if": {
              "calc": "hint_tokens >= hint_cost"
            }
          }
        },
        {
          "set": {
            "key": "last_event",
            "value": {
              "calc": "'Seat ' + digits[active_seat - 1] + ' hints Seat ' + digits[hint_target - 1] + ' about ' + hint_value + ': matching ' + (hint_yes + ['', '', '', '', ''])[0] + (', ' + (hint_yes + ['', '', '', '', ''])[1] if len(hint_yes) > 1 else '') + (', ' + (hint_yes + ['', '', '', '', ''])[2] if len(hint_yes) > 2 else '') + (', ' + (hint_yes + ['', '', '', '', ''])[3] if len(hint_yes) > 3 else '') + (', ' + (hint_yes + ['', '', '', '', ''])[4] if len(hint_yes) > 4 else '') + '; not matching ' + ((hint_no + ['', '', '', '', ''])[0] if len(hint_no) > 0 else 'none') + (', ' + (hint_no + ['', '', '', '', ''])[1] if len(hint_no) > 1 else '') + (', ' + (hint_no + ['', '', '', '', ''])[2] if len(hint_no) > 2 else '') + (', ' + (hint_no + ['', '', '', '', ''])[3] if len(hint_no) > 3 else '') + (', ' + (hint_no + ['', '', '', '', ''])[4] if len(hint_no) > 4 else '')"
            }
          }
        },
        {
          "append": {
            "key": "hint_log",
            "value": {
              "calc": "last_event"
            }
          }
        }
      ],
      "text": "{last_event}. Hint tokens left: {hint_tokens}."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "a discard",
      "when": {
        "calc": "last_move[0] == 'D'"
      },
      "do": [
        {
          "set": {
            "key": "move_id",
            "value": {
              "calc": "[i for i in players[active_seat - 1].hand_ids if 'DISCARD ' + i == last_move][0]"
            }
          }
        },
        {
          "set": {
            "key": "move_face",
            "value": {
              "calc": "[players[active_seat - 1].hand_faces[k] for k in positions if k < len(players[active_seat - 1].hand_ids) if players[active_seat - 1].hand_ids[k] == move_id][0]"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "active_seat"
            },
            "key": "hand_faces",
            "value": {
              "calc": "[players[active_seat - 1].hand_faces[k] for k in positions if k < len(players[active_seat - 1].hand_ids) if players[active_seat - 1].hand_ids[k] != move_id]"
            }
          }
        },
        {
          "remove": {
            "player": {
              "calc": "active_seat"
            },
            "key": "hand_ids",
            "value": {
              "calc": "move_id"
            }
          }
        },
        {
          "append": {
            "key": "discard_pile",
            "value": {
              "calc": "move_id + '=' + move_face"
            }
          }
        },
        {
          "set": {
            "key": "hint_tokens",
            "value": {
              "calc": "min(hint_tokens_max, hint_tokens + discard_token_gain)"
            }
          }
        },
        {
          "set": {
            "key": "last_event",
            "value": {
              "calc": "'Seat ' + digits[active_seat - 1] + ' discards ' + move_id + ', which is ' + move_face"
            }
          }
        }
      ],
      "text": "{last_event}. Hint tokens now {hint_tokens}."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "a play",
      "when": {
        "calc": "last_move[0] == 'P'"
      },
      "do": [
        {
          "set": {
            "key": "move_id",
            "value": {
              "calc": "[i for i in players[active_seat - 1].hand_ids if 'PLAY ' + i == last_move][0]"
            }
          }
        },
        {
          "set": {
            "key": "move_face",
            "value": {
              "calc": "[players[active_seat - 1].hand_faces[k] for k in positions if k < len(players[active_seat - 1].hand_ids) if players[active_seat - 1].hand_ids[k] == move_id][0]"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "active_seat"
            },
            "key": "hand_faces",
            "value": {
              "calc": "[players[active_seat - 1].hand_faces[k] for k in positions if k < len(players[active_seat - 1].hand_ids) if players[active_seat - 1].hand_ids[k] != move_id]"
            }
          }
        },
        {
          "remove": {
            "player": {
              "calc": "active_seat"
            },
            "key": "hand_ids",
            "value": {
              "calc": "move_id"
            }
          }
        },
        {
          "set": {
            "key": "move_rank",
            "value": {
              "calc": "[r + 1 for r in positions
... (cut)

Why it was refused: players are sent text with a `{name}` that was never filled in: placeholder: a player is shown the literal {target} (in a `GAME_START` message: 'END. After every turn the game ends if the fuses are 0, the team score is 15, the final-ro'); use only names the step can fill in
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "hanabi_three_fireworks",
    "name": "Hanabi: Three Fireworks",
    "players": {
      "min": 2,
      "max": 4,
      "suggested": 3
    },
    "blurb": "A cooperative card game: see every hand but your own, and use hints, discards and plays to build three colour piles to the target before the fuses run out."
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
        "key": "hand_ids",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "hand_faces",
        "visible": "others",
        "type": "list",
        "initial": []
      },
      {
        "key": "legal_options",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "total",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ],
    "game": [
      {
        "key": "num_players",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "deck_ids",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "deck_faces",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "deck_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "pile_red",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "pile_green",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "pile_blue",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hint_tokens",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "fuses",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "discard_pile",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "hint_log",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "turns_played",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "final_round_counter",
        "visible": "public",
        "type": "number",
        "initial": -1
      },
      {
        "key": "counter_set_this_turn",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "target",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "team_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "active_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "last_move",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "last_event",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "last_draw",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "hand_size",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "id_labels",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "positions",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "digits",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "colour_letters",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "hint_values",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "hint_target",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hint_value",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "hint_yes",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "hint_no",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "move_id",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "move_face",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "move_rank",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "move_pile",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "play_ok",
        "visible": "none",
        "type": "bool",
        "initial": false
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "colours",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "copies_rank_1",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "copies_rank_2",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "copies_rank_3",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "copies_rank_4",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "copies_rank_5",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "hand_size_2_players",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "hand_size_3_or_4_players",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "deck_after_deal_2_players",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "deck_after_deal_3_players",
        "visible": "public",
        "type": "number",
        "initial": 18
      },
      {
        "key": "deck_after_deal_4_players",
        "visible": "public",
        "type": "number",
        "initial": 14
      },
      {
        "key": "hint_tokens_start",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "hint_tokens_max",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "hint_cost",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "discard_token_gain",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "completed_pile_token_gain",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "fuses_start",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "failed_play_fuse_loss",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "pile_start",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "pile_max",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "target_2_or_3_players",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "target_4_players",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "max_team_score",
        "visible": "public",
        "type": "number",
        "initial": 15
      },
      {
        "key": "max_turns",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "turns_played_start",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "final_round_counter_start",
        "visible": "public",
        "type": "number",
        "initial": -1
      },
      {
        "key": "first_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "count the seats",
      "do": [
        {
          "set": {
            "key": "num_players",
            "value": {
              "calc": "len(players)"
            }
          }
        },
        {
          "set": {
            "key": "positions",
            "value": {
              "calc": "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]"
            }
          }
        },
        {
          "set": {
            "key": "digits",
            "value": {
              "calc": "['1', '2', '3', '4', '5', '6']"
            }
          }
        },
        {
          "set": {
            "key": "colour_letters",
            "value": {
              "calc": "['R', 'G', 'B']"
            }
          }
        },
        {
          "set": {
            "key": "hint_values",
            "value": {
              "calc": "['R', 'G', 'B', '1', '2', '3', '4', '5']"
            }
          }
        },
        {
          "set": {
            "key": "id_labels",
            "value": {
              "calc": "['#1', '#2', '#3', '#4', '#5', '#6', '#7', '#8', '#9', '#10', '#11', '#12', '#13', '#14', '#15', '#16', '#17', '#18', '#19', '#20', '#21', '#22', '#23', '#24', '#25', '#26', '#27', '#28', '#29', '#30']"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "set the target",
      "do": [
        {
          "set": {
            "key": "target",
            "value": {
              "calc": "target_4_players if num_players == 4 else target_2_or_3_players"
            }
          }
        },
        {
          "set": {
            "key": "hand_size",
            "value": {
              "calc": "hand_size_2_players if num_players == 2 else hand_size_3_or_4_players"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "build the faces",
      "do": [
        {
          "set": {
            "key": "deck_faces",
            "value": {
              "calc": "[colour_letters[ci] + digits[r] for ci in positions if ci < colours for r in positions if r < pile_max for k in positions if k < [copies_rank_1, copies_rank_2, copies_rank_3, copies_rank_4, copies_rank_5][r]]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "shuffle and number the cards",
      "do": [
        {
          "set": {
            "key": "deck_faces",
            "value": {
              "calc": "[q[1] for q in sorted([[uniform(0, 1000000), f] for f in deck_faces])]"
            }
          }
        },
        {
          "set": {
            "key": "deck_ids",
            "value": {
              "calc": "[id_labels[k] for k in positions if k < deck_size]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "deal the hands",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "hand_ids",
            "value": {
              "calc": "[deck_ids[r * num_players + you.seat - 1] for r in positions if r < hand_size]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_faces",
            "value": {
              "calc": "[deck_faces[r * num_players + you.seat - 1] for r in positions if r < hand_size]"
            }
          }
        },
        {
          "set": {
            "key": "deck_ids",
            "value": {
              "calc": "[deck_ids[k] for k in positions if k < len(deck_ids) if k >= hand_size * num_players]"
            }
          }
        },
        {
          "set": {
            "key": "deck_faces",
            "value": {
              "calc": "[deck_faces[k] for k in positions if k < len(deck_faces) if k >= hand_size * num_players]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "count the deck",
      "do": [
        {
          "set": {
            "key": "deck_count",
            "value": {
              "calc": "deck_after_deal_2_players if num_players == 2 else (deck_after_deal_3_players if num_players == 3 else deck_after_deal_4_players)"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "tokens, fuses and piles",
      "do": [
        {
          "set": {
            "key": "hint_tokens",
            "value": {
              "calc": "hint_tokens_start"
            }
          }
        },
        {
          "set": {
            "key": "fuses",
            "value": {
              "calc": "fuses_start"
            }
          }
        },
        {
          "set": {
            "key": "pile_red",
            "value": {
              "calc": "pile_start"
            }
          }
        },
        {
          "set": {
            "key": "pile_green",
            "value": {
              "calc": "pile_start"
            }
          }
        },
        {
          "set": {
            "key": "pile_blue",
            "value": {
              "calc": "pile_start"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "counters and first seat",
      "do": [
        {
          "set": {
            "key": "turns_played",
            "value": {
              "calc": "turns_played_start"
            }
          }
        },
        {
          "set": {
            "key": "final_round_counter",
            "value": {
              "calc": "final_round_counter_start"
            }
          }
        },
        {
          "set": {
            "key": "counter_set_this_turn",
            "value": false
          }
        },
        {
          "set": {
            "key": "play_ok",
            "value": false
          }
        },
        {
          "set": {
            "key": "team_score",
            "value": {
              "calc": "pile_start * colours"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "total",
            "value": {
              "calc": "team_score"
            }
          }
        },
        {
          "set": {
            "key": "active_seat",
            "value": {
              "calc": "first_seat"
            }
          }
        }
      ]
    },
    {
      "use": "sync",
      "label": "the table",
      "mode": "self",
      "to": "all",
      "text": "The cards are dealt. You see every hand but your own; of your own hand you see only the IDs."
    }
  ],
  "steps": [
    {
      "use": "tell",
      "phase": "turn",
      "label": "the table at the start of the turn",
      "to": "all",
      "text": "Seat {active_seat} is to move. Turns played: {turns_played}. Piles: Red {pile_red}, Green {pile_green}, Blue {pile_blue}. Hint tokens {hint_tokens}, fuses {fuses}, cards in the deck {deck_count}. Discard pile: {discard_pile}. Hint log: {hint_log}."
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "build the active seat's options",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "legal_options",
            "value": []
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == active_seat"
            },
            "key": "legal_options",
            "value": {
              "calc": "['PLAY ' + i for i in you.hand_ids] + ['DISCARD ' + i for i in you.hand_ids] + (['HINT ' + digits[p.seat - 1] + ' ' + x for p in players if p.seat != you.seat for x in hint_values if any(f[0] == x or f[1] == x for f in p.hand_faces)] if hint_tokens >= hint_cost else [])"
            }
          }
        },
        {
          "set": {
            "key": "last_move",
            "value": {
              "calc": "'DISCARD ' + players[active_seat - 1].hand_ids[0]"
            }
          }
        }
      ]
    },
    {
      "use": "sync",
      "phase": "turn",
      "label": "the active seat's private view",
      "to": {
        "where": "you.seat == active_seat"
      },
      "mode": "self",
      "text": "Your private view: the faces and IDs of every other hand, the IDs (not the faces) of your own hand, and your legal moves."
    },
    {
      "use": "ask",
      "phase": "turn",
      "label": "the move",
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "legal_options"
        }
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "last_move",
              "value": {
                "calc": "$answer if $answer in players[active_seat - 1].legal_options else 'DISCARD ' + players[active_seat - 1].hand_ids[0]"
              }
            }
          }
        ]
      },
      "text": "Your turn, Seat {active_seat}. Choose exactly one move from your options: PLAY <ID> or DISCARD <ID> for a card in your own hand, or HINT <seat> <colour or rank> to another player (costs {hint_cost} hint token). Piles: Red {pile_red}, Green {pile_green}, Blue {pile_blue}. Hint tokens {hint_tokens}, fuses {fuses}, deck {deck_count}."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "a hint",
      "when": {
        "calc": "last_move[0] == 'H'"
      },
      "do": [
        {
          "set": {
            "key": "hint_target",
            "value": {
              "calc": "[p.seat for p in players if digits[p.seat - 1] == last_move[5]][0]"
            }
          }
        },
        {
          "set": {
            "key": "hint_value",
            "value": {
              "calc": "last_move[7]"
            }
          }
        },
        {
          "set": {
            "key": "hint_yes",
            "value": {
              "calc": "[players[hint_target - 1].hand_ids[k] for k in positions if k < len(players[hint_target - 1].hand_ids) if players[hint_target - 1].hand_faces[k][0] == hint_value or players[hint_target - 1].hand_faces[k][1] == hint_value]"
            }
          }
        },
        {
          "set": {
            "key": "hint_no",
            "value": {
              "calc": "[players[hint_target - 1].hand_ids[k] for k in positions if k < len(players[hint_target - 1].hand_ids) if not (players[hint_target - 1].hand_faces[k][0] == hint_value or players[hint_target - 1].hand_faces[k][1] == hint_value)]"
            }
          }
        },
        {
          "adjust": {
            "key": "hint_tokens",
            "value": {
              "calc": "-hint_cost"
            },
            "if": {
              "calc": "hint_tokens >= hint_cost"
            }
          }
        },
        {
          "set": {
            "key": "last_event",
            "value": {
              "calc": "'Seat ' + digits[active_seat - 1] + ' hints Seat ' + digits[hint_target - 1] + ' about ' + hint_value + ': matching ' + (hint_yes + ['', '', '', '', ''])[0] + (', ' + (hint_yes + ['', '', '', '', ''])[1] if len(hint_yes) > 1 else '') + (', ' + (hint_yes + ['', '', '', '', ''])[2] if len(hint_yes) > 2 else '') + (', ' + (hint_yes + ['', '', '', '', ''])[3] if len(hint_yes) > 3 else '') + (', ' + (hint_yes + ['', '', '', '', ''])[4] if len(hint_yes) > 4 else '') + '; not matching ' + ((hint_no + ['', '', '', '', ''])[0] if len(hint_no) > 0 else 'none') + (', ' + (hint_no + ['', '', '', '', ''])[1] if len(hint_no) > 1 else '') + (', ' + (hint_no + ['', '', '', '', ''])[2] if len(hint_no) > 2 else '') + (', ' + (hint_no + ['', '', '', '', ''])[3] if len(hint_no) > 3 else '') + (', ' + (hint_no + ['', '', '', '', ''])[4] if len(hint_no) > 4 else '')"
            }
          }
        },
        {
          "append": {
            "key": "hint_log",
            "value": {
              "calc": "last_event"
            }
          }
        }
      ],
      "text": "{last_event}. Hint tokens left: {hint_tokens}."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "a discard",
      "when": {
        "calc": "last_move[0] == 'D'"
      },
      "do": [
        {
          "set": {
            "key": "move_id",
            "value": {
              "calc": "[i for i in players[active_seat - 1].hand_ids if 'DISCARD ' + i == last_move][0]"
            }
          }
        },
        {
          "set": {
            "key": "move_face",
            "value": {
              "calc": "[players[active_seat - 1].hand_faces[k] for k in positions if k < len(players[active_seat - 1].hand_ids) if players[active_seat - 1].hand_ids[k] == move_id][0]"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "active_seat"
            },
            "key": "hand_faces",
            "value": {
              "calc": "[players[active_seat - 1].hand_faces[k] for k in positions if k < len(players[active_seat - 1].hand_ids) if players[active_seat - 1].hand_ids[k] != move_id]"
            }
          }
        },
        {
          "remove": {
            "player": {
              "calc": "active_seat"
            },
            "key": "hand_ids",
            "value": {
              "calc": "move_id"
            }
          }
        },
        {
          "append": {
            "key": "discard_pile",
            "value": {
              "calc": "move_id + '=' + move_face"
            }
          }
        },
        {
          "set": {
            "key": "hint_tokens",
            "value": {
              "calc": "min(hint_tokens_max, hint_tokens + discard_token_gain)"
            }
          }
        },
        {
          "set": {
            "key": "last_event",
            "value": {
              "calc": "'Seat ' + digits[active_seat - 1] + ' discards ' + move_id + ', which is ' + move_face"
            }
          }
        }
      ],
      "text": "{last_event}. Hint tokens now {hint_tokens}."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "a play",
      "when": {
        "calc": "last_move[0] == 'P'"
      },
      "do": [
        {
          "set": {
            "key": "move_id",
            "value": {
              "calc": "[i for i in players[active_seat - 1].hand_ids if 'PLAY ' + i == last_move][0]"
            }
          }
        },
        {
          "set": {
            "key": "move_face",
            "value": {
              "calc": "[players[active_seat - 1].hand_faces[k] for k in positions if k < len(players[active_seat - 1].hand_ids) if players[active_seat - 1].hand_ids[k] == move_id][0]"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "active_seat"
            },
            "key": "hand_faces",
            "value": {
              "calc": "[players[active_seat - 1].hand_faces[k] for k in positions if k < len(players[active_seat - 1].hand_ids) if players[active_seat - 1].hand_ids[k] != move_id]"
            }
          }
        },
        {
          "remove": {
            "player": {
              "calc": "active_seat"
            },
            "key": "hand_ids",
            "value": {
              "calc": "move_id"
            }
          }
        },
        {
          "set": {
            "key": "move_rank",
            "value": {
              "calc": "[r + 1 for r in positions if r < pile_max if digits[r] == move_face[1]][0]"
            }
          }
        },
        {
          "set": {
            "key": "move_pile",
            "value": {
              "calc": "pile_red if move_face[0] == 'R' else (pile_green if move_face[0] == 'G' else pile_blue)"
            }
          }
        },
        {
          "set": {
            "key": "play_ok",
            "value": {
              "calc": "move_rank == move_pile + 1"
            }
          }
        },
        {
          "set": {
            "key": "pile_red",
            "value": {
              "calc": "move_rank"
            },
            "if": {
              "calc": "play_ok and move_face[0] == 'R'"
            }
          }
        },
        {
          "set": {
            "key": "pile_green",
            "value": {
              "calc": "move_rank"
            },
            "if": {
              "calc": "play_ok and move_face[0] == 'G'"
            }
          }
        },
        {
          "set": {
            "key": "pile_blue",
            "value": {
              "calc": "move_rank"
            },
            "if": {
              "calc": "play_ok and move_face[0] == 'B'"
            }
          }
        },
        {
          "set": {
            "key": "hint_tokens",
            "value": {
              "calc": "min(hint_tokens_max, hint_tokens + completed_pile_token_gain)"
            },
            "if": {
              "calc": "play_ok and move_rank == pile_max"
            }
          }
        },
        {
          "append": {
            "key": "discard_pile",
            "value": {
              "calc": "move_id + '=' + move_face"
            },
            "if": {
              "calc": "not play_ok"
            }
          }
        },
        {
          "adjust": {
            "key": "fuses",
            "value": {
              "calc": "-failed_play_fuse_loss"
            },
            "if": {
              "calc": "not play_ok and fuses >= failed_play_fuse_loss"
            }
          }
        },
        {
          "set": {
            "key": "last_event",
            "value": {
              "calc": "'Seat ' + digits[active_seat - 1] + ' plays ' + move_id + ', which is ' + move_face + (': it succeeds' if play_ok else ': it fails, goes to the discard pile and costs a fuse')"
            }
          }
        }
      ],
      "text": "{last_event}. Piles: Red {pile_red}, Green {pile_green}, Blue {pile_blue}. Hint tokens {hint_tokens}, fuses {fuses}."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "the final-round countdown",
      "do": [
        {
          "set": {
            "key": "counter_set_this_turn",
            "value": false
          }
        },
        {
          "adjust": {
            "key": "final_round_counter",
            "value": -1,
            "if": {
              "calc": "final_round_counter > 0"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "the draw",
      "when": {
        "calc": "last_move[0] != 'H' and deck_count > 0"
      },
      "do": [
        {
          "set": {
            "key": "last_draw",
            "value": {
              "calc": "deck_ids[0]"
            }
          }
        },
        {
          "append": {
            "player": {
              "calc": "active_seat"
            },
            "key": "hand_ids",
            "value": {
              "calc": "deck_ids[0]"
            }
          }
        },
        {
          "append": {
            "player": {
              "calc": "active_seat"
            },
            "key": "hand_faces",
            "value": {
              "calc": "deck_faces[0]"
            }
          }
        },
        {
          "set": {
            "key": "deck_ids",
            "value": {
              "calc": "[deck_ids[k] for k in positions if k >= 1 if k < len(deck_ids)]"
            }
          }
        },
        {
          "set": {
            "key": "deck_faces",
            "value": {
              "calc": "[deck_faces[k] for k in positions if k >= 1 if k < len(deck_faces)]"
            }
          }
        },
        {
          "adjust": {
            "key": "deck_count",
            "value": -1
          }
        },
        {
          "set": {
            "key": "final_round_counter",
            "value": {
              "calc": "num_players"
            },
            "if": {
              "calc": "deck_count == 0"
            }
          }
        },
        {
          "set": {
            "key": "counter_set_this_turn",
            "value": true,
            "if": {
              "calc": "deck_count == 0"
            }
          }
        }
      ],
      "text": "Seat {active_seat} draws card {last_draw}. Cards left in the deck: {deck_count}."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "the score",
      "do": [
        {
          "adjust": {
            "key": "turns_played",
            "value": 1
          }
        },
        {
          "set": {
            "key": "team_score",
            "value": {
              "calc": "0 if fuses == 0 else pile_red + pile_green + pile_blue"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "total",
            "value": {
              "calc": "team_score"
            }
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "resolve",
      "label": "is the game over",
      "against": [
        "all_win",
        "no_winner"
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "the next seat",
      "do": [
        {
          "set": {
            "key": "active_seat",
            "value": {
              "calc": "first_seat if active_seat >= num_players else active_seat + 1"
            }
          }
        }
      ]
    }
  ],
  "end": {
    "all_win": {
      "when": {
        "calc": "(fuses == 0 or team_score == max_team_score or final_round_counter == 0 or turns_played >= max_turns) and team_score >= target"
      },
      "result": "all players win",
      "text": "All players win together. Team score {team_score} (Red {pile_red}, Green {pile_green}, Blue {pile_blue}); target {target}."
    },
    "no_winner": {
      "when": {
        "calc": "(fuses == 0 or team_score == max_team_score or final_round_counter == 0 or turns_played >= max_turns) and team_score < target"
      },
      "result": "no winner",
      "text": "No winner: the team falls short. Team score {team_score} (Red {pile_red}, Green {pile_green}, Blue {pile_blue}, fuses {fuses}); target {target}."
    }
  },
  "limits": {
    "rounds": 40,
    "rounds_max": 45,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "Hanabi: Three Fireworks is cooperative. The whole team wins together or loses together; no player can win alone.\n\nCARDS. The deck has {deck_size} cards in {colours} colours: Red, Green and Blue. Each colour has {copies_rank_1} 1s, {copies_rank_2} 2s, {copies_rank_3} 3s, {copies_rank_4} 4s and {copies_rank_5} 5. A card is written as colour letter plus rank, for example R1 or B5. At the start, the deck is shuffled once and each card gets a permanent ID from #1 to #30 in shuffled order. An ID never reveals a card's face.\n\nSETUP. With 2 players each hand has {hand_size_2_players} cards; with 3 or 4 players each hand has {hand_size_3_or_4_players} cards. Cards are dealt from the top of the deck in seat order. Each hand is an ordered list of card IDs, oldest first. The rest form the face-down deck: {deck_after_deal_2_players} cards with 2 players, {deck_after_deal_3_players} with 3, {deck_after_deal_4_players} with 4. The team starts with {hint_tokens_start} hint tokens (never more than {hint_tokens_max}) and {fuses_start} fuses. There are three piles, Red, Green and Blue, each starting at {pile_start}. The target is {target_2_or_3_players} with 2 or 3 players and {target_4_players} with 4 players. Turns played starts at {turns_played_start}. The final-round counter starts at {final_round_counter_start}, meaning not started.\n\nWHAT PLAYERS SEE. At the start of every turn everyone is told the three pile values, the hint tokens and fuses remaining, the number of cards left in the deck, the turns played so far, the full discard pile with faces, and the full hint log. The active player then privately sees the colour and rank of every card in every other player's hand, and only the IDs (never the faces) of their own hand. You never see the faces of your own cards until they are played or discarded. There is no talk and no other communication.\n\nTURN ORDER. Players take turns in seat order, starting with seat {first_seat}. On your turn you give exactly one answer, chosen from the legal moves you are offered:\n(a) HINT <player> <colour or rank>. Only offered if the team has at least 1 hint token, the named player is someone else, and at least one card in their hand matches. The team spends {hint_cost} token. Everyone is told which IDs in that hand match, and that every other ID in that hand does not match. The hint is added to the public log. No card is drawn after a hint.\n(b) DISCARD <ID>, for an ID in your own hand. The card is removed, its face is revealed to everyone and it goes face up to the discard pile. The team gains {discard_token_gain} hint token, up to a maximum of {hint_tokens_max}; at {hint_tokens_max} tokens the count stays at {hint_tokens_max}.\n(c) PLAY <ID>, for an ID in your own hand. The card is removed and its face revealed to everyone. If its rank is exactly 1 more than the current value of its colour's pile, the play succeeds and that pile rises to the card's rank; if the pile has just reached {pile_max}, the team gains {completed_pile_token_gain} hint token, up to a maximum of {hint_tokens_max}. Otherwise the play fails: the card goes face up to the discard pile and the team loses {failed_play_fuse_loss} fuse.\n\nINVALID ANSWERS. An unreadable answer, a hint with 0 tokens, a hint to yourself, a hint that matches no card, or an ID not in your own hand is invalid and is replaced by DISCARD of the oldest ID in your hand. You are only offered legal moves.\n\nDRAW. After a discard or a play, if the deck is not empty, you take the top card into the end of your hand. Its ID is announced to everyone; its face is visible only to the other players.\n\nFINAL ROUND. When the last card of the deck is drawn, the final-round counter is set to the number of players. On each later turn it drops by 1 at the end of that turn, so every player, starting with the next seat and ending with the player who drew the last card, gets exactly one more turn. No draws happen during these turns.\n\nSCORE. After every turn the team score is the sum of the three pile values (0 to {max_team_score}); if the fuses are at 0, the team score is 0 instead. Every player's total is set to the team score.\n\nEND OF GAME. After every turn the game ends if the fuses are 0, the team score is {max_team_score}, the final-round counter has reached 0, or {max_turns} turns have been played. If the team score is then at least the target, every player wins together. Otherwise the team has lost and the result is no winner (a shared draw)."
}
```
````
