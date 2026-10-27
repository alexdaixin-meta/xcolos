# 25 coder

- time: 2026-10-27T17:40:28+00:00 (54.8s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 8d661bb176d445f6, reply sha256 fed8234035b574b3

## Sent

````
# Task: write the XColos game file for "Point Salad: Secret Recipes"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

VEGETABLES: Tomato (t), Lettuce (l), Carrot (c).

SETUP
1. There are exactly 3 players.
2. Recipes:
- There are 3 Recipe tiles: TL (tomato and lettuce), LC (lettuce and carrot) and CT (carrot and tomato).
- Shuffle them and deal one to each player, so all three are used.
- Each player sees only their own Recipe.
- A Recipe never changes, moves or rotates for the rest of the game.
3. Every player starts with t=0, l=0, c=0 and points=0. Baskets (t, l, c) and points are public at all times. Recipes are secret until game end.

EACH ROUND (12 rounds)
1. Draw the card: one scoring card type is drawn at random, with replacement, equally likely from these 6. It is announced to everyone.
- Tomato Fan: worth 2 × t.
- Lettuce Fan: worth 2 × l.
- Carrot Fan: worth 2 × c.
- Rainbow: worth 3 × min(t, l, c).
- Big Bowl: worth 1 × (t + l + c).
- Balance: worth 6 if t ≥ 1, l ≥ 1, c ≥ 1 and max(t,l,c) − min(t,l,c) ≤ 1; otherwise 0.
2. Talk:
- Every player writes one short message at the same time, without seeing the others.
- All messages are then shown to everyone.
- Messages bind no one.
3. Pick: every player at the same moment chooses exactly one of Tomato, Lettuce, Carrot, Card.
4. Resolve the Card:
- If exactly one player chose Card, that player gains points equal to the drawn card's value, computed from their basket as it stood at the start of this round.
- If zero players, or two or more players, chose Card, nobody gains anything from it. The card is discarded and colliding players receive nothing this round.
5. Resolve vegetables, separately for each vegetable:
- If exactly 1 player chose it, that player adds 2 of it to their basket.
- If exactly 2 players chose it, each adds 1.
- If all 3 chose it, nobody gets any.
6. Announce: everyone's pick, what each received, and all baskets and points.
7. If 12 rounds have been played, go to END. Otherwise start the next round.

END
1. Each player's Recipe is revealed and scored. With first and second as that player's counts of the Recipe's two vegetables:
recipe_score = 2 × first + 2 × second + 2 × min(first, second).
The third vegetable scores nothing in the Recipe.
- TL uses t and l.
- LC uses l and c.
- CT uses c and t.
2. Worked examples (exact):
- CT with c=2, t=2: 4 + 4 + 4 = 12.
- CT with c=3, t=2: 6 + 4 + 4 = 14.
- TL with t=4, l=1: 8 + 2 + 2 = 12.
- LC with l=0, c=6: 0 + 12 + 0 = 12.
3. final_total = points + recipe_score.
4. Example of points deciding the game: a player with points=10 and recipe 12 (final 22) beats a player with points=0 and recipe 14 (final 14).

CARD EXAMPLE: A player starting a round with t=3, l=1, c=2 who is the sole Card claimant scores:
- Tomato Fan: 6
- Lettuce Fan: 2
- Carrot Fan: 4
- Rainbow: 3
- Big Bowl: 6
- Balance: 0 (spread 2 > 1)

How the winner is decided: After round 12, the player with the highest final_total (points + recipe_score) wins. If two or three players tie for the highest final_total, the game is a draw among them.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Point Salad: Secret Recipes (3 to 3 players, best with 3)

Three players each hold a secret two-vegetable Recipe. Over 12 rounds they talk, then all at once pick a vegetable or the shared scoring Card. Collisions shrink or cancel gains, and the highest points plus recipe score wins.

STATE (every item below must exist in the file):
  - each player: t (number, starts 0); everyone sees it. tomatoes in basket
  - each player: l (number, starts 0); everyone sees it. lettuces in basket
  - each player: c (number, starts 0); everyone sees it. carrots in basket
  - each player: points (number, starts 0); everyone sees it. points won from the Card
  - each player: recipe (text, starts ''); only its owner sees it. secret Recipe tile: TL, LC or CT; revealed at game end
  - each player: pick (text, starts ''); everyone sees it. this round's pick: Tomato, Lettuce, Carrot or Card
  - each player: card_value (number, starts 0); only its owner sees it. value of this round's drawn card, computed from the basket at the start of the round
  - each player: recipe_score (number, starts 0); only its owner sees it. 2*first + 2*second + 2*min(first, second) for the two Recipe vegetables; revealed at game end
  - each player: message (text, starts ''); everyone sees it. this round's talk message
  - the table: round (number, starts 0); everyone sees it. rounds started so far
  - the table: card (text, starts ''); everyone sees it. the scoring card drawn this round
  - the table: card_types (list, starts ['Tomato Fan', 'Lettuce Fan', 'Carrot Fan', 'Rainbow', 'Big Bowl', 'Balance']); everyone sees it. the 6 card types, drawn from with replacement
  - the table: recipe_deck (list, starts ['TL', 'LC', 'CT']); hidden from all players. Recipe tiles still to deal
  - the table: n_card (number, starts 0); everyone sees it. players who picked Card this round
  - the table: n_t (number, starts 0); everyone sees it. players who picked Tomato this round
  - the table: n_l (number, starts 0); everyone sees it. players who picked Lettuce this round
  - the table: n_c (number, starts 0); everyone sees it. players who picked Carrot this round
  - parameters, each kept as a table attribute: player_count = 3, rounds = 12, card_types_count = 6, fan_multiplier = 2, rainbow_multiplier = 3, big_bowl_multiplier = 1, balance_value = 6, balance_min_each = 1, balance_max_spread = 1, sole_vegetable_gain = 2, pair_vegetable_gain = 1, triple_vegetable_gain = 0, recipe_first_weight = 2, recipe_second_weight = 2, recipe_min_weight = 2, start_vegetables = 0, start_points = 0

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Every player starts with t=0, l=0, c=0 and points=0, all public.
  2. The three Recipe tiles TL, LC and CT are dealt at random from recipe_deck, one into each player's recipe; recipe_deck ends empty.
  3. Each player is told only their own recipe.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round += 1; card = one entry of card_types drawn at random, with replacement and equally likely; announce round and card to everyone
  2. [update] all players. What happens: for each player, card_value is set from the current t, l, c: Tomato Fan 2*t; Lettuce Fan 2*l; Carrot Fan 2*c; Rainbow 3*min(t,l,c); Big Bowl t+l+c; Balance 6 if t>=1 and l>=1 and c>=1 and max(t,l,c)-min(t,l,c)<=1, otherwise 0
  3. [poll] all players answers: short text message. What happens: message set for each player; then broadcast {"to": "all", "text": "Seat {seat} says: {value}"}; messages bind no one
  4. [poll] all players answers: one of Tomato, Lettuce, Carrot, Card. What happens: pick set for each player; nobody sees a pick until all are in
  5. [update] all players. What happens: n_card = number of players with pick == Card; n_t = number with pick == Tomato; n_l = number with pick == Lettuce; n_c = number with pick == Carrot
  6. [update] all players. What happens: for each player: if pick == Card and n_card == 1, then points += card_value; otherwise no change
  7. [update] all players. What happens: for each player: if pick == Tomato, t += 2 when n_t == 1, t += 1 when n_t == 2, and nothing when n_t == 3; the same for Lettuce with l and n_l, and for Carrot with c and n_c
  8. [update] all players. What happens: recipe_score set for each player: TL gives 2*t + 2*l + 2*min(t,l); LC gives 2*l + 2*c + 2*min(l,c); CT gives 2*c + 2*t + 2*min(c,t)
  9. [tell] all players. What happens: announce every player's pick, what each received (Card points or vegetables), and every player's t, l, c and points
  10. [tell] all players. What happens: when round == 12: reveal every player's recipe, recipe_score and points + recipe_score to everyone
  11. [check] all players. What happens: if round >= 12, end the game; otherwise start the next round

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. At setup, each of the 3 players gets exactly one distinct Recipe from TL, LC and CT, and starts with t=0, l=0, c=0 and points=0.
  R2. Each round, exactly one card is drawn at random with replacement from the 6 types and announced to everyone.
  R3. When the card is Tomato Fan, its value for a player is 2*t; when it is Lettuce Fan, 2*l; when it is Carrot Fan, 2*c.
  R4. When the card is Rainbow, its value is 3*min(t,l,c); for example, t=3, l=1, c=2 gives 3.
  R5. When the card is Big Bowl, its value is t+l+c; for example, t=3, l=1, c=2 gives 6.
  R6. When the card is Balance, its value is 6 if t, l and c are each at least 1 and max minus min is at most 1, otherwise 0; for example, t=3, l=1, c=2 gives 0.
  R7. The card's value is computed from the basket as it stood at the start of the round, before any vegetables are added.
  R8. Each round, every player writes one short message at the same time, and all messages are then shown to everyone.
  R9. Each round, every player simultaneously picks exactly one of Tomato, Lettuce, Carrot or Card.
  R10. When exactly one player picks Card, that player's points increase by the card's value.
  R11. When zero players or two or more players pick Card, nobody's points change from the card.
  R12. When exactly one player picks a vegetable, that player adds 2 of it to their basket.
  R13. When exactly two players pick the same vegetable, each of them adds 1 of it.
  R14. When all three players pick the same vegetable, nobody receives any of it.
  R15. After each round, every pick, what each player received, and all baskets and points are announced.
  R16. The game ends after round 12.
  R17. A player's recipe_score is 2*first + 2*second + 2*min(first,second) over the Recipe's two vegetables: TL uses t and l, LC uses l and c, CT uses c and t. For example, CT with c=3 and t=2 scores 14, and LC with l=0 and c=6 scores 12.
  R18. At the end, recipes are revealed and the player with the highest points + recipe_score wins; for example, points 10 with recipe 12 (total 22) beats points 0 with recipe 14 (total 14).
  R19. When two or three players tie for the highest points + recipe_score, the game is a draw among them.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Talk message | asked: every seat | options: any short free text
  - Pick | asked: every seat | options: Tomato, Lettuce, Carrot, Card

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round >= 12
  - each player's standing: you.points + you.recipe_score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's final_total is points plus recipe_score. The highest final_total wins, and players tied at the top share a draw.
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

- each player: `t` (number, visible: public, starts 0): tomatoes in basket
- each player: `l` (number, visible: public, starts 0): lettuces in basket
- each player: `c` (number, visible: public, starts 0): carrots in basket
- each player: `points` (number, visible: public, starts 0): points won from the Card
- each player: `pick` (text, visible: public, starts ''): this round's pick: Tomato, Lettuce, Carrot or Card
- each player: `recipe_score` (number, visible: ally, starts 0): 2*first + 2*second + 2*min(first, second) for the two Recipe vegetables; revealed at game end
- the table: `round` (number, visible: public, starts 0): rounds started so far
- the table: `card` (text, visible: public, starts ''): the scoring card drawn this round
- parameters (each must be an attribute holding this value, never a number buried in a step): player_count = 3, rounds = 12, card_types_count = 6, fan_multiplier = 2, rainbow_multiplier = 3, big_bowl_multiplier = 1, balance_value = 6, balance_min_each = 1, balance_max_spread = 1, sole_vegetable_gain = 2, pair_vegetable_gain = 1, triple_vegetable_gain = 0, recipe_first_weight = 2, recipe_second_weight = 2, recipe_min_weight = 2, start_vegetables = 0, start_points = 0
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
```json
{
  "schema": 1,
  "meta": {
    "id": "point_salad_secret_recipes",
    "name": "Point Salad: Secret Recipes",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Three secret two-vegetable Recipes, 12 rounds of talk and simultaneous picks; collisions shrink gains, and points plus recipe score wins."
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
        "key": "recipe",
        "visible": "ally",
        "type": "text",
        "initial": "",
        "values": [
          "",
          "TL",
          "LC",
          "CT"
        ]
      },
      {
        "key": "pick",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "card_value",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "recipe_score",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "message",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "gain",
        "visible": "ally",
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
        "key": "card",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "card_types",
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
        "key": "drawn",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "n_card",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "n_t",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "n_l",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "n_c",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "player_count",
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
        "key": "card_types_count",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "fan_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "rainbow_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "big_bowl_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "balance_value",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "balance_min_each",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "balance_max_spread",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "sole_vegetable_gain",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "pair_vegetable_gain",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "triple_vegetable_gain",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "recipe_first_weight",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "recipe_second_weight",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "recipe_min_weight",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "start_vegetables",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "start_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "starting baskets",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "t",
            "value": {
              "calc": "start_vegetables"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "l",
            "value": {
              "calc": "start_vegetables"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "c",
            "value": {
              "calc": "start_vegetables"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "points",
            "value": {
              "calc": "start_points"
            }
          }
        }
      ],
      "text": "Every player starts with t={start_vegetables}, l={start_vegetables}, c={start_vegetables} and points={start_points}."
    },
    {
      "use": "update",
      "label": "deal the recipes",
      "do": [
        {
          "set": {
            "key": "drawn",
            "value": {
              "calc": "recipe_deck[int(uniform(0, len(recipe_deck)))]"
            }
          }
        },
        {
          "set": {
            "player": 1,
            "key": "recipe",
            "value": {
              "calc": "drawn"
            }
          }
        },
        {
          "remove": {
            "key": "recipe_deck",
            "value": {
              "calc": "drawn"
            }
          }
        },
        {
          "set": {
            "key": "drawn",
            "value": {
              "calc": "recipe_deck[int(uniform(0, len(recipe_deck)))]"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "recipe",
            "value": {
              "calc": "drawn"
            }
          }
        },
        {
          "remove": {
            "key": "recipe_deck",
            "value": {
              "calc": "drawn"
            }
          }
        },
        {
          "set": {
            "key": "drawn",
            "value": {
              "calc": "recipe_deck[int(uniform(0, len(recipe_deck)))]"
            }
          }
        },
        {
          "set": {
            "player": 3,
            "key": "recipe",
            "value": {
              "calc": "drawn"
            }
          }
        },
        {
          "remove": {
            "key": "recipe_deck",
            "value": {
              "calc": "drawn"
            }
          }
        }
      ],
      "text": "The three Recipe tiles have been dealt, one to each player, face down."
    },
    {
      "use": "sync",
      "label": "your recipe",
      "mode": "self",
      "to": "all",
      "text": "Your secret Recipe and starting basket:"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "draw",
      "label": "draw the card",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "key": "card",
            "value": {
              "calc": "card_types[int(uniform(0, card_types_count))]"
            }
          }
        }
      ],
      "text": "Round {round} of {rounds}: the scoring card is {card}."
    },
    {
      "use": "update",
      "phase": "draw",
      "label": "value the card",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "card_value",
            "value": {
              "calc": "fan_multiplier * you.t if card == 'Tomato Fan' else (fan_multiplier * you.l if card == 'Lettuce Fan' else (fan_multiplier * you.c if card == 'Carrot Fan' else (rainbow_multiplier * min(you.t, you.l, you.c) if card == 'Rainbow' else (big_bowl_multiplier * (you.t + you.l + you.c) if card == 'Big Bowl' else (balance_value if (min(you.t, you.l, you.c) >= balance_min_each and max(you.t, you.l, you.c) - min(you.t, you.l, you.c) <= balance_max_spread) else 0)))))"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "message",
            "value": ""
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
            "key": "gain",
            "value": 0
          }
        }
      ]
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
      "text": "The card this round is {card}. Write one short message to the table. Everyone writes at the same time; messages bind no one."
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
      "text": "Pick exactly one: Tomato, Lettuce, Carrot or Card (the {card}). Everyone picks at the same moment; nobody sees a pick until all are in."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "count the picks",
      "do": [
        {
          "set": {
            "key": "n_card",
            "value": {
              "calc": "count(p.pick == 'Card' for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "n_t",
            "value": {
              "calc": "count(p.pick == 'Tomato' for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "n_l",
            "value": {
              "calc": "count(p.pick == 'Lettuce' for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "n_c",
            "value": {
              "calc": "count(p.pick == 'Carrot' for p in players)"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "resolve the card",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.pick == 'Card'"
            },
            "key": "gain",
            "value": {
              "calc": "you.card_value if n_card == 1 else 0"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.pick == 'Card' and n_card == 1"
            },
            "key": "points",
            "value": {
              "calc": "you.gain"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "resolve the vegetables",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.pick == 'Tomato'"
            },
            "key": "gain",
            "value": {
              "calc": "sole_vegetable_gain if n_t == 1 else (pair_vegetable_gain if n_t == 2 else triple_vegetable_gain)"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.pick == 'Lettuce'"
            },
            "key": "gain",
            "value": {
              "calc": "sole_vegetable_gain if n_l == 1 else (pair_vegetable_gain if n_l == 2 else triple_vegetable_gain)"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.pick == 'Carrot'"
            },
            "key": "gain",
            "value": {
              "calc": "sole_vegetable_gain if n_c == 1 else (pair_vegetable_gain if n_c == 2 else triple_vegetable_gain)"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.pick == 'Tomato'"
            },
            "key": "t",
            "value": {
              "calc": "you.gain"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.pick == 'Lettuce'"
            },
            "key": "l",
            "value": {
              "calc": "you.gain"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.pick == 'Carrot'"
            },
            "key": "c",
            "value": {
              "calc": "you.gain"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "recipe scores",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "recipe_score",
            "value": {
              "calc": "(recipe_first_weight * you.t + recipe_second_weight * you.l + recipe_min_weight * min(you.t, you.l)) if you.recipe == 'TL' else ((recipe_first_weight * you.l + recipe_second_weight * you.c + recipe_min_weight * min(you.l, you.c)) if you.recipe == 'LC' else (recipe_first_weight * you.c + recipe_second_weight * you.t + recipe_min_weight * min(you.c, you.t)))"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "announce",
      "label": "round results",
      "to": "all",
      "text": "Round {round} results (card {card}; Card pickers {n_card}, Tomato {n_t}, Lettuce {n_l}, Carrot {n_c}). Seat 1 picked {players[0].pick} and received {players[0].gain}; now t={players[0].t}, l={players[0].l}, c={players[0].c}, points={players[0].points}. Seat 2 picked {players[1].pick} and received {players[1].gain}; now t={players[1].t}, l={players[1].l}, c={players[1].c}, points={players[1].points}. Seat 3 picked {players[2].pick} and received {players[2].gain}; now t={players[2].t}, l={players[2].l}, c={players[2].c}, points={players[2].points}."
    },
    {
      "use": "update",
      "phase": "announce",
      "label": "reveal the recipes",
      "when": {
        "calc": "round >= rounds"
      },
      "do": [
        {
          "disclose": {
            "attribute": "recipe",
            "of": 1,
            "to": "all",
            "text": "Seat {subject}'s Recipe was {value}."
          }
        },
        {
          "disclose": {
            "attribute": "recipe",
            "of": 2,
            "to": "all",
            "text": "Seat {subject}'s Recipe was {value}."
          }
        },
        {
          "disclose": {
            "attribute": "recipe",
            "of": 3,
            "to": "all",
            "text": "Seat {subject}'s Recipe was {value}."
          }
        },
        {
          "disclose": {
            "attribute": "recipe_score",
            "of": 1,
            "to": "all",
            "text": "Seat {subject}'s recipe score is {value}."
          }
        },
        {
          "disclose": {
            "attribute": "recipe_score",
            "of": 2,
            "to": "all",
            "text": "Seat {subject}'s recipe score is {value}."
          }
        },
        {
          "disclose": {
            "attribute": "recipe_score",
            "of": 3,
            "to": "all",
            "text": "Seat {subject}'s recipe score is {value}."
          }
        }
      ],
      "text": "Recipes revealed. Seat 1: {players[0].recipe}, recipe {players[0].recipe_score} + points {players[0].points}. Seat 2: {players[1].recipe}, recipe {players[1].recipe_score} + points {players[1].points}. Seat 3: {players[2].recipe}, recipe {players[2].recipe_score} + points {players[2].points}."
    },
    {
      "use": "check",
      "phase": "announce",
      "label": "after round 12",
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
        "recipe",
        "recipe_score"
      ],
      "text": "Winner: {result}. Final totals (points + recipe): Seat 1 {players[0].points} + {players[0].recipe_score}, Seat 2 {players[1].points} + {players[1].recipe_score}, Seat 3 {players[2].points} + {players[2].recipe_score}."
    }
  },
  "limits": {
    "rounds": 12,
    "rounds_max": 12,
    "actions_max": 1000,
    "deadline_s": 120
  },
  "rules": "Point Salad: Secret Recipes, for {player_count} players. Vegetables: Tomato (t), Lettuce (l), Carrot (c).\n\nSETUP: There are 3 Recipe tiles: TL (tomato and lettuce), LC (lettuce and carrot) and CT (carrot and tomato). They are shuffled and one is dealt to each player, so all three are used. Each player sees only their own Recipe. A Recipe never changes for the rest of the game. Every player starts with t={start_vegetables}, l={start_vegetables}, c={start_vegetables} and points={start_points}. Baskets (t, l, c) and points are public at all times. Recipes are secret until game end.\n\nEACH ROUND ({rounds} rounds):\n1. Draw the card: one scoring card type is drawn at random, with replacement, equally likely from these {card_types_count}, and announced to everyone. Tomato Fan: worth {fan_multiplier} x t. Lettuce Fan: worth {fan_multiplier} x l. Carrot Fan: worth {fan_multiplier} x c. Rainbow: worth {rainbow_multiplier} x min(t, l, c). Big Bowl: worth {big_bowl_multiplier} x (t + l + c). Balance: worth {balance_value} if t, l and c are each at least {balance_min_each} and max(t,l,c) - min(t,l,c) is at most {balance_max_spread}; otherwise 0.\n2. Talk: every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Messages bind no one.\n3. Pick: every player at the same moment chooses exactly one of Tomato, Lettuce, Carrot, Card.\n4. Resolve the Card: if exactly one player chose Card, that player gains points equal to the drawn card's value, computed from their basket as it stood at the start of this round. If zero players, or two or more players, chose Card, nobody gains anything from it: the card is discarded and colliding players receive nothing this round.\n5. Resolve vegetables, separately for each vegetable: if exactly 1 player chose it, that player adds {sole_vegetable_gain} of it to their basket; if exactly 2 players chose it, each adds {pair_vegetable_gain}; if all 3 chose it, nobody gets any ({triple_vegetable_gain}).\n6. Announce: everyone's pick, what each received, and all baskets and points.\n7. After {rounds} rounds the game ends.\n\nEND: Each player's Recipe is revealed and scored. With first and second as that player's counts of the Recipe's two vegetables: recipe_score = {recipe_first_weight} x first + {recipe_second_weight} x second + {recipe_min_weight} x min(first, second). The third vegetable scores nothing. TL uses t and l; LC uses l and c; CT uses c and t. Examples: CT with c=2, t=2 scores 12; CT with c=3, t=2 scores 14; TL with t=4, l=1 scores 12; LC with l=0, c=6 scores 12. final_total = points + recipe_score. The highest final_total wins; for example points 10 with recipe 12 (22) beats points 0 with recipe 14 (14). If two or three players tie for the highest final_total, the game is a draw among them (they share the win).\n\nCard example: a player starting a round with t=3, l=1, c=2 who is the sole Card claimant scores Tomato Fan 6, Lettuce Fan 2, Carrot Fan 4, Rainbow 3, Big Bowl 6, Balance 0 (spread 2 > 1)."
}
```

Why it was refused: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (message, pick, message, pick) in `your_recipe`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "point_salad_secret_recipes",
    "name": "Point Salad: Secret Recipes",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Three secret two-vegetable Recipes, 12 rounds of talk and simultaneous picks; collisions shrink gains, and points plus recipe score wins."
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
        "key": "recipe",
        "visible": "ally",
        "type": "text",
        "initial": "",
        "values": [
          "",
          "TL",
          "LC",
          "CT"
        ]
      },
      {
        "key": "pick",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "card_value",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "recipe_score",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "message",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "gain",
        "visible": "ally",
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
        "key": "card",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "card_types",
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
        "key": "drawn",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "n_card",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "n_t",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "n_l",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "n_c",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "player_count",
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
        "key": "card_types_count",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "fan_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "rainbow_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "big_bowl_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "balance_value",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "balance_min_each",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "balance_max_spread",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "sole_vegetable_gain",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "pair_vegetable_gain",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "triple_vegetable_gain",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "recipe_first_weight",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "recipe_second_weight",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "recipe_min_weight",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "start_vegetables",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "start_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "starting baskets",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "t",
            "value": {
              "calc": "start_vegetables"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "l",
            "value": {
              "calc": "start_vegetables"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "c",
            "value": {
              "calc": "start_vegetables"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "points",
            "value": {
              "calc": "start_points"
            }
          }
        }
      ],
      "text": "Every player starts with t={start_vegetables}, l={start_vegetables}, c={start_vegetables} and points={start_points}."
    },
    {
      "use": "update",
      "label": "deal the recipes",
      "do": [
        {
          "set": {
            "key": "drawn",
            "value": {
              "calc": "recipe_deck[int(uniform(0, len(recipe_deck)))]"
            }
          }
        },
        {
          "set": {
            "player": 1,
            "key": "recipe",
            "value": {
              "calc": "drawn"
            }
          }
        },
        {
          "remove": {
            "key": "recipe_deck",
            "value": {
              "calc": "drawn"
            }
          }
        },
        {
          "set": {
            "key": "drawn",
            "value": {
              "calc": "recipe_deck[int(uniform(0, len(recipe_deck)))]"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "recipe",
            "value": {
              "calc": "drawn"
            }
          }
        },
        {
          "remove": {
            "key": "recipe_deck",
            "value": {
              "calc": "drawn"
            }
          }
        },
        {
          "set": {
            "key": "drawn",
            "value": {
              "calc": "recipe_deck[int(uniform(0, len(recipe_deck)))]"
            }
          }
        },
        {
          "set": {
            "player": 3,
            "key": "recipe",
            "value": {
              "calc": "drawn"
            }
          }
        },
        {
          "remove": {
            "key": "recipe_deck",
            "value": {
              "calc": "drawn"
            }
          }
        }
      ],
      "text": "The three Recipe tiles have been dealt, one to each player, face down."
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
      "text": "Your secret Recipe and starting basket:"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "draw",
      "label": "draw the card",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "key": "card",
            "value": {
              "calc": "card_types[int(uniform(0, card_types_count))]"
            }
          }
        }
      ],
      "text": "Round {round} of {rounds}: the scoring card is {card}."
    },
    {
      "use": "update",
      "phase": "draw",
      "label": "value the card",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "card_value",
            "value": {
              "calc": "fan_multiplier * you.t if card == 'Tomato Fan' else (fan_multiplier * you.l if card == 'Lettuce Fan' else (fan_multiplier * you.c if card == 'Carrot Fan' else (rainbow_multiplier * min(you.t, you.l, you.c) if card == 'Rainbow' else (big_bowl_multiplier * (you.t + you.l + you.c) if card == 'Big Bowl' else (balance_value if (min(you.t, you.l, you.c) >= balance_min_each and max(you.t, you.l, you.c) - min(you.t, you.l, you.c) <= balance_max_spread) else 0)))))"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "message",
            "value": ""
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
            "key": "gain",
            "value": 0
          }
        }
      ]
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
      "text": "The card this round is {card}. Write one short message to the table. Everyone writes at the same time; messages bind no one."
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
      "text": "Pick exactly one: Tomato, Lettuce, Carrot or Card (the {card}). Everyone picks at the same moment; nobody sees a pick until all are in."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "count the picks",
      "do": [
        {
          "set": {
            "key": "n_card",
            "value": {
              "calc": "count(p.pick == 'Card' for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "n_t",
            "value": {
              "calc": "count(p.pick == 'Tomato' for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "n_l",
            "value": {
              "calc": "count(p.pick == 'Lettuce' for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "n_c",
            "value": {
              "calc": "count(p.pick == 'Carrot' for p in players)"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "resolve the card",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.pick == 'Card'"
            },
            "key": "gain",
            "value": {
              "calc": "you.card_value if n_card == 1 else 0"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.pick == 'Card' and n_card == 1"
            },
            "key": "points",
            "value": {
              "calc": "you.gain"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "resolve the vegetables",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.pick == 'Tomato'"
            },
            "key": "gain",
            "value": {
              "calc": "sole_vegetable_gain if n_t == 1 else (pair_vegetable_gain if n_t == 2 else triple_vegetable_gain)"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.pick == 'Lettuce'"
            },
            "key": "gain",
            "value": {
              "calc": "sole_vegetable_gain if n_l == 1 else (pair_vegetable_gain if n_l == 2 else triple_vegetable_gain)"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.pick == 'Carrot'"
            },
            "key": "gain",
            "value": {
              "calc": "sole_vegetable_gain if n_c == 1 else (pair_vegetable_gain if n_c == 2 else triple_vegetable_gain)"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.pick == 'Tomato'"
            },
            "key": "t",
            "value": {
              "calc": "you.gain"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.pick == 'Lettuce'"
            },
            "key": "l",
            "value": {
              "calc": "you.gain"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.pick == 'Carrot'"
            },
            "key": "c",
            "value": {
              "calc": "you.gain"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "recipe scores",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "recipe_score",
            "value": {
              "calc": "(recipe_first_weight * you.t + recipe_second_weight * you.l + recipe_min_weight * min(you.t, you.l)) if you.recipe == 'TL' else ((recipe_first_weight * you.l + recipe_second_weight * you.c + recipe_min_weight * min(you.l, you.c)) if you.recipe == 'LC' else (recipe_first_weight * you.c + recipe_second_weight * you.t + recipe_min_weight * min(you.c, you.t)))"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "announce",
      "label": "round results",
      "to": "all",
      "text": "Round {round} results (card {card}; Card pickers {n_card}, Tomato {n_t}, Lettuce {n_l}, Carrot {n_c}). Seat 1 picked {players[0].pick} and received {players[0].gain}; now t={players[0].t}, l={players[0].l}, c={players[0].c}, points={players[0].points}. Seat 2 picked {players[1].pick} and received {players[1].gain}; now t={players[1].t}, l={players[1].l}, c={players[1].c}, points={players[1].points}. Seat 3 picked {players[2].pick} and received {players[2].gain}; now t={players[2].t}, l={players[2].l}, c={players[2].c}, points={players[2].points}."
    },
    {
      "use": "update",
      "phase": "announce",
      "label": "reveal the recipes",
      "when": {
        "calc": "round >= rounds"
      },
      "do": [
        {
          "disclose": {
            "attribute": "recipe",
            "of": 1,
            "to": "all",
            "text": "Seat {subject}'s Recipe was {value}."
          }
        },
        {
          "disclose": {
            "attribute": "recipe",
            "of": 2,
            "to": "all",
            "text": "Seat {subject}'s Recipe was {value}."
          }
        },
        {
          "disclose": {
            "attribute": "recipe",
            "of": 3,
            "to": "all",
            "text": "Seat {subject}'s Recipe was {value}."
          }
        },
        {
          "disclose": {
            "attribute": "recipe_score",
            "of": 1,
            "to": "all",
            "text": "Seat {subject}'s recipe score is {value}."
          }
        },
        {
          "disclose": {
            "attribute": "recipe_score",
            "of": 2,
            "to": "all",
            "text": "Seat {subject}'s recipe score is {value}."
          }
        },
        {
          "disclose": {
            "attribute": "recipe_score",
            "of": 3,
            "to": "all",
            "text": "Seat {subject}'s recipe score is {value}."
          }
        }
      ],
      "text": "Recipes revealed. Seat 1: {players[0].recipe}, recipe {players[0].recipe_score} + points {players[0].points}. Seat 2: {players[1].recipe}, recipe {players[1].recipe_score} + points {players[1].points}. Seat 3: {players[2].recipe}, recipe {players[2].recipe_score} + points {players[2].points}."
    },
    {
      "use": "check",
      "phase": "announce",
      "label": "after round 12",
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
        "recipe",
        "recipe_score"
      ],
      "text": "Winner: {result}. Final totals (points + recipe): Seat 1 {players[0].points} + {players[0].recipe_score}, Seat 2 {players[1].points} + {players[1].recipe_score}, Seat 3 {players[2].points} + {players[2].recipe_score}."
    }
  },
  "limits": {
    "rounds": 12,
    "rounds_max": 12,
    "actions_max": 1000,
    "deadline_s": 120
  },
  "rules": "Point Salad: Secret Recipes, for {player_count} players. Vegetables: Tomato (t), Lettuce (l), Carrot (c).\n\nSETUP: There are 3 Recipe tiles: TL (tomato and lettuce), LC (lettuce and carrot) and CT (carrot and tomato). They are shuffled and one is dealt to each player, so all three are used. Each player sees only their own Recipe. A Recipe never changes for the rest of the game. Every player starts with t={start_vegetables}, l={start_vegetables}, c={start_vegetables} and points={start_points}. Baskets (t, l, c) and points are public at all times. Recipes are secret until game end.\n\nEACH ROUND ({rounds} rounds):\n1. Draw the card: one scoring card type is drawn at random, with replacement, equally likely from these {card_types_count}, and announced to everyone. Tomato Fan: worth {fan_multiplier} x t. Lettuce Fan: worth {fan_multiplier} x l. Carrot Fan: worth {fan_multiplier} x c. Rainbow: worth {rainbow_multiplier} x min(t, l, c). Big Bowl: worth {big_bowl_multiplier} x (t + l + c). Balance: worth {balance_value} if t, l and c are each at least {balance_min_each} and max(t,l,c) - min(t,l,c) is at most {balance_max_spread}; otherwise 0.\n2. Talk: every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Messages bind no one.\n3. Pick: every player at the same moment chooses exactly one of Tomato, Lettuce, Carrot, Card.\n4. Resolve the Card: if exactly one player chose Card, that player gains points equal to the drawn card's value, computed from their basket as it stood at the start of this round. If zero players, or two or more players, chose Card, nobody gains anything from it: the card is discarded and colliding players receive nothing this round.\n5. Resolve vegetables, separately for each vegetable: if exactly 1 player chose it, that player adds {sole_vegetable_gain} of it to their basket; if exactly 2 players chose it, each adds {pair_vegetable_gain}; if all 3 chose it, nobody gets any ({triple_vegetable_gain}).\n6. Announce: everyone's pick, what each received, and all baskets and points.\n7. After {rounds} rounds the game ends.\n\nEND: Each player's Recipe is revealed and scored. With first and second as that player's counts of the Recipe's two vegetables: recipe_score = {recipe_first_weight} x first + {recipe_second_weight} x second + {recipe_min_weight} x min(first, second). The third vegetable scores nothing. TL uses t and l; LC uses l and c; CT uses c and t. Examples: CT with c=2, t=2 scores 12; CT with c=3, t=2 scores 14; TL with t=4, l=1 scores 12; LC with l=0, c=6 scores 12. final_total = points + recipe_score. The highest final_total wins; for example points 10 with recipe 12 (22) beats points 0 with recipe 14 (14). If two or three players tie for the highest final_total, the game is a draw among them (they share the win).\n\nCard example: a player starting a round with t=3, l=1, c=2 who is the sole Card claimant scores Tomato Fan 6, Lettuce Fan 2, Carrot Fan 4, Rainbow 3, Big Bowl 6, Balance 0 (spread 2 > 1)."
}
```
````
