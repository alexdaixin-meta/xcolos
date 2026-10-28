# 23 coder

- time: 2026-10-28T03:25:29+00:00 (71.9s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 3a639e5f40ac30d3, reply sha256 294ffa464bcded1e

## Sent

````
# Task: write the XColos game file for "Quick Reversis"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 4 to 4; set `meta.players` to {"min": 4, "max": 4, "suggested": 4} (the suggested size is the one the game plays best at).

SETUP
- Players are seats 1, 2, 3 and 4. Every player's total starts at 0.
- The deck has 24 cards: A, K, Q, J, 9 and 8 in each of Spades, Hearts, Diamonds and Clubs.
- Within a suit the ranking is A (highest), K, Q, J, 9, 8. There are no trumps.

CARD POINTS
- Each Ace counts 4, each King 3, each Queen 2 and each Jack 1. Nines and eights count 0.
- The exception is the Jack of Hearts (the Quinola), which counts 5.
- Each hand contains 44 points in total.

STRUCTURE
- The game has 4 hands of 6 tricks each, so 24 rounds. Each round is one trick.

START OF A HAND (rounds 1, 7, 13 and 19)
- Shuffle the 24 cards and deal 6 face down to each player. Each player sees only their own hand.
- The leader of the first trick of hand h is seat h.
- Set the sweeper to 'none'.

EACH ROUND (ONE TRICK)
1. The leader plays any one card from their hand face up. Its suit is the led suit. Announce it.
2. The other three players each choose one card at the same moment, without seeing each other's choices.
   - A player who holds a card of the led suit must play one.
   - A player who holds none may play any card.
3. All cards are revealed together.
4. The highest card of the led suit wins the trick.
5. Add up the points of the 4 cards played. The trick winner adds them to their total.
6. Played cards leave the game for the rest of the hand.
7. Update the sweeper:
   - On the first trick of a hand, the sweeper becomes the trick winner.
   - On later tricks, if the trick winner is not the sweeper, the sweeper becomes 'none'.
8. The trick winner leads the next trick.
9. Announce every player's total.

END OF A HAND (after tricks 6, 12, 18 and 24)
- If the sweeper is a player (that player took all 6 tricks, a reversis):
  - that player subtracts 44 from their total, so the hand counts 0 for them;
  - each other player adds 15 to their total.

TALK
- There is no table talk.

END OF GAME
- After round 24 the game ends.

How the winner is decided: After 4 hands, the player with the lowest total wins. If two or more players tie for the lowest total, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Quick Reversis (4 to 4 players, best with 4)

A four-player trick-avoidance card game over 4 hands of 6 tricks: take as few card points as possible, unless you take every trick of a hand (a reversis), which wipes that hand's points for you and charges 15 to each opponent; the lowest total wins.

STATE (every item below must exist in the file):
  - each player: total (number, starts 0); everyone sees it. Card points taken so far, with reversis adjustments. Lower is better.
  - each player: hand (list, starts []); only its owner sees it. Cards the player holds in the current hand, for example 'QH' or 'JH'.
  - each player: played_card (text, starts ''); everyone sees it. The card this player played to the current trick, revealed when all cards are shown.
  - each player: tricks_this_hand (number, starts 0); everyone sees it. Tricks this player has won in the current hand.
  - the table: deck (list, starts ['AS', 'KS', 'QS', 'JS', '9S', '8S', 'AH', 'KH', 'QH', 'JH', '9H', '8H', 'AD', 'KD', 'QD', 'JD', '9D', '8D', 'AC', 'KC', 'QC', 'JC', '9C', '8C']); hidden from all players. The undealt cards. It is refilled to all 24 cards at the start of each hand.
  - the table: round (number, starts 0); everyone sees it. The current trick number, from 1 to 24.
  - the table: hand_number (number, starts 0); everyone sees it. The current hand, from 1 to 4.
  - the table: leader (number, starts 1); everyone sees it. The seat that leads the current trick.
  - the table: led_suit (text, starts ''); everyone sees it. The suit of the card led to the current trick: S, H, D or C.
  - the table: trick_winner (number, starts 0); everyone sees it. The seat that played the highest card of the led suit in the current trick.
  - the table: trick_points (number, starts 0); everyone sees it. The sum of the card points of the 4 cards in the current trick.
  - the table: sweeper (number, starts 0); everyone sees it. The seat that has won every trick of the hand so far, or 0 for 'none'.
  - parameters, each kept as a table attribute: deck_size = 24, cards_per_suit = 6, suits = 4, cards_dealt_per_player = 6, hands = 4, tricks_per_hand = 6, total_rounds = 24, ace_points = 4, king_points = 3, queen_points = 2, jack_points = 1, nine_points = 0, eight_points = 0, quinola_points = 5, points_per_hand = 44, reversis_subtract = 44, reversis_bonus_to_others = 15, rank_ace = 6, rank_king = 5, rank_queen = 4, rank_jack = 3, rank_nine = 2, rank_eight = 1, sweeper_none_code = 0

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seats are numbered 1, 2, 3 and 4, and every player's total is set to 0.
  2. The table deck is defined as the 24 cards A, K, Q, J, 9 and 8 of Spades, Hearts, Diamonds and Clubs.
  3. round and hand_number start at 0, and sweeper starts at 0 (none).

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round += 1; if (round - 1) % 6 == 0: hand_number += 1, deck is reset to all 24 cards, every player's hand is cleared and tricks_this_hand is set to 0, then 6 cards are dealt to each player by random draws (each card is removed from deck and appended to that player's hand), leader = hand_number, and sweeper = 0 (none). Every player's played_card is cleared.
  2. [sync] all players. What happens: Each player is sent their own hand, plus the public total, leader, round, hand_number and sweeper.
  3. [ask] the seat equal to leader answers: one card from their hand. What happens: The card is removed from the leader's hand and set as the leader's played_card; led_suit = the suit of that card.
  4. [tell] all players. What happens: Announce: 'Seat {leader} leads {played_card}; the led suit is {led_suit}.'
  5. [poll] every seat except leader answers: one card from their hand; if the hand holds any card of led_suit, only cards of led_suit. What happens: Each chosen card is removed from that player's hand and set as their played_card. No answer is seen until all three are in.
  6. [tell] all players. What happens: Reveal all four played_card values together.
  7. [update] all players. What happens: trick_winner = the seat whose played_card is of led_suit with the highest rank (A=6, K=5, Q=4, J=3, 9=2, 8=1); trick_points = the sum of the points of the 4 played cards (A=4, K=3, Q=2, J=1, 9=0, 8=0, but JH=5); the trick_winner's total += trick_points and their tricks_this_hand += 1.
  8. [update] all players. What happens: If (round - 1) % 6 == 0: sweeper = trick_winner. Otherwise, if trick_winner != sweeper: sweeper = 0.
  9. [update] all players. What happens: leader = trick_winner.
  10. [tell] all players. What happens: Announce: 'Seat {trick_winner} wins the trick and takes {trick_points} points. Totals: seat 1 {total}, seat 2 {total}, seat 3 {total}, seat 4 {total}.'
  11. [update] all players. What happens: When round % 6 == 0 and sweeper != 0: the player whose seat equals sweeper subtracts 44 from total, and every other player adds 15 to total. Announce the reversis if it happened.
  12. [check] all players. What happens: If round == 24, end the game; otherwise continue with the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, then every player's total is 0.
  R2. When a hand starts (rounds 1, 7, 13 and 19), then the deck is refilled to 24 cards and each player is dealt 6 cards from it into their hand, leaving the deck empty.
  R3. When hand h starts, then the leader of its first trick is seat h (hand 1 seat 1, hand 2 seat 2, hand 3 seat 3, hand 4 seat 4).
  R4. When a hand starts, then the sweeper is set to none (0).
  R5. When a player's hand is dealt, then only that player sees it; other players do not.
  R6. When the leader leads, then they may play any card in their hand, and that card's suit becomes the led suit.
  R7. When a non-leader holds at least one card of the led suit, then they must play a card of the led suit.
  R8. When a non-leader holds no card of the led suit, then they may play any card in their hand.
  R9. When the three non-leaders choose, then they choose simultaneously, and no choice is seen until all are revealed together.
  R10. When cards are compared, then the highest card of the led suit wins, with ranking A > K > Q > J > 9 > 8, and cards of other suits never win because there are no trumps.
  R11. When a trick is won, then its winner adds the points of all 4 cards to their total: Ace 4, King 3, Queen 2, Jack 1, Nine 0, Eight 0, except the Jack of Hearts (Quinola), which counts 5.
  R12. When a card is played, then it is removed from the player's hand and does not return for the rest of the hand.
  R13. When the first trick of a hand is won, then the sweeper becomes that trick's winner.
  R14. When a later trick of a hand is won by a player other than the sweeper, then the sweeper becomes none (0).
  R15. When a trick is won, then its winner leads the next trick.
  R16. When a trick ends, then every player's total is announced.
  R17. When a hand ends (after tricks 6, 12, 18 and 24) and the sweeper is a player who took all 6 tricks, then that player subtracts 44 from their total and each other player adds 15 to their total.
  R18. When a hand ends and the sweeper is none, then no totals are adjusted.
  R19. When round 24 has been played, then the game ends.
  R20. When the game ends, then the player with the lowest total wins, and players tied for the lowest total share the result (a draw).
  R21. When a hand is played, then there is no table talk.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - The leader's lead | asked: the seat equal to leader | options: every card currently in that seat's hand
  - A follower's card | asked: each of the three seats other than leader | options: if the seat holds any card of led_suit: exactly the cards of led_suit in its hand; otherwise: every card in its hand

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round == 24
  - each player's standing: 0 - you.total (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is minus their total, so the lowest total ranks highest. The player with the lowest total wins. If two or more players tie for the lowest total, they share the result, which is the source's draw.
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

