# Task: write the XColos game file for "Lost Cities: Embargo"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 2; set `meta.players` to {"min": 2, "max": 2, "suggested": 2} (the suggested size is the one the game plays best at).

COMPONENTS. A 30-card deck in three colours: Red, Green, Blue. Each colour has number cards 2, 3, 4, 5, 6, 7, 8, 9, 10 and one Wager card. There are three face-up discard piles, one per colour; only the top card of each is visible and takeable. Each player has one column per colour.

STRUCTURE. The match is 2 hands of 20 turns each, 40 rounds in total. A round is one turn of the active player. In hand 1, Seat 1 takes the odd turns (1, 3, ..., 19) and Seat 2 the even turns. In hand 2, Seat 2 takes the odd turns and Seat 1 the even turns.

HAND 1 SETUP (round 1). Shuffle the 30 cards once and record this order as the match order. Deal cards 1-5 to Seat 1 and cards 6-10 to Seat 2. Cards 11-30, in order, form the face-down draw pile (card 11 on top). Each hand is an ordered list of 5 slots; slot 1 is the oldest card.

HAND 2 SETUP (round 21). Clear all columns and discard piles. Do NOT reshuffle. Use the recorded match order: cards 1-5 go to Seat 2 and cards 6-10 go to Seat 1. Cards 11-30 form the draw pile in the same order. Each seat therefore starts hand 2 with the cards the other seat started hand 1 with, and moves at the same position.

EMBARGO (at each hand setup, after the deal). Each player secretly and simultaneously names one colour: Red, Green or Blue. This is their embargo against the opponent for this hand. It is revealed only at end-of-hand scoring.

A TURN. The active player privately sees their own hand. Both players see both players' columns, the tops of the three discard piles, the number of cards in the draw pile, and all earlier announcements of the current hand.
(1) Choose a card by slot, and choose PLAY or DISCARD.
- DISCARD: the card goes face-up onto its colour's discard pile. There is no cost.
- PLAY: if the play is legal, the card is added to the player's column of its colour. If it is illegal, the card goes onto its colour's discard pile and the player loses 1 point.
A number card is legal if it is higher than every number already in that column. A Wager is legal only if that column contains no number card yet.
(2) Choose where to draw from: the draw pile, the Red pile, the Green pile or the Blue pile. The player takes the top card of the chosen pile. If that discard pile is empty, or its top card is the card the player discarded this turn, they take the top card of the draw pile instead. The drawn card goes into slot 5, and the other cards close up to the left. The draw pile always has at least one card at this point.
(3) Announcement to both players: either 'Seat X played [card] to their [colour] column' or 'Seat X discarded [card]'. A discard announcement never says whether it was voluntary or an illegal play. The announcement also gives the pile drawn from, and the card taken if it came from a discard pile. Penalties and totals are not announced.

END OF HAND (after turn 20). Score each of a player's three columns:
- An empty column scores 0.
- Otherwise let S = (sum of its number cards) - 8.
- If S > 0 and the column holds the Wager, multiply S by 1.5 and round down. If S <= 0, the Wager has no effect.
- A column with 5 or more cards, the Wager included, gains +10.
- Embargo: if this column's colour is the one the opponent embargoed, and its score so far is positive, halve it, rounding down. A zero or negative score is unchanged.
The hand score is the sum of the three column scores minus the player's illegal-play penalties for that hand. Add it to the player's total. Then announce both embargoes, both hand scores and both totals.

END OF MATCH. After hand 2 is scored, the match ends.

How the winner is decided: After both hands, the player with the higher total wins. Equal totals are a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Lost Cities: Embargo (2 to 2 players, best with 2)

Two players build ascending colour columns over two mirrored hands from one recorded shuffle. Each player secretly embargoes one opponent colour per hand, which halves a positive column score in that colour.

