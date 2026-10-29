# 10 coder

- time: 2026-10-28T02:39:34+00:00 (54.8s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 36feafd776db784d, reply sha256 486cd0f8ea95fc57

## Sent

````
# Task: write the XColos game file for "Mirror Brusquembille"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 2; set `meta.players` to {"min": 2, "max": 2, "suggested": 2} (the suggested size is the one the game plays best at).

CARDS. There are four suits (Spades, Hearts, Diamonds, Clubs) and four ranks. From highest to lowest the ranks are Ace (11 points), Ten (10 points), King (4 points) and Seven (0 points). Each player owns a private 16-card pile containing exactly one Ace, Ten, King and Seven of every suit, worth 100 points. Both piles have this same composition, and both players are told it.

HIDDEN INFORMATION. There are exactly three hidden elements.
(1) Player 1's hand: seen only by Player 1.
(2) Player 2's hand: seen only by Player 2.
(3) The order of the cards in both piles: hidden from BOTH players, fixed by the setup shuffles.
Everything else is public: the trump suit, the leader, the trick number, both scores, the NUMBER of cards left in each pile, and every card played face up so far. No player ever sees the cards in either pile. Because the starting composition is known, each player can work out which cards the opponent still has in hand and pile combined, but not which of them are in hand.

SETUP.
1) Shuffle each player's pile separately.
2) Each player takes the top 3 cards of their own pile as their hand, leaving 13 cards in each pile.
3) Draw one suit at random as the trump suit and announce it.
4) Choose the first leader at random and announce it.
5) Both scores start at 0.

EACH TRICK (16 tricks, numbered 1 to 16):
1. Each player sees their own hand. Both players see the trump suit, both scores, the trick number, the number of cards left in each pile (13 minus the number of tricks already completed in tricks 1 to 13, then 0), and every card played so far. Neither sees the cards inside any pile.
2. The leader chooses one card from their hand and plays it face up. Any card may be played.
3. The follower chooses one card from their hand and plays it face up. In tricks 1 to 13 any card may be played. In tricks 14, 15 and 16 the follower must play a card of the led suit if they hold one; otherwise any card.
4. Decide the winner in this order:
(a) If exactly one card is a trump, that card wins.
(b) If both cards are of the same suit, the higher rank wins. If they are identical in suit and rank, the leader wins.
(c) Otherwise (different suits, neither a trump), the leader wins.
5. The winner adds the point values of both cards to their score. In trick 16 the winner also adds 1 bonus point.
6. The winner leads the next trick.
7. In tricks 1 to 13, the winner draws the top card of their own pile, then the loser draws the top card of their own pile, so both again hold 3 cards. After trick 13 both piles are empty and no more cards are drawn.
8. After trick 16 the game ends.

The points total 201 (200 card points plus the 1 bonus point), so the scores cannot be equal.

How the winner is decided: After 16 tricks, the player with the higher score wins. Since 201 points are shared, a draw is impossible.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Mirror Brusquembille (2 to 2 players, best with 2)

Two-player, 16-trick card game. Each player draws from an identical private 16-card pile, and the follower must follow suit only in the last three tricks.

