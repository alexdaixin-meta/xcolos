# Task: write the XColos game file for "Greek Hold 'em Lite"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 5; set `meta.players` to {"min": 3, "max": 5, "suggested": 4} (the suggested size is the one the game plays best at).

SETUP: Each player starts with 40 chips. The deck has 32 cards: values 1 to 8, four copies of each value. The game lasts 15 hands (rounds). There is no dealer or acting order; every decision is made simultaneously.

EACH HAND:
1. Ante and deal. Every player still in the game puts 1 chip into the pot (a player with only 1 chip is then all-in). The deck is shuffled. Each player is dealt 2 hole cards, seen only by that player, and 5 board cards are set face down. Any pot left over from the previous hand stays in the pot.

2. Flop. The first 3 board cards are revealed to everyone.

3. Flop bet. Every player in the hand secretly chooses a bet of 0, 1, 2, 3 or 4 chips (never more than their stack). All bets are revealed together and paid into the pot. Call the largest bet H.

4. Flop call or fold. Each player whose bet was less than H chooses simultaneously:
   - CALL: pay the difference so their bet equals H. If they have fewer chips, they pay their whole stack and stay in.
   - FOLD: they are out of this hand, and chips already put in stay in the pot.
   Players who bet H stay in automatically.

5. If only one player remains in the hand, they take the whole pot and the hand ends (skip to step 10).

6. Turn and river. Board cards 4 and 5 are revealed.

7. River bet. This is the same as step 3: a simultaneous secret bet of 0–4 chips by every player still in the hand.

8. River call or fold. This is the same as step 4.

9. Showdown. If only one player remains, they take the pot. Otherwise every remaining player reveals their hole cards and their Strength is computed:
   - matches = the number of the 5 board cards whose value equals either of the player's hole card values. If both hole cards share a value, a board card of that value counts once.
   - matches counts at most 3, because a hand uses exactly three board cards.
   - pair = 1 if the two hole cards have the same value, else 0.
   - Strength = 20 × min(matches, 3) + 30 × pair + (hole card 1 value) + (hole card 2 value).
   The highest Strength takes the pot. If several players tie for highest, the pot is split equally among them in whole chips, and any leftover chip stays in the pot for the next hand.

10. Elimination. Any player with 0 chips is eliminated and takes no further part.

END: The game ends after hand 15, or earlier if only one player has chips left.

How the winner is decided: When the game ends, the player with the most chips wins. If two or more players tie for the most chips, those players draw. If only one player has chips left before hand 15, that player wins.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Greek Hold 'em Lite (3 to 5 players, best with 4)

A simplified simultaneous-betting poker for 3 to 5 players: ante, flop bet, call or fold, river bet, call or fold, then an arithmetic showdown, over 15 hands; most chips wins.

