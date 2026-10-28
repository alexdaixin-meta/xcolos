# 42 coder

- time: 2026-10-28T06:47:13+00:00 (167.2s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 ac0d82419e1b6f1f, reply sha256 e67cdc1459cf3ab7

## Sent

````
# Task: write the XColos game file for "Row Yaniv"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 4; set `meta.players` to {"min": 2, "max": 4, "suggested": 3} (the suggested size is the one the game plays best at).

DECK: 54 cards, used only for their values: two Jokers worth 0; four each of values 1 to 9 (Ace = 1); sixteen cards worth 10 (the 10s, Jacks, Queens and Kings). Only values matter; suits are ignored.

STATE: Each player has three private slots c1, c2 and c3. Each slot holds one card value or is empty. A player's hand total H is the sum of their non-empty slots. Each player has a public penalty total, starting at 0.
Public table state:
- the round number (1 to 24);
- the priority seat (seat 1 in round 1);
- a 'new hand' flag (on at the start);
- the draw pile, whose order is hidden and whose size is public;
- the OFFER ROW, an ordered public list of cards;
- the DEAD PILE, a public list of every card that has left play this hand.

EACH ROUND:
1. NEW HAND. If the 'new hand' flag is on: shuffle all 54 cards to form the draw pile. This is the only random event in any round. Empty all slots, empty the dead pile, and deal 3 cards from the top of the draw pile to each player in seat order, into c1, c2 and c3, told privately. Then turn the next card face up as the offer row (one card at position 1). Switch the flag off.
2. ANNOUNCE the offer row with its positions and values, the dead pile, the draw pile size, the priority seat, and each player's number of cards.
3. CHOICES. All players answer at the same moment, privately, three things:
   (a) action: YANIV, DRAW, or TAKE;
   (b) take position: a number from 1 to the length of the offer row (used only for TAKE);
   (c) shed slot: 1, 2 or 3. It must be a non-empty slot; if it is not, the lowest-numbered non-empty slot is used.
4. YANIV CHECK. A YANIV is valid only if the player's H is 10 or less. An invalid YANIV is announced as invalid, and that player is treated as DRAW for the rest of the round.
5. If at least one valid YANIV was made, no cards move this round. Go to step 10.
6. SHED. Each player removes the card in their shed slot. Every other slot of theirs holding the same value is also removed, so a pair sheds two cards and a triple sheds three. Those extra slots stay empty for the rest of the hand. Announce every player's shed card values.
7. TAKE. Go through the TAKE players in seat order, starting at the priority seat and wrapping around. Each one receives the offer-row card at their take position if no earlier player has claimed it, and places it in their shed slot. Announce who took which card. A TAKE player whose card was already claimed becomes DRAW.
8. DRAW. In the same order (from the priority seat), each DRAW player takes the top card of the draw pile into their shed slot, told privately. The drawn value is never announced.
9. ROW UPDATE. All offer-row cards not taken go to the dead pile. The new offer row is every card shed in step 6, listed in seat order from seat 1, and within a player in the order of their slots. Announce each player's card count and the draw pile size.
10. SHOWDOWN. A showdown happens in any of three cases:
   - a valid YANIV was made this round;
   - after step 9 the draw pile holds fewer cards than there are players;
   - this is round 24.
   All hands are revealed.
   If there were valid callers: let M be the lowest H among the callers, and N the lowest H among the non-callers (N = 99 if everyone called).
   - A caller scores 0 if their H equals M and M is less than N. Otherwise they score H + 20 (Asaf).
   - A non-caller scores 0 if their H is less than or equal to M. Otherwise they score H.
   With no valid caller: every player with the lowest H scores 0, and the others score their H.
   Add the scores to the penalty totals and announce all totals. Then switch the 'new hand' flag on, so the next round begins a fresh hand and a fresh shuffle.
11. The priority seat passes to the next seat in order.
12. END CHECK. The match ends after any showdown that leaves some player's penalty total at 50 or more, or after round 24.

There is no discussion phase.

How the winner is decided: When the match ends, the player with the lowest penalty total wins. If two or more players share the lowest total, the match is a draw among them.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Row Yaniv (2 to 4 players, best with 3)

A simultaneous-choice take on Yaniv: each round every player secretly chooses to call YANIV, draw blind or take from a public offer row, and sheds a card (with any matches). The lowest hand at showdown avoids penalty, and the lowest penalty total wins.

STATE (every item below must exist in the file):
  - each player: c1 (number, starts -1); only its owner sees it. Card value in slot 1 (0-10), or -1 if empty
  - each player: c2 (number, starts -1); only its owner sees it. Card value in slot 2 (0-10), or -1 if empty
  - each player: c3 (number, starts -1); only its owner sees it. Card value in slot 3 (0-10), or -1 if empty
  - each player: hand_total (number, starts 0); only its owner sees it. H: the sum of the non-empty slots
  - each player: card_count (number, starts 0); everyone sees it. Number of non-empty slots
  - each player: penalty (number, starts 0); everyone sees it. Penalty total (the score; lower is better)
  - each player: action (text, starts ''); only its owner sees it. This round's action (YANIV, DRAW or TAKE) after invalid-YANIV and lost-TAKE conversions
  - each player: take_pos (number, starts 1); only its owner sees it. Chosen offer-row position, used only for TAKE
  - each player: shed_slot (number, starts 1); only its owner sees it. Effective shed slot (1-3), corrected to the lowest non-empty slot if the chosen one is empty
  - each player: is_caller (bool, starts False); everyone sees it. Made a valid YANIV this round
  - each player: shed_values (list, starts []); everyone sees it. Card values shed this round, in slot order
  - each player: last_hand_total (number, starts 0); everyone sees it. H revealed at the most recent showdown
  - the table: round (number, starts 1); everyone sees it. Round number, 1 to 24
  - the table: priority_seat (number, starts 1); everyone sees it. Seat that resolves first in TAKE and DRAW
  - the table: new_hand (bool, starts True); everyone sees it. When true, a fresh hand is shuffled and dealt at the start of the round
  - the table: draw_pile (list, starts []); hidden from all players. Card values in the draw pile; its order is hidden
  - the table: draw_pile_size (number, starts 0); everyone sees it. Number of cards in the draw pile
  - the table: offer_row (list, starts []); everyone sees it. Ordered public offer row of card values
  - the table: dead_pile (list, starts []); everyone sees it. Every card that has left play this hand
  - the table: claimed (list, starts []); everyone sees it. Offer-row positions already taken this round
  - the table: any_valid_yaniv (bool, starts False); everyone sees it. At least one valid YANIV was made this round
  - the table: showdown (bool, starts False); everyone sees it. A showdown happens this round
  - the table: min_caller_h (number, starts 99); everyone sees it. M: the lowest H among valid callers
  - the table: min_noncaller_h (number, starts 99); everyone sees it. N: the lowest H among non-callers (99 if everyone called)
  - the table: min_h (number, starts 99); everyone sees it. The lowest H overall, used when there is no valid caller
  - the table: max_penalty (number, starts 0); everyone sees it. The highest penalty total, kept beside the scores for the end check
  - parameters, each kept as a table attribute: deck_size = 54, joker_count = 2, joker_value = 0, copies_per_value_1_to_9 = 4, ten_value_cards = 16, ten_value = 10, slots_per_player = 3, cards_dealt_per_player = 3, initial_offer_row_length = 1, max_rounds = 24, yaniv_threshold = 10, asaf_penalty = 20, no_noncaller_n = 99, end_penalty = 50, initial_penalty = 0, empty_slot_code = -1

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Every player's penalty is set to 0 and all slots c1, c2 and c3 are set to -1 (empty).
  2. round = 1, priority_seat = 1, new_hand = true, and offer_row and dead_pile are empty.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: When new_hand is true: draw_pile is set to the full 54-card list [0,0, four each of 1-9, sixteen 10s]; all slots are set to -1; dead_pile is emptied; in seat order, each player draws 3 cards at random from draw_pile into c1, c2 and c3 (removed from draw_pile); one more random card from draw_pile becomes offer_row = [that card]; new_hand = false. Then hand_total, card_count and draw_pile_size are recomputed.
  2. [sync] all players. What happens: Each player privately sees their own c1, c2, c3 and hand_total.
  3. [tell] all players. What happens: Announce offer_row with positions and values, dead_pile, draw_pile_size, priority_seat and every player's card_count.
  4. [update] all players. What happens: Reset for the round: is_caller = false, shed_values = [], claimed = [], any_valid_yaniv = false, showdown = false.
  5. [poll] all players answers: one of YANIV, DRAW, TAKE. What happens: Stored privately in action; no answer is shown until all are in.
  6. [poll] all players answers: a whole number from 1 to the length of offer_row. What happens: Stored privately in take_pos (used only for TAKE).
  7. [poll] all players answers: one of 1, 2, 3. What happens: Stored in shed_slot; if that slot is -1, shed_slot is set to the lowest-numbered non-empty slot.
  8. [update] all players. What happens: YANIV check: for each player with action = YANIV, if hand_total <= 10 then is_caller = true, otherwise action = DRAW and the YANIV is announced as invalid. any_valid_yaniv = (count of is_caller > 0).
  9. [update] all players. What happens: SHED, when any_valid_yaniv is false: each player appends the value in their shed slot to shed_values, then for each of their other slots, in slot order, holding that same value, appends it and sets that slot to -1. The shed slot is set to -1. Every player's shed_values is announced.
  10. [update] each player in turn, starting at priority_seat and wrapping. What happens: TAKE, when any_valid_yaniv is false: for each player with action = TAKE in that order, if take_pos is not in claimed, the shed slot is set to offer_row[take_pos], take_pos is appended to claimed, and the take is announced; otherwise action = DRAW.
  11. [update] each player in turn, starting at priority_seat and wrapping. What happens: DRAW, when any_valid_yaniv is false: for each player with action = DRAW in that order, one random card is removed from draw_pile and placed in the shed slot, told only to that player; draw_pile_size decreases by 1.
  12. [update] all players. What happens: ROW UPDATE, when any_valid_yaniv is false: offer_row cards at positions not in claimed are appended to dead_pile; offer_row = the concatenation of shed_values from seat 1 upward. hand_total and card_count are recomputed, and every card_count and draw_pile_size is announced.
  13. [sync] all players. What happens: Each player privately sees their updated slots and hand_total.
  14. [update] all players. What happens: showdown = any_valid_yaniv OR draw_pile_size < number of players OR round = 24. When showdown is true: last_hand_total = hand_total for every player (all hands revealed); min_caller_h = the lowest hand_total among is_caller players (99 if none); min_noncaller_h = the lowest among the others (99 if none); min_h = the lowest hand_total overall.
  15. [update] all players. What happens: SCORING, when showdown is true. With any_valid_yaniv: a caller adds 0 if hand_total = min_caller_h and min_caller_h < min_noncaller_h, otherwise adds hand_total + 20; a non-caller adds 0 if hand_total <= min_caller_h, otherwise adds hand_total. Without any_valid_yaniv: a player adds 0 if hand_total = min_h, otherwise adds hand_total. Then max_penalty = the highest penalty, new_hand = true, and all hands and penalty totals are announced.
  16. [update] all players. What happens: priority_seat = (priority_seat mod number of players) + 1; round increases by 1.
  17. [check] all players. What happens: End the game if (showdown is true and max_penalty >= 50) or round > 24; otherwise continue.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When a new hand starts, the draw pile is the 54 values (two 0s, four each of 1-9, sixteen 10s), each player receives 3 random cards into c1, c2 and c3, and 1 more card becomes the offer row, leaving 54 - 3*players - 1 cards in the draw pile.
  R2. When a new hand starts, the dead pile is emptied and the new-hand flag is switched off.
  R3. A player's hand total H is the sum of their non-empty slots (an empty slot counts as nothing).
  R4. When a player calls YANIV with H <= 10, the call is valid; with H = 11 or more it is announced as invalid and the player is treated as DRAW.
  R5. When at least one valid YANIV is made, no card moves that round and a showdown follows.
  R6. When a player sheds, the card in their shed slot and every other slot of theirs with the same value are removed, so a pair sheds 2 cards and a triple sheds 3.
  R7. When the chosen shed slot is empty, the lowest-numbered non-empty slot is shed instead.
  R8. When two TAKE players choose the same position, the one earlier in seat order from the priority seat gets the card, and the other becomes DRAW.
  R9. A taken or drawn card is placed in the player's shed slot; extra slots emptied by a pair or triple stay empty for the rest of the hand.
  R10. A drawn card's value is told only to the drawing player, and the draw pile size drops by 1 per draw.
  R11. After the take step, untaken offer-row cards go to the dead pile, and the new offer row is all shed cards in seat order from seat 1, in slot order within each player.
  R12. A showdown happens when a valid YANIV was made, when the draw pile holds fewer cards than there are players after the row update, or in round 24.
  R13. With valid callers, a caller whose H equals M (the lowest caller H) scores 0 when M < N (the lowest non-caller H, or 99 if all called); otherwise the caller scores H + 20.
  R14. With valid callers, a non-caller scores 0 when their H <= M; otherwise they score H.
  R15. In a showdown with no valid caller, every player with the lowest H scores 0 and the others score their H.
  R16. After every showdown, scores are added to penalty totals, all hands are revealed, and the next round starts a fresh hand.
  R17. Every round the priority seat moves to the next seat, wrapping from the last seat to seat 1.
  R18. The match ends after a showdown that leaves some penalty total at 50 or more, or after round 24.
  R19. The player with the lowest penalty total wins, and players tied for the lowest share the win.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - action | asked: all players | options: YANIV, DRAW, TAKE (the offer row always holds at least one card)
  - take position | asked: all players | options: a whole number from 1 to the current length of offer_row
  - shed slot | asked: all players | options: 1, 2, 3 (an empty slot is replaced by the lowest non-empty slot, as the rules allow)

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: (showdown == true and max_penalty >= 50) or round > 24
  - each player's standing: 0 - you.penalty (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their penalty total; the lowest penalty wins, and players tied for the lowest share the win (a draw among them).
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

- each player: `card_count` (number, visible: public, starts 0): Number of non-empty slots
- each player: `penalty` (number, visible: public, starts 0): Penalty total (the score; lower is better)
- each player: `last_hand_total` (number, visible: public, starts 0): H revealed at the most recent showdown
- the table: `round` (number, visible: public, starts 1): Round number, 1 to 24
- the table: `draw_pile_size` (number, visible: public, starts 0): Number of cards in the draw pile
- the table: `offer_row` (list, visible: public, starts []): Ordered public offer row of card values
- the table: `dead_pile` (list, visible: public, starts []): Every card that has left play this hand
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 54, joker_count = 2, joker_value = 0, copies_per_value_1_to_9 = 4, ten_value_cards = 16, ten_value = 10, slots_per_player = 3, cards_dealt_per_player = 3, initial_offer_row_length = 1, max_rounds = 24, yaniv_threshold = 10, asaf_penalty = 20, no_noncaller_n = 99, end_penalty = 50, initial_penalty = 0, empty_slot_code = -1
- the game ends with ONE ending whose `rank_by` is `0 - you.penalty`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
    "id": "row_yaniv",
    "name": "Row Yaniv",
    "players": {
      "min": 2,
      "max": 4,
      "suggested": 3
    },
    "blurb": "Simultaneous Yaniv: each round secretly call YANIV, draw blind or take from a public offer row, and shed a card with its matches. Lowest penalty wins."
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
        "key": "c1",
        "visible": "ally",
        "type": "number",
        "initial": -1
      },
      {
        "key": "c2",
        "visible": "ally",
        "type": "number",
        "initial": -1
      },
      {
        "key": "c3",
        "visible": "ally",
        "type": "number",
        "initial": -1
      },
      {
        "key": "hand_total",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "card_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "penalty",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "action",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "take_pos",
        "visible": "ally",
        "type": "number",
        "initial": 1
      },
      {
        "key": "shed_slot",
        "visible": "ally",
        "type": "number",
        "initial": 1
      },
      {
        "key": "is_caller",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "shed_values",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "last_hand_total",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ],
    "game": [
      {
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "priority_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "new_hand",
        "visible": "public",
        "type": "bool",
        "initial": true
      },
      {
        "key": "draw_pile",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "draw_pile_size",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "offer_row",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "dead_pile",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "claimed",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "any_valid_yaniv",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "showdown",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "min_caller_h",
        "visible": "public",
        "type": "number",
        "initial": 99
      },
      {
        "key": "min_noncaller_h",
        "visible": "public",
        "type": "number",
        "initial": 99
      },
      {
        "key": "min_h",
        "visible": "public",
        "type": "number",
        "initial": 99
      },
      {
        "key": "max_penalty",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "full_deck",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "number",
        "initial": -1
      },
      {
        "key": "cur",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 54
      },
      {
        "key": "joker_count",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "joker_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "copies_per_value_1_to_9",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "ten_value_cards",
        "visible": "public",
        "type": "number",
        "initial": 16
      },
      {
        "key": "ten_value",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "slots_per_player",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "cards_dealt_per_player",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "initial_offer_row_length",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "max_rounds",
        "visible": "public",
        "type": "number",
        "initial": 24
      },
      {
        "key": "yaniv_threshold",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "asaf_penalty",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "no_noncaller_n",
        "visible": "public",
        "type": "number",
        "initial": 99
      },
      {
        "key": "end_penalty",
        "visible": "public",
        "type": "number",
        "initial": 50
      },
      {
        "key": "initial_penalty",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "empty_slot_code",
        "visible": "public",
        "type": "number",
        "initial": -1
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "clear the players",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "penalty",
            "value": {
              "calc": "initial_penalty"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "c1",
            "value": {
              "calc": "empty_slot_code"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "c2",
            "value": {
              "calc": "empty_slot_code"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "c3",
            "value": {
              "calc": "empty_slot_code"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "set the table",
      "do": [
        {
          "set": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "key": "priority_seat",
            "value": 1
          }
        },
        {
          "set": {
            "key": "new_hand",
            "value": true
          }
        },
        {
          "set": {
            "key": "offer_row",
            "value": []
          }
        },
        {
          "set": {
            "key": "dead_pile",
            "value": []
          }
        },
        {
          "set": {
            "key": "full_deck",
            "value": [0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
          }
        }
      ]
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "deal",
      "label": "new hand",
      "when": {
        "calc": "new_hand"
      },
      "do": [
        {
          "set": {
            "key": "draw_pile",
            "value": {
              "calc": "full_deck"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "c1",
            "value": {
              "calc": "empty_slot_code"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "c2",
            "value": {
              "calc": "empty_slot_code"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "c3",
            "value": {
              "calc": "empty_slot_code"
            }
          }
        },
        {
          "set": {
            "key": "dead_pile",
            "value": []
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "draw_pile[min(int(uniform(0, len(draw_pile))), len(draw_pile) - 1)]"
            }
          }
        },
        {
          "set": {
            "player": 1,
            "key": "c1",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "draw_pile",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "draw_pile[min(int(uniform(0, len(draw_pile))), len(draw_pile) - 1)]"
            }
          }
        },
        {
          "set": {
            "player": 1,
            "key": "c2",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "draw_pile",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "draw_pile[min(int(uniform(0, len(draw_pile))), len(draw_pile) - 1)]"
            }
          }
        },
        {
          "set": {
            "player": 1,
            "key": "c3",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "draw_pile",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "draw_pile[min(int(uniform(0, len(draw_pile))), len(draw_pile) - 1)]"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "c1",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "draw_pile",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "draw_pile[min(int(uniform(0, len(draw_pile))), len(draw_pile) - 1)]"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "c2",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "draw_pile",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "draw_pile[min(int(uniform(0, len(draw_pile))), len(draw_pile) - 1)]"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "c3",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "draw_pile",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "draw_pile[min(int(uniform(0, len(draw_pile))), len(draw_pile) - 1)]"
            },
            "if": {
              "calc": "len(players) >= 3"
            }
          }
        },
        {
          "set": {
            "player": 3,
            "key": "c1",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 3"
            }
          }
        },
        {
          "remove": {
            "key": "draw_pile",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 3"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "draw_pile[min(int(uniform(0, len(draw_pile))), len(draw_pile) - 1)]"
            },
            "if": {
              "calc": "len(players) >= 3"
            }
          }
        },
        {
          "set": {
            "player": 3,
            "key": "c2",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 3"
            }
          }
        },
        {
          "remove": {
            "key": "draw_pile",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 3"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "draw_pile[min(int(uniform(0, len(draw_pile))), len(draw_pile) - 1)]"
            },
            "if": {
              "calc": "len(players) >= 3"
            }
          }
        },
        {
          "set": {
            "player": 3,
            "key": "c3",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 3"
            }
          }
        },
        {
          "remove": {
            "key": "draw_pile",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 3"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "draw_pile[min(int(uniform(0, len(draw_pile))), len(draw_pile) - 1)]"
            },
            "if": {
              "calc": "len(players) >= 4"
            }
          }
        },
        {
          "set": {
            "player": 4,
            "key": "c1",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 4"
            }
          }
        },
        {
          "remove": {
            "key": "draw_pile",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 4"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "draw_pile[min(int(uniform(0, len(draw_pile))), len(draw_pile) - 1)]"
            },
            "if": {
              "calc": "len(players) >= 4"
            }
          }
        },
        {
          "set": {
            "player": 4,
            "key": "c2",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 4"
            }
          }
        },
        {
          "remove": {
            "key": "draw_pile",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 4"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "draw_pile[min(int(uniform(0, len(draw_pile))), len(draw_pile) - 1)]"
            },
            "if": {
              "calc": "len(players) >= 4"
            }
          }
        },
        {
          "set": {
            "player": 4,
            "key": "c3",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 4"
            }
          }
        },
        {
          "remove": {
            "key": "draw_pile",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 4"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "draw_pile[min(int(uniform(0, len(draw_pile))), len(draw_pile) - 1)]"
            }
          }
        },
        {
          "set": {
            "key": "offer_row",
            "value": {
              "calc": "[pick]"
            }
          }
        },
        {
          "remove": {
            "key": "draw_pile",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "new_hand",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_total",
            "value": {
              "calc": "(you.c1 if you.c1 != empty_slot_code else 0) + (you.c2 if you.c2 != empty_slot_code else 0) + (you.c3 if you.c3 != empty_slot_code else 0)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "card_count",
            "value": {
              "calc": "count(c != empty_slot_code for c in [you.c1, you.c2, you.c3])"
            }
          }
        },
        {
          "set": {
            "key": "draw_pile_size",
            "value": {
              "calc": "len(draw_pile)"
            }
          }
        }
      ],
      "text": "A new hand is shuffled and dealt: {cards_dealt_per_player} cards each, and one card starts the offer row."
    },
    {
      "use": "sync",
      "phase": "deal",
      "label": "your hand",
      "mode": "self",
      "to": "all",
      "fields": [
        "c1",
        "c2",
        "c3",
        "hand_total"
      ],
      "text": "Your slots (-1 means empty) and hand total:"
    },
    {
      "use": "tell",
      "phase": "deal",
      "label": "the table",
      "to": "all",
      "text": "Round {round}. Offer row, position 1 first: {offer_row}. Dead pile: {dead_pile}. Draw pile: {draw_pile_size} cards. Priority seat: {priority_seat}. Cards held [seat, cards]: {[[p.seat, p.card_count] for p in players]}."
    },
    {
      "use": "update",
      "phase": "choose",
      "label": "reset for the round",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "is_caller",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "shed_values",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "action",
            "value": ""
          }
        },
        {
          "set": {
            "key": "claimed",
            "value": []
          }
        },
        {
          "set": {
            "key": "any_valid_yaniv",
            "value": false
          }
        },
        {
          "set": {
            "key": "showdown",
            "value": false
          }
        }
      ]
    },
    {
      "use": "poll",
      "phase": "choose",
      "label": "action",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": [
          "YANIV",
          "DRAW",
          "TAKE"
        ]
      },
      "store": "action",
      "text": "Choose your action in secret: YANIV (valid only if your hand total is {yaniv_threshold} or less; otherwise it is announced invalid and you DRAW), DRAW (a card from the draw pile, seen only by you) or TAKE (a card from the offer row {offer_row})."
    },
    {
      "use": "poll",
      "phase": "choose",
      "label": "take position",
      "to": "acting",
      "answer": {
        "type": "number",
        "min": 1,
        "max": {
          "calc": "len(offer_row)"
        }
      },
      "store": "take_pos",
      "text": "Which offer-row position would you take (1 is the first card of {offer_row})? Used only if you chose TAKE."
    },
    {
      "use": "poll",
      "phase": "choose",
      "label": "shed slot",
      "to": "acting",
      "answer": {
        "type": "number",
        "min": 1,
        "max": 3
      },
      "store": "shed_slot",
      "text": "Which slot do you shed: 1, 2 or 3? Every other slot holding the same value is shed with it. If the slot is empty, your lowest-numbered non-empty slot is shed instead. A taken or drawn card goes into this slot."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "yaniv check",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "shed_slot",
            "value": {
              "calc": "int(you.shed_slot) if [you.c1, you.c2, you.c3][int(you.shed_slot) - 1] != empty_slot_code else (1 if you.c1 != empty_slot_code else (2 if you.c2 != empty_slot_code else 3))"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.action == 'YANIV' and you.hand_total <= yaniv_threshold"
            },
            "key": "is_caller",
            "value": true,
            "text": "Seat {player} calls a valid YANIV."
          }
        },
        {
          "set": {
            "players": {
              "where": "you.action == 'YANIV' and you.hand_total > yaniv_threshold"
            },
            "key": "action",
            "value": "DRAW",
            "text": "Seat {player} called YANIV with a hand over the limit: invalid, treated as DRAW."
          }
        },
        {
          "set": {
            "key": "any_valid_yaniv",
            "value": {
              "calc": "count(p.is_caller for p in players) > 0"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "shed",
      "when": {
        "calc": "not any_valid_yaniv"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "shed_values",
            "value": {
              "calc": "[c for c in [you.c1, you.c2, you.c3] if c == [you.c1, you.c2, you.c3][int(you.shed_slot) - 1]]"
            },
            "text": "Seat {player} sheds {value}."
          }
        },
        {
          "set": {
            "players": "all",
            "key": "c1",
            "value": {
              "calc": "empty_slot_code"
            },
            "if": {
              "calc": "len(you.shed_values) > 0 and you.c1 == you.shed_values[0]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "c2",
            "value": {
              "calc": "empty_slot_code"
            },
            "if": {
              "calc": "len(you.shed_values) > 0 and you.c2 == you.shed_values[0]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "c3",
            "value": {
              "calc": "empty_slot_code"
            },
            "if": {
              "calc": "len(you.shed_values) > 0 and you.c3 == you.shed_values[0]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "take",
      "when": {
        "calc": "not any_valid_yaniv"
      },
      "do": [
        {
          "set": {
            "key": "dead_pile",
            "value": {
              "calc": "dead_pile + offer_row"
            }
          }
        },
        {
          "set": {
            "key": "cur",
            "value": {
              "calc": "((priority_seat - 1 + 0) % len(players)) + 1 if 0 < len(players) else 0"
        
... (cut)

Why it was refused: playing it with random seats failed: seed 1, 2 players: the match crashed: FlowError: 'len(you.shed_values) > 0 and you.c1 == you.shed_values[0]' reads `you` where there is no player
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "row_yaniv",
    "name": "Row Yaniv",
    "players": {
      "min": 2,
      "max": 4,
      "suggested": 3
    },
    "blurb": "Simultaneous Yaniv: each round secretly call YANIV, draw blind or take from a public offer row, and shed a card with its matches. Lowest penalty wins."
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
        "key": "c1",
        "visible": "ally",
        "type": "number",
        "initial": -1
      },
      {
        "key": "c2",
        "visible": "ally",
        "type": "number",
        "initial": -1
      },
      {
        "key": "c3",
        "visible": "ally",
        "type": "number",
        "initial": -1
      },
      {
        "key": "hand_total",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "card_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "penalty",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "action",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "take_pos",
        "visible": "ally",
        "type": "number",
        "initial": 1
      },
      {
        "key": "shed_slot",
        "visible": "ally",
        "type": "number",
        "initial": 1
      },
      {
        "key": "is_caller",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "shed_values",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "last_hand_total",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ],
    "game": [
      {
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "priority_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "new_hand",
        "visible": "public",
        "type": "bool",
        "initial": true
      },
      {
        "key": "draw_pile",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "draw_pile_size",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "offer_row",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "dead_pile",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "claimed",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "any_valid_yaniv",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "showdown",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "min_caller_h",
        "visible": "public",
        "type": "number",
        "initial": 99
      },
      {
        "key": "min_noncaller_h",
        "visible": "public",
        "type": "number",
        "initial": 99
      },
      {
        "key": "min_h",
        "visible": "public",
        "type": "number",
        "initial": 99
      },
      {
        "key": "max_penalty",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "full_deck",
        "visible": "none",
        "type": "list",
        "initial": [0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
      },
      {
        "key": "positions",
        "visible": "none",
        "type": "list",
        "initial": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "number",
        "initial": -1
      },
      {
        "key": "cur",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "take_ok",
        "visible": "none",
        "type": "bool",
        "initial": false
      },
      {
        "key": "tpos",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "draw_ok",
        "visible": "none",
        "type": "bool",
        "initial": false
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 54
      },
      {
        "key": "joker_count",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "joker_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "copies_per_value_1_to_9",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "ten_value_cards",
        "visible": "public",
        "type": "number",
        "initial": 16
      },
      {
        "key": "ten_value",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "slots_per_player",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "cards_dealt_per_player",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "initial_offer_row_length",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "max_rounds",
        "visible": "public",
        "type": "number",
        "initial": 24
      },
      {
        "key": "yaniv_threshold",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "asaf_penalty",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "no_noncaller_n",
        "visible": "public",
        "type": "number",
        "initial": 99
      },
      {
        "key": "end_penalty",
        "visible": "public",
        "type": "number",
        "initial": 50
      },
      {
        "key": "initial_penalty",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "empty_slot_code",
        "visible": "public",
        "type": "number",
        "initial": -1
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "clear the players",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "penalty",
            "value": {
              "calc": "initial_penalty"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "c1",
            "value": {
              "calc": "empty_slot_code"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "c2",
            "value": {
              "calc": "empty_slot_code"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "c3",
            "value": {
              "calc": "empty_slot_code"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "set the table",
      "do": [
        {
          "set": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "key": "priority_seat",
            "value": 1
          }
        },
        {
          "set": {
            "key": "new_hand",
            "value": true
          }
        },
        {
          "set": {
            "key": "offer_row",
            "value": []
          }
        },
        {
          "set": {
            "key": "dead_pile",
            "value": []
          }
        }
      ]
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "deal",
      "label": "new hand",
      "when": {
        "calc": "new_hand"
      },
      "do": [
        {
          "set": {
            "key": "draw_pile",
            "value": {
              "calc": "full_deck"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "c1",
            "value": {
              "calc": "empty_slot_code"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "c2",
            "value": {
              "calc": "empty_slot_code"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "c3",
            "value": {
              "calc": "empty_slot_code"
            }
          }
        },
        {
          "set": {
            "key": "dead_pile",
            "value": []
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "draw_pile[min(int(uniform(0, len(draw_pile))), len(draw_pile) - 1)]"
            }
          }
        },
        {
          "set": {
            "player": 1,
            "key": "c1",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "draw_pile",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "draw_pile[min(int(uniform(0, len(draw_pile))), len(draw_pile) - 1)]"
            }
          }
        },
        {
          "set": {
            "player": 1,
            "key": "c2",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "draw_pile",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "draw_pile[min(int(uniform(0, len(draw_pile))), len(draw_pile) - 1)]"
            }
          }
        },
        {
          "set": {
            "player": 1,
            "key": "c3",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "draw_pile",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "draw_pile[min(int(uniform(0, len(draw_pile))), len(draw_pile) - 1)]"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "c1",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "draw_pile",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "draw_pile[min(int(uniform(0, len(draw_pile))), len(draw_pile) - 1)]"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "c2",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "draw_pile",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "draw_pile[min(int(uniform(0, len(draw_pile))), len(draw_pile) - 1)]"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "c3",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "draw_pile",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "draw_pile[min(int(uniform(0, len(draw_pile))), len(draw_pile) - 1)]"
            },
            "if": {
              "calc": "len(players) >= 3"
            }
          }
        },
        {
          "set": {
            "player": 3,
            "key": "c1",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 3"
            }
          }
        },
        {
          "remove": {
            "key": "draw_pile",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 3"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "draw_pile[min(int(uniform(0, len(draw_pile))), len(draw_pile) - 1)]"
            },
            "if": {
              "calc": "len(players) >= 3"
            }
          }
        },
        {
          "set": {
            "player": 3,
            "key": "c2",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 3"
            }
          }
        },
        {
          "remove": {
            "key": "draw_pile",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 3"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "draw_pile[min(int(uniform(0, len(draw_pile))), len(draw_pile) - 1)]"
            },
            "if": {
              "calc": "len(players) >= 3"
            }
          }
        },
        {
          "set": {
            "player": 3,
            "key": "c3",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 3"
            }
          }
        },
        {
          "remove": {
            "key": "draw_pile",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 3"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "draw_pile[min(int(uniform(0, len(draw_pile))), len(draw_pile) - 1)]"
            },
            "if": {
              "calc": "len(players) >= 4"
            }
          }
        },
        {
          "set": {
            "player": 4,
            "key": "c1",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 4"
            }
          }
        },
        {
          "remove": {
            "key": "draw_pile",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 4"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "draw_pile[min(int(uniform(0, len(draw_pile))), len(draw_pile) - 1)]"
            },
            "if": {
              "calc": "len(players) >= 4"
            }
          }
        },
        {
          "set": {
            "player": 4,
            "key": "c2",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 4"
            }
          }
        },
        {
          "remove": {
            "key": "draw_pile",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 4"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "draw_pile[min(int(uniform(0, len(draw_pile))), len(draw_pile) - 1)]"
            },
            "if": {
              "calc": "len(players) >= 4"
            }
          }
        },
        {
          "set": {
            "player": 4,
            "key": "c3",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 4"
            }
          }
        },
        {
          "remove": {
            "key": "draw_pile",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 4"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "draw_pile[min(int(uniform(0, len(draw_pile))), len(draw_pile) - 1)]"
            }
          }
        },
        {
          "set": {
            "key": "offer_row",
            "value": {
              "calc": "[pick]"
            }
          }
        },
        {
          "remove": {
            "key": "draw_pile",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "new_hand",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_total",
            "value": {
              "calc": "(you.c1 if you.c1 != empty_slot_code else 0) + (you.c2 if you.c2 != empty_slot_code else 0) + (you.c3 if you.c3 != empty_slot_code else 0)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "card_count",
            "value": {
              "calc": "count(c != empty_slot_code for c in [you.c1, you.c2, you.c3])"
            }
          }
        },
        {
          "set": {
            "key": "draw_pile_size",
            "value": {
              "calc": "len(draw_pile)"
            }
          }
        }
      ],
      "text": "A new hand is shuffled and dealt: {cards_dealt_per_player} cards each, and one card starts the offer row."
    },
    {
      "use": "sync",
      "phase": "deal",
      "label": "your hand",
      "mode": "self",
      "to": "all",
      "fields": [
        "c1",
        "c2",
        "c3",
        "hand_total"
      ],
      "text": "Your slots (-1 means empty) and hand total:"
    },
    {
      "use": "tell",
      "phase": "deal",
      "label": "the table",
      "to": "all",
      "text": "Round {round}. Offer row, position 1 first: {offer_row}. Dead pile: {dead_pile}. Draw pile: {draw_pile_size} cards. Priority seat: {priority_seat}. Cards held [seat, cards]: {[[p.seat, p.card_count] for p in players]}."
    },
    {
      "use": "update",
      "phase": "choose",
      "label": "reset for the round",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "is_caller",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "shed_values",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "action",
            "value": ""
          }
        },
        {
          "set": {
            "key": "claimed",
            "value": []
          }
        },
        {
          "set": {
            "key": "any_valid_yaniv",
            "value": false
          }
        },
        {
          "set": {
            "key": "showdown",
            "value": false
          }
        }
      ]
    },
    {
      "use": "poll",
      "phase": "choose",
      "label": "action",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": [
          "YANIV",
          "DRAW",
          "TAKE"
        ]
      },
      "store": "action",
      "text": "Choose your action in secret: YANIV (valid only if your hand total is {yaniv_threshold} or less; otherwise it is announced invalid and you DRAW), DRAW (the top card of the draw pile, seen only by you) or TAKE (a card from the offer row {offer_row})."
    },
    {
      "use": "poll",
      "phase": "choose",
      "label": "take position",
      "to": "acting",
      "answer": {
        "type": "number",
        "min": 1,
        "max": {
          "calc": "len(offer_row)"
        }
      },
      "store": "take_pos",
      "text": "Which offer-row position would you take (1 is the first card of {offer_row})? Used only if you chose TAKE."
    },
    {
      "use": "poll",
      "phase": "choose",
      "label": "shed slot",
      "to": "acting",
      "answer": {
        "type": "number",
        "min": 1,
        "max": 3
      },
      "store": "shed_slot",
      "text": "Which slot do you shed: 1, 2 or 3? Every other slot holding the same value is shed with it. If the slot is empty, your lowest-numbered non-empty slot is shed instead. A taken or drawn card goes into this slot."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "yaniv check",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "shed_slot",
            "value": {
              "calc": "int(you.shed_slot) if [you.c1, you.c2, you.c3][int(you.shed_slot) - 1] != empty_slot_code else (1 if you.c1 != empty_slot_code else (2 if you.c2 != empty_slot_code else 3))"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.action == 'YANIV' and you.hand_total <= yaniv_threshold"
            },
            "key": "is_caller",
            "value": true,
            "text": "Seat {player} calls a valid YANIV."
          }
        },
        {
          "set": {
            "players": {
              "where": "you.action == 'YANIV' and you.hand_total > yaniv_threshold"
            },
            "key": "action",
            "value": "DRAW",
            "text": "Seat {player} called YANIV with a hand over the limit: invalid, treated as DRAW."
          }
        },
        {
          "set": {
            "key": "any_valid_yaniv",
            "value": {
              "calc": "count(p.is_caller for p in players) > 0"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "shed",
      "when": {
        "calc": "not any_valid_yaniv"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "shed_values",
            "value": {
              "calc": "[c for c in [you.c1, you.c2, you.c3] if c == [you.c1, you.c2, you.c3][int(you.shed_slot) - 1]]"
            },
            "text": "Seat {player} sheds {value}."
          }
        },
        {
          "set": {
            "players": "all",
            "key": "c1",
            "value": {
              "calc": "empty_slot_code if (len(you.shed_values) > 0 and you.c1 == you.shed_values[0]) else you.c1"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "c2",
            "value": {
              "calc": "empty_slot_code if (len(you.shed_values) > 0 and you.c2 == you.shed_values[0]) else you.c2"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "c3",
            "value": {
              "calc": "empty_slot_code if (len(you.shed_values) > 0 and you.c3 == you.shed_values[0]) else you.c3"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "take",
      "when": {
        "calc": "not any_valid_yaniv"
      },
      "do": [
        {
          "set": {
            "key": "cur",
            "value": {
              "calc": "((priority_seat - 1 + 0) % len(players)) + 1"
            }
          }
        },
        {
          "set": {
            "key": "take_ok",
            "value": {
              "calc": "count(p.seat == cur and p.action == 'TAKE' and int(p.take_pos) not in claimed for p in players) > 0"
            }
          }
        },
        {
          "set": {
            "key": "tpos",
            "value": {
              "calc": "sum([int(p.take_pos) for p in players if p.seat == cur])"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == cur and take_ok and int(you.shed_slot) == 1"
            },
            "key": "c1",
            "value": {
              "calc": "offer_row[tpos - 1]"
            },
            "text": "Seat {player} takes {value} from the offer row."
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == cur and take_ok and int(you.shed_slot) == 2"
            },
            "key": "c2",
            "value": {
              "calc": "offer_row[tpos - 1]"
            },
            "text": "Seat {player} takes {value} from the offer row."
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == cur and take_ok and int(you.shed_slot) == 3"
            },
            "key": "c3",
            "value": {
              "calc": "offer_row[tpos - 1]"
            },
            "text": "Seat {player} takes {value} from the offer row."
          }
        },
        {
          "append": {
            "key": "claimed",
            "value": {
              "calc": "tpos"
            },
            "if": {
              "calc": "take_ok"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == cur and you.action == 'TAKE' and not take_ok"
            },
            "key": "action",
            "value": "DRAW",
            "text": "Seat {player} wanted a card already taken and draws instead."
          }
        },
        {
          "set": {
            "key": "cur",
            "value": {
              "calc": "((priority_seat - 1 + 1) % len(players)) + 1 if 1 < len(players) else 0"
            }
          }
        },
        {
          "set": {
            "key": "take_ok",
            "value": {
              "calc": "count(p.seat == cur and p.action == 'TAKE' and int(p.take_pos) not in claimed for p in players) > 0"
            }
          }
        },
        {
          "set": {
            "key": "tpos",
            "value": {
              "calc": "sum([int(p.take_pos) for p in players if p.seat == cur])"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == cur and take_ok and int(you.shed_slot) == 1"
            },
            "key": "c1",
            "value": {
              "calc": "offer_row[tpos - 1]"
            },
            "text": "Seat {player} takes {value} from the offer row."
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == cur and take_ok and int(you.shed_slot) == 2"
            },
            "key": "c2",
            "value": {
              "calc": "offer_row[tpos - 1]"
            },
            "text": "Seat {player} takes {value} from the offer row."
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == cur and take_ok and int(you.shed_slot) == 3"
            },
            "key": "c3",
            "value": {
              "calc": "offer_row[tpos - 1]"
            },
            "text": "Seat {player} takes {value} from the offer row."
          }
        },
        {
          "append": {
            "key": "claimed",
            "value": {
              "calc": "tpos"
            },
            "if": {
              "calc": "take_ok"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == cur and you.action == 'TAKE' and not take_ok"
            },
            "key": "action",
            "value": "DRAW",
            "text": "Seat {player} wanted a card already taken and draws instead."
          }
        },
        {
          "set": {
            "key": "cur",
            "value": {
              "calc": "((priority_seat - 1 + 2) % len(players)) + 1 if 2 < len(players) else 0"
            }
          }
        },
        {
          "set": {
            "key": "take_ok",
            "value": {
              "calc": "count(p.seat == cur and p.action == 'TAKE' and int(p.take_pos) not in claimed for p in players) > 0"
            }
          }
        },
        {
          "set": {
            "key": "tpos",
            "value": {
              "calc": "sum([int(p.take_pos) for p in players if p.seat == cur])"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == cur and take_ok and int(you.shed_slot) == 1"
            },
            "key": "c1",
            "value": {
              "calc": "offer_row[tpos - 1]"
            },
            "text": "Seat {player} takes {value} from the offer row."
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == cur and take_ok and int(you.shed_slot) == 2"
            },
            "key": "c2",
            "value": {
              "calc": "offer_row[tpos - 1]"
            },
            "text": "Seat {player} takes {value} from the offer row."
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == cur and take_ok and int(you.shed_slot) == 3"
            },
            "key": "c3",
            "value": {
              "calc": "offer_row[tpos - 1]"
            },
            "text": "Seat {player} takes {value} from the offer row."
          }
        },
        {
          "append": {
            "key": "claimed",
            "value": {
              "calc": "tpos"
            },
            "if": {
              "calc": "take_ok"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == cur and you.action == 'TAKE' and not take_ok"
            },
            "key": "action",
            "value": "DRAW",
            "text": "Seat {player} wanted a card already taken and draws instead."
          }
        },
        {
          "set": {
            "key": "cur",
            "value": {
              "calc": "((priority_seat - 1 + 3) % len(players)) + 1 if 3 < len(players) else 0"
            }
          }
        },
        {
          "set": {
            "key": "take_ok",
            "value": {
              "calc": "count(p.seat == cur and p.action == 'TAKE' and int(p.take_pos) not in claimed for p in players) > 0"
            }
          }
        },
        {
          "set": {
            "key": "tpos",
            "value": {
              "calc": "sum([int(p.take_pos) for p in players if p.seat == cur])"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == cur and take_ok and int(you.shed_slot) == 1"
            },
            "key": "c1",
            "value": {
              "calc": "offer_row[tpos - 1]"
            },
            "text": "Seat {player} takes {value} from the offer row."
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == cur and take_ok and int(you.shed_slot) == 2"
            },
            "key": "c2",
            "value": {
              "calc": "offer_row[tpos - 1]"
            },
            "text": "Seat {player} takes {value} from the offer row."
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == cur and take_ok and int(you.shed_slot) == 3"
            },
            "key": "c3",
            "value": {
              "calc": "offer_row[tpos - 1]"
            },
            "text": "Seat {player} takes {value} from the offer row."
          }
        },
        {
          "append": {
            "key": "claimed",
            "value": {
              "calc": "tpos"
            },
            "if": {
              "calc": "take_ok"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == cur and you.action == 'TAKE' and not take_ok"
            },
            "key": "action",
            "value": "DRAW",
            "text": "Seat {player} wanted a card already taken and draws instead."
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "draw",
      "when": {
        "calc": "not any_valid_yaniv"
      },
      "do": [
        {
          "set": {
            "key": "cur",
            "value": {
              "calc": "((priority_seat - 1 + 0) % len(players)) + 1"
            }
          }
        },
        {
          "set": {
            "key": "draw_ok",
            "value": {
              "calc": "count(p.seat == cur and p.action == 'DRAW' for p in players) > 0 and len(draw_pile) > 0"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "draw_pile[min(int(uniform(0, len(draw_pile))), len(draw_pile) - 1)]"
            },
            "if": {
              "calc": "draw_ok"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == cur and draw_ok and int(you.shed_slot) == 1"
            },
            "key": "c1",
            "value": {
              "calc": "pick"
            },
            "text": "You draw {value}.",
            "announce_to": {
              "where": "you.seat == cur"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == cur and draw_ok and int(you.shed_slot) == 2"
            },
            "key": "c2",
            "value": {
              "calc": "pick"
            },
            "text": "You draw {value}.",
            "announce_to": {
              "where": "you.seat == cur"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == cur and draw_ok and int(you.shed_slot) == 3"
            },
            "key": "c3",
            "value": {
              "calc": "pick"
            },
            "text": "You draw {value}.",
            "announce_to": {
              "where": "you.seat == cur"
            }
          }
        },
        {
          "remove": {
            "key": "draw_pile",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "draw_ok"
            }
          }
        },
        {
          "adjust": {
            "key": "draw_pile_size",
            "value": -1,
            "if": {
              "calc": "draw_ok"
            }
          }
        },
        {
          "set": {
            "key": "cur",
            "value": {
              "calc": "((priority_seat - 1 + 1) % len(players)) + 1 if 1 < len(players) else 0"
            }
          }
        },
        {
          "set": {
            "key": "draw_ok",
            "value": {
              "calc": "count(p.seat == cur and p.action == 'DRAW' for p in players) > 0 and len(draw_pile) > 0"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "draw_pile[min(int(uniform(0, len(draw_pile))), len(draw_pile) - 1)]"
            },
            "if": {
              "calc": "draw_ok"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == cur and draw_ok and int(you.shed_slot) == 1"
            },
            "key": "c1",
            "value": {
              "calc": "pick"
            },
            "text": "You draw {value}.",
            "announce_to": {
              "where": "you.seat == cur"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == cur and draw_ok and int(you.shed_slot) == 2"
            },
            "key": "c2",
            "value": {
              "calc": "pick"
            },
            "text": "You draw {value}.",
            "announce_to": {
              "where": "you.seat == cur"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == cur and draw_ok and int(you.shed_slot) == 3"
            },
            "key": "c3",
            "value": {
              "calc": "pick"
            },
            "text": "You draw {value}.",
            "announce_to": {
              "where": "you.seat == cur"
            }
          }
        },
        {
          "remove": {
            "key": "draw_pile",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "draw_ok"
            }
          }
        },
        {
          "adjust": {
            "key": "draw_pile_size",
            "value": -1,
            "if": {
              "calc": "draw_ok"
            }
          }
        },
        {
          "set": {
            "key": "cur",
            "value": {
              "calc": "((priority_seat - 1 + 2) % len(players)) + 1 if 2 < len(players) else 0"
            }
          }
        },
        {
          "set": {
            "key": "draw_ok",
            "value": {
              "calc": "count(p.seat == cur and p.action == 'DRAW' for p in players) > 0 and len(draw_pile) > 0"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "draw_pile[min(int(uniform(0, len(draw_pile))), len(draw_pile) - 1)]"
            },
            "if": {
              "calc": "draw_ok"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == cur and draw_ok and int(you.shed_slot) == 1"
            },
            "key": "c1",
            "value": {
              "calc": "pick"
            },
            "text": "You draw {value}.",
            "announce_to": {
              "where": "you.seat == cur"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == cur and draw_ok and int(you.shed_slot) == 2"
            },
            "key": "c2",
            "value": {
              "calc": "pick"
            },
            "text": "You draw {value}.",
            "announce_to": {
              "where": "you.seat == cur"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == cur and draw_ok and int(you.shed_slot) == 3"
            },
            "key": "c3",
            "value": {
              "calc": "pick"
            },
            "text": "You draw {value}.",
            "announce_to": {
              "where": "you.seat == cur"
            }
          }
        },
        {
          "remove": {
            "key": "draw_pile",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "draw_ok"
            }
          }
        },
        {
          "adjust": {
            "key": "draw_pile_size",
            "value": -1,
            "if": {
              "calc": "draw_ok"
            }
          }
        },
        {
          "set": {
            "key": "cur",
            "value": {
              "calc": "((priority_seat - 1 + 3) % len(players)) + 1 if 3 < len(players) else 0"
            }
          }
        },
        {
          "set": {
            "key": "draw_ok",
            "value": {
              "calc": "count(p.seat == cur and p.action == 'DRAW' for p in players) > 0 and len(draw_pile) > 0"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "draw_pile[min(int(uniform(0, len(draw_pile))), len(draw_pile) - 1)]"
            },
            "if": {
              "calc": "draw_ok"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == cur and draw_ok and int(you.shed_slot) == 1"
            },
            "key": "c1",
            "value": {
              "calc": "pick"
            },
            "text": "You draw {value}.",
            "announce_to": {
              "where": "you.seat == cur"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == cur and draw_ok and int(you.shed_slot) == 2"
            },
            "key": "c2",
            "value": {
              "calc": "pick"
            },
            "text": "You draw {value}.",
            "announce_to": {
              "where": "you.seat == cur"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == cur and draw_ok and int(you.shed_slot) == 3"
            },
            "key": "c3",
            "value": {
              "calc": "pick"
            },
            "text": "You draw {value}.",
            "announce_to": {
              "where": "you.seat == cur"
            }
          }
        },
        {
          "remove": {
            "key": "draw_pile",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "draw_ok"
            }
          }
        },
        {
          "adjust": {
            "key": "draw_pile_size",
            "value": -1,
            "if": {
              "calc": "draw_ok"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "row update",
      "when": {
        "calc": "not any_valid_yaniv"
      },
      "do": [
        {
          "set": {
            "key": "dead_pile",
            "value": {
              "calc": "dead_pile + [offer_row[i - 1] for i in positions if i <= len(offer_row) and i not in claimed]"
            }
          }
        },
        {
          "set": {
            "key": "offer_row",
            "value": {
              "calc": "[v for p in players for v in p.shed_values]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_total",
            "value": {
              "calc": "(you.c1 if you.c1 != empty_slot_code else 0) + (you.c2 if you.c2 != empty_slot_code else 0) + (you.c3 if you.c3 != empty_slot_code else 0)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "card_count",
            "value": {
              "calc": "count(c != empty_slot_code for c in [you.c1, you.c2, you.c3])"
            }
          }
        },
        {
          "set": {
            "key": "draw_pile_size",
            "value": {
              "calc": "len(draw_pile)"
            }
          }
        }
      ],
      "text": "New offer row: {offer_row}. Dead pile: {dead_pile}. Draw pile: {draw_pile_size} cards. Cards held [seat, cards]: {[[p.seat, p.card_count] for p in players]}."
    },
    {
      "use": "sync",
      "phase": "resolve",
      "label": "your updated hand",
      "mode": "self",
      "to": "all",
      "fields": [
        "c1",
        "c2",
        "c3",
        "hand_total"
      ],
      "text": "Your slots now (-1 means empty) and hand total:"
    },
    {
      "use": "update",
      "phase": "showdown",
      "label": "showdown test",
      "do": [
        {
          "set": {
            "key": "showdown",
            "value": {
              "calc": "any_valid_yaniv or draw_pile_size < len(players) or round >= max_rounds"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "last_hand_total",
            "value": {
              "calc": "you.hand_total if showdown else you.last_hand_total"
            }
          }
        },
        {
          "set": {
            "key": "min_caller_h",
            "value": {
              "calc": "min([p.hand_total for p in players if p.is_caller] + [no_noncaller_n])"
            },
            "if": {
              "calc": "showdown"
            }
          }
        },
        {
          "set": {
            "key": "min_noncaller_h",
            "value": {
              "calc": "min([p.hand_total for p in players if not p.is_caller] + [no_noncaller_n])"
            },
            "if": {
              "calc": "showdown"
            }
          }
        },
        {
          "set": {
            "key": "min_h",
            "value": {
              "calc": "min([p.hand_total for p in players])"
            },
            "if": {
              "calc": "showdown"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "showdown",
      "label": "scoring",
      "when": {
        "calc": "showdown"
      },
      "do": [
        {
          "adjust": {
            "players": "all",
            "key": "penalty",
            "value": {
              "calc": "((0 if (you.hand_total == min_caller_h and min_caller_h < min_noncaller_h) else you.hand_total + asaf_penalty) if you.is_caller else (0 if you.hand_total <= min_caller_h else you.hand_total)) if any_valid_yaniv else (0 if you.hand_total == min_h else you.hand_total)"
            },
            "text": "Seat {player} scores {value} penalty."
          }
        },
        {
          "set": {
            "key": "max_penalty",
            "value": {
              "calc": "max([p.penalty for p in players])"
            }
          }
        },
        {
          "set": {
            "key": "new_hand",
            "value": true
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "showdown",
      "label": "the reveal",
      "when": {
        "calc": "showdown"
      },
      "to": "all",
      "text": "Showdown. Hands [seat, slots, H]: {[[p.seat, [p.c1, p.c2, p.c3], p.hand_total] for p in players]}. Penalty totals [seat, penalty]: {[[p.seat, p.penalty] for p in players]}. A fresh hand is dealt next round."
    },
    {
      "use": "update",
      "phase": "end",
      "label": "pass priority",
      "do": [
        {
          "set": {
            "key": "priority_seat",
            "value": {
              "calc": "(priority_seat % len(players)) + 1"
            }
          }
        },
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "end",
      "label": "end check",
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "(showdown and max_penalty >= end_penalty) or round > max_rounds"
      },
      "rank_by": "0 - you.penalty",
      "text": "Winner: {result}. Final penalty totals [seat, penalty]: {[[p.seat, p.penalty] for p in players]}."
    }
  },
  "limits": {
    "rounds": 24,
    "rounds_max": 24,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "DECK: {deck_size} cards, used only for their values: {joker_count} Jokers worth {joker_value}; {copies_per_value_1_to_9} each of values 1 to 9 (Ace = 1); {ten_value_cards} cards worth {ten_value}. Suits are ignored.\n\nEach player has {slots_per_player} private slots c1, c2, c3; each holds one card value or is empty (shown as {empty_slot_code}). Your hand total H is the sum of your non-empty slots. Penalty totals are public and start at {initial_penalty}. The table shows the round (1 to {max_rounds}), the priority seat (seat 1 in round 1), the draw pile size (its order is hidden), the OFFER ROW (an ordered public list) and the DEAD PILE (every card that has left play this hand).\n\nEACH ROUND:\n1. NEW HAND. If a new hand is due, all {deck_size} cards are shuffled into the draw pile, all slots and the dead pile are emptied, each player is dealt {cards_dealt_per_player} cards into c1, c2, c3 (told privately), and {initial_offer_row_length} more card starts the offer row.\n2. The offer row, dead pile, draw pile size, priority seat and each player's card count are announced.\n3. CHOICES. All players answer at the same moment, privately: (a) action: YANIV, DRAW or TAKE; (b) take position: 1 to the length of the offer row (used only for TAKE); (c) shed slot: 1, 2 or 3. If the chosen slot is empty, your lowest-numbered non-empty slot is used.\n4. YANIV CHECK. A YANIV is valid only if your H is {yaniv_threshold} or less. If it is not, it is announced as invalid and you are treated as DRAW for the rest of the round.\n5. If at least one valid YANIV was made, no cards move this round and a showdown follows. If none was made, steps 6 to 9 happen.\n6. SHED. Each player removes the card in their shed slot, and every other slot of theirs holding the same value is also removed (a pair sheds two, a triple three). Those extra slots stay empty for the rest of the hand. Every player's shed values are announced.\n7. TAKE. TAKE players are resolved in seat order starting at the priority seat and wrapping. Each receives the offer-row card at their position if no earlier player claimed it, placed in their shed slot, and the take is announced. If it was already claimed, that player becomes DRAW.\n8. DRAW. In the same order, each DRAW player takes the top card of the draw pile into their shed slot, told only to them; the draw pile shrinks by 1 per draw.\n9. ROW UPDATE. Offer-row cards not taken go to the dead pile. The new offer row is every card shed in step 6, in seat order from seat 1, and in slot order within a player. Card counts and draw pile size are announced.\n10. SHOWDOWN happens if a valid YANIV was made, or the draw pile holds fewer cards than there are players after step 9, or this is round {max_rounds}. All hands are revealed. With valid callers: M is the lowest caller H, N the lowest non-caller H (N = {no_noncaller_n} if everyone called). A caller scores 0 if their H equals M and M is less than N; otherwise they score H + {asaf_penalty} (Asaf). A non-caller scores 0 if their H is less than or equal to M; otherwise they score H. With no valid caller: every player with the lowest H scores 0, the others score their H. Scores are added to penalty totals, all totals are announced, and the next round starts a fresh hand and shuffle. With no showdown, the hand continues next round.\n11. The priority seat passes to the next seat (wrapping to seat 1).\n12. The match ends after a showdown that leaves any penalty total at {end_penalty} or more, or after round {max_rounds}. The lowest penalty total wins; players tied for the lowest share the win.\n\nThere is no discussion."
}
```
````
