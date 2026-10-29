# Task: write the XColos game file for "For Sale: Sealed Bids"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

SETUP. There are exactly 3 players, numbered 1, 2 and 3.
- Each player starts with 18 coins. A player's coin total is private: only that player sees it.
- The property deck holds the cards 1 to 30, one of each.
- The cheque deck holds the values 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14 and 15, two of each, for 30 cheques.
- Each player has a cheque total starting at 0. It is private.
- Each player has a property hand starting empty. Hands are public.

The game lasts 16 rounds. Rounds 1-8 are BUYING rounds and rounds 9-16 are SELLING rounds.

BUYING ROUND (rounds 1-8):
1. In round 1 only, shuffle the property deck. Only the top 24 cards will ever be used; the bottom 6 stay unseen.
2. Reveal the next 3 cards from the top of the property deck. Call them LOW, MIDDLE and HIGH by value.
3. All players at the same moment secretly submit a bid: a whole number from 0 up to their current coins.
4. Rank the bids from highest to lowest. Break ties by this round's priority order. In round r, priority goes first to player ((r-1) mod 3)+1, then to the next player number, wrapping 3 to 1.
5. The first-ranked player takes HIGH and pays their full bid.
6. The second-ranked player takes MIDDLE and pays half their bid, rounded down.
7. The third-ranked player takes LOW and pays half their bid, rounded down.
8. Payments go to the bank and come out of each player's private coins.
9. Announce publicly which player took LOW, MIDDLE and HIGH. Bid amounts and coin totals are NOT announced.
After round 8 each player holds exactly 8 properties.

SELLING ROUND (rounds 9-16):
1. In round 9 only, shuffle the cheque deck. Only the top 24 cheques will ever be used.
2. Reveal the next 3 cheques from the top of the cheque deck.
3. All players at the same moment secretly choose one property from their own hand.
4. Reveal the chosen properties. Properties are all different, so there are no ties.
5. The player who played the highest property adds the highest cheque to their cheque total. The middle property gets the middle cheque, and the lowest property gets the lowest cheque.
6. Played properties are discarded from hands.
7. Announce publicly who played which property and who took which cheque. Running cheque totals stay private.

END. After round 16, each player's final money is their cheque total plus their remaining coins. These are revealed.

How the winner is decided: The player with the most final money (cheques plus remaining coins) wins. If two or more tie for most, the tied player with more remaining coins wins. If they are still tied, the game is a draw among them.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: For Sale: Sealed Bids (3 to 3 players, best with 3)

Three players spend 8 sealed-bid rounds buying property cards with private coins, then 8 simultaneous rounds selling those properties for cheques; the most cheques plus leftover coins wins.