STATE (every item below must exist in the file):
  - each player: score (number, starts 0); everyone sees it. Card points won in tricks, plus the 1-point bonus if this player won trick 16.
  - each player: hand (list, starts []); only its owner sees it. Cards in this player's hand, 3 at most. Each card is a two-letter code: rank A/T/K/7, then suit S/H/D/C (e.g. 'TH').
  - each player: pile_count (number, starts 16); everyone sees it. Number of cards left in this player's own pile.
  - the table: pile_1 (list, starts ['AS', 'TS', 'KS', '7S', 'AH', 'TH', 'KH', '7H', 'AD', 'TD', 'KD', '7D', 'AC', 'TC', 'KC', '7C']); hidden from all players. Seat 1's private pile. Its order and contents are hidden from both players.
  - the table: pile_2 (list, starts ['AS', 'TS', 'KS', '7S', 'AH', 'TH', 'KH', '7H', 'AD', 'TD', 'KD', '7D', 'AC', 'TC', 'KC', '7C']); hidden from all players. Seat 2's private pile, hidden from both players.
  - the table: trump (text, starts ''); everyone sees it. Trump suit letter (S, H, D or C), drawn at random during setup.
  - the table: leader (number, starts 0); everyone sees it. Seat (1 or 2) that leads the current trick.
  - the table: trick (number, starts 1); everyone sees it. Number of the current trick, 1 to 16. It becomes 17 when the game ends.
  - the table: led_card (text, starts ''); everyone sees it. Card the leader played face up in the current trick.
  - the table: follow_card (text, starts ''); everyone sees it. Card the follower played face up in the current trick.
  - the table: played_cards (list, starts []); everyone sees it. Every card played face up so far, in order, with the seat that played it.
  - the table: trick_winner (number, starts 0); everyone sees it. Seat that won the trick just played.
  - parameters, each kept as a table attribute: ace_points = 11, ten_points = 10, king_points = 4, seven_points = 0, suits = 4, ranks = 4, pile_size = 16, pile_points = 100, hand_size = 3, pile_after_deal = 13, tricks = 16, last_drawing_trick = 13, first_must_follow_trick = 14, last_trick_bonus = 1, total_points = 201

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Each seat's pile (pile_1, pile_2) holds the 16 cards: one Ace, Ten, King and Seven of each of the four suits. Both players are told this composition.
  2. Each seat draws 3 cards at random from its own pile into its hand. Each pile then has 13 cards, and pile_count is set to 13 for both seats.
  3. One suit is drawn at random as trump and announced.
  4. The first leader is chosen at random (seat 1 or 2) and announced.
  5. Both scores are set to 0 and trick is set to 1.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [sync] all players. What happens: Each player sees their own hand plus the public trump, leader, trick, both scores, both pile_count values and played_cards. Neither sees pile_1 or pile_2.
  2. [ask] the seat equal to leader answers: one card from their hand. What happens: led_card = the chosen card. Remove it from the leader's hand and append it to played_cards. Announce it to both players.
  3. [ask] the seat not equal to leader answers: one card from their hand. If trick >= 14 and they hold a card of led_card's suit, only cards of that suit. What happens: follow_card = the chosen card. Remove it from the follower's hand and append it to played_cards. Announce it to both players.
  4. [update] all players. What happens: Set trick_winner. If exactly one of led_card and follow_card is of the trump suit, its player wins. Otherwise, if both cards share a suit, the follower wins only when follow_card's point value is strictly greater than led_card's (Ace 11 > Ten 10 > King 4 > Seven 0), and the leader wins otherwise, including identical cards. Otherwise (different suits, neither trump) the leader wins. Announce the winner.
  5. [update] trick_winner. What happens: Add points(led_card) + points(follow_card) to the winner's score, plus 1 if trick == 16. Points are A=11, T=10, K=4, 7=0. Announce both scores.
  6. [update] all players. What happens: leader = trick_winner.
  7. [update] trick_winner, then the other seat. What happens: Only when trick <= 13: the winner moves one random card from their own pile (pile_1 or pile_2) into their hand and loses 1 pile_count. Then the loser does the same from their own pile. Both hands are back to 3 cards.
  8. [update] all players. What happens: trick += 1.
  9. [check] all players. What happens: End the game if trick > 16. Otherwise play the next trick.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. At setup, each seat's pile holds exactly one A, T, K and 7 of each of the 4 suits: 16 cards worth 100 points.
  R2. At setup, each seat draws 3 cards from its own pile into its hand, leaving pile_count = 13 for each seat.
  R3. At setup, the trump suit is one of S, H, D, C chosen at random and made public. The first leader is seat 1 or seat 2 at random.
  R4. When the game starts, both scores are 0 and trick is 1.
  R5. When the leader plays, they may choose any card in their hand, and that card leaves their hand and is added to played_cards.
  R6. When trick is 1 to 13, the follower may play any card in their hand.
  R7. When trick is 14, 15 or 16 and the follower holds a card of the led suit, the follower must play a card of the led suit.
  R8. When trick is 14, 15 or 16 and the follower holds no card of the led suit, the follower may play any card.
  R9. When exactly one of the two played cards is a trump, the player of the trump wins the trick (e.g. trump H: 7H beats AS).
  R10. When both cards are of the same suit, the higher rank wins, with A > T > K > 7 (e.g. TS beats KS).
  R11. When both cards are identical in suit and rank, the leader wins the trick.
  R12. When the cards are of different suits and neither is a trump, the leader wins the trick (e.g. trump C, leader 7S, follower AH: the leader wins).
  R13. When a player wins a trick, their score increases by the points of both cards, with A=11, T=10, K=4, 7=0 (e.g. AS and TS give +21).
  R14. When trick 16 is won, the winner gets 1 bonus point on top of the card points.
  R15. When a trick is won, the winner leads the next trick.
  R16. When trick is 1 to 13, after the trick the winner and then the loser each draw 1 card from their own pile, each pile_count drops by 1, and both hands return to 3 cards.
  R17. When trick is 14, 15 or 16, no cards are drawn, and pile_count is 0 for both seats.
  R18. When trick 16 is complete, the game ends and the two scores total 201.
  R19. When the game ends, the seat with the higher score wins. A draw is impossible.
  R20. Neither player ever sees the cards in pile_1 or pile_2, and each player sees only their own hand.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Leader plays a card | asked: the seat equal to leader | options: every card currently in that seat's hand (3 cards in tricks 1 to 14, then 2, then 1)
  - Follower plays a card | asked: the seat not equal to leader | options: tricks 1 to 13: every card in hand. Tricks 14 to 16: only the cards in hand of led_card's suit if there is at least one, otherwise every card in hand

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: trick > 16
  - each player's standing: you.score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: After 16 tricks, the player with the higher score wins. The 201 points cannot split evenly, so there is no draw.
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

