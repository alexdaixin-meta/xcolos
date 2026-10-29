# 32 coder

- time: 2026-10-27T17:21:24+00:00 (100.5s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 fe9798403eadd0b2, reply sha256 79721a7d3bf8dad0

## Sent

````
# Task: write the XColos game file for "Medici: Sealed Ledgers (revised)"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 6; set `meta.players` to {"min": 3, "max": 6, "suggested": 4} (the suggested size is the one the game plays best at).

SETUP. There are N players (3-6) in seats 1..N. Each player starts with 40 florins, known only to that player, and an empty ship that holds at most 5 cards. Each player has cumulative counts of 0 for each of the four goods: Grain, Cloth, Spice and Dye. Before round 1, each player is dealt a secret FAVOURED GOOD from a favour pool. With 3 or 4 players the pool is the 4 goods once each. With 5 or 6 players the pool is the 4 goods twice each (8 tiles). The pool is shuffled once and one tile is dealt to each player. Favoured goods stay secret until the end.

DECK. The deck has 48 cards: 12 per good. Each good has the values 0,1,1,2,2,3,3,3,4,4,5,5, which sum to 33. All four goods are identical in value.

LENGTH. A day lasts 2N rounds. The game lasts 6N rounds: 18 with 3 players, 24 with 4, 30 with 5 and 36 with 6. The active seat in a round is ((round-1) mod N)+1, so each seat is active exactly twice per day. A day uses at most 6N of the 48 cards, so the deck never runs out.

EACH ROUND, in this order:
1. DAY START, DECK (only when round mod 2N = 1): rebuild the deck as all 48 cards and shuffle it once. This shuffle is the only random event in the game after setup.
2. DAY START, SHIPS (same condition): every player's ship value, ship count and ship favoured count become 0. Cumulative good counts and florins are kept.
3. REVEAL: take the top 3 cards of the deck, in order, and show them to everyone as revealed cards 1, 2 and 3.
4. LOT SIZE: the active seat alone chooses 1, 2 or 3.
5. LOT: the lot is the first that many revealed cards. Any other revealed cards are discarded for the rest of the day. Announce the lot.
6. BIDS: every player, the active seat included, secretly writes a whole-number bid from 0 to their current florins, all at the same moment. A bid of 0 is a pass.
7. VOID: a player's bid becomes 0 if their ship count plus the lot size would exceed 5.
8. HIGH BID: record the highest bid and how many players made it.
9. PAY: if the highest bid is above 0 and exactly one player made it, that player pays their bid to the bank, and those florins leave the game. Otherwise, meaning all bids are 0 or two or more players tie for the highest, the lot is discarded and nobody pays.
10. LOAD: if a sale happened, the winner adds the lot's card values to their ship value and the lot size to their ship count. They add 1 to their ship favoured count for each lot card of their favoured good, and 1 to their cumulative count of each good for each lot card of that good.
11. ANNOUNCE: show the lot, every bid, and the winner and price, or 'no sale'.
12. DAY END, TOP (only when round mod 2N = 0): find the highest ship value.
13. Every player whose ship value equals it, if it is above 0, gains 10 florins.
14. Find the highest ship value strictly below that top value, or 0 if there is none.
15. Every player whose ship value equals this second value, if it is above 0, gains 5 florins.
16. MAJORITIES: for each of the four goods, find the highest cumulative count among all players.
17. For each good, every player whose cumulative count equals that highest count, if it is at least 1, gains 4 florins.
18. FAVOURED: each player gains 3 florins per card of their favoured good on their ship (their ship favoured count).
19. GAME END: if round = 6N, the game ends. Otherwise the next round begins.

No talk phase. Each player sees only their own florins and favoured good. Lots, all bids, prices, ships and cumulative counts are public.

How the winner is decided: After round 6N, the player with the most florins wins. If two or more players tie for the most florins, they share a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Medici: Sealed Ledgers (revised) (3 to 6 players, best with 4)

Players take turns as the active seat and set the size of a lot of 1 to 3 revealed goods cards. Everyone then makes a sealed bid for the lot. Each day pays florins for the most valuable ships, for majorities in each good and for a secret favoured good. Most florins after 6N rounds wins.

STATE (every item below must exist in the file):
  - each player: florins (number, starts 40); only its owner sees it. The player's money and score. Only the owner sees it until the end.
  - each player: favoured_good (text, starts ''); only its owner sees it. The secret favoured good (Grain, Cloth, Spice or Dye), dealt from favour_pool before round 1.
  - each player: ship_cards (list, starts []); everyone sees it. Cards loaded on the ship today, each written as Good-Value, for example Spice-3.
  - each player: ship_value (number, starts 0); everyone sees it. Sum of the card values on the ship today.
  - each player: ship_count (number, starts 0); everyone sees it. Number of cards on the ship today, at most 5.
  - each player: ship_favoured (number, starts 0); only its owner sees it. Number of cards of the player's favoured good on the ship today. It is kept private because it would reveal the favoured good.
  - each player: grain_count (number, starts 0); everyone sees it. Cumulative Grain cards won over the whole game.
  - each player: cloth_count (number, starts 0); everyone sees it. Cumulative Cloth cards won over the whole game.
  - each player: spice_count (number, starts 0); everyone sees it. Cumulative Spice cards won over the whole game.
  - each player: dye_count (number, starts 0); everyone sees it. Cumulative Dye cards won over the whole game.
  - each player: bid (number, starts 0); everyone sees it. This round's sealed bid after voiding. It is gathered by poll and announced afterwards.
  - the table: round (number, starts 0); everyone sees it. Current round number, from 1 to 6N.
  - the table: active_seat (number, starts 1); everyone sees it. ((round-1) mod N)+1.
  - the table: favour_pool (list, starts []); hidden from all players. Favour tiles: the 4 goods once each for N of 3 or 4, twice each for N of 5 or 6.
  - the table: deck (list, starts []); hidden from all players. The 48 cards, 12 per good with values 0,1,1,2,2,3,3,3,4,4,5,5, rebuilt and shuffled at each day start.
  - the table: revealed (list, starts []); everyone sees it. The 3 cards revealed this round, in order.
  - the table: lot (list, starts []); everyone sees it. The first lot_size revealed cards.
  - the table: lot_size (number, starts 0); everyone sees it. 1, 2 or 3, chosen by the active seat.
  - the table: discard (list, starts []); hidden from all players. Cards discarded for the rest of the day: unused revealed cards and unsold lots.
  - the table: high_bid (number, starts 0); everyone sees it. Highest valid bid this round.
  - the table: high_count (number, starts 0); everyone sees it. Number of players who made high_bid.
  - the table: winner_seat (number, starts 0); everyone sees it. Seat that bought the lot this round, or 0 for no sale.
  - the table: top_value (number, starts 0); everyone sees it. Highest ship value at day end.
  - the table: second_value (number, starts 0); everyone sees it. Highest ship value strictly below top_value at day end, or 0 if there is none.
  - the table: grain_max (number, starts 0); everyone sees it. Highest cumulative Grain count at day end.
  - the table: cloth_max (number, starts 0); everyone sees it. Highest cumulative Cloth count at day end.
  - the table: spice_max (number, starts 0); everyone sees it. Highest cumulative Spice count at day end.
  - the table: dye_max (number, starts 0); everyone sees it. Highest cumulative Dye count at day end.
  - parameters, each kept as a table attribute: starting_florins = 40, ship_capacity = 5, goods_count = 4, deck_size = 48, cards_per_good = 12, value_0_cards_per_good = 1, value_1_cards_per_good = 2, value_2_cards_per_good = 2, value_3_cards_per_good = 3, value_4_cards_per_good = 2, value_5_cards_per_good = 2, value_sum_per_good = 33, favour_pool_copies_3_to_4_players = 1, favour_pool_copies_5_to_6_players = 2, rounds_per_day_per_player = 2, days = 3, rounds_per_game_per_player = 6, revealed_cards_per_round = 3, lot_size_min = 1, lot_size_max = 3, bid_min = 0, top_ship_bonus = 10, second_ship_bonus = 5, majority_bonus = 4, majority_min_count = 1, favoured_card_bonus = 3

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seat N players (3 to 6) in seats 1..N.
  2. Each player's florins are set to 40, visible only to that player.
  3. Each player's ship is set empty: ship_cards [], ship_value 0, ship_count 0, ship_favoured 0.
  4. Each player's grain_count, cloth_count, spice_count and dye_count are set to 0.
  5. favour_pool is built as Grain, Cloth, Spice and Dye once each if N is 3 or 4, or twice each (8 tiles) if N is 5 or 6.
  6. One tile is drawn at random from favour_pool into each player's favoured_good and removed from favour_pool.
  7. round is set to 0.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] the table. What happens: round += 1; active_seat = ((round-1) mod N)+1; winner_seat = 0; high_bid = 0; high_count = 0; every player's bid = 0.
  2. [update] the table. What happens: when round mod 2N = 1: deck is set to all 48 cards (Grain, Cloth, Spice and Dye, each with values 0,1,1,2,2,3,3,3,4,4,5,5); discard = []. Cards are drawn at random, so the deck is shuffled.
  3. [update] all players. What happens: when round mod 2N = 1: every player's ship_cards = [], ship_value = 0, ship_count = 0, ship_favoured = 0. Florins and cumulative good counts are kept.
  4. [update] the table. What happens: revealed = []; draw 3 cards at random from deck, in order, appending each to revealed and removing it from deck. Announce revealed cards 1, 2 and 3 to everyone.
  5. [ask] the active seat (seat active_seat) answers: a whole number 1 to 3. What happens: lot_size = the answer.
  6. [update] the table. What happens: lot = the first lot_size cards of revealed; the remaining revealed cards are appended to discard; revealed = []. Announce the lot.
  7. [sync] all players. What happens: Each player is sent their own florins, favoured_good and ship_favoured, plus the public state.
  8. [poll] all players answers: a whole number from 0 to your current florins (0 = pass). What happens: Each player's bid = the answer; nobody sees any bid until all are in.
  9. [update] all players. What happens: For each player: if ship_count + lot_size > 5 then bid = 0.
  10. [update] the table. What happens: high_bid = the maximum bid over all players; high_count = the number of players whose bid = high_bid.
  11. [update] the winning player. What happens: when high_bid > 0 and high_count = 1: winner_seat = the seat whose bid = high_bid; that player's florins -= bid (paid to the bank, leaving the game). Otherwise winner_seat = 0, the lot is appended to discard, and nobody pays.
  12. [update] the winning player. What happens: when winner_seat > 0: the lot cards are appended to the winner's ship_cards; ship_value += sum of the lot values; ship_count += lot_size; ship_favoured += the number of lot cards whose good = favoured_good; grain_count, cloth_count, spice_count and dye_count each += the number of lot cards of that good; lot = [].
  13. [tell] all players. What happens: Announce the lot, every player's bid, and winner_seat with price high_bid, or 'no sale'.
  14. [update] the table. What happens: when round mod 2N = 0: top_value = the maximum ship_value over all players; second_value = the maximum ship_value among players whose ship_value < top_value, or 0 if there is none.
  15. [update] all players. What happens: when round mod 2N = 0: each player with ship_value = top_value and top_value > 0 gains 10 florins; each player with ship_value = second_value and second_value > 0 gains 5 florins.
  16. [update] all players. What happens: when round mod 2N = 0: grain_max, cloth_max, spice_max and dye_max = the maximum of that cumulative count over all players; for each good, each player whose count = that max, when the max >= 1, gains 4 florins.
  17. [update] all players. What happens: when round mod 2N = 0: each player's florins += 3 * ship_favoured.
  18. [tell] all players. What happens: when round mod 2N = 0: announce the day-end ship values and cumulative good counts. Florins and favoured goods are not shown.
  19. [check] the table. What happens: If round = 6N the game ends; otherwise the next round begins.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, then each player has 40 florins visible only to themselves, an empty ship (ship_value 0, ship_count 0) and 0 of each cumulative good count.
  R2. When N is 3 or 4, then the favour pool is Grain, Cloth, Spice and Dye once each; when N is 5 or 6, then it is each good twice (8 tiles). Each player is dealt one tile at random as a secret favoured_good.
  R3. When the deck is built, then it has 48 cards: 12 per good with values 0,1,1,2,2,3,3,3,4,4,5,5 (sum 33 per good).
  R4. When round is r, then the active seat is ((r-1) mod N)+1.
  R5. When round mod 2N = 1, then the deck is rebuilt as all 48 cards and shuffled, and every ship_value, ship_count and ship_favoured is set to 0, while florins and cumulative counts are kept.
  R6. When a round begins, then 3 cards are drawn from the deck and revealed to everyone in order as revealed cards 1, 2 and 3.
  R7. When the active seat chooses lot size k (1, 2 or 3), then the lot is the first k revealed cards and the other 3-k revealed cards are discarded for the day.
  R8. When bids are made, then every player, the active seat included, bids at the same time a whole number from 0 to their current florins, and 0 is a pass.
  R9. When a player's ship_count plus lot_size exceeds 5 (for example ship_count 4 and lot_size 2), then that player's bid becomes 0.
  R10. When the highest bid is above 0 and exactly one player made it, then that player pays their bid to the bank, the florins leave the game, and that player wins the lot.
  R11. When all bids are 0, or two or more players tie for the highest bid, then the lot is discarded, nobody pays and there is no sale.
  R12. When a player wins a lot, then their ship_value increases by the sum of the lot values, their ship_count by the lot size, their ship_favoured by the number of lot cards of their favoured good, and each cumulative good count by the number of lot cards of that good.
  R13. When a round's auction ends, then the lot, every bid, and the winner and price (or 'no sale') are announced to everyone.
  R14. When round mod 2N = 0, then every player whose ship_value equals the highest ship_value gains 10 florins, if that value is above 0.
  R15. When round mod 2N = 0, then every player whose ship_value equals the highest ship_value strictly below the top gains 5 florins, if that value is above 0.
  R16. When round mod 2N = 0, then for each of the four goods, every player whose cumulative count equals the highest count of that good gains 4 florins, if that count is at least 1.
  R17. When round mod 2N = 0, then each player gains 3 florins per card of their favoured good on their ship (3 * ship_favoured).
  R18. When round = 6N (18 with 3 players, 24 with 4, 30 with 5, 36 with 6), then the game ends after that round's day-end payouts.
  R19. When the game ends, then the player with the most florins wins, and players tied for the most share the win.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Lot size | asked: the active seat only | options: 1, 2 or 3, always (even if the active seat's own ship could not hold the lot).
  - Sealed bid | asked: every seat at the same time | options: any whole number from 0 to that seat's current florins; a seat with 0 florins may only bid 0. A seat whose ship cannot hold the lot may still bid, but the bid is voided to 0.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round = 6 * N
  - each player's standing: you.florins (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their florins after round 6N. The most florins wins, and players tied for the most share the win (a draw).
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

- each player: `florins` (number, visible: ally, starts 40): The player's money and score. Only the owner sees it until the end.
- each player: `ship_value` (number, visible: public, starts 0): Sum of the card values on the ship today.
- each player: `ship_count` (number, visible: public, starts 0): Number of cards on the ship today, at most 5.
- each player: `grain_count` (number, visible: public, starts 0): Cumulative Grain cards won over the whole game.
- each player: `cloth_count` (number, visible: public, starts 0): Cumulative Cloth cards won over the whole game.
- each player: `spice_count` (number, visible: public, starts 0): Cumulative Spice cards won over the whole game.
- each player: `dye_count` (number, visible: public, starts 0): Cumulative Dye cards won over the whole game.
- the table: `round` (number, visible: public, starts 0): Current round number, from 1 to 6N.
- the table: `active_seat` (number, visible: public, starts 1): ((round-1) mod N)+1.
- the table: `lot` (list, visible: public, starts []): The first lot_size revealed cards.
- the table: `lot_size` (number, visible: public, starts 0): 1, 2 or 3, chosen by the active seat.
- the table: `high_bid` (number, visible: public, starts 0): Highest valid bid this round.
- the table: `winner_seat` (number, visible: public, starts 0): Seat that bought the lot this round, or 0 for no sale.
- parameters (each must be an attribute holding this value, never a number buried in a step): starting_florins = 40, ship_capacity = 5, goods_count = 4, deck_size = 48, cards_per_good = 12, value_0_cards_per_good = 1, value_1_cards_per_good = 2, value_2_cards_per_good = 2, value_3_cards_per_good = 3, value_4_cards_per_good = 2, value_5_cards_per_good = 2, value_sum_per_good = 33, favour_pool_copies_3_to_4_players = 1, favour_pool_copies_5_to_6_players = 2, rounds_per_day_per_player = 2, days = 3, rounds_per_game_per_player = 6, revealed_cards_per_round = 3, lot_size_min = 1, lot_size_max = 3, bid_min = 0, top_ship_bonus = 10, second_ship_bonus = 5, majority_bonus = 4, majority_min_count = 1, favoured_card_bonus = 3
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

1) Build the deck correctly at each day start (round mod 2N = 1). For each of the 4 goods, append 12 cards with values 0,1,1,2,2,3,3,3,4,4,5,5, using the value_k_cards_per_good parameters, so the deck holds 48 distinct entries such as 'Grain-0' and 'Grain-1'. Then shuffle it once. Currently a single 'Spice-3' is appended three times, which suggests a loop writes the same pick each time or the pick is not refreshed; fix the append so each card's name comes from that iteration's good and value. 2) Increment `round` and compute active_seat = ((round-1) mod N)+1 exactly once, at the start of each round and before the reveal and the lot-size choice. Do not increment it again within the same round. In round 1 the active seat must be seat 1, and it must be offered lot sizes 1, 2 and 3. 3) Make sure the reveal draws the top 3 cards from the 48-card deck, leaving 45 after round 1. The lot must be the first lot_size revealed cards and the rest go to the discard. Confirm that the lot-size choice is actually applied: in the trace the lot ends up as ['Spice-3'] with size 1 even though the tests chose 2.


