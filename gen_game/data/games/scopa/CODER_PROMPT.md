# Task: write the XColos game file for "Scopa Duel"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 2; set `meta.players` to {"min": 2, "max": 2, "suggested": 2} (the suggested size is the one the game plays best at).

DECK: 40 cards in four suits: Coins, Cups, Swords, Clubs. Each suit has ranks 1 to 10: Ace=1, 2 to 7 at face value, Jack=8, Knight=9, King=10.

STRUCTURE: The match is 2 hands of 18 rounds each, 36 rounds in total. In each round both players play one card: first the Leader, then the Dealer. In hand 1 (rounds 1 to 18), Player A is Leader and Player B is Dealer. In hand 2 (rounds 19 to 36), the roles swap.

DEALING: At the start of round 1 and round 19, the full 40-card deck is shuffled (the only random event that round). Four cards are dealt face up to the table, and three cards are dealt privately to each player. At the start of rounds 4, 7, 10, 13 and 16 (hand 1) and rounds 22, 25, 28, 31 and 34 (hand 2), both hands are empty and three more cards are dealt to each player from the deck. Each hand uses exactly 4 + 6x3 = 40 cards.

INFORMATION: The table, all played cards and all captures are public. Each player sees only their own hand. The deck order is hidden.

A PLAY: On your turn, choose one card from your hand and declare which table cards you capture: a list, possibly empty. The declaration is legal if:
(a) some table card has the same rank as your card, and you declare exactly one such card; or
(b) no table card has the same rank, and you declare either nothing or a set of table cards whose ranks add up exactly to your card's rank.

If legal, you take your card and the declared cards into your capture pile. If you declared nothing, your card goes face up onto the table. If the declaration is illegal, your card goes face up onto the table and you capture nothing.

