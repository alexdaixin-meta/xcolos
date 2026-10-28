# Task: write the XColos game file for "Truc Duel"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 2; set `meta.players` to {"min": 2, "max": 2, "suggested": 2} (the suggested size is the one the game plays best at).

CARDS. Use a 32-card pack with four cards of each of eight ranks. Suits do not matter. Rank strength from highest to lowest: 7 (strength 8), 8 (7), A (6), K (5), Q (4), J (3), 10 (2), 9 (1).

SCORES. Both players start at 0 points.

EACH ROUND:
1. Deal. Shuffle the full 32-card pack and deal 3 cards privately to each player. Each player sees only their own hand.
2. First trick. Both players secretly and simultaneously choose one card from their hand to play. If a player names a card not in their hand, their first-listed card is played. Both cards are revealed. The higher strength wins trick 1. Equal strength means trick 1 is spoilt and belongs to no one.
3. Raise poll. Both players secretly and simultaneously choose STAY or TWO MORE. The choices are then revealed.
   - Both STAY: the round is worth 1 point.
   - Both TWO MORE: the round is worth 4 points, and no one may fold.
   - Exactly one TWO MORE: that player is the raiser. The other player, the responder, now answers once with ACCEPT, FOLD or FOUR.
     - ACCEPT: the round is worth 2 points.
     - FOLD: the raiser immediately scores 1 point, and the round ends (skip steps 4 to 6).
     - FOUR: the round is worth 4 points, and the raiser may not fold.
4. Last two tricks. Each player secretly and simultaneously writes the order in which they will play their two remaining cards (first, then second). If a player's answer is invalid, their two cards are played in the order they were dealt.
   - Trick 2 compares each player's first card.
   - Trick 3 compares each player's second card.
   - In each trick, higher strength wins and equal strength is spoilt.
5. Round winner.
   - The player who won more of the three tricks wins the round.
   - If both won the same number (1-1 with one spoilt, or 0-0 with three... see below), the winner of the earliest trick that was not spoilt wins the round.
   - If all three tricks were spoilt, the round is void and no one scores.
6. Scoring. The round winner adds the round's value (1, 2 or 4) to their score.
7. End check. If a player has 12 or more points, the game ends.

ROUND CAP. If 30 rounds have been played and no one has reached 12, the game ends.

There is no talk phase. All information comes from revealed cards and choices.

How the winner is decided: The first player whose score reaches 12 or more wins. Only one player scores in any round, so two players cannot reach 12 at once. If the game ends at the 30-round cap, the player with the higher score wins, and equal scores are a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Truc Duel (2 to 2 players, best with 2)

Two players play three-card hands of three tricks. They can raise the stakes, fold or re-raise, and the first to 12 points wins.

