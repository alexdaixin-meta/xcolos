# Task: write the XColos game file for "Jaipur Bazaar (Balanced Schedule)"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 2; set `meta.players` to {"min": 2, "max": 2, "suggested": 2} (the suggested size is the one the game plays best at).

CARDS AND STATE
- There are three goods types (Diamond, Silver, Cloth) and camels.
- Each player has a hidden hand, recorded as counts of Diamond, Silver and Cloth. Each player also has a public camel herd (a count) and a public score.
- The market is public and holds counts of Diamond, Silver, Cloth and Camel.
- Each good has a public price. The starting prices are Diamond 7, Silver 5, Cloth 3.
- A private deck of 20 goods cards is shuffled once at the start: 5 Diamond, 7 Silver, 8 Cloth. The composition is public.

SETUP
- The market starts with 2 Camel, 1 Silver and 1 Cloth.
- Each player starts with 1 Silver and 1 Cloth in hand, 1 camel in herd, and score 0.

TURN ORDER
- The round's first player is:
  - A in rounds 1, 4, 5, 8, 9, 12, 13 and 16;
  - B in rounds 2, 3, 6, 7, 10, 11, 14 and 15.
- The other player is second in that round.

EACH ROUND (16 rounds)
1. Restock: add one card to the market according to this public schedule.
   - Rounds 1 and 2: Cloth. Rounds 3 and 4: Silver. Rounds 5 and 6: Camel. Rounds 7 and 8: Diamond.
   - Rounds 9 and 10: Cloth. Rounds 11 and 12: Silver. Rounds 13 and 14: Diamond. Rounds 15 and 16: Camel.
2. Private draw: the round's first player draws the top deck card into their hand.
   - Only they see its type. Both players are told that a draw happened.
   - If that hand already holds 7 goods, the drawn card is discarded instead, and only the drawer learns its type.
3. The first player takes one turn, which is announced publicly.
4. The second player takes one turn, which is announced publicly.

A TURN: choose exactly one action.
- TAKE <good> <n>: take n cards (n at least 1) of one goods type from the market into your hand. Three conditions apply:
  - the market must hold at least n of that type;
  - you must return n-1 camels from your herd to the market, so you must own at least n-1 camels;
  - your hand must hold at most 7 goods afterwards.
- CAMELS: move all camels in the market into your herd. The market must hold at least 1 camel.
- SELL <good> <n>: discard n cards of one good from your hand.
  - Diamond and Silver need n of at least 2. Cloth needs n of at least 1.
  - You score n times that good's current price.
  - You also score a bonus: +3 if n is 3, +5 if n is 4, +8 if n is 5 or more.
  - Then that good's price drops by n, to a minimum of 1.
- An illegal or missing choice counts as a pass: nothing happens.
- What is announced publicly: the action type, the good and n. The type of a privately drawn card is never announced.

END
- After round 16, the player with strictly more camels in their herd scores +5. If camels are tied, nobody gets the bonus.
- Cards left in hand score nothing.

How the winner is decided: After the camel bonus, the player with the higher score wins. Equal scores are a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Jaipur Bazaar (Balanced Schedule) (2 to 2 players, best with 2)

Two traders take turns over 16 rounds, taking goods and camels from a public market and selling sets of goods for falling prices. A camel-majority bonus is paid at the end, and the higher score wins.

