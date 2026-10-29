# 07 coder

- time: 2026-10-28T04:45:05+00:00 (163.6s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 342fdf20714d91a8, reply sha256 533116785ac17336

## Sent

````
# Task: write the XColos game file for "Speicherstadt Queues (Even Rotation)"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 4; set `meta.players` to {"min": 3, "max": 4, "suggested": 4} (the suggested size is the one the game plays best at).

SETUP: There are 6 colours: Red, Blue, Green, Yellow, Purple, Orange. The deck has 36 cards, 6 of each colour, shuffled once at the start. Each player is privately dealt a different contract colour, drawn at random from the 6 without repetition. No one else learns it. Each player starts with 6 coins and no goods. Players are numbered 1 to N (N = 3 or 4) in seating order.

The game lasts exactly 12 rounds. Each round:
1. SUPPLY: Reveal the top 3 cards of the deck as Lot 1, Lot 2 and Lot 3. Each lot is one good of the card's colour.
2. INCOME: Every player gains 2 coins.
3. PRIORITY: This round's priority order starts with player ((round - 1) mod N) + 1 and continues in seat order, wrapping around from N back to 1. It is announced. Over the 12 rounds every player holds each position in the priority order exactly 12/N times.
4. TALK: Everyone writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Messages are not binding and may be false.
5. QUEUE (secret, simultaneous): Each player submits three whole numbers, one per lot, each from 0 to 6.
   - A 0 means no worker on that lot.
   - A positive number places a worker there, and that number is the highest price the player will pay for that lot.
   - Each player has 2 workers, so at most 2 of the 3 numbers may be positive. If more than 2 are positive, only the positive entries on the two lowest-numbered lots count, and the rest become 0.
6. RESOLVE Lot 1, then Lot 2, then Lot 3:
   - The queue for a lot is every player with a positive number on it, ordered by this round's priority order. Let k be the queue length.
   - The offer starts at price k and goes to the first player in the queue.
   - If that player's limit is at least the current price and they hold at least that many coins, they pay that many coins to the bank and take the good.
   - Otherwise they decline, the price drops by 1, and the offer passes to the next player in the queue. The k-th player is therefore offered price 1.
   - If nobody buys, the card is discarded. A lot with an empty queue is discarded.
   - Coins spent on an earlier lot this round count when checking later lots.
7. ANNOUNCE: For each lot, announce which players queued, who bought it (if anyone) and the price paid. Limits are never revealed. Every player's coins and goods held (with colours) are public at all times.
8. END CHECK: After round 12 the deck is empty and the game ends.

FINAL SCORING: Each player's score is their coins, plus 5 points for each good of their own contract colour, plus 2 points for each good of any other colour. All contract colours are then revealed.

How the winner is decided: The player with the highest final score wins. If several tie for highest, the tied player with more goods of their own contract colour wins. If they are still tied, the game is a draw among them. If all players finish equal on both measures, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Speicherstadt Queues (Even Rotation) (3 to 4 players, best with 4)

Over 12 rounds, 3-4 merchants secretly queue workers on three goods lots each round and buy through a falling-price offer that runs in a rotating priority order, trying to collect their hidden contract colour.

STATE (every item below must exist in the file):
  - each player: seat (number, starts 'seat number 1..N in seating order'); everyone sees it. the player's position in seating order
  - each player: coins (number, starts 6); everyone sees it. coins held; public at all times
  - each player: goods (list, starts []); everyone sees it. goods bought, as colour names; public at all times
  - each player: contract (text, starts 'dealt at setup'); only its owner sees it. secret contract colour, different for each player; revealed to all at game end
  - each player: own_goods (number, starts 0); only its owner sees it. number of goods held that match the player's own contract colour
  - each player: limit1 (number, starts 0); only its owner sees it. this round's secret limit on Lot 1 (0 means no worker)
  - each player: limit2 (number, starts 0); only its owner sees it. this round's secret limit on Lot 2
  - each player: limit3 (number, starts 0); only its owner sees it. this round's secret limit on Lot 3
  - each player: score (number, starts 0); everyone sees it. final score: coins + 5 per own-contract good + 2 per other good, set at game end
  - the table: deck (list, starts '36 cards: 6 each of Red, Blue, Green, Yellow, Purple, Orange'); hidden from all players. the shuffled supply deck
  - the table: contract_pool (list, starts ['Red', 'Blue', 'Green', 'Yellow', 'Purple', 'Orange']); hidden from all players. contract colours not yet dealt
  - the table: discard (list, starts []); everyone sees it. lots that nobody bought
  - the table: round (number, starts 0); everyone sees it. current round number, 1..12
  - the table: lot1 (text, starts ''); everyone sees it. colour of this round's Lot 1
  - the table: lot2 (text, starts ''); everyone sees it. colour of this round's Lot 2
  - the table: lot3 (text, starts ''); everyone sees it. colour of this round's Lot 3
  - the table: priority_start (number, starts 1); everyone sees it. seat first in this round's priority order: ((round - 1) mod N) + 1
  - the table: queue_len (number, starts 0); everyone sees it. k, the number of players queued on the lot being resolved
  - the table: offer_price (number, starts 0); everyone sees it. current offer price on the lot being resolved
  - the table: lot_sold (bool, starts False); everyone sees it. whether the lot being resolved has been bought
  - parameters, each kept as a table attribute: colours = 6, cards_per_colour = 6, deck_size = 36, rounds = 12, lots_per_round = 3, starting_coins = 6, income_per_round = 2, workers_per_player = 2, limit_min = 0, limit_max = 6, lowest_offer_price = 1, price_drop_per_decline = 1, contract_good_points = 5, other_good_points = 2, coin_points = 1, tiebreak_multiplier = 100

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seats are numbered 1 to N (N = 3 or 4) in seating order.
  2. The deck is filled with 36 cards (6 each of Red, Blue, Green, Yellow, Purple, Orange) and shuffled once.
  3. Each player is privately dealt a contract colour: one colour is drawn at random from contract_pool into that player's contract and removed from contract_pool, so no two players share a colour. No one else learns it.
  4. Each player starts with coins = 6, goods = [], own_goods = 0.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] table. What happens: round += 1; draw three cards at random from deck into lot1, lot2 and lot3, removing each from deck; announce the three lot colours.
  2. [update] all players. What happens: every player's coins += 2.
  3. [update] table. What happens: priority_start = ((round - 1) mod N) + 1; announce the priority order: priority_start, then the following seats in seat order, wrapping from N to 1.
  4. [poll] all players answers: one short text message (not binding, may be false). What happens: after all are in, broadcast {"to": "all", "text": "Seat {seat} says: {value}"}.
  5. [poll] all players answers: a whole number from 0 to 6: your limit on Lot 1 (0 = no worker). What happens: set each player's limit1; answers are never revealed.
  6. [poll] all players answers: a whole number from 0 to 6: your limit on Lot 2 (0 = no worker). What happens: set each player's limit2; answers are never revealed.
  7. [poll] all players answers: a whole number from 0 to 6: your limit on Lot 3 (0 = no worker). What happens: set each player's limit3; answers are never revealed.
  8. [update] all players. What happens: worker cap of 2: for each player, if limit1 > 0 and limit2 > 0 and limit3 > 0, then limit3 = 0.
  9. [update] table. What happens: resolve Lot 1, setup: queue_len = count of players with limit1 > 0; offer_price = queue_len; lot_sold = false.
  10. [update] each player in priority order (positions 1..N, starting at priority_start). What happens: resolve Lot 1, offers (one step per priority position): when lot_sold is false and this player's limit1 > 0, then if limit1 >= offer_price and coins >= offer_price, the player's coins -= offer_price, lot1 is appended to the player's goods, own_goods += 1 if lot1 == contract, and lot_sold = true; otherwise offer_price -= 1. Players with limit1 = 0 are skipped.
  11. [update] table. What happens: when lot_sold is false, append lot1 to discard (this covers an empty queue too).
  12. [update] table. What happens: resolve Lot 2, setup: queue_len = count of players with limit2 > 0; offer_price = queue_len; lot_sold = false.
  13. [update] each player in priority order (positions 1..N, starting at priority_start). What happens: resolve Lot 2, offers: the same as Lot 1, using limit2 and lot2; coins spent on Lot 1 this round count in the coins check.
  14. [update] table. What happens: when lot_sold is false, append lot2 to discard.
  15. [update] table. What happens: resolve Lot 3, setup: queue_len = count of players with limit3 > 0; offer_price = queue_len; lot_sold = false.
  16. [update] each player in priority order (positions 1..N, starting at priority_start). What happens: resolve Lot 3, offers: the same as Lot 1, using limit3 and lot3; coins spent earlier this round count in the coins check.
  17. [update] table. What happens: when lot_sold is false, append lot3 to discard.
  18. [tell] all players. What happens: announce, for each lot, which seats queued (a positive limit), who bought it if anyone, and the price paid; also every player's coins and goods. Limits are not revealed.
  19. [update] all players. What happens: when round == 12: score = coins + 5 * own_goods + 2 * (length(goods) - own_goods); reveal every player's contract to all.
  20. [check] table. What happens: end the game if round >= 12 (the deck is then empty); otherwise continue to the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. At setup the deck holds 36 cards, 6 of each of the 6 colours, and each player gets a different secret contract colour drawn from the 6.
  R2. At setup every player has 6 coins and no goods.
  R3. Each round, 3 cards are drawn from the deck as Lot 1, Lot 2 and Lot 3, so after 12 rounds the deck is empty.
  R4. Each round, every player gains 2 coins before queuing.
  R5. In round r the priority order starts with seat ((r - 1) mod N) + 1 and continues in seat order, wrapping from N to 1; with N = 4, round 1 starts at seat 1, round 2 at seat 2 and round 5 at seat 1.
  R6. Each round every player sends one short message at the same time, and all messages are shown to everyone after all are in.
  R7. Each player submits a limit from 0 to 6 for each lot; 0 means no worker on that lot.
  R8. When a player submits positive limits on all three lots, their Lot 3 limit is set to 0, so at most 2 workers are placed.
  R9. The first offer on a lot is at price k, the number of players queued on it, and goes to the earliest queued player in priority order.
  R10. When an offered player's limit is at least the price and they hold at least that many coins, they pay the price to the bank and take the good.
  R11. When an offered player's limit is below the price or their coins are below it, the price drops by 1 and the offer passes to the next queued player, so the k-th queued player is offered price 1.
  R12. When nobody in the queue buys, or nobody queued, the lot is discarded.
  R13. Lots resolve in the order 1, 2, 3, and coins spent on an earlier lot reduce the coins checked for later lots.
  R14. After each round, the queuers, the buyer and the price of each lot are announced; limits are never revealed; coins and goods are public at all times.
  R15. The game ends after round 12.
  R16. Final score = coins + 5 per good of the player's own contract colour + 2 per good of any other colour; for example, 10 coins with 2 own-colour goods and 3 other goods scores 26.
  R17. At game end all contract colours are revealed.
  R18. The highest score wins; a tie at the top is broken by more own-contract goods; players still tied share the win as a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Talk message | asked: every seat | options: any short text
  - Limit on Lot 1 | asked: every seat | options: whole number 0 to 6
  - Limit on Lot 2 | asked: every seat | options: whole number 0 to 6
  - Limit on Lot 3 | asked: every seat | options: whole number 0 to 6 (forced to 0 if Lot 1 and Lot 2 limits are both positive)

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round >= 12
  - each player's standing: you.score * 100 + you.own_goods (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Highest final score (coins + 5 per good of own contract colour + 2 per other good) wins. A tie is broken by more goods of own contract colour. Players still level share the win, which is a draw among them.
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