- each player: `score` (number, visible: public, starts 0): Card points won in tricks, plus the 1-point bonus if this player won trick 16.
- each player: `pile_count` (number, visible: public, starts 16): Number of cards left in this player's own pile.
- the table: `trump` (text, visible: public, starts ''): Trump suit letter (S, H, D or C), drawn at random during setup.
- the table: `leader` (number, visible: public, starts 0): Seat (1 or 2) that leads the current trick.
- the table: `trick` (number, visible: public, starts 1): Number of the current trick, 1 to 16. It becomes 17 when the game ends.
- the table: `led_card` (text, visible: public, starts ''): Card the leader played face up in the current trick.
- the table: `follow_card` (text, visible: public, starts ''): Card the follower played face up in the current trick.
- the table: `played_cards` (list, visible: public, starts []): Every card played face up so far, in order, with the seat that played it.
- the table: `trick_winner` (number, visible: public, starts 0): Seat that won the trick just played.
- parameters (each must be an attribute holding this value, never a number buried in a step): ace_points = 11, ten_points = 10, king_points = 4, seven_points = 0, suits = 4, ranks = 4, pile_size = 16, pile_points = 100, hand_size = 3, pile_after_deal = 13, tricks = 16, last_drawing_trick = 13, first_must_follow_trick = 14, last_trick_bonus = 1, total_points = 201
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
    "id": "mirror_brusquembille",
    "name": "Mirror Brusquembille",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "blurb": "Two players, identical private 16-card piles, 16 tricks; follow suit only in the last three."
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
        "key": "pile_count",
        "visible": "public",
        "type": "number",
        "initial": 16
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
        "key": "pile_1",
        "visible": "none",
        "type": "list",
        "initial": ["AS", "TS", "KS", "7S", "AH", "TH", "KH", "7H", "AD", "TD", "KD", "7D", "AC", "TC", "KC", "7C"]
      },
      {
        "key": "pile_2",
        "visible": "none",
        "type": "list",
        "initial": ["AS", "TS", "KS", "7S", "AH", "TH", "KH", "7H", "AD", "TD", "KD", "7D", "AC", "TC", "KC", "7C"]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "trump",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "leader",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "trick",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "led_card",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "follow_card",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "played_cards",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "trick_winner",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "ace_points",
        "visible": "public",
        "type": "number",
        "initial": 11
      },
      {
        "key": "ten_points",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "king_points",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "seven_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "suits",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "ranks",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "pile_size",
        "visible": "public",
        "type": "number",
        "initial": 16
      },
      {
        "key": "pile_points",
        "visible": "public",
        "type": "number",
        "initial": 100
      },
      {
        "key": "hand_size",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "pile_after_deal",
        "visible": "public",
        "type": "number",
        "initial": 13
      },
      {
        "key": "tricks",
        "visible": "public",
        "type": "number",
        "initial": 16
      },
      {
        "key": "last_drawing_trick",
        "visible": "public",
        "type": "number",
        "initial": 13
      },
      {
        "key": "first_must_follow_trick",
        "visible": "public",
        "type": "number",
        "initial": 14
      },
      {
        "key": "last_trick_bonus",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "total_points",
        "visible": "public",
        "type": "number",
        "initial": 201
      }
    ]
  },
  "setup": [
    {
      "use": "tell",
      "label": "the piles",
      "to": "all",
      "text": "Each player owns a private, shuffled pile of {pile_size} cards: one Ace, Ten, King and Seven of each of the {suits} suits (Spades, Hearts, Diamonds, Clubs), worth {pile_points} points. Both piles have this same composition. Nobody sees the order of either pile."
    },
    {
      "use": "update",
      "label": "the deal",
      "do": [
        {"set": {"key": "pick", "value": {"calc": "pile_1[int(uniform(0, len(pile_1)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "pile_1", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "pile_1[int(uniform(0, len(pile_1)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "pile_1", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "pile_1[int(uniform(0, len(pile_1)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "pile_1", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "pile_2[int(uniform(0, len(pile_2)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "pile_2", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "pile_2[int(uniform(0, len(pile_2)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "pile_2", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "pile_2[int(uniform(0, len(pile_2)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "pile_2", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": ""}},
        {"set": {"player": 1, "key": "pile_count", "value": {"calc": "len(pile_1)"}}},
        {"set": {"player": 2, "key": "pile_count", "value": {"calc": "len(pile_2)"}}}
      ],
      "text": "Each player takes the top {hand_size} cards of their own pile as their hand, leaving {pile_after_deal} cards in each pile."
    },
    {
      "use": "update",
      "label": "trump and first leader",
      "do": [
        {"set": {"key": "trump", "value": {"calc": "['S', 'H', 'D', 'C'][min(int(uniform(0, suits)), suits - 1)]"}}},
        {"set": {"key": "leader", "value": {"calc": "1 if uniform(0, 1) < 0.5 else 2"}}},
        {"set": {"players": "all", "key": "score", "value": 0}},
        {"set": {"key": "trick", "value": 1}}
      ],
      "text": "The trump suit is {trump}. Seat {leader} leads the first trick. Both scores start at 0."
    },
    {
      "use": "sync",
      "label": "the table",
      "mode": "self",
      "to": "all",
      "fields": ["hand", "score", "pile_count", "trump", "leader", "trick"],
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "sync",
      "phase": "play",
      "label": "your view",
      "mode": "self",
      "to": "all",
      "fields": ["hand", "score", "pile_count", "trump", "leader", "trick", "played_cards"],
      "text": "Trick {trick} of {tricks}. Trump {trump}, seat {leader} leads. Your state:"
    },
    {
      "use": "ask",
      "phase": "play",
      "label": "the lead",
      "to": {"where": "you.seat == leader"},
      "answer": {
        "type": "choice",
        "options": {"attribute": "hand"}
      },
      "verify": {"bind": "lead"},
      "text": "Trick {trick} of {tricks}, trump {trump}. You lead: play any one card from your hand face up."
    },
    {
      "use": "update",
      "phase": "play",
      "label": "the led card",
      "do": [
        {"set": {"key": "led_card", "value": "$lead"}},
        {"remove": {"player": {"calc": "leader"}, "key": "hand", "value": "$lead"}},
        {"append": {"key": "played_cards", "value": {"calc": "('seat 1: ' if leader == 1 else 'seat 2: ') + led_card"}}},
        {"set": {"players": "all", "key": "offer", "value": {"calc": "[c for c in you.hand if c[1] == led_card[1]] if (trick >= first_must_follow_trick and any(c[1] == led_card[1] for c in you.hand)) else you.hand"}}}
      ],
      "text": "Seat {leader} leads {led_card}."
    },
    {
      "use": "ask",
      "phase": "play",
      "label": "the follow",
      "to": {"where": "you.seat != leader"},
      "answer": {
        "type": "choice",
        "options": {"attribute": "offer"}
      },
      "verify": {"bind": "follow"},
      "text": "Trick {trick} of {tricks}, trump {trump}. Seat {leader} led {led_card}. Play one card face up from the cards offered (from trick {first_must_follow_trick} on you must follow the led suit if you can)."
    },
    {
      "use": "update",
      "phase": "play",
      "label": "the followed card",
      "do": [
        {"set": {"key": "follow_card", "value": "$follow"}},
        {"remove": {"player": {"calc": "3 - leader"}, "key": "hand", "value": "$follow"}},
        {"append": {"key": "played_cards", "value": {"calc": "('seat 1: ' if leader == 2 else 'seat 2: ') + follow_card"}}}
      ],
      "text": "The follower plays {follow_card}."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "the trick winner",
      "do": [
        {"set": {"key": "trick_winner", "value": {"calc": "((leader if led_card[1] == trump else 3 - leader) if ((led_card[1] == trump) != (follow_card[1] == trump)) else ((3 - leader) if (follow_card[1] == led_card[1] and (ace_points if follow_card[0] == 'A' else ten_points if follow_card[0] == 'T' else king_points if follow_card[0] == 'K' else seven_points) > (ace_points if led_card[0] == 'A' else ten_points if led_card[0] == 'T' else king_points if led_card[0] == 'K' else seven_points)) else leader))"}}}
      ],
      "text": "{led_card} against {follow_card}: seat {trick_winner} wins trick {trick}."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "the points",
      "do": [
        {"adjust": {"player": {"calc": "trick_winner"}, "key": "score", "value": {"calc": "(ace_points if led_card[0] == 'A' else ten_points if led_card[0] == 'T' else king_points if led_card[0] == 'K' else seven_points) + (ace_points if follow_card[0] == 'A' else ten_points if follow_card[0] == 'T' else king_points if follow_card[0] == 'K' else seven_points) + (last_trick_bonus if trick == tricks else 0)"}}}
      ],
      "text": "Scores: seat 1 {players[0].score}, seat 2 {players[1].score}."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "the next leader",
      "do": [
        {"set": {"key": "leader", "value": {"calc": "trick_winner"}}}
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "the draw",
      "when": {"calc": "trick <= last_drawing_trick"},
      "do": [
        {"set": {"key": "pick", "value": {"calc": "pile_1[int(uniform(0, len(pile_1)))]"}, "if": {"calc": "trick_winner == 1"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "trick_winner == 1"}}},
        {"remove": {"key": "pile_1", "value": {"calc": "pick"}, "if": {"calc": "trick_winner == 1"}}},
        {"adjust": {"player": 1, "key": "pile_count", "value": -1, "if": {"calc": "trick_winner == 1"}}},
        {"set": {"key": "pick", "value": {"calc": "pile_2[int(uniform(0, len(pile_2)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "pile_2", "value": {"calc": "pick"}}},
        {"adjust": {"player": 2, "key": "pile_count", "value": -1}},
        {"set": {"key": "pick", "value": {"calc": "pile_1[int(uniform(0, len(pile_1)))]"}, "if": {"calc": "trick_winner == 2"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "trick_winner == 2"}}},
        {"remove": {"key": "pile_1", "value": {"calc": "pick"}, "if": {"calc": "trick_winner == 2"}}},
        {"adjust": {"player": 1, "key": "pile_count", "value": -1, "if": {"calc": "trick_winner == 2"}}},
        {"set": {"key": "pick", "value": ""}}
      ],
      "text": "Seat {trick_winner} draws from their pile, then the other seat draws from theirs."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "next trick",
      "do": [
        {"adjust": {"key": "trick", "value": 1}}
      ]
    },
    {
      "use": "check",
      "phase": "resolve",
      "label": "after the last trick",
      "when": {"calc": "trick > tricks"},
      "against": ["over"]
    }
  ],
  "end": {
    "over": {
      "when": {"calc": "trick > tricks"},
      "rank_by": "you.score",
      "text": "Winner: {result}. Final scores: Seat 1 {players[0].score}, Seat 2 {players[1].score} (of {total_points})."
    }
  },
  "limits": {
    "rounds": 16,
    "rounds_max": 17,
    "actions_max": 400,
    "deadline_s": 120
  },
  "rules": "CARDS. Four suits (Spades S, Hearts H, Diamonds D, Clubs C) and four ranks. From highest to lowest: Ace A ({ace_points} points), Ten T ({ten_points} points), King K ({king_points} points), Seven 7 ({seven_points} points). Cards are written rank then suit, e.g. TH. Each player owns a private {pile_size}-card pile holding exactly one Ace, Ten, King and Seven of every suit, worth {pile_points} points. Both piles have this same composition.\n\nHIDDEN INFORMATION. Your hand is seen only by you. The order of the cards in both piles is hidden from both players. Everything else is public: the trump suit, the leader, the trick number, both scores, the number of cards left in each pile, and every card played face up so far. No player ever sees the cards in either pile.\n\nSETUP. Each pile is shuffled separately. Each player takes the top {hand_size} cards of their own pile as their hand, leaving {pile_after_deal} in each pile. One suit is drawn at random as trump and announced. The first leader is chosen at random and announced. Both scores start at 0.\n\nEACH TRICK ({tricks} tricks): The leader plays any one card from their hand face up. The follower then plays one card face up. In tricks 1 to {last_drawing_trick} the follower may play any card. From trick {first_must_follow_trick} to {tricks}, the follower must play a card of the led suit if they hold one; if they hold none, they may play any card.\nThe winner is decided in this order: (a) if exactly one card is a trump, that card wins; (b) if both cards are of the same suit, the higher rank wins, and if they are identical in suit and rank, the leader wins; (c) otherwise (different suits, neither a trump), the leader wins.\nThe winner adds the point values of both cards to their score; in trick {tricks} the winner also adds {last_trick_bonus} bonus point. The winner leads the next trick. In tricks 1 to {last_drawing_trick}, the winner draws the top card of their own pile, then the loser draws the top card of their own pile, so both again hold {hand_size} cards. After trick {last_drawing_trick} both piles are empty and no more cards are drawn.\n\nEND. After trick {tricks} the game ends. The points total {total_points}, so the scores cannot be equal: the player with the higher score wins."
}
```

Why it was refused: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (follow_card, led_card) in `your_view`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "mirror_brusquembille",
    "name": "Mirror Brusquembille",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "blurb": "Two players, identical private 16-card piles, 16 tricks; follow suit only in the last three."
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
        "key": "pile_count",
        "visible": "public",
        "type": "number",
        "initial": 16
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
        "key": "pile_1",
        "visible": "none",
        "type": "list",
        "initial": [
          "AS",
          "TS",
          "KS",
          "7S",
          "AH",
          "TH",
          "KH",
          "7H",
          "AD",
          "TD",
          "KD",
          "7D",
          "AC",
          "TC",
          "KC",
          "7C"
        ]
      },
      {
        "key": "pile_2",
        "visible": "none",
        "type": "list",
        "initial": [
          "AS",
          "TS",
          "KS",
          "7S",
          "AH",
          "TH",
          "KH",
          "7H",
          "AD",
          "TD",
          "KD",
          "7D",
          "AC",
          "TC",
          "KC",
          "7C"
        ]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "trump",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "leader",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "trick",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "led_card",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "follow_card",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "played_cards",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "trick_winner",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "ace_points",
        "visible": "public",
        "type": "number",
        "initial": 11
      },
      {
        "key": "ten_points",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "king_points",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "seven_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "suits",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "ranks",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "pile_size",
        "visible": "public",
        "type": "number",
        "initial": 16
      },
      {
        "key": "pile_points",
        "visible": "public",
        "type": "number",
        "initial": 100
      },
      {
        "key": "hand_size",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "pile_after_deal",
        "visible": "public",
        "type": "number",
        "initial": 13
      },
      {
        "key": "tricks",
        "visible": "public",
        "type": "number",
        "initial": 16
      },
      {
        "key": "last_drawing_trick",
        "visible": "public",
        "type": "number",
        "initial": 13
      },
      {
        "key": "first_must_follow_trick",
        "visible": "public",
        "type": "number",
        "initial": 14
      },
      {
        "key": "last_trick_bonus",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "total_points",
        "visible": "public",
        "type": "number",
        "initial": 201
      }
    ]
  },
  "setup": [
    {
      "use": "tell",
      "label": "the piles",
      "to": "all",
      "text": "Each player owns a private, shuffled pile of {pile_size} cards: one Ace, Ten, King and Seven of each of the {suits} suits (Spades, Hearts, Diamonds, Clubs), worth {pile_points} points. Both piles have this same composition. Nobody sees the order of either pile."
    },
    {
      "use": "update",
      "label": "the deal",
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "pile_1[int(uniform(0, len(pile_1)))]"
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
            "key": "pile_1",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "pile_1[int(uniform(0, len(pile_1)))]"
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
            "key": "pile_1",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "pile_1[int(uniform(0, len(pile_1)))]"
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
            "key": "pile_1",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "pile_2[int(uniform(0, len(pile_2)))]"
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
            "key": "pile_2",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "pile_2[int(uniform(0, len(pile_2)))]"
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
            "key": "pile_2",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "pile_2[int(uniform(0, len(pile_2)))]"
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
            "key": "pile_2",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": ""
          }
        },
        {
          "set": {
            "player": 1,
            "key": "pile_count",
            "value": {
              "calc": "len(pile_1)"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "pile_count",
            "value": {
              "calc": "len(pile_2)"
            }
          }
        }
      ],
      "text": "Each player takes the top {hand_size} cards of their own pile as their hand, leaving {pile_after_deal} cards in each pile."
    },
    {
      "use": "update",
      "label": "trump and first leader",
      "do": [
        {
          "set": {
            "key": "trump",
            "value": {
              "calc": "['S', 'H', 'D', 'C'][min(int(uniform(0, suits)), suits - 1)]"
            }
          }
        },
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "1 if uniform(0, 1) < 0.5 else 2"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": 0
          }
        },
        {
          "set": {
            "key": "trick",
            "value": 1
          }
        },
        {
          "set": {
            "key": "led_card",
            "value": "none yet"
          }
        },
        {
          "set": {
            "key": "follow_card",
            "value": "none yet"
          }
        }
      ],
      "text": "The trump suit is {trump}. Seat {leader} leads the first trick. Both scores start at 0."
    },
    {
      "use": "sync",
      "label": "the table",
      "mode": "self",
      "to": "all",
      "fields": [
        "hand",
        "score",
        "pile_count",
        "trump",
        "leader",
        "trick"
      ],
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "sync",
      "phase": "play",
      "label": "your view",
      "mode": "self",
      "to": "all",
      "fields": [
        "hand",
        "score",
        "pile_count",
        "trump",
        "leader",
        "trick",
        "played_cards"
      ],
      "text": "Trick {trick} of {tricks}. Trump {trump}, seat {leader} leads. Your state:"
    },
    {
      "use": "ask",
      "phase": "play",
      "label": "the lead",
      "to": {
        "where": "you.seat == leader"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "verify": {
        "bind": "lead"
      },
      "text": "Trick {trick} of {tricks}, trump {trump}. You lead: play any one card from your hand face up."
    },
    {
      "use": "update",
      "phase": "play",
      "label": "the led card",
      "do": [
        {
          "set": {
            "key": "led_card",
            "value": "$lead"
          }
        },
        {
          "remove": {
            "player": {
              "calc": "leader"
            },
            "key": "hand",
            "value": "$lead"
          }
        },
        {
          "append": {
            "key": "played_cards",
            "value": {
              "calc": "('seat 1: ' if leader == 1 else 'seat 2: ') + led_card"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "[c for c in you.hand if c[1] == led_card[1]] if (trick >= first_must_follow_trick and any(c[1] == led_card[1] for c in you.hand)) else you.hand"
            }
          }
        }
      ],
      "text": "Seat {leader} leads {led_card}."
    },
    {
      "use": "ask",
      "phase": "play",
      "label": "the follow",
      "to": {
        "where": "you.seat != leader"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "follow"
      },
      "text": "Trick {trick} of {tricks}, trump {trump}. Seat {leader} led {led_card}. Play one card face up from the cards offered (from trick {first_must_follow_trick} on you must follow the led suit if you can; otherwise any card)."
    },
    {
      "use": "update",
      "phase": "play",
      "label": "the followed card",
      "do": [
        {
          "set": {
            "key": "follow_card",
            "value": "$follow"
          }
        },
        {
          "remove": {
            "player": {
              "calc": "3 - leader"
            },
            "key": "hand",
            "value": "$follow"
          }
        },
        {
          "append": {
            "key": "played_cards",
            "value": {
              "calc": "('seat 1: ' if leader == 2 else 'seat 2: ') + follow_card"
            }
          }
        }
      ],
      "text": "The follower plays {follow_card}."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "the trick winner",
      "do": [
        {
          "set": {
            "key": "trick_winner",
            "value": {
              "calc": "((leader if led_card[1] == trump else 3 - leader) if ((led_card[1] == trump) != (follow_card[1] == trump)) else ((3 - leader) if (follow_card[1] == led_card[1] and (ace_points if follow_card[0] == 'A' else ten_points if follow_card[0] == 'T' else king_points if follow_card[0] == 'K' else seven_points) > (ace_points if led_card[0] == 'A' else ten_points if led_card[0] == 'T' else king_points if led_card[0] == 'K' else seven_points)) else leader))"
            }
          }
        }
      ],
      "text": "{led_card} against {follow_card}: seat {trick_winner} wins trick {trick}."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "the points",
      "do": [
        {
          "adjust": {
            "player": {
              "calc": "trick_winner"
            },
            "key": "score",
            "value": {
              "calc": "(ace_points if led_card[0] == 'A' else ten_points if led_card[0] == 'T' else king_points if led_card[0] == 'K' else seven_points) + (ace_points if follow_card[0] == 'A' else ten_points if follow_card[0] == 'T' else king_points if follow_card[0] == 'K' else seven_points) + (last_trick_bonus if trick == tricks else 0)"
            }
          }
        }
      ],
      "text": "Scores: seat 1 {players[0].score}, seat 2 {players[1].score}."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "the next leader",
      "do": [
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "trick_winner"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "the draw",
      "when": {
        "calc": "trick <= last_drawing_trick"
      },
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "pile_1[int(uniform(0, len(pile_1)))]"
            },
            "if": {
              "calc": "trick_winner == 1"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hand",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "trick_winner == 1"
            }
          }
        },
        {
          "remove": {
            "key": "pile_1",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "trick_winner == 1"
            }
          }
        },
        {
          "adjust": {
            "player": 1,
            "key": "pile_count",
            "value": -1,
            "if": {
              "calc": "trick_winner == 1"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "pile_2[int(uniform(0, len(pile_2)))]"
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
            "key": "pile_2",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "adjust": {
            "player": 2,
            "key": "pile_count",
            "value": -1
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "pile_1[int(uniform(0, len(pile_1)))]"
            },
            "if": {
              "calc": "trick_winner == 2"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hand",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "trick_winner == 2"
            }
          }
        },
        {
          "remove": {
            "key": "pile_1",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "trick_winner == 2"
            }
          }
        },
        {
          "adjust": {
            "player": 1,
            "key": "pile_count",
            "value": -1,
            "if": {
              "calc": "trick_winner == 2"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": ""
          }
        }
      ],
      "text": "Seat {trick_winner} draws from their pile, then the other seat draws from theirs."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "next trick",
      "do": [
        {
          "adjust": {
            "key": "trick",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "resolve",
      "label": "after the last trick",
      "when": {
        "calc": "trick > tricks"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "trick > tricks"
      },
      "rank_by": "you.score",
      "text": "Winner: {result}. Final scores: Seat 1 {players[0].score}, Seat 2 {players[1].score} (of {total_points})."
    }
  },
  "limits": {
    "rounds": 16,
    "rounds_max": 17,
    "actions_max": 400,
    "deadline_s": 120
  },
  "rules": "CARDS. Four suits (Spades S, Hearts H, Diamonds D, Clubs C) and four ranks. From highest to lowest: Ace A ({ace_points} points), Ten T ({ten_points} points), King K ({king_points} points), Seven 7 ({seven_points} points). Cards are written rank then suit, e.g. TH. Each player owns a private {pile_size}-card pile holding exactly one Ace, Ten, King and Seven of every suit, worth {pile_points} points. Both piles have this same composition.\n\nHIDDEN INFORMATION. Your hand is seen only by you. The order of the cards in both piles is hidden from both players. Everything else is public: the trump suit, the leader, the trick number, both scores, the number of cards left in each pile, and every card played face up so far. No player ever sees the cards in either pile.\n\nSETUP. Each pile is shuffled separately. Each player takes the top {hand_size} cards of their own pile as their hand, leaving {pile_after_deal} in each pile. One suit is drawn at random as trump and announced. The first leader is chosen at random and announced. Both scores start at 0.\n\nEACH TRICK ({tricks} tricks): The leader plays any one card from their hand face up. The follower then plays one card face up. In tricks 1 to {last_drawing_trick} the follower may play any card. From trick {first_must_follow_trick} to {tricks}, the follower must play a card of the led suit if they hold one; if they hold none, they may play any card.\nThe winner is decided in this order: (a) if exactly one card is a trump, that card wins; (b) if both cards are of the same suit, the higher rank wins, and if they are identical in suit and rank, the leader wins; (c) otherwise (different suits, neither a trump), the leader wins.\nThe winner adds the point values of both cards to their score; in trick {tricks} the winner also adds {last_trick_bonus} bonus point. The winner leads the next trick. In tricks 1 to {last_drawing_trick}, the winner draws the top card of their own pile, then the loser draws the top card of their own pile, so both again hold {hand_size} cards. After trick {last_drawing_trick} both piles are empty and no more cards are drawn.\n\nEND. After trick {tricks} the game ends. The points total {total_points}, so the scores cannot be equal: the player with the higher score wins."
}
```
````
