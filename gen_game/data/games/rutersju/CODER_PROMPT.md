# Task: write the XColos game file for "Rutersju Hook"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 5; set `meta.players` to {"min": 3, "max": 5, "suggested": 4} (the suggested size is the one the game plays best at).

SETUP. Use a 36-card French pack (6, 7, 8, 9, 10, J, Q, K, A in ♣ ♥ ♠ ♦). Seats are numbered 1 to N (N = 3, 4 or 5). Every player starts with 0 points. The game lasts 3 deals per player: 9 deals with 3 players, 12 with 4, 15 with 5. The priority seat is seat 1 in deal 1 and moves one seat to the left after each deal.

CARD STRENGTH. Every card has a unique strength from 1 to 36. The higher strength always wins.
- ♦7 = 36.
- The other diamonds: ♦A=35, ♦K=34, ♦Q=33, ♦J=32, ♦10=31, ♦9=30, ♦8=29, ♦6=28.
- The plain suits: ♠A=27, ♥A=26, ♣A=25, ♠K=24, ♥K=23, ♣K=22, ♠Q=21, ♥Q=20, ♣Q=19, ♠J=18, ♥J=17, ♣J=16, ♠10=15, ♥10=14, ♣10=13, ♠9=12, ♥9=11, ♣9=10, ♠8=9, ♥8=8, ♣8=7, ♠7=6, ♥7=5, ♣7=4, ♠6=3, ♥6=2, ♣6=1.

EACH DEAL.
1. Deal. Shuffle the full pack and deal 3 cards face down to each player. Each hand is seen only by its owner. Undealt cards stay hidden for the whole deal.
2. Bid (in turn). Starting with the player to the LEFT of the priority seat and going left, each player in turn announces a bid of 0, 1, 2 or 3, hearing all earlier bids. The priority seat bids last.
3. The hook. The last bidder (the priority seat) may not choose a bid that makes the sum of all bids exactly 3. The sum of the others' bids can only exceed 3 in this case if… it never matters: when the others' sum is already above 3, every bid is allowed.
4. Declarer. The player with the highest bid is the declarer. If several players tie for the highest bid, the one among them who bid LAST is the declarer. If every bid is 0, there is no declarer (the hook allows this only when the bids can total 0, which is permitted because 0 ≠ 3). Announce all bids and the declarer.
5. Tricks. Play 3 tricks. In each trick, every player secretly and simultaneously chooses one card from their hand. All chosen cards are revealed together. The card with the highest strength wins the trick, and its player adds 1 to their trick count. There is no need to follow suit. Played cards stay face up and public.
6. Settlement, for each player separately, where d = |bid − tricks won|:
   a. If d = 0, the player gains 3 + bid points (bid 0 → 3, bid 1 → 4, bid 2 → 5, bid 3 → 6).
   b. If d > 0, the player loses 2 × d points.
   c. The declarer, if there is one, additionally gains 1 point if their d = 0, or loses 1 point if their d > 0.
   Because exactly 3 tricks are won and the bids never total 3, at least one player misses every deal.
7. Announce all bids, trick counts and point totals. Move the priority seat one place to the left.

There is no discussion phase. Players communicate only through their bids, which are public and made in turn, and through the cards they play. Scores may go negative.

END. After the last deal, the single player with the highest point total wins. If two or more players tie for the highest total, the game is a draw.

How the winner is decided: After 3N deals, the single player with the highest total points wins. A tie for the highest total is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Rutersju Hook (3 to 5 players, best with 4)

A trick-taking game played with a 36-card pack. In each deal players bid 0-3 tricks in turn, and the last bidder may not make the bids total exactly 3. Players then play 3 tricks with simultaneous card choices and score for hitting their bid exactly.