- each player: `coins` (number, visible: public, starts 6): coins held; public at all times
- each player: `goods` (list, visible: public, starts []): goods bought, as colour names; public at all times
- each player: `score` (number, visible: public, starts 0): final score: coins + 5 per own-contract good + 2 per other good, set at game end
- the table: `round` (number, visible: public, starts 0): current round number, 1..12
- parameters (each must be an attribute holding this value, never a number buried in a step): colours = 6, cards_per_colour = 6, deck_size = 36, rounds = 12, lots_per_round = 3, starting_coins = 6, income_per_round = 2, workers_per_player = 2, limit_min = 0, limit_max = 6, lowest_offer_price = 1, price_drop_per_decline = 1, contract_good_points = 5, other_good_points = 2, coin_points = 1, tiebreak_multiplier = 100
- the game ends with ONE ending whose `rank_by` is `you.score * 100 + you.own_goods`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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

````

## Reply

````
{
  "schema": 1,
  "meta": {
    "id": "speicherstadt_queues_even",
    "name": "Speicherstadt Queues (Even Rotation)",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 4
    },
    "blurb": "Twelve rounds of secret worker queues on three goods lots, bought through a falling-price offer in a rotating priority order, chasing a hidden contract colour."
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
        "key": "coins",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "goods",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "contract",
        "visible": "ally",
        "type": "text",
        "initial": "",
        "values": [
          "",
          "Red",
          "Blue",
          "Green",
          "Yellow",
          "Purple",
          "Orange"
        ]
      },
      {
        "key": "own_goods",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "limit1",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "limit2",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "limit3",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "score",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ],
    "game": [
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "contract_pool",
        "visible": "none",
        "type": "list",
        "initial": [
          "Red",
          "Blue",
          "Green",
          "Yellow",
          "Purple",
          "Orange"
        ]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "cur",
        "visible": "none",
        "type": "number",
        "initial": 1
      },
      {
        "key": "can_buy",
        "visible": "none",
        "type": "bool",
        "initial": false
      },
      {
        "key": "discard",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "lot1",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "lot2",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "lot3",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "priority_start",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "priority_order",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "queue_len",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "offer_price",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "lot_sold",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "q1",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "q2",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "q3",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "buyer1",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "buyer2",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "buyer3",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "price1",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "price2",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "price3",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "colours",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "cards_per_colour",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 36
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "lots_per_round",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "starting_coins",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "income_per_round",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "workers_per_player",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "limit_min",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "limit_max",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "lowest_offer_price",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "price_drop_per_decline",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "contract_good_points",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "other_good_points",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "coin_points",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "tiebreak_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 100
      }
    ]
  },
  "setup": [
    {
      "use": "tell",
      "label": "seats",
      "to": "all",
      "text": "Seats are numbered 1 to N in seating order. You are seat {seat}."
    },
    {
      "use": "update",
      "label": "fill the deck",
      "do": [
        {
          "set": {
            "key": "deck",
            "value": [
              "Red", "Red", "Red", "Red", "Red", "Red",
              "Blue", "Blue", "Blue", "Blue", "Blue", "Blue",
              "Green", "Green", "Green", "Green", "Green", "Green",
              "Yellow", "Yellow", "Yellow", "Yellow", "Yellow", "Yellow",
              "Purple", "Purple", "Purple", "Purple", "Purple", "Purple",
              "Orange", "Orange", "Orange", "Orange", "Orange", "Orange"
            ]
          }
        }
      ],
      "text": "The deck of {deck_size} cards ({cards_per_colour} of each of {colours} colours) is shuffled."
    },
    {
      "use": "update",
      "label": "deal contracts",
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "contract_pool[min(len(contract_pool) - 1, int(uniform(0, len(contract_pool))))]"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 1"
            },
            "key": "contract",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "contract_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "contract_pool[min(len(contract_pool) - 1, int(uniform(0, len(contract_pool))))]"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 2"
            },
            "key": "contract",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "contract_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "contract_pool[min(len(contract_pool) - 1, int(uniform(0, len(contract_pool))))]"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 3"
            },
            "key": "contract",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "contract_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "contract_pool[min(len(contract_pool) - 1, int(uniform(0, len(contract_pool))))]"
            },
            "if": {
              "calc": "len(players) >= 4"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 4"
            },
            "key": "contract",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "contract_pool",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 4"
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
      "text": "Each player has been dealt a secret contract colour."
    },
    {
      "use": "update",
      "label": "starting purses",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "coins",
            "value": {
              "calc": "starting_coins"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "goods",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "own_goods",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "sync",
      "label": "your start",
      "mode": "self",
      "to": "all",
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "supply",
      "label": "supply",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "key": "lot1",
            "value": {
              "calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "lot1"
            }
          }
        },
        {
          "set": {
            "key": "lot2",
            "value": {
              "calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "lot2"
            }
          }
        },
        {
          "set": {
            "key": "lot3",
            "value": {
              "calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "lot3"
            }
          }
        }
      ],
      "text": "Round {round} of {rounds}. Lot 1: {lot1}. Lot 2: {lot2}. Lot 3: {lot3}."
    },
    {
      "use": "update",
      "phase": "income",
      "label": "income",
      "do": [
        {
          "adjust": {
            "players": "all",
            "key": "coins",
            "value": {
              "calc": "income_per_round"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "limit1",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "limit2",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "limit3",
            "value": 0
          }
        }
      ],
      "text": "Every player gains {income_per_round} coins."
    },
    {
      "use": "update",
      "phase": "priority",
      "label": "priority",
      "do": [
        {
          "set": {
            "key": "priority_start",
            "value": {
              "calc": "(round - 1) % len(players) + 1"
            }
          }
        },
        {
          "set": {
            "key": "priority_order",
            "value": {
              "calc": "[p.seat for p in players if p.seat >= priority_start] + [p.seat for p in players if p.seat < priority_start]"
            }
          }
        }
      ],
      "text": "Priority order this round (seats): {priority_order}."
    },
    {
      "use": "poll",
      "phase": "talk",
      "label": "talk",
      "to": "acting",
      "answer": {
        "type": "text",
        "max_words": 40
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} says: {value}"
      },
      "text": "Write one short message to the table. Everyone writes at the same time; messages are not binding and may be false."
    },
    {
      "use": "poll",
      "phase": "queue",
      "label": "limit on lot 1",
      "to": "acting",
      "answer": {
        "type": "number",
        "min": {
          "calc": "limit_min"
        },
        "max": {
          "calc": "limit_max"
        }
      },
      "store": "limit1",
      "text": "Secret: your limit on Lot 1 ({lot1}), a whole number from {limit_min} to {limit_max}. 0 means no worker; a positive number places a worker and is the highest price you will pay. You have {workers_per_player} workers."
    },
    {
      "use": "poll",
      "phase": "queue",
      "label": "limit on lot 2",
      "to": "acting",
      "answer": {
        "type": "number",
        "min": {
          "calc": "limit_min"
        },
        "max": {
          "calc": "limit_max"
        }
      },
      "store": "limit2",
      "text": "Secret: your limit on Lot 2 ({lot2}), a whole number from {limit_min} to {limit_max}. 0 means no worker; a positive number places a worker and is the highest price you will pay."
    },
    {
      "use": "poll",
      "phase": "queue",
      "label": "limit on lot 3",
      "to": {
        "where": "count([you.limit1 > 0, you.limit2 > 0]) < workers_per_player"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "limit_min"
        },
        "max": {
          "calc": "limit_max"
        }
      },
      "store": "limit3",
      "text": "Secret: your limit on Lot 3 ({lot3}), a whole number from {limit_min} to {limit_max}. 0 means no worker; a positive number places a worker and is the highest price you will pay."
    },
    {
      "use": "update",
      "phase": "queue",
      "label": "worker cap",
      "do": [
        {
          "set": {
            "players": {
              "where": "count([you.limit1 > 0, you.limit2 > 0, you.limit3 > 0]) > workers_per_player"
            },
            "key": "limit3",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "lot 1 setup",
      "do": [
        {
          "set": {
            "key": "q1",
            "value": {
              "calc": "[s for s in priority_order if players[s - 1].limit1 > 0]"
            }
          }
        },
        {
          "set": {
            "key": "queue_len",
            "value": {
              "calc": "len(q1)"
            }
          }
        },
        {
          "set": {
            "key": "offer_price",
            "value": {
              "calc": "queue_len"
            }
          }
        },
        {
          "set": {
            "key": "lot_sold",
            "value": false
          }
        },
        {
          "set": {
            "key": "buyer1",
            "value": 0
          }
        },
        {
          "set": {
            "key": "price1",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "lot 1 offers",
      "do": [
        {"set": {"key": "cur", "value": {"calc": "(priority_start - 1 + 0) % len(players) + 1"}}},
        {"set": {"key": "can_buy", "value": {"calc": "not lot_sold and players[cur - 1].limit1 > 0 and players[cur - 1].limit1 >= offer_price and players[cur - 1].coins >= offer_price"}}},
        {"adjust": {"key": "offer_price", "value": {"calc": "-price_drop_per_decline"}, "if": {"calc": "not lot_sold and players[cur - 1].limit1 > 0 and not can_buy and offer_price > lowest_offer_price"}}},
        {"adjust": {"player": {"calc": "cur"}, "key": "coins", "value": {"calc": "-offer_price"}, "if": {"calc": "can_buy"}, "text": "Seat {player} buys Lot 1 ({lot1}) for {offer_price}."}},
        {"append": {"player": {"calc": "cur"}, "key": "goods", "value": {"calc": "lot1"}, "if": {"calc": "can_buy"}}},
        {"adjust": {"player": {"calc": "cur"}, "key": "own_goods", "value": 1, "if": {"calc": "can_buy and lot1 == players[cur - 1].contract"}}},
        {"set": {"key": "buyer1", "value": {"calc": "cur"}, "if": {"calc": "can_buy"}}},
        {"set": {"key": "price1", "value": {"calc": "offer_price"}, "if": {"calc": "can_buy"}}},
        {"set": {"key": "lot_sold", "value": true, "if": {"calc": "can_buy"}}},

        {"set": {"key": "cur", "value": {"calc": "(priority_start - 1 + 1) % len(players) + 1"}}},
        {"set": {"key": "can_buy", "value": {"calc": "not lot_sold and players[cur - 1].limit1 > 0 and players[cur - 1].limit1 >= offer_price and players[cur - 1].coins >= offer_price"}}},
        {"adjust": {"key": "offer_price", "value": {"calc": "-price_drop_per_decline"}, "if": {"calc": "not lot_sold and players[cur - 1].limit1 > 0 and not can_buy and offer_price > lowest_offer_price"}}},
        {"adjust": {"player": {"calc": "cur"}, "key": "coins", "value": {"calc": "-offer_price"}, "if": {"calc": "can_buy"}, "text": "Seat {player} buys Lot 1 ({lot1}) for {offer_price}."}},
        {"append": {"player": {"calc": "cur"}, "key": "goods", "value": {"calc": "lot1"}, "if": {"calc": "can_buy"}}},
        {"adjust": {"player": {"calc": "cur"}, "key": "own_goods", "value": 1, "if": {"calc": "can_buy and lot1 == players[cur - 1].contract"}}},
        {"set": {"key": "buyer1", "value": {"calc": "cur"}, "if": {"calc": "can_buy"}}},
        {"set": {"key": "price1", "value": {"calc": "offer_price"}, "if": {"calc": "can_buy"}}},
        {"set": {"key": "lot_sold", "value": true, "if": {"calc": "can_buy"}}},

        {"set": {"key": "cur", "value": {"calc": "(priority_start - 1 + 2) % len(players) + 1"}}},
        {"set": {"key": "can_buy", "value": {"calc": "not lot_sold and players[cur - 1].limit1 > 0 and players[cur - 1].limit1 >= offer_price and players[cur - 1].coins >= offer_price"}}},
        {"adjust": {"key": "offer_price", "value": {"calc": "-price_drop_per_decline"}, "if": {"calc": "not lot_sold and players[cur - 1].limit1 > 0 and not can_buy and offer_price > lowest_offer_price"}}},
        {"adjust": {"player": {"calc": "cur"}, "key": "coins", "value": {"calc": "-offer_price"}, "if": {"calc": "can_buy"}, "text": "Seat {player} buys Lot 1 ({lot1}) for {offer_price}."}},
        {"append": {"player": {"calc": "cur"}, "key": "goods", "value": {"calc": "lot1"}, "if": {"calc": "can_buy"}}},
        {"adjust": {"player": {"calc": "cur"}, "key": "own_goods", "value": 1, "if": {"calc": "can_buy and lot1 == players[cur - 1].contract"}}},
        {"set": {"key": "buyer1", "value": {"calc": "cur"}, "if": {"calc": "can_buy"}}},
        {"set": {"key": "price1", "value": {"calc": "offer_price"}, "if": {"calc": "can_buy"}}},
        {"set": {"key": "lot_sold", "value": true, "if": {"calc": "can_buy"}}},

        {"set": {"key": "cur", "value": {"calc": "(priority_start - 1 + 3) % len(players) + 1"}}},
        {"set": {"key": "can_buy", "value": {"calc": "len(players) > 3 and not lot_sold and players[cur - 1].limit1 > 0 and players[cur - 1].limit1 >= offer_price and players[cur - 1].coins >= offer_price"}}},
        {"adjust": {"key": "offer_price", "value": {"calc": "-price_drop_per_decline"}, "if": {"calc": "len(players) > 3 and not lot_sold and players[cur - 1].limit1 > 0 and not can_buy and offer_price > lowest_offer_price"}}},
        {"adjust": {"player": {"calc": "cur"}, "key": "coins", "value": {"calc": "-offer_price"}, "if": {"calc": "can_buy"}, "text": "Seat {player} buys Lot 1 ({lot1}) for {offer_price}."}},
        {"append": {"player": {"calc": "cur"}, "key": "goods", "value": {"calc": "lot1"}, "if": {"calc": "can_buy"}}},
        {"adjust": {"player": {"calc": "cur"}, "key": "own_goods", "value": 1, "if": {"calc": "can_buy and lot1 == players[cur - 1].contract"}}},
        {"set": {"key": "buyer1", "value": {"calc": "cur"}, "if": {"calc": "can_buy"}}},
        {"set": {"key": "price1", "value": {"calc": "offer_price"}, "if": {"calc": "can_buy"}}},
        {"set": {"key": "lot_sold", "value": true, "if": {"calc": "can_buy"}}}
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "lot 1 discard",
      "when": {
        "calc": "not lot_sold"
      },
      "do": [
        {
          "append": {
            "key": "discard",
            "value": {
              "calc": "lot1"
            }
          }
        }
      ],
      "text": "Nobody bought Lot 1 ({lot1}); it is discarded."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "lot 2 setup",
      "do": [
        {
          "set": {
            "key": "q2",
            "value": {
              "calc": "[s for s in priority_order if players[s - 1].limit2 > 0]"
            }
          }
        },
        {
          "set": {
            "key": "queue_len",
            "value": {
              "calc": "len(q2)"
            }
          }
        },
        {
          "set": {
            "key": "offer_price",
            "value": {
              "calc": "queue_len"
            }
          }
        },
        {
          "set": {
            "key": "lot_sold",
            "value": false
          }
        },
        {
          "set": {
            "key": "buyer2",
            "value": 0
          }
        },
        {
          "set": {
            "key": "price2",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "lot 2 offers",
      "do": [
        {"set": {"key": "cur", "value": {"calc": "(priority_start - 1 + 0) % len(players) + 1"}}},
        {"set": {"key": "can_buy", "value": {"calc": "not lot_sold and players[cur - 1].limit2 > 0 and players[cur - 1].limit2 >= offer_price and players[cur - 1].coins >= offer_price"}}},
        {"adjust": {"key": "offer_price", "value": {"calc": "-price_drop_per_decline"}, "if": {"calc": "not lot_sold and players[cur - 1].limit2 > 0 and not can_buy and offer_price > lowest_offer_price"}}},
        {"adjust": {"player": {"calc": "cur"}, "key": "coins", "value": {"calc": "-offer_price"}, "if": {"calc": "can_buy"}, "text": "Seat {player} buys Lot 2 ({lot2}) for {offer_price}."}},
        {"append": {"player": {"calc": "cur"}, "key": "goods", "value": {"calc": "lot2"}, "if": {"calc": "can_buy"}}},
        {"adjust": {"player": {"calc": "cur"}, "key": "own_goods", "value": 1, "if": {"calc": "can_buy and lot2 == players[cur - 1].contract"}}},
        {"set": {"key": "buyer2", "value": {"calc": "cur"}, "if": {"calc": "can_buy"}}},
        {"set": {"key": "price2", "value": {"calc": "offer_price"}, "if": {"calc": "can_buy"}}},
        {"set": {"key": "lot_sold", "value": true, "if": {"calc": "can_buy"}}},

        {"set": {"key": "cur", "value": {"calc": "(priority_start - 1 + 1) % len(players) + 1"}}},
        {"set": {"key": "can_buy", "value": {"calc": "not lot_sold and players[cur - 1].limit2 > 0 and players[cur - 1].limit2 >= offer_price and players[cur - 1].coins >= offer_price"}}},
        {"adjust": {"key": "offer_price", "value": {"calc": "-price_drop_per_decline"}, "if": {"calc": "not lot_sold and players[cur - 1].limit2 > 0 and not can_buy and offer_price > lowest_offer_price"}}},
        {"adjust": {"player": {"calc": "cur"}, "key": "coins", "value": {"calc": "-offer_price"}, "if": {"calc": "can_buy"}, "text": "Seat {player} buys Lot 2 ({lot2}) for {offer_price}."}},
        {"append": {"player": {"calc": "cur"}, "key": "goods", "value": {"calc": "lot2"}, "if": {"calc": "can_buy"}}},
        {"adjust": {"player": {"calc": "cur"}, "key": "own_goods", "value": 1, "if": {"calc": "can_buy and lot2 == players[cur - 1].contract"}}},
        {"set": {"key": "buyer2", "value": {"calc": "cur"}, "if": {"calc": "can_buy"}}},
        {"set": {"key": "price2", "value": {"calc": "offer_price"}, "if": {"calc": "can_buy"}}},
        {"set": {"key": "lot_sold", "value": true, "if": {"calc": "can_buy"}}},

        {"set": {"key": "cur", "value": {"calc": "(priority_start - 1 + 2) % len(players) + 1"}}},
        {"set": {"key": "can_buy", "value": {"calc": "not lot_sold and players[cur - 1].limit2 > 0 and players[cur - 1].limit2 >= offer_price and players[cur - 1].coins >= offer_price"}}},
        {"adjust": {"key": "offer_price", "value": {"calc": "-price_drop_per_decline"}, "if": {"calc": "not lot_sold and players[cur - 1].limit2 > 0 and not can_buy and offer_price > lowest_offer_price"}}},
        {"adjust": {"player": {"calc": "cur"}, "key": "coins", "value": {"calc": "-offer_price"}, "if": {"calc": "can_buy"}, "text": "Seat {player} buys Lot 2 ({lot2}) for {offer_price}."}},
        {"append": {"player": {"calc": "cur"}, "key": "goods", "value": {"calc": "lot2"}, "if": {"calc": "can_buy"}}},
        {"adjust": {"player": {"calc": "cur"}, "key": "own_goods", "value": 1, "if": {"calc": "can_buy and lot2 == players[cur - 1].contract"}}},
        {"set": {"key": "buyer2", "value": {"calc": "cur"}, "if": {"calc": "can_buy"}}},
        {"set": {"key": "price2", "value": {"calc": "offer_price"}, "if": {"calc": "can_buy"}}},
        {"set": {"key": "lot_sold", "value": true, "if": {"calc": "can_buy"}}},

        {"set": {"key": "cur", "value": {"calc": "(priority_start - 1 + 3) % len(players) + 1"}}},
        {"set": {"key": "can_buy", "value": {"calc": "len(players) > 3 and not lot_sold and players[cur - 1].limit2 > 0 and players[cur - 1].limit2 >= offer_price and players[cur - 1].coins >= offer_price"}}},
        {"adjust": {"key": "offer_price", "value": {"calc": "-price_drop_per_decline"}, "if": {"calc": "len(players) > 3 and not lot_sold and players[cur - 1].limit2 > 0 and not can_buy and offer_price > lowest_offer_price"}}},
        {"adjust": {"player": {"calc": "cur"}, "key": "coins", "value": {"calc": "-offer_price"}, "if": {"calc": "can_buy"}, "text": "Seat {player} buys Lot 2 ({lot2}) for {offer_price}."}},
        {"append": {"player": {"calc": "cur"}, "key": "goods", "value": {"calc": "lot2"}, "if": {"calc": "can_buy"}}},
        {"adjust": {"player": {"calc": "cur"}, "key": "own_goods", "value": 1, "if": {"calc": "can_buy and lot2 == players[cur - 1].contract"}}},
        {"set": {"key": "buyer2", "value": {"calc": "cur"}, "if": {"calc": "can_buy"}}},
        {"set": {"key": "price2", "value": {"calc": "offer_price"}, "if": {"calc": "can_buy"}}},
        {"set": {"key": "lot_sold", "value": true, "if": {"calc": "can_buy"}}}
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "lot 2 discard",
      "when": {
        "calc": "not lot_sold"
      },
      "do": [
        {
          "append": {
            "key": "discard",
            "value": {
              "calc": "lot2"
            }
          }
        }
      ],
      "text": "Nobody bought Lot 2 ({lot2}); it is discarded."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "lot 3 setup",
      "do": [
        {
          "set": {
            "key": "q3",
            "value": {
              "calc": "[s for s in priority_order if players[s - 1].limit3 > 0]"
            }
          }
        },
        {
          "set": {
            "key": "queue_len",
            "value": {
              "calc": "len(q3)"
            }
          }
        },
        {
          "set": {
            "key": "offer_price",
            "value": {
              "calc": "queue_len"
            }
          }
        },
        {
          "set": {
            "key": "lot_sold",
            "value": false
          }
        },
        {
          "set": {
            "key": "buyer3",
            "value": 0
          }
        },
        {
          "set": {
            "key": "price3",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "lot 3 offers",
      "do": [
        {"set": {"key": "cur", "value": {"calc": "(priority_start - 1 + 0) % len(players) + 1"}}},
        {"set": {"key": "can_buy", "value": {"calc": "not lot_sold and players[cur - 1].limit3 > 0 and players[cur - 1].limit3 >= offer_price and players[cur - 1].coins >= offer_price"}}},
        {"adjust": {"key": "offer_price", "value": {"calc": "-price_drop_per_decline"}, "if": {"calc": "not lot_sold and players[cur - 1].limit3 > 0 and not can_buy and offer_price > lowest_offer_price"}}},
        {"adjust": {"player": {"calc": "cur"}, "key": "coins", "value": {"calc": "-offer_price"}, "if": {"calc": "can_buy"}, "text": "Seat {player} buys Lot 3 ({lot3}) for {offer_price}."}},
        {"append": {"player": {"calc": "cur"}, "key": "goods", "value": {"calc": "lot3"}, "if": {"calc": "can_buy"}}},
        {"adjust": {"player": {"calc": "cur"}, "key": "own_goods", "value": 1, "if": {"calc": "can_buy and lot3 == players[cur - 1].contract"}}},
        {"set": {"key": "buyer3", "value": {"calc": "cur"}, "if": {"calc": "can_buy"}}},
        {"set": {"key": "price3", "value": {"calc": "offer_price"}, "if": {"calc": "can_buy"}}},
        {"set": {"key": "lot_sold", "value": true, "if": {"calc": "can_buy"}}},

        {"set": {"key": "cur", "value": {"calc": "(priority_start - 1 + 1) % len(players) + 1"}}},
        {"set": {"key": "can_buy", "value": {"calc": "not lot_sold and players[cur - 1].limit3 > 0 and players[cur - 1].limit3 >= offer_price and players[cur - 1].coins >= offer_price"}}},
        {"adjust": {"key": "offer_price", "value": {"calc": "-price_drop_per_decline"}, "if": {"calc": "not lot_sold and players[cur - 1].limit3 > 0 and not can_buy and offer_price > lowest_offer_price"}}},
        {"adjust": {"player": {"calc": "cur"}, "key": "coins", "value": {"calc": "-offer_price"}, "if": {"calc": "can_buy"}, "text": "Seat {player} buys Lot 3 ({lot3}) for {offer_price}."}},
        {"append": {"player": {"calc": "cur"}, "key": "goods", "value": {"calc": "lot3"}, "if": {"calc": "can_buy"}}},
        {"adjust": {"player": {"calc": "cur"}, "key": "own_goods", "value": 1, "if": {"calc": "can_buy and lot3 == players[cur - 1].contract"}}},
        {"set": {"key": "buyer3", "value": {"calc": "cur"}, "if": {"calc": "can_buy"}}},
        {"set": {"key": "price3", "value": {"calc": "offer_price"}, "if": {"calc": "can_buy"}}},
        {"set": {"key": "lot_sold", "value": true, "if": {"calc": "can_buy"}}},

        {"set": {"key": "cur", "value": {"calc": "(priority_start - 1 + 2) % len(players) + 1"}}},
        {"set": {"key": "can_buy", "value": {"calc": "not lot_sold and players[cur - 1].limit3 > 0 and players[cur - 1].limit3 >= offer_price and players[cur - 1].coins >= offer_price"}}},
        {"adjust": {"key": "offer_price", "value": {"calc": "-price_drop_per_decline"}, "if": {"calc": "not lot_sold and players[cur - 1].limit3 > 0 and not can_buy and offer_price > lowest_offer_price"}}},
        {"adjust": {"player": {"calc": "cur"}, "key": "coins", "value": {"calc": "-offer_price"}, "if": {"calc": "can_buy"}, "text": "Seat {player} buys Lot 3 ({lot3}) for {offer_price}."}},
        {"append": {"player": {"calc": "cur"}, "key": "goods", "value": {"calc": "lot3"}, "if": {"calc": "can_buy"}}},
        {"adjust": {"player": {"calc": "cur"}, "key": "own_goods", "value": 1, "if": {"calc": "can_buy and lot3 == players[cur - 1].contract"}}},
        {"set": {"key": "buyer3", "value": {"calc": "cur"}, "if": {"calc": "can_buy"}}},
        {"set": {"key": "price3", "value": {"calc": "offer_price"}, "if": {"calc": "can_buy"}}},
        {"set": {"key": "lot_sold", "value": true, "if": {"calc": "can_buy"}}},

        {"set": {"key": "cur", "value": {"calc": "(priority_start - 1 + 3) % len(players) + 1"}}},
        {"set": {"key": "can_buy", "value": {"calc": "len(players) > 3 and not lot_sold and players[cur - 1].limit3 > 0 and players[cur - 1].limit3 >= offer_price and players[cur - 1].coins >= offer_price"}}},
        {"adjust": {"key": "offer_price", "value": {"calc": "-price_drop_per_decline"}, "if": {"calc": "len(players) > 3 and not lot_sold and players[cur - 1].limit3 > 0 and not can_buy and offer_price > lowest_offer_price"}}},
        {"adjust": {"player": {"calc": "cur"}, "key": "coins", "value": {"calc": "-offer_price"}, "if": {"calc": "can_buy"}, "text": "Seat {player} buys Lot 3 ({lot3}) for {offer_price}."}},
        {"append": {"player": {"calc": "cur"}, "key": "goods", "value": {"calc": "lot3"}, "if": {"calc": "can_buy"}}},
        {"adjust": {"player": {"calc": "cur"}, "key": "own_goods", "value": 1, "if": {"calc": "can_buy and lot3 == players[cur - 1].contract"}}},
        {"set": {"key": "buyer3", "value": {"calc": "cur"}, "if": {"calc": "can_buy"}}},
        {"set": {"key": "price3", "value": {"calc": "offer_price"}, "if": {"calc": "can_buy"}}},
        {"set": {"key": "lot_sold", "value": true, "if": {"calc": "can_buy"}}}
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "lot 3 discard",
      "when": {
        "calc": "not lot_sold"
      },
      "do": [
        {
          "append": {
            "key": "discard",
            "value": {
              "calc": "lot3"
            }
          }
        }
      ],
      "text": "Nobody bought Lot 3 ({lot3}); it is discarded."
    },
    {
      "use": "tell",
      "phase": "announce",
      "label": "round report",
      "to": "all",
      "text": "Round {round} results. Lot 1 ({lot1}): queued seats {q1}; bought by seat {buyer1} for {price1}. Lot 2 ({lot2}): queued seats {q2}; bought by seat {buyer2} for {price2}. Lot 3 ({lot3}): queued seats {q3}; bought by seat {buyer3} for {price3}. (Seat 0 means nobody bought it and it was discarded.) Coins and goods [seat, coins, goods]: {[[p.seat, p.coins, p.goods] for p in players]}."
    },
    {
      "use": "update",
      "phase": "scoring",
      "label": "final scoring",
      "when": {
        "calc": "round >= rounds"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "you.coins * coin_points + contract_good_points * you.own_goods + other_good_points * (len(you.goods) - you.own_goods)"
            }
          }
        }
      ],
      "text": "Final scoring. Contracts revealed [seat, contract, score]: {[[p.seat, p.contract, p.score] for p in players]}."
    },
    {
      "use": "check",
      "phase": "end",
      "label": "after round 12",
      "when": {
        "calc": "round >= rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round >= rounds"
      },
      "rank_by": "you.score * 100 + you.own_goods",
      "reveal": [
        "contract"
      ],
      "text": "Winner: {result}. Final [seat, score, own-contract goods]: {[[p.seat, p.score, p.own_goods] for p in players]}."
    }
  },
  "limits": {
    "rounds": 12,
    "rounds_max": 13,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "SETUP: There are {colours} colours: Red, Blue, Green, Yellow, Purple, Orange. The deck has {deck_size} cards, {cards_per_colour} of each colour, shuffled once at the start. Each player is privately dealt a different contract colour, drawn at random from the {colours} without repetition. No one else learns it. Each player starts with {starting_coins} coins and no goods. Players are numbered 1 to N (N = 3 or 4) in seating order.\n\nThe game lasts exactly {rounds} rounds. Each round:\n1. SUPPLY: Reveal the top {lots_per_round} cards of the deck as Lot 1, Lot 2 and Lot 3. Each lot is one good of the card's colour.\n2. INCOME: Every player gains {income_per_round} coins.\n3. PRIORITY: This round's priority order starts with player ((round - 1) mod N) + 1 and continues in seat order, wrapping around from N back to 1. It is announced. Over the {rounds} rounds every player holds each position in the priority order exactly 12/N times.\n4. TALK: Everyone writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Messages are not binding and may be false.\n5. QUEUE (secret, simultaneous): Each player submits three whole numbers, one per lot, each from {limit_min} to {limit_max}. A 0 means no worker on that lot. A positive number places a worker there, and that number is the highest price the player will pay for that lot. Each player has {workers_per_player} workers, so at most {workers_per_player} of the 3 numbers may be positive. If more than {workers_per_player} are positive, only the positive entries on the two lowest-numbered lots count, and the rest become 0 (if your Lot 1 and Lot 2 limits are both positive, you are not asked for Lot 3 and it is 0).\n6. RESOLVE Lot 1, then Lot 2, then Lot 3: The queue for a lot is every player with a positive number on it, ordered by this round's priority order. Let k be the queue length. The offer starts at price k and goes to the first player in the queue. If that player's limit is at least the current price and they hold at least that many coins, they pay that many coins to the bank and take the good. Otherwise they decline, the price drops by {price_drop_per_decline}, and the offer passes to the next player in the queue. The k-th player is therefore offered price {lowest_offer_price}. If nobody buys, the card is discarded. A lot with an empty queue is discarded. Coins spent on an earlier lot this round count when checking later lots.\n7. ANNOUNCE: For each lot, announce which players queued, who bought it (if anyone) and the price paid. Limits are never revealed. Every player's coins and goods held (with colours) are public at all times.\n8. END CHECK: After round {rounds} the deck is empty and the game ends.\n\nFINAL SCORING: Each player's score is their coins, plus {contract_good_points} points for each good of their own contract colour, plus {other_good_points} points for each good of any other colour. All contract colours are then revealed.\n\nThe player with the highest final score wins. If several tie for highest, the tied player with more goods of their own contract colour wins. If they are still tied, the game is a draw among them, and they share the win."
}
````
