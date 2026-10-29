# 35 coder

- time: 2026-10-28T04:58:25+00:00 (244.4s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 de696727d8996967, reply sha256 ebfc28089850635e

## Sent

````
# Task: write the XColos game file for "3Up Shed (Equal Turns)"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

DECK. There are 30 cards: three copies each of ranks 1 to 9, plus three Clears (C). They are split into four stacks: Low (ranks 1-3, nine cards), Mid (ranks 4-6, nine cards), High (ranks 7-9, nine cards) and Clear (three cards). Everyone knows the deck's composition.

SETUP (once, before round 1).
S1. Shuffle the Low, Mid and High stacks separately.
S2. In seat order 1, 2, 3, each seat's hand receives the top 3 Low, the top 3 Mid and the top 3 High cards, plus 1 Clear. Each hand now holds 10 cards and every stack is empty.
S3. For each seat, the engine lists as up_offer every distinct set of 3 cards from that hand. Each set is written in ascending order, with C counting above 9, and the list is sorted ascending.
S4. All seats answer at the same moment, each picking one set. A missing or invalid answer takes the first set listed.
S5. The chosen 3 cards move from the hand to that seat's up_pile. Up piles are public; hands are secret.
S6. For each seat, set hand_count = 7, up_count = 3, cards_left = 10, out = false and picked_up = 0.
S7. The table starts with an empty pile: top_rank = 0, run_count = 0, round = 0, game_over = false.

ROUND (at most 20 rounds).
R1. Increase round by 1. Set lead = ((round - 1) mod 3) + 1.
R2. Three turns are taken, in this order: seat lead, then the next seat, then the next (after seat 3 comes seat 1). A seat with out = true skips its turn: it makes no choice and nothing about it changes.
R3. After the three turns: if at least one seat has out = true, set game_over = true.
R4. If game_over is true, or round = 20, the game ends.

TURN.
T1. Source: if the seat's hand is not empty, it plays from its hand. Otherwise it plays from its up_pile.
T2. Legal plays come from the source only:
- a rank r with r >= top_rank, played as 1, 2 or 3 copies, up to the number held;
- a single C, which is always legal.
When top_rank = 0, every card is legal. The engine lists the legal plays by ascending rank, then by number of copies, with C last. If no play is legal, the only option is PICK UP.
T3. The seat chooses one option. A missing or invalid answer takes the first option listed.
T4. Apply the choice:
- Rank play: the cards go onto the pile. If the previous top was also rank r, add the number of cards played to run_count; otherwise set run_count to that number. Set top_rank = r. If run_count >= 3, wipe the pile: remove it from the game and set top_rank = 0 and run_count = 0.
- C: remove the pile and the C from the game, and set top_rank = 0 and run_count = 0.
- PICK UP: the whole pile goes into the seat's hand, picked_up increases by 1, and top_rank = 0 and run_count = 0.
Every choice ends the turn; there are no extra plays.
T5. Recompute hand_count and up_count, and set cards_left = hand_count + up_count. If cards_left = 0, set out = true.

There are no draw pile and no face-down cards.

How the winner is decided: If the game ends because game_over is true, every seat with cards_left = 0 wins. If exactly one seat has 0 cards, it wins alone; if two or three do, the game is a draw. If round 20 ends with nobody out, the seat with the fewest cards_left wins, and a tie for fewest is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: 3Up Shed (Equal Turns) (3 to 3 players, best with 3)

Three players shed a 10-card hand onto a shared pile by matching or beating its top rank. They wipe the pile with three of a rank or a Clear, or pick it up when stuck. The first seats to run out of cards win, and every seat gets the same number of turns.

STATE (every item below must exist in the file):
  - each player: hand (list, starts []); only its owner sees it. Cards in this seat's secret hand (ranks 1-9 and C).
  - each player: up_offer (list, starts []); only its owner sees it. Every distinct 3-card set from the dealt hand, each written ascending with C above 9, and the list sorted ascending. Used only at setup.
  - each player: up_pile (list, starts []); everyone sees it. The seat's face-up cards. It is played from only once the hand is empty.
  - each player: hand_count (number, starts 0); everyone sees it. Number of cards in the hand.
  - each player: up_count (number, starts 0); everyone sees it. Number of cards in the up_pile.
  - each player: cards_left (number, starts 10); everyone sees it. hand_count + up_count. This is the score: lower is better.
  - each player: out (bool, starts False); everyone sees it. True once cards_left = 0. The seat then skips its turns.
  - each player: picked_up (number, starts 0); everyone sees it. How many times this seat has picked up the pile.
  - the table: low_stack (list, starts [1, 1, 1, 2, 2, 2, 3, 3, 3]); hidden from all players. The Low stack (ranks 1-3), shuffled at setup.
  - the table: mid_stack (list, starts [4, 4, 4, 5, 5, 5, 6, 6, 6]); hidden from all players. The Mid stack (ranks 4-6), shuffled at setup.
  - the table: high_stack (list, starts [7, 7, 7, 8, 8, 8, 9, 9, 9]); hidden from all players. The High stack (ranks 7-9), shuffled at setup.
  - the table: clear_stack (list, starts ['C', 'C', 'C']); hidden from all players. The Clear stack.
  - the table: pile (list, starts []); everyone sees it. Cards currently on the shared play pile.
  - the table: top_rank (number, starts 0); everyone sees it. Rank on top of the pile. 0 means the pile is empty.
  - the table: run_count (number, starts 0); everyone sees it. How many cards of top_rank have been played in a row on the pile.
  - the table: round (number, starts 0); everyone sees it. Current round number.
  - the table: lead (number, starts 1); everyone sees it. The seat that takes the first turn this round.
  - the table: game_over (bool, starts False); everyone sees it. Set true after a round in which at least one seat is out.
  - parameters, each kept as a table attribute: deck_size = 30, min_rank = 1, max_rank = 9, copies_per_rank = 3, clear_cards = 3, low_stack_size = 9, mid_stack_size = 9, high_stack_size = 9, clear_stack_size = 3, cards_dealt_per_stack = 3, clears_dealt_per_seat = 1, starting_hand_size = 10, up_pile_size = 3, hand_after_up = 7, max_copies_per_play = 3, run_wipe_threshold = 3, max_rounds = 20, empty_top_rank = 0, clear_sort_value = 10

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Shuffle low_stack, mid_stack and high_stack separately.
  2. In seat order 1, 2, 3, move the top 3 cards of low_stack, then the top 3 of mid_stack, then the top 3 of high_stack, then 1 card of clear_stack into that seat's hand. Each hand then holds 10 cards and every stack is empty.
  3. For each seat, set up_offer to every distinct set of 3 cards from its hand. Each set is written ascending with C counting as 10, and the list is sorted ascending.
  4. Poll all seats at once. Each picks one set from its own up_offer; a missing or invalid answer takes the first set listed.
  5. Move each seat's chosen 3 cards from hand to up_pile. Up piles are public; hands stay secret.
  6. For each seat set hand_count = 7, up_count = 3, cards_left = 10, out = false, picked_up = 0.
  7. Set pile = [], top_rank = 0, run_count = 0, round = 0, game_over = false.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round += 1; lead = ((round - 1) mod 3) + 1.
  2. [ask] each player in turn, starting at seat lead, then lead+1, then lead+2 (seat 3 is followed by seat 1); a seat with out = true is skipped answers: One option from the legal plays drawn from the source (hand if hand_count > 0, otherwise up_pile). An option is a rank r with r >= top_rank played as k copies, for k = 1 up to min(3, copies of r held); or a single C; or PICK UP only if no play is legal. Options are listed by ascending rank, then by copies, with C last. A missing or invalid answer takes the first option.. What happens: Right after each seat answers, its choice is applied as in the next step, so the next seat sees the updated pile.
  3. [update] the seat that just answered (applied after each turn). What happens: Rank play r x k: move k cards of rank r from the source to pile; if top_rank == r then run_count += k, else run_count = k; top_rank = r; if run_count >= 3, clear pile (removed from game), top_rank = 0, run_count = 0. C: remove the C from the source and clear pile (both removed from game), top_rank = 0, run_count = 0. PICK UP: append all of pile to hand, pile = [], picked_up += 1, top_rank = 0, run_count = 0. Then hand_count = len(hand), up_count = len(up_pile), cards_left = hand_count + up_count; if cards_left == 0 then out = true.
  4. [update] all players. What happens: After all three turns: if the number of seats with out = true is at least 1, set game_over = true.
  5. [check] all players. What happens: End the game if game_over == true or round == 20; otherwise start the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When setup is done, each seat has hand_count 7, up_count 3 and cards_left 10. Its 10 dealt cards were 3 Low (1-3), 3 Mid (4-6), 3 High (7-9) and 1 C.
  R2. When a seat picks its up set at setup, then exactly those 3 cards move from hand to the public up_pile, and an invalid or missing pick takes the first set of up_offer.
  R3. When a round starts, round increases by 1 and lead = ((round - 1) mod 3) + 1, so rounds 1, 2, 3, 4 are led by seats 1, 2, 3, 1.
  R4. When a seat has hand_count > 0, then its legal plays come only from its hand; when hand_count = 0, they come only from its up_pile.
  R5. When top_rank = t > 0, then a rank r is offered only if r >= t, as 1 to min(3, copies held) copies, and a single C is always offered if held.
  R6. When top_rank = 0, then every rank held in the source is offered (1 up to the copies held, at most 3) and C if held.
  R7. When no rank or C play is legal, then PICK UP is the only option.
  R8. When a seat plays k cards of rank r and top_rank was already r, then run_count increases by k; otherwise run_count = k. In both cases top_rank = r.
  R9. When run_count reaches 3 or more after a play, then pile is emptied out of the game, top_rank = 0 and run_count = 0.
  R10. When a seat plays a C, then the C and the whole pile leave the game, top_rank = 0 and run_count = 0.
  R11. When a seat picks up, then every card of pile goes into its hand, pile becomes empty, picked_up increases by 1, top_rank = 0 and run_count = 0.
  R12. When any turn ends, then hand_count, up_count and cards_left = hand_count + up_count are recomputed, and cards_left = 0 sets out = true.
  R13. When a seat has out = true, then it is skipped: it is asked nothing and its attributes do not change.
  R14. When a missing or invalid answer is given on a turn, then the first listed option is applied.
  R15. When a round's three turns end with at least one seat out, then game_over = true and the game ends after that round, so every seat has had the same number of turns.
  R16. When round 20 ends, then the game ends even if nobody is out.
  R17. When the game ends, then the seats with the lowest cards_left win, and seats tied at the lowest share the win.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Setup: choose your up set | asked: every seat, simultaneously | options: Every distinct 3-card set from that seat's own 10-card hand, each ascending with C above 9, the list sorted ascending (up_offer).
  - Turn: choose a play | asked: the seat whose turn it is, if out = false | options: From the source (hand if not empty, else up_pile): each rank r >= top_rank held, as 1, 2 or 3 copies up to the number held; 'C' if a C is held. When top_rank = 0, every held rank is offered. Sorted by rank, then by copies, with C last. If none of these exist: only 'PICK UP'.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: game_over == true or round >= 20
  - each player's standing: 0 - you.cards_left (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Fewest cards_left wins. If a seat went out, every seat with cards_left = 0 shares the win (one such seat wins alone; two or three is a draw). If round 20 ends with nobody out, the seat with the fewest cards_left wins, and seats tied for fewest share it (a draw).
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

- each player: `up_pile` (list, visible: public, starts []): The seat's face-up cards. It is played from only once the hand is empty.
- each player: `hand_count` (number, visible: public, starts 0): Number of cards in the hand.
- each player: `up_count` (number, visible: public, starts 0): Number of cards in the up_pile.
- each player: `cards_left` (number, visible: public, starts 10): hand_count + up_count. This is the score: lower is better.
- each player: `out` (bool, visible: public, starts False): True once cards_left = 0. The seat then skips its turns.
- each player: `picked_up` (number, visible: public, starts 0): How many times this seat has picked up the pile.
- the table: `pile` (list, visible: public, starts []): Cards currently on the shared play pile.
- the table: `top_rank` (number, visible: public, starts 0): Rank on top of the pile. 0 means the pile is empty.
- the table: `run_count` (number, visible: public, starts 0): How many cards of top_rank have been played in a row on the pile.
- the table: `round` (number, visible: public, starts 0): Current round number.
- the table: `game_over` (bool, visible: public, starts False): Set true after a round in which at least one seat is out.
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 30, min_rank = 1, max_rank = 9, copies_per_rank = 3, clear_cards = 3, low_stack_size = 9, mid_stack_size = 9, high_stack_size = 9, clear_stack_size = 3, cards_dealt_per_stack = 3, clears_dealt_per_seat = 1, starting_hand_size = 10, up_pile_size = 3, hand_after_up = 7, max_copies_per_play = 3, run_wipe_threshold = 3, max_rounds = 20, empty_top_rank = 0, clear_sort_value = 10
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

Make setup complete before any round starts.
1. After building up_offer, run S4 as one simultaneous poll of all seats, defaulting to the first listed set.
2. Apply S5: remove exactly those 3 cards from the hand and append them to up_pile, mapping the label 'C' back to the C card. The offer labels are strings like '1 3 C'.
3. Then apply S6: hand_count = len(hand), up_count = len(up_pile), cards_left = hand_count + up_count, out = false, picked_up = 0.
4. In each turn, choose the source per T1: the hand if hand_count > 0, otherwise up_pile. Build the options only from that source, with rank r >= top_rank as 1..min(3, copies held) copies, plus a single C if held, sorted by rank then copies, with C last.
5. Remove played cards from that same source.
6. Recompute hand_count, up_count and cards_left from the actual list lengths after every turn (T5).
7. Make sure the setup steps do not re-run or overwrite a given starting state, such as hands and up_piles a test provides.

````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "3up_shed_equal_turns",
    "name": "3Up Shed (Equal Turns)",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Shed a 10-card hand onto a shared pile by matching or beating its top rank; wipe it with three of a rank or a Clear, and every seat gets the same number of turns."
  },
  "statuses": [
    {
      "id": "playing",
      "acts": true,
      "initial": true
    },
    {
      "id": "finished",
      "acts": false
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
        "key": "up_offer",
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
        "initial": 0
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
        "key": "out",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "picked_up",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "up_choice",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      }
    ],
    "game": [
      {
        "key": "low_stack",
        "visible": "none",
        "type": "list",
        "initial": [1, 1, 1, 2, 2, 2, 3, 3, 3]
      },
      {
        "key": "mid_stack",
        "visible": "none",
        "type": "list",
        "initial": [4, 4, 4, 5, 5, 5, 6, 6, 6]
      },
      {
        "key": "high_stack",
        "visible": "none",
        "type": "list",
        "initial": [7, 7, 7, 8, 8, 8, 9, 9, 9]
      },
      {
        "key": "clear_stack",
        "visible": "none",
        "type": "list",
        "initial": ["C", "C", "C"]
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
        "initial": 1
      },
      {
        "key": "game_over",
        "visible": "public",
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
        "key": "low_stack_size",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "mid_stack_size",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "high_stack_size",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "clear_stack_size",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "cards_dealt_per_stack",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "clears_dealt_per_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "starting_hand_size",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "up_pile_size",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "hand_after_up",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "max_copies_per_play",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "run_wipe_threshold",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "max_rounds",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "empty_top_rank",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "clear_sort_value",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "rank_list",
        "visible": "none",
        "type": "list",
        "initial": [1, 2, 3, 4, 5, 6, 7, 8, 9]
      },
      {
        "key": "cur",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "play",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "play_rank",
        "visible": "none",
        "type": "number",
        "initial": 0
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
        "initial": false
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "shuffle the stacks",
      "do": [
        {
          "set": {
            "key": "low_stack",
            "value": {
              "calc": "[x[1] for x in sorted([[uniform(0, 1), c] for c in low_stack])]"
            }
          }
        },
        {
          "set": {
            "key": "mid_stack",
            "value": {
              "calc": "[x[1] for x in sorted([[uniform(0, 1), c] for c in mid_stack])]"
            }
          }
        },
        {
          "set": {
            "key": "high_stack",
            "value": {
              "calc": "[x[1] for x in sorted([[uniform(0, 1), c] for c in high_stack])]"
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
            "player": 1,
            "key": "hand",
            "value": {
              "calc": "[low_stack[i - 1] for i in rank_list if i <= cards_dealt_per_stack] + [mid_stack[i - 1] for i in rank_list if i <= cards_dealt_per_stack] + [high_stack[i - 1] for i in rank_list if i <= cards_dealt_per_stack] + [clear_stack[i - 1] for i in rank_list if i <= clears_dealt_per_seat]"
            }
          }
        },
        {
          "set": {
            "key": "low_stack",
            "value": {
              "calc": "[low_stack[i] for i in rank_list if i >= cards_dealt_per_stack and i < len(low_stack)]"
            }
          }
        },
        {
          "set": {
            "key": "mid_stack",
            "value": {
              "calc": "[mid_stack[i] for i in rank_list if i >= cards_dealt_per_stack and i < len(mid_stack)]"
            }
          }
        },
        {
          "set": {
            "key": "high_stack",
            "value": {
              "calc": "[high_stack[i] for i in rank_list if i >= cards_dealt_per_stack and i < len(high_stack)]"
            }
          }
        },
        {
          "set": {
            "key": "clear_stack",
            "value": {
              "calc": "[clear_stack[i] for i in rank_list if i >= clears_dealt_per_seat and i < len(clear_stack)]"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "hand",
            "value": {
              "calc": "[low_stack[i - 1] for i in rank_list if i <= cards_dealt_per_stack] + [mid_stack[i - 1] for i in rank_list if i <= cards_dealt_per_stack] + [high_stack[i - 1] for i in rank_list if i <= cards_dealt_per_stack] + [clear_stack[i - 1] for i in rank_list if i <= clears_dealt_per_seat]"
            }
          }
        },
        {
          "set": {
            "key": "low_stack",
            "value": {
              "calc": "[low_stack[i] for i in rank_list if i >= cards_dealt_per_stack and i < len(low_stack)]"
            }
          }
        },
        {
          "set": {
            "key": "mid_stack",
            "value": {
              "calc": "[mid_stack[i] for i in rank_list if i >= cards_dealt_per_stack and i < len(mid_stack)]"
            }
          }
        },
        {
          "set": {
            "key": "high_stack",
            "value": {
              "calc": "[high_stack[i] for i in rank_list if i >= cards_dealt_per_stack and i < len(high_stack)]"
            }
          }
        },
        {
          "set": {
            "key": "clear_stack",
            "value": {
              "calc": "[clear_stack[i] for i in rank_list if i >= clears_dealt_per_seat and i < len(clear_stack)]"
            }
          }
        },
        {
          "set": {
            "player": 3,
            "key": "hand",
            "value": {
              "calc": "[low_stack[i - 1] for i in rank_list if i <= cards_dealt_per_stack] + [mid_stack[i - 1] for i in rank_list if i <= cards_dealt_per_stack] + [high_stack[i - 1] for i in rank_list if i <= cards_dealt_per_stack] + [clear_stack[i - 1] for i in rank_list if i <= clears_dealt_per_seat]"
            }
          }
        },
        {
          "set": {
            "key": "low_stack",
            "value": {
              "calc": "[low_stack[i] for i in rank_list if i >= cards_dealt_per_stack and i < len(low_stack)]"
            }
          }
        },
        {
          "set": {
            "key": "mid_stack",
            "value": {
              "calc": "[mid_stack[i] for i in rank_list if i >= cards_dealt_per_stack and i < len(mid_stack)]"
            }
          }
        },
        {
          "set": {
            "key": "high_stack",
            "value": {
              "calc": "[high_stack[i] for i in rank_list if i >= cards_dealt_per_stack and i < len(high_stack)]"
            }
          }
        },
        {
          "set": {
            "key": "clear_stack",
            "value": {
              "calc": "[clear_stack[i] for i in rank_list if i >= clears_dealt_per_seat and i < len(clear_stack)]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "list the up sets",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "up_offer",
            "value": {
              "calc": "['0123456789C'[a] + ' ' + '0123456789C'[b] + ' ' + '0123456789C'[c] for a in rank_list + [clear_sort_value] for b in rank_list + [clear_sort_value] for c in rank_list + [clear_sort_value] if a <= b and b <= c and count((clear_sort_value if h == 'C' else h) == a for h in you.hand) >= count(x == a for x in [a, b, c]) and count((clear_sort_value if h == 'C' else h) == b for h in you.hand) >= count(x == b for x in [a, b, c]) and count((clear_sort_value if h == 'C' else h) == c for h in you.hand) >= count(x == c for x in [a, b, c])]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "starting counts and the empty pile",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "hand_count",
            "value": {
              "calc": "hand_after_up"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "up_count",
            "value": {
              "calc": "up_pile_size"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "cards_left",
            "value": {
              "calc": "starting_hand_size"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "out",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "picked_up",
            "value": 0
          }
        },
        {
          "set": {
            "key": "pile",
            "value": []
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
        },
        {
          "set": {
            "key": "round",
            "value": 0
          }
        },
        {
          "set": {
            "key": "game_over",
            "value": false
          }
        }
      ]
    },
    {
      "use": "sync",
      "label": "the deal",
      "mode": "self",
      "to": "all",
      "text": "You were dealt:"
    }
  ],
  "steps": [
    {
      "use": "poll",
      "phase": "setup",
      "label": "choose your up set",
      "when": {
        "calc": "any(len(p.up_offer) > 0 and len(p.up_pile) == 0 for p in players)"
      },
      "to": {
        "where": "len(you.up_offer) > 0 and len(you.up_pile) == 0"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "up_offer"
        }
      },
      "store": "up_choice",
      "text": "Choose the 3 cards that go face up into your up pile (C is a Clear). Everyone will see them; you play them only once your hand is empty. A missing or invalid choice takes the first set listed."
    },
    {
      "use": "update",
      "phase": "setup",
      "label": "place the up piles",
      "when": {
        "calc": "any(len(p.up_offer) > 0 for p in players)"
      },
      "do": [
        {
          "set": {
            "players": {
              "where": "len(you.up_offer) > 0 and len(you.up_pile) > 0"
            },
            "key": "up_offer",
            "value": []
          }
        },
        {
          "set": {
            "players": {
              "where": "len(you.up_offer) > 0"
            },
            "key": "up_choice",
            "value": {
              "calc": "you.up_choice if you.up_choice in you.up_offer else you.up_offer[0]"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "len(you.up_offer) > 0"
            },
            "key": "up_pile",
            "value": {
              "calc": "'C' if you.up_choice[0] == 'C' else int(you.up_choice[0])"
            }
          }
        },
        {
          "remove": {
            "players": {
              "where": "len(you.up_offer) > 0"
            },
            "key": "hand",
            "value": {
              "calc": "'C' if you.up_choice[0] == 'C' else int(you.up_choice[0])"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "len(you.up_offer) > 0"
            },
            "key": "up_pile",
            "value": {
              "calc": "'C' if you.up_choice[2] == 'C' else int(you.up_choice[2])"
            }
          }
        },
        {
          "remove": {
            "players": {
              "where": "len(you.up_offer) > 0"
            },
            "key": "hand",
            "value": {
              "calc": "'C' if you.up_choice[2] == 'C' else int(you.up_choice[2])"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "len(you.up_offer) > 0"
            },
            "key": "up_pile",
            "value": {
              "calc": "'C' if you.up_choice[4] == 'C' else int(you.up_choice[4])"
            }
          }
        },
        {
          "remove": {
            "players": {
              "where": "len(you.up_offer) > 0"
            },
            "key": "hand",
            "value": {
              "calc": "'C' if you.up_choice[4] == 'C' else int(you.up_choice[4])"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "len(you.up_offer) > 0"
            },
            "key": "hand_count",
            "value": {
              "calc": "len(you.hand)"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "len(you.up_offer) > 0"
            },
            "key": "up_count",
            "value": {
              "calc": "len(you.up_pile)"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "len(you.up_offer) > 0"
            },
            "key": "cards_left",
            "value": {
              "calc": "you.hand_count + you.up_count"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "len(you.up_offer) > 0"
            },
            "key": "out",
            "value": false
          }
        },
        {
          "set": {
            "players": {
              "where": "len(you.up_offer) > 0"
            },
            "key": "picked_up",
            "value": 0
          }
        },
        {
          "set": {
            "players": {
              "where": "len(you.up_offer) > 0"
            },
            "key": "up_offer",
            "value": []
          }
        }
      ],
      "text": "The up piles are face up. Seat 1: {players[0].up_pile}. Seat 2: {players[1].up_pile}. Seat 3: {players[2].up_pile}."
    },
    {
      "use": "update",
      "phase": "round",
      "label": "a new round",
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
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "not you.out"
            },
            "key": "offer",
            "value": {
              "calc": "['0123456789'[r] + 'x' + '0123456789'[k] for r in rank_list for k in rank_list if k <= max_copies_per_play and r >= top_rank and k <= count(c == r for c in (you.hand if len(you.hand) > 0 else you.up_pile))] + (['C'] if 'C' in (you.hand if len(you.hand) > 0 else you.up_pile) else [])"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "not you.out and len(you.offer) == 0"
            },
            "key": "offer",
            "value": [
              "PICK UP"
            ]
          }
        }
      ],
      "text": "Round {round} begins. Seat {lead} takes the first turn."
    },
    {
      "use": "ask",
      "phase": "turns",
      "label": "first turn",
      "to": {
        "where": "you.seat == lead and not you.out"
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
              "key": "cur",
              "value": "$seat"
            }
          },
          {
            "set": {
              "key": "play",
              "value": {
                "calc": "$answer if $answer in players[cur - 1].offer else players[cur - 1].offer[0]"
              },
              "text": "Seat {seat} plays {value}."
            }
          },
          {
            "set": {
              "key": "play_rank",
              "value": {
                "calc": "0 if play in ['C', 'PICK UP'] else int(play[0])"
              }
            }
          },
          {
            "set": {
              "key": "play_k",
              "value": {
                "calc": "0 if play in ['C', 'PICK UP'] else int(play[2])"
              }
            }
          },
          {
            "set": {
              "key": "from_hand",
              "value": {
                "calc": "len(players[cur - 1].hand) > 0"
              }
            }
          },
          {
            "remove": {
              "player": {
                "calc": "cur"
              },
              "key": "hand",
              "value": {
                "calc": "play_rank"
              },
              "if": {
                "calc": "play_rank > 0 and from_hand and play_k >= 1"
              }
            }
          },
          {
            "remove": {
              "player": {
                "calc": "cur"
              },
              "key": "hand",
              "value": {
                "calc": "play_rank"
              },
              "if": {
                "calc": "play_rank > 0 and from_hand and play_k >= 2"
              }
            }
          },
          {
            "remove": {
              "player": {
                "calc": "cur"
              },
              "key": "hand",
              "value": {
                "calc": "play_rank"
              },
              "if": {
                "calc": "play_rank > 0 and from_hand and play_k >= 3"
              }
            }
          },
          {
            "remove": {
              "player": {
                "calc": "cur"
              },
              "key": "up_pile",
              "value": {
                "calc": "play_rank"
              },
              "if": {
                "calc": "play_rank > 0 and not from_hand and play_k >= 1"
              }
            }
          },
          {
            "remove": {
              "player": {
                "calc": "cur"
              },
              "key": "up_pile",
              "value": {
                "calc": "play_rank"
              },
              "if": {
                "calc": "play_rank > 0 and not from_hand and play_k >= 2"
              }
            }
          },
          {
            "remove": {
              "player": {
                "calc": "cur"
              },
              "key": "up_pile",
              "value": {
                "calc": "play_rank"
              },
              "if": {
                "calc": "play_rank > 0 and not from_hand and play_k >= 3"
              }
            }
          },
          {
            "remove": {
              "player": {
                "calc": "cur"
              },
              "key": "hand",
              "value": "C",
              "if": {
                "calc": "play == 'C' and from_hand"
              }
            }
          },
          {
            "remove": {
              "player": {
                "calc": "cur"
              },
              "key": "up_pile",
              "value": "C",
              "if": {
                "calc": "play == 'C' and not from_hand"
              }
            }
          },
          {
            "set": {
              "key": "pile",
              "value": {
                "calc": "pile + [play_rank for i in rank_list if i <= play_k]"
              },
              "if": {
                "calc": "play_rank > 0"
              }
            }
          },
          {
            "set": {
              "key": "run_count",
              "value": {
                "calc": "run_count + play_k if top_rank == play_rank else play_k"
              },
              "if": {
                "calc": "play_rank > 0"
              }
            }
          },
          {
            "set": {
              "key": "top_rank",
              "value": {
                "calc": "play_rank"
              },
              "if": {
                "calc": "play_rank > 0"
              }
            }
          },
          {
            "set": {
              "key": "pile",
              "value": [],
              "if": {
                "calc": "play_rank > 0 and run_count >= run_wipe_threshold"
              },
              "text": "Three of a rank in a row: the pile is wiped out of the game."
            }
          },
          {
            "set": {
              "key": "top_rank",
              "value": {
                "calc": "empty_top_rank"
              },
              "if": {
                "calc": "play_rank > 0 and run_count >= run_wipe_threshold"
              }
            }
          },
          {
            "set": {
              "key": "run_count",
              "value": 0,
              "if": {
                "calc": "play_rank > 0 and run_count >= run_wipe_threshold"
              }
            }
          },
          {
            "set": {
              "player": {
                "calc": "cur"
              },
              "key": "hand",
              "value": {
                "calc": "players[cur - 1].hand + pile"
              },
              "if": {
                "calc": "play == 'PICK UP'"
              },
              "text": "Seat {seat} picks up the pile."
            }
          },
          {
            "adjust": {
              "player": {
                "calc": "cur"
              },
              "key": "picked_up",
              "value": 1,
              "if": {
                "calc": "play == 'PICK UP'"
              }
            }
          },
          {
            "set": {
              "key": "pile",
              "value": [],
              "if": {
                "calc": "play in ['C', 'PICK UP']"
              }
            }
          },
          {
            "set": {
              "key": "top_rank",
              "value": {
                "calc": "empty_top_rank"
              },
              "if": {
                "calc": "play in ['C', 'PICK UP']"
              }
            }
          },
          {
            "set": {
              "key": "run_count",
              "value": 0,
              "if": {
                "calc": "play in ['C', 'PICK UP']"
              }
            }
          },
          {
            "set": {
              "player": {
                "calc": "cur"
              },
              "key": "hand_count",
              "value": {
                "calc": "len(players[cur - 1].hand)"
              }
            }
          },
          {
            "set": {
              "player": {
                "calc": "cur"
              },
              "key": "up_count",
              "value": {
                "calc": "len(players[cur - 1].up_pile)"
              }
            }
          },
          {
            "set": {
              "player": {
                "calc": "cur"
              },
              "key": "cards_left",
              "value": {
                "calc": "players[cur - 1].hand_count + players[cur - 1].up_count"
              }
            }
          },
          {
            "set": {
              "player": {
                "calc": "cur"
              },
              "key": "out",
              "value": true,
              "if": {
                "calc": "players[cur - 1].cards_left == 0"
              }
            }
          },
          {
            "set_status": {
              "player": {
                "calc": "cur"
              },
              "to": "finished",
              "if": {
                "calc": "players[cur - 1].out"
              },
              "text": "Seat {player} has no cards left and is out."
            }
          },
          {
            "set": {
              "players": {
                "where": "not you.out"
              },
              "key": "offer",
              "value": {
                "calc": "['0123456789'[r] + 'x' + '0123456789'[k] for r in rank_list for k in rank_list if k <= max_copies_per_play and r >= top_rank and k <= count(c == r for c in (you.hand if len(you.hand) > 0 else you.up_pile))] + (['C'] if 'C' in (you.hand if len(you.hand) > 0 else you.up_pile) else [])"
              }
            }
          },
          {
            "set": {
              "players": {
                "where": "not you.out and len(you.offer) == 0"
              },
              "key": "offer",
              "value": [
                "PICK UP"
              ]
            }
          }
        ]
      },
      "text": "Your turn. Top rank {top_rank} (0 means the pile is empty), run {run_count}, pile {pile}. Choose a play: 'RxK' plays K cards of rank R, 'C' plays a Clear, 'PICK UP' takes the whole pile into your hand."
    },
    {
      "use": "ask",
      "phase": "turns",
      "label": "second turn",
      "to": {
        "where": "you.seat == (lead % len(players)) + 1 and not you.out"
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
              "key": "cur",
              "value": "$seat"
            }
          },
          {
            "set": {
              "key": "play",
              "value": {
                "calc": "$answer if $answer in players[cur - 1].offer else players[cur - 1].offer[0]"
              },
              "text": "Seat {seat} plays {value}."
            }
          },
          {
            "set": {
              "key": "play_rank",
              "value": {
                "calc": "0 if play in ['C', 'PICK UP'] else int(play[0])"
              }
            }
          },
          {
            "set": {
              "key": "play_k",
              "value": {
                "calc": "0 if play in ['C', 'PICK UP'] else int(play[2])"
              }
            }
          },
          {
            "set": {
              "key": "from_hand",
              "value": {
                "calc": "len(players[cur - 1].hand) > 0"
              }
            }
          },
          {
            "remove": {
              "player": {
                "calc": "cur"
              },
              "key": "hand",
              "value": {
                "calc": "play_rank"
              },
              "if": {
                "calc": "play_rank > 0 and from_hand and play_k >= 1"
              }
            }
          },
          {
            "remove": {
              "player": {
                "calc": "cur"
              },
              "key": "hand",
              "value": {
                "calc": "play_rank"
              },
              "if": {
                "calc": "play_rank > 0 and from_hand and play_k >= 2"
              }
            }
          },
          {
            "remove": {
              "player": {
                "calc": "cur"
              },
              "key": "hand",
              "value": {
                "calc": "play_rank"
              },
              "if": {
                "calc": "play_rank > 0 and from_hand and play_k >= 3"
              }
            }
          },
          {
            "remove": {
              "player": {
                "calc": "cur"
              },
              "key": "up_pile",
              "value": {
                "calc": "play_rank"
              },
              "if": {
                "calc": "play_rank > 0 and not from_hand and play_k >= 1"
              }
            }
          },
          {
            "remove": {
              "player": {
                "calc": "cur"
              },
              "key": "up_pile",
              "value": {
                "calc": "play_rank"
              },
              "if": {
                "calc": "play_rank > 0 and not from_hand and play_k >= 2"
              }
            }
          },
          {
            "remove": {
              "player": {
                "calc": "cur"
              },
              "key": "up_pile",
              "value": {
                "calc": "play_rank"
              },
              "if": {
                "calc": "play_rank > 0 and not from_hand and play_k >= 3"
              }
            }
          },
          {
            "remove": {
              "player": {
                "calc": "cur"
              },
              "key": "hand",
              "value": "C",
              "if": {
                "calc": "play == 'C' and from_hand"
              }
            }
          },
          {
            "remove": {
              "player": {
                "calc": "cur"
              },
              "key": "up_pile",
              "value": "C",
              "if": {
                "calc": "play == 'C' and not from_hand"
              }
            }
          },
          {
            "set": {
              "key": "pile",
              "value": {
                "calc": "pile + [play_rank for i in rank_list if i <= play_k]"
              },
              "if": {
                "calc": "play_rank > 0"
              }
            }
          },
          {
            "set": {
              "key": "run_count",
              "value": {
                "calc": "run_count + play_k if top_rank == play_rank else play_k"
              },
              "if": {
                "calc": "play_rank > 0"
              }
            }
          },
          {
            "set": {
              "key": "top_rank",
              "value": {
                "calc": "play_rank"
              },
              "if": {
                "calc": "play_rank > 0"
              }
            }
          },
          {
            "set": {
              "key": "pile",
              "value": [],
              "if": {
                "calc": "play_rank > 0 and run_count >= run_wipe_threshold"
              },
              "text": "Three of a rank in a row: the pile is wiped out of the game."
            }
          },
          {
            "set": {
              "key": "top_rank",
              "value": {
                "calc": "empty_top_rank"
              },
              "if": {
                "calc": "play_rank > 0 and run_count >= run_wipe_threshold"
              }
            }
          },
          {
            "set": {
              "key": "run_count",
              "value": 0,
              "if": {
                "calc": "play_rank > 0 and run_count >= run_wipe_threshold"
              }
            }
          },
          {
            "set": {
              "player": {
                "calc": "cur"
              },
              "key": "hand",
              "value": {
                "calc": "players[cur - 1].hand + pile"
              },
              "if": {
                "calc": "play == 'PICK UP'"
              },
              "text": "Seat {seat} picks up the pile."
            }
          },
          {
            "adjust": {
              "player": {
                "calc": "cur"
              },
              "key": "picked_up",
              "value": 1,
              "if": {
                "calc": "play == 'PICK UP'"
              }
            }
          },
          {
            "set": {
              "key": "pile",
              "value": [],
              "if": {
                "calc": "play in ['C', 'PICK UP']"
              }
            }
          },
          {
            "set": {
              "key": "top_rank",
              "value": {
                "calc": "empty_top_rank"
              },
              "if": {
                "calc": "play in ['C', 'PICK UP']"
              }
            }
          },
          {
            "set": {
              "key": "run_count",
              "value": 0,
              "if": {
                "calc": "play in ['C', 'PICK UP']"
              }
            }
          },
          {
            "set": {
              "player": {
                "calc": "cur"
              },
              "key": "hand_count",
              "value": {
                "calc": "len(players[cur - 1].hand)"
              }
            }
          },
          {
            "set": {
              "player": {
                "calc": "cur"
              },
              "key": "up_count",
              "value": {
                "calc": "len(players[cur - 1].up_pile)"
              }
            }
          },
          {
            "set": {
              "player": {
                "calc": "cur"
              },
              "key": "cards_left",
              "value": {
                "calc": "players[cur - 1].hand_count + players[cur - 1].up_count"
              }
            }
          },
          {
            "set": {
              "player": {
                "calc": "cur"
              },
              "key": "out",
              "value": true,
              "if": {
                "calc": "players[cur - 1].cards_left == 0"
              }
            }
          },
          {
            "set_status": {
              "player": {
                "calc": "cur"
              },
              "to": "finished",
              "if": {
                "calc": "players[cur - 1].out"
              },
              "text": "Seat {player} has no cards left and is out."
            }
          },
          {
            "set": {
              "players": {
                "where": "not you.out"
              },
              "key": "offer",
              "value": {
                "calc": "['0123456789'[r] + 'x' + '0123456789'[k] for r in rank_list for k in rank_list if k <= max_copies_per_play and r >= top_rank and k <= count(c == r for c in (you.hand if len(you.hand) > 0 else you.up_pile))] + (['C'] if 'C' in (you.hand if len(you.hand) > 0 else you.up_pile) else [])"
              }
            }
          },
          {
            "set": {
              "players": {
                "where": "not you.out and len(you.offer) == 0"
              },
              "key": "offer",
              "value": [
                "PICK UP"
              ]
            }
          }
        ]
      },
      "text": "Your turn. Top rank {top_rank} (0 means the pile is empty), run {run_count}, pile {pile}. Choose a play: 'RxK' plays K cards of rank R, 'C' plays a Clear, 'PICK UP' takes the whole pile into your hand."
    },
    {
      "use": "ask",
      "phase": "turns",
      "label": "third turn",
      "to": {
        "where": "you.seat == ((lead + 1) % len(players)) + 1 and not you.out"
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
              "key": "cur",
              "value": "$seat"
            }
          },
          {
            "set": {
              "key": "play",
              "value": {
                "calc": "$answer if $answer in players[cur - 1].offer else players[cur - 1].offer[0]"
              },
              "text": "Seat {seat} plays {value}."
            }
          },
          {
            "set": {
              "key": "play_rank",
              "value": {
                "calc": "0 if play in ['C', 'PICK UP'] else int(play[0])"
              }
            }
          },
          {
            "set": {
              "key": "play_k",
              "value": {
                "calc": "0 if play in ['C', 'PICK UP'] else int(play[2])"
              }
            }
          },
          {
            "set": {
              "key": "from_hand",
              "value": {
                "calc": "len(players[cur - 1].hand) > 0"
              }
            }
          },
          {
            "remove": {
              "player": {
                "calc": "cur"
              },
              "key": "hand",
              "value": {
                "calc": "play_rank"
              },
              "if": {
                "calc": "play_rank > 0 and from_hand and play_k >= 1"
              }
            }
          },
          {
            "remove": {
              "player": {
                "calc": "cur"
              },
              "key": "hand",
              "value": {
                "calc": "play_rank"
              },
              "if": {
                "calc": "play_rank > 0 and from_hand and play_k >= 2"
              }
            }
          },
          {
            "remove": {
              "player": {
                "calc": "cur"
              },
              "key": "hand",
              "value": {
                "calc": "play_rank"
              },
              "if": {
                "calc": "play_rank > 0 and from_hand and play_k >= 3"
              }
            }
          },
          {
            "remove": {
              "player": {
                "calc": "cur"
              },
              "key": "up_pile",
              "value": {
                "calc": "play_rank"
              },
              "if": {
                "calc": "play_rank > 0 and not from_hand and play_k >= 1"
              }
            }
          },
          {
            "remove": {
              "player": {
                "calc": "cur"
              },
              "key": "up_pile",
              "value": {
                "calc": "play_rank"
              },
              "if": {
                "calc": "play_rank > 0 and not from_hand and play_k >= 2"
              }
            }
          },
          {
            "remove": {
              "player": {
                "calc": "cur"
              },
              "key": "up_pile",
              "value": {
                "calc": "play_rank"
              },
              "if": {
                "calc": "play_rank > 0 and not from_hand and play_k >= 3"
              }
            }
          },
          {
            "remove": {
              "player": {
                "calc": "cur"
              },
              "key": "hand",
              "value": "C",
              "if": {
                "calc": "play == 'C' and from_hand"
              }
            }
          },
          {
            "remove": {
              "player": {
                "calc": "cur"
              },
              "key": "up_pile",
              "value": "C",
              "if": {
                "calc": "play == 'C' and not from_hand"
              }
            }
          },
          {
            "set": {
              "key": "pile",
              "value": {
                "calc": "pile + [play_rank for i in rank_list if i <= play_k]"
              },
              "if": {
                "calc": "play_rank > 0"
              }
            }
          },
          {
            "set": {
              "key": "run_count",
              "value": {
                "calc": "run_count + play_k if top_rank == play_rank else play_k"
              },
              "if": {
                "calc": "play_rank > 0"
              }
            }
          },
          {
            "set": {
              "key": "top_rank",
              "value": {
                "calc": "play_rank"
              },
              "if": {
                "calc": "play_rank > 0"
              }
            }
          },
          {
            "set": {
              "key": "pile",
              "value": [],
              "if": {
                "calc": "play_rank > 0 and run_count >= run_wipe_threshold"
              },
              "text": "Three of a rank in a row: the pile is wiped out of the game."
            }
          },
          {
            "set": {
              "key": "top_rank",
              "value": {
                "calc": "empty_top_rank"
              },
              "if": {
                "calc": "play_rank > 0 and run_count >= run_wipe_threshold"
              }
            }
          },
          {
            "set": {
              "key": "run_count",
              "value": 0,
              "if": {
                "calc": "play_rank > 0 and run_count >= run_wipe_threshold"
              }
            }
          },
          {
            "set": {
              "player": {
                "calc": "cur"
              },
              "key": "hand",
              "value": {
                "calc": "players[cur - 1].hand + pile"
              },
              "if": {
                "calc": "play == 'PICK UP'"
              },
              "text": "Seat {seat} picks up the pile."
            }
          },
          {
            "adjust": {
              "player": {
                "calc": "cur"
              },
              "key": "picked_up",
              "value": 1,
              "if": {
                "calc": "play == 'PICK UP'"
              }
            }
          },
          {
            "set": {
              "key": "pile",
              "value": [],
              "if": {
                "calc": "play in ['C', 'PICK UP']"
              }
            }
          },
          {
            "set": {
              "key": "top_rank",
              "value": {
                "calc": "empty_top_rank"
              },
              "if": {
                "calc": "play in ['C', 'PICK UP']"
              }
            }
          },
          {
            "set": {
              "key": "run_count",
              "value": 0,
              "if": {
                "calc": "play in ['C', 'PICK UP']"
              }
            }
          },
          {
            "set": {
              "player": {
                "calc": "cur"
              },
              "key": "hand_count",
              "value": {
                "calc": "len(players[cur - 1].hand)"
              }
            }
          },
          {
            "set": {
              "player": {
                "calc": "cur"
              },
              "key": "up_count",
              "value": {
                "calc": "len(players[cur - 1].up_pile)"
              }
            }
          },
          {
            "set": {
              "player": {
                "calc": "cur"
              },
              "key": "cards_left",
              "value": {
                "calc": "players[cur - 1].hand_count + players[cur - 1].up_count"
              }
            }
          },
          {
            "set": {
              "player": {
                "calc": "cur"
              },
              "key": "out",
              "value": true,
              "if": {
                "calc": "players[cur - 1].cards_left == 0"
              }
            }
          },
          {
            "set_status": {
              "player": {
                "calc": "cur"
              },
              "to": "finished",
              "if": {
                "calc": "players[cur - 1].out"
              },
              "text": "Seat {player} has no cards left and is out."
            }
          },
          {
            "set": {
              "players": {
                "where": "not you.out"
              },
              "key": "offer",
              "value": {
                "calc": "['0123456789'[r] + 'x' + '0123456789'[k] for r in rank_list for k in rank_list if k <= max_copies_per_play and r >= top_rank and k <= count(c == r for c in (you.hand if len(you.hand) > 0 else you.up_pile))] + (['C'] if 'C' in (you.hand if len(you.hand) > 0 else you.up_pile) else [])"
              }
            }
          },
          {
            "set": {
              "players": {
                "where": "not you.out and len(you.offer) == 0"
              },
              "key": "offer",
              "value": [
                "PICK UP"
              ]
            }
          }
        ]
      },
      "text": "Your turn. Top rank {top_rank} (0 means the pile is empty), run {run_count}, pile {pile}. Choose a play: 'RxK' plays K cards of rank R, 'C' plays a Clear, 'PICK UP' takes the whole pile into your hand."
    },
    {
      "use": "update",
      "phase": "round",
      "label": "after the three turns",
      "do": [
        {
          "set": {
            "key": "game_over",
            "value": true,
            "if": {
              "calc": "count(p.out for p in players) >= 1"
            }
          }
        }
      ],
      "text": "End of round {round}. Cards left: Seat 1 {players[0].cards_left}, Seat 2 {players[1].cards_left}, Seat 3 {players[2].cards_left}."
    },
    {
      "use": "sync",
      "phase": "round",
      "label": "the standings",
      "mode": "self",
      "to": "all",
      "text": "Where you stand:"
    },
    {
      "use": "check",
      "phase": "round",
      "label": "is it over",
      "when": {
        "calc": "game_over or round >= max_rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "game_over or round >= max_rounds"
      },
      "rank_by": "0 - you.cards_left",
      "text": "Winner: {result}. Cards left: Seat 1 {players[0].cards_left}, Seat 2 {players[1].cards_left}, Seat 3 {players[2].cards_left} after round {round}."
    }
  },
  "limits": {
    "rounds": 20,
    "rounds_max": 20,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "DECK. There are {deck_size} cards: {copies_per_rank} copies each of ranks {min_rank} to {max_rank}, plus {clear_cards} Clears (C). They are split into four stacks: Low (ranks 1-3, {low_stack_size} cards), Mid (ranks 4-6, {mid_stack_size} cards), High (ranks 7-9, {high_stack_size} cards) and Clear ({clear_stack_size} cards). Everyone knows the deck's composition.\n\nSETUP. The Low, Mid and High stacks are shuffled separately. In seat order 1, 2, 3, each seat's hand receives the top {cards_dealt_per_stack} Low, the top {cards_dealt_per_stack} Mid and the top {cards_dealt_per_stack} High cards, plus {clears_dealt_per_seat} Clear, so each hand holds {starting_hand_size} cards and every stack is empty. Each seat is offered every distinct set of {up_pile_size} cards from its hand (written ascending, C counting above 9, the list sorted ascending). All seats answer at the same moment, each picking one set; a missing or invalid answer takes the first set listed. The chosen cards move from the hand to that seat's up pile. Up piles are public; hands are secret. Each seat then has {hand_after_up} cards in hand, {up_pile_size} in its up pile and {starting_hand_size} cards left. The pile starts empty (top rank {empty_top_rank}).\n\nROUND (at most {max_rounds} rounds). The round number increases by 1 and the lead seat is ((round - 1) mod 3) + 1, so rounds 1, 2, 3, 4 are led by seats 1, 2, 3, 1. Three turns are taken: the lead seat, then the next seat, then the next (after seat 3 comes seat 1). A seat that is out skips its turn: it makes no choice and nothing about it changes. After the three turns, if at least one seat is out, the game is over. The game ends after that round, or after round {max_rounds}; otherwise the next round starts.\n\nTURN. Source: if your hand is not empty you play from your hand; otherwise you play from your up pile. Legal plays come from the source only: a rank r with r at least the top rank, played as 1, 2 or up to {max_copies_per_play} copies, up to the number you hold (offered as 'rxk', e.g. '5x2' is two 5s); or a single C, which is always legal. When the top rank is {empty_top_rank} (empty pile), every card is legal. Options are listed by ascending rank, then by number of copies, with C last. If no play is legal, the only option is PICK UP. A missing or invalid answer takes the first option listed.\n- Rank play: the cards go onto the pile. If the previous top was also rank r, the cards played are added to the run count; otherwise the run count becomes the number played. The top rank becomes r. If the run count reaches {run_wipe_threshold} or more, the pile is wiped out of the game and the top rank and run count go back to 0; if not, the pile stays.\n- C: the C and the whole pile are removed from the game, and the top rank and run count go back to 0.\n- PICK UP: the whole pile goes into your hand, your picked-up count increases by 1, and the top rank and run count go back to 0.\nEvery choice ends the turn; there are no extra plays. Afterwards your hand count, up count and cards left (hand + up pile) are recomputed; if you have 0 cards left you are out and skip all later turns. There is no draw pile and there are no face-down cards.\n\nWINNING. Fewest cards left wins. If the game ends because a seat went out, every seat with 0 cards left wins (one such seat wins alone; two or three share the win as a draw). If round {max_rounds} ends with nobody out, the seat with the fewest cards left wins, and seats tied for fewest share the win."
}
```
````
