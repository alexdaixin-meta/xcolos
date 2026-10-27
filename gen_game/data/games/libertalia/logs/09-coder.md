# 09 coder

- time: 2026-10-27T22:11:11+00:00 (46.2s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 1f476c9d252bfb31, reply sha256 d27a35e38b212de4

## Sent

````
# Task: write the XColos game file for "Libertalia: Shared Hand"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

SETUP: 3 players, each with a score of 0 doubloons. The game has 2 campaigns of 5 days (10 rounds). At the start of each campaign every player receives the same 7-card hand: ranks 1 to 7, one card of each rank. Cards played are removed from the owner's hand. The 2 cards left after day 5 are discarded unused, and a fresh full hand is dealt for campaign 2. Which cards each player has played is public once revealed.

CHARACTERS:
- Rank 1, Cabin Boy: takes no booty. Gains 3 doubloons.
- Rank 2, Gunner: takes booty normally. Every other non-clashed player who played rank 6 or 7 loses 3 doubloons.
- Rank 3, Quartermaster: takes booty normally. Gains 1 doubloon for each other non-clashed player who played a higher rank.
- Rank 4, Bosun: takes booty normally. If the token taken is negative, it counts as 0.
- Rank 5, Merchant: takes booty normally. Gains 2 extra doubloons if the token taken is worth 3 or more.
- Rank 6, Captain: takes booty normally. No ability.
- Rank 7, Admiral: takes booty normally. Pays a wage: loses 2 doubloons.

BOOTY ROWS: each day one row is drawn at random, each equally likely, with replacement, from: A [5,3,1], B [5,1,-3], C [3,3,1], D [5,3,-3], E [3,1,-3], F [5,5,-3]. The values are the tokens, listed best to worst.

EACH DAY (ROUND):
1. Draw the booty row and announce it to all players.
2. Talk: everyone writes one short message at the same time. All messages are then shown to everyone. Messages are not binding.
3. All players secretly and simultaneously choose one card from their hand.
4. Reveal all cards.
5. Clash: if two or three players played the same rank, all of those players are clashed. They take no booty, their abilities do not fire, and their cards are still spent.
6. Booty: non-clashed players other than the Cabin Boy are ordered by rank, highest first. The first takes the best token, the second the next, and so on. Tokens left over are discarded.
7. Abilities of non-clashed characters resolve at the same time, as listed above. Gunner and Quartermaster count only non-clashed players.
8. Each player adds their token value plus or minus their ability effects to their score.
9. After day 5, discard leftover cards and deal fresh hands. After day 10, the game ends.

The Cabin Boy's +3 still applies when other players take booty. Scores can go negative.

How the winner is decided: After 10 rounds, the player with the highest doubloon total wins. If two or more players share the highest total, they draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Libertalia: Shared Hand (3 to 3 players, best with 3)

Three pirates play identical 7-card hands over 2 campaigns of 5 days, revealing one character a day at the same time to share out booty tokens and trigger abilities, while avoiding clashes on the same rank.

STATE (every item below must exist in the file):
  - each player: score (number, starts 0); everyone sees it. doubloons; may go negative
  - each player: hand (list, starts [1, 2, 3, 4, 5, 6, 7]); everyone sees it. ranks still in hand this campaign; public because every hand starts identical and played cards are revealed
  - each player: card (number, starts 0); everyone sees it. rank played today, chosen secretly and revealed once all have chosen
  - each player: clashed (bool, starts False); everyone sees it. true if another player played the same rank today
  - each player: token (number, starts 0); everyone sees it. booty token value taken today, after the Bosun floor
  - each player: ability (number, starts 0); everyone sees it. net ability effect on this player today, including the Gunner penalty received
  - each player: message (text, starts ''); everyone sees it. today's talk message
  - the table: day (number, starts 0); everyone sees it. current day, 1 to 10
  - the table: booty_rows (list, starts [[5, 3, 1], [5, 1, -3], [3, 3, 1], [5, 3, -3], [3, 1, -3], [5, 5, -3]]); everyone sees it. rows A to F; one is drawn each day with replacement
  - the table: booty_row (list, starts []); everyone sees it. today's three tokens, best to worst
  - parameters, each kept as a table attribute: players = 3, campaigns = 2, days_per_campaign = 5, total_rounds = 10, starting_score = 0, hand_size = 7, lowest_rank = 1, highest_rank = 7, cards_discarded_per_campaign = 2, cabin_boy_rank = 1, cabin_boy_gain = 3, gunner_rank = 2, gunner_penalty = 3, gunner_target_min_rank = 6, quartermaster_rank = 3, quartermaster_bonus_per_higher = 1, bosun_rank = 4, bosun_floor = 0, merchant_rank = 5, merchant_bonus = 2, merchant_threshold = 3, captain_rank = 6, admiral_rank = 7, admiral_wage = 2, row_count = 6, tokens_per_row = 3, row_A_1 = 5, row_A_2 = 3, row_A_3 = 1, row_B_1 = 5, row_B_2 = 1, row_B_3 = -3, row_C_1 = 3, row_C_2 = 3, row_C_3 = 1, row_D_1 = 5, row_D_2 = 3, row_D_3 = -3, row_E_1 = 3, row_E_2 = 1, row_E_3 = -3, row_F_1 = 5, row_F_2 = 5, row_F_3 = -3

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seat 3 players, each with score 0.
  2. Set day to 0.
  3. Give every player hand = [1,2,3,4,5,6,7] for campaign 1.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: day += 1; if day == 6, every player's hand is set to [1,2,3,4,5,6,7], which discards the 2 leftover cards and deals campaign 2; every player's card = 0, clashed = false, token = 0, ability = 0
  2. [update] all players. What happens: booty_row = one entry of booty_rows picked at random, each equally likely, without removing it (with replacement); announce booty_row to all
  3. [poll] all players answers: short text. What happens: message = the text; then broadcast {"to": "all", "text": "Seat {seat} says: {value}"}
  4. [poll] all players answers: one rank from own hand. What happens: card = the chosen rank; no answer is seen until all are in
  5. [update] all players. What happens: remove card from hand; reveal every player's card to all
  6. [update] all players. What happens: clashed = (number of other players whose card == you.card) >= 1
  7. [update] all players. What happens: if not clashed and card >= 2: pos = 1 + number of other players with not clashed and card >= 2 and card > you.card; token = booty_row[pos]; if card == 4, token = max(token, 0); otherwise token = 0
  8. [update] all players. What happens: ability = 0; if not clashed and card == 1: ability += 3; if not clashed and card == 3: ability += 1 * (number of other non-clashed players with card > 3); if not clashed and card == 5 and token >= 3: ability += 2; if not clashed and card == 7: ability -= 2; if not clashed and card >= 6 and some other non-clashed player has card == 2: ability -= 3
  9. [update] all players. What happens: score += token + ability; announce each player's card, clashed, token, ability and score
  10. [check] all players. What happens: end the game if day == 10, otherwise continue

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. At setup, each of the 3 players has score 0 and hand [1,2,3,4,5,6,7].
  R2. Each day, booty_row is one of A [5,3,1], B [5,1,-3], C [3,3,1], D [5,3,-3], E [3,1,-3], F [5,5,-3], drawn with equal chance and with replacement, and announced before any choice.
  R3. Each day, every player first sends one short message at the same time, and all messages are shown to everyone.
  R4. Each day, every player secretly and simultaneously plays one rank from their hand, and that rank is removed from their hand.
  R5. When two or three players play the same rank, then all of them are clashed: token 0, no ability, and the card is still removed.
  R6. When a non-clashed player plays rank 2 to 7, then they take booty_row[1 + number of other non-clashed players with rank 2 to 7 and a higher rank]; for example, the higher of two such players takes the best token and the other takes the second.
  R7. When a non-clashed player plays rank 1 (Cabin Boy), then they take no token and gain 3.
  R8. When a non-clashed player plays rank 2 (Gunner), then every other non-clashed player who played rank 6 or 7 loses 3.
  R9. When a non-clashed player plays rank 3 (Quartermaster), then they gain 1 for each other non-clashed player who played a rank above 3.
  R10. When a non-clashed player plays rank 4 (Bosun) and takes a negative token, then the token counts as 0.
  R11. When a non-clashed player plays rank 5 (Merchant) and takes a token worth 3 or more, then they gain 2 extra.
  R12. When a non-clashed player plays rank 6 (Captain), then they take booty normally and have no ability.
  R13. When a non-clashed player plays rank 7 (Admiral), then they lose 2.
  R14. Each day, each player's score changes by token + ability, and a score may go negative.
  R15. When day 6 begins, every player's 2 leftover cards are discarded and their hand is reset to [1,2,3,4,5,6,7].
  R16. When day 10 ends, the game ends, and the highest score wins, with tied leaders sharing the win.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - talk message | asked: all players | options: any short text
  - which card to play | asked: all players | options: each seat: exactly the ranks still in its own hand (7 options on days 1 and 6, down to 3 options on days 5 and 10)

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: day == 10
  - each player's standing: you.score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Highest doubloon total after 10 days wins; players tied at the top share the win (a draw).
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

- each player: `score` (number, visible: public, starts 0): doubloons; may go negative
- each player: `card` (number, visible: public, starts 0): rank played today, chosen secretly and revealed once all have chosen
- each player: `clashed` (bool, visible: public, starts False): true if another player played the same rank today
- the table: `day` (number, visible: public, starts 0): current day, 1 to 10
- the table: `booty_row` (list, visible: public, starts []): today's three tokens, best to worst
- parameters (each must be an attribute holding this value, never a number buried in a step): players = 3, campaigns = 2, days_per_campaign = 5, total_rounds = 10, starting_score = 0, hand_size = 7, lowest_rank = 1, highest_rank = 7, cards_discarded_per_campaign = 2, cabin_boy_rank = 1, cabin_boy_gain = 3, gunner_rank = 2, gunner_penalty = 3, gunner_target_min_rank = 6, quartermaster_rank = 3, quartermaster_bonus_per_higher = 1, bosun_rank = 4, bosun_floor = 0, merchant_rank = 5, merchant_bonus = 2, merchant_threshold = 3, captain_rank = 6, admiral_rank = 7, admiral_wage = 2, row_count = 6, tokens_per_row = 3, row_A_1 = 5, row_A_2 = 3, row_A_3 = 1, row_B_1 = 5, row_B_2 = 1, row_B_3 = -3, row_C_1 = 3, row_C_2 = 3, row_C_3 = 1, row_D_1 = 5, row_D_2 = 3, row_D_3 = -3, row_E_1 = 3, row_E_2 = 1, row_E_3 = -3, row_F_1 = 5, row_F_2 = 5, row_F_3 = -3
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


YOUR PREVIOUS GAME FILE WAS REFUSED. Here it is:
```json
{
  "schema": 1,
  "meta": {
    "id": "libertalia_shared_hand",
    "name": "Libertalia: Shared Hand",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Three pirates, identical 7-card hands, two campaigns of five days: reveal one character a day, share the booty, avoid clashes."
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
        "visible": "public",
        "type": "list",
        "initial": [1, 2, 3, 4, 5, 6, 7]
      },
      {
        "key": "card",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "clashed",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "token",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "ability",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "message",
        "visible": "public",
        "type": "text",
        "initial": "(nothing said yet)"
      },
      {
        "key": "choice",
        "visible": "ally",
        "type": "text",
        "initial": "0"
      }
    ],
    "game": [
      {"key": "day", "visible": "public", "type": "number", "initial": 0},
      {"key": "booty_rows", "visible": "public", "type": "list", "initial": [[5, 3, 1], [5, 1, -3], [3, 3, 1], [5, 3, -3], [3, 1, -3], [5, 5, -3]]},
      {"key": "booty_row", "visible": "public", "type": "list", "initial": []},
      {"key": "full_hand", "visible": "none", "type": "list", "initial": [1, 2, 3, 4, 5, 6, 7]},
      {"key": "players", "visible": "public", "type": "number", "initial": 3},
      {"key": "campaigns", "visible": "public", "type": "number", "initial": 2},
      {"key": "days_per_campaign", "visible": "public", "type": "number", "initial": 5},
      {"key": "total_rounds", "visible": "public", "type": "number", "initial": 10},
      {"key": "starting_score", "visible": "public", "type": "number", "initial": 0},
      {"key": "hand_size", "visible": "public", "type": "number", "initial": 7},
      {"key": "lowest_rank", "visible": "public", "type": "number", "initial": 1},
      {"key": "highest_rank", "visible": "public", "type": "number", "initial": 7},
      {"key": "cards_discarded_per_campaign", "visible": "public", "type": "number", "initial": 2},
      {"key": "cabin_boy_rank", "visible": "public", "type": "number", "initial": 1},
      {"key": "cabin_boy_gain", "visible": "public", "type": "number", "initial": 3},
      {"key": "gunner_rank", "visible": "public", "type": "number", "initial": 2},
      {"key": "gunner_penalty", "visible": "public", "type": "number", "initial": 3},
      {"key": "gunner_target_min_rank", "visible": "public", "type": "number", "initial": 6},
      {"key": "quartermaster_rank", "visible": "public", "type": "number", "initial": 3},
      {"key": "quartermaster_bonus_per_higher", "visible": "public", "type": "number", "initial": 1},
      {"key": "bosun_rank", "visible": "public", "type": "number", "initial": 4},
      {"key": "bosun_floor", "visible": "public", "type": "number", "initial": 0},
      {"key": "merchant_rank", "visible": "public", "type": "number", "initial": 5},
      {"key": "merchant_bonus", "visible": "public", "type": "number", "initial": 2},
      {"key": "merchant_threshold", "visible": "public", "type": "number", "initial": 3},
      {"key": "captain_rank", "visible": "public", "type": "number", "initial": 6},
      {"key": "admiral_rank", "visible": "public", "type": "number", "initial": 7},
      {"key": "admiral_wage", "visible": "public", "type": "number", "initial": 2},
      {"key": "row_count", "visible": "public", "type": "number", "initial": 6},
      {"key": "tokens_per_row", "visible": "public", "type": "number", "initial": 3},
      {"key": "row_A_1", "visible": "public", "type": "number", "initial": 5},
      {"key": "row_A_2", "visible": "public", "type": "number", "initial": 3},
      {"key": "row_A_3", "visible": "public", "type": "number", "initial": 1},
      {"key": "row_B_1", "visible": "public", "type": "number", "initial": 5},
      {"key": "row_B_2", "visible": "public", "type": "number", "initial": 1},
      {"key": "row_B_3", "visible": "public", "type": "number", "initial": -3},
      {"key": "row_C_1", "visible": "public", "type": "number", "initial": 3},
      {"key": "row_C_2", "visible": "public", "type": "number", "initial": 3},
      {"key": "row_C_3", "visible": "public", "type": "number", "initial": 1},
      {"key": "row_D_1", "visible": "public", "type": "number", "initial": 5},
      {"key": "row_D_2", "visible": "public", "type": "number", "initial": 3},
      {"key": "row_D_3", "visible": "public", "type": "number", "initial": -3},
      {"key": "row_E_1", "visible": "public", "type": "number", "initial": 3},
      {"key": "row_E_2", "visible": "public", "type": "number", "initial": 1},
      {"key": "row_E_3", "visible": "public", "type": "number", "initial": -3},
      {"key": "row_F_1", "visible": "public", "type": "number", "initial": 5},
      {"key": "row_F_2", "visible": "public", "type": "number", "initial": 5},
      {"key": "row_F_3", "visible": "public", "type": "number", "initial": -3}
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "seat the players",
      "do": [
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
      "label": "set the day",
      "do": [
        {
          "set": {
            "key": "day",
            "value": 0
          }
        },
        {
          "set": {
            "key": "booty_rows",
            "value": {
              "calc": "[[row_A_1, row_A_2, row_A_3], [row_B_1, row_B_2, row_B_3], [row_C_1, row_C_2, row_C_3], [row_D_1, row_D_2, row_D_3], [row_E_1, row_E_2, row_E_3], [row_F_1, row_F_2, row_F_3]]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "deal campaign 1",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "full_hand"
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
      "phase": "dawn",
      "label": "a new day",
      "do": [
        {
          "adjust": {
            "key": "day",
            "value": 1
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "full_hand"
            },
            "if": {
              "calc": "day == days_per_campaign + 1"
            },
            "text": "Campaign 2 begins: seat {player} discards the leftover cards and receives a fresh hand of ranks 1 to 7."
          }
        },
        {
          "set": {
            "players": "all",
            "key": "card",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "clashed",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "token",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "ability",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "choice",
            "value": "0"
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "dawn",
      "label": "draw the booty row",
      "do": [
        {
          "set": {
            "key": "booty_row",
            "value": {
              "calc": "booty_rows[min(int(uniform(0, row_count)), row_count - 1)]"
            }
          }
        }
      ],
      "text": "Day {day} of {total_rounds}. Today's booty row, best to worst: {booty_row}."
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
      "text": "Day {day}, booty row {booty_row}. Say one short thing to the table. Messages are not binding."
    },
    {
      "use": "poll",
      "phase": "play",
      "label": "play a card",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "store": "choice",
      "text": "Day {day}, booty row {booty_row}. Secretly choose one rank from your hand to play. Nobody sees any card until all are chosen."
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "reveal the cards",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "card",
            "value": {
              "calc": "int(you.choice)"
            }
          }
        },
        {
          "remove": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "you.card"
            }
          }
        }
      ],
      "text": "Cards revealed: seat 1 played {players[0].card}, seat 2 played {players[1].card}, seat 3 played {players[2].card}."
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "clashes",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "clashed",
            "value": {
              "calc": "count(p.card == you.card and p.seat != you.seat for p in players) >= 1"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "booty",
      "label": "share the booty",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "token",
            "value": {
              "calc": "((max(booty_row[count((not p.clashed) and p.card > cabin_boy_rank and p.card > you.card and p.seat != you.seat for p in players)], bosun_floor) if you.card == bosun_rank else booty_row[count((not p.clashed) and p.card > cabin_boy_rank and p.card > you.card and p.seat != you.seat for p in players)]) if ((not you.clashed) and you.card > cabin_boy_rank) else 0)"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "abilities",
      "label": "abilities",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "ability",
            "value": {
              "calc": "0 if you.clashed else ((cabin_boy_gain if you.card == cabin_boy_rank else 0) + (quartermaster_bonus_per_higher * count((not p.clashed) and p.card > quartermaster_rank and p.seat != you.seat for p in players) if you.card == quartermaster_rank else 0) + (merchant_bonus if (you.card == merchant_rank and you.token >= merchant_threshold) else 0) - (admiral_wage if you.card == admiral_rank else 0) - (gunner_penalty if (you.card >= gunner_target_min_rank and any((not p.clashed) and p.card == gunner_rank and p.seat != you.seat for p in players)) else 0))"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "score",
      "label": "score the day",
      "do": [
        {
          "adjust": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "you.token + you.ability"
            }
          }
        }
      ],
      "text": "Day {day} results. Seat 1: card {players[0].card}, clashed {players[0].clashed}, token {players[0].token}, ability {players[0].ability}, score {players[0].score}. Seat 2: card {players[1].card}, clashed {players[1].clashed}, token {players[1].token}, ability {players[1].ability}, score {players[1].score}. Seat 3: card {players[2].card}, clashed {players[2].clashed}, token {players[2].token}, ability {players[2].ability}, score {players[2].score}."
    },
    {
      "use": "check",
      "phase": "score",
      "label": "after day 10",
      "when": {
        "calc": "day >= total_rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "day >= total_rounds"
      },
      "rank_by": "you.score",
      "text": "Winner: {result}. Final scores: Seat 1 {players[0].score}, Seat 2 {players[1].score}, Seat 3 {players[2].score} doubloons."
    }
  },
  "limits": {
    "rounds": 10,
    "rounds_max": 10,
    "actions_max": 500,
    "deadline_s": 120
  },
  "rules": "Three pirates each start with {starting_score} doubloons. The game has {campaigns} campaigns of {days_per_campaign} days ({total_rounds} days in all). At the start of each campaign every player receives the same {hand_size}-card hand: ranks {lowest_rank} to {highest_rank}, one card of each rank. Cards played are removed from the owner's hand. The {cards_discarded_per_campaign} cards left after day {days_per_campaign} are discarded unused, and a fresh full hand is dealt for campaign 2. Which cards each player has played is public once revealed.\n\nCHARACTERS:\n- Rank {cabin_boy_rank}, Cabin Boy: takes no booty. Gains {cabin_boy_gain} doubloons.\n- Rank {gunner_rank}, Gunner: takes booty normally. Every other non-clashed player who played rank {gunner_target_min_rank} or 7 loses {gunner_penalty} doubloons.\n- Rank {quartermaster_rank}, Quartermaster: takes booty normally. Gains {quartermaster_bonus_per_higher} doubloon for each other non-clashed player who played a higher rank.\n- Rank {bosun_rank}, Bosun: takes booty normally. If the token taken is negative, it counts as {bosun_floor}; otherwise it counts at face value.\n- Rank {merchant_rank}, Merchant: takes booty normally. Gains {merchant_bonus} extra doubloons if the token taken is worth {merchant_threshold} or more; otherwise no extra.\n- Rank {captain_rank}, Captain: takes booty normally. No ability.\n- Rank {admiral_rank}, Admiral: takes booty normally. Pays a wage: loses {admiral_wage} doubloons.\n\nBOOTY ROWS: each day one row is drawn at random, each of the {row_count} equally likely, with replacement, from: A [{row_A_1},{row_A_2},{row_A_3}], B [{row_B_1},{row_B_2},{row_B_3}], C [{row_C_1},{row_C_2},{row_C_3}], D [{row_D_1},{row_D_2},{row_D_3}], E [{row_E_1},{row_E_2},{row_E_3}], F [{row_F_1},{row_F_2},{row_F_3}]. The values are the {tokens_per_row} tokens, listed best to worst.\n\nEACH DAY:\n1. Draw the booty row and announce it to all players.\n2. Talk: everyone writes one short message at the same time. All messages are then shown to everyone. Messages are not binding.\n3. All players secretly and simultaneously choose one card from their hand.\n4. Reveal all cards.\n5. Clash: if two or three players played the same rank, all of those players are clashed. They take no booty, their abilities do not fire, and their cards are still spent. A player whose rank nobody else played is not clashed and plays normally.\n6. Booty: non-clashed players other than the Cabin Boy are ordered by rank, highest first. The first takes the best token, the second the next, and so on. Tokens left over are discarded.\n7. Abilities of non-clashed characters resolve at the same time, as listed above. Gunner and Quartermaster count only non-clashed players.\n8. Each player adds their token value plus or minus their ability effects to their score.\n9. After day {days_per_campaign}, discard leftover cards and deal fresh hands. After day {total_rounds}, the game ends.\n\nThe Cabin Boy's +{cabin_boy_gain} still applies when other players take booty. Scores can go negative.\n\nAfter {total_rounds} days, the player with the highest doubloon total wins. If two or more players share the highest total, they share the win."
}
```

Why it was refused: it plays, but part of it does nothing: game attribute `booty_rows` is never changed in 3 random matches, so nothing updates it. Steps that name it: set the day. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.; game attribute `full_hand` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "libertalia_shared_hand",
    "name": "Libertalia: Shared Hand",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Three pirates, identical 7-card hands, two campaigns of five days: reveal one character a day, share the booty, avoid clashes."
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
        "visible": "public",
        "type": "list",
        "initial": [1, 2, 3, 4, 5, 6, 7]
      },
      {
        "key": "card",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "clashed",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "token",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "ability",
        "visible": "public",
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
        "key": "choice",
        "visible": "ally",
        "type": "text",
        "initial": "0"
      }
    ],
    "game": [
      {"key": "day", "visible": "public", "type": "number", "initial": 0},
      {"key": "booty_rows", "visible": "public", "type": "list", "initial": []},
      {"key": "booty_row", "visible": "public", "type": "list", "initial": []},
      {"key": "players", "visible": "public", "type": "number", "initial": 3},
      {"key": "campaigns", "visible": "public", "type": "number", "initial": 2},
      {"key": "days_per_campaign", "visible": "public", "type": "number", "initial": 5},
      {"key": "total_rounds", "visible": "public", "type": "number", "initial": 10},
      {"key": "starting_score", "visible": "public", "type": "number", "initial": 0},
      {"key": "hand_size", "visible": "public", "type": "number", "initial": 7},
      {"key": "lowest_rank", "visible": "public", "type": "number", "initial": 1},
      {"key": "highest_rank", "visible": "public", "type": "number", "initial": 7},
      {"key": "cards_discarded_per_campaign", "visible": "public", "type": "number", "initial": 2},
      {"key": "cabin_boy_rank", "visible": "public", "type": "number", "initial": 1},
      {"key": "cabin_boy_gain", "visible": "public", "type": "number", "initial": 3},
      {"key": "gunner_rank", "visible": "public", "type": "number", "initial": 2},
      {"key": "gunner_penalty", "visible": "public", "type": "number", "initial": 3},
      {"key": "gunner_target_min_rank", "visible": "public", "type": "number", "initial": 6},
      {"key": "quartermaster_rank", "visible": "public", "type": "number", "initial": 3},
      {"key": "quartermaster_bonus_per_higher", "visible": "public", "type": "number", "initial": 1},
      {"key": "bosun_rank", "visible": "public", "type": "number", "initial": 4},
      {"key": "bosun_floor", "visible": "public", "type": "number", "initial": 0},
      {"key": "merchant_rank", "visible": "public", "type": "number", "initial": 5},
      {"key": "merchant_bonus", "visible": "public", "type": "number", "initial": 2},
      {"key": "merchant_threshold", "visible": "public", "type": "number", "initial": 3},
      {"key": "captain_rank", "visible": "public", "type": "number", "initial": 6},
      {"key": "admiral_rank", "visible": "public", "type": "number", "initial": 7},
      {"key": "admiral_wage", "visible": "public", "type": "number", "initial": 2},
      {"key": "row_count", "visible": "public", "type": "number", "initial": 6},
      {"key": "tokens_per_row", "visible": "public", "type": "number", "initial": 3},
      {"key": "row_A_1", "visible": "public", "type": "number", "initial": 5},
      {"key": "row_A_2", "visible": "public", "type": "number", "initial": 3},
      {"key": "row_A_3", "visible": "public", "type": "number", "initial": 1},
      {"key": "row_B_1", "visible": "public", "type": "number", "initial": 5},
      {"key": "row_B_2", "visible": "public", "type": "number", "initial": 1},
      {"key": "row_B_3", "visible": "public", "type": "number", "initial": -3},
      {"key": "row_C_1", "visible": "public", "type": "number", "initial": 3},
      {"key": "row_C_2", "visible": "public", "type": "number", "initial": 3},
      {"key": "row_C_3", "visible": "public", "type": "number", "initial": 1},
      {"key": "row_D_1", "visible": "public", "type": "number", "initial": 5},
      {"key": "row_D_2", "visible": "public", "type": "number", "initial": 3},
      {"key": "row_D_3", "visible": "public", "type": "number", "initial": -3},
      {"key": "row_E_1", "visible": "public", "type": "number", "initial": 3},
      {"key": "row_E_2", "visible": "public", "type": "number", "initial": 1},
      {"key": "row_E_3", "visible": "public", "type": "number", "initial": -3},
      {"key": "row_F_1", "visible": "public", "type": "number", "initial": 5},
      {"key": "row_F_2", "visible": "public", "type": "number", "initial": 5},
      {"key": "row_F_3", "visible": "public", "type": "number", "initial": -3}
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "seat the players",
      "do": [
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
      "label": "set the day",
      "do": [
        {
          "set": {
            "key": "day",
            "value": 0
          }
        },
        {
          "set": {
            "key": "booty_rows",
            "value": {
              "calc": "[[row_A_1, row_A_2, row_A_3], [row_B_1, row_B_2, row_B_3], [row_C_1, row_C_2, row_C_3], [row_D_1, row_D_2, row_D_3], [row_E_1, row_E_2, row_E_3], [row_F_1, row_F_2, row_F_3]]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "deal campaign 1",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "[lowest_rank, lowest_rank + 1, lowest_rank + 2, lowest_rank + 3, lowest_rank + 4, lowest_rank + 5, highest_rank]"
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
      "phase": "dawn",
      "label": "a new day",
      "do": [
        {
          "adjust": {
            "key": "day",
            "value": 1
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "[lowest_rank, lowest_rank + 1, lowest_rank + 2, lowest_rank + 3, lowest_rank + 4, lowest_rank + 5, highest_rank]"
            },
            "if": {
              "calc": "day == days_per_campaign + 1"
            },
            "text": "Campaign 2 begins: seat {player} discards the leftover cards and receives a fresh hand of ranks 1 to 7."
          }
        },
        {
          "set": {
            "players": "all",
            "key": "card",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "clashed",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "token",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "ability",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "choice",
            "value": "0"
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "dawn",
      "label": "draw the booty row",
      "do": [
        {
          "set": {
            "key": "booty_row",
            "value": {
              "calc": "booty_rows[min(int(uniform(0, row_count)), row_count - 1)]"
            }
          }
        }
      ],
      "text": "Day {day} of {total_rounds}. Today's booty row, best to worst: {booty_row}."
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
      "text": "Day {day}, booty row {booty_row}. Say one short thing to the table. Messages are not binding."
    },
    {
      "use": "poll",
      "phase": "play",
      "label": "play a card",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "store": "choice",
      "text": "Day {day}, booty row {booty_row}. Secretly choose one rank from your hand to play. Nobody sees any card until all are chosen."
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "reveal the cards",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "card",
            "value": {
              "calc": "int(you.choice)"
            }
          }
        },
        {
          "remove": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "you.card"
            }
          }
        }
      ],
      "text": "Cards revealed: seat 1 played {players[0].card}, seat 2 played {players[1].card}, seat 3 played {players[2].card}."
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "clashes",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "clashed",
            "value": {
              "calc": "count(p.card == you.card and p.seat != you.seat for p in players) >= 1"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "booty",
      "label": "share the booty",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "token",
            "value": {
              "calc": "((max(booty_row[count((not p.clashed) and p.card > cabin_boy_rank and p.card > you.card and p.seat != you.seat for p in players)], bosun_floor) if you.card == bosun_rank else booty_row[count((not p.clashed) and p.card > cabin_boy_rank and p.card > you.card and p.seat != you.seat for p in players)]) if ((not you.clashed) and you.card > cabin_boy_rank) else 0)"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "abilities",
      "label": "abilities",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "ability",
            "value": {
              "calc": "0 if you.clashed else ((cabin_boy_gain if you.card == cabin_boy_rank else 0) + (quartermaster_bonus_per_higher * count((not p.clashed) and p.card > quartermaster_rank and p.seat != you.seat for p in players) if you.card == quartermaster_rank else 0) + (merchant_bonus if (you.card == merchant_rank and you.token >= merchant_threshold) else 0) - (admiral_wage if you.card == admiral_rank else 0) - (gunner_penalty if (you.card >= gunner_target_min_rank and any((not p.clashed) and p.card == gunner_rank and p.seat != you.seat for p in players)) else 0))"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "score",
      "label": "score the day",
      "do": [
        {
          "adjust": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "you.token + you.ability"
            }
          }
        }
      ],
      "text": "Day {day} results. Seat 1: card {players[0].card}, clashed {players[0].clashed}, token {players[0].token}, ability {players[0].ability}, score {players[0].score}. Seat 2: card {players[1].card}, clashed {players[1].clashed}, token {players[1].token}, ability {players[1].ability}, score {players[1].score}. Seat 3: card {players[2].card}, clashed {players[2].clashed}, token {players[2].token}, ability {players[2].ability}, score {players[2].score}."
    },
    {
      "use": "check",
      "phase": "score",
      "label": "after day 10",
      "when": {
        "calc": "day >= total_rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "day >= total_rounds"
      },
      "rank_by": "you.score",
      "text": "Winner: {result}. Final scores: Seat 1 {players[0].score}, Seat 2 {players[1].score}, Seat 3 {players[2].score} doubloons."
    }
  },
  "limits": {
    "rounds": 10,
    "rounds_max": 10,
    "actions_max": 500,
    "deadline_s": 120
  },
  "rules": "Three pirates each start with {starting_score} doubloons. The game has {campaigns} campaigns of {days_per_campaign} days ({total_rounds} days in all). At the start of each campaign every player receives the same {hand_size}-card hand: ranks {lowest_rank} to {highest_rank}, one card of each rank. Cards played are removed from the owner's hand. The {cards_discarded_per_campaign} cards left after day {days_per_campaign} are discarded unused, and a fresh full hand is dealt for campaign 2. Which cards each player has played is public once revealed.\n\nCHARACTERS:\n- Rank {cabin_boy_rank}, Cabin Boy: takes no booty. Gains {cabin_boy_gain} doubloons.\n- Rank {gunner_rank}, Gunner: takes booty normally. Every other non-clashed player who played rank {gunner_target_min_rank} or 7 loses {gunner_penalty} doubloons.\n- Rank {quartermaster_rank}, Quartermaster: takes booty normally. Gains {quartermaster_bonus_per_higher} doubloon for each other non-clashed player who played a higher rank.\n- Rank {bosun_rank}, Bosun: takes booty normally. If the token taken is negative, it counts as {bosun_floor}; otherwise it counts at face value.\n- Rank {merchant_rank}, Merchant: takes booty normally. Gains {merchant_bonus} extra doubloons if the token taken is worth {merchant_threshold} or more; otherwise no extra.\n- Rank {captain_rank}, Captain: takes booty normally. No ability.\n- Rank {admiral_rank}, Admiral: takes booty normally. Pays a wage: loses {admiral_wage} doubloons.\n\nBOOTY ROWS: each day one row is drawn at random, each of the {row_count} equally likely, with replacement, from: A [{row_A_1},{row_A_2},{row_A_3}], B [{row_B_1},{row_B_2},{row_B_3}], C [{row_C_1},{row_C_2},{row_C_3}], D [{row_D_1},{row_D_2},{row_D_3}], E [{row_E_1},{row_E_2},{row_E_3}], F [{row_F_1},{row_F_2},{row_F_3}]. The values are the {tokens_per_row} tokens, listed best to worst.\n\nEACH DAY:\n1. Draw the booty row and announce it to all players.\n2. Talk: everyone writes one short message at the same time. All messages are then shown to everyone. Messages are not binding.\n3. All players secretly and simultaneously choose one card from their hand.\n4. Reveal all cards.\n5. Clash: if two or three players played the same rank, all of those players are clashed. They take no booty, their abilities do not fire, and their cards are still spent. A player whose rank nobody else played is not clashed and plays normally.\n6. Booty: non-clashed players other than the Cabin Boy are ordered by rank, highest first. The first takes the best token, the second the next, and so on. Tokens left over are discarded.\n7. Abilities of non-clashed characters resolve at the same time, as listed above. Gunner and Quartermaster count only non-clashed players.\n8. Each player adds their token value plus or minus their ability effects to their score.\n9. After day {days_per_campaign}, discard leftover cards and deal fresh hands. After day {total_rounds}, the game ends.\n\nThe Cabin Boy's +{cabin_boy_gain} still applies when other players take booty. Scores can go negative.\n\nAfter {total_rounds} days, the player with the highest doubloon total wins. If two or more players share the highest total, they share the win."
}
```
````
