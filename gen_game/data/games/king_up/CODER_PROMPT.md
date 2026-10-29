# Task: write the XColos game file for "King Up: Fair Throne"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 5; set `meta.players` to {"min": 3, "max": 5, "suggested": 4} (the suggested size is the one the game plays best at).

SEAT ORDER. Seats are numbered 1 to N (N = 3, 4 or 5). 'Seat order' always means ascending seat number, wrapping from seat N back to seat 1.

SETUP.
- Use 3N characters, labelled with letters: A-I for 3 players, A-L for 4, A-O for 5.
- Each character has a public height, starting at 0. Height also records status: -1 means eliminated, 6 means king, and 0 to 5 means active.
- Shuffle all labels once. Deal 3 to seat 1, the next 3 to seat 2, and so on. Every character is favoured by exactly one player, and no two players share a character.
- Each player's 3 characters are their secret goal.
- Each player receives 2 secret No cards. Yes votes are unlimited. The number of No cards a player holds is secret.
- The round limit is 15 rounds with 3 players, 16 with 4 and 15 with 5.
- Seat 1 is the first raiser in round 1.

EACH ROUND:
1. Announce. Show everyone all heights and the round number.
2. Talk. Every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Messages bind no one.
3. Raise. Starting with this round's first raiser and going in seat order, each player in turn raises one active character's height by 1. A character may go from 4 to 5 only if no character is currently at height 5. No height may exceed 5. A player with no legal raise passes.
4. Election. If a character is at height 5, it is the candidate, and every player votes Yes or No at the same time. A player with no No cards left must vote Yes. If no character is at height 5, skip steps 4 and 5.
5. Resolve.
   - If all votes are Yes, the candidate's height becomes 6 (king) and the game ends after this round.
   - If any vote is No, each No voter loses one No card and the candidate's height becomes -1 (eliminated for the rest of the game). Only the number of No votes is announced, not who cast them.
6. Rotate. The first raiser for the next round is the next seat in seat order.
7. End check. The game ends if a king was crowned or the round limit has been played.

SCORING. Each player reveals their goal. For each of their 3 characters they score:
- 10 if its height is 6 (king);
- 0 if its height is -1 (eliminated);
- otherwise its height (0 to 5).
A player's score is the sum of these three values.

How the winner is decided: The player with the highest score wins. If two or more players tie for the highest score, the game is a draw among them.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: King Up: Fair Throne (3 to 5 players, best with 4)

Players secretly favour three characters each, take turns raising characters up a ladder, and vote on any character that reaches the top: all Yes crowns it king, any No eliminates it.

