# Task: write the XColos game file for "Hidden-Pot Ultimatum (Three Players)"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

SETUP: Three players, seats 1, 2 and 3. Everyone starts with 0 points. Totals are private: each player is told only their own total until the game ends. Each player will propose in exactly two rounds. For each player, one of those two rounds has a pot of 12 and the other a pot of 24. The order is secret and random.

PROPOSER ORDER: Round 1: seat 1. Round 2: seat 2. Round 3: seat 3. Round 4: seat 3. Round 5: seat 2. Round 6: seat 1. In each round the other two players are the Responders.

EACH ROUND:
1. Announce the round number and who the Proposer is.
2. Pot. If this is the Proposer's first proposal, the engine flips a fair coin: heads means the pot is 12 this time (and 24 next time), tails means 24 this time (and 12 next time). If it is the Proposer's second proposal, the pot is whichever value was not used the first time.
3. Tell the pot privately to the Proposer only.
4. Talk: all three players each write one short message at the same time, without seeing the others' messages. The Proposer may state, hint at or lie about the pot. Nothing said is binding.
5. Show all three messages to everyone.
6. The Proposer chooses two whole numbers: an offer to each Responder, each from 0 to 6. The two offers may differ. The Proposer's keep is the pot minus both offers (always at least 0).
7. Announce both offers to everyone. The pot and the keep are not announced.
8. The two Responders each choose Accept or Reject at the same time.
9. Announce both votes.
10. If both accepted, the deal passes: each Responder adds their offer to their total, and the Proposer adds their keep.
11. If at least one rejected, the deal fails: nobody receives an offer or a keep. The Proposer instead loses one third of their keep, rounded down (keep 12 loses 4, keep 6 loses 2, keep 2 loses 0).
12. In either case, each Responder who chose Reject loses 1 point.
13. Tell each player privately their own new total.

END: After round 6, reveal every round's pot and keep and every player's total. Totals may be negative.

How the winner is decided: The player with the strictly highest final total wins. If two or three players tie for the highest total, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Hidden-Pot Ultimatum (Three Players) (3 to 3 players, best with 3)

Over six rounds each of three players twice proposes how to split a secret pot of 12 or 24. They offer each of the other two 0 to 6 points, and both must accept or the deal fails and the Proposer is penalised.

