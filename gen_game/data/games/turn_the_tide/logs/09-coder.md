# 09 coder

- time: 2026-10-28T06:16:08+00:00 (94.8s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 3b4e959d12e702cc, reply sha256 e5cda045dff2a57f

## Sent

````
# Task: write the XColos game file for "Turn The Tide: Short Seas (revised)"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 4; set `meta.players` to {"min": 3, "max": 4, "suggested": 4} (the suggested size is the one the game plays best at).

SETUP. Let P be the number of players (3 or 4). The Weather deck is the cards 1 to 12xP (1-36 for 3 players, 1-48 for 4), each number once. Shuffle it and deal 11 cards face down to each player as that player's hand. The remaining P cards are set aside face down and stay unseen for the whole game. Each player starts with a game score of 0. The game has P deals of 10 hands each, so 10xP hands in total. One round is one hand.

INFORMATION. You always see your own hand. Every Weather card becomes public the moment it is played and stays face up in front of whoever played it until the end of that deal. Unplayed cards and set-aside cards are never shown. So from deal 2 on, every player knows the cards of a passed hand that were played in earlier deals but not its unplayed card or cards, unless they held that hand themselves.

START OF EACH DEAL (before hand 1 of deals 1 to P):
- Shuffle a Tide deck of the cards 1 to 20.
- Set every player's Tide level to 15.
- Give every player 4 lifelines.
- Clear every player's Sunk status.
- From deal 2 on: each player takes all 10 Weather cards lying face up in front of them, plus the 1 card still in their hand, making 11 cards. They pass these 11 cards as a hand to the player on their left. The face-up rows are now empty. Over the P deals each player plays each of the P original hands exactly once.

EACH HAND (10 per deal):
1. Reveal the next two cards of the Tide deck to everyone. The smaller is Low Tide and the larger is High Tide.
2. Every player secretly chooses one Weather card from their hand. All choices are revealed at the same time and each card is placed face up in front of the player who played it.
3. The player who played the highest Weather card sets their Tide level to Low Tide. The player who played the second highest sets their Tide level to High Tide. All others keep their current Tide level. Weather numbers are unique, so there are no ties. Sunk players take part in this step like anyone else.
4. Among players who are NOT Sunk, find the highest Tide level. Every non-Sunk player at that level loses 1 lifeline. A player who must lose a lifeline while at 0 lifelines becomes Sunk instead. A Sunk player stays Sunk until the next deal, keeps playing cards and is ignored in this step. If every player is Sunk, nothing happens.
5. Announce all Weather cards played, all Tide levels, all lifelines and all Sunk statuses.

END OF EACH DEAL (after hand 10 of each deal), adjust each game score:
- Each player who is not Sunk adds their remaining lifelines (0 to 4).
- Each Sunk player subtracts 1.
- Among players who are not Sunk, the player or players with the lowest Tide level each add 1.
After each deal every player holds exactly 1 card, which is not shown to others.

There is no talk phase.

END. After deal P, the game ends and the winner is decided as in the objective.

How the winner is decided: After the last deal, the player with the highest game score wins. If several players tie for the highest score, the tied player with the lowest Tide level at the end of the last deal wins. If that is still tied, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Turn The Tide: Short Seas (revised) (3 to 4 players, best with 4)

Over P deals of 10 hands, players play Weather cards at the same time to dodge high Tide levels and keep their lifelines. Each deal the hands pass to the left, and the highest total score wins.

STATE (every item below must exist in the file):
  - each player: score (number, starts 0); everyone sees it. Game score summed over the deals.
  - each player: hand (list, starts []); only its owner sees it. Weather cards held and not yet played.
  - each player: played (list, starts []); everyone sees it. Weather cards this player has played face up in the current deal.
  - each player: card_played (number, starts 0); everyone sees it. Weather card played in the current hand.
  - each player: tide (number, starts 15); everyone sees it. Current Tide level.
  - each player: lifelines (number, starts 4); everyone sees it. Lifelines left in this deal.
  - each player: sunk (bool, starts False); everyone sees it. Sunk status for this deal.
  - each player: pass_buffer (list, starts []); only its owner sees it. The 11 cards gathered for passing to the left at the start of a deal.
  - the table: weather_deck (list, starts 'cards 1 to 12*P'); hidden from all players. Shuffled Weather deck used for dealing.
  - the table: set_aside (list, starts []); hidden from all players. The P Weather cards set aside unseen for the whole game.
  - the table: tide_deck (list, starts 'cards 1 to 20'); hidden from all players. Tide deck, refilled at the start of each deal.
  - the table: low_tide (number, starts 0); everyone sees it. Smaller of the two Tide cards revealed this hand.
  - the table: high_tide (number, starts 0); everyone sees it. Larger of the two Tide cards revealed this hand.
  - the table: deal_no (number, starts 1); everyone sees it. Current deal, from 1 to P.
  - the table: hand_no (number, starts 1); everyone sees it. Current hand within the deal, from 1 to 10.
  - the table: max_tide (number, starts 0); hidden from all players. Scratch value: highest Tide level among non-Sunk players.
  - the table: min_tide (number, starts 0); hidden from all players. Scratch value: lowest Tide level among non-Sunk players at the end of a deal.
  - parameters, each kept as a table attribute: weather_cards_per_player = 12, hand_size = 11, hands_per_deal = 10, tide_deck_size = 20, tide_start_level = 15, lifelines_per_deal = 4, sunk_penalty = 1, lowest_tide_bonus = 1, deals_per_player = 1, set_aside_cards_per_player = 1, tie_break_weight = 100

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Let P be the number of players (3 or 4).
  2. weather_deck is set to the cards 1 to 12*P, each number once.
  3. Each player draws 11 cards at random from weather_deck into hand, and each card is removed from weather_deck.
  4. The remaining P cards move from weather_deck to set_aside, which is never shown.
  5. Every score is 0, deal_no is 1 and hand_no is 1.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: When hand_no == 1 and deal_no >= 2: each player's pass_buffer = played + hand; then each player's hand = pass_buffer of the player on their right (each player passes to the left); played = [] for everyone.
  2. [update] all players. What happens: When hand_no == 1: tide_deck = cards 1 to 20; every tide = 15; every lifelines = 4; every sunk = false.
  3. [sync] all players. What happens: When hand_no == 1, each player is sent their hand, along with deal_no and all public attributes.
  4. [update] all players. What happens: Draw 2 cards at random from tide_deck and remove them from it; low_tide = the smaller, high_tide = the larger.
  5. [tell] all players. What happens: Announce: 'Deal {deal_no}, hand {hand_no}: Low Tide {low_tide}, High Tide {high_tide}.'
  6. [poll] all players answers: one card from your hand. What happens: Each player's card_played = the chosen card; it is removed from hand and appended to played. All are revealed together.
  7. [update] all players. What happens: The player with the highest card_played sets tide = low_tide. The player with the second-highest card_played sets tide = high_tide. Sunk players are included. Everyone else keeps their tide.
  8. [update] all players. What happens: max_tide = the highest tide among players with sunk == false. For each player with sunk == false and tide == max_tide: if lifelines == 0 then sunk = true, else lifelines -= 1. If every player is Sunk, nothing changes.
  9. [tell] all players. What happens: Announce every card_played, tide, lifelines and sunk.
  10. [update] all players. What happens: When hand_no == 10: each player with sunk == false adds lifelines to score; each player with sunk == true subtracts 1 from score; min_tide = the lowest tide among players with sunk == false; each player with sunk == false and tide == min_tide adds 1 to score.
  11. [update] table. What happens: hand_no += 1; if hand_no > 10 then hand_no = 1 and deal_no += 1.
  12. [check] table. What happens: End the game when deal_no > P; otherwise continue.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. At setup, the Weather deck is the cards 1 to 12*P, each player is dealt 11 cards into hand, and the remaining P cards go to set_aside and are never shown.
  R2. At setup, every score is 0.
  R3. At the start of every deal, tide_deck is reset to 1 to 20, every tide is 15, every lifelines is 4 and every sunk is false.
  R4. At the start of deals 2 to P, each player's played cards plus their 1 remaining card (11 cards) pass to the player on their left as that player's hand, and played becomes empty.
  R5. Each hand, two Tide cards are drawn from tide_deck; the smaller is low_tide and the larger is high_tide.
  R6. Each hand, every player chooses one card from hand at the same time; it is removed from hand, appended to played and revealed.
  R7. The player who played the highest Weather card sets tide = low_tide, and the player who played the second highest sets tide = high_tide; this includes Sunk players.
  R8. Every non-Sunk player whose tide equals the highest tide among non-Sunk players loses 1 lifeline; a player at 0 lifelines who must lose one becomes Sunk instead.
  R9. A Sunk player stays Sunk until the next deal, still plays cards and is ignored when lifelines are lost; if all players are Sunk, no lifelines are lost.
  R10. After hand 10 of a deal, each non-Sunk player adds their lifelines (0 to 4) to score.
  R11. After hand 10 of a deal, each Sunk player subtracts 1 from score.
  R12. After hand 10 of a deal, each non-Sunk player whose tide is the lowest among non-Sunk players adds 1 to score.
  R13. A deal has 10 hands and the game ends after deal P.
  R14. The highest score wins; a tie is broken by the lowest final tide; players still level share the win.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Choose a Weather card to play this hand | asked: every seat | options: Exactly the cards currently in that seat's hand: 11 options on hand 1 of a deal, down to 2 on hand 10.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: deal_no > P (number of players)
  - each player's standing: you.score * 100 - you.tide (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: The highest game score wins. A tie is broken by the lowest Tide level at the end of the last deal. Players still level on both share the win, which stands in for the source's draw.
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

- each player: `score` (number, visible: public, starts 0): Game score summed over the deals.
- each player: `tide` (number, visible: public, starts 15): Current Tide level.
- each player: `lifelines` (number, visible: public, starts 4): Lifelines left in this deal.
- each player: `sunk` (bool, visible: public, starts False): Sunk status for this deal.
- the table: `deal_no` (number, visible: public, starts 1): Current deal, from 1 to P.
- parameters (each must be an attribute holding this value, never a number buried in a step): weather_cards_per_player = 12, hand_size = 11, hands_per_deal = 10, tide_deck_size = 20, tide_start_level = 15, lifelines_per_deal = 4, sunk_penalty = 1, lowest_tide_bonus = 1, deals_per_player = 1, set_aside_cards_per_player = 1, tie_break_weight = 100
- the game ends with ONE ending whose `rank_by` is `you.score * 100 - you.tide`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
    "id": "turn_the_tide_short_seas_revised",
    "name": "Turn The Tide: Short Seas (revised)",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 4
    },
    "blurb": "Play Weather cards at the same time to dodge high Tide levels, keep your lifelines, pass your hand left each deal, and finish with the highest score."
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
      },
      {
        "key": "hand",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "played",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "card_played",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tide",
        "visible": "public",
        "type": "number",
        "initial": 15
      },
      {
        "key": "lifelines",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "sunk",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "pass_buffer",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "chosen",
        "visible": "ally",
        "type": "text",
        "initial": ""
      }
    ],
    "game": [
      {
        "key": "weather_deck",
        "visible": "none",
        "type": "list",
        "initial": [
          1,
          2,
          3,
          4,
          5,
          6,
          7,
          8,
          9,
          10,
          11,
          12,
          13,
          14,
          15,
          16,
          17,
          18,
          19,
          20,
          21,
          22,
          23,
          24,
          25,
          26,
          27,
          28,
          29,
          30,
          31,
          32,
          33,
          34,
          35,
          36,
          37,
          38,
          39,
          40,
          41,
          42,
          43,
          44,
          45,
          46,
          47,
          48
        ]
      },
      {
        "key": "card_numbers",
        "visible": "none",
        "type": "list",
        "initial": [
          1,
          2,
          3,
          4,
          5,
          6,
          7,
          8,
          9,
          10,
          11,
          12,
          13,
          14,
          15,
          16,
          17,
          18,
          19,
          20
        ]
      },
      {
        "key": "deal_keys",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "set_aside",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "tide_deck",
        "visible": "none",
        "type": "list",
        "initial": [
          1,
          2,
          3,
          4,
          5,
          6,
          7,
          8,
          9,
          10,
          11,
          12,
          13,
          14,
          15,
          16,
          17,
          18,
          19,
          20
        ]
      },
      {
        "key": "t1",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "t2",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "low_tide",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "high_tide",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "deal_no",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "hand_no",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "max_tide",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "min_tide",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "weather_cards_per_player",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "hand_size",
        "visible": "public",
        "type": "number",
        "initial": 11
      },
      {
        "key": "hands_per_deal",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "tide_deck_size",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "tide_start_level",
        "visible": "public",
        "type": "number",
        "initial": 15
      },
      {
        "key": "lifelines_per_deal",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "sunk_penalty",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "lowest_tide_bonus",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "deals_per_player",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "set_aside_cards_per_player",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "tie_break_weight",
        "visible": "public",
        "type": "number",
        "initial": 100
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "build the weather deck",
      "do": [
        {
          "set": {
            "key": "weather_deck",
            "value": {
              "calc": "[c for c in weather_deck if c <= weather_cards_per_player * len(players)]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "shuffle and deal the hands",
      "do": [
        {
          "set": {
            "key": "deal_keys",
            "value": {
              "calc": "[[uniform(0, 1), c] for c in weather_deck]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "sorted([k[1] for k in deal_keys if count(j[0] < k[0] for j in deal_keys) >= (you.seat - 1) * hand_size and count(j[0] < k[0] for j in deal_keys) < you.seat * hand_size])"
            }
          }
        },
        {
          "set": {
            "key": "weather_deck",
            "value": {
              "calc": "[c for c in weather_deck if not any(c in p.hand for p in players)]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "set aside the remaining cards",
      "do": [
        {
          "set": {
            "key": "set_aside",
            "value": {
              "calc": "weather_deck"
            }
          }
        },
        {
          "set": {
            "key": "weather_deck",
            "value": []
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "starting scores",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": 0
          }
        },
        {
          "set": {
            "key": "deal_no",
            "value": 1
          }
        },
        {
          "set": {
            "key": "hand_no",
            "value": 1
          }
        }
      ]
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "deal",
      "label": "pass the hands left",
      "when": {
        "calc": "hand_no == 1 and deal_no >= 2"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "pass_buffer",
            "value": {
              "calc": "you.played + you.hand"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "sorted([p.pass_buffer for p in players if p.seat == (len(players) if you.seat == 1 else you.seat - 1)][0])"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "played",
            "value": []
          }
        }
      ],
      "text": "Deal {deal_no} begins: every player passes their 11 cards to the player on their left."
    },
    {
      "use": "update",
      "phase": "deal",
      "label": "reset the seas",
      "when": {
        "calc": "hand_no == 1"
      },
      "do": [
        {
          "set": {
            "key": "tide_deck",
            "value": {
              "calc": "[c for c in card_numbers if c <= tide_deck_size]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "tide",
            "value": {
              "calc": "tide_start_level"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "lifelines",
            "value": {
              "calc": "lifelines_per_deal"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "sunk",
            "value": false
          }
        }
      ],
      "text": "Deal {deal_no}: the Tide deck is reshuffled, every Tide level is {tide_start_level}, everyone has {lifelines_per_deal} lifelines and nobody is Sunk."
    },
    {
      "use": "sync",
      "phase": "deal",
      "label": "your hand",
      "when": {
        "calc": "hand_no == 1"
      },
      "mode": "self",
      "to": "all",
      "text": "Deal {deal_no}. Your state:"
    },
    {
      "use": "update",
      "phase": "hand",
      "label": "reveal the tide",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "chosen",
            "value": ""
          }
        },
        {
          "set": {
            "key": "t1",
            "value": {
              "calc": "tide_deck[int(uniform(0, len(tide_deck)))]"
            }
          }
        },
        {
          "remove": {
            "key": "tide_deck",
            "value": {
              "calc": "t1"
            }
          }
        },
        {
          "set": {
            "key": "t2",
            "value": {
              "calc": "tide_deck[int(uniform(0, len(tide_deck)))]"
            }
          }
        },
        {
          "remove": {
            "key": "tide_deck",
            "value": {
              "calc": "t2"
            }
          }
        },
        {
          "set": {
            "key": "low_tide",
            "value": {
              "calc": "min(t1, t2)"
            }
          }
        },
        {
          "set": {
            "key": "high_tide",
            "value": {
              "calc": "max(t1, t2)"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "hand",
      "label": "tide announced",
      "to": "all",
      "text": "Deal {deal_no}, hand {hand_no}: Low Tide {low_tide}, High Tide {high_tide}."
    },
    {
      "use": "poll",
      "phase": "hand",
      "label": "play a weather card",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "store": "chosen",
      "text": "Deal {deal_no}, hand {hand_no}: Low Tide {low_tide}, High Tide {high_tide}. Choose one Weather card from your hand {hand} to play face down. All cards are revealed together. The highest card takes Low Tide, the second highest takes High Tide."
    },
    {
      "use": "update",
      "phase": "hand",
      "label": "cards go face up",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "card_played",
            "value": {
              "calc": "int(you.chosen)"
            }
          }
        },
        {
          "remove": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "you.card_played"
            }
          }
        },
        {
          "append": {
            "players": "all",
            "key": "played",
            "value": {
              "calc": "you.card_played"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.card_played == max([p.card_played for p in players])"
            },
            "key": "tide",
            "value": {
              "calc": "low_tide"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.card_played == max([p.card_played for p in players if p.card_played < max([q.card_played for q in players])])"
            },
            "key": "tide",
            "value": {
              "calc": "high_tide"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "hand",
      "label": "the highest tide loses a lifeline",
      "do": [
        {
          "set": {
            "key": "max_tide",
            "value": {
              "calc": "max([p.tide for p in players if not p.sunk]) if any(not p.sunk for p in players) else 0"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "(not you.sunk) and you.tide == max_tide and you.lifelines == 0"
            },
            "key": "sunk",
            "value": true,
            "text": "Seat {player} is Sunk."
          }
        },
        {
          "adjust": {
            "players": {
              "where": "(not you.sunk) and you.tide == max_tide and you.lifelines > 0"
            },
            "key": "lifelines",
            "value": -1
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "hand",
      "label": "hand results",
      "to": "all",
      "text": "Hand {hand_no} of deal {deal_no} results [seat, card played, tide, lifelines, sunk]: {[[p.seat, p.card_played, p.tide, p.lifelines, p.sunk] for p in players]}."
    },
    {
      "use": "update",
      "phase": "scoring",
      "label": "end of deal scoring",
      "when": {
        "calc": "hand_no == hands_per_deal"
      },
      "do": [
        {
          "adjust": {
            "players": {
              "where": "not you.sunk"
            },
            "key": "score",
            "value": {
              "calc": "you.lifelines"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.sunk"
            },
            "key": "score",
            "value": {
              "calc": "-sunk_penalty"
            }
          }
        },
        {
          "set": {
            "key": "min_tide",
            "value": {
              "calc": "min([p.tide for p in players if not p.sunk]) if any(not p.sunk for p in players) else 0"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "(not you.sunk) and you.tide == min_tide"
            },
            "key": "score",
            "value": {
              "calc": "lowest_tide_bonus"
            }
          }
        }
      ],
      "text": "Deal {deal_no} is over. Scores [seat, score]: {[[p.seat, p.score] for p in players]}."
    },
    {
      "use": "update",
      "phase": "scoring",
      "label": "advance the hand",
      "do": [
        {
          "adjust": {
            "key": "hand_no",
            "value": 1
          }
        },
        {
          "adjust": {
            "key": "deal_no",
            "value": 1,
            "if": {
              "calc": "hand_no > hands_per_deal"
            }
          }
        },
        {
          "set": {
            "key": "hand_no",
            "value": 1,
            "if": {
              "calc": "hand_no > hands_per_deal"
            }
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "scoring",
      "label": "after the last deal",
      "when": {
        "calc": "deal_no > len(players) * deals_per_player"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "deal_no > len(players) * deals_per_player"
      },
      "rank_by": "you.score * 100 - you.tide",
      "text": "Winner: {result}. Final [seat, score, final tide]: {[[p.seat, p.score, p.tide] for p in players]}."
    }
  },
  "limits": {
    "rounds": 40,
    "rounds_max": 40,
    "actions_max": 3000,
    "deadline_s": 120
  },
  "rules": "SETUP. With P players, the Weather deck is the cards 1 to {weather_cards_per_player} x P, each number once. It is shuffled and each player is dealt {hand_size} cards face down as their hand. The remaining P cards ({set_aside_cards_per_player} per player) are set aside face down and are never shown. Everyone starts with a game score of 0. The game has P deals of {hands_per_deal} hands each.\n\nINFORMATION. You always see your own hand. Every Weather card becomes public the moment it is played and stays face up in front of whoever played it until the end of that deal. Unplayed cards and set-aside cards are never shown.\n\nSTART OF EACH DEAL: the Tide deck of cards 1 to {tide_deck_size} is shuffled; every Tide level is set to {tide_start_level}; every player gets {lifelines_per_deal} lifelines; every Sunk status is cleared. From deal 2 on, each player takes the 10 Weather cards face up in front of them plus the 1 card still in their hand (11 cards) and passes them as a hand to the player on their left; the face-up rows are emptied.\n\nEACH HAND:\n1. The next two Tide cards are revealed. The smaller is Low Tide, the larger is High Tide.\n2. Every player secretly chooses one Weather card from their hand. All are revealed at once and placed face up in front of whoever played them.\n3. The player who played the highest Weather card sets their Tide level to Low Tide. The player who played the second highest sets their Tide level to High Tide. Everyone else keeps their Tide level. Numbers are unique, so there are no ties. Sunk players take part in this step like anyone else.\n4. Among players who are NOT Sunk, find the highest Tide level. Every non-Sunk player at that level loses 1 lifeline; a player who must lose a lifeline while at 0 lifelines becomes Sunk instead. Players below that level lose nothing. A Sunk player stays Sunk until the next deal, keeps playing cards and is ignored in this step. If every player is Sunk, nothing happens.\n5. All cards played, Tide levels, lifelines and Sunk statuses are announced.\n\nEND OF EACH DEAL (after hand {hands_per_deal}): each player who is not Sunk adds their remaining lifelines (0 to {lifelines_per_deal}) to their score; each Sunk player subtracts {sunk_penalty}; among players who are not Sunk, the player or players with the lowest Tide level each add {lowest_tide_bonus}. After each deal every player holds exactly 1 unseen card.\n\nThere is no talk.\n\nEND. After deal P the game ends. The highest game score wins. If several players tie for the highest score, the tied player with the lowest Tide level at the end of the last deal wins. Players still tied on both share the win."
}
```
````