STATE (every item below must exist in the file):
  - each player: goal (list, starts []); only its owner sees it. The 3 character labels this player favours, dealt at setup. Secret until scoring.
  - each player: no_cards (number, starts 2); only its owner sees it. Number of No cards this player still holds. Secret.
  - each player: vote (text, starts ''); only its owner sees it. This round's election vote, Yes or No. Never revealed individually.
  - each player: score (number, starts 0); everyone sees it. Final score: the sum over the 3 goal characters of 10 if king, 0 if eliminated, otherwise the character's height. Computed at game end, when goals are revealed.
  - the table: h_a (number, starts 0); everyone sees it. Height of character A. -1 means eliminated, 6 means king, 0 to 5 means active.
  - the table: h_b (number, starts 0); everyone sees it. Height of character B.
  - the table: h_c (number, starts 0); everyone sees it. Height of character C.
  - the table: h_d (number, starts 0); everyone sees it. Height of character D.
  - the table: h_e (number, starts 0); everyone sees it. Height of character E.
  - the table: h_f (number, starts 0); everyone sees it. Height of character F.
  - the table: h_g (number, starts 0); everyone sees it. Height of character G.
  - the table: h_h (number, starts 0); everyone sees it. Height of character H.
  - the table: h_i (number, starts 0); everyone sees it. Height of character I.
  - the table: h_j (number, starts 0); everyone sees it. Height of character J. Set to -2 (not in play) when N = 3.
  - the table: h_k (number, starts 0); everyone sees it. Height of character K. Set to -2 (not in play) when N = 3.
  - the table: h_l (number, starts 0); everyone sees it. Height of character L. Set to -2 (not in play) when N = 3.
  - the table: h_m (number, starts 0); everyone sees it. Height of character M. Set to -2 (not in play) when N < 5.
  - the table: h_n (number, starts 0); everyone sees it. Height of character N. Set to -2 (not in play) when N < 5.
  - the table: h_o (number, starts 0); everyone sees it. Height of character O. Set to -2 (not in play) when N < 5.
  - the table: deck (list, starts []); hidden from all players. The shuffled character labels in play (3N of them), dealt out at setup.
  - the table: round (number, starts 0); everyone sees it. Current round number.
  - the table: round_limit (number, starts 16); everyone sees it. Last round: 15 if N = 3, 16 if N = 4, 15 if N = 5.
  - the table: first_raiser (number, starts 1); everyone sees it. Seat that raises first this round.
  - the table: candidate (text, starts ''); everyone sees it. Label of the character at height 5 this round, or empty if there is none.
  - the table: no_count (number, starts 0); everyone sees it. Number of No votes in this round's election. Announced.
  - the table: king_crowned (bool, starts False); everyone sees it. True once a character has become king.
  - parameters, each kept as a table attribute: characters_per_player = 3, no_cards_start = 2, round_limit_3_players = 15, round_limit_4_players = 16, round_limit_5_players = 15, start_height = 0, raise_amount = 1, max_active_height = 5, king_height = 6, eliminated_height = -1, unused_height = -2, king_score = 10, eliminated_score = 0, first_raiser_round_1 = 1

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Let N be the number of seats (3, 4 or 5). The characters in play are the first 3N letters: A-I for N=3, A-L for N=4, A-O for N=5.
  2. Set the height of every character in play to 0, and set the height of every letter not in play to -2 (not in play; never raisable and never in any goal).
  3. Put the 3N labels in play into deck. Shuffle once by drawing at random: seat 1 draws 3 labels into goal, then seat 2 draws 3, and so on until deck is empty. Each label is removed from deck as it is drawn, so no two players share a character.
  4. Set every player's no_cards to 2.
  5. Set round_limit to 15 if N = 3, 16 if N = 4, 15 if N = 5.
  6. Set first_raiser to 1, round to 0 and king_crowned to false.
  7. Sync: each player privately sees their own goal and no_cards.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round += 1; candidate = ''; no_count = 0; every player's vote = ''.
  2. [tell] all players. What happens: Announce the round number and the heights of all characters in play (h_a ... up to the last label in play).
  3. [poll] all players answers: short text message. What happens: Each message is broadcast to all as 'Seat {seat} says: {value}'. Messages bind no one.
  4. [ask] each player in turn, in seat order starting at seat first_raiser and wrapping from seat N to seat 1 answers: the label of one legal character, or 'pass' only if there is no legal raise. A character is legal if its height is 0 to 4, and if its height is 4 then no character is currently at height 5.. What happens: The chosen character's height += 1. Each later player sees the updated heights. A pass changes nothing.
  5. [update] all players. What happens: candidate = the label of the character whose height is 5, if any; otherwise candidate stays empty.
  6. [poll] all players answers: Yes or No; a player with no_cards = 0 is offered only Yes. What happens: when candidate is not empty: each player's vote is recorded secretly. Skipped when candidate is empty.
  7. [update] all players. What happens: when candidate is not empty: no_count = number of players with vote = No. If no_count = 0, the candidate's height = 6 and king_crowned = true. If no_count >= 1, each player with vote = No has no_cards -= 1, and the candidate's height = -1.
  8. [tell] all players. What happens: when candidate is not empty: announce the candidate, the number of No votes (no_count, not who cast them), and whether it was crowned king or eliminated.
  9. [update] all players. What happens: first_raiser = (first_raiser mod N) + 1.
  10. [update] all players. What happens: when king_crowned or round >= round_limit: reveal every player's goal; each player's score = the sum over their 3 goal characters of (10 if height = 6; 0 if height = -1; otherwise height).
  11. [check] all players. What happens: End the game if king_crowned is true or round >= round_limit; otherwise continue to the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game is set up with N players, then 3N characters are in play (A-I for 3, A-L for 4, A-O for 5), each at height 0.
  R2. When the game is set up, then each player's goal holds exactly 3 distinct labels, every label in play is in exactly one goal, and deck is empty.
  R3. When the game is set up, then every player has no_cards = 2.
  R4. When N is 3, 4 or 5, then round_limit is 15, 16 or 15 respectively.
  R5. When round 1 begins, then first_raiser is seat 1.
  R6. When a round begins, then the round number and all heights are announced to everyone.
  R7. When the talk step runs, then every player submits one message simultaneously, and all messages are shown to everyone only after all are in.
  R8. When the raise step runs, then each player in seat order starting at first_raiser and wrapping from N to 1 raises one character by exactly 1.
  R9. When a character is at height -1, 5 or 6, then it may not be raised.
  R10. When a character is at height 4 and another character is at height 5, then it may not be raised.
  R11. When a character is at height 4 and no character is at height 5, then it may be raised to 5.
  R12. When a player has no legal raise, then that player passes and no height changes.
  R13. When no character is at height 5 after the raise step, then no election is held and no_cards are unchanged.
  R14. When a character is at height 5 after the raise step, then it is the candidate and every player votes Yes or No simultaneously.
  R15. When a player has no_cards = 0, then that player may vote only Yes.
  R16. When all votes are Yes, then the candidate's height becomes 6 and the game ends after this round.
  R17. When at least one vote is No, then each No voter loses 1 No card and the candidate's height becomes -1 for the rest of the game.
  R18. When an election resolves, then only the number of No votes is announced, not who cast them.
  R19. When a round ends, then first_raiser becomes the next seat in seat order (seat N goes to seat 1).
  R20. When round reaches round_limit and no king has been crowned, then the game ends.
  R21. When the game ends, then each player scores 10 for each goal character at height 6, 0 for each at height -1, and its height for each at 0 to 5.
  R22. When the game ends, then the player with the highest score wins, and players tied for the highest score share a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Talk | asked: every seat | options: a short free-text message
  - Raise | asked: each seat in turn starting at first_raiser | options: every character label in play whose height is 0 to 3, plus every label at height 4 if no character is at height 5; if that set is empty, only 'pass'
  - Election vote | asked: every seat, only when a candidate is at height 5 | options: a seat with no_cards >= 1: Yes, No; a seat with no_cards = 0: Yes only

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: king_crowned == true OR round >= round_limit
  - each player's standing: you.score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's score is the sum over their 3 secret goal characters: 10 for a king, 0 for an eliminated character, otherwise its height (0 to 5). The highest score wins; players tied for the highest score share a draw.
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

