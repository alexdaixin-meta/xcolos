# 08 coder

- time: 2026-10-28T06:12:28+00:00 (71.9s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 1fc124cd19645ba5, reply sha256 ae38bb419bbe030e

## Sent

````
# Task: write the XColos game file for "Gracias: The Counted Gift"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 4 to 4; set `meta.players` to {"min": 4, "max": 4, "suggested": 4} (the suggested size is the one the game plays best at).

SETUP
- 4 players in seats 1-4. 4 colours: Red, Blue, Green, Yellow.
- The deck has 48 cards: 12 of each colour.
- Each player has, for each colour, a public count and a hidden count, all starting at 0, plus a game total (0) and a best session score (0).
- The game has 3 sessions of 4 rounds each, 12 rounds in all.

EACH ROUND
1. Shuffle (rounds 1, 5 and 9 only). All 48 cards are shuffled into a random order. This is the only random event in the game. No other round shuffles.
2. Lay out. The next 12 cards are removed from the top of the deck and form 4 triplets, T1 to T4. Each triplet has face-up cards A and B and a face-down card H. The A and B cards of all four triplets are announced to everyone. The H cards stay secret.
3. Draft. Players pick one at a time. In round r, seat ((r-1) mod 4) + 1 picks first, then the others in increasing seat order, wrapping from 4 to 1. On their turn a player chooses one remaining triplet, which of its two face-up cards to keep, and which opponent receives the other face-up card. They may not gift to themselves and must gift. The choice is resolved and announced at once:
   - the kept card adds 1 to the picker's public count of its colour;
   - the gifted card adds 1 to the receiver's public count of its colour;
   - the H card is told only to the picker and adds 1 to the picker's hidden count of its colour;
   - the triplet is removed. The last picker takes the one remaining triplet but still chooses which card to keep and whom to gift.
4. Announce. All public counts of every player are announced.

SESSION END (after rounds 4, 8 and 12)
5. Reveal. All hidden counts are revealed. For each player and colour, total = public count + hidden count. Across the four players, each colour's totals sum to 12.
6. Stacks. For each player and colour: stacks = floor(total / 4), and loose = total - 4 × stacks, so loose is 0, 1, 2 or 3.
7. Majority discard. For each colour, find the highest loose value among the 4 players. If it is at least 1, every player whose loose equals it scores none of those loose cards (ties all discard).
8. Session score. Each player scores 3 points per stack plus 1 point per loose card not discarded, summed over the 4 colours. This is added to their game total. If it exceeds their best session score, it becomes their best session score.
9. Reset. All public and hidden counts return to 0. The next session begins with a fresh shuffle in its first round.

COUNTING NOTE (public information): during a session, the cards not yet seen by a player are their opponents' hidden cards plus the undealt deck, and the colour make-up of these is exactly 12 per colour minus every public card minus that player's own hidden cards.

How the winner is decided: After session 3, the player with the highest game total wins. If several players tie, the one among them with the highest best session score wins. If they are still tied, the game is a draw among them.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Gracias: The Counted Gift (4 to 4 players, best with 4)

Four players draft face-up/face-down card triplets over 3 sessions of 4 rounds. In each pick a player keeps one face-up card, gifts the other to an opponent and secretly takes the hidden card. Sets of 4 in a colour score 3 points, and the largest leftover pile in each colour is discarded.

STATE (every item below must exist in the file):
  - each player: pub_red (number, starts 0); everyone sees it. Public count of Red cards this session (kept plus received as gifts)
  - each player: pub_blue (number, starts 0); everyone sees it. Public count of Blue cards this session
  - each player: pub_green (number, starts 0); everyone sees it. Public count of Green cards this session
  - each player: pub_yellow (number, starts 0); everyone sees it. Public count of Yellow cards this session
  - each player: hid_red (number, starts 0); only its owner sees it. Hidden count of Red H cards taken this session, known only to the owner until the session reveal
  - each player: hid_blue (number, starts 0); only its owner sees it. Hidden count of Blue H cards this session
  - each player: hid_green (number, starts 0); only its owner sees it. Hidden count of Green H cards this session
  - each player: hid_yellow (number, starts 0); only its owner sees it. Hidden count of Yellow H cards this session
  - each player: totals (list, starts [0, 0, 0, 0]); everyone sees it. At session end, public + hidden count per colour, in the order Red, Blue, Green, Yellow
  - each player: stacks (list, starts [0, 0, 0, 0]); everyone sees it. At session end, floor(total/4) per colour, in the order Red, Blue, Green, Yellow
  - each player: loose (list, starts [0, 0, 0, 0]); everyone sees it. At session end, total - 4*stacks per colour (0-3), in the order Red, Blue, Green, Yellow
  - each player: session_score (number, starts 0); everyone sees it. Score of the session just ended
  - each player: game_total (number, starts 0); everyone sees it. Sum of session scores; the main score
  - each player: best_session_score (number, starts 0); everyone sees it. Highest single session score so far; the tie-break
  - the table: deck (list, starts []); hidden from all players. Undealt cards (colour names); refilled to 12 of each colour (48) at rounds 1, 5 and 9
  - the table: round (number, starts 1); everyone sees it. Current round, 1 to 12
  - the table: session (number, starts 1); everyone sees it. Current session, 1 to 3
  - the table: t1_a (text, starts ''); everyone sees it. Triplet T1 face-up card A colour
  - the table: t1_b (text, starts ''); everyone sees it. Triplet T1 face-up card B colour
  - the table: t1_h (text, starts ''); hidden from all players. Triplet T1 face-down card H colour
  - the table: t2_a (text, starts ''); everyone sees it. Triplet T2 face-up card A colour
  - the table: t2_b (text, starts ''); everyone sees it. Triplet T2 face-up card B colour
  - the table: t2_h (text, starts ''); hidden from all players. Triplet T2 face-down card H colour
  - the table: t3_a (text, starts ''); everyone sees it. Triplet T3 face-up card A colour
  - the table: t3_b (text, starts ''); everyone sees it. Triplet T3 face-up card B colour
  - the table: t3_h (text, starts ''); hidden from all players. Triplet T3 face-down card H colour
  - the table: t4_a (text, starts ''); everyone sees it. Triplet T4 face-up card A colour
  - the table: t4_b (text, starts ''); everyone sees it. Triplet T4 face-up card B colour
  - the table: t4_h (text, starts ''); hidden from all players. Triplet T4 face-down card H colour
  - the table: open_triplets (list, starts []); everyone sees it. Triplets not yet taken this round (subset of T1, T2, T3, T4)
  - the table: max_loose (list, starts [0, 0, 0, 0]); everyone sees it. At session end, the highest loose value among the 4 players per colour, in the order Red, Blue, Green, Yellow
  - parameters, each kept as a table attribute: players = 4, colours = 4, cards_per_colour = 12, deck_size = 48, sessions = 3, rounds_per_session = 4, total_rounds = 12, triplets_per_round = 4, cards_per_triplet = 3, cards_laid_out_per_round = 12, shuffle_rounds_first = 1, shuffle_rounds_second = 5, shuffle_rounds_third = 9, stack_size = 4, points_per_stack = 3, points_per_loose_card = 1, min_loose_for_discard = 1, count_increment = 1, rank_tiebreak_multiplier = 1000

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seat 4 players in seats 1-4.
  2. Set every player's public and hidden counts for Red, Blue, Green and Yellow to 0, and set game_total, session_score and best_session_score to 0.
  3. Set round = 1 and session = 1. The deck is filled at the start of round 1.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] table. What happens: When round mod 4 == 1 (rounds 1, 5, 9): set deck to 48 cards, 12 each of Red, Blue, Green and Yellow (shuffle). No other round refills or shuffles the deck.
  2. [update] table. What happens: Lay out: draw 12 cards at random from deck, removing each one from deck, into t1_a, t1_b, t1_h, t2_a, t2_b, t2_h, t3_a, t3_b, t3_h, t4_a, t4_b, t4_h. Set open_triplets = [T1, T2, T3, T4].
  3. [tell] all players. What happens: Announce the A and B colours of T1-T4 (t1_a, t1_b, ..., t4_a, t4_b). The H cards stay secret.
  4. [ask] each player in turn, starting at seat ((round-1) mod 4)+1 and going up in seat order, wrapping from 4 to 1 answers: a choice from the list of every combination of (a triplet in open_triplets) x (keep A or keep B) x (an opponent seat to receive the other face-up card), e.g. 'T2: keep A (Red), give B (Blue) to seat 3'. What happens: The picker's pub_<kept colour> += 1. The chosen receiver's pub_<gifted colour> += 1. The triplet's H colour is told privately to the picker only, and the picker's hid_<H colour> += 1. The triplet is removed from open_triplets. The keep and the gift (not H) are announced to all at once.
  5. [tell] all players. What happens: Announce every player's pub_red, pub_blue, pub_green and pub_yellow.
  6. [tell] all players. What happens: When round mod 4 == 0: reveal every player's hid_red, hid_blue, hid_green and hid_yellow to everyone.
  7. [update] all players. What happens: When round mod 4 == 0: for each player and colour c, totals[c] = pub_c + hid_c, stacks[c] = floor(totals[c] / 4), loose[c] = totals[c] - 4*stacks[c].
  8. [update] table. What happens: When round mod 4 == 0: for each colour c, max_loose[c] = the maximum of loose[c] over the 4 players.
  9. [update] all players. What happens: When round mod 4 == 0: session_score = sum over the 4 colours of (3*stacks[c] + (loose[c] if NOT (max_loose[c] >= 1 and loose[c] == max_loose[c]) else 0)). Then game_total += session_score, and if session_score > best_session_score, best_session_score = session_score. Announce session_score, game_total and best_session_score.
  10. [update] all players. What happens: When round mod 4 == 0: set every pub_* and hid_* to 0, and session += 1.
  11. [update] table. What happens: round += 1.
  12. [check] table. What happens: End the game if round > 12; otherwise start the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. The deck has 48 cards: 12 each of Red, Blue, Green and Yellow.
  R2. When the round is 1, 5 or 9, the deck is reset to all 48 cards and shuffled; in no other round is it shuffled or refilled.
  R3. Each round, 12 cards leave the deck and form triplets T1-T4, each with face-up A and B and face-down H, so after the 4th round of a session the deck is empty.
  R4. When the triplets are laid out, the A and B colours of all four triplets are announced to everyone, and no H colour is announced.
  R5. In round r, seat ((r-1) mod 4)+1 picks first, then the others in increasing seat order, wrapping from 4 to 1 (round 2: seats 2, 3, 4, 1).
  R6. When a player picks, they choose one triplet still open, keep exactly one of its face-up cards, and gift the other face-up card to one opponent; gifting to oneself or not gifting is not offered.
  R7. When a player keeps a card of colour c, their pub_c rises by 1.
  R8. When a player is gifted a card of colour c, their pub_c rises by 1.
  R9. When a player takes a triplet, its H colour is told only to that player and their hid_<H colour> rises by 1.
  R10. When a triplet is taken, it is removed from open_triplets, and the 4th picker has exactly one triplet left but still chooses which card to keep and whom to gift.
  R11. After each round, every player's four public counts are announced.
  R12. After rounds 4, 8 and 12, every player's hidden counts are revealed and total = public + hidden per colour, and each colour's totals over the 4 players sum to 12.
  R13. At session end, stacks = floor(total/4) and loose = total - 4*stacks per colour (for example total 7 gives 1 stack and 3 loose).
  R14. For each colour, if the highest loose value among the players is at least 1, every player whose loose equals it scores 0 for those loose cards, and ties all discard.
  R15. Session score = 3 points per stack + 1 point per loose card not discarded, summed over the 4 colours (for example Red total 5 with Red max loose 2 gives 3+1 = 4 points).
  R16. When the session score is added, game_total rises by it, and best_session_score becomes it if it is greater than the old best.
  R17. After the session score, all public and hidden counts return to 0.
  R18. The game ends after round 12 (3 sessions of 4 rounds).
  R19. The highest game_total wins; a tie is broken by the highest best_session_score; players still tied share the win.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Draft pick (each player in turn) | asked: the seat whose turn it is | options: Every triplet in open_triplets x {keep A and gift B, keep B and gift A} x {each of the 3 other seats as receiver}: 24 options for the first picker, 18 for the second, 12 for the third, and 6 for the last picker (one triplet). The picker's own seat is never offered as receiver.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round > 12
  - each player's standing: you.game_total * 1000 + you.best_session_score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Highest game_total wins. Among players tied on it, the highest best_session_score wins. Players still tied share the win, which is the source's draw.
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

