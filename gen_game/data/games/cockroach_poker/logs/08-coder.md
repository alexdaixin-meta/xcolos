# 08 coder

- time: 2026-10-28T06:08:03+00:00 (93.9s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 1844be9ab7c40f3b, reply sha256 16afbde6d458a206

## Sent

````
# Task: write the XColos game file for "Roach Bluff"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 4; set `meta.players` to {"min": 3, "max": 4, "suggested": 4} (the suggested size is the one the game plays best at).

SETUP: The deck has 24 cards: 6 Roach, 6 Rat, 6 Fly and 6 Toad. Shuffle it once and deal it all face-down. With 4 players each gets 6 cards; with 3 players each gets 8. Each player's hand is private. Every player has a face-up pile, which starts empty; all face-up piles are public. Seat 1 is the first sender.

EACH ROUND:
1. The engine announces every player's face-up counts per creature and every player's hand size.
2. SEND: The sender privately picks one card from their hand. They declare a creature (Roach, Rat, Fly or Toad), which may be true or false. They also pick one other player as receiver. The card leaves the sender's hand and becomes the card in play. The claim and the receiver are announced to all; the card's identity is not.
3. RESPOND: The receiver chooses TRUE, FALSE or PASS.
   - TRUE or FALSE: Go to step 5.
   - PASS: Go to step 4.
4. PASS (only when the receiver chose PASS):
   - The receiver privately sees the card and becomes the passer.
   - The passer declares a creature, which may be true or false. They pick a new receiver who is neither the original sender nor the passer.
   - The new claim and new receiver are announced.
   - The final receiver must choose TRUE or FALSE; passing again is not allowed.
5. RESOLVE: The claim being judged is the latest one; the claimer is whoever made it (the sender, or the passer if there was a pass).
   - If the judge's call is correct (TRUE and the card matches the claim, or FALSE and it does not), the claimer takes the card face-up.
   - Otherwise the judge takes the card face-up.
   - The card's identity is revealed to everyone, and the player who took the card becomes the next sender.
6. CHECK:
   - If any player now has 3 face-up cards of one creature, that player loses and the game ends.
   - Otherwise, if the next sender has no cards in hand, that player loses and the game ends.

The game cannot last more than 24 rounds. There is no table talk: the claims are the only communication.

How the winner is decided: When the game ends, the player who triggered the end (three of one creature face-up, or no card to send) loses. Among all other players, the one with the fewest total face-up cards wins. If two or more of them tie for fewest, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Roach Bluff (3 to 4 players, best with 4)

A bluffing game in which players pass face-down creature cards with true or false claims; whoever ends up with three face-up cards of one creature, or has no card to send, loses.

STATE (every item below must exist in the file):
  - each player: hand (list, starts []); only its owner sees it. The cards held face-down in this player's private hand.
  - each player: hand_size (number, starts 0); everyone sees it. The number of cards in this player's hand.
  - each player: roach_up (number, starts 0); everyone sees it. The number of face-up Roach cards in this player's pile.
  - each player: rat_up (number, starts 0); everyone sees it. The number of face-up Rat cards in this player's pile.
  - each player: fly_up (number, starts 0); everyone sees it. The number of face-up Fly cards in this player's pile.
  - each player: toad_up (number, starts 0); everyone sees it. The number of face-up Toad cards in this player's pile.
  - each player: faceup_total (number, starts 0); everyone sees it. The total number of face-up cards in this player's pile. This is the score, and fewer is better.
  - each player: lost (bool, starts False); everyone sees it. True if this player triggered the end of the game and loses.
  - the table: deck (list, starts ['Roach x6', 'Rat x6', 'Fly x6', 'Toad x6']); hidden from all players. The 24-card deck before dealing: 6 each of Roach, Rat, Fly and Toad.
  - the table: card_in_play (text, starts ''); hidden from all players. The identity of the card currently being sent. It is hidden until resolution.
  - the table: sender (number, starts 1); everyone sees it. The seat of the current sender.
  - the table: receiver (number, starts 0); everyone sees it. The seat of the current receiver, who is the judge when the card resolves.
  - the table: passer (number, starts 0); everyone sees it. The seat that passed this round, or 0 if nobody passed.
  - the table: claimer (number, starts 0); everyone sees it. The seat that made the latest claim.
  - the table: claim (text, starts ''); everyone sees it. The latest declared creature.
  - the table: response (text, starts ''); everyone sees it. The latest receiver answer: TRUE, FALSE or PASS.
  - the table: passed (bool, starts False); everyone sees it. True if the first receiver passed this round.
  - the table: taker (number, starts 0); everyone sees it. The seat that took the card face-up this round.
  - the table: last_revealed (text, starts ''); everyone sees it. The identity of the card revealed at the last resolution.
  - the table: round_count (number, starts 0); everyone sees it. The number of rounds completed.
  - the table: game_over (bool, starts False); everyone sees it. True once a player has lost.
  - parameters, each kept as a table attribute: deck_size = 24, cards_per_creature = 6, creature_kinds = 4, hand_size_4_players = 6, hand_size_3_players = 8, lose_at_faceup_of_one_creature = 3, max_rounds = 24, first_sender_seat = 1, loser_rank_penalty = 1000

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Build the deck list with 24 cards: 6 Roach, 6 Rat, 6 Fly and 6 Toad.
  2. Deal the whole deck at random into the players' hand lists: 6 cards each with 4 players, or 8 cards each with 3 players. Draw each card at random from deck and remove it from deck.
  3. Set each player's hand_size to the number of cards dealt to them.
  4. Set all face-up counts, faceup_total and lost to 0 or false.
  5. Set sender to seat 1.
  6. Sync each player so they see their own hand.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] engine. What happens: Set passer=0, passed=false, response='', claim='', card_in_play=''.
  2. [tell] all players. What happens: Announce every player's roach_up, rat_up, fly_up, toad_up, faceup_total and hand_size.
  3. [ask] seat {sender} answers: one card from your own hand list. What happens: card_in_play = the chosen card; remove that card from the sender's hand; sender's hand_size -= 1. The answer is shown only to the sender.
  4. [ask] seat {sender} answers: one of Roach, Rat, Fly, Toad. What happens: claim = the answer; claimer = sender.
  5. [ask] seat {sender} answers: any seat other than the sender. What happens: receiver = the chosen seat.
  6. [tell] all players. What happens: Announce: 'Seat {sender} sends a card to seat {receiver}, claiming it is a {claim}.'
  7. [ask] seat {receiver} answers: TRUE, FALSE or PASS. What happens: response = the answer, announced to all. If the answer is PASS: passed = true, passer = receiver, claimer = receiver.
  8. [tell] seat {passer} (when passed). What happens: Privately show card_in_play to the passer.
  9. [ask] seat {passer} (when passed) answers: one of Roach, Rat, Fly, Toad. What happens: claim = the answer.
  10. [ask] seat {passer} (when passed) answers: any seat that is neither the sender nor the passer. What happens: receiver = the chosen seat.
  11. [tell] all players (when passed). What happens: Announce: 'Seat {passer} passes the card to seat {receiver}, claiming it is a {claim}.'
  12. [ask] seat {receiver} (when passed) answers: TRUE or FALSE. What happens: response = the answer, announced to all.
  13. [update] engine. What happens: correct = (response=='TRUE' and card_in_play==claim) or (response=='FALSE' and card_in_play!=claim). taker = claimer if correct, else receiver. Add 1 to the taker's count for the card_in_play creature (roach_up, rat_up, fly_up or toad_up). Add 1 to the taker's faceup_total. last_revealed = card_in_play. sender = taker. round_count += 1.
  14. [tell] all players. What happens: Announce: 'The card was a {last_revealed}. Seat {taker} takes it face-up and sends next.'
  15. [update] engine. What happens: If the taker has roach_up>=3 or rat_up>=3 or fly_up>=3 or toad_up>=3: taker.lost = true and game_over = true. Otherwise, if the sender's hand_size == 0: that player's lost = true and game_over = true.
  16. [check] engine. What happens: End the game if game_over == true or round_count >= 24. Otherwise continue.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts with 4 players, then each player holds 6 cards; with 3 players, each holds 8 cards; the 24-card deck has 6 each of Roach, Rat, Fly and Toad, and all of it is dealt.
  R2. When the game starts, then seat 1 is the first sender and every face-up count is 0.
  R3. When the sender sends a card, then that card leaves their hand and their hand_size drops by 1.
  R4. When the sender sends, then they declare one of Roach, Rat, Fly or Toad, which may be false, and choose a receiver who is not themselves.
  R5. When a claim is made, then the claim and the receiver are announced to all, but the card's identity is not.
  R6. When the receiver answers TRUE or FALSE, then the card resolves against the sender's claim.
  R7. When the receiver answers PASS, then they privately see the card, make a new claim, and choose a new receiver who is neither the original sender nor themselves.
  R8. When a card has been passed once, then the final receiver may answer only TRUE or FALSE.
  R9. When the judge says TRUE and the card matches the latest claim, or says FALSE and it does not, then the claimer takes the card face-up.
  R10. When the judge's call is wrong, then the judge takes the card face-up.
  R11. When a card resolves, then its identity is revealed to all, the taker's count for that creature and faceup_total each rise by 1, and the taker becomes the next sender.
  R12. When a player reaches 3 face-up cards of one creature, then that player loses and the game ends.
  R13. When the next sender has 0 cards in hand and nobody has 3 of one creature, then the next sender loses and the game ends.
  R14. When the game ends, then among the players who did not lose, the one with the fewest face-up cards wins, and players tied for fewest share the result.
  R15. When 24 rounds have been played, then the game ends.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Send: which card | asked: the sender | options: Any card in the sender's own hand list.
  - Send or pass: the claimed creature | asked: the sender, or the passer | options: Roach, Rat, Fly, Toad.
  - Send: the receiver | asked: the sender | options: Every seat except the sender.
  - Respond | asked: the first receiver | options: TRUE, FALSE, PASS.
  - Pass: the new receiver | asked: the passer | options: Every seat except the original sender and the passer. With 3 players there is exactly one such seat.
  - Final respond | asked: the receiver after a pass | options: TRUE, FALSE.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: game_over == true or round_count >= 24
  - each player's standing: 0 - you.faceup_total - 1000 * you.lost (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: The player who triggered the end (three face-up cards of one creature, or no card to send) loses. Among the others, the player with the fewest total face-up cards wins. Players tied for fewest share the win, which stands for the source's draw.
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