STATE (every item below must exist in the file):
  - each player: hand (list, starts []); only its owner sees it. Ordered list of up to 5 card codes such as R5, G10 or BW (W = Wager). Slot 1 is the oldest card.
  - each player: red_col (list, starts []); everyone sees it. Cards in this player's Red column, in play order
  - each player: green_col (list, starts []); everyone sees it. Cards in this player's Green column, in play order
  - each player: blue_col (list, starts []); everyone sees it. Cards in this player's Blue column, in play order
  - each player: embargo (text, starts ''); only its owner sees it. The colour this player embargoed against the opponent this hand. It is revealed in the end-of-hand announcement.
  - each player: penalty (number, starts 0); only its owner sees it. Illegal-play penalty points this hand (1 per illegal play), never announced
  - each player: hand_score (number, starts 0); everyone sees it. Score of the last completed hand, set at end-of-hand scoring
  - each player: total (number, starts 0); everyone sees it. Match total. It changes only at end-of-hand scoring.
  - the table: match_order (list, starts []); hidden from all players. The recorded order of all 30 cards from the single shuffle in round 1
  - the table: deck (list, starts []); hidden from all players. Face-down draw pile, ordered; the first element is the top
  - the table: draw_count (number, starts 20); everyone sees it. Number of cards left in the draw pile
  - the table: red_pile (list, starts []); hidden from all players. Red discard pile; the last element is the top
  - the table: green_pile (list, starts []); hidden from all players. Green discard pile; the last element is the top
  - the table: blue_pile (list, starts []); hidden from all players. Blue discard pile; the last element is the top
  - the table: red_top (text, starts ''); everyone sees it. Top card of the Red discard pile, or empty
  - the table: green_top (text, starts ''); everyone sees it. Top card of the Green discard pile, or empty
  - the table: blue_top (text, starts ''); everyone sees it. Top card of the Blue discard pile, or empty
  - the table: round (number, starts 1); everyone sees it. Round number, 1 to 40
  - the table: hand_number (number, starts 1); everyone sees it. 1 for rounds 1-20, 2 for rounds 21-40
  - the table: active_seat (number, starts 1); everyone sees it. Seat taking this round's turn. In hand 1: odd round gives seat 1, even round gives seat 2. In hand 2: odd round gives seat 2, even round gives seat 1.
  - the table: last_discard (text, starts ''); everyone sees it. Card that went to a discard pile this turn (a voluntary discard or an illegal play), or empty
  - the table: announcements (list, starts []); everyone sees it. Turn announcements of the current hand, cleared at hand 2 setup
  - parameters, each kept as a table attribute: deck_size = 30, colours = 3, lowest_number_card = 2, highest_number_card = 10, wagers_per_colour = 1, hands = 2, turns_per_hand = 20, total_rounds = 40, hand_size = 5, draw_pile_size = 20, column_offset = 8, wager_multiplier = 1.5, long_column_threshold = 5, long_column_bonus = 10, illegal_play_penalty = 1, embargo_divisor = 2

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. The 30 cards are R2-R10, RW, G2-G10, GW, B2-B10 and BW.
  2. All totals start at 0. The round counter starts at 1.
  3. The shuffle, the deal and the embargoes happen as round steps guarded by round == 1 (and round == 21 for hand 2), so they belong to the script.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] table. What happens: When round == 1: draw all 30 cards at random into match_order. Seat 1 hand = match_order[1..5]. Seat 2 hand = match_order[6..10]. deck = match_order[11..30]. draw_count = 20.
  2. [update] table. What happens: When round == 21: hand_number = 2. Clear red_col, green_col and blue_col for both seats. Clear red_pile, green_pile and blue_pile and their tops. Set penalty = 0 for both seats and clear announcements. Without reshuffling: Seat 2 hand = match_order[1..5], Seat 1 hand = match_order[6..10], deck = match_order[11..30], draw_count = 20.
  3. [poll] all players answers: When round == 1 or round == 21: one of Red, Green, Blue. What happens: embargo = the answer, kept secret (ally) until end-of-hand scoring.
  4. [update] table. What happens: Set active_seat: if hand_number == 1 then (1 if round is odd else 2), otherwise (2 if round is odd else 1). Set last_discard = ''.
  5. [sync] all players. What happens: Each seat sees its own hand. Both see all columns, red_top, green_top, blue_top, draw_count and the announcements.
  6. [ask] seat active_seat answers: one of 10 options: 'PLAY slot k (card)' or 'DISCARD slot k (card)' for k = 1..5. What happens: Records the chosen slot and action.
  7. [update] seat active_seat. What happens: Remove the chosen card from hand. DISCARD: append it to its colour's pile, set that colour's top = card, last_discard = card. PLAY of a number card: legal if it is higher than every number in that colour's column, and then it is appended to the column. PLAY of a Wager: legal if the column holds no number card, and then it is appended to the column. An illegal PLAY goes to its colour's pile as a discard: top = card, last_discard = card, penalty += 1.
  8. [ask] seat active_seat answers: one of: draw pile, Red pile, Green pile, Blue pile. What happens: Records the draw source.
  9. [update] seat active_seat. What happens: If a colour pile is chosen and it is non-empty and its top != last_discard: remove the top of that pile into hand slot 5 and reset that colour's top to the new top or ''. Otherwise remove deck[1] into hand slot 5 and set draw_count -= 1. The remaining cards close up to the left, so hand is ordered with the new card last.
  10. [tell] all players. What happens: Append to announcements and broadcast either 'Seat X played [card] to their [colour] column' or 'Seat X discarded [card]' (illegal plays are also announced as discards), plus 'and drew from the draw pile' or 'and took [card] from the [colour] pile'. Penalties and totals are not announced.
  11. [update] all players. What happens: When round == 20 or round == 40: score each column. An empty column scores 0. Otherwise S = (sum of number cards) - 8. If S > 0 and the column holds the Wager, S = floor(S * 1.5). If the column has >= 5 cards, S += 10. If the column's colour equals the opponent's embargo and S > 0, S = floor(S / 2). hand_score = the sum of the three column scores - penalty. total += hand_score.
  12. [tell] all players. What happens: When round == 20 or round == 40: announce both seats' embargo, hand_score and total.
  13. [update] table. What happens: round += 1.
  14. [check] table. What happens: End the game if round > 40, otherwise continue.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. The deck has 30 cards: in each of Red, Green and Blue, the numbers 2 to 10 and one Wager.
  R2. In round 1 the deck is shuffled once into match_order. Seat 1 gets cards 1-5, Seat 2 gets cards 6-10, and cards 11-30 form the draw pile with card 11 on top (draw_count = 20).
  R3. In round 21 all columns, discard piles and penalties are cleared and there is no reshuffle. Seat 2 gets match_order cards 1-5, Seat 1 gets cards 6-10, and cards 11-30 form the draw pile in the same order.
  R4. In rounds 1 and 21, both players simultaneously and secretly name an embargo colour (Red, Green or Blue), revealed only at end-of-hand scoring.
  R5. In hand 1, Seat 1 acts on odd rounds and Seat 2 on even rounds. In hand 2 (rounds 21-40), Seat 2 acts on odd rounds and Seat 1 on even rounds.
  R6. When a player discards a card, it goes onto its colour's discard pile at no cost.
  R7. When a player plays a number card higher than every number in that colour's column, it is added to the column.
  R8. When a player plays a number card not higher than every number in that colour's column, it goes onto its colour's discard pile and the player's penalty rises by 1.
  R9. When a player plays a Wager to a column with no number card, it is added to the column. If the column already has a number card, the play is illegal: the Wager is discarded and penalty rises by 1.
  R10. When a player draws from a discard pile that is empty, or whose top is the card that player sent to a discard pile this turn, they take the top card of the draw pile instead.
  R11. When a card is drawn it goes into hand slot 5, and the other cards close up so slot 1 stays the oldest.
  R12. Each turn's announcement says either 'Seat X played [card] to their [colour] column' or 'Seat X discarded [card]', never distinguishing an illegal play from a voluntary discard. It also gives the pile drawn from, and the card taken if it came from a discard pile.
  R13. When a hand is scored, an empty column scores 0. Otherwise S = sum of number cards - 8; for example R4, R9 gives 5.
  R14. When a column with S > 0 holds the Wager, S becomes floor(1.5 * S); for example S = 5 becomes 7. When S <= 0 the Wager has no effect.
  R15. When a column has 5 or more cards, Wager included, it gains +10.
  R16. When a column's colour is the opponent's embargo and its score so far is positive, it is halved rounding down (for example 17 becomes 8). A zero or negative score is unchanged.
  R17. Hand score = the sum of the three column scores - illegal-play penalties that hand. It is added to total, then both embargoes, hand scores and totals are announced.
  R18. After round 40 is scored the match ends. The higher total wins, and equal totals are a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Embargo colour (rounds 1 and 21) | asked: both seats | options: Red, Green, Blue
  - Card and action | asked: active seat | options: PLAY or DISCARD for each of the 5 hand slots (10 options), each labelled with its card; illegal plays are offered because they are allowed at a penalty
  - Draw source | asked: active seat | options: draw pile, Red pile, Green pile, Blue pile (an empty pile, or one topped by this turn's discard, falls back to the draw pile)

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round > 40 (after hand 2 is scored)
  - each player's standing: you.total (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's match total after both hands. The higher total wins, and equal totals share the win (a draw).
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

- each player: `red_col` (list, visible: public, starts []): Cards in this player's Red column, in play order
- each player: `green_col` (list, visible: public, starts []): Cards in this player's Green column, in play order
- each player: `blue_col` (list, visible: public, starts []): Cards in this player's Blue column, in play order
- each player: `hand_score` (number, visible: public, starts 0): Score of the last completed hand, set at end-of-hand scoring
- each player: `total` (number, visible: public, starts 0): Match total. It changes only at end-of-hand scoring.
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 30, colours = 3, lowest_number_card = 2, highest_number_card = 10, wagers_per_colour = 1, hands = 2, turns_per_hand = 20, total_rounds = 40, hand_size = 5, draw_pile_size = 20, column_offset = 8, wager_multiplier = 1.5, long_column_threshold = 5, long_column_bonus = 10, illegal_play_penalty = 1, embargo_divisor = 2
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

## Guidance from the last attempt

The previous attempt had problems:

1. Bookkeeping visibility: give every scratch attribute visibility `none` (table) or `ally` (player) so it is never printed. This covers act_choice, draw_choice, last_discard, per-column score scratch values like sc_r, and the embargo choices until reveal. The discard-pile tops are information players are allowed to see, so show them another way:
   - Either keep each discard pile as a hidden list and publish its top through the turn announcement,
   - or keep red_top/green_top/blue_top public but start them, and reset them at hand-2 setup, with a non-empty placeholder such as "none" rather than an empty value. Update the placeholder whenever a card is discarded or taken.
2. Unused attributes: remove `positions` (it is not in the interface), or actually update it. Every attribute you keep must be changed by a step that runs.
3. Scoring scope: do end-of-hand scoring in a step that runs for each player, so `you` is defined. Any condition mentioning `you.red_col`, `you.sc_r`, etc. must sit in a per-player step or operation, not a table-level `when`.
   - Compute each column as: S = sum of numbers - column_offset; if S > 0 and the Wager is present, S = floor(S * wager_multiplier); add long_column_bonus if the column has at least long_column_threshold cards; if the opponent's embargo equals that colour and the score is positive, floor-divide by embargo_divisor.
   - Then subtract the penalties, set hand_score, and add it to total.
4. Parameters: keep every parameter as an attribute.
5. Hand-2 setup: rebuild it from the recorded match order, with seats swapped.