STATE (every item below must exist in the file):
  - each player: diamond (number, starts 0); only its owner sees it. Diamond cards in this player's hidden hand
  - each player: silver (number, starts 1); only its owner sees it. Silver cards in this player's hidden hand
  - each player: cloth (number, starts 1); only its owner sees it. Cloth cards in this player's hidden hand
  - each player: camels (number, starts 1); everyone sees it. Camels in this player's public herd
  - each player: score (number, starts 0); everyone sees it. Points scored from sales and the camel bonus
  - each player: last_draw (text, starts ''); only its owner sees it. Type of the card this player most recently drew privately, and whether it was kept or discarded
  - the table: round (number, starts 0); everyone sees it. Current round, 1 to 16
  - the table: first_seat (number, starts 1); everyone sees it. Seat that acts first this round: seat 1 (A) in rounds 1,4,5,8,9,12,13,16 and seat 2 (B) otherwise
  - the table: market_diamond (number, starts 0); everyone sees it. Diamond cards in the market
  - the table: market_silver (number, starts 1); everyone sees it. Silver cards in the market
  - the table: market_cloth (number, starts 1); everyone sees it. Cloth cards in the market
  - the table: market_camel (number, starts 2); everyone sees it. Camel cards in the market
  - the table: price_diamond (number, starts 7); everyone sees it. Current Diamond price
  - the table: price_silver (number, starts 5); everyone sees it. Current Silver price
  - the table: price_cloth (number, starts 3); everyone sees it. Current Cloth price
  - the table: deck (list, starts '5 x Diamond, 7 x Silver, 8 x Cloth, shuffled'); hidden from all players. Private goods deck whose composition is public but whose order is hidden
  - the table: discard (list, starts []); hidden from all players. Cards discarded by sales and by draws into a full hand
  - the table: last_action (text, starts ''); everyone sees it. Publicly announced action type, good and n of the most recent turn
  - parameters, each kept as a table attribute: rounds = 16, price_diamond_start = 7, price_silver_start = 5, price_cloth_start = 3, deck_diamond = 5, deck_silver = 7, deck_cloth = 8, deck_size = 20, market_camel_start = 2, market_silver_start = 1, market_cloth_start = 1, market_diamond_start = 0, start_hand_silver = 1, start_hand_cloth = 1, start_camels = 1, start_score = 0, hand_limit = 7, restock_per_round = 1, draws_per_round = 1, take_min = 1, sell_min_diamond = 2, sell_min_silver = 2, sell_min_cloth = 1, bonus_sell_3 = 3, bonus_sell_4 = 5, bonus_sell_5_plus = 8, price_floor = 1, camel_majority_bonus = 5

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Shuffle the 20-card deck (5 Diamond, 7 Silver, 8 Cloth) into the hidden table list deck.
  2. Set the market to 2 Camel, 1 Silver, 1 Cloth and 0 Diamond.
  3. Set prices to Diamond 7, Silver 5 and Cloth 3.
  4. Give each player 1 Silver and 1 Cloth in hand (hidden), 1 camel in herd (public) and score 0.
  5. Sync each player their own state, and tell everyone that the deck composition is 5 Diamond, 7 Silver and 8 Cloth.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round += 1; first_seat = 1 if round in {1,4,5,8,9,12,13,16} else 2. Announce the round and the first seat.
  2. [update] all players. What happens: Restock by the public schedule: market_cloth += 1 if round in {1,2,9,10}; market_silver += 1 if round in {3,4,11,12}; market_camel += 1 if round in {5,6,15,16}; market_diamond += 1 if round in {7,8,13,14}. Announce the card added.
  3. [update] seat first_seat. What happens: Private draw: remove one random card from deck. If first player's diamond+silver+cloth < 7, add 1 to that player's matching count; otherwise append the card to discard. Set that player's last_draw to the card type and kept/discarded. Tell all players only that a draw happened.
  4. [sync] seat first_seat. What happens: The first player sees their own hand, including the drawn card type (last_draw), plus all public state.
  5. [ask] seat first_seat answers: one choice from the legal actions: TAKE <good> <n>, CAMELS, or SELL <good> <n> (see offers). What happens: TAKE g n (when market_g >= n, camels >= n-1, and diamond+silver+cloth+n <= 7): market_g -= n, player g += n, camels -= n-1, market_camel += n-1. CAMELS (when market_camel >= 1): camels += market_camel, market_camel = 0. SELL g n (when player g >= n, and n >= 2 for diamond/silver or n >= 1 for cloth): player g -= n, append n cards to discard, score += n*price_g + (3 if n==3, 5 if n==4, 8 if n>=5, else 0), price_g = max(1, price_g - n). An illegal or missing answer is a pass: nothing changes. Set last_action to the action type, good and n.
  6. [tell] all players. What happens: Announce publicly: 'Seat {first_seat} did {last_action}', then the market, prices, herds and scores. No drawn card type is announced.
  7. [sync] the seat that is not first_seat. What happens: The second player sees their own hand and all public state.
  8. [ask] the seat that is not first_seat answers: one choice from the legal actions: TAKE <good> <n>, CAMELS, or SELL <good> <n> (see offers). What happens: Same resolution as the first player's turn, applied to the second player. An illegal or missing answer is a pass. Set last_action.
  9. [tell] all players. What happens: Announce publicly: 'Seat {second seat} did {last_action}', then the market, prices, herds and scores.
  10. [update] all players. What happens: When round == 16: if seat 1 camels > seat 2 camels, seat 1 score += 5; if seat 2 camels > seat 1 camels, seat 2 score += 5; if they are tied, no change. Cards left in hand score nothing. Announce the final scores.
  11. [check] all players. What happens: End the game when round == 16; otherwise continue to the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. At setup the market holds 2 Camel, 1 Silver, 1 Cloth and 0 Diamond, and prices are Diamond 7, Silver 5, Cloth 3.
  R2. At setup each player holds 1 Silver and 1 Cloth in a hidden hand, has 1 public camel and has score 0.
  R3. The deck starts with 20 hidden cards: 5 Diamond, 7 Silver and 8 Cloth.
  R4. When the round is 1, 4, 5, 8, 9, 12, 13 or 16, seat 1 (A) acts first; in rounds 2, 3, 6, 7, 10, 11, 14 and 15, seat 2 (B) acts first.
  R5. At the start of rounds 1, 2, 9 and 10, market_cloth increases by 1.
  R6. At the start of rounds 3, 4, 11 and 12, market_silver increases by 1.
  R7. At the start of rounds 5, 6, 15 and 16, market_camel increases by 1.
  R8. At the start of rounds 7, 8, 13 and 14, market_diamond increases by 1.
  R9. Each round the first player draws one card from the deck, so the deck shrinks by exactly 1 per round.
  R10. When the first player's hand holds fewer than 7 goods, the drawn card is added to the matching hand count; when it holds 7, the card goes to the discard and the hand is unchanged.
  R11. The type of a drawn card is never announced publicly; both players are told only that a draw happened.
  R12. When a player chooses TAKE g n with market_g >= n, camels >= n-1 and hand + n <= 7, then market_g drops by n, their hand count g rises by n, their camels drop by n-1 and market_camel rises by n-1.
  R13. When TAKE g n would need more than market_g cards, more than the player's camels plus 1, or would leave more than 7 goods in hand, it is a pass and nothing changes.
  R14. When a player chooses CAMELS and market_camel >= 1, their camels rise by market_camel and market_camel becomes 0; when market_camel is 0, it is a pass.
  R15. When a player sells n Diamond or n Silver with n < 2, or sells more of a good than they hold, it is a pass and nothing changes.
  R16. When a player sells n >= 1 Cloth that they hold, the sale is legal.
  R17. When a player sells n of good g, they score n times the current price_g, and their hand count g drops by n.
  R18. When a sale has n == 3, the seller scores +3 extra; when n == 4, +5 extra; when n >= 5, +8 extra; when n <= 2, no extra.
  R19. After a sale of n of good g, price_g becomes max(1, price_g - n). For example, selling 2 Diamond at price 7 scores 14 and sets the price to 5.
  R20. An illegal or missing choice is a pass: no attribute changes.
  R21. After each turn the action type, good and n are announced publicly.
  R22. After round 16, the player with strictly more camels scores +5; when camels are tied, neither player scores the bonus.
  R23. Cards left in hand at the end score nothing.
  R24. The game ends after round 16; the higher score wins, and equal scores are a draw (both share the win).

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - First player's turn and second player's turn | asked: the seat acting | options: Each TAKE <good> <n> with n >= 1, market count of that good >= n, the player's camels >= n-1 and hand + n <= 7; CAMELS if market_camel >= 1; each SELL Diamond <n> or SELL Silver <n> with 2 <= n <= cards held; each SELL Cloth <n> with 1 <= n <= cloth held. If no action is legal, only PASS is offered.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round == 16
  - each player's standing: you.score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their final score after the camel-majority bonus. The higher score wins, and equal scores share the win (a draw).
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

