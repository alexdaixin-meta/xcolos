# Task: write the XColos game file for "Put: Twelve Hands"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 2; set `meta.players` to {"min": 2, "max": 2, "suggested": 2} (the suggested size is the one the game plays best at).

CARDS. Use a standard 52-card deck. Suits do not matter. Ranks from highest to lowest are: 3, 2, A, K, Q, J, 10, 9, 8, 7, 6, 5, 4.

MATCH. The match is exactly 12 hands. Both players start at 0 points. Seat 1 is the leader in hands 1, 3, 5, 7, 9 and 11. Seat 2 is the leader in hands 2, 4, 6, 8, 10 and 12. The other player is the responder.

EACH HAND:
1. Deal. Shuffle the full deck and deal 3 cards to each player. Each player's first dealt card is placed face up and both players see it. Each player's other two cards are private. Each player's hand is listed in the order dealt.
2. Leader's call. The leader chooses one of two options: Check, or Put.
3. Responder's action. If the leader chose Put, the responder chooses See ('I see it') or Fold. If the leader chose Check, the responder chooses Check or Put.
4. Leader's reply. This happens only if the leader checked and the responder put. The leader then chooses See or Fold.
5. Fold. If either player folded, the hand ends at once. The player who put scores 1 point, the folder scores 0, and no cards are played.
6. Card order. Otherwise, both players secretly and at the same moment choose an order for their three cards, naming which of their cards they will play first, second and third.
7. Tricks. Trick 1 compares both players' first cards, trick 2 their second cards, and trick 3 their third cards. The higher-ranked card wins the trick. Equal ranks tie the trick, and it counts for no one. Count each player's tricks won.
8. Scoring when nobody put (both checked). The player with more tricks scores 1 point. If tricks are equal, nobody scores.
9. Scoring when a Put was seen. The player who put scores 3 points if they won strictly more tricks than the opponent. Otherwise (equal tricks, or the opponent won more), the opponent scores 3 points.
10. Results. Reveal all cards, both orders, the trick results and the scores.

Only one Put can be made per hand. There is no re-raise. Talk is not part of the game.

How the winner is decided: After hand 12, the player with the higher total score wins. If the totals are equal, the match is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Put: Twelve Hands (2 to 2 players, best with 2)

Two players play 12 hands of three-card Put. Each hand they may check or Put, then see or fold, then secretly order their cards for three tricks. The higher total score wins.

STATE (every item below must exist in the file):
  - each player: score (number, starts 0); everyone sees it. Total points so far in the match
  - each player: hand (list, starts []); only its owner sees it. This hand's 3 cards in the order dealt, as rank values (4=1, 5=2, 6=3, 7=4, 8=5, 9=6, 10=7, J=8, Q=9, K=10, A=11, 2=12, 3=13)
  - each player: up_card (number, starts 0); everyone sees it. Rank value of the first dealt card, which is face up
  - each player: order (list, starts []); only its owner sees it. The player's 3 cards in the chosen play order. It is revealed at Results.
  - each player: tricks (number, starts 0); everyone sees it. Tricks won this hand
  - the table: deck (list, starts '52 cards: rank values 1 to 13, four of each'); hidden from all players. The shuffled deck that cards are dealt from
  - the table: hand_number (number, starts 0); everyone sees it. The current hand, from 1 to 12
  - the table: leader (number, starts 0); everyone sees it. Seat of the leader: 1 in odd hands, 2 in even hands
  - the table: leader_call (text, starts ''); everyone sees it. The leader's call: Check or Put
  - the table: responder_action (text, starts ''); everyone sees it. The responder's action: See, Fold, Check or Put
  - the table: leader_reply (text, starts ''); everyone sees it. The leader's reply to a responder Put: See or Fold. Empty if there was none.
  - the table: putter (number, starts 0); everyone sees it. Seat that made the Put this hand, or 0 if nobody put
  - the table: folded (bool, starts False); everyone sees it. Whether someone folded this hand
  - parameters, each kept as a table attribute: hands = 12, deck_size = 52, copies_per_rank = 4, ranks = 13, cards_per_player = 3, face_up_cards_per_player = 1, tricks_per_hand = 3, fold_points = 1, check_win_points = 1, put_seen_points = 3, start_score = 0, max_puts_per_hand = 1

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Both players' scores are set to 0.
  2. hand_number is set to 0.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: hand_number += 1; leader = 1 if hand_number is odd, else 2; deck is rebuilt as the full 52 cards (rank values 1 to 13, four each); each player's hand, order, tricks and up_card are reset; leader_call, responder_action and leader_reply are set to empty; putter = 0; folded = false
  2. [update] all players. What happens: Deal: 3 times for each player, a random card is removed from deck and appended to that player's hand. Each player's up_card = the first card of their hand.
  3. [sync] all players. What happens: Each player sees their own hand and both up_cards.
  4. [ask] the leader (seat 1 in odd hands, seat 2 in even hands) answers: one of: Check, Put. What happens: leader_call = answer; if Put, putter = leader
  5. [ask] the responder (the seat that is not the leader) answers: if leader_call = Put: one of See, Fold; if leader_call = Check: one of Check, Put. What happens: responder_action = answer; if answer = Put, putter = responder; if answer = Fold, folded = true
  6. [ask] the leader, only when leader_call = Check and responder_action = Put answers: one of: See, Fold. What happens: leader_reply = answer; if Fold, folded = true
  7. [update] all players. What happens: when folded = true: the putter's score += 1; the folder scores 0; no cards are played
  8. [poll] all players, only when folded = false answers: one of the 6 orders of the player's own three cards, by dealt position: 1-2-3, 1-3-2, 2-1-3, 2-3-1, 3-1-2, 3-2-1. What happens: Each player's order = their hand rearranged by the chosen permutation. Nobody sees the other's order until both are in.
  9. [update] all players. What happens: when folded = false: for each trick i from 1 to 3, the player whose order[i] is higher gets tricks += 1; equal values give no one a trick
  10. [update] all players. What happens: when folded = false and putter = 0: the player with more tricks scores += 1, and nobody scores if tricks are equal. When folded = false and putter > 0: if the putter's tricks > the opponent's tricks, the putter's score += 3; otherwise the opponent's score += 3.
  11. [tell] all players. What happens: Reveal both hands, both orders, each trick's result, tricks, points scored this hand and the total scores.
  12. [check] all players. What happens: End the game if hand_number = 12; otherwise continue to the next hand.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. Card ranks from highest to lowest are 3, 2, A, K, Q, J, 10, 9, 8, 7, 6, 5, 4, and suits do not matter.
  R2. The match is exactly 12 hands, and both players start at 0 points.
  R3. When hand_number is odd, seat 1 leads; when it is even, seat 2 leads.
  R4. Each hand, a full 52-card deck is shuffled and each player is dealt 3 cards, so the deck holds 46 after the deal.
  R5. Each player's first dealt card is visible to both players, and their other two cards are visible only to that player.
  R6. The leader chooses Check or Put.
  R7. When the leader puts, the responder chooses See or Fold.
  R8. When the leader checks, the responder chooses Check or Put.
  R9. When the leader checked and the responder put, the leader chooses See or Fold.
  R10. Only one Put is made per hand: a player facing a Put is never offered Put.
  R11. When a player folds, the putter scores 1 point, the folder scores 0, and no cards are played.
  R12. When nobody folded, both players secretly and at the same moment choose an order of their 3 cards.
  R13. Trick i compares the two players' i-th played cards: the higher rank wins the trick, and equal ranks give the trick to no one.
  R14. When both players checked, the player with more tricks scores 1 point, and equal tricks score nothing.
  R15. When a Put was seen and the putter won strictly more tricks, the putter scores 3 points.
  R16. When a Put was seen and the putter won equal or fewer tricks, the opponent scores 3 points.
  R17. At the end of each hand, all cards, both orders, the trick results and the scores are revealed.
  R18. After hand 12 the higher total score wins, and equal totals are a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Leader's call | asked: the leader | options: Check, Put
  - Responder's action | asked: the responder | options: if the leader put: See, Fold; if the leader checked: Check, Put
  - Leader's reply | asked: the leader, only after leader Check and responder Put | options: See, Fold
  - Card order | asked: both seats, only when nobody folded | options: 1-2-3, 1-3-2, 2-1-3, 2-3-1, 3-1-2, 3-2-1 (positions in the dealt order)

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: hand_number = 12
  - each player's standing: you.score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: After hand 12 the player with the higher total score wins; equal totals share the win, which is a draw.
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

