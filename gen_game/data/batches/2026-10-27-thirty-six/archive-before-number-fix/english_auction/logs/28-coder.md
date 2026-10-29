# 28 coder

- time: 2026-10-27T17:03:04+00:00 (42.7s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 fdf9e39811161a6d, reply sha256 6494e16d2eb2e567

## Sent

````
# Task: write the XColos game file for "Budgeted English Auction with Activity Rule"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 6; set `meta.players` to {"min": 3, "max": 6, "suggested": 4} (the suggested size is the one the game plays best at).

R1 Setup. There are N players (3 to 6). Each player starts with budget 30, score 0 and spent 0. Before round 1, each player whose values list is empty receives a private values list: a random ordering of [3,5,7,9,11,13], so every list sums to 48. A list that is already set is never overwritten. Table state starts at standing_bid 0, leader 0 (0 means no leader) and last_price 0.
R2 Privacy. A player's values list is visible only to that player. Everyone sees all budgets, scores, eligibility flags, standing_bid, leader and last_price. Everyone knows the value set is {3,5,7,9,11,13}.
R3 Items. The game has 6 rounds. In round r, item r is sold. A player's value for item r is entry r of their own list, counting from 1.
R4 Talk. At the start of each round, every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Messages bind nobody.
R5 Round reset. After talk, set standing_bid to 0 and leader to 0, and mark every player eligible.
R6 Bidding turns. Each round has exactly 3 bidding turns. Each turn is a simultaneous poll of all players. Each player answers pass (0) or a whole number from 1 up to their current budget.
R7 Validity. A bid is valid only if all three conditions hold:
(a) the bidder is eligible for this turn;
(b) the bid is at least standing_bid + 1 (in turn 1 that means at least 1);
(c) the bid is at most the bidder's budget.
Pass, and any bid that is not valid, counts as no bid.
R8 Turn result. Find the highest valid bid.
- If exactly one player made it, standing_bid becomes that amount and leader becomes that player.
- If two or more players made it (a tie), or nobody made a valid bid, standing_bid and leader stay unchanged.
- A lower valid bid never wins.
R9 Eligibility. After each turn, a player is eligible for the next turn only if they made a valid bid in this turn (winning, tied or beaten), or they are the leader after this turn. Everyone else is marked ineligible for the rest of the round. After each turn, standing_bid, leader and all eligibility flags are announced.
R10 Resolution. After turn 3:
- If leader is not 0, the leader's budget decreases by standing_bid, their spent increases by standing_bid, and their score increases by (their value for item r) minus standing_bid. This can be negative.
- last_price is set to standing_bid. If leader is 0, the item goes unsold and last_price is 0.
- The round's result is announced.
R11 End. After round 6 the game ends. Unspent budget is worth nothing.

How the winner is decided: After round 6, the player with the strictly highest score wins. If two or more players share the highest score, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Budgeted English Auction with Activity Rule (3 to 6 players, best with 4)

Six items are auctioned one per round. In each round there are three simultaneous sealed bidding turns, and a player who stops bidding drops out of that item. Each player has a budget of 30 and private values, and the highest score (value minus price, summed) wins.

STATE (every item below must exist in the file):
  - each player: budget (number, starts 30); everyone sees it. Money left to bid with. Unspent budget is worth nothing at the end.
  - each player: score (number, starts 0); everyone sees it. Sum of (value minus price paid) over the items won. It can be negative.
  - each player: spent (number, starts 0); everyone sees it. Total paid for the items won.
  - each player: values (list, starts []); only its owner sees it. Private values. Entry r (counting from 1) is this player's value for item r. It is a random ordering of [3,5,7,9,11,13].
  - each player: eligible (bool, starts True); everyone sees it. Whether this player may make a valid bid in the current bidding turn.
  - each player: bid (number, starts 0); only its owner sees it. This player's answer in the current bidding turn (0 = pass).
  - each player: valid_bid (bool, starts False); everyone sees it. Whether this player's bid in the current turn met all three validity conditions.
  - the table: round (number, starts 0); everyone sees it. Current round. Item r is sold in round r.
  - the table: turn (number, starts 0); everyone sees it. Current bidding turn within the round (1 to 3).
  - the table: standing_bid (number, starts 0); everyone sees it. The current highest uniquely-made valid bid on this round's item.
  - the table: leader (number, starts 0); everyone sees it. Seat number of the player holding the standing bid (0 = no leader).
  - the table: last_price (number, starts 0); everyone sees it. Price of the last item sold (0 if it went unsold).
  - the table: value_set (list, starts [3, 5, 7, 9, 11, 13]); everyone sees it. The public set of values that every private list is an ordering of.
  - the table: top_bid (number, starts 0); hidden from all players. Scratch: the highest valid bid in the current turn (0 if none).
  - the table: top_count (number, starts 0); hidden from all players. Scratch: how many players made top_bid as a valid bid this turn.
  - parameters, each kept as a table attribute: starting_budget = 30, starting_score = 0, starting_spent = 0, rounds = 6, items = 6, bidding_turns_per_round = 3, value_1 = 3, value_2 = 5, value_3 = 7, value_4 = 9, value_5 = 11, value_6 = 13, values_sum = 48, min_first_bid = 1, min_raise = 1, pass_bid = 0, no_leader_code = 0

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Every player starts with budget 30, score 0 and spent 0.
  2. Each player whose values list is empty receives a random ordering of [3,5,7,9,11,13] as their private values list, visible only to them. A list that is already set is never overwritten.
  3. The table starts with round 0, standing_bid 0, leader 0 (no leader) and last_price 0.
  4. Everyone is told that the value set is {3,5,7,9,11,13}, that each list sums to 48, and that there are 6 rounds with 3 bidding turns each.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round += 1. Announce that item {round} is now for sale.
  2. [poll] all players answers: one short text message. What happens: Every message is broadcast to all players as 'Seat {seat} says: {value}'. Messages bind nobody.
  3. [update] all players. What happens: standing_bid = 0; leader = 0; turn = 0; every player's eligible = true; every player's valid_bid = false.
  4. [update] all players. What happens: turn += 1.
  5. [poll] all players answers: a whole number from 0 (pass) to the player's current budget. What happens: Each player's answer is stored in their bid. Nobody sees any bid until all are in.
  6. [update] all players. What happens: For each player: valid_bid = (eligible == true AND bid >= standing_bid + 1 AND bid <= budget AND bid >= 1).
  7. [update] all players. What happens: top_bid = the maximum bid among players with valid_bid true (0 if none). top_count = the number of players with valid_bid true AND bid == top_bid.
  8. [update] all players. What happens: If top_count == 1 and top_bid >= 1: standing_bid = top_bid and leader = the seat of that player. Otherwise (a tie or no valid bid), standing_bid and leader are unchanged.
  9. [update] all players. What happens: For each player: eligible = (valid_bid == true OR seat == leader). Announce standing_bid, leader and every player's eligible flag.
  10. [repeat] all players. What happens: Run the steps from 'turn += 1' through the eligibility update again until turn == 3.
  11. [update] all players. What happens: If leader != 0: the leader's budget -= standing_bid, spent += standing_bid, and score += values[round] - standing_bid. Set last_price = standing_bid if leader != 0, otherwise last_price = 0 (the item goes unsold). Announce the round's result: the item, the winner's seat or 'unsold', the price, and every budget and score.
  12. [check] all players. What happens: If round == 6, the game ends. Otherwise, start the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, then every player has budget 30, score 0 and spent 0, and the table has standing_bid 0, leader 0 and last_price 0.
  R2. When setup runs and a player's values list is empty, then that player receives a random ordering of [3,5,7,9,11,13], which sums to 48. When a list is already set, then it is not overwritten.
  R3. When values are dealt, then a player's values list is visible only to that player, while all budgets, scores, spent, eligibility flags, standing_bid, leader and last_price are public.
  R4. When round r is played (r from 1 to 6), then item r is sold, and a player's value for it is entry r of their own values list, counting from 1.
  R5. When a round starts, then every player writes one short message at the same time, and all messages are then shown to everyone. No message binds anyone.
  R6. When the talk phase of a round ends, then standing_bid becomes 0, leader becomes 0 and every player becomes eligible.
  R7. When a round is played, then it has exactly 3 bidding turns. In each turn, all players answer at the same time with 0 (pass) or a whole number from 1 to their current budget.
  R8. When a player bids, then the bid is valid only if the player is eligible, the bid is at least standing_bid + 1 (at least 1 in turn 1), and the bid is at most the player's budget. A pass or an invalid bid counts as no bid.
  R9. When exactly one player made the highest valid bid in a turn (for example a single bid of 6 against a bid of 4), then standing_bid becomes that amount and leader becomes that player's seat.
  R10. When two or more players tie on the highest valid bid (for example two bids of 6), or nobody made a valid bid, then standing_bid and leader stay unchanged. A lower valid bid never wins.
  R11. When a turn ends, then a player stays eligible for the next turn only if they made a valid bid in that turn (winning, tied or beaten) or they are the leader. Every other player is ineligible for the rest of the round.
  R12. When a turn ends, then standing_bid, leader and every eligibility flag are announced to all.
  R13. When turn 3 ends with leader not 0 and standing_bid p, then the leader's budget decreases by p, their spent increases by p, and their score increases by (their value for item r) minus p. This can be negative: value 3 at price 8 gives -5.
  R14. When turn 3 ends, then last_price is set to standing_bid if there is a leader, and to 0 if leader is 0 (the item goes unsold). The round's result is announced.
  R15. When round 6 has been resolved, then the game ends, and unspent budget is worth nothing.
  R16. When the game ends, then the player with the strictly highest score wins. If two or more players share the highest score, then they share the result (a draw).

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Talk message at the start of each round | asked: every seat | options: one short free-text message
  - Bid in each of the 3 bidding turns | asked: every seat, eligible or not (the poll goes to all players) | options: 0 (pass) or any whole number from 1 to that seat's current budget. A bid from an ineligible seat, or one below standing_bid + 1, is accepted as an answer but counts as no bid.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round == 6 (checked after round 6's resolution)
  - each player's standing: you.score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their score (the sum of value minus price over the items won). The highest score wins. Players level at the highest score share the result, which the source calls a draw.
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

