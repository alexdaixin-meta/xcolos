# 12 coder

- time: 2026-10-27T17:40:39+00:00 (167.6s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 916220f34373fc71, reply sha256 274c9be71b5a527f

## Sent

````
# Task: write the XColos game file for "Blind Scuttle"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 2; set `meta.players` to {"min": 2, "max": 2, "suggested": 2} (the suggested size is the one the game plays best at).

DECK: 48 cards.
- 40 point cards: ranks 1 to 10, four copies of each, no suits.
- 4 Jacks and 4 Kings.
Shuffle the deck.

BANDS: Every point card has a band. Low is ranks 1-4, Mid is ranks 5-7, High is ranks 8-10.

SETUP:
- Randomly pick the First player.
- Deal 6 cards to each player. Hands are private.
- The other 36 cards are the face-down draw pile.
- The scrap pile is face up and fully public.
- Each player has a point pile (starting empty) and a King count (starting 0).

THRESHOLD:
- First player: 32 with 0 Kings, 24 with 1, 18 with 2, 14 with 3, 11 with 4.
- Second player: 30 with 0 Kings, 22 with 1, 16 with 2, 12 with 3, 9 with 4.
- Points are the sum of the ranks in your point pile.
- Shortfall is threshold minus points, with a minimum of 0.

TURNS: Players alternate single turns, First player first. There are at most 40 turns in total (20 each), numbered 1 to 40.

START OF TURN:
1. If the acting player's points are at or above their threshold right now, they win immediately.
2. Otherwise the engine shows everyone the public state:
   - each point pile as a list of cards, each shown as its band if face down or its rank if face up;
   - both King counts and thresholds;
   - the scrap pile;
   - the draw pile size;
   - both hand sizes;
   - the turn number.
3. The acting player also sees their own hand and the exact ranks of their own face-down cards.

ACTION: The acting player chooses exactly one of the following.
(a) DRAW: Take the top card of the draw pile. Not allowed if you hold 8 cards or the pile is empty.
(b) POINTS: Place one point card from your hand face down in your point pile. Its band is visible to the opponent.
(c) SCUTTLE: Choose one point card from your hand and one card in the opponent's point pile. Reveal both.
   - If your rank is equal to or higher than the target's rank, both go to scrap.
   - Otherwise your card goes to scrap and the target stays in place, now face up.
(d) KING-SCUTTLE: Play a 10 from your hand against an opponent's King. Both go to scrap and the opponent's King count falls by 1.
(e) JACK: Play a Jack from your hand and choose any card in the opponent's point pile. It moves to your point pile face up, and the Jack goes to scrap.
(f) KING: Place a King from your hand. Your King count rises by 1.
(g) PASS: Allowed only if you cannot draw.
An illegal or unparseable choice counts as PASS.

END: After turn 40, the player with the smaller shortfall wins. Equal shortfalls are a draw.

How the winner is decided: You win at the start of any of your own turns if your point total is at or above your threshold. If no one has won after turn 40, the smaller shortfall (threshold minus points, minimum 0) wins, and equal shortfalls are a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Blind Scuttle (2 to 2 players, best with 2)

Two players race to build a point pile that reaches a threshold lowered by Kings. Point cards go in face down with only their band visible, and the opponent can scuttle, steal or flip them.

STATE (every item below must exist in the file):
  - each player: is_first (bool, starts False); everyone sees it. True for the randomly chosen First player.
  - each player: hand (list, starts []); only its owner sees it. Private hand. Cards are coded '1'..'10', 'J' and 'K'.
  - each player: hand_count (number, starts 0); everyone sees it. Number of cards in hand, which is public.
  - each player: point_pile (list, starts []); only its owner sees it. Exact point pile in order. Each entry is 'D<rank>' if face down or 'U<rank>' if face up.
  - each player: point_pile_view (list, starts []); everyone sees it. Public view of the point pile, position by position. A face-down card shows as Low, Mid or High; a face-up card shows its rank.
  - each player: points (number, starts 0); only its owner sees it. Sum of the ranks in the point pile.
  - each player: king_count (number, starts 0); everyone sees it. Number of Kings placed and not yet scuttled.
  - each player: threshold (number, starts 30); everyone sees it. Target points, set from is_first and king_count by the threshold table.
  - each player: shortfall (number, starts 30); only its owner sees it. max(threshold - points, 0).
  - each player: won (number, starts 0); everyone sees it. Set to 1 when the player wins at the start of their own turn.
  - the table: draw_pile (list, starts []); hidden from all players. Face-down draw pile, shuffled. Drawing takes a random entry.
  - the table: scrap (list, starts []); everyone sees it. Face-up scrap pile.
  - the table: turn (number, starts 1); everyone sees it. Current turn number, 1 to 40.
  - the table: acting_seat (number, starts 1); everyone sees it. Seat whose turn it is.
  - the table: action (text, starts ''); everyone sees it. Action chosen this turn.
  - the table: chosen_card (text, starts ''); everyone sees it. Hand card chosen for POINTS or SCUTTLE. It is revealed when it is played.
  - the table: target_index (number, starts 0); everyone sees it. Position in the opponent's point pile targeted by SCUTTLE or JACK.
  - parameters, each kept as a table attribute: deck_size = 48, point_ranks_min = 1, point_ranks_max = 10, copies_per_rank = 4, point_cards = 40, jacks = 4, kings = 4, hand_deal = 6, draw_pile_start = 36, hand_limit_for_draw = 8, max_turns = 40, turns_each = 20, low_band_max = 4, mid_band_min = 5, mid_band_max = 7, high_band_min = 8, first_threshold_0k = 32, first_threshold_1k = 24, first_threshold_2k = 18, first_threshold_3k = 14, first_threshold_4k = 11, second_threshold_0k = 30, second_threshold_1k = 22, second_threshold_2k = 16, second_threshold_3k = 12, second_threshold_4k = 9, king_scuttle_rank = 10, shortfall_min = 0

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Build the 48-card deck as a list: four each of '1' to '10', four 'J' and four 'K'. Put it in draw_pile.
  2. Pick one seat at random as First player: set is_first true for it and set acting_seat to that seat.
  3. Deal 6 cards to each player by drawing at random from draw_pile into hand. This leaves 36 in draw_pile. Set hand_count to 6.
  4. Set threshold to 32 for the First player and 30 for the second. Set shortfall equal to threshold, points to 0 and king_count to 0. point_pile, point_pile_view and scrap start empty. turn is 1.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] acting seat. What happens: If the acting player's points >= threshold, set their won = 1.
  2. [check] all players. What happens: End the game if any player's won == 1.
  3. [tell] all players. What happens: Announce the public state: each player's point_pile_view, king_count and threshold; scrap; len(draw_pile); each hand_count; turn; acting_seat.
  4. [sync] acting seat. What happens: The acting player sees their own hand and point_pile, which includes the exact ranks of their face-down cards.
  5. [ask] acting seat answers: one of the legal actions: draw, points, scuttle, king_scuttle, jack, king, pass. What happens: Set action. An illegal or unparseable reply sets action = pass.
  6. [ask] acting seat answers: a point card ('1'..'10') from hand. What happens: When action is points or scuttle, set chosen_card. If the reply is not a point card in hand, set action = pass.
  7. [ask] acting seat answers: a position in the opponent's point_pile_view, from 1 to its length. What happens: When action is scuttle or jack, set target_index. An invalid reply sets action = pass.
  8. [update] acting seat. What happens: When action == draw: move a random card from draw_pile to the acting player's hand, and add 1 to hand_count.
  9. [update] acting seat. What happens: When action == points: remove chosen_card from hand, append 'D<rank>' to point_pile, append its band (Low for 1-4, Mid for 5-7, High for 8-10) to point_pile_view, add rank to points, and subtract 1 from hand_count.
  10. [update] acting seat. What happens: When action == scuttle: remove chosen_card from hand, subtract 1 from hand_count, and reveal chosen_card and the target's rank. If chosen rank >= target rank, remove the target entry from the opponent's point_pile and point_pile_view, subtract its rank from the opponent's points, and append both ranks to scrap. Otherwise append chosen_card to scrap and turn the target face up: its point_pile entry becomes 'U<rank>' and its view entry becomes its rank.
  11. [update] acting seat. What happens: When action == king_scuttle: remove one '10' from hand, subtract 1 from hand_count, append '10' and 'K' to scrap, subtract 1 from the opponent's king_count, and recompute the opponent's threshold.
  12. [update] acting seat. What happens: When action == jack: remove 'J' from hand, subtract 1 from hand_count, and append 'J' to scrap. Remove the target entry from the opponent's point_pile and point_pile_view and subtract its rank from the opponent's points. Append 'U<rank>' to the acting point_pile, append the rank to the acting point_pile_view, and add the rank to the acting points.
  13. [update] acting seat. What happens: When action == king: remove 'K' from hand, subtract 1 from hand_count, add 1 to king_count, and recompute threshold.
  14. [update] all players. What happens: Recompute each player's threshold from the table: First is [32,24,18,14,11][king_count] and second is [30,22,16,12,9][king_count]. Set shortfall = max(threshold - points, 0). Add 1 to turn and switch acting_seat to the other seat.
  15. [check] all players. What happens: End the game if turn > 40.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When setup is done, each player has 6 cards in hand, draw_pile has 36 cards, and the deck had 40 point cards (ranks 1-10, four each), 4 Jacks and 4 Kings.
  R2. When the game starts, a random seat is First, and the First player takes turn 1.
  R3. When the players alternate single turns, the game has at most 40 turns, numbered 1 to 40.
  R4. When the First player has 0, 1, 2, 3 or 4 Kings, then their threshold is 32, 24, 18, 14 or 11.
  R5. When the second player has 0, 1, 2, 3 or 4 Kings, then their threshold is 30, 22, 16, 12 or 9.
  R6. When a turn starts and the acting player's points are at or above their threshold, then that player wins immediately.
  R7. When a player chooses DRAW, then a card moves from draw_pile to their hand. DRAW is not allowed with 8 cards in hand or an empty draw_pile.
  R8. When a player plays POINTS with a card of rank r, then it goes face down into their point pile, their points rise by r, and the opponent sees only its band (Low 1-4, Mid 5-7, High 8-10).
  R9. When a player scuttles with rank a against a target of rank t and a >= t, then both cards go to scrap and the opponent's points fall by t.
  R10. When a player scuttles with rank a against a target of rank t and a < t, then the attacking card goes to scrap and the target stays in place, now face up.
  R11. When a player plays a 10 against an opponent who has at least one King, then the 10 and a King go to scrap and the opponent's king_count falls by 1.
  R12. When a player plays a Jack on any card in the opponent's point pile, then that card moves face up into the player's point pile, both point totals change by its rank, and the Jack goes to scrap.
  R13. When a player places a King, then their king_count rises by 1 and their threshold drops to the next table value.
  R14. When a player cannot draw, then PASS is allowed.
  R15. When a reply is illegal or unparseable, then it counts as PASS and nothing changes.
  R16. When turn 40 ends with no winner, then the player with the smaller max(threshold - points, 0) wins, and equal shortfalls are a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Action choice | asked: acting seat | options: draw if hand_count < 8 and draw_pile is not empty; points if the hand holds a point card; scuttle if the hand holds a point card and the opponent's point pile is not empty; king_scuttle if the hand holds a 10 and the opponent's king_count >= 1; jack if the hand holds a J and the opponent's point pile is not empty; king if the hand holds a K; pass only if draw is not allowed.
  - Card to play | asked: acting seat, when action is points or scuttle | options: each distinct point-card rank ('1'..'10') in the acting player's hand.
  - Target card | asked: acting seat, when action is scuttle or jack | options: each position 1..n in the opponent's point pile, shown by its public view (band or face-up rank).

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: any player's won == 1, or turn > 40
  - each player's standing: you.won * 1000 - you.shortfall (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: A player who reaches their threshold at the start of their own turn wins at once. Otherwise, after turn 40, the player with the smaller shortfall (threshold minus points, minimum 0) wins, and equal shortfalls share the result as a draw.
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
rounds it says a match may run at most) and `limits.rounds_max` to at least that. The ending's `when` holds for the real ending AND when the cap
is reached, and its `rank_by` also ranks the players as the script says at the cap, so a match that hits the cap still ends with a winner.