STATE (every item below must exist in the file):
  - each player: coins (number, starts 18); only its owner sees it. Private coin total. Bids are paid from it, and what is left counts toward final money.
  - each player: cheques (number, starts 0); only its owner sees it. Private running total of cheques won in selling rounds.
  - each player: hand (list, starts []); everyone sees it. Property cards the player holds. Hands are public.
  - each player: bid (number, starts 0); only its owner sees it. This buying round's secret bid, from 0 to coins.
  - each player: bid_key (number, starts 0); only its owner sees it. Engine scratch: bid*10 plus a priority weight of 3, 2 or 1. It ranks the bids with this round's tie-break. The rules never mention it.
  - each player: bid_rank (number, starts 0); everyone sees it. This buying round's rank: 1 takes HIGH, 2 takes MIDDLE, 3 takes LOW. It is announced through who took which card.
  - each player: played (number, starts 0); everyone sees it. The property chosen in this selling round, revealed after everyone has chosen.
  - each player: final_money (number, starts 0); everyone sees it. Set and revealed after round 16 as cheques + coins.
  - each player: final_coins (number, starts 0); everyone sees it. Remaining coins, revealed after round 16 because they are the tie-break.
  - the table: round (number, starts 1); everyone sees it. The current round, 1 to 16. Rounds 1-8 are buying rounds and rounds 9-16 are selling rounds.
  - the table: property_deck (list, starts '[1..30]'); hidden from all players. The undrawn property cards. Drawing at random is the shuffle; 6 cards are never drawn.
  - the table: cheque_deck (list, starts '[0,0,2,2,3,3,...,15,15]'); hidden from all players. The undrawn cheques, 30 in all. Drawing at random is the shuffle; 6 are never drawn.
  - the table: revealed_properties (list, starts []); everyone sees it. The 3 property cards revealed this buying round.
  - the table: revealed_cheques (list, starts []); everyone sees it. The 3 cheques revealed this selling round.
  - the table: priority_first (number, starts 1); everyone sees it. The seat with first tie-break priority this round: ((round-1) mod 3)+1.
  - parameters, each kept as a table attribute: player_count = 3, starting_coins = 18, property_min = 1, property_max = 30, property_deck_size = 30, properties_used = 24, properties_unused = 6, cheque_min_value = 0, cheque_max_value = 15, cheque_missing_value = 1, cheque_distinct_values = 15, cheque_copies_each = 2, cheque_deck_size = 30, cheques_used = 24, total_rounds = 16, buying_rounds = 8, first_selling_round = 9, cards_revealed_per_round = 3, first_place_pay_fraction = 1, second_third_pay_divisor = 2, properties_per_player_after_buying = 8, initial_cheque_total = 0, tie_break_bid_multiplier = 10, rank_coin_tiebreak_multiplier = 100

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seat the 3 players as seats 1, 2 and 3.
  2. Give each player coins = 18, cheques = 0 and an empty public hand.
  3. Put the property cards 1 to 30, one of each, into the hidden table list property_deck.
  4. Put two of each cheque value 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14 and 15 (30 cheques) into the hidden table list cheque_deck.
  5. Set round = 1.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] table. What happens: Set priority_first = ((round-1) mod 3)+1. When round <= 8: clear revealed_properties, then draw 3 cards at random from property_deck, removing each from property_deck and appending it to revealed_properties. Announce the 3 cards as LOW = min, MIDDLE = the remaining card and HIGH = max, and announce priority_first.
  2. [sync] all players. What happens: When round <= 8: each player is sent their own coins, all hands, revealed_properties and priority_first.
  3. [poll] all players answers: a whole number from 0 to your coins. What happens: When round <= 8: set bid for each player. Nobody sees any bid.
  4. [update] all players. What happens: When round <= 8: for each player, bid_key = bid*10 + (3 - ((seat - priority_first + 3) mod 3)). Then bid_rank = 1 + the number of other players whose bid_key is larger than this player's.
  5. [update] all players. What happens: When round <= 8: the player with bid_rank 1 appends max(revealed_properties) to hand and pays coins -= bid. The player with bid_rank 2 appends the middle card to hand and pays coins -= floor(bid/2). The player with bid_rank 3 appends min(revealed_properties) to hand and pays coins -= floor(bid/2). Payments go to the bank. Publicly announce which seat took LOW, MIDDLE and HIGH, without bids or coin totals.
  6. [update] table. What happens: When round >= 9: clear revealed_cheques, then draw 3 cheques at random from cheque_deck, removing each from cheque_deck and appending it to revealed_cheques. Announce the 3 cheques.
  7. [sync] all players. What happens: When round >= 9: each player is sent their own cheques and coins, all hands, and revealed_cheques.
  8. [poll] all players answers: one property card from your own hand. What happens: When round >= 9: set played for each player. The choices are revealed only after all are in.
  9. [update] all players. What happens: When round >= 9: the player with the highest played adds max(revealed_cheques) to cheques. The player with the middle played adds the middle cheque. The player with the lowest played adds min(revealed_cheques). Each player removes played from hand, which discards the card. Publicly announce who played which property and who took which cheque; cheque totals stay private.
  10. [update] table. What happens: round += 1.
  11. [update] all players. What happens: When round > 16: final_money = cheques + coins and final_coins = coins, both revealed publicly.
  12. [check] table. What happens: End the game if round > 16; otherwise continue with the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, each of the 3 players has coins = 18, cheques = 0 and an empty hand.
  R2. When the game starts, property_deck holds the 30 cards 1 to 30, and cheque_deck holds two each of 0 and 2 to 15, for 30 cheques.
  R3. When a buying round (1-8) begins, 3 cards are drawn at random from property_deck into revealed_properties, and property_deck shrinks by 3.
  R4. When a player bids in a buying round, the bid is a whole number from 0 to that player's current coins, and all bids are made simultaneously.
  R5. When bids are ranked, the higher bid ranks higher.
  R6. When bids tie in round r, priority goes first to seat ((r-1) mod 3)+1, then to the next seat, wrapping from 3 to 1; for example, in round 2 the order is 2, 3, 1.
  R7. When a player ranks first in a buying round, they take the HIGH card and pay their full bid; for example, a bid of 7 costs 7.
  R8. When a player ranks second or third, they take MIDDLE or LOW respectively and pay floor(bid/2); for example, a bid of 5 costs 2.
  R9. When a buying round ends, it is announced who took LOW, MIDDLE and HIGH, but bids and coin totals are not announced.
  R10. When round 8 ends, each player holds exactly 8 properties and 6 cards remain unused in property_deck.
  R11. When a selling round (9-16) begins, 3 cheques are drawn at random from cheque_deck into revealed_cheques.
  R12. When a selling round is played, each player simultaneously chooses one property from their own hand.
  R13. When the properties are revealed, the highest takes the highest cheque, the middle takes the middle cheque and the lowest takes the lowest cheque, each added to that player's cheques.
  R14. When a property is played, it is removed from its owner's hand.
  R15. When a selling round ends, it is announced who played which property and who took which cheque; cheque totals stay private.
  R16. When round 16 ends, the game ends and each player's final_money = cheques + coins is revealed.
  R17. When final money is compared, the most wins; a tie goes to more remaining coins, and a remaining tie is a shared win (a draw).

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Buying round bid (rounds 1-8) | asked: all three seats at once | options: every whole number from 0 to that seat's current coins
  - Selling round property choice (rounds 9-16) | asked: all three seats at once | options: each property card currently in that seat's own hand, and nothing else

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round > 16
  - each player's standing: you.final_money * 100 + you.final_coins (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: The most final money (cheque total plus remaining coins) wins. A tie goes to the tied player with more remaining coins; coins are at most 18, so the x100 weighting keeps money first. Players still level share the win, which is the draw.
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

