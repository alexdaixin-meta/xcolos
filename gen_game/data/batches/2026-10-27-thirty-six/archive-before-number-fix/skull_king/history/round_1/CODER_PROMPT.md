# Task: write the XColos game file for "Skull King: Three-Card Raids"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 5; set `meta.players` to {"min": 3, "max": 5, "suggested": 4} (the suggested size is the one the game plays best at).

DECK (18 cards, each with a power value): number cards 1 through 12 (power equals the number); Escape x2 (power 0); Mermaid x1 (power 20); Pirate A (power 30); Pirate B (power 31); Skull King x1 (power 40).

SETUP: Every player starts at 0 points. The game lasts exactly 8 rounds.

EACH ROUND:
1. DEAL (the round's only random event): Shuffle all 18 cards and deal 3 to each player, privately. The remaining cards stay face down and unseen for the whole round.
2. BID: All players at the same time secretly choose a bid of 0, 1, 2 or 3 (how many tricks they will win this round).
3. REVEAL BIDS: All bids are announced to everyone.
4. TRICK 1: All players at the same time choose one card from their hand to play. All played cards are revealed together and removed from hands.
5. RESOLVE TRICK 1: If the Mermaid and the Skull King were both played, the Mermaid's player wins the trick. Otherwise the card with the highest power wins the trick. If every card played has power 0 (all Escapes), nobody wins the trick. Add 1 to the winner's tricks-won count. Capture bonuses are recorded for the winner: if the Skull King won, count the Pirates in the trick (each is worth a +20 bonus); if the Mermaid won and the Skull King is in the trick, record a +40 bonus. Announce the winner.
6. TRICK 2 and RESOLVE TRICK 2: same as steps 4 and 5.
7. TRICK 3 and RESOLVE TRICK 3: same as steps 4 and 5 (each player plays their last card).
8. SCORING, for each player:
   - Bid 0 and won 0 tricks: +30.
   - Bid 0 and won 1 or more tricks: -30.
   - Bid k of 1 or more and won exactly k tricks: +20 times k, plus all capture bonuses that player recorded this round.
   - Bid k of 1 or more and won a different number: -10 times the absolute difference between bid and tricks won. No bonuses.
   - Capture bonuses are paid only on an exact bid (zero bids cannot have bonuses, since bonuses require winning a trick).
9. ANNOUNCE: Each player's tricks won, points this round and running total are announced. Reset tricks won and bonuses to 0.
10. END CHECK: After round 8 the game ends.

INFORMATION: Your own hand is private. Bids, every played card, trick winners and scores are public. There is no talk phase.

How the winner is decided: After 8 rounds, the player with the highest total points wins. If two or more players tie for the highest total, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Skull King: Three-Card Raids (3 to 5 players, best with 4)

Eight rounds of three simultaneous tricks: secretly bid how many tricks you will win, then play cards from a private 3-card hand. Exact bids score and pay capture bonuses.

STATE (every item below must exist in the file):
  - each player: score (number, starts 0); everyone sees it. running total of points
  - each player: hand (list, starts []); only its owner sees it. the player's private cards, each written as its power value (Escape 0, numbers 1-12, Mermaid 20, Pirate A 30, Pirate B 31, Skull King 40)
  - each player: bid (number, starts 0); everyone sees it. tricks the player bid this round, 0-3; it stays secret until all bids are revealed together
  - each player: tricks_won (number, starts 0); everyone sees it. tricks won so far this round
  - each player: bonus (number, starts 0); everyone sees it. capture bonus points recorded this round
  - each player: played (number, starts -1); everyone sees it. power of the card played in the current trick; it is revealed when all cards are in
  - each player: round_points (number, starts 0); everyone sees it. points scored this round
  - the table: deck (list, starts [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0, 0, 20, 30, 31, 40]); hidden from all players. the 18 cards as power values; the undealt cards stay face down and unseen
  - the table: round (number, starts 0); everyone sees it. current round number, 1-8
  - the table: trick_number (number, starts 0); everyone sees it. current trick within the round, 1-3
  - the table: trick_winner (number, starts 0); everyone sees it. seat that won the last trick, or 0 if nobody won
  - parameters, each kept as a table attribute: deck_size = 18, hand_size = 3, tricks_per_round = 3, rounds = 8, bid_min = 0, bid_max = 3, number_card_min = 1, number_card_max = 12, escape_count = 2, escape_power = 0, mermaid_count = 1, mermaid_power = 20, pirate_a_power = 30, pirate_b_power = 31, skull_king_count = 1, skull_king_power = 40, zero_bid_success_points = 30, zero_bid_fail_points = -30, exact_bid_points_per_trick = 20, missed_bid_points_per_trick_off = -10, pirate_capture_bonus = 20, skull_king_capture_bonus = 40, starting_score = 0, tricks_won_per_trick = 1

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Every player's score is set to 0.
  2. round is set to 0.
  3. The game will last exactly 8 rounds.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round += 1; trick_number = 0; deck = [1,2,3,4,5,6,7,8,9,10,11,12,0,0,20,30,31,40]; every hand = []; every tricks_won = 0; every bonus = 0; every round_points = 0
  2. [update] all players. What happens: Deal: 3 times for each player, pick a random card from deck, append it to that player's hand and remove it from deck. This is the round's only random event.
  3. [sync] all players. What happens: each player privately sees their own hand
  4. [poll] all players answers: a whole number from 0 to 3. What happens: bid = answer; no bid is shown until all are in
  5. [tell] all players. What happens: announce every player's bid
  6. [update] all players. What happens: trick_number += 1; every played = -1; trick_winner = 0
  7. [poll] all players answers: one card from own hand (a power value in hand). What happens: played = answer; remove one copy of answer from hand; nobody sees a card until all are in
  8. [tell] all players. What happens: reveal every player's played card
  9. [update] all players. What happens: if some player played 20 and some player played 40: trick_winner = seat with played == 20; else if max(played) > 0: trick_winner = seat with played == max(played) (unique, since only the Escapes share a power); else trick_winner = 0. If trick_winner != 0: that player's tricks_won += 1. If the winner played 40: winner's bonus += 20 * (count of players with played == 30 or played == 31). If the winner played 20 and some player played 40: winner's bonus += 40.
  10. [tell] all players. What happens: announce trick_winner (or that nobody won) and any bonus recorded
  11. [repeat] all players. What happens: run the trick steps again (from 'trick_number += 1' through the trick announcement) until trick_number == 3
  12. [update] all players. What happens: for each player: if bid == 0 and tricks_won == 0: round_points = 30; if bid == 0 and tricks_won >= 1: round_points = -30; if bid >= 1 and tricks_won == bid: round_points = 20 * bid + bonus; if bid >= 1 and tricks_won != bid: round_points = -10 * abs(bid - tricks_won). Then score += round_points.
  13. [tell] all players. What happens: announce each player's tricks_won, round_points and score
  14. [update] all players. What happens: every tricks_won = 0; every bonus = 0
  15. [check] all players. What happens: end the game if round == 8, otherwise continue

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, then every player's score is 0.
  R2. When a round starts, then the full 18-card deck (numbers 1-12, two Escapes of power 0, Mermaid 20, Pirate A 30, Pirate B 31, Skull King 40) is shuffled and each player receives exactly 3 cards in their private hand.
  R3. When cards are dealt, then the undealt cards stay in deck and are never revealed that round.
  R4. When players bid, then each chooses simultaneously a whole number from 0 to 3, and all bids are revealed only after all are in.
  R5. When a trick is played, then each player simultaneously plays one card from their own hand, and that card is removed from the hand and revealed to all.
  R6. When both the Mermaid (20) and the Skull King (40) are played in a trick, then the Mermaid's player wins the trick.
  R7. When the Mermaid and the Skull King are not both in a trick and some card has power above 0, then the player of the highest-power card wins the trick.
  R8. When every card played in a trick has power 0, then nobody wins the trick and no tricks_won changes.
  R9. When a player wins a trick, then their tricks_won increases by 1.
  R10. When the Skull King wins a trick, then its player records a bonus of +20 for each Pirate (30 or 31) in that trick.
  R11. When the Mermaid wins a trick containing the Skull King, then its player records a +40 bonus.
  R12. When a player bid 0 and won 0 tricks, then they score +30 for the round.
  R13. When a player bid 0 and won 1 or more tricks, then they score -30 for the round.
  R14. When a player bid k >= 1 and won exactly k tricks, then they score 20*k plus all bonuses recorded that round.
  R15. When a player bid k >= 1 and won a different number of tricks t, then they score -10*|k - t| and no bonuses.
  R16. When a round's scoring ends, then each player's tricks_won, round points and score are announced, and tricks_won and bonus reset to 0.
  R17. When round 8 has been scored, then the game ends and the highest score wins; players tied for the highest score share the result (a draw).
  R18. When any phase of the game runs, then there is no talk phase.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Bid | asked: all players, simultaneously | options: any whole number 0, 1, 2 or 3
  - Trick 1 card | asked: all players, simultaneously | options: any of the 3 cards in the player's own hand
  - Trick 2 card | asked: all players, simultaneously | options: any of the 2 cards remaining in the player's own hand
  - Trick 3 card | asked: all players, simultaneously | options: the 1 card remaining in the player's own hand

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round == 8 after the round's scoring
  - each player's standing: you.score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their total score after 8 rounds. The highest total wins; players tied for the highest total share the result, which is the source's draw.
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

- each player: `score` (number, visible: public, starts 0): running total of points
- each player: `bid` (number, visible: public, starts 0): tricks the player bid this round, 0-3; it stays secret until all bids are revealed together
- each player: `tricks_won` (number, visible: public, starts 0): tricks won so far this round
- each player: `played` (number, visible: public, starts -1): power of the card played in the current trick; it is revealed when all cards are in
- each player: `round_points` (number, visible: public, starts 0): points scored this round
- the table: `round` (number, visible: public, starts 0): current round number, 1-8
- the table: `trick_winner` (number, visible: public, starts 0): seat that won the last trick, or 0 if nobody won
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 18, hand_size = 3, tricks_per_round = 3, rounds = 8, bid_min = 0, bid_max = 3, number_card_min = 1, number_card_max = 12, escape_count = 2, escape_power = 0, mermaid_count = 1, mermaid_power = 20, pirate_a_power = 30, pirate_b_power = 31, skull_king_count = 1, skull_king_power = 40, zero_bid_success_points = 30, zero_bid_fail_points = -30, exact_bid_points_per_trick = 20, missed_bid_points_per_trick_off = -10, pirate_capture_bonus = 20, skull_king_capture_bonus = 40, starting_score = 0, tricks_won_per_trick = 1
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

Add the BID step to each round, after the deal and before trick 1. It must be a simultaneous poll of all players. Offer the whole numbers from `bid_min` to `bid_max` (0, 1, 2, 3), building the options from those parameter attributes rather than literal numbers. Store each choice in that player's `bid`, keep it hidden until all bids are in, then reveal it publicly. Do not reset `bid` in the end-of-round announce/reset step: the rules reset only tricks won and bonuses, and the new bid overwrites it next round. Make sure scoring reads this real `bid` value. Bid 0 gives ±30. Bid k≥1 gives +20k plus bonuses on an exact hit, or -10 × |bid − tricks won| otherwise. Keep the card-play polls offering only the cards in the player's own hand.
