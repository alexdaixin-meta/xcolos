# Task: write the XColos game file for "Medici: Sealed Lots"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 6; set `meta.players` to {"min": 3, "max": 6, "suggested": 4} (the suggested size is the one the game plays best at).

GOODS AND CARDS
There are four goods: Grain, Cloth, Spice and Dye. The deck has 48 cards. For each good there is one card of each of these values: 0, 1, 1, 2, 2, 3, 3, 3, 4, 4, 5, 5. That is 12 cards per good, worth 33 in total per good.

SETUP
N is the number of players (3 to 6). Each player starts with:
- 40 florins. Florins are PUBLIC: every player's florins are announced at the start and after every change.
- ship_value 0 and ship_count 0.
- grain_count, cloth_count, spice_count and dye_count all 0.
- bid 0.
Favour deal: if N is 3 or 4, take one tile each of Grain, Cloth, Spice and Dye (4 tiles). If N is 5 or 6, take two tiles of each good (8 tiles). Deal each player one tile at random, face down. This is their secret favoured_good, known only to them. Undealt tiles are set aside and never revealed.
Set round = 0. The game lasts 6N rounds: 3 days of 2N rounds each. The game-level values are round, active_seat, lot_size, lot_value, deck, high_bid, high_count, top, second and track_max.

EACH ROUND, IN THIS ORDER
1. ADVANCE: round = round + 1. Then active_seat = ((round - 1) mod N) + 1.
2. NEW DAY (only when round mod 2N = 1): set the deck to the full 48-card list and shuffle it once. Any cards left from the previous day are gone. Set every player's ship_value and ship_count to 0. Florins and the four goods counts are kept.
3. REVEAL: announce the top 3 cards of the deck (positions 1, 2, 3) to everyone.
4. LOT SIZE (choice): the active seat chooses 1, 2 or 3.
5. CUT: lot_size = that choice. The lot is deck positions 1 to lot_size. lot_value = the sum of those cards' values. Announce lot_size and lot_value.
6. BID (simultaneous choice): every player whose ship_count + lot_size > 5 is told their ship cannot fit this lot and only a bid of 0 counts. Then all players, at the same moment, choose a whole-number bid from 0 to their florins.
7. VALIDATE: a bid becomes 0 if it exceeds the player's florins or if ship_count + lot_size > 5.
8. RESOLVE: high_bid = the largest bid. high_count = the number of players whose bid equals high_bid. Announce every bid.
9. PAY (only if high_bid > 0 and high_count = 1): the sole high bidder loses high_bid florins, which leave the game. Announce their florins.
10. LOAD AND CLEAR: if high_bid > 0 and high_count = 1, the winner adds lot_value to ship_value and lot_size to ship_count, and adds 1 to their count of each lot card's good. Then, in every case, remove the top 3 cards from the deck. If nobody won, the lot is simply discarded.
11. SHIP RANKS (only when round mod 2N = 0): top = the highest ship_value. second = the highest ship_value strictly below top, or 0 if there is none.
12. SHIP PAYOUT (same condition): if top > 0, every player with ship_value = top gains 20 florins. If second > 0, every player with ship_value = second gains 10 florins. Announce florins.
13. GRAIN TRACK (same condition): track_max = the highest grain_count. If track_max > 0, every player with grain_count = track_max gains 6 florins.
14. CLOTH TRACK (same condition): the same, for cloth_count.
15. SPICE TRACK (same condition): the same, for spice_count.
16. DYE TRACK (same condition): the same, for dye_count. Announce florins.
17. FAVOUR (only when round = 6N): each player gains 3 florins times their count of their own favoured_good. All favoured goods are revealed and final florins announced.
18. END: if round = 6N, the game ends.

There is no talk phase.

How the winner is decided: After round 6N, the player with the most florins wins. If two or more players tie for the most florins, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Medici: Sealed Lots (3 to 6 players, best with 4)

Players bid sealed florins for lots of goods cards to fill their ships. Ships pay out at the end of each of 3 days, goods tracks pay bonuses, and a secret favoured good pays at the end. The most florins wins.

