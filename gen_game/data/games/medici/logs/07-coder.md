# 07 coder

- time: 2026-10-27T18:21:58+00:00 (148.1s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 f5a5f9fef6e75508, reply sha256 49abb8f43bfee77b

## Sent

````
# Task: write the XColos game file for "Medici: Secret Patrons"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

SETUP. Three players sit in fixed order A, B, C. Each starts with 30 florins (public). Each has a ship with room for 5 cards and three public commodity tracks (Spice, Silk, Grain), all at 0. The three commodities are shuffled and one is dealt secretly to each player as their Patron, so every player has a different Patron and knows only their own. The deck has 30 cards: for each of Spice, Silk and Grain there are 10 cards valued 0, 1, 1, 2, 2, 3, 3, 4, 4, 5.

START OF EACH DAY. There are 3 days. Shuffle all 30 cards into a face-down deck and empty every ship (tracks are NOT reset). Turn the top 3 cards face up in a row: this is the Dock, ordered first, second, third. The first active player is A on day 1, B on day 2 and C on day 3. The active role then passes in seat order A, B, C, A... each round. Each day has exactly 9 rounds.

EACH ROUND.
(1) The Dock, all ships, tracks and florins are announced.
(2) The active player chooses a lot size of 1, 2 or 3 (no more than the cards in the Dock). The lot is the first that many Dock cards. Its size is its card count and its value is the sum of its card values.
(3) Auction, once around. The next player in seat order after the active player bids first, then the other non-active player, then the active player last. Each bidder either passes or bids a whole number that is at least 1, higher than the current highest bid, and no more than their florins. A player whose ship lacks room for the whole lot must pass.
(4) If anyone bid, the highest bidder pays that many florins to the bank and loads every card of the lot onto their ship. For each card loaded, that player's track in the card's commodity rises by 1, to a maximum of 10. If everyone passed, the lot is discarded.
(5) Remove the lot's cards from the Dock, slide the remaining Dock cards forward, and refill the Dock to 3 cards from the top of the deck (fewer if the deck runs out).

END OF DAY (after round 9 of the day).
(a) Ship scoring: rank players by total value of the cards on their ship. The highest gets 20 florins and the second gets 10. Tied players add the prizes for the places they occupy and split them equally, rounded down. A player with an empty ship gets nothing.
(b) Commodity majorities: for each commodity, the player with the highest track gets 10 florins and the second highest gets 5. Ties split as above. A track at 0 earns nothing.
(c) Patron: a player who earned a majority award in step (b) in their own Patron commodity receives that same amount again.
All awards are added to florins.

END OF GAME. After day 3 scoring, Patrons are revealed and the player with the most florins wins.

How the winner is decided: After the end-of-day scoring of day 3, the player with the most florins wins. If two or more players tie for the most, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Medici: Secret Patrons (3 to 3 players, best with 3)

Three merchants auction lots of commodity cards from a dock over 3 days of 9 rounds. They score for ship value, for commodity track majorities and a second time for majorities in their own secret Patron commodity. The most florins wins.

STATE (every item below must exist in the file):
  - each player: florins (number, starts 30); everyone sees it. Money, and also the score.
  - each player: patron (text, starts ''); only its owner sees it. The secret Patron commodity (Spice, Silk or Grain). Each player holds a different one. It is revealed at game end.
  - each player: ship (list, starts []); everyone sees it. Cards loaded on the ship this day, written as 'Commodity-value', e.g. 'Silk-3'.
  - each player: ship_count (number, starts 0); everyone sees it. Number of cards on the ship (at most 5).
  - each player: ship_value (number, starts 0); everyone sees it. Sum of the values of the cards on the ship.
  - each player: track_spice (number, starts 0); everyone sees it. Spice commodity track, 0 to 10, never reset.
  - each player: track_silk (number, starts 0); everyone sees it. Silk commodity track, 0 to 10, never reset.
  - each player: track_grain (number, starts 0); everyone sees it. Grain commodity track, 0 to 10, never reset.
  - the table: deck (list, starts []); hidden from all players. The face-down deck of the cards remaining this day.
  - the table: dock (list, starts []); everyone sees it. Face-up Dock cards in order first, second, third.
  - the table: day (number, starts 1); everyone sees it. Current day, 1 to 3. It becomes 4 when the game is over.
  - the table: round_in_day (number, starts 1); everyone sees it. Round number within the day, 1 to 9.
  - the table: active_seat (number, starts 1); everyone sees it. Seat of the active player this round (1=A, 2=B, 3=C).
  - the table: lot (list, starts []); everyone sees it. The cards in the current lot (the first lot_size Dock cards).
  - the table: lot_size (number, starts 0); everyone sees it. Number of cards in the current lot.
  - the table: lot_value (number, starts 0); everyone sees it. Sum of the card values in the current lot.
  - the table: high_bid (number, starts 0); everyone sees it. Current highest bid in this auction (0 = no bid yet).
  - the table: high_bidder (number, starts 0); everyone sees it. Seat of the current highest bidder (0 = nobody).
  - parameters, each kept as a table attribute: starting_florins = 30, ship_capacity = 5, days = 3, rounds_per_day = 9, dock_size = 3, max_lot_size = 3, min_lot_size = 1, min_bid = 1, deck_size = 30, commodities = 3, cards_per_commodity = 10, card_value_min = 0, card_value_max = 5, copies_of_value_0_per_commodity = 1, copies_of_value_1_per_commodity = 2, copies_of_value_2_per_commodity = 2, copies_of_value_3_per_commodity = 2, copies_of_value_4_per_commodity = 2, copies_of_value_5_per_commodity = 1, track_start = 0, track_max = 10, ship_prize_first = 20, ship_prize_second = 10, majority_prize_first = 10, majority_prize_second = 5, patron_multiplier_extra = 1

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seats are fixed in order A (seat 1), B (seat 2), C (seat 3).
  2. Every player gets florins = 30, all three tracks = 0, an empty ship, ship_count = 0 and ship_value = 0.
  3. The three commodities Spice, Silk and Grain are shuffled, and one is dealt secretly into each player's patron. Every player has a different Patron and sees only their own.
  4. day = 1 and round_in_day = 1.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: When round_in_day == 1 (start of a day): set deck to all 30 cards (Spice, Silk and Grain, each valued 0,1,1,2,2,3,3,4,4,5). Empty every ship and set ship_count = 0 and ship_value = 0 for all players (tracks are NOT reset). Empty dock, then draw 3 cards at random from deck, removing them, and append them in order to dock.
  2. [update] all players. What happens: active_seat = ((day - 1) + (round_in_day - 1)) mod 3 + 1. high_bid = 0, high_bidder = 0, lot = [], lot_size = 0, lot_value = 0.
  3. [tell] all players. What happens: Announce day, round_in_day, active_seat, the dock in order, and every player's ship, ship_value, track_spice, track_silk, track_grain and florins.
  4. [ask] the seat equal to active_seat answers: a whole number from 1 to min(3, length of dock). What happens: lot_size = answer. lot = the first lot_size cards of dock. lot_value = sum of the values of the cards in lot. Announce the lot.
  5. [ask] each player in turn: seat active_seat+1, then seat active_seat+2, then active_seat (seats counted mod 3) answers: 0 to pass, or a whole number at least max(1, high_bid + 1) and at most own florins. A seat with ship_count + lot_size > 5, or with florins <= high_bid, may only answer 0. What happens: If answer > 0: high_bid = answer, high_bidder = this seat. Each later bidder hears the earlier bids.
  6. [update] the seat equal to high_bidder. What happens: If high_bidder > 0: that player's florins -= high_bid. Append every card of lot to their ship. ship_count += lot_size. ship_value += lot_value. For each commodity, add the number of lot cards of that commodity to the matching track, capped at 10. Whether or not anyone bid, remove the lot cards from dock (if nobody bid they are discarded).
  7. [update] all players. What happens: Refill dock: while length of dock < 3 and deck is not empty, draw a random card from deck (remove it) and append it to the end of dock.
  8. [tell] all players. What happens: Announce who won the lot and for how much (high_bidder, high_bid), or that everyone passed and the lot was discarded.
  9. [update] all players. What happens: When round_in_day == 9, ship scoring. Only players with ship_count > 0 take part. For each such player, h = number of participants with a higher ship_value and e = number of participants with an equal ship_value (self included). The player occupies places h+1 to h+e. Prizes are place 1 = 20, place 2 = 10, place 3 = 0. florins += floor((sum of the prizes for places h+1..h+e) / e). Players with ship_count == 0 get nothing.
  10. [update] all players. What happens: When round_in_day == 9, for each commodity in Spice, Silk, Grain: only players with that track > 0 take part. For each such player, h = participants with a higher track and e = participants with an equal track (self included). Prizes are place 1 = 10, place 2 = 5, place 3 = 0. award = floor((sum of the prizes for places h+1..h+e) / e) and florins += award. If that commodity equals the player's patron, florins += award again (Patron bonus).
  11. [update] all players. What happens: round_in_day += 1. If round_in_day > 9: day += 1 and round_in_day = 1.
  12. [tell] all players. What happens: When day > 3: reveal every player's patron and announce final florins.
  13. [check] all players. What happens: If day > 3, end the game. Otherwise continue with the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, then each player has 30 florins, all three tracks at 0, an empty ship, and a secret patron that differs from the other two players' patrons.
  R2. When a day starts (round_in_day == 1), then the deck is reset to the 30 cards, every ship is emptied with ship_count 0 and ship_value 0, tracks keep their values, and the dock holds 3 cards drawn from the deck.
  R3. When it is day d and round r of that day, then active_seat = ((d-1)+(r-1)) mod 3 + 1, so A is active first on day 1, B on day 2 and C on day 3.
  R4. When the active player chooses a lot size, then it is 1, 2 or 3 and no more than the number of dock cards, and the lot is the first that many dock cards.
  R5. When the auction runs, then the seat after the active seat bids first, then the other non-active seat, then the active seat last, each exactly once.
  R6. When a player bids, then the bid is at least 1, higher than the current high_bid, and at most their florins. Otherwise they pass (answer 0).
  R7. When a player's ship_count + lot_size > 5, then that player may only pass.
  R8. When at least one player bid, then the highest bidder loses exactly high_bid florins, and their ship gains every lot card, ship_count rises by lot_size and ship_value rises by lot_value.
  R9. When a player loads a card, then their track in that card's commodity rises by 1, but never above 10.
  R10. When every player passes, then the lot is discarded and no florins, ships or tracks change.
  R11. When a lot is resolved, then its cards leave the dock, the remaining dock cards keep their order, and the dock is refilled to 3 from the deck, or fewer if the deck is empty.
  R12. When round 9 of a day ends, then among players with non-empty ships the highest ship_value gains 20 florins and the second gains 10.
  R13. When players tie in ship scoring, then they add the prizes of the places they occupy and each gets the sum divided equally, rounded down: two tied first get 15 each, three tied first get 10 each, two tied second get 5 each.
  R14. When a player's ship is empty at end of day, then they get no ship prize.
  R15. When round 9 of a day ends, then for each commodity the highest track (above 0) gains 10 florins and the second highest gains 5, with ties split as in R13 (two tied first get 7 each, two tied second get 2 each, three tied first get 5 each).
  R16. When a player's track in a commodity is 0, then they earn no majority award in that commodity.
  R17. When a player earns a majority award in the commodity equal to their patron, then they gain that same amount again.
  R18. When the day 3 scoring is done, then the patrons are revealed and the game ends.
  R19. When the game ends, then the player with the most florins wins, and players tied for the most share the result (a draw).

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Lot size | asked: the active seat only | options: the whole numbers 1 to min(3, number of dock cards). With a full dock this is 1, 2 or 3.
  - Auction bid | asked: each seat once, starting after the active seat and ending with the active seat | options: a seat with ship_count + lot_size <= 5 and florins > high_bid: 0 (pass) or any whole number from max(1, high_bid+1) to its florins. A seat whose ship lacks room, or whose florins do not exceed high_bid: 0 (pass) only.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: day > 3
  - each player's standing: you.florins (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: After the day 3 end-of-day scoring, each player's standing is their florins. The player with the most florins wins. Players tied for the most share the top, which the source calls a draw.
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

- each player: `florins` (number, visible: public, starts 30): Money, and also the score.
- each player: `track_spice` (number, visible: public, starts 0): Spice commodity track, 0 to 10, never reset.
- each player: `track_silk` (number, visible: public, starts 0): Silk commodity track, 0 to 10, never reset.
- each player: `track_grain` (number, visible: public, starts 0): Grain commodity track, 0 to 10, never reset.
- the table: `day` (number, visible: public, starts 1): Current day, 1 to 3. It becomes 4 when the game is over.
- parameters (each must be an attribute holding this value, never a number buried in a step): starting_florins = 30, ship_capacity = 5, days = 3, rounds_per_day = 9, dock_size = 3, max_lot_size = 3, min_lot_size = 1, min_bid = 1, deck_size = 30, commodities = 3, cards_per_commodity = 10, card_value_min = 0, card_value_max = 5, copies_of_value_0_per_commodity = 1, copies_of_value_1_per_commodity = 2, copies_of_value_2_per_commodity = 2, copies_of_value_3_per_commodity = 2, copies_of_value_4_per_commodity = 2, copies_of_value_5_per_commodity = 1, track_start = 0, track_max = 10, ship_prize_first = 20, ship_prize_second = 10, majority_prize_first = 10, majority_prize_second = 5, patron_multiplier_extra = 1
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
    "id": "medici_secret_patrons",
    "name": "Medici: Secret Patrons",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Three merchants auction lots of Spice, Silk and Grain over 3 days, scoring ship value, track majorities and a secret Patron bonus."
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
        "initial": 30
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
        "key": "track_spice",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "track_silk",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "track_grain",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ],
    "game": [
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
          "Spice-0", "Spice-1", "Spice-1", "Spice-2", "Spice-2", "Spice-3", "Spice-3", "Spice-4", "Spice-4", "Spice-5",
          "Silk-0", "Silk-1", "Silk-1", "Silk-2", "Silk-2", "Silk-3", "Silk-3", "Silk-4", "Silk-4", "Silk-5",
          "Grain-0", "Grain-1", "Grain-1", "Grain-2", "Grain-2", "Grain-3", "Grain-3", "Grain-4", "Grain-4", "Grain-5"
        ]
      },
      {
        "key": "patron_pool",
        "visible": "none",
        "type": "list",
        "initial": [
          "Spice",
          "Silk",
          "Grain"
        ]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "dock",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "day",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "round_in_day",
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
        "key": "lot",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "lot_size",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "lot_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "high_bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "high_bidder",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "starting_florins",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "ship_capacity",
        "visible": "public",
        "type": "number",
        "initial": 5
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
        "initial": 9
      },
      {
        "key": "dock_size",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "max_lot_size",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "min_lot_size",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "min_bid",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "commodities",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "cards_per_commodity",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "card_value_min",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "card_value_max",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "copies_of_value_0_per_commodity",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "copies_of_value_1_per_commodity",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "copies_of_value_2_per_commodity",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "copies_of_value_3_per_commodity",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "copies_of_value_4_per_commodity",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "copies_of_value_5_per_commodity",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "track_start",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "track_max",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "ship_prize_first",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "ship_prize_second",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "majority_prize_first",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "majority_prize_second",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "patron_multiplier_extra",
        "visible": "public",
        "type": "number",
        "initial": 1
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the merchants",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "florins",
            "value": {
              "calc": "starting_florins"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "track_spice",
            "value": {
              "calc": "track_start"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "track_silk",
            "value": {
              "calc": "track_start"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "track_grain",
            "value": {
              "calc": "track_start"
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
              "calc": "patron_pool[min(len(patron_pool) - 1, int(uniform(0, len(patron_pool))))]"
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
              "calc": "patron_pool[min(len(patron_pool) - 1, int(uniform(0, len(patron_pool))))]"
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
              "calc": "patron_pool[0]"
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
      "use": "update",
      "label": "the first day",
      "do": [
        {
          "set": {
            "key": "day",
            "value": 1
          }
        },
        {
          "set": {
            "key": "round_in_day",
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
      "phase": "dawn",
      "label": "a new day",
      "when": {
        "calc": "round_in_day == 1"
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
            "key": "dock",
            "value": []
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"
            }
          }
        },
        {
          "append": {
            "key": "dock",
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
              "calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"
            }
          }
        },
        {
          "append": {
            "key": "dock",
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
              "calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"
            }
          }
        },
        {
          "append": {
            "key": "dock",
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
      ],
      "text": "Day {day} begins. The deck is shuffled, every ship is emptied (tracks keep their values) and the Dock is laid out: {dock}."
    },
    {
      "use": "update",
      "phase": "round",
      "label": "the round begins",
      "do": [
        {
          "set": {
            "key": "active_seat",
            "value": {
              "calc": "((day - 1) + (round_in_day - 1)) % 3 + 1"
            }
          }
        },
        {
          "set": {
            "key": "high_bid",
            "value": 0
          }
        },
        {
          "set": {
            "key": "high_bidder",
            "value": 0
          }
        },
        {
          "set": {
            "key": "lot",
            "value": []
          }
        },
        {
          "set": {
            "key": "lot_size",
            "value": 0
          }
        },
        {
          "set": {
            "key": "lot_value",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "round",
      "label": "the state of play",
      "to": "all",
      "text": "Day {day}, round {round_in_day} of {rounds_per_day}. Active seat: {active_seat}. Dock (first, second, third): {dock}.\nSeat 1 (A): ship {players[0].ship} value {players[0].ship_value}; Spice {players[0].track_spice}, Silk {players[0].track_silk}, Grain {players[0].track_grain}; florins {players[0].florins}.\nSeat 2 (B): ship {players[1].ship} value {players[1].ship_value}; Spice {players[1].track_spice}, Silk {players[1].track_silk}, Grain {players[1].track_grain}; florins {players[1].florins}.\nSeat 3 (C): ship {players[2].ship} value {players[2].ship_value}; Spice {players[2].track_spice}, Silk {players[2].track_silk}, Grain {players[2].track_grain}; florins {players[2].florins}."
    },
    {
      "use": "ask",
      "phase": "lot",
      "label": "choose the lot",
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "min_lot_size"
        },
        "max": {
          "calc": "min(max_lot_size, len(dock))"
        }
      },
      "verify": {
        "bind": "lot_n"
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "lot_size",
              "value": "$answer"
            }
          },
          {
            "set": {
              "key": "lot",
              "value": {
                "calc": "[dock[0]] + ([dock[1]] if $answer >= 2 else []) + ([dock[2]] if $answer >= 3 else [])"
              }
            }
          },
          {
            "set": {
              "key": "lot_value",
              "value": {
                "calc": "sum([int(c[len(c) - 1]) for c in lot])"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} puts up a lot of the first {value} Dock card(s)."
      },
      "text": "You are the active player. Dock (first, second, third): {dock}. Choose the lot size: a whole number from {min_lot_size} up to {max_lot_size}, and no more than the cards in the Dock. The lot is the first that many Dock cards."
    },
    {
      "use": "ask",
      "phase": "auction",
      "label": "first bidder",
      "to": {
        "where": "you.seat == active_seat % 3 + 1 and you.ship_count + lot_size <= ship_capacity and you.florins > high_bid"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "max(min_bid, high_bid + 1)"
        },
        "max": {
          "calc": "you.florins"
        },
        "or": [
          "pass",
          "0"
        ]
      },
      "verify": {
        "bind": "bid1"
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "high_bid",
              "value": "$answer",
              "if": {
                "calc": "$answer != 'pass' and $answer != '0' and $answer != 0"
              }
            }
          },
          {
            "set": {
              "key": "high_bidder",
              "value": "$seat",
              "if": {
                "calc": "$answer != 'pass' and $answer != '0' and $answer != 0"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} bids: {value}."
      },
      "text": "Auction for the lot {lot} (size {lot_size}, value {lot_value}). High bid so far: {high_bid} (seat {high_bidder}, 0 = nobody). Bid a whole number at least {min_bid}, higher than the high bid and no more than your florins, or answer pass (0)."
    },
    {
      "use": "ask",
      "phase": "auction",
      "label": "second bidder",
      "to": {
        "where": "you.seat == (active_seat + 1) % 3 + 1 and you.ship_count + lot_size <= ship_capacity and you.florins > high_bid"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "max(min_bid, high_bid + 1)"
        },
        "max": {
          "calc": "you.florins"
        },
        "or": [
          "pass",
          "0"
        ]
      },
      "verify": {
        "bind": "bid2"
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "high_bid",
              "value": "$answer",
              "if": {
                "calc": "$answer != 'pass' and $answer != '0' and $answer != 0"
              }
            }
          },
          {
            "set": {
              "key": "high_bidder",
              "value": "$seat",
              "if": {
                "calc": "$answer != 'pass' and $answer != '0' and $answer != 0"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} bids: {value}."
      },
      "text": "Auction for the lot {lot} (size {lot_size}, value {lot_value}). High bid so far: {high_bid} (seat {high_bidder}, 0 = nobody). Bid a whole number at least {min_bid}, higher than the high bid and no more than your florins, or answer pass (0)."
    },
    {
      "use": "ask",
      "phase": "auction",
      "label": "active bidder",
      "to": {
        "where": "you.seat == active_seat and you.ship_count + lot_size <= ship_capacity and you.florins > high_bid"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "max(min_bid, high_bid + 1)"
        },
        "max": {
          "calc": "you.florins"
        },
        "or": [
          "pass",
          "0"
        ]
      },
      "verify": {
        "bind": "bid3"
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "high_bid",
              "value": "$answer",
              "if": {
                "calc": "$answer != 'pass' and $answer != '0' and $answer != 0"
              }
            }
          },
          {
            "set": {
              "key": "high_bidder",
              "value": "$seat",
              "if": {
                "calc": "$answer != 'pass' and $answer != '0' and $answer != 0"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} bids: {value}."
      },
      "text": "You bid last. Lot {lot} (size {lot_size}, value {lot_value}). High bid so far: {high_bid} (seat {high_bidder}, 0 = nobody). Bid a whole number at least {min_bid}, higher than the high bid and no more than your florins, or answer pass (0)."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "load the lot",
      "do": [
        {
          "adjust": {
            "players": {
              "where": "you.seat == high_bidder and you.florins >= high_bid"
            },
            "key": "florins",
            "value": {
              "calc": "-high_bid"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == high_bidder"
            },
            "key": "ship",
            "value": {
              "calc": "you.ship + lot"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat == high_bidder"
            },
            "key": "ship_count",
            "value": {
              "calc": "lot_size"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat == high_bidder"
            },
            "key": "ship_value",
            "value": {
              "calc": "lot_value"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == high_bidder"
            },
            "key": "track_spice",
            "value": {
              "calc": "min(track_max, you.track_spice + count(c[1] == 'p' for c in lot))"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == high_bidder"
            },
            "key": "track_silk",
            "value": {
              "calc": "min(track_max, you.track_silk + count(c[1] == 'i' for c in lot))"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == high_bidder"
            },
            "key": "track_grain",
            "value": {
              "calc": "min(track_max, you.track_grain + count(c[0] == 'G' for c in lot))"
            }
          }
        },
        {
          "set": {
            "key": "dock",
            "value": {
              "calc": "([dock[1]] if lot_size < 2 and len(dock) > 1 else []) + ([dock[2]] if lot_size < 3 and len(dock) > 2 else [])"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "refill the dock",
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"
            },
            "if": {
              "calc": "len(dock) < dock_size and len(deck) > 0"
            }
          }
        },
        {
          "append": {
            "key": "dock",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(dock) < dock_size and len(deck) > 0"
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
              "calc": "len(dock) <= dock_size and len(deck) > 0 and pick in deck"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"
            },
            "if": {
              "calc": "len(dock) < dock_size and len(deck) > 0"
            }
          }
        },
        {
          "append": {
            "key": "dock",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(dock) < dock_size and len(deck) > 0"
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
              "calc": "len(dock) <= dock_size and len(deck) > 0 and pick in deck"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"
            },
            "if": {
              "calc": "len(dock) < dock_size and len(deck) > 0"
            }
          }
        },
        {
          "append": {
            "key": "dock",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(dock) < dock_size and len(deck) > 0"
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
              "calc": "len(dock) <= dock_size and len(deck) > 0 and pick in deck"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": ""
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "resolve",
      "label": "the lot is sold",
      "when": {
        "calc": "high_bidder > 0"
      },
      "to": "all",
      "text": "Seat {high_bidder} wins the lot {lot} for {high_bid} florins and loads it aboard. Dock now: {dock}."
    },
    {
      "use": "tell",
      "phase": "resolve",
      "label": "the lot is discarded",
      "when": {
        "calc": "high_bidder == 0"
      },
      "to": "all",
      "text": "Everyone passed. The lot {lot} is discarded. Dock now: {dock}."
    },
    {
      "use": "update",
      "phase": "dusk",
      "label": "ship scoring",
      "when": {
        "calc": "round_in_day == rounds_per_day"
      },
      "do": [
        {
          "adjust": {
            "players": {
              "where": "you.ship_count > 0"
            },
            "key": "florins",
            "value": {
              "calc": "int(((ship_prize_first if count(p.ship_count > 0 and p.ship_value > you.ship_value for p in players) == 0 else 0) + (ship_prize_second if count(p.ship_count > 0 and p.ship_value > you.ship_value for p in players) <= 1 and count(p.ship_count > 0 and p.ship_value > you.ship_value for p in players) + count(p.ship_count > 0 and p.ship_value == you.ship_value for p in players) >= 2 else 0)) / count(p.ship_count > 0 and p.ship_value == you.ship_value for p in players))"
            },
            "text": "Seat {player} is scored for ship value."
          }
        }
      ],
      "text": "End of day {day}: ship scoring ({ship_prize_first} for the highest ship value, {ship_prize_second} for the second; empty ships score nothing)."
    },
    {
      "use": "update",
      "phase": "dusk",
      "label": "commodity majorities",
      "when": {
        "calc": "round_in_day == rounds_per_day"
      },
      "do": [
        {
          "adjust": {
            "players": {
              "where": "you.track_spice > 0"
            },
            "key": "florins",
            "value": {
              "calc": "int(((majority_prize_first if count(p.track_spice > you.track_spice for p in players) == 0 else 0) + (majority_prize_second if count(p.track_spice > you.track_spice for p in players) <= 1 and count(p.track_spice > you.track_spice for p in players) + count(p.track_spice == you.track_spice for p in players) >= 2 else 0)) / count(p.track_spice == you.track_spice for p in players)) * (1 + (patron_multiplier_extra if you.patron == 'Spice' else 0))"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.track_silk > 0"
            },
            "key": "florins",
            "value": {
              "calc": "int(((majority_prize_first if count(p.track_silk > you.track_silk for p in players) == 0 else 0) + (majority_prize_second if count(p.track_silk > you.track_silk for p in players) <= 1 and count(p.track_silk > you.track_silk for p in players) + count(p.track_silk == you.track_silk for p in players) >= 2 else 0)) / count(p.track_silk == you.track_silk for p in players)) * (1 + (patron_multiplier_extra if you.patron == 'Silk' else 0))"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.track_grain > 0"
            },
            "key": "florins",
            "value": {
              "calc": "int(((majority_prize_first if count(p.track_grain > you.track_grain for p in players) == 0 else 0) + (majority_prize_second if count(p.track_grain > you.track_grain for p in players) <= 1 and count(p.track_grain > you.track_grain for p in players) + count(p.track_grain == you.track_grain for p in players) >= 2 else 0)) / count(p.track_grain == you.track_grain for p in players)) * (1 + (patron_multiplier_extra if you.patron == 'Grain' else 0))"
            }
          }
        }
      ],
      "text": "Commodity majorities are scored ({majority_prize_first} for the highest track, {majority_prize_second} for the second, doubled in your own Patron commodity). Florins: seat 1 {players[0].florins}, seat 2 {players[1].florins}, seat 3 {players[2].florins}."
    },
    {
      "use": "update",
      "phase": "dusk",
      "label": "advance the clock",
      "do": [
        {
          "adjust": {
            "key": "round_in_day",
            "value": 1
          }
        },
        {
          "set": {
            "key": "day",
            "value": {
              "calc": "day + 1 if round_in_day > rounds_per_day else day"
            }
          }
        },
        {
          "set": {
            "key": "round_in_day",
            "value": {
              "calc": "1 if round_in_day > rounds_per_day else round_in_day"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "dusk",
      "label": "the patrons revealed",
      "when": {
        "calc": "day > days"
      },
      "do": [
        {
          "disclose": {
            "of": 1,
            "attribute": "patron",
            "to": "all",
            "text": "Seat {subject}'s Patron was {value}."
          }
        },
        {
          "disclose": {
            "of": 2,
            "attribute": "patron",
            "to": "all",
            "text": "Seat {subject}'s Patron was {value}."
          }
        },
        {
          "disclose": {
            "of": 3,
            "attribute": "patron",
            "to": "all",
            "text": "Seat {subject}'s Patron was {value}."
          }
        }
      ],
      "text": "The game is over. Final florins: seat 1 {players[0].florins}, seat 2 {players[1].florins}, seat 3 {players[2].florins}."
    },
    {
      "use": "check",
      "phase": "dusk",
      "label": "after the last day",
      "when": {
        "calc": "day > days"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "day > days"
      },
      "rank_by": "you.florins",
      "reveal": [
        "patron"
      ],
      "text": "Winner: {result}. Final florins: Seat 1 (A) {players[0].florins}, Seat 2 (B) {players[1].florins}, Seat 3 (C) {players[2].florins}."
    }
  },
  "limits": {
    "rounds": 27,
    "rounds_max": 27,
    "actions_max": 1000,
    "deadline_s": 120
  },
  "rules": "Three merchants sit in fixed order A (seat 1), B (seat 2), C (seat 3). Each starts with {starting_florins} florins (public), a ship with room for {ship_capacity} cards, and three public commodity tracks (Spice, Silk, Grain) at {track_start}. The three commodities are shuffled and one is dealt secretly to each player as their Patron: every player has a different Patron and knows only their own. The deck has {deck_size} cards: for each of Spice, Silk and Grain there are {cards_per_commodity} cards valued 0, 1, 1, 2, 2, 3, 3, 4, 4, 5.\n\nSTART OF EACH DAY. There are {days} days. All {deck_size} cards are shuffled into a face-down deck and every ship is emptied (tracks are NOT reset). The top {dock_size} cards are turned face up in a row: the Dock, ordered first, second, third. The first active player is A on day 1, B on day 2 and C on day 3; the active role then passes in seat order A, B, C, A... each round. Each day has exactly {rounds_per_day} rounds.\n\nEACH ROUND. (1) The Dock, all ships, tracks and florins are announced. (2) The active player chooses a lot size of {min_lot_size} to {max_lot_size} (no more than the cards in the Dock). The lot is the first that many Dock cards; its size is its card count and its value is the sum of its card values. (3) Auction, once around: the next player in seat order after the active player bids first, then the other non-active player, then the active player last. Each bidder either passes (answer pass or 0) or bids a whole number that is at least {min_bid}, higher than the current highest bid, and no more than their florins. A player whose ship lacks room for the whole lot, or whose florins do not exceed the high bid, must pass and is not asked. (4) If anyone bid, the highest bidder pays that many florins to the bank and loads every card of the lot onto their ship; for each card loaded, that player's track in the card's commodity rises by 1, to a maximum of {track_max}. If everyone passed, the lot is discarded and no florins, ships or tracks change. (5) The lot's cards leave the Dock, the remaining Dock cards slide forward in order, and the Dock is refilled to {dock_size} cards from the top of the deck (fewer if the deck runs out).\n\nEND OF DAY (after round {rounds_per_day}). (a) Ship scoring: players are ranked by total value of the cards on their ship. The highest gets {ship_prize_first} florins and the second gets {ship_prize_second}. Tied players add the prizes for the places they occupy and split them equally, rounded down. A player with an empty ship gets nothing. (b) Commodity majorities: for each commodity, the player with the highest track gets {majority_prize_first} florins and the second highest gets {majority_prize_second}. Ties split as above. A track at 0 earns nothing. (c) Patron: a player who earned a majority award in step (b) in their own Patron commodity receives that same amount again; in any other commodity there is no bonus. All awards are added to florins.\n\nEND OF GAME. After day {days} scoring, Patrons are revealed and the player with the most florins wins. Players tied for the most share the win (a draw)."
}
```
````
