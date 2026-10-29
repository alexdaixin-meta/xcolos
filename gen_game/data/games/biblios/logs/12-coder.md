# 12 coder

- time: 2026-10-27T20:56:05+00:00 (87.6s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 29b9c1a33b3fb52c, reply sha256 fa8e9367b07446c2

## Sent

````
# Task: write the XColos game file for "Scriptorium Lots (Seller's Edition)"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

SETUP
- 3 players, seated 1, 2, 3.
- Each player starts with 12 gold. Gold is public.
- Each player has a holding of 0 in each of three colours: Red, Blue, Green.
- A player always knows their own holdings. Other players' holdings are never shown during the game.
- Each colour has a public worth, starting at 3.

THE LOT LIST
- The lot list is public and contains exactly these 12 lots of two cards each: R1+B4, R2+B3, B1+R4, B2+R3, R1+G4, R2+G3, G1+R4, G2+R3, B1+G4, B2+G3, G1+B4, G2+B3.
- R1 means a Red card of value 1, B4 a Blue card of value 4, and so on.
- Every lot sums to 5. Every individual card appears in exactly two lots.
- Before round 1, the 12 lots are put in a random hidden order. Round k uses the k-th lot, so all 12 lots are used, one per round.

ROUNDS
- There are 12 rounds.
- The active player is seat 1 in round 1, seat 2 in round 2, seat 3 in round 3, seat 1 in round 4, and so on. Each seat is active 4 times.
- The two other players are the bidders.

EACH ROUND
1. Private view. This round's lot is shown to the active player only. No other player ever sees it.
2. Keep. The active player chooses one of the two cards to keep. Its value is added secretly to that player's holding in its colour.
3. Announce. The other card (the auction card) is announced to everyone: its colour and value. Others can deduce the kept card's value (5 minus the auction value), but its colour is one of the two lots containing the auction card. Lots already used narrow this down.
4. Talk. All three players each write one short message at the same time, without seeing the others. All messages are then shown to everyone. Messages are not binding and may be false.
5. Bid. The two bidders, at the same time, each submit a whole-number bid from 0 up to the gold they hold.
6. Resolve. Both bids are announced.
   - If one bid is strictly higher, that bidder wins. The winner pays the bid to the active player (gold moves from winner to active player). The winner adds the auction card's value to their holding in its colour.
   - If the bids are equal (including both 0), nobody pays. The active player adds the auction card's value to their own holding in its colour.
   - The log records who received the auction card.
7. Shift worth. If a bidder won, that winner may choose one colour and raise its worth by 1 or lower it by 1, or change nothing. Worth stays between 1 and 5: a change past these limits has no effect. If nobody won, no shift happens. The worths are announced.

END OF GAME (after round 12)
- For each colour, compare the three players' holdings.
- The single highest holder scores VP equal to that colour's final worth.
- If two or three players tie for highest, each tied player scores half the worth, rounded down.
- If everyone holds 0 in a colour, nobody scores that colour.
- Each player also scores 1 VP for every full 4 gold they hold (gold divided by 4, rounded down).
- A player's VP is the colour VP plus the gold VP.

How the winner is decided: The player with the most VP wins. If players tie on VP, the tied player with more remaining gold wins. If still tied, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Scriptorium Lots (Seller's Edition) (3 to 3 players, best with 3)

Three players take turns seeing a secret two-card lot. The active player keeps one card and auctions the other to the two bidders. Winners can nudge colour worths, and majorities in each colour plus leftover gold decide the victor.

STATE (every item below must exist in the file):
  - each player: gold (number, starts 12); everyone sees it. Gold held; spent on bids, received when selling; 1 VP per full 4 at the end
  - each player: red (number, starts 0); only its owner sees it. Own Red holding (sum of Red card values received); never shown to others during the game
  - each player: blue (number, starts 0); only its owner sees it. Own Blue holding
  - each player: green (number, starts 0); only its owner sees it. Own Green holding
  - each player: bid (number, starts 0); only its owner sees it. This round's sealed bid (bidders only); announced at resolve
  - each player: message (text, starts ''); everyone sees it. This round's non-binding talk message, shown after all are in
  - each player: vp (number, starts 0); everyone sees it. Final victory points = colour VP + floor(gold/4), computed after round 12
  - the table: lots (list, starts ['R1+B4', 'R2+B3', 'B1+R4', 'B2+R3', 'R1+G4', 'R2+G3', 'G1+R4', 'G2+R3', 'B1+G4', 'B2+G3', 'G1+B4', 'G2+B3']); hidden from all players. The 12 lots in a hidden random order fixed at setup; round k uses the k-th lot
  - the table: lot_list (list, starts ['R1+B4', 'R2+B3', 'B1+R4', 'B2+R3', 'R1+G4', 'R2+G3', 'G1+R4', 'G2+R3', 'B1+G4', 'B2+G3', 'G1+B4', 'G2+B3']); everyone sees it. The public list of all 12 lots, in unshuffled form
  - the table: current_lot (text, starts ''); hidden from all players. This round's lot; revealed privately to the active seat only
  - the table: round (number, starts 1); everyone sees it. Current round, 1 to 12
  - the table: active_seat (number, starts 1); everyone sees it. Seat that sells this round: ((round-1) mod 3) + 1
  - the table: auction_colour (text, starts ''); everyone sees it. Colour of this round's auction card
  - the table: auction_value (number, starts 0); everyone sees it. Value of this round's auction card; the kept card's value is 5 minus this
  - the table: auction_recipient (number, starts 0); everyone sees it. Seat that received the auction card this round, as recorded in the log
  - the table: winner_seat (number, starts 0); everyone sees it. Seat of the winning bidder this round, or 0 if the bids tied
  - the table: worth_red (number, starts 3); everyone sees it. Public worth of Red, kept between 1 and 5
  - the table: worth_blue (number, starts 3); everyone sees it. Public worth of Blue, kept between 1 and 5
  - the table: worth_green (number, starts 3); everyone sees it. Public worth of Green, kept between 1 and 5
  - parameters, each kept as a table attribute: start_gold = 12, start_holding = 0, start_worth = 3, worth_min = 1, worth_max = 5, worth_shift = 1, rounds = 12, lot_count = 12, cards_per_lot = 2, lot_sum = 5, lots_per_card = 2, active_turns_per_seat = 4, min_bid = 0, tie_share_divisor = 2, gold_per_vp = 4, rank_vp_weight = 1000

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seat the 3 players as seats 1, 2 and 3.
  2. Each player gets gold = 12 and red = blue = green = 0.
  3. Set worth_red = worth_blue = worth_green = 3.
  4. Shuffle the 12 lots into the hidden table list `lots` with a seeded random order. The public `lot_list` shows all 12 lots, unordered.
  5. Set round = 1.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] engine. What happens: Set active_seat = ((round - 1) mod 3) + 1. Set current_lot = lots[round]. Reset every player's bid to 0, and reset winner_seat and auction_recipient to 0.
  2. [ask] the active seat (active_seat) answers: one of the two cards of current_lot, shown only to this seat (e.g. 'R2' or 'G3'). What happens: Add the kept card's value to the active seat's holding in its colour (red, blue or green). Set auction_colour and auction_value to the other card. No other player sees current_lot or the kept card.
  3. [tell] all players. What happens: Announce: 'Round {round}: seat {active_seat} auctions {auction_colour} {auction_value}.'
  4. [poll] all players answers: short text. What happens: Set each player's message, then broadcast {"to": "all", "text": "Seat {seat} says: {value}"} once all are in. Messages are not binding.
  5. [poll] the two seats other than active_seat answers: a whole number from 0 to that bidder's gold. What happens: Set each bidder's bid. No bid is seen until both are in.
  6. [update] engine. What happens: Announce both bids. If one bid is strictly higher, set winner_seat to that bidder: the winner's gold falls by the bid, the active seat's gold rises by the bid, the auction_value is added to the winner's holding in auction_colour, and auction_recipient = winner_seat. If the bids are equal (including 0 and 0), nobody pays: the auction_value is added to the active seat's holding in auction_colour, and auction_recipient = active_seat.
  7. [ask] seat winner_seat, when winner_seat > 0 answers: one of: no change, Red +1, Red -1, Blue +1, Blue -1, Green +1, Green -1. What happens: Adjust the chosen worth by 1, but only if the result stays within 1..5; otherwise nothing changes.
  8. [tell] all players. What happens: Announce: 'Seat {auction_recipient} received the auction card. Worths: Red {worth_red}, Blue {worth_blue}, Green {worth_green}.'
  9. [update] engine. What happens: Increase round by 1.
  10. [update] engine, when round > 12. What happens: For each colour C with worth W: let M = the highest holding in C, and N = the number of players holding M. If M = 0, nobody scores C. If N = 1, that player gains W colour VP. If N >= 2, each tied player gains floor(W / 2). Then set each player's vp = colour VP + floor(gold / 4), and reveal all holdings.
  11. [check] engine. What happens: End the game if round > 12; otherwise continue with the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. At the start, each player has 12 gold and 0 Red, 0 Blue and 0 Green, and each colour's worth is 3.
  R2. Gold and worths are public; each player's holdings are visible only to that player until the end of the game.
  R3. The 12 lots (R1+B4, R2+B3, B1+R4, B2+R3, R1+G4, R2+G3, G1+R4, G2+R3, B1+G4, B2+G3, G1+B4, G2+B3) are put in a hidden random order, and round k uses the k-th lot, so each lot is used exactly once.
  R4. In round k, the active seat is ((k-1) mod 3) + 1, so seats 1, 2 and 3 are each active 4 times in 12 rounds.
  R5. When a round begins, only the active seat is shown the lot; no other player ever sees it.
  R6. When the active seat keeps a card, that card's value is added to the active seat's holding in its colour, e.g. keeping G3 adds 3 to green.
  R7. When a card is kept, the other card's colour and value are announced to everyone as the auction card.
  R8. Each round, all three players submit one short text message simultaneously, and all messages are then shown to everyone.
  R9. The two non-active seats bid simultaneously, each a whole number from 0 up to their current gold.
  R10. When one bid is strictly higher, that bidder pays the bid to the active seat and adds the auction card's value to their holding in its colour; e.g. bids 5 and 3 for B4 move 5 gold from the winner to the active seat and add 4 to the winner's blue.
  R11. When the bids are equal (including 0 and 0), no gold moves, and the active seat adds the auction card's value to their own holding in its colour.
  R12. Each round, auction_recipient records the seat that received the auction card.
  R13. When a bidder wins, that bidder may raise or lower one colour's worth by 1, or change nothing.
  R14. A worth change that would take a worth below 1 or above 5 has no effect; e.g. Red at 5 with Red +1 stays 5.
  R15. When the bids tie, no worth shift happens.
  R16. After each round's resolution, the three worths are announced.
  R17. The game ends after round 12.
  R18. At the end, the single highest holder of a colour scores VP equal to that colour's worth; e.g. a sole Red leader with Red worth 4 gains 4 VP.
  R19. At the end, when two or three players tie for highest in a colour, each scores floor(worth / 2); e.g. worth 5 gives each tied player 2 VP.
  R20. At the end, when all players hold 0 in a colour, nobody scores that colour.
  R21. At the end, each player scores floor(gold / 4) VP; e.g. 15 gold gives 3 VP.
  R22. The player with the most VP wins; a VP tie is broken by more gold; players still tied share the result as a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Keep a card | asked: the active seat only | options: exactly the two cards of this round's lot, e.g. for lot R2+G3: R2, G3
  - Talk message | asked: all three seats | options: any short text
  - Bid | asked: the two seats other than the active seat | options: any whole number from 0 to that seat's current gold; the active seat is not asked
  - Shift worth | asked: the winning bidder only, and only when a bidder won | options: no change, Red +1, Red -1, Blue +1, Blue -1, Green +1, Green -1 (all always offered; a change past 1 or 5 has no effect); nobody is asked after a tie

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round > 12
  - each player's standing: you.vp * 1000 + you.gold (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Most VP wins (colour majorities at final worth, plus 1 VP per full 4 gold). A tie on VP is broken by more remaining gold. Players still tied share the win, which stands for the source's draw.
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

- each player: `gold` (number, visible: public, starts 12): Gold held; spent on bids, received when selling; 1 VP per full 4 at the end
- each player: `vp` (number, visible: public, starts 0): Final victory points = colour VP + floor(gold/4), computed after round 12
- the table: `auction_recipient` (number, visible: public, starts 0): Seat that received the auction card this round, as recorded in the log
- the table: `worth_red` (number, visible: public, starts 3): Public worth of Red, kept between 1 and 5
- the table: `worth_blue` (number, visible: public, starts 3): Public worth of Blue, kept between 1 and 5
- the table: `worth_green` (number, visible: public, starts 3): Public worth of Green, kept between 1 and 5
- parameters (each must be an attribute holding this value, never a number buried in a step): start_gold = 12, start_holding = 0, start_worth = 3, worth_min = 1, worth_max = 5, worth_shift = 1, rounds = 12, lot_count = 12, cards_per_lot = 2, lot_sum = 5, lots_per_card = 2, active_turns_per_seat = 4, min_bid = 0, tie_share_divisor = 2, gold_per_vp = 4, rank_vp_weight = 1000
- the game ends with ONE ending whose `rank_by` is `you.vp * 1000 + you.gold`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
    "id": "scriptorium_lots_sellers_edition",
    "name": "Scriptorium Lots (Seller's Edition)",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "See a secret two-card lot, keep one card, auction the other, nudge colour worths, and win colour majorities."
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
        "key": "gold",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "red",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "blue",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "green",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bid",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "message",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "vp",
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
        "key": "lots",
        "visible": "none",
        "type": "list",
        "initial": [
          "R1+B4",
          "R2+B3",
          "B1+R4",
          "B2+R3",
          "R1+G4",
          "R2+G3",
          "G1+R4",
          "G2+R3",
          "B1+G4",
          "B2+G3",
          "G1+B4",
          "G2+B3"
        ]
      },
      {
        "key": "lot_list",
        "visible": "public",
        "type": "list",
        "initial": [
          "R1+B4",
          "R2+B3",
          "B1+R4",
          "B2+R3",
          "R1+G4",
          "R2+G3",
          "G1+R4",
          "G2+R3",
          "B1+G4",
          "B2+G3",
          "G1+B4",
          "G2+B3"
        ]
      },
      {
        "key": "pool",
        "visible": "none",
        "type": "list",
        "initial": [
          "R1+B4",
          "R2+B3",
          "B1+R4",
          "B2+R3",
          "R1+G4",
          "R2+G3",
          "G1+R4",
          "G2+R3",
          "B1+G4",
          "B2+G3",
          "G1+B4",
          "G2+B3"
        ]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "current_lot",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "kept_card",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "auction_card",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "active_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "auction_colour",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "auction_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "auction_recipient",
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
        "key": "worth_red",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "worth_blue",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "worth_green",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "bidder_a",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bidder_b",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bid_a",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bid_b",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "high_bid",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "shift_choice",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "top_red",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "top_blue",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "top_green",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "n_red",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "n_blue",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "n_green",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "start_gold",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "start_holding",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "start_worth",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "worth_min",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "worth_max",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "worth_shift",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "lot_count",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "cards_per_lot",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "lot_sum",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "lots_per_card",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "active_turns_per_seat",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "min_bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tie_share_divisor",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "gold_per_vp",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "rank_vp_weight",
        "visible": "public",
        "type": "number",
        "initial": 1000
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "starting holdings and worths",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "gold",
            "value": {
              "calc": "start_gold"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "red",
            "value": {
              "calc": "start_holding"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "blue",
            "value": {
              "calc": "start_holding"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "green",
            "value": {
              "calc": "start_holding"
            }
          }
        },
        {
          "set": {
            "key": "worth_red",
            "value": {
              "calc": "start_worth"
            }
          }
        },
        {
          "set": {
            "key": "worth_blue",
            "value": {
              "calc": "start_worth"
            }
          }
        },
        {
          "set": {
            "key": "worth_green",
            "value": {
              "calc": "start_worth"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "post the public lot list",
      "do": [
        {
          "set": {
            "key": "lot_list",
            "value": {
              "calc": "pool"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "shuffle the lots",
      "do": [
        {
          "set": {
            "key": "lots",
            "value": []
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "pool[int(uniform(0, len(pool)))]"
            }
          }
        },
        {
          "append": {
            "key": "lots",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "pool[int(uniform(0, len(pool)))]"
            }
          }
        },
        {
          "append": {
            "key": "lots",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "pool[int(uniform(0, len(pool)))]"
            }
          }
        },
        {
          "append": {
            "key": "lots",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "pool[int(uniform(0, len(pool)))]"
            }
          }
        },
        {
          "append": {
            "key": "lots",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "pool[int(uniform(0, len(pool)))]"
            }
          }
        },
        {
          "append": {
            "key": "lots",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "pool[int(uniform(0, len(pool)))]"
            }
          }
        },
        {
          "append": {
            "key": "lots",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "pool[int(uniform(0, len(pool)))]"
            }
          }
        },
        {
          "append": {
            "key": "lots",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "pool[int(uniform(0, len(pool)))]"
            }
          }
        },
        {
          "append": {
            "key": "lots",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "pool[int(uniform(0, len(pool)))]"
            }
          }
        },
        {
          "append": {
            "key": "lots",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "pool[int(uniform(0, len(pool)))]"
            }
          }
        },
        {
          "append": {
            "key": "lots",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "pool[int(uniform(0, len(pool)))]"
            }
          }
        },
        {
          "append": {
            "key": "lots",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "pool[int(uniform(0, len(pool)))]"
            }
          }
        },
        {
          "append": {
            "key": "lots",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "pool",
            "value": {
              "calc": "pick"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "first round",
      "do": [
        {
          "set": {
            "key": "round",
            "value": 1
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
      "phase": "lot",
      "label": "start the round",
      "do": [
        {
          "set": {
            "key": "active_seat",
            "value": {
              "calc": "round - 1 - len(players) * int((round - 1) / len(players)) + 1"
            }
          }
        },
        {
          "set": {
            "key": "current_lot",
            "value": {
              "calc": "lots[round - 1]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "[lots[round - 1][0] + lots[round - 1][1], lots[round - 1][3] + lots[round - 1][4]] if you.seat == active_seat else []"
            }
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
            "key": "message",
            "value": ""
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
            "key": "auction_recipient",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "lot",
      "label": "keep a card",
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "keep_pick"
      },
      "text": "Round {round}: you are the seller. Your secret lot holds the two cards offered to you. Keep one of them; its value goes secretly into your holding in its colour. The other card is auctioned to the two bidders."
    },
    {
      "use": "update",
      "phase": "lot",
      "label": "the kept card",
      "do": [
        {
          "set": {
            "key": "kept_card",
            "value": "$keep_pick"
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "active_seat"
            },
            "key": "red",
            "value": {
              "calc": "int(kept_card[1])"
            },
            "if": {
              "calc": "kept_card[0] == 'R'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "active_seat"
            },
            "key": "blue",
            "value": {
              "calc": "int(kept_card[1])"
            },
            "if": {
              "calc": "kept_card[0] == 'B'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "active_seat"
            },
            "key": "green",
            "value": {
              "calc": "int(kept_card[1])"
            },
            "if": {
              "calc": "kept_card[0] == 'G'"
            }
          }
        },
        {
          "set": {
            "key": "auction_card",
            "value": {
              "calc": "current_lot[3] + current_lot[4] if kept_card == current_lot[0] + current_lot[1] else current_lot[0] + current_lot[1]"
            }
          }
        },
        {
          "set": {
            "key": "auction_colour",
            "value": {
              "calc": "'Red' if auction_card[0] == 'R' else ('Blue' if auction_card[0] == 'B' else 'Green')"
            }
          }
        },
        {
          "set": {
            "key": "auction_value",
            "value": {
              "calc": "int(auction_card[1])"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "lot",
      "label": "announce the auction card",
      "to": "all",
      "text": "Round {round}: seat {active_seat} auctions {auction_colour} {auction_value}."
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
      "text": "Write one short message to the table. Everyone writes at the same time and all messages are then shown. Messages are not binding and may be false."
    },
    {
      "use": "poll",
      "phase": "bid",
      "label": "bid",
      "to": {
        "where": "you.seat != active_seat"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "min_bid"
        },
        "max": {
          "calc": "you.gold"
        }
      },
      "store": "bid",
      "text": "Seat {active_seat} auctions {auction_colour} {auction_value}. Submit a sealed whole-number bid from {min_bid} up to your gold. If your bid is strictly higher, you pay it to the seller and take the card; if the bids are equal, nobody pays and the seller takes the card."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "resolve the auction",
      "do": [
        {
          "set": {
            "key": "bidder_a",
            "value": {
              "calc": "min([p.seat for p in players if p.seat != active_seat])"
            }
          }
        },
        {
          "set": {
            "key": "bidder_b",
            "value": {
              "calc": "max([p.seat for p in players if p.seat != active_seat])"
            }
          }
        },
        {
          "set": {
            "key": "bid_a",
            "value": {
              "calc": "sum([p.bid for p in players if p.seat == bidder_a])"
            }
          }
        },
        {
          "set": {
            "key": "bid_b",
            "value": {
              "calc": "sum([p.bid for p in players if p.seat == bidder_b])"
            }
          }
        },
        {
          "set": {
            "key": "high_bid",
            "value": {
              "calc": "max(bid_a, bid_b)"
            }
          }
        },
        {
          "set": {
            "key": "winner_seat",
            "value": {
              "calc": "bidder_a if bid_a > bid_b else (bidder_b if bid_b > bid_a else 0)"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "winner_seat"
            },
            "key": "gold",
            "value": {
              "calc": "-high_bid"
            },
            "if": {
              "calc": "winner_seat > 0 and sum([p.gold for p in players if p.seat == winner_seat]) >= high_bid"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "active_seat"
            },
            "key": "gold",
            "value": {
              "calc": "high_bid"
            },
            "if": {
              "calc": "winner_seat > 0"
            }
          }
        },
        {
          "set": {
            "key": "auction_recipient",
            "value": {
              "calc": "winner_seat if winner_seat > 0 else active_seat"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "auction_recipient"
            },
            "key": "red",
            "value": {
              "calc": "auction_value"
            },
            "if": {
              "calc": "auction_colour == 'Red'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "auction_recipient"
            },
            "key": "blue",
            "value": {
              "calc": "auction_value"
            },
            "if": {
              "calc": "auction_colour == 'Blue'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "auction_recipient"
            },
            "key": "green",
            "value": {
              "calc": "auction_value"
            },
            "if": {
              "calc": "auction_colour == 'Green'"
            }
          }
        }
      ],
      "text": "Bids: seat {bidder_a} bid {bid_a}, seat {bidder_b} bid {bid_b}. Winning bidder: {winner_seat} (0 means the bids tied and nobody pays)."
    },
    {
      "use": "ask",
      "phase": "shift",
      "label": "shift worth",
      "when": {
        "calc": "winner_seat > 0"
      },
      "to": {
        "where": "you.seat == winner_seat"
      },
      "answer": {
        "type": "choice",
        "options": [
          "no change",
          "Red +1",
          "Red -1",
          "Blue +1",
          "Blue -1",
          "Green +1",
          "Green -1"
        ]
      },
      "verify": {
        "bind": "shift_pick"
      },
      "text": "You won the auction. You may raise or lower one colour's worth by {worth_shift}, or change noth
... (cut)

Why it was refused: it plays, but part of it does nothing: game attribute `lot_list` is never changed in 3 random matches, so nothing updates it. Steps that name it: post the public lot list. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "scriptorium_lots_sellers_edition",
    "name": "Scriptorium Lots (Seller's Edition)",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "See a secret two-card lot, keep one card, auction the other, nudge colour worths, and win colour majorities."
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
        "key": "gold",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "red",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "blue",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "green",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bid",
        "visible": "ally",
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
        "key": "vp",
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
        "key": "lots",
        "visible": "none",
        "type": "list",
        "initial": [
          "R1+B4",
          "R2+B3",
          "B1+R4",
          "B2+R3",
          "R1+G4",
          "R2+G3",
          "G1+R4",
          "G2+R3",
          "B1+G4",
          "B2+G3",
          "G1+B4",
          "G2+B3"
        ]
      },
      {
        "key": "lot_list",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "pool",
        "visible": "none",
        "type": "list",
        "initial": [
          "R1+B4",
          "R2+B3",
          "B1+R4",
          "B2+R3",
          "R1+G4",
          "R2+G3",
          "G1+R4",
          "G2+R3",
          "B1+G4",
          "B2+G3",
          "G1+B4",
          "G2+B3"
        ]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "current_lot",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "kept_card",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "auction_card",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "active_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "auction_colour",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "auction_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "auction_recipient",
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
        "key": "worth_red",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "worth_blue",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "worth_green",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "bidder_a",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bidder_b",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bid_a",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bid_b",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "high_bid",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "shift_choice",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "top_red",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "top_blue",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "top_green",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "n_red",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "n_blue",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "n_green",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "start_gold",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "start_holding",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "start_worth",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "worth_min",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "worth_max",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "worth_shift",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "lot_count",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "cards_per_lot",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "lot_sum",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "lots_per_card",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "active_turns_per_seat",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "min_bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tie_share_divisor",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "gold_per_vp",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "rank_vp_weight",
        "visible": "public",
        "type": "number",
        "initial": 1000
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "starting holdings and worths",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "gold",
            "value": {
              "calc": "start_gold"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "red",
            "value": {
              "calc": "start_holding"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "blue",
            "value": {
              "calc": "start_holding"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "green",
            "value": {
              "calc": "start_holding"
            }
          }
        },
        {
          "set": {
            "key": "worth_red",
            "value": {
              "calc": "start_worth"
            }
          }
        },
        {
          "set": {
            "key": "worth_blue",
            "value": {
              "calc": "start_worth"
            }
          }
        },
        {
          "set": {
            "key": "worth_green",
            "value": {
              "calc": "start_worth"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "post the public lot list",
      "do": [
        {
          "set": {
            "key": "lot_list",
            "value": {
              "calc": "pool"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "shuffle the lots",
      "do": [
        {
          "set": {
            "key": "lots",
            "value": []
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "pool[int(uniform(0, len(pool)))]"
            }
          }
        },
        {
          "append": {
            "key": "lots",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "pool[int(uniform(0, len(pool)))]"
            }
          }
        },
        {
          "append": {
            "key": "lots",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "pool[int(uniform(0, len(pool)))]"
            }
          }
        },
        {
          "append": {
            "key": "lots",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "pool[int(uniform(0, len(pool)))]"
            }
          }
        },
        {
          "append": {
            "key": "lots",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "pool[int(uniform(0, len(pool)))]"
            }
          }
        },
        {
          "append": {
            "key": "lots",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "pool[int(uniform(0, len(pool)))]"
            }
          }
        },
        {
          "append": {
            "key": "lots",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "pool[int(uniform(0, len(pool)))]"
            }
          }
        },
        {
          "append": {
            "key": "lots",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "pool[int(uniform(0, len(pool)))]"
            }
          }
        },
        {
          "append": {
            "key": "lots",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "pool[int(uniform(0, len(pool)))]"
            }
          }
        },
        {
          "append": {
            "key": "lots",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "pool[int(uniform(0, len(pool)))]"
            }
          }
        },
        {
          "append": {
            "key": "lots",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "pool[int(uniform(0, len(pool)))]"
            }
          }
        },
        {
          "append": {
            "key": "lots",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "pool[int(uniform(0, len(pool)))]"
            }
          }
        },
        {
          "append": {
            "key": "lots",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "pool",
            "value": {
              "calc": "pick"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "first round",
      "do": [
        {
          "set": {
            "key": "round",
            "value": 1
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
      "phase": "lot",
      "label": "start the round",
      "do": [
        {
          "set": {
            "key": "active_seat",
            "value": {
              "calc": "round - 1 - len(players) * int((round - 1) / len(players)) + 1"
            }
          }
        },
        {
          "set": {
            "key": "current_lot",
            "value": {
              "calc": "lots[round - 1]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "[lots[round - 1][0] + lots[round - 1][1], lots[round - 1][3] + lots[round - 1][4]] if you.seat == active_seat else []"
            }
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
            "key": "message",
            "value": ""
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
            "key": "auction_recipient",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "lot",
      "label": "keep a card",
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "keep_pick"
      },
      "text": "Round {round}: you are the seller. Your secret lot holds the two cards offered to you. Keep one of them; its value goes secretly into your holding in its colour. The other card is auctioned to the two bidders."
    },
    {
      "use": "update",
      "phase": "lot",
      "label": "the kept card",
      "do": [
        {
          "set": {
            "key": "kept_card",
            "value": "$keep_pick"
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "active_seat"
            },
            "key": "red",
            "value": {
              "calc": "int(kept_card[1])"
            },
            "if": {
              "calc": "kept_card[0] == 'R'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "active_seat"
            },
            "key": "blue",
            "value": {
              "calc": "int(kept_card[1])"
            },
            "if": {
              "calc": "kept_card[0] == 'B'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "active_seat"
            },
            "key": "green",
            "value": {
              "calc": "int(kept_card[1])"
            },
            "if": {
              "calc": "kept_card[0] == 'G'"
            }
          }
        },
        {
          "set": {
            "key": "auction_card",
            "value": {
              "calc": "current_lot[3] + current_lot[4] if kept_card == current_lot[0] + current_lot[1] else current_lot[0] + current_lot[1]"
            }
          }
        },
        {
          "set": {
            "key": "auction_colour",
            "value": {
              "calc": "'Red' if auction_card[0] == 'R' else ('Blue' if auction_card[0] == 'B' else 'Green')"
            }
          }
        },
        {
          "set": {
            "key": "auction_value",
            "value": {
              "calc": "int(auction_card[1])"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "lot",
      "label": "announce the auction card",
      "to": "all",
      "text": "Round {round}: seat {active_seat} auctions {auction_colour} {auction_value}."
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
      "text": "Write one short message to the table. Everyone writes at the same time and all messages are then shown. Messages are not binding and may be false."
    },
    {
      "use": "poll",
      "phase": "bid",
      "label": "bid",
      "to": {
        "where": "you.seat != active_seat"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "min_bid"
        },
        "max": {
          "calc": "you.gold"
        }
      },
      "store": "bid",
      "text": "Seat {active_seat} auctions {auction_colour} {auction_value}. Submit a sealed whole-number bid from {min_bid} up to your gold. If your bid is strictly higher, you pay it to the seller and take the card; if the bids are equal, nobody pays and the seller takes the card."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "resolve the auction",
      "do": [
        {
          "set": {
            "key": "bidder_a",
            "value": {
              "calc": "min([p.seat for p in players if p.seat != active_seat])"
            }
          }
        },
        {
          "set": {
            "key": "bidder_b",
            "value": {
              "calc": "max([p.seat for p in players if p.seat != active_seat])"
            }
          }
        },
        {
          "set": {
            "key": "bid_a",
            "value": {
              "calc": "sum([p.bid for p in players if p.seat == bidder_a])"
            }
          }
        },
        {
          "set": {
            "key": "bid_b",
            "value": {
              "calc": "sum([p.bid for p in players if p.seat == bidder_b])"
            }
          }
        },
        {
          "set": {
            "key": "high_bid",
            "value": {
              "calc": "max(bid_a, bid_b)"
            }
          }
        },
        {
          "set": {
            "key": "winner_seat",
            "value": {
              "calc": "bidder_a if bid_a > bid_b else (bidder_b if bid_b > bid_a else 0)"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "winner_seat"
            },
            "key": "gold",
            "value": {
              "calc": "-high_bid"
            },
            "if": {
              "calc": "winner_seat > 0 and sum([p.gold for p in players if p.seat == winner_seat]) >= high_bid"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "active_seat"
            },
            "key": "gold",
            "value": {
              "calc": "high_bid"
            },
            "if": {
              "calc": "winner_seat > 0"
            }
          }
        },
        {
          "set": {
            "key": "auction_recipient",
            "value": {
              "calc": "winner_seat if winner_seat > 0 else active_seat"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "auction_recipient"
            },
            "key": "red",
            "value": {
              "calc": "auction_value"
            },
            "if": {
              "calc": "auction_colour == 'Red'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "auction_recipient"
            },
            "key": "blue",
            "value": {
              "calc": "auction_value"
            },
            "if": {
              "calc": "auction_colour == 'Blue'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "auction_recipient"
            },
            "key": "green",
            "value": {
              "calc": "auction_value"
            },
            "if": {
              "calc": "auction_colour == 'Green'"
            }
          }
        }
      ],
      "text": "Bids: seat {bidder_a} bid {bid_a}, seat {bidder_b} bid {bid_b}. Winning bidder: {winner_seat} (0 means the bids tied and nobody pays)."
    },
    {
      "use": "ask",
      "phase": "shift",
      "label": "shift worth",
      "when": {
        "calc": "winner_seat > 0"
      },
      "to": {
        "where": "you.seat == winner_seat"
      },
      "answer": {
        "type": "choice",
        "options": [
          "no change",
          "Red +1",
          "Red -1",
          "Blue +1",
          "Blue -1",
          "Green +1",
          "Green -1"
        ]
      },
      "verify": {
        "bind": "shift_pick"
      },
      "text": "You won the auction. You may raise or lower one colour's worth by {worth_shift}, or change nothing. Worths stay between {worth_min} and {worth_max}: a change past these limits has no effect. Current worths: Red {worth_red}, Blue {worth_blue}, Green {worth_green}."
    },
    {
      "use": "update",
      "phase": "shift",
      "label": "apply the worth shift",
      "when": {
        "calc": "winner_seat > 0"
      },
      "do": [
        {
          "set": {
            "key": "shift_choice",
            "value": "$shift_pick"
          }
        },
        {
          "adjust": {
            "key": "worth_red",
            "value": {
              "calc": "worth_shift"
            },
            "if": {
              "calc": "shift_choice == 'Red +1' and worth_red + worth_shift <= worth_max"
            }
          }
        },
        {
          "adjust": {
            "key": "worth_red",
            "value": {
              "calc": "-worth_shift"
            },
            "if": {
              "calc": "shift_choice == 'Red -1' and worth_red - worth_shift >= worth_min"
            }
          }
        },
        {
          "adjust": {
            "key": "worth_blue",
            "value": {
              "calc": "worth_shift"
            },
            "if": {
              "calc": "shift_choice == 'Blue +1' and worth_blue + worth_shift <= worth_max"
            }
          }
        },
        {
          "adjust": {
            "key": "worth_blue",
            "value": {
              "calc": "-worth_shift"
            },
            "if": {
              "calc": "shift_choice == 'Blue -1' and worth_blue - worth_shift >= worth_min"
            }
          }
        },
        {
          "adjust": {
            "key": "worth_green",
            "value": {
              "calc": "worth_shift"
            },
            "if": {
              "calc": "shift_choice == 'Green +1' and worth_green + worth_shift <= worth_max"
            }
          }
        },
        {
          "adjust": {
            "key": "worth_green",
            "value": {
              "calc": "-worth_shift"
            },
            "if": {
              "calc": "shift_choice == 'Green -1' and worth_green - worth_shift >= worth_min"
            }
          }
        }
      ],
      "text": "Seat {winner_seat} chose: {shift_choice}."
    },
    {
      "use": "tell",
      "phase": "shift",
      "label": "announce worths",
      "to": "all",
      "text": "Seat {auction_recipient} received the auction card. Worths: Red {worth_red}, Blue {worth_blue}, Green {worth_green}."
    },
    {
      "use": "update",
      "phase": "end",
      "label": "next round",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "end",
      "label": "final scoring",
      "when": {
        "calc": "round > rounds"
      },
      "do": [
        {
          "set": {
            "key": "top_red",
            "value": {
              "calc": "max([p.red for p in players])"
            }
          }
        },
        {
          "set": {
            "key": "top_blue",
            "value": {
              "calc": "max([p.blue for p in players])"
            }
          }
        },
        {
          "set": {
            "key": "top_green",
            "value": {
              "calc": "max([p.green for p in players])"
            }
          }
        },
        {
          "set": {
            "key": "n_red",
            "value": {
              "calc": "count(p.red == top_red for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "n_blue",
            "value": {
              "calc": "count(p.blue == top_blue for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "n_green",
            "value": {
              "calc": "count(p.green == top_green for p in players)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "vp",
            "value": {
              "calc": "((worth_red if n_red == 1 else int(worth_red / tie_share_divisor)) if (top_red > 0 and you.red == top_red) else 0) + ((worth_blue if n_blue == 1 else int(worth_blue / tie_share_divisor)) if (top_blue > 0 and you.blue == top_blue) else 0) + ((worth_green if n_green == 1 else int(worth_green / tie_share_divisor)) if (top_green > 0 and you.green == top_green) else 0) + int(you.gold / gold_per_vp)"
            }
          }
        }
      ],
      "text": "The game is over. Final worths: Red {worth_red}, Blue {worth_blue}, Green {worth_green}. Holdings are revealed and VP counted."
    },
    {
      "use": "check",
      "phase": "end",
      "label": "after round 12",
      "when": {
        "calc": "round > rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round > rounds"
      },
      "rank_by": "you.vp * 1000 + you.gold",
      "reveal": [
        "red",
        "blue",
        "green"
      ],
      "text": "Winner: {result}. Final VP (gold): Seat 1 {players[0].vp} ({players[0].gold}), Seat 2 {players[1].vp} ({players[1].gold}), Seat 3 {players[2].vp} ({players[2].gold})."
    }
  },
  "limits": {
    "rounds": 12,
    "rounds_max": 12,
    "actions_max": 1000,
    "deadline_s": 120
  },
  "rules": "Three players, seats 1, 2 and 3. Each player starts with {start_gold} gold and a holding of {start_holding} in each of three colours: Red, Blue and Green. Gold is public. You always know your own holdings; other players' holdings are never shown during the game. Each colour has a public worth, starting at {start_worth}.\n\nThe lot list is public and contains exactly these {lot_count} lots of two cards each: R1+B4, R2+B3, B1+R4, B2+R3, R1+G4, R2+G3, G1+R4, G2+R3, B1+G4, B2+G3, G1+B4, G2+B3. R1 means a Red card of value 1, B4 a Blue card of value 4, and so on. Every lot sums to {lot_sum}. Every individual card appears in exactly {lots_per_card} lots. Before round 1 the lots are put in a random hidden order; round k uses the k-th lot, so every lot is used once.\n\nThere are {rounds} rounds. The active player is seat 1 in round 1, seat 2 in round 2, seat 3 in round 3, seat 1 in round 4, and so on; each seat is active {active_turns_per_seat} times. The two other players are the bidders.\n\nEach round:\n1. Private view. The round's lot is shown to the active player only. No other player ever sees it.\n2. Keep. The active player chooses one of the two cards to keep. Its value is added secretly to that player's holding in its colour.\n3. Announce. The other card (the auction card) is announced to everyone: its colour and value. The kept card's value is {lot_sum} minus the auction value; its colour is one of the two lots containing the auction card, and lots already used narrow this down.\n4. Talk. All three players each write one short message at the same time, without seeing the others. All messages are then shown to everyone. Messages are not binding and may be false.\n5. Bid. The two bidders, at the same time, each submit a whole-number bid from {min_bid} up to the gold they hold.\n6. Resolve. Both bids are announced. If one bid is strictly higher, that bidder wins: the winner pays the bid to the active player and adds the auction card's value to their holding in its colour. If the bids are equal (including both 0), nobody pays and the active player adds the auction card's value to their own holding in its colour. The log records who received the auction card.\n7. Shift worth. If a bidder won, that winner may choose one colour and raise its worth by {worth_shift} or lower it by {worth_shift}, or change nothing. Worth stays between {worth_min} and {worth_max}: a change past these limits has no effect. If nobody won, no shift happens. The worths are announced.\n\nEnd of game (after round {rounds}): for each colour, compare the three players' holdings. The single highest holder scores VP equal to that colour's final worth. If two or three players tie for highest, each tied player scores half the worth, rounded down. If everyone holds 0 in a colour, nobody scores that colour. Each player also scores 1 VP for every full {gold_per_vp} gold they hold (gold divided by {gold_per_vp}, rounded down). Your VP is colour VP plus gold VP.\n\nThe player with the most VP wins. If players tie on VP, the tied player with more remaining gold wins. Players still tied share the win (a draw)."
}
```
````
