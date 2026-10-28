# 20 coder

- time: 2026-10-28T02:06:07+00:00 (90.7s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 2105c9d5844bfbf9, reply sha256 315e65bd87385adf

## Sent

````
# Task: write the XColos game file for "Greek Hold 'em Mini II"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

SETUP. Three players, numbered 1, 2 and 3. Each starts with a chip total of 0. Totals may go negative and may include fractions from split pots. The deck has 18 cards: ranks 1, 2, 3, 4, 5 and 6, three copies of each, with no suits. The game lasts exactly 36 hands. In hand h, the FIRST ACTOR is player ((h - 1) mod 3) + 1. The SECOND ACTOR is the next player after the first actor (wrapping from 3 to 1), and the THIRD ACTOR is the remaining player.

EACH HAND:
1. Deal. Shuffle all 18 cards; this is the only random event of the hand. Deal 2 hole cards face down to each player and 4 board cards face down to the table. Each player sees only their own hole cards.
2. Ante. Each player pays 1 chip into the pot. The pot starts at 3.
3. Board. Board cards 1, 2 and 3 are turned face up for everyone. Board card 4 stays face down.
4. First actor's choice: CHECK, BET 2 or BET 4. A bet is paid into the pot at once, and the choice is announced to all.
5. Second actor's choice, announced to all. If nobody has bet yet, the choices are CHECK, BET 2 or BET 4. If a bet has been made, the choices are CALL (pay the same amount as the bet into the pot) or FOLD (leave the hand, losing everything already paid).
6. Third actor's choice, with the same options as the second actor, announced to all.
7. Response. This step happens only if a bet was made after at least one player checked. Each player who checked before the bet chooses, at the same moment, CALL (pay the bet amount) or FOLD. The choices are then revealed. Only one bet is ever made in a hand: there are no raises, and the bettor never acts again.
8. Final board. Board card 4 is turned face up.
9. Hand scores. Each player's score is computed from their hole cards (ranks a and b) and the 4 board cards. Score = a + b, plus 6 if a equals b, plus 4 for each match. A match is a board card whose rank equals a or b. At most 3 matches count, because a hand may use only three board cards.
10. Showdown. The players still in the hand are those who did not fold. If exactly one player is still in, that player takes the whole pot and no hole cards are revealed. If two or three are still in, their hole cards and scores are revealed, and the pot goes to the highest score among them. Players tied for the highest score split the pot equally. If everyone checked, all three go to showdown.
11. Folded players' hole cards are never revealed.
12. Totals. Each player's total changes by the chips they won minus the chips they paid this hand. All three totals are announced.
13. All cards return to the deck for the next shuffle.

The sum of all totals is always 0.

END. After hand 36 the game ends.

How the winner is decided: After 36 hands, the player with the highest chip total wins. If two or three players share the highest total, the game is a draw among them.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Greek Hold 'em Mini II (3 to 3 players, best with 3)

Three players play 36 hands of a tiny one-bet poker with an 18-card suitless deck; the highest net chip total after hand 36 wins.

STATE (every item below must exist in the file):
  - each player: total (number, starts 0); everyone sees it. Net chip total across all hands. It may be negative or fractional.
  - each player: hole (list, starts []); only its owner sees it. The player's 2 hole cards for this hand. Only the owner sees them.
  - each player: revealed_hole (list, starts []); everyone sees it. Hole cards shown at a showdown with 2 or more players. Empty otherwise.
  - each player: hand_score (number, starts 0); only its owner sees it. This hand's score: a+b, plus 6 if a pair, plus 4 per matching board card, with at most 3 matches.
  - each player: revealed_score (number, starts 0); everyone sees it. hand_score, published at a showdown for players still in. 0 otherwise.
  - each player: action (text, starts ''); everyone sees it. The player's last announced action this hand: CHECK, BET, CALL or FOLD.
  - each player: folded (bool, starts False); everyone sees it. Whether the player has folded this hand.
  - each player: paid (number, starts 0); everyone sees it. Chips paid into the pot this hand.
  - each player: won (number, starts 0); everyone sees it. Chips won from the pot this hand.
  - the table: deck (list, starts [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6]); hidden from all players. The undealt cards.
  - the table: board_up (list, starts []); everyone sees it. Face-up board cards: 3 during betting, 4 after the final board.
  - the table: board_hidden (list, starts []); hidden from all players. Board card 4 while it is still face down.
  - the table: pot (number, starts 0); everyone sees it. Chips in the pot this hand.
  - the table: hand (number, starts 0); everyone sees it. The current hand number, from 1 to 36.
  - the table: first_actor (number, starts 1); everyone sees it. Seat ((hand-1) mod 3)+1.
  - the table: second_actor (number, starts 2); everyone sees it. The seat after the first actor, wrapping from 3 to 1.
  - the table: third_actor (number, starts 3); everyone sees it. The remaining seat.
  - the table: bet_amount (number, starts 0); everyone sees it. The size of this hand's single bet (2 or 4). 0 if nobody has bet.
  - the table: in_count (number, starts 0); everyone sees it. The number of players who have not folded.
  - the table: best_score (number, starts 0); everyone sees it. The highest hand_score among players still in.
  - the table: winner_count (number, starts 0); everyone sees it. The number of players still in who hold best_score.
  - parameters, each kept as a table attribute: num_players = 3, ranks = 6, copies_per_rank = 3, deck_size = 18, hands = 36, hole_cards = 2, board_cards = 4, board_face_up_before_betting = 3, ante = 1, starting_pot = 3, bet_small = 2, bet_large = 4, pair_bonus = 6, match_bonus = 4, max_matches = 3, starting_total = 0

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seats 1, 2 and 3 each start with a total of 0.
  2. The table's deck holds 18 cards: ranks 1 to 6, three copies of each, with no suits.
  3. The hand counter starts at 0. The game lasts exactly 36 hands.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: Increment hand by 1. Set first_actor = ((hand-1) mod 3)+1, second_actor = (first_actor mod 3)+1, and third_actor = (second_actor mod 3)+1. Return all cards to deck, so it again holds the 18 cards. For every player: clear hole and revealed_hole, set hand_score and revealed_score to 0, set action to empty, set folded to false, and set paid and won to 0. Clear board_up and board_hidden. Set bet_amount to 0.
  2. [update] all players. What happens: Deal: draw 2 random cards from deck into each player's hole. Draw 3 random cards from deck into board_up and 1 into board_hidden.
  3. [update] all players. What happens: Ante: each player's paid += 1, so pot = 3.
  4. [sync] all players. What happens: Each player sees their own hole, the 3 cards of board_up, the pot, the hand number and who acts first, second and third.
  5. [ask] the first actor (seat first_actor) answers: one of CHECK, BET 2, BET 4. What happens: On CHECK: action = CHECK. On BET x: action = BET, bet_amount = x, paid += x, pot += x. The choice is announced to all.
  6. [ask] the second actor (seat second_actor) answers: if bet_amount = 0: CHECK, BET 2 or BET 4; if bet_amount > 0: CALL or FOLD. What happens: On CHECK: action = CHECK. On BET x: action = BET, bet_amount = x, paid += x, pot += x. On CALL: action = CALL, paid += bet_amount, pot += bet_amount. On FOLD: action = FOLD, folded = true. The choice is announced to all.
  7. [ask] the third actor (seat third_actor) answers: if bet_amount = 0: CHECK, BET 2 or BET 4; if bet_amount > 0: CALL or FOLD. What happens: Same effects as the second actor's step. The choice is announced to all.
  8. [poll] every player whose action = CHECK, only when bet_amount > 0 (these players checked before the bet) answers: CALL or FOLD. What happens: Answers are collected simultaneously, then revealed. On CALL: action = CALL, paid += bet_amount, pot += bet_amount. On FOLD: action = FOLD, folded = true.
  9. [update] all players. What happens: Final board: move the card in board_hidden into board_up, so board_up holds 4 cards.
  10. [update] all players. What happens: For each player with hole ranks a and b: matches = the number of cards in board_up whose rank equals a or b. hand_score = a + b + (6 if a = b else 0) + 4 * min(3, matches).
  11. [update] all players. What happens: Set in_count = the number of players with folded = false. If in_count = 1, the unfolded player gets won = pot. If in_count >= 2: for each unfolded player, revealed_hole = hole and revealed_score = hand_score; best_score = the maximum hand_score among unfolded players; winner_count = the number of unfolded players with hand_score = best_score; each such player gets won = pot / winner_count. Folded players' hole cards are never revealed.
  12. [update] all players. What happens: Totals: each player's total += won - paid. All three totals, the showdown result and the pot split are announced.
  13. [check] all players. What happens: If hand >= 36, end the game. Otherwise play the next hand.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When a hand begins, then the deck holds all 18 cards (ranks 1-6, three of each), each player receives 2 hole cards and the board receives 4 cards, all drawn at random.
  R2. When a hand begins, then each player pays an ante of 1 and the pot is 3.
  R3. When betting starts, then 3 board cards are face up and board card 4 is hidden from everyone.
  R4. When it is hand h, then the first actor is seat ((h-1) mod 3)+1, the second actor is the next seat (wrapping from 3 to 1), and the third actor is the remaining seat.
  R5. When no bet has been made and a player acts, then they may CHECK, BET 2 or BET 4, and a bet adds that amount to their paid and to the pot.
  R6. When a bet has been made and a later actor acts, then they may only CALL (pay the bet amount into the pot) or FOLD.
  R7. When a bet is made after one or more players checked, then those checkers choose CALL or FOLD simultaneously, and the choices are revealed afterwards.
  R8. When a hand has a bet, then there is exactly one bet: there are no raises and the bettor never acts again.
  R9. When a player folds, then they leave the hand, forfeit everything they paid, and their hole cards are never revealed.
  R10. When betting ends, then board card 4 is turned face up.
  R11. When hole cards are ranks a and b, then the hand score is a + b, plus 6 if a = b, plus 4 for each board card whose rank equals a or b, counting at most 3 matches.
  R12. When exactly one player has not folded, then that player takes the whole pot and no hole cards are revealed.
  R13. When two or three players have not folded, then their hole cards and scores are revealed and the highest score takes the pot.
  R14. When players at showdown tie for the highest score, then they split the pot equally, which may give fractional totals.
  R15. When all three players check, then all three go to showdown with a pot of 3.
  R16. When a hand ends, then each player's total changes by the chips won minus the chips paid, all three totals are announced, and the totals sum to 0.
  R17. When hand 36 ends, then the game ends and the highest total wins, with tied leaders sharing the win.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - First actor's choice | asked: seat first_actor | options: CHECK, BET 2, BET 4
  - Second actor's choice | asked: seat second_actor | options: if bet_amount = 0: CHECK, BET 2, BET 4; if bet_amount > 0: CALL, FOLD
  - Third actor's choice | asked: seat third_actor | options: if bet_amount = 0: CHECK, BET 2, BET 4; if bet_amount > 0: CALL, FOLD
  - Response to a bet made after a check | asked: every seat whose action is CHECK while bet_amount > 0; other seats are not asked | options: CALL, FOLD

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: hand >= 36
  - each player's standing: you.total (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their net chip total after 36 hands. The highest total wins, and players tied at the top share the win (the source calls this a draw).
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

- each player: `total` (number, visible: public, starts 0): Net chip total across all hands. It may be negative or fractional.
- each player: `revealed_hole` (list, visible: public, starts []): Hole cards shown at a showdown with 2 or more players. Empty otherwise.
- each player: `revealed_score` (number, visible: public, starts 0): hand_score, published at a showdown for players still in. 0 otherwise.
- each player: `action` (text, visible: public, starts ''): The player's last announced action this hand: CHECK, BET, CALL or FOLD.
- each player: `folded` (bool, visible: public, starts False): Whether the player has folded this hand.
- the table: `board_up` (list, visible: public, starts []): Face-up board cards: 3 during betting, 4 after the final board.
- the table: `pot` (number, visible: public, starts 0): Chips in the pot this hand.
- the table: `hand` (number, visible: public, starts 0): The current hand number, from 1 to 36.
- the table: `bet_amount` (number, visible: public, starts 0): The size of this hand's single bet (2 or 4). 0 if nobody has bet.
- parameters (each must be an attribute holding this value, never a number buried in a step): num_players = 3, ranks = 6, copies_per_rank = 3, deck_size = 18, hands = 36, hole_cards = 2, board_cards = 4, board_face_up_before_betting = 3, ante = 1, starting_pot = 3, bet_small = 2, bet_large = 4, pair_bonus = 6, match_bonus = 4, max_matches = 3, starting_total = 0
- the game ends with ONE ending whose `rank_by` is `you.total`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
    "id": "greek_holdem_mini_ii",
    "name": "Greek Hold 'em Mini II",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Three players, 36 hands of one-bet poker with an 18-card suitless deck; the highest net chip total wins."
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
        "key": "total",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hole",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "revealed_hole",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "hand_score",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "revealed_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "action",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "folded",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "paid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "won",
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
        "key": "resp",
        "visible": "ally",
        "type": "text",
        "initial": ""
      }
    ],
    "game": [
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6]
      },
      {
        "key": "full_deck",
        "visible": "none",
        "type": "list",
        "initial": [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "board_up",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "board_hidden",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "pot",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hand",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "first_actor",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "second_actor",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "third_actor",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "bet_amount",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "in_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "best_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "winner_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "num_players",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "ranks",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "copies_per_rank",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 18
      },
      {
        "key": "hands",
        "visible": "public",
        "type": "number",
        "initial": 36
      },
      {
        "key": "hole_cards",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "board_cards",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "board_face_up_before_betting",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "ante",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "starting_pot",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "bet_small",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "bet_large",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "pair_bonus",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "match_bonus",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "max_matches",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "starting_total",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the start",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "total",
            "value": {
              "calc": "starting_total"
            }
          }
        },
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
            "key": "hand",
            "value": 0
          }
        }
      ]
    },
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
      "use": "update",
      "phase": "deal",
      "label": "a new hand",
      "do": [
        {
          "adjust": {
            "key": "hand",
            "value": 1
          }
        },
        {
          "set": {
            "key": "first_actor",
            "value": {
              "calc": "hand - 1 - num_players * int((hand - 1) / num_players) + 1"
            }
          }
        },
        {
          "set": {
            "key": "second_actor",
            "value": {
              "calc": "first_actor + 1 - num_players * int(first_actor / num_players)"
            }
          }
        },
        {
          "set": {
            "key": "third_actor",
            "value": {
              "calc": "second_actor + 1 - num_players * int(second_actor / num_players)"
            }
          }
        },
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
            "key": "hole",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "revealed_hole",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_score",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "revealed_score",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "action",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "folded",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "paid",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "won",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "resp",
            "value": ""
          }
        },
        {
          "set": {
            "key": "board_up",
            "value": []
          }
        },
        {
          "set": {
            "key": "board_hidden",
            "value": []
          }
        },
        {
          "set": {
            "key": "bet_amount",
            "value": 0
          }
        },
        {
          "set": {
            "key": "pot",
            "value": 0
          }
        },
        {
          "set": {
            "key": "in_count",
            "value": 0
          }
        },
        {
          "set": {
            "key": "best_score",
            "value": 0
          }
        },
        {
          "set": {
            "key": "winner_count",
            "value": 0
          }
        }
      ],
      "text": "Hand {hand} of {hands} begins. First actor: seat {first_actor}, second: seat {second_actor}, third: seat {third_actor}."
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hole",
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hole",
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "hole",
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "hole",
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
            }
          }
        },
        {
          "append": {
            "player": 3,
            "key": "hole",
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
            }
          }
        },
        {
          "append": {
            "player": 3,
            "key": "hole",
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
            }
          }
        },
        {
          "append": {
            "key": "board_up",
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
            }
          }
        },
        {
          "append": {
            "key": "board_up",
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
            }
          }
        },
        {
          "append": {
            "key": "board_up",
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
            }
          }
        },
        {
          "append": {
            "key": "board_hidden",
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
        }
      ],
      "text": "The cards are dealt. Face-up board: {board_up}. Board card 4 stays face down."
    },
    {
      "use": "update",
      "phase": "deal",
      "label": "the ante",
      "do": [
        {
          "adjust": {
            "players": "all",
            "key": "paid",
            "value": {
              "calc": "ante"
            }
          }
        },
        {
          "set": {
            "key": "pot",
            "value": {
              "calc": "sum(p.paid for p in players)"
            }
          }
        }
      ],
      "text": "Each player antes {ante}. The pot is {pot}."
    },
    {
      "use": "sync",
      "phase": "deal",
      "label": "your cards",
      "mode": "self",
      "to": "all",
      "text": "Hand {hand}. Board: {board_up}. Pot {pot}. Seat {first_actor} acts first, seat {second_actor} second, seat {third_actor} third. Your own state, including your hole cards:"
    },
    {
      "use": "ask",
      "phase": "betting",
      "label": "first actor",
      "to": {
        "where": "you.seat == first_actor"
      },
      "answer": {
        "type": "choice",
        "options": [
          "CHECK",
          "BET 2",
          "BET 4"
        ]
      },
      "each": {
        "do": [
          {
            "set": {
              "player": "$seat",
              "key": "action",
              "value": {
                "calc": "'BET' if $answer in ['BET 2', 'BET 4'] else $answer"
              }
            }
          },
          {
            "set": {
              "key": "bet_amount",
              "value": {
                "calc": "bet_small if $answer == 'BET 2' else bet_large"
              },
              "if": {
                "calc": "$answer in ['BET 2', 'BET 4']"
              }
            }
          },
          {
            "adjust": {
              "player": "$seat",
              "key": "paid",
              "value": {
                "calc": "bet_amount"
              },
              "if": {
                "calc": "$answer in ['BET 2', 'BET 4', 'CALL']"
              }
            }
          },
          {
            "adjust": {
              "key": "pot",
              "value": {
                "calc": "bet_amount"
              },
              "if": {
                "calc": "$answer in ['BET 2', 'BET 4', 'CALL']"
              }
            }
          },
          {
            "set": {
              "players": "all",
              "key": "offer",
              "value": {
                "calc": "['CHECK', 'BET 2', 'BET 4'] if bet_amount == 0 else ['CALL', 'FOLD']"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} (first actor): {value}. Pot {pot}."
      },
      "text": "Hand {hand}. You act first. Board: {board_up}. Your hole cards are in your state. Pot {pot}. CHECK, BET 2 or BET 4. A bet is paid into the pot at once and you will not act again this hand."
    },
    {
      "use": "ask",
      "phase": "betting",
      "label": "second actor",
      "to": {
        "where": "you.seat == second_actor"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "each": {
        "do": [
          {
            "set": {
              "player": "$seat",
              "key": "action",
              "value": {
                "calc": "'BET' if $answer in ['BET 2', 'BET 4'] else $answer"
              }
            }
          },
          {
            "set": {
              "key": "bet_amount",
              "value": {
                "calc": "bet_small if $answer == 'BET 2' else bet_large"
              },
              "if": {
                "calc": "$answer in ['BET 2', 'BET 4']"
              }
            }
          },
          {
            "adjust": {
              "player": "$seat",
              "key": "paid",
              "value": {
                "calc": "bet_amount"
              },
              "if": {
                "calc": "$answer in ['BET 2', 'BET 4', 'CALL']"
              }
            }
          },
          {
            "adjust": {
              "key": "pot",
              "value": {
                "calc": "bet_amount"
              },
              "if": {
                "calc": "$answer in ['BET 2', 'BET 4', 'CALL']"
              }
            }
          },
          {
            "set": {
              "player": "$seat",
              "key": "folded",
              "value": true,
              "if": {
                "calc": "$answer == 'FOLD'"
              }
            }
          },
          {
            "set": {
              "players": "all",
              "key": "offer",
              "value": {
                "calc": "['CHECK', 'BET 2', 'BET 4'] if bet_amount == 0 else ['CALL', 'FOLD']"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} (second actor): {value}. Pot {pot}."
      },
      "text": "Hand {hand}. You act second. Board: {board_up}. Your hole cards are in your state. Pot {pot}, current bet {bet_amount}. If nobody has bet you may CHECK, BET 2 or BET 4; if a bet has been made you may CALL (pay the bet into the pot) or FOLD (leave the hand, losing what you paid)."
    },
    {
      "use": "ask",
      "phase": "betting",
      "label": "third actor",
      "to": {
        "where": "you.seat == third_actor"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "each": {
        "do": [
          {
            "set": {
              "player": "$seat",
              "key": "action",
              "value": {
                "calc": "'BET' if $answer in ['BET 2', 'BET 4'] else $answer"
              }
            }
          },
          {
            "set": {
              "key": "bet_amount",
              "value": {
                "calc": "bet_small if $answer == 'BET 2' else bet_large"
              },
              "if": {
                "calc": "$answer in ['BET 2', 'BET 4']"
              }
            }
          },
          {
            "adjust": {
              "player": "$seat",
              "key": "paid",
              "value": {
                "calc": "bet_amount"
              },
              "if": {
                "calc": "$answer in ['BET 2', 'BET 4', 'CALL']"
              }
            }
          },
          {
            "adjust": {
              "key": "pot",
              "value": {
                "calc": "bet_amount"
              },
              "if": {
                "calc": "$answer in ['BET 2', 'BET 4', 'CALL']"
              }
            }
          },
          {
            "set": {
              "player": "$seat",
              "key": "folded",
              "value": true,
              "if": {
                "calc": "$answer == 'FOLD'"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} (third actor): {value}. Pot {pot}."
      },
      "text": "Hand {hand}. You act third. Board: {board_up}. Your hole cards are in your state. Pot {pot}, current bet {bet_amount}. If nobody has bet you may CHECK, BET 2 or BET 4; if a bet has been made you may CALL (pay the bet into the pot) or FOLD (leave the hand, losing what you paid)."
    },
    {
      "use": "poll",
      "phase": "response",
      "label": "response to the bet",
      "when": {
        "calc": "bet_amount > 0"
      },
      "to": {
        "where": "you.action == 'CHECK'"
      },
      "answer": {
        "type": "choice",
        "options": [
          "CALL",
          "FOLD"
        ]
      },
      "store": "resp",
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} responds: {value}."
      },
      "text": "You checked and then a bet of {bet_amount} was made. Board: {board_up}. Your hole cards are in your state. Pot {pot}. CALL (pay {bet_amount} into the pot and stay in) or FOLD (leave the hand, losing what you paid). Other checkers choose at the same moment."
    },
    {
      "use": "update",
      "phase": "final board",
      "label": "responses and the final board",
      "do": [
        {
          "adjust": {
            "players": {
              "where": "you.resp == 'CALL'"
            },
            "key": "paid",
            "value": {
              "calc": "bet_amount"
            }
          }
        },
        {
          "adjust": {
            "key": "pot",
            "value": {
              "calc": "bet_amount * count(p.resp == 'CALL' for p in players)"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.resp == 'FOLD'"
            },
            "key": "folded",
            "value": true
          }
        },
        {
          "set": {
            "players": {
              "where": "you.resp != ''"
            },
            "key": "action",
            "value": {
              "calc": "you.resp"
            }
          }
        },
        {
          "append": {
            "key": "board_up",
            "value": {
              "calc": "board_hidden[0]"
            },
            "if": {
              "calc": "len(board_hidden) > 0"
            }
          }
        },
        {
          "remove": {
            "key": "board_hidden",
            "value": {
              "calc": "board_hidden[0]"
            },
        
... (cut)

Why it was refused: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (action, resp, action, action) in `your_cards`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "greek_holdem_mini_ii",
    "name": "Greek Hold 'em Mini II",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Three players, 36 hands of one-bet poker with an 18-card suitless deck; the highest net chip total wins."
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
        "key": "total",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hole",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "revealed_hole",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "hand_score",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "revealed_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "action",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "folded",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "paid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "won",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "offer",
        "visible": "ally",
        "type": "list",
        "initial": [
          "CHECK",
          "BET 2",
          "BET 4"
        ]
      }
    ],
    "game": [
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6]
      },
      {
        "key": "full_deck",
        "visible": "none",
        "type": "list",
        "initial": [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "board_up",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "board_hidden",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "pot",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hand",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "first_actor",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "second_actor",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "third_actor",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "bet_amount",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "in_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "best_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "winner_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "num_players",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "ranks",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "copies_per_rank",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 18
      },
      {
        "key": "hands",
        "visible": "public",
        "type": "number",
        "initial": 36
      },
      {
        "key": "hole_cards",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "board_cards",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "board_face_up_before_betting",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "ante",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "starting_pot",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "bet_small",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "bet_large",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "pair_bonus",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "match_bonus",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "max_matches",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "starting_total",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the start",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "total",
            "value": {
              "calc": "starting_total"
            }
          }
        },
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
            "key": "hand",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "sync",
      "label": "the table",
      "mode": "self",
      "to": "all",
      "fields": [
        "total"
      ],
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "deal",
      "label": "a new hand",
      "do": [
        {
          "adjust": {
            "key": "hand",
            "value": 1
          }
        },
        {
          "set": {
            "key": "first_actor",
            "value": {
              "calc": "hand - 1 - num_players * int((hand - 1) / num_players) + 1"
            }
          }
        },
        {
          "set": {
            "key": "second_actor",
            "value": {
              "calc": "first_actor + 1 - num_players * int(first_actor / num_players)"
            }
          }
        },
        {
          "set": {
            "key": "third_actor",
            "value": {
              "calc": "second_actor + 1 - num_players * int(second_actor / num_players)"
            }
          }
        },
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
            "key": "hole",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "revealed_hole",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_score",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "revealed_score",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "action",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "folded",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "paid",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "won",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": [
              "CHECK",
              "BET 2",
              "BET 4"
            ]
          }
        },
        {
          "set": {
            "key": "board_up",
            "value": []
          }
        },
        {
          "set": {
            "key": "board_hidden",
            "value": []
          }
        },
        {
          "set": {
            "key": "bet_amount",
            "value": 0
          }
        },
        {
          "set": {
            "key": "pot",
            "value": 0
          }
        },
        {
          "set": {
            "key": "in_count",
            "value": 0
          }
        },
        {
          "set": {
            "key": "best_score",
            "value": 0
          }
        },
        {
          "set": {
            "key": "winner_count",
            "value": 0
          }
        }
      ],
      "text": "Hand {hand} of {hands} begins. First actor: seat {first_actor}, second: seat {second_actor}, third: seat {third_actor}."
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hole",
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hole",
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "hole",
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "hole",
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
            }
          }
        },
        {
          "append": {
            "player": 3,
            "key": "hole",
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
            }
          }
        },
        {
          "append": {
            "player": 3,
            "key": "hole",
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
            }
          }
        },
        {
          "append": {
            "key": "board_up",
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
            }
          }
        },
        {
          "append": {
            "key": "board_up",
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
            }
          }
        },
        {
          "append": {
            "key": "board_up",
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
            }
          }
        },
        {
          "append": {
            "key": "board_hidden",
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
        }
      ],
      "text": "The cards are dealt. Face-up board: {board_up}. Board card 4 stays face down."
    },
    {
      "use": "update",
      "phase": "deal",
      "label": "the ante",
      "do": [
        {
          "adjust": {
            "players": "all",
            "key": "paid",
            "value": {
              "calc": "ante"
            }
          }
        },
        {
          "set": {
            "key": "pot",
            "value": {
              "calc": "sum(p.paid for p in players)"
            }
          }
        }
      ],
      "text": "Each player antes {ante}. The pot is {pot}."
    },
    {
      "use": "sync",
      "phase": "deal",
      "label": "your cards",
      "mode": "self",
      "to": "all",
      "fields": [
        "hole",
        "total"
      ],
      "text": "Hand {hand}. Board: {board_up}. Pot {pot}. Seat {first_actor} acts first, seat {second_actor} second, seat {third_actor} third. Your hole cards:"
    },
    {
      "use": "ask",
      "phase": "betting",
      "label": "first actor",
      "to": {
        "where": "you.seat == first_actor"
      },
      "answer": {
        "type": "choice",
        "options": [
          "CHECK",
          "BET 2",
          "BET 4"
        ]
      },
      "each": {
        "do": [
          {
            "set": {
              "player": "$seat",
              "key": "action",
              "value": {
                "calc": "'BET' if $answer in ['BET 2', 'BET 4'] else $answer"
              }
            }
          },
          {
            "set": {
              "key": "bet_amount",
              "value": {
                "calc": "bet_small if $answer == 'BET 2' else bet_large"
              },
              "if": {
                "calc": "$answer in ['BET 2', 'BET 4']"
              }
            }
          },
          {
            "adjust": {
              "player": "$seat",
              "key": "paid",
              "value": {
                "calc": "bet_amount"
              },
              "if": {
                "calc": "$answer in ['BET 2', 'BET 4']"
              }
            }
          },
          {
            "adjust": {
              "key": "pot",
              "value": {
                "calc": "bet_amount"
              },
              "if": {
                "calc": "$answer in ['BET 2', 'BET 4']"
              }
            }
          },
          {
            "set": {
              "players": "all",
              "key": "offer",
              "value": {
                "calc": "['CHECK', 'BET 2', 'BET 4'] if bet_amount == 0 else ['CALL', 'FOLD']"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} (first actor): {value}. Pot {pot}."
      },
      "text": "Hand {hand}. You act first. Board: {board_up}. Your hole cards are in your state. Pot {pot}. CHECK, BET 2 or BET 4. A bet is paid into the pot at once and you will not act again this hand."
    },
    {
      "use": "ask",
      "phase": "betting",
      "label": "second actor",
      "to": {
        "where": "you.seat == second_actor"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "each": {
        "do": [
          {
            "set": {
              "player": "$seat",
              "key": "action",
              "value": {
                "calc": "'BET' if $answer in ['BET 2', 'BET 4'] else $answer"
              }
            }
          },
          {
            "set": {
              "key": "bet_amount",
              "value": {
                "calc": "bet_small if $answer == 'BET 2' else bet_large"
              },
              "if": {
                "calc": "$answer in ['BET 2', 'BET 4']"
              }
            }
          },
          {
            "adjust": {
              "player": "$seat",
              "key": "paid",
              "value": {
                "calc": "bet_amount"
              },
              "if": {
                "calc": "$answer in ['BET 2', 'BET 4', 'CALL']"
              }
            }
          },
          {
            "adjust": {
              "key": "pot",
              "value": {
                "calc": "bet_amount"
              },
              "if": {
                "calc": "$answer in ['BET 2', 'BET 4', 'CALL']"
              }
            }
          },
          {
            "set": {
              "player": "$seat",
              "key": "folded",
              "value": true,
              "if": {
                "calc": "$answer == 'FOLD'"
              }
            }
          },
          {
            "set": {
              "players": "all",
              "key": "offer",
              "value": {
                "calc": "['CHECK', 'BET 2', 'BET 4'] if bet_amount == 0 else ['CALL', 'FOLD']"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} (second actor): {value}. Pot {pot}."
      },
      "text": "Hand {hand}. You act second. Board: {board_up}. Your hole cards are in your state. Pot {pot}, current bet {bet_amount}. If nobody has bet you may CHECK, BET 2 or BET 4; if a bet has been made you may CALL (pay the bet into the pot) or FOLD (leave the hand, losing what you paid)."
    },
    {
      "use": "ask",
      "phase": "betting",
      "label": "third actor",
      "to": {
        "where": "you.seat == third_actor"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "each": {
        "do": [
          {
            "set": {
              "player": "$seat",
              "key": "action",
              "value": {
                "calc": "'BET' if $answer in ['BET 2', 'BET 4'] else $answer"
              }
            }
          },
          {
            "set": {
              "key": "bet_amount",
              "value": {
                "calc": "bet_small if $answer == 'BET 2' else bet_large"
              },
              "if": {
                "calc": "$answer in ['BET 2', 'BET 4']"
              }
            }
          },
          {
            "adjust": {
              "player": "$seat",
              "key": "paid",
              "value": {
                "calc": "bet_amount"
              },
              "if": {
                "calc": "$answer in ['BET 2', 'BET 4', 'CALL']"
              }
            }
          },
          {
            "adjust": {
              "key": "pot",
              "value": {
                "calc": "bet_amount"
              },
              "if": {
                "calc": "$answer in ['BET 2', 'BET 4', 'CALL']"
              }
            }
          },
          {
            "set": {
              "player": "$seat",
              "key": "folded",
              "value": true,
              "if": {
                "calc": "$answer == 'FOLD'"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} (third actor): {value}. Pot {pot}."
      },
      "text": "Hand {hand}. You act third. Board: {board_up}. Your hole cards are in your state. Pot {pot}, current bet {bet_amount}. If nobody has bet you may CHECK, BET 2 or BET 4; if a bet has been made you may CALL (pay the bet into the pot) or FOLD (leave the hand, losing what you paid)."
    },
    {
      "use": "poll",
      "phase": "response",
      "label": "response to the bet",
      "when": {
        "calc": "bet_amount > 0"
      },
      "to": {
        "where": "you.action == 'CHECK'"
      },
      "answer": {
        "type": "choice",
        "options": [
          "CALL",
          "FOLD"
        ]
      },
      "store": "action",
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} responds: {value}."
      },
      "text": "You checked and then a bet of {bet_amount} was made. Board: {board_up}. Your hole cards are in your state. Pot {pot}. CALL (pay {bet_amount} into the pot and stay in) or FOLD (leave the hand, losing what you paid). Other checkers choose at the same moment."
    },
    {
      "use": "update",
      "phase": "final board",
      "label": "responses and the final board",
      "do": [
        {
          "adjust": {
            "players": {
              "where": "you.action == 'CALL' and you.paid < ante + bet_amount"
            },
            "key": "paid",
            "value": {
              "calc": "bet_amount"
            }
          }
        },
        {
          "set": {
            "key": "pot",
            "value": {
              "calc": "sum(p.paid for p in players)"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.action == 'FOLD'"
            },
            "key": "folded",
            "value": true
          }
        },
        {
          "append": {
            "key": "board_up",
            "value": {
              "calc": "board_hidden[0]"
            },
            "if": {
              "calc": "len(board_hidden) > 0"
            }
          }
        },
        {
          "set": {
            "key": "board_hidden",
            "value": []
          }
        }
      ],
      "text": "Betting is over. Pot {pot}. Board card 4 is turned face up. Final board: {board_up}."
    },
    {
      "use": "update",
      "phase": "showdown",
      "label": "hand scores",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "hand_score",
            "value": {
              "calc": "you.hole[0] + you.hole[1] + (pair_bonus if you.hole[0] == you.hole[1] else 0) + match_bonus * min(max_matches, count(c == you.hole[0] or c == you.hole[1] for c in board_up))"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "showdown",
      "label": "the showdown",
      "do": [
        {
          "set": {
            "key": "in_count",
            "value": {
              "calc": "count(not p.folded for p in players)"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "not you.folded"
            },
            "key": "won",
            "value": {
              "calc": "pot"
            },
            "if": {
              "calc": "in_count == 1"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "not you.folded"
            },
            "key": "revealed_hole",
            "value": {
              "calc": "you.hole"
            },
            "if": {
              "calc": "in_count >= 2"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "not you.folded"
            },
            "key": "revealed_score",
            "value": {
              "calc": "you.hand_score"
            },
            "if": {
              "calc": "in_count >= 2"
            }
          }
        },
        {
          "set": {
            "key": "best_score",
            "value": {
              "calc": "max([p.hand_score for p in players if not p.folded])"
            },
            "if": {
              "calc": "in_count >= 2"
            }
          }
        },
        {
          "set": {
            "key": "winner_count",
            "value": {
              "calc": "count((not p.folded) and p.hand_score == best_score for p in players)"
            },
            "if": {
              "calc": "in_count >= 2"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "(not you.folded) and you.hand_score == best_score"
            },
            "key": "won",
            "value": {
              "calc": "pot / winner_count"
            },
            "if": {
              "calc": "in_count >= 2 and winner_count > 0"
            }
          }
        }
      ],
      "text": "Showdown ({in_count} still in, pot {pot}). Seat 1 shows {players[0].revealed_hole} score {players[0].revealed_score}, wins {players[0].won}; seat 2 shows {players[1].revealed_hole} score {players[1].revealed_score}, wins {players[1].won}; seat 3 shows {players[2].revealed_hole} score {players[2].revealed_score}, wins {players[2].won}. Folded hands and a lone survivor's hand are not shown."
    },
    {
      "use": "update",
      "phase": "showdown",
      "label": "the totals",
      "do": [
        {
          "adjust": {
            "players": "all",
            "key": "total",
            "value": {
              "calc": "you.won - you.paid"
            }
          }
        }
      ],
      "text": "Totals after hand {hand}: seat 1 {players[0].total}, seat 2 {players[1].total}, seat 3 {players[2].total}."
    },
    {
      "use": "check",
      "phase": "showdown",
      "label": "after the last hand",
      "when": {
        "calc": "hand >= hands"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "hand >= hands"
      },
      "rank_by": "you.total",
      "text": "Winner: {result}. Final totals: Seat 1 {players[0].total}, Seat 2 {players[1].total}, Seat 3 {players[2].total}."
    }
  },
  "limits": {
    "rounds": 40,
    "rounds_max": 40,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "Three players, seats 1, 2 and 3, play exactly {hands} hands. Each starts with a chip total of {starting_total}; totals may go negative and may include fractions from split pots. The sum of all totals is always 0.\n\nThe deck has {deck_size} cards: ranks 1 to {ranks}, {copies_per_rank} copies of each, with no suits. In hand h the FIRST ACTOR is seat ((h - 1) mod 3) + 1, the SECOND ACTOR is the next seat after the first actor (wrapping from 3 to 1), and the THIRD ACTOR is the remaining seat.\n\nEACH HAND:\n1. Deal. All {deck_size} cards are shuffled. Each player gets {hole_cards} hole cards face down and the table gets {board_cards} board cards face down. You see only your own hole cards.\n2. Ante. Each player pays {ante} chip into the pot. The pot starts at {starting_pot}.\n3. Board. Board cards 1, 2 and 3 are turned face up. Board card 4 stays face down.\n4. The first actor chooses CHECK, BET 2 or BET 4. A bet is paid into the pot at once, and the choice is announced to all.\n5. The second actor chooses, announced to all. If nobody has bet yet: CHECK, BET 2 or BET 4. If a bet has been made: CALL (pay the same amount as the bet into the pot) or FOLD (leave the hand, losing everything already paid).\n6. The third actor chooses, with the same options as the second actor, announced to all.\n7. Response. Only if a bet was made after at least one player checked: each player who checked before the bet chooses, at the same moment, CALL (pay the bet amount and stay in) or FOLD (leave the hand, losing what you paid). The choices are then revealed. Only one bet is ever made in a hand: there are no raises, and the bettor never acts again.\n8. Final board. Board card 4 is turned face up.\n9. Hand scores. With hole ranks a and b: score = a + b, plus {pair_bonus} if a equals b, plus {match_bonus} for each board card whose rank equals a or b. At most {max_matches} matches count.\n10. Showdown. If exactly one player has not folded, that player takes the whole pot and no hole cards are revealed. If two or three are still in, their hole cards and scores are revealed and the pot goes to the highest score among them; players tied for the highest score split the pot equally. If everyone checked, all three go to showdown with a pot of {starting_pot}.\n11. Folded players' hole cards are never revealed.\n12. Totals. Each player's total changes by the chips they won minus the chips they paid this hand. All three totals are announced.\n13. All cards return to the deck for the next shuffle.\n\nAfter hand {hands} the game ends. The highest chip total wins; players who share the highest total share the win."
}
```
````
