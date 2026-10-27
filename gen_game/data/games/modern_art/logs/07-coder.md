# 07 coder

- time: 2026-10-27T18:20:16+00:00 (107.9s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 0acc1ce04ad6dd70, reply sha256 ce6c5838bf0a55f7

## Sent

````
# Task: write the XColos game file for "Modern Art: Sealed Gallery"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 4 to 4; set `meta.players` to {"min": 4, "max": 4, "suggested": 4} (the suggested size is the one the game plays best at).

SETUP: The deck has 36 painting cards: 14 by artist Amber, 12 by Blue, 10 by Crimson. Shuffle it and deal 9 cards to each of the 4 players as a hidden hand. Each player starts with 100 money, known only to them, though all payments are announced. Every artist starts with a cumulative value of 0. Seats are numbered 1-4, and seat 1 is the first auctioneer.

TURN (one engine round):
1) Announce the turn and the auctioneer.
2) The auctioneer chooses one card from their hand and reveals it. If the auctioneer has no cards, the turn passes to the next seat. This cannot happen in practice, because at most 30 cards are ever played.
3) The card leaves the hand, and that artist's played-this-season count goes up by 1.
4) If that count is now 4, the season ends. This card is not auctioned and no one owns it. Go to SEASON END.
5) Otherwise, there is talk. Every player writes one short message at the same time without seeing the others. All messages are then shown. Talk binds no one.
6) There is a sealed bid. All 4 players, auctioneer included, at the same time submit a whole-number bid from 0 up to their current money.
7) The highest bid wins. Ties are broken in favour of the auctioneer, then in seat order clockwise from the auctioneer. If every bid is 0, the auctioneer gets the card free.
8) A non-auctioneer winner pays their bid to the auctioneer. An auctioneer who wins pays their bid to the bank.
9) The winner adds the painting to their owned paintings of that artist. All bids, the buyer and the price are announced.
10) The auctioneer role passes to the next seat.

SEASON END:
a) Rank the artists by played-this-season count. Ties go to the rarer artist: Crimson beats Blue, and Blue beats Amber.
b) The first artist's cumulative value rises by 30. The second's rises by 20. The third gains nothing.
c) Each player receives, from the bank, (number of owned paintings of the first artist × its cumulative value) plus (number of owned paintings of the second artist × its cumulative value). Paintings of the third artist pay nothing this season, even if that artist has a cumulative value from earlier seasons.
d) All owned paintings are discarded, and all played-this-season counts reset to 0. Payouts are announced. Unplayed cards stay in hands.
e) The season count goes up by 1. If it is 3, the game ends. Otherwise the auctioneer role passes to the next seat and play continues.

GAME END: The game ends after the third season. At most 30 turns are possible.

How the winner is decided: After season 3, the player with the most money wins. If two or more players tie for most money, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Modern Art: Sealed Gallery (4 to 4 players, best with 4)

Four art dealers take turns putting paintings by three artists up for sealed-bid auction. Each season ends when an artist's fourth painting appears, and the season's top two artists pay their owners. After three seasons the most money wins.

