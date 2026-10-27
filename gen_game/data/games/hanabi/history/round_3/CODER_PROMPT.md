# Task: write the XColos game file for "Hanabi Duo"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 2; set `meta.players` to {"min": 2, "max": 2, "suggested": 2} (the suggested size is the one the game plays best at).

CARDS. The deck has 12 cards in 2 colours, Red and Blue. Each colour has three 1s, two 2s and one 3. (Engine codes: Red 1/2/3 = 11/12/13, Blue 1/2/3 = 21/22/23, empty slot = 0. Colour is code divided by 10 rounded down; rank is code mod 10.)

SETUP. Shuffle the deck once. Deal 2 cards to each player into slots A and B, taking them from the front of the deck: player 1 gets A then B, then player 2 gets A then B. The 8 remaining cards stay in order face down. Set the Red pile and the Blue pile to 0. Set hint tokens to 3 (the maximum is 3) and fuses to 3. The discard pile starts empty. Every card note starts blank. Both players' scores start at 0.

WHAT EACH PLAYER SEES. On your turn you are shown:
- your partner's two cards;
- the notes on all four cards (yours and your partner's);
- both pile values, the hint tokens and the fuses;
- the full discard pile and the number of cards left in the deck;
- your partner's last action and its result.
You are never shown your own cards. There is no other communication: no messages, only the actions below.

ROUND. Each round player 1 takes a turn, then player 2 takes a turn. There are at most 12 rounds.

TURN. The active player chooses exactly one of these 8 options:
- Play A or Play B: reveal your card in that slot. If its rank is exactly 1 more than its colour's pile, that pile goes up by 1. Otherwise the play fails: the card goes to the discard pile and fuses go down by 1. If the slot is empty, nothing happens.
- Discard A or Discard B: put your card in that slot on the discard pile and gain 1 hint token, up to the maximum of 3. If the slot is empty, nothing happens.
- Hint colour of partner's A, Hint colour of partner's B, Hint rank of partner's A, or Hint rank of partner's B: if you have at least 1 hint token and the named partner slot holds a card, spend 1 token. Then name that card's colour (or rank) to your partner. Each of the partner's non-empty cards gets a note added: 'is Red' (or 'is 2', and so on) if it matches, or 'not Red' (or 'not 2') if it does not. If you have no token or the named slot is empty, nothing happens and the turn is wasted.

DRAWING. After a card leaves a slot (played, successfully or not, or discarded), the player takes the front card of the deck into that slot, and that slot's note is cleared. If the deck is empty, the slot stays empty and its note stays blank.

ANNOUNCEMENT. After every turn, the action and its result are shown to both players: which option was chosen, any card revealed, whether a play succeeded, and the hint named.

SCORE. After every turn, both players' scores are set to the Red pile plus the Blue pile. The two scores are always equal.

END. The game ends immediately when either of these happens after a turn:
- fuses reach 0;
- both piles reach 3.
Otherwise it ends after round 12. In every case the team keeps its current score.

How the winner is decided: Cooperative. When the game ends, if the team score (Red pile + Blue pile, shown identically as each player's score) is 4 or more, both seats win. Otherwise no seat wins. This holds whether the game ended on fuses, on a full score of 6, or after round 12.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Hanabi Duo (2 to 2 players, best with 2)

A cooperative two-player card game: each player sees only the partner's two cards, and the pair use hints, plays and discards to build Red and Blue piles from 1 to 3, scoring 4 or more to win together.

STATE (every item below must exist in the file):
  - each player: card_a (number, starts 0); everyone but its owner sees it. Code of the card in slot A (11/12/13 Red 1-3, 21/22/23 Blue 1-3, 0 empty). The partner sees it and the owner never does.
  - each player: card_b (number, starts 0); everyone but its owner sees it. Code of the card in slot B, same coding as card_a. The partner sees it and the owner never does.
  - each player: note_a (list, starts []); everyone sees it. Hint notes on the card in slot A, e.g. 'is Red', 'not 2'. Cleared when a new card is drawn into the slot.
  - each player: note_b (list, starts []); everyone sees it. Hint notes on the card in slot B. Cleared when a new card is drawn into the slot.
  - each player: score (number, starts 0); everyone sees it. Team score, equal to red_pile + blue_pile and identical for both seats.
  - the table: deck (list, starts [11, 11, 11, 12, 12, 13, 21, 21, 21, 22, 22, 23]); hidden from all players. Face-down draw deck, shuffled once at setup. Cards are taken from the front, index 0.
  - the table: deck_left (number, starts 12); everyone sees it. Number of cards left in the deck. It is 8 after the deal.
  - the table: red_pile (number, starts 0); everyone sees it. Highest Red rank played successfully (0 to 3).
  - the table: blue_pile (number, starts 0); everyone sees it. Highest Blue rank played successfully (0 to 3).
  - the table: hints (number, starts 3); everyone sees it. Hint tokens available (0 to 3).
  - the table: fuses (number, starts 3); everyone sees it. Fuses remaining. The game ends when this reaches 0.
  - the table: discard (list, starts []); everyone sees it. Codes of discarded cards and of cards from failed plays.
  - the table: round_number (number, starts 0); everyone sees it. Number of completed rounds.
  - the table: last_action (text, starts ''); everyone sees it. The most recent action and its result: option chosen, card revealed, success or failure, hint named.
  - the table: action (text, starts ''); hidden from all players. Scratch: the option chosen this turn by the active seat.
  - parameters, each kept as a table attribute: deck_size = 12, colours = 2, red_colour_code = 1, blue_colour_code = 2, copies_of_rank_1_per_colour = 3, copies_of_rank_2_per_colour = 2, copies_of_rank_3_per_colour = 1, hand_size = 2, cards_left_after_deal = 8, starting_hint_tokens = 3, max_hint_tokens = 3, starting_fuses = 3, hint_cost = 1, discard_gain = 1, failed_play_fuse_loss = 1, pile_start = 0, pile_max = 3, max_rounds = 12, max_score = 6, win_threshold = 4, empty_slot_code = 0

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Shuffle the deck list of 12 codes [11,11,11,12,12,13,21,21,21,22,22,23] into a random (seeded) order.
  2. Deal from the front of the deck: seat 1 card_a, then seat 1 card_b, then seat 2 card_a, then seat 2 card_b. Each dealt code is removed from deck.
  3. Set deck_left to 8.
  4. Set red_pile = 0, blue_pile = 0, hints = 3, fuses = 3, discard = [], round_number = 0, and last_action = ''.
  5. Set every note_a and note_b to [] and both scores to 0.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [sync] seat 1. What happens: Seat 1 is shown: seat 2's card_a and card_b; note_a and note_b of both seats; red_pile, blue_pile, hints, fuses; discard and deck_left; last_action. Seat 1's own card_a and card_b are not shown.
  2. [ask] seat 1 answers: one of: Play A, Play B, Discard A, Discard B, Hint colour of partner's A, Hint colour of partner's B, Hint rank of partner's A, Hint rank of partner's B. What happens: game.action = the chosen option
  3. [update] seat 1. What happens: PLAY X (X = A or B), with c = seat 1 card_X: if c == 0, nothing changes. Otherwise colour = floor(c/10) and rank = c mod 10. If (colour == 1 and rank == red_pile + 1), then red_pile += 1. Else if (colour == 2 and rank == blue_pile + 1), then blue_pile += 1. Otherwise append c to discard and fuses -= 1. In every non-empty case, card_X is vacated (marked for drawing). DISCARD X: if c != 0, append c to discard, hints = min(3, hints + 1), and vacate card_X; if c == 0, nothing changes. HINT (colour or rank) of partner's X, with p = seat 2 card_X: if hints >= 1 and p != 0, then hints -= 1 and v = floor(p/10) (colour) or p mod 10 (rank). For each of seat 2's slots Y with card_Y != 0, append 'is V' to note_Y if the matching value equals v, else append 'not V'. V is the colour name (Red for 1, Blue for 2) or the rank number. Otherwise nothing changes and the turn is wasted. Set last_action to the option, any revealed code, success or failure, and any hint named.
  4. [update] seat 1. What happens: If seat 1's slot X was vacated this turn: if deck_left > 0, then card_X = deck[0], remove deck[0], deck_left -= 1, note_X = []. If deck_left == 0, then card_X = 0 and note_X = [].
  5. [update] all players. What happens: Each seat's score = red_pile + blue_pile.
  6. [tell] all players. What happens: Announce last_action: the option seat 1 chose, any card code revealed, whether a play succeeded, and the hint named. Also announce red_pile, blue_pile, hints and fuses.
  7. [check] all players. What happens: End the game if fuses == 0 or (red_pile == 3 and blue_pile == 3); otherwise continue.
  8. [sync] seat 2. What happens: Seat 2 is shown: seat 1's card_a and card_b; note_a and note_b of both seats; red_pile, blue_pile, hints, fuses; discard and deck_left; last_action. Seat 2's own cards are not shown.
  9. [ask] seat 2 answers: one of: Play A, Play B, Discard A, Discard B, Hint colour of partner's A, Hint colour of partner's B, Hint rank of partner's A, Hint rank of partner's B. What happens: game.action = the chosen option
  10. [update] seat 2. What happens: Same resolution as seat 1's resolution step, with seat 2 as the active seat and seat 1 as the partner: plays and discards act on seat 2's card_X, and hints act on seat 1's cards and notes. Set last_action accordingly.
  11. [update] seat 2. What happens: If seat 2's slot X was vacated this turn: if deck_left > 0, then card_X = deck[0], remove deck[0], deck_left -= 1, note_X = []. If deck_left == 0, then card_X = 0 and note_X = [].
  12. [update] all players. What happens: Each seat's score = red_pile + blue_pile. round_number += 1.
  13. [tell] all players. What happens: Announce last_action for seat 2's turn (option, revealed card, success or failure, hint named), plus red_pile, blue_pile, hints and fuses.
  14. [check] all players. What happens: End the game if fuses == 0 or (red_pile == 3 and blue_pile == 3) or round_number >= 12; otherwise continue.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game is set up, the deck contains exactly 12 cards: three each of 11 and 21, two each of 12 and 22, and one each of 13 and 23.
  R2. When the deal is done, each seat holds 2 cards (card_a and card_b), deck_left is 8, red_pile and blue_pile are 0, hints is 3, fuses is 3, discard is empty, all notes are empty and both scores are 0.
  R3. When a seat is shown its state, it sees its partner's card_a and card_b but never its own card_a or card_b.
  R4. When a seat plays a card whose rank equals its colour's pile + 1 (e.g. Red 1 on red_pile 0), then that pile increases by 1 and fuses are unchanged.
  R5. When a seat plays a card whose rank is not its colour's pile + 1 (e.g. Blue 2 on blue_pile 0), then the card's code is appended to discard and fuses decrease by 1.
  R6. When a seat plays or discards an empty slot (code 0), then nothing changes: no pile, fuse, hint or discard change, and no draw.
  R7. When a seat discards a non-empty slot, then the card's code is appended to discard and hints become min(3, hints + 1); with hints at 3, hints stay 3.
  R8. When a seat gives a hint with hints >= 1 and the named partner slot is non-empty, then hints decrease by 1.
  R9. When a colour hint names Red (or Blue), then each non-empty partner card gets the note 'is Red' if its colour is Red, and 'not Red' otherwise (likewise for Blue).
  R10. When a rank hint names rank r, then each non-empty partner card gets the note 'is r' if its rank is r, and 'not r' otherwise.
  R11. When a seat gives a hint with hints == 0 or names an empty partner slot, then nothing changes and the turn is wasted.
  R12. When a card leaves a slot by play (successful or failed) or by discard and deck_left > 0, then the front card of the deck goes into that slot, deck_left decreases by 1 and that slot's note becomes empty.
  R13. When a card leaves a slot and deck_left == 0, then the slot becomes 0 and its note stays empty.
  R14. When any turn ends, then both seats' scores equal red_pile + blue_pile.
  R15. When any turn ends, then the chosen option, any revealed card, whether a play succeeded, and any hint named are announced to both seats.
  R16. When fuses reach 0 after any turn, then the game ends immediately.
  R17. When red_pile == 3 and blue_pile == 3 after any turn, then the game ends immediately with score 6.
  R18. When round 12 is completed (seat 2's 12th turn), then the game ends.
  R19. When the game ends with red_pile + blue_pile >= 4, then both seats win.
  R20. When the game ends with red_pile + blue_pile <= 3, then no seat wins.
  R21. When a round is played, then seat 1 takes its turn before seat 2.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Your turn: choose one action | asked: the active seat (seat 1, then seat 2, each round) | options: In every situation, all 8 options: Play A, Play B, Discard A, Discard B, Hint colour of partner's A, Hint colour of partner's B, Hint rank of partner's A, Hint rank of partner's B. The rules define the outcome of each option even when a slot is empty or no hint token remains (nothing happens), so all 8 are always legal.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: fuses == 0 OR (red_pile == 3 AND blue_pile == 3) OR round_number >= 12
  - the result is one of: both seats win, no seat wins
  - how the result is decided: If red_pile + blue_pile (each seat's score) >= 4, the result is 'both seats win'; otherwise it is 'no seat wins'. This applies whichever ending condition triggered.
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
rounds it says a match may run at most) and `limits.rounds_max` to at least that. The `end` rules fire the real endings from the state; add one more
ending that fires when the cap is reached and decides the winner as the script says, so a match that hits the cap still ends with a result.

## The interface the file must use

Independent tests were written against these names and you cannot see them, so use them exactly.

- each player: `score` (number, visible: public, starts 0): Team score, equal to red_pile + blue_pile and identical for both seats.
- the table: `red_pile` (number, visible: public, starts 0): Highest Red rank played successfully (0 to 3).
- the table: `blue_pile` (number, visible: public, starts 0): Highest Blue rank played successfully (0 to 3).
- the table: `hints` (number, visible: public, starts 3): Hint tokens available (0 to 3).
- the table: `fuses` (number, visible: public, starts 3): Fuses remaining. The game ends when this reaches 0.
- the table: `discard` (list, visible: public, starts []): Codes of discarded cards and of cards from failed plays.
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 12, colours = 2, red_colour_code = 1, blue_colour_code = 2, copies_of_rank_1_per_colour = 3, copies_of_rank_2_per_colour = 2, copies_of_rank_3_per_colour = 1, hand_size = 2, cards_left_after_deal = 8, starting_hint_tokens = 3, max_hint_tokens = 3, starting_fuses = 3, hint_cost = 1, discard_gain = 1, failed_play_fuse_loss = 1, pile_start = 0, pile_max = 3, max_rounds = 12, max_score = 6, win_threshold = 4, empty_slot_code = 0
- the game ends with exactly one of these results, named exactly: `both seats win`, `no seat wins`
- anything else the game needs to keep track of is yours to design: name it as you like.

## How the platform works

The complete file format reference and two example games are in your system prompt. Follow them exactly: every key an
action accepts is listed there, and the loader refuses any other. The outcome must be decided by arithmetic: every
ending's `when` is a calc condition with a `result`; no `winner`, no prose ending, no `llm` in an ending. Use calc for any rule that is
arithmetic. For a spec step marked `judged`, make that step's `when` `{"prose": "<the judged sentence, verbatim>"}`: a referee answers it
true or false at play time. You may add `llm` wording to a tell, sync or update (never an ask or poll, never an outcome branch), but always keep its `text`, which is used when no
model answers. Choices made at the same moment are a `poll`. The end screen announces only the result: every ending's `text` says who won and the final scores or deciding figures with
placeholders such as `{players[0].score}`, in a line or two, with no retelling of how the game went. End with a `result` and a calc condition as the `rps` example does (not the `auction`'s `winner`).

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
3. A `check` with `when` and `against`, and the endings in `end`, comparing `players[0].score` and `players[1].score`.
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
        "seat_1_wins",
        "seat_2_wins",
        "draw"
      ]
    }
  ],
  "end": {
    "seat_1_wins": {
      "when": {
        "calc": "players[0].score > players[1].score"
      },
      "result": "seat 1",
      "text": "Seat 1 wins."
    },
    "seat_2_wins": {
      "when": {
        "calc": "players[1].score > players[0].score"
      },
      "result": "seat 2",
      "text": "Seat 2 wins."
    },
    "draw": {
      "when": {
        "calc": "players[0].score == players[1].score"
      },
      "result": "draw",
      "text": "A draw."
    }
  }
}
```

Your file is checked by the platform's loader, a rule that the outcome is arithmetic, random play, a check that every
attribute is actually updated, and tests written independently from the rules. If it is refused you will be told why and
shown your file again; fix what is wrong and keep the rest.
