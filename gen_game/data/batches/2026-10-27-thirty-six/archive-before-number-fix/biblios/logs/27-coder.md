# 27 coder

- time: 2026-10-27T17:45:08+00:00 (75.1s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 3014d7299a942b2e, reply sha256 a4665d0c2a739fb0

## Sent

````
# Task: write the XColos game file for "Biblios: Scriptorium Duel of Three"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

VISIBILITY.
V1. Hidden: each player's private hand, colour totals (red, blue, green) and gold are known only to that player. The order of the deck is known to nobody.
V2. Public: the deck composition (R1), every lot, every talk message and who wrote it, every bid, every auction result and price, every player's bought list, every Church choice and who made it, and the table VP values.
V3. Opponents can work out part of a rival's gold from sales and purchases, but kept Gold cards are never revealed. All gold is revealed at scoring.

SETUP.
R1. The deck holds 24 cards:
- Red, Blue and Green, each with values 1,1,2,2,3,4 (written like 'red-1'), 18 cards;
- Gold cards with values 2,2,3,3 (written like 'gold-2'), 4 cards;
- 2 Church cards ('church').
The deck is shuffled once at the start and never again.
R2. Each player starts with:
- gold 4;
- an empty private hand and an empty public bought list;
- red=0, blue=0, green=0;
- bid=0, church_pending=false, church_choice='none', message empty, vp=0.
R3. The table starts with vp_red=3, vp_blue=3, vp_green=3, round=0, lot='none' and drawn empty.

EACH ROUND (12 rounds).
R4. Round r begins (round becomes r). The active seat is ((r-1) mod 3)+1, so seats go 1,2,3,1,2,3,... and each seat is active exactly 4 times.
R5. The first two cards of the deck are moved, in order, into 'drawn'. Only the active player sees them.
R6. Keep. The active player alone chooses one of the two drawn cards to keep.
R7. The kept card goes into the active player's private hand:
- a colour card adds its value to their matching colour total;
- a Gold card adds its value to their gold;
- a Church card sets their church_pending to true.
The kept card is never announced.
R8. The other drawn card becomes the lot and is announced to everyone. 'drawn' is emptied.

TALK.
R9. All three players, including the active player, each write one short message at the same moment, without seeing the others' messages. All three messages are then shown to everyone with who wrote them. Nothing said is binding. Players may propose prices, alliances or Church moves, bluff about their hands, or say nothing useful.

AUCTION.
R10. The two non-active players at the same moment each secretly bid a whole number from 0 up to their own current gold. The active player does not bid.
R11. If one bid is strictly greater than the other and is at least 1, that bidder wins the lot:
- they pay their bid from their gold to the active player's gold;
- the lot is added to their public bought list;
- a colour lot adds its value to their matching total, a Gold lot adds its value to their gold, and a Church lot sets their church_pending to true.
If the two bids are equal (including both 0), nobody pays and the lot is discarded.
R12. Both bids and the result (the winner and the price, or 'discarded') are announced to everyone. Then both bids are reset to 0 and lot becomes 'none'.

CHURCH.
R13. Every player whose church_pending is true chooses, at the same moment, one of: 'red up', 'red down', 'blue up', 'blue down', 'green up', 'green down'. The choice is stored as church_choice. At most two players can choose in a round: the active player through a kept Church, and the lot winner through a bought Church.
R14. For each colour, the net change is (number of '<colour> up' choices) minus (number of '<colour> down' choices) made this round. This net change is added to that colour's VP value, and the result is clamped once to between 1 and 5. All choices are announced with who made them. Then church_pending becomes false and church_choice becomes 'none' for everyone.
R15. If round is 12, go to END. Otherwise start the next round.

END.
R16. After round 12 the deck is empty. All hands, colour totals and gold are revealed.
R17. For each colour, if one player's total is strictly higher than both others, that player adds that colour's current VP value to their vp. If the highest total is tied between two or more players, nobody scores that colour.
R18. The highest vp wins. A tie on vp is broken by more remaining gold. If that is also tied, the game is a draw.

How the winner is decided: After 12 rounds, each colour's VP value (1 to 5) goes to the single player with the strictly highest total in that colour. A tied top total scores no one. The player with the highest vp wins. A tie on vp is broken by more remaining gold, and a further tie is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Biblios: Scriptorium Duel of Three (3 to 3 players, best with 3)

Three scribes take turns as the active seat. Each round the active seat secretly keeps one of two drawn cards, and the other two seats bid gold for the other card. Church cards shift colour values, and each colour scores for the single player with the strictly highest total.

STATE (every item below must exist in the file):
  - each player: hand (list, starts []); only its owner sees it. cards kept as the active player; never announced until the end
  - each player: bought (list, starts []); everyone sees it. lots this player won at auction
  - each player: red (number, starts 0); only its owner sees it. sum of the red card values held (hand plus bought)
  - each player: blue (number, starts 0); only its owner sees it. sum of the blue card values held
  - each player: green (number, starts 0); only its owner sees it. sum of the green card values held
  - each player: gold (number, starts 4); only its owner sees it. gold coins; hidden during play, revealed at scoring, used as the tie-break
  - each player: bid (number, starts 0); only its owner sees it. secret bid this round; announced after both bids are in, then reset to 0
  - each player: church_pending (bool, starts False); only its owner sees it. true if the player gained a Church card this round and must make a Church choice
  - each player: church_choice (text, starts 'none'); everyone sees it. the Church choice made this round
  - each player: message (text, starts ''); everyone sees it. this round's talk message
  - each player: vp (number, starts 0); everyone sees it. victory points, scored at the end
  - the table: deck (list, starts ['red-1', 'red-1', 'red-2', 'red-2', 'red-3', 'red-4', 'blue-1', 'blue-1', 'blue-2', 'blue-2', 'blue-3', 'blue-4', 'green-1', 'green-1', 'green-2', 'green-2', 'green-3', 'green-4', 'gold-2', 'gold-2', 'gold-3', 'gold-3', 'church', 'church']); hidden from all players. the shuffled deck; its order is unknown to all, and its composition is public
  - the table: drawn (list, starts []); hidden from all players. the two cards drawn this round; shown only to the active player
  - the table: lot (text, starts 'none'); everyone sees it. the card up for auction
  - the table: round (number, starts 0); everyone sees it. the current round number, 1 to 12
  - the table: active_seat (number, starts 0); everyone sees it. ((round-1) mod 3)+1
  - the table: vp_red (number, starts 3); everyone sees it. VP value of red, kept between 1 and 5
  - the table: vp_blue (number, starts 3); everyone sees it. VP value of blue, kept between 1 and 5
  - the table: vp_green (number, starts 3); everyone sees it. VP value of green, kept between 1 and 5
  - parameters, each kept as a table attribute: deck_size = 24, colour_cards = 18, colour_cards_per_colour = 6, colour_cards_value_1_per_colour = 2, colour_cards_value_2_per_colour = 2, colour_cards_value_3_per_colour = 1, colour_cards_value_4_per_colour = 1, gold_cards = 4, gold_cards_value_2 = 2, gold_cards_value_3 = 2, church_cards = 2, starting_gold = 4, starting_colour_vp = 3, vp_min = 1, vp_max = 5, rounds = 12, cards_drawn_per_round = 2, turns_active_per_seat = 4, min_winning_bid = 1, church_choices_max_per_round = 2, tiebreak_weight = 1000

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. The deck is filled with the 24 cards listed and is drawn from at random, which is equivalent to one shuffle; it is never reshuffled.
  2. Each player gets gold 4, red/blue/green 0, an empty hand and an empty bought list, bid 0, church_pending false, church_choice 'none', an empty message and vp 0.
  3. The table gets vp_red=3, vp_blue=3, vp_green=3, round=0, lot='none' and drawn empty.
  4. Each player is sent their own state.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] table. What happens: round += 1; active_seat = ((round-1) mod 3)+1; announce the round and the active seat.
  2. [update] table. What happens: Two cards are drawn at random from deck into drawn and removed from deck. They are shown only to the active seat.
  3. [ask] the active seat answers: one of the two cards in drawn. What happens: The chosen card is appended to the active player's hand. If it is red-v, blue-v or green-v, that colour total += v; if it is gold-v, gold += v; if it is church, church_pending = true. The choice is not announced.
  4. [update] table. What happens: The other drawn card becomes lot and is announced to everyone; drawn is emptied.
  5. [poll] all players answers: a short text message. What happens: message is set for each player; then broadcast {"to": "all", "text": "Seat {seat} says: {value}"}. Nothing said is binding.
  6. [poll] the two non-active seats answers: a whole number from 0 to the bidder's current gold. What happens: bid is set for each bidder and stays secret until both bids are in.
  7. [update] table. What happens: If one bid is strictly greater than the other and at least 1, that bidder: gold -= bid; the active player's gold += that bid; lot is appended to bought; a colour lot adds its value to that colour total, a gold lot adds its value to gold, and a church lot sets church_pending = true. If the bids are equal (including 0-0), nobody pays and the lot is discarded. Both bids and the result (the winner and the price, or 'discarded') are announced. Then both bids are reset to 0 and lot = 'none'.
  8. [poll] every player with church_pending true (at most two) answers: one of: red up, red down, blue up, blue down, green up, green down. What happens: church_choice is set for each chooser.
  9. [update] table. What happens: For each colour C: vp_C = min(5, max(1, vp_C + (count of 'C up') - (count of 'C down'))). All choices are announced with who made them. Then church_pending = false and church_choice = 'none' for everyone.
  10. [check] table. What happens: If round == 12, go to the end: reveal every hand, colour total and gold. For each colour C, a player whose C total is strictly greater than both other players' C totals gets vp += vp_C; a tied top total scores no one. Then the game ends. Otherwise continue.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. At the start the deck holds exactly 24 cards: red, blue and green each with values 1,1,2,2,3,4, plus gold-2, gold-2, gold-3, gold-3 and 2 church cards.
  R2. At the start each player has gold 4, red/blue/green 0, vp 0, an empty hand and an empty bought list.
  R3. At the start vp_red, vp_blue and vp_green are each 3.
  R4. In round r the active seat is ((r-1) mod 3)+1, so over 12 rounds each seat is active exactly 4 times.
  R5. Each round, 2 cards are removed from the deck into drawn, and only the active player is shown them.
  R6. When the active player keeps a colour card of value v, that colour total rises by v and the card goes to their hand unannounced.
  R7. When the active player keeps gold-v, their gold rises by v; when they keep church, their church_pending becomes true.
  R8. The drawn card that was not kept becomes the lot and is announced to everyone, and drawn is emptied.
  R9. Every round all 3 players simultaneously write one message, and all messages are then shown to everyone with the writer's seat.
  R10. Only the 2 non-active seats bid, simultaneously, each a whole number from 0 to their current gold.
  R11. When one bid is strictly higher and at least 1, that bidder pays the bid from their gold to the active player's gold and gains the lot in bought, with its colour value, gold value or church_pending applied.
  R12. When the two bids are equal (for example 2 and 2, or 0 and 0), nobody pays and the lot is discarded.
  R13. Both bids and the auction result are announced, then the bids reset to 0 and lot becomes 'none'.
  R14. Each player with church_pending true chooses one of red up, red down, blue up, blue down, green up, green down, simultaneously with any other chooser.
  R15. Each colour's VP value changes by (ups minus downs) this round and is then clamped once to 1..5: for example 5 with 1 up stays 5, and 3 with 1 up and 1 down stays 3.
  R16. After the Church step, every church_pending becomes false and every church_choice becomes 'none'.
  R17. The game ends after round 12, when the deck is empty.
  R18. At the end, a player whose total in a colour is strictly greater than both others' gains that colour's VP value in vp; if the top total is tied, nobody scores that colour.
  R19. The highest vp wins; tied vp is broken by more gold; a further tie is a shared win (draw).

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Keep a card | asked: the active seat only | options: exactly the two cards currently in drawn (if both are the same card, that card)
  - Talk | asked: all three seats | options: any short free-text message
  - Bid on the lot | asked: the two non-active seats; the active seat is not asked | options: whole numbers from 0 to the bidder's current gold
  - Church choice | asked: only seats with church_pending true; seats without a pending Church are not asked | options: red up, red down, blue up, blue down, green up, green down

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round == 12 after the Church step, with colour scoring applied
  - each player's standing: you.vp * 1000 + you.gold (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: The player with the highest vp wins. A tie on vp goes to the player with more remaining gold. Players still tied share the win, which is the source's draw.
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