SCOPA: If your legal capture leaves the table empty, you score 1 Scopa point. The exception is the final play of a hand (the Dealer's play in round 18 or round 36), which never scores a Scopa.

LAST CAPTURE: The engine records who made the most recent capture. After the Dealer's play in round 18 (and in round 36), every card left on the table goes to that player's capture pile. If nobody captured in that hand, the leftover cards are discarded.

HAND SCORING (after rounds 18 and 36), using only that hand's capture piles:
- 1 point to the player with more captured cards (none if 20-20).
- 1 point to the player with more Coins (none if 5-5).
- 1 point to the holder of the Seven of Coins.
- 1 point to the player with more sevens. If tied, the player with more sixes gets it. If still tied, no point.
- Plus each player's Scopa points.

Capture piles are then cleared for hand 2, but each player's running totals of points, captured cards and captured Coins are kept.

How the winner is decided: After round 36, the player with more total points across both hands wins. If tied, the player who captured more cards in total across both hands wins. If still tied, the player who captured more Coins in total wins. If still tied, the match is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Scopa Duel (2 to 2 players, best with 2)

Two-player Scopa over 2 hands of 18 rounds. Players capture table cards by matching rank or summing to it, score Scopas for sweeping the table, then score cards, Coins, the Seven of Coins and sevens.

STATE (every item below must exist in the file):
  - each player: hand (list, starts []); only its owner sees it. Cards held privately, as codes such as '7Co' (rank 1-10 plus suit Co=Coins, Cu=Cups, Sw=Swords, Cl=Clubs).
  - each player: captures (list, starts []); everyone sees it. This hand's capture pile. Captures are public.
  - each player: scopa_points (number, starts 0); everyone sees it. Scopas scored in the current hand.
  - each player: played_card (text, starts ''); everyone sees it. Card chosen this turn.
  - each player: declared (list, starts []); everyone sees it. Table cards declared as captured this turn; may be empty.
  - each player: score (number, starts 0); everyone sees it. Total points across both hands.
  - each player: total_cards (number, starts 0); everyone sees it. Running total of cards captured across both hands.
  - each player: total_coins (number, starts 0); everyone sees it. Running total of Coins captured across both hands.
  - the table: deck (list, starts []); hidden from all players. Undealt cards. The order is hidden.
  - the table: table_cards (list, starts []); everyone sees it. Face-up cards on the table.
  - the table: round (number, starts 1); everyone sees it. Current round, 1 to 36.
  - the table: last_capturer (number, starts 0); everyone sees it. Seat of the most recent capture in this hand; 0 if none.
  - the table: full_deck (list, starts ['1Co', '2Co', '3Co', '4Co', '5Co', '6Co', '7Co', '8Co', '9Co', '10Co', '1Cu', '2Cu', '3Cu', '4Cu', '5Cu', '6Cu', '7Cu', '8Cu', '9Cu', '10Cu', '1Sw', '2Sw', '3Sw', '4Sw', '5Sw', '6Sw', '7Sw', '8Sw', '9Sw', '10Sw', '1Cl', '2Cl', '3Cl', '4Cl', '5Cl', '6Cl', '7Cl', '8Cl', '9Cl', '10Cl']); hidden from all players. The 40 card codes, used to refill the deck at the start of each hand.
  - parameters, each kept as a table attribute: deck_size = 40, suits = 4, ranks_per_suit = 10, ace_rank = 1, jack_rank = 8, knight_rank = 9, king_rank = 10, hands = 2, rounds_per_hand = 18, total_rounds = 36, table_deal = 4, cards_per_deal = 3, deals_per_hand = 6, shuffle_round_hand1 = 1, shuffle_round_hand2 = 19, redeal_interval = 3, first_redeal_round_hand1 = 4, last_redeal_round_hand1 = 16, first_redeal_round_hand2 = 22, last_redeal_round_hand2 = 34, final_play_round_hand1 = 18, final_play_round_hand2 = 36, scopa_points = 1, most_cards_points = 1, cards_tie_count = 20, most_coins_points = 1, coins_tie_count = 5, seven_of_coins_points = 1, most_sevens_points = 1, primary_rank = 7, secondary_rank = 6, no_capturer = 0, score_weight = 10000, cards_weight = 100, coins_weight = 1

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seat 1 is Player A and seat 2 is Player B.
  2. Every player's score, total_cards and total_coins are set to 0, and round is set to 1.
  3. Dealing happens inside the round steps at rounds 1 and 19.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: When round is 1 or 19: deck = full_deck; table_cards, every hand, every captures and every declared are emptied; scopa_points = 0 for each player; last_capturer = 0. Then 4 cards are drawn at random from deck into table_cards, and 3 cards are drawn at random from deck into each player's hand (each draw is removed from deck and appended to its destination).
  2. [update] all players. What happens: When round is in {4,7,10,13,16,22,25,28,31,34}: 3 cards are drawn at random from deck into each player's hand.
  3. [sync] all players. What happens: Each player sees their own hand plus the public table_cards, captures, scopa_points, score, total_cards, total_coins and round.
  4. [ask] the Leader: seat 1 when round <= 18, seat 2 when round >= 19 answers: one card from the Leader's own hand. What happens: Leader.played_card = the chosen card; it is removed from Leader.hand.
  5. [ask] the Leader answers: short text listing the table card codes captured, separated by spaces, or 'none'. What happens: Leader.declared = the listed table cards (empty if 'none').
  6. [update] the Leader. What happens: If legal and declared is non-empty: the played_card and the declared cards are appended to Leader.captures, the declared cards are removed from table_cards, and last_capturer = Leader's seat; then, if table_cards is empty, Leader.scopa_points += 1. Otherwise (declared is empty, or the declaration is illegal): played_card is appended to table_cards and nothing is captured. The table is told what was played and captured. JUDGED: a referee rules true or false on "The declaration is legal: if some table card has the same rank as the played card, the declaration names exactly one such table card; otherwise it names either no cards or a set of distinct cards currently on the table whose ranks add up exactly to the played card's rank."; write this step's `when` as {"prose": that sentence, verbatim}.
  7. [ask] the Dealer: seat 2 when round <= 18, seat 1 when round >= 19 answers: one card from the Dealer's own hand. What happens: Dealer.played_card = the chosen card; it is removed from Dealer.hand.
  8. [ask] the Dealer answers: short text listing the table card codes captured, separated by spaces, or 'none'. What happens: Dealer.declared = the listed table cards (empty if 'none').
  9. [update] the Dealer. What happens: If legal and declared is non-empty: the played_card and the declared cards are appended to Dealer.captures, the declared cards are removed from table_cards, and last_capturer = Dealer's seat; then, if table_cards is empty and round is not 18 or 36, Dealer.scopa_points += 1. Otherwise: played_card is appended to table_cards and nothing is captured. The table is told what was played and captured. JUDGED: a referee rules true or false on "The declaration is legal: if some table card has the same rank as the played card, the declaration names exactly one such table card; otherwise it names either no cards or a set of distinct cards currently on the table whose ranks add up exactly to the played card's rank."; write this step's `when` as {"prose": that sentence, verbatim}.
  10. [update] all players. What happens: When round is 18 or 36: if last_capturer > 0, all table_cards are appended to that seat's captures; otherwise they are discarded. table_cards is emptied. Hand scoring, using this hand's captures: +1 score to the player with strictly more cards; +1 to the player with strictly more cards whose suit is Co; +1 to the holder of '7Co'; +1 to the player with more rank-7 cards, or, if those are tied, more rank-6 cards, and no point if both are tied; each player's score += scopa_points. Each player's total_cards += count(captures) and total_coins += count of Co cards in captures. The hand's results are announced.
  11. [update] all players. What happens: round += 1.
  12. [check] all players. What happens: End the game if round > 36; otherwise continue to the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When round is 1 or 19, then the deck is refilled to all 40 cards, 4 random cards go to table_cards, and each player's hand receives 3 random cards from the deck.
  R2. When round is 4, 7, 10, 13, 16, 22, 25, 28, 31 or 34, then each player receives 3 cards from the deck into their hand.
  R3. When round <= 18, then seat 1 plays first (Leader) and seat 2 plays second (Dealer); when round >= 19, then seat 2 leads and seat 1 deals.
  R4. When a player plays a card and a table card has the same rank, then the declaration is legal only if it names exactly one such card, and that card plus the played card go to the player's captures.
  R5. When no table card has the same rank and the declared table cards' ranks sum exactly to the played card's rank, then those cards plus the played card go to the player's captures.
  R6. When a player declares nothing, then the played card is added to table_cards.
  R7. When a declaration is illegal (for example, a sum is declared while a same-rank card is on the table, or the ranks do not add up), then the played card is added to table_cards and nothing is captured.
  R8. When a legal non-empty capture leaves table_cards empty, then the capturer's scopa_points increase by 1, unless it is the Dealer's play in round 18 or 36.
  R9. When a player makes a legal non-empty capture, then last_capturer is set to that player's seat.
  R10. When round 18 or 36 ends, then the remaining table_cards go to last_capturer's captures, or are discarded if last_capturer is 0.
  R11. When a hand is scored, then the player with more captured cards gets 1 point, and nobody gets it at 20-20.
  R12. When a hand is scored, then the player with more captured Coins gets 1 point, and nobody gets it at 5-5.
  R13. When a hand is scored, then the player whose captures contain 7Co gets 1 point.
  R14. When a hand is scored, then the player with more sevens gets 1 point; if sevens are tied, the player with more sixes gets it; if both are tied, nobody does.
  R15. When a hand is scored, then each player's scopa_points are added to their score, and their captured card count and Coins count are added to total_cards and total_coins.
  R16. When hand 2 begins at round 19, then captures, scopa_points and last_capturer are reset, while score, total_cards and total_coins are kept.
  R17. When round 36 is complete, then the game ends and the higher score wins, tie-broken by total_cards and then total_coins; if all three are equal, it is a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Choose a card to play | asked: the Leader, then the Dealer | options: Every card currently in that seat's own hand, and nothing else.
  - Declare the table cards you capture | asked: the Leader, then the Dealer | options: Free text: a space-separated list of card codes currently in table_cards, or 'none'. Any declaration may be sent; an illegal one sends the played card to the table and captures nothing.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round > 36
  - each player's standing: you.score * 10000 + you.total_cards * 100 + you.total_coins (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Most total points across both hands wins. A tie goes to more total captured cards, then to more total captured Coins. If still tied, both players share the result (a draw).
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

- each player: `score` (number, visible: public, starts 0): Total points across both hands.
- each player: `total_cards` (number, visible: public, starts 0): Running total of cards captured across both hands.
- each player: `total_coins` (number, visible: public, starts 0): Running total of Coins captured across both hands.
- the table: `table_cards` (list, visible: public, starts []): Face-up cards on the table.
- the table: `round` (number, visible: public, starts 1): Current round, 1 to 36.
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 40, suits = 4, ranks_per_suit = 10, ace_rank = 1, jack_rank = 8, knight_rank = 9, king_rank = 10, hands = 2, rounds_per_hand = 18, total_rounds = 36, table_deal = 4, cards_per_deal = 3, deals_per_hand = 6, shuffle_round_hand1 = 1, shuffle_round_hand2 = 19, redeal_interval = 3, first_redeal_round_hand1 = 4, last_redeal_round_hand1 = 16, first_redeal_round_hand2 = 22, last_redeal_round_hand2 = 34, final_play_round_hand1 = 18, final_play_round_hand2 = 36, scopa_points = 1, most_cards_points = 1, cards_tie_count = 20, most_coins_points = 1, coins_tie_count = 5, seven_of_coins_points = 1, most_sevens_points = 1, primary_rank = 7, secondary_rank = 6, no_capturer = 0, score_weight = 10000, cards_weight = 100, coins_weight = 1
- the game ends with ONE ending whose `rank_by` is `you.score * 10000 + you.total_cards * 100 + you.total_coins`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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

1) Play order: rounds 1 to 18 must ask seat 1 first, then seat 2. Rounds 19 to 36 must ask seat 2 first, then seat 1. Use two pairs of steps with `when` conditions on round <= final_play_round_hand1 and round >= shuffle_round_hand2. Use parameter attributes, not literal numbers.
2) Declaration: let the player pick the declared cards from the current table_cards list, with an explicit 'none' option. Store the actual card names, not a free-text acknowledgement like 'Noted.'.
3) Resolve the play with arithmetic conditions:
- If some table card has the played card's rank, the play is legal only when exactly one such card is declared. Remove that card from table_cards and add it, plus the played card, to the player's captures.
- If no table card has that rank and the declared cards' ranks sum exactly to the played rank, remove them from the table and capture them with the played card.
- If the player declared 'none', or the declaration is illegal, append the played card to table_cards and capture nothing. The captures list must stay unchanged.
4) After any legal capture, set last_capturer to that seat. Award scopa_points if table_cards is now empty, except on the Dealer's play in round final_play_round_hand1 or final_play_round_hand2.
5) Make sure the 'none' option exists as a choice the game actually offers, so that branch can be matched.