STATE (every item below must exist in the file):
  - each player: money (number, starts 100); only its owner sees it. The player's money. It is known only to the owner, but every payment is announced.
  - each player: hand (list, starts []); only its owner sees it. Hidden hand of painting cards, each one 'Amber', 'Blue' or 'Crimson'. Dealt 9 at setup.
  - each player: owned_amber (number, starts 0); everyone sees it. Amber paintings bought this season.
  - each player: owned_blue (number, starts 0); everyone sees it. Blue paintings bought this season.
  - each player: owned_crimson (number, starts 0); everyone sees it. Crimson paintings bought this season.
  - each player: message (text, starts ''); everyone sees it. This turn's talk message.
  - each player: bid (number, starts 0); only its owner sees it. This turn's sealed bid. All bids are announced after the auction.
  - the table: deck (list, starts "14 x 'Amber', 12 x 'Blue', 10 x 'Crimson'"); hidden from all players. The shuffled painting deck. It is empty after the deal.
  - the table: auctioneer (number, starts 1); everyone sees it. Seat of the current auctioneer.
  - the table: current_card (text, starts ''); everyone sees it. The artist of the painting revealed this turn.
  - the table: played_amber (number, starts 0); everyone sees it. Amber cards played this season.
  - the table: played_blue (number, starts 0); everyone sees it. Blue cards played this season.
  - the table: played_crimson (number, starts 0); everyone sees it. Crimson cards played this season.
  - the table: value_amber (number, starts 0); everyone sees it. Amber's cumulative value.
  - the table: value_blue (number, starts 0); everyone sees it. Blue's cumulative value.
  - the table: value_crimson (number, starts 0); everyone sees it. Crimson's cumulative value.
  - the table: season_ending (bool, starts False); everyone sees it. True when this turn's card was the 4th of its artist this season.
  - the table: winner_seat (number, starts 0); everyone sees it. The seat that won this turn's auction.
  - the table: price (number, starts 0); everyone sees it. The winning bid this turn.
  - the table: first_artist (text, starts ''); everyone sees it. The top-ranked artist at season end.
  - the table: second_artist (text, starts ''); everyone sees it. The second-ranked artist at season end.
  - the table: season (number, starts 0); everyone sees it. The number of seasons completed.
  - parameters, each kept as a table attribute: player_count = 4, deck_size = 36, amber_cards = 14, blue_cards = 12, crimson_cards = 10, hand_size = 9, starting_money = 100, season_end_count = 4, first_artist_gain = 30, second_artist_gain = 20, third_artist_gain = 0, seasons = 3, max_turns = 30, min_bid = 0, rarity_amber = 1, rarity_blue = 2, rarity_crimson = 3

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Fill the deck with 14 'Amber', 12 'Blue' and 10 'Crimson' cards (36 in total).
  2. Deal 9 cards to each of the 4 players. Each deal is a random draw from the deck, appended to that player's hand and removed from the deck.
  3. Set each player's money to 100, all owned and played counts to 0, all artist values to 0, and season to 0.
  4. Set auctioneer to seat 1.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [tell] all players. What happens: Announce the season (season + 1) and that seat {auctioneer} is the auctioneer.
  2. [ask] the seat equal to auctioneer answers: one artist name that appears in their hand: Amber, Blue or Crimson. What happens: Set current_card to the answer and reveal it to all.
  3. [update] the auctioneer. What happens: Remove one copy of current_card from the auctioneer's hand. Add 1 to played_<current_card>. Set season_ending = (played_<current_card> == 4). Announce the card and its new count.
  4. [tell] all players. What happens: When season_ending: announce that the 4th {current_card} ends the season, that the card is not auctioned, and that no one owns it.
  5. [poll] all players answers: a short text message. What happens: When not season_ending: store each answer in message, then broadcast {"to": "all", "text": "Seat {seat} says: {value}"}. Talk binds no one.
  6. [poll] all players answers: a whole number from 0 to the player's money. What happens: When not season_ending: store each answer in bid. No one sees a bid until all are in.
  7. [update] all players. What happens: When not season_ending: work out key = bid * 10 + (4 - ((seat - auctioneer + 4) mod 4)) for each player. Set winner_seat to the seat with the highest key, and price to that seat's bid. This breaks ties toward the auctioneer, then clockwise, and gives the card to the auctioneer free if every bid is 0.
  8. [update] winner_seat and auctioneer. What happens: When not season_ending: winner_seat's money -= price. If winner_seat != auctioneer, the auctioneer's money += price; otherwise the price goes to the bank. winner_seat's owned_<current_card> += 1. Announce all bids, the buyer and the price.
  9. [update] the table. What happens: When season_ending: give each artist the key played * 10 + rarity (Amber 1, Blue 2, Crimson 3). first_artist = the highest key and second_artist = the middle key. value_<first_artist> += 30 and value_<second_artist> += 20. Announce the ranking and the values.
  10. [update] all players. What happens: When season_ending: each player's money += owned_<first_artist> * value_<first_artist> + owned_<second_artist> * value_<second_artist>, paid by the bank. Announce each payout.
  11. [update] all players and the table. What happens: When season_ending: set every owned_amber, owned_blue and owned_crimson to 0 and every played_amber, played_blue and played_crimson to 0. season += 1. Set season_ending to false. Hands are untouched.
  12. [update] the table. What happens: auctioneer = (auctioneer mod 4) + 1.
  13. [check] the table. What happens: If season == 3, end the game; otherwise continue.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game is set up, the deck holds 14 Amber, 12 Blue and 10 Crimson cards, each player is dealt 9 hidden cards, each player has 100 money, and every artist value is 0.
  R2. When a turn begins, the seat equal to auctioneer chooses one card from its own hand, and that card is removed from the hand and revealed.
  R3. When a card of an artist is revealed, that artist's played-this-season count rises by 1.
  R4. When a revealed card makes its artist's count 4, the card is not auctioned, no player's owned count changes, and the season ends.
  R5. When a card is auctioned, every player first sends one talk message at the same time, and all messages are then shown to everyone.
  R6. When a card is auctioned, all 4 players, the auctioneer included, bid at the same time a whole number from 0 up to their current money.
  R7. When bids are in, the highest bid wins the card.
  R8. When bids tie for highest, the auctioneer wins if tied, otherwise the tied seat first clockwise from the auctioneer wins.
  R9. When every bid is 0, the auctioneer gets the card for 0.
  R10. When a non-auctioneer wins with a bid of X, the winner's money falls by X and the auctioneer's money rises by X.
  R11. When the auctioneer wins with a bid of X, the auctioneer's money falls by X and no player receives it.
  R12. When a player wins an auction, that player's owned count for the card's artist rises by 1, and all bids, the buyer and the price are announced.
  R13. When a season ends, artists rank by played-this-season count, and ties go to the rarer artist: Crimson beats Blue, and Blue beats Amber.
  R14. When a season ends, the first artist's value rises by 30, the second's by 20, and the third's by 0.
  R15. When a season ends, each player receives from the bank owned(first) * value(first) + owned(second) * value(second), and the third artist pays nothing even if its value is above 0.
  R16. When season payouts are done, all owned counts and played counts reset to 0, hands keep their unplayed cards, and season rises by 1.
  R17. When a turn ends, whether or not a season ended, the auctioneer passes to the next seat (4 passes to 1).
  R18. When season reaches 3, the game ends, and the player with the most money wins, with tied leaders drawing.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Choose a card to reveal | asked: the auctioneer only | options: each distinct artist name (Amber, Blue, Crimson) that appears at least once in the auctioneer's hand; no other seat is asked
  - Talk message | asked: all 4 seats, only when the card is being auctioned | options: any short text
  - Sealed bid | asked: all 4 seats, only when the card is being auctioned | options: a whole number from 0 to that seat's current money

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: season == 3
  - each player's standing: you.money (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: After season 3, the player with the most money wins. Players tied for the most money share the result, which is a draw among them.
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