- each player: `session_score` (number, visible: public, starts 0): Score of the session just ended
- each player: `game_total` (number, visible: public, starts 0): Sum of session scores; the main score
- each player: `best_session_score` (number, visible: public, starts 0): Highest single session score so far; the tie-break
- the table: `round` (number, visible: public, starts 1): Current round, 1 to 12
- the table: `session` (number, visible: public, starts 1): Current session, 1 to 3
- parameters (each must be an attribute holding this value, never a number buried in a step): players = 4, colours = 4, cards_per_colour = 12, deck_size = 48, sessions = 3, rounds_per_session = 4, total_rounds = 12, triplets_per_round = 4, cards_per_triplet = 3, cards_laid_out_per_round = 12, shuffle_rounds_first = 1, shuffle_rounds_second = 5, shuffle_rounds_third = 9, stack_size = 4, points_per_stack = 3, points_per_loose_card = 1, min_loose_for_discard = 1, count_increment = 1, rank_tiebreak_multiplier = 1000
- the game ends with ONE ending whose `rank_by` is `you.game_total * 1000 + you.best_session_score`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
{
  "schema": 1,
  "meta": {
    "id": "gracias_the_counted_gift",
    "name": "Gracias: The Counted Gift",
    "players": {
      "min": 4,
      "max": 4,
      "suggested": 4
    },
    "blurb": "Draft triplets over 3 sessions: keep one face-up card, gift the other, secretly take the hidden one; sets of 4 score 3, the biggest leftover pile is discarded."
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
      {"key": "pub_red", "visible": "public", "type": "number", "initial": 0},
      {"key": "pub_blue", "visible": "public", "type": "number", "initial": 0},
      {"key": "pub_green", "visible": "public", "type": "number", "initial": 0},
      {"key": "pub_yellow", "visible": "public", "type": "number", "initial": 0},
      {"key": "hid_red", "visible": "ally", "type": "number", "initial": 0},
      {"key": "hid_blue", "visible": "ally", "type": "number", "initial": 0},
      {"key": "hid_green", "visible": "ally", "type": "number", "initial": 0},
      {"key": "hid_yellow", "visible": "ally", "type": "number", "initial": 0},
      {"key": "totals", "visible": "public", "type": "list", "initial": [0, 0, 0, 0]},
      {"key": "stacks", "visible": "public", "type": "list", "initial": [0, 0, 0, 0]},
      {"key": "loose", "visible": "public", "type": "list", "initial": [0, 0, 0, 0]},
      {"key": "session_score", "visible": "public", "type": "number", "initial": 0},
      {"key": "game_total", "visible": "public", "type": "number", "initial": 0},
      {"key": "best_session_score", "visible": "public", "type": "number", "initial": 0},
      {"key": "offer", "visible": "ally", "type": "list", "initial": []},
      {"key": "last_h", "visible": "ally", "type": "text", "initial": ""}
    ],
    "game": [
      {"key": "deck", "visible": "none", "type": "list", "initial": []},
      {"key": "round", "visible": "public", "type": "number", "initial": 1},
      {"key": "session", "visible": "public", "type": "number", "initial": 1},
      {"key": "t1_a", "visible": "public", "type": "text", "initial": ""},
      {"key": "t1_b", "visible": "public", "type": "text", "initial": ""},
      {"key": "t1_h", "visible": "none", "type": "text", "initial": ""},
      {"key": "t2_a", "visible": "public", "type": "text", "initial": ""},
      {"key": "t2_b", "visible": "public", "type": "text", "initial": ""},
      {"key": "t2_h", "visible": "none", "type": "text", "initial": ""},
      {"key": "t3_a", "visible": "public", "type": "text", "initial": ""},
      {"key": "t3_b", "visible": "public", "type": "text", "initial": ""},
      {"key": "t3_h", "visible": "none", "type": "text", "initial": ""},
      {"key": "t4_a", "visible": "public", "type": "text", "initial": ""},
      {"key": "t4_b", "visible": "public", "type": "text", "initial": ""},
      {"key": "t4_h", "visible": "none", "type": "text", "initial": ""},
      {"key": "open_triplets", "visible": "public", "type": "list", "initial": []},
      {"key": "max_loose", "visible": "public", "type": "list", "initial": [0, 0, 0, 0]},
      {"key": "picker", "visible": "none", "type": "number", "initial": 0},
      {"key": "picks_made", "visible": "none", "type": "number", "initial": 0},
      {"key": "trip", "visible": "none", "type": "text", "initial": ""},
      {"key": "kc", "visible": "none", "type": "text", "initial": ""},
      {"key": "gc", "visible": "none", "type": "text", "initial": ""},
      {"key": "hc", "visible": "none", "type": "text", "initial": ""},
      {"key": "recv", "visible": "none", "type": "number", "initial": 0},
      {"key": "players", "visible": "public", "type": "number", "initial": 4},
      {"key": "colours", "visible": "public", "type": "number", "initial": 4},
      {"key": "cards_per_colour", "visible": "public", "type": "number", "initial": 12},
      {"key": "deck_size", "visible": "public", "type": "number", "initial": 48},
      {"key": "sessions", "visible": "public", "type": "number", "initial": 3},
      {"key": "rounds_per_session", "visible": "public", "type": "number", "initial": 4},
      {"key": "total_rounds", "visible": "public", "type": "number", "initial": 12},
      {"key": "triplets_per_round", "visible": "public", "type": "number", "initial": 4},
      {"key": "cards_per_triplet", "visible": "public", "type": "number", "initial": 3},
      {"key": "cards_laid_out_per_round", "visible": "public", "type": "number", "initial": 12},
      {"key": "shuffle_rounds_first", "visible": "public", "type": "number", "initial": 1},
      {"key": "shuffle_rounds_second", "visible": "public", "type": "number", "initial": 5},
      {"key": "shuffle_rounds_third", "visible": "public", "type": "number", "initial": 9},
      {"key": "stack_size", "visible": "public", "type": "number", "initial": 4},
      {"key": "points_per_stack", "visible": "public", "type": "number", "initial": 3},
      {"key": "points_per_loose_card", "visible": "public", "type": "number", "initial": 1},
      {"key": "min_loose_for_discard", "visible": "public", "type": "number", "initial": 1},
      {"key": "count_increment", "visible": "public", "type": "number", "initial": 1},
      {"key": "rank_tiebreak_multiplier", "visible": "public", "type": "number", "initial": 1000}
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "zero the counts",
      "do": [
        {"set": {"players": "all", "key": "pub_red", "value": 0}},
        {"set": {"players": "all", "key": "pub_blue", "value": 0}},
        {"set": {"players": "all", "key": "pub_green", "value": 0}},
        {"set": {"players": "all", "key": "pub_yellow", "value": 0}},
        {"set": {"players": "all", "key": "hid_red", "value": 0}},
        {"set": {"players": "all", "key": "hid_blue", "value": 0}},
        {"set": {"players": "all", "key": "hid_green", "value": 0}},
        {"set": {"players": "all", "key": "hid_yellow", "value": 0}},
        {"set": {"players": "all", "key": "game_total", "value": 0}},
        {"set": {"players": "all", "key": "session_score", "value": 0}},
        {"set": {"players": "all", "key": "best_session_score", "value": 0}}
      ]
    },
    {
      "use": "update",
      "label": "first round and session",
      "do": [
        {"set": {"key": "round", "value": 1}},
        {"set": {"key": "session", "value": 1}}
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
      "phase": "layout",
      "label": "shuffle",
      "when": {
        "calc": "round in [shuffle_rounds_first, shuffle_rounds_second, shuffle_rounds_third]"
      },
      "do": [
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "['Red'] * cards_per_colour + ['Blue'] * cards_per_colour + ['Green'] * cards_per_colour + ['Yellow'] * cards_per_colour"
            }
          }
        }
      ],
      "text": "Session {session} begins: all {deck_size} cards are shuffled into a fresh deck."
    },
    {
      "use": "update",
      "phase": "layout",
      "label": "lay out",
      "do": [
        {"set": {"key": "t1_a", "value": {"calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"}}},
        {"remove": {"key": "deck", "value": {"calc": "t1_a"}}},
        {"set": {"key": "t1_b", "value": {"calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"}}},
        {"remove": {"key": "deck", "value": {"calc": "t1_b"}}},
        {"set": {"key": "t1_h", "value": {"calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"}}},
        {"remove": {"key": "deck", "value": {"calc": "t1_h"}}},
        {"set": {"key": "t2_a", "value": {"calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"}}},
        {"remove": {"key": "deck", "value": {"calc": "t2_a"}}},
        {"set": {"key": "t2_b", "value": {"calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"}}},
        {"remove": {"key": "deck", "value": {"calc": "t2_b"}}},
        {"set": {"key": "t2_h", "value": {"calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"}}},
        {"remove": {"key": "deck", "value": {"calc": "t2_h"}}},
        {"set": {"key": "t3_a", "value": {"calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"}}},
        {"remove": {"key": "deck", "value": {"calc": "t3_a"}}},
        {"set": {"key": "t3_b", "value": {"calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"}}},
        {"remove": {"key": "deck", "value": {"calc": "t3_b"}}},
        {"set": {"key": "t3_h", "value": {"calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"}}},
        {"remove": {"key": "deck", "value": {"calc": "t3_h"}}},
        {"set": {"key": "t4_a", "value": {"calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"}}},
        {"remove": {"key": "deck", "value": {"calc": "t4_a"}}},
        {"set": {"key": "t4_b", "value": {"calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"}}},
        {"remove": {"key": "deck", "value": {"calc": "t4_b"}}},
        {"set": {"key": "t4_h", "value": {"calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"}}},
        {"remove": {"key": "deck", "value": {"calc": "t4_h"}}},
        {"set": {"key": "open_triplets", "value": {"calc": "['T1', 'T2', 'T3', 'T4']"}}}
      ]
    },
    {
      "use": "tell",
      "phase": "layout",
      "label": "the triplets",
      "to": "all",
      "text": "Round {round} (session {session}). Face-up cards: T1 A {t1_a}, B {t1_b}; T2 A {t2_a}, B {t2_b}; T3 A {t3_a}, B {t3_b}; T4 A {t4_a}, B {t4_b}. Each triplet also has one face-down card."
    },
    {
      "use": "update",
      "phase": "draft",
      "label": "prepare the draft",
      "do": [
        {"set": {"key": "picker", "value": {"calc": "((round - 1) % players) + 1"}}},
        {"set": {"key": "picks_made", "value": 0}},
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "[x[0] + ': keep ' + k[0] + ' (' + x[k[2]] + '), give ' + k[1] + ' (' + x[k[3]] + ') to seat ' + r[1] for x in [['T1', t1_a, t1_b], ['T2', t2_a, t2_b], ['T3', t3_a, t3_b], ['T4', t4_a, t4_b]] if x[0] in open_triplets for k in [['A', 'B', 1, 2], ['B', 'A', 2, 1]] for r in [[1, '1'], [2, '2'], [3, '3'], [4, '4']] if r[0] != you.seat]"
            }
          }
        }
      ]
    },
    {
      "use": "repeat",
      "phase": "draft",
      "label": "the draft",
      "until": {
        "calc": "picks_made >= players"
      },
      "max": 4,
      "steps": [
        {
          "use": "ask",
          "phase": "draft",
          "label": "pick a triplet",
          "to": {
            "where": "you.seat == picker"
          },
          "answer": {
            "type": "choice",
            "options": {
              "attribute": "offer"
            }
          },
          "broadcast": {
            "to": "all",
            "text": "Seat {seat} picks {value}."
          },
          "each": {
            "do": [
              {"set": {"key": "trip", "value": {"calc": "'T1' if 'T1:' in $answer else ('T2' if 'T2:' in $answer else ('T3' if 'T3:' in $answer else 'T4'))"}}},
              {"set": {"key": "kc", "value": {"calc": "(t1_a if trip == 'T1' else (t2_a if trip == 'T2' else (t3_a if trip == 'T3' else t4_a))) if 'keep A' in $answer else (t1_b if trip == 'T1' else (t2_b if trip == 'T2' else (t3_b if trip == 'T3' else t4_b)))"}}},
              {"set": {"key": "gc", "value": {"calc": "(t1_b if trip == 'T1' else (t2_b if trip == 'T2' else (t3_b if trip == 'T3' else t4_b))) if 'keep A' in $answer else (t1_a if trip == 'T1' else (t2_a if trip == 'T2' else (t3_a if trip == 'T3' else t4_a)))"}}},
              {"set": {"key": "hc", "value": {"calc": "t1_h if trip == 'T1' else (t2_h if trip == 'T2' else (t3_h if trip == 'T3' else t4_h))"}}},
              {"set": {"key": "recv", "value": {"calc": "1 if 'to seat 1' in $answer else (2 if 'to seat 2' in $answer else (3 if 'to seat 3' in $answer else 4))"}}},
              {"adjust": {"player": "$seat", "key": "pub_red", "value": {"calc": "count_increment"}, "if": {"calc": "kc == 'Red'"}}},
              {"adjust": {"player": "$seat", "key": "pub_blue", "value": {"calc": "count_increment"}, "if": {"calc": "kc == 'Blue'"}}},
              {"adjust": {"player": "$seat", "key": "pub_green", "value": {"calc": "count_increment"}, "if": {"calc": "kc == 'Green'"}}},
              {"adjust": {"player": "$seat", "key": "pub_yellow", "value": {"calc": "count_increment"}, "if": {"calc": "kc == 'Yellow'"}}},
              {"adjust": {"player": {"calc": "recv"}, "key": "pub_red", "value": {"calc": "count_increment"}, "if": {"calc": "gc == 'Red'"}}},
              {"adjust": {"player": {"calc": "recv"}, "key": "pub_blue", "value": {"calc": "count_increment"}, "if": {"calc": "gc == 'Blue'"}}},
              {"adjust": {"player": {"calc": "recv"}, "key": "pub_green", "value": {"calc": "count_increment"}, "if": {"calc": "gc == 'Green'"}}},
              {"adjust": {"player": {"calc": "recv"}, "key": "pub_yellow", "value": {"calc": "count_increment"}, "if": {"calc": "gc == 'Yellow'"}}},
              {"adjust": {"player": "$seat", "key": "hid_red", "value": {"calc": "count_increment"}, "if": {"calc": "hc == 'Red'"}}},
              {"adjust": {"player": "$seat", "key": "hid_blue", "value": {"calc": "count_increment"}, "if": {"calc": "hc == 'Blue'"}}},
              {"adjust": {"player": "$seat", "key": "hid_green", "value": {"calc": "count_increment"}, "if": {"calc": "hc == 'Green'"}}},
              {"adjust": {"player": "$seat", "key": "hid_yellow", "value": {"calc": "count_increment"}, "if": {"calc": "hc == 'Yellow'"}}},
              {
                "set": {
                  "player": "$seat",
                  "key": "last_h",
                  "value": {"calc": "hc"},
                  "text": "The face-down card you took is {value}.",
                  "announce_to": {"where": "you.seat == picker"}
                }
              },
              {"remove": {"key": "open_triplets", "value": {"calc": "trip"}}},
              {"adjust": {"key": "picks_made", "value": 1}},
              {"set": {"key": "picker", "value": {"calc": "picker % players + 1"}}},
              {
                "set": {
                  "players": "all",
                  "key": "offer",
                  "value": {
                    "calc": "[x[0] + ': keep ' + k[0] + ' (' + x[k[2]] + '), give ' + k[1] + ' (' + x[k[3]] + ') to seat ' + r[1] for x in [['T1', t1_a, t1_b], ['T2', t2_a, t2_b], ['T3', t3_a, t3_b], ['T4', t4_a, t4_b]] if x[0] in open_triplets for k in [['A', 'B', 1, 2], ['B', 'A', 2, 1]] for r in [[1, '1'], [2, '2'], [3, '3'], [4, '4']] if r[0] != you.seat]"
                  }
                }
              }
            ]
          },
          "text": "Your pick. Choose one open triplet, which face-up card to keep, and which opponent receives the other face-up card. You also take the triplet's face-down card in secret."
        }
      ]
    },
    {
      "use": "tell",
      "phase": "announce",
      "label": "public counts",
      "to": "all",
      "text": "Public counts (Red/Blue/Green/Yellow): Seat 1 {players[0].pub_red}/{players[0].pub_blue}/{players[0].pub_green}/{players[0].pub_yellow}; Seat 2 {players[1].pub_red}/{players[1].pub_blue}/{players[1].pub_green}/{players[1].pub_yellow}; Seat 3 {players[2].pub_red}/{players[2].pub_blue}/{players[2].pub_green}/{players[2].pub_yellow}; Seat 4 {players[3].pub_red}/{players[3].pub_blue}/{players[3].pub_green}/{players[3].pub_yellow}."
    },
    {
      "use": "tell",
      "phase": "session end",
      "label": "reveal hidden counts",
      "when": {
        "calc": "round % rounds_per_session == 0"
      },
      "to": "all",
      "text": "Session {session} ends. Hidden counts (Red/Blue/Green/Yellow): Seat 1 {players[0].hid_red}/{players[0].hid_blue}/{players[0].hid_green}/{players[0].hid_yellow}; Seat 2 {players[1].hid_red}/{players[1].hid_blue}/{players[1].hid_green}/{players[1].hid_yellow}; Seat 3 {players[2].hid_red}/{players[2].hid_blue}/{players[2].hid_green}/{players[2].hid_yellow}; Seat 4 {players[3].hid_red}/{players[3].hid_blue}/{players[3].hid_green}/{players[3].hid_yellow}."
    },
    {
      "use": "update",
      "phase": "session end",
      "label": "totals and stacks",
      "when": {
        "calc": "round % rounds_per_session == 0"
      },
      "do": [
        {"set": {"players": "all", "key": "totals", "value": {"calc": "[you.pub_red + you.hid_red, you.pub_blue + you.hid_blue, you.pub_green + you.hid_green, you.pub_yellow + you.hid_yellow]"}}},
        {"set": {"players": "all", "key": "stacks", "value": {"calc": "[int(t / stack_size) for t in you.totals]"}}},
        {"set": {"players": "all", "key": "loose", "value": {"calc": "[you.totals[i] - stack_size * you.stacks[i] for i in [0, 1, 2, 3]]"}}}
      ]
    },
    {
      "use": "update",
      "phase": "session end",
      "label": "majority loose",
      "when": {
        "calc": "round % rounds_per_session == 0"
      },
      "do": [
        {"set": {"key": "max_loose", "value": {"calc": "[max([p.loose[i] for p in players]) for i in [0, 1, 2, 3]]"}}}
      ]
    },
    {
      "use": "update",
      "phase": "session end",
      "label": "session score",
      "when": {
        "calc": "round % rounds_per_session == 0"
      },
      "do": [
        {"set": {"players": "all", "key": "session_score", "value": {"calc": "sum([points_per_stack * you.stacks[i] + (0 if (max_loose[i] >= min_loose_for_discard and you.loose[i] == max_loose[i]) else points_per_loose_card * you.loose[i]) for i in [0, 1, 2, 3]])"}}},
        {"adjust": {"players": "all", "key": "game_total", "value": {"calc": "you.session_score"}}},
        {"set": {"players": "all", "key": "best_session_score", "value": {"calc": "max(you.best_session_score, you.session_score)"}}}
      ],
      "text": "Session scores: Seat 1 {players[0].session_score}, Seat 2 {players[1].session_score}, Seat 3 {players[2].session_score}, Seat 4 {players[3].session_score}. Game totals: {players[0].game_total}, {players[1].game_total}, {players[2].game_total}, {players[3].game_total}. Best sessions: {players[0].best_session_score}, {players[1].best_session_score}, {players[2].best_session_score}, {players[3].best_session_score}."
    },
    {
      "use": "update",
      "phase": "session end",
      "label": "reset counts",
      "when": {
        "calc": "round % rounds_per_session == 0"
      },
      "do": [
        {"set": {"players": "all", "key": "pub_red", "value": 0}},
        {"set": {"players": "all", "key": "pub_blue", "value": 0}},
        {"set": {"players": "all", "key": "pub_green", "value": 0}},
        {"set": {"players": "all", "key": "pub_yellow", "value": 0}},
        {"set": {"players": "all", "key": "hid_red", "value": 0}},
        {"set": {"players": "all", "key": "hid_blue", "value": 0}},
        {"set": {"players": "all", "key": "hid_green", "value": 0}},
        {"set": {"players": "all", "key": "hid_yellow", "value": 0}},
        {"adjust": {"key": "session", "value": 1}}
      ]
    },
    {
      "use": "update",
      "phase": "end of round",
      "label": "next round",
      "do": [
        {"adjust": {"key": "round", "value": 1}}
      ]
    },
    {
      "use": "check",
      "phase": "end of round",
      "label": "after round 12",
      "when": {
        "calc": "round > total_rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round > total_rounds"
      },
      "rank_by": "you.game_total * 1000 + you.best_session_score",
      "text": "Winner: {result}. Game totals: Seat 1 {players[0].game_total}, Seat 2 {players[1].game_total}, Seat 3 {players[2].game_total}, Seat 4 {players[3].game_total}; best sessions: {players[0].best_session_score}, {players[1].best_session_score}, {players[2].best_session_score}, {players[3].best_session_score}."
    }
  },
  "limits": {
    "rounds": 12,
    "rounds_max": 12,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "{players} players in seats 1-4. {colours} colours: Red, Blue, Green, Yellow. The deck has {deck_size} cards: {cards_per_colour} of each colour. Each player has, for each colour, a public count and a hidden count, all starting at 0, plus a game total (0) and a best session score (0). The game has {sessions} sessions of {rounds_per_session} rounds each, {total_rounds} rounds in all.\n\nEACH ROUND\n1. Shuffle (rounds {shuffle_rounds_first}, {shuffle_rounds_second} and {shuffle_rounds_third} only). All {deck_size} cards are shuffled into a random order. This is the only random event in the game. No other round shuffles.\n2. Lay out. The next {cards_laid_out_per_round} cards are removed from the top of the deck and form {triplets_per_round} triplets, T1 to T4. Each triplet has face-up cards A and B and a face-down card H. The A and B cards of all four triplets are announced to everyone. The H cards stay secret.\n3. Draft. Players pick one at a time. In round r, seat ((r-1) mod 4) + 1 picks first, then the others in increasing seat order, wrapping from 4 to 1. On their turn a player chooses one remaining triplet, which of its two face-up cards to keep, and which opponent receives the other face-up card. They may not gift to themselves and must gift. The choice is resolved and announced at once: the kept card adds 1 to the picker's public count of its colour; the gifted card adds 1 to the receiver's public count of its colour; the H card is told only to the picker and adds 1 to the picker's hidden count of its colour; the triplet is removed. The last picker takes the one remaining triplet but still chooses which card to keep and whom to gift.\n4. Announce. All public counts of every player are announced.\n\nSESSION END (after rounds 4, 8 and 12)\n5. Reveal. All hidden counts are revealed. For each player and colour, total = public count + hidden count. Across the four players, each colour's totals sum to {cards_per_colour}.\n6. Stacks. For each player and colour: stacks = floor(total / {stack_size}), and loose = total - {stack_size} x stacks, so loose is 0, 1, 2 or 3.\n7. Majority discard. For each colour, find the highest loose value among the 4 players. If it is at least {min_loose_for_discard}, every player whose loose equals it scores none of those loose cards (ties all discard). If the highest loose value is 0, nobody discards.\n8. Session score. Each player scores {points_per_stack} points per stack plus {points_per_loose_card} point per loose card not discarded, summed over the 4 colours. This is added to their game total. If it exceeds their best session score, it becomes their best session score; otherwise the best stays.\n9. Reset. All public and hidden counts return to 0. The next session begins with a fresh shuffle in its first round.\n\nCOUNTING NOTE (public information): during a session, the cards not yet seen by a player are their opponents' hidden cards plus the undealt deck, and the colour make-up of these is exactly {cards_per_colour} per colour minus every public card minus that player's own hidden cards.\n\nWINNER: After session 3, the player with the highest game total wins. If several players tie, the one among them with the highest best session score wins. If they are still tied, they share the win."
}

