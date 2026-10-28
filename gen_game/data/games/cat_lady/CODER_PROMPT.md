# Task: write the XColos game file for "Cat Lady: Secret Favourites (Balanced)"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 4; set `meta.players` to {"min": 3, "max": 4, "suggested": 4} (the suggested size is the one the game plays best at).

SETUP.
The deck has 96 cards:
- 18 Food-1 (1 food each)
- 10 Food-2 (2 food each)
- 20 Cat
- 8 Stray Cat
- 24 Toy (8 Red, 8 Blue, 8 Green)
- 16 Catnip
Shuffle the deck once.
Each player is secretly dealt one Favourite, and every player gets a different one. With 3 players the Favourites are drawn from {Cats, Toys, Catnip}; with 4 players they are drawn from {Cats, Toys, Catnip, Strays}. Only the owner knows their Favourite.
Seat the players in a fixed order, seat 1 to seat N.

ROUNDS.
With 3 players there are 12 rounds; with 4 players there are 8.
In round r, the first picker is seat ((r-1) mod N) + 1, and the others follow in seat order. Over the game, every seat holds each picking position equally often: 4 times each with 3 players, 2 times each with 4 players.

EACH ROUND.
1. Deal the market from the top of the deck. With 3 players deal 4 lots (Lot A to Lot D) of 2 cards each; with 4 players deal 5 lots (Lot A to Lot E) of 2 cards each. Announce every lot's contents to all players.
2. Starting with the first picker, each player in turn chooses one remaining lot by its letter. Each player sees all earlier picks.
3. A chosen lot goes to that player at once. Food cards add their food value to the player's food total. Cats, Strays, Toys (by colour) and Catnip are added to the player's counts. Everything a player owns is public, except their Favourite.
4. When every player has picked, the one leftover lot is discarded.
5. After the last round, go to final scoring. With 4 players, the 16 cards still in the deck are never used.

FINAL SCORING. For each player:
- Feeding: each Cat needs 2 food. Fed cats = the smaller of (Cats) and (food ÷ 2, rounded down). Each fed cat scores 5 and each unfed Cat scores -1. Leftover food = food total - 2 × fed cats.
- Strays: each Stray Cat scores 3.
- Toys: each Toy scores 1, plus 4 for each complete set of one Red, one Blue and one Green. Number of sets = the smallest of the three colour counts.
- Catnip: with n Catnip cards, counting at most 6, the player scores n(n+1)/2 (maximum 21). Catnip beyond 6 scores nothing here.
- Food penalty: the player or players with the most leftover food lose 2 points, provided that amount is at least 1.
- Favourite bonus, revealed now:
  - Cats: +2 per fed cat, maximum +10.
  - Toys: +1 per Toy card.
  - Catnip: +2 per Catnip card owned (including any beyond 6), maximum +12.
  - Strays (4 players only): +3 per Stray Cat.

How the winner is decided: The highest final total wins. If players are tied, the tied player with the most fed cats wins. If they are still tied, those players draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Cat Lady: Secret Favourites (Balanced) (3 to 4 players, best with 4)

A card-drafting game for 3 to 4 players: each round players take turns picking a 2-card lot from a public market, collecting food, cats, strays, toys and catnip, and score at the end with a secret Favourite bonus.

