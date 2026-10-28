# Task: write the XColos game file for "Trischettn Duel"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 2; set `meta.players` to {"min": 2, "max": 2, "suggested": 2} (the suggested size is the one the game plays best at).

DECK. The deck has 32 cards in four suits: Hearts, Bells, Leaves, Acorns. Each suit holds these ranks, from strongest to weakest: Ten, Nine, Ace, King, Ober, Unter, Eight, Seven (strength 8 down to 1). There are no trumps.

CARD VALUES (pips).
- Ace: 3 pips.
- Ten, Nine, King, Ober and Unter: 1 pip each.
- Eight and Seven: 0 pips.
- Winning the 16th (last) trick of a deal: 3 extra pips.
Each deal therefore contains 35 pips in total.

MATCH. The match is exactly 2 deals of 16 tricks each, 32 rounds in all. Each round is one trick.

START OF A DEAL (in round 1 and round 17 only).
1. Shuffle all 32 cards.
2. Deal 8 cards face down to each player as a private hand.
3. The remaining 16 cards form the talon, face down. Its top card is turned face up as the 'talon up' card, visible to both players.
4. Both players' deal pips are set to 0.
5. The leader of the first trick is Player A in deal 1 and Player B in deal 2.

EACH TRICK.
1. The leader plays any one card from their hand face up.
2. The follower then plays one card. If they hold any card of the led suit, they must play a card of that suit. Only legal cards are offered. If they hold none, they may play any card.
3. Winning the trick: if both cards are of the led suit, the one of higher strength wins. Otherwise the leader wins.
4. The trick winner adds the pips of both cards to their deal pips. If this was the 16th trick of the deal, the winner adds 3 more.
5. If the talon is not empty:
   - the winner takes the face-up 'talon up' card into their hand, so both players know it;
   - the loser takes the next talon card face down, so only the loser sees it;
   - if any talon cards remain, the new top card is turned face up as 'talon up'; otherwise 'talon up' becomes 'none'.
   The 16-card talon empties after exactly 8 tricks. The last 8 tricks are played from hand with no drawing.
6. The trick winner leads the next trick.

END OF A DEAL (after trick 16). Each player adds their deal pips to their match total.

PUBLIC INFORMATION. Both players see:
- the deal number and trick number;
- who leads;
- both cards of the current trick (shown as 'none' before they are played);
- the 'talon up' card, or 'none';
- the number of cards left in the talon;
- both players' deal pips and match totals.
Each player privately sees only their own hand.

END OF MATCH. After round 32, the player with the higher match total wins. Equal totals are a draw.

How the winner is decided: After 2 deals (32 tricks), each player's match total is the sum of their pips from both deals, out of 70 pips available. The higher total wins. If both totals are 35, the match is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Trischettn Duel (2 to 2 players, best with 2)

A two-player, no-trump trick-taking duel over 2 deals of 16 tricks with a talon draw, where pips from won cards and the last trick decide the winner.