## The interface the file must use

Independent tests were written against these names and you cannot see them, so use them exactly.

- each player: `is_first` (bool, visible: public, starts False): True for the randomly chosen First player.
- each player: `point_pile_view` (list, visible: public, starts []): Public view of the point pile, position by position. A face-down card shows as Low, Mid or High; a face-up card shows its rank.
- each player: `points` (number, visible: ally, starts 0): Sum of the ranks in the point pile.
- each player: `king_count` (number, visible: public, starts 0): Number of Kings placed and not yet scuttled.
- each player: `threshold` (number, visible: public, starts 30): Target points, set from is_first and king_count by the threshold table.
- each player: `shortfall` (number, visible: ally, starts 30): max(threshold - points, 0).
- each player: `won` (number, visible: public, starts 0): Set to 1 when the player wins at the start of their own turn.
- the table: `turn` (number, visible: public, starts 1): Current turn number, 1 to 40.
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 48, point_ranks_min = 1, point_ranks_max = 10, copies_per_rank = 4, point_cards = 40, jacks = 4, kings = 4, hand_deal = 6, draw_pile_start = 36, hand_limit_for_draw = 8, max_turns = 40, turns_each = 20, low_band_max = 4, mid_band_min = 5, mid_band_max = 7, high_band_min = 8, first_threshold_0k = 32, first_threshold_1k = 24, first_threshold_2k = 18, first_threshold_3k = 14, first_threshold_4k = 11, second_threshold_0k = 30, second_threshold_1k = 22, second_threshold_2k = 16, second_threshold_3k = 12, second_threshold_4k = 9, king_scuttle_rank = 10, shortfall_min = 0
- the game ends with ONE ending whose `rank_by` is `you.won * 1000 - you.shortfall`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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