STATE (every item below must exist in the file):
  - each player: favourite (text, starts ''); only its owner sees it. The player's secret Favourite: cats, toys, catnip or strays
  - each player: favourite_revealed (text, starts ''); everyone sees it. The Favourite, copied here at final scoring when it is revealed
  - each player: cards (list, starts []); everyone sees it. Every card the player has taken (codes: food1, food2, cat, stray, toy_red, toy_blue, toy_green, catnip)
  - each player: food (number, starts 0); everyone sees it. Total food value: food1 counts 1 and food2 counts 2
  - each player: cats (number, starts 0); everyone sees it. Number of Cat cards
  - each player: strays (number, starts 0); everyone sees it. Number of Stray Cat cards
  - each player: toys_red (number, starts 0); everyone sees it. Number of Red Toy cards
  - each player: toys_blue (number, starts 0); everyone sees it. Number of Blue Toy cards
  - each player: toys_green (number, starts 0); everyone sees it. Number of Green Toy cards
  - each player: catnip (number, starts 0); everyone sees it. Number of Catnip cards
  - each player: fed_cats (number, starts 0); everyone sees it. Fed cats, worked out at final scoring as min(cats, floor(food/2)); also the tie-break
  - each player: leftover_food (number, starts 0); everyone sees it. food - 2 * fed_cats, worked out at final scoring
  - each player: score (number, starts 0); everyone sees it. Final total, worked out at final scoring
  - the table: deck (list, starts '96 codes: 18 food1, 10 food2, 20 cat, 8 stray, 8 toy_red, 8 toy_blue, 8 toy_green, 16 catnip'); hidden from all players. The shuffled draw deck
  - the table: favourites_pool (list, starts '[cats, toys, catnip] with 3 players; [cats, toys, catnip, strays] with 4 players'); hidden from all players. The Favourites still to be dealt
  - the table: num_rounds (number, starts '12 if N = 3, 8 if N = 4'); everyone sees it. Total rounds
  - the table: num_lots (number, starts 'N + 1'); everyone sees it. Lots dealt each round: 4 with 3 players, 5 with 4 players
  - the table: round (number, starts 0); everyone sees it. Current round number
  - the table: first_picker (number, starts 1); everyone sees it. Seat that picks first this round: ((round-1) mod N) + 1
  - the table: lot_a (list, starts []); everyone sees it. Cards in Lot A
  - the table: lot_b (list, starts []); everyone sees it. Cards in Lot B
  - the table: lot_c (list, starts []); everyone sees it. Cards in Lot C
  - the table: lot_d (list, starts []); everyone sees it. Cards in Lot D
  - the table: lot_e (list, starts []); everyone sees it. Cards in Lot E (used only with 4 players)
  - the table: lots_open (list, starts []); everyone sees it. Letters of the lots not yet picked this round
  - the table: discard (list, starts []); everyone sees it. Cards from leftover lots
  - the table: max_leftover (number, starts 0); everyone sees it. Largest leftover_food among all players, worked out at final scoring
  - parameters, each kept as a table attribute: deck_size = 96, food1_cards = 18, food1_value = 1, food2_cards = 10, food2_value = 2, cat_cards = 20, stray_cards = 8, toy_cards_per_colour = 8, toy_cards_total = 24, catnip_cards = 16, cards_per_lot = 2, lots_with_3_players = 4, lots_with_4_players = 5, rounds_with_3_players = 12, rounds_with_4_players = 8, picks_per_position_3_players = 4, picks_per_position_4_players = 2, unused_deck_cards_4_players = 16, food_per_cat = 2, fed_cat_points = 5, unfed_cat_points = -1, stray_points = 3, toy_points = 1, toy_set_points = 4, catnip_count_cap = 6, catnip_max_points = 21, food_penalty = 2, food_penalty_min_leftover = 1, fav_cats_per_fed_cat = 2, fav_cats_max = 10, fav_toys_per_toy = 1, fav_catnip_per_card = 2, fav_catnip_max = 12, fav_strays_per_stray = 3, rank_score_multiplier = 100

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Build the deck of 96 cards: 18 food1, 10 food2, 20 cat, 8 stray, 8 toy_red, 8 toy_blue, 8 toy_green and 16 catnip, and shuffle it once (all later draws are random picks from deck).
  2. Set favourites_pool to [cats, toys, catnip] with 3 players, or to [cats, toys, catnip, strays] with 4 players.
  3. Each player draws one Favourite at random from favourites_pool into their favourite (ally), and it is removed from the pool, so every Favourite is different. Each player is privately told their Favourite.
  4. Set num_rounds to 12 with 3 players or 8 with 4 players, and set num_lots to N + 1.
  5. Seats are fixed from seat 1 to seat N, and each player is sent their own state.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round += 1; first_picker = ((round - 1) mod N) + 1; lots_open = [A, B, C, D] with 3 players or [A, B, C, D, E] with 4 players.
  2. [update] all players. What happens: For each letter in lots_open, draw 2 cards at random from deck into lot_<letter> (append to the lot, remove from deck).
  3. [tell] all players. What happens: Announce round, first_picker and the contents of every lot in lots_open.
  4. [ask] each player in turn, starting with seat first_picker and continuing in seat order (wrapping from seat N to seat 1) answers: one letter from lots_open. What happens: The chosen lot's cards are appended to the player's cards. For each card: food1 adds 1 to food, food2 adds 2 to food, cat adds 1 to cats, stray adds 1 to strays, toy_red/toy_blue/toy_green add 1 to toys_red/toys_blue/toys_green, catnip adds 1 to catnip. The lot list is emptied and its letter is removed from lots_open. The pick is announced to all.
  5. [update] all players. What happens: The cards of the one lot left in lots_open are appended to discard, that lot is emptied, and lots_open is emptied.
  6. [update] all players. What happens: When round == num_rounds, for each player: fed_cats = min(cats, floor(food / 2)); leftover_food = food - 2 * fed_cats; score = 5 * fed_cats - 1 * (cats - fed_cats) + 3 * strays + 1 * (toys_red + toys_blue + toys_green) + 4 * min(toys_red, toys_blue, toys_green) + m * (m + 1) / 2 where m = min(catnip, 6).
  7. [update] all players. What happens: When round == num_rounds: max_leftover = the largest leftover_food over all players.
  8. [update] all players. What happens: When round == num_rounds, for each player: if leftover_food == max_leftover and max_leftover >= 1, score -= 2. Favourite bonus: if favourite == cats, score += min(2 * fed_cats, 10); if toys, score += toys_red + toys_blue + toys_green; if catnip, score += min(2 * catnip, 12); if strays, score += 3 * strays. favourite_revealed = favourite.
  9. [tell] all players. What happens: When round == num_rounds, announce every player's favourite_revealed, fed_cats and score.
  10. [check] all players. What happens: End the game if round >= num_rounds; otherwise continue to the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. At setup the deck holds 96 cards: 18 food1, 10 food2, 20 cat, 8 stray, 8 toy_red, 8 toy_blue, 8 toy_green and 16 catnip.
  R2. When there are 3 players, Favourites are dealt from {cats, toys, catnip}; when there are 4 players, from {cats, toys, catnip, strays}; no two players get the same Favourite.
  R3. A player's favourite is visible only to that player until final scoring, when it is copied to the public favourite_revealed.
  R4. When there are 3 players the game lasts 12 rounds; when there are 4 players it lasts 8 rounds.
  R5. In round r the first picker is seat ((r-1) mod N) + 1, and picking continues in seat order, wrapping around.
  R6. Each round, when there are 3 players, 4 lots (A to D) of 2 cards each are dealt from the deck; when there are 4 players, 5 lots (A to E) of 2 cards each are dealt.
  R7. Every lot's contents are announced to all players before any pick.
  R8. On their turn, a player must choose exactly one lot that no one has picked yet this round.
  R9. When a player takes a lot, each food1 adds 1 food, each food2 adds 2 food, and each cat, stray, toy of a colour or catnip adds 1 to the matching count.
  R10. After every player has picked, the one remaining lot is moved to the discard pile.
  R11. When there are 4 players, 16 cards remain in the deck at the end and are never used; when there are 3 players the deck is exactly used up.
  R12. At final scoring, fed_cats = min(cats, floor(food / 2)); for example 5 cats and 7 food give 3 fed cats.
  R13. Each fed cat scores 5 and each unfed cat scores -1; for example 5 cats with 3 fed score 15 - 2 = 13.
  R14. leftover_food = food - 2 * fed_cats.
  R15. Each stray scores 3.
  R16. Each toy scores 1, plus 4 for each set of one red, one blue and one green; for example 3 red, 2 blue and 1 green score 6 + 4 = 10.
  R17. With n catnip, a player scores m(m+1)/2 where m = min(n, 6); for example 4 catnip score 10, and 8 catnip score 21.
  R18. When a player's leftover_food equals the largest leftover_food at the table and that value is at least 1, the player loses 2 points; all players tied for the largest lose 2.
  R19. When the largest leftover_food at the table is 0, no player loses points for food.
  R20. When a player's Favourite is cats, they gain 2 per fed cat, at most 10.
  R21. When a player's Favourite is toys, they gain 1 per toy card.
  R22. When a player's Favourite is catnip, they gain 2 per catnip card, counting cards beyond 6, at most 12.
  R23. When a player's Favourite is strays (4 players only), they gain 3 per stray.
  R24. The game ends after round num_rounds; the highest score wins, ties go to the most fed cats, and players still tied draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Choose a lot this round | asked: each player in turn, starting with first_picker | options: The letters still in lots_open: with 3 players the first picker sees 4 letters (A to D), then 3, then 2; with 4 players the first picker sees 5 letters (A to E), then 4, 3 and 2. A lot already taken is never offered.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round >= num_rounds
  - each player's standing: you.score * 100 + you.fed_cats (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: The highest final score wins. Among players tied on score, the one with the most fed cats wins. Players still tied on both share the win, which is a draw.
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