STATE (every item below must exist in the file):
  - each player: total (number, starts 0); only its owner sees it. The player's points. Only the owner sees it until the game ends, when it becomes public. It may go negative.
  - each player: offer (number, starts 0); everyone sees it. This round's offer to this player while they are a Responder. It is 0 for the Proposer and is announced.
  - each player: vote (text, starts ''); everyone sees it. This round's vote while a Responder: accept, reject, or empty for the Proposer.
  - the table: round (number, starts 0); everyone sees it. The current round number, from 1 to 6.
  - the table: proposer (number, starts 0); everyone sees it. The seat of this round's Proposer.
  - the table: pot (number, starts 0); hidden from all players. This round's pot of 12 or 24. It is told privately to the Proposer only.
  - the table: keep (number, starts 0); hidden from all players. This round's keep, equal to pot minus both offers. It is not announced.
  - the table: second_pot_s1 (number, starts 0); hidden from all players. Seat 1's pot for its second proposal, set at its first proposal (0 = not yet flipped).
  - the table: second_pot_s2 (number, starts 0); hidden from all players. Seat 2's pot for its second proposal (0 = not yet flipped).
  - the table: second_pot_s3 (number, starts 0); hidden from all players. Seat 3's pot for its second proposal (0 = not yet flipped).
  - the table: pot_history (list, starts []); hidden from all players. Every round's pot in order. It is revealed after round 6.
  - the table: keep_history (list, starts []); hidden from all players. Every round's keep in order. It is revealed after round 6.
  - the table: top_total (number, starts 0); everyone sees it. The highest final total, computed after round 6.
  - the table: top_count (number, starts 0); everyone sees it. How many players hold the highest final total, computed after round 6.
  - parameters, each kept as a table attribute: num_players = 3, num_rounds = 6, starting_total = 0, pot_low = 12, pot_high = 24, pot_sum = 36, coin_heads_probability = 0.5, offer_min = 0, offer_max = 6, fail_keep_loss_divisor = 3, reject_penalty = 1, proposer_round_1 = 1, proposer_round_2 = 2, proposer_round_3 = 3, proposer_round_4 = 3, proposer_round_5 = 2, proposer_round_6 = 1, tie_block_margin = 1000

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seats 1, 2 and 3 each start with total = 0, visible only to themselves.
  2. The proposer order is fixed: rounds 1 to 6 are proposed by seats 1, 2, 3, 3, 2, 1.
  3. Each seat's pot order (12 then 24, or 24 then 12) is secret and decided by a fair coin at that seat's first proposal. second_pot_s1, second_pot_s2 and second_pot_s3 start at 0.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round += 1; proposer = the seat for this round from the order 1,2,3,3,2,1; every player's offer = 0 and vote = ''.
  2. [tell] all players. What happens: Announce 'Round {round}: the Proposer is seat {proposer}; the other two seats are Responders.'
  3. [update] all players. What happens: If second_pot_s{proposer} == 0 (first proposal), flip a fair coin: on heads pot = 12, on tails pot = 24, then second_pot_s{proposer} = 36 - pot. Otherwise pot = second_pot_s{proposer}. Append pot to pot_history.
  4. [tell] seat {proposer}. What happens: Privately tell the Proposer: 'The pot this round is {pot}.'
  5. [poll] all players answers: short text (one message; the Proposer may state, hint at or lie about the pot; nothing is binding). What happens: Broadcast to all: 'Seat {seat} says: {value}'. All messages are shown only after all three are in.
  6. [ask] seat {proposer} answers: a whole number from 0 to 6: the offer to the lower-numbered Responder. What happens: offer of the lower-numbered Responder = answer.
  7. [ask] seat {proposer} answers: a whole number from 0 to 6: the offer to the higher-numbered Responder. What happens: offer of the higher-numbered Responder = answer.
  8. [update] all players. What happens: keep = pot - (sum of both Responders' offer), which is always at least 0. Append keep to keep_history.
  9. [tell] all players. What happens: Announce both offers: 'Seat X is offered {offer}, seat Y is offered {offer}.' The pot and the keep are not announced.
  10. [poll] the two Responders (every seat except proposer) answers: accept | reject. What happens: Each Responder's vote = answer. Both are chosen simultaneously.
  11. [tell] all players. What happens: Announce both votes.
  12. [update] all players. What happens: If both Responders' vote == accept: each Responder's total += their offer, and the Proposer's total += keep. Otherwise the Proposer's total -= floor(keep / 3) and no offer or keep is paid. In either case, each Responder with vote == reject has total -= 1.
  13. [sync] all players. What happens: Each player is privately sent their own new total.
  14. [update] all players. What happens: When round == 6: top_total = the maximum total over all players; top_count = the number of players with total == top_total; every player's total becomes public.
  15. [tell] all players. What happens: When round == 6: reveal pot_history, keep_history and every player's total.
  16. [check] all players. What happens: If round == 6, end the game; otherwise continue to the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, then every seat's total is 0 and each seat sees only its own total.
  R2. When rounds 1 to 6 are played, then the Proposers are seats 1, 2, 3, 3, 2, 1 in that order, and the other two seats are the Responders.
  R3. When a seat proposes for the first time, then a fair coin sets the pot to 12 (heads) or 24 (tails), and that seat's second pot is set to 36 minus that pot.
  R4. When a seat proposes for the second time, then the pot is the value it did not have the first time, so over its two proposals each seat has one pot of 12 and one of 24.
  R5. When the pot is set, then it is told privately to the Proposer only and is not announced to the Responders.
  R6. When the talk step happens, then all three players each submit one short message simultaneously, and all three are shown to everyone only after all are in.
  R7. When the Proposer makes offers, then each Responder is offered a whole number from 0 to 6, and the two offers may differ.
  R8. When offers are made, then keep = pot - offer_A - offer_B (for example, pot 24 with offers 3 and 5 gives keep 16), and the keep is never below 0.
  R9. When offers are made, then both offers are announced to everyone, and the pot and the keep are not announced.
  R10. When the Responders vote, then each chooses accept or reject simultaneously, and both votes are then announced.
  R11. When both Responders accept, then each Responder's total rises by their offer and the Proposer's total rises by the keep.
  R12. When at least one Responder rejects, then no offer or keep is paid and the Proposer's total falls by floor(keep / 3): keep 12 loses 4, keep 6 loses 2, keep 2 loses 0.
  R13. When a Responder votes reject, then that Responder's total falls by 1, whether or not the deal passed.
  R14. When a round ends, then each player is privately told only their own new total.
  R15. When round 6 ends, then the game ends and every round's pot, every round's keep and every player's total are revealed. Totals may be negative.
  R16. When the game ends and exactly one player has the highest total, then that player wins.
  R17. When the game ends and two or three players tie for the highest total, then nobody wins and the game is a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Talk message each round | asked: all three seats | options: any short text
  - Offer to the lower-numbered Responder | asked: the Proposer only | options: whole numbers 0, 1, 2, 3, 4, 5, 6
  - Offer to the higher-numbered Responder | asked: the Proposer only | options: whole numbers 0, 1, 2, 3, 4, 5, 6
  - Vote on the deal | asked: the two Responders (never the Proposer) | options: accept, reject

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round == 6
  - each player's standing: you.total (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - min_to_win: top_total + 1000 * (top_count - 1) (a player whose standing is below it cannot win; if none reaches it, the match ends with no winner)
  - how the result is decided: Each player's standing is their final total. The single player with the strictly highest total wins. If two or three players tie for the highest total, the bar cannot be reached, nobody wins, and the game is a draw.
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

- each player: `total` (number, visible: ally, starts 0): The player's points. Only the owner sees it until the game ends, when it becomes public. It may go negative.
- each player: `offer` (number, visible: public, starts 0): This round's offer to this player while they are a Responder. It is 0 for the Proposer and is announced.
- each player: `vote` (text, visible: public, starts ''): This round's vote while a Responder: accept, reject, or empty for the Proposer.
- the table: `round` (number, visible: public, starts 0): The current round number, from 1 to 6.
- the table: `proposer` (number, visible: public, starts 0): The seat of this round's Proposer.
- the table: `top_total` (number, visible: public, starts 0): The highest final total, computed after round 6.
- the table: `top_count` (number, visible: public, starts 0): How many players hold the highest final total, computed after round 6.
- parameters (each must be an attribute holding this value, never a number buried in a step): num_players = 3, num_rounds = 6, starting_total = 0, pot_low = 12, pot_high = 24, pot_sum = 36, coin_heads_probability = 0.5, offer_min = 0, offer_max = 6, fail_keep_loss_divisor = 3, reject_penalty = 1, proposer_round_1 = 1, proposer_round_2 = 2, proposer_round_3 = 3, proposer_round_4 = 3, proposer_round_5 = 2, proposer_round_6 = 1, tie_block_margin = 1000
- the game ends with ONE ending whose `rank_by` is `you.total`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
- that ending's `min_to_win` is `top_total + 1000 * (top_count - 1)`: a player below it cannot win, and if nobody reaches it the match ends with no winner
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
