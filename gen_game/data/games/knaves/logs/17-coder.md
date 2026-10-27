# 17 coder

- time: 2026-10-27T18:24:27+00:00 (87.0s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 2a7755400590f68d, reply sha256 e7a23a2063c9a130

## Sent

````
# Task: write the XColos game file for "Knaves' Wager"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

PLAYERS AND DECK. 3 players sit in a fixed order. The deck has 20 cards: A, K, Q, J, 10 in each of spades, clubs, diamonds and hearts. Within a suit, cards rank A (high), K, Q, J, 10 (low).

HANDS AND ROUNDS. The game is 6 hands of 6 tricks each, 36 rounds in all. Each round is one trick. The dealer for hand 1 is player 1. The dealer moves one seat to the left each hand, so each player deals twice. The player to the dealer's left is eldest for that hand.

DEAL (first round of each hand). Shuffle all 20 cards. Deal 6 cards privately to each player; a hand is seen only by its owner. Turn the 19th card face up: its suit is trump for this hand, and the card itself is out of play. The 20th card stays face down and out of play, and is never revealed during the hand.

BID (first round of each hand, after the deal). All players at the same moment secretly choose a whole number from 0 to 6: the number of tricks they predict they will take this hand. All three bids are then revealed to everyone.

TRICK PLAY (every round). The leader plays any card from their hand face up. The eldest leads the first trick of a hand; afterwards, the winner of the previous trick leads. Then the next player to the left plays, then the third. Each must play a card of the led suit if they have one. If they have none, they may play any card, including a trump. The trick is won by the highest trump in it. If it holds no trump, the highest card of the led suit wins. All plays are visible to everyone as they are made.

TRICK SCORING. The trick winner adds 2 to their hand score. They also take penalties for any Jacks in the trick: Jack of spades -1, Jack of clubs -2, Jack of diamonds -3, Jack of hearts -4. The trick's cards, its winner and the running trick counts are announced.

END OF HAND (after the 6th trick). Any player whose tricks taken equal their bid adds 4 to their hand score. Each player's hand score (2 per trick, minus Jack penalties, plus any bid bonus) is added to their total and announced. Hand scores reset to 0, and the dealer rotates.

END OF GAME. After the 6th hand (round 36), the game ends.

How the winner is decided: After 6 hands, the player with the highest total wins. If two or three players tie for the highest total, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Knaves' Wager (3 to 3 players, best with 3)

A 3-player trick-taking game over 6 hands of 6 tricks: bid your trick count secretly, take tricks for 2 points each, avoid winning Jacks, and score a 4-point bonus for an exact bid.

STATE (every item below must exist in the file):
  - each player: hand (list, starts []); only its owner sees it. The cards this player holds, as codes such as 'AS' or '10H'. Only the owner sees it.
  - each player: bid (number, starts 0); everyone sees it. The tricks this player predicted for the current hand, from 0 to 6. Revealed after all players have bid.
  - each player: tricks_taken (number, starts 0); everyone sees it. Tricks this player has won in the current hand.
  - each player: hand_score (number, starts 0); everyone sees it. Points this player has earned in the current hand: 2 per trick, minus Jack penalties, plus any bid bonus.
  - each player: total (number, starts 0); everyone sees it. This player's running game total, which is the score.
  - each player: played_card (text, starts ''); everyone sees it. The card this player played to the current trick.
  - the table: deck (list, starts ['AS', 'KS', 'QS', 'JS', '10S', 'AC', 'KC', 'QC', 'JC', '10C', 'AD', 'KD', 'QD', 'JD', '10D', 'AH', 'KH', 'QH', 'JH', '10H']); hidden from all players. The undealt cards. At the start of each hand all 20 cards are gathered here and shuffled.
  - the table: turned_card (text, starts ''); everyone sees it. The 19th card, turned face up. It sets trump and is out of play.
  - the table: hidden_card (text, starts ''); hidden from all players. The 20th card. It stays face down, is out of play, and is never revealed during the hand.
  - the table: trump_suit (text, starts ''); everyone sees it. The suit of turned_card: S, C, D or H.
  - the table: hand_number (number, starts 1); everyone sees it. The current hand, from 1 to 6.
  - the table: trick_in_hand (number, starts 1); everyone sees it. The current trick within the hand, from 1 to 6.
  - the table: round_number (number, starts 1); everyone sees it. The current round, from 1 to 36. One round is one trick.
  - the table: dealer (number, starts 1); everyone sees it. The dealer's seat for this hand.
  - the table: eldest (number, starts 2); everyone sees it. The seat to the dealer's left, which leads the first trick of the hand.
  - the table: leader (number, starts 2); everyone sees it. The seat that leads the current trick.
  - the table: led_suit (text, starts ''); everyone sees it. The suit of the card led to the current trick.
  - the table: trick_winner (number, starts 0); everyone sees it. The seat that won the last trick.
  - parameters, each kept as a table attribute: player_count = 3, deck_size = 20, suits = 4, ranks_per_suit = 5, hands = 6, tricks_per_hand = 6, total_rounds = 36, cards_dealt_per_player = 6, trump_card_position = 19, hidden_card_position = 20, bid_min = 0, bid_max = 6, trick_points = 2, jack_of_spades_penalty = 1, jack_of_clubs_penalty = 2, jack_of_diamonds_penalty = 3, jack_of_hearts_penalty = 4, exact_bid_bonus = 4, deals_per_player = 2, first_dealer_seat = 1, rank_value_A = 14, rank_value_K = 13, rank_value_Q = 12, rank_value_J = 11, rank_value_10 = 10

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seats 1, 2 and 3 sit in a fixed order; the seat to a player's left is the next seat number, and seat 1 follows seat 3.
  2. Set every player's total to 0.
  3. Set hand_number to 1, round_number to 1 and trick_in_hand to 1.
  4. Set dealer to 1 and eldest to 2.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: When trick_in_hand = 1: gather all 20 cards into deck and empty every hand. Deal 6 cards to each player by drawing at random from deck into hand. Draw one more card at random into turned_card, and set trump_suit to its suit. Move the last card into hidden_card. Set leader = eldest. Set every player's tricks_taken, bid and hand_score to 0.
  2. [sync] all players. What happens: Each player is shown their own hand and the public state.
  3. [tell] all players. What happens: When trick_in_hand = 1: announce hand_number, dealer, eldest, turned_card and trump_suit.
  4. [poll] all players answers: a whole number from 0 to 6. What happens: When trick_in_hand = 1: each player's answer is stored in bid, and no bid is seen until all three are in.
  5. [tell] all players. What happens: When trick_in_hand = 1: reveal all three bids to everyone.
  6. [ask] the seat equal to leader answers: one card from their hand. What happens: Remove the card from the leader's hand and set the leader's played_card to it. Set led_suit to the card's suit. The play is shown to everyone.
  7. [ask] the seat to the leader's left (leader mod 3 + 1) answers: one card from their hand; it must be of led_suit if they hold any card of led_suit, otherwise any card. What happens: Remove the card from that player's hand and set their played_card to it. The play is shown to everyone.
  8. [ask] the third seat ((leader + 1) mod 3 + 1) answers: one card from their hand; it must be of led_suit if they hold any card of led_suit, otherwise any card. What happens: Remove the card from that player's hand and set their played_card to it. The play is shown to everyone.
  9. [update] all players. What happens: Rank values are A=14, K=13, Q=12, J=11, 10=10. If any played_card has suit trump_suit, trick_winner is the seat whose trump has the highest rank value; otherwise it is the seat whose led_suit card has the highest rank value. The winner gets tricks_taken += 1 and hand_score += 2, then hand_score -= 1 for JS, 2 for JC, 3 for JD and 4 for JH among the three played cards. Set leader = trick_winner.
  10. [tell] all players. What happens: Announce the three played cards, trick_winner, and every player's tricks_taken and hand_score.
  11. [update] all players. What happens: When trick_in_hand = 6: each player with tricks_taken = bid gets hand_score += 4. Then each player's total += hand_score. Announce each hand_score and total. Then set every hand_score to 0, set dealer = dealer mod 3 + 1, set eldest = dealer mod 3 + 1, and set hand_number += 1.
  12. [update] all players. What happens: Set round_number += 1. Set trick_in_hand = trick_in_hand mod 6 + 1. Clear every played_card and led_suit.
  13. [check] all players. What happens: If round_number > 36, the game ends; otherwise the round repeats.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, there are exactly 3 players and a 20-card deck of A, K, Q, J and 10 in each of spades, clubs, diamonds and hearts.
  R2. When cards of one suit are compared, they rank A (high), K, Q, J, 10 (low).
  R3. When the game runs, it consists of 6 hands of 6 tricks each, 36 rounds in all, one trick per round.
  R4. When hand 1 begins, seat 1 is dealer and seat 2 is eldest.
  R5. When a hand ends, the dealer moves one seat to the left (1 to 2, 2 to 3, 3 to 1), so each seat deals exactly 2 of the 6 hands.
  R6. When a hand begins, eldest is the seat to the dealer's left: dealer mod 3 + 1.
  R7. When a hand begins, all 20 cards are shuffled and each player is dealt 6 cards into their hand, which only the owner can see.
  R8. When a hand is dealt, the 19th card is turned face up into turned_card, trump_suit becomes its suit, and that card is out of play.
  R9. When a hand is dealt, the 20th card goes face down into hidden_card, is out of play, and is never revealed during the hand.
  R10. When a hand has been dealt, all players bid at the same moment a whole number from 0 to 6, and no bid is seen until all three are in.
  R11. When all three bids are in, all three are revealed to everyone.
  R12. When the first trick of a hand is played, eldest leads it.
  R13. When any trick after the first in a hand is played, the winner of the previous trick leads it.
  R14. When a trick is played, the leader plays first, then the seat to the leader's left, then the remaining seat.
  R15. When the leader plays, they may play any card from their hand.
  R16. When a following player holds a card of the led suit, they must play a card of the led suit.
  R17. When a following player holds no card of the led suit, they may play any card in their hand, including a trump.
  R18. When a trick contains at least one trump, the highest trump wins it.
  R19. When a trick contains no trump, the highest card of the led suit wins it, and off-suit cards cannot win.
  R20. When a player wins a trick, their tricks_taken rises by 1 and their hand_score rises by 2.
  R21. When a trick's winner takes Jacks, their hand_score falls by 1 for the Jack of spades, 2 for the Jack of clubs, 3 for the Jack of diamonds and 4 for the Jack of hearts in that trick.
  R22. When a trick ends, its three cards, its winner and every player's tricks taken are announced.
  R23. When the 6th trick of a hand ends, each player whose tricks_taken equals their bid adds 4 to their hand_score.
  R24. When the 6th trick of a hand ends, each player's hand_score is added to their total and announced, and then every hand_score resets to 0.
  R25. When all plays are made, every played card is visible to everyone as it is played.
  R26. When round 36 (the 6th trick of the 6th hand) is complete, the game ends.
  R27. When the game ends, the player with the highest total wins; if two or three players tie for the highest total, the game is a draw among them.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Bid (first round of each hand) | asked: all three seats, simultaneously | options: any whole number from 0 to 6
  - Lead a card | asked: the seat equal to leader (eldest on the first trick of a hand, otherwise the previous trick's winner) | options: every card in that seat's hand
  - Follow to the trick (second player) | asked: the seat to the leader's left | options: if the seat holds any card of led_suit, only its cards of led_suit; otherwise every card in its hand
  - Follow to the trick (third player) | asked: the remaining seat | options: if the seat holds any card of led_suit, only its cards of led_suit; otherwise every card in its hand

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round_number > 36
  - each player's standing: you.total (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their total after 6 hands (36 tricks). The highest total wins; if two or three players tie for the highest total, they share the result, which is the source's draw.
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
rounds it says a match may run at most) and `limits.rounds_max` to at least that. The ending's `when` holds for the real ending AND when the cap
is reached, and its `rank_by` also ranks the players as the script says at the cap, so a match that hits the cap still ends with a winner.

## The interface the file must use

Independent tests were written against these names and you cannot see them, so use them exactly.

- each player: `bid` (number, visible: public, starts 0): The tricks this player predicted for the current hand, from 0 to 6. Revealed after all players have bid.
- each player: `tricks_taken` (number, visible: public, starts 0): Tricks this player has won in the current hand.
- each player: `hand_score` (number, visible: public, starts 0): Points this player has earned in the current hand: 2 per trick, minus Jack penalties, plus any bid bonus.
- each player: `total` (number, visible: public, starts 0): This player's running game total, which is the score.
- each player: `played_card` (text, visible: public, starts ''): The card this player played to the current trick.
- the table: `turned_card` (text, visible: public, starts ''): The 19th card, turned face up. It sets trump and is out of play.
- the table: `trump_suit` (text, visible: public, starts ''): The suit of turned_card: S, C, D or H.
- the table: `hand_number` (number, visible: public, starts 1): The current hand, from 1 to 6.
- the table: `trick_winner` (number, visible: public, starts 0): The seat that won the last trick.
- parameters (each must be an attribute holding this value, never a number buried in a step): player_count = 3, deck_size = 20, suits = 4, ranks_per_suit = 5, hands = 6, tricks_per_hand = 6, total_rounds = 36, cards_dealt_per_player = 6, trump_card_position = 19, hidden_card_position = 20, bid_min = 0, bid_max = 6, trick_points = 2, jack_of_spades_penalty = 1, jack_of_clubs_penalty = 2, jack_of_diamonds_penalty = 3, jack_of_hearts_penalty = 4, exact_bid_bonus = 4, deals_per_player = 2, first_dealer_seat = 1, rank_value_A = 14, rank_value_K = 13, rank_value_Q = 12, rank_value_J = 11, rank_value_10 = 10
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

## Guidance from the last attempt

The previous attempt had problems:

Make the bid a single simultaneous poll of all three players in the first round of each hand, after the deal. Each player chooses a whole number from bid_min to bid_max, read from those parameter attributes, so the options are 0, 1, 2, 3, 4, 5, 6. Store each chosen value in that player's `bid` and reveal the bids only after all three are in. Do not take the bid options from the card `offer` list or from a derived value such as `strength`, and do not fall back to 0. Only after the bids are recorded should trick play begin, with the eldest leading. Check that the chosen bid is actually written: a test choosing 3 for seat 1 must leave bid = 3. Keep the rest of the deal as it is, since the hand counts, deck emptying and turned and hidden cards already behave correctly.


YOUR PREVIOUS GAME FILE WAS REFUSED. Here it is:
```json
{
  "schema": 1,
  "meta": {
    "id": "knaves_wager",
    "name": "Knaves' Wager",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Three players, six hands of six tricks: bid your tricks in secret, take tricks for points, dodge the Jacks, and hit your bid for a bonus."
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
      },
      {
        "key": "played_card",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "play_value",
        "visible": "ally",
        "type": "number",
        "initial": 0
      }
    ],
    "game": [
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": ["AS", "KS", "QS", "JS", "10S", "AC", "KC", "QC", "JC", "10C", "AD", "KD", "QD", "JD", "10D", "AH", "KH", "QH", "JH", "10H"]
      },
      {
        "key": "full_deck",
        "visible": "none",
        "type": "list",
        "initial": ["AS", "KS", "QS", "JS", "10S", "AC", "KC", "QC", "JC", "10C", "AD", "KD", "QD", "JD", "10D", "AH", "KH", "QH", "JH", "10H"]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "turned_card",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "hidden_card",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "trump_suit",
        "visible": "public",
        "type": "text",
        "initial": ""
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
        "key": "dealer",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "eldest",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "leader",
        "visible": "public",
        "type": "number",
        "initial": 2
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
        "key": "trump_weight",
        "visible": "none",
        "type": "number",
        "initial": 100
      },
      {
        "key": "led_weight",
        "visible": "none",
        "type": "number",
        "initial": 50
      },
      {
        "key": "player_count",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "suits",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "ranks_per_suit",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "hands",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "tricks_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "total_rounds",
        "visible": "public",
        "type": "number",
        "initial": 36
      },
      {
        "key": "cards_dealt_per_player",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "trump_card_position",
        "visible": "public",
        "type": "number",
        "initial": 19
      },
      {
        "key": "hidden_card_position",
        "visible": "public",
        "type": "number",
        "initial": 20
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
        "initial": 6
      },
      {
        "key": "trick_points",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "jack_of_spades_penalty",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "jack_of_clubs_penalty",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "jack_of_diamonds_penalty",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "jack_of_hearts_penalty",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "exact_bid_bonus",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "deals_per_player",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "first_dealer_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "rank_value_A",
        "visible": "public",
        "type": "number",
        "initial": 14
      },
      {
        "key": "rank_value_K",
        "visible": "public",
        "type": "number",
        "initial": 13
      },
      {
        "key": "rank_value_Q",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "rank_value_J",
        "visible": "public",
        "type": "number",
        "initial": 11
      },
      {
        "key": "rank_value_10",
        "visible": "public",
        "type": "number",
        "initial": 10
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
            "key": "trick_in_hand",
            "value": 1
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
            "key": "eldest",
            "value": {
              "calc": "dealer % player_count + 1"
            }
          }
        },
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "eldest"
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
      "label": "the deal",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "do": [
        {"set": {"key": "deck", "value": {"calc": "full_deck"}}},
        {"set": {"players": "all", "key": "hand", "value": []}},
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
        {"set": {"key": "turned_card", "value": {"calc": "pick"}}},
        {"set": {"key": "trump_suit", "value": {"calc": "turned_card[len(turned_card) - 1]"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "hidden_card", "value": {"calc": "deck[0]"}}},
        {"remove": {"key": "deck", "value": {"calc": "hidden_card"}}},
        {"set": {"key": "leader", "value": {"calc": "eldest"}}},
        {"set": {"players": "all", "key": "tricks_taken", "value": 0}},
        {"set": {"players": "all", "key": "bid", "value": 0}},
        {"set": {"players": "all", "key": "hand_score", "value": 0}},
        {"set": {"players": "all", "key": "played_card", "value": ""}}
      ]
    },
    {
      "use": "sync",
      "phase": "deal",
      "label": "your hand",
      "mode": "self",
      "to": "all",
      "fields": [
        "hand",
        "bid",
        "tricks_taken",
        "hand_score",
        "total"
      ],
      "text": "Your current state:"
    },
    {
      "use": "tell",
      "phase": "deal",
      "label": "the hand begins",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "to": "all",
      "text": "Hand {hand_number} of {hands}. Dealer: seat {dealer}. Eldest: seat {eldest}, who leads the first trick. The turned card is {turned_card}, so trump is {trump_suit}."
    },
    {
      "use": "poll",
      "phase": "bid",
      "label": "the bid",
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
      "store": "bid",
      "text": "Bid in secret: how many of the {tricks_per_hand} tricks this hand will you take? Answer a whole number from {bid_min} to {bid_max}. Trump is {trump_suit}. No bid is shown until all three are in."
    },
    {
      "use": "tell",
      "phase": "bid",
      "label": "the bids revealed",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "to": "all",
      "text": "Bids for hand {hand_number}: Seat 1 bid {players[0].bid}, Seat 2 bid {players[1].bid}, Seat 3 bid {players[2].bid}."
    },
    {
      "use": "ask",
      "phase": "trick",
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
                "calc": "[p.played_card[len(p.played_card) - 1] for p in players if p.seat == leader][0]"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} leads {value} to trick {trick_in_hand}."
      },
      "text": "You lead trick {trick_in_hand} of hand {hand_number}. Trump is {trump_suit}. Play any card from your hand."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "who may follow with what",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "[c for c in you.hand if c[len(c) - 1] == led_suit] if count(c[len(c) - 1] == led_suit for c in you.hand) > 0 else you.hand"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "the second play",
      "to": {
        "where": "you.seat == leader % player_count + 1"
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
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} plays {value}."
      },
      "text": "Led suit is {led_suit}; trump is {trump_suit}. Play a card: you must follow the led suit if you can, otherwise any card, trump included. Only legal cards are offered."
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "the third play",
      "to": {
        "where": "you.seat == (leader + 1) % player_count + 1"
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
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} plays {value}."
      },
      "text": "Led suit is {led_suit}; trump is {trump_suit}. Play a card: you must follow the led suit if you can, otherwise any card, trump included. Only legal cards are offered."
    },
    {
      "use": "update",
      "phase": "score",
      "label": "the trick is taken",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "play_value",
            "value": {
              "calc": "(rank_value_A if you.played_card[0] == 'A' else rank_value_K if you.played_card[0] == 'K' else rank_value_Q if you.played_card[0] == 'Q' else rank_value_J if you.played_card[0] == 'J' else rank_value_10) + (trump_weight if you.played_card[len(you.played_card) - 1] == trump_suit else (led_weight if you.played_card[len(you.played_card) - 1] == led_suit else 0))"
            }
          }
        },
        {
          "set": {
            "key": "trick_winner",
            "value": {
              "calc": "max([[p.play_value, p.seat] for p in players])[1]"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "trick_winner"
            },
            "key": "tricks_taken",
            "value": 1
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "trick_winner"
            },
            "key": "hand_score",
            "value": {
              "calc": "trick_points - ((jack_of_spades_penalty if count(p.played_card == 'JS' for p in players) > 0 else 0) + (jack_of_clubs_penalty if count(p.played_card == 'JC' for p in players) > 0 else 0) + (jack_of_diamonds_penalty if count(p.played_card == 'JD' for p in players) > 0 else 0) + (jack_of_hearts_penalty if count(p.played_card == 'JH' for p in players) > 0 else 0))"
            }
          }
        },
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
      "use": "tell",
      "phase": "score",
      "label": "the trick announced",
      "to": "all",
      "text": "Trick {trick_in_hand} of hand {hand_number}: Seat 1 played {players[0].played_card}, Seat 2 played {players[1].played_card}, Seat 3 played {players[2].played_card}. Seat {trick_winner} wins the trick. Tricks taken: Seat 1 {players[0].tricks_taken}, Seat 2 {players[1].tricks_taken}, Seat 3 {players[2].tricks_taken}. Hand scores: Seat 1 {players[0].hand_score}, Seat 2 {players[1].hand_score}, Seat 3 {players[2].hand_score}."
    },
    {
      "use": "update",
      "phase": "hand end",
      "label": "the hand is scored",
      "when": {
        "calc": "trick_in_hand == tricks_per_hand"
      },
      "do": [
        {
          "adjust": {
            "players": {
              "where": "you.tricks_taken == you.bid"
            },
            "key": "hand_score",
            "value": {
              "calc": "exact_bid_bonus"
            },
            "text": "Seat {player} made their bid exactly and earns the bonus."
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
        }
      ]
    },
    {
      "use": "tell",
      "phase": "hand end",
      "label": "the hand totals",
      "when": {
        "calc": "trick_in_hand == tricks_per_hand"
      },
      "to": "all",
      "text": "End of hand {hand_number}. Hand scores: Seat 1 {players[0].hand_score}, Seat 2 {players[1].hand_score}, Seat 3 {players[2].hand_score}. Totals: Seat 1 {players[0].total}, Seat 2 {players[1].total}, Seat 3 {players[2].total}."
    },
    {
      "use": "update",
      "phase": "hand end",
      "label": "advance",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "hand_score",
            "value": 0,
            "if": {
              "calc": "trick_in_hand == tricks_per_hand"
            }
          }
        },
        {
          "set": {
            "key": "dealer",
            "value": {
              "calc": "dealer % player_count + 1"
            },
            "if": {
              "calc": "trick_in_hand == tricks_per_hand"
            }
          }
        },
        {
          "set": {
            "key": "eldest",
            "value": {
              "calc": "dealer % player_count + 1"
            },
            "if": {
              "calc": "trick_in_hand == tricks_per_hand"
            }
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
          "adjust": {
            "key": "round_number",
            "value": 1
          }
        },
        {
          "set": {
            "key": "trick_in_hand",
            "value": {
              "calc": "trick_in_hand % tricks_per_hand + 1"
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
            "key": "led_suit",
            "value": ""
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "hand end",
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
      "rank_by": "you.total",
      "text": "Winner: {result}. Final totals: Seat 1 {players[0].total}, Seat 2 {players[1].total}, Seat 3 {players[2].total}."
    }
  },
  "limits": {
    "rounds": 36,
    "rounds_max": 40,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "{player_count} players sit in a fixed order; the seat to a player's left is the next seat number, and seat 1 follows seat 3. The deck has {deck_size} cards: A, K, Q, J and 10 in each of spades (S), clubs (C), diamonds (D) and hearts (H). Within a suit, cards rank A (high), K, Q, J, 10 (low).\n\nThe game is {ha
... (cut)

Why it was refused: it plays, but part of it does nothing: game attribute `full_deck` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `trump_weight` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `led_weight` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "knaves_wager",
    "name": "Knaves' Wager",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Three players, six hands of six tricks: bid your tricks in secret, take tricks for points, dodge the Jacks, and hit your bid for a bonus."
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
      },
      {
        "key": "played_card",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "play_value",
        "visible": "ally",
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
          "AS",
          "KS",
          "QS",
          "JS",
          "10S",
          "AC",
          "KC",
          "QC",
          "JC",
          "10C",
          "AD",
          "KD",
          "QD",
          "JD",
          "10D",
          "AH",
          "KH",
          "QH",
          "JH",
          "10H"
        ]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "turned_card",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "hidden_card",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "trump_suit",
        "visible": "public",
        "type": "text",
        "initial": ""
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
        "key": "dealer",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "eldest",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "leader",
        "visible": "public",
        "type": "number",
        "initial": 2
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
        "key": "player_count",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "suits",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "ranks_per_suit",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "hands",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "tricks_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "total_rounds",
        "visible": "public",
        "type": "number",
        "initial": 36
      },
      {
        "key": "cards_dealt_per_player",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "trump_card_position",
        "visible": "public",
        "type": "number",
        "initial": 19
      },
      {
        "key": "hidden_card_position",
        "visible": "public",
        "type": "number",
        "initial": 20
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
        "initial": 6
      },
      {
        "key": "trick_points",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "jack_of_spades_penalty",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "jack_of_clubs_penalty",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "jack_of_diamonds_penalty",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "jack_of_hearts_penalty",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "exact_bid_bonus",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "deals_per_player",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "first_dealer_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "rank_value_A",
        "visible": "public",
        "type": "number",
        "initial": 14
      },
      {
        "key": "rank_value_K",
        "visible": "public",
        "type": "number",
        "initial": 13
      },
      {
        "key": "rank_value_Q",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "rank_value_J",
        "visible": "public",
        "type": "number",
        "initial": 11
      },
      {
        "key": "rank_value_10",
        "visible": "public",
        "type": "number",
        "initial": 10
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
            "key": "trick_in_hand",
            "value": 1
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
            "key": "eldest",
            "value": {
              "calc": "dealer % player_count + 1"
            }
          }
        },
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "eldest"
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
      "label": "the deal",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "do": [
        {
          "append": {
            "key": "deck",
            "value": {
              "calc": "turned_card"
            },
            "if": {
              "calc": "turned_card != ''"
            }
          }
        },
        {
          "append": {
            "key": "deck",
            "value": {
              "calc": "hidden_card"
            },
            "if": {
              "calc": "hidden_card != ''"
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
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
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
              "calc": "deck[int(uniform(0, len(deck)))]"
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
              "calc": "deck[int(uniform(0, len(deck)))]"
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
              "calc": "deck[int(uniform(0, len(deck)))]"
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
              "calc": "deck[int(uniform(0, len(deck)))]"
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
              "calc": "deck[int(uniform(0, len(deck)))]"
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
              "calc": "deck[int(uniform(0, len(deck)))]"
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
              "calc": "deck[int(uniform(0, len(deck)))]"
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
              "calc": "deck[int(uniform(0, len(deck)))]"
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
              "calc": "deck[int(uniform(0, len(deck)))]"
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
              "calc": "deck[int(uniform(0, len(deck)))]"
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
              "calc": "deck[int(uniform(0, len(deck)))]"
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
              "calc": "deck[int(uniform(0, len(deck)))]"
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
              "calc": "deck[int(uniform(0, len(deck)))]"
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
              "calc": "deck[int(uniform(0, len(deck)))]"
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
              "calc": "deck[int(uniform(0, len(deck)))]"
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
              "calc": "deck[int(uniform(0, len(deck)))]"
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
              "calc": "deck[int(uniform(0, len(deck)))]"
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
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "set": {
            "key": "turned_card",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "trump_suit",
            "value": {
              "calc": "turned_card[len(turned_card) - 1]"
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
            "key": "hidden_card",
            "value": {
              "calc": "deck[0]"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "hidden_card"
            }
          }
        },
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "eldest"
            }
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
            "key": "bid",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_score",
            "value": 0
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
      "use": "sync",
      "phase": "deal",
      "label": "your hand",
      "mode": "self",
      "to": "all",
      "fields": [
        "hand",
        "bid",
        "tricks_taken",
        "hand_score",
        "total"
      ],
      "text": "Your current state:"
    },
    {
      "use": "tell",
      "phase": "deal",
      "label": "the hand begins",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "to": "all",
      "text": "Hand {hand_number} of {hands}. Dealer: seat {dealer}. Eldest: seat {eldest}, who leads the first trick. The turned card is {turned_card}, so trump is {trump_suit}."
    },
    {
      "use": "poll",
      "phase": "bid",
      "label": "the bid",
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
      "store": "bid",
      "text": "Bid in secret: how many of the {tricks_per_hand} tricks this hand will you take? Answer a whole number from {bid_min} to {bid_max}. Trump is {trump_suit}. No bid is shown until all three are in."
    },
    {
      "use": "tell",
      "phase": "bid",
      "label": "the bids revealed",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "to": "all",
      "text": "Bids for hand {hand_number}: Seat 1 bid {players[0].bid}, Seat 2 bid {players[1].bid}, Seat 3 bid {players[2].bid}."
    },
    {
      "use": "ask",
      "phase": "trick",
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
            "set": {
              "player": "$seat",
              "key": "played_card",
              "value": "$answer"
            }
          },
          {
            "append": {
              "key": "deck",
              "value": "$answer"
            }
          },
          {
            "set": {
              "key": "led_suit",
              "value": {
                "calc": "[p.played_card[len(p.played_card) - 1] for p in players if p.seat == leader][0]"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} leads {value} to trick {trick_in_hand}."
      },
      "text": "You lead trick {trick_in_hand} of hand {hand_number}. Trump is {trump_suit}. Play any card from your hand."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "who may follow with what",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "[c for c in you.hand if c[len(c) - 1] == led_suit] if count(c[len(c) - 1] == led_suit for c in you.hand) > 0 else you.hand"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "the second play",
      "to": {
        "where": "you.seat == leader % player_count + 1"
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
            "append": {
              "key": "deck",
              "value": "$answer"
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} plays {value}."
      },
      "text": "Led suit is {led_suit}; trump is {trump_suit}. Play a card: you must follow the led suit if you can, otherwise any card, trump included. Only legal cards are offered."
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "the third play",
      "to": {
        "where": "you.seat == (leader + 1) % player_count + 1"
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
            "append": {
              "key": "deck",
              "value": "$answer"
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} plays {value}."
      },
      "text": "Led suit is {led_suit}; trump is {trump_suit}. Play a card: you must follow the led suit if you can, otherwise any card, trump included. Only legal cards are offered."
    },
    {
      "use": "update",
      "phase": "score",
      "label": "the trick is taken",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "play_value",
            "value": {
              "calc": "(rank_value_A if you.played_card[0] == 'A' else rank_value_K if you.played_card[0] == 'K' else rank_value_Q if you.played_card[0] == 'Q' else rank_value_J if you.played_card[0] == 'J' else rank_value_10) + ((rank_value_A + rank_value_A) if you.played_card[len(you.played_card) - 1] == trump_suit else (rank_value_A if you.played_card[len(you.played_card) - 1] == led_suit else 0))"
            }
          }
        },
        {
          "set": {
            "key": "trick_winner",
            "value": {
              "calc": "max([[p.play_value, p.seat] for p in players])[1]"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "trick_winner"
            },
            "key": "tricks_taken",
            "value": 1
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "trick_winner"
            },
            "key": "hand_score",
            "value": {
              "calc": "trick_points - ((jack_of_spades_penalty if count(p.played_card == 'JS' for p in players) > 0 else 0) + (jack_of_clubs_penalty if count(p.played_card == 'JC' for p in players) > 0 else 0) + (jack_of_diamonds_penalty if count(p.played_card == 'JD' for p in players) > 0 else 0) + (jack_of_hearts_penalty if count(p.played_card == 'JH' for p in players) > 0 else 0))"
            }
          }
        },
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
      "use": "tell",
      "phase": "score",
      "label": "the trick announced",
      "to": "all",
      "text": "Trick {trick_in_hand} of hand {hand_number}: Seat 1 played {players[0].played_card}, Seat 2 played {players[1].played_card}, Seat 3 played {players[2].played_card}. Seat {trick_winner} wins the trick. Tricks taken: Seat 1 {players[0].tricks_taken}, Seat 2 {players[1].tricks_taken}, Seat 3 {players[2].tricks_taken}. Hand scores: Seat 1 {players[0].hand_score}, Seat 2 {players[1].hand_score}, Seat 3 {players[2].hand_score}."
    },
    {
      "use": "update",
      "phase": "hand end",
      "label": "the hand is scored",
      "when": {
        "calc": "trick_in_hand == tricks_per_hand"
      },
      "do": [
        {
          "adjust": {
            "players": {
              "where": "you.tricks_taken == you.bid"
            },
            "key": "hand_score",
            "value": {
              "calc": "exact_bid_bonus"
            },
            "text": "Seat {player} made their bid exactly and earns the bonus."
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
        }
      ]
    },
    {
      "use": "tell",
      "phase": "hand end",
      "label": "the hand totals",
      "when": {
        "calc": "trick_in_hand == tricks_per_hand"
      },
      "to": "all",
      "text": "End of hand {hand_number}. Hand scores: Seat 1 {players[0].hand_score}, Seat 2 {players[1].hand_score}, Seat 3 {players[2].hand_score}. Totals: Seat 1 {players[0].total}, Seat 2 {players[1].total}, Seat 3 {players[2].total}."
    },
    {
      "use": "update",
      "phase": "hand end",
      "label": "advance",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "hand_score",
            "value": 0,
            "if": {
              "calc": "trick_in_hand == tricks_per_hand"
            }
          }
        },
        {
          "set": {
            "key": "dealer",
            "value": {
              "calc": "dealer % player_count + 1"
            },
            "if": {
              "calc": "trick_in_hand == tricks_per_hand"
            }
          }
        },
        {
          "set": {
            "key": "eldest",
            "value": {
              "calc": "dealer % player_count + 1"
            },
            "if": {
              "calc": "trick_in_hand == tricks_per_hand"
            }
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
          "adjust": {
            "key": "round_number",
            "value": 1
          }
        },
        {
          "set": {
            "key": "trick_in_hand",
            "value": {
              "calc": "trick_in_hand % tricks_per_hand + 1"
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
            "key": "led_suit",
            "value": ""
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "hand end",
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
      "rank_by": "you.total",
      "text": "Winner: {result}. Final totals: Seat 1 {players[0].total}, Seat 2 {players[1].total}, Seat 3 {players[2].total}."
    }
  },
  "limits": {
    "rounds": 36,
    "rounds_max": 40,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "{player_count} players sit in a fixed order; the seat to a player's left is the next seat number, and seat 1 follows seat 3. The deck has {deck_size} cards: A, K, Q, J and 10 in each of spades (S), clubs (C), diamonds (D) and hearts (H). Within a suit, cards rank A (high), K, Q, J, 10 (low).\n\nThe game is {hands} hands of {tricks_per_hand} tricks each, {total_rounds} rounds in all; each round is one trick. The dealer for hand 1 is seat {first_dealer_seat}. The dealer moves one seat to the left each hand (1 to 2, 2 to 3, 3 to 1), so each player deals {deals_per_player} times. The player to the dealer's left is eldest for that hand.\n\nDEAL (first round of each hand): all {deck_size} cards are shuffled. Each player is dealt {cards_dealt_per_player} cards privately; a hand is seen only by its owner. Card {trump_card_position} is turned face up: its suit is trump for this hand, and the card itself is out of play. Card {hidden_card_position} stays face down, is out of play, and is never revealed during the hand.\n\nBID (first round of each hand, after the deal): all players at the same moment secretly choose a whole number from {bid_min} to {bid_max}: the number of tricks they predict they will take this hand. All three bids are then revealed to everyone.\n\nTRICK PLAY (every round): the leader plays any card from their hand face up. The eldest leads the first trick of a hand; afterwards, the winner of the previous trick leads. Then the next player to the left plays, then the third. Each must play a card of the led suit if they have one. If they have none, they may play any card, including a trump. You are offered only the cards you may legally play. The trick is won by the highest trump in it. If it holds no trump, the highest card of the led suit wins; off-suit cards cannot win. All plays are visible to everyone as they are made.\n\nTRICK SCORING: the trick winner adds {trick_points} to their hand score. They also take penalties for any Jacks in the trick: Jack of spades -{jack_of_spades_penalty}, Jack of clubs -{jack_of_clubs_penalty}, Jack of diamonds -{jack_of_diamonds_penalty}, Jack of hearts -{jack_of_hearts_penalty}. The trick's cards, its winner and the running trick counts are announced.\n\nEND OF HAND (after the 6th trick): any player whose tricks taken equal their bid adds {exact_bid_bonus} to their hand score; a player who misses their bid, over or under, gets no bonus. Each player's hand score (points per trick, minus Jack penalties, plus any bid bonus) is added to their total and announced. Hand scores reset to 0, and the dealer rotates.\n\nEND OF GAME: after the 6th hand (round {total_rounds}), the game ends. The player with the highest total wins; if two or three players tie for the highest total, the game is a draw among them."
}
```
````
