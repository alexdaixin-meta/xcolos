# 09 coder

- time: 2026-10-28T03:51:25+00:00 (106.1s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 58504347dc127e88, reply sha256 bf63da2454452822

## Sent

````
# Task: write the XColos game file for "Hogwash: Even Rounds"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 4; set `meta.players` to {"min": 3, "max": 4, "suggested": 3} (the suggested size is the one the game plays best at).

SETUP
- Deck: 25 cards, ranks 1 to 5, five copies of each rank.
- Shuffle once at the start. This shuffle and the deal are the only random events in the game.
- Seats are Player 1, Player 2, Player 3 (and Player 4 with four players). Clockwise means increasing seat number, wrapping from the last seat to Player 1.
- With 3 players, deal 8 cards to each player. With 4 players, deal 6 cards to each player.
- The one remaining card is placed face down as the first card of the central pile. Nobody sees it.
- Hands are private. Everyone always knows how many cards each player holds and how many cards are in the pile.
- Each player has a public 'taken' counter, starting at 0. It counts the total number of cards that player has picked up from the pile during the game.
- Turn 1: the required rank is 1 and Player 1 is the active player.
- A cycle is one turn for each seat in order, from Player 1 to the last seat. Turns 1 to 3 are cycle 1 with 3 players; turns 1 to 4 are cycle 1 with 4 players; and so on.

FINISHED PLAYERS
- A player holding 0 cards is finished.
- A finished player takes no turns: when their turn comes, it passes with no play, and the rank and turn still advance.
- A finished player writes no messages and is always counted as PASS in challenge polls.
- A finished player can never receive the pile.

EACH TURN
1. Announce the turn number, the active player and the required rank R.
2. Play. The active player secretly chooses 1, 2 or 3 cards from their hand (never more than they hold) and puts them face down on top of the pile.
   - It is announced: 'Player X plays N cards, claiming N cards of rank R.'
   - The claim is always exactly rank R and exactly the number of cards played.
   - The cards may be anything. Playing any card that is not rank R is a bluff.
3. Talk. Every player who still holds cards, including the active player, writes one short message at the same moment, without seeing the others. All messages are then shown to everyone.
   - Messages are not binding. Players may promise, threaten, bluff or lie.
4. Challenge poll. Every non-active player who holds cards simultaneously and secretly chooses CHALLENGE or PASS.
5. Resolution.
   - If nobody challenged, the cards stay in the pile.
   - Otherwise, the resolving challenger is the challenger who comes soonest clockwise after the active player.
   - Reveal only the cards just played.
   - If all of them are rank R, the claim was true: the resolving challenger takes the entire pile into their hand.
   - If any revealed card is not rank R, the claim was a bluff: the active player takes the entire pile into their hand.
   - Whoever took the pile adds the number of cards taken to their taken counter.
   - The pile is now empty. The result is announced: true or bluff, who took the pile, and how many cards.
   - Other challengers lose nothing.
6. Finish check. Any player now holding 0 cards is finished.
   - The first time any player becomes finished, the game is marked to end at the end of the current cycle.
   - A bluff that was caught never finishes the bluffer, because they have taken the pile back.
7. End check. The game ends if the turn just played was the last seat's turn and either of these is true:
   - the game has been marked to end; or
   - this was turn 36.
8. Advance. The required rank increases by 1, wrapping from 5 back to 1. The next seat clockwise becomes the active player.

NOTES
- Because 5 ranks share no factor with 3 or 4 seats, every seat is required to claim every rank over the course of five cycles.
- Because 36 turns is a whole number of cycles for both 3 and 4 players, every seat always gets the same number of turns.

How the winner is decided: When the game ends, every seat has had the same number of turns. Find the smallest hand size held by any player; this is 0 if anyone is finished. Among the players holding that many cards, the one with the lowest taken counter wins. If two or more of them tie on the lowest taken counter, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Hogwash: Even Rounds (3 to 4 players, best with 3)

A bluffing shedding game. Each turn the active player plays 1 to 3 cards face down and claims they are all the required rank. Others may challenge, and whoever is wrong takes the whole pile. The game ends at the end of the cycle in which someone empties their hand, or after 36 turns. Fewest cards wins, with fewest cards taken as the tie-break.

STATE (every item below must exist in the file):
  - each player: seat (number, starts 'seat number 1..N'); everyone sees it. Seat number; clockwise is increasing seat, wrapping from N to 1
  - each player: hand (list, starts 'dealt: 8 cards with 3 players, 6 with 4 players'); only its owner sees it. The cards (ranks 1-5) this player holds; private to the owner
  - each player: hand_count (number, starts '8 with 3 players, 6 with 4 players'); everyone sees it. Number of cards in hand; everyone always knows it
  - each player: taken (number, starts 0); everyone sees it. Total number of cards this player has picked up from the pile during the game
  - each player: finished (bool, starts False); everyone sees it. True once the player holds 0 cards; a finished player takes no turns, writes no messages, always passes and never receives the pile
  - each player: challenge (text, starts 'PASS'); only its owner sees it. This turn's secret CHALLENGE or PASS choice; PASS for the active player and for finished players
  - the table: deck (list, starts '25 cards: five each of ranks 1,2,3,4,5'); hidden from all players. The shuffled deck the hands and the first pile card are dealt from
  - the table: pile (list, starts '[] (receives the one leftover card at setup)'); hidden from all players. The face-down central pile
  - the table: pile_count (number, starts 1); everyone sees it. Number of cards in the pile; everyone always knows it
  - the table: last_played (list, starts []); hidden from all players. The cards played this turn; the only cards revealed when a challenge is resolved
  - the table: play_count (number, starts 0); everyone sees it. N, the number of cards played and claimed this turn
  - the table: turn (number, starts 1); everyone sees it. Current turn number
  - the table: required_rank (number, starts 1); everyone sees it. R, the rank the active player must claim this turn
  - the table: active_seat (number, starts 1); everyone sees it. Seat of the active player
  - the table: resolver_seat (number, starts 0); everyone sees it. The challenger soonest clockwise after the active seat; 0 if nobody challenged
  - the table: was_bluff (bool, starts False); everyone sees it. True if any card in last_played is not rank R; computed and announced only when challenged
  - the table: end_marked (bool, starts False); everyone sees it. True once any player has become finished; the game then ends at the end of the current cycle
  - parameters, each kept as a table attribute: deck_size = 25, rank_count = 5, copies_per_rank = 5, hand_size_3_players = 8, hand_size_4_players = 6, initial_pile_cards = 1, min_cards_per_play = 1, max_cards_per_play = 3, first_required_rank = 1, max_turns = 36, first_active_seat = 1, initial_taken = 0

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Build the deck list with 25 cards, five copies of each rank 1 to 5.
  2. Shuffle once: all later draws are random picks from the deck list, and this shuffle and deal are the only random events.
  3. With 3 players deal 8 cards to each player; with 4 players deal 6 cards to each player. Each card dealt is removed from deck and appended to that player's hand. Set hand_count to match.
  4. Move the one remaining deck card face down into pile and set pile_count = 1. Nobody sees it.
  5. Set each player's taken = 0 and finished = false.
  6. Set turn = 1, required_rank = 1, active_seat = 1 and end_marked = false.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [tell] all players. What happens: Announce: 'Turn {turn}: Player {active_seat} is active; required rank is {required_rank}.' If the active player is finished (hand_count = 0), also announce that their turn passes with no play. In that case steps 2-9 do not run (each carries when: active player's hand_count > 0).
  2. [ask] seat active_seat (only when its hand_count > 0) answers: a whole number from 1 to min(3, hand_count). What happens: Set play_count = the answer.
  3. [ask] seat active_seat (when hand_count > 0) answers: one card from the player's hand list (first card to play). What happens: Remove that card from the active player's hand and append it to last_played and to pile.
  4. [ask] seat active_seat (when play_count >= 2) answers: one card from the player's remaining hand list (second card to play). What happens: Remove that card from hand and append it to last_played and to pile.
  5. [ask] seat active_seat (when play_count >= 3) answers: one card from the player's remaining hand list (third card to play). What happens: Remove that card from hand and append it to last_played and to pile.
  6. [update] all players (when active player played). What happens: active player's hand_count -= play_count; pile_count += play_count. Announce 'Player {active_seat} plays {play_count} cards, claiming {play_count} cards of rank {required_rank}.'
  7. [poll] every player with hand_count > 0, including the active player (when active player played) answers: one short text message. What happens: No state change. Broadcast to all: 'Seat {seat} says: {value}'. Messages are non-binding.
  8. [poll] every non-active player with hand_count > 0 (when active player played) answers: CHALLENGE or PASS. What happens: Set each answering player's challenge to the answer. The active player and finished players keep challenge = PASS. Nobody sees any answer until all are in.
  9. [update] all players (when active player played). What happens: resolver_seat = the first seat s in clockwise order active_seat+1, active_seat+2, ... (wrapping, excluding active_seat) whose challenge = CHALLENGE; 0 if none. If resolver_seat = 0, the cards stay in pile and 'No challenge' is announced. Otherwise reveal last_played to all and set was_bluff = (count of cards in last_played whose rank != required_rank) > 0. Set taker = active_seat if was_bluff, else resolver_seat. The taker's hand gets every card in pile appended, the taker's hand_count += pile_count, and the taker's taken += pile_count. Then pile = [] and pile_count = 0. Announce 'true' or 'bluff', who took the pile and how many cards. Other challengers lose nothing.
  10. [update] all players. What happens: For each player, finished = (hand_count = 0). If any player has finished = true and end_marked = false, set end_marked = true and announce that the game ends at the end of this cycle.
  11. [check] all players. What happens: End the game if active_seat = number of players AND (end_marked = true OR turn = 36). Otherwise continue.
  12. [update] all players. What happens: required_rank = (required_rank mod 5) + 1; active_seat = (active_seat mod number_of_players) + 1; turn += 1. Clear last_played = [], play_count = 0, resolver_seat = 0, was_bluff = false, and every player's challenge = PASS.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game is set up, the deck holds 25 cards, five of each rank 1 to 5.
  R2. When there are 3 players, each player is dealt 8 cards; when there are 4 players, each is dealt 6 cards.
  R3. When dealing is complete, the 1 remaining card goes face down into the pile, so pile_count starts at 1 and the deck is empty.
  R4. When the game starts, every player's taken = 0, turn = 1, required_rank = 1 and active_seat = 1.
  R5. When an unfinished player is active, they must play at least 1 and at most min(3, hand_count) cards from their hand onto the pile.
  R6. When the active player plays N cards, the announced claim is exactly N cards of the current required rank R.
  R7. When cards are played, the active player's hand_count decreases by N and pile_count increases by N.
  R8. When cards have been played, every player with hand_count > 0, including the active player, writes one message simultaneously, and all messages are shown to everyone.
  R9. When the challenge poll runs, only non-active players with hand_count > 0 are asked, choosing CHALLENGE or PASS simultaneously; finished players count as PASS.
  R10. When nobody challenges, the played cards stay in the pile and no one's hand or taken changes.
  R11. When one or more players challenge, the resolving challenger is the challenger soonest clockwise after the active seat (e.g. with 4 players, active seat 3 and challengers 1 and 2, seat 1 resolves).
  R12. When challenged and every card just played is rank R, the resolving challenger takes the whole pile: their hand_count and taken each increase by pile_count.
  R13. When challenged and any card just played is not rank R, the active player takes the whole pile: their hand_count and taken each increase by pile_count.
  R14. When the pile is taken, pile_count becomes 0, and challengers other than the resolver lose nothing.
  R15. When a challenge is resolved, only the cards just played are revealed, and the result (true or bluff), the taker and the number of cards are announced.
  R16. When a player's hand_count is 0 after resolution, they are finished; a caught bluffer is never finished that turn, because they took the pile.
  R17. When a finished player's turn comes, no cards are played, no talk or challenge occurs, and the rank and active seat still advance.
  R18. When any player first becomes finished, end_marked becomes true.
  R19. When the last seat's turn ends and end_marked is true, the game ends.
  R20. When the last seat's turn ends and the turn number is 36, the game ends.
  R21. When a turn ends without ending the game, required_rank advances by 1 (5 wraps to 1), active_seat advances by 1 (the last seat wraps to 1), and turn increases by 1.
  R22. When the game ends, the player with the fewest cards in hand wins; among those level on fewest cards, the lowest taken wins; players level on both share the result (a draw).
  R23. A finished player can never receive the pile, since they never challenge and never play.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - How many cards to play | asked: the active seat, only if its hand_count > 0 | options: whole numbers 1 to min(3, hand_count); e.g. hand_count 1 gives only 1, hand_count 2 gives 1 or 2
  - Which card to play (first, second, third pick) | asked: the active seat, for as many picks as play_count | options: any card currently in that seat's hand list, of any rank
  - Talk message | asked: every seat with hand_count > 0, including the active seat | options: one short free-text message; finished seats are not asked
  - Challenge poll | asked: every non-active seat with hand_count > 0 | options: CHALLENGE or PASS; the active seat and finished seats are not asked

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: active_seat = number_of_players AND (end_marked = true OR turn = 36), checked after a turn
  - each player's standing: 0 - (you.hand_count * 1000 + you.taken) (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Fewest cards in hand ranks best; anyone finished holds 0. Among players level on the fewest cards, the lowest taken counter is better. The highest value of -(hand_count*1000 + taken) wins, and players level on both share the win (the source calls that a draw).
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

- each player: `hand_count` (number, visible: public, starts '8 with 3 players, 6 with 4 players'): Number of cards in hand; everyone always knows it
- each player: `taken` (number, visible: public, starts 0): Total number of cards this player has picked up from the pile during the game
- each player: `finished` (bool, visible: public, starts False): True once the player holds 0 cards; a finished player takes no turns, writes no messages, always passes and never receives the pile
- the table: `pile_count` (number, visible: public, starts 1): Number of cards in the pile; everyone always knows it
- the table: `turn` (number, visible: public, starts 1): Current turn number
- the table: `required_rank` (number, visible: public, starts 1): R, the rank the active player must claim this turn
- the table: `active_seat` (number, visible: public, starts 1): Seat of the active player
- the table: `end_marked` (bool, visible: public, starts False): True once any player has become finished; the game then ends at the end of the current cycle
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 25, rank_count = 5, copies_per_rank = 5, hand_size_3_players = 8, hand_size_4_players = 6, initial_pile_cards = 1, min_cards_per_play = 1, max_cards_per_play = 3, first_required_rank = 1, max_turns = 36, first_active_seat = 1, initial_taken = 0
- the game ends with ONE ending whose `rank_by` is `0 - (you.hand_count * 1000 + you.taken)`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
    "id": "hogwash_even_rounds",
    "name": "Hogwash: Even Rounds",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 3
    },
    "blurb": "Play 1 to 3 cards face down claiming the required rank; whoever is wrong about a challenge takes the whole pile. Fewest cards wins."
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
        "key": "hand_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "taken",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "finished",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "challenge",
        "visible": "ally",
        "type": "text",
        "initial": "PASS"
      }
    ],
    "game": [
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "pile",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "pile_count",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "last_played",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "play_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "turn",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "required_rank",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "active_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "resolver_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "was_bluff",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "end_marked",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "taker",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "cards_taken",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "verdict",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "revealed",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 25
      },
      {
        "key": "rank_count",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "copies_per_rank",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "hand_size_3_players",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "hand_size_4_players",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "initial_pile_cards",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "min_cards_per_play",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "max_cards_per_play",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "first_required_rank",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "max_turns",
        "visible": "public",
        "type": "number",
        "initial": 36
      },
      {
        "key": "first_active_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "initial_taken",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the deal",
      "do": [
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "1 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"append": {"player": {"calc": "0 - len(players) * int(0 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "1 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "1 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "2 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"append": {"player": {"calc": "1 - len(players) * int(1 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "2 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "2 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "3 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"append": {"player": {"calc": "2 - len(players) * int(2 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "3 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "3 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "4 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"append": {"player": {"calc": "3 - len(players) * int(3 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "4 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "4 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "5 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"append": {"player": {"calc": "4 - len(players) * int(4 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "5 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "5 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "6 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"append": {"player": {"calc": "5 - len(players) * int(5 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "6 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "6 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "7 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"append": {"player": {"calc": "6 - len(players) * int(6 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "7 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "7 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "8 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"append": {"player": {"calc": "7 - len(players) * int(7 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "8 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "8 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "9 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"append": {"player": {"calc": "8 - len(players) * int(8 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "9 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "9 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "10 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"append": {"player": {"calc": "9 - len(players) * int(9 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "10 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "10 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "11 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"append": {"player": {"calc": "10 - len(players) * int(10 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "11 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "11 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "12 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"append": {"player": {"calc": "11 - len(players) * int(11 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "12 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "12 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "13 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"append": {"player": {"calc": "12 - len(players) * int(12 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "13 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "13 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "14 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"append": {"player": {"calc": "13 - len(players) * int(13 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "14 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "14 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "15 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"append": {"player": {"calc": "14 - len(players) * int(14 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "15 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "15 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "16 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"append": {"player": {"calc": "15 - len(players) * int(15 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "16 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "16 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "17 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"append": {"player": {"calc": "16 - len(players) * int(16 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "17 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "17 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "18 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"append": {"player": {"calc": "17 - len(players) * int(17 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "18 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "18 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "19 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"append": {"player": {"calc": "18 - len(players) * int(18 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "19 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "19 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "20 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"append": {"player": {"calc": "19 - len(players) * int(19 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "20 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "20 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "21 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"append": {"player": {"calc": "20 - len(players) * int(20 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "21 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "21 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "22 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"append": {"player": {"calc": "21 - len(players) * int(21 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "22 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "22 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "23 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"append": {"player": {"calc": "22 - len(players) * int(22 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "23 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "23 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "24 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"append": {"player": {"calc": "23 - len(players) * int(23 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "24 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "24 <= (hand_size_3_players if len(players) == 3 else hand_size_4_players) * len(players)"}}}
      ]
    },
    {
      "use": "update",
      "label": "the first pile card and starting values",
      "do": [
        {
          "set": {
            "key": "pile",
            "value": {
              "calc": "deck"
            }
          }
        },
        {
          "set": {
            "key": "deck",
            "value": []
          }
        },
        {
          "set": {
            "key": "pile_count",
            "value": {
              "calc": "len(pile)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_count",
            "value": {
              "calc": "len(you.hand)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "taken",
            "value": {
              "calc": "initial_taken"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "finished",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "challenge",
            "value": "PASS"
          }
        },
        {
          "set": {
            "key": "turn",
            "value": 1
          }
        },
        {
          "set": {
            "key": "required_rank",
            "value": {
              "calc": "first_required_rank"
            }
          }
        },
        {
          "set": {
            "key": "active_seat",
            "value": {
              "calc": "first_active_seat"
            }
          }
        },
        {
          "set": {
            "key": "end_marked",
            "value": false
          }
        }
      ],
      "text": "The cards are dealt. One card lies face down as the start of the pile."
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
      "use": "tell",
      "phase": "announce",
      "label": "the turn",
      "to": "all",
      "text": "Turn {turn}: Player {active_seat} is active; required rank is {required_rank}."
    },
    {
      "use": "tell",
      "phase": "announce",
      "label": "a finished player passes",
      "when": {
        "calc": "not any(p.seat == active_seat and p.hand_count > 0 for p in players)"
      },
      "to": "all",
      "text": "Player {active_seat} is finished: the turn passes with no play."
    },
    {
      "use": "ask",
      "phase": "play",
      "label": "how many cards",
      "to": {
        "where": "you.seat == active_seat and you.hand_count > 0"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "min_cards_per_play"
        },
        "max": {
          "calc": "min(max_cards_per_play, you.hand_count)"
        }
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "play_count",
              "value": {
                "calc": "int($answer)"
              }
            }
          }
        ]
      },
      "text": "Turn {turn}: you must claim rank {required_rank}. How many cards will you play face down (from {min_cards_per_play} to {max_cards_per_play}, never more than you hold)? Your hand: {hand}."
    },
    {
      "use": "ask",
      "phase": "play",
      "label": "first card",
      "when": {
        "calc": "play_count >= 1"
      },
      "to": {
        "where": "you.seat == active_seat and you.hand_count > 0"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "each": {
        "do": [
          {
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": {
                "calc": "int($answer)"
              }
            }
          },
          {
            "append": {
              "key": "last_played",
              "value": {
                "calc": "int($answer)"
              }
            }
          },
          {
            "append": {
              "key": "pile",
              "value": {
                "calc": "int($answer)"
              }
            }
          }
        ]
      },
      "text": "Choose the first card to put face down. Any rank is allowed; a card that is not rank {required_rank} is a bluff. Your hand: {hand}."
    },
    {
      "use": "ask",
      "phase": "play",
      "label": "second card",
      "when": {
        "calc": "play_count >= 2"
      },
      "to": {
        "where": "you.seat == active_seat and you.hand_count > 0"
      },
      "answer": {
        "type": "choice",
        "option
... (cut)

Why it was refused: players are sent text with a `{name}` that was never filled in: placeholder: players are shown the literal {hand} (in `prompt`: 'Turn 1: you must claim rank 1. How many cards will you play face down (from 1 to 3, never '); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {hand} (in `prompt`: 'Choose the first card to put face down. Any rank is allowed; a card that is not rank 1 is '); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {hand} (in `prompt`: 'Choose the second card to put face down. Your remaining hand: {hand}.'); use only names the step can fill in (see the broadcast rule: {value} and {seat})
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "hogwash_even_rounds",
    "name": "Hogwash: Even Rounds",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 3
    },
    "blurb": "Play 1 to 3 cards face down claiming the required rank; whoever is wrong about a challenge takes the whole pile. Fewest cards wins."
  },
  "statuses": [
    {
      "id": "playing",
      "acts": true,
      "initial": true
    },
    {
      "id": "done",
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
        "key": "hand_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "taken",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "finished",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "challenge",
        "visible": "ally",
        "type": "text",
        "initial": "PASS"
      }
    ],
    "game": [
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "pile",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "pile_count",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "last_played",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "play_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "turn",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "required_rank",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "active_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "resolver_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "was_bluff",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "end_marked",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "taker",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "cards_taken",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "verdict",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "revealed",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 25
      },
      {
        "key": "rank_count",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "copies_per_rank",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "hand_size_3_players",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "hand_size_4_players",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "initial_pile_cards",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "min_cards_per_play",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "max_cards_per_play",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "first_required_rank",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "max_turns",
        "visible": "public",
        "type": "number",
        "initial": 36
      },
      {
        "key": "first_active_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "initial_taken",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the deal",
      "do": [
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "0 - len(players) * int(0 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "1 - len(players) * int(1 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "2 - len(players) * int(2 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "3 - len(players) * int(3 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "4 - len(players) * int(4 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "5 - len(players) * int(5 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "6 - len(players) * int(6 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "7 - len(players) * int(7 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "8 - len(players) * int(8 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "9 - len(players) * int(9 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "10 - len(players) * int(10 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "11 - len(players) * int(11 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "12 - len(players) * int(12 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "13 - len(players) * int(13 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "14 - len(players) * int(14 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "15 - len(players) * int(15 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "16 - len(players) * int(16 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "17 - len(players) * int(17 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "18 - len(players) * int(18 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "19 - len(players) * int(19 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "20 - len(players) * int(20 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "21 - len(players) * int(21 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "22 - len(players) * int(22 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": {"calc": "23 - len(players) * int(23 / len(players)) + 1"}, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}}
      ]
    },
    {
      "use": "update",
      "label": "the first pile card and starting values",
      "do": [
        {
          "set": {
            "key": "pile",
            "value": {
              "calc": "deck"
            }
          }
        },
        {
          "set": {
            "key": "deck",
            "value": []
          }
        },
        {
          "set": {
            "key": "pile_count",
            "value": {
              "calc": "len(pile)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_count",
            "value": {
              "calc": "len(you.hand)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "taken",
            "value": {
              "calc": "initial_taken"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "finished",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "challenge",
            "value": "PASS"
          }
        },
        {
          "set": {
            "key": "turn",
            "value": 1
          }
        },
        {
          "set": {
            "key": "required_rank",
            "value": {
              "calc": "first_required_rank"
            }
          }
        },
        {
          "set": {
            "key": "active_seat",
            "value": {
              "calc": "first_active_seat"
            }
          }
        },
        {
          "set": {
            "key": "end_marked",
            "value": false
          }
        }
      ],
      "text": "The cards are dealt. One card lies face down as the start of the pile."
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
      "use": "tell",
      "phase": "announce",
      "label": "the turn",
      "to": "all",
      "text": "Turn {turn}: Player {active_seat} is active; required rank is {required_rank}."
    },
    {
      "use": "tell",
      "phase": "announce",
      "label": "a finished player passes",
      "when": {
        "calc": "not any(p.seat == active_seat and p.hand_count > 0 for p in players)"
      },
      "to": "all",
      "text": "Player {active_seat} is finished: the turn passes with no play."
    },
    {
      "use": "ask",
      "phase": "play",
      "label": "how many cards",
      "to": {
        "where": "you.seat == active_seat and you.hand_count > 0"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "min_cards_per_play"
        },
        "max": {
          "calc": "min(max_cards_per_play, you.hand_count)"
        }
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "play_count",
              "value": {
                "calc": "int($answer)"
              }
            }
          }
        ]
      },
      "text": "Turn {turn}: you must claim rank {required_rank}. How many cards will you play face down (from {min_cards_per_play} to {max_cards_per_play}, never more than you hold)? Your hand is listed in your own state."
    },
    {
      "use": "ask",
      "phase": "play",
      "label": "first card",
      "when": {
        "calc": "play_count >= 1"
      },
      "to": {
        "where": "you.seat == active_seat and you.hand_count > 0"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "each": {
        "do": [
          {
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": {
                "calc": "int($answer)"
              }
            }
          },
          {
            "append": {
              "key": "last_played",
              "value": {
                "calc": "int($answer)"
              }
            }
          },
          {
            "append": {
              "key": "pile",
              "value": {
                "calc": "int($answer)"
              }
            }
          }
        ]
      },
      "text": "Choose the first card to put face down. Any rank is allowed; a card that is not rank {required_rank} is a bluff."
    },
    {
      "use": "ask",
      "phase": "play",
      "label": "second card",
      "when": {
        "calc": "play_count >= 2"
      },
      "to": {
        "where": "you.seat == active_seat and you.hand_count > 0"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "each": {
        "do": [
          {
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": {
                "calc": "int($answer)"
              }
            }
          },
          {
            "append": {
              "key": "last_played",
              "value": {
                "calc": "int($answer)"
              }
            }
          },
          {
            "append": {
              "key": "pile",
              "value": {
                "calc": "int($answer)"
              }
            }
          }
        ]
      },
      "text": "Choose the second card to put face down, from the cards you still hold."
    },
    {
      "use": "ask",
      "phase": "play",
      "label": "third card",
      "when": {
        "calc": "play_count >= 3"
      },
      "to": {
        "where": "you.seat == active_seat and you.hand_count > 0"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "each": {
        "do": [
          {
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": {
                "calc": "int($answer)"
              }
            }
          },
          {
            "append": {
              "key": "last_played",
              "value": {
                "calc": "int($answer)"
              }
            }
          },
          {
            "append": {
              "key": "pile",
              "value": {
                "calc": "int($answer)"
              }
            }
          }
        ]
      },
      "text": "Choose the third card to put face down, from the cards you still hold."
    },
    {
      "use": "update",
      "phase": "play",
      "label": "the claim",
      "when": {
        "calc": "play_count > 0"
      },
      "do": [
        {
          "adjust": {
            "player": {
              "calc": "active_seat"
            },
            "key": "hand_count",
            "value": {
              "calc": "0 - play_count"
            }
          }
        },
        {
          "adjust": {
            "key": "pile_count",
            "value": {
              "calc": "play_count"
            }
          }
        }
      ],
      "text": "Player {active_seat} plays {play_count} cards, claiming {play_count} cards of rank {required_rank}."
    },
    {
      "use": "poll",
      "phase": "talk",
      "label": "talk",
      "when": {
        "calc": "play_count > 0"
      },
      "to": {
        "where": "you.hand_count > 0"
      },
      "answer": {
        "type": "text",
        "max_words": 30
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} says: {value}"
      },
      "text": "Player {active_seat} claims {play_count} cards of rank {required_rank}. Write one short message to the table. Messages are not binding."
    },
    {
      "use": "poll",
      "phase": "challenge",
      "label": "challenge poll",
      "when": {
        "calc": "play_count > 0 and any(p.seat != active_seat and p.hand_count > 0 for p in players)"
      },
      "to": {
        "where": "you.seat != active_seat and you.hand_count > 0"
      },
      "answer": {
        "type": "choice",
        "options": [
          "CHALLENGE",
          "PASS"
        ]
      },
      "store": "challenge",
      "text": "Player {active_seat} claims {play_count} cards of rank {required_rank}; the pile holds {pile_count} cards. CHALLENGE or PASS? If you are the resolving challenger and the claim is true, you take the whole pile; if it is a bluff, Player {active_seat} takes it."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "resolution",
      "when": {
        "calc": "play_count > 0"
      },
      "do": [
        {
          "set": {
            "key": "resolver_seat",
            "value": {
              "calc": "min([p.seat for p in players if p.challenge == 'CHALLENGE' and p.seat > active_seat]) if count(p.challenge == 'CHALLENGE' and p.seat > active_seat for p in players) > 0 else (min([p.seat for p in players if p.challenge == 'CHALLENGE']) if count(p.challenge == 'CHALLENGE' for p in players) > 0 else 0)"
            }
          }
        },
        {
          "set": {
            "key": "was_bluff",
            "value": {
              "calc": "resolver_seat > 0 and count(c != required_rank for c in last_played) > 0"
            }
          }
        },
        {
          "set": {
            "key": "taker",
            "value": {
              "calc": "(active_seat if was_bluff else resolver_seat) if resolver_seat > 0 else 0"
            }
          }
        },
        {
          "set": {
            "key": "cards_taken",
            "value": {
              "calc": "pile_count if resolver_seat > 0 else 0"
            }
          }
        },
        {
          "set": {
            "key": "verdict",
            "value": {
              "calc": "('bluff' if was_bluff else 'true') if resolver_seat > 0 else ''"
            }
          }
        },
        {
          "set": {
            "key": "revealed",
            "value": {
              "calc": "last_played if resolver_seat > 0 else []"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == taker"
            },
            "key": "hand",
            "value": {
              "calc": "you.hand + pile"
            },
            "if": {
              "calc": "resolver_seat > 0"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat == taker"
            },
            "key": "hand_count",
            "value": {
              "calc": "cards_taken"
            },
            "if": {
              "calc": "resolver_seat > 0"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat == taker"
            },
            "key": "taken",
            "value": {
              "calc": "cards_taken"
            },
            "if": {
              "calc": "resolver_seat > 0"
            }
          }
        },
        {
          "set": {
            "key": "pile",
            "value": [],
            "if": {
              "calc": "resolver_seat > 0"
            }
          }
        },
        {
          "set": {
            "key": "pile_count",
            "value": 0,
            "if": {
              "calc": "resolver_seat > 0"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "resolve",
      "label": "no challenge",
      "when": {
        "calc": "play_count > 0 and resolver_seat == 0"
      },
      "to": "all",
      "text": "No challenge. The cards stay in the pile, which now holds {pile_count} cards."
    },
    {
      "use": "tell",
      "phase": "resolve",
      "label": "the reveal",
      "when": {
        "calc": "play_count > 0 and resolver_seat > 0"
      },
      "to": "all",
      "text": "Player {resolver_seat} resolves the challenge. The cards just played were {revealed}. The claim was {verdict}: Player {taker} takes the pile of {cards_taken} cards."
    },
    {
      "use": "update",
      "phase": "finish",
      "label": "finish check",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "finished",
            "value": {
              "calc": "you.hand_count == 0"
            }
          }
        },
        {
          "set_status": {
            "players": {
              "where": "you.hand_count == 0"
            },
            "to": "done",
            "text": "Player {player} has emptied their hand and is finished."
          }
        },
        {
          "set": {
            "key": "end_marked",
            "value": true,
            "if": {
              "calc": "not end_marked and any(p.finished for p in players)"
            },
            "text": "A player has finished: the game ends at the end of this cycle."
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "finish",
      "label": "end of cycle",
      "when": {
        "calc": "active_seat == len(players) and (end_marked or turn >= max_turns)"
      },
      "against": [
        "over"
      ]
    },
    {
      "use": "update",
      "phase": "advance",
      "label": "advance",
      "do": [
        {
          "set": {
            "key": "required_rank",
            "value": {
              "calc": "1 if required_rank >= rank_count else required_rank + 1"
            }
          }
        },
        {
          "set": {
            "key": "active_seat",
            "value": {
              "calc": "1 if active_seat >= len(players) else active_seat + 1"
            }
          }
        },
        {
          "adjust": {
            "key": "turn",
            "value": 1
          }
        },
        {
          "set": {
            "key": "last_played",
            "value": []
          }
        },
        {
          "set": {
            "key": "play_count",
            "value": 0
          }
        },
        {
          "set": {
            "key": "resolver_seat",
            "value": 0
          }
        },
        {
          "set": {
            "key": "was_bluff",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "challenge",
            "value": "PASS"
          }
        }
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "active_seat == len(players) and (end_marked or turn >= max_turns)"
      },
      "rank_by": "0 - (you.hand_count * 1000 + you.taken)",
      "text": "Winner: {result}. Final [seat, cards in hand, cards taken]: {[[p.seat, p.hand_count, p.taken] for p in players]}."
    }
  },
  "limits": {
    "rounds": 36,
    "rounds_max": 40,
    "actions_max": 1000,
    "deadline_s": 120
  },
  "rules": "SETUP. The deck has {deck_size} cards: ranks 1 to {rank_count}, {copies_per_rank} copies of each. It is shuffled once; this shuffle and the deal are the only random events. With 3 players each player is dealt {hand_size_3_players} cards; with 4 players each is dealt {hand_size_4_players}. The {initial_pile_cards} remaining card is placed face down as the first card of the central pile; nobody sees it. Hands are private, but everyone always knows how many cards each player holds and how many are in the pile. Each player has a public 'taken' counter starting at {initial_taken}: the total number of cards they have picked up from the pile. Turn 1: the required rank is {first_required_rank} and Player {first_active_seat} is active. Clockwise means increasing seat number, wrapping from the last seat to Player 1. A cycle is one turn for each seat, from Player 1 to the last seat.\n\nFINISHED PLAYERS. A player holding 0 cards is finished. A finished player takes no turns: when their turn comes it passes with no play, and the rank and turn still advance. A finished player writes no messages, is always counted as PASS in challenge polls, and can never receive the pile.\n\nEACH TURN. 1) The turn number, the active player and the required rank R are announced. 2) Play: the active player secretly chooses {min_cards_per_play} to {max_cards_per_play} cards from their hand (never more than they hold) and puts them face down on the pile. It is announced: 'Player X plays N cards, claiming N cards of rank R.' The claim is always exactly rank R and exactly the number of cards played. The cards may be anything; playing any card that is not rank R is a bluff. 3) Talk: every player who still holds cards, including the active player, writes one short message at the same moment; all messages are then shown to everyone. Messages are not binding: you may promise, threaten, bluff or lie. 4) Challenge poll: every non-active player who holds cards simultaneously and secretly chooses CHALLENGE or PASS. 5) Resolution: if nobody challenged, the cards stay in the pile and nobody's hand or taken counter changes. Otherwise the resolving challenger is the challenger who comes soonest clockwise after the active player. Only the cards just played are revealed. If all of them are rank R, the claim was true: the resolving challenger takes the entire pile into their hand. If any revealed card is not rank R, the claim was a bluff: the active player takes the entire pile into their hand. Whoever took the pile adds the number of cards taken to their taken counter, and the pile is then empty. The result (true or bluff), who took the pile and how many cards are announced. Other challengers lose nothing. 6) Finish check: any player now holding 0 cards is finished. The first time any player becomes finished, the game is marked to end at the end of the current cycle. A bluff that was caught never finishes the bluffer, because they have taken the pile back. 7) End check: the game ends if the turn just played was the last seat's turn and either the game has been marked to end, or this was turn {max_turns}. 8) Advance: the required rank increases by 1, wrapping from {rank_count} back to 1, and the next seat clockwise becomes the active player.\n\nWINNING. When the game ends every seat has had the same number of turns. The player holding the fewest cards wins (a finished player holds 0). Among players level on fewest cards, the one with the lowest taken counter wins. Players level on both share the result (a draw)."
}
```
````
