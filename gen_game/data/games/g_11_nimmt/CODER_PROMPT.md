# Task: write the XColos game file for "11 Nimmt: Two Hot Piles"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 4; set `meta.players` to {"min": 3, "max": 4, "suggested": 3} (the suggested size is the one the game plays best at).

CARDS. The deck has N cards numbered 1 to N: N = 30 with 3 players, N = 40 with 4 players.

OX-HEADS. Cards 11, 22 and 33 carry 3 ox-heads. Every other multiple of 5 (5, 10, 15, 20, 25, 30, 35, 40) carries 2. All other cards carry 1.

SETUP.
- Shuffle once.
- Deal each player a private hand of H cards: H = 9 with 3 players, H = 8 with 4 players.
- Turn the next two cards face up. They start Pile A and Pile B, each of size 1.
- The rest (1 card with 3 players, 6 with 4) are set aside unseen and take no part in the game.
- Everyone starts with penalty 0 and bulls 0.

INFORMATION. You see only your own hand. Everyone sees both piles (their cards, top card, size and ox total), every card played and every take, and all penalties and bulls.

FITTING. A card c fits a pile with top card t if d = (c - t) mod N is between 1 and 10 inclusive. Example with N = 30: on a top of 25, the cards 26 to 30 and 1 to 5 fit.

ROOM. A pile has room if it has fewer than 5 cards.

PLACEMENT. A placement is a card from your hand that fits a pile with room.

ROUNDS. The game lasts exactly H rounds. In round r the seats act one after another, starting with seat ((r - 1) mod number of players) + 1 and continuing in seat order, wrapping round. Each seat starts 3 times (3 players) or 2 times (4 players).

TURN. On your turn you choose exactly one card from your hand and one pile (A or B).
- If you hold at least one placement, you must choose a placement: the card goes on top of that pile. The pile's size rises by 1 and its ox total rises by the card's ox.
- If you hold no placement at all, you must TAKE. You choose any card and either pile, and then:
  1. Add that pile's ox total to your penalty.
  2. If the pile had 3 or more cards, gain 1 bull.
  3. Discard that pile's cards out of the game.
  4. Your chosen card becomes that pile's only card (size 1, ox equal to that card's).
- The other pile is unchanged.
- Every turn removes exactly one card from your hand, so all hands empty at the end of round H.

BULLS. Each bull is worth -2 at the end. Bulls are unlimited and never move between players.

END. After round H, each player's final score = penalty - 2 x bulls. Cards left in the two piles count against nobody.

How the winner is decided: The lowest final score (penalty minus twice bulls) wins. If two or more players tie for lowest, the game is a draw among them.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: 11 Nimmt: Two Hot Piles (3 to 4 players, best with 3)

Each turn, place one card from a hidden hand on one of two shared piles where it fits; a player with no legal placement must take a pile's ox-heads as penalty, though taking a pile of 3 or more cards earns a bull worth -2. The lowest penalty minus twice bulls wins.

