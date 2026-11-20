# Task: write the XColos game file for "One Night Revolution: Ten Nights, Hidden Ledger"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 5 to 5; set `meta.players` to {"min": 5, "max": 5, "suggested": 5} (the suggested size is the one the game plays best at).

SETUP: 5 players. Each starts with 0 total points, 0 Rebel points, 0 Informant points. Before round 1 the engine lists all 10 unordered pairs of players and shuffles the list secretly. This is the only random event. In round r (r=1 to 10) the pair in position r is the Informants; the other 3 are Rebels. Every player is Informant in exactly 4 rounds with each other player as partner exactly once, and Rebel in exactly 6 rounds. Players are told this rule but not the order. EACH ROUND, in order: 1. ROLES: Each player is privately told Rebel or Informant for this round. Each Informant is also privately told who the other Informant is. 2. NIGHT (simultaneous): Every player privately names one other player as target. A Rebel target is investigated. An Informant target is framed. An Informant may name any other player including the partner; framing a partner has no extra effect. 3. NIGHT RESULTS: Each Rebel is privately told one result about their target: 'Informant' if the target is an Informant this round OR at least one Informant framed that target this round, otherwise 'Rebel'. A 'Rebel' result is always true; an 'Informant' result may be true or a frame. Informants receive no result. 4. CLAIMS (simultaneous): Every player writes one short message, e.g. claimed role, target or result. Lying allowed. All messages then shown to everyone. 5. RESPONSES (simultaneous): Every player writes one more short message. All shown to everyone. 6. VOTE (simultaneous): Every player names one other player to Terminate. All votes showing who voted for whom are then announced publicly. 7. TERMINATION: If no player received 2 or more votes, nobody is terminated. Otherwise every player tied for the most votes is terminated. The round roles of terminated players only are announced publicly; no other roles revealed. 8. SCORING (hidden): Each Rebel who voted for an Informant gains 2 points. If at least one terminated player is an Informant, each Rebel gains 1 more point. Each Informant gains 1 point for every Rebel who voted for a Rebel (0 to 3). Each Informant who was not terminated this round gains 2 points. Points gained while Rebel are also added to Rebel points; points gained while Informant also added to Informant points. No totals of any kind are announced during the game. Only the votes and the terminated roles are announced each round. Termination removes no one; all 5 play every round. After round 10 the engine announces every player's final total, Rebel points and Informant points and the game ends.

How the winner is decided: After 10 rounds the player with the highest total points wins. Tie-break: among tied, most Rebel points wins; if still tied, most Informant points wins; if still tied, draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: One Night Revolution: Ten Nights, Hidden Ledger (5 to 5 players, best with 5)

5 players play 10 rounds as rotating Rebels and Informants with framing, claims, and termination votes for hidden points.

