# 29 coder

- time: 2026-10-27T17:20:36+00:00 (102.9s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 84dba1f5f9998ad0, reply sha256 7e27c8f5f7038207

## Sent

````
# Task: write the XColos game file for "Modern Art: Three Studios"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

R1 Setup. There are 3 players in seats 1, 2 and 3, and 3 artists: Red, Blue and Green. Each player starts with 60 money. Money is public at all times. Each player has hand counts for Red, Blue and Green and owned counts for Red, Blue and Green; all owned counts start at 0. On the table, each artist has a season count and a cumulative value, all starting at 0. seasons_done starts at 0 and the auctioneer is seat 1.

R2 Hands, at setup only. There are three hand compositions of 7 cards each. Composition A is 4 Red, 2 Blue, 1 Green. Composition B is 1 Red, 4 Blue, 2 Green. Composition C is 2 Red, 1 Blue, 4 Green. The engine draws one random whole number from 1 to 6 and gives compositions to seats 1, 2 and 3 as follows: 1 gives A,B,C; 2 gives A,C,B; 3 gives B,A,C; 4 gives B,C,A; 5 gives C,A,B; 6 gives C,B,A. Each player sees only their own hand counts. Everyone knows the three compositions exist and that each player has a different one. This is the only random event in the game.

R3 Choose a card. The auctioneer chooses one artist from those for which their hand count is above 0.

R4 Reveal. The chosen artist is announced to everyone as the current artist. The auctioneer's hand count for that artist falls by 1, and that artist's season count rises by 1.

R5 Season-ending card. If the current artist's season count is now 3, the card is discarded unsold. Skip R6 to R8 this round and go to R9.

R6 Talk. Otherwise, all three players each write one short message at the same moment without seeing the others. All messages are then shown to everyone. Talk is not binding.

R7 Sealed bids. Otherwise, all three players, the auctioneer included, submit at the same moment a whole-number bid from 0 up to their current money. The highest bid wins. If bids tie for highest, the tied player who comes first in seat order starting from the seat after the auctioneer wins, with the auctioneer last. If every bid is 0, the auctioneer wins at price 0.

R8 Settle and announce. If the winner is not the auctioneer, the winner pays their bid to the auctioneer. If the winner is the auctioneer, they pay their bid to the bank (nothing if it is 0). In every case the winner's owned count for the current artist rises by 1; this includes paintings the auctioneer keeps, which score like any other. All three bids, the winner and the price are announced to everyone. Owned counts are public.

R9 Season scoring. Scoring happens if the season-ending card was just played (R5), or if all hands are now empty and at least one season count is above 0. When it happens:
(a) First place is the artist with the highest season count, ties broken in the order Red, Blue, Green. Its cumulative value rises by 20.
(b) Second place is the highest of the remaining two artists by season count, same tie order, but only if its season count is above 0. Its cumulative value rises by 10.
(c) The third artist, and any artist with season count 0, does not place.
(d) Each player receives from the bank, for each placed artist, their owned count of that artist times that artist's cumulative value. Unplaced artists pay 0. Note that a cumulative value can be above 0 from earlier seasons, but it pays only if the artist placed this season.
(e) The placings, the new cumulative values and each player's payout are announced.
(f) All owned counts reset to 0, all season counts reset to 0, and seasons_done rises by 1.

R10 Pass the role. The auctioneer role passes to the next seat (1 to 2, 2 to 3, 3 to 1). It skips any seat whose hand is empty.

R11 End. The game ends when seasons_done reaches 3, or when all hands are empty (after R9 has scored any unfinished season). The game lasts at most 21 rounds.

How the winner is decided: When the game ends, the player with the most money wins. If two or three players tie for the most money, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Modern Art: Three Studios (3 to 3 players, best with 3)

Three dealers take turns auctioning paintings by three artists with sealed bids; at the end of each season the most-played artists pay out, and after 3 seasons or when all cards are gone the richest player wins.

STATE (every item below must exist in the file):
  - each player: money (number, starts 60); everyone sees it. Money held; the score
  - each player: hand_red (number, starts 0); only its owner sees it. Red cards in hand
  - each player: hand_blue (number, starts 0); only its owner sees it. Blue cards in hand
  - each player: hand_green (number, starts 0); only its owner sees it. Green cards in hand
  - each player: owned_red (number, starts 0); everyone sees it. Red paintings bought this season
  - each player: owned_blue (number, starts 0); everyone sees it. Blue paintings bought this season
  - each player: owned_green (number, starts 0); everyone sees it. Green paintings bought this season
  - each player: bid (number, starts 0); only its owner sees it. This round's sealed bid. It stays hidden until all bids are in, then all bids are announced
  - each player: message (text, starts ''); everyone sees it. This round's talk message, shown once all are in
  - the table: auctioneer (number, starts 1); everyone sees it. Seat of the current auctioneer
  - the table: seasons_done (number, starts 0); everyone sees it. Seasons scored so far
  - the table: current_artist (text, starts ''); everyone sees it. Artist of the card just played (Red, Blue or Green)
  - the table: season_red (number, starts 0); everyone sees it. Red cards played this season
  - the table: season_blue (number, starts 0); everyone sees it. Blue cards played this season
  - the table: season_green (number, starts 0); everyone sees it. Green cards played this season
  - the table: value_red (number, starts 0); everyone sees it. Cumulative value of Red
  - the table: value_blue (number, starts 0); everyone sees it. Cumulative value of Blue
  - the table: value_green (number, starts 0); everyone sees it. Cumulative value of Green
  - the table: deal_roll (number, starts 0); hidden from all players. Random 1-6 that picks which seat gets which hand composition
  - the table: season_ended (bool, starts False); everyone sees it. True when the card just played was the season-ending card
  - the table: winner_seat (number, starts 0); everyone sees it. Seat that won this round's auction
  - the table: price (number, starts 0); everyone sees it. Price paid by this round's auction winner
  - the table: scoring_now (bool, starts False); everyone sees it. True when season scoring happens this round
  - the table: first_artist (text, starts ''); everyone sees it. Artist placed first this season
  - the table: second_artist (text, starts ''); everyone sees it. Artist placed second this season, or empty if none
  - parameters, each kept as a table attribute: player_count = 3, starting_money = 60, hand_size = 7, composition_A_red = 4, composition_A_blue = 2, composition_A_green = 1, composition_B_red = 1, composition_B_blue = 4, composition_B_green = 2, composition_C_red = 2, composition_C_blue = 1, composition_C_green = 4, deal_roll_min = 1, deal_roll_max = 6, season_ending_count = 3, first_place_bonus = 20, second_place_bonus = 10, seasons_to_end = 3, max_rounds = 21, min_bid = 0, first_auctioneer_seat = 1

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seats 1, 2 and 3 each get money 60 and all hand and owned counts at 0. All season counts and cumulative values are 0, seasons_done is 0, and auctioneer is 1.
  2. The engine draws deal_roll uniformly from 1 to 6. This is the only random event in the game.
  3. Compositions are dealt to seats 1, 2 and 3 by deal_roll: 1 gives A,B,C; 2 gives A,C,B; 3 gives B,A,C; 4 gives B,C,A; 5 gives C,A,B; 6 gives C,B,A. A sets hand_red/blue/green to 4/2/1, B sets them to 1/4/2, and C sets them to 2/1/4.
  4. Everyone is told that compositions A, B and C exist and that each seat holds a different one. Each player is sent only their own hand counts (sync).

EACH ROUND (steps in order; the round repeats until an ending):
  1. [sync] all players. What happens: Each player sees their own hand counts and all public state: money, owned counts, season counts, values and auctioneer.
  2. [ask] the seat named by auctioneer answers: one of Red, Blue, Green, limited to artists whose own hand count is above 0. What happens: current_artist := the chosen artist
  3. [update] all players. What happens: The auctioneer's hand_<current_artist> -= 1; season_<current_artist> += 1; season_ended := (season_<current_artist> == 3). Announce: 'Seat {auctioneer} plays {current_artist}.' If season_ended, also announce that the card is discarded unsold.
  4. [poll] all players answers: short text. What happens: when season_ended is false: message := the answer; then broadcast {"to": "all", "text": "Seat {seat} says: {value}"}. The talk is not binding.
  5. [poll] all players answers: whole number from 0 to own money. What happens: when season_ended is false: bid := the answer, hidden until all are in
  6. [update] all players. What happens: when season_ended is false: compute each seat's offset = (seat - auctioneer + 3) mod 3 and key = bid*3 + ((3 - offset) mod 3), so the seat after the auctioneer breaks ties first and the auctioneer last. If the highest bid is 0, winner_seat := auctioneer and price := 0. Otherwise winner_seat := the seat with the highest key and price := that seat's bid. If winner_seat != auctioneer, the winner's money -= price and the auctioneer's money += price. If winner_seat == auctioneer, the auctioneer's money -= price (paid to the bank). The winner's owned_<current_artist> += 1. Announce all three bids, winner_seat and price.
  7. [update] all players. What happens: scoring_now := season_ended OR (sum over players of hand_red+hand_blue+hand_green == 0 AND season_red+season_blue+season_green > 0)
  8. [update] all players. What happens: when scoring_now: first_artist := the artist with the highest season count, ties broken Red > Blue > Green; value_<first_artist> += 20. second_artist := the highest of the other two by season count (same tie order) if its season count > 0, otherwise empty; if not empty, value_<second_artist> += 10. Each player's money += owned_<first_artist>*value_<first_artist> + (owned_<second_artist>*value_<second_artist> if second_artist is not empty). Unplaced artists pay 0. Announce the placings, the new values and each payout.
  9. [update] all players. What happens: when scoring_now: every owned_red, owned_blue and owned_green := 0; season_red, season_blue and season_green := 0; seasons_done += 1
  10. [update] all players. What happens: auctioneer := the next seat after auctioneer in the order 1->2->3->1 whose hand_red+hand_blue+hand_green > 0. If no seat has cards, it is left unchanged.
  11. [check] all players. What happens: End the game if seasons_done >= 3 or the sum over players of hand_red+hand_blue+hand_green == 0; otherwise continue.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. At setup, every player has money 60 and all owned counts 0, every artist has season count 0 and value 0, seasons_done is 0, and auctioneer is seat 1.
  R2. At setup, when deal_roll is 1 the seats 1,2,3 get compositions A,B,C; for 2 they get A,C,B; for 3 B,A,C; for 4 B,C,A; for 5 C,A,B; for 6 C,B,A. A is Red 4, Blue 2, Green 1; B is Red 1, Blue 4, Green 2; C is Red 2, Blue 1, Green 4.
  R3. Each player's hand counts are visible only to that player, and every hand totals 7 cards at setup.
  R4. The auctioneer may choose only an artist for which their own hand count is above 0.
  R5. When the auctioneer plays artist X, their hand_X falls by 1, season_X rises by 1, and current_artist is announced as X.
  R6. When season_X reaches 3 after the play, the card is discarded unsold: there is no talk, no bidding, no money moves and no owned count changes, and season scoring happens.
  R7. When the card is not season-ending, all three players send one short message simultaneously, and all messages are then shown to everyone.
  R8. When the card is not season-ending, all three players including the auctioneer bid simultaneously a whole number from 0 to their current money.
  R9. The highest bid wins the painting; with the auctioneer at seat 1 and bids 15, 15, 15, seat 2 wins at 15.
  R10. When bids tie for highest, the tied seat first in order starting after the auctioneer wins, with the auctioneer last; with the auctioneer at seat 2 and bids seat1=10, seat2=10, seat3=5, seat 1 wins.
  R11. When every bid is 0, the auctioneer wins the painting at price 0.
  R12. When a non-auctioneer wins with bid 12, the winner's money falls by 12 and the auctioneer's money rises by 12.
  R13. When the auctioneer wins with bid 12, the auctioneer's money falls by 12 and no other player's money changes.
  R14. The auction winner's owned count for the current artist rises by 1, including when the winner is the auctioneer.
  R15. After an auction, all three bids, the winner and the price are announced to everyone.
  R16. Season scoring happens when the season-ending card was just played, or when all hands are empty and at least one season count is above 0.
  R17. At scoring, the artist with the highest season count places first, ties broken Red, then Blue, then Green, and its value rises by 20.
  R18. At scoring, the best of the remaining two artists by season count (same tie order) places second only if its season count is above 0, and its value rises by 10.
  R19. At scoring, each player gains, for each placed artist, owned count times that artist's new cumulative value; unplaced artists pay 0 even if their value is above 0. With Red first at value 30 and a player owning 2 Red, that player gains 60 from Red.
  R20. After scoring, all owned counts and season counts reset to 0 and seasons_done rises by 1.
  R21. After each round, the auctioneer passes to the next seat in the order 1->2->3->1, skipping any seat whose hand is empty.
  R22. The game ends when seasons_done reaches 3, or when all hands are empty after any unfinished season has been scored; it lasts at most 21 rounds.
  R23. When the game ends, the player with the most money wins; players tied for the most money share the result (a draw).
  R24. Money and owned counts are public at all times.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Choose a card to auction | asked: the seat named by auctioneer | options: each of Red, Blue, Green for which that seat's own hand count is above 0; never an artist with hand count 0
  - Talk message | asked: all three seats, only when the card played is not season-ending | options: one short free-text message
  - Sealed bid | asked: all three seats including the auctioneer, only when the card played is not season-ending | options: any whole number from 0 up to that seat's current money

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: seasons_done >= 3 OR sum over players of (hand_red + hand_blue + hand_green) == 0
  - each player's standing: you.money (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their money. The player with the most money wins. Players tied for the most money share the result, which the source calls a draw.
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

- each player: `money` (number, visible: public, starts 60): Money held; the score
- each player: `owned_red` (number, visible: public, starts 0): Red paintings bought this season
- each player: `owned_blue` (number, visible: public, starts 0): Blue paintings bought this season
- each player: `owned_green` (number, visible: public, starts 0): Green paintings bought this season
- the table: `auctioneer` (number, visible: public, starts 1): Seat of the current auctioneer
- the table: `seasons_done` (number, visible: public, starts 0): Seasons scored so far
- the table: `current_artist` (text, visible: public, starts ''): Artist of the card just played (Red, Blue or Green)
- the table: `season_red` (number, visible: public, starts 0): Red cards played this season
- the table: `season_blue` (number, visible: public, starts 0): Blue cards played this season
- the table: `season_green` (number, visible: public, starts 0): Green cards played this season
- the table: `value_red` (number, visible: public, starts 0): Cumulative value of Red
- the table: `value_blue` (number, visible: public, starts 0): Cumulative value of Blue
- the table: `value_green` (number, visible: public, starts 0): Cumulative value of Green
- the table: `winner_seat` (number, visible: public, starts 0): Seat that won this round's auction
- the table: `price` (number, visible: public, starts 0): Price paid by this round's auction winner
- parameters (each must be an attribute holding this value, never a number buried in a step): player_count = 3, starting_money = 60, hand_size = 7, composition_A_red = 4, composition_A_blue = 2, composition_A_green = 1, composition_B_red = 1, composition_B_blue = 4, composition_B_green = 2, composition_C_red = 2, composition_C_blue = 1, composition_C_green = 4, deal_roll_min = 1, deal_roll_max = 6, season_ending_count = 3, first_place_bonus = 20, second_place_bonus = 10, seasons_to_end = 3, max_rounds = 21, min_bid = 0, first_auctioneer_seat = 1
- the game ends with ONE ending whose `rank_by` is `you.money`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
    "id": "modern_art_three_studios",
    "name": "Modern Art: Three Studios",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Three dealers take turns auctioning paintings by Red, Blue and Green with sealed bids; the most-played artists pay out each season, and the richest player wins."
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
        "key": "money",
        "visible": "public",
        "type": "number",
        "initial": 60
      },
      {
        "key": "hand_red",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hand_blue",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hand_green",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "owned_red",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "owned_blue",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "owned_green",
        "visible": "public",
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
        "key": "offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "last_payout",
        "visible": "ally",
        "type": "number",
        "initial": 0
      }
    ],
    "game": [
      {
        "key": "auctioneer",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "seasons_done",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "current_artist",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "season_red",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "season_blue",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "season_green",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "value_red",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "value_blue",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "value_green",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "deal_roll",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "season_ended",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "winner_seat",
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
        "key": "scoring_now",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "first_artist",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "second_artist",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "player_count",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "starting_money",
        "visible": "public",
        "type": "number",
        "initial": 60
      },
      {
        "key": "hand_size",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "composition_A_red",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "composition_A_blue",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "composition_A_green",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "composition_B_red",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "composition_B_blue",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "composition_B_green",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "composition_C_red",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "composition_C_blue",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "composition_C_green",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "deal_roll_min",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "deal_roll_max",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "season_ending_count",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "first_place_bonus",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "second_place_bonus",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "seasons_to_end",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "max_rounds",
        "visible": "public",
        "type": "number",
        "initial": 21
      },
      {
        "key": "min_bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "first_auctioneer_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "starting state",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "money",
            "value": {
              "calc": "starting_money"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_red",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_blue",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_green",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "owned_red",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "owned_blue",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "owned_green",
            "value": 0
          }
        },
        {
          "set": {
            "key": "season_red",
            "value": 0
          }
        },
        {
          "set": {
            "key": "season_blue",
            "value": 0
          }
        },
        {
          "set": {
            "key": "season_green",
            "value": 0
          }
        },
        {
          "set": {
            "key": "value_red",
            "value": 0
          }
        },
        {
          "set": {
            "key": "value_blue",
            "value": 0
          }
        },
        {
          "set": {
            "key": "value_green",
            "value": 0
          }
        },
        {
          "set": {
            "key": "seasons_done",
            "value": 0
          }
        },
        {
          "set": {
            "key": "auctioneer",
            "value": {
              "calc": "first_auctioneer_seat"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "the deal roll",
      "do": [
        {
          "set": {
            "key": "deal_roll",
            "value": {
              "calc": "min(deal_roll_max, int(uniform(deal_roll_min, deal_roll_max + 1)))"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "deal the compositions",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "hand_red",
            "value": {
              "calc": "composition_A_red if [['A','B','C'],['A','C','B'],['B','A','C'],['B','C','A'],['C','A','B'],['C','B','A']][deal_roll - 1][you.seat - 1] == 'A' else (composition_B_red if [['A','B','C'],['A','C','B'],['B','A','C'],['B','C','A'],['C','A','B'],['C','B','A']][deal_roll - 1][you.seat - 1] == 'B' else composition_C_red)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_blue",
            "value": {
              "calc": "composition_A_blue if [['A','B','C'],['A','C','B'],['B','A','C'],['B','C','A'],['C','A','B'],['C','B','A']][deal_roll - 1][you.seat - 1] == 'A' else (composition_B_blue if [['A','B','C'],['A','C','B'],['B','A','C'],['B','C','A'],['C','A','B'],['C','B','A']][deal_roll - 1][you.seat - 1] == 'B' else composition_C_blue)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_green",
            "value": {
              "calc": "composition_A_green if [['A','B','C'],['A','C','B'],['B','A','C'],['B','C','A'],['C','A','B'],['C','B','A']][deal_roll - 1][you.seat - 1] == 'A' else (composition_B_green if [['A','B','C'],['A','C','B'],['B','A','C'],['B','C','A'],['C','A','B'],['C','B','A']][deal_roll - 1][you.seat - 1] == 'B' else composition_C_green)"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "label": "the compositions",
      "to": "all",
      "text": "Three hand compositions of {hand_size} cards exist: A is Red {composition_A_red}, Blue {composition_A_blue}, Green {composition_A_green}; B is Red {composition_B_red}, Blue {composition_B_blue}, Green {composition_B_green}; C is Red {composition_C_red}, Blue {composition_C_blue}, Green {composition_C_green}. Each seat holds a different one."
    },
    {
      "use": "sync",
      "label": "your hand",
      "mode": "self",
      "to": "all",
      "fields": [
        "hand_red",
        "hand_blue",
        "hand_green"
      ],
      "text": "Your hand:"
    }
  ],
  "steps": [
    {
      "use": "sync",
      "phase": "play",
      "label": "where you stand",
      "mode": "self",
      "to": "all",
      "text": "Your state:"
    },
    {
      "use": "update",
      "phase": "play",
      "label": "prepare the offer",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "(['Red'] if you.hand_red > 0 else []) + (['Blue'] if you.hand_blue > 0 else []) + (['Green'] if you.hand_green > 0 else [])"
            }
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
            "key": "bid",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "play",
      "label": "choose a card",
      "to": {
        "where": "you.seat == auctioneer"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "chosen"
      },
      "text": "You are the auctioneer. Choose one artist from your hand to play."
    },
    {
      "use": "update",
      "phase": "play",
      "label": "reveal the card",
      "do": [
        {
          "set": {
            "key": "current_artist",
            "value": "$chosen"
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
            "key": "price",
            "value": 0
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "auctioneer"
            },
            "key": "hand_red",
            "value": -1,
            "if": {
              "calc": "$chosen == 'Red'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "auctioneer"
            },
            "key": "hand_blue",
            "value": -1,
            "if": {
              "calc": "$chosen == 'Blue'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "auctioneer"
            },
            "key": "hand_green",
            "value": -1,
            "if": {
              "calc": "$chosen == 'Green'"
            }
          }
        },
        {
          "adjust": {
            "key": "season_red",
            "value": 1,
            "if": {
              "calc": "$chosen == 'Red'"
            }
          }
        },
        {
          "adjust": {
            "key": "season_blue",
            "value": 1,
            "if": {
              "calc": "$chosen == 'Blue'"
            }
          }
        },
        {
          "adjust": {
            "key": "season_green",
            "value": 1,
            "if": {
              "calc": "$chosen == 'Green'"
            }
          }
        },
        {
          "set": {
            "key": "season_ended",
            "value": false
          }
        },
        {
          "set": {
            "key": "season_ended",
            "value": true,
            "if": {
              "calc": "(season_red if $chosen == 'Red' else (season_blue if $chosen == 'Blue' else season_green)) == season_ending_count"
            },
            "text": "That is the season-ending card: it is discarded unsold. No talk, no bidding; the season is scored now."
          }
        }
      ],
      "text": "Seat {auctioneer} plays {current_artist}."
    },
    {
      "use": "poll",
      "phase": "auction",
      "label": "talk",
      "when": {
        "calc": "not season_ended"
      },
      "to": "acting",
      "answer": {
        "type": "text",
        "max_words": 40
      },
      "store": "message",
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} says: {value}"
      },
      "text": "A {current_artist} painting is up for auction. Write one short message to the table. Talk is not binding."
    },
    {
      "use": "poll",
      "phase": "auction",
      "label": "sealed bids",
      "when": {
        "calc": "not season_ended"
      },
      "to": "acting",
      "answer": {
        "type": "number",
        "min": {
          "calc": "min_bid"
        },
        "max": {
          "calc": "you.money"
        }
      },
      "store": "bid",
      "text": "Submit your sealed bid for the {current_artist} painting: a whole number from {min_bid} up to your money. The highest bid wins; ties go to the tied seat first in order after the auctioneer, the auctioneer last; if all bids are 0 the auctioneer takes it free."
    },
    {
      "use": "update",
      "phase": "auction",
      "label": "settle the auction",
      "when": {
        "calc": "not season_ended"
      },
      "do": [
        {
          "set": {
            "key": "winner_seat",
            "value": {
              "calc": "auctioneer if max([p.bid for p in players]) == 0 else sorted([[p.bid * 3 + (3 - (p.seat - auctioneer + 3) % 3) % 3, p.seat] for p in players])[-1][1]"
            }
          }
        },
        {
          "set": {
            "key": "price",
            "value": {
              "calc": "0 if max([p.bid for p in players]) == 0 else max([p.bid for p in players])"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "winner_seat"
            },
            "key": "money",
            "value": {
              "calc": "-price"
            },
            "if": {
              "calc": "price > 0"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "auctioneer"
            },
            "key": "money",
            "value": {
              "calc": "price"
            },
            "if": {
              "calc": "winner_seat != auctioneer and price > 0"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "winner_seat"
            },
            "key": "owned_red",
            "value": 1,
            "if": {
              "calc": "current_artist == 'Red'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "winner_seat"
            },
            "key": "owned_blue",
            "value": 1,
            "if": {
              "calc": "current_artist == 'Blue'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "winner_seat"
            },
            "key": "owned_green",
            "value": 1,
            "if": {
              "calc": "current_artist == 'Green'"
            }
          }
        }
      ],
      "text": "Bids: seat 1 {players[0].bid}, seat 2 {players[1].bid}, seat 3 {players[2].bid}. Seat {winner_seat} wins the {current_artist} painting for {price}."
    },
    {
      "use": "update",
      "phase": "scoring",
      "label": "is the season scored",
      "do": [
        {
          "set": {
            "key": "scoring_now",
            "value": {
              "calc": "season_ended or (sum([p.hand_red + p.hand_blue + p.hand_green for p in players]) == 0 and season_red + season_blue + season_green > 0)"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "scoring",
      "label": "season scoring",
      "when": {
        "calc": "scoring_now"
      },
      "do": [
        {
          "set": {
            "key": "first_artist",
            "value": {
              "calc": "'Red' if season_red >= season_blue and season_red >= season_green else ('Blue' if season_blue >= season_green else 'Green')"
            }
          }
        },
        {
          "set": {
            "key": "second_artist",
            "value": {
              "calc": "('Blue' if season_blue >= season_green else 'Green') if first_artist == 'Red' else (('Red' if season_red >= season_green else 'Green') if first_artist == 'Blue' else ('Red' if season_red >= season_blue else 'Blue'))"
            }
          }
        },
        {
          "set": {
            "key": "second_artist",
            "value": "",
            "if": {
              "calc": "(season_red if second_artist == 'Red' else (season_blue if second_artist == 'Blue' else season_green)) == 0"
            }
          }
        },
        {
          "adjust": {
            "key": "value_red",
            "value": {
              "calc": "first_place_bonus"
            },
            "if": {
              "calc": "first_artist == 'Red'"
            }
          }
        },
        {
          "adjust": {
            "key": "value_blue",
            "value": {
              "calc": "first_place_bonus"
            },
            "if": {
              "calc": "first_artist == 'Blue'"
            }
          }
        },
        {
          "adjust": {
            "key": "value_green",
            "value": {
              "calc": "first_place_bonus"
            },
            "if": {
              "calc": "first_artist == 'Green'"
            }
          }
        },
        {
          "adjust": {
            "key": "value_red",
            "value": {
              "calc": "second_place_bonus"
            },
            "if": {
              "calc": "second_artist == 'Red'"
            }
          }
        },
        {
          "adjust": {
            "key": "value_blue",
            "value": {
              "calc": "second_place_bonus"
            },
            "if": {
              "calc": "second_artist == 'Blue'"
            }
          }
        },
        {
          "adjust": {
            "key": "value_green",
            "value": {
              "calc": "second_place_bonus"
            },
            "if": {
              "calc": "second_artist == 'Green'"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "last_payout",
            "value": {
              "calc": "(you.owned_red * value_red if first_artist == 'Red' or second_artist == 'Red' else 0) + (you.owned_blue * value_blue if first_artist == 'Blue' or second_artist == 'Blue' else 0) + (you.owned_green * value_green if first_artist == 'Green' or second_artist == 'Green' else 0)"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "money",
            "value": {
              "calc": "you.last_payout"
            }
          }
        }
      ],
      "text": "Season scored. First: {first_artist}. Second: {second_artist} (empty means none). Values now Red {value_red}, Blue {value_blue}, Green {value_green}. Payouts: seat 1 {players[0].last_payout}, seat 2 {players[1].last_payout}, seat 3 {players[2].last_payout}."
    },
    {
      "use": "update",
      "phase": "scoring",
      "label": "season reset",
      "when": {
        "calc": "scoring_now"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "owned_red",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "owned_blue",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "owned_green",
            "value": 0
          }
        },
        {
          "set": {
            "key": "season_red",
            "value": 0
          }
        },
        {
          "set": {
            "key": "season_blue",
            "value": 0
          }
        },
        {
          "set": {
            "key": "season_green",
            "value": 0
          }
        },
        {
          "adjust": {
            "key": "seasons_done",
            "value": 1
          }
        }
      ],
      "text": "All owned paintings and season counts reset. Seasons done: {seasons_done}."
    },
    {
      "use": "update",
      "phase": "pass",
      "label": "pass the role",
      "do": [
        {
          "set": {
            "key": "auctioneer",
            "value": {
              "calc": "auctioneer % 3 + 1 if sum([p.hand_red + p.hand_blue + p.hand_green for p in players if p.seat == auctioneer % 3 + 1]) > 0 else ((auctioneer + 1) % 3 + 1 if sum([p.hand_red + p.hand_blue + p.hand_green for p in players if p.seat == (auctioneer + 1) % 3 + 1]) > 0 else auctioneer)"
            }
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "pass",
      "label": "is it over",
      "when": {
        "calc": "seasons_done >= seasons_to_end or sum([p.hand_red + p.hand_blue + p.hand_green for p in players]) == 0"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "seasons_done >= seasons_to_end or sum([p.hand_red + p.hand_blue + p.hand_green for p in players]) == 0"
      },
      "rank_by": "you.money",
      "text": "Winner: {result}. Final money: Seat 1 {players[0].money}, Seat 2 {players[1].money}, Seat 3 {players[2].money}."
    }
  },
  "limits": {
    "rounds": 21,
    "rounds_max": 21,
    "actions_max": 400,
    "deadline_s": 120
  },
  "rules": "Three players (seats 1, 2 and 3) deal paintings by three artists: Red, Blue and Green. Each player starts with {starting_money} money. Money is public at all times. Seat {first_auctioneer_seat} is the first auctioneer.\n\nHands: there are three hand compositions of {hand_size} cards each. A is {composition_A_red} Red, {composition_A_blue} Blue, {composition_A_green} Green. B is {composition_B_red} Red, {composition_B_blue} Blue, {composition_B_green} Green. C is {composition_C_red} Red, {composition_C_blue} Blue, {composition_C_green} Green. At setup one random whole number from {deal_roll_min} to {deal_roll_max} gives compositions to seats 1, 2, 3: 1 gives A,B,C; 2 gives A,C,B; 3 gives B,A,C; 4 gives B,C,A; 5 gives C,A,B; 6 gives C,B,A. Each player sees only their own hand counts; each player has a different composition. This is the only random event in the game.\n\nEach round:\n1. Choose a card: the auctioneer chooses one artist for which their hand count is above 0.\n2. Reveal: the chosen artist is announced as the current artist. The auctioneer's hand count for it falls by 1 and that artist's season count rises by 1.\n3. Season-ending card: if that artist's season count is now {season_ending_count}, the card is discarded unsold: no talk, no bidding, no money moves, no paintings change hands, and the season is scored now. Otherwise the auction goes ahead.\n4. Talk: otherwise, all three players each write one short message at the same moment; all are shown to everyone. Talk is not binding.\n5. Sealed bids: otherwise, all three players, the auctioneer included, bid at the same moment a whole number from {min_bid} up to their current money. The highest bid wins. If bids tie for highest, the tied player who comes first in seat order starting from the seat after the auctioneer wins, with the auctioneer last. If every bid is 0, the auctioneer wins at price 0.\n6. Settle: if the winner is not the auctioneer, the winner pays their bid to the auctioneer. If the winner is the auctioneer, they pay their bid to the bank (nothing if 0). In every case the winner's owned count for the current artist rises by 1; paintings the auctioneer keeps score like any other. All three bids, the winner and the price are announced. Owned counts are public.\n7. Season scoring happens if the season-ending card was just played, or if all hands are now empty and at least one season count is above 0. First place is the artist with the highest season count (ties broken Red, Blue, Green); its cumulative value rises by {first_place_bonus}. Second place is the highest of the other two by season count (same tie order), only if its season count is above 0; its value rises by {second_place_bonus}. The third artist, and any artist with season count 0, does not place. Each player receives from the bank, for each placed artist, their owned count times that artist's cumulative value. Unplaced artists pay 0, even if their value is above 0 from earlier seasons. Placings, new values and payouts are announced. Then all owned counts and season counts reset to 0 and one more season is done.\n8. Pass the role: the auctioneer role passes to the next seat (1 to 2, 2 to 3, 3 to 1), skipping any seat whose hand is empty.\n\nEnd: the game ends when {seasons_to_end} seasons are done, or when all hands are empty (after any unfinished season is scored). It lasts at most {max_rounds} rounds. The player with the most money wins; players tied for the most money share the result (a draw)."
}
```
````
