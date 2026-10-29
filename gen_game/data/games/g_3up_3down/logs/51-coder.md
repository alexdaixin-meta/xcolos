# 51 coder

- time: 2026-10-28T05:24:28+00:00 (202.9s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 ba0299bba1d603d3, reply sha256 dd5d979ed042e29c

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

1. Run S3 inside setup, before the round loop, so it happens even when zero rounds are played. Do three simultaneous polls in which every seat picks one card from its own hand. Options are the distinct numbers in ascending order with 'C' last, and a missing or invalid answer takes the first option. Move the chosen card from hand to up_pile.
2. Then apply S4: hand_count = hand_after_picks (7), up_count = face_up_picks (3), cards_left = 10, pile = [], top_rank = empty_top_rank, run_count = 0.
3. In T1, build the offer from the source. That is the hand when hand_count > 0, otherwise the up_pile. List 'r xk' for every rank r >= top_rank and every k from 1 up to the copies held, by rank then by k. Add 'C' last if the source holds one, and use ['take'] when nothing qualifies.
4. Never index offer[0] on an empty list. Compute the full offer, including the 'take' fallback, before you resolve the choice, and resolve the choice from that same list. Do not use a separate hand-only 'offer' built during setup.
5. Make sure T3 removes cards from the correct source. In 'r xk', k cards leave the source, and a 'take' adds the pile to the hand.
6. After every turn, recompute hand_count, up_count and cards_left from the real list lengths.

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
    "blurb": "Shed a 10-card hand onto a climbing pile: three of a rank or a Clear card wipes it, a stuck player takes it, and the first to run out wins."
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
        "key": "hand",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "up_pile",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "hand_count",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "up_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "cards_left",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "pick_choice",
        "visible": "ally",
        "type": "text",
        "initial": ""
      }
    ],
    "game": [
      {
        "key": "low_stack",
        "visible": "none",
        "type": "list",
        "initial": ["1", "1", "1", "2", "2", "2", "3", "3", "3"]
      },
      {
        "key": "mid_stack",
        "visible": "none",
        "type": "list",
        "initial": ["4", "4", "4", "5", "5", "5", "6", "6", "6"]
      },
      {
        "key": "high_stack",
        "visible": "none",
        "type": "list",
        "initial": ["7", "7", "7", "8", "8", "8", "9", "9", "9"]
      },
      {
        "key": "pile",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "top_rank",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "run_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "lead",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "game_over",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "min_rank",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "max_rank",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "copies_per_rank",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "clear_cards",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "low_band_max",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "mid_band_min",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "mid_band_max",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "high_band_min",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "cards_per_band_dealt",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "clears_per_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "hand_size",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "face_up_picks",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "hand_after_picks",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "run_to_clear",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "max_rounds",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "empty_top_rank",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "ranks",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "all_plays",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "turn_seat",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "choice",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "play_rank",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "play_k",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "from_hand",
        "visible": "none",
        "type": "bool",
        "initial": true
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "S1 the stacks",
      "do": [
        {
          "set": {
            "key": "low_stack",
            "value": {
              "calc": "['1', '1', '1', '2', '2', '2', '3', '3', '3']"
            }
          }
        },
        {
          "set": {
            "key": "mid_stack",
            "value": {
              "calc": "['4', '4', '4', '5', '5', '5', '6', '6', '6']"
            }
          }
        },
        {
          "set": {
            "key": "high_stack",
            "value": {
              "calc": "['7', '7', '7', '8', '8', '8', '9', '9', '9']"
            }
          }
        },
        {
          "set": {
            "key": "ranks",
            "value": {
              "calc": "['1', '2', '3', '4', '5', '6', '7', '8', '9']"
            }
          }
        },
        {
          "set": {
            "key": "all_plays",
            "value": {
              "calc": "['1 x1', '1 x2', '1 x3', '2 x1', '2 x2', '2 x3', '3 x1', '3 x2', '3 x3', '4 x1', '4 x2', '4 x3', '5 x1', '5 x2', '5 x3', '6 x1', '6 x2', '6 x3', '7 x1', '7 x2', '7 x3', '8 x1', '8 x2', '8 x3', '9 x1', '9 x2', '9 x3']"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "S2 deal seat 1",
      "do": [
        {"set": {"key": "pick", "value": {"calc": "low_stack[int(uniform(0, len(low_stack)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "low_stack[int(uniform(0, len(low_stack)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "low_stack[int(uniform(0, len(low_stack)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[int(uniform(0, len(mid_stack)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[int(uniform(0, len(mid_stack)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[int(uniform(0, len(mid_stack)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[int(uniform(0, len(high_stack)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[int(uniform(0, len(high_stack)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[int(uniform(0, len(high_stack)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"append": {"player": 1, "key": "hand", "value": "C"}}
      ]
    },
    {
      "use": "update",
      "label": "S2 deal seat 2",
      "do": [
        {"set": {"key": "pick", "value": {"calc": "low_stack[int(uniform(0, len(low_stack)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "low_stack[int(uniform(0, len(low_stack)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "low_stack[int(uniform(0, len(low_stack)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[int(uniform(0, len(mid_stack)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[int(uniform(0, len(mid_stack)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[int(uniform(0, len(mid_stack)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[int(uniform(0, len(high_stack)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[int(uniform(0, len(high_stack)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[int(uniform(0, len(high_stack)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"append": {"player": 2, "key": "hand", "value": "C"}}
      ]
    },
    {
      "use": "update",
      "label": "S2 deal seat 3",
      "do": [
        {"set": {"key": "pick", "value": {"calc": "low_stack[int(uniform(0, len(low_stack)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "low_stack[int(uniform(0, len(low_stack)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "low_stack[int(uniform(0, len(low_stack)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[int(uniform(0, len(mid_stack)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[int(uniform(0, len(mid_stack)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[int(uniform(0, len(mid_stack)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[int(uniform(0, len(high_stack)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[int(uniform(0, len(high_stack)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[int(uniform(0, len(high_stack)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"append": {"player": 3, "key": "hand", "value": "C"}}
      ]
    },
    {
      "use": "update",
      "label": "offer face-up pick 1",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "pick_choice",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "[r for r in ranks if r in you.hand] + (['C'] if 'C' in you.hand else [])"
            }
          }
        }
      ]
    },
    {
      "use": "poll",
      "label": "face-up pick 1",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "store": "pick_choice",
      "text": "Face-up pick 1 of {face_up_picks}: choose one card from your hand to place face up in your up_pile, where everyone can see it."
    },
    {
      "use": "update",
      "label": "apply face-up pick 1",
      "do": [
        {
          "append": {
            "players": "all",
            "key": "up_pile",
            "value": {
              "calc": "you.pick_choice if you.pick_choice in you.offer else you.offer[0]"
            },
            "text": "Seat {player} turns {value} face up."
          }
        },
        {
          "remove": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "you.pick_choice if you.pick_choice in you.offer else you.offer[0]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "pick_choice",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "[r for r in ranks if r in you.hand] + (['C'] if 'C' in you.hand else [])"
            }
          }
        }
      ]
    },
    {
      "use": "poll",
      "label": "face-up pick 2",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "store": "pick_choice",
      "text": "Face-up pick 2 of {face_up_picks}: choose one card from your hand to place face up in your up_pile, where everyone can see it."
    },
    {
      "use": "update",
      "label": "apply face-up pick 2",
      "do": [
        {
          "append": {
            "players": "all",
            "key": "up_pile",
            "value": {
              "calc": "you.pick_choice if you.pick_choice in you.offer else you.offer[0]"
            },
            "text": "Seat {player} turns {value} face up."
          }
        },
        {
          "remove": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "you.pick_choice if you.pick_choice in you.offer else you.offer[0]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "pick_choice",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "[r for r in ranks if r in you.hand] + (['C'] if 'C' in you.hand else [])"
            }
          }
        }
      ]
    },
    {
      "use": "poll",
      "label": "face-up pick 3",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "store": "pick_choice",
      "text": "Face-up pick 3 of {face_up_picks}: choose one card from your hand to place face up in your up_pile, where everyone can see it."
    },
    {
      "use": "update",
      "label": "apply face-up pick 3 and S4",
      "do": [
        {
          "append": {
            "players": "all",
            "key": "up_pile",
            "value": {
              "calc": "you.pick_choice if you.pick_choice in you.offer else you.offer[0]"
            },
            "text": "Seat {player} turns {value} face up."
          }
        },
        {
          "remove": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "you.pick_choice if you.pick_choice in you.offer else you.offer[0]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "pick_choice",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "[]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_count",
            "value": {
              "calc": "hand_after_picks"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "up_count",
            "value": {
              "calc": "face_up_picks"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "cards_left",
            "value": {
              "calc": "hand_after_picks + face_up_picks"
            }
          }
        },
        {
          "set": {
            "key": "pile",
            "value": {
              "calc": "[]"
            }
          }
        },
        {
          "set": {
            "key": "top_rank",
            "value": {
              "calc": "empty_top_rank"
            }
          }
        },
        {
          "set": {
            "key": "run_count",
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
      "phase": "round",
      "label": "round start",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "key": "lead",
            "value": {
              "calc": "((round - 1) % len(players)) + 1"
            },
            "text": "Round {round} begins. Seat {value} leads."
          }
        },
        {
          "set": {
            "key": "turn_seat",
            "value": {
              "calc": "lead"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == turn_seat"
            },
            "key": "offer",
            "value": {
              "calc": "[o for o in all_plays if int(o[0]) >= top_rank and count(c == o[0] for c in (you.hand if you.hand_count > 0 else you.up_pile)) >= int(o[3])] + (['C'] if 'C' in (you.hand if you.hand_count > 0 else you.up_pile) else [])"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == turn_seat and len(you.offer) == 0"
            },
            "key": "offer",
            "value": {
              "calc": "['take']"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "turn",
      "label": "turn slot 1",
      "when": {
        "calc": "not game_over"
      },
      "to": {
        "where": "you.seat == turn_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "play1"
      },
      "text": "Your turn. The pile top is {top_rank} (0 means empty) with a run of {run_count}. Choose a play: 'r xk' plays k cards of rank r, 'C' plays a Clear card, 'take' picks up the whole pile."
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "apply slot 1",
      "when": {
        "calc": "not game_over"
      },
      "do": [
        {"set": {"key": "choice", "value": {"calc": "$play1 if $play1 in [p.offer for p in players if p.seat == turn_seat][0] else [p.offer for p in players if p.seat == turn_seat][0][0]"}, "text": "Seat {turn_seat} plays {value}."}},
        {"set": {"key": "from_hand", "value": {"calc": "[p.hand_count for p in players if p.seat == turn_seat][0] > 0"}}},
        {"set": {"key": "play_k", "value": 0}},
        {"set": {"key": "play_rank", "value": ""}},
        {"set": {"key": "play_k", "value": {"calc": "int(choice[3])"}, "if": {"calc": "choice not in ['C', 'take']"}}},
        {"set": {"key": "play_rank", "value": {"calc": "choice[0]"}, "if": {"calc": "choice not in ['C', 'take']"}}},
        {"remove": {"player": {"calc": "turn_seat"}, "key": "hand", "value": {"calc": "play_rank"}, "if": {"calc": "from_hand and play_k >= 1"}}},
        {"remove": {"player": {"calc": "turn_seat"}, "key": "hand", "value": {"calc": "play_rank"}, "if": {"calc": "from_hand and play_k >= 2"}}},
        {"remove": {"player": {"calc": "turn_seat"}, "key": "hand", "value": {"calc": "play_rank"}, "if": {"calc": "from_hand and play_k >= 3"}}},
        {"remove": {"player": {"calc": "turn_seat"}, "key": "up_pile", "value": {"calc": "play_rank"}, "if": {"calc": "not from_hand and play_k >= 1"}}},
        {"remove": {"player": {"calc": "turn_seat"}, "key": "up_pile", "value": {"calc": "play_rank"}, "if": {"calc": "not from_hand and play_k >= 2"}}},
        {"remove": {"player": {"calc": "turn_seat"}, "key": "up_pile", "value": {"calc": "play_rank"}, "if": {"calc": "not from_hand and play_k >= 3"}}},
        {"append": {"key": "pile", "value": {"calc": "play_rank"}, "if": {"calc": "play_k >= 1"}}},
        {"append": {"key": "pile", "value": {"calc": "play_rank"}, "if": {"calc": "play_k >= 2"}}},
        {"append": {"key": "pile", "value": {"calc": "play_rank"}, "if": {"calc": "play_k >= 3"}}},
        {"set": {"key": "run_count", "value": {"calc": "run_count + play_k if int(play_rank) == top_rank else play_k"}, "if": {"calc": "play_k > 0"}}},
        {"set": {"key": "top_rank", "value": {"calc": "int(play_rank)"}, "if": {"calc": "play_k > 0"}}},
        {"remove": {"player": {"calc": "turn_seat"}, "key": "hand", "value": "C", "if": {"calc": "from_hand and choice == 'C'"}}},
        {"remove": {"player": {"calc": "turn_seat"}, "key": "up_pile", "value": "C", "if": {"calc": "not from_hand and choice == 'C'"}}},
        {"set": {"player": {"calc": "turn_seat"}, "key": "hand", "value": {"calc": "[p.hand for p in players if p.seat == turn_seat][0] + pile"}, "if": {"calc": "choice == 'take'"}, "text": "Seat {turn_seat} takes the pile into hand."}},
        {"set": {"key": "pile", "value": {"calc": "[]"}, "if": {"calc": "choice == 'take'"}}},
        {"set": {"key": "pile", "value": {"calc": "[]"}, "if": {"calc": "choice == 'C' or run_count >= run_to_clear"}, "text": "The pile is cleared and removed from the game."}},
        {"set": {"key": "top_rank", "value": {"calc": "empty_top_rank"}, "if": {"calc": "choice in ['C', 'take'] or run_count >= run_to_clear"}}},
        {"set": {"key": "run_count", "value": 0, "if": {"calc": "choice in ['C', 'take'] or run_count >= run_to_clear"}}},
        {"set": {"players": {"where": "you.seat == turn_seat"}, "key": "hand_count", "value": {"calc": "len(you.hand)"}}},
        {"set": {"players": {"where": "you.seat == turn_seat"}, "key": "up_count", "value": {"calc": "len(you.up_pile)"}}},
        {"set": {"players": {"where": "you.seat == turn_seat"}, "key": "cards_left", "value": {"calc": "you.hand_count + you.up_count"}}},
        {"set": {"key": "game_over", "value": true, "if": {"calc": "[p.cards_left for p in players if p.seat == turn_seat][0] == 0"}, "text": "Seat {turn_seat} has no cards left."}},
        {"set": {"key": "turn_seat", "value": {"calc": "(lead % len(players)) + 1"}}},
        {"set": {"players": {"where": "you.seat == turn_seat"}, "key": "offer", "value": {"calc": "[o for o in all_plays if int(o[0]) >= top_rank and count(c == o[0] for c in (you.hand if you.hand_count > 0 else you.up_pile)) >= int(o[3])] + (['C'] if 'C' in (you.hand if you.hand_count > 0 else you.up_pile) else [])"}}},
        {"set": {"players": {"where": "you.seat == turn_seat and len(you.offer) == 0"}, "key": "offer", "value": {"calc": "['take']"}}}
      ]
    },
    {
      "use": "ask",
      "phase": "turn",
      "label": "turn slot 2",
      "when": {
        "calc": "not game_over"
      },
      "to": {
        "where": "you.seat == turn_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "play2"
      },
      "text": "Your turn. The pile top is {top_rank} (0 means empty) with a run of {run_count}. Choose a play: 'r xk' plays k cards of rank r, 'C' plays a Clear card, 'take' picks up the whole pile."
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "apply slot 2",
      "when": {
        "calc": "not game_over"
      },
      "do": [
        {"set": {"key": "choice", "value": {"calc": "$play2 if $play2 in [p.offer for p in players if p.seat == turn_seat][0] else [p.offer for p in players if p.seat == turn_seat][0][0]"}, "text": "Seat {turn_seat} plays {value}."}},
        {"set": {"key": "from_hand", "value": {"calc": "[p.hand_count for p in players if p.seat == turn_seat][0] > 0"}}},
        {"set": {"key": "play_k", "value": 0}},
        {"set": {"key": "play_rank", "value": ""}},
        {"set": {"key": "play_k", "value": {"calc": "int(choice[3])"}, "if": {"calc": "choice not in ['C', 'take']"}}},
        {"set": {"key": "play_rank", "value": {"calc": "choice[0]"}, "if": {"calc": "choice not in ['C', 'take']"}}},
        {"remove": {"player": {"calc": "turn_seat"}, "key": "hand", "value": {"calc": "play_rank"}, "if": {"calc": "from_hand and play_k >= 1"}}},
        {"remove": {"player": {"calc": "turn_seat"}, "key": "hand", "value": {"calc": "play_rank"}, "if": {"calc": "from_hand and play_k >= 2"}}},
        {"remove": {"player": {"calc": "turn_seat"}, "key": "hand", "value": {"calc": "play_rank"}, "if": {"calc": "from_hand and play_k >= 3"}}},
        {"remove": {"player": {"calc": "turn_seat"}, "key": "up_pile", "value": {"calc": "play_rank"}, "if": {"calc": "not from_hand and play_k >= 1"}}},
        {"remove": {"player": {"calc": "turn_seat"}, "key": "up_pile", "value": {"calc": "play_rank"}, "if": {"calc": "not from_hand and play_k >= 2"}}},
        {"remove": {"player": {"calc": "turn_seat"}, "key": "up_pile", "value": {"calc": "play_rank"}, "if": {"calc": "not from_hand and play_k >= 3"}}},
        {"append": {"key": "pile", "value": {"calc": "play_rank"}, "if": {"calc": "play_k >= 1"}}},
        {"append": {"key": "pile", "value": {"calc": "play_rank"}, "if": {"calc": "play_k >= 2"}}},
        {"append": {"key": "pile", "value": {"calc": "play_rank"}, "if": {"calc": "play_k >= 3"}}},
        {"set": {"key": "run_count", "value": {"calc": "run_count + play_k if int(play_rank) == top_rank else play_k"}, "if": {"calc": "play_k > 0"}}},
        {"set": {"key": "top_rank", "value": {"calc": "int(play_rank)"}, "if": {"calc": "play_k > 0"}}},
        {"remove": {"player": {"calc": "turn_seat"}, "key": "hand", "value": "C", "if": {"calc": "from_hand and choice == 'C'"}}},
        {"remove": {"player": {"calc": "turn_seat"}, "key": "up_pile", "value": "C", "if": {"calc": "not from_hand and choice == 'C'"}}},
        {"set": {"player": {"calc": "turn_seat"}, "key": "hand", "value": {"calc": "[p.hand for p in players if p.seat == turn_seat][0] + pile"}, "if": {"calc": "choice == 'take'"}, "text": "Seat {turn_seat} takes the pile into hand."}},
        {"set": {"key": "pile", "value": {"calc": "[]"}, "if": {"calc": "choice == 'take'"}}},
        {"set": {"key": "pile", "value": {"calc": "[]"}, "if": {"calc": "choice == 'C' or run_count >= run_to_clear"}, "text": "The pile is cleared and removed from the game."}},
        {"set": {"key": "top_rank", "value": {"calc": "empty_top_rank"}, "if": {"calc": "choice in ['C', 'take'] or run_count >= run_to_clear"}}},
        {"set": {"key": "run_count", "value": 0, "if": {"calc": "choice in ['C', 'take'] or run_count >= run_to_clear"}}},
        {"set": {"players": {"where": "you.seat == turn_seat"}, "key": "hand_count", "value": {"calc": "len(you.hand)"}}},
        {"set": {"players": {"where": "you.seat == turn_seat"}, "key": "up_count", "value": {"calc": "len(you.up_pile)"}}},
        {"set": {"players": {"where": "you.seat == turn_seat"}, "key": "cards_left", "value": {"calc": "you.hand_count + you.up_count"}}},
        {"set": {"key": "game_over", "value": true, "if": {"calc": "[p.cards_left for p in players if p.seat == turn_seat][0] == 0"}, "text": "Seat {turn_seat} has no cards left."}},
        {"set": {"key": "turn_seat", "value": {"calc": "((lead + 1) % len(players)) + 1"}}},
        {"set": {"players": {"where": "you.seat == turn_seat"}, "key": "offer", "value": {"calc": "[o for o in all_plays if int(o[0]) >= top_rank and count(c == o[0] for c in (you.hand if you.hand_count > 0 else you.up_pile)) >= int(o[3])] + (['C'] if 'C' in (you.hand if you.hand_count > 0 else you.up_pile) else [])"}}},
        {"set": {"players": {"where": "you.seat == turn_seat and len(you.offer) == 0"}, "key": "offer", "value": {"calc": "['take']"}}}
      ]
    },
    {
      "use": "ask",
      "phase": "turn",
      "label": "turn slot 3",
      "when": {
        "calc": "not game_over"
      },
      "to": {
        "where": "you.seat == turn_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "play3"
      },
      "text": "Your turn. The pile top is {top_rank} (0 means empty) with a run of {run_count}. Choose a play: 'r xk' plays k cards of rank r, 'C' plays a Clear card, 'take' picks up the whole pile."
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "apply slot 3",
      "when": {
        "calc": "not game_over"
      },
      "do": [
        {"set": {"key": "choice", "value": {"calc": "$play3 if $play3 in [p.offer for p in players if p.seat == turn_seat][0] else [p.offer for p in players if p.seat == turn_seat][0][0]"}, "text": "Seat {turn_seat} plays {value}."}},
        {"set": {"key": "from_hand", "value": {"calc": "[p.hand_count for p in players if p.seat == turn_seat][0] > 0"}}},
        {"set": {"key": "play_k", "value": 0}},
        {"set": {"key": "play_rank", "value": ""}},
        {"set": {"key": "play_k", "value": {"calc": "int(choice[3])"}, "if": {"calc": "choice not in ['C', 'take']"}}},
        {"set": {"key": "play_rank", "value": {"calc": "choice[0]"}, "if": {"calc": "choice not in ['C', 'take']"}}},
        {"remove": {"player": {"calc": "turn_seat"}, "key": "hand", "value": {"calc": "play_rank"}, "if": {"calc": "from_hand and play_k >= 1"}}},
        {"remove": {"player": {"calc": "turn_seat"}, "key": "hand", "value": {"calc": "play_rank"}, "if": {"calc": "from_hand and play_k >= 2"}}},
        {"remove": {"player": {"calc": "turn_seat"}, "key": "hand", "value": {"calc": "play_rank"}, "if": {"calc": "from_hand and play_k >= 3"}}},
        {"remove": {"player": {"calc": "turn_seat"}, "key": "up_pile", "value": {"calc": "play_rank"}, "if": {"calc": "not from_hand and play_k >= 1"}}},
        {"remove": {"player": {"calc": "turn_seat"}, "key": "up_pile", "value": {"calc": "play_rank"}, "if": {"calc": "not from_hand and play_k >= 2"}}},
        {"remove": {"player": {"calc": "turn_seat"}, "key": "up_pile", "value": {"calc": "play_rank"}, "if": {"calc": "not from_hand and play_k >= 3"}}},
        {"append": {"key": "pile", "value": {"calc": "play_rank"}, "if": {"calc": "play_k >= 1"}}},
        {"append": {"key": "pile", "value": {"calc": "play_rank"}, "if": {"calc": "play_k >= 2"}}},
        {"append": {"key": "pile", "value": {"calc": "play_rank"}, "if": {"calc": "play_k >= 3"}}},
        {"set": {"key": "run_count", "value": {"calc": "run_count + play_k if int(play_rank) == top_rank else play_k"}, "if": {"calc": "play_k > 0"}}},
        {"set": {"key": "top_rank", "value": {"calc": "int(play_rank)"}, "if": {"calc": "play_k > 0"}}},
        {"remove": {"player": {"calc": "turn_seat"}, "key": "hand", "value": "C", "if": {"calc": "from_hand and choice == 'C'"}}},
        {"remove": {"player": {"calc": "turn_seat"}, "key": "up_pile", "value": "C", "if": {"calc": "not from_hand and choice == 'C'"}}},
        {"set": {"player": {"calc": "turn_seat"}, "key": "hand", "value": {"calc": "[p.hand for p in players if p.seat == turn_seat][0] + pile"}, "if": {"calc": "choice == 'take'"}, "text": "Seat {turn_seat} takes the pile into hand."}},
        {"set": {"key": "pile", "value": {"calc": "[]"}, "if": {"calc": "choice == 'take'"}}},
        {"set": {"key": "pile", "value": {"calc": "[]"}, "if": {"calc": "choice == 'C' or run_count >= run_to_clear"}, "text": "The pile is cleared and removed from the game."}},
        {"set": {"key": "top_rank", "value": {"calc": "empty_top_rank"}, "if": {"calc": "choice in ['C', 'take'] or run_count >= run_to_clear"}}},
        {"set": {"key": "run_count", "value": 0, "if": {"calc": "choice in ['C', 'take'] or run_count >= run_to_clear"}}},
        {"set": {"players": {"where": "you.seat == turn_seat"}, "key": "hand_count", "value": {"calc": "len(you.hand)"}}},
        {"set": {"players": {"where": "you.seat == turn_seat"}, "key": "up_count", "value": {"calc": "len(you.up_pile)"}}},
        {"set": {"players": {"where": "you.seat == turn_seat"}, "key": "cards_left", "value": {"calc": "you.hand_count + you.up_count"}}},
        {"set": {"key": "game_over", "value": true, "if": {"calc": "[p.cards_left for p in players if p.seat == turn_seat][0] == 0"}, "text": "Seat {turn_seat} has no cards left."}}
      ]
    },
    {
      "use": "update",
      "phase": "end of round",
      "label": "round cap",
      "do": [
        {
          "set": {
            "key": "game_over",
            "value": true,
            "if": {
              "calc": "round >= max_rounds and not game_over"
            },
            "text": "Round {max_rounds} is over. The game ends."
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "end of round",
      "label": "is it over",
      "when": {
        "calc": "game_over"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "game_over"
      },
      "rank_by": "0 - you.cards_left",
      "text": "Winner: {result}. Cards left: Seat 1 {players[0].cards_left}, Seat 2 {players[1].cards_left}, Seat 3 {players[2].cards_left}."
    }
  },
  "limits": {
    "rounds": 30,
    "rounds_max": 31,
    "actions_max": 1000,
    "deadline_s": 120
  },
  "rules": "CARDS: ranks {min_rank} to {max_rank}, {copies_per_rank} copies of each, plus {clear_cards} Clear cards written 'C'. Low = 1-{low_band_max}, Mid = {mid_band_min}-{mid_band_max}, High = {high_band_min}-{max_rank}.\n\nSETUP: each seat is dealt {cards_per_band_dealt} random Low, {cards_per_band_dealt} random Mid and {cards_per_band_dealt} random High cards, plus {clears_per_seat} C: {hand_size} cards, kept private. Then, {face_up_picks} times, every seat at the same moment chooses one card from its own hand (options: the distinct ranks you hold in ascending order, then C last if you hold one); the chosen card moves into your up_pile, face up for everyone to see. A missing or invalid answer takes the first listed card. You then hold {hand_after_picks} cards in hand and {face_up_picks} face up.\n\nROUNDS: each round the lead seat moves on one (round 1 seat 1, round 2 seat 2, round 3 seat 3, round 4 seat 1 ...), and seats play one turn each in the order lead, lead+1, lead+2, wrapping from seat 3 to seat 1.\n\nA TURN: you play from your hand while it has cards; when your hand is empty you play from your up_pile. Your options: 'r xk' plays k cards of rank r (k from 1 up to the copies you hold) for any rank r at least the pile's top rank (top rank {empty_top_rank} means the pile is empty and any rank is legal); 'C' is always offered, listed last, if you hold one. If you have no legal rank and no C, your only option is 'take'. A missing or invalid answer plays the first listed option.\n- Playing k cards of rank r: if r equals the top rank, the run count rises by k; otherwise the run count becomes k. The top rank becomes r. If the run count reaches {run_to_clear} or more, the pile is cleared: all its cards leave the game and the top rank and run count return to 0. Otherwise the pile stays and the next seat must play onto it.\n- Playing C: the C and every pile card leave the game, and the top rank and run count return to 0.\n- Taking: every pile card goes into your hand, and the top rank and run count return to 0.\nThe next seat then plays onto the pile as it now stands. After your turn, cards_left = cards in hand + cards in up_pile. Every play and pickup is announced to all; hands stay private.\n\nEND: the first seat whose cards_left reaches 0 wins at once and the remaining turns are skipped. If {max_rounds} rounds pass with nobody at 0, the seat with the fewest cards_left wins; seats tied for fewest share the result (a draw)."
}
```
````
