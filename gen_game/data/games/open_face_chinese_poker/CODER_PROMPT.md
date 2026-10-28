# Task: write the XColos game file for "Duplicate Open-Face Pairs"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 2; set `meta.players` to {"min": 2, "max": 2, "suggested": 2} (the suggested size is the one the game plays best at).

DECK: 32 cards: values 1 to 8, four copies of each value. There are no suits.

MATCH: 4 hands of 5 rounds each, 20 rounds in total. At the start of hand 1 the deck is shuffled and its order is fixed; hands 1 and 2 both use this order. At the start of hand 3 it is shuffled again; hands 3 and 4 both use the new order.

SEATS: In each round r of a hand (r = 1 to 5), Seat X receives deck positions 6r-5, 6r-4 and 6r-3, and Seat Y receives positions 6r-2, 6r-1 and 6r. Positions 31 and 32 are never used. In hands 1 and 3, Player A is Seat X and Player B is Seat Y. In hands 2 and 4 they swap: B is Seat X and A is Seat Y. So in hand 2 each player is dealt exactly the cards the other was dealt in hand 1, round by round, and likewise for hand 4 and hand 3.

ROWS: Each player builds a Front row (1 slot), a Middle row (2 slots) and a Back row (2 slots).

EACH ROUND:
(1) Deal: each player privately receives their 3 cards for this round.
(2) Card choice: at the same moment, each player secretly chooses 1 of their 3 cards to keep.
(3) Row choice: at the same moment, each player secretly names a row (Front, Middle or Back) for the kept card. If the named row is full, the card goes to the first row that is not full, checking in the order Back, Middle, Front.
(4) The 2 unkept cards are discarded. Discards are never shown to the opponent.
(5) Reveal: both kept cards are announced face up, with the row each went to.

After round 5 each player has exactly 5 placed cards, and the hand is scored.

ROW STRENGTH:
- Front = 2 x its card value.
- Middle and Back = the sum of the two card values, plus 100 if the two values are equal (a pair).

FOUL: a hand fouls if Front strength > Middle strength, or Middle strength > Back strength. Equal strengths are allowed.

ROYALTIES (non-fouling players only):
- Front card value 7 or 8: +1.
- Middle pair: +2.
- Back pair: +1.

SCORING EACH HAND:
- If neither player fouls, compare each row. The higher strength scores 1 point for its owner; equal strengths score nothing. A player who wins all three rows scores 3 more points (scoop). Each player then adds their own royalties.
- If exactly one player fouls, the other scores 6 plus their own royalties, and the fouler scores 0.
- If both foul, both score 0.
The hand scores are added to the match totals. All row strengths, both foul results and both hand scores are announced. Rows are then cleared for the next hand.

INFORMATION: Each player sees their own dealt cards and every revealed placement. Players may use anything seen in earlier hands. In particular, in hands 2 and 4 you know exactly which 3 cards your opponent is offered each round, because they are the cards you were offered in the previous hand. In hands 1 and 3 you know the opponent was offered the cards you are about to receive in the next hand.

BUILD NOTE (engine encoding):
- Attributes per player: F, M1, M2, B1, B2 (0 = empty), a hand list, a total, a chosen card and a chosen row. Plus one shared deck list. 19 in all.
- Dealing copies cards by position: take a card from the front of the deck list and append it to the back, so the order survives for the mirrored hand. At the end of each odd hand, 2 more cards are rotated so the deck returns to its starting order.
- At scoring: F becomes 2F, M1 becomes M1+M2+100*(M1==M2), and B1 becomes B1+B2+100*(B1==B2). Foul tests, row comparisons, scoop and royalties are then single arithmetic expressions on these values.

How the winner is decided: After round 20, the player with the higher match total (the sum of their four hand scores) wins. Equal totals are a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Duplicate Open-Face Pairs (2 to 2 players, best with 2)

Two players build 1-2-2 card rows from mirrored deals over 4 hands. Rows must not foul. Players score row wins, scoops and royalties, and both players face the same cards in each pair of hands.

