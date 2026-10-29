# Task: write the XColos game file for "Masterpiece: Secret Collectors"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 4 to 4; set `meta.players` to {"min": 4, "max": 4, "suggested": 4} (the suggested size is the one the game plays best at).

MONEY: All amounts are in thousands of dollars. Bids and reserves are whole multiples of 50.

SETUP:
1. Seat the players 1 to 4 in a fixed circle. The player 'to the left' of player p is player p+1, and player 4's left is player 1.
2. Each player starts with 1500 cash. Cash is always public.
3. There are 4 public styles: Red, Blue, Gold and Green.
4. Each player receives 4 paintings, one of each style, with public names (for example 'P2-Gold'). Who owns which painting, and each painting's style, are always public.
5. Secret themes: the engine randomly gives each player a different style as their collector theme. Each player is told only their own theme. Everyone knows that the four themes are all different.
6. Painting values are dealt as follows.
   - Start from the pattern value(player p, style s) = [0, 300, 600, 1200][(p + s) mod 4], with players and styles indexed 0 to 3.
   - Then randomly shuffle which player is which row, which style is which column, and which value is which number.
   - The result: every player holds exactly one painting each worth 0, 300, 600 and 1200, and every style has exactly one painting of each of those values.
7. Each player is told privately the values of their own four paintings. A painting's value is known only to players who have owned it.

