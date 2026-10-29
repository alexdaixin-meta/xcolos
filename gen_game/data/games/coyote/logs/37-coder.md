# 37 coder

- time: 2026-10-27T09:29:16+00:00 (157.8s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 fab48c4db43668c6, reply sha256 d26b7e75bf4323e0

## Sent

````
# Task: write the XColos game file for "Coyote: Around the Fire"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 4; set `meta.players` to {"min": 3, "max": 4, "suggested": 4} (the suggested size is the one the game plays best at).

R1 Setup. Seats are numbered 1 to N clockwise (N is 3 or 4). Every player starts with 0 tokens and is alive. opener_seat = 1, hand_active = no, round = 1.

R2 Deck. The deck has exactly 20 cards:
- one −2
- two −1
- three 0
- three 1
- three 2
- three 3
- two 4
- two 5
- one special card, Max→0

R3 Start of a round. If hand_active is no, a new hand begins:
- The deck is restored to all 20 cards and shuffled.
- Each alive player is dealt exactly 1 card face-down.
- Each player is privately told the card of every other alive player, never their own.
- current_declaration is set to none and hand_active to yes.
- Everyone is told that a new hand begins and who opens it.
If hand_active is already yes, the hand in progress simply continues.

R4 Turn order. In every round the alive players take exactly one turn each:
- The first turn goes to the player in opener_seat, then each next alive player clockwise, so a round has as many turns as there are alive players (at most 4).
- The order is the same in every round of a hand, so a hand passes around the table lap after lap.
- If Coyote is called, the hand ends and any remaining turns of that round are skipped.
Before each turn, all players are shown the current declaration, who made it, and every declaration made so far this hand.

R5 A turn.
(a) If there is no declaration yet this hand, the player must declare a whole number from −3 to 20.
(b) Otherwise the player either declares a whole number at least current_declaration + 1 and at most 20, or calls Coyote. If current_declaration is 20, the player must call Coyote.
(c) A declaration makes that player the current declarer and the number the current declaration.

R6 True total. All cards are revealed to everyone.
- Add all card values, counting Max→0 as 0.
- If Max→0 was dealt, the single highest other dealt card counts as 0 instead, provided its value is positive. If several cards tie for highest, only one of them is cancelled.

R7 Resolving Coyote. Compute the true total.
- If the true total is less than the current declaration, the current declarer loses the hand.
- Otherwise the caller loses the hand.
The loser gains 1 token. All cards, the true total and the loser are announced to everyone. hand_active becomes no.

R8 Elimination. A player with 3 tokens is eliminated. They receive no more cards and are skipped in turn order.

R9 Next opener. After every hand, opener_seat moves to the next alive player clockwise from the current opener, whoever lost. If the current opener was just eliminated, it moves to the next alive player clockwise from their seat.

R10 End. The game ends immediately when only one player is alive, and that player wins. If round 40 ends first, any unfinished hand is discarded without a token. The alive player with the fewest tokens then wins; if two or more alive players tie for fewest, the game is a draw.

There is no table talk: declarations and calls are the only communication.

How the winner is decided: Be the last player not eliminated (3 tokens eliminate). If 40 rounds pass with more than one player alive, the alive player with the fewest tokens wins, and a tie for fewest is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Coyote: Around the Fire (3 to 4 players, best with 4)

Each player sees every card but their own. Players raise a claim about the table's total until someone calls Coyote, and whoever is wrong takes a token; three tokens and you are out.

STATE (every item below must exist in the file):
  - each player: seat (number, starts '1..N clockwise'); everyone sees it. seat number
  - each player: tokens (number, starts 0); everyone sees it. hands lost; at 3 the player is eliminated (the score, lower is better)
  - each player: alive (bool, starts True); everyone sees it. false once the player has 3 tokens
  - each player: card (number); everyone but its owner sees it. this hand's face-down card: -2..5, or 100 for Max→0; null if not dealt. Every other player sees it, the owner never does
  - the table: deck (list, starts [-2, -1, -1, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 5, 5, 100]); hidden from all players. undealt cards of the current hand
  - the table: opener_seat (number, starts 1); everyone sees it. seat that takes the first turn of every round of the current hand
  - the table: hand_active (bool, starts False); everyone sees it. whether a hand is in progress
  - the table: round (number, starts 1); everyone sees it. round counter, up to 40
  - the table: has_declaration (bool, starts False); everyone sees it. false while current_declaration is none
  - the table: current_declaration (number); everyone sees it. the highest declaration this hand (none at hand start)
  - the table: current_declarer (number); everyone sees it. seat that made current_declaration
  - the table: declarations (list, starts []); everyone sees it. every (seat, number) declared this hand, in order
  - the table: coyote_called (bool, starts False); everyone sees it. set when a player calls Coyote this hand
  - the table: caller (number); everyone sees it. seat that called Coyote
  - the table: true_total (number); everyone sees it. true total of the resolved hand
  - the table: last_loser (number); everyone sees it. seat that lost the last hand
  - the table: alive_count (number, starts 'N'); everyone sees it. number of alive players
  - parameters, each kept as a table attribute: deck_size = 20, count_minus2 = 1, count_minus1 = 2, count_0 = 3, count_1 = 3, count_2 = 3, count_3 = 3, count_4 = 2, count_5 = 2, count_max0 = 1, max0_code = 100, cards_per_player = 1, first_declaration_min = -3, declaration_max = 20, raise_min_step = 1, tokens_to_eliminate = 3, token_per_loss = 1, max_rounds = 40, first_opener_seat = 1

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seats are numbered 1 to N clockwise (N is 3 or 4).
  2. Every player gets tokens = 0 and alive = true, and alive_count = N.
  3. Set opener_seat = 1, hand_active = false and round = 1.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: New hand. Reset deck to the 20 cards. Set every player's card to null. For each alive player, draw 1 card at random from deck into that player's card and remove it from deck. Set has_declaration = false, current_declaration = none, current_declarer = none, declarations = [], coyote_called = false, caller = none, hand_active = true.
  2. [sync] all players. What happens: Each player is sent the cards of every other alive player (card is visible to others) and never their own.
  3. [tell] all players. What happens: Announce: 'A new hand begins; seat {opener_seat} opens.'
  4. [tell] all players. What happens: Show current_declaration, current_declarer and declarations.
  5. [ask] the 1st alive seat clockwise starting at opener_seat answers: if has_declaration is false: a whole number from -3 to 20; otherwise one of 'coyote' or a whole number from current_declaration+1 to 20 (only 'coyote' if current_declaration == 20). What happens: On a number: current_declaration = number, current_declarer = this seat, has_declaration = true, append (seat, number) to declarations. On 'coyote': coyote_called = true, caller = this seat.
  6. [tell] all players. What happens: Show current_declaration, current_declarer and declarations.
  7. [ask] the 2nd alive seat clockwise starting at opener_seat answers: as in the 1st turn. What happens: as in the 1st turn
  8. [tell] all players. What happens: Show current_declaration, current_declarer and declarations.
  9. [ask] the 3rd alive seat clockwise starting at opener_seat answers: as in the 1st turn. What happens: as in the 1st turn
  10. [tell] all players. What happens: Show current_declaration, current_declarer and declarations.
  11. [ask] the 4th alive seat clockwise starting at opener_seat answers: as in the 1st turn. What happens: as in the 1st turn
  12. [update] all players. What happens: Work out the true total. Let S = the sum of all dealt cards that are not 100, and M = the highest dealt card that is not 100. true_total = S - (M if some dealt card == 100 and M > 0, else 0); only one copy of a tied highest card is cancelled. If true_total < current_declaration, then last_loser = current_declarer, else last_loser = caller. last_loser.tokens += 1. If last_loser.tokens >= 3, then last_loser.alive = false and alive_count -= 1. opener_seat = the next alive seat clockwise from the current opener_seat (if that opener was just eliminated, the next alive seat clockwise from their seat). hand_active = false.
  13. [tell] all players. What happens: Announce every alive player's card, true_total, last_loser and the tokens, and any elimination.
  14. [check] all players. What happens: End the game if alive_count == 1.
  15. [update] all players. What happens: round += 1
  16. [check] all players. What happens: End the game if round > 40. Any unfinished hand is discarded and no token is given.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, then every player has tokens 0 and alive true, opener_seat is 1, hand_active is false and round is 1.
  R2. When a new hand begins, then deck is reset to exactly 20 cards: one -2, two -1, three 0, three 1, three 2, three 3, two 4, two 5 and one Max→0 (code 100).
  R3. When a round starts with hand_active false, then each alive player gets exactly 1 card drawn from deck, those cards leave deck, and eliminated players get no card.
  R4. When cards are dealt, then each player sees the card of every other alive player and never their own.
  R5. When a new hand begins, then current_declaration is none, declarations is empty, hand_active becomes true and everyone is told who opens.
  R6. When a round starts with hand_active true, then no cards are dealt and the hand continues with the same cards and declarations.
  R7. When a round is played, then each alive player takes at most one turn, starting at opener_seat and going clockwise through alive seats only.
  R8. When Coyote is called, then the remaining turns of that round are skipped.
  R9. When no declaration has been made this hand, then the player to act must declare a whole number from -3 to 20 and may not call Coyote.
  R10. When a declaration exists, then the player to act may declare a whole number from current_declaration+1 to 20 or call Coyote.
  R11. When current_declaration is 20, then the player to act must call Coyote.
  R12. When a player declares a number, then current_declaration becomes that number, current_declarer becomes that seat, and the pair is appended to declarations.
  R13. When Coyote is called and Max→0 is not dealt, then true_total is the sum of the dealt cards (for example 3, 5 and -1 give 7).
  R14. When Coyote is called and Max→0 is dealt with highest other card 5, then that 5 counts as 0 (for example Max→0, 5 and 2 give 2).
  R15. When Max→0 is dealt with two 3s as the highest other cards, then only one 3 is cancelled (for example Max→0, 3, 3 and 1 give 4).
  R16. When Max→0 is dealt and the highest other card is 0 or less, then nothing is cancelled (for example Max→0, -1 and 0 give -1).
  R17. When Coyote is called and true_total < current_declaration, then the current declarer gains 1 token.
  R18. When Coyote is called and true_total >= current_declaration, then the caller gains 1 token.
  R19. When a hand is resolved, then all cards, true_total and the loser are announced to everyone, and hand_active becomes false.
  R20. When a player reaches 3 tokens, then alive becomes false, they get no more cards and they are skipped in turn order.
  R21. When a hand ends, then opener_seat moves to the next alive seat clockwise from the current opener, whoever lost; if the opener was eliminated, it moves to the next alive seat clockwise from their seat.
  R22. When only one player is alive, then the game ends immediately and that player wins.
  R23. When round 40 ends with two or more players alive, then any unfinished hand is discarded with no token, and the alive player with the fewest tokens wins.
  R24. When round 40 ends and two or more alive players tie for fewest tokens, then the game is a draw between them.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - A turn in a hand with no declaration yet | asked: the alive seat whose turn it is | options: a whole number from -3 to 20; no Coyote
  - A turn with current_declaration D < 20 | asked: the alive seat whose turn it is | options: coyote, or a whole number from D+1 to 20
  - A turn with current_declaration 20 | asked: the alive seat whose turn it is | options: coyote only
  - Any turn | asked: eliminated seats | options: never asked

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: alive_count == 1 or round > 40
  - each player's standing: you.alive * 10 - you.tokens (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Eliminated players rank below every alive player. If only one player is alive, that player wins. If 40 rounds pass, the alive player with the fewest tokens wins, and alive players tied for fewest share the result (a draw).
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

- each player: `seat` (number, visible: public, starts '1..N clockwise'): seat number
- each player: `tokens` (number, visible: public, starts 0): hands lost; at 3 the player is eliminated (the score, lower is better)
- each player: `alive` (bool, visible: public, starts True): false once the player has 3 tokens
- the table: `opener_seat` (number, visible: public, starts 1): seat that takes the first turn of every round of the current hand
- the table: `round` (number, visible: public, starts 1): round counter, up to 40
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 20, count_minus2 = 1, count_minus1 = 2, count_0 = 3, count_1 = 3, count_2 = 3, count_3 = 3, count_4 = 2, count_5 = 2, count_max0 = 1, max0_code = 100, cards_per_player = 1, first_declaration_min = -3, declaration_max = 20, raise_min_step = 1, tokens_to_eliminate = 3, token_per_loss = 1, max_rounds = 40, first_opener_seat = 1
- the game ends with ONE ending whose `rank_by` is `you.alive * 10 - you.tokens`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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

1) At the start of every new hand (whenever hand_active is no at round start), rebuild the deck from the count parameters before dealing: count_minus2 × −2, count_minus1 × −1, count_0 × 0, count_1 × 1, count_2 × 2, count_3 × 3, count_4 × 4, count_5 × 5, and count_max0 × max0_code. Do this in the hand-start steps, not only at setup. Then deal cards_per_player to each alive player by removing the cards from the deck. 2) In Coyote resolution, the declarer loses only if true_total < current_declaration (strict); otherwise the caller loses, so a total equal to the declaration makes the caller lose. 3) Check true_total: sum all dealt cards, counting max0_code as 0. If Max→0 was dealt, subtract the single highest other card once, and only if it is positive (Max→0, 3, 3, 1 gives 4; 3, 5, −1 gives 7). Make sure the code 100 is never added to the sum. 4) Keep the raise range at current_declaration + raise_min_step up to declaration_max. After declarations of 6 and then 7, offering 8 to the next seat is correct.

