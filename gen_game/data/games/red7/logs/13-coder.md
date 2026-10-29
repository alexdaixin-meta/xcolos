# 13 coder

- time: 2026-10-27T17:46:32+00:00 (173.5s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 86ba319d1145f2ee, reply sha256 3f7824d333a3789b

## Sent

````
# Task: write the XColos game file for "Red3 Duel"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 3; set `meta.players` to {"min": 2, "max": 3, "suggested": 2} (the suggested size is the one the game plays best at).

CARDS. There are 21 cards: numbers 1 to 7 in each of three colours, Red, Green and Violet. Colour rank is Red 3, Green 2, Violet 1. A card's strength is number x 10 + colour rank (7 Red = 73, 4 Violet = 41). Higher strength beats lower. A card is EVEN if its number is 2, 4 or 6. A card is LOW if its number is 1, 2 or 3.

THE RULE. The Canvas shows one colour, which is the current rule. Each living player has a KEY under the current rule:
- Red: key = strength of the highest card in your palette.
- Green: key = 100 x (number of even cards in your palette) + strength of your highest even card, or 0 if you have no even card.
- Violet: key = 100 x (number of low cards in your palette) + strength of your highest low card, or 0 if you have no low card.
You are LEADING if your key is strictly higher than every other living player's key. If keys tie, including at 0, no tied player is leading.

SETUP OF A HAND. Shuffle all 21 cards. Deal each player 5 cards as a hidden hand, then 1 card face up as their palette. The remaining cards (9 with 2 players, 3 with 3 players) are set aside unseen for this hand. The Canvas starts as Red. Everyone is alive. The initial leader is the player whose palette card has the highest strength. The first turn of the hand goes to the next player in seat order after that leader.

A TURN. On your turn choose exactly one:
(a) play one card from your hand face up to your palette;
(b) discard one card from your hand to the Canvas, so the rule becomes that card's colour and the card leaves play;
(c) do (a), then (b), with two different cards;
(d) fold.
Then recompute keys under the current rule. If you are not leading, or you folded, or you named a card you do not hold, you are eliminated. Your palette stays visible but no longer counts. If you have no cards left in hand when your turn comes, you can only fold. Play passes to the next living player in seat order.

A ROUND is one pass of turns through all living players in seat order, starting with the player whose turn it is.

END OF A HAND. A hand ends the moment only one player is alive. That player is the hand winner.
- With 2 players: the hand winner scores 1 point; the other scores 0.
- With 3 players: the hand winner scores 2 points; the player whose elimination left one survivor scores 1; the first player eliminated scores 0.
The engine records the hand winner as the MOST RECENT HAND WINNER. If the match is not over, a new hand is set up at the start of the next round.

END OF THE MATCH.
- With 2 players, the match ends when a player reaches 3 points.
- With 3 players, the match ends after any hand in which a player reaches 6 or more points.
- In either case, it also ends when round 40 is complete; an unfinished hand then scores nothing.

INFORMATION. Palettes, the Canvas, eliminations, points and the most recent hand winner are public. Hands and set-aside cards are hidden. There is no table talk.

How the winner is decided: The player with the most points when the match ends wins. With 2 players this is the first to 3 points, and a tie cannot occur at that end. If two or more players share the most points, which can happen in 3 players or at the round-40 cap, the tied player who won the most recently completed hand wins. If no hand was completed at all, the match is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Red3 Duel (2 to 3 players, best with 2)

A Red7-style shedding duel: on your turn play a card to your palette and/or change the Canvas rule so that you lead under it, or you are out; the last player alive wins the hand, and points across hands win the match.

STATE (every item below must exist in the file):
  - each player: hand (list, starts []); only its owner sees it. Cards in the player's hidden hand. Each card is stored as its strength (number*10 + colour rank, e.g. 73 = 7 Red).
  - each player: palette (list, starts []); everyone sees it. Face-up cards in the player's palette, stored as strengths.
  - each player: alive (bool, starts True); everyone sees it. Whether the player is still in the current hand.
  - each player: key_value (number, starts 0); everyone sees it. The player's KEY under the current Canvas rule, recomputed after every turn.
  - each player: elim_order (number, starts 0); everyone sees it. 0 while alive this hand. Otherwise, the order in which the player was eliminated this hand (1 = first out).
  - each player: acted_this_round (bool, starts False); everyone sees it. Whether the player has taken their turn in the current round.
  - each player: points (number, starts 0); everyone sees it. Match points (the score).
  - each player: is_recent_winner (number, starts 0); everyone sees it. 1 if this player won the most recently completed hand, else 0.
  - the table: deck (list, starts [11, 12, 13, 21, 22, 23, 31, 32, 33, 41, 42, 43, 51, 52, 53, 61, 62, 63, 71, 72, 73]); hidden from all players. The undealt cards during dealing. It is rebuilt to all 21 cards at each new hand.
  - the table: set_aside (list, starts []); hidden from all players. Cards set aside unseen for the current hand (9 with 2 players, 3 with 3 players).
  - the table: canvas (number, starts 3); everyone sees it. Current rule colour: 3 = Red, 2 = Green, 1 = Violet.
  - the table: turn_seat (number, starts 0); everyone sees it. Seat whose turn it is.
  - the table: eliminated_count (number, starts 0); everyone sees it. How many players have been eliminated in the current hand.
  - the table: alive_count (number, starts 0); everyone sees it. Number of living players in the current hand.
  - the table: hand_over (bool, starts True); everyone sees it. True when no hand is in progress, so that a new hand is set up at the start of the next round.
  - the table: most_recent_winner (number, starts 0); everyone sees it. Seat of the most recent hand winner (0 = none yet).
  - the table: round_no (number, starts 0); everyone sees it. Number of completed rounds.
  - parameters, each kept as a table attribute: card_numbers_min = 1, card_numbers_max = 7, colours = 3, deck_size = 21, rank_red = 3, rank_green = 2, rank_violet = 1, strength_number_multiplier = 10, key_count_multiplier = 100, hand_size = 5, palette_start_size = 1, set_aside_2p = 9, set_aside_3p = 3, winner_points_2p = 1, loser_points_2p = 0, winner_points_3p = 2, second_points_3p = 1, first_out_points_3p = 0, target_points_2p = 3, target_points_3p = 6, round_cap = 40, even_number_1 = 2, even_number_2 = 4, even_number_3 = 6, low_number_max = 3

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Every player starts with 0 points and is_recent_winner 0. most_recent_winner is 0 and round_no is 0.
  2. hand_over is set to true, so the first round begins by setting up a hand.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: New hand: deck = all 21 strengths [11..73]. For every player: hand = [], palette = [], alive = true, elim_order = 0. Set eliminated_count = 0, alive_count = number of players, canvas = 3 (Red).
  2. [update] each player in turn. What happens: Deal: for each player, 5 times move a random card from deck to that player's hand, then move 1 random card from deck to that player's palette.
  3. [update] all players. What happens: Move all remaining deck cards to set_aside (9 with 2 players, 3 with 3 players). Compute key_value under Red (max of palette) for everyone. Set turn_seat = the next seat in seat order after the player with the highest palette strength. Set hand_over = false. Announce palettes and the Canvas.
  4. [update] all players. What happens: Start of round: acted_this_round = false for every player.
  5. [sync] all players. What happens: Each player sees their own hand plus all palettes, the canvas, alive flags, points and most_recent_winner.
  6. [repeat] each living player in turn, starting at turn_seat. What happens: Repeat the next four steps (turn, resolve, hand end, pass) until hand_over is true or every living player has acted_this_round = true.
  7. [ask] the player at turn_seat answers: one option: 'play X', 'discard X', 'play X then discard Y' (X != Y, both in hand), or 'fold'; only 'fold' if the hand is empty. What happens: Play X: move X from hand to palette. Discard X: remove X from hand (it leaves play) and set canvas = X mod 10. Play X then discard Y: do both, in that order. Fold: nothing moves. In every case set acted_this_round = true.
  8. [update] all players. What happens: Recompute key_value for every living player under canvas. Red (3): max strength in palette. Green (2): 100 * count of palette cards with floor(s/10) in {2,4,6} + max such strength, or 0 if none. Violet (1): 100 * count of palette cards with floor(s/10) <= 3 + max such strength, or 0 if none. If the acting player folded, or their key_value is not strictly greater than every other living player's key_value: alive = false, eliminated_count += 1, elim_order = eliminated_count, alive_count -= 1. Announce the action, the canvas and any elimination.
  9. [update] all players. What happens: Hand ends and the survivor is the hand winner. With 2 players: winner points += 1 (the other gets 0). With 3 players: winner points += 2, the player with elim_order 2 points += 1, the player with elim_order 1 points += 0. Set is_recent_winner = 1 for the winner and 0 for everyone else, most_recent_winner = winner's seat, hand_over = true. Announce the points.
  10. [update] all players. What happens: turn_seat = the next living seat in seat order after the seat that just acted.
  11. [update] all players. What happens: round_no += 1.
  12. [check] all players. What happens: End the match if (number of players == 2 and any player's points >= 3) or (number of players == 3 and hand_over and any player's points >= 6) or round_no >= 40. Otherwise continue to the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. The deck has 21 cards, numbers 1 to 7 in Red (rank 3), Green (rank 2) and Violet (rank 1), and each card's strength is number*10 + rank (7 Red = 73, 4 Violet = 41).
  R2. When a hand is set up, each player gets 5 hidden hand cards and 1 face-up palette card, and the rest (9 with 2 players, 3 with 3 players) go to set_aside unseen.
  R3. When a hand is set up, canvas is Red (3), every player is alive, and the first turn goes to the next seat after the player whose palette card has the highest strength.
  R4. When the canvas is Red, a player's key is the highest strength in their palette.
  R5. When the canvas is Green, a player's key is 100 * (number of palette cards numbered 2, 4 or 6) + the strength of the highest such card, or 0 if they have none.
  R6. When the canvas is Violet, a player's key is 100 * (number of palette cards numbered 1, 2 or 3) + the strength of the highest such card, or 0 if they have none.
  R7. A player is leading only if their key is strictly higher than every other living player's key; tied players, including ties at 0, are not leading.
  R8. When a player plays a card, it moves from their hand to their palette.
  R9. When a player discards a card, it leaves their hand and play entirely, and the canvas becomes that card's colour.
  R10. When a player plays then discards, the two cards must be different, and the play happens before the discard.
  R11. When, after their action, the acting player is not leading under the current canvas, they are eliminated (alive = false).
  R12. When a player folds, they are eliminated.
  R13. When a player has no cards in hand on their turn, their only option is to fold.
  R14. When a player is eliminated, their palette stays visible but their key no longer counts against others.
  R15. After a turn, play passes to the next living player in seat order.
  R16. A round is one pass of turns through all living players in seat order, starting with the player whose turn it is.
  R17. When only one player is alive, the hand ends immediately and that player is the hand winner and the most recent hand winner.
  R18. With 2 players, the hand winner scores 1 point and the other scores 0.
  R19. With 3 players, the hand winner scores 2 points, the second player eliminated scores 1, and the first player eliminated scores 0.
  R20. When a hand ends and the match is not over, a new hand is set up at the start of the next round.
  R21. With 2 players, the match ends when a player reaches 3 points.
  R22. With 3 players, the match ends after a hand in which a player reaches 6 or more points.
  R23. When round 40 is complete, the match ends and an unfinished hand scores nothing.
  R24. The player with the most points wins; a tie on points goes to the tied player who won the most recently completed hand; if no hand was completed, the match is a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Your turn: choose an action | asked: the player at turn_seat (living) | options: With an empty hand: fold only. With exactly 1 card X in hand: play X, discard X, fold. With 2 or more cards: play X for each X in hand; discard X for each X in hand; play X then discard Y for each ordered pair of different cards X, Y in hand; fold.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: (player_count == 2 and max(points) >= 3) or (player_count == 3 and hand_over and max(points) >= 6) or round_no >= 40
  - each player's standing: you.points * 10 + you.is_recent_winner (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - min_to_win: 1 (a player whose standing is below it cannot win; if none reaches it, the match ends with no winner)
  - how the result is decided: Most points wins. Among players tied on points, the one who won the most recently completed hand wins. If no hand was ever completed, nobody reaches the bar of 1 and the match is a draw with no winner.
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

- each player: `palette` (list, visible: public, starts []): Face-up cards in the player's palette, stored as strengths.
- each player: `alive` (bool, visible: public, starts True): Whether the player is still in the current hand.
- each player: `points` (number, visible: public, starts 0): Match points (the score).
- each player: `is_recent_winner` (number, visible: public, starts 0): 1 if this player won the most recently completed hand, else 0.
- the table: `canvas` (number, visible: public, starts 3): Current rule colour: 3 = Red, 2 = Green, 1 = Violet.
- the table: `most_recent_winner` (number, visible: public, starts 0): Seat of the most recent hand winner (0 = none yet).
- the table: `round_no` (number, visible: public, starts 0): Number of completed rounds.
- parameters (each must be an attribute holding this value, never a number buried in a step): card_numbers_min = 1, card_numbers_max = 7, colours = 3, deck_size = 21, rank_red = 3, rank_green = 2, rank_violet = 1, strength_number_multiplier = 10, key_count_multiplier = 100, hand_size = 5, palette_start_size = 1, set_aside_2p = 9, set_aside_3p = 3, winner_points_2p = 1, loser_points_2p = 0, winner_points_3p = 2, second_points_3p = 1, first_out_points_3p = 0, target_points_2p = 3, target_points_3p = 6, round_cap = 40, even_number_1 = 2, even_number_2 = 4, even_number_3 = 6, low_number_max = 3
- the game ends with ONE ending whose `rank_by` is `you.points * 10 + you.is_recent_winner`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
- that ending's `min_to_win` is `1`: a player below it cannot win, and if nobody reaches it the match ends with no winner
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

1) New-hand setup (R20): at the start of every hand, first reset all hand state. Clear every player's hand and palette, clear the table's set_aside and discarded lists, and rebuild the deck from all 21 card strengths (11..73). Then shuffle and deal hand_size cards to each hand and palette_start_size card to each palette. Move only the remainder to set_aside, which must be set_aside_2p = 9 or set_aside_3p = 3 cards depending on player count. Do not append to a set_aside left over from the previous hand. Also reset canvas to rank_red, set alive to true for everyone, reset the elimination order and keys, recompute the initial leader from the palette strengths, and give the first turn to the next seat after that leader. 2) Empty hand (R13): when a living player whose hand is empty gets the turn, still run the normal choice step for that seat, with an options list containing exactly 'fold', so the player is actually asked. Then apply the fold through the same path as a voluntary fold: eliminate the player, record the elimination order, and score the hand if one player is left. Do not resolve the fold internally without putting the option to the seat. Keep the option name exactly 'fold', the same name used when the hand is not empty.

