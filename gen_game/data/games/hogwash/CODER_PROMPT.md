# Task: write the XColos game file for "Hogwash: Six Ranks"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

SETUP. The deck has 24 cards: ranks 1 to 6, four copies of each. Shuffle and deal 8 cards to each of seats 1, 2 and 3. Hands are private. Everyone always knows every hand size and the pile size. The central pile starts empty; its cards are face down. Each player has two public counters starting at 0: CATCHES (correct challenges) and CAUGHT (times caught bluffing).

ROUNDS. The game lasts exactly 24 rounds. In round r the active player is seat ((r-1) mod 3)+1 and the required rank is ((r-1) mod 6)+1. As a result, seat 1 always faces ranks 1 and 4, seat 2 faces ranks 2 and 5, and seat 3 faces ranks 3 and 6. Each seat is active 8 times.

EACH ROUND:
1. Announce the round, the active player and the required rank.
2. If the active player holds 0 cards, they skip; go to step 8. Otherwise the active player privately chooses k from 1 to 4. If k exceeds their hand size, k becomes their hand size. They may add one short public statement, which may be untrue.
3. The engine moves k cards from the active player's hand onto the top of the pile. It takes cards of the required rank first, up to k. If more are needed, it takes cards of the next rank up, then the next, counting 6 as followed by 1. The play is TRUE if all k cards are the required rank; otherwise it is a BLUFF. This is recorded privately.
4. Announce: 'Seat X claims k cards of rank R', plus the statement.
5. Simultaneous poll: each of the two other players secretly chooses Trust or Challenge. The choices are revealed together.
6. If anyone challenged, reveal the k played cards to all.
   (a) If the play was a BLUFF: the active player takes the entire pile into their hand, and the pile becomes empty. The active player's CAUGHT increases by 1. Each challenger's CATCHES increases by 1.
   (b) If the play was TRUE and there was one challenger: that challenger takes the entire pile into their hand.
   (c) If the play was TRUE and there were two challengers: shuffle the pile. Each challenger takes half of it, rounded down. If one card remains, it is removed from the game face down. The pile becomes empty.
7. If both players chose Trust, nothing happens. The cards stay face down in the pile, true or not.
8. Announce every player's hand size, the pile size and all CATCHES and CAUGHT counters.
9. If round 24 has been played, the game ends.

A player holding 0 cards still answers every poll. Trusting can never give them cards.

How the winner is decided: After round 24, the player holding the fewest cards wins. If several players tie for fewest, the one with the most CATCHES wins. If still tied, the one with the fewest CAUGHT wins. If still tied, the game is a draw among those players.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Hogwash: Six Ranks (3 to 3 players, best with 3)

Three players take turns face-down dumping 1 to 4 cards that they claim are the required rank. The others secretly trust or challenge, and whoever holds the fewest cards after 24 rounds wins.