STATE (every item below must exist in the file):
  - each player: front (number, starts 0); everyone sees it. Card in the Front slot (0 = empty). At scoring it becomes the Front strength, 2 x value.
  - each player: mid1 (number, starts 0); everyone sees it. First Middle card (0 = empty). At scoring it becomes the Middle strength.
  - each player: mid2 (number, starts 0); everyone sees it. Second Middle card (0 = empty).
  - each player: back1 (number, starts 0); everyone sees it. First Back card (0 = empty). At scoring it becomes the Back strength.
  - each player: back2 (number, starts 0); everyone sees it. Second Back card (0 = empty).
  - each player: hand (list, starts []); only its owner sees it. The 3 cards dealt to this player this round. The unkept cards are discarded from here unseen.
  - each player: chosen_card (number, starts 0); only its owner sees it. The card kept this round.
  - each player: chosen_row (text, starts ''); only its owner sees it. The row named this round: Front, Middle or Back.
  - each player: fouled (bool, starts False); everyone sees it. Whether this player's rows fouled in the hand just scored.
  - each player: royalty (number, starts 0); everyone sees it. Royalties earned in the hand just scored (0 if fouled).
  - each player: hand_score (number, starts 0); everyone sees it. Points scored in the hand just scored.
  - each player: total (number, starts 0); everyone sees it. Match total: the sum of hand scores.
  - the table: deck (list, starts [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8]); hidden from all players. The 32-card deck in its fixed shuffled order. Dealing rotates cards from the front to the back, so the order survives for the mirrored hand.
  - the table: hand_number (number, starts 1); everyone sees it. Current hand, 1 to 4. Above 4 means the match is over.
  - the table: round_in_hand (number, starts 1); everyone sees it. Current round within the hand, 1 to 5.
  - the table: seat_strengths (list, starts [0, 0, 0, 0, 0, 0, 0, 0]); everyone sees it. Table copy of each player's strengths for comparison: [A front, A middle, A back, A fouled, B front, B middle, B back, B fouled].
  - parameters, each kept as a table attribute: deck_size = 32, card_value_min = 1, card_value_max = 8, copies_per_value = 4, hands = 4, rounds_per_hand = 5, total_rounds = 20, cards_per_seat_per_round = 3, cards_kept_per_round = 1, cards_discarded_per_round = 2, cards_used_per_hand = 30, unused_positions = 2, front_slots = 1, middle_slots = 2, back_slots = 2, front_multiplier = 2, pair_bonus = 100, row_win_points = 1, scoop_bonus = 3, foul_win_points = 6, front_royalty_min_value = 7, front_royalty = 1, middle_pair_royalty = 2, back_pair_royalty = 1

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Player A sits in seat 1 and Player B in seat 2.
  2. Each player's front, mid1, mid2, back1 and back2 are set to 0, and total is set to 0.
  3. The deck list holds 32 cards: values 1 to 8, four of each.
  4. hand_number is set to 1 and round_in_hand to 1.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] table. What happens: When round_in_hand == 1 and hand_number is 1 or 3: shuffle deck into a new random fixed order.
  2. [update] all players. What happens: Deal by position. Take the first 3 cards of deck, append them to the back of deck, and copy them into the Seat X player's hand. Then take the next 3 cards the same way into the Seat Y player's hand. Seat X is Player A when hand_number is odd and Player B when it is even; Seat Y is the other player.
  3. [sync] all players. What happens: Each player privately sees their own hand, all placed rows, hand_number and round_in_hand.
  4. [poll] all players answers: one of the 3 card values in your hand. What happens: chosen_card = the chosen value. Nobody sees the other's answer.
  5. [poll] all players answers: Front, Middle or Back. What happens: chosen_row = the named row. Nobody sees the other's answer.
  6. [update] all players. What happens: Place chosen_card in the first empty slot of chosen_row: front, else mid1 then mid2, else back1 then back2. If that row is full, place it in the first non-full row in the order Back, Middle, Front. Then empty hand: the 2 unkept cards are discarded unseen.
  7. [tell] all players. What happens: Announce both kept cards face up and the row each went to.
  8. [update] all players. What happens: Score the hand. front = 2*front. mid1 = mid1+mid2+100*(mid1==mid2), using the old values. back1 = back1+back2+100*(back1==back2), using the old values. fouled = (front > mid1) or (mid1 > back1). Copy front, mid1, back1 and fouled into seat_strengths. royalty = 0 if fouled, else (old front >= 7)*1 + (old mid1 == old mid2)*2 + (old back1 == old back2)*1. hand_score: if neither player fouled = rows won (1 per row with strictly higher strength than the opponent's) + 3 if all 3 rows won + royalty; if only the opponent fouled = 6 + royalty; if this player fouled = 0. total += hand_score.
  9. [tell] all players. What happens: Announce all six row strengths, both foul results and both hand scores.
  10. [update] table. What happens: If round_in_hand == 5: set every player's front, mid1, mid2, back1 and back2 to 0. If hand_number is odd, rotate 2 more cards from the front of deck to the back, so deck returns to its starting order. Then hand_number += 1 and round_in_hand = 1. Otherwise round_in_hand += 1.
  11. [check] table. What happens: End the game if hand_number > 4; otherwise continue.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. The deck has 32 cards, values 1 to 8 with four copies each, and no suits.
  R2. The match is 4 hands of 5 rounds, 20 rounds in total, and ends when hand_number exceeds 4.
  R3. When hand 1 or hand 3 begins, the deck is shuffled once. Hand 2 uses the same order as hand 1, and hand 4 the same order as hand 3.
  R4. In round r of a hand, Seat X receives deck positions 6r-5 to 6r-3 and Seat Y receives positions 6r-2 to 6r. Positions 31 and 32 are never dealt.
  R5. In hands 1 and 3 Player A is Seat X and Player B is Seat Y; in hands 2 and 4 B is Seat X and A is Seat Y.
  R6. When hand 2 or 4 is dealt, each player receives in each round exactly the 3 cards the other player received in that round of the previous hand.
  R7. Each round, both players simultaneously keep exactly 1 of their 3 dealt cards.
  R8. Each round, both players simultaneously name a row (Front, Middle or Back) for the kept card.
  R9. Front holds 1 card, Middle holds 2 and Back holds 2.
  R10. When the named row is full, the card goes to the first non-full row in the order Back, Middle, Front.
  R11. The 2 unkept cards are discarded and never shown to the opponent.
  R12. After the choices, both kept cards and the rows they went to are announced face up.
  R13. Front strength = 2 x the Front card value (for example, a Front 5 has strength 10).
  R14. Middle or Back strength = the sum of its two values, plus 100 if they are equal (for example, 4 and 4 = 108; 3 and 6 = 9).
  R15. A hand fouls when Front strength > Middle strength or Middle strength > Back strength; equal strengths do not foul.
  R16. A non-fouling player with a Front card of 7 or 8 earns a royalty of +1.
  R17. A non-fouling player with a Middle pair earns a royalty of +2.
  R18. A non-fouling player with a Back pair earns a royalty of +1.
  R19. When neither player fouls, each row with strictly higher strength scores 1 point for its owner, and equal rows score nothing.
  R20. When neither player fouls and a player wins all 3 rows, that player scores 3 extra points (a scoop), for 6 points before royalties.
  R21. When neither player fouls, each player adds their own royalties to their hand score.
  R22. When exactly one player fouls, the other scores 6 plus their royalties and the fouler scores 0.
  R23. When both players foul, both score 0 for the hand.
  R24. After each hand, each player's hand score is added to their total; all row strengths, both foul results and both hand scores are announced; and the rows are cleared.
  R25. When the match ends, the player with the higher total wins, and equal totals are a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Card choice: which card to keep | asked: both seats, simultaneously | options: Exactly the 3 card values in that seat's hand this round.
  - Row choice: which row for the kept card | asked: both seats, simultaneously | options: Front, Middle, Back. All three are always offered; a full row redirects by the Back, Middle, Front fallback.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: hand_number > 4
  - each player's standing: you.total (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their match total, the sum of their four hand scores. The higher total wins, and equal totals share the win (a draw).
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

- each player: `front` (number, visible: public, starts 0): Card in the Front slot (0 = empty). At scoring it becomes the Front strength, 2 x value.
- each player: `mid1` (number, visible: public, starts 0): First Middle card (0 = empty). At scoring it becomes the Middle strength.
- each player: `mid2` (number, visible: public, starts 0): Second Middle card (0 = empty).
- each player: `back1` (number, visible: public, starts 0): First Back card (0 = empty). At scoring it becomes the Back strength.
- each player: `back2` (number, visible: public, starts 0): Second Back card (0 = empty).
- each player: `fouled` (bool, visible: public, starts False): Whether this player's rows fouled in the hand just scored.
- each player: `hand_score` (number, visible: public, starts 0): Points scored in the hand just scored.
- each player: `total` (number, visible: public, starts 0): Match total: the sum of hand scores.
- the table: `hand_number` (number, visible: public, starts 1): Current hand, 1 to 4. Above 4 means the match is over.
- the table: `round_in_hand` (number, visible: public, starts 1): Current round within the hand, 1 to 5.
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 32, card_value_min = 1, card_value_max = 8, copies_per_value = 4, hands = 4, rounds_per_hand = 5, total_rounds = 20, cards_per_seat_per_round = 3, cards_kept_per_round = 1, cards_discarded_per_round = 2, cards_used_per_hand = 30, unused_positions = 2, front_slots = 1, middle_slots = 2, back_slots = 2, front_multiplier = 2, pair_bonus = 100, row_win_points = 1, scoop_bonus = 3, foul_win_points = 6, front_royalty_min_value = 7, front_royalty = 1, middle_pair_royalty = 2, back_pair_royalty = 1
- the game ends with ONE ending whose `rank_by` is `you.total`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
