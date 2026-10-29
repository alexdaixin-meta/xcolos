# Task: write the XColos game file for "Kobayakawa Duel Rounds with Table Talk"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 5; set `meta.players` to {"min": 3, "max": 5, "suggested": 4} (the suggested size is the one the game plays best at).

SETUP: Each player starts with 5 kamons. The centre starts with 10 kamons. The game lasts exactly 10 rounds.

EACH ROUND:
1. Deal. Shuffle a fresh deck of 15 cards numbered 1 to 15. Deal each player one face-down hand card, which only that player sees. Deal each player one face-down reserve card, which nobody sees. Turn one more card face up: this is the Kobayakawa card, value K. Announce K.
2. Draw choice. All players choose KEEP or SWAP at the same moment. A SWAP player discards their hand card face up, takes their reserve card as their new hand card, and looks at it. Reserve cards of KEEP players are not used. Announce every discarded card and who discarded it.
3. Talk. Every player writes one short public message at the same moment, without seeing the others' messages. Then all messages are shown to everyone. Messages may say anything, including false claims about one's card or intentions. Nothing said is binding.
4. Fight choice. All players choose FIGHT or PASS at the same moment. A player with 0 kamons must PASS. Each FIGHT player puts 1 kamon into the pot.
5. Resolve.
   - No fighters: nothing happens.
   - Exactly one fighter: that player takes their own kamon back. Their card is not revealed, and the centre pays nothing.
   - Two or more fighters: all fighters reveal their cards. Each fighter's total equals their card, except that the fighter with the lowest card adds K to it. The fighter with the highest total wins. If totals tie, the tied fighter with the lower card wins. The winner takes the whole pot. If the centre has at least 1 kamon, the winner also takes 1 kamon from the centre. Losing fighters lose their stakes.
6. Announce all fighters, revealed cards, totals, the winner, and every player's kamon count.
7. After round 10 the game ends.

How the winner is decided: After round 10, the player with the most kamons wins. If two or more players tie for most, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Kobayakawa Duel Rounds with Table Talk (3 to 5 players, best with 4)

Over 10 rounds, players hold one secret card, may swap it blind, talk, then fight for a pot. The lowest fighter's card adds the face-up Kobayakawa value, and the highest total takes the pot plus 1 kamon from the centre.