STATE (every item below must exist in the file):
  - each player: score (number, starts 0); everyone sees it. Points won so far.
  - each player: hand (list, starts []); only its owner sees it. Cards still in the hand, in dealt order. Each card is stored as its strength number (8=7, 7=8, 6=A, 5=K, 4=Q, 3=J, 2=10, 1=9).
  - each player: played_cards (list, starts []); everyone sees it. The cards this player has revealed this round, as strengths, in trick order.
  - each player: tricks_won (number, starts 0); everyone sees it. Tricks won in the current round (0 to 3).
  - each player: raise_choice (text, starts ''); everyone sees it. STAY or TWO MORE, revealed after the raise poll.
  - each player: order_choice (text, starts ''); everyone sees it. The order chosen for the last two cards, revealed after the order poll.
  - the table: deck (list, starts [8, 8, 8, 8, 7, 7, 7, 7, 6, 6, 6, 6, 5, 5, 5, 5, 4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1]); hidden from all players. The undealt cards of the 32-card pack, as strengths.
  - the table: round_number (number, starts 0); everyone sees it. Rounds started so far.
  - the table: round_value (number, starts 0); everyone sees it. What the current round is worth: 1, 2 or 4.
  - the table: raiser (number, starts 0); everyone sees it. The seat that alone said TWO MORE; 0 if none or both did.
  - the table: response (text, starts ''); everyone sees it. The responder's ACCEPT, FOLD or FOUR; empty if there was no response.
  - the table: folded (bool, starts False); everyone sees it. True when the responder folded this round.
  - the table: seat1_card (number, starts 0); everyone sees it. Scratch copy of seat 1's card in the current trick, kept so the two seats can be compared.
  - the table: seat2_card (number, starts 0); everyone sees it. Scratch copy of seat 2's card in the current trick.
  - the table: trick1_winner (number, starts 0); everyone sees it. Winning seat of trick 1; 0 if spoilt.
  - the table: trick2_winner (number, starts 0); everyone sees it. Winning seat of trick 2; 0 if spoilt.
  - the table: trick3_winner (number, starts 0); everyone sees it. Winning seat of trick 3; 0 if spoilt.
  - the table: round_winner (number, starts 0); everyone sees it. Seat that wins the round; 0 if the round is void.
  - parameters, each kept as a table attribute: deck_size = 32, ranks = 8, copies_per_rank = 4, hand_size = 3, tricks_per_round = 3, strength_7 = 8, strength_8 = 7, strength_A = 6, strength_K = 5, strength_Q = 4, strength_J = 3, strength_10 = 2, strength_9 = 1, value_both_stay = 1, value_accept = 2, value_four = 4, value_both_raise = 4, fold_payout = 1, win_target = 12, round_cap = 30, starting_score = 0

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seat 1 and seat 2 each start with score 0.
  2. The table deck holds the 32-card pack: four cards of each strength from 1 to 8 (9, 10, J, Q, K, A, 8, 7).
  3. Both players are told the rank order and the stakes rules.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round_number += 1. deck is reset to the full 32-card pack. Each player's hand, played_cards, raise_choice and order_choice are emptied, and tricks_won = 0. round_value = 0, raiser = 0, response = '', folded = false, trick1_winner = trick2_winner = trick3_winner = round_winner = 0.
  2. [update] each player in turn. What happens: Deal: 3 times for each player, pick a random card from deck, append it to that player's hand and remove it from deck.
  3. [sync] all players. What happens: Each player privately sees their own hand (strengths shown with rank names); the opponent's hand stays hidden.
  4. [poll] all players answers: a choice of one card from the player's own hand. What happens: The chosen card is removed from hand and appended to played_cards. An answer that is not in the hand plays the first-listed card of hand. seat1_card and seat2_card are set to the two cards.
  5. [update] all players. What happens: trick1_winner = 1 if seat1_card > seat2_card, 2 if seat2_card > seat1_card, else 0. The trick winner's tricks_won += 1.
  6. [tell] all players. What happens: Announce both trick-1 cards and trick1_winner (or 'spoilt').
  7. [poll] all players answers: STAY or TWO MORE. What happens: Each player's raise_choice is set, then revealed to both.
  8. [update] all players. What happens: If both raise_choice = STAY: round_value = 1. If both = TWO MORE: round_value = 4. If exactly one = TWO MORE: raiser = that seat.
  9. [ask] the seat that is not raiser (the responder), only when raiser != 0 answers: ACCEPT, FOLD or FOUR. What happens: response is set and revealed.
  10. [update] all players. What happens: If response = ACCEPT: round_value = 2. If response = FOUR: round_value = 4. If response = FOLD: the raiser's score += 1, folded = true, round_winner = raiser, and steps 11 to 13 do not apply this round.
  11. [poll] all players, only when folded = false answers: one of the two orderings of the player's two remaining cards: 'X first, then Y' or 'Y first, then X'. What happens: order_choice is set. An invalid answer uses dealt order. Both remaining cards are appended to played_cards in the chosen order and removed from hand.
  12. [update] all players, only when folded = false. What happens: Trick 2: seat1_card and seat2_card = each player's 2nd played card. trick2_winner = higher seat, or 0 if equal; the winner's tricks_won += 1. Trick 3: the same with the 3rd played card, giving trick3_winner. Then round_winner = the seat with more tricks_won. If tricks_won are equal, round_winner = the first non-zero of trick1_winner, trick2_winner, trick3_winner, or 0 if all are 0. If round_winner != 0, that seat's score += round_value.
  13. [tell] all players. What happens: Announce all played cards, the trick winners, round_winner (or 'void' or 'fold'), round_value and both scores.
  14. [check] all players. What happens: End the game if any player's score >= 12 or round_number >= 30; otherwise repeat the round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When a round begins, the deck is reset to all 32 cards (4 of each strength 1 to 8) and each player is dealt 3 cards into their hand, so the deck holds 26 cards.
  R2. When a player's hand is shown, only that player sees it; the opponent does not.
  R3. When a player names a trick-1 card not in their hand, then their first-listed hand card is played.
  R4. When the trick-1 cards differ, then the higher strength wins trick 1 (for example strength 8, the 7, beats strength 7, the 8); when they are equal, trick1_winner is 0 (spoilt).
  R5. When both players choose STAY, then round_value = 1.
  R6. When both players choose TWO MORE, then round_value = 4 and no response is asked, so no one can fold.
  R7. When exactly one player chooses TWO MORE, then the other player is asked once to choose from ACCEPT, FOLD and FOUR.
  R8. When the responder chooses ACCEPT, then round_value = 2.
  R9. When the responder chooses FOUR, then round_value = 4 and the raiser gets no further choice.
  R10. When the responder chooses FOLD, then the raiser's score rises by 1, no further cards are played, and the responder's score is unchanged.
  R11. When a player gives an invalid order for the last two cards, then the two cards are played in dealt order.
  R12. When tricks 2 and 3 are played, then trick 2 compares each player's first chosen card and trick 3 each player's second; higher strength wins and equal strength gives 0.
  R13. When one player has won more tricks than the other, then that player is round_winner.
  R14. When both players have won the same number of tricks and not all were spoilt, then round_winner is the winner of the earliest trick that was not spoilt (for example trick 1 spoilt, seat 2 wins trick 2, seat 1 wins trick 3 gives round_winner 2).
  R15. When all three tricks are spoilt, then round_winner = 0 and no score changes.
  R16. When there is a round winner without a fold, then that player's score rises by round_value (1, 2 or 4) and the other's is unchanged.
  R17. When a player's score reaches 12 or more at the end check, then the game ends and that player wins.
  R18. When 30 rounds have been played and no score is 12 or more, then the game ends and the higher score wins; equal scores are a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - First trick: which card to play | asked: both seats at once | options: each card currently in that seat's own hand (3 cards), shown by rank name
  - Raise poll | asked: both seats at once | options: STAY, TWO MORE
  - Response to a lone raise | asked: only the seat that chose STAY when the other chose TWO MORE | options: ACCEPT, FOLD, FOUR; the raiser is offered nothing
  - Order of the last two cards | asked: both seats at once, only if no one folded | options: 'X first, then Y' and 'Y first, then X', where X and Y are that seat's two remaining cards in dealt order

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: max(score over players) >= 12 or round_number >= 30
  - each player's standing: you.score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: The higher score wins. The game ends as soon as one player reaches 12 or more; only one player scores per round, so that player has the higher score. At the 30-round cap the higher score wins, and equal scores share the win (a draw).
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

