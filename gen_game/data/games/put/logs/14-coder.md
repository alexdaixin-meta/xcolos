# 14 coder

- time: 2026-10-28T06:28:17+00:00 (86.3s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 58b10f53ea048d8b, reply sha256 4ada6140250a23a6

## Sent

````
# Task: write the XColos game file for "Put: Show One, Keep Three"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 2; set `meta.players` to {"min": 2, "max": 2, "suggested": 2} (the suggested size is the one the game plays best at).

CARDS. Use a standard 52-card deck; suits do not matter. Strengths: 3 = 13, 2 = 12, A = 11, K = 10, Q = 9, J = 8, 10 = 7, 9 = 6, 8 = 5, 7 = 4, 6 = 3, 5 = 2, 4 = 1. Higher strength is better.

SETUP. There are two players, A and B. Each starts with 0 points and 0 hands won. The match lasts exactly 40 hands. In odd-numbered hands A is the Caller and B the Responder. In even-numbered hands B is the Caller and A the Responder.

EACH HAND:
1. Deal. Shuffle all 52 cards and deal 4 cards to each player. Each player's 4th card is face up and announced to both players. The other 3 are private to their holder.

2. Caller's call. The Caller says PUT or PASS.

3. Responder's answer.
- If the Caller said PUT, the Responder says SEE, FOLD or RE-PUT. On SEE, the stake is 2; go to step 5. On FOLD, the Caller scores 1 point and wins the hand; go to step 8. On RE-PUT, go to step 4.
- If the Caller said PASS, the Responder says PUT or PASS. On PASS, the stake is 1; go to step 5. On PUT, go to step 4.

4. Caller's answer. This step happens only if the Responder said RE-PUT or PUT in step 3. The Caller says SEE or FOLD.
- After a RE-PUT: SEE makes the stake 4. FOLD gives the Responder 2 points and the hand.
- After a PUT that followed the Caller's PASS: SEE makes the stake 2. FOLD gives the Responder 1 point and the hand.
- A FOLD ends the hand; go to step 8.

5. Play (simultaneous). Each player secretly writes an ordered list of 3 different cards chosen from their own 4 cards. The face-up card may be used or left out. The lists are then revealed.

6. Tricks. Compare the 1st cards of the two lists, then the 2nd cards, then the 3rd cards. In each pair the higher strength wins that trick. Equal strength ties the trick, and it belongs to no one.

7. Score. A player who won at least 2 of the 3 tricks scores the stake (1, 2 or 4) and wins the hand. Otherwise, for example one trick each with a tie, or one win and two ties, or three ties, nobody scores.

8. Announce. Announce all calls, all 8 cards (including any card that was left out or never played), the hand result, and both players' points and hands won.

END. After hand 40 the match ends.

How the winner is decided: After 40 hands, the player with more points wins. If points are equal, the player with more hands won wins. A hand is won by scoring it on tricks or by the opponent folding. If both are equal, the match is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Put: Show One, Keep Three (2 to 2 players, best with 2)

A two-player betting card duel over 40 hands. Each player holds 3 hidden cards and 1 face-up card, calls are made to raise the stake, and then each secretly orders 3 of their 4 cards to fight 3 tricks.

STATE (every item below must exist in the file):
  - each player: points (number, starts 0); everyone sees it. Match points scored so far.
  - each player: hands_won (number, starts 0); everyone sees it. Hands won, either on tricks or because the opponent folded. Used as the tie-break.
  - each player: hand (list, starts []); only its owner sees it. The player's 3 private cards this hand. Each card is coded as strength*10+suit, e.g. 134 is a 3 (strength 13) of suit 4.
  - each player: face_up (number, starts 0); everyone sees it. The player's 4th card, dealt face up and announced to both players (same coding).
  - each player: play (list, starts []); only its owner sees it. The ordered list of 3 different cards the player secretly chose from hand plus face_up. It is revealed in the announcement.
  - each player: tricks_won (number, starts 0); everyone sees it. Tricks won in the current hand (0 to 3).
  - the table: deck (list, starts 'all 52 codes s*10+u for strength s in 1..13 and suit u in 1..4'); hidden from all players. The shuffled deck that cards are dealt from. It is refilled every hand.
  - the table: hand_number (number, starts 1); everyone sees it. Current hand, from 1 to 40. When odd, seat 1 (A) is the Caller; when even, seat 2 (B) is the Caller.
  - the table: caller_call (text, starts ''); everyone sees it. The Caller's call: PUT or PASS.
  - the table: responder_answer (text, starts ''); everyone sees it. The Responder's answer: SEE, FOLD, RE-PUT, PUT or PASS.
  - the table: caller_answer (text, starts ''); everyone sees it. The Caller's second answer: SEE or FOLD, or empty if step 4 did not happen.
  - the table: stake (number, starts 0); everyone sees it. The stake played for on tricks: 1, 2 or 4.
  - the table: folded (bool, starts False); everyone sees it. True when a FOLD ended the hand before play.
  - parameters, each kept as a table attribute: hands_total = 40, deck_size = 52, cards_dealt_per_player = 4, private_cards_per_player = 3, face_up_cards_per_player = 1, cards_played = 3, tricks_per_hand = 3, tricks_to_win_hand = 2, starting_points = 0, starting_hands_won = 0, stake_pass_pass = 1, stake_put_see = 2, stake_pass_put_see = 2, stake_reput_see = 4, fold_to_put_points = 1, fold_to_reput_points = 2, fold_to_put_after_pass_points = 1, strength_3 = 13, strength_2 = 12, strength_A = 11, strength_K = 10, strength_Q = 9, strength_J = 8, strength_10 = 7, strength_9 = 6, strength_8 = 5, strength_7 = 4, strength_6 = 3, strength_5 = 2, strength_4 = 1, suits = 4, rank_points_weight = 1000

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seat 1 is player A and seat 2 is player B.
  2. Both players start with points = 0 and hands_won = 0.
  3. hand_number is set to 1.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: Refill deck with all 52 cards. Clear each player's hand and play, set tricks_won = 0 and face_up = 0. Set stake = 0, folded = false, and caller_call, responder_answer and caller_answer to empty.
  2. [update] all players. What happens: Deal: for each player, draw 3 cards at random from deck into hand, then draw 1 card at random from deck into face_up. Each drawn card is removed from deck.
  3. [tell] all players. What happens: Announce hand_number, who is Caller and who is Responder, and both players' face_up cards.
  4. [sync] all players. What happens: Each player sees their own hand and face_up, the opponent's face_up, and both players' points and hands_won.
  5. [ask] the Caller (seat 1 if hand_number is odd, seat 2 if even) answers: PUT or PASS. What happens: Set caller_call to the answer.
  6. [ask] the Responder (seat 2 if hand_number is odd, seat 1 if even) answers: If caller_call = PUT: SEE, FOLD or RE-PUT. If caller_call = PASS: PUT or PASS.. What happens: Set responder_answer to the answer.
  7. [update] all players. What happens: If caller_call = PUT and responder_answer = SEE, set stake = 2. If caller_call = PUT and responder_answer = FOLD, the Caller gets points += 1 and hands_won += 1, and folded = true. If caller_call = PASS and responder_answer = PASS, set stake = 1.
  8. [ask] the Caller, only when responder_answer is RE-PUT or PUT answers: SEE or FOLD. What happens: Set caller_answer to the answer.
  9. [update] all players. What happens: If responder_answer = RE-PUT and caller_answer = SEE, set stake = 4. If responder_answer = RE-PUT and caller_answer = FOLD, the Responder gets points += 2 and hands_won += 1, and folded = true. If responder_answer = PUT and caller_answer = SEE, set stake = 2. If responder_answer = PUT and caller_answer = FOLD, the Responder gets points += 1 and hands_won += 1, and folded = true.
  10. [poll] all players, only when folded = false answers: One of the 24 ordered lists of 3 different cards drawn from the player's 4 cards (hand plus face_up).. What happens: Set each player's play to the chosen ordered list. Neither player sees the other's choice until both are in.
  11. [update] all players, only when folded = false. What happens: For each position i = 1, 2, 3, compare floor(play[i]/10) between the two players. The higher strength gets tricks_won += 1. Equal strength gives the trick to no one.
  12. [update] all players, only when folded = false. What happens: A player with tricks_won >= 2 gets points += stake and hands_won += 1. Otherwise nobody scores.
  13. [tell] all players. What happens: Announce caller_call, responder_answer, caller_answer, all 8 cards (both hands and face_up cards, including cards left out or never played), both play lists, tricks_won, the hand result, and both players' points and hands_won.
  14. [update] all players. What happens: hand_number += 1.
  15. [check] all players. What happens: End the game if hand_number > 40. Otherwise run the round again.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. Card strengths are 3=13, 2=12, A=11, K=10, Q=9, J=8, 10=7, 9=6, 8=5, 7=4, 6=3, 5=2, 4=1, and suits do not matter.
  R2. Both players start with 0 points and 0 hands won, and the match lasts exactly 40 hands.
  R3. When hand_number is odd, seat 1 (A) is the Caller and seat 2 (B) is the Responder; when it is even, seat 2 is the Caller and seat 1 is the Responder.
  R4. Each hand, all 52 cards are shuffled and each player gets 3 private cards in hand and 1 face_up card that is announced to both players.
  R5. The Caller first says PUT or PASS.
  R6. When the Caller said PUT and the Responder says SEE, the stake is 2 and play follows.
  R7. When the Caller said PUT and the Responder says FOLD, the Caller scores 1 point and 1 hand won, and the hand ends without play.
  R8. When the Caller said PUT and the Responder says RE-PUT, the Caller must answer SEE or FOLD.
  R9. When the Caller said PASS and the Responder says PASS, the stake is 1 and play follows.
  R10. When the Caller said PASS and the Responder says PUT, the Caller must answer SEE or FOLD.
  R11. When the Caller answers SEE after a RE-PUT, the stake is 4 and play follows.
  R12. When the Caller answers FOLD after a RE-PUT, the Responder scores 2 points and 1 hand won, and the hand ends without play.
  R13. When the Caller answers SEE after PASS then PUT, the stake is 2 and play follows.
  R14. When the Caller answers FOLD after PASS then PUT, the Responder scores 1 point and 1 hand won, and the hand ends without play.
  R15. When play happens, both players simultaneously choose an ordered list of 3 different cards from their 4 cards, and the face-up card may be used or left out.
  R16. Trick i compares the i-th cards of the two lists; the higher strength wins the trick, and equal strength ties it so no one gets it.
  R17. When a player wins at least 2 of the 3 tricks, that player scores the stake (1, 2 or 4) and 1 hand won.
  R18. When no player wins at least 2 tricks (e.g. 1-1 with a tie, 1 win and 2 ties, or 3 ties), nobody scores that hand.
  R19. After every hand, all calls, all 8 cards, the result, and both players' points and hands won are announced.
  R20. After hand 40 the match ends; more points wins, then more hands won breaks a tie, and if both are equal it is a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Caller's call | asked: the Caller | options: PUT, PASS
  - Responder's answer | asked: the Responder | options: If caller_call = PUT: SEE, FOLD, RE-PUT. If caller_call = PASS: PUT, PASS.
  - Caller's answer | asked: the Caller, only when responder_answer is RE-PUT or PUT | options: SEE, FOLD
  - Play | asked: both seats, only when folded = false | options: Each of the 24 ordered lists of 3 different cards from that seat's own 3 hand cards plus its face_up card.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: hand_number > 40
  - each player's standing: you.points * 1000 + you.hands_won (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: After 40 hands the player with more points wins. If points are equal, the player with more hands won wins. If both are equal, the players share the result, which is a draw.
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

When only one option is left (the last unused action, the only legal card), still ask the question: the engine answers a choice with one
option for the seat, with no model call, and records it as the seat's move. Do not skip the question with a `when` and set the answer
yourself: that move is then missing from the match, and a test that scripts it fails.

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
rounds it says a match may run at most) and `limits.rounds_max` to at least that. The ending's `when` holds for the real ending AND when the cap
is reached, and its `rank_by` also ranks the players as the script says at the cap, so a match that hits the cap still ends with a winner.