STATE (every item below must exist in the file):
  - each player: hand (list, starts []); only its owner sees it. The cards (numbers) in this player's private hand
  - each player: penalty (number, starts 0); everyone sees it. Total ox-heads taken from piles
  - each player: bulls (number, starts 0); everyone sees it. Bulls earned by taking piles of 3 or more cards; each is worth -2 at the end
  - each player: score (number, starts 0); everyone sees it. Final score so far: penalty - 2 * bulls (lower is better)
  - the table: deck_size (number, starts 30); everyone sees it. N: 30 with 3 players, 40 with 4 players
  - the table: hand_size (number, starts 9); everyone sees it. H, which is also the number of rounds: 9 with 3 players, 8 with 4 players
  - the table: deck (list, starts []); hidden from all players. The shuffled undealt cards, used only during setup
  - the table: set_aside (list, starts []); hidden from all players. Cards set aside unseen that take no part in the game
  - the table: pile_a (list, starts []); everyone sees it. The cards in Pile A, in play order; the last card is the top
  - the table: pile_b (list, starts []); everyone sees it. The cards in Pile B, in play order; the last card is the top
  - the table: top_a (number, starts 0); everyone sees it. Top card of Pile A
  - the table: top_b (number, starts 0); everyone sees it. Top card of Pile B
  - the table: size_a (number, starts 0); everyone sees it. Number of cards in Pile A
  - the table: size_b (number, starts 0); everyone sees it. Number of cards in Pile B
  - the table: ox_a (number, starts 0); everyone sees it. Ox-head total of Pile A
  - the table: ox_b (number, starts 0); everyone sees it. Ox-head total of Pile B
  - the table: discarded (list, starts []); everyone sees it. Cards from taken piles, now out of the game
  - the table: round (number, starts 1); everyone sees it. Current round, from 1 to H
  - the table: current_seat (number, starts 1); everyone sees it. The seat whose turn it is
  - the table: turns_in_round (number, starts 0); hidden from all players. Scratch counter of turns taken this round
  - the table: last_play (text, starts ''); everyone sees it. Description of the latest turn: who played, which card, which pile, and whether it was a take
  - parameters, each kept as a table attribute: deck_size_3p = 30, deck_size_4p = 40, hand_size_3p = 9, hand_size_4p = 8, set_aside_3p = 1, set_aside_4p = 6, start_turns_per_seat_3p = 3, start_turns_per_seat_4p = 2, starting_piles = 2, starting_pile_size = 1, fit_min_distance = 1, fit_max_distance = 10, pile_room_limit = 5, bull_pile_threshold = 3, bull_value = 2, ox_special_cards = 3, ox_multiple_of_5 = 2, ox_other = 1, special_card_1 = 11, special_card_2 = 22, special_card_3 = 33, starting_penalty = 0, starting_bulls = 0

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Set deck_size N = 30 and hand_size H = 9 with 3 players, or N = 40 and H = 8 with 4 players.
  2. Fill deck with the cards 1 to N.
  3. Each card's ox value is 3 if it is 11, 22 or 33; otherwise 2 if it is a multiple of 5; otherwise 1.
  4. Deal each player H cards into hand, each one drawn at random from deck and removed from it.
  5. Draw one random card from deck into pile_a (top_a = that card, size_a = 1, ox_a = its ox), and one into pile_b (top_b, size_b = 1, ox_b = its ox). Both piles are public.
  6. Move every remaining deck card into set_aside (1 card with 3 players, 6 with 4). They are never seen and never used.
  7. Every player starts with penalty 0, bulls 0 and score 0, and round = 1.
  8. Sync each player's hand to that player only.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] table. What happens: current_seat = ((round - 1) mod number_of_players) + 1; turns_in_round = 0
  2. [ask] seat current_seat answers: One option naming a card from own hand and a pile, e.g. '17 on A'. If the seat holds at least one placement (card c fits pile X, meaning (c - top_X) mod N is between 1 and 10, and size_X < 5), only placements are offered. Otherwise every card in hand on A and on B is offered, each marked as a take.. What happens: Records the chosen card c and pile X
  3. [update] seat current_seat. What happens: Remove c from hand. If c fits X ((c - top_X) mod N in 1..10) and size_X < 5 (a placement): append c to pile_X, top_X = c, size_X += 1, ox_X += ox(c). Otherwise (a take): penalty += ox_X; if size_X >= 3 then bulls += 1; move all of pile_X into discarded; pile_X = [c], top_X = c, size_X = 1, ox_X = ox(c). The other pile is unchanged. Then score = penalty - 2 * bulls, and last_play describes the move.
  4. [tell] all players. What happens: Announce last_play, both piles (cards, top, size, ox total) and every player's penalty, bulls and score.
  5. [update] table. What happens: current_seat = (current_seat mod number_of_players) + 1; turns_in_round += 1
  6. [repeat] table. What happens: Repeat steps 2 to 5 until turns_in_round = number_of_players.
  7. [update] table. What happens: round += 1
  8. [sync] all players. What happens: Each player is sent their own hand and the public state.
  9. [check] table. What happens: If round > hand_size, end the game; otherwise continue.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. With 3 players the deck is cards 1 to 30 and each hand is 9 cards; with 4 players the deck is cards 1 to 40 and each hand is 8 cards.
  R2. Cards 11, 22 and 33 carry 3 ox-heads, every other multiple of 5 carries 2, and all other cards carry 1 (e.g. 11 -> 3, 25 -> 2, 7 -> 1).
  R3. At setup two face-up cards start pile_a and pile_b, each of size 1 with ox equal to its card; the remaining 1 (3 players) or 6 (4 players) cards go to set_aside and are never used.
  R4. All players start with penalty 0 and bulls 0.
  R5. A card c fits a pile with top t when (c - t) mod N is between 1 and 10 inclusive; with N = 30 and top 25, cards 26 to 30 and 1 to 5 fit, and 6 and 25 do not.
  R6. A pile has room when it holds fewer than 5 cards; a pile of 5 cards accepts no placement.
  R7. When a player holds at least one placement (a card that fits a pile with room), only placements are offered to them.
  R8. When a player places card c on pile X, c leaves the hand, becomes top_X, size_X rises by 1 and ox_X rises by ox(c); the other pile is unchanged.
  R9. When a player holds no placement, they must take: they may choose any card from hand and either pile.
  R10. When a player takes pile X, their penalty rises by ox_X, the pile's cards go to discarded, and the chosen card becomes the pile's only card (size 1, ox equal to its ox).
  R11. When the taken pile had 3 or more cards the taker gains 1 bull; when it had 1 or 2 cards they gain none.
  R12. In round r, seats act one after another starting with seat ((r - 1) mod number_of_players) + 1 and wrapping round in seat order.
  R13. Every turn removes exactly one card from the acting player's hand, so all hands are empty after round H.
  R14. The game ends after exactly H rounds (9 with 3 players, 8 with 4).
  R15. A player's final score is penalty - 2 * bulls; e.g. penalty 7 with 2 bulls scores 3.
  R16. Cards left in the two piles at the end count against nobody.
  R17. The player with the lowest final score wins; players tied for lowest share a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Your turn: choose a card and a pile | asked: seat current_seat | options: If the seat holds any placement: exactly the pairs 'c on A' where c is in hand, (c - top_a) mod N is in 1..10 and size_a < 5, plus the pairs 'c on B' meeting the same test against top_b and size_b. If the seat holds no placement: every card in hand paired with A and with B, each labelled as a take (e.g. 'take A with 17').

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round > hand_size
  - each player's standing: 2 * you.bulls - you.penalty (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's final score is penalty - 2 * bulls. The lowest final score wins, so ranking is by its negative. Players tied for lowest share the win, which is a draw among them.
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

