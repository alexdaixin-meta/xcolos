# 28 coder

- time: 2026-10-27T21:59:42+00:00 (205.2s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 80ae5ccdd6a4c55e, reply sha256 fff3f94b4fa6af9c

## Sent

````
# Task: write the XColos game file for "Little Two"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

CARDS. There are 30 cards, numbered 1 to 30. A card c has rank = floor((c+2)/3), from 1 to 10, and suit = c - 3*(rank-1), from 1 to 3. Rank 1 is lowest and rank 10 (cards 28, 29, 30) is highest and plays the role of the 2. Within a rank, a higher suit is a higher card, so a higher card number is always a higher card. Examples: card 13 has rank 5, suit 1; card 14 has rank 5, suit 2; card 16 has rank 6, suit 1.

PLAY KINDS. A play is 1 to 3 cards from your own hand, written as their numbers in ascending order separated by single spaces (for example '13 14').
- Single: 1 card.
- Pair: 2 cards of the same rank. '13 14' is a pair; '14 16' is not.
- Triple: 3 cards of the same rank.
- Run: 3 cards whose ranks are three consecutive numbers (for example ranks 4, 5, 6), in any suits. Ranks do not wrap around.
Any other set of cards is not a play. The value of a play is its highest card number.

SETUP. There are 3 players in seats 1, 2 and 3. Each player has a private hand, a public card_count, a public penalty (starting at 0), public deals_won (starting at 0) and a public last_action (starting as 'no play yet'). The table tracks deal_number (starting at 0), orbit (starting at 0), deal_active (starting false), leader_seat, first_orbit, pile_kind ('empty', 'single', 'pair', 'triple' or 'run'), pile_value and last_player (0 means nobody). The game lasts at most 40 orbits and at most 3 deals.

EACH ORBIT (one engine round):
1. Add 1 to orbit.
2. If deal_active is false and deal_number is less than 3, start a deal. Add 1 to deal_number. Shuffle all 30 cards. Deal 9 into each player's private hand and put the remaining 3 into a hidden aside list that nobody sees. Set every card_count to 9. Set leader_seat to deal_number, so seat 1 leads deal 1, seat 2 leads deal 2 and seat 3 leads deal 3. Set deal_active to true, first_orbit to true, pile_kind to 'empty', pile_value to 0 and last_player to the leader. This is the only random event in an orbit.
3. Seats then take turns in the order seat 1, seat 2, seat 3. A seat skips its turn if deal_active is false, or if first_orbit is true and its seat number is lower than leader_seat. On each turn that is not skipped:
  a. Clearance. If last_player equals this seat, the other two have passed since this seat's last play (or the deal has just started). Set pile_kind to 'empty' and pile_value to 0. This seat now leads.
  b. Options. The seat is offered exactly the following, and nothing else:
     - If pile_kind is 'empty': every single, pair, triple and run that can be made from its hand. Passing is not allowed.
     - If pile_kind is 'single': 'pass', every single with value greater than pile_value, and every triple of any value (a bomb).
     - If pile_kind is 'pair': 'pass', every pair with value greater than pile_value, and every triple of any value (a bomb).
     - If pile_kind is 'triple': 'pass' and every triple with value greater than pile_value.
     - If pile_kind is 'run': 'pass' and every run with value greater than pile_value.
  c. The seat chooses one option. Everyone sees the choice.
  d. Apply the choice. If it is 'pass', set this seat's last_action to 'pass' and change nothing else. Otherwise:
     - Split the option on spaces into all of its card numbers.
     - Remove every one of those cards from the hand.
     - Lower card_count by the number of cards played (1, 2 or 3).
     - Set pile_kind: 1 card is 'single'; 2 cards are 'pair'; 3 cards of one rank are 'triple'; 3 cards of consecutive ranks are 'run'.
     - Set pile_value to the highest card number played.
     - Set last_player to this seat.
     - Set last_action to the full option string.
     A triple that bombs a single or a pair makes pile_kind 'triple', so only a higher triple can follow it.
  e. If this seat's card_count is now 0, it wins the deal. Add 1 to its deals_won. Every other seat with n cards left adds a penalty of n, doubled to 2n if n is 7 or more, plus 1 for each card numbered 28, 29 or 30 still in its hand. Set deal_active to false. The rest of this orbit's turns are skipped.
4. At the end of the orbit, set first_orbit to false.

END. The game ends when deal 3 has ended, or when orbit 40 is complete. If orbit 40 ends while a deal is still active, every seat is penalised for the cards it holds, by the same formula. Deals that never started are not played.

There is no talk phase. All plays and passes are public, and hands and the aside cards stay hidden.

How the winner is decided: The player with the lowest total penalty wins. If two or three players tie for lowest, the one among them with the most deals_won wins. If they are still tied, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Little Two (3 to 3 players, best with 3)

A three-player climbing card game over up to 3 deals: shed your 9 cards by beating the pile with singles, pairs, triples or runs. Triples bomb singles and pairs. The lowest total penalty wins.

STATE (every item below must exist in the file):
  - each player: hand (list, starts []); only its owner sees it. card numbers (1-30) the player holds
  - each player: card_count (number, starts 0); everyone sees it. number of cards in hand
  - each player: penalty (number, starts 0); everyone sees it. total penalty points; lower is better
  - each player: deals_won (number, starts 0); everyone sees it. deals this player won by emptying their hand
  - each player: last_action (text, starts 'no play yet'); everyone sees it. 'pass' or the last play string, e.g. '13 14'
  - the table: deck (list, starts [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]); hidden from all players. undealt cards during a deal
  - the table: aside (list, starts []); hidden from all players. the 3 undealt cards set aside each deal, seen by nobody
  - the table: deal_number (number, starts 0); everyone sees it. number of deals started
  - the table: orbit (number, starts 0); everyone sees it. number of orbits (engine rounds) begun
  - the table: deal_active (bool, starts False); everyone sees it. whether a deal is in progress
  - the table: leader_seat (number, starts 0); everyone sees it. seat that leads the current deal (equals deal_number)
  - the table: first_orbit (bool, starts False); everyone sees it. true during the orbit in which a deal started
  - the table: pile_kind (text, starts 'empty'); everyone sees it. 'empty', 'single', 'pair', 'triple' or 'run'
  - the table: pile_value (number, starts 0); everyone sees it. highest card number of the play on top of the pile
  - the table: last_player (number, starts 0); everyone sees it. seat of the last non-pass play (0 = nobody)
  - parameters, each kept as a table attribute: deck_size = 30, ranks = 10, suits = 3, hand_size = 9, aside_size = 3, max_deals = 3, max_orbits = 40, double_penalty_threshold = 7, double_penalty_factor = 2, top_rank_card_low = 28, top_rank_card_high = 30, top_card_penalty = 1, min_play_cards = 1, max_play_cards = 3, run_length = 3, initial_penalty = 0, initial_deals_won = 0, deals_won_tiebreak_multiplier = 10

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seat the 3 players in seats 1, 2 and 3.
  2. Every player starts with an empty hand, card_count 0, penalty 0, deals_won 0 and last_action 'no play yet'.
  3. The table starts with deal_number 0, orbit 0, deal_active false, pile_kind 'empty', pile_value 0 and last_player 0.
  4. No cards are dealt in setup. The first deal starts in step 2 of orbit 1.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: orbit += 1
  2. [update] all players. What happens: Start a deal: deal_number += 1; set deck to cards 1..30, every hand to [] and aside to []; draw 9 random cards from deck into each player's hand (remove from deck, append to hand); move the remaining 3 deck cards into aside; every card_count = 9; leader_seat = deal_number; deal_active = true; first_orbit = true; pile_kind = 'empty'; pile_value = 0; last_player = leader_seat. Announce that deal {deal_number} has started and seat {leader_seat} leads.
  3. [sync] all players. What happens: each player privately sees their own hand and the public state
  4. [update] seat 1. What happens: Clearance: pile_kind = 'empty', pile_value = 0
  5. [ask] seat 1 answers: one option from the legal-play list built from seat 1's hand and the pile (see offers); the choice is shown to everyone. What happens: the chosen option is recorded for the next step
  6. [update] seat 1. What happens: If 'pass': seat1.last_action = 'pass'. Otherwise split the option on spaces into cards; remove each card from seat1.hand; seat1.card_count -= number of cards; pile_kind = 'single' if 1 card, 'pair' if 2, 'triple' if 3 of one rank, 'run' if 3 of consecutive ranks; pile_value = highest card; last_player = 1; seat1.last_action = option.
  7. [update] all players. What happens: seat1.deals_won += 1; for each other seat with n = card_count: penalty += n * (2 if n >= 7 else 1) + (number of cards in hand numbered 28, 29 or 30); deal_active = false
  8. [update] seat 2. What happens: Clearance: pile_kind = 'empty', pile_value = 0
  9. [ask] seat 2 answers: one option from the legal-play list built from seat 2's hand and the pile (see offers); the choice is shown to everyone. What happens: the chosen option is recorded for the next step
  10. [update] seat 2. What happens: If 'pass': seat2.last_action = 'pass'. Otherwise split the option on spaces into cards; remove each card from seat2.hand; seat2.card_count -= number of cards; set pile_kind by the cards (single, pair, triple or run); pile_value = highest card; last_player = 2; seat2.last_action = option.
  11. [update] all players. What happens: seat2.deals_won += 1; for each other seat with n = card_count: penalty += n * (2 if n >= 7 else 1) + (number of cards in hand numbered 28, 29 or 30); deal_active = false
  12. [update] seat 3. What happens: Clearance: pile_kind = 'empty', pile_value = 0
  13. [ask] seat 3 answers: one option from the legal-play list built from seat 3's hand and the pile (see offers); the choice is shown to everyone. What happens: the chosen option is recorded for the next step
  14. [update] seat 3. What happens: If 'pass': seat3.last_action = 'pass'. Otherwise split the option on spaces into cards; remove each card from seat3.hand; seat3.card_count -= number of cards; set pile_kind by the cards (single, pair, triple or run); pile_value = highest card; last_player = 3; seat3.last_action = option.
  15. [update] all players. What happens: seat3.deals_won += 1; for each other seat with n = card_count: penalty += n * (2 if n >= 7 else 1) + (number of cards in hand numbered 28, 29 or 30); deal_active = false
  16. [update] all players. What happens: first_orbit = false
  17. [update] all players. What happens: For every seat with n = card_count: penalty += n * (2 if n >= 7 else 1) + (number of cards in hand numbered 28, 29 or 30); deal_active = false
  18. [check] all players. What happens: end the game if (deal_number == 3 and deal_active == false) or orbit >= 40; otherwise continue

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. Card c has rank floor((c+2)/3), from 1 to 10, and suit c - 3*(rank-1), from 1 to 3; for example card 13 is rank 5 suit 1 and card 16 is rank 6 suit 1.
  R2. A higher card number is always a higher card, and the value of a play is its highest card number.
  R3. A single is 1 card, a pair is 2 cards of the same rank, a triple is 3 cards of the same rank, and a run is 3 cards of three consecutive ranks without wrap-around; any other set of cards is not a play.
  R4. When '13 14' is offered it is a pair; '14 16' is never offered as a pair.
  R5. Each orbit begins with orbit increased by 1.
  R6. When deal_active is false and deal_number < 3 at the start of an orbit, deal_number increases by 1, each player gets 9 random cards, 3 cards go to the hidden aside, every card_count becomes 9, leader_seat = deal_number, first_orbit = true, pile_kind = 'empty', pile_value = 0 and last_player = leader_seat.
  R7. Seat 1 leads deal 1, seat 2 leads deal 2 and seat 3 leads deal 3.
  R8. Seats take turns in order 1, 2, 3; a seat is skipped when deal_active is false, or when first_orbit is true and its seat number is below leader_seat.
  R9. When a seat's turn starts and last_player equals that seat, pile_kind becomes 'empty' and pile_value becomes 0, and that seat leads.
  R10. When pile_kind is 'empty', the seat is offered every single, pair, triple and run from its hand, and 'pass' is not offered.
  R11. When pile_kind is 'single', the seat is offered 'pass', every single with value > pile_value and every triple of any value.
  R12. When pile_kind is 'pair', the seat is offered 'pass', every pair with value > pile_value and every triple of any value.
  R13. When pile_kind is 'triple', the seat is offered 'pass' and every triple with value > pile_value.
  R14. When pile_kind is 'run', the seat is offered 'pass' and every run with value > pile_value.
  R15. When a seat passes, its last_action becomes 'pass' and nothing else changes.
  R16. When a seat plays k cards, those cards leave its hand, card_count drops by k, pile_value becomes the highest card played, last_player becomes that seat and last_action becomes the option string.
  R17. After a play, pile_kind is 'single' for 1 card, 'pair' for 2, 'triple' for 3 of one rank and 'run' for 3 consecutive ranks; a triple bombing a single or pair sets pile_kind to 'triple'.
  R18. When a seat's card_count reaches 0, its deals_won increases by 1, deal_active becomes false and the rest of that orbit's turns are skipped.
  R19. When a deal is won, each other seat with n cards adds n to penalty, or 2n if n >= 7, plus 1 per card numbered 28, 29 or 30 it holds; for example 7 cards including card 30 adds 15.
  R20. At the end of every orbit first_orbit becomes false.
  R21. When orbit 40 ends with a deal still active, every seat adds the same penalty formula for the cards it holds.
  R22. The game ends when deal 3 has ended or when orbit 40 is complete, and deals that never started are not played.
  R23. The lowest penalty wins, ties are broken by the most deals_won, and players still tied share the win.
  R24. Hands and the aside cards are hidden; card_count, penalty, deals_won, last_action and the pile are public.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Turn choice when pile_kind is 'empty' (leading) | asked: the seat whose turn it is | options: every single, pair, triple and run that can be made from its hand, each written as ascending card numbers separated by single spaces; no 'pass'
  - Turn choice when pile_kind is 'single' | asked: the seat whose turn it is | options: 'pass'; every single from its hand with card number > pile_value; every triple from its hand of any value
  - Turn choice when pile_kind is 'pair' | asked: the seat whose turn it is | options: 'pass'; every pair from its hand whose higher card > pile_value; every triple from its hand of any value
  - Turn choice when pile_kind is 'triple' | asked: the seat whose turn it is | options: 'pass'; every triple from its hand whose highest card > pile_value
  - Turn choice when pile_kind is 'run' | asked: the seat whose turn it is | options: 'pass'; every run from its hand whose highest card > pile_value
  - Any turn | asked: seats skipped by rule R8 or after the deal ended | options: not asked

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: (deal_number == 3 and deal_active == false) or orbit >= 40
  - each player's standing: you.deals_won - 10 * you.penalty (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: The lowest total penalty wins. Among players tied for lowest penalty, the one with the most deals_won wins. Players still tied share the win, which is the draw.
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

- each player: `card_count` (number, visible: public, starts 0): number of cards in hand
- each player: `penalty` (number, visible: public, starts 0): total penalty points; lower is better
- each player: `deals_won` (number, visible: public, starts 0): deals this player won by emptying their hand
- each player: `last_action` (text, visible: public, starts 'no play yet'): 'pass' or the last play string, e.g. '13 14'
- the table: `deal_number` (number, visible: public, starts 0): number of deals started
- the table: `orbit` (number, visible: public, starts 0): number of orbits (engine rounds) begun
- the table: `pile_kind` (text, visible: public, starts 'empty'): 'empty', 'single', 'pair', 'triple' or 'run'
- the table: `pile_value` (number, visible: public, starts 0): highest card number of the play on top of the pile
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 30, ranks = 10, suits = 3, hand_size = 9, aside_size = 3, max_deals = 3, max_orbits = 40, double_penalty_threshold = 7, double_penalty_factor = 2, top_rank_card_low = 28, top_rank_card_high = 30, top_card_penalty = 1, min_play_cards = 1, max_play_cards = 3, run_length = 3, initial_penalty = 0, initial_deals_won = 0, deals_won_tiebreak_multiplier = 10
- the game ends with ONE ending whose `rank_by` is `you.deals_won - 10 * you.penalty`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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

````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "little_two",
    "name": "Little Two",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "A three-player climbing card game over up to 3 deals: shed your 9 cards with singles, pairs, triples or runs; the lowest total penalty wins."
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
        "key": "deals_won",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "last_action",
        "visible": "public",
        "type": "text",
        "initial": "no play yet"
      },
      {
        "key": "offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "matches",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "played",
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
        "initial": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
      },
      {
        "key": "all_cards",
        "visible": "none",
        "type": "list",
        "initial": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
      },
      {
        "key": "card_names",
        "visible": "none",
        "type": "list",
        "initial": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"]
      },
      {
        "key": "aside",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "deal_number",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "orbit",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "deal_active",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "leader_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "first_orbit",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "pile_kind",
        "visible": "public",
        "type": "text",
        "initial": "empty",
        "values": ["empty", "single", "pair", "triple", "run"]
      },
      {
        "key": "pile_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "last_player",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "ranks",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "suits",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "hand_size",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "aside_size",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "max_deals",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "max_orbits",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "double_penalty_threshold",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "double_penalty_factor",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "top_rank_card_low",
        "visible": "public",
        "type": "number",
        "initial": 28
      },
      {
        "key": "top_rank_card_high",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "top_card_penalty",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "min_play_cards",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "max_play_cards",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "run_length",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "initial_penalty",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "initial_deals_won",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "deals_won_tiebreak_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 10
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "starting state",
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
            "key": "card_count",
            "value": 0
          }
        },
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
            "key": "deals_won",
            "value": {
              "calc": "initial_deals_won"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "last_action",
            "value": "no play yet"
          }
        },
        {
          "set": {
            "key": "deal_number",
            "value": 0
          }
        },
        {
          "set": {
            "key": "orbit",
            "value": 0
          }
        },
        {
          "set": {
            "key": "deal_active",
            "value": false
          }
        },
        {
          "set": {
            "key": "pile_kind",
            "value": "empty"
          }
        },
        {
          "set": {
            "key": "pile_value",
            "value": 0
          }
        },
        {
          "set": {
            "key": "last_player",
            "value": 0
          }
        }
      ],
      "text": "Three players take seats 1, 2 and 3. No cards are dealt yet: the first deal starts in orbit 1."
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "orbit",
      "label": "next orbit",
      "do": [
        {
          "adjust": {
            "key": "orbit",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "deal",
      "label": "start a deal",
      "when": {
        "calc": "not deal_active and deal_number < max_deals"
      },
      "do": [
        {
          "adjust": {
            "key": "deal_number",
            "value": 1
          }
        },
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
            "players": "all",
            "key": "hand",
            "value": []
          }
        },
        {
          "set": {
            "key": "aside",
            "value": []
          }
        },
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {
          "set": {
            "key": "aside",
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
            "players": "all",
            "key": "card_count",
            "value": {
              "calc": "hand_size"
            }
          }
        },
        {
          "set": {
            "key": "leader_seat",
            "value": {
              "calc": "deal_number"
            }
          }
        },
        {
          "set": {
            "key": "deal_active",
            "value": true
          }
        },
        {
          "set": {
            "key": "first_orbit",
            "value": true
          }
        },
        {
          "set": {
            "key": "pile_kind",
            "value": "empty"
          }
        },
        {
          "set": {
            "key": "pile_value",
            "value": 0
          }
        },
        {
          "set": {
            "key": "last_player",
            "value": {
              "calc": "leader_seat"
            }
          }
        }
      ],
      "text": "Deal {deal_number} has started. Everyone holds {hand_size} cards and {aside_size} cards are set aside unseen. Seat {leader_seat} leads."
    },
    {
      "use": "sync",
      "phase": "deal",
      "label": "your hand",
      "when": {
        "calc": "deal_active"
      },
      "mode": "self",
      "to": "all",
      "text": "Your hand and standing:"
    },
    {
      "use": "update",
      "phase": "seat 1",
      "label": "seat 1 clearance and options",
      "when": {
        "calc": "deal_active and not (first_orbit and 1 < leader_seat)"
      },
      "do": [
        {
          "set": {
            "key": "pile_kind",
            "value": "empty",
            "if": {
              "calc": "last_player == 1"
            }
          }
        },
        {
          "set": {
            "key": "pile_value",
            "value": 0,
            "if": {
              "calc": "last_player == 1"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 1"
            },
            "key": "offer",
            "value": {
              "calc": "([card_names[a - 1] for a in you.hand] + [card_names[a - 1] + ' ' + card_names[b - 1] for a in you.hand for b in you.hand if a < b and int((a + suits - 1) / suits) == int((b + suits - 1) / suits)] + [card_names[a - 1] + ' ' + card_names[b - 1] + ' ' + card_names[c - 1] for a in you.hand for b in you.hand for c in you.hand if a < b and b < c and int((a + suits - 1) / suits) == int((c + suits - 1) / suits)] + [card_names[a - 1] + ' ' + card_names[b - 1] + ' ' + card_names[c - 1] for a in you.hand for b in you.hand for c in you.hand if a < b and b < c and int((b + suits - 1) / suits) == int((a + suits - 1) / suits) + 1 and int((c + suits - 1) / suits) == int((b + suits - 1) / suits) + 1] if pile_kind == 'empty' else []) + (['pass'] + [card_names[a - 1] for a in you.hand if a > pile_value] + [card_names[a - 1] + ' ' + card_names[b - 1] + ' ' + card_names[c - 1] for a in you.hand for b in you.hand for c in you.hand if a < b and b < c and int((a + suits - 1) / suits) == int((c + suits - 1) / suits)] if pile_kind == 'single' else []) + (['pass'] + [card_names[a - 1] + ' ' + card_names[b - 1] for a in you.hand for b in you.hand if a < b and b > pile_value and int((a + suits - 1) / suits) == int((b + suits - 1) / suits)] + [card_names[a - 1] + ' ' + card_names[b - 1] + ' ' + card_names[c - 1] for a in you.hand for b in you.hand for c in you.hand if a < b and b < c and int((a + suits - 1) / suits) == int((c + suits - 1) / suits)] if pile_kind == 'pair' else []) + (['pass'] + [card_names[a - 1] + ' ' + card_names[b - 1] + ' ' + card_names[c - 1] for a in you.hand for b in you.hand for c in you.hand if a < b and b < c and c > pile_value and int((a + suits - 1) / suits) == int((c + suits - 1) / suits)] if pile_kind == 'triple' else []) + (['pass'] + [card_names[a - 1] + ' ' + card_names[b - 1] + ' ' + card_names[c - 1] for a in you.hand for b in you.hand for c in you.hand if a < b and b < c and c > pile_value and int((b + suits - 1) / suits) == int((a + suits - 1) / suits) + 1 and int((c + suits - 1) / suits) == int((b + suits - 1) / suits) + 1] if pile_kind == 'run' else [])"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "seat 1",
      "label": "seat 1 plays",
      "when": {
        "calc": "deal_active and not (first_orbit and 1 < leader_seat)"
      },
      "to": {
        "where": "you.seat == 1"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "c1"
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat}: {value}"
      },
      "text": "Your turn. The pile holds: {pile_kind} (value {pile_value}). Choose one of your options: a play written as its card numbers in ascending order, or 'pass' if offered."
    },
    {
      "use": "update",
      "phase": "seat 1",
      "label": "seat 1 play resolves",
      "when": {
        "calc": "deal_active and not (first_orbit and 1 < leader_seat)"
      },
      "do": [
        {
          "set": {
            "players": {
              "where": "you.seat == 1"
            },
            "key": "matches",
            "value": {
              "calc": "[[a] for a in you.hand if card_names[a - 1] == $c1] + [[a, b] for a in you.hand for b in you.hand if a < b and card_names[a - 1] + ' ' + card_names[b - 1] == $c1] + [[a, b, c] for a in you.hand for b in you.hand for c in you.hand if a < b and b < c and card_names[a - 1] + ' ' + card_names[b - 1] + ' ' + card_names[c - 1] == $c1]"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 1"
            },
            "key": "played",
            "value": {
              "calc": "you.matches[0] if len(you.matches) > 0 else []"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 1"
            },
            "key": "hand",
            "value": {
              "calc": "[x for x in you.hand if x not in you.played]"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat == 1"
            },
            "key": "card_count",
            "value": {
              "calc": "-len(you.played)"
            }
          }
        },
        {
          "set": {
            "key": "pile_kind",
            "value": {
              "calc": "'single' if len(players[0].played) == 1 else ('pair' if len(players[0].played) == 2 else ('triple' if int((players[0].played[0] + suits - 1) / suits) == int((players[0].played[2] + suits - 1) / suits) else 'run'))"
            },
            "if": {
              "calc": "len(players[0].played) > 0"
            }
          }
        },
        {
          "set": {
            "key": "pile_value",
            "value": {
              "calc": "max(players[0].played)"
            },
            "if": {
              "calc": "len(players[0].played) > 0"
            }
          }
        },
        {
          "set": {
            "key": "last_player",
            "value": 1,
            "if": {
              "calc": "len(players[0].played) > 0"
            }
          }
        },
        {
          "set": {
            "player": 1,
            "key": "last_action",
            "value": "$c1"
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "seat 1",
      "label": "seat 1 wins the deal",
      "when": {
        "calc": "deal_active and players[0].card_count == 0"
      },
      "do": [
        {
          "adjust": {
            "player": 1,
            "key": "deals_won",
            "value": 1
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat != 1"
            },
            "key": "penalty",
            "value": {
              "calc": "you.card_count * (double_penalty_factor if you.card_count >= double_penalty_threshold else 1) + top_card_penalty * count(x >= top_rank_card_low and x <= top_rank_card_high for x in you.hand)"
            }
          }
        },
        {
          "set": {
            "key": "deal_active",
            "value": false
          }
        }
      ],
      "text": "Seat 1 has played out and wins deal {deal_number}. Penalties now: seat 1 {players[0].penalty}, seat 2 {players[1].penalty}, seat 3 {players[2].penalty}."
    },
    {
      "use": "update",
      "phase": "seat 2",
      "label": "seat 2 clearance and options",
      "when": {
        "calc": "deal_active and not (first_orbit and 2 < leader_seat)"
      },
      "do": [
        {
          "set": {
            "key": "pile_kind",
            "value": "empty",
            "if": {
              "calc": "last_player == 2"
            }
          }
        },
        {
          "set": {
            "key": "pile_value",
            "value": 0,
            "if": {
              "calc": "last_player == 2"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 2"
            },
            "key": "offer",
            "value": {
              "calc": "([card_names[a - 1] for a in you.hand] + [card_names[a - 1] + ' ' + card_names[b - 1] for a in you.hand for b in you.hand if a < b and int((a + suits - 1) / suits) == int((b + suits - 1) / suits)] + [card_names[a - 1] + ' ' + card_names[b - 1] + ' ' + card_names[c - 1] for a in you.hand for b in you.hand for c in you.hand if a < b and b < c and int((a + suits - 1) / suits) == int((c + suits - 1) / suits)] + [card_names[a - 1] + ' ' + card_names[b - 1] + ' ' + card_names[c - 1] for a in you.hand for b in you.hand for c in you.hand if a < b and b < c and int((b + suits - 1) / suits) == int((a + suits - 1) / suits) + 1 and int((c + suits - 1) / suits) == int((b + suits - 1) / suits) + 1] if pile_kind == 'empty' else []) + (['pass'] + [card_names[a - 1] for a in you.hand if a > pile_value] + [card_names[a - 1] + ' ' + card_names[b - 1] + ' ' + card_names[c - 1] for a in you.hand for b in you.hand for c in you.hand if a < b and b < c and int((a + suits - 1) / suits) == int((c + suits - 1) / suits)] if pile_kind == 'single' else []) + (['pass'] + [card_names[a - 1] + ' ' + card_names[b - 1] for a in you.hand for b in you.hand if a < b and b > pile_value and int((a + suits - 1) / suits) == int((b + suits - 1) / suits)] + [card_names[a - 1] + ' ' + card_names[b - 1] + ' ' + card_names[c - 1] for a in you.hand for b in you.hand for c in you.hand if a < b and b < c and int((a + suits - 1) / suits) == int((c + suits - 1) / suits)] if pile_kind == 'pair' else []) + (['pass'] + [card_names[a - 1] + ' ' + card_names[b - 1] + ' ' + card_names[c - 1] for a in you.hand for b in you.hand for c in you.hand if a < b and b < c and c > pile_value and int((a + suits - 1) / suits) == int((c + suits - 1) / suits)] if pile_kind == 'triple' else []) + (['pass'] + [card_names[a - 1] + ' ' + card_names[b - 1] + ' ' + card_names[c - 1] for a in you.hand for b in you.hand for c in you.hand if a < b and b < c and c > pile_value and int((b + suits - 1) / suits) == int((a + suits - 1) / suits) + 1 and int((c + suits - 1) / suits) == int((b + suits - 1) / suits) + 1] if pile_kind == 'run' else [])"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "seat 2",
      "label": "seat 2 plays",
      "when": {
        "calc": "deal_active and not (first_orbit and 2 < leader_seat)"
      },
      "to": {
        "where": "you.seat == 2"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "c2"
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat}: {value}"
      },
      "text": "Your turn. The pile holds: {pile_kind} (value {pile_value}). Choose one of your options: a play written as its card numbers in ascending order, or 'pass' if offered."
    },
    {
      "use": "update",
      "phase": "seat 2",
      "label": "seat 2 play resolves",
      "when": {
        "calc": "deal_active and not (first_orbit and 2 < leader_seat)"
      },
      "do": [
        {
          "set": {
            "players": {
              "where": "you.seat == 2"
            },
            "key": "matches",
            "value": {
              "calc": "[[a] for a in you.hand if card_names[a - 1] == $c2] + [[a, b] for a in you.hand for b in you.hand if a < b and card_names[a - 1] + ' ' + card_names[b - 1] == $c2] + [[a, b, c] for a in you.hand for b in you.hand for c in you.hand if a < b and b < c and card_names[a - 1] + ' ' + card_names[b - 1] + ' ' + card_names[c - 1] == $c2]"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 2"
            },
            "key": "played",
            "value": {
              "calc": "you.matches[0] if len(you.matches) > 0 else []"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 2"
            },
            "key": "hand",
            "value": {
              "calc": "[x for x in you.hand if x not in you.played]"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat == 2"
            },
            "key": "card_count",
            "value": {
              "calc": "-len(you.played)"
            }
          }
        },
        {
          "set": {
            "key": "pile_kind",
            "value": {
              "calc": "'single' if len(players[1].played) == 1 else ('pair' if len(players[1].played) == 2 else ('triple' if int((players[1].played[0] + suits - 1) / suits) == int((players[1].played[2] + suits - 1) / suits) else 'run'))"
            },
            "if": {
              "calc": "len(players[1].played) > 0"
            }
          }
        },
        {
          "set": {
            "key": "pile_value",
            "value": {
              "calc": "max(players[1].played)"
            },
            "if": {
              "calc": "len(players[1].played) > 0"
            }
          }
        },
        {
          "set": {
            "key": "last_player",
            "value": 2,
            "if": {
              "calc": "len(players[1].played) > 0"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "last_action",
            "value": "$c2"
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "seat 2",
      "label": "seat 2 wins the deal",
      "when": {
        "calc": "deal_active and players[1].card_count == 0"
      },
      "do": [
        {
          "adjust": {
            "player": 2,
            "key": "deals_won",
            "value": 1
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat != 2"
            },
            "key": "penalty",
            "value": {
              "calc": "you.card_count * (double_penalty_factor if you.card_count >= double_penalty_threshold else 1) + top_card_penalty * count(x >= top_rank_card_low and x <= top_rank_card_high for x in you.hand)"
            }
          }
        },
        {
          "set": {
            "key": "deal_active",
            "value": false
          }
        }
      ],
      "text": "Seat 2 has played out and wins deal {deal_number}. Penalties now: seat 1 {players[0].penalty}, seat 2 {players[1].penalty}, seat 3 {players[2].penalty}."
    },
    {
      "use": "update",
      "phase": "seat 3",
      "label": "seat 3 clearance and options",
      "when": {
        "calc": "deal_active and not (first_orbit and 3 < leader_seat)"
      },
      "do": [
        {
          "set": {
            "key": "pile_kind",
            "value": "empty",
            "if": {
              "calc": "last_player == 3"
            }
          }
        },
        {
          "set": {
            "key": "pile_value",
            "value": 0,
            "if": {
              "calc": "last_player == 3"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 3"
            },
            "key": "offer",
            "value": {
              "calc": "([card_names[a - 1] for a in you.hand] + [card_names[a - 1] + ' ' + card_names[b - 1] for a in you.hand for b in you.hand if a < b and int((a + suits - 1) / suits) == int((b + suits - 1) / suits)] + [card_names[a - 1] + ' ' + card_names[b - 1] + ' ' + card_names[c - 1] for a in you.hand for b in you.hand for c in you.hand if a < b and b < c and int((a + suits - 1) / suits) == int((c + suits - 1) / suits)] + [card_names[a - 1] + ' ' + card_names[b - 1] + ' ' + card_names[c - 1] for a in you.hand for b in you.hand for c in you.hand if a < b and b < c and int((b + suits - 1) / suits) == int((a + suits - 1) / suits) + 1 and int((c + suits - 1) / suits) == int((b + suits - 1) / suits) + 1] if pile_kind == 'empty' else []) + (['pass'] + [card_names[a - 1] for a in you.hand if a > pile_value] + [card_names[a - 1] + ' ' + card_names[b - 1] + ' ' + card_names[c - 1] for a in you.hand for b in you.hand for c in you.hand if a < b and b < c and int((a + suits - 1) / suits) == int((c + suits - 1) / suits)] if pile_kind == 'single' else []) + (['pass'] + [card_names[a - 1] + ' ' + card_names[b - 1] for a in you.hand for b in you.hand if a < b and b > pile_value and int((a + suits - 1) / suits) == int((b + suits - 1) / suits)] + [card_names[a - 1] + ' ' + card_names[b - 1] + ' ' + card_names[c - 1] for a in you.hand for b in you.hand for c in you.hand if a < b and b < c and int((a + suits - 1) / suits) == int((c + suits - 1) / suits)] if pile_kind == 'pair' else []) + (['pass'] + [card_names[a - 1] + ' ' + card_names[b - 1] + ' ' + card_names[c - 1] for a in you.hand for b in you.hand for c in you.hand if a < b and b < c and c > pile_value and int((a + suits - 1) / suits) == int((c + suits - 1) / suits)] if pile_kind == 'triple' else []) + (['pass'] + [card_names[a - 1] + ' ' + card_names[b - 1] + ' ' + card_names[c - 1] for a in you.hand for b in you.hand for c in you.hand if a < b and b < c and c > pile_value and int((b + suits - 1) / suits) == int((a + suits - 1) / suits) + 1 and int((c + suits - 1) / suits) == int((b + suits - 1) / suits) + 1] if pile_kind == 'run' else [])"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "seat 3",
      "label": "seat 3 plays",
      "when": {
        "calc": "deal_active and not (first_orbit and 3 < leader_seat)"
      },
      "to": {
        "where": "you.seat == 3"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "c3"
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat}: {value}"
      },
      "text": "Your turn. The pile holds: {pile_kind} (value {pile_value}). Choose one of your options: a play written as its card numbers in ascending order, or 'pass' if offered."
    },
    {
      "use": "update",
      "phase": "seat 3",
      "label": "seat 3 play resolves",
      "when": {
        "calc": "deal_active and not (first_orbit and 3 < leader_seat)"
      },
      "do": [
        {
          "set": {
            "players": {
              "where": "you.seat == 3"
            },
            "key": "matches",
            "value": {
              "calc": "[[a] for a in you.hand if card_names[a - 1] == $c3] + [[a, b] for a in you.hand for b in you.hand if a < b and card_names[a - 1] + ' ' + card_names[b - 1] == $c3] + [[a, b, c] for a in you.hand for b in you.hand for c in you.hand if a < b and b < c and card_names[a - 1] + ' ' + card_names[b - 1] + ' ' + card_names[c - 1] == $c3]"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 3"
            },
            "key": "played",
            "value": {
              "calc": "you.matches[0] if len(you.matches) > 0 else []"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 3"
            },
            "key": "hand",
            "value": {
              "calc": "[x for x in you.hand if x not in you.played]"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat == 3"
            },
            "key": "card_count",
            "value": {
              "calc": "-len(you.played)"
            }
          }
        },
        {
          "set": {
            "key": "pile_kind",
            "value": {
              "calc": "'single' if len(players[2].played) == 1 else ('pair' if len(players[2].played) == 2 else ('triple' if int((players[2].played[0] + suits - 1) / suits) == int((players[2].played[2] + suits - 1) / suits) else 'run'))"
            },
            "if": {
              "calc": "len(players[2].played) > 0"
            }
          }
        },
        {
          "set": {
            "key": "pile_value",
            "value": {
              "calc": "max(players[2].played)"
            },
            "if": {
              "calc": "len(players[2].played) > 0"
            }
          }
        },
        {
          "set": {
            "key": "last_player",
            "value": 3,
            "if": {
              "calc": "len(players[2].played) > 0"
            }
          }
        },
        {
          "set": {
            "player": 3,
            "key": "last_action",
            "value": "$c3"
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "seat 3",
      "label": "seat 3 wins the deal",
      "when": {
        "calc": "deal_active and players[2].card_count == 0"
      },
      "do": [
        {
          "adjust": {
            "player": 3,
            "key": "deals_won",
            "value": 1
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat != 3"
            },
            "key": "penalty",
            "value": {
              "calc": "you.card_count * (double_penalty_factor if you.card_count >= double_penalty_threshold else 1) + top_card_penalty * count(x >= top_rank_card_low and x <= top_rank_card_high for x in you.hand)"
            }
          }
        },
        {
          "set": {
            "key": "deal_active",
            "value": false
          }
        }
      ],
      "text": "Seat 3 has played out and wins deal {deal_number}. Penalties now: seat 1 {players[0].penalty}, seat 2 {players[1].penalty}, seat 3 {players[2].penalty}."
    },
    {
      "use": "update",
      "phase": "end of orbit",
      "label": "first orbit over",
      "do": [
        {
          "set": {
            "key": "first_orbit",
            "value": false
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "end of orbit",
      "label": "orbit limit penalty",
      "when": {
        "calc": "orbit >= max_orbits and deal_active"
      },
      "do": [
        {
          "adjust": {
            "players": "all",
            "key": "penalty",
            "value": {
              "calc": "you.card_count * (double_penalty_factor if you.card_count >= double_penalty_threshold else 1) + top_card_penalty * count(x >= top_rank_card_low and x <= top_rank_card_high for x in you.hand)"
            }
          }
        },
        {
          "set": {
            "key": "deal_active",
            "value": false
          }
        }
      ],
      "text": "Orbit {max_orbits} is over with the deal unfinished: every seat is penalised for the cards it holds."
    },
    {
      "use": "check",
      "phase": "end of orbit",
      "label": "is the game over",
      "when": {
        "calc": "(deal_number == max_deals and not deal_active) or orbit >= max_orbits"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "(deal_number == max_deals and not deal_active) or orbit >= max_orbits"
      },
      "rank_by": "you.deals_won - 10 * you.penalty",
      "reveal": [
        "hand"
      ],
      "text": "Winner: {result}. Penalties: Seat 1 {players[0].penalty}, Seat 2 {players[1].penalty}, Seat 3 {players[2].penalty}; deals won: Seat 1 {players[0].deals_won}, Seat 2 {players[1].deals_won}, Seat 3 {players[2].deals_won}."
    }
  },
  "limits": {
    "rounds": 40,
    "rounds_max": 40,
    "actions_max": 3000,
    "deadline_s": 120
  },
  "rules": "CARDS. There are {deck_size} cards, numbered 1 to {deck_size}. A card c has rank = floor((c+2)/3), from 1 to {ranks}, and suit = c - 3*(rank-1), from 1 to {suits}. Rank 1 is lowest and rank {ranks} (cards {top_rank_card_low} to {top_rank_card_high}) is highest and plays the role of the 2. Within a rank, a higher suit is a higher card, so a higher card number is always a higher card. Examples: card 13 has rank 5, suit 1; card 14 has rank 5, suit 2; card 16 has rank 6, suit 1.\n\nPLAY KINDS. A play is {min_play_cards} to {max_play_cards} cards from your own hand, written as their numbers in ascending order separated by single spaces (for example '13 14'). Single: 1 card. Pair: 2 cards of the same rank ('13 14' is a pair; '14 16' is not). Triple: 3 cards of the same rank. Run: {run_length} cards whose ranks are three consecutive numbers (for example ranks 4, 5, 6), in any suits; ranks do not wrap around. Any other set of cards is not a play. The value of a play is its highest card number.\n\nSETUP. 3 players in seats 1, 2 and 3. Each player has a private hand, a public card_count, a public penalty (starting at {initial_penalty}), public deals_won (starting at {initial_deals_won}) and a public last_action. The game lasts at most {max_orbits} orbits and at most {max_deals} deals.\n\nEACH ORBIT: orbit goes up by 1. If no deal is active and fewer than {max_deals} deals have started, a deal starts: all {deck_size} cards are shuffled, {hand_size} go to each player's private hand and the remaining {aside_size} are set aside unseen. Seat 1 leads deal 1, seat 2 leads deal 2, seat 3 leads deal 3; the pile starts empty. Seats then take turns in order 1, 2, 3. A seat skips its turn if no deal is active, or if this is the orbit in which the deal started and its seat number is lower than the leader's.\n\nON YOUR TURN: if the last play on the pile was yours (the other two passed since, or the deal just started), the pile is cleared and you lead. You are offered exactly: if the pile is empty, every single, pair, triple and run in your hand, and you may not pass; on a single, 'pass', any higher single, or any triple (a bomb); on a pair, 'pass', any higher pair, or any triple (a bomb); on a triple, 'pass' or any higher triple; on a run, 'pass' or any higher run. Higher means a higher value (highest card number). Everyone sees your choice. If you pass, your last_action becomes 'pass' and nothing else changes; you may still play when your turn comes again. If you play, the cards leave your hand, your card_count drops by the number played, the pile becomes your play (a triple that bombs a single or pair makes the pile a triple, so only a higher triple can follow), and your last_action shows the play.\n\nWINNING A DEAL: when your card_count reaches 0 you win the deal: your deals_won goes up by 1. Every other seat with n cards left adds a penalty of n, doubled to {double_penalty_factor}n if n is {double_penalty_threshold} or more, plus {top_card_penalty} for each card numbered {top_rank_card_low} to {top_rank_card_high} still in its hand (7 cards including card 30 adds 15). The deal ends and the rest of that orbit's turns are skipped; the next deal starts next orbit.\n\nEND. The game ends when deal {max_deals} has ended, or when orbit {max_orbits} is complete. If orbit {max_orbits} ends while a deal is still active, every seat is penalised for the cards it holds by the same formula. Deals that never started are not played. There is no talk. All plays and passes are public; hands and the aside cards stay hidden.\n\nWINNER: the lowest total penalty wins. If players tie for lowest, the one among them with the most deals_won wins. Players still tied share the win."
}
```
````
