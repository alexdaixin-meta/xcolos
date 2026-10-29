# 12 coder

- time: 2026-10-28T02:32:38+00:00 (119.1s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 5d667ae75648ea48, reply sha256 c3579a1effd2e39a

## Sent

````
# Task: write the XColos game file for "Democracy: Three Tribes"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

DECK: 24 cards in 3 suits (Hearts, Spades, Diamonds). Each suit has 8 cards. From highest rank to lowest they are: Five (5 points), Four (4), Three (3), Ace (3), King (2), Queen (2), Jack (1), Six (0). Each suit totals 20 points.

MATCH: 4 deals of 6 tricks each, 24 tricks in total.

START OF EACH DEAL (tricks 1, 7, 13, 19):
- Shuffle all 24 cards.
- Deal 6 cards face down to each player as their private hand.
- Deal 6 cards face down as the voting pool, in order. Nobody sees the pool.
- Reset every player's suit tallies to 0.

EACH TRICK:
1. Flip the next voting-pool card face up. Its suit is the trump suit for this trick, and the card itself is the prize.
2. Talk: every player writes one short message at the same time, without seeing the others. All three messages are then shown to everyone. Nothing said is binding.
3. Play: every player secretly chooses one card from their hand, at the same moment. All three cards are revealed together and removed from the hands.
4. Resolve the trick:
   (a) If one or more trump-suit cards were played, the highest-ranked trump wins. Exception: if both the Six and the Five of trump were played, the Six wins.
   (b) If no trump was played, the highest-ranked card wins regardless of suit.
   (c) If no trump was played and two or more cards tie for highest rank (same rank, different suits), nobody wins the trick. Each player captures their own played card, and the voting card is discarded with no one scoring it.
5. Score the capture: for each captured card, add its points to the capturing player's tally for that card's suit. Normally the winner captures all 3 played cards plus the voting card.
6. All played cards and every voting card ever flipped stay visible to everyone for the rest of the deal, along with all suit tallies.

END OF EACH DEAL (after tricks 6, 12, 18, 24):
- For each suit, the player whose tally in that suit is 11 or more wins that suit's tribe and adds 1 to their tribe count.
- A suit with no player at 11+ awards no tribe.
- Announce everyone's tribe counts.

END OF MATCH: after trick 24 and its tribe scoring, apply the objective.

How the winner is decided: The player with the most tribes after 4 deals wins. If two or more players tie for most tribes, the tied player with the highest sum of their three suit tallies in the 4th deal wins. If they are still tied, the game is a draw among the tied players.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Democracy: Three Tribes (3 to 3 players, best with 3)

Three players play simultaneous trick-taking over 4 deals of 6 tricks. Each trick's prize card sets trump, and a player who captures 11 or more points in a suit during a deal wins that suit's tribe.

STATE (every item below must exist in the file):
  - each player: hand (list, starts []); only its owner sees it. The player's private cards for this deal. Cards are written as rank+suit, e.g. '5H', 'AS', '6D'.
  - each player: played_card (text, starts ''); everyone sees it. The card this player played this trick. It is set when all cards are revealed together.
  - each player: strength (number, starts 0); everyone sees it. Trick strength of the played card: its rank number, plus 100 if it is trump, or 200 if it is the trump Six when the trump Five was also played.
  - each player: tally_hearts (number, starts 0); everyone sees it. Points captured in Hearts this deal.
  - each player: tally_spades (number, starts 0); everyone sees it. Points captured in Spades this deal.
  - each player: tally_diamonds (number, starts 0); everyone sees it. Points captured in Diamonds this deal.
  - each player: tribes (number, starts 0); everyone sees it. Tribes won over the match. This is the score.
  - the table: deck (list, starts ['5H', '4H', '3H', 'AH', 'KH', 'QH', 'JH', '6H', '5S', '4S', '3S', 'AS', 'KS', 'QS', 'JS', '6S', '5D', '4D', '3D', 'AD', 'KD', 'QD', 'JD', '6D']); hidden from all players. Undealt cards. All 24 are restored and redealt at the start of each deal.
  - the table: pool (list, starts []); hidden from all players. The 6 face-down voting cards for this deal, in order.
  - the table: prize (text, starts ''); everyone sees it. The voting card flipped this trick.
  - the table: trump (text, starts ''); everyone sees it. The suit of the prize card (H, S or D).
  - the table: revealed (list, starts []); everyone sees it. All played cards and flipped voting cards so far this deal.
  - the table: trick_winner (number, starts 0); everyone sees it. Seat that won this trick, or 0 if nobody won (a tied top rank with no trump played).
  - the table: trick (number, starts 0); everyone sees it. Tricks played so far (0 to 24).
  - the table: deal (number, starts 0); everyone sees it. Current deal number (1 to 4).
  - parameters, each kept as a table attribute: players = 3, deck_size = 24, suits = 3, cards_per_suit = 8, suit_points_total = 20, deals = 4, tricks_per_deal = 6, total_tricks = 24, hand_size = 6, pool_size = 6, tribe_threshold = 11, tribe_award = 1, points_five = 5, points_four = 4, points_three = 3, points_ace = 3, points_king = 2, points_queen = 2, points_jack = 1, points_six = 0, rank_five = 8, rank_four = 7, rank_three = 6, rank_ace = 5, rank_king = 4, rank_queen = 3, rank_jack = 2, rank_six = 1, trump_bonus = 100, six_beats_five_strength = 200, rank_weight_tribes = 1000

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seat the 3 players.
  2. Set every player's tribes to 0, and set trick and deal to 0.
  3. Put all 24 cards in the deck: 8 ranks (5, 4, 3, A, K, Q, J, 6) in each of Hearts, Spades and Diamonds.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: When trick % 6 == 0 (start of a deal): deal += 1; deck = all 24 cards; draw 6 random cards from deck into each player's hand (removing them from deck); draw the remaining 6 at random into pool, in order; set tally_hearts, tally_spades and tally_diamonds to 0 for every player; revealed = [].
  2. [sync] all players. What happens: When trick % 6 == 0: each player is sent their own hand and the public state.
  3. [update] all players. What happens: trick += 1; prize = first card of pool, removed from pool; trump = suit of prize; append prize to revealed; trick_winner = 0.
  4. [tell] all players. What happens: Announce: 'Deal {deal}, trick {trick}: the voting card is {prize}; trump is {trump}.'
  5. [poll] all players answers: short text message. What happens: Every player writes one message at the same time. All are then broadcast: {"to": "all", "text": "Seat {seat} says: {value}"}. Nothing said is binding.
  6. [poll] all players answers: one card from the player's own hand. What happens: Simultaneously, each player's chosen card becomes played_card and is removed from hand.
  7. [update] all players. What happens: Append all three played_card values to revealed. Each player's strength = the card's rank number (5=8, 4=7, 3=6, A=5, K=4, Q=3, J=2, 6=1), plus 100 if its suit == trump; if the played card is the 6 of trump and some player played the 5 of trump, strength = 200. If exactly one player holds the maximum strength, trick_winner = that seat; otherwise trick_winner = 0.
  8. [update] all players. What happens: If trick_winner > 0: for each of the 3 played cards and the prize, add the card's points (5=5, 4=4, 3=3, A=3, K=2, Q=2, J=1, 6=0) to the winner's tally for that card's suit (tally_hearts, tally_spades or tally_diamonds). If trick_winner == 0: each player adds their own played_card's points to their own tally for its suit, and the prize scores for no one.
  9. [tell] all players. What happens: Announce the played cards, trick_winner (0 means nobody), and every player's tally_hearts, tally_spades and tally_diamonds.
  10. [update] all players. What happens: When trick % 6 == 0 (end of a deal): for each suit, the player with that suit's tally >= 11 adds 1 to tribes. A suit with no player at 11 or more awards nothing.
  11. [tell] all players. What happens: When trick % 6 == 0: announce every player's tribes.
  12. [check] all players. What happens: If trick == 24, end the game; otherwise run the round again.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. The deck has 24 cards: 8 ranks (5, 4, 3, A, K, Q, J, 6) in each of Hearts, Spades and Diamonds, worth 5, 4, 3, 3, 2, 2, 1, 0 points, so each suit totals 20 points.
  R2. The match is 4 deals of 6 tricks, 24 tricks in total.
  R3. At the start of each deal (before tricks 1, 7, 13, 19), all 24 cards are shuffled: each player's hand gets 6 cards and the pool gets 6 cards, leaving the deck empty.
  R4. At the start of each deal, every player's tally_hearts, tally_spades and tally_diamonds is reset to 0, and tribes is kept.
  R5. Each trick, the next pool card is removed from the pool and becomes the prize, and its suit becomes trump.
  R6. Each trick, every player sends one short message at the same time, and all three are shown to everyone.
  R7. Each trick, every player plays one card from their own hand at the same time; the card is removed from their hand and revealed to all.
  R8. When one or more trump cards are played, the highest-ranked trump wins (rank order 5 > 4 > 3 > A > K > Q > J > 6).
  R9. When both the 6 and the 5 of trump are played, the player of the 6 of trump wins the trick.
  R10. When no trump is played, the highest-ranked card wins regardless of suit.
  R11. When no trump is played and two or more cards tie for highest rank, trick_winner is 0: each player adds their own card's points to their own tally for its suit, and the prize scores for nobody.
  R12. When a player wins a trick, the points of all 3 played cards and the prize are added to that player's tallies, each card to its own suit's tally.
  R13. Played cards, flipped voting cards and all tallies stay public for the rest of the deal.
  R14. At the end of each deal (after tricks 6, 12, 18, 24), a player with 11 or more in a suit tally gains 1 tribe for that suit.
  R15. At the end of a deal, a suit in which no player has 11 or more awards no tribe.
  R16. The game ends after trick 24 and its tribe scoring.
  R17. The player with the most tribes wins; a tie on tribes is broken by the higher sum of the 4th-deal tallies; players still tied share the win.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Talk message each trick | asked: all seats | options: any short free-text message
  - Card to play each trick | asked: all seats | options: exactly the cards currently in that seat's own hand (6 in the first trick of a deal, down to 1 in the sixth)

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: game.trick == 24
  - each player's standing: you.tribes * 1000 + you.tally_hearts + you.tally_spades + you.tally_diamonds (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Most tribes after 4 deals wins. A tie on tribes is broken by the highest sum of the three suit tallies in the 4th deal. Players still tied share the win (a draw among them).
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

- each player: `played_card` (text, visible: public, starts ''): The card this player played this trick. It is set when all cards are revealed together.
- each player: `tally_hearts` (number, visible: public, starts 0): Points captured in Hearts this deal.
- each player: `tally_spades` (number, visible: public, starts 0): Points captured in Spades this deal.
- each player: `tally_diamonds` (number, visible: public, starts 0): Points captured in Diamonds this deal.
- each player: `tribes` (number, visible: public, starts 0): Tribes won over the match. This is the score.
- the table: `prize` (text, visible: public, starts ''): The voting card flipped this trick.
- the table: `trump` (text, visible: public, starts ''): The suit of the prize card (H, S or D).
- the table: `trick_winner` (number, visible: public, starts 0): Seat that won this trick, or 0 if nobody won (a tied top rank with no trump played).
- parameters (each must be an attribute holding this value, never a number buried in a step): players = 3, deck_size = 24, suits = 3, cards_per_suit = 8, suit_points_total = 20, deals = 4, tricks_per_deal = 6, total_tricks = 24, hand_size = 6, pool_size = 6, tribe_threshold = 11, tribe_award = 1, points_five = 5, points_four = 4, points_three = 3, points_ace = 3, points_king = 2, points_queen = 2, points_jack = 1, points_six = 0, rank_five = 8, rank_four = 7, rank_three = 6, rank_ace = 5, rank_king = 4, rank_queen = 3, rank_jack = 2, rank_six = 1, trump_bonus = 100, six_beats_five_strength = 200, rank_weight_tribes = 1000
- the game ends with ONE ending whose `rank_by` is `you.tribes * 1000 + you.tally_hearts + you.tally_spades + you.tally_diamonds`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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

1. Remove the separate player-facing 'your_new_hand' step, or make it silent. Players should not get a prompt when the cards are dealt.
2. At the start of each deal, run these as non-prompting steps: shuffle the deck, deal 6 cards to each hand, build the 6-card pool, reset the suit tallies, then flip the first pool card into `prize` and set `trump` from its suit.
3. Make the talk step of the trick the first thing any player is shown. By then `prize` and `trump` already hold values. The private hand can be shown inside that talk prompt.
4. Do not clear `played_card` back to '' at the start of a deal or a trick. Leave it holding the last revealed card until the next simultaneous reveal overwrites it.
5. If a blank `played_card` on the very first trick is still flagged, keep it out of the opening prompt. One way is to show the previous-trick information only from trick 2 onward. Do not change its interface name or visibility.
6. Keep any internal lists hidden: deck, pool, hands-in-progress and scratch strengths. Use `none` visibility on the table and `ally` on players.
7. Every non-interface attribute you keep must really be changed by a step that runs. For example, the deck list must be shuffled and have cards removed from it following the deck recipe. Otherwise delete it, as was needed for `all_cards` in attempt 3.

````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "democracy_three_tribes",
    "name": "Democracy: Three Tribes",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Three players, simultaneous tricks over 4 deals: each prize card sets trump, and 11+ points in a suit in one deal wins that suit's tribe."
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
        "key": "played_card",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "strength",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tally_hearts",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tally_spades",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tally_diamonds",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tribes",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ],
    "game": [
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": [
          "5H",
          "4H",
          "3H",
          "AH",
          "KH",
          "QH",
          "JH",
          "6H",
          "5S",
          "4S",
          "3S",
          "AS",
          "KS",
          "QS",
          "JS",
          "6S",
          "5D",
          "4D",
          "3D",
          "AD",
          "KD",
          "QD",
          "JD",
          "6D"
        ]
      },
      {
        "key": "pool",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "prize",
        "visible": "public",
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
        "key": "revealed",
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
        "key": "trick",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "deal",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "players",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 24
      },
      {
        "key": "suits",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "cards_per_suit",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "suit_points_total",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "deals",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "tricks_per_deal",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "total_tricks",
        "visible": "public",
        "type": "number",
        "initial": 24
      },
      {
        "key": "hand_size",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "pool_size",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "tribe_threshold",
        "visible": "public",
        "type": "number",
        "initial": 11
      },
      {
        "key": "tribe_award",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "points_five",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "points_four",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "points_three",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "points_ace",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "points_king",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "points_queen",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "points_jack",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "points_six",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "rank_five",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "rank_four",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "rank_three",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "rank_ace",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "rank_king",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "rank_queen",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "rank_jack",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "rank_six",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "trump_bonus",
        "visible": "public",
        "type": "number",
        "initial": 100
      },
      {
        "key": "six_beats_five_strength",
        "visible": "public",
        "type": "number",
        "initial": 200
      },
      {
        "key": "rank_weight_tribes",
        "visible": "public",
        "type": "number",
        "initial": 1000
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
            "key": "tribes",
            "value": 0
          }
        },
        {
          "set": {
            "key": "trick",
            "value": 0
          }
        },
        {
          "set": {
            "key": "deal",
            "value": 0
          }
        },
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "['5H', '4H', '3H', 'AH', 'KH', 'QH', 'JH', '6H', '5S', '4S', '3S', 'AS', 'KS', 'QS', 'JS', '6S', '5D', '4D', '3D', 'AD', 'KD', 'QD', 'JD', '6D']"
            }
          }
        }
      ]
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "deal",
      "label": "start of a deal",
      "when": {
        "calc": "trick % tricks_per_deal == 0"
      },
      "do": [
        {
          "adjust": {
            "key": "deal",
            "value": 1
          }
        },
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "['5H', '4H', '3H', 'AH', 'KH', 'QH', 'JH', '6H', '5S', '4S', '3S', 'AS', 'KS', 'QS', 'JS', '6S', '5D', '4D', '3D', 'AD', 'KD', 'QD', 'JD', '6D']"
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
            "key": "pool",
            "value": {
              "calc": "[]"
            }
          }
        },
        {
          "set": {
            "key": "revealed",
            "value": {
              "calc": "[]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "tally_hearts",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "tally_spades",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "tally_diamonds",
            "value": 0
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
        {"append": {"key": "pool", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"key": "pool", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"key": "pool", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"key": "pool", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"key": "pool", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"key": "pool", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}}
      ]
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "flip the voting card",
      "do": [
        {
          "adjust": {
            "key": "trick",
            "value": 1
          }
        },
        {
          "set": {
            "key": "prize",
            "value": {
              "calc": "pool[0]"
            }
          }
        },
        {
          "remove": {
            "key": "pool",
            "value": {
              "calc": "prize"
            }
          }
        },
        {
          "set": {
            "key": "trump",
            "value": {
              "calc": "prize[1]"
            }
          }
        },
        {
          "set": {
            "key": "revealed",
            "value": {
              "calc": "revealed + [prize]"
            }
          }
        },
        {
          "set": {
            "key": "trick_winner",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "poll",
      "phase": "talk",
      "label": "talk",
      "to": "acting",
      "answer": {
        "type": "text",
        "max_words": 30
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} says: {value}"
      },
      "text": "Deal {deal}, trick {trick}: the voting card is {prize}; trump is {trump}. Your hand: {hand}. Write one short message to the table. Everyone writes at the same time; nothing said is binding."
    },
    {
      "use": "poll",
      "phase": "play",
      "label": "play a card",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "store": "played_card",
      "text": "Deal {deal}, trick {trick}: the prize is {prize}, trump is {trump}. Choose one card from your hand to play face down. All three cards are revealed together."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "resolve the trick",
      "do": [
        {
          "remove": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "you.played_card"
            }
          }
        },
        {
          "set": {
            "key": "revealed",
            "value": {
              "calc": "revealed + [p.played_card for p in acting]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "strength",
            "value": {
              "calc": "six_beats_five_strength if (you.played_card == '6' + trump and count(p.played_card == '5' + trump for p in acting) > 0) else ((rank_five if you.played_card[0] == '5' else rank_four if you.played_card[0] == '4' else rank_three if you.played_card[0] == '3' else rank_ace if you.played_card[0] == 'A' else rank_king if you.played_card[0] == 'K' else rank_queen if you.played_card[0] == 'Q' else rank_jack if you.played_card[0] == 'J' else rank_six) + (trump_bonus if you.played_card[1] == trump else 0))"
            }
          }
        },
        {
          "set": {
            "key": "trick_winner",
            "value": {
              "calc": "max([p.seat for p in acting if p.strength == max([q.strength for q in acting])]) if count(p.strength == max([q.strength for q in acting]) for p in acting) == 1 else 0"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "score the capture",
      "do": [
        {
          "adjust": {
            "players": "all",
            "key": "tally_hearts",
            "value": {
              "calc": "sum([(points_five if c[0] == '5' else points_four if c[0] == '4' else points_three if c[0] == '3' else points_ace if c[0] == 'A' else points_king if c[0] == 'K' else points_queen if c[0] == 'Q' else points_jack if c[0] == 'J' else points_six) for c in ([p.played_card for p in acting] + [prize]) if c[1] == 'H']) if you.seat == trick_winner else ((points_five if you.played_card[0] == '5' else points_four if you.played_card[0] == '4' else points_three if you.played_card[0] == '3' else points_ace if you.played_card[0] == 'A' else points_king if you.played_card[0] == 'K' else points_queen if you.played_card[0] == 'Q' else points_jack if you.played_card[0] == 'J' else points_six) if (trick_winner == 0 and you.played_card[1] == 'H') else 0)"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "tally_spades",
            "value": {
              "calc": "sum([(points_five if c[0] == '5' else points_four if c[0] == '4' else points_three if c[0] == '3' else points_ace if c[0] == 'A' else points_king if c[0] == 'K' else points_queen if c[0] == 'Q' else points_jack if c[0] == 'J' else points_six) for c in ([p.played_card for p in acting] + [prize]) if c[1] == 'S']) if you.seat == trick_winner else ((points_five if you.played_card[0] == '5' else points_four if you.played_card[0] == '4' else points_three if you.played_card[0] == '3' else points_ace if you.played_card[0] == 'A' else points_king if you.played_card[0] == 'K' else points_queen if you.played_card[0] == 'Q' else points_jack if you.played_card[0] == 'J' else points_six) if (trick_winner == 0 and you.played_card[1] == 'S') else 0)"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "tally_diamonds",
            "value": {
              "calc": "sum([(points_five if c[0] == '5' else points_four if c[0] == '4' else points_three if c[0] == '3' else points_ace if c[0] == 'A' else points_king if c[0] == 'K' else points_queen if c[0] == 'Q' else points_jack if c[0] == 'J' else points_six) for c in ([p.played_card for p in acting] + [prize]) if c[1] == 'D']) if you.seat == trick_winner else ((points_five if you.played_card[0] == '5' else points_four if you.played_card[0] == '4' else points_three if you.played_card[0] == '3' else points_ace if you.played_card[0] == 'A' else points_king if you.played_card[0] == 'K' else points_queen if you.played_card[0] == 'Q' else points_jack if you.played_card[0] == 'J' else points_six) if (trick_winner == 0 and you.played_card[1] == 'D') else 0)"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "resolve",
      "label": "the reveal",
      "to": "all",
      "text": "Trick {trick} (prize {prize}, trump {trump}): Seat 1 played {players[0].played_card}, Seat 2 played {players[1].played_card}, Seat 3 played {players[2].played_card}. Trick winner: seat {trick_winner} (0 means nobody). Tallies Hearts/Spades/Diamonds: Seat 1 {players[0].tally_hearts}/{players[0].tally_spades}/{players[0].tally_diamonds}, Seat 2 {players[1].tally_hearts}/{players[1].tally_spades}/{players[1].tally_diamonds}, Seat 3 {players[2].tally_hearts}/{players[2].tally_spades}/{players[2].tally_diamonds}."
    },
    {
      "use": "update",
      "phase": "end of deal",
      "label": "award the tribes",
      "when": {
        "calc": "trick % tricks_per_deal == 0"
      },
      "do": [
        {
          "adjust": {
            "players": "all",
            "key": "tribes",
            "value": {
              "calc": "tribe_award * ((1 if you.tally_hearts >= tribe_threshold else 0) + (1 if you.tally_spades >= tribe_threshold else 0) + (1 if you.tally_diamonds >= tribe_threshold else 0))"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "end of deal",
      "label": "tribe counts",
      "when": {
        "calc": "trick % tricks_per_deal == 0"
      },
      "to": "all",
      "text": "Deal {deal} is over. Tribes: Seat 1 {players[0].tribes}, Seat 2 {players[1].tribes}, Seat 3 {players[2].tribes}."
    },
    {
      "use": "check",
      "phase": "end of deal",
      "label": "after trick 24",
      "when": {
        "calc": "trick == total_tricks"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "trick == total_tricks"
      },
      "rank_by": "you.tribes * 1000 + you.tally_hearts + you.tally_spades + you.tally_diamonds",
      "text": "Winner: {result}. Tribes: Seat 1 {players[0].tribes}, Seat 2 {players[1].tribes}, Seat 3 {players[2].tribes}; 4th-deal tally totals: Seat 1 {players[0].tally_hearts + players[0].tally_spades + players[0].tally_diamonds}, Seat 2 {players[1].tally_hearts + players[1].tally_spades + players[1].tally_diamonds}, Seat 3 {players[2].tally_hearts + players[2].tally_spades + players[2].tally_diamonds}."
    }
  },
  "limits": {
    "rounds": 24,
    "rounds_max": 30,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "The deck has {deck_size} cards in {suits} suits (Hearts H, Spades S, Diamonds D), {cards_per_suit} per suit. From highest rank to lowest: Five ({points_five} points), Four ({points_four}), Three ({points_three}), Ace ({points_ace}), King ({points_king}), Queen ({points_queen}), Jack ({points_jack}), Six ({points_six}). Each suit totals {suit_points_total} points. Cards are written rank+suit, e.g. 5H, AS, 6D.\n\nThe match is {deals} deals of {tricks_per_deal} tricks each, {total_tricks} tricks in total.\n\nStart of each deal (before tricks 1, 7, 13, 19): all {deck_size} cards are shuffled. Each player gets {hand_size} cards face down as a private hand, and {pool_size} cards go face down into the voting pool, in order; nobody sees the pool. Every player's suit tallies are reset to 0; tribes are kept.\n\nEach trick:\n1. The next voting-pool card is flipped face up. Its suit is the trump suit for this trick, and the card itself is the prize.\n2. Talk: every player writes one short message at the same time, without seeing the others. All three messages are then shown to everyone. Nothing said is binding.\n3. Play: every player secretly chooses one card from their hand, at the same moment. All three cards are revealed together and removed from the hands.\n4. Resolve: (a) If one or more trump-suit cards were played, the highest-ranked trump wins. Exception: if both the Six and the Five of trump were played, the Six wins. (b) If no trump was played, the highest-ranked card wins regardless of suit. (c) If no trump was played and two or more cards tie for highest rank (same rank, different suits), nobody wins the trick: each player captures their own played card, and the voting card is discarded with no one scoring it.\n5. Score: for each captured card, its points are added to the capturing player's tally for that card's suit. Normally the winner captures all 3 played cards plus the voting card.\n6. All played cards and every voting card flipped stay visible to everyone for the rest of the deal, along with all suit tallies.\n\nEnd of each deal (after tricks 6, 12, 18, 24): for each suit, the player whose tally in that suit is {tribe_threshold} or more wins that suit's tribe and adds {tribe_award} to their tribe count. A suit with no player at {tribe_threshold}+ awards no tribe. Everyone's tribe counts are announced.\n\nEnd of match: after trick {total_tricks} and its tribe scoring, the player with the most tribes wins. If two or more players tie for most tribes, the tied player with the highest sum of their three suit tallies in the 4th deal wins. If they are still tied, they share the win."
}
```
````
