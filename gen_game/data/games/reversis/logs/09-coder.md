# 09 coder

- time: 2026-10-28T03:10:53+00:00 (111.4s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 807b204e772796ad, reply sha256 b2fd4f26f5219c72

## Sent

````
# Task: write the XColos game file for "Short Reversis"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 4 to 4; set `meta.players` to {"min": 4, "max": 4, "suggested": 4} (the suggested size is the one the game plays best at).

DECK: 24 cards, A K Q J 9 8 in each of the four suits (spades, hearts, diamonds, clubs). Rank within a suit, high to low: A, K, Q, J, 9, 8. There are no trumps.

SEATS: Players 1 to 4 sit in a circle. Play goes from player 1 to 2 to 3 to 4 and back to 1. 'Left' means the next player in that order, 'right' the previous, and 'across' the player two seats away.

GAME STRUCTURE: The game is 4 hands. Each hand is 7 rounds: one passing round followed by 6 trick rounds. That makes 28 rounds in total.

PASSING ROUND (first round of each hand):
(1) The deck is shuffled and each player is dealt 6 cards, seen only by that player.
(2) In hands 1, 2 and 3, all players at the same moment each secretly choose 2 cards from their hand to pass. The passes go left in hand 1, right in hand 2 and across in hand 3. Passed cards are added to the receiver's hand after everyone has chosen, and only the passer and receiver know which cards moved. In hand 4 there is no pass.
(3) The game announces that passing is complete.

TRICK ROUNDS (6 per hand):
- Lead: In the first trick of hand h, player h leads (player 1 in hand 1, player 2 in hand 2, and so on). In every later trick, the winner of the previous trick leads.
- Playing: Starting with the leader and going around in seat order, each of the 4 players plays one card face up. The leader may play any card. Each other player must play a card of the led suit if they hold one. If they hold none, they may play any card.
- Winning: The highest card of the led suit wins the trick. Cards of other suits never win.
- Recording: The trick winner adds the trick's points to their score for this hand. Points per card: A=4, K=3, Q=2, J=1, with the Jack of Hearts (Quinola) worth 5. Nines and Eights are worth 0. The winner's trick count for the hand goes up by 1. All played cards are public.

END OF HAND (after the 6th trick):
- If one player won all 6 tricks (a reversis), that player scores 0 for the hand and each other player scores 15 for the hand.
- Otherwise each player scores the points they took. These always total 44 across the four players.
- Hand scores are added to running totals, which are public. Hand scores and trick counts reset to 0.

END OF GAME: After the 4th hand, the game ends.

How the winner is decided: After 4 hands, the player with the lowest running total wins. If two or more players tie for the lowest total, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Short Reversis (4 to 4 players, best with 4)

A 4-player trick-avoidance card game over 4 hands with a 24-card deck. Players pass cards, then try not to take points; whoever takes all 6 tricks in a hand (a reversis) scores 0 and every other player scores 15. The lowest total after 4 hands wins.

STATE (every item below must exist in the file):
  - each player: hand (list, starts []); only its owner sees it. Cards the player holds, coded rank+suit, e.g. 'AS', 'JH', '9D', '8C'
  - each player: pass_1 (text, starts ''); only its owner sees it. First card chosen to pass this hand
  - each player: pass_2 (text, starts ''); only its owner sees it. Second card chosen to pass this hand
  - each player: played_card (text, starts ''); everyone sees it. Card played face up to the current trick
  - each player: tricks_won (number, starts 0); everyone sees it. Tricks won in the current hand
  - each player: hand_points (number, starts 0); everyone sees it. Card points taken in the current hand
  - each player: hand_score (number, starts 0); everyone sees it. Score for the hand just finished, after the reversis rule
  - each player: total (number, starts 0); everyone sees it. Running total of hand scores; lower is better
  - the table: deck (list, starts ['AS', 'KS', 'QS', 'JS', '9S', '8S', 'AH', 'KH', 'QH', 'JH', '9H', '8H', 'AD', 'KD', 'QD', 'JD', '9D', '8D', 'AC', 'KC', 'QC', 'JC', '9C', '8C']); hidden from all players. Undealt cards of the 24-card deck
  - the table: hand_number (number, starts 0); everyone sees it. Current hand, 1 to 4
  - the table: trick_number (number, starts 0); everyone sees it. Tricks completed in the current hand, 0 to 6
  - the table: leader (number, starts 1); everyone sees it. Seat that leads the current trick
  - the table: led_suit (text, starts ''); everyone sees it. Suit of the card led to the current trick (S, H, D or C)
  - the table: trick_winner (number, starts 0); everyone sees it. Seat that won the last trick
  - the table: played_cards (list, starts []); everyone sees it. All cards played face up so far in this hand
  - parameters, each kept as a table attribute: num_players = 4, deck_size = 24, num_hands = 4, cards_dealt_per_player = 6, pass_count = 2, last_passing_hand = 3, tricks_per_hand = 6, rounds_per_hand = 7, total_rounds = 28, points_ace = 4, points_king = 3, points_queen = 2, points_jack = 1, points_quinola_jack_of_hearts = 5, points_nine = 0, points_eight = 0, points_total_per_hand = 44, reversis_tricks = 6, reversis_taker_score = 0, reversis_other_score = 15, rank_value_ace = 6, rank_value_king = 5, rank_value_queen = 4, rank_value_jack = 3, rank_value_nine = 2, rank_value_eight = 1

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seats 1 to 4 sit in a circle; play order is 1, 2, 3, 4, then back to 1.
  2. Every player's total starts at 0 and hand_number starts at 0.
  3. No cards are dealt yet; the deal happens at the start of each hand.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: One round of the script is one hand. hand_number += 1. deck is reset to all 24 cards. Every hand, played_cards, pass_1, pass_2 and played_card is cleared. Each player draws 6 cards at random from deck into their hand (24 draws in all, emptying the deck). trick_number = 0. leader = hand_number.
  2. [sync] all players. What happens: Each player privately sees their own hand of 6 cards.
  3. [poll] all players answers: one card from your own hand. What happens: when hand_number <= 3: pass_1 = the chosen card. Nobody sees any choice until all are in.
  4. [poll] all players answers: one card from your own hand other than pass_1. What happens: when hand_number <= 3: pass_2 = the chosen card.
  5. [update] all players. What happens: when hand_number <= 3: each player's pass_1 and pass_2 are removed from their hand and appended to the receiver's hand. The receiver is seat (seat mod 4)+1 (left) in hand 1, seat ((seat+2) mod 4)+1 (right) in hand 2, and seat ((seat+1) mod 4)+1 (across) in hand 3. Each passer and receiver is told privately which two cards moved. Every hand again holds 6 cards.
  6. [tell] all players. What happens: Announce: 'Passing is complete.' In hand 4 the announcement says there was no pass.
  7. [repeat] all players. What happens: Run the next 6 steps (one trick) until trick_number = 6.
  8. [ask] seat leader answers: any card from your hand. What happens: played_card = the chosen card; led_suit = its suit; the card is removed from hand and appended to played_cards; the play is announced to everyone.
  9. [ask] seat (leader mod 4)+1 answers: a card of led_suit from your hand if you hold one, otherwise any card from your hand. What happens: played_card = the chosen card; removed from hand and appended to played_cards; announced to everyone.
  10. [ask] seat ((leader+1) mod 4)+1 answers: a card of led_suit from your hand if you hold one, otherwise any card from your hand. What happens: played_card = the chosen card; removed from hand and appended to played_cards; announced to everyone.
  11. [ask] seat ((leader+2) mod 4)+1 answers: a card of led_suit from your hand if you hold one, otherwise any card from your hand. What happens: played_card = the chosen card; removed from hand and appended to played_cards; announced to everyone.
  12. [update] all players. What happens: trick_winner = the seat whose played_card has suit led_suit and the highest rank value (A=6, K=5, Q=4, J=3, 9=2, 8=1). That seat's hand_points += the sum of the points of the 4 played cards (A=4, K=3, Q=2, J=1 except JH=5, 9=0, 8=0). That seat's tricks_won += 1. leader = trick_winner. trick_number += 1.
  13. [tell] all players. What happens: Announce: 'Seat {trick_winner} wins trick {trick_number} and takes {points} points.' with each player's hand_points and tricks_won.
  14. [update] all players. What happens: End of hand. If some player has tricks_won = 6, that player's hand_score = 0 and every other player's hand_score = 15. Otherwise each player's hand_score = hand_points. Each player's total += hand_score. Then hand_points = 0 and tricks_won = 0 for every player.
  15. [tell] all players. What happens: Announce each player's hand_score and running total, and whether a reversis happened.
  16. [check] all players. What happens: If hand_number = 4, end the game; otherwise start the next hand.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When a hand starts, then the deck holds 24 cards (A, K, Q, J, 9, 8 of spades, hearts, diamonds and clubs) and each player is dealt 6 cards at random into their hand, seen only by that player.
  R2. When it is hand 1, 2 or 3, then all players simultaneously choose 2 different cards from their hand to pass, and no one sees another's choice before all have chosen.
  R3. When it is hand 1, then each seat s passes its 2 cards to seat (s mod 4)+1 (left), so seat 4 passes to seat 1.
  R4. When it is hand 2, then each seat s passes its 2 cards to the previous seat (right), so seat 1 passes to seat 4.
  R5. When it is hand 3, then each seat s passes its 2 cards to the seat two away (across): 1 with 3, and 2 with 4.
  R6. When cards are passed, then they leave the passer's hand and join the receiver's hand only after everyone has chosen, every hand still holds 6 cards, and only the passer and the receiver learn which cards moved.
  R7. When it is hand 4, then no cards are passed.
  R8. When passing is over, then the game announces that passing is complete.
  R9. When the first trick of hand h starts, then seat h leads (seat 1 in hand 1, seat 4 in hand 4).
  R10. When any later trick starts, then the winner of the previous trick leads.
  R11. When a trick is played, then the leader plays first and the other 3 players follow one at a time in seat order, each playing one card face up.
  R12. When the leader plays, then they may play any card in their hand.
  R13. When a non-leader holds a card of the led suit, then they must play a card of that suit.
  R14. When a non-leader holds no card of the led suit, then they may play any card in their hand.
  R15. When all 4 cards are played, then the highest card of the led suit wins the trick (A > K > Q > J > 9 > 8), there are no trumps, and a card of another suit never wins.
  R16. When a player wins a trick, then their hand points rise by the trick's card points (A=4, K=3, Q=2, J=1, Jack of Hearts=5, 9=0, 8=0) and their trick count for the hand rises by 1.
  R17. When a hand ends with no player winning all 6 tricks, then each player's hand score equals the card points they took, and the four scores total 44.
  R18. When a hand ends with one player winning all 6 tricks (a reversis), then that player scores 0 for the hand and each other player scores 15.
  R19. When a hand ends, then each hand score is added to that player's public running total, and hand points and trick counts reset to 0.
  R20. When the 4th hand has been scored, then the game ends.
  R21. When the game ends, then the player with the lowest running total wins, and players tied for the lowest total share the result (a draw).

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - First card to pass (hands 1 to 3) | asked: all players at once | options: every card in the player's own hand
  - Second card to pass (hands 1 to 3) | asked: all players at once | options: every card in the player's own hand except the one already chosen as pass_1
  - Lead a card | asked: seat leader | options: every card in the leader's hand
  - Follow to the trick | asked: each of the 3 seats after the leader, in seat order | options: a seat holding at least one card of led_suit: only its cards of led_suit; a seat holding no card of led_suit: every card in its hand

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: hand_number = 4 after the end-of-hand scoring
  - each player's standing: 0 - you.total (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their running total after 4 hands, and lower is better. The player with the lowest total wins; players tied for the lowest total share the result (the source calls this a draw).
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

- each player: `tricks_won` (number, visible: public, starts 0): Tricks won in the current hand
- each player: `hand_points` (number, visible: public, starts 0): Card points taken in the current hand
- each player: `total` (number, visible: public, starts 0): Running total of hand scores; lower is better
- the table: `hand_number` (number, visible: public, starts 0): Current hand, 1 to 4
- parameters (each must be an attribute holding this value, never a number buried in a step): num_players = 4, deck_size = 24, num_hands = 4, cards_dealt_per_player = 6, pass_count = 2, last_passing_hand = 3, tricks_per_hand = 6, rounds_per_hand = 7, total_rounds = 28, points_ace = 4, points_king = 3, points_queen = 2, points_jack = 1, points_quinola_jack_of_hearts = 5, points_nine = 0, points_eight = 0, points_total_per_hand = 44, reversis_tricks = 6, reversis_taker_score = 0, reversis_other_score = 15, rank_value_ace = 6, rank_value_king = 5, rank_value_queen = 4, rank_value_jack = 3, rank_value_nine = 2, rank_value_eight = 1
- the game ends with ONE ending whose `rank_by` is `0 - you.total`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
    "id": "short_reversis",
    "name": "Short Reversis",
    "players": {
      "min": 4,
      "max": 4,
      "suggested": 4
    },
    "blurb": "Four hands of trick avoidance with a 24-card deck: pass, dodge points, or take every trick for a reversis. The lowest total wins."
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
        "key": "pass_1",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "pass_2",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "received",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "offer",
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
        "key": "tricks_won",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hand_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hand_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "total",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ],
    "game": [
      {
        "key": "all_cards",
        "visible": "none",
        "type": "list",
        "initial": ["AS", "KS", "QS", "JS", "9S", "8S", "AH", "KH", "QH", "JH", "9H", "8H", "AD", "KD", "QD", "JD", "9D", "8D", "AC", "KC", "QC", "JC", "9C", "8C"]
      },
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": ["AS", "KS", "QS", "JS", "9S", "8S", "AH", "KH", "QH", "JH", "9H", "8H", "AD", "KD", "QD", "JD", "9D", "8D", "AC", "KC", "QC", "JC", "9C", "8C"]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "stage",
        "visible": "none",
        "type": "text",
        "initial": "pass"
      },
      {
        "key": "hand_number",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "trick_number",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "leader",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "led_suit",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "trick_winner",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "trick_points",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "reversis_seat",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "played_cards",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "num_players",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 24
      },
      {
        "key": "num_hands",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "cards_dealt_per_player",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "pass_count",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "last_passing_hand",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "tricks_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "rounds_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "total_rounds",
        "visible": "public",
        "type": "number",
        "initial": 28
      },
      {
        "key": "points_ace",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "points_king",
        "visible": "public",
        "type": "number",
        "initial": 3
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
        "key": "points_quinola_jack_of_hearts",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "points_nine",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "points_eight",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "points_total_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 44
      },
      {
        "key": "reversis_tricks",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "reversis_taker_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "reversis_other_score",
        "visible": "public",
        "type": "number",
        "initial": 15
      },
      {
        "key": "rank_value_ace",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "rank_value_king",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "rank_value_queen",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "rank_value_jack",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "rank_value_nine",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "rank_value_eight",
        "visible": "public",
        "type": "number",
        "initial": 1
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
            "key": "total",
            "value": 0
          }
        },
        {
          "set": {
            "key": "hand_number",
            "value": 0
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
            "key": "stage",
            "value": "pass"
          }
        }
      ],
      "text": "Seats 1 to 4 sit in a circle; play goes 1, 2, 3, 4 and back to 1. Every total starts at 0. Cards are dealt at the start of each hand."
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "deal",
      "label": "new hand and deal",
      "when": {
        "calc": "stage == 'pass'"
      },
      "do": [
        {
          "adjust": {
            "key": "hand_number",
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
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "[]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "pass_1",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "pass_2",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "received",
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
        },
        {
          "set": {
            "key": "played_cards",
            "value": {
              "calc": "[]"
            }
          }
        },
        {
          "set": {
            "key": "trick_number",
            "value": 0
          }
        },
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "hand_number"
            }
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
            "key": "reversis_seat",
            "value": 0
          }
        },
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}}
      ],
      "text": "Hand {hand_number} of {num_hands} begins. The deck is shuffled and each player is dealt 6 cards. Seat {leader} will lead the first trick."
    },
    {
      "use": "sync",
      "phase": "deal",
      "label": "your hand",
      "when": {
        "calc": "stage == 'pass'"
      },
      "mode": "self",
      "to": "all",
      "fields": [
        "hand"
      ],
      "text": "Your hand:"
    },
    {
      "use": "poll",
      "phase": "pass",
      "label": "first card to pass",
      "when": {
        "calc": "stage == 'pass' and hand_number <= last_passing_hand"
      },
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "store": "pass_1",
      "text": "Hand {hand_number}: choose the FIRST of the 2 cards you will pass (left in hand 1, right in hand 2, across in hand 3). Nobody sees your choice."
    },
    {
      "use": "update",
      "phase": "pass",
      "label": "offer the second pass",
      "when": {
        "calc": "stage == 'pass' and hand_number <= last_passing_hand"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "[c for c in you.hand if c != you.pass_1]"
            }
          }
        }
      ]
    },
    {
      "use": "poll",
      "phase": "pass",
      "label": "second card to pass",
      "when": {
        "calc": "stage == 'pass' and hand_number <= last_passing_hand"
      },
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "store": "pass_2",
      "text": "Choose the SECOND card you will pass. Nobody sees your choice."
    },
    {
      "use": "update",
      "phase": "pass",
      "label": "the cards move",
      "when": {
        "calc": "stage == 'pass' and hand_number <= last_passing_hand"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "received",
            "value": {
              "calc": "[players[(you.seat - 1 - [1, 3, 2][hand_number - 1] + num_players) % num_players].pass_1, players[(you.seat - 1 - [1, 3, 2][hand_number - 1] + num_players) % num_players].pass_2]"
            }
          }
        },
        {
          "remove": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "you.pass_1"
            }
          }
        },
        {
          "remove": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "you.pass_2"
            }
          }
        },
        {
          "append": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "you.received[0]"
            }
          }
        },
        {
          "append": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "you.received[1]"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "pass",
      "label": "passing complete",
      "when": {
        "calc": "stage == 'pass' and hand_number <= last_passing_hand"
      },
      "to": "all",
      "text": "Passing is complete. You passed {pass_1} and {pass_2}, and received {received}. Your hand is now {hand}."
    },
    {
      "use": "tell",
      "phase": "pass",
      "label": "no pass",
      "when": {
        "calc": "stage == 'pass' and hand_number > last_passing_hand"
      },
      "to": "all",
      "text": "Passing is complete: there was no pass in hand {hand_number}. Your hand is {hand}."
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "lead",
      "when": {
        "calc": "stage == 'trick'"
      },
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
        "bind": "lead_card"
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} leads {value}."
      },
      "text": "You lead this trick. Play any card from your hand."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "the lead is placed",
      "when": {
        "calc": "stage == 'trick'"
      },
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
            "player": {
              "calc": "leader"
            },
            "key": "played_card",
            "value": "$lead_card"
          }
        },
        {
          "set": {
            "key": "led_suit",
            "value": {
              "calc": "players[leader - 1].played_card[-1]"
            }
          }
        },
        {
          "remove": {
            "player": {
              "calc": "leader"
            },
            "key": "hand",
            "value": "$lead_card"
          }
        },
        {
          "append": {
            "key": "played_cards",
            "value": "$lead_card"
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "[c for c in you.hand if c[-1] == led_suit] if any(c[-1] == led_suit for c in you.hand) else you.hand"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "second to play",
      "when": {
        "calc": "stage == 'trick'"
      },
      "to": {
        "where": "you.seat == (leader % num_players) + 1"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "f2"
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} plays {value}."
      },
      "text": "Led suit is {led_suit}. Play a card: you must follow suit if you can; if you cannot, any card is allowed."
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "third to play",
      "when": {
        "calc": "stage == 'trick'"
      },
      "to": {
        "where": "you.seat == ((leader + 1) % num_players) + 1"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "f3"
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} plays {value}."
      },
      "text": "Led suit is {led_suit}. Play a card: you must follow suit if you can; if you cannot, any card is allowed."
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "fourth to play",
      "when": {
        "calc": "stage == 'trick'"
      },
      "to": {
        "where": "you.seat == ((leader + 2) % num_players) + 1"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "f4"
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} plays {value}."
      },
      "text": "Led suit is {led_suit}. Play a card: you must follow suit if you can; if you cannot, any card is allowed."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "the trick is won",
      "when": {
        "calc": "stage == 'trick'"
      },
      "do": [
        {
          "set": {
            "player": {
              "calc": "(leader % num_players) + 1"
            },
            "key": "played_card",
            "value": "$f2"
          }
        },
        {
          "remove": {
            "player": {
              "calc": "(leader % num_players) + 1"
            },
            "key": "hand",
            "value": "$f2"
          }
        },
        {
          "append": {
            "key": "played_cards",
            "value": "$f2"
          }
        },
        {
          "set": {
            "player": {
              "calc": "((leader + 1) % num_players) + 1"
            },
            "key": "played_card",
            "value": "$f3"
          }
        },
        {
          "remove": {
            "player": {
              "calc": "((leader + 1) % num_players) + 1"
            },
            "key": "hand",
            "value": "$f3"
          }
        },
        {
          "append": {
            "key": "played_cards",
            "value": "$f3"
          }
        },
        {
          "set": {
            "player": {
              "calc": "((leader + 2) % num_players) + 1"
            },
            "
... (cut)

Why it was refused: it plays, but part of it does nothing: game attribute `all_cards` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `reversis_seat` is never changed in 3 random matches, so nothing updates it. Steps that name it: new hand and deal, end of hand. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "short_reversis",
    "name": "Short Reversis",
    "players": {
      "min": 4,
      "max": 4,
      "suggested": 4
    },
    "blurb": "Four hands of trick avoidance with a 24-card deck: pass cards, dodge points, or take every trick for a reversis. The lowest total wins."
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
        "key": "pass_1",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "pass_2",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "received",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "offer",
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
        "key": "tricks_won",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hand_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hand_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "total",
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
        "initial": ["AS", "KS", "QS", "JS", "9S", "8S", "AH", "KH", "QH", "JH", "9H", "8H", "AD", "KD", "QD", "JD", "9D", "8D", "AC", "KC", "QC", "JC", "9C", "8C"]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "hand_number",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "trick_number",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "leader",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "led_suit",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "trick_winner",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "trick_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "played_cards",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "num_players",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 24
      },
      {
        "key": "num_hands",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "cards_dealt_per_player",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "pass_count",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "last_passing_hand",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "tricks_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "rounds_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "total_rounds",
        "visible": "public",
        "type": "number",
        "initial": 28
      },
      {
        "key": "points_ace",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "points_king",
        "visible": "public",
        "type": "number",
        "initial": 3
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
        "key": "points_quinola_jack_of_hearts",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "points_nine",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "points_eight",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "points_total_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 44
      },
      {
        "key": "reversis_tricks",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "reversis_taker_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "reversis_other_score",
        "visible": "public",
        "type": "number",
        "initial": 15
      },
      {
        "key": "rank_value_ace",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "rank_value_king",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "rank_value_queen",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "rank_value_jack",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "rank_value_nine",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "rank_value_eight",
        "visible": "public",
        "type": "number",
        "initial": 1
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
            "key": "total",
            "value": 0
          }
        },
        {
          "set": {
            "key": "hand_number",
            "value": 0
          }
        }
      ],
      "text": "Seats 1 to 4 sit in a circle; play goes 1, 2, 3, 4 and back to 1. Every total starts at 0. Cards are dealt at the start of each hand."
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "deal",
      "label": "new hand and deal",
      "do": [
        {
          "adjust": {
            "key": "hand_number",
            "value": 1
          }
        },
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "deck + played_cards"
            }
          }
        },
        {
          "set": {
            "key": "played_cards",
            "value": {
              "calc": "[]"
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
            "players": "all",
            "key": "pass_1",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "pass_2",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "received",
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
        },
        {
          "set": {
            "key": "trick_number",
            "value": 0
          }
        },
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "hand_number"
            }
          }
        },
        {
          "set": {
            "key": "led_suit",
            "value": ""
          }
        },
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}}
      ],
      "text": "Hand {hand_number} of {num_hands} begins. The deck is shuffled and each player is dealt {cards_dealt_per_player} cards. Seat {leader} will lead the first trick."
    },
    {
      "use": "sync",
      "phase": "deal",
      "label": "your hand",
      "mode": "self",
      "to": "all",
      "fields": [
        "hand"
      ],
      "text": "Your hand:"
    },
    {
      "use": "poll",
      "phase": "pass",
      "label": "first card to pass",
      "when": {
        "calc": "hand_number <= last_passing_hand"
      },
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "store": "pass_1",
      "text": "Hand {hand_number}: choose the FIRST of the 2 cards you will pass (left in hand 1, right in hand 2, across in hand 3). Nobody sees your choice until all have chosen."
    },
    {
      "use": "update",
      "phase": "pass",
      "label": "offer the second pass",
      "when": {
        "calc": "hand_number <= last_passing_hand"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "[c for c in you.hand if c != you.pass_1]"
            }
          }
        }
      ]
    },
    {
      "use": "poll",
      "phase": "pass",
      "label": "second card to pass",
      "when": {
        "calc": "hand_number <= last_passing_hand"
      },
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "store": "pass_2",
      "text": "Choose the SECOND card you will pass. Nobody sees your choice until all have chosen."
    },
    {
      "use": "update",
      "phase": "pass",
      "label": "the cards move",
      "when": {
        "calc": "hand_number <= last_passing_hand"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "received",
            "value": {
              "calc": "[players[(you.seat - 1 - [1, 3, 2][hand_number - 1] + num_players) % num_players].pass_1, players[(you.seat - 1 - [1, 3, 2][hand_number - 1] + num_players) % num_players].pass_2]"
            }
          }
        },
        {
          "remove": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "you.pass_1"
            }
          }
        },
        {
          "remove": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "you.pass_2"
            }
          }
        },
        {
          "append": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "you.received[0]"
            }
          }
        },
        {
          "append": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "you.received[1]"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "pass",
      "label": "passing complete",
      "when": {
        "calc": "hand_number <= last_passing_hand"
      },
      "to": "all",
      "text": "Passing is complete. You passed {pass_1} and {pass_2}, and received {received}. Your hand is now {hand}."
    },
    {
      "use": "tell",
      "phase": "pass",
      "label": "no pass",
      "when": {
        "calc": "hand_number > last_passing_hand"
      },
      "to": "all",
      "text": "Passing is complete: there was no pass in hand {hand_number}. Your hand is {hand}."
    },
    {
      "use": "repeat",
      "label": "the tricks",
      "until": {
        "calc": "trick_number >= tricks_per_hand"
      },
      "max": 10,
      "steps": [
        {
          "use": "ask",
          "phase": "trick",
          "label": "lead",
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
            "bind": "lead_card"
          },
          "broadcast": {
            "to": "all",
            "text": "Seat {seat} leads {value}."
          },
          "text": "You lead this trick. Play any card from your hand."
        },
        {
          "use": "update",
          "phase": "trick",
          "label": "the lead is placed",
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
                "player": {
                  "calc": "leader"
                },
                "key": "played_card",
                "value": "$lead_card"
              }
            },
            {
              "set": {
                "key": "led_suit",
                "value": {
                  "calc": "$lead_card[-1]"
                }
              }
            },
            {
              "remove": {
                "player": {
                  "calc": "leader"
                },
                "key": "hand",
                "value": "$lead_card"
              }
            },
            {
              "append": {
                "key": "played_cards",
                "value": "$lead_card"
              }
            },
            {
              "set": {
                "players": "all",
                "key": "offer",
                "value": {
                  "calc": "[c for c in you.hand if c[-1] == led_suit] if any(c[-1] == led_suit for c in you.hand) else you.hand"
                }
              }
            }
          ]
        },
        {
          "use": "ask",
          "phase": "trick",
          "label": "second to play",
          "to": {
            "where": "you.seat == (leader % num_players) + 1"
          },
          "answer": {
            "type": "choice",
            "options": {
              "attribute": "offer"
            }
          },
          "verify": {
            "bind": "f2"
          },
          "broadcast": {
            "to": "all",
            "text": "Seat {seat} plays {value}."
          },
          "text": "Led suit is {led_suit}. Play a card: you must follow suit if you can; if you cannot, any card is allowed."
        },
        {
          "use": "ask",
          "phase": "trick",
          "label": "third to play",
          "to": {
            "where": "you.seat == ((leader + 1) % num_players) + 1"
          },
          "answer": {
            "type": "choice",
            "options": {
              "attribute": "offer"
            }
          },
          "verify": {
            "bind": "f3"
          },
          "broadcast": {
            "to": "all",
            "text": "Seat {seat} plays {value}."
          },
          "text": "Led suit is {led_suit}. Play a card: you must follow suit if you can; if you cannot, any card is allowed."
        },
        {
          "use": "ask",
          "phase": "trick",
          "label": "fourth to play",
          "to": {
            "where": "you.seat == ((leader + 2) % num_players) + 1"
          },
          "answer": {
            "type": "choice",
            "options": {
              "attribute": "offer"
            }
          },
          "verify": {
            "bind": "f4"
          },
          "broadcast": {
            "to": "all",
            "text": "Seat {seat} plays {value}."
          },
          "text": "Led suit is {led_suit}. Play a card: you must follow suit if you can; if you cannot, any card is allowed."
        },
        {
          "use": "update",
          "phase": "trick",
          "label": "the trick is won",
          "do": [
            {
              "set": {
                "player": {
                  "calc": "(leader % num_players) + 1"
                },
                "key": "played_card",
                "value": "$f2"
              }
            },
            {
              "remove": {
                "player": {
                  "calc": "(leader % num_players) + 1"
                },
                "key": "hand",
                "value": "$f2"
              }
            },
            {
              "append": {
                "key": "played_cards",
                "value": "$f2"
              }
            },
            {
              "set": {
                "player": {
                  "calc": "((leader + 1) % num_players) + 1"
                },
                "key": "played_card",
                "value": "$f3"
              }
            },
            {
              "remove": {
                "player": {
                  "calc": "((leader + 1) % num_players) + 1"
                },
                "key": "hand",
                "value": "$f3"
              }
            },
            {
              "append": {
                "key": "played_cards",
                "value": "$f3"
              }
            },
            {
              "set": {
                "player": {
                  "calc": "((leader + 2) % num_players) + 1"
                },
                "key": "played_card",
                "value": "$f4"
              }
            },
            {
              "remove": {
                "player": {
                  "calc": "((leader + 2) % num_players) + 1"
                },
                "key": "hand",
                "value": "$f4"
              }
            },
            {
              "append": {
                "key": "played_cards",
                "value": "$f4"
              }
            },
            {
              "set": {
                "key": "trick_points",
                "value": {
                  "calc": "sum([(points_quinola_jack_of_hearts if c == 'JH' else points_ace if c[0] == 'A' else points_king if c[0] == 'K' else points_queen if c[0] == 'Q' else points_jack if c[0] == 'J' else points_nine if c[0] == '9' else points_eight) for c in [$lead_card, $f2, $f3, $f4]])"
                }
              }
            },
            {
              "set": {
                "key": "trick_winner",
                "value": {
                  "calc": "sorted([[(rank_value_ace if x[0][0] == 'A' else rank_value_king if x[0][0] == 'K' else rank_value_queen if x[0][0] == 'Q' else rank_value_jack if x[0][0] == 'J' else rank_value_nine if x[0][0] == '9' else rank_value_eight), x[1]] for x in [[$lead_card, leader], [$f2, (leader % num_players) + 1], [$f3, ((leader + 1) % num_players) + 1], [$f4, ((leader + 2) % num_players) + 1]] if x[0][-1] == led_suit])[-1][1]"
                }
              }
            },
            {
              "adjust": {
                "player": {
                  "calc": "trick_winner"
                },
                "key": "hand_points",
                "value": {
                  "calc": "trick_points"
                }
              }
            },
            {
              "adjust": {
                "player": {
                  "calc": "trick_winner"
                },
                "key": "tricks_won",
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
                "key": "trick_number",
                "value": 1
              }
            }
          ]
        },
        {
          "use": "tell",
          "phase": "trick",
          "label": "trick result",
          "to": "all",
          "text": "Seat {trick_winner} wins trick {trick_number} and takes {trick_points} points. Hand points: Seat 1 {players[0].hand_points}, Seat 2 {players[1].hand_points}, Seat 3 {players[2].hand_points}, Seat 4 {players[3].hand_points}. Tricks: Seat 1 {players[0].tricks_won}, Seat 2 {players[1].tricks_won}, Seat 3 {players[2].tricks_won}, Seat 4 {players[3].tricks_won}."
        }
      ]
    },
    {
      "use": "update",
      "phase": "score",
      "label": "end of hand",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "hand_score",
            "value": {
              "calc": "reversis_taker_score if you.tricks_won == reversis_tricks else (reversis_other_score if any(p.tricks_won == reversis_tricks for p in players) else you.hand_points)"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "total",
            "value": {
              "calc": "you.hand_score"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_points",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "tricks_won",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "score",
      "label": "hand scored",
      "when": {
        "calc": "sum([p.hand_score for p in players]) == points_total_per_hand"
      },
      "to": "all",
      "text": "Hand {hand_number} is over, no reversis. Hand scores: Seat 1 {players[0].hand_score}, Seat 2 {players[1].hand_score}, Seat 3 {players[2].hand_score}, Seat 4 {players[3].hand_score}. Totals: Seat 1 {players[0].total}, Seat 2 {players[1].total}, Seat 3 {players[2].total}, Seat 4 {players[3].total}."
    },
    {
      "use": "tell",
      "phase": "score",
      "label": "reversis scored",
      "when": {
        "calc": "sum([p.hand_score for p in players]) != points_total_per_hand"
      },
      "to": "all",
      "text": "Hand {hand_number} is over: a REVERSIS! One player took all {reversis_tricks} tricks and scores {reversis_taker_score}; everyone else scores {reversis_other_score}. Hand scores: Seat 1 {players[0].hand_score}, Seat 2 {players[1].hand_score}, Seat 3 {players[2].hand_score}, Seat 4 {players[3].hand_score}. Totals: Seat 1 {players[0].total}, Seat 2 {players[1].total}, Seat 3 {players[2].total}, Seat 4 {players[3].total}."
    },
    {
      "use": "check",
      "phase": "score",
      "label": "after the last hand",
      "when": {
        "calc": "hand_number >= num_hands"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "hand_number >= num_hands"
      },
      "rank_by": "0 - you.total",
      "text": "Winner (lowest total): {result}. Final totals: Seat 1 {players[0].total}, Seat 2 {players[1].total}, Seat 3 {players[2].total}, Seat 4 {players[3].total}."
    }
  },
  "limits": {
    "rounds": 4,
    "rounds_max": 6,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "DECK: {deck_size} cards, A K Q J 9 8 in each of the four suits (spades S, hearts H, diamonds D, clubs C). Cards are written rank+suit, e.g. AS, JH, 9D, 8C. Rank within a suit, high to low: A, K, Q, J, 9, 8. There are no trumps.\n\nSEATS: Players 1 to 4 sit in a circle. Play goes from 1 to 2 to 3 to 4 and back to 1. Left means the next player, right the previous, across the player two seats away.\n\nThe game is {num_hands} hands. Each hand is one passing round followed by {tricks_per_hand} tricks.\n\nPASSING: The deck is shuffled and each player is dealt {cards_dealt_per_player} cards, seen only by that player. In hands 1 to {last_passing_hand}, all players at the same moment secretly choose {pass_count} different cards from their hand to pass: left in hand 1, right in hand 2, across in hand 3. Passed cards join the receiver's hand only after everyone has chosen, and only the passer and receiver know which cards moved. In hand 4 there is no pass. The game then announces that passing is complete.\n\nTRICKS: In the first trick of hand h, seat h leads. In every later trick, the winner of the previous trick leads. Starting with the leader and going around in seat order, each player plays one card face up. The leader may play any card. Each other player must play a card of the led suit if they hold one; if they hold none, they may play any card. The highest card of the led suit wins the trick; cards of other suits never win. The winner adds the trick's points to their hand points: A={points_ace}, K={points_king}, Q={points_queen}, J={points_jack}, the Jack of Hearts (Quinola)={points_quinola_jack_of_hearts}, 9={points_nine}, 8={points_eight}. Their trick count goes up by 1. All played cards are public.\n\nEND OF HAND: If one player won all {reversis_tricks} tricks (a reversis), that player scores {reversis_taker_score} for the hand and each other player scores {reversis_other_score}. Otherwise each player scores the points they took (these total {points_total_per_hand}). Hand scores are added to public running totals; hand points and trick counts reset to 0.\n\nEND OF GAME: After the 4th hand the game ends. The player with the lowest running total wins; players tied for the lowest total share the result (a draw)."
}
```
````