STATE (every item below must exist in the file):
  - each player: score (number, starts 0); everyone sees it. Running point total. It may go negative.
  - each player: hand (list, starts []); only its owner sees it. Cards held this deal, each written 'strength:card', for example '36:♦7'.
  - each player: bid (number, starts 0); everyone sees it. This deal's bid, from 0 to 3.
  - each player: tricks (number, starts 0); everyone sees it. Tricks won this deal.
  - each player: played (text, starts ''); everyone sees it. Card played in the current trick. It is revealed only after all cards are chosen.
  - each player: is_declarer (bool, starts False); everyone sees it. Whether this player is the declarer of the current deal.
  - the table: deck (list, starts 'all 36 cards: 36:♦7, 35:♦A, 34:♦K, 33:♦Q, 32:♦J, 31:♦10, 30:♦9, 29:♦8, 28:♦6, 27:♠A, 26:♥A, 25:♣A, 24:♠K, 23:♥K, 22:♣K, 21:♠Q, 20:♥Q, 19:♣Q, 18:♠J, 17:♥J, 16:♣J, 15:♠10, 14:♥10, 13:♣10, 12:♠9, 11:♥9, 10:♣9, 9:♠8, 8:♥8, 7:♣8, 6:♠7, 5:♥7, 4:♣7, 3:♠6, 2:♥6, 1:♣6'); hidden from all players. The undealt cards. They stay hidden all deal.
  - the table: played_cards (list, starts []); everyone sees it. Cards played face up so far this deal.
  - the table: deal_number (number, starts 0); everyone sees it. Number of deals completed.
  - the table: total_deals (number, starts '3 * N'); everyone sees it. Length of the game: 3 deals per player.
  - the table: priority_seat (number, starts 1); everyone sees it. The seat that bids last in this deal.
  - the table: bid_sum (number, starts 0); everyone sees it. Sum of the bids made so far this deal.
  - the table: declarer_seat (number, starts 0); everyone sees it. Seat of the declarer; 0 means no declarer.
  - the table: trick_number (number, starts 0); everyone sees it. Tricks completed in this deal.
  - parameters, each kept as a table attribute: deck_size = 36, hand_size = 3, tricks_per_deal = 3, deals_per_player = 3, min_bid = 0, max_bid = 3, forbidden_bid_total = 3, exact_base_points = 3, miss_penalty_per_trick = 2, declarer_bonus = 1, declarer_penalty = 1, starting_score = 0, highest_strength = 36, lowest_strength = 1

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seats are numbered 1 to N, where N is 3, 4 or 5.
  2. Every player's score is set to 0.
  3. total_deals is set to 3 * N, priority_seat to 1 and deal_number to 0.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: Start a deal. Refill deck with all 36 cards. Clear every hand and played_cards. Set every bid, tricks and played to 0 or empty, every is_declarer to false, and bid_sum, declarer_seat and trick_number to 0. Deal 3 cards to each player: each card is a random draw removed from deck and appended to that player's hand.
  2. [sync] all players. What happens: Each player sees only their own hand.
  3. [ask] each player in turn, starting with seat (priority_seat mod N) + 1, going up the seat numbers with wraparound, and ending with priority_seat answers: A whole number from 0 to 3. For priority_seat, if bid_sum <= 3, the value 3 - bid_sum is not offered.. What happens: The player's bid is set to the answer and bid_sum is increased by the answer. Each bidder hears all earlier bids.
  4. [update] all players. What happens: If max bid is 0, set declarer_seat to 0. Otherwise declarer_seat is the seat with the highest bid; among tied players it is the one who bid latest in this deal's bidding order. Set is_declarer to true for that seat.
  5. [tell] all players. What happens: Announce every bid and the declarer (or 'no declarer').
  6. [repeat] all players. What happens: Repeat the next three steps until trick_number = 3.
  7. [poll] all players answers: One card from the player's own hand.. What happens: Each player's played is set to the chosen card. No player sees any choice until all choices are in.
  8. [update] all players. What happens: Remove each played card from its hand and append it to played_cards. The player whose played card has the highest strength (the number before the colon) adds 1 to tricks. Increase trick_number by 1.
  9. [tell] all players. What happens: Reveal all played cards together and announce the trick winner.
  10. [update] all players. What happens: Settle the deal. For each player, let d = |bid - tricks|. If d = 0, score += 3 + bid; otherwise score -= 2 * d. In addition, if is_declarer is true: if d = 0, score += 1; otherwise score -= 1. Then deal_number += 1 and priority_seat = (priority_seat mod N) + 1.
  11. [tell] all players. What happens: Announce all bids, trick counts and scores, and the new priority_seat.
  12. [check] all players. What happens: End the game if deal_number >= total_deals; otherwise start the next deal.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, every player has 0 points, priority_seat is 1, and total_deals is 3 * N (9 for 3 players, 12 for 4, 15 for 5).
  R2. When a deal starts, the full 36-card pack is reshuffled and each player is dealt exactly 3 cards into their hand, removed from deck. With N players, 36 - 3N cards stay hidden in deck.
  R3. When a hand is dealt, only its owner can see it, and deck is visible to no one.
  R4. When bidding happens, seats bid in order starting at the seat after priority_seat (wrapping from N to 1), each hearing all earlier bids, and priority_seat bids last.
  R5. When any player bids, the bid is a whole number from 0 to 3.
  R6. When the priority seat bids and the others' bids sum to s <= 3, the bid 3 - s is not allowed. For example, if the others sum to 1, the priority seat may bid 0, 1 or 3 but not 2.
  R7. When the others' bids sum to more than 3, the priority seat may bid any of 0, 1, 2 or 3.
  R8. When bidding ends, the player with the highest bid is the declarer. If players tie for the highest bid, the tied player who bid latest is the declarer.
  R9. When every bid is 0, there is no declarer (declarer_seat = 0).
  R10. When a trick is played, every player simultaneously chooses one card from their hand, and no choice is seen until all are in.
  R11. When the cards of a trick are revealed, the card with the highest strength wins, with no need to follow suit, and its player's tricks increases by 1. For example, ♦7 (36) beats ♦A (35), and ♦6 (28) beats ♠A (27).
  R12. When a card is played, it leaves the hand and is added to the public played_cards list.
  R13. When a deal has had 3 tricks, it moves to settlement.
  R14. When a player's tricks equals their bid, they gain 3 + bid points: 3 for bid 0, 4 for bid 1, 5 for bid 2, 6 for bid 3.
  R15. When a player's tricks differ from their bid by d > 0, they lose 2 * d points. For example, bid 3 with 1 trick loses 4.
  R16. When the declarer hits their bid exactly, they gain 1 extra point. When the declarer misses, they lose 1 extra point.
  R17. When settlement ends, scores may be negative, deal_number increases by 1, and priority_seat moves to (priority_seat mod N) + 1.
  R18. When deal_number reaches 3 * N, the game ends and the player with the highest score wins. A tie at the top is a draw, shared among the tied players.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Bid | asked: every seat except priority_seat | options: 0, 1, 2, 3
  - Bid | asked: priority_seat | options: If the sum s of the earlier bids is <= 3: 0, 1, 2, 3 except 3 - s. If s > 3: 0, 1, 2, 3.
  - Card for the trick | asked: all players | options: Exactly the cards currently in that player's own hand (3 in trick 1, 2 in trick 2, 1 in trick 3).

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: deal_number >= total_deals
  - each player's standing: you.score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: After 3N deals, the player with the highest score wins. If several players tie for the highest score, they share the result, which is the source's draw.
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

- each player: `score` (number, visible: public, starts 0): Running point total. It may go negative.
- each player: `bid` (number, visible: public, starts 0): This deal's bid, from 0 to 3.
- each player: `tricks` (number, visible: public, starts 0): Tricks won this deal.
- the table: `deal_number` (number, visible: public, starts 0): Number of deals completed.
- the table: `priority_seat` (number, visible: public, starts 1): The seat that bids last in this deal.
- the table: `declarer_seat` (number, visible: public, starts 0): Seat of the declarer; 0 means no declarer.
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 36, hand_size = 3, tricks_per_deal = 3, deals_per_player = 3, min_bid = 0, max_bid = 3, forbidden_bid_total = 3, exact_base_points = 3, miss_penalty_per_trick = 2, declarer_bonus = 1, declarer_penalty = 1, starting_score = 0, highest_strength = 36, lowest_strength = 1
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
