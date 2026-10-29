# 10 coder

- time: 2026-10-28T04:08:04+00:00 (140.3s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 9ae60c3309dcb54f, reply sha256 8953e433c678796c

## Sent

````
# Task: write the XColos game file for "Three Up: Even Rounds"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

CARDS. There are 30 cards: three copies each of ranks 1 to 9 (27 cards) and three Clear cards.

SETUP.
1. Seat the three players in a random order called First, Second and Third. Turn order is First, Second, Third in every round.
2. Make three separately shuffled stacks: Low (all 1s, 2s and 3s; 9 cards), Mid (all 4s, 5s and 6s; 9 cards) and High (all 7s, 8s and 9s; 9 cards).
3. Deal each player 3 cards from Low, 3 from Mid, 3 from High and 1 Clear, so each player has 10 cards. Every card is dealt.
4. Each player privately looks at their cards.
5. At the same moment, each player chooses exactly 3 of their cards to be their Up pile. All Up piles are then revealed.
6. A player's remaining 7 cards are their Hand, which only that player sees.
7. The discard Pile starts empty, with a run count of 0. Each player's 'picked up' count starts at 0.

PUBLIC INFORMATION. At all times everyone can see:
- every card on the Pile, its top rank and its run count (how many cards of the top rank lie on top of the Pile in a row);
- every Up pile;
- each player's number of Hand cards;
- each player's picked-up count;
- the full history of plays and pickups.

EACH ROUND (at most 40 rounds).
(a) TALK. Every player writes one short message at the same moment without seeing the others. All messages are then shown to everyone. Messages bind no one.
(b) TURNS. First, then Second, then Third each take one turn as described below. A player who already has no cards in Hand or Up pile skips their turn.
(c) END CHECK. After Third's turn, look at every player who now has no cards in Hand or Up pile.
- If exactly one player is out of cards, that player wins.
- If two or three players are out of cards, the one among them with the lowest picked-up count wins. If they are tied on that count, the game is a draw.
- If nobody is out of cards, play continues.
(d) ROUND CAP. If round 40 ends with nobody out of cards, the player with the fewest cards (Hand plus Up pile) wins. A tie for fewest cards is broken by the lowest picked-up count. If players are still tied, the game is a draw.

A TURN. The player chooses one of two actions.
- PLAY: choose one rank and play one or more cards of that rank together, all from the same source.
  - The source must be your Hand while your Hand has any cards. You play from your Up pile only once your Hand is empty.
  - A numbered play is legal only if the Pile is empty or the rank is equal to or higher than the Pile's top rank.
  - A Clear is always legal and is played on its own.
- PICK UP: take every card on the Pile into your Hand, and add the number of cards taken to your picked-up count. The Pile becomes empty with a run count of 0. You may pick up even when you have a legal play. Picking up an empty Pile does nothing.
- An illegal or unreadable choice counts as PICK UP.

RESOLVING A PLAY.
- Numbered cards go on top of the Pile. If their rank equals the previous top rank, the run count rises by the number of cards played; otherwise the run count becomes the number of cards played.
- If the run count reaches 3 or more, the Pile is cleared: its cards are removed from the game, it becomes empty, and the run count is 0.
- A played Clear and the whole Pile are removed from the game, leaving the Pile empty.
- The turn then ends, and the next player acts on whatever Pile remains. An empty Pile accepts any card.

How the winner is decided: At the end of each round, if exactly one player has no cards left in Hand or Up pile, that player wins. If several players emptied by the end of the same round, the one with the lowest total of cards picked up during the game wins; if they are tied on that total, the game is a draw. If round 40 ends with nobody out of cards, the player with the fewest remaining cards wins, ties are broken by the lowest picked-up total, and a remaining tie is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Three Up: Even Rounds (3 to 3 players, best with 3)

A three-player shedding game: each round everyone talks at the same time, then First, Second and Third each play cards of one rank at or above the Pile's top rank, play a Clear, or pick up the Pile; the first to empty Hand and Up pile wins, and the lowest picked-up total breaks ties.

STATE (every item below must exist in the file):
  - each player: hand (list, starts []); only its owner sees it. The player's Hand cards, each written as '1'..'9' or 'C' for a Clear. Only the owner sees them.
  - each player: up_choice (list, starts []); only its owner sees it. The cards picked for the Up pile during the simultaneous setup choice, held privately until every player has chosen.
  - each player: up_pile (list, starts []); everyone sees it. The player's revealed Up pile of 3 cards.
  - each player: hand_count (number, starts 0); everyone sees it. The number of cards in Hand.
  - each player: up_count (number, starts 0); everyone sees it. The number of cards in the Up pile.
  - each player: cards_left (number, starts 0); everyone sees it. hand_count + up_count.
  - each player: picked_up (number, starts 0); everyone sees it. The total number of cards this player has taken from the Pile during the game.
  - each player: out (bool, starts False); everyone sees it. True when cards_left is 0. An out player skips their turns.
  - the table: low_stack (list, starts ['1', '1', '1', '2', '2', '2', '3', '3', '3']); hidden from all players. The shuffled Low stack.
  - the table: mid_stack (list, starts ['4', '4', '4', '5', '5', '5', '6', '6', '6']); hidden from all players. The shuffled Mid stack.
  - the table: high_stack (list, starts ['7', '7', '7', '8', '8', '8', '9', '9', '9']); hidden from all players. The shuffled High stack.
  - the table: clear_stack (list, starts ['C', 'C', 'C']); hidden from all players. The three Clear cards before the deal.
  - the table: pile (list, starts []); everyone sees it. The discard Pile, bottom to top.
  - the table: top_rank (number, starts 0); everyone sees it. The rank of the Pile's top card, or 0 when the Pile is empty.
  - the table: run_count (number, starts 0); everyone sees it. How many cards of the top rank lie in a row on top of the Pile.
  - the table: removed (list, starts []); everyone sees it. Cards removed from the game by run clears and Clears.
  - the table: history (list, starts []); everyone sees it. The full public log of plays and pickups.
  - the table: round (number, starts 0); everyone sees it. The current round number.
  - the table: players_out (number, starts 0); everyone sees it. The number of players with out = true.
  - parameters, each kept as a table attribute: total_cards = 30, lowest_rank = 1, highest_rank = 9, copies_per_rank = 3, clear_cards = 3, stack_size = 9, low_ranks_max = 3, mid_ranks_max = 6, high_ranks_max = 9, deal_per_stack = 3, clear_per_player = 1, cards_per_player = 10, up_pile_size = 3, hand_after_up = 7, run_to_clear = 3, max_rounds = 40, rank_out_weight = 1000000, rank_cards_weight = 10000

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seats are assigned in random (seeded) order. Seat 1 is First, seat 2 is Second and seat 3 is Third, and turn order is seat 1, 2, 3 in every round.
  2. low_stack, mid_stack and high_stack are each shuffled separately. Drawing at random from a stack is the shuffle.
  3. Each player draws 3 cards at random from low_stack, 3 from mid_stack and 3 from high_stack, and takes 1 card from clear_stack. Each card is appended to that player's hand and removed from its stack. Every stack ends empty and each hand holds 10 cards.
  4. Each player privately sees their own hand.
  5. Up pile selection, done simultaneously by poll: three successive polls ask every player at once to choose one card from their own hand. Each chosen card moves from hand to up_choice (visible only to the owner), so nobody sees another player's choice until all three picks are made.
  6. When every player has 3 cards in up_choice, each up_choice is copied to up_pile (public) and emptied. All Up piles are announced to everyone.
  7. Every player gets hand_count = 7, up_count = 3, cards_left = 10, picked_up = 0 and out = false.
  8. The table starts with pile = [], top_rank = 0, run_count = 0, removed = [], round = 0 and players_out = 0.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round += 1; announce the round number, pile, top_rank, run_count, every up_pile, hand_count and picked_up.
  2. [poll] all players answers: short text (one message). What happens: Every message is shown to everyone at once: broadcast {"to": "all", "text": "Seat {seat} says: {value}"}. No state changes and nothing binds.
  3. [sync] all players. What happens: Each player receives their own hand, plus the public pile, top_rank, run_count, up_piles, hand_counts and picked_up counts.
  4. [ask] seat 1 (First), when out = false answers: one choice from the offered list: 'pick up', 'play Clear' (only if the source holds a C), or 'play K x rank R' for each rank R held in the source with R >= top_rank (any rank if the pile is empty) and each K from 1 to the number of R cards held. The source is hand if hand_count > 0, otherwise up_pile.. What happens: Records the chosen action. An illegal or unreadable answer counts as 'pick up'.
  5. [update] seat 1 (First), when out = false. What happens: PICK UP: append every pile card to hand; picked_up += len(pile); pile = []; top_rank = 0; run_count = 0. PLAY K x R: remove K R cards from the source and append them to pile; if R == top_rank then run_count += K, else run_count = K; top_rank = R; if run_count >= 3, move all pile cards to removed, set pile = [], top_rank = 0, run_count = 0. PLAY Clear: move the C and all pile cards to removed; pile = []; top_rank = 0; run_count = 0. Then recompute hand_count, up_count and cards_left = hand_count + up_count; out = (cards_left == 0); append the action to history; announce it.
  6. [ask] seat 2 (Second), when out = false answers: as for seat 1, against the current pile. What happens: Records the chosen action. An illegal or unreadable answer counts as 'pick up'.
  7. [update] seat 2 (Second), when out = false. What happens: Resolved exactly as for seat 1.
  8. [ask] seat 3 (Third), when out = false answers: as for seat 1, against the current pile. What happens: Records the chosen action. An illegal or unreadable answer counts as 'pick up'.
  9. [update] seat 3 (Third), when out = false. What happens: Resolved exactly as for seat 1.
  10. [update] all players. What happens: players_out = the number of players with out = true.
  11. [check] all players. What happens: End the game if players_out >= 1 or round >= 40; otherwise continue to the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game is set up, there are 30 cards: three each of ranks 1 to 9 and three Clears.
  R2. When cards are dealt, each player gets 3 cards from Low (ranks 1-3), 3 from Mid (4-6), 3 from High (7-9) and 1 Clear, 10 cards in all, and every stack ends empty.
  R3. When Up piles are chosen, every player chooses exactly 3 of their own cards simultaneously; all Up piles are then made public and each hand holds 7 cards.
  R4. When setup ends, pile is empty, top_rank = 0, run_count = 0 and every picked_up = 0.
  R5. When a round starts, every player writes one message at the same time, and all messages are shown to everyone only after all are in.
  R6. When it is a player's turn, seats act in order 1 (First), 2 (Second), 3 (Third), and a player with cards_left = 0 skips the turn.
  R7. When a player has hand_count > 0, they may play only from hand; when hand_count = 0, they play from up_pile.
  R8. When a player plays numbered cards, all cards are of one rank and from one source, and the play is legal only if the pile is empty or the rank >= top_rank (e.g., on top_rank 5, a 5 or 9 is legal and a 4 is not).
  R9. When a player plays K cards of rank R equal to top_rank, run_count increases by K; when R differs from top_rank, run_count becomes K and top_rank becomes R.
  R10. When run_count reaches 3 or more, all pile cards go to removed, the pile empties, and top_rank and run_count become 0.
  R11. When a player plays a Clear, it is played alone and is always legal; the Clear and the whole pile go to removed, and top_rank and run_count become 0.
  R12. When a player picks up, every pile card moves to their hand, picked_up increases by the number of cards taken, and pile, top_rank and run_count reset to empty/0; picking up an empty pile changes nothing.
  R13. When a player may legally play, they may still choose to pick up.
  R14. When a player's answer is illegal or unreadable, it is resolved as a pick up.
  R15. When seat 3's turn ends and exactly one player has cards_left = 0, that player wins.
  R16. When seat 3's turn ends and two or three players have cards_left = 0, the one among them with the lowest picked_up wins, and a tie on picked_up is a draw between them.
  R17. When a player empties mid-round, the round still continues to seat 3 before any end check.
  R18. When round 40 ends with nobody out, the fewest cards_left wins, ties are broken by the lowest picked_up, and a remaining tie is a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Talk message each round | asked: all players (including out players) | options: One short free-text message.
  - Up pile pick (setup, three simultaneous polls) | asked: every seat | options: Any one card still in their own hand.
  - Turn action | asked: the seat whose turn it is, if out = false; an out seat is not asked | options: Always 'pick up'. 'play Clear' if the source (hand if non-empty, else up_pile) holds a C. 'play K x rank R' for each rank R in the source with R >= top_rank (any rank when the pile is empty), with K from 1 to the count of R cards in that source. Cards from the other source are never offered.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: players_out >= 1 or round >= 40 (checked only after seat 3's turn)
  - each player's standing: you.out * 1000000 - you.cards_left * 10000 - you.picked_up (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: If any player is out at the end of the round, only the out players can win, and among them the lowest picked_up wins; out players tied on picked_up share the result (a draw). If round 40 ends with nobody out, the fewest cards_left wins, then the lowest picked_up, and players still tied share the result (a draw).
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

- each player: `up_pile` (list, visible: public, starts []): The player's revealed Up pile of 3 cards.
- each player: `hand_count` (number, visible: public, starts 0): The number of cards in Hand.
- each player: `up_count` (number, visible: public, starts 0): The number of cards in the Up pile.
- each player: `cards_left` (number, visible: public, starts 0): hand_count + up_count.
- each player: `picked_up` (number, visible: public, starts 0): The total number of cards this player has taken from the Pile during the game.
- each player: `out` (bool, visible: public, starts False): True when cards_left is 0. An out player skips their turns.
- the table: `pile` (list, visible: public, starts []): The discard Pile, bottom to top.
- the table: `top_rank` (number, visible: public, starts 0): The rank of the Pile's top card, or 0 when the Pile is empty.
- the table: `run_count` (number, visible: public, starts 0): How many cards of the top rank lie in a row on top of the Pile.
- the table: `round` (number, visible: public, starts 0): The current round number.
- the table: `players_out` (number, visible: public, starts 0): The number of players with out = true.
- parameters (each must be an attribute holding this value, never a number buried in a step): total_cards = 30, lowest_rank = 1, highest_rank = 9, copies_per_rank = 3, clear_cards = 3, stack_size = 9, low_ranks_max = 3, mid_ranks_max = 6, high_ranks_max = 9, deal_per_stack = 3, clear_per_player = 1, cards_per_player = 10, up_pile_size = 3, hand_after_up = 7, run_to_clear = 3, max_rounds = 40, rank_out_weight = 1000000, rank_cards_weight = 10000
- the game ends with ONE ending whose `rank_by` is `you.out * 1000000 - you.cards_left * 10000 - you.picked_up`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
    "id": "three_up_even_rounds",
    "name": "Three Up: Even Rounds",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Three-player shedding game: play a rank at or above the Pile's top, play a Clear, or pick up; first to empty Hand and Up pile wins."
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
        "key": "up_choice",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "up_pile",
        "visible": "public",
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
        "key": "up_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "cards_left",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "picked_up",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "out",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "up_pick",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      }
    ],
    "game": [
      {
        "key": "low_stack",
        "visible": "none",
        "type": "list",
        "initial": ["1", "1", "1", "2", "2", "2", "3", "3", "3"]
      },
      {
        "key": "mid_stack",
        "visible": "none",
        "type": "list",
        "initial": ["4", "4", "4", "5", "5", "5", "6", "6", "6"]
      },
      {
        "key": "high_stack",
        "visible": "none",
        "type": "list",
        "initial": ["7", "7", "7", "8", "8", "8", "9", "9", "9"]
      },
      {
        "key": "clear_stack",
        "visible": "none",
        "type": "list",
        "initial": ["C", "C", "C"]
      },
      {
        "key": "pile",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "top_rank",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "run_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "removed",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "history",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "players_out",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "total_cards",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "lowest_rank",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "highest_rank",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "copies_per_rank",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "clear_cards",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "stack_size",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "low_ranks_max",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "mid_ranks_max",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "high_ranks_max",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "deal_per_stack",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "clear_per_player",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "cards_per_player",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "up_pile_size",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "hand_after_up",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "run_to_clear",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "max_rounds",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "rank_out_weight",
        "visible": "public",
        "type": "number",
        "initial": 1000000
      },
      {
        "key": "rank_cards_weight",
        "visible": "public",
        "type": "number",
        "initial": 10000
      },
      {
        "key": "play_options",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "ups_done",
        "visible": "none",
        "type": "bool",
        "initial": false
      },
      {
        "key": "act",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "kind",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "play_rs",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "play_k",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "from_hand",
        "visible": "none",
        "type": "bool",
        "initial": true
      },
      {
        "key": "taken",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "burn",
        "visible": "none",
        "type": "bool",
        "initial": false
      },
      {
        "key": "last_desc",
        "visible": "none",
        "type": "text",
        "initial": ""
      }
    ]
  },
  "setup": [
    {
      "use": "tell",
      "label": "the seating",
      "to": "all",
      "text": "Seats were assigned in a random order. Seat 1 is First, seat 2 is Second and seat 3 is Third; turn order is seat 1, 2, 3 in every round."
    },
    {
      "use": "update",
      "label": "the deal",
      "do": [
        {"set": {"key": "pick", "value": {"calc": "low_stack[int(uniform(0, len(low_stack)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "low_stack[int(uniform(0, len(low_stack)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "low_stack[int(uniform(0, len(low_stack)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[int(uniform(0, len(mid_stack)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[int(uniform(0, len(mid_stack)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[int(uniform(0, len(mid_stack)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[int(uniform(0, len(high_stack)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[int(uniform(0, len(high_stack)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[int(uniform(0, len(high_stack)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "low_stack[int(uniform(0, len(low_stack)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "low_stack[int(uniform(0, len(low_stack)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "low_stack[int(uniform(0, len(low_stack)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[int(uniform(0, len(mid_stack)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[int(uniform(0, len(mid_stack)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[int(uniform(0, len(mid_stack)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[int(uniform(0, len(high_stack)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[int(uniform(0, len(high_stack)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[int(uniform(0, len(high_stack)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "low_stack[int(uniform(0, len(low_stack)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "low_stack[int(uniform(0, len(low_stack)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "low_stack[int(uniform(0, len(low_stack)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[int(uniform(0, len(mid_stack)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[int(uniform(0, len(mid_stack)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[int(uniform(0, len(mid_stack)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[int(uniform(0, len(high_stack)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[int(uniform(0, len(high_stack)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[int(uniform(0, len(high_stack)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "clear_stack[0]"}}},
        {"remove": {"key": "clear_stack", "value": {"calc": "clear_stack[0]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "clear_stack[0]"}}},
        {"remove": {"key": "clear_stack", "value": {"calc": "clear_stack[0]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "clear_stack[0]"}}},
        {"remove": {"key": "clear_stack", "value": {"calc": "clear_stack[0]"}}},
        {"set": {"key": "pick", "value": ""}}
      ],
      "text": "Each player has been dealt {deal_per_stack} cards from Low, {deal_per_stack} from Mid, {deal_per_stack} from High and {clear_per_player} Clear: {cards_per_player} cards each."
    },
    {
      "use": "update",
      "label": "the table starts",
      "do": [
        {"set": {"key": "pile", "value": []}},
        {"set": {"key": "top_rank", "value": 0}},
        {"set": {"key": "run_count", "value": 0}},
        {"set": {"key": "removed", "value": []}},
        {"set": {"key": "round", "value": 0}},
        {"set": {"key": "players_out", "value": 0}},
        {"set": {"players": "all", "key": "picked_up", "value": 0}},
        {"set": {"players": "all", "key": "out", "value": false}},
        {"set": {"key": "play_options", "value": [
          "play 1 x rank 1", "play 2 x rank 1", "play 3 x rank 1",
          "play 1 x rank 2", "play 2 x rank 2", "play 3 x rank 2",
          "play 1 x rank 3", "play 2 x rank 3", "play 3 x rank 3",
          "play 1 x rank 4", "play 2 x rank 4", "play 3 x rank 4",
          "play 1 x rank 5", "play 2 x rank 5", "play 3 x rank 5",
          "play 1 x rank 6", "play 2 x rank 6", "play 3 x rank 6",
          "play 1 x rank 7", "play 2 x rank 7", "play 3 x rank 7",
          "play 1 x rank 8", "play 2 x rank 8", "play 3 x rank 8",
          "play 1 x rank 9", "play 2 x rank 9", "play 3 x rank 9"
        ]}}
      ]
    },
    {
      "use": "sync",
      "label": "your cards",
      "mode": "self",
      "to": "all",
      "text": "Your cards:"
    }
  ],
  "steps": [
    {
      "use": "repeat",
      "label": "choose the Up piles",
      "phase": "setup",
      "until": {
        "calc": "ups_done or all(len(p.up_choice) >= up_pile_size for p in players)"
      },
      "max": 3,
      "steps": [
        {
          "use": "update",
          "label": "clear the picks",
          "phase": "setup",
          "do": [
            {"set": {"players": "all", "key": "up_pick", "value": ""}}
          ]
        },
        {
          "use": "poll",
          "label": "up pile pick",
          "phase": "setup",
          "to": "all",
          "answer": {
            "type": "choice",
            "options": {
              "attribute": "hand"
            }
          },
          "store": "up_pick",
          "text": "Choose one card from your hand for your Up pile. All players choose at the same moment; you pick {up_pile_size} cards in all, one per question, and nobody sees the Up piles until all picks are made."
        },
        {
          "use": "update",
          "label": "the pick is set aside",
          "phase": "setup",
          "do": [
            {"remove": {"players": {"where": "you.up_pick != ''"}, "key": "hand", "value": {"calc": "you.up_pick"}}},
            {"append": {"players": {"where": "you.up_pick != ''"}, "key": "up_choice", "value": {"calc": "you.up_pick"}}}
          ]
        }
      ]
    },
    {
      "use": "update",
      "label": "the Up piles are revealed",
      "phase": "setup",
      "when": {
        "calc": "not ups_done"
      },
      "do": [
        {"set": {"players": "all", "key": "up_pile", "value": {"calc": "you.up_choice"}}},
        {"set": {"players": "all", "key": "up_choice", "value": []}},
        {"set": {"players": "all", "key": "up_pick", "value": ""}},
        {"set": {"players": "all", "key": "hand_count", "value": {"calc": "len(you.hand)"}}},
        {"set": {"players": "all", "key": "up_count", "value": {"calc": "len(you.up_pile)"}}},
        {"set": {"players": "all", "key": "cards_left", "value": {"calc": "you.hand_count + you.up_count"}}},
        {"set": {"players": "all", "key": "picked_up", "value": 0}},
        {"set": {"players": "all", "key": "out", "value": false}},
        {"set": {"key": "ups_done", "value": true}}
      ],
      "text": "Up piles revealed. Seat 1: {players[0].up_pile}. Seat 2: {players[1].up_pile}. Seat 3: {players[2].up_pile}. Each hand now holds {hand_after_up} cards."
    },
    {
      "use": "update",
      "label": "a new round",
      "phase": "talk",
      "do": [
        {"adjust": {"key": "round", "value": 1}},
        {"set": {"players": "all", "key": "offer", "value": {"calc": "['pick up'] + (['play Clear'] if 'C' in (you.hand if len(you.hand) > 0 else you.up_pile) else []) + [o for o in play_options if int(o[14]) >= top_rank and int(o[5]) <= count(c == o[14] for c in (you.hand if len(you.hand) > 0 else you.up_pile))]"}}}
      ],
      "text": "Round {round} (at most {max_rounds}). Pile: {pile}, top rank {top_rank}, run {run_count}. Up piles: seat 1 {players[0].up_pile}, seat 2 {players[1].up_pile}, seat 3 {players[2].up_pile}. Hand cards: seat 1 {players[0].hand_count}, seat 2 {players[1].hand_count}, seat 3 {players[2].hand_count}. Picked up: seat 1 {players[0].picked_up}, seat 2 {players[1].picked_up}, seat 3 {players[2].picked_up}."
    },
    {
      "use": "poll",
      "label": "talk",
      "phase": "talk",
      "to": "all",
      "answer": {
        "type": "text",
        "max_words": 30
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} says: {value}"
      },
      "text": "Say one short thing to the table. Everyone writes at the same moment and all messages are shown together. Nothing said binds anyone."
    },
    {
      "use": "sync",
      "label": "where you stand",
      "phase": "talk",
      "mode": "self",
      "to": "all",
      "text": "Your hand and the table:"
    },
    {
      "use": "ask",
      "label": "seat 1 turn",
      "phase": "turns",
      "to": {
        "where": "you.seat == 1 and not you.out"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "a1"
      },
      "text": "Your turn (First). Pile: {pile}, top rank {top_rank}, run {run_count}. You play from your Hand while it has cards, otherwise from your Up pile. Choose 'pick up', 'play Clear', or 'play K x rank R'."
    },
    {
      "use": "update",
      "label": "seat 1 resolves",
      "phase": "turns",
      "when": {
        "calc": "not players[0].out"
      },
      "do": [
        {"set": {"key": "act", "value": "$a1"}},
        {"set": {"key": "kind", "value": {"calc": "'clear' if (act == 'play Clear' and act in players[0].offer) else ('num' if (act in players[0].offer and act != 'pick up') else 'pick')"}}},
        {"set": {"key": "play_rs", "value": {"calc": "act[14] if kind == 'num' else ''"}}},
        {"set": {"key": "play_k", "value": {"calc": "int(act[5]) if kind == 'num' else 0"}}},
        {"set": {"key": "from_hand", "value": {"calc": "len(players[0].hand) > 0"}}},
        {"set": {"key": "taken", "value": {"calc": "len(pile) if kind == 'pick' else 0"}}},
        {"set": {"key": "last_desc", "value": {"calc": "'Seat 1: ' + ('picked up the pile' if kind == 'pick' else ('played a Clear' if kind == 'clear' else act))"}}},
        {"adjust": {"player": 1, "key": "picked_up", "value": {"calc": "taken"}, "if": {"calc": "kind == 'pick'"}}},
        {"set": {"player": 1, "key": "hand", "value": {"calc": "players[0].hand + pile"}, "if": {"calc": "kind == 'pick'"}}},
        {"set": {"key": "removed", "value": {"calc": "removed + pile + ['C']"}, "if": {"calc": "kind == 'clear'"}}},
        {"remove": {"player": 1, "key": "hand", "value": "C", "if": {"calc": "kind == 'clear' and from_hand"}}},
        {"remove": {"player": 1, "key": "up_pile", "value": "C", "if": {"calc": "kind == 'clear' and not from_hand"}}},
        {"remove": {"player": 1, "key": "hand", "value": {"calc": "play_rs"}, "if": {"calc": "kind == 'num' and from_hand and play_k >= 1"}}},
        {"remove": {"player": 1, "key": "hand", "value": {"calc": "play_rs"}, "if": {"calc": "kind == 'num' and from_hand and play_k >= 2"}}},
        {"remove": {"player": 1, "key": "hand", "value": {"calc": "play_rs"}, "if": {"calc": "kind == 'num' and from_hand and play_k >= 3"}}},
        {"remove": {"player": 1, "key": "up_pile", "value": {"calc": "play_rs"}, "if": {"calc": "kind == 'num' and not from_hand and play_k >= 1"}}},
        {"remove": {"player": 1, "key": "up_pile", "value": {"calc": "play_rs"}, "if": {"calc": "kind == 'num' and not from_hand and play_k >= 2"}}},
        {"remove": {"player": 1, "key": "up_pile", "value": {"calc": "play_rs"}, "if": {"calc": "kind == 'num' and not from_hand and play_k >= 3"}}},
        {"append": {"key": "pile", "value": {"calc": "play_rs"}, "if": {"calc": "kind == 'num' and play_k >= 1"}}},
        {"append": {"key": "pile", "value": {"calc": "play_rs"}, "if": {"calc": "kind == 'num' and play_k >= 2"}}},
        {"append": {"key": "pile", "value": {"calc": "play_rs"}, "if": {"calc": "kind == 'num' and play_k >= 3"}}},
        {"set": {"key": "run_count", "value": {"calc": "(run_count + play_k) if int(play_rs) == top_rank else play_k"}, "if": {"calc": "kind == 'num'"}}},
        {"set": {"key": "top_rank", "value": {"calc": "int(play_rs)"}, "if": {"calc": "kind == 'num'"}}},
        {"set": {"key": "burn", "value": {"calc": "kind == 'num' and run_count >= run_to_clear"}}},
        {"set": {"key": "removed", "value": {"calc": "removed + pile"}, "if": {"calc": "burn"}}},
        {"set": {"key": "last_desc", "value": {"calc": "last_desc + ', and the run clears the pile'"}, "if": {"calc": "burn"}}},
        {"set": {"key": "pile", "value": [], "if": {"calc": "kind != 'num' or burn"}}},
        {"set": {"key": "top_rank", "value": 0, "if": {"calc": "kind != 'num' or burn"}}},
        {"set": {"key": "run_count", "value": 0, "if": {"calc": "kind != 'num' or burn"}}},
        {"set": {"player": 1, "key": "hand_count", "value": {"calc": "len(players[0].hand)"}}},
        {"set": {"player": 1, "key": "up_co
... (cut)

Why it was refused: an option is offered and then refused (see the offer-only-what-is-allowed pattern): refused: seat 1 was offered 'C' in `up_pile_pick`, picked it, and was asked again without it (round 1): the first offer held an option that was not allowed. Offer each seat only what it may do, from its own state, instead of refusing afterwards | refused: seat 2 was offered 'C' in `up_pile_pick`, picked it, and was asked again without it (round 1): the first offer held an option that was not allowed. Offer each seat only what it may do, from its own state, instead of refusing afterwards
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "three_up_even_rounds",
    "name": "Three Up: Even Rounds",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Three-player shedding game: play a rank at or above the Pile's top, play a Clear, or pick up; first to empty Hand and Up pile wins."
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
        "key": "up_choice",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "up_pile",
        "visible": "public",
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
        "key": "up_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "cards_left",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "picked_up",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "out",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "up_pick",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      }
    ],
    "game": [
      {
        "key": "low_stack",
        "visible": "none",
        "type": "list",
        "initial": ["1", "1", "1", "2", "2", "2", "3", "3", "3"]
      },
      {
        "key": "mid_stack",
        "visible": "none",
        "type": "list",
        "initial": ["4", "4", "4", "5", "5", "5", "6", "6", "6"]
      },
      {
        "key": "high_stack",
        "visible": "none",
        "type": "list",
        "initial": ["7", "7", "7", "8", "8", "8", "9", "9", "9"]
      },
      {
        "key": "clear_stack",
        "visible": "none",
        "type": "list",
        "initial": ["C", "C", "C"]
      },
      {
        "key": "pile",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "top_rank",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "run_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "removed",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "history",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "players_out",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "total_cards",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "lowest_rank",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "highest_rank",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "copies_per_rank",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "clear_cards",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "stack_size",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "low_ranks_max",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "mid_ranks_max",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "high_ranks_max",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "deal_per_stack",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "clear_per_player",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "cards_per_player",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "up_pile_size",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "hand_after_up",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "run_to_clear",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "max_rounds",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "rank_out_weight",
        "visible": "public",
        "type": "number",
        "initial": 1000000
      },
      {
        "key": "rank_cards_weight",
        "visible": "public",
        "type": "number",
        "initial": 10000
      },
      {
        "key": "play_options",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "ups_done",
        "visible": "none",
        "type": "bool",
        "initial": false
      },
      {
        "key": "act",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "kind",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "play_rs",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "play_k",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "from_hand",
        "visible": "none",
        "type": "bool",
        "initial": true
      },
      {
        "key": "taken",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "burn",
        "visible": "none",
        "type": "bool",
        "initial": false
      },
      {
        "key": "last_desc",
        "visible": "none",
        "type": "text",
        "initial": ""
      }
    ]
  },
  "setup": [
    {
      "use": "tell",
      "label": "the seating",
      "to": "all",
      "text": "Seats were assigned in a random order. Seat 1 is First, seat 2 is Second and seat 3 is Third; turn order is seat 1, 2, 3 in every round."
    },
    {
      "use": "update",
      "label": "the deal",
      "do": [
        {"set": {"key": "pick", "value": {"calc": "low_stack[int(uniform(0, len(low_stack)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "low_stack[int(uniform(0, len(low_stack)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "low_stack[int(uniform(0, len(low_stack)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[int(uniform(0, len(mid_stack)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[int(uniform(0, len(mid_stack)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[int(uniform(0, len(mid_stack)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[int(uniform(0, len(high_stack)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[int(uniform(0, len(high_stack)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[int(uniform(0, len(high_stack)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "low_stack[int(uniform(0, len(low_stack)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "low_stack[int(uniform(0, len(low_stack)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "low_stack[int(uniform(0, len(low_stack)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[int(uniform(0, len(mid_stack)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[int(uniform(0, len(mid_stack)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[int(uniform(0, len(mid_stack)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[int(uniform(0, len(high_stack)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[int(uniform(0, len(high_stack)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[int(uniform(0, len(high_stack)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "low_stack[int(uniform(0, len(low_stack)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "low_stack[int(uniform(0, len(low_stack)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "low_stack[int(uniform(0, len(low_stack)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "low_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[int(uniform(0, len(mid_stack)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[int(uniform(0, len(mid_stack)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "mid_stack[int(uniform(0, len(mid_stack)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "mid_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[int(uniform(0, len(high_stack)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[int(uniform(0, len(high_stack)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "high_stack[int(uniform(0, len(high_stack)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "high_stack", "value": {"calc": "pick"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "clear_stack[0]"}}},
        {"remove": {"key": "clear_stack", "value": {"calc": "clear_stack[0]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "clear_stack[0]"}}},
        {"remove": {"key": "clear_stack", "value": {"calc": "clear_stack[0]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "clear_stack[0]"}}},
        {"remove": {"key": "clear_stack", "value": {"calc": "clear_stack[0]"}}},
        {"set": {"key": "pick", "value": ""}}
      ],
      "text": "Each player has been dealt {deal_per_stack} cards from Low, {deal_per_stack} from Mid, {deal_per_stack} from High and {clear_per_player} Clear: {cards_per_player} cards each."
    },
    {
      "use": "update",
      "label": "the table starts",
      "do": [
        {"set": {"key": "pile", "value": []}},
        {"set": {"key": "top_rank", "value": 0}},
        {"set": {"key": "run_count", "value": 0}},
        {"set": {"key": "removed", "value": []}},
        {"set": {"key": "round", "value": 0}},
        {"set": {"key": "players_out", "value": 0}},
        {"set": {"players": "all", "key": "picked_up", "value": 0}},
        {"set": {"players": "all", "key": "out", "value": false}},
        {"set": {"key": "play_options", "value": [
          "play 1 x rank 1", "play 2 x rank 1", "play 3 x rank 1",
          "play 1 x rank 2", "play 2 x rank 2", "play 3 x rank 2",
          "play 1 x rank 3", "play 2 x rank 3", "play 3 x rank 3",
          "play 1 x rank 4", "play 2 x rank 4", "play 3 x rank 4",
          "play 1 x rank 5", "play 2 x rank 5", "play 3 x rank 5",
          "play 1 x rank 6", "play 2 x rank 6", "play 3 x rank 6",
          "play 1 x rank 7", "play 2 x rank 7", "play 3 x rank 7",
          "play 1 x rank 8", "play 2 x rank 8", "play 3 x rank 8",
          "play 1 x rank 9", "play 2 x rank 9", "play 3 x rank 9"
        ]}}
      ]
    },
    {
      "use": "sync",
      "label": "your cards",
      "mode": "self",
      "to": "all",
      "text": "Your cards:"
    }
  ],
  "steps": [
    {
      "use": "poll",
      "label": "first up pile pick",
      "phase": "setup",
      "when": {
        "calc": "not ups_done"
      },
      "to": "all",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "store": "up_pick",
      "text": "Choose the first of {up_pile_size} cards from your hand for your Up pile. All players choose at the same moment, and nobody sees any Up pile until all picks are made."
    },
    {
      "use": "update",
      "label": "first pick set aside",
      "phase": "setup",
      "when": {
        "calc": "not ups_done"
      },
      "do": [
        {"remove": {"players": {"where": "you.up_pick != ''"}, "key": "hand", "value": {"calc": "you.up_pick"}}},
        {"append": {"players": {"where": "you.up_pick != ''"}, "key": "up_choice", "value": {"calc": "you.up_pick"}}},
        {"set": {"players": "all", "key": "up_pick", "value": ""}}
      ]
    },
    {
      "use": "poll",
      "label": "second up pile pick",
      "phase": "setup",
      "when": {
        "calc": "not ups_done"
      },
      "to": "all",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "store": "up_pick",
      "text": "Choose the second card from your hand for your Up pile. All players choose at the same moment."
    },
    {
      "use": "update",
      "label": "second pick set aside",
      "phase": "setup",
      "when": {
        "calc": "not ups_done"
      },
      "do": [
        {"remove": {"players": {"where": "you.up_pick != ''"}, "key": "hand", "value": {"calc": "you.up_pick"}}},
        {"append": {"players": {"where": "you.up_pick != ''"}, "key": "up_choice", "value": {"calc": "you.up_pick"}}},
        {"set": {"players": "all", "key": "up_pick", "value": ""}}
      ]
    },
    {
      "use": "poll",
      "label": "third up pile pick",
      "phase": "setup",
      "when": {
        "calc": "not ups_done"
      },
      "to": "all",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "store": "up_pick",
      "text": "Choose the third and last card from your hand for your Up pile. All players choose at the same moment; then all Up piles are revealed."
    },
    {
      "use": "update",
      "label": "the Up piles are revealed",
      "phase": "setup",
      "when": {
        "calc": "not ups_done"
      },
      "do": [
        {"remove": {"players": {"where": "you.up_pick != ''"}, "key": "hand", "value": {"calc": "you.up_pick"}}},
        {"append": {"players": {"where": "you.up_pick != ''"}, "key": "up_choice", "value": {"calc": "you.up_pick"}}},
        {"set": {"players": "all", "key": "up_pick", "value": ""}},
        {"set": {"players": "all", "key": "up_pile", "value": {"calc": "you.up_choice"}}},
        {"set": {"players": "all", "key": "up_choice", "value": []}},
        {"set": {"players": "all", "key": "hand_count", "value": {"calc": "len(you.hand)"}}},
        {"set": {"players": "all", "key": "up_count", "value": {"calc": "len(you.up_pile)"}}},
        {"set": {"players": "all", "key": "cards_left", "value": {"calc": "you.hand_count + you.up_count"}}},
        {"set": {"players": "all", "key": "picked_up", "value": 0}},
        {"set": {"players": "all", "key": "out", "value": false}},
        {"set": {"key": "ups_done", "value": true}}
      ],
      "text": "Up piles revealed. Seat 1: {players[0].up_pile}. Seat 2: {players[1].up_pile}. Seat 3: {players[2].up_pile}. Each hand now holds {hand_after_up} cards."
    },
    {
      "use": "update",
      "label": "a new round",
      "phase": "talk",
      "do": [
        {"adjust": {"key": "round", "value": 1}},
        {"set": {"players": "all", "key": "offer", "value": {"calc": "['pick up'] + (['play Clear'] if 'C' in (you.hand if len(you.hand) > 0 else you.up_pile) else []) + [o for o in play_options if int(o[14]) >= top_rank and int(o[5]) <= count(c == o[14] for c in (you.hand if len(you.hand) > 0 else you.up_pile))]"}}}
      ],
      "text": "Round {round} (at most {max_rounds}). Pile: {pile}, top rank {top_rank}, run {run_count}. Up piles: seat 1 {players[0].up_pile}, seat 2 {players[1].up_pile}, seat 3 {players[2].up_pile}. Hand cards: seat 1 {players[0].hand_count}, seat 2 {players[1].hand_count}, seat 3 {players[2].hand_count}. Picked up: seat 1 {players[0].picked_up}, seat 2 {players[1].picked_up}, seat 3 {players[2].picked_up}."
    },
    {
      "use": "poll",
      "label": "talk",
      "phase": "talk",
      "to": "all",
      "answer": {
        "type": "text",
        "max_words": 30
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} says: {value}"
      },
      "text": "Say one short thing to the table. Everyone writes at the same moment and all messages are shown together. Nothing said binds anyone."
    },
    {
      "use": "sync",
      "label": "where you stand",
      "phase": "talk",
      "mode": "self",
      "to": "all",
      "text": "Your hand and the table:"
    },
    {
      "use": "ask",
      "label": "seat 1 turn",
      "phase": "turns",
      "to": {
        "where": "you.seat == 1 and not you.out"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "a1"
      },
      "text": "Your turn (First). Pile: {pile}, top rank {top_rank}, run {run_count}. You play from your Hand while it has cards, otherwise from your Up pile. Choose 'pick up', 'play Clear', or 'play K x rank R'."
    },
    {
      "use": "update",
      "label": "seat 1 resolves",
      "phase": "turns",
      "when": {
        "calc": "not players[0].out"
      },
      "do": [
        {"set": {"key": "act", "value": "$a1"}},
        {"set": {"key": "kind", "value": {"calc": "'clear' if (act == 'play Clear' and act in players[0].offer) else ('num' if (act in players[0].offer and act != 'pick up') else 'pick')"}}},
        {"set": {"key": "play_rs", "value": {"calc": "act[14] if kind == 'num' else ''"}}},
        {"set": {"key": "play_k", "value": {"calc": "int(act[5]) if kind == 'num' else 0"}}},
        {"set": {"key": "from_hand", "value": {"calc": "len(players[0].hand) > 0"}}},
        {"set": {"key": "taken", "value": {"calc": "len(pile) if kind == 'pick' else 0"}}},
        {"set": {"key": "last_desc", "value": {"calc": "'Seat 1: ' + (('picked up ' + str(taken) + ' cards') if kind == 'pick' else ('played a Clear' if kind == 'clear' else act))"}}},
        {"adjust": {"player": 1, "key": "picked_up", "value": {"calc": "taken"}, "if": {"calc": "kind == 'pick'"}}},
        {"set": {"player": 1, "key": "hand", "value": {"calc": "players[0].hand + pile"}, "if": {"calc": "kind == 'pick'"}}},
        {"set": {"key": "removed", "value": {"calc": "removed + pile + ['C']"}, "if": {"calc": "kind == 'clear'"}}},
        {"remove": {"player": 1, "key": "hand", "value": "C", "if": {"calc": "kind == 'clear' and from_hand"}}},
        {"remove": {"player": 1, "key": "up_pile", "value": "C", "if": {"calc": "kind == 'clear' and not from_hand"}}},
        {"remove": {"player": 1, "key": "hand", "value": {"calc": "play_rs"}, "if": {"calc": "kind == 'num' and from_hand and play_k >= 1"}}},
        {"remove": {"player": 1, "key": "hand", "value": {"calc": "play_rs"}, "if": {"calc": "kind == 'num' and from_hand and play_k >= 2"}}},
        {"remove": {"player": 1, "key": "hand", "value": {"calc": "play_rs"}, "if": {"calc": "kind == 'num' and from_hand and play_k >= 3"}}},
        {"remove": {"player": 1, "key": "up_pile", "value": {"calc": "play_rs"}, "if": {"calc": "kind == 'num' and not from_hand and play_k >= 1"}}},
        {"remove": {"player": 1, "key": "up_pile", "value": {"calc": "play_rs"}, "if": {"calc": "kind == 'num' and not from_hand and play_k >= 2"}}},
        {"remove": {"player": 1, "key": "up_pile", "value": {"calc": "play_rs"}, "if": {"calc": "kind == 'num' and not from_hand and play_k >= 3"}}},
        {"append": {"key": "pile", "value": {"calc": "play_rs"}, "if": {"calc": "kind == 'num' and play_k >= 1"}}},
        {"append": {"key": "pile", "value": {"calc": "play_rs"}, "if": {"calc": "kind == 'num' and play_k >= 2"}}},
        {"append": {"key": "pile", "value": {"calc": "play_rs"}, "if": {"calc": "kind == 'num' and play_k >= 3"}}},
        {"set": {"key": "run_count", "value": {"calc": "(run_count + play_k) if int(play_rs) == top_rank else play_k"}, "if": {"calc": "kind == 'num'"}}},
        {"set": {"key": "top_rank", "value": {"calc": "int(play_rs)"}, "if": {"calc": "kind == 'num'"}}},
        {"set": {"key": "burn", "value": {"calc": "kind == 'num' and run_count >= run_to_clear"}}},
        {"set": {"key": "removed", "value": {"calc": "removed + pile"}, "if": {"calc": "burn"}}},
        {"set": {"key": "last_desc", "value": {"calc": "last_desc + ', and the run clears the pile'"}, "if": {"calc": "burn"}}},
        {"set": {"key": "pile", "value": [], "if": {"calc": "kind != 'num' or burn"}}},
        {"set": {"key": "top_rank", "value": 0, "if": {"calc": "kind != 'num' or burn"}}},
        {"set": {"key": "run_count", "value": 0, "if": {"calc": "kind != 'num' or burn"}}},
        {"set": {"player": 1, "key": "hand_count", "value": {"calc": "len(players[0].hand)"}}},
        {"set": {"player": 1, "key": "up_count", "value": {"calc": "len(players[0].up_pile)"}}},
        {"set": {"player": 1, "key": "cards_left", "value": {"calc": "players[0].hand_count + players[0].up_count"}}},
        {"set": {"player": 1, "key": "out", "value": {"calc": "players[0].cards_left == 0"}}},
        {"set_status": {"player": 1, "to": "out", "if": {"calc": "players[0].out"}, "text": "Seat {player} has no cards left and is out of cards."}},
        {"append": {"key": "history", "value": {"calc": "last_desc"}}},
        {"set": {"players": "all", "key": "offer", "value": {"calc": "['pick up'] + (['play Clear'] if 'C' in (you.hand if len(you.hand) > 0 else you.up_pile) else []) + [o for o in play_options if int(o[14]) >= top_rank and int(o[5]) <= count(c == o[14] for c in (you.hand if len(you.hand) > 0 else you.up_pile))]"}}}
      ],
      "text": "{last_desc}. Pile now: {pile}, top rank {top_rank}, run {run_count}."
    },
    {
      "use": "ask",
      "label": "seat 2 turn",
      "phase": "turns",
      "to": {
        "where": "you.seat == 2 and not you.out"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "a2"
      },
      "text": "Your turn (Second). Pile: {pile}, top rank {top_rank}, run {run_count}. You play from your Hand while it has cards, otherwise from your Up pile. Choose 'pick up', 'play Clear', or 'play K x rank R'."
    },
    {
      "use": "update",
      "label": "seat 2 resolves",
      "phase": "turns",
      "when": {
        "calc": "not players[1].out"
      },
      "do": [
        {"set": {"key": "act", "value": "$a2"}},
        {"set": {"key": "kind", "value": {"calc": "'clear' if (act == 'play Clear' and act in players[1].offer) else ('num' if (act in players[1].offer and act != 'pick up') else 'pick')"}}},
        {"set": {"key": "play_rs", "value": {"calc": "act[14] if kind == 'num' else ''"}}},
        {"set": {"key": "play_k", "value": {"calc": "int(act[5]) if kind == 'num' else 0"}}},
        {"set": {"key": "from_hand", "value": {"calc": "len(players[1].hand) > 0"}}},
        {"set": {"key": "taken", "value": {"calc": "len(pile) if kind == 'pick' else 0"}}},
        {"set": {"key": "last_desc", "value": {"calc": "'Seat 2: ' + (('picked up ' + str(taken) + ' cards') if kind == 'pick' else ('played a Clear' if kind == 'clear' else act))"}}},
        {"adjust": {"player": 2, "key": "picked_up", "value": {"calc": "taken"}, "if": {"calc": "kind == 'pick'"}}},
        {"set": {"player": 2, "key": "hand", "value": {"calc": "players[1].hand + pile"}, "if": {"calc": "kind == 'pick'"}}},
        {"set": {"key": "removed", "value": {"calc": "removed + pile + ['C']"}, "if": {"calc": "kind == 'clear'"}}},
        {"remove": {"player": 2, "key": "hand", "value": "C", "if": {"calc": "kind == 'clear' and from_hand"}}},
        {"remove": {"player": 2, "key": "up_pile", "value": "C", "if": {"calc": "kind == 'clear' and not from_hand"}}},
        {"remove": {"player": 2, "key": "hand", "value": {"calc": "play_rs"}, "if": {"calc": "kind == 'num' and from_hand and play_k >= 1"}}},
        {"remove": {"player": 2, "key": "hand", "value": {"calc": "play_rs"}, "if": {"calc": "kind == 'num' and from_hand and play_k >= 2"}}},
        {"remove": {"player": 2, "key": "hand", "value": {"calc": "play_rs"}, "if": {"calc": "kind == 'num' and from_hand and play_k >= 3"}}},
        {"remove": {"player": 2, "key": "up_pile", "value": {"calc": "play_rs"}, "if": {"calc": "kind == 'num' and not from_hand and play_k >= 1"}}},
        {"remove": {"player": 2, "key": "up_pile", "value": {"calc": "play_rs"}, "if": {"calc": "kind == 'num' and not from_hand and play_k >= 2"}}},
        {"remove": {"player": 2, "key": "up_pile", "value": {"calc": "play_rs"}, "if": {"calc": "kind == 'num' and not from_hand and play_k >= 3"}}},
        {"append": {"key": "pile", "value": {"calc": "play_rs"}, "if": {"calc": "kind == 'num' and play_k >= 1"}}},
        {"append": {"key": "pile", "value": {"calc": "play_rs"}, "if": {"calc": "kind == 'num' and play_k >= 2"}}},
        {"append": {"key": "pile", "value": {"calc": "play_rs"}, "if": {"calc": "kind == 'num' and play_k >= 3"}}},
        {"set": {"key": "run_count", "value": {"calc": "(run_count + play_k) if int(play_rs) == top_rank else play_k"}, "if": {"calc": "kind == 'num'"}}},
        {"set": {"key": "top_rank", "value": {"calc": "int(play_rs)"}, "if": {"calc": "kind == 'num'"}}},
        {"set": {"key": "burn", "value": {"calc": "kind == 'num' and run_count >= run_to_clear"}}},
        {"set": {"key": "removed", "value": {"calc": "removed + pile"}, "if": {"calc": "burn"}}},
        {"set": {"key": "last_desc", "value": {"calc": "last_desc + ', and the run clears the pile'"}, "if": {"calc": "burn"}}},
        {"set": {"key": "pile", "value": [], "if": {"calc": "kind != 'num' or burn"}}},
        {"set": {"key": "top_rank", "value": 0, "if": {"calc": "kind != 'num' or burn"}}},
        {"set": {"key": "run_count", "value": 0, "if": {"calc": "kind != 'num' or burn"}}},
        {"set": {"player": 2, "key": "hand_count", "value": {"calc": "len(players[1].hand)"}}},
        {"set": {"player": 2, "key": "up_count", "value": {"calc": "len(players[1].up_pile)"}}},
        {"set": {"player": 2, "key": "cards_left", "value": {"calc": "players[1].hand_count + players[1].up_count"}}},
        {"set": {"player": 2, "key": "out", "value": {"calc": "players[1].cards_left == 0"}}},
        {"set_status": {"player": 2, "to": "out", "if": {"calc": "players[1].out"}, "text": "Seat {player} has no cards left and is out of cards."}},
        {"append": {"key": "history", "value": {"calc": "last_desc"}}},
        {"set": {"players": "all", "key": "offer", "value": {"calc": "['pick up'] + (['play Clear'] if 'C' in (you.hand if len(you.hand) > 0 else you.up_pile) else []) + [o for o in play_options if int(o[14]) >= top_rank and int(o[5]) <= count(c == o[14] for c in (you.hand if len(you.hand) > 0 else you.up_pile))]"}}}
      ],
      "text": "{last_desc}. Pile now: {pile}, top rank {top_rank}, run {run_count}."
    },
    {
      "use": "ask",
      "label": "seat 3 turn",
      "phase": "turns",
      "to": {
        "where": "you.seat == 3 and not you.out"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "a3"
      },
      "text": "Your turn (Third). Pile: {pile}, top rank {top_rank}, run {run_count}. You play from your Hand while it has cards, otherwise from your Up pile. Choose 'pick up', 'play Clear', or 'play K x rank R'."
    },
    {
      "use": "update",
      "label": "seat 3 resolves",
      "phase": "turns",
      "when": {
        "calc": "not players[2].out"
      },
      "do": [
        {"set": {"key": "act", "value": "$a3"}},
        {"set": {"key": "kind", "value": {"calc": "'clear' if (act == 'play Clear' and act in players[2].offer) else ('num' if (act in players[2].offer and act != 'pick up') else 'pick')"}}},
        {"set": {"key": "play_rs", "value": {"calc": "act[14] if kind == 'num' else ''"}}},
        {"set": {"key": "play_k", "value": {"calc": "int(act[5]) if kind == 'num' else 0"}}},
        {"set": {"key": "from_hand", "value": {"calc": "len(players[2].hand) > 0"}}},
        {"set": {"key": "taken", "value": {"calc": "len(pile) if kind == 'pick' else 0"}}},
        {"set": {"key": "last_desc", "value": {"calc": "'Seat 3: ' + (('picked up ' + str(taken) + ' cards') if kind == 'pick' else ('played a Clear' if kind == 'clear' else act))"}}},
        {"adjust": {"player": 3, "key": "picked_up", "value": {"calc": "taken"}, "if": {"calc": "kind == 'pick'"}}},
        {"set": {"player": 3, "key": "hand", "value": {"calc": "players[2].hand + pile"}, "if": {"calc": "kind == 'pick'"}}},
        {"set": {"key": "removed", "value": {"calc": "removed + pile + ['C']"}, "if": {"calc": "kind == 'clear'"}}},
        {"remove": {"player": 3, "key": "hand", "value": "C", "if": {"calc": "kind == 'clear' and from_hand"}}},
        {"remove": {"player": 3, "key": "up_pile", "value": "C", "if": {"calc": "kind == 'clear' and not from_hand"}}},
        {"remove": {"player": 3, "key": "hand", "value": {"calc": "play_rs"}, "if": {"calc": "kind == 'num' and from_hand and play_k >= 1"}}},
        {"remove": {"player": 3, "key": "hand", "value": {"calc": "play_rs"}, "if": {"calc": "kind == 'num' and from_hand and play_k >= 2"}}},
        {"remove": {"player": 3, "key": "hand", "value": {"calc": "play_rs"}, "if": {"calc": "kind == 'num' and from_hand and play_k >= 3"}}},
        {"remove": {"player": 3, "key": "up_pile", "value": {"calc": "play_rs"}, "if": {"calc": "kind == 'num' and not from_hand and play_k >= 1"}}},
        {"remove": {"player": 3, "key": "up_pile", "value": {"calc": "play_rs"}, "if": {"calc": "kind == 'num' and not from_hand and play_k >= 2"}}},
        {"remove": {"player": 3, "key": "up_pile", "value": {"calc": "play_rs"}, "if": {"calc": "kind == 'num' and not from_hand and play_k >= 3"}}},
        {"append": {"key": "pile", "value": {"calc": "play_rs"}, "if": {"calc": "kind == 'num' and play_k >= 1"}}},
        {"append": {"key": "pile", "value": {"calc": "play_rs"}, "if": {"calc": "kind == 'num' and play_k >= 2"}}},
        {"append": {"key": "pile", "value": {"calc": "play_rs"}, "if": {"calc": "kind == 'num' and play_k >= 3"}}},
        {"set": {"key": "run_count", "value": {"calc": "(run_count + play_k) if int(play_rs) == top_rank else play_k"}, "if": {"calc": "kind == 'num'"}}},
        {"set": {"key": "top_rank", "value": {"calc": "int(play_rs)"}, "if": {"calc": "kind == 'num'"}}},
        {"set": {"key": "burn", "value": {"calc": "kind == 'num' and run_count >= run_to_clear"}}},
        {"set": {"key": "removed", "value": {"calc": "removed + pile"}, "if": {"calc": "burn"}}},
        {"set": {"key": "last_desc", "value": {"calc": "last_desc + ', and the run clears the pile'"}, "if": {"calc": "burn"}}},
        {"set": {"key": "pile", "value": [], "if": {"calc": "kind != 'num' or burn"}}},
        {"set": {"key": "top_rank", "value": 0, "if": {"calc": "kind != 'num' or burn"}}},
        {"set": {"key": "run_count", "value": 0, "if": {"calc": "kind != 'num' or burn"}}},
        {"set": {"player": 3, "key": "hand_count", "value": {"calc": "len(players[2].hand)"}}},
        {"set": {"player": 3, "key": "up_count", "value": {"calc": "len(players[2].up_pile)"}}},
        {"set": {"player": 3, "key": "cards_left", "value": {"calc": "players[2].hand_count + players[2].up_count"}}},
        {"set": {"player": 3, "key": "out", "value": {"calc": "players[2].cards_left == 0"}}},
        {"set_status": {"player": 3, "to": "out", "if": {"calc": "players[2].out"}, "text": "Seat {player} has no cards left and is out of cards."}},
        {"append": {"key": "history", "value": {"calc": "last_desc"}}}
      ],
      "text": "{last_desc}. Pile now: {pile}, top rank {top_rank}, run {run_count}."
    },
    {
      "use": "update",
      "label": "count who is out",
      "phase": "end",
      "do": [
        {"set": {"key": "players_out", "value": {"calc": "count(p.out for p in players)"}}}
      ]
    },
    {
      "use": "check",
      "label": "end of round",
      "phase": "end",
      "when": {
        "calc": "players_out >= 1 or round >= max_rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "players_out >= 1 or round >= max_rounds"
      },
      "rank_by": "you.out * 1000000 - you.cards_left * 10000 - you.picked_up",
      "text": "Winner: {result}. Cards left: Seat 1 {players[0].cards_left}, Seat 2 {players[1].cards_left}, Seat 3 {players[2].cards_left}; picked up: Seat 1 {players[0].picked_up}, Seat 2 {players[1].picked_up}, Seat 3 {players[2].picked_up}."
    }
  },
  "limits": {
    "rounds": 40,
    "rounds_max": 40,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "CARDS. There are {total_cards} cards: {copies_per_rank} copies each of ranks {lowest_rank} to {highest_rank} and {clear_cards} Clear cards (written C).\n\nSETUP. Seats are assigned in a random order: seat 1 is First, seat 2 is Second, seat 3 is Third, and turn order is First, Second, Third in every round. Three stacks are shuffled separately: Low (ranks 1-{low_ranks_max}), Mid (ranks 4-{mid_ranks_max}) and High (ranks 7-{high_ranks_max}), {stack_size} cards each. Each player is dealt {deal_per_stack} cards from Low, {deal_per_stack} from Mid, {deal_per_stack} from High and {clear_per_player} Clear: {cards_per_player} cards each, and every card is dealt. Each player privately looks at their cards. Then, at the same moment, each player chooses exactly {up_pile_size} of their cards to be their Up pile (one card per question, three questions, all players answering together); all Up piles are then revealed. The remaining {hand_after_up} cards are your Hand, which only you see. The Pile starts empty with a run count of 0, and everyone's picked-up count starts at 0.\n\nPUBLIC INFORMATION. Everyone always sees every card on the Pile, its top rank and run count (how many cards of the top rank lie on top of the Pile in a row), every Up pile, each player's number of Hand cards, each player's picked-up count, and the full history of plays and pickups.\n\nEACH ROUND (at most {max_rounds} rounds). (a) TALK: every player writes one short message at the same moment without seeing the others; all messages are then shown to everyone. Messages bind no one. (b) TURNS: First, then Second, then Third each take one turn. A player who already has no cards in Hand or Up pile skips their turn. (c) END CHECK after Third's turn: if exactly one player is out of cards, that player wins. If two or three are out of cards, the one among them with the lowest picked-up count wins; if they are tied on that count, it is a draw between them. If nobody is out of cards, play continues. A player who empties mid-round does not end the round early: the round continues to Third first. (d) ROUND CAP: if round {max_rounds} ends with nobody out of cards, the player with the fewest cards (Hand plus Up pile) wins; a tie for fewest is broken by the lowest picked-up count; if still tied, it is a draw.\n\nA TURN. Choose one of two actions. PLAY: choose one rank and play one or more cards of that rank together, all from the same source. The source must be your Hand while your Hand has any cards; you play from your Up pile only once your Hand is empty. A numbered play is legal only if the Pile is empty or the rank is equal to or higher than the Pile's top rank (on top rank 5, a 5 or a 9 is legal, a 4 is not). A Clear is always legal and is played on its own. PICK UP: take every card on the Pile into your Hand and add the number of cards taken to your picked-up count; the Pile becomes empty with a run count of 0. You may pick up even when you have a legal play. Picking up an empty Pile does nothing. You are offered only legal choices: 'pick up', 'play Clear' if your source holds a C, and 'play K x rank R' for each legal rank R in your source and each K up to the number of R cards you hold there. An illegal or unreadable choice counts as PICK UP.\n\nRESOLVING A PLAY. Numbered cards go on top of the Pile. If their rank equals the previous top rank, the run count rises by the number of cards played; otherwise the run count becomes the number of cards played and that rank becomes the top rank. If the run count reaches {run_to_clear} or more, the Pile is cleared: its cards are removed from the game, it becomes empty, and the run count is 0. If it stays below {run_to_clear}, the cards stay on the Pile. A played Clear and the whole Pile are removed from the game, leaving the Pile empty. The turn then ends, and the next player acts on whatever Pile remains. An empty Pile accepts any card.\n\nWINNING. At the end of each round, if exactly one player has no cards left in Hand or Up pile, that player wins. If several players emptied by the end of the same round, the one with the lowest total of cards picked up during the game wins; if they are tied on that total, the game is a draw. If round {max_rounds} ends with nobody out of cards, the player with the fewest remaining cards wins, ties are broken by the lowest picked-up total, and a remaining tie is a draw."
}
```
````