STATE (every item below must exist in the file):
  - each player: hand (list, starts '8 cards dealt from deck'); only its owner sees it. the ranks of the cards this player holds
  - each player: hand_size (number, starts 8); everyone sees it. number of cards in hand, kept equal to the length of hand
  - each player: catches (number, starts 0); everyone sees it. CATCHES: challenges this player made against a bluff
  - each player: caught (number, starts 0); everyone sees it. CAUGHT: times this player was caught bluffing
  - each player: response (text, starts ''); only its owner sees it. this round's Trust or Challenge answer, revealed to all after the poll
  - the table: deck (list, starts '24 cards: ranks 1-6, four of each'); hidden from all players. undealt cards, empty after the deal
  - the table: pile (list, starts []); hidden from all players. the face-down central pile
  - the table: pile_size (number, starts 0); everyone sees it. number of cards in the pile
  - the table: removed (list, starts []); hidden from all players. cards removed from the game face down
  - the table: round (number, starts 0); everyone sees it. current round number r
  - the table: active_seat (number, starts 0); everyone sees it. ((round-1) mod 3)+1
  - the table: required_rank (number, starts 0); everyone sees it. ((round-1) mod 6)+1
  - the table: skipped (bool, starts False); everyone sees it. true when the active player held 0 cards this round
  - the table: k (number, starts 0); everyone sees it. number of cards played this round, after clamping to hand size
  - the table: statement (text, starts ''); everyone sees it. the active player's optional public statement
  - the table: played (list, starts []); hidden from all players. the k cards played this round, revealed to all if challenged
  - the table: play_true (bool, starts False); hidden from all players. true if all k played cards equal required_rank, otherwise a bluff
  - the table: challengers (number, starts 0); everyone sees it. count of non-active players who answered Challenge this round
  - parameters, each kept as a table attribute: deck_size = 24, num_ranks = 6, copies_per_rank = 4, hand_size_initial = 8, num_seats = 3, total_rounds = 24, k_min = 1, k_max = 4, turns_per_seat = 8, catches_initial = 0, caught_initial = 0, pile_initial_size = 0, rank_weight_hand = 10000, rank_weight_catches = 100, rank_weight_caught = 1

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Build the deck list with 24 cards: ranks 1 to 6, four copies of each.
  2. Deal 8 cards at random from deck into the hand of each of seats 1, 2 and 3, removing each card from deck; set each hand_size to 8.
  3. Set pile to empty, pile_size to 0, and every player's catches and caught to 0.
  4. Sync each player's own hand to them; hand sizes, pile size and counters are public.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] table. What happens: round += 1; active_seat = ((round-1) mod 3)+1; required_rank = ((round-1) mod 6)+1; skipped = (hand_size of active_seat == 0); k = 0; statement = ''; played = []; challengers = 0; every response = ''
  2. [tell] all players. What happens: announce 'Round {round}: Seat {active_seat} must play rank {required_rank}' (plus 'and skips, holding 0 cards' when skipped)
  3. [sync] all players. What happens: each player sees their own hand
  4. [ask] seat active_seat, when skipped is false answers: a whole number from 1 to 4. What happens: k = min(answer, hand_size of active seat)
  5. [ask] seat active_seat, when skipped is false answers: short text, may be empty, may be untrue. What happens: statement = answer
  6. [update] table, when skipped is false. What happens: move k cards from the active player's hand to played and onto the top of pile: first cards equal to required_rank, then rank required_rank+1, and so on, wrapping 6 to 1, until k are taken; hand_size -= k; pile_size += k; play_true = (count of cards in played equal to required_rank == k)
  7. [tell] all players, when skipped is false. What happens: announce 'Seat {active_seat} claims {k} cards of rank {required_rank}. Statement: {statement}'
  8. [poll] every seat except active_seat, simultaneously, when skipped is false (including players holding 0 cards) answers: one of: Trust, Challenge. What happens: response = answer for each polled player; then reveal all responses together; challengers = count of polled players with response == Challenge
  9. [tell] all players, when skipped is false and challengers > 0. What happens: reveal the contents of played to everyone
  10. [update] table, when skipped is false and challengers > 0 and play_true is false. What happens: append all of pile to the active player's hand; pile = []; pile_size = 0; active player's caught += 1; each player with response == Challenge: catches += 1; refresh hand_size
  11. [update] table, when skipped is false and challengers == 1 and play_true is true. What happens: append all of pile to the hand of the player with response == Challenge; pile = []; pile_size = 0; refresh hand_size
  12. [update] table, when skipped is false and challengers == 2 and play_true is true. What happens: shuffle pile; each challenger draws floor(pile_size/2) cards at random from pile into hand; if 1 card remains, move it to removed; pile = []; pile_size = 0; refresh hand_size
  13. [tell] all players. What happens: announce every player's hand_size, pile_size, and every player's catches and caught
  14. [check] table. What happens: if round >= 24, end the game; otherwise continue

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, the deck holds 24 cards (ranks 1-6, four of each) and each of seats 1, 2 and 3 is dealt 8 cards into hand, leaving deck empty.
  R2. When the game starts, pile_size is 0 and every player's catches and caught are 0.
  R3. When round r begins, then active_seat = ((r-1) mod 3)+1 and required_rank = ((r-1) mod 6)+1; e.g. round 4 has seat 1 and rank 4, round 6 has seat 3 and rank 6.
  R4. When the active player holds 0 cards, then they are not asked for k, no cards move, no poll is held, and the round goes straight to the announcement.
  R5. When the active player chooses k greater than their hand size, then k becomes their hand size (e.g. choosing 4 with 2 cards plays 2).
  R6. When k cards are played, then cards of the required rank are taken first, then the next rank up, wrapping 6 to 1; e.g. required rank 5, k=3, hand {5,6,1,2} plays 5,6,1.
  R7. When all k played cards equal the required rank, then the play is TRUE; otherwise it is a BLUFF.
  R8. When cards are played, then the active player's hand_size falls by k and pile_size rises by k.
  R9. When the claim is announced, then it reads 'Seat X claims k cards of rank R' plus the active player's statement.
  R10. When the claim is made, then exactly the two non-active seats are polled simultaneously with options Trust and Challenge, including a player holding 0 cards.
  R11. When at least one player challenges, then the k played cards are revealed to all players.
  R12. When a BLUFF is challenged, then the active player adds the whole pile to their hand, pile_size becomes 0, the active player's caught rises by 1, and each challenger's catches rises by 1.
  R13. When a TRUE play is challenged by exactly one player, then that challenger adds the whole pile to their hand and pile_size becomes 0; no catches or caught change.
  R14. When a TRUE play is challenged by both players, then each challenger gets floor(pile_size/2) random pile cards, any 1 leftover card is removed from the game, and pile_size becomes 0 (e.g. pile 7: each gets 3 and 1 is removed).
  R15. When both players choose Trust, then no hand changes and the played cards stay in the pile face down.
  R16. When a player chooses Trust, then that choice never adds cards to their hand.
  R17. When a round ends, then every hand_size, pile_size, and all catches and caught are announced.
  R18. When round 24 has been played, then the game ends.
  R19. When the game ends, then the player with the fewest cards wins; ties go to most catches, then fewest caught, and players still tied share the win.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - How many cards (k) do you play? | asked: the active seat, only when it holds at least 1 card | options: a whole number 1 to 4 (clamped to hand size afterwards); seats that are not active are not asked
  - Optional public statement | asked: the active seat, only when it holds at least 1 card | options: short free text, may be empty or untrue
  - Trust or Challenge the claim | asked: the two seats other than the active seat, whatever their hand size | options: Trust, Challenge; the active seat is not asked

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round >= 24
  - each player's standing: 0 - you.hand_size * 10000 + you.catches * 100 - you.caught (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Fewest cards in hand wins. Ties go to the most CATCHES, then to the fewest CAUGHT. Players still level share the win, which is the source's draw.
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

- each player: `hand_size` (number, visible: public, starts 8): number of cards in hand, kept equal to the length of hand
- each player: `catches` (number, visible: public, starts 0): CATCHES: challenges this player made against a bluff
- each player: `caught` (number, visible: public, starts 0): CAUGHT: times this player was caught bluffing
- the table: `pile_size` (number, visible: public, starts 0): number of cards in the pile
- the table: `round` (number, visible: public, starts 0): current round number r
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 24, num_ranks = 6, copies_per_rank = 4, hand_size_initial = 8, num_seats = 3, total_rounds = 24, k_min = 1, k_max = 4, turns_per_seat = 8, catches_initial = 0, caught_initial = 0, pile_initial_size = 0, rank_weight_hand = 10000, rank_weight_catches = 100, rank_weight_caught = 1
- the game ends with ONE ending whose `rank_by` is `0 - you.hand_size * 10000 + you.catches * 100 - you.caught`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
