# 08 coder

- time: 2026-10-27T17:27:10+00:00 (44.9s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 429d3c5d4cc77993, reply sha256 1f3a2312de3ea837

## Sent

````
# Task: write the XColos game file for "Secret Salad"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

SETUP: There are three vegetables: Tomato (T), Lettuce (L), Carrot (C). There are three secret Recipes:
- Recipe TL is worth 2 per T + 2 per L + 2 per complete T-L pair (that is, 2 x the smaller of T and L).
- Recipe LC is worth 2 per L + 2 per C + 2 x the smaller of L and C.
- Recipe CT is worth 2 per C + 2 per T + 2 x the smaller of C and T.
Shuffle the three Recipes and deal one face down to each player. Each player sees only their own Recipe and knows the other two players hold the other two. Every player starts with T=0, L=0, C=0 and 0 points.

EACH ROUND (12 rounds):
1. Draw one point card at random, with replacement, from these 6 equally likely types:
- Tomato Fan: 2 points per T you hold.
- Lettuce Fan: 2 points per L you hold.
- Carrot Fan: 2 points per C you hold.
- Rainbow: 3 points per complete set of one T, one L and one C (3 x the smallest of your three counts).
- Big Bowl: 1 point per vegetable you hold (T+L+C).
- Balance: 6 points if you hold at least one of each vegetable and your largest count minus your smallest count is at most 1; otherwise 0.
2. Announce the round number, the point card, and every player's current T, L, C counts and points. Baskets and points are public; Recipes are not.
3. Talk: every player writes one short message at the same time without seeing the others. All messages are then shown to everyone. Talk is not binding and may be false.
4. Pick: every player simultaneously chooses exactly one of: Tomato, Lettuce, Carrot, or Card. The market each round holds exactly one Tomato, one Lettuce, one Carrot and the drawn point card.
5. Resolve: for each of the four options, count how many players chose it.
- If exactly one player chose a vegetable, that player adds 1 of it to their basket.
- If exactly one player chose Card, that player immediately scores the point card against their basket as it stands now, before this round's vegetables are added. Add those points to their total.
- If two or more players chose the same option, nobody receives it.
Unclaimed items are discarded.
6. Announce what every player picked and what they received.

END: After round 12, reveal all Recipes. Each player adds their Recipe score, computed on their final basket, to the points they earned from point cards. That sum is their final total.

How the winner is decided: The player with the highest final total wins. If two or three players tie for the highest total, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Secret Salad (3 to 3 players, best with 3)

Three players each hold a secret Recipe that values two of three vegetables, and each round they pick at the same time from a market of one Tomato, one Lettuce, one Carrot and a random point card; any option two or more players pick goes to nobody.

STATE (every item below must exist in the file):
  - each player: recipe (text, starts ''); only its owner sees it. This player's secret Recipe: TL, LC or CT. It is revealed to all after round 12.
  - each player: t (number, starts 0); everyone sees it. Tomatoes in the basket.
  - each player: l (number, starts 0); everyone sees it. Lettuces in the basket.
  - each player: c (number, starts 0); everyone sees it. Carrots in the basket.
  - each player: points (number, starts 0); everyone sees it. Points earned from point cards.
  - each player: pick (text, starts ''); everyone sees it. This round's pick: Tomato, Lettuce, Carrot or Card. It is collected by a simultaneous poll, so no one sees it until all picks are in.
  - each player: received (text, starts ''); everyone sees it. What this player received this round: nothing, a vegetable, or the card points.
  - each player: recipe_score (number, starts 0); everyone sees it. Recipe score on the final basket. It is computed after round 12.
  - each player: final_total (number, starts 0); everyone sees it. points + recipe_score. It is computed after round 12.
  - the table: round (number, starts 0); everyone sees it. The current round number, 1 to 12.
  - the table: recipe_deck (list, starts ['TL', 'LC', 'CT']); hidden from all players. The three Recipes, dealt one to each player at setup.
  - the table: card_types (list, starts ['Tomato Fan', 'Lettuce Fan', 'Carrot Fan', 'Rainbow', 'Big Bowl', 'Balance']); everyone sees it. The six equally likely point card types. A draw picks one at random and does not remove it (with replacement).
  - the table: current_card (text, starts ''); everyone sees it. The point card drawn this round.
  - parameters, each kept as a table attribute: players = 3, rounds = 12, recipe_per_vegetable = 2, recipe_pair_bonus = 2, card_types = 6, fan_per_vegetable = 2, rainbow_per_set = 3, big_bowl_per_vegetable = 1, balance_bonus = 6, balance_max_spread = 1, balance_min_each = 1, market_vegetables_each = 1, starting_count = 0, starting_points = 0

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Shuffle recipe_deck (TL, LC, CT) and deal one Recipe at random into each player's recipe, removing it from recipe_deck, so that each player holds a different Recipe.
  2. Each player sees only their own recipe and knows the other two players hold the other two Recipes.
  3. Every player starts with t=0, l=0, c=0 and points=0; round=0.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round += 1; current_card = one entry of card_types chosen at random, each of the 6 equally likely, without removing it (with replacement); every player's pick = '' and received = ''.
  2. [tell] all players. What happens: Announce round, current_card, and every player's t, l, c and points. Recipes are not shown.
  3. [poll] all players answers: short free text. What happens: Each player writes one message without seeing the others. All messages are then broadcast to all as 'Seat {seat} says: {value}'. Talk is not binding and may be false.
  4. [poll] all players answers: one of: Tomato, Lettuce, Carrot, Card. What happens: Each player's pick is set to their choice. Picks are simultaneous.
  5. [update] all players. What happens: Card resolves first, on baskets as they stand before this round's vegetables. If exactly one player has pick=='Card', that player's points += card value, where the card value is: Tomato Fan 2*t; Lettuce Fan 2*l; Carrot Fan 2*c; Rainbow 3*min(t,l,c); Big Bowl t+l+c; Balance 6 if min(t,l,c)>=1 and max(t,l,c)-min(t,l,c)<=1, else 0. Set that player's received to the points gained. If two or more players picked Card, nobody scores it.
  6. [update] all players. What happens: If exactly one player has pick=='Tomato', that player's t += 1. If exactly one player has pick=='Lettuce', that player's l += 1. If exactly one player has pick=='Carrot', that player's c += 1. Set received for each of these players. Any vegetable picked by two or more players goes to nobody, and unclaimed items are discarded. Every player who received nothing gets received='nothing'.
  7. [tell] all players. What happens: Announce every player's pick and received, and the updated t, l, c and points.
  8. [update] all players. What happens: When round==12, for each player: recipe_score = 2*t+2*l+2*min(t,l) if recipe=='TL'; 2*l+2*c+2*min(l,c) if recipe=='LC'; 2*c+2*t+2*min(c,t) if recipe=='CT'. Then final_total = points + recipe_score.
  9. [tell] all players. What happens: When round==12, reveal every player's recipe, recipe_score and final_total.
  10. [check] all players. What happens: End the game if round==12; otherwise continue to the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. At setup, each of the 3 players is dealt a different Recipe from TL, LC, CT, visible only to that player.
  R2. At setup, every player has t=0, l=0, c=0 and points=0.
  R3. Each round, current_card is drawn at random with replacement from the 6 types Tomato Fan, Lettuce Fan, Carrot Fan, Rainbow, Big Bowl, Balance.
  R4. Each round, every player's t, l, c and points and the current_card are announced to all, while Recipes stay hidden.
  R5. Each round, every player writes one message simultaneously and all messages are then shown to everyone.
  R6. Each round, every player simultaneously picks exactly one of Tomato, Lettuce, Carrot, Card.
  R7. When exactly one player picks Tomato, then that player's t increases by 1.
  R8. When exactly one player picks Lettuce, then that player's l increases by 1.
  R9. When exactly one player picks Carrot, then that player's c increases by 1.
  R10. When two or more players pick the same option, then nobody receives that option.
  R11. When exactly one player picks Card, then that player scores the card on their basket as it stood before this round's vegetables are added.
  R12. When a player with t=3 scores Tomato Fan, then they gain 6 points (2 per T).
  R13. When a player with l=2 scores Lettuce Fan, then they gain 4 points (2 per L).
  R14. When a player with c=1 scores Carrot Fan, then they gain 2 points (2 per C).
  R15. When a player with t=2, l=3, c=1 scores Rainbow, then they gain 3 points (3 x min).
  R16. When a player with t=2, l=3, c=1 scores Big Bowl, then they gain 6 points (1 per vegetable).
  R17. When a player with t=2, l=2, c=1 scores Balance, then they gain 6 points, because each count is at least 1 and max-min=1.
  R18. When a player with t=3, l=1, c=1 or with c=0 scores Balance, then they gain 0 points.
  R19. After each round, every player's pick and what they received are announced to all.
  R20. When round 12 ends, then the game ends and all Recipes are revealed.
  R21. When a TL player ends with t=3, l=2, then recipe_score=14 (2*3+2*2+2*2).
  R22. When an LC player ends with l=1, c=4, then recipe_score=12 (2*1+2*4+2*1).
  R23. When a CT player ends with c=2, t=2, then recipe_score=16.
  R24. Final total = points + recipe_score, and the highest final total wins, with players tied at the top sharing the win.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Talk message | asked: all seats, simultaneously | options: Any short free-text message.
  - Pick | asked: all seats, simultaneously | options: Every seat, every round: Tomato, Lettuce, Carrot, Card.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round == 12
  - each player's standing: you.points + you.recipe_score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's final total is their point-card points plus their Recipe score on the final basket. The highest final total wins; players tied at the top share the result (the source calls this a draw).
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

- each player: `t` (number, visible: public, starts 0): Tomatoes in the basket.
- each player: `l` (number, visible: public, starts 0): Lettuces in the basket.
- each player: `c` (number, visible: public, starts 0): Carrots in the basket.
- each player: `points` (number, visible: public, starts 0): Points earned from point cards.
- each player: `pick` (text, visible: public, starts ''): This round's pick: Tomato, Lettuce, Carrot or Card. It is collected by a simultaneous poll, so no one sees it until all picks are in.
- each player: `recipe_score` (number, visible: public, starts 0): Recipe score on the final basket. It is computed after round 12.
- each player: `final_total` (number, visible: public, starts 0): points + recipe_score. It is computed after round 12.
- the table: `round` (number, visible: public, starts 0): The current round number, 1 to 12.
- the table: `current_card` (text, visible: public, starts ''): The point card drawn this round.
- parameters (each must be an attribute holding this value, never a number buried in a step): players = 3, rounds = 12, recipe_per_vegetable = 2, recipe_pair_bonus = 2, card_types = 6, fan_per_vegetable = 2, rainbow_per_set = 3, big_bowl_per_vegetable = 1, balance_bonus = 6, balance_max_spread = 1, balance_min_each = 1, market_vegetables_each = 1, starting_count = 0, starting_points = 0
- the game ends with ONE ending whose `rank_by` is `you.points + you.recipe_score`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
{
  "schema": 1,
  "meta": {
    "id": "secret_salad",
    "name": "Secret Salad",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Three secret Recipes, one shared market: pick Tomato, Lettuce, Carrot or the point card at the same time, and anything two players pick goes to nobody."
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
        "key": "recipe",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "t",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "l",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "c",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "pick",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "received",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "recipe_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "final_total",
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
        "key": "recipe_deck",
        "visible": "none",
        "type": "list",
        "initial": [
          "TL",
          "LC",
          "CT"
        ]
      },
      {
        "key": "deal_pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "card_pool",
        "visible": "public",
        "type": "list",
        "initial": [
          "Tomato Fan",
          "Lettuce Fan",
          "Carrot Fan",
          "Rainbow",
          "Big Bowl",
          "Balance"
        ]
      },
      {
        "key": "current_card",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "players",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "recipe_per_vegetable",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "recipe_pair_bonus",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "card_types",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "fan_per_vegetable",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "rainbow_per_set",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "big_bowl_per_vegetable",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "balance_bonus",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "balance_max_spread",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "balance_min_each",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "market_vegetables_each",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "starting_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "starting_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "deal the recipes",
      "do": [
        {
          "set": {
            "key": "deal_pick",
            "value": {
              "calc": "recipe_deck[min(len(recipe_deck) - 1, int(uniform(0, len(recipe_deck))))]"
            }
          }
        },
        {
          "set": {
            "player": 1,
            "key": "recipe",
            "value": {
              "calc": "deal_pick"
            }
          }
        },
        {
          "remove": {
            "key": "recipe_deck",
            "value": {
              "calc": "deal_pick"
            }
          }
        },
        {
          "set": {
            "key": "deal_pick",
            "value": {
              "calc": "recipe_deck[min(len(recipe_deck) - 1, int(uniform(0, len(recipe_deck))))]"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "recipe",
            "value": {
              "calc": "deal_pick"
            }
          }
        },
        {
          "remove": {
            "key": "recipe_deck",
            "value": {
              "calc": "deal_pick"
            }
          }
        },
        {
          "set": {
            "key": "deal_pick",
            "value": {
              "calc": "recipe_deck[min(len(recipe_deck) - 1, int(uniform(0, len(recipe_deck))))]"
            }
          }
        },
        {
          "set": {
            "player": 3,
            "key": "recipe",
            "value": {
              "calc": "deal_pick"
            }
          }
        },
        {
          "remove": {
            "key": "recipe_deck",
            "value": {
              "calc": "deal_pick"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "starting baskets",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "t",
            "value": {
              "calc": "starting_count"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "l",
            "value": {
              "calc": "starting_count"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "c",
            "value": {
              "calc": "starting_count"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "points",
            "value": {
              "calc": "starting_points"
            }
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
      "label": "your recipe",
      "mode": "self",
      "to": "all",
      "text": "You start with (your Recipe is secret; the other two players hold the other two Recipes):"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "draw",
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
            "key": "current_card",
            "value": {
              "calc": "card_pool[min(card_types - 1, int(uniform(0, card_types)))]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "pick",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "received",
            "value": ""
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "draw",
      "label": "the market",
      "to": "all",
      "text": "Round {round} of {rounds}. The point card is {current_card}. The market holds one Tomato, one Lettuce, one Carrot and the card. Baskets [seat, T, L, C, points]: {[[p.seat, p.t, p.l, p.c, p.points] for p in acting]}."
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
      "text": "Write one short message to the table. Everyone writes at the same time; talk is not binding and may be false."
    },
    {
      "use": "poll",
      "phase": "pick",
      "label": "pick",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": [
          "Tomato",
          "Lettuce",
          "Carrot",
          "Card"
        ]
      },
      "store": "pick",
      "text": "Pick exactly one of Tomato, Lettuce, Carrot or Card. Everyone picks at the same time. If you are the only one to pick an option you receive it; if two or more pick it, nobody receives it."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "the card resolves",
      "do": [
        {
          "adjust": {
            "players": {
              "where": "you.pick == 'Card' and count(p.pick == 'Card' for p in acting) == 1"
            },
            "key": "points",
            "value": {
              "calc": "(fan_per_vegetable * you.t) if current_card == 'Tomato Fan' else ((fan_per_vegetable * you.l) if current_card == 'Lettuce Fan' else ((fan_per_vegetable * you.c) if current_card == 'Carrot Fan' else ((rainbow_per_set * min([you.t, you.l, you.c])) if current_card == 'Rainbow' else ((big_bowl_per_vegetable * (you.t + you.l + you.c)) if current_card == 'Big Bowl' else (balance_bonus if (min([you.t, you.l, you.c]) >= balance_min_each and max([you.t, you.l, you.c]) - min([you.t, you.l, you.c]) <= balance_max_spread) else 0)))))"
            },
            "text": "Seat {player} alone took the {current_card} card and scores it on their basket."
          }
        },
        {
          "set": {
            "players": {
              "where": "you.pick == 'Card' and count(p.pick == 'Card' for p in acting) == 1"
            },
            "key": "received",
            "value": "the card points"
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "the vegetables resolve",
      "do": [
        {
          "adjust": {
            "players": {
              "where": "you.pick == 'Tomato' and count(p.pick == 'Tomato' for p in acting) == 1"
            },
            "key": "t",
            "value": {
              "calc": "market_vegetables_each"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.pick == 'Tomato' and count(p.pick == 'Tomato' for p in acting) == 1"
            },
            "key": "received",
            "value": "a Tomato"
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.pick == 'Lettuce' and count(p.pick == 'Lettuce' for p in acting) == 1"
            },
            "key": "l",
            "value": {
              "calc": "market_vegetables_each"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.pick == 'Lettuce' and count(p.pick == 'Lettuce' for p in acting) == 1"
            },
            "key": "received",
            "value": "a Lettuce"
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.pick == 'Carrot' and count(p.pick == 'Carrot' for p in acting) == 1"
            },
            "key": "c",
            "value": {
              "calc": "market_vegetables_each"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.pick == 'Carrot' and count(p.pick == 'Carrot' for p in acting) == 1"
            },
            "key": "received",
            "value": "a Carrot"
          }
        },
        {
          "set": {
            "players": {
              "where": "you.received == ''"
            },
            "key": "received",
            "value": "nothing"
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "resolve",
      "label": "the picks",
      "to": "all",
      "text": "Round {round} picks [seat, pick, received]: {[[p.seat, p.pick, p.received] for p in acting]}. Baskets now [seat, T, L, C, points]: {[[p.seat, p.t, p.l, p.c, p.points] for p in acting]}."
    },
    {
      "use": "update",
      "phase": "final",
      "label": "recipe scores",
      "when": {
        "calc": "round >= rounds"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "recipe_score",
            "value": {
              "calc": "(recipe_per_vegetable * you.t + recipe_per_vegetable * you.l + recipe_pair_bonus * min([you.t, you.l])) if you.recipe == 'TL' else ((recipe_per_vegetable * you.l + recipe_per_vegetable * you.c + recipe_pair_bonus * min([you.l, you.c])) if you.recipe == 'LC' else ((recipe_per_vegetable * you.c + recipe_per_vegetable * you.t + recipe_pair_bonus * min([you.c, you.t])) if you.recipe == 'CT' else 0))"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "final_total",
            "value": {
              "calc": "you.points + you.recipe_score"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "final",
      "label": "the recipes revealed",
      "when": {
        "calc": "round >= rounds"
      },
      "to": "all",
      "text": "All Recipes revealed [seat, recipe, card points, recipe score, final total]: {[[p.seat, p.recipe, p.points, p.recipe_score, p.final_total] for p in acting]}."
    },
    {
      "use": "check",
      "phase": "final",
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
      "rank_by": "you.points + you.recipe_score",
      "reveal": [
        "recipe"
      ],
      "text": "Winner: {result}. Final totals [seat, recipe, total]: {[[p.seat, p.recipe, p.points + p.recipe_score] for p in acting]}."
    }
  },
  "limits": {
    "rounds": 12,
    "rounds_max": 12,
    "actions_max": 400,
    "deadline_s": 120
  },
  "rules": "SETUP: There are three vegetables: Tomato (T), Lettuce (L), Carrot (C). There are three secret Recipes:\n- Recipe TL is worth {recipe_per_vegetable} per T + {recipe_per_vegetable} per L + {recipe_pair_bonus} per complete T-L pair (that is, {recipe_pair_bonus} x the smaller of T and L).\n- Recipe LC is worth {recipe_per_vegetable} per L + {recipe_per_vegetable} per C + {recipe_pair_bonus} x the smaller of L and C.\n- Recipe CT is worth {recipe_per_vegetable} per C + {recipe_per_vegetable} per T + {recipe_pair_bonus} x the smaller of C and T.\nThe three Recipes are shuffled and one is dealt face down to each player. Each player sees only their own Recipe and knows the other two players hold the other two. Every player starts with T={starting_count}, L={starting_count}, C={starting_count} and {starting_points} points.\n\nEACH ROUND ({rounds} rounds):\n1. One point card is drawn at random, with replacement, from these {card_types} equally likely types:\n- Tomato Fan: {fan_per_vegetable} points per T you hold.\n- Lettuce Fan: {fan_per_vegetable} points per L you hold.\n- Carrot Fan: {fan_per_vegetable} points per C you hold.\n- Rainbow: {rainbow_per_set} points per complete set of one T, one L and one C ({rainbow_per_set} x the smallest of your three counts).\n- Big Bowl: {big_bowl_per_vegetable} point per vegetable you hold (T+L+C).\n- Balance: {balance_bonus} points if you hold at least {balance_min_each} of each vegetable and your largest count minus your smallest count is at most {balance_max_spread}; otherwise 0.\n2. The round number, the point card, and every player's current T, L, C counts and points are announced. Baskets and points are public; Recipes are not.\n3. Talk: every player writes one short message at the same time without seeing the others. All messages are then shown to everyone. Talk is not binding and may be false.\n4. Pick: every player simultaneously chooses exactly one of: Tomato, Lettuce, Carrot, or Card. The market each round holds exactly one Tomato, one Lettuce, one Carrot and the drawn point card.\n5. Resolve: for each of the four options, count how many players chose it.\n- If exactly one player chose a vegetable, that player adds 1 of it to their basket.\n- If exactly one player chose Card, that player immediately scores the point card against their basket as it stands now, before this round's vegetables are added. Those points are added to their total.\n- If two or more players chose the same option, nobody receives it.\nUnclaimed items are discarded.\n6. What every player picked and what they received is announced.\n\nEND: After round {rounds}, all Recipes are revealed. Each player adds their Recipe score, computed on their final basket, to the points they earned from point cards. That sum is their final total. The player with the highest final total wins; players tied for the highest total share the win."
}

Why it was refused: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (pick, received, pick, received) in `your_recipe`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "secret_salad",
    "name": "Secret Salad",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Three secret Recipes, one shared market: pick Tomato, Lettuce, Carrot or the point card at the same time, and anything two players pick goes to nobody."
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
        "key": "recipe",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "t",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "l",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "c",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "pick",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "received",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "recipe_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "final_total",
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
        "key": "recipe_deck",
        "visible": "none",
        "type": "list",
        "initial": [
          "TL",
          "LC",
          "CT"
        ]
      },
      {
        "key": "deal_pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "card_pool",
        "visible": "public",
        "type": "list",
        "initial": [
          "Tomato Fan",
          "Lettuce Fan",
          "Carrot Fan",
          "Rainbow",
          "Big Bowl",
          "Balance"
        ]
      },
      {
        "key": "current_card",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "players",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "recipe_per_vegetable",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "recipe_pair_bonus",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "card_types",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "fan_per_vegetable",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "rainbow_per_set",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "big_bowl_per_vegetable",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "balance_bonus",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "balance_max_spread",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "balance_min_each",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "market_vegetables_each",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "starting_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "starting_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "deal the recipes",
      "do": [
        {
          "set": {
            "key": "deal_pick",
            "value": {
              "calc": "recipe_deck[min(len(recipe_deck) - 1, int(uniform(0, len(recipe_deck))))]"
            }
          }
        },
        {
          "set": {
            "player": 1,
            "key": "recipe",
            "value": {
              "calc": "deal_pick"
            }
          }
        },
        {
          "remove": {
            "key": "recipe_deck",
            "value": {
              "calc": "deal_pick"
            }
          }
        },
        {
          "set": {
            "key": "deal_pick",
            "value": {
              "calc": "recipe_deck[min(len(recipe_deck) - 1, int(uniform(0, len(recipe_deck))))]"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "recipe",
            "value": {
              "calc": "deal_pick"
            }
          }
        },
        {
          "remove": {
            "key": "recipe_deck",
            "value": {
              "calc": "deal_pick"
            }
          }
        },
        {
          "set": {
            "key": "deal_pick",
            "value": {
              "calc": "recipe_deck[min(len(recipe_deck) - 1, int(uniform(0, len(recipe_deck))))]"
            }
          }
        },
        {
          "set": {
            "player": 3,
            "key": "recipe",
            "value": {
              "calc": "deal_pick"
            }
          }
        },
        {
          "remove": {
            "key": "recipe_deck",
            "value": {
              "calc": "deal_pick"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "starting baskets",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "t",
            "value": {
              "calc": "starting_count"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "l",
            "value": {
              "calc": "starting_count"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "c",
            "value": {
              "calc": "starting_count"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "points",
            "value": {
              "calc": "starting_points"
            }
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
      "label": "your recipe",
      "mode": "self",
      "to": "all",
      "fields": [
        "recipe",
        "t",
        "l",
        "c",
        "points"
      ],
      "text": "You start with (your Recipe is secret; the other two players hold the other two Recipes):"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "draw",
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
            "key": "current_card",
            "value": {
              "calc": "card_pool[min(card_types - 1, int(uniform(0, card_types)))]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "pick",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "received",
            "value": ""
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "draw",
      "label": "the market",
      "to": "all",
      "text": "Round {round} of {rounds}. The point card is {current_card}. The market holds one Tomato, one Lettuce, one Carrot and the card. Baskets [seat, T, L, C, points]: {[[p.seat, p.t, p.l, p.c, p.points] for p in acting]}."
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
      "text": "Write one short message to the table. Everyone writes at the same time; talk is not binding and may be false."
    },
    {
      "use": "poll",
      "phase": "pick",
      "label": "pick",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": [
          "Tomato",
          "Lettuce",
          "Carrot",
          "Card"
        ]
      },
      "store": "pick",
      "text": "Pick exactly one of Tomato, Lettuce, Carrot or Card. Everyone picks at the same time. If you are the only one to pick an option you receive it; if two or more pick it, nobody receives it."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "the card resolves",
      "do": [
        {
          "adjust": {
            "players": {
              "where": "you.pick == 'Card' and count(p.pick == 'Card' for p in acting) == 1"
            },
            "key": "points",
            "value": {
              "calc": "(fan_per_vegetable * you.t) if current_card == 'Tomato Fan' else ((fan_per_vegetable * you.l) if current_card == 'Lettuce Fan' else ((fan_per_vegetable * you.c) if current_card == 'Carrot Fan' else ((rainbow_per_set * min([you.t, you.l, you.c])) if current_card == 'Rainbow' else ((big_bowl_per_vegetable * (you.t + you.l + you.c)) if current_card == 'Big Bowl' else (balance_bonus if (min([you.t, you.l, you.c]) >= balance_min_each and max([you.t, you.l, you.c]) - min([you.t, you.l, you.c]) <= balance_max_spread) else 0)))))"
            },
            "text": "Seat {player} alone took the {current_card} card and scores it on their basket."
          }
        },
        {
          "set": {
            "players": {
              "where": "you.pick == 'Card' and count(p.pick == 'Card' for p in acting) == 1"
            },
            "key": "received",
            "value": "the card points"
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "the vegetables resolve",
      "do": [
        {
          "adjust": {
            "players": {
              "where": "you.pick == 'Tomato' and count(p.pick == 'Tomato' for p in acting) == 1"
            },
            "key": "t",
            "value": {
              "calc": "market_vegetables_each"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.pick == 'Tomato' and count(p.pick == 'Tomato' for p in acting) == 1"
            },
            "key": "received",
            "value": "a Tomato"
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.pick == 'Lettuce' and count(p.pick == 'Lettuce' for p in acting) == 1"
            },
            "key": "l",
            "value": {
              "calc": "market_vegetables_each"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.pick == 'Lettuce' and count(p.pick == 'Lettuce' for p in acting) == 1"
            },
            "key": "received",
            "value": "a Lettuce"
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.pick == 'Carrot' and count(p.pick == 'Carrot' for p in acting) == 1"
            },
            "key": "c",
            "value": {
              "calc": "market_vegetables_each"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.pick == 'Carrot' and count(p.pick == 'Carrot' for p in acting) == 1"
            },
            "key": "received",
            "value": "a Carrot"
          }
        },
        {
          "set": {
            "players": {
              "where": "you.received == ''"
            },
            "key": "received",
            "value": "nothing"
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "resolve",
      "label": "the picks",
      "to": "all",
      "text": "Round {round} picks [seat, pick, received]: {[[p.seat, p.pick, p.received] for p in acting]}. Baskets now [seat, T, L, C, points]: {[[p.seat, p.t, p.l, p.c, p.points] for p in acting]}."
    },
    {
      "use": "update",
      "phase": "final",
      "label": "recipe scores",
      "when": {
        "calc": "round >= rounds"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "recipe_score",
            "value": {
              "calc": "(recipe_per_vegetable * you.t + recipe_per_vegetable * you.l + recipe_pair_bonus * min([you.t, you.l])) if you.recipe == 'TL' else ((recipe_per_vegetable * you.l + recipe_per_vegetable * you.c + recipe_pair_bonus * min([you.l, you.c])) if you.recipe == 'LC' else ((recipe_per_vegetable * you.c + recipe_per_vegetable * you.t + recipe_pair_bonus * min([you.c, you.t])) if you.recipe == 'CT' else 0))"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "final_total",
            "value": {
              "calc": "you.points + you.recipe_score"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "final",
      "label": "the recipes revealed",
      "when": {
        "calc": "round >= rounds"
      },
      "to": "all",
      "text": "All Recipes revealed [seat, recipe, card points, recipe score, final total]: {[[p.seat, p.recipe, p.points, p.recipe_score, p.final_total] for p in acting]}."
    },
    {
      "use": "check",
      "phase": "final",
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
      "rank_by": "you.points + you.recipe_score",
      "reveal": [
        "recipe"
      ],
      "text": "Winner: {result}. Final totals [seat, recipe, total]: {[[p.seat, p.recipe, p.points + p.recipe_score] for p in acting]}."
    }
  },
  "limits": {
    "rounds": 12,
    "rounds_max": 12,
    "actions_max": 400,
    "deadline_s": 120
  },
  "rules": "SETUP: There are three vegetables: Tomato (T), Lettuce (L), Carrot (C). There are three secret Recipes:\n- Recipe TL is worth {recipe_per_vegetable} per T + {recipe_per_vegetable} per L + {recipe_pair_bonus} per complete T-L pair (that is, {recipe_pair_bonus} x the smaller of T and L).\n- Recipe LC is worth {recipe_per_vegetable} per L + {recipe_per_vegetable} per C + {recipe_pair_bonus} x the smaller of L and C.\n- Recipe CT is worth {recipe_per_vegetable} per C + {recipe_per_vegetable} per T + {recipe_pair_bonus} x the smaller of C and T.\nThe three Recipes are shuffled and one is dealt face down to each player. Each player sees only their own Recipe and knows the other two players hold the other two. Every player starts with T={starting_count}, L={starting_count}, C={starting_count} and {starting_points} points.\n\nEACH ROUND ({rounds} rounds):\n1. One point card is drawn at random, with replacement, from these {card_types} equally likely types:\n- Tomato Fan: {fan_per_vegetable} points per T you hold.\n- Lettuce Fan: {fan_per_vegetable} points per L you hold.\n- Carrot Fan: {fan_per_vegetable} points per C you hold.\n- Rainbow: {rainbow_per_set} points per complete set of one T, one L and one C ({rainbow_per_set} x the smallest of your three counts).\n- Big Bowl: {big_bowl_per_vegetable} point per vegetable you hold (T+L+C).\n- Balance: {balance_bonus} points if you hold at least {balance_min_each} of each vegetable and your largest count minus your smallest count is at most {balance_max_spread}; otherwise 0.\n2. The round number, the point card, and every player's current T, L, C counts and points are announced. Baskets and points are public; Recipes are not.\n3. Talk: every player writes one short message at the same time without seeing the others. All messages are then shown to everyone. Talk is not binding and may be false.\n4. Pick: every player simultaneously chooses exactly one of: Tomato, Lettuce, Carrot, or Card. The market each round holds exactly one Tomato, one Lettuce, one Carrot and the drawn point card.\n5. Resolve: for each of the four options, count how many players chose it.\n- If exactly one player chose a vegetable, that player adds 1 of it to their basket.\n- If exactly one player chose Card, that player immediately scores the point card against their basket as it stands now, before this round's vegetables are added. Those points are added to their total.\n- If two or more players chose the same option, nobody receives it.\nUnclaimed items are discarded.\n6. What every player picked and what they received is announced.\n\nEND: After round {rounds}, all Recipes are revealed. Each player adds their Recipe score, computed on their final basket, to the points they earned from point cards. That sum is their final total. The player with the highest final total wins; players tied for the highest total share the win."
}
```
````
