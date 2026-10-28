# 07 coder

- time: 2026-10-28T03:37:04+00:00 (85.6s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 fd838efafb4a818b, reply sha256 d3def707ec7acf56

## Sent

````
# Task: write the XColos game file for "Sedmice Duel"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 2; set `meta.players` to {"min": 2, "max": 2, "suggested": 2} (the suggested size is the one the game plays best at).

CARDS: 32 cards, four each of the ranks 7, 8, 9, 10, J, Q, K, A. Suits do not matter. Aces and Tens are point cards worth 10 each. Sevens are wild.

MATCH: 4 deals. Each deal lasts up to 8 rounds, so the match has 32 rounds. Each round is one trick.

DEALING (first round of each deal): Shuffle the full deck. Each player receives exactly one Seven, one Ace and one Ten. Shuffle the remaining 26 cards and deal 5 more to each player, so each hand has 8 cards. Hands are private. The 16 undealt cards are set aside face down and are never revealed or used in that deal. Both players know the dealing rule.

FIRST LEAD: Player A leads first in deals 1 and 3. Player B leads first in deals 2 and 4. After that, the winner of each trick leads the next one.

A TRICK:
(1) The leader plays any card face up. Its rank is the 'led rank'.
(2) The follower plays any card face up. If it matches the led rank or is a Seven, the follower is currently winning. Otherwise the leader wins the trick and it ends.
(3) If the follower is currently winning, the leader may extend once by playing a second card that matches the led rank or is a Seven. The leader may also decline. If the leader declines or has no such card, the follower wins the trick.
(4) If the leader extended, the follower must play a second card (any card). If it matches the led rank or is a Seven, the follower wins the trick. Otherwise the leader wins.
A trick can never be extended more than once.

AFTER EACH TRICK: All cards played in the trick are announced. The winner scores 10 points for each Ace and each Ten among them. Both players always play the same number of cards, so both hands empty together. If the hands are now empty, the winner of this trick also scores 10 points for the last trick, and the deal ends. Any remaining rounds of that deal are skipped. A deal lasts 4 to 8 tricks.

INFORMATION: Each player sees their own hand and every card played. Neither sees the opponent's hand or the set-aside cards.

How the winner is decided: After 4 deals, the player with the higher total points across all deals wins. Equal totals are a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Sedmice Duel (2 to 2 players, best with 2)

A two-player trick-taking duel over 4 deals of 8-card hands. Sevens are wild, Aces and Tens score 10 each, and the leader may extend a trick once to win it back.

STATE (every item below must exist in the file):
  - each player: hand (list, starts []); only its owner sees it. Ranks of the cards this player holds in the current deal ('7','8','9','10','J','Q','K','A').
  - each player: score (number, starts 0); everyone sees it. Total points across all deals.
  - the table: deck (list, starts []); hidden from all players. Cards not yet dealt during dealing: 4 copies of each of 7,8,9,10,J,Q,K,A.
  - the table: set_aside (list, starts []); hidden from all players. The 16 undealt cards of the current deal. They are never revealed or used.
  - the table: deal_number (number, starts 1); everyone sees it. Current deal, from 1 to 4. It becomes 5 when the match is over.
  - the table: new_deal (bool, starts True); everyone sees it. True when the next trick is the first of a deal, so cards must be dealt.
  - the table: leader (number, starts 1); everyone sees it. Seat that leads the current trick (seat 1 = Player A, seat 2 = Player B).
  - the table: led_rank (text, starts ''); everyone sees it. Rank of the card the leader played first in this trick.
  - the table: follower_winning (bool, starts False); everyone sees it. Whether the follower is currently winning the trick.
  - the table: extended (bool, starts False); everyone sees it. Whether the leader extended this trick.
  - the table: trick_cards (list, starts []); everyone sees it. All cards played face up in the current trick.
  - the table: trick_winner (number, starts 0); everyone sees it. Seat that won the latest trick.
  - parameters, each kept as a table attribute: deck_size = 32, copies_per_rank = 4, point_card_value = 10, deals = 4, max_rounds_per_deal = 8, total_rounds = 32, guaranteed_cards_per_player = 3, extra_cards_dealt_per_player = 5, hand_size = 8, set_aside_cards = 16, last_trick_bonus = 10, max_extensions_per_trick = 1, min_tricks_per_deal = 4

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seat 1 is Player A and seat 2 is Player B.
  2. Both scores start at 0, deal_number is 1 and new_deal is true.
  3. Both players are told the dealing rule: each hand gets exactly one Seven, one Ace and one Ten, plus 5 random cards from the remaining 26.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: Set deck to the full 32 cards (four each of 7,8,9,10,J,Q,K,A). Set each hand to empty. For each player, move one '7', one 'A' and one '10' from deck to hand. Then draw 5 cards at random from deck into each hand, so each hand has 8 cards. Move the 16 remaining deck cards to set_aside. Set leader = 1 if deal_number is 1 or 3, else 2. Set new_deal = false.
  2. [sync] all players. What happens: Each player sees their own hand, both scores, deal_number and who leads.
  3. [ask] the leader (seat game.leader) answers: one card from your hand. What happens: Remove the card from the leader's hand, append it to trick_cards and set led_rank to its rank.
  4. [ask] the follower (the seat that is not game.leader) answers: one card from your hand. What happens: Remove the card from the follower's hand and append it to trick_cards. Set follower_winning = (card == led_rank or card == '7').
  5. [ask] the leader (seat game.leader) answers: decline, or one card from your hand whose rank is led_rank or '7'. What happens: If a card is chosen: remove it from the leader's hand, append it to trick_cards and set extended = true. If declined: nothing changes.
  6. [ask] the follower (the seat that is not game.leader) answers: one card from your hand. What happens: Remove the card from the follower's hand and append it to trick_cards. Set follower_winning = (card == led_rank or card == '7').
  7. [update] all players. What happens: Set trick_winner = the follower if follower_winning is true, else leader. The trick winner's score += 10 × (count of 'A' in trick_cards + count of '10' in trick_cards). Announce trick_cards, the winner and the points scored.
  8. [update] all players. What happens: If both hands are empty: the trick winner's score += last_trick_bonus (10), clear set_aside, deal_number += 1 and new_deal = true. Otherwise leader = trick_winner. Announce the result.
  9. [update] all players. What happens: Reset for the next trick: trick_cards = [], led_rank = '', follower_winning = false, extended = false.
  10. [check] all players. What happens: End the game if deal_number > 4; otherwise continue.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. The deck has 32 cards, four each of 7, 8, 9, 10, J, Q, K and A, and suits do not matter.
  R2. When a deal starts, each player receives exactly one 7, one A and one 10, then 5 random cards from the remaining 26, for a hand of 8.
  R3. When a deal has been dealt, the 16 undealt cards go to set_aside and are never revealed or played that deal.
  R4. When deal 1 or deal 3 starts, seat 1 (Player A) leads the first trick. When deal 2 or deal 4 starts, seat 2 (Player B) leads.
  R5. When a trick ends without emptying the hands, the trick winner leads the next trick.
  R6. When the leader plays the first card, its rank becomes led_rank, and the leader may play any card in hand.
  R7. When the follower's first card is neither led_rank nor a 7, the leader wins the trick immediately with 2 cards played.
  R8. When the follower's first card is led_rank or a 7, the follower is currently winning.
  R9. When the follower is currently winning and the leader holds a led_rank card or a 7, the leader may extend by playing one such card, or may decline.
  R10. When the follower is currently winning and the leader declines or holds no led_rank card and no 7, the follower wins the trick.
  R11. When the leader extends, the follower must play a second card from hand (any card).
  R12. When the follower's second card is led_rank or a 7, the follower wins the trick; otherwise the leader wins.
  R13. A trick is extended at most once, so each player plays at most 2 cards in a trick.
  R14. When a trick ends, all of its cards are announced and the winner scores 10 points for each A and each 10 among them.
  R15. When a trick empties both hands, its winner scores an extra 10 points for the last trick and the deal ends.
  R16. Both players play the same number of cards in every trick, so a deal lasts between 4 and 8 tricks and the remaining rounds of that deal are skipped.
  R17. When deal 4 ends (deal_number reaches 5), the game ends and the higher score wins; equal scores are a draw.
  R18. Each player sees only their own hand and the cards played, never the opponent's hand or the set-aside cards.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Leader's first card | asked: seat game.leader | options: every card currently in the leader's hand
  - Follower's first card | asked: the seat that is not game.leader | options: every card currently in the follower's hand
  - Leader's extension | asked: seat game.leader, only when the follower is currently winning and the leader holds a led_rank card or a 7 | options: decline, plus each card in the leader's hand whose rank is led_rank or '7'
  - Follower's second card | asked: the seat that is not game.leader, only when the leader extended | options: every card currently in the follower's hand

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: game.deal_number > 4
  - each player's standing: you.score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their total points across the 4 deals. The higher total wins, and equal totals share the win (a draw).
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

- each player: `score` (number, visible: public, starts 0): Total points across all deals.
- the table: `deal_number` (number, visible: public, starts 1): Current deal, from 1 to 4. It becomes 5 when the match is over.
- the table: `trick_cards` (list, visible: public, starts []): All cards played face up in the current trick.
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 32, copies_per_rank = 4, point_card_value = 10, deals = 4, max_rounds_per_deal = 8, total_rounds = 32, guaranteed_cards_per_player = 3, extra_cards_dealt_per_player = 5, hand_size = 8, set_aside_cards = 16, last_trick_bonus = 10, max_extensions_per_trick = 1, min_tricks_per_deal = 4
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

````

## Reply

````
{
  "schema": 1,
  "meta": {
    "id": "sedmice_duel",
    "name": "Sedmice Duel",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "blurb": "A two-player trick-taking duel over 4 deals: Sevens are wild, Aces and Tens score 10, and the leader may extend a trick once to win it back."
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
        "key": "hand",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      }
    ],
    "game": [
      {
        "key": "full_deck",
        "visible": "none",
        "type": "list",
        "initial": [
          "7", "7", "7", "7",
          "8", "8", "8", "8",
          "9", "9", "9", "9",
          "10", "10", "10", "10",
          "J", "J", "J", "J",
          "Q", "Q", "Q", "Q",
          "K", "K", "K", "K",
          "A", "A", "A", "A"
        ]
      },
      {
        "key": "deck",
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
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "deal_number",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "new_deal",
        "visible": "public",
        "type": "bool",
        "initial": true
      },
      {
        "key": "leader",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "led_rank",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "follower_winning",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "extended",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "trick_cards",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "trick_winner",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "trick_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 32
      },
      {
        "key": "copies_per_rank",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "point_card_value",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "deals",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "max_rounds_per_deal",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "total_rounds",
        "visible": "public",
        "type": "number",
        "initial": 32
      },
      {
        "key": "guaranteed_cards_per_player",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "extra_cards_dealt_per_player",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "hand_size",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "set_aside_cards",
        "visible": "public",
        "type": "number",
        "initial": 16
      },
      {
        "key": "last_trick_bonus",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "max_extensions_per_trick",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "min_tricks_per_deal",
        "visible": "public",
        "type": "number",
        "initial": 4
      }
    ]
  },
  "setup": [
    {
      "use": "tell",
      "label": "the seats",
      "to": "all",
      "text": "Seat 1 is Player A and seat 2 is Player B."
    },
    {
      "use": "update",
      "label": "the starting state",
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
            "key": "deal_number",
            "value": 1
          }
        },
        {
          "set": {
            "key": "new_deal",
            "value": true
          }
        }
      ]
    },
    {
      "use": "tell",
      "label": "the dealing rule",
      "to": "all",
      "text": "The dealing rule: each deal, each hand gets exactly one Seven, one Ace and one Ten, plus {extra_cards_dealt_per_player} random cards from the remaining 26, for {hand_size} cards. The other {set_aside_cards} cards are set aside face down and never used that deal."
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "deal",
      "label": "the deal",
      "when": {
        "calc": "new_deal"
      },
      "do": [
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "full_deck"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": []
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hand",
            "value": "7"
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": "7"
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hand",
            "value": "A"
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": "A"
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hand",
            "value": "10"
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": "10"
          }
        },
        {
          "append": {
            "player": 2,
            "key": "hand",
            "value": "7"
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": "7"
          }
        },
        {
          "append": {
            "player": 2,
            "key": "hand",
            "value": "A"
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": "A"
          }
        },
        {
          "append": {
            "player": 2,
            "key": "hand",
            "value": "10"
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": "10"
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "set_aside",
            "value": {
              "calc": "deck"
            }
          }
        },
        {
          "set": {
            "key": "deck",
            "value": []
          }
        },
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "1 if deal_number % 2 == 1 else 2"
            }
          }
        },
        {
          "set": {
            "key": "new_deal",
            "value": false
          }
        }
      ],
      "text": "Deal {deal_number} of {deals} has been dealt: {hand_size} cards each, {set_aside_cards} set aside face down. Seat {leader} leads the first trick."
    },
    {
      "use": "sync",
      "phase": "trick",
      "label": "your hand",
      "mode": "self",
      "to": "all",
      "text": "Your state before this trick:"
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "leader's first card",
      "to": {
        "where": "you.seat == leader"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "each": {
        "do": [
          {
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": "$answer"
            }
          },
          {
            "append": {
              "key": "trick_cards",
              "value": "$answer"
            }
          },
          {
            "set": {
              "key": "led_rank",
              "value": "$answer"
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} leads {value}."
      },
      "text": "You lead this trick. Play any card from your hand face up; its rank becomes the led rank."
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "follower's first card",
      "to": {
        "where": "you.seat != leader"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "each": {
        "do": [
          {
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": "$answer"
            }
          },
          {
            "append": {
              "key": "trick_cards",
              "value": "$answer"
            }
          },
          {
            "set": {
              "key": "follower_winning",
              "value": {
                "calc": "$answer == led_rank or $answer == '7'"
              }
            }
          },
          {
            "set": {
              "players": "all",
              "key": "offer",
              "value": {
                "calc": "['decline'] + (['7'] if '7' in you.hand else []) + ([led_rank] if (led_rank != '7' and led_rank in you.hand) else [])"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} follows with {value}."
      },
      "text": "Seat {leader} led {led_rank}. Play any card from your hand face up. If it is {led_rank} or a 7 you are currently winning; otherwise the leader wins the trick."
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "leader's extension",
      "when": {
        "calc": "follower_winning and any(p.seat == leader and len(p.offer) > 1 for p in players)"
      },
      "to": {
        "where": "you.seat == leader"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "each": {
        "do": [
          {
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": "$answer",
              "if": {
                "calc": "$answer != 'decline'"
              }
            }
          },
          {
            "append": {
              "key": "trick_cards",
              "value": "$answer",
              "if": {
                "calc": "$answer != 'decline'"
              }
            }
          },
          {
            "set": {
              "key": "extended",
              "value": true,
              "if": {
                "calc": "$answer != 'decline'"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} extension: {value}."
      },
      "text": "The follower is currently winning. You may extend once by playing a {led_rank} or a 7, or decline. If you decline, the follower wins the trick. If you extend, the follower must play a second card: if it is {led_rank} or a 7 the follower wins, otherwise you win."
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "follower's second card",
      "when": {
        "calc": "extended"
      },
      "to": {
        "where": "you.seat != leader"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "each": {
        "do": [
          {
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": "$answer"
            }
          },
          {
            "append": {
              "key": "trick_cards",
              "value": "$answer"
            }
          },
          {
            "set": {
              "key": "follower_winning",
              "value": {
                "calc": "$answer == led_rank or $answer == '7'"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} plays a second card: {value}."
      },
      "text": "The leader extended. You must play a second card (any card). If it is {led_rank} or a 7 you win the trick; otherwise the leader wins."
    },
    {
      "use": "update",
      "phase": "score",
      "label": "the trick is won",
      "do": [
        {
          "set": {
            "key": "trick_winner",
            "value": {
              "calc": "[p.seat for p in players if p.seat != leader][0] if follower_winning else leader"
            }
          }
        },
        {
          "set": {
            "key": "trick_points",
            "value": {
              "calc": "point_card_value * (count(c == 'A' for c in trick_cards) + count(c == '10' for c in trick_cards))"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "trick_winner"
            },
            "key": "score",
            "value": {
              "calc": "trick_points"
            }
          }
        }
      ],
      "text": "Trick cards: {trick_cards}. Seat {trick_winner} wins the trick and scores {trick_points} points."
    },
    {
      "use": "update",
      "phase": "score",
      "label": "after the trick",
      "do": [
        {
          "adjust": {
            "player": {
              "calc": "trick_winner"
            },
            "key": "score",
            "value": {
              "calc": "last_trick_bonus"
            },
            "if": {
              "calc": "all(len(p.hand) == 0 for p in players)"
            },
            "text": "Both hands are empty: seat {player} scores {last_trick_bonus} for the last trick, and deal {deal_number} ends."
          }
        },
        {
          "set": {
            "key": "set_aside",
            "value": [],
            "if": {
              "calc": "all(len(p.hand) == 0 for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "new_deal",
            "value": true,
            "if": {
              "calc": "all(len(p.hand) == 0 for p in players)"
            }
          }
        },
        {
          "adjust": {
            "key": "deal_number",
            "value": 1,
            "if": {
              "calc": "all(len(p.hand) == 0 for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "trick_winner"
            },
            "if": {
              "calc": "any(len(p.hand) > 0 for p in players)"
            },
            "text": "Seat {value} leads the next trick."
          }
        }
      ],
      "text": "Scores: seat 1 {players[0].score}, seat 2 {players[1].score}."
    },
    {
      "use": "update",
      "phase": "score",
      "label": "reset the trick",
      "do": [
        {
          "set": {
            "key": "trick_cards",
            "value": []
          }
        },
        {
          "set": {
            "key": "led_rank",
            "value": ""
          }
        },
        {
          "set": {
            "key": "follower_winning",
            "value": false
          }
        },
        {
          "set": {
            "key": "extended",
            "value": false
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "score",
      "label": "after the last deal",
      "when": {
        "calc": "deal_number > deals"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "deal_number > deals"
      },
      "rank_by": "you.score",
      "text": "Winner: {result}. Final scores: Seat 1 {players[0].score}, Seat 2 {players[1].score}."
    }
  },
  "limits": {
    "rounds": 32,
    "rounds_max": 32,
    "actions_max": 1000,
    "deadline_s": 120
  },
  "rules": "Sedmice Duel is played with {deck_size} cards: {copies_per_rank} each of the ranks 7, 8, 9, 10, J, Q, K, A. Suits do not matter. Aces and Tens are point cards worth {point_card_value} each. Sevens are wild. Seat 1 is Player A and seat 2 is Player B.\n\nThe match is {deals} deals. Each deal lasts up to {max_rounds_per_deal} rounds, so the match has {total_rounds} rounds; each round is one trick.\n\nDEALING (first round of each deal): the full deck is shuffled. Each player receives exactly one Seven, one Ace and one Ten, then {extra_cards_dealt_per_player} more random cards from the remaining 26, so each hand has {hand_size} cards. Hands are private. The {set_aside_cards} undealt cards are set aside face down and are never revealed or used in that deal.\n\nFIRST LEAD: Player A (seat 1) leads first in deals 1 and 3. Player B (seat 2) leads first in deals 2 and 4. After that, the winner of each trick leads the next one.\n\nA TRICK:\n(1) The leader plays any card face up. Its rank is the led rank.\n(2) The follower plays any card face up. If it matches the led rank or is a Seven, the follower is currently winning. Otherwise the leader wins the trick and it ends.\n(3) If the follower is currently winning, the leader may extend once by playing a second card that matches the led rank or is a Seven. The leader may also decline. If the leader declines or has no such card, the follower wins the trick.\n(4) If the leader extended, the follower must play a second card (any card). If it matches the led rank or is a Seven, the follower wins the trick. Otherwise the leader wins.\nA trick can never be extended more than {max_extensions_per_trick} time.\n\nAFTER EACH TRICK: all cards played in the trick are announced. The winner scores {point_card_value} points for each Ace and each Ten among them. Both players always play the same number of cards, so both hands empty together. If the hands are now empty, the winner of this trick also scores {last_trick_bonus} points for the last trick, and the deal ends; any remaining rounds of that deal are skipped. A deal lasts {min_tricks_per_deal} to {max_rounds_per_deal} tricks.\n\nINFORMATION: each player sees their own hand and every card played. Neither sees the opponent's hand or the set-aside cards.\n\nAfter {deals} deals, the player with the higher total points wins. Equal totals are a draw (a shared win)."
}
````
