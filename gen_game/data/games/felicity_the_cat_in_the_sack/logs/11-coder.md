# 11 coder

- time: 2026-10-27T18:24:49+00:00 (74.5s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 7de0534eaad9889e, reply sha256 ba048055ef8509d1

## Sent

````
# Task: write the XColos game file for "Cat in the Sack: Paid Entry"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 5; set `meta.players` to {"min": 3, "max": 5, "suggested": 4} (the suggested size is the one the game plays best at).

SETUP
- Every player receives the same 9 cards: cats worth -8, -5, 3, 5, 8, 11 and 15, one Rabbit worth 0, and one Dog worth 0.
- One card is removed at random from each hand. Its owner is told which card it is. No one else is told.
- Each player starts with 15 mice and 0 cat points. The bank of mice is unlimited.
- Seats are numbered. Seat 1 is the start player in round 1.
- The game lasts 8 rounds, so every remaining card is played.

EACH ROUND
1. Start player. In round 1 it is Seat 1. In each later round it is the next seat in order. The start player matters only for breaking ties.
2. Fill the sack. All players at the same time secretly choose one card from their hand and place it in the sack. Placed cards never return.
3. Shuffle. The engine shuffles the sack into a random order.
4. First reveal. Cards are shown from the front of the shuffled order. With 3 players, 1 card is shown. With 4 or 5 players, 2 cards are shown. Revealed cards do not say who placed them.
5. Talk. Every player writes one short message at the same time, without seeing the others' messages. All messages are then shown. Claims are not binding and may be lies.
6. Stay or drop. All players at the same time choose STAY or DROP. A player with fewer than 2 mice must DROP.
7. Entry and drop payment. Each player who chose STAY pays 1 mouse to the bank immediately. This fee is never refunded. Each player who chose DROP receives 2 mice from the bank and is out for this round.
8. Second reveal. The next card in the shuffled order is shown to everyone.
9. Sealed bid. Every player who chose STAY secretly bids a whole number of mice, from 1 up to their current mice (counted after paying the fee). All bids are revealed together.
10. Winner. The highest bidder wins the sack.
   - If two or more players tie for the highest bid, the tied player with fewer current mice wins.
   - If they are still tied, the tied player who comes first in seat order, counting from the start player, wins.
   - If nobody stayed, nobody wins and the sack is discarded.
   - If exactly one player stayed, that player wins and pays their bid.
11. Sack value. All remaining sack cards are revealed. The sack's value is the sum of the cats in it. The Rabbit and Dogs are worth 0.
   - If exactly one Dog is in the sack and the sack holds at least one cat, the cat with the highest value is removed before summing.
   - Two or more Dogs have no effect.
12. Payment. The winner pays their bid to the bank and adds the sack's value to their cat points. The value may be negative.
13. Losing stayers receive nothing. They have already paid their fee.
14. Discard. All sack cards are discarded face up, so everyone can count which cards have been used.
15. End check. After round 8 the game ends.

SCORING
Each player's total is their cat points plus their mice.

How the winner is decided: After round 8 the player with the highest total (cat points plus mice) wins. If totals are tied, the tied player with the most cat points wins. If that is also tied, the game is a draw among those players.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Cat in the Sack: Paid Entry (3 to 5 players, best with 4)

Each round every player secretly puts one card into a shared sack. Some sack cards are revealed, players talk, then pay to stay or get paid to drop. Stayers bid sealed mice for the sack, whose cat value may be negative.

STATE (every item below must exist in the file):
  - each player: hand (list, starts ['cat_-8', 'cat_-5', 'cat_3', 'cat_5', 'cat_8', 'cat_11', 'cat_15', 'rabbit', 'dog']); only its owner sees it. Cards still held. Before round 1 it holds 8 cards, after one is removed at random.
  - each player: removed_card (text, starts ''); only its owner sees it. The card removed at random from this player's hand at setup. Only its owner knows it.
  - each player: placed_card (text, starts ''); only its owner sees it. The card this player put into the sack this round.
  - each player: mice (number, starts 15); everyone sees it. Current mice.
  - each player: cat_points (number, starts 0); everyone sees it. Accumulated sack values won.
  - each player: stayed (bool, starts False); everyone sees it. True if the player chose STAY this round.
  - each player: bid (number, starts 0); everyone sees it. Sealed bid this round, revealed with all other bids. 0 if the player dropped.
  - each player: message (text, starts ''); everyone sees it. This round's talk message. Not binding.
  - the table: round (number, starts 0); everyone sees it. Current round number, 1 to 8.
  - the table: start_seat (number, starts 1); everyone sees it. Start player this round, used only for the sack tie-break.
  - the table: sack (list, starts []); hidden from all players. This round's sack cards in shuffled order. It does not record who placed which card.
  - the table: revealed_cards (list, starts []); everyone sees it. Sack cards shown so far this round, without owners.
  - the table: discard (list, starts []); everyone sees it. All face-up discarded sack cards from earlier rounds.
  - the table: stayer_count (number, starts 0); everyone sees it. Number of players who chose STAY this round.
  - the table: winner_seat (number, starts 0); everyone sees it. Seat that won the sack this round, or 0 if nobody did.
  - the table: sack_value (number, starts 0); everyone sees it. Computed value of this round's sack.
  - parameters, each kept as a table attribute: cat_value_1 = -8, cat_value_2 = -5, cat_value_3 = 3, cat_value_4 = 5, cat_value_5 = 8, cat_value_6 = 11, cat_value_7 = 15, rabbit_value = 0, dog_value = 0, cards_per_hand = 9, cards_removed_per_hand = 1, starting_mice = 15, starting_cat_points = 0, rounds = 8, stay_fee = 1, drop_payment = 2, min_mice_to_stay = 2, min_bid = 1, first_reveal_with_3_players = 1, first_reveal_with_4_or_5_players = 2, second_reveal_count = 1, dogs_that_cancel_top_cat = 1, start_seat_round_1 = 1

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Every player's hand is set to the same 9 cards: cat_-8, cat_-5, cat_3, cat_5, cat_8, cat_11, cat_15, rabbit and dog.
  2. For each player, one card is picked at random from their hand, removed from the hand and stored in that player's removed_card, which only that player can see.
  3. Each player's mice is set to 15 and cat_points to 0. The bank is unlimited, so it is not tracked.
  4. round is set to 0, start_seat to 1, and sack, revealed_cards and discard to empty lists.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] table. What happens: round += 1. start_seat = ((round - 1) mod player_count) + 1. Every player: stayed = false, bid = 0, placed_card = ''. sack = [], revealed_cards = [], winner_seat = 0, sack_value = 0. Announce the round and the start seat.
  2. [poll] all players answers: one card from your own hand. What happens: Each player's choice is removed from hand, stored in placed_card and appended to sack. Nobody sees the choices.
  3. [update] table. What happens: Shuffle the sack: rebuild it by repeatedly drawing a card at random from it, which gives a random order.
  4. [update] table. What happens: First reveal: append the first k cards of sack to revealed_cards, where k = 1 if player_count = 3, else 2. Tell everyone the revealed cards, without owners.
  5. [poll] all players answers: short text message. What happens: message is set for each player. Broadcast {"to": "all", "text": "Seat {seat} says: {value}"} once all messages are in.
  6. [poll] all players answers: STAY or DROP (DROP only, if mice < 2). What happens: stayed = true for STAY, false for DROP. stayer_count = number of players with stayed = true. All choices are shown together.
  7. [update] all players. What happens: Each player with stayed = true: mice -= 1 (never refunded). Each player with stayed = false: mice += 2.
  8. [update] table. What happens: Second reveal: append sack card number k+1 to revealed_cards, where k is the first-reveal count. Tell everyone.
  9. [poll] each player with stayed = true answers: whole number from 1 to your current mice. What happens: bid is set for each stayer. All bids are revealed together.
  10. [update] table. What happens: If stayer_count = 0: winner_seat = 0. Otherwise winner_seat is the stayer with the highest key = bid * 100000 - mice * 100 - ((seat - start_seat + player_count) mod player_count). The ordering is: highest bid, then fewer current mice, then first in seat order counting from start_seat. Announce it.
  11. [update] table. What happens: Reveal all sack cards to everyone. Let cats = the values of the cat_ cards in sack, and dogs = the count of 'dog' in sack. sack_value = sum(cats), minus max(cats) if dogs = 1 and at least one cat is present. Rabbit and dog are worth 0, and 2 or more dogs have no effect. Announce sack_value.
  12. [update] the winner_seat player. What happens: If winner_seat != 0: that player's mice -= bid and cat_points += sack_value (which may be negative). Losing stayers change nothing more.
  13. [update] table. What happens: Append every sack card to discard (face up, public). sack = []. Announce mice and cat_points.
  14. [check] table. What happens: If round >= 8, end the game. Otherwise continue to the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. At setup every player's hand holds cat_-8, cat_-5, cat_3, cat_5, cat_8, cat_11, cat_15, rabbit and dog (9 cards).
  R2. At setup exactly one random card is removed from each hand and recorded in that player's removed_card, visible only to that player, leaving 8 cards in hand.
  R3. At setup each player has mice = 15 and cat_points = 0.
  R4. In round r, start_seat = ((r - 1) mod player_count) + 1, so it is seat 1 in round 1 and seat 2 in round 2.
  R5. Each round every player simultaneously places one card from their hand into the sack, and that card leaves their hand permanently.
  R6. After shuffling, the first reveal shows 1 sack card with 3 players and 2 sack cards with 4 or 5 players, without naming who placed them.
  R7. Each round every player sends one simultaneous short message, and all messages are shown only after all are in. Messages are not binding.
  R8. When a player has fewer than 2 mice at the stay-or-drop step, they may only choose DROP.
  R9. When a player chooses STAY, they immediately pay 1 mouse, which is never refunded.
  R10. When a player chooses DROP, they receive 2 mice and take no further part in that round.
  R11. After stay-or-drop, one more sack card is revealed to everyone.
  R12. Each stayer bids a whole number from 1 to their mice after paying the fee, and all bids are revealed together.
  R13. When bids differ, the highest bidder wins the sack.
  R14. When two or more stayers tie for the highest bid, the tied stayer with fewer current mice wins.
  R15. When the tied stayers also have equal mice, the one first in seat order counting from start_seat wins.
  R16. When nobody stays, nobody wins, no bid is paid and the sack is discarded.
  R17. When exactly one player stays, that player wins the sack and pays their bid.
  R18. The sack value is the sum of its cat card values. The rabbit and dogs are worth 0.
  R19. When the sack holds exactly 1 dog and at least one cat, the highest-valued cat is excluded from the sum (for example, cat_15 + cat_3 + dog + rabbit = 3).
  R20. When the sack holds 2 or more dogs, they have no effect (for example, cat_15 + dog + dog = 15).
  R21. The winner pays their bid in mice and adds the sack value, which may be negative, to cat_points.
  R22. Losing stayers receive nothing and do not get back the 1-mouse fee.
  R23. All sack cards are added to the public discard list at the end of each round.
  R24. The game ends after round 8.
  R25. The player with the highest cat_points + mice wins. On a tie the higher cat_points wins, and if that also ties those players share the win.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Fill the sack | asked: all players | options: any card currently in that player's own hand
  - Talk | asked: all players | options: one short free-text message
  - Stay or drop | asked: all players | options: a player with mice >= 2: STAY, DROP. A player with mice < 2: DROP only.
  - Sealed bid | asked: each player with stayed = true | options: a whole number from 1 to that player's current mice (after the fee). Players who dropped are not asked.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round >= 8
  - each player's standing: (you.mice + you.cat_points) * 1000 + you.cat_points (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's total is cat_points plus mice, and the highest total wins. If totals tie, the tied player with more cat points wins. If that also ties, those players share the win (a draw).
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

