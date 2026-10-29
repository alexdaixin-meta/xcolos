# Task: write the XColos game file for "Modern Art: Sealed Season"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 4; set `meta.players` to {"min": 3, "max": 4, "suggested": 4} (the suggested size is the one the game plays best at).

COMPONENTS
- A deck of 46 painting cards by four artists: Red 10 cards, Blue 11, Green 12, Yellow 13.
- Artist order, used for ties: Red, then Blue, then Green, then Yellow.
- Each artist has a cumulative value, starting at 0.

SETUP
- Each player starts with 100 money. Money is private: only its owner sees it.
- Shuffle the deck. Deal each player a private hand: 10 cards with 3 players, 8 cards with 4 players. The rest of the deck is unused.
- Seat order is random. The first player in seat order is the first auctioneer.
- The season number starts at 1. Every artist's season count starts at 0.

EACH ROUND (ONE AUCTION)
1. Choose (auctioneer only). The auctioneer secretly chooses one card from their hand and a reserve price, a whole number from 0 up to their current money.
2. Reveal. The chosen card leaves the auctioneer's hand. Its artist is announced to all, and that artist's season count goes up by 1.
3. Season-end check. If that artist's season count is now 4, the card is discarded unsold and the reserve is ignored. Skip steps 4 to 7 and go to step 8, season scoring. Otherwise, announce the reserve to everyone.
4. Talk. Every player (auctioneer included) writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Messages are not binding.
5. Bid. Every player except the auctioneer submits a sealed bid at the same moment. A bid is a whole number from 0 up to the bidder's current money.
6. Resolve. The winner is the highest bid that is at least the reserve. If bids tie, the tied bidder who comes first in seat order after the auctioneer wins. The winner pays the bid to the auctioneer and takes the painting face-up in front of them.
   - If no bid reaches the reserve, the auctioneer must buy the painting. They pay the reserve to the bank (the money leaves the game) and take the painting.
7. Announce. All bids, the buyer and the price are announced publicly.
8. Season scoring. This step happens only if the season ended in step 3, or if every hand is now empty.
   a. Rank the four artists by season count, highest first. Ties go to the artist earlier in artist order.
   b. Add 30 to the cumulative value of the first-ranked artist and 20 to the second-ranked artist. If the second-ranked artist has a season count of 0, it gets nothing.
   c. Each player receives, for every face-up painting they own of the two ranked artists, money equal to that artist's cumulative value after step b. Paintings of the other two artists pay nothing, even if those artists scored in earlier seasons.
   d. Discard all face-up paintings. Reset every artist's season count to 0. Add 1 to the season number.
9. End check. The game ends after the third season scoring, or when every hand is empty (that final season is scored in step 8 first).
10. Rotate. The auctioneer passes to the next player in seat order who still holds at least one card. Any player with no cards is skipped as auctioneer but still bids.

LIMITS
- Money can never go below 0. Bids and reserves cannot exceed the player's current money.
- The game has at most 32 rounds.

How the winner is decided: When the game ends, each player's money is revealed. The player with the most money wins. If two or more players tie for the most, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Modern Art: Sealed Season (3 to 4 players, best with 4)

Players auction paintings from their hands with a secret reserve and sealed bids, while trying to make the artists they own the most-played in each season, which raises those artists' value; most money after three seasons wins.