STATE (every item below must exist in the file):
  - each player: chips (number, starts 40); everyone sees it. The player's chip stack. It is the score.
  - each player: out (bool, starts False); everyone sees it. True once the player reached 0 chips at the end of a hand and was eliminated.
  - each player: hole (list, starts []); only its owner sees it. The player's 2 hole cards (values 1-8), seen only by the owner.
  - each player: shown_hole (list, starts []); everyone sees it. Hole cards revealed at showdown by a player still in the hand.
  - each player: in_hand (bool, starts False); everyone sees it. True while the player is still contesting the current hand (has not folded and is not eliminated).
  - each player: bet (number, starts 0); everyone sees it. Chips the player has put in during the current betting round, including any call.
  - each player: strength (number, starts 0); everyone sees it. Showdown Strength = 20*min(matches,3) + 30*pair + hole1 + hole2.
  - the table: deck (list, starts [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8]); hidden from all players. The 32-card deck, rebuilt and shuffled each hand.
  - the table: board (list, starts []); hidden from all players. The 5 face-down board cards, in order.
  - the table: board_shown (list, starts []); everyone sees it. Board cards revealed so far: the first 3 at the flop, all 5 at the turn and river.
  - the table: pot (number, starts 0); everyone sees it. Chips in the pot. A leftover from a split carries to the next hand.
  - the table: hand_no (number, starts 0); everyone sees it. Number of the current hand, from 1 to 15.
  - the table: high_bet (number, starts 0); everyone sees it. H, the largest bet in the current betting round.
  - the table: in_hand_count (number, starts 0); everyone sees it. How many players have in_hand true.
  - the table: alive_count (number, starts 0); everyone sees it. How many players have out false.
  - the table: best_strength (number, starts 0); everyone sees it. The highest strength among players in the hand at showdown.
  - the table: winners_count (number, starts 0); everyone sees it. How many in-hand players have strength equal to best_strength.
  - parameters, each kept as a table attribute: starting_chips = 40, deck_size = 32, card_value_min = 1, card_value_max = 8, copies_per_value = 4, hands = 15, ante = 1, hole_cards = 2, board_cards = 5, flop_cards = 3, min_bet = 0, max_bet = 4, match_weight = 20, max_matches = 3, pair_bonus = 30, elimination_chips = 0

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Every player gets chips = 40, out = false, hole = [] and shown_hole = [].
  2. Set pot = 0, hand_no = 0, and alive_count to the number of players.
  3. There is no dealer and no acting order. Every decision is made simultaneously.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: hand_no += 1. For each player with out = false: chips -= 1, pot += 1, in_hand = true. For each player with out = true: in_hand = false. Every player gets bet = 0, strength = 0, hole = [] and shown_hole = []. Set board = [] and board_shown = []. A player left with 0 chips after the ante is all-in and stays in the hand.
  2. [update] all players. What happens: Rebuild deck as the 32 cards (values 1-8, four of each). For each player with in_hand = true, draw 2 cards at random: remove each from deck and append it to that player's hole. Then draw 5 cards at random from deck and append them in order to board.
  3. [sync] all players. What happens: Each player privately sees their own hole cards.
  4. [update] all players. What happens: Flop: board_shown = the first 3 cards of board. Announce board_shown, pot and every player's chips to everyone.
  5. [poll] every player with in_hand = true answers: a whole number from 0 to min(4, chips). What happens: Each answering player gets bet = answer, chips -= answer and pot += answer. high_bet = the largest bet among players with in_hand = true. All bets are revealed together.
  6. [poll] every player with in_hand = true and bet < high_bet answers: call | fold. What happens: call: paid = min(high_bet - bet, chips); chips -= paid, pot += paid, bet += paid, and the player stays in. fold: in_hand = false, and chips already put in stay in pot. Players with bet = high_bet stay in automatically.
  7. [update] all players. What happens: in_hand_count = number of players with in_hand = true. If in_hand_count = 1: that player's chips += pot and pot = 0, and the hand skips to elimination.
  8. [update] all players. What happens: When in_hand_count >= 2: board_shown = all 5 cards of board, every player's bet = 0, and high_bet = 0. Announce board_shown and pot.
  9. [poll] every player with in_hand = true, when in_hand_count >= 2 answers: a whole number from 0 to min(4, chips). What happens: Each answering player gets bet = answer, chips -= answer and pot += answer. high_bet = the largest bet among players with in_hand = true. All bets are revealed together.
  10. [poll] every player with in_hand = true and bet < high_bet, when in_hand_count >= 2 answers: call | fold. What happens: call: paid = min(high_bet - bet, chips); chips -= paid, pot += paid, bet += paid. fold: in_hand = false, and chips stay in pot.
  11. [update] all players. What happens: When in_hand_count >= 2 before this step: recount in_hand_count. If it is 1, that player's chips += pot and pot = 0. Otherwise it is a showdown. For each player with in_hand = true: shown_hole = hole; matches = number of board cards whose value equals either hole value; pair = 1 if hole[0] = hole[1], else 0; strength = 20*min(matches,3) + 30*pair + hole[0] + hole[1]. Then best_strength = max strength among in-hand players and winners_count = number of in-hand players with strength = best_strength. Each such player's chips += floor(pot / winners_count), and pot = pot mod winners_count. Announce the shown hole cards, the strengths and the winners.
  12. [update] all players. What happens: Elimination: every player with out = false and chips = 0 gets out = true and in_hand = false. alive_count = number of players with out = false. Announce each player's chips and who is eliminated.
  13. [check] all players. What happens: End the game if hand_no >= 15 or alive_count <= 1; otherwise run the next hand.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, each player has 40 chips and the pot is 0.
  R2. When a hand starts, each player not eliminated pays 1 chip into the pot, so a player with 5 chips goes to 4 and the pot rises by 1 per player.
  R3. When a player with exactly 1 chip antes, they have 0 chips and still take part in the hand (all-in).
  R4. When a hand starts, the deck is rebuilt to 32 cards (values 1 to 8, four of each), each player in the hand receives 2 hole cards from it, and 5 board cards are drawn from it.
  R5. When the flop happens, exactly the first 3 board cards become public in board_shown.
  R6. When a player bets in a betting round, the bet is a whole number from 0 to 4 and no more than their chips, and it moves from their chips to the pot.
  R7. When bets are revealed, H is the largest bet among players still in the hand, and only players who bet less than H are asked to call or fold.
  R8. When a player calls, they pay H minus their bet, so a player who bet 1 against H = 4 pays 3 more.
  R9. When a player calls with fewer chips than the difference, they pay all their chips, go to 0, and stay in the hand.
  R10. When a player folds, they leave the hand and the chips they already bet stay in the pot.
  R11. When only one player remains in the hand after the flop call or fold, that player takes the whole pot, the pot becomes 0, and the turn, river and showdown do not happen.
  R12. When 2 or more players remain after the flop, board cards 4 and 5 are revealed, so board_shown has all 5 cards.
  R13. When the river betting happens, it follows R6 to R10, with bets reset to 0 for the new round.
  R14. When only one player remains after the river call or fold, that player takes the whole pot.
  R15. When a showdown happens, each remaining player's hole cards become public, and strength = 20*min(matches,3) + 30*pair + hole1 + hole2.
  R16. When counting matches, a board card counts if its value equals either hole value, and it counts once even if both hole cards share that value; for example hole 5,5 with board 5,5,2,3,8 gives matches = 2, pair = 1, strength = 40+30+10 = 80.
  R17. When matches exceeds 3, only 3 count; for example hole 2,7 with board 2,2,7,7,1 gives strength = 60+0+9 = 69.
  R18. When one player has the highest strength at showdown, that player takes the whole pot.
  R19. When k players tie for the highest strength, each receives floor(pot/k) chips and pot mod k chips stay in the pot for the next hand; for example a pot of 11 split 3 ways gives 3 each and leaves 2.
  R20. When a hand ends and a player has 0 chips, that player is eliminated (out = true) and takes no further part.
  R21. When hand 15 ends, the game ends.
  R22. When only one player is not eliminated at the end of a hand, the game ends at once.
  R23. When the game ends, the player with the most chips wins, and players tied for the most chips share the win.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Flop bet | asked: every player with in_hand = true | options: a whole number from 0 to min(4, chips); a player with 0 chips (all-in) may only bet 0
  - Flop call or fold | asked: every player with in_hand = true whose bet is less than high_bet | options: call, fold; players whose bet equals high_bet, folded players and eliminated players are not asked
  - River bet | asked: every player with in_hand = true, only when 2 or more players remain | options: a whole number from 0 to min(4, chips); a player with 0 chips may only bet 0
  - River call or fold | asked: every player with in_hand = true whose river bet is less than high_bet, only when 2 or more players remain | options: call, fold; everyone else is not asked

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: hand_no >= 15 or alive_count <= 1
  - each player's standing: you.chips (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their chip count. The player with the most chips wins, and players tied for the most chips share the win (a draw). If only one player has chips left before hand 15, that player wins, because every other player has 0.
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

- each player: `chips` (number, visible: public, starts 40): The player's chip stack. It is the score.
- each player: `out` (bool, visible: public, starts False): True once the player reached 0 chips at the end of a hand and was eliminated.
- each player: `shown_hole` (list, visible: public, starts []): Hole cards revealed at showdown by a player still in the hand.
- the table: `board_shown` (list, visible: public, starts []): Board cards revealed so far: the first 3 at the flop, all 5 at the turn and river.
- the table: `pot` (number, visible: public, starts 0): Chips in the pot. A leftover from a split carries to the next hand.
- the table: `hand_no` (number, visible: public, starts 0): Number of the current hand, from 1 to 15.
- parameters (each must be an attribute holding this value, never a number buried in a step): starting_chips = 40, deck_size = 32, card_value_min = 1, card_value_max = 8, copies_per_value = 4, hands = 15, ante = 1, hole_cards = 2, board_cards = 5, flop_cards = 3, min_bet = 0, max_bet = 4, match_weight = 20, max_matches = 3, pair_bonus = 30, elimination_chips = 0
- the game ends with ONE ending whose `rank_by` is `you.chips`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