YOUR PREVIOUS GAME FILE WAS REFUSED. Here it is:
{
  "schema": 1,
  "meta": {
    "id": "medici_sealed_ledgers_revised",
    "name": "Medici: Sealed Ledgers (revised)",
    "players": {
      "min": 3,
      "max": 6,
      "suggested": 4
    },
    "blurb": "Set the lot, bid in secret, load your ship: florins for the richest ships, majorities in goods and a secret favoured good."
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
        "visible": "ally",
        "type": "number",
        "initial": 40
      },
      {
        "key": "favoured_good",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "ship_cards",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "ship_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "ship_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "ship_favoured",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "grain_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "cloth_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "spice_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "dye_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bid",
        "visible": "public",
        "type": "number",
        "initial": 0
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
        "key": "active_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "favour_pool",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "revealed",
        "visible": "public",
        "type": "list",
        "initial": []
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
        "key": "auction_lot",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "discard",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "high_bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "high_count",
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
        "key": "top_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "second_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "grain_max",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "cloth_max",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "spice_max",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "dye_max",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "goods",
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
        "key": "full_deck",
        "visible": "none",
        "type": "list",
        "initial": [
          "Grain-0",
          "Grain-1",
          "Grain-1",
          "Grain-2",
          "Grain-2",
          "Grain-3",
          "Grain-3",
          "Grain-3",
          "Grain-4",
          "Grain-4",
          "Grain-5",
          "Grain-5",
          "Cloth-0",
          "Cloth-1",
          "Cloth-1",
          "Cloth-2",
          "Cloth-2",
          "Cloth-3",
          "Cloth-3",
          "Cloth-3",
          "Cloth-4",
          "Cloth-4",
          "Cloth-5",
          "Cloth-5",
          "Spice-0",
          "Spice-1",
          "Spice-1",
          "Spice-2",
          "Spice-2",
          "Spice-3",
          "Spice-3",
          "Spice-3",
          "Spice-4",
          "Spice-4",
          "Spice-5",
          "Spice-5",
          "Dye-0",
          "Dye-1",
          "Dye-1",
          "Dye-2",
          "Dye-2",
          "Dye-3",
          "Dye-3",
          "Dye-3",
          "Dye-4",
          "Dye-4",
          "Dye-5",
          "Dye-5"
        ]
      },
      {
        "key": "starting_florins",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "ship_capacity",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "goods_count",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 48
      },
      {
        "key": "cards_per_good",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "value_0_cards_per_good",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "value_1_cards_per_good",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "value_2_cards_per_good",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "value_3_cards_per_good",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "value_4_cards_per_good",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "value_5_cards_per_good",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "value_sum_per_good",
        "visible": "public",
        "type": "number",
        "initial": 33
      },
      {
        "key": "favour_pool_copies_3_to_4_players",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "favour_pool_copies_5_to_6_players",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "rounds_per_day_per_player",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "days",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "rounds_per_game_per_player",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "revealed_cards_per_round",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "lot_size_min",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "lot_size_max",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "bid_min",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "top_ship_bonus",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "second_ship_bonus",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "majority_bonus",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "majority_min_count",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "favoured_card_bonus",
        "visible": "public",
        "type": "number",
        "initial": 3
      }
    ]
  },
  "setup": [
    {
      "use": "tell",
      "label": "the seats",
      "to": "all",
      "text": "The merchants take their seats. Seat 1 opens the first day."
    },
    {
      "use": "update",
      "label": "starting florins",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "florins",
            "value": {
              "calc": "starting_florins"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "empty ships",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "ship_cards",
            "value": []
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
            "key": "ship_count",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "ship_favoured",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "empty good counts",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "grain_count",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "cloth_count",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "spice_count",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "dye_count",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "the favour pool",
      "do": [
        {
          "set": {
            "key": "favour_pool",
            "value": {
              "calc": "[g for g in goods] + ([g for g in goods] if len(players) >= 5 else [])"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "deal the favoured goods",
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "favour_pool[min(int(uniform(0, len(favour_pool))), len(favour_pool) - 1)]"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 1"
            },
            "key": "favoured_good",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "favour_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "favour_pool[min(int(uniform(0, len(favour_pool))), len(favour_pool) - 1)]"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 2"
            },
            "key": "favoured_good",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "favour_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "favour_pool[min(int(uniform(0, len(favour_pool))), len(favour_pool) - 1)]"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 3"
            },
            "key": "favoured_good",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "favour_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "favour_pool[min(int(uniform(0, len(favour_pool))), len(favour_pool) - 1)]"
            },
            "if": {
              "calc": "len(players) >= 4"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 4"
            },
            "key": "favoured_good",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "favour_pool",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 4"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "favour_pool[min(int(uniform(0, len(favour_pool))), len(favour_pool) - 1)]"
            },
            "if": {
              "calc": "len(players) >= 5"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 5"
            },
            "key": "favoured_good",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "favour_pool",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 5"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "favour_pool[min(int(uniform(0, len(favour_pool))), len(favour_pool) - 1)]"
            },
            "if": {
              "calc": "len(players) >= 6"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 6"
            },
            "key": "favoured_good",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "favour_pool",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 6"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "round zero",
      "do": [
        {
          "set": {
            "key": "round",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "sync",
      "label": "your ledger",
      "mode": "self",
      "to": "all",
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "start",
      "label": "the round begins",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "key": "active_seat",
            "value": {
              "calc": "(round - 1) % len(players) + 1"
            }
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
            "key": "high_bid",
            "value": 0
          }
        },
        {
          "set": {
            "key": "high_count",
            "value": 0
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
      "text": "Round {round} begins. Seat {active_seat} is the active seat."
    },
    {
      "use": "update",
      "phase": "start",
      "label": "day start: the deck",
      "when": {
        "calc": "round % (rounds_per_day_per_player * len(players)) == 1"
      },
      "do": [
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "[c for c in full_deck]"
            }
          }
        },
        {
          "set": {
            "key": "discard",
            "value": []
          }
        }
      ],
      "text": "A new day begins. The deck is rebuilt with all {deck_size} cards and shuffled."
    },
    {
      "use": "update",
      "phase": "start",
      "label": "day start: the ships",
      "when": {
        "calc": "round % (rounds_per_day_per_player * len(players)) == 1"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "ship_cards",
            "value": []
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
            "key": "ship_count",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "ship_favoured",
            "value": 0
          }
        }
      ],
      "text": "Every ship sails out empty. Florins and cumulative good counts are kept."
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "the reveal",
      "do": [
        {
          "set": {
            "key": "revealed",
            "value": []
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
            }
          }
        },
        {
          "append": {
            "key": "revealed",
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
            }
          }
        },
        {
          "append": {
            "key": "revealed",
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
            }
          }
        },
        {
          "append": {
            "key": "revealed",
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
      "text": "Revealed cards 1, 2 and 3, in order: {revealed}."
    },
    {
      "use": "ask",
      "phase": "lot",
      "label": "lot size",
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "lot_size_min"
        },
        "max": {
          "calc": "lot_size_max"
        }
      },
      "verify": {
        "bind": "ls"
      },
      "text": "You are the active seat. The revealed cards, in order, are {revealed}. Choose the lot size, 1, 2 or 3: the lot is that many of the first revealed cards, and the rest are discarded for the day."
    },
    {
      "use": "update",
      "phase": "lot",
      "label": "the lot",
      "do": [
        {
          "set": {
            "key": "lot_size",
            "value": "$ls"
          }
        },
        {
          "set": {
            "key": "lot",
            "value": {
              "calc": "[revealed[i] for i in [0, 1, 2] if i < lot_size]"
            }
          }
        },
        {
          "set": {
            "key": "discard",
            "value": {
              "calc": "discard + [revealed[i] for i in [0, 1, 2] if i >= lot_size]"
            }
          }
        },
        {
          "set": {
            "key": "auction_lot",
            "value": {
              "calc": "[c for c in lot]"
            }
          }
        },
        {
          "set": {
            "key": "revealed",
            "value": []
          }
        }
      ],
      "text": "Seat {active_seat} sets the lot size at {lot_size}. The lot is {lot}."
    },
    {
      "use": "sync",
      "phase": "bid",
      "label": "your ledger before bidding",
      "mode": "self",
      "to": "all",
      "text": "Before you bid:"
    },
    {
      "use": "poll",
      "phase": "bid",
      "label": "sealed bids",
      "to": {
        "where": "you.florins > 0"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "bid_min"
        },
        "max": {
          "calc": "you.florins"
        }
      },
      "store": "bid",
      "text": "The lot is {lot} (size {lot_size}). Write a sealed bid: a whole number from 0 to your florins; 0 is a pass. If your ship count plus the lot size would exceed {ship_capacity}, your bid is voided to 0. The single highest bid above 0 pays it to the bank and takes the lot; if bids tie for highest or all are 0, nobody pays and the lot is discarded."
    },
    {
      "use": "update",
      "phase": "bid",
      "label": "void bids that do not fit",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.ship_count + lot_size > ship_capacity"
            },
            "key": "bid",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "bid",
      "label": "the high bid",
      "do": [
        {
          "set": {
            "key": "high_bid",
            "value": {
              "calc": "max([p.bid for p in players])"
            }
          }
        },
        {
          "set": {
            "key": "high_count",
            "value": {
              "calc": "count(p.bid == high_bid for p in players)"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "sale",
      "label": "payment",
      "do": [
        {
          "set": {
            "key": "winner_seat",
            "value": {
              "calc": "min([p.seat for p in players if p.bid == high_bid])"
            },
            "if": {
              "calc": "high_bid > 0 and high_count == 1"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "winner_seat > 0 and you.seat == winner_seat and you.florins >= you.bid"
            },
            "key": "florins",
            "value": {
              "calc": "-you.bid"
            }
          }
        },
        {
          "set": {
            "key": "discard",
            "value": {
              "calc": "discard + lot"
            },
            "if": {
              "calc": "winner_seat == 0"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "sale",
      "label": "loading the ship",
      "when": {
        "calc": "winner_seat > 0"
      },
      "do": [
        {
          "set": {
            "players": {
              "where": "you.seat == winner_seat"
            },
            "key": "ship_cards",
            "value": {
              "calc":
... (cut)

Why it was refused: it plays, but part of it does nothing: game attribute `goods` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `full_deck` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "medici_sealed_ledgers_revised",
    "name": "Medici: Sealed Ledgers (revised)",
    "players": {
      "min": 3,
      "max": 6,
      "suggested": 4
    },
    "blurb": "Set the lot, bid in secret, load your ship: florins for the richest ships, majorities in goods and a secret favoured good."
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
        "visible": "ally",
        "type": "number",
        "initial": 40
      },
      {
        "key": "favoured_good",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "ship_cards",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "ship_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "ship_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "ship_favoured",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "grain_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "cloth_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "spice_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "dye_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bid",
        "visible": "public",
        "type": "number",
        "initial": 0
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
        "key": "active_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "favour_pool",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "revealed",
        "visible": "public",
        "type": "list",
        "initial": []
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
        "key": "auction_lot",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "discard",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "high_bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "high_count",
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
        "key": "top_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "second_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "grain_max",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "cloth_max",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "spice_max",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "dye_max",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "starting_florins",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "ship_capacity",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "goods_count",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 48
      },
      {
        "key": "cards_per_good",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "value_0_cards_per_good",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "value_1_cards_per_good",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "value_2_cards_per_good",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "value_3_cards_per_good",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "value_4_cards_per_good",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "value_5_cards_per_good",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "value_sum_per_good",
        "visible": "public",
        "type": "number",
        "initial": 33
      },
      {
        "key": "favour_pool_copies_3_to_4_players",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "favour_pool_copies_5_to_6_players",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "rounds_per_day_per_player",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "days",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "rounds_per_game_per_player",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "revealed_cards_per_round",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "lot_size_min",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "lot_size_max",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "bid_min",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "top_ship_bonus",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "second_ship_bonus",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "majority_bonus",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "majority_min_count",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "favoured_card_bonus",
        "visible": "public",
        "type": "number",
        "initial": 3
      }
    ]
  },
  "setup": [
    {
      "use": "tell",
      "label": "the seats",
      "to": "all",
      "text": "The merchants take their seats. Seat 1 opens the first day."
    },
    {
      "use": "update",
      "label": "starting florins",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "florins",
            "value": {
              "calc": "starting_florins"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "empty ships",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "ship_cards",
            "value": []
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
            "key": "ship_count",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "ship_favoured",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "empty good counts",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "grain_count",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "cloth_count",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "spice_count",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "dye_count",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "the favour pool",
      "do": [
        {
          "set": {
            "key": "favour_pool",
            "value": {
              "calc": "['Grain', 'Cloth', 'Spice', 'Dye'] * (favour_pool_copies_5_to_6_players if len(players) >= 5 else favour_pool_copies_3_to_4_players)"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "deal the favoured goods",
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "favour_pool[min(int(uniform(0, len(favour_pool))), len(favour_pool) - 1)]"
            }
          }
        },
        {
          "set": {
            "player": 1,
            "key": "favoured_good",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "favour_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "favour_pool[min(int(uniform(0, len(favour_pool))), len(favour_pool) - 1)]"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "favoured_good",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "favour_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "favour_pool[min(int(uniform(0, len(favour_pool))), len(favour_pool) - 1)]"
            }
          }
        },
        {
          "set": {
            "player": 3,
            "key": "favoured_good",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "favour_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "favour_pool[min(int(uniform(0, len(favour_pool))), len(favour_pool) - 1)]"
            },
            "if": {
              "calc": "len(players) >= 4"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 4"
            },
            "key": "favoured_good",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "favour_pool",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 4"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "favour_pool[min(int(uniform(0, len(favour_pool))), len(favour_pool) - 1)]"
            },
            "if": {
              "calc": "len(players) >= 5"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 5"
            },
            "key": "favoured_good",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "favour_pool",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 5"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "favour_pool[min(int(uniform(0, len(favour_pool))), len(favour_pool) - 1)]"
            },
            "if": {
              "calc": "len(players) >= 6"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 6"
            },
            "key": "favoured_good",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "favour_pool",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 6"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "round zero",
      "do": [
        {
          "set": {
            "key": "round",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "sync",
      "label": "your ledger",
      "mode": "self",
      "to": "all",
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "start",
      "label": "the round begins",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "key": "active_seat",
            "value": {
              "calc": "(round - 1) % len(players) + 1"
            }
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
            "key": "high_bid",
            "value": 0
          }
        },
        {
          "set": {
            "key": "high_count",
            "value": 0
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
      "text": "Round {round} begins. Seat {active_seat} is the active seat."
    },
    {
      "use": "update",
      "phase": "start",
      "label": "day start: the deck",
      "when": {
        "calc": "round % (rounds_per_day_per_player * len(players)) == 1"
      },
      "do": [
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "[g + '-' + v for g in ['Grain', 'Cloth', 'Spice', 'Dye'] for v in (['0'] * value_0_cards_per_good + ['1'] * value_1_cards_per_good + ['2'] * value_2_cards_per_good + ['3'] * value_3_cards_per_good + ['4'] * value_4_cards_per_good + ['5'] * value_5_cards_per_good)]"
            }
          }
        },
        {
          "set": {
            "key": "discard",
            "value": []
          }
        }
      ],
      "text": "A new day begins. The deck is rebuilt with all {deck_size} cards and shuffled."
    },
    {
      "use": "update",
      "phase": "start",
      "label": "day start: the ships",
      "when": {
        "calc": "round % (rounds_per_day_per_player * len(players)) == 1"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "ship_cards",
            "value": []
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
            "key": "ship_count",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "ship_favoured",
            "value": 0
          }
        }
      ],
      "text": "Every ship sails out empty. Florins and cumulative good counts are kept."
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "the reveal",
      "do": [
        {
          "set": {
            "key": "revealed",
            "value": []
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
            }
          }
        },
        {
          "append": {
            "key": "revealed",
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
            }
          }
        },
        {
          "append": {
            "key": "revealed",
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
            }
          }
        },
        {
          "append": {
            "key": "revealed",
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
      "text": "Revealed cards 1, 2 and 3, in order: {revealed}."
    },
    {
      "use": "ask",
      "phase": "lot",
      "label": "lot size",
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "lot_size_min"
        },
        "max": {
          "calc": "lot_size_max"
        }
      },
      "verify": {
        "bind": "ls"
      },
      "text": "You are the active seat. The revealed cards, in order, are {revealed}. Choose the lot size, 1, 2 or 3: the lot is that many of the first revealed cards, and the rest are discarded for the day."
    },
    {
      "use": "update",
      "phase": "lot",
      "label": "the lot",
      "do": [
        {
          "set": {
            "key": "lot_size",
            "value": {
              "calc": "int($ls)"
            }
          }
        },
        {
          "set": {
            "key": "lot",
            "value": {
              "calc": "[revealed[i] for i in [0, 1, 2] if i < int($ls)]"
            }
          }
        },
        {
          "set": {
            "key": "auction_lot",
            "value": {
              "calc": "[revealed[i] for i in [0, 1, 2] if i < int($ls)]"
            }
          }
        },
        {
          "set": {
            "key": "discard",
            "value": {
              "calc": "discard + [revealed[i] for i in [0, 1, 2] if i >= int($ls)]"
            }
          }
        },
        {
          "set": {
            "key": "revealed",
            "value": []
          }
        }
      ],
      "text": "Seat {active_seat} sets the lot size at {lot_size}. The lot is {lot}."
    },
    {
      "use": "sync",
      "phase": "bid",
      "label": "your ledger before bidding",
      "mode": "self",
      "to": "all",
      "text": "Before you bid:"
    },
    {
      "use": "poll",
      "phase": "bid",
      "label": "sealed bids",
      "to": {
        "where": "you.florins > 0"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "bid_min"
        },
        "max": {
          "calc": "you.florins"
        }
      },
      "store": "bid",
      "text": "The lot is {lot} (size {lot_size}). Write a sealed bid: a whole number from 0 to your florins; 0 is a pass. If your ship count plus the lot size would exceed {ship_capacity}, your bid is voided to 0. The single highest bid above 0 pays it to the bank and takes the lot; if bids tie for highest or all are 0, nobody pays and the lot is discarded."
    },
    {
      "use": "update",
      "phase": "bid",
      "label": "void bids that do not fit",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.ship_count + lot_size > ship_capacity"
            },
            "key": "bid",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "bid",
      "label": "the high bid",
      "do": [
        {
          "set": {
            "key": "high_bid",
            "value": {
              "calc": "max([p.bid for p in players])"
            }
          }
        },
        {
          "set": {
            "key": "high_count",
            "value": {
              "calc": "count(p.bid == high_bid for p in players)"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "sale",
      "label": "payment",
      "do": [
        {
          "set": {
            "key": "winner_seat",
            "value": {
              "calc": "min([p.seat for p in players if p.bid == high_bid])"
            },
            "if": {
              "calc": "high_bid > 0 and high_count == 1"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "winner_seat > 0 and you.seat == winner_seat and you.florins >= you.bid"
            },
            "key": "florins",
            "value": {
              "calc": "-you.bid"
            }
          }
        },
        {
          "set": {
            "key": "discard",
            "value": {
              "calc": "discard + lot"
            },
            "if": {
              "calc": "winner_seat == 0"
            }
          }
        },
        {
          "set": {
            "key": "lot",
            "value": [],
            "if": {
              "calc": "winner_seat == 0"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "sale",
      "label": "loading the ship",
      "when": {
        "calc": "winner_seat > 0"
      },
      "do": [
        {
          "set": {
            "players": {
              "where": "you.seat == winner_seat"
            },
            "key": "ship_cards",
            "value": {
              "calc": "you.ship_cards + lot"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat == winner_seat"
            },
            "key": "ship_value",
            "value": {
              "calc": "sum([int(c[-1]) for c in lot])"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat == winner_seat"
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
              "where": "you.seat == winner_seat"
            },
            "key": "ship_favoured",
            "value": {
              "calc": "count(c[0] == you.favoured_good[0] for c in lot)"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat == winner_seat"
            },
            "key": "grain_count",
            "value": {
              "calc": "count(c[0] == 'G' for c in lot)"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat == winner_seat"
            },
            "key": "cloth_count",
            "value": {
              "calc": "count(c[0] == 'C' for c in lot)"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat == winner_seat"
            },
            "key": "spice_count",
            "value": {
              "calc": "count(c[0] == 'S' for c in lot)"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat == winner_seat"
            },
            "key": "dye_count",
            "value": {
              "calc": "count(c[0] == 'D' for c in lot)"
            }
          }
        },
        {
          "set": {
            "key": "lot",
            "value": []
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "sale",
      "label": "the auction result",
      "to": "all",
      "text": "Lot {auction_lot}. Bids [seat, bid]: {[[p.seat, p.bid] for p in players]}. {('Seat ' + ['1','2','3','4','5','6'][winner_seat - 1] + ' buys it for ' + ['%d' % 0][0]) if False else ''}Winner seat (0 = no sale): {winner_seat}, price {high_bid}."
    },
    {
      "use": "update",
      "phase": "day end",
      "label": "day end: top ships",
      "when": {
        "calc": "round % (rounds_per_day_per_player * len(players)) == 0"
      },
      "do": [
        {
          "set": {
            "key": "top_value",
            "value": {
              "calc": "max([p.ship_value for p in players])"
            }
          }
        },
        {
          "set": {
            "key": "second_value",
            "value": {
              "calc": "max([p.ship_value for p in players if p.ship_value < top_value] + [0])"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "day end",
      "label": "day end: ship bonuses",
      "when": {
        "calc": "round % (rounds_per_day_per_player * len(players)) == 0"
      },
      "do": [
        {
          "adjust": {
            "players": {
              "where": "top_value > 0 and you.ship_value == top_value"
            },
            "key": "florins",
            "value": {
              "calc": "top_ship_bonus"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "second_value > 0 and you.ship_value == second_value"
            },
            "key": "florins",
            "value": {
              "calc": "second_ship_bonus"
            }
          }
        }
      ],
      "text": "Day end: the top ship value is {top_value} and the second is {second_value}."
    },
    {
      "use": "update",
      "phase": "day end",
      "label": "day end: majorities",
      "when": {
        "calc": "round % (rounds_per_day_per_player * len(players)) == 0"
      },
      "do": [
        {
          "set": {
            "key": "grain_max",
            "value": {
              "calc": "max([p.grain_count for p in players])"
            }
          }
        },
        {
          "set": {
            "key": "cloth_max",
            "value": {
              "calc": "max([p.cloth_count for p in players])"
            }
          }
        },
        {
          "set": {
            "key": "spice_max",
            "value": {
              "calc": "max([p.spice_count for p in players])"
            }
          }
        },
        {
          "set": {
            "key": "dye_max",
            "value": {
              "calc": "max([p.dye_count for p in players])"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "grain_max >= majority_min_count and you.grain_count == grain_max"
            },
            "key": "florins",
            "value": {
              "calc": "majority_bonus"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "cloth_max >= majority_min_count and you.cloth_count == cloth_max"
            },
            "key": "florins",
            "value": {
              "calc": "majority_bonus"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "spice_max >= majority_min_count and you.spice_count == spice_max"
            },
            "key": "florins",
            "value": {
              "calc": "majority_bonus"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "dye_max >= majority_min_count and you.dye_count == dye_max"
            },
            "key": "florins",
            "value": {
              "calc": "majority_bonus"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "day end",
      "label": "day end: favoured goods",
      "when": {
        "calc": "round % (rounds_per_day_per_player * len(players)) == 0"
      },
      "do": [
        {
          "adjust": {
            "players": "all",
            "key": "florins",
            "value": {
              "calc": "favoured_card_bonus * you.ship_favoured"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "day end",
      "label": "day end report",
      "when": {
        "calc": "round % (rounds_per_day_per_player * len(players)) == 0"
      },
      "to": "all",
      "text": "The day ends. Ship values [seat, value]: {[[p.seat, p.ship_value] for p in players]}. Cumulative counts [seat, grain, cloth, spice, dye]: {[[p.seat, p.grain_count, p.cloth_count, p.spice_count, p.dye_count] for p in players]}. Highest counts: grain {grain_max}, cloth {cloth_max}, spice {spice_max}, dye {dye_max}."
    },
    {
      "use": "check",
      "phase": "day end",
      "label": "after the last round",
      "when": {
        "calc": "round >= rounds_per_game_per_player * len(players)"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round >= rounds_per_game_per_player * len(players)"
      },
      "rank_by": "you.florins",
      "text": "Winner: {result}. Final florins [seat, florins]: {[[p.seat, p.florins] for p in players]}."
    }
  },
  "limits": {
    "rounds": 36,
    "rounds_max": 36,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "SETUP. Each player starts with {starting_florins} florins, known only to that player, and an empty ship that holds at most {ship_capacity} cards. Each player has cumulative counts of 0 for each of the {goods_count} goods: Grain, Cloth, Spice and Dye. Before round 1, each player is dealt a secret FAVOURED GOOD from a favour pool. With 3 or 4 players the pool is the 4 goods once each ({favour_pool_copies_3_to_4_players} copy). With 5 or 6 players the pool is the 4 goods twice each ({favour_pool_copies_5_to_6_players} copies, 8 tiles). The pool is shuffled once and one tile is dealt to each player. Favoured goods stay secret until the end.\n\nDECK. The deck has {deck_size} cards: {cards_per_good} per good. Each good has the values 0,1,1,2,2,3,3,3,4,4,5,5, which sum to {value_sum_per_good}. All four goods are identical in value. Cards are written Good-Value, for example Spice-3.\n\nLENGTH. With N players a day lasts {rounds_per_day_per_player}N rounds and the game lasts {rounds_per_game_per_player}N rounds ({days} days): 18 with 3 players, 24 with 4, 30 with 5 and 36 with 6. The active seat in a round is ((round-1) mod N)+1, so each seat is active exactly twice per day.\n\nEACH ROUND, in this order:\n1. DAY START (first round of each day): the deck is rebuilt as all {deck_size} cards and shuffled. Every ship's value, count and favoured count become 0. Cumulative good counts and florins are kept.\n2. REVEAL: the top {revealed_cards_per_round} cards of the deck are shown to everyone, in order, as revealed cards 1, 2 and 3.\n3. LOT SIZE: the active seat alone chooses {lot_size_min}, 2 or {lot_size_max} (always allowed, even if their own ship could not hold the lot). The lot is the first that many revealed cards; the other revealed cards are discarded for the rest of the day.\n4. BIDS: every player, the active seat included, secretly writes a whole-number bid from {bid_min} to their current florins, all at the same moment. A bid of 0 is a pass. A player with 0 florins can only bid 0.\n5. VOID: a player's bid becomes 0 if their ship count plus the lot size would exceed {ship_capacity}. Such a player may still bid, but the bid counts as 0.\n6. SALE: if the highest bid is above 0 and exactly one player made it, that player pays their bid to the bank (those florins leave the game) and wins the lot. Otherwise, when all bids are 0 or two or more players tie for the highest, the lot is discarded, nobody pays and there is no sale.\n7. LOAD: the winner adds the lot's card values to their ship value and the lot size to their ship count, adds 1 to their ship favoured count for each lot card of their favoured good, and adds 1 to their cumulative count of each good for each lot card of that good.\n8. ANNOUNCE: the lot, every bid, and the winner and price, or no sale, are shown to everyone.\n9. DAY END (last round of each day): every player whose ship value equals the highest ship value gains {top_ship_bonus} florins, if that value is above 0. Every player whose ship value equals the highest value strictly below the top gains {second_ship_bonus} florins, if that value is above 0. For each of the four goods, every player whose cumulative count equals the highest count of that good gains {majority_bonus} florins, if that count is at least {majority_min_count}. Each player gains {favoured_card_bonus} florins per card of their favoured good on their ship.\n\nThe game ends after the day-end payouts of round {rounds_per_game_per_player}N. There is no talk. Each player sees only their own florins and favoured good; lots, all bids, prices, ships and cumulative counts are public.\n\nWINNING. After the last round the player with the most florins wins. Players tied for the most florins share the win."
}
```
````
