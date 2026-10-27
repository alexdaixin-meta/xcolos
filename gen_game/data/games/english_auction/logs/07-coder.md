# 07 coder

- time: 2026-10-27T18:19:44+00:00 (71.3s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 9abf1d021e7853f2, reply sha256 58576d38a32b0418

## Sent

````
# Task: write the XColos game file for "Budget English Auctions"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 5; set `meta.players` to {"min": 3, "max": 5, "suggested": 4} (the suggested size is the one the game plays best at).

SETUP
1. Each player starts with 40 coins and a score of 0. Coins and scores are public.
2. Each player gets a private deck of 8 value cards: 2, 4, 6, 8, 10, 12, 14, 16. Each deck is shuffled separately, and its order is secret.
3. Seats are numbered 1 to n.

EACH ROUND (8 rounds; round r):
1. Deal: every player privately sees the next card of their own deck. That is their value for this round's item.
2. Talk: every player writes one short message at the same time without seeing the others. All messages are then shown to everyone. Messages are not binding.
3. Bidding: the standing bid is 0 and there is no leader. Every player starts active. There are up to 3 bidding steps.
   - In each step, every active player who is not the current leader chooses at the same time either to RAISE or to DROP.
   - A RAISE names a whole number at least the standing bid + 2. It may not be more than that player's current coins.
   - A player who DROPs is out of this round's auction.
   - A player with fewer coins than the standing bid + 2 must drop.
   - The leader is not asked and stays in.
4. Resolve each step:
   - If at least one player raised, the highest raise becomes the standing bid and its bidder becomes the leader.
   - Ties for the highest raise go to the tied player with the lowest score. If still tied, they go to the tied player whose seat comes first counting from seat ((r-1) mod n)+1 upward and wrapping around.
   - Players who raised but were outbid remain active.
   - Announce the standing bid, the leader, and who dropped.
   - If nobody raised in a step, bidding ends immediately. Bidding also ends after step 3.
5. Settle:
   - If there is a leader, the leader pays the standing bid from their coins. Their score changes by (their value - standing bid), which may be negative.
   - The leader's value for this round is announced. Nobody else's value is revealed.
   - If nobody ever raised, the item goes unsold and nothing changes.
6. Unspent coins carry over to the next round.

END: after round 8 the game ends.

How the winner is decided: The player with the highest score (total of value minus price over items won) wins. If scores are tied for the top, the tied player with more coins remaining wins. If still tied, the game is a draw among them.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Budget English Auctions (3 to 5 players, best with 4)

Over 8 rounds, players with fixed coin budgets bid for items whose value only they can see, in short ascending auctions of up to 3 simultaneous bidding steps; the winner has the highest total of value minus price.

STATE (every item below must exist in the file):
  - each player: coins (number, starts 40); everyone sees it. Coins left to bid with. Unspent coins carry over between rounds.
  - each player: score (number, starts 0); everyone sees it. Total of (value - price) over all items won. It may be negative.
  - each player: deck (list, starts [2, 4, 6, 8, 10, 12, 14, 16]); only its owner sees it. The player's own private deck of value cards still to come. The next card is drawn from it at random, so its order is secret.
  - each player: value (number, starts 0); only its owner sees it. The player's private value for this round's item, which is the card drawn this round.
  - each player: active (bool, starts True); everyone sees it. Whether the player is still in this round's auction.
  - each player: raise (number, starts 0); only its owner sees it. The player's raise in the current bidding step. 0 means DROP or not asked.
  - each player: priority (number, starts 0); only its owner sees it. Scratch number used to pick the highest raise and break ties: raise*10000 + (500 - score)*10 - ((seat - start_seat + n) mod n), or 0 if the player did not raise.
  - the table: round (number, starts 0); everyone sees it. The current round, from 1 to 8.
  - the table: start_seat (number, starts 1); everyone sees it. The seat that tie-breaks count from this round: ((round-1) mod n)+1.
  - the table: standing_bid (number, starts 0); everyone sees it. The current standing bid in this round's auction.
  - the table: leader (number, starts 0); everyone sees it. The seat of the current leader. 0 means there is no leader.
  - the table: step (number, starts 0); everyone sees it. The current bidding step within the round, from 1 to 3.
  - the table: bidding_open (bool, starts False); everyone sees it. Whether this round's bidding is still going on.
  - the table: revealed_value (number, starts 0); everyone sees it. The value of the leader who bought the item this round, announced at settlement. 0 if the item went unsold.
  - parameters, each kept as a table attribute: starting_coins = 40, starting_score = 0, card_min_value = 2, card_value_step = 2, card_max_value = 16, deck_size = 8, rounds = 8, bidding_steps_max = 3, min_raise_increment = 2, initial_standing_bid = 0, no_leader_code = 0, priority_raise_weight = 10000, priority_score_offset = 500, priority_score_weight = 10, rank_score_weight = 1000

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seats are numbered 1 to n.
  2. Each player gets coins = 40 and score = 0. Both are public.
  3. Each player's private deck is set to the list [2, 4, 6, 8, 10, 12, 14, 16]. Cards are later drawn from it at random, which keeps the order secret and has the same effect as a separate shuffle.
  4. Table: round = 0, standing_bid = 0, leader = 0.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round += 1; start_seat = ((round-1) mod n)+1; standing_bid = 0; leader = 0; step = 0; bidding_open = true; revealed_value = 0; for every player: active = true, raise = 0, priority = 0; for every player: draw one card at random from their deck, set value to it and remove it from deck.
  2. [sync] all players. What happens: Each player privately sees their own value, coins and score, along with all public coins and scores.
  3. [poll] all players answers: one short free-text message. What happens: All messages are collected at once and then broadcast {"to": "all", "text": "Seat {seat} says: {value}"}. Messages are not binding and change no state.
  4. [update] all players. What happens: BIDDING STEP START (when bidding_open): step += 1; every active player who is not the leader and has coins < standing_bid + 2 gets active = false (forced drop); raise = 0 and priority = 0 for all.
  5. [poll] every active player whose seat is not leader (when bidding_open) answers: DROP, or a whole number from standing_bid + 2 to their coins. What happens: Answers are gathered at once, and nobody sees another's answer until all are in. On DROP: active = false and raise = 0. On a number: raise = that number, and the player stays active.
  6. [update] all players. What happens: (when bidding_open) For every player with raise > 0: priority = raise*10000 + (500 - score)*10 - ((seat - start_seat + n) mod n). If any raise > 0: standing_bid = max raise, and leader = the seat with the highest priority (highest raise, then lowest score, then the first seat counting upward from start_seat). Outbid raisers remain active. If no player has raise > 0: bidding_open = false. If step = 3: bidding_open = false.
  7. [tell] all players. What happens: Announce step, standing_bid, leader (or 'no leader') and the seats that dropped this step.
  8. [repeat] all players. What happens: Repeat from BIDDING STEP START (the update, poll, update and tell steps) until bidding_open = false. This happens at the latest after step 3.
  9. [update] the leader. What happens: When leader > 0: the leader's coins -= standing_bid; the leader's score += (leader's value - standing_bid); revealed_value = the leader's value. When leader = 0, nothing changes and the item is unsold.
  10. [tell] all players. What happens: If leader > 0: 'Seat {leader} buys for {standing_bid}; their value was {revealed_value}.' Otherwise: 'The item goes unsold.' No other value is revealed.
  11. [check] all players. What happens: If round >= 8, end the game. Otherwise continue to the next round. Unspent coins carry over.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, then every player has coins = 40 and score = 0, both public.
  R2. When the game starts, then each player's private deck holds exactly the cards 2, 4, 6, 8, 10, 12, 14, 16.
  R3. When a round starts, then each player draws one card from their own deck as their private value, the deck shrinks by one, and after 8 rounds every card has been used exactly once.
  R4. When a round starts, then standing_bid = 0, leader = 0 and every player is active.
  R5. When the talk step runs, then every player sends one message at the same time, and all messages are shown to everyone afterwards with no effect on state.
  R6. When a bidding step runs, then only active players who are not the leader are asked, all at the same time, to RAISE or DROP.
  R7. When a player raises, then the raise is a whole number of at least standing_bid + 2 and at most their coins (e.g. with standing_bid 6 and coins 10, only 8, 9 or 10 is allowed).
  R8. When an active non-leader has coins < standing_bid + 2 at the start of a step, then they are forced to drop and are not asked.
  R9. When a player drops, then they are out of this round's auction (active = false) and are not asked again this round.
  R10. When the leader exists during a step, then the leader is not asked and stays in.
  R11. When at least one player raised in a step, then standing_bid becomes the highest raise and its bidder becomes the leader.
  R12. When two or more players tie for the highest raise, then the one with the lowest score becomes leader.
  R13. When tied raisers also tie on score, then the leader is the first of them counting upward from seat ((r-1) mod n)+1, wrapping around (e.g. in round 2 with 4 seats, seat 2 beats seat 1).
  R14. When a player raised but was outbid, then they remain active for the next step.
  R15. When a step resolves, then the standing bid, the leader and the seats that dropped are announced.
  R16. When nobody raises in a step, then bidding ends immediately.
  R17. When step 3 has resolved, then bidding ends.
  R18. When bidding ends with a leader, then the leader pays standing_bid from coins and their score changes by (value - standing_bid), e.g. value 6 bought at 10 gives score -4.
  R19. When bidding ends with a leader, then the leader's value is announced and no other player's value is revealed.
  R20. When nobody raised during the round, then the item is unsold and no coins or scores change.
  R21. When a round ends, then unspent coins carry over to the next round.
  R22. When round 8 has settled, then the game ends.
  R23. When the game ends, then the highest score wins, ties go to more remaining coins, and players still tied share the win as a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Talk message | asked: every seat | options: one short free-text message
  - Bidding step: RAISE or DROP | asked: every active seat that is not the leader and has coins >= standing_bid + 2 | options: DROP, or a whole number from standing_bid + 2 to that seat's coins
  - Bidding step | asked: the leader | options: not asked; stays in
  - Bidding step | asked: an active non-leader seat with coins < standing_bid + 2 | options: not asked; forced DROP
  - Bidding step | asked: a seat that dropped earlier this round | options: not asked

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round >= 8
  - each player's standing: you.score * 1000 + you.coins (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: The highest score (total of value minus price over items won) wins. A tie on score is broken by more coins remaining. Players still tied share the win, which is a draw among them.
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

- each player: `coins` (number, visible: public, starts 40): Coins left to bid with. Unspent coins carry over between rounds.
- each player: `score` (number, visible: public, starts 0): Total of (value - price) over all items won. It may be negative.
- the table: `round` (number, visible: public, starts 0): The current round, from 1 to 8.
- the table: `standing_bid` (number, visible: public, starts 0): The current standing bid in this round's auction.
- the table: `leader` (number, visible: public, starts 0): The seat of the current leader. 0 means there is no leader.
- the table: `revealed_value` (number, visible: public, starts 0): The value of the leader who bought the item this round, announced at settlement. 0 if the item went unsold.
- parameters (each must be an attribute holding this value, never a number buried in a step): starting_coins = 40, starting_score = 0, card_min_value = 2, card_value_step = 2, card_max_value = 16, deck_size = 8, rounds = 8, bidding_steps_max = 3, min_raise_increment = 2, initial_standing_bid = 0, no_leader_code = 0, priority_raise_weight = 10000, priority_score_offset = 500, priority_score_weight = 10, rank_score_weight = 1000
- the game ends with ONE ending whose `rank_by` is `you.score * 1000 + you.coins`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
```json
{
  "schema": 1,
  "meta": {
    "id": "budget_english_auctions",
    "name": "Budget English Auctions",
    "players": {
      "min": 3,
      "max": 5,
      "suggested": 4
    },
    "blurb": "Eight rounds of short ascending auctions with fixed budgets and private values; the highest total of value minus price wins."
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
        "initial": 40
      },
      {
        "key": "score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "deck",
        "visible": "ally",
        "type": "list",
        "initial": [2, 4, 6, 8, 10, 12, 14, 16]
      },
      {
        "key": "value",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "active",
        "visible": "public",
        "type": "bool",
        "initial": true
      },
      {
        "key": "raise",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "priority",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bid_said",
        "visible": "ally",
        "type": "text",
        "initial": ""
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
        "key": "start_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
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
        "key": "step",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bidding_open",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "revealed_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "dropped_seats",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "top_priority",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "starting_coins",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "starting_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "card_min_value",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "card_value_step",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "card_max_value",
        "visible": "public",
        "type": "number",
        "initial": 16
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "bidding_steps_max",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "min_raise_increment",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "initial_standing_bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "no_leader_code",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "priority_raise_weight",
        "visible": "none",
        "type": "number",
        "initial": 10000
      },
      {
        "key": "priority_score_offset",
        "visible": "none",
        "type": "number",
        "initial": 500
      },
      {
        "key": "priority_score_weight",
        "visible": "none",
        "type": "number",
        "initial": 10
      },
      {
        "key": "rank_score_weight",
        "visible": "public",
        "type": "number",
        "initial": 1000
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "starting purses and decks",
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
            "key": "score",
            "value": {
              "calc": "starting_score"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "deck",
            "value": [2, 4, 6, 8, 10, 12, 14, 16]
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
            "key": "standing_bid",
            "value": {
              "calc": "initial_standing_bid"
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
            "key": "start_seat",
            "value": {
              "calc": "((round - 1) % len(players)) + 1"
            }
          }
        },
        {
          "set": {
            "key": "standing_bid",
            "value": {
              "calc": "initial_standing_bid"
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
            "key": "step",
            "value": 0
          }
        },
        {
          "set": {
            "key": "bidding_open",
            "value": true
          }
        },
        {
          "set": {
            "key": "revealed_value",
            "value": 0
          }
        },
        {
          "set": {
            "key": "dropped_seats",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "active",
            "value": true
          }
        },
        {
          "set": {
            "players": "all",
            "key": "raise",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "priority",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "value",
            "value": {
              "calc": "you.deck[int(uniform(0, len(you.deck)))]"
            }
          }
        },
        {
          "remove": {
            "players": "all",
            "key": "deck",
            "value": {
              "calc": "you.value"
            }
          }
        }
      ],
      "text": "Round {round} of {rounds} begins. Each player has drawn a private value card for this round's item."
    },
    {
      "use": "sync",
      "phase": "deal",
      "label": "your value",
      "mode": "self",
      "to": "all",
      "text": "Your state this round:"
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
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} says: {value}"
      },
      "text": "Round {round}: write one short message to the table. Everyone writes at the same time; all messages are shown afterwards. Messages are not binding."
    },
    {
      "use": "repeat",
      "phase": "bidding",
      "label": "the bidding",
      "until": {
        "calc": "not bidding_open"
      },
      "max": 4,
      "steps": [
        {
          "use": "update",
          "phase": "bidding",
          "label": "bidding step start",
          "do": [
            {
              "adjust": {
                "key": "step",
                "value": 1
              }
            },
            {
              "set": {
                "key": "dropped_seats",
                "value": {
                  "calc": "[p.seat for p in players if p.active and p.seat != leader and p.coins < standing_bid + min_raise_increment]"
                }
              }
            },
            {
              "set": {
                "players": {
                  "where": "you.active and you.seat != leader and you.coins < standing_bid + min_raise_increment"
                },
                "key": "active",
                "value": false,
                "text": "Seat {player} cannot afford the next raise and must drop."
              }
            },
            {
              "set": {
                "players": "all",
                "key": "raise",
                "value": 0
              }
            },
            {
              "set": {
                "players": "all",
                "key": "priority",
                "value": 0
              }
            },
            {
              "set": {
                "players": "all",
                "key": "bid_said",
                "value": ""
              }
            }
          ]
        },
        {
          "use": "poll",
          "phase": "bidding",
          "label": "raise or drop",
          "to": {
            "where": "you.active and you.seat != leader"
          },
          "answer": {
            "type": "number",
            "min": {
              "calc": "standing_bid + min_raise_increment"
            },
            "max": {
              "calc": "you.coins"
            },
            "or": [
              "DROP"
            ]
          },
          "store": "bid_said",
          "text": "Round {round}, bidding step {step}: the standing bid is {standing_bid} (leader seat {leader}; 0 means no leader). RAISE by answering a whole number from the standing bid + {min_raise_increment} up to your coins, or answer DROP to leave this round's auction. Everyone answers at the same time."
        },
        {
          "use": "update",
          "phase": "bidding",
          "label": "resolve the step",
          "do": [
            {
              "set": {
                "key": "dropped_seats",
                "value": {
                  "calc": "dropped_seats + [p.seat for p in players if p.bid_said == 'DROP']"
                }
              }
            },
            {
              "set": {
                "players": {
                  "where": "you.bid_said == 'DROP'"
                },
                "key": "active",
                "value": false
              }
            },
            {
              "set": {
                "players": "all",
                "key": "raise",
                "value": {
                  "calc": "int(you.bid_said) if you.bid_said not in ['', 'DROP'] else 0"
                }
              }
            },
            {
              "set": {
                "players": {
                  "where": "you.raise > 0"
                },
                "key": "priority",
                "value": {
                  "calc": "you.raise * priority_raise_weight + (priority_score_offset - you.score) * priority_score_weight - ((you.seat - start_seat + len(players)) % len(players))"
                }
              }
            },
            {
              "set": {
                "key": "top_priority",
                "value": {
                  "calc": "max([p.priority for p in players])"
                }
              }
            },
            {
              "set": {
                "key": "leader",
                "value": {
                  "calc": "min([p.seat for p in players if p.raise > 0 and p.priority == top_priority])"
                },
                "if": {
                  "calc": "count(p.raise > 0 for p in players) > 0"
                }
              }
            },
            {
              "set": {
                "key": "standing_bid",
                "value": {
                  "calc": "max([p.raise for p in players])"
                },
                "if": {
                  "calc": "count(p.raise > 0 for p in players) > 0"
                }
              }
            },
            {
              "set": {
                "key": "bidding_open",
                "value": {
                  "calc": "count(p.raise > 0 for p in players) > 0 and step < bidding_steps_max"
                }
              }
            }
          ]
        },
        {
          "use": "tell",
          "phase": "bidding",
          "label": "step result",
          "to": "all",
          "text": "Bidding step {step} resolved: standing bid {standing_bid}, leader seat {leader} (0 means no leader). Seats that dropped this step: {dropped_seats}."
        }
      ]
    },
    {
      "use": "update",
      "phase": "settle",
      "label": "settle",
      "when": {
        "calc": "leader != no_leader_code"
      },
      "do": [
        {
          "set": {
            "key": "revealed_value",
            "value": {
              "calc": "sum([p.value for p in players if p.seat == leader])"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "leader"
            },
            "key": "score",
            "value": {
              "calc": "revealed_value - standing_bid"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "leader"
            },
            "key": "coins",
            "value": {
              "calc": "-standing_bid"
            },
            "if": {
              "calc": "sum([p.coins for p in players if p.seat == leader]) >= standing_bid"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "settle",
      "label": "sold",
      "when": {
        "calc": "leader != no_leader_code"
      },
      "to": "all",
      "text": "Seat {leader} buys for {standing_bid}; their value was {revealed_value}."
    },
    {
      "use": "tell",
      "phase": "settle",
      "label": "unsold",
      "when": {
        "calc": "leader == no_leader_code"
      },
      "to": "all",
      "text": "Nobody raised. The item goes unsold and nothing changes."
    },
    {
      "use": "check",
      "phase": "settle",
      "label": "after the last round",
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
      "rank_by": "you.score * 1000 + you.coins",
      "text": "Winner: {result}. Final [seat, score, coins]: {[[p.seat, p.score, p.coins] for p in players]}."
    }
  },
  "limits": {
    "rounds": 8,
    "rounds_max": 10,
    "actions_max": 1000,
    "deadline_s": 120
  },
  "rules": "Each player starts with {starting_coins} coins and a score of {starting_score}. Coins and scores are public. Each player has a private deck of {deck_size} value cards: 2, 4, 6, 8, 10, 12, 14, 16, drawn in a secret random order. Seats are numbered 1 to n.\n\nThe game lasts {rounds} rounds. Each round:\n1. Deal: every player privately sees the next card of their own deck. That is their value for this round's item. Every card is used exactly once over the game.\n2. Talk: every player writes one short message at the same time without seeing the others. All messages are then shown to everyone. Messages are not binding and change nothing.\n3. Bidding: the standing bid is {initial_standing_bid} and there is no leader. Every player starts active. There are up to {bidding_steps_max} bidding steps. In each step, every active player who is not the current leader chooses at the same time either to RAISE or to DROP. A RAISE names a whole number at least the standing bid + {min_raise_increment}, and no more than that player's current coins. A player who DROPs is out of this round's auction and is not asked again this round. A player with fewer coins than the standing bid + {min_raise_increment} must drop and is not asked. The leader is not asked and stays in.\n4. Resolve each step: if at least one player raised, the highest raise becomes the standing bid and its bidder becomes the leader. Ties for the highest raise go to the tied player with the lowest score; if still tied, to the tied player whose seat comes first counting from seat ((r-1) mod n)+1 upward and wrapping around. Players who raised but were outbid remain active. The standing bid, the leader and who dropped are announced. If nobody raised in a step, bidding ends immediately. Bidding also ends after step {bidding_steps_max}.\n5. Settle: if there is a leader, the leader pays the standing bid from their coins and their score changes by (their value - standing bid), which may be negative. The leader's value is announced; nobody else's value is revealed. If nobody ever raised, the item goes unsold and nothing changes.\n6. Unspent coins carry over to the next round.\n\nAfter round {rounds} the game ends. The highest score wins. If scores are tied for the top, the tied player with more coins remaining wins. If still tied, the game is a draw shared among them."
}
```
````