- each player: `score` (number, visible: public, starts 0): Points won so far.
- each player: `played_cards` (list, visible: public, starts []): The cards this player has revealed this round, as strengths, in trick order.
- each player: `tricks_won` (number, visible: public, starts 0): Tricks won in the current round (0 to 3).
- each player: `raise_choice` (text, visible: public, starts ''): STAY or TWO MORE, revealed after the raise poll.
- the table: `round_number` (number, visible: public, starts 0): Rounds started so far.
- the table: `round_value` (number, visible: public, starts 0): What the current round is worth: 1, 2 or 4.
- the table: `response` (text, visible: public, starts ''): The responder's ACCEPT, FOLD or FOUR; empty if there was no response.
- the table: `trick1_winner` (number, visible: public, starts 0): Winning seat of trick 1; 0 if spoilt.
- the table: `trick2_winner` (number, visible: public, starts 0): Winning seat of trick 2; 0 if spoilt.
- the table: `trick3_winner` (number, visible: public, starts 0): Winning seat of trick 3; 0 if spoilt.
- the table: `round_winner` (number, visible: public, starts 0): Seat that wins the round; 0 if the round is void.
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 32, ranks = 8, copies_per_rank = 4, hand_size = 3, tricks_per_round = 3, strength_7 = 8, strength_8 = 7, strength_A = 6, strength_K = 5, strength_Q = 4, strength_J = 3, strength_10 = 2, strength_9 = 1, value_both_stay = 1, value_accept = 2, value_four = 4, value_both_raise = 4, fold_payout = 1, win_target = 12, round_cap = 30, starting_score = 0
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
