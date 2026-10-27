# 30 coder

- time: 2026-10-27T21:29:58+00:00 (72.1s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 1b2a3eec3e206602, reply sha256 7c829cbcc3a751f5

## Sent

````
# Task: write the XColos game file for "Wizard Duel of Three"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

DECK (32 cards). Four suits, Red, Blue, Green and Yellow, each numbered 1 to 7 (28 cards), plus 2 Wizards and 2 Jesters.

STRUCTURE. The game has 6 hands. Each hand has 5 tricks, and each trick is one game round, so the game lasts exactly 30 rounds. Seats are 1, 2 and 3. The dealer of hand 1 is seat 1, and the dealer moves to the next seat (1, then 2, then 3, then 1) each hand.

START OF A HAND (first trick of each hand only).
(a) The deck is rebuilt from all 32 cards and shuffled. This is the round's single random event.
(b) Each player receives 5 cards, kept privately.
(c) The next card is turned face up and announced. If it is a numbered card, its suit is trump for this hand. If it is a Wizard or a Jester, there is no trump this hand.
(d) The 16 remaining cards are not used this hand and nobody sees them.
(e) Each player's bid and tricks taken are reset to 0.
(f) All three players, at the same moment and without seeing each other's choice, bid how many of the 5 tricks they will take: 0, 1, 2, 3, 4 or 5. The bids need not add up to 5.
(g) All bids are then announced, one message per player.
The player after the dealer leads the first trick.

EACH TRICK.
(1) The led suit is reset to none and the trick is empty.
(2) The leader plays any one card from their hand, face up.
(3) The next player in seat order plays any one card from their hand.
(4) The third player plays any one card from their hand.
There is no obligation to follow suit: any card in hand may always be played.
The led suit is the suit of the first numbered card played in the trick. A Jester played before it does not set the suit. If a Wizard is the first card played, the trick has no led suit, and that Wizard wins.

WHO WINS THE TRICK.
- If any Wizard was played, the first Wizard played wins.
- Otherwise, if any trump was played, the highest trump wins.
- Otherwise, the highest card of the led suit wins.
- If all three cards are Jesters, the first Jester played wins.
Numbered cards not of the led suit and not trump can never win. Every card is unique, so there are no ties.
The winner's tricks taken increases by 1 and is announced, and the winner leads the next trick.

END OF A HAND (after the fifth trick).
Each player's score changes:
- If tricks taken equals the bid exactly, the player gains 20 + 10 x tricks taken.
- Otherwise, the player loses 10 x |bid - tricks taken|.
Each player's trick count and new score are announced in separate messages, then the dealer moves to the next seat.

INFORMATION. You see your own hand, the turned trump card, all revealed bids, every card played so far, and all scores. You never see other players' hands or the unused cards.

No discussion phase.

END. After the 30th trick (the end of hand 6), the game ends.

How the winner is decided: After 6 hands (30 tricks), the player with the highest score wins. If two or three players tie for the highest score, those players share the win and the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Wizard Duel of Three (3 to 3 players, best with 3)

A three-player trick-taking game of 6 hands of 5 tricks. Players bid how many tricks they will take and score for exact bids, using Wizards, Jesters and a turned trump suit.

STATE (every item below must exist in the file):
  - each player: hand (list, starts []); only its owner sees it. The cards the player holds this hand, coded as text (R1..R7, B1..B7, G1..G7, Y1..Y7, W1, W2, J1, J2).
  - each player: bid (number, starts 0); everyone sees it. Tricks bid this hand, revealed after the simultaneous bid.
  - each player: tricks_taken (number, starts 0); everyone sees it. Tricks won so far this hand.
  - each player: score (number, starts 0); everyone sees it. Running score.
  - each player: played_card (text, starts ''); everyone sees it. The card this player played to the current trick.
  - the table: deck (list, starts []); hidden from all players. The 32-card deck, rebuilt and drawn from at the start of each hand. The cards left in it after the deal are the 16 unused cards.
  - the table: trump_card (text, starts ''); everyone sees it. The card turned face up after the deal.
  - the table: trump_suit (text, starts 'none'); everyone sees it. The suit letter of trump_card if it is numbered, otherwise none.
  - the table: led_suit (text, starts 'none'); everyone sees it. The suit of the first numbered card played in the trick, or none.
  - the table: trick_cards (list, starts []); everyone sees it. The cards played to the current trick, in order of play.
  - the table: played_history (list, starts []); everyone sees it. Every card played so far this hand.
  - the table: dealer (number, starts 1); everyone sees it. The dealer seat for the current hand.
  - the table: leader (number, starts 2); everyone sees it. The seat that leads the current trick.
  - the table: hand_number (number, starts 1); everyone sees it. The current hand, from 1 to 6.
  - the table: trick_in_hand (number, starts 1); everyone sees it. The current trick within the hand, from 1 to 5.
  - the table: round_number (number, starts 1); everyone sees it. The current trick overall, from 1 to 30.
  - parameters, each kept as a table attribute: num_hands = 6, tricks_per_hand = 5, total_rounds = 30, deck_size = 32, num_suits = 4, max_rank = 7, numbered_cards = 28, num_wizards = 2, num_jesters = 2, hand_size = 5, unused_cards_per_hand = 16, bid_min = 0, bid_max = 5, exact_bid_bonus = 20, exact_bid_per_trick = 10, miss_penalty_per_trick = 10, first_dealer_seat = 1, trick_win_increment = 1

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seats are 1, 2 and 3.
  2. Every score is 0.
  3. dealer is set to 1, hand_number to 1, trick_in_hand to 1 and round_number to 1.
  4. leader is set to 2, the seat after the dealer.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] table. What happens: When trick_in_hand == 1: deck is set to all 32 cards (R1-R7, B1-B7, G1-G7, Y1-Y7, W1, W2, J1, J2). Every hand is emptied and every played_history entry is cleared.
  2. [update] all players. What happens: When trick_in_hand == 1: each player draws 5 cards at random from deck into their hand, each card removed from deck as it is drawn.
  3. [update] table. What happens: When trick_in_hand == 1: one more card is drawn at random from deck into trump_card. trump_suit is set to its suit letter if it is numbered, or to none if it is W or J. The 16 cards left in deck stay hidden and unused this hand.
  4. [tell] all players. What happens: When trick_in_hand == 1: announce 'Hand {hand_number}: dealer is seat {dealer}; turned card is {trump_card}; trump is {trump_suit}.'
  5. [update] all players. What happens: When trick_in_hand == 1: every bid and every tricks_taken is set to 0.
  6. [sync] all players. What happens: When trick_in_hand == 1: each player is sent their own hand, trump_card and the scores.
  7. [poll] all players answers: a whole number from 0 to 5. What happens: When trick_in_hand == 1: each player's bid is set to their answer. Nobody sees any bid until all are in.
  8. [tell] all players. What happens: When trick_in_hand == 1: one message per player: 'Seat {seat} bids {bid}.'
  9. [update] table. What happens: led_suit is set to none, trick_cards is emptied and every played_card is set to empty.
  10. [ask] seat leader answers: one card from the player's own hand. What happens: The card is removed from the leader's hand and appended to trick_cards and played_history. The leader's played_card is set to it. If the card is numbered, led_suit is set to its suit.
  11. [ask] seat leader % 3 + 1 answers: one card from the player's own hand. What happens: The card is removed from the player's hand and appended to trick_cards and played_history. The player's played_card is set to it. If led_suit == none and trick_cards[0] is not a Wizard and the card is numbered, led_suit is set to its suit.
  12. [ask] seat (leader + 1) % 3 + 1 answers: one card from the player's own hand. What happens: The card is removed from the player's hand and appended to trick_cards and played_history. The player's played_card is set to it. If led_suit == none and trick_cards[0] is not a Wizard and the card is numbered, led_suit is set to its suit.
  13. [update] table. What happens: The trick winner is worked out by arithmetic. Each card in trick_cards gets a power by its play position p (0, 1, 2). A Wizard has power 1000 - p. A card of trump_suit has power 200 + rank. A card of led_suit that is not trump has power 100 + rank. Any other numbered card has power 0. A Jester has power 3 - p only if all three cards are Jesters, otherwise 0. The seat that played the card with the highest power wins. That seat's tricks_taken increases by 1, and leader is set to that seat.
  14. [tell] all players. What happens: Announce 'Seat {leader} wins trick {trick_in_hand} with cards {trick_cards}; tricks taken now {tricks_taken}.'
  15. [update] all players. What happens: When trick_in_hand == 5: for each player, if tricks_taken == bid then score += 20 + 10 * tricks_taken, otherwise score -= 10 * |bid - tricks_taken|.
  16. [tell] all players. What happens: When trick_in_hand == 5: separate messages per player: 'Seat {seat} took {tricks_taken} tricks' and 'Seat {seat} score is now {score}'.
  17. [update] table. What happens: round_number += 1. If trick_in_hand == 5: hand_number += 1, trick_in_hand is set to 1, dealer is set to dealer % 3 + 1, and leader is set to dealer % 3 + 1 using the new dealer. Otherwise trick_in_hand += 1.
  18. [check] table. What happens: End the game if round_number > 30. Otherwise continue with the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game begins, the deck has 32 cards: four suits (Red, Blue, Green, Yellow) numbered 1 to 7, plus 2 Wizards and 2 Jesters.
  R2. When the game begins, every score is 0, the dealer is seat 1 and seat 2 leads the first trick.
  R3. When a hand starts (trick_in_hand == 1), the deck is rebuilt from all 32 cards and each player receives exactly 5 cards in their private hand.
  R4. When a hand starts, one more card becomes trump_card. If it is numbered, its suit is trump_suit; if it is a Wizard or Jester, trump_suit is none.
  R5. When a hand starts, 16 cards remain in the deck unused and unseen.
  R6. When a hand starts, every bid and tricks_taken is reset to 0.
  R7. When a hand starts, all three players bid simultaneously a whole number from 0 to 5, and the bids need not total 5.
  R8. When all bids are in, each player's bid is announced in its own message.
  R9. When a hand starts, the seat after the dealer leads the first trick.
  R10. When a trick is played, the leader plays first, then the next seat in order (leader % 3 + 1), then the remaining seat.
  R11. When a player plays, they may play any card in their hand, with no obligation to follow suit, and the card leaves their hand.
  R12. When the first numbered card of a trick is played and no Wizard was played first, its suit becomes led_suit; a Jester played before it does not set the suit.
  R13. When a Wizard is the first card of a trick, the trick has no led suit and that Wizard wins.
  R14. When any Wizard is played in a trick, the first Wizard played wins the trick.
  R15. When no Wizard is played but a trump is, the highest trump wins the trick.
  R16. When no Wizard and no trump is played, the highest card of led_suit wins the trick.
  R17. When all three cards in a trick are Jesters, the first Jester played wins.
  R18. When a numbered card is neither of led_suit nor trump, it never wins the trick.
  R19. When a player wins a trick, their tricks_taken increases by 1, this is announced, and they lead the next trick.
  R20. When a hand ends with tricks_taken equal to bid, the player gains 20 + 10 x tricks_taken (for example, bid 2 and took 2 gives +40; bid 0 and took 0 gives +20).
  R21. When a hand ends with tricks_taken not equal to bid, the player loses 10 x |bid - tricks_taken| (for example, bid 3 and took 1 gives -20).
  R22. When a hand ends, each player's trick count and new score are announced in separate messages.
  R23. When a hand ends, the dealer moves to the next seat (1, then 2, then 3, then 1).
  R24. When the 30th trick (the end of hand 6) is complete, the game ends.
  R25. When the game ends, the highest score wins and players tied at the top share the win.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Bid at the start of a hand | asked: all three seats, simultaneously | options: any whole number from 0 to 5
  - Lead card | asked: the seat in leader | options: every card currently in that seat's hand
  - Second card | asked: seat leader % 3 + 1 | options: every card currently in that seat's hand, whatever the led suit
  - Third card | asked: the remaining seat | options: every card currently in that seat's hand, whatever the led suit

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round_number > 30
  - each player's standing: you.score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's final score after 6 hands (30 tricks). The highest score wins, and players tied for the highest score share the win (a draw).
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

