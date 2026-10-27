# 16 coder

- time: 2026-10-27T17:00:40+00:00 (98.1s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 953e8e61e1b0b4b2, reply sha256 4b215357147ac1c2

## Sent

````
# Task: write the XColos game file for "Medici: Sealed Ledgers"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 4; set `meta.players` to {"min": 3, "max": 4, "suggested": 4} (the suggested size is the one the game plays best at).

SETUP. Each player starts with 40 florins. Florin totals are private to each player, and the engine tracks them. The deck has 48 cards: 4 goods (Grain, Cloth, Spice, Dye) with 12 cards each. Each good has the card values 0,1,1,2,2,3,3,3,4,4,5,5. Each player is secretly dealt a different favoured good, chosen at random from the 4, and only that player knows it. Seats are numbered 1 to N. The active player in round r is seat ((r-1) mod N)+1.

DAYS AND ROUNDS. The game lasts 3 days. Each day has 2N rounds: 6 rounds with 3 players, 8 with 4. The game therefore has 6N rounds in total (18 or 24). At the start of each day, all 48 cards are shuffled into a fresh deck, and every ship is empty. A ship holds at most 5 cards.

EACH ROUND:
1. Reveal. The top 3 cards of the deck are revealed to everyone, in order, as cards A, B and C.
2. Lot size. The active player chooses 1, 2 or 3. The lot is card A, cards A and B, or cards A, B and C. Unchosen revealed cards are discarded. The lot is announced.
3. Sealed bids. All players, including the active player, at the same moment secretly bid a whole number of florins from 0 up to their own current florins. A bid of 0 is a pass.
4. Validity. A bid is treated as 0 if loading the lot would put that player's ship over 5 cards.
5. Winner. The highest valid bid above 0 wins. Ties go to the active player if tied. Otherwise they go to the tied player who comes first in seating order starting after the active player. If every bid is 0, the lot is discarded.
6. Payment and loading. The winner pays the bid to the bank and loads the lot onto their ship. The winner's ship value rises by the sum of the lot's card values. Their ship card count rises by the lot size. Their game-long count of each good rises by the number of cards of that good in the lot.
7. Announcement. The engine announces the winner, the price paid, and every player's ship card count. It does not announce florin totals.

END OF DAY (after the last round of each day):
- The highest ship value earns 15 florins. The second-highest earns 7. If several players tie for highest, they split 22 florins equally, rounded down, and no second place is paid. If several tie for second, they split 7 equally, rounded down. A ship value of 0 earns nothing.
- Then all ships are emptied: value 0, card count 0. The game-long good counts are kept.

END OF GAME (after day 3 scoring):
- Majorities. For each good, the player with the most cards of it over the whole game earns 10 florins. Ties split 10 equally, rounded down. If nobody has any cards of a good, nothing is paid for it.
- Favoured good. Each player earns 3 florins per card of their own favoured good collected over the game. Favoured goods are then revealed.

There is no talk phase.

How the winner is decided: After the end-of-game scoring, the player with the most florins wins. If several tie for most, the tied player with more total cards collected over the game wins. If still tied, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Medici: Sealed Ledgers (3 to 4 players, best with 4)

Over 3 days the active player picks a lot of 1 to 3 revealed goods cards, everyone bids for it in a sealed auction, the best ships each day are paid, and at the end good majorities and secret favoured goods are paid. Most florins wins.

STATE (every item below must exist in the file):
  - each player: florins (number, starts 40); only its owner sees it. Florins held. This is the score, and only its owner sees it.
  - each player: favoured_good (text, starts ''); only its owner sees it. Secret favoured good (Grain, Cloth, Spice or Dye). Every player has a different one, and it is revealed at game end.
  - each player: bid (number, starts 0); only its owner sees it. This round's sealed bid. It is set to 0 if the bid is invalid.
  - each player: ship_cards (list, starts []); everyone sees it. Cards loaded on the ship today.
  - each player: ship_value (number, starts 0); everyone sees it. Sum of the card values on the ship today.
  - each player: ship_count (number, starts 0); everyone sees it. Number of cards on the ship today (at most 5).
  - each player: grain_count (number, starts 0); everyone sees it. Grain cards collected over the whole game.
  - each player: cloth_count (number, starts 0); everyone sees it. Cloth cards collected over the whole game.
  - each player: spice_count (number, starts 0); everyone sees it. Spice cards collected over the whole game.
  - each player: dye_count (number, starts 0); everyone sees it. Dye cards collected over the whole game.
  - each player: total_cards (number, starts 0); everyone sees it. Total cards collected over the game. This is the tie-break.
  - the table: deck (list, starts '48 cards: Grain-0, Grain-1, Grain-1, Grain-2, Grain-2, Grain-3, Grain-3, Grain-3, Grain-4, Grain-4, Grain-5, Grain-5, and the same 12 values for Cloth, Spice and Dye'); hidden from all players. Today's shuffled deck. A draw takes a card at random.
  - the table: revealed (list, starts []); everyone sees it. Cards A, B and C revealed this round, in order.
  - the table: lot (list, starts []); everyone sees it. The cards on offer this round.
  - the table: discard (list, starts []); everyone sees it. Today's unchosen revealed cards and unsold lots.
  - the table: lot_size (number, starts 0); everyone sees it. Number of cards in the lot (1 to 3).
  - the table: lot_value (number, starts 0); everyone sees it. Sum of the card values in the lot.
  - the table: round (number, starts 1); everyone sees it. Round number, from 1 to 6N.
  - the table: day (number, starts 1); everyone sees it. Current day, from 1 to 3.
  - the table: active_seat (number, starts 1); everyone sees it. The active player, equal to ((round-1) mod N)+1.
  - the table: winner_seat (number, starts 0); everyone sees it. Seat that won this round's lot (0 if nobody did).
  - the table: price_paid (number, starts 0); everyone sees it. Winning bid paid this round.
  - parameters, each kept as a table attribute: starting_florins = 40, goods_count = 4, cards_per_good = 12, deck_size = 48, value_0_copies_per_good = 1, value_1_copies_per_good = 2, value_2_copies_per_good = 2, value_3_copies_per_good = 3, value_4_copies_per_good = 2, value_5_copies_per_good = 2, days = 3, rounds_per_day_per_player = 2, total_rounds_per_player = 6, cards_revealed_per_round = 3, min_lot_size = 1, max_lot_size = 3, ship_capacity = 5, min_bid = 0, day_first_prize = 15, day_second_prize = 7, day_tied_first_pool = 22, majority_prize = 10, favoured_per_card = 3, rank_florins_weight = 1000

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Every player gets 40 florins, which only that player can see.
  2. The four goods Grain, Cloth, Spice and Dye are shuffled. Each player is secretly dealt a different one as favoured_good, without replacement.
  3. Seats are numbered 1 to N. round=1, day=1 and active_seat=1.
  4. Ship cards, ship_value, ship_count, the four good counts and total_cards all start empty or at 0.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] table. What happens: If round mod (2N) == 1 (first round of a day), deck is rebuilt as all 48 cards, discard is emptied, and every ship_cards, ship_value and ship_count is reset to empty or 0. Then active_seat = ((round-1) mod N)+1, and winner_seat and price_paid are set to 0.
  2. [update] table. What happens: Three cards are drawn at random from deck, in order, into revealed as cards A, B and C, and removed from deck.
  3. [tell] all players. What happens: Day {day}, round {round}: the active seat is {active_seat}. The revealed cards A, B, C are {revealed}.
  4. [ask] the active seat answers: a choice: 1, 2 or 3. What happens: lot_size is set to the choice. lot = the first lot_size cards of revealed, and lot_value is set to the sum of their values. The remaining revealed cards are appended to discard, and revealed is emptied.
  5. [tell] all players. What happens: The lot is {lot} ({lot_size} cards, total value {lot_value}).
  6. [poll] all players answers: a whole number from 0 to your own florins (0 is a pass). What happens: Each player's bid is set to their answer. Bids stay hidden from the other players.
  7. [update] all players. What happens: For each player: if ship_count + lot_size > 5, then bid is set to 0.
  8. [update] table. What happens: If every bid is 0, the lot is appended to discard and winner_seat stays 0. Otherwise winner_seat is the seat with the highest bid, with ties broken by priority = N - ((seat - active_seat + N) mod N). This makes the active seat highest, then the seats after it in order. price_paid is set to the winner's bid.
  9. [update] the winner. What happens: If winner_seat > 0: the winner loses price_paid florins, the lot is appended to their ship_cards, ship_value rises by lot_value, ship_count rises by lot_size, and total_cards rises by lot_size. grain_count, cloth_count, spice_count and dye_count each rise by the number of lot cards of that good. lot is then emptied.
  10. [tell] all players. What happens: Winner: seat {winner_seat} paid {price_paid} florins (seat 0 means the lot was discarded). Ship card counts of every seat: {ship_count}. Florins are not announced.
  11. [update] all players. What happens: If round mod (2N) == 0 (end of a day), day scoring is applied. Let top = max ship_value. If top > 0 and exactly one player has top, that player gains 15. If k>1 players have top, each gains floor(22/k) and no second place is paid. If exactly one player has top, let second = the highest ship_value below top. If second > 0, the m players with second each gain floor(7/m). Then every ship_cards, ship_value and ship_count is reset to empty or 0, discard is emptied, and day rises by 1.
  12. [update] all players. What happens: If round == 6N (after day 3 scoring), majorities are paid. For each of grain_count, cloth_count, spice_count and dye_count: let M = the max over players. If M > 0, the j players with M each gain floor(10/j). Then each player gains 3 × their count of their own favoured_good.
  13. [tell] all players. What happens: If round == 6N, every player's favoured_good is revealed to everyone.
  14. [update] table. What happens: round rises by 1.
  15. [check] table. What happens: If round > 6N, the game ends. Otherwise the next round begins.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, then every player has 40 florins, visible only to that player.
  R2. When the game starts, then each player holds a different favoured good drawn at random from Grain, Cloth, Spice and Dye, known only to that player.
  R3. When a day starts (round mod 2N == 1), then the deck is rebuilt as 48 cards: 12 per good, with values 0,1,1,2,2,3,3,3,4,4,5,5.
  R4. When it is round r, then the active seat is ((r-1) mod N)+1.
  R5. When the game has N players, then each day has 2N rounds and the game has 6N rounds: 18 with 3 players, 24 with 4.
  R6. When a round starts, then 3 cards are drawn from the deck and revealed in order as A, B and C.
  R7. When the active player chooses lot size 1, 2 or 3, then the lot is A, A+B or A+B+C, and the unchosen revealed cards are discarded.
  R8. When bidding happens, then all players, including the active player, bid at the same time a whole number from 0 to their own current florins, and 0 is a pass.
  R9. When a player's ship_count + lot_size > 5, then that player's bid is treated as 0.
  R10. When one valid bid above 0 is strictly highest, then that bidder wins the lot.
  R11. When the highest valid bids tie and the active player is among them, then the active player wins.
  R12. When the highest valid bids tie without the active player, then the tied player who comes first in seat order after the active seat wins.
  R13. When every bid is 0, then the lot is discarded and nobody pays.
  R14. When a player wins a lot with bid b, then their florins fall by b, ship_value rises by the sum of the lot's card values, ship_count and total_cards rise by the lot size, and each good count rises by that good's cards in the lot.
  R15. When a round ends, then the winner, the price paid and every player's ship_count are announced, and florins are not announced.
  R16. When a day ends and one player alone has the highest ship value (above 0), then that player gains 15 florins.
  R17. When a day ends and k>1 players tie for the highest ship value (above 0), then each gains floor(22/k) florins and no second place is paid.
  R18. When a day ends with a single leader, then the m players with the second-highest ship value (above 0) each gain floor(7/m) florins.
  R19. When a player's ship value is 0 at day end, then that player earns nothing from day scoring.
  R20. When day scoring is done, then all ships are emptied (value 0, count 0), and the game-long good counts are kept.
  R21. When the game ends, then for each good the j players with the most cards of it (more than 0) each gain floor(10/j) florins, and a good nobody collected pays nothing.
  R22. When the game ends, then each player gains 3 florins per card of their favoured good collected, and favoured goods are revealed.
  R23. When round 6N has been completed, then the game ends.
  R24. When the game ends, then the player with the most florins wins, a tie goes to more total_cards, and players still tied share the win.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Lot size | asked: the active seat only | options: 1, 2 or 3
  - Sealed bid | asked: every seat, including the active seat | options: any whole number from 0 to that seat's current florins. A seat whose ship cannot hold the lot is still asked, but its bid counts as 0.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round > 6 * N
  - each player's standing: you.florins * 1000 + you.total_cards (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: The player with the most florins after end-of-game scoring wins. A tie on florins goes to the tied player with more total cards collected over the game. Players still tied share the win, which is the draw.
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