- each player: `camels` (number, visible: public, starts 1): Camels in this player's public herd
- each player: `score` (number, visible: public, starts 0): Points scored from sales and the camel bonus
- the table: `round` (number, visible: public, starts 0): Current round, 1 to 16
- the table: `first_seat` (number, visible: public, starts 1): Seat that acts first this round: seat 1 (A) in rounds 1,4,5,8,9,12,13,16 and seat 2 (B) otherwise
- the table: `market_diamond` (number, visible: public, starts 0): Diamond cards in the market
- the table: `market_silver` (number, visible: public, starts 1): Silver cards in the market
- the table: `market_cloth` (number, visible: public, starts 1): Cloth cards in the market
- the table: `market_camel` (number, visible: public, starts 2): Camel cards in the market
- the table: `price_diamond` (number, visible: public, starts 7): Current Diamond price
- the table: `price_silver` (number, visible: public, starts 5): Current Silver price
- the table: `price_cloth` (number, visible: public, starts 3): Current Cloth price
- parameters (each must be an attribute holding this value, never a number buried in a step): rounds = 16, price_diamond_start = 7, price_silver_start = 5, price_cloth_start = 3, deck_diamond = 5, deck_silver = 7, deck_cloth = 8, deck_size = 20, market_camel_start = 2, market_silver_start = 1, market_cloth_start = 1, market_diamond_start = 0, start_hand_silver = 1, start_hand_cloth = 1, start_camels = 1, start_score = 0, hand_limit = 7, restock_per_round = 1, draws_per_round = 1, take_min = 1, sell_min_diamond = 2, sell_min_silver = 2, sell_min_cloth = 1, bonus_sell_3 = 3, bonus_sell_4 = 5, bonus_sell_5_plus = 8, price_floor = 1, camel_majority_bonus = 5
- the game ends with ONE ending whose `rank_by` is `you.score`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
