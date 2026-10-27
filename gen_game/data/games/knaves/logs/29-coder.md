# 29 coder

- time: 2026-10-27T18:37:11+00:00 (118.3s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 1a06244f0e4a1e7d, reply sha256 ad9b08b86b50ea40

## Sent

````
# Task: write the XColos game file for "Knaves Short Deck with Bids"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

R1 Setup. There are exactly 3 players, seats 1, 2 and 3. The full deck is the 20 cards AS KS QS JS 10S AC KC QC JC 10C AD KD QD JD 10D AH KH QH JH 10H. At the start every player's total is 0, their hand is empty, hand_number is 1, and the deck holds all 20 cards.

R2 Rank. Within a suit, cards rank A (high), K, Q, J, 10 (low).

R3 Length. The game has exactly 36 rounds. Each round is one trick. The game ends after round 36.

R4 Hands. Rounds 1-6 form hand 1, rounds 7-12 hand 2, and so on up to rounds 31-36, which form hand 6. trick_in_hand runs from 1 to 6 within each hand.

R5 Dealer. In hand h, the dealer is seat ((h-1) mod 3) + 1. So hand 1 is dealt by seat 1, hand 2 by seat 2, hand 3 by seat 3, hand 4 by seat 1, and so on.

R6 Eldest. When a hand begins, eldest is the seat to the dealer's left: (dealer mod 3) + 1. Eldest is the leader of that hand's first trick.

R7 Reset and deal. In the first round of every hand, before anything else happens:
(a) Set the deck to the full 20-card list from R1.
(b) Empty every player's hand and the discard pile.
(c) Set every player's bid, tricks_taken and hand_score to 0.
(d) Shuffle the deck once. This is the only random event in the round.
(e) Cards 1-6 of the shuffled deck go to seat 1, cards 7-12 to seat 2, and cards 13-18 to seat 3. Each hand is seen only by its owner.

R8 Turned card. Card 19 is turned face up into turned_card, seen by all, and trump_suit becomes its suit. That card is out of play for the hand.

R9 Hidden card. Card 20 goes face down into hidden_card. It is out of play and is never revealed during the hand. After the deal the deck holds 0 cards.

R10 Bid. In the first round of every hand, right after the deal, all three seats bid at the same moment in one simultaneous poll. Each seat is offered exactly the options 0, 1, 2, 3, 4, 5 and 6: the number of tricks it predicts it will take this hand. All bids are then shown to everyone.

R11 Play order. Every round, the leader plays one card from their hand first. Then seat (leader mod 3) + 1 plays, then the remaining seat. Players act one at a time and each sees the cards already played to the trick. The suit of the leader's card is led_suit. Each played card is removed from its owner's hand, recorded as that player's played_card, and added to the discard pile. It never returns to the deck.

R12 Follow suit. A player who holds any card of led_suit must play one of those cards. A player who holds none may play any card in their hand, including a trump. The leader may play any card.

R13 Trick winner. If any trump_suit cards were played, the highest-ranked trump wins. Otherwise the highest-ranked card of led_suit wins. The winner becomes trick_winner and leads the next trick of the same hand.

R14 Trick score. The trick winner adds 1 to tricks_taken and adds to hand_score: +2, minus the penalties for any Jacks among the three cards in the trick (JS 1, JC 2, JD 3, JH 4). A Jack is penalised even if it is the trump suit.

R15 End of hand. After the trick in round 6, 12, 18, 24, 30 or 36 is scored:
(a) Each player whose tricks_taken equals their bid adds 5 to hand_score.
(b) Each player adds hand_score to their total.
(c) The totals are announced to all.

R16 Winner. After round 36, the player with the highest total wins. If two or three players tie for the highest total, the game is a draw.

How the winner is decided: After the 36th trick and the final end-of-hand scoring, the single player with the highest total wins. A tie for the highest total is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Knaves Short Deck with Bids (3 to 3 players, best with 3)

Three players play 36 tricks with a 20-card deck, in six hands of six tricks. Each player bids how many tricks they will take each hand, Jacks in a won trick cost points, and an exact bid earns a bonus.

STATE (every item below must exist in the file):
  - each player: total (number, starts 0); everyone sees it. Running game score, added to at the end of each hand
  - each player: hand (list, starts []); only its owner sees it. Cards the player holds in the current hand, seen only by the owner
  - each player: bid (number, starts 0); everyone sees it. Number of tricks the player predicted for this hand, shown to all after the simultaneous bid
  - each player: tricks_taken (number, starts 0); everyone sees it. Tricks won so far in this hand
  - each player: hand_score (number, starts 0); everyone sees it. Points scored in this hand so far
  - each player: played_card (text, starts ''); everyone sees it. Card the player played to the current trick
  - the table: deck (list, starts ['AS', 'KS', 'QS', 'JS', '10S', 'AC', 'KC', 'QC', 'JC', '10C', 'AD', 'KD', 'QD', 'JD', '10D', 'AH', 'KH', 'QH', 'JH', '10H']); hidden from all players. Undealt cards; empty after each deal
  - the table: discard (list, starts []); everyone sees it. Cards played so far this hand
  - the table: turned_card (text, starts ''); everyone sees it. Card 19 of the shuffled deck, face up and out of play
  - the table: trump_suit (text, starts ''); everyone sees it. Suit of turned_card (S, C, D or H)
  - the table: hidden_card (text, starts ''); hidden from all players. Card 20 of the shuffled deck, face down, out of play, never revealed
  - the table: round (number, starts 1); everyone sees it. Current round (trick) number, 1 to 36
  - the table: hand_number (number, starts 1); everyone sees it. Current hand, floor((round-1)/6)+1
  - the table: trick_in_hand (number, starts 1); everyone sees it. Trick within the hand, ((round-1) mod 6)+1
  - the table: dealer (number, starts 1); everyone sees it. Dealer seat, ((hand_number-1) mod 3)+1
  - the table: leader (number, starts 2); everyone sees it. Seat that leads the current trick
  - the table: led_suit (text, starts ''); everyone sees it. Suit of the leader's card in the current trick
  - the table: trick_winner (number, starts 0); everyone sees it. Seat that won the most recent trick
  - parameters, each kept as a table attribute: num_players = 3, deck_size = 20, total_rounds = 36, tricks_per_hand = 6, num_hands = 6, cards_per_player = 6, turned_card_position = 19, hidden_card_position = 20, bid_min = 0, bid_max = 6, trick_base_points = 2, penalty_JS = 1, penalty_JC = 2, penalty_JD = 3, penalty_JH = 4, exact_bid_bonus = 5, rank_value_A = 5, rank_value_K = 4, rank_value_Q = 3, rank_value_J = 2, rank_value_10 = 1, trump_bonus = 10

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seat three players, seats 1, 2 and 3.
  2. Set every player's total to 0 and hand to empty.
  3. Set round to 1, hand_number to 1 and trick_in_hand to 1.
  4. Set deck to the full 20-card list: AS KS QS JS 10S AC KC QC JC 10C AD KD QD JD 10D AH KH QH JH 10H.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: When trick_in_hand == 1: set dealer = ((hand_number-1) mod 3)+1 and leader = (dealer mod 3)+1. Set deck to the full 20-card list, empty every hand and discard, and set every bid, tricks_taken and hand_score to 0. Shuffle the deck once. Deal cards 1-6 to seat 1's hand, 7-12 to seat 2's hand and 13-18 to seat 3's hand. Put card 19 in turned_card and set trump_suit to its suit. Put card 20 in hidden_card. The deck is now empty. Announce turned_card, trump_suit, dealer and leader.
  2. [sync] all players. What happens: When trick_in_hand == 1: each player is sent their own hand, plus the public turned_card and trump_suit.
  3. [poll] all players answers: a whole number from 0 to 6. What happens: When trick_in_hand == 1: set each player's bid to their answer. After all answers are in, broadcast every bid to all.
  4. [ask] the seat equal to leader answers: one card from own hand (any card). What happens: Remove the card from the leader's hand, set the leader's played_card to it, append it to discard, and set led_suit to its suit. Show the card to all.
  5. [ask] seat (leader mod 3)+1 answers: one card from own hand: a led_suit card if any is held, otherwise any card. What happens: Remove the card from the hand, set played_card to it, append it to discard, and show it to all.
  6. [ask] seat ((leader+1) mod 3)+1 answers: one card from own hand: a led_suit card if any is held, otherwise any card. What happens: Remove the card from the hand, set played_card to it, append it to discard, and show it to all.
  7. [update] all players. What happens: Score each played_card as rank value (A 5, K 4, Q 3, J 2, 10 1), plus 10 if its suit is trump_suit, or 0 if its suit is neither trump_suit nor led_suit. Set trick_winner to the seat with the highest score. That seat adds 1 to tricks_taken and adds 2 - (1 if JS played) - (2 if JC played) - (3 if JD played) - (4 if JH played) to hand_score. Set leader = trick_winner. Announce the winner.
  8. [update] all players. What happens: When trick_in_hand == 6: each player with tricks_taken == bid adds 5 to hand_score. Every player then adds hand_score to total. Announce all totals.
  9. [update] all players. What happens: Add 1 to round. Set trick_in_hand = ((round-1) mod 6)+1 and hand_number = floor((round-1)/6)+1.
  10. [check] all players. What happens: End the game if round > 36; otherwise continue to the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, every player's total is 0, hand_number is 1, and the deck holds the 20 cards AS KS QS JS 10S AC KC QC JC 10C AD KD QD JD 10D AH KH QH JH 10H.
  R2. Within a suit, cards rank A > K > Q > J > 10.
  R3. When round 36's trick and end-of-hand scoring are done, the game ends; it never runs a 37th trick.
  R4. When round is r, hand_number is floor((r-1)/6)+1 and trick_in_hand is ((r-1) mod 6)+1, so rounds 31-36 are hand 6.
  R5. When hand h begins, dealer is ((h-1) mod 3)+1: hand 1 is seat 1, hand 2 seat 2, hand 3 seat 3, hand 4 seat 1.
  R6. When a hand begins, leader of its first trick is (dealer mod 3)+1, so hand 1 is led by seat 2.
  R7. When trick_in_hand is 1, the deck is reset to 20 cards, hands and discard are emptied, bid, tricks_taken and hand_score are set to 0, and seats 1, 2 and 3 each receive 6 cards, seen only by their owner.
  R8. When a hand is dealt, card 19 becomes turned_card, visible to all, trump_suit is its suit, and it is not in any hand.
  R9. When a hand is dealt, card 20 becomes hidden_card, is never shown, and the deck then holds 0 cards.
  R10. When trick_in_hand is 1, all three seats bid simultaneously from 0-6, and after all are in, every bid is shown to all.
  R11. When a trick is played, the leader plays first, then seat (leader mod 3)+1, then the remaining seat; each played card leaves the hand, becomes played_card and is appended to discard.
  R12. When a non-leader holds a card of led_suit, they are offered only led_suit cards; when they hold none, they are offered every card in their hand.
  R13. When any trump is played, the highest trump wins the trick; otherwise the highest led_suit card wins; the winner leads the next trick.
  R14. When a player wins a trick, tricks_taken rises by 1 and hand_score rises by 2 minus 1 for JS, 2 for JC, 3 for JD and 4 for JH among the trick's cards, including a trump Jack (e.g. a trick containing JH and JS scores 2-4-1 = -3).
  R15. When trick_in_hand 6 is scored, each player with tricks_taken equal to bid gains 5 hand_score, every player adds hand_score to total, and totals are announced.
  R16. When the game ends, the player with the highest total wins; players tied for highest share it, which the source calls a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Bid (first round of each hand) | asked: all three seats, simultaneously | options: 0, 1, 2, 3, 4, 5, 6 for every seat
  - Lead a card | asked: the seat equal to leader | options: every card in the leader's hand
  - Play a card (second and third to the trick) | asked: seat (leader mod 3)+1, then the remaining seat | options: a seat holding a led_suit card: only its led_suit cards; a seat holding no led_suit card: every card in its hand

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round > 36
  - each player's standing: you.total (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their total after the end-of-hand scoring of hand 6. The highest total wins. Players tied for the highest total share the result, which the source calls a draw.
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

- each player: `total` (number, visible: public, starts 0): Running game score, added to at the end of each hand
- each player: `bid` (number, visible: public, starts 0): Number of tricks the player predicted for this hand, shown to all after the simultaneous bid
- each player: `tricks_taken` (number, visible: public, starts 0): Tricks won so far in this hand
- the table: `turned_card` (text, visible: public, starts ''): Card 19 of the shuffled deck, face up and out of play
- the table: `trump_suit` (text, visible: public, starts ''): Suit of turned_card (S, C, D or H)
- the table: `hand_number` (number, visible: public, starts 1): Current hand, floor((round-1)/6)+1
- the table: `trick_winner` (number, visible: public, starts 0): Seat that won the most recent trick
- parameters (each must be an attribute holding this value, never a number buried in a step): num_players = 3, deck_size = 20, total_rounds = 36, tricks_per_hand = 6, num_hands = 6, cards_per_player = 6, turned_card_position = 19, hidden_card_position = 20, bid_min = 0, bid_max = 6, trick_base_points = 2, penalty_JS = 1, penalty_JC = 2, penalty_JD = 3, penalty_JH = 4, exact_bid_bonus = 5, rank_value_A = 5, rank_value_K = 4, rank_value_Q = 3, rank_value_J = 2, rank_value_10 = 1, trump_bonus = 10
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

Fix the bid poll in the first round of each hand (trick_in_hand == 1). Run it as one simultaneous poll of all three seats, right after the deal. Each seat must be offered exactly the options 0, 1, 2, 3, 4, 5 and 6, built from the bid_min and bid_max parameters (0 to 6 inclusive). Do not build the range from the player's current bid or tricks_taken, and do not leave it with only one option. Make sure the option values match the form the tests use, so the strings '0' to '6' are offered. Store the chosen value in each player's `bid` as a number, and do it after the R7 reset sets bids to 0 so the reset does not wipe it. Also confirm that the bid poll runs again in rounds 7, 13, 19, 25 and 31, not only in round 1.

````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "knaves_short_deck_bids",
    "name": "Knaves Short Deck with Bids",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Three players, a 20-card deck, six hands of six tricks: bid your tricks, dodge the Jacks, hit your bid for a bonus."
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
        "key": "total",
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
      },
      {
        "key": "offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "trick_points",
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
        "key": "bid_options",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "discard",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "turned_card",
        "visible": "public",
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
        "key": "hidden_card",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 1
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
        "key": "num_players",
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
        "key": "total_rounds",
        "visible": "public",
        "type": "number",
        "initial": 36
      },
      {
        "key": "tricks_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "num_hands",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "cards_per_player",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "turned_card_position",
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
        "key": "trick_base_points",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "penalty_JS",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "penalty_JC",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "penalty_JD",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "penalty_JH",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "exact_bid_bonus",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "rank_value_A",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "rank_value_K",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "rank_value_Q",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "rank_value_J",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "rank_value_10",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "trump_bonus",
        "visible": "public",
        "type": "number",
        "initial": 10
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the starting state",
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
            "players": "all",
            "key": "hand",
            "value": []
          }
        },
        {
          "set": {
            "key": "round",
            "value": 1
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
            "key": "deck",
            "value": {
              "calc": "full_deck"
            }
          }
        },
        {
          "set": {
            "key": "bid_options",
            "value": {
              "calc": "[x for x in ['0', '1', '2', '3', '4', '5', '6'] if int(x) >= bid_min and int(x) <= bid_max]"
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
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "deal",
      "label": "reset and deal",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "do": [
        {
          "set": {
            "key": "dealer",
            "value": {
              "calc": "(hand_number - 1) % num_players + 1"
            }
          }
        },
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "dealer % num_players + 1"
            }
          }
        },
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
            "key": "discard",
            "value": []
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
            "key": "tricks_taken",
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
        },
        {
          "set": {
            "players": "all",
            "key": "bid_said",
            "value": ""
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
            "key": "turned_card",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "turned_card"
            }
          }
        },
        {
          "set": {
            "key": "trump_suit",
            "value": {
              "calc": "turned_card[-1]"
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
        }
      ],
      "text": "Hand {hand_number} is dealt by seat {dealer}. The turned card is {turned_card}, so trumps are {trump_suit}. Seat {leader} leads the first trick."
    },
    {
      "use": "sync",
      "phase": "deal",
      "label": "your cards",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "mode": "self",
      "to": "all",
      "text": "Your cards for hand {hand_number}: {hand}. Turned card {turned_card}; trumps are {trump_suit}."
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
        "type": "choice",
        "options": {
          "game": "bid_options"
        }
      },
      "store": "bid_said",
      "text": "Hand {hand_number}, trumps {trump_suit}. Bid the number of tricks you will take this hand, from {bid_min} to {bid_max}. All three seats bid at once; hitting your bid exactly earns {exact_bid_bonus} points."
    },
    {
      "use": "update",
      "phase": "bid",
      "label": "the bids are shown",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": {
              "calc": "int(you.bid_said) if you.bid_said != '' else bid_min"
            }
          }
        }
      ],
      "text": "Bids for hand {hand_number}: seat 1 bids {players[0].bid}, seat 2 bids {players[1].bid}, seat 3 bids {players[2].bid}."
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
              "key": "discard",
              "value": "$answer"
            }
          },
          {
            "set": {
              "key": "led_suit",
              "value": {
                "calc": "$answer[-1]"
              }
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
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} leads {value}."
      },
      "text": "Trick {trick_in_hand} of hand {hand_number}; trumps are {trump_suit}. You lead: play any card from your hand."
    },
    {
      "use": "ask",
      "phase": "play",
      "label": "second to play",
      "to": {
        "where": "you.seat == leader % num_players + 1"
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
              "key": "discard",
              "value": "$answer"
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} plays {value}."
      },
      "text": "Trick {trick_in_hand} of hand {hand_number}; trumps are {trump_suit}, the led suit is {led_suit}. Play a card: you must follow the led suit if you can; otherwise play any card."
    },
    {
      "use": "ask",
      "phase": "play",
      "label": "third to play",
      "to": {
        "where": "you.seat == (leader + 1) % num_players + 1"
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
              "key": "discard",
              "value": "$answer"
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} plays {value}."
      },
      "text": "Trick {trick_in_hand} of hand {hand_number}; trumps are {trump_suit}, the led suit is {led_suit}. Play a card: you must follow the led suit if you can; otherwise play any card."
    },
    {
      "use": "update",
      "phase": "score",
      "label": "the trick is won",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "trick_points",
            "value": {
              "calc": "((rank_value_A if you.played_card[0] == 'A' else rank_value_K if you.played_card[0] == 'K' else rank_value_Q if you.played_card[0] == 'Q' else rank_value_J if you.played_card[0] == 'J' else rank_value_10) + (trump_bonus if you.played_card[-1] == trump_suit else 0)) if you.played_card[-1] in [trump_suit, led_suit] else 0"
            }
          }
        },
        {
          "set": {
            "key": "trick_winner",
            "value": {
              "calc": "max([[p.trick_points, p.seat] for p in players])[1]"
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
              "calc": "trick_base_points - (penalty_JS if 'JS' in [p.played_card for p in players] else 0) - (penalty_JC if 'JC' in [p.played_card for p in players] else 0) - (penalty_JD if 'JD' in [p.played_card for p in players] else 0) - (penalty_JH if 'JH' in [p.played_card for p in players] else 0)"
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
      ],
      "text": "Seat {trick_winner} wins trick {trick_in_hand} of hand {hand_number} and leads next."
    },
    {
      "use": "update",
      "phase": "score",
      "label": "the end of the hand",
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
            "text": "Seat {player} made their bid exactly."
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
      ],
      "text": "Hand {hand_number} is over. Totals: seat 1 {players[0].total}, seat 2 {players[1].total}, seat 3 {players[2].total}."
    },
    {
      "use": "update",
      "phase": "score",
      "label": "the next round",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "key": "trick_in_hand",
            "value": {
              "calc": "(round - 1) % tricks_per_hand + 1"
            }
          }
        },
        {
          "set": {
            "key": "hand_number",
            "value": {
              "calc": "int((round - 1) / tricks_per_hand) + 1"
            }
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "score",
      "label": "after the last trick",
      "when": {
        "calc": "round > total_rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round > total_rounds"
      },
      "rank_by": "you.total",
      "text": "Winner: {result}. Final totals: Seat 1 {players[0].total}, Seat 2 {players[1].total}, Seat 3 {players[2].total}."
    }
  },
  "limits": {
    "rounds": 36,
    "rounds_max": 40,
    "actions_max": 3000,
    "deadline_s": 120
  },
  "rules": "Three players, seats 1, 2 and 3, play {total_rounds} tricks with a {deck_size}-card deck: A, K, Q, J and 10 of spades (S), clubs (C), diamonds (D) and hearts (H). Within a suit, cards rank A (high), K, Q, J, 10 (low). Everyone starts with a total of 0.\n\nThe game is {num_hands} hands of {tricks_per_hand} tricks; each round is one trick. In hand h the dealer is seat ((h-1) mod 3)+1, so seat 1 deals hand 1, seat 2 hand 2, seat 3 hand 3, seat 1 hand 4, and so on. The seat to the dealer's left, (dealer mod 3)+1, leads the first trick of the hand.\n\nAt the start of each hand the deck is reset to all {deck_size} cards, hands and the discard pile are emptied, and every bid, tricks taken and hand score is set to 0. The deck is shuffled and each seat receives {cards_per_player} cards, seen only by its owner. Card {turned_card_position} is turned face up as the turned card: its suit is trumps and it is out of play. Card {hidden_card_position} is put face down, out of play, and is never revealed.\n\nRight after the deal, all three seats bid at the same moment: each chooses a number from {bid_min} to {bid_max}, the tricks it predicts it will take this hand. All bids are then shown to everyone.\n\nEach trick, the leader plays any card first; its suit is the led suit. Then seat (leader mod 3)+1 plays, then the remaining seat, each seeing the cards already played. A player who holds any card of the led suit must play one of them; a player who holds none may play any card, including a trump. Played cards go to the discard pile and never return.\n\nIf any trump was played, the highest trump wins the trick; otherwise the highest card of the led suit wins. The winner leads the next trick of the hand. The winner adds 1 to tricks taken and adds {trick_base_points} to hand score, minus a penalty for each Jack in the trick: JS {penalty_JS}, JC {penalty_JC}, JD {penalty_JD}, JH {penalty_JH}. A Jack is penalised even if it is a trump, so a trick can score below zero (a trick with JH and JS scores 2-4-1 = -3). The players who do not win the trick score nothing for it.\n\nAfter the sixth trick of a hand, each player whose tricks taken equals their bid adds {exact_bid_bonus} to hand score; a player who missed their bid, over or under, gets no bonus. Every player then adds hand score to their total, and the totals are announced.\n\nAfter round {total_rounds} the game ends. The highest total wins; players tied for the highest total share the result (a draw)."
}
```
````
