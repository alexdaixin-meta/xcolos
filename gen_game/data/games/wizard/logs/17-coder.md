# 17 coder

- time: 2026-10-27T21:05:40+00:00 (168.4s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 fd65b0e680132a60, reply sha256 8bf152264c3ce126

## Sent

````
# Task: write the XColos game file for "Three-Card Wizard"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 4; set `meta.players` to {"min": 3, "max": 4, "suggested": 3} (the suggested size is the one the game plays best at).

DECK: 25 cards: three suits (Red, Blue, Green), each numbered 1 to 7 (21 cards), plus 2 Wizards and 2 Jesters. Wizards and Jesters have no suit.

SETUP: Seat players in a fixed order. Player 1 is dealer in round 1. The dealer moves one seat along each round. All scores start at 0. The game lasts 12 rounds.

EACH ROUND:
1. Deal: shuffle all 25 cards, deal 3 cards face down to each player (seen only by their owner), then turn the next card face up as the trump card.
2. Trump: if the trump card is a numbered card, its suit is trump for this round. If it is a Wizard or a Jester, there is no trump this round.
3. Bidding: starting with the player after the dealer and ending with the dealer, each player in turn publicly bids a whole number from 0 to 3: the number of tricks they expect to take. Each bidder sees earlier bids. The dealer may not choose a bid that makes the total of all bids exactly 3.
4. Tricks: 3 tricks are played. The player after the dealer leads the first trick; the winner of each trick leads the next. In each trick, starting with the leader, each player in turn plays one card face up from their hand, seeing the cards already played to that trick.
5. Led suit: the led suit is the suit of the first numbered card played to the trick.
   - If a Jester is led, the next numbered card played sets the led suit.
   - If a Wizard is led, there is no led suit for that trick and anything may be played.
6. Following: a player holding a numbered card of the led suit must play either a card of that suit or a Wizard or Jester. Wizards and Jesters may always be played. A player with no card of the led suit may play any card. Only legal cards are offered.
7. Trick winner:
   - the first Wizard played wins;
   - if there is no Wizard, the highest trump card wins;
   - if there is no trump, the highest card of the led suit wins;
   - if every card is a Jester, the first Jester played wins.
   The winner adds 1 to their tricks taken this round.
8. Scoring: each player whose tricks taken equals their bid scores 20 + 10 x tricks taken. Each other player loses 10 x |bid - tricks taken|.
9. Reset bids and tricks taken, and pass the deal to the next seat.

END: after round 12 the game ends.

How the winner is decided: After 12 rounds the player with the highest total score wins. If two or more players tie for the highest total, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Three-Card Wizard (3 to 4 players, best with 3)

Over 12 rounds, players are dealt 3 cards, publicly bid how many of the 3 tricks they will take, then play the tricks with trump, Wizards and Jesters; an exact bid scores 20 + 10 per trick and a missed bid loses 10 per trick off.

STATE (every item below must exist in the file):
  - each player: score (number, starts 0); everyone sees it. Running total score.
  - each player: hand (list, starts []); only its owner sees it. Cards held this round, seen only by the owner.
  - each player: bid (number, starts -1); everyone sees it. Tricks bid this round. -1 means the player has not bid yet.
  - each player: tricks (number, starts 0); everyone sees it. Tricks taken this round.
  - each player: played_card (text, starts ''); everyone sees it. Card played to the current trick, face up.
  - each player: play_pos (number, starts 0); everyone sees it. Order in which this player played to the current trick: 1 for the leader, then 2, 3, 4.
  - each player: power (number, starts 0); everyone sees it. Strength of played_card in the current trick, used to find the trick winner.
  - the table: deck (list, starts 'the 25 cards: Red 1..Red 7, Blue 1..Blue 7, Green 1..Green 7, Wizard A, Wizard B, Jester A, Jester B'); hidden from all players. Undealt cards, hidden from everyone.
  - the table: trump_card (text, starts ''); everyone sees it. Card turned face up after the deal.
  - the table: trump_suit (text, starts 'none'); everyone sees it. Trump suit this round (Red, Blue or Green), or none.
  - the table: dealer (number, starts 1); everyone sees it. Seat of this round's dealer.
  - the table: leader (number, starts 2); everyone sees it. Seat that leads the current trick.
  - the table: led_suit (text, starts ''); everyone sees it. Led suit of the current trick. Empty until it is set; 'none' if a Wizard was led.
  - the table: bid_total (number, starts 0); everyone sees it. Sum of the bids made so far this round.
  - the table: trick_no (number, starts 0); everyone sees it. Tricks completed this round.
  - the table: round_no (number, starts 0); everyone sees it. Rounds completed.
  - parameters, each kept as a table attribute: deck_size = 25, suit_count = 3, rank_min = 1, rank_max = 7, numbered_cards = 21, wizard_count = 2, jester_count = 2, hand_size = 3, tricks_per_round = 3, rounds = 12, bid_min = 0, bid_max = 3, forbidden_bid_total = 3, exact_bid_bonus = 20, points_per_trick_on_exact_bid = 10, penalty_per_trick_off = 10, first_dealer_seat = 1, wizard_power_base = 100, trump_power_base = 50, led_suit_power_base = 20, jester_power_base = 5, offsuit_power = 0

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seat the players in a fixed order, seats 1 to N.
  2. Every score starts at 0.
  3. Seat 1 is the dealer for round 1 (dealer = 1).
  4. round_no = 0.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: Shuffle: deck = all 25 cards. Each hand = [], bid = -1, tricks = 0, played_card = ''. bid_total = 0, trick_no = 0, led_suit = ''. leader = (dealer mod N) + 1.
  2. [update] all players. What happens: Deal 3 cards to each player: 3 times per player, pick a random card from deck, append it to that player's hand and remove it from deck. Then pick one more random card from deck, set trump_card to it and remove it from deck. trump_suit = the suit of trump_card if it is a numbered card; otherwise (Wizard or Jester) trump_suit = 'none'. Announce trump_card and trump_suit.
  3. [sync] all players. What happens: Each player sees their own hand, the trump_card, the trump_suit and the dealer.
  4. [ask] each player in turn, starting with seat (dealer mod N)+1 and ending with the dealer answers: a whole number from 0 to 3; for the dealer, the value 3 - bid_total is not offered. What happens: The player's bid = answer; bid_total += answer. Each bid is announced publicly.
  5. [update] all players. What happens: Start a trick: played_card = '', play_pos = 0 and power = 0 for every player; led_suit = ''.
  6. [ask] each player in turn, starting with seat leader and going round the table answers: one card from the player's own hand, chosen from the legal cards only: if led_suit is a suit and the hand holds a numbered card of that suit, the offer is the cards of that suit plus any Wizards and Jesters in hand; otherwise the whole hand. What happens: Remove the card from hand; played_card = card; play_pos = 1 + the number of players who have already played to this trick. If led_suit = '' and the card is a Wizard and play_pos = 1, then led_suit = 'none'. If led_suit = '' and the card is numbered, then led_suit = the card's suit. The card is shown to everyone.
  7. [update] all players. What happens: For each player, power = 100 - play_pos if played_card is a Wizard; 50 + rank if it is numbered and its suit = trump_suit; 20 + rank if it is numbered and its suit = led_suit (and it is not trump); 5 - play_pos if it is a Jester; 0 otherwise. The player with the highest power wins the trick: their tricks += 1, leader = that seat, trick_no += 1. Announce the trick winner.
  8. [repeat] all players. What happens: Repeat the three trick steps above (start a trick, play cards, find the winner) until trick_no = 3.
  9. [update] all players. What happens: For each player: if tricks = bid, then score += 20 + 10 * tricks; otherwise score -= 10 * |bid - tricks|. Announce each bid, tricks and score.
  10. [update] all players. What happens: round_no += 1; dealer = (dealer mod N) + 1.
  11. [check] all players. What happens: If round_no = 12, end the game; otherwise start the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When a round starts, then the deck holds all 25 cards: Red, Blue and Green 1 to 7, 2 Wizards and 2 Jesters.
  R2. When cards are dealt, then each player receives exactly 3 cards into their hand, seen only by the owner, and those cards leave the deck.
  R3. When the deal is done, then one more card from the deck becomes trump_card, face up.
  R4. When trump_card is a numbered card, then trump_suit is its suit; when it is a Wizard or a Jester, then trump_suit is none.
  R5. When bidding happens, then players bid in turn from the seat after the dealer through the dealer, each a whole number from 0 to 3, and each bid is public before the next player bids.
  R6. When the dealer bids, then the dealer may not choose the bid that makes the total of all bids exactly 3.
  R7. When the first trick of a round begins, then the seat after the dealer leads it.
  R8. When a trick is won, then its winner leads the next trick.
  R9. When the first numbered card is played to a trick, and no Wizard was led, then its suit becomes the led suit.
  R10. When a Jester is led, then the next numbered card played sets the led suit.
  R11. When a Wizard is led, then the trick has no led suit and any card may be played to it.
  R12. When a player holds a numbered card of the led suit, then they are offered only cards of that suit plus any Wizards and Jesters they hold.
  R13. When a player holds no numbered card of the led suit, or there is no led suit yet, then they are offered every card in their hand.
  R14. When a trick contains a Wizard, then the first Wizard played wins it.
  R15. When a trick has no Wizard and contains a trump card, then the highest trump card wins it.
  R16. When a trick has no Wizard and no trump card, then the highest card of the led suit wins it.
  R17. When every card in a trick is a Jester, then the first Jester played wins it.
  R18. When a player wins a trick, then their tricks increases by 1.
  R19. When 3 tricks have been played, then the round is scored.
  R20. When a player's tricks equals their bid, then they score 20 + 10 x tricks (bid 0 and took 0 gives +20; bid 2 and took 2 gives +40).
  R21. When a player's tricks differs from their bid, then they lose 10 x |bid - tricks| (bid 3 and took 1 gives -20).
  R22. When a round ends, then bids and tricks are reset and the deal passes one seat along (dealer = dealer mod N + 1).
  R23. When 12 rounds have been completed, then the game ends and the highest total score wins, with players tied at the top sharing the win.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Bid | asked: each non-dealer seat, in turn from the seat after the dealer | options: 0, 1, 2, 3
  - Bid | asked: the dealer (bids last) | options: 0, 1, 2, 3 except the value 3 - bid_total, when that value lies between 0 and 3; if bid_total > 3, all of 0 to 3
  - Play a card | asked: the trick leader | options: every card in their hand
  - Play a card | asked: a later player in the trick, when led_suit is Red, Blue or Green and they hold a numbered card of that suit | options: their cards of the led suit, plus any Wizards and Jesters in their hand
  - Play a card | asked: a later player in the trick, when led_suit is empty (only Jesters played so far), or led_suit is none (a Wizard was led), or they hold no card of the led suit | options: every card in their hand

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round_no >= 12
  - each player's standing: you.score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their total score after 12 rounds. The highest total wins. If players tie at the top, they share the result, which stands for the source's draw.
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

- each player: `score` (number, visible: public, starts 0): Running total score.
- each player: `bid` (number, visible: public, starts -1): Tricks bid this round. -1 means the player has not bid yet.
- each player: `tricks` (number, visible: public, starts 0): Tricks taken this round.
- each player: `played_card` (text, visible: public, starts ''): Card played to the current trick, face up.
- the table: `trump_card` (text, visible: public, starts ''): Card turned face up after the deal.
- the table: `trump_suit` (text, visible: public, starts 'none'): Trump suit this round (Red, Blue or Green), or none.
- the table: `dealer` (number, visible: public, starts 1): Seat of this round's dealer.
- the table: `round_no` (number, visible: public, starts 0): Rounds completed.
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 25, suit_count = 3, rank_min = 1, rank_max = 7, numbered_cards = 21, wizard_count = 2, jester_count = 2, hand_size = 3, tricks_per_round = 3, rounds = 12, bid_min = 0, bid_max = 3, forbidden_bid_total = 3, exact_bid_bonus = 20, points_per_trick_on_exact_bid = 10, penalty_per_trick_off = 10, first_dealer_seat = 1, wizard_power_base = 100, trump_power_base = 50, led_suit_power_base = 20, jester_power_base = 5, offsuit_power = 0
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

## Guidance from the last attempt

The previous attempt had problems:

Rework the `lead_a_card` step so that what is offered and what is accepted come from the same source.

1. Build the leader's options only from that seat's own private hand list (the current leader's hand, not a shared deck list and not another seat's hand). Use exactly the same card strings that the hand stores, so formats such as 'Red 6' match.
2. Do not apply any follow-suit or led-suit check to the lead. There is no led suit yet, so every card in the leader's hand is legal. Remove any `when` or `if` refusal on this step.
3. Apply the follow-suit filter only in the follow step, for seats after the leader:
   - If a Wizard was led, there is no led suit and every card is legal.
   - If a Jester was led, the next numbered card played sets the led suit.
   - Otherwise, if the player holds a card of the led suit, offer only that suit plus Wizards and Jesters.
   - Otherwise, offer the whole hand.
4. When a card is played, remove it from that seat's hand, write it to `played_card`, and set the led suit only from the first numbered card played.
5. Keep the earlier fixes:
   - Guard every deck draw so the draw index stays below `len(deck)`. Rebuild and reshuffle the 25-card deck each round before dealing 3 cards to each player plus the trump card.
   - Hide internal bookkeeping such as `led_suit` and the per-trick scratch values, so `your_hand` shows only usable information.

````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "three_card_wizard",
    "name": "Three-Card Wizard",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 3
    },
    "blurb": "Twelve rounds of three cards each: bid your tricks exactly, with trump, Wizards and Jesters in play."
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
      },
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
        "initial": -1
      },
      {
        "key": "tricks",
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
        "key": "play_pos",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "power",
        "visible": "ally",
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
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": [
          "Red 1",
          "Red 2",
          "Red 3",
          "Red 4",
          "Red 5",
          "Red 6",
          "Red 7",
          "Blue 1",
          "Blue 2",
          "Blue 3",
          "Blue 4",
          "Blue 5",
          "Blue 6",
          "Blue 7",
          "Green 1",
          "Green 2",
          "Green 3",
          "Green 4",
          "Green 5",
          "Green 6",
          "Green 7",
          "Wizard A",
          "Wizard B",
          "Jester A",
          "Jester B"
        ]
      },
      {
        "key": "full_deck",
        "visible": "none",
        "type": "list",
        "initial": [
          "Red 1",
          "Red 2",
          "Red 3",
          "Red 4",
          "Red 5",
          "Red 6",
          "Red 7",
          "Blue 1",
          "Blue 2",
          "Blue 3",
          "Blue 4",
          "Blue 5",
          "Blue 6",
          "Blue 7",
          "Green 1",
          "Green 2",
          "Green 3",
          "Green 4",
          "Green 5",
          "Green 6",
          "Green 7",
          "Wizard A",
          "Wizard B",
          "Jester A",
          "Jester B"
        ]
      },
      {
        "key": "bid_options",
        "visible": "none",
        "type": "list",
        "initial": [
          "0",
          "1",
          "2",
          "3"
        ]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "last_card",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "plays",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "trick_winner",
        "visible": "public",
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
        "key": "led_suit",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "bid_total",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "trick_no",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "round_no",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 25
      },
      {
        "key": "suit_count",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "rank_min",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "rank_max",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "numbered_cards",
        "visible": "public",
        "type": "number",
        "initial": 21
      },
      {
        "key": "wizard_count",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "jester_count",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "hand_size",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "tricks_per_round",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 12
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
        "initial": 3
      },
      {
        "key": "forbidden_bid_total",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "exact_bid_bonus",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "points_per_trick_on_exact_bid",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "penalty_per_trick_off",
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
        "key": "wizard_power_base",
        "visible": "public",
        "type": "number",
        "initial": 100
      },
      {
        "key": "trump_power_base",
        "visible": "public",
        "type": "number",
        "initial": 50
      },
      {
        "key": "led_suit_power_base",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "jester_power_base",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "offsuit_power",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "seat the players",
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
            "key": "round_no",
            "value": 0
          }
        }
      ],
      "text": "Players are seated in order. Seat {dealer} deals the first round. All scores start at 0."
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
      "label": "shuffle",
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
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": -1
          }
        },
        {
          "set": {
            "players": "all",
            "key": "tricks",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "played_card",
            "value": ""
          }
        },
        {
          "set": {
            "key": "bid_total",
            "value": 0
          }
        },
        {
          "set": {
            "key": "trick_no",
            "value": 0
          }
        },
        {
          "set": {
            "key": "led_suit",
            "value": ""
          }
        },
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "dealer % len(players) + 1"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "[o for o in bid_options if you.seat != dealer or int(o) != forbidden_bid_total - bid_total]"
            }
          }
        }
      ],
      "text": "A new round begins. Seat {dealer} deals; all {deck_size} cards are shuffled."
    },
    {
      "use": "update",
      "phase": "deal",
      "label": "deal",
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
            }
          }
        },
        {
          "append": {
            "player": 1,
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
            "key": "pick",
            "value": {
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
            }
          }
        },
        {
          "append": {
            "player": 1,
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
            "key": "pick",
            "value": {
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
            }
          }
        },
        {
          "append": {
            "player": 1,
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
            "key": "pick",
            "value": {
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
            }
          }
        },
        {
          "append": {
            "player": 2,
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
            "key": "pick",
            "value": {
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
            }
          }
        },
        {
          "append": {
            "player": 2,
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
            "key": "pick",
            "value": {
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
            }
          }
        },
        {
          "append": {
            "player": 2,
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
            "key": "pick",
            "value": {
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
            }
          }
        },
        {
          "append": {
            "player": 3,
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
            "key": "pick",
            "value": {
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
            }
          }
        },
        {
          "append": {
            "player": 3,
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
            "key": "pick",
            "value": {
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
            }
          }
        },
        {
          "append": {
            "player": 3,
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
            "key": "pick",
            "value": {
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
            },
            "if": {
              "calc": "len(players) >= 4"
            }
          }
        },
        {
          "append": {
            "player": 4,
            "key": "hand",
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
            "key": "deck",
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
            },
            "if": {
              "calc": "len(players) >= 4"
            }
          }
        },
        {
          "append": {
            "player": 4,
            "key": "hand",
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
            "key": "deck",
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
            },
            "if": {
              "calc": "len(players) >= 4"
            }
          }
        },
        {
          "append": {
            "player": 4,
            "key": "hand",
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
            "key": "deck",
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
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
              "calc": "'Red' if trump_card[0] == 'R' else ('Blue' if trump_card[0] == 'B' else ('Green' if trump_card[0] == 'G' else 'none'))"
            }
          }
        }
      ],
      "text": "Each player is dealt {hand_size} cards face down. The trump card turned up is {trump_card}; trump suit this round: {trump_suit}."
    },
    {
      "use": "sync",
      "phase": "deal",
      "label": "your hand",
      "mode": "self",
      "to": "all",
      "text": "Your hand and the table:"
    },
    {
      "use": "ask",
      "phase": "bidding",
      "label": "first bid",
      "to": {
        "where": "you.seat == dealer % len(players) + 1"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "each": {
        "do": [
          {
            "set": {
              "player": "$seat",
              "key": "bid",
              "value": {
                "calc": "int($answer)"
              }
            }
          },
          {
            "adjust": {
              "key": "bid_total",
              "value": {
                "calc": "int($answer)"
              }
            }
          },
          {
            "set": {
              "players": "all",
              "key": "offer",
              "value": {
                "calc": "[o for o in bid_options if you.seat != dealer or int(o) != forbidden_bid_total - bid_total]"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} bids {value}."
      },
      "text": "Bid how many of the {tricks_per_round} tricks you will take this round ({bid_min} to {bid_max}). Trump card: {trump_card}, trump suit: {trump_suit}."
    },
    {
      "use": "ask",
      "phase": "bidding",
      "label": "second bid",
      "to": {
        "where": "you.seat == (dealer + 1) % len(players) + 1"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "each": {
        "do": [
          {
            "set": {
              "player": "$seat",
              "key": "bid",
              "value": {
                "calc": "int($answer)"
              }
            }
          },
          {
            "adjust": {
              "key": "bid_total",
              "value": {
                "calc": "int($answer)"
              }
            }
          },
          {
            "set": {
              "players": "all",
              "key": "offer",
              "value": {
                "calc": "[o for o in bid_options if you.seat != dealer or int(o) != forbidden_bid_total - bid_total]"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} bids {value}."
      },
      "text": "Bid how many of the {tricks_per_round} tricks you will take this round. Bids so far total {bid_total}. If you are the dealer, you may not bring the total to exactly {forbidden_bid_total}."
    },
    {
      "use": "ask",
      "phase": "bidding",
      "label": "third bid",
      "to": {
        "where": "you.seat == (dealer + 2) % len(players) + 1"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "each": {
        "do": [
          {
            "set": {
              "player": "$seat",
              "key": "bid",
              "value": {
                "calc": "int($answer)"
              }
            }
          },
          {
            "adjust": {
              "key": "bid_total",
              "value": {
                "calc": "int($answer)"
              }
            }
          },
          {
            "set": {
              "players": "all",
              "key": "offer",
              "value": {
                "calc": "[o for o in bid_options if you.seat != dealer or int(o) != forbidden_bid_total - bid_total]"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} bids {value}."
      },
      "text": "Bid how many of the {tricks_per_round} tricks you will take this round. Bids so far total {bid_total}. If you are the dealer, you may not bring the total to exactly {forbidden_bid_total}."
    },
    {
      "use": "ask",
      "phase": "bidding",
      "label": "fourth bid",
      "when": {
        "calc": "len(players) >= 4"
      },
      "to": {
        "where": "you.seat == (dealer + 3) % len(players) + 1"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "each": {
        "do": [
          {
            "set": {
              "player": "$seat",
              "key": "bid",
              "value": {
                "calc": "int($answer)"
              }
            }
          },
          {
            "adjust": {
              "key": "bid_total",
              "value": {
                "calc": "int($answer)"
              }
            }
          },
          {
            "set": {
              "players": "all",
              "key": "offer",
              "value": {
                "calc": "[o for o in bid_options if you.seat != dealer or int(o) != forbidden_bid_total - bid_total]"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} bids {value}."
      },
      "text": "You are the dealer and bid last. Bids so far total {bid_total}. You may not bring the total to exactly {forbidden_bid_total}."
    },
    {
      "use": "repeat",
      "phase": "tricks",
      "label": "the tricks",
      "until": {
        "calc": "trick_no >= tricks_per_round"
      },
      "max": 10,
      "steps": [
        {
          "use": "update",
          "label": "start a trick",
          "do": [
            {
              "set": {
                "players": "all",
                "key": "played_card",
                "value": ""
              }
            },
            {
              "set": {
                "players": "all",
                "key": "play_pos",
                "value": 0
              }
            },
            {
              "set": {
                "players": "all",
                "key": "power",
                "value": 0
              }
            },
            {
              "set": {
                "key": "led_suit",
                "value": ""
              }
            },
            {
              "set": {
                "key": "plays",
                "value": 0
              }
            },
            {
              "set": {
                "players": "all",
                "key": "offer",
                "value": {
                  "calc": "you.hand"
                }
              }
            }
          ],
          "text": "A new trick begins. Seat {leader} leads."
        },
        {
          "use": "ask",
          "label": "lead a card",
          "to": {
            "where": "you.seat == leader"
          },
          "answer": {
            "type": "choice",
            "options": {
              "attribute": "offer"
            }
          },
          "each": {
            "do": [
              {
                "set": {
                  "key": "last_card",
                  "value": "$answer"
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
                "set": {
                  "player": "$seat",
                  "key": "played_card",
                  "value": "$answer"
                }
              },
              {
                "adjust": {
                  "key": "plays",
                  "value": 1
                }
              },
              {
                "set": {
                  "player": "$seat",
                  "key": "play_pos",
                  "value": {
                    "calc": "plays"
                  }
                }
              },
              {
                "set": {
                  "key": "led_suit",
                  "value": "none",
                  "if": {
                    "calc": "led_suit == '' and last_card[0] == 'W' and plays == 1"
                  }
                }
              },
              {
                "set": {
                  "key": "led_suit",
                  "value": {
                    "calc": "'Red' if last_card[0] == 'R' else ('Blue' if last_card[0] == 'B' else 'Green')"
                  },
                  "if": {
                    "calc": "led_suit == '' and last_card[0] in ['R', 'B', 'G']"
                  }
                }
              },
              {
                "set": {
                  "players": "all",
                  "key": "offer",
                  "value": {
                    "calc": "[c for c in you.hand if not (c[0] in ['R', 'B', 'G']) or c[0] == (led_suit + ' ')[0]] if any(c[0] == (led_suit + ' ')[0] for c in you.hand) else you.hand"
                  }
                }
              }
            ]
          },
          "broadcast": {
            "to": "all",
            "text": "Seat {seat} leads {value}."
          },
          "text": "You lead this trick: play any card from your hand. Trump suit: {trump_suit}."
        },
        {
          "use": "ask",
          "label": "second card",
          "to": {
            "where": "you.seat == leader % len(players) + 1"
          },
          "answer": {
            "type": "choice",
            "options": {
              "attribute": "offer"
            }
          },
          "each": {
            "do": [
              {
                "set": {
                  "key": "last_card",
                  "value": "$answer"
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
                "set": {
                  "player": "$seat",
                  "key": "played_card",
                  "value": "$answer"
                }
              },
              {
                "adjust": {
                  "key": "plays",
                  "value": 1
                }
              },
              {
                "set": {
                  "player": "$seat",
                  "key": "play_pos",
                  "value": {
                    "calc": "plays"
                  }
                }
              },
              {
                "set": {
                  "key": "led_suit",
                  "value": {
                    "calc": "'Red' if last_card[0] == 'R' else ('Blue' if last_card[0] == 'B' else 'Green')"
                  },
                  "if": {
                    "calc": "led_suit == '' and last_card[0] in ['R', 'B', 'G']"
                  }
                }
              },
              {
                "set": {
                  "players": "all",
                  "key": "offer",
                  "value": {
                    "calc": "[c for c in you.hand if not (c[0] in ['R', 'B', 'G']) or c[0] == (led_suit + ' ')[0]] if any(c[0] == (led_suit + ' ')[0] for c in you.hand) else you.hand"
                  }
                }
              }
            ]
          },
          "broadcast": {
            "to": "all",
            "text": "Seat {seat} plays {value}."
          },
          "text": "Play a card to the trick. The cards already played are face up. Only the cards you may legally play are offered. Trump suit: {trump_suit}."
        },
        {
          "use": "ask",
          "label": "third card",
          "to": {
            "where": "you.seat == (leader + 1) % len(players) + 1"
          },
          "answer": {
            "type": "choice",
            "options": {
              "attribute": "offer"
            }
          },
          "each": {
            "do": [
              {
                "set": {
                  "key": "last_card",
                  "value": "$answer"
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
                "set": {
                  "player": "$seat",
                  "key": "played_card",
                  "value": "$answer"
                }
              },
              {
                "adjust": {
                  "key": "plays",
                  "value": 1
                }
              },
              {
                "set": {
                  "player": "$seat",
                  "key": "play_pos",
                  "value": {
                    "calc": "plays"
                  }
                }
              },
              {
                "set": {
                  "key": "led_suit",
                  "value": {
                    "calc": "'Red' if last_card[0] == 'R' else ('Blue' if last_card[0] == 'B' else 'Green')"
                  },
                  "if": {
                    "calc": "led_suit == '' and last_card[0] in ['R', 'B', 'G']"
                  }
                }
              },
              {
                "set": {
                  "players": "all",
                  "key": "offer",
                  "value": {
                    "calc": "[c for c in you.hand if not (c[0] in ['R', 'B', 'G']) or c[0] == (led_suit + ' ')[0]] if any(c[0] == (led_suit + ' ')[0] for c in you.hand) else you.hand"
                  }
                }
              }
            ]
          },
          "broadcast": {
            "to": "all",
            "text": "Seat {seat} plays {value}."
          },
          "text": "Play a card to the trick. The cards already played are face up. Only the cards you may legally play are offered. Trump suit: {trump_suit}."
        },
        {
          "use": "ask",
          "label": "fourth card",
          "when": {
            "calc": "len(players) >= 4"
          },
          "to": {
            "where": "you.seat == (leader + 2) % len(players) + 1"
          },
          "answer": {
            "type": "choice",
            "options": {
              "attribute": "offer"
            }
          },
          "each": {
            "do": [
              {
                "set": {
                  "key": "last_card",
                  "value": "$answer"
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
                "set": {
                  "player": "$seat",
                  "key": "played_card",
                  "value": "$answer"
                }
              },
              {
                "adjust": {
                  "key": "plays",
                  "value": 1
                }
              },
              {
                "set": {
                  "player": "$seat",
                  "key": "play_pos",
                  "value": {
                    "calc": "plays"
                  }
                }
              },
              {
                "set": {
                  "key": "led_suit",
                  "value": {
                    "calc": "'Red' if last_card[0] == 'R' else ('Blue' if last_card[0] == 'B' else 'Green')"
                  },
                  "if": {
                    "calc": "led_suit == '' and last_card[0] in ['R', 'B', 'G']"
                  }
                }
              }
            ]
          },
          "broadcast": {
            "to": "all",
            "text": "Seat {seat} plays {value}."
          },
          "text": "Play the last card to the trick. The cards already played are face up. Only the cards you may legally play are offered. Trump suit: {trump_suit}."
        },
        {
          "use": "update",
          "label": "the trick is won",
          "do": [
            {
              "set": {
                "players": "all",
                "key": "power",
                "value": {
                  "calc": "(wizard_power_base - you.play_pos) if (you.played_card + ' ')[0] == 'W' else ((trump_power_base + int(you.played_card[-1])) if ((you.played_card + ' ')[0] in ['R', 'B', 'G'] and (you.played_card + ' ')[0] == (trump_suit + ' ')[0]) else ((led_suit_power_base + int(you.played_card[-1])) if ((you.played_card + ' ')[0] in ['R', 'B', 'G'] and (you.played_card + ' ')[0] == (led_suit + ' ')[0]) else ((jester_power_base - you.play_pos) if (you.played_card + ' ')[0] == 'J' else offsuit_power)))"
                }
              }
            },
            {
              "set": {
                "key": "trick_winner",
                "value": {
                  "calc": "min([p.seat for p in players if p.power == max([q.power for q in players])])"
                }
              }
            },
            {
              "adjust": {
                "player": {
                  "calc": "trick_winner"
                },
                "key": "tricks",
                "value": 1
              }
            },
            {
              "set": {
                "key": "leader",
                "value": {
                  "calc": "trick_winner"
                }
              }
            },
            {
              "adjust": {
                "key": "trick_no",
                "value": 1
              }
            }
          ],
          "text": "Seat {trick_winner} wins the trick and leads next. Tricks played this round: {trick_no} of {tricks_per_round}."
        }
      ]
    },
    {
      "use": "update",
      "phase": "scoring",
      "label": "score the round",
      "do": [
        {
          "adjust": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "(exact_bid_bonus + points_per_trick_on_exact_bid * you.tricks) if you.tricks == you.bid else (0 - penalty_per_trick_off * abs(you.bid - you.tricks))"
            }
          }
        }
      ],
      "text": "The round is scored. [seat, bid, tricks, score]: {[[p.seat, p.bid, p.tricks, p.score] for p in players]}."
    },
    {
      "use": "update",
      "phase": "scoring",
      "label": "pass the deal",
      "do": [
        {
          "adjust": {
            "key": "round_no",
            "value": 1
          }
        },
        {
          "set": {
            "key": "dealer",
            "value": {
              "calc": "dealer % len(players) + 1"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": -1
          }
        },
        {
          "set": {
            "players": "all",
            "key": "tricks",
            "value": 0
          }
        },
        {
          "set": {
            "key": "bid_total",
            "value": 0
          }
        }
      ],
      "text": "Round {round_no} of {rounds} is complete. The deal passes to seat {dealer}."
    },
    {
      "use": "check",
      "phase": "scoring",
      "label": "after the last round",
      "when": {
        "calc": "round_no >= rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round_no >= rounds"
      },
      "rank_by": "you.score",
      "text": "Winner: {result}. Final scores [seat, score]: {[[p.seat, p.score] for p in players]}."
    }
  },
  "limits": {
    "rounds": 12,
    "rounds_max": 12,
    "actions_max": 3000,
    "deadline_s": 120
  },
  "rules": "DECK: {deck_size} cards: three suits (Red, Blue, Green), each numbered {rank_min} to {rank_max} ({numbered_cards} cards), plus {wizard_count} Wizards and {jester_count} Jesters. Wizards and Jesters have no suit.\n\nSETUP: Players sit in a fixed order. Seat {first_dealer_seat} is dealer in round 1. The dealer moves one seat along each round. All scores start at 0. The game lasts {rounds} rounds.\n\nEACH ROUND:\n1. Deal: all {deck_size} cards are shuffled, {hand_size} cards are dealt face down to each player (seen only by their owner), then the next card is turned face up as the trump card.\n2. Trump: if the trump card is a numbered card, its suit is trump for this round. If it is a Wizard or a Jester, there is no trump this round.\n3. Bidding: starting with the player after the dealer and ending with the dealer, each player in turn publicly bids a whole number from {bid_min} to {bid_max}: the number of tricks they expect to take. Each bidder sees earlier bids. The dealer may not choose a bid that makes the total of all bids exactly {forbidden_bid_total}; that bid is not offered to the dealer. If the total cannot reach {forbidden_bid_total}, the dealer may bid anything from {bid_min} to {bid_max}.\n4. Tricks: {tricks_per_round} tricks are played. The player after the dealer leads the first trick; the winner of each trick leads the next. In each trick, starting with the leader, each player in turn plays one card face up from their hand, seeing the cards already played to that trick.\n5. Led suit: the led suit is the suit of the first numbered card played to the trick. If a Jester is led, the next numbered card played sets the led suit. If a Wizard is led, there is no led suit for that trick and anything may be played.\n6. Following: the leader may play any card. A player holding a numbered card of the led suit must play either a card of that suit or a Wizard or Jester. Wizards and Jesters may always be played. A player with no card of the led suit, or when there is no led suit yet, may play any card. Only legal cards are offered.\n7. Trick winner: the first Wizard played wins; if there is no Wizard, the highest trump card wins; if there is no trump, the highest card of the led suit wins; if every card is a Jester, the first Jester played wins. Cards of other suits never win. The winner adds 1 to their tricks taken this round.\n8. Scoring: each player whose tricks taken equals their bid scores {exact_bid_bonus} + {points_per_trick_on_exact_bid} x tricks taken (bid 0 and took 0: +20; bid 2 and took 2: +40). Each other player loses {penalty_per_trick_off} x |bid - tricks taken| (bid 3 and took 1: -20).\n9. Bids and tricks taken are reset and the deal passes to the next seat.\n\nEND: after round {rounds} the game ends. The player with the highest total score wins; players tied for the highest total share the win."
}
```
````
