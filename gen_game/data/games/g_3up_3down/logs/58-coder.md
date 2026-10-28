# 58 coder

- time: 2026-10-28T05:40:37+00:00 (123.2s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 7a1464fd006dda3b, reply sha256 6afbf994bb7b13b1

## Sent

````
# Task: write the XColos game file for "3Up Clear Race"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

CARDS: Ranks 1 to 9, three copies of each (27 cards), plus three Clear cards written 'C'. Low = 1-3, Mid = 4-6, High = 7-9.

ATTRIBUTES. Table: low_stack, mid_stack, high_stack (setup lists), pile (list), top_rank (number, 0 means empty), run_count (number), round (number, starts 0), lead (number), game_over (true/false, starts false). Each seat: hand (PRIVATE list), up_pile (public list), hand_count, up_count, cards_left (public numbers).

SETUP (before round 1):
S1. low_stack = the nine cards 1,1,1,2,2,2,3,3,3; mid_stack = the nine cards 4-6; high_stack = the nine cards 7-9. Shuffle each stack.
S2. Deal to seats 1, 2, 3 in turn: 3 cards from low_stack, 3 from mid_stack, 3 from high_stack, then add one 'C'. Every hand has 10 cards and all stacks end empty.
S3. Face-up pick, done three times (picks 1, 2, 3). Each pick is a simultaneous poll: every seat chooses one card from its own hand. Options are listed numbers ascending, then C last. The chosen card moves from hand to up_pile, which is visible to all. A missing or invalid answer takes the first listed card.
S4. For every seat: hand_count = 7, up_count = 3, cards_left = 10. Set pile = empty, top_rank = 0, run_count = 0.

ROUND (repeat while game_over is false and round < 30):
R1. round = round + 1. lead = ((round - 1) mod 3) + 1.
R2. Seats take one turn each in the order lead, lead+1, lead+2 (seat 3 wraps to seat 1). A turn is skipped if game_over is true.

A TURN (steps T1 to T5):
T1. Options. The source is the hand if hand_count > 0, otherwise the up_pile. For each rank r in the source with r >= top_rank, and for each k from 1 up to the number of copies of r in the source, add the option 'r xk' (for example '5 x2'). List these by rank ascending, then by k ascending. If the source holds a C, add the option 'C', which is ALWAYS listed last and is always legal. If there are no options, the only option is 'take'.
T2. The seat chooses one option (seen only by that seat; the result is announced to all). A missing or invalid answer takes the first option.
T3. Apply the option:
- 'r xk': move k cards of rank r from the source to the pile. If top_rank == r, run_count = run_count + k; otherwise run_count = k. Then top_rank = r.
- 'C': remove that C from the game and clear the pile (T4).
- 'take': move every pile card into the seat's hand, then set top_rank = 0 and run_count = 0.
T4. Clear: if C was played or run_count >= 3, remove all pile cards from the game, and set top_rank = 0 and run_count = 0. The turn then ends; the next seat plays onto the empty pile.
T5. Update hand_count and up_count. Set cards_left = hand_count + up_count. If cards_left == 0, set game_over = true.

END OF ROUND:
E1. If round == 30, set game_over = true.

There is no talk phase. All plays and pickups are announced publicly; hands stay private.

How the winner is decided: The first seat whose cards_left reaches 0 wins immediately. If 30 rounds pass with no seat at 0, the seat with the fewest cards_left wins. If two or more seats tie for fewest, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: 3Up Clear Race (3 to 3 players, best with 3)

Three players shed a 10-card hand onto a climbing pile. A run of three equal ranks or a Clear card wipes the pile, a stuck player must take the pile, and the first to empty hand and face-up cards wins.

STATE (every item below must exist in the file):
  - each player: hand (list, starts []); only its owner sees it. the seat's private hand of cards; each entry is a rank '1'..'9' or 'C'
  - each player: up_pile (list, starts []); everyone sees it. the seat's three face-up cards, played only once the hand is empty
  - each player: hand_count (number, starts 10); everyone sees it. number of cards in hand
  - each player: up_count (number, starts 0); everyone sees it. number of cards in up_pile
  - each player: cards_left (number, starts 10); everyone sees it. hand_count + up_count; the score, where lower is better
  - the table: low_stack (list, starts ['1', '1', '1', '2', '2', '2', '3', '3', '3']); hidden from all players. shuffled low cards to deal from
  - the table: mid_stack (list, starts ['4', '4', '4', '5', '5', '5', '6', '6', '6']); hidden from all players. shuffled mid cards to deal from
  - the table: high_stack (list, starts ['7', '7', '7', '8', '8', '8', '9', '9', '9']); hidden from all players. shuffled high cards to deal from
  - the table: pile (list, starts []); everyone sees it. the central pile of played cards
  - the table: top_rank (number, starts 0); everyone sees it. rank on top of the pile; 0 means the pile is empty
  - the table: run_count (number, starts 0); everyone sees it. how many consecutive cards of top_rank are on the pile
  - the table: round (number, starts 0); everyone sees it. round counter
  - the table: lead (number, starts 0); everyone sees it. seat that plays first this round
  - the table: game_over (bool, starts False); everyone sees it. true once a seat empties or round 30 ends
  - parameters, each kept as a table attribute: min_rank = 1, max_rank = 9, copies_per_rank = 3, clear_cards = 3, low_band_max = 3, mid_band_min = 4, mid_band_max = 6, high_band_min = 7, cards_per_band_dealt = 3, clears_per_seat = 1, hand_size = 10, face_up_picks = 3, hand_after_picks = 7, run_to_clear = 3, max_rounds = 30, empty_top_rank = 0

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Set low_stack to 1,1,1,2,2,2,3,3,3, mid_stack to 4,4,4,5,5,5,6,6,6 and high_stack to 7,7,7,8,8,8,9,9,9, then shuffle each stack.
  2. For seats 1, 2 and 3 in turn, draw 3 random cards from low_stack, 3 from mid_stack and 3 from high_stack into that seat's hand, removing each from its stack, then append one 'C' to the hand. Every hand now has 10 cards and all stacks are empty.
  3. Face-up pick 1: a simultaneous poll in which every seat chooses one card from its own hand. Options are the distinct ranks in the hand in ascending order, then 'C' last if held. The chosen card moves from hand to up_pile. A missing or invalid answer takes the first listed option.
  4. Face-up pick 2: the same poll again.
  5. Face-up pick 3: the same poll again.
  6. For every seat set hand_count = 7, up_count = 3 and cards_left = 10. Set pile = empty, top_rank = 0 and run_count = 0.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round = round + 1; lead = ((round - 1) mod 3) + 1; announce the round and the leading seat
  2. [ask] seat lead (turn slot 1); skipped when game_over is true answers: one option from the list built per rule T1: 'r xk' for each rank r >= top_rank in the source (the hand if hand_count > 0, else up_pile) and each k from 1 to the copies of r there, ascending by r then k; 'C' last if the source holds a C; if there are no options, only 'take'. A missing or invalid answer takes the first option.. What happens: the choice is recorded for this slot and announced to all
  3. [update] seat lead (turn slot 1); skipped when game_over is true. What happens: 'r xk': move k cards of rank r from the source to pile; if top_rank == r then run_count += k else run_count = k; top_rank = r. 'C': remove that C from the source and from the game. 'take': append all pile cards to hand, pile = empty, top_rank = 0, run_count = 0. Then, if 'C' was played or run_count >= 3: remove all pile cards from the game, top_rank = 0, run_count = 0. Then hand_count = length of hand, up_count = length of up_pile, cards_left = hand_count + up_count; if cards_left == 0 then game_over = true. Announce the play.
  4. [ask] seat (lead mod 3) + 1 (turn slot 2); skipped when game_over is true answers: the same option list as slot 1, built for this seat. What happens: the choice is recorded and announced to all
  5. [update] seat (lead mod 3) + 1 (turn slot 2); skipped when game_over is true. What happens: the same play, clear and count updates as slot 1, applied to this seat
  6. [ask] seat ((lead + 1) mod 3) + 1 (turn slot 3); skipped when game_over is true answers: the same option list as slot 1, built for this seat. What happens: the choice is recorded and announced to all
  7. [update] seat ((lead + 1) mod 3) + 1 (turn slot 3); skipped when game_over is true. What happens: the same play, clear and count updates as slot 1, applied to this seat
  8. [update] all players. What happens: if round == 30 then game_over = true
  9. [check] all players. What happens: end the game if game_over is true; otherwise run the round again

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When setup ends, each seat has 7 cards in hand and 3 in up_pile, every hand began as 3 low (1-3), 3 mid (4-6), 3 high (7-9) and 1 'C', and all three stacks are empty.
  R2. When a face-up pick is made, the chosen card leaves the hand and joins that seat's public up_pile; this happens 3 times, simultaneously for all seats.
  R3. When a face-up pick answer is missing or invalid, the first listed card (lowest rank, or 'C' if only C remains) is taken.
  R4. When round increments, lead = ((round - 1) mod 3) + 1, so round 1 is led by seat 1, round 2 by seat 2, round 3 by seat 3 and round 4 by seat 1.
  R5. When a seat takes its turn, seats act in the order lead, lead+1, lead+2, wrapping from seat 3 to seat 1.
  R6. When hand_count > 0, a seat plays from its hand; when hand_count == 0, it plays from its up_pile.
  R7. When top_rank is t, a seat may play k copies (k from 1 to the copies held) of any rank r >= t from its source; with top_rank 0 any rank is legal.
  R8. When a seat holds a 'C' in its source, 'C' is always offered, listed last.
  R9. When a seat has no legal rank play and no C, its only option is 'take'.
  R10. When a seat takes, every pile card moves into its hand and top_rank and run_count become 0.
  R11. When k cards of rank r are played and top_rank == r, run_count increases by k; otherwise run_count becomes k; top_rank becomes r.
  R12. When run_count reaches 3 or more, all pile cards are removed from the game and top_rank and run_count become 0.
  R13. When a 'C' is played, the C and all pile cards are removed from the game and top_rank and run_count become 0.
  R14. When a turn ends, cards_left = hand_count + up_count for that seat.
  R15. When a seat's cards_left becomes 0, game_over becomes true, the remaining turns are skipped, and that seat wins.
  R16. When round 30 ends with no seat at 0, the game ends and the seat with the fewest cards_left wins; seats tied for fewest share the result (a draw).
  R17. When a turn answer is missing or invalid, the first listed option is applied.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Face-up pick (setup, 3 times) | asked: all seats at once | options: each distinct rank in the seat's own hand, ascending, then 'C' last if the hand holds a C
  - Turn play | asked: the seat whose turn slot it is | options: source = hand if hand_count > 0, else up_pile. For each rank r in the source with r >= top_rank, options 'r x1' up to 'r xN' where N is the copies of r in the source, ascending by r then k; then 'C' if the source holds a C. If none of these exist, only 'take'.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: game_over == true
  - each player's standing: 0 - you.cards_left (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: A player's standing is how few cards they have left. A seat that reaches 0 cards_left ends the game at once and is the only seat at 0, so it wins. Otherwise, after round 30, the seat with the fewest cards_left wins, and seats tied for fewest share the result, which the source calls a draw.
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

- each player: `up_pile` (list, visible: public, starts []): the seat's three face-up cards, played only once the hand is empty
- each player: `hand_count` (number, visible: public, starts 10): number of cards in hand
- each player: `up_count` (number, visible: public, starts 0): number of cards in up_pile
- each player: `cards_left` (number, visible: public, starts 10): hand_count + up_count; the score, where lower is better
- parameters (each must be an attribute holding this value, never a number buried in a step): min_rank = 1, max_rank = 9, copies_per_rank = 3, clear_cards = 3, low_band_max = 3, mid_band_min = 4, mid_band_max = 6, high_band_min = 7, cards_per_band_dealt = 3, clears_per_seat = 1, hand_size = 10, face_up_picks = 3, hand_after_picks = 7, run_to_clear = 3, max_rounds = 30, empty_top_rank = 0
- the game ends with ONE ending whose `rank_by` is `0 - you.cards_left`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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

## Guidance from the last attempt

The previous attempt had problems:

1. Move the face-up pick into setup, after the deal (S2) and before round 1. Run it exactly 3 times (use the `face_up_picks` parameter) as a simultaneous poll of all seats. The options are the ranks in the seat's own hand, ascending, with C last.
2. Each pick moves the chosen card from hand to up_pile.
3. After the three picks, set hand_count = hand_after_picks (7), up_count = 3 and cards_left = 10. Also set pile = [], top_rank = empty_top_rank and run_count = 0 (S4).
4. Make sure no pick step runs inside the round loop. Once the picks are done, they must never execute again, including when a test starts from a given state.
5. Guard the fallback expression so it never indexes an empty list. Only compute `offer[0]` when offer is non-empty.
6. Check the turn logic separately:
   - The turn source is the hand when hand_count > 0, otherwise the up_pile.
   - Turn options are 'r xk' for every rank r >= top_rank, with C last.
   - When nothing is legal, the only option is 'take'.


YOUR PREVIOUS GAME FILE WAS REFUSED. Here it is:
```json
{
  "schema": 1,
  "meta": {
    "id": "3up_clear_race",
    "name": "3Up Clear Race",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Three players shed a 10-card hand onto a climbing pile; runs of three or a Clear card wipe it, and the first to run out of cards wins."
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
      {"key": "hand", "visible": "ally", "type": "list", "initial": []},
      {"key": "up_pile", "visible": "public", "type": "list", "initial": []},
      {"key": "hand_count", "visible": "public", "type": "number", "initial": 10},
      {"key": "up_count", "visible": "public", "type": "number", "initial": 0},
      {"key": "cards_left", "visible": "public", "type": "number", "initial": 10},
      {"key": "source", "visible": "ally", "type": "list", "initial": []},
      {"key": "offer", "visible": "ally", "type": "list", "initial": []},
      {"key": "pick_choice", "visible": "ally", "type": "text", "initial": ""},
      {"key": "pick_card", "visible": "ally", "type": "text", "initial": "none"}
    ],
    "game": [
      {"key": "low_stack", "visible": "none", "type": "list", "initial": ["1", "1", "1", "2", "2", "2", "3", "3", "3"]},
      {"key": "mid_stack", "visible": "none", "type": "list", "initial": ["4", "4", "4", "5", "5", "5", "6", "6", "6"]},
      {"key": "high_stack", "visible": "none", "type": "list", "initial": ["7", "7", "7", "8", "8", "8", "9", "9", "9"]},
      {"key": "pile", "visible": "public", "type": "list", "initial": []},
      {"key": "top_rank", "visible": "public", "type": "number", "initial": 0},
      {"key": "run_count", "visible": "public", "type": "number", "initial": 0},
      {"key": "round", "visible": "public", "type": "number", "initial": 0},
      {"key": "lead", "visible": "public", "type": "number", "initial": 0},
      {"key": "game_over", "visible": "public", "type": "bool", "initial": false},
      {"key": "min_rank", "visible": "public", "type": "number", "initial": 1},
      {"key": "max_rank", "visible": "public", "type": "number", "initial": 9},
      {"key": "copies_per_rank", "visible": "public", "type": "number", "initial": 3},
      {"key": "clear_cards", "visible": "public", "type": "number", "initial": 3},
      {"key": "low_band_max", "visible": "public", "type": "number", "initial": 3},
      {"key": "mid_band_min", "visible": "public", "type": "number", "initial": 4},
      {"key": "mid_band_max", "visible": "public", "type": "number", "initial": 6},
      {"key": "high_band_min", "visible": "public", "type": "number", "initial": 7},
      {"key": "cards_per_band_dealt", "visible": "public", "type": "number", "initial": 3},
      {"key": "clears_per_seat", "visible": "public", "type": "number", "initial": 1},
      {"key": "hand_size", "visible": "public", "type": "number", "initial": 10},
      {"key": "face_up_picks", "visible": "public", "type": "number", "initial": 3},
      {"key": "hand_after_picks", "visible": "public", "type": "number", "initial": 7},
      {"key": "run_to_clear", "visible": "public", "type": "number", "initial": 3},
      {"key": "max_rounds", "visible": "public", "type": "number", "initial": 30},
      {"key": "empty_top_rank", "visible": "public", "type": "number", "initial": 0},
      {"key": "rank_labels", "visible": "none", "type": "list", "initial": ["1", "2", "3", "4", "5", "6", "7", "8", "9"]},
      {"key": "pick", "visible": "none", "type": "text", "initial": ""},
      {"key": "actor", "visible": "none", "type": "number", "initial": 0},
      {"key": "last_move", "visible": "public", "type": "text", "initial": "nothing yet"},
      {"key": "cur_offer", "visible": "none", "type": "list", "initial": []},
      {"key": "move_rank", "visible": "none", "type": "number", "initial": 0},
      {"key": "move_k", "visible": "none", "type": "number", "initial": 0},
      {"key": "from_hand", "visible": "none", "type": "bool", "initial": true},
      {"key": "cleared", "visible": "none", "type": "bool", "initial": false}
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "build the stacks",
      "do": [
        {"set": {"key": "low_stack", "value": {"calc": "sorted([r for r in rank_labels if int(r) <= low_band_max] * copies_per_rank)"}}},
        {"set": {"key": "mid_stack", "value": {"calc": "sorted([r for r in rank_labels if int(r) >= mid_band_min and int(r) <= mid_band_max] * copies_per_rank)"}}},
        {"set": {"key": "high_stack", "value": {"calc": "sorted([r for r in rank_labels if int(r) >= high_band_min] * copies_per_rank)"}}}
      ]
    },
    {
      "use": "update",
      "label": "deal seat 1",
      "do": [
        {"set": {"key": "pick", "value": {"calc": "low_stack[min(int(uniform(0, len(low_stack))), len(low_stack) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "low_stack[min(int(uniform(0, len(low_stack))), len(low_stack) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "low_stack[min(int(uniform(0, len(low_stack))), len(low_stack) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[min(int(uniform(0, len(mid_stack))), len(mid_stack) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[min(int(uniform(0, len(mid_stack))), len(mid_stack) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[min(int(uniform(0, len(mid_stack))), len(mid_stack) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[min(int(uniform(0, len(high_stack))), len(high_stack) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[min(int(uniform(0, len(high_stack))), len(high_stack) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[min(int(uniform(0, len(high_stack))), len(high_stack) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"append": {"player": 1, "key": "hand", "value": "C"}}
      ]
    },
    {
      "use": "update",
      "label": "deal seat 2",
      "do": [
        {"set": {"key": "pick", "value": {"calc": "low_stack[min(int(uniform(0, len(low_stack))), len(low_stack) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "low_stack[min(int(uniform(0, len(low_stack))), len(low_stack) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "low_stack[min(int(uniform(0, len(low_stack))), len(low_stack) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[min(int(uniform(0, len(mid_stack))), len(mid_stack) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[min(int(uniform(0, len(mid_stack))), len(mid_stack) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[min(int(uniform(0, len(mid_stack))), len(mid_stack) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[min(int(uniform(0, len(high_stack))), len(high_stack) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[min(int(uniform(0, len(high_stack))), len(high_stack) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[min(int(uniform(0, len(high_stack))), len(high_stack) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"append": {"player": 2, "key": "hand", "value": "C"}}
      ]
    },
    {
      "use": "update",
      "label": "deal seat 3",
      "do": [
        {"set": {"key": "pick", "value": {"calc": "low_stack[min(int(uniform(0, len(low_stack))), len(low_stack) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "low_stack[min(int(uniform(0, len(low_stack))), len(low_stack) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "low_stack[min(int(uniform(0, len(low_stack))), len(low_stack) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[min(int(uniform(0, len(mid_stack))), len(mid_stack) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[min(int(uniform(0, len(mid_stack))), len(mid_stack) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[min(int(uniform(0, len(mid_stack))), len(mid_stack) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[min(int(uniform(0, len(high_stack))), len(high_stack) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[min(int(uniform(0, len(high_stack))), len(high_stack) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[min(int(uniform(0, len(high_stack))), len(high_stack) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"append": {"player": 3, "key": "hand", "value": "C"}}
      ]
    },
    {
      "use": "update",
      "label": "first pick options",
      "do": [
        {"set": {"players": "all", "key": "pick_choice", "value": ""}},
        {"set": {"players": "all", "key": "offer", "value": {"calc": "[r for r in rank_labels if r in you.hand] + (['C'] if 'C' in you.hand else [])"}}}
      ]
    },
    {
      "use": "sync",
      "label": "the deal",
      "mode": "self",
      "to": "all",
      "fields": ["hand", "up_pile", "hand_count", "up_count", "cards_left"],
      "text": "Your dealt hand:"
    }
  ],
  "steps": [
    {
      "use": "poll",
      "phase": "picks",
      "label": "face-up pick 1",
      "when": {"calc": "round == 0 and all(len(p.up_pile) == 0 for p in players)"},
      "to": "acting",
      "answer": {"type": "choice", "options": {"attribute": "offer"}},
      "store": "pick_choice",
      "text": "Face-up pick 1 of {face_up_picks}: choose one card from your hand to place face up in your up_pile, where everyone can see it. You play your face-up cards only once your hand is empty."
    },
    {
      "use": "update",
      "phase": "picks",
      "label": "place face-up card 1",
      "when": {"calc": "round == 0 and all(len(p.up_pile) == 0 for p in players)"},
      "do": [
        {"set": {"players": "all", "key": "pick_card", "value": {"calc": "you.pick_choice if you.pick_choice in you.offer else (you.offer[0] if len(you.offer) > 0 else 'none')"}}},
        {"remove": {"players": {"where": "you.pick_card in you.hand"}, "key": "hand", "value": {"calc": "you.pick_card"}}},
        {"append": {"players": {"where": "you.pick_card != 'none'"}, "key": "up_pile", "value": {"calc": "you.pick_card"}}},
        {"set": {"players": "all", "key": "pick_choice", "value": ""}},
        {"set": {"players": "all", "key": "offer", "value": {"calc": "[r for r in rank_labels if r in you.hand] + (['C'] if 'C' in you.hand else [])"}}}
      ],
      "text": "Face-up pick 1 is placed. Up piles: seat 1 {players[0].up_pile}, seat 2 {players[1].up_pile}, seat 3 {players[2].up_pile}."
    },
    {
      "use": "poll",
      "phase": "picks",
      "label": "face-up pick 2",
      "when": {"calc": "round == 0 and all(len(p.up_pile) == 1 for p in players)"},
      "to": "acting",
      "answer": {"type": "choice", "options": {"attribute": "offer"}},
      "store": "pick_choice",
      "text": "Face-up pick 2 of {face_up_picks}: choose one more card from your hand to place face up in your up_pile."
    },
    {
      "use": "update",
      "phase": "picks",
      "label": "place face-up card 2",
      "when": {"calc": "round == 0 and all(len(p.up_pile) == 1 for p in players)"},
      "do": [
        {"set": {"players": "all", "key": "pick_card", "value": {"calc": "you.pick_choice if you.pick_choice in you.offer else (you.offer[0] if len(you.offer) > 0 else 'none')"}}},
        {"remove": {"players": {"where": "you.pick_card in you.hand"}, "key": "hand", "value": {"calc": "you.pick_card"}}},
        {"append": {"players": {"where": "you.pick_card != 'none'"}, "key": "up_pile", "value": {"calc": "you.pick_card"}}},
        {"set": {"players": "all", "key": "pick_choice", "value": ""}},
        {"set": {"players": "all", "key": "offer", "value": {"calc": "[r for r in rank_labels if r in you.hand] + (['C'] if 'C' in you.hand else [])"}}}
      ],
      "text": "Face-up pick 2 is placed. Up piles: seat 1 {players[0].up_pile}, seat 2 {players[1].up_pile}, seat 3 {players[2].up_pile}."
    },
    {
      "use": "poll",
      "phase": "picks",
      "label": "face-up pick 3",
      "when": {"calc": "round == 0 and all(len(p.up_pile) == face_up_picks - 1 for p in players)"},
      "to": "acting",
      "answer": {"type": "choice", "options": {"attribute": "offer"}},
      "store": "pick_choice",
      "text": "Face-up pick 3 of {face_up_picks}: choose the last card from your hand to place face up in your up_pile."
    },
    {
      "use": "update",
      "phase": "picks",
      "label": "place face-up card 3 and settle",
      "when": {"calc": "round == 0 and all(len(p.up_pile) == face_up_picks - 1 for p in players)"},
      "do": [
        {"set": {"players": "all", "key": "pick_card", "value": {"calc": "you.pick_choice if you.pick_choice in you.offer else (you.offer[0] if len(you.offer) > 0 else 'none')"}}},
        {"remove": {"players": {"where": "you.pick_card in you.hand"}, "key": "hand", "value": {"calc": "you.pick_card"}}},
        {"append": {"players": {"where": "you.pick_card != 'none'"}, "key": "up_pile", "value": {"calc": "you.pick_card"}}},
        {"set": {"players": "all", "key": "pick_choice", "value": ""}},
        {"set": {"players": "all", "key": "hand_count", "value": {"calc": "hand_after_picks"}}},
        {"set": {"players": "all", "key": "up_count", "value": {"calc": "face_up_picks"}}},
        {"set": {"players": "all", "key": "cards_left", "value": {"calc": "hand_size"}}},
        {"set": {"key": "pile", "value": {"calc": "[]"}}},
        {"set": {"key": "top_rank", "value": {"calc": "empty_top_rank"}}},
        {"set": {"key": "run_count", "value": 0}}
      ],
      "text": "The face-up picks are done. Up piles: seat 1 {players[0].up_pile}, seat 2 {players[1].up_pile}, seat 3 {players[2].up_pile}. Every seat has {hand_after_picks} cards in hand and {face_up_picks} face up."
    },
    {
      "use": "update",
      "phase": "round",
      "label": "new round",
      "do": [
        {"adjust": {"key": "round", "value": 1}},
        {"set": {"key": "lead", "value": {"calc": "(round - 1) % len(players) + 1"}}},
        {"set": {"players": "all", "key": "source", "value": {"calc": "you.hand if you.hand_count > 0 else you.up_pile"}}},
        {"set": {"players": "all", "key": "offer", "value": {"calc": "sorted([r + ' x1' for r in rank_labels if int(r) >= top_rank and count(c == r for c in you.source) >= 1] + [r + ' x2' for r in rank_labels if int(r) >= top_rank and count(c == r for c in you.source) >= 2] + [r + ' x3' for r in rank_labels if int(r) >= top_rank and count(c == r for c in you.source) >= 3]) + (['C'] if 'C' in you.source else [])"}}},
        {"set": {"players": {"where": "len(you.offer) == 0"}, "key": "offer", "value": {"calc": "['take']"}}}
      ],
      "text": "Round {round} begins. Seat {lead} leads."
    },
    {
      "use": "ask",
      "phase": "turns",
      "label": "turn slot 1",
      "when": {"calc": "not game_over"},
      "to": {"where": "you.seat == lead"},
      "answer": {"type": "choice", "options": {"attribute": "offer"}},
      "verify": {"bind": "t1"},
      "broadcast": {"to": "all", "text": "Seat {seat} plays: {value}."},
      "text": "Your turn. The pile's top rank is {top_rank} (0 means empty) and the run is {run_count}. Choose one option: 'r xk' plays k cards of rank r, 'C' plays a Clear card, 'take' picks up the whole pile."
    },
    {
      "use": "update",
      "phase": "turns",
      "label": "apply slot 1",
      "when": {"calc": "not game_over"},
      "do": [
        {"set": {"key": "actor", "value": {"calc": "lead"}}},
        {"set": {"key": "cur_offer", "value": {"calc": "players[actor - 1].offer"}}},
        {"set": {"key": "last_move", "value": {"calc": "$t1 if $t1 in cur_offer else (cur_offer[0] if len(cur_offer) > 0 else 'take')"}}},
        {"set": {"key": "move_rank", "value": {"calc": "int(last_move[0]) if last_move not in ['C', 'take'] else 0"}}},
        {"set": {"key": "move_k", "value": {"calc": "int(last_move[3]) if last_move not in ['C', 'take'] else 0"}}},
        {"set": {"key": "from_hand", "value": {"calc": "players[actor - 1].hand_count > 0"}}},
        {"remove": {"player": {"calc": "actor"}, "key": "hand", "value": {"calc": "last_move[0]"}, "if": {"calc": "from_hand and move_k >= 1"}}},
        {"remove": {"player": {"calc": "actor"}, "key": "hand", "value": {"calc": "last_move[0]"}, "if": {"calc": "from_hand and move_k >= 2"}}},
        {"remove": {"player": {"calc": "actor"}, "key": "hand", "value": {"calc": "last_move[0]"}, "if": {"calc": "from_hand and move_k >= 3"}}},
        {"remove": {"player": {"calc": "actor"}, "key": "up_pile", "value": {"calc": "last_move[0]"}, "if": {"calc": "(not from_hand) and move_k >= 1"}}},
        {"remove": {"player": {"calc": "actor"}, "key": "up_pile", "value": {"calc": "last_move[0]"}, "if": {"calc": "(not from_hand) and move_k >= 2"}}},
        {"remove": {"player": {"calc": "actor"}, "key": "up_pile", "value": {"calc": "last_move[0]"}, "if": {"calc": "(not from_hand) and move_k >= 3"}}},
        {"append": {"key": "pile", "value": {"calc": "last_move[0]"}, "if": {"calc": "move_k >= 1"}}},
        {"append": {"key": "pile", "value": {"calc": "last_move[0]"}, "if": {"calc": "move_k >= 2"}}},
        {"append": {"key": "pile", "value": {"calc": "last_move[0]"}, "if": {"calc": "move_k >= 3"}}},
        {"set": {"key": "run_count", "value": {"calc": "run_count + move_k if top_rank == move_rank else move_k"}, "if": {"calc": "move_k > 0"}}},
        {"set": {"key": "top_rank", "value": {"calc": "move_rank"}, "if": {"calc": "move_k > 0"}}},
        {"remove": {"player": {"calc": "actor"}, "key": "hand", "value": "C", "if": {"calc": "last_move == 'C' and from_hand"}}},
        {"remove": {"player": {"calc": "actor"}, "key": "up_pile", "value": "C", "if": {"calc": "last_move == 'C' and not from_hand"}}},
        {"set": {"players": {"where": "you.seat == actor"}, "key": "hand", "value": {"calc": "you.hand + pile"}, "if": {"calc": "last_move == 'take'"}}},
        {"set": {"key": "pile", "value": {"calc": "[]"}, "if": {"calc": "last_move == 'take'"}}},
        {"set": {"key": "top_rank", "value": {"calc": "empty_top_rank"}, "if": {"calc": "last_move == 'take'"}}},
        {"set": {"key": "run_count", "value": 0, "if": {"calc": "last_move == 'take'"}}},
        {"set": {"key": "cleared", "value": {"calc": "last_move == 'C' or run_count >= run_to_clear"}}},
        {"set": {"key": "pile", "value": {"calc": "[]"}, "if": {"calc": "cleared"}}},
        {"set": {"key": "top_rank", "value": {"calc": "empty_top_rank"}, "if": {"calc": "cleared"}}},
        {"set": {"key": "run_count", "value": 0, "if": {"calc": "cleared"}}},
        {"set": {"players": {"where": "you.seat == actor"}, "key": "hand_count", "value": {"calc": "len(you.hand)"}}},
        {"set": {"players": {"where": "you.seat == actor"}, "key": "up_count", "value": {"calc": "len(you.up_pile)"}}},
        {"set": {"players": {"where": "you.seat == actor"}, "key": "cards_left", "value": {"calc": "you.hand_count + you.up_count"}}},
        {"set": {"key": "game_over", "value": {"calc": "game_over or any(p.cards_left == 0 for p in players)"}}},
        {"set": {"players": "all", "key": "source", "value": {"calc": "you.hand if you.hand_count > 0 else you.up_pile"}}},
        {"set": {"players": "all", "key": "offer", "value": {"calc": "sorted([r + ' x1' for r in rank_labels if int(r) >= top_rank and count(c == r for c in you.source) >= 1] + [r + ' x2' for r in rank_labels if int(r) >= top_rank and count(c == r for c in you.source) >= 2] + [r + ' x3' for r in rank_labels if int(r) >= top_rank and count(c == r for c in you.source) >= 3]) + (['C'] if 'C' in you.source else [])"}}},
        {"set": {"players": {"where": "len(you.offer) == 0"}, "key": "offer", "value": {"calc": "['take']"}}}
      ],
      "text": "Seat {actor} played {last_move}. Pile top rank is now {top_rank}, run {run_count}. Cards left: seat 1 {players[0].cards_left}, seat 2 {players[1].cards_left}, seat 3 {players[2].cards_left}."
    },
    {
      "use": "
... (cut)

Why it was refused: it plays, but part of it does nothing: game attribute `rank_labels` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "3up_clear_race",
    "name": "3Up Clear Race",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Three players shed a 10-card hand onto a climbing pile; runs of three or a Clear card wipe it, and the first to run out of cards wins."
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
      {"key": "hand", "visible": "ally", "type": "list", "initial": []},
      {"key": "up_pile", "visible": "public", "type": "list", "initial": []},
      {"key": "hand_count", "visible": "public", "type": "number", "initial": 10},
      {"key": "up_count", "visible": "public", "type": "number", "initial": 0},
      {"key": "cards_left", "visible": "public", "type": "number", "initial": 10},
      {"key": "source", "visible": "ally", "type": "list", "initial": []},
      {"key": "offer", "visible": "ally", "type": "list", "initial": []},
      {"key": "pick_choice", "visible": "ally", "type": "text", "initial": ""},
      {"key": "pick_card", "visible": "ally", "type": "text", "initial": "none"}
    ],
    "game": [
      {"key": "low_stack", "visible": "none", "type": "list", "initial": ["1", "1", "1", "2", "2", "2", "3", "3", "3"]},
      {"key": "mid_stack", "visible": "none", "type": "list", "initial": ["4", "4", "4", "5", "5", "5", "6", "6", "6"]},
      {"key": "high_stack", "visible": "none", "type": "list", "initial": ["7", "7", "7", "8", "8", "8", "9", "9", "9"]},
      {"key": "pile", "visible": "public", "type": "list", "initial": []},
      {"key": "top_rank", "visible": "public", "type": "number", "initial": 0},
      {"key": "run_count", "visible": "public", "type": "number", "initial": 0},
      {"key": "round", "visible": "public", "type": "number", "initial": 0},
      {"key": "lead", "visible": "public", "type": "number", "initial": 0},
      {"key": "game_over", "visible": "public", "type": "bool", "initial": false},
      {"key": "min_rank", "visible": "public", "type": "number", "initial": 1},
      {"key": "max_rank", "visible": "public", "type": "number", "initial": 9},
      {"key": "copies_per_rank", "visible": "public", "type": "number", "initial": 3},
      {"key": "clear_cards", "visible": "public", "type": "number", "initial": 3},
      {"key": "low_band_max", "visible": "public", "type": "number", "initial": 3},
      {"key": "mid_band_min", "visible": "public", "type": "number", "initial": 4},
      {"key": "mid_band_max", "visible": "public", "type": "number", "initial": 6},
      {"key": "high_band_min", "visible": "public", "type": "number", "initial": 7},
      {"key": "cards_per_band_dealt", "visible": "public", "type": "number", "initial": 3},
      {"key": "clears_per_seat", "visible": "public", "type": "number", "initial": 1},
      {"key": "hand_size", "visible": "public", "type": "number", "initial": 10},
      {"key": "face_up_picks", "visible": "public", "type": "number", "initial": 3},
      {"key": "hand_after_picks", "visible": "public", "type": "number", "initial": 7},
      {"key": "run_to_clear", "visible": "public", "type": "number", "initial": 3},
      {"key": "max_rounds", "visible": "public", "type": "number", "initial": 30},
      {"key": "empty_top_rank", "visible": "public", "type": "number", "initial": 0},
      {"key": "rank_labels", "visible": "none", "type": "list", "initial": []},
      {"key": "pick", "visible": "none", "type": "text", "initial": ""},
      {"key": "actor", "visible": "none", "type": "number", "initial": 0},
      {"key": "last_move", "visible": "public", "type": "text", "initial": "nothing yet"},
      {"key": "cur_offer", "visible": "none", "type": "list", "initial": []},
      {"key": "move_rank", "visible": "none", "type": "number", "initial": 0},
      {"key": "move_k", "visible": "none", "type": "number", "initial": 0},
      {"key": "from_hand", "visible": "none", "type": "bool", "initial": true},
      {"key": "cleared", "visible": "none", "type": "bool", "initial": false}
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "build the stacks",
      "do": [
        {"set": {"key": "rank_labels", "value": {"calc": "[r for r in ['1', '2', '3', '4', '5', '6', '7', '8', '9'] if int(r) >= min_rank and int(r) <= max_rank]"}}},
        {"set": {"key": "low_stack", "value": {"calc": "sorted([r for r in rank_labels if int(r) <= low_band_max] * copies_per_rank)"}}},
        {"set": {"key": "mid_stack", "value": {"calc": "sorted([r for r in rank_labels if int(r) >= mid_band_min and int(r) <= mid_band_max] * copies_per_rank)"}}},
        {"set": {"key": "high_stack", "value": {"calc": "sorted([r for r in rank_labels if int(r) >= high_band_min] * copies_per_rank)"}}}
      ]
    },
    {
      "use": "update",
      "label": "deal seat 1",
      "do": [
        {"set": {"key": "pick", "value": {"calc": "low_stack[min(int(uniform(0, len(low_stack))), len(low_stack) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "low_stack[min(int(uniform(0, len(low_stack))), len(low_stack) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "low_stack[min(int(uniform(0, len(low_stack))), len(low_stack) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[min(int(uniform(0, len(mid_stack))), len(mid_stack) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[min(int(uniform(0, len(mid_stack))), len(mid_stack) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[min(int(uniform(0, len(mid_stack))), len(mid_stack) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[min(int(uniform(0, len(high_stack))), len(high_stack) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[min(int(uniform(0, len(high_stack))), len(high_stack) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[min(int(uniform(0, len(high_stack))), len(high_stack) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"append": {"player": 1, "key": "hand", "value": "C"}}
      ]
    },
    {
      "use": "update",
      "label": "deal seat 2",
      "do": [
        {"set": {"key": "pick", "value": {"calc": "low_stack[min(int(uniform(0, len(low_stack))), len(low_stack) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "low_stack[min(int(uniform(0, len(low_stack))), len(low_stack) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "low_stack[min(int(uniform(0, len(low_stack))), len(low_stack) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[min(int(uniform(0, len(mid_stack))), len(mid_stack) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[min(int(uniform(0, len(mid_stack))), len(mid_stack) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[min(int(uniform(0, len(mid_stack))), len(mid_stack) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[min(int(uniform(0, len(high_stack))), len(high_stack) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[min(int(uniform(0, len(high_stack))), len(high_stack) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[min(int(uniform(0, len(high_stack))), len(high_stack) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"append": {"player": 2, "key": "hand", "value": "C"}}
      ]
    },
    {
      "use": "update",
      "label": "deal seat 3",
      "do": [
        {"set": {"key": "pick", "value": {"calc": "low_stack[min(int(uniform(0, len(low_stack))), len(low_stack) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "low_stack[min(int(uniform(0, len(low_stack))), len(low_stack) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "low_stack[min(int(uniform(0, len(low_stack))), len(low_stack) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[min(int(uniform(0, len(mid_stack))), len(mid_stack) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[min(int(uniform(0, len(mid_stack))), len(mid_stack) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[min(int(uniform(0, len(mid_stack))), len(mid_stack) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[min(int(uniform(0, len(high_stack))), len(high_stack) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[min(int(uniform(0, len(high_stack))), len(high_stack) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[min(int(uniform(0, len(high_stack))), len(high_stack) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"append": {"player": 3, "key": "hand", "value": "C"}}
      ]
    },
    {
      "use": "update",
      "label": "first pick options",
      "do": [
        {"set": {"players": "all", "key": "pick_choice", "value": ""}},
        {"set": {"players": "all", "key": "offer", "value": {"calc": "[r for r in rank_labels if r in you.hand] + (['C'] if 'C' in you.hand else [])"}}}
      ]
    },
    {
      "use": "sync",
      "label": "the deal",
      "mode": "self",
      "to": "all",
      "fields": ["hand", "up_pile", "hand_count", "up_count", "cards_left"],
      "text": "Your dealt hand:"
    }
  ],
  "steps": [
    {
      "use": "poll",
      "phase": "picks",
      "label": "face-up pick 1",
      "when": {"calc": "round == 0 and all(len(p.up_pile) == 0 for p in players)"},
      "to": "acting",
      "answer": {"type": "choice", "options": {"attribute": "offer"}},
      "store": "pick_choice",
      "text": "Face-up pick 1 of {face_up_picks}: choose one card from your hand to place face up in your up_pile, where everyone can see it. You play your face-up cards only once your hand is empty."
    },
    {
      "use": "update",
      "phase": "picks",
      "label": "place face-up card 1",
      "when": {"calc": "round == 0 and all(len(p.up_pile) == 0 for p in players)"},
      "do": [
        {"set": {"players": "all", "key": "pick_card", "value": {"calc": "you.pick_choice if you.pick_choice in you.offer else (you.offer[0] if len(you.offer) > 0 else 'none')"}}},
        {"remove": {"players": {"where": "you.pick_card in you.hand"}, "key": "hand", "value": {"calc": "you.pick_card"}}},
        {"append": {"players": {"where": "you.pick_card != 'none'"}, "key": "up_pile", "value": {"calc": "you.pick_card"}}},
        {"set": {"players": "all", "key": "pick_choice", "value": ""}},
        {"set": {"players": "all", "key": "offer", "value": {"calc": "[r for r in rank_labels if r in you.hand] + (['C'] if 'C' in you.hand else [])"}}}
      ],
      "text": "Face-up pick 1 is placed. Up piles: seat 1 {players[0].up_pile}, seat 2 {players[1].up_pile}, seat 3 {players[2].up_pile}."
    },
    {
      "use": "poll",
      "phase": "picks",
      "label": "face-up pick 2",
      "when": {"calc": "round == 0 and all(len(p.up_pile) == 1 for p in players)"},
      "to": "acting",
      "answer": {"type": "choice", "options": {"attribute": "offer"}},
      "store": "pick_choice",
      "text": "Face-up pick 2 of {face_up_picks}: choose one more card from your hand to place face up in your up_pile."
    },
    {
      "use": "update",
      "phase": "picks",
      "label": "place face-up card 2",
      "when": {"calc": "round == 0 and all(len(p.up_pile) == 1 for p in players)"},
      "do": [
        {"set": {"players": "all", "key": "pick_card", "value": {"calc": "you.pick_choice if you.pick_choice in you.offer else (you.offer[0] if len(you.offer) > 0 else 'none')"}}},
        {"remove": {"players": {"where": "you.pick_card in you.hand"}, "key": "hand", "value": {"calc": "you.pick_card"}}},
        {"append": {"players": {"where": "you.pick_card != 'none'"}, "key": "up_pile", "value": {"calc": "you.pick_card"}}},
        {"set": {"players": "all", "key": "pick_choice", "value": ""}},
        {"set": {"players": "all", "key": "offer", "value": {"calc": "[r for r in rank_labels if r in you.hand] + (['C'] if 'C' in you.hand else [])"}}}
      ],
      "text": "Face-up pick 2 is placed. Up piles: seat 1 {players[0].up_pile}, seat 2 {players[1].up_pile}, seat 3 {players[2].up_pile}."
    },
    {
      "use": "poll",
      "phase": "picks",
      "label": "face-up pick 3",
      "when": {"calc": "round == 0 and all(len(p.up_pile) == face_up_picks - 1 for p in players)"},
      "to": "acting",
      "answer": {"type": "choice", "options": {"attribute": "offer"}},
      "store": "pick_choice",
      "text": "Face-up pick 3 of {face_up_picks}: choose the last card from your hand to place face up in your up_pile."
    },
    {
      "use": "update",
      "phase": "picks",
      "label": "place face-up card 3 and settle",
      "when": {"calc": "round == 0 and all(len(p.up_pile) == face_up_picks - 1 for p in players)"},
      "do": [
        {"set": {"players": "all", "key": "pick_card", "value": {"calc": "you.pick_choice if you.pick_choice in you.offer else (you.offer[0] if len(you.offer) > 0 else 'none')"}}},
        {"remove": {"players": {"where": "you.pick_card in you.hand"}, "key": "hand", "value": {"calc": "you.pick_card"}}},
        {"append": {"players": {"where": "you.pick_card != 'none'"}, "key": "up_pile", "value": {"calc": "you.pick_card"}}},
        {"set": {"players": "all", "key": "pick_choice", "value": ""}},
        {"set": {"players": "all", "key": "hand_count", "value": {"calc": "hand_after_picks"}}},
        {"set": {"players": "all", "key": "up_count", "value": {"calc": "face_up_picks"}}},
        {"set": {"players": "all", "key": "cards_left", "value": {"calc": "hand_size"}}},
        {"set": {"key": "pile", "value": {"calc": "[]"}}},
        {"set": {"key": "top_rank", "value": {"calc": "empty_top_rank"}}},
        {"set": {"key": "run_count", "value": 0}}
      ],
      "text": "The face-up picks are done. Up piles: seat 1 {players[0].up_pile}, seat 2 {players[1].up_pile}, seat 3 {players[2].up_pile}. Every seat has {hand_after_picks} cards in hand and {face_up_picks} face up."
    },
    {
      "use": "update",
      "phase": "round",
      "label": "new round",
      "do": [
        {"adjust": {"key": "round", "value": 1}},
        {"set": {"key": "lead", "value": {"calc": "(round - 1) % len(players) + 1"}}},
        {"set": {"players": "all", "key": "source", "value": {"calc": "you.hand if you.hand_count > 0 else you.up_pile"}}},
        {"set": {"players": "all", "key": "offer", "value": {"calc": "sorted([r + ' x1' for r in rank_labels if int(r) >= top_rank and count(c == r for c in you.source) >= 1] + [r + ' x2' for r in rank_labels if int(r) >= top_rank and count(c == r for c in you.source) >= 2] + [r + ' x3' for r in rank_labels if int(r) >= top_rank and count(c == r for c in you.source) >= 3]) + (['C'] if 'C' in you.source else [])"}}},
        {"set": {"players": {"where": "len(you.offer) == 0"}, "key": "offer", "value": {"calc": "['take']"}}}
      ],
      "text": "Round {round} begins. Seat {lead} leads."
    },
    {
      "use": "ask",
      "phase": "turns",
      "label": "turn slot 1",
      "when": {"calc": "not game_over"},
      "to": {"where": "you.seat == lead"},
      "answer": {"type": "choice", "options": {"attribute": "offer"}},
      "verify": {"bind": "t1"},
      "broadcast": {"to": "all", "text": "Seat {seat} plays: {value}."},
      "text": "Your turn. The pile's top rank is {top_rank} (0 means empty) and the run is {run_count}. Choose one option: 'r xk' plays k cards of rank r, 'C' plays a Clear card, 'take' picks up the whole pile."
    },
    {
      "use": "update",
      "phase": "turns",
      "label": "apply slot 1",
      "when": {"calc": "not game_over"},
      "do": [
        {"set": {"key": "actor", "value": {"calc": "lead"}}},
        {"set": {"key": "cur_offer", "value": {"calc": "players[actor - 1].offer"}}},
        {"set": {"key": "last_move", "value": {"calc": "$t1 if $t1 in cur_offer else (cur_offer[0] if len(cur_offer) > 0 else 'take')"}}},
        {"set": {"key": "move_rank", "value": {"calc": "int(last_move[0]) if last_move not in ['C', 'take'] else 0"}}},
        {"set": {"key": "move_k", "value": {"calc": "int(last_move[3]) if last_move not in ['C', 'take'] else 0"}}},
        {"set": {"key": "from_hand", "value": {"calc": "players[actor - 1].hand_count > 0"}}},
        {"remove": {"player": {"calc": "actor"}, "key": "hand", "value": {"calc": "last_move[0]"}, "if": {"calc": "from_hand and move_k >= 1"}}},
        {"remove": {"player": {"calc": "actor"}, "key": "hand", "value": {"calc": "last_move[0]"}, "if": {"calc": "from_hand and move_k >= 2"}}},
        {"remove": {"player": {"calc": "actor"}, "key": "hand", "value": {"calc": "last_move[0]"}, "if": {"calc": "from_hand and move_k >= 3"}}},
        {"remove": {"player": {"calc": "actor"}, "key": "up_pile", "value": {"calc": "last_move[0]"}, "if": {"calc": "(not from_hand) and move_k >= 1"}}},
        {"remove": {"player": {"calc": "actor"}, "key": "up_pile", "value": {"calc": "last_move[0]"}, "if": {"calc": "(not from_hand) and move_k >= 2"}}},
        {"remove": {"player": {"calc": "actor"}, "key": "up_pile", "value": {"calc": "last_move[0]"}, "if": {"calc": "(not from_hand) and move_k >= 3"}}},
        {"append": {"key": "pile", "value": {"calc": "last_move[0]"}, "if": {"calc": "move_k >= 1"}}},
        {"append": {"key": "pile", "value": {"calc": "last_move[0]"}, "if": {"calc": "move_k >= 2"}}},
        {"append": {"key": "pile", "value": {"calc": "last_move[0]"}, "if": {"calc": "move_k >= 3"}}},
        {"set": {"key": "run_count", "value": {"calc": "run_count + move_k if top_rank == move_rank else move_k"}, "if": {"calc": "move_k > 0"}}},
        {"set": {"key": "top_rank", "value": {"calc": "move_rank"}, "if": {"calc": "move_k > 0"}}},
        {"remove": {"player": {"calc": "actor"}, "key": "hand", "value": "C", "if": {"calc": "last_move == 'C' and from_hand"}}},
        {"remove": {"player": {"calc": "actor"}, "key": "up_pile", "value": "C", "if": {"calc": "last_move == 'C' and not from_hand"}}},
        {"set": {"players": {"where": "you.seat == actor"}, "key": "hand", "value": {"calc": "you.hand + pile"}, "if": {"calc": "last_move == 'take'"}}},
        {"set": {"key": "pile", "value": {"calc": "[]"}, "if": {"calc": "last_move == 'take'"}}},
        {"set": {"key": "top_rank", "value": {"calc": "empty_top_rank"}, "if": {"calc": "last_move == 'take'"}}},
        {"set": {"key": "run_count", "value": 0, "if": {"calc": "last_move == 'take'"}}},
        {"set": {"key": "cleared", "value": {"calc": "last_move == 'C' or run_count >= run_to_clear"}}},
        {"set": {"key": "pile", "value": {"calc": "[]"}, "if": {"calc": "cleared"}}},
        {"set": {"key": "top_rank", "value": {"calc": "empty_top_rank"}, "if": {"calc": "cleared"}}},
        {"set": {"key": "run_count", "value": 0, "if": {"calc": "cleared"}}},
        {"set": {"players": {"where": "you.seat == actor"}, "key": "hand_count", "value": {"calc": "len(you.hand)"}}},
        {"set": {"players": {"where": "you.seat == actor"}, "key": "up_count", "value": {"calc": "len(you.up_pile)"}}},
        {"set": {"players": {"where": "you.seat == actor"}, "key": "cards_left", "value": {"calc": "you.hand_count + you.up_count"}}},
        {"set": {"key": "game_over", "value": {"calc": "game_over or any(p.cards_left == 0 for p in players)"}}},
        {"set": {"players": "all", "key": "source", "value": {"calc": "you.hand if you.hand_count > 0 else you.up_pile"}}},
        {"set": {"players": "all", "key": "offer", "value": {"calc": "sorted([r + ' x1' for r in rank_labels if int(r) >= top_rank and count(c == r for c in you.source) >= 1] + [r + ' x2' for r in rank_labels if int(r) >= top_rank and count(c == r for c in you.source) >= 2] + [r + ' x3' for r in rank_labels if int(r) >= top_rank and count(c == r for c in you.source) >= 3]) + (['C'] if 'C' in you.source else [])"}}},
        {"set": {"players": {"where": "len(you.offer) == 0"}, "key": "offer", "value": {"calc": "['take']"}}}
      ],
      "text": "Seat {actor} played {last_move}. Pile top rank is now {top_rank}, run {run_count}. Cards left: seat 1 {players[0].cards_left}, seat 2 {players[1].cards_left}, seat 3 {players[2].cards_left}."
    },
    {
      "use": "ask",
      "phase": "turns",
      "label": "turn slot 2",
      "when": {"calc": "not game_over"},
      "to": {"where": "you.seat == lead % len(players) + 1"},
      "answer": {"type": "choice", "options": {"attribute": "offer"}},
      "verify": {"bind": "t2"},
      "broadcast": {"to": "all", "text": "Seat {seat} plays: {value}."},
      "text": "Your turn. The pile's top rank is {top_rank} (0 means empty) and the run is {run_count}. Choose one option: 'r xk' plays k cards of rank r, 'C' plays a Clear card, 'take' picks up the whole pile."
    },
    {
      "use": "update",
      "phase": "turns",
      "label": "apply slot 2",
      "when": {"calc": "not game_over"},
      "do": [
        {"set": {"key": "actor", "value": {"calc": "lead % len(players) + 1"}}},
        {"set": {"key": "cur_offer", "value": {"calc": "players[actor - 1].offer"}}},
        {"set": {"key": "last_move", "value": {"calc": "$t2 if $t2 in cur_offer else (cur_offer[0] if len(cur_offer) > 0 else 'take')"}}},
        {"set": {"key": "move_rank", "value": {"calc": "int(last_move[0]) if last_move not in ['C', 'take'] else 0"}}},
        {"set": {"key": "move_k", "value": {"calc": "int(last_move[3]) if last_move not in ['C', 'take'] else 0"}}},
        {"set": {"key": "from_hand", "value": {"calc": "players[actor - 1].hand_count > 0"}}},
        {"remove": {"player": {"calc": "actor"}, "key": "hand", "value": {"calc": "last_move[0]"}, "if": {"calc": "from_hand and move_k >= 1"}}},
        {"remove": {"player": {"calc": "actor"}, "key": "hand", "value": {"calc": "last_move[0]"}, "if": {"calc": "from_hand and move_k >= 2"}}},
        {"remove": {"player": {"calc": "actor"}, "key": "hand", "value": {"calc": "last_move[0]"}, "if": {"calc": "from_hand and move_k >= 3"}}},
        {"remove": {"player": {"calc": "actor"}, "key": "up_pile", "value": {"calc": "last_move[0]"}, "if": {"calc": "(not from_hand) and move_k >= 1"}}},
        {"remove": {"player": {"calc": "actor"}, "key": "up_pile", "value": {"calc": "last_move[0]"}, "if": {"calc": "(not from_hand) and move_k >= 2"}}},
        {"remove": {"player": {"calc": "actor"}, "key": "up_pile", "value": {"calc": "last_move[0]"}, "if": {"calc": "(not from_hand) and move_k >= 3"}}},
        {"append": {"key": "pile", "value": {"calc": "last_move[0]"}, "if": {"calc": "move_k >= 1"}}},
        {"append": {"key": "pile", "value": {"calc": "last_move[0]"}, "if": {"calc": "move_k >= 2"}}},
        {"append": {"key": "pile", "value": {"calc": "last_move[0]"}, "if": {"calc": "move_k >= 3"}}},
        {"set": {"key": "run_count", "value": {"calc": "run_count + move_k if top_rank == move_rank else move_k"}, "if": {"calc": "move_k > 0"}}},
        {"set": {"key": "top_rank", "value": {"calc": "move_rank"}, "if": {"calc": "move_k > 0"}}},
        {"remove": {"player": {"calc": "actor"}, "key": "hand", "value": "C", "if": {"calc": "last_move == 'C' and from_hand"}}},
        {"remove": {"player": {"calc": "actor"}, "key": "up_pile", "value": "C", "if": {"calc": "last_move == 'C' and not from_hand"}}},
        {"set": {"players": {"where": "you.seat == actor"}, "key": "hand", "value": {"calc": "you.hand + pile"}, "if": {"calc": "last_move == 'take'"}}},
        {"set": {"key": "pile", "value": {"calc": "[]"}, "if": {"calc": "last_move == 'take'"}}},
        {"set": {"key": "top_rank", "value": {"calc": "empty_top_rank"}, "if": {"calc": "last_move == 'take'"}}},
        {"set": {"key": "run_count", "value": 0, "if": {"calc": "last_move == 'take'"}}},
        {"set": {"key": "cleared", "value": {"calc": "last_move == 'C' or run_count >= run_to_clear"}}},
        {"set": {"key": "pile", "value": {"calc": "[]"}, "if": {"calc": "cleared"}}},
        {"set": {"key": "top_rank", "value": {"calc": "empty_top_rank"}, "if": {"calc": "cleared"}}},
        {"set": {"key": "run_count", "value": 0, "if": {"calc": "cleared"}}},
        {"set": {"players": {"where": "you.seat == actor"}, "key": "hand_count", "value": {"calc": "len(you.hand)"}}},
        {"set": {"players": {"where": "you.seat == actor"}, "key": "up_count", "value": {"calc": "len(you.up_pile)"}}},
        {"set": {"players": {"where": "you.seat == actor"}, "key": "cards_left", "value": {"calc": "you.hand_count + you.up_count"}}},
        {"set": {"key": "game_over", "value": {"calc": "game_over or any(p.cards_left == 0 for p in players)"}}},
        {"set": {"players": "all", "key": "source", "value": {"calc": "you.hand if you.hand_count > 0 else you.up_pile"}}},
        {"set": {"players": "all", "key": "offer", "value": {"calc": "sorted([r + ' x1' for r in rank_labels if int(r) >= top_rank and count(c == r for c in you.source) >= 1] + [r + ' x2' for r in rank_labels if int(r) >= top_rank and count(c == r for c in you.source) >= 2] + [r + ' x3' for r in rank_labels if int(r) >= top_rank and count(c == r for c in you.source) >= 3]) + (['C'] if 'C' in you.source else [])"}}},
        {"set": {"players": {"where": "len(you.offer) == 0"}, "key": "offer", "value": {"calc": "['take']"}}}
      ],
      "text": "Seat {actor} played {last_move}. Pile top rank is now {top_rank}, run {run_count}. Cards left: seat 1 {players[0].cards_left}, seat 2 {players[1].cards_left}, seat 3 {players[2].cards_left}."
    },
    {
      "use": "ask",
      "phase": "turns",
      "label": "turn slot 3",
      "when": {"calc": "not game_over"},
      "to": {"where": "you.seat == (lead + 1) % len(players) + 1"},
      "answer": {"type": "choice", "options": {"attribute": "offer"}},
      "verify": {"bind": "t3"},
      "broadcast": {"to": "all", "text": "Seat {seat} plays: {value}."},
      "text": "Your turn. The pile's top rank is {top_rank} (0 means empty) and the run is {run_count}. Choose one option: 'r xk' plays k cards of rank r, 'C' plays a Clear card, 'take' picks up the whole pile."
    },
    {
      "use": "update",
      "phase": "turns",
      "label": "apply slot 3",
      "when": {"calc": "not game_over"},
      "do": [
        {"set": {"key": "actor", "value": {"calc": "(lead + 1) % len(players) + 1"}}},
        {"set": {"key": "cur_offer", "value": {"calc": "players[actor - 1].offer"}}},
        {"set": {"key": "last_move", "value": {"calc": "$t3 if $t3 in cur_offer else (cur_offer[0] if len(cur_offer) > 0 else 'take')"}}},
        {"set": {"key": "move_rank", "value": {"calc": "int(last_move[0]) if last_move not in ['C', 'take'] else 0"}}},
        {"set": {"key": "move_k", "value": {"calc": "int(last_move[3]) if last_move not in ['C', 'take'] else 0"}}},
        {"set": {"key": "from_hand", "value": {"calc": "players[actor - 1].hand_count > 0"}}},
        {"remove": {"player": {"calc": "actor"}, "key": "hand", "value": {"calc": "last_move[0]"}, "if": {"calc": "from_hand and move_k >= 1"}}},
        {"remove": {"player": {"calc": "actor"}, "key": "hand", "value": {"calc": "last_move[0]"}, "if": {"calc": "from_hand and move_k >= 2"}}},
        {"remove": {"player": {"calc": "actor"}, "key": "hand", "value": {"calc": "last_move[0]"}, "if": {"calc": "from_hand and move_k >= 3"}}},
        {"remove": {"player": {"calc": "actor"}, "key": "up_pile", "value": {"calc": "last_move[0]"}, "if": {"calc": "(not from_hand) and move_k >= 1"}}},
        {"remove": {"player": {"calc": "actor"}, "key": "up_pile", "value": {"calc": "last_move[0]"}, "if": {"calc": "(not from_hand) and move_k >= 2"}}},
        {"remove": {"player": {"calc": "actor"}, "key": "up_pile", "value": {"calc": "last_move[0]"}, "if": {"calc": "(not from_hand) and move_k >= 3"}}},
        {"append": {"key": "pile", "value": {"calc": "last_move[0]"}, "if": {"calc": "move_k >= 1"}}},
        {"append": {"key": "pile", "value": {"calc": "last_move[0]"}, "if": {"calc": "move_k >= 2"}}},
        {"append": {"key": "pile", "value": {"calc": "last_move[0]"}, "if": {"calc": "move_k >= 3"}}},
        {"set": {"key": "run_count", "value": {"calc": "run_count + move_k if top_rank == move_rank else move_k"}, "if": {"calc": "move_k > 0"}}},
        {"set": {"key": "top_rank", "value": {"calc": "move_rank"}, "if": {"calc": "move_k > 0"}}},
        {"remove": {"player": {"calc": "actor"}, "key": "hand", "value": "C", "if": {"calc": "last_move == 'C' and from_hand"}}},
        {"remove": {"player": {"calc": "actor"}, "key": "up_pile", "value": "C", "if": {"calc": "last_move == 'C' and not from_hand"}}},
        {"set": {"players": {"where": "you.seat == actor"}, "key": "hand", "value": {"calc": "you.hand + pile"}, "if": {"calc": "last_move == 'take'"}}},
        {"set": {"key": "pile", "value": {"calc": "[]"}, "if": {"calc": "last_move == 'take'"}}},
        {"set": {"key": "top_rank", "value": {"calc": "empty_top_rank"}, "if": {"calc": "last_move == 'take'"}}},
        {"set": {"key": "run_count", "value": 0, "if": {"calc": "last_move == 'take'"}}},
        {"set": {"key": "cleared", "value": {"calc": "last_move == 'C' or run_count >= run_to_clear"}}},
        {"set": {"key": "pile", "value": {"calc": "[]"}, "if": {"calc": "cleared"}}},
        {"set": {"key": "top_rank", "value": {"calc": "empty_top_rank"}, "if": {"calc": "cleared"}}},
        {"set": {"key": "run_count", "value": 0, "if": {"calc": "cleared"}}},
        {"set": {"players": {"where": "you.seat == actor"}, "key": "hand_count", "value": {"calc": "len(you.hand)"}}},
        {"set": {"players": {"where": "you.seat == actor"}, "key": "up_count", "value": {"calc": "len(you.up_pile)"}}},
        {"set": {"players": {"where": "you.seat == actor"}, "key": "cards_left", "value": {"calc": "you.hand_count + you.up_count"}}},
        {"set": {"key": "game_over", "value": {"calc": "game_over or any(p.cards_left == 0 for p in players)"}}},
        {"set": {"players": "all", "key": "source", "value": {"calc": "you.hand if you.hand_count > 0 else you.up_pile"}}},
        {"set": {"players": "all", "key": "offer", "value": {"calc": "sorted([r + ' x1' for r in rank_labels if int(r) >= top_rank and count(c == r for c in you.source) >= 1] + [r + ' x2' for r in rank_labels if int(r) >= top_rank and count(c == r for c in you.source) >= 2] + [r + ' x3' for r in rank_labels if int(r) >= top_rank and count(c == r for c in you.source) >= 3]) + (['C'] if 'C' in you.source else [])"}}},
        {"set": {"players": {"where": "len(you.offer) == 0"}, "key": "offer", "value": {"calc": "['take']"}}}
      ],
      "text": "Seat {actor} played {last_move}. Pile top rank is now {top_rank}, run {run_count}. Cards left: seat 1 {players[0].cards_left}, seat 2 {players[1].cards_left}, seat 3 {players[2].cards_left}."
    },
    {
      "use": "update",
      "phase": "end of round",
      "label": "round limit",
      "do": [
        {"set": {"key": "game_over", "value": true, "if": {"calc": "round >= max_rounds"}}}
      ]
    },
    {
      "use": "check",
      "phase": "end of round",
      "label": "is it over",
      "when": {"calc": "game_over"},
      "against": ["over"]
    }
  ],
  "end": {
    "over": {
      "when": {"calc": "game_over"},
      "rank_by": "0 - you.cards_left",
      "text": "Winner: {result}. Cards left: Seat 1 {players[0].cards_left}, Seat 2 {players[1].cards_left}, Seat 3 {players[2].cards_left}."
    }
  },
  "limits": {
    "rounds": 31,
    "rounds_max": 31,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "CARDS: Ranks {min_rank} to {max_rank}, {copies_per_rank} copies of each, plus {clear_cards} Clear cards written 'C'. Low = 1-{low_band_max}, Mid = {mid_band_min}-{mid_band_max}, High = {high_band_min}-{max_rank}.\n\nSETUP: Each seat is dealt {cards_per_band_dealt} random low, {cards_per_band_dealt} mid and {cards_per_band_dealt} high cards plus {clears_per_seat} C: {hand_size} cards, kept private. Then {face_up_picks} face-up picks are made, all seats choosing at the same time: each pick moves one card of your choice (options are the ranks in your hand ascending, then C last) from your hand to your public up_pile. A missing or invalid pick takes the first listed card. You then hold {hand_after_picks} in hand and {face_up_picks} face up.\n\nROUNDS: Each round the lead moves one seat: round 1 is led by seat 1, round 2 by seat 2, round 3 by seat 3, round 4 by seat 1, and so on. Seats play in order lead, lead+1, lead+2 (seat 3 wraps to seat 1).\n\nA TURN: You play from your hand while it has cards; once your hand is empty you play from your up_pile. Your options: for each rank r you hold with r at least the pile's top rank (top rank {empty_top_rank} means empty, so anything goes), 'r xk' for k from 1 up to the copies of r you hold, listed by rank then k; then 'C' last if you hold a C (always legal). If you have none of these, your only option is 'take'. A missing or invalid answer plays the first listed option.\n- 'r xk': the k cards go on the pile. If the top rank was already r, the run grows by k; otherwise the run becomes k. The top rank becomes r.\n- 'C': the C and the whole pile are removed from the game; top rank and run reset to 0.\n- 'take': every pile card goes into your hand; top rank and run reset to 0.\nIf the run reaches {run_to_clear} or more, the whole pile is removed from the game and top rank and run reset to 0; if it does not, the pile stays. After your turn, cards_left = cards in hand + cards in up_pile. All plays are announced; hands stay private. There is no talk.\n\nWINNING: The first seat whose cards_left reaches 0 ends the game at once (remaining turns are skipped) and wins. If {max_rounds} rounds pass with nobody at 0, the seat with the fewest cards_left wins; seats tied for fewest share the result (a draw)."
}
```
````
