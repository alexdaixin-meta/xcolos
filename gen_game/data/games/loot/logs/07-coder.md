# 07 coder

- time: 2026-10-28T05:08:06+00:00 (43.6s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 281c4a11586f909b, reply sha256 ebc07bcb74abea32

## Sent

````
# Task: write the XColos game file for "Loot: Sealed Raids"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 5; set `meta.players` to {"min": 3, "max": 5, "suggested": 4} (the suggested size is the one the game plays best at).

SETUP: Each player starts with 30 crew (private: only that player and the engine know their remaining crew), 0 gold, three unsailed merchant ships worth 3, 5 and 7 gold, one unused Captain and one unused Admiral. Players are seated 1 to N. The game lasts 3 x N rounds (12 with 4 players).

EACH ROUND:
1. Owner. The owner is player ((round - 1) mod N) + 1. Each player is owner exactly 3 times. The engine announces who the owner is and which of the owner's ships are still unsailed.
2. Sail. The owner privately chooses one of their unsailed ships to sail. If only one remains, it is sailed automatically. Its value is not yet revealed.
3. Talk. Every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Talk binds no one.
4. Commit. At the same moment, every player secretly chooses a whole number of crew to commit, from 0 up to their remaining crew. In the same poll, the owner may declare their Admiral if it is unused, and each non-owner may declare their Captain if it is unused. Invalid amounts are set to 0. Invalid trump declarations are ignored.
5. Spend. Every player's committed crew is subtracted from their remaining crew, whatever the result.
6. Strength. The owner's defense equals the crew they committed. Each attacker's strength equals the crew they committed, plus 6 if they declared their Captain this round.
7. Resolve. The rules are applied in this order:
   (a) If the owner declared the Admiral, the owner keeps the ship.
   (b) Otherwise, find the highest attacker strength. The ship goes to that attacker only if their strength is strictly greater than the owner's defense and strictly greater than every other attacker's strength.
   (c) In every other case, including ties between the top attackers or an attack that does not beat the defense, the owner keeps the ship.
8. Score. Whoever gets the ship adds its value to their gold.
9. Bookkeeping. The ship is marked sailed. Declared trumps are marked used.
10. Announce. The engine reveals the ship's value, who got it, and who used a Captain or Admiral this round. It does not reveal any crew amounts.
11. Advance. Move to the next round, or end the game after round 3 x N.

END: Unspent crew is worth nothing.

How the winner is decided: After the final round, the player with the most gold wins. If two or more players tie for the most gold, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Loot: Sealed Raids (3 to 5 players, best with 4)

Each round one seat sails a hidden-value merchant ship and every seat secretly commits crew from a fixed budget of 30 to defend it or raid it, with one-shot Captain and Admiral trumps. The most gold after 3 x N rounds wins.

STATE (every item below must exist in the file):
  - each player: crew (number, starts 30); only its owner sees it. Remaining crew. Only the owner of the attribute and the engine know it.
  - each player: gold (number, starts 0); everyone sees it. Gold won from ships. This is the score.
  - each player: ships (list, starts [3, 5, 7]); everyone sees it. Values of this player's unsailed ships. A value is removed only at bookkeeping, after it has been revealed.
  - each player: captain_used (bool, starts False); everyone sees it. Whether this player's Captain has been used.
  - each player: admiral_used (bool, starts False); everyone sees it. Whether this player's Admiral has been used.
  - each player: committed (number, starts 0); only its owner sees it. Crew this player committed this round.
  - each player: trump_declared (bool, starts False); only its owner sees it. Whether this player validly declared a trump this round (an Admiral for the owner, a Captain for a non-owner).
  - each player: strength (number, starts 0); only its owner sees it. This round's strength: committed crew, plus 6 for an attacker who declared the Captain. For the owner it is the defense.
  - the table: round (number, starts 0); everyone sees it. Current round number.
  - the table: owner (number, starts 0); everyone sees it. Seat of this round's owner: ((round - 1) mod N) + 1.
  - the table: current_ship (number, starts 0); hidden from all players. Value of the ship sailed this round. It stays hidden until the announcement.
  - the table: last_ship_value (number, starts 0); everyone sees it. Value of the ship revealed at the end of the round.
  - the table: last_taker (number, starts 0); everyone sees it. Seat that got this round's ship.
  - the table: defense (number, starts 0); hidden from all players. Scratch value: the owner's defense this round.
  - the table: top_attack (number, starts 0); hidden from all players. Scratch value: the highest attacker strength this round.
  - the table: top_count (number, starts 0); hidden from all players. Scratch value: how many attackers have the highest strength.
  - parameters, each kept as a table attribute: min_players = 3, max_players = 5, suggested_players = 4, starting_crew = 30, starting_gold = 0, ship_value_small = 3, ship_value_medium = 5, ship_value_large = 7, ships_per_player = 3, captains_per_player = 1, admirals_per_player = 1, captain_bonus = 6, rounds_per_player = 3, min_commit = 0, unspent_crew_value = 0

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seat the players 1 to N.
  2. Every player gets 30 crew (private), 0 gold, unsailed ships worth 3, 5 and 7 gold, an unused Captain and an unused Admiral.
  3. Set round to 0. The game lasts 3 x N rounds.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round += 1; owner = ((round - 1) mod N) + 1; for every player, set committed = 0, trump_declared = false and strength = 0.
  2. [tell] all players. What happens: Announce: 'Round {round}: Seat {owner} is the owner. Unsailed ships: {owner.ships}.'
  3. [update] seat owner. What happens: When the length of owner.ships = 1, set current_ship = the only value in owner.ships (it sails automatically).
  4. [ask] seat owner answers: one value from owner.ships. What happens: When the length of owner.ships > 1, set current_ship = the chosen value. The choice is private.
  5. [poll] all players answers: short text. What happens: Every message is shown to everyone after all are in: broadcast {"to": "all", "text": "Seat {seat} says: {value}"}. Talk binds no one.
  6. [poll] all players answers: A whole number of crew from 0 to your crew. Also a trump choice: the owner chooses 'none' or 'admiral', with 'admiral' offered only if admiral_used is false; a non-owner chooses 'none' or 'captain', with 'captain' offered only if captain_used is false.. What happens: committed = the amount, or 0 if the amount is invalid. trump_declared = true only for a valid declaration; an invalid declaration is ignored.
  7. [update] all players. What happens: crew -= committed. strength = committed + (6 if the seat is not the owner and trump_declared, else 0). defense = owner.strength.
  8. [update] all players. What happens: top_attack = the highest strength among non-owners; top_count = the number of non-owners whose strength = top_attack. If owner.trump_declared, last_taker = owner. Otherwise, if top_attack > defense and top_count = 1, last_taker = the non-owner whose strength = top_attack. Otherwise last_taker = owner.
  9. [update] all players. What happens: The player in seat last_taker adds current_ship to gold. last_ship_value = current_ship.
  10. [update] all players. What happens: Remove current_ship from owner.ships. If owner.trump_declared, set owner.admiral_used = true. For each non-owner with trump_declared, set captain_used = true.
  11. [tell] all players. What happens: Announce: 'The ship was worth {last_ship_value}. Seat {last_taker} got it.' Then list who used a Captain or Admiral this round. No crew amounts are revealed.
  12. [check] all players. What happens: End the game if round >= 3 * N; otherwise continue.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, then each player has 30 crew, 0 gold, ships [3, 5, 7], an unused Captain and an unused Admiral.
  R2. When it is round r, then the owner is seat ((r - 1) mod N) + 1, so with 4 players round 5 is owned by seat 1.
  R3. When the game has N players, then it lasts 3 x N rounds (12 with 4 players) and each seat is owner exactly 3 times.
  R4. When a round begins, then the owner and the owner's unsailed ships are announced.
  R5. When the owner has more than one unsailed ship, then the owner privately chooses which one sails.
  R6. When the owner has exactly one unsailed ship, then it sails automatically.
  R7. When a ship sails, then its value is not revealed until the end-of-round announcement.
  R8. When the talk step runs, then every player writes one message at the same time and all messages are shown to everyone only after all are in.
  R9. When crew is committed, then every player chooses at the same time a whole number from 0 to their remaining crew.
  R10. When a committed amount is invalid, then it is set to 0.
  R11. When a player commits crew, then it is subtracted from their crew whatever the result, so 30 crew minus a commit of 10 leaves 20.
  R12. When a non-owner declares an unused Captain, then their strength is their committed crew + 6.
  R13. When the owner declares an unused Admiral, then the owner keeps the ship regardless of any attack.
  R14. When a trump declaration is invalid (already used, or the wrong role), then it is ignored.
  R15. When no Admiral is declared and one attacker's strength is strictly greater than the defense and strictly greater than every other attacker's, then that attacker gets the ship (attack 8 against defense 7 wins).
  R16. When the highest attacker strength equals the defense, then the owner keeps the ship (attack 7 against defense 7 loses).
  R17. When two or more attackers tie for the highest strength, then the owner keeps the ship, even if that strength beats the defense.
  R18. When a player gets a ship, then they add its value to their gold.
  R19. When the round ends, then the sailed ship is removed from the owner's unsailed ships and declared trumps are marked used.
  R20. When the round ends, then the ship's value, its taker and who used a Captain or Admiral are announced, but no crew amounts are.
  R21. When the game ends, then unspent crew is worth 0 and the player with the most gold wins; players tied for the most gold share the result, standing for the source's draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Sail: which ship to sail | asked: the owner, only when they have 2 or more unsailed ships | options: each value in owner.ships
  - Talk message | asked: all seats | options: a short free-text message
  - Commit: crew amount | asked: all seats | options: a whole number from 0 to that seat's crew
  - Commit: trump | asked: all seats | options: The owner with an unused Admiral: none, admiral. The owner with a used Admiral: none. A non-owner with an unused Captain: none, captain. A non-owner with a used Captain: none.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round >= 3 * N
  - each player's standing: you.gold (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their gold. The player with the most gold wins. Players tied for the most gold share the result, which stands for the source's draw.
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

- each player: `gold` (number, visible: public, starts 0): Gold won from ships. This is the score.
- each player: `ships` (list, visible: public, starts [3, 5, 7]): Values of this player's unsailed ships. A value is removed only at bookkeeping, after it has been revealed.
- each player: `captain_used` (bool, visible: public, starts False): Whether this player's Captain has been used.
- each player: `admiral_used` (bool, visible: public, starts False): Whether this player's Admiral has been used.
- the table: `round` (number, visible: public, starts 0): Current round number.
- the table: `owner` (number, visible: public, starts 0): Seat of this round's owner: ((round - 1) mod N) + 1.
- the table: `last_ship_value` (number, visible: public, starts 0): Value of the ship revealed at the end of the round.
- the table: `last_taker` (number, visible: public, starts 0): Seat that got this round's ship.
- parameters (each must be an attribute holding this value, never a number buried in a step): min_players = 3, max_players = 5, suggested_players = 4, starting_crew = 30, starting_gold = 0, ship_value_small = 3, ship_value_medium = 5, ship_value_large = 7, ships_per_player = 3, captains_per_player = 1, admirals_per_player = 1, captain_bonus = 6, rounds_per_player = 3, min_commit = 0, unspent_crew_value = 0
- the game ends with ONE ending whose `rank_by` is `you.gold`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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


YOUR PREVIOUS GAME FILE WAS REFUSED. Here it is:
```json
{
  "schema": 1,
  "meta": {
    "id": "loot_sealed_raids",
    "name": "Loot: Sealed Raids",
    "players": {
      "min": 3,
      "max": 5,
      "suggested": 4
    },
    "blurb": "Each round one seat sails a hidden-value ship and everyone secretly commits crew to defend or raid it, with one-shot Captain and Admiral trumps."
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
        "key": "crew",
        "visible": "ally",
        "type": "number",
        "initial": 30
      },
      {
        "key": "gold",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "ships",
        "visible": "public",
        "type": "list",
        "initial": [3, 5, 7]
      },
      {
        "key": "captain_used",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "admiral_used",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "committed",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "trump_declared",
        "visible": "ally",
        "type": "bool",
        "initial": false
      },
      {
        "key": "strength",
        "visible": "ally",
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
        "key": "trump_choice",
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
        "key": "owner",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "current_ship",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "last_ship_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "last_taker",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "defense",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "top_attack",
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
        "key": "min_players",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "max_players",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "suggested_players",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "starting_crew",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "starting_gold",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "ship_value_small",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "ship_value_medium",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "ship_value_large",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "ships_per_player",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "captains_per_player",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "admirals_per_player",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "captain_bonus",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "rounds_per_player",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "min_commit",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "unspent_crew_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "outfit the fleets",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "crew",
            "value": {
              "calc": "starting_crew"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "gold",
            "value": {
              "calc": "starting_gold"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "ships",
            "value": {
              "calc": "[ship_value_small, ship_value_medium, ship_value_large]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "captain_used",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "admiral_used",
            "value": false
          }
        },
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
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "owner",
      "label": "the next round",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "key": "owner",
            "value": {
              "calc": "((round - 1) % len(players)) + 1"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "committed",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "trump_declared",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "strength",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "trump_choice",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "['none'] + (['admiral'] if you.seat == owner and not you.admiral_used else []) + (['captain'] if you.seat != owner and not you.captain_used else [])"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "owner",
      "label": "the owner",
      "to": "all",
      "text": "Round {round}: Seat {owner} is the owner. Unsailed ships: {[p.ships for p in players if p.seat == owner][0]}."
    },
    {
      "use": "update",
      "phase": "sail",
      "label": "the last ship sails",
      "when": {
        "calc": "max([len(p.ships) for p in players if p.seat == owner]) == 1"
      },
      "do": [
        {
          "set": {
            "key": "current_ship",
            "value": {
              "calc": "max([p.ships[0] for p in players if p.seat == owner])"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "sail",
      "label": "sail",
      "to": {
        "where": "you.seat == owner and len(you.ships) > 1"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "ships"
        }
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "current_ship",
              "value": {
                "calc": "int($answer)"
              }
            }
          }
        ]
      },
      "text": "You are the owner. Choose which of your unsailed ships sails this round. Its value stays secret until the end of the round."
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
      "text": "Say one short thing to the table. Everyone writes at the same time; talk binds no one."
    },
    {
      "use": "poll",
      "phase": "commit",
      "label": "commit crew",
      "to": "acting",
      "answer": {
        "type": "number",
        "min": {
          "calc": "min_commit"
        },
        "max": {
          "calc": "you.crew"
        }
      },
      "store": "committed",
      "text": "Round {round}, owner Seat {owner}. Secretly commit a whole number of crew, from {min_commit} up to your remaining crew. The owner's crew defends the ship; everyone else's crew raids it. Committed crew is spent whatever happens."
    },
    {
      "use": "poll",
      "phase": "commit",
      "label": "commit trump",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "store": "trump_choice",
      "text": "At the same moment, declare a trump or none. The owner may declare their unused Admiral (the owner keeps the ship whatever the attack). A non-owner may declare their unused Captain (+{captain_bonus} strength). A trump declared is used up."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "spend and strength",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "trump_declared",
            "value": {
              "calc": "you.trump_choice != 'none' and you.trump_choice != '' and you.trump_choice in you.offer"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "crew",
            "value": {
              "calc": "-you.committed"
            },
            "if": {
              "calc": "you.committed <= you.crew"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "strength",
            "value": {
              "calc": "you.committed + (captain_bonus if you.seat != owner and you.trump_declared else 0)"
            }
          }
        },
        {
          "set": {
            "key": "defense",
            "value": {
              "calc": "max([p.strength for p in players if p.seat == owner])"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "resolve the raid",
      "do": [
        {
          "set": {
            "key": "top_attack",
            "value": {
              "calc": "max([p.strength for p in players if p.seat != owner])"
            }
          }
        },
        {
          "set": {
            "key": "top_count",
            "value": {
              "calc": "count(p.seat != owner and p.strength == top_attack for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "last_taker",
            "value": {
              "calc": "owner if any(p.trump_declared for p in players if p.seat == owner) else (max([p.seat for p in players if p.seat != owner and p.strength == top_attack]) if top_attack > defense and top_count == 1 else owner)"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "score",
      "do": [
        {
          "adjust": {
            "player": {
              "calc": "last_taker"
            },
            "key": "gold",
            "value": {
              "calc": "current_ship"
            }
          }
        },
        {
          "set": {
            "key": "last_ship_value",
            "value": {
              "calc": "current_ship"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "bookkeeping",
      "do": [
        {
          "remove": {
            "player": {
              "calc": "owner"
            },
            "key": "ships",
            "value": {
              "calc": "current_ship"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == owner and you.trump_declared"
            },
            "key": "admiral_used",
            "value": true
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat != owner and you.trump_declared"
            },
            "key": "captain_used",
            "value": true
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "resolve",
      "label": "the reveal",
      "to": "all",
      "text": "The ship was worth {last_ship_value}. Seat {last_taker} got it. Admiral used this round by seats: {[p.seat for p in players if p.trump_declared and p.seat == owner]}. Captains used this round by seats: {[p.seat for p in players if p.trump_declared and p.seat != owner]}."
    },
    {
      "use": "check",
      "phase": "resolve",
      "label": "after the last round",
      "when": {
        "calc": "round >= rounds_per_player * len(players)"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round >= rounds_per_player * len(players)"
      },
      "rank_by": "you.gold",
      "text": "Winner: {result}. Final gold [seat, gold]: {[[p.seat, p.gold] for p in players]}."
    }
  },
  "limits": {
    "rounds": 15,
    "rounds_max": 15,
    "actions_max": 1000,
    "deadline_s": 120
  },
  "rules": "Each player starts with {starting_crew} crew (private: only you know your remaining crew), {starting_gold} gold, {ships_per_player} unsailed merchant ships worth {ship_value_small}, {ship_value_medium} and {ship_value_large} gold, {captains_per_player} unused Captain and {admirals_per_player} unused Admiral. Players are seated 1 to N. The game lasts {rounds_per_player} x N rounds (12 with 4 players).\n\nEach round:\n1. Owner. The owner is player ((round - 1) mod N) + 1, so each player is owner exactly {rounds_per_player} times. The owner and the owner's unsailed ships are announced.\n2. Sail. The owner privately chooses one of their unsailed ships to sail. If only one remains, it is sailed automatically. Its value is not revealed until the end of the round.\n3. Talk. Every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Talk binds no one.\n4. Commit. At the same moment, every player secretly chooses a whole number of crew to commit, from {min_commit} up to their remaining crew. At the same moment, the owner may declare their Admiral if it is unused, and each non-owner may declare their Captain if it is unused; you are only offered a trump you may legally declare. Invalid amounts are set to 0; invalid trump declarations are ignored.\n5. Spend. Every player's committed crew is subtracted from their remaining crew, whatever the result (30 crew minus a commit of 10 leaves 20).\n6. Strength. The owner's defense equals the crew they committed. Each attacker's strength equals the crew they committed, plus {captain_bonus} if they declared their Captain this round.\n7. Resolve, in this order: (a) If the owner declared the Admiral, the owner keeps the ship, whatever the attack. (b) Otherwise, find the highest attacker strength. The ship goes to that attacker only if their strength is strictly greater than the owner's defense and strictly greater than every other attacker's strength (attack 8 against defense 7 wins). (c) In every other case, including ties between the top attackers (even if they beat the defense) or an attack that does not beat the defense (attack 7 against defense 7 loses), the owner keeps the ship.\n8. Score. Whoever gets the ship adds its value to their gold.\n9. Bookkeeping. The ship is removed from the owner's unsailed ships. Declared trumps are marked used and cannot be declared again; an undeclared trump stays unused.\n10. Announce. The ship's value, who got it, and who used a Captain or Admiral this round are revealed. No crew amounts are revealed.\n\nEnd: after round {rounds_per_player} x N the game ends. Unspent crew is worth {unspent_crew_value}. The player with the most gold wins; players tied for the most gold share the result (a draw)."
}
```

Why it was refused: playing it with random seats failed: seed 1, 3 players: the match crashed: FlowError: 'you.committed <= you.crew' reads `you` where there is no player
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "loot_sealed_raids",
    "name": "Loot: Sealed Raids",
    "players": {
      "min": 3,
      "max": 5,
      "suggested": 4
    },
    "blurb": "Each round one seat sails a hidden-value ship and everyone secretly commits crew to defend or raid it, with one-shot Captain and Admiral trumps."
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
        "key": "crew",
        "visible": "ally",
        "type": "number",
        "initial": 30
      },
      {
        "key": "gold",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "ships",
        "visible": "public",
        "type": "list",
        "initial": [3, 5, 7]
      },
      {
        "key": "captain_used",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "admiral_used",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "committed",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "trump_declared",
        "visible": "ally",
        "type": "bool",
        "initial": false
      },
      {
        "key": "strength",
        "visible": "ally",
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
        "key": "trump_choice",
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
        "key": "owner",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "current_ship",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "last_ship_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "last_taker",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "defense",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "top_attack",
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
        "key": "min_players",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "max_players",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "suggested_players",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "starting_crew",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "starting_gold",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "ship_value_small",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "ship_value_medium",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "ship_value_large",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "ships_per_player",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "captains_per_player",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "admirals_per_player",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "captain_bonus",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "rounds_per_player",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "min_commit",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "unspent_crew_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "outfit the fleets",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "crew",
            "value": {
              "calc": "starting_crew"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "gold",
            "value": {
              "calc": "starting_gold"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "ships",
            "value": {
              "calc": "[ship_value_small, ship_value_medium, ship_value_large]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "captain_used",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "admiral_used",
            "value": false
          }
        },
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
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "owner",
      "label": "the next round",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "key": "owner",
            "value": {
              "calc": "((round - 1) % len(players)) + 1"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "committed",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "trump_declared",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "strength",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "trump_choice",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "['none'] + (['admiral'] if you.seat == owner and not you.admiral_used else []) + (['captain'] if you.seat != owner and not you.captain_used else [])"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "owner",
      "label": "the owner",
      "to": "all",
      "text": "Round {round}: Seat {owner} is the owner. Unsailed ships: {[p.ships for p in players if p.seat == owner][0]}."
    },
    {
      "use": "update",
      "phase": "sail",
      "label": "the last ship sails",
      "when": {
        "calc": "max([len(p.ships) for p in players if p.seat == owner]) == 1"
      },
      "do": [
        {
          "set": {
            "key": "current_ship",
            "value": {
              "calc": "max([p.ships[0] for p in players if p.seat == owner])"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "sail",
      "label": "sail",
      "to": {
        "where": "you.seat == owner and len(you.ships) > 1"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "ships"
        }
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "current_ship",
              "value": {
                "calc": "int($answer)"
              }
            }
          }
        ]
      },
      "text": "You are the owner. Choose which of your unsailed ships sails this round. Its value stays secret until the end of the round."
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
      "text": "Say one short thing to the table. Everyone writes at the same time; talk binds no one."
    },
    {
      "use": "poll",
      "phase": "commit",
      "label": "commit crew",
      "to": "acting",
      "answer": {
        "type": "number",
        "min": {
          "calc": "min_commit"
        },
        "max": {
          "calc": "you.crew"
        }
      },
      "store": "committed",
      "text": "Round {round}, owner Seat {owner}. Secretly commit a whole number of crew, from {min_commit} up to your remaining crew. The owner's crew defends the ship; everyone else's crew raids it. Committed crew is spent whatever happens."
    },
    {
      "use": "poll",
      "phase": "commit",
      "label": "commit trump",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "store": "trump_choice",
      "text": "At the same moment, declare a trump or none. The owner may declare their unused Admiral (the owner keeps the ship whatever the attack). A non-owner may declare their unused Captain (+{captain_bonus} strength). A trump declared is used up."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "spend and strength",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "trump_declared",
            "value": {
              "calc": "you.trump_choice != 'none' and you.trump_choice != '' and you.trump_choice in you.offer"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "crew",
            "value": {
              "calc": "-min(you.committed, you.crew)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "strength",
            "value": {
              "calc": "you.committed + (captain_bonus if you.seat != owner and you.trump_declared else 0)"
            }
          }
        },
        {
          "set": {
            "key": "defense",
            "value": {
              "calc": "max([p.strength for p in players if p.seat == owner])"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "resolve the raid",
      "do": [
        {
          "set": {
            "key": "top_attack",
            "value": {
              "calc": "max([p.strength for p in players if p.seat != owner])"
            }
          }
        },
        {
          "set": {
            "key": "top_count",
            "value": {
              "calc": "count(p.seat != owner and p.strength == top_attack for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "last_taker",
            "value": {
              "calc": "owner if any(p.trump_declared for p in players if p.seat == owner) else (max([p.seat for p in players if p.seat != owner and p.strength == top_attack]) if top_attack > defense and top_count == 1 else owner)"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "score",
      "do": [
        {
          "adjust": {
            "player": {
              "calc": "last_taker"
            },
            "key": "gold",
            "value": {
              "calc": "current_ship"
            }
          }
        },
        {
          "set": {
            "key": "last_ship_value",
            "value": {
              "calc": "current_ship"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "bookkeeping",
      "do": [
        {
          "remove": {
            "player": {
              "calc": "owner"
            },
            "key": "ships",
            "value": {
              "calc": "current_ship"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == owner and you.trump_declared"
            },
            "key": "admiral_used",
            "value": true
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat != owner and you.trump_declared"
            },
            "key": "captain_used",
            "value": true
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "resolve",
      "label": "the reveal",
      "to": "all",
      "text": "The ship was worth {last_ship_value}. Seat {last_taker} got it. Admiral used this round by seats: {[p.seat for p in players if p.trump_declared and p.seat == owner]}. Captains used this round by seats: {[p.seat for p in players if p.trump_declared and p.seat != owner]}."
    },
    {
      "use": "check",
      "phase": "resolve",
      "label": "after the last round",
      "when": {
        "calc": "round >= rounds_per_player * len(players)"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round >= rounds_per_player * len(players)"
      },
      "rank_by": "you.gold",
      "text": "Winner: {result}. Final gold [seat, gold]: {[[p.seat, p.gold] for p in players]}."
    }
  },
  "limits": {
    "rounds": 15,
    "rounds_max": 15,
    "actions_max": 1000,
    "deadline_s": 120
  },
  "rules": "Each player starts with {starting_crew} crew (private: only you know your remaining crew), {starting_gold} gold, {ships_per_player} unsailed merchant ships worth {ship_value_small}, {ship_value_medium} and {ship_value_large} gold, {captains_per_player} unused Captain and {admirals_per_player} unused Admiral. Players are seated 1 to N. The game lasts {rounds_per_player} x N rounds (12 with 4 players).\n\nEach round:\n1. Owner. The owner is player ((round - 1) mod N) + 1, so each player is owner exactly {rounds_per_player} times. The owner and the owner's unsailed ships are announced.\n2. Sail. The owner privately chooses one of their unsailed ships to sail. If only one remains, it is sailed automatically. Its value is not revealed until the end of the round.\n3. Talk. Every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Talk binds no one.\n4. Commit. At the same moment, every player secretly chooses a whole number of crew to commit, from {min_commit} up to their remaining crew. At the same moment, the owner may declare their Admiral if it is unused, and each non-owner may declare their Captain if it is unused; you are only offered a trump you may legally declare. Invalid amounts are set to 0; invalid trump declarations are ignored.\n5. Spend. Every player's committed crew is subtracted from their remaining crew, whatever the result (30 crew minus a commit of 10 leaves 20).\n6. Strength. The owner's defense equals the crew they committed. Each attacker's strength equals the crew they committed, plus {captain_bonus} if they declared their Captain this round.\n7. Resolve, in this order: (a) If the owner declared the Admiral, the owner keeps the ship, whatever the attack. (b) Otherwise, find the highest attacker strength. The ship goes to that attacker only if their strength is strictly greater than the owner's defense and strictly greater than every other attacker's strength (attack 8 against defense 7 wins). (c) In every other case, including ties between the top attackers (even if they beat the defense) or an attack that does not beat the defense (attack 7 against defense 7 loses), the owner keeps the ship.\n8. Score. Whoever gets the ship adds its value to their gold.\n9. Bookkeeping. The ship is removed from the owner's unsailed ships. Declared trumps are marked used and cannot be declared again; an undeclared trump stays unused.\n10. Announce. The ship's value, who got it, and who used a Captain or Admiral this round are revealed. No crew amounts are revealed.\n\nEnd: after round {rounds_per_player} x N the game ends. Unspent crew is worth {unspent_crew_value}. The player with the most gold wins; players tied for the most gold share the result (a draw)."
}
```
````