- each player: `score` (number, visible: public, starts 0): Final score: the sum over the 3 goal characters of 10 if king, 0 if eliminated, otherwise the character's height. Computed at game end, when goals are revealed.
- the table: `h_a` (number, visible: public, starts 0): Height of character A. -1 means eliminated, 6 means king, 0 to 5 means active.
- the table: `h_b` (number, visible: public, starts 0): Height of character B.
- the table: `h_c` (number, visible: public, starts 0): Height of character C.
- the table: `h_d` (number, visible: public, starts 0): Height of character D.
- the table: `h_e` (number, visible: public, starts 0): Height of character E.
- the table: `h_f` (number, visible: public, starts 0): Height of character F.
- the table: `h_g` (number, visible: public, starts 0): Height of character G.
- the table: `h_h` (number, visible: public, starts 0): Height of character H.
- the table: `h_i` (number, visible: public, starts 0): Height of character I.
- the table: `h_j` (number, visible: public, starts 0): Height of character J. Set to -2 (not in play) when N = 3.
- the table: `h_k` (number, visible: public, starts 0): Height of character K. Set to -2 (not in play) when N = 3.
- the table: `h_l` (number, visible: public, starts 0): Height of character L. Set to -2 (not in play) when N = 3.
- the table: `h_m` (number, visible: public, starts 0): Height of character M. Set to -2 (not in play) when N < 5.
- the table: `h_n` (number, visible: public, starts 0): Height of character N. Set to -2 (not in play) when N < 5.
- the table: `h_o` (number, visible: public, starts 0): Height of character O. Set to -2 (not in play) when N < 5.
- the table: `round` (number, visible: public, starts 0): Current round number.
- the table: `no_count` (number, visible: public, starts 0): Number of No votes in this round's election. Announced.
- the table: `king_crowned` (bool, visible: public, starts False): True once a character has become king.
- parameters (each must be an attribute holding this value, never a number buried in a step): characters_per_player = 3, no_cards_start = 2, round_limit_3_players = 15, round_limit_4_players = 16, round_limit_5_players = 15, start_height = 0, raise_amount = 1, max_active_height = 5, king_height = 6, eliminated_height = -1, unused_height = -2, king_score = 10, eliminated_score = 0, first_raiser_round_1 = 1
- the game ends with ONE ending whose `rank_by` is `you.score`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