- each player: `bid` (number, visible: public, starts 0): Tricks bid this hand, revealed after the simultaneous bid.
- each player: `tricks_taken` (number, visible: public, starts 0): Tricks won so far this hand.
- each player: `score` (number, visible: public, starts 0): Running score.
- the table: `trump_card` (text, visible: public, starts ''): The card turned face up after the deal.
- parameters (each must be an attribute holding this value, never a number buried in a step): num_hands = 6, tricks_per_hand = 5, total_rounds = 30, deck_size = 32, num_suits = 4, max_rank = 7, numbered_cards = 28, num_wizards = 2, num_jesters = 2, hand_size = 5, unused_cards_per_hand = 16, bid_min = 0, bid_max = 5, exact_bid_bonus = 20, exact_bid_per_trick = 10, miss_penalty_per_trick = 10, first_dealer_seat = 1, trick_win_increment = 1
- the game ends with ONE ending whose `rank_by` is `you.score`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
    "id": "wizard_duel_of_three",
    "name": "Wizard Duel of Three",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Three players, 6 hands of 5 tricks: bid your tricks exactly, with Wizards, Jesters and a turned trump suit."
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
        "key": "bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tricks_taken",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "played_card",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "bid_said",
        "visible": "ally",
        "type": "text",
        "initial": ""
      }
    ],
    "game": [
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": ["R1", "R2", "R3", "R4", "R5", "R6", "R7", "B1", "B2", "B3", "B4", "B5", "B6", "B7", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "Y1", "Y2", "Y3", "Y4", "Y5", "Y6", "Y7", "W1", "W2", "J1", "J2"]
      },
      {
        "key": "full_deck",
        "visible": "none",
        "type": "list",
        "initial": ["R1", "R2", "R3", "R4", "R5", "R6", "R7", "B1", "B2", "B3", "B4", "B5", "B6", "B7", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "Y1", "Y2", "Y3", "Y4", "Y5", "Y6", "Y7", "W1", "W2", "J1", "J2"]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "powers",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "winner_seat",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "trump_card",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "trump_suit",
        "visible": "public",
        "type": "text",
        "initial": "none"
      },
      {
        "key": "led_suit",
        "visible": "public",
        "type": "text",
        "initial": "none"
      },
      {
        "key": "trick_cards",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "played_history",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "dealer",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "leader",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "hand_number",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "trick_in_hand",
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
        "key": "num_hands",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "tricks_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "total_rounds",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 32
      },
      {
        "key": "num_suits",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "max_rank",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "numbered_cards",
        "visible": "public",
        "type": "number",
        "initial": 28
      },
      {
        "key": "num_wizards",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "num_jesters",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "hand_size",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "unused_cards_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 16
      },
      {
        "key": "bid_min",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bid_max",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "exact_bid_bonus",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "exact_bid_per_trick",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "miss_penalty_per_trick",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "first_dealer_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "trick_win_increment",
        "visible": "public",
        "type": "number",
        "initial": 1
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the starting table",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": 0
          }
        },
        {
          "set": {
            "key": "dealer",
            "value": {
              "calc": "first_dealer_seat"
            }
          }
        },
        {
          "set": {
            "key": "hand_number",
            "value": 1
          }
        },
        {
          "set": {
            "key": "trick_in_hand",
            "value": 1
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
            "key": "leader",
            "value": {
              "calc": "dealer % 3 + 1"
            }
          }
        }
      ]
    },
    {
      "use": "sync",
      "label": "the table",
      "mode": "self",
      "to": "all",
      "fields": [
        "score"
      ],
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "deal",
      "label": "rebuild the deck",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "do": [
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "full_deck"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "[]"
            }
          }
        },
        {
          "set": {
            "key": "played_history",
            "value": {
              "calc": "[]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "deal",
      "label": "deal the hands",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "do": [
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}}
      ]
    },
    {
      "use": "update",
      "phase": "deal",
      "label": "turn the trump card",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "set": {
            "key": "trump_card",
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
            "key": "trump_suit",
            "value": {
              "calc": "trump_card[0] if trump_card[0] in ['R', 'B', 'G', 'Y'] else 'none'"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "deal",
      "label": "the hand begins",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "to": "all",
      "text": "Hand {hand_number}: dealer is seat {dealer}; turned card is {trump_card}; trump is {trump_suit}."
    },
    {
      "use": "update",
      "phase": "deal",
      "label": "reset bids and tricks",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "tricks_taken",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bid_said",
            "value": ""
          }
        }
      ]
    },
    {
      "use": "sync",
      "phase": "deal",
      "label": "your hand",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "mode": "self",
      "to": "all",
      "fields": [
        "hand",
        "score"
      ],
      "text": "Your cards and score for this hand (trump card {trump_card}):"
    },
    {
      "use": "poll",
      "phase": "bid",
      "label": "the bids",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "to": "acting",
      "answer": {
        "type": "number",
        "min": {
          "calc": "bid_min"
        },
        "max": {
          "calc": "bid_max"
        }
      },
      "store": "bid_said",
      "text": "Hand {hand_number}, trump is {trump_suit} (turned card {trump_card}). Bid how many of the {tricks_per_hand} tricks you will take, a whole number from {bid_min} to {bid_max}. Nobody sees any bid until all are in."
    },
    {
      "use": "update",
      "phase": "bid",
      "label": "the bids revealed",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": {
              "calc": "int(you.bid_said)"
            },
            "text": "Seat {player} bids {value}."
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "clear the trick",
      "do": [
        {
          "set": {
            "key": "led_suit",
            "value": "none"
          }
        },
        {
          "set": {
            "key": "trick_cards",
            "value": {
              "calc": "[]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "played_card",
            "value": ""
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "lead card",
      "to": {
        "where": "you.seat == leader"
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
              "value": "$answer"
            }
          },
          {
            "append": {
              "key": "trick_cards",
              "value": "$answer"
            }
          },
          {
            "append": {
              "key": "played_history",
              "value": "$answer"
            }
          },
          {
            "set": {
              "player": "$seat",
              "key": "played_card",
              "value": "$answer"
            }
          },
          {
            "set": {
              "key": "led_suit",
              "value": {
                "calc": "$answer[0]"
              },
              "if": {
                "calc": "$answer[0] in ['R', 'B', 'G', 'Y']"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} leads {value}."
      },
      "text": "Trick {trick_in_hand} of hand {hand_number}. You lead: play any card from your hand. Trump is {trump_suit}."
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "second card",
      "to": {
        "where": "you.seat == leader % 3 + 1"
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
            "set": {
              "key": "led_suit",
              "value": {
                "calc": "$answer[0]"
              },
              "if": {
                "calc": "led_suit == 'none' and trick_cards[0][0] != 'W' and $answer[0] in ['R', 'B', 'G', 'Y']"
              }
            }
          },
          {
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": "$answer"
            }
          },
          {
            "append": {
              "key": "trick_cards",
              "value": "$answer"
            }
          },
          {
            "append": {
              "key": "played_history",
              "value": "$answer"
            }
          },
          {
            "set": {
              "player": "$seat",
              "key": "played_card",
              "value": "$answer"
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} plays {value}."
      },
      "text": "Trick {trick_in_hand}: cards so far {trick_cards}, led suit {led_suit}, trump {trump_suit}. Play any card from your hand; you need not follow suit."
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "third card",
      "to": {
        "where": "you.seat == (leader + 1) % 3 + 1"
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
            "set": {
              "key": "led_suit",
              "value": {
                "calc": "$answer[0]"
              },
              "if": {
                "calc": "led_suit == 'none' and trick_cards[0][0] != 'W' and $answer[0] in ['R', 'B', 'G', 'Y']"
              }
            }
          },
          {
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": "$answer"
            }
          },
          {
            "append": {
              "key": "trick_cards",
              "value": "$answer"
            }
          },
          {
            "append": {
              "key": "played_history",
              "value": "$answer"
            }
          },
          {
            "set": {
              "player": "$seat",
              "key": "played_card",
              "value": "$answer"
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} plays {value}."
      },
      "text": "Trick {trick_in_hand}: cards so far {trick_cards}, led suit {led_suit}, trump {trump_suit}. Play any card from your hand; you need not follow suit."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "the trick is won",
      "do": [
        {
          "set": {
            "key": "powers",
            "value": {
              "calc": "[((1000 - p) if trick_cards[p][0] == 'W' else ((200 + int(trick_cards[p][1])) if trick_cards[p][0] == trump_suit else ((100 + int(trick_cards[p][1])) if trick_cards[p][0] == led_suit else ((3 - p) if (trick_cards[p][0] == 'J' and all(x[0] == 'J' for x in trick_cards)) else 0)))) for p in [0, 1, 2]]"
            }
          }
        },
        {
          "set": {
            "key": "winner_seat",
            "value": {
              "calc": "[leader, leader % 3 + 1, (leader + 1) % 3 + 1][[p for p in [0, 1, 2] if powers[p] == max(powers)][0]]"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "winner_seat"
            },
            "key": "tricks_taken",
            "value": {
              "calc": "trick_win_increment"
            }
          }
        },
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "winner_seat"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "trick",
      "label": "trick result",
      "to": "all",
      "text": "Seat {leader} wins trick {trick_in_hand} with cards {trick_cards}; tricks taken now: seat 1 {players[0].tricks_taken}, seat 2 {players[1].tricks_taken}, seat 3 {players[2].tricks_taken}. Seat {leader} leads next."
    },
    {
      "use": "update",
      "phase": "scoring",
      "label": "score the hand",
      "when": {
        "calc": "trick_in_hand == tricks_per_hand"
      },
      "do": [
        {
          "adjust": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "(exact_bid_bonus + exact_bid_per_trick * you.tricks_taken) if you.tricks_taken == you.bid else (0 - miss_penalty_per_trick * abs(you.bid - you.tricks_taken))"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "scoring",
      "label": "hand results announced",
      "when": {
        "calc": "trick_in_hand == tricks_per_hand"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "tricks_taken",
            "value": {
              "calc": "you.tricks_taken"
            },
            "text": "Seat {player} took {value} tricks."
          }
        },
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "you.score"
            },
            "text": "Seat {player} score is now {value}."
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "scoring",
      "label": "advance the round",
      "do": [
        {
          "adjust": {
            "key": "round_number",
            "value": 1
          }
        },
        {
          "adjust": {
            "key": "hand_number",
            "value": 1,
            "if": {
              "calc": "trick_in_hand == tricks_per_hand"
            }
          }
        },
        {
          "set": {
            "key": "dealer",
            "value": {
              "calc": "dealer % 3 + 1"
            },
            "if": {
              "calc": "trick_in_hand == tricks_per_hand"
            }
          }
        },
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "dealer % 3 + 1"
            },
            "if": {
              "calc": "trick_in_hand == tricks_per_hand"
            }
          }
        },
        {
          "set": {
            "key": "trick_in_hand",
            "value": {
              "calc": "1 if trick_in_hand == tricks_per_hand else trick_in_hand + 1"
            }
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "scoring",
      "label": "after the last trick",
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
      "rank_by": "you.score",
      "text": "Winner: {result}. Final scores: Seat 1 {players[0].score}, Seat 2 {players[1].score}, Seat 3 {players[2].score}."
    }
  },
  "limits": {
    "rounds": 30,
    "rounds_max": 32,
    "actions_max": 3000,
    "deadline_s": 120
  },
  "rules": "DECK ({deck_size} cards). Four suits, Red (R), Blue (B), Green (G) and Yellow (Y), each numbered 1 to {max_rank} ({numbered_cards} cards), plus {num_wizards} Wizards (W1, W2) and {num_jesters} Jesters (J1, J2).\n\nSTRUCTURE. The game has {num_hands} hands. Each hand has {tricks_per_hand} tricks, and each trick is one game round, so the game lasts exactly {total_rounds} rounds. Seats are 1, 2 and 3. The dealer of hand 1 is seat {first_dealer_seat}, and the dealer moves to the next seat (1, then 2, then 3, then 1) each hand.\n\nSTART OF A HAND (first t
... (cut)

Why it was refused: it plays, but part of it does nothing: game attribute `full_deck` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "wizard_duel_of_three",
    "name": "Wizard Duel of Three",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Three players, 6 hands of 5 tricks: bid your tricks exactly, with Wizards, Jesters and a turned trump suit."
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
        "key": "bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tricks_taken",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "played_card",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "bid_said",
        "visible": "ally",
        "type": "text",
        "initial": ""
      }
    ],
    "game": [
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": ["R1", "R2", "R3", "R4", "R5", "R6", "R7", "B1", "B2", "B3", "B4", "B5", "B6", "B7", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "Y1", "Y2", "Y3", "Y4", "Y5", "Y6", "Y7", "W1", "W2", "J1", "J2"]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "powers",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "winner_seat",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "trump_card",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "trump_suit",
        "visible": "public",
        "type": "text",
        "initial": "none"
      },
      {
        "key": "led_suit",
        "visible": "public",
        "type": "text",
        "initial": "none"
      },
      {
        "key": "trick_cards",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "played_history",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "dealer",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "leader",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "hand_number",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "trick_in_hand",
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
        "key": "num_hands",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "tricks_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "total_rounds",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 32
      },
      {
        "key": "num_suits",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "max_rank",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "numbered_cards",
        "visible": "public",
        "type": "number",
        "initial": 28
      },
      {
        "key": "num_wizards",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "num_jesters",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "hand_size",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "unused_cards_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 16
      },
      {
        "key": "bid_min",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bid_max",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "exact_bid_bonus",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "exact_bid_per_trick",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "miss_penalty_per_trick",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "first_dealer_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "trick_win_increment",
        "visible": "public",
        "type": "number",
        "initial": 1
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the starting table",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": 0
          }
        },
        {
          "set": {
            "key": "dealer",
            "value": {
              "calc": "first_dealer_seat"
            }
          }
        },
        {
          "set": {
            "key": "hand_number",
            "value": 1
          }
        },
        {
          "set": {
            "key": "trick_in_hand",
            "value": 1
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
            "key": "leader",
            "value": {
              "calc": "dealer % 3 + 1"
            }
          }
        }
      ]
    },
    {
      "use": "sync",
      "label": "the table",
      "mode": "self",
      "to": "all",
      "fields": [
        "score"
      ],
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "deal",
      "label": "rebuild the deck",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "do": [
        {
          "set": {
            "key": "deck",
            "value": ["R1", "R2", "R3", "R4", "R5", "R6", "R7", "B1", "B2", "B3", "B4", "B5", "B6", "B7", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "Y1", "Y2", "Y3", "Y4", "Y5", "Y6", "Y7", "W1", "W2", "J1", "J2"]
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "[]"
            }
          }
        },
        {
          "set": {
            "key": "played_history",
            "value": {
              "calc": "[]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "deal",
      "label": "deal the hands",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "do": [
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}}
      ]
    },
    {
      "use": "update",
      "phase": "deal",
      "label": "turn the trump card",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "set": {
            "key": "trump_card",
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
            "key": "trump_suit",
            "value": {
              "calc": "trump_card[0] if trump_card[0] in ['R', 'B', 'G', 'Y'] else 'none'"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "deal",
      "label": "the hand begins",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "to": "all",
      "text": "Hand {hand_number}: dealer is seat {dealer}; turned card is {trump_card}; trump is {trump_suit}."
    },
    {
      "use": "update",
      "phase": "deal",
      "label": "reset bids and tricks",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "tricks_taken",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bid_said",
            "value": ""
          }
        }
      ]
    },
    {
      "use": "sync",
      "phase": "deal",
      "label": "your hand",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "mode": "self",
      "to": "all",
      "fields": [
        "hand",
        "score"
      ],
      "text": "Your cards and score for this hand (trump card {trump_card}):"
    },
    {
      "use": "poll",
      "phase": "bid",
      "label": "the bids",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "to": "acting",
      "answer": {
        "type": "number",
        "min": {
          "calc": "bid_min"
        },
        "max": {
          "calc": "bid_max"
        }
      },
      "store": "bid_said",
      "text": "Hand {hand_number}, trump is {trump_suit} (turned card {trump_card}). Bid how many of the {tricks_per_hand} tricks you will take, a whole number from {bid_min} to {bid_max}. Nobody sees any bid until all are in."
    },
    {
      "use": "update",
      "phase": "bid",
      "label": "the bids revealed",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": {
              "calc": "int(you.bid_said)"
            },
            "text": "Seat {player} bids {value}."
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "clear the trick",
      "do": [
        {
          "set": {
            "key": "led_suit",
            "value": "none"
          }
        },
        {
          "set": {
            "key": "trick_cards",
            "value": {
              "calc": "[]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "played_card",
            "value": ""
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "lead card",
      "to": {
        "where": "you.seat == leader"
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
              "value": "$answer"
            }
          },
          {
            "append": {
              "key": "trick_cards",
              "value": "$answer"
            }
          },
          {
            "append": {
              "key": "played_history",
              "value": "$answer"
            }
          },
          {
            "set": {
              "player": "$seat",
              "key": "played_card",
              "value": "$answer"
            }
          },
          {
            "set": {
              "key": "led_suit",
              "value": {
                "calc": "$answer[0]"
              },
              "if": {
                "calc": "$answer[0] in ['R', 'B', 'G', 'Y']"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} leads {value}."
      },
      "text": "Trick {trick_in_hand} of hand {hand_number}. You lead: play any card from your hand. Trump is {trump_suit}."
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "second card",
      "to": {
        "where": "you.seat == leader % 3 + 1"
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
            "set": {
              "key": "led_suit",
              "value": {
                "calc": "$answer[0]"
              },
              "if": {
                "calc": "led_suit == 'none' and trick_cards[0][0] != 'W' and $answer[0] in ['R', 'B', 'G', 'Y']"
              }
            }
          },
          {
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": "$answer"
            }
          },
          {
            "append": {
              "key": "trick_cards",
              "value": "$answer"
            }
          },
          {
            "append": {
              "key": "played_history",
              "value": "$answer"
            }
          },
          {
            "set": {
              "player": "$seat",
              "key": "played_card",
              "value": "$answer"
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} plays {value}."
      },
      "text": "Trick {trick_in_hand}: cards so far {trick_cards}, led suit {led_suit}, trump {trump_suit}. Play any card from your hand; you need not follow suit."
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "third card",
      "to": {
        "where": "you.seat == (leader + 1) % 3 + 1"
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
            "set": {
              "key": "led_suit",
              "value": {
                "calc": "$answer[0]"
              },
              "if": {
                "calc": "led_suit == 'none' and trick_cards[0][0] != 'W' and $answer[0] in ['R', 'B', 'G', 'Y']"
              }
            }
          },
          {
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": "$answer"
            }
          },
          {
            "append": {
              "key": "trick_cards",
              "value": "$answer"
            }
          },
          {
            "append": {
              "key": "played_history",
              "value": "$answer"
            }
          },
          {
            "set": {
              "player": "$seat",
              "key": "played_card",
              "value": "$answer"
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} plays {value}."
      },
      "text": "Trick {trick_in_hand}: cards so far {trick_cards}, led suit {led_suit}, trump {trump_suit}. Play any card from your hand; you need not follow suit."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "the trick is won",
      "do": [
        {
          "set": {
            "key": "powers",
            "value": {
              "calc": "[((1000 - p) if trick_cards[p][0] == 'W' else ((200 + int(trick_cards[p][1])) if trick_cards[p][0] == trump_suit else ((100 + int(trick_cards[p][1])) if trick_cards[p][0] == led_suit else ((3 - p) if (trick_cards[p][0] == 'J' and all(x[0] == 'J' for x in trick_cards)) else 0)))) for p in [0, 1, 2]]"
            }
          }
        },
        {
          "set": {
            "key": "winner_seat",
            "value": {
              "calc": "[leader, leader % 3 + 1, (leader + 1) % 3 + 1][[p for p in [0, 1, 2] if powers[p] == max(powers)][0]]"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "winner_seat"
            },
            "key": "tricks_taken",
            "value": {
              "calc": "trick_win_increment"
            }
          }
        },
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "winner_seat"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "trick",
      "label": "trick result",
      "to": "all",
      "text": "Seat {leader} wins trick {trick_in_hand} with cards {trick_cards}; tricks taken now: seat 1 {players[0].tricks_taken}, seat 2 {players[1].tricks_taken}, seat 3 {players[2].tricks_taken}. Seat {leader} leads next."
    },
    {
      "use": "update",
      "phase": "scoring",
      "label": "score the hand",
      "when": {
        "calc": "trick_in_hand == tricks_per_hand"
      },
      "do": [
        {
          "adjust": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "(exact_bid_bonus + exact_bid_per_trick * you.tricks_taken) if you.tricks_taken == you.bid else (0 - miss_penalty_per_trick * abs(you.bid - you.tricks_taken))"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "scoring",
      "label": "hand results announced",
      "when": {
        "calc": "trick_in_hand == tricks_per_hand"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "tricks_taken",
            "value": {
              "calc": "you.tricks_taken"
            },
            "text": "Seat {player} took {value} tricks."
          }
        },
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "you.score"
            },
            "text": "Seat {player} score is now {value}."
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "scoring",
      "label": "advance the round",
      "do": [
        {
          "adjust": {
            "key": "round_number",
            "value": 1
          }
        },
        {
          "adjust": {
            "key": "hand_number",
            "value": 1,
            "if": {
              "calc": "trick_in_hand == tricks_per_hand"
            }
          }
        },
        {
          "set": {
            "key": "dealer",
            "value": {
              "calc": "dealer % 3 + 1"
            },
            "if": {
              "calc": "trick_in_hand == tricks_per_hand"
            }
          }
        },
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "dealer % 3 + 1"
            },
            "if": {
              "calc": "trick_in_hand == tricks_per_hand"
            }
          }
        },
        {
          "set": {
            "key": "trick_in_hand",
            "value": {
              "calc": "1 if trick_in_hand == tricks_per_hand else trick_in_hand + 1"
            }
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "scoring",
      "label": "after the last trick",
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
      "rank_by": "you.score",
      "text": "Winner: {result}. Final scores: Seat 1 {players[0].score}, Seat 2 {players[1].score}, Seat 3 {players[2].score}."
    }
  },
  "limits": {
    "rounds": 30,
    "rounds_max": 32,
    "actions_max": 3000,
    "deadline_s": 120
  },
  "rules": "DECK ({deck_size} cards). Four suits, Red (R), Blue (B), Green (G) and Yellow (Y), each numbered 1 to {max_rank} ({numbered_cards} cards), plus {num_wizards} Wizards (W1, W2) and {num_jesters} Jesters (J1, J2). Cards are written as suit letter and number, e.g. R5.\n\nSTRUCTURE. The game has {num_hands} hands. Each hand has {tricks_per_hand} tricks, and each trick is one game round, so the game lasts exactly {total_rounds} rounds. Seats are 1, 2 and 3. The dealer of hand 1 is seat {first_dealer_seat}, and the dealer moves to the next seat (1, then 2, then 3, then 1) each hand.\n\nSTART OF A HAND (first trick of each hand only). (a) The deck is rebuilt from all {deck_size} cards and shuffled. (b) Each player receives {hand_size} cards, kept privately. (c) The next card is turned face up and announced. If it is a numbered card, its suit is trump for this hand. If it is a Wizard or a Jester, there is no trump this hand. (d) The {unused_cards_per_hand} remaining cards are not used this hand and nobody sees them. (e) Each player's bid and tricks taken are reset to 0. (f) All three players, at the same moment and without seeing each other's choice, bid how many of the {tricks_per_hand} tricks they will take: {bid_min} to {bid_max}. The bids need not add up to {tricks_per_hand}. (g) All bids are then announced, one message per player. The player after the dealer leads the first trick.\n\nEACH TRICK. (1) The led suit is reset to none and the trick is empty. (2) The leader plays any one card from their hand, face up. (3) The next player in seat order plays any one card from their hand. (4) The third player plays any one card from their hand. There is no obligation to follow suit: any card in hand may always be played, and the played card leaves your hand. The led suit is the suit of the first numbered card played in the trick. A Jester played before it does not set the suit. If a Wizard is the first card played, the trick has no led suit, and that Wizard wins.\n\nWHO WINS THE TRICK. If any Wizard was played, the first Wizard played wins. Otherwise, if any trump was played, the highest trump wins. Otherwise, the highest card of the led suit wins. If all three cards are Jesters, the first Jester played wins. Numbered cards not of the led suit and not trump can never win. Every card is unique, so there are no ties. The winner's tricks taken increases by {trick_win_increment} and is announced, and the winner leads the next trick.\n\nEND OF A HAND (after the fifth trick). Each player's score changes: if tricks taken equals the bid exactly, the player gains {exact_bid_bonus} + {exact_bid_per_trick} x tricks taken (bid 2 and took 2 gives +40; bid 0 and took 0 gives +20). Otherwise, the player loses {miss_penalty_per_trick} x |bid - tricks taken| (bid 3 and took 1 gives -20). Each player's trick count and new score are announced in separate messages, then the dealer moves to the next seat.\n\nINFORMATION. You see your own hand, the turned trump card, all revealed bids, every card played so far, and all scores. You never see other players' hands or the unused cards. There is no discussion phase.\n\nEND. After the {total_rounds}th trick (the end of hand {num_hands}), the game ends. The player with the highest score wins. If two or three players tie for the highest score, those players share the win and the game is a draw."
}
```
````