STATE (every item below must exist in the file):
  - each player: money (number, starts 100); only its owner sees it. The player's money, private to its owner until the end. This is the score.
  - each player: hand (list, starts []); only its owner sees it. Painting cards in hand, each an artist name (red, blue, green, yellow).
  - each player: paintings (list, starts []); everyone sees it. Face-up paintings bought this season, each an artist name.
  - each player: chosen_card (text, starts ''); only its owner sees it. The card the auctioneer secretly chose this round.
  - each player: reserve_choice (number, starts 0); only its owner sees it. The reserve price the auctioneer secretly chose this round.
  - each player: bid (number, starts 0); only its owner sees it. This round's sealed bid. It stays hidden until the announce step.
  - the table: deck (list, starts '10 red, 11 blue, 12 green, 13 yellow'); hidden from all players. The shuffled deck that hands are dealt from. The rest is unused.
  - the table: auctioneer (number, starts 1); everyone sees it. Seat number of the current auctioneer.
  - the table: current_artist (text, starts ''); everyone sees it. The artist of the card revealed this round.
  - the table: reserve (number, starts 0); everyone sees it. The announced reserve price for this round.
  - the table: season_ended (bool, starts False); everyone sees it. True when the revealed card brought its artist's season count to 4.
  - the table: count_red (number, starts 0); everyone sees it. Red's season count.
  - the table: count_blue (number, starts 0); everyone sees it. Blue's season count.
  - the table: count_green (number, starts 0); everyone sees it. Green's season count.
  - the table: count_yellow (number, starts 0); everyone sees it. Yellow's season count.
  - the table: value_red (number, starts 0); everyone sees it. Red's cumulative value.
  - the table: value_blue (number, starts 0); everyone sees it. Blue's cumulative value.
  - the table: value_green (number, starts 0); everyone sees it. Green's cumulative value.
  - the table: value_yellow (number, starts 0); everyone sees it. Yellow's cumulative value.
  - the table: season (number, starts 1); everyone sees it. The current season number.
  - the table: seasons_scored (number, starts 0); everyone sees it. How many season scorings have happened.
  - the table: buyer (number, starts 0); everyone sees it. Seat that took this round's painting (0 if none).
  - the table: price (number, starts 0); everyone sees it. Price paid for this round's painting.
  - the table: round_number (number, starts 0); everyone sees it. Number of auctions started.
  - parameters, each kept as a table attribute: starting_money = 100, deck_size = 46, red_cards = 10, blue_cards = 11, green_cards = 12, yellow_cards = 13, hand_size_3_players = 10, hand_size_4_players = 8, season_end_count = 4, first_place_award = 30, second_place_award = 20, seasons_to_end = 3, max_rounds = 32, min_reserve = 0, min_bid = 0, artist_tiebreak_red = 3, artist_tiebreak_blue = 2, artist_tiebreak_green = 1, artist_tiebreak_yellow = 0

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seats are assigned in random order; seat 1 is the first auctioneer (auctioneer = 1).
  2. Every player's money is set to 100.
  3. The deck list is filled with 10 red, 11 blue, 12 green and 13 yellow cards.
  4. Each player draws cards at random from deck into hand: 10 each with 3 players, 8 each with 4 players. The remaining deck is unused.
  5. season = 1, seasons_scored = 0, and every count_<artist> and value_<artist> = 0.
  6. Each player is synced their own money and hand.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] engine. What happens: round_number += 1; season_ended = false; buyer = 0; price = 0; every player's bid = 0.
  2. [ask] seat auctioneer answers: one artist name present in own hand. What happens: auctioneer.chosen_card = answer (kept secret).
  3. [ask] seat auctioneer answers: whole number from 0 to auctioneer.money. What happens: auctioneer.reserve_choice = answer (kept secret).
  4. [update] engine. What happens: Remove one copy of auctioneer.chosen_card from auctioneer.hand; current_artist = chosen_card; count_<current_artist> += 1; season_ended = (count_<current_artist> == 4). Announce the artist to all.
  5. [update] engine. What happens: When season_ended is false: reserve = auctioneer.reserve_choice and the reserve is announced to all. When season_ended is true: announce that the card is discarded unsold and the season ends (the reserve is ignored).
  6. [poll] all players (when season_ended is false) answers: one short text message. What happens: Messages are broadcast to all: {"to": "all", "text": "Seat {seat} says: {value}"}. They are not binding.
  7. [poll] all players except the auctioneer (when season_ended is false) answers: whole number from 0 to own money. What happens: Each bidder's bid = answer, hidden until all bids are in.
  8. [update] engine. What happens: When season_ended is false: the eligible bids are those with bid >= reserve. If any exist, buyer = the highest eligible bidder, with ties going to the tied seat that comes first in seat order after the auctioneer; price = buyer.bid; buyer.money -= price; auctioneer.money += price; append current_artist to buyer.paintings. Otherwise buyer = auctioneer; price = reserve; auctioneer.money -= reserve (the money leaves the game); append current_artist to auctioneer.paintings.
  9. [tell] all players (when season_ended is false). What happens: Announce every bidder's bid, the buyer and the price.
  10. [update] engine. What happens: When season_ended is true or the sum of hand sizes == 0, score the season. (a) Each artist's key = count*4 + tiebreak (red 3, blue 2, green 1, yellow 0); first = the highest key, second = the next highest. (b) value_<first> += 30; if count_<second> > 0 then value_<second> += 20, otherwise second scores nothing. (c) Each player's money += value_<first> times the number of first in paintings, plus (if count_<second> > 0) value_<second> times the number of second in paintings. (d) Every paintings list is emptied; every count_<artist> = 0; season += 1; seasons_scored += 1. Announce the new values and payouts.
  11. [check] engine. What happens: End the game if seasons_scored >= 3, or the sum of hand sizes == 0, or round_number >= 32; otherwise continue.
  12. [update] engine. What happens: auctioneer = the next seat in seat order after the current auctioneer whose hand is not empty. Seats with empty hands are skipped as auctioneer but still bid.
  13. [sync] all players. What happens: Each player is sent their own money and hand, plus the public state.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, then every player has 100 money, visible only to its owner.
  R2. When there are 3 players, then each is dealt 10 cards; when there are 4 players, then each is dealt 8 cards, from a 46-card deck of 10 red, 11 blue, 12 green and 13 yellow.
  R3. When a round begins, then the auctioneer secretly picks one card from their hand and a reserve from 0 to their current money.
  R4. When the card is revealed, then it leaves the auctioneer's hand, its artist is announced, and that artist's season count rises by 1.
  R5. When the revealed card brings its artist's season count to 4, then the card is discarded unsold, the reserve is ignored, there is no talk or bidding, and season scoring happens.
  R6. When the season does not end on the reveal, then the reserve is announced to everyone.
  R7. When the season does not end on the reveal, then every player including the auctioneer submits one short message simultaneously, and all messages are shown to everyone.
  R8. When bidding happens, then every player except the auctioneer submits a sealed bid from 0 to their own current money, simultaneously.
  R9. When at least one bid is >= the reserve, then the highest such bidder pays their bid to the auctioneer and appends the painting to their paintings.
  R10. When the highest eligible bids tie, then the tied bidder first in seat order after the auctioneer wins.
  R11. When no bid reaches the reserve, then the auctioneer pays the reserve to the bank (money leaves the game) and takes the painting.
  R12. When an auction resolves, then all bids, the buyer and the price are announced publicly.
  R13. When season scoring happens, then artists are ranked by season count with ties to the earlier of red, blue, green, yellow; the first gains 30 cumulative value and the second gains 20 unless its count is 0.
  R14. When season scoring happens, then each player gains, for each painting they own of a ranked artist, that artist's cumulative value after the increase; paintings of unranked artists pay 0.
  R15. When season scoring finishes, then all paintings are discarded, all season counts reset to 0, and the season number rises by 1.
  R16. When every hand is empty after an auction, then the current season is scored and the game ends.
  R17. When the third season scoring is done, then the game ends.
  R18. When the game would pass 32 rounds, then it ends.
  R19. When the auctioneer rotates, then it passes to the next seat in order holding at least one card; empty-handed players still bid.
  R20. When the game ends, then the player with the most money wins, and players tied for most share the result.
  R21. Money never goes below 0, because bids and reserves are capped at the player's current money.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Auctioneer chooses a card | asked: the auctioneer | options: each distinct artist name (red, blue, green, yellow) that appears at least once in the auctioneer's hand
  - Auctioneer chooses a reserve | asked: the auctioneer | options: any whole number from 0 to the auctioneer's current money
  - Talk | asked: every seat including the auctioneer, only when the season did not end on the reveal | options: one short free-text message
  - Sealed bid | asked: every seat except the auctioneer, including empty-handed seats, only when the season did not end on the reveal | options: any whole number from 0 to that seat's current money

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: seasons_scored >= 3 or sum over players of size(hand) == 0 or round_number >= 32
  - each player's standing: you.money (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their final money; it is revealed at the end and the most money wins. Players tied at the top share the win (the source calls this a draw).
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