STATE (every item below must exist in the file):
  - each player: total_points (number, starts 0); only its owner sees it. total hidden points
  - each player: rebel_points (number, starts 0); only its owner sees it. points earned while Rebel
  - each player: informant_points (number, starts 0); only its owner sees it. points earned while Informant
  - each player: current_role (text, starts ''); only its owner sees it. Rebel or Informant this round
  - each player: partner (number, starts 0); only its owner sees it. other Informant seat this round, 0 if Rebel
  - each player: target (number, starts 0); only its owner sees it. night target seat
  - each player: investigation_result (text, starts ''); only its owner sees it. Rebel night result Rebel or Informant, empty for Informants
  - each player: claim_msg (text, starts ''); everyone sees it. round claim message shown to all
  - each player: response_msg (text, starts ''); everyone sees it. round response message shown to all
  - each player: vote (number, starts 0); everyone sees it. seat voted to Terminate
  - each player: is_terminated (bool, starts False); everyone sees it. terminated this round
  - each player: revealed_role (text, starts ''); everyone sees it. round role announced if terminated else empty
  - the table: round_number (number, starts 1); everyone sees it. current round 1 to 10
  - the table: pair_order (list, starts []); hidden from all players. secret shuffled list of all 10 unordered pairs, position r is Informants in round r
  - the table: terminated_informant_count (number, starts 0); everyone sees it. number of terminated players who were Informant this round
  - parameters, each kept as a table attribute: num_players = 5, num_rounds = 10, num_pairs = 10, initial_points = 0, informant_rounds_per_player = 4, rebel_rounds_per_player = 6, rebel_correct_vote_gain = 2, rebel_team_bonus = 1, informant_per_misdirected_gain = 1, informant_survival_gain = 2, termination_min_votes = 2

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Each of the 5 players starts with 0 total points, 0 Rebel points and 0 Informant points.
  2. The engine lists all 10 unordered pairs of the 5 players and shuffles the list secretly as pair_order.
  3. This shuffle is the only random event and players are told the schedule rule but not the order.
  4. The engine sets game round_number to 1.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: sets each player current_role and partner from pair_order for game.round_number; clears is_terminated, revealed_role, target, vote, investigation_result
  2. [sync] all players. What happens: privately sends each player current_role; Informants also receive partner
  3. [poll] all players answers: {'type': 'choice', 'prompt': 'name one other player as night target'}. What happens: sets player.target; Rebel target is investigated and Informant target is framed
  4. [update] all players. What happens: sets player.investigation_result to Informant if target current_role is Informant or target was framed by any Informant, else Rebel; Informants keep empty
  5. [sync] all players. What happens: privately sends each Rebel investigation_result; Informants receive no result
  6. [poll] all players answers: {'type': 'text', 'prompt': 'write one short claim message'}. What happens: sets player.claim_msg and broadcasts to all as Seat {seat} says: {value}
  7. [poll] all players answers: {'type': 'text', 'prompt': 'write one short response message'}. What happens: sets player.response_msg and broadcasts to all as Seat {seat} says: {value}
  8. [poll] all players answers: {'type': 'choice', 'prompt': 'name one other player to Terminate'}. What happens: sets player.vote
  9. [tell] all players. What happens: announces all player.vote showing who voted for whom using vote
  10. [update] all players. What happens: sets player.is_terminated: if no seat has 2 or more votes then false for all, else true for seats tied for most votes; sets player.revealed_role to current_role if is_terminated else empty; sets game.terminated_informant_count
  11. [tell] all players. What happens: announces player.is_terminated and player.revealed_role for terminated players only
  12. [update] all players. What happens: adds hidden points: Rebels who voted for an Informant gain 2 to total_points and rebel_points; if terminated_informant_count >=1 each Rebel gains 1 more to total_points and rebel_points; each Informant gains 1 per Rebel who voted for a Rebel to total_points and informant_points; each Informant with is_terminated false gains 2 to total_points and informant_points; increments game.round_number; nothing about points is announced
  13. [check] all players. What happens: continues if game.round_number <= 10, otherwise ends and announces total_points, rebel_points and informant_points

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, then each player has 0 total points, 0 Rebel points and 0 Informant points.
  R2. When the game is played, then there are 10 rounds and in round r the pair in position r of the shuffled 10 pairs is the Informants.
  R3. When the schedule is used, then each player is Informant in exactly 4 rounds with each other player as partner exactly once and Rebel in exactly 6 rounds.
  R4. When a round starts, then each player is privately told Rebel or Informant and each Informant is told who the other Informant is.
  R5. When night happens, then every player simultaneously names one other player as target.
  R6. When night targets are set, then a Rebel target is investigated and an Informant target is framed, and an Informant may target anyone including the partner with no extra effect for framing a partner.
  R7. When night results are given, then each Rebel is privately told Informant if the target is an Informant this round or at least one Informant framed that target, otherwise Rebel.
  R8. When night results are given, then a Rebel result is always true and an Informant result may be true or a frame.
  R9. When night results are given, then Informants receive no result.
  R10. When claims happen, then every player simultaneously writes one short message with lying allowed and all messages are then shown to everyone.
  R11. When responses happen, then every player simultaneously writes one more short message and all are then shown to everyone.
  R12. When voting happens, then every player simultaneously names one other player to Terminate and all votes showing who voted for whom are announced publicly.
  R13. When votes are counted, then if no player received 2 or more votes nobody is terminated.
  R14. When at least one player received 2 or more votes, then every player tied for the most votes is terminated.
  R15. When termination is announced, then only the round roles of terminated players are announced publicly and no other roles are revealed.
  R16. When scoring happens, then each Rebel who voted for an Informant gains 2 points.
  R17. When scoring happens, then if at least one terminated player is an Informant each Rebel gains 1 more point.
  R18. When scoring happens, then each Informant gains 1 point for every Rebel who voted for a Rebel.
  R19. When scoring happens, then each Informant who was not terminated this round gains 2 points.
  R20. When points are gained while Rebel, then they are also added to Rebel points and when gained while Informant also added to Informant points.
  R21. When the game is played, then no totals of any kind are announced during the game and only votes and terminated roles are announced each round.
  R22. When termination happens, then it removes no one and all 5 play every round.
  R23. When round 10 ends, then the engine announces every player's final total, Rebel points and Informant points and the game ends.
  R24. When the game ends, then the player with the highest total points wins with tie-break most Rebel points then most Informant points then draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - night target | asked: all players | options: any other living seat except self: the 4 other seats
  - claim message | asked: all players | options: any short text, lying allowed
  - response message | asked: all players | options: any short text, lying allowed
  - vote to Terminate | asked: all players | options: any other living seat except self: the 4 other seats

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: game.round_number > 10
  - each player's standing: you.total_points * 1000000 + you.rebel_points * 1000 + you.informant_points (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: standing is total_points, tie-break most rebel_points then most informant_points; highest wins and tied top share the win
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

- each player: `total_points` (number, visible: ally, starts 0): total hidden points
- each player: `rebel_points` (number, visible: ally, starts 0): points earned while Rebel
- each player: `informant_points` (number, visible: ally, starts 0): points earned while Informant
- each player: `vote` (number, visible: public, starts 0): seat voted to Terminate
- each player: `is_terminated` (bool, visible: public, starts False): terminated this round
- each player: `revealed_role` (text, visible: public, starts ''): round role announced if terminated else empty
- the table: `terminated_informant_count` (number, visible: public, starts 0): number of terminated players who were Informant this round
- parameters (each must be an attribute holding this value, never a number buried in a step): num_players = 5, num_rounds = 10, num_pairs = 10, initial_points = 0, informant_rounds_per_player = 4, rebel_rounds_per_player = 6, rebel_correct_vote_gain = 2, rebel_team_bonus = 1, informant_per_misdirected_gain = 1, informant_survival_gain = 2, termination_min_votes = 2
- the game ends with ONE ending whose `rank_by` is `you.total_points * 1000000 + you.rebel_points * 1000 + you.informant_points`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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

Reset is_terminated to False, revealed_role to '' and terminated_informant_count to 0 at start of each round. Count votes from vote only, and if max votes >= termination_min_votes terminate every player tied for max. Do not eliminate anyone: all 5 must give target/claim/response/vote every round. Keep the single secret shuffled 10-pair list for rounds 1-10 and do not sort it.