## The interface the file must use

Independent tests were written against these names and you cannot see them, so use them exactly.

- each player: `points` (number, visible: public, starts 0): Match points scored so far.
- each player: `hands_won` (number, visible: public, starts 0): Hands won, either on tricks or because the opponent folded. Used as the tie-break.
- each player: `face_up` (number, visible: public, starts 0): The player's 4th card, dealt face up and announced to both players (same coding).
- the table: `hand_number` (number, visible: public, starts 1): Current hand, from 1 to 40. When odd, seat 1 (A) is the Caller; when even, seat 2 (B) is the Caller.
- parameters (each must be an attribute holding this value, never a number buried in a step): hands_total = 40, deck_size = 52, cards_dealt_per_player = 4, private_cards_per_player = 3, face_up_cards_per_player = 1, cards_played = 3, tricks_per_hand = 3, tricks_to_win_hand = 2, starting_points = 0, starting_hands_won = 0, stake_pass_pass = 1, stake_put_see = 2, stake_pass_put_see = 2, stake_reput_see = 4, fold_to_put_points = 1, fold_to_reput_points = 2, fold_to_put_after_pass_points = 1, strength_3 = 13, strength_2 = 12, strength_A = 11, strength_K = 10, strength_Q = 9, strength_J = 8, strength_10 = 7, strength_9 = 6, strength_8 = 5, strength_7 = 4, strength_6 = 3, strength_5 = 2, strength_4 = 1, suits = 4, rank_points_weight = 1000
- the game ends with ONE ending whose `rank_by` is `you.points * 1000 + you.hands_won`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
- anything else the game needs to keep track of is yours to design: name it as you like.