- each player: `florins` (number, visible: ally, starts 40): Florins held. This is the score, and only its owner sees it.
- each player: `ship_count` (number, visible: public, starts 0): Number of cards on the ship today (at most 5).
- each player: `total_cards` (number, visible: public, starts 0): Total cards collected over the game. This is the tie-break.
- the table: `round` (number, visible: public, starts 1): Round number, from 1 to 6N.
- the table: `day` (number, visible: public, starts 1): Current day, from 1 to 3.
- parameters (each must be an attribute holding this value, never a number buried in a step): starting_florins = 40, goods_count = 4, cards_per_good = 12, deck_size = 48, value_0_copies_per_good = 1, value_1_copies_per_good = 2, value_2_copies_per_good = 2, value_3_copies_per_good = 3, value_4_copies_per_good = 2, value_5_copies_per_good = 2, days = 3, rounds_per_day_per_player = 2, total_rounds_per_player = 6, cards_revealed_per_round = 3, min_lot_size = 1, max_lot_size = 3, ship_capacity = 5, min_bid = 0, day_first_prize = 15, day_second_prize = 7, day_tied_first_pool = 22, majority_prize = 10, favoured_per_card = 3, rank_florins_weight = 1000
- the game ends with ONE ending whose `rank_by` is `you.florins * 1000 + you.total_cards`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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

