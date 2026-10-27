# Task: write the XColos game file for "Duel Durak"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 2; set `meta.players` to {"min": 2, "max": 2, "suggested": 2} (the suggested size is the one the game plays best at).

CARDS. There are 36 cards with ids 0 to 35.
- Suit = floor(id/9): 0 Clubs, 1 Diamonds, 2 Hearts, 3 Spades.
- Rank = (id mod 9) + 6: 6, 7, 8, 9, 10, Jack 11, Queen 12, King 13, Ace 14.
- Two cards have the same rank when their ids are equal mod 9.

BEATING. A card d beats a card a if either:
(i) floor(d/9) = floor(a/9) and d > a, or
(ii) floor(d/9) = trump and floor(a/9) is not trump.

SETUP (before round 1):
- The deck 0..35 is shuffled once.
- Seat 1 gets shuffled positions 1-8 and seat 2 gets positions 9-16. Both hands are sorted ascending.
- Positions 17-36 (20 cards) form the set_aside pile. It is never seen and never drawn from.
- Each seat sees only its own hand. Both are told that each player holds 8 cards.
- Table values: trump = -1, attacker = none, bout = 0, discard = empty.

ROUND 1 (trump choice).
- Step A: Seat 2 chooses one pair of suits from these six: Clubs and Diamonds; Clubs and Hearts; Clubs and Spades; Diamonds and Hearts; Diamonds and Spades; Hearts and Spades. A missing or illegal answer means Clubs and Diamonds.
- Step B: Seat 1 chooses one suit of that pair. A missing or illegal answer means the first suit named. That suit becomes trump and is announced.
- First attacker: the seat holding the lowest-id card of the trump suit. If neither seat holds a trump, seat 2 attacks first.

ROUNDS 2 to 40 (one bout per round). The defender is the seat that is not the attacker.
- Step 1 (reset): table_cards = empty, attack_card = -1, defence_card = -1, throw_card = -1, defender_took = false.
- Step 2 (attack): The attacker chooses any card from their hand. A missing or illegal answer means their lowest-id card. The card moves from their hand to table_cards as attack_card and is shown to both players.
- Step 3 (defence options): The defender's options are TAKE, plus every card in the defender's hand that beats attack_card.
- Step 4 (defence): The defender chooses. A missing or illegal answer means TAKE. If they choose a card, it moves from their hand to table_cards as defence_card. If they choose TAKE, defender_took = true.
- Step 5 (throw-in options): The option list is built as follows.
  - Start with [PASS].
  - Only if (defender_took is true OR the defender holds at least 1 card) AND the attacker holds at least 1 card: for each card c in the attacker's hand, add c if c mod 9 = attack_card mod 9, or if defence_card is not -1 and c mod 9 = defence_card mod 9.
  - No other card is ever added. In particular, if the defender beat the attack with their last card, the list is only [PASS].
- Step 6 (throw-in): The attacker chooses one option. A missing or illegal answer means PASS. A chosen card moves from the attacker's hand to table_cards as throw_card and is shown. At most 1 card is thrown in per bout.
- Step 7 (second defence options): This step and Step 8 happen only if throw_card is not -1 and defender_took is false. The options are TAKE, plus every card in the defender's hand that beats throw_card.
- Step 8 (second defence): The defender chooses. A missing or illegal answer means TAKE. A chosen card moves from their hand to table_cards. TAKE sets defender_took = true.
- Step 9 (resolve):
  - If defender_took is true, all table_cards go into the defender's hand, sorted, and the attacker stays the attacker. The result is announced as 'taken'.
  - Otherwise all table_cards go to discard, the defender becomes the next attacker, and the result is announced as 'beaten off'.
- Step 10: Update both hand sizes, announce them, and set bout = bout + 1.
- Step 11 (end check):
  - If exactly one seat holds 0 cards, that seat wins and the game ends.
  - If both hold 0, the game is a draw.
