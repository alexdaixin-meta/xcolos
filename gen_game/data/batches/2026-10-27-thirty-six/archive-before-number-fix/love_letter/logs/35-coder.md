# 35 coder

- time: 2026-10-27T19:15:29+00:00 (113.8s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 1bb93732b87c3efe, reply sha256 21dce441d7cf012d

## Sent

````
# Task: write the XColos game file for "Love Letter: Short Hands"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 2; set `meta.players` to {"min": 2, "max": 2, "suggested": 2} (the suggested size is the one the game plays best at).

CARDS (16, stored once as full_deck): 5 Guard (rank 1), 2 Priest (2), 2 Baron (3), 2 Handmaid (4), 2 Prince (5), 1 King (6), 1 Countess (7), 1 Princess (8).

STATE
- Each player has: hand (private, seen only by its owner), discards (public list), points (start 0), protected (public, 0/1) and eliminated (public, 0/1).
- The table shows: out_of_play (public list), deck_count (public, always the number of cards in the deck), stake, active seat, starter seat (starts as seat 1) and round number.
- Hidden bookkeeping: deck order, new_hand (starts 1), folded, current_discard and guard_guess.
- The bottom card of the deck is the RESERVE. It is never drawn at the start of a turn.

ROUND: one round is one turn by the active player. The game lasts exactly 40 rounds. The steps run in order every round. A step marked 'when' runs only if its condition holds.

1. NEW HAND (when new_hand = 1):
- Empty both players' hands and discards, and clear out_of_play.
- Copy full_deck into the deck and shuffle it. This is the only random event in a round.
- Move the top 5 cards face up into out_of_play.
- Deal 1 card to each player's hand. The deck now holds 9 cards.
- Set protected = 0 and eliminated = 0 for both players, stake = 1 and folded = 0.
- The active seat becomes the starter seat. Set new_hand = 0.

2. START OF TURN: set the active player's protected to 0. The active player draws the top card of the deck, so they hold 2 cards.

3. DISCARD (choice, active player): 'Choose one of your two cards to discard.'

4. RESOLVE DISCARD: if the active player holds the Countess together with a King or a Prince, the Countess is discarded whatever was chosen. The card goes onto the player's discards and becomes current_discard. Everyone is told 'Seat X discards CARD'.

5. GUARD GUESS (choice, when current_discard is a Guard and the opponent is not protected): the active player names a rank from 2 to 8. The named rank is announced to both players.

6. GUARD CHECK (when step 5 ran): if the opponent's card has the named rank, the opponent is eliminated and everyone is told 'Hit: CARD'. Otherwise everyone is told 'Miss'.

7. PRIEST (when current_discard is a Priest and the opponent is not protected): only the active player is told the opponent's card.

8. BARON (when current_discard is a Baron and the opponent is not protected): the two hand cards are compared. The holder of the lower rank is eliminated and their card is announced. On equal ranks nothing happens and nothing is revealed.

9. HANDMAID (when current_discard is a Handmaid): the active player becomes protected (until their next turn starts).

10. PRINCE DISCARD (when current_discard is a Prince): the target is the opponent, or the active player if the opponent is protected. The target discards their hand card face up with no effect, and it is announced. If it is the Princess, the target is eliminated.

11. PRINCE REDRAW (when step 10 ran and the target is not eliminated): the target takes the top card of the deck. This may be the reserve if it is the only card left.

12. KING (when current_discard is a King and the opponent is not protected): the two players swap hand cards.

13. PRINCESS (when current_discard is the Princess): the active player is eliminated.

14. RAISE (choice, active player; only when stake = 1, nobody is eliminated, deck_count >= 2 and the opponent has at least one card in their discards): 'Raise this hand's stake to 2, or pass?'

15. RESPONSE (choice, opponent; when a raise was just made): 'Accept (the stake becomes 2) or fold?' On accept, stake = 2. On fold, folded = 1.

16. HAND END. Apply the first of these that holds:
- (a) If folded = 1, the active player gains 1 point.
- (b) Otherwise, if a player is eliminated, the other player gains points equal to the stake.
- (c) Otherwise, if deck_count <= 1 or this is round 40, there is a showdown. Both hand cards are revealed and the higher rank gains points equal to the stake. On equal ranks nobody scores.
If (a), (b) or (c) applied, set new_hand = 1 and switch the starter seat to the other seat.

17. PASS TURN AND GAME END:
- If new_hand = 1, the active seat becomes the starter seat. Otherwise the opponent becomes the active player.
- After round 40 the game ends.

DECK CHECK: after the deal the deck holds 9 cards. A hand goes to showdown whenever 1 or 0 cards remain at the end of a turn. So every turn starts with at least 2 cards in the deck, the draw always leaves at least the reserve, and a Prince redraw always has a card to take.

How the winner is decided: After exactly 40 rounds (a hand still running in round 40 is settled by showdown in that round), the player with more points wins. Equal points is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Love Letter: Short Hands (2 to 2 players, best with 2)

Two-player Love Letter over exactly 40 turns: draw, discard a card to use its effect, knock out the rival or win the showdown, and optionally raise a hand's stake to 2.

STATE (every item below must exist in the file):
  - each player: hand (list, starts []); only its owner sees it. Ranks of the cards held: 1 card between turns, 2 during own turn.
  - each player: discards (list, starts []); everyone sees it. Ranks this player discarded this hand, in order.
  - each player: points (number, starts 0); everyone sees it. Score.
  - each player: protected (number, starts 0); everyone sees it. 1 if protected by a Handmaid until this player's next turn starts.
  - each player: eliminated (number, starts 0); everyone sees it. 1 if knocked out of the current hand.
  - the table: full_deck (list, starts [1, 1, 1, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 7, 8]); hidden from all players. The 16 card ranks, copied into the deck each new hand.
  - the table: deck (list, starts []); hidden from all players. Drawable cards in shuffled order, top first, not counting the reserve.
  - the table: reserve (list, starts []); hidden from all players. The bottom card of the deck. It is never drawn at the start of a turn. A Prince redraw takes it only when the deck list is empty.
  - the table: deck_count (number, starts 0); everyone sees it. Cards left in the deck: length of deck plus length of reserve.
  - the table: out_of_play (list, starts []); everyone sees it. The 5 cards set aside face up at the start of each hand.
  - the table: stake (number, starts 1); everyone sees it. Points the current hand is worth.
  - the table: active_seat (number, starts 1); everyone sees it. Seat taking this turn.
  - the table: starter_seat (number, starts 1); everyone sees it. Seat that starts the next or current hand.
  - the table: round_number (number, starts 1); everyone sees it. Current round (turn), 1 to 40.
  - the table: new_hand (number, starts 1); hidden from all players. 1 if a new hand must be dealt at the start of this round.
  - the table: folded (number, starts 0); hidden from all players. 1 if the opponent folded to a raise this turn.
  - the table: current_discard (number, starts 0); hidden from all players. Rank discarded this turn.
  - the table: guard_guess (number, starts 0); hidden from all players. Rank named with a Guard this turn (0 if none).
  - the table: raised (number, starts 0); hidden from all players. Scratch: 1 if the active player raised this turn.
  - the table: prince_target (number, starts 0); hidden from all players. Scratch: seat targeted by a Prince this turn (0 if none).
  - parameters, each kept as a table attribute: deck_size = 16, guard_count = 5, guard_rank = 1, priest_count = 2, priest_rank = 2, baron_count = 2, baron_rank = 3, handmaid_count = 2, handmaid_rank = 4, prince_count = 2, prince_rank = 5, king_count = 1, king_rank = 6, countess_count = 1, countess_rank = 7, princess_count = 1, princess_rank = 8, total_rounds = 40, cards_out_of_play = 5, cards_dealt_each = 1, deck_after_deal = 9, base_stake = 1, raised_stake = 2, fold_points = 1, guard_guess_min = 2, guard_guess_max = 8, showdown_deck_threshold = 1, raise_min_deck = 2, starting_points = 0, starting_starter_seat = 1

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Every player starts with points 0, empty hand and discards, protected 0 and eliminated 0.
  2. Set starter_seat = 1, active_seat = 1, round_number = 1, new_hand = 1 and stake = 1.
  3. No cards are dealt in setup. The first hand is dealt by the NEW HAND step of round 1.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] table. What happens: When new_hand = 1: empty both players' hand and discards. Clear out_of_play. Copy full_deck into deck and shuffle it. Move the top 5 cards of deck into out_of_play (public). Deal 1 card from the top of deck to each player's hand. Move the bottom card of deck into reserve, leaving deck with 8 cards and reserve with 1. Set deck_count = 9, protected = 0 and eliminated = 0 for both players, stake = 1, folded = 0, active_seat = starter_seat and new_hand = 0. Announce out_of_play to everyone.
  2. [update] active seat. What happens: Reset guard_guess = 0, raised = 0, prince_target = 0. Set the active player's protected = 0. Move the top card of deck into the active player's hand (never the reserve). Set deck_count = len(deck) + len(reserve).
  3. [sync] all players. What happens: Each player sees their own hand and all public attributes.
  4. [ask] active seat answers: one rank from the active player's hand (see offers). What happens: The chosen rank is held for the next step. Prompt: 'Choose one of your two cards to discard.'
  5. [update] active seat. What happens: If the active hand contains 7 together with 5 or 6, the discarded card is 7 whatever was chosen. Remove that card from the active hand, append it to the active player's discards and set current_discard to it. Announce 'Seat {active_seat} discards {card name}'.
  6. [ask] active seat answers: a whole number from 2 to 8. What happens: When current_discard = 1 and the opponent's protected = 0: set guard_guess to the named rank and announce the named rank to both players.
  7. [update] table. What happens: When guard_guess >= 2: if the opponent's hand card equals guard_guess, set the opponent's eliminated = 1 and announce 'Hit: {card name}'. Otherwise announce 'Miss'.
  8. [tell] active seat only. What happens: When current_discard = 2 and the opponent's protected = 0: privately tell the active player the opponent's hand card.
  9. [update] table. What happens: When current_discard = 3 and the opponent's protected = 0: compare the active hand card with the opponent's hand card. The holder of the lower rank gets eliminated = 1 and their card is announced. On equal ranks nothing happens and nothing is revealed.
  10. [update] active seat. What happens: When current_discard = 4: set the active player's protected = 1.
  11. [update] table. What happens: When current_discard = 5: prince_target = the opponent if the opponent's protected = 0, otherwise the active seat. Move the target's hand card to the target's discards and announce it. If that card is 8, set the target's eliminated = 1.
  12. [update] prince target. What happens: When prince_target > 0 and the target's eliminated = 0: move the top card of deck into the target's hand, or the reserve card if deck is empty. Set deck_count = len(deck) + len(reserve).
  13. [update] both players. What happens: When current_discard = 6 and the opponent's protected = 0: swap the active player's hand with the opponent's hand.
  14. [update] active seat. What happens: When current_discard = 8: set the active player's eliminated = 1.
  15. [sync] all players. What happens: Each player sees their own (possibly swapped or redrawn) hand and all public attributes.
  16. [ask] active seat answers: raise | pass. What happens: When stake = 1, both players' eliminated = 0, deck_count >= 2 and the opponent's discards has at least 1 card: prompt 'Raise this hand's stake to 2, or pass?' On raise, set raised = 1 and announce the raise.
  17. [ask] opponent of the active seat answers: accept | fold. What happens: When raised = 1: prompt 'Accept (the stake becomes 2) or fold?' On accept, set stake = 2. On fold, set folded = 1. Announce the answer.
  18. [update] table. What happens: HAND END, first that holds: (a) if folded = 1, the active player's points += 1; (b) else if a player has eliminated = 1, the other player's points += stake; (c) else if deck_count <= 1 or round_number = 40, reveal both hand cards and the higher rank's points += stake, with no score on equal ranks. If (a), (b) or (c) applied, set new_hand = 1 and starter_seat = 3 - starter_seat, and announce the result.
  19. [update] table. What happens: If new_hand = 1, set active_seat = starter_seat. Otherwise set active_seat = 3 - active_seat. Then round_number += 1.
  20. [check] table. What happens: End the game if round_number > 40, otherwise continue.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When a new hand starts, the 16-card deck (5 Guard, 2 Priest, 2 Baron, 2 Handmaid, 2 Prince, 1 King, 1 Countess, 1 Princess) is shuffled, 5 cards go face up to out_of_play, each player gets 1 card, and deck_count = 9.
  R2. When a new hand starts, both players' discards are emptied, protected = 0, eliminated = 0, stake = 1, and the active seat becomes the starter seat.
  R3. When a turn starts, the active player's protected becomes 0 and they draw the top card, holding 2 cards, and deck_count falls by 1.
  R4. The bottom (reserve) card is never drawn at the start of a turn.
  R5. When the active player chooses a discard, that card moves from their hand to their discards and is announced as 'Seat X discards CARD'.
  R6. When the active player holds the Countess (7) with a King (6) or Prince (5), the Countess is discarded whatever was chosen.
  R7. When a Guard (1) is discarded and the opponent is not protected, the active player names a rank from 2 to 8, which is announced.
  R8. When the named Guard rank equals the opponent's card, the opponent is eliminated and 'Hit: CARD' is announced; otherwise 'Miss' is announced.
  R9. When a Priest (2) is discarded and the opponent is not protected, only the active player is told the opponent's card.
  R10. When a Baron (3) is discarded and the opponent is not protected, the lower hand card's holder is eliminated and their card announced; on equal ranks nothing happens and nothing is revealed.
  R11. When a Handmaid (4) is discarded, the active player's protected becomes 1 until their next turn starts.
  R12. When a Prince (5) is discarded, the opponent (or the active player if the opponent is protected) discards their hand card face up with no effect, and it is announced.
  R13. When a Prince makes a player discard the Princess (8), that player is eliminated.
  R14. When a Prince target is not eliminated, they draw the top card, taking the reserve only if it is the last card.
  R15. When a King (6) is discarded and the opponent is not protected, the two players swap hand cards.
  R16. When the Princess (8) is discarded, the active player is eliminated.
  R17. Cards targeting the opponent (Guard, Priest, Baron, King) have no effect when the opponent's protected = 1.
  R18. When stake = 1, nobody is eliminated, deck_count >= 2 and the opponent has at least 1 discard, the active player may raise or pass.
  R19. When the active player raises, the opponent accepts (stake = 2) or folds (folded = 1).
  R20. When the opponent folds, the active player gains 1 point and the hand ends.
  R21. When a player is eliminated and nobody folded, the other player gains points equal to the stake and the hand ends.
  R22. When nobody folded or was eliminated and deck_count <= 1 or it is round 40, both cards are revealed and the higher rank gains the stake; equal ranks score nothing.
  R23. When a hand ends, the starter seat switches and the new starter takes the next turn; otherwise the turn passes to the opponent.
  R24. After round 40 the game ends and the player with more points wins; equal points is a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Choose one of your two cards to discard | asked: active seat | options: Holding 7 together with 5 or 6: only 7. Otherwise: either of the two ranks in hand (one option if both are equal).
  - Guard guess | asked: active seat, only when a Guard was discarded and the opponent is not protected | options: a whole number 2 to 8
  - Raise this hand's stake to 2, or pass? | asked: active seat, only when stake = 1, nobody is eliminated, deck_count >= 2 and the opponent has at least 1 discard | options: raise, pass
  - Accept (the stake becomes 2) or fold? | asked: the opponent, only right after a raise | options: accept, fold

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round_number > 40
  - each player's standing: you.points (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: After exactly 40 rounds, the player with more points wins. Equal points share the win, which is the draw.
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