- each player: `bought` (list, visible: public, starts []): lots this player won at auction
- each player: `gold` (number, visible: ally, starts 4): gold coins; hidden during play, revealed at scoring, used as the tie-break
- each player: `vp` (number, visible: public, starts 0): victory points, scored at the end
- the table: `round` (number, visible: public, starts 0): the current round number, 1 to 12
- the table: `vp_red` (number, visible: public, starts 3): VP value of red, kept between 1 and 5
- the table: `vp_blue` (number, visible: public, starts 3): VP value of blue, kept between 1 and 5
- the table: `vp_green` (number, visible: public, starts 3): VP value of green, kept between 1 and 5
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 24, colour_cards = 18, colour_cards_per_colour = 6, colour_cards_value_1_per_colour = 2, colour_cards_value_2_per_colour = 2, colour_cards_value_3_per_colour = 1, colour_cards_value_4_per_colour = 1, gold_cards = 4, gold_cards_value_2 = 2, gold_cards_value_3 = 2, church_cards = 2, starting_gold = 4, starting_colour_vp = 3, vp_min = 1, vp_max = 5, rounds = 12, cards_drawn_per_round = 2, turns_active_per_seat = 4, min_winning_bid = 1, church_choices_max_per_round = 2, tiebreak_weight = 1000
- the game ends with ONE ending whose `rank_by` is `you.vp * 1000 + you.gold`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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