````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "red3_duel",
    "name": "Red3 Duel",
    "players": {
      "min": 2,
      "max": 3,
      "suggested": 2
    },
    "blurb": "A Red7-style shedding duel: play to your palette or change the Canvas rule so you lead, or you are out; last alive wins the hand."
  },
  "statuses": [
    {
      "id": "playing",
      "acts": true,
      "initial": true
    },
    {
      "id": "out",
      "acts": false
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
        "key": "palette",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "alive",
        "visible": "public",
        "type": "bool",
        "initial": true
      },
      {
        "key": "key_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "elim_order",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "acted_this_round",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "is_recent_winner",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "sel_play",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "sel_discard",
        "visible": "ally",
        "type": "number",
        "initial": 0
      }
    ],
    "game": [
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": [11, 12, 13, 21, 22, 23, 31, 32, 33, 41, 42, 43, 51, 52, 53, 61, 62, 63, 71, 72, 73]
      },
      {
        "key": "all_cards",
        "visible": "none",
        "type": "list",
        "initial": [11, 12, 13, 21, 22, 23, 31, 32, 33, 41, 42, 43, 51, 52, 53, 61, 62, 63, 71, 72, 73]
      },
      {
        "key": "set_aside",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "canvas",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "turn_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "eliminated_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "alive_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hand_over",
        "visible": "public",
        "type": "bool",
        "initial": true
      },
      {
        "key": "most_recent_winner",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "round_no",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "last_action",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "deal_seat",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "leader_seat",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "play_card",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "discard_card",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "actor_out",
        "visible": "none",
        "type": "bool",
        "initial": false
      },
      {
        "key": "hand_winner",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "card_names",
        "visible": "none",
        "type": "list",
        "initial": [
          "", "", "", "", "", "", "", "", "", "", "",
          "1 Violet", "1 Green", "1 Red",
          "", "", "", "", "", "", "",
          "2 Violet", "2 Green", "2 Red",
          "", "", "", "", "", "", "",
          "3 Violet", "3 Green", "3 Red",
          "", "", "", "", "", "", "",
          "4 Violet", "4 Green", "4 Red",
          "", "", "", "", "", "", "",
          "5 Violet", "5 Green", "5 Red",
          "", "", "", "", "", "", "",
          "6 Violet", "6 Green", "6 Red",
          "", "", "", "", "", "", "",
          "7 Violet", "7 Green", "7 Red"
        ]
      },
      {
        "key": "pair_index",
        "visible": "none",
        "type": "list",
        "initial": [
          [0, 1], [0, 2], [0, 3], [0, 4],
          [1, 0], [1, 2], [1, 3], [1, 4],
          [2, 0], [2, 1], [2, 3], [2, 4],
          [3, 0], [3, 1], [3, 2], [3, 4],
          [4, 0], [4, 1], [4, 2], [4, 3]
        ]
      },
      {
        "key": "card_numbers_min",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "card_numbers_max",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "colours",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 21
      },
      {
        "key": "rank_red",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "rank_green",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "rank_violet",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "strength_number_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "key_count_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 100
      },
      {
        "key": "hand_size",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "palette_start_size",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "set_aside_2p",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "set_aside_3p",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "winner_points_2p",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "loser_points_2p",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "winner_points_3p",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "second_points_3p",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "first_out_points_3p",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "target_points_2p",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "target_points_3p",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "round_cap",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "even_number_1",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "even_number_2",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "even_number_3",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "low_number_max",
        "visible": "public",
        "type": "number",
        "initial": 3
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the match begins",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "points",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "is_recent_winner",
            "value": 0
          }
        },
        {
          "set": {
            "key": "most_recent_winner",
            "value": 0
          }
        },
        {
          "set": {
            "key": "round_no",
            "value": 0
          }
        },
        {
          "set": {
            "key": "hand_over",
            "value": true
          }
        }
      ]
    },
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
      "use": "update",
      "phase": "new hand",
      "label": "a new hand",
      "when": {
        "calc": "hand_over"
      },
      "do": [
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "all_cards"
            }
          }
        },
        {
          "set": {
            "key": "set_aside",
            "value": {
              "calc": "[]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "[]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "palette",
            "value": {
              "calc": "[]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "alive",
            "value": true
          }
        },
        {
          "set": {
            "players": "all",
            "key": "elim_order",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "key_value",
            "value": 0
          }
        },
        {
          "set_status": {
            "players": "all",
            "to": "playing"
          }
        },
        {
          "set": {
            "key": "eliminated_count",
            "value": 0
          }
        },
        {
          "set": {
            "key": "alive_count",
            "value": {
              "calc": "len(players)"
            }
          }
        },
        {
          "set": {
            "key": "canvas",
            "value": {
              "calc": "rank_red"
            }
          }
        }
      ]
    },
    {
      "use": "repeat",
      "phase": "new hand",
      "label": "the deal",
      "when": {
        "calc": "hand_over"
      },
      "until": {
        "calc": "all([len(p.hand) >= hand_size and len(p.palette) >= palette_start_size for p in players])"
      },
      "max": 30,
      "steps": [
        {
          "use": "update",
          "label": "deal one card",
          "do": [
            {
              "set": {
                "key": "pick",
                "value": {
                  "calc": "deck[int(uniform(0, len(deck)))]"
                }
              }
            },
            {
              "set": {
                "key": "deal_seat",
                "value": {
                  "calc": "min([p.seat for p in players if len(p.hand) < hand_size] + [p.seat + 100 for p in players if len(p.palette) < palette_start_size])"
                }
              }
            },
            {
              "append": {
                "player": {
                  "calc": "deal_seat"
                },
                "key": "hand",
                "value": {
                  "calc": "pick"
                },
                "if": {
                  "calc": "deal_seat < 100"
                }
              }
            },
            {
              "append": {
                "player": {
                  "calc": "deal_seat - 100"
                },
                "key": "palette",
                "value": {
                  "calc": "pick"
                },
                "if": {
                  "calc": "deal_seat >= 100"
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
            }
          ]
        }
      ]
    },
    {
      "use": "update",
      "phase": "new hand",
      "label": "set aside and first leader",
      "when": {
        "calc": "hand_over"
      },
      "do": [
        {
          "set": {
            "key": "set_aside",
            "value": {
              "calc": "deck"
            }
          }
        },
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "[]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "key_value",
            "value": {
              "calc": "max([0] + you.palette)"
            }
          }
        },
        {
          "set": {
            "key": "leader_seat",
            "value": {
              "calc": "min([p.seat for p in players if max([0] + p.palette) == max([max([0] + q.palette) for q in players])])"
            }
          }
        },
        {
          "set": {
            "key": "turn_seat",
            "value": {
              "calc": "leader_seat + 1 if leader_seat < len(players) else 1"
            }
          }
        },
        {
          "set": {
            "key": "hand_over",
            "value": false
          }
        }
      ],
      "text": "A new hand is dealt: {hand_size} hidden cards each and one face-up palette card. The Canvas is Red (3). Seat {leader_seat} has the strongest palette card, so seat {turn_seat} plays first."
    },
    {
      "use": "update",
      "phase": "round",
      "label": "start of round",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "acted_this_round",
            "value": false
          }
        }
      ]
    },
    {
      "use": "sync",
      "phase": "round",
      "label": "where you stand",
      "mode": "self",
      "to": "all",
      "text": "Where you stand:"
    },
    {
      "use": "repeat",
      "phase": "turns",
      "label": "the turns",
      "until": {
        "calc": "hand_over or all([p.acted_this_round for p in players if p.alive])"
      },
      "max": 10,
      "steps": [
        {
          "use": "update",
          "label": "your options",
          "do": [
            {
              "set": {
                "players": {
                  "where": "you.seat == turn_seat"
                },
                "key": "offer",
                "value": {
                  "calc": "['play ' + card_names[c] for c in you.hand] + ['discard ' + card_names[c] for c in you.hand] + ['play ' + card_names[you.hand[x[0]]] + ' then discard ' + card_names[you.hand[x[1]]] for x in pair_index if x[0] < len(you.hand) and x[1] < len(you.hand)] + ['fold']"
                }
              }
            }
          ]
        },
        {
          "use": "ask",
          "label": "your turn",
          "to": {
            "where": "you.seat == turn_seat"
          },
          "answer": {
            "type": "choice",
            "options": {
              "attribute": "offer"
            }
          },
          "verify": {
            "bind": "act"
          },
          "text": "Your turn. The Canvas rule is {canvas} (3 = Red, 2 = Green, 1 = Violet). Play a card to your palette, discard a card to make its colour the rule, play then discard two different cards, or fold. If you are not strictly leading afterwards, or you fold, you are eliminated from this hand."
        },
        {
          "use": "update",
          "label": "resolve the turn",
          "do": [
            {
              "set": {
                "key": "last_action",
                "value": "$act"
              }
            },
            {
              "set": {
                "players": {
                  "where": "you.seat == turn_seat"
                },
                "key": "sel_play",
                "value": {
                  "calc": "max([0] + [c for c in you.hand if $act == 'play ' + card_names[c]] + [you.hand[x[0]] for x in pair_index if x[0] < len(you.hand) and x[1] < len(you.hand) and $act == 'play ' + card_names[you.hand[x[0]]] + ' then discard ' + card_names[you.hand[x[1]]]])"
                }
              }
            },
            {
              "set": {
                "players": {
                  "where": "you.seat == turn_seat"
                },
                "key": "sel_discard",
                "value": {
                  "calc": "max([0] + [c for c in you.hand if $act == 'discard ' + card_names[c]] + [you.hand[x[1]] for x in pair_index if x[0] < len(you.hand) and x[1] < len(you.hand) and $act == 'play ' + card_names[you.hand[x[0]]] + ' then discard ' + card_names[you.hand[x[1]]]])"
                }
              }
            },
            {
              "set": {
                "key": "play_card",
                "value": {
                  "calc": "max([0] + [p.sel_play for p in players if p.seat == turn_seat])"
                }
              }
            },
            {
              "set": {
                "key": "discard_card",
                "value": {
                  "calc": "max([0] + [p.sel_discard for p in players if p.seat == turn_seat])"
                }
              }
            },
            {
              "remove": {
                "player": {
                  "calc": "turn_seat"
                },
                "key": "hand",
                "value": {
                  "calc": "play_card"
                },
                "if": {
                  "calc": "play_card > 0"
                }
              }
            },
            {
              "append": {
                "player": {
                  "calc": "turn_seat"
                },
                "key": "palette",
                "value": {
                  "calc": "play_card"
                },
                "if": {
                  "calc": "play_card > 0"
                }
              }
            },
            {
              "remove": {
                "player": {
                  "calc": "turn_seat"
                },
                "key": "hand",
                "value": {
                  "calc": "discard_card"
                },
                "if": {
                  "calc": "discard_card > 0"
                }
              }
            },
            {
              "set": {
                "key": "canvas",
                "value": {
                  "calc": "discard_card - int(discard_card / strength_number_multiplier) * strength_number_multiplier"
                },
                "if": {
                  "calc": "discard_card > 0"
                }
              }
            },
            {
              "set": {
                "player": {
                  "calc": "turn_seat"
                },
                "key": "acted_this_round",
                "value": true
              }
            },
            {
              "set": {
                "players": {
                  "where": "you.alive"
                },
                "key": "key_value",
                "value": {
                  "calc": "max([0] + you.palette) if canvas == rank_red else ((key_count_multiplier * len([s for s in you.palette if int(s / strength_number_multiplier) in [even_number_1, even_number_2, even_number_3]]) + max([0] + [s for s in you.palette if int(s / strength_number_multiplier) in [even_number_1, even_number_2, even_number_3]])) if canvas == rank_green else (key_count_multiplier * len([s for s in you.palette if int(s / strength_number_multiplier) <= low_number_max]) + max([0] + [s for s in you.palette if int(s / strength_number_multiplier) <= low_number_max])))"
                }
              }
            },
            {
              "set": {
                "key": "actor_out",
                "value": {
                  "calc": "$act == 'fold' or max([0] + [p.key_value for p in players if p.seat == turn_seat]) <= max([0] + [p.key_value for p in players if p.alive and p.seat != turn_seat])"
                }
              }
            },
            {
              "adjust": {
                "key": "eliminated_count",
                "value": 1,
                "if": {
                  "calc": "actor_out"
                }
              }
            },
            {
              "adjust": {
                "key": "alive_count",
                "value": -1,
                "if": {
                  "calc": "actor_out"
                }
              }
            },
            {
              "set": {
                "player": {
                  "calc": "turn_seat"
                },
                "key": "alive",
                "value": false,
                "if": {
                  "calc": "actor_out"
                }
              }
            },
            {
              "set": {
                "player": {
                  "calc": "turn_seat"
                },
                "key": "elim_order",
                "value": {
                  "calc": "eliminated_count"
                },
                "if": {
                  "calc": "actor_out"
                }
              }
            },
            {
              "set_status": {
                "player": {
                  "calc": "turn_seat"
                },
                "to": "out",
                "if": {
                  "calc": "actor_out"
                },
                "text": "Seat {player} is not leading and is eliminated from this hand. Their palette stays on the table but no longer counts."
              }
            }
          ],
          "text": "Seat {turn_seat}: {last_action}. The Canvas is now {canvas} (3 = Red, 2 = Green, 1 = Violet)."
        },
        {
          "use": "update",
          "label": "the hand ends",
          "when": {
            "calc": "alive_count <= 1 and not hand_over"
          },
          "do": [
            {
              "set": {
                "key": "hand_winner",
                "value": {
                  "calc": "max([0] + [p.seat for p in players if p.alive])"
                }
              }
            },
            {
              "adjust": {
                "player": {
                  "calc": "hand_winner"
                },
                "key": "points",
                "value": {
                  "calc": "winner_points_2p if len(players) == 2 else winner_points_3p"
                },
                "if": {
                  "calc": "hand_winner > 0"
                }
              }
            },
            {
              "adjust": {
                "player": {
                  "calc": "max([0] + [p.seat for p in players if p.elim_order == 1])"
                },
                "key": "points",
                "value": {
                  "calc": "loser_points_2p"
                },
                "if": {
                  "calc": "len(players) == 2 and any([p.elim_order == 1 for p in players])"
                }
              }
            },
            {
              "adjust": {
                "player": {
                  "calc": "max([0] + [p.seat for p in players if p.elim_order == 2])"
                },
                "key": "points",
                "value": {
                  "calc": "second_points_3p"
                },
                "if": {
                  "calc": "len(players) == 3 and any([p.elim_order == 2 for p in players])"
                }
              }
            },
            {
              "adjust": {
                "player": {
                  "calc": "max([0] + [p.seat for p in players if p.elim_order == 1])"
                },
                "key": "points",
                "value": {
                  "calc": "first_out_points_3p"
                },
                "if": {
                  "calc": "len(players) == 3 and any([p.elim_order == 1 for p in players])"
                }
              }
            },
            {
              "set": {
                "players": "all",
                "key": "is_recent_winner",
                "value": 0
              }
            },
            {
              "set": {
                "player": {
                  "calc": "hand_winner"
                },
                "key": "is_recent_winner",
                "value": 1,
                "if": {
                  "calc": "hand_winner > 0"
                }
              }
            },
            {
              "set": {
                "key": "most_recent_winner",
                "value": {
                  "calc": "hand_winner"
                }
              }
            },
            {
              "set": {
                "key": "hand_over",
                "value": true
              }
            }
          ],
          "text": "The hand is over: seat {most_recent_winner} is the last player alive and wins the hand. Points so far [seat, points]: {[[p.seat, p.points] for p in players]}."
        },
        {
          "use": "update",
          "label": "pass the turn",
          "when": {
            "calc": "not hand_over"
          },
          "do": [
            {
              "set": {
                "key": "turn_seat",
                "value": {
                  "calc": "min([p.seat for p in players if p.alive and p.seat > turn_seat]) if any([p.alive and p.seat > turn_seat for p in players]) else min([p.seat for p in players if p.alive])"
                }
              }
            }
          ]
        }
      ]
    },
    {
      "use": "update",
      "phase": "round end",
      "label": "count the round",
      "do": [
        {
          "adjust": {
            "key": "round_no",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "round end",
      "label": "is the match over",
      "when": {
        "calc": "(len(players) == 2 and max([p.points for p in players]) >= target_points_2p) or (len(players) == 3 and hand_over and max([p.points for p in players]) >= target_points_3p) or round_no >= round_cap"
      },
      "against": [
        "match_over"
      ]
    }
  ],
  "end": {
    "match_over": {
      "when": {
        "calc": "(len(players) == 2 and max([p.points for p in players]) >= target_points_2p) or (len(players) == 3 and hand_over and max([p.points for p in players]) >= target_points_3p) or round_no >= round_cap"
      },
      "rank_by": "you.points * 10 + you.is_recent_winner",
      "min_to_win": 1,
      "text": "Winner: {result}. Final points [seat, points]: {[[p.seat, p.points] for p in players]}; most recent hand winner: seat {most_recent_winner}."
    }
  },
  "limits": {
    "rounds": 40,
    "rounds_max": 40,
    "actions_max": 3000,
    "deadline_s": 120
  },
  "rules": "CARDS. There are {deck_size} cards: numbers {card_numbers_min} to {card_numbers_max} in each of {colours} colours, Red, Green and Violet. Colour rank is Red {rank_red}, Green {rank_green}, Violet {rank_violet}. A card's strength is number x {strength_number_multiplier} + colour rank (7 Red = 73, 4 Violet = 41). Higher strength beats lower. A card is EVEN if its number is {even_number_1}, {even_number_2} or {even_number_3}. A card is LOW if its number is {low_number_max} or less.\n\nTHE RULE. The Canvas shows one colour, which is the current rule (canvas 3 = Red, 2 = Green, 1 = Violet). Each living player has a KEY under the current rule:\n- Red: key = strength of the highest card in your palette.\n- Green: key = {key_count_multiplier} x (number of even cards in your palette) + strength of your highest even card, or 0 if you have no even card.\n- Violet: key = {key_count_multiplier} x (number of low cards in your palette) + strength of your highest low card, or 0 if you have no low card.\nYou are LEADING if your key is strictly higher than every other living player's key. If keys tie, including at 0, no tied player is leading.\n\nSETUP OF A HAND. Shuffle all {deck_size} cards. Deal each player {hand_size} cards as a hidden hand, then {palette_start_size} card face up as their palette. The remaining cards ({set_aside_2p} with 2 players, {set_aside_3p} with 3 players) are set aside unseen for this hand. The Canvas starts as Red. Everyone is alive. The initial leader is the player whose palette card has the highest strength. The first turn of the hand goes to the next player in seat order after that leader.\n\nA TURN. On your turn choose exactly one:\n(a) play one card from your hand face up to your palette;\n(b) discard one card from your hand to the Canvas, so the rule becomes that card's colour and the card leaves play;\n(c) do (a), then (b), with two different cards;\n(d) fold.\nThen keys are recomputed under the current rule. If you are leading, you stay in and play passes on. If you are not leading, or you folded, you are eliminated: your palette stays visible but no longer counts. If you have no cards left in hand when your turn comes, you can only fold. Play passes to the next living player in seat order.\n\nA ROUND is one pass of turns through all living players in seat order, starting with the player whose turn it is.\n\nEND OF A HAND. A hand ends the moment only one player is alive. That player is the hand winner.\n- With 2 players: the hand winner scores {winner_points_2p} point; the other scores {loser_points_2p}.\n- With 3 players: the hand winner scores {winner_points_3p} points; the player whose elimination left one survivor scores {second_points_3p}; the first player eliminated scores {first_out_points_3p}.\nThe hand winner is recorded as the MOST RECENT HAND WINNER. If the match is not over, a new hand is set up at the start of the next round.\n\nEND OF THE MATCH.\n- With 2 players, the match ends when a player reaches {target_points_2p} points.\n- With 3 players, the match ends after any hand in which a player reaches {target_points_3p} or more points.\n- In either case, it also ends when round {round_cap} is complete; an unfinished hand then scores nothing.\n\nINFORMATION. Palettes, the Canvas, eliminations, points and the most recent hand winner are public. Hands and set-aside cards are hidden. There is no table talk.\n\nWINNING. The player with the most points when the match ends wins. If two or more players share the most points, the tied player who won the most recently completed hand wins. If no hand was completed at all, the match is a draw."
}
```
````
