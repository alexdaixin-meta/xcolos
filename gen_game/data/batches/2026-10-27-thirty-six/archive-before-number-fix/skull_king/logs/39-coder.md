# 39 coder

- time: 2026-10-27T18:30:48+00:00 (77.8s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 869d39e37a33c315, reply sha256 f41b76896a6be6e5

## Sent

````
# Task: write the XColos game file for "Skull King: Blind Broadsides"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 4; set `meta.players` to {"min": 3, "max": 4, "suggested": 4} (the suggested size is the one the game plays best at).

CARDS. Each card has a power number. The deck holds 18 cards:
- the numbers 1 to 12 (power equal to the number);
- two Escapes (power 0);
- the Mermaid (power 20);
- Pirate A (power 30);
- Pirate B (power 31);
- the Skull King (power 40).

CONSTANTS. rounds = 10, hand_size = 3, tricks per round = 3, revealed cards = 3, bids from 0 to 3.

R1 SETUP. When the game starts, every player's score is 0 and the round counter is 0.

R2 ROUND START.
- round increases by 1.
- Every player's tricks_won is set to 0, bonus to 0 and hand to empty.
- The public list 'revealed' is set to empty.

R3 SHUFFLE. The deck is reset to all 18 cards and shuffled. This is the round's only chance event.

R4 DEAL. Each player receives 3 cards from the top of the deck into a private hand that only they can see.

R5 REVEAL. The next 3 cards of the deck are moved to 'revealed' and shown to everyone. These cards are out of play this round. The remaining undealt cards (3 with 4 players, 6 with 3 players) stay hidden.

R6 BID. All players bid at the same moment, without seeing other bids. The options are exactly 0, 1, 2 or 3, and the choice is stored as the number bid.

R7 ANNOUNCE. All bids are shown to everyone.

R8 TRICKS. Three tricks are played. Each trick has three steps.

(a) PLAY. All players at the same moment choose one card from their own hand. The chosen card is removed from the hand and becomes that player's 'played' card.

(b) SHOW. All played cards are revealed together.

(c) RESOLVE. The trick winner is decided as follows:
- If the played cards include both the Mermaid and the Skull King, the Mermaid's player wins the trick, even if a Pirate was also played, and that player's bonus increases by 10.
- Otherwise the card with the highest power wins.
- Only the two Escapes share a power, and there are at least 3 players, so a unique winner always exists.
- The winner's tricks_won increases by 1.

R9 SCORING. After the third trick, each player's score changes as follows:
- if tricks_won equals bid (including bid 0 with 0 tricks): +30 + bonus;
- otherwise: −10 × |bid − tricks_won|, and the bonus is lost.

R10 END. If round equals 10, the game ends. Otherwise the next round starts at R2.

There is no discussion phase.

How the winner is decided: After round 10, the player with the highest score wins. If two or more players tie for the highest score, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Skull King: Blind Broadsides (3 to 4 players, best with 4)

A simultaneous trick-taking game over 10 rounds: players bid how many of 3 tricks they will win, then all play a card at once in each trick, scoring for exact bids and a bonus when the Mermaid captures the Skull King.

STATE (every item below must exist in the file):
  - each player: score (number, starts 0); everyone sees it. Running total of points.
  - each player: bid (number, starts 0); everyone sees it. Tricks bid this round (0 to 3). It is gathered by a simultaneous poll, so no bid is seen until all are in.
  - each player: tricks_won (number, starts 0); everyone sees it. Tricks won this round.
  - each player: bonus (number, starts 0); everyone sees it. Bonus earned this round: +10 each time this player's Mermaid captures the Skull King.
  - each player: hand (list, starts []); only its owner sees it. Private hand of card powers (0 = Escape, 1-12 = numbers, 20 = Mermaid, 30 = Pirate A, 31 = Pirate B, 40 = Skull King).
  - each player: played (number, starts -1); everyone sees it. Power of the card played in the current trick, shown after all have played; -1 means none.
  - the table: round (number, starts 0); everyone sees it. Round counter, 1 to 10.
  - the table: deck (list, starts [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0, 0, 20, 30, 31, 40]); hidden from all players. Hidden deck of card powers. It is reset to all 18 cards each round, and cards are drawn from it at random.
  - the table: revealed (list, starts []); everyone sees it. The 3 face-up cards that are out of play this round.
  - the table: trick (number, starts 0); everyone sees it. Trick counter within the round, 0 to 3.
  - the table: winning_power (number, starts -1); everyone sees it. Power that wins the current trick: 20 if both the Mermaid and the Skull King were played, otherwise the highest played power.
  - parameters, each kept as a table attribute: rounds = 10, hand_size = 3, tricks_per_round = 3, revealed_cards = 3, bid_min = 0, bid_max = 3, deck_size = 18, number_card_min = 1, number_card_max = 12, escape_count = 2, escape_power = 0, mermaid_power = 20, pirate_a_power = 30, pirate_b_power = 31, skull_king_power = 40, made_bid_points = 30, mermaid_capture_bonus = 10, miss_penalty_per_trick = 10, initial_score = 0, initial_round = 0

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Every player's score is set to 0.
  2. The table's round counter is set to 0.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round += 1; for every player: tricks_won = 0, bonus = 0, hand = [], played = -1; revealed = []; trick = 0; deck = [1,2,3,4,5,6,7,8,9,10,11,12,0,0,20,30,31,40]. Announce the new round number.
  2. [update] all players. What happens: Deal: for each player, 3 times, pick a random card from deck, append it to that player's hand and remove it from deck (random picks are the shuffle).
  3. [update] all players. What happens: Reveal: 3 times, pick a random card from deck, append it to revealed and remove it from deck. The rest of deck stays hidden (3 cards with 4 players, 6 with 3).
  4. [sync] all players. What happens: Each player is sent their own hand, the revealed list, the scores and the round number.
  5. [poll] all players answers: a whole number from 0 to 3. What happens: Each player's bid = their answer. No one sees a bid until all are in.
  6. [tell] all players. What happens: Announce every player's bid to everyone.
  7. [poll] all players answers: one card (power) from the player's own hand. What happens: Each player's played = the chosen card, which is removed from their hand. No one sees a choice until all are in.
  8. [tell] all players. What happens: Show every player's played card to everyone at once.
  9. [update] all players. What happens: winning_power = 20 if some player's played == 20 and some player's played == 40, otherwise the maximum of played over all players. The player whose played == winning_power gets tricks_won += 1. If that player's played == 20 and some played == 40, that player also gets bonus += 10. trick += 1. Announce the trick winner.
  10. [repeat] all players. What happens: Run the play, show and resolve steps again until trick == 3.
  11. [update] all players. What happens: Scoring for each player: if tricks_won == bid then score += 30 + bonus; otherwise score -= 10 * |bid - tricks_won| and the bonus is lost. Announce all scores.
  12. [check] all players. What happens: If round == 10 the game ends; otherwise go back to the first round step.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, every player's score is 0 and round is 0.
  R2. When a round starts, round increases by 1, and every player's tricks_won is set to 0, bonus to 0 and hand to empty, while revealed is set to empty.
  R3. When a round starts, deck is reset to the 18 cards [1..12, 0, 0, 20, 30, 31, 40].
  R4. When cards are dealt, each player receives exactly 3 random cards from deck into their private hand, and those cards are removed from deck.
  R5. When cards are revealed, 3 further random cards move from deck to the public revealed list, are out of play this round, and leave 3 hidden cards in deck with 4 players or 6 with 3 players.
  R6. When bidding, all players answer at the same time with exactly 0, 1, 2 or 3, and the answer is stored as bid.
  R7. When all bids are in, every player's bid is shown to everyone.
  R8. When a trick is played, every player at the same time chooses one card from their own hand, and that card is removed from hand and stored as played.
  R9. When all cards of a trick are chosen, every played card is shown to everyone together.
  R10. When the played cards include both the Mermaid (20) and the Skull King (40), the Mermaid's player wins the trick even if a Pirate (30 or 31) was played, and gains bonus +10.
  R11. When the played cards do not include both the Mermaid and the Skull King, the player with the highest played power wins the trick (for example 31 beats 30, and 1 beats an Escape at 0).
  R12. When a player wins a trick, their tricks_won increases by 1.
  R13. When the round is played, exactly 3 tricks are played, so each player plays all 3 cards in hand.
  R14. When a player's tricks_won equals their bid after the third trick (including bid 0 with 0 tricks), their score increases by 30 + bonus (for example bid 1, won 1, bonus 10 gives +40).
  R15. When a player's tricks_won differs from their bid after the third trick, their score decreases by 10 × |bid − tricks_won| and the bonus is lost (for example bid 3, won 1 gives −20).
  R16. When round equals 10 after scoring, the game ends; otherwise a new round starts.
  R17. When the game ends, the player with the highest score wins, and players tied at the highest score share the top place.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Bid | asked: all players | options: 0, 1, 2 or 3, for every seat in every round.
  - Play a card | asked: all players | options: Each seat is offered exactly the cards currently in its own hand: 3 cards in the first trick, the 2 remaining in the second, the 1 remaining in the third.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round == 10 (checked after the round's scoring)
  - each player's standing: you.score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their final score after round 10. The highest score wins, and players tied for the highest score share the result (the source calls this a draw).
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

- each player: `score` (number, visible: public, starts 0): Running total of points.
- each player: `bid` (number, visible: public, starts 0): Tricks bid this round (0 to 3). It is gathered by a simultaneous poll, so no bid is seen until all are in.
- each player: `tricks_won` (number, visible: public, starts 0): Tricks won this round.
- the table: `round` (number, visible: public, starts 0): Round counter, 1 to 10.
- the table: `revealed` (list, visible: public, starts []): The 3 face-up cards that are out of play this round.
- parameters (each must be an attribute holding this value, never a number buried in a step): rounds = 10, hand_size = 3, tricks_per_round = 3, revealed_cards = 3, bid_min = 0, bid_max = 3, deck_size = 18, number_card_min = 1, number_card_max = 12, escape_count = 2, escape_power = 0, mermaid_power = 20, pirate_a_power = 30, pirate_b_power = 31, skull_king_power = 40, made_bid_points = 30, mermaid_capture_bonus = 10, miss_penalty_per_trick = 10, initial_score = 0, initial_round = 0
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
    "id": "skull_king_blind_broadsides",
    "name": "Skull King: Blind Broadsides",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 4
    },
    "blurb": "Bid how many of 3 tricks you will win, then play every trick blind and simultaneous; the Mermaid captures the Skull King for a bonus."
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
        "key": "bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tricks_won",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bonus",
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
        "key": "played",
        "visible": "public",
        "type": "number",
        "initial": -1
      },
      {
        "key": "card_choice",
        "visible": "ally",
        "type": "text",
        "initial": ""
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
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0, 0, 20, 30, 31, 40]
      },
      {
        "key": "revealed",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "trick",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "winning_power",
        "visible": "public",
        "type": "number",
        "initial": -1
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "number",
        "initial": -1
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "hand_size",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "tricks_per_round",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "revealed_cards",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "bid_min",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bid_max",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 18
      },
      {
        "key": "number_card_min",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "number_card_max",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "escape_count",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "escape_power",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "mermaid_power",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "pirate_a_power",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "pirate_b_power",
        "visible": "public",
        "type": "number",
        "initial": 31
      },
      {
        "key": "skull_king_power",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "made_bid_points",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "mermaid_capture_bonus",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "miss_penalty_per_trick",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "initial_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "initial_round",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "start the game",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "initial_score"
            }
          }
        },
        {
          "set": {
            "key": "round",
            "value": {
              "calc": "initial_round"
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
      "phase": "round start",
      "label": "new round",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "players": "all",
            "key": "tricks_won",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bonus",
            "value": 0
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
          "set": {
            "players": "all",
            "key": "played",
            "value": -1
          }
        },
        {
          "set": {
            "players": "all",
            "key": "card_choice",
            "value": ""
          }
        },
        {
          "set": {
            "key": "revealed",
            "value": []
          }
        },
        {
          "set": {
            "key": "trick",
            "value": 0
          }
        },
        {
          "set": {
            "key": "winning_power",
            "value": -1
          }
        },
        {
          "set": {
            "key": "deck",
            "value": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0, 0, 20, 30, 31, 40]
          }
        }
      ],
      "text": "Round {round} of {rounds} begins. The deck of {deck_size} cards is shuffled."
    },
    {
      "use": "update",
      "phase": "deal",
      "label": "deal the hands",
      "do": [
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}, "if": {"calc": "len(players) >= 4"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}, "if": {"calc": "len(players) >= 4"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}, "if": {"calc": "len(players) >= 4"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}}
      ],
      "text": "Each player is dealt {hand_size} cards in secret."
    },
    {
      "use": "update",
      "phase": "deal",
      "label": "reveal three cards",
      "do": [
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"key": "revealed", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"key": "revealed", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"key": "revealed", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}}
      ],
      "text": "Revealed and out of play this round: {revealed}."
    },
    {
      "use": "sync",
      "phase": "deal",
      "label": "your hand",
      "mode": "self",
      "to": "all",
      "text": "Round {round}. Your hand, the revealed cards {revealed} and the scores:"
    },
    {
      "use": "poll",
      "phase": "bid",
      "label": "bid",
      "to": "acting",
      "answer": {
        "type": "number",
        "min": {
          "calc": "bid_min"
        },
        "max": {
          "calc": "bid_max"
        }
      },
      "store": "bid",
      "text": "Round {round}: bid how many of the {tricks_per_round} tricks you will win, a whole number from {bid_min} to {bid_max}. Nobody sees any bid until all are in."
    },
    {
      "use": "tell",
      "phase": "bid",
      "label": "the bids",
      "to": "all",
      "text": "Bids [seat, bid]: {[[p.seat, p.bid] for p in players]}."
    },
    {
      "use": "repeat",
      "phase": "tricks",
      "label": "the tricks",
      "until": {
        "calc": "trick >= tricks_per_round"
      },
      "max": 5,
      "steps": [
        {
          "use": "poll",
          "phase": "tricks",
          "label": "play a card",
          "to": "acting",
          "answer": {
            "type": "choice",
            "options": {
              "attribute": "hand"
            }
          },
          "store": "card_choice",
          "text": "Choose one card from your hand to play in this trick. All cards are revealed together."
        },
        {
          "use": "update",
          "phase": "tricks",
          "label": "cards leave the hands",
          "do": [
            {
              "set": {
                "players": "all",
                "key": "played",
                "value": {
                  "calc": "int(you.card_choice)"
                }
              }
            },
            {
              "remove": {
                "players": "all",
                "key": "hand",
                "value": {
                  "calc": "you.played"
                }
              }
            }
          ]
        },
        {
          "use": "tell",
          "phase": "tricks",
          "label": "show the cards",
          "to": "all",
          "text": "Cards played [seat, power]: {[[p.seat, p.played] for p in players]}."
        },
        {
          "use": "update",
          "phase": "tricks",
          "label": "resolve the trick",
          "do": [
            {
              "set": {
                "key": "winning_power",
                "value": {
                  "calc": "mermaid_power if (any(p.played == mermaid_power for p in players) and any(p.played == skull_king_power for p in players)) else max([p.played for p in players])"
                }
              }
            },
            {
              "adjust": {
                "players": {
                  "where": "you.played == winning_power"
                },
                "key": "tricks_won",
                "value": 1,
                "text": "Seat {player} wins the trick with power {winning_power}."
              }
            },
            {
              "adjust": {
                "players": {
                  "where": "you.played == mermaid_power and any(p.played == skull_king_power for p in players)"
                },
                "key": "bonus",
                "value": {
                  "calc": "mermaid_capture_bonus"
                },
                "text": "Seat {player}'s Mermaid captures the Skull King: bonus +{mermaid_capture_bonus}."
              }
            },
            {
              "adjust": {
                "key": "trick",
                "value": 1
              }
            },
            {
              "set": {
                "players": "all",
                "key": "card_choice",
                "value": ""
              }
            }
          ]
        }
      ]
    },
    {
      "use": "update",
      "phase": "scoring",
      "label": "score the round",
      "do": [
        {
          "adjust": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "(made_bid_points + you.bonus) if you.tricks_won == you.bid else -miss_penalty_per_trick * abs(you.bid - you.tricks_won)"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.tricks_won != you.bid"
            },
            "key": "bonus",
            "value": 0
          }
        }
      ],
      "text": "Round {round} scored. Scores [seat, score]: {[[p.seat, p.score] for p in players]}."
    },
    {
      "use": "check",
      "phase": "scoring",
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
      "rank_by": "you.score",
      "text": "Winner: {result}. Final scores [seat, score]: {[[p.seat, p.score] for p in players]}."
    }
  },
  "limits": {
    "rounds": 10,
    "rounds_max": 10,
    "actions_max": 3000,
    "deadline_s": 120
  },
  "rules": "CARDS. The deck holds {deck_size} cards, each with a power: the numbers {number_card_min} to {number_card_max} (power equal to the number); {escape_count} Escapes (power {escape_power}); the Mermaid (power {mermaid_power}); Pirate A (power {pirate_a_power}); Pirate B (power {pirate_b_power}); the Skull King (power {skull_king_power}).\n\nThe game lasts {rounds} rounds. Every score starts at {initial_score}.\n\nROUND START. The round counter increases by 1. Every player's tricks won and bonus are set to 0 and hands are emptied; the revealed list is emptied.\n\nSHUFFLE AND DEAL. The deck is reset to all {deck_size} cards and shuffled. Each player receives {hand_size} cards into a private hand only they can see. The next {revealed_cards} cards are revealed to everyone and are out of play this round. The remaining undealt cards (3 with 4 players, 6 with 3 players) stay hidden.\n\nBID. All players bid at the same moment, without seeing other bids: exactly {bid_min}, 1, 2 or {bid_max}, the number of tricks you expect to win. Then all bids are shown to everyone.\n\nTRICKS. {tricks_per_round} tricks are played. In each trick: (a) all players at the same moment choose one card from their own hand; it leaves the hand and becomes their played card. (b) All played cards are revealed together. (c) If the played cards include both the Mermaid and the Skull King, the Mermaid's player wins the trick, even if a Pirate was also played, and that player's bonus increases by {mermaid_capture_bonus}. Otherwise the card with the highest power wins (31 beats 30, 1 beats an Escape), and no bonus is gained. Only the two Escapes share a power, so a unique winner always exists. The winner's tricks won increases by 1.\n\nSCORING. After the third trick: if your tricks won equals your bid (including bid 0 with 0 tricks), your score increases by {made_bid_points} plus your bonus (bid 1, won 1, bonus 10 gives +40). If it does not, your score decreases by {miss_penalty_per_trick} times the difference between bid and tricks won (bid 3, won 1 gives -20), and your bonus is lost.\n\nEND. If the round counter equals {rounds}, the game ends; otherwise the next round starts. After the last round the highest score wins; players tied for the highest score share the top place. There is no discussion."
}
````