STATE (every item below must exist in the file):
  - each player: florins (number, starts 40); everyone sees it. Money and score. It is announced at the start and after every change.
  - each player: ship_value (number, starts 0); everyone sees it. Sum of the card values loaded on the ship today. It is reset each new day.
  - each player: ship_count (number, starts 0); everyone sees it. Number of cards loaded on the ship today, at most 5. It is reset each new day.
  - each player: grain_count (number, starts 0); everyone sees it. Grain cards won over the whole game.
  - each player: cloth_count (number, starts 0); everyone sees it. Cloth cards won over the whole game.
  - each player: spice_count (number, starts 0); everyone sees it. Spice cards won over the whole game.
  - each player: dye_count (number, starts 0); everyone sees it. Dye cards won over the whole game.
  - each player: bid (number, starts 0); everyone sees it. This round's sealed bid. It is gathered by a simultaneous poll and announced at resolve.
  - each player: favoured_good (text, starts ''); only its owner sees it. Secret favour tile (Grain, Cloth, Spice or Dye), known only to its owner. It is revealed at the end of the game.
  - the table: round (number, starts 0); everyone sees it. Round counter, from 1 to 6N.
  - the table: active_seat (number, starts 0); everyone sees it. Seat that chooses the lot size this round: ((round-1) mod N)+1.
  - the table: deck (list, starts []); hidden from all players. Today's ordered deck of cards, each coded good:value (for example Spice:3). Position 1 is the top.
  - the table: revealed (list, starts []); everyone sees it. The top 3 deck cards shown this round.
  - the table: lot_size (number, starts 0); everyone sees it. Number of cards in this round's lot (1 to 3).
  - the table: lot_value (number, starts 0); everyone sees it. Sum of the values of the lot cards.
  - the table: high_bid (number, starts 0); everyone sees it. Largest valid bid this round.
  - the table: high_count (number, starts 0); everyone sees it. Number of players whose bid equals high_bid.
  - the table: top (number, starts 0); everyone sees it. Highest ship_value at the end of the day.
  - the table: second (number, starts 0); everyone sees it. Highest ship_value strictly below top, or 0 if there is none.
  - the table: track_max (number, starts 0); everyone sees it. Highest count on the goods track being scored.
  - the table: favour_tiles (list, starts []); hidden from all players. Favour tiles to deal from. Undealt tiles stay here and are never revealed.
  - parameters, each kept as a table attribute: starting_florins = 40, deck_size = 48, goods = 4, cards_per_good = 12, cards_of_value_0_per_good = 1, cards_of_value_1_per_good = 2, cards_of_value_2_per_good = 2, cards_of_value_3_per_good = 3, cards_of_value_4_per_good = 2, cards_of_value_5_per_good = 2, value_per_good_total = 33, reveal_count = 3, lot_size_min = 1, lot_size_max = 3, cards_cleared_per_round = 3, ship_capacity = 5, days = 3, rounds_per_day_per_player = 2, total_rounds_per_player = 6, ship_first_payout = 20, ship_second_payout = 10, track_bonus = 6, favour_multiplier = 3, favour_tiles_per_good_small = 1, favour_tiles_per_good_large = 2, small_table_max = 4, bid_min = 0

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Every player starts with florins 40, ship_value 0, ship_count 0, grain_count 0, cloth_count 0, spice_count 0, dye_count 0 and bid 0.
  2. favour_tiles is set to one tile each of Grain, Cloth, Spice and Dye if N is 3 or 4, or to two tiles of each good (8 tiles) if N is 5 or 6.
  3. Each player draws one tile at random from favour_tiles into favoured_good, visible only to that player. The remaining tiles stay hidden in favour_tiles.
  4. round is set to 0. The game lasts 6N rounds: 3 days of 2N rounds each.
  5. Every player's florins are announced.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round = round + 1; active_seat = ((round - 1) mod N) + 1.
  2. [update] all players. What happens: When round mod 2N = 1: deck is rebuilt as the full 48-card list (for each of Grain, Cloth, Spice and Dye, the values 0,1,1,2,2,3,3,3,4,4,5,5) and placed in random order by drawing every card at random. Any old cards are discarded. Every player's ship_value = 0 and ship_count = 0. Florins and goods counts are kept.
  3. [update] all players. What happens: revealed = deck positions 1, 2 and 3. These are announced to everyone.
  4. [ask] the player at active_seat answers: a choice of 1, 2 or 3. What happens: Records the lot size choice.
  5. [update] all players. What happens: lot_size = the choice; lot_value = the sum of the values of deck positions 1..lot_size. lot_size and lot_value are announced.
  6. [tell] every player with ship_count + lot_size > 5. What happens: Tells each such player that their ship cannot fit this lot and only a bid of 0 counts.
  7. [poll] all players answers: a whole number from 0 to the player's florins. What happens: bid = the answer. All players answer simultaneously, and no one sees a bid until all are in.
  8. [update] all players. What happens: For each player: if bid > florins or ship_count + lot_size > 5, then bid = 0.
  9. [update] all players. What happens: high_bid = the maximum bid; high_count = the number of players with bid = high_bid. Every bid is announced.
  10. [update] the sole high bidder. What happens: When high_bid > 0 and high_count = 1: the player with bid = high_bid has florins = florins - high_bid (these florins leave the game), and their florins are announced.
  11. [update] all players. What happens: When high_bid > 0 and high_count = 1: the winner's ship_value += lot_value and ship_count += lot_size, and the winner gains +1 grain_count, cloth_count, spice_count or dye_count for each lot card of that good. In every case, the top 3 cards are removed from deck (an unwon lot is simply discarded).
  12. [update] all players. What happens: When round mod 2N = 0: top = the maximum ship_value; second = the maximum ship_value strictly below top, or 0 if there is none.
  13. [update] all players. What happens: When round mod 2N = 0: if top > 0, every player with ship_value = top gains 20 florins; if second > 0, every player with ship_value = second gains 10 florins. Florins are announced.
  14. [update] all players. What happens: When round mod 2N = 0: track_max = the maximum grain_count; if track_max > 0, every player with grain_count = track_max gains 6 florins.
  15. [update] all players. What happens: When round mod 2N = 0: track_max = the maximum cloth_count; if track_max > 0, every player with cloth_count = track_max gains 6 florins.
  16. [update] all players. What happens: When round mod 2N = 0: track_max = the maximum spice_count; if track_max > 0, every player with spice_count = track_max gains 6 florins.
  17. [update] all players. What happens: When round mod 2N = 0: track_max = the maximum dye_count; if track_max > 0, every player with dye_count = track_max gains 6 florins. Florins are announced.
  18. [update] all players. What happens: When round = 6N: each player gains florins += 3 × (their count of their favoured_good). Every favoured_good is revealed to all, and final florins are announced.
  19. [check] all players. What happens: The game ends if round = 6N; otherwise play continues.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, then every player has 40 florins, ship_value 0, ship_count 0 and all four goods counts 0.
  R2. When N is 3 or 4, then the favour tiles are 1 of each good (4 tiles); when N is 5 or 6, then they are 2 of each good (8 tiles). Each player is dealt exactly 1 tile, seen only by that player.
  R3. When a round begins, then round increases by 1 and active_seat = ((round - 1) mod N) + 1.
  R4. When round mod 2N = 1, then the deck is reset to the full 48 cards (12 per good, values 0,1,1,2,2,3,3,3,4,4,5,5) in random order, and every ship_value and ship_count is set to 0, while florins and goods counts are kept.
  R5. When a round's reveal happens, then the top 3 deck cards are shown to everyone.
  R6. When the active seat chooses a lot size, then it is 1, 2 or 3, and lot_value equals the sum of the values of the top lot_size cards.
  R7. When bids are made, then all players bid simultaneously with a whole number from 0 to their florins.
  R8. When a player's ship_count + lot_size > 5, then they are told that only 0 counts, and their bid is set to 0.
  R9. When a bid exceeds the bidder's florins, then it becomes 0.
  R10. When high_bid > 0 and exactly one player bid high_bid, then that player loses high_bid florins, adds lot_value to ship_value and lot_size to ship_count, and gains 1 in the matching goods count per lot card.
  R11. When high_bid = 0, or two or more players tie at high_bid, then nobody pays and the lot is discarded.
  R12. When any round ends its load step, then the top 3 cards are removed from the deck regardless of lot size.
  R13. When round mod 2N = 0 and top > 0, then every player with ship_value = top gains 20 florins.
  R14. When round mod 2N = 0 and second > 0, then every player with ship_value = second (the highest value strictly below top) gains 10 florins.
  R15. When round mod 2N = 0, then for each of grain, cloth, spice and dye, if the highest count is > 0, every player with that highest count gains 6 florins.
  R16. When round = 6N, then each player gains 3 florins per card of their favoured_good, and all favoured goods are revealed.
  R17. When round = 6N, then the game ends and the player with the most florins wins, with players tied for the most sharing the result (a draw).

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Lot size | asked: the player at active_seat only | options: 1, 2 or 3
  - Sealed bid | asked: all players | options: Any whole number from 0 to the player's current florins. A player whose ship_count + lot_size > 5 is offered the same range but is told that only a bid of 0 counts.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round = 6 * N
  - each player's standing: you.florins (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their florins after round 6N. The most florins wins. Players tied for the most florins share the result, which stands for the source's draw.
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