- each player: `score` (number, visible: public, starts 0): Total points so far in the match
- each player: `up_card` (number, visible: public, starts 0): Rank value of the first dealt card, which is face up
- each player: `tricks` (number, visible: public, starts 0): Tricks won this hand
- the table: `hand_number` (number, visible: public, starts 0): The current hand, from 1 to 12
- the table: `leader` (number, visible: public, starts 0): Seat of the leader: 1 in odd hands, 2 in even hands
- the table: `leader_call` (text, visible: public, starts ''): The leader's call: Check or Put
- the table: `responder_action` (text, visible: public, starts ''): The responder's action: See, Fold, Check or Put
- the table: `leader_reply` (text, visible: public, starts ''): The leader's reply to a responder Put: See or Fold. Empty if there was none.
- the table: `putter` (number, visible: public, starts 0): Seat that made the Put this hand, or 0 if nobody put
- the table: `folded` (bool, visible: public, starts False): Whether someone folded this hand
- parameters (each must be an attribute holding this value, never a number buried in a step): hands = 12, deck_size = 52, copies_per_rank = 4, ranks = 13, cards_per_player = 3, face_up_cards_per_player = 1, tricks_per_hand = 3, fold_points = 1, check_win_points = 1, put_seen_points = 3, start_score = 0, max_puts_per_hand = 1
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

## Guidance from the last attempt

The previous attempt had problems:

Start from the attempt-5 file. Either delete `full_deck` (it is not in the interface) or make it do real work: the deck is reshuffled every hand, so each hand should rebuild the draw pile from `full_deck` (copy it, shuffle, deal 3 cards to each player by remove/append), and that step must actually change it. Keep the attempt-5 handling of the blank fields: at the start of each hand, set `leader_call`, `responder_action` and `leader_reply` to a visible non-empty value (such as 'none'), then overwrite them with the real choices. Mark any scratch attributes as hidden bookkeeping (`none` on the table, `ally` on a player), such as card orders, per-trick comparisons and deck piles. Do not reintroduce `{hand}` or any placeholder other than {value} and {seat} in prompts. Check the rest of the file still holds: every parameter (hands=12, fold_points=1, check_win_points=1, put_seen_points=3, etc.) is stored as an attribute rather than written into a step; `up_card` is set to the first dealt card's rank value; the card order is a simultaneous poll; each trick is decided by the rank order 3>2>A>K>...>4; and the single ending ranks by `you.score`.
