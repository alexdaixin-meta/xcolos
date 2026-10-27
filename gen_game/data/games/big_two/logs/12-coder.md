# 12 coder

- time: 2026-10-27T21:22:42+00:00 (211.6s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 04528dd673c7d578, reply sha256 f8d501d468243fb0

## Sent

````
# Task: write the XColos game file for "Little Two"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

CARDS. There are 30 cards numbered 1 to 30. A card's rank is (card + 2) divided by 3, rounded down, giving ranks 1 to 10. Its suit is card − 3 × (rank − 1), giving suits 1 to 3. A higher card number always beats a lower one. Rank 10 (cards 28, 29, 30) are called 'twos'.

SEATS. The players sit as A, B and C. Turn order is always A, then B, then C, then A again.

MATCH. The match has 3 deals and at most 40 orbits. An orbit is one turn for each seat in order.

DEALING. At the start of each deal, shuffle all 30 cards. Deal 9 to each player, privately. Set the remaining 3 cards aside face-down; nobody sees them during the deal. Every player's card count is public at all times.

COMBINATIONS. There are four kinds:
- Single: one card.
- Pair: two cards of the same rank.
- Triple: three cards of the same rank.
- Run: three cards of three consecutive ranks, any suits. Ranks do not wrap around, so 9-10-1 is not a run.
The value of a combination is its highest card number.

THE PILE. The pile holds a current kind and a current value, or is empty.
- When the pile is empty, the player whose turn it is must lead any combination. They may not pass.
- When the pile is not empty, the player whose turn it is may pass, or may play a combination of the same kind with a higher value.
- Bomb: a triple may be played on a single or a pair whatever its value. The pile's kind then becomes triple.
- A triple on the pile can only be beaten by a higher triple.
- A run can only be beaten by a higher run.
Played cards are announced to everyone and removed from the game for the rest of the deal.

PASSING AND CLEARING. A player who passes may play again the next time their turn comes in the same trick. The engine records who made the last play. If play comes back round to that player because both others passed since their play, the pile is cleared and that player must lead.

ILLEGAL PLAYS. An illegal or malformed play counts as a pass. If the player was required to lead, their lowest-numbered card is played as a single instead.

STARTING A DEAL. In deal 1, seat A leads first. In deal 2, seat B leads first. In deal 3, seat C leads first. Seats before the leader in the first orbit of a deal do not act in that orbit.

END OF A DEAL. A deal ends the moment a player plays their last card. That player wins the deal, and the rest of that orbit is skipped. The next deal begins at the start of the next orbit.

PENALTIES. Each non-winner receives a penalty equal to the number of cards left in their hand, plus 1 for each two (rank 10) left in their hand. If they have 7 or more cards left, this penalty is doubled. The deal winner receives 0. Penalties are added to each player's public running total.

END OF THE MATCH. The match ends after the third deal ends, or at the end of orbit 40, whichever comes first. If orbit 40 ends during a deal, that deal is scored as if it had ended with no winner: every player receives a penalty under the rule above.

How the winner is decided: The player with the lowest total penalty after the match ends wins. If two or three players tie for the lowest total, the match is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Little Two (3 to 3 players, best with 3)

A three-player climbing card game. Over 3 deals, players shed singles, pairs, triples and runs onto a pile, and each deal's losers take penalties for the cards left in hand. The lowest total penalty wins.

STATE (every item below must exist in the file):
  - each player: hand (list, starts []); only its owner sees it. Card numbers (1-30) the player holds in the current deal.
  - each player: card_count (number, starts 0); everyone sees it. Number of cards in hand. It is public at all times.
  - each player: penalty (number, starts 0); everyone sees it. Running total of penalties across deals. This is the score, and lower is better.
  - each player: deals_won (number, starts 0); everyone sees it. Number of deals this player won by emptying their hand.
  - each player: last_action (text, starts ''); everyone sees it. Announcement of this player's most recent play or pass.
  - the table: deck (list, starts []); hidden from all players. Cards still to be dealt this deal (shuffled 1-30).
  - the table: aside (list, starts []); hidden from all players. The 3 face-down cards set aside, unseen during the deal.
  - the table: deal_number (number, starts 0); everyone sees it. Current deal (1-3); 0 before the first deal.
  - the table: orbit (number, starts 0); everyone sees it. Number of completed orbits in the match.
  - the table: deal_active (bool, starts False); everyone sees it. True while a deal is in progress.
  - the table: leader_seat (number, starts 0); everyone sees it. Seat (1=A, 2=B, 3=C) that leads first in the current deal.
  - the table: first_orbit (bool, starts False); everyone sees it. True during the first orbit of a deal, when seats before the leader do not act.
  - the table: pile_kind (text, starts 'empty'); everyone sees it. Current combination kind on the pile: empty, single, pair, triple or run.
  - the table: pile_value (number, starts 0); everyone sees it. Highest card number of the combination on the pile (0 when empty).
  - the table: last_player (number, starts 0); everyone sees it. Seat that made the last play on the current pile (0 if none).
  - parameters, each kept as a table attribute: card_count_total = 30, rank_count = 10, suit_count = 3, deals = 3, max_orbits = 40, hand_size = 9, cards_aside = 3, two_rank = 10, two_lowest_card = 28, two_extra_penalty = 1, double_threshold = 7, double_factor = 2, winner_penalty = 0, run_length = 3, pair_size = 2, triple_size = 3

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seats are named A (seat 1), B (seat 2) and C (seat 3); turn order is always A, B, C.
  2. Every player's penalty, deals_won and card_count start at 0; deal_number and orbit start at 0; deal_active is false.
  3. The first deal is dealt by the first round step, since deal_active is false.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] table. What happens: WHEN deal_active is false AND deal_number < 3: deal_number += 1; deck = [1..30]; aside = []; each player's hand = []; pile_kind = 'empty'; pile_value = 0; last_player = 0; leader_seat = deal_number; first_orbit = true; deal_active = true. Announce 'Deal {deal_number} begins; seat {leader_seat} leads.'
  2. [update] table. What happens: WHEN first_orbit is true AND orbit has not advanced since the deal started (the deal-start condition above): for each player, 9 times move a random card from deck to hand; card_count = 9; then move the remaining 3 deck cards to aside. Hands stay private (ally).
  3. [sync] all players. What happens: Each player sees their own hand, all card_counts, all penalties, pile_kind, pile_value and last_player.
  4. [update] seat 1. What happens: WHEN deal_active AND NOT (first_orbit AND leader_seat > 1): if last_player == 1, then pile_kind = 'empty' and pile_value = 0 (the pile clears because both others passed).
  5. [ask] seat 1 answers: short text: 'pass', or the card numbers to play separated by spaces (e.g. '13 14'). 'pass' is not allowed when pile_kind is empty.. What happens: WHEN deal_active AND NOT (first_orbit AND leader_seat > 1). Records the answer for the next step.
  6. [update] seat 1. What happens: WHEN the same condition as seat 1's ask. If judged true: remove the cards from hand; card_count -= number of cards; pile_kind = that kind; pile_value = highest card played; last_player = 1; last_action announces the cards to everyone. If judged false and pile_kind != 'empty': treat as a pass (last_action = 'pass'). If judged false and pile_kind == 'empty': play min(hand) as a single (remove it, card_count -= 1, pile_kind = 'single', pile_value = that card, last_player = 1, announce). JUDGED: a referee rules true or false on "The answer is not 'pass', every named card is in seat 1's hand, the cards form a single, a pair (2 cards, same rank floor((c+2)/3)), a triple (3 same rank) or a run (3 cards of three consecutive ranks without wrap), and either pile_kind is empty, or the kind equals pile_kind with highest card > pile_value, or it is a triple played on a single or pair."; write this step's `when` as {"prose": that sentence, verbatim}.
  7. [update] table. What happens: WHEN deal_active AND seat 1 card_count == 0: seat 1 deals_won += 1; each other player's penalty += (card_count + number of hand cards >= 28) * (2 if card_count >= 7 else 1); deal_active = false. Announce the deal result. The remaining seats' steps this orbit are skipped because deal_active is false.
  8. [update] seat 2. What happens: WHEN deal_active AND NOT (first_orbit AND leader_seat > 2): if last_player == 2, then pile_kind = 'empty' and pile_value = 0.
  9. [ask] seat 2 answers: short text: 'pass' or card numbers separated by spaces; 'pass' is not allowed when pile_kind is empty.. What happens: WHEN deal_active AND NOT (first_orbit AND leader_seat > 2).
  10. [update] seat 2. What happens: Same as seat 1's resolution with seat 2: a legal play removes the cards, lowers card_count, sets pile_kind and pile_value, sets last_player = 2 and is announced. An illegal answer is a pass, or, if the pile is empty, min(hand) is played as a single. JUDGED: a referee rules true or false on "The answer is not 'pass', every named card is in seat 2's hand, the cards form a single, pair, triple or run (ranks floor((c+2)/3), runs without wrap), and either pile_kind is empty, or the kind equals pile_kind with highest card > pile_value, or it is a triple played on a single or pair."; write this step's `when` as {"prose": that sentence, verbatim}.
  11. [update] table. What happens: WHEN deal_active AND seat 2 card_count == 0: seat 2 deals_won += 1; each other player's penalty += (card_count + twos in hand) * (2 if card_count >= 7 else 1); deal_active = false.
  12. [update] seat 3. What happens: WHEN deal_active: if last_player == 3, then pile_kind = 'empty' and pile_value = 0.
  13. [ask] seat 3 answers: short text: 'pass' or card numbers separated by spaces; 'pass' is not allowed when pile_kind is empty.. What happens: WHEN deal_active.
  14. [update] seat 3. What happens: Same as seat 1's resolution with seat 3 (last_player = 3). JUDGED: a referee rules true or false on "The answer is not 'pass', every named card is in seat 3's hand, the cards form a single, pair, triple or run (ranks floor((c+2)/3), runs without wrap), and either pile_kind is empty, or the kind equals pile_kind with highest card > pile_value, or it is a triple played on a single or pair."; write this step's `when` as {"prose": that sentence, verbatim}.
  15. [update] table. What happens: WHEN deal_active AND seat 3 card_count == 0: seat 3 deals_won += 1; each other player's penalty += (card_count + twos in hand) * (2 if card_count >= 7 else 1); deal_active = false.
  16. [update] table. What happens: orbit += 1; first_orbit = false. If orbit == 40 AND deal_active: every player's penalty += (card_count + twos in hand) * (2 if card_count >= 7 else 1); deal_active = false. Announce penalty totals.
  17. [check] table. What happens: End the game if (deal_number == 3 AND deal_active == false) OR orbit >= 40; otherwise continue.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When card c is ranked, then rank = floor((c+2)/3) (1-10) and suit = c - 3*(rank-1) (1-3); e.g. card 14 has rank 5, suit 2.
  R2. When a deal starts, then the 30 cards are shuffled, each player receives 9 cards into a private hand, 3 cards go to the hidden aside list, and every card_count is set to 9.
  R3. When deal 1, 2 or 3 starts, then seat A, B or C respectively leads first, and seats before the leader do not act in that first orbit.
  R4. When the pile is empty, then the acting player must lead any single, pair, triple or run and may not pass.
  R5. When the pile is not empty, then the acting player may pass or play the same kind with a higher value (highest card number).
  R6. When a triple is played on a single or a pair of any value, then it is legal (a bomb) and pile_kind becomes triple.
  R7. When a triple is on the pile, then only a triple with a higher value may be played on it.
  R8. When a run is on the pile, then only a run with a higher value may be played on it; runs are three consecutive ranks without wrap, so ranks 9-10-1 are not a run.
  R9. When a pair or triple is played, then all its cards must share a rank; e.g. 4,5,6 is a triple of rank 2 and 4,5 is a pair of rank 2.
  R10. When a legal play is made, then the cards leave the player's hand, card_count drops by the number played, pile_value becomes the highest card, last_player becomes that seat, and the cards are announced to everyone.
  R11. When a player passes, then they may still play on their next turn in the same trick.
  R12. When play returns to last_player after both other seats passed, then the pile is cleared (pile_kind empty, pile_value 0) and that player must lead.
  R13. When a play is illegal or malformed and the pile is not empty, then it counts as a pass.
  R14. When a play is illegal or malformed and the player was required to lead, then their lowest-numbered card is played as a single.
  R15. When a player plays their last card, then they win the deal, deals_won increases by 1, they take 0 penalty, and the rest of the orbit is skipped.
  R16. When a deal ends, then each non-winner's penalty increases by card_count plus 1 per card numbered 28-30 in hand; e.g. 3 cards including one two gives 4.
  R17. When a non-winner holds 7 or more cards at the end of a deal, then their penalty for that deal is doubled; e.g. 7 cards with no twos gives 14.
  R18. When orbit 40 ends during a deal, then every player receives the penalty under R16 and R17 and the match ends.
  R19. When the third deal ends, then the match ends.
  R20. When the match ends, then the player with the lowest total penalty wins, and players tied for the lowest share the result (a draw).

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Seat's turn (play or pass) | asked: the acting seat, when the pile is empty | options: any single, pair, triple or run made from cards in their hand, written as card numbers; 'pass' is not offered
  - Seat's turn (play or pass) | asked: the acting seat, when the pile holds a single or pair | options: 'pass'; the same kind with a higher highest card; or any triple from their hand (bomb)
  - Seat's turn (play or pass) | asked: the acting seat, when the pile holds a triple | options: 'pass'; or a triple with a higher highest card
  - Seat's turn (play or pass) | asked: the acting seat, when the pile holds a run | options: 'pass'; or a run with a higher highest card
  - Seat's turn | asked: seats before the leader in the first orbit of a deal, and all seats after the deal has ended in that orbit | options: not asked

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: (deal_number == 3 AND deal_active == false) OR orbit >= 40
  - each player's standing: 0 - you.penalty (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their total penalty, and lower is better. The player with the lowest total wins. Players tied for the lowest total share the result, which the source calls a draw.
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