## How the platform works

The complete file format reference and two example games are in your system prompt. Follow them exactly: every key an
action accepts is listed there, and the loader refuses any other. The outcome must be decided by arithmetic: write ONE
ending, whose `when` is a calc condition and whose `rank_by` is the ranking in the interface below; no `result`, no `winner`, no prose
ending, no `llm` in an ending. Use calc for any rule that is arithmetic. For a spec step marked `judged`, make that step's `when` `{"prose": "<the judged sentence, verbatim>"}`: a referee answers it
true or false at play time. You may add `llm` wording to a tell, sync or update (never an ask or poll, never an outcome branch), but always keep its `text`, which is used when no
model answers. Choices made at the same moment are a `poll`. The end screen announces only the result: the ending's `text` says who won (`{result}`) and the final scores or deciding figures with
placeholders such as `{players[0].score}`, in a line or two, with no retelling of how the game went. End with `rank_by` as both examples do.

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
3. A `check` with `when` and `against`, and ONE ending in `end` whose `rank_by` is `you.score`: the engine ranks the players by it.
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
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "rounds_left <= 0"
      },
      "rank_by": "you.score",
      "text": "{result} wins."
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
    "id": "put_show_one_keep_three",
    "name": "Put: Show One, Keep Three",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "blurb": "A two-player betting card duel over 40 hands: three hidden cards, one face up, raise the stake, then order three cards to fight three tricks."
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
        "key": "points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hands_won",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hand",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "face_up",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "play",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "tricks_won",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "play_code",
        "visible": "ally",
        "type": "number",
        "initial": 0
      }
    ],
    "game": [
      {
        "key": "full_deck",
        "visible": "none",
        "type": "list",
        "initial": [11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 41, 42, 43, 44, 51, 52, 53, 54, 61, 62, 63, 64, 71, 72, 73, 74, 81, 82, 83, 84, 91, 92, 93, 94, 101, 102, 103, 104, 111, 112, 113, 114, 121, 122, 123, 124, 131, 132, 133, 134]
      },
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": [11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 41, 42, 43, 44, 51, 52, 53, 54, 61, 62, 63, 64, 71, 72, 73, 74, 81, 82, 83, 84, 91, 92, 93, 94, 101, 102, 103, 104, 111, 112, 113, 114, 121, 122, 123, 124, 131, 132, 133, 134]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hand_number",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "caller_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "responder_seat",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "caller_call",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "responder_answer",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "caller_answer",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "resp_options",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "stake",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "folded",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "hand_winner",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "cards_shown",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "plays_shown",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "hands_total",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 52
      },
      {
        "key": "cards_dealt_per_player",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "private_cards_per_player",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "face_up_cards_per_player",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "cards_played",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "tricks_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "tricks_to_win_hand",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "starting_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "starting_hands_won",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "stake_pass_pass",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "stake_put_see",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "stake_pass_put_see",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "stake_reput_see",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "fold_to_put_points",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "fold_to_reput_points",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "fold_to_put_after_pass_points",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "strength_3",
        "visible": "public",
        "type": "number",
        "initial": 13
      },
      {
        "key": "strength_2",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "strength_A",
        "visible": "public",
        "type": "number",
        "initial": 11
      },
      {
        "key": "strength_K",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "strength_Q",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "strength_J",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "strength_10",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "strength_9",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "strength_8",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "strength_7",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "strength_6",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "strength_5",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "strength_4",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "suits",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "rank_points_weight",
        "visible": "public",
        "type": "number",
        "initial": 1000
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the players",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "points",
            "value": {
              "calc": "starting_points"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hands_won",
            "value": {
              "calc": "starting_hands_won"
            }
          }
        },
        {
          "set": {
            "key": "hand_number",
            "value": 1
          }
        }
      ],
      "text": "Seat 1 is player A and seat 2 is player B. Both start with {starting_points} points and {starting_hands_won} hands won."
    },
    {
      "use": "sync",
      "label": "the table",
      "mode": "self",
      "to": "all",
      "fields": [
        "points",
        "hands_won"
      ],
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "deal",
      "label": "clear the table",
      "do": [
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "full_deck"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "play",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "tricks_won",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "face_up",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "play_code",
            "value": 0
          }
        },
        {
          "set": {
            "key": "stake",
            "value": 0
          }
        },
        {
          "set": {
            "key": "folded",
            "value": false
          }
        },
        {
          "set": {
            "key": "caller_call",
            "value": ""
          }
        },
        {
          "set": {
            "key": "responder_answer",
            "value": ""
          }
        },
        {
          "set": {
            "key": "caller_answer",
            "value": ""
          }
        },
        {
          "set": {
            "key": "hand_winner",
            "value": 0
          }
        },
        {
          "set": {
            "key": "cards_shown",
            "value": []
          }
        },
        {
          "set": {
            "key": "plays_shown",
            "value": []
          }
        },
        {
          "set": {
            "key": "caller_seat",
            "value": {
              "calc": "1 if int(hand_number / 2) * 2 != hand_number else 2"
            }
          }
        },
        {
          "set": {
            "key": "responder_seat",
            "value": {
              "calc": "2 if caller_seat == 1 else 1"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "deal",
      "label": "the deal",
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "set": {
            "player": 1,
            "key": "face_up",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "face_up",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "[a * 1000000 + b * 1000 + c for a in you.hand + [you.face_up] for b in you.hand + [you.face_up] for c in you.hand + [you.face_up] if a != b and a != c and b != c]"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "deal",
      "label": "the hand begins",
      "to": "all",
      "text": "Hand {hand_number} of {hands_total}. Seat {caller_seat} is the Caller and seat {responder_seat} is the Responder. Face-up cards: seat 1 {players[0].face_up}, seat 2 {players[1].face_up}."
    },
    {
      "use": "sync",
      "phase": "deal",
      "label": "your cards",
      "mode": "self",
      "to": "all",
      "fields": [
        "hand",
        "face_up",
        "points",
        "hands_won"
      ],
      "text": "Your cards and the standings:"
    },
    {
      "use": "ask",
      "phase": "calls",
      "label": "caller's call",
      "to": {
        "where": "you.seat == caller_seat"
      },
      "answer": {
        "type": "choice",
        "options": [
          "PUT",
          "PASS"
        ]
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "caller_call",
              "value": "$answer"
            }
          },
          {
            "set": {
              "key": "resp_options",
              "value": {
                "calc": "['SEE', 'FOLD', 'RE-PUT'] if $answer == 'PUT' else ['PUT', 'PASS']"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "The Caller (seat {seat}) says {value}."
      },
      "text": "You are the Caller in hand {hand_number}. Say PUT (raise) or PASS."
    },
    {
      "use": "ask",
      "phase": "calls",
      "label": "responder's answer",
      "to": {
        "where": "you.seat == responder_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "game": "resp_options"
        }
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "responder_answer",
              "value": "$answer"
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "The Responder (seat {seat}) says {value}."
      },
      "text": "You are the Responder. The Caller said {caller_call}. After PUT: SEE (stake {stake_put_see}, play follows), FOLD (Caller scores {fold_to_put_points} and wins the hand, no play) or RE-PUT (Caller must answer SEE or FOLD). After PASS: PASS (stake {stake_pass_pass}, play follows) or PUT (Caller must answer SEE or FOLD)."
    },
    {
      "use": "update",
      "phase": "calls",
      "label": "the responder's answer settles",
      "do": [
        {
          "set": {
            "key": "stake",
            "value": {
              "calc": "stake_put_see"
            },
            "if": {
              "calc": "caller_call == 'PUT' and responder_answer == 'SEE'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "caller_seat"
            },
            "key": "points",
            "value": {
              "calc": "fold_to_put_points"
            },
            "if": {
              "calc": "caller_call == 'PUT' and responder_answer == 'FOLD'"
            },
            "text": "The Responder folds. Seat {player} scores and wins the hand."
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "caller_seat"
            },
            "key": "hands_won",
            "value": 1,
            "if": {
              "calc": "caller_call == 'PUT' and responder_answer == 'FOLD'"
            }
          }
        },
        {
          "set": {
            "key": "hand_winner",
            "value": {
              "calc": "caller_seat"
            },
            "if": {
              "calc": "caller_call == 'PUT' and responder_answer == 'FOLD'"
            }
          }
        },
        {
          "set": {
            "key": "folded",
            "value": true,
            "if": {
              "calc": "caller_call == 'PUT' and responder_answer == 'FOLD'"
            }
          }
        },
        {
          "set": {
            "key": "stake",
            "value": {
              "calc": "stake_pass_pass"
            },
            "if": {
              "calc": "caller_call == 'PASS' and responder_answer == 'PASS'"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "calls",
      "label": "caller's answer",
      "when": {
        "calc": "responder_answer in ['RE-PUT', 'PUT']"
      },
      "to": {
        "where": "you.seat == caller_seat"
      },
      "answer": {
        "type": "choice",
        "options": [
          "SEE",
          "FOLD"
        ]
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "caller_answer",
              "value": "$answer"
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "The Caller (seat {seat}) answers {value}."
      },
      "text": "The Responder said {responder_answer}. Say SEE or FOLD. After a RE-PUT: SEE makes the stake {stake_reput_see} and play follows; FOLD gives the Responder {fold_to_reput_points} points and the hand, no play. After PASS then PUT: SEE makes the stake {stake_pass_put_see} and play follows; FOLD gives the Responder {fold_to_put_after_pass_points} point and the hand, no play."
    },
    {
      "use": "update",
      "phase": "calls",
      "label": "the caller's answer settles",
      "do": [
        {
          "set": {
            "key": "stake",
            "value": {
              "calc": "stake_reput_see"
            },
            "if": {
              "calc": "responder_answer == 'RE-PUT' and caller_answer == 'SEE'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "responder_seat"
            },
            "key": "points",
            "value": {
              "calc": "fold_to_reput_points"
            },
            "if": {
              "calc": "responder_answer == 'RE-PUT' and caller_answer == 'FOLD'"
            },
            "text": "The Caller folds to the RE-PUT. Seat {player} scores and wins the hand."
          }
        },
        {
          "set": {
            "key": "stake",
            "value": {
              "calc": "stake_pass_put_see"
            },
            "if": {
              "calc": "responder_answer == 'PUT' and caller_answer == 'SEE'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "responder_seat"
            },
            "key": "points",
            "value": {
              "calc": "fold_to_put_after_pass_points"
            },
            "if": {
              "calc": "responder_answer == 'PUT' and caller_answer == 'FOLD'"
            },
            "text": "The Caller folds to the PUT. Seat {player} scores and wins the hand."
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "responder_seat"
            },
            "key": "hands_won",
            "value": 1,
            "if": {
              "calc": "responder_answer in ['RE-PUT', 'PUT'] and caller_answer == 'FOLD'"
            }
          }
        },
        {
          "set": {
            "key": "hand_winner",
            "value": {
              "calc": "responder_seat"
            },
            "if": {
              "calc": "responder_answer in ['RE-PUT', 'PUT'] and caller_answer == 'FOLD'"
            }
          }
        },
        {
          "set": {
            "key": "folded",
            "value": true,
            "if": {
              "calc": "responder_answer in ['RE-PUT', 'PUT'] and caller_answer == 'FOLD'"
            }
          }
        },
        {
          "set": {
            "key": "cards_shown",
            "value": {
              "calc": "[p.hand + [p.face_up] for p in players]"
            }
          }
        }
      ]
    },
    {
      "use": "poll",
      "phase": "play",
      "label": "play",
      "when": {
        "calc": "folded == False"
      },
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "store": "play_code",
      "text": "The stake is {stake}. Choose an ordered list of 3 different cards from your 4 (your hand plus your face-up card). Each option is one 9-digit number: the first three digits are your 1st card, the next three your 2nd, the last three your 3rd (for example 134092051 means 134, then 92, then 51). A card's code is strength*10+suit. Your opponent chooses at the same moment and sees nothing until both lists are in."
    },
    {
      "use": "update",
      "phase": "play",
      "label": "the tricks",
      "when": {
   
... (cut)

Why it was refused: it plays, but part of it does nothing: game attribute `full_deck` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "put_show_one_keep_three",
    "name": "Put: Show One, Keep Three",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "blurb": "A two-player betting card duel over 40 hands: three hidden cards, one face up, raise the stake, then order three cards to fight three tricks."
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
        "key": "points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hands_won",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hand",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "face_up",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "play",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "tricks_won",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "play_code",
        "visible": "ally",
        "type": "number",
        "initial": 0
      }
    ],
    "game": [
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": [11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 41, 42, 43, 44, 51, 52, 53, 54, 61, 62, 63, 64, 71, 72, 73, 74, 81, 82, 83, 84, 91, 92, 93, 94, 101, 102, 103, 104, 111, 112, 113, 114, 121, 122, 123, 124, 131, 132, 133, 134]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hand_number",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "caller_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "responder_seat",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "caller_call",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "responder_answer",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "caller_answer",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "resp_options",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "stake",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "folded",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "hand_winner",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "cards_shown",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "plays_shown",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "hands_total",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 52
      },
      {
        "key": "cards_dealt_per_player",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "private_cards_per_player",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "face_up_cards_per_player",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "cards_played",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "tricks_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "tricks_to_win_hand",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "starting_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "starting_hands_won",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "stake_pass_pass",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "stake_put_see",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "stake_pass_put_see",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "stake_reput_see",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "fold_to_put_points",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "fold_to_reput_points",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "fold_to_put_after_pass_points",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "strength_3",
        "visible": "public",
        "type": "number",
        "initial": 13
      },
      {
        "key": "strength_2",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "strength_A",
        "visible": "public",
        "type": "number",
        "initial": 11
      },
      {
        "key": "strength_K",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "strength_Q",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "strength_J",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "strength_10",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "strength_9",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "strength_8",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "strength_7",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "strength_6",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "strength_5",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "strength_4",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "suits",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "rank_points_weight",
        "visible": "public",
        "type": "number",
        "initial": 1000
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the players",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "points",
            "value": {
              "calc": "starting_points"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hands_won",
            "value": {
              "calc": "starting_hands_won"
            }
          }
        },
        {
          "set": {
            "key": "hand_number",
            "value": 1
          }
        }
      ],
      "text": "Seat 1 is player A and seat 2 is player B. Both start with {starting_points} points and {starting_hands_won} hands won."
    },
    {
      "use": "sync",
      "label": "the table",
      "mode": "self",
      "to": "all",
      "fields": [
        "points",
        "hands_won"
      ],
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "deal",
      "label": "clear the table",
      "do": [
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "deck + players[0].hand + players[1].hand + [p.face_up for p in players if p.face_up > 0]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "play",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "tricks_won",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "face_up",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "play_code",
            "value": 0
          }
        },
        {
          "set": {
            "key": "stake",
            "value": 0
          }
        },
        {
          "set": {
            "key": "folded",
            "value": false
          }
        },
        {
          "set": {
            "key": "caller_call",
            "value": ""
          }
        },
        {
          "set": {
            "key": "responder_answer",
            "value": ""
          }
        },
        {
          "set": {
            "key": "caller_answer",
            "value": ""
          }
        },
        {
          "set": {
            "key": "hand_winner",
            "value": 0
          }
        },
        {
          "set": {
            "key": "cards_shown",
            "value": []
          }
        },
        {
          "set": {
            "key": "plays_shown",
            "value": []
          }
        },
        {
          "set": {
            "key": "caller_seat",
            "value": {
              "calc": "1 if int(hand_number / 2) * 2 != hand_number else 2"
            }
          }
        },
        {
          "set": {
            "key": "responder_seat",
            "value": {
              "calc": "2 if caller_seat == 1 else 1"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "deal",
      "label": "the deal",
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "set": {
            "player": 1,
            "key": "face_up",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "face_up",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "[a * 1000000 + b * 1000 + c for a in you.hand + [you.face_up] for b in you.hand + [you.face_up] for c in you.hand + [you.face_up] if a != b and a != c and b != c]"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "deal",
      "label": "the hand begins",
      "to": "all",
      "text": "Hand {hand_number} of {hands_total}. Seat {caller_seat} is the Caller and seat {responder_seat} is the Responder. Face-up cards: seat 1 {players[0].face_up}, seat 2 {players[1].face_up}."
    },
    {
      "use": "sync",
      "phase": "deal",
      "label": "your cards",
      "mode": "self",
      "to": "all",
      "fields": [
        "hand",
        "face_up",
        "points",
        "hands_won"
      ],
      "text": "Your cards and the standings:"
    },
    {
      "use": "ask",
      "phase": "calls",
      "label": "caller's call",
      "to": {
        "where": "you.seat == caller_seat"
      },
      "answer": {
        "type": "choice",
        "options": [
          "PUT",
          "PASS"
        ]
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "caller_call",
              "value": "$answer"
            }
          },
          {
            "set": {
              "key": "resp_options",
              "value": {
                "calc": "['SEE', 'FOLD', 'RE-PUT'] if $answer == 'PUT' else ['PUT', 'PASS']"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "The Caller (seat {seat}) says {value}."
      },
      "text": "You are the Caller in hand {hand_number}. Say PUT or PASS."
    },
    {
      "use": "ask",
      "phase": "calls",
      "label": "responder's answer",
      "to": {
        "where": "you.seat == responder_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "game": "resp_options"
        }
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "responder_answer",
              "value": "$answer"
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "The Responder (seat {seat}) says {value}."
      },
      "text": "You are the Responder. The Caller said {caller_call}. After PUT: SEE (stake {stake_put_see}, play follows), FOLD (Caller scores {fold_to_put_points} point and wins the hand, no play) or RE-PUT (Caller must answer SEE or FOLD). After PASS: PASS (stake {stake_pass_pass}, play follows) or PUT (Caller must answer SEE or FOLD)."
    },
    {
      "use": "update",
      "phase": "calls",
      "label": "the responder's answer settles",
      "do": [
        {
          "set": {
            "key": "stake",
            "value": {
              "calc": "stake_put_see"
            },
            "if": {
              "calc": "caller_call == 'PUT' and responder_answer == 'SEE'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "caller_seat"
            },
            "key": "points",
            "value": {
              "calc": "fold_to_put_points"
            },
            "if": {
              "calc": "caller_call == 'PUT' and responder_answer == 'FOLD'"
            },
            "text": "The Responder folds. Seat {player} scores and wins the hand."
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "caller_seat"
            },
            "key": "hands_won",
            "value": 1,
            "if": {
              "calc": "caller_call == 'PUT' and responder_answer == 'FOLD'"
            }
          }
        },
        {
          "set": {
            "key": "hand_winner",
            "value": {
              "calc": "caller_seat"
            },
            "if": {
              "calc": "caller_call == 'PUT' and responder_answer == 'FOLD'"
            }
          }
        },
        {
          "set": {
            "key": "folded",
            "value": true,
            "if": {
              "calc": "caller_call == 'PUT' and responder_answer == 'FOLD'"
            }
          }
        },
        {
          "set": {
            "key": "stake",
            "value": {
              "calc": "stake_pass_pass"
            },
            "if": {
              "calc": "caller_call == 'PASS' and responder_answer == 'PASS'"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "calls",
      "label": "caller's answer",
      "when": {
        "calc": "responder_answer in ['RE-PUT', 'PUT']"
      },
      "to": {
        "where": "you.seat == caller_seat"
      },
      "answer": {
        "type": "choice",
        "options": [
          "SEE",
          "FOLD"
        ]
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "caller_answer",
              "value": "$answer"
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "The Caller (seat {seat}) answers {value}."
      },
      "text": "The Responder said {responder_answer}. Say SEE or FOLD. After a RE-PUT: SEE makes the stake {stake_reput_see} and play follows; FOLD gives the Responder {fold_to_reput_points} points and the hand, no play. After PASS then PUT: SEE makes the stake {stake_pass_put_see} and play follows; FOLD gives the Responder {fold_to_put_after_pass_points} point and the hand, no play."
    },
    {
      "use": "update",
      "phase": "calls",
      "label": "the caller's answer settles",
      "do": [
        {
          "set": {
            "key": "stake",
            "value": {
              "calc": "stake_reput_see"
            },
            "if": {
              "calc": "responder_answer == 'RE-PUT' and caller_answer == 'SEE'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "responder_seat"
            },
            "key": "points",
            "value": {
              "calc": "fold_to_reput_points"
            },
            "if": {
              "calc": "responder_answer == 'RE-PUT' and caller_answer == 'FOLD'"
            },
            "text": "The Caller folds to the RE-PUT. Seat {player} scores and wins the hand."
          }
        },
        {
          "set": {
            "key": "stake",
            "value": {
              "calc": "stake_pass_put_see"
            },
            "if": {
              "calc": "responder_answer == 'PUT' and caller_answer == 'SEE'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "responder_seat"
            },
            "key": "points",
            "value": {
              "calc": "fold_to_put_after_pass_points"
            },
            "if": {
              "calc": "responder_answer == 'PUT' and caller_answer == 'FOLD'"
            },
            "text": "The Caller folds to the PUT. Seat {player} scores and wins the hand."
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "responder_seat"
            },
            "key": "hands_won",
            "value": 1,
            "if": {
              "calc": "responder_answer in ['RE-PUT', 'PUT'] and caller_answer == 'FOLD'"
            }
          }
        },
        {
          "set": {
            "key": "hand_winner",
            "value": {
              "calc": "responder_seat"
            },
            "if": {
              "calc": "responder_answer in ['RE-PUT', 'PUT'] and caller_answer == 'FOLD'"
            }
          }
        },
        {
          "set": {
            "key": "folded",
            "value": true,
            "if": {
              "calc": "responder_answer in ['RE-PUT', 'PUT'] and caller_answer == 'FOLD'"
            }
          }
        },
        {
          "set": {
            "key": "cards_shown",
            "value": {
              "calc": "[p.hand + [p.face_up] for p in players]"
            }
          }
        }
      ]
    },
    {
      "use": "poll",
      "phase": "play",
      "label": "play",
      "when": {
        "calc": "folded == False"
      },
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "store": "play_code",
      "text": "The stake is {stake}. Choose an ordered list of 3 different cards from your 4 (your hand plus your face-up card). Each option is one number: the last three digits are your 3rd card, the three before them your 2nd card, and the digits before those your 1st card (for example 134092051 means 134, then 92, then 51). A card's code is strength*10+suit. Your opponent chooses at the same moment and sees nothing until both lists are in."
    },
    {
      "use": "update",
      "phase": "play",
      "label": "the tricks",
      "when": {
        "calc": "folded == False"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "play",
            "value": {
              "calc": "[int(you.play_code / 1000000), int(you.play_code / 1000) - int(you.play_code / 1000000) * 1000, you.play_code - int(you.play_code / 1000) * 1000]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "tricks_won",
            "value": {
              "calc": "len([1 for q in players if q.seat != you.seat for i in [0, 1, 2] if int(you.play[i] / 10) > int(q.play[i] / 10)])"
            }
          }
        },
        {
          "set": {
            "key": "plays_shown",
            "value": {
              "calc": "[p.play for p in players]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "play",
      "label": "score the hand",
      "when": {
        "calc": "folded == False"
      },
      "do": [
        {
          "set": {
            "key": "hand_winner",
            "value": {
              "calc": "max([0] + [p.seat for p in players if p.tricks_won >= tricks_to_win_hand])"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.tricks_won >= tricks_to_win_hand"
            },
            "key": "points",
            "value": {
              "calc": "stake"
            },
            "text": "Seat {player} wins at least {tricks_to_win_hand} tricks and scores the stake of {stake}."
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.tricks_won >= tricks_to_win_hand"
            },
            "key": "hands_won",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "reveal",
      "label": "the hand result",
      "to": "all",
      "text": "Hand {hand_number} result. Calls: Caller {caller_call}, Responder {responder_answer}, Caller's answer {caller_answer}. All cards: seat 1 hand {players[0].hand} face up {players[0].face_up}; seat 2 hand {players[1].hand} face up {players[1].face_up}. Plays: seat 1 {players[0].play}, seat 2 {players[1].play}. Tricks won: seat 1 {players[0].tricks_won}, seat 2 {players[1].tricks_won}. Stake {stake}, ended by a fold: {folded}. Hand won by seat {hand_winner} (0 means nobody scored). Points: seat 1 {players[0].points}, seat 2 {players[1].points}. Hands won: seat 1 {players[0].hands_won}, seat 2 {players[1].hands_won}."
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "next hand",
      "do": [
        {
          "adjust": {
            "key": "hand_number",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "reveal",
      "label": "after the last hand",
      "when": {
        "calc": "hand_number > hands_total"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "hand_number > hands_total"
      },
      "rank_by": "you.points * 1000 + you.hands_won",
      "text": "Winner: {result}. Final points: seat 1 {players[0].points} ({players[0].hands_won} hands won), seat 2 {players[1].points} ({players[1].hands_won} hands won)."
    }
  },
  "limits": {
    "rounds": 40,
    "rounds_max": 40,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "Two players: seat 1 is A, seat 2 is B. Each starts with {starting_points} points and {starting_hands_won} hands won. The match lasts exactly {hands_total} hands. In odd-numbered hands A is the Caller and B the Responder; in even-numbered hands B is the Caller and A the Responder.\n\nCARDS. A standard {deck_size}-card deck; suits do not matter. Strengths: 3 = {strength_3}, 2 = {strength_2}, A = {strength_A}, K = {strength_K}, Q = {strength_Q}, J = {strength_J}, 10 = {strength_10}, 9 = {strength_9}, 8 = {strength_8}, 7 = {strength_7}, 6 = {strength_6}, 5 = {strength_5}, 4 = {strength_4}. Higher strength is better. A card is written as strength*10+suit (suit 1 to {suits}), so 134 is a 3 (strength 13).\n\nEACH HAND:\n1. Deal. All {deck_size} cards are shuffled and each player gets {cards_dealt_per_player} cards: {private_cards_per_player} private cards in hand and {face_up_cards_per_player} face-up card announced to both players.\n2. Caller's call. The Caller says PUT or PASS.\n3. Responder's answer. If the Caller said PUT, the Responder says SEE, FOLD or RE-PUT. On SEE the stake is {stake_put_see} and play follows. On FOLD the Caller scores {fold_to_put_points} point and wins the hand, with no play. On RE-PUT the Caller must answer. If the Caller said PASS, the Responder says PUT or PASS. On PASS the stake is {stake_pass_pass} and play follows. On PUT the Caller must answer.\n4. Caller's answer (only after RE-PUT or PUT). The Caller says SEE or FOLD. After a RE-PUT: SEE makes the stake {stake_reput_see} and play follows; FOLD gives the Responder {fold_to_reput_points} points and the hand, with no play. After a PUT that followed the Caller's PASS: SEE makes the stake {stake_pass_put_see} and play follows; FOLD gives the Responder {fold_to_put_after_pass_points} point and the hand, with no play.\n5. Play (simultaneous). Each player secretly chooses an ordered list of {cards_played} different cards from their own 4 cards. The face-up card may be used or left out. The lists are then revealed.\n6. Tricks. The 1st cards are compared, then the 2nd, then the 3rd. In each pair the higher strength wins that trick; equal strength ties the trick and it belongs to no one.\n7. Score. A player who won at least {tricks_to_win_hand} of the {tricks_per_hand} tricks scores the stake (1, 2 or 4) and wins the hand. Otherwise (for example one trick each with a tie, one win and two ties, or three ties) nobody scores.\n8. Announce. All calls, all 8 cards (including any card left out), the hand result, and both players' points and hands won are announced.\n\nEND. After hand {hands_total} the match ends. The player with more points wins. If points are equal, the player with more hands won wins (a hand is won by scoring it on tricks or by the opponent folding). If both are equal, the match is a draw and the result is shared."
}
```
````