STATE (every item below must exist in the file):
  - each player: hand (list, starts []); only its owner sees it. The player's private hand of cards, each written like 'Ace of Bells'.
  - each player: deal_pips (number, starts 0); everyone sees it. Pips won so far in the current deal, including the last-trick bonus.
  - each player: match_total (number, starts 0); everyone sees it. Sum of deal pips from completed deals. This is the score.
  - the table: deck (list, starts 'all 32 cards: Ten, Nine, Ace, King, Ober, Unter, Eight, Seven of each of Hearts, Bells, Leaves, Acorns'); hidden from all players. The full deck. It is rebuilt and shuffled at the start of each deal.
  - the table: talon (list, starts []); hidden from all players. The face-down talon cards below the talon-up card, in order.
  - the table: talon_up (text, starts 'none'); everyone sees it. The face-up top card of the talon, or 'none'.
  - the table: talon_count (number, starts 0); everyone sees it. Number of cards left in the talon, counting the talon-up card.
  - the table: deal_number (number, starts 1); everyone sees it. The current deal, 1 or 2. It is set to 3 when the match is over.
  - the table: trick_number (number, starts 1); everyone sees it. The current trick within the deal, from 1 to 16.
  - the table: leader_seat (number, starts 1); everyone sees it. The seat that leads the current trick.
  - the table: led_card (text, starts 'none'); everyone sees it. The card led to the current trick, or 'none'.
  - the table: follow_card (text, starts 'none'); everyone sees it. The card played by the follower to the current trick, or 'none'.
  - the table: trick_winner_seat (number, starts 0); everyone sees it. The seat that won the last trick.
  - parameters, each kept as a table attribute: deck_size = 32, suits = 4, ranks_per_suit = 8, hand_size = 8, talon_size = 16, tricks_per_deal = 16, deals = 2, total_rounds = 32, drawing_tricks_per_deal = 8, strength_ten = 8, strength_nine = 7, strength_ace = 6, strength_king = 5, strength_ober = 4, strength_unter = 3, strength_eight = 2, strength_seven = 1, pips_ace = 3, pips_ten = 1, pips_nine = 1, pips_king = 1, pips_ober = 1, pips_unter = 1, pips_eight = 0, pips_seven = 0, last_trick_bonus = 3, pips_per_deal = 35, pips_per_match = 70, deal_1_first_leader_seat = 1, deal_2_first_leader_seat = 2

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seat 1 is Player A and seat 2 is Player B.
  2. Both players start with match_total 0 and deal_pips 0.
  3. deal_number is set to 1 and trick_number to 1. The deal itself happens in the first round step, because it also runs at the start of deal 2.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] table. What happens: When trick_number = 1: rebuild deck with all 32 cards, empty every hand, then draw 8 cards at random from deck into each player's hand. Move the remaining 16 cards into talon in random order, then remove the first talon card and set it as talon_up. Set talon_count = 16, set each deal_pips = 0, and set leader_seat = 1 if deal_number = 1, else 2. Announce the deal number, talon_up and the leader.
  2. [sync] all players. What happens: Each player sees their own hand plus all public attributes: deal_number, trick_number, leader_seat, led_card, follow_card, talon_up, talon_count, every deal_pips and every match_total.
  3. [ask] the seat equal to leader_seat answers: one card from their hand. What happens: Remove the chosen card from the leader's hand and set led_card to it. Announce led_card.
  4. [ask] the seat not equal to leader_seat answers: one card from their hand of the suit of led_card; if they hold no card of that suit, any card in their hand. What happens: Remove the chosen card from the follower's hand and set follow_card to it. Announce follow_card.
  5. [update] table. What happens: If follow_card has the same suit as led_card and its strength is higher (Ten 8, Nine 7, Ace 6, King 5, Ober 4, Unter 3, Eight 2, Seven 1), set trick_winner_seat to the follower's seat; otherwise set it to leader_seat. Add the pips of led_card and follow_card (Ace 3; Ten, Nine, King, Ober, Unter 1; Eight, Seven 0) to the winner's deal_pips, plus 3 if trick_number = 16. Announce the winner and both deal_pips.
  6. [update] table. What happens: When talon_count > 0: append talon_up to the winner's hand and announce which card it was. Remove the first card of talon and append it to the loser's hand, without announcing it. Set talon_count = talon_count - 2. If talon_count > 0, remove the first card of talon and set talon_up to it; otherwise set talon_up = 'none'. Announce talon_up and talon_count.
  7. [update] table. What happens: Set leader_seat = trick_winner_seat, led_card = 'none' and follow_card = 'none'. If trick_number = 16, add each player's deal_pips to their match_total, announce both match_total values, set deal_number = deal_number + 1 and trick_number = 1. Otherwise set trick_number = trick_number + 1.
  8. [check] table. What happens: End the game if deal_number > 2; otherwise continue with the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the match starts, then there are 2 deals of 16 tricks each, 32 rounds in all, and each round is one trick.
  R2. When a deal starts (trick 1 of deal 1 or deal 2), then all 32 cards are shuffled, each player's hand gets 8 cards, and the other 16 form the talon.
  R3. When a deal starts, then the top talon card is turned face up as talon_up, talon_count is 16, and both deal_pips are set to 0.
  R4. When deal 1 starts, then seat 1 (Player A) leads trick 1; when deal 2 starts, then seat 2 (Player B) leads trick 1.
  R5. When a trick begins, then the leader may play any one card from their hand, which is removed from the hand and shown as led_card.
  R6. When the follower holds at least one card of the led suit, then only cards of that suit are offered to them.
  R7. When the follower holds no card of the led suit, then every card in their hand is offered.
  R8. When both cards are of the led suit, then the card of higher strength wins, with Ten 8, Nine 7, Ace 6, King 5, Ober 4, Unter 3, Eight 2, Seven 1.
  R9. When the follower's card is not of the led suit, then the leader wins the trick, because there are no trumps.
  R10. When a trick is won, then the winner adds the pips of both cards to their deal_pips: Ace 3; Ten, Nine, King, Ober and Unter 1; Eight and Seven 0.
  R11. When trick 16 of a deal is won, then the winner adds 3 extra pips to their deal_pips.
  R12. When a trick ends and talon_count > 0, then the winner takes talon_up into their hand openly and the loser takes the next talon card into their hand unseen by the winner.
  R13. When a talon draw leaves cards in the talon, then the new top card becomes talon_up; when it leaves none, then talon_up becomes 'none'.
  R14. When 8 tricks of a deal have been played, then the talon is empty (talon_count 0) and tricks 9 to 16 are played with no drawing.
  R15. When a trick ends, then its winner leads the next trick.
  R16. When trick 16 of a deal ends, then each player's deal_pips are added to their match_total.
  R17. When a deal is scored, then the deal_pips of the two players total 35.
  R18. When round 32 ends (deal_number becomes 3), then the game ends and the higher match_total wins.
  R19. When both match totals are equal (35 each), then the match is a draw and both players share the win.
  R20. When a player looks at the game, then they see only their own hand, but both players see the deal and trick numbers, leader, led_card, follow_card, talon_up, talon_count, both deal_pips and both match totals.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Leader plays a card | asked: the seat equal to leader_seat | options: every card in that seat's hand
  - Follower plays a card | asked: the seat not equal to leader_seat | options: if the hand holds any card of led_card's suit: only those cards; otherwise every card in the hand

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: deal_number > 2
  - each player's standing: you.match_total (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their match total, the pips summed over both deals (70 available). The higher total wins. Equal totals (35 each) share the win, which is a draw.
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