1. Do not advance `round` or `active_seat` at the start of a round. Work out the active seat from the current round as ((round-1) mod N)+1, play the whole round (reveal, lot size, simultaneous bids, validity, winner, payment and loading), and increase `round` only after the round ends. Round 1 must have seat 1 active, and the game must not reach round 3 after one round of play.
2. Put the lot-size choice (1/2/3) only to the active seat.
3. Run the bids as one simultaneous poll for all seats, including the active seat. Each seat's options run from 0 up to its own `florins`.
4. Build the lot from the first lot_size revealed cards and move only the unchosen revealed cards to `discard`. With lot size 2, exactly C is discarded.
5. Score a bid as 0 when ship_count + lot_size exceeds ship_capacity.
6. The highest valid bid above 0 wins. Break ties in favour of the active seat, then by seat order starting after the active seat.
7. Charge the winner the bid and add the lot to the winner's ship_count, ship_value, per-good counts and total_cards.
8. Check that the seed or given deck is not replaced before the reveal, so the revealed A, B and C come from the deck in place.


YOUR PREVIOUS GAME FILE WAS REFUSED. Here it is:
{
  "schema": 1,
  "meta": {
    "id": "medici_sealed_ledgers",
    "name": "Medici: Sealed Ledgers",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 4
    },
    "blurb": "Three days of sealed-bid auctions for lots of goods: fill your ship, win the day, take good majorities and collect your secret favoured good."
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
        "key": "bid",
        "visible": "ally",
        "type": "number",
        "initial": 0
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
        "key": "total_cards",
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
        "initial": [
          "Grain-0", "Grain-1", "Grain-1", "Grain-2", "Grain-2", "Grain-3", "Grain-3", "Grain-3", "Grain-4", "Grain-4", "Grain-5", "Grain-5",
          "Cloth-0", "Cloth-1", "Cloth-1", "Cloth-2", "Cloth-2", "Cloth-3", "Cloth-3", "Cloth-3", "Cloth-4", "Cloth-4", "Cloth-5", "Cloth-5",
          "Spice-0", "Spice-1", "Spice-1", "Spice-2", "Spice-2", "Spice-3", "Spice-3", "Spice-3", "Spice-4", "Spice-4", "Spice-5", "Spice-5",
          "Dye-0", "Dye-1", "Dye-1", "Dye-2", "Dye-2", "Dye-3", "Dye-3", "Dye-3", "Dye-4", "Dye-4", "Dye-5", "Dye-5"
        ]
      },
      {
        "key": "full_deck",
        "visible": "none",
        "type": "list",
        "initial": [
          "Grain-0", "Grain-1", "Grain-1", "Grain-2", "Grain-2", "Grain-3", "Grain-3", "Grain-3", "Grain-4", "Grain-4", "Grain-5", "Grain-5",
          "Cloth-0", "Cloth-1", "Cloth-1", "Cloth-2", "Cloth-2", "Cloth-3", "Cloth-3", "Cloth-3", "Cloth-4", "Cloth-4", "Cloth-5", "Cloth-5",
          "Spice-0", "Spice-1", "Spice-1", "Spice-2", "Spice-2", "Spice-3", "Spice-3", "Spice-3", "Spice-4", "Spice-4", "Spice-5", "Spice-5",
          "Dye-0", "Dye-1", "Dye-1", "Dye-2", "Dye-2", "Dye-3", "Dye-3", "Dye-3", "Dye-4", "Dye-4", "Dye-5", "Dye-5"
        ]
      },
      {
        "key": "goods_pool",
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
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
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
        "key": "discard",
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
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "day",
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
        "key": "winner_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "price_paid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "ship_counts",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "favoured_reveal",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "top_value",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "top_count",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "second_value",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "second_count",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "starting_florins",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "goods_count",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "cards_per_good",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 48
      },
      {
        "key": "value_0_copies_per_good",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "value_1_copies_per_good",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "value_2_copies_per_good",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "value_3_copies_per_good",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "value_4_copies_per_good",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "value_5_copies_per_good",
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
        "key": "rounds_per_day_per_player",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "total_rounds_per_player",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "cards_revealed_per_round",
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
        "key": "max_lot_size",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "ship_capacity",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "min_bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "day_first_prize",
        "visible": "public",
        "type": "number",
        "initial": 15
      },
      {
        "key": "day_second_prize",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "day_tied_first_pool",
        "visible": "public",
        "type": "number",
        "initial": 22
      },
      {
        "key": "majority_prize",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "favoured_per_card",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "rank_florins_weight",
        "visible": "public",
        "type": "number",
        "initial": 1000
      }
    ]
  },
  "setup": [
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
      "label": "deal favoured goods",
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "goods_pool[min(int(uniform(0, len(goods_pool))), len(goods_pool) - 1)]"
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
            "key": "goods_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "goods_pool[min(int(uniform(0, len(goods_pool))), len(goods_pool) - 1)]"
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
            "key": "goods_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "goods_pool[min(int(uniform(0, len(goods_pool))), len(goods_pool) - 1)]"
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
            "key": "goods_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "goods_pool[min(int(uniform(0, len(goods_pool))), len(goods_pool) - 1)]"
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
            "key": "goods_pool",
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
            "value": ""
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "round, day and active seat",
      "do": [
        {
          "set": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "key": "day",
            "value": 1
          }
        },
        {
          "set": {
            "key": "active_seat",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "empty ships and counts",
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
        },
        {
          "set": {
            "players": "all",
            "key": "total_cards",
            "value": 0
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
      "phase": "start",
      "label": "start of round",
      "do": [
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "full_deck"
            },
            "if": {
              "calc": "round % (rounds_per_day_per_player * len(players)) == 1"
            }
          }
        },
        {
          "set": {
            "key": "discard",
            "value": [],
            "if": {
              "calc": "round % (rounds_per_day_per_player * len(players)) == 1"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "round % (rounds_per_day_per_player * len(players)) == 1"
            },
            "key": "ship_cards",
            "value": []
          }
        },
        {
          "set": {
            "players": {
              "where": "round % (rounds_per_day_per_player * len(players)) == 1"
            },
            "key": "ship_value",
            "value": 0
          }
        },
        {
          "set": {
            "players": {
              "where": "round % (rounds_per_day_per_player * len(players)) == 1"
            },
            "key": "ship_count",
            "value": 0
          }
        },
        {
          "set": {
            "key": "active_seat",
            "value": {
              "calc": "((round - 1) % len(players)) + 1"
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
            "key": "price_paid",
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
      ]
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "reveal three cards",
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
      ]
    },
    {
      "use": "tell",
      "phase": "reveal",
      "label": "the reveal",
      "to": "all",
      "text": "Day {day}, round {round}: the active seat is {active_seat}. The revealed cards A, B, C are {revealed}."
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
          "calc": "min_lot_size"
        },
        "max": {
          "calc": "max_lot_size"
        }
      },
      "verify": {
        "bind": "lot_choice"
      },
      "text": "You are the active player. The revealed cards A, B, C are {revealed}. Choose the lot size: 1 (card A), 2 (cards A and B) or 3 (cards A, B and C). Unchosen revealed cards are discarded."
    },
    {
      "use": "update",
      "phase": "lot",
      "label": "form the lot",
      "do": [
        {
          "set": {
            "key": "lot_size",
            "value": {
              "calc": "int($lot_choice)"
            }
          }
        },
        {
          "set": {
            "key": "lot",
            "value": {
              "calc": "[revealed[0]] + ([revealed[1]] if lot_size >= 2 else []) + ([revealed[2]] if lot_size >= 3 else [])"
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
        },
        {
          "set": {
            "key": "discard",
            "value": {
              "calc": "discard + ([revealed[1]] if lot_size < 2 else []) + ([revealed[2]] if lot_size < 3 else [])"
            }
          }
        },
        {
          "set": {
            "key": "revealed",
            "value": []
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "lot",
      "label": "the lot",
      "to": "all",
      "text": "The lot is {lot} ({lot_size} cards, total value {lot_value})."
    },
    {
      "use": "poll",
      "phase": "bid",
      "label": "sealed bids",
      "to": "acting",
      "answer": {
        "type": "number",
        "min": {
          "calc": "min_bid"
        },
        "max": {
          "calc": "you.florins"
        }
      },
      "store": "bid",
      "text": "Sealed bid for the lot {lot} ({lot_size} cards, total value {lot_value}). Bid a whole number of florins from 0 up to your current florins ({florins}); 0 is a pass. If loading the lot would put your ship over {ship_capacity} cards, your bid counts as 0. Bids stay hidden."
    },
    {
      "use": "update",
      "phase": "bid",
      "label": "validity",
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
      "label": "find the winner",
      "do": [
        {
          "set": {
            "key": "winner_seat",
            "value": {
              "calc": "0 if max([p.bid for p in players]) <= 0 else [p.seat for p in players if p.bid == max([q.bid for q in players]) and (len(players) - ((p.seat - active_seat + len(players)) % len(players))) == max([len(players) - ((q.seat - active_seat + len(players)) % len(players)) for q in players if q.bid == max([r.bid for r in players])])][0]"
            }
          }
        },
        {
          "set": {
            "key": "price_paid",
            "value": {
              "calc": "max([p.bid for p in players]) if winner_seat > 0 else 0"
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
      "phase": "load",
      "label": "payment and loading",
      "do": [
        {
          "adjust": {
            "players": {
              "where": "you.seat == winner_seat and you.florins >= price_paid"
            },
            "key": "florins",
            "value": {
              "calc": "-price_paid"
            }
          }
        },
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
              "calc": "lot_value"
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
            "key": "total_cards",
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
        },
        {
          "set": {
            "key": "ship_counts",
            "value": {
              "calc": "[p.ship_count for p in players]"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "load",
      "label": "the announcement",
      "to": "all",
      "text": "Winner: seat {winner_seat} paid {price_paid} florins (seat 0 means nobody bid and the lot was discarded). Ship card counts of every seat, in seat order: {ship_counts}. Florins are not announced."
    },
    {
      "use": "update",
      "phase": "day end",
      "label": "day scoring",
      "when": {
        "calc": "round % (rounds
... (cut)

Why it was refused: players are sent text with a `{name}` that was never filled in: placeholder: players are shown the literal {florins} (in `prompt`: "Sealed bid for the lot ['Spice-4', 'Dye-2', 'Dye-4'] (3 cards, total value 10). Bid a whol"); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {florins} (in `prompt`: "Sealed bid for the lot ['Spice-4', 'Dye-2', 'Dye-4'] (3 cards, total value 10). Bid a whol"); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {florins} (in `prompt`: "Sealed bid for the lot ['Spice-4', 'Dye-2', 'Dye-4'] (3 cards, total value 10). Bid a whol"); use only names the step can fill in (see the broadcast rule: {value} and {seat})
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "medici_sealed_ledgers",
    "name": "Medici: Sealed Ledgers",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 4
    },
    "blurb": "Three days of sealed-bid auctions for lots of goods: fill your ship, win the day, take good majorities and collect your secret favoured good."
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
        "key": "bid",
        "visible": "ally",
        "type": "number",
        "initial": 0
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
        "key": "total_cards",
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
        "initial": [
          "Grain-0", "Grain-1", "Grain-1", "Grain-2", "Grain-2", "Grain-3", "Grain-3", "Grain-3", "Grain-4", "Grain-4", "Grain-5", "Grain-5",
          "Cloth-0", "Cloth-1", "Cloth-1", "Cloth-2", "Cloth-2", "Cloth-3", "Cloth-3", "Cloth-3", "Cloth-4", "Cloth-4", "Cloth-5", "Cloth-5",
          "Spice-0", "Spice-1", "Spice-1", "Spice-2", "Spice-2", "Spice-3", "Spice-3", "Spice-3", "Spice-4", "Spice-4", "Spice-5", "Spice-5",
          "Dye-0", "Dye-1", "Dye-1", "Dye-2", "Dye-2", "Dye-3", "Dye-3", "Dye-3", "Dye-4", "Dye-4", "Dye-5", "Dye-5"
        ]
      },
      {
        "key": "full_deck",
        "visible": "none",
        "type": "list",
        "initial": [
          "Grain-0", "Grain-1", "Grain-1", "Grain-2", "Grain-2", "Grain-3", "Grain-3", "Grain-3", "Grain-4", "Grain-4", "Grain-5", "Grain-5",
          "Cloth-0", "Cloth-1", "Cloth-1", "Cloth-2", "Cloth-2", "Cloth-3", "Cloth-3", "Cloth-3", "Cloth-4", "Cloth-4", "Cloth-5", "Cloth-5",
          "Spice-0", "Spice-1", "Spice-1", "Spice-2", "Spice-2", "Spice-3", "Spice-3", "Spice-3", "Spice-4", "Spice-4", "Spice-5", "Spice-5",
          "Dye-0", "Dye-1", "Dye-1", "Dye-2", "Dye-2", "Dye-3", "Dye-3", "Dye-3", "Dye-4", "Dye-4", "Dye-5", "Dye-5"
        ]
      },
      {
        "key": "goods_pool",
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
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
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
        "key": "discard",
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
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "day",
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
        "key": "winner_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "price_paid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "ship_counts",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "favoured_reveal",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "top_value",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "top_count",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "second_value",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "second_count",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "starting_florins",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "goods_count",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "cards_per_good",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 48
      },
      {
        "key": "value_0_copies_per_good",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "value_1_copies_per_good",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "value_2_copies_per_good",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "value_3_copies_per_good",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "value_4_copies_per_good",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "value_5_copies_per_good",
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
        "key": "rounds_per_day_per_player",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "total_rounds_per_player",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "cards_revealed_per_round",
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
        "key": "max_lot_size",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "ship_capacity",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "min_bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "day_first_prize",
        "visible": "public",
        "type": "number",
        "initial": 15
      },
      {
        "key": "day_second_prize",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "day_tied_first_pool",
        "visible": "public",
        "type": "number",
        "initial": 22
      },
      {
        "key": "majority_prize",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "favoured_per_card",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "rank_florins_weight",
        "visible": "public",
        "type": "number",
        "initial": 1000
      }
    ]
  },
  "setup": [
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
      "label": "deal favoured goods",
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "goods_pool[min(int(uniform(0, len(goods_pool))), len(goods_pool) - 1)]"
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
            "key": "goods_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "goods_pool[min(int(uniform(0, len(goods_pool))), len(goods_pool) - 1)]"
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
            "key": "goods_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "goods_pool[min(int(uniform(0, len(goods_pool))), len(goods_pool) - 1)]"
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
            "key": "goods_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "goods_pool[min(int(uniform(0, len(goods_pool))), len(goods_pool) - 1)]"
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
            "key": "goods_pool",
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
            "value": ""
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "round, day and active seat",
      "do": [
        {
          "set": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "key": "day",
            "value": 1
          }
        },
        {
          "set": {
            "key": "active_seat",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "empty ships and counts",
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
        },
        {
          "set": {
            "players": "all",
            "key": "total_cards",
            "value": 0
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
      "phase": "start",
      "label": "start of round",
      "do": [
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "full_deck"
            },
            "if": {
              "calc": "round % (rounds_per_day_per_player * len(players)) == 1"
            }
          }
        },
        {
          "set": {
            "key": "discard",
            "value": [],
            "if": {
              "calc": "round % (rounds_per_day_per_player * len(players)) == 1"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "round % (rounds_per_day_per_player * len(players)) == 1"
            },
            "key": "ship_cards",
            "value": []
          }
        },
        {
          "set": {
            "players": {
              "where": "round % (rounds_per_day_per_player * len(players)) == 1"
            },
            "key": "ship_value",
            "value": 0
          }
        },
        {
          "set": {
            "players": {
              "where": "round % (rounds_per_day_per_player * len(players)) == 1"
            },
            "key": "ship_count",
            "value": 0
          }
        },
        {
          "set": {
            "key": "active_seat",
            "value": {
              "calc": "((round - 1) % len(players)) + 1"
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
            "key": "price_paid",
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
      ]
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "reveal three cards",
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
      ]
    },
    {
      "use": "tell",
      "phase": "reveal",
      "label": "the reveal",
      "to": "all",
      "text": "Day {day}, round {round}: the active seat is {active_seat}. The revealed cards A, B, C are {revealed}."
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
          "calc": "min_lot_size"
        },
        "max": {
          "calc": "max_lot_size"
        }
      },
      "verify": {
        "bind": "lot_choice"
      },
      "text": "You are the active player. The revealed cards A, B, C are {revealed}. Choose the lot size: 1 (card A), 2 (cards A and B) or 3 (cards A, B and C). Unchosen revealed cards are discarded."
    },
    {
      "use": "update",
      "phase": "lot",
      "label": "form the lot",
      "do": [
        {
          "set": {
            "key": "lot_size",
            "value": {
              "calc": "int($lot_choice)"
            }
          }
        },
        {
          "set": {
            "key": "lot",
            "value": {
              "calc": "[revealed[0]] + ([revealed[1]] if lot_size >= 2 else []) + ([revealed[2]] if lot_size >= 3 else [])"
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
        },
        {
          "set": {
            "key": "discard",
            "value": {
              "calc": "discard + ([revealed[1]] if lot_size < 2 else []) + ([revealed[2]] if lot_size < 3 else [])"
            }
          }
        },
        {
          "set": {
            "key": "revealed",
            "value": []
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "lot",
      "label": "the lot",
      "to": "all",
      "text": "The lot is {lot} ({lot_size} cards, total value {lot_value})."
    },
    {
      "use": "poll",
      "phase": "bid",
      "label": "sealed bids",
      "to": "acting",
      "answer": {
        "type": "number",
        "min": {
          "calc": "min_bid"
        },
        "max": {
          "calc": "you.florins"
        }
      },
      "store": "bid",
      "text": "Sealed bid for the lot {lot} ({lot_size} cards, total value {lot_value}). Bid a whole number of florins from 0 up to your current florins; 0 is a pass. If loading the lot would put your ship over {ship_capacity} cards, your bid counts as 0. Bids stay hidden."
    },
    {
      "use": "update",
      "phase": "bid",
      "label": "validity",
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
      "label": "find the winner",
      "do": [
        {
          "set": {
            "key": "winner_seat",
            "value": {
              "calc": "0 if max([p.bid for p in players]) <= 0 else [p.seat for p in players if p.bid == max([q.bid for q in players]) and (len(players) - ((p.seat - active_seat + len(players)) % len(players))) == max([len(players) - ((q.seat - active_seat + len(players)) % len(players)) for q in players if q.bid == max([r.bid for r in players])])][0]"
            }
          }
        },
        {
          "set": {
            "key": "price_paid",
            "value": {
              "calc": "max([p.bid for p in players]) if winner_seat > 0 else 0"
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
      "phase": "load",
      "label": "payment and loading",
      "do": [
        {
          "adjust": {
            "players": {
              "where": "you.seat == winner_seat and you.florins >= price_paid"
            },
            "key": "florins",
            "value": {
              "calc": "-price_paid"
            }
          }
        },
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
              "calc": "lot_value"
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
            "key": "total_cards",
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
        },
        {
          "set": {
            "key": "ship_counts",
            "value": {
              "calc": "[p.ship_count for p in players]"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "load",
      "label": "the announcement",
      "to": "all",
      "text": "Winner: seat {winner_seat} paid {price_paid} florins (seat 0 means nobody bid and the lot was discarded). Ship card counts of every seat, in seat order: {ship_counts}. Florins are not announced."
    },
    {
      "use": "update",
      "phase": "day end",
      "label": "day scoring",
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
            "key": "top_count",
            "value": {
              "calc": "count(p.ship_value == top_value for p in players)"
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
        },
        {
          "set": {
            "key": "second_count",
            "value": {
              "calc": "count(p.ship_value == second_value for p in players)"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "top_value > 0 and top_count == 1 and you.ship_value == top_value"
            },
            "key": "florins",
            "value": {
              "calc": "day_first_prize"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "top_value > 0 and top_count > 1 and you.ship_value == top_value"
            },
            "key": "florins",
            "value": {
              "calc": "int(day_tied_first_pool / top_count)"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "top_value > 0 and top_count == 1 and second_value > 0 and you.ship_value == second_value"
            },
            "key": "florins",
            "value": {
              "calc": "int(day_second_prize / second_count)"
            }
          }
        },
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
            "key": "discard",
            "value": []
          }
        },
        {
          "adjust": {
            "key": "day",
            "value": 1,
            "if": {
              "calc": "day < days"
            }
          }
        }
      ],
      "text": "The day ends. The best ships are paid (florins stay private) and all ships are emptied."
    },
    {
      "use": "update",
      "phase": "game end",
      "label": "end-of-game scoring",
      "when": {
        "calc": "round == total_rounds_per_player * len(players)"
      },
      "do": [
        {
          "adjust": {
            "players": {
              "where": "max([p.grain_count for p in players]) > 0 and you.grain_count == max([p.grain_count for p in players])"
            },
            "key": "florins",
            "value": {
              "calc": "int(majority_prize / count(p.grain_count == max([q.grain_count for q in players]) for p in players))"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "max([p.cloth_count for p in players]) > 0 and you.cloth_count == max([p.cloth_count for p in players])"
            },
            "key": "florins",
            "value": {
              "calc": "int(majority_prize / count(p.cloth_count == max([q.cloth_count for q in players]) for p in players))"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "max([p.spice_count for p in players]) > 0 and you.spice_count == max([p.spice_count for p in players])"
            },
            "key": "florins",
            "value": {
              "calc": "int(majority_prize / count(p.spice_count == max([q.spice_count for q in players]) for p in players))"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "max([p.dye_count for p in players]) > 0 and you.dye_count == max([p.dye_count for p in players])"
            },
            "key": "florins",
            "value": {
              "calc": "int(majority_prize / count(p.dye_count == max([q.dye_count for q in players]) for p in players))"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "florins",
            "value": {
              "calc": "favoured_per_card * (you.grain_count if you.favoured_good == 'Grain' else (you.cloth_count if you.favoured_good == 'Cloth' else (you.spice_count if you.favoured_good == 'Spice' else (you.dye_count if you.favoured_good == 'Dye' else 0))))"
            }
          }
        },
        {
          "set": {
            "key": "favoured_reveal",
            "value": {
              "calc": "[p.favoured_good for p in players]"
            }
          }
        }
      ],
      "text": "Final scoring: good majorities and favoured goods are paid."
    },
    {
      "use": "tell",
      "phase": "game end",
      "label": "favoured goods revealed",
      "when": {
        "calc": "round == total_rounds_per_player * len(players)"
      },
      "to": "all",
      "text": "Favoured goods revealed, in seat order: {favoured_reveal}."
    },
    {
      "use": "update",
      "phase": "end of round",
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
      "phase": "end of round",
      "label": "after the last round",
      "when": {
        "calc": "round > total_rounds_per_player * len(players)"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round > total_rounds_per_player * len(players)"
      },
      "rank_by": "you.florins * 1000 + you.total_cards",
      "text": "Winner: {result}. Final [seat, florins, total cards]: {[[p.seat, p.florins, p.total_cards] for p in players]}."
    }
  },
  "limits": {
    "rounds": 24,
    "rounds_max": 30,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "Each player starts with {starting_florins} florins. Your florins are private: only you and the engine know them. The deck has {deck_size} cards: {goods_count} goods (Grain, Cloth, Spice, Dye) with {cards_per_good} cards each, valued 0,1,1,2,2,3,3,3,4,4,5,5. Each player is secretly dealt a different favoured good, chosen at random; only you know yours. Seats are numbered 1 to N. The active player in round r is seat ((r-1) mod N)+1.\n\nThe game lasts {days} days. Each day has {rounds_per_day_per_player} x N rounds (6 with 3 players, 8 with 4), so the game has {total_rounds_per_player} x N rounds (18 or 24). At the start of each day all 48 cards are shuffled into a fresh deck and every ship is empty. A ship holds at most {ship_capacity} cards.\n\nEach round:\n1. Reveal. The top {cards_revealed_per_round} cards of the deck are revealed to everyone, in order, as cards A, B and C.\n2. Lot size. The active player chooses {min_lot_size}, 2 or {max_lot_size}. The lot is card A, cards A and B, or cards A, B and C. Unchosen revealed cards are discarded. The lot is announced.\n3. Sealed bids. All players, including the active player, at the same moment secretly bid a whole number of florins from {min_bid} up to their own current florins. A bid of 0 is a pass.\n4. Validity. A bid is treated as 0 if loading the lot would put that player's ship over {ship_capacity} cards; otherwise it stands as bid.\n5. Winner. The highest valid bid above 0 wins. Ties go to the active player if tied. Otherwise they go to the tied player who comes first in seating order starting after the active player. If every bid is 0, the lot is discarded and nobody pays.\n6. Payment and loading. The winner pays the bid to the bank and loads the lot onto their ship. The winner's ship value rises by the sum of the lot's card values. Their ship card count rises by the lot size. Their game-long count of each good rises by the number of cards of that good in the lot. Losing bidders pay nothing.\n7. Announcement. The engine announces the winner, the price paid, and every player's ship card count. It does not announce florin totals.\n\nEnd of day (after the last round of each day): the highest ship value earns {day_first_prize} florins. The second-highest earns {day_second_prize}. If several players tie for highest, they split {day_tied_first_pool} florins equally, rounded down, and no second place is paid. If several tie for second, they split {day_second_prize} equally, rounded down. A ship value of 0 earns nothing. Then all ships are emptied: value 0, card count 0. The game-long good counts are kept.\n\nEnd of game (after day 3 scoring): Majorities. For each good, the player with the most cards of it over the whole game earns {majority_prize} florins. Ties split {majority_prize} equally, rounded down. If nobody has any cards of a good, nothing is paid for it. Favoured good. Each player earns {favoured_per_card} florins per card of their own favoured good collected over the game. Favoured goods are then revealed.\n\nThere is no talk phase. After the end-of-game scoring, the player with the most florins wins. If several tie for most, the tied player with more total cards collected over the game wins. If still tied, the game is a draw and those players share the win."
}
```
````