````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "coyote_around_the_fire",
    "name": "Coyote: Around the Fire",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 4
    },
    "blurb": "You see every card but your own. Raise the claim about the table's total or call Coyote; whoever is wrong takes a token, and three tokens put you out."
  },
  "statuses": [
    {
      "id": "playing",
      "acts": true,
      "initial": true
    },
    {
      "id": "out",
      "acts": false
    }
  ],
  "attributes": {
    "player": [
      {
        "key": "seat",
        "visible": "public",
        "type": "number"
      },
      {
        "key": "tokens",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "alive",
        "visible": "public",
        "type": "bool",
        "initial": true
      },
      {
        "key": "card",
        "visible": "others",
        "type": "number"
      }
    ],
    "game": [
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": [-2, -1, -1, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 5, 5, 100]
      },
      {
        "key": "opener_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "hand_active",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "has_declaration",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "current_declaration",
        "visible": "public",
        "type": "number"
      },
      {
        "key": "current_declarer",
        "visible": "public",
        "type": "number"
      },
      {
        "key": "declarations",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "coyote_called",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "caller",
        "visible": "public",
        "type": "number"
      },
      {
        "key": "true_total",
        "visible": "public",
        "type": "number"
      },
      {
        "key": "last_loser",
        "visible": "public",
        "type": "number"
      },
      {
        "key": "alive_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "revealed",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "token_board",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "order",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "turn_idx",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "turn_seat",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "new_hand",
        "visible": "none",
        "type": "bool",
        "initial": false
      },
      {
        "key": "just_out",
        "visible": "none",
        "type": "bool",
        "initial": false
      },
      {
        "key": "rounds_done",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "count_minus2",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "count_minus1",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "count_0",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "count_1",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "count_2",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "count_3",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "count_4",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "count_5",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "count_max0",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "max0_code",
        "visible": "public",
        "type": "number",
        "initial": 100
      },
      {
        "key": "cards_per_player",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "first_declaration_min",
        "visible": "public",
        "type": "number",
        "initial": -3
      },
      {
        "key": "declaration_max",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "raise_min_step",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "tokens_to_eliminate",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "token_per_loss",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "max_rounds",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "first_opener_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the table is set",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "seat",
            "value": {
              "calc": "you.seat"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "tokens",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "alive",
            "value": true
          }
        },
        {
          "set": {
            "key": "alive_count",
            "value": {
              "calc": "len(players)"
            }
          }
        },
        {
          "set": {
            "key": "opener_seat",
            "value": {
              "calc": "first_opener_seat"
            }
          }
        },
        {
          "set": {
            "key": "hand_active",
            "value": false
          }
        },
        {
          "set": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "key": "rounds_done",
            "value": 0
          }
        }
      ]
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "deal",
      "label": "a new hand",
      "when": {
        "calc": "not hand_active"
      },
      "do": [
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "[-2] * count_minus2 + [-1] * count_minus1 + [0] * count_0 + [1] * count_1 + [2] * count_2 + [3] * count_3 + [4] * count_4 + [5] * count_5 + [max0_code] * count_max0"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "card",
            "value": null
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
            },
            "if": {
              "calc": "len(players) >= 1 and players[0].alive"
            }
          }
        },
        {
          "set": {
            "player": 1,
            "key": "card",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 1 and players[0].alive"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 1 and players[0].alive"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
            },
            "if": {
              "calc": "len(players) >= 2 and players[1].alive"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "card",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 2 and players[1].alive"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 2 and players[1].alive"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
            },
            "if": {
              "calc": "len(players) >= 3 and players[2].alive"
            }
          }
        },
        {
          "set": {
            "player": 3,
            "key": "card",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 3 and players[2].alive"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 3 and players[2].alive"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
            },
            "if": {
              "calc": "len(players) >= 4 and players[3].alive"
            }
          }
        },
        {
          "set": {
            "player": 4,
            "key": "card",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 4 and players[3].alive"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 4 and players[3].alive"
            }
          }
        },
        {
          "set": {
            "key": "has_declaration",
            "value": false
          }
        },
        {
          "set": {
            "key": "current_declaration",
            "value": null
          }
        },
        {
          "set": {
            "key": "current_declarer",
            "value": null
          }
        },
        {
          "set": {
            "key": "declarations",
            "value": []
          }
        },
        {
          "set": {
            "key": "coyote_called",
            "value": false
          }
        },
        {
          "set": {
            "key": "caller",
            "value": null
          }
        },
        {
          "set": {
            "key": "hand_active",
            "value": true
          }
        },
        {
          "set": {
            "key": "order",
            "value": {
              "calc": "[x - 10 if x > 10 else x for x in sorted([p.seat + 10 if p.seat < opener_seat else p.seat for p in players if p.alive])]"
            }
          }
        },
        {
          "set": {
            "key": "new_hand",
            "value": true
          }
        }
      ]
    },
    {
      "use": "sync",
      "phase": "deal",
      "label": "the cards you can see",
      "when": {
        "calc": "new_hand"
      },
      "to": "acting",
      "mode": "others",
      "fields": [
        "card"
      ],
      "text": "A card you can see (100 means Max→0):"
    },
    {
      "use": "tell",
      "phase": "deal",
      "label": "the hand opens",
      "when": {
        "calc": "new_hand"
      },
      "to": "all",
      "text": "A new hand begins; seat {opener_seat} opens."
    },
    {
      "use": "update",
      "phase": "turns",
      "label": "the round begins",
      "do": [
        {
          "set": {
            "key": "turn_idx",
            "value": 0
          }
        },
        {
          "set": {
            "key": "turn_seat",
            "value": {
              "calc": "order[0] if len(order) > 0 else 0"
            }
          }
        },
        {
          "set": {
            "key": "new_hand",
            "value": false
          }
        }
      ]
    },
    {
      "use": "repeat",
      "phase": "turns",
      "label": "the turns",
      "until": {
        "calc": "coyote_called or turn_idx >= len(order)"
      },
      "max": 5,
      "steps": [
        {
          "use": "tell",
          "label": "the declarations so far",
          "to": "all",
          "text": "Seat {turn_seat} to act. Current declaration: {current_declaration}, made by seat {current_declarer}. Declarations this hand [seat, number]: {declarations}."
        },
        {
          "use": "update",
          "label": "coyote is forced",
          "when": {
            "calc": "has_declaration and not coyote_called and current_declaration >= declaration_max"
          },
          "do": [
            {
              "set": {
                "key": "coyote_called",
                "value": true
              }
            },
            {
              "set": {
                "key": "caller",
                "value": {
                  "calc": "turn_seat"
                }
              }
            }
          ],
          "text": "The declaration is at {declaration_max}, so seat {turn_seat} must call Coyote, and does."
        },
        {
          "use": "ask",
          "label": "raise or call coyote",
          "when": {
            "calc": "has_declaration and not coyote_called and current_declaration < declaration_max"
          },
          "to": {
            "where": "you.seat == turn_seat"
          },
          "answer": {
            "type": "number",
            "min": {
              "calc": "current_declaration + raise_min_step"
            },
            "max": {
              "calc": "declaration_max"
            },
            "or": [
              "coyote"
            ]
          },
          "each": {
            "do": [
              {
                "set": {
                  "key": "coyote_called",
                  "value": true,
                  "if": {
                    "calc": "$answer == 'coyote'"
                  }
                }
              },
              {
                "set": {
                  "key": "caller",
                  "value": "$seat",
                  "if": {
                    "calc": "$answer == 'coyote'"
                  }
                }
              },
              {
                "set": {
                  "key": "current_declaration",
                  "value": "$answer",
                  "if": {
                    "calc": "$answer != 'coyote'"
                  }
                }
              },
              {
                "set": {
                  "key": "current_declarer",
                  "value": "$seat",
                  "if": {
                    "calc": "$answer != 'coyote'"
                  }
                }
              },
              {
                "append": {
                  "key": "declarations",
                  "value": {
                    "calc": "[$seat, $answer]"
                  },
                  "if": {
                    "calc": "$answer != 'coyote'"
                  }
                }
              }
            ]
          },
          "broadcast": {
            "to": "all",
            "text": "Seat {seat}: {value}."
          },
          "text": "The current declaration is {current_declaration} by seat {current_declarer}. Either declare a whole number from {current_declaration} + {raise_min_step} up to {declaration_max}, claiming the true total is at least that, or answer coyote to challenge the current declaration."
        },
        {
          "use": "ask",
          "label": "the opening declaration",
          "when": {
            "calc": "not has_declaration and not coyote_called"
          },
          "to": {
            "where": "you.seat == turn_seat"
          },
          "answer": {
            "type": "number",
            "min": {
              "calc": "first_declaration_min"
            },
            "max": {
              "calc": "declaration_max"
            }
          },
          "each": {
            "do": [
              {
                "set": {
                  "key": "current_declaration",
                  "value": "$answer"
                }
              },
              {
                "set": {
                  "key": "current_declarer",
                  "value": "$seat"
                }
              },
              {
                "set": {
                  "key": "has_declaration",
                  "value": true
                }
              },
              {
                "append": {
                  "key": "declarations",
                  "value": {
                    "calc": "[$seat, $answer]"
                  }
                }
              }
            ]
          },
          "broadcast": {
            "to": "all",
            "text": "Seat {seat} declares {value}."
          },
          "text": "Nobody has declared yet this hand. Declare a whole number from {first_declaration_min} to {declaration_max}: your claim that the true total of all dealt cards is at least that. You may not call Coyote yet."
        },
        {
          "use": "update",
          "label": "the next turn",
          "do": [
            {
              "adjust": {
                "key": "turn_idx",
                "value": 1
              }
            },
            {
              "set": {
                "key": "turn_seat",
                "value": {
                  "calc": "order[turn_idx] if turn_idx < len(order) else 0"
                }
              }
            }
          ]
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "coyote is resolved",
      "when": {
        "calc": "coyote_called"
      },
      "do": [
        {
          "set": {
            "key": "revealed",
            "value": {
              "calc": "[[p.seat, p.card] for p in players if p.alive]"
            }
          }
        },
        {
          "set": {
            "key": "true_total",
            "value": {
              "calc": "sum([p.card for p in players if p.alive and p.card != max0_code]) - (max([p.card for p in players if p.alive and p.card != max0_code]) if (max0_code in [p.card for p in players if p.alive]) and max([p.card for p in players if p.alive and p.card != max0_code]) > 0 else 0)"
            }
          }
        },
        {
          "set": {
            "key": "last_loser",
            "value": {
              "calc": "current_declarer if true_total < current_declaration else caller"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "last_loser"
            },
            "key": "tokens",
            "value": {
              "calc": "token_per_loss"
            }
          }
        },
        {
          "set": {
            "key": "just_out",
            "value": {
              "calc": "players[last_loser - 1].tokens >= tokens_to_eliminate"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "last_loser"
            },
            "key": "alive",
            "value": false,
            "if": {
              "calc": "just_out"
            }
          }
        },
        {
          "set_status": {
            "player": {
              "calc": "last_loser"
            },
            "to": "out",
            "if": {
              "calc": "just_out"
            },
            "text": "Seat {player} has {tokens_to_eliminate} tokens and is eliminated."
          }
        },
        {
          "adjust": {
            "key": "alive_count",
            "value": -1,
            "if": {
              "calc": "just_out"
            }
          }
        },
        {
          "set": {
            "key": "opener_seat",
            "value": {
              "calc": "min([p.seat for p in players if p.alive and p.seat > opener_seat]) if any([p.alive and p.seat > opener_seat for p in players]) else min([p.seat for p in players if p.alive])"
            }
          }
        },
        {
          "set": {
            "key": "hand_active",
            "value": false
          }
        },
        {
          "set": {
            "key": "token_board",
            "value": {
              "calc": "[[p.seat, p.tokens] for p in players]"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "resolve",
      "label": "the reveal",
      "when": {
        "calc": "coyote_called"
      },
      "to": "all",
      "text": "Coyote called by seat {caller}! Cards [seat, card] (100 = Max→0): {revealed}. True total {true_total} against the declaration of {current_declaration} by seat {current_declarer}. Seat {last_loser} loses the hand and takes a token. Tokens [seat, tokens]: {token_board}. Seat {opener_seat} will open the next hand."
    },
    {
      "use": "check",
      "phase": "resolve",
      "label": "one player left",
      "when": {
        "calc": "alive_count == 1"
      },
      "against": [
        "over"
      ]
    },
    {
      "use": "update",
      "phase": "end of round",
      "label": "the round ends",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        },
        {
          "adjust": {
            "key": "rounds_done",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "end of round",
      "label": "the round limit",
      "when": {
        "calc": "rounds_done >= max_rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "alive_count == 1 or rounds_done >= max_rounds"
      },
      "rank_by": "you.alive * 10 - you.tokens",
      "text": "Winner: {result}. Final [seat, tokens, alive]: {[[p.seat, p.tokens, p.alive] for p in players]}."
    }
  },
  "limits": {
    "rounds": 40,
    "rounds_max": 41,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "Seats are numbered clockwise. Everyone starts with 0 tokens and alive. Seat {first_opener_seat} opens the first hand.\n\nThe deck has {deck_size} cards: {count_minus2} of -2, {count_minus1} of -1, {count_0} of 0, {count_1} of 1, {count_2} of 2, {count_3} of 3, {count_4} of 4, {count_5} of 5, and {count_max0} special card Max→0 (shown as {max0_code}).\n\nNew hand: at the start of a round with no hand in progress, the deck is restored to all {deck_size} cards and shuffled, and each alive player is dealt {cards_per_player} card face down. You are told the card of every other alive player, never your own. There is no declaration yet, and everyone is told who opens. If a hand is already in progress, it simply continues with the same cards and declarations.\n\nTurn order: in every round each alive player takes exactly one turn, starting with the opener and going clockwise through alive seats. The order is the same every round of a hand, so a hand goes round the table lap after lap. If Coyote is called, the hand ends and the remaining turns of that round are skipped. Before each turn everyone is shown the current declaration, who made it, and every declaration so far this hand.\n\nA turn: if nobody has declared yet this hand, you must declare a whole number from {first_declaration_min} to {declaration_max}; you may not call Coyote. Otherwise you either declare a whole number at least the current declaration + {raise_min_step} and at most {declaration_max}, or call Coyote. If the current declaration is {declaration_max}, you must call Coyote. A declaration makes you the current declarer and your number the current declaration.\n\nTrue total: all cards are revealed. Add all card values, counting Max→0 as 0. If Max→0 was dealt, the single highest other dealt card counts as 0 instead, provided its value is positive; if several cards tie for highest, only one of them is cancelled. If the highest other card is 0 or less, nothing is cancelled.\n\nResolving Coyote: if the true total is less than the current declaration, the current declarer loses the hand. Otherwise (the true total is equal to or more than the declaration) the caller loses the hand. The loser gains {token_per_loss} token. All cards, the true total and the loser are announced to everyone, and the hand is over.\n\nElimination: a player with {tokens_to_eliminate} tokens is eliminated, receives no more cards and is skipped in turn order.\n\nNext opener: after every hand the opener moves to the next alive player clockwise from the current opener, whoever lost. If the opener was just eliminated, it moves to the next alive player clockwise from their seat.\n\nEnd: the game ends immediately when only one player is alive, and that player wins. If round {max_rounds} ends first, any unfinished hand is discarded without a token, and the alive player with the fewest tokens wins; alive players tied for fewest share the result (a draw). Eliminated players rank below every alive player.\n\nThere is no table talk: declarations and calls are the only communication."
}
```
````