- each player: `money` (number, visible: ally, starts 100): The player's money. It is known only to the owner, but every payment is announced.
- each player: `owned_amber` (number, visible: public, starts 0): Amber paintings bought this season.
- each player: `owned_blue` (number, visible: public, starts 0): Blue paintings bought this season.
- each player: `owned_crimson` (number, visible: public, starts 0): Crimson paintings bought this season.
- the table: `auctioneer` (number, visible: public, starts 1): Seat of the current auctioneer.
- the table: `played_amber` (number, visible: public, starts 0): Amber cards played this season.
- the table: `played_blue` (number, visible: public, starts 0): Blue cards played this season.
- the table: `played_crimson` (number, visible: public, starts 0): Crimson cards played this season.
- the table: `value_amber` (number, visible: public, starts 0): Amber's cumulative value.
- the table: `value_blue` (number, visible: public, starts 0): Blue's cumulative value.
- the table: `value_crimson` (number, visible: public, starts 0): Crimson's cumulative value.
- the table: `season` (number, visible: public, starts 0): The number of seasons completed.
- parameters (each must be an attribute holding this value, never a number buried in a step): player_count = 4, deck_size = 36, amber_cards = 14, blue_cards = 12, crimson_cards = 10, hand_size = 9, starting_money = 100, season_end_count = 4, first_artist_gain = 30, second_artist_gain = 20, third_artist_gain = 0, seasons = 3, max_turns = 30, min_bid = 0, rarity_amber = 1, rarity_blue = 2, rarity_crimson = 3
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
    "id": "modern_art_sealed_gallery",
    "name": "Modern Art: Sealed Gallery",
    "players": {
      "min": 4,
      "max": 4,
      "suggested": 4
    },
    "blurb": "Four dealers auction paintings by three artists in sealed bids; over three seasons the top artists pay their owners, and the most money wins."
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
        "visible": "ally",
        "type": "number",
        "initial": 100
      },
      {
        "key": "hand",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "owned_amber",
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
        "key": "owned_crimson",
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
        "key": "bid",
        "visible": "ally",
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
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": [
          "Amber", "Amber", "Amber", "Amber", "Amber", "Amber", "Amber",
          "Amber", "Amber", "Amber", "Amber", "Amber", "Amber", "Amber",
          "Blue", "Blue", "Blue", "Blue", "Blue", "Blue",
          "Blue", "Blue", "Blue", "Blue", "Blue", "Blue",
          "Crimson", "Crimson", "Crimson", "Crimson", "Crimson",
          "Crimson", "Crimson", "Crimson", "Crimson", "Crimson"
        ]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "auctioneer",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "current_card",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "played_amber",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "played_blue",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "played_crimson",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "value_amber",
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
        "key": "value_crimson",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "season_ending",
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
        "key": "season",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "player_count",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 36
      },
      {
        "key": "amber_cards",
        "visible": "public",
        "type": "number",
        "initial": 14
      },
      {
        "key": "blue_cards",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "crimson_cards",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "hand_size",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "starting_money",
        "visible": "public",
        "type": "number",
        "initial": 100
      },
      {
        "key": "season_end_count",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "first_artist_gain",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "second_artist_gain",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "third_artist_gain",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "seasons",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "max_turns",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "min_bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "rarity_amber",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "rarity_blue",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "rarity_crimson",
        "visible": "public",
        "type": "number",
        "initial": 3
      }
    ]
  },
  "rules": "The deck has {deck_size} painting cards: {amber_cards} by artist Amber, {blue_cards} by Blue, {crimson_cards} by Crimson. It is shuffled and {hand_size} cards are dealt to each of the {player_count} players as a hidden hand. Each player starts with {starting_money} money, known only to them, though all payments are announced. Every artist starts with a cumulative value of 0. Seats are numbered 1-4, and seat 1 is the first auctioneer.\n\nEACH TURN: The auctioneer chooses one card from their hand and reveals it. You are offered only the artists you actually hold. The card leaves the hand, and that artist's played-this-season count goes up by 1.\n\nIf that count is now {season_end_count}, the season ends: this card is not auctioned, no one owns it, and nobody talks or bids this turn. Otherwise the card is auctioned: first there is talk, where every player writes one short message at the same time without seeing the others; all messages are then shown. Talk binds no one. Then there is a sealed bid: all {player_count} players, auctioneer included, at the same time submit a whole-number bid from {min_bid} up to their current money.\n\nThe highest bid wins. Ties are broken in favour of the auctioneer, then in seat order clockwise from the auctioneer. If every bid is 0, the auctioneer gets the card free. A non-auctioneer winner pays their bid to the auctioneer. An auctioneer who wins pays their bid to the bank, and no player receives it. The winner adds the painting to their owned paintings of that artist. All bids, the buyer and the price are announced.\n\nSEASON END: Rank the artists by played-this-season count. Ties go to the rarer artist: Crimson beats Blue, and Blue beats Amber. The first artist's cumulative value rises by {first_artist_gain}, the second's by {second_artist_gain}, the third's by {third_artist_gain}. Each player receives from the bank (owned paintings of the first artist x its cumulative value) plus (owned paintings of the second artist x its cumulative value). Paintings of the third artist pay nothing this season, even if that artist has a cumulative value from earlier seasons. Then all owned paintings are discarded and all played-this-season counts reset to 0. Payouts are announced. Unplayed cards stay in hands. The season count goes up by 1.\n\nAt the end of every turn, whether or not a season ended, the auctioneer role passes to the next seat (seat 4 passes to seat 1).\n\nGAME END: The game ends after season {seasons} (at most {max_turns} turns). The player with the most money wins. If two or more players tie for most money, they share the result as a draw.",
  "setup": [
    {
      "use": "update",
      "label": "set up the table",
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
            "key": "owned_amber",
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
            "key": "owned_crimson",
            "value": 0
          }
        },
        {
          "set": {
            "key": "played_amber",
            "value": 0
          }
        },
        {
          "set": {
            "key": "played_blue",
            "value": 0
          }
        },
        {
          "set": {
            "key": "played_crimson",
            "value": 0
          }
        },
        {
          "set": {
            "key": "value_amber",
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
            "key": "value_crimson",
            "value": 0
          }
        },
        {
          "set": {
            "key": "season",
            "value": 0
          }
        },
        {
          "set": {
            "key": "auctioneer",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "deal the hands",
      "do": [
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}}
      ]
    },
    {
      "use": "sync",
      "label": "your starting state",
      "mode": "self",
      "to": "all",
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "tell",
      "phase": "reveal",
      "label": "a new turn",
      "to": "all",
      "text": "A new turn begins. Seasons completed: {season} of {seasons}. Seat {auctioneer} is the auctioneer."
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "what the auctioneer may reveal",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "[a for a in ['Amber', 'Blue', 'Crimson'] if a in you.hand] if you.seat == auctioneer else []"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "reveal",
      "label": "choose a card to reveal",
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
        "bind": "card"
      },
      "text": "You are the auctioneer. Choose one painting from your hand to reveal: answer with the artist's name."
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "the reveal",
      "do": [
        {
          "set": {
            "key": "current_card",
            "value": "$card"
          }
        },
        {
          "remove": {
            "player": {
              "calc": "auctioneer"
            },
            "key": "hand",
            "value": {
              "calc": "current_card"
            }
          }
        },
        {
          "adjust": {
            "key": "played_amber",
            "value": 1,
            "if": {
              "calc": "current_card == 'Amber'"
            }
          }
        },
        {
          "adjust": {
            "key": "played_blue",
            "value": 1,
            "if": {
              "calc": "current_card == 'Blue'"
            }
          }
        },
        {
          "adjust": {
            "key": "played_crimson",
            "value": 1,
            "if": {
              "calc": "current_card == 'Crimson'"
            }
          }
        },
        {
          "set": {
            "key": "season_ending",
            "value": {
              "calc": "(played_amber if current_card == 'Amber' else (played_blue if current_card == 'Blue' else played_crimson)) == season_end_count"
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
      ],
      "text": "Seat {auctioneer} reveals a {current_card} painting. Played this season: Amber {played_amber}, Blue {played_blue}, Crimson {played_crimson}."
    },
    {
      "use": "tell",
      "phase": "reveal",
      "label": "the season ends",
      "when": {
        "calc": "season_ending"
      },
      "to": "all",
      "text": "That is the 4th {current_card} painting this season: the season ends. The card is not auctioned and no one owns it."
    },
    {
      "use": "poll",
      "phase": "auction",
      "label": "talk",
      "when": {
        "calc": "not season_ending"
      },
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
      "text": "A {current_card} painting is up for auction. Write one short message to the table; everyone writes at the same time and talk binds no one."
    },
    {
      "use": "poll",
      "phase": "auction",
      "label": "sealed bid",
      "when": {
        "calc": "not season_ending"
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
      "text": "Submit your sealed bid for the {current_card} painting: a whole number from {min_bid} up to your money. Highest bid wins; ties go to the auctioneer, then clockwise from the auctioneer. A non-auctioneer winner pays the auctioneer; an auctioneer who wins pays the bank."
    },
    {
      "use": "update",
      "phase": "auction",
      "label": "find the winner",
      "when": {
        "calc": "not season_ending"
      },
      "do": [
        {
          "set": {
            "key": "winner_seat",
            "value": {
              "calc": "[p.seat for p in players if p.bid * 10 + player_count - ((p.seat - auctioneer + player_count) % player_count) == max([q.bid * 10 + player_count - ((q.seat - auctioneer + player_count) % player_count) for q in players])][0]"
            }
          }
        },
        {
          "set": {
            "key": "price",
            "value": {
              "calc": "[p.bid for p in players if p.seat == winner_seat][0]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "auction",
      "label": "the sale",
      "when": {
        "calc": "not season_ending"
      },
      "do": [
        {
          "adjust": {
            "player": {
              "calc": "winner_seat"
            },
            "key": "money",
            "value": {
              "calc": "-price"
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
              "calc": "winner_seat != auctioneer"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "winner_seat"
            },
            "key": "owned_amber",
            "value": 1,
            "if": {
              "calc": "current_card == 'Amber'"
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
              "calc": "current_card == 'Blue'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "winner_seat"
            },
            "key": "owned_crimson",
            "value": 1,
            "if": {
              "calc": "current_card == 'Crimson'"
            }
          }
        }
      ],
      "text": "Bids: seat 1 {players[0].bid}, seat 2 {players[1].bid}, seat 3 {players[2].bid}, seat 4 {players[3].bid}. Seat {winner_seat} buys the {current_card} painting for {price} (paid to the auctioneer, seat {auctioneer}, or to the bank if the auctioneer bought it)."
    },
    {
      "use": "update",
      "phase": "season end",
      "label": "rank the artists",
      "when": {
        "calc": "season_ending"
      },
      "do": [
        {
          "set": {
            "key": "first_artist",
            "value": {
              "calc": "sorted([[played_amber * 10 + rarity_amber, 'Amber'], [played_blue * 10 + rarity_blue, 'Blue'], [played_crimson * 10 + rarity_crimson, 'Crimson']])[2][1]"
            }
          }
        },
        {
          "set": {
            "key": "second_artist",
            "value": {
              "calc": "sorted([[played_amber * 10 + rarity_amber, 'Amber'], [played_blue * 10 + rarity_blue, 'Blue'], [played_crimson * 10 + rarity_crimson, 'Crimson']])[1][1]"
            }
          }
        },
        {
          "adjust": {
            "key": "value_amber",
            "value": {
              "calc": "first_artist_gain if first_artist == 'Amber' else (second_artist_gain if second_artist == 'Amber' else third_artist_gain)"
            }
          }
        },
        {
          "adjust": {
            "key": "value_blue",
            "value": {
              "calc": "first_artist_gain if first_artist == 'Blue' else (second_artist_gain if second_artist == 'Blue' else third_artist_gain)"
            }
          }
        },
        {
          "adjust": {
            "key": "value_crimson",
            "value": {
              "calc": "first_artist_gain if first_artist == 'Crimson' else (second_artist_gain if second_artist == 'Crimson' else third_artist_gain)"
            }
          }
        }
      ],
      "text": "Season ranking: first {first_artist}, second {second_artist}. Artist values: Amber {value_amber}, Blue {value_blue}, Crimson {value_crimson}."
    },
    {
      "use": "update",
      "phase": "season end",
      "label": "season payouts",
      "when": {
        "calc": "season_ending"
      },
      "do": [
        {
          "adjust": {
            "players": "all",
            "key": "money",
            "value": {
              "calc": "(you.owned_amber * value_amber if first_artist == 'Amber' or second_artist == 'Amber' else 0) + (you.owned_blue * value_blue if first_artist == 'Blue' or second_artist == 'Blue' else 0) + (you.owned_crimson * value_crimson if first_artist == 'Crimson' or second_artist == 'Crimson' else 0)"
            },
            "text": "Seat {player} receives {value} from the bank."
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "season end",
      "label": "clear the season",
      "when": {
        "calc": "season_ending"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "owned_amber",
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
            "key": "owned_crimson",
            "value": 0
          }
        },
        {
          "set": {
            "key": "played_amber",
            "value": 0
          }
        },
        {
          "set": {
            "key": "played_blue",
            "value": 0
          }
        },
        {
          "set": {
            "key": "played_crimson",
            "value": 0
          }
        },
        {
          "adjust": {
            "key": "season",
            "value": 1
          }
        },
        {
          "set": {
            "key": "season_ending",
            "value": false
          }
        }
      ],
      "text": "Owned paintings are discarded and played counts reset. Seasons completed: {season} of {seasons}."
    },
    {
      "use": "update",
      "phase": "end of turn",
      "label": "pass the auctioneer",
      "do": [
        {
          "set": {
            "key": "auctioneer",
            "value": {
              "calc": "auctioneer % player_count + 1"
            }
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "end of turn",
      "label": "after the last season",
      "when": {
        "calc": "season >= seasons"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "season >= seasons"
      },
      "rank_by": "you.money",
      "text": "Winner: {result}. Final money: Seat 1 {players[0].money}, Seat 2 {players[1].money}, Seat 3 {players[2].money}, Seat 4 {players[3].money}."
    }
  },
  "limits": {
    "rounds": 30,
    "rounds_max": 31,
    "actions_max": 1000,
    "deadline_s": 120
  }
}
```
````
