# 10 coder

- time: 2026-10-28T01:42:09+00:00 (85.1s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 50062c7398df7994, reply sha256 d24567d0bee45120

## Sent

````
# Task: write the XColos game file for "One Night Revolution: Ten Nights"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 5 to 5; set `meta.players` to {"min": 5, "max": 5, "suggested": 5} (the suggested size is the one the game plays best at).

SETUP: There are 5 players, each starting with 0 points. Each player also keeps two sub-totals, Rebel points and Informant points, both starting at 0. Before round 1, the engine lists all 10 possible pairs of players and shuffles that list secretly. This is the only random event in the game. In round r (r = 1 to 10), the pair in position r of the shuffled list are the Informants; the other 3 players are Rebels for that round. As a result, every player is an Informant in exactly 4 rounds, with each other player as partner exactly once, and a Rebel in exactly 6 rounds. All players are told this rule but not the order.

EACH ROUND:
1. ROLES: Each player is privately told their role for this round. Each Informant is also privately told who the other Informant is.
2. NIGHT (simultaneous): Every player privately names one other player as a target. A Rebel's target is investigated. An Informant's target is framed. An Informant may name any other player, including their partner (framing a partner has no extra effect).
3. NIGHT RESULTS: Each Rebel is privately told one result about their target. The result is 'Informant' if the target is an Informant this round, or if at least one Informant framed that target this round. Otherwise it is 'Rebel'. A 'Rebel' result is therefore always true; an 'Informant' result may be a frame. Informants receive no result.
4. CLAIMS (simultaneous): Every player writes one short message, for example a claimed role, target or result. Lying is allowed. All messages are then shown to everyone.
5. RESPONSES (simultaneous): Every player writes one more short message. All are shown to everyone.
6. VOTE (simultaneous): Every player names one other player to Terminate. All votes, showing who voted for whom, are then announced publicly.
7. TERMINATION: If no player received 2 or more votes, nobody is terminated. Otherwise, every player tied for the most votes is terminated. The round roles of the terminated players only are announced publicly; no other roles are revealed.
8. SCORING (individual):
   - Each Rebel who voted for an Informant gains 2 points.
   - If at least one terminated player is an Informant, each Rebel gains 1 more point.
   - Each Informant gains 1 point for every Rebel who voted for a Rebel (0 to 3).
   - If no Informant was terminated, each Informant gains 2 more points.
   - Points gained as a Rebel are also added to that player's Rebel points; points gained as an Informant are also added to their Informant points.
   - Everyone's totals are announced.
9. Termination does not remove anyone; all 5 players take part in every round. After round 10 the game ends.

How the winner is decided: After 10 rounds, the player with the highest total points wins. If several players tie, the one among them with the most Rebel points wins. If still tied, the one with the most Informant points wins. If still tied, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: One Night Revolution: Ten Nights (5 to 5 players, best with 5)

Five players play ten rounds of hidden roles. Each round a secretly scheduled pair are Informants and the other three are Rebels; players investigate or frame at night, talk twice, then vote, and score points individually.

STATE (every item below must exist in the file):
  - each player: score (number, starts 0); everyone sees it. total points
  - each player: rebel_points (number, starts 0); everyone sees it. points gained while a Rebel (first tie-break)
  - each player: informant_points (number, starts 0); everyone sees it. points gained while an Informant (second tie-break)
  - each player: role (text, starts ''); only its owner sees it. this round's role: 'Informant' or 'Rebel'
  - each player: partner (text, starts ''); only its owner sees it. for an Informant, the seat of the other Informant this round; empty for a Rebel
  - each player: target (text, starts ''); only its owner sees it. the seat named at night (investigated by a Rebel, framed by an Informant)
  - each player: result (text, starts ''); only its owner sees it. a Rebel's night result about their target: 'Informant' or 'Rebel'
  - each player: claim (text, starts ''); everyone sees it. this round's claims message
  - each player: response (text, starts ''); everyone sees it. this round's response message
  - each player: vote (text, starts ''); everyone sees it. the seat this player voted to Terminate this round
  - each player: votes_received (number, starts 0); everyone sees it. number of Terminate votes received this round
  - each player: terminated (bool, starts False); everyone sees it. terminated this round
  - each player: revealed_role (text, starts ''); everyone sees it. this round's role, announced only when the player is terminated; otherwise empty
  - the table: pair_order (list, starts 'the 10 pairs of seats, shuffled secretly at setup'); hidden from all players. entry r is the Informant pair for round r
  - the table: framed_seats (list, starts []); hidden from all players. the seats framed by at least one Informant this round; hidden, the engine keeps it
  - the table: round (number, starts 0); everyone sees it. current round number
  - the table: max_votes (number, starts 0); everyone sees it. the highest votes_received this round
  - the table: informant_terminated (bool, starts False); everyone sees it. true if at least one terminated player is an Informant this round
  - the table: rebel_misvotes (number, starts 0); everyone sees it. number of Rebels who voted for a Rebel this round
  - parameters, each kept as a table attribute: player_count = 5, rounds = 10, possible_pairs = 10, informants_per_round = 2, rebels_per_round = 3, informant_rounds_per_player = 4, rebel_rounds_per_player = 6, starting_points = 0, termination_vote_threshold = 2, rebel_correct_vote_points = 2, rebel_informant_terminated_bonus = 1, informant_points_per_rebel_misvote = 1, informant_max_misvote_points = 3, informant_survival_bonus = 2, messages_per_round = 2

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Five seats are filled; each player's score, rebel_points and informant_points start at 0.
  2. The engine lists all 10 pairs of the 5 seats and shuffles the list secretly into pair_order. This is the only random event in the game.
  3. All players are told that in round r the pair in position r of pair_order are the Informants and the other 3 are Rebels. Each player is therefore an Informant in exactly 4 rounds, partnered with each other player exactly once, and a Rebel in 6 rounds. They are not told the order.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round += 1. For every player, reset target, result, claim, response and vote to '', terminated to false, revealed_role to '' and votes_received to 0. Set framed_seats to [] and reset max_votes, informant_terminated and rebel_misvotes.
  2. [update] all players. What happens: Let the pair be pair_order[round]. Each seat in the pair gets role = 'Informant' and partner = the other seat of the pair. Every other seat gets role = 'Rebel' and partner = ''.
  3. [sync] all players. What happens: Each player privately sees their own role and, if an Informant, their partner.
  4. [poll] all players answers: one other seat. What happens: Set target. Then, for each Informant, append that Informant's target to framed_seats if it is not already there. Framing the partner has no extra effect.
  5. [update] each Rebel. What happens: result = 'Informant' if target.role == 'Informant' or target is in framed_seats; otherwise result = 'Rebel'.
  6. [sync] each Rebel. What happens: Each Rebel privately sees their result. Informants receive no result.
  7. [poll] all players answers: short text (claims; lying allowed). What happens: Set claim; broadcast {"to": "all", "text": "Seat {seat} says: {value}"}.
  8. [poll] all players answers: short text (responses; lying allowed). What happens: Set response; broadcast {"to": "all", "text": "Seat {seat} responds: {value}"}.
  9. [poll] all players answers: one other seat to Terminate. What happens: Set vote; publicly announce every voter and whom they voted for.
  10. [update] all players. What happens: votes_received = number of players whose vote names this seat; max_votes = the highest votes_received.
  11. [update] all players. What happens: If max_votes >= 2, then terminated = true for each player with votes_received == max_votes. For each terminated player, revealed_role = role. informant_terminated = true if any terminated player has role 'Informant'. Announce the revealed roles of terminated players only.
  12. [update] all players. What happens: rebel_misvotes = number of Rebels whose vote names a Rebel. Each Rebel gains g = (2 if their vote names an Informant else 0) + (1 if informant_terminated else 0); score += g and rebel_points += g. Each Informant gains g = rebel_misvotes + (2 if not informant_terminated else 0); score += g and informant_points += g.
  13. [tell] all players. What happens: Announce every player's score, rebel_points and informant_points.
  14. [check] all players. What happens: If round >= 10, end the game; otherwise run the next round. No one is ever removed from play.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. At the start, every player has score 0, rebel_points 0 and informant_points 0.
  R2. Before round 1, the 10 pairs of the 5 seats are shuffled once into pair_order, and no other randomness occurs.
  R3. In round r, the two seats in pair_order position r have role Informant and the other 3 have role Rebel.
  R4. Over 10 rounds, each player is an Informant exactly 4 times, with each other player as partner exactly once, and a Rebel exactly 6 times.
  R5. Each round, each Informant privately learns the seat of the other Informant; Rebels learn no partner.
  R6. At night, every player names exactly one other seat as target, simultaneously; naming oneself is not allowed.
  R7. When a Rebel's target is an Informant this round, the Rebel's result is 'Informant'.
  R8. When a Rebel's target is a Rebel framed by at least one Informant this round, the result is 'Informant'.
  R9. When a Rebel's target is a Rebel that no Informant framed, the result is 'Rebel'.
  R10. Informants receive no night result.
  R11. Every player sends one claim message and then one response message, each collected simultaneously and shown to all.
  R12. Every player votes for exactly one other seat, simultaneously, and all votes are announced with voter and target.
  R13. When no player receives 2 or more votes, nobody is terminated.
  R14. When the highest vote count is 2 or more, every player with that count is terminated (for example, a 2-2-1 split terminates two players).
  R15. Only terminated players have their round role announced publicly.
  R16. When a Rebel votes for an Informant, that Rebel gains 2 points.
  R17. When at least one terminated player is an Informant, each Rebel gains 1 more point.
  R18. Each Informant gains 1 point for every Rebel who voted for a Rebel (0 to 3).
  R19. When no Informant is terminated (including when nobody is terminated), each Informant gains 2 more points.
  R20. Points gained as a Rebel are added to both score and rebel_points; points gained as an Informant are added to both score and informant_points.
  R21. Termination removes no one; all 5 players take part in every round.
  R22. After round 10 the game ends, and the highest score wins.
  R23. When scores tie at the top, the player with the most rebel_points wins; if still tied, the one with the most informant_points; if still tied, the tied players share a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Night target | asked: every seat | options: any one of the 4 other seats (an Informant may name their partner)
  - Claim message | asked: every seat | options: short free text
  - Response message | asked: every seat | options: short free text
  - Terminate vote | asked: every seat | options: any one of the 4 other seats

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round >= 10
  - each player's standing: you.score * 10000 + you.rebel_points * 100 + you.informant_points (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Highest total points wins. Ties are broken by most Rebel points, then by most Informant points. Players still level share the result, which counts as the draw.
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

- each player: `score` (number, visible: public, starts 0): total points
- each player: `rebel_points` (number, visible: public, starts 0): points gained while a Rebel (first tie-break)
- each player: `informant_points` (number, visible: public, starts 0): points gained while an Informant (second tie-break)
- each player: `vote` (text, visible: public, starts ''): the seat this player voted to Terminate this round
- each player: `terminated` (bool, visible: public, starts False): terminated this round
- each player: `revealed_role` (text, visible: public, starts ''): this round's role, announced only when the player is terminated; otherwise empty
- the table: `round` (number, visible: public, starts 0): current round number
- parameters (each must be an attribute holding this value, never a number buried in a step): player_count = 5, rounds = 10, possible_pairs = 10, informants_per_round = 2, rebels_per_round = 3, informant_rounds_per_player = 4, rebel_rounds_per_player = 6, starting_points = 0, termination_vote_threshold = 2, rebel_correct_vote_points = 2, rebel_informant_terminated_bonus = 1, informant_points_per_rebel_misvote = 1, informant_max_misvote_points = 3, informant_survival_bonus = 2, messages_per_round = 2
- the game ends with ONE ending whose `rank_by` is `you.score * 10000 + you.rebel_points * 100 + you.informant_points`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
    "id": "one_night_revolution_ten_nights",
    "name": "One Night Revolution: Ten Nights",
    "players": {
      "min": 5,
      "max": 5,
      "suggested": 5
    },
    "blurb": "Five players, ten nights: each night a secret pair are Informants, the rest Rebels; investigate or frame, talk twice, vote, score alone."
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
        "key": "rebel_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "informant_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "role",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "partner",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "target",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "result",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "claim",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "response",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "vote",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "votes_received",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "terminated",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "revealed_role",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "seat_options",
        "visible": "ally",
        "type": "list",
        "initial": []
      }
    ],
    "game": [
      {
        "key": "pair_order",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "framed_seats",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "max_votes",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "informant_terminated",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "rebel_misvotes",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "pair_pool",
        "visible": "none",
        "type": "list",
        "initial": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
      },
      {
        "key": "pair_a",
        "visible": "none",
        "type": "list",
        "initial": [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
      },
      {
        "key": "pair_b",
        "visible": "none",
        "type": "list",
        "initial": [2, 3, 4, 5, 3, 4, 5, 4, 5, 5]
      },
      {
        "key": "seat_labels",
        "visible": "none",
        "type": "list",
        "initial": ["1", "2", "3", "4", "5"]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "player_count",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "possible_pairs",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "informants_per_round",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "rebels_per_round",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "informant_rounds_per_player",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "rebel_rounds_per_player",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "starting_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "termination_vote_threshold",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "rebel_correct_vote_points",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "rebel_informant_terminated_bonus",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "informant_points_per_rebel_misvote",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "informant_max_misvote_points",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "informant_survival_bonus",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "messages_per_round",
        "visible": "public",
        "type": "number",
        "initial": 2
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the seats",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "starting_points"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "rebel_points",
            "value": {
              "calc": "starting_points"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "informant_points",
            "value": {
              "calc": "starting_points"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "seat_options",
            "value": {
              "calc": "[l for l in seat_labels if l != seat_labels[you.seat - 1]]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "shuffle the pairs",
      "do": [
        {"set": {"key": "pick", "value": {"calc": "pair_pool[int(uniform(0, len(pair_pool)))]"}}},
        {"append": {"key": "pair_order", "value": {"calc": "pick"}}},
        {"remove": {"key": "pair_pool", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "pair_pool[int(uniform(0, len(pair_pool)))]"}}},
        {"append": {"key": "pair_order", "value": {"calc": "pick"}}},
        {"remove": {"key": "pair_pool", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "pair_pool[int(uniform(0, len(pair_pool)))]"}}},
        {"append": {"key": "pair_order", "value": {"calc": "pick"}}},
        {"remove": {"key": "pair_pool", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "pair_pool[int(uniform(0, len(pair_pool)))]"}}},
        {"append": {"key": "pair_order", "value": {"calc": "pick"}}},
        {"remove": {"key": "pair_pool", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "pair_pool[int(uniform(0, len(pair_pool)))]"}}},
        {"append": {"key": "pair_order", "value": {"calc": "pick"}}},
        {"remove": {"key": "pair_pool", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "pair_pool[int(uniform(0, len(pair_pool)))]"}}},
        {"append": {"key": "pair_order", "value": {"calc": "pick"}}},
        {"remove": {"key": "pair_pool", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "pair_pool[int(uniform(0, len(pair_pool)))]"}}},
        {"append": {"key": "pair_order", "value": {"calc": "pick"}}},
        {"remove": {"key": "pair_pool", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "pair_pool[int(uniform(0, len(pair_pool)))]"}}},
        {"append": {"key": "pair_order", "value": {"calc": "pick"}}},
        {"remove": {"key": "pair_pool", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "pair_pool[int(uniform(0, len(pair_pool)))]"}}},
        {"append": {"key": "pair_order", "value": {"calc": "pick"}}},
        {"remove": {"key": "pair_pool", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "pair_pool[int(uniform(0, len(pair_pool)))]"}}},
        {"append": {"key": "pair_order", "value": {"calc": "pick"}}},
        {"remove": {"key": "pair_pool", "value": {"calc": "pick"}}}
      ]
    },
    {
      "use": "tell",
      "label": "the schedule",
      "to": "all",
      "text": "All {possible_pairs} pairs of seats have been shuffled secretly into a schedule. In round r the pair in position r are the {informants_per_round} Informants and the other {rebels_per_round} are Rebels. Each of you is an Informant in exactly {informant_rounds_per_player} rounds, partnered with each other player exactly once, and a Rebel in {rebel_rounds_per_player} rounds. The order is not revealed."
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
      "phase": "dusk",
      "label": "a new round",
      "do": [
        {"adjust": {"key": "round", "value": 1}},
        {"set": {"players": "all", "key": "target", "value": ""}},
        {"set": {"players": "all", "key": "result", "value": ""}},
        {"set": {"players": "all", "key": "claim", "value": ""}},
        {"set": {"players": "all", "key": "response", "value": ""}},
        {"set": {"players": "all", "key": "vote", "value": ""}},
        {"set": {"players": "all", "key": "terminated", "value": false}},
        {"set": {"players": "all", "key": "revealed_role", "value": ""}},
        {"set": {"players": "all", "key": "votes_received", "value": 0}},
        {"set": {"key": "framed_seats", "value": []}},
        {"set": {"key": "max_votes", "value": 0}},
        {"set": {"key": "informant_terminated", "value": false}},
        {"set": {"key": "rebel_misvotes", "value": 0}}
      ],
      "text": "Round {round} of {rounds} begins."
    },
    {
      "use": "update",
      "phase": "dusk",
      "label": "the roles",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "role",
            "value": {
              "calc": "'Informant' if (you.seat == pair_a[pair_order[round - 1]] or you.seat == pair_b[pair_order[round - 1]]) else 'Rebel'"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "partner",
            "value": {
              "calc": "seat_labels[pair_b[pair_order[round - 1]] - 1] if you.seat == pair_a[pair_order[round - 1]] else (seat_labels[pair_a[pair_order[round - 1]] - 1] if you.seat == pair_b[pair_order[round - 1]] else '')"
            }
          }
        }
      ]
    },
    {
      "use": "sync",
      "phase": "dusk",
      "label": "your role",
      "mode": "self",
      "to": "all",
      "fields": ["role", "partner"],
      "text": "Your role this round (and your partner, if you are an Informant):"
    },
    {
      "use": "poll",
      "phase": "night",
      "label": "night target",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "seat_options"
        }
      },
      "store": "target",
      "text": "Night falls. Name one other seat as your target. If you are a Rebel, you investigate them. If you are an Informant, you frame them (you may name your partner; that has no extra effect)."
    },
    {
      "use": "update",
      "phase": "night",
      "label": "night results",
      "do": [
        {
          "set": {
            "key": "framed_seats",
            "value": {
              "calc": "[l for l in seat_labels if any(p.role == 'Informant' and p.target == l for p in players)]"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.role == 'Rebel'"
            },
            "key": "result",
            "value": {
              "calc": "'Informant' if (you.target in framed_seats or any(p.role == 'Informant' and seat_labels[p.seat - 1] == you.target for p in players)) else 'Rebel'"
            }
          }
        }
      ]
    },
    {
      "use": "sync",
      "phase": "night",
      "label": "your result",
      "mode": "self",
      "to": {
        "where": "you.role == 'Rebel'"
      },
      "fields": ["target", "result"],
      "text": "Your investigation result:"
    },
    {
      "use": "poll",
      "phase": "day",
      "label": "claims",
      "to": "acting",
      "answer": {
        "type": "text",
        "max_words": 40
      },
      "store": "claim",
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} says: {value}"
      },
      "text": "Write one short message to the table: a claimed role, target or result, or anything else. Lying is allowed. Everyone will see it."
    },
    {
      "use": "poll",
      "phase": "day",
      "label": "responses",
      "to": "acting",
      "answer": {
        "type": "text",
        "max_words": 40
      },
      "store": "response",
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} responds: {value}"
      },
      "text": "Write one more short message responding to the claims. Lying is allowed. Everyone will see it."
    },
    {
      "use": "poll",
      "phase": "vote",
      "label": "terminate vote",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "seat_options"
        }
      },
      "store": "vote",
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} votes to Terminate seat {value}."
      },
      "text": "Name one other seat to Terminate. All votes are announced with who voted for whom."
    },
    {
      "use": "update",
      "phase": "vote",
      "label": "count the votes",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "votes_received",
            "value": {
              "calc": "count(p.vote == seat_labels[you.seat - 1] for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "max_votes",
            "value": {
              "calc": "max([p.votes_received for p in players])"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "vote",
      "label": "termination",
      "do": [
        {
          "set": {
            "players": {
              "where": "max_votes >= termination_vote_threshold and you.votes_received == max_votes"
            },
            "key": "terminated",
            "value": true
          }
        },
        {
          "set": {
            "players": {
              "where": "you.terminated"
            },
            "key": "revealed_role",
            "value": {
              "calc": "you.role"
            }
          }
        },
        {
          "set": {
            "key": "informant_terminated",
            "value": {
              "calc": "any(p.terminated and p.role == 'Informant' for p in players)"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "vote",
      "label": "terminated roles",
      "when": {
        "calc": "max_votes >= termination_vote_threshold"
      },
      "to": "all",
      "text": "Terminated this round [seat, role]: {[[p.seat, p.revealed_role] for p in players if p.terminated]}."
    },
    {
      "use": "tell",
      "phase": "vote",
      "label": "nobody terminated",
      "when": {
        "calc": "max_votes < termination_vote_threshold"
      },
      "to": "all",
      "text": "No player received {termination_vote_threshold} or more votes. Nobody is terminated."
    },
    {
      "use": "update",
      "phase": "score",
      "label": "scoring",
      "do": [
        {
          "set": {
            "key": "rebel_misvotes",
            "value": {
              "calc": "count(p.role == 'Rebel' and any(q.role == 'Rebel' and seat_labels[q.seat - 1] == p.vote for q in players) for p in players)"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.role == 'Rebel'"
            },
            "key": "score",
            "value": {
              "calc": "(rebel_correct_vote_points if any(q.role == 'Informant' and seat_labels[q.seat - 1] == you.vote for q in players) else 0) + (rebel_informant_terminated_bonus if informant_terminated else 0)"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.role == 'Rebel'"
            },
            "key": "rebel_points",
            "value": {
              "calc": "(rebel_correct_vote_points if any(q.role == 'Informant' and seat_labels[q.seat - 1] == you.vote for q in players) else 0) + (rebel_informant_terminated_bonus if informant_terminated else 0)"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.role == 'Informant'"
            },
            "key": "score",
            "value": {
              "calc": "min(rebel_misvotes * informant_points_per_rebel_misvote, informant_max_misvote_points) + (0 if informant_terminated else informant_survival_bonus)"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.role == 'Informant'"
            },
            "key": "informant_points",
            "value": {
              "calc": "min(rebel_misvotes * informant_points_per_rebel_misvote, informant_max_misvote_points) + (0 if informant_terminated else informant_survival_bonus)"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "score",
      "label": "totals",
      "to": "all",
      "text": "After round {round}, totals [seat, score, rebel points, informant points]: {[[p.seat, p.score, p.rebel_points, p.informant_points] for p in players]}."
    },
    {
      "use": "check",
      "phase": "score",
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
      "rank_by": "you.score * 10000 + you.rebel_points * 100 + you.informant_points",
      "text": "Winner: {result}. Final [seat, score, rebel points, informant points]: {[[p.seat, p.score, p.rebel_points, p.informant_points] for p in players]}."
    }
  },
  "limits": {
    "rounds": 10,
    "rounds_max": 10,
    "actions_max": 1000,
    "deadline_s": 120
  },
  "rules": "There are {player_count} players, each starting with {starting_points} points, {starting_points} Rebel points and {starting_points} Informant points. Before round 1, all {possible_pairs} possible pairs of players are listed and the list is shuffled secretly; this is the only random event in the game. In round r (r = 1 to {rounds}), the pair in position r of the shuffled list are the {informants_per_round} Informants; the other {rebels_per_round} players are Rebels for that round. So every player is an Informant in exactly {informant_rounds_per_player} rounds, with each other player as partner exactly once, and a Rebel in exactly {rebel_rounds_per_player} rounds. You are not told the order.\n\nEACH ROUND:\n1. ROLES: Each player is privately told their role for this round. Each Informant is also privately told who the other Informant is. Rebels learn no partner.\n2. NIGHT (simultaneous): Every player privately names one other player (never themselves) as a target. A Rebel's target is investigated. An Informant's target is framed. An Informant may name any other player, including their partner (framing a partner has no extra effect).\n3. NIGHT RESULTS: Each Rebel is privately told one result about their target. The result is 'Informant' if the target is an Informant this round, or if at least one Informant framed that target this round. Otherwise it is 'Rebel'. A 'Rebel' result is therefore always true; an 'Informant' result may be a frame. Informants receive no result.\n4. CLAIMS (simultaneous): Every player writes one short message, for example a claimed role, target or result. Lying is allowed. All messages are then shown to everyone.\n5. RESPONSES (simultaneous): Every player writes one more short message. All are shown to everyone. ({messages_per_round} messages per player per round.)\n6. VOTE (simultaneous): Every player names one other player to Terminate. All votes, showing who voted for whom, are then announced publicly.\n7. TERMINATION: If no player received {termination_vote_threshold} or more votes, nobody is terminated. Otherwise, every player tied for the most votes is terminated (for example, a 2-2-1 split terminates two players). The round roles of the terminated players only are announced publicly; no other roles are revealed.\n8. SCORING (individual):\n - Each Rebel who voted for an Informant gains {rebel_correct_vote_points} points; a Rebel who voted for a Rebel gains nothing for the vote.\n - If at least one terminated player is an Informant, each Rebel gains {rebel_informant_terminated_bonus} more point; otherwise Rebels get no bonus.\n - Each Informant gains {informant_points_per_rebel_misvote} point for every Rebel who voted for a Rebel (at most {informant_max_misvote_points}).\n - If no Informant was terminated (including when nobody is terminated), each Informant gains {informant_survival_bonus} more points; if an Informant was terminated, they get no such bonus.\n - Points gained as a Rebel are also added to that player's Rebel points; points gained as an Informant are also added to their Informant points.\n - Everyone's totals are announced.\n9. Termination does not remove anyone; all {player_count} players take part in every round. After round {rounds} the game ends.\n\nWINNING: After {rounds} rounds, the player with the highest total points wins. If several players tie, the one among them with the most Rebel points wins. If still tied, the one with the most Informant points wins. If still tied, the tied players share the result as a draw."
}
```
````