- each player: `card_count` (number, visible: public, starts 0): Number of cards in hand. It is public at all times.
- each player: `penalty` (number, visible: public, starts 0): Running total of penalties across deals. This is the score, and lower is better.
- each player: `deals_won` (number, visible: public, starts 0): Number of deals this player won by emptying their hand.
- the table: `deal_number` (number, visible: public, starts 0): Current deal (1-3); 0 before the first deal.
- the table: `orbit` (number, visible: public, starts 0): Number of completed orbits in the match.
- parameters (each must be an attribute holding this value, never a number buried in a step): card_count_total = 30, rank_count = 10, suit_count = 3, deals = 3, max_orbits = 40, hand_size = 9, cards_aside = 3, two_rank = 10, two_lowest_card = 28, two_extra_penalty = 1, double_threshold = 7, double_factor = 2, winner_penalty = 0, run_length = 3, pair_size = 2, triple_size = 3
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

## Guidance from the last attempt

The previous attempt had problems:

Offer each combination as a text option listing its card numbers in ascending order separated by single spaces (e.g. '13 14', '4 5 6', '10 13 16'). Keep singles as the plain card number and 'pass' as is. Parse the chosen option back into its cards to remove them from the hand, set pile_kind and set pile_value to the highest card. Check that the offer list holds every legal combination from the hand: singles, pairs and triples of the same rank (rank = floor((c+2)/3)), and runs of three consecutive ranks with no wrap from 10 to 1. On a non-empty pile, offer only the same kind with a higher value, plus triples as bombs on a single or a pair. On a triple, offer only higher triples; on a run, only higher runs. When leading, do not offer 'pass'.

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
    "blurb": "A three-player climbing card game: shed singles, pairs, triples and runs over 3 deals; the lowest total penalty wins."
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
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "aside",
        "visible": "none",
        "type": "list",
        "initial": []
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
        "values": [
          "empty",
          "single",
          "pair",
          "triple",
          "run"
        ]
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
        "key": "card_count_total",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "rank_count",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "suit_count",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "deals",
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
        "key": "hand_size",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "cards_aside",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "two_rank",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "two_lowest_card",
        "visible": "public",
        "type": "number",
        "initial": 28
      },
      {
        "key": "two_extra_penalty",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "double_threshold",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "double_factor",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "winner_penalty",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "run_length",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "pair_size",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "triple_size",
        "visible": "public",
        "type": "number",
        "initial": 3
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
        "key": "played",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "resolved",
        "visible": "none",
        "type": "bool",
        "initial": false
      },
      {
        "key": "forced",
        "visible": "none",
        "type": "bool",
        "initial": false
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "seats and scores",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "penalty",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "deals_won",
            "value": 0
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
        }
      ],
      "text": "Seats: A is seat 1, B is seat 2, C is seat 3. Turn order is always A, B, C. The first deal is dealt at the start of the first orbit."
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
      "phase": "deal",
      "label": "a new deal",
      "when": {
        "calc": "not deal_active and deal_number < deals"
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
            "key": "aside",
            "value": []
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
            "key": "last_action",
            "value": ""
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
            "key": "first_orbit",
            "value": true
          }
        },
        {
          "set": {
            "key": "deal_active",
            "value": true
          }
        }
      ],
      "text": "Deal {deal_number} begins; seat {leader_seat} leads (1 = A, 2 = B, 3 = C)."
    },
    {
      "use": "update",
      "phase": "deal",
      "label": "shuffle and deal",
      "when": {
        "calc": "deal_active and len(deck) == card_count_total"
      },
      "do": [
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "[p[1] for p in sorted([[uniform(0, 1), c] for c in all_cards])]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "sorted([deck[i - 1] for i in all_cards if i > (you.seat - 1) * hand_size and i <= you.seat * hand_size])"
            }
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
            "key": "aside",
            "value": {
              "calc": "[deck[i - 1] for i in all_cards if i > card_count_total - cards_aside]"
            }
          }
        },
        {
          "set": {
            "key": "deck",
            "value": []
          }
        }
      ],
      "text": "The cards are shuffled. Each player receives {hand_size} cards in private; {cards_aside} cards are set aside face down."
    },
    {
      "use": "sync",
      "phase": "play",
      "label": "your view",
      "mode": "self",
      "to": "all",
      "text": "Your hand and standing:"
    },
    {
      "use": "update",
      "phase": "play",
      "label": "seat A prepares",
      "when": {
        "calc": "deal_active and not (first_orbit and leader_seat > 1)"
      },
      "do": [
        {
          "set": {
            "key": "pile_kind",
            "value": "empty",
            "if": {
              "calc": "last_player == 1 and pile_kind != 'empty'"
            },
            "text": "Both other seats passed: the pile is cleared and seat A must lead."
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
            "key": "resolved",
            "value": false
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 1"
            },
            "key": "offer",
            "value": {
              "calc": "(['pass'] if pile_kind != 'empty' else []) + [card_names[a - 1] for a in you.hand if pile_kind == 'empty' or (pile_kind == 'single' and a > pile_value)] + [card_names[a - 1] + ' ' + card_names[b - 1] for a in you.hand for b in you.hand if a < b and int((a + suit_count - 1) / suit_count) == int((b + suit_count - 1) / suit_count) and (pile_kind == 'empty' or (pile_kind == 'pair' and b > pile_value))] + [card_names[a - 1] + ' ' + card_names[b - 1] + ' ' + card_names[c - 1] for a in you.hand for b in you.hand for c in you.hand if a < b and b < c and int((a + suit_count - 1) / suit_count) == int((c + suit_count - 1) / suit_count) and (pile_kind in ['empty', 'single', 'pair'] or (pile_kind == 'triple' and c > pile_value))] + [card_names[a - 1] + ' ' + card_names[b - 1] + ' ' + card_names[c - 1] for a in you.hand for b in you.hand for c in you.hand if int((b + suit_count - 1) / suit_count) == int((a + suit_count - 1) / suit_count) + 1 and int((c + suit_count - 1) / suit_count) == int((b + suit_count - 1) / suit_count) + 1 and (pile_kind == 'empty' or (pile_kind == 'run' and c > pile_value))]"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "play",
      "label": "seat A plays",
      "when": {
        "calc": "deal_active and not (first_orbit and leader_seat > 1)"
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
        "bind": "a1"
      },
      "text": "Your turn, seat A. The pile holds: {pile_kind} (value {pile_value}). Choose one of the offered plays, written as card numbers separated by spaces, or 'pass' if it is offered. When the pile is empty you must lead and cannot pass."
    },
    {
      "use": "update",
      "phase": "play",
      "label": "seat A's play resolves",
      "when": {
        "prose": "The answer is not 'pass', every named card is in seat 1's hand, the cards form a single, a pair (2 cards, same rank floor((c+2)/3)), a triple (3 same rank) or a run (3 cards of three consecutive ranks without wrap), and either pile_kind is empty, or the kind equals pile_kind with highest card > pile_value, or it is a triple played on a single or pair."
      },
      "do": [
        {
          "set": {
            "key": "played",
            "value": {
              "calc": "[c for c in players[0].hand if (' ' + card_names[c - 1] + ' ') in (' ' + $a1 + ' ')]"
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
              "calc": "[c for c in you.hand if c not in played]"
            },
            "if": {
              "calc": "len(played) > 0"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 1"
            },
            "key": "card_count",
            "value": {
              "calc": "len(you.hand)"
            },
            "if": {
              "calc": "len(played) > 0"
            }
          }
        },
        {
          "set": {
            "key": "pile_kind",
            "value": {
              "calc": "'single' if len(played) == 1 else ('pair' if len(played) == pair_size else ('triple' if int((played[0] + suit_count - 1) / suit_count) == int((played[triple_size - 1] + suit_count - 1) / suit_count) else 'run'))"
            },
            "if": {
              "calc": "len(played) > 0"
            }
          }
        },
        {
          "set": {
            "key": "pile_value",
            "value": {
              "calc": "max(played)"
            },
            "if": {
              "calc": "len(played) > 0"
            }
          }
        },
        {
          "set": {
            "key": "last_player",
            "value": 1,
            "if": {
              "calc": "len(played) > 0"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 1"
            },
            "key": "last_action",
            "value": {
              "calc": "'played ' + $a1"
            },
            "if": {
              "calc": "len(played) > 0"
            },
            "text": "Seat A {value}."
          }
        },
        {
          "set": {
            "key": "resolved",
            "value": {
              "calc": "len(played) > 0"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "play",
      "label": "after seat A",
      "when": {
        "calc": "deal_active and not (first_orbit and leader_seat > 1)"
      },
      "do": [
        {
          "set": {
            "key": "forced",
            "value": {
              "calc": "(not resolved) and pile_kind == 'empty'"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 1"
            },
            "key": "last_action",
            "value": "pass",
            "if": {
              "calc": "not resolved and not forced"
            },
            "text": "Seat A passes."
          }
        },
        {
          "set": {
            "key": "played",
            "value": {
              "calc": "[min(players[0].hand)]"
            },
            "if": {
              "calc": "forced"
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
              "calc": "[c for c in you.hand if c not in played]"
            },
            "if": {
              "calc": "forced"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 1"
            },
            "key": "card_count",
            "value": {
              "calc": "len(you.hand)"
            },
            "if": {
              "calc": "forced"
            }
          }
        },
        {
          "set": {
            "key": "pile_kind",
            "value": "single",
            "if": {
              "calc": "forced"
            }
          }
        },
        {
          "set": {
            "key": "pile_value",
            "value": {
              "calc": "played[0]"
            },
            "if": {
              "calc": "forced"
            },
            "text": "Seat A had to lead and plays its lowest card, {value}, as a single."
          }
        },
        {
          "set": {
            "key": "last_player",
            "value": 1,
            "if": {
              "calc": "forced"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 1"
            },
            "key": "last_action",
            "value": {
              "calc": "'played ' + card_names[played[0] - 1]"
            },
            "if": {
              "calc": "forced"
            }
          }
        },
        {
          "adjust": {
            "player": 1,
            "key": "deals_won",
            "value": 1,
            "if": {
              "calc": "players[0].card_count == 0"
            },
            "text": "Seat A played its last card and wins deal {deal_number}."
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat != 1"
            },
            "key": "penalty",
            "value": {
              "calc": "(you.card_count + count(c >= two_lowest_card for c in you.hand) * two_extra_penalty) * (double_factor if you.card_count >= double_threshold else 1)"
            },
            "if": {
              "calc": "players[0].card_count == 0"
            },
            "text": "Seat {player} takes {value} penalty points."
          }
        },
        {
          "adjust": {
            "player": 1,
            "key": "penalty",
            "value": {
              "calc": "winner_penalty"
            },
            "if": {
              "calc": "players[0].card_count == 0"
            }
          }
        },
        {
          "set": {
            "key": "deal_active",
            "value": false,
            "if": {
              "calc": "players[0].card_count == 0"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "play",
      "label": "seat B prepares",
      "when": {
        "calc": "deal_active and not (first_orbit and leader_seat > 2)"
      },
      "do": [
        {
          "set": {
            "key": "pile_kind",
            "value": "empty",
            "if": {
              "calc": "last_player == 2 and pile_kind != 'empty'"
            },
            "text": "Both other seats passed: the pile is cleared and seat B must lead."
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
            "key": "resolved",
            "value": false
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 2"
            },
            "key": "offer",
            "value": {
              "calc": "(['pass'] if pile_kind != 'empty' else []) + [card_names[a - 1] for a in you.hand if pile_kind == 'empty' or (pile_kind == 'single' and a > pile_value)] + [card_names[a - 1] + ' ' + card_names[b - 1] for a in you.hand for b in you.hand if a < b and int((a + suit_count - 1) / suit_count) == int((b + suit_count - 1) / suit_count) and (pile_kind == 'empty' or (pile_kind == 'pair' and b > pile_value))] + [card_names[a - 1] + ' ' + card_names[b - 1] + ' ' + card_names[c - 1] for a in you.hand for b in you.hand for c in you.hand if a < b and b < c and int((a + suit_count - 1) / suit_count) == int((c + suit_count - 1) / suit_count) and (pile_kind in ['empty', 'single', 'pair'] or (pile_kind == 'triple' and c > pile_value))] + [card_names[a - 1] + ' ' + card_names[b - 1] + ' ' + card_names[c - 1] for a in you.hand for b in you.hand for c in you.hand if int((b + suit_count - 1) / suit_count) == int((a + suit_count - 1) / suit_count) + 1 and int((c + suit_count - 1) / suit_count) == int((b + suit_count - 1) / suit_count) + 1 and (pile_kind == 'empty' or (pile_kind == 'run' and c > pile_value))]"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "play",
      "label": "seat B plays",
      "when": {
        "calc": "deal_active and not (first_orbit and leader_seat > 2)"
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
        "bind": "a2"
      },
      "text": "Your turn, seat B. The pile holds: {pile_kind} (value {pile_value}). Choose one of the offered plays, written as card numbers separated by spaces, or 'pass' if it is offered. When the pile is empty you must lead and cannot pass."
    },
    {
      "use": "update",
      "phase": "play",
      "label": "seat B's play resolves",
      "when": {
        "prose": "The answer is not 'pass', every named card is in seat 2's hand, the cards form a single, pair, triple or run (ranks floor((c+2)/3), runs without wrap), and either pile_kind is empty, or the kind equals pile_kind with highest card > pile_value, or it is a triple played on a single or pair."
      },
      "do": [
        {
          "set": {
            "key": "played",
            "value": {
              "calc": "[c for c in players[1].hand if (' ' + card_names[c - 1] + ' ') in (' ' + $a2 + ' ')]"
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
              "calc": "[c for c in you.hand if c not in played]"
            },
            "if": {
              "calc": "len(played) > 0"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 2"
            },
            "key": "card_count",
            "value": {
              "calc": "len(you.hand)"
            },
            "if": {
              "calc": "len(played) > 0"
            }
          }
        },
        {
          "set": {
            "key": "pile_kind",
            "value": {
              "calc": "'single' if len(played) == 1 else ('pair' if len(played) == pair_size else ('triple' if int((played[0] + suit_count - 1) / suit_count) == int((played[triple_size - 1] + suit_count - 1) / suit_count) else 'run'))"
            },
            "if": {
              "calc": "len(played) > 0"
            }
          }
        },
        {
          "set": {
            "key": "pile_value",
            "value": {
              "calc": "max(played)"
            },
            "if": {
              "calc": "len(played) > 0"
            }
          }
        },
        {
          "set": {
            "key": "last_player",
            "value": 2,
            "if": {
              "calc": "len(played) > 0"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 2"
            },
            "key": "last_action",
            "value": {
              "calc": "'played ' + $a2"
            },
            "if": {
              "calc": "len(played) > 0"
            },
            "text": "Seat B {value}."
          }
        },
        {
          "set": {
            "key": "resolved",
            "value": {
              "calc": "len(played) > 0"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "play",
      "label": "after seat B",
      "when": {
        "calc": "deal_active and not (first_orbit and leader_seat > 2)"
      },
      "do": [
        {
          "set": {
            "key": "forced",
            "value": {
              "calc": "(not resolved) and pile_kind == 'empty'"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 2"
            },
            "key": "last_action",
            "value": "pass",
            "if": {
              "calc": "not resolved and not forced"
            },
            "text": "Seat B passes."
          }
        },
        {
          "set": {
            "key": "played",
            "value": {
              "calc": "[min(players[1].hand)]"
            },
            "if": {
              "calc": "forced"
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
              "calc": "[c for c in you.hand if c not in played]"
            },
            "if": {
              "calc": "forced"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 2"
            },
            "key": "card_count",
            "value": {
              "calc": "len(you.hand)"
            },
            "if": {
              "calc": "forced"
            }
          }
        },
        {
          "set": {
            "key": "pile_kind",
            "value": "single",
            "if": {
              "calc": "forced"
            }
          }
        },
        {
          "set": {
            "key": "pile_value",
            "value": {
              "calc": "played[0]"
            },
            "if": {
              "calc": "forced"
            },
            "text": "Seat B had to lead and plays its lowest card, {value}, as a single."
          }
        },
        {
          "set": {
            "key": "last_player",
            "value": 2,
            "if": {
              "calc": "forced"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 2"
            },
            "key": "last_action",
            "value": {
              "calc": "'played ' + card_names[played[0] - 1]"
            },
            "if": {
              "calc": "forced"
            }
          }
        },
        {
          "adjust": {
            "player": 2,
            "key": "deals_won",
            "value": 1,
            "if": {
              "calc": "players[1].card_count == 0"
            },
            "text": "Seat B played its last card and wins deal {deal_number}."
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat != 2"
            },
            "key": "penalty",
            "value": {
              "calc": "(you.card_count + count(c >= two_lowest_card for c in you.hand) * two_extra_penalty) * (double_factor if you.card_count >= double_threshold else 1)"
            },
            "if": {
              "calc": "players[1].card_count == 0"
            },
            "text": "Seat {player} takes {value} penalty points."
          }
        },
        {
          "adjust": {
            "player": 2,
            "key": "penalty",
            "value": {
              "calc": "winner_penalty"
            },
            "if": {
              "calc": "players[1].card_count == 0"
            }
          }
        },
        {
          "set": {
            "key": "deal_active",
            "value": false,
            "if": {
              "calc": "players[1].card_count == 0"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "play",
      "label": "seat C prepares",
      "when": {
        "calc": "deal_active and not (first_orbit and leader_seat > 3)"
      },
      "do": [
        {
          "set": {
            "key": "pile_kind",
            "value": "empty",
            "if": {
              "calc": "last_player == 3 and pile_kind != 'empty'"
            },
            "text": "Both other seats passed: the pile is cleared and seat C must lead."
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
            "key": "resolved",
            "value": false
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 3"
            },
            "key": "offer",
            "value": {
              "calc": "(['pass'] if pile_kind != 'empty' else []) + [card_names[a - 1] for a in you.hand if pile_kind == 'empty' or (pile_kind == 'single' and a > pile_value)] + [card_names[a - 1] + ' ' + card_names[b - 1] for a in you.hand for b in you.hand if a < b and int((a + suit_count - 1) / suit_count) == int((b + suit_count - 1) / suit_count) and (pile_kind == 'empty' or (pile_kind == 'pair' and b > pile_value))] + [card_names[a - 1] + ' ' + card_names[b - 1] + ' ' + card_names[c - 1] for a in you.hand for b in you.hand for c in you.hand if a < b and b < c and int((a + suit_count - 1) / suit_count) == int((c + suit_count - 1) / suit_count) and (pile_kind in ['empty', 'single', 'pair'] or (pile_kind == 'triple' and c > pile_value))] + [card_names[a - 1] + ' ' + card_names[b - 1] + ' ' + card_names[c - 1] for a in you.hand for b in you.hand for c in you.hand if int((b + suit_count - 1) / suit_count) == int((a + suit_count - 1) / suit_count) + 1 and int((c + suit_count - 1) / suit_count) == int((b + suit_count - 1) / suit_count) + 1 and (pile_kind == 'empty' or (pile_kind == 'run' and c > pile_value))]"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "play",
      "label": "seat C plays",
      "when": {
        "calc": "deal_active and not (first_orbit and leader_seat > 3)"
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
        "bind": "a3"
      },
      "text": "Your turn, seat C. The pile holds: {pile_kind} (value {pile_value}). Choose one of the offered plays, written as card numbers separated by spaces, or 'pass' if it is offered. When the pile is empty you must lead and cannot pass."
    },
    {
      "use": "update",
      "phase": "play",
      "label": "seat C's play resolves",
      "when": {
        "prose": "The answer is not 'pass', every named card is in seat 3's hand, the cards form a single, pair, triple or run (ranks floor((c+2)/3), runs without wrap), and either pile_kind is empty, or the kind equals pile_kind with highest card > pile_value, or it is a triple played on a single or pair."
      },
      "do": [
        {
          "set": {
            "key": "played",
            "value": {
              "calc": "[c for c in players[2].hand if (' ' + card_names[c - 1] + ' ') in (' ' + $a3 + ' ')]"
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
              "calc": "[c for c in you.hand if c not in played]"
            },
            "if": {
              "calc": "len(played) > 0"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 3"
            },
            "key": "card_count",
            "value": {
              "calc": "len(you.hand)"
            },
            "if": {
              "calc": "len(played) > 0"
            }
          }
        },
        {
          "set": {
            "key": "pile_kind",
            "value": {
              "calc": "'single' if len(played) == 1 else ('pair' if len(played) == pair_size else ('triple' if int((played[0] + suit_count - 1) / suit_count) == int((played[triple_size - 1] + suit_count - 1) / suit_count) else 'run'))"
            },
            "if": {
              "calc": "len(played) > 0"
            }
          }
        },
        {
          "set": {
            "key": "pile_value",
            "value": {
              "calc": "max(played)"
            },
            "if": {
              "calc": "len(played) > 0"
            }
          }
        },
        {
          "set": {
            "key": "last_player",
            "value": 3,
            "if": {
              "calc": "len(played) > 0"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 3"
            },
            "key": "last_action",
            "value": {
              "calc": "'played ' + $a3"
            },
            "if": {
              "calc": "len(played) > 0"
            },
            "text": "Seat C {value}."
          }
        },
        {
          "set": {
            "key": "resolved",
            "value": {
              "calc": "len(played) > 0"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "play",
      "label": "after seat C",
      "when": {
        "calc": "deal_active and not (first_orbit and leader_seat > 3)"
      },
      "do": [
        {
          "set": {
            "key": "forced",
            "value": {
              "calc": "(not resolved) and pile_kind == 'empty'"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 3"
            },
            "key": "last_action",
            "value": "pass",
            "if": {
              "calc": "not resolved and not forced"
            },
            "text": "Seat C passes."
          }
        },
        {
          "set": {
            "key": "played",
            "value": {
              "calc": "[min(players[2].hand)]"
            },
            "if": {
              "calc": "forced"
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
              "calc": "[c for c in you.hand if c not in played]"
            },
            "if": {
              "calc": "forced"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 3"
            },
            "key": "card_count",
            "value": {
              "calc": "len(you.hand)"
            },
            "if": {
              "calc": "forced"
            }
          }
        },
        {
          "set": {
            "key": "pile_kind",
            "value": "single",
            "if": {
              "calc": "forced"
            }
          }
        },
        {
          "set": {
            "key": "pile_value",
            "value": {
              "calc": "played[0]"
            },
            "if": {
              "calc": "forced"
            },
            "text": "Seat C had to lead and plays its lowest card, {value}, as a single."
          }
        },
        {
          "set": {
            "key": "last_player",
            "value": 3,
            "if": {
              "calc": "forced"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 3"
            },
            "key": "last_action",
            "value": {
              "calc": "'played ' + card_names[played[0] - 1]"
            },
            "if": {
              "calc": "forced"
            }
          }
        },
        {
          "adjust": {
            "player": 3,
            "key": "deals_won",
            "value": 1,
            "if": {
              "calc": "players[2].card_count == 0"
            },
            "text": "Seat C played its last card and wins deal {deal_number}."
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat != 3"
            },
            "key": "penalty",
            "value": {
              "calc": "(you.card_count + count(c >= two_lowest_card for c in you.hand) * two_extra_penalty) * (double_factor if you.card_count >= double_threshold else 1)"
            },
            "if": {
              "calc": "players[2].card_count == 0"
            },
            "text": "Seat {player} takes {value} penalty points."
          }
        },
        {
          "adjust": {
            "player": 3,
            "key": "penalty",
            "value": {
              "calc": "winner_penalty"
            },
            "if": {
              "calc": "players[2].card_count == 0"
            }
          }
        },
        {
          "set": {
            "key": "deal_active",
            "value": false,
            "if": {
              "calc": "players[2].card_count == 0"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "orbit",
      "label": "end of orbit",
      "do": [
        {
          "adjust": {
            "key": "orbit",
            "value": 1
          }
        },
        {
          "set": {
            "key": "first_orbit",
            "value": false
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "penalty",
            "value": {
              "calc": "(you.card_count + count(c >= two_lowest_card for c in you.hand) * two_extra_penalty) * (double_factor if you.card_count >= double_threshold else 1)"
            },
            "if": {
              "calc": "orbit >= max_orbits and deal_active"
            },
            "text": "Orbit limit reached: seat {player} takes {value} penalty points."
          }
        },
        {
          "set": {
            "key": "deal_active",
            "value": false,
            "if": {
              "calc": "orbit >= max_orbits"
            }
          }
        }
      ],
      "text": "Orbit {orbit} complete. Penalty totals: A {players[0].penalty}, B {players[1].penalty}, C {players[2].penalty}."
    },
    {
      "use": "check",
      "phase": "orbit",
      "label": "is the match over",
      "when": {
        "calc": "(deal_number >= deals and not deal_active) or orbit >= max_orbits"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "(deal_number >= deals and not deal_active) or orbit >= max_orbits"
      },
      "rank_by": "0 - you.penalty",
      "text": "Winner: {result} (lowest total penalty). Final penalties: A {players[0].penalty}, B {players[1].penalty}, C {players[2].penalty}; deals won: A {players[0].deals_won}, B {players[1].deals_won}, C {players[2].deals_won}."
    }
  },
  "limits": {
    "rounds": 40,
    "rounds_max": 40,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "CARDS. There are {card_count_total} cards numbered 1 to {card_count_total}. A card's rank is (card + 2) divided by 3, rounded down, giving ranks 1 to {rank_count}. Its suit is card - 3 x (rank - 1), giving suits 1 to {suit_count}. For example, card 14 has rank 5, suit 2. A higher card number always beats a lower one. Rank {two_rank} (cards {two_lowest_card}, 29, 30) are called 'twos'.\n\nSEATS. The players sit as A (seat 1), B (seat 2) and C (seat 3). Turn order is always A, then B, then C, then A again.\n\nMATCH. The match has {deals} deals and at most {max_orbits} orbits. An orbit is one turn for each seat in order.\n\nDEALING. At the start of each deal, all {card_count_total} cards are shuffled. Each player is dealt {hand_size}, privately. The remaining {cards_aside} cards are set aside face-down; nobody sees them during the deal. Every player's card count is public at all times.\n\nCOMBINATIONS. There are four kinds:\n- Single: one card.\n- Pair: {pair_size} cards of the same rank (e.g. 4 5 is a pair of rank 2).\n- Triple: {triple_size} cards of the same rank (e.g. 4 5 6 is a triple of rank 2).\n- Run: {run_length} cards of three consecutive ranks, any suits. Ranks do not wrap around, so 9-10-1 is not a run.\nThe value of a combination is its highest card number.\n\nTHE PILE. The pile holds a current kind and a current value, or is empty.\n- When the pile is empty, the player whose turn it is must lead any combination. They may not pass.\n- When the pile is not empty, the player whose turn it is may pass, or may play a combination of the same kind with a higher value.\n- Bomb: a triple may be played on a single or a pair whatever its value. The pile's kind then becomes triple.\n- A triple on the pile can only be beaten by a higher triple.\n- A run can only be beaten by a higher run.\nPlayed cards are announced to everyone and removed from the game for the rest of the deal: they leave your hand, your card count drops by the number played, the pile's value becomes the highest card played, and you become the last player.\n\nON YOUR TURN you are offered exactly the plays you may legally make, each written as its card numbers in ascending order separated by spaces (e.g. '13 14'), plus 'pass' when the pile is not empty. Choose one of them.\n\nPASSING AND CLEARING. A player who passes may play again the next time their turn comes in the same trick. The engine records who made the last play. If play comes back round to that player because both others passed since their play, the pile is cleared and that player must lead.\n\nILLEGAL PLAYS. An illegal or malformed play counts as a pass. If the player was required to lead, their lowest-numbered card is played as a single instead.\n\nSTARTING A DEAL. In deal 1, seat A leads first. In deal 2, seat B leads first. In deal 3, seat C leads first. Seats before the leader in the first orbit of a deal do not act in that orbit.\n\nEND OF A DEAL. A deal ends the moment a player plays their last card. That player wins the deal (their deals won rises by 1), and the rest of that orbit is skipped. The next deal begins at the start of the next orbit.\n\nPENALTIES. Each non-winner receives a penalty equal to the number of cards left in their hand, plus {two_extra_penalty} for each two (rank {two_rank}, cards {two_lowest_card}-30) left in their hand; e.g. 3 cards including one two gives 4. If they have {double_threshold} or more cards left, this penalty is multiplied by {double_factor}; e.g. 7 cards with no twos gives 14. The deal winner receives {winner_penalty}. Penalties are added to each player's public running total.\n\nEND OF THE MATCH. The match ends after the third deal ends, or at the end of orbit {max_orbits}, whichever comes first. If orbit {max_orbits} ends during a deal, that deal is scored as if it had ended with no winner: every player receives a penalty under the rule above.\n\nWINNING. The player with the lowest total penalty after the match ends wins. If two or three players tie for the lowest total, they share the result (a draw)."
}
```
````