1) Scuttle and Jack targeting. Do not depend on a separate `pile_ranks` list that can fall out of step with the real point pile (`point_pile` / `point_pile_view`). Either read the target's rank straight from the actual point-pile list, or make sure every step that changes the pile also updates `pile_ranks` in the same position. Guard every indexed lookup with a `when`/`if` so it only runs when `target_index` is between 1 and the opponent's pile length. Never evaluate the target lookup on turns whose action is not SCUTTLE or JACK. An out-of-range target counts as an illegal choice, which is PASS.
2) Unparseable or illegal replies. Make PASS the fallback for any reply that does not match a legal option. Do not let the engine default to the first offered option ('draw'). When the reply is invalid, no hand, pile, draw-pile or score attribute may change; only the turn advances.
3) Afterwards, re-check that SCUTTLE (a >= t: both cards to scrap and the owner's points drop by t; a < t: the attacker goes to scrap and the target turns face up, showing its rank in `point_pile_view`) and JACK (the card moves face up to the actor's pile, both point totals change by its rank, the Jack goes to scrap) update `points`, `threshold` and `shortfall` correctly.

````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "blind_scuttle",
    "name": "Blind Scuttle",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "blurb": "Race to a King-lowered threshold with face-down point cards that your opponent can scuttle, steal or flip."
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
        "key": "is_first",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "hand",
        "visible": "ally",
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
        "key": "point_pile",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "point_pile_view",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "points",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "king_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "threshold",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "shortfall",
        "visible": "ally",
        "type": "number",
        "initial": 30
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
        "key": "card_offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "target_offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      }
    ],
    "game": [
      {
        "key": "draw_pile",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "draw_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "scrap",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "turn",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "acting_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "action",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "chosen_card",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "target_index",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "target_code",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "target_rank",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "point_rank_codes",
        "visible": "none",
        "type": "list",
        "initial": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
      },
      {
        "key": "slot_labels",
        "visible": "none",
        "type": "list",
        "initial": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40"]
      },
      {
        "key": "slot_indices",
        "visible": "none",
        "type": "list",
        "initial": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39]
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 48
      },
      {
        "key": "point_ranks_min",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "point_ranks_max",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "copies_per_rank",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "point_cards",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "jacks",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "kings",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "hand_deal",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "draw_pile_start",
        "visible": "public",
        "type": "number",
        "initial": 36
      },
      {
        "key": "hand_limit_for_draw",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "max_turns",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "turns_each",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "low_band_max",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "mid_band_min",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "mid_band_max",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "high_band_min",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "first_threshold_0k",
        "visible": "public",
        "type": "number",
        "initial": 32
      },
      {
        "key": "first_threshold_1k",
        "visible": "public",
        "type": "number",
        "initial": 24
      },
      {
        "key": "first_threshold_2k",
        "visible": "public",
        "type": "number",
        "initial": 18
      },
      {
        "key": "first_threshold_3k",
        "visible": "public",
        "type": "number",
        "initial": 14
      },
      {
        "key": "first_threshold_4k",
        "visible": "public",
        "type": "number",
        "initial": 11
      },
      {
        "key": "second_threshold_0k",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "second_threshold_1k",
        "visible": "public",
        "type": "number",
        "initial": 22
      },
      {
        "key": "second_threshold_2k",
        "visible": "public",
        "type": "number",
        "initial": 16
      },
      {
        "key": "second_threshold_3k",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "second_threshold_4k",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "king_scuttle_rank",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "shortfall_min",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "build the deck",
      "do": [
        {
          "set": {
            "key": "draw_pile",
            "value": ["1", "1", "1", "1", "2", "2", "2", "2", "3", "3", "3", "3", "4", "4", "4", "4", "5", "5", "5", "5", "6", "6", "6", "6", "7", "7", "7", "7", "8", "8", "8", "8", "9", "9", "9", "9", "10", "10", "10", "10", "J", "J", "J", "J", "K", "K", "K", "K"]
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "pick the first player",
      "do": [
        {
          "set": {
            "key": "acting_seat",
            "value": {
              "calc": "1 if uniform(0, 1) < 0.5 else 2"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "is_first",
            "value": {
              "calc": "you.seat == acting_seat"
            }
          }
        }
      ],
      "text": "Seat {acting_seat} is the First player and takes turn 1."
    },
    {
      "use": "update",
      "label": "deal the hands",
      "do": [
        {"set": {"key": "pick", "value": {"calc": "draw_pile[int(uniform(0, len(draw_pile)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "draw_pile", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "draw_pile[int(uniform(0, len(draw_pile)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "draw_pile", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "draw_pile[int(uniform(0, len(draw_pile)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "draw_pile", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "draw_pile[int(uniform(0, len(draw_pile)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "draw_pile", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "draw_pile[int(uniform(0, len(draw_pile)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "draw_pile", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "draw_pile[int(uniform(0, len(draw_pile)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "draw_pile", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "draw_pile[int(uniform(0, len(draw_pile)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "draw_pile", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "draw_pile[int(uniform(0, len(draw_pile)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "draw_pile", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "draw_pile[int(uniform(0, len(draw_pile)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "draw_pile", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "draw_pile[int(uniform(0, len(draw_pile)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "draw_pile", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "draw_pile[int(uniform(0, len(draw_pile)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "draw_pile", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "draw_pile[int(uniform(0, len(draw_pile)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "draw_pile", "value": {"calc": "pick"}}},
        {
          "set": {
            "players": "all",
            "key": "hand_count",
            "value": {
              "calc": "len(you.hand)"
            }
          }
        },
        {
          "set": {
            "key": "draw_count",
            "value": {
              "calc": "len(draw_pile)"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": ""
          }
        }
      ],
      "text": "Each player is dealt {hand_deal} cards. The draw pile holds {draw_count} cards."
    },
    {
      "use": "update",
      "label": "set the thresholds",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "points",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "king_count",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "threshold",
            "value": {
              "calc": "([first_threshold_0k, first_threshold_1k, first_threshold_2k, first_threshold_3k, first_threshold_4k] if you.is_first else [second_threshold_0k, second_threshold_1k, second_threshold_2k, second_threshold_3k, second_threshold_4k])[min(you.king_count, kings)]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "shortfall",
            "value": {
              "calc": "max(you.threshold - you.points, shortfall_min)"
            }
          }
        },
        {
          "set": {
            "key": "turn",
            "value": 1
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
      "phase": "start",
      "label": "threshold reached",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.seat == acting_seat and you.points >= you.threshold"
            },
            "key": "won",
            "value": 1,
            "text": "Seat {player} starts their turn at or above their threshold and wins."
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "start",
      "label": "a player has won",
      "when": {
        "calc": "any(p.won == 1 for p in players)"
      },
      "against": [
        "over"
      ]
    },
    {
      "use": "tell",
      "phase": "start",
      "label": "the public state",
      "to": "all",
      "text": "Turn {turn} of {max_turns}; seat {acting_seat} to act. Seat 1: point pile {players[0].point_pile_view}, Kings {players[0].king_count}, threshold {players[0].threshold}, hand {players[0].hand_count} cards. Seat 2: point pile {players[1].point_pile_view}, Kings {players[1].king_count}, threshold {players[1].threshold}, hand {players[1].hand_count} cards. Scrap: {scrap}. Draw pile: {draw_count} cards."
    },
    {
      "use": "update",
      "phase": "start",
      "label": "the offers",
      "do": [
        {
          "set": {
            "key": "action",
            "value": ""
          }
        },
        {
          "set": {
            "key": "chosen_card",
            "value": ""
          }
        },
        {
          "set": {
            "key": "target_index",
            "value": 0
          }
        },
        {
          "set": {
            "key": "target_code",
            "value": ""
          }
        },
        {
          "set": {
            "key": "target_rank",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "(['draw'] if you.hand_count < hand_limit_for_draw and len(draw_pile) > 0 else []) + (['points'] if len([c for c in point_rank_codes if c in you.hand]) > 0 else []) + (['scuttle'] if len([c for c in point_rank_codes if c in you.hand]) > 0 and len(players[2 - you.seat].point_pile) > 0 else []) + (['king_scuttle'] if point_rank_codes[king_scuttle_rank - 1] in you.hand and players[2 - you.seat].king_count >= 1 else []) + (['jack'] if 'J' in you.hand and len(players[2 - you.seat].point_pile) > 0 else []) + (['king'] if 'K' in you.hand else []) + (['pass'] if not (you.hand_count < hand_limit_for_draw and len(draw_pile) > 0) else [])"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "card_offer",
            "value": {
              "calc": "[c for c in point_rank_codes if c in you.hand]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "target_offer",
            "value": {
              "calc": "[slot_labels[k] + ':' + players[2 - you.seat].point_pile_view[k] for k in slot_indices if k < len(players[2 - you.seat].point_pile_view)]"
            }
          }
        }
      ]
    },
    {
      "use": "sync",
      "phase": "start",
      "label": "your hand",
      "mode": "self",
      "to": {
        "where": "you.seat == acting_seat"
      },
      "fields": [
        "hand",
        "point_pile",
        "points"
      ],
      "text": "Your hand and your exact point pile (D = face down, U = face up):"
    },
    {
      "use": "ask",
      "phase": "action",
      "label": "choose an action",
      "to": {
        "where": "you.seat == acting_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "act"
      },
      "text": "Turn {turn}: choose one action from those offered (draw, points, scuttle, king_scuttle, jack, king, pass)."
    },
    {
      "use": "update",
      "phase": "action",
      "label": "record the action",
      "do": [
        {
          "set": {
            "key": "action",
            "value": {
              "calc": "$act if $act in players[acting_seat - 1].offer else 'pass'"
            }
          }
        }
      ],
      "text": "Seat {acting_seat} chooses {action}."
    },
    {
      "use": "ask",
      "phase": "action",
      "label": "choose a card",
      "when": {
        "calc": "action in ['points', 'scuttle']"
      },
      "to": {
        "where": "you.seat == acting_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "card_offer"
        }
      },
      "verify": {
        "bind": "card"
      },
      "text": "Choose the point card from your hand to play for {action}."
    },
    {
      "use": "ask",
      "phase": "action",
      "label": "choose a target",
      "when": {
        "calc": "action in ['scuttle', 'jack']"
      },
      "to": {
        "where": "you.seat == acting_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "target_offer"
        }
      },
      "verify": {
        "bind": "tgt"
      },
      "text": "Choose the target card in your opponent's point pile, by position and its public view (band if face down, rank if face up)."
    },
    {
      "use": "update",
      "phase": "action",
      "label": "resolve the choices",
      "do": [
        {
          "set": {
            "key": "chosen_card",
            "value": "$card",
            "if": {
              "calc": "action in ['points', 'scuttle']"
            }
          }
        },
        {
          "set": {
            "key": "target_index",
            "value": {
              "calc": "([k + 1 for k in slot_indices if k < len(players[acting_seat - 1].target_offer) and players[acting_seat - 1].target_offer[k] == $tgt] + [0])[0]"
            },
            "if": {
              "calc": "action in ['scuttle', 'jack']"
            }
          }
        },
        {
          "set": {
            "key": "action",
            "value": "pass",
            "if": {
              "calc": "(action in ['points', 'scuttle'] and chosen_card not in players[acting_seat - 1].card_offer) or (action in ['scuttle', 'jack'] and (target_index < 1 or target_index > len(players[2 - acting_seat].point_pile)))"
            }
          }
        },
        {
          "set": {
            "key": "chosen_card",
            "value": "",
            "if": {
              "calc": "action == 'pass'"
            }
          }
        },
        {
          "set": {
            "key": "target_index",
            "value": 0,
            "if": {
              "calc": "action == 'pass'"
            }
          }
        },
        {
          "set": {
            "key": "target_code",
            "value": {
              "calc": "[r for r in point_rank_codes if ('D' + r) == players[2 - acting_seat].point_pile[target_index - 1] or ('U' + r) == players[2 - acting_seat].point_pile[target_index - 1]][0]"
            },
            "if": {
              "calc": "action in ['scuttle', 'jack'] and target_index >= 1 and target_index <= len(players[2 - acting_seat].point_pile)"
            }
          }
        },
        {
          "set": {
            "key": "target_rank",
            "value": {
              "calc": "int(target_code)"
            },
            "if": {
              "calc": "action in ['scuttle', 'jack'] and target_code != ''"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "draw",
      "when": {
        "calc": "action == 'draw'"
      },
      "do": [
        {"set": {"key": "pick", "value": {"calc": "draw_pile[int(uniform(0, len(draw_pile)))]"}}},
        {"append": {"player": {"calc": "acting_seat"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "draw_pile", "value": {"calc": "pick"}}},
        {"adjust": {"player": {"calc": "acting_seat"}, "key": "hand_count", "value": 1}},
        {"adjust": {"key": "draw_count", "value": -1}}
      ],
      "text": "Seat {acting_seat} draws a card."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "points",
      "when": {
        "calc": "action == 'points'"
      },
      "do": [
        {"remove": {"player": {"calc": "acting_seat"}, "key": "hand", "value": {"calc": "chosen_card"}}},
        {"adjust": {"player": {"calc": "acting_seat"}, "key": "hand_count", "value": -1}},
        {"append": {"player": {"calc": "acting_seat"}, "key": "point_pile", "value": {"calc": "'D' + chosen_card"}}},
        {"append": {"player": {"calc": "acting_seat"}, "key": "point_pile_view", "value": {"calc": "'Low' if int(chosen_card) <= low_band_max else ('Mid' if int(chosen_card) <= mid_band_max else 'High')"}}},
        {"adjust": {"player": {"calc": "acting_seat"}, "key": "points", "value": {"calc": "int(chosen_card)"}}}
      ],
      "text": "Seat {acting_seat} places a point card face down; only its band shows in their point pile."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "scuttle",
      "when": {
        "calc": "action == 'scuttle' and target_code != ''"
      },
      "do": [
        {"remove": {"player": {"calc": "acting_seat"}, "key": "hand", "value": {"calc": "chosen_card"}}},
        {"adjust": {"player": {"calc": "acting_seat"}, "key": "hand_count", "value": -1}},
        {
          "set": {
            "player": {"calc": "3 - acting_seat"},
            "key": "point_pile",
            "value": {"calc": "[players[2 - acting_seat].point_pile[k] for k in slot_indices if k < len(players[2 - acting_seat].point_pile) and k != target_index - 1]"},
            "if": {"calc": "int(chosen_card) >= target_rank"}
          }
        },
        {
          "set": {
            "player": {"calc": "3 - acting_seat"},
            "key": "point_pile_view",
            "value": {"calc": "[players[2 - acting_seat].point_pile_view[k] for k in slot_indices if k < len(players[2 - acting_seat].point_pile_view) and k != target_index - 1]"},
            "if": {"calc": "int(chosen_card) >= target_rank"}
          }
        },
        {
          "adjust": {
            "player": {"calc": "3 - acting_seat"},
            "key": "points",
            "value": {"calc": "-target_rank"},
            "if": {"calc": "int(chosen_card) >= target_rank"},
            "text": "The {chosen_card} is equal to or higher than the {target_code}: both cards go to scrap."
          }
        },
        {
          "append": {
            "key": "scrap",
            "value": {"calc": "chosen_card"}
          }
        },
        {
          "append": {
            "key": "scrap",
            "value": {"calc": "target_code"},
            "if": {"calc": "int(chosen_card) >= target_rank"}
          }
        },
        {
          "set": {
            "player": {"calc": "3 - acting_seat"},
            "key": "point_pile",
            "value": {"calc": "[('U' + target_code) if k == target_index - 1 else players[2 - acting_seat].point_pile[k] for k in slot_indices if k < len(players[2 - acting_seat].point_pile)]"},
            "if": {"calc": "int(chosen_card) < target_rank"}
          }
        },
        {
          "set": {
            "player": {"calc": "3 - acting_seat"},
            "key": "point_pile_view",
            "value": {"calc": "[target_code if k == target_index - 1 else players[2 - acting_seat].point_pile_view[k] for k in slot_indices if k < len(players[2 - acting_seat].point_pile_view)]"},
            "if": {"calc": "int(chosen_card) < target_rank"},
            "text": "The {chosen_card} is lower than the {target_code}: the attacking card goes to scrap and the target stays, now face up."
          }
        }
      ],
      "text": "Seat {acting_seat} scuttles with a {chosen_card} against position {target_index} of seat {3 - acting_seat}'s point pile, revealed as a {target_code}."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "king scuttle",
      "when": {
        "calc": "action == 'king_scuttle'"
      },
      "do": [
        {"remove": {"player": {"calc": "acting_seat"}, "key": "hand", "value": {"calc": "point_rank_codes[king_scuttle_rank - 1]"}}},
        {"adjust": {"player": {"calc": "acting_seat"}, "key": "hand_count", "value": -1}},
        {"append": {"key": "scrap", "value": {"calc": "point_rank_codes[king_scuttle_rank - 1]"}}},
        {"append": {"key": "scrap", "value": "K"}},
        {
          "adjust": {
            "player": {"calc": "3 - acting_seat"},
            "key": "king_count",
            "value": -1,
            "if": {"calc": "players[2 - acting_seat].king_count >= 1"}
          }
        }
      ],
      "text": "Seat {acting_seat} plays a {king_scuttle_rank} against one of the opponent's Kings: both go to scrap."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "jack",
      "when": {
        "calc": "action == 'jack' and target_code != ''"
      },
      "do": [
        {"remove": {"player": {"calc": "acting_seat"}, "key": "hand", "value": "J"}},
        {"adjust": {"player": {"calc": "acting_seat"}, "key": "hand_count", "value": -1}},
        {"append": {"key": "scrap", "value": "J"}},
        {
          "set": {
            "player": {"calc": "3 - acting_seat"},
            "key": "point_pile",
            "value": {"calc": "[players[2 - acting_seat].point_pile[k] for k in slot_indices if k < len(players[2 - acting_seat].point_pile) and k != target_index - 1]"}
          }
        },
        {
          "set": {
            "player": {"calc": "3 - acting_seat"},
            "key": "point_pile_view",
            "value": {"calc": "[players[2 - acting_seat].point_pile_view[k] for k in slot_indices if k < len(players[2 - acting_seat].point_pile_view) and k != target_index - 1]"}
          }
        },
        {"adjust": {"player": {"calc": "3 - acting_seat"}, "key": "points", "value": {"calc": "-target_rank"}}},
        {"append": {"player": {"calc": "acting_seat"}, "key": "point_pile", "value": {"calc": "'U' + target_code"}}},
        {"append": {"player": {"calc": "acting_seat"}, "key": "point_pile_view", "value": {"calc": "target_code"}}},
        {"adjust": {"player": {"calc": "acting_seat"}, "key": "points", "value": {"calc": "target_rank"}}}
      ],
      "text": "Seat {acting_seat} plays a Jack and takes the {target_code} from position {target_index} of the opponent's point pile, face up. The Jack goes to scrap."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "king",
      "when": {
        "calc": "action == 'king'"
      },
      "do": [
        {"remove": {"player": {"calc": "acting_seat"}, "key": "hand", "value": "K"}},
        {"adjust": {"player": {"calc": "acting_seat"}, "key": "hand_count", "value": -1}},
        {"adjust": {"player": {"calc": "acting_seat"}, "key": "king_count", "value": 1}}
      ],
      "text": "Seat {acting_seat} places a King."
    },
    {
      "use": "update",
      "phase": "end",
      "label": "end of turn",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "threshold",
            "value": {
              "calc": "([first_threshold_0k, first_threshold_1k, first_threshold_2k, first_threshold_3k, first_threshold_4k] if you.is_first else [second_threshold_0k, second_threshold_1k, second_threshold_2k, second_threshold_3k, second_threshold_4k])[max(0, min(you.king_count, kings))]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "shortfall",
            "value": {
              "calc": "max(you.threshold - you.points, shortfall_min)"
            }
          }
        },
        {
          "adjust": {
            "key": "turn",
            "value": 1
          }
        },
        {
          "set": {
            "key": "acting_seat",
            "value": {
              "calc": "3 - acting_seat"
            }
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "end",
      "label": "after the last turn",
      "when": {
        "calc": "turn > max_turns"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "any(p.won == 1 for p in players) or turn > max_turns"
      },
      "rank_by": "you.won * 1000 - you.shortfall",
      "text": "Winner: {result}. Seat 1: points {players[0].points}, threshold {players[0].threshold}, shortfall {players[0].shortfall}. Seat 2: points {players[1].points}, threshold {players[1].threshold}, shortfall {players[1].shortfall}."
    }
  },
  "limits": {
    "rounds": 40,
    "rounds_max": 41,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "DECK: {deck_size} cards: {point_cards} point cards (ranks {point_ranks_min} to {point_ranks_max}, {copies_per_rank} copies of each, no suits), {jacks} Jacks and {kings} Kings. The deck is shuffled.\n\nBANDS: Every point card has a band. Low is ranks {point_ranks_min}-{low_band_max}, Mid is ranks {mid_band_min}-{mid_band_max}, High is ranks {high_band_min}-{point_ranks_max}.\n\nSETUP: A First player is picked at random. Each player is dealt {hand_deal} cards; hands are private. The other {draw_pile_start} cards are the face-down draw pile. The scrap pile is face up and fully public. Each player has a point pile (starting empty) and a King count (starting 0).\n\nTHRESHOLD: First player: {first_threshold_0k} with 0 Kings, {first_threshold_1k} with 1, {first_threshold_2k} with 2, {first_threshold_3k} with 3, {first_threshold_4k} with 4. Second player: {second_threshold_0k} with 0 Kings, {second_threshold_1k} with 1, {second_threshold_2k} with 2, {second_threshold_3k} with 3, {second_threshold_4k} with 4. Points are the sum of the ranks in your point pile. Shortfall is threshold minus points, with a minimum of {shortfall_min}.\n\nTURNS: Players alternate single turns, First player first. There are at most {max_turns} turns in total ({turns_each} each), numbered 1 to {max_turns}.\n\nSTART OF TURN: If the acting player's points are at or above their threshold right now, they win immediately. Otherwise everyone is shown the public state: each point pile as a list of cards (its band if face down, its rank if face up), both King counts and thresholds, the scrap pile, the draw pile size, both hand sizes and the turn number. The acting player also sees their own hand and the exact ranks of their own face-down cards.\n\nACTION: The acting player chooses exactly one of the following; you are only offered actions you may legally take.\n(a) DRAW: Take the top card of the draw pile. Not allowed if you hold {hand_limit_for_draw} cards or the pile is empty.\n(b) POINTS: Place one point card from your hand face down in your point pile. Your points rise by its rank. Its band is visible to the opponent.\n(c) SCUTTLE: Choose one point card from your hand and one card in the opponent's point pile (by position). Reveal both. If your rank is equal to or higher than the target's rank, both go to scrap and the opponent's points fall by the target's rank. Otherwise your card goes to scrap and the target stays in place, now face up (its rank shows in the public view); the opponent's points do not change.\n(d) KING-SCUTTLE: Play a {king_scuttle_rank} from your hand against an opponent's King (only if they have at least one). Both go to scrap and the opponent's King count falls by 1, raising their threshold.\n(e) JACK: Play a Jack from your hand and choose any card in the opponent's point pile. It moves to your point pile face up: your points rise by its rank and theirs fall by it. The Jack goes to scrap.\n(f) KING: Place a King from your hand. Your King count rises by 1 and your threshold drops to the next table value.\n(g) PASS: Allowed only if you cannot draw.\nAn illegal or unparseable choice counts as PASS: nothing changes and the turn passes.\n\nEND: After turn {max_turns}, the player with the smaller shortfall wins. Equal shortfalls are a draw (the win is shared)."
}
```
````