- each player: `hand` (list, visible: public, starts []): Property cards the player holds. Hands are public.
- each player: `final_money` (number, visible: public, starts 0): Set and revealed after round 16 as cheques + coins.
- each player: `final_coins` (number, visible: public, starts 0): Remaining coins, revealed after round 16 because they are the tie-break.
- the table: `round` (number, visible: public, starts 1): The current round, 1 to 16. Rounds 1-8 are buying rounds and rounds 9-16 are selling rounds.
- parameters (each must be an attribute holding this value, never a number buried in a step): player_count = 3, starting_coins = 18, property_min = 1, property_max = 30, property_deck_size = 30, properties_used = 24, properties_unused = 6, cheque_min_value = 0, cheque_max_value = 15, cheque_missing_value = 1, cheque_distinct_values = 15, cheque_copies_each = 2, cheque_deck_size = 30, cheques_used = 24, total_rounds = 16, buying_rounds = 8, first_selling_round = 9, cards_revealed_per_round = 3, first_place_pay_fraction = 1, second_third_pay_divisor = 2, properties_per_player_after_buying = 8, initial_cheque_total = 0, tie_break_bid_multiplier = 10, rank_coin_tiebreak_multiplier = 100
- the game ends with ONE ending whose `rank_by` is `you.final_money * 100 + you.final_coins`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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

Rewrite the buying-round bid step as a simultaneous choice for all three seats.
- Its options must be an explicit list of whole numbers from 0 up to that seat's own current coins, computed per seat from the `coins` attribute. For example, a seat with 5 coins must be offered exactly 0,1,2,3,4,5.
- Do not use a fixed list, the starting_coins parameter, or a free numeric entry that is never presented as options.
- Store each seat's chosen value in `bid`.
- Rank by bid_key = bid * tie_break_bid_multiplier + priority weight, where the priority weight comes from ((round-1) mod 3)+1 with wrap-around. For example, in round 2 the order is 2, 3, 1.
- First rank takes the max of revealed_properties and pays the full bid. Second takes the middle card, third takes the minimum, and each pays floor(bid / second_third_pay_divisor).
- Keep the 3-card draw from property_deck as it is; it already shrinks the deck by 3.
- In selling rounds, likewise offer each seat its own `hand` cards as the options.
- Check that a scenario with distinct bids gives HIGH to the highest bid.