- each player: `budget` (number, visible: public, starts 30): Money left to bid with. Unspent budget is worth nothing at the end.
- each player: `score` (number, visible: public, starts 0): Sum of (value minus price paid) over the items won. It can be negative.
- each player: `spent` (number, visible: public, starts 0): Total paid for the items won.
- the table: `round` (number, visible: public, starts 0): Current round. Item r is sold in round r.
- the table: `standing_bid` (number, visible: public, starts 0): The current highest uniquely-made valid bid on this round's item.
- the table: `leader` (number, visible: public, starts 0): Seat number of the player holding the standing bid (0 = no leader).
- the table: `last_price` (number, visible: public, starts 0): Price of the last item sold (0 if it went unsold).
- parameters (each must be an attribute holding this value, never a number buried in a step): starting_budget = 30, starting_score = 0, starting_spent = 0, rounds = 6, items = 6, bidding_turns_per_round = 3, value_1 = 3, value_2 = 5, value_3 = 7, value_4 = 9, value_5 = 11, value_6 = 13, values_sum = 48, min_first_bid = 1, min_raise = 1, pass_bid = 0, no_leader_code = 0
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

## Guidance from the last attempt

The previous attempt had problems:

Make each bidding turn a simultaneous poll of all players whose options are pass (pass_bid = 0) plus every whole number from min_first_bid (1) up to that player's current budget, built from the budget attribute and not hard-coded. Store each answer in the player's bid. Then apply R7 to decide validity: the player must be eligible, the bid must be at least standing_bid + min_raise, and it must not exceed budget. Compute top_bid and top_count over the valid bids, and set standing_bid and leader only when top_count == 1. Update eligibility per R9: valid bidders and the current leader stay eligible. After turn 3, apply R10: if leader != 0, take standing_bid from the leader's budget, add it to spent, add (values[round] - standing_bid) to score, and set last_price = standing_bid; otherwise set last_price = 0. Do the R5 reset (standing_bid 0, leader 0, all players eligible) at the start of each round, after the simultaneous talk step. Check this against the scenario 'seat 1 bids 4 on item 1 with values [13,...]', which should end with budget 26, score 9, spent 4, leader 1, standing_bid 4 and last_price 4.