- each player: `total` (number, visible: public, starts 0): Card points taken so far, with reversis adjustments. Lower is better.
- each player: `played_card` (text, visible: public, starts ''): The card this player played to the current trick, revealed when all cards are shown.
- the table: `round` (number, visible: public, starts 0): The current trick number, from 1 to 24.
- the table: `hand_number` (number, visible: public, starts 0): The current hand, from 1 to 4.
- the table: `leader` (number, visible: public, starts 1): The seat that leads the current trick.
- the table: `led_suit` (text, visible: public, starts ''): The suit of the card led to the current trick: S, H, D or C.
- the table: `trick_winner` (number, visible: public, starts 0): The seat that played the highest card of the led suit in the current trick.
- the table: `sweeper` (number, visible: public, starts 0): The seat that has won every trick of the hand so far, or 0 for 'none'.
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 24, cards_per_suit = 6, suits = 4, cards_dealt_per_player = 6, hands = 4, tricks_per_hand = 6, total_rounds = 24, ace_points = 4, king_points = 3, queen_points = 2, jack_points = 1, nine_points = 0, eight_points = 0, quinola_points = 5, points_per_hand = 44, reversis_subtract = 44, reversis_bonus_to_others = 15, rank_ace = 6, rank_king = 5, rank_queen = 4, rank_jack = 3, rank_nine = 2, rank_eight = 1, sweeper_none_code = 0
- the game ends with ONE ending whose `rank_by` is `0 - you.total`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
    "id": "quick_reversis",
    "name": "Quick Reversis",
    "players": {
      "min": 4,
      "max": 4,
      "suggested": 4
    },
    "blurb": "Four hands of six tricks: avoid card points, unless you take every trick of a hand for a reversis. Lowest total wins."
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
        "key": "total",
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
        "key": "played_card",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "tricks_this_hand",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "follow",
        "visible": "ally",
        "type": "text",
        "initial": ""
      }
    ],
    "game": [
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": ["AS", "KS", "QS", "JS", "9S", "8S", "AH", "KH", "QH", "JH", "9H", "8H", "AD", "KD", "QD", "JD", "9D", "8D", "AC", "KC", "QC", "JC", "9C", "8C"]
      },
      {
        "key": "full_deck",
        "visible": "none",
        "type": "list",
        "initial": ["AS", "KS", "QS", "JS", "9S", "8S", "AH", "KH", "QH", "JH", "9H", "8H", "AD", "KD", "QD", "JD", "9D", "8D", "AC", "KC", "QC", "JC", "9C", "8C"]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "best_rank",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "lead_card",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hand_number",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "leader",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "led_suit",
        "visible": "public",
        "type": "text",
        "initial": ""
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
        "key": "sweeper",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 24
      },
      {
        "key": "cards_per_suit",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "suits",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "cards_dealt_per_player",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "hands",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "tricks_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "total_rounds",
        "visible": "public",
        "type": "number",
        "initial": 24
      },
      {
        "key": "ace_points",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "king_points",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "queen_points",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "jack_points",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "nine_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "eight_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "quinola_points",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "points_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 44
      },
      {
        "key": "reversis_subtract",
        "visible": "public",
        "type": "number",
        "initial": 44
      },
      {
        "key": "reversis_bonus_to_others",
        "visible": "public",
        "type": "number",
        "initial": 15
      },
      {
        "key": "rank_ace",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "rank_king",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "rank_queen",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "rank_jack",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "rank_nine",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "rank_eight",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "sweeper_none_code",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "totals start at zero",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "total",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "the deck",
      "do": [
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "full_deck"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "counters",
      "do": [
        {
          "set": {
            "key": "round",
            "value": 0
          }
        },
        {
          "set": {
            "key": "hand_number",
            "value": 0
          }
        },
        {
          "set": {
            "key": "sweeper",
            "value": {
              "calc": "sweeper_none_code"
            }
          }
        }
      ]
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "start",
      "label": "the next trick",
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
            "key": "played_card",
            "value": ""
          }
        },
        {
          "set": {
            "key": "lead_card",
            "value": ""
          }
        },
        {
          "set": {
            "key": "led_suit",
            "value": ""
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "start",
      "label": "a new hand is dealt",
      "when": {
        "calc": "(round - 1) % tricks_per_hand == 0"
      },
      "do": [
        {
          "adjust": {
            "key": "hand_number",
            "value": 1
          }
        },
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
          "set": {
            "players": "all",
            "key": "tricks_this_hand",
            "value": 0
          }
        },
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "hand_number"
            }
          }
        },
        {
          "set": {
            "key": "sweeper",
            "value": {
              "calc": "sweeper_none_code"
            }
          }
        }
      ],
      "text": "Hand {hand_number} of {hands} is dealt: {cards_dealt_per_player} cards each. Seat {leader} leads the first trick."
    },
    {
      "use": "sync",
      "phase": "start",
      "label": "your hand",
      "mode": "self",
      "to": "all",
      "fields": [
        "hand",
        "total",
        "tricks_this_hand"
      ],
      "text": "Trick {round} (hand {hand_number} of {hands}). Seat {leader} leads. Sweeper: {sweeper} (0 means none). Your state:"
    },
    {
      "use": "ask",
      "phase": "lead",
      "label": "the lead",
      "to": {
        "where": "you.seat == leader"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "verify": {
        "bind": "lead"
      },
      "text": "You lead trick {round}. Play any one card from your hand face up; its suit becomes the led suit. The highest card of the led suit takes the trick and its points."
    },
    {
      "use": "update",
      "phase": "lead",
      "label": "the lead is played",
      "do": [
        {
          "set": {
            "key": "lead_card",
            "value": "$lead"
          }
        },
        {
          "remove": {
            "player": {
              "calc": "leader"
            },
            "key": "hand",
            "value": {
              "calc": "lead_card"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "leader"
            },
            "key": "played_card",
            "value": {
              "calc": "lead_card"
            }
          }
        },
        {
          "set": {
            "key": "led_suit",
            "value": {
              "calc": "lead_card[1]"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "lead",
      "label": "the lead is announced",
      "to": "all",
      "text": "Seat {leader} leads {lead}; the led suit is {led_suit}."
    },
    {
      "use": "update",
      "phase": "follow",
      "label": "what each follower may play",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "follow",
            "value": ""
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat != leader"
            },
            "key": "offer",
            "value": {
              "calc": "[c for c in you.hand if c[1] == led_suit] if any([c[1] == led_suit for c in you.hand]) else you.hand"
            }
          }
        }
      ]
    },
    {
      "use": "poll",
      "phase": "follow",
      "label": "the followers play",
      "to": {
        "where": "you.seat != leader"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "store": "follow",
      "text": "Seat {leader} led {lead} (suit {led_suit}). Choose one card face down. If you hold a card of the led suit you must play one (only those are offered); if you hold none you may play any card. Nobody sees your choice until all cards are revealed together."
    },
    {
      "use": "update",
      "phase": "follow",
      "label": "the followers' cards are played",
      "do": [
        {
          "remove": {
            "players": {
              "where": "you.seat != leader"
            },
            "key": "hand",
            "value": {
              "calc": "you.follow"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat != leader"
            },
            "key": "played_card",
            "value": {
              "calc": "you.follow"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "reveal",
      "label": "the reveal",
      "to": "all",
      "text": "Cards revealed: seat 1 {players[0].played_card}, seat 2 {players[1].played_card}, seat 3 {players[2].played_card}, seat 4 {players[3].played_card}."
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "the trick is scored",
      "do": [
        {
          "set": {
            "key": "best_rank",
            "value": {
              "calc": "max([(rank_ace if p.played_card[0] == 'A' else rank_king if p.played_card[0] == 'K' else rank_queen if p.played_card[0] == 'Q' else rank_jack if p.played_card[0] == 'J' else rank_nine if p.played_card[0] == '9' else rank_eight) for p in players if p.played_card[1] == led_suit])"
            }
          }
        },
        {
          "set": {
            "key": "trick_winner",
            "value": {
              "calc": "min([p.seat for p in players if p.played_card[1] == led_suit and (rank_ace if p.played_card[0] == 'A' else rank_king if p.played_card[0] == 'K' else rank_queen if p.played_card[0] == 'Q' else rank_jack if p.played_card[0] == 'J' else rank_nine if p.played_card[0] == '9' else rank_eight) == best_rank])"
            }
          }
        },
        {
          "set": {
            "key": "trick_points",
            "value": {
              "calc": "sum([(quinola_points if p.played_card == 'JH' else ace_points if p.played_card[0] == 'A' else king_points if p.played_card[0] == 'K' else queen_points if p.played_card[0] == 'Q' else jack_points if p.played_card[0] == 'J' else nine_points if p.played_card[0] == '9' else eight_points) for p in players])"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "trick_winner"
            },
            "key": "total",
            "value": {
              "calc": "trick_points"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "trick_winner"
            },
            "key": "tricks_this_hand",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "the sweeper",
      "do": [
        {
          "set": {
            "key": "sweeper",
            "value": {
              "calc": "trick_winner"
            },
            "if": {
              "calc": "(round - 1) % tricks_per_hand == 0"
            }
          }
        },
        {
          "set": {
            "key": "sweeper",
            "value": {
              "calc": "sweeper_none_code"
            },
            "if": {
              "calc": "(round - 1) % tricks_per_hand != 0 and trick_winner != sweeper"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "the winner leads next",
      "do": [
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "trick_winner"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "reveal",
      "label": "the totals",
      "to": "all",
      "text": "Seat {trick_winner} wins the trick and takes {trick_points} points. Totals: seat 1 {players[0].total}, seat 2 {players[1].total}, seat 3 {players[2].total}, seat 4 {players[3].total}."
    },
    {
      "use": "update",
      "phase": "end of hand",
      "label": "the reversis",
      "when": {
        "calc": "round % tricks_per_hand == 0 and sweeper != sweeper_none_code"
      },
      "do": [
        {
          "adjust": {
            "players": {
              "where": "you.seat == sweeper"
            },
            "key": "total",
            "value": {
              "calc": "0 - reversis_subtract"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat != sweeper"
            },
            "key": "total",
            "value": {
              "calc": "reversis_bonus_to_others"
            }
          }
        }
      ],
      "text": "Reversis! Seat {sweeper} took all {tricks_per_hand} tricks of hand {hand_number}: they subtract {reversis_subtract} and every other player adds {reversis_bonus_to_others}."
    },
    {
      "use": "check",
      "phase": "end of hand",
      "label": "after the last trick",
      "when": {
        "calc": "round >= total_rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round >= total_rounds"
      },
      "rank_by": "0 - you.total",
      "text": "Winner (lowest total): {result}. Final totals: Seat 1 {players[0].total}, Seat 2 {players[1].total}, Seat 3 {players[2].total}, Seat 4 {players[3].total}."
    }
  },
  "limits": {
    "rounds": 24,
    "rounds_max": 30,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "Quick Reversis is for four players, seats 1 to 4. Every player's total starts at 0; lower is better.\n\nThe deck has {deck_size} cards: A, K, Q, J, 9 and 8 in each of Spades (S), Hearts (H), Diamonds (D) and Clubs (C). Within a suit the ranking is A (highest), K, Q, J, 9, 8. There are no trumps. Cards are written like 'QH' (Queen of Hearts).\n\nCard points: each Ace counts {ace_points}, each King {king_points}, each Queen {queen_points} and each Jack {jack_points}. Nines count {nine_points} and eights {eight_points}. The exception is the Jack of Hearts (the Quinola, JH), which counts {quinola_points}. Each hand contains {points_per_hand} points in total.\n\nThe game has {hands} hands of {tricks_per_hand} tricks each, {total_rounds} rounds in all; each round is one trick.\n\nStart of a hand (rounds 1, 7, 13 and 19): the {deck_size} cards are shuffled and {
... (cut)

Why it was refused: it plays, but part of it does nothing: game attribute `full_deck` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "quick_reversis",
    "name": "Quick Reversis",
    "players": {
      "min": 4,
      "max": 4,
      "suggested": 4
    },
    "blurb": "Four hands of six tricks: avoid card points, unless you take every trick of a hand for a reversis. Lowest total wins."
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
        "key": "total",
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
        "key": "played_card",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "tricks_this_hand",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "follow",
        "visible": "ally",
        "type": "text",
        "initial": ""
      }
    ],
    "game": [
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": ["AS", "KS", "QS", "JS", "9S", "8S", "AH", "KH", "QH", "JH", "9H", "8H", "AD", "KD", "QD", "JD", "9D", "8D", "AC", "KC", "QC", "JC", "9C", "8C"]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "best_rank",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "lead_card",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hand_number",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "leader",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "led_suit",
        "visible": "public",
        "type": "text",
        "initial": ""
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
        "key": "sweeper",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 24
      },
      {
        "key": "cards_per_suit",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "suits",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "cards_dealt_per_player",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "hands",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "tricks_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "total_rounds",
        "visible": "public",
        "type": "number",
        "initial": 24
      },
      {
        "key": "ace_points",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "king_points",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "queen_points",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "jack_points",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "nine_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "eight_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "quinola_points",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "points_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 44
      },
      {
        "key": "reversis_subtract",
        "visible": "public",
        "type": "number",
        "initial": 44
      },
      {
        "key": "reversis_bonus_to_others",
        "visible": "public",
        "type": "number",
        "initial": 15
      },
      {
        "key": "rank_ace",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "rank_king",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "rank_queen",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "rank_jack",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "rank_nine",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "rank_eight",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "sweeper_none_code",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "totals start at zero",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "total",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "the deck",
      "do": [
        {
          "set": {
            "key": "deck",
            "value": ["AS", "KS", "QS", "JS", "9S", "8S", "AH", "KH", "QH", "JH", "9H", "8H", "AD", "KD", "QD", "JD", "9D", "8D", "AC", "KC", "QC", "JC", "9C", "8C"]
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "counters",
      "do": [
        {
          "set": {
            "key": "round",
            "value": 0
          }
        },
        {
          "set": {
            "key": "hand_number",
            "value": 0
          }
        },
        {
          "set": {
            "key": "sweeper",
            "value": {
              "calc": "sweeper_none_code"
            }
          }
        }
      ]
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "start",
      "label": "the next trick",
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
            "key": "played_card",
            "value": ""
          }
        },
        {
          "set": {
            "key": "lead_card",
            "value": ""
          }
        },
        {
          "set": {
            "key": "led_suit",
            "value": ""
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "start",
      "label": "a new hand is dealt",
      "when": {
        "calc": "(round - 1) % tricks_per_hand == 0"
      },
      "do": [
        {
          "adjust": {
            "key": "hand_number",
            "value": 1
          }
        },
        {
          "set": {
            "key": "deck",
            "value": ["AS", "KS", "QS", "JS", "9S", "8S", "AH", "KH", "QH", "JH", "9H", "8H", "AD", "KD", "QD", "JD", "9D", "8D", "AC", "KC", "QC", "JC", "9C", "8C"]
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
            "key": "tricks_this_hand",
            "value": 0
          }
        },
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "hand_number"
            }
          }
        },
        {
          "set": {
            "key": "sweeper",
            "value": {
              "calc": "sweeper_none_code"
            }
          }
        }
      ],
      "text": "Hand {hand_number} of {hands} is dealt: {cards_dealt_per_player} cards each. Seat {leader} leads the first trick."
    },
    {
      "use": "sync",
      "phase": "start",
      "label": "your hand",
      "mode": "self",
      "to": "all",
      "fields": [
        "hand",
        "total",
        "tricks_this_hand"
      ],
      "text": "Trick {round} (hand {hand_number} of {hands}). Seat {leader} leads. Sweeper: {sweeper} (0 means none). Your state:"
    },
    {
      "use": "ask",
      "phase": "lead",
      "label": "the lead",
      "to": {
        "where": "you.seat == leader"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "verify": {
        "bind": "lead"
      },
      "text": "You lead trick {round}. Play any one card from your hand face up; its suit becomes the led suit. The highest card of the led suit takes the trick and its points."
    },
    {
      "use": "update",
      "phase": "lead",
      "label": "the lead is played",
      "do": [
        {
          "set": {
            "key": "lead_card",
            "value": "$lead"
          }
        },
        {
          "remove": {
            "player": {
              "calc": "leader"
            },
            "key": "hand",
            "value": {
              "calc": "lead_card"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "leader"
            },
            "key": "played_card",
            "value": {
              "calc": "lead_card"
            }
          }
        },
        {
          "set": {
            "key": "led_suit",
            "value": {
              "calc": "lead_card[1]"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "lead",
      "label": "the lead is announced",
      "to": "all",
      "text": "Seat {leader} leads {lead}; the led suit is {led_suit}."
    },
    {
      "use": "update",
      "phase": "follow",
      "label": "what each follower may play",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "follow",
            "value": ""
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat != leader"
            },
            "key": "offer",
            "value": {
              "calc": "[c for c in you.hand if c[1] == led_suit] if any([c[1] == led_suit for c in you.hand]) else you.hand"
            }
          }
        }
      ]
    },
    {
      "use": "poll",
      "phase": "follow",
      "label": "the followers play",
      "to": {
        "where": "you.seat != leader"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "store": "follow",
      "text": "Seat {leader} led {lead} (suit {led_suit}). Choose one card face down. If you hold a card of the led suit you must play one (only those are offered); if you hold none you may play any card. Nobody sees your choice until all cards are revealed together."
    },
    {
      "use": "update",
      "phase": "follow",
      "label": "the followers' cards are played",
      "do": [
        {
          "remove": {
            "players": {
              "where": "you.seat != leader"
            },
            "key": "hand",
            "value": {
              "calc": "you.follow"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat != leader"
            },
            "key": "played_card",
            "value": {
              "calc": "you.follow"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "reveal",
      "label": "the reveal",
      "to": "all",
      "text": "Cards revealed: seat 1 {players[0].played_card}, seat 2 {players[1].played_card}, seat 3 {players[2].played_card}, seat 4 {players[3].played_card}."
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "the trick is scored",
      "do": [
        {
          "set": {
            "key": "best_rank",
            "value": {
              "calc": "max([(rank_ace if p.played_card[0] == 'A' else rank_king if p.played_card[0] == 'K' else rank_queen if p.played_card[0] == 'Q' else rank_jack if p.played_card[0] == 'J' else rank_nine if p.played_card[0] == '9' else rank_eight) for p in players if p.played_card[1] == led_suit])"
            }
          }
        },
        {
          "set": {
            "key": "trick_winner",
            "value": {
              "calc": "min([p.seat for p in players if p.played_card[1] == led_suit and (rank_ace if p.played_card[0] == 'A' else rank_king if p.played_card[0] == 'K' else rank_queen if p.played_card[0] == 'Q' else rank_jack if p.played_card[0] == 'J' else rank_nine if p.played_card[0] == '9' else rank_eight) == best_rank])"
            }
          }
        },
        {
          "set": {
            "key": "trick_points",
            "value": {
              "calc": "sum([(quinola_points if p.played_card == 'JH' else ace_points if p.played_card[0] == 'A' else king_points if p.played_card[0] == 'K' else queen_points if p.played_card[0] == 'Q' else jack_points if p.played_card[0] == 'J' else nine_points if p.played_card[0] == '9' else eight_points) for p in players])"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "trick_winner"
            },
            "key": "total",
            "value": {
              "calc": "trick_points"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "trick_winner"
            },
            "key": "tricks_this_hand",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "the sweeper",
      "do": [
        {
          "set": {
            "key": "sweeper",
            "value": {
              "calc": "trick_winner"
            },
            "if": {
              "calc": "(round - 1) % tricks_per_hand == 0"
            }
          }
        },
        {
          "set": {
            "key": "sweeper",
            "value": {
              "calc": "sweeper_none_code"
            },
            "if": {
              "calc": "(round - 1) % tricks_per_hand != 0 and trick_winner != sweeper"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "the winner leads next",
      "do": [
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "trick_winner"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "reveal",
      "label": "the totals",
      "to": "all",
      "text": "Seat {trick_winner} wins the trick and takes {trick_points} points. Totals: seat 1 {players[0].total}, seat 2 {players[1].total}, seat 3 {players[2].total}, seat 4 {players[3].total}."
    },
    {
      "use": "update",
      "phase": "end of hand",
      "label": "the reversis",
      "when": {
        "calc": "round % tricks_per_hand == 0 and sweeper != sweeper_none_code"
      },
      "do": [
        {
          "adjust": {
            "players": {
              "where": "you.seat == sweeper"
            },
            "key": "total",
            "value": {
              "calc": "0 - reversis_subtract"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat != sweeper"
            },
            "key": "total",
            "value": {
              "calc": "reversis_bonus_to_others"
            }
          }
        }
      ],
      "text": "Reversis! Seat {sweeper} took all {tricks_per_hand} tricks of hand {hand_number}: they subtract {reversis_subtract} and every other player adds {reversis_bonus_to_others}."
    },
    {
      "use": "check",
      "phase": "end of hand",
      "label": "after the last trick",
      "when": {
        "calc": "round >= total_rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round >= total_rounds"
      },
      "rank_by": "0 - you.total",
      "text": "Winner (lowest total): {result}. Final totals: Seat 1 {players[0].total}, Seat 2 {players[1].total}, Seat 3 {players[2].total}, Seat 4 {players[3].total}."
    }
  },
  "limits": {
    "rounds": 24,
    "rounds_max": 30,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "Quick Reversis is for four players, seats 1 to 4. Every player's total starts at 0; lower is better.\n\nThe deck has {deck_size} cards: A, K, Q, J, 9 and 8 in each of Spades (S), Hearts (H), Diamonds (D) and Clubs (C). Within a suit the ranking is A (highest), K, Q, J, 9, 8. There are no trumps. Cards are written like 'QH' (Queen of Hearts).\n\nCard points: each Ace counts {ace_points}, each King {king_points}, each Queen {queen_points} and each Jack {jack_points}. Nines count {nine_points} and eights {eight_points}. The exception is the Jack of Hearts (the Quinola, JH), which counts {quinola_points}. Each hand contains {points_per_hand} points in total.\n\nThe game has {hands} hands of {tricks_per_hand} tricks each, {total_rounds} rounds in all; each round is one trick.\n\nStart of a hand (rounds 1, 7, 13 and 19): the {deck_size} cards are shuffled and {cards_dealt_per_player} are dealt face down to each player. Each player sees only their own hand. The leader of the first trick of hand h is seat h. The sweeper is set to none (0).\n\nEach trick: (1) The leader plays any one card from their hand face up; its suit is the led suit, and it is announced. (2) The other three players each choose one card at the same moment, without seeing each other's choices. A player who holds a card of the led suit must play one (only those cards are offered); a player who holds none may play any card. (3) All cards are revealed together. (4) The highest card of the led suit wins the trick; cards of other suits never win. (5) The points of the 4 cards played are added up and the trick winner adds them to their total. (6) Played cards leave the game for the rest of the hand. (7) The sweeper is updated: on the first trick of a hand, the sweeper becomes the trick winner; on later tricks, if the trick winner is not the sweeper, the sweeper becomes none (0); if the trick winner is the sweeper, the sweeper stays. (8) The trick winner leads the next trick. (9) Every player's total is announced.\n\nEnd of a hand (after tricks 6, 12, 18 and 24): if the sweeper is a player (that player took all {tricks_per_hand} tricks, a reversis), that player subtracts {reversis_subtract} from their total, so the hand counts 0 for them, and each other player adds {reversis_bonus_to_others} to their total. If the sweeper is none, no totals are adjusted.\n\nThere is no table talk.\n\nAfter round {total_rounds} the game ends. The player with the lowest total wins. If two or more players tie for the lowest total, the game is a draw and they share the result."
}
```
````