- each player: `deal_pips` (number, visible: public, starts 0): Pips won so far in the current deal, including the last-trick bonus.
- each player: `match_total` (number, visible: public, starts 0): Sum of deal pips from completed deals. This is the score.
- the table: `talon_up` (text, visible: public, starts 'none'): The face-up top card of the talon, or 'none'.
- the table: `talon_count` (number, visible: public, starts 0): Number of cards left in the talon, counting the talon-up card.
- the table: `deal_number` (number, visible: public, starts 1): The current deal, 1 or 2. It is set to 3 when the match is over.
- the table: `trick_number` (number, visible: public, starts 1): The current trick within the deal, from 1 to 16.
- the table: `leader_seat` (number, visible: public, starts 1): The seat that leads the current trick.
- the table: `led_card` (text, visible: public, starts 'none'): The card led to the current trick, or 'none'.
- the table: `follow_card` (text, visible: public, starts 'none'): The card played by the follower to the current trick, or 'none'.
- the table: `trick_winner_seat` (number, visible: public, starts 0): The seat that won the last trick.
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 32, suits = 4, ranks_per_suit = 8, hand_size = 8, talon_size = 16, tricks_per_deal = 16, deals = 2, total_rounds = 32, drawing_tricks_per_deal = 8, strength_ten = 8, strength_nine = 7, strength_ace = 6, strength_king = 5, strength_ober = 4, strength_unter = 3, strength_eight = 2, strength_seven = 1, pips_ace = 3, pips_ten = 1, pips_nine = 1, pips_king = 1, pips_ober = 1, pips_unter = 1, pips_eight = 0, pips_seven = 0, last_trick_bonus = 3, pips_per_deal = 35, pips_per_match = 70, deal_1_first_leader_seat = 1, deal_2_first_leader_seat = 2
- the game ends with ONE ending whose `rank_by` is `you.match_total`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