- each player: `favourite_revealed` (text, visible: public, starts ''): The Favourite, copied here at final scoring when it is revealed
- each player: `fed_cats` (number, visible: public, starts 0): Fed cats, worked out at final scoring as min(cats, floor(food/2)); also the tie-break
- each player: `score` (number, visible: public, starts 0): Final total, worked out at final scoring
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 96, food1_cards = 18, food1_value = 1, food2_cards = 10, food2_value = 2, cat_cards = 20, stray_cards = 8, toy_cards_per_colour = 8, toy_cards_total = 24, catnip_cards = 16, cards_per_lot = 2, lots_with_3_players = 4, lots_with_4_players = 5, rounds_with_3_players = 12, rounds_with_4_players = 8, picks_per_position_3_players = 4, picks_per_position_4_players = 2, unused_deck_cards_4_players = 16, food_per_cat = 2, fed_cat_points = 5, unfed_cat_points = -1, stray_points = 3, toy_points = 1, toy_set_points = 4, catnip_count_cap = 6, catnip_max_points = 21, food_penalty = 2, food_penalty_min_leftover = 1, fav_cats_per_fed_cat = 2, fav_cats_max = 10, fav_toys_per_toy = 1, fav_catnip_per_card = 2, fav_catnip_max = 12, fav_strays_per_stray = 3, rank_score_multiplier = 100
- the game ends with ONE ending whose `rank_by` is `you.score * 100 + you.fed_cats`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