- each player: `penalty` (number, visible: public, starts 0): Total ox-heads taken from piles
- each player: `bulls` (number, visible: public, starts 0): Bulls earned by taking piles of 3 or more cards; each is worth -2 at the end
- each player: `score` (number, visible: public, starts 0): Final score so far: penalty - 2 * bulls (lower is better)
- the table: `pile_a` (list, visible: public, starts []): The cards in Pile A, in play order; the last card is the top
- the table: `pile_b` (list, visible: public, starts []): The cards in Pile B, in play order; the last card is the top
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size_3p = 30, deck_size_4p = 40, hand_size_3p = 9, hand_size_4p = 8, set_aside_3p = 1, set_aside_4p = 6, start_turns_per_seat_3p = 3, start_turns_per_seat_4p = 2, starting_piles = 2, starting_pile_size = 1, fit_min_distance = 1, fit_max_distance = 10, pile_room_limit = 5, bull_pile_threshold = 3, bull_value = 2, ox_special_cards = 3, ox_multiple_of_5 = 2, ox_other = 1, special_card_1 = 11, special_card_2 = 22, special_card_3 = 33, starting_penalty = 0, starting_bulls = 0
- the game ends with ONE ending whose `rank_by` is `2 * you.bulls - you.penalty`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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

1) Fitting: compute d = ((c - t) mod N + N) mod N, using the active deck size for N (30 with 3 players, 40 with 4). A card fits only if fit_min_distance <= d <= fit_max_distance and the pile has fewer than pile_room_limit cards. Build each seat's offer from this test: if any placement exists, offer only placements; otherwise offer only takes (any card on either pile). Check that card 6 on a top of 25 is refused, and that 27 and 5 are accepted. 2) Ox values: ox_values is stored with card 1 at position 0, so look up card c at position c-1, or store it 1-indexed with a padding entry at position 0. Taking [25] must add 2 and taking [11] must add 3. Also make sure each pile's ox total is set from the starting card at setup and updated with the correct value on every placement and take. 3) Room: a pile with 5 cards must never be offered for placement, and a pile with 4 cards must be. 4) When a test seeds hands and piles through 'given', recompute the derived values from those piles before the first turn: top, size and ox total of each pile, and each seat's offer. The R5, R6 and R7 failures show stale or incorrect values (pile_a became [16, 17] when [25, 5] was expected). Keep score = penalty - bull_value * bulls, and keep every parameter as its own attribute.