- each player: `florins` (number, visible: public, starts 40): Money and score. It is announced at the start and after every change.
- each player: `ship_value` (number, visible: public, starts 0): Sum of the card values loaded on the ship today. It is reset each new day.
- the table: `round` (number, visible: public, starts 0): Round counter, from 1 to 6N.
- parameters (each must be an attribute holding this value, never a number buried in a step): starting_florins = 40, deck_size = 48, goods = 4, cards_per_good = 12, cards_of_value_0_per_good = 1, cards_of_value_1_per_good = 2, cards_of_value_2_per_good = 2, cards_of_value_3_per_good = 3, cards_of_value_4_per_good = 2, cards_of_value_5_per_good = 2, value_per_good_total = 33, reveal_count = 3, lot_size_min = 1, lot_size_max = 3, cards_cleared_per_round = 3, ship_capacity = 5, days = 3, rounds_per_day_per_player = 2, total_rounds_per_player = 6, ship_first_payout = 20, ship_second_payout = 10, track_bonus = 6, favour_multiplier = 3, favour_tiles_per_good_small = 1, favour_tiles_per_good_large = 2, small_table_max = 4, bid_min = 0
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

## Guidance from the last attempt

The previous attempt had problems:

1. Advance step: increment `round` exactly once per round, then immediately set `active_seat = ((round - 1) mod N) + 1`, before the new-day, reveal and lot-size steps. In round 1 with 3 players the active seat must be 1. Remove the duplicate increment that leaves `round` at 2 after one round.
2. Lot size: put the lot-size choice (options `lot_size_min`..`lot_size_max`, i.e. 1, 2, 3) to the player whose seat equals `active_seat`, not to any other seat.
3. Cut: compute `lot_value` as the sum of deck positions 1..`lot_size` after the choice.
4. Bids: make bidding a simultaneous poll of all players. Each player's options are whole numbers from `bid_min` (0) to their current `florins` (seat 1 with 40 florins must be offered 0 through 40). Then zero out a bid if it exceeds florins or if `ship_count + lot_size > ship_capacity`.
5. Resolve, pay and load: compute `high_bid` and `high_count`. If `high_bid > 0` and `high_count = 1`, deduct `high_bid` from the winner's florins. Add `lot_value` to their `ship_value`, add `lot_size` to their `ship_count`, and add 1 to their goods count for each lot card's good. Then remove `cards_cleared_per_round` (3) cards from the deck in every case.
6. Day end: keep the ship payout, track and favour steps gated on `round mod 2N = 0` and `round = 6N`, with N derived from the player count.
