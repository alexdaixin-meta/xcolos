# Task: write the XColos game file for "Ys: Brokers of the Blind Market"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

SETUP: There are three gem colors: Red, Blue and Green. Each color's price starts at 3. Before round 1, the three colors are dealt randomly, one to each player, as that player's SECRET FAVORED COLOR. Every player has a different color, and each player knows only their own. All players start with 0 gems of each color and 0 commerce points. The game lasts 6 rounds.

EACH ROUND:
1. Announce. The round number and the current prices of Red, Blue and Green are shown to all.
2. Talk. Everyone writes one short message at the same time without seeing the others. All messages are then shown. Talk is not binding.
3. Allocate (simultaneous, secret). Each player submits four whole numbers, each 0 or more, summing to exactly 6: their influence in the Red district, the Blue district, the Green district and the Commerce district.
4. Reveal. All allocations are shown to everyone.
5. Resolve each of the four districts separately:
   - If one player has the strictly highest influence (above 0), they win FIRST. Otherwise, all players tied at the highest value (above 0) each count as tied-first.
   - If there is a single first, the player with the strictly next-highest influence (above 0) wins SECOND. Second is not awarded if there is a tie for it, or if first was tied.
   - In a gem district, a single first gains 2 gems of that color, second gains 1 gem, and each tied-first gains 1 gem.
   - In Commerce, a single first gains 8 commerce points, second gains 3, and each tied-first gains 3.
   - A player with 0 influence in a district gains nothing there.
6. Market vote (simultaneous). Each player names one color: Red, Blue or Green.
7. Price update. Each color's price rises by 1 for every vote it received. Each color that received 0 votes falls by 1, but never below 1. The votes are then shown.
8. End check. After round 6 the game ends.

