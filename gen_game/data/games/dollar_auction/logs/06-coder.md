# 06 coder

- time: 2026-10-27T18:18:54+00:00 (69.2s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 ce7bc70e04ac2927, reply sha256 ca90d8b3e38cc4ea

## Sent

````
# Task: write the XColos game file for "Collector's Dollar Auction"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 4 to 4; set `meta.players` to {"min": 4, "max": 4, "suggested": 4} (the suggested size is the one the game plays best at).

SETUP: There are exactly 4 players. Each starts with 40 coins (public) and 0 prize points (private). At the start, two players are secretly dealt the type Red and two the type Blue, uniformly at random. Each player knows only their own type. The game lasts 8 rounds. Odd rounds (1, 3, 5, 7) offer a Red prize and even rounds (2, 4, 6, 8) offer a Blue prize. A prize is worth 12 prize points to a player whose type matches its colour and 6 prize points to a player whose type does not. Coins and all bids are public. Prize points are private until the end.

EACH ROUND:
1. Announce the round number and the prize colour.
2. TALK: every player writes one short message at the same time, without seeing the others. All four messages are then shown to everyone. Messages are not binding.
3. OPENING BID: every player at the same time secretly chooses a whole-number opening bid from 0 up to their current coins.
4. Reveal all opening bids. The CONTENDERS are every player whose opening bid is greater than 0 and at least as large as the second-highest opening bid (ties included). If only one player bid more than 0, that player is the sole contender. If nobody bid more than 0, there are no contenders.
5. RAISE 1: if there are at least two contenders, each contender at the same time chooses a whole-number raise from 0 up to (their current coins minus what they have already bid this round). A contender who raises 0 has dropped out and may not raise again this round.
6. Reveal all Raise 1 amounts and each player's running total bid.
7. RAISE 2: if at least two contenders raised more than 0 in Raise 1, each of those contenders at the same time chooses a further whole-number raise from 0 up to (current coins minus what they have already bid this round). Contenders who dropped out in Raise 1 add nothing.
8. Reveal Raise 2 amounts and final total bids. A player's total bid is their opening bid plus their raises.
9. The round winner is the single player with the highest total bid. If two or more players tie for the highest total bid, nobody wins the prize this round.
10. PAYMENT: every player, winner or not, loses coins equal to their total bid.
11. The round winner, if any, privately gains 12 prize points if the prize colour matches their type, otherwise 6. Everyone is told who won, but not how many points they gained.
12. Go to the next round. After round 8 the game ends.

END: Each player's final score is their coins plus their prize points. All scores and types are revealed.

How the winner is decided: The player with the highest final score (coins plus prize points) wins. If two or more players tie for the highest score, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Collector's Dollar Auction (4 to 4 players, best with 4)

Four players with hidden Red or Blue types bid over 8 rounds for alternating Red and Blue prizes; every player pays their own bid, win or lose, and the highest coins plus prize points wins.

STATE (every item below must exist in the file):
  - each player: coins (number, starts 40); everyone sees it. Coins held. Bids are paid from these.
  - each player: prize_points (number, starts 0); only its owner sees it. Prize points won. Private until the end, then revealed.
  - each player: type (text, starts ''); only its owner sees it. Secret type, Red or Blue, dealt at setup. Revealed at the end.
  - each player: opening_bid (number, starts 0); everyone sees it. This round's opening bid. Revealed after the simultaneous choice.
  - each player: raise1 (number, starts 0); everyone sees it. This round's Raise 1 amount (0 if not a contender or dropped out).
  - each player: raise2 (number, starts 0); everyone sees it. This round's Raise 2 amount (0 if not eligible).
  - each player: total_bid (number, starts 0); everyone sees it. opening_bid + raise1 + raise2 for this round.
  - each player: contender (bool, starts False); everyone sees it. True if opening_bid > 0 and opening_bid >= second_highest_opening.
  - each player: score (number, starts 0); everyone sees it. Final score, coins + prize_points, set at game end.
  - the table: round (number, starts 0); everyone sees it. Current round number, 1 to 8.
  - the table: prize_colour (text, starts ''); everyone sees it. Red in odd rounds, Blue in even rounds.
  - the table: type_deck (list, starts ['Red', 'Red', 'Blue', 'Blue']); hidden from all players. Types dealt at random, one to each player, at setup.
  - the table: second_highest_opening (number, starts 0); everyone sees it. Second-highest of the four opening bids this round, ties counted (the 2nd value when sorted descending).
  - the table: contender_count (number, starts 0); everyone sees it. Number of contenders this round.
  - the table: raise2_count (number, starts 0); everyone sees it. Number of contenders with raise1 > 0.
  - the table: highest_total (number, starts 0); everyone sees it. Highest total_bid this round.
  - the table: top_count (number, starts 0); everyone sees it. Number of players whose total_bid equals highest_total.
  - the table: round_winner (number, starts 0); everyone sees it. Seat that won this round's prize, or 0 if nobody won.
  - parameters, each kept as a table attribute: player_count = 4, starting_coins = 40, starting_prize_points = 0, red_types = 2, blue_types = 2, rounds = 8, match_prize_points = 12, mismatch_prize_points = 6, min_bid = 0, min_contenders_for_raise = 2, raise_rounds = 2

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Each of the 4 players starts with coins = 40 and prize_points = 0.
  2. The type_deck holds Red, Red, Blue, Blue. Each player draws one type at random into their own type attribute (visible only to them), and it is removed from type_deck.
  3. round is set to 0.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round += 1; prize_colour = 'Red' if round is odd, else 'Blue'; for every player opening_bid = 0, raise1 = 0, raise2 = 0, total_bid = 0, contender = false; round_winner = 0.
  2. [tell] all players. What happens: Announce: 'Round {round} of 8: the prize is {prize_colour}.'
  3. [poll] all players answers: one short free-text message. What happens: Every message is broadcast to all: 'Seat {seat} says: {value}'. Messages are not binding.
  4. [poll] all players answers: a whole number from 0 to your coins. What happens: Set each player's opening_bid. Nobody sees a bid until all are in.
  5. [update] all players. What happens: Reveal all opening_bid values. second_highest_opening = the 2nd value of the four opening bids sorted descending. For each player, contender = (opening_bid > 0 and opening_bid >= second_highest_opening). contender_count = number of players with contender true.
  6. [poll] each player with contender true, only when contender_count >= 2 answers: a whole number from 0 to (coins - opening_bid). What happens: Set raise1 for each contender. A raise of 0 means that contender has dropped out for this round.
  7. [update] all players. What happens: Reveal raise1 values and running totals opening_bid + raise1. raise2_count = number of contenders with raise1 > 0.
  8. [poll] each contender with raise1 > 0, only when raise2_count >= 2 answers: a whole number from 0 to (coins - opening_bid - raise1). What happens: Set raise2 for each eligible contender.
  9. [update] all players. What happens: For each player total_bid = opening_bid + raise1 + raise2. Reveal raise2 values and every total_bid. highest_total = max total_bid; top_count = number of players with total_bid == highest_total. round_winner = the seat with total_bid == highest_total if top_count == 1 and highest_total > 0, else 0.
  10. [update] all players. What happens: Payment: each player coins -= total_bid, winner or not.
  11. [update] the round winner, only when round_winner != 0. What happens: Winner's prize_points += 12 if type == prize_colour, else += 6 (private). Announce to all: 'Seat {round_winner} wins the {prize_colour} prize' (or 'Nobody wins the prize' if round_winner == 0), without the points gained.
  12. [sync] all players. What happens: Each player is sent their own state: coins, prize_points, type.
  13. [check] all players. What happens: If round == 8: for each player score = coins + prize_points; reveal every type, prize_points and score to all; end the game. Otherwise continue to the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, then every player has 40 coins and 0 prize points.
  R2. When types are dealt, then exactly 2 players have type Red and 2 have type Blue, and each player sees only their own type.
  R3. When the round is odd (1, 3, 5, 7), then the prize is Red. When it is even (2, 4, 6, 8), then the prize is Blue.
  R4. When the talk step runs, then every player submits one message at the same time and all four messages are shown to everyone.
  R5. When opening bids are made, then every player simultaneously picks a whole number from 0 to their current coins.
  R6. When opening bids are revealed, then a player is a contender if and only if their opening bid is > 0 and >= the second-highest opening bid (ties counted). For example, bids 5,5,5,2 give three contenders, and bids 7,0,0,0 make the bidder of 7 the sole contender.
  R7. When all opening bids are 0, then there are no contenders and nobody wins the prize.
  R8. When there are at least 2 contenders, then each contender simultaneously chooses a Raise 1 from 0 to (coins - opening bid). Non-contenders are not asked.
  R9. When fewer than 2 contenders exist, then Raise 1 and Raise 2 are skipped.
  R10. When a contender raises 0 in Raise 1, then they have dropped out and are not asked in Raise 2.
  R11. When at least 2 contenders raised more than 0 in Raise 1, then each of them simultaneously chooses a Raise 2 from 0 to (coins - opening bid - Raise 1). Otherwise Raise 2 is skipped.
  R12. When bidding ends, then each player's total bid = opening bid + Raise 1 + Raise 2.
  R13. When exactly one player has the highest total bid, then that player wins the round's prize.
  R14. When two or more players tie for the highest total bid, then nobody wins the prize that round.
  R15. When payment happens, then every player, winner or not, loses coins equal to their own total bid.
  R16. When the winner's type matches the prize colour, then they gain 12 prize points. Otherwise they gain 6.
  R17. When a round's prize is won, then everyone is told who won but not how many points were gained.
  R18. When round 8 ends, then the game ends, each score = coins + prize points, and all scores and types are revealed.
  R19. When the game ends, then the highest score wins, and tied top scores share the result (a draw).

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Talk message | asked: all four seats | options: one short free-text message
  - Opening bid | asked: all four seats | options: a whole number from 0 to that seat's current coins
  - Raise 1 (only when contender_count >= 2) | asked: each seat with contender true | options: a whole number from 0 to (coins - opening_bid). Non-contenders are not asked.
  - Raise 2 (only when raise2_count >= 2) | asked: each contender with raise1 > 0 | options: a whole number from 0 to (coins - opening_bid - raise1). Dropped-out contenders and non-contenders are not asked.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round == 8 (after the round-8 steps)
  - each player's standing: you.coins + you.prize_points (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's final score is coins plus prize points. The highest score wins, and players tied at the top share the result (the source's draw).
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

- each player: `coins` (number, visible: public, starts 40): Coins held. Bids are paid from these.
- each player: `prize_points` (number, visible: ally, starts 0): Prize points won. Private until the end, then revealed.
- each player: `score` (number, visible: public, starts 0): Final score, coins + prize_points, set at game end.
- the table: `round` (number, visible: public, starts 0): Current round number, 1 to 8.
- the table: `round_winner` (number, visible: public, starts 0): Seat that won this round's prize, or 0 if nobody won.
- parameters (each must be an attribute holding this value, never a number buried in a step): player_count = 4, starting_coins = 40, starting_prize_points = 0, red_types = 2, blue_types = 2, rounds = 8, match_prize_points = 12, mismatch_prize_points = 6, min_bid = 0, min_contenders_for_raise = 2, raise_rounds = 2
- the game ends with ONE ending whose `rank_by` is `you.coins + you.prize_points`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
    "id": "collectors_dollar_auction",
    "name": "Collector's Dollar Auction",
    "players": {
      "min": 4,
      "max": 4,
      "suggested": 4
    },
    "blurb": "Four players with secret Red or Blue types bid for alternating prizes over 8 rounds; everyone pays their own bid, win or lose."
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
        "key": "prize_points",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "type",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "opening_bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "raise1",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "raise2",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "total_bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "contender",
        "visible": "public",
        "type": "bool",
        "initial": false
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
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "prize_colour",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "type_deck",
        "visible": "none",
        "type": "list",
        "initial": [
          "Red",
          "Red",
          "Blue",
          "Blue"
        ]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "second_highest_opening",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "contender_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "raise2_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "highest_total",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "top_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "round_winner",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "player_count",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "starting_coins",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "starting_prize_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "red_types",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "blue_types",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "match_prize_points",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "mismatch_prize_points",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "min_bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "min_contenders_for_raise",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "raise_rounds",
        "visible": "public",
        "type": "number",
        "initial": 2
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
            "key": "coins",
            "value": {
              "calc": "starting_coins"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "prize_points",
            "value": {
              "calc": "starting_prize_points"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "deal the types",
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "type_deck[min(len(type_deck) - 1, int(uniform(0, len(type_deck))))]"
            }
          }
        },
        {
          "set": {
            "player": 1,
            "key": "type",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "type_deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "type_deck[min(len(type_deck) - 1, int(uniform(0, len(type_deck))))]"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "type",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "type_deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "type_deck[min(len(type_deck) - 1, int(uniform(0, len(type_deck))))]"
            }
          }
        },
        {
          "set": {
            "player": 3,
            "key": "type",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "type_deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "type_deck[0]"
            }
          }
        },
        {
          "set": {
            "player": 4,
            "key": "type",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "type_deck",
            "value": {
              "calc": "pick"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "set the round counter",
      "do": [
        {
          "set": {
            "key": "round",
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
      "fields": [
        "coins",
        "prize_points",
        "type"
      ],
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "start",
      "label": "new round",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "key": "prize_colour",
            "value": {
              "calc": "'Red' if round - 2 * int(round / 2) == 1 else 'Blue'"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "opening_bid",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "raise1",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "raise2",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "total_bid",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "contender",
            "value": false
          }
        },
        {
          "set": {
            "key": "round_winner",
            "value": 0
          }
        },
        {
          "set": {
            "key": "contender_count",
            "value": 0
          }
        },
        {
          "set": {
            "key": "raise2_count",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "start",
      "label": "announce the prize",
      "to": "all",
      "text": "Round {round} of {rounds}: the prize is {prize_colour}."
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
      "text": "Write one short message to the table. Everyone writes at the same time; all messages are then shown to everyone. Messages are not binding."
    },
    {
      "use": "poll",
      "phase": "bid",
      "label": "opening bid",
      "to": "acting",
      "answer": {
        "type": "number",
        "min": {
          "calc": "min_bid"
        },
        "max": {
          "calc": "you.coins"
        }
      },
      "store": "opening_bid",
      "text": "Round {round}, {prize_colour} prize. Choose your secret opening bid: a whole number from 0 up to your coins. You pay your total bid whether you win or not."
    },
    {
      "use": "update",
      "phase": "bid",
      "label": "reveal opening bids",
      "do": [
        {
          "set": {
            "key": "second_highest_opening",
            "value": {
              "calc": "sorted([p.opening_bid for p in players])[player_count - 2]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "contender",
            "value": {
              "calc": "you.opening_bid > 0 and you.opening_bid >= second_highest_opening"
            }
          }
        },
        {
          "set": {
            "key": "contender_count",
            "value": {
              "calc": "count(p.contender for p in players)"
            }
          }
        }
      ],
      "text": "Opening bids: Seat 1 {players[0].opening_bid}, Seat 2 {players[1].opening_bid}, Seat 3 {players[2].opening_bid}, Seat 4 {players[3].opening_bid}. Second-highest opening bid: {second_highest_opening}. Contenders: {contender_count}."
    },
    {
      "use": "poll",
      "phase": "raise",
      "label": "raise 1",
      "when": {
        "calc": "contender_count >= min_contenders_for_raise"
      },
      "to": {
        "where": "you.contender"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "min_bid"
        },
        "max": {
          "calc": "you.coins - you.opening_bid"
        }
      },
      "store": "raise1",
      "text": "Raise 1: you are a contender. Choose a secret raise from 0 up to your coins minus your opening bid. A raise of 0 means you drop out and cannot raise again this round."
    },
    {
      "use": "update",
      "phase": "raise",
      "label": "reveal raise 1",
      "when": {
        "calc": "contender_count >= min_contenders_for_raise"
      },
      "do": [
        {
          "set": {
            "key": "raise2_count",
            "value": {
              "calc": "count(p.contender and p.raise1 > 0 for p in players)"
            }
          }
        }
      ],
      "text": "Raise 1: Seat 1 {players[0].raise1} (total {players[0].opening_bid + players[0].raise1}), Seat 2 {players[1].raise1} (total {players[1].opening_bid + players[1].raise1}), Seat 3 {players[2].raise1} (total {players[2].opening_bid + players[2].raise1}), Seat 4 {players[3].raise1} (total {players[3].opening_bid + players[3].raise1})."
    },
    {
      "use": "poll",
      "phase": "raise",
      "label": "raise 2",
      "when": {
        "calc": "raise2_count >= min_contenders_for_raise"
      },
      "to": {
        "where": "you.contender and you.raise1 > 0"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "min_bid"
        },
        "max": {
          "calc": "you.coins - you.opening_bid - you.raise1"
        }
      },
      "store": "raise2",
      "text": "Raise 2: choose a secret further raise from 0 up to your coins minus what you have already bid this round. This is the last raise."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "final bids",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "total_bid",
            "value": {
              "calc": "you.opening_bid + you.raise1 + you.raise2"
            }
          }
        },
        {
          "set": {
            "key": "highest_total",
            "value": {
              "calc": "max([p.total_bid for p in players])"
            }
          }
        },
        {
          "set": {
            "key": "top_count",
            "value": {
              "calc": "count(p.total_bid == highest_total for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "round_winner",
            "value": {
              "calc": "min([p.seat for p in players if p.total_bid == highest_total]) if top_count == 1 and highest_total > 0 else 0"
            }
          }
        }
      ],
      "text": "Raise 2: Seat 1 {players[0].raise2}, Seat 2 {players[1].raise2}, Seat 3 {players[2].raise2}, Seat 4 {players[3].raise2}. Total bids: Seat 1 {players[0].total_bid}, Seat 2 {players[1].total_bid}, Seat 3 {players[2].total_bid}, Seat 4 {players[3].total_bid}."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "payment",
      "do": [
        {
          "adjust": {
            "players": "all",
            "key": "coins",
            "value": {
              "calc": "-you.total_bid"
            },
            "if": {
              "calc": "you.total_bid <= you.coins"
            }
          }
        }
      ],
      "text": "Every player pays their own total bid, winner or not."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "the prize",
      "when": {
        "calc": "round_winner != 0"
      },
      "do": [
        {
          "adjust": {
            "players": {
              "where": "you.seat == round_winner"
            },
            "key": "prize_points",
            "value": {
              "calc": "match_prize_points if you.type == prize_colour else mismatch_prize_points"
            }
          }
        }
      ],
      "text": "Seat {round_winner} wins the {prize_colour} prize."
    },
    {
      "use": "tell",
      "phase": "resolve",
      "label": "no winner",
      "when": {
        "calc": "round_winner == 0"
      },
      "to": "all",
      "text": "Nobody wins the {prize_colour} prize this round."
    },
    {
      "use": "sync",
      "phase": "resolve",
      "label": "your standing",
      "mode": "self",
      "to": "all",
      "fields": [
        "coins",
        "prize_points",
        "type"
      ],
      "text": "Where you stand:"
    },
    {
      "use": "update",
      "phase": "end",
      "label": "final scores",
      "when": {
        "calc": "round >= rounds"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "you.coins + you.prize_points"
            }
          }
        }
      ],
      "text": "Final: Seat 1 is {players[0].type} with {players[0].prize_points} prize points, score {players[0].score}; Seat 2 is {players[1].type} with {players[1].prize_points}, score {players[1].score}; Seat 3 is {players[2].type} with {players[2].prize_points}, score {players[2].score}; Seat 4 is {players[3].type} with {players[3].prize_points}, score {players[3].score}."
    },
    {
      "use": "check",
      "phase": "end",
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
      "rank_by": "you.coins + you.prize_points",
      "reveal": [
        "type",
        "prize_points",
        "score"
      ],
      "text": "Winner: {result}. Final scores: Seat 1 {players[0].score}, Seat 2 {players[1].score}, Seat 3 {players[2].score}, Seat 4 {players[3].score}."
    }
  },
  "limits": {
    "rounds": 8,
    "rounds_max": 8,
    "actions_max": 400,
    "deadline_s": 120
  },
  "rules": "There are exactly {player_count} players. Each starts with {starting_coins} coins (public) and {starting_prize_points} prize points (private). At the start, {red_types} players are secretly dealt the type Red and {blue_types} the type Blue, uniformly at random. Each player knows only their own type. The game lasts {rounds} rounds. Odd rounds (1, 3, 5, 7) offer a Red prize and even rounds (2, 4, 6, 8) offer a Blue prize. A prize is worth {match_prize_points} prize points to a player whose type matches its colour and {mismatch_prize_points} prize points to a player whose type does not. Coins and all bids are public. Prize points are private until the end.\n\nEACH ROUND:\n1. The round number and the prize colour are announced.\n2. TALK: every player writes one short message at the same time, without seeing the others. All four messages are then shown to everyone. Messages are not binding.\n3. OPENING BID: every player at the same time secretly chooses a whole-number opening bid from 0 up to their current coins.\n4. All opening bids are revealed. The CONTENDERS are every player whose opening bid is greater than 0 and at least as large as the second-highest opening bid (ties included). For example, bids 5,5,5,2 give three contenders. If only one player bid more than 0, that player is the sole contender. If nobody bid more than 0, there are no contenders and nobody wins the prize.\n5. RAISE 1: if there are at least {min_contenders_for_raise} contenders, each contender at the same time chooses a whole-number raise from 0 up to (their current coins minus what they have already bid this round). Non-contenders are not asked. A contender who raises 0 has dropped out and may not raise again this round. If there are fewer than {min_contenders_for_raise} contenders, Raise 1 and Raise 2 are skipped.\n6. All Raise 1 amounts and each player's running total bid are revealed.\n7. RAISE 2: if at least {min_contenders_for_raise} contenders raised more than 0 in Raise 1, each of those contenders at the same time chooses a further whole-number raise from 0 up to (current coins minus what they have already bid this round). Contenders who dropped out in Raise 1 add nothing. Otherwise Raise 2 is skipped.\n8. Raise 2 amounts and final total bids are revealed. A player's total bid is their opening bid plus their raises.\n9. The round winner is the single player with the highest total bid. If two or more players tie for the highest total bid, nobody wins the prize this round.\n10. PAYMENT: every player, winner or not, loses coins equal to their total bid.\n11. The round winner, if any, privately gains {match_prize_points} prize points if the prize colour matches their type, otherwise {mismatch_prize_points}. Everyone is told who won, but not how many points they gained.\n12. Go to the next round. After round {rounds} the game ends.\n\nEND: Each player's final score is their coins plus their prize points. All scores and types are revealed. The player with the highest final score wins; if two or more players tie for the highest score, they share the result (a draw)."
}
```
````