- After round 40, the seat with fewer cards wins. Equal counts are a draw.

How the winner is decided: The first seat to hold 0 cards at an end check wins. If both seats hold 0 at the same check, the game is a draw. If round 40 ends with both still holding cards, the seat with fewer cards wins, and equal counts are a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Duel Durak (2 to 2 players, best with 2)

Two-player Durak with no drawing: one bout per round, each with one attack and at most one throw-in; the first player to empty their hand wins, or after round 40 the player with fewer cards wins.

STATE (every item below must exist in the file):
  - each player: hand (list, starts []); only its owner sees it. Card ids (0-35) the player holds, kept in ascending order.
  - each player: hand_size (number, starts 8); everyone sees it. Number of cards in hand. It is announced after every bout. Fewer is better, and 0 wins.
  - the table: deck (list, starts 'ids 0..35'); hidden from all players. The shuffled deck that the hands and the set-aside pile are dealt from.
  - the table: set_aside (list, starts []); hidden from all players. The 20 cards at shuffled positions 17-36. They are never seen and never drawn.
  - the table: suit_pair (text, starts ''); everyone sees it. The pair of suits seat 2 offers for trump.
  - the table: trump (number, starts -1); everyone sees it. The trump suit: 0 Clubs, 1 Diamonds, 2 Hearts, 3 Spades. It is -1 until chosen.
  - the table: attacker (number, starts 0); everyone sees it. The seat that attacks this bout (0 means none yet). The defender is the other seat.
  - the table: bout (number, starts 0); everyone sees it. Number of bouts completed.
  - the table: round_number (number, starts 0); everyone sees it. The current round. Round 1 is the trump choice, and rounds 2-40 are bouts.
  - the table: discard (list, starts []); everyone sees it. Cards from bouts that were beaten off.
  - the table: table_cards (list, starts []); everyone sees it. Cards played in the current bout.
  - the table: attack_card (number, starts -1); everyone sees it. The attacking card this bout.
  - the table: defence_card (number, starts -1); everyone sees it. The card that beat the attack card this bout.
  - the table: throw_card (number, starts -1); everyone sees it. The thrown-in card this bout.
  - the table: defender_took (bool, starts False); everyone sees it. Whether the defender chose TAKE this bout.
  - parameters, each kept as a table attribute: deck_size = 36, suits = 4, cards_per_suit = 9, rank_offset = 6, hand_size = 8, set_aside_size = 20, seat1_first_position = 1, seat1_last_position = 8, seat2_first_position = 9, seat2_last_position = 16, set_aside_first_position = 17, set_aside_last_position = 36, trump_unset = -1, card_unset = -1, max_throw_ins_per_bout = 1, trump_round = 1, first_bout_round = 2, last_round = 40, suit_pairs = 6

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Shuffle the deck of ids 0..35 once.
  2. Deal shuffled positions 1-8 into seat 1's hand and positions 9-16 into seat 2's hand. Sort both hands ascending.
  3. Put positions 17-36 (20 cards) into set_aside. They are never seen or drawn.
  4. Each seat sees only its own hand. Tell both players that each player holds 8 cards (hand_size = 8 each).
  5. Set trump = -1, attacker = 0 (none), bout = 0, discard = empty, round_number = 0.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round_number += 1
  2. [ask] seat 2 (only when round_number = 1) answers: one of: Clubs and Diamonds; Clubs and Hearts; Clubs and Spades; Diamonds and Hearts; Diamonds and Spades; Hearts and Spades. A missing or illegal answer means Clubs and Diamonds.. What happens: suit_pair = the chosen pair, announced
  3. [ask] seat 1 (only when round_number = 1) answers: one of the two suits in suit_pair. A missing or illegal answer means the first suit named.. What happens: trump = the chosen suit's number (0-3), announced to both
  4. [update] all players (only when round_number = 1). What happens: attacker = the seat whose hand holds the lowest id c with floor(c/9) = trump. If neither seat holds a trump card, attacker = 2. Announced.
  5. [update] all players (only when round_number >= 2). What happens: Step 1: table_cards = [], attack_card = -1, defence_card = -1, throw_card = -1, defender_took = false
  6. [ask] the attacker (only when round_number >= 2) answers: any card in the attacker's hand. A missing or illegal answer means their lowest id.. What happens: Step 2: remove the card from attacker.hand, append it to table_cards, set attack_card = card, and show it to both players
  7. [ask] the defender (only when round_number >= 2) answers: TAKE, or any card d in the defender's hand that beats attack_card [(floor(d/9) = floor(attack_card/9) and d > attack_card) or (floor(d/9) = trump and floor(attack_card/9) != trump)]. A missing or illegal answer means TAKE.. What happens: Steps 3-4: if a card is chosen, remove it from defender.hand, append it to table_cards, set defence_card = card, and show it. If TAKE, defender_took = true.
  8. [ask] the attacker (only when round_number >= 2) answers: PASS, plus (only if (defender_took or the defender's hand_size >= 1) and the attacker's hand_size >= 1) every card c in the attacker's hand with c mod 9 = attack_card mod 9, or with defence_card != -1 and c mod 9 = defence_card mod 9. A missing or illegal answer means PASS.. What happens: Steps 5-6: if a card is chosen, remove it from attacker.hand, append it to table_cards, set throw_card = card, and show it
  9. [ask] the defender (only when round_number >= 2 and throw_card != -1 and defender_took = false) answers: TAKE, or any card in the defender's hand that beats throw_card (same beating rule). A missing or illegal answer means TAKE.. What happens: Steps 7-8: if a card is chosen, remove it from defender.hand and append it to table_cards. If TAKE, defender_took = true.
  10. [update] all players (only when round_number >= 2). What happens: Step 9: if defender_took, append all table_cards to defender.hand (sorted ascending), keep the attacker, and announce 'taken'. Otherwise append table_cards to discard, set attacker = the defender's seat, and announce 'beaten off'. Then table_cards = [].
  11. [update] all players (only when round_number >= 2). What happens: Step 10: hand_size = length of hand for both seats, announced. bout += 1.
  12. [check] all players. What happens: Step 11: end if round_number >= 2 and any seat has hand_size = 0, or if round_number = 40. Otherwise continue.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. Card id c has suit floor(c/9) (0 Clubs, 1 Diamonds, 2 Hearts, 3 Spades) and rank (c mod 9) + 6. Two cards have the same rank when their ids are equal mod 9.
  R2. Card d beats card a when floor(d/9) = floor(a/9) and d > a, or when floor(d/9) = trump and floor(a/9) != trump. For example, with trump = 3, card 27 beats card 8, card 5 beats card 3, and card 3 does not beat card 5.
  R3. At setup, seat 1 holds shuffled positions 1-8 and seat 2 holds positions 9-16. Each has hand_size = 8, and the 20 remaining cards go to set_aside, which is never drawn.
  R4. At setup, trump = -1, attacker = 0 (none), bout = 0 and discard is empty.
  R5. In round 1, seat 2 picks one of 6 suit pairs. A missing or illegal answer gives Clubs and Diamonds.
  R6. In round 1, seat 1 picks one suit of that pair as trump. A missing or illegal answer gives the first suit named. Trump is announced.
  R7. After trump is set, the attacker is the seat holding the lowest-id trump card. If neither seat holds a trump card, seat 2 attacks first.
  R8. At the start of each bout, table_cards = [], attack_card = -1, defence_card = -1, throw_card = -1 and defender_took = false.
  R9. When the attacker attacks, the chosen card leaves their hand, goes to table_cards as attack_card and is shown. A missing or illegal answer plays their lowest id.
  R10. The defender is offered TAKE plus exactly the cards in their hand that beat attack_card. A missing or illegal answer means TAKE.
  R11. When the defender plays a card, it leaves their hand, goes to table_cards and becomes defence_card. When the defender chooses TAKE, defender_took becomes true.
  R12. The throw-in options are PASS plus attacker cards matching attack_card mod 9 or defence_card mod 9 (when defence_card != -1). Cards are added only if (defender_took or the defender holds >= 1 card) and the attacker holds >= 1 card.
  R13. When the defender beat the attack with their last card, the throw-in options are only PASS.
  R14. At most 1 card is thrown in per bout. A thrown card leaves the attacker's hand, goes to table_cards as throw_card and is shown. A missing or illegal answer means PASS.
  R15. When throw_card != -1 and defender_took is false, the defender is offered TAKE plus the cards in their hand that beat throw_card. A chosen card goes to table_cards, TAKE sets defender_took = true, and a missing or illegal answer means TAKE.
  R16. When throw_card != -1 and defender_took is already true, there is no second defence.
  R17. When defender_took is true at resolve, all table_cards go into the defender's hand, the attacker stays the attacker, and 'taken' is announced.
  R18. When defender_took is false at resolve, all table_cards go to discard, the defender becomes the attacker, and 'beaten off' is announced.
  R19. After each bout, both hand_size values are updated and announced, and bout increases by 1.
  R20. When exactly one seat has hand_size = 0 at an end check, that seat wins and the game ends.
  R21. When both seats have hand_size = 0 at an end check, the game ends in a draw.
  R22. When round 40 ends with both seats holding cards, the seat with fewer cards wins, and equal counts are a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Round 1, suit pair | asked: seat 2 | options: Clubs and Diamonds; Clubs and Hearts; Clubs and Spades; Diamonds and Hearts; Diamonds and Spades; Hearts and Spades
  - Round 1, trump suit | asked: seat 1 | options: the two suits of suit_pair
  - Attack | asked: the attacker | options: every card in the attacker's hand
  - Defence | asked: the defender | options: TAKE, plus every card in the defender's hand that beats attack_card
  - Throw-in | asked: the attacker | options: If (defender_took or the defender holds >= 1 card) and the attacker holds >= 1 card: PASS plus attacker cards with the same rank (id mod 9) as attack_card or as defence_card (if one was played). Otherwise, including when the defender beat the attack with their last card: PASS only.
  - Second defence | asked: the defender, only when throw_card != -1 and defender_took = false | options: TAKE, plus every card in the defender's hand that beats throw_card

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: (round_number >= 2 and (seat1.hand_size = 0 or seat2.hand_size = 0)) or round_number = 40
  - each player's standing: 0 - you.hand_size (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Fewer cards in hand ranks higher. A seat at 0 cards while the other holds cards wins. Both at 0 is a shared result (draw). After round 40 the seat with fewer cards wins, and equal counts share (draw).
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

- each player: `hand_size` (number, visible: public, starts 8): Number of cards in hand. It is announced after every bout. Fewer is better, and 0 wins.
- the table: `trump` (number, visible: public, starts -1): The trump suit: 0 Clubs, 1 Diamonds, 2 Hearts, 3 Spades. It is -1 until chosen.
- the table: `attacker` (number, visible: public, starts 0): The seat that attacks this bout (0 means none yet). The defender is the other seat.
- the table: `bout` (number, visible: public, starts 0): Number of bouts completed.
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 36, suits = 4, cards_per_suit = 9, rank_offset = 6, hand_size = 8, set_aside_size = 20, seat1_first_position = 1, seat1_last_position = 8, seat2_first_position = 9, seat2_last_position = 16, set_aside_first_position = 17, set_aside_last_position = 36, trump_unset = -1, card_unset = -1, max_throw_ins_per_bout = 1, trump_round = 1, first_bout_round = 2, last_round = 40, suit_pairs = 6
- the game ends with ONE ending whose `rank_by` is `0 - you.hand_size`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