- each player: `discards` (list, visible: public, starts []): Ranks this player discarded this hand, in order.
- each player: `points` (number, visible: public, starts 0): Score.
- each player: `protected` (number, visible: public, starts 0): 1 if protected by a Handmaid until this player's next turn starts.
- each player: `eliminated` (number, visible: public, starts 0): 1 if knocked out of the current hand.
- the table: `deck_count` (number, visible: public, starts 0): Cards left in the deck: length of deck plus length of reserve.
- the table: `out_of_play` (list, visible: public, starts []): The 5 cards set aside face up at the start of each hand.
- the table: `stake` (number, visible: public, starts 1): Points the current hand is worth.
- the table: `round_number` (number, visible: public, starts 1): Current round (turn), 1 to 40.
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 16, guard_count = 5, guard_rank = 1, priest_count = 2, priest_rank = 2, baron_count = 2, baron_rank = 3, handmaid_count = 2, handmaid_rank = 4, prince_count = 2, prince_rank = 5, king_count = 1, king_rank = 6, countess_count = 1, countess_rank = 7, princess_count = 1, princess_rank = 8, total_rounds = 40, cards_out_of_play = 5, cards_dealt_each = 1, deck_after_deal = 9, base_stake = 1, raised_stake = 2, fold_points = 1, guard_guess_min = 2, guard_guess_max = 8, showdown_deck_threshold = 1, raise_min_deck = 2, starting_points = 0, starting_starter_seat = 1
- the game ends with ONE ending whose `rank_by` is `you.points`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
    "id": "love_letter_short_hands",
    "name": "Love Letter: Short Hands",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "blurb": "Two-player Love Letter over exactly 40 turns: draw, discard a card to use its effect, knock out the rival or win the showdown, and optionally raise a hand's stake to 2."
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
        "key": "discards",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "protected",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "eliminated",
        "visible": "public",
        "type": "number",
        "initial": 0
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
        "key": "full_deck",
        "visible": "none",
        "type": "list",
        "initial": [1, 1, 1, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 7, 8]
      },
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "reserve",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "shuffle",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "card_names",
        "visible": "none",
        "type": "list",
        "initial": ["none", "Guard", "Priest", "Baron", "Handmaid", "Prince", "King", "Countess", "Princess"]
      },
      {
        "key": "deck_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "out_of_play",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "stake",
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
        "key": "starter_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "round_number",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "new_hand",
        "visible": "none",
        "type": "number",
        "initial": 1
      },
      {
        "key": "folded",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "current_discard",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "guard_guess",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "raised",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "prince_target",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "end_kind",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "disc_name",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "opp_name",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "msg",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "msg2",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 16
      },
      {
        "key": "guard_count",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "guard_rank",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "priest_count",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "priest_rank",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "baron_count",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "baron_rank",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "handmaid_count",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "handmaid_rank",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "prince_count",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "prince_rank",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "king_count",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "king_rank",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "countess_count",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "countess_rank",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "princess_count",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "princess_rank",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "total_rounds",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "cards_out_of_play",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "cards_dealt_each",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "deck_after_deal",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "base_stake",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "raised_stake",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "fold_points",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "guard_guess_min",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "guard_guess_max",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "showdown_deck_threshold",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "raise_min_deck",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "starting_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "starting_starter_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "players start",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "points",
            "value": {
              "calc": "starting_points"
            }
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
            "key": "discards",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "protected",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "eliminated",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "table starts",
      "do": [
        {
          "set": {
            "key": "starter_seat",
            "value": {
              "calc": "starting_starter_seat"
            }
          }
        },
        {
          "set": {
            "key": "active_seat",
            "value": {
              "calc": "starting_starter_seat"
            }
          }
        },
        {
          "set": {
            "key": "round_number",
            "value": 1
          }
        },
        {
          "set": {
            "key": "new_hand",
            "value": 1
          }
        },
        {
          "set": {
            "key": "stake",
            "value": {
              "calc": "base_stake"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "label": "no deal yet",
      "to": "all",
      "text": "No cards are dealt yet. The first hand is dealt at the start of round 1, and seat {starter_seat} starts it."
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "deal",
      "label": "new hand",
      "when": {
        "calc": "new_hand == 1"
      },
      "do": [
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
            "key": "discards",
            "value": []
          }
        },
        {
          "set": {
            "key": "out_of_play",
            "value": []
          }
        },
        {
          "set": {
            "key": "shuffle",
            "value": {
              "calc": "sorted([[uniform(0, 1000000), c] for c in full_deck])"
            }
          }
        },
        {
          "set": {
            "key": "out_of_play",
            "value": {
              "calc": "[p[1] for p in shuffle if p[0] < shuffle[cards_out_of_play][0]]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "[shuffle[cards_out_of_play + you.seat - 1][1]]"
            }
          }
        },
        {
          "set": {
            "key": "reserve",
            "value": {
              "calc": "[shuffle[deck_size - 1][1]]"
            }
          }
        },
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "[p[1] for p in shuffle if p[0] > shuffle[cards_out_of_play + len(players) * cards_dealt_each - 1][0] and p[0] < shuffle[deck_size - 1][0]]"
            }
          }
        },
        {
          "set": {
            "key": "deck_count",
            "value": {
              "calc": "len(deck) + len(reserve)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "protected",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "eliminated",
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
            "key": "stake",
            "value": {
              "calc": "base_stake"
            }
          }
        },
        {
          "set": {
            "key": "folded",
            "value": 0
          }
        },
        {
          "set": {
            "key": "active_seat",
            "value": {
              "calc": "starter_seat"
            }
          }
        },
        {
          "set": {
            "key": "new_hand",
            "value": 0
          }
        }
      ],
      "text": "A new hand begins. Seat {active_seat} starts; the stake is {stake}. Set aside face up (out of play): {out_of_play}. Cards in the deck: {deck_count}."
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "start of turn",
      "do": [
        {
          "set": {
            "key": "guard_guess",
            "value": 0
          }
        },
        {
          "set": {
            "key": "raised",
            "value": 0
          }
        },
        {
          "set": {
            "key": "prince_target",
            "value": 0
          }
        },
        {
          "set": {
            "player": {
              "calc": "active_seat"
            },
            "key": "protected",
            "value": 0
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[0]"
            }
          }
        },
        {
          "append": {
            "player": {
              "calc": "active_seat"
            },
            "key": "hand",
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
            "key": "deck_count",
            "value": {
              "calc": "len(deck) + len(reserve)"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == active_seat"
            },
            "key": "offer",
            "value": {
              "calc": "[countess_rank] if (countess_rank in you.hand and (king_rank in you.hand or prince_rank in you.hand)) else ([you.hand[0]] if you.hand[0] == you.hand[1] else you.hand)"
            }
          }
        }
      ],
      "text": "Round {round_number}: seat {active_seat} draws a card. Cards left in the deck: {deck_count}."
    },
    {
      "use": "sync",
      "phase": "turn",
      "label": "your hand",
      "mode": "self",
      "to": "all",
      "text": "Your state now:"
    },
    {
      "use": "ask",
      "phase": "turn",
      "label": "discard",
      "when": {
        "calc": "len(players[active_seat - 1].offer) > 1"
      },
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "chosen"
      },
      "text": "Choose one of your two cards to discard. Answer with its rank (1 Guard, 2 Priest, 3 Baron, 4 Handmaid, 5 Prince, 6 King, 7 Countess, 8 Princess). Its effect happens at once; you keep the other card."
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "resolve discard",
      "do": [
        {
          "set": {
            "key": "current_discard",
            "value": {
              "calc": "players[active_seat - 1].offer[0]"
            },
            "if": {
              "calc": "len(players[active_seat - 1].offer) == 1"
            }
          }
        },
        {
          "set": {
            "key": "current_discard",
            "value": {
              "calc": "countess_rank if (countess_rank in players[active_seat - 1].hand and (king_rank in players[active_seat - 1].hand or prince_rank in players[active_seat - 1].hand)) else int($chosen)"
            },
            "if": {
              "calc": "len(players[active_seat - 1].offer) > 1"
            }
          }
        },
        {
          "remove": {
            "player": {
              "calc": "active_seat"
            },
            "key": "hand",
            "value": {
              "calc": "current_discard"
            }
          }
        },
        {
          "append": {
            "player": {
              "calc": "active_seat"
            },
            "key": "discards",
            "value": {
              "calc": "current_discard"
            }
          }
        },
        {
          "set": {
            "key": "disc_name",
            "value": {
              "calc": "card_names[current_discard]"
            }
          }
        },
        {
          "set": {
            "key": "opp_name",
            "value": {
              "calc": "card_names[players[2 - active_seat].hand[0]]"
            }
          }
        }
      ],
      "text": "Seat {active_seat} discards {disc_name}."
    },
    {
      "use": "ask",
      "phase": "effect",
      "label": "guard guess",
      "when": {
        "calc": "current_discard == guard_rank and players[2 - active_seat].protected == 0"
      },
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "guard_guess_min"
        },
        "max": {
          "calc": "guard_guess_max"
        }
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "guard_guess",
              "value": "$answer"
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} names rank {value} with the Guard."
      },
      "text": "Guard: name a rank from {guard_guess_min} to {guard_guess_max}. If your opponent's card has that rank, they are eliminated from the hand; otherwise nothing happens."
    },
    {
      "use": "update",
      "phase": "effect",
      "label": "guard check",
      "when": {
        "calc": "guard_guess >= guard_guess_min"
      },
      "do": [
        {
          "set": {
            "key": "msg",
            "value": {
              "calc": "card_names[players[2 - active_seat].hand[0]]"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "3 - active_seat"
            },
            "key": "eliminated",
            "value": 1,
            "if": {
              "calc": "players[2 - active_seat].hand[0] == guard_guess"
            },
            "text": "Hit: {msg}. Seat {player} is eliminated from the hand."
          }
        },
        {
          "set_status": {
            "player": {
              "calc": "3 - active_seat"
            },
            "to": "out",
            "if": {
              "calc": "players[2 - active_seat].hand[0] == guard_guess"
            }
          }
        },
        {
          "set": {
            "key": "msg",
            "value": "Miss",
            "if": {
              "calc": "players[2 - active_seat].hand[0] != guard_guess"
            },
            "text": "Miss."
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "effect",
      "label": "priest",
      "when": {
        "calc": "current_discard == priest_rank and players[2 - active_seat].protected == 0"
      },
      "to": {
        "where": "you.seat == active_seat"
      },
      "text": "Priest: your opponent's card is {opp_name}."
    },
    {
      "use": "update",
      "phase": "effect",
      "label": "baron",
      "when": {
        "calc": "current_discard == baron_rank and players[2 - active_seat].protected == 0"
      },
      "do": [
        {
          "set": {
            "key": "msg",
            "value": {
              "calc": "card_names[players[active_seat - 1].hand[0]]"
            },
            "if": {
              "calc": "players[active_seat - 1].hand[0] < players[2 - active_seat].hand[0]"
            }
          }
        },
        {
          "set": {
            "key": "msg",
            "value": {
              "calc": "card_names[players[2 - active_seat].hand[0]]"
            },
            "if": {
              "calc": "players[2 - active_seat].hand[0] < players[active_seat - 1].hand[0]"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "active_seat"
            },
            "key": "eliminated",
            "value": 1,
            "if": {
              "calc": "players[active_seat - 1].hand[0] < players[2 - active_seat].hand[0]"
            },
            "text": "Baron: seat {player} has the lower card, {msg}, and is eliminated from the hand."
          }
        },
        {
          "set": {
            "player": {
              "calc": "3 - active_seat"
            },
            "key": "eliminated",
            "value": 1,
            "if": {
              "calc": "players[2 - active_seat].hand[0] < players[active_seat - 1].hand[0]"
            },
            "text": "Baron: seat {player} has the lower card, {msg}, and is eliminated from the hand."
          }
        },
        {
          "set_status": {
            "player": {
              "calc": "active_seat"
            },
            "to": "out",
            "if": {
              "calc": "players[active_seat - 1].hand[0] < players[2 - active_seat].hand[0]"
            }
          }
        },
        {
          "set_status": {
            "player": {
              "calc": "3 - active_seat"
            },
            "to": "out",
            "if": {
              "calc": "players[2 - active_seat].hand[0] < players[active_seat - 1].hand[0]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "effect",
      "label": "handmaid",
      "when": {
        "calc": "current_discard == handmaid_rank"
      },
      "do": [
        {
          "set": {
            "player": {
              "calc": "active_seat"
            },
            "key": "protected",
            "value": 1,
            "text": "Seat {player} is protected until their next turn starts."
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "effect",
      "label": "prince discard",
      "when": {
        "calc": "current_discard == prince_rank"
      },
      "do": [
        {
          "set": {
            "key": "prince_target",
            "value": {
              "calc": "(3 - active_seat) if players[2 - active_seat].protected == 0 else active_seat"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "players[prince_target - 1].hand[0]"
            }
          }
        },
        {
          "set": {
            "key": "msg",
            "value": {
              "calc": "card_names[pick]"
            }
          }
        },
        {
          "remove": {
            "player": {
              "calc": "prince_target"
            },
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "append": {
            "player": {
              "calc": "prince_target"
            },
            "key": "discards",
            "value": {
              "calc": "pick"
            },
            "text": "Prince: seat {player} discards {msg} face up, with no effect."
          }
        },
        {
          "set": {
            "player": {
              "calc": "prince_target"
            },
            "key": "eliminated",
            "value": 1,
            "if": {
              "calc": "pick == princess_rank"
            },
            "text": "Seat {player} discarded the Princess and is eliminated from the hand."
          }
        },
        {
          "set_status": {
            "player": {
              "calc": "prince_target"
            },
            "to": "out",
            "if": {
              "calc": "pick == princess_rank"
            }
      
... (cut)

Why it was refused: the game file was refused by the loader: love_letter: steps[6].do[3].text: 'Miss.' is neither a declared template nor a sentence. Write the words here, or add 'Miss.' to the `text` block.
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "love_letter_short_hands",
    "name": "Love Letter: Short Hands",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "blurb": "Two-player Love Letter over exactly 40 turns: draw, discard a card to use its effect, knock out the rival or win the showdown, and optionally raise a hand's stake to 2."
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
        "key": "discards",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "protected",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "eliminated",
        "visible": "public",
        "type": "number",
        "initial": 0
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
        "key": "full_deck",
        "visible": "none",
        "type": "list",
        "initial": [1, 1, 1, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 7, 8]
      },
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "reserve",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "shuffle",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "card_names",
        "visible": "none",
        "type": "list",
        "initial": ["none", "Guard", "Priest", "Baron", "Handmaid", "Prince", "King", "Countess", "Princess"]
      },
      {
        "key": "deck_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "out_of_play",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "stake",
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
        "key": "starter_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "round_number",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "new_hand",
        "visible": "none",
        "type": "number",
        "initial": 1
      },
      {
        "key": "folded",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "current_discard",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "guard_guess",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "raised",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "prince_target",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "end_kind",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "disc_name",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "opp_name",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "msg",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "msg2",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 16
      },
      {
        "key": "guard_count",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "guard_rank",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "priest_count",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "priest_rank",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "baron_count",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "baron_rank",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "handmaid_count",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "handmaid_rank",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "prince_count",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "prince_rank",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "king_count",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "king_rank",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "countess_count",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "countess_rank",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "princess_count",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "princess_rank",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "total_rounds",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "cards_out_of_play",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "cards_dealt_each",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "deck_after_deal",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "base_stake",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "raised_stake",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "fold_points",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "guard_guess_min",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "guard_guess_max",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "showdown_deck_threshold",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "raise_min_deck",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "starting_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "starting_starter_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "players start",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "points",
            "value": {
              "calc": "starting_points"
            }
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
            "key": "discards",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "protected",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "eliminated",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "table starts",
      "do": [
        {
          "set": {
            "key": "starter_seat",
            "value": {
              "calc": "starting_starter_seat"
            }
          }
        },
        {
          "set": {
            "key": "active_seat",
            "value": {
              "calc": "starting_starter_seat"
            }
          }
        },
        {
          "set": {
            "key": "round_number",
            "value": 1
          }
        },
        {
          "set": {
            "key": "new_hand",
            "value": 1
          }
        },
        {
          "set": {
            "key": "stake",
            "value": {
              "calc": "base_stake"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "label": "no deal yet",
      "to": "all",
      "text": "No cards are dealt yet. The first hand is dealt at the start of round 1, and seat {starter_seat} starts it."
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "deal",
      "label": "new hand",
      "when": {
        "calc": "new_hand == 1"
      },
      "do": [
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
            "key": "discards",
            "value": []
          }
        },
        {
          "set": {
            "key": "out_of_play",
            "value": []
          }
        },
        {
          "set": {
            "key": "shuffle",
            "value": {
              "calc": "sorted([[uniform(0, 1000000), c] for c in full_deck])"
            }
          }
        },
        {
          "set": {
            "key": "out_of_play",
            "value": {
              "calc": "[p[1] for p in shuffle if p[0] < shuffle[cards_out_of_play][0]]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "[shuffle[cards_out_of_play + you.seat - 1][1]]"
            }
          }
        },
        {
          "set": {
            "key": "reserve",
            "value": {
              "calc": "[shuffle[deck_size - 1][1]]"
            }
          }
        },
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "[p[1] for p in shuffle if p[0] > shuffle[cards_out_of_play + len(players) * cards_dealt_each - 1][0] and p[0] < shuffle[deck_size - 1][0]]"
            }
          }
        },
        {
          "set": {
            "key": "deck_count",
            "value": {
              "calc": "len(deck) + len(reserve)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "protected",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "eliminated",
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
            "key": "stake",
            "value": {
              "calc": "base_stake"
            }
          }
        },
        {
          "set": {
            "key": "folded",
            "value": 0
          }
        },
        {
          "set": {
            "key": "active_seat",
            "value": {
              "calc": "starter_seat"
            }
          }
        },
        {
          "set": {
            "key": "new_hand",
            "value": 0
          }
        }
      ],
      "text": "A new hand begins. Seat {active_seat} starts; the stake is {stake}. Set aside face up (out of play): {out_of_play}. Cards in the deck: {deck_count}."
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "start of turn",
      "do": [
        {
          "set": {
            "key": "guard_guess",
            "value": 0
          }
        },
        {
          "set": {
            "key": "raised",
            "value": 0
          }
        },
        {
          "set": {
            "key": "prince_target",
            "value": 0
          }
        },
        {
          "set": {
            "player": {
              "calc": "active_seat"
            },
            "key": "protected",
            "value": 0
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[0]"
            }
          }
        },
        {
          "append": {
            "player": {
              "calc": "active_seat"
            },
            "key": "hand",
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
            "key": "deck_count",
            "value": {
              "calc": "len(deck) + len(reserve)"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == active_seat"
            },
            "key": "offer",
            "value": {
              "calc": "[countess_rank] if (countess_rank in you.hand and (king_rank in you.hand or prince_rank in you.hand)) else ([you.hand[0]] if you.hand[0] == you.hand[1] else you.hand)"
            }
          }
        }
      ],
      "text": "Round {round_number}: seat {active_seat} draws a card. Cards left in the deck: {deck_count}."
    },
    {
      "use": "sync",
      "phase": "turn",
      "label": "your hand",
      "mode": "self",
      "to": "all",
      "text": "Your state now:"
    },
    {
      "use": "ask",
      "phase": "turn",
      "label": "discard",
      "when": {
        "calc": "len(players[active_seat - 1].offer) > 1"
      },
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "chosen"
      },
      "text": "Choose one of your two cards to discard. Answer with its rank (1 Guard, 2 Priest, 3 Baron, 4 Handmaid, 5 Prince, 6 King, 7 Countess, 8 Princess). Its effect happens at once; you keep the other card."
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "resolve discard",
      "do": [
        {
          "set": {
            "key": "current_discard",
            "value": {
              "calc": "players[active_seat - 1].offer[0]"
            },
            "if": {
              "calc": "len(players[active_seat - 1].offer) == 1"
            }
          }
        },
        {
          "set": {
            "key": "current_discard",
            "value": {
              "calc": "countess_rank if (countess_rank in players[active_seat - 1].hand and (king_rank in players[active_seat - 1].hand or prince_rank in players[active_seat - 1].hand)) else int($chosen)"
            },
            "if": {
              "calc": "len(players[active_seat - 1].offer) > 1"
            }
          }
        },
        {
          "remove": {
            "player": {
              "calc": "active_seat"
            },
            "key": "hand",
            "value": {
              "calc": "current_discard"
            }
          }
        },
        {
          "append": {
            "player": {
              "calc": "active_seat"
            },
            "key": "discards",
            "value": {
              "calc": "current_discard"
            }
          }
        },
        {
          "set": {
            "key": "disc_name",
            "value": {
              "calc": "card_names[current_discard]"
            }
          }
        },
        {
          "set": {
            "key": "opp_name",
            "value": {
              "calc": "card_names[players[2 - active_seat].hand[0]]"
            }
          }
        }
      ],
      "text": "Seat {active_seat} discards {disc_name}."
    },
    {
      "use": "ask",
      "phase": "effect",
      "label": "guard guess",
      "when": {
        "calc": "current_discard == guard_rank and players[2 - active_seat].protected == 0"
      },
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "guard_guess_min"
        },
        "max": {
          "calc": "guard_guess_max"
        }
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "guard_guess",
              "value": "$answer"
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} names rank {value} with the Guard."
      },
      "text": "Guard: name a rank from {guard_guess_min} to {guard_guess_max}. If your opponent's card has that rank, they are eliminated from the hand; otherwise nothing happens."
    },
    {
      "use": "update",
      "phase": "effect",
      "label": "guard check",
      "when": {
        "calc": "guard_guess >= guard_guess_min"
      },
      "do": [
        {
          "set": {
            "key": "msg",
            "value": {
              "calc": "card_names[players[2 - active_seat].hand[0]]"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "3 - active_seat"
            },
            "key": "eliminated",
            "value": 1,
            "if": {
              "calc": "players[2 - active_seat].hand[0] == guard_guess"
            },
            "text": "Hit: {msg}. Seat {player} is eliminated from the hand."
          }
        },
        {
          "set_status": {
            "player": {
              "calc": "3 - active_seat"
            },
            "to": "out",
            "if": {
              "calc": "players[2 - active_seat].hand[0] == guard_guess"
            }
          }
        },
        {
          "set": {
            "key": "msg2",
            "value": "Miss",
            "if": {
              "calc": "players[2 - active_seat].hand[0] != guard_guess"
            },
            "text": "Guard result: Miss. The named rank was wrong."
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "effect",
      "label": "priest",
      "when": {
        "calc": "current_discard == priest_rank and players[2 - active_seat].protected == 0"
      },
      "to": {
        "where": "you.seat == active_seat"
      },
      "text": "Priest: your opponent's card is {opp_name}."
    },
    {
      "use": "update",
      "phase": "effect",
      "label": "baron",
      "when": {
        "calc": "current_discard == baron_rank and players[2 - active_seat].protected == 0"
      },
      "do": [
        {
          "set": {
            "key": "msg",
            "value": {
              "calc": "card_names[players[active_seat - 1].hand[0]]"
            },
            "if": {
              "calc": "players[active_seat - 1].hand[0] < players[2 - active_seat].hand[0]"
            }
          }
        },
        {
          "set": {
            "key": "msg",
            "value": {
              "calc": "card_names[players[2 - active_seat].hand[0]]"
            },
            "if": {
              "calc": "players[2 - active_seat].hand[0] < players[active_seat - 1].hand[0]"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "active_seat"
            },
            "key": "eliminated",
            "value": 1,
            "if": {
              "calc": "players[active_seat - 1].hand[0] < players[2 - active_seat].hand[0]"
            },
            "text": "Baron: seat {player} has the lower card, {msg}, and is eliminated from the hand."
          }
        },
        {
          "set": {
            "player": {
              "calc": "3 - active_seat"
            },
            "key": "eliminated",
            "value": 1,
            "if": {
              "calc": "players[2 - active_seat].hand[0] < players[active_seat - 1].hand[0]"
            },
            "text": "Baron: seat {player} has the lower card, {msg}, and is eliminated from the hand."
          }
        },
        {
          "set_status": {
            "player": {
              "calc": "active_seat"
            },
            "to": "out",
            "if": {
              "calc": "players[active_seat - 1].eliminated == 1"
            }
          }
        },
        {
          "set_status": {
            "player": {
              "calc": "3 - active_seat"
            },
            "to": "out",
            "if": {
              "calc": "players[2 - active_seat].eliminated == 1"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "effect",
      "label": "handmaid",
      "when": {
        "calc": "current_discard == handmaid_rank"
      },
      "do": [
        {
          "set": {
            "player": {
              "calc": "active_seat"
            },
            "key": "protected",
            "value": 1,
            "text": "Seat {player} is protected until their next turn starts."
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "effect",
      "label": "prince discard",
      "when": {
        "calc": "current_discard == prince_rank"
      },
      "do": [
        {
          "set": {
            "key": "prince_target",
            "value": {
              "calc": "(3 - active_seat) if players[2 - active_seat].protected == 0 else active_seat"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "players[prince_target - 1].hand[0]"
            }
          }
        },
        {
          "set": {
            "key": "msg",
            "value": {
              "calc": "card_names[pick]"
            }
          }
        },
        {
          "remove": {
            "player": {
              "calc": "prince_target"
            },
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "append": {
            "player": {
              "calc": "prince_target"
            },
            "key": "discards",
            "value": {
              "calc": "pick"
            },
            "text": "Prince: seat {player} discards {msg} face up, with no effect."
          }
        },
        {
          "set": {
            "player": {
              "calc": "prince_target"
            },
            "key": "eliminated",
            "value": 1,
            "if": {
              "calc": "pick == princess_rank"
            },
            "text": "Seat {player} discarded the Princess and is eliminated from the hand."
          }
        },
        {
          "set_status": {
            "player": {
              "calc": "prince_target"
            },
            "to": "out",
            "if": {
              "calc": "pick == princess_rank"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "effect",
      "label": "prince redraw",
      "when": {
        "calc": "prince_target > 0 and players[prince_target - 1].eliminated == 0"
      },
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[0] if len(deck) > 0 else reserve[0]"
            }
          }
        },
        {
          "append": {
            "player": {
              "calc": "prince_target"
            },
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "reserve",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(deck) == 0"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(deck) > 0"
            }
          }
        },
        {
          "set": {
            "key": "deck_count",
            "value": {
              "calc": "len(deck) + len(reserve)"
            }
          }
        }
      ],
      "text": "Seat {prince_target} draws a new card. Cards left in the deck: {deck_count}."
    },
    {
      "use": "update",
      "phase": "effect",
      "label": "king",
      "when": {
        "calc": "current_discard == king_rank and players[2 - active_seat].protected == 0"
      },
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "players[active_seat - 1].hand[0]"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "active_seat"
            },
            "key": "hand",
            "value": {
              "calc": "players[2 - active_seat].hand"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "3 - active_seat"
            },
            "key": "hand",
            "value": {
              "calc": "[pick]"
            }
          }
        }
      ],
      "text": "King: seats 1 and 2 swap hand cards."
    },
    {
      "use": "update",
      "phase": "effect",
      "label": "princess",
      "when": {
        "calc": "current_discard == princess_rank"
      },
      "do": [
        {
          "set": {
            "player": {
              "calc": "active_seat"
            },
            "key": "eliminated",
            "value": 1,
            "text": "Seat {player} discarded the Princess and is eliminated from the hand."
          }
        },
        {
          "set_status": {
            "player": {
              "calc": "active_seat"
            },
            "to": "out"
          }
        }
      ]
    },
    {
      "use": "sync",
      "phase": "effect",
      "label": "after effects",
      "mode": "self",
      "to": "all",
      "text": "Your state after the effect:"
    },
    {
      "use": "ask",
      "phase": "stake",
      "label": "raise",
      "when": {
        "calc": "stake == base_stake and all(p.eliminated == 0 for p in players) and deck_count >= raise_min_deck and len(players[2 - active_seat].discards) >= 1"
      },
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "choice",
        "options": [
          "raise",
          "pass"
        ]
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "raised",
              "value": 1,
              "if": {
                "calc": "$answer == 'raise'"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} answers: {value}."
      },
      "text": "Raise this hand's stake to 2, or pass? If you raise, your opponent accepts (the stake becomes {raised_stake}) or folds (you gain {fold_points} point and the hand ends). If you pass, the stake stays {stake}."
    },
    {
      "use": "ask",
      "phase": "stake",
      "label": "response",
      "when": {
        "calc": "raised == 1"
      },
      "to": {
        "where": "you.seat == 3 - active_seat"
      },
      "answer": {
        "type": "choice",
        "options": [
          "accept",
          "fold"
        ]
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "stake",
              "value": {
                "calc": "raised_stake"
              },
              "if": {
                "calc": "$answer == 'accept'"
              }
            }
          },
          {
            "set": {
              "key": "folded",
              "value": 1,
              "if": {
                "calc": "$answer == 'fold'"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} answers the raise: {value}."
      },
      "text": "Accept (the stake becomes 2) or fold? If you accept, the hand goes on worth {raised_stake} points. If you fold, your opponent gains {fold_points} point and the hand ends."
    },
    {
      "use": "update",
      "phase": "end",
      "label": "hand end",
      "do": [
        {
          "set": {
            "key": "end_kind",
            "value": {
              "calc": "1 if folded == 1 else (2 if any(p.eliminated == 1 for p in players) else (3 if (deck_count <= showdown_deck_threshold or round_number == total_rounds) else 0))"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "active_seat"
            },
            "key": "points",
            "value": {
              "calc": "fold_points"
            },
            "if": {
              "calc": "end_kind == 1"
            },
            "text": "The raise was folded: seat {player} gains {fold_points} point and the hand ends."
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.eliminated == 0"
            },
            "key": "points",
            "value": {
              "calc": "stake"
            },
            "if": {
              "calc": "end_kind == 2"
            },
            "text": "Seat {player} wins the hand and gains {stake} points."
          }
        },
        {
          "set": {
            "key": "msg",
            "value": {
              "calc": "'seat 1 holds ' + card_names[players[0].hand[0]] + ', seat 2 holds ' + card_names[players[1].hand[0]]"
            },
            "if": {
              "calc": "end_kind == 3"
            },
            "text": "Showdown: {msg}."
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.hand[0] > players[2 - you.seat].hand[0]"
            },
            "key": "points",
            "value": {
              "calc": "stake"
            },
            "if": {
              "calc": "end_kind == 3"
            },
            "text": "Seat {player} has the higher card and gains {stake} points."
          }
        },
        {
          "set": {
            "key": "msg2",
            "value": "tie",
            "if": {
              "calc": "end_kind == 3 and players[0].hand[0] == players[1].hand[0]"
            },
            "text": "Equal ranks at the showdown: nobody scores this hand."
          }
        },
        {
          "set": {
            "key": "new_hand",
            "value": 1,
            "if": {
              "calc": "end_kind > 0"
            }
          }
        },
        {
          "set": {
            "key": "starter_seat",
            "value": {
              "calc": "3 - starter_seat"
            },
            "if": {
              "calc": "end_kind > 0"
            },
            "text": "The hand is over. Seat {starter_seat} starts the next hand."
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "end",
      "label": "pass turn",
      "do": [
        {
          "set": {
            "key": "active_seat",
            "value": {
              "calc": "starter_seat if new_hand == 1 else 3 - active_seat"
            }
          }
        },
        {
          "adjust": {
            "key": "round_number",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "end",
      "label": "after round 40",
      "when": {
        "calc": "round_number > total_rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round_number > total_rounds"
      },
      "rank_by": "you.points",
      "text": "Winner: {result}. Final points: Seat 1 {players[0].points}, Seat 2 {players[1].points}."
    }
  },
  "limits": {
    "rounds": 40,
    "rounds_max": 40,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "Two-player Love Letter over exactly {total_rounds} rounds. One round is one turn by the active player.\n\nCARDS ({deck_size}): {guard_count} Guard (rank {guard_rank}), {priest_count} Priest ({priest_rank}), {baron_count} Baron ({baron_rank}), {handmaid_count} Handmaid ({handmaid_rank}), {prince_count} Prince ({prince_rank}), {king_count} King ({king_rank}), {countess_count} Countess ({countess_rank}), {princess_count} Princess ({princess_rank}).\n\nNEW HAND: both hands and discards are emptied and out_of_play is cleared. The deck is shuffled, the top {cards_out_of_play} cards go face up into out_of_play, and each player is dealt {cards_dealt_each} card, so the deck holds {deck_after_deal} cards. The bottom card of the deck is the reserve: it is never drawn at the start of a turn. Both players are unprotected and not eliminated, the stake is {base_stake}, and the starter seat (seat {starting_starter_seat} for the first hand) takes the first turn.\n\nTURN: your protection ends and you draw the top card, so you hold 2. Choose one of your two cards to discard; its effect happens at once. If you hold the Countess together with a King or a Prince, the Countess is discarded whatever you chose. Everyone is told which card you discarded.\n- Guard: if your opponent is not protected, name a rank from {guard_guess_min} to {guard_guess_max}; it is announced. If their card has that rank they are eliminated and everyone is told 'Hit: CARD'; otherwise everyone is told 'Miss' and nothing happens.\n- Priest: if your opponent is not protected, only you are told their card.\n- Baron: if your opponent is not protected, compare hand cards. The holder of the lower rank is eliminated and their card is announced. On equal ranks nothing happens and nothing is revealed.\n- Handmaid: you are protected until your next turn starts.\n- Prince: the target is your opponent, or you if your opponent is protected. The target discards their hand card face up with no effect, and it is announced. If it is the Princess, the target is eliminated; otherwise the target takes the top card of the deck (the reserve only if it is the last card).\n- King: if your opponent is not protected, you swap hand cards.\n- Countess: no effect.\n- Princess: you are eliminated.\nGuard, Priest, Baron and King have no effect when the opponent is protected.\n\nRAISE: when the stake is {base_stake}, nobody is eliminated, at least {raise_min_deck} cards remain in the deck and your opponent has at least one card in their discards, you may raise the hand's stake to {raised_stake} or pass. After a raise your opponent accepts (the stake becomes {raised_stake}) or folds. If you pass, nothing changes.\n\nHAND END, the first that holds: (a) if the opponent folded, the active player gains {fold_points} point; (b) otherwise, if a player is eliminated, the other player gains points equal to the stake; (c) otherwise, if {showdown_deck_threshold} or fewer cards remain in the deck or this is round {total_rounds}, there is a showdown: both hand cards are revealed and the higher rank gains points equal to the stake; on equal ranks nobody scores. If a hand ended, the starter seat switches and the new starter takes the next turn. Otherwise the turn passes to the opponent.\n\nAfter round {total_rounds} the game ends. The player with more points wins; equal points is a draw (a shared win)."
}
```
````