ROUNDS: The game has 12 rounds. The seller in round r is player ((r-1) mod 4) + 1, so each player sells 3 times. Each round:
1. ANNOUNCE: The engine names the seller. If the seller owns no paintings, skip to step 9.
2. LOT CHOICE: The player to the seller's left chooses one painting from the seller's current collection. The engine announces it, with its style, as the lot.
3. TALK: Every player, seller included, writes one short message at the same moment without seeing the others. All messages are then shown to everyone. Talk is not binding and may be false.
4. SEALED BIDS AND RESERVE: At the same moment, each non-seller submits a bid from 0 up to their current cash, and the seller submits a secret reserve from 0 to 2000.
5. HIGH BID: Let B be the highest bid. A tie goes to the tied bidder nearest the seller going clockwise (seller's left first).
6. RESOLVE:
   - If B > reserve, the high bidder pays B to the seller, takes the painting, and is told its value privately.
   - Otherwise the seller keeps the painting. If B is at least 50, the seller pays a fee of 50 to the bank, or all their cash if they have less than 50. Fee money leaves the game.
7. ANNOUNCE: The engine publishes all bids, whether the lot was sold or kept, the money moved and the new cash totals. The reserve and the painting's value are NOT published.
8. A painting that was bought can be chosen as a lot again later, when its new owner is the seller.
9. END CHECK: After round 12, go to scoring.

SCORING:
1. All values and themes are revealed.
2. Each player's score = cash + the total value of the paintings they own + 400 for each painting they own whose style is their own theme.

How the winner is decided: The highest score wins. If several players tie for the highest score, the one among them with the most cash wins. If they are still tied, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Masterpiece: Secret Collectors (4 to 4 players, best with 4)

Four collectors take turns selling paintings in sealed-bid auctions against secret reserves, each guarding private knowledge of painting values and a secret theme style worth a 400 bonus per matching painting.

STATE (every item below must exist in the file):
  - each player: cash (number, starts 1500); everyone sees it. Cash in thousands of dollars. Always public.
  - each player: paintings (list, starts "four painting names, one of each style, e.g. ['P2-Red','P2-Blue','P2-Gold','P2-Green']"); everyone sees it. Names of the paintings this player currently owns. Ownership and style are public; a name encodes its style.
  - each player: theme (text, starts 'a random style, different for every player'); only its owner sees it. Secret collector theme style. Each owned painting of this style is worth +400 at scoring. Revealed at the end.
  - each player: known_values (list, starts "'name=value' entries for the player's own four paintings"); only its owner sees it. Painting values this player has learned: the values of every painting they have ever owned.
  - each player: bid (number, starts 0); only its owner sees it. Sealed bid this round (non-sellers). Published after resolution.
  - each player: reserve (number, starts 0); only its owner sees it. Secret reserve this round (seller only). Never published.
  - each player: message (text, starts ''); everyone sees it. This round's talk message, shown to all after everyone has written.
  - each player: tie_priority (number, starts 0); everyone sees it. Scratch tie-break key this round: 3 for the seller's left, 2 for the next seat, 1 for the seat after that, 0 for the seller.
  - each player: score (number, starts 0); everyone sees it. Final score = cash + total value of owned paintings + 400 for each owned painting of the player's theme. Computed at game end.
  - the table: round (number, starts 0); everyone sees it. Current round number, 1 to 12.
  - the table: seller (number, starts 0); everyone sees it. Seat of this round's seller: ((round-1) mod 4) + 1.
  - the table: lot (text, starts ''); everyone sees it. Name of the painting being auctioned this round.
  - the table: lot_style (text, starts ''); everyone sees it. Style of the current lot.
  - the table: painting_values (list, starts "16 'name=value' entries dealt from a shuffled Latin square of {0,300,600,1200}"); hidden from all players. True value of every painting. Hidden from all; each player learns only the values of paintings they have owned. Revealed at the end.
  - the table: high_bid (number, starts 0); everyone sees it. Highest bid B this round.
  - the table: high_bidder (number, starts 0); everyone sees it. Seat of the winning bidder after the tie-break.
  - the table: sold (bool, starts False); everyone sees it. Whether this round's lot was sold.
  - parameters, each kept as a table attribute: starting_cash = 1500, num_styles = 4, paintings_per_player = 4, value_low = 0, value_mid_low = 300, value_mid_high = 600, value_high = 1200, rounds = 12, sales_per_player = 3, bid_step = 50, reserve_max = 2000, bid_min = 0, reserve_min = 0, unsold_fee = 50, fee_trigger_min_bid = 50, theme_bonus = 400

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seat players 1 to 4 in a fixed circle; the left of seat p is seat p+1, and the left of seat 4 is seat 1.
  2. Every player's cash is set to 1500.
  3. Each player p receives four paintings named 'Pp-Red', 'Pp-Blue', 'Pp-Gold' and 'Pp-Green' in their paintings list.
  4. The four styles Red, Blue, Gold and Green are dealt at random as secret themes, one different style per player, each stored in that player's theme (ally).
  5. Painting values are built from the pattern value(p, s) = [0,300,600,1200][(p+s) mod 4], with players and styles indexed 0 to 3. Rows (players), columns (styles) and the value labels are then shuffled at random, so each player holds one painting each worth 0, 300, 600 and 1200, and each style has one painting of each value. The result is stored in painting_values (hidden).
  6. Each player's known_values is set to the values of their own four paintings, and the engine tells each player those values privately.
  7. Everyone is told that the four themes are all different.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round += 1; seller = ((round-1) mod 4) + 1; sold = false; high_bid = 0; high_bidder = 0; lot = ''; each player's bid = 0 and reserve = 0; tie_priority = 3 for seat ((seller) mod 4)+1, 2 for seat ((seller+1) mod 4)+1, 1 for seat ((seller+2) mod 4)+1, 0 for the seller. Announces the seller.
  2. [ask] the seat to the seller's left: ((seller) mod 4) + 1 answers: one painting name from the seller's current paintings list. What happens: when the seller's paintings list is not empty: lot = chosen name; lot_style = its style. The lot and its style are announced to all.
  3. [poll] all players answers: short text message. What happens: when the seller's paintings list is not empty: each player's message = their text; afterwards broadcast {"to": "all", "text": "Seat {seat} says: {value}"}. Talk is not binding.
  4. [poll] all players answers: non-sellers: a whole number from 0 to their cash (bid); seller: a whole number from 0 to 2000 (reserve). What happens: when the seller's paintings list is not empty: each value is rounded down to a multiple of 50. Each non-seller's bid is set to their number; the seller's reserve is set to theirs. Nobody sees any answer until all are in.
  5. [update] all players. What happens: when the seller's paintings list is not empty: high_bid = max over non-sellers of bid; high_bidder = the non-seller with the largest (bid * 10 + tie_priority).
  6. [update] seller and high bidder. What happens: when the seller's paintings list is not empty: if high_bid > seller.reserve then sold = true; high_bidder.cash -= high_bid; seller.cash += high_bid; remove lot from seller.paintings; append lot to high_bidder.paintings; append the lot's 'name=value' entry from painting_values to high_bidder.known_values and tell the high bidder privately. Otherwise sold = false, and if high_bid >= 50 then seller.cash -= min(50, seller.cash), and that money leaves the game.
  7. [tell] all players. What happens: when the seller's paintings list is not empty: publish every non-seller's bid, whether the lot was sold or kept, the money moved (price or fee) and every player's new cash. The reserve and the painting's value are not published.
  8. [update] all players. What happens: when round == 12: reveal painting_values and every theme to all; each player's score = cash + sum of values of the paintings in their paintings list + 400 * (number of paintings in their list whose style equals their theme).
  9. [check] all players. What happens: end the game if round == 12, otherwise continue to the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, then every player has cash 1500 and owns exactly 4 paintings, one each of Red, Blue, Gold and Green.
  R2. When themes are dealt, then each of the 4 players has a different theme style, and each is told only their own.
  R3. When values are dealt, then each player holds one painting each worth 0, 300, 600 and 1200, and each style has exactly one painting of each of those values.
  R4. When values are dealt, then each player learns privately the values of their own 4 paintings and no other values.
  R5. When round r begins, then the seller is seat ((r-1) mod 4)+1, so seats 1, 2, 3, 4 sell in rounds 1, 2, 3, 4 and again in rounds 5 to 8 and 9 to 12.
  R6. When the seller owns no paintings, then the lot choice, talk, bids and resolution are skipped that round.
  R7. When a lot is chosen, then the chooser is the seat to the seller's left (seat seller mod 4 + 1), the lot is one of the seller's current paintings, and it is announced with its style.
  R8. When talk happens, then every player, seller included, submits one message at the same time, and all messages are shown to everyone afterwards.
  R9. When bids are made, then each non-seller bids a multiple of 50 from 0 to their current cash, and the seller sets a secret reserve that is a multiple of 50 from 0 to 2000, all at the same time.
  R10. When two or more bidders tie for the highest bid B, then the winner is the tied bidder nearest the seller going clockwise, the seller's left first.
  R11. When B > reserve, then the high bidder pays B to the seller, the lot moves to the high bidder's paintings, and the high bidder privately learns its value.
  R12. When B <= reserve and B >= 50, then the seller keeps the lot and pays a fee of 50 (or all their cash if under 50), which leaves the game.
  R13. When B <= reserve and B is 0, then the seller keeps the lot and pays no fee.
  R14. When an auction resolves, then all bids, sold or kept, the money moved and every new cash total are published, but not the reserve or the painting's value.
  R15. When a bought painting's new owner is the seller in a later round, then that painting may be chosen as the lot.
  R16. When round 12 ends, then the game ends, and all values and themes are revealed.
  R17. When scoring, then score = cash + the total value of owned paintings + 400 for each owned painting whose style equals the owner's theme.
  R18. When scores tie at the top, then the tied player with more cash wins, and players tied on both share the win (the draw).

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Lot choice | asked: the seat to the seller's left | options: each painting name currently in the seller's paintings list; the step is not asked if that list is empty
  - Talk | asked: all four seats | options: one short free-text message
  - Sealed bid | asked: each non-seller | options: a whole number from 0 to their current cash, rounded down to a multiple of 50
  - Secret reserve | asked: the seller | options: a whole number from 0 to 2000, rounded down to a multiple of 50

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round == 12
  - each player's standing: you.score * 100000 + you.cash (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their score (cash + value of owned paintings + 400 per owned painting of their theme), with cash breaking ties. The highest wins; players still level on both score and cash share the win, which stands for the source's draw.
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

- each player: `cash` (number, visible: public, starts 1500): Cash in thousands of dollars. Always public.
- each player: `paintings` (list, visible: public, starts "four painting names, one of each style, e.g. ['P2-Red','P2-Blue','P2-Gold','P2-Green']"): Names of the paintings this player currently owns. Ownership and style are public; a name encodes its style.
- each player: `score` (number, visible: public, starts 0): Final score = cash + total value of owned paintings + 400 for each owned painting of the player's theme. Computed at game end.
- the table: `round` (number, visible: public, starts 0): Current round number, 1 to 12.
- the table: `seller` (number, visible: public, starts 0): Seat of this round's seller: ((round-1) mod 4) + 1.
- the table: `lot` (text, visible: public, starts ''): Name of the painting being auctioned this round.
- the table: `high_bid` (number, visible: public, starts 0): Highest bid B this round.
- the table: `high_bidder` (number, visible: public, starts 0): Seat of the winning bidder after the tie-break.
- the table: `sold` (bool, visible: public, starts False): Whether this round's lot was sold.
- parameters (each must be an attribute holding this value, never a number buried in a step): starting_cash = 1500, num_styles = 4, paintings_per_player = 4, value_low = 0, value_mid_low = 300, value_mid_high = 600, value_high = 1200, rounds = 12, sales_per_player = 3, bid_step = 50, reserve_max = 2000, bid_min = 0, reserve_min = 0, unsold_fee = 50, fee_trigger_min_bid = 50, theme_bonus = 400
- the game ends with ONE ending whose `rank_by` is `you.score * 100000 + you.cash`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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

Rewrite the final scoring. For each player:
- Start from `cash`.
- Look up every painting currently in their `paintings` list in the table's authoritative `painting_values` list. This list is the one set at setup or given by the scenario, not each player's private `known_values`, which is only what they were told.
- Sum those values. Paintings bought from others count at their true value.
- Add `theme_bonus` (400) once for each owned painting whose style, the part of the name after the dash, equals that player's own `theme`.
- Store the result in `score`.

Do not count paintings the player no longer owns. Do not apply the bonus per style held instead of per painting. Do not use another player's theme. Do not take values from a separate internal deal that ignores `painting_values`.

Keep the ending's rank_by as `you.score * 100000 + you.cash`. Check the case above: seat 2 with cash 1500, P2-Blue=600, P2-Gold=1200, P2-Green=0 and theme Blue must score 3700.