Why it was refused: playing it with random seats failed: seed 1, 4 players: the match crashed: CalcError: '((round - 1) % players) + 1': unsupported operand type(s) for %: 'int' and 'list'
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "gracias_the_counted_gift",
    "name": "Gracias: The Counted Gift",
    "players": {
      "min": 4,
      "max": 4,
      "suggested": 4
    },
    "blurb": "Draft triplets over 3 sessions: keep one face-up card, gift the other, secretly take the hidden one; sets of 4 score 3, the biggest leftover pile is discarded."
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
      {"key": "pub_red", "visible": "public", "type": "number", "initial": 0},
      {"key": "pub_blue", "visible": "public", "type": "number", "initial": 0},
      {"key": "pub_green", "visible": "public", "type": "number", "initial": 0},
      {"key": "pub_yellow", "visible": "public", "type": "number", "initial": 0},
      {"key": "hid_red", "visible": "ally", "type": "number", "initial": 0},
      {"key": "hid_blue", "visible": "ally", "type": "number", "initial": 0},
      {"key": "hid_green", "visible": "ally", "type": "number", "initial": 0},
      {"key": "hid_yellow", "visible": "ally", "type": "number", "initial": 0},
      {"key": "totals", "visible": "public", "type": "list", "initial": [0, 0, 0, 0]},
      {"key": "stacks", "visible": "public", "type": "list", "initial": [0, 0, 0, 0]},
      {"key": "loose", "visible": "public", "type": "list", "initial": [0, 0, 0, 0]},
      {"key": "session_score", "visible": "public", "type": "number", "initial": 0},
      {"key": "game_total", "visible": "public", "type": "number", "initial": 0},
      {"key": "best_session_score", "visible": "public", "type": "number", "initial": 0},
      {"key": "offer", "visible": "ally", "type": "list", "initial": []},
      {"key": "last_h", "visible": "ally", "type": "text", "initial": ""}
    ],
    "game": [
      {"key": "deck", "visible": "none", "type": "list", "initial": []},
      {"key": "round", "visible": "public", "type": "number", "initial": 1},
      {"key": "session", "visible": "public", "type": "number", "initial": 1},
      {"key": "t1_a", "visible": "public", "type": "text", "initial": ""},
      {"key": "t1_b", "visible": "public", "type": "text", "initial": ""},
      {"key": "t1_h", "visible": "none", "type": "text", "initial": ""},
      {"key": "t2_a", "visible": "public", "type": "text", "initial": ""},
      {"key": "t2_b", "visible": "public", "type": "text", "initial": ""},
      {"key": "t2_h", "visible": "none", "type": "text", "initial": ""},
      {"key": "t3_a", "visible": "public", "type": "text", "initial": ""},
      {"key": "t3_b", "visible": "public", "type": "text", "initial": ""},
      {"key": "t3_h", "visible": "none", "type": "text", "initial": ""},
      {"key": "t4_a", "visible": "public", "type": "text", "initial": ""},
      {"key": "t4_b", "visible": "public", "type": "text", "initial": ""},
      {"key": "t4_h", "visible": "none", "type": "text", "initial": ""},
      {"key": "open_triplets", "visible": "public", "type": "list", "initial": []},
      {"key": "max_loose", "visible": "public", "type": "list", "initial": [0, 0, 0, 0]},
      {"key": "picker", "visible": "none", "type": "number", "initial": 0},
      {"key": "picks_made", "visible": "none", "type": "number", "initial": 0},
      {"key": "trip", "visible": "none", "type": "text", "initial": ""},
      {"key": "kc", "visible": "none", "type": "text", "initial": ""},
      {"key": "gc", "visible": "none", "type": "text", "initial": ""},
      {"key": "hc", "visible": "none", "type": "text", "initial": ""},
      {"key": "recv", "visible": "none", "type": "number", "initial": 0},
      {"key": "players", "visible": "public", "type": "number", "initial": 4},
      {"key": "colours", "visible": "public", "type": "number", "initial": 4},
      {"key": "cards_per_colour", "visible": "public", "type": "number", "initial": 12},
      {"key": "deck_size", "visible": "public", "type": "number", "initial": 48},
      {"key": "sessions", "visible": "public", "type": "number", "initial": 3},
      {"key": "rounds_per_session", "visible": "public", "type": "number", "initial": 4},
      {"key": "total_rounds", "visible": "public", "type": "number", "initial": 12},
      {"key": "triplets_per_round", "visible": "public", "type": "number", "initial": 4},
      {"key": "cards_per_triplet", "visible": "public", "type": "number", "initial": 3},
      {"key": "cards_laid_out_per_round", "visible": "public", "type": "number", "initial": 12},
      {"key": "shuffle_rounds_first", "visible": "public", "type": "number", "initial": 1},
      {"key": "shuffle_rounds_second", "visible": "public", "type": "number", "initial": 5},
      {"key": "shuffle_rounds_third", "visible": "public", "type": "number", "initial": 9},
      {"key": "stack_size", "visible": "public", "type": "number", "initial": 4},
      {"key": "points_per_stack", "visible": "public", "type": "number", "initial": 3},
      {"key": "points_per_loose_card", "visible": "public", "type": "number", "initial": 1},
      {"key": "min_loose_for_discard", "visible": "public", "type": "number", "initial": 1},
      {"key": "count_increment", "visible": "public", "type": "number", "initial": 1},
      {"key": "rank_tiebreak_multiplier", "visible": "public", "type": "number", "initial": 1000}
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "zero the counts",
      "do": [
        {"set": {"players": "all", "key": "pub_red", "value": 0}},
        {"set": {"players": "all", "key": "pub_blue", "value": 0}},
        {"set": {"players": "all", "key": "pub_green", "value": 0}},
        {"set": {"players": "all", "key": "pub_yellow", "value": 0}},
        {"set": {"players": "all", "key": "hid_red", "value": 0}},
        {"set": {"players": "all", "key": "hid_blue", "value": 0}},
        {"set": {"players": "all", "key": "hid_green", "value": 0}},
        {"set": {"players": "all", "key": "hid_yellow", "value": 0}},
        {"set": {"players": "all", "key": "game_total", "value": 0}},
        {"set": {"players": "all", "key": "session_score", "value": 0}},
        {"set": {"players": "all", "key": "best_session_score", "value": 0}}
      ]
    },
    {
      "use": "update",
      "label": "first round and session",
      "do": [
        {"set": {"key": "round", "value": 1}},
        {"set": {"key": "session", "value": 1}}
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
      "phase": "layout",
      "label": "shuffle",
      "when": {
        "calc": "round in [shuffle_rounds_first, shuffle_rounds_second, shuffle_rounds_third]"
      },
      "do": [
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "['Red'] * cards_per_colour + ['Blue'] * cards_per_colour + ['Green'] * cards_per_colour + ['Yellow'] * cards_per_colour"
            }
          }
        }
      ],
      "text": "Session {session} begins: all {deck_size} cards are shuffled into a fresh deck."
    },
    {
      "use": "update",
      "phase": "layout",
      "label": "lay out",
      "do": [
        {"set": {"key": "t1_a", "value": {"calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"}}},
        {"remove": {"key": "deck", "value": {"calc": "t1_a"}}},
        {"set": {"key": "t1_b", "value": {"calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"}}},
        {"remove": {"key": "deck", "value": {"calc": "t1_b"}}},
        {"set": {"key": "t1_h", "value": {"calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"}}},
        {"remove": {"key": "deck", "value": {"calc": "t1_h"}}},
        {"set": {"key": "t2_a", "value": {"calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"}}},
        {"remove": {"key": "deck", "value": {"calc": "t2_a"}}},
        {"set": {"key": "t2_b", "value": {"calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"}}},
        {"remove": {"key": "deck", "value": {"calc": "t2_b"}}},
        {"set": {"key": "t2_h", "value": {"calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"}}},
        {"remove": {"key": "deck", "value": {"calc": "t2_h"}}},
        {"set": {"key": "t3_a", "value": {"calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"}}},
        {"remove": {"key": "deck", "value": {"calc": "t3_a"}}},
        {"set": {"key": "t3_b", "value": {"calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"}}},
        {"remove": {"key": "deck", "value": {"calc": "t3_b"}}},
        {"set": {"key": "t3_h", "value": {"calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"}}},
        {"remove": {"key": "deck", "value": {"calc": "t3_h"}}},
        {"set": {"key": "t4_a", "value": {"calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"}}},
        {"remove": {"key": "deck", "value": {"calc": "t4_a"}}},
        {"set": {"key": "t4_b", "value": {"calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"}}},
        {"remove": {"key": "deck", "value": {"calc": "t4_b"}}},
        {"set": {"key": "t4_h", "value": {"calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"}}},
        {"remove": {"key": "deck", "value": {"calc": "t4_h"}}},
        {"set": {"key": "open_triplets", "value": {"calc": "['T1', 'T2', 'T3', 'T4']"}}}
      ]
    },
    {
      "use": "tell",
      "phase": "layout",
      "label": "the triplets",
      "to": "all",
      "text": "Round {round} (session {session}). Face-up cards: T1 A {t1_a}, B {t1_b}; T2 A {t2_a}, B {t2_b}; T3 A {t3_a}, B {t3_b}; T4 A {t4_a}, B {t4_b}. Each triplet also has one face-down card."
    },
    {
      "use": "update",
      "phase": "draft",
      "label": "prepare the draft",
      "do": [
        {"set": {"key": "picker", "value": {"calc": "((round - 1) % len(players)) + 1"}}},
        {"set": {"key": "picks_made", "value": 0}},
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "[x[0] + ': keep ' + k[0] + ' (' + x[k[2]] + '), give ' + k[1] + ' (' + x[k[3]] + ') to seat ' + r[1] for x in [['T1', t1_a, t1_b], ['T2', t2_a, t2_b], ['T3', t3_a, t3_b], ['T4', t4_a, t4_b]] if x[0] in open_triplets for k in [['A', 'B', 1, 2], ['B', 'A', 2, 1]] for r in [[1, '1'], [2, '2'], [3, '3'], [4, '4']] if r[0] != you.seat]"
            }
          }
        }
      ]
    },
    {
      "use": "repeat",
      "phase": "draft",
      "label": "the draft",
      "until": {
        "calc": "picks_made >= len(players)"
      },
      "max": 4,
      "steps": [
        {
          "use": "ask",
          "phase": "draft",
          "label": "pick a triplet",
          "to": {
            "where": "you.seat == picker"
          },
          "answer": {
            "type": "choice",
            "options": {
              "attribute": "offer"
            }
          },
          "broadcast": {
            "to": "all",
            "text": "Seat {seat} picks {value}."
          },
          "each": {
            "do": [
              {"set": {"key": "trip", "value": {"calc": "'T1' if 'T1:' in $answer else ('T2' if 'T2:' in $answer else ('T3' if 'T3:' in $answer else 'T4'))"}}},
              {"set": {"key": "kc", "value": {"calc": "(t1_a if trip == 'T1' else (t2_a if trip == 'T2' else (t3_a if trip == 'T3' else t4_a))) if 'keep A' in $answer else (t1_b if trip == 'T1' else (t2_b if trip == 'T2' else (t3_b if trip == 'T3' else t4_b)))"}}},
              {"set": {"key": "gc", "value": {"calc": "(t1_b if trip == 'T1' else (t2_b if trip == 'T2' else (t3_b if trip == 'T3' else t4_b))) if 'keep A' in $answer else (t1_a if trip == 'T1' else (t2_a if trip == 'T2' else (t3_a if trip == 'T3' else t4_a)))"}}},
              {"set": {"key": "hc", "value": {"calc": "t1_h if trip == 'T1' else (t2_h if trip == 'T2' else (t3_h if trip == 'T3' else t4_h))"}}},
              {"set": {"key": "recv", "value": {"calc": "1 if 'to seat 1' in $answer else (2 if 'to seat 2' in $answer else (3 if 'to seat 3' in $answer else 4))"}}},
              {"adjust": {"player": "$seat", "key": "pub_red", "value": {"calc": "count_increment"}, "if": {"calc": "kc == 'Red'"}}},
              {"adjust": {"player": "$seat", "key": "pub_blue", "value": {"calc": "count_increment"}, "if": {"calc": "kc == 'Blue'"}}},
              {"adjust": {"player": "$seat", "key": "pub_green", "value": {"calc": "count_increment"}, "if": {"calc": "kc == 'Green'"}}},
              {"adjust": {"player": "$seat", "key": "pub_yellow", "value": {"calc": "count_increment"}, "if": {"calc": "kc == 'Yellow'"}}},
              {"adjust": {"player": {"calc": "recv"}, "key": "pub_red", "value": {"calc": "count_increment"}, "if": {"calc": "gc == 'Red'"}}},
              {"adjust": {"player": {"calc": "recv"}, "key": "pub_blue", "value": {"calc": "count_increment"}, "if": {"calc": "gc == 'Blue'"}}},
              {"adjust": {"player": {"calc": "recv"}, "key": "pub_green", "value": {"calc": "count_increment"}, "if": {"calc": "gc == 'Green'"}}},
              {"adjust": {"player": {"calc": "recv"}, "key": "pub_yellow", "value": {"calc": "count_increment"}, "if": {"calc": "gc == 'Yellow'"}}},
              {"adjust": {"player": "$seat", "key": "hid_red", "value": {"calc": "count_increment"}, "if": {"calc": "hc == 'Red'"}}},
              {"adjust": {"player": "$seat", "key": "hid_blue", "value": {"calc": "count_increment"}, "if": {"calc": "hc == 'Blue'"}}},
              {"adjust": {"player": "$seat", "key": "hid_green", "value": {"calc": "count_increment"}, "if": {"calc": "hc == 'Green'"}}},
              {"adjust": {"player": "$seat", "key": "hid_yellow", "value": {"calc": "count_increment"}, "if": {"calc": "hc == 'Yellow'"}}},
              {
                "set": {
                  "player": "$seat",
                  "key": "last_h",
                  "value": {"calc": "hc"},
                  "text": "The face-down card you took is {value}.",
                  "announce_to": {"where": "you.seat == picker"}
                }
              },
              {"remove": {"key": "open_triplets", "value": {"calc": "trip"}}},
              {"adjust": {"key": "picks_made", "value": 1}},
              {"set": {"key": "picker", "value": {"calc": "picker % len(players) + 1"}}},
              {
                "set": {
                  "players": "all",
                  "key": "offer",
                  "value": {
                    "calc": "[x[0] + ': keep ' + k[0] + ' (' + x[k[2]] + '), give ' + k[1] + ' (' + x[k[3]] + ') to seat ' + r[1] for x in [['T1', t1_a, t1_b], ['T2', t2_a, t2_b], ['T3', t3_a, t3_b], ['T4', t4_a, t4_b]] if x[0] in open_triplets for k in [['A', 'B', 1, 2], ['B', 'A', 2, 1]] for r in [[1, '1'], [2, '2'], [3, '3'], [4, '4']] if r[0] != you.seat]"
                  }
                }
              }
            ]
          },
          "text": "Your pick. Choose one open triplet, which face-up card to keep, and which opponent receives the other face-up card. You also take the triplet's face-down card in secret."
        }
      ]
    },
    {
      "use": "tell",
      "phase": "announce",
      "label": "public counts",
      "to": "all",
      "text": "Public counts (Red/Blue/Green/Yellow): Seat 1 {players[0].pub_red}/{players[0].pub_blue}/{players[0].pub_green}/{players[0].pub_yellow}; Seat 2 {players[1].pub_red}/{players[1].pub_blue}/{players[1].pub_green}/{players[1].pub_yellow}; Seat 3 {players[2].pub_red}/{players[2].pub_blue}/{players[2].pub_green}/{players[2].pub_yellow}; Seat 4 {players[3].pub_red}/{players[3].pub_blue}/{players[3].pub_green}/{players[3].pub_yellow}."
    },
    {
      "use": "tell",
      "phase": "session end",
      "label": "reveal hidden counts",
      "when": {
        "calc": "round % rounds_per_session == 0"
      },
      "to": "all",
      "text": "Session {session} ends. Hidden counts (Red/Blue/Green/Yellow): Seat 1 {players[0].hid_red}/{players[0].hid_blue}/{players[0].hid_green}/{players[0].hid_yellow}; Seat 2 {players[1].hid_red}/{players[1].hid_blue}/{players[1].hid_green}/{players[1].hid_yellow}; Seat 3 {players[2].hid_red}/{players[2].hid_blue}/{players[2].hid_green}/{players[2].hid_yellow}; Seat 4 {players[3].hid_red}/{players[3].hid_blue}/{players[3].hid_green}/{players[3].hid_yellow}."
    },
    {
      "use": "update",
      "phase": "session end",
      "label": "totals and stacks",
      "when": {
        "calc": "round % rounds_per_session == 0"
      },
      "do": [
        {"set": {"players": "all", "key": "totals", "value": {"calc": "[you.pub_red + you.hid_red, you.pub_blue + you.hid_blue, you.pub_green + you.hid_green, you.pub_yellow + you.hid_yellow]"}}},
        {"set": {"players": "all", "key": "stacks", "value": {"calc": "[int(t / stack_size) for t in you.totals]"}}},
        {"set": {"players": "all", "key": "loose", "value": {"calc": "[you.totals[i] - stack_size * you.stacks[i] for i in [0, 1, 2, 3]]"}}}
      ]
    },
    {
      "use": "update",
      "phase": "session end",
      "label": "majority loose",
      "when": {
        "calc": "round % rounds_per_session == 0"
      },
      "do": [
        {"set": {"key": "max_loose", "value": {"calc": "[max([p.loose[i] for p in players]) for i in [0, 1, 2, 3]]"}}}
      ]
    },
    {
      "use": "update",
      "phase": "session end",
      "label": "session score",
      "when": {
        "calc": "round % rounds_per_session == 0"
      },
      "do": [
        {"set": {"players": "all", "key": "session_score", "value": {"calc": "sum([points_per_stack * you.stacks[i] + (0 if (max_loose[i] >= min_loose_for_discard and you.loose[i] == max_loose[i]) else points_per_loose_card * you.loose[i]) for i in [0, 1, 2, 3]])"}}},
        {"adjust": {"players": "all", "key": "game_total", "value": {"calc": "you.session_score"}}},
        {"set": {"players": "all", "key": "best_session_score", "value": {"calc": "max(you.best_session_score, you.session_score)"}}}
      ],
      "text": "Session scores: Seat 1 {players[0].session_score}, Seat 2 {players[1].session_score}, Seat 3 {players[2].session_score}, Seat 4 {players[3].session_score}. Game totals: {players[0].game_total}, {players[1].game_total}, {players[2].game_total}, {players[3].game_total}. Best sessions: {players[0].best_session_score}, {players[1].best_session_score}, {players[2].best_session_score}, {players[3].best_session_score}."
    },
    {
      "use": "update",
      "phase": "session end",
      "label": "reset counts",
      "when": {
        "calc": "round % rounds_per_session == 0"
      },
      "do": [
        {"set": {"players": "all", "key": "pub_red", "value": 0}},
        {"set": {"players": "all", "key": "pub_blue", "value": 0}},
        {"set": {"players": "all", "key": "pub_green", "value": 0}},
        {"set": {"players": "all", "key": "pub_yellow", "value": 0}},
        {"set": {"players": "all", "key": "hid_red", "value": 0}},
        {"set": {"players": "all", "key": "hid_blue", "value": 0}},
        {"set": {"players": "all", "key": "hid_green", "value": 0}},
        {"set": {"players": "all", "key": "hid_yellow", "value": 0}},
        {"adjust": {"key": "session", "value": 1}}
      ]
    },
    {
      "use": "update",
      "phase": "end of round",
      "label": "next round",
      "do": [
        {"adjust": {"key": "round", "value": 1}}
      ]
    },
    {
      "use": "check",
      "phase": "end of round",
      "label": "after round 12",
      "when": {
        "calc": "round > total_rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round > total_rounds"
      },
      "rank_by": "you.game_total * 1000 + you.best_session_score",
      "text": "Winner: {result}. Game totals: Seat 1 {players[0].game_total}, Seat 2 {players[1].game_total}, Seat 3 {players[2].game_total}, Seat 4 {players[3].game_total}; best sessions: {players[0].best_session_score}, {players[1].best_session_score}, {players[2].best_session_score}, {players[3].best_session_score}."
    }
  },
  "limits": {
    "rounds": 12,
    "rounds_max": 12,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "4 players in seats 1-4. {colours} colours: Red, Blue, Green, Yellow. The deck has {deck_size} cards: {cards_per_colour} of each colour. Each player has, for each colour, a public count and a hidden count, all starting at 0, plus a game total (0) and a best session score (0). The game has {sessions} sessions of {rounds_per_session} rounds each, {total_rounds} rounds in all.\n\nEACH ROUND\n1. Shuffle (rounds {shuffle_rounds_first}, {shuffle_rounds_second} and {shuffle_rounds_third} only). All {deck_size} cards are shuffled into a random order. This is the only random event in the game. No other round shuffles.\n2. Lay out. The next {cards_laid_out_per_round} cards are removed from the top of the deck and form {triplets_per_round} triplets, T1 to T4. Each triplet has face-up cards A and B and a face-down card H. The A and B cards of all four triplets are announced to everyone. The H cards stay secret.\n3. Draft. Players pick one at a time. In round r, seat ((r-1) mod 4) + 1 picks first, then the others in increasing seat order, wrapping from 4 to 1. On their turn a player chooses one remaining triplet, which of its two face-up cards to keep, and which opponent receives the other face-up card. They may not gift to themselves and must gift. The choice is resolved and announced at once: the kept card adds 1 to the picker's public count of its colour; the gifted card adds 1 to the receiver's public count of its colour; the H card is told only to the picker and adds 1 to the picker's hidden count of its colour; the triplet is removed. The last picker takes the one remaining triplet but still chooses which card to keep and whom to gift.\n4. Announce. All public counts of every player are announced.\n\nSESSION END (after rounds 4, 8 and 12)\n5. Reveal. All hidden counts are revealed. For each player and colour, total = public count + hidden count. Across the four players, each colour's totals sum to {cards_per_colour}.\n6. Stacks. For each player and colour: stacks = floor(total / {stack_size}), and loose = total - {stack_size} x stacks, so loose is 0, 1, 2 or 3.\n7. Majority discard. For each colour, find the highest loose value among the 4 players. If it is at least {min_loose_for_discard}, every player whose loose equals it scores none of those loose cards (ties all discard). If the highest loose value is 0, nobody discards.\n8. Session score. Each player scores {points_per_stack} points per stack plus {points_per_loose_card} point per loose card not discarded, summed over the 4 colours. This is added to their game total. If it exceeds their best session score, it becomes their best session score; otherwise the best stays.\n9. Reset. All public and hidden counts return to 0. The next session begins with a fresh shuffle in its first round.\n\nCOUNTING NOTE (public information): during a session, the cards not yet seen by a player are their opponents' hidden cards plus the undealt deck, and the colour make-up of these is exactly {cards_per_colour} per colour minus every public card minus that player's own hidden cards.\n\nWINNER: After session 3, the player with the highest game total wins. If several players tie, the one among them with the highest best session score wins. If they are still tied, they share the win."
}
```
````