- each player: `hand_size` (number, visible: public, starts 0): The number of cards in this player's hand.
- each player: `roach_up` (number, visible: public, starts 0): The number of face-up Roach cards in this player's pile.
- each player: `rat_up` (number, visible: public, starts 0): The number of face-up Rat cards in this player's pile.
- each player: `fly_up` (number, visible: public, starts 0): The number of face-up Fly cards in this player's pile.
- each player: `toad_up` (number, visible: public, starts 0): The number of face-up Toad cards in this player's pile.
- each player: `faceup_total` (number, visible: public, starts 0): The total number of face-up cards in this player's pile. This is the score, and fewer is better.
- each player: `lost` (bool, visible: public, starts False): True if this player triggered the end of the game and loses.
- the table: `last_revealed` (text, visible: public, starts ''): The identity of the card revealed at the last resolution.
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 24, cards_per_creature = 6, creature_kinds = 4, hand_size_4_players = 6, hand_size_3_players = 8, lose_at_faceup_of_one_creature = 3, max_rounds = 24, first_sender_seat = 1, loser_rank_penalty = 1000
- the game ends with ONE ending whose `rank_by` is `0 - you.faceup_total - 1000 * you.lost`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
    "id": "roach_bluff",
    "name": "Roach Bluff",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 4
    },
    "blurb": "Pass face-down creature cards with true or false claims; three face-up of one creature, or no card to send, and you lose."
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
        "key": "hand_size",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "roach_up",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "rat_up",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "fly_up",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "toad_up",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "faceup_total",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "lost",
        "visible": "public",
        "type": "bool",
        "initial": false
      }
    ],
    "game": [
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": [
          "Roach",
          "Roach",
          "Roach",
          "Roach",
          "Roach",
          "Roach",
          "Rat",
          "Rat",
          "Rat",
          "Rat",
          "Rat",
          "Rat",
          "Fly",
          "Fly",
          "Fly",
          "Fly",
          "Fly",
          "Fly",
          "Toad",
          "Toad",
          "Toad",
          "Toad",
          "Toad",
          "Toad"
        ]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "correct",
        "visible": "none",
        "type": "bool",
        "initial": false
      },
      {
        "key": "card_in_play",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "sender",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "receiver",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "passer",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "claimer",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "claim",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "response",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "passed",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "taker",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "last_revealed",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "round_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "game_over",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 24
      },
      {
        "key": "cards_per_creature",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "creature_kinds",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "hand_size_4_players",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "hand_size_3_players",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "lose_at_faceup_of_one_creature",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "max_rounds",
        "visible": "public",
        "type": "number",
        "initial": 24
      },
      {
        "key": "first_sender_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "loser_rank_penalty",
        "visible": "public",
        "type": "number",
        "initial": 1000
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "build the deck",
      "do": [
        {
          "set": {
            "key": "deck",
            "value": [
              "Roach",
              "Roach",
              "Roach",
              "Roach",
              "Roach",
              "Roach",
              "Rat",
              "Rat",
              "Rat",
              "Rat",
              "Rat",
              "Rat",
              "Fly",
              "Fly",
              "Fly",
              "Fly",
              "Fly",
              "Fly",
              "Toad",
              "Toad",
              "Toad",
              "Toad",
              "Toad",
              "Toad"
            ]
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "deal the deck",
      "do": [
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
            "player": {
              "calc": "0 - len(players) * int(0 / len(players)) + 1"
            },
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
            "player": {
              "calc": "1 - len(players) * int(1 / len(players)) + 1"
            },
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
            "player": {
              "calc": "2 - len(players) * int(2 / len(players)) + 1"
            },
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
            "player": {
              "calc": "3 - len(players) * int(3 / len(players)) + 1"
            },
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
            "player": {
              "calc": "4 - len(players) * int(4 / len(players)) + 1"
            },
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
            "player": {
              "calc": "5 - len(players) * int(5 / len(players)) + 1"
            },
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
            "player": {
              "calc": "6 - len(players) * int(6 / len(players)) + 1"
            },
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
            "player": {
              "calc": "7 - len(players) * int(7 / len(players)) + 1"
            },
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
            "player": {
              "calc": "8 - len(players) * int(8 / len(players)) + 1"
            },
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
            "player": {
              "calc": "9 - len(players) * int(9 / len(players)) + 1"
            },
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
            "player": {
              "calc": "10 - len(players) * int(10 / len(players)) + 1"
            },
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
            "player": {
              "calc": "11 - len(players) * int(11 / len(players)) + 1"
            },
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
            "player": {
              "calc": "12 - len(players) * int(12 / len(players)) + 1"
            },
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
            "player": {
              "calc": "13 - len(players) * int(13 / len(players)) + 1"
            },
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
            "player": {
              "calc": "14 - len(players) * int(14 / len(players)) + 1"
            },
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
            "player": {
              "calc": "15 - len(players) * int(15 / len(players)) + 1"
            },
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
            "player": {
              "calc": "16 - len(players) * int(16 / len(players)) + 1"
            },
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
            "player": {
              "calc": "17 - len(players) * int(17 / len(players)) + 1"
            },
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
            "player": {
              "calc": "18 - len(players) * int(18 / len(players)) + 1"
            },
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
            "player": {
              "calc": "19 - len(players) * int(19 / len(players)) + 1"
            },
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
            "player": {
              "calc": "20 - len(players) * int(20 / len(players)) + 1"
            },
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
            "player": {
              "calc": "21 - len(players) * int(21 / len(players)) + 1"
            },
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
            "player": {
              "calc": "22 - len(players) * int(22 / len(players)) + 1"
            },
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
            "player": {
              "calc": "23 - len(players) * int(23 / len(players)) + 1"
            },
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
        }
      ]
    },
    {
      "use": "update",
      "label": "starting counts",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "hand_size",
            "value": {
              "calc": "len(you.hand)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "roach_up",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "rat_up",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "fly_up",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "toad_up",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "faceup_total",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "lost",
            "value": false
          }
        },
        {
          "set": {
            "key": "sender",
            "value": {
              "calc": "first_sender_seat"
            }
          }
        }
      ]
    },
    {
      "use": "sync",
      "label": "your hand",
      "mode": "self",
      "to": "all",
      "fields": [
        "hand",
        "hand_size"
      ],
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "send",
      "label": "clear the round",
      "do": [
        {
          "set": {
            "key": "passer",
            "value": 0
          }
        },
        {
          "set": {
            "key": "passed",
            "value": false
          }
        },
        {
          "set": {
            "key": "response",
            "value": ""
          }
        },
        {
          "set": {
            "key": "claim",
            "value": ""
          }
        },
        {
          "set": {
            "key": "card_in_play",
            "value": ""
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "send",
      "label": "the table",
      "to": "all",
      "text": "Rounds played: {round_count}. Piles and hands [seat, Roach, Rat, Fly, Toad, face-up total, hand size]: {[[p.seat, p.roach_up, p.rat_up, p.fly_up, p.toad_up, p.faceup_total, p.hand_size] for p in players]}. Seat {sender} sends."
    },
    {
      "use": "ask",
      "phase": "send",
      "label": "choose the card",
      "to": {
        "where": "you.seat == sender"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "verify": {
        "bind": "sent_card"
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "card_in_play",
              "value": "$answer"
            }
          },
          {
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": "$answer"
            }
          },
          {
            "adjust": {
              "player": "$seat",
              "key": "hand_size",
              "value": -1
            }
          }
        ]
      },
      "text": "You are the sender. Choose one card from your hand to send face-down. Nobody else will see which card it is."
    },
    {
      "use": "ask",
      "phase": "send",
      "label": "declare the creature",
      "to": {
        "where": "you.seat == sender"
      },
      "answer": {
        "type": "choice",
        "options": [
          "Roach",
          "Rat",
          "Fly",
          "Toad"
        ]
      },
      "verify": {
        "bind": "send_claim"
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "claim",
              "value": "$answer"
            }
          },
          {
            "set": {
              "key": "claimer",
              "value": "$seat"
            }
          }
        ]
      },
      "text": "Declare what creature the card is: Roach, Rat, Fly or Toad. You may tell the truth or lie."
    },
    {
      "use": "ask",
      "phase": "send",
      "label": "choose the receiver",
      "to": {
        "where": "you.seat == sender"
      },
      "answer": {
        "type": "player",
        "exclude_self": true
      },
      "verify": {
        "bind": "send_to"
      },
      "each": {
        "do": [
    
... (cut)

Why it was refused: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (claim, last_revealed) in `your_hand`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "roach_bluff",
    "name": "Roach Bluff",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 4
    },
    "blurb": "Pass face-down creature cards with true or false claims; three face-up of one creature, or no card to send, and you lose."
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
        "key": "hand_size",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "roach_up",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "rat_up",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "fly_up",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "toad_up",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "faceup_total",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "lost",
        "visible": "public",
        "type": "bool",
        "initial": false
      }
    ],
    "game": [
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": [
          "Roach",
          "Roach",
          "Roach",
          "Roach",
          "Roach",
          "Roach",
          "Rat",
          "Rat",
          "Rat",
          "Rat",
          "Rat",
          "Rat",
          "Fly",
          "Fly",
          "Fly",
          "Fly",
          "Fly",
          "Fly",
          "Toad",
          "Toad",
          "Toad",
          "Toad",
          "Toad",
          "Toad"
        ]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "correct",
        "visible": "none",
        "type": "bool",
        "initial": false
      },
      {
        "key": "card_in_play",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "sender",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "receiver",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "passer",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "claimer",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "claim",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "response",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "passed",
        "visible": "none",
        "type": "bool",
        "initial": false
      },
      {
        "key": "taker",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "last_revealed",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "round_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "game_over",
        "visible": "none",
        "type": "bool",
        "initial": false
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 24
      },
      {
        "key": "cards_per_creature",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "creature_kinds",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "hand_size_4_players",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "hand_size_3_players",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "lose_at_faceup_of_one_creature",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "max_rounds",
        "visible": "public",
        "type": "number",
        "initial": 24
      },
      {
        "key": "first_sender_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "loser_rank_penalty",
        "visible": "public",
        "type": "number",
        "initial": 1000
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "build the deck",
      "do": [
        {
          "set": {
            "key": "deck",
            "value": [
              "Roach",
              "Roach",
              "Roach",
              "Roach",
              "Roach",
              "Roach",
              "Rat",
              "Rat",
              "Rat",
              "Rat",
              "Rat",
              "Rat",
              "Fly",
              "Fly",
              "Fly",
              "Fly",
              "Fly",
              "Fly",
              "Toad",
              "Toad",
              "Toad",
              "Toad",
              "Toad",
              "Toad"
            ]
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "deal the deck",
      "do": [
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "0 - len(players) * int(0 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "1 - len(players) * int(1 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "2 - len(players) * int(2 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "3 - len(players) * int(3 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "4 - len(players) * int(4 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "5 - len(players) * int(5 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "6 - len(players) * int(6 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "7 - len(players) * int(7 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "8 - len(players) * int(8 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "9 - len(players) * int(9 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "10 - len(players) * int(10 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "11 - len(players) * int(11 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "12 - len(players) * int(12 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "13 - len(players) * int(13 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "14 - len(players) * int(14 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "15 - len(players) * int(15 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "16 - len(players) * int(16 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "17 - len(players) * int(17 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "18 - len(players) * int(18 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "19 - len(players) * int(19 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "20 - len(players) * int(20 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "21 - len(players) * int(21 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "22 - len(players) * int(22 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "23 - len(players) * int(23 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}}
      ]
    },
    {
      "use": "update",
      "label": "starting counts",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "hand_size",
            "value": {
              "calc": "len(you.hand)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "roach_up",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "rat_up",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "fly_up",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "toad_up",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "faceup_total",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "lost",
            "value": false
          }
        },
        {
          "set": {
            "key": "sender",
            "value": {
              "calc": "first_sender_seat"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "label": "your hand",
      "to": "all",
      "text": "Your hand ({hand_size} cards): {hand}. Seat {sender} sends first."
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "send",
      "label": "clear the round",
      "do": [
        {
          "set": {
            "key": "passer",
            "value": 0
          }
        },
        {
          "set": {
            "key": "passed",
            "value": false
          }
        },
        {
          "set": {
            "key": "response",
            "value": ""
          }
        },
        {
          "set": {
            "key": "claim",
            "value": ""
          }
        },
        {
          "set": {
            "key": "card_in_play",
            "value": ""
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "send",
      "label": "the table",
      "to": "all",
      "text": "Rounds played: {round_count}. Piles and hands [seat, Roach, Rat, Fly, Toad, face-up total, hand size]: {[[p.seat, p.roach_up, p.rat_up, p.fly_up, p.toad_up, p.faceup_total, p.hand_size] for p in players]}. Seat {sender} sends."
    },
    {
      "use": "ask",
      "phase": "send",
      "label": "choose the card",
      "to": {
        "where": "you.seat == sender"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "verify": {
        "bind": "sent_card"
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "card_in_play",
              "value": "$answer"
            }
          },
          {
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": "$answer"
            }
          },
          {
            "adjust": {
              "player": "$seat",
              "key": "hand_size",
              "value": -1
            }
          }
        ]
      },
      "text": "You are the sender. Choose one card from your hand to send face-down. Nobody else will see which card it is."
    },
    {
      "use": "ask",
      "phase": "send",
      "label": "declare the creature",
      "to": {
        "where": "you.seat == sender"
      },
      "answer": {
        "type": "choice",
        "options": [
          "Roach",
          "Rat",
          "Fly",
          "Toad"
        ]
      },
      "verify": {
        "bind": "send_claim"
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "claim",
              "value": "$answer"
            }
          },
          {
            "set": {
              "key": "claimer",
              "value": "$seat"
            }
          }
        ]
      },
      "text": "Declare what creature the card is: Roach, Rat, Fly or Toad. You may tell the truth or lie."
    },
    {
      "use": "ask",
      "phase": "send",
      "label": "choose the receiver",
      "to": {
        "where": "you.seat == sender"
      },
      "answer": {
        "type": "player",
        "exclude_self": true
      },
      "verify": {
        "bind": "send_to"
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "receiver",
              "value": "$answer"
            }
          }
        ]
      },
      "text": "Choose the player who receives the card. You may not choose yourself."
    },
    {
      "use": "tell",
      "phase": "send",
      "label": "the claim",
      "to": "all",
      "text": "Seat {sender} sends a card to seat {receiver}, claiming it is a {claim}."
    },
    {
      "use": "ask",
      "phase": "respond",
      "label": "respond",
      "to": {
        "where": "you.seat == receiver"
      },
      "answer": {
        "type": "choice",
        "options": [
          "TRUE",
          "FALSE",
          "PASS"
        ]
      },
      "verify": {
        "bind": "first_response"
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "response",
              "value": "$answer"
            }
          },
          {
            "set": {
              "key": "passed",
              "value": true,
              "if": {
                "calc": "$answer == 'PASS'"
              }
            }
          },
          {
            "set": {
              "key": "passer",
              "value": "$seat",
              "if": {
                "calc": "$answer == 'PASS'"
              }
            }
          },
          {
            "set": {
              "key": "claimer",
              "value": "$seat",
              "if": {
                "calc": "$answer == 'PASS'"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} answers {value}."
      },
      "text": "Seat {sender} sent you a card claiming it is a {claim}. Answer TRUE if you think the claim is true, FALSE if you think it is false, or PASS to look at the card and pass it on to another player with a claim of your own."
    },
    {
      "use": "tell",
      "phase": "pass",
      "label": "the passer looks",
      "when": {
        "calc": "passed"
      },
      "to": {
        "where": "you.seat == passer"
      },
      "text": "You look at the card: it is a {card_in_play}."
    },
    {
      "use": "ask",
      "phase": "pass",
      "label": "the passer declares",
      "when": {
        "calc": "passed"
      },
      "to": {
        "where": "you.seat == passer"
      },
      "answer": {
        "type": "choice",
        "options": [
          "Roach",
          "Rat",
          "Fly",
          "Toad"
        ]
      },
      "verify": {
        "bind": "pass_claim"
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "claim",
              "value": "$answer"
            }
          }
        ]
      },
      "text": "You are passing the card on. Declare what creature it is: Roach, Rat, Fly or Toad. You may tell the truth or lie."
    },
    {
      "use": "ask",
      "phase": "pass",
      "label": "the passer chooses a receiver",
      "when": {
        "calc": "passed"
      },
      "to": {
        "where": "you.seat == passer"
      },
      "answer": {
        "type": "player",
        "exclude_self": true,
        "exclude": {
          "where": "you.seat == sender"
        }
      },
      "verify": {
        "bind": "pass_to"
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "receiver",
              "value": "$answer"
            }
          }
        ]
      },
      "text": "Choose the new receiver. You may not choose yourself or seat {sender}, who sent the card."
    },
    {
      "use": "tell",
      "phase": "pass",
      "label": "the new claim",
      "when": {
        "calc": "passed"
      },
      "to": "all",
      "text": "Seat {passer} passes the card to seat {receiver}, claiming it is a {claim}."
    },
    {
      "use": "ask",
      "phase": "pass",
      "label": "final respond",
      "when": {
        "calc": "passed"
      },
      "to": {
        "where": "you.seat == receiver"
      },
      "answer": {
        "type": "choice",
        "options": [
          "TRUE",
          "FALSE"
        ]
      },
      "verify": {
        "bind": "final_response"
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "response",
              "value": "$answer"
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} answers {value}."
      },
      "text": "Seat {passer} passed you the card claiming it is a {claim}. The card has already been passed once, so you must answer TRUE or FALSE."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "resolve the card",
      "do": [
        {
          "set": {
            "key": "correct",
            "value": {
              "calc": "(response == 'TRUE' and card_in_play == claim) or (response == 'FALSE' and card_in_play != claim)"
            }
          }
        },
        {
          "set": {
            "key": "taker",
            "value": {
              "calc": "claimer if correct else receiver"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "taker"
            },
            "key": "roach_up",
            "value": 1,
            "if": {
              "calc": "card_in_play == 'Roach'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "taker"
            },
            "key": "rat_up",
            "value": 1,
            "if": {
              "calc": "card_in_play == 'Rat'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "taker"
            },
            "key": "fly_up",
            "value": 1,
            "if": {
              "calc": "card_in_play == 'Fly'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "taker"
            },
            "key": "toad_up",
            "value": 1,
            "if": {
              "calc": "card_in_play == 'Toad'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "taker"
            },
            "key": "faceup_total",
            "value": 1
          }
        },
        {
          "set": {
            "key": "last_revealed",
            "value": {
              "calc": "card_in_play"
            }
          }
        },
        {
          "set": {
            "key": "sender",
            "value": {
              "calc": "taker"
            }
          }
        },
        {
          "adjust": {
            "key": "round_count",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "resolve",
      "label": "the reveal",
      "to": "all",
      "text": "The card was a {last_revealed}. Seat {taker} takes it face-up and sends next."
    },
    {
      "use": "update",
      "phase": "check",
      "label": "who loses",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.seat == taker and (you.roach_up >= lose_at_faceup_of_one_creature or you.rat_up >= lose_at_faceup_of_one_creature or you.fly_up >= lose_at_faceup_of_one_creature or you.toad_up >= lose_at_faceup_of_one_creature)"
            },
            "key": "lost",
            "value": true,
            "text": "Seat {player} has {lose_at_faceup_of_one_creature} face-up cards of one creature and loses."
          }
        },
        {
          "set": {
            "key": "game_over",
            "value": true,
            "if": {
              "calc": "any(p.lost for p in players)"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == sender and you.hand_size == 0"
            },
            "key": "lost",
            "value": true,
            "if": {
              "calc": "not game_over"
            },
            "text": "Seat {player} must send next but has no cards in hand, and loses."
          }
        },
        {
          "set": {
            "key": "game_over",
            "value": true,
            "if": {
              "calc": "any(p.lost for p in players)"
            }
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "check",
      "label": "is it over",
      "when": {
        "calc": "game_over or round_count >= max_rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "game_over or round_count >= max_rounds"
      },
      "rank_by": "0 - you.faceup_total - 1000 * you.lost",
      "text": "Winner: {result}. Final standings [seat, face-up total, lost]: {[[p.seat, p.faceup_total, p.lost] for p in players]}."
    }
  },
  "limits": {
    "rounds": 24,
    "rounds_max": 24,
    "actions_max": 1000,
    "deadline_s": 120
  },
  "rules": "The deck has {deck_size} cards: {cards_per_creature} each of {creature_kinds} creatures, Roach, Rat, Fly and Toad. It is shuffled once and dealt out entirely face-down: with 4 players each gets {hand_size_4_players} cards; with 3 players each gets {hand_size_3_players}. Your hand is private. Every player has a face-up pile, which starts empty; all face-up piles are public. Seat {first_sender_seat} is the first sender.\n\nEach round:\n1. Every player's face-up counts per creature and every player's hand size are announced.\n2. SEND: The sender privately picks one card from their hand. They declare a creature (Roach, Rat, Fly or Toad), which may be true or false. They also pick one other player as receiver. The card leaves the sender's hand and becomes the card in play. The claim and the receiver are announced to all; the card's identity is not.\n3. RESPOND: The receiver chooses TRUE, FALSE or PASS. TRUE or FALSE: the card resolves at once against the sender's claim (step 5). PASS: go to step 4.\n4. PASS (only when the receiver chose PASS): the receiver privately sees the card and becomes the passer. The passer declares a creature, which may be true or false, and picks a new receiver who is neither the original sender nor the passer. The new claim and new receiver are announced. The final receiver must choose TRUE or FALSE; passing again is not allowed.\n5. RESOLVE: The claim being judged is the latest one; the claimer is whoever made it (the sender, or the passer if there was a pass). If the judge's call is correct (TRUE and the card matches the claim, or FALSE and it does not), the claimer takes the card face-up. Otherwise (TRUE and the card does not match, or FALSE and it does match) the judge takes the card face-up. The card's identity is revealed to everyone, and the player who took the card becomes the next sender.\n6. CHECK: If any player now has {lose_at_faceup_of_one_creature} face-up cards of one creature, that player loses and the game ends. Otherwise, if the next sender has no cards in hand, that player loses and the game ends. Otherwise play continues.\n\nThe game cannot last more than {max_rounds} rounds. There is no table talk: the claims are the only communication.\n\nWhen the game ends, the player who triggered the end (three of one creature face-up, or no card to send) loses. Among all other players, the one with the fewest total face-up cards wins. If two or more of them tie for fewest, they share the result (a draw)."
}
```
````