YOUR PREVIOUS GAME FILE WAS REFUSED. Here it is:
```json
{
  "schema": 1,
  "meta": {
    "id": "biblios_duel_of_three",
    "name": "Biblios: Scriptorium Duel of Three",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Three scribes take turns keeping one of two drawn cards while the others bid gold for the second; Church cards shift colour values."
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
        "key": "hand",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "bought",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "red",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "blue",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "green",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "gold",
        "visible": "ally",
        "type": "number",
        "initial": 4
      },
      {
        "key": "bid",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "church_pending",
        "visible": "ally",
        "type": "bool",
        "initial": false
      },
      {
        "key": "church_choice",
        "visible": "public",
        "type": "text",
        "initial": "none"
      },
      {
        "key": "message",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "vp",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "keep_offer",
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
          "red-1",
          "red-1",
          "red-2",
          "red-2",
          "red-3",
          "red-4",
          "blue-1",
          "blue-1",
          "blue-2",
          "blue-2",
          "blue-3",
          "blue-4",
          "green-1",
          "green-1",
          "green-2",
          "green-2",
          "green-3",
          "green-4",
          "gold-2",
          "gold-2",
          "gold-3",
          "gold-3",
          "church",
          "church"
        ]
      },
      {
        "key": "drawn",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "lot",
        "visible": "public",
        "type": "text",
        "initial": "none"
      },
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
        "initial": 0
      },
      {
        "key": "vp_red",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "vp_blue",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "vp_green",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "kept",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "win_seat",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "price",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bids_shown",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "church_shown",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "final_shown",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 24
      },
      {
        "key": "colour_cards",
        "visible": "public",
        "type": "number",
        "initial": 18
      },
      {
        "key": "colour_cards_per_colour",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "colour_cards_value_1_per_colour",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "colour_cards_value_2_per_colour",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "colour_cards_value_3_per_colour",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "colour_cards_value_4_per_colour",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "gold_cards",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "gold_cards_value_2",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "gold_cards_value_3",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "church_cards",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "starting_gold",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "starting_colour_vp",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "vp_min",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "vp_max",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "cards_drawn_per_round",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "turns_active_per_seat",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "min_winning_bid",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "church_choices_max_per_round",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "tiebreak_weight",
        "visible": "public",
        "type": "number",
        "initial": 1000
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "fill the deck",
      "do": [
        {
          "set": {
            "key": "deck",
            "value": [
              "red-1",
              "red-1",
              "red-2",
              "red-2",
              "red-3",
              "red-4",
              "blue-1",
              "blue-1",
              "blue-2",
              "blue-2",
              "blue-3",
              "blue-4",
              "green-1",
              "green-1",
              "green-2",
              "green-2",
              "green-3",
              "green-4",
              "gold-2",
              "gold-2",
              "gold-3",
              "gold-3",
              "church",
              "church"
            ]
          }
        }
      ],
      "text": "The deck of {deck_size} cards is shuffled."
    },
    {
      "use": "update",
      "label": "the scribes",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "gold",
            "value": {
              "calc": "starting_gold"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "red",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "blue",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "green",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bought",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "church_pending",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "church_choice",
            "value": "none"
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
            "key": "vp",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "the table",
      "do": [
        {
          "set": {
            "key": "vp_red",
            "value": {
              "calc": "starting_colour_vp"
            }
          }
        },
        {
          "set": {
            "key": "vp_blue",
            "value": {
              "calc": "starting_colour_vp"
            }
          }
        },
        {
          "set": {
            "key": "vp_green",
            "value": {
              "calc": "starting_colour_vp"
            }
          }
        },
        {
          "set": {
            "key": "round",
            "value": 0
          }
        },
        {
          "set": {
            "key": "lot",
            "value": "none"
          }
        },
        {
          "set": {
            "key": "drawn",
            "value": []
          }
        }
      ]
    },
    {
      "use": "sync",
      "label": "your state",
      "mode": "self",
      "to": "all",
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "draw",
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
              "calc": "((round - 1) % len(players)) + 1"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "message",
            "value": ""
          }
        }
      ],
      "text": "Round {round} of {rounds}: seat {active_seat} is the active seat."
    },
    {
      "use": "update",
      "phase": "draw",
      "label": "the draw",
      "do": [
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
            "key": "drawn",
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
            "key": "drawn",
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
            "players": "all",
            "key": "keep_offer",
            "value": {
              "calc": "([drawn[0]] + ([drawn[1]] if drawn[1] != drawn[0] else [])) if you.seat == active_seat else []"
            }
          }
        }
      ],
      "text": "Seat {active_seat} draws {cards_drawn_per_round} cards in secret."
    },
    {
      "use": "ask",
      "phase": "keep",
      "label": "keep a card",
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "keep_offer"
        }
      },
      "verify": {
        "bind": "kept_card"
      },
      "text": "You are the active seat. You drew {drawn}. Keep one card in your private hand; the other goes up for auction and the other two seats bid gold for it, paid to you."
    },
    {
      "use": "update",
      "phase": "keep",
      "label": "the kept card",
      "do": [
        {
          "set": {
            "key": "kept",
            "value": "$kept_card"
          }
        },
        {
          "append": {
            "player": {
              "calc": "active_seat"
            },
            "key": "hand",
            "value": {
              "calc": "kept"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "active_seat"
            },
            "key": "red",
            "value": {
              "calc": "int(kept[len(kept) - 1])"
            },
            "if": {
              "calc": "kept in ['red-1', 'red-2', 'red-3', 'red-4']"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "active_seat"
            },
            "key": "blue",
            "value": {
              "calc": "int(kept[len(kept) - 1])"
            },
            "if": {
              "calc": "kept in ['blue-1', 'blue-2', 'blue-3', 'blue-4']"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "active_seat"
            },
            "key": "green",
            "value": {
              "calc": "int(kept[len(kept) - 1])"
            },
            "if": {
              "calc": "kept in ['green-1', 'green-2', 'green-3', 'green-4']"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "active_seat"
            },
            "key": "gold",
            "value": {
              "calc": "int(kept[len(kept) - 1])"
            },
            "if": {
              "calc": "kept in ['gold-2', 'gold-3']"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "active_seat"
            },
            "key": "church_pending",
            "value": true,
            "if": {
              "calc": "kept == 'church'"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "keep",
      "label": "the lot",
      "do": [
        {
          "set": {
            "key": "lot",
            "value": {
              "calc": "drawn[1] if drawn[0] == kept else drawn[0]"
            }
          }
        },
        {
          "set": {
            "key": "drawn",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "keep_offer",
            "value": []
          }
        }
      ],
      "text": "Seat {active_seat} has kept one card. The lot up for auction is {lot}."
    },
    {
      "use": "poll",
      "phase": "talk",
      "label": "talk",
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
      "text": "Write one short message to the table. The lot is {lot}; seat {active_seat} is active. Nothing said is binding: propose prices, alliances or Church moves, bluff, or say nothing useful."
    },
    {
      "use": "poll",
      "phase": "auction",
      "label": "bid on the lot",
      "to": {
        "where": "you.seat != active_seat"
      },
      "answer": {
        "type": "number",
        "min": 0,
        "max": {
          "calc": "you.gold"
        }
      },
      "store": "bid",
      "text": "Bid in secret for the lot {lot}: a whole number from 0 up to your gold. If your bid is strictly higher than the other bid and at least {min_winning_bid}, you pay it to seat {active_seat} and take the lot; if the bids are equal, nobody pays and the lot is discarded."
    },
    {
      "use": "update",
      "phase": "auction",
      "label": "the auction result",
      "do": [
        {
          "set": {
            "key": "bids_shown",
            "value": {
              "calc": "[[p.seat, p.bid] for p in players if p.seat != active_seat]"
            },
            "text": "Bids [seat, bid]: {value}."
          }
        },
        {
          "set": {
            "key": "win_seat",
            "value": {
              "calc": "max([p.seat for p in players if p.seat != active_seat and p.bid >= min_winning_bid and all(p.bid > q.bid for q in players if q.seat != active_seat and q.seat != p.seat)] + [0])"
            }
          }
        },
        {
          "set": {
            "key": "price",
            "value": {
              "calc": "max([p.bid for p in players if p.seat == win_seat] + [0])"
            }
          }
        },
        {
          "set": {
            "key": "lot",
            "value": "none",
            "if": {
              "calc": "win_seat == 0"
            },
            "text": "The bids are equal: nobody pays and the lot is discarded."
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "win_seat"
            },
            "key": "gold",
            "value": {
              "calc": "-price"
            },
            "if": {
              "calc": "win_seat > 0"
            },
            "text": "Seat {player} wins the {lot} for {price} gold, paid to seat {active_seat}."
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "active_seat"
            },
            "key": "gold",
            "value": {
              "calc": "price"
            },
            "if": {
              "calc": "win_seat > 0"
            }
          }
        },
        {
          "append": {
            "player": {
              "calc": "win_seat"
            },
            "key": "bought",
            "value": {
              "calc": "lot"
            },
            "if": {
              "calc": "win_seat > 0"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "win_seat"
            },
            "key": "red",
            "value": {
              "calc": "int(lot[len(lot) - 1])"
            },
            "if": {
              "calc": "win_seat > 0 and lot in ['red-1', 'red-2', 'red-3', 'red-4']"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "win_seat"
            },
            "key": "blue",
            "value": {
              "calc": "int(lot[len(lot) - 1])"
            },
            "if": {
              "calc": "win_seat > 0 and lot in ['blue-1', 'blue-2', 'blue-3', 'blue-4']"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "win_seat"
            },
            "key": "green",
            "value": {
              "calc": "int(lot[len(lot) - 1])"
            },
            "if": {
              "calc": "win_seat > 0 and lot in ['green-1', 'green-2', 'green-3', 'green-4']"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "win_seat"
            },
            "key": "gold",
            "value": {
              "calc": "int(lot[len(lot) - 1])"
            },
            "if": {
              "calc": "win_seat > 0 and lot in ['gold-2', 'gold-3']"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "win_seat"
            },
            "key": "church_pending",
            "value": true,
            "if": {
              "calc": "win_seat > 0 and lot == 'church'"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": 0
          }
        },
        {
          "set": {
            "key": "lot",
            "value": "none"
          }
        }
      ]
    },
    {
      "use": "poll",
      "phase": "church",
      "label": "church choice",
      "when": {
        "calc": "count(p.church_pending for p in players) > 0"
      },
      "to": {
        "where": "you.church_pending"
      },
      "answer": {
        "type": "choice",
        "options": [
          "red up",
          "red down",
          "blue up",
          "blue down",
          "green up",
          "green down"
        ]
      },
      "store": "church_choice",
      "text": "You gained a Church card this round. Choose one colour to move up or down by 1. All choices this round are added together, then each colour value is kept between {vp_min} and {vp_max}. Current values: red {vp_red}, blue {vp_blue}, green {vp_green}."
    },
    {
      "use": "update",
      "phase": "church",
      "label": "the church resolves",
      "do": [
        {
          "set": {
            "key": "church_shown",
            "value": {
              "calc": "[[p.seat, p.church_choice] for p in players if p.church_choice != 'none']"
            },
            "if": {
              "calc": "count(p.church_choice != 'none' for p in players) > 0"
            },
            "text": "Church choices [seat, choice]: {value}."
          }
        },
        {
          "set": {
            "key": "vp_red",
            "value": {
              "calc": "min(vp_max, max(vp_min, vp_red + count(p.church_choice == 'red up' for p in players) - count(p.church_choice == 'red down' for p in players)))"
            }
          }
        },
        {
          "set": {
            "key": "vp_blue",
            "value": {
              "calc": "min(vp_max, max(vp_min, vp_blue + count(p.church_choice == 'blue up' for p in players) - count(p.church_choice == 'blue down' for p in players)))"
            }
          }
        },
        {
          "set": {
            "key": "vp_green",
            "value": {
              "calc": "min(vp_max, max(vp_min, vp_green + count(p.church_choice == 'green up' for p in players) - count(p.church_choice == 'green down' for p in players)))"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "church_pending",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "church_choice",
            "value": "none"
          }
        }
      ],
      "text": "Colour values: red {vp_red}, blue {vp_blue}, green {vp_green}."
    },
    {
      "use": "update",
      "phase": "scoring",
      "label": "final scoring",
      "when": {
        "calc": "round >= rounds"
      },
      "do": [
        {
          "set": {
            "key": "final_shown",
            "value": {
              "calc": "[[p.seat, p.red, p.blue, p.green, p.gold, p.hand] for p in players]"
            },
            "text": "Revealed [seat, red, blue, green, gold, hand]: {value}."
          }
        },
        {
          "adjust": {
            "players": {
              "where": "all(you.red > p.red for p in players if p.seat != you.seat)"
            },
            "k
... (cut)

Why it was refused: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (message, message, message) in `your_state`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "biblios_duel_of_three",
    "name": "Biblios: Scriptorium Duel of Three",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Three scribes take turns keeping one of two drawn cards while the others bid gold for the second; Church cards shift colour values."
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
        "key": "hand",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "bought",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "red",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "blue",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "green",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "gold",
        "visible": "ally",
        "type": "number",
        "initial": 4
      },
      {
        "key": "bid",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "church_pending",
        "visible": "ally",
        "type": "bool",
        "initial": false
      },
      {
        "key": "church_choice",
        "visible": "public",
        "type": "text",
        "initial": "none"
      },
      {
        "key": "message",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "vp",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "keep_offer",
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
          "red-1",
          "red-1",
          "red-2",
          "red-2",
          "red-3",
          "red-4",
          "blue-1",
          "blue-1",
          "blue-2",
          "blue-2",
          "blue-3",
          "blue-4",
          "green-1",
          "green-1",
          "green-2",
          "green-2",
          "green-3",
          "green-4",
          "gold-2",
          "gold-2",
          "gold-3",
          "gold-3",
          "church",
          "church"
        ]
      },
      {
        "key": "drawn",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "lot",
        "visible": "public",
        "type": "text",
        "initial": "none"
      },
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
        "initial": 0
      },
      {
        "key": "vp_red",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "vp_blue",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "vp_green",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "kept",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "win_seat",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "price",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bids_shown",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "church_shown",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "final_shown",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 24
      },
      {
        "key": "colour_cards",
        "visible": "public",
        "type": "number",
        "initial": 18
      },
      {
        "key": "colour_cards_per_colour",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "colour_cards_value_1_per_colour",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "colour_cards_value_2_per_colour",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "colour_cards_value_3_per_colour",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "colour_cards_value_4_per_colour",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "gold_cards",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "gold_cards_value_2",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "gold_cards_value_3",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "church_cards",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "starting_gold",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "starting_colour_vp",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "vp_min",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "vp_max",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "cards_drawn_per_round",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "turns_active_per_seat",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "min_winning_bid",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "church_choices_max_per_round",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "tiebreak_weight",
        "visible": "public",
        "type": "number",
        "initial": 1000
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "fill the deck",
      "do": [
        {
          "set": {
            "key": "deck",
            "value": [
              "red-1",
              "red-1",
              "red-2",
              "red-2",
              "red-3",
              "red-4",
              "blue-1",
              "blue-1",
              "blue-2",
              "blue-2",
              "blue-3",
              "blue-4",
              "green-1",
              "green-1",
              "green-2",
              "green-2",
              "green-3",
              "green-4",
              "gold-2",
              "gold-2",
              "gold-3",
              "gold-3",
              "church",
              "church"
            ]
          }
        }
      ],
      "text": "The deck of {deck_size} cards is shuffled."
    },
    {
      "use": "update",
      "label": "the scribes",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "gold",
            "value": {
              "calc": "starting_gold"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "red",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "blue",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "green",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bought",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "church_pending",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "church_choice",
            "value": "none"
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
            "key": "vp",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "the table",
      "do": [
        {
          "set": {
            "key": "vp_red",
            "value": {
              "calc": "starting_colour_vp"
            }
          }
        },
        {
          "set": {
            "key": "vp_blue",
            "value": {
              "calc": "starting_colour_vp"
            }
          }
        },
        {
          "set": {
            "key": "vp_green",
            "value": {
              "calc": "starting_colour_vp"
            }
          }
        },
        {
          "set": {
            "key": "round",
            "value": 0
          }
        },
        {
          "set": {
            "key": "lot",
            "value": "none"
          }
        },
        {
          "set": {
            "key": "drawn",
            "value": []
          }
        }
      ]
    },
    {
      "use": "sync",
      "label": "your state",
      "mode": "self",
      "to": "all",
      "fields": [
        "gold",
        "red",
        "blue",
        "green",
        "vp"
      ],
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "draw",
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
              "calc": "((round - 1) % len(players)) + 1"
            }
          }
        }
      ],
      "text": "Round {round} of {rounds}: seat {active_seat} is the active seat."
    },
    {
      "use": "update",
      "phase": "draw",
      "label": "the draw",
      "do": [
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
            "key": "drawn",
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
            "key": "drawn",
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
            "players": "all",
            "key": "keep_offer",
            "value": {
              "calc": "([drawn[0]] + ([drawn[1]] if drawn[1] != drawn[0] else [])) if you.seat == active_seat else []"
            }
          }
        }
      ],
      "text": "Seat {active_seat} draws {cards_drawn_per_round} cards in secret."
    },
    {
      "use": "ask",
      "phase": "keep",
      "label": "keep a card",
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "keep_offer"
        }
      },
      "verify": {
        "bind": "kept_card"
      },
      "text": "You are the active seat. You drew {drawn}. Keep one card in your private hand; the other goes up for auction and the other two seats bid gold for it, paid to you."
    },
    {
      "use": "update",
      "phase": "keep",
      "label": "the kept card",
      "do": [
        {
          "set": {
            "key": "kept",
            "value": "$kept_card"
          }
        },
        {
          "append": {
            "player": {
              "calc": "active_seat"
            },
            "key": "hand",
            "value": {
              "calc": "kept"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "active_seat"
            },
            "key": "red",
            "value": {
              "calc": "int(kept[len(kept) - 1])"
            },
            "if": {
              "calc": "kept in ['red-1', 'red-2', 'red-3', 'red-4']"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "active_seat"
            },
            "key": "blue",
            "value": {
              "calc": "int(kept[len(kept) - 1])"
            },
            "if": {
              "calc": "kept in ['blue-1', 'blue-2', 'blue-3', 'blue-4']"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "active_seat"
            },
            "key": "green",
            "value": {
              "calc": "int(kept[len(kept) - 1])"
            },
            "if": {
              "calc": "kept in ['green-1', 'green-2', 'green-3', 'green-4']"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "active_seat"
            },
            "key": "gold",
            "value": {
              "calc": "int(kept[len(kept) - 1])"
            },
            "if": {
              "calc": "kept in ['gold-2', 'gold-3']"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "active_seat"
            },
            "key": "church_pending",
            "value": true,
            "if": {
              "calc": "kept == 'church'"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "keep",
      "label": "the lot",
      "do": [
        {
          "set": {
            "key": "lot",
            "value": {
              "calc": "drawn[1] if drawn[0] == kept else drawn[0]"
            }
          }
        },
        {
          "set": {
            "key": "drawn",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "keep_offer",
            "value": []
          }
        }
      ],
      "text": "Seat {active_seat} has kept one card. The lot up for auction is {lot}."
    },
    {
      "use": "poll",
      "phase": "talk",
      "label": "talk",
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
      "text": "Write one short message to the table. The lot is {lot}; seat {active_seat} is active. Nothing said is binding: propose prices, alliances or Church moves, bluff, or say nothing useful."
    },
    {
      "use": "poll",
      "phase": "auction",
      "label": "bid on the lot",
      "to": {
        "where": "you.seat != active_seat"
      },
      "answer": {
        "type": "number",
        "min": 0,
        "max": {
          "calc": "you.gold"
        }
      },
      "store": "bid",
      "text": "Bid in secret for the lot {lot}: a whole number from 0 up to your gold. If your bid is strictly higher than the other bid and at least {min_winning_bid}, you pay it to seat {active_seat} and take the lot; if the bids are equal, nobody pays and the lot is discarded."
    },
    {
      "use": "update",
      "phase": "auction",
      "label": "the auction result",
      "do": [
        {
          "set": {
            "key": "bids_shown",
            "value": {
              "calc": "[[p.seat, p.bid] for p in players if p.seat != active_seat]"
            },
            "text": "Bids [seat, bid]: {value}."
          }
        },
        {
          "set": {
            "key": "win_seat",
            "value": {
              "calc": "max([p.seat for p in players if p.seat != active_seat and p.bid >= min_winning_bid and all(p.bid > q.bid for q in players if q.seat != active_seat and q.seat != p.seat)] + [0])"
            }
          }
        },
        {
          "set": {
            "key": "price",
            "value": {
              "calc": "max([p.bid for p in players if p.seat == win_seat] + [0])"
            }
          }
        },
        {
          "set": {
            "key": "lot",
            "value": "none",
            "if": {
              "calc": "win_seat == 0"
            },
            "text": "The bids are equal: nobody pays and the lot is discarded."
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "win_seat"
            },
            "key": "gold",
            "value": {
              "calc": "-price"
            },
            "if": {
              "calc": "win_seat > 0"
            },
            "text": "Seat {player} wins the {lot} for {price} gold, paid to seat {active_seat}."
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "active_seat"
            },
            "key": "gold",
            "value": {
              "calc": "price"
            },
            "if": {
              "calc": "win_seat > 0"
            }
          }
        },
        {
          "append": {
            "player": {
              "calc": "win_seat"
            },
            "key": "bought",
            "value": {
              "calc": "lot"
            },
            "if": {
              "calc": "win_seat > 0"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "win_seat"
            },
            "key": "red",
            "value": {
              "calc": "int(lot[len(lot) - 1])"
            },
            "if": {
              "calc": "win_seat > 0 and lot in ['red-1', 'red-2', 'red-3', 'red-4']"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "win_seat"
            },
            "key": "blue",
            "value": {
              "calc": "int(lot[len(lot) - 1])"
            },
            "if": {
              "calc": "win_seat > 0 and lot in ['blue-1', 'blue-2', 'blue-3', 'blue-4']"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "win_seat"
            },
            "key": "green",
            "value": {
              "calc": "int(lot[len(lot) - 1])"
            },
            "if": {
              "calc": "win_seat > 0 and lot in ['green-1', 'green-2', 'green-3', 'green-4']"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "win_seat"
            },
            "key": "gold",
            "value": {
              "calc": "int(lot[len(lot) - 1])"
            },
            "if": {
              "calc": "win_seat > 0 and lot in ['gold-2', 'gold-3']"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "win_seat"
            },
            "key": "church_pending",
            "value": true,
            "if": {
              "calc": "win_seat > 0 and lot == 'church'"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": 0
          }
        },
        {
          "set": {
            "key": "lot",
            "value": "none"
          }
        }
      ]
    },
    {
      "use": "poll",
      "phase": "church",
      "label": "church choice",
      "when": {
        "calc": "count(p.church_pending for p in players) > 0"
      },
      "to": {
        "where": "you.church_pending"
      },
      "answer": {
        "type": "choice",
        "options": [
          "red up",
          "red down",
          "blue up",
          "blue down",
          "green up",
          "green down"
        ]
      },
      "store": "church_choice",
      "text": "You gained a Church card this round. Choose one colour to move up or down by 1. All choices this round are added together, then each colour value is kept between {vp_min} and {vp_max}. Current values: red {vp_red}, blue {vp_blue}, green {vp_green}."
    },
    {
      "use": "update",
      "phase": "church",
      "label": "the church resolves",
      "do": [
        {
          "set": {
            "key": "church_shown",
            "value": {
              "calc": "[[p.seat, p.church_choice] for p in players if p.church_choice != 'none']"
            },
            "if": {
              "calc": "count(p.church_choice != 'none' for p in players) > 0"
            },
            "text": "Church choices [seat, choice]: {value}."
          }
        },
        {
          "set": {
            "key": "vp_red",
            "value": {
              "calc": "min(vp_max, max(vp_min, vp_red + count(p.church_choice == 'red up' for p in players) - count(p.church_choice == 'red down' for p in players)))"
            }
          }
        },
        {
          "set": {
            "key": "vp_blue",
            "value": {
              "calc": "min(vp_max, max(vp_min, vp_blue + count(p.church_choice == 'blue up' for p in players) - count(p.church_choice == 'blue down' for p in players)))"
            }
          }
        },
        {
          "set": {
            "key": "vp_green",
            "value": {
              "calc": "min(vp_max, max(vp_min, vp_green + count(p.church_choice == 'green up' for p in players) - count(p.church_choice == 'green down' for p in players)))"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "church_pending",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "church_choice",
            "value": "none"
          }
        }
      ],
      "text": "Colour values: red {vp_red}, blue {vp_blue}, green {vp_green}."
    },
    {
      "use": "update",
      "phase": "scoring",
      "label": "final scoring",
      "when": {
        "calc": "round >= rounds"
      },
      "do": [
        {
          "set": {
            "key": "final_shown",
            "value": {
              "calc": "[[p.seat, p.red, p.blue, p.green, p.gold, p.hand] for p in players]"
            },
            "text": "Revealed [seat, red, blue, green, gold, hand]: {value}."
          }
        },
        {
          "adjust": {
            "players": {
              "where": "all(you.red > p.red for p in players if p.seat != you.seat)"
            },
            "key": "vp",
            "value": {
              "calc": "vp_red"
            },
            "text": "Seat {player} has the most red and scores {vp_red}."
          }
        },
        {
          "adjust": {
            "players": {
              "where": "all(you.blue > p.blue for p in players if p.seat != you.seat)"
            },
            "key": "vp",
            "value": {
              "calc": "vp_blue"
            },
            "text": "Seat {player} has the most blue and scores {vp_blue}."
          }
        },
        {
          "adjust": {
            "players": {
              "where": "all(you.green > p.green for p in players if p.seat != you.seat)"
            },
            "key": "vp",
            "value": {
              "calc": "vp_green"
            },
            "text": "Seat {player} has the most green and scores {vp_green}."
          }
        }
      ],
      "text": "Final colour values: red {vp_red}, blue {vp_blue}, green {vp_green}."
    },
    {
      "use": "check",
      "phase": "scoring",
      "label": "after the last round",
      "when": {
        "calc": "round >= rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round >= rounds"
      },
      "rank_by": "you.vp * 1000 + you.gold",
      "reveal": [
        "hand",
        "red",
        "blue",
        "green",
        "gold"
      ],
      "text": "Winner: {result}. Final VP (gold): Seat 1 {players[0].vp} ({players[0].gold}), Seat 2 {players[1].vp} ({players[1].gold}), Seat 3 {players[2].vp} ({players[2].gold})."
    }
  },
  "limits": {
    "rounds": 12,
    "rounds_max": 12,
    "actions_max": 400,
    "deadline_s": 120
  },
  "rules": "SETUP. The deck holds {deck_size} cards: red, blue and green, each with values 1,1,2,2,3,4 (written like 'red-1'), {colour_cards} cards; Gold cards with values 2,2,3,3 (written like 'gold-2'), {gold_cards} cards; and {church_cards} Church cards ('church'). The deck is shuffled once at the start and never again. Each player starts with {starting_gold} gold, an empty private hand, an empty public bought list, and red, blue and green totals of 0. Each colour's VP value starts at {starting_colour_vp}. Your hand, colour totals and gold are known only to you; your bought list is public. All gold is revealed at scoring.\n\nEACH ROUND ({rounds} rounds). In round r the active seat is ((r-1) mod 3)+1, so seats go 1,2,3,1,2,3,... and each seat is active exactly {turns_active_per_seat} times. The first {cards_drawn_per_round} cards of the deck are drawn; only the active player sees them.\n\nKEEP. The active player alone chooses one of the two drawn cards to keep. The kept card goes into their private hand: a colour card adds its value to their matching colour total; a Gold card adds its value to their gold; a Church card means they make a Church choice this round. The kept card is never announced. The other drawn card becomes the lot and is announced to everyone.\n\nTALK. All three players, including the active player, each write one short message at the same moment, without seeing the others' messages. All three are then shown to everyone with who wrote them. Nothing said is binding.\n\nAUCTION. The two non-active players at the same moment each secretly bid a whole number from 0 up to their own current gold. The active player does not bid. If one bid is strictly greater than the other and is at least {min_winning_bid}, that bidder wins the lot: they pay their bid from their gold to the active player's gold, the lot is added to their public bought list, and a colour lot adds its value to their matching total, a Gold lot adds its value to their gold, and a Church lot means they make a Church choice this round. If the two bids are equal (including both 0), nobody pays and the lot is discarded. Both bids and the result (the winner and the price, or 'discarded') are announced to everyone.\n\nCHURCH. Every player who gained a Church card this round chooses, at the same moment, one of: red up, red down, blue up, blue down, green up, green down. At most {church_choices_max_per_round} players can choose in a round. For each colour, the net change is the number of 'up' choices minus the number of 'down' choices this round; it is added to that colour's VP value, and the result is clamped once to between {vp_min} and {vp_max} (5 with 1 up stays 5; 3 with 1 up and 1 down stays 3). All choices are announced with who made them. Players without a Church card are not asked.\n\nEND. After round {rounds} the deck is empty. All hands, colour totals and gold are revealed. For each colour, if one player's total is strictly higher than both others, that player adds that colour's current VP value to their vp. If the highest total is tied between two or more players, nobody scores that colour. The highest vp wins. A tie on vp is broken by more remaining gold. If that is also tied, the tied players share the win (a draw)."
}
```
````