FINAL SCORING: Each player's score is the sum over the three colors of (gems of that color × that color's final price). Then add (gems of their secret favored color × that color's final price) again, so favored gems count double. Then add their commerce points. Secret colors are revealed at the end.

How the winner is decided: The player with the highest final score wins. If two or three players tie for the highest score, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Ys: Brokers of the Blind Market (3 to 3 players, best with 3)

Three brokers secretly favor one gem color each. Over 6 rounds they split 6 influence across Red, Blue, Green and Commerce districts to win gems or points, then vote on prices, with favored gems scoring double at the end.

STATE (every item below must exist in the file):
  - each player: favored_color (text, starts ''); only its owner sees it. This player's secret favored color (Red, Blue or Green), dealt from color_deck. Revealed at the end.
  - each player: red_gems (number, starts 0); everyone sees it. Red gems held.
  - each player: blue_gems (number, starts 0); everyone sees it. Blue gems held.
  - each player: green_gems (number, starts 0); everyone sees it. Green gems held.
  - each player: commerce_points (number, starts 0); everyone sees it. Commerce points earned.
  - each player: pending_allocation (text, starts ''); only its owner sees it. This round's secret allocation choice 'r/b/g/c', held until the reveal.
  - each player: alloc_red (number, starts 0); everyone sees it. Revealed influence in the Red district this round.
  - each player: alloc_blue (number, starts 0); everyone sees it. Revealed influence in the Blue district this round.
  - each player: alloc_green (number, starts 0); everyone sees it. Revealed influence in the Green district this round.
  - each player: alloc_commerce (number, starts 0); everyone sees it. Revealed influence in the Commerce district this round.
  - each player: vote (text, starts ''); everyone sees it. Color named in this round's market vote.
  - each player: revealed_color (text, starts ''); everyone sees it. favored_color copied here when secret colors are revealed at game end.
  - each player: score (number, starts 0); everyone sees it. Final score, computed after round 6.
  - the table: round (number, starts 0); everyone sees it. Current round number (1 to 6).
  - the table: price_red (number, starts 3); everyone sees it. Current Red price.
  - the table: price_blue (number, starts 3); everyone sees it. Current Blue price.
  - the table: price_green (number, starts 3); everyone sees it. Current Green price.
  - the table: color_deck (list, starts ['Red', 'Blue', 'Green']); hidden from all players. Undealt favored colors, used once at setup.
  - the table: votes_red (number, starts 0); everyone sees it. Votes Red received this round.
  - the table: votes_blue (number, starts 0); everyone sees it. Votes Blue received this round.
  - the table: votes_green (number, starts 0); everyone sees it. Votes Green received this round.
  - parameters, each kept as a table attribute: colors = 3, starting_price = 3, rounds = 6, influence_budget = 6, gem_first_award = 2, gem_second_award = 1, gem_tied_first_award = 1, commerce_first_award = 8, commerce_second_award = 3, commerce_tied_first_award = 3, price_rise_per_vote = 1, price_fall_no_votes = 1, price_floor = 1, favored_extra_multiplier = 1

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Set price_red, price_blue and price_green to 3.
  2. Set every player's red_gems, blue_gems, green_gems and commerce_points to 0.
  3. For each player in seat order, draw one color at random from color_deck into that player's favored_color and remove it from color_deck, so every player holds a different color.
  4. Sync: each player is told only their own favored_color.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round += 1.
  2. [tell] all players. What happens: Announce: 'Round {round}. Prices: Red {price_red}, Blue {price_blue}, Green {price_green}.' Also show every player's public gems and commerce_points.
  3. [poll] all players answers: short text message. What happens: Every message is broadcast to all once everyone has answered: {"to": "all", "text": "Seat {seat} says: {value}"}. Nothing is stored, and nothing is binding.
  4. [poll] all players answers: one choice from the 84 strings 'r/b/g/c', where r, b, g and c are whole numbers of 0 or more that sum to exactly 6 (influence in Red, Blue, Green and Commerce). What happens: pending_allocation := the choice. It stays hidden until every answer is in.
  5. [update] all players. What happens: Parse pending_allocation into alloc_red, alloc_blue, alloc_green and alloc_commerce, then announce all four values for every seat.
  6. [update] all players. What happens: Resolve each district D in {red, blue, green} with x = alloc_D. Let M = max of x over the players and N = the count of players with x == M. Let S = max of x over the players with x < M, and K = the count of players with x == S. For each player: if M > 0, x == M and N == 1, then D_gems += 2. If M > 0, x == M and N >= 2, then D_gems += 1. If N == 1, M > 0, S > 0, x == S and K == 1, then D_gems += 1. Otherwise nothing.
  7. [update] all players. What happens: Resolve Commerce the same way with x = alloc_commerce: a single first gets commerce_points += 8, each tied-first gets commerce_points += 3, and a single untied second gets commerce_points += 3. A player with 0 influence gains nothing.
  8. [poll] all players answers: one of: Red, Blue, Green. What happens: vote := the choice.
  9. [update] all players. What happens: votes_red := count of players with vote == 'Red'. votes_blue := count with vote == 'Blue'. votes_green := count with vote == 'Green'. For each color C: if votes_C > 0, then price_C += votes_C; else price_C := max(1, price_C - 1). Announce every seat's vote and the new prices.
  10. [update] all players. What happens: When round == 6: revealed_color := favored_color. score := red_gems*price_red + blue_gems*price_blue + green_gems*price_green + (favored_color=='Red' ? red_gems*price_red : 0) + (favored_color=='Blue' ? blue_gems*price_blue : 0) + (favored_color=='Green' ? green_gems*price_green : 0) + commerce_points. Announce every seat's revealed_color and score.
  11. [check] all players. What happens: If round >= 6, end the game; otherwise run the round again.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. At setup, each of the three players is dealt a different favored_color from Red, Blue and Green, and sees only their own.
  R2. At setup, price_red, price_blue and price_green are each 3, and every player has 0 gems of each color and 0 commerce_points.
  R3. The game lasts exactly 6 rounds and ends after round 6.
  R4. Each round, every player submits one talk message simultaneously, and all messages are shown only after all are in.
  R5. Each round, each player allocates whole-number influence of 0 or more to Red, Blue, Green and Commerce summing to exactly 6, and an allocation summing to anything else cannot be chosen.
  R6. Allocations are secret until all are submitted, then all four values of every player are revealed.
  R7. When one player has the strictly highest influence above 0 in a gem district, they gain 2 gems of that color (e.g. Red allocations 4,1,0 give the first player red_gems +2).
  R8. When a gem district has a single first, the player with the strictly next-highest influence above 0, untied, gains 1 gem of that color (e.g. Red allocations 4,1,0 give the second player red_gems +1 and the third player nothing).
  R9. When two or more players tie for highest influence above 0 in a gem district, each tied player gains 1 gem and no second is awarded (e.g. Blue allocations 3,3,1 give +1, +1 and 0).
  R10. When there is a single first but two players tie for second, no second is awarded (e.g. Green allocations 4,1,1 give +2, 0 and 0).
  R11. In Commerce, a single first gains 8 commerce_points, a single untied second gains 3, and each tied-first gains 3 (e.g. allocations 2,2,0 give 3, 3 and 0).
  R12. A player with 0 influence in a district gains nothing there, and if every player has 0 in a district, nobody gains.
  R13. Each round, every player simultaneously votes for one color: Red, Blue or Green.
  R14. After the vote, each color's price rises by 1 per vote it received (e.g. 2 votes raise price 3 to 5).
  R15. After the vote, each color with 0 votes falls by 1 but never below 1 (e.g. 3 becomes 2, and 1 stays 1).
  R16. After the price update, every player's vote is shown to all.
  R17. At game end, score = red_gems*price_red + blue_gems*price_blue + green_gems*price_green + (favored gems × that color's price) + commerce_points (e.g. favored Red, 2 red at price 5, 1 blue at price 2, 8 commerce gives 10+2+10+8 = 30).
  R18. At game end, every player's favored color is revealed.
  R19. The player with the highest score wins, and when two or three players tie for highest, the game is a draw among them.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Talk message | asked: every seat, simultaneously | options: any short free text
  - Allocation | asked: every seat, simultaneously | options: each of the 84 strings 'r/b/g/c' with whole numbers r, b, g, c >= 0 and r+b+g+c = 6, for example '6/0/0/0', '2/1/0/3', '0/0/0/6'
  - Market vote | asked: every seat, simultaneously | options: Red, Blue, Green

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round >= 6
  - each player's standing: you.score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their final score: gem values at final prices, favored-color gems counted twice, plus commerce points. The highest score wins. If two or three players tie at the top, they share the result, which is the source's draw.
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

- each player: `red_gems` (number, visible: public, starts 0): Red gems held.
- each player: `blue_gems` (number, visible: public, starts 0): Blue gems held.
- each player: `green_gems` (number, visible: public, starts 0): Green gems held.
- each player: `commerce_points` (number, visible: public, starts 0): Commerce points earned.
- each player: `revealed_color` (text, visible: public, starts ''): favored_color copied here when secret colors are revealed at game end.
- each player: `score` (number, visible: public, starts 0): Final score, computed after round 6.
- the table: `round` (number, visible: public, starts 0): Current round number (1 to 6).
- the table: `price_red` (number, visible: public, starts 3): Current Red price.
- the table: `price_blue` (number, visible: public, starts 3): Current Blue price.
- the table: `price_green` (number, visible: public, starts 3): Current Green price.
- parameters (each must be an attribute holding this value, never a number buried in a step): colors = 3, starting_price = 3, rounds = 6, influence_budget = 6, gem_first_award = 2, gem_second_award = 1, gem_tied_first_award = 1, commerce_first_award = 8, commerce_second_award = 3, commerce_tied_first_award = 3, price_rise_per_vote = 1, price_fall_no_votes = 1, price_floor = 1, favored_extra_multiplier = 1
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