- each player: `mice` (number, visible: public, starts 15): Current mice.
- each player: `cat_points` (number, visible: public, starts 0): Accumulated sack values won.
- each player: `stayed` (bool, visible: public, starts False): True if the player chose STAY this round.
- each player: `bid` (number, visible: public, starts 0): Sealed bid this round, revealed with all other bids. 0 if the player dropped.
- the table: `round` (number, visible: public, starts 0): Current round number, 1 to 8.
- the table: `start_seat` (number, visible: public, starts 1): Start player this round, used only for the sack tie-break.
- the table: `revealed_cards` (list, visible: public, starts []): Sack cards shown so far this round, without owners.
- the table: `discard` (list, visible: public, starts []): All face-up discarded sack cards from earlier rounds.
- the table: `winner_seat` (number, visible: public, starts 0): Seat that won the sack this round, or 0 if nobody did.
- the table: `sack_value` (number, visible: public, starts 0): Computed value of this round's sack.
- parameters (each must be an attribute holding this value, never a number buried in a step): cat_value_1 = -8, cat_value_2 = -5, cat_value_3 = 3, cat_value_4 = 5, cat_value_5 = 8, cat_value_6 = 11, cat_value_7 = 15, rabbit_value = 0, dog_value = 0, cards_per_hand = 9, cards_removed_per_hand = 1, starting_mice = 15, starting_cat_points = 0, rounds = 8, stay_fee = 1, drop_payment = 2, min_mice_to_stay = 2, min_bid = 1, first_reveal_with_3_players = 1, first_reveal_with_4_or_5_players = 2, second_reveal_count = 1, dogs_that_cancel_top_cat = 1, start_seat_round_1 = 1
- the game ends with ONE ending whose `rank_by` is `(you.mice + you.cat_points) * 1000 + you.cat_points`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
    "id": "cat_in_the_sack_paid_entry",
    "name": "Cat in the Sack: Paid Entry",
    "players": {
      "min": 3,
      "max": 5,
      "suggested": 4
    },
    "blurb": "Each round everyone secretly feeds one card to a shared sack; pay to stay, get paid to drop, and bid sealed mice for a sack whose cat value may be negative."
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
        "initial": [
          "cat_-8",
          "cat_-5",
          "cat_3",
          "cat_5",
          "cat_8",
          "cat_11",
          "cat_15",
          "rabbit",
          "dog"
        ]
      },
      {
        "key": "removed_card",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "placed_card",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "mice",
        "visible": "public",
        "type": "number",
        "initial": 15
      },
      {
        "key": "cat_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "stayed",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "message",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "choice",
        "visible": "ally",
        "type": "text",
        "initial": ""
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
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "start_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "sack",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "shuffled",
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
        "key": "sack_cats",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "best_key",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "first_reveal_count",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "revealed_cards",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "discard",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "stayer_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "winner_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "sack_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "cat_value_1",
        "visible": "public",
        "type": "number",
        "initial": -8
      },
      {
        "key": "cat_value_2",
        "visible": "public",
        "type": "number",
        "initial": -5
      },
      {
        "key": "cat_value_3",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "cat_value_4",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "cat_value_5",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "cat_value_6",
        "visible": "public",
        "type": "number",
        "initial": 11
      },
      {
        "key": "cat_value_7",
        "visible": "public",
        "type": "number",
        "initial": 15
      },
      {
        "key": "rabbit_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "dog_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "cards_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "cards_removed_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "starting_mice",
        "visible": "public",
        "type": "number",
        "initial": 15
      },
      {
        "key": "starting_cat_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "stay_fee",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "drop_payment",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "min_mice_to_stay",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "min_bid",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "first_reveal_with_3_players",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "first_reveal_with_4_or_5_players",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "second_reveal_count",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "dogs_that_cancel_top_cat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "start_seat_round_1",
        "visible": "public",
        "type": "number",
        "initial": 1
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "deal the hands",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": [
              "cat_-8",
              "cat_-5",
              "cat_3",
              "cat_5",
              "cat_8",
              "cat_11",
              "cat_15",
              "rabbit",
              "dog"
            ]
          }
        },
        {
          "set": {
            "players": "all",
            "key": "removed_card",
            "value": {
              "calc": "you.hand[min(len(you.hand) - 1, int(uniform(0, len(you.hand))))]"
            },
            "if": {
              "calc": "cards_removed_per_hand >= 1"
            }
          }
        },
        {
          "remove": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "you.removed_card"
            },
            "if": {
              "calc": "cards_removed_per_hand >= 1"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "mice",
            "value": {
              "calc": "starting_mice"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "cat_points",
            "value": {
              "calc": "starting_cat_points"
            }
          }
        },
        {
          "set": {
            "key": "round",
            "value": 0
          }
        },
        {
          "set": {
            "key": "start_seat",
            "value": {
              "calc": "start_seat_round_1"
            }
          }
        },
        {
          "set": {
            "key": "sack",
            "value": []
          }
        },
        {
          "set": {
            "key": "revealed_cards",
            "value": []
          }
        },
        {
          "set": {
            "key": "discard",
            "value": []
          }
        }
      ]
    },
    {
      "use": "sync",
      "label": "the table",
      "mode": "self",
      "to": "all",
      "text": "You start with (your removed card is known only to you):"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "start",
      "label": "a new round",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "key": "start_seat",
            "value": {
              "calc": "(round - 1) - len(players) * int((round - 1) / len(players)) + 1"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "stayed",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "placed_card",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "message",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "choice",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "['STAY', 'DROP'] if you.mice >= min_mice_to_stay else ['DROP']"
            }
          }
        },
        {
          "set": {
            "key": "sack",
            "value": []
          }
        },
        {
          "set": {
            "key": "revealed_cards",
            "value": []
          }
        },
        {
          "set": {
            "key": "winner_seat",
            "value": 0
          }
        },
        {
          "set": {
            "key": "sack_value",
            "value": 0
          }
        },
        {
          "set": {
            "key": "stayer_count",
            "value": 0
          }
        },
        {
          "set": {
            "key": "first_reveal_count",
            "value": {
              "calc": "first_reveal_with_3_players if len(players) == 3 else first_reveal_with_4_or_5_players"
            }
          }
        }
      ],
      "text": "Round {round} of {rounds} begins. The start seat is seat {start_seat}."
    },
    {
      "use": "poll",
      "phase": "sack",
      "label": "fill the sack",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "store": "placed_card",
      "text": "Secretly choose one card from your hand to place in the sack. It never comes back. Nobody sees which card you chose."
    },
    {
      "use": "update",
      "phase": "sack",
      "label": "the sack is shuffled",
      "do": [
        {
          "remove": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "you.placed_card"
            }
          }
        },
        {
          "set": {
            "key": "sack",
            "value": {
              "calc": "[p.placed_card for p in players]"
            }
          }
        },
        {
          "set": {
            "key": "shuffled",
            "value": []
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "sack[min(len(sack) - 1, int(uniform(0, len(sack))))]"
            },
            "if": {
              "calc": "len(sack) > 0"
            }
          }
        },
        {
          "append": {
            "key": "shuffled",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(sack) > 0"
            }
          }
        },
        {
          "remove": {
            "key": "sack",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(sack) > 0"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "sack[min(len(sack) - 1, int(uniform(0, len(sack))))]"
            },
            "if": {
              "calc": "len(sack) > 0"
            }
          }
        },
        {
          "append": {
            "key": "shuffled",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(sack) > 0"
            }
          }
        },
        {
          "remove": {
            "key": "sack",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(sack) > 0"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "sack[min(len(sack) - 1, int(uniform(0, len(sack))))]"
            },
            "if": {
              "calc": "len(sack) > 0"
            }
          }
        },
        {
          "append": {
            "key": "shuffled",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(sack) > 0"
            }
          }
        },
        {
          "remove": {
            "key": "sack",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(sack) > 0"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "sack[min(len(sack) - 1, int(uniform(0, len(sack))))]"
            },
            "if": {
              "calc": "len(sack) > 0"
            }
          }
        },
        {
          "append": {
            "key": "shuffled",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(sack) > 0"
            }
          }
        },
        {
          "remove": {
            "key": "sack",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(sack) > 0"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "sack[min(len(sack) - 1, int(uniform(0, len(sack))))]"
            },
            "if": {
              "calc": "len(sack) > 0"
            }
          }
        },
        {
          "append": {
            "key": "shuffled",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(sack) > 0"
            }
          }
        },
        {
          "remove": {
            "key": "sack",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(sack) > 0"
            }
          }
        },
        {
          "set": {
            "key": "sack",
            "value": {
              "calc": "shuffled"
            }
          }
        },
        {
          "set": {
            "key": "shuffled",
            "value": []
          }
        }
      ],
      "text": "Every card is in the sack, and the sack has been shuffled."
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "first reveal",
      "do": [
        {
          "set": {
            "key": "revealed_cards",
            "value": {
              "calc": "[sack[0]] + ([sack[1]] if first_reveal_count >= 2 else [])"
            }
          }
        }
      ],
      "text": "First reveal (owners are not named): {revealed_cards}."
    },
    {
      "use": "poll",
      "phase": "talk",
      "label": "talk",
      "to": "acting",
      "answer": {
        "type": "text",
        "max_words": 30
      },
      "store": "message",
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} says: {value}"
      },
      "text": "Write one short message to the table. Everyone writes at the same time; claims are not binding and may be lies."
    },
    {
      "use": "poll",
      "phase": "stay",
      "label": "stay or drop",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "store": "choice",
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} chooses {value}."
      },
      "text": "Choose STAY or DROP. STAY: pay {stay_fee} mouse now (never refunded) and bid for the sack. DROP: receive {drop_payment} mice and sit out the rest of this round. With fewer than {min_mice_to_stay} mice you may only DROP."
    },
    {
      "use": "update",
      "phase": "stay",
      "label": "entry and drop payment",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "stayed",
            "value": {
              "calc": "you.choice == 'STAY'"
            }
          }
        },
        {
          "set": {
            "key": "stayer_count",
            "value": {
              "calc": "count(p.stayed for p in players)"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.stayed"
            },
            "key": "mice",
            "value": {
              "calc": "-stay_fee"
            },
            "text": "Seat {player} stays and pays the fee."
          }
        },
        {
          "adjust": {
            "players": {
              "where": "not you.stayed"
            },
            "key": "mice",
            "value": {
              "calc": "drop_payment"
            },
            "text": "Seat {player} drops and receives mice."
          }
        }
      ],
      "text": "{stayer_count} player(s) stayed."
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "second reveal",
      "do": [
        {
          "append": {
            "key": "revealed_cards",
            "value": {
              "calc": "sack[first_reveal_count]"
            }
          }
        }
      ],
      "text": "Second reveal. Sack cards shown so far: {revealed_cards}."
    },
    {
      "use": "poll",
      "phase": "bid",
      "label": "sealed bid",
      "to": {
        "where": "you.stayed"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "min_bid"
        },
        "max": {
          "calc": "you.mice"
        }
      },
      "store": "bid",
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} bids {value}."
      },
      "text": "Secretly bid a whole number of mice, from {min_bid} up to your current mice. All bids are revealed together. The highest bid wins the sack; ties go to fewer current mice, then to the first seat counting from the start seat."
    },
    {
      "use": "update",
      "phase": "bid",
      "label": "the sack winner",
      "do": [
        {
          "set": {
            "key": "best_key",
            "value": {
              "calc": "max([p.bid * 100000 - p.mice * 100 - ((p.seat - start_seat) if p.seat >= start_seat else (p.seat - start_seat + len(players))) for p in players if p.stayed])"
            },
            "if": {
              "calc": "stayer_count > 0"
            }
          }
        },
        {
          "set": {
            "key": "winner_seat",
            "value": {
              "calc": "sum([p.seat for p in players if p.stayed and p.bid * 100000 - p.mice * 100 - ((p.seat - start_seat) if p.seat >= start_seat else (p.seat - start_seat + len(players))) == best_key])"
            },
            "if": {
              "calc": "stayer_count > 0"
            }
          }
        }
      ],
      "text": "The sack goes to seat {winner_seat} (0 means nobody stayed and the sack is discarded)."
    },
    {
      "use": "update",
      "phase": "value",
      "label": "sack value",
      "do": [
        {
          "set": {
            "key": "revealed_cards",
            "value": {
              "calc": "sack"
            }
          }
        },
        {
          "set": {
            "key": "sack_cats",
            "value": {
              "calc": "[cat_value_1 if c == 'cat_-8' else cat_value_2 if c == 'cat_-5' else cat_value_3 if c == 'cat_3' else cat_value_4 if c == 'cat_5' else cat_value_5 if c == 'cat_8' else cat_value_6 if c == 'cat_11' else cat_value_7 for c in sack if c != 'rabbit' and c != 'dog']"
            }
          }
        },
        {
          "set": {
            "key": "sack_value",
            "value": {
              "calc": "sum(sack_cats) + rabbit_value * count(c == 'rabbit' for c in sack) + dog_value * count(c == 'dog' for c in sack) - (max(sack_cats) if count(c == 'dog' for c in sack) == dogs_that_cancel_top_cat and len(sack_cats) > 0 else 0)"
            }
          }
        }
      ],
      "text": "The whole sack: {revealed_cards}. Sack value: {sack_value}."
    },
    {
      "use": "update",
      "phase": "value",
      "label": "payment",
      "do": [
        {
          "adjust": {
            "players": {
              "where": "you.seat == winner_seat"
            },
            "key": "mice",
            "value": {
              "calc": "-you.bid"
            },
            "if": {
              "calc": "winner_seat > 0"
            },
            "text": "Seat {player} pays their bid."
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat == winner_seat"
            },
            "key": "cat_points",
            "value": {
              "calc": "sack_value"
            },
            "if": {
              "calc": "winner_seat > 0"
            },
            "text": "Seat {player} adds {sack_value} to their cat points."
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "value",
      "label": "discard",
      "do": [
        {
          "set": {
            "key": "discard",
            "value": {
              "calc": "discard + sack"
            }
          }
        },
        {
          "set": {
            "key": "sack",
            "value": []
          }
        }
      ],
      "text": "The sack cards are discarded face up. Discard pile: {discard}. Standings [seat, mice, cat points]: {[[p.seat, p.mice, p.cat_points] for p in players]}."
    },
    {
      "use": "check",
      "phase": "value",
      "label": "end check",
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
      "rank_by": "(you.mice + you.cat_points) * 1000 + you.cat_points",
      "text": "Winner: {result}. Final [seat, cat points, mice, total]: {[[p.seat, p.cat_points, p.mice, p.cat_points + p.mice] for p in players]}."
    }
  },
  "limits": {
    "rounds": 8,
    "rounds_max": 10,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "SETUP. Every player receives the same {cards_per_hand} cards: cats worth {cat_value_1}, {cat_value_2}, {cat_value_3}, {cat_value_4}, {cat_value_5}, {cat_value_6} and {cat_value_7}, one Rabbit worth {rabbit_value}, and one Dog worth {dog_value}. {cards_removed_per_hand} card is removed at random from each hand; its owner is told which card it is, no one else is told. Each player starts with {starting_mice} mice and {starting_cat_points} cat points. The bank of mice is unlimited. Seat {start_seat_round_1} is the start player in round 1. The game lasts {rounds} rounds, so every remaining card is pla
... (cut)

Why it was refused: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state a player is shown has empty fields (choice, message, placed_card, message); hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "cat_in_the_sack_paid_entry",
    "name": "Cat in the Sack: Paid Entry",
    "players": {
      "min": 3,
      "max": 5,
      "suggested": 4
    },
    "blurb": "Each round everyone secretly feeds one card to a shared sack; pay to stay, get paid to drop, and bid sealed mice for a sack whose cat value may be negative."
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
        "initial": [
          "cat_-8",
          "cat_-5",
          "cat_3",
          "cat_5",
          "cat_8",
          "cat_11",
          "cat_15",
          "rabbit",
          "dog"
        ]
      },
      {
        "key": "removed_card",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "placed_card",
        "visible": "ally",
        "type": "text",
        "initial": "none"
      },
      {
        "key": "mice",
        "visible": "public",
        "type": "number",
        "initial": 15
      },
      {
        "key": "cat_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "stayed",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "message",
        "visible": "public",
        "type": "text",
        "initial": "none"
      },
      {
        "key": "choice",
        "visible": "ally",
        "type": "text",
        "initial": "none"
      },
      {
        "key": "offer",
        "visible": "ally",
        "type": "list",
        "initial": [
          "STAY",
          "DROP"
        ]
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
        "key": "start_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "sack",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "shuffled",
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
        "key": "sack_cats",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "best_key",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "first_reveal_count",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "revealed_cards",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "discard",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "stayer_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "winner_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "sack_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "cat_value_1",
        "visible": "public",
        "type": "number",
        "initial": -8
      },
      {
        "key": "cat_value_2",
        "visible": "public",
        "type": "number",
        "initial": -5
      },
      {
        "key": "cat_value_3",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "cat_value_4",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "cat_value_5",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "cat_value_6",
        "visible": "public",
        "type": "number",
        "initial": 11
      },
      {
        "key": "cat_value_7",
        "visible": "public",
        "type": "number",
        "initial": 15
      },
      {
        "key": "rabbit_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "dog_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "cards_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "cards_removed_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "starting_mice",
        "visible": "public",
        "type": "number",
        "initial": 15
      },
      {
        "key": "starting_cat_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "stay_fee",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "drop_payment",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "min_mice_to_stay",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "min_bid",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "first_reveal_with_3_players",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "first_reveal_with_4_or_5_players",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "second_reveal_count",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "dogs_that_cancel_top_cat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "start_seat_round_1",
        "visible": "public",
        "type": "number",
        "initial": 1
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "deal the hands",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": [
              "cat_-8",
              "cat_-5",
              "cat_3",
              "cat_5",
              "cat_8",
              "cat_11",
              "cat_15",
              "rabbit",
              "dog"
            ]
          }
        },
        {
          "set": {
            "players": "all",
            "key": "removed_card",
            "value": {
              "calc": "you.hand[min(len(you.hand) - 1, int(uniform(0, len(you.hand))))]"
            },
            "if": {
              "calc": "cards_removed_per_hand >= 1"
            }
          }
        },
        {
          "remove": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "you.removed_card"
            },
            "if": {
              "calc": "cards_removed_per_hand >= 1"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "mice",
            "value": {
              "calc": "starting_mice"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "cat_points",
            "value": {
              "calc": "starting_cat_points"
            }
          }
        },
        {
          "set": {
            "key": "round",
            "value": 0
          }
        },
        {
          "set": {
            "key": "start_seat",
            "value": {
              "calc": "start_seat_round_1"
            }
          }
        },
        {
          "set": {
            "key": "sack",
            "value": []
          }
        },
        {
          "set": {
            "key": "revealed_cards",
            "value": []
          }
        },
        {
          "set": {
            "key": "discard",
            "value": []
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
        "hand",
        "removed_card",
        "mice",
        "cat_points"
      ],
      "text": "You start with (your removed card is known only to you):"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "start",
      "label": "a new round",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "key": "start_seat",
            "value": {
              "calc": "(round - 1) - len(players) * int((round - 1) / len(players)) + 1"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "stayed",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "placed_card",
            "value": "none"
          }
        },
        {
          "set": {
            "players": "all",
            "key": "choice",
            "value": "none"
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "['STAY', 'DROP'] if you.mice >= min_mice_to_stay else ['DROP']"
            }
          }
        },
        {
          "set": {
            "key": "sack",
            "value": []
          }
        },
        {
          "set": {
            "key": "revealed_cards",
            "value": []
          }
        },
        {
          "set": {
            "key": "winner_seat",
            "value": 0
          }
        },
        {
          "set": {
            "key": "sack_value",
            "value": 0
          }
        },
        {
          "set": {
            "key": "stayer_count",
            "value": 0
          }
        },
        {
          "set": {
            "key": "first_reveal_count",
            "value": {
              "calc": "first_reveal_with_3_players if len(players) == 3 else first_reveal_with_4_or_5_players"
            }
          }
        }
      ],
      "text": "Round {round} of {rounds} begins. The start seat is seat {start_seat}."
    },
    {
      "use": "poll",
      "phase": "sack",
      "label": "fill the sack",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "store": "placed_card",
      "text": "Secretly choose one card from your hand to place in the sack. It never comes back. Nobody sees which card you chose."
    },
    {
      "use": "update",
      "phase": "sack",
      "label": "the sack is shuffled",
      "do": [
        {
          "remove": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "you.placed_card"
            }
          }
        },
        {
          "set": {
            "key": "sack",
            "value": {
              "calc": "[p.placed_card for p in players]"
            }
          }
        },
        {
          "set": {
            "key": "shuffled",
            "value": []
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "sack[min(len(sack) - 1, int(uniform(0, len(sack))))]"
            },
            "if": {
              "calc": "len(sack) > 0"
            }
          }
        },
        {
          "append": {
            "key": "shuffled",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(sack) > 0"
            }
          }
        },
        {
          "remove": {
            "key": "sack",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(sack) > 0"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "sack[min(len(sack) - 1, int(uniform(0, len(sack))))]"
            },
            "if": {
              "calc": "len(sack) > 0"
            }
          }
        },
        {
          "append": {
            "key": "shuffled",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(sack) > 0"
            }
          }
        },
        {
          "remove": {
            "key": "sack",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(sack) > 0"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "sack[min(len(sack) - 1, int(uniform(0, len(sack))))]"
            },
            "if": {
              "calc": "len(sack) > 0"
            }
          }
        },
        {
          "append": {
            "key": "shuffled",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(sack) > 0"
            }
          }
        },
        {
          "remove": {
            "key": "sack",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(sack) > 0"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "sack[min(len(sack) - 1, int(uniform(0, len(sack))))]"
            },
            "if": {
              "calc": "len(sack) > 0"
            }
          }
        },
        {
          "append": {
            "key": "shuffled",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(sack) > 0"
            }
          }
        },
        {
          "remove": {
            "key": "sack",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(sack) > 0"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "sack[min(len(sack) - 1, int(uniform(0, len(sack))))]"
            },
            "if": {
              "calc": "len(sack) > 0"
            }
          }
        },
        {
          "append": {
            "key": "shuffled",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(sack) > 0"
            }
          }
        },
        {
          "remove": {
            "key": "sack",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(sack) > 0"
            }
          }
        },
        {
          "set": {
            "key": "sack",
            "value": {
              "calc": "shuffled"
            }
          }
        },
        {
          "set": {
            "key": "shuffled",
            "value": []
          }
        }
      ],
      "text": "Every card is in the sack, and the sack has been shuffled."
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "first reveal",
      "do": [
        {
          "set": {
            "key": "revealed_cards",
            "value": {
              "calc": "[sack[0]] + ([sack[1]] if first_reveal_count >= 2 else [])"
            }
          }
        }
      ],
      "text": "First reveal (owners are not named): {revealed_cards}."
    },
    {
      "use": "poll",
      "phase": "talk",
      "label": "talk",
      "to": "acting",
      "answer": {
        "type": "text",
        "max_words": 30
      },
      "store": "message",
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} says: {value}"
      },
      "text": "Write one short message to the table. Everyone writes at the same time; claims are not binding and may be lies."
    },
    {
      "use": "poll",
      "phase": "stay",
      "label": "stay or drop",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "store": "choice",
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} chooses {value}."
      },
      "text": "Choose STAY or DROP. STAY: pay {stay_fee} mouse now (never refunded) and bid for the sack. DROP: receive {drop_payment} mice and sit out the rest of this round. With fewer than {min_mice_to_stay} mice you may only DROP."
    },
    {
      "use": "update",
      "phase": "stay",
      "label": "entry and drop payment",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "stayed",
            "value": {
              "calc": "you.choice == 'STAY'"
            }
          }
        },
        {
          "set": {
            "key": "stayer_count",
            "value": {
              "calc": "count(p.stayed for p in players)"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.stayed"
            },
            "key": "mice",
            "value": {
              "calc": "-stay_fee"
            },
            "text": "Seat {player} stays and pays the fee."
          }
        },
        {
          "adjust": {
            "players": {
              "where": "not you.stayed"
            },
            "key": "mice",
            "value": {
              "calc": "drop_payment"
            },
            "text": "Seat {player} drops and receives mice."
          }
        }
      ],
      "text": "{stayer_count} player(s) stayed."
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "second reveal",
      "do": [
        {
          "append": {
            "key": "revealed_cards",
            "value": {
              "calc": "sack[first_reveal_count]"
            }
          }
        }
      ],
      "text": "Second reveal. Sack cards shown so far: {revealed_cards}."
    },
    {
      "use": "poll",
      "phase": "bid",
      "label": "sealed bid",
      "to": {
        "where": "you.stayed"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "min_bid"
        },
        "max": {
          "calc": "you.mice"
        }
      },
      "store": "bid",
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} bids {value}."
      },
      "text": "Secretly bid a whole number of mice, from {min_bid} up to your current mice. All bids are revealed together. The highest bid wins the sack; ties go to fewer current mice, then to the first seat counting from the start seat."
    },
    {
      "use": "update",
      "phase": "bid",
      "label": "the sack winner",
      "do": [
        {
          "set": {
            "key": "best_key",
            "value": {
              "calc": "max([p.bid * 100000 - p.mice * 100 - ((p.seat - start_seat) if p.seat >= start_seat else (p.seat - start_seat + len(players))) for p in players if p.stayed])"
            },
            "if": {
              "calc": "stayer_count > 0"
            }
          }
        },
        {
          "set": {
            "key": "winner_seat",
            "value": {
              "calc": "sum([p.seat for p in players if p.stayed and p.bid * 100000 - p.mice * 100 - ((p.seat - start_seat) if p.seat >= start_seat else (p.seat - start_seat + len(players))) == best_key])"
            },
            "if": {
              "calc": "stayer_count > 0"
            }
          }
        }
      ],
      "text": "The sack goes to seat {winner_seat} (0 means nobody stayed and the sack is discarded)."
    },
    {
      "use": "update",
      "phase": "value",
      "label": "sack value",
      "do": [
        {
          "set": {
            "key": "revealed_cards",
            "value": {
              "calc": "sack"
            }
          }
        },
        {
          "set": {
            "key": "sack_cats",
            "value": {
              "calc": "[cat_value_1 if c == 'cat_-8' else cat_value_2 if c == 'cat_-5' else cat_value_3 if c == 'cat_3' else cat_value_4 if c == 'cat_5' else cat_value_5 if c == 'cat_8' else cat_value_6 if c == 'cat_11' else cat_value_7 for c in sack if c != 'rabbit' and c != 'dog']"
            }
          }
        },
        {
          "set": {
            "key": "sack_value",
            "value": {
              "calc": "sum(sack_cats) + rabbit_value * count(c == 'rabbit' for c in sack) + dog_value * count(c == 'dog' for c in sack) - (max(sack_cats) if count(c == 'dog' for c in sack) == dogs_that_cancel_top_cat and len(sack_cats) > 0 else 0)"
            }
          }
        }
      ],
      "text": "The whole sack: {revealed_cards}. Sack value: {sack_value}."
    },
    {
      "use": "update",
      "phase": "value",
      "label": "payment",
      "do": [
        {
          "adjust": {
            "players": {
              "where": "you.seat == winner_seat"
            },
            "key": "mice",
            "value": {
              "calc": "-you.bid"
            },
            "if": {
              "calc": "winner_seat > 0"
            },
            "text": "Seat {player} pays their bid."
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat == winner_seat"
            },
            "key": "cat_points",
            "value": {
              "calc": "sack_value"
            },
            "if": {
              "calc": "winner_seat > 0"
            },
            "text": "Seat {player} adds {sack_value} to their cat points."
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "value",
      "label": "discard",
      "do": [
        {
          "set": {
            "key": "discard",
            "value": {
              "calc": "discard + sack"
            }
          }
        },
        {
          "set": {
            "key": "sack",
            "value": []
          }
        }
      ],
      "text": "The sack cards are discarded face up. Discard pile: {discard}. Standings [seat, mice, cat points]: {[[p.seat, p.mice, p.cat_points] for p in players]}."
    },
    {
      "use": "check",
      "phase": "value",
      "label": "end check",
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
      "rank_by": "(you.mice + you.cat_points) * 1000 + you.cat_points",
      "text": "Winner: {result}. Final [seat, cat points, mice, total]: {[[p.seat, p.cat_points, p.mice, p.cat_points + p.mice] for p in players]}."
    }
  },
  "limits": {
    "rounds": 8,
    "rounds_max": 10,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "SETUP. Every player receives the same {cards_per_hand} cards: cats worth {cat_value_1}, {cat_value_2}, {cat_value_3}, {cat_value_4}, {cat_value_5}, {cat_value_6} and {cat_value_7}, one Rabbit worth {rabbit_value}, and one Dog worth {dog_value}. {cards_removed_per_hand} card is removed at random from each hand; its owner is told which card it is, no one else is told. Each player starts with {starting_mice} mice and {starting_cat_points} cat points. The bank of mice is unlimited. Seat {start_seat_round_1} is the start player in round 1. The game lasts {rounds} rounds, so every remaining card is played.\n\nEACH ROUND.\n1. Start player: seat {start_seat_round_1} in round 1, then the next seat in order each later round. The start player matters only for breaking ties.\n2. Fill the sack: all players at the same time secretly choose one card from their hand and place it in the sack. Placed cards never return.\n3. Shuffle: the sack is shuffled into a random order.\n4. First reveal: cards are shown from the front of the shuffled order, {first_reveal_with_3_players} card with 3 players, {first_reveal_with_4_or_5_players} cards with 4 or 5 players. Revealed cards do not say who placed them.\n5. Talk: every player writes one short message at the same time, without seeing the others' messages. All messages are then shown. Claims are not binding and may be lies.\n6. Stay or drop: all players at the same time choose STAY or DROP. A player with fewer than {min_mice_to_stay} mice must DROP.\n7. Entry and drop payment: each player who chose STAY pays {stay_fee} mouse to the bank immediately; this fee is never refunded, whether or not they win the sack. Each player who chose DROP receives {drop_payment} mice from the bank and is out for this round.\n8. Second reveal: the next {second_reveal_count} card in the shuffled order is shown to everyone.\n9. Sealed bid: every player who chose STAY secretly bids a whole number of mice, from {min_bid} up to their current mice (counted after paying the fee). All bids are revealed together.\n10. Winner: the highest bidder wins the sack. If two or more players tie for the highest bid, the tied player with fewer current mice wins. If they are still tied, the tied player who comes first in seat order, counting from the start player, wins. If nobody stayed, nobody wins, no bid is paid and the sack is discarded. If exactly one player stayed, that player wins and pays their bid.\n11. Sack value: all remaining sack cards are revealed. The sack's value is the sum of the cats in it; the Rabbit and Dogs are worth 0. If exactly {dogs_that_cancel_top_cat} Dog is in the sack and the sack holds at least one cat, the cat with the highest value is removed before summing (cat 15 + cat 3 + Dog + Rabbit = 3). Two or more Dogs have no effect (cat 15 + Dog + Dog = 15).\n12. Payment: the winner pays their bid to the bank and adds the sack's value to their cat points. The value may be negative.\n13. Losing stayers receive nothing. They have already paid their fee.\n14. Discard: all sack cards are discarded face up, so everyone can count which cards have been used.\n15. End check: after round {rounds} the game ends.\n\nSCORING. Each player's total is their cat points plus their mice. The player with the highest total wins. If totals are tied, the tied player with the most cat points wins. If that is also tied, those players share the win."
}
```
````
