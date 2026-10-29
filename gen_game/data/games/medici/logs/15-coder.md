# 15 coder

- time: 2026-10-27T18:33:32+00:00 (108.9s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 cf6340140c13578b, reply sha256 91877f9d7aea5a7e

## Sent

````
# Task: write the XColos game file for "Medici: Sealed Harbour"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

SETUP
- Players and money: 3 players in seats 1, 2 and 3. Each starts with 25 florins. Florin totals are public.
- Deck: 20 cards, one of each combination of 4 commodities (Grain, Cloth, Spice, Dye) and values 1, 2, 3, 4 and 5.
- Patron commodity: at the start of the game, 3 of the 4 commodities are dealt at random, one to each player, as that player's secret patron commodity. Each player sees only their own. The fourth commodity is nobody's patron.

STRUCTURE
- Days and rounds: the game has 3 days of 6 rounds each, 18 rounds in all.
- Start of day: the full 20-card deck is shuffled and every ship is empty. Each ship holds at most 3 cards per day.
- Seller order: day 1 begins with seat 1 as seller, day 2 with seat 2, day 3 with seat 3. The seller then moves to the next seat each round (1, 2, 3, 1, ...). Each player sells exactly twice per day.

EACH ROUND
1. Draw: the top card of the deck is revealed to everyone. This card is the lot.
2. Talk: all three players write one short message at the same time, without seeing the others. All messages are then shown to everyone. Talk is not binding.
3. Reserve: the seller secretly chooses a reserve price, a whole number from 1 to 6.
4. Bids: at the same moment, the two non-sellers each choose a sealed bid, a whole number from 0 to 10, no more than their current florins.
   - A bid of 0 means pass.
   - A player whose ship already holds 3 cards must bid 0.
5. Resolve, case A (a bid reaches the reserve): the highest bid wins. If the two bids tie, the bidder sitting first clockwise after the seller wins. The winner pays their bid to the seller and loads the card.
6. Resolve, case B (no bid reaches the reserve):
   - If the seller's ship has room, the seller must load the card and pay the reserve to the bank.
   - If the seller's ship is full, the card is discarded.
   - If the seller has fewer florins than the reserve, they pay all they have.
7. Reveal: the reserve, both bids, the buyer and the price are announced to everyone.

END OF EACH DAY (after round 6, 12 and 18)
- Ship prize: each player's ship value is the sum of the card values in their ship. Highest ship value receives 12 florins and second highest receives 6.
  - If two or more players tie, they add together the prizes for the places they occupy and split the sum equally, rounded down.
  - A player with an empty ship never receives a prize.
- Patron bonus: each player receives 3 florins for each card of their own patron commodity in their ship.
- Empty-slot penalty: each player pays the bank 2 florins for each empty slot in their ship (0 to 3 slots). Florins cannot drop below 0.
- Reset: ships are emptied and the next day begins.

How the winner is decided: After the end-of-day scoring of day 3, the player with the most florins wins. If two or three players tie for most, it is a draw between them.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Medici: Sealed Harbour (3 to 3 players, best with 3)

Three Florentine merchants spend 3 days auctioning commodity cards in sealed-bid rounds against a seller's secret reserve, filling 3-card ships for ship prizes and secret patron bonuses; the most florins wins.

STATE (every item below must exist in the file):
  - each player: florins (number, starts 25); everyone sees it. The player's florins. This is the score.
  - each player: patron (text, starts ''); only its owner sees it. The player's secret patron commodity, dealt from patron_pool.
  - each player: ship (list, starts []); everyone sees it. Cards loaded on the player's ship today, at most 3, such as 'Spice 4'. Public because every lot and buyer is announced.
  - each player: ship_count (number, starts 0); everyone sees it. Number of cards in ship (0 to 3).
  - each player: ship_value (number, starts 0); everyone sees it. Sum of the card values in ship.
  - each player: patron_cards (number, starts 0); only its owner sees it. Number of cards in ship whose commodity equals patron.
  - each player: reserve (number, starts 0); only its owner sees it. The secret reserve price set while this player is seller (1 to 6).
  - each player: bid (number, starts 0); only its owner sees it. This round's sealed bid (0 to 10, 0 = pass). Revealed at the reveal step.
  - the table: patron_pool (list, starts ['Grain', 'Cloth', 'Spice', 'Dye']); hidden from all players. Commodities from which patrons are dealt. The one left over is nobody's patron.
  - the table: deck (list, starts []); hidden from all players. The day's deck: the 20 cards Grain/Cloth/Spice/Dye x values 1-5, refilled at the start of each day.
  - the table: day (number, starts 1); everyone sees it. Current day (1 to 3).
  - the table: round (number, starts 1); everyone sees it. Current round overall (1 to 18).
  - the table: seller (number, starts 1); everyone sees it. Seat of this round's seller.
  - the table: lot (text, starts ''); everyone sees it. The card drawn this round.
  - the table: lot_commodity (text, starts ''); everyone sees it. Commodity of lot.
  - the table: lot_value (number, starts 0); everyone sees it. Value (1 to 5) of lot.
  - the table: buyer (number, starts 0); everyone sees it. Seat that loaded the lot this round. 0 if the lot was discarded.
  - the table: price (number, starts 0); everyone sees it. Florins paid for the lot this round.
  - parameters, each kept as a table attribute: start_florins = 25, deck_size = 20, commodity_count = 4, card_value_min = 1, card_value_max = 5, patron_commodities_dealt = 3, days = 3, rounds_per_day = 6, total_rounds = 18, ship_capacity = 3, sales_per_player_per_day = 2, reserve_min = 1, reserve_max = 6, bid_min = 0, bid_max = 10, first_ship_prize = 12, second_ship_prize = 6, patron_bonus_per_card = 3, empty_slot_penalty = 2, florin_floor = 0

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seats 1, 2 and 3 each receive florins = 25.
  2. Three commodities are drawn at random from patron_pool, one into each player's patron. The fourth stays in patron_pool and is nobody's patron.
  3. Each player sees only their own patron.
  4. Set day = 1 and round = 1.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: When (round - 1) mod 6 == 0 (start of a day): set deck to the full 20 cards (each of Grain, Cloth, Spice, Dye with each value 1-5). Every player's ship = [], ship_count = 0, ship_value = 0, patron_cards = 0.
  2. [update] all players. What happens: Set seller = ((day - 1) + ((round - 1) mod 6)) mod 3 + 1. Day 1 runs 1,2,3,1,2,3, day 2 runs 2,3,1,2,3,1, and day 3 runs 3,1,2,3,1,2.
  3. [update] all players. What happens: Draw: remove one card at random from deck and set lot to it. Set lot_commodity and lot_value from that card. Announce the lot to everyone.
  4. [poll] all players answers: short text message. What happens: All messages are shown together: broadcast {"to": "all", "text": "Seat {seat} says: {value}"}. The talk is not binding.
  5. [ask] seat seller answers: whole number 1 to 6. What happens: The seller's reserve = the answer, kept secret.
  6. [poll] the two players other than seller answers: whole number 0 to min(10, you.florins); exactly 0 if you.ship_count >= 3. What happens: Each non-seller's bid = the answer, sealed until all bids are in.
  7. [update] all players. What happens: Resolve. Let R = seller's reserve. Let F = (seller mod 3) + 1, the first bidder clockwise after the seller. Case A, at least one non-seller bid >= R: the winner is the non-seller with the higher bid among those with bid >= R; if the two bids are equal, F wins. The winner's florins -= bid and the seller's florins += that bid. Set buyer = winner and price = bid. Case B, no bid >= R: if the seller's ship_count < 3, set buyer = seller, price = min(R, seller.florins), and seller.florins -= price, paid to the bank; otherwise set buyer = 0 and price = 0, and the lot is discarded. If buyer != 0: append lot to buyer's ship, buyer.ship_count += 1, buyer.ship_value += lot_value, and if lot_commodity == buyer.patron then buyer.patron_cards += 1.
  8. [tell] all players. What happens: Reveal to everyone: the seller's reserve, both non-sellers' bids, the buyer (or 'discarded'), and the price.
  9. [update] all players. What happens: When round mod 6 == 0 (end of day), in this order. (1) Ship prize: for each player with ship_count > 0, let h = the number of players with ship_count > 0 and a higher ship_value, and k = the number of players with ship_count > 0 and an equal ship_value (including themself). Those players occupy places h+1 to h+k. Place prizes are 12 for place 1, 6 for place 2 and 0 otherwise. The player gains floor(sum of the prizes for places h+1..h+k / k). Players with ship_count == 0 gain nothing. (2) Patron bonus: florins += 3 * patron_cards. (3) Empty-slot penalty: florins = max(0, florins - 2 * (3 - ship_count)). (4) Reset: ship = [], ship_count = 0, ship_value = 0, patron_cards = 0, and day += 1.
  10. [update] all players. What happens: round += 1.
  11. [check] all players. What happens: End the game if round > 18. Otherwise continue with the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, then each of the 3 players has 25 public florins.
  R2. When the game starts, then 3 of the 4 commodities (Grain, Cloth, Spice, Dye) are dealt at random as secret patrons, one per player, and the fourth is nobody's patron.
  R3. When a player's patron is dealt, then only that player can see it.
  R4. When a day starts (rounds 1, 7 and 13), then the deck holds all 20 cards (4 commodities x values 1-5) and every ship is empty.
  R5. When it is round r of day d (r = 0 to 5 within the day), then the seller is seat ((d-1)+r) mod 3 + 1, so day 1 starts with seat 1, day 2 with seat 2 and day 3 with seat 3.
  R6. When a day is played, then each player is seller exactly 2 times.
  R7. When a round begins, then one card is drawn at random from the deck as the lot and shown to everyone.
  R8. When the talk step runs, then all 3 players submit a message at the same time and all messages are shown to everyone afterwards.
  R9. When the seller sets a reserve, then it is a whole number from 1 to 6 and stays secret until the reveal.
  R10. When the two non-sellers bid, then they bid simultaneously, each a whole number from 0 to 10 and at most their current florins, where 0 means pass.
  R11. When a non-seller's ship holds 3 cards, then their only allowed bid is 0.
  R12. When at least one bid is >= the reserve, then the higher such bid wins, the winner pays their bid to the seller, and the winner loads the lot (for example, reserve 4 with bids 5 and 3: the 5-bidder pays 5 to the seller).
  R13. When both bids are equal and >= the reserve, then the bidder at seat (seller mod 3)+1 wins (for example, seller 3 with bids of 6 and 6: seat 1 wins).
  R14. When no bid reaches the reserve and the seller's ship holds fewer than 3 cards, then the seller loads the lot and pays the reserve to the bank.
  R15. When no bid reaches the reserve and the seller has fewer florins than the reserve, then the seller pays all their florins and still loads the lot if the ship has room.
  R16. When no bid reaches the reserve and the seller's ship holds 3 cards, then the lot is discarded and no one pays.
  R17. When a round resolves, then the reserve, both bids, the buyer and the price are announced to everyone.
  R18. When a ship holds 3 cards, then it can take no more cards that day.
  R19. When a day ends (after rounds 6, 12 and 18), then the highest ship value receives 12 florins and the second highest receives 6.
  R20. When players tie for ship value at day end, then they add the prizes for the places they occupy and split the sum equally, rounded down (two tied for first get floor(18/2) = 9 each; three tied get floor(18/3) = 6 each; two tied for second get floor(6/2) = 3 each).
  R21. When a player's ship is empty at day end, then they receive no ship prize and occupy no place.
  R22. When a day ends, then each player gains 3 florins per card of their own patron commodity in their ship.
  R23. When a day ends, then each player pays 2 florins per empty ship slot (0 to 3 slots), and florins never drop below 0.
  R24. When day-end scoring is done, then all ships are emptied.
  R25. When round 18's day-end scoring is complete, then the game ends and the player with the most florins wins, with tied leaders sharing a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Talk message | asked: all three seats | options: Any short free-text message, every round.
  - Reserve price | asked: the seller only | options: A whole number from 1 to 6. Non-sellers are not asked.
  - Sealed bid | asked: the two non-sellers | options: A non-seller with ship_count < 3: a whole number from 0 to min(10, florins). A non-seller with ship_count = 3: 0 only. The seller is not asked.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round > 18
  - each player's standing: you.florins (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: After the end-of-day scoring of day 3, each player's standing is their florins. The most florins wins, and players tied for most share the win (a draw between them).
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

- each player: `florins` (number, visible: public, starts 25): The player's florins. This is the score.
- the table: `day` (number, visible: public, starts 1): Current day (1 to 3).
- the table: `round` (number, visible: public, starts 1): Current round overall (1 to 18).
- parameters (each must be an attribute holding this value, never a number buried in a step): start_florins = 25, deck_size = 20, commodity_count = 4, card_value_min = 1, card_value_max = 5, patron_commodities_dealt = 3, days = 3, rounds_per_day = 6, total_rounds = 18, ship_capacity = 3, sales_per_player_per_day = 2, reserve_min = 1, reserve_max = 6, bid_min = 0, bid_max = 10, first_ship_prize = 12, second_ship_prize = 6, patron_bonus_per_card = 3, empty_slot_penalty = 2, florin_floor = 0
- the game ends with ONE ending whose `rank_by` is `you.florins`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
```json
{
  "schema": 1,
  "meta": {
    "id": "medici_sealed_harbour",
    "name": "Medici: Sealed Harbour",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Three merchants, three days, sealed bids against a secret reserve: fill your ship, please your secret patron, and end with the most florins."
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
        "key": "florins",
        "visible": "public",
        "type": "number",
        "initial": 25
      },
      {
        "key": "patron",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "ship",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "ship_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "ship_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "patron_cards",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "reserve",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bid",
        "visible": "ally",
        "type": "number",
        "initial": 0
      }
    ],
    "game": [
      {
        "key": "patron_pool",
        "visible": "none",
        "type": "list",
        "initial": [
          "Grain",
          "Cloth",
          "Spice",
          "Dye"
        ]
      },
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "full_deck",
        "visible": "none",
        "type": "list",
        "initial": [
          "Grain 1",
          "Grain 2",
          "Grain 3",
          "Grain 4",
          "Grain 5",
          "Cloth 1",
          "Cloth 2",
          "Cloth 3",
          "Cloth 4",
          "Cloth 5",
          "Spice 1",
          "Spice 2",
          "Spice 3",
          "Spice 4",
          "Spice 5",
          "Dye 1",
          "Dye 2",
          "Dye 3",
          "Dye 4",
          "Dye 5"
        ]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "day",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "seller",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "lot",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "lot_commodity",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "lot_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "buyer",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "price",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "last_reserve",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "seat_f",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "seat_g",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bid_f",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bid_g",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "winner",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "start_florins",
        "visible": "public",
        "type": "number",
        "initial": 25
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "commodity_count",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "card_value_min",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "card_value_max",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "patron_commodities_dealt",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "days",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "rounds_per_day",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "total_rounds",
        "visible": "public",
        "type": "number",
        "initial": 18
      },
      {
        "key": "ship_capacity",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "sales_per_player_per_day",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "reserve_min",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "reserve_max",
        "visible": "public",
        "type": "number",
        "initial": 6
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
        "initial": 10
      },
      {
        "key": "first_ship_prize",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "second_ship_prize",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "patron_bonus_per_card",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "empty_slot_penalty",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "florin_floor",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the purses",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "florins",
            "value": {
              "calc": "start_florins"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "deal the patrons",
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "patron_pool[int(uniform(0, len(patron_pool)))]"
            }
          }
        },
        {
          "set": {
            "player": 1,
            "key": "patron",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "patron_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "patron_pool[int(uniform(0, len(patron_pool)))]"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "patron",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "patron_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "patron_pool[int(uniform(0, len(patron_pool)))]"
            }
          }
        },
        {
          "set": {
            "player": 3,
            "key": "patron",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "patron_pool",
            "value": {
              "calc": "pick"
            }
          }
        }
      ]
    },
    {
      "use": "sync",
      "label": "your patron",
      "mode": "self",
      "to": "all",
      "fields": [
        "patron",
        "florins"
      ],
      "text": "Your secret patron and purse:"
    },
    {
      "use": "update",
      "label": "the calendar",
      "do": [
        {
          "set": {
            "key": "day",
            "value": 1
          }
        },
        {
          "set": {
            "key": "round",
            "value": 1
          }
        }
      ]
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "dawn",
      "label": "a new day",
      "when": {
        "calc": "(round - 1) % rounds_per_day == 0"
      },
      "do": [
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
            "key": "ship",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "ship_count",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "ship_value",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "patron_cards",
            "value": 0
          }
        }
      ],
      "text": "Day {day} begins. The full deck is shuffled and every ship is empty."
    },
    {
      "use": "update",
      "phase": "draw",
      "label": "the seller",
      "do": [
        {
          "set": {
            "key": "seller",
            "value": {
              "calc": "((day - 1) + ((round - 1) % rounds_per_day)) % len(players) + 1"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "draw",
      "label": "the lot",
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
          "set": {
            "key": "lot",
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
            "key": "lot_commodity",
            "value": {
              "calc": "'Grain' if lot[0] == 'G' else ('Cloth' if lot[0] == 'C' else ('Spice' if lot[0] == 'S' else 'Dye'))"
            }
          }
        },
        {
          "set": {
            "key": "lot_value",
            "value": {
              "calc": "int(lot[-1])"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": 0
          }
        }
      ],
      "text": "Round {round} (day {day}). Seat {seller} is the seller. The lot is {lot}."
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
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} says: {value}"
      },
      "text": "The lot is {lot} and seat {seller} is selling. Say one short thing to the table. Talk is not binding."
    },
    {
      "use": "ask",
      "phase": "reserve",
      "label": "the reserve",
      "to": {
        "where": "you.seat == seller"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "reserve_min"
        },
        "max": {
          "calc": "reserve_max"
        }
      },
      "verify": {
        "bind": "res"
      },
      "text": "You are selling {lot}. Choose a secret reserve price from {reserve_min} to {reserve_max}. If no bid reaches it and your ship has room, you must load the lot yourself and pay the reserve to the bank."
    },
    {
      "use": "poll",
      "phase": "bids",
      "label": "sealed bids",
      "to": {
        "where": "you.seat != seller and you.ship_count < ship_capacity and you.florins > 0"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "bid_min"
        },
        "max": {
          "calc": "min(bid_max, you.florins)"
        }
      },
      "store": "bid",
      "text": "Seat {seller} is selling {lot} against a secret reserve. Enter a sealed bid, a whole number from {bid_min} up to {bid_max} and no more than your florins; 0 means pass."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "resolve the sale",
      "do": [
        {
          "set": {
            "player": {
              "calc": "seller"
            },
            "key": "reserve",
            "value": "$res"
          }
        },
        {
          "set": {
            "key": "last_reserve",
            "value": "$res"
          }
        },
        {
          "set": {
            "key": "seat_f",
            "value": {
              "calc": "seller % len(players) + 1"
            }
          }
        },
        {
          "set": {
            "key": "seat_g",
            "value": {
              "calc": "(seller + 1) % len(players) + 1"
            }
          }
        },
        {
          "set": {
            "key": "bid_f",
            "value": {
              "calc": "sum([p.bid for p in players if p.seat == seat_f])"
            }
          }
        },
        {
          "set": {
            "key": "bid_g",
            "value": {
              "calc": "sum([p.bid for p in players if p.seat == seat_g])"
            }
          }
        },
        {
          "set": {
            "key": "winner",
            "value": {
              "calc": "seat_f if (bid_f >= last_reserve and bid_f >= bid_g) else (seat_g if bid_g >= last_reserve else 0)"
            }
          }
        },
        {
          "set": {
            "key": "buyer",
            "value": {
              "calc": "winner if winner > 0 else (seller if sum([p.ship_count for p in players if p.seat == seller]) < ship_capacity else 0)"
            }
          }
        },
        {
          "set": {
            "key": "price",
            "value": {
              "calc": "(bid_f if winner == seat_f else bid_g) if winner > 0 else (min(last_reserve, sum([p.florins for p in players if p.seat == seller])) if buyer == seller else 0)"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "buyer"
            },
            "key": "florins",
            "value": {
              "calc": "-price"
            },
            "if": {
              "calc": "buyer > 0 and price > 0"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "seller"
            },
            "key": "florins",
            "value": {
              "calc": "price"
            },
            "if": {
              "calc": "winner > 0"
            }
          }
        },
        {
          "append": {
            "player": {
              "calc": "buyer"
            },
            "key": "ship",
            "value": {
              "calc": "lot"
            },
            "if": {
              "calc": "buyer > 0"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "buyer"
            },
            "key": "ship_count",
            "value": 1,
            "if": {
              "calc": "buyer > 0"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "buyer"
            },
            "key": "ship_value",
            "value": {
              "calc": "lot_value"
            },
            "if": {
              "calc": "buyer > 0"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "buyer"
            },
            "key": "patron_cards",
            "value": 1,
            "if": {
              "calc": "buyer > 0 and count(p.seat == buyer and p.patron == lot_commodity for p in players) > 0"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "reveal",
      "label": "the reveal",
      "when": {
        "calc": "buyer > 0"
      },
      "to": "all",
      "text": "Reveal: seller seat {seller} set reserve {last_reserve}. Seat {seat_f} bid {bid_f}; seat {seat_g} bid {bid_g}. Seat {buyer} loads {lot} for {price} florins."
    },
    {
      "use": "tell",
      "phase": "reveal",
      "label": "the lot is discarded",
      "when": {
        "calc": "buyer == 0"
      },
      "to": "all",
      "text": "Reveal: seller seat {seller} set reserve {last_reserve}. Seat {seat_f} bid {bid_f}; seat {seat_g} bid {bid_g}. No bid reached the reserve and the seller's ship is full: {lot} is discarded. Price 0."
    },
    {
      "use": "update",
      "phase": "day end",
      "label": "day-end scoring",
      "when": {
        "calc": "round % rounds_per_day == 0"
      },
      "do": [
        {
          "adjust": {
            "players": {
              "where": "you.ship_count > 0"
            },
            "key": "florins",
            "value": {
              "calc": "int(((first_ship_prize if count(p.ship_count > 0 and p.ship_value > you.ship_value for p in players) == 0 else 0) + (second_ship_prize if (count(p.ship_count > 0 and p.ship_value > you.ship_value for p in players) <= 1 and count(p.ship_count > 0 and p.ship_value >= you.ship_value for p in players) >= 2) else 0)) / count(p.ship_count > 0 and p.ship_value == you.ship_value for p in players))"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "florins",
            "value": {
              "calc": "patron_bonus_per_card * you.patron_cards"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "florins",
            "value": {
              "calc": "max(florin_floor, you.florins - empty_slot_penalty * (ship_capacity - you.ship_count))"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "ship",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "ship_count",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "ship_value",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "patron_cards",
            "value": 0
          }
        },
        {
          "adjust": {
            "key": "day",
            "value": 1
          }
        }
      ],
      "text": "The day is over: ship prizes, patron bonuses and empty-slot penalties are paid, and the ships are emptied. Florins: seat 1 {players[0].florins}, seat 2 {players[1].florins}, seat 3 {players[2].florins}."
    },
    {
      "use": "update",
      "phase": "day end",
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
      "use": "check",
      "phase": "day end",
      "label": "after round 18",
      "when": {
        "calc": "round > total_rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round > total_rounds"
      },
      "rank_by": "you.florins",
      "reveal": [
        "patron"
      ],
      "text": "Winner: {result}. Final florins: Seat 1 {players[0].florins}, Seat 2 {players[1].florins}, Seat 3 {players[2].florins}."
    }
  },
  "limits": {
    "rounds": 18,
    "rounds_max": 20,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "Three Florentine merchants in seats 1, 2 and 3. Each starts with {start_florins} florins; florin totals are public.\n\nThe deck has {deck_size} cards: one of each combination of {commodity_count} commodities (Grain, Cloth, Spice, Dye) and values {card_value_min} to {card_value_max}. At the start of the game, {patron_commodities_dealt} of the 4 commodities are dealt at random, one to each player, as that player's secret patron commodity. Each player sees only their own. The fourth commodity is nobody's patron.\n\nThe game has {days} days of {rounds_per_day} rounds each, {total_rounds} rounds in all. At the start of each day the full deck is shuffled and every ship is empty. Each ship holds at most {ship_capacity} cards per day; a full ship can take no more cards that day. Day 1 begins with seat 1 as seller, day 2 with seat 2, day 3 with seat 3, and the seller then moves to the next seat each round (1, 2, 3, 1, ...), so each player sells exactly {sales_per_player_per_day} times per day.\n\nEACH ROUND\n1. Draw: the top card of the deck is revealed to everyone. This card is the lot.\n2. Talk: all three players write one short message at the same time, without seeing the others. All messages are then shown to everyone. Talk is not binding.\n3. Reserve: the seller secretly chooses a reserve price, a whole number from {reserve_min} to {reserve_max}.\n4. Bids: at the same moment, the two non-sellers each choose a sealed bid, a whole number from {bid_min} to {bid_max}, no more than their current florins. A bid of 0 means pass. A player whose ship already holds {ship_capacity} cards must bid 0 (they are not asked; their bid is 0), as is a player with no florins.\n5. Resolve, case A (a bid reaches the reserve): the highest bid wins. If the two bids tie, the bidder sitting first clockwise after the seller wins. The winner pays their bid to the seller and loads the card.\n6. Resolve, case B (no bid reaches the reserve): if the seller's ship has room, the seller must load the card and pay the reserve to the bank. If the seller's ship is full, the card is discarded and no one pays. If the seller has fewer florins than the reserve, they pay all they have and still load the card if the ship has room.\n7. Reveal: the reserve, both bids, the buyer and the price are announced to everyone.\n\nEND OF EACH DAY (after rounds 6, 12 and 18)\n- Ship prize: each player's ship value is the sum of the card values in their ship. Highest ship value receives {first_ship_prize} florins and second highest receives {second_ship_prize}. If two or more players tie, they add together the prizes for the places they occupy and split the sum equally, rounded down (two tied for first get 9 each; three tied get 6 each; two tied for second get 3 each). A player with an empty ship never receives a prize and occupies no place.\n- Patron bonus: each player receives {patron_bonus_per_card} florins for each card of their own patron commodity in their ship.\n- Empty-slot penalty: each player pays the bank {empty_slot_penalty} florins for each empty slot in their ship (0 to 3 slots). Florins cannot drop below {florin_floor}.\n- Reset: ships are emptied and the next day begins.\n\nAfter the end-of-day scoring of day 3, the player with the most florins wins. If two or three players tie for most, it is a draw between them."
}
```
````