YOUR PREVIOUS GAME FILE WAS REFUSED. Here it is:
```json
{
  "schema": 1,
  "meta": {
    "id": "budgeted_english_auction_activity_rule",
    "name": "Budgeted English Auction with Activity Rule",
    "players": {
      "min": 3,
      "max": 6,
      "suggested": 4
    },
    "blurb": "Six items, three sealed bidding turns each, a budget of 30 and private values: stop bidding and you drop out of the item."
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
        "key": "budget",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "spent",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "values",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "eligible",
        "visible": "public",
        "type": "bool",
        "initial": true
      },
      {
        "key": "bid",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "valid_bid",
        "visible": "public",
        "type": "bool",
        "initial": false
      }
    ],
    "game": [
      {
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "turn",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "standing_bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "leader",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "last_price",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "value_set",
        "visible": "public",
        "type": "list",
        "initial": [
          3,
          5,
          7,
          9,
          11,
          13
        ]
      },
      {
        "key": "top_bid",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "top_count",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "starting_budget",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "starting_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "starting_spent",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "items",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "bidding_turns_per_round",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "value_1",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "value_2",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "value_3",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "value_4",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "value_5",
        "visible": "public",
        "type": "number",
        "initial": 11
      },
      {
        "key": "value_6",
        "visible": "public",
        "type": "number",
        "initial": 13
      },
      {
        "key": "values_sum",
        "visible": "public",
        "type": "number",
        "initial": 48
      },
      {
        "key": "min_first_bid",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "min_raise",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "pass_bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "no_leader_code",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "starting purses",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "budget",
            "value": {
              "calc": "starting_budget"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "starting_score"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "spent",
            "value": {
              "calc": "starting_spent"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "deal private values",
      "do": [
        {
          "set": {
            "players": {
              "where": "len(you.values) == 0"
            },
            "key": "values",
            "value": {
              "calc": "[x[1] for x in sorted([[uniform(0, 1), v] for v in value_set])]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "the table starts",
      "do": [
        {
          "set": {
            "key": "round",
            "value": 0
          }
        },
        {
          "set": {
            "key": "standing_bid",
            "value": 0
          }
        },
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "no_leader_code"
            }
          }
        },
        {
          "set": {
            "key": "last_price",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "tell",
      "label": "the value set",
      "to": "all",
      "text": "Every private values list is an ordering of {value_set}, so each list sums to {values_sum}. There are {rounds} rounds with {bidding_turns_per_round} bidding turns each."
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
      "phase": "open",
      "label": "the next item",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        }
      ],
      "text": "Item {round} of {items} is now for sale. Your value for it is entry {round} of your values list."
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
      "text": "Item {round} is up. Write one short message to the table. Everyone writes at the same time; messages bind nobody."
    },
    {
      "use": "update",
      "phase": "talk",
      "label": "round reset",
      "do": [
        {
          "set": {
            "key": "standing_bid",
            "value": 0
          }
        },
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "no_leader_code"
            }
          }
        },
        {
          "set": {
            "key": "turn",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "eligible",
            "value": true
          }
        },
        {
          "set": {
            "players": "all",
            "key": "valid_bid",
            "value": false
          }
        }
      ],
      "text": "Bidding on item {round} opens: standing bid 0, no leader, everyone eligible."
    },
    {
      "use": "repeat",
      "phase": "bidding",
      "label": "the bidding turns",
      "until": {
        "calc": "turn >= bidding_turns_per_round"
      },
      "max": 4,
      "steps": [
        {
          "use": "update",
          "phase": "bidding",
          "label": "next turn",
          "do": [
            {
              "adjust": {
                "key": "turn",
                "value": 1
              }
            },
            {
              "set": {
                "players": "all",
                "key": "bid",
                "value": {
                  "calc": "pass_bid"
                }
              }
            }
          ]
        },
        {
          "use": "poll",
          "phase": "bidding",
          "label": "bid",
          "to": "acting",
          "answer": {
            "type": "number",
            "min": {
              "calc": "pass_bid"
            },
            "max": {
              "calc": "you.budget"
            }
          },
          "store": "bid",
          "text": "Item {round}, bidding turn {turn} of {bidding_turns_per_round}. Standing bid {standing_bid}, leader seat {leader} (0 = none). Answer {pass_bid} to pass, or a whole number from {min_first_bid} up to your current budget. Your bid is valid only if you are eligible this turn and it is at least the standing bid + {min_raise}; otherwise it counts as no bid."
        },
        {
          "use": "update",
          "phase": "bidding",
          "label": "validity",
          "do": [
            {
              "set": {
                "players": "all",
                "key": "valid_bid",
                "value": {
                  "calc": "you.eligible and you.bid >= standing_bid + min_raise and you.bid <= you.budget and you.bid >= min_first_bid"
                }
              }
            }
          ]
        },
        {
          "use": "update",
          "phase": "bidding",
          "label": "top bid",
          "do": [
            {
              "set": {
                "key": "top_bid",
                "value": {
                  "calc": "max([p.bid for p in players if p.valid_bid] + [0])"
                }
              }
            },
            {
              "set": {
                "key": "top_count",
                "value": {
                  "calc": "count(p.valid_bid and p.bid == top_bid for p in players)"
                }
              }
            }
          ]
        },
        {
          "use": "update",
          "phase": "bidding",
          "label": "turn result",
          "do": [
            {
              "set": {
                "key": "leader",
                "value": {
                  "calc": "min([p.seat for p in players if p.valid_bid and p.bid == top_bid])"
                },
                "if": {
                  "calc": "top_count == 1 and top_bid >= min_first_bid"
                }
              }
            },
            {
              "set": {
                "key": "standing_bid",
                "value": {
                  "calc": "top_bid"
                },
                "if": {
                  "calc": "top_count == 1 and top_bid >= min_first_bid"
                }
              }
            }
          ]
        },
        {
          "use": "update",
          "phase": "bidding",
          "label": "eligibility",
          "do": [
            {
              "set": {
                "players": "all",
                "key": "eligible",
                "value": {
                  "calc": "you.valid_bid or you.seat == leader"
                }
              }
            }
          ],
          "text": "After turn {turn} on item {round}: standing bid {standing_bid}, leader seat {leader} (0 = none). Eligible [seat, eligible]: {[[p.seat, p.eligible] for p in players]}."
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "resolution",
      "do": [
        {
          "adjust": {
            "players": {
              "where": "you.seat == leader and leader != no_leader_code"
            },
            "key": "score",
            "value": {
              "calc": "you.values[round - 1] - standing_bid"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat == leader and leader != no_leader_code and you.budget >= standing_bid"
            },
            "key": "spent",
            "value": {
              "calc": "standing_bid"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat == leader and leader != no_leader_code and you.budget >= standing_bid"
            },
            "key": "budget",
            "value": {
              "calc": "-standing_bid"
            }
          }
        },
        {
          "set": {
            "key": "last_price",
            "value": {
              "calc": "standing_bid if leader != no_leader_code else 0"
            }
          }
        }
      ],
      "text": "Item {round} result: winner seat {leader} (0 = unsold), price {last_price}. Budgets [seat, budget]: {[[p.seat, p.budget] for p in players]}. Scores [seat, score]: {[[p.seat, p.score] for p in players]}."
    },
    {
      "use": "check",
      "phase": "resolve",
      "label": "after the last item",
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
      "rank_by": "you.score",
      "text": "Winner: {result}. Final scores [seat, score]: {[[p.seat, p.score] for p in players]}."
    }
  },
  "limits": {
    "rounds": 6,
    "rounds_max": 7,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "Each player starts with a budget of {starting_budget}, score {starting_score} and spent {starting_spent}. Before round 1, each player receives a private values list: a random ordering of {value_set}, so every list sums to {values_sum}. Only you see your own list; everyone sees all budgets, scores, spent, eligibility flags, the standing bid, the leader and the last price.\n\nThe game has {rounds} rounds. In round r, item r is sold, and your value for it is entry r of your own list, counting from 1.\n\nAt the start of each round, every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Messages bind nobody.\n\nAfter talk, the standing bid is set to 0, the leader to 0 (no leader), and every player is marked eligible.\n\nEach round has exactly {bidding_turns_per_round} bidding turns. Each turn, all players answer at the same time: {pass_bid} to pass, or a whole number from {min_first_bid} up to their current budget.\n\nA bid is valid only if all three hold: (a) you are eligible for this turn; (b) the bid is at least the standing bid + {min_raise} (in turn 1, at least {min_first_bid}); (c) the bid is at most your budget. A pass, and any bid that is not valid, counts as no bid.\n\nTurn result: find the highest valid bid. If exactly one player made it, the standing bid becomes that amount and that player becomes the leader. If two or more players made it (a tie), or nobody made a valid bid, the standing bid and the leader stay unchanged. A lower valid bid never wins.\n\nEligibility: after each turn, you stay eligible for the next turn only if you made a valid bid in this turn (winning, tied or beaten), or you are the leader after this turn. Everyone else is ineligible for the rest of the round. After each turn the standing bid, the leader and every eligibility flag are announced.\n\nAfter turn 3: if there is a leader, the leader's budget decreases by the standing bid, their spent increases by it, and their score increases by their value for the item minus the standing bid (this can be negative); the last price becomes the standing bid. If there is no leader, the item goes unsold and the last price is 0. The round's result is announced.\n\nAfter round {rounds} the game ends. Unspent budget is worth nothing. The player with the highest score wins; if two or more players share the highest score, they share the result (a draw)."
}
```

