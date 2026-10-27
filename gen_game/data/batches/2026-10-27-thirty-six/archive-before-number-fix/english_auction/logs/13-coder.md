# 13 coder

- time: 2026-10-27T16:50:51+00:00 (62.6s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 b45cd15889994109, reply sha256 24a179c9f78d1db5

## Sent

````
# Task: write the XColos game file for "Budgeted English Auction Series"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 5; set `meta.players` to {"min": 3, "max": 5, "suggested": 3} (the suggested size is the one the game plays best at).

SETUP. There are 6 items, auctioned one per round in a known order (item 1 in round 1, and so on to item 6 in round 6). Before round 1, each player is privately dealt the six values 3, 5, 7, 9, 11 and 13 in a random order: one value per item, each value used exactly once. Each player sees only their own values. Every player's values sum to 48. Each player starts with a budget of 30 coins and a score of 0. Seats are numbered 1 to N.

PRIORITY. In round r, the tie-break priority goes to seat ((r - 1) mod N) + 1 first, then the following seats in increasing order, wrapping around. The priority order is announced at the start of the round.

EACH ROUND (one item):
1. Announce the item number, the priority order, and every player's remaining budget. Budgets and scores are public.
2. Talk: every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Messages bind nobody.
3. Bidding turn 1: every player at the same time either submits a whole-number bid of at least 1 or passes. A bid is valid only if it does not exceed the bidder's remaining budget; an invalid bid counts as a pass. If at least one valid bid was made, the highest becomes the standing bid and its bidder becomes the leader. Equal highest bids go to the player earliest in this round's priority order.
4. Announce the standing bid and the leader, or announce that there is no bid.
5. Bidding turn 2: every player at the same time either passes or submits a whole-number bid. To be valid, the bid must be at least the standing bid plus 1 (at least 1 if there is no standing bid) and must not exceed the bidder's remaining budget; otherwise it counts as a pass. The leader may also bid, though they need not. If any valid bid was made, the highest becomes the new standing bid and its bidder the new leader, with ties broken by priority. If nobody makes a valid bid, the standing bid and leader stay as they were.
6. Announce the standing bid and the leader.
7. Bidding turn 3: same as turn 2.
8. Announce the final standing bid and the leader.
9. Resolution: if there is a leader, that player wins the item. They pay the standing bid from their budget, and their score changes by (their private value for this item minus the standing bid), which may be negative. The price is announced, but the winner's value stays private. If there is no leader, the item goes unsold and nobody scores for it.
10. Advance to the next round. After round 6 the game ends.

Unspent coins are worth nothing at the end. Scores count only item values won minus prices paid.

How the winner is decided: After round 6, the player with the highest score wins. If two or more players share the highest score, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Budgeted English Auction Series (3 to 5 players, best with 3)

Six items are auctioned one per round. Each auction has three simultaneous sealed bidding turns, and players hold private values and separate budgets of 30 coins; the highest total of value won minus price paid wins.

STATE (every item below must exist in the file):
  - each player: budget (number, starts 30); everyone sees it. Remaining coins. Winning an item reduces it by the price. Unspent coins are worth nothing at the end.
  - each player: score (number, starts 0); everyone sees it. Sum over won items of (private value minus price paid). It may be negative.
  - each player: values (list, starts []); only its owner sees it. The player's private values for items 1 to 6, in item order. It is a random permutation of 3, 5, 7, 9, 11, 13.
  - each player: bid (number, starts 0); only its owner sees it. This bidding turn's submitted bid, where 0 means pass. It stays sealed until all bids are in.
  - each player: bid_valid (bool, starts False); only its owner sees it. Whether this turn's bid met the validity rule. An invalid bid counts as a pass.
  - each player: message (text, starts ''); everyone sees it. This round's short talk message. It binds nobody.
  - the table: round (number, starts 1); everyone sees it. Current round, which is also the number of the item on sale (1 to 6).
  - the table: first_seat (number, starts 1); everyone sees it. The seat with top tie-break priority this round: ((round - 1) mod N) + 1.
  - the table: priority_order (list, starts []); everyone sees it. Seats in this round's tie-break order: first_seat, then increasing seat numbers, wrapping around.
  - the table: standing_bid (number, starts 0); everyone sees it. Current highest valid bid this round. 0 means no bid yet.
  - the table: leader (number, starts 0); everyone sees it. Seat holding the standing bid. 0 means no leader.
  - the table: last_price (number, starts 0); everyone sees it. Price paid for the most recently resolved item. 0 if the item went unsold.
  - the table: value_pool (list, starts []); hidden from all players. A temporary copy of [3,5,7,9,11,13], drawn from at random to deal one player's values.
  - parameters, each kept as a table attribute: items = 6, rounds = 6, item_value_1 = 3, item_value_2 = 5, item_value_3 = 7, item_value_4 = 9, item_value_5 = 11, item_value_6 = 13, value_sum = 48, starting_budget = 30, starting_score = 0, min_bid = 1, min_raise = 1, bidding_turns_per_round = 3, no_leader_code = 0, pass_code = 0, tiebreak_multiplier = 10

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seats are numbered 1 to N, where N is the number of players.
  2. Every player gets budget 30 and score 0.
  3. For each player in turn, value_pool is set to [3,5,7,9,11,13]. Six times, one entry is drawn at random from value_pool, appended to that player's values list and removed from value_pool. values[k-1] is that player's private value for item k. Each value is used exactly once, so the values sum to 48.
  4. Each player is sent their own values list. No player sees another's values.
  5. round is set to 1, standing_bid to 0, leader to 0 and last_price to 0.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: first_seat = ((round - 1) mod N) + 1. priority_order = [first_seat, first_seat+1, ..., N, 1, ..., first_seat-1]. standing_bid = 0. leader = 0. Every player's bid = 0 and bid_valid = false.
  2. [tell] all players. What happens: Announce: 'Item {round} is on sale. Priority order: {priority_order}. Budgets: {budget of each seat}. Scores: {score of each seat}.'
  3. [poll] all players answers: short text. What happens: Each player's message is set to their reply. Once all replies are in, broadcast {"to": "all", "text": "Seat {seat} says: {value}"}. Messages bind nobody.
  4. [poll] all players answers: a whole number from 0 to your budget; 0 = pass, otherwise a bid of at least 1. What happens: Bidding turn 1. Each player's bid = reply. bid_valid = (bid >= 1 and bid <= budget). If any bid_valid: the valid bidder with the highest key = bid * 10 + (N - 1 - ((seat - first_seat) mod N)) becomes leader, and standing_bid = that bid. Otherwise standing_bid = 0 and leader = 0.
  5. [tell] all players. What happens: Announce 'Standing bid {standing_bid} by seat {leader}' if leader > 0, else 'No bid.'
  6. [poll] all players answers: a whole number from 0 to your budget; 0 = pass, otherwise a bid of at least standing_bid + 1. What happens: Bidding turn 2. Each player's bid = reply. bid_valid = (bid >= standing_bid + 1 and bid >= 1 and bid <= budget). The leader may bid too. If any bid_valid: the valid bidder with the highest key = bid * 10 + (N - 1 - ((seat - first_seat) mod N)) becomes leader, and standing_bid = that bid. Otherwise standing_bid and leader are unchanged.
  7. [tell] all players. What happens: Announce 'Standing bid {standing_bid} by seat {leader}' if leader > 0, else 'No bid.'
  8. [poll] all players answers: a whole number from 0 to your budget; 0 = pass, otherwise a bid of at least standing_bid + 1. What happens: Bidding turn 3, the same as turn 2: bid_valid = (bid >= standing_bid + 1 and bid >= 1 and bid <= budget). The valid bidder with the highest key becomes leader, and standing_bid = that bid. If there is no valid bid, nothing changes.
  9. [tell] all players. What happens: Announce 'Final standing bid {standing_bid} by seat {leader}' if leader > 0, else 'No bid; item {round} goes unsold.'
  10. [update] seat leader. What happens: When leader > 0: the leader's budget -= standing_bid, the leader's score += values[round - 1] - standing_bid, and last_price = standing_bid. When leader = 0: last_price = 0 and nobody's budget or score changes.
  11. [tell] all players. What happens: If leader > 0, announce 'Item {round} sold to seat {leader} for {last_price}.' The winner's value is not announced. Otherwise announce 'Item {round} unsold.'
  12. [update] all players. What happens: round += 1.
  13. [check] all players. What happens: End the game if round > 6. Otherwise continue with the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, every player has budget 30 and score 0, and a private values list that is a permutation of [3,5,7,9,11,13] summing to 48.
  R2. When the game starts, each player's values list is visible only to that player.
  R3. In round r, item r is sold, for r from 1 to 6.
  R4. In round r with N players, priority starts at seat ((r - 1) mod N) + 1 and continues in increasing seat order, wrapping around; with N = 3, round 2's order is 2, 3, 1.
  R5. At the start of each round, the item number, priority order, every budget and every score are announced.
  R6. Before bidding each round, every player submits one short message simultaneously, and all messages are then shown to everyone.
  R7. In bidding turn 1, a bid is valid only if it is at least 1 and at most the bidder's budget; 0 or an invalid bid counts as a pass.
  R8. In bidding turn 1, if at least one valid bid is made, the highest valid bid becomes standing_bid and its bidder becomes leader; if none is made, standing_bid = 0 and leader = 0.
  R9. In bidding turns 2 and 3, a bid is valid only if it is at least standing_bid + 1 (at least 1 when there is no standing bid) and at most the bidder's budget; otherwise it counts as a pass.
  R10. In bidding turns 2 and 3, if any valid bid is made, the highest valid bid becomes standing_bid and its bidder becomes leader; if none is made, standing_bid and leader are unchanged.
  R11. When two or more players make the same highest valid bid in a turn, the one earliest in this round's priority order becomes leader; e.g. in round 1 with seats 1 and 3 both bidding 8, seat 1 leads.
  R12. The current leader may bid in turns 2 and 3 but need not.
  R13. After each bidding turn, the standing bid and leader (or no bid) are announced.
  R14. When a round ends with a leader, the leader's budget falls by standing_bid and their score changes by (their value for this item minus standing_bid); e.g. value 7 bought at 10 gives score -3.
  R15. When a round ends with a leader, the price is announced but the winner's private value is not.
  R16. When a round ends with no leader, the item is unsold and no budget or score changes.
  R17. When round 6 is resolved, the game ends.
  R18. When the game ends, the player with the highest score wins, unspent budget is worth 0, and players tied at the highest score share the result as a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Talk message each round | asked: every seat | options: Any short text message.
  - Bidding turn 1 | asked: every seat | options: Pass (0), or a whole-number bid from 1 to the seat's own budget. A seat with budget 0 may only pass.
  - Bidding turns 2 and 3 | asked: every seat, including the current leader | options: Pass (0), or a whole-number bid from standing_bid + 1 to the seat's own budget. A seat whose budget is below standing_bid + 1 may only pass. The engine range is 0 to budget, and any entry from 1 to standing_bid is treated as a pass.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round > 6
  - each player's standing: you.score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their score: the total of private values of items won minus prices paid. Unspent budget counts for nothing. The highest score wins. Players level at the top share the win, which stands in for the source's draw.
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

- each player: `budget` (number, visible: public, starts 30): Remaining coins. Winning an item reduces it by the price. Unspent coins are worth nothing at the end.
- each player: `score` (number, visible: public, starts 0): Sum over won items of (private value minus price paid). It may be negative.
- the table: `round` (number, visible: public, starts 1): Current round, which is also the number of the item on sale (1 to 6).
- the table: `standing_bid` (number, visible: public, starts 0): Current highest valid bid this round. 0 means no bid yet.
- the table: `leader` (number, visible: public, starts 0): Seat holding the standing bid. 0 means no leader.
- the table: `last_price` (number, visible: public, starts 0): Price paid for the most recently resolved item. 0 if the item went unsold.
- parameters (each must be an attribute holding this value, never a number buried in a step): items = 6, rounds = 6, item_value_1 = 3, item_value_2 = 5, item_value_3 = 7, item_value_4 = 9, item_value_5 = 11, item_value_6 = 13, value_sum = 48, starting_budget = 30, starting_score = 0, min_bid = 1, min_raise = 1, bidding_turns_per_round = 3, no_leader_code = 0, pass_code = 0, tiebreak_multiplier = 10
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

Make each of the three bidding turns a simultaneous numeric choice. Its options must include pass_code (0) and every whole number from min_bid up to the player's remaining budget, or the platform's numeric_bids range form. A bid of 4 must be selectable when the budget is 30.

After each poll:
- Mark bids valid only if they are at least min_bid (turn 1), or at least standing_bid + min_raise (turns 2 and 3), and do not exceed the bidder's budget.
- Pick the highest valid bid. Break ties by priority, for example with a key of bid*tiebreak_multiplier plus a priority term derived from first_seat.
- Set standing_bid and leader.

At resolution, when leader != no_leader_code:
- Subtract standing_bid from the leader's budget.
- Add values[round] - standing_bid to the leader's score.
- Set last_price = standing_bid; otherwise set last_price = 0.

Leave standing_bid and leader showing the resolved round's values until the next round starts. The tests read them after resolution.

Also check the setup. The trace shows seat 1's dealt values being replaced by the sorted list. That came from the test's `given` here, but make sure the deal itself never overwrites values.


YOUR PREVIOUS GAME FILE WAS REFUSED. Here it is:
```json
{
  "schema": 1,
  "meta": {
    "id": "budgeted_english_auction_series",
    "name": "Budgeted English Auction Series",
    "players": {
      "min": 3,
      "max": 5,
      "suggested": 3
    },
    "blurb": "Six items, three sealed bidding turns each, private values and a 30-coin budget: the highest total of value won minus price paid wins."
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
        "key": "values",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "bid",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bid_valid",
        "visible": "ally",
        "type": "bool",
        "initial": false
      },
      {
        "key": "message",
        "visible": "public",
        "type": "text",
        "initial": ""
      }
    ],
    "game": [
      {
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "first_seat",
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
        "key": "value_pool",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "best_key",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "items",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "item_value_1",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "item_value_2",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "item_value_3",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "item_value_4",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "item_value_5",
        "visible": "public",
        "type": "number",
        "initial": 11
      },
      {
        "key": "item_value_6",
        "visible": "public",
        "type": "number",
        "initial": 13
      },
      {
        "key": "value_sum",
        "visible": "public",
        "type": "number",
        "initial": 48
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
        "key": "min_bid",
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
        "key": "bidding_turns_per_round",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "no_leader_code",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "pass_code",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tiebreak_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 10
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "starting budgets and scores",
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
        }
      ]
    },
    {
      "use": "update",
      "label": "deal the private values",
      "do": [
        {
          "set": {
            "key": "value_pool",
            "value": {
              "calc": "[item_value_1, item_value_2, item_value_3, item_value_4, item_value_5, item_value_6]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "values",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "values",
            "value": {
              "calc": "you.values + [[v for v in value_pool if v not in you.values][min(int(uniform(0, len(value_pool) - len(you.values))), len(value_pool) - len(you.values) - 1)]]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "values",
            "value": {
              "calc": "you.values + [[v for v in value_pool if v not in you.values][min(int(uniform(0, len(value_pool) - len(you.values))), len(value_pool) - len(you.values) - 1)]]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "values",
            "value": {
              "calc": "you.values + [[v for v in value_pool if v not in you.values][min(int(uniform(0, len(value_pool) - len(you.values))), len(value_pool) - len(you.values) - 1)]]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "values",
            "value": {
              "calc": "you.values + [[v for v in value_pool if v not in you.values][min(int(uniform(0, len(value_pool) - len(you.values))), len(value_pool) - len(you.values) - 1)]]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "values",
            "value": {
              "calc": "you.values + [[v for v in value_pool if v not in you.values][min(int(uniform(0, len(value_pool) - len(you.values))), len(value_pool) - len(you.values) - 1)]]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "values",
            "value": {
              "calc": "you.values + [[v for v in value_pool if v not in you.values][min(int(uniform(0, len(value_pool) - len(you.values))), len(value_pool) - len(you.values) - 1)]]"
            }
          }
        },
        {
          "set": {
            "key": "value_pool",
            "value": []
          }
        }
      ]
    },
    {
      "use": "sync",
      "label": "your private values",
      "mode": "self",
      "to": "all",
      "text": "Your private values for items 1 to 6 (in item order), your budget and your score:"
    },
    {
      "use": "update",
      "label": "the table is ready",
      "do": [
        {
          "set": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "key": "standing_bid",
            "value": {
              "calc": "no_leader_code"
            }
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
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "open",
      "label": "the round opens",
      "do": [
        {
          "set": {
            "key": "first_seat",
            "value": {
              "calc": "((round - 1) % len(players)) + 1"
            }
          }
        },
        {
          "set": {
            "key": "priority_order",
            "value": {
              "calc": "[p.seat for p in players if p.seat >= first_seat] + [p.seat for p in players if p.seat < first_seat]"
            }
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
            "players": "all",
            "key": "bid",
            "value": {
              "calc": "pass_code"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bid_valid",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "message",
            "value": ""
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "open",
      "label": "the item is up",
      "to": "all",
      "text": "Item {round} is on sale. Priority order: {priority_order}. Budgets [seat, budget]: {[[p.seat, p.budget] for p in players]}. Scores [seat, score]: {[[p.seat, p.score] for p in players]}."
    },
    {
      "use": "poll",
      "phase": "talk",
      "label": "talk",
      "to": "acting",
      "answer": {
        "type": "text",
        "max_words": 30
      },
      "store": "message",
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} says: {value}"
      },
      "text": "Item {round} is on sale. Write one short message to the table. Everyone writes at the same time; messages bind nobody."
    },
    {
      "use": "poll",
      "phase": "bidding",
      "label": "bidding turn 1",
      "to": {
        "where": "you.budget >= min_bid"
      },
      "answer": {
        "type": "number",
        "min": 0,
        "max": {
          "calc": "you.budget"
        }
      },
      "store": "bid",
      "text": "Bidding turn 1 of {bidding_turns_per_round} on item {round}. Answer 0 to pass, or a whole-number bid of at least {min_bid} and no more than your budget. Bids are sealed until all are in. The highest valid bid becomes the standing bid; equal highest bids go to the seat earliest in the priority order {priority_order}."
    },
    {
      "use": "update",
      "phase": "bidding",
      "label": "turn 1 resolves",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": {
              "calc": "int(you.bid)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bid_valid",
            "value": {
              "calc": "you.bid >= min_bid and you.bid <= you.budget"
            }
          }
        },
        {
          "set": {
            "key": "best_key",
            "value": {
              "calc": "max([p.bid * tiebreak_multiplier + (len(players) - 1 - ((p.seat - first_seat) % len(players))) for p in players if p.bid_valid] + [0])"
            }
          }
        },
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "max([p.seat for p in players if p.bid_valid and p.bid * tiebreak_multiplier + (len(players) - 1 - ((p.seat - first_seat) % len(players))) == best_key] + [no_leader_code])"
            }
          }
        },
        {
          "set": {
            "key": "standing_bid",
            "value": {
              "calc": "max([p.bid for p in players if p.bid_valid] + [0])"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": {
              "calc": "pass_code"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "bidding",
      "label": "standing bid after turn 1",
      "when": {
        "calc": "leader != no_leader_code"
      },
      "to": "all",
      "text": "Standing bid {standing_bid} by seat {leader}."
    },
    {
      "use": "tell",
      "phase": "bidding",
      "label": "no bid after turn 1",
      "when": {
        "calc": "leader == no_leader_code"
      },
      "to": "all",
      "text": "No bid."
    },
    {
      "use": "poll",
      "phase": "bidding",
      "label": "bidding turn 2",
      "to": {
        "where": "you.budget >= standing_bid + min_raise"
      },
      "answer": {
        "type": "number",
        "min": 0,
        "max": {
          "calc": "you.budget"
        }
      },
      "store": "bid",
      "text": "Bidding turn 2 of {bidding_turns_per_round} on item {round}. Standing bid {standing_bid}, leader seat {leader} (0 means none). Answer 0 to pass, or a whole-number bid of at least the standing bid plus {min_raise} and no more than your budget; any lower bid counts as a pass. The leader may bid too. Equal highest bids go to the seat earliest in the priority order {priority_order}."
    },
    {
      "use": "update",
      "phase": "bidding",
      "label": "turn 2 resolves",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": {
              "calc": "int(you.bid)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bid_valid",
            "value": {
              "calc": "you.bid >= standing_bid + min_raise and you.bid >= min_bid and you.bid <= you.budget"
            }
          }
        },
        {
          "set": {
            "key": "best_key",
            "value": {
              "calc": "max([p.bid * tiebreak_multiplier + (len(players) - 1 - ((p.seat - first_seat) % len(players))) for p in players if p.bid_valid] + [0])"
            }
          }
        },
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "max([p.seat for p in players if p.bid_valid and p.bid * tiebreak_multiplier + (len(players) - 1 - ((p.seat - first_seat) % len(players))) == best_key] + [no_leader_code])"
            },
            "if": {
              "calc": "any(p.bid_valid for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "standing_bid",
            "value": {
              "calc": "max([p.bid for p in players if p.bid_valid] + [0])"
            },
            "if": {
              "calc": "any(p.bid_valid for p in players)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": {
              "calc": "pass_code"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "bidding",
      "label": "standing bid after turn 2",
      "when": {
        "calc": "leader != no_leader_code"
      },
      "to": "all",
      "text": "Standing bid {standing_bid} by seat {leader}."
    },
    {
      "use": "tell",
      "phase": "bidding",
      "label": "no bid after turn 2",
      "when": {
        "calc": "leader == no_leader_code"
      },
      "to": "all",
      "text": "No bid."
    },
    {
      "use": "poll",
      "phase": "bidding",
      "label": "bidding turn 3",
      "to": {
        "where": "you.budget >= standing_bid + min_raise"
      },
      "answer": {
        "type": "number",
        "min": 0,
        "max": {
          "calc": "you.budget"
        }
      },
      "store": "bid",
      "text": "Bidding turn 3 of {bidding_turns_per_round} (the last) on item {round}. Standing bid {standing_bid}, leader seat {leader} (0 means none). Answer 0 to pass, or a whole-number bid of at least the standing bid plus {min_raise} and no more than your budget; any lower bid counts as a pass. The leader may bid too. Equal highest bids go to the seat earliest in the priority order {priority_order}."
    },
    {
      "use": "update",
      "phase": "bidding",
      "label": "turn 3 resolves",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": {
              "calc": "int(you.bid)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bid_valid",
            "value": {
              "calc": "you.bid >= standing_bid + min_raise and you.bid >= min_bid and you.bid <= you.budget"
            }
          }
        },
        {
          "set": {
            "key": "best_key",
            "value": {
              "calc": "max([p.bid * tiebreak_multiplier + (len(players) - 1 - ((p.seat - first_seat) % len(players))) for p in players if p.bid_valid] + [0])"
            }
          }
        },
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "max([p.seat for p in players if p.bid_valid and p.bid * tiebreak_multiplier + (len(players) - 1 - ((p.seat - first_seat) % len(players))) == best_key] + [no_leader_code])"
            },
            "if": {
              "calc": "any(p.bid_valid for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "standing_bid",
            "value": {
              "calc": "max([p.bid for p in players if p.bid_valid] + [0])"
            },
            "if": {
              "calc": "any(p.bid_valid for p in players)"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "bidding",
      "label": "final standing bid",
      "when": {
        "calc": "leader != no_leader_code"
      },
      "to": "all",
      "text": "Final standing bid {standing_bid} by seat {leader}."
    },
    {
      "use": "tell",
      "phase": "bidding",
      "label": "no final bid",
      "when": {
        "calc": "leader == no_leader_code"
      },
      "to": "all",
      "text": "No bid; item {round} goes unsold."
    },
    {
      "use": "update",
      "phase": "resolution",
      "label": "the item is resolved",
      "do": [
        {
          "adjust": {
            "players": {
              "where": "you.seat == leader and you.budget >= standing_bid"
            },
            "key": "score",
            "value": {
              "calc": "you.values[round - 1] - standing_bid"
            },
            "if": {
              "calc": "leader != no_leader_code"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat == leader and you.budget >= standing_bid"
            },
            "key": "budget",
            "value": {
              "calc": "-standing_bid"
            },
            "if": {
              "calc": "leader != no_leader_code"
            }
          }
        },
        {
          "set": {
            "key": "last_price",
            "value": {
              "calc": "standing_bid"
            },
            "if": {
              "calc": "leader != no_leader_code"
            },
            "text": "Item {round} sold to seat {leader} for {standing_bid}."
          }
        },
        {
          "set": {
            "key": "last_price",
            "value": 0,
            "if": {
              "calc": "leader == no_leader_code"
            },
            "text": "Item {round} unsold."
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolution",
      "label": "advance the round",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "resolution",
      "label": "after the last item",
      "when": {
        "calc": "round > rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round > rounds"
      },
      "rank_by": "you.score",
      "text": "Winner: {result}. Final scores [seat, score]: {[[p.seat, p.score] for p in players]}."
    }
  },
  "limits": {
    "rounds": 6,
    "rounds_max": 6,
    "actions_max": 1000,
    "deadline_s": 120
  },
  "rules": "There are {items} items, auctioned one per round in a known order: item 1 in round 1, and so on to item {items} in round {rounds}. Before round 1, each player is privately dealt the six values {item_value_1}, {item_value_2}, {item_value_3}, {item_value_4}, {item_value_5} and {item_value_6} in a random order: one value per item, each value used exactly once. Each player sees only their own values. Every player's values sum to {value_sum}. Each player starts with a budget of {starting_budget} coins and a score of {starting_score}. Seats are numbered 1 to N.\n\nPRIORITY. In round r, the tie-break priority goes to seat ((r - 1) mod N) + 1 first, then the following seats in increasing order, wrapping around (with 3 players, round 2's order is 2, 3, 1). The priority order is announced at the start of the round.\n\nEACH ROUND (one item):\n1. The item number, the priority order, and every player's remaining budget and score are announced. Budgets and scores are public.\n2. Talk: every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Messages bind nobody.\n3. Bidding turn 1: every player at the same time either submits a whole-number bid of at least {min_bid} or passes (answers 0). A bid is valid only if it does not exceed the bidder's remaining budget; an invalid bid counts as a pass. If at least one valid bid was made, the highest becomes the standing bid and its bidder becomes the leader. Equal highest bids go to the player earliest in this round's priority order. If no valid bid was made, there is no standing bid and no leader.\n4. The standing bid and the leader are announced, or that there is no bid.\n5. Bidding turn 2: every player at the same time either passes (0) or submits a whole-number bid. To be valid, the bid must be at least the standing bid plus {min_raise} (at least {min_bid} if there is no standing bid) and must not exceed the bidder's remaining budget; otherwise it counts as a pass. The leader may also bid, though they need not. If any valid bid was made, the highest becomes the new standing bid and its bidder the new leader, with ties broken by priority. If nobody makes a valid bid, the standing bid and leader stay as they were. A player whose budget is below the lowest valid bid is not asked and passes.\n6. The standing bid and the leader are announced.\n7. Bidding turn 3: same as turn 2.\n8. The final standing bid and the leader are announced.\n9. Resolution: if there is a leader, that player wins the item. They pay the standing bid from their budget, and their score changes by (their private value for this item minus the standing bid), which may be negative (value 7 bought at 10 gives -3). The price is announced, but the winner's value stays private. If there is no leader, the item goes unsold, nobody pays and nobody scores for it.\n10. Advance to the next round. After round {rounds} the game ends.\n\nUnspent coins are worth nothing at the end. Scores count only item values won minus prices paid. After round {rounds}, the player with the highest score wins; players level at the highest score share the win (a draw)."
}
```

Why it was refused: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (message, message, message) in `your_private_values`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "budgeted_english_auction_series",
    "name": "Budgeted English Auction Series",
    "players": {
      "min": 3,
      "max": 5,
      "suggested": 3
    },
    "blurb": "Six items, three sealed bidding turns each, private values and a 30-coin budget: the highest total of value won minus price paid wins."
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
        "key": "values",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "bid",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bid_valid",
        "visible": "ally",
        "type": "bool",
        "initial": false
      },
      {
        "key": "message",
        "visible": "public",
        "type": "text",
        "initial": ""
      }
    ],
    "game": [
      {
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "first_seat",
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
        "key": "value_pool",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "best_key",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "items",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "item_value_1",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "item_value_2",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "item_value_3",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "item_value_4",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "item_value_5",
        "visible": "public",
        "type": "number",
        "initial": 11
      },
      {
        "key": "item_value_6",
        "visible": "public",
        "type": "number",
        "initial": 13
      },
      {
        "key": "value_sum",
        "visible": "public",
        "type": "number",
        "initial": 48
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
        "key": "min_bid",
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
        "key": "bidding_turns_per_round",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "no_leader_code",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "pass_code",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tiebreak_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 10
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "starting budgets and scores",
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
        }
      ]
    },
    {
      "use": "update",
      "label": "deal the private values",
      "do": [
        {
          "set": {
            "key": "value_pool",
            "value": {
              "calc": "[item_value_1, item_value_2, item_value_3, item_value_4, item_value_5, item_value_6]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "values",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "values",
            "value": {
              "calc": "you.values + [[v for v in value_pool if v not in you.values][min(int(uniform(0, len(value_pool) - len(you.values))), len(value_pool) - len(you.values) - 1)]]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "values",
            "value": {
              "calc": "you.values + [[v for v in value_pool if v not in you.values][min(int(uniform(0, len(value_pool) - len(you.values))), len(value_pool) - len(you.values) - 1)]]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "values",
            "value": {
              "calc": "you.values + [[v for v in value_pool if v not in you.values][min(int(uniform(0, len(value_pool) - len(you.values))), len(value_pool) - len(you.values) - 1)]]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "values",
            "value": {
              "calc": "you.values + [[v for v in value_pool if v not in you.values][min(int(uniform(0, len(value_pool) - len(you.values))), len(value_pool) - len(you.values) - 1)]]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "values",
            "value": {
              "calc": "you.values + [[v for v in value_pool if v not in you.values][min(int(uniform(0, len(value_pool) - len(you.values))), len(value_pool) - len(you.values) - 1)]]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "values",
            "value": {
              "calc": "you.values + [[v for v in value_pool if v not in you.values][min(int(uniform(0, len(value_pool) - len(you.values))), len(value_pool) - len(you.values) - 1)]]"
            }
          }
        },
        {
          "set": {
            "key": "value_pool",
            "value": []
          }
        }
      ]
    },
    {
      "use": "sync",
      "label": "your private values",
      "mode": "self",
      "to": "all",
      "fields": [
        "values",
        "budget",
        "score"
      ],
      "text": "Your private values for items 1 to 6 (in item order), your budget and your score:"
    },
    {
      "use": "update",
      "label": "the table is ready",
      "do": [
        {
          "set": {
            "key": "round",
            "value": 1
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
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "open",
      "label": "the round opens",
      "do": [
        {
          "set": {
            "key": "first_seat",
            "value": {
              "calc": "((round - 1) % len(players)) + 1"
            }
          }
        },
        {
          "set": {
            "key": "priority_order",
            "value": {
              "calc": "[p.seat for p in players if p.seat >= first_seat] + [p.seat for p in players if p.seat < first_seat]"
            }
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
            "players": "all",
            "key": "bid",
            "value": {
              "calc": "pass_code"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bid_valid",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "message",
            "value": ""
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "open",
      "label": "the item is up",
      "to": "all",
      "text": "Item {round} is on sale. Priority order: {priority_order}. Budgets [seat, budget]: {[[p.seat, p.budget] for p in players]}. Scores [seat, score]: {[[p.seat, p.score] for p in players]}."
    },
    {
      "use": "poll",
      "phase": "talk",
      "label": "talk",
      "to": "acting",
      "answer": {
        "type": "text",
        "max_words": 30
      },
      "store": "message",
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} says: {value}"
      },
      "text": "Item {round} is on sale. Write one short message to the table. Everyone writes at the same time; messages bind nobody."
    },
    {
      "use": "poll",
      "phase": "bidding",
      "label": "bidding turn 1",
      "to": {
        "where": "you.budget >= min_bid"
      },
      "answer": {
        "type": "number",
        "min": 0,
        "max": {
          "calc": "you.budget"
        }
      },
      "store": "bid",
      "text": "Bidding turn 1 of {bidding_turns_per_round} on item {round}. Answer 0 to pass, or a whole-number bid of at least {min_bid} and no more than your budget. Bids are sealed until all are in. The highest valid bid becomes the standing bid; equal highest bids go to the seat earliest in the priority order {priority_order}."
    },
    {
      "use": "update",
      "phase": "bidding",
      "label": "turn 1 resolves",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": {
              "calc": "int(you.bid)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bid_valid",
            "value": {
              "calc": "you.bid >= min_bid and you.bid <= you.budget"
            }
          }
        },
        {
          "set": {
            "key": "best_key",
            "value": {
              "calc": "max([p.bid * tiebreak_multiplier + (len(players) - 1 - ((p.seat - first_seat) % len(players))) for p in players if p.bid_valid] + [0])"
            }
          }
        },
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "max([p.seat for p in players if p.bid_valid and p.bid * tiebreak_multiplier + (len(players) - 1 - ((p.seat - first_seat) % len(players))) == best_key] + [no_leader_code])"
            }
          }
        },
        {
          "set": {
            "key": "standing_bid",
            "value": {
              "calc": "max([p.bid for p in players if p.bid_valid] + [0])"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": {
              "calc": "pass_code"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "bidding",
      "label": "standing bid after turn 1",
      "when": {
        "calc": "leader != no_leader_code"
      },
      "to": "all",
      "text": "Standing bid {standing_bid} by seat {leader}."
    },
    {
      "use": "tell",
      "phase": "bidding",
      "label": "no bid after turn 1",
      "when": {
        "calc": "leader == no_leader_code"
      },
      "to": "all",
      "text": "No bid."
    },
    {
      "use": "poll",
      "phase": "bidding",
      "label": "bidding turn 2",
      "to": {
        "where": "you.budget >= standing_bid + min_raise"
      },
      "answer": {
        "type": "number",
        "min": 0,
        "max": {
          "calc": "you.budget"
        }
      },
      "store": "bid",
      "text": "Bidding turn 2 of {bidding_turns_per_round} on item {round}. Standing bid {standing_bid}, leader seat {leader} (0 means none). Answer 0 to pass, or a whole-number bid of at least the standing bid plus {min_raise} and no more than your budget; any lower bid counts as a pass. The leader may bid too. Equal highest bids go to the seat earliest in the priority order {priority_order}."
    },
    {
      "use": "update",
      "phase": "bidding",
      "label": "turn 2 resolves",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": {
              "calc": "int(you.bid)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bid_valid",
            "value": {
              "calc": "you.bid >= standing_bid + min_raise and you.bid >= min_bid and you.bid <= you.budget"
            }
          }
        },
        {
          "set": {
            "key": "best_key",
            "value": {
              "calc": "max([p.bid * tiebreak_multiplier + (len(players) - 1 - ((p.seat - first_seat) % len(players))) for p in players if p.bid_valid] + [0])"
            }
          }
        },
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "max([p.seat for p in players if p.bid_valid and p.bid * tiebreak_multiplier + (len(players) - 1 - ((p.seat - first_seat) % len(players))) == best_key] + [no_leader_code])"
            },
            "if": {
              "calc": "any(p.bid_valid for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "standing_bid",
            "value": {
              "calc": "max([p.bid for p in players if p.bid_valid] + [0])"
            },
            "if": {
              "calc": "any(p.bid_valid for p in players)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": {
              "calc": "pass_code"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "bidding",
      "label": "standing bid after turn 2",
      "when": {
        "calc": "leader != no_leader_code"
      },
      "to": "all",
      "text": "Standing bid {standing_bid} by seat {leader}."
    },
    {
      "use": "tell",
      "phase": "bidding",
      "label": "no bid after turn 2",
      "when": {
        "calc": "leader == no_leader_code"
      },
      "to": "all",
      "text": "No bid."
    },
    {
      "use": "poll",
      "phase": "bidding",
      "label": "bidding turn 3",
      "to": {
        "where": "you.budget >= standing_bid + min_raise"
      },
      "answer": {
        "type": "number",
        "min": 0,
        "max": {
          "calc": "you.budget"
        }
      },
      "store": "bid",
      "text": "Bidding turn 3 of {bidding_turns_per_round} (the last) on item {round}. Standing bid {standing_bid}, leader seat {leader} (0 means none). Answer 0 to pass, or a whole-number bid of at least the standing bid plus {min_raise} and no more than your budget; any lower bid counts as a pass. The leader may bid too. Equal highest bids go to the seat earliest in the priority order {priority_order}."
    },
    {
      "use": "update",
      "phase": "bidding",
      "label": "turn 3 resolves",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": {
              "calc": "int(you.bid)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bid_valid",
            "value": {
              "calc": "you.bid >= standing_bid + min_raise and you.bid >= min_bid and you.bid <= you.budget"
            }
          }
        },
        {
          "set": {
            "key": "best_key",
            "value": {
              "calc": "max([p.bid * tiebreak_multiplier + (len(players) - 1 - ((p.seat - first_seat) % len(players))) for p in players if p.bid_valid] + [0])"
            }
          }
        },
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "max([p.seat for p in players if p.bid_valid and p.bid * tiebreak_multiplier + (len(players) - 1 - ((p.seat - first_seat) % len(players))) == best_key] + [no_leader_code])"
            },
            "if": {
              "calc": "any(p.bid_valid for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "standing_bid",
            "value": {
              "calc": "max([p.bid for p in players if p.bid_valid] + [0])"
            },
            "if": {
              "calc": "any(p.bid_valid for p in players)"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "bidding",
      "label": "final standing bid",
      "when": {
        "calc": "leader != no_leader_code"
      },
      "to": "all",
      "text": "Final standing bid {standing_bid} by seat {leader}."
    },
    {
      "use": "tell",
      "phase": "bidding",
      "label": "no final bid",
      "when": {
        "calc": "leader == no_leader_code"
      },
      "to": "all",
      "text": "No bid; item {round} goes unsold."
    },
    {
      "use": "update",
      "phase": "resolution",
      "label": "the item is resolved",
      "do": [
        {
          "adjust": {
            "players": {
              "where": "you.seat == leader and you.budget >= standing_bid"
            },
            "key": "score",
            "value": {
              "calc": "you.values[round - 1] - standing_bid"
            },
            "if": {
              "calc": "leader != no_leader_code"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat == leader and you.budget >= standing_bid"
            },
            "key": "budget",
            "value": {
              "calc": "-standing_bid"
            },
            "if": {
              "calc": "leader != no_leader_code"
            }
          }
        },
        {
          "set": {
            "key": "last_price",
            "value": {
              "calc": "standing_bid"
            },
            "if": {
              "calc": "leader != no_leader_code"
            },
            "text": "Item {round} sold to seat {leader} for {standing_bid}."
          }
        },
        {
          "set": {
            "key": "last_price",
            "value": 0,
            "if": {
              "calc": "leader == no_leader_code"
            },
            "text": "Item {round} unsold."
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolution",
      "label": "advance the round",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "resolution",
      "label": "after the last item",
      "when": {
        "calc": "round > rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round > rounds"
      },
      "rank_by": "you.score",
      "text": "Winner: {result}. Final scores [seat, score]: {[[p.seat, p.score] for p in players]}."
    }
  },
  "limits": {
    "rounds": 6,
    "rounds_max": 6,
    "actions_max": 1000,
    "deadline_s": 120
  },
  "rules": "There are {items} items, auctioned one per round in a known order: item 1 in round 1, and so on to item {items} in round {rounds}. Before round 1, each player is privately dealt the six values {item_value_1}, {item_value_2}, {item_value_3}, {item_value_4}, {item_value_5} and {item_value_6} in a random order: one value per item, each value used exactly once. Each player sees only their own values. Every player's values sum to {value_sum}. Each player starts with a budget of {starting_budget} coins and a score of {starting_score}. Seats are numbered 1 to N.\n\nPRIORITY. In round r, the tie-break priority goes to seat ((r - 1) mod N) + 1 first, then the following seats in increasing order, wrapping around (with 3 players, round 2's order is 2, 3, 1). The priority order is announced at the start of the round.\n\nEACH ROUND (one item):\n1. The item number, the priority order, and every player's remaining budget and score are announced. Budgets and scores are public.\n2. Talk: every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Messages bind nobody.\n3. Bidding turn 1: every player at the same time either submits a whole-number bid of at least {min_bid} or passes (answers 0). A bid is valid only if it does not exceed the bidder's remaining budget; an invalid bid counts as a pass. If at least one valid bid was made, the highest becomes the standing bid and its bidder becomes the leader. Equal highest bids go to the player earliest in this round's priority order. If no valid bid was made, there is no standing bid and no leader.\n4. The standing bid and the leader are announced, or that there is no bid.\n5. Bidding turn 2: every player at the same time either passes (0) or submits a whole-number bid. To be valid, the bid must be at least the standing bid plus {min_raise} (at least {min_bid} if there is no standing bid) and must not exceed the bidder's remaining budget; otherwise it counts as a pass. The leader may also bid, though they need not. If any valid bid was made, the highest becomes the new standing bid and its bidder the new leader, with ties broken by priority. If nobody makes a valid bid, the standing bid and leader stay as they were. A player whose budget is below the lowest valid bid is not asked and passes.\n6. The standing bid and the leader are announced.\n7. Bidding turn 3: same as turn 2.\n8. The final standing bid and the leader are announced.\n9. Resolution: if there is a leader, that player wins the item. They pay the standing bid from their budget, and their score changes by (their private value for this item minus the standing bid), which may be negative (value 7 bought at 10 gives -3). The price is announced, but the winner's value stays private. If there is no leader, the item goes unsold, nobody pays and nobody scores for it.\n10. Advance to the next round. After round {rounds} the game ends.\n\nUnspent coins are worth nothing at the end. Scores count only item values won minus prices paid. After round {rounds}, the player with the highest score wins; players level at the highest score share the win (a draw)."
}
```
````