STATE (every item below must exist in the file):
  - each player: kamons (number, starts 5); everyone sees it. the player's kamons; this is the score
  - each player: hand (number, starts 0); only its owner sees it. the player's current face-down hand card (1-15), seen only by its owner
  - each player: draw_choice (text, starts ''); everyone sees it. KEEP or SWAP this round
  - each player: discarded (number, starts 0); everyone sees it. the card discarded face up by a SWAP this round (0 if the player kept)
  - each player: message (text, starts ''); everyone sees it. this round's public table-talk message
  - each player: fight_choice (text, starts ''); everyone sees it. FIGHT or PASS this round
  - each player: fought (bool, starts False); everyone sees it. whether the player fights this round
  - each player: revealed_card (number, starts 0); everyone sees it. the card revealed in a showdown of 2 or more fighters (0 if not revealed)
  - each player: total (number, starts 0); everyone sees it. the fight total in a showdown: the card, plus K for the lowest card (0 if not in a showdown)
  - the table: round (number, starts 0); everyone sees it. the current round number
  - the table: deck (list, starts []); hidden from all players. this round's fresh shuffled deck of cards 1-15
  - the table: reserve_cards (list, starts []); hidden from all players. each seat's face-down reserve card, in seat order; nobody sees it
  - the table: kobayakawa (number, starts 0); everyone sees it. K, the face-up Kobayakawa card this round
  - the table: centre (number, starts 10); everyone sees it. kamons left in the centre
  - the table: pot (number, starts 0); everyone sees it. kamons staked this round
  - the table: fighter_count (number, starts 0); everyone sees it. the number of FIGHT players this round
  - the table: lowest_card (number, starts 0); everyone sees it. the lowest card among the fighters in a showdown
  - the table: winner_seat (number, starts 0); everyone sees it. the seat that won this round's showdown (0 if there was none)
  - parameters, each kept as a table attribute: starting_kamons = 5, centre_starting_kamons = 10, rounds = 10, deck_size = 15, card_min = 1, card_max = 15, fight_stake = 1, centre_bonus = 1, hand_cards_per_player = 1, reserve_cards_per_player = 1, minimum_fighters_for_showdown = 2

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Every player's kamons is set to 5.
  2. The centre is set to 10 kamons.
  3. The round is set to 0.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round += 1; deck = [1..15] (a fresh deck); reserve_cards = []; pot = 0; fighter_count = 0; lowest_card = 0; winner_seat = 0; for every player: draw_choice = '', discarded = 0, message = '', fight_choice = '', fought = false, revealed_card = 0, total = 0
  2. [update] all players. What happens: For each player: draw one random card from deck into hand and remove it from deck. Then, for each seat in order: draw one random card from deck, append it to reserve_cards and remove it from deck. Then draw one random card from deck into kobayakawa and remove it from deck. Announce: 'Round {round}: the Kobayakawa card K is {kobayakawa}.'
  3. [sync] all players. What happens: Each player sees their own hand, every player's kamons, the centre and kobayakawa.
  4. [poll] all players answers: choice: KEEP | SWAP. What happens: draw_choice = the answer
  5. [update] all players. What happens: For each player with draw_choice == 'SWAP': discarded = hand; hand = reserve_cards[seat-1]. Announce each discard: 'Seat {seat} swapped and discarded {discarded}.'
  6. [sync] each player with draw_choice SWAP. What happens: Each swapping player sees their new hand.
  7. [poll] all players answers: short text. What happens: message = the answer; broadcast {"to": "all", "text": "Seat {seat} says: {value}"} once all messages are in
  8. [poll] all players answers: choice: FIGHT | PASS (only PASS when kamons == 0). What happens: fight_choice = the answer; fought = (fight_choice == 'FIGHT')
  9. [update] all players. What happens: For each player with fought: kamons -= 1; pot += 1. fighter_count = the number of players with fought.
  10. [update] the single fighter. What happens: when fighter_count == 1: that player's kamons += pot; pot = 0. The card is not revealed and the centre is unchanged.
  11. [update] all fighters. What happens: when fighter_count >= 2: lowest_card = min(hand) over players with fought; for each player with fought: revealed_card = hand; total = hand + (hand == lowest_card ? kobayakawa : 0)
  12. [update] the showdown winner. What happens: when fighter_count >= 2: winner_seat = the fighter with the largest (total * 100 - hand), so the highest total wins and a tie goes to the lower card; that player's kamons += pot + min(1, centre); centre -= min(1, centre); pot = 0
  13. [tell] all players. What happens: Announce the fighters, each revealed_card and total, winner_seat, and every player's kamons and the centre.
  14. [check] all players. What happens: End the game if round >= 10; otherwise continue.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, then each player has 5 kamons, the centre has 10 kamons and the round is 0.
  R2. When a round starts, then the deck is a fresh set of the 15 cards 1 to 15, and each player gets 1 hand card and 1 reserve card from it, all distinct.
  R3. When the deal is done, then one more card from the deck is set as kobayakawa (K) and announced publicly.
  R4. When a player's hand is dealt, then only that player can see it, and no player can see any reserve card.
  R5. When a player chooses SWAP, then discarded becomes their old hand card (publicly announced with their seat) and hand becomes their reserve card.
  R6. When a player chooses KEEP, then hand is unchanged, discarded stays 0 and their reserve card is not used.
  R7. When the KEEP/SWAP choice is asked, then all players answer at once, without seeing the others' choices.
  R8. When the talk step runs, then every player submits one short message at once, and all messages are shown to everyone only after all are in.
  R9. When a player has 0 kamons at the fight choice, then their only option is PASS.
  R10. When a player chooses FIGHT, then their kamons drop by 1 and the pot rises by 1.
  R11. When no player fights, then no kamons change that round.
  R12. When exactly one player fights, then that player gets their 1 kamon back, their card is not revealed and the centre is unchanged.
  R13. When two or more players fight, then each fighter's revealed_card equals their hand and their total equals their hand, plus K for the fighter with the lowest card.
  R14. When two or more players fight, then the fighter with the highest total wins, and if totals tie the tied fighter with the lower card wins (e.g. K=5: cards 3 and 8 give totals 8 and 8, so card 3 wins).
  R15. When a showdown winner is decided and the centre has at least 1 kamon, then the winner gains the whole pot plus 1 kamon and the centre loses 1.
  R16. When a showdown winner is decided and the centre has 0 kamons, then the winner gains only the pot.
  R17. When a showdown is decided, then each losing fighter loses the 1 kamon they staked.
  R18. When round 10 ends, then the game ends and the player with the most kamons wins, with players tied for most sharing the result.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Draw choice | asked: every seat | options: KEEP, SWAP
  - Talk message | asked: every seat | options: any short text
  - Fight choice | asked: every seat | options: a seat with kamons >= 1: FIGHT, PASS; a seat with kamons == 0: PASS only

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round >= 10
  - each player's standing: you.kamons (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: After round 10, each player's standing is their kamons. The most kamons wins, and players tied for most share the result (the source calls this a draw).
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

- each player: `kamons` (number, visible: public, starts 5): the player's kamons; this is the score
- each player: `discarded` (number, visible: public, starts 0): the card discarded face up by a SWAP this round (0 if the player kept)
- each player: `revealed_card` (number, visible: public, starts 0): the card revealed in a showdown of 2 or more fighters (0 if not revealed)
- each player: `total` (number, visible: public, starts 0): the fight total in a showdown: the card, plus K for the lowest card (0 if not in a showdown)
- the table: `round` (number, visible: public, starts 0): the current round number
- the table: `kobayakawa` (number, visible: public, starts 0): K, the face-up Kobayakawa card this round
- the table: `centre` (number, visible: public, starts 10): kamons left in the centre
- the table: `winner_seat` (number, visible: public, starts 0): the seat that won this round's showdown (0 if there was none)
- parameters (each must be an attribute holding this value, never a number buried in a step): starting_kamons = 5, centre_starting_kamons = 10, rounds = 10, deck_size = 15, card_min = 1, card_max = 15, fight_stake = 1, centre_bonus = 1, hand_cards_per_player = 1, reserve_cards_per_player = 1, minimum_fighters_for_showdown = 2
- the game ends with ONE ending whose `rank_by` is `you.kamons`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