- each player: `money` (number, visible: ally, starts 100): The player's money, private to its owner until the end. This is the score.
- each player: `paintings` (list, visible: public, starts []): Face-up paintings bought this season, each an artist name.
- the table: `auctioneer` (number, visible: public, starts 1): Seat number of the current auctioneer.
- the table: `current_artist` (text, visible: public, starts ''): The artist of the card revealed this round.
- the table: `reserve` (number, visible: public, starts 0): The announced reserve price for this round.
- the table: `count_red` (number, visible: public, starts 0): Red's season count.
- the table: `count_blue` (number, visible: public, starts 0): Blue's season count.
- the table: `count_green` (number, visible: public, starts 0): Green's season count.
- the table: `count_yellow` (number, visible: public, starts 0): Yellow's season count.
- the table: `value_red` (number, visible: public, starts 0): Red's cumulative value.
- the table: `value_blue` (number, visible: public, starts 0): Blue's cumulative value.
- the table: `value_green` (number, visible: public, starts 0): Green's cumulative value.
- the table: `value_yellow` (number, visible: public, starts 0): Yellow's cumulative value.
- the table: `season` (number, visible: public, starts 1): The current season number.
- the table: `seasons_scored` (number, visible: public, starts 0): How many season scorings have happened.
- the table: `buyer` (number, visible: public, starts 0): Seat that took this round's painting (0 if none).
- the table: `price` (number, visible: public, starts 0): Price paid for this round's painting.
- parameters (each must be an attribute holding this value, never a number buried in a step): starting_money = 100, deck_size = 46, red_cards = 10, blue_cards = 11, green_cards = 12, yellow_cards = 13, hand_size_3_players = 10, hand_size_4_players = 8, season_end_count = 4, first_place_award = 30, second_place_award = 20, seasons_to_end = 3, max_rounds = 32, min_reserve = 0, min_bid = 0, artist_tiebreak_red = 3, artist_tiebreak_blue = 2, artist_tiebreak_green = 1, artist_tiebreak_yellow = 0
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

## Guidance from the last attempt

The previous attempt had problems:

1. Make the auctioneer's reserve a real choice put to the auctioneer seat only, offering every whole number from `min_reserve` (0) up to that seat's current `money` inclusive, so 0 and 100 are both offered at 100 money. Use a parameter attribute for the minimum, not a literal.
2. After the choice, copy the chosen reserve into the table `reserve` in the not-season-ending branch, guarded with `when`/`if` on the season-end check, so it is announced. Do not leave `reserve` at its default 0.
3. Make sure the card choice and the reserve choice are two separate prompts to the auctioneer in that order.
4. Increment the matching `count_*` from the chosen card and remove that card from the auctioneer's hand.
5. When the season count reaches `season_end_count`, skip talk and bidding and go straight to scoring.
6. When a scenario supplies starting hands, do not deal over them, so the given hands are used as given.
