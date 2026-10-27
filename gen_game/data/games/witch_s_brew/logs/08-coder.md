# 08 coder

- time: 2026-10-27T22:15:23+00:00 (49.2s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 8f0fff11942dce7f, reply sha256 9bfa64793b1f728f

## Sent

````
# Task: write the XColos game file for "Witch's Brew: Claims"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 5; set `meta.players` to {"min": 3, "max": 5, "suggested": 4} (the suggested size is the one the game plays best at).

SETUP. N players (3-5) sit in a fixed clockwise order, numbered 1 to N. Everyone starts with 0 points. The game has 3 sets of N rounds each (3N rounds in total).

ROLES. There are six roles, each with a strong reward and a weak reward:
- Witch: strong 5, weak 2.
- Raven Keeper: strong 6, weak 0.
- Alchemist: strong 4, weak 1.
- Druid: strong 3, weak 2.
- Herb Hag: strong 2, weak 1.
- Thief: the strong reward is to take 3 points from the other player with the highest current total (ties go to the tied player first clockwise after the Thief). The Thief gains 3, that player loses 3, and a total may go below 0. Weak 1.

START OF A SET. At the start of each set, every player secretly and simultaneously chooses exactly 3 different roles to hold for that set. Hands are private; the engine records them. The list of roles led this set is emptied.

LEADER. In set k, the first round's leader is player k (set 3 with 3 players: player 3). Leadership then passes clockwise each round, so every player leads exactly once per set.

EACH ROUND:
1. The leader is announced.
2. The leader names one role that has not yet been led in this set. They may name a role they do not hold. The named role is added to this set's led list.
3. Talk: every player at the same time writes one short message without seeing the others. All messages are then shown to everyone. Messages bind no one.
4. Responses: every player other than the leader who holds the named role must respond. All of them choose at the same moment, either CONTEST or YIELD. Players who do not hold it pass automatically.
5. Reveal: all responses are shown, so everyone learns who held the role.
6. Resolve: start from the leader and go clockwise. The leader is the first claimant, and each contester, in clockwise order, takes over the claim. The final claimant is the last contester in clockwise order after the leader, or the leader if nobody contested.
   - The final claimant gets the role's strong reward. Exception: if the final claimant is the leader and the leader does not hold the named role, they get nothing.
   - The leader, if overtaken, gets 0. Every contester overtaken by a later contester gets 0.
   - Every player who yielded gets the role's weak reward.
7. The named role is removed from the hand of the leader (if held) and of every responder. A role cannot be led again this set.
8. Scores are announced and leadership passes clockwise.

Roles held but never led or responded to during a set are simply lost when the set ends. After round 3N, the game ends.

How the winner is decided: After the final round, the player with the highest total points wins. If two or more players tie for the highest total, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Witch's Brew: Claims (3 to 5 players, best with 4)

Over 3 sets of N rounds, players secretly hold 3 of 6 roles. Each round a leader names a role, holders choose at once to contest or yield, and the last contester clockwise takes the strong reward.

STATE (every item below must exist in the file):
  - each player: score (number, starts 0); everyone sees it. Total points. It may go below 0 because of the Thief.
  - each player: hand (list, starts []); only its owner sees it. The roles this player holds in the current set: 3 chosen at the start of the set, each removed once led or responded to.
  - each player: response (text, starts 'none'); everyone sees it. This round's response: contest, yield, or none (the player is the leader or does not hold the named role). It is shown to everyone at the reveal.
  - the table: set_number (number, starts 1); everyone sees it. The current set, from 1 to 3.
  - the table: round_in_set (number, starts 1); everyone sees it. The round within the current set, from 1 to N.
  - the table: round_count (number, starts 0); everyone sees it. Rounds completed so far.
  - the table: leader_seat (number, starts 1); everyone sees it. The seat leading this round.
  - the table: named_role (text, starts ''); everyone sees it. The role named by the leader this round.
  - the table: led_list (list, starts []); everyone sees it. The roles already led in the current set.
  - the table: leader_holds (bool, starts False); hidden from all players. Whether the named role was in the leader's hand when it was named.
  - the table: final_claimant (number, starts 0); everyone sees it. The seat that ends up with the claim this round.
  - the table: thief_target (number, starts 0); everyone sees it. The seat robbed by a strong Thief reward this round.
  - parameters, each kept as a table attribute: num_sets = 3, roles_per_hand = 3, role_count = 6, witch_strong = 5, witch_weak = 2, raven_keeper_strong = 6, raven_keeper_weak = 0, alchemist_strong = 4, alchemist_weak = 1, druid_strong = 3, druid_weak = 2, herb_hag_strong = 2, herb_hag_weak = 1, thief_steal = 3, thief_weak = 1, starting_score = 0, overtaken_reward = 0

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seats are numbered 1 to N clockwise, with N from 3 to 5.
  2. Every player's score is set to 0.
  3. set_number = 1, round_in_set = 1, round_count = 0, and led_list is empty.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: When round_in_set == 1: empty every player's hand (roles left unused from the previous set are lost) and empty led_list.
  2. [poll] all players answers: One of the 20 combinations of 3 different roles from {Witch, Raven Keeper, Alchemist, Druid, Herb Hag, Thief}. What happens: When round_in_set == 1: set each player's hand to the 3 roles in the chosen combination. Hands stay private (ally).
  3. [update] all players. What happens: Set leader_seat = ((set_number - 1) + (round_in_set - 1)) mod N + 1 and set every player's response to 'none'. Announce: 'Seat {leader_seat} leads this round.'
  4. [ask] seat leader_seat answers: One role from {Witch, Raven Keeper, Alchemist, Druid, Herb Hag, Thief} that is not in led_list. What happens: Set named_role to the chosen role and append it to led_list. Set leader_holds = (named_role is in the leader's hand). Announce the named role.
  5. [poll] all players answers: Short text message. What happens: Broadcast to all: 'Seat {seat} says: {value}'. Nothing binds.
  6. [poll] each player other than leader_seat whose hand contains named_role answers: contest | yield. What happens: Set response to 'contest' or 'yield'. Players who do not hold the role keep 'none' (an automatic pass).
  7. [tell] all players. What happens: Reveal every seat's response, which shows who held named_role.
  8. [update] all players. What happens: If any player's response == 'contest', set final_claimant to the contester with the largest (seat - leader_seat) mod N. Otherwise set final_claimant = leader_seat.
  9. [update] all players. What happens: Strong reward. If final_claimant != leader_seat or leader_holds is true, then: if named_role is not Thief, final_claimant's score += that role's strong value (Witch 5, Raven Keeper 6, Alchemist 4, Druid 3, Herb Hag 2). If named_role is Thief, set thief_target to the seat other than final_claimant with the highest score (ties go to the smallest (seat - final_claimant) mod N), then final_claimant's score += 3 and thief_target's score -= 3. If final_claimant == leader_seat and leader_holds is false, nobody gets the strong reward. The overtaken leader and overtaken contesters get 0.
  10. [update] all players. What happens: Weak reward: every player with response == 'yield' gets score += the weak value of named_role (Witch 2, Raven Keeper 0, Alchemist 1, Druid 2, Herb Hag 1, Thief 1).
  11. [update] all players. What happens: Remove named_role from the hand of leader_seat (if held) and from the hand of every player whose response != 'none'.
  12. [update] all players. What happens: round_count += 1 and round_in_set += 1. If round_in_set > N, set round_in_set = 1 and set_number += 1. Announce all scores.
  13. [check] all players. What happens: End the game if round_count >= 3 * N; otherwise continue.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, every player has score 0.
  R2. When round_in_set is 1, every player simultaneously chooses exactly 3 different roles, and these become their hand, replacing any roles left from the previous set.
  R3. When a new set begins, led_list is emptied.
  R4. When round r of set k is played, the leader is seat ((k-1)+(r-1)) mod N + 1, so set 1 starts with seat 1, set 2 with seat 2 and set 3 with seat 3.
  R5. When the leader names a role, it must not already be in led_list; it may be a role the leader does not hold, and it is appended to led_list.
  R6. When the role is named, every player submits one short message simultaneously, and all messages are then shown to everyone.
  R7. When a non-leader holds the named role, they must choose contest or yield simultaneously with the other holders; non-holders and the leader have response 'none'.
  R8. When responses are in, all responses are revealed to everyone.
  R9. When at least one player contests, the final claimant is the contester furthest clockwise from the leader (largest (seat - leader) mod N); otherwise the final claimant is the leader.
  R10. When the final claimant is not the leader, or is the leader and holds the named role, they gain the strong reward: Witch 5, Raven Keeper 6, Alchemist 4, Druid 3, Herb Hag 2.
  R11. When the final claimant is the leader and the leader does not hold the named role, nobody gains the strong reward.
  R12. When the strong Thief reward is given, the claimant gains 3 and the other player with the highest score loses 3 (ties go to the first tied seat clockwise after the claimant), and a score may go below 0.
  R13. When the leader or a contester is overtaken by a later contester, they gain 0 points.
  R14. When a player yields, they gain the weak reward: Witch 2, Raven Keeper 0, Alchemist 1, Druid 2, Herb Hag 1, Thief 1.
  R15. When a round resolves, the named role is removed from the leader's hand (if held) and from the hand of every player who contested or yielded.
  R16. When round_count reaches 3*N, the game ends, and the highest score wins, with tied top scores sharing the result.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Choose roles for the set (when round_in_set == 1) | asked: all players | options: Any of the 20 combinations of 3 different roles from Witch, Raven Keeper, Alchemist, Druid, Herb Hag, Thief
  - Name a role | asked: seat leader_seat | options: Every role not in led_list, whether held or not
  - Talk | asked: all players | options: One short free-text message
  - Respond to the named role | asked: each non-leader seat holding named_role | options: A holder other than the leader: contest, yield. The leader and non-holders are not asked.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round_count >= 3 * N
  - each player's standing: you.score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's total score. The highest total wins, and players tied for the highest share the result (the source calls this a draw).
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

- each player: `score` (number, visible: public, starts 0): Total points. It may go below 0 because of the Thief.
- each player: `response` (text, visible: public, starts 'none'): This round's response: contest, yield, or none (the player is the leader or does not hold the named role). It is shown to everyone at the reveal.
- the table: `named_role` (text, visible: public, starts ''): The role named by the leader this round.
- parameters (each must be an attribute holding this value, never a number buried in a step): num_sets = 3, roles_per_hand = 3, role_count = 6, witch_strong = 5, witch_weak = 2, raven_keeper_strong = 6, raven_keeper_weak = 0, alchemist_strong = 4, alchemist_weak = 1, druid_strong = 3, druid_weak = 2, herb_hag_strong = 2, herb_hag_weak = 1, thief_steal = 3, thief_weak = 1, starting_score = 0, overtaken_reward = 0
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
    "id": "witchs_brew_claims",
    "name": "Witch's Brew: Claims",
    "players": {
      "min": 3,
      "max": 5,
      "suggested": 4
    },
    "blurb": "Over 3 sets, secretly hold 3 of 6 roles; leaders name roles, holders contest or yield, and the last contester clockwise takes the strong reward."
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
        "key": "response",
        "visible": "public",
        "type": "text",
        "initial": "none"
      },
      {
        "key": "set_pick",
        "visible": "ally",
        "type": "text",
        "initial": "none"
      }
    ],
    "game": [
      {
        "key": "set_number",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "round_in_set",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "round_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "leader_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "named_role",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "led_list",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "leader_holds",
        "visible": "none",
        "type": "bool",
        "initial": false
      },
      {
        "key": "final_claimant",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "thief_target",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "roles",
        "visible": "none",
        "type": "list",
        "initial": [
          "Witch",
          "Raven Keeper",
          "Alchemist",
          "Druid",
          "Herb Hag",
          "Thief"
        ]
      },
      {
        "key": "name_offer",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "num_sets",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "roles_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "role_count",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "witch_strong",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "witch_weak",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "raven_keeper_strong",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "raven_keeper_weak",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "alchemist_strong",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "alchemist_weak",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "druid_strong",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "druid_weak",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "herb_hag_strong",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "herb_hag_weak",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "thief_steal",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "thief_weak",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "starting_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "overtaken_reward",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the starting state",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "starting_score"
            }
          }
        },
        {
          "set": {
            "key": "set_number",
            "value": 1
          }
        },
        {
          "set": {
            "key": "round_in_set",
            "value": 1
          }
        },
        {
          "set": {
            "key": "round_count",
            "value": 0
          }
        },
        {
          "set": {
            "key": "led_list",
            "value": []
          }
        },
        {
          "set": {
            "key": "named_role",
            "value": "none yet"
          }
        }
      ]
    },
    {
      "use": "sync",
      "label": "the table",
      "mode": "self",
      "to": "all",
      "fields": [
        "score"
      ],
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "set start",
      "label": "a new set begins",
      "when": {
        "calc": "round_in_set == 1"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "set_pick",
            "value": "none"
          }
        },
        {
          "set": {
            "key": "led_list",
            "value": []
          }
        }
      ],
      "text": "Set {set_number} of {num_sets} begins. All unused roles are lost and no role has been led yet."
    },
    {
      "use": "poll",
      "phase": "set start",
      "label": "choose roles",
      "when": {
        "calc": "round_in_set == 1"
      },
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": [
          "Witch + Raven Keeper + Alchemist",
          "Witch + Raven Keeper + Druid",
          "Witch + Raven Keeper + Herb Hag",
          "Witch + Raven Keeper + Thief",
          "Witch + Alchemist + Druid",
          "Witch + Alchemist + Herb Hag",
          "Witch + Alchemist + Thief",
          "Witch + Druid + Herb Hag",
          "Witch + Druid + Thief",
          "Witch + Herb Hag + Thief",
          "Raven Keeper + Alchemist + Druid",
          "Raven Keeper + Alchemist + Herb Hag",
          "Raven Keeper + Alchemist + Thief",
          "Raven Keeper + Druid + Herb Hag",
          "Raven Keeper + Druid + Thief",
          "Raven Keeper + Herb Hag + Thief",
          "Alchemist + Druid + Herb Hag",
          "Alchemist + Druid + Thief",
          "Alchemist + Herb Hag + Thief",
          "Druid + Herb Hag + Thief"
        ]
      },
      "store": "set_pick",
      "text": "Set {set_number}: secretly choose the {roles_per_hand} different roles you will hold for this set. Nobody else sees your hand."
    },
    {
      "use": "update",
      "phase": "set start",
      "label": "hands are set",
      "when": {
        "calc": "round_in_set == 1"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "[r for r in roles if r in you.set_pick]"
            }
          }
        }
      ]
    },
    {
      "use": "sync",
      "phase": "set start",
      "label": "your hand",
      "when": {
        "calc": "round_in_set == 1"
      },
      "mode": "self",
      "to": "all",
      "fields": [
        "hand"
      ],
      "text": "Your hand for this set:"
    },
    {
      "use": "update",
      "phase": "lead",
      "label": "the leader",
      "do": [
        {
          "set": {
            "key": "leader_seat",
            "value": {
              "calc": "((set_number - 1) + (round_in_set - 1)) % len(players) + 1"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "response",
            "value": "none"
          }
        },
        {
          "set": {
            "key": "final_claimant",
            "value": 0
          }
        },
        {
          "set": {
            "key": "thief_target",
            "value": 0
          }
        },
        {
          "set": {
            "key": "name_offer",
            "value": {
              "calc": "[r for r in roles if r not in led_list]"
            }
          }
        }
      ],
      "text": "Seat {leader_seat} leads this round."
    },
    {
      "use": "ask",
      "phase": "lead",
      "label": "name a role",
      "to": {
        "where": "you.seat == leader_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "game": "name_offer"
        }
      },
      "verify": {
        "bind": "nr"
      },
      "text": "You lead. Name one role not yet led this set. You may name a role you do not hold, but if nobody contests and you do not hold it, you get nothing."
    },
    {
      "use": "update",
      "phase": "lead",
      "label": "the role is named",
      "do": [
        {
          "set": {
            "key": "named_role",
            "value": "$nr"
          }
        },
        {
          "append": {
            "key": "led_list",
            "value": "$nr"
          }
        },
        {
          "set": {
            "key": "leader_holds",
            "value": {
              "calc": "$nr in [p.hand for p in players if p.seat == leader_seat][0]"
            }
          }
        }
      ],
      "text": "Seat {leader_seat} names the {named_role}."
    },
    {
      "use": "poll",
      "phase": "talk",
      "label": "talk",
      "to": "acting",
      "answer": {
        "type": "text",
        "max_words": 40
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} says: {value}"
      },
      "text": "The {named_role} has been named by seat {leader_seat}. Say one short thing to the table. Nothing said binds anyone."
    },
    {
      "use": "poll",
      "phase": "respond",
      "label": "respond",
      "to": {
        "where": "you.seat != leader_seat and named_role in you.hand"
      },
      "answer": {
        "type": "choice",
        "options": [
          "contest",
          "yield"
        ]
      },
      "store": "response",
      "text": "You hold the {named_role}, named by seat {leader_seat}. Contest to take over the claim (the last contester clockwise after the leader gets the strong reward; anyone overtaken gets 0), or yield to take the weak reward. Either way the role leaves your hand."
    },
    {
      "use": "tell",
      "phase": "reveal",
      "label": "the reveal",
      "to": "all",
      "text": "Responses to the {named_role} [seat, response]: {[[p.seat, p.response] for p in players]}."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "the final claimant",
      "do": [
        {
          "set": {
            "key": "final_claimant",
            "value": {
              "calc": "(max([((p.seat - leader_seat + len(players)) % len(players)) * 10 + p.seat for p in players if p.response == 'contest']) % 10) if count(p.response == 'contest' for p in players) > 0 else leader_seat"
            }
          }
        }
      ],
      "text": "Seat {final_claimant} holds the final claim on the {named_role}."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "the strong reward",
      "do": [
        {
          "adjust": {
            "player": {
              "calc": "final_claimant"
            },
            "key": "score",
            "value": {
              "calc": "witch_strong if named_role == 'Witch' else (raven_keeper_strong if named_role == 'Raven Keeper' else (alchemist_strong if named_role == 'Alchemist' else (druid_strong if named_role == 'Druid' else herb_hag_strong)))"
            },
            "if": {
              "calc": "(final_claimant != leader_seat or leader_holds) and named_role != 'Thief'"
            },
            "text": "Seat {player} takes the strong reward of the {named_role}."
          }
        },
        {
          "set": {
            "key": "thief_target",
            "value": {
              "calc": "[p.seat for p in players if p.seat != final_claimant and p.score * 100 - ((p.seat - final_claimant + len(players)) % len(players)) == max([q.score * 100 - ((q.seat - final_claimant + len(players)) % len(players)) for q in players if q.seat != final_claimant])][0]"
            },
            "if": {
              "calc": "(final_claimant != leader_seat or leader_holds) and named_role == 'Thief'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "final_claimant"
            },
            "key": "score",
            "value": {
              "calc": "thief_steal"
            },
            "if": {
              "calc": "thief_target > 0"
            },
            "text": "Seat {player} steals {thief_steal} points as the Thief."
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "thief_target"
            },
            "key": "score",
            "value": {
              "calc": "-thief_steal"
            },
            "if": {
              "calc": "thief_target > 0"
            },
            "text": "Seat {player} is robbed of {thief_steal} points."
          }
        },
        {
          "adjust": {
            "players": {
              "where": "(you.seat == leader_seat or you.response == 'contest') and you.seat != final_claimant"
            },
            "key": "score",
            "value": {
              "calc": "overtaken_reward"
            },
            "text": "Seat {player} was overtaken and gets nothing."
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "the weak reward",
      "do": [
        {
          "adjust": {
            "players": {
              "where": "you.response == 'yield'"
            },
            "key": "score",
            "value": {
              "calc": "witch_weak if named_role == 'Witch' else (raven_keeper_weak if named_role == 'Raven Keeper' else (alchemist_weak if named_role == 'Alchemist' else (druid_weak if named_role == 'Druid' else (herb_hag_weak if named_role == 'Herb Hag' else thief_weak))))"
            },
            "text": "Seat {player} yields and takes the weak reward of the {named_role}."
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "the role is spent",
      "do": [
        {
          "remove": {
            "players": {
              "where": "(you.seat == leader_seat or you.response != 'none') and named_role in you.hand"
            },
            "key": "hand",
            "value": {
              "calc": "named_role"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "next round",
      "do": [
        {
          "adjust": {
            "key": "round_count",
            "value": 1
          }
        },
        {
          "adjust": {
            "key": "round_in_set",
            "value": 1
          }
        },
        {
          "adjust": {
            "key": "set_number",
            "value": 1,
            "if": {
              "calc": "round_in_set > len(players)"
            }
          }
        },
        {
          "set": {
            "key": "round_in_set",
            "value": 1,
            "if": {
              "calc": "round_in_set > len(players)"
            }
          }
        }
      ],
      "text": "Scores [seat, score]: {[[p.seat, p.score] for p in players]}."
    },
    {
      "use": "check",
      "phase": "resolve",
      "label": "after the last round",
      "when": {
        "calc": "round_count >= num_sets * len(players)"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round_count >= num_sets * len(players)"
      },
      "rank_by": "you.score",
      "text": "Winner: {result}. Final scores [seat, score]: {[[p.seat, p.score] for p in players]}."
    }
  },
  "limits": {
    "rounds": 15,
    "rounds_max": 15,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "Players sit in a fixed clockwise order, numbered 1 to N. Everyone starts with {starting_score} points. The game has {num_sets} sets of N rounds each.\n\nROLES. There are {role_count} roles, each with a strong reward and a weak reward:\n- Witch: strong {witch_strong}, weak {witch_weak}.\n- Raven Keeper: strong {raven_keeper_strong}, weak {raven_keeper_weak}.\n- Alchemist: strong {alchemist_strong}, weak {alchemist_weak}.\n- Druid: strong {druid_strong}, weak {druid_weak}.\n- Herb Hag: strong {herb_hag_strong}, weak {herb_hag_weak}.\n- Thief: the strong reward is to take {thief_steal} points from the other player with the highest current total (ties go to the tied player first clockwise after the Thief). The Thief gains {thief_steal}, that player loses {thief_steal}, and a total may go below 0. Weak {thief_weak}.\n\nSTART OF A SET. At the start of each set, every player secretly and simultaneously chooses exactly {roles_per_hand} different roles to hold for that set, replacing anything left from the previous set. Hands are private. The list of roles led this set is emptied.\n\nLEADER. In set k, the first round's leader is player k. Leadership then passes clockwise each round, so every player leads exactly once per set.\n\nEACH ROUND:\n1. The leader is announced.\n2. The leader names one role that has not yet been led in this set. They may name a role they do not hold. The named role is added to this set's led list.\n3. Talk: every player at the same time writes one short message without seeing the others. All messages are then shown to everyone. Messages bind no one.\n4. Responses: every player other than the leader who holds the named role must respond. All of them choose at the same moment, either CONTEST or YIELD. Players who do not hold it pass automatically (response none).\n5. Reveal: all responses are shown, so everyone learns who held the role.\n6. Resolve: start from the leader and go clockwise. The leader is the first claimant, and each contester, in clockwise order, takes over the claim. The final claimant is the last contester in clockwise order after the leader, or the leader if nobody contested.\n   - The final claimant gets the role's strong reward. Exception: if the final claimant is the leader and the leader does not hold the named role, they get nothing, and nobody gets the strong reward.\n   - The leader, if overtaken, gets {overtaken_reward}. Every contester overtaken by a later contester gets {overtaken_reward}.\n   - Every player who yielded gets the role's weak reward, whether or not anyone contested.\n7. The named role is removed from the hand of the leader (if held) and of every responder. A role cannot be led again this set.\n8. Scores are announced and leadership passes clockwise.\n\nRoles held but never led or responded to during a set are simply lost when the set ends. After round {num_sets} x N the game ends: the player with the highest total points wins, and players tied for the highest total share the result (a draw)."
}
```

Why it was refused: it plays, but part of it does nothing: game attribute `roles` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "witchs_brew_claims",
    "name": "Witch's Brew: Claims",
    "players": {
      "min": 3,
      "max": 5,
      "suggested": 4
    },
    "blurb": "Over 3 sets, secretly hold 3 of 6 roles; leaders name roles, holders contest or yield, and the last contester clockwise takes the strong reward."
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
        "key": "response",
        "visible": "public",
        "type": "text",
        "initial": "none"
      },
      {
        "key": "set_pick",
        "visible": "ally",
        "type": "text",
        "initial": "none"
      }
    ],
    "game": [
      {
        "key": "set_number",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "round_in_set",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "round_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "leader_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "named_role",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "led_list",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "leader_holds",
        "visible": "none",
        "type": "bool",
        "initial": false
      },
      {
        "key": "final_claimant",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "thief_target",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "name_offer",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "num_sets",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "roles_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "role_count",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "witch_strong",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "witch_weak",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "raven_keeper_strong",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "raven_keeper_weak",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "alchemist_strong",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "alchemist_weak",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "druid_strong",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "druid_weak",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "herb_hag_strong",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "herb_hag_weak",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "thief_steal",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "thief_weak",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "starting_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "overtaken_reward",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the starting state",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "starting_score"
            }
          }
        },
        {
          "set": {
            "key": "set_number",
            "value": 1
          }
        },
        {
          "set": {
            "key": "round_in_set",
            "value": 1
          }
        },
        {
          "set": {
            "key": "round_count",
            "value": 0
          }
        },
        {
          "set": {
            "key": "led_list",
            "value": []
          }
        },
        {
          "set": {
            "key": "named_role",
            "value": "none yet"
          }
        }
      ]
    },
    {
      "use": "sync",
      "label": "the table",
      "mode": "self",
      "to": "all",
      "fields": [
        "score"
      ],
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "set start",
      "label": "a new set begins",
      "when": {
        "calc": "round_in_set == 1"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "set_pick",
            "value": "none"
          }
        },
        {
          "set": {
            "key": "led_list",
            "value": []
          }
        }
      ],
      "text": "Set {set_number} of {num_sets} begins. All unused roles are lost and no role has been led yet."
    },
    {
      "use": "poll",
      "phase": "set start",
      "label": "choose roles",
      "when": {
        "calc": "round_in_set == 1"
      },
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": [
          "Witch + Raven Keeper + Alchemist",
          "Witch + Raven Keeper + Druid",
          "Witch + Raven Keeper + Herb Hag",
          "Witch + Raven Keeper + Thief",
          "Witch + Alchemist + Druid",
          "Witch + Alchemist + Herb Hag",
          "Witch + Alchemist + Thief",
          "Witch + Druid + Herb Hag",
          "Witch + Druid + Thief",
          "Witch + Herb Hag + Thief",
          "Raven Keeper + Alchemist + Druid",
          "Raven Keeper + Alchemist + Herb Hag",
          "Raven Keeper + Alchemist + Thief",
          "Raven Keeper + Druid + Herb Hag",
          "Raven Keeper + Druid + Thief",
          "Raven Keeper + Herb Hag + Thief",
          "Alchemist + Druid + Herb Hag",
          "Alchemist + Druid + Thief",
          "Alchemist + Herb Hag + Thief",
          "Druid + Herb Hag + Thief"
        ]
      },
      "store": "set_pick",
      "text": "Set {set_number}: secretly choose the {roles_per_hand} different roles you will hold for this set. Nobody else sees your hand."
    },
    {
      "use": "update",
      "phase": "set start",
      "label": "hands are set",
      "when": {
        "calc": "round_in_set == 1"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "[r for r in ['Witch', 'Raven Keeper', 'Alchemist', 'Druid', 'Herb Hag', 'Thief'] if r in you.set_pick]"
            }
          }
        }
      ]
    },
    {
      "use": "sync",
      "phase": "set start",
      "label": "your hand",
      "when": {
        "calc": "round_in_set == 1"
      },
      "mode": "self",
      "to": "all",
      "fields": [
        "hand"
      ],
      "text": "Your hand for this set:"
    },
    {
      "use": "update",
      "phase": "lead",
      "label": "the leader",
      "do": [
        {
          "set": {
            "key": "leader_seat",
            "value": {
              "calc": "((set_number - 1) + (round_in_set - 1)) % len(players) + 1"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "response",
            "value": "none"
          }
        },
        {
          "set": {
            "key": "final_claimant",
            "value": 0
          }
        },
        {
          "set": {
            "key": "thief_target",
            "value": 0
          }
        },
        {
          "set": {
            "key": "name_offer",
            "value": {
              "calc": "[r for r in ['Witch', 'Raven Keeper', 'Alchemist', 'Druid', 'Herb Hag', 'Thief'] if r not in led_list]"
            }
          }
        }
      ],
      "text": "Seat {leader_seat} leads this round."
    },
    {
      "use": "ask",
      "phase": "lead",
      "label": "name a role",
      "to": {
        "where": "you.seat == leader_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "game": "name_offer"
        }
      },
      "verify": {
        "bind": "nr"
      },
      "text": "You lead. Name one role not yet led this set. You may name a role you do not hold, but if nobody contests and you do not hold it, you get nothing."
    },
    {
      "use": "update",
      "phase": "lead",
      "label": "the role is named",
      "do": [
        {
          "set": {
            "key": "named_role",
            "value": "$nr"
          }
        },
        {
          "append": {
            "key": "led_list",
            "value": "$nr"
          }
        },
        {
          "set": {
            "key": "leader_holds",
            "value": {
              "calc": "$nr in [p.hand for p in players if p.seat == leader_seat][0]"
            }
          }
        }
      ],
      "text": "Seat {leader_seat} names the {named_role}."
    },
    {
      "use": "poll",
      "phase": "talk",
      "label": "talk",
      "to": "acting",
      "answer": {
        "type": "text",
        "max_words": 40
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} says: {value}"
      },
      "text": "The {named_role} has been named by seat {leader_seat}. Say one short thing to the table. Nothing said binds anyone."
    },
    {
      "use": "poll",
      "phase": "respond",
      "label": "respond",
      "to": {
        "where": "you.seat != leader_seat and named_role in you.hand"
      },
      "answer": {
        "type": "choice",
        "options": [
          "contest",
          "yield"
        ]
      },
      "store": "response",
      "text": "You hold the {named_role}, named by seat {leader_seat}. Contest to take over the claim (the last contester clockwise after the leader gets the strong reward; anyone overtaken gets 0), or yield to take the weak reward. Either way the role leaves your hand."
    },
    {
      "use": "tell",
      "phase": "reveal",
      "label": "the reveal",
      "to": "all",
      "text": "Responses to the {named_role} [seat, response]: {[[p.seat, p.response] for p in players]}."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "the final claimant",
      "do": [
        {
          "set": {
            "key": "final_claimant",
            "value": {
              "calc": "(max([((p.seat - leader_seat + len(players)) % len(players)) * 10 + p.seat for p in players if p.response == 'contest']) % 10) if count(p.response == 'contest' for p in players) > 0 else leader_seat"
            }
          }
        }
      ],
      "text": "Seat {final_claimant} holds the final claim on the {named_role}."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "the strong reward",
      "do": [
        {
          "adjust": {
            "player": {
              "calc": "final_claimant"
            },
            "key": "score",
            "value": {
              "calc": "witch_strong if named_role == 'Witch' else (raven_keeper_strong if named_role == 'Raven Keeper' else (alchemist_strong if named_role == 'Alchemist' else (druid_strong if named_role == 'Druid' else herb_hag_strong)))"
            },
            "if": {
              "calc": "(final_claimant != leader_seat or leader_holds) and named_role != 'Thief'"
            },
            "text": "Seat {player} takes the strong reward of the {named_role}."
          }
        },
        {
          "set": {
            "key": "thief_target",
            "value": {
              "calc": "[p.seat for p in players if p.seat != final_claimant and p.score * 100 - ((p.seat - final_claimant + len(players)) % len(players)) == max([q.score * 100 - ((q.seat - final_claimant + len(players)) % len(players)) for q in players if q.seat != final_claimant])][0]"
            },
            "if": {
              "calc": "(final_claimant != leader_seat or leader_holds) and named_role == 'Thief'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "final_claimant"
            },
            "key": "score",
            "value": {
              "calc": "thief_steal"
            },
            "if": {
              "calc": "thief_target > 0"
            },
            "text": "Seat {player} steals {thief_steal} points as the Thief."
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "thief_target"
            },
            "key": "score",
            "value": {
              "calc": "-thief_steal"
            },
            "if": {
              "calc": "thief_target > 0"
            },
            "text": "Seat {player} is robbed of {thief_steal} points."
          }
        },
        {
          "adjust": {
            "players": {
              "where": "(you.seat == leader_seat or you.response == 'contest') and you.seat != final_claimant"
            },
            "key": "score",
            "value": {
              "calc": "overtaken_reward"
            },
            "text": "Seat {player} was overtaken and gets nothing."
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "the weak reward",
      "do": [
        {
          "adjust": {
            "players": {
              "where": "you.response == 'yield'"
            },
            "key": "score",
            "value": {
              "calc": "witch_weak if named_role == 'Witch' else (raven_keeper_weak if named_role == 'Raven Keeper' else (alchemist_weak if named_role == 'Alchemist' else (druid_weak if named_role == 'Druid' else (herb_hag_weak if named_role == 'Herb Hag' else thief_weak))))"
            },
            "text": "Seat {player} yields and takes the weak reward of the {named_role}."
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "the role is spent",
      "do": [
        {
          "remove": {
            "players": {
              "where": "(you.seat == leader_seat or you.response != 'none') and named_role in you.hand"
            },
            "key": "hand",
            "value": {
              "calc": "named_role"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "next round",
      "do": [
        {
          "adjust": {
            "key": "round_count",
            "value": 1
          }
        },
        {
          "adjust": {
            "key": "round_in_set",
            "value": 1
          }
        },
        {
          "adjust": {
            "key": "set_number",
            "value": 1,
            "if": {
              "calc": "round_in_set > len(players)"
            }
          }
        },
        {
          "set": {
            "key": "round_in_set",
            "value": 1,
            "if": {
              "calc": "round_in_set > len(players)"
            }
          }
        }
      ],
      "text": "Scores [seat, score]: {[[p.seat, p.score] for p in players]}."
    },
    {
      "use": "check",
      "phase": "resolve",
      "label": "after the last round",
      "when": {
        "calc": "round_count >= num_sets * len(players)"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round_count >= num_sets * len(players)"
      },
      "rank_by": "you.score",
      "text": "Winner: {result}. Final scores [seat, score]: {[[p.seat, p.score] for p in players]}."
    }
  },
  "limits": {
    "rounds": 15,
    "rounds_max": 15,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "Players sit in a fixed clockwise order, numbered 1 to N. Everyone starts with {starting_score} points. The game has {num_sets} sets of N rounds each.\n\nROLES. There are {role_count} roles, each with a strong reward and a weak reward:\n- Witch: strong {witch_strong}, weak {witch_weak}.\n- Raven Keeper: strong {raven_keeper_strong}, weak {raven_keeper_weak}.\n- Alchemist: strong {alchemist_strong}, weak {alchemist_weak}.\n- Druid: strong {druid_strong}, weak {druid_weak}.\n- Herb Hag: strong {herb_hag_strong}, weak {herb_hag_weak}.\n- Thief: the strong reward is to take {thief_steal} points from the other player with the highest current total (ties go to the tied player first clockwise after the Thief). The Thief gains {thief_steal}, that player loses {thief_steal}, and a total may go below 0. Weak {thief_weak}.\n\nSTART OF A SET. At the start of each set, every player secretly and simultaneously chooses exactly {roles_per_hand} different roles to hold for that set, replacing anything left from the previous set. Hands are private. The list of roles led this set is emptied.\n\nLEADER. In set k, the first round's leader is player k. Leadership then passes clockwise each round, so every player leads exactly once per set.\n\nEACH ROUND:\n1. The leader is announced.\n2. The leader names one role that has not yet been led in this set. They may name a role they do not hold. The named role is added to this set's led list.\n3. Talk: every player at the same time writes one short message without seeing the others. All messages are then shown to everyone. Messages bind no one.\n4. Responses: every player other than the leader who holds the named role must respond. All of them choose at the same moment, either CONTEST or YIELD. Players who do not hold it pass automatically (response none).\n5. Reveal: all responses are shown, so everyone learns who held the role.\n6. Resolve: start from the leader and go clockwise. The leader is the first claimant, and each contester, in clockwise order, takes over the claim. The final claimant is the last contester in clockwise order after the leader, or the leader if nobody contested.\n   - The final claimant gets the role's strong reward. Exception: if the final claimant is the leader and the leader does not hold the named role, they get nothing, and nobody gets the strong reward.\n   - The leader, if overtaken, gets {overtaken_reward}. Every contester overtaken by a later contester gets {overtaken_reward}.\n   - Every player who yielded gets the role's weak reward, whether or not anyone contested.\n7. The named role is removed from the hand of the leader (if held) and of every responder. A role cannot be led again this set.\n8. Scores are announced and leadership passes clockwise.\n\nRoles held but never led or responded to during a set are simply lost when the set ends. After round {num_sets} x N the game ends: the player with the highest total points wins, and players tied for the highest total share the result (a draw)."
}
```
````