Why it was refused: it plays, but part of it does nothing: game attribute `value_set` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "budgeted_english_auction_activity_rule",
    "name": "Budgeted English Auction with Activity Rule",
    "players": {
      "min": 3,
      "max": 6,
      "suggested": 4
    },
    "blurb": "Six items, three sealed bidding turns each, a budget of 30 and private values: stop bidding and you drop out of the item."
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
        "key": "budget",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "spent",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "values",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "eligible",
        "visible": "public",
        "type": "bool",
        "initial": true
      },
      {
        "key": "bid",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "valid_bid",
        "visible": "public",
        "type": "bool",
        "initial": false
      }
    ],
    "game": [
      {
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "turn",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "standing_bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "leader",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "last_price",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "value_set",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "top_bid",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "top_count",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "starting_budget",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "starting_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "starting_spent",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "items",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "bidding_turns_per_round",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "value_1",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "value_2",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "value_3",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "value_4",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "value_5",
        "visible": "public",
        "type": "number",
        "initial": 11
      },
      {
        "key": "value_6",
        "visible": "public",
        "type": "number",
        "initial": 13
      },
      {
        "key": "values_sum",
        "visible": "public",
        "type": "number",
        "initial": 48
      },
      {
        "key": "min_first_bid",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "min_raise",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "pass_bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "no_leader_code",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "starting purses",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "budget",
            "value": {
              "calc": "starting_budget"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "starting_score"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "spent",
            "value": {
              "calc": "starting_spent"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "deal private values",
      "do": [
        {
          "set": {
            "key": "value_set",
            "value": {
              "calc": "[value_1, value_2, value_3, value_4, value_5, value_6]"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "len(you.values) == 0"
            },
            "key": "values",
            "value": {
              "calc": "[x[1] for x in sorted([[uniform(0, 1), v] for v in value_set])]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "the table starts",
      "do": [
        {
          "set": {
            "key": "round",
            "value": 0
          }
        },
        {
          "set": {
            "key": "standing_bid",
            "value": 0
          }
        },
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "no_leader_code"
            }
          }
        },
        {
          "set": {
            "key": "last_price",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "tell",
      "label": "the value set",
      "to": "all",
      "text": "Every private values list is an ordering of {value_set}, so each list sums to {values_sum}. There are {rounds} rounds with {bidding_turns_per_round} bidding turns each."
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
      "phase": "open",
      "label": "the next item",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        }
      ],
      "text": "Item {round} of {items} is now for sale. Your value for it is entry {round} of your values list."
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
      "text": "Item {round} is up. Write one short message to the table. Everyone writes at the same time; messages bind nobody."
    },
    {
      "use": "update",
      "phase": "talk",
      "label": "round reset",
      "do": [
        {
          "set": {
            "key": "standing_bid",
            "value": 0
          }
        },
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "no_leader_code"
            }
          }
        },
        {
          "set": {
            "key": "turn",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "eligible",
            "value": true
          }
        },
        {
          "set": {
            "players": "all",
            "key": "valid_bid",
            "value": false
          }
        }
      ],
      "text": "Bidding on item {round} opens: standing bid 0, no leader, everyone eligible."
    },
    {
      "use": "repeat",
      "phase": "bidding",
      "label": "the bidding turns",
      "until": {
        "calc": "turn >= bidding_turns_per_round"
      },
      "max": 4,
      "steps": [
        {
          "use": "update",
          "phase": "bidding",
          "label": "next turn",
          "do": [
            {
              "adjust": {
                "key": "turn",
                "value": 1
              }
            },
            {
              "set": {
                "players": "all",
                "key": "bid",
                "value": {
                  "calc": "pass_bid"
                }
              }
            }
          ]
        },
        {
          "use": "poll",
          "phase": "bidding",
          "label": "bid",
          "to": "acting",
          "answer": {
            "type": "number",
            "min": {
              "calc": "pass_bid"
            },
            "max": {
              "calc": "you.budget"
            }
          },
          "store": "bid",
          "text": "Item {round}, bidding turn {turn} of {bidding_turns_per_round}. Standing bid {standing_bid}, leader seat {leader} (0 = none). Answer {pass_bid} to pass, or a whole number from {min_first_bid} up to your current budget. Your bid is valid only if you are eligible this turn and it is at least the standing bid + {min_raise}; otherwise it counts as no bid."
        },
        {
          "use": "update",
          "phase": "bidding",
          "label": "validity",
          "do": [
            {
              "set": {
                "players": "all",
                "key": "valid_bid",
                "value": {
                  "calc": "you.eligible and you.bid >= standing_bid + min_raise and you.bid <= you.budget and you.bid >= min_first_bid"
                }
              }
            }
          ]
        },
        {
          "use": "update",
          "phase": "bidding",
          "label": "top bid",
          "do": [
            {
              "set": {
                "key": "top_bid",
                "value": {
                  "calc": "max([p.bid for p in players if p.valid_bid] + [0])"
                }
              }
            },
            {
              "set": {
                "key": "top_count",
                "value": {
                  "calc": "count(p.valid_bid and p.bid == top_bid for p in players)"
                }
              }
            }
          ]
        },
        {
          "use": "update",
          "phase": "bidding",
          "label": "turn result",
          "do": [
            {
              "set": {
                "key": "leader",
                "value": {
                  "calc": "min([p.seat for p in players if p.valid_bid and p.bid == top_bid])"
                },
                "if": {
                  "calc": "top_count == 1 and top_bid >= min_first_bid"
                }
              }
            },
            {
              "set": {
                "key": "standing_bid",
                "value": {
                  "calc": "top_bid"
                },
                "if": {
                  "calc": "top_count == 1 and top_bid >= min_first_bid"
                }
              }
            }
          ]
        },
        {
          "use": "update",
          "phase": "bidding",
          "label": "eligibility",
          "do": [
            {
              "set": {
                "players": "all",
                "key": "eligible",
                "value": {
                  "calc": "you.valid_bid or you.seat == leader"
                }
              }
            }
          ],
          "text": "After turn {turn} on item {round}: standing bid {standing_bid}, leader seat {leader} (0 = none). Eligible [seat, eligible]: {[[p.seat, p.eligible] for p in players]}."
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "resolution",
      "do": [
        {
          "adjust": {
            "players": {
              "where": "you.seat == leader and leader != no_leader_code"
            },
            "key": "score",
            "value": {
              "calc": "you.values[round - 1] - standing_bid"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat == leader and leader != no_leader_code and you.budget >= standing_bid"
            },
            "key": "spent",
            "value": {
              "calc": "standing_bid"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat == leader and leader != no_leader_code and you.budget >= standing_bid"
            },
            "key": "budget",
            "value": {
              "calc": "-standing_bid"
            }
          }
        },
        {
          "set": {
            "key": "last_price",
            "value": {
              "calc": "standing_bid if leader != no_leader_code else 0"
            }
          }
        }
      ],
      "text": "Item {round} result: winner seat {leader} (0 = unsold), price {last_price}. Budgets [seat, budget]: {[[p.seat, p.budget] for p in players]}. Scores [seat, score]: {[[p.seat, p.score] for p in players]}."
    },
    {
      "use": "check",
      "phase": "resolve",
      "label": "after the last item",
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
      "rank_by": "you.score",
      "text": "Winner: {result}. Final scores [seat, score]: {[[p.seat, p.score] for p in players]}."
    }
  },
  "limits": {
    "rounds": 6,
    "rounds_max": 7,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "Each player starts with a budget of {starting_budget}, score {starting_score} and spent {starting_spent}. Before round 1, each player receives a private values list: a random ordering of 3, 5, 7, 9, 11 and 13, so every list sums to {values_sum}. Only you see your own list; everyone sees all budgets, scores, spent, eligibility flags, the standing bid, the leader and the last price.\n\nThe game has {rounds} rounds. In round r, item r is sold, and your value for it is entry r of your own list, counting from 1.\n\nAt the start of each round, every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Messages bind nobody.\n\nAfter talk, the standing bid is set to 0, the leader to 0 (no leader), and every player is marked eligible.\n\nEach round has exactly {bidding_turns_per_round} bidding turns. Each turn, all players answer at the same time: {pass_bid} to pass, or a whole number from {min_first_bid} up to their current budget.\n\nA bid is valid only if all three hold: (a) you are eligible for this turn; (b) the bid is at least the standing bid + {min_raise} (in turn 1, at least {min_first_bid}); (c) the bid is at most your budget. A pass, and any bid that is not valid, counts as no bid.\n\nTurn result: find the highest valid bid. If exactly one player made it, the standing bid becomes that amount and that player becomes the leader. If two or more players made it (a tie), or nobody made a valid bid, the standing bid and the leader stay unchanged. A lower valid bid never wins.\n\nEligibility: after each turn, you stay eligible for the next turn only if you made a valid bid in this turn (winning, tied or beaten), or you are the leader after this turn. Everyone else is ineligible for the rest of the round. After each turn the standing bid, the leader and every eligibility flag are announced.\n\nAfter turn 3: if there is a leader, the leader's budget decreases by the standing bid, their spent increases by it, and their score increases by their value for the item minus the standing bid (this can be negative); the last price becomes the standing bid. If there is no leader, the item goes unsold and the last price is 0. The round's result is announced.\n\nAfter round {rounds} the game ends. Unspent budget is worth nothing. The player with the highest score wins; if two or more players share the highest score, they share the result (a draw)."
}
```
````
